"""A small local HTTP server speaking the Messages API's shape, for the API door's tests
(package 42; `tests/test_api_door.py`, truth 86): no network, nothing of the API itself.

It answers `GET /v1/models/{name}` (the model's name as the server reports it, and its
context) and `POST /v1/messages` with the reply the test scripted, streamed as the API
streams (server-sent events: `message_start`, each block's start, deltas and stop,
`message_delta` with the stop reason and the usage, `message_stop`), and keeps every
request: the path, the headers, the body. A request whose `x-api-key` header is not the
test's key is refused (401), as the API would. A scripted reply is a dict:

    {"content": [{"type": "text", "text": "..."},
                 {"type": "tool_use", "name": "say", "input": {...}},
                 {"type": "thinking", "thinking": "", "signature": "sig"}],
     "stop_reason": "end_turn" | "tool_use" | "max_tokens" | "refusal",
     "usage": {"input_tokens": .., "output_tokens": .., "cache_read_input_tokens": ..,
               "cache_creation_input_tokens": ..},
     "model": "another name, to answer as another model",
     "stop_details": {...}}

or a callable taking the request's body and returning one; when the script is spent the
server answers with a short text.
"""

from __future__ import annotations

import json
import threading
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

MODEL = "made-up-model-7"  # a name of no model, as the tests use
CONTEXT = 200_000


class MessagesServer:
    def __init__(
        self,
        key: str,
        replies: list[dict[str, Any] | Callable[[dict[str, Any]], dict[str, Any]]] | None = None,
        models: dict[str, str] | None = None,
        context: int = CONTEXT,
    ):
        self.key = key
        self.replies = list(replies or [])
        # the names asked for to the name the server reports (an alias resolved)
        self.models = models if models is not None else {MODEL: MODEL}
        self.context = context
        self.requests: list[dict[str, Any]] = []
        self.lock = threading.Lock()
        self._srv: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    # -- the server ------------------------------------------------------------------

    def __enter__(self) -> MessagesServer:
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: Any) -> None:  # quiet
                return

            def _keep(self, body: bytes) -> dict[str, Any]:
                entry = {
                    "method": self.command,
                    "path": self.path,
                    "headers": {k.lower(): v for k, v in self.headers.items()},
                    "body": body.decode("utf-8", "replace"),
                }
                with outer.lock:
                    outer.requests.append(entry)
                return entry

            def _json(self, status: int, payload: dict[str, Any]) -> None:
                data = json.dumps(payload).encode("utf-8")
                self.send_response(status)
                self.send_header("content-type", "application/json")
                self.send_header("content-length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _authorised(self) -> bool:
                if self.headers.get("x-api-key") == outer.key:
                    return True
                self._json(
                    401,
                    {
                        "type": "error",
                        "error": {"type": "authentication_error", "message": "invalid x-api-key"},
                    },
                )
                return False

            def do_GET(self) -> None:  # noqa: N802
                self._keep(b"")
                if not self._authorised():
                    return
                path = self.path.split("?")[0]
                if path.startswith("/v1/models/"):
                    name = path.removeprefix("/v1/models/")
                    if name not in outer.models:
                        self._json(
                            404,
                            {
                                "type": "error",
                                "error": {"type": "not_found_error", "message": f"model: {name}"},
                            },
                        )
                        return
                    self._json(
                        200,
                        {
                            "type": "model",
                            "id": outer.models[name],
                            "display_name": "A made-up model",
                            "created_at": "2026-01-01T00:00:00Z",
                            "max_input_tokens": outer.context,
                            "max_tokens": 64000,
                        },
                    )
                    return
                self._json(
                    404, {"type": "error", "error": {"type": "not_found_error", "message": path}}
                )

            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("content-length") or 0)
                body = self.rfile.read(length)
                self._keep(body)
                if not self._authorised():
                    return
                if self.path.split("?")[0] != "/v1/messages":
                    self._json(
                        404,
                        {
                            "type": "error",
                            "error": {"type": "not_found_error", "message": self.path},
                        },
                    )
                    return
                request = json.loads(body)
                with outer.lock:
                    reply = outer.replies.pop(0) if outer.replies else None
                if callable(reply):
                    reply = reply(request)
                if reply is None:
                    reply = {"content": [{"type": "text", "text": "All well."}]}
                if "__status__" in reply:
                    self._json(reply["__status__"], reply["json"])
                    return
                self._stream(request, reply)

            def _stream(self, request: dict[str, Any], reply: dict[str, Any]) -> None:
                self.send_response(200)
                self.send_header("content-type", "text/event-stream")
                self.send_header("cache-control", "no-cache")
                self.end_headers()
                usage = {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cache_creation_input_tokens": 0,
                    "cache_read_input_tokens": 0,
                    **(reply.get("usage") or {}),
                }
                model = reply.get("model") or request.get("model")

                def send(event: str, data: dict[str, Any]) -> None:
                    chunk = f"event: {event}\ndata: {json.dumps(data)}\n\n".encode()
                    self.wfile.write(chunk)

                send(
                    "message_start",
                    {
                        "type": "message_start",
                        "message": {
                            "id": f"msg_test_{len(outer.requests)}",
                            "type": "message",
                            "role": "assistant",
                            "model": model,
                            "content": [],
                            "stop_reason": None,
                            "stop_sequence": None,
                            "usage": {**usage, "output_tokens": 1},
                        },
                    },
                )
                calls = 0
                for i, block in enumerate(reply.get("content") or []):
                    kind = block["type"]
                    if kind == "text":
                        send(
                            "content_block_start",
                            {
                                "type": "content_block_start",
                                "index": i,
                                "content_block": {"type": "text", "text": ""},
                            },
                        )
                        send(
                            "content_block_delta",
                            {
                                "type": "content_block_delta",
                                "index": i,
                                "delta": {"type": "text_delta", "text": block["text"]},
                            },
                        )
                    elif kind == "thinking":
                        send(
                            "content_block_start",
                            {
                                "type": "content_block_start",
                                "index": i,
                                "content_block": {
                                    "type": "thinking",
                                    "thinking": "",
                                    "signature": "",
                                },
                            },
                        )
                        if block.get("thinking"):
                            send(
                                "content_block_delta",
                                {
                                    "type": "content_block_delta",
                                    "index": i,
                                    "delta": {
                                        "type": "thinking_delta",
                                        "thinking": block["thinking"],
                                    },
                                },
                            )
                        send(
                            "content_block_delta",
                            {
                                "type": "content_block_delta",
                                "index": i,
                                "delta": {
                                    "type": "signature_delta",
                                    "signature": block.get("signature", "sig"),
                                },
                            },
                        )
                    elif kind == "tool_use":
                        calls += 1
                        cid = block.get("id") or f"toolu_test_{len(outer.requests)}_{calls}"
                        send(
                            "content_block_start",
                            {
                                "type": "content_block_start",
                                "index": i,
                                "content_block": {
                                    "type": "tool_use",
                                    "id": cid,
                                    "name": block["name"],
                                    "input": {},
                                },
                            },
                        )
                        send(
                            "content_block_delta",
                            {
                                "type": "content_block_delta",
                                "index": i,
                                "delta": {
                                    "type": "input_json_delta",
                                    "partial_json": json.dumps(block.get("input") or {}),
                                },
                            },
                        )
                    send("content_block_stop", {"type": "content_block_stop", "index": i})
                stop = reply.get("stop_reason") or ("tool_use" if calls else "end_turn")
                delta: dict[str, Any] = {"stop_reason": stop, "stop_sequence": None}
                if reply.get("stop_details"):
                    delta["stop_details"] = reply["stop_details"]
                send(
                    "message_delta",
                    {
                        "type": "message_delta",
                        "delta": delta,
                        "usage": {"output_tokens": usage["output_tokens"]},
                    },
                )
                send("message_stop", {"type": "message_stop"})
                self.wfile.flush()

        self._srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._srv.serve_forever, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *exc: Any) -> None:
        if self._srv is not None:
            self._srv.shutdown()
            self._srv.server_close()

    @property
    def url(self) -> str:
        assert self._srv is not None
        host, port = self._srv.server_address[:2]
        return f"http://{host}:{port}"

    # -- what it saw -----------------------------------------------------------------

    def bodies(self) -> list[dict[str, Any]]:
        """The bodies of the messages requests, parsed."""
        with self.lock:
            return [
                json.loads(r["body"])
                for r in self.requests
                if r["method"] == "POST" and r["path"].split("?")[0] == "/v1/messages"
            ]


# ---------------------------------------------------------------------------
# The game's side, a fake credential store and a fake page, for the door's tests
# ---------------------------------------------------------------------------


def fake_store(monkeypatch: Any) -> Any:
    """A credential store of the test's own in place of the platform's, which the tests
    never touch: `keyring`'s backend set to a dictionary for the test's length."""
    import keyring.backend
    import keyring.core

    class FakeStore(keyring.backend.KeyringBackend):
        priority = 1  # type: ignore[assignment]

        def __init__(self) -> None:
            super().__init__()
            self.kept: dict[tuple[str, str], str] = {}

        def get_password(self, service: str, username: str) -> str | None:
            return self.kept.get((service, username))

        def set_password(self, service: str, username: str, password: str) -> None:
            self.kept[(service, username)] = password

        def delete_password(self, service: str, username: str) -> None:
            self.kept.pop((service, username), None)

    store = FakeStore()
    monkeypatch.setattr(keyring.core, "_keyring_backend", store)
    return store


def png(width: int = 4, height: int = 3) -> bytes:
    """A small PNG of the size asked, as a page's canvas would post."""
    import struct
    import zlib

    def chunk(kind: bytes, data: bytes) -> bytes:
        c = kind + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + b"\x80\x90\xa0" * width for _ in range(height))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


class Game:
    """The browser game on a `TestClient`, as the local runner's tests have it, whose clock
    the test turns while the door runs in a thread; `page()` opens a fake page that draws
    the pictures a tool asks for."""

    def __init__(self, tmp_path: Any, station: str = "watcher"):
        from pathlib import Path

        from fastapi.testclient import TestClient

        from freesail.api.session import make_world
        from freesail.core.world import Scenario
        from freesail.ui.server import Driver, create_app

        root = Path(__file__).resolve().parents[1]
        scenario = Scenario(
            wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0
        )
        self.world = make_world(7, str(root / "data/ships/frigate-36.yaml"), scenario)
        self.driver = Driver(self.world)
        self.records = tmp_path / "consent"
        self.saves = tmp_path / "saves"
        self.station = station
        self.app = create_app(
            self.driver,
            game="FreeSail's browser game (freesail.ui.server on port 8000)",
            consent_records=self.records,
            saves_dir=self.saves,
        )
        self.http = TestClient(self.app)
        self.asked: list[dict[str, Any]] = []

    def page(self, width: int = 4, height: int = 3) -> None:
        """A page open on the game, which answers a picture's request with a PNG."""

        def listener(message: dict[str, Any]) -> None:
            if message.get("type") != "picture":
                return
            self.asked.append(dict(message))
            pid = message["id"]

            def post() -> None:
                self.http.post(
                    f"/api/picture/{pid}?width={width}&height={height}",
                    content=png(width, height),
                    headers={"content-type": "image/png"},
                )

            threading.Thread(target=post, daemon=True).start()

        self.driver.add_listener(listener)

    @property
    def harness(self) -> Any:
        return self.world.agents.get(self.station)

    def wait_for(self, test: Callable[[], bool], seconds: float = 15.0) -> None:
        import time

        end = time.monotonic() + seconds
        while time.monotonic() < end:
            with self.driver.lock:
                if test():
                    return
            time.sleep(0.02)
        raise AssertionError("the door did not get there in time")

    def floor_is_the_games(self, replies: int) -> Callable[[], bool]:
        return lambda: (
            self.harness is not None
            and len(self.harness.transcript) > replies
            and self.harness.open_sample is None
        )

    def lines(self, kind: str) -> list[str]:
        return [e.text for e in self.world.log if e.kind == kind]


def run_door(game: Game, argv: list[str], environ: dict[str, str], inp: str = "") -> dict[str, Any]:
    """The API door in a thread against the game and the test's server."""
    import io

    from freesail.agents import api

    got: dict[str, Any] = {"out": io.StringIO()}

    def run() -> None:
        got["code"] = api.main(
            ["--game", "http://testserver", *argv],
            inp=io.StringIO(inp),
            out=got["out"],
            game_http=game.http,
            poll_wait=0.5,
            environ=environ,
        )

    got["thread"] = threading.Thread(target=run, daemon=True)
    got["thread"].start()
    return got


def finished(got: dict[str, Any], seconds: float = 20.0) -> int:
    got["thread"].join(timeout=seconds)
    assert not got["thread"].is_alive(), got["out"].getvalue()
    return got["code"]
