"""The worlds the browser probe's plans start from where no scenario reaches the place by
play in minutes (package 98, step 1; `tools/browser_probe.py`, a plan's `world:`)."""

from __future__ import annotations

from typing import Any


def prisoner() -> Any:
    """The player struck to a crewed French frigate and taken possession of: his person in
    her cabin, a prisoner, his parole not asked (as `tests/test_captive.py` builds it)."""
    from tests.test_captive import _struck_to_a_crewed_frigate

    world, _captor = _struck_to_a_crewed_frigate()
    world.record_driver("routine", "driver.book", "The book of standing orders begins empty.")
    return world
