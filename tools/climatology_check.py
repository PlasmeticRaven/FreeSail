"""Run a thousand simulated months of the climatology and print, by month, the days with
each prevailing quarter and the gale days beside the study's table (spec M5 §2, truth 53;
`docs/design/WeatherSystems.md` §1.1, §1.2, §5).

    python tools/climatology_check.py [--months 1000] [--seed 7] [--step-hours 1]

Each simulated month is a `Weather` of its own, seeded from the master seed and the
month's serial through the same named-stream rule the World uses, advanced hour by hour
with the surface wind read at the box's centre. A day's prevailing quarter is the one
holding the plurality of its hours when it holds at least half (`weather.prevailing`;
S1's indices leave about a tenth of days with none). A day is counted a strong-breeze
day when its mean wind reaches 22 knots (Ushant's 31-knot gust at a gust factor of about
1.25 over water, W §1.2) and a strong-gale day at 41 knots (its 54-knot gust). Ushant's
station is on a cliff and reads high for the open sea, so its counts are a ceiling here.

The test (`tests/test_weather.py`, truth 53) requires the westerly and easterly shares
within `CLIMATOLOGY_TOLERANCE_PCT` of the table in every month.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from freesail import units  # noqa: E402
from freesail.world.weather import (  # noqa: E402
    QUARTERS,
    Climatology,
    Weather,
    load_climatology,
    prevailing,
    quarter_of,
)

# The tolerance on the westerly and easterly shares, in points of per cent (spec M5 §2).
CLIMATOLOGY_TOLERANCE_PCT = 5
# A strong-breeze day and a strong-gale day, by the day's strongest mean wind (W §1.2:
# Ushant's 31- and 54-knot gusts at a gust factor of about 1.25).
STRONG_BREEZE_KN = 22.0
STRONG_GALE_KN = 41.0
DAYS = 30


@dataclass
class MonthCount:
    month: int
    days: int = 0
    by_quarter: dict[str, int] = field(default_factory=lambda: {q: 0 for q in QUARTERS})
    none: int = 0
    strong_breeze_days: int = 0
    strong_gale_days: int = 0
    draws: int = 0
    months: int = 0

    def share(self, q: str) -> float:
        return 100.0 * self.by_quarter[q] / self.days if self.days else 0.0

    @property
    def none_share(self) -> float:
        return 100.0 * self.none / self.days if self.days else 0.0

    def per_month(self, n: int) -> float:
        return n / self.months if self.months else 0.0


def month_stream(seed: int, serial: int) -> random.Random:
    """A month's stream, by the World's rule (`core.rng.Rng.stream`): the seed and a name."""
    digest = hashlib.sha256(f"{seed}:weather:{serial}".encode()).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def run_month(
    month: int, serial: int, seed: int, clim: Climatology, step_h: int = 1, days: int = DAYS
) -> MonthCount:
    start = datetime(1805, month, 1)
    weather = Weather(
        start, month_stream(seed, serial), seed=seed * 1000 + serial, climatology=clim
    )
    count = MonthCount(month=month, months=1)
    t = start
    for _ in range(days):
        quarters = []
        strongest = 0.0
        for _h in range(0, 24, step_h):
            weather.advance(t)
            direction, speed = weather.surface_wind_at(0.0, 0.0, t)
            quarters.append(quarter_of(direction, speed))
            strongest = max(strongest, units.ms_to_knots(speed))
            t += timedelta(hours=step_h)
        q = prevailing(quarters)
        count.days += 1
        if q is None:
            count.none += 1
        else:
            count.by_quarter[q] += 1
        if strongest >= STRONG_BREEZE_KN:
            count.strong_breeze_days += 1
        if strongest >= STRONG_GALE_KN:
            count.strong_gale_days += 1
    count.draws = weather.lows_drawn - weather.LOW_SLOTS  # the lows born after the start
    return count


def run(
    months: int = 1000, seed: int = 7, clim: Climatology | None = None, step_h: int = 1
) -> dict[int, MonthCount]:
    """The counts by calendar month over `months` simulated months, the calendar months
    taken in turn."""
    clim = clim or load_climatology()
    totals = {m: MonthCount(month=m) for m in range(1, 13)}
    for serial in range(months):
        m = serial % 12 + 1
        c = run_month(m, serial, seed, clim, step_h)
        tot = totals[m]
        tot.days += c.days
        tot.none += c.none
        for q in QUARTERS:
            tot.by_quarter[q] += c.by_quarter[q]
        tot.strong_breeze_days += c.strong_breeze_days
        tot.strong_gale_days += c.strong_gale_days
        tot.draws += c.draws
        tot.months += 1
    return totals


def table(totals: dict[int, MonthCount], clim: Climatology) -> list[str]:
    """The tool's table: each month's shares beside the study's, the gale days beside
    Ushant's, and whether the month is within the tolerance."""
    head = (
        f"{'Month':<10}{'W':>6}{'(tab)':>7}{'E':>6}{'(tab)':>7}{'S':>6}{'(tab)':>7}"
        f"{'N':>6}{'(tab)':>7}{'none':>6}{'F6+':>6}{'(Ush)':>7}{'F9+':>6}{'(Ush)':>7}"
        f"{'lows':>6}  within"
    )
    out = [head]
    for m in range(1, 13):
        t = clim.month(m)
        c = totals[m]
        ok = (
            abs(c.share("W") - t.check["westerly_pct"]) <= CLIMATOLOGY_TOLERANCE_PCT
            and abs(c.share("E") - t.check["easterly_pct"]) <= CLIMATOLOGY_TOLERANCE_PCT
        )
        out.append(
            f"{t.name:<10}{c.share('W'):>6.1f}{t.check['westerly_pct']:>7.0f}"
            f"{c.share('E'):>6.1f}{t.check['easterly_pct']:>7.0f}"
            f"{c.share('S'):>6.1f}{t.check['southerly_pct']:>7.0f}"
            f"{c.share('N'):>6.1f}{t.check['northerly_pct']:>7.0f}"
            f"{c.none_share:>6.1f}"
            f"{c.per_month(c.strong_breeze_days):>6.1f}{t.check['ushant_gust31_days']:>7.1f}"
            f"{c.per_month(c.strong_gale_days):>6.1f}{t.check['ushant_gust54_days']:>7.1f}"
            f"{c.per_month(c.draws):>6.1f}  {'yes' if ok else 'NO'}"
        )
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="FreeSail: check the climatology's seeding against the study's table"
    )
    ap.add_argument("--months", type=int, default=1000, help="simulated months (default 1000)")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--step-hours", type=int, default=1, help="the sampling step within a day")
    args = ap.parse_args(argv)
    clim = load_climatology()
    totals = run(args.months, args.seed, clim, args.step_hours)
    print(
        f"{args.months} simulated months at seed {args.seed}, {DAYS} days each, the wind read "
        f"every "
        f"{args.step_hours} hour(s) at the box's centre; the table's shares from {clim.source}"
        f"{' (provisional)' if clim.provisional else ''}."
    )
    print(
        "Days in the month (%) by prevailing quarter, the table's beside; strong-breeze (22 kn) "
        "and "
        "strong-gale (41 kn) days a month beside Ushant's gust-day counts; lows drawn a month."
    )
    for line in table(totals, clim):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
