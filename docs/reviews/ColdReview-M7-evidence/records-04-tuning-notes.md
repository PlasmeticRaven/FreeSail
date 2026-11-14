# Records reader 04: `docs/dev/TuningNotes.md`

The tree at 504a250 (the clone's head is the review's own commit b72ed89, which adds only the review's files). The record is 28,704 lines and 2,912,718 bytes. Nothing was changed but this file. No suite was run.

## What I read, exactly

- `RECORDREADERS.md` whole; `ColdReview-M7.md` whole (heads 1 to 5).
- **Whole:** lines 1 to 600; 5741 to 6140; 11481 to 11880; 17221 to 17620; 22961 to 23360 (four parts at even fifths of the file); 27205 to 28704 (the last 1,500).
- **By search, with context read:** the ten pins below; 30 re-pin entries out of 173 lines that name one (lines 145, 1108, 2168, 3343, 3778, 3975 to 3990, 5380, 5653, 5762 to 5789, 6047, 6688, 7625 to 7670, 8382, 9897 to 9915, 10806, 11445, 13225, 13468, 13790, 15318, 15844, 17379 to 17392, 18020, 19974, 22596, 23136 to 23143, 23957, 24367 to 24395, 25699, 27239 to 27251, 27757 to 27762); the three "Open, for the lead" sections (7680 to 7735, 10603 to 10700); the suite-timing sections (1120 to 1155, 3323 to 3352); 31 "not mended" lines.
- About 7,300 of the 28,704 lines read whole (a quarter); the rest seen only through grep.

## The map

**Headings:** 912 in all: one `#`, 130 `##`, 778 `###`, 3 `####`. There is **no index**, by subject, by constant, by truth number or by test. Lines 1 to 7 still describe the file as "Two parts": package 10's starting point and package 10's record. They have not been true for 128 sections.

**Order:** the order in which sections were appended at merge. It is not by subject, and not strictly by date or by package:

- lines 9 to 3240: by milestone (M1 to M5);
- lines 3240 to 4408: M6 by package;
- from line 4409: by package in merge order. The packages run 45, 45c, 43, 44, 43b, 42b, 50, 52, 54, 53, 57, 56 and on; 79c and 79d (dated 2026-10-29) stand after package 75 (2026-11-10); package 105 is split between lines 27153 and 27639, and line 27641 says so.
- A finding and its mend can stand in reverse order. Line 28368 records the checkpoint's chart as mended. Line 28423, later in the file, reports the same fault as found. Line 28655 still lists it under "Found for others, not mended".

**Size by subject** (summed from the `##` sections):

| Subject | Lines | Share |
|---|---:|---:|
| Package 75, the ships | 6,919 | 24% |
| The chart blocks and the chart sessions | about 5,840 | 20% |
| Milestones 0 to 5 together | 3,231 | 11% |
| The single largest section, the *Neufchatel* (line 13866) | 1,700 | 6% |
| The director's milestone, its packages 50, 52 and 62 | about 460 | under 2% |

**References into it:** the code, the data and the tests name the file 329 times from 143 files, 82 of them in `tests/test_known_truths.py`. Almost all of these give a package, not a line or a heading. One test asserts sentences inside it (`tests/test_practice.py:594-600`).

## The ten pins, used as a builder would use them

"Calls" is the number of tool calls it took to find the answer in the record.

| # | Pin (tree) | Calls | Found | Reason or history? |
|---|---|---:|---|---|
| 1 | Square sail lift peak 1.12 (`data/sail_classes.yaml:43`, at 40°) | 2 | l.126 (1.4 at 28° to 1.12 at 35°, truths 1 and 4); l.281 (moved five degrees, to 40°, for Fincham's brace limits) | **A reason, then a history.** The two places agree. But the data file's own header (`sail_classes.yaml:28`) still says "1.12 (square, at 35°)": stale since 3b. |
| 1b | The generator's studding coefficient 1.25 (`tools/gen_ships.py:136`) against the engine's 1.44 | 2 | l.131 (studding peak 1.35 "more drag") and l.142 (`PEAK_COEFF` studding 1.25), **rows 7 and 18 of the same table of package 10** | The drift the review found (F2.1) was born in one package's one table and is in the record from the first day. hypot(1.35, 0.50) = 1.44. No later entry notices it. |
| 2 | Frigate brace limits 62/64/66/68 (`data/ships/frigate-36.yaml:195-219`) | 1 | l.281 (Fincham art. 102); l.36 (Luce, the earlier 55 to 62); l.11849 ("only with a source") | **A reason, with a source.** Consistent. |
| 3 | `CREWED_CAP = 3` (`world/crews.py:98`) | 2 | l.4888 (package 43) | **A reason, by measure.** The figures behind it disagree: 100 to 114 ticks a second with three crewed (l.4888); "about 140" (the code's comment, `crews.py:93`); 194 on the build machine and 281 on the owner's (l.5808-5813); 165 to 171 (l.23192). Each figure agrees that three is the most. |
| 4 | Pace floor 500 (`test_known_truths.py:2157-2163`) | 2 | l.406: half of 1,000 measured, "so four workers ... do not fail it" | **The reason's premise is gone.** 45 lines record the floor missed or met by a hair: 382 to 402 on the CI runners (l.3349), 246 (l.7479), 463 (l.10801), 471/474/486 (l.27828). The record itself concludes "this container is under the floor whatever the tree" (l.25938) and "the floor sits inside the machine's spread ... a finding for the lead, not mended" (l.27834). The constant `BUILD_MACHINE_MEASURED = 1000` still stands. |
| 5 | `GATE_5A_DAY_DIGEST = "1680cb1391720dd8"` (`test_known_truths.py:2525`) | 2 | l.7625-7633 (the well's order out of the starter book) | **A history, the best kind the file has:** what changed, the old and new figures, and "each re-pin was proven the starter's by restoring the absent row" (a toggle). |
| 6 | `WAR_FACTOR = 1.5` (`world/ports.py:339`) | 1 | l.1257 and l.1277 | **"judgement", no source.** The base prices are "FROM MEMORY" (l.1259). Truth 69's sum (l.1283) shows the double count the review found (Brest's tin 180 "by the file", then the half put on) and treats it as correct. |
| 7 | `CREWED_NM = 4.0` (`crews.py:90`) | (with 3) | l.4886: the tops make out her rig at four miles (`RIG_MADE_OUT_NM`, l.1367, Luce 1866) | **A reason.** |
| 8 | Frigate tack band `285 <= s <= 600` (`test_known_truths.py:420`) | 2 | l.281: "the tack comes in 298 s (floor moved from 300 to 285)" | **A history, and the band was moved to fit the build.** The test's docstring says "Luce's five to ten minutes", which is 300 s. |
| 9 | The officer's handover budget (`tests/test_officer.py:945`, 23,000) | 4 | 16,384 to 17,000 (l.6271-6275); to 18,000 (l.6701); to 19,000 from 18,500 (l.10373); to 20,500 from 20,000 (l.10757); to 23,000 from 22,500 (l.24386-24395) | **A history.** "every package that lengthened his brief or his readings has given the budget five hundred more (the test's own comment keeps the history)"; ruled by the lead on 2026-11-10 (l.24778). The fault was named on 2026-10-17: "A local model with a sixteen-thousand context at the frigate's officer's station starts within a hair of the handover's ask: a note for the lead" (l.6273). The brief is now 13,516 tokens; the harness's constants are unchanged. |
| 10 | Signal hoist 60 s (`data/evolutions/make_signal.yaml:20`) | 3 | l.9282 ("a minute a hoist") | **No reason beyond "from memory; judgement".** Package 76 later read Popham 1803 whole (l.25074) and did not revisit the figure. |

**The sum.** Every pin was found, in one to four calls, by grepping the constant's name or its number. None could be found by the file's structure.

- The physics pins of package 10 and 3b (1, 2, 7) have reasons with sources.
- The world's pins (3, 6, 10) are judgement, honestly marked so.
- The test pins (4, 5, 8, 9) have histories, not reasons. For two of them (4, 9) the record shows the reason has lapsed while the number was kept.
- Where several answers exist (3), they disagree in figures but not in conclusion.

## How pins are moved, as the record shows it

**Counts:** "re-pinned" 61 lines; "re-pin" 72; "pins moved" or "pin moved" 103; "old beside new" 118; "digest" 502; "bisect" 51; "toggle" 35; 16 headings `### Pins moved`. The re-pin lines found number 173, of which I read the 30 listed above.

**What a re-pin's record holds**, at its best (l.7625, l.9897 to 9915, l.23136 to 23143):

- the pin's name, its old and new figures, and the commit;
- the cause in the code (often "the line's words": l.3337, l.5382);
- whether it was proven by a toggle or a bisection;
- the suites run on that tree, with counts.

From package 98 on, a standard sentence is written: "No digest moved, no kept save and no pin", or "the pins moved are those listed above, each the ruling's" (l.27273).

**What it does not hold:**

1. **Whether the change in the game was meant, judged by anyone but the builder.** The builder states the cause. The lead re-pins at merge, sometimes without repeating the proof: "re-pinned by the lead with the old figures beside ... the lead did not repeat the bisection" (l.7652). The owner is never shown a re-pin.
2. **The player's view of the change.** It does say what the ship did differently, often well (l.3975 to 3990: "the stranger spoken three minutes sooner"). It never says whether that is better or worse seamanship.
3. **Whether the new figure is right.** Package 37p's method is stated plainly: "by running the pinned tests and taking each figure the run gave where the pin stood" (l.3977). A re-pin is a new measurement, not a check.
4. **A register.** Each re-pin is prose inside a package's section. There is no list of how often a pin has moved. The tack band, the budget and GATE_5A's digest (five lines and three digests in its test comment) can be traced only by grep.
5. **The stale pins left.** "the lee-shore trial's digest was stale on the trunk ... not this package's, and not re-pinned here" (l.22593-22596). "Truth 88's pace test is marked `pace` by hand ... but `_is_pace` knows ..." (l.8386).

## The suites' cost and the machines

| Date (package) | Measurement | Place |
|---|---|---|
| 2026-10-01 (32c) | 2,098 tests; the fast tier of 1,866: 60 to 162 s at `-n 4`; the whole suite 990 s quiet, 2,145 to 2,369 s loaded; the slow tier 463 to 875 s; CI fast tier 2 to 3 min | l.1124, 1140-1145, 1154 |
| 2026-10-09 (the lead) | `test_known_truths.py --slow -n 4`: "an hour under that load" | l.3317 |
| 2026-10-17 (50) | fast tier 3,320 passed; **the slow tier whole 3,612 passed in an hour and three quarters**; pace 6 in 151 s | l.5947-5961 |
| 2026-10-17 (52) | slow tier alone 296 in half an hour | l.6063-6066 |
| 2026-11-05 (75 L2, L3) | fast tier 6,024 in 32:13, then 6,272 in 34:54, then 6,276 in 40:02 | l.13027, 13205, 13270 |
| 2026-11-06 (82b step 3) | fast tier 5,938 in 42 min 28 s; slow of touched files 2,972 in 1 h 3 min; pace 13 in 5 min 12 s | l.23286-23289 |
| 2026-11-06 (82b step 4) | fast tier 6,309 in 45 min 7 s; the slow tier "in two halves so neither met the two-hour limit a single run of the whole met" (1 h 0 min 35 s + 17 min 11 s) | l.23346-23356 |
| 2026-11-07 (75 B2 to B4) | fast tier 6,900 in 56:17; 6,725 in 48:43; 6,912 in 55:17; 7,038 in 42:36 | l.13538, 14684, 15358, 15854 |
| 2026-11-10 | fast tier 7,097 in 31:56; "the tiers as separate tasks under its two-hour cap" (six times, l.24251 to 24713) | l.18689 |
| 2026-11-13 (111) | fast tier 7,559 "in 54 minutes on a loaded machine"; 7,594 in 59 minutes | l.27528, 27548 |

**Growth:** in six weeks the fast tier went from 1,866 tests in one to three minutes to some 7,600 tests in half an hour to an hour on the same kind of four-core container. That is four times the tests for twenty to thirty times the time.

- The tiers were measured by `--durations` once (l.1128: "re-measure ... when the fast tier grows slow"). The word `--durations` appears three times in the file; the measurement was not repeated.
- "Restart" appears 24 times; runs "lost to" a restart or a cap appear repeatedly (l.1146, 5147, 27942, 28288); the two-hour cap of a background job is met at least fifteen times.
- Package 111 timed its own cost: +68 s serial to the fast tier and +89 s to the slow (l.27353-27358). This is the only package I found that costs itself.

## Faults the notes record as known and left

**Counts:** "Found on the way" 144; "for the lead" 268; "for the owner" 30; "not mended" 31; "not fixed" 6; "open item" 19; "deferred" 2; "left for" / "left to the" / "Left as" 77; three `## Open, for the lead` sections.

A fault that is later mended is **not marked in its first place**:

- the swing at the turn of the tide (l.7685, mended at l.8115);
- the Channel east's tide (l.11693, mended by package 89, l.20001);
- the remote door's sentence (l.23101 "stands unchanged"; mended in `agents/remote.py:1041`);
- the checkpoint's chart (l.28655).

The reader cannot tell from where a fault is written whether it is open.

The twenty most consequential for a player ("code" means checked at 504a250 by me):

1. **The same report sent down again and again**; "the rules master, called, does not come up ... the mate sends five times in twenty minutes" (l.23272-23278, 2026-11-06). Code: `world/reports.py:410-419` reports every reportable line of the minute with no check against the last report. **Still there** (the review met it, head 1.5).
2. **Vessels steering across the land.** 8 of 35 vessels were on land in naval-cruise; the prototype to stop it "exists only as described here" (l.28237-28240). Code: no `_led_round` or `_flight_clear` in `world/ships.py`; only `_off_the_land` (`ships.py:1283`, the goal's square). **Still there.**
3. **The officer cannot see how long a job has left**, so a model belays it three seconds from done (l.10648-10668). Code: `api/readings.py:1692-1722` gives doing, waiting and belayed, with no time. **Still there.**
4. **The frigate-36's quarterdeck guns are wrong** (eight carronades and two 9s where Winfield p. 143 gives six and eight); the owner's ruling was to leave it (l.10611-10621). Code: `tools/gen_ships.py:4672-4788` "INCORRECT, pending correction". **Still there, by the owner's ruling.**
5. **A kedge cannot be weighed aground** (l.7699). Code: `evolutions/scripts.py:7524-7525`, `WeighAnchorScript.check` refuses "she is aground". **Still there.**
6. **The pace floor is a coin toss on every machine the project has** (l.25938, 27834).
7. **Determinism is per C library.** The five Windows-only passages (l.7663-7670, 2026-10-23, booked "a package before the gate"). Nine passages moved when the cloud's image changed glibc (l.22871-22912): "The pins stand as they are; they are the 24.04 machine's." The remedy applied: `whole-suite.yml:42,58` pins `ubuntu-24.04`. `ci.yml:52` still runs `ubuntu-latest` and `windows-latest`.
8. **A sixteen-thousand-token local model is asked for its handover at once** (l.6273; the budget raised since; table above).
9. **A long telegraph signal holds the hands a tack wants** (l.10670-10674).
10. **Order words the game itself prints are refused** ("the sail bearing ESE", "belay making signal"; l.10675-10682).
11. **The open ocean's tide is the Channel's eleven gauges; at level 1 the water's level is counted twice**, so 765 coarse cells of land flood at mean tide (l.28215, 28487-28497). Measured, "Put to the lead and not yet answered" (l.28668).
12. **A ship sails through the Eddystone and the Longships**: no rock under the lights (l.27380-27381).
13. **The business's land guard refuses the way in or out of 25 of 90 ports**, so no trader is drawn for them (l.27377-27379, 28307-28309).
14. **Every blockade is Brest's book, a frigate and a brig, whatever the port** (l.11550-11559).
15. **The director's say-as still answers a line naming nothing "as said"** (l.27256-27260).
16. **An unanswered question is sampled again every tick**, bringing the nudge within three ticks (l.23116-23119).
17. **A visitor's `say` at the prompt speaks as "the captain"** of the ship he visits (l.23328-23332).
18. **The wars table makes the Canaries hostile to a King's ship after 1808** (l.28220-28221).
19. **The far quarter galleries stand proud of the hull by up to 1.27 m** in the picture (l.12699).
20. **The physics' own strict expected failures:** lying a-try goes astern at 4.4 to 5.1 kn (truth 28, l.294 and 305: "A physics question for the owner, not a constant to move quietly"); the wear loses too little ground (truth 11, l.199); the watch's plain-sail times (truth 18, l.257); the night's sleep and the night's call share one constant (l.450). All four still xfail (`test_known_truths.py:465`, 729, 1263).

Checked as mended since their first record: the swing at the turn, the Channel east's tide, the remote door's sentence, and the checkpoint's chart (`core/replay.py:567-575` uses `chart_holding`).

## The five questions

### 1. Where the record and the thing differ

- The file's own head (l.1-7) describes two parts. It has 130.
- `data/sail_classes.yaml:28` says the square peak is at 35°; the array puts it at 40° (l.281 moved it).
- The generator's `PEAK_COEFF` studding 1.25 has disagreed with the engine's curve since the table that set both (l.131 against l.142). The record holds the drift without seeing it.
- "Not mended" items stay so in the text after they are mended (four found, above). So the record overstates what is open, and the reader cannot trust it either way.
- **Corrections to the review:**
  - §3.2 says the project's tests "pin different digests for Linux and Windows". The record shows something worse: the pins are one C library's. The project knew on 2026-10-23 (l.7663) and on 2026-11-05 (l.22906-22912), and answered by pinning the runner image, not by finding the source.
  - §3.7 says the cloud runner gives 480 to 520. The record's figures are wider: 382 to 677 (l.3349, l.27833).
  - The review's "budget raised nine times" is confirmed as a ruled practice (l.24386-24395, l.24778).

### 2. What the project already knew

- **The repeated report** (2026-11-06, l.23272).
- **The officer's handover at a small context** (2026-10-17, l.6273).
- **The pace floor's edge** (from 2026-10-01, l.1150; "a finding for the lead" 2026-11-13, l.27834).
- **Determinism across machines** (2026-10-23, l.7663; 2026-11-05, l.22906).
- **The generator's copy of the force law** (in the record from package 10 without being seen: l.142).
- **The war counted on prices already high** (in truth 69's sum, l.1283, unseen as a fault).
- **The far world's ships over the land** (the owner's note, l.28232; left to package 61).
- **The checkpoint's two charts** (found and mended 2026-11-13, l.28368).

The boundary, the sandbox, the wire's truth, the boat-lost purchase and the director's holes are not in this record. Line 13115 shows the builders' own action casts the guns loose by order, the road the review says every test takes.

### 3. The method

**The builder runs** ruff, the fast tier whole, the slow tier "of the touched files and the known truths", and the pace "alone and last", each at a pinned hash. The report adds "the tree reported differs from <hash> by this paragraph alone" (from package 98).

**"Green" has changed:**

- 2026-10-17 meant the whole slow tier, run once (l.5951);
- by November it meant "the whole suite is the lead's in the cloud at the merge" (l.11545, 23029, 23167), with builders running parts;
- pace failures count as "the machine's spread" (l.27828-27835).

**The lead decides alone:**

- the re-pin practice (l.24778);
- the order of merges (l.27535);
- the steering stopped "on the pace" (l.28226).

**Put to the owner well:** "**Told plainly, for the owner: 218 m² cannot stand with the boom clear of her taffrail.**" (l.11825); and the Winfield ruling with "What correcting it would move" (l.10619-10627).

**Put badly:** "**Left by the lead to the owner's test, for the eye:** lee helm at her own close-hauled course, -0.95° at six points and -0.53° at 70°, against the *Bellona*'s weatherly helm (Bel §2.1, §9; Lavery 1985 p. 9)" (l.11867-11869). A non-programmer cannot sail six points with a helm figure in hand.

**The lead's own errors are written:**

- "The cause is the lead's" (l.3339);
- "the lead's error in the spec" (l.361);
- "The lead's own fault" (l.3688);
- the lead's correction of a misread clock (l.7638-7646);
- "My proposal was wrong" (l.27458, a builder's).

### 4. The cost

- The suites' growth (table above).
- At least fifteen meetings with a two-hour cap; runs lost to container restarts (l.1146, 5147, 27942, 28288).
- The record itself: 2.9 MB, about a quarter of it the ship designs of package 75 and a fifth the chart blocks. The director's guardrails, the review's most serious finding, take under 2%.

### 5. The record as a record

**Could the owner find the state of a thing today? No.**

- There is no index, and the order is that of merges.
- A finding and its mend can be thousands of lines apart and in either order.
- A fault mended is not marked where it was found.
- A pin's current reason is wherever the last package that moved it wrote.

**It is honest, unusually so.** It records the lead's own errors as plainly as the builders', and it says "judgement", "FROM MEMORY" and "unverified" at every figure that is.

**It holds what nobody will read:**

- per-tile byte counts;
- 26-row helm sweeps of a knob;
- the suites' pass counts for every step's tree;
- the hashes of trees.

**It lacks what it should hold:**

- one current line per pinned number: its value, its reason, how many times it has moved, and whether it is meant;
- a list of open faults kept current.

## Does the file do the work it was made for?

**In part, and less with every package.** Its stated work (l.6-7) is to be "why the numbers are what they are", read beside the truths.

- For the first 600 lines, package 10 and milestone 3b, it does that well. Each constant has one row: before, after, why, and the truth it moved.
- From milestone 5 on, it becomes the builders' report of each package: what was built, what was found, the suites' counts and the re-pins. The reasons for numbers are still there, but buried. Pin 9 took four calls and six places to trace. Pin 4's reason has been false for a month while 45 lines record it failing.

At 2.9 MB in merge order, with no index and no marking of what is current, it is a diary that the tests point into by package name. It answers "what happened in package N" well. It answers "why is this number this number today" only for someone who greps the number and reads every hit.

## The ten things that matter

1. **Determinism hangs on the C library; the remedy was to pin the CI image.** Record: l.7663-7670, l.22871-22912. Tree: `.github/workflows/whole-suite.yml:42,58` (`ubuntu-24.04`) against `ci.yml:52` (`ubuntu-latest`, `windows-latest`).
2. **The pace floor's premise (1,000 measured) has lapsed.** It is now inside every machine's spread and recorded as missed some 45 times. Record: l.406, 25938, 27834. Tree: `tests/test_known_truths.py:2157-2163`.
3. **The officer's handover budget is raised by each package, as ruled practice, while a 16k local model is now asked at once.** Record: l.6273, 24386-24395, 24778. Tree: `tests/test_officer.py:945`; `agents/harness.py:341-365`.
4. **A re-pin records cause and figures but not whether the change was meant, and is sometimes "the figure the run gave".** Record: l.3977, 7652, 22596. Tree: the comments beside every pin in `test_known_truths.py`.
5. **The report repeated to a captain below was known before the review met it, and left.** Record: l.23272-23278. Tree: `world/reports.py:410-419`.
6. **The vessels on land were measured, a prototype was built and discarded, and nothing is in the tree.** Record: l.28237-28309. Tree: `world/ships.py` (only `_off_the_land`, l.1283).
7. **The generator's drift from the engine's sail law was born in package 10's own table.** Record: l.131 against l.142. Tree: `tools/gen_ships.py:136`; `data/sail_classes.yaml:118-119`.
8. **The tack band was moved below its source to fit the build.** Record: l.281. Tree: `tests/test_known_truths.py:403-420`.
9. **No index, merge order, and mended faults left marked open.** Record: l.1-7, 7685 against 8115, 23101 against `agents/remote.py:1041`, 28655 against `core/replay.py:567-575`.
10. **The suites' cost rose some twentyfold in six weeks, measured but never re-tiered.** Record: l.1128-1145, 13538, 23351, 27548.

## What I did not read

- About three quarters of the file, lines 600 to 27205 outside the four parts and the searched passages. That includes most of package 75 (6,919 lines), most of the chart blocks, packages 70 to 74, 76 and 84 whole, and the director's packages 62 and 67.
- The 143 lines naming a re-pin that I did not open.
- The other records under `docs/dev/` that this file points to (the work packages, `ChartBlocks.md`, the design notes).
- I did not run any test to confirm a pin's current figure, and did not check the twenty faults beyond the five verified in code and the four found mended.
