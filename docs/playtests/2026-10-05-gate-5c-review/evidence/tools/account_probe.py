"""Read-only probe: sail a recorded scenario whole under its own book and print how far the
captain's account stands from the truth along the way, with the master's own doubt beside it.
Run once with PYTHONPATH on the tree before a package and once after, and set the two side
by side.

usage: account_probe.py SCENARIO.yaml HOURS [SHIP]

The doubt printed is the master's stated doubt as one figure: the greater axis of his ellipse,
one sigma, in miles (what his sentence gives first: "I would not trust the reckoning within
three miles ..."). A sample is marked * when the true error is more than twice that figure;
the share of such samples is the passage's honesty (package 37e, item 12). The doubt is read
as it stands at the moment of the sample where the build can say it (`Navigation.doubt_now`,
package 37e), and as it stood at the last working of the account on a build before that.
"""
import math
import sys

from freesail.world.scenarios import begin, load_scenario, make_scenario_world

path, hours = sys.argv[1], float(sys.argv[2])
ship = sys.argv[3] if len(sys.argv) > 3 else None
sf = load_scenario(path)
world = make_scenario_world(sf, ship=ship) if ship else make_scenario_world(sf)

NM = 1852.0


def err_nm():
    truth = world.position
    acc = world.navigation.account_now()
    if truth is None or acc is None:
        return float("nan")
    dn = (acc.lat_deg - truth.lat_deg) * 60.0
    de = (acc.lon_deg - truth.lon_deg) * 60.0 * math.cos(math.radians(truth.lat_deg))
    return math.hypot(de, dn)


def doubt_nm():
    """The master's stated doubt as one figure: the greater axis of his ellipse, miles."""
    nav = world.navigation
    now = getattr(nav, "doubt_now", None)
    ellipse = now() if callable(now) else nav.reckoning.ellipse()
    return float(ellipse["semi_major_nm"])


moments = []
KINDS = {
    "reckoning.noon": "noon",
    "ship.aground": "AGROUND",
    "ship.afloat": "afloat",
    "port.pilot_aboard": "pilot aboard",
    "port.pilot_left": "pilot left",
    "ship.anchored": "anchored",
    "ship.brought_up": "brought up",
    "lookout.land_ahead": "land ahead",
    "anchor.dragging": "dragging",
}
counts = {}
landfall_tick = None


def watch(e):
    global landfall_tick
    counts[e.kind] = counts.get(e.kind, 0) + 1
    landfall = e.kind == "lookout.sighting" and e.data.get("landfall")
    if landfall and landfall_tick is None:
        landfall_tick = e.tick
    if landfall or e.kind in KINDS:
        moments.append(
            (e.tick, "landfall" if landfall else KINDS[e.kind], err_nm(), doubt_nm(), e.text[:104])
        )


world.log.subscribe(watch)
begin(world, sf)
series = []
after_landfall = []
total = int(hours * 3600)
for t in range(total):
    world.tick()
    tick = world.clock.tick
    if tick % 1800 == 0:
        series.append((tick, err_nm(), doubt_nm()))
    if landfall_tick is not None and tick - landfall_tick <= 3600 and (tick - landfall_tick) % 300 == 0:
        after_landfall.append(((tick - landfall_tick) // 60, err_nm(), doubt_nm()))
world.log.unsubscribe(watch)

print(f"scenario {path}; {hours} h; log lines {len(world.log.all())}; digest {world.log.digest()[:16]}")
print(
    "account's error from the truth / the master's doubt, miles, every half hour "
    "(tick: err/doubt; * the error more than twice the doubt):"
)
row = []
for tick, e, d in series:
    flag = "*" if e > 2.0 * d else " "
    row.append(f"{tick // 3600:>3}h{(tick % 3600) // 60:02d}:{e:5.2f}/{d:4.2f}{flag}")
    if len(row) == 6:
        print("  " + "  ".join(row))
        row = []
if row:
    print("  " + "  ".join(row))
vals = [e for _, e, _ in series if e == e]
if vals:
    vals_sorted = sorted(vals)
    print(
        f"mean {sum(vals) / len(vals):.2f} nm; median {vals_sorted[len(vals) // 2]:.2f}; "
        f"worst {max(vals):.2f}; share over 1 nm {sum(v > 1 for v in vals) / len(vals):.0%}; "
        f"over 3 nm {sum(v > 3 for v in vals) / len(vals):.0%}"
    )
    pairs = [(e, d) for _, e, d in series if e == e]
    out = sum(e > 2.0 * d for e, d in pairs)
    doubts = sorted(d for _, d in pairs)
    print(
        f"honesty: the error more than twice the stated doubt in {out} of {len(pairs)} samples "
        f"({out / len(pairs):.0%}); the doubt's median {doubts[len(doubts) // 2]:.2f} nm, "
        f"greatest {doubts[-1]:.2f}"
    )
if after_landfall:
    print(
        f"the hour after the landfall (tick {landfall_tick}), minutes: err/doubt: "
        + "  ".join(f"{m}m:{e:.2f}/{d:.2f}" for m, e, d in after_landfall)
    )
print("moments (tick, what, account error nm, doubt nm, text):")
for tick, what, e, d, text in moments:
    print(f"  {tick:>7} {what:<13} {e:5.2f} {d:5.2f}  {text}")
print(
    "counts:",
    {
        k: counts.get(k, 0)
        for k in (
            "bearing.taken",
            "reckoning.fix",
            "sounding",
            "ship.aground",
            "lookout.land_ahead",
            "order.rejected",
        )
    },
)
