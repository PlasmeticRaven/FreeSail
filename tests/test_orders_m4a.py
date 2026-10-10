"""The orders milestone 4a adds beyond the standing dialect (spec M4 §7): `trim the
<sail>`, `tend the sheets`, `bear away one point` and `come up one point`, the owner's
words for bearing away, and `steady out the bowlines` re-hauling after she has fallen
off and come up again; and the starter routines file (spec §6) loading on both drivers
with its refused line refused and the rest entered.
"""

from __future__ import annotations

import io
import math
from dataclasses import dataclass, field

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario, World
from freesail.orders import handle
from freesail.orders.errors import OrderError
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState
from freesail.ui.console import Console
from freesail.ui.server import Driver

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
STARTER = "data/standing_orders/starter.orders"


class FakeRunner:
    """As tests/test_trim_order.py stands in for the runner: records the starts."""

    def __init__(self, ship: Ship):
        self.started: list[tuple[str, str, dict]] = []
        ship.extra["evolutions"] = self

    def start(self, ship, evolution, subject, params=None):
        self.started.append((evolution, subject, params or {}))
        return f"started {evolution} on {subject}"

    def step(self, ship, dt, wind):
        pass

    def in_progress(self):
        return []


def rigged(path: str = FRIGATE, awa_deg: float = 48.0) -> tuple[Ship, FakeRunner]:
    ship = load_ship(path)
    runner = FakeRunner(ship)
    ship.dyn.apparent_wind_angle = units.deg_to_rad(awa_deg)
    ship.dyn.apparent_wind_speed = 8.0
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    for yard in ship.spars.values():
        if yard.is_yard:
            yard.brace_angle = yard.brace_limit
    for sail in ship.sails.values():
        if sail.is_set and sail.is_fore_and_aft:
            sail.sheet_angle = 0.0
    return ship, runner


# ---------------------------------------------------------------------------
# trim the <sail>, tend the sheets
# ---------------------------------------------------------------------------


@dataclass
class ok:
    yards: list[str] = field(default_factory=list)  # the yards braced
    sheets: list[str] = field(default_factory=list)  # the sails whose sheets were trimmed
    text: list[str] = field(default_factory=list)


@dataclass
class no:
    mentions: list[str] = field(default_factory=list)


TRIM_TABLE: list[tuple[str, ok | no]] = [
    (
        "trim the fore topsail",
        ok(yards=["fore.topsail.yard"], text=["Braced the fore topsail to the wind"]),
    ),
    ("trim the mainsail", ok(yards=["main.yard"], text=["Braced the main course to the wind"])),
    (
        "trim the topsails",
        ok(
            yards=["fore.topsail.yard", "main.topsail.yard", "mizzen.topsail.yard"],
            text=["Braced the topsails to the wind"],
        ),
    ),
    ("trim the fore yard", ok(yards=["fore.yard"], text=["Braced the fore yard to the wind"])),
    # package 32e: a sheet is trimmed by an evolution with hands and time, so the order's
    # line says the work is begun
    ("trim the jib", ok(sheets=["jib"], text=["Trimming the sheet of the jib."])),
    (
        "trim the spanker",
        ok(sheets=["mizzen.spanker"], text=["Trimming the sheet of the mizzen spanker."]),
    ),
    (
        "trim the headsails",
        ok(
            sheets=["fore.topmast_staysail", "jib"],
            text=["Trimming the sheets of the fore topmast staysail and the jib."],
        ),
    ),
    (
        "tend the sheets",
        ok(
            sheets=["mizzen.spanker", "fore.topmast_staysail", "jib"],
            text=[
                "Trimming the sheets of the mizzen spanker, the fore topmast staysail and the jib."
            ],
        ),
    ),
    ("tend sheets", ok(sheets=["mizzen.spanker", "fore.topmast_staysail", "jib"])),
    ("trim the sheets", ok(sheets=["mizzen.spanker", "fore.topmast_staysail", "jib"])),
    ("trim the fore royal", no(["The fore royal is furled; there is no sail to trim."])),
    ("trim the main mast", no(["The main mast is not a yard; trim a sail or a yard."])),
    ("trim the fore topsail sheet", no(["Which fore topsail sheet"])),
    ("trim the weather main brace", no(["is not a sail; trim a sail or a yard."])),
    ("trim the mainbrace", no(["no such part as the mainbrace"])),
]


@pytest.mark.parametrize("text,expect", TRIM_TABLE, ids=[t for t, _ in TRIM_TABLE])
def test_trim_the_sail_and_tend_the_sheets(text: str, expect: ok | no):
    ship, runner = rigged()
    if isinstance(expect, no):
        with pytest.raises(OrderError) as info:
            handle(ship, text)
        for m in expect.mentions:
            assert m in str(info.value), str(info.value)
        assert runner.started == []
        return
    kind, log, data = handle(ship, text)
    assert [s for e, s, _ in runner.started if e == "brace"] == expect.yards
    assert data["trimmed_sheets"] == [
        f"the {ship.sails[s].id.replace('.', ' ').replace('_', ' ')}" for s in expect.sheets
    ] or len(data["trimmed_sheets"]) == len(expect.sheets)
    # each sheet trimmed by its own evolution (package 32e), none set at once
    assert [s for e, s, _ in runner.started if e.startswith("trim_")] == expect.sheets
    for m in expect.text:
        assert m in log, log
    assert log[0].isupper() and log.endswith(".")
    if expect.yards and not expect.sheets:
        assert kind == "evolution.started"
    if expect.sheets and not expect.yards:
        assert kind == "sail.trimmed"


def test_trim_the_sail_braces_only_that_yard_and_to_the_wind():
    ship, runner = rigged(awa_deg=60.0)
    handle(ship, "trim the fore topsail")
    assert len(runner.started) == 1
    evo, subject, params = runner.started[0]
    assert evo == "brace" and subject == "fore.topsail.yard" and params["mode"] == "to the wind"
    # the same angle the whole-ship trim would give that yard
    ship2, runner2 = rigged(awa_deg=60.0)
    handle(ship2, "trim the yards")
    whole = {s: p["target_deg"] for _, s, p in runner2.started}
    assert params["target_deg"] == whole["fore.topsail.yard"]


def test_tend_the_sheets_touches_no_brace_and_trim_sails_does_both():
    ship, runner = rigged()
    kind, _, data = handle(ship, "tend the sheets")
    assert not [e for e, _, _ in runner.started if e == "brace"]
    assert len(runner.started) == 3 and len(data["trimmed_sheets"]) == 3
    assert kind == "sail.trimmed"
    ship, runner = rigged()
    _, _, data = handle(ship, "trim sails")
    assert len([e for e, _, _ in runner.started if e == "brace"]) == 12
    assert len(data["trimmed_sheets"]) == 3 and len(runner.started) == 15


def test_the_schooner_trims_her_gaff_sails_by_the_sheet_and_her_topsail_by_the_yard():
    ship, runner = rigged(SCHOONER, awa_deg=45.0)
    kind, log, data = handle(ship, "trim the mainsail")
    assert [(e, s) for e, s, _ in runner.started] == [("trim_gaff_sheet", "main.sail")]
    assert data["trimmed_sheets"] == ["the main sail"]
    assert log == "Trimming the sheet of the main sail."
    kind, log, _ = handle(ship, "trim the fore topsail")
    assert [s for e, s, _ in runner.started if e == "brace"] == ["fore.topsail.yard"]


# ---------------------------------------------------------------------------
# Helm: bear away one point, come up one point, and the owner's words
# ---------------------------------------------------------------------------

HELM_TABLE: list[tuple[str, str, float]] = [
    # (order, the log's words, points to leeward: negative is toward the wind)
    ("bear away one point", "bear away a point", 1.0),
    ("bear away a point", "bear away a point", 1.0),
    ("come up one point", "come up a point", -1.0),
    ("come up a point", "come up a point", -1.0),
    ("bear away", "bear away a point", 1.0),
    ("bear off", "bear away a point", 1.0),
    ("fall off", "bear away a point", 1.0),
    ("off the wind", "bear away a point", 1.0),
    ("steer off the wind", "bear away a point", 1.0),
    ("bear off the wind", "bear away a point", 1.0),
    ("fall off two points", "bear away two points", 2.0),
    ("luff", "come up a point", -1.0),
]


@pytest.mark.parametrize("text,said,points", HELM_TABLE, ids=[t for t, _, _ in HELM_TABLE])
def test_bear_away_and_come_up_by_points(text: str, said: str, points: float):
    ship, _ = rigged()  # the wind on the starboard bow: to leeward is to larboard
    ship.dyn.heading = units.deg_to_rad(293.0)
    ship.dyn.target_heading = ship.dyn.heading
    kind, log, data = handle(ship, text)
    assert kind == "helm.order" and said in log
    turned = units.wrap_pi(data["target_heading"] - units.deg_to_rad(293.0))
    assert math.degrees(turned) == pytest.approx(-points * 11.25, abs=0.01)


def test_by_and_large_stays_refused():
    ship, _ = rigged()
    with pytest.raises(OrderError, match="not an order this ship understands"):
        handle(ship, "by and large")


# ---------------------------------------------------------------------------
# Steady out the bowlines after falling off and coming up again (the real ship)
# ---------------------------------------------------------------------------


def close_hauled_frigate() -> World:
    w = make_world(
        7,
        FRIGATE,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=15.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=293.0,
            ship_speed_kn=4.0,
        ),
    )
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    w.run(900)
    w.submit("trim sails")
    w.run(300)
    return w


def hauled(world: World) -> list[str]:
    return [ln.id for ln in world.ship.lines.values() if ln.bowline_hauled]


def test_steady_out_the_bowlines_re_hauls_them_after_falling_off_and_coming_up():
    """Spec M4 §7 and the owner's note at gate M3b. The weather bowlines hauled on a
    wind stand while she is kept within four points of it; fallen off to a broad reach
    and trimmed, the yards come in past forty degrees from square and the bowlines are
    let go by the hands with a log line (spec 3b §4); brought by the wind and trimmed
    again, they want hauling afresh, and `steady out the bowlines` is the order."""
    w = close_hauled_frigate()
    assert w.submit("haul the weather bowlines").kind == "order.accepted"
    w.run(200)
    assert len(hauled(w)) == 5
    # four points off: the yards stay braced up beyond forty degrees; the bowlines stand
    w.submit("bear away four points")
    w.run(600)
    w.submit("trim sails")
    w.run(300)
    assert len(hauled(w)) == 5
    refused = w.submit("steady out the bowlines")
    assert refused.kind == "order.rejected" and "hauled out already" in refused.text
    # eight points off: the yards come in, the bowlines are let go
    w.submit("bear away four points")
    w.run(600)
    w.submit("trim sails")
    w.run(300)
    slacked = [e for e in w.log if e.kind == "line.slacked"]
    assert len(slacked) == 5 and hauled(w) == []
    assert any(
        e.text.startswith("Let go the starboard fore course bowline as the fore yard came in")
        for e in slacked
    )
    assert all("a bowline will not stand off the wind" in e.text for e in slacked)
    # by the wind again: braced up, and the bowlines steadied out
    w.submit("come up eight points")
    w.run(600)
    w.submit("trim sails")
    w.run(300)
    assert hauled(w) == []
    e = w.submit("steady out the bowlines")
    assert e.kind == "order.accepted", e.text
    w.run(200)
    assert len(hauled(w)) == 5
    lines = [ev.text for ev in w.log if ev.kind == "line.hauled" or "Steadied out" in ev.text]
    assert sum(1 for t in lines if t.startswith("Steadied out")) >= 10


# ---------------------------------------------------------------------------
# The starter routines file on both drivers
# ---------------------------------------------------------------------------

STARTER_NAMES = [
    "night routine",
    "morning sail",
    "shorten sail for weather",
    "keep her full",
    "trim on a shift",
    "tend the sheets",  # package 32e: the sheets tended every glass
    "heavy weather",  # package 37p: it sets the storm staysails, the companion order gone
    "sound the well",  # package 33c: held in the book until the well is a reading
]


def test_the_starter_file_loads_in_the_console_with_the_well_held_and_the_rest_entered():
    out = io.StringIO()
    con = Console(close_hauled_frigate(), out=out)
    assert con.handle_line(f"read the standing orders from {STARTER}")
    text = out.getvalue()
    # 32e: tending the sheets; 37p: the storm staysail's companion order folded into heavy
    # weather
    assert f"Read 8 standing orders from {STARTER}." in text
    assert con.world.standing.book.names == STARTER_NAMES
    assert not [e for e in con.world.log if e.kind == "order.rejected"]
    # package 33c: the well's order is entered and held, saying why, and journaled with
    # the seven others (32e: the sheets; 37p: the storm staysail's order gone)
    held = [e for e in con.world.log if e.kind == "standing.given" and "Held until" in e.text]
    assert len(held) == 1 and "The ship has no well to sound yet" in held[0].text
    journaled = [t for _, _, t in con.world.journal if t.startswith("standing order")]
    assert len(journaled) == 8
    con.handle_line("standing orders")
    assert "Standing orders (8):" in out.getvalue()


def test_the_starter_file_loads_on_the_server_driver():
    d = Driver(close_hauled_frigate())
    e = d.submit(f"read the standing orders from {STARTER}")
    assert e.kind == "driver.standing_orders"
    assert d.world.standing.book.names == STARTER_NAMES


def test_the_starter_file_names_a_source_for_every_order():
    from pathlib import Path

    text = Path(STARTER).read_text(encoding="utf-8")
    assert text.count('standing order "') == 8  # 32e: "tend the sheets"; 37p: storm staysail gone
    for word in ("Luce 1866", "truth 9", "truth 28", "milestone 5", "judgement"):
        assert word in text, word
    assert "\r" not in text
