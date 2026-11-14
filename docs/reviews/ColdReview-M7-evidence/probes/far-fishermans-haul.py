import sys; sys.path.insert(0, "/home/user/FreeSail/tests"); sys.path.insert(0, "/home/user/FreeSail")
from test_fishing import world_at, GERRANS
from freesail.world import fishing as F
from freesail.world.ships import vessel_from_spec
w = world_at(ship="data/ships/smack.yaml", lat=49.85, lon=-5.2)
print("player hold salt before", w.hold.goods.get("salt"))
w.hold.goods["salt"] = w.hold.goods.get("salt", 0) or 2.0
w.ship.extra["gear_drag"] = F.TRAWL_DRAG
print("player salt set", w.hold.goods.get("salt"), "drag", w.ship.extra.get("gear_drag"))
w.vessels.serial += 1
v = vessel_from_spec(w, {"description": "smack","name": "Brothers","nation": "britain",
 "position": {"lat_deg": GERRANS[0], "lon_deg": GERRANS[1]},"goal": "bound for Falmouth",
 "intent": "fish on the seine ground in Gerrans Bay for 2 hours from Falmouth"}, w.vessels.serial)
w.vessels.add(v)
fy = F.far_fishery(v)
for _ in range(int(F._shoot_s("seine")//60)+1): F.far_work(w, v, 60.0)
for _ in range(60): F.far_work(w, v, 60.0)
for _ in range(int(F._haul_s("seine")//60)+1): F.far_work(w, v, 60.0)
print("far catch tons", fy.catch.tons(), [ (l.fish, getattr(l,'salted',None)) for l in fy.catch.lots][:5])
print("player salt after", w.hold.goods.get("salt"), "drag after", w.ship.extra.get("gear_drag"))
