"""Condensed, optionally sliced, merged timeline from a FreeSail save + checkpoint (read-only).

usage: condense.py SAVE.json OUT_FILE LABEL [START_TICK END_TICK]

Leaves out chatty ROUTINE-severity kinds, and collapses long runs of the same kind.
"""
import collections
import json
import os
import sys

from freesail import units
from freesail.core.replay import read_checkpoint

save_path, out_file, label = sys.argv[1], sys.argv[2], sys.argv[3]
lo = int(sys.argv[4]) if len(sys.argv) > 4 else 0
hi = int(sys.argv[5]) if len(sys.argv) > 5 else 10**12

DROP = {
    "evolution.started", "evolution.step", "ship.leeway", "wind.gust", "clock.bell",
    "agent.stood_by", "sail.trimmed", "sail.filled", "log.read", "helm.steady",
    "driver.eased",
}
RUN_KEEP_HEAD, RUN_KEEP_TAIL, RUN_MIN = 3, 1, 7

d = json.load(open(save_path, encoding="utf-8"))
header, world = read_checkpoint(os.path.splitext(save_path)[0] + ".checkpoint")
log = world.log.all()
MARK = {"routine": " ", "notable": "*", "urgent": "!"}

rows = []  # (tick, order, kindkey, text)
note_ticks = collections.defaultdict(list)
dropped = collections.Counter()
for i, e in enumerate(log):
    if not (lo <= e.tick <= hi):
        continue
    routine = e.severity.value == "routine"
    if routine and e.kind in DROP:
        dropped[e.kind] += 1
        continue
    if routine and e.kind == "order.accepted" and e.actor.startswith("standing order"):
        dropped["order.accepted (routine, by a standing order)"] += 1
        continue
    if e.kind == "order.accepted" and e.text.lower().startswith("order: tell the "):
        dropped["order.accepted (the captain's 'tell the ...', duplicated by the agent.told line)"] += 1
        continue
    if e.kind == "agent.note":
        note_ticks[e.tick].append(e.text)
    text = e.text
    if e.kind == "agent.handover" and len(text) > 160:
        text = text[:160] + " [... the whole note is in the '>>' handover_note / hand_over call at or just before this tick]"
    e_text = text
    stamp = units.time_stamp(e.ship_time)
    rows.append(
        (e.tick, 0, i, e.kind,
         f"{e.tick:>7} | {e.ship_time.strftime('%d %b')} | {MARK[e.severity.value]} {stamp} | {e.kind} | {e.actor} | {e_text}")
    )
j = 0
for a in d.get("agents", []):
    name = a["station"].get("name")
    for t in a["transcript"]:
        tick = t.get("tick")
        if not (lo <= tick <= hi):
            continue
        if "reply" in t:
            r = t["reply"]
            parts = [f"CALL {c.get('name')}({json.dumps(c.get('args'), ensure_ascii=False)})" for c in r.get("calls", [])]
            if r.get("text"):
                parts.append(f"TEXT: {r['text']}")
            if not parts:
                parts.append(f"RAW: {str(r.get('raw'))[:1200]}")
            line = " ;; ".join(parts)
            if not r.get("calls") and r.get("text"):
                head = r["text"][:60]
                if any(head in n for n in note_ticks.get(tick, [])):
                    dropped[">> spoken-text-only replies (duplicated by the agent.note log line)"] += 1
                    continue
        else:
            line = f"DOOR-EVENT by={t.get('by')} door={t.get('door')} reason={t.get('reason')}"
        j += 1
        rows.append((tick, 1, j, ">>", f"{tick:>7} | >> [{name}] {line}"))
rows.sort(key=lambda r: (r[0], r[1], r[2]))

# collapse runs of the same kind
out = []
i = 0
collapsed = collections.Counter()
while i < len(rows):
    k = rows[i][3]
    jx = i
    while jx < len(rows) and rows[jx][3] == k:
        jx += 1
    run = rows[i:jx]
    if k != ">>" and len(run) >= RUN_MIN:
        out.extend(r[4] for r in run[:RUN_KEEP_HEAD])
        mid = run[RUN_KEEP_HEAD:len(run) - RUN_KEEP_TAIL]
        out.append(
            f"        [... {len(mid)} more consecutive '{k}' lines left out here, ticks {mid[0][0]} to {mid[-1][0]} ...]"
        )
        collapsed[k] += len(mid)
        out.extend(r[4] for r in run[len(run) - RUN_KEEP_TAIL:])
    else:
        out.extend(r[4] for r in run)
    i = jx

with open(out_file, "w", encoding="utf-8") as f:
    f.write(f"# CONDENSED TIMELINE of {label}, ticks {lo} to {min(hi, d['end_tick'])} (the game ran to tick {d['end_tick']}; a tick is one second of ship's time).\n")
    f.write("# The ship's log merged with what each model at a station sent (lines with '>>': its tool calls and spoken text; tool RESULTS are not stored in saves).\n")
    f.write("# Log columns: tick | day | mark (' ' routine, '*' notable, '!' urgent) ship-time | kind | actor | text\n")
    f.write(f"# ROUTINE-severity lines of these chatty kinds are LEFT OUT (counts): {dict(dropped)}\n")
    f.write(f"# Long runs of one kind are collapsed to head+tail with a '[... N more ...]' marker (counts left out): {dict(collapsed)}\n")
    f.write("# The complete log is in the .log-full.txt beside the session's other dumps; grep it by tick or kind for anything left out.\n")
    for line in out:
        f.write(line + "\n")
print(label, lo, hi, "lines", len(out), "bytes", os.path.getsize(out_file), "dropped", sum(dropped.values()), "collapsed", sum(collapsed.values()))
