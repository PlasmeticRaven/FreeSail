import sys; sys.path.insert(0, "/home/user/FreeSail")
from tests.test_director import directed
from freesail.agents import director as D
w = directed("quiet-passage")
print("limits:", D.brief_of(w).limits)
print("captain:", [p.name for p in w.people.all][:6])
for _ in range(120): w.tick() if hasattr(w,'tick') else None
print("tick", w.clock.tick)
cap = next(p for p in w.people.all if p.role in ("captain","commander"))
for t in [f"aboard: {cap.name} is badly hurt", f"aboard: {cap.name} is badly hurt [reason: the story]",
          'ship: a cutter "Lark" of Britain at 49 31 N 5 31 W, bound for Plymouth',
          'ship "the ship": struck to the Lark',
          'ship "the ship": struck to the Lark [reason: the story wants a captivity]']:
    print(">>", t); print("  ", D.direct(w, t, by="test")[:300])
print("struck:", getattr(w.vessels.own,'struck',None))
