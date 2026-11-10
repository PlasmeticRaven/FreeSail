"""The browser probe (package 98, step 1; the owner's testing procedure of 2026-11-09): play a
plan at the real page in a headless browser, as the player plays it, and say for every line
typed whether he was answered.

    python3 tools/browser_probe.py tests/browser_plans/ashore.yaml [--out DIR] [--chromium PATH]
    python3 tools/browser_probe.py tests/browser_plans/          (every plan in the folder)

The game is started by the server's own road (`freesail.ui.server.prepare_game` from the
plan's flags, the World a plan's `world:` builder makes where no scenario can reach the
place: a prisoner), served by uvicorn in a thread on a free port with the consent records and
the saves in a folder of the run's own (never `docs/agents/consent/`), and stopped when the
plan ends. The page is opened in Chromium (the pre-installed one; nothing is downloaded) and
every websocket frame it is sent is kept. For each line typed at the order line the probe
keeps, side by side: whether a request left the page (`/api/order`, `/api/driver`, or none:
the page took the line itself), the server's answer, the frames the page was sent after it,
the new rows of the log pane and the "Where you are" instrument, and marks the line:

    ANSWERED   the answer's first words are in a new row of the log pane
    OTHER      a row appeared, not the answer
    UNSHOWN    no row appeared

**A plan** (YAML) names its game and its steps:

    name: Ashore at Falmouth
    scenario: tests/browser_plans/neufchatel-falmouth.yaml   # or world: module:function
    flags: [--seat, officer]          # more of the server's flags (optional)
    steps:
      - label: ON DECK                # a heading in the report
      - say: let go the anchor        # typed; `setup: true` expects nothing of it
        setup: true
      - tick: 300                     # the clock advanced, held after
      - say: where am I               # typed; by default expected ANSWERED
      - say: go below
        expect: {sent: order, answered: true, contains: cabin}
      - where: in the cabin           # the instrument must contain the words
      - until: ashore                 # tick until the instrument says it (or the snapshot)
        tick: 60
        max: 90
      - shot: landed                  # a screenshot

A typed line's `expect` is `answered` (the default), `shown` (any new row), `unshown`, or a
mapping of: `answered` (bool), `shown` (bool), `sent` (`order`, `driver` or `none`),
`contains` (words, or a list, each in some new row), `absent` (words in no new row), `kind`
(the answer's kind starts with it). A step that fails is screenshotted
(`<out>/fail-NN.png`). The run writes `report.json` and `report.txt` to `--out` (a folder
of the run's own by default) and exits 1 if any expectation failed, 2 if the browser could
not be started.

The slow tier plays every plan in `tests/browser_plans/` (`tests/test_browser_probe.py`),
skipped where Playwright or its browser is missing, as `tests/test_pictures.py` is.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import socket
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PLANS = ROOT / "tests" / "browser_plans"
SENT_WAIT_S = 1.5  # how long a typed line is given to leave the page
ANSWER_WAIT_S = 60.0  # how long the server is given to answer it
SHOWN_WAIT_S = 2.0  # how long the log pane is watched for the answer's row
QUIET_S = 0.3  # the frames after the answer are kept until the socket is this quiet

# The page's own record of the frames it is sent, put in before its scripts run.
_WIRE_SCRIPT = """
(() => {
  window.__wire = [];
  const Real = window.WebSocket;
  function Probed(url, protos) {
    const ws = protos ? new Real(url, protos) : new Real(url);
    ws.addEventListener("message", (m) => {
      try {
        const d = JSON.parse(m.data);
        if (d.type === "snapshot") window.__lastSnap = d.snapshot;
        else window.__wire.push(d);
      } catch (e) {}
    });
    return ws;
  }
  Probed.prototype = Real.prototype;
  Object.assign(Probed, { OPEN: 1, CLOSED: 3, CONNECTING: 0, CLOSING: 2 });
  window.WebSocket = Probed;
})();
"""


def chromium_path() -> str | None:
    """The browser to launch: `FREESAIL_CHROMIUM`, else the `chromium` link under
    `PLAYWRIGHT_BROWSERS_PATH` (the pre-installed browser), else Playwright's own default
    (None). Nothing is ever downloaded here (as `tests/test_pictures.py`)."""
    named = os.environ.get("FREESAIL_CHROMIUM")
    if named and Path(named).exists():
        return named
    folder = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if folder and (Path(folder) / "chromium").exists():
        return str(Path(folder) / "chromium")
    return None


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


# ---------------------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------------------


@dataclass
class Plan:
    path: Path
    name: str
    steps: list[dict[str, Any]]
    scenario: str | None = None
    world: str | None = None
    flags: list[str] = field(default_factory=list)


def load_plan(path: str | Path) -> Plan:
    p = Path(path)
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or not isinstance(data.get("steps"), list):
        raise ValueError(f"{p}: a plan is a mapping with a list of steps")
    if bool(data.get("scenario")) == bool(data.get("world")):
        raise ValueError(f"{p}: a plan names a scenario or a world, one of them")
    steps = []
    for s in data["steps"]:
        steps.append({"say": s} if isinstance(s, str) else dict(s))
    return Plan(
        path=p,
        name=str(data.get("name") or p.stem),
        steps=steps,
        scenario=data.get("scenario"),
        world=data.get("world"),
        flags=[str(f) for f in data.get("flags") or []],
    )


def plan_files(where: str | Path = PLANS) -> list[Path]:
    p = Path(where)
    if p.is_dir():
        return sorted(p.glob("*.yaml"))
    return [p]


def is_plan(path: Path) -> bool:
    """A plan file (a mapping with `steps`), not a scenario kept beside the plans."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return False
    return isinstance(data, dict) and isinstance(data.get("steps"), list)


# ---------------------------------------------------------------------------------------
# The game on a port
# ---------------------------------------------------------------------------------------


class Game:
    """The plan's game served by uvicorn in a thread of this process on a free port, its
    consent records and saves in `scratch`; the clock held, advanced by the plan's ticks."""

    def __init__(self, plan: Plan, scratch: Path):
        import uvicorn

        from freesail.ui.server import Driver, create_app, prepare_game, server_parser

        records, saves = scratch / "consent", scratch / "saves"
        records.mkdir(parents=True, exist_ok=True)
        saves.mkdir(parents=True, exist_ok=True)
        self.port = _free_port()
        argv = list(plan.flags) + ["--consent-records", str(records), "--saves", str(saves)]
        argv += ["--port", str(self.port)]
        if plan.scenario:
            argv += ["--scenario", str(ROOT / plan.scenario)]
        args = server_parser().parse_args(argv)
        if plan.world:
            module, _, fn = str(plan.world).partition(":")
            world = getattr(importlib.import_module(module), fn)()
        else:
            world = prepare_game(args, say=lambda _line: None)
        self.driver = Driver(world, compression=args.time)
        app = create_app(
            self.driver,
            game=f"FreeSail's browser game (the browser probe, {plan.name})",
            consent_records=records,
            saves_dir=saves,
        )
        self.url = f"http://127.0.0.1:{self.port}"
        config = uvicorn.Config(app, host="127.0.0.1", port=self.port, log_level="warning")
        self.server = uvicorn.Server(config)
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()
        deadline = time.monotonic() + 30
        while not self.server.started:
            if time.monotonic() > deadline or not self.thread.is_alive():
                raise RuntimeError("the game's server did not start")
            time.sleep(0.05)

    def tick(self) -> int:
        with self.driver.lock:
            return int(self.driver.world.clock.tick)

    def close(self) -> None:
        self.server.should_exit = True
        self.thread.join(timeout=15)


# ---------------------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------------------


def _clean(s: str) -> str:
    return " ".join(str(s or "").split())


def _head(text: str) -> str:
    """The first words of an answer, as the log pane shows them (its first line, its
    whitespace closed up, sixty characters)."""
    return _clean(str(text or "").split("\n")[0])[:60]


class Page:
    def __init__(self, browser: Any, url: str):
        self.page = browser.new_page(viewport={"width": 1600, "height": 1000})
        self.errors: list[str] = []
        self.page.on("pageerror", lambda e: self.errors.append(str(e)))
        self.page.add_init_script(_WIRE_SCRIPT)
        self.page.goto(url + "/", wait_until="domcontentloaded")
        self.page.wait_for_function(
            "window.__wire && window.__wire.some(d => d.type === 'hello')", timeout=60_000
        )
        self.page.wait_for_timeout(300)

    def rows(self) -> list[str]:
        return self.page.eval_on_selector_all(
            "#log-list > *", "els => els.map(e => e.innerText.replace(/\\s+/g, ' ').trim())"
        )

    def where(self) -> str:
        try:
            return _clean(self.page.eval_on_selector("#i-knowledge", "e => e.textContent"))
        except Exception:  # noqa: BLE001
            return ""

    def snapshot_text(self) -> str:
        return str(self.page.evaluate("JSON.stringify(window.__lastSnap || {})"))

    def wire_len(self) -> int:
        return int(self.page.evaluate("window.__wire.length"))

    def wire_from(self, n: int) -> list[dict[str, Any]]:
        return self.page.evaluate(
            """n => window.__wire.slice(n).map(d => {
                 const e = d.event || d.rollup || d.line || {};
                 return {type: d.type, kind: e.kind || '', text: e.text || ''};
               })""",
            n,
        )

    def type_line(self, text: str) -> dict[str, Any]:
        before = len(self.rows())
        w0 = self.wire_len()
        t0 = time.monotonic()
        answer: dict[str, Any] | None = None
        box = self.page.locator("#command")
        box.fill(text)

        def leaves(r: Any) -> bool:
            return r.method == "POST" and (
                r.url.endswith("/api/order") or r.url.endswith("/api/driver")
            )

        request = None
        try:
            with self.page.expect_request(leaves, timeout=SENT_WAIT_S * 1000) as got:
                box.press("Enter")
            request = got.value
        except Exception:  # noqa: BLE001  (no request left the page: it took the line itself)
            request = None
        sent = "none"
        if request is not None:
            sent = "order" if request.url.endswith("/api/order") else "driver"
            deadline = time.monotonic() + ANSWER_WAIT_S
            resp = None
            while resp is None and time.monotonic() < deadline:
                try:
                    resp = request.response()
                except Exception:  # noqa: BLE001
                    resp = None
                if resp is None:
                    self.page.wait_for_timeout(100)
            if resp is not None:
                try:
                    answer = resp.json()
                except Exception:  # noqa: BLE001
                    answer = {"status": resp.status}
        said = str((answer or {}).get("text") or "") if sent == "order" else ""
        head = _head(said)
        # the pane watched until the answer's row is in it, or SHOWN_WAIT_S
        deadline = time.monotonic() + SHOWN_WAIT_S
        new: list[str] = []
        while True:
            new = self.rows()[before:]
            if head and any(head in r for r in new):
                break
            if time.monotonic() > deadline:
                break
            self.page.wait_for_timeout(100)
        # and the socket until it is quiet
        n = self.wire_len()
        while True:
            self.page.wait_for_timeout(int(QUIET_S * 1000))
            m = self.wire_len()
            if m == n:
                break
            n = m
        new = self.rows()[before:]
        if head and any(head in r for r in new):
            mark = "ANSWERED"
        elif new:
            mark = "OTHER"
        else:
            mark = "UNSHOWN"
        return {
            "text": text,
            "ms": int((time.monotonic() - t0) * 1000),
            "sent": sent,
            "answer": (
                {"kind": str(answer.get("kind") or ""), "text": said}
                if sent == "order" and isinstance(answer, dict)
                else answer
            ),
            "wire": self.wire_from(w0),
            "rows": new,
            "where": self.where(),
            "mark": mark,
        }

    def tick(self, n: int) -> None:
        self.page.evaluate(
            """n => fetch('/api/driver', {method: 'POST',
                 headers: {'Content-Type': 'application/json'},
                 body: JSON.stringify({action: 'tick', value: n})}).then(r => r.json())""",
            int(n),
        )

    def caught_up(self, tick: int, seconds: float = 120.0) -> bool:
        """Wait until the page has taken the snapshot of `tick` (an hour ticked at 1x is
        3600 snapshots on the socket, and the page reads them one by one)."""
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            got = self.page.evaluate("(window.__lastSnap || {}).tick")
            if got is not None and int(got) >= tick:
                return True
            self.page.wait_for_timeout(100)
        return False

    def shot(self, path: Path) -> None:
        self.page.screenshot(path=str(path))


# ---------------------------------------------------------------------------------------
# Expectations
# ---------------------------------------------------------------------------------------


def _expectation(step: dict[str, Any]) -> dict[str, Any]:
    exp = step.get("expect")
    if exp is None:
        return {} if step.get("setup") else {"answered": True}
    if isinstance(exp, str):
        return {
            "answered": {"answered": True},
            "shown": {"shown": True},
            "unshown": {"shown": False},
        }[exp]
    return dict(exp)


def judge(step: dict[str, Any], r: dict[str, Any]) -> list[str]:
    """What a typed line's record fails of its step's expectation, in words (empty: met)."""
    exp = _expectation(step)
    bad: list[str] = []
    rows = r["rows"]
    if "sent" in exp and r["sent"] != exp["sent"]:
        bad.append(f"sent to {r['sent']}, expected {exp['sent']}")
    if exp.get("answered") is True and r["mark"] != "ANSWERED":
        bad.append(f"the answer not shown ({r['mark']})")
    if exp.get("answered") is False and r["mark"] == "ANSWERED":
        bad.append("the answer shown, expected not")
    if exp.get("shown") is True and not rows:
        bad.append("no row shown")
    if exp.get("shown") is False and rows:
        bad.append(f"a row shown, expected none: {rows[0][:80]}")
    contains = exp.get("contains")
    for words in [contains] if isinstance(contains, str) else contains or []:
        if not any(str(words).lower() in x.lower() for x in rows):
            bad.append(f"no row contains {words!r}")
    absent = exp.get("absent")
    for words in [absent] if isinstance(absent, str) else absent or []:
        if any(str(words).lower() in x.lower() for x in rows):
            bad.append(f"a row contains {words!r}, expected none")
    kind = exp.get("kind")
    if kind:
        got = str((r.get("answer") or {}).get("kind") or "")
        if not got.startswith(str(kind)):
            bad.append(f"the answer's kind {got!r}, expected {kind!r}")
    return bad


# ---------------------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------------------


@dataclass
class Result:
    plan: Plan
    records: list[dict[str, Any]]
    failures: list[str]
    lines: list[str]
    out: Path

    @property
    def ok(self) -> bool:
        return not self.failures


def _line_words(r: dict[str, Any]) -> str:
    a = r.get("answer")
    if isinstance(a, dict) and "kind" in a:
        said = f"{a['kind']}: {_clean(a.get('text', ''))[:110]}"
    else:
        said = json.dumps(a)[:110] if a is not None else "(no request left the page)"
    wire = ", ".join(w["kind"] or w["type"] for w in r["wire"]) or "(nothing)"
    pane = " | ".join(x[:110] for x in r["rows"]) or "(nothing)"
    return (
        f"{r['mark']:<9} {r['ms']:>5}ms  > {r['text']}\n"
        f"             sent:   {r['sent']}\n"
        f"             server: {said}\n"
        f"             wire:   {wire}\n"
        f"             pane:   {pane}"
    )


def run_plan(
    plan: Plan, browser: Any, out: Path, say: Any = print, scratch: Path | None = None
) -> Result:
    """Play one plan in `browser` (a Playwright Chromium), its record written to `out`."""
    out.mkdir(parents=True, exist_ok=True)
    scratch = scratch or Path(tempfile.mkdtemp(prefix="probe-"))
    records: list[dict[str, Any]] = []
    failures: list[str] = []
    lines: list[str] = []

    def tell(s: str) -> None:
        lines.append(s)
        say(s)

    game = Game(plan, scratch)
    page = None
    try:
        page = Page(browser, game.url)
        tell(f"# {plan.name} ({plan.path.name})")
        fails = 0
        for i, step in enumerate(plan.steps, 1):
            where = f"step {i}"
            if "say" in step:
                r = page.type_line(str(step["say"]))
                r["setup"] = bool(step.get("setup"))
                r["step"] = i
                bad = judge(step, r)
                r["failed"] = bad
                records.append(r)
                tell(_line_words(r) + ("".join(f"\n             FAILED: {b}" for b in bad)))
                if bad:
                    failures += [f"{where} '{step['say']}': {b}" for b in bad]
            elif "label" in step:
                records.append({"label": step["label"], "step": i})
                tell(f"\n=== {step['label']} === ({page.where()[:100]})")
                continue
            elif "until" in step:
                words = str(step["until"])
                reached = False
                for _ in range(int(step.get("max", 60))):
                    page.tick(int(step.get("tick", 60)))
                    page.caught_up(game.tick())
                    if words in page.where() or words in page.snapshot_text():
                        reached = True
                        break
                tell(f"  (until {words!r}: {'reached' if reached else 'NOT reached'})")
                records.append({"until": words, "reached": reached, "step": i})
                bad = [] if reached else [f"{where}: {words!r} not reached"]
                failures += bad
            elif "tick" in step:
                page.tick(int(step["tick"]))
                page.caught_up(game.tick())
                page.page.wait_for_timeout(200)
                records.append({"tick": int(step["tick"]), "step": i})
                continue
            elif "where" in step:
                got = page.where()
                ok = str(step["where"]).lower() in got.lower()
                tell(f"  (where: {got[:120]!r} {'ok' if ok else 'FAILED'})")
                records.append({"where": got, "expected": step["where"], "step": i, "ok": ok})
                bad = [] if ok else [f"{where}: where-you-are lacks {step['where']!r}"]
                failures += bad
            elif "shot" in step:
                page.shot(out / f"{i:02d}-{step['shot']}.png")
                continue
            else:
                raise ValueError(f"{plan.path}: step {i} is none of the probe's: {step}")
            if bad:
                fails += 1
                page.shot(out / f"fail-{i:02d}.png")
        typed = [r for r in records if "text" in r and not r.get("setup")]
        unshown = sum(1 for r in typed if r["mark"] == "UNSHOWN")
        tell(
            f"\n{unshown} of {len(typed)} lines typed got no line in the log pane; "
            f"{len(failures)} expectation(s) failed."
        )
        if page.errors:
            tell("the page's errors: " + "; ".join(page.errors[:5]))
    finally:
        if page is not None:
            page.page.close()
        game.close()
    (out / "report.json").write_text(json.dumps(records, indent=1, default=str), "utf-8")
    (out / "report.txt").write_text("\n".join(lines) + "\n", "utf-8")
    return Result(plan, records, failures, lines, out)


def launch_browser() -> tuple[Any, Any]:
    """(playwright, browser), the pre-installed Chromium; raises where none can be had."""
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    try:
        return pw, pw.chromium.launch(headless=True, executable_path=chromium_path())
    except Exception:
        pw.stop()
        raise


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("plans", nargs="*", default=[str(PLANS)], help="plan files or a folder")
    ap.add_argument("--out", help="where the reports and screenshots go (a new folder)")
    ap.add_argument("--chromium", help="the browser to launch (else the pre-installed one)")
    args = ap.parse_args(argv)
    if args.chromium:
        os.environ["FREESAIL_CHROMIUM"] = args.chromium
    files = [f for p in args.plans for f in plan_files(p) if is_plan(f)]
    out = Path(args.out) if args.out else Path(tempfile.mkdtemp(prefix="browser-probe-"))
    try:
        pw, browser = launch_browser()
    except Exception as e:  # noqa: BLE001
        print(f"The probe could not start a browser: {e}", file=sys.stderr)
        return 2
    failed = 0
    try:
        for f in files:
            r = run_plan(load_plan(f), browser, out / f.stem)
            failed += not r.ok
            for x in r.failures:
                print(f"FAILED {f.name}: {x}")
    finally:
        browser.close()
        pw.stop()
    print(f"\n{len(files) - failed} of {len(files)} plans met; the record is in {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
