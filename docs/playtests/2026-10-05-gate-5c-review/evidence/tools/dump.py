"""Read-only dump of a FreeSail save + checkpoint into readable text files (in the scratchpad).

usage: dump.py SAVE.json OUT_DIR LABEL [comma,separated,kinds,to,drop,from,timeline]
"""
import collections
import json
import os
import sys

from freesail import units
from freesail.core.replay import read_checkpoint

save_path, out_dir, label = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out_dir, exist_ok=True)
d = json.load(open(save_path, encoding="utf-8"))
cp = os.path.splitext(save_path)[0] + ".checkpoint"
header, world = read_checkpoint(cp)
assert header["end_tick"] == d["end_tick"], (header, d["end_tick"])
log = world.log.all()
MARK = {"routine": " ", "notable": "*", "urgent": "!"}


def stamp(e):
    return units.time_stamp(e.ship_time)


def day(e):
    return e.ship_time.strftime("%d %b")


# 1. full log
with open(os.path.join(out_dir, label + ".log-full.txt"), "w", encoding="utf-8") as f:
    f.write(
        f"# FULL LOG of {label}: {len(log)} events, end tick {d['end_tick']}. "
        "Columns: tick | day | mark(' ' routine, '*' notable, '!' urgent) ship-time | kind | actor | text\n"
    )
    for e in log:
        f.write(
            f"{e.tick:>7} | {day(e)} | {MARK[e.severity.value]} {stamp(e)} | {e.kind} | {e.actor} | {e.text}\n"
        )

kinds = collections.Counter(e.kind for e in log)
sev = collections.Counter(e.severity.value for e in log)

# 2. transcripts
agents = d.get("agents", [])
tx_by_tick = collections.defaultdict(list)
with open(os.path.join(out_dir, label + ".transcripts.txt"), "w", encoding="utf-8") as f:
    f.write(
        f"# STATION TRANSCRIPTS of {label}. Each entry is what the MODEL sent (its tool calls and any "
        "spoken text); tool results are not stored in a save.\n"
    )
    for a in agents:
        st = a["station"]
        f.write("\n" + "=" * 100 + "\n")
        f.write(
            f"STATION: {st.get('name')} | model: {a.get('model_name')} | door: {a.get('door')} | "
            f"seatings: {a.get('seatings')} | budget_tokens: {a.get('budget_tokens')} | "
            f"stationed_tick: {a.get('stationed_tick')} | final state: {a.get('state_words')} | "
            f"deck: {a.get('deck')} | stand_by_ends_turn: {a.get('stand_by_ends_turn')}\n"
        )
        f.write(
            f"authority: {st.get('authority')} | policy: {json.dumps(st.get('policy'))} | "
            f"patience_s: {st.get('patience_s')}\n"
        )
        f.write(f"session_kind: {a.get('session_kind')}\ndoor_note: {a.get('door_note')}\n")
        f.write("STATION BRIEF:\n" + str(st.get("brief")) + "\n")
        for k in st:
            if k not in ("name", "authority", "policy", "patience_s", "brief"):
                f.write(f"station.{k}: {json.dumps(st[k], ensure_ascii=False)[:3000]}\n")
        f.write("-" * 100 + "\n")
        for i, t in enumerate(a["transcript"]):
            tick = t.get("tick")
            if "reply" in t:
                r = t["reply"]
                parts = []
                for c in r.get("calls", []):
                    parts.append(f"CALL {c.get('name')}({json.dumps(c.get('args'), ensure_ascii=False)})")
                if r.get("text"):
                    parts.append(f"TEXT: {r['text']}")
                if not parts:
                    parts.append(f"RAW: {str(r.get('raw'))[:1500]}")
                line = " ;; ".join(parts)
            else:
                line = f"DOOR-EVENT by={t.get('by')} door={t.get('door')} reason={t.get('reason')}"
            f.write(f"[{i:>4}] tick {tick:>7} (after {t.get('after_orders')} orders) {line}\n")
            tx_by_tick[tick].append((st.get("name"), line))

# 3. agent journals
with open(os.path.join(out_dir, label + ".agent-journals.txt"), "w", encoding="utf-8") as f:
    f.write(
        f"# AGENT JOURNALS of {label} (each station's own journal as the harness keeps it: its notes, "
        "stand-bys, deck events, handover notes)\n"
    )
    for name, entries in (d.get("agent_journals") or {}).items():
        f.write("\n" + "=" * 100 + f"\nJOURNAL OF: {name} ({len(entries)} entries)\n")
        for x in entries:
            f.write(f"{x.get('tick'):>7} | {x.get('stamp')} | {x.get('kind')} | {x.get('text')}\n")

# 4. inputs
with open(os.path.join(out_dir, label + ".inputs.txt"), "w", encoding="utf-8") as f:
    f.write(
        f"# INPUTS of {label}: every order in the order given (actor = who typed/submitted it), and driver lines\n"
    )
    for x in d.get("inputs", []):
        if "order" in x:
            f.write(f"{x['tick']:>7} | {x.get('actor')} | {x['order']}\n")
        else:
            ln = x.get("line", {})
            f.write(f"{x['tick']:>7} | DRIVER-LINE {ln.get('kind')} [{ln.get('severity')}] | {ln.get('text')}\n")

# 5. standing orders + scenario
with open(os.path.join(out_dir, label + ".standing-and-scenario.txt"), "w", encoding="utf-8") as f:
    f.write(f"# STANDING ORDERS at the end of {label}\n")
    for s in d.get("standing_orders", []):
        f.write(
            f"- given_tick {s.get('given_tick')} | fired {s.get('fired')} (last {s.get('last_fired_tick')}) | "
            f"belayed={s.get('belayed')} | by {s.get('given_by')} | {s.get('text')}\n"
        )
    f.write("\n# SCENARIO (as saved)\n")
    f.write(json.dumps(d.get("scenario", {}), ensure_ascii=False, indent=1)[:60000])
    f.write("\n\n# WORLD ORDERS\n" + json.dumps(d.get("world_orders"), ensure_ascii=False, indent=1)[:8000])

# 6. merged timeline: log events + model calls, minus very chatty routine kinds
DROP = set(sys.argv[4].split(",")) if len(sys.argv) > 4 and sys.argv[4] else set()
events_by_tick = collections.defaultdict(list)
for e in log:
    events_by_tick[e.tick].append(e)
ticks = sorted(set(events_by_tick) | set(tx_by_tick))
dropped = collections.Counter()
n = 0
with open(os.path.join(out_dir, label + ".timeline.txt"), "w", encoding="utf-8") as f:
    f.write(
        f"# TIMELINE of {label}: the ship's log merged with what each model sent (lines with '>>'), in tick order.\n"
    )
    f.write(
        "# Log columns: tick | day | mark(' ' routine, '*' notable, '!' urgent) ship-time | kind | actor | text."
        "   '>>' lines: tick | station | the model's tool call(s) / text.\n"
    )
    f.write(
        f"# Chatty ROUTINE-severity kinds LEFT OUT of this file (the .log-full.txt has them): {sorted(DROP)}\n"
    )
    for t in ticks:
        for e in events_by_tick.get(t, []):
            if e.kind in DROP and e.severity.value == "routine":
                dropped[e.kind] += 1
                continue
            f.write(
                f"{e.tick:>7} | {day(e)} | {MARK[e.severity.value]} {stamp(e)} | {e.kind} | {e.actor} | {e.text}\n"
            )
            n += 1
        for name, line in tx_by_tick.get(t, []):
            f.write(f"{t:>7} | >> [{name}] {line}\n")
            n += 1

# 7. summary
with open(os.path.join(out_dir, label + ".summary.txt"), "w", encoding="utf-8") as f:
    f.write(
        f"# SUMMARY of {label}\nsave: {save_path}\nscenario: {d['scenario'].get('name')} | "
        f"start {d['scenario'].get('start_time')} | ship {json.dumps(d.get('ship_ref'))} | seed {d.get('seed')}\n"
    )
    f.write(f"end_tick: {d['end_tick']} | log events: {len(log)} | severities: {dict(sev)}\n")
    f.write(f"first log time: {log[0].ship_time} | last log time: {log[-1].ship_time}\n")
    f.write(
        f"inputs: {len(d.get('inputs', []))} | journal (accepted orders): {len(d.get('journal', []))} | "
        f"standing orders: {len(d.get('standing_orders', []))}\n"
    )
    actors = collections.Counter(x.get("actor") for x in d.get("inputs", []) if "order" in x)
    f.write(f"orders by actor: {dict(actors)}\n")
    for a in agents:
        calls = collections.Counter()
        for t in a["transcript"]:
            if "reply" in t:
                for c in t["reply"].get("calls", []):
                    calls[c.get("name")] += 1
                if t["reply"].get("text") and not t["reply"].get("calls"):
                    calls["(spoken text only)"] += 1
            else:
                calls["(door event)"] += 1
        f.write(
            f"agent: {a['station'].get('name')} | {a.get('model_name')} | door {a.get('door')} | "
            f"seatings {a.get('seatings')} | transcript entries {len(a['transcript'])} | calls: {dict(calls)}\n"
        )
    f.write("\nlog kinds (count, of which notable/urgent):\n")
    nu = collections.Counter((e.kind, e.severity.value) for e in log)
    for k, v in kinds.most_common():
        f.write(f"{v:>7}  {k}   (notable {nu.get((k, 'notable'), 0)}, urgent {nu.get((k, 'urgent'), 0)})\n")
    f.write(f"\ntimeline lines written: {n}; dropped from timeline: {dict(dropped)}\n")
print(label, "events", len(log), "timeline lines", n, "dropped", sum(dropped.values()))
