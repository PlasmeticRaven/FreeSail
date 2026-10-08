"""Read-only check: is the sea breeze what flips the wind off Penlee on 19 June 1805?

Loads the Harpy's save of tick 602,100 from its checkpoint (nothing is written), runs the
world on with the brig left at anchor so that the weather is the game's own, and from 12:27
samples the surface wind each second along a line run north-east at four knots from her
anchorage (roughly the course she stood in on), with the sea breeze as built and with it
set to nothing.
"""
import math
import sys

import freesail.world.weather as weather
from freesail import units
from freesail.core import replay

save = sys.argv[1]
world, how = replay.load(save)
print("loaded by", how, "at tick", world.clock.tick, world.clock.ship_time)
x0, y0 = world.ship_x_km, world.ship_y_km
print("anchored at plane km", round(x0, 3), round(y0, 3), "position", world.position)

START, END = 631_666, 636_653  # aweigh; the strike
KN = 4.0
BEARING = math.radians(45.0)
step_km = units.knots_to_ms(KN) / 1000.0  # km a second


def wind(x, y, breeze_on):
    keep = weather.SEA_BREEZE_MAX_KN
    if not breeze_on:
        weather.SEA_BREEZE_MAX_KN = 0.0
    try:
        d, s = world.systems.surface_wind_at(x, y)
    finally:
        weather.SEA_BREEZE_MAX_KN = keep
    return math.degrees(d) % 360.0, units.ms_to_knots(s)


def turn(a, b):
    return abs((b - a + 180.0) % 360.0 - 180.0)


while world.clock.tick < START:
    world.tick()
print("at", world.clock.ship_time, "conditions:", getattr(world, "conditions", None))

rows = {"moving, breeze as built": [], "moving, breeze off": [], "at anchor, breeze as built": []}
n = 0
while world.clock.tick < END:
    world.tick()
    n += 1
    x = x0 + step_km * n * math.sin(BEARING)
    y = y0 + step_km * n * math.cos(BEARING)
    rows["moving, breeze as built"].append(wind(x, y, True))
    rows["moving, breeze off"].append(wind(x, y, False))
    rows["at anchor, breeze as built"].append(wind(x0, y0, True))

print("sampled", n, "seconds, to", world.clock.ship_time, "; run", round(step_km * n / 1.852, 2), "miles NE")
for name, r in rows.items():
    jumps = [turn(r[i - 1][0], r[i][0]) for i in range(1, len(r))]
    two_points = sum(1 for j in jumps if j >= 22.5)
    one_point = sum(1 for j in jumps if j >= 11.25)
    dirs = sorted({round(d / 11.25) % 32 for d, _ in r})
    speeds = [s for _, s in r]
    print(f"{name}:")
    print(f"   second-to-second turns of a point or more: {one_point}; of two points or more: {two_points}; largest {max(jumps):.0f} deg")
    print(f"   compass points visited: {len(dirs)}; speed {min(speeds):.1f} to {max(speeds):.1f} kn")
# the breeze itself along the moving line
bz = []
for i in range(1, n + 1, 60):
    x = x0 + step_km * i * math.sin(BEARING)
    y = y0 + step_km * i * math.cos(BEARING)
    bx, by = world.systems.sea_breeze(x, y, world.systems.now)
    bz.append(units.ms_to_knots(math.hypot(bx, by)))
print("sea breeze strength along the line at the end time, sampled each minute of run: min %.1f max %.1f kn" % (min(bz), max(bz)))
