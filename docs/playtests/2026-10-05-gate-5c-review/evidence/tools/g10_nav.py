"""Read-only: from the probe's output, how the account stood against the truth through
game 10: by stretch, at every fix, bearing and cast that moved it, and around the two
moments the owner and the lead flagged.

usage: g10_nav.py PROBE_PREFIX
"""
import json
import statistics
import sys

pre = sys.argv[1]
series = [json.loads(x) for x in open(pre + ".series.jsonl", encoding="utf-8")]
events = [json.loads(x) for x in open(pre + ".events.jsonl", encoding="utf-8")]
series = [r for r in series if "err" in r]


def dbt(r):
    d = r.get("doubt_nm")
    return d if d is not None else max(r.get("sig_e", 0), r.get("sig_n", 0))


def stamp(t):
    s = 5 * 3600 + t
    d = 12 + s // 86400
    return f"{d} Jun {s % 86400 // 3600:02d}:{s % 3600 // 60:02d}"


def stretch(name, lo, hi):
    rows = [r for r in series if lo <= r["tick"] <= hi]
    if not rows:
        return
    errs = [r["err"] for r in rows]
    sig = [dbt(r) for r in rows]
    inside = sum(1 for r in rows if r["err"] <= 2.0 * max(dbt(r), 0.01))
    print(
        f"{name:<44} {stamp(lo)} to {stamp(hi)} | error median {statistics.median(errs):5.2f} max {max(errs):5.2f} nm"
        f" | doubt median {statistics.median(sig):5.2f} | truth within twice the doubt {inside / len(rows):4.0%}"
    )


print("== THE ACCOUNT AGAINST THE TRUTH, BY STRETCH")
stretch("Falmouth to the Manacles", 10436, 18300)
stretch("Off the Lizard, beating, to the calm", 18300, 77450)
stretch("At anchor off the Lizard", 77450, 85311)
stretch("The Lizard to Scilly, in fog", 85311, 116428)
stretch("Fog lifted, to the gig", 116428, 135000)
stretch("The gig to the anchor off the Sound", 135000, 140400)
stretch("At anchor off the Sound", 140400, 155200)
stretch("Under way and hove to, to the run in", 155200, 162700)
stretch("The run in, to the cast that moved her", 162700, 169700)
stretch("After the cast, to the anchor", 169706, 171200)
stretch("At anchor in the Sound", 171200, 212400)
stretch("Out of the Sound, to the end", 215051, 226800)
stretch("THE WHOLE GAME", 0, 226801)

print()
print("== EVERY OBSERVATION THAT MOVED THE ACCOUNT HALF A MILE OR MORE, OR WAS 'OUT BY IT'")
print("   (error before is from the series row just before; after is at the event)")
by_tick = {r["tick"]: r for r in series}


def before(t):
    k = (t // 30) * 30
    while k > 0 and k not in by_tick:
        k -= 30
    if k == t:
        k -= 30
    return by_tick.get(k)


for e in events:
    if e["kind"] not in ("reckoning.fix", "bearing.taken", "sounding", "reckoning.noon", "master.place"):
        continue
    text = e["text"]
    if "out by it" not in text and "moved a mile" not in text and "moved two" not in text and "miles to" not in text:
        continue
    b = before(e["tick"])
    eb = f"{b['err']:.2f}" if b else "?"
    sb = f"{dbt(b):.2f}" if b else "?"
    print(f"{e['tick']:>7} {stamp(e['tick'])} [{e['kind']}] error before {eb} nm (doubt {sb}) -> after {e.get('err', '?')} nm (doubt {dbt(e):.2f})")
    print(f"         {text[:330]}")
    if e["kind"] == "sounding":
        print(f"         water under her {e.get('depth_true_fm')} fm (chart {e.get('chart_true_fm')} + tide {e.get('tide_m')} m); chart at the account {e.get('chart_acc_fm')} fm; master's tide allowance {e.get('allow_m')} m")

print()
print("== THE RUN IN, 02:15 TO 04:25 ON 14 JUNE: every fix, bearing and cast")
for e in events:
    if not (162600 <= e["tick"] <= 171200):
        continue
    if e["kind"] not in ("reckoning.fix", "bearing.taken", "sounding", "ship.anchored", "ship.wore", "ship.hove_to", "ship.aweigh", "ship.brought_up", "lookout.land_ahead"):
        continue
    extra = ""
    if e["kind"] == "sounding":
        extra = f" || true water {e.get('depth_true_fm')} fm, chart at account {e.get('chart_acc_fm')} fm, tide {e.get('tide_m')} m, allowed {e.get('allow_m')} m"
    print(f"{e['tick']:>7} {stamp(e['tick'])[7:]} err {e.get('err', '?'):>5} (N {e.get('err_n', 0):+.2f} E {e.get('err_e', 0):+.2f}) doubt {dbt(e):.2f} [{e['kind']}] {e['text'][:215]}{extra}")
