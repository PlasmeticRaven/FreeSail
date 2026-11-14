import sys
from freesail.world.ports import load_port
from freesail.world.chart import load_chart
c=load_chart("atlantic-east")
a=load_port(sys.argv[1],c); b=load_port(sys.argv[2],c)
print("by_night", a.pilot.by_night, "->", b.pilot.by_night)
print("tracks", sorted(a.tracks), "->", sorted(b.tracks))
for k in ("outer_road","anchorage","mooring","shore"):
    print(k, "depth", getattr(a,k).depth_m, "->", getattr(b,k).depth_m)
print("no warning raised")
