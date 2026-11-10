"""The browser probe's plans (package 98, step 1; `tools/browser_probe.py`): every plan in
`tests/browser_plans/` played at the real page in Chromium, each line typed and its answer,
the frames and the log pane's rows kept side by side, and every expectation of the plan met.

The slow tier (`DAY_FIXTURES` in `tests/conftest.py`: the browser is the fixture), skipped
cleanly where Playwright or its browser is missing, as `tests/test_pictures.py` is; nothing
is ever downloaded. The consent records and the saves go to the test's own folder."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("uvicorn")
pytest.importorskip("playwright.sync_api", reason="Playwright is not installed")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import browser_probe as B  # noqa: E402

PLANS = [p for p in B.plan_files(B.PLANS) if B.is_plan(p)]


@pytest.fixture(scope="module")
def probe_browser():
    """The pre-installed Chromium, launched once for the module's plans."""
    try:
        pw, browser = B.launch_browser()
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"no browser for Playwright here: {e}")
    try:
        yield browser
    finally:
        browser.close()
        pw.stop()


def test_the_plans_are_found_and_each_names_its_game():
    names = {p.stem for p in PLANS}
    assert {"ashore", "deck-and-below", "asleep", "boat-and-visitor", "prisoner"} <= names
    for p in PLANS:
        plan = B.load_plan(p)
        assert bool(plan.scenario) != bool(plan.world) and plan.steps, p


@pytest.mark.parametrize("plan_file", PLANS, ids=[p.stem for p in PLANS])
def test_the_plan_is_played_and_every_line_is_as_the_plan_expects(
    plan_file, probe_browser, tmp_path
):
    result = B.run_plan(
        B.load_plan(plan_file),
        probe_browser,
        tmp_path / "out",
        say=lambda _s: None,
        scratch=tmp_path / "game",
    )
    assert result.ok, "\n".join([*result.failures, "", *result.lines])
