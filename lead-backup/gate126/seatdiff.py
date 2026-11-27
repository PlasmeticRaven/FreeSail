"""Compare two seat.py outputs: every served item and every order's answer that differs.

    python3 -I <probes>/gate/seatdiff.py OLD.json NEW.json [--full]
"""

import difflib
import json
import sys


def main(argv):
    a, b = json.load(open(argv[0])), json.load(open(argv[1]))
    full = "--full" in argv
    n_served = n_orders = d_served = d_orders = 0
    for ship in sorted(set(a) | set(b)):
        ra, rb = a.get(ship, {}), b.get(ship, {})
        if ra.get("error") or rb.get("error"):
            print("ERROR", ship, (ra.get("error") or "")[-200:], (rb.get("error") or "")[-200:])
        sa, sb = ra.get("served", {}), rb.get("served", {})
        for k in sorted(set(sa) | set(sb)):
            n_served += 1
            if sa.get(k) != sb.get(k):
                d_served += 1
                print(f"SERVED {ship} {k}")
                x = json.dumps(sa.get(k), indent=1, sort_keys=True).splitlines()
                y = json.dumps(sb.get(k), indent=1, sort_keys=True).splitlines()
                for line in list(difflib.unified_diff(x, y, lineterm="", n=0))[2:(None if full else 12)]:
                    print("   ", line[:400])
        oa, ob = ra.get("orders", {}), rb.get("orders", {})
        for k in sorted(set(oa) | set(ob)):
            n_orders += 1
            if oa.get(k) != ob.get(k):
                d_orders += 1
                x, y = oa.get(k) or {}, ob.get(k) or {}
                print(f"ORDER {ship} '{k}'")
                if (x.get("kind"), x.get("text")) != (y.get("kind"), y.get("text")):
                    print("    reply old:", x.get("kind"), (x.get("text") or x.get("error") or "")[:500])
                    print("    reply new:", y.get("kind"), (y.get("text") or y.get("error") or "")[:500])
                la = [tuple(l) for l in x.get("lines", [])]
                lb = [tuple(l) for l in y.get("lines", [])]
                for l in la:
                    if l not in lb:
                        print("    - ", l)
                for l in lb:
                    if l not in la:
                        print("    + ", l)
    print(f"TOTAL served items {n_served}, differing {d_served}; orders {n_orders}, differing {d_orders}")


if __name__ == "__main__":
    main(sys.argv[1:])
