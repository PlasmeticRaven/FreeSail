"""The local web server: a FastAPI app around one world, and the browser client.

    python -m freesail.ui.server data/ships/frigate-36.yaml [--seed N] [--wind FROM,KN]
                                 [--heading DEG] [--time N] [--port 8000] [--watcher fake]
                                 [--lockstep] [--consent-records DIR] [--saves DIR]
    python -m freesail.ui.server --scenario data/scenarios/gate-4c-day.yaml [...]
    python -m freesail.ui.server --load SAVE [...]

then open http://localhost:8000. `--scenario FILE` starts from a scenario file (its
ship, start, weather script, seed, standing orders and first orders; spec M4 §19);
`--load SAVE` replays a save to its last tick and goes on from there, as the console's
`--load` does (spec M4 §21).

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
                        server's disk (also `save PATH` on the command line)
    WS   /ws            every log event as it happens, and a snapshot every
                        tick at 1x, every 10 ticks at 10x, every 60 at 60x and up;
                        at 60x and up the log is rolled up (spec M4 §20): the notable
                        and urgent lines and the captain's come as events, and each
                        hour's routine lines as one {"type": "rollup"} message
                        (`events.RollupView`, the console's and the samples' view)

The agent API (spec M4 §13 as revised, package 28b; `agent_routes`, which the console
hosts too on `--agents-port`): a language model's door is a client of this game.

    POST /api/agents/{station}          {model_name, door, door_note?, session_kind?,
                                        client?, ask_again?}: station an agent, the
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

`--lockstep` holds the clock while a door has the floor (a sample open for it), for
testing at 1x and for competitive play; without it the game runs at its compression and
a door's late reply finds its turn grown by what happened meanwhile (the harness's fold).

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
import sys
import threading
import time
from collections.abc import Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from freesail import units
from freesail.api import queries
from freesail.core import replay as replay_mod
from freesail.core.events import Event, Rollup, RollupView, Severity, Shown, kept, rolls_up
from freesail.core.events import rollup as rolled
from freesail.core.world import World
from freesail.ui.console import (
    ALARM_SPEED,
    SPEED_WORDS,
    check_agents_unattended,
    clamp_compression,
    eased_words,
    read_standing_orders,
    read_standing_orders_path,
    start_world,
    station_watcher,
)

CLIENT_DIR = Path(__file__).resolve().parents[2] / "client"

Listener = Callable[[dict[str, Any]], None]


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

    def __init__(self, world: World, compression: float = 1.0, lockstep: bool = False):
        self.world = world
        self.compression = clamp_compression(compression)
        self.world.compression = self.compression
        self.lockstep = lockstep
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
            e = self.world.submit(text)
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
                self._ease()  # auto-slow: the rest of this batch is not run
                break
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


def event_dict(e: Event) -> dict[str, Any]:
    """An event for the wire: its dictionary plus the watch-and-bells stamp people read."""
    d = e.to_dict()
    d["stamp"] = units.time_stamp(e.ship_time)
    d["kept"] = kept(e)  # shown as it is at any speed: the client's roll-up leaves it out
    return d


# ---------------------------------------------------------------------------
# The app
# ---------------------------------------------------------------------------


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

    @router.get("/api/agents/{station}/turns")
    def api_turns(station: str, since: int = 0, wait: float = 0.0) -> JSONResponse:
        return call(desk.turns, station, since, wait)

    @router.post("/api/agents/{station}/reply")
    def api_reply(station: str, body: dict[str, Any]) -> JSONResponse:
        return call(desk.reply, station, body)

    @router.post("/api/agents/{station}/owner")
    def api_owner(station: str, body: dict[str, Any]) -> JSONResponse:
        return call(desk.owner, station, str(body.get("text") or ""))

    @router.post("/api/agents/{station}/release")
    def api_release(station: str, body: dict[str, Any]) -> JSONResponse:
        return call(desk.release, station, str(body.get("reason") or ""))

    @router.get("/api/agents/{station}/library")
    def api_library(
        station: str, topic: str = "contents", section: str = "", find: str = ""
    ) -> JSONResponse:
        return JSONResponse({"text": desk.library(station, topic, section, find)})

    router.desk = desk  # type: ignore[attr-defined]
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
            else:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Say hold, go, speed N, tick N, standing_orders FILE or save PATH "
                        "to the driver."
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
    world, _ = start_world(args)
    return world


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FreeSail local server")
    ap.add_argument("ship", nargs="?", help="ship file, e.g. data/ships/frigate-36.yaml")
    ap.add_argument("--seed", type=int, help="the seed (default a scenario's, else 1805)")
    ap.add_argument(
        "--time", "--speed", type=float, default=1.0, help="compression, game s per real s"
    )
    ap.add_argument("--load", help="save file to replay and continue from (spec M4 §21)")
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
        "--consent-records",
        help="where the consent records are read and written (default docs/agents/consent)",
    )
    ap.add_argument("--saves", help="where a released station saves the game (default saves/)")
    args = ap.parse_args(argv)

    import uvicorn

    world, scenario_file = start_world(args)
    if args.watcher:
        station_watcher(world, args.watcher, out=sys.stdout)
    if scenario_file is not None:
        from freesail.world.scenarios import begin

        for line in scenario_file.lines():
            print(line)
        begin(world, scenario_file)
    if args.standing_orders:
        read_standing_orders(world, args.standing_orders)
    if args.load:
        print(
            f"Loaded {args.load}: replayed to tick {world.clock.tick}, "
            f"{world.clock.stamp()}; the log's digest is {world.log.digest()[:16]}."
        )
    driver = Driver(world, compression=args.time, lockstep=args.lockstep)
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
