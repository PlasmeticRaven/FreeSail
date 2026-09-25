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


F, S = "frigate", "schooner"

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
    (F, "let go the best bower", no(["no such part as the best bower"], UnknownNounError)),
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
    (F, "splice the main brace", no(["not an order this ship understands", "begins with a verb"])),
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
    (F, "close reef the fore topsail", no()),  # 'close' is a modifier, not a verb
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
        ok(evo="brace", subjects=["main.yard"], params={"target_deg": -15.0}),
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
    (F, "ease the spanker sheet", ok(kind="line.eased", text=["mizzen spanker now 5°"])),
    (F, "ease the spanker sheet a fathom", ok(kind="line.eased", text=["5° off the centreline"])),
    (
        F,
        "ease the spanker sheet two fathoms",
        ok(kind="line.eased", text=["10° off the centreline"]),
    ),
    (F, "ease the spanker sheet handsomely", ok(kind="line.eased", text=["handsomely"])),
    (F, "start the spanker sheet", ok(kind="line.eased")),
    (F, "haul the spanker sheet", no(["already hard in"])),
    (F, "haul the fore topsail halyard", no(["already hauled home"])),
    (F, "ease the fore topsail halyard", ok(kind="line.eased", text=["nine-tenths hauled"])),
    (F, "ease the fore topsail halyard a little", ok(kind="line.eased", text=["nine-tenths"])),
    (F, "check the fore topsail halyard", ok(kind="line.eased")),
    (F, "ease the jib sheet, lee", ok(kind="line.eased", text=["larboard (lee) jib sheet"])),
    (F, "haul the jib sheet", no(["Which jib sheet"])),
    (F, "let go the fore topsail sheet, starboard", ok(kind="line.let_go", text=["ran free"])),
    (F, "let go the starboard fore topsail sheet", ok(kind="line.let_go")),
    (F, "cast off the fore course tack, weather", ok(kind="line.let_go")),
    (F, "belay the fore topsail halyard", ok(kind="line.belay", text=["Belayed"])),
    (F, "make fast the main topsail halyard", ok(kind="line.belay")),
    (F, "haul the spanker peak halyard", no(["already hauled home"])),
    (F, "ease the spanker peak halyard", ok(kind="line.eased", text=["mizzen gaff peak halyard"])),
    (F, "ease the mainsail sheet, lee", ok(kind="line.eased", text=["main course sheet"])),
    (F, "ease the main sheet", no(["no such part as the main sheet"], UnknownNounError)),
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
    (S, "ease the main sheet", ok(kind="line.eased", text=["main sail now 5°"])),
    (S, "ease the main sheet a fathom", ok(kind="line.eased", text=["5° off"])),
    (S, "ease the mainsail sheet two fathoms", ok(kind="line.eased", text=["10° off"])),
    (S, "ease the fore sheet, lee", ok(kind="line.eased", text=["larboard (lee) fore sail sheet"])),
    (S, "haul the fore sheet, lee", no(["already hard in"])),
    (S, "haul the jib sheet", no(["Which jib sheet"])),
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
    (S, "splice the mainbrace", no(["not an order this ship understands"])),
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
    yard = ship.spars["main.yard"]  # limit 38 degrees
    for _ in range(7):
        orders.handle(ship, "haul the larboard main brace")
    assert yard.brace_angle == pytest.approx(units.deg_to_rad(35))
    _, log, _ = orders.handle(ship, "haul the larboard main brace")
    assert yard.brace_angle == pytest.approx(yard.brace_limit)
    assert "38°" in log and "starboard tack" in log
    with pytest.raises(OrderError, match="will come no further"):
        orders.handle(ship, "haul the larboard main brace")
    assert yard.brace_angle == pytest.approx(yard.brace_limit)


def test_hauling_by_fathoms_takes_several_steps():
    ship, _ = make("frigate")
    yard = ship.spars["fore.yard"]
    orders.handle(ship, "haul the lee fore brace two fathoms")
    assert yard.brace_angle == pytest.approx(units.deg_to_rad(10))


def test_sheet_of_a_fore_and_aft_sail_changes_its_angle():
    ship, _ = make("schooner")
    sail = ship.sails["main.sail"]
    assert sail.sheet_angle == 0.0
    with pytest.raises(OrderError, match="already hard in"):
        orders.handle(ship, "haul the main sheet")
    orders.handle(ship, "ease the main sheet")
    assert sail.sheet_angle == pytest.approx(units.deg_to_rad(5))
    orders.handle(ship, "ease the main sheet three fathoms")
    assert sail.sheet_angle == pytest.approx(units.deg_to_rad(20))
    _, log, _ = orders.handle(ship, "haul the main sheet")
    assert sail.sheet_angle == pytest.approx(units.deg_to_rad(15))
    assert "15° off the centreline" in log


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
    assert by_yard["fore.yard"]["target_deg"] == 38.0
    assert by_yard["fore.topsail.yard"]["target_deg"] == 42.0
    assert by_yard["fore.yard"]["target_angle"] == pytest.approx(
        ship.spars["fore.yard"].brace_limit
    )
    runner.started.clear()
    orders.handle(ship, "brace the fore yards sharp up on the larboard tack")
    assert all(p["target_deg"] < 0 for _, _, p in runner.started)
    runner.started.clear()
    orders.handle(ship, "brace the fore yards up on the larboard tack")
    assert all(p["target_deg"] == -30.0 for _, _, p in runner.started)
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
    assert event.kind == "evolution.started"
    assert world.journal == [(0, "captain", "set the fore topsail")]
    assert [e.kind for e in world.log][-2:] == ["order.accepted", "evolution.started"]
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
