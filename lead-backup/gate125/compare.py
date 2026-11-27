"""Gate comparer: OLD beside NEW records from run.py, every differing line classed.

    python3 -I <probes>/gate/compare.py OLD.jsonl NEW.jsonl [--rules RULES.py] [--show N] [--json OUT]

For each case (matched by id): the log lines are aligned (difflib on tick, kind, severity, text);
each line only in OLD ("-") or only in NEW ("+"), and each line whose severity alone moved ("~"),
is classed by RULES (a .py defining `classify(kind, sev, text, side) -> label`; the default
below is package 127's). Lines after the first tick where the ship's physical state hash differs
are counted apart as "post-divergence". Prints per case: first state divergence, end-state
differences, differing replies, and counts by (label, side, kind, severity); then totals.
UNDECLARED lines are always printed in full.
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from collections import Counter

WAIT_RE = re.compile(r"'[^']*' will follow '[^']*', which the hands are still at\.")


def classify(kind, sev, text, side):
    t = text
    if kind == "evolution.waiting" and (
        "will follow" in t or "will not come in till she pays off" in t or "waits for the anchor" in t
    ):
        return "R1-wait"
    if "the watch on deck has" in t and "waits for the watch to be relieved" in t:
        return "R9-few"
    if kind in ("ship.filled_away", "ship.way") or t.startswith(("Filled away", "Braced full on", "Her sheets drawn")):
        return "R3-fill"
    if "Belayed setting" in t or (kind == "work.belayed" and "setting" in t):
        return "R4-belay"
    if kind == "strain.warning" and re.search(r"drum-tight|bending like|stranding|will carry", t):
        return "R7-dire"
    if "griped fast" in t or "The boats are out and towing astern" in t or t.endswith("the ship is clear.") or t == "The ship is clear.":
        return "R13-boats"
    if re.search(r"no hand aloft|Stations for making sail|Cast off the gaskets|Lay aloft, sail-loosers|Hoist away the|Let fall! Sheet home|ready-men aloft|Man the bars; heave round", t):
        return "R8-cast"
    return "UNDECLARED"


DIVERGING = ("R4-belay",)


def pair_class(old, new):
    """A replaced pair (old line, new line at the same tick and kind): words-only classes."""
    ot, nt = old[3], new[3]
    if "Belayed setting" in nt and "Belayed setting" not in ot:
        return "R4-belay"
    if WAIT_RE.sub("", ot).replace("  ", " ").strip().rstrip(":").strip() == nt.rstrip(":").strip():
        return "R1-trim"
    if WAIT_RE.sub("", ot).strip() == WAIT_RE.sub("", nt).strip() and ot != nt:
        return "R1-trim"
    return None


def label_of(e):
    return classify(e[1], e[2], e[3], "")


def load(path):
    out = {}
    for line in open(path):
        r = json.loads(line)
        out[r["id"]] = r
    return out


def first_div(a, b):
    ha = {t: h for t, h, _ in a["hashes"]}
    for t, h, sig in b["hashes"]:
        if t in ha and ha[t] != h:
            return t
    return None


def compare_case(a, b, cls, show):
    rep = {"id": a["id"], "errors": [a["error"], b["error"]], "div": first_div(a, b), "counts": Counter(),
           "undeclared": [], "end_diff": {}, "replies": [], "lines": [len(a["events"]), len(b["events"])]}
    div = rep["div"]
    # a line of a rule that changes what she does (DIVERGING) moves the divergence point to it
    r4 = [e[0] for e in b["events"] if cls(e[1], e[2], e[3], "+") in DIVERGING]
    if r4 and (div is None or min(r4) < div):
        div = rep["div"] = min(r4)
        rep["div_by"] = "R4"
    ea = [tuple(e[:4]) for e in a["events"]]
    eb = [tuple(e[:4]) for e in b["events"]]
    sm = difflib.SequenceMatcher(None, ea, eb, autojunk=False)
    diffs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        olds, news = ea[i1:i2], eb[j1:j2]
        used_new = set()
        for o in olds:
            # severity alone moved?
            m = next((k for k, n in enumerate(news) if k not in used_new and n[0] == o[0] and n[1] == o[1] and n[3] == o[3]), None)
            if m is not None:
                used_new.add(m)
                diffs.append(("~", o, news[m]))
                continue
            m = next((k for k, n in enumerate(news) if k not in used_new and n[0] == o[0] and n[1] == o[1] and pair_class(o, n)), None)
            if m is not None:
                used_new.add(m)
                diffs.append(("r", o, news[m]))
                continue
            diffs.append(("-", o, None))
        for k, n in enumerate(news):
            if k not in used_new:
                diffs.append(("+", None, n))
    for side, o, n in diffs:
        e = n if n is not None else o
        post = div is not None and (e[0] > div or (rep.get("div_by") and e[0] >= div - 1))
        if post and side in "+-" and cls(e[1], e[2], e[3], side) in DIVERGING:
            post = False  # the diverging rule's own line is counted as itself
        if side == "~":
            label = cls(o[1], o[2], o[3], "~")
            key = (("post:" if post else "") + label, f"~{o[2]}>{n[2]}", o[1])
        elif side == "r":
            label = pair_class(o, n)
            key = (("post:" if post else "") + label, f"r{o[2]}>{n[2]}", o[1])
        else:
            label = cls(e[1], e[2], e[3], side)
            key = (("post:" if post else "") + label, side + e[2], e[1])
        rep["counts"][key] += 1
        if label == "UNDECLARED" and not post:
            rep["undeclared"].append((side, o, n))
    ae, be = a.get("end") or {}, b.get("end") or {}
    for k in ("tick", "u", "heading", "x", "y", "carried_away", "parted", "blown_out", "phys"):
        if ae.get(k) != be.get(k):
            rep["end_diff"][k] = (ae.get(k), be.get(k))
    sd = {s: (ae.get("sails", {}).get(s), be.get("sails", {}).get(s)) for s in set(ae.get("sails", {})) | set(be.get("sails", {}))}
    sd = {s: v for s, v in sd.items() if v[0] != v[1]}
    if sd:
        rep["end_diff"]["sails"] = sd
    ra, rb = a["replies"], b["replies"]
    for x, y in zip(ra, rb):
        if x != y:
            rep["replies"].append((x, y))
    return rep


def main(argv):
    A, B = load(argv[0]), load(argv[1])
    cls = classify
    if "--rules" in argv:
        ns = {}
        exec(open(argv[argv.index("--rules") + 1]).read(), ns)
        cls = ns["classify"]
    show = int(argv[argv.index("--show") + 1]) if "--show" in argv else 0
    total = Counter()
    reports = []
    for cid in sorted(set(A) & set(B)):
        r = compare_case(A[cid], B[cid], cls, show)
        reports.append(r)
        total.update(r["counts"])
        quiet = "--quiet" in argv
        if quiet and not r["undeclared"] and not r["end_diff"] and not any(r["errors"]):
            continue
        print(f"== {cid}: lines {r['lines'][0]}->{r['lines'][1]}; first state divergence: {r['div']}")
        for e in r["errors"]:
            if e:
                print("  ERROR:", e.strip().splitlines()[-1])
        if r["end_diff"]:
            print("  END DIFF:", json.dumps(r["end_diff"])[:1500])
        if not quiet:
            for k, v in sorted(r["counts"].items()):
                print(f"  {v:4d}  {k[0]:18s} {k[1]:20s} {k[2]}")
            for x, y in r["replies"][:show or 5]:
                print("  REPLY old:", x[1:], "\n        new:", y[1:])
        for side, o, n in r["undeclared"][: max(show, 30)]:
            print("  UNDECLARED", side, o, "->", n)
    print("== TOTAL over", len(reports), "cases")
    for k, v in sorted(total.items()):
        print(f"  {v:5d}  {k[0]:18s} {k[1]:20s} {k[2]}")
    print("cases with state divergence:", sum(1 for r in reports if r["div"] is not None or r["end_diff"].get("phys")))
    if "--json" in argv:
        json.dump([{**r, "counts": [[list(k), v] for k, v in r["counts"].items()]} for r in reports],
                  open(argv[argv.index("--json") + 1], "w"), default=str)


if __name__ == "__main__":
    main(sys.argv[1:])
