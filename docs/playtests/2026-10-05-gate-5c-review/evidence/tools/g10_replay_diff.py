"""Read-only: replay a scratch copy of a save and say exactly how the replayed log
differs from the log in its checkpoint (every differing line, not only the first).

usage: g10_replay_diff.py SAVE.json   (run from the build folder)
"""
import difflib
import sys

from freesail.api.session import ship_factory
from freesail.core import replay as R

path = sys.argv[1]
data = R.load_file(path)
header, cw = R.read_checkpoint(R.checkpoint_path(path))
world = R.build_world(data, ship_factory)
end = data["end_tick"]
inputs = data["inputs"]
i = 0
while True:
    while i < len(inputs) and int(inputs[i]["tick"]) == world.clock.tick:
        R._give(world, inputs[i])
        i += 1
        for agent in list(world.agents.values()):
            agent.on_input()
    if world.clock.tick >= end:
        break
    world.tick()


def lines(w):
    return [f"{e.tick} | {e.kind} | {e.actor} | {e.text[:150]}" for e in w.log.all()]


a, b = lines(cw), lines(world)
print(f"played {len(a)} lines, replayed {len(b)} lines; digests equal: {cw.log.digest() == world.log.digest()}")
n = 0
for d in difflib.unified_diff(a, b, "played", "replayed", lineterm="", n=0):
    print(d[:230])
    n += 1
    if n > 80:
        print("... more")
        break
t, r = cw.position, world.position
print("true position at the end, played:", t, "| replayed:", r)
for name in cw.agents:
    x, y = cw.agents[name], world.agents[name]
    print(f"station {name}: turns held played {len(x.turns)}, replayed {len(y.turns)}; journal entries {len(x.journal.entries) if hasattr(x.journal, 'entries') else '?'} / {len(y.journal.entries) if hasattr(y.journal, 'entries') else '?'}")
