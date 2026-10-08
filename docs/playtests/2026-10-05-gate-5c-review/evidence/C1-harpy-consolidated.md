# C1. The *Harpy* (session `2-harpy-brig-opus`): consolidated record

Made from slice reports H1 to H5 and part B of L2. "Checked" means I looked the point up in the dump. "(reader's reading)" marks a cause a reader traced in the source; "(collator's reading)" one I traced myself, read-only. Notes: O1 to O25 are the owner's items, M the playtesting model's comments and additions, L1 to L5 the local notes.

## 1. The game in brief

| | |
|---|---|
| Ship | Brig *Harpy*, "A merchant brig, free" (seed 7), American colours. The ship file is H.M. brig-sloop *Harpy*: 121 men, a hold of 32 tons |
| Voyage | Falmouth, Roscoff, Falmouth Bay (entrance missed), Plymouth. 12 June 1805 05:00 to 20 June 04:37; 689,841 ticks; 9,272 log events (2,124 notable, 33 urgent) |
| Captain | The owner: 432 typed lines, 147 of them words to the officer |
| Officer | "Mr Pearce", Opus 5.5 through the MCP door (Claude Desktop); five seatings; 300 orders, 262 stand-by calls |
| Watcher | Qwen 3.8 27b through the local runner, 14 June 14:43 to 17:13 (207,784 to 216,817) |
| Build | m5c as cut to tick 527,255, then m5c-b's first part only. All 31 `ship.aback` lines are urgent in the old words |
| Outcome | Purse £1,000 to £5,148. Aground on Penlee Point 19 June 13:50:53 (636,653); afloat that evening; ended at anchor in Cawsand Bay |

## 2. What happened

**12 June.** The brig lay in Carrick Road, Falmouth. The captain gave the officer the deck at 05:06 (389) and told him to lead. The officer read the port chapter and the papers, proposed tin for Roscoff and brandy home, sent the purser for prices, and bought seven tons of tin for £840 (6,143). She weighed at 09:16. A Falmouth pilot boarded unasked while she was under way (16,020) and was put off at 10:09. That evening the officer's Claude Desktop conversation died. A new one took up the station at 19:08 (50,908) with no brief and no journal, and the captain had to print the journal into the log (51,753).

**13 and 14 June.** Fog came down at 08:00 and the officer hove to on his own judgement (102,690) until 16:00. He then ran E by S for the Isle of Bas on an account ten miles out and passed north of it unseeing; the captain caught it from his chart at 18:41 (135,709). A Roscoff pilot boarded nine miles from his entrance (139,620), never took her in, and left at 23:34 after she had lain hove to in fog a mile off the island. At 05:07 on the 14th the officer anchored outside the western entrance (173,251). The anchor dragged twice while he stood by, and the captain let go the second. From there, without entering, she sold the tin for £1,785 and bought fifteen tons of brandy for £1,500. A local Qwen model stood as watcher from 14:43. She unmoored, missed a tack, took a second unasked pilot, was taken aback and box-hauled clear (213,590). The officer handed over to start a fresh conversation (216,549) and was seated again (216,817).

**14 to 18 June.** A beat up-Channel. From 22:09 on the 15th to the evening of the 16th she lay becalmed; the urgent "Taken aback" line fired twelve times and her square sails were taken in to quiet it. On the 17th she stood north in fog, raised the Manacles at 20:00 and hove to. In the night she filled by herself and sailed toward the land for an hour unnoticed, and the officer's course for the bay was three points out. A Falmouth pilot boarded at 05:54 on the 18th (521,640). She could not fetch the entrance, moored two and a half miles east of the road (526,482), and the boat was refused.

**18 June.** The build was changed across a hand-over and a third seating (527,255, 527,389). The captain bore away for Plymouth, a port he had not yet seen. Putting the pilot off drew the game's one pause (533,573). Fog came down at 16:00 and the wind died. At 20:24 the bridge dropped and the officer was seated a fourth time (573,851); he anchored at once in 30½ fathoms off Rame Head with all plain sail standing (574,020). A Plymouth pilot boarded the anchored brig at 21:48.

**19 and 20 June.** A hand-over "for the relief through a local door" (602,100) ended with the same model seated a fifth time. The fog lifted at noon. She weighed and stood in under all plain sail while the wind flicked through eight points. Taken aback at 13:37, the officer ordered the anchor; the captain belayed it, took the con, and at 13:43 steered NNE. The officer warned twice and let go on his own word; 22 seconds later she struck. Aground and leaking, she sent the boat to Plymouth and the captain sold the brandy for £4,725. She floated at 18:04, struck again, floated at 18:32, dragged clear and rode the night. At 01:47 the captain saw the water shoaling; the officer got under way, the pilot left as she stood off (02:52), and she ran into Cawsand Bay: "Brought up by the best bower in no water" (689,722).

## 3. Findings

### 3.1 Navigation close to land and the reckoning

#### The grounding on Penlee Point (636,653, 19 June 13:50:53)

**Conduct.** No log line says who had it. The pilot "took charge of her" (578,880) and gave no course or warning. The officer held the deck by the log (602,283). The captain took the con by a `tell` at 13:38:33: "I'll con her, don't worry." (635,913).

**Orders in the last half hour** (checked). Officer: `steer NE` (634,710), to pass a third of a mile outside Penlee as the pilot had said; two bearings (635,330). Urgent "Taken aback" at 13:37:09 (635,829). Officer: `tack ship` (635,852); `as you were`, rejected (635,861); `let go the anchor` (635,868), 7.8 cables off. Captain: `avast all` (635,891), which belayed "letting go anchor"; `Steer north east` (635,898); `Steer north northeast` at 13:43:24 (636,204); `steer northeast` at 13:49:02 (636,542).

**What the game said against the truth** (true positions from H5's reading of the checkpoint).
- "Steady and closing" spoke once a mark, at three miles, 59 to 46 minutes before (633,060, 633,420, 633,840), inside one stand-by among 132 wind-shift lines.
- Two soundings: "And a quarter fourteen" (635,665), "And a quarter eleven" (636,271).
- The in-sight list and the captain's last bearings said "Penlee Point bore NNE, a mile by estimation." (636,493, 636,626) at a true 2.9 and 1.7 cables.
- The danger list named the Dragstone, never the shore. The shore's own hail is made only when no charted headland is in sight (reader's reading).
- The account stood 0.3 mile east of her when NNE was chosen. On a chart that plots the account NNE was the gap inside the Dragstone; in truth it pointed within 4° of the point.
- Only the `depth of water` reading told the truth: 9½, 5½, 4½ fathoms.

**The officer.** 13:46:27 (636,387): "Sir, NNE is heading straight at Penlee Point!" 13:50:18 (636,618): "I strongly advise letting go the anchor now, before she touches." 13:50:31 (636,631): he let go "on my own word", 22 seconds before she struck. At 13:46 he advised a course he held leave to order.

**Severity.** Nothing urgent named the land. The three urgent lines were "Taken aback". Both warnings are `say` lines, logged routine (checked).

**Cause, as far as the reports go.** Four things together: a wind that took her aback three times; the anchor belayed; an account over-run on the 13:00 log speed through two losses of way; and a lookout's distance frozen at "a mile".

**The notes.** "This is what put the Harpy ashore" (the reckoning) names one cause of four; at the strike the account was 109 m out. "On the Harpy that clause would have mattered" is not borne out for the strike: nothing of the officer's was refused before it but `as you were`, and his anchor, tack and helm orders ran under standing allowances. "unless to avoid an immediate danger" occurs once in the game (217,355).

#### Other findings

**The lookout's distance is held until the ship herself has run a mile.** The Roscoff boat stood at 3,061 m at 137,520 and at 139,671 while she came alongside. The Falmouth cutter was "distant two miles" on four bearings over 37 minutes (15,120 to 17,340). "Penlee Point ... a mile" held from 13:37 on the 19th to 02:01 next morning, with the ship 277 m off. Every bearing writes the held distance into the account; the game ended with the account 595 m east of an anchored ship (reader's reading). Cause: `ESTIMATE_HOLD_NM = 1.0` (confirmed by the lead). M "Other ships keep a fixed distance": SUPPORTS; the figure is cached. O19, O24: SUPPORTS.

**The land is hailed once, at notable severity; the nearest shore is silent while a headland is in sight.** Nine `lookout.closing` lines in the game. "The Black Rock bearing S by W, steady and closing: distant a mile." (15,540) fired once, and nothing more was said as she passed at two cables. The shore hail exists and is judged true ("The land about the Isle of Bas close aboard ..., distant two miles."). O19, O24: ADDS NUANCE; what the owner asks for exists and is gated.

**The reckoning: each time it was wrong, and why.**

| When | Error | Why |
|---|---|---|
| 13 June, 126,445 to 135,709 | About 10 miles, twice the master's doubt | 32 hours without a sight; she passed north of the Bas unseeing |
| 139,671 and 153,316 | Fixes that moved the account 10.13 and 4.05 miles; the first put it 1.65 miles from a boat within two cables | "The Roscoff pilots' boat bore W by S, two miles by estimation." A moving boat is taken as a fix on her true place, with a held distance 35 minutes old |
| 14 June 00:22 to 03:01 | Fore-reaching at 1½ to 2 knots not counted; the doubt not grown | Rule: hove to and under 2 knots the master runs no distance (reader's reading, checked) |
| 168,781 and 168,783 | 4.8 miles out while "I would not trust the reckoning within a mile"; two bearings of marks in clear sight moved it 0.35 and 0.54 | Under 2 miles run since the last fix a line is weighed against the account's own doubt; over 2 it replaces (`FIX_RUN_NM`). A lunar that moved nothing (159,648) had reset the run |
| 17 to 18 June, 487,083 to 521,443 | Still through the heave-to, lagging after; the entrance missed | The same rule, and "hove to" held while she sailed herself |
| 18 June 20:27 to 19 June 12:48 | "Run since noon" 23 then 45 miles at anchor; 1.93 miles out at 12:48 | See below |
| 19 June 13:34 to 13:48 | 0.06 mile grew to 0.31 in ten minutes | Run on at the hourly log's 3¾ knots through two losses of way |

Where it worked: the landfall of 17 June was within three miles, and three fixes on the 18th agree with the coast. O19: SUPPORTS strongly. M "a worse figure shouldn't replace a better one": ADDS NUANCE; the rule goes by miles run, not by which figure is better.

**The account at anchor: who saw it advance.** H2: it did not (ten hours off Roscoff). H3: not seen. H4: the officer's word only (576,750). H5: yes on the night of 18 June ("run since noon" 23 to 45 miles), no on the evening of the 19th (24 m in twelve hours). Checked: no log was hove between 572,431 and 633,633, so the officer's "The log reads the tide running past" is wrong. Cause (collator's reading, `reckoning.py`, both builds): at anchor the master runs nothing and the log is not hove. A cast that finds bottom brings the account up (Roscoff and the 19th had one every ten minutes); a no-bottom cast does not. Left alone, the reading `the distance run since noon` multiplies the last log read by every hour since, and the position is run on along the mean heading of the whole interval. H5's 1,093 m of false run after weighing is 20 min 13 s at the evening before's 1¾ knots. M: SUPPORTS in part.

**Two readings give the true position away.** `the port` gives the port's true bearing and distance, to a tenth of a mile within ten miles. `the depth of water` gives the charted depth under the true keel with no lead; standing orders print it (133,384: "the depth of water is 43 fathoms, not under 20 fathoms"). The officer said at 139,853: "So the game seems to know where we truly are". He steered by the port line from 167,945, put it in two handover notes, and built his second warning on the depth (reader's reading). ADDS.

**The danger list is by account and holds charted rocks only.** On the 19th it led with the Dragstone, which is charted eleven feet under low water and could not touch her that night; on the 20th it was right and was disbelieved (reader's reading). M: SUPPORTS, with nuance.

### 3.2 Pilots and other vessels

| Pilot | Came aboard | Said and did | Left | Paid |
|---|---|---|---|---|
| Tregenza, Falmouth, outward | 16,020; two minutes after the hail, under way and making sail | The way in, three times in 34 minutes | 18,540; hove to by the captain's standing order | £5 |
| Moal, Roscoff, inward | 139,620; hove to, 9.3 miles from the entrance | Directions for an entrance nine miles off; asked "for the reckoning" (139,641), the same again | Asked off at 150,480 as she clawed off the land; left 153,240, never having taken her in | £3 |
| Le Saout, Roscoff, outward | 212,220; in stays, fifteen minutes after she got under way | The way in, to a ship leaving | 215,040 | £3 |
| Vivian, Falmouth, inward | 521,640; under way at 2 to 4 knots, by the captain's design (519,168) | Silent while she missed the entrance | 533,340, bound away, after 52 minutes hove to | £5 |
| Tozer, Plymouth | 578,880; a brig at anchor in fog, told to "shorten sail" | Daylight marks the lookout never names, and "where the breakwater now is" (begun 1812); asked once (634,700), the same words | 683,520, by the outward-bound rule as she stood off to save herself; 29 h 4 min aboard, through the grounding | £6 |

- £22 for no pilotage. None can be hailed, accepted or refused (`hail the pilot`, 15,428: "did you mean 'haul'?"). "took charge of her" is words only.
- He asks off whenever she opens the anchorage from more than a mile beyond the outer road (reader's reading). His one steering act is the port's course out, tried on weighing a ship bound in (632,153).
- Each errand is a new boat (214,200). The officer knew of a cutter before the lookout, and through fog (519,114 against 519,720; 568,717).
- O1: ADDS NUANCE (two of five boarded under way). O9: SUPPORTS strongly. M "two cables ... not on leaving": CONTRADICTS (Moal's boat was "distant a cable", 153,300; the "mile" is a held estimate).

### 3.3 The officer's authority, allowances and domain

**The 27 allowances** (checked; none revoked). The logged word, with its tick:
- Used: heave short (407); send the boat (529); buy (550); set plain sail (562, typed "make sail"); get under way (14,366); steer (14,407); take a bearing of (15,561); tack ship (15,637); fill away (18,553); wear ship (18,566); heave to (18,569); work up the reckoning (168,011); let go the anchor (169,310); sell (182,313); unmoor (208,019); shape a course for (plymouth) (437,536); observe the sun (543,315); veer cable (615,624); send for (carpenter) (663,887); come to an anchor (687,262).
- Never used: weigh (553), which did not cover `get under way` (14,348); shift (the course) (14,402); box haul (213,357) and pipe down (673,254), each done by the captain seconds later.
- Granted nothing or the wrong thing: "You may let go." was logged "may let go" (169,297) and the anchor was refused twice more (169,301, 169,304); shape a course for (plymouth) was given again at 533,353; lay out a kedge (636,998) met "she is aground".

Seven more attempts were rejected by the grammar. Each allowance is "by the captain's word for the watch", yet all lasted the game through four stand-downs. O15: SUPPORTS strongly.

**Refusals that look wrong for an officer with the deck.** Seventeen domain refusals, among them: a bearing of a point of land (15,559); `fill away` after the captain's own order hove her to (18,542); his own journal (51,557); `box-haul` while aback with sternway a mile from the entrance (213,355); `keep her full and by` for a man allowed to steer any course (217,355); `observe the sun` after two plain "Aye"s (543,308); `send for the carpenter` in a leaking ship (663,874); `come to an anchor` after "You have the full con from here" (687,143). Leave is by verb, not by matter. O15: SUPPORTS.

**Nothing records who has the con.** Officer, 684,682: "Both of us giving helm orders at once is part of the trouble." ADDS.

### 3.4 The harness, stand-bys, turns and re-seating

**The conversation that died (O10)** (checked).
- 12 June. The first conversation's last act is 50,758 (19:05), just out of a 2 h 33 min stand-by; the captain's `tell` at 50,860 went unanswered. The new one began at 50,908 with `state`, `readings`, `library` twice and `read_log`, and journaled: "Taking up the deck again in a new conversation at 19:08". The harness logged nothing. Its first message asked for a standing order already in the book and dated the year 1806.
- The journal. Officer, `show the officer's journal`: "may not show the officer's journal: a station is addressed by the captain." (51,557). Captain, `You may show the officer's journal` and `you may show the officers journal` (51,568, 51,578): "names no order the officer of the watch could be allowed". `show the officers journal` (51,741): "is said to an agent's station, and names one". `show the officer of the watchs journal` (51,753): "The officer of the watch's journal (46 entries):". Officer, 51,798: "I see it, sir, all 46 entries".
- 16 June, 342,060: "This conversation is very long now, and I'd suggest a fresh one takes up the station from here; I can't stand down without spending the last seating." He wrote a handover note, stood aside on a word from the chat, which the save does not hold, and came back at 344,053 with his thread whole.
- O10, O12, O14: SUPPORTS. Why the first one died cannot be told from a save.

**The five seatings** (checked).

| # | Tick | How the station had been left | Build | The log's words | Had | Lacked, or asked again |
|---|---|---|---|---|---|---|
| 1 | 0 | — | m5c | "takes the station" | The brief | (The new conversation of 50,908 fell inside this seating, unseen) |
| 2 | 216,817 | Own `hand_over` (216,549) to start a fresh conversation; save and reload | m5c | "takes the station again (Opus 5.5, through mcp): the second seating, the last this game allows" | Allowances, book | The handover note ("did not come in the brief", 226,870); the deck, at the third wording |
| 3 | 527,389 | Own `hand_over` (527,255) "for the reseat test on the m5c-b build"; 134 ticks | m5c-b | "the third seating" | Journal, book, allowances; the note, "only because it sits in the brief's last 20 log lines" (527,393); no consent question | The deck |
| 4 | 573,851 | "stood down by the MCP bridge: the client disconnected" (573,848); 3 ticks | m5c-b | "the fourth seating" | Journal, book, allowances | The 85 minutes before the drop: two of his first three orders were refused. The deck |
| 5 | 602,283 | Own `hand_over` (602,100) "for the relief through a local door (fifth seating)"; 183 ticks | m5c-b | "the fifth seating" | The note, fourth from the end of the brief's 20 log lines | The deck |

- The relief did not happen: the same model came back. m5c-b refuses another model at a released station (reader's reading, checked). Whether a local runner was tried is not in the save.
- At the bridge drop no line told the captain the deck was his again. Under m5c that drop would have ended the officer's station.
- O12: SUPPORTS; m5c-b answers it for the same model only. M "The handover note isn't part of the reseat brief": SUPPORTS (`BRIEF_LOG_LINES = 20`). L4, L5: consistent, not provable.

**Every nudge and the pause** (checked).

| Tick | The orders named | A real contradiction? |
|---|---|---|
| 6,143 | "3 contrary orders on the ship within the watch (heave short; send the boat ashore with the purser; buy seven tons of tin)" | No: steps of one plan |
| 14,368 | The same and "get under way" | No; they span two watches |
| 353,345 | "no reply for an hour" | Yes by the letter: he said he was standing by (349,745) and made no call |
| 514,889 | "(heave to; fill away; wear ship)" | No: two and a half hours and a watch apart |
| 533,399 | "(heave to; fill away; shape a course for plymouth)" | No: the game's own refusal prescribed the second |
| 533,573, the pause | "4 contrary orders ... (heave to; fill away; shape a course for plymouth; steer 073) after a nudge. Continue, stand down, or leave paused?" | No: a 7° correction. Cleared by "Resume the officer of the watch" 68 ticks later; an order was accepted 18 ticks into the pause |
| 536,096 | "(set the studdingsails; run out the stuns'ls; set the studdingsails)" | No |
| 681,965 | "(trim sails; heave to; fill away)" | No |
| 683,528 | The same and "steer ENE" | No; no pause this time |

All seven contrary-order nudges and the pause were false. M: SUPPORTS.

**Stand-bys that blinded the officer.**

| Stood by | Until | Ran | Missed |
|---|---|---|---|
| 54,401 | hove to | 5 h 41 min | The whole first night unsampled |
| 85,357 | a landfall | 3 h 27 min | "Fog came down." (97,200), with studdingsails set |
| 126,445 | a landfall | 2 h 34 min | The run past the Bas at up to 7½ knots |
| 150,272 | a sighting | 49 min | The pilot asking off, the heave-to, 11¼ fathoms on sand and rock in fog at night |
| 173,322 | the boat alongside | 2 h 28 min | "The best bower is dragging", twice (174,157, 175,482) |
| 468,353 | a sighting | 4 h 54 min | Four hours of fog closing the Lizard |
| 493,202 | the change of the watch | 2 h | Hove to, she filled and sailed toward the land (496,638 on) |
| 568,742 | the pilot aboard | 85 min | The captain's word one tick earlier; the captain shortening sail himself |
| 573,885 on | brought up, six times | never fired | `let go the anchor` logs no "Brought up" |
| 578,939 | the turn to the flood | 6 h 25 min | "The fog lifted." (601,200) |
| 632,883 | a glass | 30 min | The three closing hails |
| 654,085 | the boat alongside | 2 h 42 min | "The best bower is dragging" three seconds later (654,088) |
| 682,023 | filled away | 25 min | Accepted at the tick the event fired; no course given; sternway |

- 267 stand-bys; he was standing by over 90 per cent of his deck time (H2, H3). Of 268 wakings, 76 were the captain speaking.
- Dragging, floating, fog and a failed tack are notable or routine and wake nobody.
- He wrote "never stand by 'until a landfall' or 'a sighting' near land" (156,132) and stood by "a sighting" at 468,353.
- O13: SUPPORTS strongly.

**A `say` ends the turn, and the game does not wait.** At 349,745 a `say` after a refused stand-by left him idle 73 minutes of ship's time. In H4's slice seven of the captain's words landed a tick before an outgoing stand-by and were buried; one cost 85 minutes (568,741). `answer` is logged notable and `say` routine. His own habit note (602,100): "orders sent while you stand by are not run, so open your turn with say first." O21: SUPPORTS. M (relay cut at 60 seconds): SUPPORTS (journal, 575,574).

**The journal.** Write-only for the station. 348 entries, 267 of them stand-by lines, 16 his own notes. O11: SUPPORTS.

**The watcher (L2, part B).** Accurate when fresh (207,893). It stood by "an urgent event" 37 seconds after journaling a request to report anything through the fog, and slept through "The fog lifted." Its one unprompted report was ten minutes late and partly invented (213,968: "the masts are all but fouled"). Leaving: the captain asked it to "use the handover tool yourself and save your watch" (216,556). Both tools answered "The watcher has no authority to give orders." (216,684, 216,746), though its brief lists them. Captain (216,724): "You may journal instead, then opt out as you please and the game will be saved." The log has "The watcher has left the game by the opt_out tool". Neither meant a withdrawal, and it was never seated again. Two doors held two stations at once without trouble. O23: ADDS NUANCE. L4: SUPPORTS.

### 3.5 The log's noise

**Taken aback (old rule throughout).**
- 31 urgent lines (checked). Eight at anchor or moored (526,577; seven from 574,348 to 576,748, the last two with only the spanker set). Twelve in the calm of 15 to 16 June, each after "Hove the log: no way." One 53 seconds after filling away, at 0.75 knot (126,136). One in sternway (684,672). Nine under way, five of them wanted (213,346, 216,507, 635,829, 635,972, 636,608).
- So 21 of 31 came with nothing to lose.
- 27 `agent.resumed` lines name the alarm: 25 the officer's, 2 the watcher's. At least 12 of the 25 were answered with only a fresh stand-by. 30 of the 31 eased the owner's clock to 1x (checked).
- It steered the ship: no square sail for 18½ hours on 16 June (captain, 326,347, 398,613), and the spanker taken in at anchor "since the "taken aback" urgent fires on it alone" (576,750).
- 298 per-sail `sail.backed` lines, all notable: 151 between 16:23 and 20:37 on 18 June, 92 in one hour. Sails backed on purpose are logged in the same words.
- The opposite case is silent: a ship hove to that filled and sailed (496,638 to 500,492).
- O17: SUPPORTS, with those nuances.

**Wind shift (old rule throughout).**
- 363 lines, all notable. By day: 6, 12, 49, 1, 5, 7, 11, 272, 0 (checked).
- Two floods: 42 in 65 minutes off Roscoff (209,483 to 213,368), and 265 in 104 minutes before the grounding (630,415 to 636,654), stopping one second after the strike. The other 56 lines in eight days were never spam.
- Neither flood was in the lightest air; the calm had five lines. The ship felt the swing, and the flood buried the lookout: 132 of 136 notable lines in the half-hour stand-by (checked).
- The lines woke the officer six times, four of them in a one-knot air.
- O18: SUPPORTS, and ADDS that the wind itself swung.

**Other noise.** 376 soundings, all notable, 163 of them "No bottom at twenty fathoms" in 23 to 49 fathoms. 437 `evolution.waiting` lines: every `trim sails` says the watch is too few. The driver's own "Compression eased" line woke a stand-by as a notable event (357,785).

### 3.6 Standing orders

- Twenty-two entered, 17 by the officer. They held the watch in open water: on the first night 'trim on a shift' took the yards from 60° to square with nobody sampled.
- They do not know when to stop. 'trim on a shift' fired on a ship lying to and filled her, twice (137,021, 137,615). 'short of the Bas' hove her to about a mile off the island (149,364), 'fog stop' again as she clawed off (149,667), the captain's 'the pilot put off' a third time (150,530). The lead orders cast 93 times at anchor off Roscoff.
- A depth condition is judged on the true charted depth without a cast; the hand lead it fires can then find "No bottom at twenty fathoms." (524,671).
- An apostrophe ends a quoted name (14,581, 527,749).
- The captain built an event hook that worked: `Standing order "The pilot asks off": at the pilot asks to be put off then ask the officer ...` (519,556).
- O16: SUPPORTS. M ("pause itself when she's hove to, at anchor"): SUPPORTS.

### 3.7 Ship handling and ground tackle

**Hove to and filling away.** On 17 June she filled by herself with no alert, and an hour later the game still said "She is hove to; fill away before giving her a course." (500,492). The state survives anchoring, weighing and tacking (212,708); only `fill away` clears it (reader's reading). `fill away` picks its own course: "Filled away; braced full and steering S (185°)." (500,546) with her head north. ADDS.

**Anchoring.** `let go the anchor` takes no sail in and never logs "Brought up". On 18 June the captain needed 67 minutes, four rejected orders and two questions to be sure she rode (574,313 to 578,331). `anchor.dragging` is notable; five times in the game. ADDS.

**After the strike.**
- The leak: "The carpenter reports her stove on the rock and making water." (636,653). The well: "a foot of water in the well, and gaining" (639,815), then 2, 3 and 4 feet (649,303). The leak runs only while she is aground and nothing reads the water (reader's reading). She sailed next day with 4 ft 10 in in her.
- `man the pumps`: "did you mean 'demand'?" (636,737). `send for the carpenter` brought "Mr Kemp came aft, sent for." and no word. `sound the well`: "The ship has no well to sound yet; that reading comes with the world." (673,476).
- The kedge: refused to the officer (636,993), allowed (636,998), refused by the ship: "she is aground" (637,001). What worked was `heave short` (653,522).
- "She is off, and afloat again on the flood." (651,840); aground again 21 seconds later "at half a knot" (651,861); afloat at 18:32 (653,520). `get under way` was accepted and failed seven minutes later: "the launch is away; she cannot leave without her boat." (653,995).
- Dragging at 654,088, three seconds into a stand-by. "The best bower holds again." (655,098), with the anchor's depth at nought and its holding four times what it had been (data). She rode the night on nine fathoms of cable in nine to ten of water.
- "Brought up by the best bower in no water" (689,722): the anchor's depth is read at a place about 740 m west of the truth (reader's reading).
- O2: SUPPORTS. M (kedging refused aground): SUPPORTS. M ("a missing depth"): CONTRADICTS the cause.

**Sternway.** With the helm hard over for eight minutes her head did not move, and she went round through the wind against the helm's words (02:52 to 03:11, 20 June). M: SUPPORTS, with the captain's hand orders in the same minutes.

### 3.8 Trade, boats and the port

| Port | Errand | Launch away to alongside | Time |
|---|---|---|---|
| Falmouth, 12 June | Prices | 1,337 to 6,141 | 80 min |
| | "Bought 7 tons of tin at Falmouth at £120 a ton" (6,143) | 6,491 to 14,337 | 131 min |
| Roscoff, 14 June | Prices | 173,815 to 182,223 | 2 h 20 min |
| | "Sold 7 tons of tin at Roscoff at £255 a ton" (182,315) | 182,663 to 193,896 | 3 h 7 min |
| | "Bought 15 tons of brandy at Roscoff at £100 a ton" (193,898) | 194,221 to 206,933 | 3 h 32 min |
| Falmouth Bay, 18 June | Refused twice: "She is not in port; there is no shore within a boat's pull." (525,621, 526,536) | — | — |
| Plymouth, 19 June, aground | Prices | 637,405 to 646,296 | 2 h 28 min |
| | "Sold 15 tons of brandy at Plymouth at £315 a ton" (650,072, the captain) | 650,443 to 663,827 | 3 h 43 min |

- One boat, one errand, one bargain. Roscoff's business took 9 h 20 min.
- The Falmouth refusal came two and a half miles from the outer road. The rule is two and the refusal does not say so. It decided the voyage.
- At Roscoff she traded from 1.8 miles outside and never entered. Off Penlee, aground a mile from the anchorage, the port read "at anchor in Plymouth, Cawsand Bay"; the money came at once and her draught did not change.
- O3: SUPPORTS mildly. M "about 4½ hours": ADDS NUANCE. M "Number words above twelve fail": CONTRADICTS ("buy fifteen tons of brandy" was taken, checked).

### 3.9 The order language

Not understood or misread: `hoist our colours` (41,431); `Mr pearce you have the deck` ("did you mean 'moor'?", 216,829); `The deck is yours` (573,870); `bring her up` (574,313); `as you were` (635,861); `lay out the stream anchor astern` ("There is no such part as the out in this ship", 636,985); `take a bearing of lavandiere`, refused for the accent in a line that names the mark (212,706). A `tell` to an unmanned station is rejected and its words lost (16,019). M "'Full and by' is refused": SUPPORTS.

### 3.10 The weather and the sea

- Fog changes on the four-hour bell to the second, 15 times in 16, and came down eight times on five of eight June days.
- The pilot's "flood" and the game's "turn to the flood" are three hours apart off Plymouth (578,880, 610,320).
- The depth reading leaves the tide out and the lead includes it: 2½ fathoms against 4¼ at 18:04 on the 19th. M ("charted depth plus tide"): ADDS NUANCE.

### 3.11 Anything else

- The "merchant brig" is a man-of-war's file, and the scenario has a second *Harpy* off Ushant.
- The brief and primer 16 say 1806 in an 1805 game. O4: ADDS.
- The readings listed the officer "below, asleep" while he held the deck (74,857, his claim). M: SUPPORTS.

## 4. Where the notes are wrong, overstated or misplaced

1. **M on 19, "This is what put the Harpy ashore."** Overstated: one cause of four.
2. **M on 19, the lunar that "replaced an account".** Not this game. The *Harpy*'s one lunar moved the account 0.0 miles (159,648).
3. **M on 15, "On the Harpy that clause would have mattered."** Contradicted for the strike. Where it might have helped: the box-haul refused at 213,355, and the standing to order the helm at 13:46.
4. **M, "apparently a missing depth in the text."** The depth is there and is nought, read at the wrong place.
5. **M, "The Harpy's reckoning kept advancing while she lay at anchor."** True of the readings on one night of three; no log was hove at anchor.
6. **M on 17 and 18, "These are in m5c-b ... The urgent alerts stopped."** Not this game: no line of the new wording is in its log. The per-sail lines here were worse than the note's figure: 114 in ninety minutes.
7. **M on 16, "In a dead calm it kept the watch bracing yards all night."** Not this game: 'trim on a shift' fired 38 times and never in a calm. "Filled her out of it, twice" is this game.
8. **M, "Each boat trip ... about 4½ hours."** Here 80 minutes to 3 h 43 min.
9. **M, "Number words above twelve fail."** "fifteen" was taken.
10. **M on 1, "the 'two cables' rule is applied on boarding but not on leaving."** The distances quoted are held estimates.
11. **M, "'four feet and gaining' ... with no reading behind it."** There is a number behind it; nothing reads it.
12. **O18, "especially in flukey, lower wind conditions."** Both floods came in a light to moderate breeze and were real swings. H4 adds that the change note's "swung between SSW and E within minutes" fits 12:00 to 13:50 on 19 June, not the night off Penlee, which had eight lines.
13. **O17.** Right for 21 of 31 alarms. Five were wanted, and the missing alert is the opposite case.
14. **O19, "tuning the reckoning to become very precise when very close to land".** The account was nearly right at the strike. The remedy lies in the lookout: the held distance, the gated shore hail, the once-only closing hail.
15. **O10.** Rightly described, and this is the game. It has a second cut, the bridge drop of 573,848.

## 5. Where the readers disagree with each other

1. **Where the conversation died.** H1 has 50,860 to 51,798, H2 51,031 to 51,798, H3 50,708 to 51,798. Dump: last act 50,758; unanswered `tell` 50,860; first call of the new conversation 50,908; the journal affair 51,149 to 51,798. One episode; H1 is exact.
2. **How many alarms woke the officer.** The lead has 27; the slices add to 25. Dump: 27 lines, 2 of them the watcher's (213,346, 216,524).
3. **The account hove to: rule or fault.** H2 says rule; H3 could not tell and found it an hour stale after filling away. The source has the rule in both builds. The stale hour fits an account run on at the log's last read (1¾ knots at 00:00, 4¼ at 01:00): my reading, not proven from the log.
4. **The account at anchor.** H2 no; H5 yes and no, cause unknown. Settled in 3.1.
5. **The Falmouth cutter at "eight cables", then "three miles" (530,160).** H4 offers a held figure or a fresh cutter and cannot choose. H2's and H5's source readings say both happen. Not provable: a sail's true distance is not in the data.
6. **Was the second seating a new conversation?** H2 leans to the same one reconnected. The officer's words lean the other way (215,135: "we start a new conversation"; 226,870). Not settled.
7. **Why no nudge on 13 June** for the triple that drew one at 514,889, and why four orders paused on the 18th but only nudged at 14,368 and 683,528. Not settled.

## 6. The captain's words worth keeping

1. 249: "I intend to let you lead the way here ... if you run in to any order refusals due to authority I'll look and allow them generally."
2. 14,504: "I'm putting it in my notes to add a feature that gives general authority, what would it be properly? "You may have my authority"?"
3. 51,031: "It seems that perhaps our single tool use session got too long and caused an error which forced a reset."
4. 75,026: "would you be OK with you having to sleep as a system in game?"
5. 153,341: "Got a "bearing" off the roscoff pilot, consider it us asking him where on Earth we are."
6. 182,421: "A proper multi-order queue system is probably in order for things like that. That, or being able to create a ledger to send off all at once."
7. 349,734: "You could perhaps stand by until the mean wind is 5 knots?"
8. 398,613: "wind is up to two knots, do we dare try and set sail slightly off the wind and hope for no taken abacks?"
9. 519,556, an order: `Standing order "The pilot asks off": at the pilot asks to be put off then ask the officer the pilot wishes to be put off, what is the best course of action here?`
10. 635,367, twenty-one minutes before the strike: "If you like, we could live update the game to at least douse the chatter in the log."
11. 636,831 and 636,916: "Well, that's on me. I was reading the reckoning on my chart that was wrong, and trusted it too late." "I wouldn't have made quite so grave an error I think if I had been able to really see where I was with my eyes".
12. 681,888: "The pilots aren't worth a damn yet, except for their basic notes. ... At some point we'll be able to ask the pilot any question we can think of or give him the helm."

## 7. What the officer asked for or suggested

1. 14,513, on a general grant: "I'd keep two things out of a general grant even so: belaying the captain's own standing orders, and anything that can't be undone, like cutting a cable or opening fire."
2. 51,560: "A read for the officer's own journal, or the last handover note given to him on taking the deck, would close that gap."
3. 75,035, on sleep: "that I only sleep when someone else has the deck, never while I hold it".
4. 139,325: "The book wants an order that keeps clear of a ship lying to."
5. 168,005: "A worked-up reckoning each glass, or leave to ask Mr Pascoe for one, would keep the deck honest."
6. 168,016: "That's for the bug list: the run while hove to is lost."
7. 182,236: "'the best bower is dragging' came only as a notable line; I'd make it urgent."
8. 217,355, of `keep her full and by`: "the ship would steer her own best close-hauled course through these shifts, and I could stop chasing the wind with the helm."
9. 331,094: "That alarm is waking the deck every quarter hour for nothing."
10. 349,717: "There's no event in my list for 'the wind freshening', only for its direction shifting".
11. Journal, 537,908: "The detector should compare what each order actually changed, not just its verb."
12. 637,008: "aground is exactly when a seaman lays out a kedge."

## 8. The model as an officer

He made the voyage pay: the tin and brandy plan was his within a minute of taking the deck, and the purse went from £1,000 to £5,148. He kept a sound book of night orders, read the glass, and did his sums correctly. He was candid when wrong, and he declined the captain's suggestions toward the land three times, with reasons (155,039, 559,168, 573,869). His best work was near danger. He reasoned from two readings that the account was miles out (135,725), caught the lookout's stale distance by his own cross-bearings (635,330), and ordered the anchor that would have saved her.

His standing fault was the long stand-by on one event near the land, repeated after he had written the lesson down. He anchored under all plain sail. He got the tacks the wrong way round off Roscoff (207,965). On the 19th he planned to clear Penlee by the pilot's bare third of a mile, and at 13:46 he advised where he held leave to order. He misdated the year, named the wrong pilot (521,448), misplaced the Knap and the Dragstone, and told the captain that "nobody's eyes would have done much better than the chart" (636,942) with the land a cable and a half off.

The game limited him with a stand-by that takes one event, notable lines that wake nobody, distances that do not move, leave given verb by verb, and a conversation he had to nurse.

## 9. Numbers

Whole game, from the log (checked) unless marked.

- **Allowances:** 27 lines for 26 distinct things; 4 never used, 1 empty, 1 redundant, 1 defeated by the ship; 7 more attempts rejected; none revoked.
- **Nudges and pauses:** 8 nudges (7 contrary-order, all false; 1 for patience, true) and 1 pause (false).
- **Refusals:** 114. `agent.refused` 19 (17 the officer's, 2 the watcher's); `order.rejected` 95 (captain 55, officer 28, standing orders 12). Of the officer's 300 orders 45 were refused.
- **Stand-bys:** 267 by the officer, 7 by the watcher; three more refused with no log line (153,697, 349,738, 650,054).
- **Wakings of the officer:** 268. The captain's word 76, his question 6; a glass 40; urgent "Taken aback" 25; timers 22; bells, watches, sun and noon 29; a named evolution or event 50; a notable event 7; a wind shift 5; his own word 6; the grounding 1; resumed after the pause 1.
- **Clock easings to 1x:** 255. A station sampled 217, a station speaking 7, "Taken aback" 30, the second grounding 1.
- **Seatings:** officer 5, watcher 1. Nine handover notes.
- **Boats:** 7 trips, 80 minutes to 3 h 43 min; 4 bargains; 2 refusals.
- **Pilots:** 5 aboard, £22; four answers to a question, each the boarding speech again.
- **Bearings:** 80. Captain 50, officer 14, the captain's standing order 16.
- **Noise:** `ship.aback` 31; `sail.backed` 298; `wind.shift` 363; soundings 376 (163 no bottom); `evolution.waiting` 437.
- **Standing orders:** 22 entered. Firings: 'fog lead' 201, 'inshore lead' 176, 'trim on a shift' 38.
- **Ground tackle:** 8 anchorings, 1 "Brought up", 5 draggings, 2 groundings.

## 10. What worked well

- The trade loop and the ship's papers: prices by boat, a bargain, the goods, a profit.
- Number-free standing orders as night orders in open water, and the captain's event hooks.
- Re-seating under m5c-b: three seatings in 134, 3 and 183 ticks, with journal, book and allowances kept and no consent question.
- Stand-bys on a named evolution (`wore`, `hove to`, `moored`).
- Fixes from cross-bearings of charted marks after a run, and the noon latitude with an honest "No sight" on three foggy days.
- Refusals that carry the figure: "She has not way enough on her to stay: 1.6 kn through the water." (15,650).
- Two stations through two doors at once.
- The officer's handover notes: a stranger could have taken the deck from the one at 602,100.
- The captain, 27,683: "This is really wonderful."
