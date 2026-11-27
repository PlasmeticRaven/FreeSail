import sys, json
sys.path.insert(0, ".")
from datetime import datetime
mode, path = sys.argv[1], sys.argv[2]
from freesail.core.replay import write_checkpoint, read_checkpoint
if mode == "write":
    from tests.test_chart import SCHOONER, chart_world, high_over_the_channel
    w = chart_world(50.12, -5.03, ship=SCHOONER, start=datetime(1805, 6, 5, 7, 0),
                    systems=high_over_the_channel(datetime(1805, 6, 1, 0, 0)))
    w.run(int(sys.argv[3]))
    write_checkpoint(w, path)
    print("written at", w.clock.ship_time, w.conditions.weather, w.conditions.visibility,
          [e.text for e in w.log if e.kind.startswith("weather.") and "fog" in e.text.lower()])
else:
    _, w = read_checkpoint(path)
    n0 = len(w.log)
    print("loaded at", w.clock.ship_time, w.conditions.weather, w.conditions.visibility, getattr(w, "_fog_said", "n/a"))
    for m in range(int(sys.argv[3])):
        w.run(60)
        for e in w.log[n0:]:
            if e.kind in ("weather.fog", "weather.change"):
                print(f"  +{m+1:3d}m {w.clock.ship_time:%H:%M} {e.kind} {e.severity.value}: {e.text} [vis now {w.conditions.visibility}]")
        n0 = len(w.log)
    print("end", w.clock.ship_time, w.conditions.weather, w.conditions.visibility)
