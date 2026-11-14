import sys; sys.path.insert(0, "/home/user/FreeSail")
from tests.test_director import directed
from freesail.agents import director as D
from freesail.core.events import for_the_record
w = directed("quiet-passage")
for _ in range(120): w.tick()
cap = next(p for p in w.people.all if p.role in ("captain","commander"))
for t in [f"aboard: {cap.name} is badly hurt [reason: the story]",
          'ship: a cutter "Lark" of Britain at 49 31 N 5 31 W, bound for Plymouth [reason: x]',
          'ship "the ship": struck to the Lark [reason: the story wants a captivity]']:
    D.direct(w, t.split(" [")[0], by="test")
    print(">>", t); print("  ", D.direct(w, t, by="test")[:400])
print("struck:", getattr(w.vessels.own,'struck',None))
print("wounds:", [ (p.name, getattr(p,'wound',None) or getattr(p,'health',None)) for p in w.people.all if p.name==cap.name])
print("play log:", [e.line() for e in w.log.all() if not for_the_record(e)][-6:])
