# Brief: the review's second edition, for the repository's session

Written 2026-10-08 by the review's lead, for the owner to read before it is given to
anyone. Revised the same day at his word: the new report keeps as much of the first as it
can, put in order and brought up to date, and is not cut down to a summary.

It is two briefs with one set of rules. **Part A** is for an auditor, who works in the
code. **Part B** is for an editor, who works in the report. Each is a reviewer who has seen
none of this work, and each is given only its own part, the background and the rules.

## Background, for both

FreeSail's gate 5c was cut as the folder `D:\Projects\FreeSail\FreeSail-gate-m5c`. Since
then a week of work has been done beside it, with no commits, in
`D:\Projects\FreeSail\FreeSail-gate-m5c-c`: a provisional update (m5c-b), four packages
(37d, 37e, 37f, 37g, the last in two passes), ten playtests reviewed, and a number of
rulings by the owner. The record of it is a review report,
`docs\playtests\2026-10-05-gate-5c-review\report.md` in the build folder: about 3,000
lines and 39,000 words, written in three layers (the first review on 5 October; a game
played on the build on the 6th; a game played on it last night), with a status block at
the top that was added to after each step. It was never meant to be read cold, and much
of what it recommends has since been built, ruled on or overtaken.

Later today the owner takes the work to the session that keeps the game's repository. That
session knows the game and its code well and has seen **nothing since m5c was cut**. It
has to understand what was found, what was decided and what was built, and decide package
by package whether to take the work as it stands or change it. Then the owner closes the
gate (the naval cruise among other things) and the project moves to the next milestone.
The owner will read the new report too; he designed the game and is not a programmer.

**Where things are.**

- **The build**: `FreeSail-gate-m5c-c`. Its `CHANGES-m5c-c.md` says what each package
  claims. `docs\dev\M5-WorkPackages.md`, from "Follow-ups from gate 5c's first playtests,
  sorted" to "Integration", holds the plan as ruled and the four briefs.
- **The gate as cut**: `FreeSail-gate-m5c`, the baseline.
- **m5c-b**: `FreeSail-gate-m5c-b`, with `CHANGES-m5c-b.md` and `m5c-b.diff`.
- **The build after each package**: the lead's snapshots `m5cc-at-37d`, `m5cc-at-37e`,
  `m5cc-at-37f` and `m5cc-at-37g` (the last is before 37g's second pass) under
  `C:\Users\frenc\AppData\Local\Temp\claude\D--Projects-FreeSail-FreeSail-gate-m5c\ec2795ad-6930-4b13-b530-df0ee191d2dc\scratchpad\`.
  They leave out caches and any folder named `saves`. Read only. Some paths in them are
  longer than Python will open without the long-path prefix; a file that seems missing
  there may only be that.
- **The review folder**: `docs\playtests\2026-10-05-gate-5c-review\` in the build folder:
  `report.md`, `evidence\` (measurements, the readers' reports, the scripts), `drafts\`.
- **The game's own documents**: `docs\DesignProposal.md` (its decisions log),
  `docs\TechnicalSpec-M5.md`, `docs\gates\gate-m5c.md`, `docs\agents\` (the consent brief,
  its commitments in `README.md`, the records under `consent\`), `docs\dev\TuningNotes.md`.

## Part A: the auditor

**What is wanted.** A true account of the build as it stands today, checked in the code
and the tests and not taken from anyone's description of it. You are told no verdicts
here on purpose: the lead checked every package and may be inclined to think each did
what it was asked. The changes file, the briefs and the review, its section 11 included,
are claims.

**What you write**: one file, `handover-audit.md`, in the review folder. Four parts.

1. **The ledger.** One table with a row for every recommendation in the review (its
   sections 8, 10.6 and 11.6), every ruling in its section 9 and at the end of 10.6, every
   numbered item of the four packages' briefs, and every "left undone" in the changes
   file. For each: where it came from; its state (**built**, **partly built** and what is
   missing, **not built**, **overtaken by a ruling** and which, or **could not tell** and
   why); and what you looked at to say so (a file and function, a test by name, a line of
   a log).
2. **The gate.** `docs\gates\gate-m5c.md` item by item as the build stands today. Every
   test marked as an expected failure, and why it is. What closing the gate needs. The
   naval cruise wants particular care: find exactly what stops it, and where in the code.
3. **What changed in the tree**, from comparing the two folders yourself: by area of the
   code, new and removed files, data and fixtures, documents, and which package made each
   change (the snapshots tell you). The consent records made in play. What belongs to this
   folder alone and should not be carried into a repository (the owner's saves and notes,
   the build's own name, and whatever else you find).
4. **Where the claims and the code part company**, most serious first; and your advice for
   each package: take as it is, take with a named change, or hold. It is advice; the owner
   and the repository's session decide.

**How to work.** For each row find the code and a test. Say "not checked" where you did
not look; a guess is worse. Run what helps: single tests, small read-only scripts of your
own, and the whole suite once near the end, so that its result is stated first hand
(`py -m pytest -n 4 --slow -p no:cacheprovider` from the build folder; about twelve
minutes; when the lead last ran it, it ended with 2,981 passed and 9 expected failures),
and `py -m ruff check .`. If time runs short, parts 2, 3 and 4 come before the ledger's
long tail.

## Part B: the editor

**What is wanted.** A second edition of the review report: the same substance, in an
order a cold reader can follow, true of today. The first edition is the record and is not
touched. The second is what the repository's session will read.

**Keep.** As much of the detail and the important content as you can. Every finding with
its evidence: the ticks, the ship's times, the quotations from the logs, the figures and
the tables of measurements. The owner's notes and his answers in his own words. The
account of each game. What each package did and what it measured. The plan. If it comes
to 2,500 lines, that is what it comes to. Losing lines is fine where they are repetition
or are no longer true; it is not the aim.

**Change.**

- **The order.** The first edition is in the order it was written. Arrange the second by
  what a reader needs: what this is and how to read it; what happened, by date, in a page;
  the owner's rulings in one table; the games; then the findings **by subject**, each
  followed through from start to finish. The first edition spreads one subject (the
  reckoning, say, or the anchors, or the officer's station) over its sections 5, 7, 8, 9,
  10 and 11; bring each together.
- **The status.** For each finding say what was found and on what evidence; what the
  owner ruled; what was built, in which package and where; how it did in the games played
  afterwards; and what is left. A recommendation that has been built becomes an account of
  what was built. One that was ruled otherwise says so in a line. One overtaken by a later
  finding gives way to the later finding.
- **What is no longer needed.** The status block's running history, cross-references to
  "the next package" that is now built, questions that have been answered (keep the
  answers), and the review of the m5c-b diff at its present length, since m5c-b is inside
  the build (keep what it found that still matters).
- **Words coined in this work.** A short list near the top of the terms a reader who left
  at m5c will not know (the build folders and their names, the packages by number and
  name, "the account" and "the doubt", "the one rule", "the general authority", "the lean
  brief", a seating, and so on).

**Do not.** Invent anything. Alter a figure, a tick or a quotation. Change the owner's
words. Soften a finding, or the places where the review says it was itself wrong. Drop a
finding without saying so.

**What you write.**

- `report-2.md` in the review folder: the second edition. Leave three places for the
  auditor's work, each a heading with one line saying it is to come: the gate as the build
  stands; folding the work in, with advice by package; and the ledger, as an appendix.
- At its end, two short appendices of your own: **where each part of the first edition
  went** (its sections and subsections against yours), and **what the first edition had
  that this one does not**, with the reason for each.

**How to work.**

- Read the whole first edition before you write. Then make the plan of the second and the
  table of where everything goes, and write from that.
- Write it part by part into files in your scratch folder and join them at the end. Do not
  try to hold or write it in one piece.
- When it is joined, check it against the first by script as well as by eye: every tick
  and time, every figure in a table and every quoted line of the first edition is either
  in the second or in your list of what was left out.
- **For the status of each thing**, use the changes file, the briefs, and the first
  edition's own status block and its sections 10 and 11, and keep a working list of every
  place where you state that something is built, partly built or open. The auditor's file
  will be sent to you when it is done. You then put its three parts in their places and go
  down your list, correcting whatever the audit found otherwise. Until then, do not check
  the code yourself; that is the auditor's work.
- Write as the first edition does: plain words, short sentences, British spelling, dates
  and ship's times given, no dashes used as punctuation.

## Rules, for both

- You change nothing in either folder except to add your own file. No code, test, data
  file or existing document is edited, and nothing is deleted. `report.md` is not edited.
  `saves\`, `m5c-c Notes.txt` and `.mcp.json` are the owner's. No record under
  `docs\agents\consent\` is touched.
- No git command of any kind, anywhere. Never open or touch
  `D:\Projects\FreeSail\FreeSail-repo` or any `FreeSail-claude-*` folder.
- Never call a tool whose name begins `mcp__freesail__`: it is a live bridge into the
  owner's game. Seat no model, answer no consent question, start no server on port 8000.
- Scratch files go in a folder of your own under the scratchpad path above
  (`handover-audit\` or `handover-edition\`), never in the tree. Set `PYTHONPATH` to the
  build folder, `PYTHONUTF8=1` and `PYTHONDONTWRITEBYTECODE=1` on every command; four test
  workers at most; one suite at a time; leave no `.pytest_cache` and no process running.
- Spawn no agents. Install nothing.

## What each hands back

A short report to the lead, in plain words.

- **The auditor**: what it wrote; the suite's last line and the linter's; every place where
  the code does not bear out the changes file, a brief or the review, most serious first;
  what it could not check and why; anything the owner should decide before the work is
  folded in.
- **The editor**: the second edition's plan and length; what was left out and why; anything
  in the first edition it found unclear, contradictory or unsupported; and, after the
  audit is folded in, every statement of status it changed.
