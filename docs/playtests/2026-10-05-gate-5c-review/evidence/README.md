# Evidence for the gate 5c playtest review

The detailed reports that `../report.md` was written from. Each was written by a separate
Claude Opus 5.5 reader session on 2026-10-05, working read-only from the saves, the code and
the documents. They carry the ticks and quotations that the report leaves out.

Read them as working papers. A reader's statement marked as its "reading of the source" was
traced in the code by that reader and not always by anyone else. `../report.md` marks with
**(lead)** what the lead confirmed directly, and section 7 and 8.5 say where the readers and
the notes were found wrong.

## What each file is

**The games, slice by slice** (one reader a slice):

| File | Game | Covers |
|---|---|---|
| `M2-merchant-passage-owner-alone.md` | 1 | The gate's merchant passage, the owner alone |
| `H1` to `H5` | 2, the *Harpy* | Ticks 0 to 111,480; to 216,817; to 527,389; to 602,283; to the end (the grounding) |
| `P1` to `P5` | 3 and 4, the *Speedwell* | The abandoned first start and ticks 0 to 111,720; to 259,700; to 457,500 (the calm); to 521,460; to the end (Scilly) |
| `L1-cutter-gemma.md` | 5 | Gemma 4 on the cutter |
| `L2-qwen-ollama-cutter-watcher-consent.md` | 6, and part of 2 | Qwen under Ollama on the cutter; the same weights as watcher on the *Harpy*; its consent records |
| `L3-cutter-qwen-llamacpp.md` | 7 | Qwen under llama.cpp on the cutter |
| `M1-amazon-merchant-ship-opus.md` | 8 | The *Amazon* as a merchant ship |

**The games, consolidated** (one collator a game, from the slice reports, with the readers'
disagreements settled against the logs):
`C1-harpy-consolidated.md`, `C2-speedwell-consolidated.md`, `C3-local-models-consolidated.md`.
Start with these.

**The notes against the documents:**
`D1-m5-expectations.md` (the M5 specification, work packages and gate),
`D2-harness-as-designed.md` (the harness and consent documents),
`D3-design-proposal-map.md` (the design proposal and its companion papers).

**The m5c-b change set:** `R1-m5c-b-diff-review.md`, an independent review.

**The notes against the code:**
`V1a-harness-lifecycle-code.md` (seating, doors, turns, the journal),
`V1b-authority-standing-detector-code.md` (authority, stand-bys, standing orders, the
contrary detector, taken aback, the wind and the sea breeze),
`V2a-navigation-lookout-pilot-code.md` (the reckoning, the lookout, the pilot),
`V2b-ship-handling-ground-client-code.md` (handling, the anchor, grounding, the browser),
`V2c-trade-boats-parsing-code.md` (the port, the boats, the order language).

**The owner's material:** `amazon-post-session-chat.md`, the *Amazon*'s officer's own account
after the session, from the Claude Desktop chat, supplied by the owner.

**Game 9, the first game on m5c-c (added 2026-10-06 and 07; the report's section 10):**
`harpy-m5cc-post-session-chat.md`, the brig's officer's own summary after the run, supplied by
the owner; and `G9-brig-m5cc-measurements.txt`, the lead's measurements of that game from a
replay of it (the account against the truth by stretch, every fix and bearing, the sights,
the master's doubt beside the true error, her head against the wind while hove to, the
Goulet minute by minute, the anchors' own movement over the ground, and a test of what the
ground-tackle orders do with an anchor's name). No separate reader worked this game: the lead
read its log, transcript and journal directly.

**Game 10, the first game on the build with 37e, 37f and 37g (added 2026-10-08; the report's
section 11):** `G10-cutter-m5cc-measurements.txt`, the lead's measurements of that game from a
replay of it: how the replay differs from the game as played (one line); the account against
the truth by stretch, at every observation that moved it, and fix by fix on the run into St
Mary's Sound, with the true and the charted depth and the tide at each cast; the hour
standing off and on; what the harness held of the officer's conversation when the model
server refused it for size, by its own count and the server's; her head, the wind and her
way at each urgent "taken aback"; the officer's empty replies; every order refused; and the
station's events. The owner's two notes on this game were given in conversation and are
quoted in the report's 11.2. No reader worked this game either.

**The stations' briefs after the consent brief was made leaner (added 2026-10-07):**
`station-briefs-after-37g-second-pass.txt`, the watcher's and the officer's briefs as a model
is sent them on build m5c-c/37g, composed by the lead with no model seated: each part of the
head and the station brief whole through the bridge, and the door's note for the other two
doors. It is what the lead read to check that everything moved out of the consent brief is
said in a station's brief (`../drafts/consent-brief-lean-draft.md`, the table).

## The paths inside the reports

The reports cite files under a scratch folder
(`...\scratchpad\sessions\<game>\<game>.log-full.txt` and the like). That folder was
temporary. The files in it were dumps of each game's full log, transcripts, journals and
orders, and can be made again from the saves in seconds with the scripts in `tools/`.

## The scripts in `tools/`

All read-only: they load a save's checkpoint through the game's own restricted loader and
write text files wherever you point them. Run them from the tree whose code wrote the save,
with `PYTHONPATH` set to that tree so that its classes are the ones loaded (the editable
install points at m5c). For example, in PowerShell from `FreeSail-gate-m5c-b`:

```
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:PYTHONUTF8 = "1"
py path\to\tools\dump.py saves\freesail-seed7-tick689841.json C:\some\out\folder 2-harpy-brig-opus
py path\to\tools\condense.py saves\freesail-seed7-tick689841.json C:\some\out\harpy-part5.txt 2-harpy-brig-opus 602100 689841
```

- `dump.py SAVE OUT_DIR LABEL` writes the whole log, each station's transcript and journal,
  every order typed, the standing orders and scenario, and a summary with counts by kind.
- `condense.py SAVE OUT_FILE LABEL [START END]` writes the log merged with what each model
  sent, between two ticks, with the chattiest routine lines left out.
- `slice.py` prints a tick range of a dumped log by kind (edit its path to your dump folder).
- `lineage.py` shows which saves are continuations of which.
- `seabreeze_check.py SAVE` is the check of section 5.6: it loads the *Harpy*'s save of tick
  602,100, runs the weather on, and samples the wind along a line run north-east from her
  anchorage, with the sea breeze as built and with it set to nothing. It takes about a
  minute.
- `replay_check.py SAVE` replays a save from its first tick on the build named by
  `PYTHONPATH` and sets the replayed log against the one in the save's checkpoint: the same
  digest or not, and the first line that differs. `replay_check2.py SAVE` does the same and
  says whether the two logs hold the same lines in another order or differ in substance.
  They are the check of the report's section 9, question 1 (added 2026-10-05, after the
  owner's answers). A replay runs at roughly a thousand ticks a second; allow two or three
  minutes for a day and a half of ship's time.
- `account_probe.py SCENARIO HOURS` sails one of the recorded passages under its own book and
  prints how far the account stood from the truth along the way; run it on the tree before a
  package and on the tree after, and set the two side by side (used on package 37d).
- `fix_vs_bearing.py` and `legs_compare.py` read the 37d builder's own dumps of the merchant
  passage (not kept here) and were the check behind the correction in `CHANGES-m5c-c.md`,
  "The Goulet".
- `replay_probe.py SAVE OUT_PREFIX [EVERY]` replays a scratch copy of a save on the build
  that wrote it and records the truth, the account, the master's doubt, her head, way and
  wind once a minute and at every observation, then checks the replayed log's digest against
  the checkpoint's. Run it from inside the build's folder (the ship file is found by a
  relative path). `g9_analyse.py OUT_PREFIX [section ...]` prints the tables of
  `G9-brig-m5cc-measurements.txt` from its output. Game 9, five days of ship's time, took
  seven minutes.
- `anchor_probe.py SAVE OUT FROM END` does the same replay and records each anchor's place
  on the ground, scope, load and holding while it is down.
- `tackle_words_test.py SAVE` loads a save's checkpoint in memory and tries the veer, weigh
  and heave-short orders with and without an anchor's name; nothing is written.

The last save of each game:

| Game | Save | Tree |
|---|---|---|
| 1 | `merchant-passage-complete.json` | m5c |
| 2 | `saves\freesail-seed7-tick689841.json` | m5c-b |
| 3 | `saves\freesail-seed7-tick6753.json` | m5c-b |
| 4 | `saves\freesail-seed7-tick558434.json` | m5c-b |
| 5 | `saves\freesail-seed7-tick54107.json` | m5c |
| 6 | `saves\freesail-seed7-tick34091.json` | m5c |
| 7 | `saves\freesail-seed7-tick112613.json` | m5c |
| 8 | `saves\freesail-seed7-tick123673.json` | m5c |
| 9 | `saves\freesail-seed7-tick430516.json` | m5c-c |
