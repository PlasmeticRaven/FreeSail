"""Cells of truth 7-779 b, reproduced: (ship, wind, seed, how) with how in old (run in the OLD
tree, no patches), trunk/instant/mine (NEW tree, by the test's own _spar_passage). Records the
measures plus the whole log of the passage for line-for-line comparison.

    cd <tree> && PYTHONPATH=$PWD python3 -P cell3.py OUT.jsonl HOWS [-j N]
"""
import json
import sys
import tempfile
import traceback
from multiprocessing import Pool
from pathlib import Path

INSTANT_CELLS = [("bilander", w) for w in ("12", "25", "12-heading", "20-38")] + [
    ("seventy-four", w) for w in ("12", "25", "20-38")]
OTHER_CELLS = [("merchant-brig", "20-38"), ("merchant-brig", "12-heading"), ("topsail-schooner", "25"),
               ("frigate-36", "20-38"), ("cutter", "25"), ("brig", "20-38"), ("seventy-four", "12-heading"), ("topsail-schooner", "20-38")]
SEEDS = (7, 8, 9, 3, 11)


def passage(ship, wind, seed, how):
    import importlib.util, os
    src = os.environ.get("NEW_TESTS")
    if src:
        spec = importlib.util.spec_from_file_location("t126new", src)
        T = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(T)
    else:
        import tests.test_mends_126 as T
    if how != "old":
        r = T._spar_passage(ship, wind, seed, how)
        w = r.pop("world")
    else:
        # the trunk itself: the same scenario and the same loss, nothing patched
        from freesail.physics import strain as ST
        from freesail.world.scenarios import begin, load_scenario, make_scenario_world
        lines = "\n".join(
            f"    - {{at: 1805-06-14T{at}, from_deg: {d}, knots: {k}"
            f"{', air_mass: neutral' if i == 0 else ''}}}"
            for i, (at, d, k) in enumerate(T.PASSAGE_WINDS[wind]))
        path = Path(tempfile.mkdtemp()) / "passage.yaml"
        path.write_text(T.PASSAGE.format(ship=ship, wind=lines, seed=seed), encoding="utf-8")
        sf = load_scenario(str(path))
        w = make_scenario_world(sf)
        begin(w, sf)
        w.run(600)
        s = w.ship
        ST._wreck_spar(s, ST.strain_state(s), s.spars[T.PASSAGE_SPARS[ship]], 2.0)
        n0 = len(w.log)
        start = T._from_falmouth_nm(w._position.lat_deg, w._position.lon_deg)
        astern = 0
        for _ in range(180):
            w.run(60)
            if float(s.dyn.u) < -0.05:
                astern += 1
        log = w.log[n0:]
        r = {"made_good": start - T._from_falmouth_nm(w._position.lat_deg, w._position.lon_deg),
             "astern": astern, "aback": sum(1 for e in log if e.kind == "ship.aback"),
             "brought_to": next((e.tick for e in log if e.kind == "ship.hove_to"), None)}
    r["events"] = [[e.tick, e.kind, e.severity.value, e.text] for e in w.log]
    return r


def run(job):
    ship, wind, seed, how = job
    try:
        r = passage(ship, wind, seed, how)
        err = None
    except Exception:
        r, err = {}, traceback.format_exc()[-2000:]
    return {"id": f"{ship}|{wind}|{seed}|{how}", "error": err, **r}


def main(argv):
    out, hows = argv[0], argv[1].split(",")
    jobs = int(argv[argv.index("-j") + 1]) if "-j" in argv else 1
    cells = INSTANT_CELLS + OTHER_CELLS
    first = [("bilander", "20-38"), ("seventy-four", "25")]
    inst = first + [c for c in INSTANT_CELLS if c not in first]
    work = [(s, w, seed, how) for (s, w) in inst for seed in (7, 3, 11) for how in hows]
    work += [(s, w, seed, how) for (s, w) in OTHER_CELLS for seed in (7, 11) for how in hows]
    import os
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["id"] for l in open(out)}
    work = [j for j in work if f"{j[0]}|{j[1]}|{j[2]}|{j[3]}" not in done]
    if "--four" in argv:  # the trunk stand-in against OLD, line for line, on four cell-seeds
        work = [(s, w, 7, how) for (s, w) in [("bilander", "20-38"), ("merchant-brig", "20-38"),
                                               ("seventy-four", "25"), ("cutter", "12-heading")] for how in hows]
    sys.path.insert(0, ".")
    with open(out, "a") as f, Pool(jobs) as pool:
        for rec in pool.imap_unordered(run, work):
            f.write(json.dumps(rec) + "\n")
            f.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
