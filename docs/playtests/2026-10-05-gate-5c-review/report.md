# Gate 5c playtest review

Written 2026-10-05 by a Claude Opus 5.5 session in Claude Code, at the owner's request, as a
read-only review: nothing in `FreeSail-gate-m5c` or `FreeSail-gate-m5c-b` was changed to
produce it, apart from adding this folder. The readers' detailed reports, with every tick
and quotation, are in `evidence/`.

**Status, 2026-10-07.** Sections 1 to 9 are the first review, read by the owner, who
answered its ten questions on 5 October (section 9). Since then:

- A build folder, `FreeSail-gate-m5c-c`, was made beside the gate (m5c with the m5c-b
  changes), and one package has been built in it in two passes: **37d**, the saves and the
  sight of land. What it holds, what was measured and what was left undone are in that
  folder's `CHANGES-m5c-c.md`; its brief is in that folder's `docs/dev/M5-WorkPackages.md`.
- The owner played a first game on that build on 6 October. **Section 10** is new and is
  that game: what happened, what 37d did in play, his six notes and the officer's findings
  checked against the log, a replay and the code, and what it changes in the plan.
- On 7 October the owner ruled on what comes next (10.6) and on the five points that had
  waited from section 9 (recorded at its end), and approved the briefs of three packages,
  which are in the build folder's `docs/dev/M5-WorkPackages.md`: **37e** the account,
  **37f** lying to and the ground, **37g** the station's safety with the consent brief's
  one revision.
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
- **The owner played the build that night** (7 to 8 October): a merchant cutter from
  Falmouth to Scilly and out again, 63 hours, with a local model as officer of the watch.
  **Section 11** is new and is that game, the first with 37e, 37f and 37g in it. The
  consent question was put to the model again with the lean brief as approved, and
  answered yes; the seven words were not added, and the lead's advice is now to leave the
  brief as it is. In short: the model was a useful mate; fixes near land were very good
  and the master's doubt is honest; and the faults that hurt were the harness's and the
  reckoning's. A cast of the lead moved a sound account a mile, twice. The model's context
  overflowed and ended both seatings. One reply in twenty was lost to the limit on a
  reply. An anchor left aweigh could not be let go. The account goes wrong when she
  stands off and on. A course given with a half point steers her to its last word. Two of
  these come from this review's own advice (11.6).
- Nothing beyond 37g is approved. 37h, the pilot, is not written. What section 11 proposes
  (the local runner first, then amendments to 37e and 37f, and words) waits on the owner.

By the owner's word the work is done locally in the gate folders, with no commits and the
GitHub repository and its worktree left alone; he folds it in with the lead session that
works the repository. What this review's own lead session confirmed directly is marked
**(lead)** in sections 1 to 9; the rest of those sections rests on the readers' reports.
Sections 10 and 11 are the lead's own reading throughout.

## What this is

A review of everything played and noted at gate 5c so far, written to answer four questions:

1. What happened in each playtest, and what did it show?
2. What does the provisional update `FreeSail-gate-m5c-b` change, and is it sound?
3. How do the owner's and the playtesting model's notes
   (`m5c playtest and model notes.txt`) read against Milestone 5's own documents and the
   design proposal?
4. Of everything found: what can be built now, what needs a ruling or more design first, and
   what should be pushed back on?

## The short version

**The gate's claim largely holds.** A passage between ports with a cargo, a pilot, the tide
and the anchor is a game, and a model can hold the officer's watch. Opus 5.5 kept the deck
for eight days and for six and a half, made the *Harpy*'s voyage pay, and near danger read
the situation better than the game's own words did. A local 27B model kept a 27-hour watch.

**The grounding and the near misses come from a handful of faults close to land, most of
them small, and not from the chart reckoning as such** (5.1, 5.6):

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

**In the harness** (5.4) the weightiest faults are these: a seat is found by the station's
name alone, so another door's calls ran under a seated model's name; the turn budget can
refuse the leaving tool and drops calls without a line in the log; a stand-by takes one
condition, has no bound, and is not broken by a dragging anchor or fog; a paused officer
keeps the deck while the ship sails on; the contrary-order detector was wrong 29 times in 31;
and a station cannot read its own journal.

**m5c-b** (section 6): carry all three parts, the re-seating rule after its opt-out path is
mended, the two log rules with a floor and a change of key. Apply the diff; do not copy the
folder.

**Before changing the harness**, settle what happens to saved games with a model aboard,
which no longer replay once the rules that wake a station change (8.1).

**The notes** are confirmed in the main. A dozen of the model's points do not hold as
stated, and several of the owner's are better met another way (section 7, 8.5).

**The gate itself** is not fully played: the naval cruise was never run, and the lead's own
watch is not in the record (section 4).

A suggested order of work is in 8.8. The questions put to the owner, with his answers, are in
section 9.

### Added 2026-10-07: the first game on the new build (section 10)

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
- The lunar did overrule the better account. That was never part of 37d; it is the first
  item of the next package. The same rule let a good noon latitude be ignored.
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

What it changes in the plan is in 10.6: one rule for when an observation is believed, the
next package built as two, and a choice for the owner about how the master learns that the
tides run hard.

## 1. What was reviewed, and how

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

## 2. The games

Eight distinct games at the time of the first review; a ninth played on 6 October on the
build folder m5c-c, which section 10 covers; and a tenth played there on the night of 7 to 8
October, on the build with 37e, 37f and 37g, which section 11 covers. A chain of saves from
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
| 9 | A merchant brig (the officer calls her the *Harpy*): Falmouth, Roscoff, outside Ushant, Brest. **Section 10** | merchant brig | none to Roscoff, the owner alone; then officer: Opus 5.5 through the MCP bridge, two seatings, the deck for 78 hours | m5c-c with package 37d | 12 June 05:00 to 17 June 04:35 (5 days) | 6 Oct |
| 10 | A merchant cutter: Falmouth, at anchor off the Lizard, Scilly (St Mary's Sound), out for Ushant. **Section 11** | cutter | officer: Qwen 3.8 27B under llama.cpp through the local runner, 102,400-token budget, two seatings, the deck for 53 hours | m5c-c with packages 37d to 37g | 12 June 05:00 to 14 June 20:00 (63 h) | 7 to 8 Oct |

The build of each game is the build of the folder that holds its saves: the owner confirms
that a save was played on the build of the folder it was saved in (section 9, answer 3). So
games 5 to 8, whose saves are in `m5c/saves`, are plain m5c. The Gemma game's log agrees: it
has m5c's reseat wording ("the second seating, the last this game allows").

### The games in numbers

Counted from each game's full log. Game 9's figures are in 10.1.

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

## 3. What happened in each game

Times are ship's time; numbers in brackets are ticks, for finding the place in a log.

### Game 1. The merchant passage, the owner alone

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

### Game 8. The *Amazon* as a merchant ship

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

### Game 2. The *Harpy*

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
section 5.1. She struck Penlee Point at 13:50:53 (636,653), aground and leaking. The captain
sold the brandy by boat for £4,725 while she lay there. She floated on the flood at 18:04,
struck again 21 seconds later, floated at 18:32 and rode the night.

**20 June.** The pilot left as she stood off to save herself. She anchored in Cawsand Bay:
"Brought up by the best bower in no water". The purse had gone from £1,000 to £5,148.

### Game 3. The first start from Plymouth

Two hours. The captain belayed the long-boat seventeen seconds into hoisting out, meaning to
send the mate in her. The boat stayed "away, hoisting out" for good, and a *rejected* order
had put the mate, who was the officer and held the deck, into it (3,237). They started again.

### Game 4. The *Speedwell*

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

### Games 5 to 7. The local models on the cutter

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

## 4. Gate 5c's checklist against what was played

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
| 12. The gate's truths | The suite, not play (section 6 has a full run of m5c-b's) | |
| 13. A scenario saved and loaded | Saves and checkpoint loads carried game 2 across two builds | A save during the chase |

What follows for the verdict:

- The record supports a verdict on places and people, the papers, the tide and the anchor,
  the officer's watch, and the sighting half of "other sail". For the chronometer and the
  chase it holds nothing beyond the suite's own truths, unless the cruise is run or the owner
  takes those on the tests' word.
- Item 13 should not be waved through: the one defect of its kind was found exactly by
  loading a save with a station held (section 6).
- The spec makes the verdict wait on the lead's own officer's watch through Claude Code. That
  watch is not in the record.
- Two of the three long watches ran wholly or partly on m5c-b, whose consent brief and log
  lines differ from the build as cut.

The four rulings the gate asks for are taken up in 8.7.

**Added 2026-10-07.** Game 9 (section 10) adds to the table: a fourth long watch by Opus
5.5, on m5c-c (item 10); a star lunar (item 3); mooring and unmooring twice, three anchors
down and dragging on bad ground (item 5); a cargo bought at Roscoff and prices fetched at
Brest (item 6); Roscoff and Brest under American colours (item 7); and, for item 13, a save
with a station held that loads from its checkpoint and also replays exactly on the build
that wrote it. It runs neither of the gate's two scenarios, and leaves the naval cruise, the
chronometer and British colours off Roscoff unplayed as before.

## 5. Findings

Each finding gives where it was seen (game and tick) and, where the cause was traced, the
place in the code. All code references are to m5c; m5c-b differs only where section 6 says.
**(lead)** marks what the lead confirmed directly in the code or the log. Everything else is
from a reader's report in `evidence/`, most of it checked by a second reader.

### 5.1 Navigation close to land

This is the weightiest area: one grounding, two near misses, and an account that was wrong
with the land in sight. The owner's notes 19 and 24 put it down to the reckoning near visible
land. The record says the chart reckoning itself is sound in open water, and that close in
it is defeated by a handful of specific faults, most of them small.

#### The *Harpy* on Penlee Point (lead, from the log)

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

1. **A wind that took her aback three times in thirteen minutes** (5.6).
2. **The lookout's distance frozen at "a mile"** (below).
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

#### The mechanisms

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

**Every bearing writes that held distance into the account** (lead;
`reckoning.py:1358-1415`). `take a bearing` does two things. It draws the account onto the
bearing line, with a figure good to about a degree and a half. It then applies the lookout's
distance by estimation as a second line, trusted to 15 per cent. That estimate carries a
random factor drawn once for the whole sighting, and is frozen as above. So each single
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

#### Three readings give the true position away (lead)

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

#### Parity, as the owner's note 24 asks

A human at the browser sees the shape of the coast; a model has a list of bearings to
points. But the chart is drawn about the account, so when the account is out the picture
misleads the human too. The words give a bearing to the compass point, 11¼ degrees, while
the account is moved with a figure good to a degree and a half; the human sees the result on
the chart and the model does not. The *Speedwell*'s officer: "my bearings are rounded to the
point, so you're better placed." Shown a picture of the chart afterwards, the *Amazon*'s
officer saw at once that the account's track ended on the island's own western ledges
(`evidence/amazon-post-session-chat.md`).

#### What worked

Cross bearings of charted marks after a run put the account right at once (the Isle of Bas,
St Agnes light, the Manacles). The noon latitude is honest, with "No sight" on thick days.
`shape a course` warned of the Gilstone and the Old Wall. The officers' lead orders did real
work: a three-minute lead was entered six minutes before the *Speedwell*'s 3½-fathom cast.
In game 1 the book's lead and bearings every five minutes took the schooner through the
Goulet cleanly.

### 5.2 Pilots and other vessels

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

**Other vessels at a fixed distance** are the held estimate of 5.1, not ships circling.

### 5.3 The officer's authority and the deck

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

### 5.4 The harness and the doors

**After stationing, a seat is found by the station's name alone** (`remote.py:820-829`). The
calls for turns, replies and release carry no key. This is the owner's local note 5. In game
7 Qwen's last reply is entry 148 of its transcript, at 08:05. At 12:14 the captain typed
"Resume the officer", and eight calls from a Claude Desktop session still attached to the
same game ran in Qwen's seat: it belayed a standing order, hove her to on Qwen's allowance,
was refused the anchor, and wrote the final handover note (112,483 to 112,613). The log and
every field of the save give them as Qwen's; only the shape of the raw replies differs. No
consent was asked of the model that acted. From the same code a stale bridge quitting would
stand down another door's station, and a consent conversation takes replies the same way.

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

**`say` ends the turn at the MCP door.** Fifty of the *Speedwell*'s stand-bys were set about
fifty seconds after a spoken line. On the *Amazon* it cost thirteen such waits, one of them
35 seconds after letting go the anchor while the topsails still drew and she dragged
(121,684). The captain told one officer not to use `say` at all (546,431). `answer` does not
end a turn.

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

**A word from the captain that lands while the officer's turn is open does not wake the
stand-by that follows.** On the *Speedwell* 22 of 126 typed tells and asks went this way,
nine of them wanting an answer: the warning of unmarked land in shoaling water waited 66
seconds (200,139), "Are we safe to moor here overnight by your reckoning?" two hours
(204,890). In game 3 the deck itself was given this way and not taken up for four minutes.

**A paused officer keeps the deck while the clock runs.** In game 7 the local model's turn
stood open and it never replied. The harness nudged, then paused: one notable line, no easing
of the clock, no deck returned. The cutter ran four hours in thick fog from fourteen miles
off Roscoff to 1.6 (97,556 to 112,463). The stand-down waits ten real minutes, which is ten
hours of ship's time at 60x. The silence detector also takes a model at work inside an open
turn for one that is silent.

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

**A late reply is acted on as fresh.** On the Ollama cutter a `heave to` landed 71 minutes of
ship's time after the model's previous reply, meant for a pilot already gone (game 6,
15,937). The game does not wait, the owner had sped up while the turn was open, and an order
carries no "as of". The watcher's reports ran ten minutes behind.

**What a waking officer is given is thin.** A sample's log lines carry no actor, so one
officer's handover note claimed the captain's standing orders as its own (game 6, 34,091).
The captain's helm orders arrive only as a count: "26 orders given".

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
  left by `opt_out` at the captain's word (5.12).

**What worked.** Re-seating under m5c-b. Two stations through two doors at once. The handover
request and the fold at a known context (5.12). The officers' handover notes: a stranger
could have taken the *Harpy*'s deck from the one at 602,100.

### 5.5 The log's noise

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
in the weather (5.6).

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

### 5.6 The wind near land

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
(section 6).

**Fog changes on the four-hour bell**, to the second, in fifteen changes of sixteen on the
*Harpy*.

### 5.7 Standing orders and continuous duties

Standing orders held the watch well in open water. On the *Harpy*'s first night "trim on a
shift" took the yards from sixty degrees to square with nobody sampled. Number-free forms
("every glass then take a bearing of the land") and the captain's event hooks
(`at the pilot asks to be put off then ask the officer ...`) both worked. What they lack is
knowing when to stop.

- **`trim sails` fills a ship that is hove to**, four times in two games (*Harpy* 137,021,
  137,615; *Speedwell* 162,102, 193,303). `trim` has no hove-to check, though `steer` and
  `keep her full` do. She stays recorded as hove to, so `heave to` is then refused: "She is
  hove to already" (193,441). *Added 2026-10-06, from the owner:* the dialect has had the
  guard since package 33c. A rule ending `... and she is not hove to then trim sails` (or
  `and the manoeuvre in hand is not hove to`) sleeps from the moment the heave-to begins
  until she fills away (lead; `standing/rules.py:274-278`, and the project's own test,
  `tests/test_standing.py:1741-1810`). Neither the starter book's "trim on a shift" nor the
  officers' own trim rules carried it.
- **In a calm** its only floor is half a metre a second of apparent wind. The *Speedwell*'s
  rule braced the yards six times in a one-knot night. The note's "all night" overstates it.
- **The event `a wind shift` fires at one point of the mean wind; the log's line needs two.**
  So the hands trim "by standing order" with no shift logged.
- **A trim is fixed at the moment of the order**, so `steer X; trim sails` trims to the old
  course. The cure exists and the gate's own books use it:
  `at steady on the course then trim sails`.
- **A condition on the depth reads the true charted depth** with no cast (5.1).
- **A condition that can never be true is accepted without a word**: "the distance to the
  land is under 3 miles" (game 6, 11,665).
- **The grammar is strict about small things**: five refusals in thirteen seconds for a
  missing "is", and an apostrophe ends a quoted name.
- **A second cast of the lead is queued, never run beside the first.** "Not hands enough to
  heave lead" came with one, two and three lead rules in force, each time during a trim. The
  trim took the hands, not the third rule.

### 5.8 Ship handling and ground tackle

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

**Sternway.** The note that the helm steers as if she had headway is not borne out: the
rudder and the helmsman both reverse (`hull.py:231-243`, `358-362`). What the log shows is
`steer ENE` taking the short way round, through the wind, with no way on.

**Small vessels speak the frigate's words**: "In studding sails, royals and topgallants; up
courses" on the cutter; "two of the young gentlemen" in a merchant schooner. Five of the
starter book's nine rules are refused on the cutter.

### 5.9 Ports, trade and boats

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

### 5.10 The order language

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

### 5.11 The browser client

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

### 5.12 The local models

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

### 5.13 What worked well

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

## 6. The m5c-b change set

`FreeSail-gate-m5c-b` is a copy of m5c with three changes, made on 3 October by the Opus 5.5
session that was playing the *Harpy*'s officer, and played live the same day: the *Harpy*
from tick 527,255 on the first change alone, the *Speedwell* on all three.

| Part | What it does | Verdict |
|---|---|---|
| 37b, the rule | A station may be seated again any number of times. How it was left decides: stood down or handed over, seated as it was; left by the token or `opt_out`, the consent question first; `opt_out` with `final`, not in this game. | **Carry, after mending the opt-out path.** |
| 37b, the fix | A save whose station was held when it was saved can be taken over again by the same model after loading from its checkpoint. | **Carry as it is.** |
| 37c, the wind-shift line | Reads the ten-minute mean wind, two points from the last line, held a minute. | **Carry, with a floor on wind strength and steadiness.** |
| 37c, the taken-aback line | Once an episode, re-armed after a minute clear; urgent only with way on, four knots of apparent wind, and no anchor or ground holding her. | **Carry, with re-arming by state and one flag per severity.** |

### How it was checked

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

### 37b: what play showed, and what is not right yet

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
  three of the seven reseat briefs in these games, and no tool reads the journal (5.4).
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

### 37c: what play showed

**Taken aback.** The urgency rule did its work. In six and a half days the *Speedwell* logged
five urgent lines, four of them real, against the *Harpy*'s 31 under the old rule, 21 of
which came with nothing to lose (5.5). What remains:

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
the sea breeze changing direction as the ship moves (5.6). No rule in the log can cure it,
and CHANGES says rightly that 37c does not touch it.

Three definitions of a wind shift still stand: the log's (two points on the mean), the
`a wind shift` event's (one point against the last sample), and the standing orders' (the
instant wind). On the *Speedwell* the trim rule fired 40 times, 12 of them near a log line.
CHANGES says the change "closes" the spec's open item 11; it narrows it.

### The cost CHANGES does not state

CHANGES says the simulation and the saves are unchanged. That holds for a game with no model
aboard and for any load from a checkpoint. It does not hold for a **replay** of an older save
with a model at a station. A station's orders are not in the journal: a replay hands the
recorded replies back when today's rules open a sample. The *Harpy*'s officer was woken four
times on the night of 15 June by urgent lines that 37c no longer writes, and its recorded
orders would land elsewhere. Every *Harpy* save is therefore good from its checkpoint only.

This is wider than 37c. Any change to what wakes a station, what is urgent, or how many calls
a turn holds will do the same to every saved game with a model in it, and most of the harness
changes the notes ask for are of that kind (8.1).

### Carrying it forward, in order

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

## 7. The notes, item by item

Every item of `m5c playtest and model notes.txt`, read against the record, Milestone 5's own
documents and the design proposal. The last column says where it falls in section 8:

- **Now**: build now. **Rule**: needs the owner's ruling first. **Design**: needs design
  work first. **Push**: pushed back on, wholly or in part. **Later**: a later milestone's
  by the documents. **Done**: already in m5c-b.

The owner's six notes on the first m5c-c game (`m5c-c Notes.txt` in the build folder), and
that game's officer's findings, are taken the same way in 10.3 and 10.4.

### The owner's items

| # | The note | What the record shows | Against M5 and the design | |
|---|---|---|---|---|
| 1 | Pilots boarding a moving ship; a baseline now, the director later | Pilots boarded ships under way, stopped, hove to and at anchor. The real fault is the reverse: a ship that heaves to at the hail is not boarded, because the boat lies to at a predicted meeting point | Other vessels with captains are M6, the director M7b. A baseline now fits how the proposal stages things | Now |
| 2 | `the well` says there is no well | Confirmed. The leak is a rate and a level nothing reads; no pumps; the carpenter comes with nothing to say | The spec says touching the ground has consequences. The well's reading was owed since M4's open items and is in no M5 package. Pumps are "a later milestone", none named | Now, Rule |
| 3 | The price list should hold every visited port | Half built: the paper keeps every port's list with its date; the `the prices` reading shows the last. The *Speedwell*'s starting list was skipped by a capital letter | Within spec §23 | Now |
| 4 | The primer needs a full clean-up into a general guide | Build and test wording runs through chapters 4, 5, 7, 14, 15 and 16. The brief and chapter 16 say 1806 in an 1805 game, and one officer dated the year by it | Decision 28 already says the primer must not narrate a gate's day. Its code blocks are run by `tests/test_primer.py`, so a clean-up must keep them valid | Later |
| 5 | The scripted passage is clean; evidence that its author could captain, or direct | The run matches the gate's reference to the tick. It also holds three casts that timed out as "paid off", a noon sight not adopted, and the anchor-depth fault | Weak evidence for a captain or director: the book was written with the author's view of the true chart, on a pinned wind and seed. The director is M7b and is tested differently | Push |
| 6 | Soundings on the chart read "NaN fm" | Confirmed; one undefined constant | A plain defect | Now |
| 7 | The reckoned track is trimmed too hard | Confirmed: 168 points, one added at every cast and bearing | Spec §17 promises "the track by account" | Now |
| 8 | Move the 1x option; show the anchor in the state window | The 1x option is the ease-to-1x checkbox. Anchor facts are readings, not in the snapshot | Client work | Now |
| 9 | Accepting or refusing the pilot, with hailing when that comes | Confirmed automatic. He boards outward-bound ships; the *Harpy* paid £22 to five pilots for no pilotage | Signals are M7 and M8. Accepting or declining needs no signal | Rule |
| 10 | The returning session could not read its journal | Confirmed in the code and in two games. No tool reads it; the brief is twenty log lines | The documents call the journal the model's memory in five places and give no way to read it. A defect | Now |
| 11 | Keep the journal out of the context by default | Low yield: everything a model writes is 4 to 8 per cent of its conversation; the samples are over 80 | "The journal" is a section the re-ask rule watches. Needs 10 first | Push |
| 12 | Amicable re-seating as the default | Done for the same model in m5c-b and proven five times. Left: `I have the deck` stands the station down; another model cannot relieve; the opt-out path | "Once" was the owner's own reading, not a model's condition. The decisions log is not updated | Done, Rule |
| 13 | Stand by until x, y or z; parity with the orders' conditions | Strongly supported, and more: a stand-by has no bound and nothing notable breaks it | Decision 18 promised a stand-by on "a reading crossing a value"; unbuilt. The package's brief asked for notable-level wakes | Now, Design |
| 14 | Claude Desktop must be restarted between sessions | Cause found: the bridge asks for its station once in its life | Documented as the procedure, with no reason given | Now |
| 15 | A general grant of authority, with some things kept back | Strongly supported: 27, 27 and 20 allowances, a third unused. Also found: allowances are keyed to a verb, resolve by prefix, and never lapse | Ruled otherwise so far (a domain plus named allowances). Changes the consent brief's domain sentence. Approaches the captain's station, which is M6 and for which one model reserved its consent | Rule |
| 16 | A `keep` prefix for continuous orders | The duty already exists as a standing order. The faults are that `trim` fills a hove-to ship and that the event has no wind floor | The dialect has every guard a `keep` needs; `keep her full` is already a verb (decision 22) | Now, Push |
| 17 | "Taken aback" urgent in a calm | Confirmed: 21 of the *Harpy*'s 31 came with nothing to lose. Five were wanted. m5c-b's urgency rule held | The proposal's own risk table names log thrash | Done, Now |
| 18 | Wind shifts fill the log in light airs | Confirmed, but the floods are not light airs: they are the sea breeze flipping near land | Spec open item 11, narrowed by m5c-b, not closed | Now |
| 19 | Near visible land: an urgent lookout call; the reckoning made precise | The first half is right and cheap: a ten-minute look-ahead would have given the *Harpy* 9.3 minutes. The second half should come through observations, not by nearness | The lookout "notable for a landfall or a danger" is in spec §12. Making the account precise from the truth breaks the two-positions rule | Now, Design |
| 20 | A movable compass rose, lines and markers on the chart | Nothing of the kind exists. The captain's own markers have no names | Client work. The cold review: every drawn thing is first a reading | Later |
| 21 | A turn should not end on `say` or `answer`; a larger budget, as a setting | `say` ends a turn at the MCP door only; `answer` never does. The budget is eight and counts stand-bys, reads and leaving | `stand_by` ending a turn is decision 24. The budget is "a judgement, not a welfare rule". Old saves replay against it | Now, Rule |
| 22 | The cutter's square sail is too short | Confirmed, in the data: a 27-foot sail on a yard 52 feet up | Vessel library, M8, or sooner | Now |
| 23 | Several stations through one door | Two stations through two doors already work. Nothing binds a chat to a role, and a seat is found by the station's name alone | Consent is per exact weights, "each through its own door" | Push |
| 24 | Parity near unnamed coast and area landmarks; "nearest land"; features by their parts | Confirmed need. The chart can already answer "nearest land"; features by parts are data | `ChartData.md` gives the nearest shore "for the lookout". Squarely the design's intent | Now |
| 25 | Image tools for image-capable doors | Not present; feasible. The cheapest route is the owner's open browser capturing the view | The proposal is silent. Changes what an instance sees, so a re-ask. Sound only once the same thing exists as words | Design |

### The model's comments on the owner's items

| On | The comment | What the record shows | |
|---|---|---|---|
| 1 | Tozer boarded at four knots; Moal only once sailed down to; his boat "held eight cables off for an hour"; he left a mile away; the "two cables" rule is not applied on leaving | Tozer boarded a ship stopped in irons. Moal's boat lay to at its meeting point: a bug. The distances are held estimates. One test serves boarding and leaving | Now, Push |
| 2 | "Four feet and gaining" has no reading behind it | There is a number behind it; nothing reads it | Now |
| 3 | Show which goods a port trades before its prices are known | Confirmed absent. By the proposal's own rule the knowledge must come by a carrier: a paper, the pilot's news, another master | Rule |
| 11 | A one-line pointer to the journal in each sample | Cheap and sound, once the journal can be read | Now |
| 13 | "A sounding, or the pilot's hail, or a danger sighted"; "a sounding" wakes on no bottom | Confirmed: 32 such wakings on the *Speedwell*, nine on no-bottom casts in one stretch | Now |
| 15 | An explicit-only list of anchoring, the port and buying and selling; an emergency clause; "on the Harpy that clause would have mattered" | The clause is worth building and the gate asks for it. The *Harpy* claim is not borne out. The logs argue against keeping the anchor back: it was the thing wanted in a hurry | Rule, Push |
| 16 | `trim` fired hove to, twice; bracing all night in a calm; a `keep` should pause itself | Four times in two games. Six or seven firings in the calm night, not all night. The remedy is right | Now |
| 17, 18 | Under m5c-b the urgent alerts stopped; about 25 no-way lines in a night; forty per-sail lines in ninety minutes; a dozen shifts in an afternoon; a minimum wind strength "would finish it off"; the cause is in the weather | Right on the first four (the per-sail figure understates: 53). The dozen was 22. A floor alone would not finish it: 23 lines came in a gentle to moderate breeze at Scilly. The cause is in the weather, in the sea breeze | Now, Push |
| 19 | A worse figure should not replace a better; the danger list should come from the best fix; "this is what put the Harpy ashore" | Right in substance: clean on the *Amazon*, and by two or three to one on the *Speedwell*. "Good to about 2" is overstated. The danger list point holds. The reckoning was one cause of four on the *Harpy* | Now, Design |

### The model's additions

| The addition | What the record shows | |
|---|---|---|
| The relay cut calls at 60 seconds; `--wait 50` should be the default for remote clients | Confirmed. The default is 200 seconds, tuned to Desktop; the bridge names the remedy and does not adapt | Now |
| The drill's stand-by carried into the station; the first `hand_over` was "Nothing was run" | Partly. The drill cannot carry. It was the loaded save's own stand-by, kept on take-over and never told to the model | Now |
| The handover note is not in the reseat brief | Confirmed: missing from three of seven | Now |
| The officer is not a person on deck: sent off in the boat; listed asleep | Confirmed. Binding a station to a person is M6 by ruling. That a *refused* order still moved him is a bug today | Now, Later |
| The contrary-orders warning fires on ordinary sequences | Confirmed: 28 of 30 nudges and the one pause were false | Now |
| Kedging refused aground; hauling up to a kedge not modelled | Refused, yes. `heave short` does haul a floating ship to her anchor. Working a kedge is M8 by the gate | Later |
| With sternway the helm steers as if she had headway | Not borne out: the rudder and the helmsman both reverse | Push |
| The schooner's `get under way` does not cast her head | Confirmed at Plymouth; Roscoff was clean. The script says "paid off" on a timeout, in the gate's own passage too | Now |
| `trim sails` acts before the helm has swung | As designed, and the cure exists: `at steady on the course then trim sails` | Now |
| The hand lead says "no bottom" while the depth reads 15; confusing without a deep-sea lead | The depth reading is the chart's at the true position and leaves out the tide. A deep-sea lead exists and was the officer's to order | Push |
| Three lead orders at once caused "not hands enough" | Casts queue. The trim took the hands, with one, two or three lead rules in force | Now |
| "Brought up in no water": a missing depth | Not missing: the anchor's depth is read in the wrong place | Now |
| The *Harpy*'s reckoning kept advancing at anchor | The "run since noon" reading, on one night of three. The position only creeps | Now |
| Belaying a boat mid-hoist leaves it stuck for good | Confirmed, and two more ways to the same end | Now |
| One bargain a trip, about four and a half hours | As built. Trips ran from 80 minutes to 4 h 36 m by a formula | Rule |
| Other ships keep a fixed distance | The held estimate | Now |
| The water sail cannot be taken in by name | Confirmed for `take in`, `furl`, `lower` and `clew up`. `haul down`, `douse` and `hand` work | Now |
| Number words above twelve fail | Wider and odder: the teens, across five separate readers. "Fifteen" and the tens work | Now |
| "Full and by" is refused; the permission's name does not match | As designed: it is the verb `keep her full`, and allowances are named by their verb | Rule |

**"What worked well".** The pilot's directions at Roscoff were good and were never sailed; at
St Mary's the same kind of text could not be followed. Fixes from bearings: yes, with the
distance fault of 5.1. The quieter "aback" lines: yes for urgency. Number-free standing
orders, `what is she`, the ship's papers: yes. The noon latitude: yes, though twice it was
not adopted.

### The owner's local notes

| # | The note | What the record shows | |
|---|---|---|---|
| 1 | llama.cpp was necessary; the experience smooth; game-sense reasonable | Necessary, because Ollama reported no context size. "Smooth" wants qualifying: a silent reply cap, four budget-closed turns, and a four-hour stall. Game-sense held in outline; none of the three navigated. The Gemma game on record ran through Ollama's port | Now |
| 2 | The handover and its notice work; make the threshold a setting; could it be higher? | Confirmed, twice, with the model's own exact account. A constant with no flag. Higher is safe on large contexts only; a reserve in tokens is the better shape | Now |
| 3 | The turn budget is a blocker; at least double it | Confirmed. Sixteen covers every turn seen. For Gemma the harm was the message's wording and counted refusals, which a bigger number hides without curing | Now |
| 4 | The handover served as in-game compaction; reconnecting and the reseat limit remain | True of game 7. Gemma's "compaction" was a `hand_over`, a restart of the runner and the only reseat | Done, Now |
| 5 | A Claude Desktop session's calls went through in the local model's place | Confirmed to the entry: eight calls, recorded as Qwen's. The cold review had named the weakness | Now |

## 8. Recommendations

Sizes: **S** is under about thirty lines in one place; **M** is one module with its tests;
**L** is several modules, or a decision first. "Digests" says whether the change moves the
recorded known-truths constants in `tests/test_known_truths.py`.

**Read with 10.6 (added 2026-10-07).** Most of steps 1 and 2 of the order in 8.8 is built,
as package 37d; `CHANGES-m5c-c.md` in the build folder lists what it holds and what it left.
The first game on that build sharpened what comes next: 10.6 states one rule for when an
observation is believed, proposes the next package as two, and adds a few small items.
Nothing in this section is withdrawn.

### 8.1 Three things to settle before the rest

**The replay of a saved game with a model in it.** A station's orders are not journaled; a
replay hands its recorded replies back when today's rules open a sample. So any change to
what wakes a station, what is urgent, how many calls a turn holds, or what an allowance
grants makes an older save replay as a different game. Most of 8.2's second table is of that
kind, and 37c already is. The cheap course: stamp every save with an engine version (it has
read "0.0.1" since milestone 0), have `load` say so when it must replay an older save that
holds a transcript, and treat such saves as good from their checkpoints only. The lasting
cure is a replay that opens samples where the transcript says they were opened; that is a
design item (8.4). The proposal calls replay "a hard requirement", so this wants a ruling,
not a drift. The owner's answer, what a checkpoint gives materially, and a recommendation
are in section 9, under question 1.

**One revision of the consent brief.** Seven identities hold a yes, and each change to a
watched section asks all of them again; it took five conversations to carry one family of
weights through two days. The changes below that touch the brief are: the words of
**Leaving** (37b, mended); a way to read the journal; `I have the deck` leaving the station
seated; the domain, a general grant and the emergency route; and the detector's description
if its rule changes. Settle the words of all of them, then merge the brief once.

**One re-measuring of the recorded passages.** The near-land fixes, the anchor's place, the
schooner's cast and the log rules each move the recorded digests. Done together they cost one
re-recording and one slow run on Windows.

### 8.2 Build now

#### Near land

| # | Change | Where | Size | Digests |
|---|---|---|---|---|
| 1 | Judge a distance afresh when it has changed by a tenth, for land and sail alike | `lookout.py:362-386` | S | Every passage with land or a cutter |
| 2 | A single bearing gives a line. Stop applying the distance by estimation as a measurement good to 15 per cent; at most a loose one | `reckoning.py:1395-1400` | S | The same |
| 3 | `take a fix`: cross the two or three best-cut marks in sight, lines only, and say the fix and how well the marks cut. Open it to the officer | `reckoning.py`, `orders/navigation.py`, vocabulary | M | None |
| 4 | No fix from a bearing of a sail | `reckoning.py:1358-1415` | S | None |
| 5 | The shore always a sighting; a `the nearest land` reading, in every sample | `lookout.py:294`, `api/readings.py` | S | Lines near any coast |
| 6 | Land ahead: a look-ahead along her true course over the ground, clamped by the visibility; notable under ten minutes, urgent under four | `lookout.py`, events in `api/readings.py` | M | Lines where she stands in |
| 7 | The sea breeze's direction from the coast's trend over a kilometre or two, and no breeze where the field is flat | `chart.py:601-625`, `weather.py:1234-1281` | S to M | None recorded |
| 8 | The anchor's place taken from the ship's own position | `core/world.py:578-584` | S | The 5c merchant passage |
| 9 | A lunar or other sight blended unless it is the better figure, and the line says what the master did with it | `reckoning.py:675-739`, `1989-2026` | S | None |
| 10 | The pilot's boat closes with the ship, and keeps closing | `ships.py:563-578` | S | Pilot ticks |
| 11 | The account at anchor, hove to and after a manoeuvre: the run since noon, fore-reaching, her way judged by eye until the log is next hove | `reckoning.py:1003-1170`, `2243-2265` | S | Passages that heave to |
| 12 | Bearings, the deep-sea lead and `heave the log` plainly within the officer's domain | the domain's data in `agent.py` | S | None; the brief's domain sentence |
| 13 | "The best bower is dragging" urgent; a pilot's hail notable | the lines' severities | S | Lines |
| 14 | *After 5 and 6:* `the port` and `the depth of water` by the captain's means: from the account, or from a cast | `ports.py:976-1018`, `api/readings.py:557-566` | S | None |

Items 1 and 2 are the two that answer the owner's own observation, and item 1 is the single
most useful change in this report. Item 14 must come last: today those two readings are the
only true numbers an officer has near land.

Item 7's cause is proved from the *Harpy*'s own checkpoint (5.6). The script that did it is
`evidence/tools/seabreeze_check.py`.

#### The station and the doors

| # | Change | Where | Size |
|---|---|---|---|
| 1 | A key issued with each seating and asked for on every call; a second door refused in words; a line in the log whenever the door behind a station changes | `remote.py:820-829`, `mcp_server.py`, `local.py` | M |
| 2 | The turn budget: `stand_by`, `opt_out` and `hand_over` always run; reads counted apart from orders, or not at all; every call not run is said and logged; the words fit the door; a setting; sixteen | `harness.py:212`, `tools.py` | S to M |
| 3 | A captain's word that lands in an open turn breaks the stand-by that follows | `harness.py` | S |
| 4 | A stand-by with the deck is broken by any notable line that concerns danger (dragging, fog, a sail, land closing, strain, a failed evolution), is told when its event can no longer come, and has a bound | `harness.py`, the events table | S to M |
| 5 | A station paused or silent with the deck: the deck returns to the captain, the clock eases, and the line is urgent | `harness.py:1525-1596` | S |
| 6 | The silence detector counts calls made inside an open turn | `harness.py` | S |
| 7 | The contrary detector: a stand-by that answers a nudge clears the chain; the nudge travels in the result of the order that caused it; drift counted only within two glasses | `harness.py:1452-1568`, `2007` | S each |
| 8 | ... and counts a link only when the later order undoes or re-says the earlier, from a table of opposites kept as data | `standing/runtime.py`, `data/vocabulary.yaml` | M |
| 9 | The journal: a tool that reads it; the last handover note and "N entries, latest at ..." in every brief; `read_log` able to reach back past 200 lines | `tools.py:554-559`, `harness.py:592-597` | M |
| 10 | The bridge asks for its station again when the game answers 404; its wait adapts when a call is cut | `mcp_server.py:438-441` | S |
| 11 | A sample's lines carry their actor, and the captain's orders are listed, not counted | the sample builder in `harness.py` | S |
| 12 | A watcher can stand down with a save | `tools.py` | S |
| 13 | An allowance says what it granted, and one that resolves by prefix to a verb already allowed is refused with the longer forms named | `orders/stations.py` | S |
| 14 | The handover threshold as a reserve in tokens, with a flag; no officer seated when the server reports no context; the stationing guard measured on the officer's brief | `local.py` | S |
| 15 | The 37b mending of section 6 | | S to M |

Items 1, 2 and 5 are the ones with a welfare side: a model acted under another's name, the
leaving tool can be refused, and a silent station was left holding the deck of a ship
standing into a lee shore. Do the detector's faults and the silence detector (6 to 8) before
making turns longer, or longer turns will be stopped as silence.

#### The log

| # | Change | Where | Size | Digests |
|---|---|---|---|---|
| 1 | "Aback": one flag per severity; the lesser lines re-armed by state (way on again, or wind again); the per-sail lines once an episode, and none for sails backed by order | `physics/integrate.py`, `physics/sails.py` | M | The six of 37c again |
| 2 | Wind shift: no line under a light breeze or while the wind is unsteady; "light and variable" said once; the same floor on the `a wind shift` event | `core/world.py`, `api/readings.py:2115` | S | Any recorded shift in light airs |
| 3 | A standing order with nothing to do logs one routine "held" line a watch | `standing/runtime.py:327-344` | S | The merchant passage's count |
| 4 | A no-bottom cast is routine, and "a sounding" as an event means bottom found | the lead's lines | S | Lines |
| 5 | What the officer says with the deck is notable | `harness.py` | S | None |

#### Small faults

All S unless marked.

- **Client.** Define `FATHOM` in `client/units.js`. Keep the track's hourly points and thin
  only for drawing. Fade bearing lines older than a glass. Name the captain's markers. The
  anchor in the state snapshot.
- **Boats.** One state machine for the boat, cleared when its evolution is belayed or
  dropped (M). A refused order must not move the person it named. The refusal says the rule:
  "she lies more than two miles from the road".
- **Numbers.** One reader for numbers in words, used by every order (M).
- **Sails.** `take in`, `furl`, `lower` and `clew up` reach the water sail and the jibs.
- **Hove to.** The flag cleared by anchoring, weighing and tacking; the starter book's trim
  rule given the dialect's own guard (`and she is not hove to`, 5.7), and `trim sails`
  itself declining to brace a hove-to ship round, as `steer` and `keep her full` decline; a
  hove-to ship that fills and gathers way says so, urgently.
- **Getting under way.** The fore-and-aft cast: tend the helm, hold the jib to windward, and
  never say "paid off" on a timeout (S to M; re-pins the merchant passage).
- **Tacking.** A tack that could not begin says why, and not in the words of a missed stay.
- **The anchor.** `heave in 70 fathoms` heaves in seventy. `come to an anchor in twelve
  fathoms` as the primer has it. `let go the anchor` logs "Brought up". A warning when the
  scope asked is more cable than sense, and when the water is under her draught.
- **At anchor and aground.** Go through the 26 refused verbs; `furl all sail` at least.
- **The filter.** `take in twenty tons of water` must not pass as the port's order.
- **Papers.** Her draught in the ship's papers. `the prices` shows every list the paper
  holds. A scenario's port names matched without regard to case, or refused aloud.
- **The carpenter**, sent for in a leaking ship, reports the well.
- **Replay.** An officer who took his station at tick 0 is seated by a replay before the
  game's opening line and not after it, which changes the digest of such a save (section
  9, question 1).
- **Words.** 1805, not 1806, in the brief and primer 16. "The breakwater" out of the
  Plymouth pilot's mouth. The gate's "£6,000". Hints that do not send `hail` to `haul`.

### 8.3 Build after a ruling

Since ruled, on 2026-10-05 (section 9): item 1 in part, and items 4, 5 and 6. The others
stand open.

| # | The matter | What needs ruling |
|---|---|---|
| 1 | A general grant of authority (note 15) | What stays out of it. The record suggests the port's business and belaying the captain's standing orders; the *Harpy*'s officer added "anything that can't be undone". Whether a grant lapses with the watch, as its own words say, or with `I have the deck` |
| 2 | The emergency route (gate ruling 1) | Whether the officer's own word opens it, logged notable with his reason, for a fixed set: the helm, heaving to, the anchor. The local games argue for logging it loudly: one model steered dead to windward unasked |
| 3 | Whether `say` ends a turn (note 21) | It is deliberate today. If it stops, the stand-by is the only close, and items 5 and 6 of the second table must be in first |
| 4 | The pilot (note 9) | Whether he is taken or declined by a plain order now, before signals exist; and whether, aboard, he cons, or warns, or only speaks |
| 5 | The master's own fixes in pilot waters | Whether fixing by cross bearings is the master's routine when marks are in sight, or is left to an order and a standing order. Anchor bearings at every anchoring, which the Regulations ask of a captain, are the smallest step |
| 6 | Relief of the watch by another model | Whether a station may change hands within a game, with the incoming model's consent and the handover note as its brief |
| 7 | What a ship knows of another port's trade | By which carrier: a paper aboard, the pilot's news, another master's word |
| 8 | The boat's errands | Several bargains to a trip, a second boat, or a list sent ashore at once |
| 9 | The well and the pumps | Whether a reading and a pumping duty come now. The reading alone moves digests, because the starter book's held rule would begin to fire |
| 10 | A late reply | Whether an order that answers a sample more than some minutes old is held and the model told |
| 11 | Who may ask a station back after a welfare stand-down | m5c-b seats it again like a returned deck |

### 8.4 Needs design work first

1. **A replay driven by the transcript** (8.1).
2. **The con.** The game knows who has the deck and not who is conning. Both groundings and
   near misses had two hands on the helm. "I'll con her" should be an order. *Since the
   owner's answer 5 (section 9) the deck can be taken and given back freely, which gives the
   captain a plain way to take the con. Whether a separate con is still wanted can wait on
   play.*
3. **Stand by until x, or y, or z**, with the standing dialect's own conditions ("when the
   depth is under ten fathoms", "when the mean wind exceeds five knots"). The dialect and the
   stand-by have separate lists today.
4. **Features by their parts, and how marks stand to one another**: "the west end of the Isle
   of Bas", "the Lavandière open of the island". By hand it is data, about eight lines a
   feature and a day's work for the five ports' approaches. Derived from the coastline it is
   a larger thing.
5. **The pilot as a voice**: asked anything, or given the helm. The owner said as much in
   the game (*Harpy*, 681,888). *Ruled later work, with the director (section 9, answer 6);
   his warnings come now.*
6. **What a sample carries.** Samples are four fifths of a conversation. Trimming what a
   long stand-by's digest repeats would save more than moving the journal out.
7. **Image tools** (note 25), after the same things exist as words.
8. **The drill for a station with authority**: one order given and refused, a budget met, and
   the three ways of leaving told apart.

### 8.5 Where I would push back

On the notes:

1. **"The reckoning made very precise close to land" (19).** Not by nearness. The account
   was within 110 metres ten minutes before the *Harpy* struck; what failed was a distance
   that did not move, a bearing that wrote it into the account, and a lookout with no urgent
   word. Mend those and let observation do the rest. A rule that shrinks the doubt because
   land is near is the truth leaking into the account, which the same review asks to be
   removed elsewhere.
2. **"On the Harpy that clause would have mattered" (the comment on 15).** It would not. The
   officer held the anchor, the tack and the helm, and used them. The clause is still worth
   having, for the box-haul refused off Roscoff and for the standing to order.
3. **Keeping the anchor out of a general grant.** In both the *Harpy* and the *Amazon* the
   anchor was the thing wanted in a hurry.
4. **A `keep` prefix as a new mechanism (16).** The dialect can already say it. Mend `trim`
   and the event, ship `at steady on the course then trim sails` in the starter book, and
   see whether a new form is still wanted.
5. **"A minimum wind strength would finish it off" (the comment on 18).** It would have left
   the floods at Scilly and off Roscoff, which came in a breeze. Mend the sea breeze.
6. **The journal out of the context (11).** A small saving for a change to a watched consent
   section. Give the station its journal to read first.
7. **Doubling the turn budget as the cure (21, local 3).** Size mends the Qwen games. What
   did the harm more widely is what is counted, what is silently dropped, and a message that
   names a tool the door does not have.
8. **Several stations through one door (23).** The opposite problem is the live one: a door
   is not bound to its station at all. Bind it first.
9. **Image tools (25) now.** A picture of the chart shows the account, which was wrong when
   it mattered. It helped the *Amazon*'s officer afterwards because the track was already
   drawn. Words first.
10. **The scripted passage as evidence for a captain or a director (5).** A clean run under a
    book written with the true chart in view, on a pinned wind, is evidence that the book is
    good. The officers' watches are the better evidence, and they are encouraging.
11. **Taken aback as only noise (17).** Five of the *Harpy*'s 31 were wanted, and the
    opposite fault is the dangerous one: a hove-to ship that fills is silent.

On the model's additions: the helm under sternway, the missing deep-sea lead, "three lead
orders at once", the "two cables" rule, "about 4½ hours" and "above twelve" do not hold as
stated (section 7).

On m5c-b: the opt-out path as written (section 6), and its claim that saves and simulation
are unchanged.

### 8.6 Already a later milestone's

Working a kedge, warping and towing (M8). Signals, hailing and colours (M7, M8). The officer
as a person aboard, a captain's station, and other ships with captains of their own (M6). The
director (M7b). The primer as a general guide and the vessel library's figures (M8). None of
these needs pulling forward for the gate.

### 8.7 The gate's four rulings

**1. The officer's domain as drawn.** Too tight for a watch near land. He should have
bearings, the deep-sea lead and the log; `fill away` after a heave-to he did not order;
heaving in with weighing and veering; and a course change judged by its effect, so that
`come up half a point` and `steer 340` are one thing. The "immediate danger" exception is
worth building as a standing allowance by the officer's own word, logged. It is not what
failed on the *Harpy*.

**2. The sample's size on a local model.** Not the limit, given a context size. Qwen 3.8
kept the thread for 27 hours and two folds at 102,400 tokens. Without a size nothing is
asked or trimmed, so an officer should not be seated when the server reports none. What
limited the local models was the turn budget, the stand-by, the silent reply cap, and the
order language of a fore-and-aft vessel.

**3. A far-detail vessel's bound.** Play gives no evidence either way: no ship was seen over
the land. Four free scenarios were written during the playtest, so "before any scenario is
written" has passed. The guard is one line and still worth having. The held estimate of 5.1
mattered far more to how other vessels looked.

**4. The re-asks.** The rule worked as written, on exactly the sections that changed, and it
is costly: batch changes. The drill is too small for a station with authority (8.4).

### 8.8 A suggested order

1. The saves: stamp them, have `load` say which road it took, and keep a few of the
   playtest's checkpoints as tests. The wider ruling on replay can follow (section 9,
   question 1).
2. Near land, the sea breeze, the anchor's place and the schooner's cast; re-measure once.
3. The station's safety: the seat key, the budget's exemptions, the lost word, the stand-by's
   wakes and bound, the paused deck, the detector.
4. The brief's one revision: 37b mended, the journal, `I have the deck`, the domain and the
   grant; one re-ask.
5. The log's noise and the small faults.
6. Then play what the gate still lacks: the naval cruise, the chronometer, British colours
   off Roscoff, and the lead's own watch.

## 9. Questions for the owner, and his answers

The ten questions as first put, each with the owner's answer of 2026-10-05 and what follows
from it. Where an answer is read further than its words, that is said, and it stays this
review's reading until he confirms it. The points still waiting on him are gathered at the
end.

### 1. Replay

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
  wrong default. The m5c opt-out that loads as a stand-down (section 6) is a slip of that
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

- The fixes of 8.2 change the game itself and not only the harness: the wind near a coast,
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
- Each build is kept in its own folder with its saves (answer 3), so that road stays open
  for every game but one: the *Harpy* after tick 527,255 was played on m5c-b before its
  second part was added, and that state of the build is in no folder now.
- Keeping old saves replayable has a running cost. Each change to a harness rule must carry
  a switch that plays old saves by the old rule; one exists already
  (`stand_by_ends_turn`). The change of answer 5 below is two functions without such a
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

### 2. The gate's verdict

*Is it to wait on the naval cruise and the lead's watch, or be given on what was played, with
the chronometer and the chase taken on the suite's word?*

**Answer.** It is not in question for the moment: it waits for the naval cruise and the
lead's watch. The work stays within the milestone and is checked as part of the final gate.

**What follows.** The order of 8.8 stands, with the gate's remaining play as its last step.

### 3. Builds

*Games 5 to 8 are taken here as plain m5c. Is that right?*

**Answer.** Saves were saved in their own folders: any save in a build's folder was played
on that build when it was saved.

**What follows.** Games 5 to 8 are plain m5c, as taken, and section 2 is amended. The rule
is also a reason to do new work in a folder of its own, so that `m5c` and `m5c-b` stay the
builds their saves were played on.

### 4. The grant

*What stays out of a general grant, and when does a grant lapse?*

**Answer.** By default a general grant should keep back the port's business and the
belaying or cancelling of the captain's standing orders, and perhaps anything else that the
standard of the era would make an unlikely grant.

**What follows.** The anchor is within a general grant (8.5, item 3). For the standard of
the era the project's own reference gives a start. The Regulations' chapter for the
lieutenant has him never change the course of the ship without the captain's directions,
unless it be necessary to avoid some danger (lead;
`docs/references/admiralty/regulations-and-instructions-1808-ocr.txt`, Sect. VI, Chap. I,
art. XIII). A general grant relaxes the first half. The second half is the emergency route
of 8.3's item 2, in the period's own words.

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

**Not yet answered: when a grant lapses.** A proposal that follows from answer 5: a grant
stands while the officer is seated, has force only while he has the deck, is said again in
the sample that gives him the deck, and ends when he is stood down or the captain says
`you may not`.

### 5. The deck

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
  (answer 10). A `stand_down` tool for any station, with a note for whoever sits next,
  would leave three ways that cannot be taken for one another: give the deck back and
  stay; stand down for now; withdraw.
- **The readings should say where a seated officer without the deck is** ("off watch"),
  and what he says should be notable with the deck or without, so that his warning reaches
  a captain who has taken the con.
- **Taking the deck becomes the captain's plain way to take the con** (8.4, item 2). On the
  cutter of game 5 a stale "You may steer" turned her 44 minutes after the captain's "I'll
  con her", which the game took for talk. Had he taken the deck, that order would have been
  refused.

All of it touches the consent brief's watched sections and belongs in the one revision of
8.1.

### 6. The pilot

*Taken or declined by an order now? And aboard: does he con, warn, or speak?*

**Answer.** For now an order accepts or declines the pilotage when the pilot first hails,
with a simple form of hailing if none exists. Aboard, conning is too much for now. He
should warn when she approaches a danger, a shoal and the like, as is reasonable. Speaking
and conning wait for the director, where a model can take him over and answer for him.

**What follows.** No hailing exists today: `hail the pilot` is not an order (5.2). The
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
- He does not con and he answers nothing new. 8.4's item 5 moves to the director's
  milestone.

His warning and the lookout's (8.2, near land, item 6) are two halves of one thing: the
lookout calls the land a man can see, and the pilot the shoal he cannot.

### 7. Fixing in pilot waters

*The master's routine, or an order and a standing order?*

**Answer.** `take a fix` can simply be an order, used freely like any other. It need not be
a routine.

**What follows.** 8.2's near-land item 3 as written, open to the officer and usable in a
standing order (`every glass then take a fix`). The master does no fixing of his own, and
8.3's item 5 is closed.

### 8. Relief

*May another model take a station within a game?*

**Answer.** Yes. When a model stands down from a station, the same model or another must
still be able to take it up, so that a stand-down never locks a station out of a game for
the player.

**What follows.** The rule that refuses a station once held to any other identity goes. A
station that is *held* stays refused, which the seat key of 8.2 makes safe. The incoming
model gives its own consent and has the handover note in its brief. Read further than the
answer's words, for the owner to confirm:

- **A leaving by `opt_out`, final or not, is the leaving of the model that made it.** It
  should bar or re-ask that model only, and never close the station to another.
- **Whether a relief of other weights reads the journal of the one before it**, or only the
  notes written for a relief, should be said in the brief's journal section.

### 9. The consent record of 3 October

*It was answered by the session that wrote the change. Should it stand, or be asked afresh of
a session that did not?*

**Answer.** Plenty of fresh consents will be taken after the harness changes, so yes.

**What follows.** Read here as: no separate re-ask now. The record stands as what was
answered on the day, and the one revision of the brief (8.1) asks every identity again,
Opus 5.5 among them, of sessions that did not write the change.

### 10. The watcher's leaving

*Its `opt_out` at the captain's word was not a withdrawal. Should the record say so?*

**Answer.** Yes. He believes no opt-out in any test so far, this one included, has been
other than amicable.

**What follows.** Recorded here: the Qwen 3.8 watcher's `opt_out` on the *Harpy* (tick
216,817) was made at the captain's word, to stand down with a save after `hand_over` was
refused to a watcher. It was not a withdrawal of consent. The logs bear the owner out
(lead): the eight games hold one line of a station leaving the game, and it is this one.
The only other use of the token in the record was in a consent conversation and was an
accident, the token quoted inside a yes (5.12). The consent records themselves are read by
the game and should not be edited by hand. The `stand_down` tool of answer 5 would make the
difference a matter of record from then on.

### The five points that waited, and the owner's rulings of 2026-10-07

1. **Replay** (question 1). "As recommended, save is exact from the checkpoint, replay is
   promised only on the build that made it." Built in 37d, and proved on a five-day game
   (10.2).
2. **The general grant** (question 4). "The proposed held-back list is approved for the
   first version of the general authority grant. It should lapse when the officer is fully
   stood down, or the authority is directly countermanded by the captain." So it stands
   through the deck going to and fro, which answer 5 had already implied.
3. **The three ways of leaving** (question 5). "Approved as read, parity for the officer's
   hand_over and the captain's, stand_down for the amicable save and exit."
4. **The pilot's hail unanswered** (question 6). "The pilot may keep company, hail once
   more, and bear away. He may warn of the shoal water or shore ahead with true knowledge
   in his water. Thick weather means he cannot see his marks."
5. **A final opt-out and relief** (question 8). "Yes, a final opt-out (need to be careful
   of false-positives, but a fair start) should bar the model, not the station. The relief
   may read the journal of the last holder of the station, as with a standard re-seat."

Points 2, 3 and 5 are built by package 37g, and point 4 by 37h; the briefs are in the
build folder's `docs/dev/M5-WorkPackages.md`. One matter of 8.3 had stayed open, the way
out of danger on the officer's own word (item 2 there). It was written into 37g's brief as
a proposal, and the owner kept it on 2026-10-07: "37g is pre-approved with 19. (the way out
of danger) kept as proposed." So an officer with the deck and no grant may, on its own word
and giving its reason, put the helm over, heave to or let go an anchor to avoid an
immediate danger, and the log says that it did and why.

**Approvals, 2026-10-07.** 37e approved and launched. 37f approved, to be launched when
the lead's checks of 37e have passed. 37g approved beforehand, as briefed.

### How the work is to be done

By the owner's word of 2026-10-05: locally, in the gate folders, with no commits, and with
the GitHub repository and its worktree left alone. He folds the work in with the lead
session that works the repository. m5c-b set the pattern for that: a folder of its own
beside `m5c`, a CHANGES note, and one diff against m5c as cut.

## 10. The first game on m5c-c (game 9)

Added 2026-10-07. The owner played the build folder `FreeSail-gate-m5c-c` (m5c, the m5c-b
changes, and package 37d) on 6 October and left two saves and six notes
(`m5c-c Notes.txt`); he also supplied the officer's own summary from the chat
(`evidence/harpy-m5cc-post-session-chat.md`). This section is that game: what happened, what
37d did in play, his notes and the officer's findings checked one by one, and what it changes
in the plan.

**How it was checked.** No reader sessions this time. The lead read the whole log (7,140
lines), the officer's 631 transcript entries and its journal, and every line the owner typed.
Then a scratch copy of the last save was replayed on the build that wrote it, with a probe
recording the true position, the account and the master's doubt once a minute and at every
observation. The replay reproduced the played log exactly, line for line and digest for
digest, so the figures below are of the game as it was played. The tables in full are in
`evidence/G9-brig-m5cc-measurements.txt`; the scripts are in `evidence/tools`. Everything in
this section is the lead's own reading unless it says "the officer says" or "not checked".

### 10.1 What was played

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

### 10.2 What package 37d did in play

**The saves.** Both saves carry the build's stamp. Replayed on that build, the game came out
identical: 7,140 lines, the same digest, with a model aboard for 78 hours, two seatings and
631 recorded replies. This is the first real test of the rule recommended under question 1
of section 9 (exact from the checkpoint, and replayable on the build that wrote it), and it
passes on a five-day game.

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
marks it was two to five miles out, and once eight; 10.3 takes that up under note 2.

**The landfall.** The first bearing of the Isle of Bas, at twelve miles after a night's run,
took the account from 7.1 miles out to 0.7: the estimated distance was laid down, as 37d's
second pass meant it to be.

**`take a fix`.** 61 fixes. The fix's own distance from the truth: a median of 1.2 cables,
nine in ten within 7 cables, the worst 1.1 miles. Three things about it are taken up below:
it chooses far marks when near ones are in sight, its "good to" is too hopeful, and at anchor
it can move a right account.

**`the nearest land`.** The officer found the reading in the library and wrote two standing
orders on it ("every glass, if the nearest land is under 3 miles then take a fix").

**Land ahead.** Three lines. The urgent one, "The Mingan close ahead, on the starboard bow,
four cables!", came five minutes before she passed the rock at 1.2 cables. 10.5 has more.

**The wind.** Nothing like the *Harpy*'s afternoon off Penlee came back: 50 wind-shift lines
in five days against game 2's 363 in eight. Most of the 50 are of another kind (10.5).

### 10.3 The owner's six notes

Tags as in section 7.

**1. "Take a fix and the other reckoning changes seem good so far."** Borne out by the
measurements above. Three qualifications, all for the next package:

- *The fix prefers far marks.* In the Goulet four fixes were worked by marks three to seven
  miles off (Camaret, Brest, Conquet, Pezeaux), with Petit Minou inside a mile and the Mingan
  closing from two. Their lines met within six cables at best and a mile and a half at
  worst. They left the account 1 to 3 cables out; each bearing and distance of Petit Minou
  then brought it to one cable or less. The cause is the brief's rule (the lead's): the
  master picks the marks that cut at the widest angles, and nearness only breaks ties.
  **Now.**
- *"Good to" is too hopeful.* In 12 fixes of 61 the true error was more than twice the
  stated figure. The cocked hat "inside three cables" that the officer admired at 06:05 on
  the 16th was 1.1 miles from the truth. Every bearing carries the compass's own error, about
  two and a half degrees in this ship (measured: 2.2 to 2.6), and the three lines of a fix
  share it, so a tight hat can sit well off the ship: four cables at ten miles, a quarter
  cable at one mile. The stated doubt counts only each line's separate error. **Now**: count
  the shared error, which also makes the master prefer near marks. The period's cure is in
  the game already and nobody used it: `observe an amplitude` corrects the variation.
- *A fix replaces the account even when it is the poorer figure.* Moored in Brest road, her
  account right to a cable, the standing order's fix by the castle and St Matthew's light
  (eleven miles off) moved it nearly a mile, and the next one left it six cables out. **Now**,
  with the rule under note 5.

**2. "Reckoning uncertainty drift with no visible marks was deemed a bit low by the
officer."** It is far too low for these waters, and the measurements make the size plain.
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

**Now**, as the heart of the next package. One choice in it is the owner's, and is put in
10.6: how the master's doubt comes to know that the tides run strong where she is. A second
remedy is already in the game and was not used: `allow two knots of set to the westward`
tells the master to carry a stream in his reckoning.

**3. The officer's interest in a command of its own, and lessons in the primer.** The
exchange is in the log (14 June 23:30). Asked whether a command would interest it, the
officer said yes, and that it would want first "to have made a few more landfalls on my own
reckoning, and taken her in and out of a road or two without your hand on the con". The
captain's station is Milestone 6 by the documents (**Later**); the lessons can start now as
writing (**Design**, small). This game supplies their matter. What the officer says it
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

**4. A wardroom under a model captain; several stations through several doors.** A design
decision for Milestone 6 (**Later**), with one part due now. The question in the note,
whether it needs several servers: no. One game is one server; each client starts its own
small bridge, which connects to that one game and asks for one station. Two doors have
served one game already: in game 2 a Qwen watcher at the local door and the Opus officer
through Claude Desktop were both seated in one game, on one server. What a model captain
with a model officer would need:

- the captain's station itself, and officers as people with stations of their own (both
  Milestone 6);
- the seat tied to the door and the identity that took it. Today a station is found by its
  name alone, so calls from another door can reach it. The officer raised this again in its
  consent answer of 6 October. It is already in the station-safety package (8.2), and it is
  the one part to build before any such trial;
- a rule for pace when two models are sampled in the same minute, and for cost;
- a consent record for each identity, as now, and a brief for the captain's station;
- a ruling on what the owner is in such a game, and who may give `you may` to whom.

**5. "A lunar with a poor certainty still overrode the better account."** Confirmed. The
lunar gave 5° 23' W, "which he would trust within 25 miles"; the account took that longitude
outright, and its doubt east and west went from 0.8 mile to 12. Two things the owner should
know:

- *This was never in 37d.* The owner told the officer it "was supposed to be fixed in this
  version". 37d's second pass guarded one thing only, the estimated distance after a
  bearing. The lunar and the noon latitude still follow the older rule (an observation
  replaces the account once she has run two miles since the last one), and that rule was
  kept back for the next package, where it is the first item.
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
overruled by it. **Now**: 10.6 states the rule that would replace it.

**6. "The brig still likes to come through the wind when hove to."** Confirmed, in four
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

**Now.** The owner's guard for a trim rule ("and the manoeuvre in hand is not hove to") was
in his book this game and worked.

### 10.4 The officer's findings, checked

The officer's list is in its journal and its summary. Each is set against the log, the
replay or the code.

**Right as said**

| The officer says | What the record shows |
|---|---|
| A lunar good to 25 miles replaced an account good to a mile | 10.3, note 5 |
| The noon latitude of the 16th was not applied | 10.3, note 5 |
| The doubt shrank while she drifted becalmed | 10.3, note 2 |
| The doubt stood at "a mile" through four hours of fog | It grew from 0.5 to 1.1; the true error reached 8.3 miles |
| She spins out of a heave-to | 10.3, note 6 |
| "Weigh the small bower" weighs the anchor she rides by | Tried on the last checkpoint: `weigh the small bower` weighed the best bower. The name is dropped without a word. The owner met it too, weighing at Roscoff on the 14th |
| "Loose the topsails" set them | The log: both sheeted home, the main topsail aback, and an anchor dragged for it |
| `shape a course` checks rocks and not the shore | Shaped for Brest from off Roscoff, the line ran across the land with no word. The waypoint the officer chose off Petit Minou lay against the shore, the line "came back clear", and the lookout's land-ahead line was the first warning |
| All hands called under the grant are logged "by the captain's order" | The words are fixed in the code |
| "Trim sails" refuses in a knot of air | Refused under one knot of wind across the deck; a standing order met it ten times |
| A second grant of one kind hides the first in the readings | So the code: grants are kept one to an order word. 10.5 says what follows from it |
| No fog signal; `heave short` takes no number; no order to shift the head sheets over | The orders are not in the language |
| "The chart ends here" reads as if the world stops | The words are the lookout's, for no charted marks beyond |
| "A moonlit night; the land may be made out at a league", said in thick fog | In the log at 22:44 on the 13th, inside the fog of 20:00 to midnight |
| The readings do not show the orders waiting for hands | The owner's window shows them; the officer's readings do not |

**Right, but the cause is another**

| The officer says | What it is |
|---|---|
| "A veer goes past the number: 75 ran to 228, 180 to 240, 45 to 67" | Three things. `let go` veers five times the depth by itself: 128 fathoms in 26½, 67 in 13. So "veer to 75" and "veer to 45" found more out already and were refused, in clear words. And with an anchor named, "to" is lost: `veer the small bower to 100 fathoms` veered 100 **more**, and on the best bower, the one she rode by. Tried on the last checkpoint: `veer to 80` goes to 80; `veer the best bower to 80` goes to 148; `veer the small bower to 80` puts the best bower at 148 |
| "Anchors report dragging while the ship isn't moving; the slack one sets off the alarm" | In the Goulet the anchors did come home: the best bower two cables in seven hours, the small bower nearly two in eight, the sheet anchor half a cable in four. The ground there is "rock and mud", which the game counts as rock, holding about a third of what good ground holds. What misleads is the flag: it stays up five minutes after an anchor last moved, slack or not, and each relapse is a fresh urgent line. There were 18 in eight hours, each waking the officer and easing the clock |
| "Fill away picks the old course or the wrong tack" | It always takes the tack she hove to on (10.3, note 6) |
| "The doubt grew with the drift in the fog on the 15th, a welcome change" | It did not grow with the drift. A cast of the deep-sea lead replaced the doubt across the sounding's line with the cast's own three miles. Hove to, the doubt does not grow at all |
| "The lookout and the bearing disagree by a point; the in-sight line may be stale" | The lookout speaks the true bearing; a bearing order carries the compass's two and a half degrees, which here crossed the boundary between two points. Nothing is stale |
| "A bearing that left the position unchanged cut the doubt from three miles to one" | By chance the compass's error made the bearing agree with the account exactly, so nothing moved. A line does properly narrow the doubt across itself. The fault is that the words give only east and west, north and south, and hide a doubt that is now long and thin along the sight |
| "The account sat on the Mingan while the lookout had it astern" | After the bearings of 16:32 the account was right to a quarter of a cable. Six minutes later it was two cables out again and at 16:42 three and a half: the flood was carrying her, and the account knows nothing of the stream (10.3, note 2) |
| Waiting for "six bells" in the last dog watch never wakes | The last dog watch strikes no six bells, so the wait ran past the watch, and sunset's notable line ended it at 20:28. Whether it would have ended at six bells of the first watch was not checked |

**Its own mistakes**, named by the officer and borne out: hauling toward the wind with the
studding sails set (taken aback at 04:03 on the 15th); three anchors on far too much cable
in a berth two cables from the shore; reading the sheets wrong twice; "shift the headsails",
which the ship rightly took as unbending them.

**What worked, by the officer's account and the record:** the fixes, the list of dangers on
a shaped course (new to it since the *Speedwell*, and it used the warning to choose a safer
holding point at 02:20 on the 16th), the deep-sea lead with its ground, the pilot's words,
the boat for prices, and the refusals that say what to do next ("rig it out first").

### 10.5 What neither noted

Found by the lead in the log and the replay.

**The harness paused the officer in the Goulet.** At 16:38 on the 16th, three minutes after
the Mingan passed at a cable and a quarter and with the wind failing, the contrary-orders
detector paused the officer for "steer NE; steer 53; steer ENE; steer NE by E". Those were
four small alterations to pass a rock. The owner typed `resume the officer` six seconds
later. Had he been away, the officer would have stayed paused with the deck for ten real
minutes and then been stood down. Over the game the detector spoke eleven times (ten nudges
and this pause) and every one was ordinary conning: small changes of course chasing a light
wind, heaving to and filling away for a pilot, letting go and veering. Section 5.4 found it
wrong 29 times in 31 in the earlier games; with this game that is 40 in 42. It is in the
station-safety package already; this raises its place in it.

**Twenty-three grants, and two of them waited for at a bad moment.** The owner told the
officer "you have the con and nav and general authority in to Brest", and there is no order
that says so. Each thing was granted by name as it was refused. Calling all hands was
refused while she lay aback; letting go the anchor was refused in the Goulet as the wind
died, and granted 23 seconds later. This is question 4 of section 9, the general grant, with
a game's worth of evidence.

**A grant's place is not checked.** The owner granted each of the officer's five waypoints
by name. The first would have done for all: a grant is matched by its order word alone, and
the words after it are kept only to be shown. `You may shape a course for Brest` in fact
allows a course shaped for anywhere, and the officer later shaped for seven places never
granted, each taken. It did no harm here. It matters for the general grant, where a new
destination is on the proposed kept-back list (section 9, question 4): as built, the game
cannot keep one destination back while allowing another.

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

**At the Mingan the cry was right, and the map was not.** The owner told the officer not to
overreact, "the alert does not mean a strike incoming". By the true track she passed 1.2
cables from the rock. When the lookout cried it was 4.8 cables off; the account, which is
what the owner's chart draws, had it at 8.3. So the warning was sound and the picture he
judged it by was three and a half cables kind. One change is worth making to the words: the
line said "She will be on it in three minutes", and she was never going to be on it. A cry
that says how near she will pass ("standing to pass within a cable of it") would be truer
and would not be read as a strike.

**Fog on the stroke of eight bells.** Seven spells of fog in five days, each beginning and
ending exactly at eight bells and lasting four hours or eight; about a quarter of the game.
Fog is common off Ushant in summer, but fog that keeps the ship's bells is the weather
model's four-hour step showing. **Later**, with the weather's polish.

**The log.**

- 31 of the 50 wind-shift lines came with under four knots of wind, and 18 of them in a calm
  at anchor ("Wind veered to S, calm."). In a calm the wind has no direction worth a notable
  line. Section 6 asked for a floor on 37c's rule; this is the case for it.
- "Her sails aback; she had no way on to lose", ten times in three hours becalmed, each
  notable.
- 25 notable "could not" lines for things already done ("Could not set the jib: The jib is
  set already").

**The standing-order book.** The owner needed four tries to write 'Triangulate'. "The
distance to the land" was entered each time and then quietly held at every firing ("the
distance to the land is not on the chart"). A condition that names nothing the ship knows
should be refused when the rule is entered.

**The ground's words.** "Rock and mud" in the Goulet and "sand and rock" at Roscoff both
count as rock, the worst word in the note. Brest road has no bottom note at all, though the
pilot says mud. Small, and worth a look when the ground tackle is opened.

**"Take a bearing of Bas"**, with only the island's shore in sight and not yet its mark,
is now refused as "the land close aboard is no mark of the chart ... name a headland", to a
captain who has just named one. Before 37d it said the Isle of Bas was not in sight and
listed what was. The older words were the clearer.

### 10.6 What this changes in the plan

Nothing in sections 8 and 9 is overturned. The game sharpens the next package and adds to
it. All of what follows is proposed, for the owner's word; nothing is built.

**The account's rule, stated once.** Today there are three rules for when an observation is
believed: the two-mile run (sights, soundings, plain bearings), the second pass's guard (a
bearing's distance), and outright replacement (a fix). This game shows each failing. One
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
and a new duty at a station is a change to the consent brief, which is being held to one
revision (8.1).

**The package itself is now too big for one.** It was to hold the wind lines, the ground and
the account. With this game's findings it is better built as two, one after the other, since
both move the recorded passages:

- *The account*: the rule above; the doubt; the fix's choice of marks and its "good to";
  the account pinned at anchor; and the merchant passage's book tuned for a true account,
  with the fix put back in its pilot-water rule (the stopgap of 37d's second pass).
- *Lying to and the ground*: heaving to that holds its tack; `fill away` on the tack she is
  on; the hove-to record cleared by the anchor; the guard in the shipped books' trim rules;
  an anchor's name honoured by `veer`, `weigh` and `heave short`, or refused in words;
  "to" kept when an anchor is named; `let go` saying the scope it will veer, and taking one
  ("let go the best bower and veer to 45 fathoms"); `heave in to N fathoms`; one dragging
  line an episode and a flag that drops when the anchor holds; the wind-shift floor; the
  aback and "already" lines made quiet; and a standing order's condition checked on entry.

**Small additions elsewhere.**

- `shape a course` should say when its line crosses or skirts the shore, as it does for
  charted rocks. 37d built the means (the nearest shore). **Now**, small.
- The land-ahead cry should say how near she will pass. **Now**, small.
- The station-safety package: the detector first. A general grant (question 4) would have
  saved most of this game's refusals.
- **The chart in words.** The owner raised it in the game (a "show me the chart" feature,
  "that's on the books") and the officer called it "the single most useful thing on the
  books for this kind of work". It is the second officer to ask: the *Amazon*'s asked for "a word
  picture of the near coast" (section 7). **Design**, as in 8.4, and now with a plain
  requirement from play: what the officer lacked was where the shore runs between the named
  points. Whatever is built must be drawn from the account and not from the truth, or it
  becomes a fourth reading that gives the position away (5.1).
- A fog signal (a bell; a gun waits for powder). **Later.**

**For the gate's checklist (section 4).** Game 9 adds: a fourth long watch by Opus 5.5, on
m5c-c; a star lunar; mooring and unmooring twice, three anchors down, dragging on bad
ground; a cargo bought at Roscoff and prices fetched at Brest; Roscoff and Brest under
American colours; and, for item 13, a save with a station held that both loads from its
checkpoint and replays exactly. It still does not run either of the gate's two scenarios,
the naval cruise, the chronometer or British colours off Roscoff.

**The plan as ruled, 2026-10-07.** The owner took the split, and joined the station's
safety to the consent brief's revision, so that three packages follow 37d, one at a time:

- **37e, the account**: the rule above, the honest doubt, the fix's marks, the master's
  tide, a shaped course that makes good, and the books re-tuned.
- **37f, lying to and the ground**: as listed above, with three rulings. `loose` stays as
  it is and sets the sail ("Loose should remain as is"). `trim sails` declines while she is
  hove to. `let go` keeps veering the scope the depth wants, says the figure, and takes a
  number.
- **37g, the station's safety, and the deck, the leaving and the grant**: the faults of 5.4
  and 10.5, and every change that asks the consent question again, in one revision of the
  brief.

The pilot is 37h. The three briefs are in the build folder's
`docs/dev/M5-WorkPackages.md`, for his review before any is launched.

**Where I would push back.**

- On the officer's ground-tackle list as written. Two of its four items are not faults of
  the kind it says (the veer; the dragging), and a builder handed that list would chase the
  wrong things. The table in 10.4 is the list to build from.
- On reading the doubt's growth in the fog of the 15th as a mend. It was an accident of the
  lead line.
- On making the land-ahead cry milder. It was the one thing in the Goulet that was right to
  the cable.
- Gently, on the lessons as a cure for the officer's trouble at anchor. A lesson would have
  helped with scope. It would not have told it that `veer the small bower to 100` meant
  a hundred more on another anchor.

## 11. The first game on the build with 37e, 37f and 37g (game 10)

Added 2026-10-08. On the night of 7 to 8 October the owner played the build folder as it
stood after 37g's second pass (build `m5c-c/37g`): everything planned in sections 8 to 10
that has been built, which is packages 37d, 37e, 37f and 37g with the leaner consent brief.
Not in it: the pilot (37h, not written), the follow-up pass, and whatever else in this report
has not been built. He left two saves and gave two notes in conversation, quoted in 11.2.
This section is that game.

**How it was checked.** As for game 9, with no reader sessions. The lead read the log (4,240
lines), the officer's 414 transcript entries and its journal, and every line the owner typed,
then replayed a scratch copy of the last save on the build that wrote it, with a probe
recording the true position, the account, the master's doubt as he would state it, the depth
and the tide twice a minute and at every observation. The replay reproduced the played log
but for one line (11.3, the saves), and the ship's place at the end was the same, so the
figures below are of the game as it was played. The tables in full are in
`evidence/G10-cutter-m5cc-measurements.txt`; the scripts are in `evidence/tools`. Everything
here is the lead's own reading unless it says otherwise.

### 11.1 What was played

One game, seed 7, the scenario "A merchant cutter, free" under American colours, from Carrick
Road on 12 June 05:00 to eight miles south-east of St Mary's on 14 June 20:00: 63 hours of
ship's time. The owner was captain throughout. The officer of the watch, in the place of Mr
Pearce, was Qwen 3.8 27B (Q4_K_M) under llama.cpp through the local runner, with a context of
102,400 tokens: the same model, server and size of context as game 7.

- **The consent question was put again**, as the rule requires, with the lean brief and the
  notice of why (the four sections named). The first reply was empty; after the reminder the
  answer was a yes with no condition. The drill was passed on the last of its four replies
  (11.3). The record is `docs/agents/consent/2026-10-07-qwen3.8-27b-0814-q4_k_m.gguf.md`.
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
  04:08 a cast moved the reckoning a mile (11.2); he anchored again, with some trouble
  (11.3), and moored.
- **14 June 08:00, the first seating ended** when the model server refused the conversation
  for its size. The same model was seated again eight seconds later, the second seating, and
  read its journal.
- **The day at St Mary's.** The salt sold at £28, twenty tons of salt fish bought. At 15:15 the
  deck and the general authority again. Unmoored and weighed by 16:44, out to the south-east
  with the St Mary's pilot aboard for an hour, and a course shaped for Ushant at 17:34.
- **14 June 20:00, the second seating ended** the same way, and the owner stopped there.

The officer had the deck for 48 hours in the first seating and for nearly five in the
second. Nothing was carried away and she did not touch the ground.

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
as 10.5 found in game 9.

### 11.2 The owner's two notes

**1. "Thought block seems to be hitting token limit and stopping the turn rather than
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

**2. "Single stray sounding during a sudden fog bank while entering St Mary's caused a jump
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

### 11.3 What the three packages did in play

**37e, the account.**

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
- **The cast**, as in 11.2.
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

**37f, lying to and the ground.**

- **Hove to, she held.** The second heave-to on the 12th held for fourteen minutes until
  `fill away and steer sse` took her off, as it should. Off the Sound on the 14th she lay
  hove to for about seventy minutes, some four points from the wind, forereaching at about a
  knot.
- **The first heave-to did not hold, and not for the old reason.** The officer was hauling
  down the foresail, at the pilot's hail, while the captain hove to; the heave-to backed
  that same foresail, said "Hove to", and she filled within a minute. The second, which
  backed the jib, held. A heave-to should back a sail that is set.
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
  - one followed a helm order the ship misread (11.4, the order's words);
  - one came in four knots of wind after the headsail sheets were eased;
  - one was the yards left aback by a heave-to belayed half done, and was right.
- **A standing order's action is not read when it is given.** The officer's "the fix at the
  watch" was accepted with the action "take a fix as soon as a bearing can be taken", which
  the ship then read at each change of the watch as a mark of that name, and refused four
  times before the owner replaced it. 37f checks the condition at entry; the action wants
  the same.

**37g, the station.**

- **The detector for orders undoing one another said nothing all game**, where in game 9 it
  spoke ten times and paused the officer once, wrongly each time.
- **The deck, the grants and the general authority worked as built.** The general
  authority's line in the log names everything kept back. A named grant said what it
  allowed ("may helm a lee: the course is his to alter, by any of its orders").
- **The way out of danger was tried once and refused rightly**: taken aback at 14:10 on
  the 12th, the officer asked to wear on its own word, and wearing is not one of the three
  things. But its first try, three minutes before, was "Put the helm over to starboard
  ...", which the ship does not understand. "Put the helm over" is the officer's brief's
  own phrase for the way out, and it is not an order.
- **The relief worked.** The second seating found its journal and the last handover note
  and carried on.
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
  model and this context without trouble. This review recommended the change (section 8,
  item 14 of the harness list: "the handover threshold as a reserve in tokens"), on
  arithmetic in section 5 that took the four-character count for true; 37g made the
  reserve 14,000, and the short count eats nearly all of it.
- **The samples have grown.** The largest in the second seating were 13,000 to 25,000
  characters, after long stand-bys at anchor. A cast of the lead every five minutes by
  standing order is a notable line each time, and so is every note the officer writes with
  its orders (280 of them); all of these are listed in the sample that ends a stand-by.
- **The consent drill miscounted.** The model sent the three calls in one reply. The
  journal shows all three ran, but the drill counted only the stand-by and asked for the
  other two; when they were sent again it asked for the stand-by again. The model passed on
  the last reply it was allowed. Not traced in the code.
- **The saves.** Both carry the build's stamp and load from their checkpoints. Replayed on
  the build that wrote it, the last save comes out one log line short of the game as
  played: where the door stood the station down at 08:00 on the 14th, the replay leaves out
  the line that says the officer was sampled. The ship's place at the end is the same. By
  the owner's ruling of 7 October a replay is promised on the build that made the save, so
  this is a fault, though a small one.

### 11.4 What else the game showed

**A course with a half point is read as its last word.** `Steer south by west half west`
was taken as "steer west; W (270°)", and so was `steer west north west half west`. The first
time the wind was at WSW and she was taken aback 37 seconds later. This is worse than a
refusal: the order is accepted and the ship steers somewhere else.

**The reading of the nearest land in fog invites a wrong reading.** In thick weather it
says "not to be seen: in this weather the shore shows within a cable at most". The officer
read that as land within a cable. At 08:01 on the 13th, in mid-Channel with no land within
leagues, it hove to on that, under the general authority, and the owner had to countermand
it; the yards left aback by the belayed heave-to were one of the eight alarms. It quoted the
same words again in the Sound.

**St Mary's Sound.**

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

**Standing orders that cannot act say so every time.** Thirty-three refusals, most of them
"Trim the Fore and Afts" while at anchor and "Bearings" or the fix at the watch with nothing
in sight. They are routine lines and do no harm, but the owner's condition "if the manoeuvre
in hand is not hove to" did not cover lying at anchor, and nothing told him so.

### 11.5 The officer

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

### 11.6 What this changes in the plan

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
standing order's action read when it is given. The phrasings in 11.4. The drill's count.

**For 37h, when it is written.** The depths in St Mary's Sound against the pilot's own
directions; the dangers he names shown by name; and a pilot who is aboard three times in
one game and takes her nowhere.

**The consent brief stands as approved.** The owner seated the model before the question of
the seven words (the fourth sign the harness counts) was answered, so the brief has now been
put to one identity as he approved it. Adding the words now would ask that identity a second
time. The lead's advice is to leave it; both stations' briefs state the fourth sign.

**Where the lead was wrong.**

- The one rule, applied to a cast of the lead as to a fix. That was in the brief of 37e.
- The handover reserve. That came from this review's own recommendation, and game 7 is the
  evidence that the fraction it replaced was safe at this context.
- In the first read of this game given to the owner, the lead said three of the alarms came
  of "a small header". On a closer look they came at the edge of squalls, with the wind
  falling and shifting by 16 to 50 degrees, and were real.
