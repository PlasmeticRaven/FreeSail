"""The programmer's front door: build a world with a real ship, query it, drive it."""

# The readings' registry is filled when `readings` loads, and its companion modules
# (`action_readings`, `signal_readings`, `damage_readings`, `squadron_readings`,
# `practice_readings`) each import `readings` in turn. Load it first, whichever module of
# this package is asked for first, so that a companion imported on its own (a test file first
# in a worker) does not find the registry half built: found by package 81 (2026-11-07) in
# tests/test_filling.py, which imports `action_readings` before anything has loaded `readings`.
from freesail.api import readings as _readings  # noqa: F401
