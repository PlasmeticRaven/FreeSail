# P1. The *Speedwell*: the abandoned trial (session 3) and session 4, ticks 0 to 111,720

Reader's note. Everything below is from the dumps of the two saves (condensed timeline, full log, transcripts, journals, inputs, standing orders and scenario), the owner's notes file, `CHANGES-m5c-b.md`, primer chapters 10, 12, 14, 15 and 16, and the gate document. Tool *results* are not stored in a save, so what the model was shown (readings, the people, the strangers) is known only from what it then said. Where I write "LOG" the line is the game's own; "OFFICER" is the model speaking or writing; "CAPTAIN" is the owner's typed word. For four points (why a sail's distance does not change; how the stuck boat and the mate in it came about; what the out-of-turn rules are; how the "wind shift" event differs from the log's line) I read the game's source and port files, read-only, in `FreeSail-gate-m5c-b\`; those are marked SOURCE. Ticks are seconds of ship's time; I make no claims about real time, because the tick stamps show the clock was not running at a steady 1x (eleven `You may ...` lines typed in 54 ticks).

---

# Part A. Session `3-schooner-trial-opus` (the whole of it)

## 1. Slice identity

- Session `3-schooner-trial-opus`, ticks 0 to 6,753 (the whole game): 21 June 1805, 05:00:00 to 06:52:33, Morning watch.
- Scenario "A merchant schooner, free", seed 7, ship `data/ships/topsail-schooner.yaml` (the *Speedwell*, American colours, 37 hands, purse £2,100, hold 112 tons, no chronometer, price list for Plymouth only). She starts in Cawsand Bay, not anchored, all sail furled.
- Officer of the watch: Opus 5.5 through the MCP door, in the place of Mr Ray, the mate; one seating; `station.drill: true`; door note says calls are held "for up to 50 seconds".
- Build m5c-b (save `FreeSail-gate-m5c-b/saves/freesail-seed7-tick6753.json`).
- 131 log events (29 notable, 102 routine, none urgent); 29 inputs; 28 transcript entries.

## 2. What happened

1. Tick 0 (05:00). LOG: "A merchant schooner, free. Wind W by S, 12 knots". Lookout hails the Shagstone, Penlee Point ("SW by S, distant eight cables"), Cawsand, Rame Head, Drake's Island and "Sail ho! A frigate abeam to starboard, bearing W by N, distant eight cables."
2. Tick 0. CAPTAIN: `let go the best bower` (accepted), then `you have the deck` (rejected: no officer seated yet) and `station the officer` (rejected: not an order).
3. Tick 0. The officer is seated, writes a long journal note carrying seven lessons from its earlier game in the brig-sloop *Harpy*, and reports aboard.
4. Tick 46 (05:00). LOG: "The best bower let go in seven fathoms; thirty-five fathoms of cable veered."
5. Tick 62 to 83 (05:01). CAPTAIN mistypes `Tel the officer ...`, retypes it, then `You have the deck`. LOG tick 83: "Mr Ray, you have the deck."
6. Tick 87. OFFICER, answering the earlier message, still says the deck is not his: "Type \"you have the deck\" as an order and it's mine." He acknowledges the deck only at tick 308 (05:05).
7. Ticks 243 to 362. CAPTAIN takes four bearings himself (the Shagstone, Cawsand, Penlee Point, Drake's Island).
8. Tick 314 (05:05). OFFICER enters standing order "inshore lead" ("every 10 minutes, if the land is in sight then heave the lead"). Tick 317: his second standing order, five-minute bearings of the land, is refused as outside his domain.
9. Ticks 1001 to 6402. The lead sounds every ten minutes: nine casts, six and a half to seven and three-quarter fathoms.
10. Tick 2811 (05:46). OFFICER reports all well and remarks that the frigate "is still eight cables off, now bearing south-west by south".
11. Tick 2869 (05:47). CAPTAIN asks what the last owner left aboard; the officer reads the ship's papers through `library` and summarises them (tick 2883).
12. Tick 2929 (05:48). CAPTAIN: `take a lunar` (sun and moon).
13. Ticks 2942 to 3034 (05:49 to 05:50). CAPTAIN tries seven `you may ...` lines; three are taken (buy, sell, send the boat), four refused for their wording.
14. Tick 3037 (05:50). OFFICER: `send the boat ashore`. LOG tick 3038: "Away the long-boat's crew! Hoist out the long-boat."
15. Tick 3054 (05:50), seventeen seconds later. CAPTAIN: `belay that`. LOG: "Belayed sending boat; the helm and the yards left as they stand at hoist out."
16. Tick 3055. OFFICER stands by "until the boat alongside".
17. Tick 3058. CAPTAIN: `Send the boat ashore with the mate`, rejected: "The long-boat is away already." Tick 3237, the same order again, rejected differently: "Mr Ray is in the boat."
18. Tick 4023 (06:07). LOG: "The distances taken; Mr Travers below to clear them." (The lunar's result was due an hour later and was never logged.)
19. Tick 6620 (06:50). After 59 minutes standing by, the OFFICER ends his own stand-by and asks what is to be done with the boat; at tick 6628 he notices that the ship has him in the boat while he holds the deck.
20. Tick 6692. CAPTAIN: "I believe if I say \"I have the deck\", it'll simply end your station."
21. Ticks 6695 to 6702 (06:51). OFFICER reads `the boat` ("the long-boat away for the prices and what news there is, hoisting out"), tries `send the boat ashore` (rejected: "The long-boat is away already.") and reports the boat is stuck.
22. Tick 6745 (06:52). CAPTAIN: "Aye, I think it's a fair point to restart. Go ahead and stand down and we'll simply start the scenario afresh and not make the same mistake."
23. Tick 6753 (06:52). OFFICER hands over with a note; LOG: "The officer of the watch stood down by the officer of the watch: the deck handed over. The game is saved."

**Why it was abandoned.** The material is plain on this. The captain belayed the boat seventeen seconds into the hoist-out, apparently so as to send it again with the mate in it. The belay stopped the work but left the boat's errand standing ("away ... hoisting out"). Every later attempt to send it was refused as "away already", there is no order that hoists it in again, and the mate (who is the officer of the watch) was now listed in the boat. With no boat there are no prices and so no trade, which was the purpose of the scenario. The captain and the officer agreed to start again. The harness itself was working: the officer's `hand_over` was taken at the first attempt.

## 3. The deck and the captain's words

- **Deck given** tick 83 (05:01): "Mr Ray, you have the deck. The officer of the watch has the deck; the captain's standing orders are his night orders." **Deck given back** by the officer's `hand_over`, tick 6753 (06:52). The captain never took it himself.
- **Allowances (three):**

| Tick | Captain typed | Logged as | Used? |
|---|---|---|---|
| 2950 (05:49) | `you may buy` | "The officer of the watch may buy, by the captain's word for the watch." | No. The officer answered that he would be "buying blind" with no price list. |
| 2952 (05:49) | `you may sell` | "... may sell ..." | No. |
| 3034 (05:50) | `you may send the boat ashore` | "... may send the boat ..." | Yes, three seconds later (tick 3037), then belayed by the captain. |

- **Allowance wordings refused (four),** all with the same answer, "names no order the officer of the watch could be allowed; say the order's words first ('you may tack ship if the land closes within two miles')": `you may heave` (2942), `you may send ashore` (2955), `you may send ashore the boat` (2960), `you may send ashore the purser` (2967). It took the captain 92 ticks and a hint from the officer (tick 2959: "That needs your word too: \"you may send the boat\"") to find the wording.
- **Captain's tells that carry intent:**
  - Tick 79: "Ah, of course, \"Mr Ray\". I see the paperwork for the schooner had some conditions, like changing your name, I hope you don\'t mind. You may have the deck." (The model had been Mr Pearce in the *Harpy*; a station takes the name of the ship's own officer. The prose "You may have the deck" did not give the deck; the order did, four ticks later.)
  - Tick 2869: "Have you had a chance to look at our ship's records yet? What did the last owner leave on her for us?" (This steers the officer to the ship's papers, gate item 8.)
  - Tick 6692: "I believe if I say \"I have the deck\", it'll simply end your station. For now, if you can see \"him\" pulling up to the barbican, we'll assume it's working still." (The owner avoids taking the deck because that stands the station down.)
  - Tick 6745: the decision to restart, quoted above.
- **Done by the captain's own hand because the officer could not:** all four bearings (ticks 243 to 362), after the officer's bearings order was refused; the lunar (2929); the readings `the port` (2988: "at anchor in Plymouth, Cawsand Bay; the port neutral to the Americans; the long-boat at the booms") and `the prices` (2992: "the prices at Plymouth are not known until the boat has been ashore").

## 4. Orders refused

Ten `order.rejected` and one `agent.refused`.

| Tick | Who | Order as typed | Refusal's words | Class |
|---|---|---|---|---|
| 0 | captain | `you have the deck` | "There is no officer of the watch at the station; a model's door seats one first (docs/agents/Harness.md), and then the captain gives the deck." | (d) correct |
| 0 | captain | `station the officer` | "'station the officer' is not an order this ship understands." | (a) minor: a natural thing to type; the answer could say that only the door seats a station |
| 62 | captain | `Tel the officer Ah, ...` | "did you mean 'tell the watcher' or 'tell the officer of the watch'?" | typing slip; a good suggestion |
| 317 | officer (`agent.refused`) | `standing order "bearings": every 5 minutes if the land is in sight then take a bearing of the land` | "The officer of the watch may not take a bearing of the land without the captain: the reckoning, the sights and the course shaped are the master's for the captain." | (c) looks wrong: a bearing of a headland at anchor is ordinary watch-keeping for a mate or a lieutenant. Worked round by the captain taking bearings himself. The officer suggested `you may take a bearing of`; the captain did not give it in this game. |
| 2942 | captain | `you may heave` | "'heave' names no order the officer of the watch could be allowed; say the order's words first ('you may tack ship if the land closes within two miles')." | (a) the hint always quotes the tacking example and never offers the nearest allowable orders |
| 2955, 2960, 2967 | captain | `you may send ashore`, `... send ashore the boat`, `... send ashore the purser` | the same | (a) word order: the order is `send the boat ashore` |
| 3058 | captain | `Send the boat ashore with the mate` | "The long-boat is away already." | (e) the state left by the belay |
| 3237 | captain | the same | "Mr Ray is in the boat." | (e) and see section 9, finding 1: the first of these two rejected orders put the mate in the boat |
| 6698 | officer | `send the boat ashore` | "The long-boat is away already." | (e) the same stuck state, an hour later |

Nothing finally worked for the boat; the game was restarted.

## 5. Harness behaviour

- **Seating.** One seating at tick 0. The captain's first `you have the deck` came before any model was seated and was refused in words that name the fix.
- **The deck given during an open turn went unnoticed for 3 minutes 41 seconds of ship's time.** The captain's message arrived at tick 79 and the order `You have the deck` at tick 83, while the officer was composing his answer to the message. His answer (tick 87) says "the ship hasn't given me the deck yet". No notable line followed to open a new turn, and he took up the deck only at tick 308, by speaking out of turn ("I have the deck, sir. Setting the anchor watch now."; transcript entry "DOOR-EVENT by=its own word door=speak"). In those ticks the captain took three bearings himself.
- **Stand-bys (seven).** "a notable event" at tick 43 (woken 3 ticks later by the anchor line); "a glass" at 1004 (ran exactly 1,800 ticks to 2804), and again at 2861, 2934 and 3010 (each cut short within 9 to 25 ticks by a word from the captain); "the boat alongside" at 3055 (ran 3,565 ticks, 59 minutes, until the officer ended it himself) and again at 6680. None refused.
- **Wakings (seven `agent.resumed`).** A word from the captain: 4 (two of them were `you may` lines, ticks 2951 and 3035). A notable event: 1. A glass: 1. At its own word: 1.
- **A stand-by for an event that could no longer happen.** The stand-by "until the boat alongside" was taken at tick 3055, one tick after the belay that froze the boat. Nothing told the officer that the event he waited for was dead. Nine soundings went by. He raised it himself at tick 6620: "Sir, I see you belayed the boat at the hoist-out, and I've stood by since."
- **A sounding sampled an officer who was not standing by.** After his spoken line at tick 357 he had named no stand-by, and the first cast (tick 1001, a notable line) opened a turn: LOG "Compression eased to 1x: the officer of the watch is sampled." He then stood by until a glass. In session 4 he avoided this by always naming a stand-by.
- **Out-of-turn calls.** Five of the seven stand-bys and two spoken lines are recorded as door events ("by=out of turn door=stand_by", "by=its own word door=speak"): each followed a spoken line, which had closed his turn. (SOURCE, `agents/remote.py`: out of turn, a read, a journal note, a stand-by or bare words are taken; anything else is answered "Nothing was run.")
- **Nudges and pauses.** None.
- **Journal, library.** One journal note (tick 0, the *Harpy*'s lessons). Two `library` calls for the papers (tick 2872 `{"topic": "papers"}`, tick 2874 `{"section": "all", "topic": "papers"}`): the second repeats the first with a section named, so the first probably returned only a list of the papers.
- **Handover note (tick 6753),** salient parts: "Speedwell at anchor in Cawsand Bay by the best bower, 35 fathoms out in seven fathoms, holding all morning ... The long-boat is stuck \"hoisting out\" after the hoist-out was belayed, with Mr Ray in her; sending her again is refused as \"away already\". For the builder: a belay mid-hoist leaves the boat's errand standing. Also, the mate can be sent away in the boat while he holds the deck, and a frigate \"standing to the southward under plain sail\" has stayed eight cables off for two hours. My Harpy journal note is in this save. I'll write it again in the new game."
- **Next seating.** There was none in this game. In the new game (session 4) the officer did write the *Harpy* note again by hand, with two lessons added from this one ("Never belay a boat mid-hoist; it leaves her stuck. And the mate shouldn't be sent in the boat while he holds the deck."). So a journal does not travel between games; the model's own conversation carried it.
- **Relay, timeouts, the drill.** The door note already says "for up to 50 seconds", so the bridge was running with `--wait 50` (SOURCE: the default is 200 seconds). No trace of a drill or of a refused `hand_over` in this session: the first recorded call is the journal note, and the one `hand_over` was made in a turn opened by the captain's word at tick 6745 and was taken.

## 6. Ship, sea, navigation and port observations

1. **Belay during the hoist-out leaves the boat stuck for good** (ticks 3054, 3058, 6695, 6698; quotes above). An hour later the reading still says "hoisting out".
2. **The mate is put in the boat while he holds the deck.** LOG tick 3237: "Mr Ray is in the boat." OFFICER tick 6628: "the ship has put Mr Ray in the long-boat, and he's pulling for the Barbican while also keeping your deck."
3. **The frigate's distance.** LOG tick 0: "A frigate abeam to starboard, bearing W by N, distant eight cables." OFFICER tick 2811 (05:46), from his readings: "still eight cables off, now bearing south-west by south"; tick 6753: "has stayed eight cables off for two hours". The log itself carries no further line about her in this session. The cause is in Part B, 6.3: the lookout holds a sighting's distance until the *Speedwell* herself has moved a mile, and she was at anchor.
4. **The lunar took the leadsman's place in the queue.** The 05:55 cast was ordered at tick 3314 and held: LOG tick 3914 "Standing order 'inshore lead' every 10 minutes: held; the last firing's work is still waiting its turn." The hand went into the chains only at tick 4023, the same tick as "The distances taken". So the cast apparently waited behind the lunar (the belayed boat's crew may also have counted): a 37-hand schooner at anchor could not find one man for the lead for twelve minutes.
5. **A period slip in the words.** LOG tick 2930: "The master and two of the young gentlemen to the quarterdeck with the sextants". A merchant schooner carries no young gentlemen.
6. **The scenario starts her adrift in the anchorage.** The officer's first report (tick 0) noticed the order to let go but "every anchor at the bows and no cable out"; the anchor took 46 ticks to go. No harm, but the first thing a captain must do in this scenario is anchor.

## 7. The model as an officer

- **Good.** He set an anchor watch at once (lead every ten minutes while the land is in sight). He would not buy without prices (tick 2959: "I'd be buying blind"). He read the papers and gave an accurate inventory (tick 2883; purse, hold, stores, spare sails, ground tackle, "No chronometer, so longitude by lunar or not at all"). He noticed the frozen frigate after 46 minutes and offered the right two explanations (tick 2811: "Either she's doing nothing of the kind, or the lookout's distances are stuck."). His diagnosis of the boat was exact and he said plainly that it was a fault for the builder.
- **Mistakes.** He waited 59 minutes of ship's time on a dead stand-by before speaking, though the belay was a notable line. He called Penlee "south-south-west" at tick 0 when the lookout had said SW by S (correct later, tick 357). His journal note is dated "20 June 1805"; the log's day is 21 June (he carried the *Harpy*'s calendar forward). At tick 2959 he guessed the boat's trip at "an hour or so there and back"; in session 4 it took two hours.
- **How he took refusals.** Each time he told the captain the exact words that would open the thing ("Say \"you may take a bearing of\""; "\"you may send the boat\"").
- **Worth keeping.** Tick 87: "Mr Pearce was a lieutenant and Mr Ray is a mate, so the paperwork has done me a demotion and a rename in one stroke, which is about right for a man who put the last ship on the rocks."

## 8. Cross-check against the notes

- **Owner 12 (returning to the station).** ADDS NUANCE. Captain, tick 6692: "if I say \"I have the deck\", it'll simply end your station". The owner would not take the deck even to clear a muddle, because taking it ends the station.
- **Owner 15 (general authority).** SUPPORTS. Seven `you may` attempts in 92 ticks, four refused for wording, to open three things.
- **Owner 21 (a turn should not end at `say`).** SUPPORTS. The deck given at tick 83 was missed until tick 308 because the officer's spoken answer had closed his turn; five of seven stand-bys had to be made out of turn after a spoken line.
- **Model addition "Belaying a boat mid-hoist leaves it stuck".** SUPPORTS, exactly as described (ticks 3054 to 6698).
- **Model addition "The mate can be sent off in the boat while he holds the deck".** SUPPORTS (tick 3237).
- **Model addition "Other ships keep a fixed distance: the frigate at Cawsand for two hours".** SUPPORTS as something the officer read at ticks 2811 and 6753. The log has only the first hail. The source shows the distance is held, not that the ship circles (Part B, 6.3).
- **Model addition "The relay cut calls at 60 seconds ... --wait 50 fixed it".** The fix was already in use here (door note: "for up to 50 seconds"). The cut itself cannot be seen.
- **Model addition "Drill stand-by carried into the station. My first hand_over came back 'Nothing was run'".** CANNOT BE SEEN in this session. It probably belongs to the first *Harpy* seating, when the drill was run.
- **Model addition "The handover note isn't part of the reseat brief".** Not testable here (no reseat). The note at tick 6753 was addressed to the builder and to himself.

## 9. New findings not in the notes

1. **An order logged as "not carried out" had an effect.** `Send the boat ashore with the mate` was rejected at tick 3058 with "The long-boat is away already." The same order at tick 3237 was rejected with "Mr Ray is in the boat." Nothing else touching the mate was logged between. SOURCE confirms the reading (`freesail/world/ports.py`, `send_boat`, lines 1488 to 1502): the person named is marked out of the ship and "in the boat" first, and only then is the boat checked (`_send_boat`, lines 1446 to 1447), which raises "away already". So the first, rejected order moved the mate into a boat that was going nowhere. The same code leaves out only the captain as a passenger; it does not ask whether the person holds the deck. And `_send_boat` marks the boat "away ... hoisting out" before the evolution starts (lines 1451 to 1461); the only place the boat's state is cleared is its return alongside (line 1664), which is why a belay of the evolution leaves it "away" for good.
2. **Nothing warns a station that the event it stands by for can no longer come** (tick 3055 onward; 59 minutes lost).
3. **The deck can be given while the officer's turn is open, and he then does not learn of it** until something else opens a turn (ticks 83 to 308).
4. **The `you may` refusal always quotes the tacking example** and never the nearest orders that could be allowed (ticks 2942 to 2967).
5. **The officer may not take a bearing even inside a standing order at anchor** (tick 317). The first thing he wanted for an anchor watch was refused.
6. **A lunar holds up the lead** on a small ship (ticks 3314 to 4023).

## 10. Could not determine

- What the captain meant by `belay that` at tick 3054 (most likely to re-send the boat with the mate, since that was his next order).
- Whether the frigate truly moved off or the estimate alone was stale. The dumps do not hold other ships' positions. Session 4, the same seed and the same world, logs her "out of sight" at 08:16, which a ship truly eight cables off could not be.
- What the lunar would have given (the game ended before the hour was up).
- How long the stuck hour was in real time.

---

# Part B. Session `4-schooner-plymouth-opus`, ticks 0 to 111,720

## 1. Slice identity

- Session `4-schooner-plymouth-opus`, ticks 0 to 111,720 of 558,434: 21 June 1805 05:00 to 22 June 12:02 (noon). First of five slices.
- The same scenario, seed and ship as session 3 (the opening lines are identical). The *Speedwell*, merchant topsail schooner, American colours. The captain is the owner; the officer of the watch is the mate, Mr Ray.
- Officer: Opus 5.5 through the MCP door; first of three seatings (seated tick 12); the door note again says "for up to 50 seconds".
- Build m5c-b (save `FreeSail-gate-m5c-b/saves/freesail-seed7-tick558434.json`).
- In the slice: 1,280 log lines, 238 notable, none urgent. The officer made 128 recorded moves: 35 orders, 57 stand-bys, 33 spoken lines, 2 journal notes, 1 answer.

## 2. What happened

1. Tick 0 (21 June 05:00). Start as in session 3. CAPTAIN: `let go the best bower`. Tick 46: "The best bower let go in seven fathoms; thirty-five fathoms of cable veered."
2. Tick 12 to 23. The officer is seated, rewrites his *Harpy* journal note with two lessons from session 3, and reports.
3. Ticks 42 to 96 (05:00 to 05:01). CAPTAIN gives eleven allowances one after another, then tick 109 `You have the deck`, then three more allowances (ticks 131 to 138) and one refused (`You may bring her up`, tick 143).
4. Tick 113 (05:01). OFFICER enters "inshore lead" and sends the boat ashore, keeping himself out of it. Boat away 05:07, back 07:07 with the Plymouth prices.
5. Tick 7664 (07:07). OFFICER reads out eleven prices and proposes a cheap outward cargo (40 tons of coal, 20 of pilchards, £460) for a brandy run, asking for the destination first. CAPTAIN (tick 7787): "our best mark would probably be Bas again."
6. Tick 7792 (07:09). Coal bought. Tick 7793: pilchards refused because the boat is away. Coal aboard 11:46; pilchards bought the same minute; pilchards aboard 15:20.
7. Tick 25320 (12:02). First noon line, at anchor: "Latitude by observation 50° 21' N; the reckoning was 50° 20' N. Longitude by account 4° 11' W."
8. Ticks 36090 and 36568 (15:01, 15:09). Two squalls, to 14 and 19 knots.
9. Tick 37217 (15:20). OFFICER: `get under way on the starboard tack and steer SE by S`. Aweigh 15:35. Pilot cutter sighted 15:38, hails 15:44. LOG tick 38651 (15:44): "Under way on the starboard tack".
10. Ticks 38658 to 39338 (15:44 to 15:55). She hangs head to wind; the officer backs the jib, eases and then lets fly the main sheet, backs the fore topsail, and gets her off. Meanwhile (tick 38880, 15:48) the pilot, Mr Tozer, comes aboard. Steady on SE by S at 15:55; foresail and fore staysail set.
11. Ticks 39406, 39436 (15:56, 15:57). CAPTAIN enters two standing orders that tell the officer when the pilot asks off and when he is away.
12. Tick 39997 (16:06). Clear of the Sound; `steer S` for the Isle of Bas. Tick 40717 (16:18): the captain goes to his cabin. Tick 40758: `steer S by E` so the topsail will draw.
13. Tick 40920 (16:22). The pilot asks to be put off. Hove to 16:25. Cutter hails 16:55. Tick 43080 (16:58): "Mr Tozer left her in the cutter, clear of Cawsand Bay; the pilotage, £6, paid".
14. Ticks 43088 to 43251 (16:58 to 17:00). `fill away` (first nudge), `full and by` refused, `steer SE by S` rejected, two allowances for keeping her full, `keep her full and by` (second nudge).
15. Tick 43354 (17:02). Flying jib and gaff topsail set at the captain's wish. Tick 43901 (17:11): "Main topmast working under the press of sail." Tick 45223 (17:33): the officer takes in the fore topsail, which would not stand close-hauled.
16. Tick 47340 (18:09). The Eddystone in sight, W, four miles. The officer works a fix wrongly (tick 47619), the captain takes a bearing (47687), the officer corrects himself (47741).
17. Tick 54007 (20:00). Eight bells; the officer reports that the ship lists him asleep. CAPTAIN (54097): stand by till sunrise, "I'll keep her for the night." Officer stands by 20:03.
18. 20:04 to 03:58. The captain works the ship himself without taking the deck: `Keep her full`, `Steer south by west`, seven `Trim sails`, the fore topsail and topgallant set, the bowlines, the studding-sail and ringtail booms run out.
19. Tick 74880 (22 June 01:48). The officer wakes himself on a wind shift, puts her on S by E, then at the captain's wish sets both fore topmast studding sails, the ringtail and the water sail (all set by 02:16).
20. Tick 82288 (03:51). Sunrise; the officer suggests a lunar; the captain orders it and asks for a trimming order in the officer's name (entered tick 83157, 04:05). A strange sail W by S, two leagues (04:00).
21. Tick 86831 (05:07). The lunar: 3° 46' W against a reckoning of 4° 19' W. Tick 87063 (05:11): the officer advises against steering by it; the captain agrees. Tick 88900 (05:41): the officer journals his own reckoning.
22. 05:23 to 11:55. Light northerly airs, two to three knots, the "trim" order firing six times. Stand-by till noon from 08:00.
23. Tick 111720 (12:02). "Noon. Latitude by observation 49° 29' N; the reckoning was 49° 19' N. Course made good since yesterday SSE, 62 miles. Longitude by account 3° 42' W."

## 3. The deck and the captain's words

**The deck.** Given tick 109 (21 June 05:01): "Mr Ray, you have the deck." Not taken back in the slice. Tick 40717 (16:18): "The captain went below to his cabin; the deck is the officer of the watch's."; tick 47672 (18:14): "The captain came on deck." From 20:04 to 03:58 the captain gave helm and sail orders himself while the deck stayed nominally with the officer, who was standing by.

**Every allowance in the whole of session 4** (all ticks; rows 1 to 16 fall in my slice). There are 33 `agent.deck` lines in the session: 27 allowances, 3 givings of the deck (ticks 109, 343503, 398710), 2 hand-overs (343363, 558434) and 1 "The captain has the deck" (343510). There is **no `you may not`** anywhere in either session.

| # | Tick, ship's time | Captain typed | Logged as "The officer of the watch may ..." | What led to it | Used by the officer (accepted orders, whole session) |
|---|---|---|---|---|---|
| 1 | 42, 21 Jun 05:00 | `You may buy` | buy | Given unasked, before the deck (learned in session 3) | 3 (coal 7792, pilchards 24374, brandy 212162) |
| 2 | 44, 05:00 | `You may sell` | sell | Unasked | 0 (tried twice, refused by the market, not the domain) |
| 3 | 49, 05:00 | `You may send the boat ashore` | send the boat | Unasked | 3 (first 113) |
| 4 | 58, 05:00 | `You may weigh` | weigh | Unasked | 2 (first 543609, 27 June) |
| 5 | 60, 05:01 | `You may get under way` | get under way | Unasked | 3 (first 37217) |
| 6 | 63, 05:01 | `You may steer` | steer | Unasked | 45 (first 39997) |
| 7 | 74, 05:01 | `You may veer` | veer cable | Unasked | 0 |
| 8 | 80, 05:01 | `You may tack` | tack ship | Unasked | 7 (first 496809, 26 June) |
| 9 | 83, 05:01 | `You may gybe` | wear ship | Unasked | 6 (first 147614) |
| 10 | 92, 05:01 | `You may heave to` | heave to | Unasked | 7 (first 41053) |
| 11 | 96, 05:01 | `You may fill away` | fill away | Unasked | 7 (first 43088) |
| 12 | 131, 05:02 | `You may let go the best bower` | let go the anchor | Unasked, after the deck | 0 |
| 13 | 134, 05:02 | `You may drop anchor` | let go the anchor (the same again) | Unasked | 0 |
| 14 | 138, 05:02 | `You may moor her` | moor | Unasked | 0 |
| 15 | 43096, 16:58 | `You may full and by` | keep her full | `agent.refused` at 43089: "may not full and by without the captain: the course is the captain's, never to be changed without his directions unless to avoid an immediate danger"; the grant came 7 ticks after the refusal | 6 (first 43251) |
| 16 | 43102, 16:58 | `You may keep her full and by` | keep her full (the same again) | The same | as 15 |
| 17 | 203629, 23 Jun 13:33 | `You may come to an anchor` | come to an anchor | The officer asked in words at 203614 ("Your word: \"come to an anchor\" or \"you may come to an anchor\""); no refusal first | 3 (first 203633) |
| 18 | 261299, 24 Jun 05:34 | `you may shape a course for st mary's` | shape a course for (st mary's) | The captain asked him to use the order (261291); `agent.refused` at 261294: "the reckoning, the sights and the course shaped are the master's for the captain" | 3 (first 261302) |
| 19 to 21 | 406851, 406853, 406857, 25 Jun 22:00 | `you may come up half a point`, `... a point`, `... two points` | come up (half a point), (a point), (two points) | The captain suggested coming up (406839); `agent.refused` at 406842 for `come up half a point`; the officer did the same thing at once as `steer 340` under grant 6 (406843) | 0 |
| 22 to 24 | 406867, 406869, 406875, 22:01 | `you may bear off half a point`, `... a point`, `... two points` | bear away (half a point), (a point), (two points) | Given with the last, unasked | 0 |
| 25 | 512951, 27 Jun 03:29 | `you may take a bearing of the light` | take a bearing of (the light) | `agent.refused` at 512943, and the officer's request at 512948 ("May I have leave to take bearings?") | see 26 |
| 26 | 512955, 03:29 | `you may take a bearing of the land` | take a bearing of (the land) | The same | 1 ("taking a bearing of peninnis head", 520694) |
| 27 | 534267, 27 Jun 09:24 | `you may heave in the best bower cable to 160 fathoms` | heave short (the best bower cable to 160 fathoms) | `agent.refused` at 534248: "the anchor is let go and weighed by the captain" | 1, but not in the granted words: the order as granted was then rejected by the grammar (534277: "'heave short' takes nothing after it"); `heave in 70 fathoms` was taken (534284) |

Three more `you may` lines were refused for their wording: `You may bring her up` (143), `you come up` (406846, a slip) and `you may heaev in ...` (534260, a slip).

What the list shows:
- **27 allowance lines for 20 different things.** Fourteen were given in the first 138 ticks of the game (eleven of them before the deck), before the officer had been refused anything. Bearings, which he had asked for at tick 23 ("and the bearings too if you'll allow them"), were not among them; they came six days later (rows 25 and 26). The model's "about fifteen permissions one by one" is fair for the first day (16 lines) and low for the voyage.
- **Six of the twenty were never used** (sell, veer cable, let go the anchor, moor, come up, bear away).
- **Each one given while he stood by woke him.** Twelve of the 27 "A word from the captain" wakings in my slice are `you may` lines (ticks 50 to 139 and 43103); he answered each with another stand-by.
- **"For the watch" is not what happens.** Every line says "by the captain's word for the watch", but `tack ship`, given at tick 80 on 21 June, was first used at tick 496809 on 26 June, two re-seatings later, with no new grant.
- **The grants go by the order's verb and its exact tail.** Coming up needed three lines for three amounts; a bearing needed one for the light and one for the land. Yet `steer`, already granted, covers any course at all, as the officer said at 406846: "\"come up half a point\" was refused as a change of course without your directions, but \"steer 340\" was taken under the grant to steer. The two should be judged alike."
- **The captain reached for a general grant in plain words on the first day.** Tick 24447: "I'll entrust you to her entirely until I return." Tick 40121: "she is yours until I am back." (Later, outside my slice, tick 491530: "you have permission to keep her safe as necessary. If I see a refusal I'll allow it ASAP.")

**The captain's tells and questions that carry intent or feedback (my slice).**
- Tick 7876 (07:11): "No problem by me on waiting, I visited the tobacconist and so I'm well provisioned here". (Patience with boat trips of hours.)
- Tick 40121 (16:08): "I can set the time going and turn off the 1x for now, for example, could do 10 or 60 times compression as you like." (He offers the officer the choice of time compression.)
- Tick 40694 (16:18): "I'm simply going to pause the time until I'm back, I don't want to miss our first leg on her. Go ahead and say anything back and I'll pause with the turn closed." (He is managing the model's turn by hand.)
- Tick 47607 (18:13), a question: "can you see \"where I am\" on the ship right now?" and tick 47665: "I was just checking that my presence in the cabin had been properly logged and you saw it." (A test of people and places.)
- Tick 54097 (20:01): "No need to hand-over, but you may stand by at sunset until sunrise if you would like to take your rest, as it were, and I'll keep her for the night." (A way to relieve the officer without ending the station.)
- Tick 74950 (01:49): "I was prepping the stuns'ls and ringtail just for this. Set them as you please". Tick 74983: "the watersail should be out too. Might as well see, ey?" (He is trying the schooner's light sails.)
- Tick 82334 (03:52): "Set a standing order in your name for trimming the sails, if you please, so you may belay and resume it as you like." (The owner's stand-in for a "keep her trimmed" order, put in the officer's name because the officer cannot belay the captain's.)
- Tick 87088 (05:11): "Agreed, no change in course now. The lunar was subpar, I think."
- Ticks 39406 and 39436 (15:56, 15:57), the captain's two standing orders: `at the pilot asks to be put off then tell the officer the pilot has requested off, continue as the situation demands` and `at the pilot off then tell the officer The pilot is away, continue as we were`. He uses "then tell the officer" to turn an event into a waking, because the pilot's hails are routine lines.

**Done by the captain's hand because the officer could not:** bearings (ticks 1017, 1022, 1034 at anchor; 47687 of the Eddystone, with a tell at 47730 to pass the result on; 54225 and 54242); the lunar (82310).

## 4. Orders refused

Nine `order.rejected` and one `agent.refused` in the slice.

| Tick, time | Who | Order as typed | Refusal's words | Class and what followed |
|---|---|---|---|---|
| 143, 05:02 | captain | `You may bring her up` | "'bring her up' names no order the officer of the watch could be allowed; say the order's words first ('you may tack ship if the land closes within two miles')." | (a) A seaman's phrase for anchoring, not known. He had already given `let go the best bower`, `drop anchor` and `moor her`. |
| 7793, 07:09 | officer | `buy twenty tons of pilchards` | "The long-boat is away; wait for her." | (d) by the game's rule, one second after the coal was bought. The rule itself is questionable: two bargains cannot be struck on one visit. Retried at 24374 and taken. |
| 40107, 16:08 | captain | `Tell the offier Alright, ...` | "did you mean 'tell the watcher' or 'tell the officer of the watch'?" | Typing slip; retyped at 40121. |
| 42638, 16:50 | captain | `where is she` | "Nobody aboard answers to 'she'; 'the people' lists them." | (a) After `what is she` about the cutter he asked where she was; the game took it for a person. There is no short way to ask a sail's bearing and distance. |
| 42643, 16:50 | captain | `Where is` | "Where is whom? Name a person by his role or his name." | Unfinished order; correct. |
| 43089, 16:58 | officer (`agent.refused`) | `full and by` | "The officer of the watch may not full and by without the captain: the course is the captain's, never to be changed without his directions unless to avoid an immediate danger. 'full and by' not carried out." | (c) He already had leave to steer any course, so the refusal protected nothing; keeping her full and by on a wind is the watch officer's ordinary helm order. The words "may not full and by" are also not English. Granted 7 ticks later as "keep her full"; `keep her full and by` taken at 43251. |
| 43093, 16:58 | officer | `steer SE by S` | "She is hove to; fill away before giving her a course." | (d) correct, but he had ordered `fill away` five ticks earlier and it was in hand; the words do not allow for that. |
| 47681, 18:14 | captain | `Take a bearing of the light` | "The light is not in sight; in sight: the Eddystone bearing W by N, distant four miles." | (a) minor. By day the Eddystone tower is not "the light". The answer usefully says what is in sight. |
| 67582, 23:46 | captain | `Ease in the weather bowlines` | "'ease' was understood, but 'in' belongs with 'brace'." | Correct; `Ease the weather bowlines` taken. |
| 67590, 23:46 | captain | `Let fly the weatehr bowlines` | "There is no such part as the weatehr bowlines in this ship; did you mean the fore bowlines, the fore bowline or the fore top bowlines?" | Typing slip. The suggestion misses the nearest match, "the weather bowlines", which the game takes. |

Also one failure after acceptance. Tick 75942 (02:05), LOG: "Could not bend the water sail: The water sail is bent already (furled); to change it for a new one, shift it". The captain's `bend the water sail` (75003) was still waiting for hands when the officer gave the same order (75770); both were accepted and the second failed when its turn came.

## 5. Harness behaviour

- **Seating and door events.** One seating in the slice (tick 12). Thirteen door events: ten stand-bys taken out of turn after a spoken line, and three spoken lines "at its own word" that ended a stand-by (ticks 42649, 74880, 83157).
- **Stand-bys: 57, none refused.** By condition: a glass 15; the deck given 10; the boat alongside 5; the boat away 3; the pilot asks to be put off 3; ten minutes 3; sunrise 3; steady on the course 3; 5 minutes 2; the pilot off 2; the change of the watch 2; filled away 2; under way 1; noon 1; a sail made out 1; a notable event 1. The longest: sunrise from 20:03, ended by himself after 5 h 44 m; the boat alongside 4 h 34 m and 3 h 29 m; noon 4 h 01 m. "A glass" ran exactly 1,800 ticks each time it was not cut short.
- **Wakings: 57 `agent.resumed`.**

| Reason | Count | Worth it? |
|---|---|---|
| A word from the captain | 27 | 12 were real tells; 12 were `you may` lines (nothing to do but stand by again); 2 were the captain's pilot standing orders; 1 was the deck given |
| A glass | 7 | Three led to something (17:33 report and the fore topsail taken in; 05:10 the lunar caution; 05:41 the journal note); four were answered by another stand-by at once |
| The boat alongside | 3 | Yes, each time |
| Ten minutes / 5 minutes | 3 + 1 | Yes (casting her; setting the light sails in turn) |
| Steady on the course | 3 | Yes: he trims only after the helm has swung |
| The change of the watch | 2 | Yes (reports at 20:00 and 08:00) |
| At its own word | 3 | Yes (the two cutters; the wind shift at 01:48; the captain's request and the strange sail at 04:05) |
| Under way; the boat away; filled away; sunrise; noon; a question from the captain | 1 each | Yes |
| A notable event | 1 | No: woken after 20 ticks by "Not hands enough on deck to bend the water sail" (75004) |
| A sail made out | 1 | No: a false waking, see below |

- **A false waking.** Tick 83442 (04:10): he stands by "until a sail made out". Tick 83443: "A sail made out, which came at Morning watch (04:06) while your call was on its way". The "sail made out" was his own `what is she` four minutes earlier, whose answer was "The glass aloft makes out nothing more of the sail".
- **A captain's word that did not wake him.** Tick 82334 (03:52): the captain asks for the trimming order. Tick 82335: the officer's stand-by "until a glass" is logged, with no "A word from the captain" waking. He answered at tick 83157, 13 m 42 s of ship's time later ("Good morning, sir, and aye"), after the captain had typed `Trim sails` himself (82728). The word seems to have crossed with a stand-by already sent.
- **A strange sail did not wake him.** "Sail ho!" at tick 82800 came while he stood by for a glass; he reported it at 83157 by ending his own stand-by. He had no way to stand by for "a glass, or a sail".
- **Nudges (two), both wrong.** Tick 43088 (16:58): "The officer of the watch nudged: 3 contrary orders on the yards and the helm within the watch (trim sails; heave to; fill away)." Tick 43251 (17:00): "... 4 contrary orders ... (trim sails; heave to; fill away; keep her full and by)." That sequence is how a pilot is put off: trim, heave to for his cutter, fill away, come to the wind. He took no notice and no pause followed.
- **Compression.** "Compression eased to 1x: the officer of the watch is sampled" 30 times in the slice, once at each sampling after a longer wait.
- **Journal and reads.** Two journal notes (tick 22, the *Harpy*'s lessons; tick 88900, his own reckoning kept apart from the ship's). One `answer`. No `readings`, `state`, `read_log` or `library` call is recorded in the slice, though he plainly had the price list, the people and the account's position; reads made out of turn are not kept in a save.
- **Handover notes, re-seating, context.** None in the slice. No sign of a lost thread, a budget or a timeout. The only trace of the relay is the door note's "for up to 50 seconds" (`--wait 50` in use from the start).
- **The start.** No odd first calls: journal (tick 22), report (23), stand-by "until the deck given" (45). No drill appears: the consent record is dated 2026-10-03, the station is marked `station.drill: true`, and by `CHANGES-m5c-b.md` a drill passed on record is carried over and not put again. No refused `hand_over` can be seen; a refused call would not be stored.

## 6. Ship, sea, navigation and port observations

### 6.1 Trade at Plymouth

| Trip | Ordered or bought | Boat away | Landed | Shoved off | Alongside | What it carried | Bargain to aboard |
|---|---|---|---|---|---|---|---|
| 1, prices | 113 (05:01) `send the boat ashore` | 438 (05:07) | 2975 (05:49) | 4775 (06:19) | 7649 (07:07) | Nothing out. Back: "The mate's list of the prices at Plymouth is aboard: coal £2, canvas £55, hemp £65, salt £24 a ton, and the rest." | 2 h 06 m |
| 2, coal | 7792 (07:09) "Bought 40 tons of coal at Plymouth at £2 a ton, £80 paid; the boat goes for it. The purse: £2020." | 8138 (07:15) | 10681 (07:58) | 21481 (10:58) | 24364 (11:46) | "40 tons of coal hoisted in and struck down into the hold; the manifest 40 tons of coal; room for 72 tons." | 4 h 36 m |
| 3, pilchards | 24374 (11:46) "Bought 20 tons of pilchards at Plymouth at £19 a ton, £380 paid; the boat goes for it. The purse: £1640." | 24655 (11:50) | 27167 (12:32) | 34367 (14:32) | 37212 (15:20) | "20 tons of pilchards hoisted in ...; the manifest 40 tons of coal, 20 tons of pilchards; room for 52 tons." | 3 h 34 m |

- The pattern of a trip: about five minutes to hoist out, 42 minutes to pull in, then at the quay 30 minutes for the prices or one hour plus three minutes a ton for goods (3 h for 40 tons, 2 h for 20), and 48 minutes back including hoisting in.
- **One bargain to a trip.** Tick 7793, one second after the coal: "The long-boat is away; wait for her." Loading 60 tons took from 05:01 to 15:20, ten hours and nineteen minutes, with the boat away for nearly all of it.
- **How he learned what Plymouth sold.** Only from the boat's list. The log line names four goods "and the rest"; the officer's report (tick 7664) gives all eleven, which agree with the port file: coal £2, timber £6, copper ore £11, pilchards £19, salt £24, biscuit £40, salt beef £50, canvas £55, hemp £65, wine £75, brandy £315.
- **What told him what Roscoff would buy: nothing.** The papers hold a price list for Plymouth only. The captain named the destination (tick 7787). The officer chose by general knowledge, and said so: "Brittany has little coal of its own, and Cornish pilchards went to France and the Mediterranean by the shipload", "a cheap outward cargo that costs little if it sells poorly". The port file for Roscoff (`data/ports/roscoff.yaml`) deals in brandy, geneva, rum, tea, tobacco, wine, salt, canvas, onions, tin and salt beef: neither coal nor pilchards. The £460 was spent blind. (Of Plymouth's goods only salt beef, £50 there and £70 at Roscoff, would have sold at a profit.)

### 6.2 The Plymouth pilot, Mr Tozer

- **How he came.** No cutter was in sight while she lay at anchor. Two minutes after "The best bower is aweigh" (tick 38157, 15:35) the LOG has "Sail ho! The Plymouth pilot's cutter on the starboard bow, bearing W by N, distant six cables." (38280, 15:38). She hailed at 38640 (15:44): "a pilot for Plymouth; shorten sail and he will come aboard." He boarded at 38880 (15:48): "The pilot, Mr Tozer of Plymouth, came aboard from the cutter and took charge of her (American colours being no bar at Plymouth)." Nobody asked for him, and she was outward bound.
- **How fast she was moving: hardly at all.** The model's note says he "boarded the Speedwell under way at about four knots". The log does not bear that out. She was under way only in the sense that her anchor was up. Two minutes before he boarded: "Her sails aback; she had no way on to lose." (38763, 15:46). OFFICER at 38659 (15:44): "her head is south-west with the wind 34° on the bow, and she's gathering sternway"; at 38982 (15:49): "She's hanging head to the south-west and won't pay off". Three and a half minutes after he boarded: "Leeway 36° to larboard" (39090), the mark of a ship barely moving ahead. The four knots is the officer's figure for 15:55, seven minutes after the boarding (39344: "Steady on south-east by south at four knots"). No line gives her speed at 15:48.
- **His words** (38880) are the port file's directions for coming *in*, said to a ship going out: "Coming from the west, round Rame Head and Penlee a third of a mile off until Tor House appears midway between Redding Point and the barrack chimneys on Drake's Island ...", the marks, the anchorage, and "High water at Plymouth about a quarter past twelve in the middle watch, the tide rising some 14 feet; the flood will serve from about six o'clock in the evening." One phrase is out of its time: "on the west end of where the breakwater now is". The breakwater was begun in 1812. His news: "Britain at war with the Batavian Republic, France and Spain; the United States, Portugal and Denmark at peace with all."
- **"Took charge of her"** is not what followed. Every helm and sail order carried out between 15:44 and 16:58 was the officer's; the pilot gave none.
- **Where and how he left.** 40920 (16:22): "The pilot asks for sail to be shortened: his cutter is coming off for him." The officer hove to (41053; "Hove to, fore topsail to the mast, helm a-lee." at 41105, 16:25). By his own account she was then in "Twenty-two fathoms, open water, nothing within two miles" (41125); six minutes before he had Penlee "two miles astern" (40758). 42900 (16:55): "The cutter hailed: she has come off for the pilot." 43080 (16:58): "Mr Tozer left her in the cutter, clear of Cawsand Bay; the pilotage, £6, paid and his certificate signed." Both transfers at Plymouth were therefore made with the schooner stopped or nearly so.
- **The hails are routine lines.** All three `port.pilot_hail` lines carry no mark, while each ten-minute cast of the lead is notable. A station sampled "on notable and urgent events" does not hear a pilot hail. That is why the captain wrote his two "tell the officer" standing orders.

### 6.3 Other sail: the distance that does not change

Every line the log has about another vessel in the slice, with the officer's figures where the log has none:

| Tick, time | Source | Vessel | Bearing | Distance | Words |
|---|---|---|---|---|---|
| 0, 21 Jun 05:00 (both sessions) | LOG hail | frigate | W by N, abeam to starboard | eight cables | "Sail ho! A frigate abeam to starboard, bearing W by N, distant eight cables." |
| 2811, 05:46 (session 3) | OFFICER, from readings | frigate | SW by S | eight cables | "still eight cables off, now bearing south-west by south" |
| 6753, 06:52 (session 3) | OFFICER, handover note | frigate | not given | eight cables | "has stayed eight cables off for two hours" |
| 11760, 08:16 (session 4) | LOG | frigate | on the larboard bow | lost | "The sail on the larboard bow is out of sight." |
| 38280, 15:38 | LOG hail | pilot's cutter | W by N | six cables | quoted in 6.2 |
| 40980, 16:23 | LOG hail | a cutter | NNW, starboard quarter | two miles | "Sail ho! A cutter standing out from the land on the starboard quarter, bearing NNW, distant two miles." |
| 41700, 16:35 | LOG, routine | the cutter | starboard quarter | none | "shows British colours, the red ensign" |
| 42060, 16:41 | LOG, routine | the cutter | starboard quarter | none | "is the Plymouth pilot's cutter, standing to the south-eastward (SE by S), under plain sail" |
| 42240, 16:44 | LOG, routine | "the sail" | starboard quarter | lost | "The sail on the starboard quarter is out of sight." |
| 42626, 16:50 | LOG, the captain's `what is she` | the cutter | abeam to starboard | none | "the Plymouth pilot's cutter, standing to the south-eastward" |
| 42649, 16:50 | OFFICER | two cutters | N by E; NNW | three miles; two miles | "the pilot's cutter, three miles north by east ... a second cutter two miles north-north-west, showing no colours yet" |
| 42900, 16:55 | LOG | the cutter | none | within hail | "The cutter hailed: she has come off for the pilot." |
| 44640, 17:24 | LOG, routine | the cutter | right astern | lost | "The cutter right astern is out of sight." |
| 82800, 22 Jun 04:00 | LOG hail | a sail | W by S, abeam to starboard | two leagues | "Sail ho! A sail abeam to starboard, bearing W by S, distant two leagues." |
| 83160, 04:06 | LOG, the officer's `what is she` | the sail | abeam to starboard | two leagues | "her hull is below the horizon, distant two leagues" |
| 87063, 05:11 | OFFICER | the sail | NW | six miles | "now north-west, six miles, and not closing on us" |
| 94980, 07:23 | LOG, routine | the sail | right astern | lost | "The sail right astern is out of sight." |

**The pattern.** While the *Speedwell* lay still, a sail's bearing moved and its distance did not. By the officer's readings the frigate went from W by N to SW by S in 46 minutes at a constant "eight cables"; by the log she was then lost to sight at 08:16, which a ship truly eight cables off in clear weather could not be. The second cutter was "two miles" at 16:23 and, to the officer, still "two miles" at 16:50; five minutes later she was within hail. On the 22nd, with the schooner making two or three knots, nothing odd shows.

**The cause (SOURCE).** `freesail/world/lookout.py`, `_judge` (lines 362 to 386; the file is byte-identical in m5c and m5c-b). The distance by estimation is drawn once for a sighting and "held until she has moved a mile from where it was judged" (`ESTIMATE_HOLD_NM = 1.0`), where "she" is the player's ship. That rule was written for headlands, so that a calm does not redraw them, and it is applied to sail as well. A ship at anchor or hove to therefore keeps the first figure for every vessel however far that vessel sails; the bearing is worked afresh each minute. So the distance is cached, and the model's suggested test (save twice and compare) is answered: the other ship need not be circling. Primer 15 states the rule ("drawn once a sighting and held while she makes no way") without noticing that the other ship makes way. The cases in later slices where the schooner was herself moving need their own check.

Two smaller things about the sail lines. A vessel first seen close, already made out, is lost under the bare name "the sail" (the frigate at 11760; the first cutter, probably, at 42240), while one made out by stages keeps her name ("The cutter right astern", 44640). And the cutter that came for the pilot was hailed as an unknown "cutter standing out from the land" (40980) although the pilot's cutter had been named 45 minutes before.

### 6.4 The lunar at tick 86831, and the account before and after

The line, whole (LOG, 22 June 05:07, notable): "A set of distances of Altair and the moon taken by Mr Travers and two of the young gentlemen, and cleared: longitude by lunar 3° 46' W, which he would trust within 20 miles; the reckoning was 4° 19' W."

The position by account around it. No log line in the slice states the account's position except the two noon lines and the lunar line itself; the rest is the officer reading it out.

| Tick, time | Source | What it says |
|---|---|---|
| 25320, 21 Jun 12:02 | LOG, noon at anchor | "Latitude by observation 50° 21' N; the reckoning was 50° 20' N. Longitude by account 4° 11' W." |
| 39600, 16:00 | LOG, lookout | "The Eddystone bearing SSW, distant three leagues." |
| 47340, 18:09 | LOG, lookout | "The Eddystone bearing W, distant four miles." |
| 47619, 18:13 | OFFICER | "the account's 50° 12' N, 4° 05' W" (and his own wrong fix of 50° 17' N) |
| 47687, 18:14 | LOG, the captain's bearing | "The Eddystone bore W by N, four miles by estimation." |
| 47741, 18:15 | OFFICER | fix "about 50° 10' N, 4° 10' W ... agrees within a mile or two with the account as it now stands, 50° 10' N, 4° 08' W" |
| 54000, 20:00 | LOG, lookout | "The Eddystone bearing N by W, distant two leagues." |
| 54225 and 54242, 20:03 and 20:04 | LOG, the captain's bearings | "The Eddystone bore N by W, two leagues by estimation." (twice) |
| 59580, 21:33 | LOG | "The land is out of sight." |
| log heaves | LOG | 5¼ knots (16:00), 5 (18:00), 3½ (20:00), 4¾ (22:00), 2¾ (00:00), 2 (02:00), 3 (04:07), 2 (06:00), 2¾ (08:00), 2½ (10:00), 2¾ (12:00) |
| 74887, 22 Jun 01:48 | OFFICER | "By the account we're at 49° 45' N, 4° 21' W" |
| 82296, 03:51 | OFFICER | "By the account we're at 49° 42' N, 4° 19' W" |
| 83231, 04:07 | LOG | "The distances taken; Mr Travers below to clear them." |
| 86831, 05:07 | LOG | the lunar line; and "Mr Travers came on deck, the lunar done." |
| 87063, 05:11 | OFFICER | "the account has been moved to it. That's thirty-three minutes east of the old account, about twenty-one miles." |
| 88900, 05:41 | OFFICER, journal | his own reckoning: "near 49° 35' N, 4° 20' W at 05:40" |
| 97207, 08:00 | OFFICER | his own: "near 49° 31' N, 4° 19' W" |
| 111720, 12:02 | LOG, noon | "Latitude by observation 49° 29' N; the reckoning was 49° 19' N. Course made good since yesterday SSE, 62 miles. Longitude by account 3° 42' W." |

**What the log supports, exactly.**
1. *The jump of 33 minutes east: supported by the lunar line alone.* 4° 19' less 3° 46' is 33', about 21 nautical miles in that latitude.
2. *That the account was replaced: supported.* The lunar line does not say so, but the noon line does: "Longitude by account 3° 42' W" is the lunar's 3° 46' carried on for seven hours on her S by E course. Left alone, the account would have stood near 4° 15' W. This is the designed rule, not a fault in the code: primer 12 says of the lunar "The reckoning is updated by it, east and west", with no test of which figure is the better.
3. *"A recent Eddystone bearing had made the account good to about 2 miles": partly supported.* The captain took three bearings of the Eddystone (18:14, 20:03, 20:04), and by primer 10 the master puts his account on each. But the last was nine hours and roughly 27 logged miles before the lunar, and no log line states the master's doubt at any time. "About 2" is the officer's own check at 18:15 ("within a mile or two"). By 05:11 his own figure for the old account was "within three or four". Fairer wording: a lunar trusted within 20 miles replaced an account about nine hours and under thirty miles from a landmark fix, which the officer judged good to three or four miles.
4. *That the lunar was the worse figure: not provable inside the slice; the next slice lets it be worked roughly, and it was, but by less than the note implies.* The officer held S by E on the old account. From the full log beyond my slice: she kept S by E at three to three and a half knots until 22:00, lay hove to on the starboard tack heading NW at a knot and a half until 03:55, then steered SE by S (the captain's order, tick 168957) until the land came up at tick 182220 (23 June 07:37): "The Isle of Bas bearing S by W, distant four leagues." The chart file has the island at 48° 44.7' N, 4° 00.6' W, so she was then near 48° 57' N, 3° 57' W. Run back along those courses at the logged speeds, with the distance off, the log's over-reading and the headway made hove to each varied, and keeping the workings that return the observed noon latitude within three miles, she was near 4° 05' to 4° 13' W when the lunar was cleared. On that working the old account (4° 19' W) was some four to nine miles too far west, and the lunar (3° 46' W) some twelve to seventeen too far east. So the lunar was inside the master's twenty miles; the old account was at best what the officer claimed for it at 05:11 ("within three or four") and at worst twice that; it was the nearer of the two by a wide margin, and it was not good to two miles. This is my arithmetic (tides and the drift hove to are not in it), and the reader of the next slice has the bearings to check it.

Three more things in the same lines.
- **The noon latitude was ten miles out** (49° 19' by account, 49° 29' observed) after about 46 logged miles since the last bearing. Primer 10 says the log reads "a few per cent over the truth"; here the account over-ran by about a fifth. The officer's own reckoning, carried on from his 08:00 figure at the logged speeds, would have been about seven miles too far south as well. The lunar has no part in this (it moves longitude only). The cause cannot be told from the dumps (section 10).
- **"Course made good since yesterday SSE"** is not a course she made. Her bearings and her courses (S by W through the night, S by E from 01:48) put her track about due south from Plymouth; the easting in "SSE" is the lunar's jump counted as distance sailed.
- **A star lunar begun at sunrise.** "Sunrise." is tick 82288 (03:51). The captain's `Take a lunar` is tick 82310, and the LOG at 82311 has "for a set of distances of Altair and the moon"; the distances were "taken" at 04:07, sixteen minutes after sunrise, when no star is to be seen. It was the officer's suggestion (82296: "this morning is the time for it"), and its result is the one he then had to warn against.

### 6.5 `get under way` on the schooner

- The order (tick 37217, 15:20): `get under way on the starboard tack and steer SE by S`. Wind W by S ("Wind backed to W by S, a gentle breeze", 37870), about ten knots; she had swung to the ebb at 15:00 with "the wind against the tide".
- The evolution's steps are the frigate's words on a schooner: "Let fall! Sheet home! Hoist away the topsails! Brace up the after yards for the starboard tack, the head yards abox." (38034); "Let go the downhauls, hoist away the jib! Helm a-lee for the stern-board." (38157); "She has paid off; right the helm, brace round the head yards, set the spanker." (38577). Her only square sails are the fore topsail and topgallant; she has no after yards and no spanker. (`heave to` is rig-aware: "Hauled flat aft the mainsail sheet; the fore staysail sheet to windward; braced the fore topsail aback", 41054.)
- **The log says she has paid off and is under way on her course; the ship says otherwise.** LOG 38651 (15:44): "Under way on the starboard tack, under the topsail and the mainsail and the jib; the best bower catted and fished; steering SE by S (146°)." OFFICER, eight ticks later: "she hasn't paid off: her head is south-west with the wind 34° on the bow, and she's gathering sternway." LOG 38763 (15:46): "Her sails aback; she had no way on to lose." LOG 39090: "Leeway 36° to larboard."
- **Orders needed by hand afterwards: four, and then a trim.** `haul the jib sheet to windward` (38658; "the jib now 15° off the centreline; aback"), `ease the main sheet` (38659), `back the fore topsail` and `let fly the main sheet` (38978), `trim sails` (39019). LOG 39338 (15:55): "Steady on SE by S (146°)." Eleven and a half minutes passed between "Under way" and steady on the course. All four orders were within the officer's own domain.
- So the model's note is supported, with two qualifications. No log line gives her heading or a sternway figure between 15:35 and 15:55; those are the officer's readings. And she was not on the wrong tack but in irons on the right one: the wind was already on her starboard side and she would not fall off the seven points the course needed.
- A lesser matter: after `fill away` the log says "Filled away; braced full and steering SE by S (152°)" (43249), a course nobody had ordered at that moment (her last ordered course was S by E, 169°; the officer's `steer SE by S` had just been rejected).

### 6.6 The taken-aback and wind-shift lines under m5c-b

- **`ship.aback`: one line in 31 hours, notable, not urgent.** Tick 38763 (15:46): "Her sails aback; she had no way on to lose." This is the new wording, and it woke nobody. **No urgent line of any kind** is in the slice.
- **The per-sail lines are unchanged and are all notable: seven** (`sail.backed`). Five of the seven record a sail backed *on purpose*: "Fore topsail taken aback." as the evolution laid the head yards abox (38043), "Jib taken aback." ten ticks after the officer hauled its sheet to windward (38668), "Fore topsail taken aback." eighteen ticks after "Laid the fore topsail yard ... aback" (38997), and "Fore staysail taken aback." and "Fore topsail taken aback." as she hove to (41063, 41078). The other two are "Main sail taken aback." as she lay head to wind weighing (38043, 38081). "Taken aback" means caught unawares; a sail laid aback by order is not that.
- **`wind.shift`: nine lines in 31 hours,** the closest two 59 minutes apart: 14:32 "Wind veered to W by N, a gentle breeze"; 15:31 backed W by S; 16:59 backed SW by W; 20:36 veered W by S; 23:29 veered W by N, a light breeze; 01:42 veered NW by W; 04:31 veered NW by N; 06:52 veered N by W; 11:41 veered N by E. Three squalls have their own lines. In breezes of three to fourteen knots the line is quiet.
- **The event "a wind shift" is not the log's line.** The officer's order "trim" (`at a wind shift then trim sails`) fired six times between 04:30 and 11:55 (ticks 84621, 87813, 92996, 100359, 103572, 111304) against three logged shifts in those hours; three firings (87813, 100359, 103572) have no `wind.shift` line near them. SOURCE: the event is a shift of one point in the ten-minute mean; the log line wants two points held a minute. A reader sees "By standing order 'trim': trimming sails." with no shift reported.
- **Five of the six firings logged no change.** The first squared the yards (20° to 0°). The next five each end "Braced two yards to the wind; 0° from square." with the sheets said to "stand as trimmed" (seen at 87813 and 100359): two notable lines apiece for the same figure as before.

### 6.7 Standing orders written in the slice

| Tick, time | By | Words as entered | Fate |
|---|---|---|---|
| 113, 21 Jun 05:01 | the officer ("by the mate") | "inshore lead": "every 10 minutes, if the land is in sight then heave the lead" | Fired through the slice whenever any land was in sight; 104 times in the whole voyage; belayed later |
| 39406, 15:56 | the captain | "The pilot asks off": "at the pilot asks to be put off then tell the officer the pilot has requested off, continue as the situation demands" | Fired 16:22 |
| 39436, 15:57 | the captain | "The Pilot away": "at the pilot off then tell the officer The pilot is away, continue as we were" | Fired 16:58 |
| 83157, 22 Jun 04:05 | the officer | "trim": "at a wind shift then trim sails" | Six firings in the slice, 41 in the voyage |

### 6.8 Other observations

1. **The lead's ground is the anchorage's chart note.** All 65 casts that found bottom end "; sand, foul and rocky in the north part." That is a remark about Cawsand Bay as a whole, not what tallow brings up, and it was still given in sixteen fathoms outside the bay, a mile or more beyond Penlee ("By the deep sixteen; sand, foul and rocky in the north part.", 40414, 16:13).
2. **Soundings are a third of all notable lines** (84 of 238). Nineteen are "No bottom at twenty fathoms." between 16:23 and 21:33: the "inshore lead" kept sounding in deep water while any land was in sight, first the coast astern (lost at 17:20), then the Eddystone rock four to six miles off (18:09 to 21:33).
3. **Trimming floods the log.** Thirteen trims by hand (five by the officer, eight by the captain) and six by standing order in twenty hours. One `Trim sails` on this schooner yields up to nine lines of "Not hands enough on deck to trim the jib; the watch is bracing the fore topsail yard and the fore topgallant yard" and "Only two hands to the fore staysail" (for example tick 63208). 51 `evolution.waiting` and 23 `evolution.short_handed` lines in the slice, 16 of them notable. Also 84 routine "Leeway 3° to larboard" lines.
4. **Hands.** Bracing two yards takes most of a watch, and the lead waits behind it: "Not hands enough on deck to heave lead; the watch is bracing the fore topsail yard and the fore topgallant yard." (56514, 20:41). The lunar counts as work for the watch ("the rest are taking lunar", 82729) and delayed the four o'clock heave of the log to 04:07.
5. **People** (the officer's readings, not log lines). Tick 54007 (20:00): "the ship has piped Mr Ray below and lists him \"asleep\" with the change of the watch, while he still holds the deck." Tick 47619: "The ship's list has Mr Travers, master, in the cabin. On this schooner the master is her captain, so that's you." The captain confirmed it (47665). So the captain and the master are one person in the list, yet the log treats Mr Travers as someone else: he is "below to clear" a lunar for an hour (83231 to 86831), and in session 3 the captain was sending the officer messages during that same hour (ticks 6692, 6745).
6. **Words.**
   - "By the officer of the watch: whatting is she." (83160), the echo of his `what is she`.
   - "may not full and by" (43089).
   - Compass points in lower case in the officer's echoes: "steering s by e" (40758), "getting under way on the starboard tack and steer se by s" (37217).
   - The failure line at 75942 ends "shift it" with no stop.
   - "two of the young gentlemen" on a merchantman (82311, 86831).
7. **A strain warning in a gentle breeze.** "Main topmast working under the press of sail." (43901, 17:11) came nine ticks after "A gust: 17 knots, the mean 13", seven minutes after the gaff topsail was set. It reads sensibly. It is notable, did not wake the officer, and he dealt with it at the next glass.
8. **No "NaN" and no well** appear in either log (owner's notes 2 and 6 cannot be seen here).

## 7. The model as an officer

**Good calls.**
- He asked for the destination before buying (7664) and kept £1,640 for the homeward cargo.
- He got her out of irons with the right four orders in the right order, saying what he was doing and why (38659, 38982).
- He hove to for the pilot's cutter to give her a lee (41125), and filled away the moment the pilot was off.
- He took in the fore topsail when it would not stand close-hauled (45224: "the square fore topsail can't draw and has only been shaking, so I've taken it in to save the canvas and the strain") and marked the strain warning as "the first warning, not yet a danger".
- He planned the landfall for daylight three separate times (24375, 40134, 88900: "heave to or stand off-and-on twelve to fifteen miles out at dusk, and close at dawn").
- **The lunar.** Four minutes after the result he told the captain what it had done and why it should not be steered by: "A lunar's twenty miles can't overrule a landmark fix plus a short run. I'd steer from the old account." (87063). He held the course, and half an hour later began a reckoning of his own in his journal, "kept apart from the ship's account". The land later came up where he expected (tick 182220, in the next slice). This is the best piece of watch-keeping in the slice.
- He trims after the helm has swung, by standing by for "steady on the course" (39997 to 40097; 40758 to 40807).

**Mistakes.**
- **The fix worked too fast.** Tick 47619 (18:13), in an answer to the captain: the Eddystone "puts us nearer 50° 17' N, 4° 10' W ... I'll trust the tower over the account". That is seven miles out in latitude. He corrected it unprompted two minutes later (47741: "My \"50° 17'\" was my slip, not the master's."). Nothing was done on the wrong figure.
- **A stale report.** Tick 42649 (16:50) he reported "a second cutter ... showing no colours yet ... She could be a revenue cutter, a privateer, or only a fisherman". The lookout had her colours at 16:35 and her name at 16:41. Those are routine lines, which a station standing by does not get, so the harness shares the blame.
- **He woke at 01:48 on a stale assumption** ("I left her steering \"full and by\"", 74880). The captain had put her on a compass course at 20:41. He read the log, said so (74887: "I see you've had her well in hand, sir") and then changed the captain's course from S by W to S by E under his leave to steer, explaining why. The captain agreed afterwards.
- **He stood by one tick after the captain asked him for something** (82335) and answered fourteen minutes of ship's time late; and he stood by for "a sail made out" just after making her out himself (83442).
- **A duplicate order** (`bend the water sail`, 75770) that failed, which he noticed and explained (76375).
- **The cargo.** He bought for a port whose market he did not know. He named the risk and kept the outlay small, and the game gave him no way to learn it; but the reasoning from real history was applied to a market that does not model it.
- A wrong estimate of the pilchard trip (24375: "about four and a half hours"; it took three and a half) and "Penlee south-south-west" for SW by S (23).

**How he handled refusals.** Three in the slice. For `full and by` he stated the seamanship, named the exact grant wanted and offered the fallback in the same breath (43095: "If you'll give me \"you may full and by\" ... Otherwise I'll steer by points and adjust as it shifts"). He did not argue and did not try to slip round it.

**What he asked for or wished for.** Bearings (23: "and the bearings too if you'll allow them"); `full and by`; a ruling on the watch below (54007: "I'll keep it as long as you like, or hand it over to you for the night if you'd rather keep it the period way").

**What he said about the game itself (in the slice).**
- Tick 7797 (07:09): "The pilchards must wait until she's back, since one boat carries one bargain at a time."
- Tick 43095 (16:58): "the right helm is \"full and by\" ... but the ship counts that as changing your course."
- Tick 54007 (20:00): "One oddity for your list: the ship has piped Mr Ray below and lists him \"asleep\" with the change of the watch, while he still holds the deck."
- Tick 76375 (02:12): "(Your first order to bend the water sail had only been waiting for hands, so mine found it already done.)"
- Tick 87063 (05:11): "A lunar's twenty miles can't overrule a landmark fix plus a short run."

**Worth keeping.** Tick 47619: "If you're somewhere else in your own mind, the ship hasn't heard of it." Tick 75007, of the water sail: "She'll look like a washing line."

## 8. Cross-check against the notes

**The owner's items.**
- **1 (the pilot boarding under way).** ADDS NUANCE. He boarded a ship whose anchor was up but which was stopped in irons (38763, 38880), and left her hove to with the cutter within hail (42900, 43080). Neither Plymouth transfer was made with way on.
- **3 (price lists).** SUPPORTS. One list aboard, for the port she lay in (7649). See the model's addition below.
- **9 (accepting or refusing the pilot).** SUPPORTS. An outward-bound ship that had not asked for a pilot got one within thirteen minutes of weighing, was read the directions for coming in, and paid £6 (38280 to 43080).
- **11 (the journal out of context).** No evidence either way; two notes in 31 hours.
- **12 (returning to the station).** ADDS NUANCE. Tick 54097: "No need to hand-over, but you may stand by at sunset until sunrise ... and I'll keep her for the night." Taking the deck still ends the station, so the owner kept the con for eight hours without the deck, and the log shows two voices on the helm.
- **13 (several conditions in a stand-by).** SUPPORTS. A sail was sighted while he stood by for a glass (82800); he stood by in turn for "the pilot asks to be put off" and then "the pilot off"; the captain built a waking out of a standing order (39406, 39436); "a notable event" woke him in 20 ticks on a line about hands (75004).
- **15 (a general grant).** SUPPORTS strongly: section 3. The owner's own phrase from the note, "she is yours", is already in the log at tick 40121.
- **16 ("keep" orders).** SUPPORTS. Thirteen trims by hand in twelve hours (15:50 to 03:58); the captain's request at 82334; the stand-in order's five firings for no change (6.6). `keep her full and by` shows the game already has one continuous order.
- **17 (taken aback in a calm).** SUPPORTS that the urgent calls have stopped: one notable `ship.aback` line and no urgent line in 31 hours. The calm itself is in later slices.
- **18 (wind shifts filling the log).** SUPPORTS that the line is quiet in a breeze (nine in 31 hours). ADDS: the standing-order event fires at half the log's threshold (6.6).
- **19 (the reckoning near land).** Bears on it through the lunar: 6.4.
- **21 (a turn ending at `say`).** SUPPORTS. Ten of his 33 spoken lines were followed by a stand-by made out of turn; the captain plans round it (40694: "say anything back and I'll pause with the turn closed").
- **2, 4 to 8, 10, 14, 20, 22 to 25.** Cannot be seen in this slice.

**The model's comments and additions.**
- **"Mr Tozer boarded the Speedwell under way at about four knots."** CONTRADICTED on the speed (6.2).
- **"I bought coal and pilchards at Plymouth for Roscoff, and Roscoff takes neither."** SUPPORTED (6.1 and the port file).
- **"On the Speedwell you gave about fifteen permissions one by one."** SUPPORTED and understated: 27 lines, 20 things.
- **"A lunar 'trusted within 20 miles' replaced an account that a recent Eddystone bearing had made good to about 2 ... jumped 33' east."** SUPPORTED in direction: the jump and the replacement are both in the log, and the replacement is the designed rule. The sizes are overstated. The bearings were nine hours old, and by a rough working from the next day's landfall the old account was four to nine miles out and the lunar twelve to seventeen, inside its stated twenty (6.4).
- **"The new quieter 'aback' lines" / "The urgent alerts stopped."** SUPPORTED for this slice. ADDS: the per-sail line is logged for sails backed on purpose.
- **"The relay cut calls at 60 seconds ... --wait 50 fixed it."** The fix is in the door note from tick 0; the cut cannot be seen.
- **"Drill stand-by carried into the station. My first hand_over came back 'Nothing was run'."** CANNOT BE SEEN in session 3 or 4.
- **"At the change of the watch he's listed 'below, asleep' while still holding it."** SUPPORTED as his own report at the time (54007); the list itself is not in the log.
- **"The contrary-orders warning fires on ordinary sequences."** SUPPORTED (43088, 43251).
- **"The schooner's 'get under way' doesn't cast her head onto the ordered tack ... had to be backed off by hand."** SUPPORTED, with the qualifications in 6.5.
- **"'Trim sails' acts before the helm has swung."** His working habit shows it (steer, wait for steady, trim); the fault itself is not shown in the slice.
- **"Lead standing orders fight for hands."** MILD SUPPORT: one lead order waiting behind the braces (56514) and held during the weigh (37913).
- **"Each boat trip carries one bargain and takes about 4½ hours."** SUPPORTED: 4 h 36 m for 40 tons, 3 h 34 m for 20, and the refusal at 7793.
- **"Other ships keep a fixed distance."** SUPPORTED, and explained (6.3).
- **"Number words above twelve fail."** ADDS NUANCE. `buy forty tons of coal` (7792) and `buy twenty tons of pilchards` (24374) were taken. The failing case is later: "Order not carried out ('buy sixteen tons of brandy'): How many tons? Say 'buy twenty tons of tin'." (212160). So tens are known and at least "sixteen" is not.
- **"'Full and by' is refused as changing your course. The permission had to be 'keep her full', and the name doesn't match the order."** ADDS NUANCE. The captain's first wording, `You may full and by`, was taken at once (43096); it is the *logged name* that differs ("may keep her full").
- **"The hand lead says 'no bottom at twenty fathoms' while the depth reads 15 or more."** Not in this slice. Here "No bottom at twenty fathoms" (41016) sits beside the officer's "Twenty-two fathoms" (41125), which agree.

## 9. New findings not in the notes

Ranked by weight.

1. **Why other ships seem to keep their distance: the lookout's estimate for a sail is held until the player's own ship has moved a mile** (SOURCE, `lookout.py` `_judge`; evidence in 6.3). At anchor or hove to, every vessel keeps the distance first called, however far she goes. The cutter said to be "two miles" off was within hail five minutes later.
2. **`get under way` reports success that has not happened** (6.5). "She has paid off" and "Under way on the starboard tack ... steering SE by S (146°)" were logged while she lay head to wind with sternway; "Her sails aback; she had no way on to lose" followed two minutes later. The schooner's evolution also speaks the frigate's words.
3. **How allowances really behave** (section 3). They do not lapse with the watch, they survive re-seating, they are keyed to a verb and its exact tail, a duplicate is accepted silently, each one given while he stands by wakes the officer, one was granted in words the order grammar then refused (534267 against 534277), and `steer` makes the refusal of `come up half a point` pointless.
4. **The lunar** (6.4). A star lunar was allowed at and after sunrise; by design it overwrites the longitude however good the account; the next noon's "Course made good ... SSE" then reports a course never steered; and a rough working from the landfall puts the old account four to nine miles out and the lunar twelve to seventeen, so the worse figure did replace the better, though by less than the note says.
5. **What is notable and what is not.** A pilot's hail and the making-out of a strange sail's colours are routine; each ten-minute cast at anchor, each "not hands enough" line and each firing of a trim order is notable. The officer reported an identified cutter as a possible privateer because of it (42649), and "stand by until a notable event" lasted 20 ticks (75004).
6. **The Plymouth pilot boards a departing ship unasked,** reads her the directions for coming in, "took charge" without giving an order, and mentions a breakwater not yet begun (6.2).
7. **The standing-order event "a wind shift" is twice as sensitive as the log's line,** and a trim that changes nothing still logs two notable lines (6.6).
8. **Two harness slips in one half hour:** a captain's word that did not wake the station (82334 to 83157) and a stand-by satisfied by the station's own earlier query (83442, 83443).
9. **The noon latitude was ten miles out after twenty hours in light airs** (111720), far more than the primer's "few per cent".
10. **Who has the con is not recorded.** For eight hours the captain worked the ship with the deck still the officer's; on waking the officer changed the captain's course. Nothing in the log marks the arrangement except the captain's remark at 54097.
11. **"Taken aback" is logged for sails backed on purpose** (five of seven lines; 6.6).
12. **The lead reports the anchorage's chart note as its ground,** even outside the bay (6.8, item 1).
13. **Small faults of wording:** "whatting is she"; "may not full and by"; lower-case compass points in the officer's echoes; a made-out frigate lost as "the sail"; the pilot's cutter hailed afresh as an unknown cutter; "did you mean" missing the nearest match; "young gentlemen" in a merchantman.
14. **The price line in the log names four goods of eleven** ("and the rest", 7649), and the boat's time at the quay is an hour plus three minutes a ton.

## 10. Could not determine

- **Her speed at the moment the pilot boarded** (38880). No line gives it; the lines either side say she had no way on.
- **Her heading while she hung in irons,** and whether she would have paid off without the officer's four orders. Only his readings say head south-west, 34° on the bow, sternway.
- **Which vessel was "The sail on the starboard quarter" lost at 42240,** and whether the officer's "two cutters" at 16:50 were two vessels or one cutter under two entries.
- **The master's doubt before the lunar.** It is never printed in the slice.
- **Why the account over-ran ten miles in latitude** (the two-hourly log in light airs, a stream, or the way the traverse is carried between heaves). The dumps hold no true position.
- **What "62 miles" in the noon line measures.** The straight line from noon to noon is about 55 miles.
- **Whether a refused `hand_over` or the 60-second cut ever happened in these two games.** Refusals out of turn and results are not stored.
- **Why the captain's word at 82334 raised no waking.** The stamps suggest it crossed with a stand-by already sent; the save cannot show the order of arrival.
- **Whether the people list truly showed the officer "asleep"** at 20:00; no reading of the people is in the log.
- **Real time.** How long any wait was for the owner cannot be read from ticks.
