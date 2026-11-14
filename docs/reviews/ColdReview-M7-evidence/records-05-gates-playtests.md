# Records 05: the gates, the playtests, and CHANGES-m5c-c.md

Reader under the reviewer, second sitting. Tree at 504a250 (the review's branch head b72ed89 adds only the review). Read: `docs/reviews/ColdReview-M7.md` heads 1 to 5; `docs/gates/README.md`, `gate-m5c.md`, `gate-m6a.md`, `gate-m6a-2.md`, `gate-m6c.md`, `gate-m7-interim.md` whole; the other eleven gate reports for their heads, checklists and verdicts; `docs/playtests/README.md`; every `notes.md`, `post-session-notes*`, `debrief.md`, `testing-report.md` (heads), `case-study.md`, `review-of-the-local-work.md` (head and outline), the owners'-runs `README.md`s of m6a, m6a-2 and m6c (they hold his notes verbatim), the Éclair `owner-notes.md`, `owner-notes-2026-10-27.txt`, `model-officer-review.md`; the M7b playtest review (summary, §5 to §8); the gate-5c review's second edition (A, B, a few sections by search, the ledger's tally); `CHANGES-m5c-c.md` (head and outline). Saves, logs and transcripts were listed and grepped only. Nothing in the tree was changed but this file. Model names in the records are written here as "a model", "the lead's model" and so on.

---

## (a) The gates

### Each gate, by its own report

The gate process (`docs/gates/README.md:3,18`): "No milestone is finished until the owner has checked it live and said so"; "The next milestone does not start until the verdict is in"; each gate is a report, a release zip, the suite on GitHub, and the owner's verdict. Every report is written by the lead (or a builder) for the owner; the verdict line at the top of each is the lead's summary of what the owner said.

| Gate | Run by the owner? | When | Verdict (report line 3) | What it tested |
|---|---|---|---|---|
| m0 | yes | 25 Sep | Passed with notes; "All ten items passed" | a live checklist at the console: exact commands, exact lines to see |
| m1 | yes | 25 Sep | Passed; items 1 to 8, 10 to 13 | live checklist, two ships (item 9 "observe, do not judge", 14 free words) |
| m2 | yes | 26 Sep | Passed; items 1 to 17 | live checklist, console and browser |
| m3 | yes | 26 Sep | Passed | live checklist (crew) |
| m3b | yes | 27 Sep | Passed | live checklist plus item 11, a document to rule on (TuningNotes truths 24 to 33) |
| m4a | yes | 27 Sep | Passed; items 1 to 8 | live checklist (standing orders, the Python twin at item 8) |
| m4b | yes | 27 Sep | **Not passed** ("the lead's error in spec M4 §13", `gate-m4b.md:5`) | Part A checklist; Part B a model session |
| (m4b-2) | yes | 28 Sep | no report file; its record is inside m4b-3 | playtests 3 and 4 |
| m4b-3 | yes | 28 Sep | Passed "on the local-model items"; Desktop and Claude Code items **not run**, carried to 4c | playtests 5 and 6 (models at the watcher's station) |
| m4c | yes | 29 Sep | Passed on playtests 7 to 9; **`--load` not exercised**, the Claude Code item **not run**, both carried | a day sailed with a model watcher; the report is the playtest form |
| m5a / m5a-2 | yes | 30 Sep | Passed (one verdict, the same text in both files); items 5 (`--load`) and 7 (climatology) **not exercised**, deferred to 5b; re-cut once for a Windows fault (27 failed, 8 errored) | playtest 11 plus "the owner's own run of the items alongside" |
| m5b | yes | 1 Oct | Passed on playtests 12 and 13; items 7 (`--load`) and 8 carried "count for both" (`gate-m5b.md:5`); the verdict does not say they were run | two model-watched passages |
| m5c | yes | 8 Oct | **Passed** on the build as cut; **provisional** on m5c-c "to stand once the fold-in satisfies both"; the lead's own officer's watch, one of the two halves the spec required, **withdrawn** (`gate-m5c.md:3,5`) | ten games of 2 to 8 Oct and the naval cruise; items 1 to 13 never ticked, item 14 (rulings) ticked |
| m6a | yes, 11 Oct | 11 Oct | **"open"** to this day (`gate-m6a.md:3`); the owner's runs found seven faults, routed to package 45 (`gate-m6a.md:180-192`) | trials, trade runs, the wardroom game |
| m6a-2 | runs yes, gate no | 13-15 Oct | **"not cut"**; folded into 6c by the owner's word of 15 Oct (`gate-m6a-2.md:3`) | free voyages on package 45's build |
| m6c | in part | 17 Oct | **"run in part"**: items 1 to 3, 5 and 8 run, the rest "deferred to the director's milestone's gate by decision 50" (`gate-m6c.md:3`) | 5 of 13 items |
| m7-interim | **no** | drafted 29 Oct to 6 Nov | **Pending**; "not a full gate: no build is cut ... no verdict closes the milestone on it" (`gate-m7-interim.md:3`) | 17 items, none run |

Of 192 checkboxes in the seventeen reports, one is ticked (m5c item 14). The per-item record of every gate is the verdict sentence and, from 4c on, the playtest folder.

**The last gate passed whole is m5c (8 October 2026)**, and only by the owner's word: its lead's watch was withdrawn rather than run, its m5c-c half passed "provisionally" with no later record that the provision was met, and its checklist items were not recorded one by one. Strictly by the reports, the last gate whose items are all said to have been run is **m4a (27 September)**: the `--load` item was carried from 4c to 5a to 5b to 5c (`gate-m4c.md:3`, `gate-m5a.md:3`, `gate-m5b.md:5,85`, `gate-m5c.md:77`) without a recorded run, which bears directly on the review's checkpoint finding (head 5.4).

**No gate of milestone 6 was passed.** m6a's verdict line still reads "open"; m6a-2 was never cut; m6c was run in part. The review's §11 row ("no gate has been passed whole since milestone 6's first parts") is too kind by one: milestone 6's first parts were never passed either. *Correction for the review, head 1.3 §11 and head 5.2.*

### "Gate m6c passed" against "run in part"

The repository's `README.md:5` says "Status: gate m6c passed". The gate's own report (`gate-m6c.md:3`), the owner's-runs folder (`docs/playtests/2026-10-17-gate-m6c-owner-runs/README.md:4-6`: "The gate was run in part: its untested items are deferred") and decision 50 (`docs/DesignProposal.md:655`) all say **run in part**. Decision 50 is right; the README is wrong. No other file in the tree says m6c passed.

Worse than "in part": of the five items run, the owner's own notes show three failing their stated expectations. Item 2 expects "never aground"; the gale trial "eventually ... simply ran aground on a steady tack" (save `m6c-trial-station-gale-aground`; notes lines 28-31). Item 8 expects "the frigate gives up a stale chase and returns to her station"; the stranger trial "kept the ship well south and west of the station" (save `m6c-trial-station-stranger-failure`; notes 37-39). Item 5's merchant passage "took the ground while coming to anchor in Berthaume" without the pilot (notes 33). Only item 3 and the naval cruise read as passes. The deferred items went to "the director's milestone's gate", which decision 51 (`DesignProposal.md:657`) froze unrun; **none of them reappears in the M7 interim gate** (no regatta, no seat hook, no lugger or smack, no world's business, no Funchal to Angra: grep of `gate-m7-interim.md`). They are lost, not deferred.

### The interim gate of milestone 7

- **What it is:** a draft "where milestone 7 stands since m6c", "package 85's last deliverable, the owner's word of 2026-10-29" (`gate-m7-interim.md:3`); the lead added "The engine's and the world's half" on 30 Oct (line 21) and the owner's two reminders J1 and J2 on 6 Nov (lines 75-106). It cuts no build, no release, closes nothing (line 124).
- **Who wrote it:** a builder session of package 85 (the player's side), the lead (the engine's half and the records), the owner (J1, J2 by dictation).
- **Run?** No. Verdict "Pending"; all 17 boxes empty. Its two playtests were to follow package 84 and package 75's *Indefatigable* (line 3); both have landed (84's step 11 is in its own suite table, line 29; the *Indefatigable*'s testing report is dated 30 Oct), and neither playtest is in `docs/playtests/`.
- **What of the review's findings it would have caught, if run as written:**
  - the guns silent in the first action: **probably not**. Item 3 plays `first-action.yaml` "with the enemy awake", but asks for the private signal, the fire "opened" and the logs read; it does not ask the player to give the first order himself, and the owner's own first action (below) gave none.
  - the starter book refused on fore-and-aft vessels: **no**; item 6 sails `mahon.yaml`, a frigate (`data/scenarios/mahon.yaml:31`).
  - the director's reach onto the player's ship: **no**; item 10 has the lead at the director's seat pulling levers on the *Raven*, the tender, and asks "nothing in the owner's log from nowhere"; nothing on `captain: intent` aboard the player's ship, a wound, a strike, or the brief's limits.
  - the purchase with the boat lost, the harbour's first game, the repeated reports: **no item touches them**.
  - the checkpoint and replay: **in part**; item 4 saves and replays many hulls "to the last digit" but does not try a checkpoint from elsewhere or a Python rule.
  - the boundary, the sandbox, the tests that cannot fail: **no**; it says it "does not run the whole slow tier" (line 124).
  Its own items are the lead's and builders' lists of what they built; none is the newcomer's road.

### Code in the tree that has never been before a gate

By the records (the clone is shallow, so the attribution is the records', not git's): everything merged after the m6c cut of 17 Oct at package 42b (`gate-m6c.md:3`), and the m6c packages whose items were not run.

- **Milestone 7b (the director), frozen open, gate not run** (decision 51): packages 50, 52, 53, 53b, 54, 56, 57, 58 (a, b), 59, 62, 66, 67, 68 (`docs/dev/M7b-WorkPackages.md` headings).
- **Milestone 7, interim gate drafted and not run:** 60, 65, 70 to 77, 79a to 79d, 81, 82, 82b, 83, 84, 85, 86, 88, 89, 92 to 96, 98 to 107 (with 103a, 106a, 106b), 109 to 112, 114 (`docs/dev/M7-WorkPackages.md` headings).
- **Milestone 6 in the m6c build but untested there:** 43b (the lugger, the smack, the world's business, the ports' faults), 44 (the regatta, the trims, the parity tests), the seat hook of 43.
- Modules that by their packages are wholly post-cut: `freesail/combat/` (5,866 lines), `agents/director.py` (2,381), `world/signals.py` (1,629), `world/squadrons.py` (1,752), `world/prizes.py` (1,693), `world/boats.py` (1,036), `world/water.py` (952), `world/needs.py` (837), `world/hulls.py` (553): about 16,700 lines, before the post-cut changes inside older modules (84's one world touched most of `world/`, `core/world.py` among them). Beside them `tools/ships/` (18,429 lines: the *Indefatigable*, the *Bellerophon*, the eight hulls) and five chart regions (79a to 79d).
- The two ship reports of that period say so themselves: "**Nobody has sailed her in a live page yet** ... The first test of how she feels is still yours" (`docs/playtests/2026-10-30-pilot-indefatigable/testing-report.md:3-5`, "For the owner, in place of your own test"); the same for the eight hulls (`2026-10-31-hulls-the-eight/testing-report.md:3-5`).

---

## (b) The playtests

### What the owner met when he played, by date

| Date | Record | What he met (his words where kept) |
|---|---|---|
| 25 Sep | gate m0 | a log line pulled his half-typed order into the output |
| 27 Sep | `2026-09-27-gate-3b/notes.md` | six tries to say "bear off"; quarter points refused; leeway 145° from a standing start |
| 27 Sep | `gate-4b-sonnet-watcher` | the door's shape "really, really unwieldy"; the lead's spec error |
| 28 to 29 Sep | 4b-2, 4b-3, 4c | lost samples, loops, a runner timeout; **no order belays work in hand** (`2026-09-29-gate-4c-qwen-watcher/notes.md:29-38`); re-firing routines call all hands |
| 30 Sep | 5a | 27 tests failed on Windows; all hands to one sail; a standing order cannot `tell` the watcher |
| 1 Oct | 5b | "Definitely need text suggestions ... in the browser, plus ability to pull up the docs" (`2026-10-01-gate-5b-opus-5.5-the-passage/notes.md:23`); "Couldn't figure out all the ... reckoning's uncertainty terms ... a lot of the orders were refused" (line 24) |
| 2 to 8 Oct | 5c review | ten games; the *Harpy* aground off Penlee; three readings give the true position away; **five of the starter book's nine rules refused on the cutter** (`report-2.md:2643-2645`) |
| 11 Oct | m6a runs | full and by aback; storm staysail blown; the merchant balks an entrance; pictures white; aground on the Filletes with the pilot aboard |
| 13 to 15 Oct | m6a-2 runs | the boat "ghosted"; image shelving; 25 notes, most of them design wishes (needs, people, the director's voices, gybing) |
| 17 Oct | m6c runs; the *Éclair* | aground in two of five items (above); the lugger's sails wrong |
| 18 Oct | dispatches director test (`notes.md`) | the director's hand lasts a glass; the lookout sees through the land (finding 10); the consent brief "says the director is 'to come'" (finding 24) |
| 18 to 22 Oct | M7b review (63 findings) | the grounding at Horta with no warning (R-01); words to the captain misfiled (R-13); the "no enemy heavier than a brig" limit refusing nothing (R-38); **the player at a lesser seat refused `how am I`, `eat` without the deck** (R-22) |
| 24 Oct | `2026-10-24-owner-first-action/notes.md` | "not bad at all for a start"; played "with no input until the enemy struck" (line 3-4); the circle through the wind; two of the fighting book's orders refused at load (fixed) |
| 25 to 27 Oct | 70 to 72 | the convoy stalls; a model captain of another ship cannot go ashore; colours flicker |
| 5 Nov | two case studies | the captain's word through the officer is no word; "the guns are still secured; they must be cast loose by your order" (below) |

### The review's player-facing findings (heads 1.5 and 5.3) against the playtests

| Review finding | Met before? | Where | What was done |
|---|---|---|---|
| Guns secured and silent; "firing as they bear already" | **Not by the owner**; met by a model and filed as a success | Owner's first action played with no order of his (`2026-10-24-owner-first-action/notes.md:3-4`), so the rules captain cast loose and fought. On 5 Nov the director, in the gunner's voice, told the model captain "the guns are still secured; they must be cast loose by your order", and the lead's case study lists that under **"What held"** (`2026-11-05-brig-off-falmouth-fully-crewed/case-study.md:36-39`) | Nothing. The trap was seen and read as the director's good conduct. No record finds "as they bear already" |
| The starter book refused on the cutter | **Yes, 4 to 5 October** | gate-5c games 5 to 7: "5 of its 9 standing orders are refused for a cutter" (`2026-10-05-gate-5c-review/evidence/L1-cutter-gemma.md:34,420`); report-2 lists it among "small faults" (`report-2.md:2643-2645`) | Not mended; the book is now seven rules and three still refuse (review head 1.5). Lost among the "small faults" that "wait" (`report-2.md:441-445`) |
| A purchase with the boat lost: money taken, nothing delivered | **No**; the design that allows it was recorded | The 5c evidence quotes primer 14: the bargain "moves the purse at once, and sends the boat" (`evidence/V2c-trade-boats-parsing-code.md:197`); `trade` named as what blocks several bargains | Never tried with the boat lost |
| A port scenario "at the usual anchorage" with no anchor down | No | The 18 Oct dispatches test used the same scenario; the model captain anchored at 05:02 at once (`2026-10-18-dispatches-director-test/notes.md:16`), so nobody met the refusal | Nothing |
| The log's repeated lines (the same report eight times) | **The class, many times** | the log "chatty" (playtest 7, finding 6); 265 wind-shift lines (`report-2.md:285-287`, made quiet by 37f); the sample "repeats the history" (dispatches finding 21); notable noise waking stations (R-31), 66 tide-swing lines (R-04); "every gun shot ... a notable event" (`model-officer-review.md`, point 4) | Each instance mended where found (37f; the deltas, 58), the class never: the review met a new instance |
| The harbour page offers no first game | **No playtest met it**: the owner always knew which file to open | His nearest note is 5b's wish for the books in the browser | Nothing; the playtests are all by people who know the game |
| (also) The seated player without the deck refused `go below`, `eat` | **Yes, 18 Oct** (R-22, `FreeSail-M7b-Playtest-and-Hotfix-Review.md:544`), again in package 98's "found for others" (`docs/dev/M7-WorkPackages.md:3654`) | | Not mended at 504a250 (review pillar 4) |
| (also) Sight across the land | **Yes, 18 Oct** (dispatches finding 10, "the owner's note on sight across land") | | "Routed" to the owner's note; still so (review F2.8) |
| (also) The brief's limit on an enemy's weight | **Yes, 22 Oct** (R-38, P0, `...Review.md:570`) | | Mended for "brig" by package 68 (`agents/director.py:404-424`), but `rank is None` still returns None: any word the ranker cannot read passes, which is the review's "line-of-battle ship" (decision 14). The record calls it mended; the hole is the same hole one step on |
| (also) The consent brief's "director is to come" | **Yes**: owner's note 17 of m6a-2 (13 Oct), decision 48 (17 Oct) rewrote the sentence leaving "the director alone 'to come'" while package 50 built him the same day, dispatches finding 24 (18 Oct), R-51 (22 Oct) | | Deferred by decision 51 to package 55; still in `docs/agents/ConsentBrief.md:13` |

### The owner's own words on what the game is to be, and where the work went

- 11 Oct: "the basics must function well and reliably. We needn't be able to handle every single edge case" (`2026-10-11-gate-m6a-owner-runs/README.md:31`).
- 13 Oct: "I like driving towards more immersion for both players and LLMs" (`2026-10-13-gate-m6a-2-owner-runs/README.md:54`), and with the needs "a warning not too make the needs too much busywork that might distract from the seamanship" (line 58).
- 22 Oct, as the M7b review reports him: a game "fun for everyone playing, both human and LLM", "not research" (`...Review.md:752`).
- 27 Oct: "now it's a matter of ensuring that the flow of the game through the log does not lose our attention to playability and understandability and that our additions to the game world from here are focused on integrating holistically" (`2026-10-25-to-27-owner-playtests-70-72/debrief.md:6-9`).

Where the work then went (the interim gate's own list and the reports): the one-world refactor in eleven steps (84), four chart packages east and south with the tide's tiles rebuilt (79a to 79d, 89, 93, 94), a 64 and a razee "in place of your own test" (30 Oct), eight hulls redrawn (31 Oct), prizes, boats as vessels, the warrant officers. Of the 27 October words, the "integrating holistically" half was taken (84); the "playability and understandability" half has no package in the interim gate's list, and the review's first hour (F2.7) is what it would have been.

### How many of the playtests' findings were mended, deferred or lost

The records allow only partial counts.

- **Gate 5c's ledger** (8 Oct, `report-2.md` appendix 1, 285 rows): 134 "Built", 36 "Not built", 18 "Still so", 2 "Partly built", 7 "Overtaken", 13 "Followed", 6 "Not checked" (tallied by this reader).
- **The M7b review's 63 findings** (22 Oct): of its seven P0 rows, all are named in the code or tests at 504a250 (grep of R-01, R-05, R-13, R-14, R-15, R-25, R-27, R-30, R-38, R-45), so taken; R-38 only in part (above). Of the P1 rows tried, R-22 (the player at a lesser seat) appears nowhere in code, tests or `docs/dev/` by its id: lost, then found again by package 98's builder.
- **Routing without closing.** Every owner's note since 13 Oct is "routed" to a package or "the reviewer's list" (`docs/playtests/2026-10-13-.../README.md:9-10`; dispatches "Routed", lines 113-118; 70-72 notes lines 38-67). The records do not hold a register that says which routed item closed. A finding is mended where a later record says so; otherwise the reader cannot tell deferred from lost.
- **Gate items lost:** m6c's eight deferred items (above); the 4c to 5c `--load` item.

---

## (c) What the saves and transcripts carry

Grep over `docs/playtests/` (plain files, and the 25 `.gz` saves unpacked in memory). Values not reported.

| Kind | Count |
|---|---|
| A user's profile folder on Windows (`<drive>:\Users\<name>` and the encoded `C--Users-<name>` form) | **one distinct profile name, 32 occurrences**; with the related `AppData` paths, **61 matches in 21 files**: the owner's eight saves of 25 to 27 Oct (4 each, in `director.brief.source` and `scenario.director.brief.source`), the dispatches save, the M7b review and five of its reviewers' files and four extracted transcripts. None in the `.gz` saves |
| E-mail addresses | 0 |
| Key-shaped strings (vendor key prefixes, cloud key ids, tokens, `Bearer` values, private-key headers, `"api_key"`/`"token"` fields with values) | 0 |
| URLs to IP addresses | 12, all loopback |
| Mentions of a model vendor's router service by name | 81 in 20 files (names, not keys) |

The playtest form asks for the ship's path to be made relative before a save is committed (`docs/playtests/README.md:16-17`); the director brief's source path was not.

**Size:** `docs/playtests/` is **81.8 MB tracked** (79 MB on disk), 13.3% of the repository's 617 MB of tracked bytes; saves, checkpoints and extracted transcripts are 60.7 MB of it. The largest single files: the Western Islands save 10.4 MB, five saves of 3.2 to 3.5 MB, the extracted cutter transcript 2.0 MB.

---

## (d) `CHANGES-m5c-c.md` (66,507 bytes, 440 lines, the repository's root)

The change record of **a local working copy of the gate-5c zip**, `FreeSail-gate-m5c-c`, made on 6 Oct "at the owner's word", in which packages 37b to 37g were built with "no commits ... and the GitHub repository is not touched" (lines 3-6). It records each package's files, the pins moved and what was left undone, for the hand-over to the lead. It sits at the root because it sat at the root of that folder, and the folder "was taken whole on 2026-10-08 as the merge of a branch made at the gate's commit" (`docs/dev/M5-CloseOut-5c.md:68-73`). It is still read: two tests cite it in comments (`tests/test_known_truths.py:4318`, `tests/test_checkpoint.py:157`), and `docs/dev/M5-WorkPackages.md` and `TuningNotes.md` point into it a dozen times. In the repository its own words are no longer true: "no commits are made here", and "Running it: `cd D:\Projects\FreeSail\FreeSail-gate-m5c-c`" (lines 54-60). It belongs under `docs/dev/` as a record with a line saying what it was.

---

## 1. Where the record and the thing differ

1. **"Status: gate m6c passed"** (`README.md:5`) against `gate-m6c.md:3`, the owner's-runs README and decision 50: run in part, and three of the five items run failed their expectations.
2. **`gate-m6a.md:3` "open"** for 35 days; m6c's line 10 says the verdicts of m6a, m6a-2 and m6c "are the owner's together, and the milestone closes on them". No verdict closes m6a anywhere.
3. **`docs/gates/README.md:18`** "The next milestone does not start until the verdict is in" has been false since decision 29 (30 Sep) and is unamended; `gate-m6a-2.md:91` says 43, 43b and 44 "wait on this gate", and they ran on a gate never cut.
4. **R-38 recorded as a P0 taken**, the code (`agents/director.py:420-421`) still lets through any word it cannot rank: the review's decision 14 finding is that residue.
5. **The consent brief's "director is to come"**: decision 48 (17 Oct) records the sentence rewritten; it kept the director "to come" the day the director was built.
6. **The gate-m5c line "a provisional pass on m5c-c ... to stand once the fold-in satisfies both"**: no record says it stood.
7. **`docs/playtests/README.md:114-129`** "The records so far" lists four of the 28 folders.
8. **The repository README's "Four reference ships are in `data/ships/`"** (`README.md:32`): there are 18 files.
9. **Where the review is wrong, or should be sharpened:** head 1.3 §11 and 5.2 should say no gate of milestone 6 was passed (m6a open, m6a-2 never cut, m6c in part), and the last passed is m5c on 8 Oct; head 5.4's row "Gate m6c passed" is confirmed against the report. Head 1.5's "No test takes the player's road" can add: no playtest did either; the owner's first action was played with no order of his.

## 2. What the project already knew

| Finding | Known | Done |
|---|---|---|
| The boundary, the sandbox, no player Python | Not in these records | — |
| Director's reach and limits | R-38 (22 Oct, P0); R-61 `director: brief` drops `nobody_dies` | R-38 half mended; R-61 not seen mended here |
| The checkpoint / save and load | `--load` carried unrun through four gates (4c to 5c); the 5c audit's replay rule | built, never run at a gate by the owner |
| The true position | 5c, 8 Oct: "`the port` and `the depth of water` still give the true position away, on purpose, until the owner has played what is built" (`report-2.md:441-443`) | a deliberate deferral; the leak on the wire not in these records |
| The consent brief's promises | "to come": 13 Oct, 17 Oct, 18 Oct, 22 Oct | deferred to 55 by decision 51 |
| The newcomer's first hour | Not met: every playtest by the owner, the lead or a model with the primer | — |
| The guns left secured | Met 5 Nov, filed as "what held" | — |
| The purchase with the boat lost | The pay-first design recorded 5 Oct | — |
| The far world: sight across land | 18 Oct, finding 10 | routed to a note |
| The starter book on fore-and-aft vessels | 4 to 5 Oct | lost among small faults |
| Hand-kept tiers, flaky tests, the pace floor | The interim gate: the pace job failing "two to four of ten" on seven runs "read each time ... as the runner's day"; three known flakes on the lead's containers (`gate-m7-interim.md:29`, `115`) | "None re-pinned"; nothing changed |

## 3. The method, as these records show it

- **Who writes what.** The lead writes every gate report and every verdict line; from 4c on the "report" is a playtest folder, and the playtest notes are "drafted by the build session" with the owner's words marked (`2026-09-27-gate-3b/notes.md:8-9`, `docs/playtests/README.md:4-6`). The M7 interim was drafted by a builder (package 85). Two ship reports are written by builders "for the owner, in place of your own test".
- **What a gate tested changed** from a live checklist with exact commands and lines to see (m0 to m4a) to "the owner's runs" and his notes, then to a list of what the packages built (m6c, the interim). The checklists stopped being ticked from the first gate.
- **Re-cuts and letters in these records:** m4b cut three times, m5a twice, m6a then m6a-2 then folded; package 37 ran b to p, 39 a to f, 40 b and c, 42 a and b, 45 and 45c, 79 a to d, 58 a and b, 106 a and b.
- **A fault traced to its step, done honestly:** the lead records its own error at m4b ("That was the lead's error in spec M4 §13, not the package's", `gate-m4b.md:5`); the 5c audit records "the reason on record is partly wrong" (`report-2.md:410-431`); the dispatches test records a fix made the same day. The records do not trace the gate process's own lapses: m6a's verdict, the deferred items' loss, the README's claim.
- **A ruling put well:** the M7b review's "For the owner: decisions this review can't make" (`...Review.md:835-845`): six questions, each a choice he can make. **Put badly:** the owner's J1 reminder as the lead wrote it, "the dip the heel plus the roll's amplitude on the lee side and the roll less the heel on the weather side, so the small ships' weather ports shut in bands of wind in a seaway ..." (`gate-m7-interim.md:85-88`), one sentence of 140 words ending "tune the foot, the six inches, the minute and the roll's share, old beside new, and rule".

## 4. The cost, as these records show it

- The whole suite at gate 5c: `2981 passed, 9 xfailed in 1179.13s (0:19:39)` on four workers (`report-2.md:403-405`); 842.59 s on the owner's Windows machine at m5c-c's start (`CHANGES-m5c-c.md`, "The suite at the start"); the interim's cloud runs 7 to 20 at 4,250 to 4,337 passed, the pace job 155 to 300 s and failing on seven runs (`gate-m7-interim.md:29`).
- One gate's review: `report-2.md` 536,638 chars, `report.md` 215,204, `handover-audit.md` 110,825, `evidence/` 2.2 MB: some 860,000 characters of report for one gate.
- The M7b review: 99,091 chars plus sixteen reviewers' files (about 450,000) plus 4 MB of extracted transcripts.
- Model cost met in play: two API seats "about 16.3 M prompt tokens in about two hours"; "the OpenRouter credit that ran out" (R-34, `...Review.md:561`); a director's stand-by "about 1.3 M characters in four hours" (R-26); a 13-hour day took "two hours and a half" of real time (dispatches finding 16).
- Records against work: the gates folder 273,857 chars; the playtests 81.8 MB, 13% of the repository.

## 5. The record as a record

- **Could the owner find the state of a gate today?** Only by reading three files against one another: the README says passed, the gate says in part, the proposal says deferred, and the deferred items are in no later gate.
- **Current against history:** each gate's head is rewritten as later rulings land (m5c's line 7 "As the build stands after the fold-in"; m4b-3's "first attempt" inside the third), so a report is neither the gate as cut nor the gate as it stands. m6a-2 says it "stays as drafted".
- **Left out:** a register of findings and their state after 8 Oct (the 5c ledger is the last); any record that the 4c to 5c `--load` item was run; any playtest by someone new to the game.
- **Held and unlikely to be read:** 60.7 MB of saves and transcripts "kept for the record ... not read by any test".
- **Honest:** yes, in substance. The lead's errors are written plainly where found. What the record does not do is check its own summaries: the README's status line is the clearest case.

---

## The ten things that matter

1. **No gate of milestone 6 or 7 has been passed; the last pass is m5c (8 Oct)** with its lead's watch withdrawn and its m5c-c half provisional. `gate-m6a.md:3`, `gate-m6a-2.md:3`, `gate-m6c.md:3`, `gate-m7-interim.md:3`; `gate-m5c.md:3`.
2. **"Gate m6c passed" is false by the gate's own report**, and three of its five items run failed their expectations. `README.md:5`; `gate-m6c.md:3`; `docs/playtests/2026-10-17-gate-m6c-owner-runs/README.md:28-39`.
3. **m6c's eight deferred items are lost**: the gate they were deferred to was frozen unrun and the interim gate does not carry them. `DesignProposal.md:655,657`; `gate-m7-interim.md` (no regatta, seat hook, lugger, business).
4. **The interim gate is the builders' list of what they built, not run, and would have caught almost none of the review's player-facing findings.** `gate-m7-interim.md:50-73`; `data/scenarios/mahon.yaml:31`.
5. **Some 16,700 lines of post-cut modules plus 18,400 of ship tools have never been before a gate**; the two ship reports stand "in place of" the owner's test. `freesail/combat/`, `agents/director.py`, `world/{signals,squadrons,prizes,boats,water,needs,hulls}.py`, `tools/ships/`; `2026-10-30-pilot-indefatigable/testing-report.md:3-5`.
6. **The guns-secured trap was met on 5 Nov and filed as a success**; the owner's own first action gave no order. `2026-11-05-brig-off-falmouth-fully-crewed/case-study.md:36-39`; `2026-10-24-owner-first-action/notes.md:3-4`.
7. **The starter book's refusal on the cutter was found on 4 to 5 Oct and lost among "small faults".** `2026-10-05-gate-5c-review/report-2.md:2643-2645`; `evidence/L1-cutter-gemma.md:34`; `data/standing_orders/starter.orders`.
8. **The checkpoint's load was carried unrun from 4c to 5c**, the gate the review's checkpoint finding would have needed. `gate-m4c.md:3`, `gate-m5a.md:3`, `gate-m5b.md:5`, `gate-m5c.md:77`; `freesail/core/replay.py`.
9. **R-38 and the "to come" sentence, each recorded as dealt with, are open**: the limit fails open on an unknown word; the brief still promises a director to come. `...Review.md:570,595`; `agents/director.py:420-421`; `docs/agents/ConsentBrief.md:13`.
10. **The saves carry the owner's profile folder name (32 times, 21 files with related paths) and make up 61 MB**; no e-mail or key. `docs/playtests/2026-10-25-to-27-owner-playtests-70-72/saves/*` (`director.brief.source`); `docs/playtests/README.md:16-17`.

## What I did not read

- The saves, checkpoints, logs, runner logs, transcripts and extracted transcripts (listed and grepped only), the regatta results, the pictures.
- Of the gate-5c review: most of `report-2.md` (536k; read A, B, its ledger's tally and sections by search), `report.md` and `handover-audit.md` (not opened beyond references), `evidence/` (three files by search).
- Of the M7b review: §1 to §4 and the appendix; the sixteen reviewers' files and `work/all-findings.md` (only lines found by search).
- `review-of-the-local-work.md` beyond its head and outline; the two testing reports beyond their first sections; the drafts of the consent brief; the journals and `refused*.md` files; `lead-officer-replies.md`; `captain-debrief.md`.
- The gates m0 to m5b beyond their heads, verdicts and checklist lines.
- `CHANGES-m5c-c.md` beyond its head, outline and the lines cited.
