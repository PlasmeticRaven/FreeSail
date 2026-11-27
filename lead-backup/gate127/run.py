"""Gate harness: drive worlds through scripted steps and record everything the log says.

Run from inside a tree (the tree under test is whatever is on PYTHONPATH):

    cd <tree> && PYTHONPATH=$PWD python3 -P <probes>/gate/run.py CASES.json OUT.jsonl [-j N]

CASES.json is a list of cases (or a .py file defining CASES, a list). A case:

    {"id": "brig-gale-1",
     "ship": "data/ships/brig.yaml",          # a ship file, with "scenario": Scenario kwargs
     "scenario": {"wind_from_deg": 0, "wind_speed_kn": 35, "gustiness": 0.3, ...},
     "scenario_file": "data/scenarios/x.yaml", # or a scenario file (its first orders given)
     "seed": 7,
     "hash_every": 60,                          # seconds between state hashes
     "steps": [["order", "set plain sail"], ["run", 600],
               ["wind", from_deg, knots],       # wind.follow at once
               ["ramp", from_deg, kn0, kn1, secs, step_s],
               ["py", "python with w in scope"],
               ["checkpoint", "path"], ["load_checkpoint", "path"]]}

Each output line is one case: id, events [tick, kind, severity, text, subject, turn_wait],
replies [tick, order, kind, text], hashes [tick, phys_hash, sails_sig], end (a state summary),
error (a traceback, or null). The phys hash covers the ship's motion, every part's primitive
fields (state, reefs, loads, condition, braces, ...), the strain state's records (not its new
`last_dire_s`) and, in a scenario, every vessel's position and heading.
"""

from __future__ import annotations

import hashlib
import json
import sys
import traceback
from enum import Enum
from multiprocessing import Pool


def _prim(v):
    if isinstance(v, Enum):
        return v.name
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, (int, str, bool)) or v is None:
        return v
    return None


def _fields(o):
    """An object's fields, its dataclass defaults counted (a checkpoint drops attributes that
    equal their class default from __dict__, so vars() alone reads differently after a load)."""
    import dataclasses
    import os

    if os.environ.get("GATE_HASH") == "vars":
        # the first gate-127 runs' hash (vars() alone), to compare with records made then
        return {k: v for k, v in sorted(vars(o).items())}
    names = set(vars(o))
    if dataclasses.is_dataclass(o):
        names |= {f.name for f in dataclasses.fields(o)}
    return {k: getattr(o, k, None) for k in sorted(names)}


def phys(w):
    s = w.ship
    out = []
    d = s.dyn
    import os

    if os.environ.get("GATE_HASH") == "vars":
        out.append(("dyn", [_prim(getattr(d, k)) for k in sorted(vars(d))]))  # the first runs' form
    else:
        out.append(("dyn", [(k, _prim(v)) for k, v in _fields(d).items()]))
    for pid in sorted(s.parts):
        p = s.parts[pid]
        out.append((pid, [(k, _prim(v)) for k, v in _fields(p).items() if _prim(v) is not None]))
    st = s.extra.get("strain")
    if st is not None:
        out.append(("strain", st.snapshot() if hasattr(st, "snapshot") else None))
        out.append(("strain.last", sorted((k, repr(v)) for k, v in st.last_warning_s.items())))
    try:
        vs = w.vessels.vessels
        items = vs.items() if isinstance(vs, dict) else ((getattr(v, "id", i), v) for i, v in enumerate(vs))
        for vid, v in sorted(items, key=lambda kv: str(kv[0])):
            pos = getattr(v, "position", None)
            out.append((str(vid), repr(getattr(pos, "lat_deg", pos)), repr(getattr(pos, "lon_deg", None)),
                        repr(getattr(v, "heading", None))))
    except Exception:
        pass
    return hashlib.sha256(json.dumps(out, default=str).encode()).hexdigest()[:16]


def sails_sig(w):
    return ";".join(f"{sid}={sl.state.name[:4]}{sl.reefs or ''}" for sid, sl in sorted(w.ship.sails.items()))


def end_summary(w):
    s = w.ship
    st = s.extra.get("strain")
    return {
        "tick": w.clock.tick,
        "u": s.dyn.u,
        "heading": s.dyn.heading,
        "x": s.dyn.x,
        "y": s.dyn.y,
        "sails": {sid: [sl.state.name, sl.reefs] for sid, sl in sorted(s.sails.items())},
        "spars": {sid: [sp.condition, sp.wrecked] for sid, sp in sorted(s.spars.items())},
        "carried_away": list(getattr(st, "carried_away", []) or []),
        "parted": list(getattr(st, "parted", []) or []),
        "blown_out": list(getattr(st, "blown_out", []) or []),
        "max_load_ratio": max(
            (p.load_kn / p.rating_kn for p in s.parts.values() if getattr(p, "rating_kn", 0)), default=0.0
        ),
        "running": [
            [i.evo.id, i.subject_id, bool(i.waiting)]
            for i in getattr(s.extra.get("evolutions"), "instances", [])
        ],
        "phys": phys(w),
    }


def make(case):
    if case.get("scenario_file"):
        from freesail.world.scenarios import begin, load_scenario, make_scenario_world

        sf = load_scenario(case["scenario_file"])
        w = make_scenario_world(sf, seed=case.get("seed"))
        begin(w, sf)
        return w
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    return make_world(case.get("seed", 7), case["ship"], Scenario(**case.get("scenario", {})))


def run_case(case):
    rec = {"id": case["id"], "events": [], "replies": [], "hashes": [], "end": None, "error": None}
    w = None
    try:
        from freesail import units

        w = make(case)
        if case.get("watcher"):
            # the scripted fake at the watcher's station (console's `--watcher fake`), every
            # sample's tick and reason recorded in rec["samples"]
            from freesail.agents import harness as H
            from freesail.ui.console import station_watcher

            rec["samples"] = []
            orig = H.Harness._sample

            def _sample(self, reason, stood_by=None, _o=orig):
                rec["samples"].append([self.world.clock.tick, reason])
                return _o(self, reason, stood_by)

            H.Harness._sample = _sample
            import freesail.ui.console as _con

            _con.replay_mod.save_to_file = lambda _w, p, *a, **k: p  # write nothing in the tree
            station_watcher(w, "fake")
        every = int(case.get("hash_every", 60))
        import os

        legacy = os.environ.get("GATE_HASH") == "vars"  # the first runs' schedule: 1, 1+every, ...
        state = {"next": 0 if legacy else (w.clock.tick // every + 1) * every}

        def advance(secs):
            left = int(secs)
            while left > 0:
                n = min(left, max(1, state["next"] - w.clock.tick))
                w.run(n)
                left -= n
                if w.clock.tick >= state["next"]:
                    rec["hashes"].append([w.clock.tick, phys(w), sails_sig(w)])
                    state["next"] = w.clock.tick + every if legacy else (w.clock.tick // every + 1) * every

        for step in case["steps"]:
            op = step[0]
            if op == "order":
                r = w.submit(step[1])
                rec["replies"].append([w.clock.tick, step[1], getattr(r, "kind", None), getattr(r, "text", str(r))])
            elif op == "run":
                advance(step[1])
            elif op == "wind":
                w.wind.follow(units.wrap_2pi(units.deg_to_rad(step[1])), units.knots_to_ms(step[2]))
            elif op == "ramp":
                _, frm, k0, k1, secs, dt = step
                n = max(1, int(secs // dt))
                for i in range(1, n + 1):
                    kn = k0 + (k1 - k0) * i / n
                    w.wind.follow(units.wrap_2pi(units.deg_to_rad(frm)), units.knots_to_ms(kn))
                    advance(dt)
            elif op == "py":
                exec(step[1], {"w": w, "units": units, "rec": rec})
            elif op == "checkpoint":
                from freesail.core.replay import write_checkpoint

                write_checkpoint(w, step[1])
            elif op == "load_checkpoint":
                from freesail.core.replay import read_checkpoint

                _, w = read_checkpoint(step[1])
                state["next"] = (w.clock.tick // every + 1) * every
            else:
                raise ValueError(op)
    except Exception:
        rec["error"] = traceback.format_exc()[-3000:]
    if w is not None:
        for e in w.log:
            rec["events"].append(
                [e.tick, e.kind, e.severity.value, e.text, e.subject, bool((e.data or {}).get("turn_wait"))]
            )
        try:
            rec["end"] = end_summary(w)
        except Exception:
            rec["error"] = (rec["error"] or "") + traceback.format_exc()[-1500:]
    return rec


def load_cases(path):
    if path.endswith(".py"):
        ns = {}
        exec(open(path).read(), ns)
        return ns["CASES"]
    return json.load(open(path))


def main(argv):
    cases_path, out_path = argv[0], argv[1]
    jobs = int(argv[argv.index("-j") + 1]) if "-j" in argv else 1
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    cases = load_cases(cases_path)
    if only:
        cases = [c for c in cases if any(c["id"].startswith(o) for o in only)]
    with open(out_path, "w") as f:
        if jobs > 1:
            with Pool(jobs) as pool:
                for rec in pool.imap_unordered(run_case, cases):
                    f.write(json.dumps(rec) + "\n")
                    f.flush()
        else:
            for c in cases:
                f.write(json.dumps(run_case(c)) + "\n")
                f.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
