# Planting the faults: the task given to each runner

Read `READERS.md` beside this file first: its rules on what may not be opened (nothing
under `docs/dev/`, `docs/design/`, `docs/playtests/`, `docs/gates/`, nor the sealed notes)
bind you too. Its rule against running tests does **not** bind you: running tests is your
work, in your scratch copy and nowhere else.

**What this is.** The readers of the test suite claimed, of named tests, that each is
"built not to fail": that the behaviour the test's name promises could be broken and the
test would still pass. A claim is not a finding until it is tried. You try them: plant the
fault in a scratch copy of the code, run the test, and see. A reader who was wrong is as
useful to the review as one who was right; report what happened, not what was predicted.

**Where you work.** Your task names a scratch copy, a directory under the session's
scratchpad (`.../scratchpad/m/N`). It is a copy of the tree at the commit under review
(504a250): `freesail/`, `tests/`, `tools/`, `client/` and `data/` are real copies you may
edit; `data/charts` and `docs` are links to a shared copy and are **never** edited. The
pristine copy is `.../scratchpad/mut` (never edited: you restore files from it).
**Nothing in `/home/user/FreeSail` is edited, ever,** except the one evidence file your
task names. Run everything from inside your scratch copy, as:

    cd <your scratch copy> && timeout 900 python3 -m pytest -q -p no:cacheprovider -x "<node id>" 2>&1 | tail -15

(`python3 -m pytest` run there imports the scratch copy's `freesail`. A test chosen by its
node id runs whatever its tier. Do not pass `-n`: one process at a time, because three
other runners share this machine's four cores. Never run a whole test file of more than
a few seconds or the whole suite.)

**For each fault** in the `## Faults to plant` sections of the evidence files your task
names (those under the readers' heading (b), and those the reader says "no test would
catch"):

1. **Baseline.** Run the named test unmodified. If it does not pass before any fault is
   planted, record that (it is a finding of its own) and go on.
2. **Plant.** Make the edit the reader describes. Line numbers are of the commit under
   review, which your copy is. If the reader's description is loose, plant the fault that
   best breaks the behaviour the test's name promises, and write down exactly what you
   changed (a unified diff of a few lines: `diff -u <pristine file> <your file>`).
   Confirm the fault is live where you can: a one-line python check that the behaviour
   changed, or a second test nearby that fails. A fault that changes nothing proves
   nothing.
3. **Run** the named test (and, for a "no test would catch it" fault: grep the tests for
   the function, the constant or the log kind the fault touches and run up to five of the
   likeliest tests by node id; say which).
4. **Record** the result: **SURVIVED** (the test passed with the game broken: the reader's
   claim stands), **KILLED** (the test failed: the claim is refuted; quote the assertion
   that caught it), or **NOT RUN** (say why: the test needs a browser, takes over fifteen
   minutes, the edit could not be made as described).
5. **Restore** the file from the pristine copy (`cp .../scratchpad/mut/<path> <path>`)
   and check with `diff -r -q` on `freesail/` and `data/` (excluding `charts`) that your
   copy is pristine again before the next fault.

Keep to a budget: at most fifteen minutes of running per fault; if a test's fixture sails
for longer, mark it NOT RUN with the reason. Work through the faults in order and write
your evidence file as you go (append each fault's row as it is done), so that a stop
loses nothing.

**Your evidence file** has, at its head, a table: number, the test (file::name), the
fault in a few words, baseline, result (SURVIVED / KILLED / NOT RUN), seconds the run
took. Then one short section per fault with the diff and the tail of the test's output.
End with a count (how many survived, how many were killed, how many not run) and, in two
or three sentences, what the survivals have in common.

Your reply to the reviewer: at most 300 words: the counts, the survivals that matter most
to a player, and any claim of a reader's that was refuted.
