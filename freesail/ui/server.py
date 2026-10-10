"""The local web server: a FastAPI app around one world, and the browser client.

    python -m freesail.ui.server data/ships/frigate-36.yaml [--seed N] [--wind FROM,KN]
                                 [--heading DEG] [--time N] [--port 8000] [--watcher fake]
                                 [--lockstep] [--ease-on-station]
                                 [--consent-records DIR] [--saves DIR]
    python -m freesail.ui.server --scenario data/scenarios/gate-4c-day.yaml [...]
    python -m freesail.ui.server --load SAVE [--replay-anyway] [...]

then open http://localhost:8000. `--scenario FILE` starts from a scenario file (its
ship, start, weather script, seed, standing orders and first orders; spec M4 §19);
`--load SAVE` takes a save up at its last tick and goes on from there, as the console's
`--load` does (spec M4 §21): from the checkpoint beside it, else by a replay of its
journal, and the terminal says which and why. A save written by another build that holds
a station's transcript is not replayed unless `--replay-anyway` is given (package 37d).

Routes (spec §9.2):

    GET  /              the client, client/index.html
    GET  /client/...    the client's scripts and styles
    GET  /api/ship      the ship graph, for drawing (queries.ship_graph)
    GET  /api/state     the current snapshot (queries.snapshot) plus the driver
    GET  /api/log       the log, optionally ?since=TICK, ?until=TICK and ?limit=N: the
                        store, every line (a roll-up's lines are asked for by its ticks)
    GET  /api/save      the save file (seed, scenario, journal) as a download,
                        the same file `save PATH` writes; the browser can keep it
    POST /api/order     {"text": "..."} -> the accepted or rejected event
    POST /api/driver    {"action": "hold"|"go"|"speed"|"time"|"tick", "value": N}
                        (speed and time are the same: compression up to 300)
                        or {"action": "standing_orders", "value": FILE} to read a file
                        of standing orders (also `read the standing orders from FILE`
                        on the command line, as in the console), or
                        {"action": "save", "value": PATH} to write a save file on the
                        server's disk (also `save PATH` on the command line), or
                        {"action": "ease_on_station", "value": true|false}, the
                        instruments' option that `--ease-on-station` sets (below)
    GET  /api/complete  ?line=...&limit=N: the console's completer, its whole-line
                        suggestions for the order line (package 33d)
    GET  /api/library   ?topic=...&section=...&find=...: a page of the reference
                        library, as the model's `library` tool serves it, for the
                        browser's pane; /api/library/topics the topics and their
                        sections, /api/library/papers the ship's papers (`shelf_routes`)
    GET  /api/marks     the player's lines, rings and notes on the chart (package 37n);
                        POST one, DELETE /api/marks/{id} one or /api/marks all
                        (`mark_routes`): kept with the game, read by the chart alone
    WS   /ws          every log event as it happens, and a snapshot every
                        tick at 1x, every 10 ticks at 10x, every 60 at 60x and up;
                        at 60x and up the log is rolled up (spec M4 §20): the notable
                        and urgent lines and the captain's come as events, and each
                        hour's routine lines as one {"type": "rollup"} message
                        (`events.RollupView`, the console's and the samples' view)

The agent API (spec M4 §13 as revised, package 28b; `agent_routes`, which the console
hosts too on `--agents-port`): a language model's door is a client of this game.

    POST /api/agents/{station}          {model_name, door, door_note?, session_kind?,
                                        client?, ask_again?}: station an agent (the answer
                                        carries the seating's `key`, which every later
                                        call for the station sends: package 37g), the
                                        consent gate first (the consent conversation,
                                        the station brief, or refused in words)
    GET  /api/agents/{station}/turns    ?since=N&wait=S: the turns from N on, as soon as
                                        there are any, or none after S real seconds
    POST /api/agents/{station}/reply    {text, calls: [{name, args}], raw, since?}: one
                                        reply through the harness; the turns it made
                                        and whose the floor is
    POST /api/agents/{station}/owner    {text}: the owner's reply to what the model
                                        wrote in the consent conversation
    POST /api/agents/{station}/release  {reason}: the door is going; stood down, saved
    GET  /api/agents/{station}/library  ?topic=...&section=...&find=...: a page of the
                                        reference library
    GET  /api/agents                    the stations and their states (the snapshot's
                                        `agents` is the same list)
    GET  /api/agents/{station}/picture/{id}  ?key=K: a picture a tool of the station's
                                        made, its bytes (package 42; `agents.pictures`)

The pictures (package 42, item 4; `Easel`): a tool's request for the chart or the ship's
view goes to the open page as `{"type": "picture", "id", "view", "facing", "max_px",
"max_bytes"}` on the socket; the page draws it as the player sees it and posts it back,
`POST /api/picture/{id}?width=W&height=H` with the image as the body (or `?failed=WORDS`).

`--lockstep` holds the clock while a door has the floor (a sample open for it), for
testing at 1x and for competitive play; without it the game runs at its compression and
a door's late reply finds its turn grown by what happened meanwhile (the harness's fold).

`--ease-on-station` (package 33d; playtest 12, the owner's note 3), also an option in the
instruments: whenever a station is sampled or speaks while the clock runs faster than 1x,
the clock is eased to 1x as an urgent line eases it, and the log says so in a driver's
line (`driver.eased`, routine, with the station), which a replay writes again; the player
speeds up again by hand. Off by default.

The driver mirrors the console: the clock runs in a background thread that
ticks the world `compression` times per real second, and every use of the
world from a request goes through the same lock. Websocket clients are fed
through per-connection asyncio queues; the clock thread hands messages to
the event loop with `call_soon_threadsafe`, so the simulation never waits
on a socket.
"""

from __future__ import annotations

import argparse
import asyncio
import math
import sys
import threading
import time
from collections.abc import Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from freesail import units
from freesail.api import queries
from freesail.core import replay as replay_mod
from freesail.core.events import Event, Rollup, RollupView, Severity, Shown, kept, rolls_up
from freesail.core.events import rollup as rolled
from freesail.core.world import UNLOGGED_KINDS, World
from freesail.ui.console import (
    ALARM_SPEED,
    REPLAY_ANYWAY_FLAG,
    REPLAY_ANYWAY_HELP,
    SEAT_HELP,
    SPEED_WORDS,
    book_words,
    check_agents_unattended,
    clamp_compression,
    eased_words,
    loaded_words,
    read_standing_orders,
    read_standing_orders_path,
    start_world,
    station_watcher,
)

CLIENT_DIR = Path(__file__).resolve().parents[2] / "client"

Listener = Callable[[dict[str, Any]], None]

# The log kinds of a station speaking (`World.AGENT_LOG_KINDS`): its narration and its
# answer to a question. With `--ease-on-station` either eases the clock, as its turn
# opening does (package 33d; playtest 12, the owner's note 3).
STATION_SPEAKS = ("agent.note", "agent.said")


def snapshot_interval(compression: float) -> int:
    """Ticks between snapshots on the stream: every tick at 1x, every 10 at 10x,
    every 60 at 60x and above (spec §9.2)."""
    if compression >= 60:
        return 60
    if compression >= 10:
        return 10
    return 1


def save_path(line: str) -> str | None:
    """The path named by `save <path>`, or None. The console's own `save` is the same
    word; here it is read out of the order box so the browser session can save too."""
    words = line.split()
    if not words or words[0].lower() != "save":
        return None
    return " ".join(words[1:]).strip().strip("\"'")


class Driver:
    """Hold, go, compression and tick, around one world, with a lock.

    The clock thread and every request share `lock`. Listeners receive
    message dictionaries (`{"type": "event"|"snapshot", ...}`) from whichever
    thread produced them; the websocket layer makes that safe.
    """

    def __init__(
        self,
        world: World,
        compression: float = 1.0,
        lockstep: bool = False,
        ease_on_station: bool = False,
    ):
        self.world = world
        self.compression = clamp_compression(compression)
        self.world.compression = self.compression
        self.lockstep = lockstep
        # `--ease-on-station` (package 33d): the clock eased to 1x when a station is sampled
        # or speaks, as an urgent line eases it; off unless asked for
        self.ease_on_station = bool(ease_on_station)
        self._heard: tuple[str, str] | None = None  # (station, why) seen while running fast
        self._samples_seen = self._samples_now()  # each station's samples, last looked at
        self._view = RollupView()  # the roll-up (spec M4 §20), the console's rule
        self._alarm: Event | None = None  # an urgent line seen while running fast
        # the last auto-slow (spec M4 open item 8), shown until the player sets the speed
        self.eased: dict[str, Any] | None = None
        self.desk: Any = None  # the agent API's stations (`agent_routes`), when mounted
        self.running = False
        self.lock = threading.RLock()
        self._listeners: list[Listener] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._ticks_since_snapshot = 0
        self.world.log.subscribe(self._on_event)

    # -- listeners ----------------------------------------------------------

    def add_listener(self, fn: Listener) -> None:
        with self.lock:
            self._listeners.append(fn)

    def remove_listener(self, fn: Listener) -> None:
        with self.lock:
            if fn in self._listeners:
                self._listeners.remove(fn)

    def _emit(self, message: dict[str, Any]) -> None:
        for fn in list(self._listeners):
            fn(message)

    def _on_event(self, e: Event) -> None:
        if (
            e.severity is Severity.URGENT
            and self.running
            and self.compression > ALARM_SPEED
            and self._alarm is None
        ):
            self._alarm = e  # eased once the tick is over (`_run_ticks`)
        if e.kind in STATION_SPEAKS and self._heard is None and e.actor.startswith("the "):
            self._heard = (e.actor.removeprefix("the "), "speaks")  # `--ease-on-station`
        for x in self._view.feed(e, self.compression):
            self._emit_shown(x)

    def _emit_shown(self, x: Shown) -> None:
        if isinstance(x, Rollup):
            self._emit({"type": "rollup", "rollup": x.to_dict()})
        else:
            self._emit({"type": "event", "event": event_dict(x)})

    # -- state --------------------------------------------------------------

    def state(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "running": self.running,
            "compression": self.compression,
            "snapshot_every": snapshot_interval(self.compression),
        }
        if self.eased is not None:  # the clock was eased on an alarm (open item 8)
            out["eased"] = dict(self.eased)
        if self.ease_on_station:  # and eases when a station is sampled or speaks (33d)
            out["ease_on_station"] = True
        if self.lockstep:  # the clock waits for a door that has the floor
            out["lockstep"] = True
            out["waiting_for"] = self.held_for()
        return out

    def held_for(self) -> str | None:
        """In lockstep, the station whose door has the floor, which the clock waits for."""
        if not self.lockstep or self.desk is None:
            return None
        with self.lock:
            return self.desk.holding()

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            snap = queries.snapshot(self.world)
            if self.desk is not None:
                snap["agents"] = self.desk.stations()
            snap["driver"] = self.state()
            return snap

    def emit_snapshot(self) -> None:
        self._ticks_since_snapshot = 0
        self._emit({"type": "snapshot", "snapshot": self.snapshot()})

    def emit_marks(self) -> None:
        """The player's marks on the chart to every page (package 37n), after a change."""
        with self.lock:
            marks = [dict(m) for m in self.world.chart_marks]
        self._emit({"type": "marks", "marks": marks})

    # -- commands -----------------------------------------------------------

    def hold(self) -> None:
        with self.lock:
            self.running = False
            self.emit_snapshot()

    def go(self) -> None:
        with self.lock:
            self.running = True
            self.emit_snapshot()

    def set_compression(self, value: float) -> None:
        """`speed N` (or `time N`), up to 300 (spec M4 §20). The player's choice clears
        the auto-slow notice; an hour the roll-up holds is let go when the speed comes
        down below its threshold."""
        with self.lock:
            self._set_compression(value)
            self.eased = None
            self.emit_snapshot()

    def _set_compression(self, value: float) -> None:
        self.compression = clamp_compression(value)
        self.world.compression = self.compression
        if self._view.holding and not rolls_up(self.compression):
            for x in self._view.flush():
                self._emit_shown(x)

    def _ease(self) -> None:
        """Auto-slow (spec M4 open item 8): an urgent line while the clock ran faster
        than ALARM_SPEED eases it to that, the log says so (a driver's line, which a replay
        writes again), and the client shows the notice until the player sets the speed."""
        e, self._alarm = self._alarm, None
        if e is None or self.compression <= ALARM_SPEED:
            return
        was = self.compression
        self._set_compression(ALARM_SPEED)
        self.eased = {"from": was, "to": ALARM_SPEED, "line": e.text, "tick": e.tick}
        self.world.record_driver(
            "notable",
            "driver.eased",
            eased_words(e),
            data={"from": was, "to": ALARM_SPEED, "tick": e.tick, "kind": e.kind},
        )
        self.emit_snapshot()

    # -- `--ease-on-station` (package 33d) ------------------------------------

    def set_ease_on_station(self, on: bool) -> None:
        """The instruments' option and the flag: ease the clock to 1x whenever a station is
        sampled or speaks. The player speeds up again by hand, as after an alarm."""
        with self.lock:
            self.ease_on_station = bool(on)
            self._station_heard()  # what a station did before the option was set is past
            self.emit_snapshot()

    def _samples_now(self) -> dict[str, int]:
        return {
            name: int(getattr(getattr(h, "agent", None), "samples", 0) or 0)
            for name, h in self.world.agents.items()
        }

    def _station_heard(self) -> tuple[str, str] | None:
        """The station that was sampled or spoke since the last look, and which (`sampled`,
        `speaks`), or None. Looked at after every tick and every order, option or not, so
        that switching the option on does not ease for what is past."""
        heard, self._heard = self._heard, None
        now = self._samples_now()
        for name, n in now.items():
            if n > self._samples_seen.get(name, 0):
                heard = (name, "sampled")  # a turn opened is the first thing to say
                break
        self._samples_seen = now
        return heard

    def _ease_for_station(self) -> bool:
        """`--ease-on-station`: a station sampled or speaking while the clock runs faster
        than ALARM_SPEED eases it to that, as an urgent line does (`_ease`), and the log says
        so in a driver's line, which a replay writes again. The line is routine, kept at any
        speed as the driver's lines are, so that it does not itself sample a station that is
        sampled on notable lines. Returns whether the clock was eased."""
        heard = self._station_heard()
        if heard is None or not self.ease_on_station or not self.running:
            return False
        if self.compression <= ALARM_SPEED:
            return False
        station, why = heard
        was = self.compression
        self._set_compression(ALARM_SPEED)
        said = f"the {station} {'is sampled' if why == 'sampled' else 'speaks'}"
        tick = self.world.clock.tick
        self.eased = {"from": was, "to": ALARM_SPEED, "line": said, "tick": tick, "why": "station"}
        self.world.record_driver(
            "routine",
            "driver.eased",
            f"Compression eased to {ALARM_SPEED:g}x: {said}.",
            data={"from": was, "to": ALARM_SPEED, "tick": tick, "station": station, "why": why},
        )
        self.emit_snapshot()
        return True

    def shown_log(self, n: int = 500) -> list[dict[str, Any]]:
        """The last `n` lines of the store as the client shows them now: rolled up at the
        driver's compression, the hour still open left for the live view to close."""
        return [
            x.to_dict() if isinstance(x, Rollup) else event_dict(x)
            for x in rolled(self.world.log.tail(n), self.compression)
        ]

    def tick(self, n: int) -> None:
        """Advance n ticks now, then hold."""
        with self.lock:
            self.running = False
            self._run_ticks(max(0, int(n)))
            self.emit_snapshot()

    def submit(self, text: str) -> Event:
        with self.lock:
            path = read_standing_orders_path(text)
            if path is not None:
                # the driver's command, as in the console (spec M4 §3): reading the disk
                # is the driver's business; each order in the file is journaled
                return self._read_standing_orders(path)
            path = save_path(text)
            if path is not None:
                # `save PATH`, as in the console: writing the disk is the driver's too
                return self._save(path)
            seat = getattr(self.world, "player_seat", None)
            if seat is not None and not seat.agent.released:
                # the player's seat at a station (package 40): the line is the owner's
                # where it is his, the seat's otherwise, judged by its authority
                e = seat.route(text)
            else:
                e = self.world.submit(text)
            if e is not None and e.kind in UNLOGGED_KINDS:
                # an answer for the player who asked and not a line of the log (package
                # 40b: the master's slate): sent to the pages as a line is, kept nowhere
                self._emit({"type": "event", "event": event_dict(e)})
            # a question put to a station is answered on the order (spec M4 §12)
            if not self._ease_for_station():
                self.emit_snapshot()
            return e

    def read_standing_orders(self, path: str) -> Event:
        with self.lock:
            return self._read_standing_orders(path)

    def save(self, path: str) -> Event:
        with self.lock:
            return self._save(path)

    def _save(self, path: str) -> Event:
        """Write the save file and say so in the log (not journaled: a save is the
        driver's act, not an order, and a replay must not re-save)."""
        if not path:
            return self.world.record_driver(
                "routine",
                "driver.refused",
                "Say 'save somewhere.json'.",
                data={"path": path},
            )
        try:
            p = replay_mod.save_to_file(self.world, path)
        except OSError as e:
            return self.world.record_driver(
                "routine",
                "driver.refused",
                f"Could not write {path}: {e.strerror or e}.",
                data={"path": path},
            )
        # the digest of the log the save holds (this line comes after it), so a replay of
        # the file can be checked against it (spec M4 §21)
        return self.world.record_driver(
            "notable",
            "driver.saved",
            f"Saved to {p} at tick {self.world.clock.tick}; the log's digest is "
            f"{self.world.log.digest()[:16]}.",
            data={"path": str(p), "tick": self.world.clock.tick},
        )

    def _read_standing_orders(self, path: str) -> Event:
        try:
            n = read_standing_orders(self.world, path)
        except OSError as e:
            return self.world.record_driver(
                "routine",
                "driver.refused",
                f"Could not read {path or 'the standing orders'}: {e.strerror or e}.",
                data={"path": path},
            )
        finally:
            self.emit_snapshot()
        return self.world.record_driver(
            "routine",
            "driver.standing_orders",
            f"Read {n} standing order{'s' if n != 1 else ''} from {path}.",
            data={"path": path, "count": n},
        )

    # -- the clock ----------------------------------------------------------

    def _run_ticks(self, n: int) -> None:
        every = snapshot_interval(self.compression)
        for _ in range(n):
            if self.held_for() is not None:
                break  # lockstep: the World waits for the door that has the floor
            self.world.tick()
            self._ticks_since_snapshot += 1
            if self._alarm is not None:
                self._station_heard()  # the alarm's easing says it; a station's is past
                self._ease()  # auto-slow: the rest of this batch is not run
                break
            if self._ease_for_station():
                break  # `--ease-on-station`: the rest of this batch is not run either
            if self._ticks_since_snapshot >= every:
                self.emit_snapshot()

    def _tick_owed(self, owed: float, period: float) -> float:
        if self.running:
            owed += self.compression * period
            n = int(owed)
            owed -= n
            if n:
                with self.lock:
                    if self.running:
                        self._run_ticks(n)
        with self.lock:
            # the unattended bound on this driver's clock, every period, running or not:
            # ten real minutes of a pause unanswered, however fast the ship's clock runs
            # (package 31c; before, the check ran only on a period that ran ticks)
            check_agents_unattended(self.world)
        return owed

    def _clock_thread(self) -> None:
        period = 0.1
        owed = 0.0
        while not self._stop.is_set():
            owed = self._tick_owed(owed, period)
            time.sleep(period)

    def start(self) -> None:
        if self._thread is None:
            self._stop.clear()
            self._thread = threading.Thread(target=self._clock_thread, daemon=True)
            self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None


def switched_on(value: Any) -> bool:
    """A driver option's value: true, 1, 'on', 'yes' and 'true' switch it on."""
    if isinstance(value, str):
        return value.strip().lower() in ("on", "yes", "true", "1")
    return bool(value)


def event_dict(e: Event) -> dict[str, Any]:
    """An event for the wire: its dictionary plus the watch-and-bells stamp people read."""
    d = e.to_dict()
    d["stamp"] = units.time_stamp(e.ship_time)
    d["kept"] = kept(e)  # shown as it is at any speed: the client's roll-up leaves it out
    return d


# ---------------------------------------------------------------------------
# The app
# ---------------------------------------------------------------------------


class Easel:
    """The browser's painting of the chart and the ship's view, on a tool's request
    (package 42, item 4; `agents.pictures`): the request goes to every open page through
    the driver's listeners, the first page to post its picture back answers it, and the
    pictures are kept here, the newest `pictures.KEPT`, for the doors to fetch by id. The
    tool waits for the post holding the World's lock; the post itself takes no lock."""

    def __init__(self, driver: Driver, wait_s: float | None = None):
        from collections import OrderedDict

        from freesail.agents import pictures

        self.driver = driver
        self.wait_s = pictures.PAINT_WAIT_S if wait_s is None else float(wait_s)
        self._lock = threading.Lock()
        self._pending: dict[str, dict[str, Any]] = {}
        self._kept: OrderedDict[str, Any] = OrderedDict()

    def paint(self, view: str, facing: str, stamp: str) -> Any:
        import secrets

        from freesail.agents import pictures as P

        if not self.driver._listeners:
            return "No browser page is open on this game (the picture is drawn by the open page)"
        deg, said = P.facing_of(facing) if view == P.SHIP else (None, "")
        pid = secrets.token_hex(8)
        slot: dict[str, Any] = {"event": threading.Event(), "post": None, "why": ""}
        with self._lock:
            self._pending[pid] = slot
        self.driver._emit(
            {
                "type": "picture",
                "id": pid,
                "view": view,
                "facing": deg,
                "facing_words": said,
                "max_px": P.MAX_PX,
                "max_bytes": P.MAX_BYTES,
            }
        )
        answered = slot["event"].wait(self.wait_s)
        with self._lock:
            self._pending.pop(pid, None)
        if not answered:
            return (
                f"The open page did not send its picture within {self.wait_s:g} seconds (a page "
                "in a background tab may not draw)"
            )
        if slot["why"]:
            return f"The open page could not draw it ({slot['why']})"
        media, data, width, height = slot["post"]
        pic = P.Picture(pid, media, data, width, height, view, said, stamp)
        with self._lock:
            self._kept[pid] = pic
            while len(self._kept) > P.KEPT:
                self._kept.popitem(last=False)
        return pic

    def post(self, pid: str, media: str, data: bytes, width: int, height: int, failed: str) -> str:
        """The page's picture for a request: "" when taken, else why not (an unknown or an
        answered request, a picture too large or of no kind a door shows)."""
        from freesail.agents import pictures as P

        with self._lock:
            slot = self._pending.get(pid)
            if slot is None or slot["event"].is_set():
                return "no request waits for that picture"
            if failed:
                slot["why"] = " ".join(failed.split())[:200]
            elif media not in P.MEDIA_TYPES:
                slot["why"] = f"a picture of the kind {media or 'unnamed'}, which no door shows"
            elif len(data) > P.MAX_BYTES:
                slot["why"] = f"a picture of {len(data):,} bytes, past the bound of {P.MAX_BYTES:,}"
            elif not data:
                slot["why"] = "an empty picture"
            else:
                w, h = _png_size(data) if media == "image/png" else (None, None)
                slot["post"] = (media, bytes(data), w or int(width), h or int(height))
            slot["event"].set()
        return "" if slot["post"] is not None else slot["why"]

    def get(self, pid: str) -> Any:
        with self._lock:
            return self._kept.get(pid)


def _png_size(data: bytes) -> tuple[int | None, int | None]:
    """A PNG's width and height from its header, or (None, None) when it is no PNG."""
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def picture_routes(easel: Easel) -> APIRouter:
    """The page's post of a picture it drew (package 42, item 4). No lock is taken: the
    tool that asked holds the World's while it waits."""
    from freesail.agents import pictures as P

    router = APIRouter()

    @router.post("/api/picture/{pid}")
    async def api_picture(
        pid: str, request: Request, width: int = 0, height: int = 0, failed: str = ""
    ) -> JSONResponse:
        size = int(request.headers.get("content-length") or 0)
        if size > P.MAX_BYTES:
            easel.post(pid, "", b"", 0, 0, f"a picture of {size:,} bytes, past the bound")
            raise HTTPException(status_code=413, detail="The picture is larger than the bound.")
        data = b"" if failed else await request.body()
        media = str(request.headers.get("content-type") or "").split(";")[0].strip()
        why = easel.post(pid, media, data, width, height, failed)
        if why:
            raise HTTPException(status_code=409, detail=f"Not taken: {why}.")
        return JSONResponse({"taken": pid})

    return router


def agent_routes(lock: Any, world: Callable[[], World], **desk_options: Any) -> APIRouter:
    """The agent API's routes (spec M4 §13 as revised), given the driver's lock and a
    way to reach its World now; the browser server mounts them on its own port and the
    console on `--agents-port`. The stations are a `remote.Desk` (`router.desk`), built
    from `desk_options` (`game`, `records_dir`, `saves_dir`, `lockstep`, `say`,
    `changed`, `today`). The routes are plain functions, so a long poll waits on a worker
    thread and never on the event loop, and never holds the lock while it waits."""
    from freesail.agents.remote import Desk, DeskError

    desk = Desk(lock, world, **desk_options)
    router = APIRouter()

    def call(fn: Callable[..., Any], *args: Any) -> JSONResponse:
        try:
            return JSONResponse(fn(*args))
        except DeskError as e:
            raise HTTPException(status_code=e.status, detail=e.words) from None

    @router.get("/api/agents")
    def api_agents() -> JSONResponse:
        with lock:
            return JSONResponse({"stations": desk.stations()})

    @router.post("/api/agents/{station}")
    def api_station(station: str, body: dict[str, Any]) -> JSONResponse:
        return call(desk.station, station, body)

    # Each call that reads, speaks or orders for a station carries its seating's key
    # (package 37g, item 1; `remote.Desk`): `key` in the query of a GET and in the body of
    # a POST. A call without it is refused in words (409), and nothing is run.

    @router.get("/api/agents/{station}/turns")
    def api_turns(station: str, since: int = 0, wait: float = 0.0, key: str = "") -> JSONResponse:
        return call(desk.turns, station, since, wait, key)

    @router.post("/api/agents/{station}/reply")
    def api_reply(station: str, body: dict[str, Any]) -> JSONResponse:
        return call(desk.reply, station, body)

    @router.post("/api/agents/{station}/owner")
    def api_owner(station: str, body: dict[str, Any]) -> JSONResponse:
        return call(desk.owner, station, str(body.get("text") or ""), body.get("key"))

    @router.post("/api/agents/{station}/release")
    def api_release(station: str, body: dict[str, Any]) -> JSONResponse:
        return call(desk.release, station, str(body.get("reason") or ""), body.get("key"))

    @router.get("/api/agents/{station}/library")
    def api_library(
        station: str, topic: str = "contents", section: str = "", find: str = "", key: str = ""
    ) -> JSONResponse:
        def read(*args: Any) -> dict[str, Any]:
            return {"text": desk.library(*args)}

        return call(read, station, topic, section, find, key)

    @router.get("/api/agents/{station}/picture/{pid}")
    def api_agent_picture(station: str, pid: str, key: str = "") -> Response:
        try:
            pic = desk.picture(station, pid, key)
        except DeskError as e:
            raise HTTPException(status_code=e.status, detail=e.words) from None
        return Response(content=pic.data, media_type=pic.media_type)

    router.desk = desk  # type: ignore[attr-defined]
    return router


# ---------------------------------------------------------------------------
# The browser's shelf (package 33d): completion, the library and the ship's papers
# ---------------------------------------------------------------------------

# The console's own words, which its completer offers and the browser's order line does
# not take: the instruments are its `state` and `muster`, the log panel its `log`, the
# browser its `quit`; `replay` is `--load`. Everything else the completer offers is
# offered as it is (`freesail.orders.complete`).
CONSOLE_ONLY = ("state", "muster", "log", "replay ", "help", "quit")

# The station the browser's captain reads the library as. The library serves every
# station the same pages (`tools.library`); the name only fills its signature.
BROWSER_READER = "captain"


def ship_papers(world: World) -> dict[str, Any]:
    """The ship's papers (package 35; spec M5 §22): the library's `papers` topic, the
    same pages the model's `library(topic='papers')` serves (`freesail.agents.tools`),
    each by handle with its keeper, its place and its last entry; nothing waits any
    more. Read, never logged: the keepers' writing is what the log says."""
    from freesail.agents import tools
    from freesail.world.places import PLACES

    ship = world.ship
    if not hasattr(ship, "spars"):
        return {"papers": [], "waiting": [], "words": "A ship with no parts keeps no papers."}
    top = tools._papers_topic(world)
    papers = []
    for page in world.papers.pages():
        place = PLACES.get(page.place)
        papers.append(
            {
                "handle": page.handle,
                "words": (
                    f"{page.words}; kept by the {page.keeper} in "
                    f"{place.name if place is not None else page.place}; last written {page.as_of}"
                ),
                "lines": page.lines,
                "keeper": page.keeper,
                "place": page.place,
                "as_of": page.as_of,
                "ask": f"library(topic='papers', section='{page.handle}')",
            }
        )
    return {"papers": papers, "waiting": [], "words": "", "title": top.title}


def shelf_routes(lock: Any, world: Callable[[], World]) -> APIRouter:
    """The browser's shelf (package 33d; `docs/design/Presentation.md`, playtest 12's
    notes 1): the console's completer behind the order line, and the reference library
    and the ship's papers in a pane of their own. Every page is the model's `library`
    tool's own (`freesail.agents.tools.library`), the same text from the same Markdown;
    nothing is served the model cannot ask for. All are reads: none writes the log.

        GET /api/complete?line=...&limit=N    the completer's whole-line suggestions
        GET /api/library?topic=&section=&find= a page of the library, as the tool serves it
        GET /api/library/topics               the shelf's index: each topic, its sections
        GET /api/library/papers               the ship's papers, the library's `papers` topic
    """
    from freesail.agents import tools
    from freesail.orders.complete import suggestions

    router = APIRouter()

    @router.get("/api/complete")
    def api_complete(line: str = "", limit: int = 12) -> JSONResponse:
        limit = max(1, min(int(limit), 50))
        with lock:
            found = suggestions(world().ship, line, limit + len(CONSOLE_ONLY))
        offered = [s for s in found if s not in CONSOLE_ONLY][:limit]
        return JSONResponse({"line": line, "suggestions": offered})

    @router.get("/api/library")
    def api_library(topic: str = "contents", section: str = "", find: str = "") -> JSONResponse:
        with lock:
            page = tools.library(world(), BROWSER_READER, topic or "contents", section, find)
        return JSONResponse(
            {
                "topic": topic or "contents",
                "section": section,
                "find": find,
                "title": page.title,
                "reopen": page.reopen,
                "text": str(page),
            }
        )

    @router.get("/api/library/topics")
    def api_library_topics() -> JSONResponse:
        """The topics `library(topic='contents')` names, with the sections each one lists,
        and for each section the words `section=` takes (its number, else its heading)."""
        with lock:
            every = tools._every_topic(world())
        topics = [
            {
                "key": top.key,
                "name": top.name,
                "title": top.title,
                "sections": [
                    {
                        "number": sec.number,
                        "heading": sec.heading,
                        "label": sec.label(),
                        "level": sec.level,
                        "ask": sec.number or sec.heading,
                    }
                    for sec in top.sections
                ],
            }
            for top in every
        ]
        return JSONResponse({"topics": topics})

    @router.get("/api/library/papers")
    def api_library_papers() -> JSONResponse:
        with lock:
            return JSONResponse(ship_papers(world()))

    return router


# ---------------------------------------------------------------------------
# The player's pencil on the chart (package 37n)
# ---------------------------------------------------------------------------
#
# The lines, rings and notes the player lays on the captain's chart in the browser
# (`client/map.js`; the owner's note 5 of 2026-10-09). The server keeps them on the World
# (`World.chart_marks`), so that every save carries them (`World.save`, the checkpoint
# beside it), and gives them back when a save is taken up here (`take_marks`). They are the
# player's own: never in the log, the journal, the readings or the snapshot, and read by
# nothing but the chart; a model's door does not see them. A mark is a place or two on the
# chart as the player clicked them (latitude and longitude on the chart, the plane's metres
# on the plane), never a position of the truth's.

MARK_KINDS = ("line", "ring", "note")
MARKS_MAX = 200  # a voyage's pencilling, and a save that stays small (judgement)
MARK_TEXT_MAX = 200  # characters in a note or a label
MARK_RADIUS_MAX_M = 200 * units.NAUTICAL_MILE  # a ring no wider than the chart's widest view


def _mark_point(p: Any) -> dict[str, float]:
    """A point of a mark: {lat, lon} on the chart or {x, y} on the plane, finite numbers."""
    if not isinstance(p, dict):
        raise ValueError("A mark's point is {lat, lon} or {x, y}.")
    keys = ("lat", "lon") if "lat" in p or "lon" in p else ("x", "y")
    try:
        out = {k: float(p[k]) for k in keys}
    except (KeyError, TypeError, ValueError):
        raise ValueError("A mark's point is {lat, lon} or {x, y}, in numbers.") from None
    if not all(math.isfinite(v) for v in out.values()):
        raise ValueError("A mark's point must be a finite place.")
    if keys[0] == "lat" and not (-90.0 <= out["lat"] <= 90.0 and -180.0 <= out["lon"] <= 180.0):
        raise ValueError("A mark's latitude and longitude are out of range.")
    return out


def clean_mark(body: Any) -> dict[str, Any]:
    """A mark as the client sends it, checked and cut to its fields: `kind` (line, ring,
    note), `points` (two for a line, one for a ring or a note, all on one frame),
    `radius_m` for a ring, `text` for a note (and an optional label on a line or a ring).
    ValueError, in words, for anything else."""
    if not isinstance(body, dict):
        raise ValueError("A mark is an object.")
    kind = str(body.get("kind") or "")
    if kind not in MARK_KINDS:
        raise ValueError(f"A mark is a {', a '.join(MARK_KINDS[:-1])} or a {MARK_KINDS[-1]}.")
    raw = body.get("points")
    want = 2 if kind == "line" else 1
    if not isinstance(raw, list) or len(raw) != want:
        raise ValueError(f"A {kind} has {'two points' if want == 2 else 'one point'}.")
    points = [_mark_point(p) for p in raw]
    if len({tuple(sorted(p)) for p in points}) != 1:
        raise ValueError("A line's two ends are on one chart.")
    mark: dict[str, Any] = {"kind": kind, "points": points}
    text = body.get("text")
    if text is not None:
        text = " ".join(str(text).split())[:MARK_TEXT_MAX]
        if text:
            mark["text"] = text
    if kind == "note" and not mark.get("text"):
        raise ValueError("A note wants some words.")
    if kind == "ring":
        try:
            radius = float(body.get("radius_m"))
        except (TypeError, ValueError):
            raise ValueError("A ring wants its radius in metres.") from None
        if not (math.isfinite(radius) and 0.0 < radius <= MARK_RADIUS_MAX_M):
            raise ValueError("A ring's radius is more than nothing and less than 200 miles.")
        mark["radius_m"] = radius
    return mark


def take_marks(world: World, data: dict[str, Any]) -> None:
    """The marks of a save, given back to the World it was taken up into (a replay makes
    none; a checkpoint holds the same). Marks that do not read are left out, not refused:
    the game loads whatever the pencil did."""
    kept = []
    for i, m in enumerate(data.get("chart_marks") or []):
        try:
            mark = clean_mark(m)
        except ValueError:
            continue
        mark["id"] = str(m.get("id") or f"m{i + 1}")
        kept.append(mark)
    world.chart_marks = kept[:MARKS_MAX]


def _next_mark_id(marks: list[dict[str, Any]]) -> str:
    n = 0
    for m in marks:
        tail = str(m.get("id", ""))[1:]
        if tail.isdigit():
            n = max(n, int(tail))
    return f"m{n + 1}"


def mark_routes(driver: Driver) -> APIRouter:
    """The chart's pencil (package 37n):

        GET    /api/marks          {"marks": [...]}: every mark kept with the game
        POST   /api/marks          a mark (`clean_mark`) -> the mark with its id
        DELETE /api/marks/{id}     rub one out
        DELETE /api/marks          rub them all out

    Every change goes to every page on the socket as {"type": "marks", "marks": [...]}."""
    router = APIRouter()

    def changed() -> list[dict[str, Any]]:
        marks = [dict(m) for m in driver.world.chart_marks]
        driver.emit_marks()
        return marks

    @router.get("/api/marks")
    def api_marks() -> JSONResponse:
        with driver.lock:
            return JSONResponse({"marks": [dict(m) for m in driver.world.chart_marks]})

    @router.post("/api/marks")
    def api_marks_add(body: dict[str, Any]) -> JSONResponse:
        try:
            mark = clean_mark(body)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from None
        with driver.lock:
            marks = list(driver.world.chart_marks)
            if len(marks) >= MARKS_MAX:
                raise HTTPException(
                    status_code=400,
                    detail=f"The chart holds {MARKS_MAX} marks; rub some out first.",
                )
            mark["id"] = _next_mark_id(marks)
            driver.world.chart_marks = [*marks, mark]
            changed()
        return JSONResponse(mark)

    @router.delete("/api/marks/{mark_id}")
    def api_marks_remove(mark_id: str) -> JSONResponse:
        with driver.lock:
            marks = list(driver.world.chart_marks)
            left = [m for m in marks if m.get("id") != mark_id]
            if len(left) == len(marks):
                raise HTTPException(status_code=404, detail=f"No mark {mark_id} on the chart.")
            driver.world.chart_marks = left
            return JSONResponse({"marks": changed()})

    @router.delete("/api/marks")
    def api_marks_clear() -> JSONResponse:
        with driver.lock:
            driver.world.chart_marks = []
            return JSONResponse({"marks": changed()})

    return router


def create_app(
    driver: Driver,
    client_dir: Path = CLIENT_DIR,
    *,
    game: str = "FreeSail's browser game (freesail.ui.server)",
    consent_records: Path | str | None = None,
    saves_dir: Path | str | None = None,
    say: Callable[[str], None] | None = None,
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        driver.start()
        try:
            yield
        finally:
            driver.stop()

    app = FastAPI(title="FreeSail", lifespan=lifespan)
    app.state.driver = driver
    options: dict[str, Any] = {"game": game, "lockstep": driver.lockstep, "say": say}
    if consent_records is not None:
        options["records_dir"] = consent_records
    if saves_dir is not None:
        options["saves_dir"] = saves_dir
    router = agent_routes(
        driver.lock, lambda: driver.world, changed=driver.emit_snapshot, **options
    )
    driver.desk = router.desk  # type: ignore[attr-defined]
    app.include_router(router)
    app.include_router(shelf_routes(driver.lock, lambda: driver.world))  # package 33d
    app.include_router(mark_routes(driver))  # package 37n: the chart's pencil
    # package 42: the chart and the ship's view drawn by the open page for a tool
    from freesail.agents import pictures

    easel = Easel(driver)
    pictures.set_painter(driver.world, easel)
    app.state.easel = easel
    app.include_router(picture_routes(easel))

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(client_dir / "index.html", media_type="text/html")

    @app.get("/api/ship")
    def api_ship() -> JSONResponse:
        with driver.lock:
            ship = driver.world.ship
            if not hasattr(ship, "spars"):
                raise HTTPException(status_code=404, detail="This world has no ship file.")
            return JSONResponse(queries.ship_graph(ship))

    @app.get("/api/state")
    def api_state() -> JSONResponse:
        return JSONResponse(driver.snapshot())

    @app.get("/api/chart")
    def api_chart() -> JSONResponse:
        """The captain's chart for the browser (spec M5 §17, the first half; package 32):
        the coast and the features of the world's chart region, fetched once."""
        with driver.lock:
            chart = queries.chart_block(driver.world)
        if chart is None:
            raise HTTPException(status_code=404, detail="This world has no chart region.")
        return JSONResponse(chart)

    @app.get("/api/log")
    def api_log(
        since: int | None = None, until: int | None = None, limit: int = 200
    ) -> JSONResponse:
        with driver.lock:
            events = driver.world.log.since(since) if since is not None else driver.world.log.all()
            if until is not None:
                events = [e for e in events if e.tick <= until]
            events = events[-max(1, min(limit, 5000)) :]
            return JSONResponse([event_dict(e) for e in events])

    @app.get("/api/save")
    def api_save() -> JSONResponse:
        with driver.lock:
            data = driver.world.save()
            tick = driver.world.clock.tick
        name = f"freesail-seed{data['seed']}-tick{tick}.json"
        return JSONResponse(data, headers={"Content-Disposition": f'attachment; filename="{name}"'})

    @app.post("/api/order")
    def api_order(body: dict[str, Any]) -> JSONResponse:
        text = str(body.get("text") or "").strip()
        if not text:
            raise HTTPException(status_code=400, detail="An order needs some words.")
        return JSONResponse(event_dict(driver.submit(text)))

    @app.post("/api/driver")
    def api_driver(body: dict[str, Any]) -> JSONResponse:
        action = str(body.get("action") or "").lower()
        value = body.get("value")
        try:
            if action == "hold":
                driver.hold()
            elif action == "go":
                driver.go()
            elif action in SPEED_WORDS:
                driver.set_compression(float(value))
            elif action == "tick":
                driver.tick(int(value if value is not None else 1))
            elif action == "standing_orders":
                driver.read_standing_orders(str(value or ""))
            elif action == "save":
                driver.save(str(value or ""))
            elif action == "ease_on_station":  # the instruments' option (package 33d)
                driver.set_ease_on_station(switched_on(value))
            else:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Say hold, go, speed N, tick N, standing_orders FILE, save PATH or "
                        "ease_on_station on|off to the driver."
                    ),
                )
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail=f"'{value}' is not a number.") from None
        return JSONResponse(driver.state())

    @app.websocket("/ws")
    async def ws(websocket: WebSocket) -> None:
        await websocket.accept()
        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

        def listener(message: dict[str, Any]) -> None:
            loop.call_soon_threadsafe(queue.put_nowait, message)

        with driver.lock:
            ship = driver.world.ship
            hello = {
                "type": "hello",
                "ship": queries.ship_graph(ship) if hasattr(ship, "spars") else None,
                "snapshot": driver.snapshot(),
                "log": driver.shown_log(500),
                # the player's pencil on the chart (package 37n), for the chart alone
                "marks": [dict(m) for m in driver.world.chart_marks],
            }
            driver.add_listener(listener)
        try:
            await websocket.send_json(hello)
            receiver = asyncio.ensure_future(_receive_orders(websocket, driver, queue))
            try:
                while True:
                    message = await queue.get()
                    if message.get("type") == "closed":
                        break
                    await websocket.send_json(message)
            finally:
                receiver.cancel()
        except (WebSocketDisconnect, RuntimeError):
            pass
        finally:
            driver.remove_listener(listener)

    app.mount("/client", StaticFiles(directory=str(client_dir)), name="client")
    return app


async def _receive_orders(
    websocket: WebSocket, driver: Driver, queue: asyncio.Queue[dict[str, Any]]
) -> None:
    """Orders and driver commands may also arrive over the socket. When the
    client goes away, a `closed` message on the queue ends the sending loop."""
    try:
        while True:
            data = await websocket.receive_json()
            kind = data.get("type")
            if kind == "order":
                await asyncio.to_thread(driver.submit, str(data.get("text") or ""))
            elif kind == "driver":
                action, value = data.get("action"), data.get("value")
                if action == "hold":
                    driver.hold()
                elif action == "go":
                    driver.go()
                elif action in SPEED_WORDS:
                    driver.set_compression(float(value))
                elif action == "tick":
                    await asyncio.to_thread(driver.tick, int(value or 1))
    except (WebSocketDisconnect, RuntimeError, ValueError, TypeError):
        pass
    finally:
        queue.put_nowait({"type": "closed"})


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------


def say_to_terminal(text: str) -> None:
    """The game's lines about a model's station, on the server's terminal. A model's
    words may hold characters a Windows code page cannot write; they are replaced
    rather than fail the request that carried them."""
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        enc = getattr(sys.stdout, "encoding", None) or "ascii"
        print(text.encode(enc, "replace").decode(enc), flush=True)


def build_world(args: argparse.Namespace) -> World:
    """The server's World from its command line, as the console's (`console.start_world`):
    a save replayed (`--load`), a scenario file (`--scenario`, its orders given later by
    `main`), or the ship, seed, wind and heading."""
    world, _ = start_server_world(args)
    return world


def start_server_world(args: argparse.Namespace) -> tuple[World, Any]:
    """`console.start_world`, and a save's marks on the chart taken up with it (package
    37n): the console draws no chart and leaves them in the file."""
    world, scenario_file = start_world(args)
    if getattr(args, "load", None):
        take_marks(world, replay_mod.load_file(args.load))
    return world, scenario_file


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FreeSail local server")
    ap.add_argument("ship", nargs="?", help="ship file, e.g. data/ships/frigate-36.yaml")
    ap.add_argument("--seed", type=int, help="the seed (default a scenario's, else 1805)")
    ap.add_argument(
        "--time", "--speed", type=float, default=1.0, help="compression, game s per real s"
    )
    ap.add_argument("--load", help="save file to replay and continue from (spec M4 §21)")
    ap.add_argument(REPLAY_ANYWAY_FLAG, action="store_true", help=REPLAY_ANYWAY_HELP)
    ap.add_argument(
        "--scenario",
        help="a scenario file: ship, start, weather script, orders (spec M4 §19)",
    )
    ap.add_argument("--wind", help="wind as 'FROM_DEG,KNOTS', e.g. 225,15")
    ap.add_argument("--heading", type=float, help="starting heading in degrees")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument(
        "--standing-orders", help="a file of standing orders to give at the start (spec M4 §6)"
    )
    ap.add_argument(
        "--watcher", help="station a watcher: 'fake' for the scripted narrator (spec M4 §12)"
    )
    ap.add_argument(
        "--lockstep",
        action="store_true",
        help="hold the clock while a model's door has the floor (spec M4 §13)",
    )
    ap.add_argument(
        "--ease-on-station",
        action="store_true",
        help="ease the clock to 1x whenever a station is sampled or speaks (package 33d)",
    )
    ap.add_argument(
        "--consent-records",
        help="where the consent records are read and written (default docs/agents/consent)",
    )
    ap.add_argument("--saves", help="where a released station saves the game (default saves/)")
    ap.add_argument("--seat", help=SEAT_HELP)
    args = ap.parse_args(argv)

    import uvicorn

    world, scenario_file = start_server_world(args)
    if args.watcher:
        station_watcher(world, args.watcher, out=sys.stdout)
    if scenario_file is not None:
        from freesail.world.scenarios import begin

        for line in scenario_file.lines():
            print(line)
        begin(world, scenario_file)
    if args.standing_orders:
        read_standing_orders(world, args.standing_orders)
    if args.seat:
        from freesail.agents.seat import seat_player

        seat_player(world, args.seat, door="browser")
    # package 33c (decision 30): the starter book is a choice; the opening words, on the
    # terminal and as the browser's first driver line, say how to load it or begin with none
    opening = book_words(world)
    print(opening)
    if not args.load:
        world.record_driver("routine", "driver.book", opening)
    if args.load:
        # the road taken and why, in the same words at every door (package 37d)
        for line in loaded_words(world, args.load):
            print(line)
    driver = Driver(
        world,
        compression=args.time,
        lockstep=args.lockstep,
        ease_on_station=args.ease_on_station,
    )
    app = create_app(
        driver,
        game=f"FreeSail's browser game (freesail.ui.server on port {args.port})",
        consent_records=args.consent_records,
        saves_dir=args.saves,
        say=say_to_terminal,
    )
    print(f"FreeSail server. Seed {world.seed}. Open http://{args.host}:{args.port}/")
    print(
        f"A model's door connects to http://localhost:{args.port} (docs/agents/Harness.md)"
        + ("; the clock waits for it (--lockstep)." if args.lockstep else ".")
    )
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
