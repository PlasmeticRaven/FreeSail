import json, sys
from collections import Counter
sys.path.insert(0, sys.argv[2])
from freesail.world.weather import VISIBILITY_NM
order = sorted(VISIBILITY_NM, key=lambda k: -VISIBILITY_NM[k])
rung = {w: i for i, w in enumerate(order)}
THICKER = {"The fog is thickening.", "The fog has shut in thick.", "A fog is settling in.", "Fog came down."}
THINNER = {"The fog seems to be clearing.", "The fog is thinning.", "The fog lifted."}
tot = Counter()
for line in open(sys.argv[1]):
    r = json.loads(line)
    if r["error"]:
        print(r["id"], "ERROR", r["error"][-300:]); continue
    M = r["minutes"]  # index m = minute m+1 (tick (m+1)*60)
    at = lambda minute: M[minute - 1] if 1 <= minute <= len(M) else None
    fogmin = sum(1 for x in M if x[0] == "fog")
    fogs = sum(1 for i in range(1, len(M)) if M[i][0] == "fog" and M[i - 1][0] != "fog")
    jumps = [(i + 1, M[i - 1][1], M[i][1]) for i in range(1, len(M)) if abs(rung[M[i][1]] - rung[M[i - 1][1]]) > 1]
    fl = [l for l in r["lines"] if l[1] in ("weather.fog", "weather.change") and ("fog" in l[3].lower() or "Fog" in l[3])]
    notable = [l for l in fl if l[2] in ("notable", "urgent")]
    nofog = [l for l in fl if l[1] == "weather.fog" and (at(l[0]) is None or at(l[0])[0] != "fog")]
    contra = []
    for a, b in zip(fl, fl[1:]):
        da = a[3].split(". ")[0] + "." if not a[3].endswith(".") else a[3]
        ta = a[3] in THICKER or a[3].startswith("A fog") ; tb = b[3] in THICKER
        tha = any(a[3].startswith(x) for x in THINNER); thb = any(b[3].startswith(x) for x in THINNER)
        if b[0] - a[0] <= 10 and ((ta and thb) or (tha and tb)):
            contra.append((a, b))
    # lost: in fog, the sight differs from the last said for 15+ minutes running
    said, run, lost = None, 0, []
    byminute = {}
    for l in fl:
        byminute.setdefault(l[0], []).append(l)
    for mi in range(1, len(M) + 1):
        x = at(mi)
        for l in byminute.get(mi, []):
            said = x[1] if x[0] == "fog" else None
        if x[0] == "fog" and said is not None and x[1] != said:
            run += 1
            if run == 15:
                lost.append((mi, said, x[1]))
        else:
            run = 0
        if x[0] != "fog":
            said = None
    hours = fogmin / 60.0
    per_fog = Counter()
    print(f"{r['id']:18s} fog_minutes={fogmin:5d} fogs={fogs:3d} lines={len(fl):4d} notable={len(notable):4d} "
          f"notable/fog={len(notable)/max(1,fogs):.1f} notable/fog-hour={len(notable)/max(1e-9,hours) if hours else 0:.2f} "
          f"jumps>1={len(jumps)} contra10={len(contra)} fogline_not_fog={len(nofog)} lost15={len(lost)}")
    for j in jumps[:3]: print("    JUMP", j)
    for c in contra[:3]: print("    CONTRA", c)
    for n in nofog[:3]: print("    NOFOG", n, at(n[0]))
    for x in lost[:3]: print("    LOST", x)
    tot.update(fog_minutes=fogmin, fogs=fogs, lines=len(fl), notable=len(notable), jumps=len(jumps), contra=len(contra), nofog=len(nofog), lost=len(lost))
    # busiest hour of notable fog lines
    hourly = Counter(l[0] // 60 for l in notable)
    if hourly: tot["max_notable_in_an_hour"] = max(tot["max_notable_in_an_hour"], max(hourly.values()))
print("TOTAL", dict(tot))
