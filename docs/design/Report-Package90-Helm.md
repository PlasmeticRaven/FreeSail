# Report: package 90, A3, the helm's kind (2026-11-20)

The builder's report for step A3, built in a session of its own beside the engine track (the
lead's nudge 27). It is also the nudge to the coordinating session.

## The second pass: stop 2 built (the lead's nudge 31, 2026-11-20)

The lead allowed both stops. Stop 2 was the builder's to build; stop 1 is the coordinating
session's, at A3's merge. This section is the nudge for the second pass. The first pass's
sections follow it as they were reported, with marks where this pass supersedes them.

- **The commit: `5426600a0f0efa8d6dd108afd0ff2e44a5a47b40`** ("Package 90, A3: the captain's
  mend order from the one table"), on this step's own branch after the first pass's report
  (58b89c96). Four files:
  - `freesail/world/captains.py`;
  - `tests/test_known_truths.py`;
  - `tests/test_helm_kind.py`;
  - `docs/dev/TuningNotes.md`.
- **`freesail/world/captains.py`, as the first pass's §7 drafts it.** In `Captain._repairs`,
  `from freesail.evolutions.scripts import helm_words` beside the function's own import, and the
  order `wanted.append((helm_words(ship)["mend"], "steering by the relieving tackles"))`. There
  is no branch on the hull's kind.
  - With the reason's line (`_helm_first`), that is three lines of A3's in the file and no
    more: `git diff 8b8a982d -- freesail/world/captains.py` shows one line added and two
    changed, all outside the going-about rows.
  - Package 121's lines elsewhere in the file are not chased.
- **What it says now.** On a tiller hull: "By the captain, taking possession: shipping the spare
  tiller (steering by the relieving tackles)." On a wheel ship: "... repairing the wheel (...)",
  as before.
- **Pin moved, old beside new** (TuningNotes, "Package 90, A3"): truth 7-634's last clause, the
  captain's line after the action, from "repairing the wheel" to "shipping the spare tiller".
  Words only; every other clause is as it was.
  - The first pass's 7-634, run on this tree, fails by that clause alone.
  - With 7-632 and 7-633, the step now moves the three truths the ground report named (its rows
    23 to 25).
- **Measured, old beside new** (the probe again, the base beside this commit).
  - The first action at seed 6, left to the captain: 255 lines; every tick, kind and actor the
    same; 9 texts moved, where the first pass had 8. The one more is his line at tick 4,620.
  - The other eight runs are as the first pass measured them.
  - Across all nine runs, no line on a tiller hull names a wheel, but for the player's own
    `repair the wheel` echoed as typed.
- **`tests/test_helm_kind.py`** gains `test_the_captains_mend_order_is_her_helms`, on either
  helm: the tackles rove and nothing else to mend, his repairs give the table's order, said in
  her helm's words, and the work begun is the mend. On the first pass's code its tiller case
  fails (it said "repairing the wheel") and its wheel case passes. The file now has 35 cases.

**The tests of this pass** (on 5426600a, its own worktree; `python -m pytest -n 4 -p
no:cacheprovider -o addopts="--dist loadgroup"`):

| Set | Result |
|---|---|
| the four helm truths, 7-626, 7-632, 7-633, 7-634 (`--slow`) | 4 passed |
| the first pass's truth 7-634 on this tree | 1 failed, by its last clause (the move) |
| `tests/test_helm_kind.py` | 35 passed |
| the captain's files, `--slow`: `test_captain.py`, `test_captain_rules.py`, `test_captains.py`, `test_captain_trials.py` | 51 passed (their whole count) |
| **the fast tier whole**, in the suite's six shards, compared test by test with the base (8b8a982d) | 8,515: 8,508 passed, 6 failed, 1 xfailed. The same differences as the first pass and no other: stop 1's six (passed -> failed); the eight f5be9110 records (skipped at the shallow base -> passed); `tests/test_helm_kind.py`'s 35 (new, passed) |
| the slow tier of the test files touched, `--slow -m "slow and not pace"`: `test_known_truths.py`, the four hull files, `test_helm_kind.py` | 205: 197 passed, 8 xfailed (the suite's own marks, as the first pass), 0 failed; 38 min 37 s |

**Stop 1** (`tests/test_probes_90.py`, six cases) is left alone, on the lead's word: the
coordinating session makes stage 0's guards one table at A3's merge. Its six cases are still the
only failures of the fast tier.

**The package's branch** has moved to 00382c4e since the first pass: A2 merged alone. By
condition 1 its merge into this work is the coordinating session's, so it is not merged here. A
dry run, to save that session a surprise, was made with nothing committed to any branch: `git
merge-tree` of the package's branch and 5426600a, and a local throwaway worktree of the result.
- The merge has **no conflict**: A2's `scripts.py` and `test_known_truths.py` merge cleanly with
  A3's.
- On the merged tree the generator writes every committed ship file byte for byte (A2 moves no
  ship file).
- `tests/test_helm_kind.py`, A2's `tests/test_rig_words.py` and the four hull files: 172 passed.
- The four helm truths: 4 passed.
- Its fast tier was not run: that is the coordinating session's, on its own merge.

**Left as the first pass reports it**, apart from these two changes:
- the captain's unlogged refusal of his own helm order would now be a fourth and a fifth line of
  `captains.py`;
- the mend order is no longer among the places left (§5).

## In brief (the first pass, 8d218fb8)

- **The step's commit: `8d218fb85d84d0e968dcd76c47067b5c24a4f24b`** on this step's own branch,
  cut from 8b8a982d. One commit, 25 files. This report is a second commit, pushed after it.
- **Merged:** nothing.
  - The package's branch has moved to f6f26f8a since the cut (fetched 14:33 UTC). Its new
    commits are documents only: eleven files under `docs/` (the tartane's step 1, nudges 27 to
    29, packages 121 to 123 booked). They share no file with A3, and nothing in them bears on
    it (grepped for A3, tiller, helm and wheel).
  - Since nothing in it was needed, it is not merged. The base stays 8b8a982d, whose code and
    data are f6f26f8a's, so the base run is the merged tree's in all but documents.
- **Built as ruled:**
  - the helm's words come from one table keyed on what her file says she steers by;
  - the six tiller files carry `helm: tiller` with a sourced note, by the generator, the
    hermaphrodite brig's marked JUDGEMENT with ZAZ6177 and ZAZ6179 named;
  - the bilander stays on the wheel, and the twelve other files are byte for byte;
  - the four synonyms are understood;
  - the wheel's words are package 116's exactly.
- **Every tick, kind and actor is the same**, measured base beside head on nine runs: the six
  files, the brig, and the first action at seed 6 twice. Only words move.
- **Pins moved, as the brief names them:** the eight records of the six files, and truths 7-632
  and 7-633, words only. Truth 7-626 holds, as expected. **Truth 7-634 holds too**, because of
  stop 2.
- **Two stops, not built, for the lead** (both allowed at nudge 31: stop 2 built in the
  second pass above; stop 1 the coordinating session's):
  1. **`tests/test_probes_90.py`**: stage 0's guard "no committed file carries ... a hull's
     `helm`" fails on the six files, six cases. The brief does not name it, so it is not moved.
     It is the one test of the fast tier and the guard set that fails by this step.
  2. **The captain's mend order** (`world/captains.py`) needs a third line, an import, so by
     condition 2 it is not built. On a tiller hull he still says "repairing the wheel".
- **The fast tier whole**, the head beside the base, test by test. The head has 8,513 tests
  (8,506 passed, 6 failed, 1 xfailed); the base has 8,480 (8,471 passed, 8 skipped, 1 xfailed).
  - The only failures are stop 1's six.
  - The 33 new tests pass.
  - The base's eight skips were records reading f5be9110 while the clone was shallow. They pass
    at both with history.
  - Nothing else differs.
- **The slow tier of the test files touched** (`test_known_truths.py`, the four hull files and
  `test_helm_kind.py`): 197 passed, 8 xfailed (the suite's own marks), none failed.

## 1. The commit and its files

`8d218fb8` "Package 90, A3: the helm's kind, a tiller's words": 25 files, 689 insertions and 77
deletions. Every file is on the card's list for A3, or is a test or note the brief names.

| File | What | The card's name for it |
|---|---|---|
| `freesail/evolutions/scripts.py` | `HELM_WORDS` (the wheel's row and the tiller's), `helm_words(ship)`, `Script.work()` (None by default), the heave-to's aside read from the table; `HELM_LOST_WORDS` and `HELM_LOST_ASIDE` the wheel's, unchanged | `evolutions/scripts.py` |
| `freesail/combat/hits.py` | the hit's line, its state (`helm_lost`) and the minute's words from the table; the draws as they were | `combat/hits.py` |
| `freesail/evolutions/runner.py` | the manoeuvre's refusal from the table; `_describe` reads `Script.work()` first, the one road for a work's name | `runner.py` |
| `freesail/orders/verbs.py` | the helm orders' refusal from the table; a docstring word | `orders/verbs.py` |
| `freesail/evolutions/repair_scripts.py` | the tackles' and the mend's words from the table; the mend's hold and its `work()` | the tackles' and the repair's words |
| `freesail/orders/damage.py` | "The hands are {the work in hand} already." by `Runner.doing`; a comment | the order given twice |
| `freesail/world/captains.py` | **one line**: the captain's reason, `why=str(ship.extra["helm_lost"])`, the hit's own words | one of its two repair lines (the other is stop 2) |
| `data/evolutions/relieving_tackles.yaml` | `on_start: {log: "{begin}"}` | its start line |
| `data/evolutions/repair_wheel.yaml` | `on_start: {log: "{begin}"}`, `on_fail: {log: "Could not {work}: {reason}." ...}` | its start and fail lines |
| `data/vocabulary.yaml` | the four synonyms of `repair the wheel`, and nothing else | condition 3 |
| `tools/gen_ships.py` | `"helm": "tiller"` and its note in four hull dicts: the cutter, the lugger, the smack, and the schooners' one | the hull dicts |
| `tools/ships/neufchatel.py` | the same in `HULL_FIGURES` and `HULL_NOTES` | the hermaphrodite brig's key |
| `data/ships/` six files | regenerated, two lines each (below) | by the generator |
| `tests/test_helm_kind.py` (new) | the cause's level: 33 cases | plan §7.1's new test file |
| `tests/test_hull_cutter.py`, `test_hull_lugger.py`, `test_hull_smack.py`, `test_hull_schooner.py` | the eight records, naming the key | the brief's pins |
| `tests/test_known_truths.py` | truths 7-632 and 7-633, words; `TILLER_LOST` beside them | the brief's pins |
| `docs/dev/TuningNotes.md` | "Package 90, A3", placed after the package's other sections and before package 119's | the brief |

## 2. The pins moved, old beside new

The reason for each is the same: the six files carry `helm: tiller`, A3's ruled key, and the
first action's ship is the cutter, a tiller hull. Every case is a move in words or a key, with
every tick the same.

| Test | Old | New |
|---|---|---|
| `tests/test_hull_cutter.py::test_the_hull_figures_stand_as_filed` | her hull but its profile is `HULL_AS_FILED` | the same once `helm` is held to "tiller" and taken out (`HELM_A3 = (None, "tiller")`) |
| `tests/test_hull_cutter.py::test_a_diff_of_her_physics_keys_against_git_shows_none` | her hull equals f5be9110's; the old keys, then `profile` | the same once `helm`, absent there and "tiller" here, is taken out; the old keys, then `helm` and `profile` |
| `tests/test_hull_lugger.py::test_no_hull_figure_the_physics_reads_moved` | `HULL_AS_FILED`; the profile last | the same once `helm` is held and taken out; the profile last still |
| `tests/test_hull_lugger.py::test_a_diff_of_her_files_physics_keys_against_git_shows_none` | her hull equals f5be9110's | the same once `helm` is taken out, old beside new |
| `tests/test_hull_smack.py::test_no_figure_the_physics_reads_has_moved_by_the_pins` | `PHYSICS_KEYS`, in order | the same once `helm`, the last of those keys, is held and taken out |
| `tests/test_hull_smack.py::test_her_file_but_for_her_lines_is_what_it_was_against_git` | the file at f5be9110 but for SW-4's keys and her lines, as data and as text | the same once `helm` is taken out of the data and its two lines (`HELM_A3_LINES`) out of the text, found once, just before her lines |
| `tests/test_hull_schooner.py::test_no_figure_the_physics_reads_moved[data/ships/topsail-schooner.yaml]` and `[...privateer-schooner.yaml]` | the physics' view equals f5be9110's but for SW-4 and item 37 | the same once the hull's `helm` is taken out, old beside new |
| truth 7-632 (`test_truth_7_632_the_wheel_shot_away_stops_the_helm_until_the_tackles_are_rove`) | ten refusals and the standing order's end with `HELM_LOST_WORDS`; the aside "the helm not answering, the wheel shot away" | each ends with the tiller's refusal, "The tiller is shot away and the helm does not answer: rig the relieving tackles ('rig the relieving tackles') to steer her by them, or ship the spare tiller ('ship the spare tiller')."; the aside "... the tiller shot away"; her helm asserted the tiller. Its two assertions on `HELM_LOST_WORDS` are kept |
| truth 7-633 (`test_truth_7_633_by_the_tackles_she_answers_at_half_the_wheels_rate_until_it_is_repaired`) | "more slowly than by the wheel."; "The hands are repairing the wheel already."; "The wheel is repaired and new wheel-ropes rove: she steers by the wheel again; the relieving tackles are cast off."; "the wheel is whole" | "more slowly than by the tiller."; "The hands are shipping the spare tiller already."; "The spare tiller is shipped in the rudder head: she steers by the tiller again; the relieving tackles are cast off."; "the tiller is whole". The rates are asserted as they were |

**That these ten and no others move** (measured): the base's own four hull files, run on this
commit's tree, fail exactly the eight records (8 failed, 100 passed), and the base's own
truths 7-626 to 7-634 fail exactly 7-632 and 7-633 (7-626 and 7-634 pass). At the base, all of
them pass.

**Held:**
- **truth 7-626**: its words are the same on either helm;
- **truth 7-634**: its "repairing the wheel" is the captain's mend order, left by stop 2. With
  the mend order built, its last clause moves to "shipping the spare tiller" (the ground
  report's row 25).

## 3. Every tick and kind the same

**The probe** (kept in the session's scratch). Each of the six files, and the brig as the
wheel's control, started from the harbour at seed 7:
- at 60 s her helm was shot away by `combat.hits._deck_hit` itself, its draw forced, nobody hurt;
- then the orders: `steer north` and `rig the relieving tackles`, run until rove; `repair the
  wheel` twice, run until mended; then, with the helm whole, `repair the wheel`, `repair the
  tiller` and `ship the spare tiller`.

The first action at seed 6 was run twice, as the harbour starts it:
- with the player at the prompt on the minute the helm goes: `steer north-west`, `tack`, `heave
  to`, the tackles twice, a course, the mend twice and done, then the three orders with the helm
  whole;
- left to the captain for two hours.

Every log line is compared by tick, kind and actor, the base (8b8a982d) beside this commit:

| Run | Lines | Ticks, kinds, actors | Texts moved | Rove (s, sampled) | Mended (s, sampled) |
|---|---|---|---|---|---|
| cutter | 21 | the same | 10 | 330 = 330 | 2,555 = 2,555 |
| lugger | 22 | the same | 10 | 330 = 330 | 2,525 = 2,525 |
| smack | 20 | the same | 10 | 420 = 420 | 2,555 = 2,555 |
| topsail schooner | 19 | the same | 10 | 390 = 390 | 2,615 = 2,615 |
| privateer schooner | 19 | the same | 10 | 390 = 390 | 2,615 = 2,615 |
| hermaphrodite brig | 17 | the same | 10 | 390 = 390 | 2,585 = 2,585 |
| brig (the wheel) | 20 | the same | 2: `repair the tiller` and `ship the spare tiller`, "not an order this ship understands" -> "the wheel is whole and she steers by it" | 390 = 390 | 2,585 = 2,585 |
| first action, the prompt | 51 | the same | 13 | 460 = 460 | 4,545 = 4,545 |
| first action, the captain | 255 | the same | 8 | the same | his mend begun at tick 4,620 at both |

On the six files the ten lines that move are:
- the hit;
- the refusal;
- the tackles begun;
- the tackles rove;
- the mend begun;
- given twice;
- the mend done;
- the helm whole;
- `repair the tiller` and `ship the spare tiller`, each understood where it was refused.

The first action adds the heave-to's aside, the minute's line ("Shot from a cutter: the tiller
shot away."), the robbed gun ("Shipping the spare tiller at quarters: four hands taken from No.
3 gun; the guns go on short-handed."), the captain's reason ("By the captain, engaging: rigging
the relieving tackles (the tiller shot away).") and the work named in the waiting and short
lines ("... the hands are setting up the rigging, shipping the spare tiller, and filling away.").
The full old-beside-new table of the words is in TuningNotes, "Package 90, A3".

**On a tiller hull, the one line of the game left in the wheel's words** is the captain's mend
order (stop 2): "By the captain, taking possession: repairing the wheel (steering by the
relieving tackles)." The player's own `repair the wheel` is echoed as typed ("Order: repair the
wheel."), and is answered in the tiller's words.

**Not moved:** the tackles' five minutes with six hands and the mend's half hour with four are
the files' own on either helm (`tests/test_helm_kind.py` reads them). The two works hold no gear
in common on either helm: the mend holds "the wheel" or "the rudder head", and the tackles hold
"the tiller". So they go on together as before. No class is added, so the checkpoint's list is
not touched and truth 7-606 was not needed.

## 4. The tests run, with their counts

All were run from the tree's root with `python -m pytest -n 4 -p no:cacheprovider -o
addopts="--dist loadgroup"`. The clone was shallow at first. With history fetched, the five
git-diff records run (they skip where f5be9110 is missing); all 108 cases of the four hull files
pass at the base and at the head.

| Set | Tree | Result |
|---|---|---|
| **the fast tier whole**, base | 8b8a982d (worktree), one run | 8,480: 8,471 passed, 8 skipped, 1 xfailed; 1 h 44 min (beside the head's first try and my sets) |
| **the fast tier whole**, head | 8d218fb8 (worktree), in the suite's own six shards (`FREESAIL_SHARD=i/6`, i 0 to 5, one after another) | 8,513: 8,506 passed, 6 failed (stop 1's six), 1 xfailed; 1,430 + 1,445 + 1,452 + 1,378 + 1,421 + 1,381 by shard, 13 to 15 min each |
| the guard set, `--slow`: truth 7-185 (the byte test, two-way), `test_rig_classing.py` (the golden table), `test_schooner_mast.py`, `test_probes_90.py`, `test_check_viewer_guns.py` | head | 249 passed, 6 failed (stop 1's six) |
| the four helm truths, `--slow` | head | 4 passed |
| the base's own four helm truths | head | 7-626 and 7-634 pass; 7-632 and 7-633 fail (the moves) |
| the six hulls' files (`test_hull_cutter`, `_lugger`, `_smack`, `_schooner`, `test_neufchatel`), `test_helm_kind`, `test_held_work`, `test_grammar_book`, `test_fight`, `test_checkpoint`, the four `test_boat_*` files, `test_agents`, `test_catalogue`, `test_in_world`, `--slow` | head | 579 passed, 2 xfailed (the base's two) |
| the base's own four hull files | head | 8 failed (the eight records), 100 passed |
| the slow tier of the test files touched (`test_known_truths.py`, the four hull files, `test_helm_kind.py`), `--slow -m "slow and not pace"` | head (8d218fb8 worktree) | 205: 197 passed, 8 xfailed (the suite's own marks: truths 11, 24, 26, 28, 31, the schooner's polar peak, the frigate's plain sail, truth 7b-100's old form; none added), 0 failed; 42 min 48 s |

**The base comparison, test by test** (`compare_junit.py` in the session's scratch):

Test names are compared without the xdist group label (`@file.py::fixture`), which names
whichever fixture grouped the test first and so differs between a whole run and a shard.

| Base -> head | Tests |
|---|---|
| passed -> failed (6) | `tests/test_probes_90.py::test_no_committed_file_carries_sweeps_a_towed_boat_a_helm_or_a_dipping_whole_lateen[cutter]`, `[hermaphrodite-brig]`, `[lugger]`, `[privateer-schooner]`, `[smack]`, `[topsail-schooner]`: stop 1 |
| skipped -> passed (8) | the records that read f5be9110: `test_hull_brig` (two), `test_hull_frigate`, `test_hull_cutter`'s diff, `test_hull_lugger`'s diff, `test_hull_schooner` (two), `test_hull_smack`'s diff. The base ran while the clone was shallow; run again at the base with history, the six hull files pass whole (177 passed). Of the eight, the cutter's, the lugger's, the smack's and the two schooners' are moved records; the frigate's and the brigs' are A0's, unmoved |
| absent -> passed (33) | `tests/test_helm_kind.py`, the new file |
| any other | none |

**Why the head ran in shards.** The container restarted at about 14:30 UTC, at about a third of
the head's first whole run. The second was run in the suite's own shards, so that a further
restart would lose one shard and not the whole. The shards together are the whole run: every
test of the base's run is in one of them.

## 5. Where else the cause was looked for

Every "wheel" in `freesail/`, `data/` (bar the ship files), `client/` and `docs/primer/` was read
(`git grep -i wheel`):

**Mended here** (each now reads the table):
- the hit;
- the two refusals;
- the aside;
- the tackles' four lines;
- the mend's six lines, with its hold and its name;
- the order given twice;
- the captain's reason.

**Left, each for a reason:**
1. **`world/captains.py`, the mend order**: stop 2 (built in the second pass).
2. **`world/captains.py`, the refusal of his own helm order** while the tackles are not rove
   (`give`: `text=HELM_LOST_WORDS`, `"not_given": "the wheel shot away"`). It is the wheel's on
   every hull. The event goes back to his judgement and is never logged: truth 7-634 asserts
   nothing of his is refused in the log, and his callers read only its `kind`. So no one reads
   its words. It would be a fourth and a fifth line of that file (the second pass).
3. **The comments in `world/captains.py`** about the wheel (ll. 4667, 4677, 4960, 4981).
   Comments, and outside the two lines.
4. **The primer.** Chapter 25's table (`docs/primer/25-water-wounds-and-the-fight-on-deck.md`,
   ll. 63-70) gives the wheel's words. Chapter 2 (l. 192) says that the conning words "speak to
   the wheel". The card does not give A3 the primer (the ground report's §6 found chapter 25).
5. **`freesail/ship/schema.py`** (stage 0's) still says the helm is "read by nothing yet" (ll.
   134, 620). That is now untrue, and for stage 0 to mend.
6. **The two evolution files**: their header comments and `repair_wheel.yaml`'s `verb:` comment
   ("repairing the wheel"). Comments, outside the start and fail lines the card gives.
7. **`belay the tiller`** is refused ("There is no such part as the tiller in this ship.").
   `more_work_nouns` has `wheel` alone. On either helm, `belay the wheel` belays the mend. On a
   tiller hull, `belay shipping the spare tiller` and `belay ship the spare tiller` belay it by
   its name. Condition 3 keeps the vocabulary's change to the four synonyms.
8. **`physics/hull.py`, `physics/integrate.py`** name the man at the wheel in comments. The
   helmsman's model is one for both helms. Not A3's files.
9. **`world/places.py:83`** quotes Falconer's QUARTER-DECK (where the wheel is), a place's words
   and not a helm shot away. Out of A3's reach.
10. **The client's "wheel"** is the mouse's wheel.
11. **A game saved before this step**, on one of the six, reads the wheel until a new start. Her
    pickled spec has no `helm` (the ground report's §6).

**The four synonyms reach the wheel files too**, as the ground report foresaw (its §6):
`ship the spare tiller` mends a wheel ship's wheel. No pin moves by it.

## 6. The generated files, and the tool that writes each

- **`data/ships/*.yaml`**, by `python tools/gen_ships.py data/ships`, the first bare argument
  the folder. Run into a scratch folder first and compared with `cmp`:
  - six move, each by two added lines under `hull:` (a note and `helm: tiller`, after `rudder`
    and before `profile`): `cutter.yaml`, `lugger.yaml`, `smack.yaml`, `topsail-schooner.yaml`,
    `privateer-schooner.yaml`, `hermaphrodite-brig.yaml`;
  - the other twelve are byte for byte, the bilander among them.
  - Truth 7-185 (the generated set equals the committed set, file for file) passes, so the files
    are reproducible by their tool on any merged tree.
- **No other generated file moves.** The checkpoint's list is unmoved (no class added). The
  grammar book's page is served from the vocabulary at run time, and no committed page holds the
  synonyms (grepped).

## 7. The two stops, with the moves they want

**Stop 1: `tests/test_probes_90.py::test_no_committed_file_carries_sweeps_a_towed_boat_a_helm_or_a_dipping_whole_lateen`**,
the six cases `[cutter]`, `[lugger]`, `[smack]`, `[topsail-schooner]`, `[privateer-schooner]` and
`[hermaphrodite-brig]`.
- **Why it moves:** stage 0's guard that the key is inert, `assert "helm" not in doc["hull"]` and
  `ship.spec.hull.helm == "wheel"` for every committed file. A3's ruled move is that six files
  carry the key, so the guard cannot hold for them. It was written after the ground report was
  measured (at 5067945e, before stage 0), so the ground report and the brief do not name it.
- **Not moved here.** The step's other 12 cases of that test pass.
- **The move it wants**, words of the test only:

  ```python
  # package 90, A3 (old beside new: TuningNotes): the six tiller files carry the key, the twelve none
  helm = "tiller" if path.stem in A3_TILLER_FILES else None
  assert doc["hull"].get("helm") == helm
  ...
  assert ship.spec.sweeps is None and ship.spec.hull.helm == (helm or "wheel")
  ```

  `A3_TILLER_FILES` would be the six stems, and its docstring would say so. Its name
  ("..._a_helm_...") would be kept.

**Stop 2: the captain's mend order** (`freesail/world/captains.py`, `Captain._repairs`). Built
in the second pass, as drafted here (the top of this report).
- **Why it needs a third line:** the order must be the table's (`helm_words(ship)["mend"]`), and
  `_repairs` has no road to the table without an import.
  - The local import block there names three functions of `repair_scripts`.
  - Reading the hit's state, which serves the reason line, cannot serve the order.
  - A branch on the hull's kind in the line would be the branch per message the brief forbids.
- **What it wants**, three lines in all with the reason's:

  ```python
          from freesail.evolutions.scripts import helm_words  # the third line
          ...
              wanted.append((helm_words(ship)["mend"], "steering by the relieving tackles"))
  ```

  With it, "By the captain, taking possession: shipping the spare tiller (steering by the
  relieving tackles)." Measured: `said_as_done` on the cutter gives "shipping the spare tiller"
  for that order. Truth 7-634's last clause moves with it, `"repairing the wheel"` to
  `"shipping the spare tiller"`, words only.

## 8. What I was unsure of

- **Words not in the ground report's table.** The builder's own, by the same ruling (JUDGEMENT):
  - the tackles not wanted: "the spare tiller is shipped; the relieving tackles are not wanted";
  - the mend belayed: "the spare tiller not shipped, ...";
  - the mend failing: "Could not ship the spare tiller: ...";
  - the mend's hold on a tiller hull, "the rudder head". It is never said, and it is chosen so
    that the tackles and the mend go on together as on the wheel.
- **The captain's reason** reads the hit's state (`ship.extra["helm_lost"]`), which the hit
  writes from the table. It is one line and needs no import. A reader may prefer the table read
  directly, which would need stop 2's import.
- **The sources' notes** cite page facts and paraphrase rather than quote:
  - Falconer's "a wheel save in small vessels, which need none";
  - Chapelle's reading of *Musquidobit*;
  - Holdsworth's mizens stepped for the tiller's play.
- **The test's own measure.** `tests/test_helm_kind.py` drives each of the six and two wheel
  ships through the whole passage, at about one to two seconds a case, in the fast tier. Its
  ticks are not pinned, since the mend's time is stretched by the weather's factor. The
  ticks-the-same proof is the probe's, base beside head (§3).
- **Running the tiers.** The base's run and the head's ran at the same time on four cores, with
  my probes and sets beside them at the start. A test that times itself (the replay's
  fingerprint, the pace floors) may differ by load alone. None did here: the base's run
  failed nothing, and the head's shards (run alone) failed nothing but stop 1's six.

## 9. Rules kept

- No name of an AI model or its maker in any file or commit message; no trailer.
- LF only: `git diff | tr -cd '\r' | wc -c` is 0.
- Ruff is clean; no added Python line is over 100 characters.
- Nothing under `docs/agents/consent/`.
- No test is skipped, xfailed or loosened. Each moved pin is old beside new, its new figure held
  exactly.
- Pushed only to this step's own branch; no force, no rebase, no merge.

## The list of nudge 45 (2026-11-21)

The lead's reader passed A3 with a list (nudge 45; the trunk at 6038f23a, the note at the end of
`docs/dev/M7-WorkPackages.md`). Each item is its own commit, to ride the next package hash. None
moves a tick.

**The branch.** Fast-forwarded to the package's branch at **0d5d2c56** (A3, A1a and A1b), which held
fba02fff, so there was no merge commit. The four items are built on it, and the base run below is
on that same tree.

| Item | Commit | Files |
|---|---|---|
| 1. A mend not in hand named as her helm names it | `ebe85fd4` | `freesail/orders/work.py`, `freesail/evolutions/scripts.py`, `freesail/evolutions/repair_scripts.py`, `tests/test_helm_kind.py`, `docs/dev/TuningNotes.md` |
| 2. `belay the tiller` and `belay the spare tiller` belay the mend | `e8112190` | `data/vocabulary.yaml`, `tests/test_helm_kind.py`, `docs/dev/TuningNotes.md` |
| 3. The tiller's words on a wheel ship, pinned | `9c8fb3c0` | `tests/test_helm_kind.py`, `docs/dev/TuningNotes.md` |
| 4. The primer, the schema's comments (the quarterdeck a stop) | `b7e0f650` | `docs/primer/02-...`, `22-...`, `25-...`, `freesail/ship/schema.py`, `tests/test_helm_kind.py`, `docs/dev/TuningNotes.md` |

The record, old beside new, is TuningNotes, "Package 90, A3", its subsection "The list of nudge
45". **The proof of each:** a probe of every belay order on the cutter (a tiller) and the brig (a
wheel), the tackles in hand and the mend in hand, each order on a fresh world at seed 7, old
(0d5d2c56) beside new (`probe_belay.py`, in the session's scratch). Each item's new test fails on
the old code: all four run together in a separate worktree at 0d5d2c56, 4 failed (item 1's wheel
case passes there, as it should).

### 1. A mend not in hand, named as her helm names it

**The cause:** a belay's refusal named a work not in hand by the vocabulary's verb, while the
runner names it, once begun, by its script.

**The mend at that cause:** the script's own name is readable before the work exists
(`Script.work_of(ship)`, a class method that `Script.work` calls). `orders/work.py` names a work
not in hand by it (`_work_words`), in both of its readings: by the order and by the kind of work.
Only the helm's mend has a name of its own, so every other work is named as before.

| The cutter, the tackles in hand, no mend | Old | New |
|---|---|---|
| `belay shipping the spare tiller`, `belay ship the spare tiller`, `belay the wheel`, `belay repairing the wheel` | "Nothing in hand or waiting is repairing the wheel. The work in hand: rigging the relieving tackles." | "Nothing in hand or waiting is shipping the spare tiller. The work in hand: rigging the relieving tackles." |

- On the brig, the same four answer as before ("... is repairing the wheel.").
- Every answer's kind, the lines after it and the work in hand are the same.
- No pin moves.
- Pinned: `test_a_mend_not_in_hand_is_named_as_her_helm_names_it`, on either helm. On the old code
  its tiller case fails and its wheel case passes. (Its first check ran in the base's tiering
  worktree for a few seconds, under a name pytest does not collect, and was removed at once. It was
  run again in the separate worktree with the other three.)

### 2. `belay the tiller` and `belay the spare tiller`

`more_work_nouns` gains `tiller` and `spare tiller`, each to the mend's verb, beside `wheel`.

| Order | Ship, in hand | Old | New |
|---|---|---|---|
| `belay the tiller` | cutter, tackles and mend | "There is no such part as the tiller in this ship." | "Belayed shipping the spare tiller; the spare tiller not shipped, the helm lost as the shot left it." |
| `belay the spare tiller` | cutter, tackles and mend | "... as the spare tiller in this ship; did you mean the square sail?" | the same |
| either | cutter, tackles alone | the refusals above | "Nothing in hand or waiting is shipping the spare tiller. ..." |
| either | brig, tackles and mend | "There is no such part as ..." | "Belayed repairing the wheel; the wheel not mended, ..." |
| either | brig, tackles alone | the refusals above | "Nothing in hand or waiting is repairing the wheel. ..." |

- **Beside it, refusal to refusal (measured, no pin):** `belay the tiller tackles` and `belay the
  tiller ropes`.
  - Old: "There is no such part as the tiller tackles (ropes) in this ship", with "did you mean the
    topsail reef tackle?" on the cutter.
  - New: "Nothing in hand or waiting answers to 'the tiller tackles' ('the tiller ropes'): name the
    work as the log does, ...".
  - Neither belays anything, old or new. The vocabulary has `rig the tiller tackles` and `reeve new
    tiller ropes` as synonyms of the two works. **A noun for each, so that each belays its work, is
    listed for the lead, not built:** the list names the tiller and the spare tiller alone, and
    `belay the wheel ropes` is refused as these now are.
- Pinned: `test_on_a_tiller_hull_the_tiller_and_the_spare_tiller_belay_the_mend`. It fails on the
  old code.

### 3. The tiller's words on a wheel ship

Pinned on the brig with the tackles in hand
(`test_on_a_wheel_ship_the_tillers_words_start_and_belay_her_wheels_mend`):
- `ship the spare tiller`, `ship a spare tiller`, `ship a new tiller` and `repair the tiller` each
  start the wheel's mend, begun in the wheel's words and named "repairing the wheel";
- `belay the tiller`, `belay the spare tiller`, `belay shipping the spare tiller` and `belay ship
  the spare tiller` each belay it, in the wheel's words;
- the "whole" refusal is pinned beside them already.

Nothing moves by this item: the starts were taken before, and two of the belays are item 2's. On
the old code the test fails at `belay the tiller`.

### 4. Older wheel words a tiller hull still read

- **The primer**, a clause each, each run against the game
  (`test_the_primer_says_of_a_tiller_what_the_game_does`):
  - **Chapter 25:** a row, `ship the spare tiller`: "the same where she steers by a tiller: the
    tackles hooked to the stump of the tiller and manned on deck, and the spare tiller shipped in
    the rudder head, half an hour". Below it, "With the wheel (or the tiller) shot away ...".
  - **Chapter 22:** "the wheel shot away (or the tiller, in a hull steered by one) loses you the
    helm".
  - **Chapter 2:** the conning words "speak to the wheel rather than to the course (to the tiller,
    in the same words, in the cutter, the lugger, the smack, the two schooners and the
    hermaphrodite brig)". Run on the cutter beside the frigate, the ten are taken in the frigate's
    words, but for her own heading where a word names it.
  - No forms table or orders block changes. The chapters' sizes are measured where they are served
    (only chapter 3's is pinned). The primer's, the grammar book's, the in-world, the agents' and
    the loader's tests pass, 1,486 with the helm tests.
- **`freesail/ship/schema.py`**: its two comments that the key is "read by nothing yet" now say
  that the six tiller files carry it and the helm's words read it. Comments only.
- **`freesail/world/places.py`'s quarterdeck, by her helm: a stop, not built.**
  - `Places` is made with the ship's name alone, by `core/world.py`, which nobody touches after
    stage 0.
  - The description's two readers (`the places` reading's `items` and `described`) are in
    `api/readings.py`, which the list does not give.
  - So in `places.py` alone it cannot be keyed on her helm. It wants two lines of
    `api/readings.py`'s `_places`, the quarterdeck's description by the ship's helm, read through
    `places.py`.
  - The other road is "the helm" on every ship, which moves every wheel ship's words. For the lead.

**Listed, not asked, and left:** the five boats' files, and the hermaphrodite brig's helm.

### The tests, on b7e0f650 against the base on the same tree (0d5d2c56)

All on b7e0f650 in its own worktree, and the base on 0d5d2c56 in its own: `python -m pytest -n 4
-p no:cacheprovider -o addopts="--dist loadgroup"`, the fast tier in the suite's six shards
(`FREESAIL_SHARD=i/6`, i 0 to 5, one after another; the two runs never shared the cores).

| Set | Base, 0d5d2c56 | Head, b7e0f650 |
|---|---|---|
| **the fast tier whole** | 8,665: 8,664 passed, 1 xfailed | 8,670: 8,669 passed, 1 xfailed |
| the four helm truths, 7-626 and 7-632 to 7-634 (`--slow`) | | 4 passed |
| `test_held_work`, `test_hands`, `test_helm_kind`, `test_primer` (`--slow`) | | 1,263 passed |
| the primer's and the vocabulary's readers (`test_primer`, `test_grammar_book`, `test_in_world`, `test_agents`, `test_probes_90`, `test_ship_loader`, `test_helm_kind`), at item 4 | | 1,486 passed, 1 xfailed |
| the vocabulary's (`test_grammar_book`, `test_orders`, `test_helm_kind`, `--slow`), at item 2 | | 773 passed |
| the list's four new tests on the old code (a worktree at 0d5d2c56) | 4 failed (item 1's wheel case passes) | 5 passed |

**Test by test** (names without the xdist group label): **the head is the base's 8,665, each with
the same outcome, and five new tests, each passed**:
- `test_a_mend_not_in_hand_is_named_as_her_helm_names_it[tiller]` and `[wheel]`;
- `test_on_a_tiller_hull_the_tiller_and_the_spare_tiller_belay_the_mend`;
- `test_on_a_wheel_ship_the_tillers_words_start_and_belay_her_wheels_mend`;
- `test_the_primer_says_of_a_tiller_what_the_game_does`.

Nothing else differs. No timing test tripped in either run.

**The package's branch has moved since**, to 248569c5 (A1c merged). By your word its merge with
these four commits, and the tiers there, are yours. A dry run, with nothing committed to any
branch: `git merge-tree` of 248569c5 and b7e0f650 has **no conflict** (A1c's `scripts.py` and
`TuningNotes.md` merge cleanly with the list's). On a throwaway worktree of the result, ruff is clean
over `freesail`, `tools` and `tests`, and `test_helm_kind` with A1c's `test_lateen_whole` pass
(122).

### Rules

- Each commit's author is as the cloud gives it.
- No model or vendor name and no trailer in any commit.
- LF endings; ruff clean.
- TuningNotes' sections are kept whole: the new subsection sits at the end of A3's, before package
  119's.
- No generated file is touched: no ship file moves, and the checkpoint's list is unmoved (no class
  added; `Script.work_of` is a method).
- Pushed only to this step's own branch.
