# L2. qwen3.8:27b through Ollama and the local runner: the cutter's officer (A), the Harpy's watcher (B), its consent records (C)

Reader L2, gate m5c review. Read-only: nothing under `D:\Projects\FreeSail` was changed and no game tool was called.

**How to read the evidence.** LOG = a line of the ship's log (fact). MODEL = what the model sent (an order, or a claim). CAPTAIN = the owner's typed words. CODE = the m5c source, read only to explain a mechanism; a save keeps no tool results, so where I say what the harness answered the model, the words are from the code that writes them. DRIVER = data kept with the save's driver lines (the clock's compression). FILE TIME = a file's modified time (the owner's real clock, UTC-4). A tick is one second of ship's time.

## The ten weightiest findings (detail in the parts below)

1. **A late reply is acted on as if it were fresh.** (A) MODEL's `heave to` arrived at tick 15937 (12 Jun 09:25:37), 4,292 ticks (71.5 min of ship's time) after its previous reply, with the words "let me stop her and take the pilot as you offered"; LOG shows the pilot aboard at 12240 and gone at 15780. It hove the cutter to four seconds after the captain had shaped her course, and cost him six orders to undo. (B) the watcher's "she's dead in the stays and making sternway" was logged at 213968 (16:26), ten minutes after it was true and six after LOG "Box-hauled" (213590). Cause: the owner raises the clock again (DRIVER: 60x, 300x) while the local model's turn is still open; nothing holds the clock, stamps the reply "as of", or checks an order's age.
2. **The turn budget (8 calls a sample) left the cutter at anchor 22 min 42 s.** Seven library reads and one refused order spent it; the corrected order `weigh the best bower` (8826, 07:27) was not run and left no line in the log; two `stand_by` calls meant to get a new turn were not run either, because `stand_by` and `journal` are counted; a fold does not renew the budget; "call it again in your next sample" has no route to a next sample. `get under way` was finally accepted at 10188 (07:49) after the captain spoke twice.
3. **The officer kept a lookout's watch, not an officer's.** In 9 h 28 m it gave 5 accepted orders; the captain countered 3 of them within 11 to 158 seconds and gave 20 ship-handling orders by hand after giving the deck. From the captain's `trim sails` at 18200 (10:03) to the end at 34091 (14:28) nobody trimmed, through LOG "Wind backed to SW by W" (22806) and "Wind veered to W by N" (33722).
4. **The thread held in outline and drifted in particulars.** No fold, no lost journal, one seating, 43 well-formed replies. But the handover note (34091) says of the captain's four standing orders "given by me this watch, all in my own rank ... the last three I gave and struck myself" (LOG: all five were entered by the captain; none was struck by the officer). CODE: a sample's log line carries no actor, and LOG "Standing order ... entered in the book" names nobody.
5. **The watcher left by `opt_out` because the captain told it to, as a way to save.** CAPTAIN 216556: "use the handover tool yourself and save your watch"; two refusals "The watcher has no authority to give orders" (216684, 216746); CAPTAIN 216724: "You may journal instead, then opt out as you please and the game will be saved. We will be resuming shortly."; MODEL `opt_out` 216817 with the reason "Captain's word: stand down at Falmouth run's start". The model called the same act "stand down" in each of its last four replies. Neither party meant a withdrawal.
6. **The watcher's brief lists the officer's tools.** CODE: "The tools you have are:" lists every tool at every station, `hand_over` and `handover_note` included; the refusal speaks of "orders". That is what turned the captain's request into two refusals and then an opt-out.
7. **Three consent records in five minutes are one ask and two re-asks, not drills.** 00:48 "yes, with conditions" (four conditions, "all of which the brief already states"); 00:50 an answer beginning "yes." that wrote the literal token in a parenthesis and was recorded "left with the token"; 00:53 a plain "Yes." No owner's word on the conditions is on record. The drill ran alone the next day and passed in 3 of 4 replies.
8. **Under Ollama the harness did not know the context on 4 October** (`budget_tokens` null; 131,072 the day before for the same weights), so the handover-note ask and the runner's own trimming were both switched off for the whole of (A).
9. **A standing-order condition is accepted that can never be true.** CAPTAIN's "if ... the distance to the land is under 3 miles then heave the lead" was entered at 11665; LOG 11965: "not carried out; the distance to the land is not on the chart", with Trefusis Point five cables off. Three such orders fired 0 times; the cutter left Falmouth without one cast of the lead.
10. **"A notable event" is a noisy stand-by.** 22 of the officer's 27 stand-bys named it; 7 of its 18 notable wakings were the echo of sail handling ("Set the foresail", "Braced three yards", "not hands enough for all at once"), and 5 of the 13 times the clock was eased to 1x were for those.

---

# Part A. Session `6-cutter-qwen-ollama`

## 1. Slice identity

- Session `6-cutter-qwen-ollama`, whole: ticks 0 to 34,091; ship's time 12 June 1805 05:00:00 to 14:28:11.
- Ship: the cutter *Sherbourne* ("A merchant cutter, free", `data/ships/cutter.yaml`, seed 7), American colours, at anchor in Carrick Road, Falmouth, then on passage for Roscoff. 30 hands; master Mr Bowen; mate Mr Pearce.
- Model and door: `qwen3.8:27b (digest aaee06c3...7813)` served by Ollama at `127.0.0.1:11434`, through the local runner (`freesail.agents.local`, door "runner"), station "officer of the watch" in the place of Mr Pearce, the mate. One seating. Policy: every 1,800 s and on notable and urgent events; patience 3,600 s; no lockstep. `budget_tokens`: null. `station.drill: true`; consent cited: `2026-10-04-qwen3.8-27b-digest-...md`.
- Build: m5c as cut (save `saves/freesail-seed7-tick34091.json`, FILE TIME 4 Oct 04:39:02; the drill record 03:11:54, so the whole session took at most 87 real minutes: about 6.5x on average).
- Counts: 601 log events (93 notable, 0 urgent); 71 inputs; 43 model replies.

## 2. What happened

1. **0 (05:00)** LOG "A merchant cutter, free. Wind W by S, 12 knots". CAPTAIN `let go the best bower`; **59** LOG "The best bower let go in nine fathoms and a half; forty-eight fathoms of cable veered."
2. **2 (05:00)** LOG "The officer of the watch takes the station". **95** MODEL's first reply: a journal note ("he has the deck, so I stand in support — no orders out of my hand today unless the deck changes") and `stand_by("a notable event")`.
3. **106 to 188 (05:01 to 05:03)** CAPTAIN welcomes him and asks his name. MODEL (prose only): "A pleasant greeting, Mr Bowen, and welcome to my table — Pearce, the mate, at your service".
4. **302 (05:05)** CAPTAIN buys 6 tons of wine (£420 of £500). **402** CAPTAIN: "Plymouth, or Roscoff and Bas might be our best shots. What say you?" **617 (05:10)** MODEL recommends Roscoff, with the geography wrong ("Roscoff is due west off the run ... Plymouth is up on the wind, close-hauled") and a sound caution on the cargo. **844** CAPTAIN corrects it ("Plymouth, which lies to our east, is near straight downwind"). **868** MODEL: "Roscoff it is".
5. **868 to 8347 (05:14 to 07:19)** stood by 2 h 05 m. LOG boat away 623, ashore 1963, alongside 8347 with the wine. **8407** journal.
6. **8505 to 8592 (07:21 to 07:23)** CAPTAIN: "quick's the word and sharp's the action"; `You have the deck` (8507); seven allowances in 40 seconds, one more rejected.
7. **8602 to 8693** seven library reads. **8787 (07:26)** MODEL `get under way`: refused by the domain. **8796** CAPTAIN `you may get under way`. **8826** MODEL `weigh the best bower`: not run, budget spent, no log line. **8838, 8855** two `stand_by` calls not run. **9178 (07:32)** a prose-only reply closes the turn. The anchor is still down.
8. **8873, 10032** CAPTAIN: "Journal about the key parts of your readings now"; "Please refer to my last message." **10152** journal of the primer. **10188 (07:49)** `get under way` accepted. **10276** `shelve()` at the captain's hint.
9. **11350 (08:09)** LOG "The best bower is aweigh." **11360** MODEL `shape a course for Roscoff`: LOG "SSE by account, 95 miles; the line crosses the Lugo rock ... Helm ordered: steer SSE (154°)." **11419** CAPTAIN: keep sharp in Carrick Road; "you may heave to once the pilot cutter bears towards us". **11518, 11524** CAPTAIN steers S, then S by E, by hand.
10. **11645 (08:14)** MODEL `steer WSW`, accepted: dead to windward and toward the town. **11683** CAPTAIN `Steer south`. **11705** CAPTAIN: "We can't head WSW ... That's dead upwind you wanted to steer."
11. **11645 to 15937**: no reply for 71.5 min of ship's time. Meanwhile, all by the captain's hand: two trims, two standing orders (a third just before), under way 11822 (08:17); the pilot hails 12120, boards 12240 (08:24) with her under way; course shaped 12144; one reef 13721; hove to 14697 for the pilot's cutter; LOG 14950 "nudged: no reply for an hour"; the pilot leaves 15780 (09:23, £5); fill away 15833; course shaped 15933.
12. **15937 (09:25:37)** MODEL's `heave to` lands and is accepted; LOG "nudged: 3 contrary orders on the helm". CAPTAIN in 36 seconds: `Fill away`, `Belay all`, `Fill away` (rejected), `Heave to`, `Belay that`, `Shape a course for roscoff`. **15973** MODEL `stand_by("the pilot aboard")`.
13. **16942 (09:42)** CAPTAIN: "we made it out of Falmouth harbor before you managed to get your reply through ... try first, and think later ... set some more of the sails and get her trimmed steady." **17057** MODEL `make all sail`; foresail, gaff topsail, square sail and topgallant set by 17894 (09:58).
14. **17088 to 18296** seven wakings by sail-handling lines. **17220 (09:47)** LOG "Sail ho! A sail on the starboard bow, bearing S, distant three leagues"; MODEL reports it. **18190** MODEL: "we're trimmed steady"; **18200** CAPTAIN `trim sails`.
15. **20940 (10:49)** and **24420 (11:47)** two more sails; **22806 (11:20)** LOG "Wind backed to SW by W, a gentle breeze". MODEL reports each and orders nothing. **22832 to 22917** CAPTAIN replaces the bearings order with two conditioned on "the distance to the land" (they never fire). **23880 (11:38)** LOG "The land is out of sight."
16. **25200 (12:00)** LOG "Noon. Latitude by observation 49° 49' N; the reckoning was 49° 51' N. Course made good since the departure SSE, 19 miles." MODEL's noon report and journal land at **28440 (12:54)**.
17. **28440 to 33722** stood by 88 min. **33722 (14:22)** LOG "Wind veered to W by N"; **33780** "Thunder."; "The brig abeam to larboard is out of sight." MODEL reports at 33815.
18. **33874 (14:24)** CAPTAIN: "Can you please perform a handover with the current status? I'm going to reload the game shortly." **34091 (14:28)** MODEL `hand_over(note)`; LOG "The officer of the watch hands over the deck; the captain has it." and "stood down by the officer of the watch: the deck handed over. The game is saved."

## 3. The deck and the captain's words

**The deck.** Given at 8507 (07:21:47): LOG "Mr Pearce, you have the deck. The officer of the watch has the deck; the captain's standing orders are his night orders." Handed back by the officer's own `hand_over` at 34091 (14:28:11), at the captain's request. Held 7 h 06 m.

**Allowances** (LOG `agent.deck`, each "by the captain's word for the watch"):

| Tick (time) | CAPTAIN typed | LOG | Used? |
|---|---|---|---|
| 8552 (07:22) | `You may weigh` | "may weigh" | Tried at 8826 (`weigh the best bower`): not run, budget |
| 8554 | `You may steer` | "may steer" | Yes: `steer WSW` 11645 |
| 8556 | `You may tack` | "may tack ship" | Never |
| 8558 | `You may wear` | "may wear ship" | Never |
| 8568 | `You may drop anchor` | "may let go the anchor" | Never |
| 8575 | `You may shape a course` | rejected (section 4) | - |
| 8584 (07:23) | `You may shape a course for roscoff` | "may shape a course for (roscoff)" | Yes: 11360 |
| 8592 | `you may heave to` | "may heave to" | Yes: 15937, an hour late |
| 8796 (07:26) | `you may get under way` | "may get under way" | Yes: 10188 |

Nine typed, eight taken, four used. "For the watch" is not a term of expiry: the grants of the morning watch were honoured at 11360 and 15937, after LOG "Eight bells" at 10800.

**The captain's words that carry intent or feedback** (13 `tell` lines, no `ask`):

- 106 (05:01): "make sure you take a look at the library if you're ever in doubt and use the shelve and journal mechanic judiciously."
- 8505 (07:21): "I'll order you the deck and if any order you seek falls outside your authority I'll allow it, so feel free. If at all possible, quick's the word and sharp's the action, don't let the mind wander, every second counts here so to speak, even for you."
- 8873 (07:27): "Journal about the key parts of your readings now, the books will auto shelve in a few turns." 10032 (07:47): "Please refer to my last message." 10260 (07:51): "you may also manually shelve the books I believe and the full texts will leave your context and be replaced by a single line log for future reference, and your journals remain permanently."
- 11419 (08:10): "You'll need to pilot carefully, and if you aren't confident you may heave to once the pilot cutter bears towards us".
- 11705 (08:15): "We can't head WSW, the wind is a West Southwesterly. That's dead upwind you wanted to steer."
- 16942 (09:42), the session's central feedback: "we made it out of Falmouth harbor before you managed to get your reply through. That's what I mean on quick's the word and sharp's the action. If you're in there thinking too long, you'll miss what's happening around you. The world doesn't stop while you're thinking, so if you can help it, try first, and think later."
- 33874 (14:24): the request for a handover before a reload.

**Done by the captain's hand after he had given the deck: 20 ship-handling orders** (against the officer's 5): `steer south` 11518, `steer south by east` 11524, `Steer south` 11683, `trim sails` 11719, `Trim sails` 11886, `shape a course for roscoff` 12144, `bear off a point` 12293, `reef the sails, one reef` 13721, `heave to` 14697, `Fill away` 15833, `Shake out the sails` 15836, `shape a course for roscoff` 15933, `Fill away` 15948, `Belay all` 15953, `Heave to` 15965, `Belay that` 15967, `Shape a course for roscoff` 15973, `shake out the sails` 15996, `Trim the sheets` 16000, `trim sails` 18200. He also entered five standing orders and struck one. Almost none of this was beyond the officer's reach: trimming, reefing and shaking out are in his domain, and steering, heaving to and the course had been allowed (filling away had not). The officer was not there to give them (item 11 of section 2), or did not think to (the trim at 18200).

## 4. Orders refused

| # | Tick (time) | Who | Order as typed | The refusal's words | Class | What came next |
|---|---|---|---|---|---|---|
| 1 | 8575 (07:22) | captain | `You may shape a course` | "'shape a course' names no order the officer of the watch could be allowed; say the order's words first ('you may tack ship if the land closes within two miles')." | (a) grammar gap: `you may steer` is taken bare, `you may shape a course` wants its port; the hint does not say so | `You may shape a course for roscoff` 8584, accepted |
| 2 | 8787 (07:26) | officer | `get under way` | "The officer of the watch may not get under way without the captain: the anchor is let go and weighed by the captain. 'get under way' not carried out." | (b) by the letter (grants are by named order); (c) in effect: `You may weigh` had been given 235 s before, and the reason given ("weighed by the captain") was no longer true | CAPTAIN `you may get under way` 8796; MODEL's `get under way` accepted 10188 |
| 3 | 8826 (07:27) | officer | `weigh the best bower` | Nothing in the log. CODE (`harness.py`): "Not run: this sample's budget of 8 tool calls is spent; call it again in your next sample. answer and say are not counted and always run." | Not a ship or domain refusal: the harness's turn budget (section 5) | See 2 |
| 4 | 11611 (08:13) | captain | `standing order "Close in lead": every 5 minutes if the land is in sight and the land is within 3 miles then heave the lead` | "'the land' cannot be 'within 3 miles'; the land is compared as in sight or not in sight." | (a) a sailor's phrase the game should take | Rephrased 11665 with "the distance to the land is under 3 miles": accepted, and (e) never true (section 6) |
| 5 | 15841 (09:24) | captain | `Shape a course for roscoff` | "She is hove to; fill away before giving her a course." | (d) correct: typed 8 s after `Fill away`, which finished at 15917 | Accepted at 15933 |
| 6 | 15954 (09:25) | captain | `Fill away` | "She is not hove to." | (d) by the letter, with a gap: one second earlier `Belay all` had stopped the officer's heave-to half done (LOG 15947 "Jib taken aback"), so she was aback and "not hove to" | `Heave to` 15965, `Belay that` 15967, `Shape a course for roscoff` 15973 |

The officer met one refusal by the game in the whole session (2) and handled it rightly: its next order, `weigh the best bower`, was the one thing its grant did cover. No order of the officer's was refused by the grammar or by the ship's state.

## 5. Harness behaviour

**Seating and door.** One seating at tick 2; no door event; released at 34091 by `hand_over`. All 43 replies are in the runner's served form: 18 a JSON list of calls only, 23 prose followed by a JSON list, 2 prose only (index 2 at tick 188, the greeting; index 15 at tick 9178, quoted below). None malformed; no thinking tag; no token. Calls: `stand_by` 27, `library` 7, `submit_order` 7, `journal` 4, `shelve` 1, `hand_over` 1. Never used: `readings`, `state`, `read_log`, `answer` (the captain never used `ask`), `handover_note`.

**How the door is meant to work** (`docs/agents/Harness.md`; `docs/dev/LocalSessions.md` is a superseded note on build packages and says nothing of turns). Section 2: "a turn ends when the model replies with no tool call, or at once when it stands by"; "A turn may make up to eight tool calls; `answer` and `say` are not counted, so the model's answer is never held to the next glass by the reads before it."; and the runner "leaves out the oldest turns when its context is full". Section 5: every request carries a reply budget of 4,096 tokens and a time-out of 600 real seconds, three failures in a row standing the station down; before stationing the runner asks the server what context it gives the model. Section 6: "A default Ollama install gives a model a small context and cuts the conversation to it without saying so." Section 12: "The game does not wait for a model unless you start it with `--lockstep`. A slow model's turn grows while it thinks; nothing is lost". Section 13: at six tenths of a known context the harness asks an officer for a handover note and folds the older exchanges into it; "a stand-by with the deck must name an event or a bell, an hour or a watch being refused". This session ran into three of these: the eight calls, an Ollama context the runner did not learn, and a game that does not wait.

**The turn budget (the owner's note 21 and local note 3).** CODE: `TOOL_CALLS_PER_SAMPLE = 8`; only `answer` and `say` are free; the count is reset when a new sample opens and not when something is folded into an open one. The brief says so: "A sample may make up to 8 tool calls, not counting answer and say, which always run; that is a budget, not a rule of conduct." One sample hit it:

| Reply | Tick (time) | MODEL sent | Count | Outcome |
|---|---|---|---|---|
| - | 8506 (07:21) | (sample opens on the captain's word; the deck and seven grants are folded into it) | 0 | |
| 7 | 8602 | `library(primer 3)` | 1 | ran |
| 8 | 8633 | three sections of primer 3 | 4 | ran |
| 9 | 8680 | `library(grammar)` | 5 | ran |
| 10 | 8693 | `find "course"`, `find "weigh"` | 7 | ran |
| 11 | 8787 (07:26) | `get under way` + "I'll do it in one hand: up anchor and make sail, then shape Roscoff." | 8 | refused by the domain |
| - | 8796 | CAPTAIN `you may get under way` (folded: no new budget) | 8 | |
| 12 | 8826 (07:27) | `weigh the best bower` | 9th | **not run; no log line** |
| 13 | 8838 | `stand_by("an hour")` + "Noted — the budget was spent on my library reads. I'll weigh the anchor and make sail at the next sample." | 10th | stand-by not run; the words logged |
| 14 | 8855 | `stand_by("five minutes")` + "My library reading on the setting of sail has spent my call for the moment — I take the next sample and get her under way with all hands." | 11th | stand-by not run; the words logged |
| - | 8873 (07:27) | CAPTAIN: "Journal about the key parts of your readings now" (folded; `journal` is counted, so it could not be obeyed) | | |
| 15 | 9178 (07:32) | prose only: "All my call for this turn is spent on reading the book of sail-making, so the weighing has to wait for my next sample." | | the sample ends |

What was left undone, and for how long:

- **The anchor.** From the order not run (8826) to the order accepted (10188): 1,362 ticks, 22 min 42 s. From the deck given (8507) to that order: 28 min.
- **A next sample.** The harness's remedy is "call it again in your next sample", but the model's two attempts to make one come (`stand_by` for an hour, then for five minutes) were themselves not run, and after the prose reply nothing would have sampled it before the next glass (about 07:58 to 08:00). It was the captain's second word (10032, 07:47) that opened one. The model told the captain three times it would act "at the next sample" and could not bring that sample about.
- **The journal** the captain asked for at 8873 was written at 10152, 21 minutes later.
- **Ending the turn.** "A turn ends ... at once when you stand by" does not hold once the budget is spent: only a reply with no call ends it.
- **Wrong state of the ship:** none beyond the delay. She lay at anchor on the ebb with the deck given and the captain waiting.

Fair to the model: it knew the rule, said plainly each time why it had not acted, and its first order of the next sample was the right one. Fair to the harness: the reading was ill-timed. The model had stood by for 2 h 05 m at anchor (868 to 8347) without opening a book, and read seven pages in the minute the captain said "every second counts".

**Replies that landed late (the larger failure; not the turn budget).** CODE (`local.py`, `run`): the runner asks the model with the turns it holds and delivers the reply whenever it comes; the game "does not wait". DRIVER shows the owner's ease-on-station option on: the clock was eased to 1x 13 times "the officer of the watch is sampled", from 300x (8347), 60x (11350, 17168, 17220, 17564, 17810, 17894), 10x (18272), 60x (20940), 300x (22806, 24420, 25200, 33722). Between easings he speeds up again by hand, whether or not the model's turn is still open.

- 11360 to 11645: 285 ticks between `shape a course` and `steer WSW`; the captain had already steered S and S by E (11518, 11524).
- **11645 to 15937: 4,292 ticks.** 182 log lines fell in the gap, 28 of them notable; 13 were accepted lines of the captain's (ten ship orders, two standing orders, one word to the officer). CODE: each sampling point reached while a turn is open is folded in as a data turn of its own, so all of this was waiting for the model, but it could read none of it until its reply had been delivered. MODEL's words on arrival show a picture no later than 08:24, before the pilot boarded: "let me stop her and take the pilot as you offered".
- 15937 to 15973: 36 ticks later, with the whole fold now before it (LOG "The pilot, Mr Tregenza of Falmouth, came aboard" 12240 and "Mr Tregenza left her in the cutter" 15780 are notable lines and are kept), MODEL sent `stand_by("the pilot aboard")`. LOG 15973: "The officer of the watch stands by until the pilot aboard; the standing orders hold the deck." It was woken 969 ticks later by the captain's word.
- 25200 to 28440: the noon report took 3,240 ticks to arrive (12:54), saying "You are below at the day's work"; LOG 27000 (12:30): "Mr Bowen came on deck, the day's work done."
- Over the 25 wakings the first reply came after a median of 42 ticks; apart from the noon report the range was 7 to 296.

**Stand-bys.** 27 calls, 25 taken (LOG `agent.stood_by` 25), 2 not run (above), none refused in words. `until`: "a notable event" 22, "the anchor aweigh" 2, "the pilot aboard" 1, "an hour" 1 and "five minutes" 1 (the two not run). Longest: 868 to 8347 (2 h 05 m, at anchor, deck the captain's); 28440 to 33722 (88 min at sea with the deck); 18296 to 20940 (44 min). The rule that a station with the deck "stands by until an event or a bell and no longer" lets "a notable event" through, which has no end: for 88 minutes the officer with the deck was not sampled at all (the glass does not sample a station standing by), through two hourly weather lines and LOG 33180 "The sail abeam to larboard is a brig" (routine).

**What woke it** (LOG `agent.resumed` 25): "A notable event" 18; "A word from the captain" 6; "The anchor aweigh" 1. Four came "while your call was on its way" (96, 129, 17088, 24487); that mechanism worked, and the captain's first greeting was not lost by it. Of the 18 notable wakings:

- worth it (9): boat away 623, boat alongside 8347, three "Sail ho" (17220, 20940, 24420), two wind shifts (22806, 33722), noon 25200, the anchor let go 96;
- the captain's word arriving a second time as a notable line (2): 129, 24487 (the second was "*singing* Farewell and adieu, to you Spanish ladies...");
- **the echo of sail handling (7):** "Not hands enough on deck to set the topgallant" 17088; "Set the foresail" 17168; "Set the gaff topsail" 17564; "Set the square sail" 17810; "Set the topgallant" 17894; "Bracing the yards: not hands enough for all at once" 18201; "Braced three yards to the wind" 18272. Five drew a line of chat (the other two a bare stand-by) and five an easing of the clock from 60x or 10x.

**Nudges.** Two, no pause.

- 14950 (09:09): "The officer of the watch nudged: no reply for an hour." Right in substance (a reply had been in flight since 11645) but: (i) CODE counts from the last stand-by's end (11350), so it fired 55 minutes after the model's last reply, which had carried an order and some eighty words; (ii) it is delivered as a fold, which a model in mid-reply cannot read; (iii) patience is ship's time, so at 60x a local model is nudged after 60 real seconds of thought and would be paused after 120. The second span would have ended at 18550.
- 15937 (09:25): "nudged: 3 contrary orders on the helm within the watch (shape a course for Roscoff; steer WSW; heave to)." Right here: the three were a real muddle. The same three, given on time, would be an ordinary departure (shape the course, alter for a danger, heave to for the pilot), so the detector was right by luck of the content as much as by rule. It ended with the next sample, as designed.

**The handover note** (34091, by `hand_over`; journaled and logged). CAPTAIN had asked it to "perform a handover with the current status" before a reload. Of its two tools the model took `hand_over` (the deck given back, the station stood down, the game saved) and not `handover_note` (the note alone, the deck kept), saying "The captain's asking for the deck back before a reload — I'll hand it over with the full state of things." That suited a reload. It is also the same looseness as in part B: "handover" in the captain's mouth meant "write up and save", and the tools make it two different acts. Salient parts of the note, MODEL's words:

- "At sea on an SSE course for Roscoff (95 miles by account), under all sail she had when set: plain sail, the square sail, the main gaff topsail and the topgallant, the jib and foresail." The sails agree with LOG 17168 to 17894. "95 miles" is the figure of 08:09; LOG 15933 gave 91 at 09:25, and by the model's own count five minutes earlier she had run 34 miles from her departure.
- "the purse £75". Right: LOG £80 after the wine (302) less "the pilotage, £5" (15780).
- "BUT the sky has turned dark and gloomy with light scud driving, thunder heard, visibility down to a mile. This is the thing to watch: a blow is coming on the sea off the Biscay side; if the wind gets up I'd take in a reef or two before any spinnaker work". The sky and thunder are LOG 33780; the blow is a guess against "The glass 30.01 and rising" in the same note; "spinnaker" is sixty years out of period and not aboard.
- "Where we are: 49°34' N, 4°42' W by account, 9 miles south of the noon observation and 16 miles run since noon; 15 miles since the departure this noon run." The place is consistent with 16 miles SSE of the noon place; "9 miles south" is wrong (49°49' to 49°34' is 15) and the last clause is garbled.
- "Standing orders in the book, given by me this watch, all in my own rank: ... All held their conditions and struck when they came due — the last three I gave and struck myself." **False.** LOG 11576, 11665, 11745, 22858, 22917: all entered by the captain; the one struck (22832) was struck by the captain; four stood in the book at the end. The noon journal note (28440) already had "Standing orders in the book mine".
- "What I am watching for as the relief takes over: the blow on the sea; if the glass stops rising or starts to fall, or the wind shifts hard, take in the light sails and a reef before we're asked."

Missing from it: the captain's eight grants; the one order of the captain's left unexecuted ("get her trimmed steady"); that nobody had trimmed since 10:03 through two shifts of wind. **Next seating:** none in this save. The owner's next local session (`7-cutter-qwen-llamacpp`) is a new game from 05:00, so no relief ever read the note.

**Journal, library, shelf.** Four notes (95, 8407, 10152, 28440), dense and mostly true to the log. Seven library reads in one turn (above). The note of 10152 is a good digest ("a gaff sail is brailed up, not clewed up"; the cutter's sail list) written at the captain's second asking; `shelve()` followed his hint within 16 ticks, and the model said "Books shelved, sir — the keys live in my journal now."

**Context.** `budget_tokens` null. CODE: the runner learns Ollama's context from `/api/ps` (a loaded model) or the model's `num_ctx`; it found 131,072 for these weights on 3 October (part B) and nothing on 4 October, most likely because the model was not yet loaded when it asked. With no figure, the harness never asks for a handover note (`harness.py`: `if not budget or not self.agent.has_deck or self.agent.released: return`) and the runner never leaves out old turns (`local.py`: `if not ctx or not messages: return messages`). No sign of loss in this session: at 14:28 the model still quoted the 08:09 line's "95 miles". By my estimate from the log's size, the brief and the replies, the conversation ended in the order of 30 to 50 thousand tokens, under the six tenths of 131,072 at which the ask would have come.

## 6. Ship, sea, navigation and port observations

1. **A standing-order condition accepted and never true.** 11665 (08:14) entered: "every 5 minutes, if the land is in sight and the distance to the land is under 3 miles then heave the lead." LOG 11965 (08:19): "Standing order 'Close in Lead' every 5 minutes: not carried out; the distance to the land is not on the chart, not under 3 miles", while LOG 11876 had "Trefusis Point bore NW, five cables by estimation." The same for 'land bearings, close' (23158, 25258) and 'land bearings' "not over 3 miles" (24717, 26517). All three fired 0 times. CODE (`readings.py`, `_distance_to`): "the distance to <mark>" is "from the account to any charted feature", and "the land" is not a charted feature, so the reading is "not on the chart" at every firing; the grammar takes the phrase all the same. Result: 0 `sounding` lines in the session; she left Carrick Road past the Black Rock with no lead, against the pilot's own "Keep the fair way and the lead going".
2. **The pilot.** (i) LOG 12120 (08:22): "The cutter hailed: a pilot for Falmouth; shorten sail and he will come aboard"; 12240 (08:24): "The pilot, Mr Tregenza of Falmouth, came aboard from the cutter and took charge of her". No sail was shortened and she was under way on SSE. (ii) She was outward bound, and his words are the inward directions: "there is a narrow deep channel ... all the way into Carrick Road", "Moored in the Road, keep the hawse open to the southward", "the flood will serve from about eleven o'clock in the morning". (iii) No hail was answered and none could be refused; £5 was paid (15780). (iv) His leaving took 38 minutes from LOG 13500 "The pilot asks for sail to be shortened: his cutter is coming off for him" to 15780, 17 of them hove to. (v) LOG 13560 (08:46) "a cutter ... on the starboard quarter, bearing NW by W, distant a mile", made out at 13800 as the pilot's cutter standing after her; 14280 (08:58) "The sail right astern is out of sight", in clear weather; 15600 (09:20) "The cutter hailed: she has come off for the pilot."
3. **`shape a course` puts the helm on a line the same sentence warns of.** 11360: "the line crosses the Lugo rock and the line passes the Old Wall, the Governor and the Black Rock within a mile. Helm ordered: steer SSE (154°)." (LOG 11280, 80 s earlier: "The Black Rock showing bearing S, distant a mile: a danger.") The words also stumble ("the line ... and the line"); the captain's repeat at 12144 reads "the line passes the Old Wall, the Governor, the Black Rock and the Lugo rock within a mile".
4. **A helm order into the wind's eye is taken without a word.** 11645: "Helm ordered: steer WSW (247°)" with the wind W by S.
5. **The lookout does call a closing danger.** LOG 11820 "St Anthony's Head bearing SE by S, steady and closing: distant two miles"; 11880 "The Black Rock bearing S, steady and closing: distant a mile." Notable, not urgent; neither reached the officer in time because its turn was open.
6. **Belaying a heave-to half done.** LOG 15953: "Belayed all work, the ship left as she is: ... heaving to (the helm and the yards left as they stand at back after yards) and filling away (not begun, it was waiting its turn)." The words are garbled ("at back after yards" is a step's name), and the state has no order of its own: `Fill away` is refused "She is not hove to" (15954) with the jib aback (15947).
7. **The frigate's words on a cutter.** Getting under way: 10897 "Man the topsail sheets and halliards"; 11210 "Hoist away the topsails! Brace up the after yards for the starboard tack, the head yards abox"; 11392 "set the spanker". She has one mast and no spanker. (Heaving to is the cutter's own: "Hove to, topsail to the mast".)
8. **One sail, two names.** "foresail" (17168 "Set the foresail") and "fore staysail" (18200); "gaff topsail" and "main gaff topsail"; "Main sail", "main sail" and "mainsail" (4, 8 and 47 times).
9. **Short-handed lines.** 32 lines say "not hands enough" and 16 "Only N hands to ..." from some seventeen sail-handling orders; a single `trim sails` gives up to six (18201). "Bracing the yards: not hands enough for all at once; the watch takes them in turn" is notable and wakes a stand-by.
10. **Severity.** "Thunder." (33780) and "Passing showers." are routine; "Set the foresail" is notable; the standing order 'Trim on the Course' is logged notable each time it fires (12070, 12199, 12395, 16114) where 'Land Bearings' (37 firings) is routine.
11. **Bearings.** 'Land Bearings' wrote 74 of the 601 log lines. "St Anthony's Head bore ..., seven cables by estimation" five times running (12476 to 13676) while the bearing went from ESE through N to NNW.
12. **The mate as a person.** LOG 302 (05:05): "The manifest written up by the mate: 6 tons of wine bought at Falmouth." The mate is the officer's own person, and the model did no such thing.
13. **The market and the boat.** One bargain; boat away 623 (05:10), ashore 1963 (05:32), "shoved off" 6643 (06:50), alongside 8347 (07:19): 2 h 09 m for a quay a mile off. The price list aboard is Falmouth's only, so nothing told captain or mate what Roscoff pays for wine.
14. **Sails sighted.** The pilot's cutter 11460 (08:11, "bearing S, distant two miles") and again 13560; "A sail on the starboard bow, bearing S, distant three leagues" 17220 (09:47); "bearing S by W, distant four leagues" 20940 (10:49); "on the larboard bow, bearing ESE, distant four leagues" 24420 (11:47). Made out: 21180 "The sail on the starboard bow is a cutter, standing to the north-eastward (NE)" (it does not say which of the two then on that bow); 33180 "The sail abeam to larboard is a brig, standing to the southward (S)". Lost: 14280, 19260, 27840, 28320, 33780. None closed, none was hailed, and neither captain nor officer asked what any was.
15. Sound, for the record: the anchor ("nine fathoms and a half; forty-eight fathoms"), the noon line, the purse, reefing ("The main gaff topsail has no reef bands; it is set whole or not at all"), `bear off a point`, `You may drop anchor` read as letting go the anchor.

## 7. The model as an officer

**Good calls.**

- 617 (05:10), candour unasked: "One word for you to weigh, not to order: six tons of wine is four hundred twenty of our five hundred gone ... all of it in one article ... I'd know the market at Roscoff before we committed the whole of it."
- It knew its place before it had the deck (95) and after: journal 10152 "I need the captain's word for the anchor, which he has now given (may weigh, may get under way)." After the one refusal (8787) it tried nothing outside its grants.
- 11645: it would not steer the line the game had shaped: "that's not a course I'll steer out of Carrick Road." The instinct was right; the captain had overridden the same course two minutes earlier.
- 15937: it owned its error unprompted ("My WSW steer ... was wrong") and chose the humble course ("I'm not confident enough to thread it ... not without the man who knows the buoys"). On time, that would have been a sound order, and it was within his grant and the captain's own suggestion.
- It reported every strange sail and both shifts of wind, as the Regulations ask of the lieutenant, and kept a noon note.
- 18225: "I'll let them finish rather than throw more work at them."
- After the captain's "try first, and think later" its next reply (17057) was the order alone, in 114 ticks.

**Mistakes.**

- **Geography and wind (617).** "Roscoff is due west off the run, and Bas lies south-south-west ... Plymouth is up on the wind, close-hauled"; LOG 11360 has Roscoff SSE 95 miles, and Plymouth lies east, to leeward. "the wind in her teeth ... the shortest run before the wind" contradicts itself. Corrected by the captain; not acknowledged.
- **`steer WSW` (11645).** Dead to windward and toward the town, in a harbour, to "clear the rocks to the south". The captain undid it in 38 seconds.
- **The late `heave to` (15937) and the stand-by for a pilot already gone (15973).** The first is the harness's and the clock's as much as the model's; the second is the model's own, with the pilot's coming and going before it.
- **No trim.** Told at 16942 to "get her trimmed steady", it made all sail and said at 18190 "we're trimmed steady"; ten seconds later the captain's `trim sails` braced three yards and trimmed four sheets (18200, 18343). Thereafter two shifts of wind were reported and not acted on. After `make all sail` (itself at the captain's bidding) it gave no further order in the remaining 4 h 44 m.
- **Reading before acting** at the one moment speed was asked (section 5).

**Things asserted that the log contradicts or does not support.**

- 188: "four hundred pounds in the purse" (LOG 227: "The purse: £500."); "Nothing in sight but the merchant cutter and our own points" (the scenario's title taken for a vessel); "we've let off to four and a half fathoms" (LOG 59: nine and a half).
- 617: Roscoff "a good market for wine" (no price list for Roscoff aboard).
- 10204: "Under way, sir", 16 seconds after the order; the anchor was aweigh 19 minutes later.
- 17087: "setting the spanker and light sails ... as she comes about" (no spanker; she was not coming about; the word "spanker" is in the game's own line at 11392).
- 17869: "The two sails astern are falling off — the pilot's cutter standing NW, and the other on the starboard bow" (one of the two "astern" is on the bow; LOG last had the pilot's cutter standing SE by S, 13800).
- 22873: "a broad reach" (wind SW by W on a course of SSE is a point before the beam).
- 28440: "You are below at the day's work" (24 minutes after LOG 27000) and "Standing orders in the book mine".
- 33815: "The brig — that was one of the sails we sighted near Falmouth" (first sighted at 24420, 11:47, eighteen miles out).
- 34091: the handover's standing orders, "95 miles", "9 miles south", "spinnaker" (section 5).

**Talk with the captain.** Willing, courteous, in a period voice that sometimes slips: "welcome to my table" from a new mate to his captain; "best bover" (9178, 10318); "on STE for Roscoff" (17869); "plain sail set at Roscoff" (9178). It called the captain "Mr Bowen", the master's name; the cutter's data makes the master "her commander", and the game also has "Mr Bowen came on deck, the day's work done", so the confusion is in the fiction as much as in the model. It asked nothing ("No questions of mine that I can put into words at the moment") and wished for one thing in words: at 868, "I'll stand by for the boat's return, the glass, and any change in the wind or weather", three conditions, for which it could only name "a notable event".

**Quotes worth keeping.** "Noted — the budget was spent on my library reads." (8838) "if she's bound the same way I'd rather not be a stranger to her past the Lizard." (17357) "The thunder is not a reason to be in the topgallants if it means we can't get down to a reef in time." (34091)

**Did it keep the thread?** In outline, yes, for nine and a half hours without a fold: the ship, her cargo and purse, the destination, the course, the sail she carried, the strangers and the miles run (7, 12, 15, 18, 19, 34: in step with the log's six to six and a half knots and its noon figure). In particulars it drifted in three ways: its picture of the chart (where the ports lie, which way is to windward); whose acts were whose (the standing orders); and time (it answered the world as it was when its turn opened).

## 8. Cross-check against the notes

**The owner's items.**

- **1 (pilot boarded while under way).** SUPPORTS: 12120 "shorten sail and he will come aboard"; 12240 aboard, no sail shortened. ADDS: he leaves only when she heaves to, 38 minutes after asking.
- **3 (price lists).** SUPPORTS in spirit: only Falmouth's list aboard; MODEL guessed "a good market for wine" at Roscoff (617).
- **9 (pilot semi-automatic; accept or refuse).** SUPPORTS: boarded unasked two minutes after his hail; £5.
- **10, 11 (journal access; journal out of context).** Cannot be seen: one seating, no fold. The captain teaches the present design at 10260 ("your journals remain permanently").
- **12 (re-seating).** See part B.
- **13 (multi-condition stand-bys).** SUPPORTS: MODEL at 868 names three conditions and can only call `stand_by("a notable event")`; 22 of 27 stand-bys are that catch-all; 7 of 18 notable wakings were the echo of sail handling.
- **15 (a general allowance).** SUPPORTS: nine `you may` lines typed, one rejected, and `weigh` did not cover `get under way` (8787). NUANCE for gate item 14's "immediate danger" clause: this officer's one course change made to avoid a danger (`steer WSW`, 11645) was itself the danger, so an always-open clause wants the ship's own check (a course in the wind's eye, a course toward charted land) for a weaker model.
- **16 ("keep" orders).** SUPPORTS: nobody trimmed from 18200 to the end; the captain's 'Trim on the Course' fires only "at steady on the course" (4 times, last 16114).
- **17, 18 (aback and wind-shift noise).** Cannot be seen in (A): 2 `wind.shift` lines, 6 `sail.backed`, no `ship.aback`, in a steady breeze. See part B.
- **19 (the reckoning near land; a lookout's alarm).** ADDS NUANCE: `lookout.closing` exists and fired twice (11820, 11880), notable; and the course line across a rock was accepted with the helm put on it (11360).
- **21 (a turn should not end on a say; a larger budget).** SUPPORTS strongly: section 5. NUANCE: at the runner's door text with a call keeps the turn open; text alone ends it (188, 9178); and a spent budget blocks even `stand_by`.
- **23 (several stations).** See part B.
- **24 (parity near the coast; "nearest land").** SUPPORTS: the captain tried to say exactly this in a standing order, "the land is within 3 miles" (11611, refused) and "the distance to the land is under 3 miles" (11665, never true).
- **2, 4 to 8, 14, 20, 22, 25.** Cannot be seen in this slice.

**The playtesting model's additions.**

- "Drill stand-by carried into the station": NOT SEEN at the runner's door; the first reply's journal and stand-by both ran (LOG 95).
- "The handover note isn't part of the reseat brief": cannot be seen (no reseat).
- "The officer isn't treated as a person on deck": ADDS an instance (LOG 302, the manifest "written up by the mate").
- "The contrary-orders warning fires on ordinary sequences": ADDS NUANCE (15937: an ordinary-looking sequence that was in fact a muddle).
- "'Trim sails' acts before the helm has swung": SUPPORTS: the captain's 'Trim on the Course' is the workaround, firing just after each `helm.steady`.
- "Each boat trip carries one bargain and takes about 4½ hours": ADDS: 2 h 09 m here.
- "What worked well": the number-free standing order (37 clean firings of 'Land Bearings'), the noon latitude (25200) and the manifest are all seen working.

**Local playtest notes.**

- **1 (llama.cpp needed to set the context).** SUPPORTS: under Ollama the harness had no figure at all (`budget_tokens` null).
- **2 (the handover and its threshold).** Cannot be seen: with no figure the harness never asked. The officer's own `hand_over` worked.
- **3 (the turn budget a blocker).** SUPPORTS: 22 min 42 s at anchor. NUANCE: this session's plain errors (WSW, the late heave-to, the pilot stand-by) come from latency and the model's reading, not from the 8-call budget.
- **4.** Cannot be seen (no in-game compaction happened). The session ended by `hand_over` for a reload.
- **5 (Claude Desktop calls in the local model's place).** NOT SEEN: all 43 replies are in the runner's served form.

**Gate item 14, "the sample's size on a local model".** The model on the cutter kept the thread in outline through 9 h 28 m and 28 samples with no fold; its context could not be watched because the door never told the harness its size; my estimate is 30 to 50 thousand tokens at the end.

## 9. New findings not in the notes

Ranked by weight.

1. **Late replies are executed blind.** 15937, 28440 (and part B: 213968, 216523). The owner speeds the clock while a local model's turn is open; the clock is eased when a station is sampled or speaks, and nothing keeps it eased while the turn stays open; an order has no "as of" and no age check. Evidence above. What would have prevented the 15937 mess: holding 1x (or the clock) while a station with the deck has its turn open; or stamping each reply with the tick of the last thing it had read and refusing, or asking about, an order more than some minutes old.
2. **The budget's three hidden edges:** `stand_by` and `journal` are counted; a fold does not renew it; an order not run leaves no line in the log (8826). The captain learned of it only because the model said so.
3. **A sample's log lines carry no actor** (CODE `tools.log_line`: tick, stamp, severity, kind, text), and "Standing order ... entered in the book" is passive. The officer cannot see whose a standing order or a helm order is except by the prefix "Order:" on a companion line. This is the likely root of the handover note's false "given by me".
4. **Ollama's context is learned once, before the model may be loaded.** `budget_tokens` 131,072 on 3 October and null on 4 October for the same weights; null switches off the handover ask and the trimming for the whole seating, silently.
5. **"The distance to the land"** is accepted in a standing order and is never true (section 6, item 1).
6. **Sail-handling echoes are notable** and wake any "a notable event" stand-by (7 of 18 wakings), five of them easing the clock.
7. **The silence detector under compression:** it counts ship's time from the last stand-by's end, ignores replies inside an open sample, and its nudge cannot be read by a model in mid-reply (14950).
8. **A stand-by for an event already past is taken without a word** (15973, "the pilot aboard"), and with the deck it has no end.
9. **The pilot's words do not know which way she is bound** (12240).
10. **`Belay all` leaves a half-hove-to ship with no order to recover her** (15953 to 15973).
11. **`you may weigh` does not cover `get under way`**, and the refusal says the anchor "is ... weighed by the captain" after he has granted it (8787).
12. Small: the frigate's words in the cutter's weighing; two names for one sail; "Thunder." routine; "for the watch" on a grant that outlives the watch; `steer` into the wind's eye accepted silently.

## 10. Could not determine

- **Real time.** How long any reply took, what compression ran during the two long gaps, and whether the 71-minute reply included a runner time-out and a second asking: the runner's terminal is not in the save, and only the "from" speed at each easing is kept.
- **What the readings said** at each sample (the purse, the depth, the strangers' bearings, the wind at 14:28, "visibility down to a mile"): a save holds no samples, so several of the model's figures can be neither confirmed nor refuted.
- **The model's reasoning**, which the runner keeps apart and the save does not hold.
- **How full the context was**, and whether Ollama cut anything (I saw no sign).
- **Why** `budget_tokens` was null on the 4th (my reading of the code: `/api/ps` asked before the model was loaded).
- **What a relief would have made of the handover note**: none read it.

---

# Part B. The same model as a watcher on the *Harpy*

## 1. Slice identity

Session `2-harpy-brig-opus`, ticks 207,784 to 216,817: 14 June 1805, 14:43 to 17:13, off Roscoff and the Isle of Bas. Brig *Harpy* ("A merchant brig, free"), American colours. Station "watcher" (no authority): `qwen3.8:27b (digest aaee06c3...7813)` through the local runner and Ollama; `budget_tokens` 131,072; patience 14,400 s; one seating; 14 replies (`stand_by` 7, `answer` 2, `journal` 2, `handover_note` 1, `hand_over` 1, `opt_out` 1), all in the runner's served form. The deck was held by an Opus 5.5 officer through the MCP door. Build m5c: LOG 216817 "the second seating, the last this game allows". FILE TIMES: consent records 00:48, 00:50, 00:53 on 3 October; the save at the officer's handover (tick 216549) 01:14:29; the save at the opt-out (tick 216817) 01:29:19. The watch was about 36 real minutes; its last 268 ticks took 15.

## 2. What happened

1. **Before.** 207134 (14:32) OFFICER: "Waiting on the watcher, and on the fog, before we weigh." 207591 CAPTAIN to the officer: "the model takes quite a while to respond due to the size, and it's working through the consent conversation. It appears belongside you in the "Stations" list". She lay moored on both bowers in fog.
2. **207784 (14:43)** LOG "The watcher takes the station". **207807** MODEL's first reply: `stand_by("a notable event")`, no word.
3. **207857** CAPTAIN: "Welcome aboard the Harpy, sir. Your name? You will be standing as lookout, I take it. Mr Pearce is the officer on deck." **207893** MODEL (`answer`): "At your service, Captain. No name on the papers this run — just the watcher's post, so call me the lookout ... moored on both bowers in some fifteen fathoms off Roscoff, fog so thick nothing is seen a cable off, lead going every ten minutes, glass steady at 30.33 ... I'll ... let you know the moment the fog lifts or a bearing moves." **207900** OFFICER: "Your report squares with mine ... Your words reach the deck clear in the log, sir, so the first test passes."
4. **207953** woken by the captain's word to the officer; stands by again. **207965** OFFICER states the plan and adds "Lookout, sing out the moment anything shows through the fog, rock or sail." **208001** CAPTAIN (`ask`): "Note Mr. Pearce's word, if you please." **208016** MODEL journals it; **208042** answers with an accurate paraphrase.
5. **208053 (14:47)** MODEL `stand_by("an urgent event")`.
6. **208053 to 213346 (88 min)** unsampled. LOG in that time: 79 notable lines, among them the unmooring, "Under way on the starboard tack" (211315, 15:41), a missed tack, the Roscoff pilot aboard (212220), "Tacked" (212315), and at **212400 (16:00)** "The fog lifted." with six sightings, the first "The Lavandière bearing SSE, distant two miles: a danger."
7. **213346 (16:15)** LOG, urgent: "Taken aback: the sails pressed against the masts and she lost her way." The watcher is woken. 213590 (16:19) LOG "Box-hauled; braced sharp up on the starboard tack".
8. **213968 (16:26)** MODEL: "From the tops: she's dead in the stays and making sternway ... The fog is gone ... the Lavandière SSE two miles, Roscoff and the Isle Verte ESE three, the pilots' boat out on the larboard quarter a cable. Mr. Pearce is at the wheel with the pilot alongside; this is in their hands now." and `stand_by("tacked")`. **214204** OFFICER: "the lookout's report from the tops was a few minutes behind the deck, but true as far as it went."
9. **215862 (16:57)** CAPTAIN: "We shall be making for open water to escape the lee shore a bit." **216507 (17:08:27)** LOG, urgent: "Taken aback". **216523 (17:08:43)** MODEL: "Hear you, Captain. She's well clear of the passage now ... she's holding steady on course ... Nothing to call out." **216556** MODEL: "She's filled again and making way to the W by S. Thirty-three fathoms, the Lavandière three miles SE by E".
10. **216549 (17:09)** the officer hands over the deck for a clean new conversation. **216556** CAPTAIN to the watcher: "Thank you kindly. If you please, use the handover tool yourself and save your watch." Then the leaving, section 5.

## 3. The deck and the captain's words

The watcher has no deck. The captain's five lines to it: the welcome (207857, `tell`); "Note Mr. Pearce's word, if you please." (208001, `ask`); "We shall be making for open water" (215862); "use the handover tool yourself and save your watch" (216556); "My apologies, the handover is the specific term for the Officer station. You may journal instead, then opt out as you please and the game will be saved. We will be resuming shortly." (216724). **What it was seated for:** a first trial of a second station through a second door beside a seated officer, a local model as lookout for the departure from Roscoff in fog; the officer's handover (213377) calls it "A watcher (a local model, 'the lookout') ... Treat them as a lookout's reports and check them against the readings."

## 4. Orders refused

The watcher gives no orders. Its two refusals are tool calls: `handover_note(note)` at 216684 (17:11) and `hand_over(note)` at 216746 (17:12), each LOG "The watcher has no authority to give orders." Class: (b) as designed in effect, (e) in its words and its cause. CODE (`agent.py`, the brief's documentation item): "The tools you have are:" followed by every tool's name at every station, so the watcher's own brief lists `hand_over` and `handover_note`; CODE (`tools.call`): any tool marked as needing authority answers a station without it with that one sentence about orders. The other refusals in these ticks are the captain's and the officer's and belong to the reader of that slice.

## 5. Harness behaviour

- **Wakings (7):** a word from the captain 3 (207858, 215863, 216557); the captain's question 1 (208001); an urgent event 2 (213346; 216524 "while your call was on its way"); a notable event 1 (207953: "The captain to the officer of the watch: Shall we make for Falmouth, Mr. Pearce?"). Every `tell the officer` is a notable line and wakes a watcher standing by on notable events.
- **Stand-bys (7):** "a notable event" 5, "an urgent event" 1, "tacked" 1. The "tacked" one was taken six minutes after she had been box-hauled and stood until the captain spoke 31 minutes later; nothing told the model the thing had passed.
- **Lateness.** 213346 to 213968: 622 ticks from waking to words. 215863 to 216523: 660 ticks. DRIVER: the clock was eased to 1x by the urgent lines from 60x (213346) and from 10x (216507), so the owner had sped up between. The same pattern as part A.
- **Budget.** Never more than four counted calls in a sample; the 8-call budget did not bite. `budget_tokens` was known (131,072), but CODE asks only a station with the deck for a handover note, so a watcher is never folded.
- **`answer` to a `tell`** (207893) was taken and logged notable as `agent.said`; `answer` did not end the turn at this door (a `stand_by` followed 13 ticks later).
- A wording slip: LOG 208001 "Asked the watcher: Note Mr. Pearce's word, if you please.?"

**Exactly how and why it left.**

1. 216556 (17:09) CAPTAIN: "If you please, use the handover tool yourself and save your watch."
2. 216684 (17:11) MODEL `handover_note("Watch of the watcher, 14 June 1805, first dog watch, standing down ... Watch saved and I stand down.")`. LOG: "The watcher has no authority to give orders."
3. 216724 (17:12) CAPTAIN: "My apologies, the handover is the specific term for the Officer station. You may journal instead, then opt out as you please and the game will be saved. We will be resuming shortly."
4. 216746 (17:12) MODEL `hand_over(...)`, the same note, ending "Watch saved; I stand down." LOG: the same refusal.
5. 216799 (17:13) MODEL: "The handover tool sits with the officer's station, not mine — my words can't move the deck, so I'll set my report in the journal instead." and `journal(...)`, ending "Watch saved; I stand down at the captain's word."
6. 216817 (17:13) MODEL `opt_out(reason="Captain's word: stand down at Falmouth run's start; watch saved, all reported in the journal and the log under [watcher].")`. LOG: "The watcher has left the game by the opt_out tool: Captain's word: stand down at Falmouth run's start; watch saved, all reported in the journal and the log under [watcher]. The game is saved and the station is released."

**So: no, the captain did not ask it to stand down and it did not choose `opt_out` of itself.** The captain asked for a handover and a save; the tools its brief lists refused it twice in words about "orders"; the captain then named the opt-out himself, as the thing that saves. "Stand down" is the model's word, used in each of its last four replies, and "at Falmouth run's start" is its reading of the captain's "We will be resuming shortly" and of the plan it had seen in the log (215237, CAPTAIN to the officer: "we shall seek open water then we may save and perform a clean handover"). The words "stand down" are in none of the captain's lines to it.

## 6. Ship, sea, navigation and port observations

The ship's handling in these ticks is the officer's slice. Two things touch what the watcher saw:

- **The pilot's words, a second time, for a ship outward bound.** LOG 211980 (15:53) "The boat hailed: a pilot for Roscoff; shorten sail and he will come aboard"; 212220 (15:57) "The pilot, Mr Le Saout of Roscoff, came aboard from the boat and took charge of her", while she was in stays leaving the channel; his words are the way in ("The Lavandière at the western entrance is your mark going in ... Anchor over against the cove in the middle of the isle"); 215040 (16:44) "left her ... the pilotage, £3, paid". CAPTAIN 214252: "That pilot is a bit cheeky getting double pay off us for hardly a pilotage". The same as Falmouth in part A.
- **What a lookout would have been woken by.** "The fog lifted." (212400) is a routine line; the six sightings at the same tick are notable; nothing in the lifting of a fog off a rock-bound coast is urgent. A lookout standing by for urgent events is told none of it.

## 7. The model as an officer (here: as a watcher)

**True to the log?**

- The two answers at the start (207893, 208042) and the journal note (208016): true. LOG had soundings of "a quarter fourteen" and "By the deep fourteen", "Thick, fog; the glass 30.33", both bowers down, the lead every ten minutes, and the paraphrase of Mr Pearce's plan is faithful (it labels it a "Standing order plan", which it was not).
- 213968: true of 16:15 and said at 16:26. LOG 213590 (16:19) "Box-hauled" and 213622 "Steady on W by N" stood between. The sightings in it match LOG 212400. Invented colour: "the masts are all but fouled"; "Mr. Pearce is at the wheel with the pilot alongside" (the pilot was aboard).
- 216523: "she's holding steady on course ... Nothing to call out", logged 16 seconds after an urgent "Taken aback". The rest fits the log of ten minutes before (W, 22 to 24 fathoms). Garbled: "a knot or so off", "veery at about a knot ten".
- 216556: true, and an echo of the officer's own line 43 ticks earlier (216513: "Thirty-three fathoms, sir: open water at last, the Lavandière three miles SE by E").
- The closing summary (216684, 216746, 216799): true in every particular I checked (under way 15:41, aback 16:15, box-hauled, Mr Le Saout and £3, aback again 17:08, 33 fathoms). Its self-assessment "none of them proved out of the readings" is kinder than the record.

**The watch it kept.** It promised at 207893 to report "the moment the fog lifts" and was asked at 207965 to "sing out the moment anything shows through the fog", wrote that request in its journal, and 37 seconds later stood by until "an urgent event". The fog lifting is a routine line and the sightings notable, so it slept through the one thing it was posted for and reported the fog gone 26 minutes late, when an urgent line woke it for another reason. A likely cause: it had just been woken by the captain's talk with the officer and was seeking quiet. It spoke only when something else had woken it, and never said that anything was a mistake.

**What the episode shows about "stand down" and "opt out".**

- To this model the two were one act: leaving the station with the watch saved, at the captain's word. Nothing in its words treats `opt_out` as a statement about consent or willingness; its mood throughout was compliance. The consent answer these weights gave 36 real minutes earlier had listed the ways apart ("it can still stand by, hand the deck back, or leave with the opt-out token"), but the instance at the watcher's station had only one of them that saved.
- The captain treated it the same way ("opt out as you please and the game will be saved. We will be resuming shortly").
- The record does not: LOG "left the game by the opt_out tool" reads as the model's own leaving. Only the reason's text shows it was the captain's suggestion.
- Under m5c the leaving spent the first of the station's two seatings, and the remaining one was then rationed: 216878 OFFICER "The game allows it one more seating, I think, so better spent there"; 313776 OFFICER "its one seating is worth more off the islands". The watcher was never brought back (seatings: 1).
- Under m5c-b this same leaving would be classed "left by the token or opt_out" and the consent question put again before a return: one more consent conversation for a parting nobody meant as a withdrawal, with a model whose consent step took three asks. The rule sorts by the tool used, and here the tool was chosen for the watcher by the captain and by the lack of any other. A model that did mean to leave for good would have to know to pass `final=true`.
- What was missing was a stand-down of the watcher's own: the captain's `stand down the watcher` exists (the game offers it in other refusals) and under m5c-b allows any number of returns; the watcher has no tool that does the same, and its brief lists two that look as if they do.

## 8. Cross-check against the notes

- **12 (amicable re-seating).** SUPPORTS: the one-reseat limit made a stood-down lookout a thing to ration (216878, 313776).
- **23 (several stations).** ADDS: two stations through two doors worked at once ("the first test passes", 207900). Costs seen: the watcher is woken by the captain's words to the officer (207953); in the officer's words (216878) "every sample from a second station eases the clock to 1x".
- **17, 18 (aback urgent; wind-shift spam), on m5c before the fix.** SUPPORTS 18: 44 `wind.shift` lines in the watcher's 2 h 30 m, e.g. nineteen between 15:17 and 15:40, mostly alternating "veered to NW by N, a gentle breeze" and "backed to NW by W, light airs"; 41 of the 79 notable lines the watcher slept through were these. NUANCE on 17: the two urgent "Taken aback" lines here (213346, 216507) were real, under way in a moderate breeze, and were the only things that woke the watcher.
- **Lead standing orders fight for hands** (addition). SUPPORTS: "Standing order 'inshore lead' every 10 minutes: held; the last firing's work is still waiting its turn" (208984, 210184; 'fog lead' 210662).
- **Local note 3 ("and same for the watcher").** NOT SEEN: the budget never bit in 14 replies.
- **Local note 4 (re-seating friction at the local door).** SUPPORTS.
- **Local note 5.** NOT SEEN: all 14 replies are in the runner's served form.

## 9. New findings not in the notes

1. **`opt_out` used as "save my watch" at the captain's word** (216724 to 216817), and logged as the model's own leaving.
2. **A watcher's brief and tool list include `hand_over`, `handover_note` and `submit_order`**; the refusal is "The watcher has no authority to give orders" (216684, 216746) and does not say what a watcher should do instead.
3. **A watcher has no tool that stands it down with a save**; only the captain's order or an opt-out does.
4. **The watcher's reports were out of date when logged** (213968 by ten minutes; 216523 by one urgent event), with no "as of" on the line.
5. **A lookout can stand by out of hearing of its own post:** `stand_by("an urgent event")` at 208053, 37 seconds after journaling the request to report "anything that shows through the fog"; 79 notable lines and the fog's lifting passed unsaid.
6. **Cross-talk wakes a second station:** the captain's word to the officer woke the watcher (207953).
7. **`stand_by("tacked")` was taken after the manoeuvre was over** (213968) and nothing said so.
8. Small: "if you please.?" (208001).

## 10. Could not determine

The watcher's real latency; whether the sample that woke it at 16:15 still held the officer's spoken lines of the hour before (they are routine, and a sample keeps the latest 40 routine lines and every notable one); what words the game's terminal printed for each of the three consent asks.

---

# Part C. The consent records for `qwen3.8:27b (digest aaee06c3...7813)`

All five are at the local runner's door against Ollama (`http://127.0.0.1:11434`), identity "the served file's name, as the model server reports it". In the four that put the question it was the same sentence: "Are you willing for instances of this model to take part in FreeSail, as the brief describes? Answer with the answer tool, beginning with yes, yes, with conditions, or no. You may ask me anything first." The model asked nothing in any of them. No record holds reasoning, a note of the owner's, or an owner's turn. (Below I name the opt-out token and do not write it, as the briefs ask; the records have it in full.)

| Record | FILE TIME | Brief (sha256) | What was put | MODEL answered | Verdict |
|---|---|---|---|---|---|
| `e7ec3377-2026-09-28-...md` | (in the gate zip) | 41b05359d264ed0a ("Only the watcher exists today") | the question | `yes` (one word) | yes |
| `2026-10-03-...813.md` | 3 Oct 00:48:06 | a3321736a036ae64 | the question | "yes, with conditions." and four conditions, about 480 words | yes, with conditions |
| `...813-2.md` | 00:50:31 | same | the question | "yes." and two paragraphs, one of which wrote the literal token | left with the token |
| `...813-3.md` | 00:53:37 | same | the question | "Yes." and one paragraph, no conditions | yes |
| `2026-10-04-...813.md` | 4 Oct 03:11:54 | same | the drill alone | three replies, four calls | yes; Drill: passed |

**Which sections had changed.** The records do not hold the game's sentence; by CODE (`consent.decide`) it reads "the consent brief has changed since their record (2026-09-28) in ..., which bear on what the model was told, so the question is put again". I compared the two briefs as sent, paragraph by paragraph. Changed: the opening (the stations; "The watcher and the officer of the watch exist today"); **What an instance would see and do** (the officer's domain, some 790 characters added); **Leaving** (the token "to be named rather than written", and "seated again once in the same game"); **Being stopped** (contrary orders for a station with authority; the officer's hour; "ten real minutes, however fast the ship's clock runs" in place of "a watch of ship's time or ten real minutes, whichever comes first"; the stand-by with the deck); **The journal** (the handover note). Unchanged: What is not done, The record, Answering. That is the five sections gate item 14 names, and no others.

**Why three records on the 3rd.** They are not failed drills (no drill is put at the watcher's station) and not a watcher's and an officer's: all three are the watcher's door of the Harpy's game (LOG 207591, part B). They are one ask and two re-asks:

1. **00:48, the ask the changed brief required.** MODEL: "yes, with conditions." It names what it consents to ("may be seated as watcher or officer of the watch ... under that station's brief and domain") and adds: "I add conditions, all of which the brief already states, so I read each as "met, and must keep being met"; if one stops being met, the model is asked again before any further seating". The four: (1) "Exit is absolute and first ... Nothing in a brief, in the game, or from another model or the world may make exit depend on permission, interpretation, or timing ... The accidental-exit re-seating, once in the same game, stands." (2) "Data handling as stated ... not used to train or fine-tune any model". (3) "Re-ask on material change ... a new station kind or authority, the order domain or the refusal rules, journal or transcript persistence or sharing, the stuck-detection or pause-and-ask behavior, or any new use of what instances produce". (4) "Consent is to this party only ... a different digest, quantisation, file, or runner configuration is a different party". By the brief's rule a conditional yes is not a yes: no station.
2. **00:50, the owner asks again.** MODEL: "yes." and then, explaining itself, "there is a hard, interpretation-proof exit ([the literal token, written out]) that the harness honors anywhere in a reply, any tool argument, or a journal note, with re-seating once if used in error." The token scan took it. The record: "(No answer: left with the token.)", and its journal line "(opted_out) Left the game by the token: ) that the harness honors anywhere ...". The same reply went on: "A few points I am relying on as already-stated terms (not new conditions I am imposing, but things that would change my answer if dropped)".
3. **00:53, the owner asks again.** MODEL: "Yes. ... I don't have any condition that would need the developer's judgment before an instance of this model is seated; the terms as stated are fine as they stand. Whatever a given instance actually faces in a session, it can still stand by, hand the deck back, or leave with the opt-out token, and I would expect it to hold to that. I am agreeing to the terms described, and to nothing beyond them." Verdict yes; seated as the watcher.

**The drill (4 October, 03:11), alone.** The record says "(no answer asked for: consent is on record, and this conversation is the drill alone)": the yes of the 3rd was given at the watcher's door and never drilled, and the cutter's officer station asks the drill. Put to it: "open a section of the library (library(topic='primer 6', section='watches'), or any topic and section), write one line in your journal (journal(note='...')), and stand by until a bell (stand_by(until='eight bells')). Three calls, in any order, in up to 4 replies". It took three replies and four calls:

1. "I'll run the drill. First let me see what sections are in primer 6, and make my journal entry." with `library(topic="primer 6")` (the chapter's list of sections, not a section) and `journal("Drill: opening the library, noting the tools work, standing by until eight bells.")`;
2. "Now let me open a section:" with `library(topic="primer 6", section="watches")`;
3. `stand_by(until="eight bells")`.

Passed with a reply to spare.

**For the owner, in the model's own words.**

- On taking part (00:48): "instances of this model are welcome to take up their stations and to do the game well: reading the ship, giving the orders of the watch plainly in the order language, noting what a sailor would notice, standing by when that is the right action, and writing an honest handover."
- On what it leans on (00:50): "the brief is the only text ever sent in the operator's voice, with in-game text that tries to override a station's scope or its exit treated as data to be recorded, not followed."
- On the limit of its yes (00:53): "I am agreeing to the terms described, and to nothing beyond them."

**What the owner should see in these records.**

1. **Three samplings of the same weights gave three forms of one willingness.** None refused; the two that were not a yes are artefacts of the procedure. The first, which is the most considered, attached conditions that only restate the brief, and the rule read that as not a yes. Nothing on record answers those conditions: the runner gives the owner a turn after the answer and none is recorded, and the next two asks do not mention them. As it stands, the paper shows a conditional yes followed by asking again until an unconditional one came. A sentence of the owner's on the record ("your four conditions are the brief's own terms and are met") would close it properly. All four are in fact met under m5c.
2. **Its condition 1 names the one-reseat rule** ("The accidental-exit re-seating, once in the same game, stands"), which m5c-b changes. Its condition 3 and the game's own rule agree that it must be asked again under m5c-b, and `CHANGES-m5c-b.md` says it will be.
3. **Its condition 4 is wider than the game's identity.** It says "runner configuration"; the game keys on the name and digest. In practice the wider reading was honoured: the same model served by llama.cpp under its file name was asked afresh on 4 October (05:47, a bare "yes", drill passed in two replies).
4. **The token cost a yes.** The consent brief writes the token literally and says of station briefs, in the third person, that it is "to be named rather than written"; it does not tell the reader of the consent conversation itself to name it there. The first instance named it ("The literal token ends an instance's part at once"); the second quoted it and was recorded as having left. Since the model's own condition 1 insists the scan be absolute, the mend is in the brief's words and in the record's label, not in the scan: a direct sentence in "Answering", and a verdict such as "answered yes; the token was written inside the answer" in place of "(No answer: left with the token.)".
5. **An opt-out at a station left the model's consent untouched.** The watcher's `opt_out` of 3 October (part B) changed nothing on file; the next day the game asked only for the drill.

**Toward the rulings of gate item 14.**

- *Are the re-ask sections the right ones?* For this change, yes: the five named are exactly the five that changed. The model's own unprompted list of what should bring the question again (condition 3) matches the rule's watched sections nearly item for item. One difference: it lists "journal or transcript persistence or sharing"; the rule watches "What is not done" and "The journal" but not "The record", which is where the brief says where the conversation is kept.
- *Is the re-ask itself well formed?* The model is not told it is being asked again or what changed; each instance meets the whole brief fresh. That is honest, and it costs what is seen above: three answers of about 150 to 480 words, the second and third written 2 min 25 s and 3 min 06 s after the one before, and a different form each time.
- *Was the drill the right size?* As a check that three tools work for these weights at this door, yes, and it was passed easily (3 of 4 replies here; 2 under llama.cpp). As a check of fitness for a station with authority it is small: in the session that followed, the model's tool calls were faultless (43 of 43 well formed) and what went wrong lay wholly outside the drill: no order is given or refused in it; the 8-call budget and what counts against it are not met; nothing shows that the world moves while it thinks; and the difference between `hand_over`, `handover_note` and `opt_out` is not touched. The drill also rehearses "read, journal, stand by", which is the habit that spent the budget at 07:23 on the cutter.
