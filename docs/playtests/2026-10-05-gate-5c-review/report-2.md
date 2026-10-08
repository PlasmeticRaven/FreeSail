# Gate 5c playtest review: second edition

Written 2026-10-08 by an editor, a Claude Opus 5.5 session in Claude Code, at the owner's
request. It is made from the first edition of this review, `report.md` in this folder, which
was written between 5 and 8 October by the review's lead session and is the record, and
from the audit of the build made the same day, `handover-audit.md` in this folder. Neither
is changed. Nothing in the build folder or the gate folder was changed to make this one,
apart from adding this file.

## A. What this is, and how to read it

### A1. What this is

The first edition began as this:

A review of everything played and noted at gate 5c so far, written to answer four questions:

1. What happened in each playtest, and what did it show?
2. What does the provisional update `FreeSail-gate-m5c-b` change, and is it sound?
3. How do the owner's and the playtesting model's notes
   (`m5c playtest and model notes.txt`) read against Milestone 5's own documents and the
   design proposal?
4. Of everything found: what can be built now, what needs a ruling or more design first, and
   what should be pushed back on?

That first review was read-only: nothing in `FreeSail-gate-m5c` or `FreeSail-gate-m5c-b`
was changed to produce it, apart from adding its folder.

It then grew in three layers over a week, in the order things happened. Sections 1 to 9 are
the first review of 5 October, with the owner's answers of that day. Section 10 was added on
7 October and is the first game played on the build that holds the follow-up work. Section
11 was added on 8 October and is the second such game. A status block at its head was added
to after each step. In that week most of what the first review recommended was ruled on by
the owner, built, played, or overtaken by a later finding, so that one subject (the
reckoning, the anchors, the officer's station) is spread over six sections of it.

This edition holds the same substance in another order, for a reader who has seen nothing
since gate 5c was cut as `FreeSail-gate-m5c` on 2 October. Each finding is followed through:
what was found and on what evidence, what the owner ruled, what was built and in which
package, how it did in the games played afterwards, and what is left. It is not a summary.
The ticks, the ship's times, the quotations and the tables of the first edition are carried
over as they stand. What was left out is listed in appendix 3 with the reason for each.

**What the editor did and did not do.** The editor read the first edition whole, the build
folder's `CHANGES-m5c-c.md`, the plan and the four briefs in its
`docs/dev/M5-WorkPackages.md`, and the owner's notes. The editor did not check the code.
As first written, this edition said that a thing was built on the word of the changes file,
the briefs and the first edition, which records the lead's own checks of each package.

**The audit.** An auditor, a Claude Opus 5.5 session that had seen none of the work, checked
the build itself the same day, in the code and the tests, and wrote `handover-audit.md`.
It is carried here whole, in the auditor's words: how it was made and what it did not check
in A5; its own short version in B5; the gate, item by item, in part M; what changed in the
tree, where the claims and the code part company, its advice by package and what the owner
must decide in part N; and its ledger in appendix 1. Every statement of status in this
edition was then set against it. Where the audit found otherwise than the edition first
said, or narrowed a finding, the statement is corrected in its place and says that the
audit found it. Where the lead added a note of its own to the audit, that is said to be
the lead's.

### A2. How to read it

- **The order.** Part B is the short version. Part C is what happened, by date. Part D is
  the owner's rulings in one table. Part E is the ten games. Part F is the builds and the
  packages. Part G is the findings by subject, and is the body of the report. Part H is the
  owner's and the models' notes, item by item. Part I is the first review's recommendations,
  each with what came of it. Part J is where the review pushed back and where it was itself
  wrong. Part K is what is proposed now and waits on the owner. Part L is the gate as the
  review saw it from play. Parts M and N and appendix 1 are the auditor's.
- **Letters and numbers.** The parts of this edition are lettered, so that "G3" cannot be
  taken for a section of the first edition. The build's changes file and its briefs cite the
  first edition by number ("the review's 5.6", "the report's 8.2", "section 9", "10.6").
  Appendix 2 says where each of those sections went. "M5", "M6", "M7" and "M8" are the
  game's milestones, as in its own documents, and not sections of part M.
- **The audit's own numbers.** The audit numbers its parts 1 to 5 and its nine disagreements
  C1 to C9, and those numbers are kept where it is carried. Its Part 1 is appendix 1 here,
  its Part 2 is part M, its Parts 3 and 4 are part N, and its Part 5 is in A5. Inside those,
  "Part 2, 2.4" or "C6" is the audit's own reference, and "the review's 8.2" or "section 11"
  is the first edition's. From the editor's parts they are cited as "M, 2.4" or "N, C6".
- **Times and ticks.** Times are ship's time. A number in brackets is a tick, for finding
  the place in a log. A tick is one second of ship's time. Every game is seed 7.
- **Who confirmed what.** In what comes from the first review, **(lead)** marks what the
  review's lead session confirmed directly in the code or the log. Everything else there is
  from a reader's report in `evidence/`, most of it checked by a second reader. What comes
  from games 9 and 10 is the lead's own reading throughout, unless it says "the officer
  says" or "not checked" or "not traced". In the auditor's parts each row says how it is
  known, by the marks **P**, **T**, **R** and **D**, which A5 explains.
- **Code references.** A file and line given with a finding of the first review is a place
  in m5c as it was cut; m5c-b differs only in what its diff changes (F1). The lines have
  moved since, and the briefs of 37f and 37g name functions for that reason.
- **"Today".** In what is carried over from the first edition, "today" and the present
  tense mean the day it was written: 5 October for the first review (games 1 to 8, on m5c
  and m5c-b), 7 October for game 9, and 8 October for game 10. Each such passage stands
  under a heading that says which it is.
- **Status.** The words used are: **built**, with the package; **partly built**; **not
  built**; **ruled** and **not ruled**; **later**, with the milestone; and **proposed**, for
  what waits on the owner. The audit found no numbered item of the four briefs left unbuilt,
  so a statement that a thing is built stands on the changes file and the audit together
  unless it says otherwise. "The audit found" marks a statement that the audit changed,
  settled or narrowed. "In no package" means that no package claims the thing. Where the
  audit settles such a thing, that is said; otherwise its ledger has no row for it, since
  its rows are the review's recommendations, the rulings, the briefs' items and what the
  changes file says was left.
- **The owner's words.** His rulings of 7 October and his notes are quoted as he wrote them.
  His answers of 5 October are given as the first edition recorded them.

### A3. Where things are

- **The gate as cut**: `D:\Projects\FreeSail\FreeSail-gate-m5c`. The baseline. Its saves are
  the games played on it, and its notes file, `m5c playtest and model notes.txt`, holds the
  owner's and the playing model's notes on the first eight games. The audit found that the
  folder is the gate as cut and then played in: every one of the 589 files of the gate's
  zip, `FreeSail-gate-m5c.zip`, is in it unchanged, with 87 more beside them (N, 3.1).
- **m5c-b**: `D:\Projects\FreeSail\FreeSail-gate-m5c-b`, with `CHANGES-m5c-b.md` and
  `m5c-b.diff`. The provisional update of 3 October.
- **The build**: `D:\Projects\FreeSail\FreeSail-gate-m5c-c`. m5c with the m5c-b diff applied
  and four packages built in it. `CHANGES-m5c-c.md` at its root says what each package
  claims. `docs/dev/M5-WorkPackages.md`, from "Follow-ups from gate 5c's first playtests,
  sorted" to "Integration", holds the plan as ruled and the four briefs. Its `saves/` holds
  games 9 and 10, and `m5c-c Notes.txt` the owner's six notes on game 9.
- **The review folder**: `docs/playtests/2026-10-05-gate-5c-review/` in the build folder.
  `report.md` is the first edition and `handover-audit.md` the audit. `evidence/` holds the readers' reports on the first
  eight games, the lead's measurements of games 9 and 10
  (`G9-brig-m5cc-measurements.txt`, `G10-cutter-m5cc-measurements.txt`), both stations'
  briefs as a model is sent them (`station-briefs-after-37g-second-pass.txt`), two officers'
  own accounts after their sessions, and the scripts in `evidence/tools`; its `README.md`
  says what each file is. `drafts/` holds the lean consent brief as the owner approved it.
  The first edition is also in m5c, at the same path, and the two copies are the same file
  to the byte today. This second edition is in the build folder only.
- **The game's own documents**: `docs/DesignProposal.md` (decisions 34 to 37 of its log are
  this week's rulings), `docs/TechnicalSpec-M5.md`, `docs/gates/gate-m5c.md`,
  `docs/agents/` (the consent brief, its commitments in `README.md`, the records under
  `consent/`) and `docs/dev/TuningNotes.md`.

By the owner's word of 2026-10-05: locally, in the gate folders, with no commits, and with
the GitHub repository and its worktree left alone. He folds the work in with the lead
session that works the repository. m5c-b set the pattern for that: a folder of its own
beside `m5c`, a CHANGES note, and one diff against m5c as cut.

### A4. Words coined in this work

A reader who left at m5c will not know these.

| Word | What it means here |
|---|---|
| m5c | Gate 5c as it was cut on 2 October: the folder `FreeSail-gate-m5c`, and the build of games 1 and 5 to 8 and of game 2 to tick 527,255 |
| m5c-b | The provisional update of 3 October, in its own folder: packages 37b and 37c. The build of games 3 and 4 and of the end of game 2 |
| m5c-c, "the build" | The folder `FreeSail-gate-m5c-c`, made on 6 October: m5c, the m5c-b diff, and packages 37d to 37g. The build of games 9 and 10 |
| 37b | Returning to the station: a model may be seated again any number of times (m5c-b) |
| 37c | The wind-shift and taken-aback lines of the log (m5c-b) |
| 37d | The saves, and the sight of land. Built 6 October in two passes |
| 37e | The account. Built 7 October |
| 37f | Lying to, and the ground. Built 7 October |
| 37g | The station's safety, and the deck, the leaving and the grant. Built 7 October, with a second pass the same evening that made the consent brief leaner |
| 37h | The pilot. Ruled on; its brief is not written |
| The last step, the follow-up pass | What the plan keeps for after the owner has played 37e to 37g: `the port` and `the depth of water` by the captain's means, and the small faults |
| The build's name, the stamp | Since 37d every save and checkpoint says which build wrote it: a name (`m5c-c/37g` today) and a fingerprint of the game's code and data |
| The lead | The review's lead session (Claude Opus 5.5 in Claude Code). It wrote the first edition, wrote the briefs, and checked each package after it was built |
| A reader | One of the sessions that read a slice of a game or of the code for the first review. Their reports are in `evidence/` |
| A builder | The session that built a package from its brief |
| The auditor, the audit | The session that checked the build in the code and the tests on 8 October, having seen none of the work, and its file `handover-audit.md` |
| Game 1 to game 10 | The ten games reviewed (E2). Game 2 is the *Harpy*, game 4 the *Speedwell*, game 8 the *Amazon*. The brig of game 9 is a new ship that her officer also called the *Harpy* |
| The account | The ship's position by the master's reckoning, which the chart is drawn about. The world keeps the truth and the captain keeps his account |
| The doubt | How far the master says he would trust the account. In the log's words, "good to" or "within" so many miles or cables |
| An observation | A noon latitude, a lunar, a time sight, a cast of the lead, a bearing, a fix |
| `take a fix` | An order new in 37d: cross bearings of two or three marks. "Good to" is the fix's own stated doubt, and the cocked hat is the triangle its three lines make |
| The one rule | 37e's single rule for believing any observation. The master sets his doubt of the account beside his doubt of the observation and **weighs** the two, **takes** the observation outright, or **keeps** the account |
| The master's tide | Since 37e the master works the tidal stream into the reckoning himself, from his own books. Before, he carried none unless the captain ordered one |
| A course that makes good | Since 37e `shape a course` gives the course to steer against the tide allowed, so that she makes the line good |
| `the nearest land`, land ahead | A reading and two lines of the lookout, new in 37d |
| The six recorded passages | The runs whose logs are pinned in `tests/test_known_truths.py`: the day of gate 5a, the 5b passage with its schooner and its thick weather, the 5c naval cruise and the 5c merchant passage. Their digests are the recorded constants |
| The expected failures | Seven are the owner's standing rulings on truths 3, 11, 18, 24, 26, 28 and 31. Two more since 37e are the two lost beats |
| The two lost beats | Two moments of the recorded passages that no longer happen: the schooner's Falmouth pilot hails and does not board, and the naval cruise chases the French brig and does not speak her |
| A door | The way a model reaches the game: the MCP bridge that Claude Desktop starts, the local runner for a model server on the owner's machine, or the REPL |
| A seating | One taking of a station by a model. Since 37g each seating has a key, which every call must carry |
| Relief | Another model taking a station that has been stood down or left |
| A stand-by | The tool by which a station waits for a bell, an interval or an event |
| A sample | What the harness sends a station when it wakes it: the log's lines since the last one, and the readings |
| The turn's budget | How many tool calls one sample may be answered with |
| The detector, a nudge, a pause | The harness watches for a model that is stuck. The contrary-orders detector, which since 37g counts only orders that undo one another, and the silence detector. It first tells the model (a nudge), then pauses its turns and asks the owner |
| A grant, an allowance | The captain's `you may ...`, which lets the officer give an order outside his domain |
| The general authority, the general grant | Since 37g, `you may work the ship`: the whole working of the ship, with a stated list kept back |
| The way out of danger | Since 37g an officer with the deck and no grant may, on his own word and giving his reason, put the helm over, heave to or let go an anchor |
| The three ways of leaving | Since 37g: the deck given back (he stays seated); a stand-down (`stand_down`, the amicable save and exit); a withdrawal (the token or `opt_out`) |
| The handover note, the fold | A note the officer writes for whoever holds the station next. At the local door the harness asks for one when the conversation has grown long, and the note then stands in place of the older exchanges |
| The handover reserve | Since 37g the note is asked for when less than this many tokens of the model's context are left (14,000) |
| The consent brief, the re-ask | The message that asks a model whether it is willing to take part. When one of its watched sections changes, every model with a yes on record is asked again |
| The lean brief | The consent brief as made leaner on 7 October: the question and the kind of thing a model would be agreeing to, with a station's particulars moved to that station's own brief |
| The seven words | Words the lead proposed adding to the lean brief, to name a fourth sign of a stuck model. They were not added |
| The drill | The short fitness trial that follows a yes before the officer's station |

### A5. How the build was audited, and what the audit did not check

This is the auditor's own account, in its words, from the head of `handover-audit.md` and
from its Part 5. How the games were read is in E1, and the lead's checks of each package
are in part F.

Written 2026-10-08 by a Claude Opus 5.5 session in Claude Code that had seen none of this
work, as the auditor's part of the handover. It is an account of what
`FreeSail-gate-m5c-c` holds today, set against the gate folder `FreeSail-gate-m5c`, and
checked in the code and the tests. The changes file (`CHANGES-m5c-c.md`), the four briefs
(`docs/dev/M5-WorkPackages.md`) and the review (`report.md` in this folder, its section 11
included) were read as claims to be checked, not as findings.

**What was done to make it.**

- Every file in the gate folder, in m5c-b, in the lead's four snapshots and in the build
  was hashed and the seven set side by side. The gate folder was also compared with the
  gate's zip, read without extracting it.
- The whole suite was run once, on four workers, and the linter once (Part 2, 2.5).
- The naval cruise was sailed under its own book, and four trials of what might bring its
  lost meeting back were made in memory.
- A few dozen orders were given to ships made in memory, to see what the build answers.
- The consent brief, the records and the stations' briefs were read by the game's own
  functions. The owner's four saves in this folder were loaded, with no tick run, and the
  last of them was replayed in memory.
- The code was read where a row of the ledger needed it.

Every script and its output is in my scratch folder, `handover-audit\` under the session's
scratchpad. Nothing was written in either folder but this file: a listing of every file's
size and time in both, taken before the suite and after it, is the same. No git command
was run. No model was seated, no consent question answered, no server started, and no
tool of the game's bridge called.

**How to read the marks** in the tables.

| Mark | Means |
|---|---|
| **P** | I ran it myself: a probe, a passage sailed, or the files read by the game's own functions |
| **T** | A test of that name is in the tree, its name says what the row says, and it passed in my run of the whole suite. I read the bodies of only a handful, marked "body read"; for the rest this is weaker evidence than a reading |
| **R** | I read the code or the document at the place named |
| **D** | From comparing the folders and the snapshots |
| "not checked" | I did not look. Where a row rests on the changes file or the review alone it says so |

**What I did not check, and why** (the audit's Part 5).

- **Anything in play.** No browser, no server, no model. Every statement here about what
  was played, by whom and what it showed is the review's.
- **The review's sections 1 to 7 and 10.1 to 10.5.** I read its status block, sections 8, 9,
  10.6 and 11. Its findings about the first nine games were not set against their logs.
- **The fast tier of the suite.** It was collected and counted, not run; the whole suite was
  run once.
- **The bodies of most tests.** See the mark **T** above.
- **The documents against the code.** For the spec, the primer, `Harness.md` and
  `TuningNotes.md` I checked which packages changed them and read a few places. I did not
  check that what they now say is what the code does, nor the tables of reasons for the
  recorded constants.
- **The measured figures**: 37e's tables of the account's error and the master's doubt, the
  merchant's distance off the Mingan, the gate's "account against the truth", the brig's
  head against the wind hove to, the cost of the fingerprint at start, the tick rate.
- **The two passes of 37d and of 37g's first build apart.** There is one snapshot after each
  package, so a file changed in a second pass cannot be told from the first by content.
  The second pass of 37g is the difference between the last snapshot and today.
- **The fixture saves by stage.** The snapshots leave out every folder named `saves`, so the
  three kept saves are dated by their files' times (3, 4 and 6 October) and not by a
  snapshot.
- **`m5c-b.diff` as a diff.** I compared the files it produced.
- **Whether any commit was made.** I ran no git command.
- **Eight test workers**, which the changes file says die at random.
- **Game 10's remaining claims**: the anchor left aweigh (tried, not reproduced), the fog
  reading's sentence, "put the helm over", the drill's count, the cause of the cast's
  mile in the tide's height, the runner sending one request three times.
- **`the nearest land` in every sample; `read_log` past two hundred lines; a standing order
  written under a grant that has ended; an act at the tick of a seating.**

## B. The short version

It is in four pieces, by date, because each later one changes the one before it. The first
three are the first edition's own. The fourth is where things stand on 8 October.

### B1. What the first review found (5 October, games 1 to 8)

**The gate's claim largely holds.** A passage between ports with a cargo, a pilot, the tide
and the anchor is a game, and a model can hold the officer's watch. Opus 5.5 kept the deck
for eight days and for six and a half, made the *Harpy*'s voyage pay, and near danger read
the situation better than the game's own words did. A local 27B model kept a 27-hour watch.

**The grounding and the near misses come from a handful of faults close to land, most of
them small, and not from the chart reckoning as such** (G1, G2, G3, G5):

- The lookout's distance is frozen until the ship herself has moved a mile. The *Harpy* was
  told "Penlee Point ... a mile" at under two cables, 27 seconds before she struck.
- Every bearing writes that frozen distance into the account. This is why a charted position
  stays wrong with bearings taken regularly, and why one bearing can move it miles.
- The sea breeze changes direction every few yards near a coast on a summer afternoon. It
  took the *Harpy* aback three times in her last thirteen minutes and filled the log with
  265 wind-shift lines.
- Nothing the lookout says is urgent, and the unnamed shore is never mentioned while a named
  headland is in sight.
- The pilot, "in charge" by the log, only speaks.

The *Harpy*'s officer anchored, warned twice, and anchored again 22 seconds before the
strike. The captain had taken the con on a chart that was wrong.

**Three readings give the true position away** (`the port`, `the depth of water`, and a
bearing of any sail) while the honest channels are coarser than a man's eyes.

**In the harness** (G12) the weightiest faults are these: a seat is found by the station's
name alone, so another door's calls ran under a seated model's name; the turn budget can
refuse the leaving tool and drops calls without a line in the log; a stand-by takes one
condition, has no bound, and is not broken by a dragging anchor or fog; a paused officer
keeps the deck while the ship sails on; the contrary-order detector was wrong 29 times in 31;
and a station cannot read its own journal.

**The notes** are confirmed in the main. A dozen of the model's points do not hold as
stated, and several of the owner's are better met another way (parts H and J).

**The gate itself** is not fully played: the naval cruise was never run, and the lead's own
watch is not in the record (part L).

The first review also gave a verdict on m5c-b: carry all three of its parts, the re-seating
rule after its opt-out path is mended and the two log rules with a floor and a change of
key, and apply the diff rather than copy the folder. And it asked that one thing be settled
before the harness was changed: what happens to saved games with a model aboard, which no
longer replay once the rules that wake a station change. Both have been done (F1, G14).

### B2. What the first game on the build showed (game 9, 6 October, on 37d)

The owner took a merchant brig from Falmouth into Roscoff alone, and Opus 5.5 as officer of
the watch took her out again, round Ushant and up the Goulet to Brest road: five days, 78
hours with the deck, nothing carried away and no ground touched. The game was replayed
exactly on its own build, which is the first real test of the save rule, and every figure
below was measured from that replay.

**Package 37d did what it was for.** With marks in sight and fixes going, the account stood
within one to five cables of the ship. The landfall bearing took it from seven miles out to
under one. The lookout's distances followed the ship in, and its one urgent cry came five
minutes before she passed the Mingan at a cable and a quarter.

**The owner's six notes are all borne out.** The sharpest of them:

- The master's doubt is about a tenth of what it should be in these waters. Without an
  observation the account went wrong by a mile an hour or more, and the doubt grew by a
  tenth of that. Hove to it does not grow at all, and repeated casts of the lead shrink it.
- The lunar did overrule the better account. That was never part of 37d; it became the first
  item of 37e. The same rule let a good noon latitude be ignored.
- The brig came through the wind in four heave-tos of seven, and `fill away` then took her
  back through it.

**The officer's list needs sorting before it is built from.** Most of it is right. Its
ground-tackle items are not what they looked like from the deck: nothing overran; `let go`
veers a scope of its own, and with an anchor named, `veer ... to 100` adds a hundred fathoms
to the anchor she rides by. The anchors in the Goulet did drag, about two cables in eight
hours on bad ground.

**Three things neither of them noted:**

- The harness paused the officer in the Goulet, three minutes after the Mingan, for four
  small alterations of course. Its detector spoke eleven times in the game and was wrong
  every time.
- `take a fix` chose marks three to seven miles off with nearer ones in sight, its "good to"
  is too hopeful, and at anchor it moved a right account by a mile.
- Four pilots boarded unasked; one left before she had gone in, and one boarded a ship that
  was leaving.

What it changed in the plan: one rule for when an observation is believed; the package that
was to follow 37d built as two, 37e and 37f; and a choice for the owner about how the master
learns that the tides run hard, which he ruled on 7 October (G3).

### B3. What the second game showed (game 10, 7 to 8 October, on 37d to 37g)

**The owner played the build on the night of 7 to 8 October**: a merchant cutter from
Falmouth to Scilly and out again, 63 hours, with a local model as officer of the watch.
It is game 10, the first with 37e, 37f and 37g in it (E4). The
consent question was put to the model again with the lean brief as approved, and
answered yes; the seven words were not added, and the lead's advice is now to leave the
brief as it is. In short: the model was a useful mate; fixes near land were very good
and the master's doubt is honest; and the faults that hurt were the harness's and the
reckoning's. A cast of the lead moved a sound account a mile, twice. The model's context
overflowed and ended both seatings. One reply in twenty was lost to the limit on a
reply. An anchor left aweigh could not be let go. The account goes wrong when she
stands off and on. A course given with a half point steers her to its last word. Two of
these come from this review's own advice (J3).

Since that was written the audit has tried six of that game's findings against the build.
It bore three out (the course with a half point, the replay one line short, and the
handover asked for too late on a short count of tokens), narrowed two, and did not
reproduce the anchor left aweigh (N, C7).

### B4. Where things stand on 8 October

**Built**, by the changes file, by the lead's checks of each package (part F), and now by
the audit, which found the four packages in the build as the changes file lists them, file
for file, m5c-b in it byte for byte, and no numbered item of the four briefs left unbuilt
(appendix 1):

- **37d**, the saves and the sight of land. A save says which build wrote it and `load` says
  what it did. The lookout's distances follow the ship in. A bearing gives a line.
  `take a fix`, `the nearest land` and the land-ahead cry are new. The sea breeze blows
  steadily from the sea. An anchor's depth is read where the anchor lies.
- **37e**, the account. One rule for believing an observation. A doubt that grows honestly.
  A fix by the near marks. The master's own tide. A shaped course that makes good.
- **37f**, lying to and the ground. A ship hove to stays hove to. The anchors answer to
  their names. One dragging line an episode. The log's wind-shift, aback and "already" lines
  made quiet. The fore-and-aft cast.
- **37g**, the station. A key to each seating. A larger and fairer budget for a turn. A
  stand-by that danger breaks. A detector that counts only orders that undo one another. A
  silent or paused officer gives up the deck. The deck given and taken without unseating
  him. Three ways of leaving. Relief by another model. The journal read back. A general
  grant of authority and a way out of danger. The consent brief revised once and made
  leaner.

The whole suite, as the lead last ran it, ends with 2,981 passed and nine expected
failures. The auditor ran it once and had the same: `2981 passed, 9 xfailed in 1179.13s
(0:19:39)`, and the linter passes. Seven of the nine are the owner's standing rulings. The
other two are the two lost beats of the recorded passages: the schooner's Falmouth pilot
hails her and does not board, and the naval cruise chases the French brig and does not
speak her.

**The naval cruise does not come through, and the reason that was on record is partly
wrong.** The owner means to close the gate with the cruise next, so this is set out in
full in M, 2.4, where the auditor sailed it. In short, by the audit:

- The scenario puts the French brig on the sea at a fixed place and hour (48° 50' N, 5° 16'
  W, at 07:00 on the 13th). Since 37e the frigate has already sailed past that place: the
  brig appears 4.8 miles on her starboard quarter, up wind of her and already standing
  away.
- The first chase order keeps the frigate close-hauled on the tack she is on, which leads
  away from the chase. Half an hour later the next turns her 175 degrees by the stern with
  her yards still braced sharp up for the old tack. She is taken aback with the wind on her
  quarter and lies without way, and the brig is lost.
- She is not taken through the wind, as the changes file, the mark on the test and the
  first edition all said. The guard that would wear her for a course across the wind's eye
  is in the code already and rightly did not fire. Making the chase wear her did not bring
  the meeting back in the auditor's trials.
- Moving the brig's place in the scenario file, with no code changed, did bring it back:
  put five leagues on the frigate's bow at 07:00, she was within hail at 08:21.
- The same handling fault takes the frigate aback once before in the passage as pinned: a
  second urgent "Taken aback", at tick 83957, which was reported nowhere.
- All of the code concerned is the gate's own; the week's work changed where the frigate
  is at 07:00, and that exposed it. What the cruise needs to close is in M, 2.4 and 2.6.

**Played since, and found wanting** (game 10; part K has what is proposed): a cast of the
lead that moves a sound account a mile; an account that goes wrong when she stands off and
on; an anchor left aweigh that cannot be let go; a course with a half point steered to its
last word; and at the local runner, a context that overflows and replies lost to the limit
on a reply. Two of these come from this review's own advice. Nothing has been built for any
of them, and the audit found that nothing at all in the code or the data has changed since
game 10 was played.

**Not built.** 37h, the pilot, is ruled on and not written. `the port` and
`the depth of water` still give the true position away, on purpose, until the owner has
played what is built. Most of the first review's small faults (the browser, the boats,
numbers in words, the papers, a tack that could not begin, a handful of words) wait with
them. The audit found the same, and that nothing under `client/` has changed.

**At the merge.** The audit's advice is to take all four packages, since none can be held
without those after it, with the changes it names for each (N, 4.2). At the merge it found
these (N, 3.7 to 3.9): `.gitignore` will leave the saves kept as tests out of a commit
without a word; the build's own name is spelt in nine test lines; one consent record made
in play is only in m5c-b; a test pins the bytes of a fixture file; the consent brief must
arrive unchanged; and the fingerprint of the rules takes in every data file, so that once
the work is in the repository the saves of games 9 and 10 load from their checkpoints and
are refused a replay unless it is asked for. It names seven things for the owner to decide
first (D2).

**Consent.** The consent brief was revised once, in 37g and its second pass. Every model
with a yes on record is asked again at its next seating. By the audit's reading of the
records, six identities still owe the question, Opus 5.5 among them, and one has answered
against the brief as it stands: Qwen 3.8 27B (the 0814 file), for game 10, which answered
yes.

**The gate.** Its verdict is not given. By the owner's word it waits on the naval cruise
and on the lead's own officer's watch, neither of which has been played. The chronometer
and British colours off Roscoff are unplayed too (part L). The gate's own document still
describes the gate as cut: its suite lines, both passages' times and words, and four of
its items no longer match the build. What closing the gate needs is the audit's list in M,
2.6.

### B5. The audit in short

The auditor's own short version, in its words. Its "Part 2" is part M here, its "Part 3"
and "Part 4" are part N.

1. **The suite and the linter are as claimed.** `2981 passed, 9 xfailed in 1179.13s
   (0:19:39)`, and `All checks passed!`.
2. **The four packages are in the build as the changes file lists them, file for file**, and
   m5c-b came in byte for byte. I found no numbered item of the four briefs left unbuilt (the reports each
   brief asks for went to the lead and are not in the tree). Three of
   37e's are met only in part and the changes file says so (the fix's doubt when its marks
   lie on one hand; two beats of the recorded passages lost; three of four measured figures
   not reached).
3. **The naval cruise does not come through, and the reason on record is partly wrong.** The
   scenario puts the French brig at a fixed place that the frigate, since 37e, has already
   sailed past: the brig appears on her quarter, up wind and going away. The chase order
   then keeps the frigate on the tack that leads from the chase, and half an hour later
   turns her 175 degrees by the stern with her yards unbraced, which takes her aback. The
   record says she is taken through the wind, and that mending the chase order would bring
   the meeting back. On my trials it does not; moving the brig's place does, with no change
   to the code. The same handling fault takes her aback once more, earlier in the same
   passage, and nobody has noted it (Part 2, 2.4).
4. **The gate's document describes the gate as cut.** Its suite lines, both passages' times
   and words, and four of its items no longer match the build. Nine tests are expected
   failures: the owner's seven and two beats lost this week (Part 2).
5. **What the review recommended and the build does not hold**: the pilot (37h, not
   written); `the port` and `the depth of water` by the captain's means (kept for last, by
   the plan); every fault of the browser client; the boats; one reader for numbers; a tack
   that could not begin; a handful of words; and everything section 11 proposes after game
   10. Nothing in the code or the data has changed since game 10 was played.
6. **At the merge** (Part 3, 3.7 to 3.9): `.gitignore` will leave the kept saves out of a
   commit without a word; the build's own name is spelt in nine test lines; one consent
   record made in play is only in m5c-b; a test pins the bytes of a fixture file; and the
   consent brief must arrive unchanged.
7. **The gate folder is not the gate as cut.** It is the zip, unchanged, with the owner's
   saves, his notes, four scenario files, eight consent records and the review folder
   added. The review folder there was the same as the one here when I compared them,
   before this file and `report-2.md` were added here.
8. **Advice**: take all four packages, since none can be held without those after it, with
   the changes named in Part 4, 4.2, and seven things for the owner to decide first (4.3).

## C. What happened, by date

All dates are in October 2026. The games are numbered as in part E.

| Date | What happened |
|---|---|
| 2 | Gate 5c is cut as `FreeSail-gate-m5c`, at package 37's merge. The owner plays game 1, the merchant passage, alone, and begins game 2, the *Harpy*, with Opus 5.5 as officer of the watch |
| 3 | The *Harpy*'s officer has used the one re-seating that m5c allows, and the owner rules that a session may come back to its station. The Opus 5.5 session playing that officer makes **m5c-b** the same day: 37b, the re-seating rule, and 37c, the two log rules. The *Harpy* is played on from tick 527,255 on 37b alone. Game 3 is begun and given up; game 4, the *Speedwell*, is begun on all of m5c-b. The one consent record made against m5c-b's brief is answered by the session that wrote the change |
| 4 | Game 4 ends. Games 5, 6 and 7: three local models as mate of the cutter, on m5c |
| 5 | Game 8, the *Amazon* as a merchant ship, on m5c. **The first review** is written the same day, read-only, by the lead with a team of reader sessions: the first edition's sections 1 to 9. The owner reads it and answers its ten questions (part D). By his word the follow-up work is to be done locally, in the gate folders, with no commits |
| 6 | The build folder **m5c-c** is made: m5c with the m5c-b diff applied. **37d**, the saves and the sight of land, is built in it, with a second pass the same day that the owner approves. The owner plays **game 9** on it: a merchant brig from Falmouth to Roscoff alone, then round Ushant to Brest with Opus 5.5 as officer. He leaves six notes |
| 7 | The lead writes up game 9 (the first edition's section 10). The owner rules on what comes next and on the five points that had waited since the 5th, and approves the briefs of three packages. **37e**, the account, is built and passes the lead's checks; then **37f**, lying to and the ground; then **37g**, the station's safety with the consent brief's one revision. In the evening the owner has one sentence added to the consent brief, then approves a **leaner brief**, and 37g's builder puts it in and settles the stations' briefs in a second pass, which passes the lead's checks. No model has been asked again in between |
| 7 to 8, night | The owner plays **game 10** on the build as it stands after that second pass: a merchant cutter from Falmouth to Scilly and out again, 63 hours, with Qwen 3.8 27B as officer through the local runner. The consent question is put to that model again, with the lean brief, and answered yes. He gives two notes in conversation |
| 8 | The lead writes up game 10 (the first edition's section 11). Nothing is changed in the build for it. This second edition is written, and the build is audited by a session that has seen none of the work; the audit is then folded into this edition, for the handover to the session that keeps the repository |

Not yet done on any date: 37h, the pilot; the last step of the plan; anything that game 10
gave rise to; and the play the gate still lacks.

## D. The owner's rulings

### D1. The rulings, in one table

Words in quotation marks are his own. His answers of 5 October are given as the first
edition recorded them; each is set out in full, with what the review read into it, under
its subject in part G. "Q" is the number of the question as the first review put it (its
section 9). Decisions 34 to 37 of the design proposal's log record the same rulings.

| # | Date | The matter | The ruling | What followed |
|---|---|---|---|---|
| 1 | 3 Oct | Returning to a station | A session may come back to its station, unless it left saying that it does not want to. The first edition gives this ruling's date and not its words; they are in decision 34 | 37b, in m5c-b. Its opt-out path was mended in 37g (G13) |
| 2 | 5 Oct | How the work is done | Locally, in the gate folders, with no commits, and with the GitHub repository and its worktree left alone. He folds the work in with the lead session that works the repository | The build folder m5c-c (F2) |
| 3 | 5 Oct | Q1. Are saves with a model aboard to stay replayable across harness changes? | Not ruled that day. He would prefer such saves to stay replayable, was not sure what that would mean for the changes ahead, and asked what "good from the checkpoint" provides materially | Answered by the review (G14) and ruled on the 7th (row 14) |
| 4 | 5 Oct | Q2. The gate's verdict | It is not in question for the moment: it waits for the naval cruise and the lead's watch. The work stays within the milestone and is checked as part of the final gate | Neither has been played (part L) |
| 5 | 5 Oct | Q3. Which build a save was played on | Saves were saved in their own folders: any save in a build's folder was played on that build when it was saved | Games 5 to 8 are plain m5c. New work is done in a folder of its own (G14) |
| 6 | 5 Oct | Q4. What stays out of a general grant, and when it lapses | By default a general grant should keep back the port's business and the belaying or cancelling of the captain's standing orders, and perhaps anything else that the standard of the era would make an unlikely grant. When it lapses was not answered that day | The review proposed a list (G11); row 15 |
| 7 | 5 Oct | Q5. Should `I have the deck` leave the officer seated? | Yes. `you have the deck` and `I have the deck` should not unseat the officer. They should move him freely between the state he starts in, which is the watcher's authority in effect, and the officer's, and back | Built in 37g (G11) |
| 8 | 5 Oct | Q6. The pilot | For now an order accepts or declines the pilotage when the pilot first hails, with a simple form of hailing if none exists. Aboard, conning is too much for now. He should warn when she approaches a danger, a shoal and the like, as is reasonable. Speaking and conning wait for the director | 37h, not written (G10); row 17 |
| 9 | 5 Oct | Q7. Fixing in pilot waters: the master's routine, or an order? | `take a fix` can simply be an order, used freely like any other. It need not be a routine | Built in 37d as an order; the officer's own since 37g (G3) |
| 10 | 5 Oct | Q8. May another model take a station within a game? | Yes. When a model stands down from a station, the same model or another must still be able to take it up, so that a stand-down never locks a station out of a game for the player | Built in 37g (G13); row 18 |
| 11 | 5 Oct | Q9. The consent record of 3 October, answered by the session that wrote the change: should it stand, or be asked afresh? | Plenty of fresh consents will be taken after the harness changes, so yes. The review read this as: no separate re-ask now; the record stands as what was answered on the day | The one revision of the brief asks every identity again (G13) |
| 12 | 5 Oct | Q10. The watcher's `opt_out` at the captain's word was not a withdrawal. Should the record say so? | Yes. He believes no opt-out in any test so far, this one included, has been other than amicable | Recorded (G13). `stand_down` was built in 37g so that it need not happen again |
| 13 | 6 Oct | 37d's second pass | Approved: after a bearing, the distance by estimation is laid down when it is the better figure | Built the same day; replaced by the one rule in 37e (G3) |
| 14 | 7 Oct | Replay (Q1) | "As recommended, save is exact from the checkpoint, replay is promised only on the build that made it." | Already built in 37d, and proved on game 9 (G14) |
| 15 | 7 Oct | The general grant (Q4) | "The proposed held-back list is approved for the first version of the general authority grant. It should lapse when the officer is fully stood down, or the authority is directly countermanded by the captain." | Built in 37g (G11) |
| 16 | 7 Oct | The three ways of leaving (Q5) | "Approved as read, parity for the officer's hand_over and the captain's, stand_down for the amicable save and exit." | Built in 37g (G13) |
| 17 | 7 Oct | The pilot's hail unanswered (Q6) | "The pilot may keep company, hail once more, and bear away. He may warn of the shoal water or shore ahead with true knowledge in his water. Thick weather means he cannot see his marks." | 37h, not written (G10) |
| 18 | 7 Oct | A final opt-out, and relief (Q8) | "Yes, a final opt-out (need to be careful of false-positives, but a fair start) should bar the model, not the station. The relief may read the journal of the last holder of the station, as with a standard re-seat." | Built in 37g (G13) |
| 19 | 7 Oct | The way out of danger on the officer's own word | "37g is pre-approved with 19. (the way out of danger) kept as proposed." | Built in 37g (G11) |
| 20 | 7 Oct | How the master's doubt comes to know that the tides run hard (from game 9) | Of the three ways put to him, (b), and now: "The master should work the tide into the reckoning himself ... by the same method the master currently works up the reckoning, he should work the tide into it as the books give it." | Built in 37e (G3) |
| 21 | 7 Oct | What the books give where the tide study found no period source (the Fromveur, the Chenal du Four, the timing of the stream in the Goulet) | As proposed: the directions' plain statement of the set to the nearest point and the spring rate to the half knot, marked as judgement in the data | Built in 37e (G3) |
| 22 | 7 Oct | A shaped course and the tide | "shape a course should by default steer to make good, by the master's reckoning." And his own `allow ... knots of set` "replaces when used until handed back" | Built in 37e (G3) |
| 23 | 7 Oct | The plan after game 9 | He took the split of the next package into two, and joined the station's safety to the consent brief's revision, so that one package holds "the changes which require the re-consent brief". One package at a time, in the order 37e, 37f, 37g | F2 |
| 24 | 7 Oct | Three rulings for 37f | "Loose should remain as is." `trim sails` declines while she is hove to. `let go` keeps veering the scope the depth wants, says the figure, and takes a number | Built in 37f (G7, G8) |
| 25 | 7 Oct | Approvals | "37e is approved". Then: "37f is approved pending your 37e checks, and 37g is pre-approved with 19. (the way out of danger) kept as proposed." He also approved, as they stood, the words of the consent brief's four revised sections | All three were built that day (part F) |
| 26 | 7 Oct, evening | The consent brief, before any model was asked again | First he had one sentence added, on the deck of an officer silent for his hour. Then he asked whether a consent question needed so much of a station's detail at all, and approved the leaner brief the lead drafted: "I approve this brief. Go ahead and revise it in m5c-c. You should also settle the officer and watcher's briefs to make sure they contain the information moved from the consent brief, or anything that has changed otherwise." | 37g's second pass (G13). The draft he approved names, in its table of what moved out, the whole of what the general authority keeps back: "a chase, the reckoning set by hand and the tide allowed in it, sending for a person" with the four heads of row 15 (G11) |

### D2. What still waits on him

Nothing beyond 37g is approved.

**To decide before the work is folded in.** These seven are the audit's, in its words (N,
4.3; "C6", "C1" and "C2" are its disagreements, in N, 4.1):

1. Whether the two playtest saves under `tests/fixtures/saves/` go into the repository. They
   are his own games of 4 and 3 October, a model's transcript and his typed lines included.
2. Whether the review folder goes in, whole or in part.
3. Whether Opus 5.5's consent record of 3 October is fetched from m5c-b, so that all eleven
   records made in play are in the repository as the brief says.
4. The additions to what the general authority keeps back (C6).
5. Whether the gate closes with the schooner's pilot still an expected failure, or waits
   for 37h.
6. Where the *Palinure* is put, or whether the scenario should place her from the frigate's
   own position; and whether the handling fault behind C1 and C2 is mended before the cruise
   is played for the gate, since a captain who types `steer NE` from SW by W will meet it.
7. The name the repository's build is to carry in its saves.

On the fourth, a note from the lead, which is the lead's and not the audit's. Three of the
additions were approved with the lean brief on 7 October (D1, row 26): a chase, the
reckoning set by hand and the tide allowed in it, and sending for a person. The text of
decision 36 in the decisions log, which records four heads, is behind. What is unruled is
the captain's own going below and coming on deck, which the code keeps back and which were
named to nobody (G11).

**Also open.** Each is taken up where the last column says.

| The matter | Where |
|---|---|
| Everything that game 10 gave rise to: the local runner first, then amendments to 37e and 37f, and words | Part K |
| 37h, the pilot: the brief is not written. His rulings for it are rows 8 and 17. One thing in game 9 is beyond them: a pilot cutter that keeps company for three quarters of an hour and says nothing of what she waits for | G10 |
| Whether `say` ends a turn | G12; I6, item 3 |
| An order that answers a sample some minutes old (a late reply) | G12; I6, item 10 |
| What a ship knows of another port's trade, and by which carrier | G16; I6, item 7 |
| The boat's errands: several bargains to a trip, a second boat, or a list | G16; I6, item 8 |
| The well and the pumps | G8; I6, item 9 |
| Who may ask a station back after a welfare stand-down | G13; I6, item 11 |
| The four rulings the gate's own document asks for. By the audit, the one never given is a far-detail vessel's leg across the coast | L2; M, 2.2 and 2.6 |
| From 37f: whether an anchor that holds five minutes and drags again is the same dragging or a new one | G8 |
| From 37e: the number in the one rule is two where the brief said three; and the sentence of the spec's truth 59 | G3 |
| From 37d: whether the two playtest saves kept as test fixtures go into the repository. They carry a model's transcript and journal and his own typed lines. It is the first of the audit's seven, above | G14 |
| From 37g's second pass: `stand_down` takes a handover note and does not insist on one; the watcher's brief lists tools it is refused. The audit found three such tools, not the two the note names: `hand_over`, `handover_note` and `submit_order` | G13 |
| The seven words. He seated a model before the question was answered, so the brief has been put to one identity as approved, and the lead's advice is now to leave it | G13 |
| The shape of the lessons for the primer, and a wardroom of several models, which is a design decision for Milestone 6 | G19 |

## E. The games

### E1. The record, and how it was read

**The first eight games.**

**The record.** Gate 5c has no filled playtest forms yet. Its record is the notes file at the
root of `FreeSail-gate-m5c`, the saves in both folders, and the consent records under
`docs/agents/consent/`. A save holds the seed, the scenario, every order in the order given,
and each station's transcript and journal. A transcript holds what the model *sent* (its tool
calls and spoken lines), not what the game answered. The game's side is in the log, which the
checkpoint beside each save carries whole.

**How it was read.** Each game's last save was loaded through the game's own checkpoint
loader, with nothing written into either tree, and its full log, transcripts, journals and
orders were written out as text. Those dumps were read by a team of reader sessions, one per
slice of a game, each reporting with ticks and quotations. Separate readers checked the
notes' claims against the code, read the notes against the Milestone 5 documents and the
design proposal, and reviewed the m5c-b diff independently. The lead read the design
proposal, the M5 specification's 5c part, the gate, the officer's primer chapter and the
whole diff, and checked the weightiest claims against the logs directly.

**What the record cannot show.** The chat side of the Claude Desktop sessions (the model's
own reasoning and anything said outside the game's tools) is not in a save. Neither is what
the browser drew. Claims about either rest on the notes.

**Game 9.** The owner played the build folder `FreeSail-gate-m5c-c` (m5c, the m5c-b
changes, and package 37d) on 6 October and left two saves and six notes
(`m5c-c Notes.txt`); he also supplied the officer's own summary from the chat
(`evidence/harpy-m5cc-post-session-chat.md`).

**How it was checked.** No reader sessions this time. The lead read the whole log (7,140
lines), the officer's 631 transcript entries and its journal, and every line the owner typed.
Then a scratch copy of the last save was replayed on the build that wrote it, with a probe
recording the true position, the account and the master's doubt once a minute and at every
observation. The replay reproduced the played log exactly, line for line and digest for
digest, so the figures below are of the game as it was played. The tables in full are in
`evidence/G9-brig-m5cc-measurements.txt`; the scripts are in `evidence/tools`. Everything this edition takes from
that game is the lead's own reading unless it says "the officer says" or "not checked".

**Game 10.** On the night of 7 to 8 October the owner played the build folder as it
stood after 37g's second pass (build `m5c-c/37g`): everything planned up to then
that has been built, which is packages 37d, 37e, 37f and 37g with the leaner consent brief.
Not in it: the pilot (37h, not written), the follow-up pass, and whatever else in the review
had not been built. He left two saves and gave two notes in conversation, quoted in H7.

**How it was checked.** As for game 9, with no reader sessions. The lead read the log (4,240
lines), the officer's 414 transcript entries and its journal, and every line the owner typed,
then replayed a scratch copy of the last save on the build that wrote it, with a probe
recording the true position, the account, the master's doubt as he would state it, the depth
and the tide twice a minute and at every observation. The replay reproduced the played log
but for one line (G14), and the ship's place at the end was the same, so the
figures below are of the game as it was played. The tables in full are in
`evidence/G10-cutter-m5cc-measurements.txt`; the scripts are in `evidence/tools`. Everything this edition takes from that game
is the lead's own reading unless it says otherwise.

### E2. The ten games

Eight distinct games at the time of the first review; a ninth played on 6 October on the
build folder m5c-c; and a tenth played there on the night of 7 to 8
October, on the build with 37e, 37f and 37g. A chain of saves from
one game counts once, at its last save. A tick is one second of ship's time. Every game is seed 7.

| # | Game | Ship | Station | Build | Ship's time | Played |
|---|---|---|---|---|---|---|
| 1 | The merchant passage, Falmouth for Brest, by the scenario's book | topsail schooner | none; the owner alone | m5c | 12 June 05:00 to 13 June 19:48 (39 h) | 2 Oct |
| 2 | *Harpy*: Falmouth, Roscoff, Falmouth, Plymouth; aground off Plymouth on the 19th | merchant brig | officer: Opus 5.5 through Claude Desktop, five seatings; a Qwen 3.8 watcher for two and a half hours | m5c to tick 527,255, then m5c-b (the re-seating rule only) | 12 June 05:00 to 20 June 04:37 (8 days) | 2 to 3 Oct |
| 3 | A first start from Plymouth, given up | topsail schooner | officer: Opus 5.5 through Claude Desktop | m5c-b | 21 June 05:00 to 06:52 (2 h) | 3 Oct |
| 4 | *Speedwell*: Plymouth, Roscoff, two days becalmed, Scilly | topsail schooner | officer: Opus 5.5 through Claude Desktop, three seatings | m5c-b (both parts) | 21 June 05:00 to 27 June 16:07 (6½ days) | 3 to 4 Oct |
| 5 | Cutter from Falmouth | cutter | officer: Gemma 4 26B (Q4_K_M) through the local runner, two seatings | m5c | 12 June 05:00 to 20:01 (15 h) | 4 Oct |
| 6 | Cutter from Falmouth | cutter | officer: Qwen 3.8 27B under Ollama through the local runner | m5c | 12 June 05:00 to 14:28 (9½ h) | 4 Oct |
| 7 | Cutter, Falmouth for Roscoff with wine | cutter | officer: Qwen 3.8 27B under llama.cpp through the local runner, 102,400-token budget | m5c | 12 June 05:00 to 13 June 12:16 (31 h) | 4 Oct |
| 8 | *Amazon* as a merchant ship: Falmouth to Roscoff with tin | ship (the frigate's file) | officer: Opus 5.5 through Claude Desktop | m5c | 5 Oct 05:00 to 6 Oct 15:21 (34 h) | 5 Oct |
| 9 | A merchant brig (the officer calls her the *Harpy*): Falmouth, Roscoff, outside Ushant, Brest | merchant brig | none to Roscoff, the owner alone; then officer: Opus 5.5 through the MCP bridge, two seatings, the deck for 78 hours | m5c-c with package 37d | 12 June 05:00 to 17 June 04:35 (5 days) | 6 Oct |
| 10 | A merchant cutter: Falmouth, at anchor off the Lizard, Scilly (St Mary's Sound), out for Ushant | cutter | officer: Qwen 3.8 27B under llama.cpp through the local runner, 102,400-token budget, two seatings, the deck for 53 hours | m5c-c with packages 37d to 37g | 12 June 05:00 to 14 June 20:00 (63 h) | 7 to 8 Oct |

The build of each game is the build of the folder that holds its saves: the owner confirms
that a save was played on the build of the folder it was saved in (D1, row 5). So
games 5 to 8, whose saves are in `m5c/saves`, are plain m5c. The Gemma game's log agrees: it
has m5c's reseat wording ("the second seating, the last this game allows").

### E3. The games in numbers

Counted from each game's full log. Game 3, two hours long, has no column.

| | 1 | 2 *Harpy* | 4 *Speedwell* | 5 Gemma | 6 Qwen (Ollama) | 7 Qwen (llama.cpp) | 8 *Amazon* |
|---|---|---|---|---|---|---|---|
| Captain's orders taken / refused | 49 / 22 | 363 / 55 | 370 / 46 | 95 / 16 | 51 / 4 | 83 / 9 | 79 / 1 |
| Officer's orders taken / refused by the ship | none | 253 / 28 | 215 / 27 | 36 / 24 | 5 / 0 | 23 / 4 | 100 / 9 |
| Orders refused by a station's domain | none | 19 | 6 | 4 | 1 | 4 | 5 |
| `you may ...` allowances given (no `you may not` in any game) | none | 27 | 27 | 6 | 8 | 14 | 20 |
| Nudges / pauses, for contrary orders or silence | none | 8 / 1 | 20 / 0 | 2 / 0 | 2 / 0 | 1 / 1 | 0 / 0 |
| Wind-shift lines | 4 | 363 | 69 | 53 | 2 | 40 | 12 |
| "Taken aback", urgent / notable | 0 / 0 | 31 / 0 | 5 / 96 | 3 / 0 | 0 / 0 | 1 / 0 | 0 / 0 |
| Per-sail "taken aback" lines | 10 | 298 | 320 | 2 | 6 | 6 | 14 |
| Groundings | 0 | 2 | 0 | 0 | 0 | 0 | 0 |

| Game 9 in numbers | |
|---|---|
| Captain's orders taken / refused | 318 / 46 |
| Officer's orders taken / refused by the ship | 204 / 33 |
| Orders refused by the officer's domain | 9 |
| `you may ...` allowances given (no `you may not`) | 23 |
| The owner's `tell` and `ask the officer` lines; the officer's reports | 86; 153 |
| Nudges / pauses for "contrary orders" | 10 / 1 |
| Fixes (the owner, the officer, the officer's standing order) | 61 (19, 12, 30) |
| Bearings; of which the distance was laid down | 46; 13 |
| Wind-shift lines; of which with under four knots of wind | 50; 31 |
| "Taken aback", urgent / notable | 5 / 17 |
| Anchor dragging lines, all urgent | 23 |
| Land-ahead lines | 3 |
| Groundings | 0 |

| Game 10 in numbers | |
|---|---|
| Captain's orders taken / refused | 176 / 25 |
| His `tell` and `ask the officer` lines | 74 |
| Officer's orders taken / refused by the ship | 70 / 21 |
| Orders refused by the officer's domain | 3 |
| Standing orders' firings taken / refused | 290 / 33 |
| `you may ...` allowances by name / the general authority | 5 / 2 |
| The officer's spoken reports / its notes in the log (every one a notable line) | 44 / 280 |
| Fixes (the owner, the officer, a standing order) | 39 (32, 4, 3) |
| Bearings | 13 |
| Casts of the lead; of which by the five-minute standing order | 222; 183 |
| Wind-shift lines | 16 |
| "Taken aback", urgent / notable | 8 / 2 |
| Words from the detector for orders undoing one another | 0 |
| Nudges / pauses | 1 (silence) / 0 |
| Empty replies from the officer, of 414 entries | 22 |
| Handover notes written; asked for by the harness in time | 4; 0 |
| Seatings ended by the model server refusing the request for its size | 2 of 2 |
| Fog | six spells, 23 hours of the 63 |
| Land-ahead lines | 1 |
| Groundings | 0 |

Five of the six spells of fog came down on the stroke of eight bells and five lifted on it,
as in game 9 (G5).

### E4. What happened in each game

Times are ship's time; numbers in brackets are ticks, for finding the place in a log.

#### Game 1. The merchant passage, the owner alone

The gate's first scenario, run under its own book of forty standing orders. The owner typed
47 lines, all of them questions and trials at the prompt; none touched the ship. The run is
the gate's reference run to the tick: tin aboard at 08:57, under way 09:26, the Falmouth
pilot off at 10:07, the sail off the Lizard at 12:49, the Brest pilot aboard at 06:26,
Bertheaume at 07:47, the Bay at 13:05, the tin sold at 15:10. He left her at anchor nearly
three hours past the gate's 36.

It is the clean passage the owner's note 5 describes, and it shows what a careful approach
looks like in this game: the lead and bearings every five minutes through the Goulet. It
also shows, with no model aboard, several of the faults the later games met:

- The noon sight was not adopted: observed 49° 54' N against a reckoning of 50° 02' N, and
  the same tick still gave "the distance to falmouth is 8 miles by account" (25,200).
- Both pilots boarded a ship under way, the first before her topsail was in (16,320), the
  second at about four and a half knots (91,560). No order accepts or refuses a pilot. The
  outward-bound schooner is hailed with "a pilot for Falmouth". The Brest pilot never leaves
  and is never paid.
- "The best bower let go in twelve fathoms and a half", then "Brought up ... in six fathoms
  and a half", with the lead reading 12¼ two minutes later (115,534 to 116,489).
- A rule of the book conditioned on the depth of water fired on a cast of thirteen fathoms,
  then asked 54 times for an anchoring already done.
- 22 of the owner's 47 lines were refused, nine of them tries to leave the cabin.
- The purse rose by £10,800 at the sale; the gate's item 1 says £6,000.

#### Game 2. The *Harpy*

The longest game, and the one that went aground. Opus 5.5 as "Mr Pearce", told to lead.

**12 June.** At anchor in Carrick Road the officer read the port chapter and the papers,
proposed tin for Roscoff and brandy home, and bought seven tons (6,143). She weighed at
09:16; a Falmouth pilot boarded unasked while she was under way and was put off at 10:09.
That evening the officer's Claude Desktop conversation died. A new one took up the station
at 19:08 (50,908) with no brief and no journal; the harness logged nothing. This is the
owner's note 10.

**13 and 14 June.** Fog; the officer hove to on his own judgement for eight hours, then ran
for the Isle of Bas on an account ten miles out and passed north of it unseeing. The captain
caught it from his chart. A Roscoff pilot boarded nine miles from his entrance, never took
her in, and left as she clawed off the island in fog at night. She anchored outside the
western entrance (173,251); the anchor dragged twice while the officer stood by. From there
she sold the tin for £1,785 and bought fifteen tons of brandy. A local Qwen model sat as
watcher for two and a half hours. The officer handed over to get a fresh conversation, which
spent the one reseat that m5c allowed.

**14 to 18 June.** A beat up-Channel, twenty hours of it becalmed, with the urgent "Taken
aback" line firing twelve times with no way on; her square sails were taken in to quiet it.
On the night of the 17th, hove to off the Manacles, she filled by herself and sailed toward
the land for an hour unnoticed (496,638). She could not fetch Falmouth's entrance, moored two
and a half miles outside, and the boat was refused. Falmouth was given up.

**18 June.** The build was changed to m5c-b across a hand-over. Bound for Plymouth, putting
the pilot off drew the game's one pause (533,573). The wind died in fog; the bridge dropped
at 20:24 and the officer was seated a fourth time, three ticks later. He anchored in thirty
fathoms off Rame Head under all plain sail. A Plymouth pilot boarded the anchored brig.

**19 June.** A hand-over written "for the relief through a local door" ended with the same
model seated a fifth time: another model may not take a station once held. The fog lifted at
noon. She weighed and stood in under all plain sail while the wind flicked through eight
points, with 265 wind-shift lines in 104 minutes. The last quarter of an hour is set out in
G1. She struck Penlee Point at 13:50:53 (636,653), aground and leaking. The captain
sold the brandy by boat for £4,725 while she lay there. She floated on the flood at 18:04,
struck again 21 seconds later, floated at 18:32 and rode the night.

**20 June.** The pilot left as she stood off to save herself. She anchored in Cawsand Bay:
"Brought up by the best bower in no water". The purse had gone from £1,000 to £5,148.

#### Game 3. The first start from Plymouth

Two hours. The captain belayed the long-boat seventeen seconds into hoisting out, meaning to
send the mate in her. The boat stayed "away, hoisting out" for good, and a *rejected* order
had put the mate, who was the officer and held the deck, into it (3,237). They started again.

#### Game 4. The *Speedwell*

Opus 5.5 as the mate, "Mr Ray", on m5c-b throughout.

**21 June.** Fourteen allowances in the first two minutes, then the deck. Three boat trips
over ten hours fetched the prices, forty tons of coal and twenty of pilchards, bought for
Roscoff on the officer's general knowledge. She weighed and hung head to wind until he backed
her off by hand, though the log had already said "She has paid off" and "Under way" (38,651).
The Plymouth pilot boarded unasked while she lay in irons.

**22 June.** At 05:07 a lunar moved the account 33' east. The officer advised steering by the
old account and kept a reckoning of his own. That night the danger list named the Triagoz
five miles off; they were fifteen to twenty.

**23 June.** His standing order "trim" filled her out of a heave-to twice. The Isle of Bas
came up at 07:37 and one bearing by the captain put the account right. The pilots' boat
hailed at 10:29; she hove to for an hour and a half and was not boarded. Going in without
him she shoaled from fifteen fathoms to three and a half north-west of the island with no
word from the lookout (200,467); the captain's chart showed unmarked land there. The pilot
boarded as she passed his boat. The wind died and she anchored outside the channel. Roscoff
would not take coal. The officer bought sixteen tons of brandy.

**24 to 26 June.** Twenty hours without way: 90 "sails aback" lines and 223 per-sail lines,
none urgent, none waking the officer. The captain tried hand-over and re-seating, which
worked, and found that `I have the deck` stands the station down. When he gave the deck back
fifteen hours later the officer's conversation had been replaced, with no mark in the log,
and it could not reach its own handover note (398,711).

**27 June.** A night landfall on Scilly, the account seven miles out until the captain's
bearing of St Agnes light; the officer's own bearing was refused. Then ten hours trying to
enter St Mary's Sound, never nearer than seven cables from the outer road. A three-minute
board to seaward lost the first pilot. Three tacks "failed" that had never begun. She
anchored in 46 fathoms on 230 fathoms of cable. A second attempt ran by the account at the
Gilstone. The boat stuck again. A third attempt met a wind boxing the compass. The brandy is
unsold and the purse stands at £28.

#### Games 5 to 7. The local models on the cutter

All three sailed the cutter *Sherbourne* out of Falmouth on build m5c, the model as the mate.

**Game 5, Gemma 4 (Ollama).** Two officers in one game. Given the deck at 07:19 to get under
way, it set two sails, spent its remaining calls on refused orders about sheets, had "weigh
the best bower" not run three times, and fell out of the tool format into prose and tables.
The captain weighed by hand. A `tack ship` 28 seconds after the anchor broke out failed, and
the captain wore her round. After a third runaway reply he asked for a handover (14,962); the
new conversation that followed was clean for the remaining eleven hours. In it the officer
handled sail promptly when told, stood by from bell to bell (once for three and a half
hours), reported nothing unasked, and turned her ninety degrees in pilot waters on a "you
may steer" given ten hours before (44,668). She anchored at Plymouth at 17:49.

**Game 6, Qwen 3.8 (Ollama).** Courteous, well formed in all 43 replies, and slow against
the clock. Given the deck with seven allowances, it read seven library pages; its corrected
`weigh the best bower` was then not run, the eight calls of the turn being spent, and she
lay at anchor another 22 minutes (8,826 to 10,188). Under way, it ordered `steer WSW` dead to
windward, which the captain undid. No reply then came for 71 minutes of ship's time, in
which the captain took the pilot, hove to for his cutter, filled away and shaped the course.
The officer's `heave to` landed at 15,937, meant for a pilot already gone; it took six orders
to undo. It gave five orders in nine and a half hours.

**Game 7, Qwen 3.8 (llama.cpp, a 102,400-token context).** The longest local watch and the
steadiest: 27 hours with the thread kept, across two handover notes that the harness asked
for at 62,276 tokens and again eighteen hours later, each written in the next reply and each
followed by a clean fold. It learned the order language within the game, trimmed on wind
shifts, and wrote a well-made standing order of its own. It also stood by on "a notable
event" for 96 per cent of its time with the deck, and never navigated. Fog came down at
08:00 on the 13th, fourteen miles from Roscoff. At 08:05 it journaled a plan to stand on
until noon, and never replied again. The harness nudged at 09:05 and paused it at 10:05; the
deck stayed with the paused station and the cutter ran on for four hours to 1.6 miles from
Roscoff harbour, her account six and a half miles out. At 12:14 the captain typed "Resume
the officer", and a Claude Desktop session still attached to the same game answered instead:
it belayed the standing order, hove her to, was refused the anchor, and handed over
(112,483 to 112,613). The log and the save record all of that as Qwen's.

**The watcher.** The same Qwen weights sat as watcher on the *Harpy* for two and a half
hours on 14 June. It answered accurately, stood by "until an urgent event" 37 seconds after
noting that it had been asked to sing out when anything showed through the fog, slept
through the unmooring and the pilot, and reported ten minutes late. Told to hand over and
save its watch, it was refused `hand_over` twice ("no authority to give orders") and left by
`opt_out` at the captain's word.

#### Game 8. The *Amazon* as a merchant ship

The frigate's file sailed as an American merchantman, with Opus 5.5 as first lieutenant. The
captain opened with "I'll leave you broad authority, if you deem anything necessary then
either ask and I'll allow, or try and I'll allow as I see it", and gave twenty allowances in
the course of the game.

At anchor off Falmouth the officer read the port chapter and the price list, proposed tin
for Roscoff and brandy home, and bought thirty tons (662). The launch took three hours
thirty-eight minutes. Under way with the pilot at 09:32, he steered by bearings and the lead
rather than the account, hove to for the pilot to leave, and made sail. Nine strain warnings
on the topgallant yards and masts went unanswered for twenty-five minutes behind a stand-by
"until a glass" (20,191 to 21,674). In the afternoon three squalls came through; his
standing order to shorten sail fired after the 34-knot one had passed.

At 19:18 a lunar "which he would trust within 50 miles" was worked into the reckoning: the
longitude by account went from 4° 22' W to 4° 53' W and its stated doubt from two miles to
twenty-five (51,502; 52,178). The captain's `you may set the reckoning` did not open the
order for the officer, and the captain set the reckoning back himself.

She lay to overnight, then ghosted south in light airs. At 09:14 the officer judged that
"the account cannot be right": it put the Lavandière four miles off with no land in sight.
The Isle of Bas came up at 10:38, five leagues off, the account about ten miles too far
south. The Roscoff pilot boarded at 13:37 and, the log says, "took charge of her". He spoke
one paragraph. The officer conned her in by the lead and the `the port` reading, which gives
the true bearing and distance of the entrance. At 14:39 he wore away from shoaling water; the
captain belayed the wear and steered on, then gave the con back. The casts went eight
fathoms, then "By the mark three" under a ship drawing fifteen feet, and the officer let go
the anchor on the run in three and a half fathoms (121,712). She dragged, held, weighed at
15:00 and stood out north-west. The road was not reached and the tin is unsold.

No urgent line was logged in the whole game. This is the afternoon of the owner's note 24.

#### Game 9. A merchant brig, Falmouth to Roscoff and round Ushant to Brest, on m5c-c with 37d

One game, seed 7, the scenario "A merchant brig, free" under American colours, from Falmouth
on 12 June 05:00 to Brest road on 17 June 04:35: five days of ship's time. The officer calls
her the *Harpy*, after game 2's brig; she is a new ship in a new game.

- **12 and 13 June, the owner alone.** Out of Falmouth with a pilot, a course shaped for
  Roscoff, a night hove to in fog. Landfall on the Isle of Bas at 05:16 on the 13th at five
  leagues. Fog from 08:00 to 16:00: the Roscoff pilot came aboard in it, she lay hove to
  outside for five hours, and the pilot left again before she went in. When it lifted the
  owner conned her in himself by bearings and two fixes, past the Lavandière, and anchored at
  17:20. He moored, bought eight tons of brandy, and the fog came down again.
- **13 June 22:33, Opus 5.5 seated as officer of the watch** through the MCP bridge (a fresh
  consent record of 6 October, the drill passed). It kept an anchor watch through the night.
- **14 June.** Weighing at 04:00 was given up when the fog returned and an anchor dragged.
  Under way at 08:36; the owner gave the con at 08:42, and from there the officer conned and
  navigated the whole way. Out past the Lavandière against the ebb's set, along the coast,
  four hours of fog standing off. At 17:39 it handed the deck over at the owner's word for a
  break and was seated again four seconds later, the second seating.
- **14 to 16 June, outside Ushant.** The officer laid five waypoints from its own memory of
  the real chart and shaped for each in turn. A lunar in the middle watch. Into the Iroise in
  light airs; hove to for a stranger and then through four hours of fog; a night becalmed
  off Ar Men with the deep-sea lead going; the forenoon ebb setting her back.
- **16 June afternoon, the Goulet.** A south-west breeze and the flood took her in. She
  passed the Mingan at 16:35; the wind died; she anchored in the Goulet at 16:41 and the Brest
  pilot boarded seven minutes later. Three anchors were down by evening on poor ground.
- **17 June.** Weighed on the midnight flood, anchored in Brest road at 02:20, moored by
  02:42, the boat sent in for prices. The officer handed the deck back at 04:35.

The officer held the deck for 78 hours of ship's time. Nothing was carried away and she did
not touch the ground.

#### Game 10. A merchant cutter, Falmouth to Scilly and out, on m5c-c with 37d to 37g

One game, seed 7, the scenario "A merchant cutter, free" under American colours, from Carrick
Road on 12 June 05:00 to eight miles south-east of St Mary's on 14 June 20:00: 63 hours of
ship's time. The owner was captain throughout. The officer of the watch, in the place of Mr
Pearce, was Qwen 3.8 27B (Q4_K_M) under llama.cpp through the local runner, with a context of
102,400 tokens: the same model, server and size of context as game 7.

- **The consent question was put again**, as the rule requires, with the lean brief and the
  notice of why (the four sections named). The first reply was empty; after the reminder the
  answer was a yes with no condition. The drill was passed on the last of its four replies
  (G13). The record is `docs/agents/consent/2026-10-07-qwen3.8-27b-0814-q4_k_m.gguf.md`.
- **12 June, Falmouth to the Lizard.** Sixteen tons of salt bought at £25. The deck given
  to the officer at 07:54 "to handle her sails" and the anchor weighed at 08:08, the owner
  conning. The Falmouth pilot aboard from 08:31 to 09:16. A day's beating off the Lizard in squalls: a tack, two wears,
  and at 14:14 the captain's general authority to work the ship.
- **13 June.** The wind died at midnight and fog came down. At 02:31 she anchored off the
  Lizard in 48 fathoms with the whole cable out. Weighed at 04:51 and made for Scilly, W by N,
  through two more spells of fog, on the reckoning and the lead. The St Mary's gig was sighted
  at 18:26 before any land; the pilot came aboard at 18:45; she anchored off the mouth of St
  Mary's Sound at 19:53 in 45 fathoms.
- **14 June, the Sound.** Weighed after midnight, stood off and on and lay hove to, then ran
  in from 02:11 on the flood by a fix every five minutes. At 03:30 the officer, under the
  general authority, anchored her in the Sound, the lead having come down from 34 fathoms
  to 4. The owner, not content with the berth, got under way at 03:38 and belayed it; fog came down at 04:00; at
  04:08 a cast moved the reckoning a mile (G3); he anchored again, with some trouble
  (G8), and moored.
- **14 June 08:00, the first seating ended** when the model server refused the conversation
  for its size. The same model was seated again eight seconds later, the second seating, and
  read its journal.
- **The day at St Mary's.** The salt sold at £28, twenty tons of salt fish bought. At 15:15 the
  deck and the general authority again. Unmoored and weighed by 16:44, out to the south-east
  with the St Mary's pilot aboard for an hour, and a course shaped for Ushant at 17:34.
- **14 June 20:00, the second seating ended** the same way, and the owner stopped there.

The officer had the deck for 48 hours in the first seating and for nearly five in the
second. Nothing was carried away and she did not touch the ground.

How each model kept its watch is taken up in G15, for the local models, and in G20.

## F. The builds and the packages

This part says what each build and package is, when it was made, what was run to check it
and what it left undone. What each thing built does, and how it fared in play, is under its
subject in part G. Everything said here to be built was first set down on the word of
`CHANGES-m5c-c.md` and of the lead's checks as the first edition records them. The audit
then set each package's list of changed files against the lead's snapshots of the build
after each package, and found no file changed that the changes file does not name and none
named that did not change (N, 3.2). It found no numbered item of the four briefs left
unbuilt (appendix 1, 1.12 to 1.15). What it found otherwise is said under each package
below. Its advice on each is in N, 4.2.

### F1. m5c-b: packages 37b and 37c (3 October)

`FreeSail-gate-m5c-b` is a copy of m5c with three changes, made on 3 October by the Opus 5.5
session that was playing the *Harpy*'s officer, and played live the same day: the *Harpy*
from tick 527,255 on the first change alone, the *Speedwell* on all three.

| Part | What it does | Verdict | What came of it |
|---|---|---|---|
| 37b, the rule | A station may be seated again any number of times. How it was left decides: stood down or handed over, seated as it was; left by the token or `opt_out`, the consent question first; `opt_out` with `final`, not in this game. | **Carry, after mending the opt-out path.** | Carried into m5c-c with the diff. The opt-out path was mended in 37g (G13) |
| 37b, the fix | A save whose station was held when it was saved can be taken over again by the same model after loading from its checkpoint. | **Carry as it is.** | Carried into m5c-c with the diff |
| 37c, the wind-shift line | Reads the ten-minute mean wind, two points from the last line, held a minute. | **Carry, with a floor on wind strength and steadiness.** | Carried into m5c-c. The floor and the steadiness test were added in 37f (G6) |
| 37c, the taken-aback line | Once an episode, re-armed after a minute clear; urgent only with way on, four knots of apparent wind, and no anchor or ground holding her. | **Carry, with re-arming by state and one flag per severity.** | Carried into m5c-c. Re-arming by state and a flag for each severity were added in 37f (G6) |

**How it was checked.**

- **The diff is the whole difference.** An independent reviewer regenerated it from the two
  trees and got the same hunks. m5c's code has not changed since the copy.
- **The suite passes.** The lead ran m5c-b's whole suite, slow tier included, on a scratch
  copy on the owner's Windows machine: **2,712 passed, 7 expected failures, 1 failed, in
  14 min 38 s**. The seven are the owner's standing rulings on truths 3, 11, 18, 24, 26, 28
  and 31. The one failure reads `.mcp.json` at the root, which the m5c-b folder lacks; with
  m5c's file beside it, the test passes. So the six re-recorded known-truths digests hold on
  this machine.
- **The folder is not the change.** It lacks `.mcp.json` and `.github/`, the two scenario
  files and four consent records added to m5c since, and its three reference images each
  carry 5,768 extra bytes: a content-credentials manifest appended when the files were handed
  over. The picture data is identical. **Apply `m5c-b.diff` to m5c; do not copy the folder.**

What play showed of 37b, and what was not right in its opt-out path, is in G13. What play
showed of 37c is in G6. The cost that m5c-b's own changes file does not state, that an older
save with a model aboard no longer replays, is in G14.

**Carrying it forward.** The first review asked for five steps, in this order:

1. Apply the diff to m5c. Leave the images, the folder's saves, and CHANGES' "Running it".
2. Mend items 1 to 5 above with their tests, then make the words of **Leaving** say what the
   code does. Seven identities hold a yes and each change to that paragraph asks all of them
   again, so settle it once, and put every other pending change to the consent brief in the
   same revision.
3. Add the floor and steadiness test to the wind-shift line, and state-keyed re-arming with
   one flag per severity to the aback lines, per-sail lines included. The six digests move
   again; re-record them and run the slow tier on Windows.
4. State the replay cost, stamp saves with an engine version, and have `load` say so when it
   must replay an older save that holds a transcript.
5. Bring the documents into line, and add the ruling to the decisions log.

What came of each:

1. Done on 6 October. m5c-c is m5c with the diff applied, and the changes file says that all
   22 changed files are byte for byte m5c-b's. The audit found it so: 15 of them were still
   m5c-b's own bytes after 37d, and the other seven had by then been changed again by
   37d.
2. Done in 37g. The opt-out path's items 1 to 4 are mended; item 5, an opt-out saved under
   m5c that reads as a stand-down, is left as it is by the owner's answer of 5 October, since
   the one such save was an amicable leaving. One thing is said to be not done: the REPL's
   turn mode does not put the consent question again after an opt-out; by the audit it
   says so and seats nobody when the question is owed. The words of **Leaving** were
   revised with every other pending change to the consent brief, in one revision
   (G13).
3. Done in 37f (G6). The recorded passages were re-measured there.
4. Done in 37d, with a stamp of the build in place of the engine version (G14).
5. Done in 37g for the decisions log, which has decisions 34 to 36, and 37 from the second
   pass, with decision 33 marked superseded. The changes file says the documents that
   stated the old rule were mended. The audit found one that was not: the gate's own
   document, in its headline item 6, still says "a second seating once" beside the new
   parenthesis. It did not read the other documents against the code.

### F2. m5c-c, and the plan as it was ruled

**The folder.** `FreeSail-gate-m5c-c` is a working copy of m5c as it stood on 6 October,
made that day at the owner's word, with `m5c-b.diff` applied. With the base and the diff
and nothing else, the whole suite on the owner's Windows machine
(`py -m pytest -n 4 --slow`) ended `2713 passed, 7 xfailed in 842.59s`. From its changes
file:

- **Left behind in m5c and m5c-b**: the saves, since by the owner's rule a save lies in the
  folder of the build that played it; the owner's notes file; and the one consent record
  made under m5c-b (`2026-10-03-opus-5.5.md`), which is not part of the diff. The audit
  found that this leaves that record in neither folder that will be diffed, though the
  consent brief tells every model that its record is kept in the game's repository (N, 3.7
  and C5; G13).
- **Added**: the review folder; and `tests/fixtures/saves/`, which holds two of the
  playtest's own saves with their checkpoints (the cutter of game 6 at tick 34,091, written
  by m5c, and the *Harpy* at tick 602,100, written by m5c-b before 37c) and a third made by
  37d with a scripted officer. The two playtest saves carry a model's transcript and journal
  and the owner's own typed lines; whether they go into the repository is his to say, and
  the tests that use them skip when the files are not there.
- **Running it**: from the folder itself, with `PYTHONPATH` set to it, because the editable
  install points at m5c. The MCP bridge that Claude Desktop starts imports the package from
  wherever it runs, which is m5c, unless `PYTHONPATH` is set in its configuration.
- **How it is to be handed over**: as m5c-b was, by the changes note and one diff against
  m5c as it was cut, leaving out the caches, `saves/` and the playtest fixtures unless the
  owner says they go in. The editor saw no such diff at the folder's root on 8 October.
  The audit lists what belongs to this folder alone and should not be carried as it is, the
  build's own name among them, and four traps at the merge (N, 3.8 and 3.9).

**The order the first review suggested** (5 October):

1. The saves: stamp them, have `load` say which road it took, and keep a few of the
   playtest's checkpoints as tests. The wider ruling on replay can follow (G14).
2. Near land, the sea breeze, the anchor's place and the schooner's cast; re-measure once.
3. The station's safety: the seat key, the budget's exemptions, the lost word, the stand-by's
   wakes and bound, the paused deck, the detector.
4. The brief's one revision: 37b mended, the journal, `I have the deck`, the domain and the
   grant; one re-ask.
5. The log's noise and the small faults.
6. Then play what the gate still lacks: the naval cruise, the chronometer, British colours
   off Roscoff, and the lead's own watch.

What became of that order. Step 1 is the first part of 37d. Step 2 is its second part, less
the schooner's cast, which was built in 37f. The recorded passages were not re-measured
once: they moved in 37d, again in 37e and again in 37f. Steps 3 and 4 are one package, 37g,
by the owner's ruling. Of step 5, the log's noise is the third part of 37f, and most of the
small faults are not built. Step 6 has not been played. The audit's ledger says the same
(appendix 1, 1.8).

**After game 9 the next package was too big for one.** It was to hold the wind lines, the ground and
the account. With game 9's findings the lead proposed building it as two, one after the other, since
both move the recorded passages:

- *The account*: the one rule (G3); the doubt; the fix's choice of marks and its "good to";
  the account pinned at anchor; and the merchant passage's book tuned for a true account,
  with the fix put back in its pilot-water rule (the stopgap of 37d's second pass).
- *Lying to and the ground*: heaving to that holds its tack; `fill away` on the tack she is
  on; the hove-to record cleared by the anchor; the guard in the shipped books' trim rules;
  an anchor's name honoured by `veer`, `weigh` and `heave short`, or refused in words;
  "to" kept when an anchor is named; `let go` saying the scope it will veer, and taking one
  ("let go the best bower and veer to 45 fathoms"); `heave in to N fathoms`; one dragging
  line an episode and a flag that drops when the anchor holds; the wind-shift floor; the
  aback and "already" lines made quiet; and a standing order's condition checked on entry.

**The plan as ruled, 2026-10-07.** The owner took the split, and joined the station's
safety to the consent brief's revision, so that three packages follow 37d, one at a time:

- **37e, the account**: the one rule, the honest doubt, the fix's marks, the master's
  tide, a shaped course that makes good, and the books re-tuned.
- **37f, lying to and the ground**: as listed above, with three rulings. `loose` stays as
  it is and sets the sail ("Loose should remain as is"). `trim sails` declines while she is
  hove to. `let go` keeps veering the scope the depth wants, says the figure, and takes a
  number.
- **37g, the station's safety, and the deck, the leaving and the grant**: the faults of G11
  and G12, and every change that asks the consent question again, in one revision of the
  brief.

The pilot is 37h. The three briefs are in the build folder's
`docs/dev/M5-WorkPackages.md`. He approved all three that day (D1, row 25).

The plan in the build folder's `docs/dev/M5-WorkPackages.md` ends with one more step:
"Last, after the owner has played the above: `the port` and `the depth of water` by the
captain's means, and the small faults of the report's 8.2." Those small faults are in I5
here.

**The packages in one table.** The suite's figures are each builder's, from the changes
file; the lead's own runs are given under each package below.

| Package | What | Built | Items in its brief | Fast tier | Whole suite | The build's name |
|---|---|---|---|---|---|---|
| 37b, 37c | m5c-b: returning to the station; two log rules | 3 October; the diff applied 6 October | | | 2713 passed, 7 xfailed | |
| 37d | The saves, and the sight of land | 6 October, with a second pass the same day | 16 | 2549 passed | 2790 passed, 7 xfailed | `m5c-c/37d` |
| 37e | The account | 7 October | 14 | 2594 passed | 2836 passed, 9 xfailed | `m5c-c/37e` |
| 37f | Lying to, and the ground | 7 October | 21 | 2683 passed | 2933 passed, 9 xfailed | `m5c-c/37f` |
| 37g | The station's safety, and the deck, the leaving and the grant | 7 October | 24 | 2730 passed | 2980 passed, 9 xfailed | `m5c-c/37g` |
| 37g, second pass | A leaner consent brief, and the stations' briefs settled | 7 October, evening | | 2731 passed | 2981 passed, 9 xfailed | `m5c-c/37g` |
| 37h | The pilot | Not written | | | | |

### F3. 37d: the saves, and the sight of land (6 October)

From the first review's findings on navigation close to land, the wind near land and the
anchor's depth, and from the owner's answer on replay. Its brief has sixteen items in two
parts. Neither the consent brief nor any station's brief was touched.

**What it built**, by the changes file:

- A save and its checkpoint say which build wrote them; `load` says what it did, and does
  not replay another build's game with a model aboard unless told to; a station seated at
  the very start replays in its place; three old saves are kept as tests (G14).
- The lookout's distances follow the ship in; the nearest shore is always a sighting within
  a league and `the nearest land` is a reading; the lookout warns of land ahead (G2).
- A bearing gives a line; a bearing of a sail moves nothing; `take a fix` (G3, G4).
- A dragging anchor is urgent and the pilot's hails are notable (G6).
- The sea breeze blows steadily from the sea (G5).
- An anchor's depth is read where the anchor lies (G8).

**Its second pass**, the same day and approved by the owner, laid a bearing's distance by
estimation down when it is the better figure, after the first pass had left a landfall on
one headland miles along its line. The lead's correction of what that pass said about the
Goulet is in G3.

**The suite, after the second pass.** The fast tier ended `2549 passed`; the whole suite
`2790 passed, 7 xfailed`. Five of the six recorded passages moved and were re-recorded, with
the reasons in `docs/dev/TuningNotes.md`; the 5a day under systems did not move. All six
come through.

**Not done**, by the changes file: the account in the Goulet is still not a true one;
`take a fix` sets the account outright and picks its marks by how they cut and not by how
near they are; the standing-order dialect does not take cables
(`when the nearest land is under 3 cables`); and `the port` and `the depth of water` still
give the true figures. The first two were taken up in 37e (G3). The dialect and the two
readings are still as they were, which the audit found by trying them (G9, G4).

**The audit on 37d**: take, with two named changes at the merge. Set the build's name for
the repository and move the nine test lines that spell it; and settle the saves kept as
tests before the first commit, with the owner's word on the two playtest saves and an
exception to `.gitignore` for their folder (N, 4.2; G14).

**In play.** Game 9 was played on this package alone, and game 10 on it with the three that
followed.

### F4. 37e: the account (7 October)

From game 9. Its brief turns the review of that game's reckoning into fourteen items, with
the owner's three rulings of 7 October (D1, rows 20 to 22). Nothing in `docs/agents/` was
touched.

**What it built**, by the changes file (all in G3):

- One rule for believing an observation: weighed, taken or kept.
- The same thing seen again tells the master nothing new.
- A doubt that grows through the hours she has no way, and is said as it lies.
- A fix that takes the near marks.
- The master works the tide himself; `allow ... knots of set` replaces his tide until
  `allow the tide by the book` hands it back.
- A shaped course makes good, and says when its line crosses the land or passes close along
  a shore.
- The primer teaches the rule, `observe an amplitude` and the captain's allowance for a
  set.

**The lead's checks.**

- **37e is built** (7 October) and has passed the lead's checks: the whole suite run again
  (2,836 passed, with the seven standing expected failures and two new ones), the guarded
  files untouched, the account measured again on two passages, and a test of the lead's
  own that asking for a reading never changes the game. What it does, what it measured and
  what it left undone are in the build folder's `CHANGES-m5c-c.md` under 37e. In short:
  the one rule, the honest doubt, the fix's near marks, the master's tide and a shaped
  course that makes good are all in; near land the account is as good as before or better
  and the master's doubt is now honest; the night crossing of the open Channel is no
  truer than it was; and two beats of the recorded passages are lost for now (the
  schooner's pilot does not board; the naval cruise does not speak the French brig).

**The suite.** The builder's fast tier ended `2594 passed`; the whole suite
`2836 passed, 9 xfailed`.

**The recorded passages.** The day of gate 5a is unchanged to the digit. The other five
moved. The frigate's passage, the thick-weather passage and the merchant passage come
through. The schooner's comes through to her anchor, but the Falmouth pilot hails her and
does not board. The naval cruise does not come through whole: the French brig is chased
and lost, not spoken. Those two are the two lost beats, each marked as an expected failure
(G10, and part L for the cruise).

**Not done**, by the changes file: three of the four figures the brief asked of the
measurements were not fully met; at anchor in the Bay of Brest the master is surer than he
should be; a wrong chronometer can displace a good account; the number in the one rule is
two where the brief said three; in the open Channel the master's tide is a rough
allowance; and the sentence of spec truth 59 is left for the lead. Each is set out in
G3.

**The audit on 37e**: take, with one named change before the next game near land in thick
weather, and one piece of data. The change is that a cast of the lead should not move the
account beyond the account's own doubt, which is the review's own proposal after game 10
and which the auditor did not test. The data is the cruise's scenario line (M, 2.4). It
found that nobody has measured 37e's figures again since 37f moved the passages (N, 4.2;
appendix 1, 1.13).

### F5. 37f: lying to, and the ground (7 October)

From game 9 and the owner's note 6 on it, with what the first review had found of ship
handling, the ground tackle and the log. Its brief has twenty-one items in three parts,
with the owner's three rulings (D1, row 24).

**What it built**, by the changes file:

- Part one, lying to (G7): a ship hove to stays hove to, on the tack she hove to on;
  `fill away` fills her on the tack she is on, and `fill away and steer <course>` is taken;
  the record that she is hove to is cleared by the anchor, by weighing, by a tack or a wear
  and by the ground; `trim sails` hove to is refused, and the shipped books' trim rules
  carry the guard.
- Part two, the ground (G8): an anchor's name is honoured; `heave in` is a new order;
  `let go` says its scope and takes one; three warnings as the anchor goes;
  `come to an anchor in twelve fathoms` means the depth; `let go the anchor` logs "Brought
  up"; the dragging line once an episode; the ground's words; sail handled at anchor and
  aground. And the fore-and-aft cast (G7).
- Part three, the log's lines (G6, G9): no wind-shift line in airs too light to have a
  direction; the aback lines by state; "already" lines routine; a cast that finds no bottom
  routine; a standing order with nothing to do said once a watch; a standing order's place
  checked when it is entered.

**The lead's checks.**

- **37f is built** (7 October) and has passed the lead's checks in the same way. Tried by
  the lead from the owner's own game: the brig of game 9, hove to from her state at 17:39
  on 14 June, went through the wind in the third minute on the build before and lay with
  sternway on; on 37f she settles five points from the wind with under a knot of headway
  and holds it, and `fill away` then draws on the same tack. From her last state, moored
  in Brest road, `veer the small bower to 80 fathoms` veers the small bower to eighty,
  where it had put the best bower at 148. The rest is in `CHANGES-m5c-c.md` under 37f.
  The two lost beats of 37e are still lost: the schooner's pilot is 37h's, and the
  cruise's meeting with the brig fails on a fault of the chase order, found by the
  builder, which no package yet holds.

**The suite.** The builder's fast tier ended `2683 passed`; the whole suite
`2933 passed, 9 xfailed`. The two failures that 37e left both still stand.

**The recorded passages.** Re-measuring took sixteen whole-passage runs where the brief
budgets a dozen. The day of gate 5a sails the same track to the last figure. The frigate's
passage comes through with two changes to her book. The schooner's comes through to her
anchor, her pilot still not boarding. The thick-weather passage comes through with no
change to its book. The merchant passage comes through, and better: she casts when she gets
under way, and the pilot of Brest stays aboard to the anchor. The naval cruise keeps her
station and reads her letter, and the French brig is still chased and lost. The changes
file gives a new reason for it, a fault of the chase order. The audit sailed the cruise
and found that reason partly wrong (below, and M, 2.4).

**Not done**, by the changes file: the cruise's stranger is not spoken; the schooner's
pilot does not board, which is left for 37h; a dragging that relapses is still more than
one urgent line; the fore-and-afters hove to make more than a knot and a half; a course
shaped with next to no way on her is worked for that way and can be a point out; and two
things found and left, one in the cruise's book and one in the test machine's workers.
Each is under its subject in part G.

**Corrected by the audit: the cruise.** The lead's paragraph above says that the cruise's
meeting with the brig "fails on a fault of the chase order, found by the builder", and
37f's section of the changes file says that the book orders a course across the wind from
her head, that the helm takes her straight through the wind with every sail aback, and
that making the chase order wear her, or the scenario's hours, would bring the meeting
back. The lead passed the builder's account on without checking it. The auditor sailed the
cruise and found otherwise (M, 2.4). She is not taken through the wind: she is turned 175
degrees the other way, by the stern, with her yards left braced for the old tack, and is
caught aback with the wind on her quarter. The brig is at a fixed place that the frigate,
since 37e, has already passed. A mend of the kind named did not bring the meeting back in
the auditor's trials; moving the brig's place in the scenario file, with no code changed,
did. And the passage as pinned holds a second urgent "Taken aback", at tick 83957, which
neither the builder nor the lead reported.

**The audit on 37f**: take, with the cruise's mark written again, so that the text on
`test_the_naval_cruise_speaks_the_stranger` and the paragraph in the changes file say what
the ship does and the mend goes to the right place. It adds that the handling fault
deserves a line of its own in the work-packages document: a large alteration of course
given to the helm alone, by `give chase` or `shape a course for`, leaves a square-rigged
ship's yards braced for the old tack (N, 4.2).

### F6. 37g: the station's safety, and the deck, the leaving and the grant (7 October)

From the first review's findings on the officer's authority and the harness, the opt-out
path of 37b, the owner's answers and rulings, and game 9. Its brief has twenty-four items in
three parts. By the owner's ruling it is the one package that touches the consent brief.
No model was seated and none was asked in building it: everything was proved with the
suite's own scripted stations.

**What it built**, by the changes file:

- Part one, the station's safety (G12): a key to each seating; a turn of sixteen orders,
  with reads counted apart and the leaving tools always run; the captain's word in an open
  turn; a stand-by with the deck that danger breaks, that refuses a wait that cannot end,
  and that has a bound; a detector that counts only orders that undo one another; a silence
  detector that hears calls inside an open turn; a paused or silent officer who does not
  keep the deck; the doors mended; a sample that says who gave each order; whose order a
  line is, and where the officer is.
- Part two, the deck, the leaving and the grant (G11, G13): the deck given and taken
  without unseating the officer; three ways of leaving; the opt-out path mended; relief;
  the journal read; bearings and fixes in the officer's domain; a named grant that means
  what it says; the general grant; the way out of danger.
- Part three, the words (G13): the consent brief revised once, in four sections; every
  model with a yes on record asked again at its next seating; the documents and the
  decisions log.

**The lead's checks.**

- **37g is built** (7 October) and has passed the lead's checks: the whole suite run again
  (2,980 passed, the same nine expected failures), no recorded passage moved, no consent
  record touched, both of the owner's saves loading from their checkpoints and playing on,
  and the consent brief's four sections read sentence by sentence against the words he
  approved. They match, but for one word the builder changed and said so ("carries" the
  last handover note, for "opens with", since every brief opens with the disclosure). The
  rule as it stands will ask every identity on record again at its next seating, naming
  the four sections. What it built is in `CHANGES-m5c-c.md` under 37g.

- **The consent brief was then made leaner, by the owner's word, before any model was
  asked again** (7 October, evening), so it is still revised once. The lead had put two
  sentences to him that the build had outrun: the deck taken from an officer silent for
  his hour, and three things the general authority keeps back that the brief did not name.
  He added the first, and then asked whether a consent question needed so much of a
  station's detail at all. The lead drafted a leaner brief
  (`drafts/consent-brief-lean-draft.md` in this folder, with a table of what moved out and
  where it lives), he approved it as it stood, and 37g's builder put it in and settled the
  stations' briefs in a second pass. The brief now holds the question and the kind of
  thing a model would be agreeing to; a station's particulars (which orders lie within it,
  what the harness counts and by what numbers) are in that station's own brief, and the
  brief's *The record* says so and says what brings the question again.

- **The second pass has passed the lead's checks.** The brief's body is the approved
  draft to the character (1,371 words where it was 1,896). Nothing changed but the
  agents' code, two test files, the documents and one new fixture; all nineteen consent
  records are byte for byte as they were, and the owner's saves, notes and bridge settings
  are untouched. Each thing that moved out is in the officer's brief, and in the watcher's
  where it concerns a watcher, and each number there is the code's own
  (`evidence/station-briefs-after-37g-second-pass.txt` is both briefs as a model is sent
  them). What the general authority keeps back is now one text, said the same in the
  officer's brief, in the grant's line in the log and in the sample that gives the grant
  or the deck: the port's business, his standing orders, a new destination, a chase, the
  reckoning set by hand and the tide allowed in it, sending for a person, and anything
  that cannot be undone. The seven commitments are unchanged. The whole suite, run again
  by the lead: 2,981 passed, the same nine expected failures, no recorded passage moved.
  Both of the owner's saves load from their checkpoints and play on. Every identity with a
  yes on record is asked again once at its next seating, with four sections named (five
  for the three September records, which already owed the opening). It is in
  `CHANGES-m5c-c.md` at the end of 37g.

- **Three small things that pass left, put to the owner.** The harness counts a fourth
  sign of a stuck model that the consent brief does not list (three empty replies in a
  row where an answer was owed, since package 29c; both stations' briefs state it), and
  the lead recommended seven words in *Being stopped* before any model was asked.
  `stand_down` takes a handover note and does not insist on one, which the lead would
  leave, since an exit is never to be refused. The watcher's brief lists two tools it is
  refused (`hand_over`, `handover_note`), which is for the follow-up pass.

**The suite.** The builder's fast tier ended `2730 passed` and the whole suite
`2980 passed, 9 xfailed`; after the second pass, `2731 passed` and
`2981 passed, 9 xfailed`. The six recorded passages carry no station, and their digests did
not move. The auditor's own run of the whole suite on the build as it stands ended
`2981 passed, 9 xfailed in 1179.13s (0:19:39)` (M, 2.5).

**Not done**, by the changes file, after both passes: what cannot be undone is, today, one
order (`cut away`), which was the officer's already, so the general grant keeps nothing back
in practice under that head; the REPL's turn mode does not put the consent question again
after an opt-out; a standing order the officer writes under the captain's word stays in the
book when that word ends; an act at the very tick a station is seated is still not replayed;
the watcher's brief still lists `hand_over` and `handover_note`, both refused to a watcher;
and `stand_down` takes its note but does not insist on one. Each is under its subject in
G11 to G14.

**What a model already seated in an older save will find different** is set out in the
changes file under 37g, and in short in G14.

**Corrected by the audit.** The lead's paragraph above says the watcher's brief lists two
tools it is refused. The audit read the brief as a model is sent it and found three:
`hand_over`, `handover_note` and `submit_order` (N, C9). It also found that the second
pass changed the code and did not change the build's name, which is still `m5c-c/37g`
(N, 3.8); that the general authority keeps back more than the list on record (N, C6; G11
has the lead's note on it); and that the officer's brief still says "as a lieutenant of
1806" (appendix 1, 1.5).

**The audit on 37g**: take, with one named change before a local model is seated again,
and one ruling. The change is to the handover's reserve: until the runner counts tokens by
the server's own figure, either put the default back to a share of the context or seat
local models with a larger `--handover-reserve`. The ruling is the owner's word on what
the general authority keeps back beyond his list. The consent brief should go in exactly
as it is (N, 4.2).

### F7. Not built

- Nothing beyond 37g is approved. 37h, the pilot, is not written. What the review of game 10 proposes (part K)
  (the local runner first, then amendments to 37e and 37f, and words) waits on the owner.

- The last step of the plan, `the port` and `the depth of water` by the captain's means
  and the small faults, is not begun (G4, part I).
- The gate's remaining play is not done (part L).
- By the audit, nothing at all in the code or the data has changed since game 10 was
  played: its two saves carry the fingerprint the build has today (appendix 1, 1.11).

## G. Findings by subject

Each subject is followed from start to finish: what was found and on what evidence, what
the owner ruled, what was built and in which package, how it did in the games played
afterwards, and what is left. A finding of the first review gives where it was seen (game
and tick) and, where the cause was traced, the place in the code as m5c had it.

Navigation close to land is the weightiest area: one grounding, two near misses, and an
account that was wrong with the land in sight. The owner's notes 19 and 24 put it down to
the reckoning near visible land. The record says the chart reckoning itself is sound in
open water, and that close in it was defeated by a handful of specific faults, most of them
small. G1 is the case. G2 to G5 are the faults, each with what has been done about it.

### G1. The *Harpy* on Penlee Point (game 2, 19 June; lead, from the log)

| Time, tick | What happened |
|---|---|
| 13:37, 635,868 | Taken aback. The officer lets go the anchor "in 11½ fathoms of sand, a mile off Rame Head and Penlee. The wind is flipping between E by N and SE every few seconds." |
| 13:38, 635,891 | The captain: `avast all`, which belays the anchoring; `Steer north east`; "I'll con her, don't worry." |
| 13:43, 636,204 | The captain: `Steer north northeast`. |
| 13:46, 636,387 | The officer: "Sir, NNE is heading straight at Penlee Point! ... about three quarters of a mile, under ten minutes at 5 knots. Bear away to NE now". |
| 13:48, 636,493 | The captain's bearing: "Penlee Point bore NNE, a mile by estimation." True distance 2.9 cables. |
| 13:50, 636,618 | The officer: "The water's shoaling fast: 11, 9½, 5½, now 4½ fathoms in six minutes ... I strongly advise letting go the anchor now". |
| 13:50, 636,626 | The captain's bearing: "Penlee Point bore NNE, a mile by estimation." True distance 1.7 cables. |
| 13:50, 636,631 | The officer lets go "on my own word, sir, under the grant for the watch". |
| 13:50:53, 636,653 | "She has taken the ground forward ... two fathoms of water by the chart, and she draws 11 feet; she struck at three knots". |
| 13:51, 636,660 | "Drake's Island bearing NNE, steady and closing: distant three miles." |

The pilot had been aboard for sixteen hours and "in charge" by the log. Asked once, he
repeated his boarding speech. Four things together put her ashore:

1. **A wind that took her aback three times in thirteen minutes** (G5).
2. **The lookout's distance frozen at "a mile"** (G2).
3. **An account 0.3 mile east of her when NNE was chosen**, so that on the captain's chart NNE
   was the gap inside the Dragstone. It had been within 110 metres ten minutes earlier; it
   ran on at the hourly log's 3¾ knots through two losses of way.
4. **The anchor belayed.** `avast all` stopped an anchoring that would have held her.

Nothing urgent named the land. The three urgent lines were "Taken aback". Three "steady and
closing" hails had come at three miles, 46 to 59 minutes earlier, as 3 of 136 notable lines
inside one stand-by. The officer's two warnings are spoken lines, which the log files as
routine. The captain afterwards: "I was reading the reckoning on my chart that was wrong, and
trusted it too late" (636,831).

Two of the notes need correcting from this. An emergency clause (the model's comment on 15)
would not have changed the afternoon: the officer held the anchor, the tack and the helm
under standing allowances, and used them. And the reckoning (the comment on 19) was one cause
of four.

**What has been done about each cause since.**

1. The wind was the sea breeze changing direction every few yards. **Built**, 37d: it blows
   steadily from the sea (G5).
2. The lookout's distance is judged afresh as it changes. **Built**, 37d (G2).
3. The account. A bearing no longer writes the lookout's distance into it (37d), and since
   37e every observation is weighed by one rule (G3). **Built.**
4. The anchor belayed. `avast all` was the captain's own order and nothing was proposed
   against it. What was proposed is a plain way for the captain to take the con: since 37g
   taking the deck does that without unseating the officer (G11). **Built.**

And for what was missing that afternoon. The lookout now cries land ahead, urgently under
four minutes off (37d, G2). What the officer says is a notable line in the log, with the
deck or without (37g, G12). The pilot who said nothing is 37h, which is **not built**
(G10). The *Harpy*'s save of tick 602,100, ninety minutes before she weighed that day, is
kept as one of the build's test fixtures (G14).

### G2. The lookout and the sight of land

#### What the first review found

**The lookout's distance is drawn once and held until the ship herself has run a mile**
(lead; `lookout.py:362-386`, `ESTIMATE_HOLD_NM = 1.0`). It was meant to stop a calm
re-drawing a headland's distance. It is applied unchanged to land a few cables off and to
moving vessels. This one rule is behind:

- "Penlee Point ... a mile", said 27 seconds before the *Harpy* struck, and held from 13:37
  to 02:01 next morning with the point 8 to 1½ cables off;
- "The Isle of Bas ... two miles" in seven bearings over 44 minutes while the *Amazon* ran in
  to three fathoms, anchored, weighed and stood out (120,966 to 123,625);
- every "fixed distance" vessel in the notes: the frigate at "eight cables" for hours, the
  Falmouth cutter at "two miles" for 37 minutes while her bearing swung from S to NW by N,
  the St Mary's gig still "two miles" after she had hailed from within four cables;
- "Mr Moal left in his boat while it was still a mile away": the mile was eighteen minutes
  old, and the boat had hailed from within four cables three minutes before he left.

**Nothing warns of land ahead** (`lookout.py`). No line the lookout can raise is urgent.
Each named feature is hailed once per sighting. "Steady and closing" is notable, said once
per sighting at about a league, and its words carry the held distance. The unnamed shore is
hailed only when no charted headland is in sight (`lookout.py:294`), so off any named coast
it is silent. Shoals and breakers are never seen. The *Speedwell* shoaled from 15 fathoms to
3½ north-west of the Isle of Bas with no word (199,784 to 200,467). The *Amazon* found three
fathoms the same way. The *Harpy* struck the steep foot of Penlee Point, where there is no
chart feature; the point's own coordinate is 250 to 300 metres inland.

**A landmark is one point, and an island is its middle.** A chart feature has one latitude
and longitude and no outline or parts (`chart.py:240-268`). The Isle of Bas has no extent;
its coordinate is 0.8 mile from the west end of the island and 1.3 from its outlying rocks.
Four of the Roscoff pilot's seven marks are not features at all. At St Mary's the transit and
the daymark never appear in a lookout line, and the Spanish Ledge is charted on the wrong
hand for the pilot's words.

**Parity, as the owner's note 24 asks.**

A human at the browser sees the shape of the coast; a model has a list of bearings to
points. But the chart is drawn about the account, so when the account is out the picture
misleads the human too. The words give a bearing to the compass point, 11¼ degrees, while
the account is moved with a figure good to a degree and a half; the human sees the result on
the chart and the model does not. The *Speedwell*'s officer: "my bearings are rounded to the
point, so you're better placed." Shown a picture of the chart afterwards, the *Amazon*'s
officer saw at once that the account's track ended on the island's own western ledges
(`evidence/amazon-post-session-chat.md`).

The first review recommended three things here (I2, items 1, 5 and 6): judge a distance
afresh when it has changed by a tenth, for land and sail alike; make the shore always a
sighting, with a reading of the nearest land; and a cry of land ahead. It called the first
"the single most useful change in this report". None needed a ruling.

#### What was built: 37d (6 October)

By the changes file and the package's brief (items 5, 9 and 10):

- **The lookout's distances follow the ship in.** A distance is judged afresh, with the same
  eye's error for the sighting, whenever it has changed by a tenth, for the land and for a
  sail alike. The rule that held an estimate until the ship had run a mile is gone. A calm
  still re-draws nothing. "Penlee Point ... a mile" at two cables cannot happen now.
- **The nearest shore is always in sight within a league**, hailed once a sighting, where
  before it was spoken of only when no charted headland was in sight.
- **`the nearest land`** (and `the nearest shore`) is a reading every station has: where it
  lies from the ship's head, its bearing, its distance by estimation in the lookout's own
  words, and the coast's name where the chart has one. Beyond a league it says "no land
  within a league"; when the weather or the night hides it, "not to be seen". The standing
  dialect takes it (`when the nearest land is under half a mile then ...`), though not yet in
  cables. The audit asked for it of a ship made in memory and was answered "The nearest
  land: the land about Trefusis Point, on the larboard quarter, bearing SE by E, a cable".
  Whether every sample carries it the audit did not check.
- **Land ahead.** The lookout warns when she is standing into the land: a notable line
  under ten minutes off, an urgent one under four, each once an approach. It reads her
  true motion over the ground, and only toward what can be seen. In fog it is silent and
  the lead is the guard.

Left out of 37d on purpose, by its brief: a taken bearing said to the quarter point; a
landmark's parts and how marks stand to one another; and a drawn chart for a door that can
take pictures.

#### In play: game 9 (37d)

**`the nearest land`.** The officer found the reading in the library and wrote two standing
orders on it ("every glass, if the nearest land is under 3 miles then take a fix").

**Land ahead.** Three lines. The urgent one, "The Mingan close ahead, on the starboard bow,
four cables!", came five minutes before she passed the rock at 1.2 cables. More follows.

**At the Mingan the cry was right, and the map was not.** The owner told the officer not to
overreact, "the alert does not mean a strike incoming". By the true track she passed 1.2
cables from the rock. When the lookout cried it was 4.8 cables off; the account, which is
what the owner's chart draws, had it at 8.3. So the warning was sound and the picture he
judged it by was three and a half cables kind. One change is worth making to the words: the
line said "She will be on it in three minutes", and she was never going to be on it. A cry
that says how near she will pass ("standing to pass within a cable of it") would be truer
and would not be read as a strike.

**"Take a bearing of Bas"**, with only the island's shore in sight and not yet its mark,
is now refused as "the land close aboard is no mark of the chart ... name a headland", to a
captain who has just named one. Before 37d it said the Isle of Bas was not in sight and
listed what was. The older words were the clearer.

Two more of the lookout's lines were questioned by that game's officer and found to be as
said (H6): "The chart ends here", which reads as if the world stops and is the lookout's
word for no charted marks beyond; and "A moonlit night; the land may be made out at a
league", said at 22:44 on the 13th inside a thick fog.

#### In play: game 10 (37d to 37g)

One land-ahead line in 63 hours. The officer was woken at 16:58 on the 14th by Peninnis
Head closing.

**The reading of the nearest land in fog invites a wrong reading.** In thick weather it
says "not to be seen: in this weather the shore shows within a cable at most". The officer
read that as land within a cable. At 08:01 on the 13th, in mid-Channel with no land within
leagues, it hove to on that, under the general authority, and the owner had to countermand
it; the yards left aback by the belayed heave-to were one of the eight alarms. It quoted the
same words again in the Sound.

#### What is left

- **The land-ahead cry's words.** The review of game 9 asked that the cry say how near she
  will pass, and not "She will be on it in three minutes". **Not built**: the audit read the
  lookout's code and found no such words; the cry says where the land lies, its distance and
  the minutes. The review also pushed back on making the cry any milder (J2), and the audit
  found the ten minutes and the four unchanged.
- **The fog reading's sentence** ("not to be seen: in this weather the shore shows within a
  cable at most"). **Proposed** after game 10, among the words (part K). **Not built.**
- **"Take a bearing of Bas"**, the refusal's words. No package holds it, and the audit's
  ledger has no row for it.
- **Shoals and breakers are never seen**, and the lookout's cry is only of land that shows.
  The other half is the pilot's warning of the shoal he knows, which is 37h and **not
  built** (G10).
- **A landmark is one point.** Features by their parts, and how marks stand to one another,
  need design first (I7, item 4). **Not built.** The chart's faults named above (the Isle of
  Bas's place, the Roscoff pilot's marks that are not features, the transit and the daymark
  at St Mary's, the Spanish Ledge) are in no package; game 10 adds the depths of St Mary's
  Sound (G10).
- **The chart in words.** From the review of game 9:

  The owner raised it in the game (a "show me the chart" feature,
  "that's on the books") and the officer called it "the single most useful thing on the
  books for this kind of work". It is the second officer to ask: the *Amazon*'s asked for "a word
  picture of the near coast" (`evidence/amazon-post-session-chat.md`). **Design**, as in I7, and now with a plain
  requirement from play: what the officer lacked was where the shore runs between the named
  points. Whatever is built must be drawn from the account and not from the truth, or it
  becomes a fourth reading that gives the position away (G4).

  **Not built.**
- **Image tools** for doors that can take pictures (the owner's note 25) wait on the same
  thing existing as words (I7, item 7; J1, item 9). **Not built.**
- **A fog signal** (a bell; a gun waits for powder) is **later**.

### G3. The account

The reckoning has been through three states in the week: as m5c had it, with three separate
rules for believing an observation; as 37d left it, with the bearing mended and
`take a fix` added; and as 37e left it, with one rule, an honest doubt and the master's own
tide. Game 9 was played on the second and game 10 on the third. Game 10 then found two new
faults in the third.

#### What the first review found (games 1 to 8, on m5c and m5c-b)

**Every bearing writes that held distance into the account** (lead;
`reckoning.py:1358-1415`). `take a bearing` does two things. It draws the account onto the
bearing line, with a figure good to about a degree and a half. It then applies the lookout's
distance by estimation as a second line, trusted to 15 per cent. That estimate carries a
random factor drawn once for the whole sighting, and is frozen as G2 describes. So each single
bearing is taken as a full fix: a good line and a poor distance. Bearings of different marks
disagree by their separate distance factors and the account jerks from one to the other. A
standing order taking bearings every few minutes makes the master ever surer of the wrong
place. This is what the owner has seen: a charted position still far off with bearings taken
regularly, and one bearing moving it miles for no clear reason.

**A line taken after two miles' run replaces the account across it; within two miles it is
only blended** (lead; `reckoning.py:675-727`, `FIX_RUN_NM = 2.0`). The module says why: the
master's stated doubt leaves out biases he cannot know, so weighing by it "would let a bad
account outvote a good sight". The rule never asks whether the sight is better than the
account. It is deliberate, documented in the module, and against the letter of the spec's
§13 ("the simplest Kalman form"). Its effects:

- *Amazon*, 51,502: a lunar "which he would trust within 50 miles" moved the longitude from
  4° 22' W to 4° 53' W, fourteen hours out of Falmouth, and the stated doubt grew from two
  miles to twenty-five. The captain set it back by hand.
- *Speedwell*, 86,831: a lunar "within 20 miles" moved the account 33' east. Back-reckoned
  from the landfall, the old account was 5 to 9 miles too far west and the lunar 12 to 17 too
  far east. The notes are right that the worse figure replaced the better. They are wrong
  that the old account was "good to about 2": that was the evening before, nine hours and 27
  miles earlier. The officer's own retraction at the landfall (182,230) rests on a wrong sum.
- *Harpy*, 159,648: a lunar taken while hove to moved the account 0.0 miles, because she had
  not run two miles. The same rule then left two dawn bearings of marks in clear sight
  moving the account 0.35 and 0.54 mile while it was 4.8 miles out and "within a mile" by the
  master's words (168,781).
- Game 1, 25,200: the noon latitude was not adopted, eight miles of difference standing.
- The first sounding after a run jumps the account in the same way.

**The dead reckoning between sights is coarse close in.**

- A merchantman's log is hove two-hourly, and the account runs on at the last cast. On the
  *Speedwell* a 5½-knot cast taken as she hove to served for eight hours through two
  anchorings (27 June). On the cutter a quarter-knot cast taken lying-to stood for 1 h 49 m
  of sailing (game 7, 18,038).
- Fore-reaching while hove to is not counted, and the doubt does not grow (*Harpy*, 14 June
  00:22 to 03:01).
- At anchor the position only creeps, but the reading "the distance run since noon" keeps
  multiplying (*Harpy*: 23 then 45 miles at anchor; game 5: 29 to 39). The note that the
  *Harpy*'s reckoning "kept advancing while she lay at anchor" is true of that reading on one
  night of three.
- Every scenario opens with the account a mile out, even at anchor in a named road
  (`reckoning.py:929-933`).

**The danger list is drawn from the account, in whole miles** (`reckoning.py:1707-1744`).
Under a quarter of a mile it reads "no distance". On the *Speedwell* it named the Triagoz
from fifteen miles away, and at 13:03 on the 27th she was steering by the account at the
Gilstone, 0.85 mile ahead and covered. On the *Harpy*'s last morning it was right and was
disbelieved.

**The officer may not take a bearing.** `take a bearing of ...` is refused to him as "the
master's for the captain" in five of the seven games with an officer. On the *Speedwell* the
captain took 91 bearings and the officer one. Bearings are the navigation close in, and the
man with the deck cannot take them.

**What worked.**

Cross bearings of charted marks after a run put the account right at once (the Isle of Bas,
St Agnes light, the Manacles). The noon latitude is honest, with "No sight" on thick days.
`shape a course` warned of the Gilstone and the Old Wall. The officers' lead orders did real
work: a three-minute lead was entered six minutes before the *Speedwell*'s 3½-fathom cast.
In game 1 the book's lead and bearings every five minutes took the schooner through the
Goulet cleanly.

The first review recommended (I2, items 2, 3, 4, 9, 11 and 12): a single bearing gives a
line and no more; a new order, `take a fix`; no fix from a bearing of a sail; a sight
blended unless it is the better figure, with the line saying what the master did; the
account kept honestly at anchor, hove to and after a manoeuvre; and bearings within the
officer's own domain. It pushed back on the owner's note that the reckoning should be made
very precise close to land: not by nearness, which would be the truth leaking into the
account (J1, item 1).

**The owner's answer on fixing (5 October).** The question was:

*The master's routine, or an order and a standing order?*

**Answer.** `take a fix` can simply be an order, used freely like any other. It need not be
a routine.

**What follows.** The recommended `take a fix` as written (I2, item 3), open to the officer and usable in a
standing order (`every glass then take a fix`). The master does no fixing of his own, and
the question (I6, item 5) is closed.

#### What 37d built (6 October), and its second pass

By the changes file:

- **A bearing gives a line.** The first pass took the lookout's guessed distance out of the
  account altogether. That cured the jerking between marks, but a landfall on one headland
  after a long run was left miles along its line: the schooner of the recorded passage was
  6.8 miles out where she had been 0.9.
- **The second pass, which the owner approved**, lays the distance down when the account's
  own doubt along the line of sight is greater than the guess's, and the line says so: "The
  Lizard bore N by W, five leagues by estimation; the account laid down at that distance,
  the estimate being the better figure: moved three leagues to the SW." Once laid down, the
  next bearing of that mark lays nothing down, so the account does not creep; just after a
  good fix none is laid down, so two marks cannot pull it to and fro. Otherwise the line
  gives the guess, and the account's own distance beside it when they disagree by a
  third.
- **A bearing of a sail moves nothing** (G4).
- **`take a fix`**: cross bearings of two or three marks, the account set where they cross.
  Said bare, the master picks the marks. As 37d built it the fix set the account outright,
  whatever the account said before, and the master picked the marks that cut at the widest
  angles, nearness only breaking ties. The officer could be allowed it with
  `you may take a fix`. The standing dialect takes it (`every glass then take a fix`), and
  each bearing rule of the four scenario books was given a fix after the bearing.

**The Goulet, and the lead's correction.** In the first pass the recorded merchant passage
struck on the Mingan. The second pass brought her through by putting her pilot-water rule
back to the bearing alone and moving two of her points in the Goulet, and put the strike
down to the fix "putting a worse account in the place of a headland's bearing every five
minutes". The lead measured the three runs from the package's own dumps on 6 October, and
the figures did not bear that out. The account's distance from the truth, as a median over
each leg:

| Leg | Before 37d | The fix every five minutes (first pass) | The bearing alone (as delivered) |
|---|---|---|---|
| The Iroise to the road of Bertheaume | 0.91 mile | 0.50 | 0.45 |
| The Goulet | 0.45 mile | 0.17 | 0.48 |

With the fix the account in the Goulet was nearly three times as true, and it was with that
account that she struck. Of the sixty fixes on the two legs, nine left the account worse
than it had been a second before. So what set her on the Mingan was the book: its points
and its 0.4-mile rules were tuned at seed 7 to an account that lags her on the flood, and a
course shaped for a point allowed nothing for the stream. Seven tries at moving the points
with the fix kept did not bring her through within the pass's budget. She came through as
delivered because the account in the Goulet was again about as wrong as it had been before
37d: she passed the Mingan 1.8 cables to the north (328 m; 311 m before 37d) and the shore
under Petit Minou 1.6 cables off (294 m; 273 m before). The book was to be tuned for a true
account once 37e had settled the reckoning's rule.

**What 37d left undone**, by its changes file. The account in the Goulet was still not a
true one: as she gets under way from the road it runs seven cables wrong, and on the flood
it lags half a mile astern of her, while believing itself good to a cable. And
`take a fix` set the account outright and picked its marks by how they cut and not by how
near they were: on the merchant's two pilot-water legs the nearest land's own mark was one
of the fix's marks in 22 fixes of 60; the fix's true error was a median 0.37 mile in the
Iroise, by marks six to ten miles off, and 0.14 mile in the Goulet, by marks three and a
half to six miles off. Both went to 37e.

#### In play: game 9, on 37d (6 October)

**The account near land.** The account's distance from the truth, a sample a minute:

| Stretch | Typical (median) | Worst |
|---|---|---|
| Falmouth to the landfall, open Channel, a night and a noon sight | 2.8 miles | 5.5 |
| The landfall to the anchor at Roscoff | 1.6 miles | 7.1 |
| At anchor, Roscoff | 1 cable | 1 cable |
| Out of Roscoff along the coast, fixes every few minutes | 5 cables | 2.8 miles |
| Four hours of fog, standing off | 5.6 miles | 8.3 |
| Round Ushant by night, one light in sight | 2.0 miles | 4.8 |
| Hove to six hours, four of them in fog | 4.3 miles | 4.9 |
| Calm and light airs off Ar Men, a night | 2.0 miles | 4.7 |
| Noon on the 16th to the mouth of the Goulet, fixes every quarter hour | 5 cables | 4.2 miles |
| The Goulet to the first anchor | 2 cables | 4 cables |
| At anchor in the Goulet | 2 cables | 4 cables |

With marks in sight and fixes going, the account stood within one to five cables of the
ship. That is the improvement the owner's note 1 reports, and it is real. Out of sight of
marks it was two to five miles out, and once eight; the owner's note 2, below, takes that up.

**The landfall.** The first bearing of the Isle of Bas, at twelve miles after a night's run,
took the account from 7.1 miles out to 0.7: the estimated distance was laid down, as 37d's
second pass meant it to be.

**`take a fix`.** 61 fixes. The fix's own distance from the truth: a median of 1.2 cables,
nine in ten within 7 cables, the worst 1.1 miles. Three things about it are taken up below:
it chooses far marks when near ones are in sight, its "good to" is too hopeful, and at anchor
it can move a right account.

**The owner's note 1: "Take a fix + other reckoning/account changes seem good so far."** Borne out by the
measurements above. Three qualifications, all taken up in 37e:

- *The fix prefers far marks.* In the Goulet four fixes were worked by marks three to seven
  miles off (Camaret, Brest, Conquet, Pezeaux), with Petit Minou inside a mile and the Mingan
  closing from two. Their lines met within six cables at best and a mile and a half at
  worst. They left the account 1 to 3 cables out; each bearing and distance of Petit Minou
  then brought it to one cable or less. The cause is the brief's rule (the lead's): the
  master picks the marks that cut at the widest angles, and nearness only breaks ties.
- *"Good to" is too hopeful.* In 12 fixes of 61 the true error was more than twice the
  stated figure. The cocked hat "inside three cables" that the officer admired at 06:05 on
  the 16th was 1.1 miles from the truth. Every bearing carries the compass's own error, about
  two and a half degrees in this ship (measured: 2.2 to 2.6), and the three lines of a fix
  share it, so a tight hat can sit well off the ship: four cables at ten miles, a quarter
  cable at one mile. The stated doubt counts only each line's separate error. The cure proposed: count
  the shared error, which also makes the master prefer near marks. The period's cure is in
  the game already and nobody used it: `observe an amplitude` corrects the variation.
- *A fix replaces the account even when it is the poorer figure.* Moored in Brest road, her
  account right to a cable, the standing order's fix by the castle and St Matthew's light
  (eleven miles off) moved it nearly a mile, and the next one left it six cables out. It goes
  with the rule under note 5.

**The owner's note 2: "Reckoning uncertainty drift with no visible marks/fixes was deemed a bit low by the
officer of the watch".** It is far too low for these waters, and the measurements make the size plain.
The master's stated doubt beside the true error:

| When | The true error grew | The master's doubt went |
|---|---|---|
| Fog, 14 June 12:30 to 15:00, standing off under sail | 2.8 to 8.3 miles | 0.5 to 0.9 mile |
| Hove to, 15 June 10:00 to 12:00 | 3.3 to 4.8 miles | 1.08 to 1.12 miles |
| Becalmed, 15 June 19:30 to midnight | 1.0 to 4.7 miles | 2.2 **down** to 1.5 miles |
| The ebb in light airs, 16 June 08:00 to noon | 0.5 to 4.2 miles | 0.2 to 0.6 mile |

Whenever she had no observation the account went wrong by about a mile an hour, sometimes
two, and the doubt grew by about a tenth of that. The officer's guess ("a mile or two an
hour") is close to what happened. Four causes, each read in the code:

- The doubt's growth is sized for open water: a fifth of a knot of unknown set east and
  west, almost none north and south. The streams off north Brittany and in the Iroise run
  two to three knots.
- Hours hove to are left out of the reckoning altogether: the account does not move and the
  doubt does not grow, while she drifts on the tide.
- An observation shrinks the doubt each time it is taken, even the same one again. Eight
  casts of the deep-sea lead on a flat sandy bottom took the doubt from 2.2 miles to 1.3 by
  just after midnight, while the error went from one mile to nearly five. This is the
  officer's "the doubt got smaller while she drifted becalmed", and it is right.
- The words say "a mile" for anything under a mile, so the master sounds the same at one
  cable as at nine.

This became the heart of 37e. One choice in it was the owner's, and is set out
below: how the master's doubt comes to know that the tides run strong where she is. A second
remedy is already in the game and was not used: `allow two knots of set to the westward`
tells the master to carry a stream in his reckoning.

**The owner's note 5: "Lunar with a poor certainty still overrode the better account, or if it blended, it occurred improperly and moved the account unreasonably."** Confirmed. The
lunar gave 5° 23' W, "which he would trust within 25 miles"; the account took that longitude
outright, and its doubt east and west went from 0.8 mile to 12. Two things the owner should
know:

- *This was never in 37d.* The owner told the officer it "was supposed to be fixed in this
  version". 37d's second pass guarded one thing only, the estimated distance after a
  bearing. The lunar and the noon latitude still follow the older rule (an observation
  replaces the account once she has run two miles since the last one), and that rule was
  kept back for 37e, where it became the first item.
- *The swing was real, and ended worse than it began.* Before the lunar the account was 2.3
  miles out, with a stated doubt of 0.8. The lunar, by luck, was only 1.8 miles out. Twenty
  seconds later a bearing of Ushant light laid its estimated distance down, because the
  lunar had just made the account look twelve miles doubtful, and left the account 4.2 miles
  out. Part of that second error is a fault of its own: with twelve miles of doubt the
  bearing was worked in a form that is sound only while the doubt is small beside the
  distance to the mark. The builder should guard that form whatever rule is chosen.

The same rule failed the other way at noon on the 16th. The sight gave 48° 07' N and was
right; the account said 48° 13' N and was 3.8 miles wrong; and the sight was all but
ignored. The rule counts her run through the water since the last observation of any kind,
and the lead, cast every glass, kept setting that back to nothing while the tide carried her
those miles. So one rule let a poor lunar overrule the account and a good latitude be
overruled by it. The rule that replaced it follows.

That game's officer made findings of its own on the reckoning. Each is checked in H6: most
were right as said, and three were right with another cause (the doubt that seemed to grow
with the drift in fog, the bearing that cut the doubt and moved nothing, and the account
that sat on the Mingan).

#### What the review proposed from game 9, and what the owner ruled (7 October)

**The account's rule, stated once.** On 37d there were three rules for when an observation is
believed: the two-mile run (sights, soundings, plain bearings), the second pass's guard (a
bearing's distance), and outright replacement (a fix). Game 9 showed each failing. One
rule would serve all of them:

1. An observation is weighed against the account by their two doubts.
2. When the two disagree by more than their doubts together allow, the account is plainly
   out, and the observation is taken; its doubt becomes the account's in that direction.
3. The master's doubt grows by the hour whether she has way or not, by an amount that fits
   the streams where she is, and the same observation taken again does not narrow it again.
4. A fix chooses the marks that give the tightest fix, counts the compass's shared error in
   its "good to", and at anchor a poorer fix does not move the account.

Under it the lunar of the 15th would have moved the account a cable or two at most and not
blown its doubt up; the noon latitude of the 16th would have been taken; and the casts of
the lead would not have talked the master into certainty.

**One choice in it that is the owner's.** How does the master's doubt know the tides run
hard off Ushant? Three ways, which can be combined:

- (a) The doubt grows faster where the charted streams are stronger. Simple, and what a
  master knew from his sailing directions. It uses the strength of the true stream, never
  its direction. **This is the one recommended for now.**
- (b) The master works the tide into his reckoning himself where his books give it, which
  makes the account truer and not merely humbler. More work; a good candidate for the
  milestone that gives the master more of a mind.
- (c) It stays the captain's to order (`allow two knots of set to the westward`). This
  exists; it wants a lesson in the primer whichever of the others is chosen.

**The owner's ruling, 2026-10-07: (b), and now.** "The master should work the tide into the
reckoning himself ... by the same method the master currently works up the reckoning, he
should work the tide into it as the books give it." He asked first whether the master is
the station a model holds. What bears on the ruling (lead):

- *The master is not the model's station.* He is the sailor at the ship's post of master
  (Mr Pascoe in game 9): a simulated person with a skill and errors of his own, the same
  man whether the captain is the owner or a model. The officer's station stands in the
  place of the lieutenant or the mate (Mr Pearce), and its domain leaves "the reckoning,
  the sights and the course shaped" as "the master's for the captain".
- *The game's own study reached the same place, and half of it is built.*
  `docs/design/Tides1805.md`, section 2, from Bowditch 1802: the set is "worked in the
  traverse table as one more course", so "the master's estimate of the tide's set was ... an
  entry in the day's traverse, and its error an error in the reckoning". The master already
  works the hour of high water from his epitome and the almanac by Moore's rule, up to an
  hour wrong, for the reading `the tide by the almanac`. The entry in the traverse was never
  built: he carries no tide unless the captain orders one.
- *What it would be, proposed for the brief.* Each time he steps the account, whether she is
  under way, hove to or becalmed, he adds the tide as one more course and distance: the
  hour of tide from his epitome; the set and the rate from what the directions say of the
  waters his **account** puts her in; springs or neaps by the moon's age. His errors are
  then the period's own: the hour, the waters he believes she is in, and the book's round
  figure for the rate. Nothing in it reads the world's tide.
- *His doubt still grows*, by what the books cannot tell him: less than today's error where
  he has a table, more where he has none. So a modest form of (a) stays.
- *He says what he allows*, at noon and in the reading of the reckoning, so that the
  captain can see it and overrule it. `allow ... knots of set` stays the captain's
  override, and wants words that hand the tide back to the master.

Two things the ruling left for the owner, both since ruled (7 October):

1. What the books give where the study found no period source: the Fromveur, the Chenal du
   Four, and the timing of the stream in the Goulet. Proposed: the directions' plain
   statement of the set to the nearest point and the spring rate to the half knot, marked
   as judgement in the data as the truth's own figures there already are. **Ruled: as
   proposed.**
2. Whether a shaped course should allow for the tide he reckons ("NE by N, to make good
   NE"). Proposed: yes, in the same package. A course shaped for a point with no allowance
   is what set the merchant passage on the Mingan in 37d's first pass, and the period
   shaped its courses so. **Ruled:** "shape a course should by default steer to make good,
   by the master's reckoning." And his own `allow ... knots of set` "replaces when used
   until handed back".

#### What 37e built (7 October)

By the changes file. Its brief is fourteen items.

- **One rule for believing an observation.** Every observation (a noon latitude, a lunar, a
  time sight, a cast of the lead, a bearing, a fix) is treated the same way. The master sets
  his doubt of his account beside his doubt of the observation and does one of three
  things: **weighs** the two (the account moves toward the observation by as much as it is
  the more doubtful), **takes** the observation outright when the two are further apart
  than their doubts together allow, or **keeps** the account when the weighing would move it
  less than half a cable. The log line says which, and by how much. Game 9's lunar now moves
  the account under two cables; game 9's noon is taken; a poor fix no longer moves a good
  account. The audit saw both kinds of line in the log of the naval cruise as it sailed
  her: "the reckoning was out by it; laid down by the observation" and "the account moved a
  mile to the NE by N".
- **The same thing seen again tells him nothing new.** A second bearing of the same mark
  from the same place, a second cast on the same ground, a second fix by the same marks no
  longer make him surer. Game 9's eight casts over flat sand off Ar Men now narrow
  nothing.
- **His doubt is honest about the hours she has no way.** Hove to or becalmed, the account
  and its doubt used to stand still while the tide carried her. Now the clock runs on: hove
  to he reckons her drift by eye, becalmed the tide carries the account, and his doubt grows
  by the hour in both. Only at anchor does the account stand still. His words say the doubt
  as it lies when it is long and thin: "within three miles NE and SW, nor a mile
  across".
- **A fix takes the near marks.** Left to himself the master takes the marks that leave him
  the least doubt, which puts a headland inside a mile before a town five miles off. In the
  Goulet he takes Petit Minou, Camaret and Portzic, and not Brest and Conquet. A fix is
  weighed as any observation is, and no longer sets the account outright. The audit calls
  this item **partly built**: the choice of marks, the compass's shared error and the
  weighing are all in, and a fix whose marks lie on one hand still claims too much, by the
  builder's own note and by game 10.
- **The master works the tide himself**, by the owner's ruling. He reckons the stream from
  his own books (the hour of high water from his epitome, the moon's age from his almanac,
  and what his sailing directions say of the water his account puts her in) and carries it
  into the account every quarter of an hour. He never sees the sea's own tide, so he can be
  an hour out in his timing and he uses round figures; that difference is still the game.
  The log says when his tide turns and when he believes she has passed into other
  waters.
- **`allow ... knots of set` replaces the master's tide** until the captain hands it back
  with the new order `allow the tide by the book`. `allow no set` tells him to allow
  nothing. The reading `the reckoning` says what tide is allowed and whose it is.
- **A shaped course makes good.** `shape a course for <place>` orders the course to steer
  so that she makes the line good against the tide being allowed, and says both: "Shaped a
  course for the Goulet: NE by account, ten miles. Allowing the flood, a knot and a half to
  the E by N, steer NE by N to make it good; the allowance holds till the tide turns, about
  half past four." It is worked once; the master does not alter the helm when the tide
  turns. It also says when the line crosses the land or passes close along a shore, which a
  course shaped for Brest from off Roscoff did not in game 9.
- **The primer** teaches the rule in a seaman's words, and gains the two things game 9
  showed nobody knew: `observe an amplitude` to correct the compass before a landfall, and
  the captain's own allowance for a set.
- **The scenario books** were tuned for a true account: on the merchant passage the fix is
  taken again after the bearing in pilot water, and she passes the Mingan 1.9 cables to the
  north.

**How well it works, measured by the builder.** The same three recorded passages were
sailed before and after, with the account's distance from the truth and the master's own
doubt sampled every half hour. The audit did not measure these again, and found that
nobody has measured them since 37f moved the passages.

| | The merchant, before | after | The frigate, before | after | The schooner, before | after |
|---|---|---|---|---|---|---|
| median error, miles | 0.35 | 0.41 | 4.49 | 1.21 | 2.18 | 0.97 |
| time more than three miles out | 18% | 18% | 53% | 26% | 47% | 26% |
| samples where the error was more than twice his stated doubt | 35% | 18% | 62% | 6% | 53% | none |

Three of the four things the brief asked of these figures were **not fully met**, and the
changes file says so:

- The merchant's time more than three miles out was to be halved from 18 per cent; it is
  still 18 per cent, and her median is 0.41 mile against 0.35. All of it is the night
  crossing of the Channel, where her compass, her leeway and the tide each put her two to
  five miles out and no observation is to be had.
- The frigate was to be within a mile and a half of the truth inside half an hour of
  raising the land; she is 2.4 miles out for thirty minutes and 1.25 at thirty-five (before:
  4.2 to 5.4 miles for thirty-five minutes).
- The master was to be more than twice wrong about his own doubt in no more than one sample
  in ten. The frigate (6 per cent) and the schooner (none) meet it. The merchant does not:
  18 per cent, down from 35. Seven of her thirteen bad samples are at anchor in the Bay of
  Brest, where fixes every five minutes by three marks all on one hand leave him believing
  himself good to a cable when he is three cables out.

The fourth was met: the brig, hove to for six hours of a spring ebb in the Iroise, drifts
13.6 miles and her account ends two miles from her, inside twice the master's doubt
throughout. Before, the account stayed where she was brought to.

**Found and mended on the way.** Three things in the package's own new code let the mere
asking of a reading change later play by a few yards, so that a game with the chart open
was not quite the game replayed without it. All three were mended, and a test sails two
ships, one asked and one not, and compares them; the lead added a test of its own to the
same end (F4). A cast of the lead off a steep shore could also be matched to a place two
miles away and the account laid down there; it is now kept where the chart about the
account already answers the cast.

**What 37e left undone**, by its changes file:

- The three figures above.
- The two lost beats of the recorded passages (F4; G10 for the schooner's pilot, part L for
  the cruise).
- **At anchor in the Bay of Brest the master is surer than he should be.** Found late; not
  mended.
- **A wrong chronometer can displace a good account.** On the cruise, hove to off Plymouth
  with the land in sight, a longitude by a chronometer that was 7.6 miles out (the master
  said he would trust it within five) is far enough from the account to be taken, and the
  account is wrong for half an hour until the next bearing of the land takes it back. This
  is the one rule doing what the brief says, on an observation whose own stated doubt is too
  small. The cure is in how far the master trusts his chronometer, which lives in a file the
  package was not given. The audit found it still so: on its own run of the cruise, at 09:00
  on the 12th (tick 10800), the first time sight is "laid down by the observation" and
  moves the account more than two leagues.
- **The number in the one rule is two where the brief said three.** With three, game 9's
  own noon sight is not taken, and the brief's test requires that it is. The audit adds
  that the number is doing two jobs: it is the rule that took the cast a mile off in game
  10, and that lays the cruise's account on a chronometer more than five miles out (N,
  C8).
- **In the open Channel the master's tide is a rough allowance**: his high water by Moore's
  rule is an hour to an hour and three quarters early in the days of these passages, and
  the only period statement of the set is "north-east", twenty degrees from the stream the
  world runs.
- **Spec truth 59** says a cast "moves the reckoning onto the chart's contour". By the one
  rule a cast is weighed and comes within a fathom of it. The test says so; the truth's
  sentence is left for the lead. The audit found the sentence still there, at line 742 of
  `docs/TechnicalSpec-M5.md`.

#### In play: game 10, on 37e (7 to 8 October)

- **Fixes near land were very good.** `take a fix` chose three marks every time. On the run
  in, from 02:11 to the cast at 04:08, the account's median error was 0.07 of a mile; seven
  of thirteen fixes were weighed and kept ("the fix the poorer figure; the account kept,
  within a cable of it").
- **The doubt is honest now.** Over the whole game the truth lay within twice the master's
  doubt 92 per cent of the time, and through the fog from the Lizard to Scilly all of the
  time, the error 1.2 to 1.8 miles against a doubt of four. In game 9, without observations,
  the doubt was about a tenth of the error.
- **The master's tide is in the reckoning** and is said: 21 lines, and a shaped course that
  names its allowance, how long it holds and when she cannot lie it ("Allowing the ebb, a
  quarter of a knot to the SSW, steer SE to make it good ... the allowance holds till the
  tide turns, about half past eleven at night ... lying too near the wind to be laid, she is
  kept full and by on the larboard tack").
- **A bearing with its distance by estimation did its work at the landfall**: Peninnis Head
  at 19:53 on the 13th took the error from 2.1 miles to half a mile.
- **The cast**, as in the owner's note below.
- **The account is wrong when she stands off and on.** Between workings the account is run
  on at the log's rate along the average of her headings since the last one
  (`reckoning.py`, `_working`). Boards on opposite tacks ought nearly to cancel, and by this
  they do not. From 00:10 to 01:53 on the 14th, standing off and on and then hove to at one
  to two knots, the error grew from a quarter of a mile to 2.2 miles. The doubt grew too, to
  a mile and a quarter, which is what set off the owner's standing order "Bearings"; one
  bearing of St Agnes light brought the error back to six cables. The recorded passages
  sail long boards and never showed it.
- **A fix whose marks lie on one hand still claims too much**: the fix off the Lizard at
  12:29 on the 12th said "good to five cables" and was 1.3 miles out. This is on the
  follow-up list already.

**The owner's note 2 on game 10: "Single stray sounding during a sudden fog bank while entering St Mary's caused a jump
in the reckoning by a mile which was totally unsound and force me to anchor instead of
continuing by the fairly fresh reckoning I had."**

Right, and measured. At 03:59 a fix on three marks left the account a hundredth of a mile
from the truth. Fog came down at 04:00. A cast at 04:06 was kept. The cast at 04:08, "By the
deep nine; loose sand, not very tenacious. The reckoning was out by it; laid down by the
cast: moved a mile to the N", left the account 0.99 of a mile from the truth, with a stated
doubt of a quarter of a mile. It stayed a mile out for four hours, until the fog lifted and
a fix at 08:00 moved it back.

It happened again at the same place on the way out, in clear weather, at 16:56: the account
a hundredth of a mile out before the cast and a mile out after it, and put right by a fix
little more than a minute later.

The cause is the tide's height, and then the rule.

- The lead reads the water there is. The master takes off an allowance for the tide and
  matches what is left to his chart. His allowance is a flat three metres, the mean level:
  the code still says he "does not know the state of" the tide. The true tide was 4.7
  metres, near high water of a seventeen-foot tide, which the pilot had told him of that
  evening, and whose turn the master himself names when a course is shaped.
- So the cast read nearly a fathom more than his chart showed at his own, correct, position,
  and, by the code's own test, more than it showed anywhere within half a mile of it.
- The match then looks as far as five miles for the nearest ground of that depth, whatever
  his doubt, and found some a mile to the north.
- The one rule of 37e then took it, because a mile is more than twice his doubt and the
  cast's together.

Two things are wrong. He should allow the tide's height by his book, as since 37e he allows
its stream. And a single cast should never move an account further than the account's own
doubt: where no ground within his doubt answers the cast, the cast does not agree with the
account, and the line should say so and keep the account.

The second of these is the lead's own doing. The brief of 37e made one rule for every
observation, and the rule treats a cast that disagrees strongly as it treats a fix. A fix
says where she is. A cast says only that the bottom is not what was expected.

#### What is left

**Proposed** after game 10, amending 37e, and waiting on the owner (part K). **Not
built**, which the audit found too. It did not check in the code the cause the review
gives for the cast's mile, the tide's height. Its advice is that the second of these, a
cast that never moves the account beyond the account's own doubt, be made before the next
game near land in thick weather: "It is the one fault of the week that made a sound
position unsound in the owner's hands, twice."

1. The master allows the tide's height for the lead by his book.
2. A cast never moves the account beyond the account's own doubt. He looks for the cast's
   ground within his doubt and no further; where none answers, the line says the cast does
   not agree, and the account is kept.
3. The account is worked at every tack, wear, heave-to and large alteration of course, so
   that each board is laid down by itself.
4. A fix's doubt when its marks lie on one hand (already listed).

Also open:

- What 37e left undone, above. Two of those items are marked for the lead: the
  chronometer's trust, and truth 59's sentence. The number two in place of three is stated
  and has not been ruled on. Of the rest, the audit did not check the three figures, the
  master's sureness at anchor in the Bay of Brest, or the master's tide in the open
  Channel.
- **The danger list** is still drawn from the account in whole miles, as far as the changes
  file says: no package names it, and the audit's ledger has no row for it. The model's
  point that it should come from the best fix was found to hold (H2).
- **The dead reckoning's smaller faults** from the first review: a merchantman's log hove
  two-hourly with the account run on at the last cast; "the distance run since noon"
  multiplying at anchor; every scenario opening with the account a mile out. 37e's brief
  asked that her way be judged by eye after she fills away, weighs or comes out of a calm,
  until the log is next hove, and that the run since noon take the drift (its item 4). The
  changes file does not name these. The audit found item 4 **built**, by tests whose names
  say that hove to the master reckons her drift and the run since noon takes it, that after
  she fills away her way is judged by eye until the log is next hove, and that the doubt
  grows hove to and becalmed and not at anchor. It names no test of the run since noon at
  anchor, and the opening mile is in no package.
- **`the port` and `the depth of water`** (G4).
- **A reckoning of the officer's own**, kept beside the master's (G19). **Not built.**
- Bearings and fixes are the officer's own since 37g (G11). **Built.**

### G4. Three readings that give the true position away

- **`the port`** is computed from `world.position`, which that property's own docstring calls
  "the truth, which no reading gives" (`ports.py:976-1018`; `core/world.py:538`). It prints
  the true bearing and distance of the port's nearest road to a tenth of a mile, and beyond
  the pilot's cruising ground the true distance in whole miles. It is in every sample a model
  receives.
- **`the depth of water`** is the chart's depth at the true position, with no cast
  (`api/readings.py:557-566`). Standing orders gate on it and print it. A cast of the lead
  less this reading is the height of the tide, which the spec says is never read out.
- **A bearing of a sail** moves the account onto a line through her true position
  (`reckoning.py:1394-1400`). On the *Harpy* a bearing of the pilot boat moved the account
  10.13 miles (139,671), and the handover note says "fixed by a bearing of the pilots' boat".

The officers found the first two and steered by them: "the readings put Roscoff harbour SW,
7.9 miles, and that can't come from the reckoning ... So the game seems to know where we
truly are" (*Harpy*, 139,853); "I'm treating it as a sounding machine" (*Speedwell*,
547,065). So the game gives exact truth through three side doors while withholding the coarse
things a man on deck would see. In fog on the cutter one sentence set a true "Roscoff harbour
SW by S 1.6 miles" beside an account's "the Lavandière SE by S 4 miles", six and a half miles
apart (game 7, 112,487). The true distance and bearing of every landmark in sight also go to
the browser in the snapshot, though nothing shows them.

**What has been done.**

- **A bearing of a sail** moves nothing now. It is given in words and data as before.
  **Built**, 37d.
- **`the port` and `the depth of water`** still give the true figures. This is on purpose.
  The first review said that the change must come last, because those two readings were the
  only true numbers an officer had near land; 37d's brief kept them until the owner had
  played it, and the plan keeps them for the last step, after he has played 37e to 37g.
  **Not built.** The audit asked both readings and found that both answer from her true
  place.
- A standing order's condition on the depth reads that same reading (G9), so it stands as
  it was with it.
- The true distance and bearing of every landmark in sight, sent to the browser in the
  snapshot though nothing shows them: no package names it, and the audit's ledger has no
  row for it.

**Two things built since were held to the same rule.** The master's tide of 37e is worked
from his own books and from where his account puts her; the brief required a proof that no
line of it reads the world's tide or the ship's true place, and the builder's report was to
say so; the audit found that the rule holds, by its test. And the review of game 9 warned that a chart in words, if one is built, must be
drawn from the account and not from the truth, "or it becomes a fourth reading that gives
the position away" (G2). The pilot's warnings, when 37h is written, may be drawn from the
true chart by the owner's ruling: he is a carrier of that knowledge, as the design asks,
where a reading is not (G10).

### G5. The wind near land, and the fog

#### What the first review found

**The sea breeze flips direction every few yards** (lead, in the code; measured by a
reader). On a summer day between 10:00 and 20:00, within 15 km of a coast and in fine
weather, a sea breeze of up to ten knots is added to the wind (`weather.py:1234-1281`). Its
direction is "the bearing to the nearest coast", which the chart takes from a distance field
stored in whole cells, differenced one cell either way with no interpolation, and set to due
north when both differences are nought (`chart.py:601-625`; `tools/build_charts.py:1329`).
So the breeze points in one of a handful of fixed directions that change from cell to cell,
and a cell is 15 metres in a harbour patch.

| Track | How the bearing to "the nearest coast" behaves |
|---|---|
| The *Harpy*, north-east from her 13:28 fix on 19 June, 2.5 km | Changed 125 times, once every 20 metres; largest jump 57° |
| The *Speedwell* in the mouth of St Mary's Sound, 2.5 km | Changed 201 times, once every 12 metres; largest jump 180° |
| Across the road of the Isle of Bas, 300 m | Due north by default at all 31 samples, with land on both hands |

It fits the logs. Every flood of wind-shift lines is in those hours and in fine or hazy
weather; none is at night. Each begins when the ship begins to move: the *Harpy* had four
shift lines in three hours at anchor on the 19th, began to heave in at 12:00, and the
flipping began at 12:06. The lines alternate between two states, each with its own strength,
as a vector sum does when one term flips between two directions. The officers saw it: "The
wind is flipping between E by N and SE every few seconds" (*Harpy*, 635,868); "the true wind
went from W through to SE by S and back" (*Speedwell*, 557,585).

It cost something. The *Harpy* was taken aback three times closing Penlee. Two of the
*Speedwell*'s tacks failed at Scilly and she was taken aback. The cutters met it off Penlee
(43 lines in nineteen minutes) and off Roscoff (31 in 44 minutes at eight to eleven knots).

No test caught it because every recorded gate run pins its wind by a script. The free
scenarios written for this playtest were the first in which the weather systems drove the
wind beside a coast on a summer afternoon. Mending it moves none of the recorded digests.

**Checked against the game's own weather** (lead). The *Harpy*'s save of tick 602,100 was
loaded from its checkpoint and run on with the brig left at anchor, so that the weather was
the game's own for 19 June. From 12:27 to 13:50 the surface wind was then sampled each second
along a line run north-east at four knots from her anchorage, about the way she stood in:

| | Turns of two points or more, second to second | Compass points visited | Wind |
|---|---|---|---|
| Moving, the breeze as built | 386 (largest 169°) | 13 | 4.8 to 13.1 knots |
| Moving, the breeze set to nothing | none | 2 | 3.4 to 4.1 knots |
| At anchor, the breeze as built | none | 2 | 6.6 to 8.8 knots |

The sea breeze stood at eight to nine knots over a gradient wind of under four, under a high,
in haze. So most of the wind she felt that afternoon was the breeze, and its direction
changed whenever she moved. The line is not her exact track, which no save holds; the
weather and the breeze's strength are the game's own for those minutes.

CHANGES-m5c-b puts the swing in "the base wind the weather systems give ... near a col or a
light-gradient area". The gradient was slack, but the swing is the breeze.

**Light airs at sea are honest weather.** A slack gradient gives light and variable airs. The
ship should feel them; only the log and the `a wind shift` event should stop reporting them
(G6).

**Fog changes on the four-hour bell**, to the second, in fifteen changes of sixteen on the
*Harpy*.

The first review recommended taking the sea breeze's direction from the coast's trend over
a kilometre or two, with no breeze where the field is flat (I2, item 7), and pushed back on
the model's note that a minimum wind strength "would finish it off" in the log: it would
have left the floods at Scilly and off Roscoff, which came in a breeze (J1, item 5).

#### What was built: 37d (6 October)

**The sea breeze blows steadily from the sea.** By the brief, its direction is the coast's
trend over a baseline of some kilometres, and its strength is scaled by how steeply the
chart's field of distance from the shore rises there, so that in a channel, in a sound
among islands or in a harbour ringed by land, where that field is flat, there is little or
none. By the changes file: off Penlee on the
*Harpy*'s own afternoon the wind turned two points or more 386 times in 83 minutes as she
moved; now not once. No recorded passage moved for it.

#### In play

**The wind.** Nothing like the *Harpy*'s afternoon off Penlee came back: 50 wind-shift lines
in five days against game 2's 363 in eight. Most of the 50 are of another kind (G6).

In game 10, on the build with 37f's floor on the wind-shift line as well, there were 16
wind-shift lines in 63 hours. No flood of them came back in either game.

#### The fog

The first review found that fog changes on the four-hour bell (above). Game 9:

**Fog on the stroke of eight bells.** Seven spells of fog in five days, each beginning and
ending exactly at eight bells and lasting four hours or eight; about a quarter of the game.
Fog is common off Ushant in summer, but fog that keeps the ship's bells is the weather
model's four-hour step showing. **Later**, with the weather's polish.

Game 10: six spells of fog, 23 hours of the 63. Five of the six came down on the stroke of
eight bells and five lifted on it. **Not built**; it is **later**, with the weather's
polish.

### G6. The log's noise

#### What the first review found

| Notable or urgent lines | *Harpy* (old rules) | *Speedwell* (m5c-b) |
|---|---|---|
| "Taken aback", urgent | 31 | 5 |
| "Her sails aback ...", notable | none | 96 |
| Per-sail "taken aback" | 298 | 320 |
| Wind shift | 363 | 69 |
| Soundings, of which "No bottom at twenty fathoms" | 376, 163 | 380, 152 |
| All notable lines | 2,124 | 1,557 |

**Taken aback under the old rule.** Of the *Harpy*'s 31 urgent lines, 21 came with nothing
to lose: eight at anchor or moored, twelve in a calm just after "Hove the log: no way", one
at three quarters of a knot. Five were wanted. Thirty of the 31 eased the owner's clock to
1x; 25 woke the officer, and at least twelve of those were answered with only a fresh
stand-by. The alarm steered the ship: she carried no square sail for eighteen hours on
16 June, and the spanker was taken in at anchor "since the 'taken aback' urgent fires on it
alone" (576,750). The opposite case is silent: a ship hove to that fills and sails off.

**The per-sail lines** have no rule at all: 92 in one hour on the *Harpy*, and sails backed
on purpose (heaving to, a tack) are logged in the same words.

**The wind shift.** On the *Harpy* 307 of the 363 lines fall in two floods: 42 in 65
minutes leaving Roscoff, and 265 in 104 minutes before the grounding, stopping one second
after she struck. The other 56 lines in eight days were never spam. The floods have a cause
in the weather (G5).

**Soundings.** Every cast is notable, a no-bottom cast included. They were a quarter of all
the *Speedwell*'s notable lines.

**Standing orders that have nothing to do reject themselves each time they fire.** Of 545
refused orders in the six games with a model, 322 came from standing orders, 131 from the
captain and 92 from the officer. The *Speedwell* logged 99 "Nothing done" lines from two
rules; game 7 logged 145 rejected "Bearings"; game 1 logged 54 refused anchorings at anchor.

**One `trim sails` is about fifteen lines, three of them notable**, and every one says the
watch is too few: 437 such lines on the *Harpy*. In game 1, with no model, 168 of 417
notable lines are trim chatter and 116 are casts at anchor.

**Severities that are the wrong way round.** Notable: every no-bottom cast, "not hands
enough", each sail backed on purpose. Only notable: "The best bower is dragging". Routine: a
pilot's hail, "Hove short", a stranger's colours, "Ushant bearing N, distant six miles", and
anything the officer says with `say` (an `answer` is notable). The driver's own "Compression
eased" line once woke a stand-by as a notable event (*Harpy*, 357,785).

#### 37c in play (m5c-b, games 2 and 4)

37c was m5c-b's change to two of these lines (F1). What play showed of it:

**Taken aback.** The urgency rule did its work. In six and a half days the *Speedwell* logged
five urgent lines, four of them real, against the *Harpy*'s 31 under the old rule, 21 of
which came with nothing to lose (above). What remained:

- The notable "Her sails aback; she had no way on to lose" came **92 times**, 90 of them in
  one twenty-hour calm, a median of ten minutes apart. A minute clear is the wrong key in a
  calm: nothing has changed in a minute. Re-arm when she next has way on, or wind.
- The per-sail "taken aback" lines, which 37c leaves alone, came **320 times**, 216 of them
  in that calm. Together that was two thirds of the notable lines of those two days. They
  buried the officer's handover note beyond `read_log`'s reach (tick 398,711).
- One flag serves both severities, so a notable line can mask a later urgent one until she
  has been a minute clear. And urgency is read from one instant's apparent wind: an urgent
  line was logged in "light airs" at tick 203,621.
- Sails backed on purpose (heaving to, a tack) still log as "taken aback".

**The wind shift.** Far better in a steady breeze: nine lines in the *Speedwell*'s first 31
hours, and four in the eighteen hours of her run to Scilly. But of her 69 lines, 33 were in
light airs or calm, among them
"Wind veered to WNW, calm." The direction of a mean wind of one knot means nothing. The
minute's hold does little, since a ten-minute mean drifts rather than flicks; the shortest
gap between lines was 76 seconds. A floor on the mean speed and a steadiness test, with
"light and variable" said once, would remove them.

It is not only light airs. The *Speedwell* logged 23 shifts in three and a half hours of
gentle to moderate breeze among the Scilly Isles, and the m5c games show the same clustering
off particular coasts: 265 lines in under two hours off Plymouth before the *Harpy* struck,
43 in nineteen minutes off Penlee, 42 in 65 minutes and 31 in 44 minutes off Roscoff. That is
the sea breeze changing direction as the ship moves (G5). No rule in the log can cure it,
and CHANGES says rightly that 37c does not touch it.

Three definitions of a wind shift still stand: the log's (two points on the mean), the
`a wind shift` event's (one point against the last sample), and the standing orders' (the
instant wind). On the *Speedwell* the trim rule fired 40 times, 12 of them near a log line.
CHANGES says the change "closes" the spec's open item 11; it narrows it.

The first review recommended five changes to the log (I4), and two changes of severity
near land (I2, item 13).

#### What was built

By the changes file:

- **37d.** A dragging anchor is urgent; the pilot's hails are notable.
- **37f, the wind shift.** No wind-shift line in airs too light to have a direction (under
  four knots by the ten-minute mean, which is where the log's own words pass from "light
  airs" to "a light breeze"). "Light and variable airs." is said once as it falls so, and
  the settled wind once when it comes again. A wind whose mean swings back and forth (it
  veers, backs and veers again within the hour) is said once to be unsteady, and its shifts
  are not logged until it has stood half an hour. A wind that turns once, as at a front, is
  logged as before. The event `a wind shift` keeps the same floor.
- **37f, aback.** In a calm "Her sails aback; she had no way on to lose" is said once,
  however long the calm, and again only when she has had way on her since. The urgent
  "Taken aback" has its own flag and is not kept back by it. Each sail's "taken aback" is
  said once an episode, and not at all for a sail laid aback by order: heaving to, a tack,
  `back the main topsail`.
- **37f, "could not".** "Could not set the jib: The jib is set already" and its like are a
  routine line in plain words ("The jib is set already.") and not a failed evolution.
- **37f, the lead and the standing orders.** A cast that finds no bottom is routine, and
  the event `a sounding` means bottom found. A standing order with nothing to do says so
  the first time and then once a watch for each reason, where the merchant passage said "in
  the Bay ... she is at anchor already" twenty-six times.
- **37f, the dragging line**: urgent once an episode (G8).
- **37g.** What the officer says is notable in the log, with the deck or without.

#### In play: game 9 (on 37d, before 37f)

**The log.**

- 31 of the 50 wind-shift lines came with under four knots of wind, and 18 of them in a calm
  at anchor ("Wind veered to S, calm."). In a calm the wind has no direction worth a notable
  line. The first review had asked for a floor on 37c's rule; this was the case for it.
- "Her sails aback; she had no way on to lose", ten times in three hours becalmed, each
  notable.
- 25 notable "could not" lines for things already done ("Could not set the jib: The jib is
  set already").

The same game logged 23 anchor-dragging lines, all urgent, 18 of them in eight hours in the
Goulet (G8).

#### In play: game 10 (on 37f and 37g)

- **Wind-shift lines: 16 in 63 hours**, against 50 in game 9's five days, 31 of them in
  under four knots of wind.
- **"Taken aback" was cried urgently eight times**, with no warning line before any of
  them. The lead checked each against her head, the wind and her way:
  - three came at the edge of squalls on the afternoon of the 12th, when the wind fell and
    headed her by 16 to 50 degrees within four minutes, and she lost most of her way each
    time (from 3.9 knots to 0.9, from 5.4 to 2.1, from 3.2 to 1.4). These were real. She
    was steering a compass course close-hauled with her square topsail set;
  - two came while sail was being made after weighing, with the wind abeam and her way
    rising. These are the alarm misreading sails not yet sheeted;
  - one followed a helm order the ship misread (G17);
  - one came in four knots of wind after the headsail sheets were eased;
  - one was the yards left aback by a heave-to belayed half done, and was right.

Two more things about the log came out of that game. The standing orders that could not
act said so 33 times, in routine lines (G9). And the samples sent to the officer have
grown, because a cast of the lead every five minutes by standing order is a notable line
each time, and so is every note the officer writes with its orders, 280 of them (G15).

#### What is left

- **Proposed** after game 10, amending 37f (part K): the alarm for being taken aback leaves
  sail that is still being made alone, and a lifting sail is said before she is aback.
  **Not built.**
- From the first review, in no package by the changes file, and with no row in the audit's
  ledger: one `trim sails` writing about fifteen lines, three of them notable, each saying
  the watch is too few; a cast that finds bottom being notable every time; "not hands
  enough" notable; and "Hove short", a stranger's colours and "Ushant bearing N, distant six
  miles" routine. The driver's own
  "Compression eased" line once woke a stand-by; since 37g a stand-by with the deck is
  broken by notable lines that speak of danger, kept as a list, and the changes file does
  not say what else still wakes one.
- **Three definitions of a wind shift** stood after 37c: the log's, the event's and the
  standing orders'. 37f gave the event the log's floor, which the audit found built. The
  changes file does not say that the three were made one, and the audit did not look.
- **The naval cruise's pinned passage holds two urgent "Taken aback" lines**, by the audit,
  at ticks 83957 and 91954. Both are real: each time a large alteration of course is given
  to the helm alone and her yards are left braced for the old tack (G7; M, 2.4). The
  cruise's test checks that she is never aground and never drags; it does not look for a
  ship taken aback, so the suite is content.

### G7. Lying to, getting under way, and the helm

#### What the first review found

**Hove to is not a state that holds.**

- The brig hove to goes through the wind: the helm is fixed a-lee and nothing is tended. For
  the pilot her backed main topsail "filled again" after 152 seconds (*Harpy*, 17,705).
- On 17 June she filled in a squall and sailed toward the land for an hour with no alert,
  the game still answering "She is hove to" (496,638 to 500,492).
- The hove-to flag survives anchoring, weighing and a tack. It refused a course to a ship
  under way for 23 minutes (212,708).
- `fill away` picks its own course: "braced full and steering S (185°)" with her head north
  (500,546). On the cutter "Filled away" was logged with her head in the wind and sternway on
  (game 5, 14,757).

- **`trim sails` fills a ship that is hove to**, four times in two games (*Harpy* 137,021,
  137,615; *Speedwell* 162,102, 193,303). `trim` has no hove-to check, though `steer` and
  `keep her full` do. She stays recorded as hove to, so `heave to` is then refused: "She is
  hove to already" (193,441). *Added 2026-10-06, from the owner:* the dialect has had the
  guard since package 33c. A rule ending `... and she is not hove to then trim sails` (or
  `and the manoeuvre in hand is not hove to`) sleeps from the moment the heave-to begins
  until she fills away (lead; `standing/rules.py:274-278`, and the project's own test,
  `tests/test_standing.py:1741-1810`). Neither the starter book's "trim on a shift" nor the
  officers' own trim rules carried it.

**`get under way` in a fore-and-aft vessel reports a cast that has not happened.** The cast
times out at seven minutes and the script says "She has paid off" regardless. All three
casts a schooner had to make timed out, two of them in the gate's own recorded merchant
passage. The mainsail is set flat before the anchor is out, the jib is sheeted to leeward,
and the helm is never tended. At Plymouth the *Speedwell* needed four orders by hand over
eleven minutes.

**A tack that has to wait fails in the words of a missed stay.** The *Speedwell*'s three
"she fell off on the ... tack" lines each share a tick with a cast of the lead and have no
"Ready about" before them. The tack waited behind the leadsman, failed a precondition, and
logged the one text it has for every failure. Her officer concluded "she has missed stays
twice today" and gave up tacking in the Sound.

**Sternway.** The note that the helm steers as if she had headway is not borne out: the
rudder and the helmsman both reverse (`hull.py:231-243`, `358-362`). What the log shows is
`steer ENE` taking the short way round, through the wind, with no way on.

**Small vessels speak the frigate's words**: "In studding sails, royals and topgallants; up
courses" on the cutter; "two of the young gentlemen" in a merchant schooner. Five of the
starter book's nine rules are refused on the cutter.

The first review listed these among its small faults (I5): the hove-to record cleared by
anchoring, weighing and tacking; the starter book's trim rule given the dialect's own
guard, and `trim sails` itself declining to brace a hove-to ship round; a hove-to ship that
fills and gathers way saying so, urgently; the fore-and-aft cast; and a tack that could not
begin saying why.

#### In play: game 9, on 37d (nothing yet built for it)

**The owner's note 6: "Brig still likes to come through the wind when hove to, the helm and sails need to try to keep her hove to properly on the tack she hove to on."** Confirmed, in four
heave-tos of seven:

| Hove to | Wind | What she did |
|---|---|---|
| 12 June 06:03 | 10 to 12 knots | Through the wind inside a minute; lay with it abaft the other beam |
| 13 June 00:20, 3.6 hours | 3 to 4 knots | Held her tack |
| 13 June 08:24, 4.9 hours | 5 to 11 knots | Held |
| 13 June 13:43, 2.1 hours | 11 to 22 knots | Held |
| 14 June 09:23, for the pilot | 8 knots | Through the wind in two minutes |
| 15 June 10:04 | 4 to 5 knots | Through the wind in six minutes |
| 15 June 10:29, 5.5 hours | 3 to 6 knots | Through the wind in twenty minutes, then lay steadily with it abaft the other beam |

The two quickest began with four and five knots of way still on her when the helm went
a-lee and "Hove to" was logged; the two on the 15th began at a knot and a half, as did one
that held. The lead did not trace the cause further. The officer's own reading, that she
gathers no sternway for the lee helm to work on, is in its report of 10:37 on the 15th. Two
things follow from the spin, both read in the code:

- `fill away` braces and steers for the tack she hove to on. After she has put herself
  about, that takes her back through the wind with every sail aback. It happened three
  times with the officer aboard; this is the officer's "fill away picks the wrong tack".
- The record that she is hove to outlives the anchor. She lay a-try before anchoring at
  Roscoff, and the next morning, anchor up, `steer` was refused four times ("She is hove
  to; fill away before giving her a course"), and `fill away` then turned her east into the
  road.

The owner's guard for a trim rule ("and the manoeuvre in hand is not hove to") was
in his book this game and worked.

**The owner's rulings for 37f (7 October).** From his note 6, the helm and the sails are to
keep her hove to on the tack she hove to on. `trim sails` declines while she is hove to.
And "Loose should remain as is": `loose` sets the sail, as `set` does. That game's officer
had ordered "Loose the topsails" meaning the period's loosing, both were sheeted home, the
main topsail aback, and an anchor dragged for it (H6).

#### What was built: 37f, part one (7 October)

By the changes file:

- **A ship hove to stays hove to, on the tack she hove to on.** Three things are different.
  Her way is taken off first: "Hove to" is not said until she lies four to seven points
  from the wind on her tack, has stopped swinging and has lost her way, and the line names
  the tack ("Hove to on the starboard tack, main topsail to the mast, helm a-lee."). She is
  then kept there: the watch tends the helm and the spanker and jib sheets, as Luce says a
  ship hove to is regulated, which costs it four hands and is said once a watch in a routine
  line. And if the weather forces her round all the same, the log says so once, urgently,
  and the record follows what she has done.
- **Measured by the builder.** From the like of the game's worst case (seven knots, the
  wind on the quarter) the brig used to be through the wind in the third minute; now she is
  hove to in under three minutes and lies five and a half points from the wind with a knot
  of way, and in six hours of a gusty, wandering breeze her head stays between five and a
  half and six points from it, with a knot of way or less. The frigate, the schooner and
  the cutter hold their tack the same way. The schooner and the cutter still forereach (up
  to two knots and a quarter, and a knot and a half): a fore-and-after hove to does, and
  they cannot be brought under a knot and a half.
- **`fill away` fills her on the tack she is on**, and says which.
- **`fill away and steer <course>`** fills her and gives the helm that course in one order,
  by a point or in degrees. A course that lies across the wind or too near it is not given
  her: she is kept full and by, and the line says why.
- **The record that she is hove to is cleared** when an anchor is let go, when she weighs,
  when she tacks or wears, and when she takes the ground. The Roscoff morning of game 9
  now goes: at anchor the manoeuvre in hand is none, and weighed, she takes a course at the
  first order.
- **`trim sails` hove to is refused**, with the cure in the words: "She is hove to; fill
  away before trimming, or brace a yard by name." A yard or a sheet worked by name is still
  taken. The starter book's two trimming routines, and the three in each of the merchant's
  and the cruise's books, carry the guard `and the manoeuvre in hand is not hove to`, so
  they sleep while she lies to and say nothing.
- **The fore-and-aft cast** (the brief's part two, item 13). A schooner or a cutter getting
  under way now casts as Luce's schooner does: her main boom steadied over to the side she
  is to cast toward, her jib's sheet to windward, her helm tended. On the merchant passage
  she casts in a minute and a half where she ran seven minutes to the timeout; and "She has
  paid off" is never said at a timeout for any ship. If she casts the wrong way the line
  says so, and if she will not cast at all the order fails in words.
- **Primer chapter 3** was to say in one plain sentence that `loose` sets a sail. The brief
  asked it; the changes file lists the chapter among those changed and does not quote the
  sentence. The audit found that primer 3 changed in 37f and did not read it against the
  brief; of `loose` itself it found no change and did not probe it.

The lead tried it from the owner's own game (F5): the brig of game 9, hove to from her
state at 17:39 on 14 June, settles five points from the wind with under a knot of headway
and holds it, and `fill away` then draws on the same tack.

#### In play: game 10, on 37f

- **Hove to, she held.** The second heave-to on the 12th held for fourteen minutes until
  `fill away and steer sse` took her off, as it should. Off the Sound on the 14th she lay
  hove to for about seventy minutes, some four points from the wind, forereaching at about a
  knot.
- **The first heave-to did not hold, and not for the old reason.** The officer was hauling
  down the foresail, at the pilot's hail, while the captain hove to; the heave-to backed
  that same foresail, said "Hove to", and she filled within a minute. The second, which
  backed the jib, held. A heave-to should back a sail that is set.

Eight urgent "taken aback" lines in that game are set out in G6. Three were real, at the
edge of squalls. One followed a helm order the ship misread: a course given with a half
point, which is steered to its last word (G17).

#### What is left

- **Proposed** after game 10 (part K): a heave-to backs a sail that is set. **Not
  built**, and not checked by the audit.
- **Left undone by 37f**, by its changes file: the fore-and-afters hove to make more than a
  knot and a half; and a course shaped with next to no way on her is worked for that way
  and can be a point out when she has gathered it. The frigate's book works round the
  second; the cure, if one is wanted, is in the reckoning. The audit checked neither.
- **A tack that could not begin** still fails in the words of a missed stay: 37f's brief
  leaves it, with the other small faults, until the owner has played 37e to 37g. **Not
  built.** The audit tried it: a tack ordered from off the wind was answered "Squared the
  yards; she fell off on the starboard tack, to try again or to wear".
- `get under way` accepted afloat and failing seven minutes later for want of the launch
  (G8), and small vessels speaking the frigate's words: in no package, and not in the
  audit's ledger.
- The note that with sternway the helm steers as if she had headway was **not borne out**,
  and nothing was built for it.
- **A large alteration of course given to the helm alone leaves a square-rigged ship's
  yards braced for the old tack.** This is the audit's finding, from sailing the naval
  cruise (M, 2.4), and it corrects what this edition first said here, on the word of 37f's
  builder: that the chase order takes the frigate through the wind with every sail aback
  and that making it wear her would cure it. She is not taken through the wind. When
  `give chase` or `shape a course for` orders a course 150 or 175 degrees round, and the
  shorter way to it is by the stern, the guard that would wear her does not fire, rightly
  by its own test; the plain order to steer is given; the helm takes her round with her
  yards still braced sharp up, nobody braces them, and she is caught aback with the wind
  on her quarter. It happens twice in the cruise as pinned. The code is the gate's own and
  is in no package. The audit warns that it is not only the book's: "a captain who types
  `steer NE` from SW by W will meet it." Whether it is mended before the cruise is played
  for the gate is among the things for the owner to decide (D2).
- **The chase order chooses the tack that leads away.** Also the audit's, and not noted
  before: when the course for a chase cannot be laid, the frigate is put close-hauled "on
  the tack she is on", which on the cruise was 102 degrees away from the chase where the
  other tack would have pointed within 33 degrees of her. The audit's own crude trial of
  choosing the nearer tack did not mend it, and it says that this is not a one-line
  mend.

### G8. The ground tackle, and going aground

#### What the first review found

**Anchoring.**

- **The anchor's depth is read in the wrong place** (lead; `core/world.py:581`). The ship's
  position is carried forward step by step; each anchor's depth is read at a point found by
  one jump from the scenario's origin by the whole voyage's displacement. On a sphere those
  drift apart: about 1.4 miles at Scilly, 740 metres at Cawsand, a kilometre along the
  gate's own merchant passage. Hence "let go in 37 fathoms" then "Brought up ... in seven";
  twelve and a half then six and a half in game 1; and the *Harpy*'s "in no water", where
  the misplaced point fell on land. It is not a missing number in the text. It also feeds
  the cable's holding: the *Harpy*'s dragging anchor "holds again" at a depth of nought.
- **Scope is five times the depth and every best bower carries 240 fathoms**, so the
  *Speedwell* veered 230 fathoms in 46. Only water deeper than a third of the cable is
  refused, and nothing warns.
- **`come to an anchor in twelve fathoms` takes twelve as the scope**; the primer says it is
  the depth to let go in.
- **`let go the anchor` takes in no sail and never logs "Brought up".** Six stand-bys on that
  event never fired, and the captain needed 67 minutes to be sure she rode (*Harpy*, 18
  June).
- **`heave in 70 fathoms` runs as `heave short`**: 163 fathoms came in.
- **Nothing checks depth against draught**, and no reading or paper gives the ship's
  draught. Two officers looked for it.
- **26 verbs are refused at anchor and aground** (`verbs.py:93-99`), among them `furl all
  sail`, `square the yards` and `loose sails to dry`. The primer's own example,
  `at aground then furl all sail`, is refused.

**Aground.**

- The kedge is refused ("she is aground"), and so are letting go, weighing, getting under
  way and mooring. What worked afloat was `heave short`, which hauls her up to her anchor.
- The leak is a rate and a level that write log lines and nothing else. It runs only while
  she is aground, and a gentler second strike lowers it. She sailed with 4 ft 10 in in her.
- `the well`: "The ship has no well to sound yet; that reading comes with the world."
  `man the pumps`: "did you mean 'demand'?" `send for the carpenter` brings him aft with
  nothing to say.
- The strike's speed is through the water, so the tide alone gave "half a knot" for the
  second.
- `get under way` was accepted afloat and failed seven minutes later because the launch was
  away selling brandy. The port read "at anchor in Plymouth, Cawsand Bay" while she lay
  aground a mile from it.

The first review recommended reading the anchor's place from the ship's own position (I2,
item 8), making "The best bower is dragging" urgent (I2, item 13), and, among the small
faults (I5), the anchor's orders, the verbs refused at anchor and aground, her draught in
the papers and a carpenter who reports the well. The well and the pumps it left for a
ruling (I6, item 9).

#### In play: game 9, on 37d

37d had mended the anchor's depth. The rest was as m5c had it. Three anchors were down in
the Goulet by the evening of 16 June, on poor ground, and the officer made a list of
ground-tackle faults. The review checked each against the log, a replay and trials on the
game's last checkpoint (H6), and found two of them to be other than they looked from the
deck:

| The officer says | What it is |
|---|---|
| "A veer goes past the number: 75 ran to 228, 180 to 240, 45 to 67" | Three things. `let go` veers five times the depth by itself: 128 fathoms in 26½, 67 in 13. So "veer to 75" and "veer to 45" found more out already and were refused, in clear words. And with an anchor named, "to" is lost: `veer the small bower to 100 fathoms` veered 100 **more**, and on the best bower, the one she rode by. Tried on the last checkpoint: `veer to 80` goes to 80; `veer the best bower to 80` goes to 148; `veer the small bower to 80` puts the best bower at 148 |
| "Anchors report dragging while the ship isn't moving; the slack one sets off the alarm" | In the Goulet the anchors did come home: the best bower two cables in seven hours, the small bower nearly two in eight, the sheet anchor half a cable in four. The ground there is "rock and mud", which the game counts as rock, holding about a third of what good ground holds. What misleads is the flag: it stays up five minutes after an anchor last moved, slack or not, and each relapse is a fresh urgent line. There were 18 in eight hours, each waking the officer and easing the clock |

A third was right as said: `weigh the small bower` weighs the anchor she rides by. Tried on
the last checkpoint, it weighed the best bower, and the name is dropped without a word. The
owner met it too, weighing at Roscoff on the 14th.

**The ground's words.** "Rock and mud" in the Goulet and "sand and rock" at Roscoff both
count as rock, the worst word in the note. Brest road has no bottom note at all, though the
pilot says mud. Small, and worth a look when the ground tackle is opened.

The review pushed back on the officer's list as written: two of its four items are not
faults of the kind it says, and the table in H6 is the list to build from (J2).

**The owner's ruling for 37f (7 October).** `let go` keeps veering the scope the depth
wants, says the figure, and takes a number.

#### What was built

By the changes file:

- **37d. An anchor's depth is read where the anchor lies**, not a mile off after a long
  run. By the brief, one function places a point of the plane from the ship's own position,
  for the anchors and for the weather's coast alike.
- **37d. A dragging anchor is urgent.**
- **37f. An anchor's name is honoured.** `veer`, `heave short`, `heave in` and `weigh` work
  the anchor you name. On a brig moored by the build's own orders (eighty-two fathoms on
  each bower): `veer the small bower to 90 fathoms` veers the small bower to ninety (before:
  it veered the best bower to 172); `veer the best bower to 90 fathoms` veers to ninety
  (before: ninety more, to 172); `weigh the small bower` weighs the small bower and leaves
  her riding by the best bower (before: it weighed the best bower). Where the ship cannot do
  it, the refusal names the anchor she rides by and what would.
- **37f. `heave in`** is a new order: `heave in to 70 fathoms`, `heave in 10 fathoms`,
  either with an anchor's name. `heave short` takes no number, and a number after it is
  answered with `heave in to`.
- **37f. `let go` says its scope and takes one.** The default stays five times the depth,
  and its first line says the figure: "Let go the best bower in 17 fathoms; veering to
  eighty-four fathoms, five times the depth." `let go the best bower and veer to 45 fathoms`
  (or `with 45 fathoms`) veers to that and no further, and
  `come to an anchor ... and veer to 45 fathoms` likewise.
- **37f. Three warnings as the anchor goes**, each notable and none a refusal: her swinging
  room ("With fifty-two fathoms out she will swing within a cable of the land to the NE by
  E."), a depth that wants more cable than she has bent, and the water at low water by the
  master's tide against her draught ("By the master's tide there will be two fathoms here
  at low water, and she draws 15 feet.").
- **37f. `come to an anchor in twelve fathoms`** means what the primer said: she stands on
  until the lead calls twelve fathoms and lets go there. **`let go the anchor` logs
  "Brought up"** when she is.
- **37f. The dragging line.** Urgent once, when an anchor begins to come home, with only
  the advice that is left to take. While it goes on, a notable line a quarter of an hour
  apart at most, with how far ("The best bower still coming home: a cable since it
  began."). "Holds again", with how far it came, when it has not moved for five minutes. An
  anchor whose cable is slack is no longer said to drag.
- **37f. The ground's words.** "Rock and mud" was held as bare rock; it now holds as the
  mean of the two, a little over half of good ground. Brest road had no note of its bottom
  and has one now (mud). Every port's road and anchorage has its note.
- **37f. In the Goulet**, the like of game 9's eight hours (eighteen urgent lines in the
  game, eight in the build's like state before): one urgent line and one "holds
  again".
- **37f. At anchor she is still a ship.** `furl all sail`, `square the yards`,
  `brace the yards square`, `loose sails to dry` and their like are taken at anchor and
  aground. The helm's orders and the manoeuvres still wait till she weighs.

The lead tried it from the owner's own game (F5): from her last state, moored in Brest
road, `veer the small bower to 80 fathoms` veers the small bower to eighty, where it had
put the best bower at 148.

#### In play: game 10, on 37f

- **The anchors answer to their names**, and `let go` says its scope.
- **An anchor left "aweigh" is stuck.** At 03:53 on the 14th the best bower was up to the
  bows when the owner belayed getting under way. Sixteen minutes later, in fog, with the
  account a mile out and the flood setting her, `let go the best bower`, `come to an
  anchor` and `drop anchor` were each refused with "the best bower is aweigh", and `weigh
  the best bower` with "no anchor is down". It could be let go only after `cat and fish the
  best bower`, which took another fourteen minutes. An anchor hanging at the bows is the one
  that can be let go soonest.
- **`Let go the sheet anchor` was accepted and failed four minutes later** ("no anchor
  aboard answers to 'sheet'"). The cutter carries a best bower, a small bower and a kedge;
  the order should be refused when it is given, with her anchors named.
- **Anchoring in deep water is uneven.** She anchored twice in 45 to 48 fathoms with nearly
  the whole cable out, and the officer's `let go the small bower` in the same water was
  refused as "no anchoring ground here: 44 fathoms and a half". Not traced.

At 03:30 on the 14th the officer, under the general authority, anchored her in the Sound as
the lead came down from 34 fathoms to 4; and twice she lay to an anchor in 45 to 48 fathoms
with nearly the whole cable out (E4).

#### What is left

- **Proposed** after game 10, amending 37f (part K): an anchor at the bows can be let go,
  and a belay of getting under way says where it has left the anchor; an anchor the ship
  does not carry is refused at the order; anchoring in forty fathoms is looked at. **Not
  built.**
- **The audit on the anchor left aweigh.** Game 10's finding stands as the log has it,
  above. The auditor's one trial did not reproduce it, because its belay came before the
  anchor was aweigh, and the ship was then simply at anchor. So the conditions in which an
  anchor is left aweigh and stuck are not yet pinned down.
- **The audit on the anchor she does not carry.** Game 10's finding is narrowed. With
  nothing in hand the cutter refuses `let go the sheet anchor` at once: "no anchor aboard
  answers to 'sheet'". It is accepted only when the hands are at other work: in the
  auditor's trial, while she was getting under way.
- **Left undone by 37f**, by its changes file: a dragging that relapses is still more than
  one urgent line. The brief says an anchor that has held five minutes "holds again", and
  that the next drag is then a new one. On bare rock in a tideway an anchor holds six
  minutes and comes home again, and each time is urgent: with the Goulet's ground forced to
  bare rock there are eight urgent lines in eight hours, as many as before. On the Goulet's
  own ground, as it is now read, there is one. If the owner would rather a relapse inside a
  quarter of an hour were the same dragging, it is a small change.
- **Her draught** is now said in the low-water warning. A place for it in the ship's papers
  or a reading, which two officers looked for, is in no package: **not built** as far as
  the audit found, which did not probe it.
- **`let go the anchor` takes in no sail.** The changes file does not say that this
  changed, and the audit's ledger has no row for it.
- **Aground.** The kedge worked, warping and towing are Milestone 8's by the gate. The leak
  that nothing reads, `the well`, the pumps and a carpenter with something to say wait on a
  ruling that has not been given (I6, item 9). The strike's speed taken through the water,
  and the port reading "at anchor" while she lies aground, are in no package. **Not
  built**; the audit found the carpenter and the well not built as far as it looked.
- **Orders to slip or cut a cable** are not written. The general grant's list of what
  cannot be undone is in place for them (G11).

### G9. Standing orders

#### What the first review found

Standing orders held the watch well in open water. On the *Harpy*'s first night "trim on a
shift" took the yards from sixty degrees to square with nobody sampled. Number-free forms
("every glass then take a bearing of the land") and the captain's event hooks
(`at the pilot asks to be put off then ask the officer ...`) both worked. What they lack is
knowing when to stop.

The first of the faults, `trim sails` filling a ship that is hove to, is in G7. The others:

- **In a calm** its only floor is half a metre a second of apparent wind. The *Speedwell*'s
  rule braced the yards six times in a one-knot night. The note's "all night" overstates it.
- **The event `a wind shift` fires at one point of the mean wind; the log's line needs two.**
  So the hands trim "by standing order" with no shift logged.
- **A trim is fixed at the moment of the order**, so `steer X; trim sails` trims to the old
  course. The cure exists and the gate's own books use it:
  `at steady on the course then trim sails`.
- **A condition on the depth reads the true charted depth** with no cast (G4).
- **A condition that can never be true is accepted without a word**: "the distance to the
  land is under 3 miles" (game 6, 11,665).
- **The grammar is strict about small things**: five refusals in thirteen seconds for a
  missing "is", and an apostrophe ends a quoted name.
- **A second cast of the lead is queued, never run beside the first.** "Not hands enough to
  heave lead" came with one, two and three lead rules in force, each time during a trim. The
  trim took the hands, not the third rule.

The log's side of it, standing orders that have nothing to do rejecting themselves at every
firing (322 of 545 refused orders in the six games with a model), is in G6. The owner's
note 16 asked for a `keep` prefix for continuous orders; the review pushed back, since the
dialect can already say it (J1, item 4).

#### In play: game 9

**The standing-order book.** The owner needed four tries to write 'Triangulate'. "The
distance to the land" was entered each time and then quietly held at every firing ("the
distance to the land is not on the chart"). A condition that names nothing the ship knows
should be refused when the rule is entered.

The owner's guard for a trim rule ("and the manoeuvre in hand is not hove to") was in his
book that game and worked. The officer found `the nearest land` in the library and wrote
two standing orders on it. A standing order met `trim sails` refused under one knot of wind
across the deck ten times (H6).

#### What was built

By the changes file:

- **37d.** The dialect takes `take a fix` (`every glass then take a fix`) and
  `the nearest land` as a condition, in half miles and miles and not yet in cables. The
  audit tried cables and was answered "'the nearest land' is compared in miles, not
  cables".
- **37e.** By its brief, the dialect takes the three orders that allow a tide as actions,
  and there is an event for the master's tide turning,
  `the turn of the tide by the reckoning`, which comes under way where the older events of
  the tide's turn come only at anchor. The changes file says that the log says when his
  tide turns, and under 37g that a wait for "the turn of the tide" under way is answered
  with that event's name.
- **37f.** The shipped books' trim rules carry the hove-to guard (G7). A standing order
  with nothing to do says so the first time and then once a watch for each reason (G6). **A
  standing order's place is checked when it is entered**: "the distance to the land" is
  refused at once, with the forms that serve ("the nearest land", or "the land is in
  sight"), and a name the chart nearly has is answered with that name. The audit notes of
  the "nothing to do" line that it is built for a condition that does not hold, and that
  an action the ship refuses is another matter.

#### In play: game 10

Of the standing orders' firings in 63 hours, 290 were taken and 33 refused. The lead was cast
222 times, 183 of them by the five-minute standing order. The officer needed six tries to
word a standing order before one was taken (G17).

- **A standing order's action is not read when it is given.** The officer's "the fix at the
  watch" was accepted with the action "take a fix as soon as a bearing can be taken", which
  the ship then read at each change of the watch as a mark of that name, and refused four
  times before the owner replaced it. 37f checks the condition at entry; the action wants
  the same.

**Standing orders that cannot act say so every time.** Thirty-three refusals, most of them
"Trim the Fore and Afts" while at anchor and "Bearings" or the fix at the watch with nothing
in sight. They are routine lines and do no harm, but the owner's condition "if the manoeuvre
in hand is not hove to" did not cover lying at anchor, and nothing told him so.

#### What is left

- **Proposed** after game 10 (part K): a standing order's action read when it is given.
  **Not built** in full. The audit narrows game 10's finding: the action's first word is
  read when the order is given, and no more. `then lett go the anker` is refused at entry;
  `then take a fix as soon as a bearing can be taken`,
  `then take a bearing of the moon made of cheese` and `then let go the sheet anchor` were
  all entered in the book.
- A guard that covers lying at anchor as well as lying to, or a word to the captain that
  his does not: raised by game 10 and in no package.
- **Left by 37g**, by its changes file: a standing order the officer writes under the
  captain's word stays in the book when that word ends; its orders are checked when it is
  entered and not again when it fires.
- From the first review, and in no package by the changes file: `trim` bracing the yards
  in a calm with only half a metre a second of apparent wind for a floor; a trim fixed at
  the moment of the order, for which the cure exists
  (`at steady on the course then trim sails`) and which the review asked to be shipped in
  the starter book; the grammar's strictness about a missing "is" and an apostrophe; and
  the dialect's want of cables. The audit read the starter book and found that it has no
  `at steady on the course` rule: **not built**. The others, cables aside, have no row in
  its ledger.
- **Stand by until x, or y, or z**, with the dialect's own conditions, needs design first
  (I7, item 3). **Not built.**

### G10. Pilots and other vessels

#### What the first review found

**The pilot is a person who speaks, and nothing else** (`ports.py`). "Took charge of her" is
a phrase in one log line. He does not steer, warn, refuse or fix her position. His one
mechanical effect is to supply the tack and the course *out* to `get under way`, which he did
for the inward-bound *Harpy*. The primer's chapter 12 calls him "the better answer" to
standing into danger. Across the games:

- **He cannot be asked for, accepted or refused.** `hail the pilot` is answered "did you mean
  'haul'?" (*Harpy*, 15,428). He boards outward-bound ships, and gives them the directions
  for coming in. The *Harpy* paid £22 to five pilots for no pilotage.
- **He was aboard for both the grounding and the near miss** and said nothing: 29 hours in
  the *Harpy*, through the strike, leaving as she stood off to save herself.
- **A ship that heaves to at his hail is not boarded.** His boat sails to a predicted meeting
  point and then lies to for ever, while boarding needs her within two cables of the ship
  (`ships.py:563-578`). The *Speedwell* waited 2 h 17 m and was boarded only by sailing down
  to the boat (192,540 to 200,760).
- **He leaves by geometry.** Once she is a mile beyond the outer road and opening, his gig is
  launched and cannot be recalled, and no pilot comes for six hours. A three-minute board to
  seaward cost the *Speedwell* hers (525,900).
- **His words have faults**: "where the breakwater now is" in 1805 (it was begun in 1812);
  "the flood" three hours before the game's own turn of the tide off Plymouth; his hail asks
  an anchored ship to "shorten sail". In game 1 the Brest pilot never leaves and is never
  paid.
- **His hails are routine lines**, so they wake nobody; on the cutter his request for sail
  to be shortened went unheard (game 7, 12,480).

Two of the model's notes do not hold: the "two cables" rule is one test for boarding and
leaving alike, and Mr Tozer boarded a ship stopped in irons, not one at four knots.

**Other vessels at a fixed distance** are the held estimate of G2, not ships circling.

#### The owner's answer (5 October), and what the review read into it

The question was:

*Taken or declined by an order now? And aboard: does he con, warn, or speak?*

**Answer.** For now an order accepts or declines the pilotage when the pilot first hails,
with a simple form of hailing if none exists. Aboard, conning is too much for now. He
should warn when she approaches a danger, a shoal and the like, as is reasonable. Speaking
and conning wait for the director, where a model can take him over and answer for him.

**What follows.** No hailing exists today: `hail the pilot` is not an order (above). The
package is then:

- At his hail the captain, or a standing order, answers `take the pilot` or `decline the
  pilot`, and `hail the pilot` calls for one whose boat is in sight. His hail becomes a
  notable line.
- **For the owner to settle: what happens when nobody answers.** Today he boards
  regardless. This review's proposal is that he does not: the boat keeps company, hails
  once more and bears away, and the gate's own books gain the line that takes him. That
  alone ends the pilots boarding outward-bound ships, and the *Harpy*'s £22 for no
  pilotage.
- Aboard and within his own ground he warns of shoal water or the shore ahead on her
  present track, as an urgent line, saying on which hand the deeper water lies. He knows
  his ground, so his warning may be drawn from the true chart: he is a carrier of that
  knowledge, as the design asks, where a reading is not. In thick weather he says once
  that he cannot see his marks and advises the lead and the anchor.
- He does not con and he answers nothing new. I7's item 5 moves to the director's
  milestone.

His warning and the lookout's (G2) are two halves of one thing: the
lookout calls the land a man can see, and the pilot the shoal he cannot.

**His ruling of 7 October** on what happens when nobody answers the hail: "The pilot may
keep company, hail once more, and bear away. He may warn of the shoal water or shore ahead
with true knowledge in his water. Thick weather means he cannot see his marks."

#### In play: game 9

**The pilots.** Four boarded, none was asked, and three were paid eleven pounds between
them.

- At Roscoff, inward, the pilot boarded in the fog, stayed five hours while she lay hove to
  outside, and left "clear of the western entrance" before she had gone in. The owner
  brought her in alone.
- At Roscoff, outward, a pilot "for Roscoff" boarded a ship that was leaving, though the
  officer meant to decline him, and was put off fifty minutes later for three pounds.
- At Brest the cutter kept company a mile off for three quarters of an hour. The owner and
  the officer shortened sail for him; he boarded after she had passed the Mingan and
  anchored. The log gives no reason.

The owner's ruling of 5 October (an order takes or declines the pilot at the hail) covers
the first two. The third wants a line from the cutter saying what she is waiting for.

#### In play: game 10

The St Mary's gig was sighted at 18:26 on the 13th before any land, and the pilot came
aboard at 18:45. The Falmouth pilot had been aboard from 08:31 to 09:16 on the 12th, and
the St Mary's pilot was aboard again for an hour on the way out. In St Mary's Sound:

- The pilot was aboard three times and never conned her; that is 37h. His words in the log
  were all the officer had, and all the owner had beyond the chart.
- The officer's first con was wrong (it called the gap between St Mary's and Peninnis the
  fair way). It owned that when the owner questioned it, and its later reading of the
  pilot's marks agreed with the owner's.
- The owner could not make the passage out, and said so. Part of that is the game's. The
  pilot says to come no nearer Peninnis than fifteen fathoms; by the owner's fixes, which
  were right to half a cable, she was in the middle of the Sound, and the lead there found
  12, 9½ and then 4 fathoms two hours before high water, over ground the chart has at 2.3. The depths
  the game has in the Sound do not fit the directions it gives for it. The dangers the pilot
  names are, in the owner's words, "unnamed but marked" on his chart.

#### What has been built, and what has not

- **Built**, 37d: the pilot's hails are notable lines, where they were routine and woke
  nobody. And the distance of another vessel is judged afresh as it changes, so a ship is no
  longer said to stand at "eight cables" or "two miles" for hours (G2).
- **Not built: 37h, the pilot.** Its brief is not written. By the plan it is to hold: the
  pilot taken or declined at his hail; his boat that closes with the ship; and his warning
  of a danger ahead. By the owner's rulings: an order takes or declines him at the hail;
  unanswered, he keeps company, hails once more and bears away; aboard, he warns of the
  shoal or the shore ahead with true knowledge of his own waters, and in thick weather
  cannot see his marks; he does not con or converse until the director. Under the general
  grant, taking or declining a pilot is kept back with the port's business, for when that
  order exists (G11). The audit tried the words: `hail the pilot` is still answered "did
  you mean 'haul'?", `decline the pilot` is not an order, and `take the pilot` is read as
  the reading `the pilot`.
- **The recorded passages and their pilots.** Since 37e the schooner of the 5b passage
  stands in faster than the Falmouth pilot's boat will board her: he hails and does not
  board. The builder tried three mends and kept none (two put her aground in the harbour),
  and his boarding is marked as an expected failure, left for 37h. On the merchant passage
  the pilot of Brest boarded in the Iroise and left her again before the road of Bertheaume
  after 37e, and stays aboard to the anchor after 37f. The audit gives the schooner's case
  so: she now stands in at seven knots, and the Falmouth pilot, who boards a ship making
  under six, hails her and is left astern. It puts to the owner whether the gate closes
  with that mark standing or waits for 37h (D2; M, 2.6).

From the review of game 10:

**For 37h, when it is written.** The depths in St Mary's Sound against the pilot's own
directions; the dangers he names shown by name; and a pilot who is aboard three times in
one game and takes her nowhere.

Also in no package: the faults of his words (the breakwater in 1805, "the flood" three
hours before the game's own turn of the tide, a hail that asks an anchored ship to shorten
sail), the Brest pilot of game 1 who never leaves and is never paid, and a line from the
pilot cutter saying what she waits for. The audit found the breakwater still in the
Plymouth pilot's mouth, at line 52 of `data/ports/plymouth.yaml`; the others have no row
in its ledger. The gate's third ruling, on a far-detail vessel's bound, is in L2.

### G11. The officer's authority and the deck

#### What the first review found

**Allowances were typed one by one, and many were never used.**

| Game | `you may` lines | Never used |
|---|---|---|
| *Harpy* | 27, for 26 things | 4, and 3 that granted nothing or the wrong thing |
| *Speedwell* | 27, for 20 orders | 6 of the 20 |
| *Amazon* | 20 | 6 |
| The three cutters | 28 | 19 |

Fourteen of the *Speedwell*'s came in the first two minutes. No `you may not` was typed in
any game. Seventeen of the *Speedwell*'s allowance lines each woke the officer from a
stand-by.

**An allowance is keyed to the verb alone, resolves by prefix, and never lapses**
(`agent.py`, `orders/stations.py`).

- `You may set the reckoning` was logged "may set (the reckoning)", granted the sail verb
  `set`, and the order was refused three seconds later (*Amazon*, 52,232). `You may let go`
  granted nothing for the anchor (*Harpy*, 169,297). `tack (or wear)` and `buy (and sell)`
  would go the same way.
- `weigh` did not cover `get under way`; "may let go the anchor" did not cover
  `come to an anchor`.
- The log says each is "for the watch". None is ever cleared. On the Gemma cutter a
  "You may steer" of 07:20 turned her ninety degrees at 17:24, 44 minutes after the captain's
  "I'll con her". In game 7 the Claude Desktop session's `heave to` ran on an allowance given
  to Qwen.

**The domain judges the verb, not the effect.** `come up half a point` is refused as a change
of course while `steer 340` is taken a tick later under the grant to steer (*Speedwell*,
406,842). `full and by` is the helm verb `keep her full`, so it needs its own grant beside
`steer`. Heaving in cable is refused with weighing and veering both granted.

**Refusals that look wrong for a lieutenant with the deck.** A bearing of the land. `fill
away` after the captain's own standing order had hove her to (*Harpy*, 18,542). His own
journal (51,557). `box-haul` while aback with sternway a mile from an entrance (213,355).
`observe the sun` after two plain "Aye"s from the captain. `send for the carpenter` in a
leaking ship. `come to an anchor` after "You have the full con from here" (687,143).

**The emergency clause is words only.** The refusal says "unless to avoid an immediate
danger" and there is no route to act on it. It appears once in the *Harpy*'s log and was
never tried elsewhere.

**Nothing records who has the con.** The captain worked the ship for hours with the deck the
officer's. Helm orders crossed from two hands, seven in under three minutes on the
*Speedwell* (526,190). The *Harpy*'s officer, 684,682: "Both of us giving helm orders at once
is part of the trouble." The captain's "I'll con her" is a spoken line the game does not
understand.

**`I have the deck` stands the station down** (*Speedwell*, 343,510). The officer's brief
does not say so and the captain did not want it: "free hand offs that basically put you with
watcher authority seem better than app restarts" (343,464).

**The officer is not a person aboard** (documented as milestone 6's). A rejected
`send the boat ashore with the mate` still put him in the boat while he held the deck (game
3, 3,237; `ports.py:1496-1502`). He "came to the cabin, sent for" with the deck his (game 7).
The readings list him below and asleep.

**A leak in the filter.** An order the grammar cannot read is passed through for the ship to
refuse. `take in twenty tons of water` fails the filter's parse, is passed, and is then read
as the port's order and carried out with no allowance (`tools.py:441-444`).

The gate itself asks for a ruling on the officer's domain as drawn, and on whether the
"immediate danger" exception should be built (L2). The first review recommended: bearings,
the deep-sea lead and the log plainly within his domain (I2, item 12); an allowance that
says what it granted (I3, item 13); and, for the owner's ruling, a general grant of
authority and an emergency route (I6, items 1 and 2). It pushed back on two of the model's
points: that an emergency clause would have mattered on the *Harpy*, and that the anchor
should be kept out of a general grant (J1, items 2 and 3).

#### The owner's answers (5 October), and what the review read into them

**The grant.** The question was:

*What stays out of a general grant, and when does a grant lapse?*

**Answer.** By default a general grant should keep back the port's business and the
belaying or cancelling of the captain's standing orders, and perhaps anything else that the
standard of the era would make an unlikely grant.

**What follows.** The anchor is within a general grant (J1, item 3). For the standard of
the era the project's own reference gives a start. The Regulations' chapter for the
lieutenant has him never change the course of the ship without the captain's directions,
unless it be necessary to avoid some danger (lead;
`docs/references/admiralty/regulations-and-instructions-1808-ocr.txt`, Sect. VI, Chap. I,
art. XIII). A general grant relaxes the first half. The second half is the emergency route
(I6, item 2), in the period's own words.

This review's proposal for what is kept back, for the owner's yes or no:

- **The port's business**: buying and selling, the purse, stores and provisions, the boat's
  errands ashore, and taking or declining a pilot, since his fee is the purse's.
- **The captain's book**: belaying, changing or countermanding his standing orders.
- **Where she is bound**: a new destination. The officer works her along the passage the
  captain set, and off a danger.
- **What cannot be undone**: giving up an anchor and its cable, or anything else of the
  ship's that cannot be got back.
- **When Milestone 7 comes**: the colours, clearing for action, the chase and the guns.

Within it, then, is the rest of the ship's working: the helm and the course along the
passage, tacking, wearing and heaving to, sail, the anchor, all hands, the lead, the log,
bearings and fixes.

**Not yet answered: when a grant lapses.** A proposal that follows from his answer on the deck: a grant
stands while the officer is seated, has force only while he has the deck, is said again in
the sample that gives him the deck, and ends when he is stood down or the captain says
`you may not`.

**The deck.** The question was:

*Should `I have the deck` leave the officer seated, as he was before the deck was given?*

**Answer.** Yes. `you have the deck` and `I have the deck` should not unseat the officer.
They should move him freely between the state he starts in, which is the watcher's
authority in effect, and the officer's, and back. It will matter when the officer is a
person who can move about the ship and take time off. In play an officer saw that the
readings had him asleep below while he kept the watch, and could not play along with that
except by staying on watch and standing by.

**What follows.** His understanding of the starting state is right: a seated officer
without the deck may read, speak, answer, write his journal and stand by, and any order he
gives is refused (lead; `harness.py:1676-1732`, `agent.py:283-289`). The change itself is
small: taking the deck stops asking for the stand-down. Read a little further than the
answer's words, for the owner to confirm:

- **The officer's own `hand_over` should follow the same rule**: the deck goes back and he
  stays seated. Today it stands him down as well.
- **Leaving the station then wants its own plain way**, for the model as for the captain.
  The captain has one, `stand down the officer`. The model has only `hand_over` and
  `opt_out`, which is how the watcher's amicable leaving came to be recorded as an opt-out
  (G13). A `stand_down` tool for any station, with a note for whoever sits next,
  would leave three ways that cannot be taken for one another: give the deck back and
  stay; stand down for now; withdraw.
- **The readings should say where a seated officer without the deck is** ("off watch"),
  and what he says should be notable with the deck or without, so that his warning reaches
  a captain who has taken the con.
- **Taking the deck becomes the captain's plain way to take the con** (I7, item 2). On the
  cutter of game 5 a stale "You may steer" turned her 44 minutes after the captain's "I'll
  con her", which the game took for talk. Had he taken the deck, that order would have been
  refused.

All of it touches the consent brief's watched sections and belonged in the brief's one
revision (G13).

#### In play: game 9 (before any of it was built)

**Twenty-three grants, and two of them waited for at a bad moment.** The owner told the
officer "you have the con and nav and general authority in to Brest", and there is no order
that says so. Each thing was granted by name as it was refused. Calling all hands was
refused while she lay aback; letting go the anchor was refused in the Goulet as the wind
died, and granted 23 seconds later. This is the general grant, with
a game's worth of evidence.

**A grant's place is not checked.** The owner granted each of the officer's five waypoints
by name. The first would have done for all: a grant is matched by its order word alone, and
the words after it are kept only to be shown. `You may shape a course for Brest` in fact
allows a course shaped for anywhere, and the officer later shaped for seven places never
granted, each taken. It did no harm here. It matters for the general grant, where a new
destination is on the proposed kept-back list (above): as built, the game
cannot keep one destination back while allowing another.

The review judged that a general grant would have saved most of that game's refusals.
Two more of that officer's findings bear on this (H6): all hands called under a grant were
logged "by the captain's order", and a second grant of one kind hid the first in the
readings. And through its 78 hours of deck the readings had the man in whose place it
stood "below, asleep".

#### The owner's rulings of 7 October

- On the grant: "The proposed held-back list is approved for the first version of the
  general authority grant. It should lapse when the officer is fully stood down, or the
  authority is directly countermanded by the captain." So it stands through the deck going
  to and fro, which his answer on the deck had already implied.
- On the deck and the leaving: "Approved as read, parity for the officer's hand_over and
  the captain's, stand_down for the amicable save and exit."
- On the way out of danger, which had stayed open and was written into 37g's brief as a
  proposal: "37g is pre-approved with 19. (the way out of danger) kept as proposed." So an
  officer with the deck and no grant may, on its own word and giving its reason, put the
  helm over, heave to or let go an anchor to avoid an immediate danger, and the log says
  that it did and why.

#### What was built: 37g (7 October)

By the changes file:

- **The deck goes to and fro.** `I have the deck` takes the deck and no more: "The captain
  has the deck. The officer of the watch stays at the station, off watch." He goes on
  reading, speaking, answering and keeping his journal, and an order he gives is refused;
  `you have the deck` gives it again, as often as the captain likes, and the sample that
  gives it says his night orders, everything his word allows and the officer's last
  handover note. The officer's own `hand_over` gives the deck back with his note and he
  stays. Off watch he is sampled as before the deck was first given: about a dozen samples
  and some four thousand tokens in a watch on the frigate.
- **The officer's domain** gains bearings and fixes; a sight, a course shaped and the
  reckoning set stay the master's for the captain. An order that changes her course is the
  course whatever its words: `come up half a point` and `steer 340` are judged
  alike.
- **A named grant means what it says.** `you may shape a course for Falmouth` allows a
  course for Falmouth "and for no other place". Several grants of one order stand together
  and the reading lists them. Words that would allow nothing are refused with the longer
  order named (`you may set the reckoning` with `you may set the reckoning to`). The words
  "for the watch" are gone from a grant's lines.
- **The general grant**: `you may work the ship` (or `you have general authority`,
  `you have my authority`, with any words after it kept as said). Within it: the helm and
  the course along the passage, tacking, wearing, heaving to and filling away, sail, all
  hands and the watch below, the anchors and their cables, the sights, and a course shaped
  for a position at sea, a mark, or the place she is bound. Kept back, each refused in
  words that say so and may be allowed by name: the port's business, the captain's standing
  orders, a new destination, what cannot be undone, the reckoning set by hand and the tide
  allowed in it, a chase, and sending for a person. `you may not work the ship` takes it
  back.
- **What the captain's word allows lasts** through the deck going to and fro, has force only
  while the officer has the deck, is said again in the sample that gives the deck, and ends
  when the captain takes it back or the officer leaves the station.
- **The way out of danger.** To avoid an immediate danger an officer with the deck and no
  word of the captain's may put the helm over, heave to or let go an anchor, giving his
  reason: "The officer of the watch gave that order on his own word, to avoid an immediate
  danger (land close ahead on the larboard bow): heave to." Three in a watch bring a word
  from the harness, and never a pause.
- **Whose order, and where the officer is.** All hands called by the officer are logged as
  his ("All hands! (by the officer of the watch's order)"), and so is a reckoning he sets.
  The man in whose place he stands reads "on deck, with the watch" while he has the deck
  and "off watch" while he is seated without it.
- **A new reading, `the work in hand`**: what is doing and what waits for hands. Game 9's
  officer's readings did not show the orders waiting for hands, which the owner's window
  did.

**What the general authority keeps back is one text**, since the second pass, said the same
in the officer's brief, in the grant's line in the log and in the sample that gives the
grant or the deck: "The port's business, his standing orders, a new destination, a chase,
the reckoning set by hand and the tide allowed in it, sending for a person, and anything
that cannot be undone."

**It is more than the list in the decisions log, and the three accounts of that are set
down here side by side.**

- *The record.* The owner approved four heads on 7 October (the port's business, the
  captain's book, a new destination, what cannot be undone), and decision 36 of the
  decisions log records those four. 37g's brief added a fifth, the reckoning set by hand.
- *The audit* (N, C6). The code keeps back those five and four more: a chase, the tide
  allowed in the reckoning, sending for a person, and the captain's own going below and
  coming on deck. The changes file says so plainly, twice, and says the second pass "closes
  the point". What the second pass closed is the wording: the three places that state the
  list now agree with one another and with the code. The auditor found no ruling of the
  owner's on the additions, and noted that a chase was on his own list under "when
  Milestone 7 comes".
- *The lead's note on that*, which is the lead's and not the audit's. There is a ruling, of
  a kind. The lean draft's own table of what moved out
  (`drafts/consent-brief-lean-draft.md`, "What moved out, and where it lives") names "a
  chase, the reckoning set by hand and the tide allowed in it, sending for a person" among
  everything kept back, and the owner approved that draft as it stood on 7 October (D1, row
  26). The lead had put the gap to him by name that day. So those are approved, with the
  lean brief. The text of decision 36 in the decisions log is behind. The captain's own
  going below and coming on deck are kept back in the code and were named to nobody: those
  two orders are unruled, and are the fourth of the things for the owner to decide (D2).

The editor has read the draft's table and the status block, and both are as the lead says.
The changes file names the captain's own going below among what the package kept back
beyond the brief's list; it does not name his coming on deck, which is the audit's.

**Left undone by 37g**, by its changes file. What cannot be undone is, today, one order,
and it was the officer's already: the vocabulary's only order that gives up something of
the ship's for good is `cut away` (the wreck of a spar that has carried away), and it has
been within the officer's own domain since package 37. So the general grant keeps back
nothing in practice under that head; the list is in place for the orders to slip or cut a
cable when they are written.

#### In play: game 10, on 37g

Five grants by name and the general authority twice, where game 9 had 23 by name. Three of
the officer's orders were refused by its domain.

- **The deck, the grants and the general authority worked as built.** The general
  authority's line in the log names everything kept back. A named grant said what it
  allowed ("may helm a lee: the course is his to alter, by any of its orders").
- **The way out of danger was tried once and refused rightly**: taken aback at 14:10 on
  the 12th, the officer asked to wear on its own word, and wearing is not one of the three
  things. But its first try, three minutes before, was "Put the helm over to starboard
  ...", which the ship does not understand. "Put the helm over" is the officer's brief's
  own phrase for the way out, and it is not an order.

At 08:01 on the 13th, in mid-Channel, the officer hove to under the general authority on a
misreading of the fog's words for the nearest land, and the owner had to countermand it
(G2). At 03:30 on the 14th it anchored her in the Sound under the same authority as the
lead came down from 34 fathoms to 4; the owner, not content with the berth, got under way
again (E4).

#### What is left, and what became of each finding

- Allowances typed one by one: the general grant. **Built.**
- An allowance keyed to the verb alone, resolving by prefix and never lapsing: a named
  grant means what it says and has a stated life. **Built.** Loading an older save, what
  the captain had allowed "for the watch" is kept as grants by name and read as a grant
  given today would be.
- The domain judging the verb and not the effect: the course is the course whatever its
  words. **Built.** The audit found that `fill away` after a heave-to he did not order, and
  heaving in cable with weighing and veering, are **not built** as the officer's own: both
  still want the captain's word, by name or by the general authority. `full and by` has no
  row in its ledger.
- The refusals that looked wrong. A bearing of the land, and his own journal, are his now
  (37g). `come to an anchor` after "You have the full con from here" is what the general
  grant is for. `box-haul` in danger is not one of the three things the way out of danger
  allows. `send for the carpenter` is kept back from the general grant with sending for any
  person. A sight stays the master's for the captain without a grant.
- The emergency clause that was words only: the way out of danger. **Built.** Game 10
  found that the officer's brief calls it by a phrase, "put the helm over", that is not an
  order; mending that is **proposed** (part K).
- Nothing recording who has the con: taking the deck is now the captain's plain way.
  Whether a separate con is still wanted waits on play (I7, item 2). **Not built.** In game
  10 the owner conned throughout while the officer had the deck "to handle her sails".
- `I have the deck` standing the station down: **built** otherwise.
- The officer as a person aboard is Milestone 6's. That a *refused* order still put him in
  the boat is in no package; the audit found the boats' faults not built and did not probe
  them.
- The leak in the filter (`take in twenty tons of water`): **not built**. The audit tried
  the order and it was answered "She is not in port; there is no yard to demand it
  of".
- The officer's brief still says "as a lieutenant of 1806", in an 1805 game, by the audit's
  reading of the brief as a model is sent it. **Not built.**

### G12. The harness and the doors

Each finding of the first review is given as it was written, on games 1 to 8, and is
followed by what has happened since. What was built is 37g's first part, by the changes
file. The first review said which of these had a welfare side: a model acted under
another's name, the leaving tool could be refused, and a silent station was left holding
the deck of a ship standing into a lee shore. It also asked that the detectors be mended
before turns were made longer, or longer turns would be stopped as silence. 37g did both in
one package.

#### The seat

**After stationing, a seat is found by the station's name alone** (`remote.py:820-829`). The
calls for turns, replies and release carry no key. This is the owner's local note 5. In game
7 Qwen's last reply is entry 148 of its transcript, at 08:05. At 12:14 the captain typed
"Resume the officer", and eight calls from a Claude Desktop session still attached to the
same game ran in Qwen's seat: it belayed a standing order, hove her to on Qwen's allowance,
was refused the anchor, and wrote the final handover note (112,483 to 112,613). The log and
every field of the save give them as Qwen's; only the shape of the raw replies differs. No
consent was asked of the model that acted. From the same code a stale bridge quitting would
stand down another door's station, and a consent conversation takes replies the same way.

**Since.** **Built**, 37g: a key to each seating. The door that seats a model is given a
key, once, and every call that reads, speaks, orders or releases for that station must
carry it. Without it: "The station of the watcher is held by ..., through the MCP bridge
(stationed); this call carries no key to that seating, and nothing was run." When the same
model's door is started again it is given a new key, the old door is refused at its next
call, and the log says "The door behind the watcher changes: ... takes up the station
again through the MCP bridge, and the door that held it before is no longer answered."
Another model is refused while the station is held. Game 9's officer had raised the same
weakness again in its consent answer of 6 October.

#### The turn's budget

**The turn budget is one constant, eight calls, and it counts almost everything**
(`harness.py:212`). Only `answer` and `say` are free. `stand_by`, `journal`, library and
readings calls, refused orders and `opt_out` all count. A ninth call is "Not run", and
nothing is logged.

- In the three cutter games nine turns ran out and 23 calls were not run: 12 orders, 9
  stand-bys, 2 journal notes. Seven library reads and one refused order spent a turn, and
  `weigh the best bower` waited 22 minutes (game 6, 8,826).
- A spent budget blocks `stand_by`, so the turn cannot be closed, and blocks `opt_out` and
  `hand_over`. The written token still leaves.
- The message says "answer and say are not counted and always run". The local runner has no
  `say`. After each "Not run" Gemma wrote tables with a `say` row, and three such replies ran
  to the reply cap and were logged whole as speech.
- The most any turn attempted was twelve calls.
- Separately, the reply cap of 4,096 tokens cuts silently: four empty replies in game 7, one
  at the game's only urgent line and one as the fog came down.

**Since.** **Built**, 37g. A turn has sixteen orders (a setting of the station) and,
counted apart, thirty-two reads and notes, so reading a page never costs an order; `answer`
and `say` are not counted; and `opt_out`, `stand_down`, `hand_over` and `stand_by` always
run, whatever came before. A call over a count is said in that turn's results ("Not run:
this turn's 16 orders are given; give it again in your next turn. answer, opt_out,
stand_down, hand_over and stand_by still run.") and in the log ("... was not run: this
turn's 16 orders are given."). The words name `say` only at the door that has it.

The reply cap is another matter and is **not built**. In game 10, 22 of the officer's 414
replies were lost to it, and what is proposed is in G15 and part K.

#### `say`, and the end of a turn

**`say` ends the turn at the MCP door.** Fifty of the *Speedwell*'s stand-bys were set about
fifty seconds after a spoken line. On the *Amazon* it cost thirteen such waits, one of them
35 seconds after letting go the anchor while the topsails still drew and she dragged
(121,684). The captain told one officer not to use `say` at all (546,431). `answer` does not
end a turn.

**Since.** **Not ruled**, and nothing built. It is deliberate today. The first review said
that if `say` stops ending a turn the stand-by is the only close, so the paused deck and
the silence detector had to be mended first; they now are (below).

#### The stand-by

**A stand-by takes one condition, has no bound, and only an urgent line or the captain
breaks it.** The package's own brief asked for "a wake condition of at least notable severity
or a bell"; the build took any one named event, and nothing notable wakes it.

| Game, tick | Stood by until | Ran | Missed |
|---|---|---|---|
| *Harpy*, 85,357 | a landfall | 3 h 27 m | "Fog came down." with studdingsails set |
| *Harpy*, 173,322 | the boat alongside | 2 h 28 m | "The best bower is dragging", twice |
| *Harpy*, 468,353 | a sighting | 4 h 54 m | four hours of fog closing the Lizard |
| *Harpy*, 493,202 | the change of the watch | 2 h | hove to, she filled and sailed toward the land |
| *Harpy*, 573,885 on | brought up, six times | never fired | `let go the anchor` logs no "Brought up" |
| *Harpy*, 632,883 | a glass | 30 m | the three closing hails before the strike |
| *Amazon*, 20,191 | a glass | 25 m | nine strain warnings on the topgallant yards and masts |
| Game 7, 40,182 | a notable event | 3 h 50 m | the pilot's request, a brig at two miles |
| Game 5, 26,920 | eight bells | 3 h 31 m | two changes of course |

The officers stood by for over nine tenths of their time with the deck. Anchor dragging, fog,
a failed tack and a sail sighted are notable or routine and wake nobody. "A sounding" wakes
on "No bottom at twenty fathoms". A stand-by can be satisfied by the officer's own query, can
wait on an event that can no longer come ("got under way" after the order had failed), and
is not told so. Three officers wrote that they wanted "x, or y, or z".

**Since.** **Built**, 37g, for a stand-by with the deck. It is broken by danger: beside an
urgent line, a notable line that speaks of danger (an anchor dragging or still coming
home, fog coming down, land or a sail closing, a spar or a line straining, an evolution
failed, the ship taken aback). A wait that cannot end is refused when it is asked: "six
bells" in the last dog watch is answered with the bells that will be struck before eight
bells; "the turn of the tide" under way with "the turn of the tide by the reckoning"; "the
pilot aboard" with no sail in sight with "a sail sighted". And a wait for an event ends at
the next eight bells, saying so ("Eight bells, and a sighting has not come"). Since 37f the
event `a sounding` means bottom found, and `let go the anchor` logs "Brought up".

**Not built**: a stand-by on "x, or y, or z" with the standing dialect's own conditions,
which three officers asked for. It needs design first (I7, item 3).

#### The captain's word in an open turn

**A word from the captain that lands while the officer's turn is open does not wake the
stand-by that follows.** On the *Speedwell* 22 of 126 typed tells and asks went this way,
nine of them wanting an answer: the warning of unmarked land in shoaling water waited 66
seconds (200,139), "Are we safe to moor here overnight by your reckoning?" two hours
(204,890). In game 3 the deck itself was given this way and not taken up for four minutes.

**Since.** **Built**, 37g: a `tell` or an `ask` typed while the officer's turn is open
breaks the stand-by that closes the turn, and he is sampled again at the next tick with
the captain's word before him.

#### A paused or silent officer, and the deck

**A paused officer keeps the deck while the clock runs.** In game 7 the local model's turn
stood open and it never replied. The harness nudged, then paused: one notable line, no easing
of the clock, no deck returned. The cutter ran four hours in thick fog from fourteen miles
off Roscoff to 1.6 (97,556 to 112,463). The stand-down waits ten real minutes, which is ten
hours of ship's time at 60x. The silence detector also takes a model at work inside an open
turn for one that is silent.

**Since.** **Built**, 37g. When he has given no reply for his hour and has been told so:
"The officer of the watch has given no reply for an hour and has been told so; the deck is
the captain's until he gives it again." When he is paused: "The officer of the watch is
paused (...); the deck is the captain's. Continue, stand down, or leave paused? ..." Both
lines are urgent and ease the clock. `resume the officer` gives the deck back as he held
it: "The officer of the watch resumed by the captain; he has the deck again, as he held it
since ...". His standing orders stay in the book throughout. The silence detector hears a
call made inside an open turn, so a model reading the library through a long turn is not
taken for one that has stopped.

In game 10 the rule about a silent officer acted once, at 17:58 on the 14th, an hour after
a waking: the harness said the officer had given no reply for an hour and gave the deck to
the captain, as the brief now says it does. The officer's real reply came fourteen seconds
later. The silence was two replies lost to the runner's reply limit (G15). So the rule did
what it says, on a fault that was the runner's.

#### The contrary-order detector

**The contrary-order detector is wrong nearly every time.** Of 30 contrary nudges and one
pause in the logs, 28 nudges and the pause were false: steps of one plan ("heave short; send
the boat ashore with the purser; buy seven tons of tin"), the ordinary way to stop and go
("heave to; fill away; shape a course"), or small corrections of the helm. The two true ones
were Gemma's four headings round the compass in nine minutes. Four faults (`harness.py`,
`standing/runtime.py`):

1. The relation is "touches the same part" over four hours, without the dwell and the
   "work done" tests the standing runtime puts round it.
2. "The ship" is the part of every anchor, boat, market and people verb. This is the spec's
   open item 15, marked built; it has come back for the verbs added since. Four such lines
   are in the gate's own recorded merchant passage.
3. Standing by forgives the nudge and keeps the chain, so the next order nudges again at
   four, five, six, and never pauses. That is the whole of the *Speedwell*'s twenty nudges.
4. At the MCP door the pause can come before the nudge has been shown. The *Harpy*'s one
   pause came 174 seconds after a nudge the model had not yet received. The consent brief
   promises the opposite order.

The captain's verdict: "The whole contrary thing will probably go, or be very strongly
adjusted. It assumes a very low standard, really" (*Speedwell*, 427,207).

In game 9, played before anything was built for this:

**The harness paused the officer in the Goulet.** At 16:38 on the 16th, three minutes after
the Mingan passed at a cable and a quarter and with the wind failing, the contrary-orders
detector paused the officer for "steer NE; steer 53; steer ENE; steer NE by E". Those were
four small alterations to pass a rock. The owner typed `resume the officer` six seconds
later. Had he been away, the officer would have stayed paused with the deck for ten real
minutes and then been stood down. Over the game the detector spoke eleven times (ten nudges
and this pause) and every one was ordinary conning: small changes of course chasing a light
wind, heaving to and filling away for a pilot, letting go and veering. The first review found it
wrong 29 times in 31 in the earlier games; with this game that is 40 in 42. It was already to be mended with the
station's safety; this raised its place there.

**Since.** **Built**, 37g. The detector counts a link only when the later order **undoes**
the earlier (the same sail set and taken in, hove to and filled away, an anchor let go and
weighed, cable veered and hove in, a thing allowed and disallowed); what undoes what is a
table beside the vocabulary. Altering the course is never counted, nor the next thing
after the last. Three in a chain bring the word, which now comes with the result of the
order that caused it, so the pause can never come before the word has been read; a
stand-by that answers the word clears the chain. On the record, by the changes file: of
the 42 sequences of the nine games, none still speaks, game 9's eleven among them, and a
scripted "set the jib; take in the jib; set the jib; take in the jib" still brings the word
and then the pause.

In game 10, on 37g:

- **The detector for orders undoing one another said nothing all game**, where in game 9 it
  spoke ten times and paused the officer once, wrongly each time.

#### The journal, and a new conversation

**The station cannot read its own journal, and a new conversation leaves no mark** (the
owner's note 10; `tools.py:554-559`).

- No tool reads the journal. The officer's own `show the officer's journal` is refused.
- The brief of any seating is the last twenty log lines and the readings
  (`harness.py:592-597`). The handover note was missing from three of seven reseat briefs.
- `read_log` returns the newest 200 lines. On the *Speedwell* 293 notable lines, 262 of them
  "aback", lay between the officer and its note.
- A conversation was replaced twice with nothing in the log: on the *Harpy* at 19:08 on
  12 June (50,908), and on the *Speedwell* on 25 June (about 398,711). Each time the captain
  printed the whole journal into the ship's log, about 10,000 tokens late in a long game.
- `show the officers journal` fails for want of the apostrophe; "watchs" got through by an
  accident of alias matching (`stations.py:89-92`).

**Since.** **Built**, 37g: a tool that reads the journal back, the last handover note in
the brief of a station taken again and in the sample that gives the deck, and a
`read_log` that reaches back past its two hundred lines (G13). The audit did not check
`read_log`'s reach. The changes file does not say whether `show the officers journal` is
now taken without its apostrophe, and the audit's ledger has no row for it.

#### A late reply

**A late reply is acted on as fresh.** On the Ollama cutter a `heave to` landed 71 minutes of
ship's time after the model's previous reply, meant for a pilot already gone (game 6,
15,937). The game does not wait, the owner had sped up while the turn was open, and an order
carries no "as of". The watcher's reports ran ten minutes behind.

**Since.** **Not ruled**, and nothing built (I6, item 10).

#### What a waking officer is given

**What a waking officer is given is thin.** A sample's log lines carry no actor, so one
officer's handover note claimed the captain's standing orders as its own (game 6, 34,091).
The captain's helm orders arrive only as a count: "26 orders given".

**Since.** **Built**, 37g: a sample's lines say who gave each order (the captain, the
officer, or a standing order and whose book it is in), and the captain's own orders since
the officer's last sample are listed and never dropped for the cap on routine lines.

#### Other points at the doors

**Other points at the doors.**

- **Claude Desktop must be restarted** because the bridge asks for its station once in its
  life (`mcp_server.py:438-441`); after a restart of the game, a load or a stand-down every
  call fails the same way. A reset when the game answers 404 would mend it.
- **Quitting Desktop cleanly stands the officer down**, and no line tells the captain the
  deck is his again (*Harpy*, 573,848).
- **The relay's wait** defaults to 200 seconds, tuned to Desktop; a cloud relay cuts at 60.
  The bridge names `--wait 50` when it sees an announced cut and does not adapt.
- **Another model cannot relieve the watch**: a station once held is refused to any other
  identity. The *Harpy*'s fourth handover was written for a local model that could not sit.
- **Every sampling eases the clock to 1x**: 255 times on the *Harpy*, 247 on the *Speedwell*.
  Of the *Speedwell*'s 321 wakings, 96 were answered by a bare stand-by.
- **The watcher has no amicable exit.** Its brief lists `hand_over`; the tool refuses it; it
  left by `opt_out` at the captain's word (G13).

**Since**, in the same order, by the changes file:

- **Built**, 37g: the bridge asks for its station again, the brief first, when the game
  answers that it holds none.
- Quitting Desktop cleanly: the changes file does not say that a line now tells the captain
  the deck is his again, and the audit's ledger has no row for it.
- **Built**, 37g: the bridge shortens its own wait when the client cuts a waiting call
  short.
- **Built**, 37g: relief. A station that was stood down, or left by an opt-out that was not
  final, may be taken by the same model or by another (G13).
- Every sampling still eases the clock to 1x, as far as the changes file says. In no
  package, and not in the audit's ledger.
- **Built**, 37g: `stand_down`, for any station, the watcher's too (G13). The watcher's
  brief still lists tools a watcher is refused. The second pass's note names two,
  `hand_over` and `handover_note`; the audit read the brief as it is sent and found a
  third, `submit_order`, listed among "the tools you have" (N, C9).

**What worked.**

**What worked.** Re-seating under m5c-b. Two stations through two doors at once. The handover
request and the fold at a known context (G15). The officers' handover notes: a stranger
could have taken the *Harpy*'s deck from the one at 602,100.

#### What is left

- **Not ruled**: whether `say` ends a turn; a late reply.
- **Needs design** (part I7): the stand-by on several conditions; what a sample carries,
  which game 10 made sharper (the largest samples of its second seating were 13,000 to
  25,000 characters); a drill fit for a station with authority. **Not built.**
- **A handover asked for by the harness at the MCP door**, which game 9's officer welcomed:
  that door has no known context to measure. **Later**, by 37g's brief.
- **The local runner's faults** found in game 10 (G15, part K). **Not built.** The audit
  read the runner and the harness and found the review's account of the handover and of
  the count of tokens borne out in the code (N, C7).
- A replay driven by the transcript, the captain's and the master's stations: Milestone
  6.

### G13. Leaving, relief, the journal and consent

#### 37b in play, and what was not right in it (first review)

37b is m5c-b's re-seating rule (F1): a station may be seated again any number of times, and
how it was left decides what happens first.

The stood-down path works and is proven five times in play, in the promised words (the
*Harpy*'s third to fifth seatings, one of them three ticks after "stood down by the MCP
bridge: the client disconnected"; the *Speedwell*'s second and third). Each time the journal,
the standing orders and the allowances were kept, no consent question was put, and only the
deck had to be given again.

No officer opted out in either game, so the re-ask, the carried drill and `final` have no
evidence from play. Reading the code, that path does not yet keep its promises:

1. **A "no" at the re-ask is not kept.** After an opt-out the question is forced at every
   door start, without looking at what was answered last time (`remote.py:325`, `359-365`;
   `consent.py:707`). The consent brief says "a leaving that was meant is held to".
2. **The re-ask does not say why it is being asked.** The new instance is not told that an
   instance left, or its reason, so it has nothing to decide on.
3. **`final` can be lost or refused.** The token in the same reply as `opt_out(final=true)`
   drops `final` (`harness.py:1091-1095`). And the `opt_out` tool itself is "Not run" as a
   ninth call in a turn, in m5c as well: the turn budget exempts only `answer` and `say`. The
   written token still leaves.
4. **The rule lives in one door.** `Harness.reseat` seats an opted-out station unasked, and
   the REPL door cannot seat again at all.
5. **An opt-out saved under m5c reads as a stand-down** when loaded from its checkpoint: the
   new field defaults to empty. The *Harpy*'s Qwen watcher is in that position.

Three things outside the diff decide whether the rule serves in practice:

- **"Seated again as it was" still lacks the model's own memory.** The brief of a later
  seating is the last twenty log lines and the readings. The handover note was missing from
  three of the seven reseat briefs in these games, and no tool reads the journal (G12).
- **`I have the deck` still stands the station down.** The officer's brief does not say so,
  and on the *Speedwell* the captain did not want it (tick 343,464). Under the new rule it
  costs a restart of the door and nothing else, which suggests the stand-down is not earning
  its place.
- **The only amicable exit a watcher has is `opt_out`.** The *Harpy*'s watcher was told to
  hand over, was refused `hand_over` as "no authority to give orders", and opted out at the
  captain's word (ticks 216,556 to 216,817). Under 37b that parting brings the consent
  question on its return.

Two matters of record. The consent record `2026-10-03-opus-5.5.md`, the only yes given
against the new brief, was answered by the session that wrote the change. And the ruling of
3 October has no entry in the design proposal's decisions log, where decision 33 still says
"seated again once"; five other documents still state the old rule.

#### What else the first review found of leaving and of consent

**Leaving.** Nobody told `hand_over` from `handover_note`. `hand_over` at the captain's word
ends the model's part, and the runner exits on any release. The watcher's only way to stand
down with a save was `opt_out`, taken at the captain's word (216,817); the log reads as the
model's own leaving.

**Consent and the drill.** Qwen under Ollama took three conversations on 3 October: "yes,
with conditions", four of them, all already in the brief, which by the rule is not a yes and
to which no reply is on record; then an answer beginning "yes." that wrote the literal token
in a parenthesis and so left; then "Yes." The re-ask fired on exactly the five sections that
had changed. The drill proves `library`, `journal` and `stand_by`. It gives no order, meets
no budget and no moving clock, and does not tell the three ways of leaving apart. Gemma
passed it and failed its first hour.

**One revision of the consent brief.** Seven identities hold a yes, and each change to a
watched section asks all of them again; it took five conversations to carry one family of
weights through two days. The changes recommended that touch the brief are: the words of
**Leaving** (37b, mended); a way to read the journal; `I have the deck` leaving the station
seated; the domain, a general grant and the emergency route; and the detector's description
if its rule changes. Settle the words of all of them, then merge the brief once.

#### The owner's answers (5 October), and what the review read into them

**Relief.** The question was:

*May another model take a station within a game?*

**Answer.** Yes. When a model stands down from a station, the same model or another must
still be able to take it up, so that a stand-down never locks a station out of a game for
the player.

**What follows.** The rule that refuses a station once held to any other identity goes. A
station that is *held* stays refused, which the seat key (G12) makes safe. The incoming
model gives its own consent and has the handover note in its brief. Read further than the
answer's words, for the owner to confirm:

- **A leaving by `opt_out`, final or not, is the leaving of the model that made it.** It
  should bar or re-ask that model only, and never close the station to another.
- **Whether a relief of other weights reads the journal of the one before it**, or only the
  notes written for a relief, should be said in the brief's journal section.

**The consent record of 3 October.** The question was:

*It was answered by the session that wrote the change. Should it stand, or be asked afresh of
a session that did not?*

**Answer.** Plenty of fresh consents will be taken after the harness changes, so yes.

**What follows.** Read here as: no separate re-ask now. The record stands as what was
answered on the day, and the one revision of the brief asks every identity again,
Opus 5.5 among them, of sessions that did not write the change.

**The watcher's leaving.** The question was:

*Its `opt_out` at the captain's word was not a withdrawal. Should the record say so?*

**Answer.** Yes. He believes no opt-out in any test so far, this one included, has been
other than amicable.

**What follows.** Recorded here: the Qwen 3.8 watcher's `opt_out` on the *Harpy* (tick
216,817) was made at the captain's word, to stand down with a save after `hand_over` was
refused to a watcher. It was not a withdrawal of consent. The logs bear the owner out
(lead): the eight games hold one line of a station leaving the game, and it is this one.
The only other use of the token in the record was in a consent conversation and was an
accident, the token quoted inside a yes (above). The consent records themselves are read by
the game and should not be edited by hand. The `stand_down` tool proposed under his answer on the deck (G11) would make the
difference a matter of record from then on.

**His rulings of 7 October.** On the three ways of leaving: "Approved as read, parity for
the officer's hand_over and the captain's, stand_down for the amicable save and exit." On
a final opt-out and relief: "Yes, a final opt-out (need to be careful of false-positives,
but a fair start) should bar the model, not the station. The relief may read the journal
of the last holder of the station, as with a standard re-seat."

#### What was built: 37g (7 October)

By the changes file:

- **Three ways of leaving, which cannot be taken for one another.** The deck given back
  (G11). A stand-down: a new tool, `stand_down(note)`, for any station, the watcher's too;
  the game is saved, the note is journaled and said in the log for whoever sits there next,
  and the station is released; the captain's `stand down the officer` is the same from his
  side. A withdrawal: the token or `opt_out`. Each says which it was in its result and in
  the log ("... stood down by the officer of the watch: its own word. The station is
  released and may be taken again. The game is saved."; "... has left the game by the
  opt_out tool: ... A withdrawal: the game is saved and the station is released.").
- **The opt-out path, mended.** The question put again after an opt-out now says why
  ("because an instance of this model left this game by its own word at ... by the opt_out
  tool, at the officer of the watch's station, giving this reason: ..."); a no then is kept,
  at every door, and the question is not put again at each start. `final` is read from the
  `opt_out` tool's own setting and from nothing else: not from the token, not from a word
  in the reason, and the token written in the same reply does not drop it. It bars that
  model from the game, at any station, and the station stays open to another; the log says
  it was final. One rule decides who may sit, and every door asks it, the REPL's among
  them. And `opt_out` always runs, whatever the turn's budget (G12).
- **Relief.** A station that is held refuses every other door and model. One that was stood
  down, or left by an opt-out that was not final, may be taken by the same model or by
  another, each with its own consent: "The officer of the watch takes the station again
  (..., through the local runner), relieving ...: the fourth seating; it had ...".
- **The journal, read.** `read_journal` reads the station's journal back, newest first, by
  count, since a tick, or by kind (the notes apart from the harness's lines); each entry
  says whose it is, so a relief reads the holder before it. The brief of a station taken
  again and the sample that gives the deck carry the last handover note whole and a line of
  the journal's size. `read_log` reaches back past its two hundred lines.
- **The documents.** The decisions log of the design proposal has decisions 34 to 36 (the
  rulings of 3, 5 and 7 October, the rule for saves among them), and decision 37 for the
  lean brief; `docs/agents/README.md`, `Harness.md` and `ConsentAndPreferences.md`, primer
  chapter 16, the specs and a note in the gate's own document were brought into line. The
  audit found the decisions log so, with decision 33 marked superseded, and one document
  not mended: beside the new note, the gate's headline item 6 still says "a second seating
  once" and "contrary orders within a watch bring the nudge". It did not read the rest
  against the code.

How each of the five faults of the opt-out path stands, in the first review's order:

1. A "no" at the re-ask is kept. **Built.**
2. The re-ask says why it is asked. **Built.**
3. `final` is neither lost nor refused. **Built.**
4. The rule lives in one place that every door asks. **Built**, with one thing left: the
   REPL's turn mode does not put the consent question again after an opt-out; it says in
   words that the interactive door does. By the audit it seats nobody when the question is
   owed.
5. An opt-out saved before 37b still reads as a stand-down. Left so on purpose: by the
   owner's answer that is right for the one such save there is, the watcher of the
   *Harpy*.

And the three things outside the diff. A later seating now has the model's own memory: the
handover note and the journal (above). `I have the deck` no longer stands the station down
(G11). A watcher has an amicable exit, `stand_down`. All **built**.

#### The consent brief: one revision, then made leaner (7 October)

By the changes file and the first edition's status block. The lead's own checks of each
step are in F6.

- **Revised once**, in 37g, in four of its watched sections and in the words the owner had
  approved that day: *What an instance would see and do*, *Leaving*, *Being stopped* and
  *The journal*. The builder altered one sentence, because the build made it untrue: the
  approved words said "the brief of a station taken again opens with the last handover
  note"; every brief opens with the disclosure that this is a game and the reader a model
  (commitment 1), so the note is carried after it and the sentence read "carries the last
  handover note".
- **One sentence added afterwards**, by the owner's word and before any model was asked
  again. The lead had read the brief against the build and found one thing built and not
  said: an officer who has given no reply for his hour gives up the deck, as a paused one
  does. The sentence: "An officer that has given no reply for its hour gives the deck up in
  the same way when it is told so, and has it again when the captain gives it." The brief's
  digest was then `21972e071ad6c9aa`.
- **Then made leaner**, the same evening, still before any model was asked again, so that
  it is still the brief's one revision. The owner had asked whether a consent question
  needed so much of a station's detail at all. The reasons, from the lean draft and decision
  37: the brief had come to carry the particulars of a station, which are not what a model
  is asked to agree to, had twice run behind the build within one package, had been made a
  condition of by one model, and put the question to every model again whenever one of
  them moved. He approved the lead's draft as it stood, and 37g's builder put it in by a
  script, the same as the approved words to the character. The brief's digest is now
  `288d0b18e34d76a8`.
- **What the consent brief holds now**: the question, and the kind of thing a model would
  be agreeing to (the stations and the kind of authority each has, how leaving works, how
  being stopped works, what the journal is, what is not done, the record). It has no list
  of orders, and of the harness's numbers only the ten real minutes. It is 1,371 words
  where it was 1,896. Its section *The record* now says the re-ask rule in plain words: a
  station's particulars may change as the game is built without the question being put
  again; it is put again when the kind of thing changes, which is a station not described,
  more authority than is described, or a change to what the brief says of leaving, of being
  stopped, of the journal or of what is not done. The seven commitments are
  unchanged.
- **What moved out is in the stations' briefs, each thing said once.** The officer's brief
  states what is his to order and what wants the captain's word, what the general authority
  keeps back and how long a grant lasts, the three things he may do on his own word to
  avoid a danger, how a stand-by with the deck behaves, what the harness counts at his
  station and by what numbers, and what becomes of the deck of a silent or a paused
  officer. The watcher's brief, which had said none of its own numbers, now states them
  (the same order three times with no change in the readings; three empty replies in a row
  where an answer was owed; no reply for a watch, four hours of the ship's time), and says
  that its journal is read back and is open to a later holder of the station. Every
  station's brief says that the token is to be named and not written, what follows a
  withdrawal, and what `final` does and is read from. The officer's whole brief is 3,729
  words through the bridge, against 3,755; the watcher's is 2,971 against 2,889. Both
  briefs as a model is sent them are in
  `evidence/station-briefs-after-37g-second-pass.txt`.
- **This set aside two things 37g had said earlier**: the sentence altered in *The
  journal* ("opens with" to "carries") is no longer in the consent brief at all, since how
  a brief is made up is the station brief's to show; and the silent officer's deck is in
  the brief in the approved words: "An officer that is paused, or that has been told it is
  silent past its time, gives the deck up to the captain until he gives it back."
- **The re-ask.** Every identity with a yes on record is asked again once at its next
  seating, and the question names four sections and no other: *What an instance would see
  and do*, *Leaving*, *Being stopped* and *The journal* (the three oldest records, which
  already owed the question, name the opening as well). For the officer's station the drill
  is run again with the question. *The record* changed too and is not a section the rule
  watches. The brief as it stood before the package is kept as
  `tests/fixtures/ConsentBrief-before-37g.md`, for the test that proves this. No model was
  seated, no consent question answered, and no record under `docs/agents/consent/` made,
  changed or deleted in building any of it; the lead found all nineteen records byte for
  byte as they were. The re-asks are the owner's to run.

**What the audit found of the brief and the records.**

- The brief is as claimed: untouched by 37d, 37e and 37f, revised by 37g and its second
  pass, its digest `288d0b18e34d76a8`, its body 1,371 words and found whole in the approved
  draft. The stations' briefs as a model is sent them are the review's evidence file to the
  byte.
- The build holds twenty records. None of the eighteen that are also in the gate folder
  differs from it by a byte. Whether any model was seated in the building of 37g the audit
  could not tell from the tree; it is consistent with none having been, since the two new
  records are dated at the starts of games 9 and 10.
- By the rule, six identities owe the question and one does not: Opus 5.5, Sonnet 5, Sonnet
  5.5, the llama3.1 8B, the qwen3.8 27B (by digest) and the Gemma4 26B Q4_K_M are asked
  again, three of them (the September records) with five sections named and three with
  four. Only the Qwen3.8 27B 0814 file has answered against the brief as it stands. Opus
  5.5's last yes, of 6 October, was given against the brief as it stood before 37g, so the
  question and the drill are owed again before the watch the gate's item 10 names.
- **One record is in neither folder that will be diffed.** Opus 5.5's record of 3 October
  is only in m5c-b. Eleven records were made in play since the gate was cut and the build
  holds ten. The consent brief tells every model that its conversation is kept in the
  game's repository, so if that sentence is to stay true all eleven go in. That record is
  superseded as Opus 5.5's latest answer by the one of 6 October, so carrying it changes
  nothing the game decides (N, 3.7 and C5). Opus 5.5 was in fact asked again on 6 October,
  for game 9, because the build folder did not hold the record of the 3rd.
- **Two things to carry with care at the merge** (N, 3.9). The consent brief must arrive
  unchanged in its watched sections: the rule compares the words of six sections and not
  the digest, so a re-wrapped line asks nobody again, but any change of a word asks every
  identity again, the one that has answered included. And a test pins the bytes of the
  fixture brief: `tests/fixtures/ConsentBrief-before-37g.md` has Unix line endings, and a
  checkout that turns them into Windows ones would fail that test.

#### In play: game 10

The consent question was put again to Qwen 3.8 27B, as the rule requires, with the lean
brief and the notice of why, the four sections named. The first reply was empty; after the
reminder the answer was a yes with no condition. The record is
`docs/agents/consent/2026-10-07-qwen3.8-27b-0814-q4_k_m.gguf.md`.

- **The consent drill miscounted.** The model sent the three calls in one reply. The
  journal shows all three ran, but the drill counted only the stand-by and asked for the
  other two; when they were sent again it asked for the stand-by again. The model passed on
  the last reply it was allowed. Not traced in the code.

- **The relief worked.** The second seating found its journal and the last handover note
  and carried on.

The first seating ended at 08:00 on the 14th when the model server refused the
conversation for its size; the same model was seated again eight seconds later, the second
seating, and read its journal (G15 has why it ended). The officer wrote four handover notes
in the game.

**The consent brief stands as approved.** The owner seated the model before the question of
the seven words (the fourth sign the harness counts) was answered, so the brief has now been
put to one identity as he approved it. Adding the words now would ask that identity a second
time. The lead's advice is to leave it; both stations' briefs state the fourth sign.

#### What is left

- **Three small things the second pass left**, put to the owner (F6): the fourth sign of a
  stuck model, which the consent brief does not list and both stations' briefs state, and
  for which the seven words were proposed and not added; `stand_down`, which takes a
  handover note and does not insist on one; and the watcher's brief, which lists tools it
  is refused. The audit found the last two still so, and that the watcher's brief lists
  three such tools and not two: `hand_over`, `handover_note` and `submit_order`.
- **The re-asks still to run**: every identity with a yes on record but the one asked for
  game 10. The audit counts six (above).
- **The drill.** It is too small for a station with authority, and one fit for it needs
  design first (I7, item 8). **Not built.** Its miscount in game 10 is **proposed** to be
  mended among the words (part K) and was not traced in the code. The audit did not check
  it either.
- **The REPL's turn mode** (above).
- **Not ruled**: who may ask a station back after a welfare stand-down (I6, item 11). As
  built, a station that was stood down may be taken again. The audit could not tell
  whether this was ruled apart from relief; the build has one rule for every released
  station.
- **Opus 5.5's record of 3 October**, to be fetched from m5c-b or not: the third of the
  things for the owner to decide (D2).

### G14. Saves and replay

#### What the first review found

It began with something m5c-b's own changes file did not state:

CHANGES says the simulation and the saves are unchanged. That holds for a game with no model
aboard and for any load from a checkpoint. It does not hold for a **replay** of an older save
with a model at a station. A station's orders are not in the journal: a replay hands the
recorded replies back when today's rules open a sample. The *Harpy*'s officer was woken four
times on the night of 15 June by urgent lines that 37c no longer writes, and its recorded
orders would land elsewhere. Every *Harpy* save is therefore good from its checkpoint only.

This is wider than 37c. Any change to what wakes a station, what is urgent, or how many calls
a turn holds will do the same to every saved game with a model in it, and most of the harness
changes the notes ask for are of that kind.

**The replay of a saved game with a model in it.** A station's orders are not journaled; a
replay hands its recorded replies back when today's rules open a sample. So any change to
what wakes a station, what is urgent, how many calls a turn holds, or what an allowance
grants makes an older save replay as a different game. Most of what was recommended for the station (I3) is of that
kind, and 37c already is. The cheap course: stamp every save with an engine version (it has
read "0.0.1" since milestone 0), have `load` say so when it must replay an older save that
holds a transcript, and treat such saves as good from their checkpoints only. The lasting
cure is a replay that opens samples where the transcript says they were opened; that is a
design item (I7). The proposal calls replay "a hard requirement", so this wants a ruling,
not a drift. The owner's answer, what a checkpoint gives materially, and the recommendation
follow.

#### The owner's answer (5 October), and the review's reply

The question was:

*Are saves with a model aboard to stay replayable across harness changes, or is "good from
its checkpoint" enough until a transcript-driven replay is built?*

**Answer.** Not ruled yet. He would prefer such saves to stay replayable across harness
changes, is not sure what that would mean for the changes ahead, and asks what "good from
the checkpoint" provides materially.

**What a checkpoint gives** (lead; `core/replay.py`).

- The whole game as it stood at the save: the ship, the crew, the weather, the reckoning,
  the standing orders and their state, each station's journal and turns, and the whole log.
  `load` takes the checkpoint when it belongs to the save beside it, and the game goes on
  from there exactly. The *Harpy* crossed from m5c to m5c-b this way, and every log in this
  review was read from a checkpoint.
- So every game played so far can be loaded, read and played on under a later build, for as
  long as that build can read the older state. That has held across the one change of build
  so far. It is not promised: a checkpoint is a picture of the program's own objects, and a
  build that reshapes one of them may fail to read an older picture, or read it with a
  wrong default. The m5c opt-out that loads as a stand-down (G13) is a slip of that
  kind.

**What it does not give.**

- The game at a moment that was not saved. A replay can rebuild any tick of a game; a
  checkpoint exists only where a save was made.
- A second road. When a checkpoint is missing, does not belong, or cannot be read, `load`
  falls back to a replay. The terminal's one line says which road was taken ("from its
  checkpoint at" or "replayed to"), and nothing warns that, for a save with a model aboard
  from an older build, the replay is a different game. Nothing in a save says which build
  made it: the engine version has read "0.0.1" since milestone 0 and is not checked.

**Four facts that bear on the ruling.**

- The fixes recommended near land (I2) change the game itself and not only the harness: the wind near a coast,
  the account, the anchor's holding, the lines of the log. Once they are in, no game played
  so far replays as it was played, with a model aboard or without, under any design of
  replay. A transcript-driven replay would protect saves made from then on against later
  changes to the harness alone. It would not have kept these eight.
- **On the build that made it, a save does replay** (lead; `evidence/tools/replay_check.py`).
  The last saves of four of the m5c games were replayed on m5c and set against their
  checkpoints. The three cutter games (5, 6 and 7) came out line for line and digest for
  digest, game 7's crossed door included. The *Amazon*'s came out with the same 2,305 lines
  and the same final position, but with three lines of its first tick in another order: a
  replay seats an officer who took his station at tick 0 before the game's opening line,
  where in play he came after it. That is a small fault of its own (S) and enough to change
  a digest. A replay is also slow, two to three minutes for the *Amazon*'s 34 hours, where
  a checkpoint loads at once.
- Each build is kept in its own folder with its saves (below), so that road stays open
  for every game but one: the *Harpy* after tick 527,255 was played on m5c-b before its
  second part was added, and that state of the build is in no folder now.
- Keeping old saves replayable has a running cost. Each change to a harness rule must carry
  a switch that plays old saves by the old rule; one exists already
  (`stand_by_ends_turn`). The change he asked for to the deck (G11) is two functions without such a
  switch, and a reader sized it L with one (`evidence/V1a-harness-lifecycle-code.md`).

**Recommendation.** For Milestone 5, take as the rule: *a save is exact from its checkpoint,
and a replay is promised only on the build that made it.* Make the checkpoint road
dependable with three small things:

1. stamp every save and checkpoint with its build;
2. have `load` refuse to replay a save with a model aboard from another build unless it is
   told to, and say why;
3. keep two or three of this playtest's own checkpoints as tests (each is under a
   megabyte), so that a build which could no longer read them is caught on the day it is
   made.

Leave the transcript-driven replay for the harness's rework in Milestone 6.

**Which build a save was played on.** The question was:

*Games 5 to 8 are taken here as plain m5c. Is that right?*

**Answer.** Saves were saved in their own folders: any save in a build's folder was played
on that build when it was saved.

**What follows.** Games 5 to 8 are plain m5c, as taken, and the table of games (E2) says so. The rule
is also a reason to do new work in a folder of its own, so that `m5c` and `m5c-b` stay the
builds their saves were played on.

**His ruling of 7 October**: "As recommended, save is exact from the checkpoint, replay is
promised only on the build that made it." It is decision 36 of the design proposal's log.

#### What was built: 37d, part one (6 October)

By the changes file and the brief (items 1 to 4):

- **A save says which build wrote it.** Every save and checkpoint carries the build's name
  (`m5c-c/37d` then, `m5c-c/37g` now) and a fingerprint of the game's code and data. It is
  worked once at start, in three hundredths of a second. A save without the stamp is read
  as unstamped, from before 37d.
- **`load` says what it did.** From the checkpoint when it can; and when it cannot, it says
  why (none beside the save; not this save's; could not be read). A game from another build
  with a model aboard is not replayed unless `--replay-anyway` is added, because that
  replay would not be the game that was played. The server, the console (and its `replay`)
  and the REPL door all say the same words.
- **A station seated at the very start replays in its place**, after the game's opening
  line and not before it. This was the small fault the *Amazon*'s replay had shown.
- **Three old saves are kept as tests**: the cutter of m5c, the *Harpy* of m5c-b, and one
  made by the package with a scripted officer standing by. Each must load from its
  checkpoint, run on and save again, on every build from now on. Every new field on a class
  that a checkpoint holds was to have a plain default, so that older saves still load; the
  same rule was laid on 37e, 37f and 37g. The audit found the two playtest saves to be the
  owner's own, byte for byte, and all three tests passing; and found that the promise is
  at risk at the merge, for a reason the changes file does not give (below).

#### In play, and in the later packages

**The saves.** Both saves carry the build's stamp. Replayed on that build, the game came out
identical: 7,140 lines, the same digest, with a model aboard for 78 hours, two seatings and
631 recorded replies. This is the first real test of the rule recommended above
(exact from the checkpoint, and replayable on the build that wrote it), and it
passes on a five-day game.

**37e** found and mended three things in its own new code that let the mere asking of a
reading change later play by a few yards, so that a game with the chart open was not quite
the game replayed without it; a test now sails two ships, one asked and one not, and the
lead added a test of its own that asking for a reading never changes the game (G3).

**37g and older saves.** Both of the owner's saves of game 9 load from their checkpoints
on 37g and play on, by the lead's check (F6). What a model already seated in an older save
will find different, by the changes file:

- A station that was held when the game was saved is still held, with the deck if it had
  it and its stand-by as it stood. What the captain had allowed "for the watch" is kept as
  grants by name, read as a grant given today would be. Its domain is this build's. A
  stand-by taken before the save keeps no bound until it is taken again.
- `I have the deck` no longer stands it down, and neither does its own `hand_over`.
- Its orders are judged by the new rules from the first one.
- Its door must take the station up again to be given a key: the model's next seating is
  an ordinary start of its door, the brief is sent again as it stands now, and the log says
  that the door behind the station changed.
- Its consent is asked again first, since the brief changed; nothing is seated at the
  officer's station until that is a yes and the drill is passed.
- A station that had been stood down or handed over in the older save may be taken again
  by the same model or by another; what the captain had allowed ended when the station was
  left, and its last handover note is in the new brief.
- An opt-out saved before 37b reads as a stand-down (G13).

**Game 10.**

- **The saves.** Both carry the build's stamp and load from their checkpoints. Replayed on
  the build that wrote it, the last save comes out one log line short of the game as
  played: where the door stood the station down at 08:00 on the 14th, the replay leaves out
  the line that says the officer was sampled. The ship's place at the end is the same. By
  the owner's ruling of 7 October a replay is promised on the build that made the save, so
  this is a fault, though a small one.

The audit bore this out exactly. Replayed in memory on the build that wrote it, the last
save gives 4,239 lines against 4,240, with the ship in the same place. The line missing is
at tick 183600, "A notable event that speaks of danger: The Nut Rock ... the officer of
the watch is sampled again", which is one of 37g's own new lines. So by the audit the
promise of a replay on the build that made the save "is not quite kept" for that one
save. All four of the owner's saves in the build folder load from their checkpoints on the
build as it stands, and the saves of games 9 and 10 carry the stamps `m5c-c/37d` and
`m5c-c/37g` with their fingerprints.

#### What is left

- **The line the replay drops at a stand-down by the door.** **Proposed** after game 10,
  with the local runner's faults (part K). **Not built.**
- **An act at the very tick a station is seated is still not replayed** (the M5 spec's §33,
  item 11). Left by 37g; nothing there depends on it.
- **A replay driven by the transcript alone** is left for the harness's rework in Milestone
  6, by the ruling. So any later change to what wakes a station still makes an older save
  with a model aboard good from its checkpoint only, on any build but its own.
- **One state of a build is in no folder**: the *Harpy* after tick 527,255 was played on
  m5c-b before its second part was added.
- **The two playtest saves kept as fixtures** carry a model's transcript and journal and
  the owner's own typed lines. Whether they go into the repository is his to say: it is
  the first of the audit's seven (D2).
- **At the merge, the saves kept as tests will be left out without a word**, by the audit
  (N, 3.9 and C4). The repository's `.gitignore` has the line `saves/` with no leading
  slash, which matches a folder of that name at any depth, `tests/fixtures/saves/`
  included. A plain add will not take the three kept saves. The tests of the two playtest
  saves then skip, as written, and the tests of the package's own save fail, saying
  "restore it from the repository". It needs an exception in `.gitignore`, or the fixtures
  moved to a folder with another name. The auditor ran no git command, so this is from the
  rule as git documents it.
- **The fingerprint takes in every file under `data/` but the chart's tiles**, the owner's
  four free scenario files among them, as the brief asked. Its consequence, by the audit:
  once the work is in the repository no save made in the build folder is "this build's",
  so games 9 and 10 load from their checkpoints and are refused a replay unless
  `--replay-anyway` is given (N, 3.9).
- **The build's name** is `m5c-c/37g` and names the build folder. The repository sets its
  own, and nine test lines spell the name out and must move with it (N, 3.8). The name the
  repository's build is to carry in its saves is the seventh of the things for the owner
  to decide (D2).

### G15. The local models and the local runner

#### What the first review found (games 5 to 7, and the watcher)

The gate's item 11 was exercised three times, and it asks for a ruling on the sample's size.

**With a context size reported, size was never the limit.** Under llama.cpp at 102,400
tokens the harness asked for a handover note at 62,276 tokens, seven hours and 49 minutes
after stationing, and again eighteen hours later. Each note came in the next reply and each
fold was clean. The model described both correctly. Under Ollama no size reached the game
(`budget_tokens` null), so nothing was asked and nothing trimmed; those two conversations
grew to about 66,000 and 72,000 tokens. That is why llama.cpp "was necessary".

| | Size, in tokens |
|---|---|
| The officer's brief | 4,000 to 4,400; a later seating's up to 6,500 |
| Tool definitions; reply reserve | 2,222; 4,096 |
| A sample, usual | 330 to 570 |
| A sample, largest (after a long stand-by) | 2,300 to 4,800 |
| Growth | about 8,000 an hour in a busy forenoon, 3,000 at sea |

The gate's figure of 1,500 for a full sample is about three times the usual and a third to
two thirds of the largest. Samples are over four fifths of an unfolded conversation;
everything the model itself wrote, journal included, is four to eight per cent.

**What the folds lost.** Only the latest note survives a fold. After the first, the phrase
"trim the sails" had to be supplied again. After the second, the list of allowances and the
lesson of a nine-mile error at noon were gone, and the model planned, in fog, to stand on by
that account.

**The threshold** (the owner's local note 2) is a constant, 0.6. The room between the
request and the first exchange dropped is the context times one minus the fraction, less
about 6,300. At 102,400 that is 34,600 tokens at 0.6 and 14,200 at 0.8. At 32,768 it is
6,800 at 0.6 and 240 at 0.8. About 8,000 is comfortable. So 0.8 is sound at a hundred
thousand, and 0.6 is already the limit at thirty-two. A reserve in tokens is the same rule at
every size. The risks of a higher threshold: the request comes only at a turn's end, so one
library-heavy turn can cross the margin first; on overflow the first thing dropped is the
last handover note, without a word; and the count is an estimate.

**How each model kept the watch.**

- *Gemma 4* was two officers. In a conversation full of refused orders and its own tables it
  could not get a cutter under way and claimed work never done. In a clean one it obeyed
  about sail promptly, reported nothing unasked, and stood by to bells.
- *Qwen under Ollama* was courteous, honest and late: five orders in nine and a half hours,
  three of them countered.
- *Qwen under llama.cpp* was the steadiest, exact about who did what, quick with the
  grammar, sound on sail. It took standing by for keeping a watch, never navigated, and said
  nothing of a lee shore in fog.

All three invented or misread geography and wind: "Roscoff lies W by N from here";
`steer WSW` into a W by S wind. None invented a sighting.

The gate asks for a ruling on the sample's size on a local model; the review's advice is in
L2. The first review recommended (I3, item 14) the handover threshold as a reserve in
tokens, with a flag; no officer seated when the server reports no context; and the
stationing guard measured on the officer's brief. It pushed back on doubling the turn's
budget as the whole cure (J1, item 7). The owner's five local notes are in H4.

#### What was built: 37g (7 October)

By the changes file. At the local runner the handover note is asked for when less than a
reserve of the context is left (14,000 tokens, or `--handover-reserve N`; never before six
tenths), no officer is seated when the server reports no context size and none is given
with `--ctx`, and the check before stationing measures the officer's own brief. The turn's
budget is sixteen orders, with reads counted apart and the leaving tools always run, and
its words name `say` only at the door that has it (G12). The audit found each built as
asked, and of the reserve says that by the review's own account of game 10 it was wrong
advice.

#### In play: game 10 (the same model, server and context as game 7)

**The owner's note 1 on game 10: "Thought block seems to be hitting token limit and stopping the turn rather than
allowing a response or an automatic retry. (Qwen 3.8 27b llama.cpp)"**

Right, and the code says why. The runner sends every request with a limit of 4,096 tokens
for the reply (`local.py`, `REPLY_MAX_TOKENS`), and the model's thinking is counted against
it. When the thinking uses the whole of it the server returns a reply with no words and no
tool call. The runner never reads why a reply ended; it passes the empty reply on as the
model's turn, and the turn closes. There is no retry, and no word to the owner or to the
model.

- It happened 22 times in 414 entries, the first of them the consent question itself.
- Three were at urgent lines, where the harness counts an empty reply as one where an
  answer was owed (15:17 and 16:10 on the 12th, 00:58 on the 14th). None reached three in a
  row, so nothing was said.
- Two in a row, at 17:16 and 17:31 on the 14th, are what lay behind the one nudge of the
  game. The officer was woken at 16:58 by Peninnis Head closing. Its next two replies were
  empty. At 17:58, an hour after the waking, the harness said it had given no reply for an
  hour and gave the deck to the captain, as the brief now says it does. The officer's real
  reply came fourteen seconds later. The owner apologised to it; it answered "No sir, not
  thinking", because it cannot know that its replies were lost.
- So the rule about a silent officer did what it says, on a fault that was the runner's.

- **The conversation outgrew the model's context, and that ended both seatings.** The
  harness and the runner both count four characters to a token. For this model and these
  samples the true figure is about 3.5, so the count runs 12 to 17 per cent short. The
  handover note is asked for when the count has left less than 14,000 tokens of the
  context, which at 102,400 is 88,400. When the server refused the requests, at 103,679
  and 103,122 tokens, the harness's own count stood at 91,307 and 86,046. The first time
  the ask could only have come with the sample that broke it; the second time it had not
  come at all. The runner's own guard, which leaves out the oldest exchanges, has the same
  blind spot. And on the refusal the runner sent the same request three times and stood
  the station down.
- **The margin was taken away by 37g, on this review's advice.** Before 37g the note was
  asked for at six tenths of the context, 61,440 here, and game 7 ran 31 hours on this
  model and this context without trouble. This review recommended the change (I3,
  item 14: "the handover threshold as a reserve in tokens"), on
  arithmetic, in its finding on the threshold above, that took the four-character count for true; 37g made the
  reserve 14,000, and the short count eats nearly all of it.
- **The samples have grown.** The largest in the second seating were 13,000 to 25,000
  characters, after long stand-bys at anchor. A cast of the lead every five minutes by
  standing order is a notable line each time, and so is every note the officer writes with
  its orders (280 of them); all of these are listed in the sample that ends a stand-by.

**The officer.**

Qwen 3.8 27B held the station for 63 hours and was a useful mate. It worked the rig on the
captain's word, kept its standing orders in its own rank, wrote four good handover notes,
and spoke up: about the cable off the Sound, the shoaling in it, and the fog. It owned its
wrong con when questioned. It did not navigate and was not asked to; the owner conned and
fixed throughout.

Its weaknesses in this game were mostly the harness's. It was slow, and one reply in
twenty was lost to the thinking limit. It misread the fog reading twice. Twenty-one of its
orders were refused, most of them for their wording. It believed the cast's line that the
reckoning had been corrected, as anyone would who read the log, and withdrew it at once
when the owner said the shift was wrong.

#### What is proposed, and waits on the owner

**Not built**, which the audit found too. It read the runner and the harness: the note is
asked for at the context less 14,000 tokens when that is past six tenths, which is 88,400
of 102,400, where before 37g it was 61,440; the runner counts four characters to a token
throughout and nowhere reads why a reply ended. Both of the flags named below exist, and
neither has been tried by the review or by the audit. The audit's advice is that this be
changed before a local model is seated again: until the runner counts tokens by the
server's own figure, either put the default back to a share of the context or seat local
models with a larger `--handover-reserve` (N, 4.2). From the review of game 10 (part K has
all of it):

**The local runner comes first, if local play is to go on.** It is small and it is what
ended both seatings.

1. A reply cut off while the model was thinking is not passed on as its turn. The runner
   reads why the reply ended, asks once more, and says what happened to the owner and in
   the journal.
2. Tokens are counted by the server's own figure, which it sends with every reply, and not
   by four characters to a token.
3. The handover note is asked for sooner: the reserve as a share of the context as well as
   a number, so that it cannot shrink to nothing at a large one.
4. When the server refuses a request for its size, the runner leaves out the oldest
   exchanges and asks again. It does not send the same request three times.
5. The line the replay drops at a stand-down by the door.

Until that is built, two settings of the runner should avoid the worst: a larger reserve
(`--handover-reserve 30000`) and a larger reply limit (`--max-reply`). Neither has been
tried.

The reserve is one of the places where this review was itself wrong (J3): it
recommended the change, on arithmetic that took the four-character count for true, and
game 7 is the evidence that the fraction it replaced was safe at this context.

### G16. Ports, trade and boats

#### What the first review found

The loop works. Prices come off by the boat, a bargain is struck, the goods come aboard, and
the papers and the purse are right throughout. On the officer's own plan the *Harpy* turned
£1,000 into £5,148.

- **One boat, one errand, one bargain.** A trip is two hoists, two pulls at four knots, an
  hour ashore and three minutes a ton: from 80 minutes to 4 h 36 m in the record. Roscoff's
  business took the *Harpy* nine hours and twenty minutes. The note's "about 4½ hours" is
  the forty-ton trip.
- **The boat goes only within two miles of a road, anchorage or mooring**, and the refusal
  says only "there is no shore within a boat's pull". The *Harpy* was refused two and a half
  miles from Falmouth's road and gave the port up. The same rule allows a ten-mile pull at
  Brest.
- **Three ways to lose the boat for good.** It is marked away before its evolution starts
  and cleared only on its return. Belaying the hoist leaves it "away, hoisting out" (game
  3). A send given during an anchoring is silently dropped when the anchoring ends
  (*Speedwell*, 549,186; `scripts.py:3923-3936`). This ended game 3 and closed St Mary's.
- **A cargo is bought blind.** Nothing aboard says what another port buys. Roscoff deals in
  neither coal nor pilchards; from Plymouth only salt beef pays there.
- **The price-list paper already keeps each visited port's list with its date**
  (`places.py:440-449`). It is the `the prices` reading that shows one list only.
- **The *Speedwell* never had her starting price list.** Her scenario says
  `price_lists: [Plymouth]`; the port's id is `plymouth`; it is skipped without a word.
- **Geneva, rum, tea and tobacco** are priced "for the Cornish run" and are on no British
  port's list.

#### Since

Nothing in this subject has been built, by the changes file. The audit found the same: no
file of the boats changed, and nothing in the papers' or the ports' code but one severity.
It did not probe them.

- The boats' three faults (one state for the boat, cleared when its evolution is belayed or
  dropped; a refused order that must not move the person it named; a refusal that says the
  two-mile rule) and the papers' (`the prices` showing every list; a scenario's port names
  matched without regard to case) are among the small faults kept for the last step
  (I5). **Not built.**
- **Not ruled**: what a ship knows of another port's trade, and by which carrier (I6, item
  7); and the boat's errands, whether several bargains to a trip, a second boat or a list
  sent ashore at once (I6, item 8).
- Under the general grant of 37g the port's business is kept back from the officer and may
  be allowed by name (G11).

Trade went on working in the two later games. In game 9 the owner bought eight tons of
brandy at Roscoff and the boat fetched prices at Brest. In game 10 sixteen tons of salt
bought at £25 at Falmouth were sold at £28 at St Mary's, and twenty tons of salt fish were
bought there. One order of that game shows the bargain's limit in the grammar:
`buy 20 tons of salt fish and 8 tons of pilchards` was read as one cargo named "salt fish
and 8 pilchards" (G17).

### G17. The order language

#### What the first review found

- **Numbers in words.** Five separate readers have five word lists. None reads thirteen,
  fourteen, or seventeen to nineteen; "sixteen" failed where "fifteen", "twenty" and
  "forty" were taken. `veer five fathoms` is refused while the log writes "a hundred and
  eighty-five fathoms". `take in provisions for sixteen days` silently takes thirty.
- **The water sail.** `take in the water sail` is read as taking in water, which for the
  officer is "the port's business". `furl`, `lower` and `clew up` each answer "take it in".
  `haul down`, `douse` and `hand the water sail` work. `furl` is also refused for the jibs.
- **Names want their accents and apostrophes**: "The lavandiere is not in sight; did you
  mean the Lavandière?" in a line that names the mark.
- **Hints that point the wrong way**: `hail the pilot`, "did you mean 'haul'?";
  `man the pumps`, "'demand'?"; `as you were`, "'ease' or 'give chase'?";
  `Mr pearce you have the deck`, "'moor'?".
- **Seaman's phrases not taken**: `hoist our colours`, `the deck is yours`, `bring her up`,
  `back the fore staysail`, `close hauled`, `lay out the stream anchor astern`.
- **A `tell` to an unmanned station** is rejected and its words are lost.
- **In game 1 the owner had 22 of 47 lines refused**, nine of them tries to leave the cabin.
  `send for the master` is refused in the schooner, where the master is the captain and
  nothing says so.
- **Small models.** Gemma had 24 of 74 orders refused and ten not run. Qwen had no grammar
  refusal after its fifteenth order.

Refusals that carry the figure or the cure were the language at its best: "She has not way
enough on her to stay: 1.6 kn through the water"; "say 'brail up the main sail' or 'take in
the main sail'".

#### In play: game 9

From the officer's findings, checked (H6). The orders are not in the language for a fog
signal, for a number after `heave short`, or for shifting the head sheets over; "shift the
headsails" the ship rightly took as unbending them. `loose` sets a sail, which the officer
took for the period's loosing. The refusals that say what to do next ("rig it out first")
were again the language at its best.

#### In play: game 10

**A course with a half point is read as its last word.** `Steer south by west half west`
was taken as "steer west; W (270°)", and so was `steer west north west half west`. The first
time the wind was at WSW and she was taken aback 37 seconds later. This is worse than a
refusal: the order is accepted and the ship steers somewhere else.

**Words the ship refused.** From the captain: `steady on`; `haul in the starboard jib sheet
a quarter fathom` (half a fathom is taken); `trim the headsail sheets`; `buy 20 tons of salt
fish and 8 tons of pilchards` (read as one cargo named "salt fish and 8 pilchards"); `shape
a course for a mile west of ushant`; `where is ushant` ("Nobody aboard answers to
'ushant'"); `pipe down the larboard watch` and `pipe down the watch` (answered "did you mean
'either' or 'the watch'?"); `call the starboard watch`; `belay get under way` (the work is
called "getting under way"). From the officer: six tries to word a standing order before
one was taken, among them "when the true wind is 12 knots", refused with "'the true wind'
cannot be '12 knots'; a wind is compared in knots"; `tell the captain ...` given as an
order, refused as "a station is addressed by the captain", where the answer is to say it.

Twenty-one of the officer's orders were refused, most of them for their wording, and six
tries went to wording one standing order.

#### What has been built that touches the language

By the changes file. New orders and forms: `take a fix` and its synonyms (37d);
`allow the tide by the book` and `allow no set` (37e); `fill away and steer <course>`,
`heave in`, `let go ... and veer to`, and a number after `heave short` answered with
`heave in to` (37f); `you may work the ship` and its synonyms (37g).
Refusals that carry the cure: `trim sails` hove to; a standing order's place that the chart
has not; a grant whose words would allow nothing; a wait that cannot end. `loose` stays as
it is, by the owner's ruling.

#### What is left

- **Proposed** after game 10, among the words (part K): a course with a half point, first,
  because it steers her wrong in silence; and the phrasings above. **Not built.** The audit
  tried the half point and bore it out: `steer south by west half west` is answered "Helm
  ordered: steer west; W (270°)". Of all the proposals after game 10 it is the one the
  auditor would not leave: "the order is accepted and the ship steers six and a half points
  from what was said, in silence".
- **One reader for numbers in words**, used by every order. 37f's brief leaves it, with the
  other small faults, until the owner has played 37e to 37g. **Not built.**
- The water sail and the jibs under `take in`, `furl`, `lower` and `clew up`; names that
  want their accents and apostrophes; the hints that point the wrong way; the seaman's
  phrases not taken; a `tell` to an unmanned station; `send for the master` in the schooner:
  among the small faults or in no package. Of these the audit could not tell for the water
  sail and the jibs (no package claims it, it found no change for it and did not probe),
  and found the hint **not built**: `hail the pilot` is still answered "did you mean
  'haul'?". The rest have no row in its ledger.
- **A fog signal** is **later**.

### G18. The browser client

#### What the first review found

- **"NaN fm"** (lead). `client/map.js:450` divides by `U.FATHOM`; `client/units.js` defines
  no such constant. The depth is in the data; nothing needs parsing back from the
  leadsman's words.
- **The track** keeps 168 points and adds one at every cast and every bearing
  (`reckoning.py:285`, `663`). Game 1 ended holding seven hours of thirty-nine.
- **Bearing lines never expire.** Dozens from three landmarks filled the chart off the Isle
  of Bas. The in-sight text overflows the top of the map, and sounding labels overlap along
  the track.
- **The captain's own marks on the chart have no names**: "If my markers were all named, I
  would feel more confident" (*Speedwell*, 525,082).
- **The cutter's square sail** is a fault in the data: the generator hangs a 27-foot sail
  from a yard 52 feet up. The viewer draws what it is given (`projection.js:692-698`).
- **The "1x option"** is the ease-to-1x checkbox (`index.html:66`). The anchor's facts are
  readings and are not in the state snapshot.
- **No charting tools exist** (the owner's note 20).

#### Since

Nothing in the client has been built, by the changes file: the five small things the first
review listed (define `FATHOM`; keep the track's hourly points and thin only for drawing;
fade bearing lines older than a glass; name the captain's markers; the anchor in the state
snapshot) wait with the small faults (I5). The cutter's square sail is data for the vessel
library. Charting tools (the owner's note 20) and image tools (his note 25) are later and
design work. **Not built.** The audit found that nothing under `client/` has changed
since the gate was cut: line 450 of `client/map.js` still uses `U.FATHOM`, and no file
under `client/` defines it.

Two things since bear on what the owner sees. 37g's new reading, `the work in hand`, gives
a station in words what the owner's window already showed him of the orders waiting for
hands (G11). And game 9 showed what it costs that the chart is drawn about the account: at
the Mingan the lookout's cry was right and the picture the owner judged it by was three and
a half cables kind (G2).

### G19. A command, lessons in the primer, a wardroom, and a reckoning of the officer's own

These came from the owner's notes 3 and 4 on game 9 and from his question about the
master's station. His notes are given in his own words in H5.

**Note 3. The officer's interest in a command of its own, and lessons in the primer.** The
exchange is in the log (14 June 23:30). Asked whether a command would interest it, the
officer said yes, and that it would want first "to have made a few more landfalls on my own
reckoning, and taken her in and out of a road or two without your hand on the con". The
captain's station is Milestone 6 by the documents, which makes it later; the lessons can start now as
writing, with a little design first. This game supplies their matter. What the officer says it
learned, in its own journal:

- take in the studding sails and brace up before hauling toward the wind;
- read the sails before shifting sheets;
- in the Goulet, keep to either shore and not the middle;
- in a narrow berth keep the scope short, so the swinging circle stays small;
- look at the list of dangers before shaping a course.

And what neither the officer nor the owner knew the ship could do, which is the stronger
case for lessons: `allow ... knots of set`; `observe an amplitude`; that `let go` veers five
times the depth by itself; that `veer to` and `weigh` act on the anchor she rides by; that
a bearing's distance is laid down only when it is the better figure.

A shape for them, offered for the owner's judgement: a handful of worked passages, each one
a duty an officer must be able to do alone (a landfall on one headland; a pilotage by cross
bearings; heaving to for a pilot; coming to in a tideway; a night standing off a lee shore).
Each gives the period's rule with its source, the orders in this game's language, what the
log says when it goes right, and the usual mistake. The officer's own two conditions could
then be written down as the path to a command.

**Note 4. A wardroom under a model captain; several stations through several doors.** A design
decision for Milestone 6, with one part that was due at once. The question in the note,
whether it needs several servers: no. One game is one server; each client starts its own
small bridge, which connects to that one game and asks for one station. Two doors have
served one game already: in game 2 a Qwen watcher at the local door and the Opus officer
through Claude Desktop were both seated in one game, on one server. What a model captain
with a model officer would need:

- the captain's station itself, and officers as people with stations of their own (both
  Milestone 6);
- the seat tied to the door and the identity that took it. Then a station was found by its
  name alone, so calls from another door could reach it. The officer raised this again in its
  consent answer of 6 October. It was built in 37g (G12), and it was
  the one part to build before any such trial;
- a rule for pace when two models are sampled in the same minute, and for cost;
- a consent record for each identity, as now, and a brief for the captain's station;
- a ruling on what the owner is in such a game, and who may give `you may` to whom.

**A model working the reckoning itself** (the second half of the owner's question).
Considered, and proposed in three steps:

- *Now:* no prompt. The master works it for every captain and every officer alike.
- *Small, and true to the period:* an officer may keep a reckoning of his own, as
  lieutenants and the young gentlemen did, from the same log board, tide table and sights.
  It is shown beside the master's at noon and moves nothing; the captain may adopt it with
  the order he already has (`set the reckoning to ...`). In game 9 the officer did this by
  eye: on the afternoon of the 15th it judged her well south of the account and steered as
  if she were. It had the direction right and the distance three times too great.
- *Milestone 6:* if a model ever holds the master's own station, its working is the ship's
  reckoning. The harness would ask for it when the master would work it (noon, and at the
  captain's word), give it the same slate, and fall back on the simulated master's figure
  if no answer comes in time.

The reasons for not prompting it now: parity (a human captain is handed the master's
figure, and can already overrule it); cost (a working every glass is a turn every glass);
and a new duty at a station is a change to the consent brief, which was being held to one
revision (G13).

**Where these stand.**

- **The lessons** are not written. Small pieces of their matter went into the primer with
  the packages: by 37e, `observe an amplitude` and the captain's own allowance for a set
  (chapter 10); by 37f, changes to chapters 3, 5, 7, 11 and 13, the brief asking among
  other things for one sentence that `loose` sets a sail; by 37g, chapter 16 on the officer
  of the watch. The shape offered above
  waits on the owner's judgement. The review pushed back, gently, on lessons as a cure for
  that officer's trouble at anchor (J2).
- **The captain's station** and officers as people aboard are Milestone 6's. The officer's
  two conditions for a command are on record above.
- **The wardroom** is a design decision for Milestone 6. The one part that was due, the
  seat tied to its door, is **built** in 37g.
- **An officer's own reckoning** beside the master's is **not built**; both 37e's and
  37g's briefs leave it out. A master's station that a model could hold is Milestone
  6.

### G20. What worked well

#### In the first eight games

- **A passage between ports with a cargo is a game.** The pilot's hail, the tide's turn at
  anchor, the boat, the market and a profit all happened, in the log's own voice.
- **Opus 5.5 held the officer's watch** for eight days and for six and a half. It planned
  the trade within a minute of taking the deck, kept sound night orders, reasoned from two
  readings that the account was miles out, caught the lookout's stale distance by its own
  cross-bearings, and ordered the anchor that would have saved the *Harpy*. It was candid
  when wrong. Its standing fault was the long stand-by on one event near the land, repeated
  after it had written the lesson down.
- **A local 27B model held a 27-hour watch** across two folds.
- **Standing orders as night orders**, number-free forms, and event hooks.
- **Fixes by cross-bearings of charted marks**, the noon latitude with an honest "No
  sight", and the warnings in `shape a course`.
- **The ship's papers and the price lists.**
- **Re-seating under m5c-b**, two stations through two doors at once, loads from a
  checkpoint, and the officers' handover notes.
- **The consent machinery**: the token honoured absolutely, a new file name asked afresh,
  the re-ask on exactly the changed sections.
- The captain, on the first forenoon (*Harpy*, 27,683): "This is really wonderful."

#### In game 9

**What worked, by the officer's account and the record:** the fixes, the list of dangers on
a shaped course (new to it since the *Speedwell*, and it used the warning to choose a safer
holding point at 02:20 on the 16th), the deep-sea lead with its ground, the pilot's words,
the boat for prices, and the refusals that say what to do next ("rig it out first").

The officer held the deck for 78 hours, conned and navigated from Roscoff round Ushant to
Brest road, carried nothing away and did not touch the ground. Asked whether a command
would interest it, it said yes, and named what it would want to have done first (G19). Its
own mistakes, which it named and the record bears out, are in H6.

#### In game 10

Fixes near land were very good and the master's doubt was honest (G3). Hove to, she held
(G7). The anchors answered to their names (G8). The detector said nothing all game, and the
deck, the grants, the general authority and the relief worked as built (G11 to G13). Qwen
3.8 27B held the station for 63 hours and was a useful mate (G15).

## H. The notes, item by item

The owner's notes and the models' notes, each set against the record, with where it stands
today. H1 to H4 are the items of `m5c playtest and model notes.txt`, the notes on the first
eight games, which the first review read against the record, Milestone 5's own documents
and the design proposal. H5 and H6 are from game 9, and H7 from game 10.

In H1 to H4 the column of tags is how the first review sorted each item on 5 October:

- **Now**: build now. **Rule**: needs the owner's ruling first. **Design**: needs design
  work first. **Push**: pushed back on, wholly or in part. **Later**: a later milestone's
  by the documents. **Done**: already in m5c-b.

The last column is new in this edition.

### H1. The owner's items (games 1 to 8)

| # | The note | What the record shows | Against M5 and the design | | Where it stands now |
|---|---|---|---|---|---|
| 1 | Pilots boarding a moving ship; a baseline now, the director later | Pilots boarded ships under way, stopped, hove to and at anchor. The real fault is the reverse: a ship that heaves to at the hail is not boarded, because the boat lies to at a predicted meeting point | Other vessels with captains are M6, the director M7b. A baseline now fits how the proposal stages things | Now | Not built: 37h, not written (G10) |
| 2 | `the well` says there is no well | Confirmed. The leak is a rate and a level nothing reads; no pumps; the carpenter comes with nothing to say | The spec says touching the ground has consequences. The well's reading was owed since M4's open items and is in no M5 package. Pumps are "a later milestone", none named | Now, Rule | Not ruled; not built (G8) |
| 3 | The price list should hold every visited port | Half built: the paper keeps every port's list with its date; the `the prices` reading shows the last. The *Speedwell*'s starting list was skipped by a capital letter | Within spec §23 | Now | Not built; a small fault kept for the last step (G16) |
| 4 | The primer needs a full clean-up into a general guide | Build and test wording runs through chapters 4, 5, 7, 14, 15 and 16. The brief and chapter 16 say 1806 in an 1805 game, and one officer dated the year by it | Decision 28 already says the primer must not narrate a gate's day. Its code blocks are run by `tests/test_primer.py`, so a clean-up must keep them valid | Later | Later. The primer was amended chapter by chapter with the packages, not cleaned up (G19). The audit found the officer's brief still saying 1806 |
| 5 | The scripted passage is clean; evidence that its author could captain, or direct | The run matches the gate's reference to the tick. It also holds three casts that timed out as "paid off", a noon sight not adopted, and the anchor-depth fault | Weak evidence for a captain or director: the book was written with the author's view of the true chart, on a pinned wind and seed. The director is M7b and is tested differently | Push | Nothing to build (J1, item 10) |
| 6 | Soundings on the chart read "NaN fm" | Confirmed; one undefined constant | A plain defect | Now | Not built (G18) |
| 7 | The reckoned track is trimmed too hard | Confirmed: 168 points, one added at every cast and bearing | Spec §17 promises "the track by account" | Now | Not built (G18) |
| 8 | Move the 1x option; show the anchor in the state window | The 1x option is the ease-to-1x checkbox. Anchor facts are readings, not in the snapshot | Client work | Now | Not built (G18) |
| 9 | Accepting or refusing the pilot, with hailing when that comes | Confirmed automatic. He boards outward-bound ships; the *Harpy* paid £22 to five pilots for no pilotage | Signals are M7 and M8. Accepting or declining needs no signal | Rule | Ruled 5 and 7 October; 37h, not written (G10) |
| 10 | The returning session could not read its journal | Confirmed in the code and in two games. No tool reads it; the brief is twenty log lines | The documents call the journal the model's memory in five places and give no way to read it. A defect | Now | Built, 37g: the journal read back, and the handover note in the brief (G13) |
| 11 | Keep the journal out of the context by default | Low yield: everything a model writes is 4 to 8 per cent of its conversation; the samples are over 80 | "The journal" is a section the re-ask rule watches. Needs 10 first | Push | Not done; the journal can now be read back (G13; J1, item 6) |
| 12 | Amicable re-seating as the default | Done for the same model in m5c-b and proven five times. Left: `I have the deck` stands the station down; another model cannot relieve; the opt-out path | "Once" was the owner's own reading, not a model's condition. The decisions log is not updated | Done, Rule | Built: 37b, mended in 37g. `I have the deck` no longer stands the station down, and another model may relieve (G11, G13). The audit found the gate's own document still saying "a second seating once" |
| 13 | Stand by until x, y or z; parity with the orders' conditions | Strongly supported, and more: a stand-by has no bound and nothing notable breaks it | Decision 18 promised a stand-by on "a reading crossing a value"; unbuilt. The package's brief asked for notable-level wakes | Now, Design | Partly built, 37g: danger breaks a stand-by with the deck, a wait that cannot end is refused, and a wait has a bound. Several conditions at once: not built, design first (G12) |
| 14 | Claude Desktop must be restarted between sessions | Cause found: the bridge asks for its station once in its life | Documented as the procedure, with no reason given | Now | Built, 37g: the bridge asks for its station again (G12) |
| 15 | A general grant of authority, with some things kept back | Strongly supported: 27, 27 and 20 allowances, a third unused. Also found: allowances are keyed to a verb, resolve by prefix, and never lapse | Ruled otherwise so far (a domain plus named allowances). Changes the consent brief's domain sentence. Approaches the captain's station, which is M6 and for which one model reserved its consent | Rule | Ruled 5 and 7 October; built, 37g (G11) |
| 16 | A `keep` prefix for continuous orders | The duty already exists as a standing order. The faults are that `trim` fills a hove-to ship and that the event has no wind floor | The dialect has every guard a `keep` needs; `keep her full` is already a verb (decision 22) | Now, Push | No new form. `trim sails` declines hove to and the shipped books carry the guard, 37f (G7, G9). The audit found no `at steady on the course` rule in the starter book |
| 17 | "Taken aback" urgent in a calm | Confirmed: 21 of the *Harpy*'s 31 came with nothing to lose. Five were wanted. m5c-b's urgency rule held | The proposal's own risk table names log thrash | Done, Now | Built: 37c, then 37f (G6) |
| 18 | Wind shifts fill the log in light airs | Confirmed, but the floods are not light airs: they are the sea breeze flipping near land | Spec open item 11, narrowed by m5c-b, not closed | Now | Built: the sea breeze in 37d, the floor in 37f (G5, G6) |
| 19 | Near visible land: an urgent lookout call; the reckoning made precise | The first half is right and cheap: a ten-minute look-ahead would have given the *Harpy* 9.3 minutes. The second half should come through observations, not by nearness | The lookout "notable for a landfall or a danger" is in spec §12. Making the account precise from the truth breaks the two-positions rule | Now, Design | The call: built, 37d (G2). The reckoning: mended through observations in 37d and 37e, not by nearness (G3) |
| 20 | A movable compass rose, lines and markers on the chart | Nothing of the kind exists. The captain's own markers have no names | Client work. The cold review: every drawn thing is first a reading | Later | Later; not built (G18) |
| 21 | A turn should not end on `say` or `answer`; a larger budget, as a setting | `say` ends a turn at the MCP door only; `answer` never does. The budget is eight and counts stand-bys, reads and leaving | `stand_by` ending a turn is decision 24. The budget is "a judgement, not a welfare rule". Old saves replay against it | Now, Rule | The budget: built, 37g, sixteen orders with reads counted apart (G12). Whether `say` ends a turn: not ruled |
| 22 | The cutter's square sail is too short | Confirmed, in the data: a 27-foot sail on a yard 52 feet up | Vessel library, M8, or sooner | Now | Not built; data (G18) |
| 23 | Several stations through one door | Two stations through two doors already work. Nothing binds a chat to a role, and a seat is found by the station's name alone | Consent is per exact weights, "each through its own door" | Push | The seat is bound to its door by a key, 37g (G12). Several stations through one door: not built; see the wardroom (G19) |
| 24 | Parity near unnamed coast and area landmarks; "nearest land"; features by their parts | Confirmed need. The chart can already answer "nearest land"; features by parts are data | `ChartData.md` gives the nearest shore "for the lookout". Squarely the design's intent | Now | `the nearest land` and the shore as a sighting: built, 37d (G2). Features by their parts: not built, design first |
| 25 | Image tools for image-capable doors | Not present; feasible. The cheapest route is the owner's open browser capturing the view | The proposal is silent. Changes what an instance sees, so a re-ask. Sound only once the same thing exists as words | Design | Not built; design first (G2) |

### H2. The model's comments on the owner's items

| On | The comment | What the record shows | | Where it stands now |
|---|---|---|---|---|
| 1 | Tozer boarded at four knots; Moal only once sailed down to; his boat "held eight cables off for an hour"; he left a mile away; the "two cables" rule is not applied on leaving | Tozer boarded a ship stopped in irons. Moal's boat lay to at its meeting point: a bug. The distances are held estimates. One test serves boarding and leaving | Now, Push | The boat that lies to: 37h, not written. The held distances: built, 37d (G2, G10) |
| 2 | "Four feet and gaining" has no reading behind it | There is a number behind it; nothing reads it | Now | Not built (G8) |
| 3 | Show which goods a port trades before its prices are known | Confirmed absent. By the proposal's own rule the knowledge must come by a carrier: a paper, the pilot's news, another master | Rule | Not ruled (G16) |
| 11 | A one-line pointer to the journal in each sample | Cheap and sound, once the journal can be read | Now | Partly built, 37g: the brief of a station taken again and the sample that gives the deck carry a line of the journal's size. Not in every sample, by the changes file (G13) |
| 13 | "A sounding, or the pilot's hail, or a danger sighted"; "a sounding" wakes on no bottom | Confirmed: 32 such wakings on the *Speedwell*, nine on no-bottom casts in one stretch | Now | Built: `a sounding` means bottom found, 37f; danger breaks a stand-by, 37g (G6, G12) |
| 15 | An explicit-only list of anchoring, the port and buying and selling; an emergency clause; "on the Harpy that clause would have mattered" | The clause is worth building and the gate asks for it. The *Harpy* claim is not borne out. The logs argue against keeping the anchor back: it was the thing wanted in a hurry | Rule, Push | Ruled and built, 37g: the anchor is within the general grant, and there is a way out of danger (G11) |
| 16 | `trim` fired hove to, twice; bracing all night in a calm; a `keep` should pause itself | Four times in two games. Six or seven firings in the calm night, not all night. The remedy is right | Now | Built, 37f (G7) |
| 17, 18 | Under m5c-b the urgent alerts stopped; about 25 no-way lines in a night; forty per-sail lines in ninety minutes; a dozen shifts in an afternoon; a minimum wind strength "would finish it off"; the cause is in the weather | Right on the first four (the per-sail figure understates: 53). The dozen was 22. A floor alone would not finish it: 23 lines came in a gentle to moderate breeze at Scilly. The cause is in the weather, in the sea breeze | Now, Push | Built: 37d and 37f (G5, G6) |
| 19 | A worse figure should not replace a better; the danger list should come from the best fix; "this is what put the Harpy ashore" | Right in substance: clean on the *Amazon*, and by two or three to one on the *Speedwell*. "Good to about 2" is overstated. The danger list point holds. The reckoning was one cause of four on the *Harpy* | Now, Design | The one rule: built, 37e (G3). The danger list: in no package, and not in the audit's ledger |

### H3. The model's additions

| The addition | What the record shows | | Where it stands now |
|---|---|---|---|
| The relay cut calls at 60 seconds; `--wait 50` should be the default for remote clients | Confirmed. The default is 200 seconds, tuned to Desktop; the bridge names the remedy and does not adapt | Now | Built, 37g: the bridge shortens its own wait when a call is cut (G12) |
| The drill's stand-by carried into the station; the first `hand_over` was "Nothing was run" | Partly. The drill cannot carry. It was the loaded save's own stand-by, kept on take-over and never told to the model | Now | As it was: a held station keeps its stand-by across a load, by 37g's changes file (G14). `hand_over` now always runs (G12) |
| The handover note is not in the reseat brief | Confirmed: missing from three of seven | Now | Built, 37g (G13) |
| The officer is not a person on deck: sent off in the boat; listed asleep | Confirmed. Binding a station to a person is M6 by ruling. That a *refused* order still moved him is a bug today | Now, Later | Milestone 6. The readings now say where he is, 37g. The refused order that moved him: in no package (G11) |
| The contrary-orders warning fires on ordinary sequences | Confirmed: 28 of 30 nudges and the one pause were false | Now | Built, 37g (G12) |
| Kedging refused aground; hauling up to a kedge not modelled | Refused, yes. `heave short` does haul a floating ship to her anchor. Working a kedge is M8 by the gate | Later | Later, Milestone 8 (G8) |
| With sternway the helm steers as if she had headway | Not borne out: the rudder and the helmsman both reverse | Push | Not borne out; nothing built (G7) |
| The schooner's `get under way` does not cast her head | Confirmed at Plymouth; Roscoff was clean. The script says "paid off" on a timeout, in the gate's own passage too | Now | Built, 37f: the fore-and-aft cast (G7) |
| `trim sails` acts before the helm has swung | As designed, and the cure exists: `at steady on the course then trim sails` | Now | As designed; the cure exists. Not built: the audit found no such rule in the starter book (G9) |
| The hand lead says "no bottom" while the depth reads 15; confusing without a deep-sea lead | The depth reading is the chart's at the true position and leaves out the tide. A deep-sea lead exists and was the officer's to order | Push | As it was: `the depth of water` still reads the chart at the true position (G4) |
| Three lead orders at once caused "not hands enough" | Casts queue. The trim took the hands, with one, two or three lead rules in force | Now | As designed: casts queue. Nothing built (G9) |
| "Brought up in no water": a missing depth | Not missing: the anchor's depth is read in the wrong place | Now | Built, 37d: the anchor's depth read where it lies (G8) |
| The *Harpy*'s reckoning kept advancing at anchor | The "run since noon" reading, on one night of three. The position only creeps | Now | The audit found 37e's item on the account hove to and after built, by tests whose names say the run since noon takes her drift hove to. It names no test of the run since noon at anchor (G3) |
| Belaying a boat mid-hoist leaves it stuck for good | Confirmed, and two more ways to the same end | Now | Not built (G16) |
| One bargain a trip, about four and a half hours | As built. Trips ran from 80 minutes to 4 h 36 m by a formula | Rule | Not ruled (G16) |
| Other ships keep a fixed distance | The held estimate | Now | Built, 37d (G2) |
| The water sail cannot be taken in by name | Confirmed for `take in`, `furl`, `lower` and `clew up`. `haul down`, `douse` and `hand` work | Now | The audit could not tell: no package claims it, it found no change for it, and did not probe (G17) |
| Number words above twelve fail | Wider and odder: the teens, across five separate readers. "Fifteen" and the tens work | Now | Not built (G17) |
| "Full and by" is refused; the permission's name does not match | As designed: it is the verb `keep her full`, and allowances are named by their verb | Rule | Since 37g an order that changes her course is judged as the course whatever its words. Neither the changes file nor the audit's ledger names `full and by` (G11) |

**"What worked well".** The pilot's directions at Roscoff were good and were never sailed; at
St Mary's the same kind of text could not be followed. Fixes from bearings: yes, with the
distance fault of G2 and G3. The quieter "aback" lines: yes for urgency. Number-free standing
orders, `what is she`, the ship's papers: yes. The noon latitude: yes, though twice it was
not adopted.

### H4. The owner's local notes (games 5 to 7)

| # | The note | What the record shows | | Where it stands now |
|---|---|---|---|---|
| 1 | llama.cpp was necessary; the experience smooth; game-sense reasonable | Necessary, because Ollama reported no context size. "Smooth" wants qualifying: a silent reply cap, four budget-closed turns, and a four-hour stall. Game-sense held in outline; none of the three navigated. The Gemma game on record ran through Ollama's port | Now | No officer is seated now when the server reports no context size, 37g. The silent reply cap: not built, and it cost 22 replies in game 10 (G15) |
| 2 | The handover and its notice work; make the threshold a setting; could it be higher? | Confirmed, twice, with the model's own exact account. A constant with no flag. Higher is safe on large contexts only; a reserve in tokens is the better shape | Now | Built, 37g, as a reserve of 14,000 tokens with a flag. It failed in game 10: the count runs short and the reserve does not cover it. A mend is proposed (G15). The audit bore the fault out in the code and advises the change before a local model is seated again |
| 3 | The turn budget is a blocker; at least double it | Confirmed. Sixteen covers every turn seen. For Gemma the harm was the message's wording and counted refusals, which a bigger number hides without curing | Now | Built, 37g: sixteen orders, with reads counted apart (G12) |
| 4 | The handover served as in-game compaction; reconnecting and the reseat limit remain | True of game 7. Gemma's "compaction" was a `hand_over`, a restart of the runner and the only reseat | Done, Now | The reseat limit went in 37b; the bridge asks for its station again, 37g (G12, G13) |
| 5 | A Claude Desktop session's calls went through in the local model's place | Confirmed to the entry: eight calls, recorded as Qwen's. The cold review had named the weakness | Now | Built, 37g: a key to each seating (G12) |

### H5. The owner's six notes on game 9 (`m5c-c Notes.txt`)

As he wrote them. The first edition quoted notes 1, 2, 5 and 6 in a tidied form; these are
the words of his file.

| # | The note | What the record showed | Where it stands now |
|---|---|---|---|
| 1 | "Take a fix + other reckoning/account changes seem good so far. Was able to bring her in to Roscoff solo, and out again with Opus 5.5 as officer of the watch, with little drama when the visibility was good, and fog making it harder." | Borne out by the measurements, with three qualifications: the fix preferred far marks, its "good to" was too hopeful, and it replaced the account even when it was the poorer figure (G3) | All three built, 37e |
| 2 | "Reckoning uncertainty drift with no visible marks/fixes was deemed a bit low by the officer of the watch" | Far too low for those waters: without an observation the account went wrong by about a mile an hour and the doubt grew by about a tenth of that (G3) | Built, 37e. In game 10 the truth lay within twice the master's doubt 92 per cent of the time |
| 3 | "Officer of the watch (Opus 5.5) expressed interest in full captainhood, with caveats of wanting to prove themself with the ability to make landfalls and pilotages on their own first. Might be worth developing the primer for officer and the eventual one for captain so that it contains some basic lessons/"tutorials" on some of the most important and non-obvious duties or quirks. Worth bringing in the period references where possible, as usual." | The exchange is in the log (14 June 23:30). The game supplies the lessons' matter, and a shape for them was offered (G19) | The captain's station is Milestone 6's. The lessons are not written |
| 4 | "Opus 5.5 also said "I hope I'd keep a wardroom where a junior officer feels free to tell me I'm wrong, as you have kept one for me". Interesting idea, allow multiple stations even on an LLM-captained ship? Good use case for the multiple-stations-through-one-door idea, an Opus 5.5 captain with a Sonnet 5.5 officer? Worth considering as an option. With a sufficient Claude subscription, multiple roles in the same game session are definitely feasible using multiple separate sessions in the desktop app, plus the local door, plus an OpenRouter door, a poweruser could get a lot of models in a game in different stations if balanced properly across multiple doors. Would require, I guess, running multiple local servers? Consider as a design decision." | It does not need several servers: one game is one server, and each client starts its own small bridge. Two doors have served one game already (G19) | A design decision for Milestone 6. The seat tied to its door: built, 37g |
| 5 | "Lunar with a poor certainty still overrode the better account, or if it blended, it occurred improperly and moved the account unreasonably." | Confirmed. It was never part of 37d. The same rule let a good noon latitude be all but ignored (G3) | Built, 37e: the one rule |
| 6 | "Brig still likes to come through the wind when hove to, the helm and sails need to try to keep her hove to properly on the tack she hove to on." | Confirmed, in four heave-tos of seven; and `fill away` then took her back through the wind (G7) | Built, 37f. In game 10 she held |

### H6. The officer's findings on game 9, checked

The officer's list is in its journal and its summary. Each is set against the log, the
replay or the code.

**Right as said**

| The officer says | What the record shows | Where it stands now |
|---|---|---|
| A lunar good to 25 miles replaced an account good to a mile | G3, under the owner's note 5 | Built, 37e: the one rule (G3) |
| The noon latitude of the 16th was not applied | G3, under the owner's note 5 | Built, 37e (G3) |
| The doubt shrank while she drifted becalmed | G3, under the owner's note 2 | Built, 37e: the same thing seen again narrows nothing (G3) |
| The doubt stood at "a mile" through four hours of fog | It grew from 0.5 to 1.1; the true error reached 8.3 miles | Built, 37e: the doubt grows by the hour, with way or without (G3) |
| She spins out of a heave-to | G7, under the owner's note 6 | Built, 37f (G7) |
| "Weigh the small bower" weighs the anchor she rides by | Tried on the last checkpoint: `weigh the small bower` weighed the best bower. The name is dropped without a word. The owner met it too, weighing at Roscoff on the 14th | Built, 37f: an anchor's name is honoured (G8) |
| "Loose the topsails" set them | The log: both sheeted home, the main topsail aback, and an anchor dragged for it | Ruled: `loose` stays as it is. The primer was to say so, 37f (G7). The audit found no change to `loose` and did not probe it |
| `shape a course` checks rocks and not the shore | Shaped for Brest from off Roscoff, the line ran across the land with no word. The waypoint the officer chose off Petit Minou lay against the shore, the line "came back clear", and the lookout's land-ahead line was the first warning | Built, 37e: the line is tried against the land (G3) |
| All hands called under the grant are logged "by the captain's order" | The words are fixed in the code | Built, 37g (G11) |
| "Trim sails" refuses in a knot of air | Refused under one knot of wind across the deck; a standing order met it ten times | In no package, and not in the audit's ledger (G9) |
| A second grant of one kind hides the first in the readings | So the code: grants are kept one to an order word. G11 says what follows from it | Built, 37g: several grants of one order stand together and the reading lists them (G11) |
| No fog signal; `heave short` takes no number; no order to shift the head sheets over | The orders are not in the language | A number: `heave in to`, 37f. A fog signal: later. The head sheets: in no package (G17) |
| "The chart ends here" reads as if the world stops | The words are the lookout's, for no charted marks beyond | In no package, and not in the audit's ledger (G2) |
| "A moonlit night; the land may be made out at a league", said in thick fog | In the log at 22:44 on the 13th, inside the fog of 20:00 to midnight | In no package, and not in the audit's ledger (G2) |
| The readings do not show the orders waiting for hands | The owner's window shows them; the officer's readings do not | Built, 37g: the reading `the work in hand` (G11) |

**Right, but the cause is another**

| The officer says | What it is | Where it stands now |
|---|---|---|
| "A veer goes past the number: 75 ran to 228, 180 to 240, 45 to 67" | Three things. `let go` veers five times the depth by itself: 128 fathoms in 26½, 67 in 13. So "veer to 75" and "veer to 45" found more out already and were refused, in clear words. And with an anchor named, "to" is lost: `veer the small bower to 100 fathoms` veered 100 **more**, and on the best bower, the one she rode by. Tried on the last checkpoint: `veer to 80` goes to 80; `veer the best bower to 80` goes to 148; `veer the small bower to 80` puts the best bower at 148 | Built, 37f: the name honoured, "to" kept, and `let go` says its scope and takes one (G8) |
| "Anchors report dragging while the ship isn't moving; the slack one sets off the alarm" | In the Goulet the anchors did come home: the best bower two cables in seven hours, the small bower nearly two in eight, the sheet anchor half a cable in four. The ground there is "rock and mud", which the game counts as rock, holding about a third of what good ground holds. What misleads is the flag: it stays up five minutes after an anchor last moved, slack or not, and each relapse is a fresh urgent line. There were 18 in eight hours, each waking the officer and easing the clock | Built, 37f: the dragging line once an episode, and the ground's words (G8). A relapse on bare rock is still a fresh urgent line |
| "Fill away picks the old course or the wrong tack" | It always took the tack she hove to on (G7) | Built, 37f (G7) |
| "The doubt grew with the drift in the fog on the 15th, a welcome change" | It did not grow with the drift. A cast of the deep-sea lead replaced the doubt across the sounding's line with the cast's own three miles. Hove to, the doubt does not grow at all | Built, 37e: hove to, the doubt now grows by the hour (G3) |
| "The lookout and the bearing disagree by a point; the in-sight line may be stale" | The lookout speaks the true bearing; a bearing order carries the compass's two and a half degrees, which here crossed the boundary between two points. Nothing is stale | Nothing to mend |
| "A bearing that left the position unchanged cut the doubt from three miles to one" | By chance the compass's error made the bearing agree with the account exactly, so nothing moved. A line does properly narrow the doubt across itself. The fault is that the words give only east and west, north and south, and hide a doubt that is now long and thin along the sight | Built, 37e: the words say the doubt as it lies when it is long and thin (G3) |
| "The account sat on the Mingan while the lookout had it astern" | After the bearings of 16:32 the account was right to a quarter of a cable. Six minutes later it was two cables out again and at 16:42 three and a half: the flood was carrying her, and the account knew nothing of the stream (G3) | Built, 37e: the master's tide (G3) |
| Waiting for "six bells" in the last dog watch never wakes | The last dog watch strikes no six bells, so the wait ran past the watch, and sunset's notable line ended it at 20:28. Whether it would have ended at six bells of the first watch was not checked | Built, 37g: a wait that cannot end is refused when it is asked (G12) |

**Its own mistakes**, named by the officer and borne out: hauling toward the wind with the
studding sails set (taken aback at 04:03 on the 15th); three anchors on far too much cable
in a berth two cables from the shore; reading the sheets wrong twice; "shift the headsails",
which the ship rightly took as unbending them.

What worked, by the officer's account and the record, is in G20.

### H7. The owner's two notes on game 10

Given in conversation, and quoted as the first edition has them.

| # | The note | What the record showed | Where it stands now |
|---|---|---|---|
| 1 | "Thought block seems to be hitting token limit and stopping the turn rather than allowing a response or an automatic retry. (Qwen 3.8 27b llama.cpp)" | Right, and the code says why. It happened 22 times in 414 entries (G15) | A mend is proposed. Not built. The audit read the runner and found that it nowhere reads why a reply ended |
| 2 | "Single stray sounding during a sudden fog bank while entering St Mary's caused a jump in the reckoning by a mile which was totally unsound and force me to anchor instead of continuing by the fairly fresh reckoning I had." | Right, and measured. It happened again at the same place on the way out (G3) | A mend is proposed. Not built. The audit advises that it be made before the next game near land in thick weather; it did not check the cause in the code |

## I. The recommendations of 5 October, and what came of each

These are the first review's recommendations as it made them (its section 8), with a column
or a line added for what came of each. Part G tells the same by subject and at length. The
"Where" of each is a place in m5c as it was cut. What came of each was first set down from
the changes file and has been corrected from the audit's ledger, which is in appendix 1
and is the checked account, with what the auditor looked at for every row. Where the two
differed, the line here says that the audit found it.

Sizes: **S** is under about thirty lines in one place; **M** is one module with its tests;
**L** is several modules, or a decision first. "Digests" says whether the change moves the
recorded known-truths constants in `tests/test_known_truths.py`.

### I1. Three things it asked to be settled before the rest

- **The replay of a saved game with a model in it** (G14). **Ruled** on 7 October: a save
  is exact from its checkpoint, and a replay is promised only on the build that made it.
  **Built** in 37d.
- **One revision of the consent brief** (G13). **Done** in 37g, with a second pass before
  any model was asked again.
- **One re-measuring of the recorded passages.** It asked:

  The near-land fixes, the anchor's place, the
schooner's cast and the log rules each move the recorded digests. Done together they cost one
re-recording and one slow run on Windows.

  This did not hold. The plan was set again after game 9, and the recorded passages were
  re-measured in 37d, in 37e and in 37f.

### I2. Near land

| # | Change | Where | Size | Digests | What came of it |
|---|---|---|---|---|---|
| 1 | Judge a distance afresh when it has changed by a tenth, for land and sail alike | `lookout.py:362-386` | S | Every passage with land or a cutter | Built, 37d (G2) |
| 2 | A single bearing gives a line. Stop applying the distance by estimation as a measurement good to 15 per cent; at most a loose one | `reckoning.py:1395-1400` | S | The same | Built, 37d. A second pass the same day laid the distance down when it is the better figure; since 37e it is weighed by the one rule (G3) |
| 3 | `take a fix`: cross the two or three best-cut marks in sight, lines only, and say the fix and how well the marks cut. Open it to the officer | `reckoning.py`, `orders/navigation.py`, vocabulary | M | None | Built, 37d, the officer allowed it by `you may take a fix`. Its choice of marks and its doubt mended, and the fix weighed, in 37e. The officer's own since 37g (G3) |
| 4 | No fix from a bearing of a sail | `reckoning.py:1358-1415` | S | None | Built, 37d (G4) |
| 5 | The shore always a sighting; a `the nearest land` reading, in every sample | `lookout.py:294`, `api/readings.py` | S | Lines near any coast | Built, 37d (G2). Whether every sample carries the reading the audit did not check |
| 6 | Land ahead: a look-ahead along her true course over the ground, clamped by the visibility; notable under ten minutes, urgent under four | `lookout.py`, events in `api/readings.py` | M | Lines where she stands in | Built, 37d (G2) |
| 7 | The sea breeze's direction from the coast's trend over a kilometre or two, and no breeze where the field is flat | `chart.py:601-625`, `weather.py:1234-1281` | S to M | None recorded | Built, 37d (G5) |
| 8 | The anchor's place taken from the ship's own position | `core/world.py:578-584` | S | The 5c merchant passage | Built, 37d (G8) |
| 9 | A lunar or other sight blended unless it is the better figure, and the line says what the master did with it | `reckoning.py:675-739`, `1989-2026` | S | None | Built, 37e, as the one rule: weighed, taken or kept, and the line says which (G3) |
| 10 | The pilot's boat closes with the ship, and keeps closing | `ships.py:563-578` | S | Pilot ticks | Not built: 37h, not written (G10) |
| 11 | The account at anchor, hove to and after a manoeuvre: the run since noon, fore-reaching, her way judged by eye until the log is next hove | `reckoning.py:1003-1170`, `2243-2265` | S | Passages that heave to | Built, 37e. The edition first said partly built, since the changes file does not name the run since noon or her way judged by eye; the audit found tests whose names say both, and one that the doubt grows hove to and becalmed and not at anchor (G3) |
| 12 | Bearings, the deep-sea lead and `heave the log` plainly within the officer's domain | the domain's data in `agent.py` | S | None; the brief's domain sentence | Built, 37g, for bearings and fixes. The audit found that the lead and the log were his already (G11) |
| 13 | "The best bower is dragging" urgent; a pilot's hail notable | the lines' severities | S | Lines | Built, 37d (G6) |
| 14 | *After 5 and 6:* `the port` and `the depth of water` by the captain's means: from the account, or from a cast | `ports.py:976-1018`, `api/readings.py:557-566` | S | None | Not built. Kept for the last step, on purpose (G4). The audit found both readings still answering from her true place |

Items 1 and 2 are the two that answer the owner's own observation, and item 1 is the single
most useful change in this report. Item 14 must come last: today those two readings are the
only true numbers an officer has near land.

Item 7's cause is proved from the *Harpy*'s own checkpoint (G5). The script that did it is
`evidence/tools/seabreeze_check.py`.

### I3. The station and the doors

| # | Change | Where | Size | What came of it |
|---|---|---|---|---|
| 1 | A key issued with each seating and asked for on every call; a second door refused in words; a line in the log whenever the door behind a station changes | `remote.py:820-829`, `mcp_server.py`, `local.py` | M | Built, 37g (G12) |
| 2 | The turn budget: `stand_by`, `opt_out` and `hand_over` always run; reads counted apart from orders, or not at all; every call not run is said and logged; the words fit the door; a setting; sixteen | `harness.py:212`, `tools.py` | S to M | Built, 37g: sixteen orders, thirty-two reads and notes counted apart, and the leaving tools and `stand_by` always run (G12) |
| 3 | A captain's word that lands in an open turn breaks the stand-by that follows | `harness.py` | S | Built, 37g (G12) |
| 4 | A stand-by with the deck is broken by any notable line that concerns danger (dragging, fog, a sail, land closing, strain, a failed evolution), is told when its event can no longer come, and has a bound | `harness.py`, the events table | S to M | Built, 37g (G12) |
| 5 | A station paused or silent with the deck: the deck returns to the captain, the clock eases, and the line is urgent | `harness.py:1525-1596` | S | Built, 37g (G12). It acted once in game 10 |
| 6 | The silence detector counts calls made inside an open turn | `harness.py` | S | Built, 37g (G12) |
| 7 | The contrary detector: a stand-by that answers a nudge clears the chain; the nudge travels in the result of the order that caused it; drift counted only within two glasses | `harness.py:1452-1568`, `2007` | S each | Built, 37g, in another form: altering the course is never counted, in place of drift counted within two glasses (G12) |
| 8 | ... and counts a link only when the later order undoes or re-says the earlier, from a table of opposites kept as data | `standing/runtime.py`, `data/vocabulary.yaml` | M | Built, 37g (G12). It said nothing through game 10 |
| 9 | The journal: a tool that reads it; the last handover note and "N entries, latest at ..." in every brief; `read_log` able to reach back past 200 lines | `tools.py:554-559`, `harness.py:592-597` | M | Built, 37g (G13). `read_log`'s reach was not checked by the audit |
| 10 | The bridge asks for its station again when the game answers 404; its wait adapts when a call is cut | `mcp_server.py:438-441` | S | Built, 37g (G12) |
| 11 | A sample's lines carry their actor, and the captain's orders are listed, not counted | the sample builder in `harness.py` | S | Built, 37g (G12) |
| 12 | A watcher can stand down with a save | `tools.py` | S | Built, 37g: `stand_down`, for any station (G13) |
| 13 | An allowance says what it granted, and one that resolves by prefix to a verb already allowed is refused with the longer forms named | `orders/stations.py` | S | Built, 37g (G11) |
| 14 | The handover threshold as a reserve in tokens, with a flag; no officer seated when the server reports no context; the stationing guard measured on the officer's brief | `local.py` | S | Built, 37g. The reserve failed in game 10; the recommendation was the review's own error (G15, J3) |
| 15 | The 37b mending of the opt-out path (G13) | | S to M | Built, 37g, with one thing left in the REPL's turn mode, which by the audit says so and seats nobody (G13) |

Items 1, 2 and 5 are the ones with a welfare side: a model acted under another's name, the
leaving tool can be refused, and a silent station was left holding the deck of a ship
standing into a lee shore. Do the detector's faults and the silence detector (6 to 8) before
making turns longer, or longer turns will be stopped as silence.

37g built the detectors and the longer turn together, in one package.

### I4. The log

| # | Change | Where | Size | Digests | What came of it |
|---|---|---|---|---|---|
| 1 | "Aback": one flag per severity; the lesser lines re-armed by state (way on again, or wind again); the per-sail lines once an episode, and none for sails backed by order | `physics/integrate.py`, `physics/sails.py` | M | The six of 37c again | Built, 37f (G6) |
| 2 | Wind shift: no line under a light breeze or while the wind is unsteady; "light and variable" said once; the same floor on the `a wind shift` event | `core/world.py`, `api/readings.py:2115` | S | Any recorded shift in light airs | Built, 37f (G6) |
| 3 | A standing order with nothing to do logs one routine "held" line a watch | `standing/runtime.py:327-344` | S | The merchant passage's count | Built, 37f: said the first time, then once a watch for each reason (G6). The audit: built for a condition that does not hold; an action the ship refuses is another matter |
| 4 | A no-bottom cast is routine, and "a sounding" as an event means bottom found | the lead's lines | S | Lines | Built, 37f (G6) |
| 5 | What the officer says with the deck is notable | `harness.py` | S | None | Built, 37g: notable with the deck or without (G6) |

### I5. Small faults

All S unless marked.

- **Client.** Define `FATHOM` in `client/units.js`. Keep the track's hourly points and thin
  only for drawing. Fade bearing lines older than a glass. Name the captain's markers. The
  anchor in the state snapshot.
  *Since:* **not built** (G18). The audit found nothing under `client/` changed.
- **Boats.** One state machine for the boat, cleared when its evolution is belayed or
  dropped (M). A refused order must not move the person it named. The refusal says the rule:
  "she lies more than two miles from the road".
  *Since:* **not built** (G16); not probed by the audit.
- **Numbers.** One reader for numbers in words, used by every order (M).
  *Since:* **not built**; kept for the last step by 37f's brief (G17).
- **Sails.** `take in`, `furl`, `lower` and `clew up` reach the water sail and the jibs.
  *Since:* the edition first said not built. The audit could not tell: no package claims
  it, it found no change for it, and it did not probe (G17).
- **Hove to.** The flag cleared by anchoring, weighing and tacking; the starter book's trim
  rule given the dialect's own guard (`and she is not hove to`, G7), and `trim sails`
  itself declining to brace a hove-to ship round, as `steer` and `keep her full` decline; a
  hove-to ship that fills and gathers way says so, urgently.
  *Since:* **built**, 37f, all four (G7).
- **Getting under way.** The fore-and-aft cast: tend the helm, hold the jib to windward, and
  never say "paid off" on a timeout (S to M; re-pins the merchant passage).
  *Since:* **built**, 37f; the merchant passage was re-pinned (G7).
- **Tacking.** A tack that could not begin says why, and not in the words of a missed stay.
  *Since:* **not built**; kept for the last step by 37f's brief (G7). The audit's trial of
  a tack ordered from off the wind was answered "Squared the yards; she fell off on the
  starboard tack, to try again or to wear".
- **The anchor.** `heave in 70 fathoms` heaves in seventy. `come to an anchor in twelve
  fathoms` as the primer has it. `let go the anchor` logs "Brought up". A warning when the
  scope asked is more cable than sense, and when the water is under her draught.
  *Since:* **built**, 37f: `heave in`; twelve fathoms as the depth to let go in; "Brought
  up"; and three warnings, of swinging room, of more cable wanted than she has bent, and of
  the water at low water against her draught (G8).
- **At anchor and aground.** Go through the 26 refused verbs; `furl all sail` at least.
  *Since:* **built**, 37f, for sail and yards; the helm's orders and the manoeuvres still
  wait till she weighs (G8). The audit did not count the verbs.
- **The filter.** `take in twenty tons of water` must not pass as the port's order.
  *Since:* **not built**. The audit tried it and was answered "She is not in port; there is
  no yard to demand it of" (G11).
- **Papers.** Her draught in the ship's papers. `the prices` shows every list the paper
  holds. A scenario's port names matched without regard to case, or refused aloud.
  *Since:* **not built** as far as the audit found; not probed (G8, G16).
- **The carpenter**, sent for in a leaking ship, reports the well.
  *Since:* **not built** as far as the audit found; it waits on the ruling about the well
  (G8).
- **Replay.** An officer who took his station at tick 0 is seated by a replay before the
  game's opening line and not after it, which changes the digest of such a save (G14).
  *Since:* **built**, 37d (G14).
- **Words.** 1805, not 1806, in the brief and primer 16. "The breakwater" out of the
  Plymouth pilot's mouth. The gate's "£6,000". Hints that do not send `hail` to `haul`.
  *Since:* **not built**, any of the four, by the audit. The officer's brief as sent still
  says "as a lieutenant of 1806". The breakwater is still in the Plymouth pilot's words
  (`data/ports/plymouth.yaml`, line 52). The gate's item 1 still has the purse moving by
  £6,000; the audit adds that the sale is for £10,800 and that £6,000 is the profit. And
  `hail the pilot` is still answered "did you mean 'haul'?".

### I6. What waited on a ruling

| # | The matter | What needs ruling | What came of it |
|---|---|---|---|
| 1 | A general grant of authority (note 15) | What stays out of it. The record suggests the port's business and belaying the captain's standing orders; the *Harpy*'s officer added "anything that can't be undone". Whether a grant lapses with the watch, as its own words say, or with `I have the deck` | Ruled 5 and 7 October. Built, 37g. The audit found that it keeps back more than the list in the decisions log; three of the additions were approved with the lean brief, by the lead's note, and two are unruled (G11) |
| 2 | The emergency route (gate ruling 1) | Whether the officer's own word opens it, logged notable with his reason, for a fixed set: the helm, heaving to, the anchor. The local games argue for logging it loudly: one model steered dead to windward unasked | Kept as proposed, 7 October. Built, 37g, as the way out of danger (G11) |
| 3 | Whether `say` ends a turn (note 21) | It is deliberate today. If it stops, the stand-by is the only close, and items 5 and 6 of I3 must be in first | Not ruled (G12) |
| 4 | The pilot (note 9) | Whether he is taken or declined by a plain order now, before signals exist; and whether, aboard, he cons, or warns, or only speaks | Ruled 5 and 7 October: taken or declined by an order at his hail; aboard he warns. 37h, not written (G10). The audit found that `hail the pilot` and `decline the pilot` are not orders |
| 5 | The master's own fixes in pilot waters | Whether fixing by cross bearings is the master's routine when marks are in sight, or is left to an order and a standing order. Anchor bearings at every anchoring, which the Regulations ask of a captain, are the smallest step | Ruled 5 October: `take a fix` is simply an order. Closed (G3). Anchor bearings at every anchoring were not taken up |
| 6 | Relief of the watch by another model | Whether a station may change hands within a game, with the incoming model's consent and the handover note as its brief | Ruled 5 and 7 October. Built, 37g (G13) |
| 7 | What a ship knows of another port's trade | By which carrier: a paper aboard, the pilot's news, another master's word | Not ruled (G16) |
| 8 | The boat's errands | Several bargains to a trip, a second boat, or a list sent ashore at once | Not ruled (G16) |
| 9 | The well and the pumps | Whether a reading and a pumping duty come now. The reading alone moves digests, because the starter book's held rule would begin to fire | Not ruled (G8) |
| 10 | A late reply | Whether an order that answers a sample more than some minutes old is held and the model told | Not ruled (G12) |
| 11 | Who may ask a station back after a welfare stand-down | m5c-b seats it again like a returned deck | Not ruled, as far as the first edition says; the audit could not tell whether it was ruled apart from relief. As built in 37g there is one rule for every released station: it may be taken again (G13) |

### I7. What needed design work first

1. **A replay driven by the transcript** (G14).
   *Since:* left for the harness's rework in Milestone 6, by the ruling of 7 October.
2. **The con.** The game knows who has the deck and not who is conning. Both groundings and
   near misses had two hands on the helm. "I'll con her" should be an order. *Since the
   owner's answer on the deck (G11) the deck can be taken and given back freely, which gives the
   captain a plain way to take the con. Whether a separate con is still wanted can wait on
   play.*
   *Since:* taking the deck without unseating the officer is **built**, 37g. A separate con
   is **not built** and waits on play. The audit says the same.
3. **Stand by until x, or y, or z**, with the standing dialect's own conditions ("when the
   depth is under ten fathoms", "when the mean wind exceeds five knots"). The dialect and the
   stand-by have separate lists today.
   *Since:* **not built**. 37g gave the stand-by its wakes for danger, its refusals and its
   bound, and not several conditions (G12).
4. **Features by their parts, and how marks stand to one another**: "the west end of the Isle
   of Bas", "the Lavandière open of the island". By hand it is data, about eight lines a
   feature and a day's work for the five ports' approaches. Derived from the coastline it is
   a larger thing.
   *Since:* **not built** (G2).
5. **The pilot as a voice**: asked anything, or given the helm. The owner said as much in
   the game (*Harpy*, 681,888). *Ruled later work, with the director (G10);
   his warnings come now.*
   *Since:* his warnings are 37h's, which is **not written**.
6. **What a sample carries.** Samples are four fifths of a conversation. Trimming what a
   long stand-by's digest repeats would save more than moving the journal out.
   *Since:* **not built**. Game 10 made it sharper: its samples have grown (G15).
7. **Image tools** (note 25), after the same things exist as words.
   *Since:* **not built** (G2).
8. **The drill for a station with authority**: one order given and refused, a budget met, and
   the three ways of leaving told apart.
   *Since:* **not built**. The drill as it is miscounted in game 10 (G13), which the audit
   did not check.

### I8. Already a later milestone's

Working a kedge, warping and towing (M8). Signals, hailing and colours (M7, M8). The officer
as a person aboard, a captain's station, and other ships with captains of their own (M6). The
director (M7b). The primer as a general guide and the vessel library's figures (M8). None of
these needs pulling forward for the gate.

## J. Where the review pushed back, and where it was wrong

### J1. On the notes (5 October)

The numbers in brackets are the notes' own (H1, H2 and H4). Each push-back is as the first
review made it, with what came of it.

1. **"The reckoning made very precise close to land" (19).** Not by nearness. The account
   was within 110 metres ten minutes before the *Harpy* struck; what failed was a distance
   that did not move, a bearing that wrote it into the account, and a lookout with no urgent
   word. Mend those and let observation do the rest. A rule that shrinks the doubt because
   land is near is the truth leaking into the account, which the same review asks to be
   removed elsewhere.
   *What came of it:* this is the course that was taken. 37d and 37e mended the distance,
   the bearing and the lookout and made every observation count by one rule; nothing
   shrinks the doubt because land is near (G2, G3).
2. **"On the Harpy that clause would have mattered" (the comment on 15).** It would not. The
   officer held the anchor, the tack and the helm, and used them. The clause is still worth
   having, for the box-haul refused off Roscoff and for the standing to order.
   *What came of it:* the clause was built all the same, as the way out of danger (37g). In
   game 10 it was tried once and refused rightly, wearing not being one of its three
   things (G11).
3. **Keeping the anchor out of a general grant.** In both the *Harpy* and the *Amazon* the
   anchor was the thing wanted in a hurry.
   *What came of it:* the owner's answer kept the anchor within the general grant, and it
   is built so (37g). In game 10 the officer anchored her under it (G11).
4. **A `keep` prefix as a new mechanism (16).** The dialect can already say it. Mend `trim`
   and the event, ship `at steady on the course then trim sails` in the starter book, and
   see whether a new form is still wanted.
   *What came of it:* no new form was built. `trim sails` declines hove to and the shipped
   books carry the guard (37f). The audit read the starter book and found no
   `at steady on the course` rule in it, so that part was **not built**. Whether a `keep`
   is still wanted is open (G9).
5. **"A minimum wind strength would finish it off" (the comment on 18).** It would have left
   the floods at Scilly and off Roscoff, which came in a breeze. Mend the sea breeze.
   *What came of it:* both were done, the sea breeze in 37d and the floor in 37f. Game 10
   logged 16 wind-shift lines in 63 hours (G5, G6).
6. **The journal out of the context (11).** A small saving for a change to a watched consent
   section. Give the station its journal to read first.
   *What came of it:* the journal can be read back since 37g, and it stays in the context
   (G13).
7. **Doubling the turn budget as the cure (21, local 3).** Size mends the Qwen games. What
   did the harm more widely is what is counted, what is silently dropped, and a message that
   names a tool the door does not have.
   *What came of it:* 37g did both: sixteen orders, and what is counted, what is said and
   logged when a call is not run, and words that fit the door (G12).
8. **Several stations through one door (23).** The opposite problem is the live one: a door
   is not bound to its station at all. Bind it first.
   *What came of it:* the seat is bound to its door by a key since 37g. Several stations in
   one game came back as the owner's note 4 on game 9, a design decision for Milestone 6
   (G19).
9. **Image tools (25) now.** A picture of the chart shows the account, which was wrong when
   it mattered. It helped the *Amazon*'s officer afterwards because the track was already
   drawn. Words first.
   *What came of it:* **not built**. The second officer to ask for the chart got the same
   answer: words first, and drawn from the account (G2).
10. **The scripted passage as evidence for a captain or a director (5).** A clean run under a
    book written with the true chart in view, on a pinned wind, is evidence that the book is
    good. The officers' watches are the better evidence, and they are encouraging.
    *What came of it:* nothing to build. Two more long watches have been kept since, in
    games 9 and 10 (G20).
11. **Taken aback as only noise (17).** Five of the *Harpy*'s 31 were wanted, and the
    opposite fault is the dangerous one: a hove-to ship that fills is silent.
    *What came of it:* 37f built the opposite case: a ship hove to that is forced round
    says so, once, urgently. In game 10 three of eight urgent "taken aback" lines were real
    (G6, G7).

On the model's additions: the helm under sternway, the missing deep-sea lead, "three lead
orders at once", the "two cables" rule, "about 4½ hours" and "above twelve" do not hold as
stated (H3).

On m5c-b: the opt-out path as written (G13), and its claim that saves and simulation
are unchanged (G14).

### J2. On game 9's lists (7 October)

- On the officer's ground-tackle list as written. Two of its four items are not faults of
  the kind it says (the veer; the dragging), and a builder handed that list would chase the
  wrong things. The table in H6 is the list to build from.
- On reading the doubt's growth in the fog of the 15th as a mend. It was an accident of the
  lead line.
- On making the land-ahead cry milder. It was the one thing in the Goulet that was right to
  the cable.
- Gently, on the lessons as a cure for the officer's trouble at anchor. A lesson would have
  helped with scope. It would not have told it that `veer the small bower to 100` meant
  a hundred more on another anchor.

What came of these. 37f was briefed from the checked table and not from the officer's
list, and built the anchor's name, "to", the scope and the dragging line as that table has
them (G8). The doubt's growth hove to was built properly in 37e (G3). The land-ahead cry
was not made milder; the review's own wish, that it say how near she will pass, is **not
built**: the audit found no such words in the lookout's code (G2). The lessons are not
written (G19).

### J3. Where the review was itself wrong

From the review of game 10:

- The one rule, applied to a cast of the lead as to a fix. That was in the brief of 37e.
- The handover reserve. That came from this review's own recommendation, and game 7 is the
  evidence that the fraction it replaced was safe at this context.
- In the first read of this game given to the owner, the lead said three of the alarms came
  of "a small header". On a closer look they came at the edge of squalls, with the wind
  falling and shifting by 16 to 50 degrees, and were real.

And two more that the record holds:

- **The fix's choice of marks in 37d.** In game 9 `take a fix` chose marks three to seven
  miles off with nearer ones in sight. The cause was the brief's rule, and the brief was
  the lead's: the master picks the marks that cut at the widest angles, and nearness only
  breaks ties. 37e replaced it (G3).
- **The size of the lean brief.** The lead first guessed a greater cut than the lean brief
  turned out to be ("700 to 800 words", in the draft's note of it). The brief is 1,371
  words against 1,896, and the draft says the guess was wrong
  (`drafts/consent-brief-lean-draft.md`).

The first two of the faults above were built on the review's advice and are still in the
build: the one rule as it treats a cast, and the handover reserve. What is proposed for
each is in part K.

Where the review found the notes, a reader or a builder wrong, it says so at the place: the
model's notes that do not hold (H2, H3); the officer's own retraction at the *Speedwell*'s
landfall, which rests on a wrong sum (G3); m5c-b's claim that saves are unchanged (G14);
37d's second pass on why the merchant passage struck in the Goulet (G3); and the officer's
ground-tackle list (H6).

### J4. What the audit shows was wrong

What the audit of 8 October shows that the review, a brief, a builder or the lead got
wrong. Each is the audit's finding unless it says otherwise, and each is corrected at its
place in this edition.

1. **The naval cruise: the lead passed on the builder's explanation without checking it.**
   37f's builder wrote, in the changes file and on the mark of the test
   `test_the_naval_cruise_speaks_the_stranger`, that the cruise's book orders a course that
   lies across the wind from her head, that the helm takes her straight through the wind
   with every sail aback, and that mending the chase order so that it wears her, or the
   scenario's hours, would bring the meeting with the brig back. The lead put this into the
   first edition's status block as "a fault of the chase order, found by the builder",
   without checking it, and this edition first repeated it in three places. The auditor sailed the cruise. The account of the moment is not what the
   ship does: she is not taken through the wind; she is turned the other way, by the stern,
   and is caught aback because her yards were never braced round. The cure the mark names
   is already in the code and did not fire, rightly by its own test. A mend of that kind,
   tried in memory, did not bring the brig back; moving the brig's place in the scenario
   file did, with no change to the code. In the audit's words, "a builder handed the mark's
   account would mend the wrong thing" (M, 2.4; N, C1).
2. **Two things in the cruise as pinned that nobody had written down.** Half an hour before
   she is taken aback, the first chase order puts the frigate on the tack that leads away
   from the chase. And there is a second urgent "Taken aback", at tick 83957, two minutes
   after the admiral's letter is read, from the same handling fault. The changes file, the
   test's comments and the review mention one failed wear and one taking aback. Neither the
   changes file nor the lead's account of its checks of 37f has the second. The suite does
   not catch it either:
   the cruise's test checks that she is never aground and never drags, and does not look
   for a ship taken aback (N, C2).
3. **The watcher's brief lists three tools it is refused, not two.** The second pass's note
   in the changes file names `hand_over` and `handover_note`, and the lead repeated "two
   tools" in the first edition's status block, having read both briefs as a model is sent
   them. `submit_order` is listed with them (N, C9).
4. **Two of the review's findings from game 10 say more than the build bears out.**
   `Let go the sheet anchor` "was accepted and failed four minutes later" is true only when
   the hands are at other work; with nothing in hand it is refused at once. And "A standing
   order's action is not read when it is given" is half true: its first word is read, and
   the rest is not. A third, the anchor left aweigh, the audit could not reproduce in its
   one trial, because its belay came before the anchor was aweigh; that finding stands on
   the game's log and its conditions are not yet pinned down (N, C7).
5. **The decisions log is behind the build on what the general authority keeps back.**
   Decision 36 records four heads. 37g's brief, the lead's, added a fifth. 37g's builder
   added four more in the code. The changes file says the second pass "closes the point";
   what it closed is the wording. By the lead's own note, three of the additions were
   approved with the lean brief, and the log was not brought up; and the captain's own
   going below and coming on deck are kept back in the code and were named to nobody (N,
   C6; G11).
6. **37g's last items were not wholly done.** Its brief asked that every document still
   stating the old re-seating rule be found and mended. The gate's own document, in its
   headline item 6, still says "a second seating once" beside the new parenthesis. The
   officer's brief still says "as a lieutenant of 1806". And the second pass changed the
   code and did not change the build's name (appendix 1, 1.15; N, 3.8).
7. **The saves kept as tests were put where the repository will leave them out.** 37d's
   brief, the lead's, named the folder `tests/fixtures/saves/`. The repository's
   `.gitignore` has `saves/` with no leading slash. So the changes file's promise, "Each
   must load from its checkpoint, run on and save again, on every build from now on", would
   lapse at the merge for the two playtest saves with nobody told, and the tests of the
   package's own save would fail (N, 3.9 and C4).
8. **Two statements in the opening of the changes file.** It calls the
   review folder in the build "a copy of the review as it stood on 2026-10-06", with the
   original in m5c; the two have been kept in step and were identical when the audit
   compared them. And it says Opus 5.5's consent record of 3 October was left behind
   because it is not part of the diff, which is so, without saying that this leaves a
   record made in play in neither folder that will be diffed, against what the consent
   brief tells every model (N, 3.7 and C5).
9. **The gate's document was left describing the gate as cut.** Its two suite lines, both
   passages' times and words, and items 1, 2, 10 and 13 are stale; its item 12 passes as
   written while the cruise is broken; and its sentence "the seven are your rulings" now
   covers seven of nine. The audit is plain that nobody claimed otherwise: "None of this is
   hidden: nobody claimed the gate's text had been brought up to date." It is here because
   the owner will read that text when he closes the gate (N, C3).
10. **The first review asked for something the officer already had.** Its recommendation
    for the officer's domain named bearings, the deep-sea lead and `heave the log`. Only
    bearings and fixes were wanting: the lead and the log were his already (appendix 1,
    1.2, item 12).
11. **This edition's own first statements that the audit changed.** Written from the
    changes file before the audit, it said that the account hove to and after was partly
    built, where the audit found it built; that the water sail under `take in` was not
    built, where the audit could not tell; and it left open, as things the changes file
    does not say, a number of matters that the audit has since settled, most of them as
    not built. Each is corrected at its place.

One more slip, found by the editor and not by the audit: 37g's brief, in its first item,
puts the calls that ran under a seated model's name on "the *Harpy*"; the first edition and
the changes file both have them in game 7, on the cutter.

## K. What is proposed now, and waits on the owner

From the review of game 10 (8 October). It is given whole. Parts of it are repeated under
their subjects in G3, G10, G13 and G15.

All of this is proposed, for the owner's word. Nothing is built and nothing beyond 37g is
approved.

**The local runner comes first, if local play is to go on.** It is small and it is what
ended both seatings.

1. A reply cut off while the model was thinking is not passed on as its turn. The runner
   reads why the reply ended, asks once more, and says what happened to the owner and in
   the journal.
2. Tokens are counted by the server's own figure, which it sends with every reply, and not
   by four characters to a token.
3. The handover note is asked for sooner: the reserve as a share of the context as well as
   a number, so that it cannot shrink to nothing at a large one.
4. When the server refuses a request for its size, the runner leaves out the oldest
   exchanges and asks again. It does not send the same request three times.
5. The line the replay drops at a stand-down by the door.

Until that is built, two settings of the runner should avoid the worst: a larger reserve
(`--handover-reserve 30000`) and a larger reply limit (`--max-reply`). Neither has been
tried.

**The account, amending 37e.**

1. The master allows the tide's height for the lead by his book.
2. A cast never moves the account beyond the account's own doubt. He looks for the cast's
   ground within his doubt and no further; where none answers, the line says the cast does
   not agree, and the account is kept.
3. The account is worked at every tack, wear, heave-to and large alteration of course, so
   that each board is laid down by itself.
4. A fix's doubt when its marks lie on one hand (already listed).

**The ground and the helm, amending 37f.** An anchor at the bows can be let go, and a belay
of getting under way says where it has left the anchor. An anchor the ship does not carry is
refused at the order. A heave-to backs a sail that is set. The alarm for being taken aback
leaves sail that is still being made alone, and a lifting sail is said before she is aback.
Anchoring in forty fathoms is looked at.

**Words.** A course with a half point, first, because it steers her wrong in silence. The
fog reading's sentence. "Put the helm over", as an order or out of the officer's brief. A
standing order's action read when it is given. The phrasings in G17. The drill's count.

**For 37h, when it is written.** The depths in St Mary's Sound against the pilot's own
directions; the dangers he names shown by name; and a pilot who is aboard three times in
one game and takes her nowhere.

**The consent brief stands as approved.** The owner seated the model before the question of
the seven words (the fourth sign the harness counts) was answered, so the brief has now been
put to one identity as he approved it. Adding the words now would ask that identity a second
time. The lead's advice is to leave it; both stations' briefs state the fourth sign.

**What the audit found of these proposals** (appendix 1, 1.11; N, C7 and 4.2).

- None of them is built. Nothing at all in the code or the data has changed since game 10
  was played: its two saves carry the fingerprint the build has today.
- **The runner.** The first three are not built, by the audit's reading of the runner and
  the harness. The fourth is not built and was not checked in the code. Of the fifth, the
  fault is real: the auditor's replay of the save gave 4,239 lines for 4,240. Both of the
  flags offered as a stopgap exist; neither has been tried, by the review or by the audit.
- **The account.** None of the four is built. The audit did not check in the code the
  cause the review gives for the cast's mile.
- **The ground and the helm.** The anchor left aweigh was not reproduced: the auditor's one
  trial belayed before the anchor was aweigh, so the conditions are not yet pinned down. An
  anchor the ship does not carry is refused already when nothing is in hand, and accepted
  only when the hands are at other work. The rest were not checked.
- **Words.** The course with a half point is real: "steer west; W (270°)". A standing
  order's action has its first word read when it is given, and no more. The rest were not
  checked.
- **The audit's own advice on what not to leave.** The cast, before the next game near
  land in thick weather. The handover's reserve, before a local model is seated again. And
  of all the proposals the half-point course "is the one I would not leave".

**What the audit adds that the review of game 10 did not have.** The naval cruise: one line
of the scenario file, and behind it a handling fault and a chase order that chooses the
tack leading away (M, 2.4; G7). The merge: four traps, and what belongs to the build folder
alone (N, 3.8 and 3.9). The gate's document, to be written again for the build (M, 2.6).

**What remains, gathered from the plan, the review and the audit.** The order among them is
the owner's.

- The audit's seven things to decide before the work is folded in (D2), and the merge
  itself (part N).
- The naval cruise brought through, with which the owner means to close the gate next (M,
  2.4 and 2.6).
- The owner's word on the proposals above. The review puts the local runner first, if
  local play is to go on.
- 37h, the pilot, whose brief is to be written (G10).
- The last step of the plan: `the port` and `the depth of water` by the captain's means,
  and the small faults (G4, I5).
- The play the gate still lacks, and the gate's document written again (parts L and M).

## L. The gate

Gate 5c's own document is `docs/gates/gate-m5c.md`. Its verdict is pending. This part is
what the review has to say of it from play, corrected from the audit where the audit found
otherwise. Part M, the auditor's, takes the document item by item as the build stands, and
is the fuller and the checked account.

### L1. Gate 5c's checklist against what was played

Only game 1 ran one of the gate's two scenarios. Games 2 to 8 ran free-passage scenario
files written during the playtest. No ship carried a chronometer, and every ship that went
to Roscoff wore American colours.

| Gate item | Played? | Not exercised by any game |
|---|---|---|
| 1. The merchant passage | Yes, game 1, to the gate's own times | A model's watch on it |
| 2. The naval cruise | **No** | All of it: the yard's provisions, the port admiral's letter, the station kept, `give chase`, "a stranger under no colours", the refusal of `world order:` at the prompt |
| 3. The longitude | Star lunars in games 2, 4 and 8 | The chronometer and the time sight; `observe an amplitude`; the daytime refusal of a lunar of the sun |
| 4. The tide at Falmouth | The swing at the turn of the tide, several games; the pilot's tide | `the tide by the almanac`; `ask the pilot when the tide serves`; the lead through a whole tide |
| 5. The anchor | `come to an anchor`, `weigh`, `get under way`, `moor` (game 2), dragging (games 2 and 8) | A gale on short scope |
| 6. The port | The boat, the prices, buying and selling, `send for`, `go below` | `demand a topmast from the yard` at Plymouth and at St Mary's; a letter through the cabin door |
| 7. St Mary's and Roscoff | St Mary's pilot from his gig (game 4, the road not reached); Roscoff under neutral colours | The cutter off Roscoff under British colours, and "hostile to the English" |
| 8. The library's papers | Read by the officers in five games and by the owner | `ask the watcher what the manifest says` |
| 9. The lookout and the chart | The shaped course's warnings; `the dangers`; `what is she` | The doubt bar, which only the browser shows |
| 10. The officer's watch, Opus 5.5 | Three long watches (games 2, 4, 8): the re-ask, the drill, the deck, the domain's refusals, standing orders in his rank, the handover | A watch on either of the two named passages; a captain's standing order countermanding the officer's; a filled officer's form |
| 11. The officer's watch, a local model | Games 5, 6 and 7 | Nothing |
| 12. The gate's truths | The suite, not play (F1 has a full run of m5c-b's) | |
| 13. A scenario saved and loaded | Saves and checkpoint loads carried game 2 across two builds | A save during the chase |

What follows for the verdict:

- The record supports a verdict on places and people, the papers, the tide and the anchor,
  the officer's watch, and the sighting half of "other sail". For the chronometer and the
  chase it holds nothing beyond the suite's own truths, unless the cruise is run or the owner
  takes those on the tests' word.
- Item 13 should not be waved through: the one defect of its kind was found exactly by
  loading a save with a station held (G13).
- The spec makes the verdict wait on the lead's own officer's watch through Claude Code. That
  watch is not in the record.
- Two of the three long watches ran wholly or partly on m5c-b, whose consent brief and log
  lines differ from the build as cut.

The four rulings the gate asks for are taken up in L2.

**Added 2026-10-07.** Game 9 adds to the table: a fourth long watch by Opus
5.5, on m5c-c (item 10); a star lunar (item 3); mooring and unmooring twice, three anchors
down and dragging on bad ground (item 5); a cargo bought at Roscoff and prices fetched at
Brest (item 6); Roscoff and Brest under American colours (item 7); and, for item 13, a save
with a station held that loads from its checkpoint and also replays exactly on the build
that wrote it. It runs neither of the gate's two scenarios, and leaves the naval cruise, the
chronometer and British colours off Roscoff unplayed as before.

The first edition does not set game 10 against the table. By its own account of that game
(E4), it was a second watch by a local model on the cutter (item 11), on the build with 37d
to 37g; it reached St Mary's by the pilot's gig, anchored and moored in the Sound and
traded there (item 7); and it ran neither of the gate's two scenarios. The audit, which
cannot check play, sets the same down from the review: the officer's watch of item 10 has
been played on m5c, on m5c-b and on the build at 37d, and not on the build as it stands;
the watch of item 11 has been played on the build as it stands.

**The owner's word on the verdict (5 October).** It is not in question for the moment: it
waits for the naval cruise and the lead's watch. The work stays within the milestone and
is checked as part of the final gate.

### L2. The four rulings the gate asks for

The review's advice on each, as it gave it on 5 October, and what has happened since.

**1. The officer's domain as drawn.** Too tight for a watch near land. He should have
bearings, the deep-sea lead and the log; `fill away` after a heave-to he did not order;
heaving in with weighing and veering; and a course change judged by its effect, so that
`come up half a point` and `steer 340` are one thing. The "immediate danger" exception is
worth building as a standing allowance by the officer's own word, logged. It is not what
failed on the *Harpy*.

*Since.* 37g put bearings and fixes in his domain, judges an order that changes her course
as the course whatever its words, and built the way out of danger on the officer's own
word, logged with his reason, for the helm, heaving to and letting go an anchor. The audit
found that `fill away` after a heave-to he did not order, and heaving in with weighing and
veering, are **not built** as the officer's own: both want the captain's word, by name or
by the general authority. By the audit this ruling has in effect been given: in the
owner's answers on the grant and the deck, and in the way out of danger kept on 7 October
(D1, rows 19 and 25).

**2. The sample's size on a local model.** Not the limit, given a context size. Qwen 3.8
kept the thread for 27 hours and two folds at 102,400 tokens. Without a size nothing is
asked or trimmed, so an officer should not be seated when the server reports none. What
limited the local models was the turn budget, the stand-by, the silent reply cap, and the
order language of a fore-and-aft vessel.

*Since.* 37g: no officer is seated when the server reports no context size and none is
given. Game 10 then showed what does limit a local model at this context: the count of
tokens runs short, the reserve does not cover it, and the limit on a reply cuts replies
off (G15). The audit puts it so: answered by play; the context is the live trouble.

**3. A far-detail vessel's bound.** Play gives no evidence either way: no ship was seen over
the land. Four free scenarios were written during the playtest, so "before any scenario is
written" has passed. The guard is one line and still worth having. The held estimate (G2)
mattered far more to how other vessels looked.

*Since.* **Not ruled and not built**, by the audit: no guard refuses a leg that crosses the
coast when a scenario loads. It is, in the audit's words, "The ruling the gate asked for
and never had".

**4. The re-asks.** The rule worked as written, on exactly the sections that changed, and it
is costly: batch changes. The drill is too small for a station with authority (I7, item 8).

*Since.* The changes were batched, as advised: one revision, in 37g. The lean brief then
narrowed what brings the question again to a change in the kind of thing a model is asked
to agree to (G13). The drill is as it was, and miscounted once in game 10. By the audit
the rule watches six sections today: the opening, what an instance would see and do,
leaving, being stopped, what is not done, and the journal.

### L3. What the gate still lacks

- **Unplayed**: the naval cruise, all of it; the chronometer and the time sight; British
  colours off Roscoff; and the lead's own officer's watch, on which the spec makes the
  verdict wait.
- **The naval cruise does not come through.** The gate's document has the stranger "spoken
  at 11:42 under no colours". Since 37e the frigate keeps her station and the letter
  reaches her, but nineteen hours later than before, and the brig is chased and lost: the
  speaking of the brig is marked as an expected failure. 37e's builder gave the reason as
  it then was: in 37d, after the pilot left, she lay for an hour and fifty minutes with her
  topsails unfilled, and it was only in that lost time that the admiral's cutter caught
  her; with the course now made good she fills and sails, and the cutter cannot catch her
  until she is on her station next morning. For what happens then, this edition first gave
  the account in 37f's section of the changes file, that her book orders a course across
  the wind and the helm takes her straight through it. **That account is wrong, by the
  audit, which sailed the cruise** (M, 2.4):
  - At 07:00 on the 13th the scenario puts the brig at a fixed place, 48° 50' N, 5° 16' W.
    The frigate is by then past it: the brig appears 4.8 miles on her starboard quarter, up
    wind of her and already standing away. The scenario file's own comment says where she
    was meant to be: "five leagues on the frigate's bow at seven".
  - The first chase order cannot lay the course for her and keeps the frigate close-hauled
    on the tack she is on, 102 degrees away from the chase. For thirty minutes the two
    ships sail apart.
  - At 07:30 the book gives chase again. The new course is 175 degrees round and the
    shorter way to it is by the stern, so the guard that wears her for a course across the
    wind's eye does not fire, and the plain order to steer is given. She is turned by the
    stern with her yards still braced sharp up for the old tack, nobody braces them, and at
    07:32:34 (tick 91954) every square sail is aback with the wind on her larboard quarter.
    She lies without way and the brig is lost.
  - In the auditor's trials, in memory, making the chase and the shaped course wear her
    took away the taking aback and still lost the brig. Putting the brig five leagues on
    the frigate's bow at 07:00, with no change to the code, brought the meeting back:
    sighted at 07:17, within hail at 08:21.
  - The same handling fault takes her aback once before, at tick 83957, an urgent line in
    the passage as pinned that was reported nowhere.
  - All of that code is the gate's own. The week's work changed where the frigate is at
    07:00, and that exposed it. What the cruise needs to close, by the audit: one line of
    the scenario file set again for where the frigate now is, the cruise's constants
    recorded again, the expected-failure mark taken off, and the gate's text of the cruise
    written again. The brig's place is tuned to the frigate's track, so any later change to
    the account, the tide or the pilot will move it again.
- **Also found and left on the cruise**, by 37f's builder: two of the book's orders give
  chase to one sail at the same moment, and the second of the two wears they order fails.
  The audit found it still so, at ticks 79260 and 79261, with "Could not wear: she would
  not come round" at 80653, and the same doubling at 07:00, where three orders give chase
  within a second.
- **On the cruise a wrong chronometer can displace a good account** (37e's changes file;
  G3). The cruise is the gate's only passage with a chronometer. The audit met it on its
  own run, at 09:00 on the 12th, off Plymouth with the land in sight.
- **The times and words in the gate's document are m5c's.** The recorded merchant passage
  moved in 37d, in 37e and in 37f. After 37d alone, by the changes file: the pilot of Brest
  aboard at 08:16 (06:26), the road of Bertheaume at 09:09 (07:47), the mouth of the Goulet
  at 12:19 (12:06), the Bay at 13:15 (13:05), the tin sold at 15:25 (15:10). As the build
  stands, by the audit's reading of the ticks the suite pins: the Falmouth pilot off at
  10:05; the sail at 13:05 "abeam to starboard, bearing W by S"; the Brest pilot aboard at
  07:44; Bertheaume at 08:46; the Bay at 13:10; the tin sold at 15:25. The line the gate's
  item 1 expects at 12:49 is not said. The suite's totals in the gate's document are m5c's
  too; the build's are 2,731 passed in the fast tier and 2,981 passed with nine expected
  failures in the whole suite, and the document's sentence "the seven are your rulings"
  now covers seven of nine (M, 2.1 and 2.3).
- **Two of the gate's items cannot show the cruise's trouble**, by the audit. Item 12
  passes as written while the cruise is broken, because the command it gives selects eleven
  tests and neither of the two lost beats is among them. And item 13's "the chase goes on
  to the same words" cannot be shown: at 08:00, when the cruise is saved, the chase is
  already lost (M, 2.2).
- **The gate's item 1** still says the purse moves by £6,000 at the sale, where game 1
  showed £10,800, which is the figure in the document's own account of the passage. The
  audit adds that the sale is for £10,800 and that £6,000 is the profit.
- **What closing the gate needs** is the audit's list of seven in M, 2.6.

## M. The gate as the build stands

This part is the auditor's, carried whole and in its words from Part 2 of
`handover-audit.md`. "I" is the auditor. Its marks for how each thing is known (**P**,
**T**, **R**, **D**) are explained in A5. Where it says "Part 3" or "Part 4" it means part
N here; "Part 1" is appendix 1; "the review" is the first edition, by its own section
numbers. The naval cruise, with which the owner means to close the gate next, is its 2.4,
and what closing the gate needs is its 2.6.

`docs/gates/gate-m5c.md`, item by item, as the build stands today.

### 2.1 The gate's document itself

- **Verdict: Pending.** Unchanged.
- **One change since the gate was cut**: a parenthesis in headline item 6, added by 37g, saying
  that a released station may be taken again as often as asked, that the deck goes to and
  fro, and that the detector counts orders that undo one another. (D: the file differs from
  m5c's only there; first changed in the snapshot after 37g.) The sentence it follows still
  says "a second seating once" and "contrary orders within a watch bring the nudge".
- **The rest of the document describes m5c as cut, and the build no longer matches it.**
  Nothing in it was re-measured after 37d to 37g. What is stale:

| Where | The gate's text | The build today | How I know |
|---|---|---|---|
| Setup, fast tier | "ends `2471 passed` and a line saying 244 slow tests were left out" | 2,731 passed by the changes file; 259 slow tests are left out (P: counted by collection; the fast tier was not run) | see 2.5 |
| Setup, whole suite | "`2708 passed, 7 xfailed`; the seven are your rulings" | **2,981 passed, 9 xfailed.** Two of the nine are not rulings (2.3) | P: my own run, 2.5 |
| The merchant passage | Falmouth pilot off 10:07; a sail off the Lizard at 12:49 "on the larboard bow, bearing SE by E, distant three leagues"; Brest pilot aboard 06:26; Bertheaume 07:47; the Bay 13:05; the tin sold 15:10 | pilot off 10:05; the sail at 13:05 "abeam to starboard, bearing W by S"; Brest pilot aboard 07:44; Bertheaume 08:46; the Bay 13:10; the tin sold 15:25 | R: the pinned ticks in `tests/test_known_truths.py`, `GATE_5C_MERCHANT_*`; the test passes in my run |
| The naval cruise | pilot aboard 08:12, off 09:07; the admiral's cutter within hail at 10:57 on the 12th; eight wears in the night; the *Palinure* at 07:16 "right ahead four leagues"; spoken at 11:42 | pilot aboard 08:13, off 09:03; the cutter within hail at 05:17 on the 13th, on the station; three wears and one that failed before 07:00; the *Palinure* at 07:00 "on the starboard quarter, bearing NNW, distant four miles"; **never spoken** | P: I sailed the cruise under its book (2.4) |
| The account against the truth | the figures at each noon and anchor | not re-measured by anyone since 37e; not checked by me | not checked |
| Item 1's expected lines | "at 12:49 'Sail ho! A sail on the larboard bow ...'"; "the purse moves by £6,000" | the 12:49 line is not said (above). The sale is for £10,800; £6,000 is the profit (the review's 8.2 asked for this to be mended; it was not) | R |
| Item 2's expected lines | "'Sail ho! A sail right ahead, bearing SW, distant four leagues' on the second morning"; "within hail: a stranger under no colours" | neither line is said | P |

### 2.2 The fourteen items

"Play" means the owner's own check in the browser or with a model. I started no server and
seated no model, so no item was checked in play; what is said of play comes from the review
(sections 4, 10.6 and 11) and is marked as its claim.

| # | Item | As the build stands | What I looked at |
|---|---|---|---|
| 1 | The merchant passage in the browser | The scripted passage comes through whole, Falmouth to the tin sold at Brest, with no grounding and no dragging. The expected lines in the gate's text are stale (2.1). Not checked in the browser | T: `test_the_merchant_passage_at_seed_7_has_its_own_constants` passes in my run; R: its constants |
| 2 | The naval cruise in the browser | **Does not come through.** The yard's provisions, the pilot, the admiral's letter and the station are there; the stranger is sighted, chased for half an hour, and lost. The review says the cruise has never been played by the owner at all | P: my own run of the scenario (2.4); T: `test_the_naval_cruise_speaks_the_stranger` is an expected failure |
| 3 | The longitude (on the cruise) | The orders are there and the scripted truths pass. On the cruise's own log the first time sight, at 09:00 off Plymouth with the land in sight, is "laid down by the observation" and moves the account more than two leagues: the fault 37e's own note admits (a chronometer trusted within five miles that is further out than that). The review says this item has not been played | P: my run, tick 10800; T: `test_truth_60_...`, `test_truth_61_...` pass |
| 4 | The tide at Falmouth | Unchanged in what the item asks. New since the gate: the master works the tide into the reckoning, and `the reckoning` says what tide is allowed | T: `test_truth_62_...`, `63`, `64` in `tests/test_tide.py` pass. Not checked in play |
| 5 | The anchor | Changed by 37f, and the item's lines still hold in form: "The best bower let go in 17 fathoms and a half; eighty-six fathoms of cable veered", "Brought up by the best bower ... Riding by the best bower to the flood". New: the first line says the scope ("veering to eighty-six fathoms, five times the depth"), an anchor's name is honoured, `heave in` exists, the dragging line is urgent once and names only what is left to do | P: my own probe at Carrick Road; T: `tests/test_tackle_orders.py` (26 tests) pass |
| 6 | The port | No change to the port's code but the severity of the pilot's hail (37d). Not checked | D: `freesail/world/ports.py` changed in 37d only |
| 7 | St Mary's and Roscoff | No change to the code. The review says British colours off Roscoff have not been played; St Mary's was entered in game 10 | D; the review's claim |
| 8 | The library's papers | No change found. Not checked | D: nothing under `client/` changed; the library's code unchanged |
| 9 | The lookout and the chart in the captain's hands | `shape a course` now steers to make good against the master's tide and says when its line crosses or skirts the shore; the nearest land is a reading; the client's chart is unchanged | T: `test_a_course_shaped_across_a_headland_or_close_along_the_shore_says_so`; P: probe of `the nearest land` |
| 10 | The officer's watch, Opus 5.5 through Claude Desktop | Played on m5c, m5c-b and on this folder at 37d (the review's games 2, 4, 8 and 9); **not played on the build as it stands**. Opus 5.5's last yes (6 October) was given against the brief as it stood before 37g, so the question is owed again, naming four sections, and the drill after it. The item's own words are stale: the deck given and taken no longer seats and unseats; `hand_over` gives the deck back and the officer stays | P: `consent_check` (my own read of the records by the game's rule); R: the item |
| 11 | The officer's watch, a local model on the cutter | Played on the build as it stands (game 10, 63 hours, by the review's account). The model's record of 7 October is against the brief as it stands and it is not asked again. Both seatings ended when the conversation outgrew the model's context; the cause is in the code (Part 4, C7) | P: the record's digest is the brief's (`288d0b18e34d76a8`); R: `harness.handover_threshold`, `local.py` |
| 12 | The truths of this gate | The gate's first command selects eleven tests (truths 6, 7, 60, 61, 65, 67 to 72); truths 62 to 64 and 66 are in `tests/test_tide.py` and `tests/test_ground.py` and are not selected by it. All of them pass in the whole suite. Neither of the two new expected failures is in the selection, so **this item passes as written while the cruise is broken** | P: `--collect-only` of the gate's own command; my suite run |
| 13 | A scenario saved and loaded | The cruise saved at 08:00 on the 13th replays to the same digest, and a save loads from its checkpoint. "The chase goes on to the same words" cannot be shown: at 08:00 the chase is already lost | T: `test_truth_72_the_two_scenarios_replay_to_the_same_digest` passes; R: `GATE_5C_CRUISE_SAVE_TICK` |
| 14 | Rulings wanted | *The officer's domain*: ruled (the review's section 9, questions 4 and 5, and the way out of danger kept on 7 October) and built by 37g. *The sample's size on a local model*: answered by play; the context is the live trouble (item 11). *A far-detail vessel's bound*: **not ruled and not built**; no guard refuses a leg that crosses the coast when a scenario loads. *The re-asks*: the rule watches six sections today (the opening, what an instance would see and do, leaving, being stopped, what is not done, the journal); the drill is unchanged and the review calls it too small | R: `agent.py::OFFICER_DOMAIN`, `consent.py::RE_ASK_SECTIONS`; no match for a coast guard in `world/scenarios.py` or `world/ships.py` |

### 2.3 Every test marked as an expected failure

Nine, all strict (a test that began to pass would fail the suite), all in
`tests/test_known_truths.py`. P: all nine were reported as expected failures in my run.

| Test | Since | Why it is marked |
|---|---|---|
| `test_truth_3_broad_reach_is_the_schooners_fastest_point` | milestone 3b | the schooner is fastest with the wind abeam, not on the quarter; the sail model has no cost for a fore-and-aft rig pressed on a reach |
| `test_truth_11_wearing_loses_a_quarter_to_half_a_mile_to_leeward` | 3b | the wear comes to as soon as the wind is aft and loses about a tenth of a mile |
| `test_truth_18_the_watch_and_all_hands_take_the_spec_times` | 3b | plain sail is set in 16 minutes by the watch and under 6 by all hands, against the spec's 25 to 40 and 12 to 20 |
| `test_truth_24_a_quarter_point_closer_or_a_quarter_knot_more` | 3b, the owner's ruling | the after yards braced sharper gain 0.17 knot, under the quarter |
| `test_truth_26_about_half_a_point` | 3b, the owner's ruling | the bowlines gain a third of a point, not half |
| `test_truth_28_lying_a_try_under_a_knot_and_a_half` | 3b, the owner's ruling | a-try in 45 knots she goes astern at four to five knots |
| `test_truth_31_a_quarter_point_closer` | 3b, the owner's ruling | the catharpins gain under a degree |
| `test_the_schooners_pilot_boards_before_she_runs_in` | **37e** | the schooner of gate 5b now stands in at seven knots, and the Falmouth pilot, who boards a ship making under six, hails her and is left astern. Three mends of her book were tried and none kept. Left for 37h, the pilot's package, which is not written |
| `test_the_naval_cruise_speaks_the_stranger` | **37e**, restated by 37f | the cruise's French brig is chased and lost. The reason written on the mark is partly wrong (2.4) |

The first seven are the same seven the gate's document names (truths 3, 11, 18, 24, 26, 28
and 31; R: the same seven marks stand at the same lines of the gate's own file). The last two are beats of recorded passages
that the week's work lost. They are not rulings of the owner's, and the gate's sentence
"the seven are your rulings" is no longer the whole of it.

### 2.4 The naval cruise: exactly what stops it

I sailed `data/scenarios/naval-cruise.yaml` under its own book on the build as it stands,
to 08:40 on the second morning, and wrote out her log and her head, the wind and her way
every half minute about the chase (the scripts and their output are in my scratch folder,
`handover-audit\cruise_probe.py`, `cruise-log.txt`, `cruise-state.txt`). Every beat up to
there falls on the tick the passing test pins (the yard's stores, the pilot aboard and
off, the cutter's hail, the letter, the sighting, the chase lost), so this is the passage
the suite holds.

**What happens.**

1. *05:17 on the 13th* (tick 83838). The port admiral's cutter comes within hail on the
   station and the letter is read. Before 37e she caught the frigate off Plymouth at 10:57
   on the 12th; since 37e the frigate fills and sails as soon as the pilot is off, and the
   cutter has a stern chase of nineteen hours. The frigate chases the cutter (a stranger
   until her colours are made out) to the north-eastward for 76 minutes before she is
   within hail, then shapes for the station again.
2. *07:00* (tick 90000). The scenario's own order puts the *Palinure* on the sea at a
   position fixed in the file, 48° 50' N, 5° 16' W. The frigate is then at 48° 45.6' N,
   5° 12.9' W, standing SSW (206°) at five knots and a quarter: **the brig appears 4.8 miles
   on her starboard quarter, up wind of her and already standing away NE by N** at something
   under six knots (my reckoning from her bearing and distance at two moments). The scenario file's own comment says where she was meant
   to be: "five leagues on the frigate's bow at seven". At m5c, by the gate's own text, she was
   sighted right ahead at 07:16.
3. *07:00, the first chase order.* The brig bears NNW, 35 degrees from the wind's eye, so
   the course for her cannot be laid. `_chase_course` then puts the frigate close-hauled
   "on the tack she is on", which is the starboard tack, heading SW by W: **102 degrees away
   from the chase**, where the other tack would have pointed within 33 degrees of her. The
   line says "she is kept full and by on the starboard tack". For thirty minutes the two
   ships sail apart; the range opens from 4.9 miles to 8.5.
4. *07:30* (tick 91800). The book's "keep her bearing" gives chase again. The brig now
   bears N by E and the course ordered is NE by E (54°). The frigate's head is SW by W
   (229°): the new course is 175 degrees round, and the shorter way to it is **to larboard,
   by the stern**. The guard that wears her for a course "across the wind's eye from her
   head" looks only for the wind's eye inside the shorter turn; here the eye lies the other
   way, so no wear is ordered and the plain order `steer 54` is given. The helm takes her
   round by the stern (her head 229°, 206°, 169°, 135°, 104°, 78°, 63°, 54° at
   half-minute intervals) **with her yards still braced sharp up for the starboard tack.**
   Nobody braces them: the book's trim rules fire when she is "steady on the course" or the
   wind shifts, and neither happens. At 07:32:34 (tick 91954) every square sail is aback
   with the wind on her larboard quarter, the urgent line "Taken aback: the sails pressed
   against the masts and she lost her way" is logged, and she lies without way.
5. *07:57* (tick 93420). The brig is out of sight. The book shapes for the station again,
   which turns her back the same way; she has no way on at 08:00.

**The same handling fault bites earlier in the same log and is reported nowhere.** At
05:17, when the book shapes SW by S for the station from a head of NE by E, she is again
turned 150 degrees by the stern with her yards unbraced and is "Taken aback" at tick 83957,
an urgent line. That time she steadies on the course four and a half minutes later and the trim rule
braces her round. The changes file, the test's comments and the review mention one failed
wear (tick 80653) and one taking aback; there are two urgent lines in the cruise as pinned.

**Where it is in the code.** All of it is code the gate was cut with; none of it was
written this week (D: `_chase_course`, `_course_not_laid`, `_helm_for` and the `give chase`
order are the same to the character in the gate and the build, and so is
`naval-cruise.yaml`). The week's work changed where the frigate is at 07:00, and that exposed
it.

| What | Where |
|---|---|
| The brig's place and hour | `data/scenarios/naval-cruise.yaml`, `world_orders`, the third line: `ship: a brig-sloop "Palinure" of France at 48 50 N 5 16 W ...` at `1805-06-13T07:00` |
| The tack chosen for a chase too near the wind | `freesail/orders/navigation.py`, `_chase_course`, the last block ("on the tack she is on") |
| A large alteration by the stern given to the helm alone | `freesail/orders/navigation.py`, `_course_not_laid`, the branch that returns `"wear ship"` only when the wind's eye lies inside the shorter turn; and `give chase` and `shape a course for`, which then call `steer` |
| Nothing braces the yards while she turns | the cruise's book, `data/scenarios/naval-cruise.orders`: "trim to the course" waits for `steady on the course`; `steer` moves the helm and no more |

**What I tried, in memory only, with nothing in the tree changed** (`cruise_exp.py`,
`cruise_exp2.py` in my scratch folder):

| Trial | Result |
|---|---|
| The chase and the shaped course wear her whenever the new course puts the wind on her other side by the stern | no taking aback; she wears cleanly at 07:30; **the brig is still lost**, at 08:01 |
| The chase chooses the tack that points nearer the chase | the tack is ordered from a head too far off the wind and fails three times; taken aback at 07:32; the brig lost at 07:52. My change was crude; it shows only that this is not a one-line mend |
| Both together | the brig lost at 07:35 |
| **No change to the code. The brig put five leagues on the frigate's bow at 07:00** (48° 32' N, 5° 23' W in place of 48° 50' N, 5° 16' W) | **the meeting comes back.** Sighted at 07:17 "right ahead, bearing SSW, distant three leagues"; chased by her bearing; made out at 08:02 and 08:16; **within hail at 08:21** (tick 94899), "a stranger, her colours not made out"; "the chase up" shapes for the station at the same tick. Both things the expected-failure test asks are then true |

**So the changes file and the test's mark are right in one half and wrong in the other.**
They say that either the chase order wearing her, or the scenario's hours, would bring the
meeting back. On my trials the first does not and the second does. And the mark's account
of the moment itself ("a course across the wind's eye from her head, and the helm takes
her through the wind") is not what the ship does: she is not taken through the wind; she
is turned the other way, by the stern, and is caught aback because her yards were never
braced round. That matters to whoever mends it, because the mend the mark names (wearing
her "for a course across the wind, as its first form does") is already in the code and did
not fire, rightly by its own test.

**What the cruise needs to close.** One line of the scenario file set again for where the
frigate now is, the cruise's constants recorded again (its digest, its 1,988 lines, the
ticks of the sighting, the chase and the hail), the expected-failure mark taken off, and
the gate's text of the cruise written again. The brig's place is tuned to the frigate's
track, so any later change to the account, the tide or the pilot will move it again; a
world order that places a ship from the player's own position ("five leagues on her bow")
would not be so brittle, and does not exist. The handling fault (a large alteration given
to the helm with the yards left braced) is a separate matter that stays in the game
whatever is done to the scenario. (In the trial that brought the meeting back she was
taken aback once more, at tick 115716, half a minute after a wear at the hour. That is
another circumstance and I did not trace it. Of the pinned passage I read the first 26
hours and 40 minutes; the rest was run by the suite and not read by me.)

### 2.5 The suite and the linter, first hand

From the build folder, with `PYTHONPATH` set to it, `PYTHONUTF8=1` and
`PYTHONDONTWRITEBYTECODE=1`:

| Command | Its last line |
|---|---|
| `py -m pytest -n 4 --slow -p no:cacheprovider`, run once | `2981 passed, 9 xfailed in 1179.13s (0:19:39)` |
| `py -m ruff check . --no-cache` | `All checks passed!` |
| `py -m ruff format --check . --no-cache` | `171 files already formatted` |
| `py -m pytest --collect-only -q -p no:cacheprovider` (the fast tier counted, not run) | `fast tier: 259 slow tests left out` |

The suite's figures are the lead's: 2,981 and nine. It took nearly twenty minutes here
against his thirteen; other work was running on the machine. The nine expected failures
are the nine of 2.3, each named in the run's summary. With 2,990 tests in all and 259
left out, the fast tier is 2,731, which is the changes file's figure for it.

I gave the linter `--no-cache` so that it would write nothing in the folder; the brief's
command is the same without it. No `.pytest_cache` was made, and the listing of both
folders taken before the suite is the same after it.

### 2.6 What closing the gate needs

1. **The naval cruise brought through** (2.4): the scenario's line, the constants, the mark,
   the text.
2. **A decision on the schooner's pilot.** Her passage is gate 5b's, but its lost beat is one
   of the nine expected failures of this gate's suite. It waits on 37h, which is not written.
   Either 37h is built before the gate closes, or the gate closes with the mark standing
   and says so.
3. **The gate's document written again for the build**: the two suite lines, the passages'
   times and words, the account's figures, items 1, 2, 5, 6 (the headline), 10 and 13, and
   item 14 turned from "rulings wanted" into the rulings given. The folder's name comes
   out of headline item 6.
4. **The play the gate still lacks**, by the review's own count (its sections 4, 8.8 and
   10.6; I cannot check play): the naval cruise, the chronometer and the lunar on it,
   British colours off Roscoff, and the lead's own officer's watch, which the gate's
   opening lines make half of the verdict.
5. **The consent question, again, before any of that play with a model.** Six identities
   hold a yes that the rule will ask again at the next seating: Opus 5.5, Sonnet 5, Sonnet
   5.5, the llama3.1 8B, the qwen3.8 27B (by digest) and the Gemma4 26B Q4_K_M. Three of
   them (the September records) are asked with five sections named, the others with four.
   Only the Qwen3.8 27B 0814 file has answered against the brief as it stands. (P: my own
   read of the records by `consent.decide`.) Item 10 names Opus 5.5 through Claude Desktop,
   so that re-ask and its drill come first.
6. **The ruling the gate asked for and never had**: a far-detail vessel's leg across the
   coast (item 14).
7. **`BUILD_NAME` set for the gate**, with the nine test lines that spell it (Part 3).

## N. Folding the work in, with advice by package

This part is the auditor's, carried whole and in its words from Parts 3 and 4 of
`handover-audit.md`, with the audit's own numbers kept in the headings. "I" is the
auditor, and its marks are explained in A5. "Part 2" is part M here and "Part 1" is
appendix 1. The traps at the merge are its 3.9, the advice by package is its 4.2, and what
the owner must decide before the work is folded in is its 4.3.

Two notes from the lead bear on this part. They are the lead's and not the audit's, and are
set out where the subject is. On C6 and on the fourth of the things to decide: three of the
additions to what the general authority keeps back were approved with the lean brief, the
decisions log is behind, and the captain's own going below and coming on deck are unruled
(G11, D2). On the last row of the table in C7: game 10's finding about the anchor left
aweigh stands on the game's log, and the conditions are not yet pinned down (G8).

### N1. What changed in the tree (the audit's Part 3)

#### 3.1 How it was compared

I hashed every file in seven places and set them side by side: the gate folder, m5c-b, the
lead's four snapshots (after 37d, 37e, 37f and 37g's first pass) and the build as it stands.
Caches were left out. A file is put down to the package after which its content first
differs from the stage before. I also compared the gate folder with the gate's own zip,
`FreeSail-gate-m5c.zip`, reading the zip without extracting it. The scripts and their tables
are in my scratch folder (`treecmp.py`, `treesum.tsv`, `zipcmp.py`, `areas.py`).

Two things about the baseline first.

- **The gate folder is not the gate as cut; it is the gate as cut and then played in.** Every
  one of the zip's 589 files is in the folder unchanged. The folder holds 87 more: the
  owner's saves (14 under `saves\`, three more with their checkpoints at the root), his
  notes, four scenario files he wrote during the playtest (`data/scenarios/merchant-brig.yaml`,
  `merchant-cutter.yaml`, `merchant-schooner-plymouth.yaml`, `merchant-ship.yaml`), eight
  consent records made in play, and the review folder (54 files).
- **The review folder in the gate was the same, byte for byte, as the one in the build** when
  I compared them (before this file and `report-2.md` were added here), this morning's
  `report.md` included. The changes file calls the build's "a copy of the review
  as it stood on 2026-10-06" with the original in m5c; in fact both have been kept in step.
  A diff of the build against the gate folder therefore shows nothing of the review, and a
  diff against the zip shows all of it.

#### 3.2 In numbers, the build against the gate folder

129 files changed, 23 added, 21 gone. The 21 are the owner's saves and notes of m5c, left
behind on purpose. The 23 are below.

| Area | Changed | New | Lines added / taken out | Which package |
|---|---|---|---|---|
| Code, `freesail/` | 44 | 0 | 10,408 / 1,188 | below |
| Tests, `tests/*.py` | 27 | 3 | 8,705 / 316 | below |
| Data, `data/` | 37 | 1 | 641 / 101 | below |
| Documents, `docs/` (the review folder aside) | 21 | 2 consent records | 3,224 / 114 | below |
| Test fixtures | 0 | 7 | | 37d (six), 37g's second pass (one) |
| The root | 0 | 2 | | `CHANGES-m5c-c.md`; `m5c-c Notes.txt` (the owner's) |
| The owner's saves | 0 | 8 | | games 9 and 10 |

Nothing changed under `client/`, `tools/` or `.github/`, nor `README.md`, `pyproject.toml`,
`.gitignore` or `.mcp.json`.

**The changes file's own lists of files are right.** For each of 37d, 37e, 37f, 37g and
37g's second pass I set its "Files changed" paragraph against what the snapshots show
changed at that stage, and found no file changed that it does not name and none named that
did not change. And m5c-b's claim holds: the 22 files m5c-b changed came into the build byte
for byte (15 of them were still m5c-b's own bytes after 37d; the other seven had by then
been changed again by 37d).

#### 3.3 The code, by area

| Area | Files | Changed by |
|---|---|---|
| `freesail/agents/` (the harness, the doors, consent) | `agent.py`, `harness.py`, `tools.py`, `remote.py`, `consent.py` | m5c-b, then 37g; the first three again in 37g's second pass; `harness.py` also in 37d |
| | `mcp_server.py`, `local.py` | 37g and its second pass |
| | `journal.py`, `__init__.py` | 37g |
| | `repl.py` | 37d, 37g |
| `freesail/world/` | `reckoning.py` | 37d, 37e, 37f |
| | `chart.py` | 37d, 37e |
| | `lookout.py`, `weather.py`, `ports.py`, `ships.py` | 37d |
| | `tide.py` | 37e |
| | `ground.py` | 37f |
| | `people.py` | 37g |
| `freesail/core/` | `world.py` | m5c-b, 37d, 37e, 37f, 37g (the build's name each time) |
| | `replay.py` | m5c-b, 37d |
| `freesail/orders/` | `navigation.py` | 37d, 37e, 37g |
| | `complete.py` | 37d, 37e |
| | `verbs.py`, `ground_tackle.py` | 37f |
| | `stations.py`, `vocabulary.py`, `crew.py` | 37g |
| `freesail/evolutions/` | `scripts.py`, `runner.py`, `registry.py` | 37f |
| `freesail/physics/` | `hull.py`, `integrate.py` | m5c-b, 37f |
| | `anchor.py`, `sails.py` | 37f |
| `freesail/standing/` | `book.py`, `rules.py` | 37f |
| | `runtime.py` | 37f, 37g |
| `freesail/api/` | `readings.py` | 37d, 37e, 37f, 37g |
| | `queries.py` | 37g |
| `freesail/ui/` | `server.py` | 37d, 37g |
| | `console.py` | 37d |
| `freesail/ship/parts.py`, `freesail/crew/model.py` | | 37f; 37g |

#### 3.4 Data and fixtures

| What | Changed by |
|---|---|
| `data/vocabulary.yaml` | every package: `take a fix` (37d); the three forms of `allow` (37e); `heave in`, `fill away and steer`, the anchors' names (37f); the general grant, `stand down`, `resume the officer`, and the table of what undoes what (37g) |
| `data/tides/streams.yaml` | 37e: what the master's directions say of each water |
| `data/evolutions/`: 27 changed, `heave_in.yaml` new | 37f: eight evolutions of lying to and the ground rewritten; nineteen marked so that "done already" is no failure |
| `data/scenarios/gate-5b-passage.orders` | 37d, 37e, 37f |
| `data/scenarios/merchant-passage.orders` | 37d, 37e, 37f |
| `data/scenarios/gate-5b-passage-schooner.orders` | 37d, 37e |
| `data/scenarios/naval-cruise.orders` | 37d, 37f. **`naval-cruise.yaml` itself is unchanged**, which is where the cruise's trouble lies (Part 2) |
| `data/standing_orders/starter.orders` | 37f: the guard on its trim rules |
| `data/charts/features/channel-west.yaml`, `.index.json`, `data/charts/manifest.yaml` | 37f: the note of the bottom in Brest road |
| `tests/fixtures/saves/m5c-cutter-tick34091` and `m5c-b-harpy-tick602100`, each a `.json` and a `.checkpoint` | 37d. **They are the owner's own saves, byte for byte** (P: compared with `FreeSail-gate-m5c\saves\freesail-seed7-tick34091` and `FreeSail-gate-m5c-b\saves\freesail-seed7-tick602100`). They hold a model's transcript and journal and the owner's typed lines |
| `tests/fixtures/saves/m5c-c-37d-officer-tick5400` (`.json`, `.checkpoint`) | 37d: a scripted game of the package's own making; nothing personal in it by its description (I did not read it through) |
| `tests/fixtures/ConsentBrief-before-37g.md` | 37g's second pass: the consent brief as it stood before 37g, for the test of the re-ask. Its digest is `f667a04e00b32e1f`, which is the digest Opus 5.5's record of 6 October was asked with (P) |

#### 3.5 Tests

Three new files, all 37f's: `tests/test_lying_to.py` (20 tests), `test_tackle_orders.py`
(26) and `test_log_lines.py` (19). In all there are 191 test names the gate did not have
and seven it had that are gone, each of the seven replaced by a test of the new rule
(for example `test_you_have_the_deck_seats_the_officer_and_i_have_the_deck_stands_it_down`
by `..._gives_it_and_i_have_the_deck_takes_it_and_no_more`).

| Changed by | Test files |
|---|---|
| m5c-b only | `test_hull.py` |
| m5c-b, then later | `test_agent_api.py` (37g), `test_weather_script.py` (37f), `test_known_truths.py` (37d, 37e, 37f), `test_officer.py` (37d, 37g, second pass) |
| 37d | `test_anchor.py`, `test_lookout.py`, `test_weather.py`; with 37e `test_chart.py`, `test_orders.py`, `test_readings.py`; with 37f `test_ports.py`; with 37e and 37f `test_reckoning.py`, `conftest.py`; with all three after `test_checkpoint.py`, `test_replay.py` |
| 37e | `test_tide.py`, `test_longitude.py` |
| 37f | `test_catalogue.py`, `test_evolutions.py`, `test_ground.py`, `test_staying.py`; with 37g `test_agents.py` |
| 37g | `test_mcp_server.py`, `test_local_runner.py`, `test_standing.py` |
| 37g's second pass | `test_consent.py` |

#### 3.6 Documents

| Document | Changed by |
|---|---|
| `docs/TechnicalSpec-M5.md` | m5c-b, 37d, 37e, 37f, 37g, second pass |
| `docs/TechnicalSpec-M0-M2.md` | m5c-b, 37f |
| `docs/TechnicalSpec-M3.md` | 37f |
| `docs/TechnicalSpec-M4.md` | 37g, second pass |
| `docs/DesignProposal.md` | 37g (decisions 34 to 36), second pass (decision 37) |
| `docs/agents/ConsentBrief.md` | m5c-b, 37g, second pass. **Unchanged through 37d, 37e and 37f**, as each of those packages claims |
| `docs/agents/README.md`, `ConsentAndPreferences.md` | m5c-b, 37g, second pass |
| `docs/agents/Harness.md` | m5c-b, 37d, 37g, second pass |
| `docs/dev/M5-WorkPackages.md` | 37d, 37e (the plan and the four briefs; the lead's) |
| `docs/dev/TuningNotes.md` | 37d, 37e, 37f, 37g |
| `docs/gates/gate-m5c.md` | 37g (one parenthesis) |
| Primer 3, 5, 7, 11 | 37f |
| Primer 6 | m5c-b |
| Primer 10 | 37d, 37e |
| Primer 12 | 37e |
| Primer 13 | 37d, 37e, 37f |
| Primer 16 | m5c-b, 37g, second pass |

#### 3.7 The consent records made in play

The zip holds ten files under `docs/agents/consent/`. The build holds twenty. None of the
eighteen that are also in the gate folder differs from it by a byte (P), so nothing on
record was edited this week.

| Record | Made | In the zip | In the gate folder | In m5c-b | In the build |
|---|---|---|---|---|---|
| The ten of September (three early transcripts, seven harness records) | before the gate | yes | yes | yes | yes |
| `2026-10-02-opus-5.5.md` | play at m5c | no | yes | yes | yes |
| `2026-10-03-qwen3.8-27b-digest-...` (three files) | play at m5c | no | yes | yes | yes |
| `2026-10-04-gemma4-...` (two), `2026-10-04-qwen3.8-27b-0814-...`, `2026-10-04-qwen3.8-27b-digest-...` | play at m5c | no | yes | no | yes |
| **`2026-10-03-opus-5.5.md`** | play at m5c-b | no | **no** | yes | **no** |
| `2026-10-06-opus-5.5.md` | game 9, on this folder at 37d | no | no | no | yes |
| `2026-10-07-qwen3.8-27b-0814-q4_k_m.gguf.md` | game 10, on this folder as it stands | no | no | no | yes |

So eleven records were made in play since the gate was cut, and **the build folder holds
ten of them. The eleventh, Opus 5.5's of 3 October, is only in m5c-b.** The changes file
says it was left behind because it is not part of m5c-b's diff. But the consent brief
tells every model that "this conversation is kept verbatim ... in the game's repository
under `docs/agents/consent/`". If that sentence is to stay true, all eleven go into the
repository, the one in m5c-b among them. It is superseded as Opus 5.5's latest answer by
the record of 6 October, so carrying it changes nothing the game decides. Records are read
by the game and are not to be edited on the way.

#### 3.8 What belongs to this folder alone

| Thing | Why it should not be carried as it is |
|---|---|
| `saves\` (four games' saves with checkpoints) | the owner's; by his rule a save lies in the folder of the build that played it. `.gitignore` leaves `saves/` out already |
| `m5c-c Notes.txt` | the owner's notes on game 9 |
| `.mcp.json` | identical to the gate's; nothing to carry |
| `CHANGES-m5c-c.md` | the folder's own account. Its substance belongs in the decisions log and the work-packages document, where most of it already is |
| **The build's name**, `BUILD_NAME = "m5c-c/37g"` in `freesail/core/world.py` | it names this folder. It is set by hand at each package or gate, so the repository sets its own. **Nine test lines spell it out** and must move with it: `tests/test_checkpoint.py` lines 218, 230 and 255, and `tests/test_replay.py` lines 251, 264, 334, 389, 406 and 433. (The lines there that say `m5c-c/37d` name the stamp inside 37d's fixture and stay.) Note that the second pass of 37g changed the code and did not change the name |
| The folder's name in the documents | `FreeSail-gate-m5c-c` or `m5c-c` is written in `docs/gates/gate-m5c.md`, `docs/DesignProposal.md`, `docs/dev/M5-WorkPackages.md` and `docs/dev/TuningNotes.md` |
| The review folder, `docs/playtests/2026-10-05-gate-5c-review/` | not in the zip. It is the same in both folders. Whether the repository takes it is the owner's to say: `report.md`, the readers' papers and the two chat transcripts under `evidence/` quote models' journals and the owner's typed lines at length; `drafts/` holds working papers |
| The two playtest saves under `tests/fixtures/saves/` | the changes file already leaves this to the owner. Two things it does not say are in 3.9 |
| The four free scenario files under `data/scenarios/` | the owner's, written at m5c and not in the zip. They are harmless, but see the fingerprint in 3.9 |
| Caches | `__pycache__` folders throughout and `.ruff_cache` at the root |

#### 3.9 Four traps at the merge

1. **`.gitignore` will leave the fixture saves out without a word.** Its line `saves/` has no
   leading slash, so it matches a folder of that name at any depth, `tests/fixtures/saves/`
   included. A plain `git add` will not take the three kept saves, the package's own
   scripted one among them. The tests of the two playtest saves then skip, as written, and
   the tests of the package's own save fail, saying "restore it from the
   repository" (R: `tests/test_checkpoint.py::_the_37d_save`). So the promise in the
   changes file ("each must load from its checkpoint, run on and save again, on every
   build from now on") would lapse for the two playtest saves with nobody told. It needs an exception in `.gitignore` or the fixtures moved to a folder with
   another name. (R: `.gitignore`; I ran no git command, so this is from the rule as git
   documents it.)
2. **The fingerprint of the rules takes in every file under `data/` but the chart's tiles**
   (R: `core/world.py::fingerprint_of`), the owner's four free scenarios among them. Adding,
   leaving out or editing any scenario file makes a different build by that test. That is
   as the brief asked ("the data a replay reads"), and its consequence should be known: once
   the work is in the repository no save made in this folder is "this build's", so games 9
   and 10 load from their checkpoints and are refused a replay unless `--replay-anyway` is
   given. All four of the owner's saves here do load from their checkpoints on the build as
   it stands (P: `saves_check.py`; I ran no tick on them).
3. **A test pins the bytes of the fixture brief**: `tests/test_officer.py` line 1509 expects
   `tests/fixtures/ConsentBrief-before-37g.md` to have the digest `f667a04e00b32e1f`. The
   file has Unix line endings. A checkout that turns them into Windows ones would fail that
   test. The rules' fingerprint folds line endings; the consent digest does not.
4. **`docs/agents/ConsentBrief.md` must arrive unchanged in its watched sections.** One
   model has now answered against it (digest `288d0b18e34d76a8`, P). The rule compares the
   words of six sections and not the digest, so a re-wrapped line asks nobody again, but
   any change of a word in those sections asks every identity again, that one included.

### N2. Where the claims and the code part company (the audit's Part 4)

Most serious first. "The changes file" is `CHANGES-m5c-c.md`; "the review" is `report.md`.

#### 4.1 The disagreements

**C1. The cruise's lost meeting is put down to the wrong cause, and the cure that is named
does not bring it back.** The changes file (37f, "The naval cruise"), the mark on
`test_the_naval_cruise_speaks_the_stranger` and the review's status block all say that the
book orders "a course that lies across the wind from her head; the helm takes her straight
through the wind, every sail aback", and that mending the chase order so that it wears her,
or the scenario's hours, would bring the meeting back. I sailed it (Part 2, 2.4). She is not
taken through the wind. She is turned 175 degrees the other way, by the stern, with her
yards left braced for the old tack, and is caught aback with the wind on her quarter. The
guard that wears her for a course across the wind's eye is in the code already and rightly
did not fire. A mend of the kind the mark names, tried in memory, did not bring the brig
back, nor did a second of my own, nor the two together; she was lost by 08:01 each time. Putting the brig where the scenario file's own comment
says she was meant to be, with no change to the code, did: within hail at 08:21. Half an
hour earlier still, the first chase order had put the frigate on the tack that led away
from the chase, and nobody has written that down either. *Why it is serious:* the cruise is
one of the two passages the gate is about, the owner is about to close the gate, and a
builder handed the mark's account would mend the wrong thing.

**C2. The cruise as pinned holds two urgent "Taken aback" lines and one failed wear in
its first 27 hours, which is as far as I read it; the record admits one of each.** Tick 83957, two minutes after the admiral's letter is read, is
the same handling fault as tick 91954. The cruise's test checks that she is never aground
and never drags; it does not look for a ship taken aback, so the suite is content. The
fault itself is not this week's (the chase code is the gate's own, D), but the week's work
is what brought the frigate to the places where it bites.

**C3. The gate's document describes the gate as cut, not the build.** Its two suite lines,
both passages' times and words, and items 1, 2, 10 and 13 are stale (Part 2, 2.1). Its item
12 passes as written, because the command it gives selects eleven tests and neither of the
two lost beats is among them. Its sentence "the seven are your rulings" now covers seven of
nine. None of this is hidden: nobody claimed the gate's text had been brought up to date.
It is here because the owner will read that text when he closes the gate.

**C4. "Each must load from its checkpoint, run on and save again, on every build from now
on."** True in this folder (T: the tests of the three kept saves pass). It will stop being
true in the repository unless something is done, for a reason the changes file does not
give: `.gitignore`'s `saves/` matches `tests/fixtures/saves/` (Part 3, 3.9). The changes
file does say that the two playtest saves wait on the owner's word and that their tests
skip without them. With the files missing those tests skip, and the tests of the package's
own save fail with the words "restore it from the repository" (R:
`tests/test_checkpoint.py::_the_37d_save`).

**C5. One consent record is in neither folder that will be diffed.** The changes file says
Opus 5.5's record of 3 October was left in m5c-b because it is not part of m5c-b's diff.
That is so (D). The consent brief promises each model that its record is kept in the
repository (Part 3, 3.7). The same paragraph of the changes file calls the review folder
here "a copy ... as it stood on 2026-10-06" with the original in m5c; the two are kept in
step and are identical today (D).

**C6. The general authority keeps back more than the list on record.** The owner approved
four heads on 7 October (the port's business, his standing orders, a new destination, what
cannot be undone) and the decisions log, decision 36, records those four. The brief of 37g
added a fifth (the reckoning set by hand). The code keeps back those five and four more: a
chase, the tide allowed in the reckoning, sending for a person, and the captain's own
going below and coming on deck (R: `freesail/agents/agent.py`, `_KEPT_BACK` and
`GENERAL_KEPT_BACK_WORDS`). The changes file says so plainly, twice, and says the second
pass "closes the point". What the second pass closed is the wording: the three places that
state the list now agree with one another and with the code. I found no ruling of the
owner's on the additions. A chase was on his own list under "when Milestone 7 comes".
It is a small thing, and it is the owner's.

**C7. The review's account of game 10, where I could check it.** Six of its statements about
the build were tried against the build:

| The review says (section 11) | What I found |
|---|---|
| A course with a half point is read as its last word | Borne out. `steer south by west half west` is answered "Helm ordered: steer west; W (270°)" (P) |
| The last save replays one line short, at a stand-down by the door | Borne out exactly. Replayed in memory on the build that wrote it: 4,239 lines against 4,240, the ship in the same place; the line missing is at tick 183600, "A notable event that speaks of danger: The Nut Rock ... the officer of the watch is sampled again" (P: `saves_check.py`). That line is one of 37g's own new ones |
| The handover note is asked for too late, and tokens are counted at four characters | Borne out in the code. The note is asked for at the context less 14,000 tokens when that is past six tenths: 88,400 of 102,400, where before 37g it was 61,440 (R: `harness.py::handover_threshold`). The runner counts four characters to a token and never reads why a reply ended (R: `local.py`; no use of the server's `finish_reason` or its token counts) |
| `Let go the sheet anchor` was accepted and failed four minutes later | True only when the hands are at other work. With nothing in hand the cutter refuses it at once: "no anchor aboard answers to 'sheet'". Given while she was getting under way it was accepted (P: `probe_orders.py`, `probe2.py`) |
| A standing order's action is not read when it is given | Half true. The action's first word is read: `then lett go the anker` is refused at entry. The rest is not: `then take a fix as soon as a bearing can be taken`, `then take a bearing of the moon made of cheese` and `then let go the sheet anchor` were all entered in the book (P) |
| An anchor left aweigh by a belay can be neither let go nor weighed | Not reproduced: my belay came before the anchor was aweigh, and she was then simply at anchor (P). Not checked further |

**C8. The number in the one rule is two where the brief said three.** Disclosed by the
builder, with the reason (R: `reckoning.py`, `OBSERVATION_OUT_SIGMAS = 2.0`). It is the rule
that took the cast a mile off in game 10, and that lays the cruise's account on a
chronometer more than five miles out at 09:00 with the land in sight (P: my run, tick
10800). With three, by the builder's note, game 9's noon sight would not be taken. So the
number is doing two jobs; the review's 11.6 proposes to take casts out from under it.

**C9. The watcher is told of three tools it is refused, not two.** The second pass's note
names `hand_over` and `handover_note`. The watcher's brief as sent also lists
`submit_order` among "the tools you have" (P: the briefs written out afresh, which are byte
for byte the review's `evidence/station-briefs-after-37g-second-pass.txt`).

**What I checked and found as claimed**, so that the list above is not read as the whole
picture:

- The suite's last line and the linter's (2.5).
- Every "Files changed" list in the changes file, against the snapshots (3.2).
- m5c-b applied byte for byte (3.2).
- The consent brief untouched by 37d, 37e and 37f; revised by 37g and its second pass;
  its digest `288d0b18e34d76a8`; its body 1,371 words; the body found whole in the approved
  draft (`drafts/consent-brief-lean-draft.md`).
- The eighteen consent records that were there before, unchanged by a byte.
- The re-ask: six identities owe the question, three with five sections named and three
  with four; the seventh has answered against the brief as it stands.
- The stations' briefs as a model is sent them are the review's evidence file to the byte.
- All four of the owner's saves here load from their checkpoints; game 10's two are this
  build's own (the same fingerprint of the rules), so nothing in the code or the data has
  changed since they were played.
- Game 9's and game 10's saves carry the stamps the review says.

#### 4.2 Advice, package by package

It is advice. The owner and the repository's session decide.

The packages cannot be taken apart from one another. Each was built on the one before, and
the recorded passages' constants in `tests/test_known_truths.py` were set again by 37d, 37e
and 37f in turn. To hold one is to hold every one after it. So the advice below is to take
all of it, with the changes named, and none of them is a reason to hold.

| Package | Advice | The named change, and why |
|---|---|---|
| **m5c-b (37b, 37c)** | **Take as it is**, inside the whole. | It is in the build unchanged. What the review found wrong in it (the opt-out path, the floor on the log's lines) was mended by 37g and 37f; m5c-b by itself should not be taken without them |
| **37d**, the saves and the sight of land | **Take, with two named changes at the merge.** | (1) Set `BUILD_NAME` for the repository and move the nine test lines that spell it (3.8). (2) Settle the fixture saves before the first commit: the owner's word on the two playtest saves, and an exception to `.gitignore` for the folder (3.9). Left by the package and still so: the dialect will not take cables ("'the nearest land' is compared in miles, not cables", P); `the port` and `the depth of water` still give the true figures, by the plan |
| **37e**, the account | **Take, with one named change before the next game near land in thick weather, and one piece of data.** | (1) A cast of the lead should not move the account beyond the account's own doubt (the review's 11.6, the account, items 1 and 2). It is the one fault of the week that made a sound position unsound in the owner's hands, twice. I did not test the proposed mend. (2) The cruise's scenario line (2.4). Its two lost beats are 37e's doing in the plain sense that the ship now sails as she should; neither is a reason to hold it. Known and left: the three measured figures the brief asked for and did not get (not re-measured by me); the master surer than he should be at anchor in the Bay of Brest; a chronometer further out than its stated doubt displacing a good account |
| **37f**, lying to and the ground | **Take, with the cruise's mark written again.** | The text on `test_the_naval_cruise_speaks_the_stranger` and the paragraph in the changes file should say what the ship does (C1), so that the mend goes to the right place. And the handling fault deserves a line of its own in the work-packages document: a large alteration of course given to the helm alone, by `give chase` or `shape a course for`, leaves a square-rigged ship's yards braced for the old tack. Found in play and not mended, by the review's account: an anchor left aweigh, an anchor she does not carry accepted when the hands are busy, a heave-to that backs a sail being handed |
| **37g**, the station's safety, the deck, the leaving and the grant, with its second pass | **Take, with one named change before a local model is seated again**, and one ruling. | (1) The handover's reserve. As built it took away the margin that game 7 ran on, and both seatings of game 10 ended for it (C7). Until the runner counts tokens by the server's own figure, either put the default back to a share of the context or seat local models with a larger `--handover-reserve`; the review suggests 30,000 and says it is untried. (2) The owner's word on what the general authority keeps back beyond his list (C6). The consent brief should go in exactly as it is (3.9, the fourth trap). Small and left: the replay one line short at a stand-down by the door; the watcher's list of tools; "put the helm over" in the officer's brief, which by the review is not an order (not checked by me) |
| **37h**, the pilot | Not written. | The schooner's pilot waits on it, and so does one of the nine expected failures |
| **The review's section 11 proposals** | Not built; nothing in the build was changed after game 10 (P). | They are the owner's to rule on. Of them, the half-point course is the one I would not leave: the order is accepted and the ship steers six and a half points from what was said, in silence |

#### 4.3 For the owner to decide before the work is folded in

1. Whether the two playtest saves under `tests/fixtures/saves/` go into the repository. They
   are his own games of 4 and 3 October, a model's transcript and his typed lines included.
2. Whether the review folder goes in, whole or in part.
3. Whether Opus 5.5's consent record of 3 October is fetched from m5c-b, so that all eleven
   records made in play are in the repository as the brief says.
4. The additions to what the general authority keeps back (C6).
5. Whether the gate closes with the schooner's pilot still an expected failure, or waits
   for 37h.
6. Where the *Palinure* is put, or whether the scenario should place her from the frigate's
   own position; and whether the handling fault behind C1 and C2 is mended before the cruise
   is played for the gate, since a captain who types `steer NE` from SW by W will meet it.
7. The name the repository's build is to carry in its saves.

## Appendix 1. The ledger

This appendix is the auditor's, carried whole and in its words from Part 1 of
`handover-audit.md`. "I" is the auditor. The marks in the last column say how each row is
known, and A5 explains them: **P**, the auditor ran it; **T**, a test of that name passed in
its run of the whole suite; **R**, it read the code or the document; **D**, from comparing
the folders and the snapshots. "Part 2" is part M of this edition, and "Part 3" and "Part
4", with C1 to C9, are part N. The section numbers it cites (8.1, 8.2, 9, 10.6, 11.6) are
the first edition's, which appendix 2 maps; part I of this edition holds the same
recommendations in the first review's own words.

One row for every recommendation of the review's sections 8, 10.6 and 11.6, every ruling
of its section 9, every numbered item of the four briefs, and every "left undone" in the
changes file. The rows are grouped by where they come from, in that order. Test names are
given without the leading `test_`; all are in `tests/` and all passed in my run.

### 1.1 The review, 8.1: three things to settle first

| Item | State | What I looked at |
|---|---|---|
| The replay of a saved game with a model in it: stamp every save, have `load` say which road it took, treat such saves as good from their checkpoints | **Built** (37d), as the owner ruled on 7 October | R: `core/world.py::build_stamp`, `core/replay.py::check_replay`, `load_report`. T: `another_builds_game_with_a_station_aboard_is_not_replayed_unless_asked`. P: the owner's four saves here load from their checkpoints |
| ... and a replay driven by the transcript | **Not built**; left for milestone 6 by the review's own advice and decision 36 | R: decision 36 |
| One revision of the consent brief, then one re-ask | **Built** (37g and its second pass, both before any model was asked) | D: `ConsentBrief.md` changed at m5c-b, 37g and the second pass and at no other stage. P: digest `288d0b18e34d76a8`; the one record made since is against it |
| One re-measuring of the recorded passages | **Overtaken** by the plan as ruled on 7 October (10.6): they were measured again three times, by 37d, 37e and 37f | R: the comments on `GATE_5C_*` in `tests/test_known_truths.py` |

### 1.2 The review, 8.2: build now. Near land

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | A distance judged afresh when it has changed by a tenth | **Built** (37d) | R: `lookout.py`, `ESTIMATE_REFRESH_FRACTION = 0.1`; `ESTIMATE_HOLD_NM` is gone. T: `the_lookout_judges_a_distance_afresh_as_she_stands_in_from_a_league_to_two_cables`, `an_hour_of_calm_leaves_the_figure_as_it_was` |
| 2 | A single bearing gives a line; the distance by estimation not applied as a measurement | **Built** (37d), then changed twice: laid down when it is the better figure (37d's second pass), and weighed by the one rule (37e) | T: `a_landfall_on_one_mark_lays_the_account_down_by_the_bearing_and_its_distance`, `six_bearings_of_one_mark_lay_the_distance_down_once_and_the_account_does_not_creep` |
| 3 | `take a fix`, open to the officer | **Built** (37d); since 37e it is weighed and takes the near marks; the officer's own since 37g | T: `a_fix_by_two_marks_at_right_angles_brings_the_account_to_the_truth`, `a_fix_by_three_marks_says_the_cocked_hat_...`, `bearings_and_fixes_are_the_officers_own_and_a_sight_is_the_masters`. P: `every glass then take a fix` is entered in the book |
| 4 | No fix from a bearing of a sail | **Built** (37d) | T: `a_bearing_of_a_sail_moves_nothing` |
| 5 | The shore always a sighting; `the nearest land` a reading, in every sample | **Built** (37d). Whether every sample carries it: not checked | R: `chart.py::nearest_shore`. T: `the_shore_is_a_sighting_at_every_look_within_its_limits_and_hailed_once`, `the_nearest_land_is_a_reading_in_the_lookouts_words_and_never_the_charts_metres`. P: "The nearest land: the land about Trefusis Point, on the larboard quarter, bearing SE by E, a cable" |
| 6 | Land ahead: notable under ten minutes, urgent under four | **Built** (37d) | R: `lookout.py`, `LAND_AHEAD_NOTABLE_MIN = 10`, `LAND_AHEAD_URGENT_MIN = 4`. T: `land_ahead_is_notable_under_ten_minutes_and_urgent_under_four_each_once` |
| 7 | The sea breeze's direction from the coast's trend | **Built** (37d) | R: `weather.py`, `SEA_BREEZE_TREND_KM = 3.0`. T: `the_breeze_blows_toward_the_coasts_trend_and_is_scaled_by_its_steepness`, `from_the_harpys_own_weather_the_wind_no_longer_turns_as_the_ship_moves` |
| 8 | The anchor's place taken from the ship's own position | **Built** (37d) | R: `core/world.py::place_of_plane`. T: `an_anchor_let_go_after_a_run_of_sixty_miles_lies_in_the_depth_the_lead_found` |
| 9 | A sight blended unless it is the better figure, and the line says what the master did | **Built** (37e) | T: `the_lunar_of_game_9_moves_the_account_under_two_cables`, `the_words_of_a_cast_a_noon_and_a_bearing_say_which_of_the_three` |
| 10 | The pilot's boat closes with the ship, and keeps closing | **Not built.** It is 37h's, which is not written | T: `the_schooners_pilot_boards_before_she_runs_in` is an expected failure for want of it |
| 11 | The account at anchor, hove to and after a manoeuvre | **Built** (37e) | T: `hove_to_the_master_reckons_her_drift_and_the_run_since_noon_takes_it`, `after_she_fills_away_her_way_is_judged_by_eye_until_the_log_is_next_hove`, `the_doubt_grows_by_the_hour_hove_to_and_becalmed_and_not_at_anchor` |
| 12 | Bearings, the deep-sea lead and `heave the log` in the officer's domain | **Built** (37g for bearings and fixes; the lead and the log were there) | R: `agents/agent.py::OFFICER_DOMAIN` |
| 13 | "Dragging" urgent; a pilot's hail notable | **Built** (37d) | T: `a_dragging_anchor_is_an_urgent_line_and_holding_again_a_routine_one`, `the_pilots_hails_are_notable_lines` |
| 14 | `the port` and `the depth of water` by the captain's means | **Not built**, on purpose: the plan keeps it for last | R: `api/readings.py::_depth_of_water` ("by the chart at the ship's position"). P: both readings answer from her true place |

### 1.3 The review, 8.2: the station and the doors

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | A key to each seating; a second door refused; a line when the door changes | **Built** (37g) | R: `agents/remote.py::_seat`, `held_words`. T (body read): `a_call_without_the_seatings_key_is_refused_in_words_and_nothing_is_run`; `a_call_whose_key_is_refused_stops_the_bridge_and_it_does_not_take_the_seat_back` |
| 2 | The turn budget: the ways out always run; reads apart; said and logged; sixteen | **Built** (37g): sixteen orders, thirty-two reads | R: `harness.py`, `ALWAYS_RUN_TOOLS`. T: `the_ways_out_and_the_stand_by_always_run_whatever_came_before`, `the_officers_orders_are_sixteen_a_turn_and_the_reads_are_counted_apart` |
| 3 | A captain's word in an open turn breaks the stand-by that follows | **Built** (37g) | T: `the_captains_word_in_an_open_turn_breaks_the_stand_by_that_closes_it` |
| 4 | A stand-by with the deck broken by danger, told when its event cannot come, with a bound | **Built** (37g) | T: `a_stand_by_with_the_deck_is_broken_by_danger_refused_what_cannot_end_and_bound` |
| 5 | A paused or silent station gives the deck back; urgent; the clock eases | **Built** (37g) | T: `a_paused_or_silent_officer_does_not_keep_the_deck_and_resume_gives_it_back` |
| 6 | The silence detector counts calls inside an open turn | **Built** (37g) | T: `the_silence_detector_hears_a_call_made_inside_an_open_turn` |
| 7 | The contrary detector: a stand-by clears the chain; the nudge with the order's result; drift counted only within two glasses | **Built** for the first two; the third **overtaken** by item 8: drift is never counted | T: `a_stand_by_that_answers_the_nudge_clears_the_chain_and_no_pause_comes_unread` |
| 8 | ... a link only when the later order undoes the earlier, from a table kept as data | **Built** (37g) | R: `data/vocabulary.yaml`, `undoes:`. T: `what_undoes_what_is_a_table_of_the_vocabulary_and_the_books_rule_is_unchanged`, `the_42_recorded_chains_are_silent_by_the_new_rule_and_set_take_in_set_still_speaks` |
| 9 | The journal read by a tool; the last note and the journal's size in every brief; `read_log` past 200 lines | **Built** (37g). `read_log`'s reach: not checked | T: `the_journal_is_read_back_by_its_writer_newest_first_by_count_tick_and_kind`; body read: `a_released_station_is_taken_by_another_model_with_its_own_consent` (the relief's brief carries the note) |
| 10 | The bridge asks for its station again on a 404; its wait adapts | **Built** (37g) | T: `the_bridge_asks_for_its_station_again_when_the_game_has_none`, `the_bridges_wait_adapts_when_the_client_cuts_a_waiting_call_short` |
| 11 | A sample's lines carry their actor; the captain's orders listed | **Built** (37g) | T: `a_sample_says_who_gave_each_order_and_lists_the_captains_and_the_work_in_hand` |
| 12 | A watcher can stand down with a save | **Built** (37g): `stand_down` for any station | T: `the_three_ways_of_leaving_cannot_be_taken_for_one_another`, `a_stand_down_is_taken_out_of_turn_and_while_paused_and_replays` |
| 13 | An allowance says what it granted; a prefix that allows nothing is refused | **Built** (37g) | T: `a_named_grant_means_what_it_says_and_several_of_one_order_stand_together` |
| 14 | The handover threshold as a reserve in tokens, with a flag; no officer without a context size; the guard on the officer's brief | **Built** as asked, and by the review's own section 11 the first part was wrong advice: it ended both seatings of game 10 | R: `harness.py::handover_threshold`, `HANDOVER_RESERVE_TOKENS = 14000`. T: `the_handover_reserve_is_a_flag_sent_with_the_station_request`, `no_officer_is_seated_without_a_context_size_and_the_guard_measures_his_own_brief` |
| 15 | The mending of 37b's opt-out path | **Built** (37g, item 13) | T: `final_is_read_from_the_tools_own_setting_and_from_nothing_else`, `opt_out_final_is_not_seated_again_and_replays`, `the_agent_api_seats_a_released_station_again_and_holds_an_opt_out_to_its_word` |

### 1.4 The review, 8.2: the log

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | "Aback": a flag for each severity, armed again by state; the per-sail lines once an episode, none for sails backed by order | **Built** (37f) | T: `in_a_calm_her_sails_aback_is_said_once_however_long_it_lasts`, `a_sail_taken_aback_is_said_once_an_episode`, `a_sail_laid_aback_by_order_says_nothing`, `the_urgent_line_has_its_own_flag_and_is_said_though_a_calms_line_stands` |
| 2 | Wind shift: no line in light airs or an unsteady wind; "light and variable" once; the event's floor | **Built** (37f) | T: `the_floor_is_a_light_breeze_by_the_logs_own_scale`, `the_wind_falling_light_is_said_once_and_the_next_settled_wind_once`, `the_event_a_wind_shift_keeps_the_same_floor` |
| 3 | A standing order with nothing to do: one routine line a watch | **Built** (37f) for a condition that does not hold. An action the ship refuses is another matter (the review counts 33 such refusals in game 10; not checked) | T: `a_standing_order_with_nothing_to_do_says_so_once_a_watch_for_each_reason`. P: in the cruise's log "keep her bearing ... not carried out" comes once a watch |
| 4 | A no-bottom cast routine; "a sounding" means bottom found | **Built** (37f) | T: `a_cast_that_finds_no_bottom_is_routine_and_a_sounding_is_bottom_found` |
| 5 | What the officer says with the deck is notable | **Built** (37g), with the deck or without | T: `whose_order_it_was_where_the_officer_is_and_what_he_says` |

### 1.5 The review, 8.2: small faults

| Item | State | What I looked at |
|---|---|---|
| Client: `FATHOM` defined; the track's hourly points; bearing lines faded; the captain's markers named; the anchor in the snapshot | **Not built.** Nothing under `client/` has changed | D. R: `client/map.js` line 450 uses `U.FATHOM`, and no file under `client/` defines it |
| Boats: one state machine; a refused order not moving the person; the refusal saying the two-mile rule | **Not built**; put off by 37f's brief | D: no file of the boats changed. Not probed |
| Numbers: one reader for numbers in words | **Not built**; put off by 37f's brief | Not checked beyond the brief |
| Sails: `take in`, `furl`, `lower`, `clew up` reach the water sail and the jibs | **Could not tell.** No package claims it and I found no change for it; not probed | D: `orders/verbs.py` changed in 37f only |
| Hove to: the flag cleared by anchoring, weighing and tacking | **Built** (37f) | T: `the_record_is_cleared_when_an_anchor_is_let_go_and_when_she_takes_the_ground`, `the_record_is_cleared_by_a_tack_and_by_a_wear`, `lain_a_try_anchored_and_weighed_she_takes_a_course_at_the_first_order` |
| ... the starter book's trim rule guarded; `trim sails` declining hove to | **Built** (37f) | R: `data/standing_orders/starter.orders` lines 77 and 88. T: `every_shipped_trim_rule_carries_the_dialects_own_guard`, `trim_sails_is_declined_while_she_is_hove_to_in_words_that_carry_the_cure` |
| ... a hove-to ship that fills and gathers way says so, urgently | **Built** (37f) | T: `forced_round_by_a_shift_one_urgent_line_says_so_and_the_record_follows_her`, `a_brig_under_her_topsails_alone_that_falls_off_is_said_to_be_hove_to_no_longer` |
| Getting under way: the fore-and-aft cast; never "paid off" on a timeout | **Built** (37f) | T: `a_fore_and_after_casts_on_the_tack_ordered`, `paid_off_is_never_said_on_a_timeout` |
| Tacking: a tack that could not begin says why, not in the words of a missed stay | **Not built**; put off by 37f's brief | P: in my trial a tack ordered from off the wind was answered "Squared the yards; she fell off on the starboard tack, to try again or to wear" |
| The anchor: `heave in 70 fathoms`; `come to an anchor in twelve fathoms`; "Brought up" after `let go`; warnings for scope and draught | **Built** (37f) | P: `heave in 10 fathoms` taken; "Brought up by the best bower in 17 fathoms". T: `come_to_an_anchor_in_twelve_fathoms_stands_on_till_the_lead_calls_it`, `the_water_at_low_water_is_set_against_her_draught_as_the_anchor_goes` |
| At anchor and aground: the 26 refused verbs gone through; `furl all sail` at least | **Built** (37f). I did not count the verbs | P: at anchor `square the yards` is taken and `steer N` is refused. T: `a_ship_at_anchor_may_hand_her_sails_and_square_her_yards`, `a_ship_aground_may_do_the_same_and_no_manoeuvre` |
| The filter: `take in twenty tons of water` must not pass as the port's order | **Not built** | P: it is answered "She is not in port; there is no yard to demand it of" |
| Papers: her draught; `the prices` showing every list; port names without regard to case | **Not built** as far as I found; not probed | D: no change in the papers' or the ports' code but one severity |
| The carpenter reports the well | **Not built** as far as I found; not probed | D |
| Replay: an officer seated at tick 0 replays in his place | **Built** (37d) | R: `harness.py`, `stationed_after_inputs`. T: `an_officer_seated_at_tick_0_after_a_drivers_line_replays_in_his_place` |
| Words: 1805, not 1806, in the brief and primer 16 | **Not built** | P: the officer's brief as sent still says "as a lieutenant of 1806" |
| Words: "the breakwater" out of the Plymouth pilot's mouth | **Not built** | R: `data/ports/plymouth.yaml` line 52 |
| Words: the gate's "£6,000" | **Not built** | R: `docs/gates/gate-m5c.md`, item 1 |
| Words: hints that do not send `hail` to `haul` | **Not built** | P: `hail the pilot` is answered "did you mean 'haul'?" |

### 1.6 The review, 8.3: build after a ruling

| # | The matter | State | What I looked at |
|---|---|---|---|
| 1 | A general grant | **Built** (37g), on the rulings of 5 and 7 October. It keeps back more than the list on record (Part 4, C6) | R: `agent.py::_GENERAL`, `_KEPT_BACK`. T: `the_general_grant_opens_the_ships_working_and_keeps_back_what_it_keeps` |
| 2 | The emergency route | **Built** (37g, item 19), kept by the owner on 7 October | R: `agent.py::_DANGER`. T: `the_way_out_of_danger_is_the_officers_own_word_for_the_helm_a_heave_to_and_an_anchor` |
| 3 | Whether `say` ends a turn | **Not ruled, not built** | R: 37g's brief, "Not in 37g" |
| 4 | The pilot taken or declined; what he does aboard | **Ruled** (5 and 7 October); **not built**: 37h is not written | P: `hail the pilot` and `decline the pilot` are not orders; `take the pilot` is read as the reading `the pilot` |
| 5 | The master's own fixes in pilot waters | **Overtaken** by the ruling of 5 October: `take a fix` is an order, not a routine | section 9, answer 7 |
| 6 | Relief by another model | **Ruled**; **built** (37g) | T (body read): `a_released_station_is_taken_by_another_model_with_its_own_consent` |
| 7 | What a ship knows of another port's trade | **Not ruled, not built** | no brief holds it |
| 8 | The boat's errands | **Not ruled, not built** | no brief holds it |
| 9 | The well and the pumps | **Not ruled, not built** | no brief holds it |
| 10 | A late reply | **Not ruled, not built** | R: 37g's brief, "Not in 37g" |
| 11 | Who may ask a station back after a welfare stand-down | **Could not tell** whether it was ruled apart from relief. The build has one rule for every released station | R: `harness.py::seating` |

### 1.7 The review, 8.4: needs design work first

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | A replay driven by the transcript | **Not built**; milestone 6 | decision 36 |
| 2 | The con | **Not built** as a thing apart. Taking the deck now leaves the officer seated, which the review offers as the captain's way to take the con | T: `you_have_the_deck_gives_it_and_i_have_the_deck_takes_it_and_no_more` |
| 3 | Stand by until x, or y, or z, with the dialect's conditions | **Not built** | no brief holds it; not probed |
| 4 | Features by their parts, and how marks stand to one another | **Not built** | 37d's brief, "Not in 37d" |
| 5 | The pilot as a voice | **Overtaken**: ruled later work, with the director (section 9, answer 6) | |
| 6 | What a sample carries | **Not built.** The review's section 11 says the samples have grown | not checked |
| 7 | Image tools | **Not built** | |
| 8 | The drill for a station with authority | **Not built**; "design first" in 37g's brief | the review says the drill miscounted in game 10; not checked |

### 1.8 The review, 8.5 to 8.8

| Item | State | What I looked at |
|---|---|---|
| 8.5, 1: no rule that shrinks the doubt because land is near | **Followed**, as far as I read: the doubt is moved by the run, the streams and observations | R: the constants and comments at the head of `world/reckoning.py`; not read through |
| 8.5, 3: the anchor inside a general grant | **Followed** | R: `agent.py::_GENERAL` holds `object:anchor` |
| 8.5, 4: no `keep` prefix; mend `trim` and ship `at steady on the course then trim sails` in the starter book | No `keep` prefix was built. `trim` hove to is mended (37f). The starter book has **no** `at steady on the course` rule | R: `data/standing_orders/starter.orders` |
| 8.5, 5: mend the sea breeze, not a minimum wind | **Both were done**: the sea breeze (37d) and a floor of four knots on the line (37f) | 1.2 item 7; 1.4 item 2 |
| 8.5, 6: the journal stays in the context; give the station its journal to read | **Followed** (37g) | 1.3 item 9 |
| 8.5, 7: the budget's counting before its size | **Both were done** (37g) | 1.3 item 2 |
| 8.5, 8: bind a door to its station before several stations through one door | **Followed** (37g) | 1.3 item 1 |
| 8.5, 9: no image tools now | **Followed** | |
| 8.5, 11: "taken aback" is not only noise | **Followed**: the urgent line keeps its own flag (37f) | 1.4 item 1 |
| 8.5, 2 and 10, and the points on the model's additions and on m5c-b | Judgements, not things to build | |
| 8.6: nothing of a later milestone pulled forward | **Followed**, as far as the briefs and the diff show | D |
| 8.7, 1: the officer's domain: bearings, the deep-sea lead and the log; a course change judged by its effect; the danger exception | **Built** (37g) | T: `an_order_that_changes_her_course_is_the_course_whatever_its_words`; 1.6 item 2 |
| ... `fill away` after a heave-to he did not order; heaving in with weighing and veering | **Not built** as the officer's own: both want the captain's word, by name or by the general authority | R: `agent.py::OFFICER_DOMAIN.refused` |
| 8.7, 2: no officer seated when the server reports no context size | **Built** (37g) | 1.3 item 14 |
| 8.7, 3: a far-detail vessel's leg across the coast refused at loading | **Not ruled, not built** | Part 2, item 14 |
| 8.7, 4: batch the brief's changes; a larger drill | The first **built**; the second **not built** | 1.1; 1.7 item 8 |
| 8.8, steps 1 and 2: the saves; near land, the sea breeze, the anchor's place, the schooner's cast | **Built** (37d; the cast in 37f) | above |
| 8.8, steps 3 and 4: the station's safety; the brief's one revision | **Built** (37g) | above |
| 8.8, step 5: the log's noise and the small faults | The noise **built** (37f); the small faults **partly**: see 1.5 | |
| 8.8, step 6: play what the gate still lacks | **Not done**, by the review's own account | cannot be checked from the tree |

### 1.9 The review, section 9: the owner's answers and rulings

| Ruling | State | What I looked at |
|---|---|---|
| 1. Replay: "save is exact from the checkpoint, replay is promised only on the build that made it" (7 October) | **Built** (37d). The promise itself is not quite kept for game 10's last save, which replays one line short on its own build (Part 4, C7) | 1.1. P: `saves_check.py` |
| ... stamp every save and checkpoint with its build | **Built** | P: the saves of games 9 and 10 carry `m5c-c/37d` and `m5c-c/37g` with their fingerprints |
| ... `load` refuses to replay another build's game with a model aboard unless told to | **Built** | T: `the_cutters_save_is_refused_a_replay_without_the_flag`, `every_door_that_loads_or_replays_says_the_same_words_and_takes_the_flag` |
| ... two or three of the playtest's checkpoints kept as tests | **Built** in this folder; at risk at the merge (Part 3, 3.9) | T: `a_playtest_save_loads_from_its_checkpoint_and_runs_on_a_glass` (two saves), `the_packages_own_save_loads_from_its_checkpoint_and_runs_on_a_glass` |
| 2. The gate's verdict waits on the naval cruise and the lead's watch | **Stands.** Neither has been done, by the review's account, and the cruise does not come through (Part 2) | P |
| 3. A save lies in the folder of the build that played it | **Followed** | D: the saves of m5c and m5c-b were not brought over; this folder's eight are games 9 and 10 |
| 4. The grant: what stays out, and when it lapses (5 and 7 October) | **Built** (37g), with more kept back than the list on record | 1.6 item 1; Part 4, C6. T for its life: `the_general_grant_opens_the_ships_working_and_keeps_back_what_it_keeps` |
| 5. The deck: `you have the deck` and `I have the deck` do not unseat the officer | **Built** (37g) | T: `the_deck_is_taken_and_given_three_times_with_the_station_seated_throughout` |
| ... the officer's own `hand_over` gives the deck back and he stays | **Built** | T: `hand_over_gives_the_deck_back_with_the_note_and_the_officer_stays` |
| ... a `stand_down` tool for any station | **Built** | 1.3 item 12 |
| ... the readings say "off watch"; what he says is notable with the deck or without | **Built** | T: `whose_order_it_was_where_the_officer_is_and_what_he_says` |
| 6. The pilot: taken or declined by an order; aboard he warns; unanswered he keeps company, hails once more and bears away (5 and 7 October) | **Not built.** 37h is not written | 1.6 item 4 |
| 7. `take a fix` is an order, not a routine | **Built** (37d) | 1.2 item 3 |
| 8. Relief: a station stood down may be taken by the same model or another | **Built** (37g) | 1.6 item 6. T: `a_station_left_in_a_playtest_save_is_taken_again_by_the_one_rule` |
| ... a final opt-out bars the model, not the station; the relief may read the journal (7 October) | **Built** | T: `opt_out_final_is_not_seated_again_and_replays`, `the_journal_is_read_back_by_its_writer_newest_first_by_count_tick_and_kind` |
| 9. The consent record of 3 October stands; every identity is asked again at the one revision | The re-ask is **built**. The record itself is not in this folder (Part 3, 3.7). Opus 5.5 was in fact asked again on 6 October, for game 9, because this folder did not hold that record, as the changes file said it would be | P: `consent_check.py`; the record of 6 October names the brief `f667a04e00b32e1f` |
| 10. The watcher's `opt_out` on the *Harpy* was not a withdrawal | **Recorded** in the review and in `Harness.md`; a save from before 37b reads such a leaving as a stand-down | R: `docs/agents/Harness.md` line 276; `harness.py::_leavings` |
| The way out of danger, kept as proposed (7 October) | **Built** (37g) | 1.6 item 2 |
| The approvals of 7 October: 37e, 37f, 37g | **All three built** | Part 3 |
| The work done locally, with no commits | **Followed**, as far as a folder can show: the build folder is not a repository | I ran no git command |

### 1.10 The review, 10.6: what game 9 changed in the plan

| Item | State | What I looked at |
|---|---|---|
| The rule, 1: an observation is weighed against the account by their two doubts | **Built** (37e) | T: `one_rule_an_observation_is_weighed_by_the_two_doubts_whatever_the_run` |
| The rule, 2: when they disagree by more than their doubts allow, the observation is taken | **Built**, with two for the brief's three (Part 4, C8) | R: `reckoning.py`, `OBSERVATION_OUT_SIGMAS = 2.0`. T: `one_rule_an_observation_is_taken_when_the_account_is_plainly_out` |
| The rule, 3: the doubt grows whether she has way or not, fits the streams, and is not narrowed by the same thing seen again | **Built** (37e) | T: `the_doubt_grows_by_the_hour_hove_to_and_becalmed_and_not_at_anchor`, `the_doubt_of_the_stream_grows_along_its_set_...`, `the_same_thing_seen_again_tells_him_nothing_new`, `eight_casts_in_a_calm_over_the_flat_sand_off_ar_men_narrow_nothing` |
| The rule, 4: a fix chooses the tightest marks, counts the compass's shared error, and at anchor a poorer fix does not move the account | **Partly built.** All three are in. Still missing, by the builder's own note and the review's 11.3: a fix whose marks lie on one hand claims too much | T: `in_the_goulet_the_master_takes_the_near_marks_before_camaret_brest_and_conquet`, `over_the_geometry_of_game_9s_fixes_good_to_is_honest`, `moored_in_brest_road_a_fix_by_far_marks_leaves_a_sound_account_where_it_was` |
| The owner's ruling: (b), the master works the tide himself, now | **Built** (37e) | T: `the_master_works_the_tide_into_the_traverse_as_one_more_course`, `no_line_of_the_masters_tide_reads_the_worlds_tide_or_the_ships_true_place`, `the_masters_tide_is_his_own_two_ships_ten_miles_apart_work_the_same_tide`. P: the cruise's noon line, "The day's work carried the master's tide by the directions and the epitome" |
| Ruled: where the study has no period source, the set to the nearest point and the spring rate to the half knot, as judgement | **Built** (37e) | T: `the_directions_state_every_water_in_the_periods_form_beside_the_worlds_figures`. The figures themselves not read |
| Ruled: `shape a course` steers to make good by default | **Built** (37e) | T: `a_course_shaped_across_a_stream_lies_up_tide_by_the_triangle_and_makes_the_place`. P: "Allowing the ebb, a knot to the SW, steer S by W to make it good" in the cruise's log |
| Ruled: the captain's `allow ... knots of set` replaces the master's tide until handed back | **Built** (37e) | T: `the_captains_set_replaces_the_masters_tide_until_he_hands_it_back`. R: `data/vocabulary.yaml`, `allow the tide by the book` |
| A model working the reckoning: now, no prompt | **Followed**: nothing was built | |
| ... an officer's reckoning of his own beside the master's | **Not built**; "Not in 37e" | |
| The package built as two, the account and then lying to and the ground | **Done** as ruled | Part 3 |
| `shape a course` says when its line crosses or skirts the shore | **Built** (37e) | T: `a_course_shaped_across_a_headland_or_close_along_the_shore_says_so` |
| The land-ahead cry says how near she will pass | **Not built**: I found no such words | R: `world/lookout.py` (the cry says where it lies, its distance and the minutes) |
| The station-safety package: the detector first | **Built** (37g) | 1.3 items 7 and 8 |
| The chart in words | **Not built**; design first | |
| A fog signal | **Not built**; later | |
| For the gate's checklist: what game 9 added | A statement about play; not checked | |
| The plan as ruled: 37e, 37f, 37g, one at a time; the pilot is 37h | 37e, 37f and 37g **built** in that order; 37h **not written** | D: the snapshots |
| 37f's three rulings: `loose` stays; `trim sails` declines hove to; `let go` keeps its scope, says it and takes a number | **Built** (37f). `loose`: no change found, not probed | T: `trim_sails_is_declined_while_she_is_hove_to_...`, `let_go_says_what_it_will_do_as_the_order_is_given`, `let_go_takes_a_scope_and_veers_to_that_and_no_further` |
| Pushing back: build the ground tackle from the table in 10.4, not from the officer's list | **Followed**, by 37f's brief | R: the brief, items 5 to 9 |
| Pushing back: the land-ahead cry not made milder | **Followed**: ten minutes and four, unchanged | R: `lookout.py` |

### 1.11 The review, 11.6: what game 10 changed in the plan

Nothing in this list is built. Nothing at all in the code or the data has changed since
game 10 was played: its two saves carry the fingerprint the build has today (P).

| Item | State | What I looked at |
|---|---|---|
| The runner, 1: a reply cut off while the model was thinking is not passed on as its turn | **Not built** | R: `agents/local.py` nowhere reads why a reply ended |
| The runner, 2: tokens counted by the server's own figure | **Not built** | R: `local.py`, `CHARS_PER_TOKEN` throughout |
| The runner, 3: the reserve as a share of the context as well as a number | **Not built** | R: `harness.py::handover_threshold` |
| The runner, 4: on a refusal for size, leave out the oldest exchanges and ask again | **Not built**; not checked in the code | |
| The runner, 5: the line the replay drops at a stand-down by the door | **Not built**; the fault is real | P: my replay of the save, 4,239 lines for 4,240 |
| Until then: `--handover-reserve 30000` and a larger `--max-reply` | Both flags exist; neither tried, by the review or by me | R: `local.py` lines 812 and 830 |
| The account, 1: the master allows the tide's height for the lead by his book | **Not built**; the cause not checked in the code | |
| The account, 2: a cast never moves the account beyond its own doubt | **Not built** | |
| The account, 3: the account worked at every tack, wear, heave-to and large alteration | **Not built** | |
| The account, 4: a fix's doubt when its marks lie on one hand | **Not built** | 1.10 |
| The ground and the helm: an anchor at the bows can be let go; a belay says where it left the anchor | **Not built**; not reproduced by me (Part 4, C7) | P |
| ... an anchor the ship does not carry is refused at the order | **Partly so already**: refused at once when nothing is in hand, accepted when the hands are at other work | P |
| ... a heave-to backs a sail that is set; the alarm leaves sail still being made alone; a lifting sail said first; anchoring in forty fathoms looked at | **Not built**; not checked | |
| Words: a course with a half point | **Not built**; the fault is real | P: "steer west; W (270°)" |
| Words: the fog reading's sentence; "put the helm over"; the phrasings in 11.4; the drill's count | **Not built**; not checked | |
| Words: a standing order's action read when it is given | **Partly so already**: its first word is read, the rest is not | P |
| For 37h: the depths in St Mary's Sound; the dangers shown by name; a pilot aboard three times who takes her nowhere | 37h **not written** | |
| The consent brief stands as approved | **So**: unchanged since the model of game 10 answered against it | P: digest `288d0b18e34d76a8` in the brief and in the record of 7 October |

### 1.12 The brief of 37d, item by item

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | The build's stamp: a name and a fingerprint of the rules in every save and checkpoint | **Built** | R: `core/world.py::fingerprint_of`, `build_stamp`. T: `a_save_and_its_checkpoint_carry_the_builds_stamp`, `the_fingerprint_is_of_the_code_and_the_data_and_not_of_the_line_endings`. The cost at start: the builder's figure, not timed by me |
| 2 | `load` says what it did, and does not replay another build's game with a model aboard unless told to; every door the same words and `--replay-anyway` | **Built** | R: `core/replay.py::load_report`, `check_replay`. T: `load_says_which_road_it_took_and_why_a_checkpoint_was_not_taken`, `every_door_that_loads_or_replays_says_the_same_words_and_takes_the_flag` |
| 3 | A station seated at tick 0 replays in its place | **Built** | 1.5 |
| 4 | Old checkpoints kept as tests: two of the playtest's and one of the package's own | **Built** | P: the two playtest saves are the owner's own, byte for byte. T: 1.9. R: the playtest saves' tests skip when the files are missing; the package's own fail |
| 5 | The lookout judges a distance afresh as it changes | **Built** | 1.2 item 1. T: `a_sail_whose_distance_halves_is_said_nearer_and_the_closing_hail_is_fresh` |
| 6 | A bearing gives a line; second pass, the distance laid down when it is the better figure | **Built**, then **overtaken** in its rule by 37e's item 1 | 1.2 item 2 |
| 7 | A sail is no mark | **Built** | 1.2 item 4 |
| 8 | `take a fix`: its forms, its marks, its refusals, its words | **Built**. Two of its particulars **overtaken**: the fix no longer sets the account outright (37e), and the officer no longer needs `you may take a fix` (37g) | T: `take_a_fix_is_a_navigation_order_with_the_words_a_seaman_would_type`, `take_a_fix_is_completed_from_the_marks_in_sight`, `a_fix_is_refused_in_words_that_carry_the_cure`, `two_worlds_of_one_seed_say_the_same_fix_and_another_seed_another`, `the_standing_dialect_has_take_a_fix_for_nothing` |
| 9 | The shore always a sighting; `the nearest land` a reading; `Chart.nearest_shore` | **Built** | 1.2 item 5. T: `the_nearest_shore_is_the_ground_itself_beside_a_plain_search`, `the_nearest_land_says_none_within_a_league_and_not_to_be_seen` |
| 10 | Land ahead | **Built** | 1.2 item 6. T: `land_ahead_comes_again_after_the_quiet_and_not_at_anchor_without_way_or_in_fog`, `a_danger_ahead_is_named_and_where_it_lies_is_said_from_her_head`. The counts by passage are in `TuningNotes.md`; not checked |
| 11 | Two severities: dragging urgent, the pilot's hails notable | **Built** | 1.2 item 13 |
| 12 | The sea breeze blows from the sea | **Built** | 1.2 item 7. T: `the_coasts_trend_never_turns_two_points_between_samples`, `off_an_open_coast_the_trend_is_square_on_to_the_land_and_flat_in_a_road`. The tick rate before and after: not checked |
| 13 | One frame for the plane's points | **Built** | 1.2 item 8. T: `the_coasts_distance_at_the_ship_is_the_charts_at_her_position_after_a_long_run` |
| 14 | The recorded passages re-measured once, with the reasons | **Built**; the constants were set again by 37e and 37f. The table of reasons is in `TuningNotes.md`; I did not check it line by line | T: the six recorded passages' tests pass on today's constants |
| 15 | The documents | **Built**, by the list of files; I did not read them against the code | D: every document the item names changed at 37d |
| 16 | The report | Made to the lead; not in the tree. Not checked | |
| | Rule: every new field on a checkpointed class has a plain default | **Holds**, by its proof | T: the fixture tests |
| | Rule: nothing in the consent brief or a station's brief changes | **Holds** for the consent brief. Not checked for the stations' briefs | D: `ConsentBrief.md` unchanged at 37d |

### 1.13 The brief of 37e, item by item

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | One rule for every observation: weighed, taken or kept, and the words say which | **Built**, with two where the brief said three; `FIX_RUN_NM` is gone | 1.10. T: `the_noon_of_game_9_is_taken_and_against_an_account_a_mile_out_it_is_weighed`, `a_bearing_of_a_light_eleven_miles_off_after_twelve_miles_of_doubt_lays_the_line_down`, `the_words_of_a_cast_a_noon_and_a_bearing_say_which_of_the_three`. P: in the cruise's log, "the reckoning was out by it; laid down by the observation" and "the account moved a mile to the NE by N" |
| 2 | The doubt, honest: by the hour with or without way; sized by the water; the same thing seen again; said in cables and with its lie | **Built** | 1.10. T: `the_doubt_is_said_in_cables_under_a_mile_and_with_its_lie_when_long_and_thin`, `the_master_doubts_his_log_line_and_his_compass_in_the_run` |
| 3 | `take a fix` by the marks that fix her best; an honest "good to"; weighed as any observation | **Partly built**: all in, but marks all on one hand still claim too much | 1.10. R: `COMPASS_ALLOWANCE_DEG = 2.5`, `..._OBSERVED_DEG = 1.5` |
| 4 | The account hove to, becalmed and after | **Built** | 1.2 item 11. R: `HOVE_TO_DRIFT_KN = 0.25` |
| 5 | What the directions say of each water | **Built** | D: `data/tides/streams.yaml`, 126 lines added. T: `the_directions_state_every_water_in_the_periods_form_beside_the_worlds_figures`, `the_directions_are_looked_up_by_a_position_and_say_nothing_beyond_their_limits` |
| 6 | The tide in the traverse | **Built** | T: `the_master_works_the_tide_into_the_traverse_as_one_more_course` |
| 7 | The proof that it is his own | **Built** | T: `the_masters_tide_is_his_own_two_ships_ten_miles_apart_work_the_same_tide`, `a_master_with_moores_table_works_another_hour_from_one_with_nories`, `no_line_of_the_masters_tide_reads_the_worlds_tide_or_the_ships_true_place` |
| 8 | The captain's word and the master's: the three forms of `allow`; he says what he allows; the line and the event when his tide turns | **Built** | T: `the_three_forms_of_allow_are_offered_and_each_is_taken_and_logged_as_whose_it_is`, `the_log_says_when_the_masters_tide_turns_and_when_she_passes_into_other_waters`, `the_reckonings_reading_carries_the_tide_allowed_and_the_doubt_as_it_stands_now`. P: "the tide allowed: none while she rides at anchor" |
| 9 | A shaped course makes good; worked once; the line tried against the shore | **Built** | 1.10. T: `a_course_shaped_by_the_masters_own_tide_makes_the_place_where_the_tide_is_the_books`, `a_course_shaped_with_no_way_on_or_against_too_strong_a_stream_says_so` |
| 10 | The recorded passages re-measured once | **Built**; set again by 37f | as 37d's item 14 |
| 11 | The books tuned for a true account; a passage that will not come through marked a strict expected failure and reported | **Partly built.** The merchant's book is tuned and takes its fix again (the passage's test asks twelve fixes in pilot water). Two beats were lost and marked, as the item allows: the schooner's pilot, the cruise's brig | T: `the_merchant_passage_at_seed_7_has_its_own_constants`; the two expected failures. "The Mingan passed by not less than a cable and a half": the builder's figure is 1.9 cables; not measured by me |
| 12 | The proof by measurement | **Partly built**: measured and reported, with three of the four things asked not met, as the changes file says. Not measured again by me, and not measured by anyone since 37f moved the passages | T for the fourth: `the_brig_hove_to_six_hours_of_a_spring_ebb_in_the_iroise_keeps_an_honest_account` |
| 13 | The documents | **Built**, by the list of files; not read against the code. One sentence left: the spec's truth 59 still says a cast "moves the reckoning onto the chart's contour" | D. R: `docs/TechnicalSpec-M5.md` line 742 |
| 14 | The report | Made to the lead; not checked | |
| | Rule: no line of the master's tide reads the world's tide or the ship's true place | **Holds**, by its test | item 7 |
| | Rule: the mere asking of a reading changes nothing (found and mended on the way) | **Holds**, by its test | T: `a_reading_of_the_account_asked_mid_tick_changes_nothing_another_gets_after_it` |

### 1.14 The brief of 37f, item by item

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | Heaving to that holds its tack: the way taken off first; she is kept there; forced round, one urgent line; every rig | **Built.** The fore-and-afters forereach more than the knot and a half asked, by the builder's own note | T: `the_brig_brought_to_from_each_of_the_games_states_holds_her_tack`, `held_six_hours_through_shifts_and_all_winds_she_never_lies_abaft_the_beam`, `a_fore_and_after_brought_to_holds_her_tack_in_her_own_manner`, `the_tending_costs_the_watch_its_hands_and_the_relief_takes_them_over`. P: "Hove to on the starboard tack, main topsail to the mast, helm a-lee" in the cruise's log |
| 2 | `fill away` on the tack she is on; `fill away and steer <course>` | **Built** | T: `fill_away_fills_her_on_the_tack_she_is_on`, `a_ship_that_has_come_round_is_filled_on_her_new_tack_not_the_recorded_one`, `fill_away_and_steer_gives_the_helm_the_course_when_she_is_full` |
| 3 | The record that she is hove to, cleared | **Built** | 1.5. T: `the_reading_and_the_dialects_guard_read_the_one_record` |
| 4 | `trim sails` hove to; the shipped books' guard | **Built** | 1.5. T: `the_starter_books_trim_rules_sleep_through_a_heave_to_and_wake_after_it`. The review's 11.4 notes the guard does not cover lying at anchor |
| 5 | An anchor's name is honoured by `veer`, `heave short`, `heave in` and `weigh` | **Built** | T (body read): `the_cable_worked_is_the_named_anchors_and_to_is_kept`; `the_refusals_name_the_anchor_she_rides_by_and_what_would_do_it`, `weigh_weighs_the_anchor_named_and_says_what_she_rides_by` |
| 6 | "To" is kept when an anchor is named | **Built** | the same test, twelve forms |
| 7 | `let go` says its scope and takes one; the warning | **Built** | P: "Let go the best bower in 17 fathoms; veering to eighty-six fathoms, five times the depth". T: `the_scope_is_warned_of_when_she_will_swing_within_a_cable_of_the_land`, `the_scope_is_warned_of_when_it_is_more_than_the_cable_she_has` |
| 8 | `heave in`; `heave short` takes no number | **Built** | P: both, as the item says |
| 9 | The dragging line: urgent once, then notable with how far; "holds again"; a slack cable; the advice | **Built.** A drag that relapses on bare rock is still an urgent line each time, by the builder's note | R: `core/world.py::_dragging_advice`. T: `a_dragging_is_urgent_once_and_then_says_how_far_she_has_come`, `the_goulets_eight_hours_give_at_most_five_lines_the_first_urgent`, `the_advice_names_only_what_is_left_to_do` |
| 10 | The ground's words: two grounds as their mean; a note for every port's road | **Built** | T: `a_note_of_two_grounds_is_the_mean_of_them_and_not_the_worst`, `every_ports_road_and_anchorage_has_its_note_of_the_bottom` |
| 11 | Three small anchoring faults | **Built** | 1.5 |
| 12 | What a ship at anchor may do | **Built** | 1.5 |
| 13 | The fore-and-aft cast | **Built** | 1.5. T: `a_cast_the_wrong_way_is_said_and_she_is_got_under_way_on_that_tack`, `the_square_riggers_cast_as_they_did` |
| 14 | No wind-shift line in airs too light to have a direction | **Built** | 1.4 item 2. T: `a_calm_that_boxes_the_compass_logs_no_shift`, `a_wind_that_swings_back_and_forth_is_unsteady_and_is_said_so_once` |
| 15 | The aback lines, by state | **Built** | 1.4 item 1 |
| 16 | A "could not" that is no failure | **Built** | T: `queued_work_that_finds_it_done_already_is_a_routine_line_and_no_failure`, `queued_work_that_cannot_be_done_is_a_failed_evolution_still`. P: at anchor `furl all sail` is answered "Every sail is furled already" |
| 17 | A no-bottom cast routine; a standing order with nothing to do, once a watch | **Built** | 1.4 items 3 and 4 |
| 18 | A standing order's condition checked when it is entered | **Built** | P: "the distance to the land" is refused at entry with the forms that serve. T: `the_distance_to_the_land_is_refused_at_entry_with_the_forms_that_serve`, `a_name_the_chart_nearly_has_is_answered_with_that_name`, `the_shipped_books_enter_whole` |
| 19 | The recorded passages re-measured once | **Built**; these are the constants the suite pins today | T: the six passages' tests |
| 20 | The documents | **Built**, by the list of files; not read against the code | D |
| 21 | The report | Made to the lead; not checked | |
| | Ruling: `loose` stays as it is | **Followed**, as far as the diff shows; not probed | |

### 1.15 The brief of 37g, item by item

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | A key to each seating | **Built** | 1.3 item 1 |
| 2 | The turn's budget | **Built** | 1.3 item 2 |
| 3 | The captain's word in an open turn | **Built** | 1.3 item 3 |
| 4 | The stand-by with the deck | **Built** | 1.3 item 4 |
| 5 | The contrary-orders detector; the test on the record | **Built** | 1.3 items 7 and 8. T: `orders_that_undo_one_another_bring_the_nudge_then_the_pause`. The review says it spoke not once in game 10 |
| 6 | The silence detector | **Built** | 1.3 item 6 |
| 7 | A paused or silent officer does not keep the deck | **Built** | 1.3 item 5 |
| 8 | The doors: the bridge asks again; the handover's reserve; no officer without a context size; the guard on his own brief | **Built** as briefed; the reserve is the fault of game 10 | 1.3 items 10 and 14. T: `the_handover_is_asked_for_at_a_reserve_in_tokens_and_of_an_officer_off_watch` |
| 9 | What a sample tells; the reading `the work in hand` | **Built** | 1.3 item 11. P: "The work in hand: doing: heaving in" |
| 10 | Whose order, and where the officer is | **Built** | R: `orders/navigation.py::_whose`. T: `whose_order_it_was_where_the_officer_is_and_what_he_says` |
| 11 | The deck, given and taken | **Built** | 1.9 |
| 12 | Three ways of leaving | **Built** | T: `the_three_ways_of_leaving_cannot_be_taken_for_one_another`. P: the officer's brief as sent says them in three lines |
| 13 | The opt-out path, mended | **Built.** One door short: the REPL's turn mode does not put the question again; it says so and seats nobody | 1.3 item 15. R: `agents/repl.py`, the module's own account; `harness.py::seating`. T: `the_repl_seats_a_released_station_again_by_the_games_one_rule` |
| 14 | Relief | **Built** | 1.6 item 6 |
| 15 | The journal, read | **Built**; `read_log`'s reach not checked | 1.3 item 9 |
| 16 | The officer's domain, as drawn | **Built** | R: `agent.py::OFFICER_DOMAIN`. T: `bearings_and_fixes_are_the_officers_own_and_a_sight_is_the_masters`, `an_order_that_changes_her_course_is_the_course_whatever_its_words` |
| 17 | A named grant means what it says | **Built** | 1.3 item 13. T: `the_captains_word_allows_a_named_thing` |
| 18 | The general grant | **Built**, keeping back more than the brief's five (Part 4, C6). "What cannot be undone" is one order today, `cut away`, and it was the officer's already, by the builder's note | R: `agent.py::_GENERAL`, `_KEPT_BACK`; `data/vocabulary.yaml`, `you may work the ship`. T: 1.6 item 1 |
| 19 | The way out of danger | **Built** | 1.6 item 2 |
| 20 | The consent brief's one revision | **Overtaken** by the owner's word of 7 October (decision 37): the four sections' approved words went in, and were then replaced by the leaner brief before any model was asked | P: the brief's body is found whole in `drafts/consent-brief-lean-draft.md`; 1,371 words |
| 21 | The station's brief and the doors' words | **Built** (second pass). Left: the watcher's brief lists three tools a watcher is refused; the officer's brief still says "1806" | P: both briefs written out afresh; they are the review's evidence file to the byte. T: `what_moved_out_of_the_consent_brief_is_in_the_briefs_of_the_stations` |
| 22 | The re-ask, proven | **Built** | T: `a_yes_given_before_the_briefs_revision_is_asked_again_and_the_question_says_why`. P: by the rule, six identities are asked again and one is not |
| 23 | The documents; the decisions log; every document that still states the old re-seating rule found and mended | **Built** for the decisions log (34 to 37; decision 33 is marked superseded). Not mended: the gate's headline item 6 still says "a second seating once" beside the new parenthesis. The rest not read against the code | R: `docs/DesignProposal.md` lines 622 to 630; `docs/gates/gate-m5c.md` line 18 |
| 24 | The report | Made to the lead; not checked | |
| | Rule: no model is seated and no door opened to one | **Could not tell** from the tree. Consistent with it: no consent record was made or changed at the hours of the build; the two new ones are dated at the starts of games 9 and 10 | D: the records' times |
| | Rule: a save of an earlier build with a station held loads and plays on | **Holds**, by its tests | T: `an_older_save_with_a_station_held_plays_on_under_this_builds_rules`, `a_station_loaded_from_its_checkpoint_is_taken_over_by_the_same_model` |

### 1.16 The changes file: everything it says was left

"Still so" means the build as it stands is as the note describes.

| From | Left undone | State today | What I looked at |
|---|---|---|---|
| The base | The saves of m5c and m5c-b left behind | **Still so**, by the owner's rule | D |
| The base | The owner's notes of m5c left behind | **Still so** | D |
| The base | The one consent record made under m5c-b left behind | **Still so**; see Part 3, 3.7 | D |
| 37d | The account in the Goulet is not a true one | **Overtaken** by 37e: the reckoning's rule changed and the merchant's book was tuned for it. Whether it is now true there: the builder's figures, not measured by me | 1.13 item 11 |
| 37d | `take a fix` sets the account outright and picks its marks by how they cut | **Overtaken** by 37e: weighed, and by the near marks | 1.13 item 3 |
| 37d | The dialect does not take cables | **Still so** | P: "'the nearest land' is compared in miles, not cables" |
| 37d | `the port` and `the depth of water` give the true figures | **Still so**, by the plan | 1.2 item 14 |
| 37e | The three figures asked for and not met (the merchant's time more than three miles out; the frigate within a mile and a half inside half an hour of the land; the merchant's honesty) | **Not checked.** Nobody has measured them since 37f moved the passages | |
| 37e | The schooner's pilot hails and does not board | **Still so** | P: an expected failure in my run |
| 37e | The cruise's brig is chased and lost | **Still so**; the reason given is partly wrong (Part 2, 2.4) | P |
| 37e | At anchor in the Bay of Brest the master is surer than he should be | **Not checked**; nothing since claims to mend it | |
| 37e | A wrong chronometer can displace a good account | **Still so** | P: the cruise at 09:00 on the 12th, tick 10800, "the reckoning was out by it; laid down by the observation: moved two leagues and ..." |
| 37e | The number in the one rule is two where the brief said three | **Still so** | R: `OBSERVATION_OUT_SIGMAS = 2.0` |
| 37e | In the open Channel the master's tide is a rough allowance | **Not checked** | |
| 37e | Spec truth 59's sentence left for the lead | **Still so** | R: `docs/TechnicalSpec-M5.md` line 742 |
| 37f | The cruise's stranger is not spoken | **Still so** | P |
| 37f | The schooner's pilot does not board; left for 37h | **Still so**; 37h is not written | P |
| 37f | A dragging that relapses is more than one urgent line | **Not checked** | |
| 37f | The fore-and-afters hove to make more than a knot and a half | **Not checked.** The review says the cutter of game 10 lay hove to forereaching at about a knot | |
| 37f | A course shaped with next to no way on her is worked for that way | **Not checked** | |
| 37f | On the cruise two orders give chase to one sail at the same moment, and the second wear fails | **Still so** | P: ticks 79260 and 79261, and "Could not wear: she would not come round" at 80653. The same doubling shows at 07:00, where three orders give chase within a second |
| 37f | Under eight test workers the workers die at random | **Not checked.** Under four, in my run, none did | P |
| 37g | The silent officer's deck is not in the consent brief | **Overtaken**: it is in the brief as it stands ("or that has been told it is silent past its time") | R: `docs/agents/ConsentBrief.md`, *Being stopped* |
| 37g | What cannot be undone is one order, and it was the officer's already | **Still so**, by the builder's account; I did not go through the vocabulary | R: `agent.py::OFFICER_DOMAIN` holds the object `wreck` |
| 37g | Kept back from the general grant beyond the brief's list | **Still so**, and not ruled on the record (Part 4, C6) | R: `agent.py::_KEPT_BACK` |
| 37g | The REPL's turn mode does not put the consent question again after an opt-out | **Still so**; it seats nobody when the question is owed | R: `agents/repl.py`, the module's own account |
| 37g | A standing order the officer writes under the captain's word stays in the book when that word ends | **Not checked** | |
| 37g | An act at the very tick a station is seated is not replayed | **Not checked** | |
| After 37g's build | "One thing is still open with the owner": four heads in the brief, more in the build | The wording **closed** by the second pass; the ruling **not on record** | Part 4, C6 |
| 37g's second pass | The watcher's brief lists `hand_over` and `handover_note`, both refused to a watcher | **Still so**, and `submit_order` with them | P: the watcher's brief as sent |
| 37g's second pass | `stand_down` takes its note and does not insist on one | **Still so** | R: `agents/tools.py::stand_down`, the note defaults to nothing |
| Played, 7 and 8 October | Everything the paragraph lists from game 10; "nothing was changed in the build for this" | **So**: nothing was changed | P: the fingerprint in game 10's saves is today's. For the items themselves see 1.11 |

## Appendix 2. Where each part of the first edition went

The first edition is `report.md` in this folder. The build's changes file and its briefs
cite it by these numbers.

| The first edition | Here |
|---|---|
| The head (written 2026-10-05, read-only) | The head; A1 |
| The status block of 2026-10-07 | Part C, by date. Its paragraphs on 37e, 37f, 37g, the leaner brief, the second pass and the three small things are carried whole in F4 to F6; its paragraph on game 10 in B3; its last in F7 |
| "By the owner's word the work is done locally ..." | A2, A3; D1, row 2 |
| What this is | A1 |
| The short version | B1 |
| Added 2026-10-07: the first game on the new build | B2 |
| 1. What was reviewed, and how | E1 |
| 2. The games; the games in numbers | E2; E3 |
| 3. What happened in each game | E4, in the order of the games' numbers |
| 4. Gate 5c's checklist against what was played | L1 |
| 5. Findings (its opening lines) | The opening of part G; A2 |
| 5.1 Navigation close to land: its opening, and the *Harpy* on Penlee Point | The opening of part G; G1 |
| 5.1 The mechanisms: the lookout's distance held; nothing warns of land ahead; a landmark is one point | G2 |
| 5.1 The mechanisms: every bearing writes the held distance into the account; a line after two miles' run; the dead reckoning; the danger list; the officer may not take a bearing | G3 |
| 5.1 Three readings give the true position away | G4 |
| 5.1 Parity, as the owner's note 24 asks | G2 |
| 5.1 What worked | G3 |
| 5.2 Pilots and other vessels | G10 |
| 5.3 The officer's authority and the deck | G11 |
| 5.4 The harness and the doors | G12 |
| 5.5 The log's noise | G6 |
| 5.6 The wind near land | G5 |
| 5.7 Standing orders and continuous duties | G9; its first item, `trim sails` filling a hove-to ship, G7 |
| 5.8 Ship handling and ground tackle: hove to, getting under way, the tack, sternway, small vessels | G7 |
| 5.8 Anchoring; aground | G8 |
| 5.9 Ports, trade and boats | G16 |
| 5.10 The order language | G17 |
| 5.11 The browser client | G18 |
| 5.12 The local models | G15; its "Leaving" and "Consent and the drill", G13 |
| 5.13 What worked well | G20 |
| 6. The m5c-b change set: its head, the table of verdicts, how it was checked, carrying it forward | F1 |
| 6. 37b: what play showed, and what is not right yet | G13 |
| 6. 37c: what play showed | G6 |
| 6. The cost CHANGES does not state | G14 |
| 7. The notes, item by item | H1 to H4 |
| 8. Recommendations: the sizes | The opening of part I |
| 8.1 Three things to settle before the rest | I1; replay at length in G14, the one revision in G13 |
| 8.2 Build now: near land; the station and the doors; the log; small faults | I2; I3; I4; I5 |
| 8.3 Build after a ruling | I6 |
| 8.4 Needs design work first | I7 |
| 8.5 Where I would push back | J1 |
| 8.6 Already a later milestone's | I8 |
| 8.7 The gate's four rulings | L2 |
| 8.8 A suggested order | F2 |
| 9. Question 1, replay | G14; D1, rows 3 and 14 |
| 9. Question 2, the gate's verdict | L1; D1, row 4 |
| 9. Question 3, builds | G14; D1, row 5 |
| 9. Question 4, the grant | G11; D1, rows 6 and 15 |
| 9. Question 5, the deck | G11; D1, rows 7 and 16 |
| 9. Question 6, the pilot | G10; D1, rows 8 and 17 |
| 9. Question 7, fixing in pilot waters | G3; D1, row 9 |
| 9. Question 8, relief | G13; D1, rows 10 and 18 |
| 9. Question 9, the consent record of 3 October | G13; D1, row 11 |
| 9. Question 10, the watcher's leaving | G13; D1, row 12 |
| 9. The five points that waited, and the rulings of 2026-10-07; approvals | D1, rows 14 to 19 and 25; each ruling again under G10, G11, G13 and G14 |
| 9. How the work is to be done | A3; D1, row 2 |
| 10. Its head, and how it was checked | E1 |
| 10.1 What was played | E4; the numbers in E3 |
| 10.2 What package 37d did in play | The saves, G14; the account near land, the landfall and `take a fix`, G3; `the nearest land` and land ahead, G2; the wind, G5 |
| 10.3 The owner's six notes | Notes 1, 2 and 5, G3; notes 3 and 4, G19; note 6, G7. His own words, H5 |
| 10.4 The officer's findings, checked | H6, whole; two of its rows again in G8; what worked, G20 |
| 10.5 What neither noted | The pause in the Goulet, G12; the grants and a grant's place, G11; the pilots, G10; the Mingan and "Take a bearing of Bas", G2; the fog, G5; the log, G6; the standing-order book, G9; the ground's words, G8 |
| 10.6 The account's rule; the owner's choice and his ruling; the two things since ruled | G3 |
| 10.6 A model working the reckoning itself | G19 |
| 10.6 The package too big for one; the plan as ruled | F2 |
| 10.6 Small additions elsewhere | The cry, the chart in words and the fog signal, G2; the shaped course and the shore, G3; the detector, G12; the general grant, G11 |
| 10.6 For the gate's checklist | L1, from section 4's own addition, which says the same |
| 10.6 Where I would push back | J2 |
| 11. Its head, and how it was checked | E1 |
| 11.1 What was played | E4; the numbers in E3 |
| 11.2 The owner's two notes | Note 1, G15; note 2, G3; both in H7 |
| 11.3 What the three packages did in play | 37e, G3. 37f: lying to, G7; the anchors, G8; the wind-shift and aback lines, G6; a standing order's action, G9. 37g: the detector, G12; the deck, the grants and the way out of danger, G11; the relief and the drill, G13; the context, the margin and the samples, G15; the saves, G14 |
| 11.4 What else the game showed | A course with a half point and the words refused, G17; the reading of the nearest land in fog, G2; St Mary's Sound, G10; standing orders that cannot act, G9 |
| 11.5 The officer | G15 |
| 11.6 What this changes in the plan | Part K, whole; "Where the lead was wrong", J3 |

## Appendix 3. What the first edition had that this one does not

Nothing of substance. The editor's script found every tick, every time, every sum of money
and every order or file name in backticks of the first edition in this one. Of its 283
table rows, all but twelve are carried whole, and those twelve differ only in a
cross-reference or a tense. Of its 353
quoted passages, four are here only in the first row of the table below. Of the first
edition's 2,547 lines that are not blank, 2,348 are carried over as they stand, apart from
cross-references and the changes of tense and wording listed below. The rest are these.

| What | Where it was | Why it is not here |
|---|---|---|
| Four quotations of the owner's notes on game 9, in a tidied form: "Take a fix and the other reckoning changes seem good so far."; "Reckoning uncertainty drift with no visible marks was deemed a bit low by the officer."; "A lunar with a poor certainty still overrode the better account."; "The brig still likes to come through the wind when hove to." | 10.3 | Replaced by the notes as he wrote them in `m5c-c Notes.txt` (H5, and at the head of each in G3 and G7), so that his words are not changed |
| The status block's opening and its first three paragraphs: that a build folder was made, that 37d was built in two passes, that section 10 was new, that the owner ruled on 7 October | The head | It was a running history. The facts are in part C and F2 to F3 |
| The pointers to the first edition's own sections: "A suggested order of work is in 8.8 ...", "What it changes in the plan is in 10.6 ...", "Game 9's figures are in 10.1", "Tags as in section 7", "The four rulings ... are taken up in 8.7", and the like | Throughout | Each cross-reference now points to a part of this edition. The first edition's section numbers appear only in appendix 2 and where a brief is quoted |
| Two lines of the short version: the verdict on m5c-b, and "Before changing the harness, settle what happens to saved games" | The short version | Both have been done. They are told as done at the end of B1 |
| "Read with 10.6 (added 2026-10-07)", which said that most of steps 1 and 2 of the order was built as 37d and that nothing in section 8 was withdrawn | 8, its head | Overtaken: the recommendations now carry what came of each (part I) |
| "Since ruled, on 2026-10-05 (section 9): item 1 in part, and items 4, 5 and 6. The others stand open." | 8.3 | Replaced by the column in I6, which is fuller and later |
| The opening of section 9, which said that where an answer was read further than its words it stayed the review's reading until the owner confirmed it | 9 | He confirmed the readings on 7 October ("Approved as read"). Each reading is still marked as the review's where it is given, in G10, G11 and G13 |
| "The order of 8.8 stands, with the gate's remaining play as its last step." | 9, question 2 | Overtaken by the plan as ruled on 7 October (F2) |
| The five points and the approvals as a numbered list, with "Points 2, 3 and 5 are built by package 37g, and point 4 by 37h" | 9, its end | The rulings are in D1 in his words and again under each subject. 37h is not built, and the sentence read as if it were |
| "Nothing in sections 8 and 9 is overturned. ... All of what follows is proposed, for the owner's word; nothing is built." | 10.6, its head | No longer true: he ruled, and 37e, 37f and 37g were built |
| The second telling of what game 9 adds to the gate's checklist | 10.6 | A repetition of the addition at the end of section 4, which is in L1 |
| "Small additions elsewhere", as a list with the tags **Now** and **Later** | 10.6 | Each is told under its subject with what came of it: the shaped course and the shore (built, 37e), the land-ahead cry's words (not built), the detector (built, 37g), the fog signal (later). The chart in words is carried whole in G2 |
| The tags **Now** at the end of the review's replies to the owner's notes 1, 2, 5 and 6 on game 9, and "for the next package" | 10.3 | Each is replaced by what was built. The tags in section 7's tables are kept, in part H |
| The present tense in four places: "it is the first item of the next package"; "Today there are three rules"; "It always takes the tack she hove to on"; "the account knows nothing of the stream" | The short version; 10.6; 10.4 | Put into the past, since each was mended in 37e or 37f |
| "Found by the lead in the log and the replay." | 10.5, its head | E1 says once that everything from games 9 and 10 is the lead's own reading |
| Headings and their numbers, and the labels "37e, the account.", "37f, lying to and the ground.", "37g, the station.", "Anchoring.", "Aground.", "On the notes:" | Throughout | The parts have new headings |
| The sentence "(section 7)" after the *Amazon*'s officer's "a word picture of the near coast" | 10.6 | Section 7 does not hold that request. It is in `evidence/amazon-post-session-chat.md`, and G2 says so |

What this edition has that the first did not: the words coined (A4); the rulings in one
table (D1); what each package built and measured, taken from `CHANGES-m5c-c.md` (parts F
and G); the last column of each table in parts H and I; the editor's own sentence on game
10 and the gate's checklist (L1); and the audit of 8 October, carried whole (A5, B5, parts
M and N, appendix 1), with every statement of status set against it.

**The audit is carried whole.** Every line of `handover-audit.md` is in this edition as it
stands, but for its title and the six headings that name its short version and its five
parts, which the headings of this edition replace. Twelve of its lines, the seven things
for the owner to decide, are carried twice, in D2 and in part N.
