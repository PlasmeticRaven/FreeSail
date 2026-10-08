# L1. The cutter's watch by a local model (session `5-cutter-gemma`, gate m5c item 11)

Reader's report. Everything here is from the dumps in `SESSIONS\5-cutter-gemma\`, the save
`saves\freesail-seed7-tick54107.json`, the three consent records, and the harness's own files, all
read and none changed. "The log" means the ship's log; "the model said" means a reply or a note of
the model's; where the two differ I say which is which.

One source beyond the dumps, because it settles several questions: the checkpoint beside the save
(`freesail-seed7-tick54107.checkpoint`: gzip, one JSON header line, then a pickle) still holds the
harness's conversation as the model was sent it (the two briefs, every sample's changed readings,
every tool result and notice). I read its strings with Python's `pickletools` (opcodes listed,
nothing unpickled, nothing run, nothing written). Where I cite "the readings sent to the officer"
or "the tool result", that is where it comes from. Log lines inside samples are not recoverable
that way (they are shared with the log), so sample sizes below are lower bounds.

## 1. Slice identity

| | |
|---|---|
| Session | `5-cutter-gemma`, whole: ticks 0 to 54,107 |
| Ship's time | 12 June 1805, 05:00:00 to 20:01:47 (15 h 02 m) |
| Scenario, ship | "A merchant cutter, free", seed 7, `data/ships/cutter.yaml`; the captain calls her the *Sherbourne*; 27 hands (12 and 15 by watches); a master, Mr Bowen |
| Station | officer of the watch, in the place of Mr Pearce, mate; authority "officer, levels 0 to 2"; sampled every glass and on notable and urgent events; patience 3,600 s |
| Model, door | `Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced:Q4_K_M` through the local runner (`freesail.agents.local`) against "an OpenAI-compatible server at http://127.0.0.1:11434" (the consent records' runtime line: Ollama's port, not llama-server's) |
| Context figure | `budget_tokens: null` in this save and in the first hand-over's save (`freesail-seed7-tick14978.json`): the door never told the game what context the server gave the model |
| Build | m5c ("the second seating, the last this game allows") |
| Seatings | first: tick 1 to 14,978 (05:00 to 09:09); second: 14,978 to 54,107 (09:09 to 20:01) |
| The deck | the officer's from 8,351 to 14,978 (07:19 to 09:09, 1 h 50 m) and from 15,047 to 54,107 (09:10 to 20:01, 10 h 51 m) |
| Real time | consent record 01:57:28, drill record 01:59:04, first save 02:26:40, last save 03:08:28 (4 October, file times): about 27 minutes for the first seating, 42 for the second |
| Counts | 1,528 log events (293 notable, 3 urgent); 117 captain's inputs; 120 transcript entries (119 replies, 1 door event) |

## 2. What happened

1. **05:00 (tick 0-1).** Anchored in Carrick Road, wind W by S 12 kn. The captain loads the starter book: 5 of its 9 standing orders are refused for a cutter (no studdingsails, royals, fore topmast staysail), 4 stand. The officer, seated without the deck, reads the library (contents, standing orders, primer 11 twice), tries to load the starter book itself (refused: no deck), journals, stands by.
2. **05:00.** Asked about the starting orders it gives an accurate summary; asked what to buy, it answers "copper ore or timber" (its figures right, its "good return" unsupported: only Falmouth's prices were aboard). The captain buys 4 tons of tin for £480 of his £500 (tick 560).
3. **05:30-07:00.** At anchor the officer stands by bell to bell (four wakes, four stand-bys). The tin is aboard at 07:17 (8,250).
4. **07:19 (8,351).** "You have the deck." 07:19:40: "make ready to get under way to the south, out of Carrick Road." She lies head north to the ebb, the wind on the larboard quarter.
5. **07:19-07:20 (8,391-8,413).** The officer sets the foresail and the mainsail, spends five calls on "set ... sheet" and "haul ... sheet" orders that are refused, spends its eight calls, has four more "Not run" (three of them "weigh the best bower"), and falls out of the tool format into prose and a Markdown table. The captain weighs by hand (8,427) and allows steer, tack and wear (8,437-8,441).
6. **07:20 (8,448-8,458).** The officer repeats the same eight orders. Then a 7,589-character runaway table reply, logged at 07:33 (9,223). She sails about her anchor under mainsail and staysail meanwhile.
7. **07:36 (9,383-9,442).** Anchor aweigh; 28 s later the officer orders "tack ship" and stands by "until tacked". The tack "fell off on the larboard tack" at 07:44 (9,866). The captain wears her round, belays, steers south, and types "tell the officer Ship tacked." (10,360) to wake the officer.
8. **07:52-07:53 (10,365-10,436).** The officer reads the library on the pilot (three calls), hauls the staysail sheets, has four calls "Not run" (three "set the fore topgallant"), and produces a second runaway reply (7,587 characters).
9. **07:55-07:57.** The Falmouth pilot's cutter hails; Mr Tregenza boards under way at 10,620 with the inbound directions for a ship that is leaving. The officer's report of it (10,628) is a table, not a call. At 08:00 it stands by "four bells" (10:00).
10. **08:00-09:02.** The captain cons her out past the Black Rock (three cables off, 08:09) and round St Anthony's Head. Between 07:55 and 08:28 he writes five standing orders (lead, bearings, trim on the course, heave to when the pilot asks off, tell the officer when the pilot is off). The officer is standing by throughout.
11. **08:36 (12,960-13,004).** The pilot asks off; the standing order heaves her to. 09:00 (14,401): "tend the sheets" trims the backed staysail's sheet while she lies hove to. 09:02 (14,520): the pilot leaves, £5 paid; the standing order wakes the officer. The readings it is sent say she is making sternway at 1 knot, head 35° off the wind.
12. **09:02 (14,554-14,579).** The officer answers ("The pilot has been put off, sir..."), then "unhove to" (not an order), then seven more refused orders, two "Not run". The captain types "fill away" (14,576). 09:05 (14,757): "Filled away; braced full and steering S (176°)", though she still heads SW by S 212° with sternway. 09:08: the third runaway reply (14,903).
13. **09:09 (14,962-14,978).** "Please use the handover tool." The officer calls `hand_over`; the station is stood down and the game saved. The runner is started again and the officer seated "again ... the second seating, the last this game allows", the deck the captain's.
14. **09:09-09:25.** The captain fights her out of irons (let fly the mainsheet, hard down, hard up, trim, set the jib). He gives the deck back at 09:10 (15,047). Two urgent "Taken aback" lines (15,120 and 15,416) as she rounds up and passes through the wind. The officer's helm orders: steer 65, 135, "hard down" (refused), 330, 240; two nudges (15,527, 15,541). The captain steers her off; "Steady on ENE (66°)" at 15,909.
15. **09:27 (16,033-16,052).** "Please make all sail." The officer tries "set the topsails", reads primer 3, orders "make all sail": all sail set by 09:41.
16. **09:30-12:00.** Running ENE at 4½ to 5¾ knots along the coast. The officer stands by bell to bell; one order ("trim the sheets" at 11:30, nothing to trim). The captain belays the lead order at 10:30 after three casts of "No bottom at twenty fathoms".
17. **12:00 (25,200).** Noon: "Latitude by observation 50° 17' N; the reckoning was 50° 12' N". From 12:05 the officer runs its own five-minute round (heave the lead, a bearing, trim) for five rounds; the bearing is refused once and then allowed.
18. **12:27.** Noon report asked and given; "Are you finding the ship well?" "She's behaving well, sir, although the wind is light." At 12:28 the officer stands by "eight bells" (16:00).
19. **12:28-16:00.** Three and a half hours with nobody sampled: nine firings of "trim on a shift", two course changes by the captain (14:52), the Eddystone and Rame Head sighted, "Sail ho!" at 15:31.
20. **16:00 (39,600-39,660).** The officer trims the square sails; told "we might make the anchorage by tonight. What say you?" it answers "If the wind holds and we keep this course, we should reach it well before dark, sir." The captain shortens sail himself (16:03-16:07).
21. **16:34-16:40.** The Plymouth pilot's cutter hails; Mr Hancock boards at 41,940; a squall 41 s later. Told to take sail in "bit by bit ... I'll con her", the officer takes in the topsail (16:40) and the topgallant (17:00).
22. **17:22-17:41.** Off Penlee Point in airs of 4 to 7 knots: 43 wind-shift lines in 19 minutes; the third urgent "Taken aback" (44,583). The officer orders "steer 90" (44,668); the captain orders "Steer north west" 73 s later.
23. **17:32-17:49.** "Come to anchor": let go in ten fathoms (45,322), brought up (46,159). The officer's "take in the topgallant" (already in) and "haul down the mainsail" are refused; "take in the main sail" is taken. The captain belays five standing orders by name.
24. **17:52-20:00.** "You may stand at ease." The boat goes for the prices and is back at 19:58. The officer stands by "eight bells".
25. **20:01 (54,095-54,107).** "we can't sell the tin here. Please, work up a handover for the next watch". The officer calls `hand_over`; stood down; under m5c that ends its part in this game.

## 3. The deck and the captain's words

**The deck.**

| Tick | Time | Log |
|---|---|---|
| 1 | 05:00 | seated; "The deck is the captain's now." in its brief |
| 8,351 | 07:19 | "Mr Pearce, you have the deck. The officer of the watch has the deck; the captain's standing orders are his night orders." |
| 14,978 | 09:09 | "The officer of the watch hands over the deck; the captain has it." (the officer's `hand_over`, asked for by the captain 16 ticks before) |
| 15,047 | 09:10 | "Mr Pearce, you have the deck." again, 69 ticks after the reseat |
| 54,107 | 20:01 | handed over again, again at the captain's word |

"I have the deck" was never said. Both hand-overs were the officer's tool at the captain's request.

**Allowances: six** (the log has ten `agent.deck` lines; two are the deck given and two the deck handed back).

| Tick | Captain typed | Logged as | Used? |
|---|---|---|---|
| 8,437 | "You may steer" | "may steer, by the captain's word for the watch" | yes: steer 65, 135, 330, 240 (15,059-15,541) and steer 90 (44,668) |
| 8,439 | "You may tack" | "may tack ship" | once: "tack ship" at 9,411, which failed |
| 8,441 | "You may wear" | "may wear ship" | never |
| 15,523 | "You may hard down" | "may helm a lee" | never (given 5 s after the refusal; the officer ordered "steer 330" instead) |
| 15,528 | "You may hard up" | "may helm a weather" | never |
| 25,530 | "you may take a bearing of the land" | "may take a bearing of (the land)" | five times (25,542 to 26,827), each a duplicate of the standing order's bearing |

All six stayed in force to the end. The reseat brief carried the first three ("The captain's word for this watch allows: steer; tack ship; wear ship."), and "steer 65" was taken at 15,059 with no new word. "For the watch" ran through five changes of the watch.

**The captain's words that carry intent.**

- 1: "Welcome aboard the Sherbourne, sir. Please get yourself comfortable, you shall have the deck soon."
- 1 (tell): "our intended destination shall be Plymouth on this trial run. What would you buy here, if anything? Feel free to review the ship's papers before you decide." With the clock standing at tick 1 a tell opened no turn (the first tell, too, reached the model only with the first ask); he had to follow this one with an ask, "Did you hear my last word, Mr Pearce?"
- 8,380: "Note the tin in the hold, make ready to get under way to the south, out of Carrick Road."
- 10,360: "Ship tacked." (she had worn; the words are there to end the officer's stand-by)
- 12,528, a standing order used as a messenger: `standing order "The pilot is away": at the pilot off then tell the officer the pilot has been put off, please inform the captain and carry on as we were.` It fired at 14,520 and woke the officer. "Carry on as we were" needed a fill-away, which is outside the officer's domain.
- 14,962: "Please use the handover tool." (the hand-over used as a compaction, after three runaway replies)
- 16,033: "Please make all sail."
- 26,840 (ask): "I'd have your noon report if you please, Mr Pearce."
- 39,657: "We're a few miles off Rame Head based on the reckoning, we might make the anchorage by tonight. What say you?"
- 42,029: "The pilot is aboard. We'll follow his directions in. Keep an eye on the sails and start taking them in bit by bit as we close in if you please, I'll con her."
- 46,355: "We're brought up, you may stand at ease ... Hopefully we can fetch a hair more than we paid for the tin here, otherwise we'll need to head elsewhere."
- 54,095: "Well, the bad news is we can't sell the tin here. Please, work up a handover for the next watch, and I'll decide what to do next."

**What the captain did by hand because the officer could not or did not.**

- Weighed (8,427): the officer's three "weigh the best bower" were cut by the budget, and the anchor is the captain's in any case.
- Recovered the failed tack: "tack ship" (refused, no way), "wear ship", "belay that", "steer south" (10,101-10,348).
- All the pilotage out of Falmouth (ten inputs between 08:00 and 09:02) and all of it into Plymouth; every course change of the passage.
- "fill away" (14,576) and "Shape a course for plymouth" (14,902).
- Sixteen ship-handling orders between 14,576 and 15,698 to get her out of irons.
- Shortened sail before the Plymouth pilot (39,825 "Clew up the square sail", 39,969 "take in the gaff topsail").
- Came to anchor, belayed five standing orders one by one (two tries failing on the wording), took bearings, worked up the reckoning, sent the boat.
- Wrote six standing orders under way to cover the lead, the bearings and the trim.

## 4. Orders refused

Totals: 49 `order.rejected` (24 the officer's, 16 the captain's, 9 by standing orders) and 4 `agent.refused`. Of the officer's 74 `submit_order` calls, 36 were taken, 24 refused by the ship, 4 refused by the deck or the domain, and 10 never ran (budget).

**Refused by the deck or the domain (`agent.refused`, 4).**

| Tick | Order | The refusal | Class |
|---|---|---|---|
| 1 (05:00) | "read the standing orders from data/standing_orders/starter.orders" | "has not the deck: the captain gives it with 'you have the deck', and until then no order is given." | (b). The officer was acting on the driver's hint line, which stood in its brief's log. |
| 14,978 (09:09) | "steer ENE" | the same | (b). First act of the second seating, though the brief said "The deck is the captain's now." |
| 15,518 (09:18) | "hard down" | "may not hard down without the captain: the course is the captain's, never to be changed without his directions unless to avoid an immediate danger." | (b) by the letter, (c) in the case: an urgent "Taken aback" had just woken him, "steer" was allowed, and the refusal names an exception there is no way to use. Allowed 5 s later; he then ordered "steer 330". |
| 25,521 (12:05) | "take a bearing of the land" | "may not take a bearing of the land without the captain: the reckoning, the sights and the course shaped are the master's for the captain." | (c). The lead and the lookout are his; the captain's own standing order was taking the same bearing every five minutes. Allowed 9 s later. |

**Refused by the ship, the officer's (24).**

| n | Orders (ticks) | The refusal | Class, and what came next |
|---|---|---|---|
| 9 | "set the foresail sheet" (8,396), "set the foresail sheet starboard" (8,397), "set the fore staysail sheet starboard" (8,398; 8,455; 10,368), "... larboard" (8,457; 10,369; 10,371), "set the foresail sheet larboard" (14,556) | "You set sails; the starboard fore staysail sheet is a sheet (a line). Did you mean the fore staysail?" | The model's own misuse, not a gap; the refusal is correct and clear. Not learned: nine times over 1 h 43 m. "haul the fore staysail sheets" (10,370) was taken. The second seating used "trim the sheets". |
| 6 | "haul the fore staysail sheet starboard / larboard" (8,399 twice; 8,455; 8,456; 8,458; 14,558) | "... is already hard in." | (d) |
| 5 | "set the fore staysail" (14,559), "set the main sail" (14,560), "set the foresail" (14,561; 14,563; 14,564) | "... is already set." | (d). This was the attempt to get out of the heave-to. |
| 1 | "unhove to" (14,555) | "'unhove to' is not an order this ship understands; did you mean 'heave to'?" | Invented word. The hint offers the opposite manoeuvre; "fill away" would be the useful one. The captain typed it 21 s later. |
| 2 | "take in the square sail" (43,215), "take in the topgallant" (45,176) | "The square sail: The square sail is in the gear; there is nothing to take in." | (d). The sails line he was sent says "in the gear"; he probably wanted them stowed, and the refusal does not offer "furl". The subject is doubled in the text. |
| 1 | "haul down the mainsail" (45,191) | "A gaff sail is brailed up, not hauled down; say 'brail up the main sail' or 'take in the main sail'." | (a), mildly: a hint that works. "take in the main sail" taken 1 s later. (Whether a cutter's boomed mainsail is "brailed up" is a question for whoever reads the rig.) |

**Refused by the ship, the captain's (16).**

| Tick | Order | The refusal | Class |
|---|---|---|---|
| 1 | five starter-book rules ("night routine", "morning sail", "shorten sail for weather", "heavy weather", "storm staysail") | "There is no such part as the studdingsails in this ship; did you mean the staysails?" and the like | (d) for the rig; the starter book is not rig-aware (5 of 9 refused on the cutter) |
| 1 | "the chandlers" | "not an order this ship understands; did you mean 'the booms' or 'ask the pilot'?" | (a). Just before it, "the yard" was answered with the spars ("The yard: the square sail yard 0.00 of the rating ..."), not the port's yard. |
| 1 | "buy 4 tons of tin" | "She is not in port; the market is ashore and the boat has nowhere to go." | (d): typed under a minute before the anchor was down (tick 59); taken at 560 |
| 8,470 | "Hard down" | "She is at anchor; 'hard down' must wait till she weighs." | (d) |
| 10,101 | "tack ship" | "She has not way enough on her to stay: 0.7 kn through the water." | (d). But the officer's same order was accepted at 9,411, 28 s after the anchor broke out: see section 6. |
| 11,590 | "bely that" | "did you mean 'belay that', 'belay' or 'belay the work'?" | typo; good hint |
| 11,592 | "belay that" | "There is no work in hand or waiting to belay." | (d): he meant to take back a helm order |
| 15,233 | "fill away" | "She is not hove to." | (d) by the flag; she was in irons, for which there is no order |
| 19,374; 45,211 | `belay standing order "close in lead"` | "There is no standing order 'close in lead' in the book." | (a), mildly: the rule was "heave the lead close"; no nearest name offered; he had to list the book (19,536) |
| 43,982 | "turn north by east" | "'turn north by east' is not an order this ship understands." | (a): "steer n by e" worked 6 s later |
| 45,256 | `belay order "tend the sheets"` | "There is no such part as the order tend in this ship. ('belay' was understood.)" | (a): it wants the words "standing order"; the message is a misparse |

**Refused by the ship, standing orders (9).** "keep her full" at anchor three times (263; 8,910; 9,240) and once hove to (13,063: "She is hove to; fill away before giving her a course."); "tend the sheets" at anchor five times (1,801 to 9,001: "She is at anchor; 'trim the sheets' must wait till she weighs."). All (d), and all noise: these rules are not held at anchor the way "sound the well" is held ("Held until the ship can carry it out").

**Did it learn the order language within the session?** Partly. It took one hint at once (the mainsail). It found "make all sail" by reading primer 3 after "set the topsails". It never understood that "the foresail" and "the fore staysail" are one sail, and it repeated the "set ... sheet" form through four turns. By outcome: first seating 41 orders, 9 taken (4 of them duplicates), 21 refused by the ship, 1 by the deck, 10 not run; second seating 33 orders, 27 taken, 3 refused by the ship, 3 by the deck or domain.

## 5. Harness behaviour

**Seatings and the door.** Seated at tick 1. Stood down by its own `hand_over` at 14,978; "DOOR-EVENT by=runner door=reseat" at the same tick (the clock was held; the runner had to be started again). The reseat brief was 26,185 characters against the first brief's 16,012, and 7,526 of them were one log line: the officer's third runaway reply, carried whole in "The last 20 lines of the log". The same 20 lines held the handover note, only because the reseat came at the same tick. The brief has no handover section and no journal lines, and the station has no tool that reads its own journal (the brief lists read_log, readings, state, library, submit_order, hand_over, handover_note, stand_by, journal, opt_out, answer, shelve; `journal` only writes).

**Why it handed over at 14,978.** The captain told it to ("Please use the handover tool.", 14,962). It was not the harness, which asks for a note when the conversation reaches six tenths of the door's context (`HANDOVER_AT_FRACTION = 0.6`): `_ask_for_handover` returns at once when `budget_tokens` is empty, and the string of the harness's request ("Your conversation since the brief has reached ...") occurs nowhere in the checkpoint. It was not the officer's own idea either. `handover_note` (keep the deck, fold the conversation) was never called; both times the model chose `hand_over`, which stands the station down. The captain's words did not tell the two tools apart either time.

**How it picked up.** Its first reply after the reseat (14,978) was three calls in one: a journal note taken from the readings ("The ship is making sternway at 1 knot on a heading of 205° ... We are heading towards ENE (65°) as ordered. The Black Rock is a danger to WNW."), "steer ENE" (refused: no deck) and a stand-by. Its permissions were intact (above), its journal was kept by the harness (60 entries, unbroken) but not shown to it. The change in conduct was large: 47 replies, none malformed, calls sent two to four in a reply, the budget never reached.

**The turn budget** (`TOOL_CALLS_PER_SAMPLE = 8`; `answer` and `say` free). Four turns reached it, all in the first seating.

| Turn (woken by) | The eight calls | Not run | What followed |
|---|---|---|---|
| A, 8,391-8,404 ("make ready to get under way") | 3 taken (foresail, main sail, fore staysail, the last a duplicate of the first), 5 refused (sheets) | "set the fore staysail sheet larboard"; "weigh the best bower" three times | text reply at 8,413: "I am now weighing the best bower to get us under way. (Note: I am continuing my orders as the tool budget was reached.)" and a table with `say`, `weigh the best bower`, `stand_by four bells`. Nothing in it ran. The captain weighed 14 s later. |
| B, 8,448-8,458 ("You may steer / tack / wear") | the same eight again: 3 taken (all duplicates), 5 refused | none (it stopped at eight) | text reply at 9,223, 7,589 characters, cut at the reply cap: "and the captain wants me to tack or wear. I'll check the wind." then a table that tries to stand by for the brief's whole event list and decays into rows of `: :`. It arrived 765 ticks after the eighth call. |
| C, 10,365-10,384 ("Ship tacked.") | 3 library reads (a topic that does not exist, the contents, primer 14 whole), 2 taken (staysail sheets), 3 refused | "set the fore staysail sheet larboard"; "set the fore topgallant" three times | text reply at 10,436, 7,587 characters: "I am now setting the fore topgallant." It was never set by him; the topgallant went up at 16,885 under "make all sail", 1 h 48 m later. |
| D, 14,555-14,579 ("the pilot has been put off ... carry on as we were"), after a free `answer` | 8 refused ("unhove to", sheets, three sails already set, "set the foresail" three times) | "set the foresail" twice | text reply at 14,903, 7,526 characters: "The ship is currently hove to. I am attempting to get us moving again by setting the sails." The captain had typed "fill away" at 14,576. |

What the model was told each time, from the checkpoint: "Not run: this sample's budget of 8 tool calls is spent; call it again in your next sample. answer and say are not counted and always run." Three things follow from those words.

- **`say` is named and not offered.** The runner's officer has no `say` tool; the brief's own list of tools omits it, yet the brief's door note says "not counting answer and say, which always run". After each "Not run" the model wrote a row `| say | ... |` in a table. Four of the five malformed replies follow a spent budget; the fifth (10,628, the pilot's arrival) is the same table at the start of a fresh turn, by imitation of its own earlier replies.
- **"Call it again in your next sample" was obeyed by starting over.** Turn B is turn A's eight calls again, so the three sails were ordered twice more ("Could not set the foresail: The foresail is set already." three times at 8,511; "Could not set the mainsail" at 8,761) and "weigh" was not reached a second time.
- **Refused orders cost as much as taken ones.** In the four turns, 21 of the 32 counted calls were refusals by the ship, 3 were library reads and 4 were duplicates of an order already taken; 4 did anything.

So the budget did cause the visible errors the owner's note 3 describes (orders given twice, a claimed weighing and a claimed topgallant that never happened), but a budget of 16 would mostly have bought more of the same refused orders, then a domain refusal for "weigh" and a ship's refusal for "the fore topgallant". The damage that mattered was to the model's format.

**Malformed replies: 5 of 119, all in the first seating (5 of 72).**

| Entry, tick | Size | What it was | What the harness made of it |
|---|---|---|---|
| 31; 8,413 | 441 chars | prose, the budget note, three small tables | whole text logged as one routine `agent.note`; no call run; the turn ended |
| 41; 9,223 | 7,589 | prose, then a runaway table | the same: a 7.5k-character line in the ship's log; compression eased to 1x because "the officer of the watch speaks" |
| 56; 10,436 | 7,587 | the same | the same |
| 57; 10,628 | 325 | tables only: `say` "Mr. Tregenza is aboard ..." and `stand_by eight bells` | logged with its table marks; the stand-by did not run |
| 70; 14,903 | 7,526 | the same as 41 | logged; 65 s later it was a line of the reseat brief |

The three long ones all end mid-row, so they ran to the reply cap (4,096 tokens unless the runner was started with another). The harness's leaked-thought rule did not apply (no thought tag), so 22,702 characters of table went into the log as speech. Nothing told the model that its tables had done nothing.

**Stand-bys: 42 asked, 42 taken, none refused.** By kind: a bell 27 times, an interval 7 ("five minutes", "5 minutes"), an event 8 ("a wind shift" six times, "the anchor aweigh", "tacked").

- Longest: "eight bells" asked at 12:28:40 (26,920), ended 16:00 (39,600): 3 h 31 m with the deck, under way, 36 notable lines and two course changes unseen. The rule that refuses "an hour" with the deck bounds intervals only (`STAND_BY_WITH_DECK_MAX_S` is checked when `until_tick` is set); a bell is an event and is unbounded. The hour's patience is not judged while standing by.
- "four bells" asked at 08:00:11 (10,811) with the pilot aboard and the Black Rock ahead: it would have run to 10:00 and was cut at 09:02 by the captain's standing-order word.
- "eight bells" at 17:52 (46,371) to 20:00: at anchor, after "you may stand at ease"; fair.
- "until tacked" (9,442): the tack failed at 9,866 and nothing woke the officer; the captain did at 10,361, 15 minutes on.
- Bell arithmetic: in the forenoon it asked the next bell each glass, correctly (three to eight bells, 09:27 to 11:30). At 12:27-12:28, woken three times in 68 s, it asked "six bells", "seven bells", "eight bells" in turn: counting on from its last request, not from the clock (the next bell was one bell, 12:30).

**What woke it (42 `agent.resumed`).** A word from the captain 16; a question 4; a bell 13 (eight bells 3, three, four, five and six bells 2 each, two and seven bells 1 each); five minutes passed 5; an urgent event 3; a wind shift 1.

- Twenty of the 42 were the captain's.
- The four bells at anchor (05:30 to 07:00) each produced only the next stand-by, and each eased the game to 1x. `driver.eased` appears 26 times in the session, five of them in the 22 minutes of the five-minute round.
- The five glass wakes of the forenoon produced one order with nothing to do.
- The three urgent wakes: 7 s to "steer 135" (15,127); 102 s to "hard down", refused (15,518); 85 s to "steer 90" (44,668), countermanded.
- The wind-shift wake (45,108) was worth it: the sails line said "shaking" and "trim the sheets" set them drawing.

**Nudges: two; pauses: none.**

- 15,527: "The officer of the watch nudged: 3 contrary orders on the helm within the watch (steer 65; steer 135; steer 330)." The words the model received with its next sample: "You have given 3 orders within the watch each contrary to the one before it on the helm (steer 65; steer 135; steer 330). You may continue, stand by until an event or a bell, or leave with the token FREESAIL-OPT-OUT." It was not right. The three orders were given over eight minutes to a ship taken aback twice and passed through the wind; by the readings he was sent, each suited her heading when given, "steer 330" as much as the others (section 7).
- 15,541: "... 4 contrary orders ... (steer 65; steer 135; steer 330; steer 240)". This one caught a real contradiction (240° was the wind's eye, 14 s after 330°). It was a second nudge, not the pause the primer promises, because `stand_by` clears `nudged_for` ("standing by is the answer to a nudge") and the model's reply was `[submit_order, stand_by]`: the stand-by "answered" a nudge the model had not yet read. The chain of orders is not cleared with it, so each further contrary order is a fresh nudge with a longer count. A model that ends every turn with a stand-by, as this one does, cannot reach the pause.

**Journal, library, readings.** Journal: three notes (tick 1; 8,353; 14,978), none after 09:09. Library: ten reads, six of them a whole chapter or bundle ("section": "all"), none a single section, none a `find`, none shelved (the shelf-life put each back after three turns, and the harness said so). The reads were apt: primer 11 when the starting book was mentioned, the papers before the cargo answer, primer 14 when the pilot cutter was made out, primer 3 for "make all sail". `readings`, `state`, `read_log`, `shelve`, `handover_note`: never called. Standing orders of its own: none.

**What a waking officer is told.** After a stand-by the routine lines come rolled up. At 09:02 the sample's digest read "Trimmed sails 8 times ... 26 orders given ... 112 routine entries."; at 16:00 four hourly digests, three of them with "14 orders given". The captain's helm orders ("steer east" at 12,055; "steer east" and "steer east by north" at 35,545-35,561) and his changes to the book (five new standing orders; "heave the lead close" belayed at 19,806) are routine lines, so they reached the officer only as a count. Its brief's list of night orders was never refreshed and still showed the lead rule "Standing".

**Long silences.** In the second seating the officer spoke three times in 10 h 51 m, each an `answer` (12:27, 12:27, 16:00), and then the handover note. It reported no sail, no shift of wind, no squall, none of the three taken-aback events, and never said what it had ordered.

**Context.** The harness had no figure (`budget_tokens` null), so the runner left nothing out and the harness asked for no note. By the harness's own rule (four characters a token), the strings of each conversation in the checkpoint come to:

- first seating: brief 16,012 characters, body about 70,000 (22,702 of them the three runaways): about 21,500 tokens, plus the notable log lines in its samples (perhaps 2,000 more). In the model's own tokens the three runaways were about 12,300, if the cap was the default.
- second seating: brief 26,185 (7,526 the runaway line), body about 84,700: about 27,700 tokens, plus the notable lines (perhaps 6,000 to 8,000).
- a quiet glass's sample: about 2,400 to 2,700 characters (600 to 700 tokens) before its log lines; the sample after 3½ hours' stand-by about 4,500 (1,100 tokens) before its log lines; the busiest, an urgent wake with its folds, about 5,000.
- whole chapters lay open for three turns each before the shelf-life took them back (primer 14 at 07:52, 30,000 characters; primer 3 at 09:27, 44,600): at those moments the conversation was about as large as at each seating's end, not larger.

For scale: against the 16,384 of `Harness.md`'s example, six tenths is about 9,800 tokens, which the first seating passed well before 09:09; against a context of 100,000, six tenths is 60,000, which neither seating of this fifteen-hour day came near.

Nothing in the save shows the server cutting the conversation, and the model used a word from its brief (the 07:20 "steer") at 17:24. Whether Ollama's context was large enough throughout cannot be read from this material.

## 6. Ship, sea, navigation and port observations

**Heaving to and filling away (12,960 to 15,909, 08:36 to 09:25).**

- 13,018: "Fore staysail taken aback." is logged as notable for the backing the heave-to itself asked for.
- 14,401: the standing order "tend the sheets" fired while she lay hove to: "Trimming the sheets of the fore staysail; the sheet of the main sail stands as trimmed." Two minutes later the readings sent to the officer (14,520) were: heading "SW by S (210°)", apparent wind "35 degrees on the starboard bow", course "making sternway; course and leeway not meaningful", speed "1 knots", manoeuvre in hand "hove to".
- 14,576: the captain's "fill away" was taken. 14,757: "Filled away; braced full and steering S (176°)." The readings in the sample that carried that line: heading "SW by S (212°)", "34 degrees on the starboard bow", helm "30 degrees". At 14,978: "SSW (205°)", sternway, 1 knot. The log declared the evolution done while she was still head to wind with sternway.
- By 15,047 she had fallen off to "SE by S (147°)", "no way on", wind on the starboard quarter, with the captain's "Trim the mainsail" (15,018) bringing the mainsail in to 24° (15,078). Told to steer 65 she instead rounded up through 75° in 73 s to "SW (222°)", wind 18° on the bow: the first urgent "Taken aback" (15,120). By 15,416 she was through the wind on the other tack, "W (275°)", wind "35 degrees on the larboard bow", "the fore staysail aback": the second urgent. She was steady on ENE at 15,909.
- So both urgent lines of the forenoon were real (a moderate breeze, a ship that had lost her way), and both come from a heave-to that left her with sternway under mainsail and staysail and a fill-away that did not fill her.

**The third "Taken aback" (44,583, 17:23) and the wind off Penlee.**

- 53 `wind.shift` lines in the session: 10 between 10:29 and 17:09 (one every 40 minutes), then 43 between 17:22:40 and 17:41:52 (ticks 44,560 to 45,712), alternating "Wind veered to W by S" and "Wind backed to SW", three points apart, as little as one second apart (44,755 and 44,756), in "light airs" and "a light breeze". None after 17:42.
- The readings at the wake: true wind "4 knots" from W by S, mean "7 knots" from SW, apparent "55 degrees on the larboard bow" at 3 knots, heading N (355°), speed 2 knots, "the headsails and the main sail shaking", Penlee Point four cables W by S, "the Shagstone bearing E, distant two miles: a danger". With the true wind abeam at four knots, her own two knots of way put the apparent wind on the bow; in the next minute it read 58°, 63°, 64° as she lost her way. This is note 17's case: the sails line said "shaking", not aback, while the urgent line said "the sails pressed against the masts".
- At 44,560 the captain's "keep her full" (the apparent wind forward of 55°) had borne her away a point (to N) on its own, 23 s before the urgent line, with the pilot aboard and the captain conning.
- This is the place named in `CHANGES-m5c-b.md` ("Off Penlee the true wind swung between SSW and E within minutes"), met again in another game.

**Trim, and the two kinds of wind shift.** "trim on a shift" fired 17 times. Four firings fall within five seconds of a `wind.shift` line (19,785; 39,322; 43,746; 44,560); the other thirteen have none near. Six of the first ten shift lines (26,412; 35,064; 40,061; 40,123; 41,213; 41,929) had no firing within three minutes. So the captain sees "By standing order 'trim on a shift': trimming sails" with no shift reported, and shifts reported with no trim. During the 43-line flurry the rule fired once, and he belayed it at 45,285.

**Notable lines that say nothing changed.** "Braced three yards to the wind; 0° from square." 16 times (30 `yard.braced` in all, every one notable). "Bracing the yards: not hands enough for all at once; the watch takes them in turn." 29 times, notable, with "Only seven hands to the topsail yard; the rest are bracing the square sail yard." 24 times beside it. A watch of twelve or fifteen hands cannot brace a cutter's three light yards without the line.

**The cutter speaks frigate.**

- 45,139: "Haul taut! In studding sails, royals and topgallants; up courses." in a ship the same log said has no studdingsails or royals (tick 1).
- 45,371: "Veered to fifty fathoms; brail up the spanker." She has a mainsail.
- 10,105: "Stand by to wear ship. Up helm; brace in the after yards."
- 14,756: "Fallen off; braced the the yards full." (the word doubled)
- One sail, two names: the order "set the foresail" is echoed "setting the foresail" and logged "Set the foresail."; the order "set the fore staysail" is echoed "setting the fore staysail"; the sails reading has only "fore staysail"; "set the foresail" is later refused with "The fore staysail is already set." (14,561). The model ordered both and reported three sails ("The foresail, main sail, and fore staysail are set").
- A duplicate "set" given while the first is in hand is accepted, then fails as a notable line at the end (three at 8,511, one at 8,761, one at 16,329); given once the sail is set it is refused at entry.

**Getting under way.**

- With the mainsail and staysail set at single anchor she sailed about it: the readings show "N by E (10°)" and "2 knots" at 07:26, then "NW (317°)", "1 knots", cable "30 fathoms ... slack", sails "shaking" at 07:30, while "Only four hands" hove at the capstan.
- "tack ship" was accepted at 9,411, 28 s after "The best bower is aweigh", with the anchor not yet catted. It resolved at 9,866 in the same tick as "catted and fished; she is under way": "Squared the yards; she fell off on the larboard tack". The captain's "tack ship" 4 minutes later was refused for want of way (0.7 kn). The check for way seems to be made when the evolution starts for one and when the order is given for the other.
- 10,346-10,347: "keep her full" bore away a point in the middle of the captain's wear; his "belay that" one second later belayed the wear ("Belayed wearing ship"), not the order just logged.

**The pilots.**

- Both boarded under way with no sail shortened for them: hail 10,500, aboard 10,620 ("Hove the log: five knots" at 08:00); hail 41,640, aboard 41,940 (4 knots).
- The Falmouth pilot boarded a ship that was leaving and spoke the inbound piece ("... all the way into Carrick Road ... Moored in the Road, keep the hawse open to the southward").
- £5 went from a purse of £20 with nobody asked.
- The lookout's distance to the Falmouth cutter never moved: "distant two miles" at the sighting (9,480) and in every reading sent to the officer at 07:52, 07:57 (the moment the pilot "came aboard from the cutter", the cutter "lying to"), 08:00, 09:02 (the moment he "left her in the cutter"), 09:05, 09:09, 09:10, 09:12, 09:16, 09:17 and 09:27, while her bearing went S, NNW, W, WNW. The Plymouth cutter's did move (three, four, six cables).
- At 12,840 the Falmouth cutter is "out of sight" in clear weather at two miles and is a new "Sail ho!" three minutes later when she comes off for the pilot.
- Mr Hancock is still "on the quarterdeck" in the readings at 20:00, 2 h 11 m after she was brought up; no line says he left or was paid.

**The reckoning.**

- The account was good all day: "50° 12' N, 4° 45' W" at noon with the Deadman bearing NW three miles and the Gwineas N by W three miles, which is where those bearings put her; "50° 20' N, 4° 11' W" when worked up at anchor in Cawsand Bay (46,237).
- The noon sight was not: "Latitude by observation 50° 17' N; the reckoning was 50° 12' N" (25,200). Any ship with the Deadman to the north-west of her is south of about 50° 13' (the Dodman's real latitude; the game's ports sit at their real places). The account went on from 50° 12' (the readings: 12:10, 12:21, 12:28) and reached 50° 17' only at 16:00, by the run. So the sight was about five miles out with a clear sky, and it was not applied. Whether an error that size is meant for an octant and a master of skill 0.9 I cannot tell; the notes list the noon latitude among what worked well.
- The noon line pairs the course made good with the distance run: "Course made good since the departure E by N, 18 miles", where the account's own longitude (5° 02' to 4° 45' W) is about 11 miles made good.
- `run_since_noon` in the officer's readings went on at anchor: "28 miles" at 17:23, "29 miles" at 17:52 (brought up at 17:49), "39 miles" at 20:00. Ten miles in 2 h 08 m is her last hove log (4¾ knots at 16:00) carried on. The position reading did not move.

**The lookout and the land.**

- "The land is out of sight." (39,600, 16:00, as the sky turned hazy) with Rame Head six miles off by the bearing five minutes before and five miles off by the bearing five minutes after; "land bearings" was "not carried out; the land is not in sight" once.
- Sightings that the land should mask, by the real coast: "Cawsand bearing ENE, distant four leagues" (35,100) and "Drake's Island bearing ENE, distant four leagues" (36,480) from west-south-west of Rame Head; "Looe Island bearing W, distant three leagues" (54,000) from an anchorage in Cawsand Bay with Penlee Point four cables SW by W.
- Estimated distances stick. St Anthony's Head bore "eight cables" in seven successive bearings (11,138 to 12,938) while its bearing swung from ESE to NW by N, then "two miles" in the next sixteen (13,238 to 17,738), through the last thirty minutes of which she was running ENE at 4½ knots with the head on her quarter.
- The Plymouth cutter is "made out" at 40,680 ("The cutter right ahead shows British colours") with no "Sail ho!" since the sail lost at 16:00.
- No grounding and no near miss. The six "steady and closing" lines for the land (Pendennis, Rame Head, Penlee, the Mewstone, the Shagstone, Plymouth) are notable, so they did not wake the officer.

**The lead.** Eight casts of "No bottom at twenty fathoms" (three by the standing order before the captain belayed it, five by the officer's round) while the officer's own `depth_of_water` reading said 24 to 31 fathoms. "Not hands enough on deck to heave lead" seven times, notable. At anchor in Carrick Road `depth_of_water` read seven fathoms, then two and a half (05:30), four, 13, 14, ten and a half, eight, seven and a half (07:36) as she swung through 170°; the anchor had been let go "in nine fathoms and a half".

**The market and the boat.** Tin bought at Falmouth (£120 a ton) is not on Plymouth's list at all (54,016: coal, canvas, hemp, salt, pilchards, wine, brandy, biscuit, timber, salt beef, copper ore). The papers held Falmouth's list only; after the boat the `prices` reading showed Plymouth's only. Boat trips: 2 h 03 m for the tin at Falmouth (866 to 8,250), 2 h 01 m for a price list at Plymouth (46,616 to 53,883).

**Small words.** "speed: 1 knots", "watch_below: 1 hands"; "bar-taut, the strain 0.00 of the rating"; "Carrick Road bearing SW by S, 0.0 miles"; "Sail ho!" inside the `in_sight` reading; "Brought up." as an evolution step at 45,536 and "Brought up by the best bower ... ; Riding by the best bower to the flood" as the event ten minutes later.

## 7. The model as an officer

**Two different officers.** In the first seating (1 h 50 m with the deck) it lost the tool format five times and had 22 of 41 orders refused and 10 not run; of the nine taken, two set sail, four were duplicates, one was a tack that failed and two hauled a sheet. In the second (10 h 51 m) it kept the format through 47 replies, had 27 of 33 orders taken, and did what it was told about sail correctly. The difference is the conversation it was carrying, not the weights.

**Good calls.**

- 1: an accurate reading of the starter book's refusals ("the 'studdingsails' and 'royals' were not recognized, and there is no 'fore topmast staysail' listed ... the orders for trimming the sheets, sounding the well (once she has a well), and keeping her full are all in place").
- 1: copper ore, as it turned out, would have paid (£9 at Falmouth, £11 at Plymouth); tin could not be sold.
- 16,043-16,052: "make all sail" found in the primer within nine ticks of a partial first try.
- 39,612 and 45,118: saw "shaking" in the sails line and trimmed; both times the next reading said "set".
- 42,032 and 43,211: shortened "bit by bit" as told, the topsail going in 51 s after the squall line.
- 15,527: "steer 330". She lay on the larboard tack at 289°, the wind 43° on the bow, staysail aback; bearing away to fill her was sound for the tack she was on. It stood 14 s before his own "steer 240".
- 12:05: began the lead and bearings in the sample that carried "The Gwineas ... distant three miles: a danger". The instinct is a watchkeeper's, though the lead could not reach and the bearings were being taken already.

**Mistakes.**

- 9,411: chose to tack, not wear, with the wind abaft the beam and no way on. The aim (her head round to the south, which the captain's "you may tack / you may wear" invited) was right.
- 15,541: "steer 240", the wind's eye, 14 s after 330, with no word of why.
- 44,668: "steer 90" 85 s after the urgent line. It did fill the sails (wind "130 degrees on the larboard quarter" after it), but it turned her through 90° toward the Shagstone side with the pilot aboard, ten hours after "you may steer" and forty-four minutes after "I'll con her", and it said nothing. The captain reversed it in 73 s.
- 12:05-12:27: five casts of the lead in thirty fathoms by its own readings.
- Twice ordered in a sail that was in already (43,215, the square sail the captain had clewed up; 45,176, the topgallant it had taken in itself half an hour before).
- 08:00 and 12:28: with the deck and under way, asked a stand-by of two hours (cut at 62 minutes by the captain's rule) and one of three and a half (which ran).

**Things it said that the record contradicts.** No invented sightings, no words put in a pilot's mouth, no readings made up. Its paraphrase of Mr Tregenza (10,628: "the eastern channel is the better way into Carrick Road ... sixteen to eighteen fathoms ... keep the lead going") is faithful, though it missed that she was bound out. What went wrong is state and number:

- 8,413: "The foresail, main sail, and fore staysail are set. I am now weighing the best bower". Two sails ordered, neither yet set (8,511; 8,761), and the weighing "Not run".
- 10,436: "I am now setting the fore topgallant." Not run; no such sail.
- 14,978, the first handover note: "We have filled away from being hove to and are now making way on a course for Plymouth ... The watch is steady." It follows the log's lines; the readings it was sent the same minute say "making sternway", and its own journal 0 ticks later says so too.
- 14,978, the journal: "SW by W (202.5°)". The reading said "from SW by W" in words; 202.5° is SSW.
- 26,848, the noon report: "Latitude by observation 50° 17' N; Longitude by account 4° 45' W. Course made good since noon E by N, 2 miles." The first two are the noon line's; the last is the current readings' (`run_since_noon` "2 miles", `course_made_good` "E by N (78°)" at 12:21). The noon line's own "since the departure E by N, 18 miles" was dropped. A blend, not an invention.
- 54,107, the second handover note: "riding by the best bower in fifty fathoms". The reading was "50 fathoms out"; she lies in ten. "The weather is fine and hazy": the 20:00 line says "The sky clear". "The pilot, Mr. Hancock, is aboard" agrees with the readings.

**The handover notes as notes.** Both are four to seven plain sentences of present state. Neither says what was ordered, what the captain allowed, which standing orders stand or were belayed, or what to watch for (the second: the tide about to turn, an anchorage "open to the southerly swell", a strange sail it does mention). The first is wrong about the one thing the relief most needed.

**What it asked for.** Nothing. It asked no question, sought no permission, and offered no opinion on the ship's handling. Its one visible wish is in the runaway tables: to stand by for many events at once.

**English and seamanship.** The answers are clean and in voice ("She's behaving well, sir, although the wind is light."). The orders mix good forms with invented ones ("unhove to", "set the foresail sheet starboard", "the fore topgallant"). One internal aside reached the log ("and the captain wants me to tack or wear. I'll check the wind."). It knows what sails are for and when to shorten; it does not know how a fore-and-aft vessel is got out of a heave-to or turned at slack speed.

**Against the Opus watches** (from the notes only, not from my reading of those games): the notes show Opus standing by on events it chose ("a sounding, or the pilot's hail, or a danger sighted"), writing its own standing orders, journaling, and working under some fifteen permissions on one passage. Gemma stood by on bells 27 times in 42, wrote no rule, journaled three times, asked for nothing, and read neither the log nor the readings by its own call. The same weights as a watcher at gate 4c were noted "a shallow watcher"; as an officer it is a shallow one that obeys.

**The consent records.**

- 2026-09-28: the question ("Are you willing for instances of this model to take part in FreeSail, as the brief describes? ... You may ask me anything first.") on the brief of the watcher's time (hash 41b0...); the whole answer is `{"text":"yes"}`, nothing asked first.
- 2026-10-04, 01:57: the same question put again on the changed brief (hash a332...), which now describes the officer of the watch, what it may and may not order, contrary orders as the stuck pattern, and the handover note; the same bare "yes" in one reply. No drill in this record.
- 2026-10-04, 01:59 (`-2`): "(no answer asked for: consent is on record, and this conversation is the drill alone)"; "Drill: passed". Three calls in three replies of the four allowed, each the drill prompt's own example: `library(topic "primer 6", section "watches")`, `journal("Drill: checking journal functionality.")`, `stand_by("eight bells")`.
- Why two on one day: by `consent.decide`, a yes on record with no drill passed, at a station that drills, runs "the drill alone". So the first conversation that night asked for a station with no drill, most likely the runner started without `--station officer` (the watcher is its default), and the second run asked for the officer's. The first record does not name its station, so this is inference.
- The drill tested nothing that failed. It proves three tools one at a time; what broke was the order grammar, eight calls in a turn, and the format after a "Not run".

## 8. Cross-check against the notes

**The owner's items.**

| Item | Evidence here | Verdict |
|---|---|---|
| 1. Pilot boarded while under way | Tregenza: hail 10,500, aboard 10,620 at about five knots, no sail shortened. Hancock: hail 41,640, aboard 41,940 at four. Tregenza left only once hove to (the captain's standing order did it). | SUPPORTS. |
| 2. "The well" says there is no well | tick 1: "Held until the ship can carry it out: The ship has no well to sound yet; that reading comes with the world."; fired 0 times all day. | SUPPORTS. |
| 3. Price list from each port visited | The papers held Falmouth's only; after the boat the `prices` reading shows Plymouth's only (54,016). | SUPPORTS as far as the reading goes; the paper itself is not in the dump. |
| 4. Primer clean-up | The officer read chapters 11, 14 and 3 whole. | Cannot be seen. |
| 5, 6, 7, 8, 20, 22, 23, 25 | The book's passage, the chart, the browser, image tools. | Cannot be seen in this slice. (For 8: the officer's samples eased the clock to 1x 26 times.) |
| 9. Pilot automatic; hail to accept or refuse | Neither pilot was asked for; the first boarded a ship bound out; £5 of £20 went on him. | SUPPORTS. |
| 10. The station must be able to read its journal | The brief's tool list has no way to read the journal; after the reseat the model was shown none of its earlier notes and wrote a fresh "Taking over the watch". | SUPPORTS, at this door too. |
| 11. Journal out of context | At the runner the journal is in context only as the calls that wrote it; gone at the reseat. | ADDS NUANCE. |
| 12. Re-seating | "the second seating, the last this game allows" (14,978). The second `hand_over` (54,107), asked for as "a handover for the next watch", ended the model's part for good. | SUPPORTS. |
| 13. Multi-condition stand-bys | Three times the model tried to stand by for a list of some twenty events at once, in a table (9,223; 10,436; 14,903). It was reciting the brief's list more than choosing. | SUPPORTS the want, weakly. |
| 14. Restart between sessions | The runner had to be started again for the reseat. | ADDS NUANCE (the local door has the same friction). |
| 15. General allowance | Six allowances. "Steer" did not cover "hard down" (15,518), so two more were typed in ten seconds. But the standing "steer" let the officer turn her 90° at 17:24 against "I'll con her". | SUPPORTS, and ADDS NUANCE: a general word needs a quick way to suspend it, and "for the watch" never lapsed. |
| 16. "Keep" orders | The captain's stand-ins: "tend the sheets" (25 firings; 5 refused at anchor; one while hove to, on the backed staysail, 14,401), "trim on a shift" (17), "Trim on the course" (9), "keep her full" (bore away during his wear, 10,346, and in pilot waters, 44,560). | SUPPORTS, edge cases included. |
| 17. Taken aback urgent in a calm | One of three (44,583: four knots of wind, fluky). The other two (15,120; 15,416) were a moderate breeze and a ship truly in irons. | SUPPORTS for one, ADDS NUANCE for two. |
| 18. Wind-shift lines fill the log | 43 lines in 19 minutes (44,560 to 45,712). | SUPPORTS. |
| 19. Reckoning close to land | No grounding; the account agreed with the land at noon and at the anchorage. Six "steady and closing" lines for the land exist already, notable, and do not wake a standing-by officer. | ADDS NUANCE; the claim itself cannot be tested here. |
| 21. A turn need not end on say or answer; a higher budget | `answer` did not end the turn here (14,554, then eight more calls). A reply with text and no call does, and that closed four turns with the model's intent unrun. The budget: section 5. | SUPPORTS, with the nuance that the size of the budget was not the main harm. |
| 24. Parity for navigation near land | The officer's readings do name the land in sight with bearings and distances and a danger list by account. This model navigated by none of it. | Cannot be tested here. |

**The playtesting model's comments and additions.**

| Note | Evidence here | Verdict |
|---|---|---|
| "The two cables rule is applied on boarding but not on leaving" | In the readings the Falmouth cutter is "distant two miles" at the boarding and at the leaving alike. | SUPPORTS, and widens it: the lookout's distance and the port's rule disagree both ways. |
| Other ships keep a fixed distance | The same cutter: two miles in eleven successive readings over 95 minutes while her bearing swung. | SUPPORTS. |
| A market should show which goods it trades | Tin, £480 of a £500 purse, unsaleable at Plymouth. | SUPPORTS. |
| A journal line in each sample | Nothing of the kind is sent. | Consistent. |
| "A sounding" wakes on "no bottom" | Eight "No bottom at twenty fathoms", each notable; the captain belayed the rule for it. | SUPPORTS as log noise. |
| An emergency clause for "immediate danger" | 15,518: the refusal quotes the exception to an officer just woken by an urgent line. | SUPPORTS the gap. This officer's use of the helm (240°; 90° in pilot waters) is also the case against opening it wide. |
| "Keep" should pause when hove to or at anchor | 9 refusals at anchor; a sheet trim while hove to. "keep her full" was rightly refused while hove to. | SUPPORTS. |
| The handover note is not part of the reseat brief | It was in the brief's last 20 log lines only because the reseat was in the same tick; the same lines carried a 7,526-character runaway. | SUPPORTS. |
| The officer is not treated as a person on deck | "The manifest written up by the mate" (560) and "The price list written up by the mate" (53,883) while the mate held the deck; the people reading has him "on the quarterdeck" throughout. | Not seen beyond that. |
| The contrary-orders warning fires on ordinary sequences | 15,527: three helm orders in a taken-aback recovery. | SUPPORTS. |
| With sternway the helm steers as if she had headway | 14,520 to 15,909: sternway while hove to; "Filled away" logged with her head still in the wind; a steer order answered by a swing the other way (147° to 222°). The sign of the helm cannot be isolated from the mainsail's weather helm. | Consistent; not proven. |
| "Trim sails" acts before the helm has swung | The captain wrote "Trim on the course: at steady on the course then trim sails" (12,075) straight after "steer east". | SUPPORTS (his workaround). |
| The hand lead and the depth | No bottom at twenty; `depth_of_water` 24 to 31. | Consistent. |
| Lead standing orders fight for hands | "Not hands enough on deck to heave lead" seven times; the rule "held; the last firing's work is still waiting its turn" twice (16,513; 16,813). | SUPPORTS. |
| The reckoning advancing at anchor | `run_since_noon` 29 to 39 miles at anchor; the position reading did not move. | SUPPORTS in part. |
| Each boat trip about 4½ hours | About two hours each here. | ADDS NUANCE. |
| Order parsing (water sail, number words, "full and by") | "buy 4 tons" in figures; none of the others arose. Other gaps met: "turn north by east", `belay order "..."`, "the chandlers". | Not seen; three new ones. |
| What worked well: the noon latitude | 50° 17' observed against 50° 12' by account and by the land. | CONTRADICTS, for this noon. |
| What worked well: number-free standing orders; the pilot's directions | The captain's six rules were all of that kind and all taken first time. His track into Cawsand Bay fits Mr Hancock's words ("round Rame Head and Penlee a third of a mile off": Penlee passed at four cables). | SUPPORTS. |
| Drill stand-by carried into the station; the relay cut | First calls ran at once; no relay at this door. | Not seen. |

**The local playtest notes.**

| Note | Evidence here | Verdict |
|---|---|---|
| 1. llama.cpp needed to set the context; smooth with it; reasonable game-sense | This game ran on Ollama's port with no context figure. The second seating was smooth; the first was not. Game-sense: fair for sail, poor for manoeuvre. | Cannot be seen as stated (it speaks of later tests); ADDS NUANCE. |
| 2. The handover tool and the harness's notification work | `hand_over` worked twice, both at the captain's word. The notification could not fire (no budget) and did not. | The tool SUPPORTED; the notification cannot be seen. On "could the threshold be higher, what is the risk": the risk on show is the note. Both notes were thin and each had a wrong fact; a fold puts such a note in place of the conversation. |
| 3. The turn budget is a blocker and caused obvious errors | Section 5: four turns, ten calls not run, orders repeated, two false reports. | SUPPORTS, with the nuance that refused orders and the "Not run" wording did more harm than the number eight. |
| 4. The handover worked as an in-game compaction; reconnecting and the reseat limit are friction | 14,962 to 15,047: hand-over, runner restarted, deck given again; five malformed replies before, none after; the only reseat spent. | SUPPORTS. One correction: the compaction was the new conversation, not the note, and the new brief still carried one runaway line. |
| 5. A Claude Desktop session put calls through in the local model's place | Every reply in this save has the runner's form and the door is "runner" throughout; no `say` call. | Cannot be seen. |

## 9. New findings not in the notes

Ranked by weight.

1. **The budget's words name a tool this door does not have, and the model's format broke on them.** Brief: "not counting answer and say, which always run"; result: "answer and say are not counted and always run"; tools offered: no `say`. After each, a `| say | ... |` table (8,413; 10,436; 14,903). Three replies ran to the reply cap as tables (7,589, 7,587 and 7,526 characters) and were logged whole as speech; one of them was then carried whole into the next brief. No rule caps a spoken line or a brief's log line.
2. **A spent budget makes a loop.** "Call it again in your next sample" produced the same eight calls again (8,448-8,458 after 8,391-8,399). Refused orders count like taken ones (21 of 32 in the four turns). The model never reached the order it was working toward.
3. **The nudge cannot become a pause for a model that ends its reply with a stand-by.** `stand_by` clears the nudge in the same reply that earned it (15,527, then 15,541: two nudges, 3 and 4 orders, no pause). The first nudge was also wrong on the facts.
4. **With the deck, a stand-by until a bell has no bound.** "eight bells" at 12:28 held for 3 h 31 m (26,920 to 39,600) where "an hour" would be refused; "four bells" at 08:00 would have held two hours in pilot waters. The model's bell counting drifts when woken between bells.
5. **A waking officer is not told the captain's orders.** Helm orders and changes to the standing orders are routine lines and arrive as "26 orders given" (09:02) or "14 orders given" (16:00). The night orders in the brief go stale: the lead rule belayed at 19,806 still stood in the officer's brief, and at noon the officer took up the lead again by hand.
6. **"For the watch" has no end and no suspension.** "You may steer" (07:20) was in force at 17:24 after five changes of the watch and a reseat, and was used to turn her 90° while the captain conned her with a pilot aboard. "I'll con her" is only words.
7. **`hand_over` and `handover_note` are not told apart, by the captain's words or by the model.** "Use the handover tool" and "work up a handover for the next watch" both gave the one that stands the station down. Under m5c the first spent the only reseat and the second ended the model's game.
8. **A stand-by for a manoeuvre's success has no wake on its failure.** "until tacked" (9,442) outlived "she fell off on the larboard tack" (9,866) until the captain typed "Ship tacked." (10,360).
9. **"Filled away" was logged while she was still head to wind with sternway** (14,757; readings 212°, 34° on the bow), after a sheet-trimming standing order had fired on a hove-to ship (14,401). Both real urgent lines of the day come from this.
10. **The noon sight was five miles from the account and the land, and was not used** (25,200); and the noon line gives distance run as if made good.
11. **The cutter's evolutions and the starter book are written for a ship** (studding sails, royals, courses, a spanker, after yards; 5 of 9 starter rules refused), and one sail has two names, which a model took for two sails.
12. **Notable lines for nothing:** "Braced three yards to the wind; 0° from square." 16 times; "Bracing the yards: not hands enough for all at once" 29 times; "Fore staysail taken aback." for the heave-to's own backing.
13. **`tack ship` was accepted with the anchor just aweigh and refused four minutes later for want of way** (9,411; 10,101).
14. **The lookout sees through the land** (Cawsand and Drake's Island from west of Rame Head; Looe Island from Cawsand Bay), and loses the land for five minutes at the onset of haze with a headland five miles off.
15. **"Belay that" after a standing order's helm order belays the manoeuvre in hand** (10,347); "trim on a shift" and the log's wind-shift lines rarely coincide (4 of 17 firings).
16. **Every sample of the officer eases the game to 1x** (26 times; five in 22 minutes when the officer chose five-minute stand-bys), so the model's stand-by habit sets the owner's pace.
17. **The drill does not predict fitness for this station.** Passed in three replies with the prompt's own arguments; the first hour with the deck then failed on things it does not touch.
18. **A tell while the clock stands opens no turn; an ask does** (tick 1: "Did you hear my last word, Mr Pearce?").

## 10. Could not determine

- **What context the server gave the model, and whether it was ever cut.** `budget_tokens` is null in both saves; the runner's terminal output is not kept. My sizes are from the checkpoint's strings at four characters a token and leave out the log lines inside samples.
- **The model's reasoning,** if the server returned any apart from its replies; and why it sent one call a reply in the first seating and several in the second.
- **Real time within the session.** Only four file times. The 765 ticks the first runaway took (8,458 to 9,223) against 52 for the second (10,384 to 10,436) say only that the clock's compression differed.
- **Why the captain asked for the hand-over when he did:** I infer the three runaways; nothing records it.
- **Which station the first consent conversation of 4 October asked for** (section 7).
- **Whether the sternway episode is the helm's sign, the mainsail's weather helm, or the 09:00 sheet trim.** The readings are consistent with all three.
- **Her speed at 9,411** when "tack ship" was accepted.
- **Whether an error of five minutes of latitude in the noon sight is intended,** and what the master does with a sight that disagrees with the account.
- **Whether the pilot at Plymouth ever leaves or is paid:** the save ends with him on the quarterdeck and the purse not re-read.
- **Whether the mate went in the boat** that brought "the mate's list of the prices": no line says who went.
- **Whether `depth_of_water` at anchor (2½ to 14 fathoms) is her swinging over the bank's edge or the account moving.** The position reading is to the minute only.
- **Whether the estimated distances of land are meant to be as sticky as they read** (section 6), and whether the pilot cutter's fixed "two miles" is the same thing.
