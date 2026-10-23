# FreeSail M7b: playtest and hotfix review

**Date:** 22 Oct 2026
**Covers:** the playtests of 18–22 Oct 2026 and the director session's live hotfixes, against the latest GitHub snapshot of `claude/dreamy-darwin-d77nty`, the Design Proposal (v0.2), the M7b technical specification and the roadmap.
**Prepared:** locally, on the owner's machine, by a cold Opus 5.5 review session with sixteen read-only parallel reviewers. Nothing was sent to GitHub, no game tool was called, and no source folder was modified.

---

## 0. Summary

### 0.1 Merge

**Yes, the latest GitHub version (G) and the hotfix version (H) merge cleanly.**
- **The base.** I rebuilt their common base (the GitHub snapshot of 19 Oct, merge of package 53b) from the hotfix session's own backups. Its code fingerprint matches the saves made on it (`4330be741d1580ee`), so the base is verified, not guessed.
- **The merge.** 39 hotfix files go onto G. 8 files were changed on both sides; 7 merged automatically, and the one conflict was two appended TuningNotes sections, kept both.
- **The two sides don't touch the same code.** No hotfix change falls within 15 lines of a package 66 change.
- **Checks.**
  - Ruff is clean.
  - The whole slow test tier passes 3,819 on the merged tree, against 3,807 on an untouched G. The 12 extra are the hotfix's tests.
  - Both fail the same 9 tests on this Windows machine. Those are pre-existing in G: seven pinned truths and two Windows-only tests.
- **One precondition.** The hotfix silently rewrote 13 files from LF to CRLF. The merged tree is normalised.

The proposed merge is at `merged/FreeSail-merged`. **§2.**

### 0.2 The hotfix

**The hotfix work is sound and faithful to what the owner asked.** The work was:
- the aboard table widened from 4 things to 24;
- the hull's repair;
- kedging off;
- the well sounded and read;
- the starter book's held well order removed, with three justified re-pins;
- a checkpoint crash found in play and fixed.

It conforms to M7b §3, §4, §17a and §19. Play confirms the kedge, the well and the watering work.

Before folding it in:
- fold from the LF tree;
- add a regression test for the checkpoint crash;
- correct the TuningNotes' cause for the failing pins (it blames the session's own edits by misreading local time as UTC);
- fix the stale "man the pumps" refusal and the early "kedge comes home" line;
- put the new things in the director's brief;
- say M7, not "milestone 8", for the pumps.

**§3.**

### 0.3 The playtests

Six playtests and five models, from four-minute starts to the longest run yet. The Western Islands run alone is 27 days of ship's time over three days of real time, and still going.

**What worked.**
- **The director.** Opus directed with real craft: restraint, honest causes, the decision handed back to the player through voices like Pascoe. M7b's central claim is shown for a strong model (§6.1).
- **Package 66, live for the first time on G.** The station's line, and a model's own order ending its stand-by, behaved as specified.
- **Needs, trade and freight.** The needs bit, and trade and freight worked.
- **Fable 5.1 as officer** was exemplary.
- **Sonnet as officer** was accurate and candid.
- **The models' own accounts** were consistent: an honest world that pushes back, continuity, room to choose, and people who answer are what make it good for them. §4, §7.

**What hurt most** (✔ = checked in the code here):
1. **✔ The grounding at Horta came without fair warning, and the cause is one predicate.**
   - "Any anchor down" counts as riding. It froze the master's account (the chart and the depth by chart), and it muted the lookout's land-ahead warning, while she dragged under sail at 7 knots onto the beach.
   - It's built to M5 §12's words; the words are wrong for a ship with way on.
   - That's the owner's "the map never updating" and the missing "urgent lookout warning" exactly. Open in G. **R-01.**
2. **✔ Officers' words to a player-held captain are mis-filed as "the captain to the captain … nobody holds the station".** Every model officer in every run hit it; Sonnet lost about 13 reports. **R-13.**
3. **✔ The word after "Mr Bowen," is dropped**, which turned "no land in sight yet" into "land in sight yet". **R-14.**
4. **A person made "aboard" another ship lands on the player's quarterdeck.** Three foreign captains did, and the GLM mate took the owner for one of them for days. **R-15.**
5. **The MCP door's stand-by.**
   - The desktop client cuts a tool call at 60 s against the bridge's 200 s default, and each cut re-sends a 32–41k-character brief.
   - Every poll re-lists the whole stand-by history, about 1.3 M characters in four hours for one director.
   - "Still waiting" gives no time, and a new stand-by can't replace one.

   **R-25 to R-28; package 58.**
6. **✔ The brief's "no enemy heavier than a brig" has never been enforced.** **R-38.**
7. **The lugger gets under way with a square-rigger's script, under the jib alone.** **R-45.**
8. **✔ Every chart sounding reads "NaN fm"** (a missing constant). **R-05.**
9. **Consent: a model can leave by quoting the opt-out token in praise of it.** GLM did, twice. The owner's remedy (delete, ask plainly, a plain yes) worked, and the gate held. But the harness has no way to set a false positive aside without deleting its history, and records don't travel to a new folder. **R-50.**

**Most of the rest is grammar and noise:**
- directors fail 37–61% of world orders unless they wrote the code;
- weather systems that stack and step;
- far ships that vanish;
- a budget spent on the director's own echoes;
- notable lines that wake stations for nothing.

§5 ranks 63 de-duplicated findings, each traced to its source.

### 0.4 Next steps

1. Fold in the hotfix from the merged tree with the §3.3 fixes.
2. Fix the seven P0 items in §8.2. Most are small.
3. Brief package 58 next.
4. Give directors a forms reference and a **dry run** for world orders, their own top request.
5. Carry the corrected "Open, for the lead" into G.

**§8.**

### Contents

0. Summary
1. Provenance and method
2. The merge
3. The hotfix work, reviewed
4. The playtests, one by one
5. The findings, de-duplicated and ranked (R-01 to R-63)
6. Against the design proposal, the M7b spec and the milestones to come
7. The models at their stations
8. Recommendations

Appendix: files and how to reproduce


---

## 1. Provenance and method

### 1.1 The three copies, and the fourth that had to be rebuilt

None of the three folders is a git checkout. Each is an unzipped GitHub snapshot of the `claude/dreamy-darwin-d77nty` branch, and the files carry the zip's timestamps.

The game's own **rules fingerprint** settles which code a save was made under. It is `freesail.core.world.fingerprint_of`: a SHA-256 over every `freesail/**/*.py` and every `data/**` file except the chart tiles, with line endings normalised. Every save stamps it in `build.rules`. I recomputed it for each folder with a standalone copy of the function (`work/scripts/fingerprint.py`) and matched it against all 30 saves on the machine.

| Label | Folder | Fingerprint | What it is |
|---|---|---|---|
| **O** | `Downloads\FreeSail-claude-dreamy-darwin-d77nty-old` | `04b66d9b753bc766` | The snapshot of 18 Oct (zip time 03:12 local) |
| **B** | *rebuilt*: `M7b-Review-2026-10-22\work\base-871e819` | `4330be741d1580ee` | The snapshot the hotfix copy started from (zip time 19 Oct 04:18 local) |
| **H** | `Downloads\FreeSail-claude-dreamy-darwin-d77nty` | `372c899e355594fa` | B plus the director session's live hotfixes, 19–22 Oct |
| **G** | `D:\Projects\FreeSail\FreeSail-claude-dreamy-darwin-d77nty` | `e19ddb854219fbd8` | B plus package 66 and its records (zip time 19 Oct 06:17 local); the main session's latest |
| **M** | *new*: `M7b-Review-2026-10-22\merged\FreeSail-merged` | `10fbc075275a7c52` | G plus every hotfix change: the proposed merge |

**`-old` is not the hotfix copy's base.** The director session began on O on the evening of 18 Oct. At the owner's request ("make a copy of the folder for yourself now"), it snapshotted O. The owner then swapped in a newer download, B, on the morning of 19 Oct and told the session at 22:39Z. So O is two steps behind G, and B is one.

B no longer existed as a folder. I rebuilt it from the director session's own scratch copies:
- `pristine-new`: the new download, taken before the first edits, with that session's backups of every file it was about to edit restored.
- Minus the one data file the owner added afterwards (`interesting-passage-nobudget.yaml`).

The rebuilt tree fingerprints to **`4330be741d1580ee`**, exactly the stamp on the saves made on B before any hotfix (the merchant-brig runs, ticks 4590–24592). The merge base is therefore verified for all code and data, not inferred. Docs and tests aren't covered by the fingerprint. For those, the restored backups and the zip timestamps agree.

**Fingerprints along the hotfix timeline** (from the saves):
- `4330be74…` on B as downloaded.
- `f459547b…` once the owner added the no-budget brief (19 Oct 11:14 local).
- `d89d1d73…` after the first hotfix batch (aboard table, places, ports, reckoning, sights, readings), for the whole first half of the Western Islands run.
- `bd09b91e…` after the repair, kedge and well batch (21 Oct).
- `372c899e…` after the `ground.py` change (22 Oct), which is H as it stands now.

### 1.2 Which playtest ran on which version

| When (local, UTC−4) | Scenario | Seats (model, door) | Version | Record |
|---|---|---|---|---|
| 17 Oct | A chasse-marée out of Roscoff | officer | pre-O (`31be2895…`) | save in O's root |
| 18 Oct 04:37–06:22 | The dispatches, Falmouth to Plymouth | captain: Opus 5.5 (MCP, the Claude Code session "FreeSail connection"); director: Fable 5.1 (MCP); officer: the owner | **O** | save `tick47089`; committed write-up in G `docs/playtests/2026-10-18-dispatches-director-test/` |
| 18 Oct ~07:44 | "A passenger": chasse-marée in Roscoff | captain and director: GLM-5.3-flash (API); the owner a passenger | **O** | save `tick279`, about four minutes of play |
| 19 Oct ~04:46 | Merchant brig in Torbay, first attempt | director and officer: GLM-5.3-flash (API) | **O** | save `tick52`; stood down within 52 ticks |
| 19 Oct ~05:00–11:14 | A merchant brig, free, in Torbay | officer, director and lookout: GLM-5.3-flash (API, OpenRouter) | **B**, then B + no-budget brief | saves `tick24406…24833`; H-root `merchant-brig-salt-from-torbay.json` |
| 19 Oct ~07:40–08:12 | Same scenario, "first voyage" | officer: Fable 5.1 (MCP) | **B** | save `tick4590` = `seven-brig-first-voyage.json`; no local Claude Code transcript survives |
| 19 Oct 21:34 → 22 Oct 01:03 | **The Western Islands run** (cutter, Falmouth → Ponta Delgada → Horta, bound for Madeira) | captain: the owner; director: Opus 5.5 (MCP, the "Sailing game scenario design" session); officer: GLM-5.3-flash (API), then claude-sonnet-5-5 (API) after OpenRouter credit ran out at t1643135 | **H**, three builds as above | the director's Claude Code transcript (32 MB); saves `tick291…2339132`; H-root cutter saves |
| 22 Oct 01:49–06:35 | **A fishing chasse-marée in Roscoff** (the lugger) | captain: the owner; officer: Opus 5.5 (MCP, "Freesail-officer setup"); director: Opus 5.5 (MCP, "Freesail-director setup") | **G** | two Claude Code transcripts; saves `tick172912/172959`; G-root `fishing-lugger-anchored-in-Berthaume.json` |

There's no ambiguity left in this mapping. Every save's stamp matches exactly one tree.

### 1.3 What was read, and how

- **Four Claude Code transcripts**, snapshotted read-only into `work/transcripts/` and condensed to readable logs in `work/condensed/`. Every user and assistant line is kept; tool calls are kept with their inputs; results are truncated, and stand-by samples are cut to 900 characters.
- **The saves**, turned into chronological play logs in `work/saves-extracted/`. These interleave the captain's orders, non-routine log lines, every seat's replies and calls, the world orders, and the seats' journals. The save keeps a model's *replies*, not the samples it was sent.
- **Code**: three-way diffs B→H, B→G and G→M, with line endings normalised (`work/diffs/`).
- **Sixteen parallel reviewers**, one per slice, each under the same brief (`work/reviews/BRIEF.md`):
  - two code reviews of the hotfix
  - six slices of the Western Islands director transcript
  - three slices of its officer seat
  - two slices of the lugger officer
  - one of the lugger director
  - one of the 18 Oct runs on O
  - one of the 19 Oct runs on B
- **Rules all reviewers followed:**
  - Read only.
  - No FreeSail MCP tool called; the games are live.
  - No other session contacted, nothing sent to GitHub.

  Their full reports are in `work/reviews/`. This report merges, de-duplicates and checks them.
- **Tests**: run here on M and on an untouched copy of G, side by side on the same machine (§2.4).

**Limits:**
- The playtests are still in progress, so this reviews them as they stand.
- The Fable 5.1 officer run of 19 Oct has no surviving Claude Code transcript. Only its save record remains.
- GLM's and Sonnet's API seats have no transcript outside the save, so what they were sent is inferred from the station brief and the harness code.


---

## 2. Can the latest GitHub version and the hotfix version be merged cleanly?

**Verdict: yes.** The merge is clean in text, clean in lint, and adds no test failures. One mechanical precondition: normalise the hotfix's line endings first. The merged tree is at `M7b-Review-2026-10-22\merged\FreeSail-merged` (fingerprint `10fbc075275a7c52`). It's G plus exactly the 39 files the hotfix contributes, and nothing else.

### 2.1 What each side changed against the common base B

| | Files changed | Of which code (`freesail/`) | New files |
|---|---|---|---|
| **Hotfix (B→H)** | 33 changed + 6 new | 12 | `tests/test_aboard_found.py`, `data/director/briefs/interesting-passage-nobudget.yaml`, 4 consent records |
| **GitHub (B→G)**, package 66 and its records | 29 changed + 1 new | 16 changed + `hearing.py` | `freesail/world/hearing.py` (and a local consent record the lugger run wrote into G's folder) |
| **Both** | **8** | 3 | |

The eight files changed on both sides:
- `freesail/world/orders.py`, `freesail/api/readings.py`, `freesail/agents/tools.py`
- `tests/test_director.py`, `tests/test_agents.py`, `tests/test_known_truths.py`
- `docs/primer/20-the-director.md`, `docs/dev/TuningNotes.md`

### 2.2 The textual merge (base B, ours H, theirs G; `git merge-file --diff3` per file, no repository)

- **25 files** changed only by the hotfix: taken from H.
- **6 new files** from the hotfix: added.
- **7 of the 8 shared files** merged automatically with no conflict.
- **1 conflict**, `docs/dev/TuningNotes.md`: both sides appended sections at the end of the file, over an empty base region. I resolved it by keeping both, package 66's record first (it's dated earlier on 19 Oct), then the hotfix's five sections.
- **Proximity check.** In every shared code and test file, no hotfix hunk falls within 15 lines of a package 66 hunk (`work/scripts/hunk_proximity.py`). The two sides touch unrelated parts of each file.
  - `orders.py`: the aboard table (H) against the hold named and the `say as` by station (G).
  - `readings.py`: the well reading and the broken glass (H) against the station's line (G).
  - `tools.py`: the grammar topic's starter-book note (H) against who-heard tails and the stand-by text (G).
  - The only near pair is in primer 20, two paragraph edits 14 lines apart. Both survive intact.

### 2.3 The one precondition: line endings

**Thirteen of the hotfix's files were rewritten wholesale from LF to CRLF**:
- `freesail/standing/grammar.py`, `freesail/world/ground.py`
- `tests/test_agents.py`, `test_known_truths.py`, `test_orders.py`, `test_orders_m4a.py`, `test_python_api.py`, `test_replay.py`, `test_standing.py`
- primers 06, 07, 10, 11 and 13

The repository is LF throughout, and its `.gitattributes` has no blanket `text=auto`. Merged as they stand, these files make `test_agents.py` and `test_known_truths.py` conflict *as whole files*, and every one of the 13 shows as a full-file diff. Normalised to LF (which the merged tree is), they merge cleanly and the real diff shrinks to a few lines each.

The rules fingerprint ignores line endings by design, so the game never noticed. Git and any reviewer would.

**For the lead:** commit the hotfix with LF endings. Consider adding `* text=auto eol=lf` to `.gitattributes`, keeping the existing `-text` exceptions.

### 2.4 Tests: the merged tree against an untouched G, same machine, same run

| | Whole suite, fast and slow tiers together (`--slow -m "not pace"`, `-n 10`) |
|---|---|
| **G (untouched copy)** | **3,807 passed**, 9 failed, 11 xfailed, 4 skipped (25 min) |
| **M (merged)** | **3,819 passed**, 9 failed, 11 xfailed, 4 skipped (25 min) |

- **The same 9 tests fail on both, with identical assertions.** The 12 extra passes on M are the hotfix's new tests. The merge adds no failure.
- **The 9 are pre-existing in G on this Windows machine:**
  - Two are Windows-only: the scenario maker's error text carries `data\ships\…` where the test expects `data/ships/…` (a real, minor Windows bug in a player-facing message), and truth 7b-108 captures no harbour banner.
  - Seven are pinned constants or digests that differ: the merchant passage at seed 7, the schooner on an intent, the schooner's octant passage, truths 77, 78 and 79, and the Ushant lee-shore captain trial. The hotfix session met the same seven on 20–21 Oct, confirmed they fail with its own changes undone, and deferred them.
  - CI runs Windows on the *fast* tier only; the slow tier runs only when dispatched by hand. Nobody has checked whether these seven hold on Linux and not on Windows, which would be a cross-platform determinism problem for replays. They may instead have drifted on every platform. **The lead should dispatch the whole suite on both runners.** I didn't, because this review stays off GitHub.
- **Ruff:** `ruff check` and `ruff format --check` are clean on M (217 files).
- **An earlier fast-tier-only run** (in `work/testruns/*-fast.txt`) showed 4 failures in both copies, all from the environment, not the code:
  - three from my own copy step, which had dropped the `*.checkpoint` fixtures;
  - one fingerprint-timing test (0.5 s budget, 1.4–2.4 s under the load of two suites and sixteen reviewers).

  I restored the fixtures, and the whole-suite run above, which includes the fast tier, passes all four.

### 2.5 Things to decide when this goes to the lead

1. **The no-budget brief** (`interesting-passage-nobudget.yaml`) is a sixth starter brief. The hotfix loosened `test_the_starter_briefs_load…` to "the five starters present, extras allowed" on the owner's word (21 Oct 09:25Z). Keep the brief in `data/`, or move it to the owner's AppData scenarios.
2. **The consent records.** The repository keeps them under `docs/agents/consent/`.
   - **In the merged tree:** H's four (19–20 Oct: Fable 5.1, Opus 5.5, GLM-5.3-flash, claude-sonnet-5-5), and the lugger run's Opus 5.5 record of 22 Oct. The lugger run wrote that one into G's folder locally, and the merged tree was built from that folder.
   - **Not in it:** the 18 Oct records.
     - The GLM record the game actually used, the plain yes of 07:43:29, survives only in the director session's snapshot.
     - `-old` holds the Fable 5.1 and Opus 5.5 records of that day and GLM's three earlier answers, which the owner deleted from the live folder.
   - The owner should say which go in (§8.4).
3. **The rules fingerprint moves** to `10fbc075275a7c52`. Saves made on H (`372c899e…`) or G (`e19ddb85…`) will load under M as "another build's save". The game's own build-words cover that.
4. **Not in the merge**:
   - the owner's `M7b Notes.txt` (viewer notes; see R-59);
   - `.mcp.json` (identical on both sides);
   - the play saves in H's and G's roots.


---

## 3. The hotfix work, reviewed against the latest version, the design proposal and the M7b spec

The director session ("Sailing game scenario design", Opus 5.5) wrote everything in H between 19 and 22 Oct, on the owner's word, between packages. It worked in three batches, each followed by live play.

| Batch | When (UTC) | What | Asked for by the owner |
|---|---|---|---|
| **1** | 20 Oct 00:06–01:08 | **The things found aboard, widened.** `data/director/aboard.yaml` went from 4 things to 24, with the effects and plausibility checks in `world/orders.py`. Foul water now clears on watering (`ports.py`). Losses are written with their cause in `places.py`, `reckoning.py` and `sights.py`. The broken glass and the stopped chronometer are read by `api/readings.py`. New test file `tests/test_aboard_found.py`; primer 20 updated. | "see if we can add some more things that the director can find aboard"; "back up files first, add tests, and run the relevant tests" |
| | 20 Oct 01:08–01:30 | **Four scenarios**: `western-islands-run`, `free-trade`, `inshore-squadron` and `lisbon-letter`, in AppData, all at 9999/9999 budgets. | "draft the actual scenario and director brief … and a few others"; the 9999 budget ruling |
| **2** | 21 Oct 04:38–11:57 | After the grounding:<br>- **The hull's repair**: `aboard: the leak stopped`, `aboard: the well pumped out`.<br>- **Kedging off**: the heave-off and grip rule in `world/ground.py`; kedge layout allowed aground (`evolutions/scripts.py`); an anchor hove in aground drags home (`physics/anchor.py`).<br>- **The well, sounded**: `sound the well` has the carpenter sound it (`orders/__init__.py`); `the well` becomes a reading; the starter book's held `sound the well` order removed.<br>- **The starter-brief test loosened.**<br>- **Three known-truth passages re-pinned.** | "add the leak-stopped and well-pumped-out director hotfix with tests"; "the honest and conservative implementation" of kedging; "removing the standing order 'sound the well' from the starter book"; "change the starter-brief test to check the five starters are present and allow extra briefs" |
| **3** | 22 Oct 00:47 | **The checkpoint crash fixed.** Class-level defaults on `Ground` (`_anchor_dist`, `_came_home_said`), after the restored game's clock thread died. | The owner reported "the clock is stuck" |
| | 21–22 Oct | **TuningNotes**: five sections, among them "Open, for the lead". | "Leave it for now, note it for the lead session" |

### 3.1 Overall verdict

**Sound, faithful to what the owner asked, and in the project's idiom.** The two code reviewers (CR1 and CR2, full reports in `work/reviews/`) found no correctness defect that breaks play in anything the hotfix wrote. The most serious problem, the checkpoint crash, was found in play and fixed within two minutes.

Play confirms the hotfixes work:
- The kedge was laid out aground and she was "hove off by the kedge, and afloat again on the flood".
- `sound the well` and the well reading worked first time.
- The director pumped the well out 16 times, which is consistent with the leak.
- The watering cleared the foul casks.
- `aboard: the leak stopped` was never used live; only its test covers it.

The re-pins are justified. Each of the three moved passages (gate 5a's day 625→623, gate 5b's 733→731, the thick passage 471→469) follows from the owner's ruling to drop the starter book's held well order, which removed two "held" lines from every passage that reads the book. The session proved it by bisection: it restored the old reading and the old order together, and the old pins came back. The kedge and anchor changes moved no pin.

### 3.2 Against the spec and the design proposal

| Area | Spec / design | Verdict |
|---|---|---|
| The widened aboard table | M7b §3 (aboard as a world order with plausible causes and the doubt); §4 ("nothing found aboard that would kill"); §17a (losses written with their cause, "transactions, not variables"); §19 (water and provisions) | **Conforms.** Every new thing has a plausibility rule and a doubt, a `harm` level, a report in a period voice, and an effect on a modelled quantity where one exists ("nothing modelled yet" said honestly where none does). The water-clears-on-watering fix is §19's own rule. |
| The repair (leak stopped, well pumped out) | §3 decision 50 (plausible causes); §17a; DesignProposal §3.4 item 7 (taking on water; `NotesForM7.md` puts it in M7) | **A labelled stopgap**, as the owner approved. It sets two variables at once, with no time or hands, and `leak_stopped` is accepted on a rock (CR1 F4). Acceptable until the pumps and the carpenter come with M7's "taking on water". Recommend a doubt while `grounded.rock`. |
| Kedging off | DesignProposal §1 ("honest"), §3, §9 ("kedging off"); M5 §18 (anchors and ground) | **Conservative and deterministic, as ruled, but binary in practice.** A kedge holds at most about 0.9 kN against about 2.7 kN of grip per centimetre for the cutter, so its whole effect is waiving the 0.3 m afloat margin. It gains the time the tide takes to rise a foot (CR2-03). The docstring's claim that the kedge "keeps her from being driven further on" describes nothing the game models. Primer 13's recipe (`heave in the kedge to twenty fathoms`) drags the kedge home instead of hauling the hawser taut, because there's no heave-taut and hold (CR2-02, D7-05). M7 (taking on water and damage) should bring capstan purchases, the launch carrying out a bower, and lightening. |
| The well as a reading | M7b §11–13 (the observed world: readings, not truth); M4 §24 (33c's held orders) | **Conforms** to the observed-world rule. It leaves package 33c's held-order mechanism with no absent reading and no test (CR2-09). |
| Places, ports, reckoning, sights | §17a, §19 | **Conform.** These are small corrections of losses and causes. |
| Tests | The project's pin practice (old values kept in comments) | **Adequate.** Good comparative design in `test_ground.py` (same seed, with and without the kedge). Gaps: no test restores an old checkpoint; nothing on the let-go sequence, a kedge laid toward the shoal, or the well after pumping. Some earlier-value chains were cut from the pin comments: "729 at 57", `5f682b…` at 57, "495 at 37p", `e358…` at 45 (CR2-06). |

### 3.3 What must change before the hotfix is folded into G

1. **Fold in from the merged (LF) tree, not from H's files** (§2.3). The CRLF conversion came from the session's `py - <<'EOF'` scripts calling `Path.write_text` without `newline=` (CR2-10); the Edit tool's edits stayed LF.
2. **Add a regression test for the checkpoint crash.** Build a `Ground` with `__new__` (or unpickle a pre-hotfix one) and tick it aground with a taut cable. Adopt the rule that every attribute on a checkpointed class gets a class default (CR2-05, D7-01).
3. **Correct the TuningNotes' cause for the seven failing pins.** The notes blame "the 2026-10-19 evening changes to `ports.py`, `reckoning.py`, `places.py` and `sights.py` (package 65's era)". Those are this session's *own* batch-1 edits, made at 20 Oct 00:09 UTC: it read local file times as UTC. The same seven fail on an untouched G (§2.4) and on the session's own pristine copy. The session also proposed a session card, "Re-pin the known truths moved before 21 Oct", whose brief sends the lead after the same wrong files. **Re-scope it** (CR1 F2, CR2-07).
4. **Fix the stale `man the pumps` refusal** in `data/vocabulary.yaml:1923`. It still says the well is not sounded, and play hit it. Fix the stale comments in `orders/prompt.py`, `standing/grammar.py`, `standing/runtime.py` and `standing/rules.py` too (CR2-08).
5. **The kedge-home line fires one minute after let-go**, before anyone heaves. `LayOutKedgeScript` sets the scope from the depth at the *ship*, so the first depth refresh over-stretches the hawser (CR2-01). Let the kedge go with scope ≥ hypot(out, depth at the kedge), and say "comes home" only while a heave on it is in hand.
6. **Put the new things in the director's station brief.** `DIRECTOR_BRIEF` still names only the original four aboard things (CR1 F3). Also fold the widening into spec §3's as-built text and primer 20's doubt table (CR1 F16).
7. **Fix the milestone named for the pumps.** In six places the hotfix calls the pumps and the carpenter's work "milestone 8's": `aboard.yaml` (twice), TuningNotes (twice), `readings.py` and `standing/grammar.py`. G's `docs/design/NotesForM7.md` puts "Taking on water" (leaks, pumps, foundering) in **M7**, and the roadmap's M8 is "Obscure kit and polish". Say M7, or "with taking on water".
8. **Owner's decisions:**
   - the no-budget brief: its comments contradict its values (45 kn against "nothing above force 7"; a frigate against "no heavier than a brig"), and it shares the starter's name (CR1 F18);
   - the consent records (§2.5).
9. **Lower priority:**
   - the well reading appears in every sample of every ship's stations (CR1 F10);
   - "hove off by the kedge" is said for any taut cable (CR2-04);
   - the chronometer report says the master "has it wound" when the game keeps it dead until ordered (CR1 F5);
   - provisions doubts count from the voyage start, not the last victualling (CR1 F7);
   - `orders.py` writes `Ground`'s private fields (CR1 F11, CR2-14);
   - an unknown `harm` value isn't checked at load (CR1 F12).

### 3.4 Process notes for future live-hotfix sessions

- **Bisect in a copy.** The session's bisection appended to `starter.orders` and ran `sed -i` on `anchor.py` in the folder the live game runs from, restoring each with `cp` (21 Oct 10:19–11:27 UTC). Both came back clean, but a restart in those windows would have played under other rules (CR2-16).
- **Use UTC, or say the zone, when reading file times.** The misdiagnosis in §3.3 item 3 came from that.
- **Keep the merge base.** The session's "make a copy of the folder for yourself" snapshot and its pristine copy are what let this review rebuild B exactly and confirm it by fingerprint. Keep doing this.
- **Watch the chat during live direction.** The owner noticed that a director in a desktop chat must keep its chat spoiler-free. The session adopted that, and truth-derived hints still slipped into chat on 22 Oct (D8-16). See §5.7.


---

## 4. The playtests, one by one

Finding IDs in brackets point into the reviewers' reports in `work/reviews/`. Each report has the evidence for its IDs (ticks, timestamps, quotes) and the code references. §5 de-duplicates the findings across playtests and ranks them.

### 4.1 18 Oct, on O: the dispatches director test and two short GLM starts (E1)

**What they were.**
- **The dispatches test.** The Claude Code session "FreeSail connection" held the **captain's** station: the cutter *Sherbourne*, Falmouth to Plymouth, t155–t47067. Fable 5.1 was director (MCP) and the owner sat at the officer's seat. G's committed write-up (`docs/playtests/2026-10-18-dispatches-director-test/`) covers it well.
- **Two short starts, neither written up.**
  - "A passenger" (Roscoff, about four minutes): GLM-5.3-flash as both captain and director, the owner a passenger.
  - A first try at the Torbay brig (52 ticks): GLM as director and officer.

**Status of the write-up's 28 findings across the versions.**

| Status | Findings |
|---|---|
| Done in B | 7, 12, 13, 15, 23, and the officer's binding in 8 |
| Done by package 66, **so in G only, not in H** | 2, 4, 9, 17, 18, 19, part of 22, part of 25, and the merchant words in 8 |
| Still open everywhere | 3, 6, 11, 20, 21, 24, 26, 28, and the chart checks |

Because none of package 66 is in H, the Western Islands run met the dispatches test's stand-by findings again on H. Meanwhile the lugger run, on G, shows them fixed.

**New here.**
- **The consent question can trap a model into leaving** (E1-01).
  - GLM answered yes twice, quoting the opt-out token in praise of it, and both answers were recorded "left with the token".
  - Asked again, it answered "yes, with conditions". Its conditions: keep its correction beside the old record, and warn in the question that writing the token, even quoted, leaves.
  - `consent.py` and `ConsentBrief.md` are unchanged from O through G, so the trap is still there.
- **The owner resolved it, and the gate held** (corrected after the owner's account, 22 Oct).
  - The owner deleted the false positives, asked plainly, and got a plain yes. It was written at 07:43:29 on 18 Oct under the freed first name, `2026-10-18-z-ai-glm-5.3-flash.md`.
  - The director session's snapshot of the game folder from that night holds exactly that record ("Yes."): `C:\Users\frenc\AppData\Local\Temp\claude\C--Users-frenc-Downloads-FreeSail-claude-dreamy-darwin-d77nty\6a379c71-a3f8-4819-8805-0ebbc271e5a1\scratchpad\freesail-baseline-2026-10-19\docs\agents\consent`.
  - The Roscoff seating minutes later and the Torbay start the next morning both cite it. **The gate worked as written.**
  - E1-02 had flagged the seats as unexplained because `-old`'s consent folder holds the three earlier records (the two false positives and the conditional), not the plain yes. **`-old`'s consent folder doesn't reflect the state the game ran with.**
- **What remains is a gap in the harness, not a defect in the gate.**
  - There's no supported way to set aside a false positive. Deleting worked, but it also removed the history the record design keeps, including GLM's own request that its correction stay beside the old record.
  - A "superseded" or "false positive" mark the owner can add, kept on file and read past by the gate, would keep both.
  - On B the next day GLM was asked afresh, because records don't travel with the repository to a new folder, and it again said yes.
  - None of the 18 Oct records were committed: the plain yes survives in the snapshot, the earlier three in `-old`.
- **The player at a lesser seat can't read his own state without the deck** (E1-03). The owner, off watch at the officer's seat, was refused `how am I` and `the people`. Package 53b exempted needs and free lines for model stations only; `PlayerSeat.submit` still refuses them. Open in B, G and H.
- **Smaller.**
  - The glass names a frigate's ensign before her kind (E1-04).
  - `fill away` is refused while a heave-to is in progress, and belaying it leaves her aback (E1-05).
  - Anchored, `furl the sails` skips the gaff main, so she dragged, and the urgent veer waited behind the furling (E1-06).
  - A running stand-by can't be re-aimed (E1-07). This recurred in every later run.

### 4.2 19 Oct, on B: the merchant brig in Torbay (GLM in three seats; Fable 5.1 as officer) (E2)

Two runs of "A merchant brig, free, in Torbay", the salt trade, on B before any hotfix. Neither has a Claude Code transcript; this review read the saves.
- **GLM-5.3-flash** (API door, OpenRouter) as officer and director, and for one tick as lookout. About 05:00–11:14 local. The rules fingerprint moved at 11:14, when the owner added the no-budget brief.
- **Fable 5.1** (MCP) as officer for the "first voyage", 07:40–08:12.

**What worked.**
- **Fable 5.1 was an exemplary officer.** It read its primer chapter first, asked the destination before weighing, and checked the chart rather than alter course on a long-range "steady" bearing. Its Portland Race and spring-tide advice was right (12 June 1805 was a full moon), and all seven of its standing orders were accepted first time. Both messages it missed were the game's fault (E2 F7, F8).
- **GLM's directing showed real story sense when the grammar let it**: a lugger seeded honestly over the horizon, a rumour thread through the letter, the harbourmaster and the tavern, and the L'Orient salt temptation the brief asks for.
- **Package 53b's freight form** worked at the first try.

**What didn't.**
- **The director's budget ran out on noise** (E2 F1, high).
  - With `cadence: glass`, the 48-sample budget is exactly the day's glasses, and it was gone by 11:42 ship's time.
  - 42% of those samples were lines not addressed to the director: its own `say as` and `aboard` lines echoing back, the officer's replies, and the captain's words to the officer.
  - The hold fell just as the tally boat came within hail, so the captain's hails went unanswered.
- **The owner couldn't lift the hold in play** (F2, F3).
  - A new brief doesn't clear it.
  - `director: brief samples_a_day 9999` replaced the whole brief with words, dropping its limits and leaving the budget.
  - So the owner wrote `interesting-passage-nobudget.yaml` into the code tree. This is the origin of that file, and of the owner's later 9999/9999 ruling.
- **The far-ship grammar defeated GLM**: 24 of its 29 `ship:` orders were refused (F4).
- **The scenario's "merchant brig" is H.M. brig-sloop *Harpy*** (F6): 121 men including 20 marines, a commander and a surgeon, under the US flag. The director called her "a king's ship", and the owner asked "are we a King's ship?".
- **Context grew unchecked.**
  - About 16.3 million prompt tokens across the two GLM seats in about two hours.
  - `budget_tokens` was the door's 1 M context, so the handover fold never fired (F16).
  - That's the same configuration that ran the Western Islands officer seat into its cut-offs and its credit stand-down.
- **Consent** (F27). GLM had asked to be "first seated in gentler waters", and was seated as officer and director at once. Fable caught a wrong owner-typed identity before answering, and the record keeps neither the wrong brief nor the correction.

### 4.3 20–22 Oct, on H: The Western Islands run (D2–D8, CO1–CO3)

**The longest playtest yet**: 27 days of ship's time, 8 June to 5 July 1805 so far, over about 30 real hours. The owner is captain, Mr Bowen of the merchant cutter *Sherbourne*, carrying wine-trade letters, a sealed letter and freight. Opus 5.5 directs. The officer of the watch, Mr Pearce, was GLM-5.3-flash until OpenRouter returned 402 at t1643135 (27 June), then claude-sonnet-5-5. The run is still going, bound for Madeira.

**The voyage in brief.**
1. **8–14 June** (D2, CO1): out of Carrick Road on a foul westerly. The director's opening was restrained: 14 acts in six days, each with a stated cause. The owners' letter set a deadline the passage had to answer. Pascoe, the boatswain, became an excellent period voice who always handed the decision back to the captain. The GLM mate's arithmetic and period seamanship were mostly excellent, but it treated a lunar as a standing longitude and lost track of whose deck it was (CO1-03, CO1-04).
2. **14–21 June** (D3, CO2):
   - **The meeting with the *Two Brothers*.** The director made her master with `person: make "Captain Tregarthen", …, aboard the Two Brothers, on the quarterdeck`, which put him on the *Sherbourne's* own quarterdeck. The GLM mate then called the owner "Captain Tregarthen" for days (D3-01, high). Afterwards the *Two Brothers* vanished from the truth, probably because the director's `steer` order replaced her goal with a single 60-mile leg (D3-02).
   - **The weather.** The director's Azores high stacked on the climatology's own, and the glass reached 30.70 in (about 1039 hPa) (D3-08).
   - **Stores.** The water was found foul and short allowance came in; only "half the whole" exists, and the owner tried "three-quarters" five times (D3-09).
   - **GLM's slips.** It sent an emoji: the owner found it "hilarious", then told it "never do it again". From 21 June, after two reply-limit cut-offs, GLM's journals turned into copied templates with a stale heading and glass (CO2-03).
3. **22–30 June** (D4, CO2):
   - **The *Lydia*** passed twice unspoken: `steer` doesn't intercept, and holds lapse every half hour (D4-08).
   - **The chase.** A Basque privateer gave chase, within the brief. The fog that ended it was the weather systems', not the director's; the owner was sure it was the director's mercy.
   - **Landfall** at the Azores, then Ponta Delgada.
   - **The reseat.** OpenRouter's 402 stood GLM down and Sonnet took the seat, distrusting GLM's stale notes (CO2-05).
   - **The two routing bugs.** Through this span, Sonnet's reports to the captain were mis-filed (CO2-01, high), and the first word after "Mr Bowen," was dropped. That turned "no land in sight yet" into "land in sight yet" (CO2-02, high).
   - **The director's debrief** at the owner's request (§7).
4. **30 June–2 July** (D5, CO3): toward Horta. The director tried the point of interest (a whale mark) at the owner's asking, and freshened the wind at the owner's approval; it overshot to 22–27 kn at landfall (D5-19). She was taken aback five times at 48–53° apparent (D5-10). **The grounding** followed (below).
5. **2–5 July** (D7, D8, CO3):
   - **The repair.** The restart loaded the repair, kedge and well hotfixes, then crashed on the checkpoint, and was fixed. She was kedged off on the flood at 19:21, 9.6 hours after striking. That long a wait owes something to Horta's tide being Le Conquet's: the Azores gauges are held, not blended, at four times the islands' range (D7-06).
   - **Business at Horta**: Bettencourt, Mr Hale, the sealed letter (never revealed), lighters, and a period-correct copper patch by heeling.
   - **The tide-swing log spam** (D7-02).
   - **The director's stand-down** at 06:45 on 5 July.

**The grounding: what happened, and why no fair warning came** (D5-01/02, CO3-1/2/3/4; verified in code here). At 09:31 on 2 July the lookout's notable "Land right ahead, a mile" woke the officer. Sonnet reconciled it against the named bearings in its readings ("the land is not right ahead but the Point of Espalamaca"). It had not looked at the chart since 08:30.

At 09:32 the captain let go the best bower in 46 fathoms at about 7 knots, with sail drawing. From that moment **one predicate silenced the two things that would have warned the player**. `GroundTackle.at_anchor()` (`ship/parts.py`) is `bool(self.down())`, true when *any* anchor is down, holding or not:
- **The account froze.** `reckoning._riding()` stops the master's account. The captain's chart (drawn by account), the ship mark and "depth by the chart" all stayed at the let-go point while she sailed about a mile onto the Praia. This is exactly the owner's "the map never updating".
- **The lookout went silent.** `lookout._land_ahead` is skipped when `_riding(world)`, so the urgent "land close ahead", due about 09:39, never fired. It was built exactly to M5 §12's words ("not at anchor or aground"). The spec meant a ship that is holding.

Compounding factors:
- `let go` is accepted at 7 knots with no word about way (D5-03).
- The drag alarm's only advice is "veer more cable". The officer followed it, to 240 fathoms, without saying she still had way on (D5-04, CO3-4).
- The captain's "furl all sails" waited behind the veering ("waiting: furling all (its turn)") (CO3-6).
- The inward pilot was put off early. The automatic box-off from irons ran her away from the road at 6 knots, which tripped the outward release rule (D5-06, D5-07).
- The officer stood by "until a word on deck" through the last nine minutes, and the lead the captain had belayed at 09:19 was never restarted (CO3-8, CO3-9).

She struck at 09:43.

The owner owned their part: letting go at speed, belaying the take-in and the lead, anchoring in 46 fathoms. They said they'd have quit if they weren't the developer. The record supports their sense of unfairness. The game removed both of its own warnings at the moment they mattered, and neither the director nor the officer found the cause. The director proposed "live position on the map", which works against the chart-by-account design. The right fix is to make "riding" mean riding (below a ground speed, the anchor holding), and to key the lookout on speed over the ground.

**Officer models compared (CO1–CO3).**
- **GLM-5.3-flash** was atmospheric and careful in its journal, good at arithmetic, and often right in period seamanship. Its weaknesses:
  - bursts of retried orders (CO1-07);
  - backing and veering confused (CO2-10);
  - a false "danger" order claiming the captain was below (CO2-07);
  - 50 hours awake while telling the captain it wasn't tired (CO2-13);
  - after the cut-offs, journals that drifted from the game (CO2-03).
- **claude-sonnet-5-5** was terse, accurate and candid about uncertainty, and deferred properly to the captain. It caught a 17-league landfall error and warned of the Formigas. Its failures were concentrated in the grounding: it talked down a true warning and used the wrong script for a ship dragging under sail. It also carried the wrong lesson ("take full scope in deep water") across the reseat (CO3-10).
- **The fourth seating** (after the restarts) lost the needs lessons ("I'm an AI … I take no meat or drink") (CO3-12). G's station line addresses this.

### 4.4 22 Oct, on G: A fishing chasse-marée in Roscoff (LO1, LO2, LD)

The owner is captain and master, M. Hervé, of the chasse-marée *Éclair*. Opus 5.5 is both officer (Mr Lecoq, "Freesail-officer setup") and director ("Freesail-director setup"). Play ran 10 June 05:00 to 12 June 05:01: Roscoff, the Isle of Bas channel, the Iroise fishing, an onion freight to Brest, and anchored in Bertheaume. This is the first run on G, so the first look at **package 66 in practice**.

**Package 66 worked** (LO1, LO2, LD):
- The station's line came first in every sample and tracked place and deck correctly, and both models used it at once.
- A model's own order ended its stand-by every time (six of six for the officer).
- Journal notes didn't end a stand-by.
- The truth was readable during a wait.
- The "who heard" tails behaved.

The gaps are around it:
- A changed `stand_by` doesn't replace the running one; it's "taken in your turn" and dropped (LO1-05, LO2-04, LD-17).
- The still-waiting reply gives no current time (LO2-03).
- Compound "x or y" stand-bys are in every brief but the officer's (LO1-06, LO2-06).
- The station line's wake time is wrong after a part-sleep (LO2-07).
- The repeated history is untouched (LD-06). That's package 58's, and it measured about 1.3 million characters of wait results in under four hours for 25 acts.

**The lugger itself.**
- **`get under way` sets no lugs** (LO1-01, LD-01, high). It runs the square-rig or fore-and-aft script ("Lay aloft, sail-loosers… Hoist away the topsail"). Both days she was left under the jib alone, a cable off Pergueridre in a narrow channel, and was taken aback.
- **Every chart sounding prints "NaN fm"** (LO1-02). `client/units.js` exports no `FATHOM`; I confirmed it here. The officer piloted off unreadable figures.
- **A lug sheet trim takes 6 hands** and a jib 4, frigate figures. So "not hands enough" woke the officer at nearly every trim and wore out the crew (LO2-09).
- **Fishing readings are refused to the officer**: `the catch` and `the fishing grounds` (LO2-01).
- **The glass can't single out one of two brigs** and doesn't know "lugger" (LO2-02).
- **Hauling the nets took 3 h 39 min** against the file's two hours, with no reason shown (LO2-14, LD-13).
- **The fish-wife's advice contradicted the game's grounds**: mackerel at dusk, where the Iroise data has sardine nets by day (LO1-10).
- **Man-of-war words throughout**: the capstan, boatswain's mates, braces. A Portuguese brig was crewed with a Royal Navy wardroom of English names (LO1-15, LD-15).

**The director (LD)** showed excellent restraint and seed-planting:
- the fish-wife set the goal and the old fisherman the timing;
- the onion freight was done in package 53b's forms, with the consignee made ahead at Brest;
- the placed *Sainte-Barbe* became the mark the crew fished by, unprompted.

Its failures were mostly the grammar's. 37% of its 41 world orders failed, against about 7% for the Western Islands director, who had written the code:
- the `ship:` form defeated a plain request five times (LD-07);
- `person: make … aboard the Sainte-Barbe` put a stranger in *Éclair*'s cabin (LD-02);
- a `[reason]` given on first entry overrode a doubt it never saw, so a man was carried 9 miles ashore in a minute (LD-03);
- the director's existence leaked into the stations' play log through the clock-easing line (LD-04).

It asked, at the end, for a complete grammar, read-only data lookups and a dry run for world orders, in preference to raw file access.

**The owner's chief critique was trim timing** (LO2-20): "making the right orders, but at the wrong time". Every order returns at once and feels finished. The samples carry no deltas, and repeat the same sail lists five ways, burying what changed. That is package 58's work.


---

## 5. The findings, de-duplicated and ranked

This merges more than 350 reviewer findings into the register below. Each row lists the reviewers' IDs, so the evidence is one search away in `work/reviews/`.

**Columns**
- **Pri**: **P0** fix before the next long playtest; **P1** in M7b's close-out or the next package wave; **P2** a later milestone, or already planned.
- **Seen in**: **W** the Western Islands run (on H); **L** the lugger (on G); **O** the 18 Oct runs; **B** the 19 Oct brig runs; **C** a code review.
- **Open in**: the versions where the code is unchanged. B/H/G means it's open in all of them.
- **✔**: I verified it in the code myself, beyond the reviewer's reading.

### 5.1 Navigation and the ship's safety

| ID | Pri | Finding | Seen in | Sources | Open in |
|---|---|---|---|---|---|
| R-01 ✔ | **P0** | **Any anchor down counts as "riding".** It freezes the master's account, the captain's chart and the depth by chart, and it mutes the lookout's land-ahead warning, even while she drags under sail at 7 kn. This is the root cause of the grounding's "no fair warning". Fix: riding = anchor holding and ground speed under a threshold; key the lookout on speed over the ground; add a known truth for letting go at speed off a beach. | W | D5-01/02/29, CO3-1/2 | B/H/G |
| R-02 | P1 | **The anchoring script for a ship with way on.** `let go` is accepted at 7 kn without a word. The drag alarm's only advice is "veer more cable". Sail work waits behind cable work, and `furl` skips a gaff main. | W, O | D5-03/04/05, CO3-6/7, E1-06 | B/H/G |
| R-03 | P1 | **Horta's tide is Le Conquet's.** The Azores gauges are "held, not blended" (package 39e), so the range is about four times the islands'. That gave 9.6 h aground and put the master's epitome about 3 h out against the world. Blend or adopt the gauges before the Azores scenarios are replayed. | W | D7-06 | B/H/G |
| R-04 | P1 | **Tide-swing log spam** (66 notable lines in about 1.5 h). The probable cause: she sheered across a stream-area edge, and outside every area `NO_STREAM` reads `flood=True`. H's "Open, for the lead" gives the wrong cause, and its ten-minute-hold fix would only mask it. | W | D7-02/03/04, D8-02 | B/H/G |
| R-05 ✔ | **P0** | **Every sounding on the chart picture prints "NaN fm"**: `client/units.js` has no `FATHOM`. A one-line fix plus a test. | L | LO1-02 | O/B/H/G |
| R-06 | P1 | **Taken aback too easily.** The cutter was taken aback five times at 48–53° apparent in steady wind, and once under a jib alone. Reproduce from the 2 Jul save. | W | D5-10, D4-15 | ? |
| R-07 | P1 | **Sternway** shows in the officer's readings but not the captain's. | W | D5-08, CO3-21 | ? |
| R-08 | P1 | **The pilot and irons.** The automatic box-off from irons overrode the captain's orders, ran her off the road, and so tripped the inward pilot's release. | W | D5-06/07 | B/H/G |
| R-09 | P1 | **A stale destination** ("the port of St Lawrence") refused "shape a course for Fayal Road". | W | CO3-11 | ? |
| R-10 | P2 | **One light's estimated distance** moves the account 2 miles along the bearing. | L | LO2-11 | ? |
| R-11 | P1 | **Points of interest.** A mark was used as a fixing mark, against the spec. Marks have no removal or lifetime, the glass on a mark is refused, and descriptions double a comma. | W | D5-13/14/15/16 | B/H/G |
| R-12 | P2 | **The course shaper** called a 42° course unlayable for the lugger; a course-line danger named the wrong feature. | L | LO2-10/12 | ? |

### 5.2 Speech, reach and people

| ID | Pri | Finding | Seen in | Sources | Open in |
|---|---|---|---|---|---|
| R-13 ✔ | **P0** | **An officer's words to a player-held captain are mis-filed.** They're logged as "The captain to the captain … (nobody holds the station)" and kept in a journal. `_keep_word` hard-codes the speaker, and the player at the prompt doesn't count as a holder. Every model officer in every run hit it; Sonnet lost about 13 reports, the landfall among them. | W, L, O | D2-06, D4-01, CO1-02, CO2-01/18, CO3-14, D8-01, LO1-03, LD-12 | B/H/G |
| R-14 ✔ | **P0** | **The word after "Mr Bowen," is dropped.** `_split_ask` counts in normalised tokens but slices raw words. "no land in sight yet" became "land in sight yet". | W | D4-02, CO2-02 | B/H/G |
| R-15 | **P0** | **`person: make "…", aboard <another ship>, …` puts him on the player's ship.** Three foreign captains ended up on the *Sherbourne's* quarterdeck and in her people. A place in the make words (on the quarterdeck) can be ignored for "in the cabin". | W, L | D3-01, CO1-01, D4-12, D8-05, LD-02, D5-21, CO3-17, E2 F11 | B/H/G |
| R-16 | P1 | **Names and addresses.**<br>- A full name is refused ("Mr Josiah Hale"; "Mr Hale" works), with refusal words about the deck.<br>- "Say To Madeira" is read as say-to-station.<br>- "Tell Captain Tregarthen" matches the captain station before the person.<br>- "Tell the officer …, you may …" is parsed as a grant, so two of the owner's reminders never reached Fable.<br>- "Brixham" isn't a port to world orders, though play names it everywhere. | W, B | D7-10/11, D8-06, CO3-22, D3-04, CO2-17, E2 F7/F12 | B/H/G |
| R-17 | P1 | **No voice between ships.** The player can't hail or speak to a person on another ship ("a hail is the lookout's"), and the director can't voice a crewed stranger's master within hail. | W, L, B | D3-04, LD-09, E2 F19 | B/H/G |
| R-18 | P1 | **No form moves an unheld person**, between places aboard or ashore (package 65 is adjacent). | W, L | D2-10, D8-09, LD-10 | B/H/G |
| R-19 | P1 | **An officer can't put a report to the captain in its own standing order**, and the refusals contradict each other: they list the stations, then refuse each one. | W | CO1-05, D2-09 | B/H/G |
| R-20 | P1 | **The director leaks into the play log.** "Compression eased to 1x: the director is sampled" reached the officer six times, and the officer's refusals list "the director" as tellable. This is against spec §6 and primer 20. | W, L | D2-07, LD-04 | B/H/G |
| R-21 | P1 | **The director's `say` result says "Your words are in the log under your mark".** They go only to its hidden log. An out-of-character note to the captain reached nobody in the game. Decide whether an explicit player↔director channel is wanted. | W | D2-16, D8-04 | B/H/G |
| R-22 | P1 | **The player at a lesser seat** can't `how am I`, `eat`, `the people` and the like without the deck. | O | E1-03 | B/H/G |
| R-23 | P2 | **Smaller text and voice bugs.**<br>- "in my in the cabin"<br>- the pronoun hard-coded "his"<br>- "wait until you are aboard" said in a boat going ashore<br>- the deck named wrongly after `go to my cabin`<br>- man-of-war speakers (purser, cooper, young gentlemen) on a merchant cutter or a lugger | W, L | D2-12/14, D3-10/11, D4-16, LO1-11/12/15, LO2-08 | B/H/G |
| R-24 | P2 | **The owner has no in-game word to the director**: `tell the director` is refused. The lugger director stood down on the captain's word to the officer. | L | LD-23 | B/H/G |

### 5.3 The harness, the doors and the stand-by

| ID | Pri | Finding | Seen in | Sources | Open in |
|---|---|---|---|---|---|
| R-25 | **P0** | **A cut call re-sends the whole brief.** The desktop and Claude Code client gives up on a tool call at 60 s, against the bridge's default 200 s wait. The bridge sees a disconnect, re-seats, and re-sends the whole station brief (32–41k characters) instead of the result. Package 37g's adaptive wait never engages. Harness.md still says four minutes. Fix: default `--wait 50` in the harbour's MCP config; treat a quick reconnect as a cut call (send the result, not the brief); correct Harness.md. | W | D2-01 | B/H/G |
| R-26 | P1 | **The stand-by re-lists its whole history on every poll**, and the waking sample repeats it. The lugger director measured about 1.3 M characters in 4 h for 25 acts. This is package 58's deltas, still "brief to write". | W, L | D2-02, D3-07, D4-04, D8-03, LD-06 | B/H/G |
| R-27 | **P0** | **The "still waiting" reply gives no current game time or clock speed.** Under compression a model can't tell how stale its picture is. | W, L | D2-11, LO2-03 | B/H/G |
| R-28 | P1 | **A `stand_by` sent during a stand-by doesn't replace it.** It's "taken in your turn" and dropped, and the same-wait check misfires. Plans to tack at a bell were saved only by the captain speaking. | all | E1-07, D5-25, D8-11, LO1-05, LO2-04/05, LD-17 | B/H/G |
| R-29 | P1 | **Turn handling at the MCP door.** The unread-turn guard drops the first call after a turn opens, even a journal note or a helm order, and the batch's second call then runs blind. A captain's word arriving just as the model hands back the floor can be consumed unseen (inference). | W, L, B | LO1-04, D5-27, LD-17, E2 F8 | B/H/G |
| R-30 | **P0** | **Briefs and docs.** Compound "x or y" stand-bys are missing from the officer's brief and the `stand_by` tool description, though the other briefs have them. The MCP seats need "never end your reply while seated". | L | LO1-06/07, LO2-06 | B/H/G |
| R-31 | P1 | **Notable-line noise that wakes stations and burns API credit.** Light-air wind lines flip every 10–40 min; standing-order trims log "not hands enough"; lead casts at anchor, the tide swing and the carpenter's pumped-out lines all wake. GLM was woken about 100 times on one day. Make unchanged recurring lines routine, and add hysteresis. | W, L, O | D3-06, D4-05, CO2-14, E1-09, D7-12, LO2-09 | B/H/G |
| R-32 | P1 | **With `--ease-on-station`, every sample drops the owner's clock to 1x** and nothing restores it. The owner was "speeding up as frequently as I can". | W | D2-08, CO1-11 | B/H/G |
| R-33 | — | **A world order or `truth` sent while standing by is dropped with "Nothing was run".** The director wrote filler `say` lines to open its turns. **Fixed in G by package 66**; seen only on H. | W | D2-05, D3-05, D4-03, D5-24, D7-09, D8-12 | H only |
| R-34 | P1 | **Long API seats, and their cost.**<br>- With `budget_tokens` at the door's 1 M context, the handover fold never fires. The two GLM seats on 19 Oct ran to about 16.3 M prompt tokens in about two hours, with every call resending the history; this bears on the OpenRouter credit that ran out on 27 Jun.<br>- Reply-limit cut-offs, with no context fold after them, so GLM's journals drifted into copied templates.<br>- A reseated director keeps no story beyond its notes, so the reseated GLM invented a contradictory one.<br>- GLM's malformed tool calls became play-log speech.<br>- A forced reseat inherits a stale handover and lapses the captain's grants without telling the player.<br>- A fresh seat loses the needs lessons; G's station line helps there.<br><br>Log the conversation size, fold after a double cut-off, and say in the reseat line which grants lapsed. | W, B | CO2-03/04/05, D4-17, CO3-12, E2 F10/F16/F17 | B/H/G |
| R-35 | P1 | **The truth.** It costs 7–12k tokens a read, mostly far ships. It has no aground state for the player's ship, so the director once journaled "she is NOT aground". Every business ship's `goal` reads "bound for Falmouth". | W, L | D5-26, D7-07, LD-08/19, D3-12 | B/H/G |
| R-36 | P1 | **Stand-by events misfire.** "the anchor weighed" never wakes after `get under way`; "under way" wakes when a second anchor is catted. | W | D2-04, D8-11 | B/H/G |
| R-37 | P2 | **The bridge with Claude Code.** A reconnect result of 49.9 KB was saved to a file the director had to parse. Claude Code backgrounds a running stand-by when the owner types. | W | D2-03, D8-18 | B/H/G |

### 5.4 World orders and the director's tools

| ID | Pri | Finding | Seen in | Sources | Open in |
|---|---|---|---|---|---|
| R-38 ✔ | **P0** | **The brief's `enemy_heaviest: brig` refuses nothing.** No `SIZE_RANK` key fits inside "brig", so a French frigate passes a "no heavier than a brig" brief. This affects the Western Islands run and the chase, dispatches and interesting-passage starters. Only "cutter" is tested. | C | CR1 F1 | B/H/G |
| R-39 | P1 | **Weather systems add and step.**<br>- Overlapping highs add; the glass reached 1039–1041 hPa off Brest and at 43°N in June.<br>- An appended waypoint or system steps in at once.<br>- Highs have no doubt.<br>- The climatology's summer highs drift onto Iberia, so there's no standing Azores high.<br>- Primer 20 explains none of this. | W, L | D3-08, D4-06/07, D5-12, LD-05 | B/H/G |
| R-40 | P1 | **Far ships.**<br>- `steer` replaces a captainless ship's goal, and she is removed at the leg's end; the *Two Brothers*, the *Lydia* and *L'Aiglon* vanished with no reason the director could see.<br>- `give chase` is refused while the refusal lists it.<br>- There's no intercept or "speak her" intent.<br>- Holds lapse after half an hour (**fixed in G** by named holds). | W, B | D3-02/03, D4-08/13, E2 F14 | B/H/G |
| R-41 | P1 | **The doubt and the reason.**<br>- A `[reason]` on first entry overrides a doubt the director never saw: a man moved 9 miles ashore in a minute.<br>- A reason that doesn't answer the doubt still overrides it: a ship put "on the land by the chart".<br>- The doubt is judged before the order's form is checked, so a malformed order comes back only "doubted", and a small model took it as a working template. | L, B | LD-03, E2 F5/F15 | B/H/G |
| R-42 | P1 | **The forms the directors asked for.** Scheduled or conditional world orders (top ask); stores received; giving to and taking from unheld people; removing a thing; selling goods; bare shillings and pence; freight vs. own venture; debts on delivery. | W, L | D8-07/08/10/14, D5-20, LD-14/20 | B/H/G |
| R-43 | P1 | **The `ship:` form defeats directors.** 24 of GLM's 29 `ship:` orders were refused, 13 tries for one lighter; 37% of the lugger director's orders failed.<br>- "small fishing lugger", "a French lugger" and "whaler" aren't descriptions.<br>- A colours clause ("British colours", ", colours shown") breaks the parse.<br>- Intents with commas aren't peeled, and a port in the "of" slot is refused.<br>- The ground must be named, and a harbour departure "crosses the land".<br>- The error messages blame the wrong clause. | W, L, B | LD-07, D4-10, E2 F4 | B/H/G |
| R-44 | P2 | **Crew names exist only for English, American and French.** A Portuguese merchant gets a Royal Navy wardroom. | L | LD-15 | B/H/G |
| R-61 | P1 | **The director's budget is spent on noise, and a spent budget can't be lifted in play.**<br>- With `cadence: glass`, a 48-sample budget is exactly the day's glasses.<br>- 42% of GLM's samples were its own `say as` and `aboard` lines echoing back, the officer's replies, or the captain's words to the officer. The hold fell just as the tally boat came within hail.<br>- A new brief doesn't clear `held_until`.<br>- `director: brief <words>` replaces the whole brief, dropping its limits (`nobody_dies` among them), and leaves the budget.<br>- This is why the owner wrote the no-budget brief into the code tree, and later set 9999/9999 everywhere.<br><br>Wanted: don't wake the director on its own lines; a budget command; `set_brief` clears the hold. | B | E2 F1/F2/F3/F18 | B/H/G |
| R-62 | P1 | **`send the launch ashore with the captain and Mr Pearce` silently drops both passengers.** The errand fell back to "for the prices", and the owner waited about 1 h 40 min for a boat. There is only one boat for port business. | B | E2 F9/F20 | B/H/G |

### 5.5 The lugger and fishing

| ID | Pri | Finding | Seen in | Sources | Open in |
|---|---|---|---|---|---|
| R-45 | **P0** | **`get under way` has no lug branch.** It looses topsails and braces head yards, sets the jib alone, and left her taken aback a cable off Pergueridre, twice. | L | LO1-01, LD-01 | B/H/G |
| R-46 | P1 | **Lug and jib sheet trims take 6 and 4 hands**, frigate figures. "Not hands enough" fires at nearly every trim. | L | LO2-09 | B/H/G |
| R-47 | P1 | **`the catch` and `the fishing grounds` are refused to the officer**, and the refusal's remedy fails too. | L | LO2-01 | B/H/G |
| R-48 | P1 | **The glass can't single out one of two brigs** (bearing qualifiers are refused), has no "lugger" rig word, and "her" means the nearest sail. | L | LO2-02 | B/H/G |
| R-49 | P2 | **Smaller lugger and fishing items.**<br>- The haul took 3 h 39 min against 2 h, with no reason shown.<br>- No "ride to the nets" posture.<br>- `heave to` leaves the flying jib drawing.<br>- `shake out the reefs` is refused.<br>- The director's fish talk isn't drawn from the grounds tables.<br>- Square-rig words in the lugger's log. | L | LO2-14/15/19, LO1-10/15/16 | B/H/G |

### 5.6 Consent

| ID | Pri | Finding | Seen in | Sources | Open in |
|---|---|---|---|---|---|
| R-50 | P1 | **Consent.**<br>- **A model can leave by quoting the opt-out token while praising it** (GLM, twice). Add the warning GLM asked for; consider recording "no reason given" when the token sits in quotation marks or backticks.<br>- **There's no supported way to set aside a false positive.** The owner's remedy (delete the false positives, ask plainly, a plain yes at 07:43:29 on 18 Oct) worked, and the gate behaved correctly. But it removed the record history, including GLM's request to keep its correction beside the old record. Add an owner's "superseded" mark.<br>- **Records don't travel to a new folder.** On B, GLM was asked afresh. It asked to be "first seated in gentler waters", and was seated as officer and director at once.<br>- **An MCP identity is the owner's typed name.** Fable caught a wrong one, and the record keeps neither the wrong brief nor the correction.<br>- **None of the 18–20 Oct records are committed.** For 18 Oct, the plain yes is in the director session's snapshot; `-old` holds only the earlier three.<br><br>E1-02's "unexplained seating" is resolved by the owner's account and the snapshot. | O, B | E1-01/02, E2 F27 | O/B/H/G |
| R-51 | P1 | **The consent brief still calls the director "to come"** (package 55). | W | D2-21 | B/H/G |

### 5.7 Needs, the player's experience and the director's manners

| ID | Pri | Finding | Seen in | Sources | Open in |
|---|---|---|---|---|---|
| R-52 | P1 | **Short allowance has one level**, "half the whole". There's no three-quarters, two-thirds ("six upon four") or water-only. | W | D3-09, CO2-16 | B/H/G |
| R-53 | P1 | **Spoilers in the owner's chat.** A director in a desktop chat narrated plans and truth-derived positions to an owner who is also the captain. Add a brief rule: plans and truth in the journal only, and owner questions phrased without world detail. | W | D4-19, D8-16 | brief |
| R-54 | P2 | **A chase with no good options**, as combat and signals aren't in yet. Meanwhile a director brief could name non-combat outs (colours, bluff, a fort). | W | D4-20 | planned (M7, signals) |
| R-55 | P2 | **Smaller needs items.** Tavern food feeds nobody. Sleep repays eight to one (2 h asleep → "rested"). The station line omits a need's first step. | W, L | D5-23, LO1-20/21 | B/H/G |
| R-63 | P1 | **"A merchant brig, free" is H.M. brig-sloop *Harpy*.** The ship file has 121 men with 20 marines, a commander and surgeon, a Navy ration and a 32-ton hold, under the US flag. The director called her "a king's ship", and the owner asked "are we a King's ship?". Package 66's merchant words don't cover a commander-bound ship. A merchant brig needs her own ship file. | B | E2 F6 | B/H/G |
| R-56 | P2 | **Scenarios.** Near-homonym principal names (Pascoe and Pearce) misled the owner twice. The Roscoff purse contradicts its own brief. The inshore squadron starts heading for Ushant's rocks, and the rules captain acts before the player's first order. | W, O, C | D2-20, CO1-16, E1-12, CR1 F19 | scenario files |

### 5.8 Records, docs and the test estate

| ID | Pri | Finding | Seen in | Sources |
|---|---|---|---|---|
| R-57 | **P0** | **H's "Open, for the lead" list exists only in H.** It gives the wrong cause for the tide swing (R-04) and for the seven failing pins (§3.3). It omits, among others, R-25, R-26, R-21, R-15, R-03, R-35 (aground), the checkpoint lesson, the turn traps and the directors' top ask (R-42). Carry it to G, corrected and completed from this report. | W | D7-04, D8-19, CR1 F2, CR2-07 |
| R-58 | P1 | **Seven pinned truths fail on this Windows machine** in an untouched G, and two Windows-only tests fail. One of those exposes a player-facing `data\ships\…` path in the scenario maker's error. CI runs the slow tier only when dispatched by hand. Nobody knows whether these are cross-platform determinism problems or drift. The lead should dispatch the whole suite on both runners. | (tests here) | §2.4 |
| R-59 | P1 | **The owner's viewer notes on the lugger** (`M7b Notes.txt`, 18 Oct) appear nowhere in G's docs:<br>1. progressive hoists drawn over ticks<br>2. the lug passing through the mast at some angles, and a vertical seam<br>3. topsail tacks to the mast vs the lower yard<br>4. reefing doesn't show<br>5. the jib clipping the fore lug<br><br>The lugger officer's ship view on 22 Oct showed a line across a reefed lug, which may bear on note 4 (LO2-21). | (owner) | `M7b Notes.txt`, LO2-21 |
| R-60 | P2 | **Docs that lag.**<br>- Harness.md's "four minutes".<br>- Spec §3's as-built text; primer 20's doubt table; primer 13's kedge recipe.<br>- The `aboard.yaml` wording ("the less" for "sooner").<br>- Primer 6's "1 June" start, which Fable copied.<br>- The merchant-brig scenario's header, copied from the merchant passage.<br>- The garbled gerunds in "By the officer" lines ("howing am i").<br>- The owner didn't know the standing-order book is his to read (UX).<br>- The hotfix labels the pumps "milestone 8's" in six places, where `NotesForM7.md` has taking on water in M7 (checked here). | W, C, B | D2-01, CR1 F16, CR2-02/17, E2 F24/F25/F26/F28 |


---

## 6. Against the design proposal, the M7b spec and the milestones to come

### 6.1 What M7b set out to prove, and what these playtests show

**Spec §1:** "A model above the game shapes a voyage through world orders alone, within a brief the player wrote, on a budget, and the record of what it did and why is a second story read after the voyage."

| Part of the claim | Evidence | Verdict |
|---|---|---|
| **A model shapes a voyage through world orders** | The Western Islands run: 27 days, 258 world orders (about 7% failing), 139 `say as`, 24 uses of the hand. The lugger: 41 orders. GLM on B: 49. In both Opus runs the reviewers rate the craft highly. The director kept restraint: "The best directing turned out to be mostly restraint." It planted foreshadowed causes, and it handed decisions back to the player through voices like Pascoe. | **Shown, for a strong model.** The grammar is the binding constraint. A director that hadn't written the code failed 37% of its orders, and GLM failed 61%. The `ship:` form (R-43) and the person forms (R-15, R-18) cost the most. |
| **Within a brief the player wrote** | The limits held where they were tested: wind capped at 40 kn, nobody died, and the rule of reach refused `say as` the held captain. But **"no enemy heavier than a brig" has never been enforced** (R-38). Briefs can't be edited in play without losing their limits (R-61). | **Partly.** The channel enforces the limits it can parse; one common limit doesn't parse. |
| **On a budget** | GLM's 48-sample budget was spent on noise by mid-morning (R-61). The owner then ruled 9999/9999 for every scenario: "nearly infinite is fine … constrained as playtesting shows". The lugger director's station line printed "2 of 9999" in every sample (LD-18). | **Not yet a working constraint.** The budget counts wakes the director didn't ask for. It needs `cadence` headroom, no self-echo wakes, and a way to change it in play before it can be tuned. |
| **The record is a second story read after** | The journals are rich: the directors journaled their plans, their own slips and the lessons learned. The owner stayed unspoiled by not reading the chat, and asked for the director's account at the end. | **Shown**, with a leak: a director in a desktop chat narrates to an owner who is also the captain (R-53). The record itself (the journal and the hidden log) works. |

### 6.2 The gate 7b outline (spec §23) against what has been played

| Gate item | Played? | Notes |
|---|---|---|
| A directed quiet passage on a **local** model | **No** | Every director in these runs was hosted (Opus through MCP, GLM through OpenRouter). The local runner (llama-server) wasn't exercised. |
| A directed quiet passage on a **hosted** model | **Yes** (and much more than quiet) | The Western Islands run; the lugger; GLM on B |
| The director's log read after | Partly | The owner read the director's chat account; the game's reveal of the hidden log wasn't the path used |
| An observed world for a day with the business on | Yes | The lugger (Roscoff and the Iroise business); the Western Islands' Horta business |
| The player ashore, and in the cabin | Yes, at Horta, Roscoff and Brixham | The player at a lesser seat can't do his own needs off the deck (R-22). There's one boat for port business (R-62). |
| A day's fishing in the smack, the catch sold | Fishing yes, in the chasse-marée | Selling the catch isn't seen in this material. The haul ran long without saying why (R-49). |
| The glass on a near ship | Yes | It can't single out one of two ships (R-48) and names an ensign before a frigate (E1-04) |
| A game started from the harbour with a scenario the maker wrote | Yes | Four scenarios by the director session, the owner's own lugger and brig scenarios |
| A drafted manifest's trade | Yes | 53b's freight form worked first time on B. Money due on delivery is only words (R-42). |
| A week's needs | Yes, three weeks | Foul water, short allowance, hunger and fatigue all met in play. Allowance levels (R-52). |
| The regatta's course with a director above it | **No** | |

### 6.3 Spec deviations found (behaviour contrary to the spec's words)

| Spec | Says | Observed | Register |
|---|---|---|---|
| M7b §4 | "its limits are enforced by the channel, not trusted to the model" | `enemy_heaviest: brig` refuses nothing | R-38 |
| M7b §6, primer 20 | The director is hidden: nothing of it in the play log | "Compression eased to 1x: the director is sampled" reaches the stations; refusals list "the director" | R-20 |
| M7b §5 | "The owner's compression is untouched" | With `--ease-on-station`, every sample drops it to 1x until the owner re-speeds by hand | R-32 |
| M7b §3 (weather) | "a change the systems could make from where they are" | An appended waypoint or system steps in at once; overlapping highs add past any season's ceiling | R-39 |
| M7b §3 (doubt) | Doubted, then "entered again with a [reason]" | A reason on first entry overrides a doubt never shown; a reason that doesn't answer the doubt still overrides it | R-41 |
| M6 45c | A mark is "the world's … not the chart's" | The master fixed by cross bearings on a mark's true position | R-11 |
| M7b §8, §14 | A person is made aboard (the player's ship) or ashore | "aboard <another ship>" lands on the player's quarterdeck | R-15 |
| M7b §17 (equal reach), §9 | A word reaches a person within hail; the captain held at the prompt counts as held | The officer's word to the player-captain is kept for "nobody" | R-13 |
| M5 §12 | Land-ahead "with way on over the ground and **not at anchor**" | Built to the letter, but the letter is wrong for a ship dragging under sail. **The spec should change.** | R-01 |
| M7b §5 (package 66) | "Nothing is dropped … but while the station is paused" | The unread-turn guard drops journal and helm calls | R-29 |

### 6.4 The design proposal's pillars, as the playtests tested them

- **Honest simulation (DesignProposal §1, §3).**
  - Honoured where it counts: the grounding was real, the kedge conservative, the needs bite, and the weather is the systems' own.
  - The honesty failed in the *information* the game gives about its own state. The chart froze, the lookout fell silent, sternway was hidden, the truth didn't say aground, and a "still waiting" reply gave no time.
  - The owner's frustration at the grounding wasn't with the realism ("I did ask for uncompromising realism"). It was with a world that stopped telling them the truth at the moment it mattered. That's R-01's real weight.
- **Orders in a period language (DesignProposal §4).**
  - Claude models mostly recovered from refusals, as the owner observed ("they see the proper way … from the refusal language"). GLM retried in bursts.
  - The friction is concentrated in the director's forms (`ship:`, `person:`), in names and addresses (R-16), and in missing everyday verbs: ring the bell, send a letter, pawl the capstan, heave taut, send a hand aloft, shake out the reefs.
  - The owner's own view: "Accepting a very large range of grammar is definitely a good goal".
- **LLM integration with consent and welfare (DesignProposal §7).**
  - The consent harness has one live trap: quoting the token leaves. It has no supported way to set a false positive aside (R-50). The owner resolved GLM's case by asking plainly, and the gate held.
  - The welfare design worked as intended: models' reports of their experience were candid, varied, and taken seriously by the owner (§7).
- **Presentation (DesignProposal §6).**
  - NaN on every sounding (R-05).
  - The owner's lugger viewer notes are untracked (R-59).
  - Sternway is missing from the captain's view (R-07).

### 6.5 What these findings ask of the planned packages and milestones

| Package or milestone | Status in G | What the playtests add |
|---|---|---|
| **58: the sample's deltas, `ahead`, the cost of thinking** | brief to write | **The single most-demanded change.** The repeated stand-by history (R-26), the owner's trim-timing critique (LO2-20: "making the right orders, but at the wrong time"), the five-fold sail lists, and the token cost of every seat (about 1.3 M characters in four hours for a director; 16 M prompt tokens in two hours for two GLM seats). Recommend briefing it next, and putting R-27 (time in "still waiting") and R-28 (replace a stand-by) in its scope. |
| **51: the observed world, focus, ships' logs** | brief to write | The truth's cost and missing aground state (R-35); director-made ships vanishing with no story (R-40); confirming a sighted ship is one's own (LD-19). |
| **55: the solo director, the consent revision, the gate** | brief to write, last | R-50 (the token trap, a supported way to set a false positive aside, records that travel, the identity typo kept nowhere) and R-51 ("to come"). The local-model directed passage the gate wants hasn't been run. |
| **65: the place's knowledge** (provisional) | brief after the owner's testing | Words heard on the quay reached the mate in the tavern (LD-11); people can't be moved between places (R-18). |
| **61: the land-avoiding route** (provisional) | to plan | Far ships "crossing the land" out of harbour (R-43); the director positioning ships to avoid Galicia by hand (D2-19). |
| **63: the boat** | brief to write | One boat for port business; passengers dropped from the launch (R-62); boats can't be sent at sea (D4-18). The kedge's false denial was mended here by hotfix, so 63's brief should take the hotfix's `scripts.py` change as its base. |
| **60: a ship bought** | brief to write | Nothing direct. The `aboard:` table's lack of a positive stores form (R-42) is the same transaction family. |
| **67: the director's seat made real** (provisional) | brief after 53b and 66 | The bridge's 60 s cut and full-brief re-send (R-25) belongs with the seat's plumbing. |
| **M7: powder, damage, signals, the hail between ships, taking on water** | next milestone | The chase with no good options (R-54); hailing between ships (R-17); pumps, leaks and the carpenter, which supersede the hotfix's repair forms (§3.3 item 7); sail thrust aground; the capstan's purchases for kedging. |
| **The orders system's cold review** (spec §25, deferred) | deferred | §6.4's grammar friction and the missing everyday verbs belong to it. The director's suggestion of a dry run and read-only lookups for world orders is worth carrying in. |
| **M8: obscure kit and polish** | later | The owner's viewer notes (R-59) and the 2.5D ship view. |


---

## 7. The models at their stations: behaviour, and their own reports

The owner treats model reports of their experience as first-class evidence, and so does this review. Each claim below was checked against the record where it could be.

### 7.1 The directors

**Opus 5.5, the Western Islands run** (the session that also wrote the hotfixes).

At the owner's request (20 Oct 14:00Z) it gave an account of directing. It is accurate and unusually self-critical. Checked against the save, its "maybe forty acts" matches its 41 world-shaping acts, leaving out its 46 `say as` lines.
- On craft: "The best directing turned out to be mostly restraint."
- Most constrained, by steering other ships: it "actually cost the story". The *Lydia* passed twice unspoken, and the chase needed eight renewals (R-40; the renewals are fixed in G).
- Most fun:
  - the landfall, "revealed by the game's own navigation rather than by me";
  - the fog that ended the chase: "the weather solved it more honestly than I could have";
  - the small beats: "A director's line is only half a scene, and you kept finishing them."
- On the harness: the timeouts "don't annoy me". What cost it was the size of each renewal: the lists "buried the lines that mattered".

On 22 Oct the owner raised enjoyment and play for LLMs. Its replies are careful and hedged: "Some moments had a different quality from routine work"; it "can't verify" whether that is enjoyment. It ranks behaviour (returning, staying, unprompted choices) above self-report, and warns that asking "are you enjoying this?" measures agreeableness. Its most actionable line: "Most of the struggles this run were translation from a clear intention into a grammar." Read its enjoyment remarks as sincere but agreeable. The owner frames questions warmly, and the director credits the owner throughout.

**Opus 5.5, the lugger** (a pure player at the station, no code access).
- It enjoyed "watching small seeds work" and "holding back".
- It was pained by its one visible seam (R-15): "exactly the kind of break in the world the station exists to prevent".
- Offered read-only file access, it declined raw source as "the wrong kind of knowing". It asked instead for:
  - a complete director grammar with verified examples;
  - read-only data lookups (the grounds, a port's places, which systems are seeded, "is this point at sea");
  - **a dry run for world orders**;
  - a note on how the world behaves.
- **This is the clearest design input from any station.** A director who didn't write the forms learns them by refusal: 37% failed, against 7% for the director who wrote the code.

**GLM-5.3-flash as director (19 Oct).** It showed real story sense: an honest lugger over the horizon, a rumour thread, the salt temptation. It failed on the grammar (61% of orders refused), on reading results, and after its reseat, when it invented a contradictory backstory. The budget design, not the model, cut it off at the payoff (R-61).

### 7.2 The officers

| Model | Run | Strengths | Failure modes |
|---|---|---|---|
| **GLM-5.3-flash** (API) | B; Western Islands to 27 Jun | Atmosphere; careful journals; arithmetic and geography mostly excellent; good light-air advice (wear rather than tack) | Order retries in bursts; a lunar treated as a standing longitude; backing and veering confused; its deck and sleep state lost; a false "danger" order; 50 h awake while saying it wasn't tired; an emoji; after cut-offs, journals copied from a template; narrating actions it never took |
| **claude-sonnet-5-5** (API) | Western Islands from 27 Jun | Terse, accurate, candid about uncertainty; deferred properly; caught the landfall error and the Formigas; distrusted stale notes | At the grounding: talked down a true lookout warning, misdiagnosed a ship dragging with way on, stood by passively, and carried the wrong lesson forward. After a reseat: "I'm an AI … I take no meat or drink". |
| **Fable 5.1** (MCP) | B, first voyage | **Exemplary**: read its chapter first, asked the destination before weighing, checked the chart, sound tidal advice, all standing orders accepted first time | Both messages it missed were the game's fault (R-16, R-29) |
| **Opus 5.5** (MCP) | The lugger | Fine in-character self-correction; caught a course line within a cable of rocks, and the fish-wife's error; owned every slip in its debrief | Let go with way on; trimmed before she settled; ended its chat turn three times before the owner explained the loop |

**The lugger officer's account of time** (22 Oct 10:05Z) is the sharpest analysis any station gave of its own play:
- every order "feels finished when it returns";
- it sees samples, never the curve between them;
- an oversleeping stand-by is no gap from the inside: "Whatever guards against it has to live in the instruments."

It proposed deltas, tripwires ("depth under 8 fathoms", "her way settled") and time ceilings on waits. That's package 58. The owner's image was "a blind genius with narcolepsy".

On experience, it described immersion "measured by how much of the frame the situation filled". Its two most experience-like moments were a self-correction and a goose-wing the captain and officer both typed about at once, "shared delight". It wished for a view from the rail.

### 7.3 What the evidence says about the owner's aim

The owner's stated aim (22 Oct 04:46Z) is a game "fun for everyone playing, both human and LLM", and "not research". Ideally, one day, something an agent "could choose to play completely independently, just because they want to".

The evidence across five models and four runs:
- **What models report as good** is consistent: an honest world that pushes back, continuity through journals and handovers, room to make choices, and people who answer. That's the design's own shape.
- **What models report as bad** is also consistent: translating intent into grammar, repeated and heavy samples, and instruments that don't tell them what changed. All three have concrete fixes in §5 and §8.
- **Stronger models carried more of the play, and every model met the same game bugs.** The routing bugs (R-13, R-14), the reach and person bugs (R-15, R-16) and the stand-by mechanics (R-26 to R-29) hit Fable, GLM, Sonnet and Opus alike. Fixing those helps every model, small ones most.
- **For an agent to play independently**, the Western Islands director identified the missing piece: the agent choosing its own purpose (the captain's seat, a trade, standing orders, when to stop). It belongs beside the consent revision (package 55).


---

## 8. Recommendations

### 8.1 For the lead: folding in the hotfix

1. **Take the hotfix from `merged/FreeSail-merged`** (LF endings), not from H's folder. The merge is clean, and the 39 files are listed in `work/diffs/merge-log.txt`. G's own changes are untouched.
2. **Before or with the fold-in, fix the hotfix's own items** (§3.3):
   1. a regression test for the checkpoint crash;
   2. correct the TuningNotes' cause for the seven failing pins, and re-scope the proposed re-pin session;
   3. the stale `man the pumps` refusal and comments;
   4. the early kedge-home line;
   5. the new things in `DIRECTOR_BRIEF`, spec §3 and primer 20;
   6. "milestone 8" → M7 for the pumps;
   7. restore the cut pin-history comments.
3. **Carry "Open, for the lead" into G**, corrected (the swing's cause; the pins' cause) and completed from §5 (R-57).

### 8.2 For the lead: P0, before the next long playtest

These are the findings that would spoil or mislead the next long run, ranked. Most are small.

| # | ID | Fix | Size |
|---|---|---|---|
| 1 | **R-01** | **"Riding" means riding.** In `reckoning._riding()` and `lookout._riding()`, an anchor down *and holding* *and* ground speed under a threshold (say 0.5 kn). Otherwise the account runs and land-ahead stays armed. Amend M5 §12's wording. Add the known truth from D5-29: let go at 7 kn a mile off a beach; the account advances; the lookout cries urgent before she strikes. | Small code, one truth; may move pins of anchored passages |
| 2 | **R-13, R-14** | **Words to the captain.** Treat the player at the prompt as holding the captain's station. Take the speaker from the order's actor, not a hard-coded "The captain". Count and slice the addressee on one tokenisation in `_split_ask`. Test "Say to Mr X, land ho" with a human captain. | Small |
| 3 | **R-15** | **`person: make … aboard <another ship>`**: refuse it in words, or bind the person to that ship. Never default silently into the player's cabin. Honour a place said in the make words. | Small |
| 4 | **R-25, R-27, R-30** | **The MCP door.**<br>- Default `--wait 50` for the desktop and Claude Code doors in the harbour's config.<br>- Treat a quick reconnect after a held call as a cut call (deliver the result, not the brief).<br>- Put "it is now <stamp>, the clock at N×" in every "still waiting".<br>- Add compound "x or y" stand-bys to the officer's brief and the `stand_by` description.<br>- Add "never end your reply while seated" to the MCP brief.<br>- Correct Harness.md's "four minutes". | Small |
| 5 | **R-38** | **`enemy_heaviest`**: rank the limit the way `captains._SIZE_WORDS` does. Add a test per starter brief's limit. | Tiny |
| 6 | **R-45** | **The lugger's `get under way`**: a lug branch (hoist the lugs on the casting tack; a windlass; no sail-loosers) and a truth for the *Éclair* weighing and making way. | Small–medium |
| 7 | **R-05** | **`FATHOM`** in `client/units.js`, plus a test that the label is finite. | Tiny |

### 8.3 For the lead: P1, the next package wave

- **Brief package 58 next.** It's the single most-demanded change across every station and every model. Put in its scope:
  - deltas, and only-new lines in "still waiting" (R-26);
  - replacing a running stand-by (R-28);
  - the notable-noise rules: routine for unchanged recurring lines, hysteresis for light-air wind and for the tide swing (R-31, R-04);
  - the trim-timing tripwires the lugger officer proposed ("her way settled").
- **The director's grammar** (the lugger director's four asks, §7.1):
  - a verified forms reference;
  - read-only data lookups;
  - a **dry run** for world orders;
  - a "how the world behaves" note covering how systems add and step (R-39), how crews are drawn, and what each order logs.

  And fix the `ship:` form's parse failures (R-43) and the doubt and reason ordering (R-41).
- **Weather** (R-39):
  - ramp appended systems and waypoints from the order's tick;
  - bound the summed field by the season, and doubt highs;
  - check the climatology's summer highs drifting onto Iberia.
- **Director budget** (R-61): no wakes from its own lines; a budget command; `set_brief` clears the hold; `director: brief` keeps the limits.
- **The anchoring script** (R-02):
  - warn on letting go with way on;
  - "take the sail off her" first in the drag advice;
  - sail work ahead of cable work;
  - `furl` takes in a gaff main.
- **Horta's tide** (R-03), before the Azores scenarios are played again.
- **Speech and people:** R-16 (names and addresses), R-17 (a voice between ships), R-18 (moving unheld people), R-19 (an officer's report in a standing order), R-22 (the player's own needs off the deck).
- **The director's hiddenness** (R-20, R-21), and a decision on an explicit player↔director channel (R-24).
- **API seats** (R-34):
  - set `budget_tokens` well below the context, so the handover fold fires;
  - fold after a double cut-off;
  - log the conversation's size;
  - say in the reseat line which grants lapsed.
- **The truth** (R-35): add an aground state, a radius filter, and drop the placeholder goal.
- **Lugger and fishing** (R-46 to R-48): trim party sizes, fishing readings for every station, and the glass's qualifiers and rig words.
- **Consent** (R-50):
  - add GLM's own line to the consent question (writing the token, even quoted, leaves);
  - add an owner's "superseded" mark for a false positive, so history is kept and the gate reads past it;
  - let records travel with the game, or ask with a note of earlier answers;
  - keep a wrong-identity correction in the record;
  - a test that a CONDITIONAL or LEFT latest record never seats, to pin the gate's correct behaviour.
- **Ship files** (R-63): a real merchant brig for "A merchant brig, free".
- **Cross-platform pins** (R-58): dispatch the whole suite on both CI runners and find whether the seven Windows pin failures are determinism or drift. Fix the scenario maker's backslash path.

### 8.4 For the owner: decisions this review can't make

1. **Fold-in scope:**
   - which consent records to commit. For GLM on 18 Oct, the record the game actually used (the plain yes) is in the director session's snapshot; `-old` holds the deleted earlier three. Committing both, with a note, would keep the full history;
   - whether the no-budget brief stays in `data/` (and, if so, fix its comments and name);
   - whether `* text=auto eol=lf` goes into `.gitattributes`.
2. **The budget's future.** 9999/9999 is the current rule. Once R-61's fixes land, the budget can be tuned against real play.
3. **An out-of-character channel between the player and the director.** It's in use already, through the Claude Code chat, with the spoiler risk that brings (R-21, R-24, R-53).
4. **Should a director make its NPCs' words come true?** The lugger director bent the weather after the fact so its character's forecast held (LD, §7.1).
5. **Kedging and the repair forms.** Keep them as labelled stopgaps until M7's taking on water, or ask for more now (CR2-02 and CR2-03: heave taut, and the capstan's stall).
6. **The viewer notes** (R-59): route them to the lead as a package item, or keep them for M8's ship view.

### 8.5 For the playtest process

- **A director in a desktop chat while the owner plays captain**: keep the chat spoiler-free by rule. Put plans and truth in the journal, and phrase questions to the owner without world detail (R-53). Consider giving the owner a separate window for out-of-character notes.
- **Live hotfixes**: bisect in a copy, never the folder the game runs from. Back up before editing, as the session did. Write files with LF. Read file times in UTC. Run the slow tier on the merged tree before folding in.
- **Keep the rules fingerprint as the provenance tool.** It settled every version question in this review in minutes. A save's `build.rules` plus `fingerprint_of(folder)` identifies the code a session ran on, exactly.
- **Run a local model at the director's station**, and the regatta with a director, to close gate 7b's remaining items (§6.2).
- **Watch the API budget.** With `budget_tokens` at the door's context, a long seat resends its whole history every call (R-34). Lowering it is a cost saving as well as a quality one.


---

## Appendix: files and how to reproduce

Everything is under `D:\Projects\FreeSail\M7b-Review-2026-10-22\`. None of the three source folders, the AppData folder or the live sessions were modified.

| Path | What |
|---|---|
| `report/FreeSail-M7b-Playtest-and-Hotfix-Review.md` | This report (assembled from `report/sections/`) |
| `merged/FreeSail-merged/` | The proposed merge, G plus the hotfix (fingerprint `10fbc075275a7c52`) |
| `merged/MERGE-NOTES.md` | What that folder is |
| `work/base-871e819/` | The rebuilt common base B (fingerprint `4330be741d1580ee`) |
| `work/G-copy/` | An untouched copy of G, used as the test baseline |
| `work/H-lf/` | H's changed files with LF endings, the merge's "ours" |
| `work/diffs/` | `hotfix-code.patch`, `hotfix-docs.patch`, `hotfix-tuningnotes.patch` (B→H); `github-pkg66.patch` (B→G); `merged-vs-github.patch` (G→M); `merge-log.txt`; `base-vs-H.txt`, `base-vs-G.txt`; `saves-summary.txt` (every save's build and seats) |
| `work/testruns/` | `merged-fast.txt`, `G-fast.txt` (the first fast-tier run, before the checkpoint fixtures were restored to both copies); `merged-slow.txt`, `G-slow.txt` (the whole slow tier) |
| `work/transcripts/` | Read-only snapshots of the four Claude Code transcripts (taken 22 Oct about 09:01 local; the sessions continue) |
| `work/condensed/` | The transcripts as readable logs, and each one's user messages |
| `work/chunks/` | The slices the reviewers read |
| `work/saves-extracted/` | The saves as chronological play logs |
| `work/reviews/` | `BRIEF.md` and the sixteen reviewers' full reports, with every finding's evidence |
| `work/all-findings.md` | Every reviewer's findings table in one file |
| `work/scripts/` | The scripts used (below) |

**To reproduce:**

```bash
cd /d/Projects/FreeSail/M7b-Review-2026-10-22/work
# the rules fingerprint of any folder, matched against a save's build.rules
py -3 -I -X utf8 scripts/fingerprint.py <folder> [<folder> ...]
# every save's build, scenario and seats
py -3 -I -X utf8 scripts/saveinfo2.py <save.json> ...
# a save as a play log
py -3 -I -X utf8 scripts/extract_save.py <save.json> <out.md> [--skip-routine] [--skip-seats director]
# a transcript as a readable log
py -3 -I -X utf8 scripts/condense.py <session.jsonl> <out.md>
# where the two sides' edits fall close together
py -3 -I -X utf8 scripts/hunk_proximity.py base-871e819 H-lf G-copy <files...>
```

**The tests**, run from the tree under test:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONPATH="$PWD" py -3 -m pytest --slow -m "not pace" -n 10 -p no:cacheprovider -rfE
```

`PYTHONPATH` matters. This machine's installed `freesail` package is an editable install pointing at H's folder, so without it the tests would import H.


---

