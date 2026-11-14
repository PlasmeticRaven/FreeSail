"""The game's own page and doors as the tests' client (package 115, part A).

The server answers its own page alone (`freesail.ui.guard`): at its own address, from its
own origin, with the mark it wrote into the page. A test that plays as the page plays as
the page does: `PageClient` is the browser on the machine itself at `http://localhost:8000`
with the page's mark in every request and in its socket's address, and the page's origin;
`DoorClient` is the machine's page and an agent's door side by side: on the doors' routes
it comes as `agents.remote.GameClient` comes (the same address, no origin, no mark, the
seating's key in its calls), elsewhere as the page.

The refusals themselves are tested through real sockets and real requests against a
running server (`LiveGame` below; truths 7-600 on, `tests/test_known_truths.py`).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urljoin, urlsplit

from fastapi.testclient import TestClient

from freesail.ui.guard import DOORS_PREFIX, MARK_HEADER, MARK_QUERY

ROOT = Path(__file__).resolve().parents[1]
OWN = "localhost:8000"
ON_THE_MACHINE = ("127.0.0.1", 50000)


def mark_of(app: Any) -> str:
    return app.state.guard.token


class PageClient(TestClient):
    """The game's own page in a browser on the machine itself."""

    def __init__(self, app: Any, **kw: Any):
        headers = dict(kw.pop("headers", None) or {})
        guard = getattr(getattr(app, "state", None), "guard", None)
        self.mark = guard.token if guard is not None else ""
        if self.mark:
            headers.setdefault(MARK_HEADER, self.mark)
        headers.setdefault("origin", f"http://{OWN}")
        kw.setdefault("base_url", f"http://{OWN}")
        kw.setdefault("client", ON_THE_MACHINE)
        super().__init__(app, headers=headers, **kw)

    def websocket_connect(self, url: str, subprotocols: Any = None, **kwargs: Any) -> Any:
        if self.mark and f"{MARK_QUERY}=" not in url:
            url += ("&" if "?" in url else "?") + urlencode({MARK_QUERY: self.mark})
        return super().websocket_connect(urljoin(f"ws://{OWN}", url), subprotocols, **kwargs)


class DoorClient(PageClient):
    """The machine's own clients side by side, as they are on the owner's machine: an
    agent's door (`agents.remote.GameClient`) on the doors' routes (`/api/agents/...`), with
    no mark and no origin, its seating's key in its calls; the game's own page on every
    other route (the test turns the clock and gives the page's orders as the page does)."""

    def request(self, method: str, url: Any, **kwargs: Any) -> Any:  # type: ignore[override]
        path = urlsplit(str(url)).path
        if path == DOORS_PREFIX or path.startswith(DOORS_PREFIX + "/"):
            # a door's request: nothing of the page's
            self.headers.pop(MARK_HEADER, None)
            self.headers.pop("origin", None)
            try:
                return super().request(method, url, **kwargs)
            finally:
                if self.mark:
                    self.headers[MARK_HEADER] = self.mark
                self.headers["origin"] = f"http://{OWN}"
        return super().request(method, url, **kwargs)


class LiveGame:
    """The game's server run as the owner runs it (`py -m freesail`, its own process, the
    browser not opened), on a free port, from a scratch folder, with its settings, saves and
    scenarios in that folder: the door every guard test comes in by. `mark` is read from the
    harbour's page as a page reads it."""

    def __init__(self, tmp: Any, *flags: str, module: str = "freesail"):
        import socket

        self.tmp = Path(tmp)
        self.saves = self.tmp / "saves"
        self.saves.mkdir(parents=True, exist_ok=True)
        self.settings = self.tmp / "player" / "settings.yaml"
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            self.port = s.getsockname()[1]
        self.flags = flags
        self.module = module  # `freesail` (the harbour) or `freesail.ui.server`
        self.url = f"http://127.0.0.1:{self.port}"
        self.own = f"127.0.0.1:{self.port}"
        self.mark = ""
        self.out = ""

    def __enter__(self) -> LiveGame:
        import os
        import subprocess
        import time

        import httpx

        from freesail import settings as S

        s = S.load_settings(self.settings)
        s["places"]["consent_records"] = str(self.tmp / "consent")
        s["places"]["desktop_config"] = str(self.tmp / "desktop" / "config.json")
        S.save_settings(s, self.settings)
        argv = [sys.executable, "-m", self.module, "--port", str(self.port)]
        if self.module == "freesail":
            argv += ["--no-browser", "--settings", str(self.settings)]
        argv += ["--saves", str(self.saves), *self.flags]
        self.proc = subprocess.Popen(
            argv,
            cwd=str(self.tmp),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env={**os.environ, "PYTHONPATH": str(ROOT), "FREESAIL_SETTINGS": str(self.settings)},
        )
        deadline = time.monotonic() + 90
        while True:
            try:
                page = httpx.get(self.url + "/harbour", timeout=30)
                break
            except httpx.TransportError:
                assert self.proc.poll() is None, "the server ended before it answered"
                assert time.monotonic() < deadline, "the server did not answer"
                time.sleep(0.2)
        found = re.search(r'<meta name="freesail-page" content="([^"]+)">', page.text)
        assert found, "the harbour's page carries no mark"
        self.mark = found.group(1)
        return self

    def __exit__(self, *exc: Any) -> None:
        self.proc.terminate()
        self.out, _ = self.proc.communicate(timeout=30)

    def page(self) -> Any:
        """An HTTP client as the game's own page: its origin and its mark."""
        import httpx

        return httpx.Client(
            base_url=self.url,
            timeout=60,
            headers={MARK_HEADER: self.mark, "origin": f"http://{self.own}"},
        )

    def log_texts(self) -> list[str]:
        with self.page() as c:
            return [e["text"] for e in c.get("/api/log", params={"limit": 5000}).json()]
