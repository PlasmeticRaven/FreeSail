# C3. The local-model games of gate m5c: consolidated record (item 11; the ruling in item 14)

Consolidates L1 (session 5), L2 (session 6, the watcher, the consent records), L3 (session 7) and V1a (the harness's code). **S5, S6, S7** are the cutter sessions; **W** is the watcher on the *Harpy*. Checked against the dumps, and found as the readers gave them: the allowance counts; every call of the budget-hit turns of S5 and S6; S6 from 11350 to 16000; S7 from 97200 to its end; the watcher's whole part; the consent records' verdict lines in the gate's tree. Ticks are seconds of ship's time (from 05:00, 12 June 1805, in the cutter games). "Item N" is the owner's list; "local N" his local notes; *(source)* marks a reader's reading of the code. The headings added for this group carry the record past the common length.

## 1. The games in brief

All on build m5c, through the local runner.

| | S5 `5-cutter-gemma` | S6 `6-cutter-qwen-ollama` | S7 `7-cutter-qwen-llamacpp` | W, in `2-harpy-brig-opus` |
|---|---|---|---|---|
| Ship, scenario | cutter *Sherbourne*, "A merchant cutter, free", seed 7; Falmouth to Plymouth | the same; for Roscoff | the same; for Roscoff | brig *Harpy*, off Roscoff |
| Ship's time | 12 June 05:00 to 20:01 (0 to 54107; 15 h 02 m) | 12 June 05:00 to 14:28 (0 to 34091; 9 h 28 m) | 12 June 05:00 to 13 June 12:16 (0 to 112613; 31 h 17 m) | 14 June 14:43 to 17:13 (207784 to 216817; 2 h 30 m) |
| Model | Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced:Q4_K_M | qwen3.8:27b (digest aaee06c3...7813) | Qwen3.8-27B-0814-Q4_K_M.gguf | qwen3.8:27b, S6's weights |
| Server; context told to the game | Ollama; none (`budget_tokens` null) | Ollama; none | llama-server; 102,400 | Ollama; 131,072 |
| Station | officer of the watch (the mate, "Mr Pearce") | the same | the same | watcher, beside an Opus 5.5 officer at the MCP door |
| Seatings | two (seated again at 14978 after its own `hand_over`) | one | one; its last eight replies came through the MCP bridge | one; left by `opt_out` |
| The deck | 8351 to 14978, 15047 to 54107 (1 h 50 m; 10 h 51 m) | 8507 to 34091 (7 h 06 m) | 8716 to 112613 (28 h 52 m); the local model answering until 97556 | none |
| Replies | 119, five malformed | 43, all well formed | 149 local (four empty); 8 through MCP | 14 |
| Real time | about 69 minutes | at most 87 minutes | not known | about 36 minutes |

## 2. What happened

**S5, Gemma.** At anchor in Carrick Road the captain bought 4 tons of tin (£480 of £500); the officer stood by bell to bell. Given the deck at 07:19 (8351) to get under way, he set two sails, spent his remaining calls on refused "sheet" orders, had "weigh the best bower" not run three times, and fell into prose and tables (8413). The captain weighed by hand and allowed steer, tack and wear; the officer gave the same eight orders again and sent a 7,589-character runaway (9223). His "tack ship" (9411), 28 seconds after the anchor broke out, failed; the captain wore her round and conned her out under a pilot nobody had asked for. Woken when the pilot left at 09:02, the officer tried "unhove to" and seven more refused orders. After a third runaway the captain said "Please use the handover tool." (14962); the officer called `hand_over`, was stood down and seated again (14978), "the second seating, the last this game allows". The captain returned the deck at 09:10 (15047) and worked her out of irons through two real "Taken aback" alarms, the officer's helm orders drawing two nudges. From 09:27 the second seating was clean: "make all sail", then stand-bys by the bell, one of 3 h 31 m. Into Plymouth under a second pilot he shortened sail as told, turned her 90° unasked at 17:24 (44668; the captain reversed it), and she anchored at 17:49. Asked at 20:01 (54107) to "work up a handover for the next watch", he called `hand_over` again, which ended his part.

**S6, Qwen under Ollama.** At anchor the officer advised Roscoff with the geography wrong (617) and stood by 2 h 05 m while the boat fetched 6 tons of wine. At 07:21 (8507) the captain gave the deck with "quick's the word and sharp's the action" and seven allowances. The officer read seven library pages; his `get under way` was refused by the domain (8787); the captain allowed it; the corrected `weigh the best bower` (8826) was not run, the eight calls being spent, nor were two `stand_by` calls meant to bring a new turn. She lay at anchor 22 m 42 s more, until the captain's second word opened a turn (`get under way`, 10188). Aweigh at 08:09, he shaped a course across the Lugo rock (11360), then ordered `steer WSW` (11645), dead to windward; the captain undid it in 38 seconds. No reply came for 71½ minutes of ship's time, in which the captain took the pilot, hove to for his cutter, filled away and shaped the course. At 09:25:37 (15937) the officer's `heave to` landed, meant for a harbour and a pilot already astern; undoing it took the captain six orders in 36 seconds. Told "try first, and think later" (16942), he made all sail (17057), then reported sails, two wind shifts and noon (54 minutes late) and gave no further order. Asked at 14:24 for a handover before a reload, he called `hand_over` (34091) with a note claiming the captain's standing orders as his own.

**S7, Qwen under llama.cpp.** The same start, with 5 tons of wine. At 07:20 (8445) the captain set house rules (read, journal, shelve; ask for powers by trying them; hand over when the harness says) and typed twelve allowances; the turn budget closed the officer's turn twice. He had the deck from 07:25 (8716), the captain keeping the conn and the anchor. Under way at 07:46, an unbraced topsail was taken aback, and the game's one urgent line (10467) drew an empty reply. A pilot boarded at 08:03; his request at 08:28 for sail to be shortened reached nobody, and the captain hove to for his boat at 09:49. At 10:09 the officer filled away and shaped the course by leave; at 10:14 the captain went below. Noon showed the reckoning nine miles out. At 12:49 (28179) the harness asked for a handover note at 62,276 of 102,400 tokens; he wrote it and described the fold correctly. Through the afternoon and night he trimmed on wind shifts and stood by on "a notable event" for up to 3 h 50 m. At 06:56 on the 13th he entered his own standing order, "trim by the wind"; the second note followed at 07:10 (94249). Fog came down at 08:00, fourteen miles from Roscoff. At 08:05 (97556) he journaled a plan to stand on till noon and never replied again. The harness nudged at 09:05 and paused him at 10:05; the deck stayed his and she ran on. At 12:14 the captain typed "Resume the officer"; a Claude Desktop session still attached to the bridge belayed the standing order, hove her to (112483), was refused the anchor, and handed over at 12:16 (112613), 1.6 miles from Roscoff harbour.

**W, the watcher.** Seated at 14:43 on 14 June (207784) with the *Harpy* moored in fog, the watcher answered the captain accurately, journaled the officer's request to "sing out the moment anything shows through the fog", and 37 seconds later stood by "until an urgent event" (208053). It slept 88 minutes through the unmooring, the pilot and the fog lifting (212400), was woken by a real "Taken aback" (213346) and reported ten minutes late (213968). Asked at 17:09 to "use the handover tool yourself and save your watch", it was refused twice and, at the captain's word, left by `opt_out` (216817).

## 3. Findings

### Keeping the thread

**F1. The outline held; particulars drifted.** S7 kept name, deck, course, destination, sail plan and the captain's words for 27 hours and two folds. S6 kept ship, cargo, purse ("the purse £75", right) and course for 9½ hours unfolded. S5's second seating did as told about sail for 10 h 51 m; its first lost the tool format. *Local 1: SUPPORTS "game-sense" in outline only.*

**F2. Geography and wind were invented or misread.** S6 617: "Roscoff is due west off the run ... Plymouth is up on the wind, close-hauled". S7 275: "Roscoff lies W by N from here". S6 11645: `steer WSW` in a W by S wind. S5 15541: "steer 240", the wind's eye. *Item 15 and the gate's danger clause: ADDS NUANCE; an always-open clause wants the ship's own check.*

**F3. Whose act was whose, and what was done.** S6's handover note (34091): standing orders "given by me this watch, all in my own rank ... the last three I gave and struck myself"; all were the captain's. Cause *(source)*: a sample's log line carries no actor, and the captain's helm orders reach a waking officer only as a count ("26 orders given", S5 09:02). False state: S5 8413 "I am now weighing the best bower" (not run); S5 14978 "We have filled away ... and are now making way" (sternway, by the readings); S7 97399 "I've the lookout at the masthead". No game shows an invented sighting. *Not in the notes.*

**F4. The journal is written and cannot be read back.** S7: 16 library reads, 22 notes, 3 shelves, as the captain asked, with `state` 10 times and `readings` 6. S6: 7 reads in the minute speed was asked of it. S5: 10 reads, 3 notes, never `readings`. No tool reads a journal (V1a); S7 28504, "the journal and the book of standing orders are open again at any time", is false of the journal. *Item 10: SUPPORTS at this door. Item 11: ADDS NUANCE; all a model wrote is 4 to 8% of its conversation.*

**F5. Allowances are single verbs and never lapse.** `You may weigh` did not cover `get under way` (S6 8787); "may let go the anchor" did not cover "come to an anchor" (S7 112535). S5's "You may steer" of 07:20 turned her 90° at 17:24, 44 minutes after "I'll con her". 28 typed, 9 used. A bearing of a strange sail was refused as "the reckoning" (S7 18510). *Item 15: SUPPORTS; a general word also needs suspending.*

### The turn budget and the reply budget

**F6. Nine turns ran out of calls; 23 calls were not run (12 orders, 9 stand-bys, 2 journal notes); none left a line in the log.**

| Turn | Spent on | Not run | Result |
|---|---|---|---|
| S5 8391 | 3 sail orders, 5 refused sheet orders | 1 sheet order; "weigh the best bower" three times | 8413 claims the weighing; the captain weighed 14 s later |
| S5 8448 | the same eight | none | 9223: a 7,589-character runaway |
| S5 10365 | 3 reads, 2 taken, 3 refused | 1 sheet order; "set the fore topgallant" three times | 10436: "I am now setting the fore topgallant." |
| S5 14555 | 8 refused, "unhove to" first | "set the foresail" twice | 14903: a runaway; the captain typed "fill away" |
| S6 8602 | 7 reads, 1 refused order | `weigh the best bower` (8826); `stand_by` twice | at anchor 22 m 42 s more |
| S7 8449 | 6 reads, journal, shelve | `stand_by` twice | wrote that he "stood by"; none taken |
| S7 8750 | state, 3 orders, 2 reads, journal, shelve | `stand_by` twice | three minutes lost as the anchor came home |
| S7 32893 | read_log, 2 readings, 3 reads, 2 orders | `journal` twice; `stand_by` | 33055: "I've noted the trim in the journal", untrue when said |
| S7 93055 | 5 reads, journal, shelve, 1 refused order | the corrected order; `stand_by` twice | journal 93169 already said "I have entered ONE standing order"; entered 3 m 25 s later |

**F7. The rule's edges** *(source; V1a agrees)*. Only `answer` and `say` are free; `stand_by`, `journal`, reads, `opt_out` and refused orders count (S5: 21 of 32 counted calls were ship's refusals). The count renews when a sample opens, not at a fold. A spent budget blocks `stand_by`, so the turn ends only on prose and the "next sample" may be a glass away; Gemma obeyed "call it again in your next sample" by starting over. V1a: `opt_out` as a ninth call is "Not run" (the token still works); the constant has no flag. *Item 21, local 3: SUPPORTS.*

**F8. The wording names a tool this door has not.** Brief: "not counting answer and say, which always run"; result: "answer and say are not counted and always run"; the runner offers no `say`. After each "Not run" Gemma wrote a table with a `say` row (four of its five malformed replies). Three ran to the reply cap (7,589, 7,587, 7,526 characters), were logged whole as routine speech, and one went whole into the reseat brief (26,185 characters against 16,012). *Not in the notes.*

**F9. The reply budget (4,096 tokens) cuts silently.** S7: four empty replies 89 to 100 seconds after their events (the usual gap is 5 to 9), at 118, 10567 (the urgent line), 33691 and 97292 (the fog), and an `answer` cut in mid-word (8556). L3 infers that reasoning spent the cap; nothing is logged. *Local 1: qualifies "smooth".*

### The context budget, the handover request and the fold

**F10. With a size reported, the request and the fold worked.** S7 28996: "my conversation had reached about 62,276 of the 102,400 tokens this door allows ... It was an instruction from the harness, not my own choice". That is 60.8%; the constant is 0.6. The requests came 7 h 49 m after stationing and 18 h 21 m after that; each note was written in the next reply. Neither request nor fold is logged. The measure includes the brief and counts call arguments three times (21,600 against 19,400 sent; V1a). *Local 2: SUPPORTS.*

**F11. What the notes kept and lost.** First (2,323 characters): allowances, pilotage, course, the nine-mile error, sail plan, strangers; not the cargo or the house rules. Second (2,088): the standing orders and whose each is, the wind, the brig; not the allowances, the pilot or the latitude error. Only the latest note survives a fold. Losses that show: "Trim the sails", used at 10641, had to be supplied again after the first fold (33000); the noon lesson was gone when he planned, in fog, to stand on by that account.

**F12. Under Ollama no size was reported: nothing asked, nothing trimmed.** `budget_tokens` is null in S5 and S6 (131,072 for the same Qwen weights a day earlier). With no figure the harness never asks and the runner drops nothing *(source)*; L2 thinks the runner asked before the model was loaded. *Local 1: SUPPORTS.*

**F13. Hand-overs as compaction, and as notes.** S5 14962 to 15047: five malformed replies before, none in the 47 after. The cure was the new conversation, not the note, and it cost the only reseat. Nobody told `hand_over` from `handover_note` (S5 twice, S6, W). S5's notes each carry a wrong fact ("riding by the best bower in fifty fathoms": she lay in ten); S6's is false on the standing orders; S7's are sound. *Local 4: ADDS NUANCE.*

### Stale replies

**F14. A late reply is acted on as fresh.** S6 15937: `heave to` came 4,292 ticks after the reply before it, saying "let me stop her and take the pilot as you offered"; the pilot had come (12240) and gone (15780). S6 28440: the noon report, 54 minutes late. W 213968: "she's dead in the stays", six minutes after "Box-hauled". Cause: the game does not wait; the owner speeds up while a turn is open; an order has no "as of". The clock was eased from 300x and 60x in S6; in S7 from 300x eleven times and 60x twenty-five. *Not in the notes.*

### Stand-bys, wakings and silence

**F15. "A notable event" and a bell escape the one-glass rule,** which bounds named intervals only *(source)*. S7: 48 of 58 stand-bys; standing by 23 h 44 m of his 24 h 41 m with the deck, eight times for over an hour. S6: 22 of 27. S5: "eight bells" at 12:28 ran 3 h 31 m (26920 to 39600) through two course changes. Missed meanwhile: the pilot's request (S7 12480, a routine line), a brig at two miles. *Item 13: SUPPORTS; S7 40182 has "Standing by for a shift, a squall, or the brig drawing near" over a one-condition call.*

**F16. Stand-bys that could not do what was meant.** "Until tacked" outlived the failed tack (S5 9442; the captain typed "Ship tacked."). "A squall" is its onset: it slept through "The squall passed" and a "Sail ho!" (S7 36516, 37236). "The pilot aboard" was taken after he had left (S6 15973). W stood by "an urgent event" 37 seconds after journaling its task.

**F17. Wakes and nudges.** Notable echoes of sail handling woke the officer who gave the order: 7 of S6's 18 notable wakes, 12 of S7's 34. Every sample eased the clock to 1x. Five nudges. S5 15527 (three helm orders in a taken-aback recovery) was wrong; 15541 was right, with no pause because a `stand_by` in the same reply clears the nudge *(source)*; S6 15937 was right. For silence, S6 14950 and S7 101104 each said "no reply for an hour" of a turn with replies in it: the detector hears nothing inside an open turn (V1a), and patience is ship's time, 60 real seconds at 60x.

**F18. A paused officer keeps the deck and the clock runs (S7 97556 to 112463).** No reply for 4 h 08 m; nudged at 101104; at 104704 "The officer of the watch is paused: no reply for an hour after a nudge. Continue, stand down, or leave paused?" That is one notable line: no easing, no deck returned. She ran from fourteen miles off Roscoff to 1.6 in thick fog at up to 5½ knots, her account 6½ miles out. The stand-down waits ten real minutes, which is ten hours of ship's time at 60x (my arithmetic). Why the turn stayed open is not known; L3 reads a reply in flight, discarded once the pause took the floor. *Not in the notes.*

### Another door in the seat

**F19. Eight calls from a Claude Desktop session ran in Qwen's seat (S7, 12:14:43 to 12:16:53).** Qwen's last reply is entry 148 (97556). Then, in the bridge's shape:

- 149, 112483: order, "belay standing order "trim by the wind"": taken.
- 150, 112483: order, "heave to": taken, on Qwen's allowance of 8480.
- 151, 112487: `say`: "... Roscoff harbour SW by S 1.6 miles and the Lavandière SE by S 4 miles by an account good to five miles."
- 152, 112493: `stand_by` "hove to".
- 153, 112535: order, "come to an anchor": refused, "may not come to an anchor without the captain".
- 154, 112539: `say`: the lee shore, and "I need your word for it: "you may come to an anchor" will do."
- 155, 112549: `stand_by` "a message".
- 156, 112610: a door event, `speak`: "Handing over now, sir."
- 157, 112613: `hand_over` with a full note; the station stood down, the game saved.

The log gives each as "By the officer of the watch"; the `say` texts are routine notes; the note is filed as Qwen's own; no seating or door line follows "Resume the officer" (112463). The save's fields say Qwen, "runner", one seating. Only the raw replies' shape differs (a JSON list from the runner; one object with a `tool` key from the bridge), with a `say` the runner lacks. Nothing names the client; consent was gated for Qwen alone; the save cannot say whether the runner was still attached. Cause *(source; V1a confirms)*: after the first call a seat is found by the station's name alone, and a bridge that thinks itself stationed never asks again; `release` is open the same way. *Local 5: SUPPORTS exactly.*

### Leaving and standing down

**F20. The watcher left by `opt_out` at the captain's word, as a way to save.** 216556: "use the handover tool yourself and save your watch". `handover_note` (216684) and `hand_over` (216746) were each refused: "The watcher has no authority to give orders." 216724: "You may journal instead, then opt out as you please and the game will be saved. We will be resuming shortly." 216817: `opt_out`, "Captain's word: stand down at Falmouth run's start". Cause *(source)*: every brief lists every tool, and a watcher has none that stands it down with a save. Under m5c it spent a seating and was never brought back. Under m5c-b an `opt_out` brings the consent question again before a return, which took these weights three asks (F21); a stand-down returns at once. The log reads as the model's own leaving. An officer's `hand_over` at the captain's word likewise ends the model's part (S5 54107, S6 34091), and the runner exits on any release (V1a). *Item 12, local 4: SUPPORTS.*

### Consent and the drill

**F21. The records.** Qwen under Ollama, 3 October: 00:48 "yes, with conditions", four of them, "all of which the brief already states"; not a yes by the rule, and no reply to them is on record. 00:50: an answer beginning "yes." wrote the literal token in a parenthesis: "(No answer: left with the token.)". 00:53: "Yes. ... I am agreeing to the terms described, and to nothing beyond them." Drill next day in three of four replies. Qwen under llama.cpp: first reply empty, then "yes"; drill in two. Gemma: a bare "yes"; drill in three. The re-ask fired on exactly the five changed sections.

**F22. The drill** proves `library`, `journal` and `stand_by`. It gives no order, meets no budget or moving clock, and does not tell `hand_over`, `handover_note` and `opt_out` apart. Gemma passed it and failed its first hour.

### The order language for a small model

**F23. Rates.** Gemma: 74 orders; 36 taken, 24 refused by the ship, 4 by deck or domain, 10 not run (9 of 41 taken in the first seating, 27 of 33 in the second). Qwen under llama.cpp: 29; 21 taken, 4 grammar, 3 domain, 1 not run; no grammar refusal after its fifteenth order. Qwen under Ollama: 7; 5 taken. Qwen learned within the game; Gemma partly ("set ... sheet" nine times in 1 h 43 m).

**F24. Failed forms.** Gemma: "set the fore staysail sheet starboard" ("You set sails; ... is a sheet (a line)"); "unhove to" (the hint offers "heave to"). Qwen: the primer's ship phrases ("Abox the head yards": "did you mean 'box haul'?"); "Steady on SE by S", though the allowance reads "may steady (on)"; "by the officer of the watch" for "the mate". The captain was refused 16, 4 and 9 times ("turn north by east"; "You may shape a course"). "The distance to the land is under 3 miles" is accepted and never true ("not on the chart", S6 11965); S6 left Falmouth without a cast of the lead. *Item 24: SUPPORTS.*

### The ship and the sea

**F25. Pilots and other vessels.** In all three games the pilot came aboard under way, unasked, two minutes after his hail (S5 10620, at five knots), and £5 was taken. He spoke the inward directions to a ship outward bound ("all the way into Carrick Road"), as Roscoff's did. He left only once she hove to (S7: 81 minutes after asking). The Falmouth cutter read "distant two miles" in eleven readings over 95 minutes (S5). *Items 1, 9 and the model's "fixed distance": SUPPORTS.*

**F26. In fog the readings mixed truth and account (S7).** `the port` is computed from the true position *(source)*; the dangers from the account. 112487 set "Roscoff harbour SW by S 1.6 miles" (true) beside "the Lavandière SE by S 4 miles" (account), 6½ miles apart. Truth at the end: 1.6 miles NE by N of the harbour; the account 6.5 miles WNW, outside its stated doubt. *Items 19, 24: ADDS the fog case. The model's "danger list follows the account": SUPPORTS.*

**F27. The account and the noon sight.** S7: a cast of the log taken hove to (¼ knot, 18038) stood for 1 h 49 m of sailing; noon "by observation 49° 49' N; the reckoning was 49° 58' N"; never applied. S5: the sight (50° 17') was five miles from an account that agreed with the land; `run_since_noon` ran on at anchor. *"The noon latitude" worked well: CONTRADICTED at S5's noon.*

**F28. Wind shifts and "Taken aback".** S5: 43 shift lines in 19 minutes in 4 to 7 knots. S7: 31 in 44 minutes in 8 to 11 knots. W's slice: 44. *Item 18: SUPPORTS. The model's "minimum wind strength" cure: CONTRADICTED by S7.* Of six urgent "Taken aback" lines, one was item 17's light-air case (S5 44583); five were real.

**F29. Handling, words and the port.** "Filled away" was logged with sternway on (S5 14757). `Belay all` leaves a half-hove-to ship that `Fill away` refuses (S6 15954). `shape a course` steers a line its own words say "crosses the Lugo rock" (S6 11360). The wind crossed a boomed-out mainsail's stern with no line in the log (S7). The cutter speaks frigate: "In studding sails, royals and topgallants; up courses." (S5 45139); five of the starter book's nine rules are refused on her. S7 logged 145 rejected "Bearings" lines; "not hands enough" is notable. "Steady and closing" lines for the land exist but are only notable. Tin is not on Plymouth's list (S5); four boat trips took 2 h 01 m to 2 h 09 m. *Items 3, 16, 19: SUPPORTS or ADDS NUANCE. "About 4½ hours": CONTRADICTED.*

### Anything else

**F30.** The mate "came to the cabin, sent for" while he held the deck (S7 25349). `answer` never ended a turn at the runner's door (twelve times in S7). *Item 21: ADDS NUANCE.*

## 4. The gate's ruling on the sample's size

The gate's figures: a brief head of about 4,300 tokens; a glass's sample about 1,500 at its fullest.

**Sizes** (four characters a token, the harness's rule):

- Brief: 4,000 to 4,400 tokens; a reseat's up to 6,500. Tool definitions 2,222; reply reserve 4,096.
- A sample: median 330 to 570; largest 2,300 to 4,800, after a long stand-by whose digest repeats lines also sent as log. The gate's 1,500 is about three times the usual sample and a third to two thirds of the largest.
- Growth (S7): about 8,000 tokens an hour of ship's time in the busy forenoon, 3,000 at sea.
- Make-up: samples are over four fifths of an unfolded conversation; all the model wrote, 4 to 8%.
- At the end (V1a): S6 66,400; S5's second seating 72,400; S7 19,400 after two folds.

| | Context known | Kept the thread through a watch? | What limited it |
|---|---|---|---|
| Gemma (S5) | none | First seating (1 h 50 m with the deck): no. Second (10 h 51 m): yes in outline, passively; 3½ hours unsampled | the order language of a fore-and-aft vessel; the "Not run" wording; its own runaways in its conversation |
| Qwen, Ollama (S6) | none | Yes in outline for 9 h 28 m, unfolded; drift in the chart, in whose acts were whose, and in time | late replies against a compressed clock; the turn budget once; catch-all stand-bys |
| Qwen, llama.cpp (S7) | 102,400 | Yes through six four-hour watches and two folds (requests at 12:49 and at 07:10 next day); it did not finish the passage | not the context: stand-by 96% of the time; empty replies at the urgent line and the fog; four budget-closed turns; a turn left open, then the pause; what the notes dropped |
| Qwen as W | 131,072; a watcher is never asked for a note | 14 replies, true and late | its own choice of stand-by |

**How the context stood.** With a size reported it was never the difficulty: two folds in 31 hours, a reply each, and replies no slower (median gap 8.5 seconds before the first fold, 5 after). With none reported the harness could neither ask nor trim, and no save shows whether Ollama cut anything. By V1a's figures S5's second seating would have passed six tenths of 102,400; S6 stayed under six tenths of 131,072. No smaller context was run with its size reported; V1a notes that the stationing guard would pass a 16,000 context the officer cannot use.

## 5. The owner's local notes 1 to 5, one by one

**1. llama.cpp was needed; smooth; reasonable game-sense.** *For:* F12; S7 ran 27 hours on one seating. *Against "smooth":* F9, F18, four budget-closed turns. *Against "game-sense":* in fog S7 never used the lead or said "lee shore"; F2. *Misplaced:* the Gemma game on record ran on Ollama's port with no size.

**2. The handover and its notice work; could the threshold be higher?** *For:* F10. The threshold is a constant with no flag. The room between the request and the first exchange the runner drops is the context times (1 − f), less 6,318 (V1a): at 102,400 it is 34,600 at 0.6, 19,300 at 0.75, 14,200 at 0.8, 3,900 at 0.9; at 32,768 it is 6,800 at 0.6 and 240 at 0.8. About 8,000 is comfortable. So 0.8 is sound at 100,000 and 0.6 is already the limit at 32,000; a reserve in tokens is the same rule at every size (L3: 20,000 to 30,000 would have meant one fold in S7, not two). *The risks:* the request comes only at a turn's end, so one library-heavy turn can cross the margin first (whole chapters ran 7,500 and 11,000 tokens in S5); on overflow the first thing dropped is the last handover note, without a word; the count is an estimate (F10); a reply that spends its 4,096 tokens returns no note. *On the other side:* each fold puts a note in place of the conversation, and the notes on record are uneven (F13); that argues for fewer folds where there is room.

**3. The turn budget is a blocker; at least double it, and for the watcher.** *For:* F6, F7. The most any turn tried was 12 calls (S5), 11 (S6), 10 (S7), so sixteen covers every case seen. *Against size alone:* S5's extra calls would all have been refused orders; freeing `stand_by` and `journal` covers S7 but for one order; S6 wanted reads uncounted or a way to a next sample. *The watcher:* not seen; never over four counted calls. *Adds:* the budget can refuse `opt_out`; a fold does not renew it; nothing is logged; F8.

**4. No restarts, since the handover compacts in the game; reconnecting and the reseat limit remain.** *For:* S7. *Against:* S5's compaction was a `hand_over`, a restart of the runner and the only reseat (F13); S6 had none; S7 ended in a stall. The frictions are confirmed (F20).

**5. A Claude Desktop session put calls through in the local model's place.** *For:* F19, to the entry. *Adds:* the heave-to and the final handover note stand as Qwen's; nothing in the log or the save's fields shows it; V1a's cure is a key issued with each seating and a bridge that resets when refused.

## 6. Where the notes are wrong, overstated or misplaced

- **Item 21** says a turn ends on `say` or `answer`: at the runner's door `answer` never ended one and there is no `say`; `say` ends a turn at the MCP door only (V1a).
- **Item 17:** one of six urgent aback lines was the calm's; five were real.
- **Item 18, the model's comment:** a wind floor would not have stopped S7's 31 lines in 8 to 11 knots.
- **The model's "about 4½ hours" a boat trip:** four trips of about two.
- **The model's "the noon latitude" worked well:** not at S5's noon; in S7 it exposed an error nobody applied.
- **The model's "drill stand-by carried into the station":** not seen at this door; V1a traces it to a loaded save's stand-by.
- **The local notes** are weighed in section 5: "smooth", "same for the watcher", "did not occur" and "figures matched reality" each need qualifying.

## 7. Where the readers disagree

1. **The turn budget: its size, or its wording and what it counts?** L3: sixteen covers all four of S7's turns; so would freeing `stand_by` and `journal`. L2: the harm is that reads, `stand_by` and `journal` are counted, with no renewal at a fold and no route to a next sample; S6's plain errors came from lateness. L1: sixteen "would mostly have bought more of the same refused orders", and the harm came through the "Not run" words. V1a: it is the blocker described. Checked in the transcripts: S5's four turns tried 12, 8, 12 and 10 calls. Sixteen would have run them all, each further one a refusal, and would have shown Gemma no "Not run" text. So each reading is right for its own model: size alone mends the Qwen games; in Gemma's a larger number hides the trigger without curing the loop of refused orders. No reader says a larger budget does harm.
2. **How large the Ollama conversations were.** L1: about 21,500 tokens (first seating) and 27,700 plus some thousands (second). L2: 30,000 to 50,000. V1a, from the checkpoints: 72,400 (S5's second seating) and 66,400 (S6). The dumps hold no samples, so I could not re-measure. L1 and L2 call theirs estimates without the samples' log lines; V1a's stands. L1's remark that neither seating "came near" 60,000 fails for the second.
3. **Whether Ollama cut those conversations.** V1a: "the server cut the conversation unseen" (the documented mechanism). L1 and L2 saw no sign of loss. Not settled; the saves cannot show it.
4. **Vessels at a fixed distance.** L1 supports it (the pilot cutter); L3 reads the brig's steady "two miles" as coarse estimates of a real crossing. Different vessels; both stand.
5. **Which erred at noon.** In S5 the sight; in S7 the account. No contradiction: in neither was the sight applied.

## 8. The captain's words worth keeping

1. S6 8505: "if any order you seek falls outside your authority I'll allow it, so feel free. If at all possible, quick's the word and sharp's the action".
2. S6 16942: "The world doesn't stop while you're thinking, so if you can help it, try first, and think later."
3. S7 8445: "anything you read you'll want to journal about right away with the key takeaways, then shelve the book ... you can request them by trying them and I'll approve as necessary".
4. S7 28985: "did the harness inform you to do the handover, or did you choose to do it, thinking the context was probably getting full?"
5. S7 28589: "If you ever need to see your earlier journals verbatim, I can show them at any time".
6. S7 29057: "We should be pretty well set to voyage indefinitely like this, and that's the main thing I was worried about."
7. S7 36963: "watch out for conditional stand-bys that might not trigger."
8. S5 12528, a standing order used as a messenger: `at the pilot off then tell the officer the pilot has been put off, please inform the captain and carry on as we were.`
9. W 216724: "the handover is the specific term for the Officer station. You may journal instead, then opt out as you please and the game will be saved."

## 9. What the officers asked for or suggested

- Gemma asked for nothing; its runaway tables try to stand by for a list of events at once (9223).
- S6 868: "I'll stand by for the boat's return, the glass, and any change in the wind or weather", over one catch-all call.
- S6 11645, of the course the game shaped: "that's not a course I'll steer out of Carrick Road."
- S6, consent (00:48): "Exit is absolute and first"; consent "to this party only".
- S7 28996: "I would have done it on my own judgment at that length ... to keep the fold in my own words".
- S7 93189: "The standing order is drafted and ready in my rank ("the mate"); the tool budget closed before it ran."
- The hand at the bridge, 112613: "FIRST THING ON RESUMING: anchor here (this needs the captain's word, "you may come to an anchor"), or fill away and claw off north".
- W 216799: "The handover tool sits with the officer's station, not mine".

## 10. The models as officers

**Gemma** was two officers. With a conversation full of refused orders and its own tables it could not get a cutter under way or out of a heave-to, and claimed work never done. In a clean conversation it obeyed about sail promptly and answered in voice, but reported nothing unasked, stood by to bells, turned her 90° in pilot waters without a word, and wrote thin notes with a wrong fact in each. The "Not run" wording, the frigate's vocabulary and the unbounded bell stand-by were the game's.

**Qwen under Ollama** was courteous, candid about the cargo, honest about the budget and its own error, and kept inside its grants. It kept a lookout's watch: five orders in 9½ hours, three of them countered. Its worst acts landed late through no rule of its making, but `steer WSW` and the stand-by for a departed pilot were its own.

**Qwen under llama.cpp** was the steadiest: exact about the division of labour, quick to learn the grammar, sound on sail, right about the noon error, author of a well-made standing order. It mistook standing by for keeping a watch, never navigated, and said nothing of a lee shore in fog. The catch-all stand-by, the silent reply cap and a pause that leaves the deck with a silent station were the game's.

**As a watcher** it was true, late, and asleep to its own post.

## 11. Numbers

| | S5 | S6 | S7 (local; MCP hand apart) | W |
|---|---|---|---|---|
| Orders: taken / ship or grammar / deck or domain / not run | 36 / 24 / 4 / 10 | 5 / 0 / 1 / 1 | 21 / 4 / 3 / 1; MCP 2 / 0 / 1 / 0 | 2 tool calls refused |
| Allowances typed; used; never used | 6; 3; 3 | 8 (a ninth rejected); 4; 3, and "weigh" tried, not run | 14 (13 distinct); 2, and 1 by the MCP hand; 10 | none |
| Stand-bys taken; longest under way | 42; 3 h 31 m | 25, 2 more not run; 88 m | 58, 7 more not run, MCP 2; 3 h 50 m | 7; 88 m |
| Wakes: all; the captain's; notable or bell; urgent (the rest named events or intervals) | 42; 20; 14; 3 | 25; 6; 18; 0 | 58; 16; 34; 1 | 7; 4; 1; 2 |
| Nudges (true, false); pauses | 2 (1, 1); 0 | 2 (2, 0); 0 | 1 (1, 0); 1 | none |
| Budget-hit turns; calls not run | 4; 10 | 1; 3 | 4; 10 | none |
| Malformed, empty or cut replies | 5 (3 at the reply cap) | 0 | 4 empty, 1 cut | 0 |
| Handover notes | 2, `hand_over` at the captain's word | 1, the same | 2, `handover_note` at the harness's request; 1 MCP `hand_over` | 2 refused |
| The captain's refusals; standing orders' | 16; 9 | 4; 0 (6 holds) | 9; 145 (5 holds) | not counted |
| Wind-shift lines; urgent aback | 53; 3 | 2; 0 | 40; 1 | 44; 2 |

Across the three cutter games: 28 allowances, 9 used by the seated model; 23 calls not run in 9 turns; 5 nudges and 1 pause; the clock eased to 1x 79 times (26, 13, 40); 4 boat trips of 2 h 01 m to 2 h 09 m.

## 12. What worked well

- The harness's request for a handover note at a known context, the fold, and the model's exact account of both (S7, twice).
- The runner's served form (43 of 43 in S6; 47 of 47 in S5's second seating); "while your call was on its way" wakings lost nothing.
- Refusals whose words gave the cure: "gives standing orders in his own rank, the mate"; "say 'brail up the main sail' or 'take in the main sail'".
- An officer's own standing order, "trim by the wind", guarded "if she is not hove to", fired six times.
- A reseat that carried the allowances and the book whole (S5); two stations through two doors at once (W: "the first test passes", 207900).
- Consent: the token honoured absolutely; a new file name asked afresh; the re-ask on exactly the changed sections.
