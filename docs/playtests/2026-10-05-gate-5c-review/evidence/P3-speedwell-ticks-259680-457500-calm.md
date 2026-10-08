# P3 · *Speedwell*, ticks 259680 to 457500: two days of calm and light airs

Reader's report for the gate m5c review. Session `4-schooner-plymouth-opus`, the third of five slices.

**How to read this.** Ticks are written without separators so they can be searched in the dumps. Tick 0 is 21 June 1805 05:00:00 and a tick is one second, so 25 June 00:00 is tick 327600 and 26 June 00:00 is tick 414000. Every count is from `4-schooner-plymouth-opus.log-full.txt`, ticks 259680 to 457500 inclusive. "Log:" marks what the log shows. "Officer said" and "Captain said" mark claims. A save keeps no tool results, so what the officer read in `readings`, `state` and `read_log` is known only from what it said next. Where I read code to explain a behaviour, it is the m5c-b copy, read only, with file and line given.

## 1. Slice identity

| | |
|---|---|
| Session | `4-schooner-plymouth-opus` |
| Ticks | 259680 to 457500 |
| Ship's time | 24 June 1805 05:08 to 26 June 12:05 (55 hours) |
| Ship | Merchant topsail schooner *Speedwell*, American colours, scenario "A merchant schooner, free", seed 7. In the hold: 40 tons of coal, 20 of pilchards, 16 of brandy. Bound from Roscoff to St Mary's, Scilly |
| Officer | The mate, "Mr Ray", held by Opus 5.5 through the MCP door. The transcript header says calls are held "for up to 50 seconds", so the bridge ran with `--wait 50` |
| Captain | The owner, at the game's window |
| Build | m5c-b (the save is under `FreeSail-gate-m5c-b/saves`) |
| Size of the slice | 1,967 log lines, 481 notable, 0 urgent. 147 transcript entries: 31 orders, 41 spoken lines, 48 `stand_by` calls, 16 door events, 3 `answer`, 1 `hand_over`, 3 `readings`, 2 `read_log`, 2 `state`. No `journal`, `library` or `handover_note` call |

## 2. What happened

| Tick | Ship's time | Event |
|---|---|---|
| 259680 | 24 Jun 05:08 | Log: "Mr Moal left her in the boat, clear of the western entrance of the channel of Bas". The officer fills away (259682), orders "keep her full and by" (259872) and only then resumes his standing order 'trim' (259873) |
| 261229–261247 | 05:33 | The captain takes five bearings by hand (the Lavandière, Bas, Roscoff, its church, Pergueridre) |
| 261291–261302 | 05:34 | The captain asks the officer to try `shape a course for st mary's`. It is refused for the officer, the captain allows it, and the log has "Shaped a course for St Mary's: NW by account, 112 miles; the line passes the Gilstone within a mile. Helm ordered: steer NW by W (309°)." |
| 261384–261444 | 05:36 | A toast to the Harpy from the officers' cask |
| 263352 | 06:09 | The officer belays 'approach lead' after seven "No bottom at twenty fathoms" |
| 270000 | 08:00 | Log: "The land is out of sight." 'trim' fires at 270475 |
| 284520 | 12:02 | Log: "Noon. Latitude by observation 48° 52' N; the reckoning was 48° 56' N. Course made good since yesterday WNW, 20 miles. Longitude by account 4° 23' W." |
| 298800–299202 | 16:00 | The captain asks which port the officer would choose; a conversation about Funchal and the East Indies. The wind is falling: mean 5 knots in the morning, 3 at 16:00, 2 at 18:00. The log reads 3 knots at noon and 1¼ at 18:00 |
| 313207 | 20:00 | Officer said: "flat calm: one knot of air, no way on, her canvas slatting". He stands by until sunrise (313212) with 'trim' still in force |
| 319676 | 21:47 | Log: the first "Her sails aback; she had no way on to lose." The log reads "no way" from 22:00. Overnight there are 19 such lines, 32 per-sail lines, 4 wind-shift lines and 7 firings of 'trim'. Nothing wakes the officer |
| 341875–341940 | 25 Jun 03:57 | Sunrise wakes him. He belays 'trim'. Captain said: "I'm eager to make Scilly, we'll work to it if the wind at least picks up." |
| 343351–343555 | 04:22–04:25 | Hand-over at the captain's request, second seating 18 seconds later. The deck is given and taken back as a test, the officer is "stood down by the captain", and the third seating follows 41 seconds later |
| 343812 | 04:30 | The officer stands by "until the deck given". The captain keeps the deck for 15 hours 20 minutes, to 398710 |
| 344363–392668 | 04:39–18:04 | Dead calm. Mean wind 1 knot. The log reads "no way" at nine heaves running (22:00 to 14:00). 71 more ship-aback lines and 191 more per-sail lines |
| 359391–366127 | 08:49–10:42 | The captain tries the ship himself. "Wear ship" is refused ("She has no way on her to wear: 0.5 kn through the water"), "Fill away" is refused ("She is not hove to"), he braces, trims and orders "Steer north" |
| 371100 | 12:05 | Log: "Noon. Latitude by observation 49° 04' N; the reckoning was 49° 00' N. Course made good since yesterday NW, 12 miles. Longitude by account 4° 38' W." |
| 397131–398567 | 19:18–19:42 | A 2-knot air from NW by W. The captain lets fly, trims, orders "Keep her full and by", sets the fore topgallant and swifters in the catharpins |
| 398710 | 19:45 | Log: "Mr Ray, you have the deck." The officer has lost his thread: `readings`, `read_log`, then "No, sir, I didn't get one this seating" (398809). The captain types `show the journal of the officer` (398818). The officer resumes 'trim' (398889) |
| 399616–399925 | 20:00 | Fore yards braced sharp up. The catharpins, he reports, gain nothing |
| 406839–406875 | 22:00 | `come up half a point` is refused, `steer 340` is accepted, and the captain gives six allowances in 24 seconds |
| 414752–415360 | 26 Jun 00:12 | He wears to the starboard tack, on the captain's word that wearing is better than tacking in 3 knots. At 415818 he finds "full and by" has let her fall off and steers 268 by compass |
| 420281, 424818 | 01:44, 03:00 | He comes up to 280 and 287 as the wind veers. The harness nudges him for "3 contrary orders on the helm" |
| 437305, 441540 | 06:28, 07:39 | Headed. He bears away to 255 and then 235 to keep her moving |
| 441628–441645 | 07:40 | The captain asks for a weather forecast and gets one from the glass |
| 443449–444230 | 08:10 | He wears back to the larboard tack and steers 328 |
| 448216–453133 | 09:30–10:52 | The wind backs W, WSW, SW. He steers 318, shapes a course twice (the log says it is "too near the wind to be laid"), then steers 309 by hand |
| 457500 | 12:05 | Log: "Noon. No sight; the sun was hid at noon in drizzle. Latitude by account 49° 13' N. Course made good since yesterday NW, 22 miles. Longitude by account 4° 54' W." About 70 miles remain |

In 40 hours, from 20:00 on the 24th to noon on the 26th, the distance to St Mary's by account fell from 85 miles to about 70.

## 3. The deck and the captain's words

### When the deck was given and taken

| Tick | Ship's time | Log words |
|---|---|---|
| 109 (before the slice) | 21 Jun 05:01 | "Mr Ray, you have the deck." The officer then held it without a break for 95 hours |
| 343363 | 25 Jun 04:22 | "The officer of the watch hands over the deck; the captain has it." |
| 343503 | 04:25 | "Mr Ray, you have the deck. The officer of the watch has the deck; the captain's standing orders are his night orders." |
| 343510 | 04:25 | "The captain has the deck. The officer of the watch is stood down." (seven seconds later, as a test) |
| 398710 | 19:45 | "Mr Ray, you have the deck." He holds it to the end of the slice |

### Allowances given in the slice

| Tick | The captain typed | Log | Used? |
|---|---|---|---|
| 261299 | `you may shape a course for st mary's` | "The officer of the watch may shape a course for (st mary's), by the captain's word for the watch." | Yes: 261302, 448993, 451328 |
| 406851 | `you may come up half a point` | "…may come up (half a point)…" | No |
| 406853 | `you may come up a point` | "…may come up (a point)…" | No |
| 406857 | `you may come up two points` | "…may come up (two points)…" | No |
| 406867 | `you may bear off half a point` | "…may bear away (half a point)…" | No |
| 406869 | `you may bear off a point` | "…may bear away (a point)…" | No |
| 406875 | `you may bear off two points` | "…may bear away (two points)…" | No |

The six come-up and bear-off allowances took the captain 24 seconds and seven typed lines (one, `you come up`, was a slip). The officer never used any of them, in this slice or later: the only `come up` he ever submitted is the refused one at 406842. He used `steer NNN` every time. Whether a bare `you may come up` would have covered every amount was not tried.

Allowances from the first day carried through both stand-downs. `wear ship` (allowed on 21 June) was accepted at 414752 and 443449. `steer` (tick 63), `fill away` (tick 96) and `keep her full and by` (43102) were all accepted after the re-seatings.

### The captain's telling lines

- 261291 (24 Jun 05:34, a question): "I can't draw on my map, but would you like to use "shape a course for st mary's" and see what it recommends based on our reckoning to "chart" the course?"
- 299199 (16:06): "A ten thousand foot peak is just the thing when you feel you can't make out the land right in front of you."
- 343351 (25 Jun 04:22): "Mr Ray, please perform a handover so your station is ready and the status logged. Then you may retake the station."
- 343464 (04:24): "For now, since I think we can only hand off the deck once per session (definitely a gap to fix, free hand offs that basically put you with watcher authority seem better than app restarts), I'll hold the deck until the wind picks up and we can start working towards Scilly. Then I'll pass the deck. Reasonable?"
- 343496 (04:24): "Ah, in fact, we'll try it now. Stand by."
- 398804 (19:46, a question): "Did you receive the handover from the last watch? If not, I can show it in the log here."
- 398881 (19:48): "The journal is in the log for your review. … You have the deck, I am here as well of course. Ask me any questions as you please."
- 399971 (20:06): "I had hoped we'd gain a bit on the fore topsail, but fair enough."
- 403651 (21:07): "Ah, by my log the speed and leeway are the same between either of the points. The squares shaking don't seem to be hurting her, at least from what I see."
- 414750 (26 Jun 00:12): "In 3 knots, we may be better off wearing."
- 427207 (03:40): "The whole contrary thing will probably go, or be very strongly adjusted. It assumes a very low standard, really."
- 441609 then 441628 (07:40): `Ask the watcher …` is refused ("There is no watcher at the station"), then `Ask the officer Based on your expert sailorly knowledge of the weather, are we looking at more calm, or maybe something blowing in? What would tell you?`
- 444304 (08:25): "*cough* As the captain, I definitely already knew that and was simply testing your knowledge."

### What the captain did by hand

- **Bearings.** Five at 261229–261247. The officer's journal notes that bearings need the captain's word. He did not ask for it here.
- **The journal.** `show the journal of the officer` at 398818, because the officer has no tool that reads it (section 5.2).
- **Trimming during the officer's watch.** After 398710 the captain typed nine trim orders while the officer had the deck: "Trim sails" at 400078, 400556, 403357, 407482, 411301 and 416118, and "Trim (the) fore and aft sails" at 421223, 431903 and 439749. Six of them follow a helm order the officer had just given and not trimmed to (section 7).
- **Two helm orders of his own** in the first half hour of the officer's watch: "Steer 350" (400002) and "Come up half a point" (403247).
- **The clock.** Officer said at 313207: "You may want to put some speed on the clock, sir. It'll be a long night of nothing at this rate."

## 4. Orders refused

Eleven in the slice: 2 `agent.refused` and 9 `order.rejected`. Classes: (a) vocabulary or grammar gap, (b) domain refusal as designed, (c) domain refusal that looks wrong for an officer with the deck in 1805, (d) correct ship-state refusal, (e) apparent bug.

| Tick, time | By | Order as typed | Refusal's words | Class | What came next |
|---|---|---|---|---|---|
| 261294, 24 Jun 05:34 | Officer | `shape a course for st mary's` | "The officer of the watch may not shape a course for st mary's without the captain: the reckoning, the sights and the course shaped are the master's for the captain." | (b). The captain had asked him to do it three seconds before | Captain: `you may shape a course for st mary's` (261299). Accepted at 261302 |
| 327484, 24 Jun 23:58 | Standing order 'trim' | `trim sails` | "Standing order 'trim': order not carried out ('trim sails'): There is no wind to trim to." | (d) | The same order was carried out six other times that night in the same 1-knot air (section 6.2) |
| 359391, 25 Jun 08:49 | Captain | `Wear ship` | "She has no way on her to wear: 0.5 kn through the water." | (d) | `Brace sharp up on the starboard tack` accepted |
| 359701, 08:55 | Captain | `Fill away` | "She is not hove to." | (d), with a touch of (a): the captain wanted her sails filled, and the phrase is known only as the way out of heaving to | `Trim sails` accepted |
| 397440, 19:24 | Captain | `Let fly the headsail sheets` | "There is no such part as the headsail sheets in this ship; did you mean the mainsail sheet, the foresail sheet or the headsails? ('let go' was understood.)" | (a) | Three orders in its place: `Let fly the jib sheets`, `Let fly the staysail sheets`, `let fly the flying jib sheets` |
| 399616, 20:00 | Officer | `brace the fore yards up sharp` | "'brace' was understood, but not 'sharp'; did you mean 'trim sails head yards sharper'? (…a modifier such as 'sharp up'…)" | (a). The captain's own phrase at 398946 was "brace up sharp" | `brace the fore yards sharp up` accepted one second later |
| 403361, 21:02 | Captain | `Haul in the weather bowlines` | "The larboard fore topsail bowline is hauled out already." | (d) | None needed |
| 406842, 22:00 | Officer | `come up half a point` | "The officer of the watch may not come up half a point without the captain: the course is the captain's, never to be changed without his directions unless to avoid an immediate danger." | (c). The captain had just invited it (406839), and `steer` had been allowed since the first day | `steer 340` accepted one second later (406843) |
| 406846, 22:00 | Captain | `you come up` | "'you come up' is not an order this ship understands; did you mean 'you may' or 'you have the deck'?" | A slip. The reply's guess was right | `you may come up half a point` |
| 417401, 26 Jun 00:56 | Captain | `haul in the weather bowlines` | "The starboard fore topsail bowline is hauled out already." | (d) | None needed |
| 441609, 07:40 | Captain | `Ask the watcher Based on your expert sailorly knowledge…` | "There is no watcher at the station; nobody has been stationed there." | A slip, (d) | `Ask the officer …` 19 seconds later |

Two things stand out. The domain check works by verb, not by effect: `steer 340` and `come up half a point` do the same thing, and one passes while the other is refused. Over the voyage the captain allowed the helm ten separate times under five verbs (steer, keep her full, shape a course, come up, bear away). And the refusal texts are clear in every case; the three grammar ones name what was understood and offer the near form.

## 5. Harness behaviour

### 5.1 The three seatings (343363 to 343555, 25 June 04:22 to 04:25)

| Tick | Log words |
|---|---|
| 343351 | "The captain to the officer of the watch: Mr Ray, please perform a handover so your station is ready and the status logged. Then you may retake the station." |
| 343363 | "Handover note, handing over the deck: Deck to the captain, 25 June 1805, Morning watch 04:22. …" |
| 343363 | "The officer of the watch stood down by the officer of the watch: the deck handed over. The game is saved." |
| 343381 | "The officer of the watch takes the station again (Opus 5.5, through mcp): the second seating; it had stood down by the officer of the watch: the deck handed over." |
| 343510 | "The officer of the watch stood down by the captain: the captain has the deck. The game is saved." |
| 343551 | "The officer of the watch takes the station again (Opus 5.5, through mcp): the third seating; it had stood down by the captain: the captain has the deck." |

The journal's own entries read "Seated again, the second seating; I had stood down by the officer of the watch: the deck handed over." and "Seated again, the third seating; I had stood down by the captain: the captain has the deck."

**The officer's first calls each time.**

- Second seating (343381): a spoken line at the same tick, "Mr Ray back aboard, sir: the second seating, and my handover note is right there in the log for me." Then `stand_by` until "the deck given" (343428). No read of the journal or the log, and none needed: the note had been logged 18 seconds earlier and was the fourth line from the end of the log.
- Third seating (343551): a spoken line at 343555, "Mr Ray aboard again, sir, the third seating, with the log of the deck going back and forth all plain to read." Then `stand_by` until "the deck given" (343812).

**What the captain was testing.** First, hand-over and return (343351). Then, on the officer's suggestion, whether the deck could pass back and forth without a stand-down. Officer said at 343473: "By my brief, "I have the deck" only takes the deck back. The station stays seated, and the officer goes on standing by and advising. It's my hand_over that releases the station and needs the app restart to come back. So you may be able to pass the deck back and forth freely". The test at 343503–343510 showed otherwise: "I have the deck" stood the station down. That is what primer 16 says ("`I have the deck` takes it back, and the station is stood down with its journal saved"), but the station brief only says the officer holds the deck "until he takes it back ('I have the deck') or you hand it over", so the officer's reading of his brief was a fair one.

**What m5c-b showed.** The re-seating rule works. Both returns happened 18 and 41 seconds after the stand-down, by all signs inside the same chat, with no restart and, as far as the transcript shows, no consent question. Allowances, standing orders and their belayed state all carried over: 'trim', belayed at 341879, was still belayed when he resumed it at 398889. The captain still believed at 343464 that "we can only hand off the deck once per session"; the third seating answered that.

**"My first hand_over came back 'Nothing was run'".** Not in this slice. The one `hand_over` here (343363) ran at once, because the captain's word at 343351 had opened a turn. The incident is in session `2-harpy-brig-opus` at tick 527255: a door event `by=its own word door=speak` ("Mr Pearce on deck. … handing over the deck for the reseat test."), then `hand_over` at the same tick. The code explains the words. While the game has the floor the harness takes only reads, `shelve`, a journal note, and a lone `stand_by` from a model not already standing by; any other call gets "Nothing was run." (`freesail/agents/remote.py` lines 117–123 and 633–643). A `hand_over` sent during a stand-by is such a call.

### 5.2 A fourth arrival that the log does not show (398711, 25 June 19:45)

Log: no seating, stand-down or door event between 343551 and 398710. The station stood by "until the deck given" for 54,899 seconds of ship's time.

What the officer did when the deck came back:

| Tick | Call or words |
|---|---|
| 398773 | `readings({})`, 62 ticks after the deck was given. His usual answer to a waking comes within 2 ticks |
| 398781 | "I have the deck, sir. Wind NW by W, a light air of two knots, with St Mary's dead to windward of us at about 309°." |
| 398804 | Captain: "Did you receive the handover from the last watch? If not, I can show it in the log here." |
| 398806 | `read_log({"severity": "notable", "since_tick": 0})` |
| 398809 | "No, sir, I didn't get one this seating. The log gives me the noon sight (49°04'N), the yards braced and the fore topgallant set about 19:30, the swifters belayed, and a long calm with the headsails flapping aback all afternoon, but no handover note. I'd be glad to see it if you'll show it in the log." |
| 398818 | Captain: `show the journal of the officer`. Log: "The officer of the watch's journal (200 entries):" |
| 398893 | "Thank you, sir, I've read the journal and my old handover. One thing has changed since I wrote it: the glass, which was falling a hundredth an hour, is rising now" |

The model that wrote the handover note at 343363 and read it back at 343381 did not know of it at 398809, and spoke of "this seating". Something on the owner's side had replaced the conversation: a restart, a new chat or a compaction. The save cannot say which. The code shows why the log is silent. A door that asks for a station the same model already holds is attached, not re-seated: "The same model asks for a station it holds (a door restarted): the door reads … the station's brief sent again" (`remote.py` lines 478–488). By that code the only trace is a line on the server's console; nothing goes to the ship's log or the journal.

Why the officer could not recover alone:

- **The brief carries no journal and no handover note.** It is built from the last 20 lines of the log, the readings, the standing-order book, the allowances and the deck's state (`harness.py` lines 582–624; `BRIEF_LOG_LINES = 20`, `agent.py` line 96). At 398711 the last 20 lines were the captain's trimming and the catharpins.
- **`read_log` returns only the newest 200 matching lines.** `READ_LOG_LIMIT = 200` (`tools.py` line 102), applied as `events[-READ_LOG_LIMIT:]` (line 280). There is no upper bound to ask for, so nothing older than the newest 200 can be reached at any severity.
- **The calm's aback lines filled those 200.** 293 notable lines followed the handover note before the officer's read, 262 of them `sail.backed` or `ship.aback`, so the note was the 294th from the end. The newest 200 reached back only to 10:15 on the 25th (364544), and 184 of those 200 were aback lines. His account matches: the oldest thing he names is the noon sight.
- **No tool reads the journal.** `journal` only appends (`tools.py` lines 555–560).

The captain's dump was 200 entries and about 21,000 characters. 151 entries were "Stood by until …", 12 were ended stand-bys, 22 were allowances and deck changes, 6 were nudges, 2 were stand-downs and 2 were seatings. Four were the officer's own notes and one was the handover.

### 5.3 Door events

The session has 71. Sixteen fall in the slice: 14 are `by=out of turn door=stand_by`, and 2 are `by=mcp door=reseat reason=Opus 5.5`. None is `by=its own word door=speak` (13 before the slice, 3 after) and none is a library read.

| Tick | by | door | reason | Ticks since the entry before, and what that was |
|---|---|---|---|---|
| 259734 | out of turn | stand_by | filled away | 50, a spoken line |
| 261359 | out of turn | stand_by | a glass | 50, a spoken line |
| 261439 | out of turn | stand_by | a glass | 50, a spoken line |
| 284579 | out of turn | stand_by | the change of the watch | 50, a spoken line |
| 298942 | out of turn | stand_by | the change of the watch | 50, a spoken line |
| 299196 | out of turn | stand_by | the change of the watch | 49, a spoken line |
| 343381 | mcp | reseat | Opus 5.5 | 18, the `hand_over` |
| 343428 | out of turn | stand_by | the deck given | 47, a spoken line |
| 343551 | mcp | reseat | Opus 5.5 | 45, a spoken line |
| 398944 | out of turn | stand_by | a glass | 51, a spoken line |
| 403631 | out of turn | stand_by | a glass | 50, a spoken line |
| 416077 | out of turn | stand_by | ten minutes | 256, a spoken line |
| 441593 | out of turn | stand_by | a glass | 50, a spoken line |
| 444282 | out of turn | stand_by | a glass | 50, a spoken line |
| 449348 | out of turn | stand_by | a glass | 50, a spoken line |
| 449526 | out of turn | stand_by | a glass | 157, a spoken line |

What they are. The out-of-turn stand-bys are not the officer's spoken lines and not relay cuts. Each is a `stand_by` sent while the game had the floor and the officer was not yet standing by. Eleven of the 14 come 49 to 51 ticks after a spoken line: `say` hands the floor back, the call is held 50 seconds, it returns with no turn opened, and the officer then asks to stand by. The harness takes such a call at once (`remote.py` lines 645–665). So each spoken line that is not followed by a captain's word costs one more call, and the 50-tick spacing confirms that the fifty-second hold was in force and that the game was at 1x at those moments. No cut-off call shows in the slice.

One limit on this evidence: reads made out of turn are answered and not recorded (`remote.py` lines 38–43), so the transcript's 3 `readings`, 2 `read_log` and 2 `state` are only those made in turn. By the same code a `stand_by` that merely continues a wait is not recorded either, so the transcript cannot show how many calls a long stand-by took.

### 5.4 Stand-bys

62 `agent.stood_by` lines, none refused.

| `until` | Count | Longest sleeps (seconds) |
|---|---|---|
| a glass | 36 | 1800 each |
| the change of the watch | 8 | 14221, 7197, 6798, 6648 |
| 5 minutes | 5 | 300 |
| ten minutes | 3 | 600 |
| noon | 2 | 14508, 2511 |
| a wind shift | 2 | 42, 7 (both cut short by the captain) |
| the deck given | 2 | 54899, 37 |
| sunrise | 1 | 28663 |
| filled away, wore, a message | 1 each | 136, 436, 70 |

The two long ones are the calm. From 313212 (24 Jun 20:00) to sunrise at 341875 he slept 7.96 hours with the deck. From 343812 (25 Jun 04:30) to 398711 (19:45) he waited 15.25 hours without it.

**What woke the station: 63 `agent.resumed` lines.**

| Reason | Count |
|---|---|
| A glass | 26 |
| A word from the captain | 21 |
| The change of the watch | 4 |
| Ten minutes have passed | 3 |
| A question from the captain | 2 |
| Noon | 2 |
| 5 minutes have passed | 2 |
| Filled away, Sunrise, Wore | 1 each |

No waking came from a `ship.aback`, `sail.backed` or `wind.shift` line, and no urgent line fired at all. The game eased to 1x 55 times in the slice, each time because the officer was sampled or spoke, never for a weather line.

**Were the wakings worth it?** Of the 26 glass wakings, 11 led to an order, 2 to a spoken report and 13 to nothing but another stand-by. That is a fair return for the second night, when he was steering by compass in a shifting 2- to 3-knot air and no event names "the wind has headed her" or "she has lost her way". Three of the 21 captain's-word wakings were allowance lines (406854, 406858, 406868). They broke the 5-minute stand-by he had just set three times in 15 seconds.

**What an officer can do in a calm.** Very little, and nothing was refused because nothing was tried. No order for sweeps, a boat to tow, a kedge or the anchor was submitted by the officer or the captain. The gate document puts towing and working the kedge in M8. The officer could have taken in the slatting canvas (in his domain) and did not. He could have ordered `heave the log` when the breeze died and made (also in his domain) and did not; section 6.3 shows what that cost the reckoning. His promise at 341940, "I'll wake when the breeze comes", had only "a wind shift" behind it, which is an event about the wind's direction and not its strength. No event names a breeze making or the ship gathering way. He replaced that stand-by two minutes later in any case.

### 5.5 The nudge

One, at 424818 (26 Jun 03:00): "The officer of the watch nudged: 3 contrary orders on the helm within the watch (steer 268; steer 280; steer 287)." It was wrong. The three orders were 74 and 76 minutes apart and all the same way, coming up as the wind veered. Officer said at 427161: "Those were all the same way, coming up as the wind lifted, so it might count only orders that reverse each other." The captain's answer is quoted in section 3. No pause followed. In the forenoon the same pattern (steer 328, 318, then 309, with two `shape a course` between) drew no nudge.

### 5.6 The handover note

Written at 343363 through `hand_over`. Salient parts:

- "Speedwell becalmed at sea about 49° 00' N, 4° 38' W by account (uncertain 5 miles east-west), 51 fathoms."
- "Glass 30.04 and falling slowly, a hundredth an hour for a day: I expect the westerly back, perhaps with some weight."
- "Bound for St Mary's, Scilly, about 85 miles north-west by west (shaped course 309°; the direct line passes within a mile of the Gilstone, so haul north of the Western Rocks on the approach). Captain's word: make Scilly, working to windward if need be."
- "My standing orders: 'trim' (at a wind shift, trim sails) is belayed for the calm; resume it once there's a working breeze, and belay it before any heave-to. The lead orders … are all belayed"
- "Purse £31."

I checked it against the log and found it accurate: the purse (£34 after the brandy, less £3 pilotage at 259680), the 36 tons of room, the sails aback, the fore topgallant furled, the state of each standing order. Its one forecast did not come true that day; the glass turned and rose from the evening.

On the next two seatings the note did its work only because it was 18 seconds old. On the arrival at 398711 it did nothing until the captain intervened. When the officer did read it he followed it: he resumed 'trim' "now there's a breeze" (398889, 398893) and belayed it before each wear.

### 5.7 Tools, silences and turns that ended oddly

- **Reads.** All seven recorded reads come after 398711. In the 23 hours before the hand-over he made none in turn and relied on the samples.
- **Journal.** He wrote no note in the slice. The journal gained 78 entries, all by the harness: 62 "Stood by until …", 10 allowances and deck changes, 2 stood down, 2 seated, 1 nudge, 1 handover. When his thread was lost, the newest note of his own was from 23 June 19:24.
- **`answer` keeps the turn open and `say` closes it.** After each of the three answers (261298, 398809, 441645) a further call ran within a tick or two. After a spoken line the next call was usually the out-of-turn stand-by 50 ticks later.
- **Speaking before acting.** At 414715 he said "I mean to go about now", which closed his turn. The captain's reply 35 seconds later reopened it and he wore at 414752. Elsewhere he acts first and speaks second.
- **A nine-minute silence.** Sampled at 426619 (26 Jun 03:30), he said nothing until 427161. The driver line at 427162, "Compression eased to 1x: the officer of the watch speaks", shows the clock had been run up meanwhile. This was the turn after the nudge. The cause cannot be told from the save.
- **Stated one thing, did another.** At 427209 he said "I'll stand by for the change of the watch", had no stand-by in force for 18 minutes, and at the sunrise sample (428296) stood by "until a glass".
- **The long waits.** With fifty-second calls, the 15-hour stand-by was a long run of tool calls with nothing in the chat. That is the likely setting for the lost conversation, and it matches the owner's note 10.

## 6. Ship, sea, navigation and port observations

### 6.1 The m5c-b log changes in a calm, measured

**`ship.aback`.** 90 lines, all notable, all the same words: "Her sails aback; she had no way on to lose." None is urgent. None reads "Taken aback: …", "…in the light air; she has lost what way she had" or "…as she lies at anchor / aground". The first is at 319676 (24 Jun 21:47) and the last at 391566 (25 Jun 17:46). The whole voyage has 92 lines with these words, so 90 of them are here.

- Spacing: median 9.7 minutes, mean 13.5, shortest 3.0 (181 s), longest 92. Twelve of the 89 gaps are under 5 minutes and 49 are under 10.
- Densest hour: 11 lines, 06:26 to 07:26 on the 25th (350777–354361). Densest four hours: 29 lines, 12:40 to 16:28.

**`sail.backed`.** 228 lines, all notable. 223 are in the calm, from 320129 (24 Jun 21:55) to 392668 (25 Jun 18:04). The other 5 are the fore-and-aft sails going over in the wear at 443790. By sail: fore topsail 66, fore staysail 45, fore sail 40, jib 38, flying jib 38, main sail 1.

- Densest hour: 39 lines, 13:19 to 14:17 on the 25th (375568–379055). With the ship lines, 46 notable lines in the hour.
- Densest 90 minutes: 53 lines, 15:46 to 17:14 (384401–389654). With the ship lines, 62.
- A sail stayed aback for a median of 7½ to 11 minutes, but 48 of the 223 episodes lasted under a minute. Between 376232 and 376675 (7 minutes) the log has 14 per-sail lines and 2 ship lines; the fore staysail is taken aback at 376232, fills at 376248 and is aback again at 376300.

**`sail.filled`.** 230 routine lines ("Fore topsail filled again."), one for each aback line.

**`wind.shift`.** 9 lines in 55 hours.

| Tick | Ship's time | Words | Mean wind near it |
|---|---|---|---|
| 325204 | 24 Jun 23:20 | "Wind backed to N by E, light airs." | 1 knot |
| 331975 | 25 Jun 01:12 | "Wind backed to N by W, calm." | 1 knot |
| 336000 | 02:20 | "Wind backed to NW by N, calm." | 1 knot |
| 341475 | 03:51 | "Wind backed to NW by W, light airs." | 1 knot |
| 419007 | 26 Jun 01:23 | "Wind veered to NW by N, light airs." | 3 knots |
| 440364 | 07:19 | "Wind backed to NW by W, light airs." | 2 knots |
| 446805 | 09:06 | "Wind backed to W, light airs." | 2 knots |
| 450561 | 10:09 | "Wind backed to WSW, light airs." | 2 knots |
| 454459 | 11:14 | "Wind backed to SW, light airs." | 2 to 3 knots |

Each is a real step of two points or more in a slow turn of the wind: eight points of backing across the first night's four lines (the log had last put the wind at NE by N, on the 23rd), a two-point veer, then nine points of backing on the 26th. There is no chatter. There is also no shift line at all between 03:51 on the 25th and 01:23 on the 26th, 21½ hours in which the log has 72 ship-aback lines.

**By period.**

| Period | Mean wind | Log | `ship.aback` | `sail.backed` | `wind.shift` | 'trim' fired | Officer woken |
|---|---|---|---|---|---|---|---|
| 24 Jun 05:08–20:00 | 5 falling to 2 | 2¼ to 3 knots, 1¼ at 18:00 | 0 | 0 | 0 | 3 | 14 |
| Night 1, 20:00–04:00 | 2, then 1 from 22:48 | ¼, then "no way" | 19 | 32 | 4 | 7 (1 refused) | 3: the watch at 20:00, sunrise, the captain. None by the weather |
| 25 Jun 04:00–08:00 | 1 | "no way" | 25 | 36 | 0 | belayed | 3, all the captain |
| 25 Jun 08:00–12:00 | 1 | "no way" | 11 | 28 | 0 | belayed | 0 |
| 25 Jun 12:00–16:00 | 1 | "no way" | 26 | 64 | 0 | belayed | 0 |
| 25 Jun 16:00–20:00 | 1, 2 from 19:00 | ¼ | 9 | 63 | 0 | belayed | 3, all the captain |
| Night 2, 20:00–04:00 | 1 to 3 | ¾ to 1½ | 0 | 0 | 1 | 2 | 20: 12 glasses, 5 captain, 3 timed |
| 26 Jun 04:00–12:05 | 2 to 3 | ¾ to 2¼ | 0 | 5 (a wear) | 4 | 10 | 20 |
| Whole slice | | | 90 | 228 | 9 | 22 | 63 |

**Hour by hour through the calm.** `weather.hour` gives the sky, the glass and the sea but not the wind ("Clear, fine; the glass 30.10; a smooth sea, easy."). The wind column is the mean named in the routine `wind.gust` lines ("A gust: 2 knots, the mean 1.").

| Hour from | Sky; glass | Mean wind, knots | Log | `ship.aback` | `sail.backed` | `wind.shift` | 'trim' |
|---|---|---|---|---|---|---|---|
| 24 Jun 20:00 | Clear; 30.12 | 2 | ¼ knot | 0 | 0 | | |
| 21:00 | Clear; 30.12 | 2 | | 1 | 5 | | |
| 22:00 | Clear; 30.10 | 1 | no way | 5 | 2 | | 1 |
| 23:00 | Clear; 30.10 | 1 | | 3 | 3 | N by E, light airs | 1 (refused) |
| 25 Jun 00:00 | Clear; 30.09 | 1 | no way | 3 | 3 | | |
| 01:00 | Clear; 30.08 | 1 | | 4 | 8 | N by W, calm | 2 |
| 02:00 | Clear; 30.07 | 1 | no way | 0 | 5 | NW by N, calm | 1 |
| 03:00 | Clear; 30.06 | 1 | | 3 | 6 | NW by W, light airs | 2 |
| 04:00 | Hazy; 30.05 | 1 | no way | 3 | 7 | | |
| 05:00 | Detached clouds; 30.04 | 1 | | 6 | 24 | | |
| 06:00 | Detached clouds; 30.04 | 1 | no way | 8 | 5 | | |
| 07:00 | Detached clouds; 30.04 | 1 | | 8 | 0 | | |
| 08:00 | Detached clouds; 30.04 | 1 | no way | 1 | 6 | | |
| 09:00 | Detached clouds; 30.04 | 1 | | 4 | 4 | | |
| 10:00 | Detached clouds; 30.04 | 1 | no way | 4 | 8 | | |
| 11:00 | Detached clouds; 30.04 | 1 | | 2 | 10 | | |
| 12:00 | Detached clouds; 30.05 | 1 | no way | 3 | 1 | | |
| 13:00 | Detached clouds; 30.04 | 1 | | 7 | 33 | | |
| 14:00 | Detached clouds; 30.04 | 1 | no way | 8 | 15 | | |
| 15:00 | Detached clouds; 30.04 | 1 | | 8 | 15 | | |
| 16:00 | Clear; 30.04 | 1 | ¼ knot | 5 | 31 | | |
| 17:00 | Clear; 30.04 | 1 | | 4 | 27 | | |
| 18:00 | Clear; 30.04 | 1 | ¼ knot | 0 | 5 | | |
| 19:00 | Clear; 30.05 | 2 | | 0 | 0 | | |

**What the numbers say.**

- The urgency fix held completely. Under m5c's rule these episodes would have been urgent "Taken aback" lines, each one waking the officer and easing the clock.
- The calm still wrote 318 notable aback lines, 66% of the slice's 481 notable lines. In the calm proper (319676–392668) they are 313 of 358, or 87%.
- 85 of the 90 came while the gust lines named a mean wind of 1 knot. The first five came between 21:47 and 22:47 on the 24th, as the mean fell from 2 to 1. The log read "no way" or ¼ knot throughout. In the second night, with 2 to 3 knots of wind and ¾ to 1½ knots of way, there were none. A floor of about two knots, or re-arming only after she has had way on, would have left at most those first five.
- The per-sail lines have no re-arm at all and are the larger part: 228 against 90.
- The lines had a second cost. They are what put the handover note beyond `read_log` (section 5.2).

### 6.2 "Keep her trimmed": the standing order 'trim'

**The text.** Given by the officer at tick 83157 (22 June 04:05), at the captain's request: `standing order "trim" by the mate: at a wind shift then trim sails`. It fired 41 times in the voyage, 22 of them in this slice.

**Every firing in the slice.**

| Period | Ticks and times | Count |
|---|---|---|
| 24 Jun, by day | 270475 (08:07), 305628 (17:53), 311604 (19:33) | 3 |
| Night 1, in the calm | 323714 (22:55), 327484 (23:58, refused: "There is no wind to trim to."), 331634 (01:07), 333374 (01:36), 335657 (02:14), 339571 (03:19), 341001 (03:43) | 7 |
| 25 Jun, by day | Belayed by the officer at 341879 (03:57), resumed at 398889 (19:48) | 0 |
| Night 2 | 406527 (21:55), 407600 (22:13) | 2 |
| 26 Jun, morning and forenoon | 434071 (05:34), 435819 (06:03), 437199 (06:26), 442467 (07:54), 446838 (09:07), 448991 (09:43), 450544 (10:09), 452227 (10:37), 454391 (11:13), 456563 (11:49) | 10 |

**The bracing in the calm.** Six carried out between 22:55 and 03:43, each a notable "By standing order 'trim': trimming sails." and a notable `yard.braced` line. The wind's angle to the ship in the six `sail.trimmed` lines was "143° on the larboard quarter", "93° on the larboard beam", "60° on the larboard bow", "36° on the starboard bow", "115° on the larboard quarter" and "19° on the larboard bow". The yards went to 0° from square, 37°, 58° to 60°, 58° to 60°, 15°, and 58° to 60°. Each firing also wrote "Bracing the yards: not hands enough for all at once; the watch takes the sails in turn." Officer said at 341882: "My "trim" order kept the hands bracing the yards to every breath, to no purpose, so I've belayed it until there's a wind worth trimming to."

**Counts for the slice.** 21 `order.accepted` and 1 `order.rejected` by 'trim'. 21 of the 42 `yard.braced` lines follow it (18 follow the captain's orders, 3 the officer's). Within two minutes of the 21 firings the log has 248 lines, 56 of them notable.

**The firings were not chatter.** The event "a wind shift" for a standing order or a stand-by is one point of the ten-minute mean from where it stood (`freesail/api/readings.py` lines 2105–2115). The log's line needs two points (`core/world.py` lines 208–212). The order fired about once for each point the wind went round: seven times for about eight points in the first night, ten times for about ten on the 26th. So the order did what its words say. It has no sense of when trimming is pointless.

**One refusal shows the game already knows.** At 327484 the firing was refused with "There is no wind to trim to." Six other firings that night went ahead in the same 1-knot air.

**The two hove-to incidents are before this slice.**

| Tick | Ship's time | What happened |
|---|---|---|
| 162102 | 23 Jun 02:01 | She had lain hove to since 147971. 'trim' fired: "Braced two yards to the wind, 41° on the starboard bow". The fore topgallant, fore staysail and fore topsail "filled again" (162129–162139). The captain belayed 'trim' (162559) and backed the fore yards. The officer, asleep until sunrise, broke his stand-by at 162663: "my "trim" standing order fired on a wind shift at two o'clock while she lay hove to". Then: "That's my oversight. A trim order should never have stood while she lay to." |
| 193303 | 23 Jun 10:41 | Hove to since 192632 for the pilot. 'trim' fired and the same three sails filled (193332–193342). The captain belayed it (193417) and backed the yards by hand. Officer said at 193441: "My fault again, sir: I said I'd belay "trim" before lying to and didn't, and it has just filled her out of the heave-to." His own `heave to` was refused: "She is hove to already; fill away before heaving to again." So the ship still counted herself hove to with her topsails full. He added at 193449: "I'd ask the builder for "trim" to stand aside by itself while she lies to." |

In this slice the lesson held. He resumed 'trim' only after she had filled away (259873), belayed it before each wear (414752, 443449) and resumed it after (415362, 444230). That is seven belay and resume orders in 55 hours to mind one standing order (belayed at 341879, 414752 and 443449; resumed at 259873, 398889, 415362 and 444230).

### 6.3 The reckoning through the calm

**The noon lines.**

| Tick | Line | Observed against account |
|---|---|---|
| 284520 | "Latitude by observation 48° 52' N; the reckoning was 48° 56' N. Course made good since yesterday WNW, 20 miles. Longitude by account 4° 23' W." | 4' south |
| 371100 | "Latitude by observation 49° 04' N; the reckoning was 49° 00' N. Course made good since yesterday NW, 12 miles. Longitude by account 4° 38' W." | 4' north |
| 457500 | "No sight; the sun was hid at noon in drizzle. Latitude by account 49° 13' N. Course made good since yesterday NW, 22 miles. Longitude by account 4° 54' W." | no sight |

**The account as the officer reported it.**

| Tick | Ship's time | Officer said |
|---|---|---|
| 298808 | 24 Jun 16:00 | "By account we're at 48° 59' N, 4° 35' W" and "Ten miles since noon" |
| 313207 | 20:00:07 | "By account we're at 49° 02' N, 4° 40' W" |
| 341882 | 25 Jun 03:57 | "She has drifted about the same patch of sea all night, near 49° 00' N, 4° 38' W by account." |
| 399925 | 20:05 | "Since noon she has made good only four miles to the south-east, so the tide has been setting us more than she has sailed." |
| 403581 | 21:06 | "Since noon she has made good five miles eastward, so the set is still beating her sailing." |
| 411085 | 23:11 | "By account we're at 49°08'N, eight miles made since noon." |

**The log heaves** come every two hours: 3 knots at 12:00 on the 24th, 2½ at 14:00, 2¼ at 16:00, 1¼ at 18:00, ¼ at 20:00, then "no way" nine times from 22:00 to 14:00 on the 25th, ¼ at 16:00 and 18:00, and 1¼ at 20:00.

**The account did not drift while she had no way on.** It stood at 49° 00' N, 4° 38' W from the 20:00 heave on the 24th to the noon sight on the 25th, 16 hours. That is right for an account kept by log and compass, and it is unlike the Harpy's at anchor. The noon sight then moved the latitude 4 miles north. That is the set of 24 hours, or part set and part the sight's own error, and the account knew nothing of it. No `master.place` line gives a position; the two in the slice (286320, 372900) read "Mr Travers came on deck, the day's work done."

**But the account steps at the heaves, and the steps are large in a failing or making wind.** This is my inference from the officer's figures and the log reads; it fits them closely.

- Between heaves the readings carry the account forward at the last read, as primer 10 says. At a heave the interval just past is worked again at the new read.
- 24 June: "Ten miles since noon" at 16:00:08 is 5 miles for 12:00–14:00 worked at 2½ knots, plus 5 projected at 2½. The position at 20:00:07 fits 14½ miles from noon. After the 20:00 heave at ¼ knot the same interval is worth ½ mile, and the account falls back 2 miles to 49° 00' N, 4° 38' W. The officer's reports at 20:00 and at sunrise are 2' of latitude and 2' of longitude apart, and he spoke of her having "drifted about the same patch of sea".
- 25 June: summed the same way the reads give 12½ miles from noon to noon; the line says 12.
- 25 June, evening: by 20:00 the reads give 0 + ½ + ½ + 2½ = 3½ miles since noon, 4.9 by 21:06 and 8.3 by 23:11. The officer read "four miles", "five miles" and "eight miles". Of that, 2½ miles are the 20:00 heave of 1¼ knots credited to the whole of 18:00–20:00. She had had steerage way only since about 19:30.
- So the "four miles to the south-east" is the account's own run, and the account cannot know the tide. The officer's "the tide has been setting us" has nothing under it.

A two-hour heave is coarse for airs like these. The officer may order `heave the log` and did not.

### 6.4 "Full and by", and the shaped course

**"Too near the wind to be laid" when it was not.** Log at 451328 (26 Jun 10:22): "Shaped a course for St Mary's: NW by W by account, 73 miles; the line passes the Gilstone within a mile; NW by W (309°) lying too near the wind to be laid, she is kept full and by on the larboard tack." Thirteen minutes earlier the log had "Wind backed to WSW, light airs." (450561). With the wind at WSW the course is 61° from it. At 453133 the officer ordered `steer 309`; the log has "Steady on NW by W (309°)" at 453208 and 2¼ knots at noon. Officer said at 453136: "A note for the book: when a course is shaped and the wind frees, the shaped course should take over from full and by. Here it said "too near the wind to be laid" with the wind 62° off the course." The same words at 448993 (09:43) were fair: the wind was then about W by S and the course about 50° from it.

A likely cause, which I could not confirm: the test for whether a course can be laid uses a wider angle than the one at which "full and by" holds this schooner. On her first settling, with almost no way on, the log has "Steady, full and by, the wind 52° on the larboard bow." (398047).

**"Full and by" cost height for no speed.** The officer at 403581 wanted to fall off half a point because "At 45° on the bow the square sails shake". The captain's reply, quoted in section 3, was that his log showed the same speed and leeway at either point.

**"Full and by" let her fall off after the wear.** Officer said at 415821: ""Full and by" let her fall right off to SW (228°). With the true wind NW, that's nearly on the beam." He gave it up for compass courses and from then on adjusted the course by hand at the glass: 268, 280, 287, 255, 235, 328, 318, 309. The log can show only "Wore ship; … heading WSW (248°)" (415360) and "Steady, full and by, the wind 47° on the starboard bow." (415668). His 228° and his explanation cannot be checked.

### 6.5 Other things that look odd or unfinished

1. **Speed in light airs looks high.** At 10:00 on the 26th the log reads "two knots" with gust lines "A gust: 2 knots, the mean 2." at 09:31 and 09:52. At noon it reads "two knots and a quarter" with "the mean 3" at 11:33. At noon on the 24th it reads "three knots" with the mean at 4. A loaded schooner making the speed of the wind in a 2-knot air is fast. The log over-reads a few per cent by design, and the "mean" in a gust line is rounded.
2. **Swiftering the catharpins where it can gain nothing.** The captain's `Swifter in the catharpins` (398427) set a party to work on both masts, the main included, which has no yards. He belayed it and ordered the fore mast only (398567). Twenty minutes later: "Swiftered in the catharpins on the fore mast; she has no yard on the lower mast there to brace the sharper." (399737). Easing them took another 19 minutes and ended with the same clause (413872). The game knew the answer before the hands were sent.
3. **Bearings that disagree.** At 261235 "Roscoff bore SE by E, three miles by estimation." and at 261241 "The church of Roscoff bore SE by E, five miles by estimation." The town and its church lie on one bearing, two miles apart.
4. **A notable line for nothing done.** 18 of the 21 `yard.braced` lines after 'trim' read "Braced two yards to the wind; 58° to 60° from square." From 21:56 on the 25th to 11:49 on the 26th that is twelve times running with the yards where they were.
5. **"Not hands enough" as a notable line.** "Bracing the yards: not hands enough for all at once; the watch takes the sails in turn." is notable 23 times (25 with two variants). It is the ordinary state of a schooner's watch at every trim.
6. **Gust lines that are not gusts.** 125 `wind.gust` lines; in 66 the gust equals the mean, and 35 read "A gust: 1 knots, the mean 1."
7. **A shift in a calm.** "Wind backed to N by W, calm." (331975, 336000).
8. **"Taken aback" in a wear.** At 443790 the fore sail, main sail, fore staysail, jib and flying jib are each "taken aback", notable, as they go over.
9. **Words.** "0.5 kn through the water" in a refusal; "the jib flogging" in a 2-knot air (397445); "stood down by the officer of the watch" where the officer is also the subject (343363); a doubled stop when the captain's words end in one ("…retake the station..", 343351; "…in the log here.?", 398804).
10. **`weather.hour` has no wind.** In 55 hours it named the sky, the glass and the sea 55 times and the wind never.
11. **No strange sail.** No `lookout.sighting` in 55 hours near the mouth of the Channel. The scenario has twelve other ships.
12. **All hands to wear a schooner in a 3-knot air.** "All hands! (to wear ship)" at 414753 and 443450. The wears took 10 and 13 minutes.

What worked without remark: the pilot's leaving and the standing order that reports it; the Gilstone warning in `shape a course`; a slow and coherent turn of wind and glass that an officer could reason from; "No sight; the sun was hid at noon in drizzle."

Nothing to report on ports, the market, the boats, groundings or near misses: after the pilot left at 259680 she was in open, deep water throughout (the handover gives 51 fathoms).

## 7. The model as an officer

**Good calls.**

- He filled away the moment the pilot left and put 'trim' back only when she was full (259682–259873).
- He belayed the ten-minute lead an hour offshore (263352).
- His own figure for the course matched the master's before he saw it: "three hundred and eight degrees, some 112 miles" (261298) against "112 miles … steer NW by W (309°)" (261302).
- He planned around the Gilstone warning and around a night landfall (261309, 284529).
- Each watch got a plain report with the account, the glass's trend and the distance to run. Those I could check against the log are right.
- His tack was the right one each time (398781, 414715, 443451). He took the captain's word to wear and not tack in 3 knots without argument.
- When his thread was lost he said so at once, read what he was shown, and corrected his own old forecast from the glass (398893).
- He reported the two faults he met in the game's own terms: the wrong nudge (427161) and "The two should be judged alike." (406846).
- He corrected himself unprompted: "Madeira's peak is about six thousand feet, not ten. I made the mountain grow in the telling, which is a sailor's privilege but not a mate's." (299147).

**Mistakes and gaps.**

- **He left 'trim' in force through a night he had called "flat calm".** It fired seven times before he belayed it at sunrise.
- **He told the captain, from his brief, that "I have the deck" would leave him seated** (343473). The test 37 seconds later showed otherwise.
- **He gave ten `steer` orders after 398710 and trimmed after none of them.** The captain typed a trim order within 16 minutes of four of them (after 340, 348, 268 and 280) and later after two more (287 and 255). His joining note in the journal says "Trim after the helm has swung." His one trim order in the slice was on taking the deck (398811).
- **He blamed the tide three times without grounds.** Twice for what the account's own arithmetic explains (399925, 403581). Once for an apparent wind "pulling round" (441543) when the wind was simply backing, as the log said at 09:06; a set to the north-west would in any case have drawn the apparent wind the other way.
- **He wrote nothing in his journal for 55 hours.**
- **He did not heave the log** when the wind died or when it made.
- **He stood on headed for a while.** From 06:28 on the 26th he bore away to 255 and then 235 on the starboard tack. By 07:39, by my working, she was steering about 74° from her line when the other tack would have lain within about 35° of it. He wore at 08:10. At 06:28 she had no way to wear with.
- **Modern words in a period voice:** "high pressure building over us", "under the ridge" (441645), "not a front" (443451). The reasoning itself is sound and its near forecast, "More calm first", was right.

**What he asked for or wished for, in his words.**

- 313207: "You may want to put some speed on the clock, sir."
- 343473: free passing of the deck "while I stay aboard".
- 398809: "I'd be glad to see it if you'll show it in the log."
- 406846: "A note for the order book: "come up half a point" was refused as a change of course without your directions, but "steer 340" was taken under the grant to steer. The two should be judged alike."
- 415821: "A note for the book: in light airs, full and by seems to steer by the apparent wind on the topsails and gives away a great deal of height."
- 427161: the nudge "might count only orders that reverse each other."
- 453136: "when a course is shaped and the wind frees, the shaped course should take over from full and by."
- The handover: 'trim' to be belayed "before any heave-to".

**In character.** Asked which port he would make for, he chose Funchal: "I like the idea of a cargo that gets better for being carried a long way" (298892). His history is right for June 1805: the Salem pepper ships, the Cape "Dutch just now", the Gilstone as "Sir Cloudesley Shovell's rock". To the captain's song he answered "seventy-four miles, about twenty-five leagues" (449369).

## 8. Cross-check against the notes

### The owner's items

| Note | Evidence in the slice | Verdict |
|---|---|---|
| 10. A long tool-use session crashed or timed out; the returning session could not see its journal | 398773–398893. `read_log` could not reach the note and no tool reads the journal. The phrase that worked here was `show the journal of the officer` (398818), first time; no refused variant is in this session's inputs | SUPPORTS, and adds the mechanism (section 5.2) |
| 11. Keep the journal out of context by default | The dump at 398818 was 200 entries and about 5,000 tokens. 163 entries were stand-bys begun or ended. Four were the officer's own notes | ADDS NUANCE: the journal's bulk is the harness's entries, not the model's |
| 12. Re-seating should be the default | Second and third seatings 18 and 41 seconds after the stand-downs, same chat, everything kept (343381, 343551) | SUPPORTS that m5c-b delivers it. But "I have the deck" still stands the station down, and the captain wants "free hand offs that basically put you with watcher authority" (343464) |
| 13. Multi-condition stand-bys | He stood by "a wind shift" at 341895 and replaced it with "the change of the watch" at 342012; he could not have both. From 19:45 on the 25th the glass woke him 25 times in 16 hours, for want of an event on the readings | SUPPORTS |
| 14. Claude Desktop must be restarted between sessions | No restart was needed for the two re-seatings. Something replaced the conversation before 398711 | ADDS NUANCE |
| 15. A general allowance of authority | Seven allowances in the slice. Six in 24 seconds for one authority, none used (406851–406875). `steer 340` passed where `come up half a point` did not | SUPPORTS strongly |
| 16. "Keep" orders | 22 firings of 'trim', and 7 belay and resume orders to mind it. "Keep her full and by" is already a keep order of a kind, and the officer gave it up in light airs (415818) | SUPPORTS |
| 17. Taken aback urgent in a calm | 0 urgent of 90; 0 wakings; 0 easings of the clock | SUPPORTS that m5c-b fixed the urgency |
| 18. Wind shifts fill the log | 9 lines in 55 hours, each a real step | In this slice the fix is complete |
| 19, 24. The reckoning near land | Open sea throughout. Only the bearings at 261235 and 261241 touch it | Cannot be seen here |
| 20. Chart tools | "I can't draw on my map" (261291) | SUPPORTS |
| 21. A turn need not end at `say` or `answer` | 14 out-of-turn stand-bys after spoken lines; an intention spoken before the act at 414715. `answer` did not end the turn in any of its 3 uses | SUPPORTS for `say`; ADDS NUANCE for `answer` |
| 23. More than one station through a door | The captain asked "the watcher" for the weather while the officer had the deck (441609) | SUPPORTS the wish |
| 1–9, 22, 25, and the local notes | Nothing in the slice | Cannot be seen here |

### The model's comments

| Comment | Evidence | Verdict |
|---|---|---|
| On 16: 'trim' "fired while she lay hove to and filled her out of it, twice" | 162102 and 193303, both before the slice | SUPPORTS, by the full log |
| On 16: "In a dead calm it kept the watch bracing yards all night for nothing." | Six bracings between 22:55 and 03:43, the yards going 0°, 37°, 58–60°, 58–60°, 15°, 58–60° | SUPPORTS. "All night" is five hours |
| On 16: a keep order "should pause itself when … there's no wind to trim to" | The game refused one firing in those words (327484) and carried out six | SUPPORTS; the check exists and is momentary |
| On 17, 18: "The urgent alerts stopped." | 0 urgent | SUPPORTS |
| "about 25 times in one night" | 19 in the first and middle watches, 25 in the morning watch after, 90 in 20 hours | SUPPORTS as an order of size |
| "came every few minutes" | Median 9.7 minutes; 12 of 89 gaps under 5 minutes; never under 3 | ADDS NUANCE: every ten minutes, in bursts of every three to five |
| "wants re-arming only after she has had way on again, or nothing logged under about two knots" | 85 of the 90 at a mean of 1 knot, the first five as it fell from 2; none in 2 to 3 knots with way on | SUPPORTS: either rule would have removed nearly all |
| Redacted addition: "Every sail also is individually logged as aback, forty notable lines in 90 minutes" | 228 lines; 53 in the densest 90 minutes; 39 in the densest hour | SUPPORTS, and it understates |
| "In airs of one to four knots … it logged a dozen shifts in an afternoon." | Not here. Neither afternoon in the slice has a shift line. The dozen is 23 June at the Roscoff anchorage: 21 lines from 13:23 to 17:45 (203031–218759) | Cannot be seen in this slice |
| "A minimum wind strength before logging a shift would finish it off." | The four lines of the calm night were at a mean of 1 knot, two of them worded "calm" | ADDS NUANCE: a floor would have hidden a real backing of eight points, though nobody could use it |
| "The ship itself still feels the swings, so the cause is in the weather systems." | Here the logged wind turned steadily. The aback flicker is a ship with no steerage way in a 1-knot air | ADDS NUANCE: in this slice it is a calm, not a chattering wind |

### The model's additions

| Addition | Evidence | Verdict |
|---|---|---|
| "The relay cut calls at 60 seconds … --wait 50 fixed it" | The header says 50 seconds; 11 out-of-turn stand-bys sit 49 to 51 ticks after a spoken line; no cut call | SUPPORTS that the setting was in force and held |
| "My first hand_over came back 'Nothing was run'" | Not here; session 2, tick 527255 | Cannot be seen in this slice |
| "The handover note isn't part of the reseat brief. It only shows if it happens to fall in the brief's last 20 log lines." | 343381: "my handover note is right there in the log for me". 398809: "I didn't get one this seating". The code agrees (section 5.2). The officer's first statement of it is in session 2's journal at tick 527393 | SUPPORTS on both sides |
| "The officer isn't treated as a person on deck … listed 'below, asleep'" | The remark is at tick 54007, before the slice. Here 16 `watch.relieved` lines relieve "the deck" by watches and name nobody; the officer holds the deck through 12 of them | Cannot be seen here; the log's lines are consistent with it |
| "The contrary-orders warning fires on ordinary sequences" | 424818 | SUPPORTS |
| ""Trim sails" acts before the helm has swung" | The captain trimmed by hand after six of the officer's helm orders; 'trim' does not fire on a change of course | ADDS NUANCE: the larger gap here is that nothing trims after a course change |
| "The Harpy's reckoning kept advancing while she lay at anchor." | Here the account stood still for 16 hours of "no way" | Does not recur. But see the phantom 2½ miles (section 6.3) |
| ""Full and by" is refused as changing your course." | Accepted here under the old allowance (259872, 415362). The same pattern returned with `come up` (406842) | SUPPORTS the pattern |
| The hand lead and "no bottom at twenty fathoms" | Seven such lines offshore; the handover gives "51 fathoms" from the readings | Consistent |
| Worked well: "The new quieter "aback" lines." | Quiet as to waking, loud as to the log | ADDS NUANCE |
| Worked well: "at a wind shift then trim sails" | It fired faithfully, about once a point. Seven of its 22 firings came in a calm, and it was belayed three times and resumed four | ADDS NUANCE |
| Worked well: "The noon latitude." | Two sights, each 4 miles from the account, in opposite senses | SUPPORTS: the only evidence of set the ship had |

### The gate's rulings wanted (item 14)

- **The officer's domain as drawn.** In this slice the rule on the course was a formality, since `steer` had been allowed since the first day. Its one bite was on a synonym (406842). The slice's evidence favours judging an order by what it does and not by its verb, so that one word from the captain opens the helm.
- **The "immediate danger" exception.** The refusal at 406842 quotes it. No danger arose in the slice, so it was not tested.

## 9. New findings not in the notes

Ranked by weight.

1. **A change of conversation behind a manned station leaves no mark, and the arriving model cannot reach its own handover note or journal.** 398711–398893. The door attaches silently. The brief has 20 log lines. `read_log` returns only the newest 200 lines of a severity, and 262 aback lines lay in the way. The captain had to be the courier. The seat counting of m5c-b counts stand-downs, not sessions.
2. **The calm's aback lines are still two thirds of everything notable**, and the per-sail lines, which have no re-arm, are the greater part: 228 against 90 (section 6.1).
3. **The officer gave ten `steer` orders and never trimmed to one; the captain typed nine trim orders during that watch, six of them after the officer's helm orders.** 406843–453133. 'trim' fires on the wind, not on the helm. This is what the later standing order "steady trim" (469859) answers.
4. **`shape a course` reported a course "too near the wind to be laid" that lay 61° from the logged wind and was then steered without trouble.** 451328, 453133. The shaped course does not take over when the wind frees.
5. **The account moves in two-hour steps.** One heave of 1¼ knots after the calm credited about 2½ miles she had not sailed (399631), and a failing wind pulled the reported position back 2 miles at one heave (313231). The officer read both as drift or tide.
6. **The helm is five verbs to the domain check.** `steer` allowed, `come up` refused (406842); ten allowance lines over the voyage for one authority.
7. **A standing order's "wind shift" is one point of the mean and the log's is two.** 22 firings against 9 lines; 16 firings have no shift line within 15 minutes. A reader of the log sees the hands trim "by standing order" with no cause given.
8. **"I have the deck" stands the station down, and the brief does not say so.** 343473, 343510.
9. **The game refused one futile trim and carried out six.** 327484.
10. **Full and by gives away height for no speed in this schooner**, by the captain's own log (403651), and the officer gave it up for compass courses.
11. **The schooner makes about the speed of the wind in 2 to 3 knots of it.** 450031, 457231.
12. **An order that cannot help is worked for twenty minutes before the log says so.** 398567–399737, the catharpins.
13. **The journal is nearly all the harness's own entries.** Of the 200 shown at 398818, 195 were the harness's and 151 of those were "Stood by until …".
14. **Each sampling of the officer drops the game to 1x**: 55 times in the slice, 22 of them in the second night and 20 more on the morning of the 26th. In the calm, with the officer asleep or without the deck, it happened hardly at all.
15. **Small wording and noise items**, listed in section 6.5.

## 10. Could not determine

- **What happened on the owner's side before 398711**: a restart, a new chat or a compaction. The save holds no door event for it.
- **How long the stand-bys lasted in real time**, and so how many fifty-second calls the 15-hour wait took.
- **Why the officer was silent for nine minutes of ship's time at 426619.**
- **What the readings actually said** at 399925, 403581 and 415814. My account of the reckoning's steps is inferred from the officer's figures and the log reads. It fits the 24th to the half mile. For the 26th the same sum gives 24½ miles where the noon line says 22, so the rule for the noon distance is not settled.
- **What "full and by" steers by**: the wind of the moment, the ten-minute mean, or the apparent wind. The officer's two reports (415821, 453136) point different ways.
- **Why "too near the wind to be laid" was said at 451328.** A wider angle in the test than in the steering is my guess.
- **Whether a bare `you may come up` would have covered every amount.**
- **Whether the officer was listed "below, asleep" in this slice.** No `the people` reading was taken here, and the log's watch lines name nobody.
- **Whether the 4-mile differences at the two noon sights are set or the sight's own error.** Primer 10 allows the sight two miles or so.
- **Whether notable lines open a turn when no stand-by is in force.** The sunrise at 428295 did. If so, an officer who only spoke and never stood by would have been sampled at each of the calm's 318 lines. He always stood by, so it was not tested.
