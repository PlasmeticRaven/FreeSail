"""The pictures through the doors, with a real browser (package 45, Part A item 1; the
owner's wardroom run of gate m6a, item 11: "ship view and chart reported nonfunctional,
showing a white image", and the model captain's "returned only its catalogue line to me and
no picture at all").

The game's own server is started on a local port, its page opened in the Chromium that
Playwright finds (the pre-installed browser; no download is ever made here), and a station
seated twice: through the API door against the fake Messages API server
(`tests/messages_api.py`), and through the MCP bridge's own in-process client. Each asks
`chart` and `ship_view`, and the test proves **at the far end** (the request body the fake
API received; the MCP result's content) that an image block arrived whose PNG decodes to the
size the tool said and is not blank: the pixels' standard deviation above a floor and dark
strokes present (the coast's ink, the hull and the spars). The first turn, and then the next
after the model shelves the picture, whose stub must tell it what it saw.

Skipped cleanly where Playwright, its browser or Pillow (which decodes the PNG) is missing.
"""

from __future__ import annotations

import base64
import io
import json
import os
import socket
import threading
import time
from pathlib import Path
from typing import Any

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("uvicorn")
pytest.importorskip("anthropic")
sync_api = pytest.importorskip("playwright.sync_api", reason="Playwright is not installed")
PIL_Image = pytest.importorskip("PIL.Image", reason="Pillow decodes the pictures")

import numpy as np  # noqa: E402
from messages_api import MODEL, MessagesServer, fake_store  # noqa: E402

from freesail.agents import api, consent  # noqa: E402
from freesail.agents import mcp_server as M  # noqa: E402
from freesail.agents.remote import GameClient  # noqa: E402
from freesail.ui.server import Driver, create_app  # noqa: E402
from freesail.world.scenarios import begin, load_scenario, make_scenario_world  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
KEY = "a-test-key-of-no-account-0123456789"
MCP_IDENTITY = "made-up-chat-model, as the client lists it"

# A picture is blank when its pixels hardly vary and nothing dark is drawn on it: the
# chart's coast and names are ink on paper, the ship's hull and spars dark on the sky and
# the sea (judgement: a flat white or sky-blue frame has a standard deviation under two).
BLANK_STD = 8.0
DARK_LEVEL = 110
DARK_FRACTION = 0.001


# ---------------------------------------------------------------------------
# The game on a port, and the page in the browser
# ---------------------------------------------------------------------------


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class LiveGame:
    """The browser game served by uvicorn in a thread of this process, on a free port, the
    frigate in pilot water off Falmouth (the chart drawn, the coast in view)."""

    def __init__(self, tmp_path: Path, scenario: str = "data/scenarios/lesson-falmouth.yaml"):
        import uvicorn

        sf = load_scenario(str(ROOT / scenario))
        self.world = make_scenario_world(sf)
        begin(self.world, sf)
        self.world.run(600)
        self.driver = Driver(self.world, compression=60.0)
        self.records = tmp_path / "consent"
        self.saves = tmp_path / "saves"
        self.app = create_app(
            self.driver,
            game="FreeSail's browser game (the pictures' test)",
            consent_records=self.records,
            saves_dir=self.saves,
        )
        self.port = _free_port()
        self.url = f"http://127.0.0.1:{self.port}"
        config = uvicorn.Config(self.app, host="127.0.0.1", port=self.port, log_level="warning")
        self.server = uvicorn.Server(config)
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()
        deadline = time.monotonic() + 20
        while not self.server.started:
            if time.monotonic() > deadline or not self.thread.is_alive():
                raise AssertionError("the game's server did not start")
            time.sleep(0.05)
        self.driver.go()  # the clock runs, so a station is sampled between its turns

    def close(self) -> None:
        self.server.should_exit = True
        self.thread.join(timeout=10)

    @property
    def harness(self) -> Any:
        return self.world.agents.get("watcher")

    def wait_for(self, test: Any, seconds: float = 30.0) -> None:
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            with self.driver.lock:
                if test():
                    return
            time.sleep(0.05)
        raise AssertionError("the door did not get there in time")


@pytest.fixture(scope="module")
def game(tmp_path_factory):
    g = LiveGame(tmp_path_factory.mktemp("pictures"))
    try:
        yield g
    finally:
        g.close()


def chromium_path() -> str | None:
    """The browser to launch: `FREESAIL_CHROMIUM`, else the `chromium` link under
    `PLAYWRIGHT_BROWSERS_PATH` (the pre-installed browser), else Playwright's own default
    (None). Nothing is ever downloaded here."""
    named = os.environ.get("FREESAIL_CHROMIUM")
    if named and Path(named).exists():
        return named
    folder = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if folder and (Path(folder) / "chromium").exists():
        return str(Path(folder) / "chromium")
    return None


@pytest.fixture(scope="module")
def page(game):
    """The game's page open in Chromium, connected and with its chart fetched."""
    try:
        pw = sync_api.sync_playwright().start()
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"Playwright could not start: {e}")
    try:
        browser = pw.chromium.launch(headless=True, executable_path=chromium_path())
    except Exception as e:  # noqa: BLE001
        pw.stop()
        pytest.skip(f"no browser for Playwright here: {e}")
    try:
        pg = browser.new_page(viewport={"width": 1280, "height": 900})
        with pg.expect_response(lambda r: r.url.endswith("/api/chart"), timeout=30_000):
            pg.goto(game.url + "/")
        pg.wait_for_function("document.getElementById('status').textContent === 'connected'")
        pg.wait_for_timeout(500)  # the coast drawn at the next frame
        yield pg
    finally:
        browser.close()
        pw.stop()


# ---------------------------------------------------------------------------
# What a picture must be
# ---------------------------------------------------------------------------


def decode(data: bytes) -> tuple[int, int, np.ndarray]:
    """A PNG's size and its pixels as RGB, decoded by Pillow (not by the page)."""
    img = PIL_Image.open(io.BytesIO(data))
    img.load()
    assert img.format == "PNG", img.format
    rgb = np.asarray(img.convert("RGBA"), dtype=np.float64)
    # over white, as a client shows a transparent picture: a canvas nothing was drawn on
    # is transparent black, which "shows" white, the owner's "white image"
    alpha = rgb[..., 3:4] / 255.0
    flat = rgb[..., :3] * alpha + 255.0 * (1.0 - alpha)
    return img.width, img.height, flat


def must_be_a_picture(data: bytes, width: int, height: int, what: str) -> dict[str, float]:
    keep = os.environ.get("FREESAIL_KEEP_PICTURES")
    if keep:
        Path(keep).mkdir(parents=True, exist_ok=True)
        (Path(keep) / f"{what.replace(' ', '-').replace(chr(39), '')}.png").write_bytes(data)
    w, h, px = decode(data)
    assert (w, h) == (width, height), f"{what}: {w} by {h}, the tool said {width} by {height}"
    lum = px.mean(axis=2)
    std = float(lum.std())
    dark = float((lum < DARK_LEVEL).mean())
    assert std > BLANK_STD, f"{what} is blank (std {std:.1f})"
    assert dark > DARK_FRACTION, f"{what} has no dark strokes ({dark:.4%} dark)"
    return {"std": std, "dark": dark}


def image_blocks(content: Any) -> list[dict[str, Any]]:
    if not isinstance(content, list):
        return []
    return [b for b in content if isinstance(b, dict) and b.get("type") == "image"]


def text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    return " ".join(b.get("text", "") for b in content if isinstance(b, dict))


# ---------------------------------------------------------------------------
# The API door: the first turn, and the next after a shelving
# ---------------------------------------------------------------------------


def _text(t: str) -> dict:
    return {"type": "text", "text": t}


def _call(name: str, **args: Any) -> dict:
    return {"type": "tool_use", "name": name, "input": args}


def test_the_api_door_shows_the_model_the_chart_and_the_ships_view_and_the_stub_says_what_it_saw(
    monkeypatch, tmp_path, game: LiveGame, page
):
    """The first turn asks `chart` and `ship_view`: the next request carries two image
    blocks, each a PNG of the size the tool said, not blank. The model then shelves them
    (as the owner's captain did), and the request after that carries their stubs in the
    pictures' place: a stub says plainly what the picture was and that it was shown, so a
    model reading its own history does not conclude it never saw one (the owner's reading
    of his transcript, 2026-10-11)."""
    fake_store(monkeypatch)
    replies = [
        {"content": [_call("answer", text="Yes, I am willing.")]},
        {
            "content": [
                _text("Let me see the chart and the ship."),
                _call("chart"),
                _call("ship_view", facing="leeward"),
            ]
        },
        {"content": [_text("The Manacles on the quarter."), _call("shelve", book="all")]},
        {"content": [_text("Looking back over what I was shown.")]},
        {"content": [_call("stand_by", until="a glass")]},
    ]
    got: dict[str, Any] = {"out": io.StringIO()}
    with MessagesServer(KEY, replies) as srv:

        def run() -> None:
            got["code"] = api.main(
                [
                    "--game",
                    game.url,
                    "--model",
                    MODEL,
                    "--base-url",
                    srv.url,
                    "--session",
                    "test",
                ],
                inp=io.StringIO("\n"),
                out=got["out"],
                poll_wait=0.5,
                environ={"FREESAIL_API_KEY": KEY},
            )

        t = threading.Thread(target=run, daemon=True)
        t.start()
        try:
            game.wait_for(lambda: game.harness is not None and game.harness.agent.standing_by)
        except AssertionError as e:
            raise AssertionError(f"{e}; the door said: {got['out'].getvalue()[-1500:]}") from None
        with game.driver.lock:
            game.world.submit("stand down the watcher")
        t.join(timeout=30)
        assert not t.is_alive(), got["out"].getvalue()
        bodies = srv.bodies()
    out = got["out"].getvalue()
    assert consent.check(MODEL, game.records) is not None
    # the request after the first turn: the two pictures as images, each decoding to the
    # size the tool said and not blank
    shown = bodies[2]["messages"][-1]["content"]
    results = [b for b in shown if b.get("type") == "tool_result"]
    assert len(results) == 2, json.dumps(shown)[:400]
    measured = {}
    for res, what in zip(results, ("the chart", "the ship's view"), strict=True):
        images = image_blocks(res["content"])
        assert len(images) == 1, f"{what}: {text_of(res['content'])[:300]}"
        assert images[0]["source"]["media_type"] == "image/png"
        words = text_of(res["content"])
        note = [n for e in game.harness.transcript for n in e.get("shown", [])]
        pic = next(n for n in note if (n["view"] == "chart") == (what == "the chart"))
        data = base64.standard_b64decode(images[0]["source"]["data"])
        measured[what] = must_be_a_picture(data, pic["width"], pic["height"], what)
        assert f"{pic['width']} by {pic['height']} pixels" in words
    print("the pictures through the API door:", measured)
    # after the shelving, the next request holds each picture's stub in its place, no
    # image, and the stub says what it was and that it was shown
    after = bodies[3]["messages"]
    stubs = [
        b
        for m in after
        if m["role"] == "user" and isinstance(m["content"], list)
        for b in m["content"]
        if b.get("type") == "tool_result" and "chart" in text_of(b["content"]).lower()
    ]
    assert stubs, json.dumps(after)[-800:]
    assert not image_blocks(stubs[0]["content"])
    stub = text_of(stubs[0]["content"])
    assert "shown to you" in stub and "put back" in stub, stub
    ship_stubs = [
        b
        for m in after
        if m["role"] == "user" and isinstance(m["content"], list)
        for b in m["content"]
        if b.get("type") == "tool_result" and "ship" in text_of(b["content"]).lower()
    ]
    assert ship_stubs and "shown to you" in text_of(ship_stubs[0]["content"])
    # the brief tells the station what a shelved picture is
    assert "shelved picture" in bodies[1]["system"][0]["text"].lower()
    assert KEY not in out


# ---------------------------------------------------------------------------
# The MCP bridge: the same two pictures as image content
# ---------------------------------------------------------------------------


def test_the_mcp_bridge_returns_the_chart_and_the_ships_view_as_images_that_are_not_blank(
    tmp_path, game: LiveGame, page
):
    anyio = pytest.importorskip("anyio")
    pytest.importorskip("mcp")
    from mcp import Client
    from mcp_types import Implementation

    rec = consent.Record(MCP_IDENTITY, "a test runtime", "2026-09-26", consent.YES, answer="Yes.")
    rec.write(game.records)
    bridge = M.Bridge(GameClient(game.url), MCP_IDENTITY, wait=5.0, tell_owner=lambda w: None)
    server = M.build_server(bridge)
    out: dict[str, Any] = {}

    async def script(c: Any) -> None:
        await c.call_tool("readings", {})
        out["chart"] = await c.call_tool("chart", {})
        out["ship"] = await c.call_tool("ship_view", {"facing": "90"})
        out["second"] = await c.call_tool("chart", {})

    async def main() -> None:
        async with Client(
            server, mode="legacy", client_info=Implementation(name="t", version="0"), cache=None
        ) as client:
            await script(client)

    def run() -> None:
        try:
            anyio.run(main)
        except Exception as e:  # noqa: BLE001
            out["error"] = repr(e)

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(timeout=90)
    assert not t.is_alive() and "error" not in out, out.get("error")
    try:
        measured = {}
        for key, what in (
            ("chart", "the chart"),
            ("ship", "the ship's view"),
            ("second", "the chart again"),
        ):
            result = out[key]
            images = [c for c in result.content if c.type == "image"]
            words = "\n".join(c.text for c in result.content if getattr(c, "text", None))
            assert len(images) == 1 and images[0].mime_type == "image/png", words[:300]
            data = base64.standard_b64decode(images[0].data)
            w, h, _ = decode(data)
            assert f"{w} by {h} pixels" in words, words
            measured[what] = must_be_a_picture(data, w, h, what)
        print("the pictures through the MCP bridge:", measured)
    finally:
        with game.driver.lock:
            if game.harness is not None:
                game.world.submit("stand down the watcher")
