"""The server's guard: the game answers its own page and nobody else's (package 115, part A;
the cold review of milestone 7, 5.7 and 6.1).

The cause it mends: the server took a request from anywhere a browser could send one. A
browser lets any web page open a socket to `ws://localhost:8000/ws` (the same-origin rule
does not hold for sockets), and lets any page send a form-like POST; a page served from an
attacker's name that is made to resolve to this machine (DNS rebinding) is even
"same-origin". So the socket gave the whole game to any page open in the same browser and
obeyed its orders, and the order line it carried read and wrote files.

The guard is one ASGI middleware around the whole app (`PageGuard`), so that every route,
the socket among them, passes the same three questions before anything of the game is
touched:

1. **The Host** a request names is one this server answers at: `localhost`, an address
   given as figures (a page can have such an origin only by being served from that
   address), the machine's own name, or the `--host` it was started with. An attacker's
   name, which is what a rebinding page carries, is never one of them.
2. **The Origin**, which a browser sends with every socket and every cross-origin request,
   is the server's own when it is sent (`http://` and the Host).
3. **The page's mark** (the token): made at the server's start (`Guard.token`) and written
   into the game's own pages as they are served (`Guard.page`), from which `client/token.js`
   sends it with every request of the page's and `client/app.js` with its socket. It is
   asked of the socket, of every request that is not a plain reading (POST, DELETE, ...),
   and of the readings that change something (`/api/director/log` records a reveal); and
   of every request at all, but the client's own scripts, from a device other than the
   machine itself, where the page itself is had only at the address the terminal printed,
   which carries the mark (`?page=...`), and a cookie keeps it for the page's later loads.
The harbour's routes that write the settings, the desktop client's file or a shortcut, or
start, speak to or stop a door, are answered only to a client on the machine itself.

The agents' doors (`/api/agents/...`) have no page: on the machine itself they carry no
mark, are seated by the game's own rule and every later call carries the seating's key
(package 37g); from another device they want the mark as every request there does. The
Host and the Origin rules hold for them too, so that no web page can seat a station.

A refusal is in the game's words and is made before the game is touched: no listener added,
no line written, nothing read.
"""

from __future__ import annotations

import hmac
import ipaddress
import secrets
import socket
from collections.abc import Iterable
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

from starlette.responses import HTMLResponse, JSONResponse

# The mark's names: the header the page's requests carry it in, the query word a socket and
# the terminal's address carry it in, the meta tag the page is given it in, and the cookie a
# page served keeps it in (one per port, so that two games on one machine keep their own).
MARK_HEADER = "x-freesail-page"
MARK_QUERY = "page"
MARK_META = "freesail-page"
MARK_COOKIE = "freesail-page-"

# The plain readings, which change nothing and are answered to a page on the machine itself
# without the mark (a page elsewhere in the browser cannot read their answers: the browser
# keeps a cross-origin answer from it, and the Host rule keeps a rebinding page out).
SAFE_METHODS = frozenset({"GET", "HEAD"})
# The readings that change something, which ask the mark as an order does.
MARKED_READINGS = frozenset({"/api/director/log"})
# The doors' routes (no page, a seating key): the Host and the Origin rules alone.
DOORS_PREFIX = "/api/agents"
# The client's own scripts and styles: the game's code, answered to any device it serves.
CLIENT_PREFIX = "/client/"
# The harbour's routes that write the settings, the desktop client's file (a command that
# client runs) or a shortcut, or start, speak to or stop a door (a program of the
# machine's): answered only to a client on the machine itself, mark or no mark (the lead's
# ruling of 2026-11-14; JUDGEMENT: a device the player trusts with the game is not given
# the machine's programs with it).
HERE_ONLY = ("/api/harbour/settings", "/api/harbour/desktop", "/api/harbour/shortcut")
HERE_ONLY_PREFIX = "/api/harbour/doors"

REFUSED_HOST = (
    "This is FreeSail's game, and it answers only at its own address: localhost on this "
    "machine, or the address its terminal printed."
)
REFUSED_ORIGIN = (
    "The ship takes her orders from the game's own page alone; this came from another page, "
    "and nothing was done."
)
REFUSED_MARK = (
    "The ship takes her orders from the game's own page alone, which carries the game's "
    "mark; this carried none, and nothing was done. Open the game's page again from its "
    "own address."
)
REFUSED_WRONG_MARK = (
    "The ship takes her orders from the game's own page alone, which carries the game's "
    "mark; this carried another, and nothing was done. The game may have been started "
    "again since the page was opened: open the game's page again from its own address."
)
REFUSED_DOOR_ELSEWHERE = (
    "A door from another device comes in with the game's mark, which the address its "
    "terminal printed carries; this carried none, and no station was touched."
)
REFUSED_HERE_ONLY = (
    "The harbour's settings, the desktop client's file, the shortcut and the doors are "
    "kept at the machine the game runs on; they are changed there, not from another device."
)
REFUSED_ELSEWHERE = (
    "From another device the game is opened at the address its terminal printed, which "
    "carries the game's mark; this carried none, or one of an earlier start of the game."
)


def _loopback(host: str) -> bool:
    try:
        ip = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        return host.lower() == "localhost"
    # the machine itself as a server bound to `::` sees it: `::ffff:127.0.0.1`
    mapped = getattr(ip, "ipv4_mapped", None)
    return bool(ip.is_loopback or (mapped is not None and mapped.is_loopback))


def _figures(host: str) -> bool:
    try:
        ipaddress.ip_address(host.strip("[]"))
        return True
    except ValueError:
        return False


def _hostname(host_header: str) -> str:
    """The name of a Host header without its port: `localhost:8000` -> `localhost`,
    `[::1]:8000` -> `[::1]`."""
    h = host_header.strip().lower()
    if h.startswith("["):
        return h.split("]", 1)[0] + "]"
    return h.rsplit(":", 1)[0] if h.count(":") == 1 else h


def machine_names() -> set[str]:
    """The machine's own names, as another device on its network may name it."""
    names: set[str] = set()
    try:
        name = socket.gethostname().lower()
    except OSError:
        return names
    if name:
        names |= {name, f"{name}.local", name.split(".")[0]}
    return names


class Guard:
    """The mark and the names this server answers at. `hosts` are the names given at the
    start (`--host`) beside localhost, the figures and the machine's own names."""

    def __init__(self, hosts: Iterable[str] = (), token: str | None = None):
        self.token = token or secrets.token_urlsafe(24)
        self.hosts = {"localhost"} | machine_names()
        for h in hosts:
            if h:
                self.hosts.add(_hostname(h))

    # -- the three questions -------------------------------------------------------

    def host_ok(self, host_header: str) -> bool:
        name = _hostname(host_header)
        return bool(name) and (name in self.hosts or _figures(name))

    @staticmethod
    def origin_ok(origin: str, host_header: str) -> bool:
        o = origin.strip().lower().rstrip("/")
        h = host_header.strip().lower()
        return o in (f"http://{h}", f"https://{h}")

    def mark_ok(self, given: str | None) -> bool:
        # compared as bytes, so that a mark of any characters is refused, never an error
        if not given:
            return False
        return hmac.compare_digest(str(given).encode("utf-8"), self.token.encode("utf-8"))

    def refusal(self, scope: dict[str, Any]) -> str | None:
        """The words a request is refused in, or None for one the game answers."""
        names = [k.decode("latin-1").lower() for k, _ in scope["headers"]]
        if names.count("host") > 1 or names.count("origin") > 1:
            # read once by the guard and once by the framework, two of either could be read
            # two ways: a request that carries either twice is refused
            return REFUSED_HOST
        headers = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope["headers"]}
        host = headers.get("host", "")
        if not self.host_ok(host):
            return REFUSED_HOST
        origin = headers.get("origin")
        if origin is not None and not self.origin_ok(origin, host):
            return REFUSED_ORIGIN
        path = scope.get("path", "")
        socket_ = scope["type"] == "websocket"
        method = scope.get("method", "GET").upper()
        client = (scope.get("client") or ("", 0))[0] or ""
        here = _loopback(client)
        query = parse_qs(scope.get("query_string", b"").decode("latin-1"))
        given = headers.get(MARK_HEADER) or (query.get(MARK_QUERY) or [None])[0]
        if path == DOORS_PREFIX or path.startswith(DOORS_PREFIX + "/"):
            # the doors: on the machine, seated by the game's rule and then by their key;
            # from another device, the mark as every other request there (the lead's ruling
            # of 2026-11-14), in the request itself
            if here or self.mark_ok(given):
                return None
            return REFUSED_DOOR_ELSEWHERE
        if path.startswith(CLIENT_PREFIX) and not socket_:
            return None  # the game's own scripts and styles
        writes = not socket_ and method not in SAFE_METHODS
        if writes and not here and (path in HERE_ONLY or path.startswith(HERE_ONLY_PREFIX)):
            return REFUSED_HERE_ONLY
        asked = socket_ or method not in SAFE_METHODS or path in MARKED_READINGS or not here
        if not asked:
            return None
        if not given and not socket_ and method in SAFE_METHODS and path not in MARKED_READINGS:
            # a page's own loads after the first (a link followed, the library's window), from
            # another device: plain readings alone; a reading that changes something (the
            # director's log revealed) wants the mark in the request itself, since a page of
            # another port on the same machine is sent the cookie too
            cookie = SimpleCookie()
            try:
                cookie.load(headers.get("cookie", ""))
            except Exception:  # noqa: BLE001  (a malformed cookie is no mark)
                cookie = SimpleCookie()
            kept = cookie.get(self.cookie_name(host))
            given = kept.value if kept is not None else None
        if self.mark_ok(given):
            return None
        if not here:
            return REFUSED_ELSEWHERE
        return REFUSED_WRONG_MARK if given else REFUSED_MARK

    # -- the page ------------------------------------------------------------------

    @staticmethod
    def cookie_name(host_header: str) -> str:
        port = host_header.rsplit(":", 1)[1] if host_header.count(":") == 1 else ""
        if host_header.startswith("[") and "]:" in host_header:
            port = host_header.rsplit("]:", 1)[1]
        return MARK_COOKIE + (port if port.isdigit() else "80")

    def page(self, path: Path, host_header: str = "") -> HTMLResponse:
        """One of the game's pages with its mark in it, and the mark kept in a cookie for
        the page's later loads (a cookie the browser never sends with another site's
        request, and that the page's scripts cannot read)."""
        text = path.read_text(encoding="utf-8")
        meta = f'<meta name="{MARK_META}" content="{self.token}">'
        text = text.replace("<head>", "<head>\n" + meta, 1)
        response = HTMLResponse(text)
        response.set_cookie(
            self.cookie_name(host_header or "localhost:80"),
            self.token,
            httponly=True,
            samesite="strict",
            path="/",
        )
        return response


class PageGuard:
    """The ASGI middleware: every request and socket passes `Guard.refusal` first."""

    def __init__(self, app: Any, guard: Guard):
        self.app = app
        self.guard = guard

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return
        why = self.guard.refusal(scope)
        if why is None:
            await self.app(scope, receive, send)
            return
        if scope["type"] == "http":
            await JSONResponse({"detail": why}, status_code=403)(scope, receive, send)
            return
        # a socket refused before it is accepted: the browser is answered 403, and the
        # game's hello, its listener and its orders are never reached
        message = await receive()  # the socket's opening, answered by the refusal
        if message.get("type") != "websocket.connect":
            return
        await send({"type": "websocket.close", "code": 1008, "reason": ""})


def guard_app(app: Any, guard: Guard) -> Guard:
    """Put the guard around `app` and keep it on the app's state."""
    app.add_middleware(PageGuard, guard=guard)
    app.state.guard = guard
    return guard
