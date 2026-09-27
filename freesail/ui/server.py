"""The local web server: a FastAPI app around one world, and the browser client.

    python -m freesail.ui.server data/ships/frigate-36.yaml [--seed N] [--wind FROM,KN]
                                 [--heading DEG] [--time N] [--port 8000] [--watcher fake]

then open http://localhost:8000.

Routes (spec §9.2):

    GET  /              the client, client/index.html
    GET  /client/...    the client's scripts and styles
    GET  /api/ship      the ship graph, for drawing (queries.ship_graph)
    GET  /api/state     the current snapshot (queries.snapshot) plus the driver
    GET  /api/log       the log, optionally ?since=TICK and ?limit=N
    GET  /api/save      the save file (seed, scenario, journal) as a download,
                        the same file `save PATH` writes; the browser can keep it
    POST /api/order     {"text": "..."} -> the accepted or rejected event
    POST /api/driver    {"action": "hold"|"go"|"time"|"tick", "value": N}
                        or {"action": "standing_orders", "value": FILE} to read a file
                        of standing orders (also `read the standing orders from FILE`
                        on the command line, as in the console), or
                        {"action": "save", "value": PATH} to write a save file on the
                        server's disk (also `save PATH` on the command line)
    WS   /ws            every log event as it happens, and a snapshot every
                        tick at 1x, every 10 ticks at 10x, every 60 at 60x and up

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

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from freesail import units
from freesail.api import queries
from freesail.core import replay as replay_mod
from freesail.core.events import Event
from freesail.core.world import Scenario, World
from freesail.ui.console import (
    check_agents_unattended,
    read_standing_orders,
    read_standing_orders_path,
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

    def __init__(self, world: World, compression: float = 1.0):
        self.world = world
        self.compression = compression
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
        self._emit({"type": "event", "event": event_dict(e)})

    # -- state --------------------------------------------------------------

    def state(self) -> dict[str, Any]:
        return {
            "running": self.running,
            "compression": self.compression,
            "snapshot_every": snapshot_interval(self.compression),
        }

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            snap = queries.snapshot(self.world)
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
        with self.lock:
            self.compression = max(0.1, float(value))
            self.emit_snapshot()

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
            return self.world.record(
                "routine",
                "driver.refused",
                "Say 'save somewhere.json'.",
                actor="driver",
                data={"path": path},
            )
        try:
            p = replay_mod.save_to_file(self.world, path)
        except OSError as e:
            return self.world.record(
                "routine",
                "driver.refused",
                f"Could not write {path}: {e.strerror or e}.",
                actor="driver",
                data={"path": path},
            )
        return self.world.record(
            "notable",
            "driver.saved",
            f"Saved to {p} at tick {self.world.clock.tick}.",
            actor="driver",
            data={"path": str(p), "tick": self.world.clock.tick},
        )

    def _read_standing_orders(self, path: str) -> Event:
        try:
            n = read_standing_orders(self.world, path)
        except OSError as e:
            return self.world.record(
                "routine",
                "driver.refused",
                f"Could not read {path or 'the standing orders'}: {e.strerror or e}.",
                actor="driver",
                data={"path": path},
            )
        finally:
            self.emit_snapshot()
        return self.world.record(
            "routine",
            "driver.standing_orders",
            f"Read {n} standing order{'s' if n != 1 else ''} from {path}.",
            actor="driver",
            data={"path": path, "count": n},
        )

    # -- the clock ----------------------------------------------------------

    def _run_ticks(self, n: int) -> None:
        every = snapshot_interval(self.compression)
        for _ in range(n):
            self.world.tick()
            self._ticks_since_snapshot += 1
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
    return d


# ---------------------------------------------------------------------------
# The app
# ---------------------------------------------------------------------------


def create_app(driver: Driver, client_dir: Path = CLIENT_DIR) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        driver.start()
        try:
            yield
        finally:
            driver.stop()

    app = FastAPI(title="FreeSail", lifespan=lifespan)
    app.state.driver = driver

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

    @app.get("/api/log")
    def api_log(since: int | None = None, limit: int = 200) -> JSONResponse:
        with driver.lock:
            events = driver.world.log.since(since) if since is not None else driver.world.log.all()
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
            elif action == "time":
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
                        "Say hold, go, time N, tick N, standing_orders FILE or save PATH "
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
                "log": [event_dict(e) for e in driver.world.log.tail(500)],
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
                elif action == "time":
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


def build_world(args: argparse.Namespace) -> World:
    from freesail.api.session import make_world

    scenario = Scenario()
    if args.wind:
        d, s = args.wind.split(",")
        scenario.wind_from_deg, scenario.wind_speed_kn = float(d), float(s)
    if args.heading is not None:
        scenario.ship_heading_deg = args.heading
    if args.ship:
        return make_world(args.seed, args.ship, scenario)
    return World(seed=args.seed, scenario=scenario)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FreeSail local server")
    ap.add_argument("ship", nargs="?", help="ship file, e.g. data/ships/frigate-36.yaml")
    ap.add_argument("--seed", type=int, default=1805)
    ap.add_argument("--time", type=float, default=1.0, help="compression, game s per real s")
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
    args = ap.parse_args(argv)

    import uvicorn

    world = build_world(args)
    if args.watcher:
        station_watcher(world, args.watcher, out=sys.stdout)
    if args.standing_orders:
        read_standing_orders(world, args.standing_orders)
    driver = Driver(world, compression=args.time)
    app = create_app(driver)
    print(f"FreeSail server. Seed {world.seed}. Open http://{args.host}:{args.port}/")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
