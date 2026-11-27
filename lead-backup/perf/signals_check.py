import sys, os
tree, save = sys.argv[1], sys.argv[2]
sys.path.insert(0, tree); os.chdir(tree)
from freesail.core import replay as R
from freesail.world import signals as SG, service as SV
data = R.load_file(save)
w = R.replay(data, until_tick=30)
cap = getattr(w, "captain", None)
print("papers:", w.scenario.papers)
print("captain role:", getattr(cap, "role", None), "| service_of:", SV.service_of(w) if hasattr(SV, "service_of") else "?")
print("table_of:", SG.table_of(w))
books = SG.books_for(w)
for r in ("kings-ship", "privateer", "cruiser", "merchant", ""):
    print(" carried_by", repr(r), books.table_carried_by(r))
for order in ("the private signal", "show the private signal", "the ship"):
    try:
        out = w.submit("captain", order) if hasattr(w, "submit") else None
        print(order, "->", out)
    except Exception as e:
        print(order, "-> REFUSED:", e)
