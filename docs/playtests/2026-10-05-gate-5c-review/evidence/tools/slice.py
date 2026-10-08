import sys
# usage: slice.py SESSION LO HI [kind,kind,...|ALL] [maxchars]
s, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
kinds = None if len(sys.argv) < 5 or sys.argv[4] == "ALL" else set(sys.argv[4].split(","))
mx = int(sys.argv[5]) if len(sys.argv) > 5 else 700
import os
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sessions", s, s + ".log-full.txt")
for line in open(base, encoding="utf-8"):
    if line.startswith("#"):
        continue
    p = line.rstrip("\n").split(" | ", 5)
    if len(p) < 6:
        continue
    t = int(p[0])
    if t < lo or t > hi:
        continue
    if kinds and p[3] not in kinds:
        continue
    out = f"{p[0].strip()} {p[2]} [{p[3]}] {p[4]}: {p[5]}"
    print(out[:mx])
