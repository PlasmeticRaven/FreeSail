"""Standing orders (spec M4 §3 and §4): the grammar's acceptances and refusals as a table
against both ships, the runtime's guards with synthetic readings, the conflict rule with a
synthetic officer, determinism of firing, the book, the drivers, and the seams package 26
builds on (`parse_condition`, the `Rule` constructor).
"""

from __future__ import annotations

import io
import math
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from freesail import units
from freesail.api import readings as R
from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.world import Scenario, World
from freesail.orders import complete
from freesail.orders.errors import OrderError
from freesail.ship.graph import Ship
from freesail.ship.loader import load_spec
from freesail.ship.parts import SailState
from freesail.standing import (
    STANDING_DWELL_S,
    Rule,
    Trigger,
    parse_condition,
    parse_duration,
    parse_standing,
    recognises,
)
from freesail.ui.console import Console
from freesail.ui.server import Driver

ROOT = Path(__file__).resolve().parents[1]
SHIP_FILES = {
    "frigate": ROOT / "data" / "ships" / "frigate-36.yaml",
    "schooner": ROOT / "data" / "ships" / "topsail-schooner.yaml",
    "cutter": ROOT / "data" / "ships" / "cutter.yaml",
    "brig": ROOT / "data" / "ships" / "brig.yaml",
}
SPECS = {name: load_spec(path) for name, path in SHIP_FILES.items()}
FRIGATE = str(SHIP_FILES["frigate"])
F, S, C, B = "frigate", "schooner", "cutter", "brig"

# the six starter routines of spec §3, which are also the primer's sentences
NIGHT = (
    'standing order "night routine": at sunset then take in the studdingsails; take in the royals'
)
MORNING = (
    'standing order "morning sail": at sunrise, if the true wind is under 20 knots '
    "then set the royals"
)
SHORTEN = (
    'standing order "shorten sail for weather": when the true wind exceeds 30 knots for '
    "2 minutes then take in the studdingsails; take in the royals; reef the topsails, one reef"
)
KEEP_FULL = (
    'standing order "keep her full": when the apparent wind is forward of 55 degrees '
    "then bear away one point"
)
HEAVY = (
    'standing order "heavy weather": when the true wind exceeds 40 knots for 5 minutes then '
    "send down the topgallant masts; shift the fore topmast staysail for the fore storm "
    "staysail; close reef the topsails"
)
WELL = 'standing order "sound the well": every glass then sound the well'


def make(which: str, tack: str = "starboard") -> Ship:
    ship = Ship(SPECS[which])
    ship.dyn.apparent_wind_angle = math.radians(40 if tack == "starboard" else -40)
    ship.dyn.apparent_wind_speed = 8.0
    return ship


# ---------------------------------------------------------------------------
# The table
# ---------------------------------------------------------------------------


@dataclass
class ok:
    kind: str  # when | at | every
    reading: str | None = None  # the first clause's reading id
    op: str | None = None  # and its comparison
    value: Any = None
    duration: int | None = None
    event: str | None = None
    interval: int | None = None
    actions: int | None = None
    given_by: str = "captain"
    params: tuple[str, ...] | None = None
    clauses: int | None = None
    if_reading: str | None = None


@dataclass
class no:
    mentions: list[str] = field(default_factory=list)


TABLE: list[tuple[str, str, ok | no]] = [
    # -- the starter routines (spec §3, §6) --------------------------------------------
    (F, NIGHT, ok("at", event="sunset", actions=2)),
    (F, MORNING, ok("at", event="sunrise", actions=1, if_reading="true_wind_speed")),
    (F, SHORTEN, ok("when", "true_wind_speed", "gt", 30.0, duration=120, actions=3)),
    (F, KEEP_FULL, ok("when", "apparent_wind_angle", "forward_of", 55.0, actions=1)),
    (F, HEAVY, ok("when", "true_wind_speed", "gt", 40.0, duration=300, actions=3)),
    (F, WELL, ok("every", interval=1800, actions=1)),  # held, not refused (package 33c)
    # -- triggers ------------------------------------------------------------------------
    (
        F,
        'standing order "bells": at eight bells then call all hands',
        ok("at", event="eight bells"),
    ),
    (
        F,
        'standing order "w": at the change of the watch then trim sails',
        ok("at", event="the change of the watch"),
    ),
    (
        F,
        'standing order "w": at change of the watch then trim sails',
        ok("at", event="the change of the watch"),
    ),
    (
        F,
        'standing order "s": at a strain warning then reef the topsails, one reef',
        ok("at", event="a strain warning"),
    ),
    (
        F,
        'standing order "b": at a sail blown out then shorten sail',
        ok("at", event="a sail blown out"),
    ),
    (F, 'standing order "g": every glass then trim sails', ok("every", interval=1800)),
    (F, 'standing order "g": every bell then trim sails', ok("every", interval=1800)),
    (F, 'standing order "g": every 20 minutes then trim sails', ok("every", interval=1200)),
    (F, 'standing order "g": every half an hour then trim sails', ok("every", interval=1800)),
    (F, 'standing order "g": every two hours then trim sails', ok("every", interval=7200)),
    (F, 'standing order "g": every watch then trim sails', ok("every", interval=14400)),
    (
        F,
        'standing order "g": every hour, if the speed is under 3 knots then trim sails',
        ok("every", interval=3600, if_reading="speed"),
    ),
    (
        F,
        'standing order "d": when the heel exceeds 15 degrees for a glass '
        "then reef the topsails, one reef",
        ok("when", "heel", "gt", 15.0, duration=1800),
    ),
    (
        F,
        'standing order "d": when the speed is under 2 knots for 90 seconds then trim sails',
        ok("when", "speed", "lt", 2.0, duration=90),
    ),
    (
        F,
        'standing order "d": when the speed is under 2 knots for half an hour then trim sails',
        ok("when", "speed", "lt", 2.0, duration=1800),
    ),
    # -- the wind ---------------------------------------------------------------------------
    (
        F,
        'standing order "b": when the true wind backs two points then wear ship',
        ok("when", "true_wind_from", "backs", 2.0),
    ),
    (
        F,
        'standing order "v": when the wind veers a point and a half then tack ship',
        ok("when", "true_wind_from", "veers", 1.5),
    ),
    (
        F,
        'standing order "v": when the wind veers half a point then trim sails',
        ok("when", "true_wind_from", "veers", 0.5),
    ),
    (
        F,
        'standing order "nw": when the true wind is from the north-west then steer west',
        ok("when", "true_wind_from", "from", math.radians(315)),
    ),
    (
        F,
        'standing order "nw": when the true wind is from NW then steer west',
        ok("when", "true_wind_from", "from", math.radians(315)),
    ),
    (
        F,
        'standing order "u": when the true wind is under 20 knots then set the royals',
        ok("when", "true_wind_speed", "lt", 20.0),
    ),
    (
        F,
        'standing order "u": when the true wind is over 20 then set the royals',
        ok("when", "true_wind_speed", "gt", 20.0),
    ),
    (
        F,
        'standing order "u": when the true wind is below 20 knots then set the royals',
        ok("when", "true_wind_speed", "lt", 20.0),
    ),
    (
        F,
        'standing order "a": when the apparent wind is abaft the beam '
        "then set the studdingsails, both sides",
        ok("when", "apparent_wind_angle", "abaft", 90.0),
    ),
    (
        F,
        'standing order "a": when the apparent wind is forward of the beam '
        "then take in the studdingsails",
        ok("when", "apparent_wind_angle", "forward_of", 90.0),
    ),
    (
        F,
        'standing order "a": when the apparent wind is abaft 120 degrees '
        "then set the studdingsails, both sides",
        ok("when", "apparent_wind_angle", "abaft", 120.0),
    ),
    (
        F,
        'standing order "a": when the apparent wind is forward of five points then come up',
        ok("when", "apparent_wind_angle", "forward_of", 56.25),
    ),
    (
        F,
        'standing order "a": when the apparent wind exceeds 25 knots '
        "then reef the topsails, one reef",
        ok("when", "apparent_wind_speed", "gt", 25.0),
    ),
    (
        F,
        'standing order "a": when the apparent wind is on the larboard bow then tack ship',
        ok("when", "apparent_wind_angle", "side", "larboard"),
    ),
    # -- the ship -----------------------------------------------------------------------------
    (
        F,
        'standing order "l": when the leeway is over 5 degrees then come up one point',
        ok("when", "leeway", "gt", 5.0),
    ),
    (
        F,
        'standing order "h": when the helm exceeds 15 degrees then trim sails',
        ok("when", "helm", "gt", 15.0),
    ),
    (
        F,
        'standing order "h": when the heading is east of south then steer south',
        ok("when", "heading", "east_of", math.pi),
    ),
    (
        F,
        'standing order "h": when the course is west of north then steer north',
        ok("when", "course", "west_of", 0.0),
    ),
    (
        F,
        'standing order "h": when the heading is south-west by west then steer south',
        ok("when", "heading", "point", math.radians(236.25)),
    ),
    (
        F,
        'standing order "m": when the watch is the middle watch and the true wind exceeds '
        "25 knots then take in the topgallants",
        ok("when", "watch", "is", "middle watch", clauses=2),
    ),
    (
        F,
        'standing order "m": when the watch is not the first watch then trim sails',
        ok("when", "watch", "is_not", "first watch"),
    ),
    (
        F,
        'standing order "t": when the time is eight bells then call all hands',
        ok("when", "time", "is", 8),
    ),
    # -- sails and parts by name --------------------------------------------------------------
    (
        F,
        'standing order "s": when the fore royal is shaking then take in the fore royal',
        ok("when", "sail", "is", "shaking", params=("fore.royal",)),
    ),
    (
        F,
        'standing order "s": when the main topsail is aback then fill away',
        ok("when", "sail", "is", "aback", params=("main.topsail",)),
    ),
    (
        F,
        'standing order "s": when the spanker is not set then set the spanker',
        ok("when", "sail", "is_not", "set", params=("mizzen.spanker",)),
    ),
    (
        F,
        'standing order "s": when the fore course is blown out then bend a new fore course',
        ok("when", "sail", "is", "blown out", params=("fore.course",)),
    ),
    (
        F,
        'standing order "r": when the royals are set and the true wind exceeds 25 knots '
        "then take in the royals",
        ok(
            "when",
            "sail",
            "is",
            "set",
            params=("fore.royal", "main.royal", "mizzen.royal"),
            clauses=2,
        ),
    ),
    (
        F,
        'standing order "s": when the starboard fore topmast studdingsail is shaking '
        "then take in the fore topmast studdingsail, starboard",
        ok("when", "sail", "is", "shaking", params=("fore.topmast.studdingsail.starboard",)),
    ),
    (
        F,
        'standing order "y": when the fore royal yard is straining then take in the fore royal',
        ok("when", "strain", "straining", R.STRAINING_RATIO, params=("fore.royal.yard",)),
    ),
    (
        F,
        'standing order "y": when the fore royal is straining then take in the fore royal',
        ok("when", "strain", "straining", R.STRAINING_RATIO, params=("fore.royal",)),
    ),
    (
        F,
        'standing order "y": when the main topmast exceeds the rating '
        "then send down the topgallant masts",
        ok("when", "strain", "gt", 1.0, params=("main.topmast",)),
    ),
    (
        F,
        'standing order "r": when the strain exceeds the rating then shorten sail',
        ok("when", "strain", "gt", 1.0, params=()),
    ),
    (
        F,
        'standing order "r": when the strain exceeds 1.2 then shorten sail',
        ok("when", "strain", "gt", 1.2),
    ),
    (
        F,
        'standing order "r": when the strain is over 1.2 for 2 minutes then shorten sail',
        ok("when", "strain", "gt", 1.2, duration=120),
    ),
    # -- the hands ------------------------------------------------------------------------------
    (
        F,
        'standing order "w": when the hands on deck are worn out then pipe down',
        ok("when", "hands_on_deck", "is", "worn out"),
    ),
    (
        F,
        'standing order "w": when the watch below are fresh then relieve the watch',
        ok("when", "watch_below", "is", "fresh"),
    ),
    (
        F,
        'standing order "w": when the hands on deck are under 40 then call all hands',
        ok("when", "hands_on_deck", "lt", 40.0),
    ),
    (
        F,
        'standing order "w": when the hands on deck exceed 200 then pipe down',
        ok("when", "hands_on_deck", "gt", 200.0),
    ),
    # -- form: officers, quotes, case, spacing --------------------------------------------------
    (
        F,
        'standing order "o" by the master: at eight bells then trim sails',
        ok("at", event="eight bells", given_by="master"),
    ),
    (
        F,
        'standing order "o" by the first lieutenant: at eight bells then trim sails',
        ok("at", event="eight bells", given_by="first lieutenant"),
    ),
    (
        F,
        'standing order "o" by a midshipman: at eight bells then trim sails',
        ok("at", event="eight bells", given_by="midshipman"),
    ),
    (
        F,
        "Standing Order “Curly Quotes”: at Sunset then Take in the Royals.",
        ok("at", event="sunset", actions=1),
    ),
    (F, "standing order 'single': at sunset then take in the royals", ok("at", event="sunset")),
    (
        F,
        '  standing   order "spaced" :  at  sunset  then  take in the royals ; '
        "take in the studdingsails ",
        ok("at", event="sunset", actions=2),
    ),
    (
        F,
        'standing order "x": when the true wind exceeds 30 knots then shorten sail',
        ok("when", "true_wind_speed", "gt", 30.0, actions=1),
    ),
    # -- the schooner -----------------------------------------------------------------------------
    (
        S,
        'standing order "night": at sunset then take in the gaff topsail',
        ok("at", event="sunset"),
    ),
    (
        S,
        'standing order "fore": when the fore topsail is shaking then trim sails',
        ok("when", "sail", "is", "shaking", params=("fore.topsail",)),
    ),
    (
        S,
        'standing order "reef": when the true wind exceeds 25 knots for 2 minutes '
        "then reef the mainsail, one reef",
        ok("when", "true_wind_speed", "gt", 25.0, duration=120),
    ),
    (S, 'standing order "g": every glass then trim sails', ok("every", interval=1800)),
    (
        S,
        'standing order "j": when the jib is aback then fill away',
        ok("when", "sail", "is", "aback", params=("jib",)),
    ),
    (
        S,
        'standing order "x": when the mizzen royal is shaking then trim sails',
        no(["is not a reading the ship has"]),
    ),
    (
        S,
        'standing order "x": at sunset then take in the royals',
        no(["'take in the royals' is refused", "no such part"]),
    ),
    # -- package 32b: the cutter, whose starter routines name parts she lacks ------------------
    (C, NIGHT, no(["'take in the studdingsails' is refused", "no such part as the studdingsails"])),
    (C, MORNING, no(["'set the royals' is refused", "no such part as the royals"])),
    (C, SHORTEN, no(["'take in the studdingsails' is refused"])),
    (C, KEEP_FULL, ok("when", "apparent_wind_angle", "forward_of", 55.0, actions=1)),
    (
        C,
        HEAVY,
        no(["'shift the fore topmast staysail for the fore storm staysail' is refused"]),
    ),
    (C, WELL, ok("every", interval=1800, actions=1)),  # held (package 33c)
    (
        C,
        'standing order "night": at sunset then take in the gaff topsail; take in the topgallant',
        ok("at", event="sunset", actions=2),
    ),
    (
        C,
        'standing order "morning": at sunrise, if the true wind is under 20 knots '
        "then set the topgallant",
        ok("at", event="sunrise", actions=1, if_reading="true_wind_speed"),
    ),
    (
        C,
        'standing order "reef": when the true wind exceeds 25 knots for 2 minutes '
        "then reef the mainsail, two reefs; reef the topsail",
        ok("when", "true_wind_speed", "gt", 25.0, duration=120, actions=2),
    ),
    (
        C,
        'standing order "bowsprit": when the true wind exceeds 35 knots for 5 minutes then '
        "take in the jib; reef the bowsprit; shift the jib for the storm jib",
        ok("when", "true_wind_speed", "gt", 35.0, duration=300, actions=3),
    ),
    (
        C,
        'standing order "heavy": when the true wind exceeds 40 knots for 5 minutes then send '
        "down the topgallant mast; shift the mainsail for the storm trysail; run in the bowsprit",
        ok("when", "true_wind_speed", "gt", 40.0, duration=300, actions=3),
    ),
    (
        C,
        'standing order "out": when the true wind is under 20 knots for 10 minutes then '
        "rig out the bowsprit; set the jib",
        ok("when", "true_wind_speed", "lt", 20.0, duration=600, actions=2),
    ),
    (
        C,
        'standing order "j": when the jib is aback then fill away',
        ok("when", "sail", "is", "aback", params=("jib",)),
    ),
    (
        C,
        'standing order "main": when the mainsail is shaking then trim sails',
        ok("when", "sail", "is", "shaking", params=("main.sail",)),
    ),
    (
        C,
        'standing order "fore": when the foresail is shaking then trim sails',
        ok("when", "sail", "is", "shaking", params=("fore.staysail",)),
    ),
    (
        C,
        'standing order "sq": when the square sail is aback then trim sails',
        ok("when", "sail", "is", "aback", params=("square_sail",)),
    ),
    (
        C,
        'standing order "x": when the fore topsail is shaking then trim sails',
        no(["'the fore topsail is shaking' is not a reading the ship has"]),
    ),
    (
        C,
        'standing order "x": when the spanker is shaking then trim sails',
        no(["is not a reading the ship has"]),
    ),
    (C, 'standing order "g": every glass then trim sails', ok("every", interval=1800)),
    (
        C,
        'standing order "x": when the true wind exceeds 30 knots then shorten sail',
        ok("when", "true_wind_speed", "gt", 30.0, actions=1),
    ),
    # -- package 32b: the brig, on whom the starter routines all read -----------------------------
    (B, NIGHT, ok("at", event="sunset", actions=2)),
    (B, MORNING, ok("at", event="sunrise", actions=1, if_reading="true_wind_speed")),
    (B, SHORTEN, ok("when", "true_wind_speed", "gt", 30.0, duration=120, actions=3)),
    (B, KEEP_FULL, ok("when", "apparent_wind_angle", "forward_of", 55.0, actions=1)),
    (B, HEAVY, ok("when", "true_wind_speed", "gt", 40.0, duration=300, actions=3)),
    (B, WELL, ok("every", interval=1800, actions=1)),  # held (package 33c)
    (
        B,
        'standing order "reef": when the true wind exceeds 25 knots for 2 minutes '
        "then reef the topsails, one reef; reef the spanker, one reef",
        ok("when", "true_wind_speed", "gt", 25.0, duration=120, actions=2),
    ),
    (
        B,
        'standing order "heavy": when the true wind exceeds 40 knots for 5 minutes then send '
        "down the topgallant masts; shift the fore topmast staysail for the fore storm staysail; "
        "shift the spanker for the storm trysail; close reef the topsails",
        ok("when", "true_wind_speed", "gt", 40.0, duration=300, actions=4),
    ),
    (
        B,
        'standing order "sp": when the spanker is shaking then trim sails',
        ok("when", "sail", "is", "shaking", params=("main.spanker",)),
    ),
    (
        B,
        'standing order "x": when the fore topsail is shaking then trim sails',
        ok("when", "sail", "is", "shaking", params=("fore.topsail",)),
    ),
    (
        B,
        'standing order "x": when the mizzen topsail is shaking then trim sails',
        no(["is not a reading the ship has", "did you mean the main topsail"]),
    ),
    (
        B,
        'standing order "x": at sunset then take in the gaff topsail',
        no(["'take in the gaff topsail' is refused", "no such part"]),
    ),
    (B, 'standing order "g": every glass then trim sails', ok("every", interval=1800)),
    # -- refusals, each naming the word ------------------------------------------------------------
    (
        F,
        'standing order "x": when the true wind is shaking then set the royals',
        no(["'the true wind' cannot be 'shaking'", "a wind is compared in knots or points"]),
    ),
    (
        F,
        'standing order "x": when the heel exceeds 15 knots then reef the topsails, one reef',
        no(["'the heel' is compared in degrees, not knots"]),
    ),
    (
        F,
        'standing order "x": when the fore royal exceeds 30 knots then trim sails',
        no(["'the fore royal' is compared", "not knots"]),
    ),
    (
        F,
        'standing order "x": when the fore royal is falling then trim sails',
        no(["'the fore royal' cannot be 'falling'", "a sail is compared by its state"]),
    ),
    (
        F,
        'standing order "x": when the apparent wind exceeds 60 degrees then bear away',
        no(["compared on the bow", "is forward of 60 degrees", "is abaft 60 degrees"]),
    ),
    (
        F,
        'standing order "x": when the watch is the dog watch then trim sails',
        no(["'the watch' cannot be 'the dog watch'", "is the middle watch"]),
    ),
    (F, 'standing order "x": when the true wind backs then wear ship', no(["how many points"])),
    (
        F,
        'standing order "x": when the true wind backs two degrees then wear ship',
        no(["backs in points"]),
    ),
    (
        F,
        'standing order "x": when the true wind is from the moon then steer west',
        no(["what point", "compass point"]),
    ),
    (
        F,
        'standing order "x": when the well is over three feet then heave to',
        no(["The ship has no well to sound yet; that reading comes with the world."]),
    ),
    # the lead's cast (package 33a): `the depth` is the last cast's, in fathoms
    (
        F,
        'standing order "x": when the depth is under 10 fathoms then heave to',
        ok("when", "depth", "lt", 10.0, actions=1),
    ),
    (
        F,
        'standing order "x": when a sail in sight is near then clear for action',
        # a reading since package 35 (the lookout's other sail): compared as the land is
        no(["'a sail in sight' cannot be 'near'", "in sight or not in sight"]),
    ),
    (
        F,
        'standing order "x": when the barometer falls then shorten sail',
        # the glass is a reading since package 30 (spec M5 §5); 'falls' is not its word
        no(["'the barometer' cannot be 'falls'", "is falling"]),
    ),
    (
        F,
        'standing order "x": when the true wind exceeds 30 knots or the heel exceeds '
        "15 degrees then shorten sail",
        no(["expected 'and'", "not 'or'"]),
    ),
    (
        F,
        'standing order "x": when the true wind exceeds 30 knots for two fathoms then shorten sail',
        no(["'two fathoms' is not a duration"]),
    ),
    (
        F,
        'standing order "x": when the true wind exceeds 30 knots for then shorten sail',
        no(["for how long"]),
    ),
    (
        F,
        'standing order "x": when the true wind then shorten sail',
        no(["'the true wind' compared how?"]),
    ),
    (F, 'standing order "x": when then shorten sail', no(["when what?"])),
    (
        F,
        'standing order "x": at dawn then set the royals',
        no(["'at dawn' names no event", "sunrise"]),
    ),
    # the lookout's sighting is an event since package 33a named it (the line is package
    # 32's); `clear for action` is still no order of the ship's
    (
        F,
        'standing order "x": at a sighting then clear for action',
        no(["'clear for action' is refused"]),
    ),
    (F, 'standing order "x": at a landfall then heave the lead', ok("at", event="a landfall")),
    (F, 'standing order "x": at noon then work up the reckoning', ok("at", event="noon")),
    (
        F,
        'standing order "x": at sunset then set the royls',
        no(["In standing order 'x', 'set the royls' is refused", "did you mean the royals"]),
    ),
    (
        F,
        'standing order "x": at sunset then set the royals; splice the mainbrace',
        no(["'splice the mainbrace' is refused", "no such part as the mainbrace"]),
    ),
    (
        F,
        'standing order "x": at sunset then muster',
        no(["'muster' is refused", "console command"]),
    ),
    (
        F,
        'standing order "x": at sunset then standing order "y": at sunrise then set the royals',
        no(["is a standing order itself"]),
    ),
    (
        F,
        'standing order "x": every fortnight then trim sails',
        no(["'fortnight' is not an interval"]),
    ),
    (F, 'standing order "x": every then trim sails', no(["every what?"])),
    (F, "standing order: at sunset then set the royals", no(["named in quotes"])),
    (F, 'standing order "": at sunset then set the royals', no(["needs a name"])),
    (F, 'standing order "x: at sunset then set the royals', no(["closing quote"])),
    (F, 'standing order "x" at sunset then set the royals', no(["colon"])),
    (F, 'standing order "x": at sunset set the royals', no(["after 'then'"])),
    (F, 'standing order "x": at sunset then', no(["gives no order after 'then'"])),
    (F, 'standing order "x": then set the royals', no(["says nothing to wait for"])),
    (
        F,
        'standing order "x": sometimes the wind blows then set the royals',
        no(["begins with when, at or every, not 'sometimes'"]),
    ),
    (
        F,
        'standing order "x" by the purser: at sunset then set the royals',
        no(["'purser' is no officer", "the master"]),
    ),
    (
        F,
        'standing order "x": when the true wind exceeds lots then trim sails',
        no(["what number"]),
    ),
    # package 37l: a number in words is a number, by the one reader for numbers
    (
        F,
        'standing order "x": when the true wind exceeds thirty then trim sails',
        ok("when", reading="true_wind_speed", op="gt", value=30.0),
    ),
    # -- package 31c: the weather's events, the new comparisons, the station verbs ------
    # an event that is a reading's change is kept as a `when` of its condition
    (
        F,
        'standing order "g": at the glass falling fast then take in the royals',
        ok("when", "tendency", "is", "falling fast", event="the glass falling fast"),
    ),
    (
        F,
        'standing order "g": at glass falling fast then take in the royals',
        ok("when", "tendency", "is", "falling fast", event="the glass falling fast"),
    ),
    (
        F,
        'standing order "t": at the glass turning then trim sails',
        ok("when", "tendency", "is", "turning", event="the glass turning"),
    ),
    (
        F,
        'standing order "s": at a wind shift then trim sails',
        ok("when", "mean_true_wind_from", "shifts", (1.0, 1.0), event="a wind shift"),
    ),
    (
        F,
        'standing order "u": at the sea getting up, if the true wind exceeds 30 knots then '
        "reef the topsails, one reef",
        ok(
            "when", "sea", "gets_up", None, event="the sea getting up", if_reading="true_wind_speed"
        ),
    ),
    (
        F,
        'standing order "c": at a change in the sky then trim sails',
        ok("at", event="a change in the sky"),
    ),
    (
        F,
        'standing order "t": when the glass is turning then trim sails',
        ok("when", "tendency", "is", "turning"),
    ),
    (
        F,
        'standing order "u": when the sea gets up then trim sails',
        ok("when", "sea", "gets_up", None),
    ),
    (
        F,
        'standing order "u": when the sea is getting up for 5 minutes then trim sails',
        ok("when", "sea", "gets_up", None, duration=300),
    ),
    (
        F,
        'standing order "x": when the heel gets up then trim sails',
        no(["'the heel' cannot be 'gets up'"]),
    ),
    (F, 'standing order "x": at the glass rising then trim sails', no(["names no event"])),
    # the station verbs after 'then' (the owner's finding at gate 5a): tell and ask, to a
    # station aboard, resolved when the order is given
    (
        F,
        'standing order "sea": when the sea is heavy then tell the watcher the sea is getting up',
        ok("when", "sea", "is", "heavy", actions=1),
    ),
    (
        F,
        'standing order "glass": every glass then ask the watcher how the glass stands; '
        "say to the watcher keep a weather eye",
        ok("every", interval=1800, actions=2),
    ),
    (
        F,
        'standing order "w": at eight bells then tell watcher the watch is changed; trim sails',
        ok("at", event="eight bells", actions=2),
    ),
    (
        # the lookout's station is aboard since package 41: a book may tell it, and the
        # firing is refused in words if nobody mans it then, as the watcher's is
        F,
        'standing order "look": at sunset then tell the lookout to look sharp',
        ok("at", event="sunset", actions=1),
    ),
    (
        # the officer of the watch is a station aboard (package 37): a book may ask it
        F,
        'standing order "o": at sunset then ask the officer of the watch how she heads',
        ok("at", event="sunset", actions=1),
    ),
    (
        F,
        'standing order "o": at sunset then ask the lookout what she sees',
        ok("at", event="sunset", actions=1),
    ),
    (
        # a station the ship has not got (package 41: the stations are the World's
        # binding) is refused with the stations aboard named
        F,
        'standing order "o": at sunset then ask the purser what she sees',
        no(["there is no purser aboard yet", "tell or ask the watcher or the officer"]),
    ),
    (
        F,
        'standing order "c": at sunset then ask the captain whether to shorten sail',
        no(["a standing order speaks for the captain"]),
    ),
    (
        F,
        'standing order "d": at sunset then stand down the watcher',
        no(["the captain's own to say to a station, not a standing order's"]),
    ),
    (
        F,
        'standing order "j": at sunset then show the watcher\'s journal',
        no(["the captain's own to say to a station"]),
    ),
    (F, 'standing order "e": at sunset then tell the watcher', no(["Tell the watcher what?"])),
    (F, 'standing order "e": at sunset then ask the watcher', no(["Ask the watcher what?"])),
]


@pytest.mark.parametrize("which,text,expect", TABLE, ids=[f"{w}: {t[:60]}" for w, t, _ in TABLE])
def test_table(which: str, text: str, expect: ok | no):
    ship = make(which)
    if isinstance(expect, no):
        with pytest.raises(OrderError) as info:
            parse_standing(ship, text)
        message = str(info.value)
        for m in expect.mentions:
            assert m in message, f"{text!r}: expected {m!r} in {message!r}"
        return
    rule = parse_standing(ship, text)
    t = rule.trigger
    assert t.kind == expect.kind
    assert rule.given_by == expect.given_by
    if expect.duration is not None:
        assert t.duration_s == expect.duration
    if expect.event is not None:
        assert t.event == expect.event
    if expect.interval is not None:
        assert t.interval_s == expect.interval
    if expect.actions is not None:
        assert len(rule.actions) == expect.actions
    if expect.reading is not None:
        assert t.condition is not None
        clause = t.condition.clauses[0]
        assert clause.reading == expect.reading, clause
        assert clause.comparison.op == expect.op, clause
        if isinstance(expect.value, float):
            assert clause.comparison.value == pytest.approx(expect.value)
        else:
            assert clause.comparison.value == expect.value
        if expect.params is not None:
            assert tuple(clause.params) == expect.params
        if expect.clauses is not None:
            assert len(t.condition.clauses) == expect.clauses
    if expect.if_reading is not None:
        assert rule.condition is not None
        assert rule.condition.clauses[0].reading == expect.if_reading
    assert rule.text == " ".join(text.split())


def test_table_is_large_enough():
    assert len(TABLE) >= 100
    assert sum(1 for _, _, e in TABLE if isinstance(e, no)) >= 30


def test_recognises_the_dialect_and_nothing_else():
    assert recognises('standing order "x": at sunset then set the royals') == "standing order"
    assert recognises("standing orders") == "standing orders"
    assert recognises("list the standing orders") == "standing orders"
    assert recognises('belay standing order "x"') == "belay standing order"
    assert recognises("belay all standing orders") == "belay all standing orders"
    assert recognises("belay the fore topsail sheet") is None
    assert recognises("set the royals") is None
    assert recognises("read the standing orders from data/x.orders") is None


def test_parse_duration_words():
    assert parse_duration(["2", "minutes"]) == 120
    assert parse_duration(["a", "glass"]) == 1800
    assert parse_duration(["an", "hour"]) == 3600
    assert parse_duration(["a", "watch"]) == 14400
    assert parse_duration(["half", "an", "hour"]) == 1800
    assert parse_duration(["three", "hours"]) == 10800


# ---------------------------------------------------------------------------
# Synthetic readings: swap a row of the registry for the test and put it back
# ---------------------------------------------------------------------------


@pytest.fixture
def synthetic():
    """`synthetic(id, fn)` makes reading `id` return `fn(world)`; restored at teardown."""
    originals: dict[str, R.Reading] = {}

    def set_reading(id: str, fn) -> None:
        row = R.REGISTRY.get(id)
        originals.setdefault(id, row)
        R.REGISTRY.add(
            R.Reading(id, row.words, row.kind, row.unit, lambda w, p: fn(w), row.parametric)
        )

    yield set_reading
    for row in originals.values():
        R.REGISTRY.add(row)


def point_world(start: datetime = datetime(1805, 6, 1, 7, 40)) -> World:
    """The point ship: a cheap clock for the runtime's timing, with `steer` for an order."""
    return World(seed=3, scenario=Scenario(start_time=start, gustiness=0.0, variability=0.0))


def rule_of(text: str, world: World, actions: list[str] | None = None, **kw) -> Rule:
    """A rule built from the pieces, as package 26's decorators build one: the condition
    as dialect text, the actions as order texts."""
    if text.startswith("at "):
        trigger = Trigger("at", text, event=text[3:])
    elif text.startswith("every "):
        trigger = Trigger("every", text, interval_s=parse_duration(text.split()[1:]))
    else:
        words = text[5:]
        duration = 0
        if " for " in words:
            words, _, tail = words.rpartition(" for ")
            duration = parse_duration(tail.split())
        trigger = Trigger("when", text, condition=parse_condition(words), duration_s=duration)
    rule = Rule(name=kw.pop("name", "test"), trigger=trigger, actions=actions or ["steer 90"], **kw)
    world.standing.book.add(rule)
    return rule


def given(world: World, name: str) -> list[int]:
    """The ticks at which the standing order gave an order, carried out or refused by
    the ship ("take in the royals" with the royals furled is given, and refused)."""
    actor = f"standing order '{name}'"
    return [
        e.tick
        for e in world.log
        if e.kind in ("order.accepted", "order.rejected") and e.actor == actor
    ]


def firings(world: World, name: str = "test") -> list[int]:
    actor = f"standing order '{name}'"
    return [e.tick for e in world.log if e.kind == "order.accepted" and e.actor == actor]


def test_when_fires_on_the_edge_after_its_duration_and_not_again_until_the_dwell(synthetic):
    kn = {"v": 10.0}
    synthetic("true_wind_speed", lambda w: units.knots_to_ms(kn["v"]))
    w = point_world()
    rule = rule_of("when the true wind exceeds 30 knots for 2 minutes", w)
    kn["v"] = 35.0
    w.run(119)
    assert firings(w) == [], "not before two minutes have held"
    w.run(1)
    assert firings(w) == [120], "once, at the edge"
    assert rule.fired == 1 and rule.last_fired_tick == 120 and not rule.armed
    w.run(600)
    assert firings(w) == [120], "the wind still over thirty: no second firing"
    kn["v"] = 10.0
    w.run(STANDING_DWELL_S - 1)
    kn["v"] = 35.0
    w.run(200)
    assert firings(w) == [120], "the dwell was a second short; the rule was not re-armed"
    kn["v"] = 10.0
    w.run(STANDING_DWELL_S)
    assert rule.armed, "false for the dwell: armed again"
    kn["v"] = 35.0
    w.run(119)
    assert firings(w) == [120], "the duration counts afresh"
    w.run(1)
    assert len(firings(w)) == 2


def test_a_gust_that_falls_away_does_not_fire(synthetic):
    """Truth 35's negative: two minutes less a second at thirty-two, then it falls away."""
    kn = {"v": 32.0}
    synthetic("true_wind_speed", lambda w: units.knots_to_ms(kn["v"]))
    w = point_world()
    rule = rule_of("when the true wind exceeds 30 knots for 2 minutes", w)
    w.run(119)
    kn["v"] = 20.0
    w.run(60)
    kn["v"] = 32.0
    w.run(119)
    assert firings(w) == [] and rule.fired == 0
    assert rule.held_s == 119


def test_when_without_a_duration_fires_at_once_and_is_edge_triggered(synthetic):
    deg = {"v": 70.0}
    synthetic("apparent_wind_angle", lambda w: math.radians(deg["v"]))
    w = point_world()
    rule_of("when the apparent wind is forward of 55 degrees", w)
    w.run(10)
    assert firings(w) == []
    deg["v"] = 50.0
    w.run(1)
    assert firings(w) == [11]
    w.run(50)
    assert firings(w) == [11]


def test_at_fires_once_per_event():
    w = point_world()  # 07:40: eight bells at 08:00, then the bells of the forenoon watch
    rule = rule_of("at eight bells", w)
    w.run(3 * 3600)
    assert firings(w) == [1200], "eight bells struck once in three hours from 07:40"
    assert rule.fired == 1
    four = point_world()
    rule_of("at four bells", four)
    four.run(3 * 3600)
    assert firings(four) == [1200 + 7200], "four bells at 10:00"


def test_every_fires_on_its_interval_from_when_it_was_given():
    w = point_world()
    w.run(100)
    rule_of("every 20 minutes", w)
    w.run(3700)
    assert firings(w) == [1300, 2500, 3700]


def test_the_if_clause_is_tested_at_firing_and_its_failure_is_logged(synthetic):
    kn = {"v": 25.0}
    synthetic("true_wind_speed", lambda w: units.knots_to_ms(kn["v"]))
    w = point_world()
    trigger = Trigger("at", "at eight bells", event="eight bells")
    rule = Rule(
        "morning sail",
        trigger,
        ["steer 90"],
        condition=parse_condition("the true wind is under 20 knots"),
    )
    w.standing.book.add(rule)
    w.run(1200)
    assert firings(w, "morning sail") == []
    held = [e for e in w.log if e.kind == "standing.held"]
    assert len(held) == 1
    assert held[0].text == (
        "Standing order 'morning sail' at eight bells: not carried out; "
        "the true wind is 25 knots, not under 20 knots."
    )
    assert rule.fired == 0


def test_backs_and_veers_measure_from_the_direction_when_armed(synthetic):
    direction = {"v": 0.0}
    synthetic("true_wind_from", lambda w: direction["v"])
    w = point_world()
    rule_of("when the true wind backs two points", w)
    w.run(5)
    direction["v"] = units.wrap_2pi(-1.5 * units.POINT)
    w.run(5)
    assert firings(w) == []
    direction["v"] = units.wrap_2pi(-2.0 * units.POINT)
    w.run(1)
    assert firings(w) == [11]
    # veering is the other way
    v = point_world()
    rule_of("when the true wind veers a point", v, name="veer")
    v.run(2)
    direction["v"] = units.wrap_2pi(-2.0 * units.POINT - units.POINT)  # backed further
    v.run(2)
    assert firings(v, "veer") == []
    direction["v"] = units.wrap_2pi(-2.0 * units.POINT + 1.01 * units.POINT)
    v.run(1)
    assert firings(v, "veer") == [5]


def test_a_shift_either_way_fires_and_is_measured_afresh_from_the_wind_it_fired_on(synthetic):
    """Package 29b (the starter's "trim on a shift"): 'veers 1 point or backs 1 point' is
    one comparison, the two ways the wind turns, and 'shifts 1 point' says the same. Once
    fired, the shift is spent: the order stands again after the dwell and fires at the next
    point from the wind it fired on, whichever way."""
    for said in ("veers 1 point or backs 1 point", "backs 1 point or veers 1 point"):
        clause = parse_condition(f"the true wind {said}").clauses[0]
        assert clause.comparison.op == "shifts" and clause.comparison.value == (1.0, 1.0)
    clause = parse_condition("the true wind shifts 2 points").clauses[0]
    assert (clause.comparison.op, clause.comparison.value) == ("shifts", (2.0, 2.0))
    clause = parse_condition("the true wind veers 2 points or backs a point").clauses[0]
    assert clause.comparison.value == (2.0, 1.0)
    direction = {"v": 0.0}
    synthetic("true_wind_from", lambda w: direction["v"])
    w = point_world()
    rule_of("when the true wind veers 1 point or backs 1 point", w)
    w.run(5)
    direction["v"] = 0.9 * units.POINT
    w.run(5)
    assert firings(w) == []
    direction["v"] = 1.01 * units.POINT  # veered a point
    w.run(1)
    assert firings(w) == [11]
    w.run(STANDING_DWELL_S + 10)  # held there: it stands again, and does not fire
    assert firings(w) == [11]
    direction["v"] = units.wrap_2pi(0.0)  # backed a point from where it fired
    w.run(1)
    assert len(firings(w)) == 2


def test_a_firing_is_logged_by_standing_order_and_never_journaled():
    w = point_world()
    rule_of("at eight bells", w, actions=["steer 90", "speed 5 knots"], name="bells")
    w.run(1200)
    lines = [e for e in w.log if e.actor == "standing order 'bells'"]
    assert [e.text for e in lines if e.kind == "order.accepted"] == [
        "By standing order 'bells': steering 90.",
        "By standing order 'bells': speeding 5 knots.",
    ]
    assert all(e.severity.value == "notable" for e in lines if e.kind == "order.accepted")
    assert all(a != "standing order 'bells'" for _, a, _ in w.journal)
    assert w.journal == []


def test_a_cadences_firing_is_a_routine_line():
    """A firing on a cadence (`every glass then ...`) is the watch's routine work: its line
    is routine, kept in the log and the roll-up, and does not wake a watcher standing by
    (the lead, 2026-09-30: package 32e's sheet-tending routine put fifty-seven notable
    lines in a day). A `when` or an `at` firing stays notable."""
    w = point_world()
    rule_of("every 20 minutes", w, actions=["steer 90"], name="cadence")
    rule_of("at eight bells", w, actions=["speed 5 knots"], name="bells")
    w.run(1300)
    by = {e.actor: e for e in w.log if e.kind == "order.accepted"}
    assert by["standing order 'cadence'"].severity.value == "routine"
    assert by["standing order 'bells'"].severity.value == "notable"


def test_firing_is_deterministic(synthetic):
    """Two worlds, one seed, one journal, a synthetic wind that is a function of the tick:
    one log."""
    synthetic(
        "true_wind_speed",
        lambda w: units.knots_to_ms(35.0 if 600 <= w.clock.tick < 1000 else 10.0),
    )

    def voyage() -> World:
        w = make_world(7, FRIGATE, Scenario(wind_from_deg=0.0, ship_heading_deg=293.0))
        w.submit("set plain sail")
        w.submit(SHORTEN)
        w.submit('standing order "glass": every glass then trim sails')
        w.run(2000)
        return w

    a, b = voyage(), voyage()
    assert a.log.digest() == b.log.digest()
    assert [(r.name, r.fired, r.last_fired_tick) for r in a.standing.book] == [
        ("shorten sail for weather", 1, 719),  # over thirty from tick 600: 120 ticks held
        ("glass", 1, 1800),
    ]


# ---------------------------------------------------------------------------
# The runner's part: the dwell waits for the work; `every` queues at most one
# ---------------------------------------------------------------------------


def frigate(start: datetime = datetime(1805, 6, 1, 7, 40)) -> World:
    return make_world(
        7,
        FRIGATE,
        Scenario(
            start_time=start,
            wind_from_deg=0.0,
            wind_speed_kn=15.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=293.0,
        ),
    )


def test_every_never_queues_more_than_one():
    w = frigate()
    w.submit("set plain sail")
    w.run(900)
    e = w.submit('standing order "reef": every minute then reef the fore topsail, one reef')
    assert e.kind == "standing.given", e.text
    runner = w.ship.extra["evolutions"]
    most_waiting = 0
    for _ in range(600):
        w.tick()
        waiting = sum(1 for i in runner.instances if i.subject_id == "fore.topsail" and i.waiting)
        most_waiting = max(most_waiting, waiting)
    assert most_waiting <= 1
    held = [e for e in w.log if e.kind == "standing.held" and "still waiting" in e.text]
    assert held, "an interval passed while the last firing's reef was still queued"


def test_the_dwell_waits_for_the_evolution_the_firing_started(synthetic):
    kn = {"v": 10.0}
    synthetic("true_wind_speed", lambda w: units.knots_to_ms(kn["v"]))
    w = frigate()
    w.submit("set plain sail")
    w.run(600)
    w.submit(
        'standing order "gust": when the true wind exceeds 30 knots '
        "then reef the fore topsail, one reef"
    )
    kn["v"] = 35.0
    w.run(1)
    rule = w.standing.book.get("gust")
    assert rule.fired == 1 and rule.started, "the firing started a reef"
    kn["v"] = 10.0
    w.run(STANDING_DWELL_S + 1)
    runner = w.ship.extra["evolutions"]
    if any(i in runner.instances for i in rule.started):
        assert not rule.armed, "the reef still in hand: not yet re-armed"
        w.run(1200)
    assert rule.armed


# ---------------------------------------------------------------------------
# The conflict rule, with a synthetic officer
# ---------------------------------------------------------------------------

MASTER = (
    'standing order "master sets" by the master: when the speed is under 100 knots '
    "then set the royals"
)
CAPTAIN = (
    'standing order "captain furls": when the speed is under 100 knots then take in the royals'
)


def countermanded(w: World) -> list[str]:
    return [e.text for e in w.log if e.kind == "standing.countermanded"]


def test_the_captains_standing_order_countermands_the_masters_given_after_it():
    w = frigate()
    w.submit(MASTER)
    w.submit(CAPTAIN)
    w.run(1)
    assert countermanded(w) == [
        "Standing order 'master sets' (the master) countermanded by 'captain furls' (the captain)."
    ]
    assert given(w, "master sets") == [1], "the master's order went first"
    assert given(w, "captain furls") == [1], "and the captain's stands"


def test_the_masters_standing_order_is_not_given_within_the_dwell_of_the_captains():
    w = frigate()
    w.submit(CAPTAIN)
    w.submit(MASTER)
    w.run(1)
    assert countermanded(w) == [
        "Standing order 'master sets' (the master) countermanded by 'captain furls' (the captain)."
    ]
    assert firings(w, "master sets") == [], "the master's order was not given"
    assert w.standing.book.get("master sets").fired == 0
    assert w.standing.book.get("master sets").conflicts == 1


def test_two_of_one_rank_are_noted_and_the_later_stands():
    w = frigate()
    w.submit('standing order "a": when the speed is under 100 knots then set the royals')
    w.submit('standing order "b": when the speed is under 100 knots then take in the royals')
    w.run(1)
    notes = [e.text for e in w.log if e.kind == "standing.conflict"]
    assert notes == [
        "Standing orders 'a' and 'b' (both the captain's) give contrary orders on the fore "
        "royal, the main royal and the mizzen royal; the later stands."
    ]
    assert given(w, "b") == [1]


def test_orders_on_different_parts_or_the_same_order_twice_do_not_conflict():
    w = frigate()
    w.submit(
        'standing order "a" by the master: when the speed is under 100 knots then set the royals'
    )
    w.submit('standing order "b": when the speed is under 100 knots then set the topgallants')
    w.submit('standing order "c": when the speed is under 100 knots then set the royals')
    w.run(1)
    assert countermanded(w) == [] and not [e for e in w.log if e.kind == "standing.conflict"]


def test_a_rule_refuses_a_stranger_as_its_officer():
    with pytest.raises(ValueError):
        Rule("x", Trigger("at", "at sunset", event="sunset"), ["set the royals"], given_by="purser")
    r = Rule(
        "x", Trigger("at", "at sunset", event="sunset"), ["set the royals"], given_by="the master"
    )
    assert r.given_by == "master" and r.rank == 3 and r.officer == "the master"


# ---------------------------------------------------------------------------
# The book: through the world, saved and restored
# ---------------------------------------------------------------------------


def test_the_book_through_the_world():
    w = frigate()
    e = w.submit(NIGHT)
    assert e.kind == "standing.given"
    assert e.text == (
        "Standing order 'night routine' entered in the book: at sunset then take in the "
        "studdingsails; take in the royals."
    )
    assert w.submit(NIGHT).kind == "order.rejected"
    assert "in the book already" in w.submit(NIGHT).text
    w.submit(KEEP_FULL)
    listing = w.submit("standing orders")
    assert listing.kind == "query.standing_orders"
    assert listing.text.split("\n")[0] == "Standing orders (2):"
    assert '"night routine" (the captain): at sunset then' in listing.text
    assert "Standing; never fired." in listing.text
    assert w.submit('show standing order "keep her full"').text.startswith(
        'Standing order "keep her full", given by the captain: when the apparent wind'
    )
    assert w.submit('belay standing order "keep her full"').text == (
        "Standing order 'keep her full' belayed."
    )
    assert "belayed already" in w.submit('belay standing order "keep her full"').text
    assert "Belayed; never fired." in w.submit('show standing order "keep her full"').text
    assert w.submit('resume standing order "keep her full"').kind == "standing.resumed"
    assert "was not belayed" in w.submit('resume standing order "keep her full"').text
    missing = w.submit('belay standing order "night routin"')
    assert (
        "There is no standing order 'night routin' in the book; did you mean 'night routine'?"
        in missing.text
    )
    assert w.submit("belay all standing orders").text == "All 2 standing orders belayed."
    assert "belayed already" in w.submit("belay all standing orders").text
    assert all(r.belayed for r in w.standing.book)
    # queries are answered and not journaled; the rest are journaled as given
    assert [t for _, _, t in w.journal] == [
        NIGHT,
        KEEP_FULL,
        'belay standing order "keep her full"',
        'resume standing order "keep her full"',
        "belay all standing orders",
    ]
    empty = frigate()
    assert empty.submit("standing orders").text == "There are no standing orders in the book."
    assert "the book is empty" in empty.submit('show standing order "x"').text


def test_a_belayed_order_does_not_fire_and_a_resumed_one_is_armed_afresh(synthetic):
    kn = {"v": 35.0}
    synthetic("true_wind_speed", lambda w: units.knots_to_ms(kn["v"]))
    w = point_world()
    rule = rule_of("when the true wind exceeds 30 knots", w, name="gust")
    rule.belayed = True
    w.run(100)
    assert firings(w, "gust") == []
    rule.belayed = False
    w.standing.arm(rule)
    w.run(1)
    assert firings(w, "gust") == [101]


def test_the_book_is_saved_with_the_game_and_restored_by_replay(tmp_path):
    w = frigate()
    w.submit("set plain sail")
    w.submit('standing order "bells": at eight bells then call all hands')
    w.submit('standing order "glass": every glass then trim sails')
    w.submit(KEEP_FULL)
    w.run(1500)
    w.submit('belay standing order "keep her full"')
    w.run(400)
    saved = w.save()
    assert [r["name"] for r in saved["standing_orders"]] == ["bells", "glass", "keep her full"]
    assert saved["standing_orders"][0]["fired"] == 1
    assert saved["standing_orders"][0]["last_fired_tick"] == 1200
    assert saved["standing_orders"][2]["belayed"] is True
    path = replay.save_to_file(w, tmp_path / "standing.json")
    copy = replay.replay(replay.load_file(path), ship_factory)
    assert copy.standing.book.save() == saved["standing_orders"]
    assert copy.log.digest() == w.log.digest()
    assert firings(copy, "bells") == firings(w, "bells") == [1200]
    assert firings(copy, "glass") == firings(w, "glass") == [1800]
    # restore_state is the seam for a book loaded without a replay (package 26)
    fresh = frigate()
    fresh.submit('standing order "bells": at eight bells then call all hands')
    missing = fresh.standing.book.restore_state(saved["standing_orders"])
    assert missing == ["glass", "keep her full"]
    assert fresh.standing.book.get("bells").fired == 1


def test_strike_takes_an_order_out_of_the_book_and_belay_keeps_it(tmp_path):
    """Package 28c (playtest 3: the captain tried `cancel standing order`, and belaying
    left the order in the book under its name). `strike standing order "x"`, or `cancel`
    or `remove`, takes it out: journaled as an order, logged, no longer listed or fired,
    its name free again; a belayed order stays in the book as it is. A replay strikes it
    at the same point."""
    w = frigate()
    w.submit("set plain sail")
    w.submit('standing order "glass": every glass then trim sails')
    w.submit(KEEP_FULL)
    w.submit(NIGHT)
    w.submit('belay standing order "keep her full"')
    assert w.standing.book.names == ["glass", "keep her full", "night routine"]
    assert w.standing.book.get("keep her full").belayed  # belayed, and still in the book
    w.run(100)
    e = w.submit('strike standing order "glass"')
    assert e.kind == "standing.struck"
    assert e.text == "Standing order 'glass' struck from the book."
    assert w.submit('cancel standing order "keep her full"').text == (
        "Standing order 'keep her full' struck from the book."
    )
    assert w.submit("remove the standing order 'night routine'").kind == "standing.struck"
    assert w.standing.book.names == []
    w.run(1800)
    assert firings(w, "glass") == []  # struck before its glass came
    # the name is free again
    assert w.submit('standing order "glass": every glass then trim sails').kind == (
        "standing.given"
    )
    assert [t for _, _, t in w.journal][-4:] == [
        'strike standing order "glass"',
        'cancel standing order "keep her full"',
        "remove the standing order 'night routine'",
        'standing order "glass": every glass then trim sails',
    ]
    w.run(1800)
    assert firings(w, "glass")  # given again, it keeps its glass
    path = replay.save_to_file(w, tmp_path / "struck.json")
    copy = replay.replay(replay.load_file(path), ship_factory)
    assert copy.standing.book.names == ["glass"]
    assert copy.standing.book.save() == w.standing.book.save()
    assert copy.log.digest() == w.log.digest()
    # the book's words for it (queries and refusals are logged, not journaled, so they
    # are asked of another game)
    other = frigate()
    other.submit(NIGHT)
    other.submit('strike standing order "night routine"')
    assert other.submit("standing orders").text == "There are no standing orders in the book."
    assert "the book is empty" in other.submit('strike standing order "glass"').text
    assert 'strike standing order "' in complete.STANDING_SENTENCES


# ---------------------------------------------------------------------------
# The drivers: `read the standing orders from <file>`, the book as a query
# ---------------------------------------------------------------------------

ORDERS_FILE = f"""# the night routine and the gust rule (Luce's routine of the day)
{NIGHT}
{SHORTEN}

standing order "glass":
    every glass then trim sails
"""


def test_console_reads_a_file_of_standing_orders_and_lists_the_book(tmp_path):
    path = tmp_path / "starter.orders"
    path.write_text(ORDERS_FILE, encoding="utf-8")
    out = io.StringIO()
    con = Console(frigate(), out=out)
    assert con.handle_line(f"read the standing orders from {path}")
    assert f"Read 3 standing orders from {path}." in out.getvalue()
    assert [t for _, _, t in con.world.journal] == [
        NIGHT,
        SHORTEN,
        'standing order "glass": every glass then trim sails',
    ]
    before = len(con.world.journal)
    assert con.handle_line("standing orders")
    assert con.handle_line('show standing order "glass"')
    assert len(con.world.journal) == before, "the book is a query, never journaled"
    text = out.getvalue()
    assert "Standing orders (3):" in text
    assert 'Standing order "glass", given by the captain: every glass then trim sails.' in text
    assert "Next due in 1800 s." in text
    con.handle_line("read the standing orders from nowhere.orders")
    assert "Could not read nowhere.orders" in out.getvalue()


def test_console_flag_reads_the_file_at_the_start(tmp_path, monkeypatch):
    from freesail.ui import console as console_mod

    printed: list[str] = []

    class Capturing(console_mod.Console):
        def _print(self, text: str) -> None:
            printed.append(text)

    path = tmp_path / "starter.orders"
    path.write_text(NIGHT + "\n", encoding="utf-8")
    monkeypatch.setattr(console_mod, "Console", Capturing)
    monkeypatch.setattr("sys.stdin", io.StringIO("standing orders\nquit\n"))
    monkeypatch.setattr("sys.stdin.isatty", lambda: False, raising=False)
    console_mod.main([FRIGATE, "--seed", "7", "--standing-orders", str(path)])
    text = "\n".join(printed)
    assert "Standing order 'night routine' entered in the book" in text
    assert "Standing orders (1):" in text


def test_server_driver_reads_a_file_and_answers_the_book(tmp_path):
    path = tmp_path / "starter.orders"
    path.write_text(NIGHT + "\n" + KEEP_FULL + "\n", encoding="utf-8")
    d = Driver(frigate())
    e = d.submit(f"read the standing orders from {path}")
    assert e.kind == "driver.standing_orders" and e.text == f"Read 2 standing orders from {path}."
    assert len(d.world.standing.book) == 2
    assert d.submit("standing orders").kind == "query.standing_orders"
    assert d.read_standing_orders("nowhere.orders").kind == "driver.refused"
    assert [t for _, _, t in d.world.journal] == [NIGHT, KEEP_FULL]


# ---------------------------------------------------------------------------
# The seams package 26 uses
# ---------------------------------------------------------------------------


def test_parse_condition_alone():
    c = parse_condition("the true wind exceeds 30 knots and the heel is over 15 degrees")
    assert [cl.reading for cl in c.clauses] == ["true_wind_speed", "heel"]
    assert c.text == "the true wind exceeds 30 knots and the heel is over 15 degrees"
    with pytest.raises(OrderError, match="cannot be 'shaking'"):
        parse_condition("the true wind is shaking")
    with pytest.raises(OrderError, match="is not a reading the ship has"):
        parse_condition("the fore royal is shaking")  # a sail needs the ship
    ship = make(F)
    c = parse_condition("the fore royal is shaking", ship)
    assert c.clauses[0].params == ("fore.royal",)


def test_a_rule_built_from_the_pieces_fires_like_its_dialect_twin(synthetic):
    kn = {"v": 35.0}
    synthetic("true_wind_speed", lambda w: units.knots_to_ms(kn["v"]))
    dialect = point_world()
    python = point_world()
    text = 'standing order "gust": when the true wind exceeds 30 knots for 2 minutes then steer 90'
    # the dialect's, through the World: the point ship has no Orders grammar, so through
    # the parser and the book directly
    rule = parse_standing(make(F), text)
    dialect.standing.book.add(rule)
    twin = Rule(
        name="gust",
        trigger=Trigger(
            "when",
            "when the true wind exceeds 30 knots for 2 minutes",
            condition=parse_condition("the true wind exceeds 30 knots"),
            duration_s=120,
        ),
        actions=["steer 90"],
        source="python",
        trusted=True,
    )
    python.standing.book.add(twin)
    dialect.run(300)
    python.run(300)
    assert firings(dialect, "gust") == firings(python, "gust") == [120]
    assert [e.text for e in dialect.log if e.actor.startswith("standing")] == [
        e.text for e in python.log if e.actor.startswith("standing")
    ]


def test_completion_knows_the_words():
    ship = frigate().ship
    assert 'standing order "' in complete.suggestions(ship, "stand")
    assert "belay all standing orders" in complete.suggestions(ship, "belay all")
    assert "read the standing orders from " in complete.suggestions(ship, "read the")
    assert 'standing order "x": when ' in complete.suggestions(ship, 'standing order "x": ')
    assert 'standing order "x": when the true wind ' in complete.suggestions(
        ship, 'standing order "x": when the tr'
    )
    assert 'standing order "x": when the true wind exceeds ' in complete.suggestions(
        ship, 'standing order "x": when the true wind '
    )
    got = complete.suggestions(ship, 'standing order "x": at sunset then set the roy')
    assert 'standing order "x": at sunset then set the royals' in got


# ---------------------------------------------------------------------------
# Package 31c: the weather's events in the dialect, and the station verbs
# ---------------------------------------------------------------------------


def tendency(words: str, three: float = 0.0, one: float = 0.0) -> dict[str, Any]:
    return {"words": words, "three_hours_in": three, "one_hour_in": one}


def test_an_event_that_is_a_readings_change_fires_at_its_onset_each_time(synthetic):
    """The glass falling fast is the tendency coming to "falling fast": not while it goes
    on falling fast, and not at the first look (an order given while it is falling fast
    waits for the next time it comes); and a fall that eases for a while and comes again
    inside the hour (`EVENT_SETTLE_S`) is the same fall, not a new event, since the glass's
    words hover about their thresholds. The same condition a stand-by watches
    (`rules.event_condition`)."""
    from freesail.standing.rules import EVENT_SETTLE_S

    glass = {"v": tendency("falling fast", -0.12, -0.04)}
    synthetic("tendency", lambda w: glass["v"])
    w = point_world()
    rule = rule_of("at the glass falling fast", w)
    assert rule.trigger.kind == "when" and rule.trigger.event == "the glass falling fast"
    assert rule.trigger.text == "at the glass falling fast"
    w.run(STANDING_DWELL_S + 60)
    assert firings(w) == [], "falling fast when given: not the event"
    glass["v"] = tendency("falling", -0.08, -0.02)
    w.run(600)
    glass["v"] = tendency("falling fast", -0.11, -0.04)
    w.run(600)
    assert firings(w) == [], "come again inside the hour: the same fall"
    glass["v"] = tendency("falling", -0.08, -0.02)
    w.run(EVENT_SETTLE_S)
    glass["v"] = tendency("falling fast", -0.11, -0.04)
    w.run(10)
    first = firings(w)
    assert len(first) == 1, "an hour without: this is a new fall"
    w.run(STANDING_DWELL_S + 60)  # it goes on falling fast: no second firing
    assert firings(w) == first
    for _ in range(3):  # hovering about the tenth: the same fall
        glass["v"] = tendency("falling", -0.09, -0.02)
        w.run(120)
        glass["v"] = tendency("falling fast", -0.10, -0.03)
        w.run(240)
    assert firings(w) == first
    glass["v"] = tendency("falling", -0.09, -0.02)
    w.run(EVENT_SETTLE_S + 10)
    glass["v"] = tendency("falling fast", -0.12, -0.05)
    w.run(1)
    assert len(firings(w)) == 2
    assert EVENT_SETTLE_S == 3600
    assert "at the glass falling fast then steer 90" in w.standing.book.lines()[1]


def test_a_wind_shift_is_the_mean_wind_a_point_from_where_it_stood(synthetic):
    """'a wind shift' is the ten minutes' mean a point or more from where it stood when the
    order was given, and afresh from each shift: a steady veer is an event at each point."""
    mean = {"v": 0.0}
    synthetic("mean_true_wind_from", lambda w: mean["v"])
    w = point_world()
    rule_of("at a wind shift", w)
    w.run(10)
    mean["v"] = 0.9 * units.POINT
    w.run(10)
    assert firings(w) == []
    mean["v"] = 1.05 * units.POINT
    w.run(1)
    assert firings(w) == [21]
    w.run(STANDING_DWELL_S + 10)
    assert firings(w) == [21], "held there: no second shift"
    mean["v"] = units.wrap_2pi(-0.1 * units.POINT)  # backed a point from where it fired
    w.run(1)
    assert len(firings(w)) == 2


def test_the_sea_getting_up_is_its_words_upward_and_the_glass_turning_its_hour_against_three(
    synthetic,
):
    from freesail.standing.rules import GLASS_TURN_IN, event_condition

    sea = {"v": {"words": "a moderate sea", "state": "moderate", "confused": False}}
    synthetic("sea", lambda w: sea["v"])
    w = point_world()
    rule_of("at the sea getting up", w, name="sea")
    w.run(10)
    sea["v"] = {"words": "a smooth sea", "state": "smooth", "confused": False}
    w.run(10)
    assert firings(w, "sea") == [], "going down is not getting up"
    sea["v"] = {"words": "a moderate sea", "state": "moderate", "confused": False}
    w.run(10)
    assert firings(w, "sea") == [], "back to where it stood when the order was given"
    sea["v"] = {"words": "a short chopping sea", "state": "short", "confused": False}
    w.run(1)
    assert firings(w, "sea") == [31]
    # the glass turning: the last hour's change against the three hours', three hundredths
    # each way at least
    assert GLASS_TURN_IN == 0.03
    cond = event_condition("the glass turning")
    for three, one, turning in (
        (-0.12, 0.01, False),  # a hundredth in the hour is the glass's noise
        (-0.08, 0.03, True),  # the rise after the low
        (0.11, -0.02, False),  # the pumping of a heavy sea
        (0.10, -0.04, True),  # the fall after the high
        (-0.02, 0.05, False),  # steady over three hours: nothing to turn from
        (-0.08, -0.03, False),  # falling still
    ):
        clause = cond.clauses[0]
        assert clause._one(tendency("x", three, one), {}) is turning, (three, one)


def test_a_change_in_the_sky_is_the_skys_line_or_the_weathers():
    from freesail.core.events import Severity

    w = point_world()
    rule_of("at a change in the sky", w, name="sky")
    w.record(Severity.ROUTINE, "weather.sky", "The sky overcast.", data={"sky": "overcast"})
    w.run(1)
    w.record(Severity.ROUTINE, "weather.change", "Rain set in.", data={"weather": "rain"})
    w.run(1)
    w.record(Severity.ROUTINE, "weather.hour", "Overcast, rain; the glass 29.90.")
    w.run(1)
    assert len(firings(w, "sky")) == 2
    spec = R.EVENTS["a change in the sky"]
    assert (spec.kind, spec.also, spec.watch) == ("weather.sky", ("weather.change",), None)
    for words in (
        "a wind shift",
        "the glass falling fast",
        "the glass turning",
        "the sea getting up",
    ):
        assert R.EVENTS[words].watch and not R.event_matches(R.EVENTS[words], "", {})


def test_the_station_verbs_after_then_are_resolved_when_the_order_is_given():
    """The owner's finding at gate 5a: `standing order "sea": when the sea is heavy then
    tell the watcher the sea is getting up` was refused ("'tell the watcher' is said to an
    agent's station"). Now `tell` and `ask` follow `then`, to a station aboard, whether or
    not one mans it when the order is given; the words are free, and checked for nothing
    but being there."""
    w = frigate()
    e = w.submit(
        'standing order "sea": when the sea is heavy then tell the watcher the sea is getting '
        "up; take in the royals"
    )
    assert e.kind == "standing.given", e.text
    assert e.text == (
        "Standing order 'sea' entered in the book: when the sea is heavy then tell the "
        "watcher the sea is getting up; take in the royals."
    )
    # free words: 'the well' in them is not the absent reading, 'standing order' no sentence
    e = w.submit(
        'standing order "q": every glass then ask the watcher whether the well wants sounding '
        "and what the standing order says"
    )
    assert e.kind == "standing.given", e.text
    e = w.submit('standing order "l": at sunset then tell the purser to look sharp')
    assert e.kind == "order.rejected"
    assert e.text.endswith(
        "In standing order 'l', 'tell the purser to look sharp' is refused: there is no "
        "purser aboard yet; a standing order may tell or ask the watcher or the officer of "
        "the watch or the master or the lookout or the passenger."
    )
    assert [r.name for r in w.standing.book] == ["sea", "q"]


# ---------------------------------------------------------------------------
# Package 33c: the dialect's article, the manoeuvre in hand, a name said loosely, the well
# held, the held lines once a watch, and the conflict rule's grain (spec M5 open item 15)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "condition,reading",
    [
        ("when the daylight is night", "daylight"),
        ("when daylight is night", "daylight"),
        ("when the true wind exceeds 30 knots", "true_wind_speed"),
        ("when true wind exceeds 30 knots", "true_wind_speed"),
        ("when she is hove to", "manoeuvre_in_hand"),
        ("when she is not hove to", "manoeuvre_in_hand"),
        ("when the manoeuvre in hand is tacking", "manoeuvre_in_hand"),
        ("when the manoeuvre is none", "manoeuvre_in_hand"),
    ],
)
def test_the_article_before_a_reading_and_she_for_the_manoeuvre(condition, reading):
    """Playtest 13's brig: "the daylight is night" refused where "daylight is night" was
    taken; the trim rules belayed by hand through a night hove to, for want of `if she is
    not hove to`."""
    rule = parse_standing(make(F), f'standing order "x": {condition} then trim sails')
    assert rule.trigger.condition.clauses[0].reading == reading


def test_she_is_hove_to_from_the_heave_to_until_she_fills_away():
    """The manoeuvre in hand (a reading of its own, `the manoeuvre in hand`): none,
    heaving to, hove to, filling away, none; `she is hove to` holds from the moment the
    heave-to begins until she fills away, so a trim rule sleeps through it."""
    w = frigate()
    for sid in w.ship.groups["plain sail"]:
        w.ship.sails[sid].state = SailState.SET
    w.submit("brace the yards sharp up")
    w.submit("keep her full")
    w.run(300)
    hove = parse_condition("she is hove to", w.ship)
    awake = parse_condition("she is not hove to", w.ship)
    seen: list[tuple[str, bool, bool]] = []

    def look() -> None:
        now = (
            w.readings.words("manoeuvre_in_hand"),
            hove.holds(w.readings),
            awake.holds(w.readings),
        )
        if not seen or seen[-1] != now:
            seen.append(now)

    look()
    w.submit("heave to")
    for _ in range(900):
        w.tick()
        look()
    w.submit("fill away")
    for _ in range(900):
        w.tick()
        look()
    assert seen == [
        ("none", False, True),
        ("heaving to", True, False),
        ("hove to", True, False),
        ("filling away", False, True),
        ("none", False, True),
    ]
    e = w.submit("the manoeuvre in hand")
    assert e.kind == "query.reading" and e.text == "The manoeuvre in hand: none."


def test_a_standing_order_is_found_case_blind_and_by_a_distinct_part_of_its_name():
    """Playtest 13's brig: `belay "blind lead"` read as a line called the blind lead, and
    `resume standing order "trim by the wind"` refused for "Trim Sails by the Wind"."""
    w = frigate()
    w.submit('standing order "Blind Lead": every 10 minutes then heave the lead')
    w.submit(
        'standing order "Trim Sails by the Wind": when the true wind veers 1 point then trim sails'
    )
    w.submit('standing order "Trim Sails by the Glass": every glass then trim sails')
    e = w.submit('Belay "blind lead"')
    assert e.kind == "standing.belayed" and e.text == "Standing order 'Blind Lead' belayed."
    e = w.submit('avast "trim by the wind"')
    assert e.text == "Standing order 'Trim Sails by the Wind' belayed."
    e = w.submit('resume standing order "trim by the wind"')
    assert e.text == "Standing order 'Trim Sails by the Wind' resumed."
    e = w.submit('belay standing order "trim sails"')  # two answer: say which
    assert e.kind == "order.rejected"
    assert "could be standing order 'Trim Sails by the Wind' or 'Trim Sails by the Glass'" in e.text
    e = w.submit("resume blind lead")  # the whole name, without quotes
    assert e.text == "Standing order 'Blind Lead' resumed."
    e = w.submit('show "the glass"')
    assert e.kind == "query.standing_orders" and "Trim Sails by the Glass" in e.text
    # words that name a line are the line verb still, though a standing order's name has
    # them in it
    w.submit('standing order "ease the main sheet": every glass then ease the main sheet')
    e = w.submit("belay the main sheet")
    assert e.kind != "standing.belayed", e.text


def test_the_well_is_held_in_the_book_and_never_fires():
    """Spec M4 §24 item 4: the starter's `sound the well` was refused at every start, a
    line of noise in every log; now it is entered, held, and silent until the well is a
    reading, and it is journaled and replays like any order."""
    from freesail.core import replay as replay_mod

    w = frigate()
    e = w.submit(WELL)
    assert e.kind == "standing.given"
    assert e.text == (
        "Standing order 'sound the well' entered in the book: every glass then sound the well. "
        "Held until the ship can carry it out: The ship has no well to sound yet; that "
        "reading comes with the world."
    )
    rule = w.standing.book.get("sound the well")
    assert rule.held is not None and rule.state_words() == (
        "held: the ship has no well to sound yet; that reading comes with the world"
    )
    w.run(2 * 3600)
    assert rule.fired == 0 and not [e for e in w.log if "sound the well" in e.actor]
    assert [t for _, _, t in w.journal] == [WELL]
    copy = replay_mod.replay(w.save(), ship_factory)
    assert copy.log.digest() == w.log.digest()
    # an order on the well at the prompt is refused in the registry's words
    e = w.submit("sound the well")
    assert e.kind == "order.rejected" and e.text.endswith(
        "The ship has no well to sound yet; that reading comes with the world."
    )


def test_a_failing_if_is_said_the_first_time_and_then_once_a_watch(synthetic):
    """Spec M5 open item 15: an `at` or `every` order whose `if` fails said so at every
    firing (the gate's passage: a hundred and fifty-seven lines, the two leads every ten
    minutes); now the first time, then once in each watch of the ship's clock while it goes
    on failing, and afresh after it has fired."""
    kn = {"v": 25.0}
    synthetic("true_wind_speed", lambda w: units.knots_to_ms(kn["v"]))
    w = point_world()  # 07:40, the morning watch
    rule = Rule(
        "lead",
        Trigger("every", "every 10 minutes", interval_s=600),
        ["steer 90"],
        condition=parse_condition("the true wind is under 20 knots"),
    )
    w.standing.book.add(rule)
    w.run(5 * 3600)  # to 12:40: the morning, the forenoon and the afternoon watches
    held = [e for e in w.log if e.kind == "standing.held"]
    assert [e.ship_time.strftime("%H:%M") for e in held] == ["07:50", "08:00", "12:00"]
    kn["v"] = 15.0
    w.run(600)
    assert len(firings(w, "lead")) == 1
    kn["v"] = 25.0
    w.run(1200)  # fired, then failing again in the same watch: said again, once
    held = [e for e in w.log if e.kind == "standing.held"]
    assert [e.ship_time.strftime("%H:%M") for e in held][3:] == ["13:00"]


def test_the_lead_and_a_manoeuvre_are_not_contrary_orders_on_the_ship():
    """Spec M5 open item 15 (gate 5b's passage: `heave the lead` against `heave to` and
    `wear ship` logged as contrary orders on "the ship"): the lead is the leadsman's, the
    log the log's, a bearing the master's, a manoeuvre the helm's and the yards'."""
    from freesail.standing.runtime import HELM, LEAD, LOG_LINE, RECKONING, action_parts

    w = frigate()
    ship = w.ship
    yards = {s.id for s in ship.spars.values() if s.is_yard}
    assert action_parts(ship, "heave the lead").parts == {LEAD}
    assert action_parts(ship, "heave the deep-sea lead").parts == {LEAD}
    assert action_parts(ship, "heave the log").parts == {LOG_LINE}
    assert action_parts(ship, "take a bearing of the land").parts == {RECKONING}
    assert action_parts(ship, "shape a course for Falmouth").parts == {HELM}
    for manoeuvre in ("heave to", "wear ship", "tack ship", "fill away"):
        assert action_parts(ship, manoeuvre).parts == {HELM} | yards
    w.submit('standing order "a": when the speed is under 100 knots then heave the lead')
    w.submit('standing order "b": when the speed is under 100 knots then heave to')
    w.run(1)
    assert not [e for e in w.log if e.kind == "standing.conflict"]
    w.submit('standing order "c": when the speed is under 100 knots then trim sails')
    w.run(1)
    notes = [e.text for e in w.log if e.kind == "standing.conflict"]
    assert notes == [
        "Standing orders 'b' and 'c' (both the captain's) give contrary orders on the yards; "
        "the later stands."
    ]


def test_an_order_after_a_firings_work_is_done_is_the_next_step_not_a_contrary_one():
    """`at wore then heave to` follows the wear: a firing whose evolutions have all ended
    is done with, though its five minutes are not out."""
    w = frigate()
    w.submit('standing order "a": when the speed is under 100 knots then square the fore yard')
    w.run(1)
    runner = w.ship.extra["evolutions"]
    for _ in range(280):
        if not runner.instances:
            break
        w.tick()
    assert not runner.instances and w.clock.tick < 290  # the brace done inside the dwell
    w.submit('standing order "b": when the speed is under 100 knots then brace the fore yard up')
    w.run(1)
    assert not [e for e in w.log if e.kind == "standing.conflict"]
    # while the work is in hand the same two are contrary, as they always were
    w2 = frigate()
    w2.submit('standing order "a": when the speed is under 100 knots then square the fore yard')
    w2.run(1)
    w2.submit('standing order "b": when the speed is under 100 knots then brace the fore yard up')
    w2.run(1)
    notes = [e.text for e in w2.log if e.kind == "standing.conflict"]
    assert notes == [
        "Standing orders 'a' and 'b' (both the captain's) give contrary orders on the fore "
        "yard; the later stands."
    ]


# ---------------------------------------------------------------------------
# Package 37g, item 5: what undoes what, as data beside the vocabulary
# ---------------------------------------------------------------------------


def test_what_undoes_what_is_a_table_of_the_vocabulary_and_the_books_rule_is_unchanged(tmp_path):
    """The harness's detector for a station with authority counts a link only when the
    later order undoes the earlier (`standing.runtime.undoes`), and what undoes what is a
    table of `data/vocabulary.yaml`, each pair read both ways and each name a verb. The
    book's own conflict rule (`contrary`, between two standing orders' firings) is another
    rule and is as it was: it still calls two helm orders contrary, which the undo rule
    never does."""
    import shutil

    from freesail.orders.vocabulary import load_vocabulary
    from freesail.standing.runtime import (
        GROUND_TACKLE,
        contrary,
        order_acts,
        undo_chain,
        undoes,
        where_words,
    )

    ship = frigate().ship
    vocab = load_vocabulary()
    assert all(len(pair) == 2 and pair <= set(vocab.verbs) for pair in vocab.undoes)
    assert set(vocab.irrevocable) <= set(vocab.verbs)
    # the same sail set and taken in; hove to and filled away; an anchor let go and weighed;
    # cable veered and hove in; a thing allowed and disallowed
    assert where_words(ship, undoes(ship, "set the jib", "furl the jib")) == "the jib"
    assert undoes(ship, "fill away", "heave to") and undoes(ship, "heave to", "fill away")
    assert undoes(ship, "let go the best bower", "weigh") == {GROUND_TACKLE}
    assert undoes(ship, "veer the small bower to 100 fathoms", "heave in 20 fathoms")
    assert undoes(ship, "call all hands", "pipe down")
    assert undoes(ship, 'belay standing order "trim"', 'resume standing order "trim"')
    assert not undoes(ship, 'belay standing order "trim"', 'resume standing order "reef"')
    # a group evolution is its lines: shortening sail undoes the royals set
    assert [a.verb for a in order_acts(ship, "set the main royal")] == ["set"]
    # the course is never a pair, and the book's own rule still calls it contrary
    assert not undoes(ship, "steer 90", "steer 95") and contrary(ship, "steer 90", "steer 95")
    assert not undoes(ship, "tack ship", "wear ship") and contrary(ship, "tack ship", "wear ship")
    assert not undoes(ship, "heave to", "steer N")
    # the chain is the run at the end in which each undoes the one before it
    orders = ["steer N", "set the jib", "take in the jib", "set the jib"]
    chain, shared = undo_chain(ship, orders)
    assert chain == orders[1:] and where_words(ship, shared) == "the jib"
    assert undo_chain(ship, [*orders, "steer NE"])[0] == ["steer NE"]
    assert undo_chain(ship, []) == ([], frozenset())
    # the loader refuses a pair that is not two verbs of the table
    source = Path(__file__).resolve().parents[1] / "data" / "vocabulary.yaml"
    for bad, why in (
        ("  - [set, no such verb]\n", "undoes names 'no such verb', which is no verb"),
        ("  - [set, set]\n", "a pair is two different verbs"),
    ):
        copy = tmp_path / f"vocabulary-{len(why)}.yaml"
        shutil.copyfile(source, copy)
        text = copy.read_text(encoding="utf-8").replace("\nundoes:\n", "\nundoes:\n" + bad, 1)
        copy.write_text(text, encoding="utf-8", newline="\n")
        with pytest.raises(ValueError, match=why):
            load_vocabulary(copy)
    copy = tmp_path / "vocabulary-irrevocable.yaml"
    text = source.read_text(encoding="utf-8").replace("  - cut away\n", "  - cut and run\n")
    copy.write_text(text, encoding="utf-8", newline="\n")
    with pytest.raises(ValueError, match="irrevocable names 'cut and run', which is no verb"):
        load_vocabulary(copy)


# ---------------------------------------------------------------------------
# Package 37l: a standing order's action read whole when it is given (the audit: its
# first word was read and no more), and "when the true wind is 12 knots"
# ---------------------------------------------------------------------------


def channel(ship: str = "frigate") -> World:
    """A ship off the Lizard with the chart, for the actions that name a mark or a place."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        position={"lat_deg": 49.9, "lon_deg": -5.5},
        region="channel-west",
    )
    return make_world(7, str(SHIP_FILES[ship]), scenario)


@pytest.mark.parametrize(
    "ship,action,named,words",
    [
        # the audit's three, each entered before and met at sea
        (
            F,
            "take a fix as soon as a bearing can be taken",
            "take a fix as soon as a bearing can be taken",
            "names no mark of the chart",
        ),
        (
            F,
            "take a bearing of the moon made of cheese",
            "take a bearing of the moon made of cheese",
            "The chart has no mark named 'the moon made of cheese'",
        ),
        (C, "let go the sheet anchor", "let go the sheet anchor", "carries no sheet anchor"),
        # a fault in the third order, refused at the giving and named
        (
            F,
            "heave the lead; trim sails; shape a course for atlantis",
            "shape a course for atlantis",
            "The chart has no place named 'atlantis'",
        ),
        (F, "heave the lead; trim sails; set the topsail", "set the topsail", "say which"),
        (F, "heave the lead; veer umpteen fathoms", "veer umpteen fathoms", "not a number of"),
        (F, "heave the lead; send for the cook's cat", "send for the cook's cat", "Nobody aboard"),
        (F, "heave the lead; hoist our colours", "hoist our colours", "milestone 7"),
        (F, "heave the lead; steer south by west half", "steer south by west half", "toward which"),
        (F, "heave the lead; buy umpteen tons of tin", "buy umpteen tons of tin", "How many tons"),
        (
            F,
            "heave the lead; take in provisions for a good while",
            "take in provisions for a good while",
            "not a time to provision for",
        ),
    ],
)
def test_a_standing_orders_action_is_read_whole_when_it_is_given(
    ship: str, action: str, named: str, words: str
):
    w = channel(ship)
    e = w.submit(f'standing order "x": every glass then {action}')
    assert e.kind == "order.rejected", e.text
    assert f"In standing order 'x', '{named}' is refused: " in e.text, e.text
    assert words in e.text, e.text
    assert w.standing.book.get("x") is None


@pytest.mark.parametrize(
    "action",
    [
        "take a fix",
        "take a fix by the Lizard and the Manacles",
        "take a bearing of the lizard",
        "take a bearing of the land",
        "take a bearing of manacle",
        "shape a course for Falmouth",
        "shape a course for a mile south of the Lizard",
        "shape a course for 49 52 N 6 10 W",
        "let go the best bower",
        "heave in to eighty fathoms",
        "veer a hundred and eighty-five fathoms",
        "send for the master",
        "steer south by west half west",
        "tell the watcher the Lizard is abeam",
        "allow half a knot of set to the south west",
        "set the reckoning to 49 52 N 6 10 W",
    ],
)
def test_an_action_that_reads_whole_is_entered_whatever_the_moment(action: str):
    """What depends on the moment (a mark in sight, an anchor down, a port) is the
    order's business when it fires: read whole, these are entered."""
    w = channel()
    e = w.submit(f'standing order "x": every glass then {action}')
    assert e.kind == "standing.given", e.text


def test_the_starter_and_the_scenario_books_still_load_whole():
    """Every book the game ships is entered as it was: read whole, no action of theirs is
    refused that was taken before."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    for name in ("gate-5b-passage", "merchant-passage", "naval-cruise", "gate-4c-day"):
        sf = load_scenario(ROOT / "data" / "scenarios" / f"{name}.yaml")
        world = make_scenario_world(sf)
        begin(world, sf)
        refused = [e.text for e in world.log if e.kind == "order.rejected"]
        assert refused == [], (name, refused)


def test_when_the_true_wind_is_twelve_knots_holds_within_half_a_knot(synthetic):
    """Game 10's officer, six tries at "when the true wind is 12 knots" before one was
    taken: it is the comparison it is, the wind at twelve knots within half a knot either
    way, so a `when` fires as the wind comes to it from above or from below."""
    kn = {"v": 10.0}
    synthetic("true_wind_speed", lambda w: units.knots_to_ms(kn["v"]))
    cond = parse_condition("the true wind is 12 knots")
    (clause,) = cond.clauses
    assert clause.comparison.op == "about" and clause.comparison.value == 12.0
    assert clause.comparison.text == "12 knots, within half a knot"
    for v, holds in ((10.0, False), (11.4, False), (11.6, True), (12.4, True), (12.6, False)):
        assert clause._one(units.knots_to_ms(v), {}) is holds, v
    w = point_world()
    rule_of("when the true wind is twelve knots", w)
    kn["v"] = 10.0
    w.run(10)
    assert firings(w) == []
    kn["v"] = 11.8
    w.run(10)
    assert len(firings(w)) == 1
    assert parse_condition("the speed is five knots").clauses[0].comparison.op == "about"
    with pytest.raises(OrderError, match="cannot be"):
        parse_condition("the true wind is 12 degrees")


def test_a_condition_on_the_depth_reads_the_lead_and_the_chart_only_by_the_chart():
    """Package 37j, item 7: a standing order's condition on the depth reads the last cast
    of the lead, as the officer of the watch would ("at a sounding, if the depth of water
    is under 13 fathoms"), and the chart's figure at the account only when the book says
    `by the chart`; until then `the depth of water` was the chart at her true place, which
    the books gated on as a sounding machine (the review's G4)."""
    from freesail.standing.grammar import parse_condition

    w = make_world(
        7,
        "data/ships/brig.yaml",
        Scenario(
            start_time=datetime(1805, 6, 12, 13, 0),
            wind_from_deg=225.0,
            wind_speed_kn=0.0,
            gustiness=0.0,
            variability=0.0,
            position={"lat_deg": 50.12, "lon_deg": -5.03},
            region="channel-west",
        ),
    )
    lead = parse_condition("the depth of water is under 30 fathoms", w.ship)
    chart = parse_condition("the depth of water by the chart is under 30 fathoms", w.ship)
    by_name = parse_condition("the depth is under 30 fathoms", w.ship)
    assert [c.reading for c in lead.clauses] == ["depth"] == [c.reading for c in by_name.clauses]
    assert [c.reading for c in chart.clauses] == ["depth_of_water"]
    assert chart.holds(w.readings, {}) is True
    assert lead.holds(w.readings, {}) is False  # the lead not yet hove
    w.submit("heave the lead")
    w.run(300)
    assert lead.holds(w.readings, {}) is True
