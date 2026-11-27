import json, sys, difflib
A = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[1])}
B = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[2])}
for k in sorted(set(A) & set(B)):
    a, b = A[k], B[k]
    ea = [tuple(e[:4]) for e in a['events']]; eb = [tuple(e[:4]) for e in b['events']]
    same = ea == eb and a['hashes'] == b['hashes'] and a['end'] == b['end']
    if same:
        print(f"SAME  {k}"); continue
    hv = lambda r: next((e[0] for e in r['events'] if e[1] == 'ship.hove_to'), None)
    ref = lambda r: [e for e in r['events'] if e[1] in ('order.rejected', 'evolution.failed') and any(x in e[3] for x in ('lie a-try', 'heave to', 'bring her to', 'heaving to'))]
    print(f"DIFF  {k}: lines {len(ea)}->{len(eb)} brought to {hv(a)}->{hv(b)} bring-to refused/failed {len(ref(a))}->{len(ref(b))}")
    sm = difflib.SequenceMatcher(None, ea, eb, autojunk=False)
    n = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal': continue
        for e in ea[i1:i2][:3]: print('     -', e[0], e[1], e[3][:150])
        for e in eb[j1:j2][:3]: print('     +', e[0], e[1], e[3][:150])
        n += 1
        if n >= int(sys.argv[3] if len(sys.argv) > 3 else 2): break
