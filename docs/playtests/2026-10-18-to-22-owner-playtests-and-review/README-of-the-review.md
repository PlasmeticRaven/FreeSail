# FreeSail M7b: the playtest and hotfix review, for the lead

**From:** the owner, 22 Oct 2026.
**Prepared by:** a cold review session (Opus 5.5) working locally on the owner's machine, with sixteen read-only parallel reviewers.
**Covers:** the playtests of 18–22 Oct 2026, and the live hotfixes the director session ("Sailing game scenario design") wrote between 19 and 22 Oct.
**How it was done:** nothing was pushed, no repository was touched, and no FreeSail tool was called. The playtests are still going.

## Start here

1. **`report/FreeSail-M7b-Playtest-and-Hotfix-Review.md`**
   - §0 is the summary.
   - §2 is the merge.
   - §3 reviews the hotfix and lists **what to fix before folding it in** (§3.3).
   - §5 ranks 63 findings (R-01 to R-63), each traced to the reviewers' evidence.
   - §8.2 is the **P0 list for before the next long playtest**.
2. **`patch/hotfix-onto-953caab.patch`**: the hotfix as one patch onto the GitHub snapshot.

## The versions

Every save stamps the rules fingerprint (`freesail.core.world.fingerprint_of`), and every claim about versions below rests on it.

| Label | What | Rules fingerprint |
|---|---|---|
| **O** | The owner's 18 Oct snapshot (`…-old`) | `04b66d9b753bc766` |
| **B** | The snapshot the hotfix copy started from: **commit `871e819`**, the merge of package 53b. The review rebuilt it from the director session's own backups, and it matches the saves made on it. | `4330be741d1580ee` |
| **H** | B plus the live hotfixes. The Western Islands run was played on it. | `372c899e355594fa` |
| **G** | The latest GitHub snapshot: **commit `953caab`**, the record of 53b and 66. The lugger run was played on it. | `e19ddb854219fbd8` |
| **M** | G plus the hotfix, i.e. this patch applied | `10fbc075275a7c52` |

The commits are identified by the zip files' timestamps against the branch's commit times, and confirmed by the fingerprints.

## Applying the hotfix

```bash
git checkout 953caab   # or your branch, if it has moved on: then use --3way
git apply --3way patch/hotfix-onto-953caab.patch
```

**Verified:** applied to an exact copy of the 953caab snapshot, the result is byte-identical to the reviewed merged tree, with fingerprint `10fbc075275a7c52`. The index lines carry full blob ids, so `--3way` works on a branch that has moved on.

**What it contains:**
- **39 files** (list: `patch/files.txt`; how each was merged: `work/diffs/merge-log.txt`):
  - 25 changed only by the hotfix;
  - 6 new;
  - 8 changed on both sides, merged three-way over B. Seven merged cleanly; one was an append-only conflict in `docs/dev/TuningNotes.md`, resolved by keeping package 66's section and then the hotfix's five.
- **LF throughout.** The hotfix had rewritten 13 files to CRLF; they're normalised here (report §2.3).
- **The owner's to decide** (report §2.5, §8.4):
  - four consent records of 19–20 Oct;
  - the owner's `data/director/briefs/interesting-passage-nobudget.yaml`.

  To leave them out, add `--exclude='docs/agents/consent/*'` or `--exclude='*nobudget*'`.

**Tests**, on the owner's Windows machine, whole suite (`--slow -m "not pace"`):

| Tree | Passed | Failed |
|---|---|---|
| Merged | 3,819 | 9 |
| Untouched 953caab | 3,807 | the same 9 |

The 9 are pre-existing on Windows: seven pinned truths, plus two Windows-only tests (report §2.4; logs in `work/testruns/`). **Please dispatch the whole suite on both CI runners** to tell cross-platform determinism from drift (R-58). The reviewer didn't, so as to stay off GitHub.

**Before committing**, report §3.3 has the fixes to make with the fold-in:
- a regression test for the checkpoint crash;
- correct the TuningNotes' cause for the failing pins (and re-scope the proposed re-pin session);
- the stale "man the pumps" refusal;
- the early "kedge comes home" line;
- the new things in `DIRECTOR_BRIEF`, spec §3 and primer 20;
- "milestone 8" → M7 for the pumps;
- the cut pin-history comments.

## What else is here

- **`consent-records/`**
  - `2026-10-18/`: the three records the 18 Oct games ran with. They were never committed and are on the owner's machine only.
    - Fable 5.1 and Opus 5.5.
    - GLM-5.3-flash's plain yes of 07:43:29. The owner wrote it by deleting two false positives (GLM quoted the opt-out token while praising it) and a conditional answer, then asking plainly.
    - The game's seatings that day cite this record. The consent gate worked.
  - `2026-10-18/glm-earlier-answers-deleted-from-live-folder/`: the three deleted answers, kept for history (report R-50).
  - `2026-10-19-to-20-in-the-patch/`: copies of the four records the patch adds.
  - `2026-10-22-not-in-the-patch/`: the lugger officer's record, which the run wrote into the owner's folder locally. It isn't in the snapshot or in the patch.
- **`saves/`**: each playtest's save with its `.checkpoint`. The folder name gives the date, the run and the version letter.
  - The cutter's final save (`…Bound-For-Madeira-Cutter`) carries the whole voyage, including the grounding at Horta (2 Jul 09:43, t2090591). `Falmouth-to-Ponta-Delgada-Cutter` is the last save before it (30 Jun).
  - Ship references are relative. Some lines name paths in the owner's Windows user folder. Make any paths relative before committing a save as a playtest record (docs/playtests/README.md).
- **`scenarios/`**: from the owner's AppData.
  - `western-islands-run`, `free-trade`, `inshore-squadron` and `lisbon-letter` were written by the director session, at 9999/9999 budgets on the owner's ruling.
  - The rest are the owner's.
- **`owner-notes/M7b Notes.txt`**: the owner's lugger viewer notes of 18 Oct, which aren't tracked anywhere in the repository (R-59).
- **`work/`**: the evidence behind the report.

  | Folder or file | What |
  |---|---|
  | `reviews/` | `BRIEF.md` and the sixteen reviewers' full reports, with ticks, timestamps and code references for every finding |
  | `all-findings.md` | Every reviewer's findings table in one file |
  | `diffs/` | B→H (`hotfix-*.patch`) and B→G (`github-pkg66.patch`), LF-normalised; the merge log; `saves-summary.txt` (every save's build and seats) |
  | `testruns/` | The test logs |
  | `scripts/` | The fingerprint, save-extraction, transcript-condensing and proximity scripts |
  | `saves-extracted/` | The saves as chronological play logs |
  | `condensed/` | The four Claude Code session transcripts as readable logs. These hold the owner's own chat with those sessions. |

## Paths the report cites, and what they are here

| In the report | Here |
|---|---|
| `D:\Projects\FreeSail\FreeSail-claude-dreamy-darwin-d77nty` (G) | Commit 953caab |
| `C:\Users\frenc\Downloads\FreeSail-claude-dreamy-darwin-d77nty` (H) | 953caab plus this patch, or `work/diffs/hotfix-*.patch` over B |
| `…-old` (O) | The owner's 18 Oct snapshot; not included |
| `work/base-871e819` (B) | Commit 871e819; not included |
| `merged/FreeSail-merged` (M) | Apply the patch; not included |
| `work/chunks/` | Slices of `work/condensed/`; not included |
| `work/transcripts/` | The raw session transcripts; held back (verbatim, personal data) |
| The director session's scratchpad snapshot | The source of `consent-records/2026-10-18/` |
