"""Gate mutant runner: apply each mutant to a scratch copy, run its tests, restore.

    python3 -I <probes>/gate/mutate.py MUTANTS.py PRISTINE_TREE SCRATCH_TREE OUT.txt [--only M01,M02] [-n 4] [--slow]

MUTANTS.py defines MUTANTS = [(id, file, old_str, new_str, [test files or node ids]), ...].
Each mutant: the file is restored from PRISTINE_TREE, old_str (which must occur exactly once)
replaced, the tests run in SCRATCH_TREE (pytest -n N -q -p no:cacheprovider -o addopts=""),
and the file restored. A mutant is KILLED if any test fails or errors, SURVIVED if all pass.
"""

import os
import re
import shutil
import subprocess
import sys


def main(argv):
    ns = {}
    exec(open(argv[0]).read(), ns)
    pristine, scratch, out = argv[1], argv[2], argv[3]
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    n = argv[argv.index("-n") + 1] if "-n" in argv else "4"
    slow = ["--slow"] if "--slow" in argv else []
    with open(out, "a") as f:
        for mid, path, old, new, tests in ns["MUTANTS"]:
            if only and not any(mid.startswith(o) for o in only):
                continue
            src = os.path.join(pristine, path)
            dst = os.path.join(scratch, path)
            text = open(src).read()
            if text.count(old) != 1:
                f.write(f"{mid}: NOT APPLIED (old string found {text.count(old)} times)\n")
                f.flush()
                continue
            open(dst, "w").write(text.replace(old, new))
            try:
                cmd = [sys.executable, "-P", "-m", "pytest", "-n", n, "-q", "-p", "no:cacheprovider",
                       "-o", "addopts=", "-x", *slow, *tests]
                env = dict(os.environ, PYTHONPATH=scratch)
                r = subprocess.run(cmd, cwd=scratch, env=env, capture_output=True, text=True, timeout=3600)
                tail = [l for l in r.stdout.splitlines() if re.search(r"passed|failed|error", l)][-1:]
                failed = [l for l in r.stdout.splitlines() if l.startswith(("FAILED", "ERROR"))]
                verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
                f.write(f"{mid}: {verdict} | {' '.join(tail)}\n")
                for l in failed[:8]:
                    f.write(f"    {l[:220]}\n")
                f.flush()
            finally:
                shutil.copyfile(src, dst)


if __name__ == "__main__":
    main(sys.argv[1:])
