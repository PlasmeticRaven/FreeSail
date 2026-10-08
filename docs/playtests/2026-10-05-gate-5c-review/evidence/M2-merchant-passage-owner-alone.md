# M2. Session 1, "The merchant passage, Falmouth for Brest", the owner alone (gate m5c, item 1)

Reader's note on method. Everything marked LOG is a line of the session's log, quoted with its tick and ship's time. Where I give a likely cause I say whether it comes from the log or from reading the game's source (read only; nothing was run, no game tool was called). Positions marked "reconstructed" are worked by me from the log's own "by account" distances and bearings and the marks' coordinates in `data/charts/features/channel-west.yaml`; the save holds inputs only, so the truth is nowhere in this material.

---

## 1. Slice identity

- **Session** `1-merchant-passage-owner-alone`, the whole of it. Save `merchant-passage-complete.json` (44 KB, file dated 2 Oct 20:43; it stores the 89 inputs and is replayed for the dump).
- **Ticks** 0 to 139,713. **Ship's time** 12 June 1805 05:00:00 to 13 June 19:48:33, that is 38 h 48 m 33 s. 2,751 log events: 2,334 routine, 417 notable, 0 urgent.
- **Scenario** "The merchant passage, Falmouth for Brest", seed 7, book `merchant-passage.orders` (40 standing orders). **Ship**: the topsail schooner (the *Speedwell* by the scenario file's header; the log never names her), American colours, octant, no chronometer. Named people: Mr Travers, master; Mr Ray, mate; Mr Paul, boatswain; Ebenr. Schley, boy.
- **Model and door**: none. All 88 orders carry the actor `captain`: 41 are the scenario's (40 standing orders and `let go the best bower`, all at tick 0) and 47 were typed by the owner.
- **Build** m5c.

## 2. What happened

| Tick | Ship's time | Event (LOG) |
|---|---|---|
| 0 | 12 Jun 05:00 | Scenario opens: "Wind W, 14 knots, a moderate breeze." The book is entered: "The book holds 40 standing orders; 'standing orders' lists them." |
| 57 | 05:00 | "The best bower let go in nine fathoms and a half; forty-eight fathoms of cable veered." By 'the cargo': "Bought 40 tons of tin at Falmouth at £120 a ton, £4800 paid; the boat goes for it. The purse: £1200." |
| 396 to 14249 | 05:06 to 08:57 | Long-boat away, landed 05:28, shoved off 08:28, alongside 08:57: "40 tons of tin hoisted in and struck down into the hold; the manifest 40 tons of tin; room for 72 tons." 'sail on the ebb' orders her under way in the same second. |
| 15497 | 09:18 | "The best bower is aweigh." |
| 15600 | 09:20 | "Sail ho! A cutter standing out from the land on the larboard bow, bearing S, distant two miles." |
| 16005 | 09:26 | "Under way on the starboard tack, under the topsail and the mainsail and the jib; the best bower catted and fished; steering S by E (169°)." |
| 16200, 16320 | 09:30, 09:32 | Cutter hails; "The pilot, Mr Tregenza of Falmouth, came aboard from the cutter and took charge of her (American colours being no bar at Falmouth)." Plain sail made 09:37 to 09:44. |
| 17580 to 18490 | 09:53 to 10:08 | "The pilot asks for sail to be shortened: his cutter is coming off for him." Hove to 09:53:58. 10:00: "Hove the log: no way." 10:07: "Mr Tregenza left her in the cutter, clear of the outer road; the pilotage, £5, paid and his certificate signed." Filled away 10:08, steering SSE (161°). |
| 19200 to 23400 | 10:20 to 11:30 | "The Manacles bearing SSW, distant three miles: a danger." Bearings each glass of Manacle Point, Lowland Point, Black Head. Three sails sighted. |
| 25200 | 12:00 | "Noon. Latitude by observation 49° 54' N; the reckoning was 50° 02' N. Course made good since the departure S, a mile. Longitude by account 5° 03' W." Then (12:00:45) "Hove the log: seven knots and a half." Land out of sight 12:21. |
| 28140 | 12:49 | "Sail ho! A sail on the larboard bow, bearing SE by E, distant three leagues." (the gate's sail off the Lizard) |
| 30145 to 30490 | 13:22 to 13:28 | The owner's first five lines: `the people`, `the hold`, `the cabin`, `the well`, `the stores`. |
| 32400 | 14:00 | 'the course across' shapes its first course: "S by W by account, 97 miles." Re-shaped every hour to 01:00. |
| 43616, 55489, 59063 | 17:06, 20:24, 21:24 | Wind veered WNW, backed W, veered WNW. Sunset 20:03. |
| 61020, 61200 | 21:57, 22:00 | "A light right ahead, bearing S by W." "The light on Ushant bore S by W, nine leagues by estimation." Course to the soundings goes from "S by W ... 49 miles" (21:00) to "SSW ... 44 miles". |
| 72000 | 13 Jun 01:00 | "The light on Ushant bore E by N, three leagues by estimation." (abeam) |
| 75600 | 02:00 | "Shaped a course for the Passage de l'Iroise: E by S by account, 18 miles." |
| 80220 | 03:17 | "Ushant bearing N, distant six miles." "Molène bearing ENE, distant five miles." Sunrise 03:58. |
| 82800 | 04:00 | Hourly Iroise course held: "the distance to ushant is 7 miles by account, not over 10 miles." |
| 83520 to 86700 | 04:12 to 05:05 | "Béniguet bearing E by N, steady and closing: distant four miles." La Helle and the Black Rocks named as dangers three miles off. Five bearings running: "Béniguet bore ..., a mile by estimation." |
| 87242 | 05:14 | 'past the Iroise': "SE by account, 6 miles." |
| 88080 | 05:28 | "Sail ho! A sail on the larboard bow, bearing E, distant two leagues." (the Brest pilot's cutter) |
| 91380, 91560 | 06:23, 06:26 | Hail; fore topsail in; "The pilot, Mr Le Floch of Brest, came aboard from the cutter and took charge of her (American colours being no bar at Brest)." His words, the news, the letter. |
| 91620 | 06:27 | "The captain read it: The tin will fetch its price; the Prefect maritime asks that the papers be shown at the castle." |
| 96147, 96475 | 07:42, 07:47 | "And a quarter thirteen; sand and mud." 'in the road' anchors her: "The best bower let go in 13 fathoms and a half." Brought up 08:06. |
| 96475 to 108960 | 07:47 to 11:16 | At anchor on the ebb; a cast and a bearing every five minutes (38 casts, 14 down to 12¼ fathoms). |
| 108960 | 11:16 | "The cable slack at the turn; she swings to the flood." 'the flood' gets her under way; aweigh 11:36. |
| 110675 | 11:44 | "Under way on the larboard tack, under the topsail and the mainsail and the jib; the best bower catted and fished; steering E (90°)." Plain sail; course for the Goulet's mouth. |
| 111660 | 12:01 | "Noon. Latitude by observation 48° 23' N; the reckoning was 48° 19' N. Course made good since yesterday S by E, 127 miles. Longitude by account 4° 39' W." |
| 111817, 111840 | 12:03, 12:04 | The owner asks `the pilots words` and `the pilot cutter`. |
| 112005 to 114382 | 12:06 to 12:46 | Six points through the Goulet north of the Mingan and the Fillettes; 17 casts, 20 bearing lines. |
| 115285, 115534 | 13:01, 13:05 | "By the mark thirteen; mud." 'in the Bay' anchors her: "The best bower let go in twelve fathoms and a half." |
| 116377 | 13:19 | "Brought up by the best bower in six fathoms and a half, sixty-three fathoms of cable; Riding by the best bower to the flood, the wind across the tide." 'the agent' sends the boat with the mate. |
| 123004 | 15:10 | Boat alongside with the prices. "Sold 40 tons of tin at Brest at £270 a ton, £10800 taken; the boat lands it. The purse: £11995." |
| 123364 to 139604 | 15:16 to 19:46 | Long-boat away "with the goods sold", at the quay 15:58 to 18:58, alongside 19:46. Swings to the ebb 16:50. |
| 129600 | 17:00 | The gate's 36 hours end here. |
| 130160 to 130694 | 17:09 to 17:18 | The owner types 25 lines; goes below at 17:12. |
| 139369 to 139703 | 19:42 to 19:48 | `the purse` twice, `the people`, then nine tries to get back on deck. Save at 139713. |

## 3. The deck and the captain's words

- **The deck** was never given or taken: no officer was seated. 130362 (13 Jun 17:12) `retire to the cabin`: "The captain went below to his cabin; the deck is the officer of the watch's." That line came three minutes after four lines were refused with "There is no officer of the watch at the station". 139699 (19:48) `come on deck`: "The captain came on deck."
- **`You may ...`**: four tried at 130160 to 130176 (17:09): `You may wear ship`, `You may tack ship`, `You may send the boat`, `You may live`. All four refused in the same words (section 4); none could be used. The refusal answers before the allowance is parsed, so the nonsense `You may live` got the same reply as the real ones.
- **Tell/ask**: none to an officer. He asked the pilot four times (130666 to 130694).
- **By hand**: nothing. None of his 47 lines touched sail, helm, anchor, boat or cargo; the book did the passage.
- **On this ship the master is the captain.** `the people` lists "Mr Travers, master" and no captain, and `send for the master` answers "You are the captain; there is no sending for yourself." (130224, 139685). Mr Travers moves with the player: "on the quarterdeck" at 17:12 (130347), "in the cabin" at 19:47 (139637). The source says so in a comment (`freesail/world/people.py:321`, "a vessel whose master commands ... the master is the captain"). Nothing the player can read says it.

**Every line the owner typed** (47; 8 accepted orders, 17 readings answered, 22 refused):

| Tick | Time | Typed | Reply (LOG) | What he seems to be after |
|---|---|---|---|---|
| 30145 | 12 Jun 13:22 | `the people` | "The people: Mr Travers, master: on the quarterdeck. Mr Ray, mate: on the quarterdeck. Mr Paul, boatswain: on the deck. Ebenr. Schley, boy: on the quarterdeck." | Gate item 1's check |
| 30157 | 13:22 | `the hold` | "The manifest: 40 tons of tin; room for 72 tons." | The cargo |
| 30163 | 13:22 | `the cabin` | refused (section 4) | A place as a reading |
| 30358 | 13:25 | `the well` | "The well: the ship has no well to sound yet; that reading comes with the world." | Note 2 |
| 30490 | 13:28 | `the stores` | "The stores: water 8 tons, provisions for 60 days." | |
| 111817 | 13 Jun 12:03 | `the pilots words` | "The pilot: Mr Le Floch of Brest aboard; high water at Brest about half past four in the afternoon, the tide rising some 21 feet; the flood is making now and serves." | The pilot's directions again; he got the pilot-and-tide reading instead |
| 111840 | 12:04 | `the pilot cutter` | "A sail in sight: not in sight." | Where the cutter was (note 1) |
| 130160 to 130176 | 17:09 | `You may wear ship`, `You may tack ship`, `You may send the boat`, `You may live` | refused ×4 | Trying the allowance grammar |
| 130195 | 17:09 | `the boats` | "The boats: the long-boat (20 ft, 6 oars, 7 hands), the yawl (16 ft, 4 oars, 5 hands)." | |
| 130202, 130310 | 17:10, 17:11 | `The boatswains store`, `The boatswains stores` | "The boatswain's store holds 150 fathoms of spare cordage." ×2 | |
| 130207 | 17:10 | `Brest` | refused | The port |
| 130218 | 17:10 | `Send the master ashore` | refused | Very likely the letter's errand (the papers to the castle) |
| 130224 | 17:10 | `Send for the master` | refused | |
| 130234 | 17:10 | `Send for the boatswain` | "Passed the word for Mr Paul by Ebenr. Schley; he is on the deck." then 130294 "Mr Paul came aft, sent for." | Gate item 6's check |
| 130246, 130254 | 17:10 | `Ask the boatswain`, `The boatswain` | refused ×2 | Something to do with a man once sent for |
| 130265, 130279, 130319 | 17:11 | `Send the boatswain below`, `Send down the boatswain`, `Send the boatswain ashore` | refused ×3 | To dismiss him or send him ashore |
| 130347 | 17:12 | `the people` | "... Mr Paul, boatswain: on the quarterdeck. ... Mr Le Floch, pilot: on the quarterdeck." | |
| 130362 | 17:12 | `retire to the cabin` | "The captain went below to his cabin; the deck is the officer of the watch's." | |
| 130395 | 17:13 | `send for the boatswain` | "Passed the word for Mr Paul by Ebenr. Schley; he is on the quarterdeck." then 130455 "Mr Paul came to the cabin, sent for." | Sending for a man from below |
| 130406 | 17:13 | `the epitome` | "The epitome: Moore's table of high water by the moon's bearing (Moore 1799) ... Brest: 3h 45m at full and change (the moon SW by W). ..." | |
| 130424 | 17:13 | `THe port` | "The port: at anchor in Brest, the Bay of Brest; the port neutral to the Americans; the pilot Mr Le Floch aboard; the long-boat away with the goods sold, at the quay." | |
| 130550 | 17:15 | `the prices` | "The prices: at Brest (13 June, Afternoon watch (15:10)): wine £35 a ton, brandy £110 a ton, canvas £40 a ton, salt £12 a ton, hemp £55 a ton, tin £270 a ton, pilchards £45 a ton, coal £9 a ton, timber £5 a ton, salt beef £70 a ton, copper ore £30 a ton." | Note 3 |
| 130666 | 17:17 | `ask the pilot about the channel` | "Mr Le Floch: Range along either shore of the Goulet and fear nothing, but not the middle ... and you are in the south channel." | |
| 130684 | 17:18 | `Ask the pilot how` | the whole speech again, the tide now "High water at Brest about a quarter to five in the morning ... the flood will serve from about half past ten at night." | |
| 130690, 130694 | 17:18 | `Ask the pilot` ×2 | the channel answer again ×2 | Looking for more than four stock answers |
| 139369, 139422 | 19:42, 19:43 | `the purse` ×2 | "The purse: £11995." ×2 | The money, after the boat was back |
| 139637 | 19:47 | `the people` | "The people: Mr Travers, master: in the cabin. Mr Ray, mate: on the deck. Mr Paul, boatswain: in the cabin. Ebenr. Schley, boy: on the quarterdeck. Mr Le Floch, pilot: on the quarterdeck." | |
| 139644 | 19:47 | `where is the mate` | "Where is the mate: Mr Ray, on the deck." | |
| 139648 to 139690 | 19:47 to 19:48 | `where am I`, `go to the deck`, `take the deck`, `leave my cabin`, `go to my cabin`, `call for the master`, `send for the master`, `captain takes the deck` | refused ×8 | Getting out of the cabin |
| 139699 | 19:48 | `come on deck` | "The captain came on deck." | The form that works |
| 139703 | 19:48 | `come on deck again` | refused: "You are on the quarterdeck already." | |

The typing fell in four short bursts (345, 23, 534 and 334 ticks long), so the clock was near 1x while he typed and the 22½ hours between 13:28 on the 12th and 12:03 on the 13th passed with no input at all.

## 4. Orders refused

117 `order.rejected`, no `agent.refused` (no agent). 22 are the owner's, 95 the book's.

**The owner's 22.** Classes: (a) vocabulary or grammar gap, (d) ship-state refusal that is correct, (e) apparent bug.

| Tick, time | As typed | The refusal's words | Class | What worked |
|---|---|---|---|---|
| 30163, 12 Jun 13:22 | `the cabin` | "'the cabin' is not an order this ship understands; did you mean 'take in', 'the booms' or 'ask the pilot'? An order begins with a verb such as set, take in, furl, reef, shake out, brace, trim or haul." | (a) a place is not a reading; `the places` is the form, never suggested | nothing tried |
| 130160, 130167, 130170, 130176, 13 Jun 17:09 | `You may wear ship`, `You may tack ship`, `You may send the boat`, `You may live` | "There is no officer of the watch at the station; a model's door seats one first (docs/agents/Harness.md), and then the captain gives the deck." | (d) correct. The reply puts a file path in a line of the ship's log | none |
| 130207, 17:10 | `Brest` | "'brest' is not an order this ship understands; did you mean 'brace'? ..." | (a) a port's name alone | `THe port` at 130424 |
| 130218, 17:10 | `Send the master ashore` | "'send the master ashore' is not an order this ship understands; did you mean 'send the boat', 'send for' or 'send down'? ..." | (a) "send <person> ashore"; the form is `send the boat ashore with ...`. The boat was away, and on this ship the master is himself | none |
| 130224, 17:10 and 139685, 19:48 | `Send for the master` | "You are the captain; there is no sending for yourself." | (d) by the rule, but it reads as (e): `send for the master` is the primer's own example and `the people` gives no sign that Mr Travers is the player | none |
| 130246, 17:10 | `Ask the boatswain` | "'ask the boatswain' is not an order this ship understands; did you mean 'ask the pilot' or 'ask the watcher'? ..." | (a) only the pilot and the watcher can be asked | none |
| 130254, 17:10 | `The boatswain` | "'the boatswain' is not an order this ship understands; did you mean 'the boatswains store', 'the booms' or 'ask the pilot'? ..." | (a) `where is the boatswain` is the form | `the people` |
| 130265, 17:11 | `Send the boatswain below` | "... did you mean 'send the boat', 'send for' or 'send down'? ..." | (a) no order dismisses a man sent for | none |
| 130279, 17:11 | `Send down the boatswain` | "There is no such part as the boatswain in this ship. ('send down' was understood.)" | (a) read as sending down a spar | none |
| 130319, 17:11 | `Send the boatswain ashore` | as 130218 | (a) | none |
| 139648, 19:47 | `where am I` | "'where am i' is not an order this ship understands. ..." | (a) | `the people` says it only if you know who you are |
| 139657, 19:47 | `go to the deck` | "'go' is a console command, not an order to the ship; the ship takes orders such as 'set the topsails' or 'steer south-west'." | (a), and inconsistent: `go to my cabin` ten ticks later is understood | |
| 139660, 19:47 | `take the deck` | "... did you mean 'take in', 'take in water' or 'take a lunar'? ..." | (a) | |
| 139665, 19:47 | `leave my cabin` | "... did you mean 'ease' or 'heave to'? ..." | (a) | |
| 139667, 19:47 | `go to my cabin` | "You are in the cabin already." | (d) correct, and it told him where he was | |
| 139680, 19:48 | `call for the master` | "... did you mean 'allow' or 'call all hands'? ..." | (a) `call the master` is taken, `call for` is not | |
| 139690, 19:48 | `captain takes the deck` | "'captain takes the deck' is not an order this ship understands. ..." | (a) | `come on deck` at 139699 |
| 139703, 19:48 | `come on deck again` | "You are on the quarterdeck already." | (d) correct | |

Nine tries in 51 ticks to leave the cabin; none of the eight refusals suggested `come on deck`.

**The book's 95.**

| Count | Standing order, order | Span | The refusal's words | Class |
|---|---|---|---|---|
| 54 | 'in the Bay', `come to an anchor` | 116489 (13 Jun 13:21) to 139590 (19:46); 28 of them inside the gate's 36 hours | "she is at anchor already, riding by the best bower" | (d) correct refusal of a firing that should not happen: the rule's guard "the speed is over 2 knots" reads her way through the water, and the stream gives an anchored ship two knots (see 6.6) |
| 29 | 'tend the sheets', `trim the sheets` | 1800 (12 Jun 05:30) to 138600 (13 Jun 19:30) | "She is at anchor; 'trim the sheets' must wait till she weighs." | (d) correct, every glass at anchor |
| 9 | 'trim on a shift', `trim sails` | 8306 (12 Jun 07:18) to 130327 (13 Jun 17:12) | "She is at anchor; 'trim sails' must wait till she weighs." | (d) |
| 1 | 'clear of the road', `shape a course for 50 00 N 4 57 W` | 17612 (12 Jun 09:53) | "She is hove to; fill away before giving her a course." | (d) |
| 1 | 'under way again', `set plain sail` | 18490 (10:08) | "Could not set plain sail: 'set the plain sail': Nothing done: the fore sail is already set; the main sail is already set; ..." | (d) a no-op said as a refusal |
| 1 | 'the tin sold', `sell forty tons of tin` | 139604 (13 Jun 19:46) | "The hold has 0 tons of tin, not 40; the manifest says so." | (d) the rule fired again when the boat came back from landing the tin |

## 5. Harness behaviour

Does not apply: no model was seated at any station in this session (the transcripts and journals dumps are empty).

## 6. Ship, sea, navigation and port observations

### 6.1 The run against the gate's account

The run is the gate's reference run, to the tick and to the line. The ticks pinned in `tests/test_known_truths.py` (lines 3709 to 3731: the tin aboard, under way, both pilots aboard, the pilot off, the sail, both noons, the three anchors, the turn to the flood, the Goulet's mouth, the sale) all agree. The reference log is 2,460 lines at 36 hours (`GATE_5C_MERCHANT_LINES`). This log has 2,468 lines at or before tick 129,600: the 2,460, the owner's 7 lines typed before then (five on the 12th, two at noon on the 13th), and the server's one opening line about the book, which the test's bare world does not print (`freesail/ui/server.py:954`). A reading typed at the prompt changes nothing aboard, so nothing he typed moved the passage, and compression cannot move it either.

| The gate's account (seed 7) | LOG: tick, time, words | Agrees? |
|---|---|---|
| anchored in Carrick Road at the start | 57, 12 Jun 05:00:57: "The best bower let go in nine fathoms and a half; forty-eight fathoms of cable veered." | yes |
| forty tons of tin bought at £120 | 57: "Bought 40 tons of tin at Falmouth at £120 a ton, £4800 paid; the boat goes for it. The purse: £1200." | yes |
| aboard by the lighter at 08:57 | 14249, 08:57: "40 tons of tin hoisted in and struck down into the hold; the manifest 40 tons of tin; room for 72 tons." | time yes. The word "lighter" is nowhere in the log (0 matches); the log shows only the long-boat going "for the goods bought" and coming back |
| under way on the ebb at 09:26 | 16005, 09:26 | yes |
| the Falmouth pilot off at 10:07 | 18420, 10:07 | yes |
| a sail off the Lizard at 12:49 hailed and not made out | 28140, 12:49: "Sail ho! A sail on the larboard bow, bearing SE by E, distant three leagues." Never made out; lost at 16:16 (probably her: 40560 "The sail on the larboard quarter is out of sight.") | yes. "Hailed" is the lookout's hail. She was some fifteen miles to the south-eastward of the Lizard (reconstructed), the land lost since 12:21 |
| Ushant's light at night | 61020, 21:57: "A light right ahead, bearing S by W." Eleven bearings 22:00 to 03:00 | yes; see 6.5 for what "right ahead" meant |
| the Brest pilot aboard in the Iroise at 06:26 with a letter | 91560, 13 Jun 06:26 | yes. By the bearing a minute before she was three miles south of St Matthew's Point; "4 miles by account" from the road of Bertheaume |
| anchored in Bertheaume road at 07:47 | 96475, 07:47: "The best bower let go in 13 fathoms and a half." | yes |
| the Goulet taken on the flood by the pass north of the Mingan with the lead and bearings every five minutes | turn 108960 (11:16); under way 110675 (11:44); the six points 112005 to 114382 (12:06 to 12:46); 17 casts and 20 bearing lines to the anchor | yes |
| anchored in the Bay at 13:05 | 115534, 13:05: "The best bower let go in twelve fathoms and a half." | yes |
| the tin sold at 15:10 for £10,800 | 123004, 15:10: "Sold 40 tons of tin at Brest at £270 a ton, £10800 taken; the boat lands it. The purse: £11995." | yes |
| No grounding | no `ship.aground`, no "dragging" (0 matches each) | yes |
| 36 hours | the save runs to 139,713 = 38 h 48 m | the owner let it run 10,113 ticks (2 h 48 m 33 s) past the gate's end |

**Differences, all in words, none in events.**
1. **Item 1 says "the purse moves by £6,000".** In the log the purse moves by £10,800 at the sale (£1,195 to £11,995). £6,000 is the venture's profit (£10,800 less £4,800); the purse over the voyage moves by £5,995 (£6,000 to £11,995), the £5 being the Falmouth pilotage. The paragraph's "sold ... for £10,800" is the figure the log supports.
2. **Item 1 says "`sell the tin` after the boat has been ashore".** The owner never typed it; the book's 'the tin sold' sold in the same tick the boat came alongside (123004).
3. **The lighter** is not in the log's words (above).
4. **The scenario file's header and primer 15** both promise "the Iroise in her chart's words at the deep-sea lead's cast". No deep-sea cast is made at seed 7: the four rules for it never fired (6.6). The gate's paragraph leaves it out; the test's docstring and `docs/dev/TuningNotes.md` (line 1393) say it "was not made at seed 7".

**After the tin was sold (15:10).** The long-boat left at 15:16 "with the goods sold", lay three hours at the quay and was alongside at 19:46. Nothing else happened to the ship: she rode at anchor and swung to the ebb at 16:50 (129000). The book went on working as if under way: after the sale 56 more casts of the lead (all notable), 64 more bearing lines, 32 more refused "come to an anchor" and 11 refused trims, in 440 lines of log. The pilot stayed aboard (6.2). Thirty-nine of the owner's 47 lines fall in this stretch, all after 17:09.

### 6.2 The pilots (the owner's notes 1 and 9)

**What the player had to do to get a pilot: nothing.** The owner typed nothing between tick 0 and 30145. The Falmouth pilot came, boarded, asked to be put off, left and was paid £5 without a keystroke. There is no order in the log (or in primer 14's table of forms) to call, accept or refuse a pilot. By the source (`freesail/world/ports.py:684` to 776, read only) a cutter is launched from the port's outer road whenever no pilot is aboard and the ship is within the port's cruising ground, under sail with a knot of way, by day, not at anchor and not an enemy; she hails within four cables and the pilot boards within two cables when the ship's speed over the ground is six knots or less. The only refusal open to a captain is to keep more than six knots on her. The book's part is three rules: fore topsail in at the hail, heave to when he asks to be put off, fill away when he is gone.

**Falmouth, Mr Tregenza.**

| Tick, time | LOG | She was |
|---|---|---|
| 15497, 09:18 | "The best bower is aweigh." | casting |
| 15600, 09:20 | "Sail ho! A cutter standing out from the land on the larboard bow, bearing S, distant two miles." | two minutes after aweigh; the outer road (the cutter's launching place) is 1.8 miles south of Carrick Road |
| 15720, 09:22 | "The cutter on the larboard bow is the Falmouth pilot's cutter, standing to the northward (N by E), under plain sail; British colours, the red ensign." | (within a mile and a half by primer 15's rule) |
| 16005, 09:26 | "Under way on the starboard tack ... steering S by E (169°)." | under way |
| 16200, 09:30 | "The cutter hailed: a pilot for Falmouth; shorten sail and he will come aboard." 'the pilot boards': "taking in the fore topsail." 16201: "Not hands enough on deck to take in the fore topsail; ..." | under way 3¼ minutes |
| 16282, 09:31 | "Clewed up the fore topsail." | |
| **16320, 09:32** | **"The pilot, Mr Tregenza of Falmouth, came aboard from the cutter and took charge of her (American colours being no bar at Falmouth)."** | **under way 5¼ minutes, steering S by E under mainsail and jib, the fore topsail clewed up; not hove to. No speed is logged (I put it at three to five knots from the bearings at 09:30 and 10:00).** |
| 16338, 09:32 | "Took in the fore topsail; hanging in the gear." | 18 seconds after he boarded |
| 16320 | 'the pilot aboard' sets plain sail at once: "Standing orders 'the pilot boards' and 'the pilot aboard' (both the captain's) give contrary orders on the fore topsail; the later stands." | the topsail was set again by 09:37 |
| 17580, 09:53 | "The pilot asks for sail to be shortened: his cutter is coming off for him." 'the pilot put off': "heaving to." | |
| 17638, 09:53 | "Hove to, fore topsail to the mast, helm a-lee." | hove to |
| 17640, 09:54 | "Sail ho! The Falmouth pilot's cutter abeam to starboard, bearing NW by N, distant eight cables." | |
| 18038, 10:00 | "Hove the log: no way." | |
| 18240, 10:04 | "The cutter hailed: she has come off for the pilot." | |
| **18420, 10:07** | **"Mr Tregenza left her in the cutter, clear of the outer road; the pilotage, £5, paid and his certificate signed."** | **hove to, no way** |
| 19080, 10:18 | "The cutter on the starboard quarter is out of sight." | |
| 21060, 10:51 | "The sail right astern is out of sight." | |

What he said (16320): "The pilot says: Keep the fair way and the lead going; there is a narrow deep channel of sixteen or eighteen fathoms all the way into Carrick Road. The Black Rock lies nearly in the middle of the entrance and shows itself at half tide; the eastern channel is the better ... Moored in the Road, keep the hawse open to the southward ... High water at Falmouth about five o'clock in the evening, the tide rising some 17 feet; the flood will serve from about eleven o'clock in the morning." News: "Britain at war with the Batavian Republic, France and Spain; the United States, Portugal and Denmark at peace with all."

**Brest, Mr Le Floch.**

| Tick, time | LOG | She was |
|---|---|---|
| 88080, 05:28 | "Sail ho! A sail on the larboard bow, bearing E, distant two leagues." | steering SE; about seven miles west of the road of Bertheaume, the cutter's launching place |
| 89760, 05:56 | "The sail abeam to larboard is a cutter standing out from the land, standing to the south-westward (WSW), under plain sail." | (within four miles) |
| 90036, 06:00 | "Hove the log: four knots and a half." | plain sail |
| 90840, 06:14 | "The cutter on the larboard bow shows French colours, the tricolour." | (within two miles) |
| 90960, 06:16 | "The cutter on the larboard bow is the Brest pilot's cutter, standing to the south-westward (SW), under plain sail; French colours, the tricolour." | (within a mile and a half) |
| 91380, 06:23 | "The cutter hailed: a pilot for Brest; shorten sail and he will come aboard." | |
| 91499, 06:24 | "Took in the fore topsail; hanging in the gear." | |
| 91500, 06:25 | "St Matthew's Point bore N by E, three miles by estimation." | |
| **91560, 06:26** | **"The pilot, Mr Le Floch of Brest, came aboard from the cutter and took charge of her (American colours being no bar at Brest)."** | **under way, steering E by N (81°), 4½ knots by the log 26 minutes earlier and now without her fore topsail; not hove to** |
| 91560 | "A letter from the agent of the owners came aboard by the pilot cutter; Ebenr. Schley took it aft for the captain, who is on the quarterdeck." | |
| 91620, 06:27 | "Ebenr. Schley brought a letter from the agent of the owners to the captain on the quarterdeck." "The captain read it: The tin will fetch its price; the Prefect maritime asks that the papers be shown at the castle." | |
| 106320, 10:32 | "The sail on the starboard bow is out of sight." | at anchor in the road; this can only be the cutter, now called "the sail" |
| 111840, 12:04 | (the owner's `the pilot cutter`) "A sail in sight: not in sight." | |
| 130347 (17:12), 130424 (17:13), 139637 (19:47) | "Mr Le Floch, pilot: on the quarterdeck." "... the pilot Mr Le Floch aboard ..." | **never left** |

What he said (91560): "The pilot says: Range along either shore of the Goulet and fear nothing, but not the middle, for the Fillettes and the Mingan lie there; the passage between them is very dangerous for the rocks under water. Keep the castle of Brest in full view, clear of Penaleuch point, and you are in the south channel. When Point Bertheaume bears north you may stand to the east for the Goulet. ... High water at Brest about half past four in the afternoon, the tide rising some 21 feet; the flood will serve from about a quarter past ten in the morning." The same news as Falmouth's.

**Points for the lead.**
1. **Both pilots boarded with the ship under way, neither hove to**; at Falmouth before the sail the book takes in was even in. Leaving was hove to with no way on.
2. **No distance is logged at the moment of boarding or of leaving.** "came aboard from the cutter" follows a last stated distance of two miles (Falmouth) or two leagues (Brest). The model's "two cables on boarding but not on leaving" cannot be checked from words here.
3. **The inward pilot never leaves and is never paid.** No `port.pilot_left` for Mr Le Floch; the purse is £11,995 = £1,200 less £5 plus £10,800. By the source a pilot is fetched off only when the ship is a mile beyond the outer road and opening from the anchorage (`ports.py:743` to 776), which an inward-bound ship at her anchor never is. He was on the quarterdeck 6½ hours after the anchor went down in the Bay.
4. **The outward pilot is offered as an inward one.** Six minutes out from her anchorage the Speedwell is hailed "a pilot for Falmouth" and told the way "all the way into Carrick Road", how to moor there and when the flood serves, while she leaves on the ebb. The code has no inward or outward: any ship with way on in the cruising ground gets the hail and the same words.
5. **"took charge of her"** is said both times; in both cases the book's own courses went on being shaped. With Mr Tregenza "in charge" (16846, 09:40) the book "Shaped a course for 50° 00' N, 4° 57' W: SSE by account, 9 miles; the line crosses the Old Wall." and nothing answered the warning. The book's comment has it right: "the pilot aboard answers and does not con".
6. **There were two Falmouth cutters.** The second "Sail ho!" (17640) is a new vessel launched at the outer road to fetch him while the first is going home (`ports.py:748`, `_launch_cutter(port, "fetch")`). It appears eight cables off, abeam, in clear weather, already known for the pilot's cutter. That is why the log loses eight sails and sights seven (6.7).
7. **The letter outran its cutter.** 90000 (06:00): "World order (the scenario): a letter from the agent of the owners left at Brest." The cutter had been at sea in the Iroise since before 05:28, ten miles outside the Goulet; she handed the letter over at 06:26. In the code every letter waiting at the port goes with the pilot at the instant he boards (`ports.py:839`). Primer 14's rule is "Nothing arrives from nowhere".
8. **The letter asks for something the game cannot do.** "the Prefect maritime asks that the papers be shown at the castle": the owner's `Send the master ashore` and `Send the boatswain ashore` (130218, 130319) look like attempts at it.
9. **The pilot at anchor still gives the way in.** Asked four times at 17:17 to 17:18 in the Bay, he repeated the Goulet's directions.
10. **The tide words differ by an hour from the stream.** Pilot: "the flood will serve from about a quarter past ten in the morning"; the lead's least water at Bertheaume was 12¼ fathoms at 09:51 to 10:51, and the stream turned at 11:16 (108960). That is low water against slack, as it should be; the book rightly waits for the turn.

### 6.3 "The well" and other readings that answer with a "no" (the owner's note 2)

- 30358 (12 Jun 13:25:58), typed `the well`: **"The well: the ship has no well to sound yet; that reading comes with the world."** These are the designed words for a reading not yet built (primer 10 quotes the sentence). `sound the well` was not typed in this session.
- 111840 (13 Jun 12:04), typed `the pilot cutter`: "A sail in sight: not in sight." The wording stumbles ("in sight: not in sight"), and it answers a question about the cutter with a line about any sail.
- 18038 (12 Jun 10:00): "Hove the log: no way." A true reading, taken in the fourteen minutes she lay hove to; it then stood as her speed for two hours (6.5).
- Three casts "No bottom at twenty fathoms." (6.4). No "NaN", "None", "null" or "no water" anywhere in the log (0 matches).

### 6.4 The lead and the chart (the owner's note 6)

136 `sounding` lines, all notable, first 95942 (13 Jun 07:39), last 139590 (19:46). 116 were taken at anchor, 20 under way.

| Kind of line | Count | Example (LOG) |
|---|---|---|
| "By the mark <n>; <ground>." | 28 | 98800, 08:26: "By the mark thirteen; sand and mud." |
| "By the deep <n>; <ground>." | 9 | 97893, 08:11: "By the deep fourteen; sand and mud." |
| "And a half <n>; <ground>." | 26 | 98198, 08:16: "And a half thirteen; sand and mud." |
| "And a quarter <n>; <ground>." | 27 | 96147, 07:42: "And a quarter thirteen; sand and mud." |
| "Quarter less <n>; <ground>." | 43 | 95942, 07:39: "Quarter less fourteen; sand and mud." |
| "No bottom at twenty fathoms." | 3 | 112300 (12:11), 113200 (12:26), 114092 (12:41), all in the Goulet |
| missing or odd depth | 0 | none |

Grounds: "mud" 81, "sand and mud" 46, "rock and mud" 6. The six "rock and mud" casts are all in the Goulet (12:06 to 12:46), so the owner's "NaN fm rock and mud" was one of those. Marks and deeps are called correctly (thirteen and seventeen by the mark; eleven, twelve and fourteen by the deep).

**The log is not where the chart chokes; every cast with a depth chokes it.** From the source (read only): `client/map.js:450` writes the label as `Math.round(s.depth_m / U.FATHOM) + " fm"`, and `client/units.js` exports `KNOT`, `NAUTICAL_MILE`, `CABLE` and `POINT` but no `FATHOM`. A number divided by an undefined constant is NaN, so each of the 133 casts with a depth draws "NaN fm" and its ground; the three with no bottom draw "no bottom". The reckoning's record carries a good `depth_m`. The same line and the same missing constant are in the m5c-b copy.

One inconsistency in the lead's own words: 113553 (12:32) "And a quarter twenty; rock and mud." from a hand lead that elsewhere says "No bottom at twenty fathoms." In the source the twenty-fathom cut is made on the true depth before the leadsman's quarter-fathom error is added (`reckoning.py:1252` to 1258).

### 6.5 The reckoning (the owner's note 7, and the gate's stated errors)

**What the log holds.** Two noon lines (25200, 111660; quoted in section 2). Two `master.place` lines: 27000 (12 Jun 12:30) and 113460 (13 Jun 12:31), both "Mr Travers came on deck, the day's work done." No lunar, no `work up the reckoning`, no reading of the reckoning or of its doubt. 244 `bearing.taken` lines (58 by 'bearings' each glass, 186 by 'pilot water' every five minutes); 155 of the 244 were taken at anchor. Every bearing is of the one nearest mark with a distance "by estimation"; there is no line that crosses two marks and no line of kind "fix". 12 heaves of the log, every two hours on the even hour, none at anchor.

**The gate's four figures against the log.**

| Gate (author's view of the truth) | What the log shows |
|---|---|
| 9.6 miles at the first noon | consistent: "Latitude by observation 49° 54' N; the reckoning was 50° 02' N" is eight miles in latitude alone |
| 0.8 at Bertheaume | cannot be seen; the five-minute bearings of Point Bertheaume agree with the account's "a mile" from the road's mark (97200) |
| 0.3 at the second noon | here it is the sight that is out: "Latitude by observation 48° 23' N; the reckoning was 48° 19' N" in the mouth of the Goulet. 48° 23' N is the latitude of Brest town, on the land four miles north of her |
| 0.7 in the Bay | cannot be seen |

The gate gives the error at four moments. Between the first two the log shows a good deal more.

**(a) The account stood still for two hours and the noon sight did not move it.** LOG, in order:
- 18038 (10:00:38): "Hove the log: no way." She was hove to from 09:53:58 to 10:08:10 for the pilot's boat. The next heave is 25245 (12:00:45): "Hove the log: seven knots and a half."
- 25200 (12:00): "Latitude by observation 49° 54' N; the reckoning was 50° 02' N. Course made good since the departure S, a mile." A mile, 2 h 34 m after getting under way in a fourteen-knot breeze.
- 25200, the same tick, after the sight and after the bearing "Black Head bore NW, three leagues by estimation": "Standing order 'the course across' every hour: not carried out; **the distance to falmouth is 8 miles by account**, not over 18 miles." Falmouth is at 50° 09' N. Eight miles from it is 50° 01' N, the old reckoning; the observed 49° 54' N is fifteen.
- 28800 (13:00): 'the course across' shapes no course. Its only guard that could fail is "the distance to Falmouth is over 18 miles", so an hour's run later the account still had her inside eighteen.
- 32400 (14:00): "S by W by account, 97 miles" to the soundings mark (48° 12' N 5° 24' W). That puts the account at about 49° 47' N 4° 56' W (reconstructed). From the noon observation, two hours SSE at seven knots is about 49° 41' N.

So the observed latitude, which agrees to the mile with that noon's bearing and distance of Black Head, was not put in place of the reckoned one. Primer 10 says it is ("the observed latitude replaces the reckoned one").

Likely cause, from the source (read only), two things together:
1. *The stale read.* The account runs at the log's last read. The read "no way" was taken while hove to. The source means a new read to cover the time since the last step (`reckoning.py:1194` to 1204, `bring_up(read)`), but every bearing steps the account first at the old read, and the book takes a bearing every glass. So 10:00 to 12:00 was run at no knots in four half-hour steps and the 7½ knots covered 45 seconds. `docs/dev/TuningNotes.md` (line 1391) has the same thing in the naval cruise: "7.1 miles at the first noon".
2. *The gate that decides whether a sight replaces the account.* `reckoning.py:675` to 727: an observation replaces the account across its line only if the account has run more than `FIX_RUN_NM` = 2.0 miles since the last observation; otherwise it is weighed against the master's own doubt. The run is counted in miles by account, which were nil. His doubt north and south can only have been small: it grows with the run, which was nil, and with the set at `SET_DOUBT_NORTH_KN` = 0.03 knots. The octant's noon sight on this ship is worth about three miles (`sights.py:116` to 127, 203 to 211). So the sight was weighed at next to nothing. The same weighing let the three bearings with their distances (10:30, 11:00, 11:30) drag the account only sideways onto each bearing's line, close under the mark; worked through by hand with weights of that order, the account ends within a mile of the noon line's "50° 02' N ... 5° 03' W" (reconstructed; the weights are my guesses). The source's own comment names this failure: "a weighing by that doubt would let a bad account outvote a good sight".

**(b) It was Ushant's light, ten hours later, that set the account right.**
- 57600 (21:00): "S by W by account, 49 miles. Helm ordered: steer S by W (190°)."
- 61020 (21:57): "A light right ahead, bearing S by W."
- 61200 (22:00): "The light on Ushant bore S by W, nine leagues by estimation." and "SSW by account, 44 miles. Helm ordered: steer SSW (204°)."

An hour's run from the 21:00 account is about 48° 53' N 5° 13' W; from there the light should bear about 165°, two points and a quarter on the larboard bow. It was right ahead. After the bearing the account is at about 48° 52' N 4° 57' W: **the bearing moved it about ten and a half miles to the eastward** (reconstructed; rounding in the log's miles and degrees allows half a mile either way). The book means to pass ten miles west of Ushant; she was steering for the light. The hourly re-shaping turned her 14° to starboard at 22:00 and she passed the light at "three leagues by estimation" at about 00:45. `TuningNotes.md` line 1393 says of the first noon's error "set right by the Lizard's bearings within the glass". The log does not bear that out: there was one bearing after noon, in the same tick, and the land was lost at 12:21.

**(c) The landfall under Ushant was five miles out, and the track at the Iroise was not the book's.**
- 79200 (03:00): "The light on Ushant bore NNE, four leagues by estimation." and "Shaped a course for the Passage de l'Iroise: E by S by account, 12 miles." The account is then about 48° 18' N 5° 12' W.
- 80220 (03:17): "Ushant bearing N, distant six miles." "Molène bearing ENE, distant five miles." The two bearings cross at about 48° 21½' N 5° 06' W, some five miles north-east of where the account had her (reconstructed). The distances by estimation of the light, taken all night, look about a quarter to a third too long. Both sightings are routine lines.
- 82800 (04:00): "Standing order 'the course for the Iroise' every hour: not carried out; the distance to ushant is 7 miles by account, not over 10 miles." The book's guard expects Ushant "ten miles off and more" on that leg. With the account now right and the Iroise's mark nine miles off to the south-east, the rule that would have re-shaped the course was held by its own guard at 04:00 and again at 05:00, and she ran on E by S from 03:00 to 05:14.
- 83520 (04:12): "Béniguet bearing E by N, steady and closing: distant four miles." 84960 (04:36): "La Helle bearing NE by N, distant three miles: a danger." 85440 (04:44): "The Black Rocks bearing SSE, distant three miles: a danger." 85500 to 86700 (04:45 to 05:05): five bearings "Béniguet bore NE by N / N by E / N by W / NW by N / NW, a mile by estimation".

She passed about a mile south of the mark the chart calls Béniguet, which lies 7.4 miles north of the Passage de l'Iroise's mark the book steers for. `TuningNotes.md` gives the closest she came to that mark as "three miles north by the truth". Whether the water a mile south of Béniguet is foul on the game's chart I cannot tell (section 10).

**(d) The second noon.** 111660 (12:01): the sight read four miles north of her. It did no harm: a bearing had been taken a minute before (111600), so by the same gate the sight was weighed and not adopted, and 'the mouth of the Goulet' fired on time at 112005. Here the gate did the right thing; at the first noon the wrong one. The model's note 19 (a lunar replacing a bearing-fixed account) is the third face of the same rule.

**(e) The master's day's work in the Goulet.** 113460 (13 Jun 12:31): "Mr Travers came on deck, the day's work done." By the source the master is below from the noon line for thirty minutes (`DAYS_WORK_MINUTES`). On this ship he is the captain, and those thirty minutes (12:01 to 12:31) are the Goulet from its mouth to the Mingan. Six bearings were worked onto the account in that time.

**(f) The chart's track (note 7).** Not in the log, but the cause is plain in the source (read only): `reckoning.py:285`, `TRACK_KEPT = 168`, commented "a week of hourly steps". A point is added at every step of the account (`reckoning.py:662`), and every bearing, cast and heave is a step. This book makes about 25 an hour in pilot water and goes on at anchor. Counting only the ticks with a bearing, a cast, a heave or a noon (362 in the session, a lower bound): the 169th step came at 11:45 on the 13th; by 13:05, anchored in the Bay, the kept track began at 04:00 that morning; by 15:10 at 07:50; at the end at 12:41. So the 81 minutes of the Goulet pushed the whole passage from Falmouth to off Ushant, some 18½ hours of sailing, off the chart.

### 6.6 The standing orders at work

**Fired most** (the dump's counts): 'pilot water' 186, 'the lead in pilot water' 140, 'tend the sheets' 77, 'bearings' 58, 'in the Bay' 55, 'trim on a shift' 37, 'trim to the course' 27, 'the course across' 12. Nineteen rules fired once and four twice.

**Never fired: 9 of 40.**

| Rule | Why not (LOG or reconstructed) |
|---|---|
| 'round the Manacles', 'across the Channel' | the account never came within two miles of 50° 00' N 4° 57' W: it stood still while she sailed over the point (6.5a). She held SSE until 14:00 and never made the corner off the Lizard |
| 'the Iroise' | the hourly rule turned her at 02:00 with the soundings "8 miles by account, not over 8 miles" (75600), a mile short of this rule's seven |
| 'bring to in the Iroise', 'the bottom of the Iroise', 'fill away after the cast', 'for Bertheaume' | she never came within a mile and a half of the Iroise's mark by account; so no deep-sea cast |
| 'the pilot in the road' | 91560: "the distance to the road of bertheaume is 4 miles by account, not under 4 miles" |
| 'the mark in the Bay' | the lead anchored her first |

Both of the passage's planned turning marks at sea were missed because the account was not where the ship was. The hourly rules and the fall-back 'past the Iroise' (87242) carried her. The book is safe by having a second rule behind every first, not by being accurate.

**Held** (`standing.held`, 76 lines, said once a watch per rule and reason): mostly rules asleep outside their place. The telling ones: 'in the road' 95942 "the heading is NE (45°), not west of north-east"; 97893 "the speed is 1 knots, not over 3 knots"; 'in the Bay' 124895 "the speed is 2 knots, not over 2 knots"; 'the lead in pilot water' eight times "held; the last firing's work is still waiting its turn" while all hands were at the anchor.

**Conflicts** (`standing.conflict`, 6): 16320 'the pilot boards' against 'the pilot aboard' "on the fore topsail" (a true one: the book takes the sail in and sets it again within the minute); 17612 'the pilot put off' against 'clear of the road' "on the helm" (true, though the later one that "stands" is refused in the next line, she being hove to); and four that are not conflicts at all: 116489, 123004, 123096, 139604, each "give contrary orders on the ship", between sending the boat, selling the tin and coming to an anchor.

**Fighting for hands.** 177 `evolution.waiting` (59 notable) and 103 `evolution.short_handed`, nearly all the hourly trim: "Bracing the yards: not hands enough for all at once; the watch takes the sails in turn." 45 times. The lead lost its turn once where it mattered: 113401 (13 Jun 12:30, between the Mingan and the Fillettes) "Not hands enough on deck to heave lead; the watch is bracing the fore topsail yard and the fore topgallant yard and trimming the foresail."; that cast came 2½ minutes late.

**The two anchoring rules read the world, not the lead.** 'in the Bay' is "at a sounding, if ... the depth of water is under 12 fathoms and the speed is over 2 knots then come to an anchor". It fired on 115285 "By the mark thirteen; mud." and went on passing at casts of 13½ and 14 fathoms (132093, 132693). 'in the road' ("under 13 fathoms") fired on "And a quarter thirteen" (96147). `the depth of water` is "the chart's depth where she is (the truth's chart, which the lead finds and the master does not see)" (primer 10's table; `freesail/api/readings.py:557`): the world's own number at her true place, at the datum, without the tide. The cast is only the occasion. And "the speed" is her way through the water, so at anchor in a two-knot stream the guard meant to say "she has way on" is true: 54 refused anchorings. `TuningNotes.md` knows of "six"; this run has 28 inside the 36 hours.

**The Goulet as a model of a careful approach.** From under way (11:44) to the anchor (13:05), 81 minutes: 17 casts, 20 bearing lines at 17 times, seven courses shaped, three of them saying what lay near the line ("the line passes the Mingan and the Fillettes within a mile", 112674). What in the book made it safe:
1. She did not take the Goulet when she arrived. She anchored outside in Bertheaume road on the ebb and waited 3½ hours for the turn, by daylight ('the flood': "if the daylight is day").
2. The account was held by a bearing every five minutes from fourteen miles off, with a named mark never more than three miles away.
3. The lead went every five minutes within six miles of the Goulet's middle.
4. The track was six points pricked beforehand in deep water on one side of the channel, legs of a mile or two, each taken when within 0.4 mile.
5. She was re-trimmed after every turn, so she kept her way and her steerage.
6. She anchored on a cast, near a mark, with way on, with a second rule behind it.
7. Every rule is fenced to its place by a distance.

Its limits, which matter when it is held up against a model with no book. The points were pricked by an author who can see the world, and moved after trials: `TuningNotes.md` line 1393 says an earlier point under Petit Minou "put her on the grid's shore ... four times" after another change "moved her track a cable". 112599 (12:16) "And a quarter twelve; rock and mud." between a no-bottom cast and 17½ fathoms, seven cables from Petit Minou, is that shelf. Nothing in the book answers a shoaling cast. She ran the Goulet under all plain sail (fore topgallant set at 12:03) at about seven knots over the ground (4.9 miles from the first point to the last in 40 minutes). The lookout's last word on the Mingan is "steady and closing: distant two miles" (112200, 12:10); her passing it at about five cables is not said. And the anchoring rules look at the world's depth.

### 6.7 Other sail

Eight vessels were seen: two Falmouth pilot cutters, five strangers, the Brest cutter. Of the scenario's dozen ships five were raised, all on the 12th; two were made out as to rig, none as to colours, none came within hail. Nothing but the pilot cutter was seen in the Iroise or off the Goulet, though the chart's own note calls the road of Bertheaume "the blockading squadrons' station".

| Vessel | Sighted (LOG) | After | Lost |
|---|---|---|---|
| Falmouth cutter, the first | 15600, 09:20: "... on the larboard bow, bearing S, distant two miles." | 09:22 made out (within 1½ miles); 09:30 hail (4 cables); 09:32 pilot aboard (2 cables) | one of 19080 (10:18) "The cutter on the starboard quarter is out of sight." and 21060 (10:51) "The sail right astern is out of sight." |
| Falmouth cutter, the second | 17640, 09:54: "... abeam to starboard, bearing NW by N, distant eight cables." | 10:04 hail; 10:07 pilot leaves | the other of those two |
| Sail A | 17580, 09:53: "... larboard bow, bearing SE by S, distant three leagues." | never made out | probably 24360 (11:46) "The sail abeam to larboard is out of sight." |
| Sail B | 19680, 10:28: "... starboard bow, bearing S, distant four leagues." | 21960 (11:06): "The sail on the starboard bow is a schooner, standing to the northward (N), under plain sail." | 25920 (12:12) "The sail right astern is out of sight." |
| Sail C | 23340, 11:29: "... right ahead, bearing SSE, distant four leagues." | never made out | probably 41880 (16:38) "... starboard quarter ..." |
| Sail D, the gate's | 28140, 12:49: "... larboard bow, bearing SE by E, distant three leagues." | never made out | probably 40560 (16:16) "... larboard quarter ..." |
| Sail E | 34200, 14:30: "... larboard bow, bearing S, distant three leagues." | 47460 (18:11): "The sail right ahead is a ship, standing to the south-westward (SSW), under plain sail." | 54240 (20:04), a minute after sunset |
| Brest cutter | 88080, 05:28: "... larboard bow, bearing E, distant two leagues." | 05:56 a cutter (4 miles); 06:14 colours (2); 06:16 the pilot's (1½); 06:23 hail (4 cables); 06:26 aboard (2 cables) | 106320 (10:32) "The sail on the starboard bow is out of sight." |

(The distances in brackets are primer 15's and the source's thresholds for each kind of line, not words of the log. The pairing of A, C and D with their losses is mine, by where each should have borne.)

**The model's "fixed distance" cannot be tested on the strangers here**: the log gives each sail one distance, at the hail, and the owner never asked `the strangers`. For the two pilot cutters the thresholds show a steady closing: Brest two leagues, then within four miles after 28 minutes, two miles after 18 more, a mile and a half, four cables, two cables. Sail B closed eight miles in 38 minutes on an opposite course and was lost astern an hour later, as a real ship would be. So in this session nothing held its distance. The Falmouth cutter's "eight cables" at 09:54 is the same figure the model reports at Roscoff, but here it is simply where the outer road lay from the ship when the second cutter was launched.

**The two world orders.** 25200 (12 Jun 12:00): "World order (the scenario): a waypoint appended to the old high over Biscay." 90000 (13 Jun 06:00): "World order (the scenario): a letter from the agent of the owners left at Brest." Both "done" in the dump; the second is the letter of 6.2.

### 6.8 The port business

**Falmouth.** The bargain is struck the instant the anchor is let go (57), from the price list aboard at the start. Boat: away 396 (05:06), landed 1716 (05:28, 22 minutes' pull), three hours at the quay, shoved off 12516 (08:28), alongside 14249 (08:57, 29 minutes). 3 h 51 m from "away" to "alongside". 57: "The manifest written up by the mate: 40 tons of tin bought at Falmouth.", four hours before the tin is aboard.

**Brest, the prices.** 116377 (13:19) 'the agent'; 116697 (13:24) "The long-boat away for the quay below the castle of Brest with Mr Ray, for the prices and what news there is."; landed 119222 (14:07, 42 minutes); shoved off 120122 (14:22, a quarter of an hour ashore); alongside 123004 (15:10, 48 minutes). 1 h 45 m. "Mr Ray came aboard from the boat." "The mate's list of the prices at Brest is aboard: wine £35, brandy £110, canvas £40, salt £12 a ton, and the rest."

**Brest, the sale.** 123004 (15:10), the tick the boat came alongside, some 2.8 miles from the quay (42 minutes at the boat's four knots): "Sold 40 tons of tin at Brest at £270 a ton, £10800 taken; the boat lands it. The purse: £11995." The money is in hand before the tin leaves the hold. "The manifest written up by the mate: 40 tons of tin sold at Brest." in the same tick. Then away 123364 (15:16) "with the goods sold"; landed 125891 (15:58); three hours at the quay; shoved off 136691 (18:58); alongside 139604 (19:46). **4 h 30 m 40 s.** There is no line for the tin leaving the ship: the purchase has "hoisted in and struck down", the sale has nothing, and the next word on the hold is the refusal at 139604, "The hold has 0 tons of tin, not 40".

**Which figure for the purse.** £6,000 at the start; £1,200 after the purchase (57); £1,195 after the pilotage (18420); £11,995 after the sale (123004); "The purse: £11995." (139369, 139422). The sale moves it £10,800. Nothing in the log moves it £6,000.

**The prices and the people.** The prices reading is quoted in section 3. It shows the Brest list alone, dated; the Falmouth list the ship began with is not in it. The 40 tons went at one price though the market's rule takes a hundredth off for each ton sold. The people are quoted in section 3: four at sea, five with the pilot.

### 6.9 Log noise

- `wind.shift` 4 (12 Jun 17:06, 20:24, 21:24; 13 Jun 09:39). `ship.aback` 0. `sail.backed` 10, every one a sail backed on purpose (casting at 09:15 to 09:19 and 11:34 to 11:36, heaving to at 09:53, anchoring at 13:06), and every one notable. The breeze was a steady ten to fourteen knots, so this session does not show the m5c wind-shift flood.
- The trigger behind the trim is noisier than the log line: 'trim on a shift' fired 37 times against 4 logged shifts, four of them between 17:06 and 17:35 on the 12th, each ending "Braced two yards to the wind; 58° to 60° from square." or within a degree of it.
- **Busiest hour**: 13 June 12:00 to 12:59, the Goulet: 217 lines, 47 notable. Busiest ten minutes: 63 lines from 113343 (12:29). Next: 12 June 09:00 to 09:59, 127 lines, 34 notable. Tick 0 alone has 89 lines.
- **At the notable level** (417 lines):

| Stretch | Notable | Of which |
|---|---|---|
| Channel crossing, 12 Jun 14:00 to 22:00 | 61 | 55 are the trim's three lines; 6 are events (3 wind shifts, 2 sightings, sunset) |
| Ushant night, 22:00 to 04:00 | 40 | 39 trim, 1 sunrise |
| At anchor in Bertheaume road, 07:47 to 11:36 | 47 | 38 casts of the lead |
| The Goulet, 11:36 to 13:05 | 66 | 19 orders accepted (ten of them trims), 17 casts, 19 lines of the trim's waiting and bracing, 11 events |
| At anchor in the Bay, 13:05 to 19:48 | 88 | 78 casts of the lead |

  Over the whole passage 168 notable lines are trim chatter and 116 are casts at anchor: 284 of 417. "Braced two yards to the wind; 58° to 60° from square." is a notable line 29 times in the same words.
- What is routine is sometimes the news: "Ushant bearing N, distant six miles." (80220) and "Hove the log: no way." (18038) are routine lines.
- After the anchor went down at Bertheaume (07:47 on the 13th) 924 lines, a third of the whole log, were written with the ship at anchor.

So the passage reads cleanly at the notable level only in its first morning. From noon on the 12th the events are a small part of a steady beat, and in the Bay the beat is all there is.

### 6.10 What reads wrong to a sailor, missing numbers, contradictions

1. **The anchor's depth.** 115534 (13:05) "let go in twelve fathoms and a half"; 116377 (13:19) "Brought up by the best bower in six fathoms and a half, sixty-three fathoms of cable"; 116489 (13:21) "And a quarter twelve; mud."; 11½ to 14¼ fathoms for the next six hours. Sixty-three fathoms is five times twelve and a half, so the cable agrees with the let-go and the lead, and the brought-up figure stands alone. At Bertheaume the two lines agree. `TuningNotes.md` records "brought up at 116377 in six and a half" without remark, so the reference run has it too. Likely cause, from the source (read only): once a minute the anchor's depth is re-read from the chart at `origin.advanced(ground_x, ground_y)` (`freesail/core/world.py:578` to 584), one step from the scenario's origin at the mean latitude, while the ship's own place is advanced tick by tick at the latitude she is in (`world.py:681`; `freesail/world/geo.py:72`). For a track that goes south and then east the two differ in longitude. I make it about a cable and a quarter east at Bertheaume and about three cables east in the Bay (reconstructed from an approximate track), and the book says the flats there "rise from eleven fathoms to two in half a mile". The same lines end `max(0.0, ...)`, and a depth under a quarter of a fathom is worded "no water" (`freesail/world/chart.py:191`): the Harpy's "brought up in no water" in the model's notes.
2. **Numbers in two styles in one event.** "nine fathoms and a half", "twelve fathoms and a half", but "13 fathoms and a half" (96475, 97567). The depth's words stop at twelve (`chart.py:176` to 192); the cable's ("sixty-nine fathoms") come from another function.
3. **"the speed is 1 knots"** (97893, 126093).
4. **"taken aback"** for sails backed by order: "Fore topsail taken aback." (17615) as she heaves to with the fore topsail to the mast. All ten are of this kind.
5. **A ship's words on a schooner.** 15347: "Hoist away the topsails! Brace up the after yards for the starboard tack, the head yards abox." 15917: "... set the spanker." 96148, 115286: "Haul taut! In studding sails, royals and topgallants; up courses." 96542: "... brail up the spanker." She has yards on the fore only, a gaff mainsail and no royals.
6. **The fore topsail taken in under a standing topgallant.** 91499 (06:24) "Took in the fore topsail; hanging in the gear."; no line takes in the fore topgallant, and the trims at 06:44 and 07:33 still brace "the fore topsail yard and the fore topgallant yard". She stood so to the anchor at 07:42.
7. **Two bearings of one mark at one second disagree by a point**, eight times, for instance 93600 (07:00): "St Matthew's Point bore NNW" and "St Matthew's Point bore N by W".
8. **The nearest land changes at anchor.** In the Bay the five-minute bearing is "Brest bore N by W, two miles by estimation." until 16:35 and "Portzic bore WNW, three miles by estimation." from 16:40 (128400). 130260 (17:11): "St Matthew's Point bearing W, distant four leagues." is newly sighted from the same anchor.
9. **The boat hoisted in twice in one tick.** "The long-boat alongside from the shore and hoisted in." and "The long-boat hoisted in." (14249, 123004, 139604).
10. **A man sent for stays.** Mr Paul, sent for to the cabin at 17:13, is "in the cabin" at 19:47.
11. **A file path in the ship's log.** "... a model's door seats one first (docs/agents/Harness.md) ..." (130160).

The pilot's wording (6.2), "A sail in sight: not in sight." (6.3), "And a quarter twenty" (6.4), "Course made good since the departure S, a mile" and the day's work in the Goulet (6.5), the four false conflicts (6.6) and the manifest written before the goods move (6.8) belong in this list too.

## 7. The model as an officer

Does not apply: the owner played alone with the scenario's book.

## 8. Cross-check against the notes

**The owner's items.**

| Note | Evidence in this session | Verdict |
|---|---|---|
| 1. Pilot boarded while under way | 16320 (12 Jun 09:32): boarded 5¼ minutes after "Under way", before "Took in the fore topsail" (16338). 91560 (13 Jun 06:26): boarded at about 4½ knots, steering E by N. Left hove to (18420), "Hove the log: no way." | SUPPORTS. Adds: the rule in the source is two cables and six knots over the ground, not hove to; no distance is ever logged at the transfer; the inward pilot never leaves; the outward pilot is hailed as an inward one |
| 2. "The well" still says there is no well | 30358: "The well: the ship has no well to sound yet; that reading comes with the world." | SUPPORTS, exact words. `TuningNotes.md` speaks of a grounded ship "stove and the well rising", so the flooding has words but no reading |
| 3. Price list should hold every port visited | 130550: `the prices` gives "at Brest (13 June, Afternoon watch (15:10))" only; the Falmouth list she started with is gone from the reading | SUPPORTS |
| 4. Primer wants a clean-up | Primer 15 and the scenario's header promise the Iroise cast that seed 7 never makes; primer 14 does not say when an inward pilot leaves; primer 10 says the noon latitude "replaces" the reckoned one, which it did not at 25200 | ADDS three places |
| 5. The book makes a clean passage | Agrees with the gate to the tick; no grounding; £5,995 up. But: 9 of 40 rules never fired; both turning marks at sea were missed; the account ran 8 to 10½ miles out from 10:30 to 22:00 on the 12th; Ushant's light came up right ahead (61020); she passed a mile from Béniguet (85500 to 86700); the anchoring rules read the world's depth; the Goulet's points were moved after four groundings in tuning (`TuningNotes.md` line 1393), and the book's own comments record other trials ("which anchored her twice", "the pilot was carried to the Iroise") | ADDS NUANCE. Clean in outcome at this seed. The book was fitted by trial to a replay that never varies; that is a different thing from a plan made beforehand that holds |
| 6. Soundings read "NaN fm ..." on the chart | Not in the log. `client/map.js:450` divides by `U.FATHOM`, which `client/units.js` does not define | SUPPORTS, with the cause; every depth is affected, and m5c-b has the same line |
| 7. The chart's track is cleaned up aggressively | Not in the log. `TRACK_KEPT = 168` counts steps of the account; by 13:05 on the 13th the track began at 04:00 that morning, at the end at 12:41 | SUPPORTS, with the cause |
| 8. Anchor information in the state window | Cannot be seen (browser). The log's own anchor line carried a wrong depth (116377). He never typed `the anchor` or `the cable` | cannot be seen; adds a caution |
| 9. Pilot automatic; wants hailing and signalling | No input from tick 0 to 30145; no order to call, accept or refuse exists | SUPPORTS |
| 15. General allowance of authority | 130160 to 130176: four `You may ...` tried with no officer seated, all refused | cannot be judged here; shows he was trying the grammar on this voyage |
| 16. "keep" orders | 'tend the sheets' refused 29 times and 'trim on a shift' 9 times "She is at anchor; ... must wait till she weighs."; 10 firings of 'tend the sheets' under way found every sheet to "stand as trimmed" | SUPPORTS the model's rider that such an order should pause itself at anchor |
| 17, 18. Aback alarms and wind-shift lines | `ship.aback` 0; `wind.shift` 4 in 39 hours of a steady breeze | CANNOT BE SEEN here. Adds: the trigger 'when the true wind veers 1 point' fired 37 times against those 4 lines |
| 19. Reckoning close to visible land | 80220: Ushant "distant six miles" raised about five miles from where the account had her; 82800: the course rule held by its own guard; a mile from Béniguet with one "steady and closing" line (83520) and no urgent line. And the rule that decides when a sight replaces the account | ADDS NUANCE, and a mechanism (6.5a, d) |
| 24. Nearest land, features by their parts | Each five-minute bearing names one mark, a point: "Béniguet bore N by E, a mile by estimation." (85800) for an island | ADDS slightly |
| 10 to 14, 20 to 23, 25, and the local notes | no model, no harness | do not apply |

**The model's comments and additions.**

| Claim | Evidence here | Verdict |
|---|---|---|
| "the 'two cables' rule is applied on boarding but not on leaving" | no distance is logged at either | CANNOT BE SEEN |
| "'Send for the carpenter' brings him aft with nothing to say" | 130234 to 130319: the boatswain came aft and to the cabin; `Ask the boatswain`, `The boatswain`, `Send the boatswain below` all refused | SUPPORTS |
| A port's market should show which goods it trades | 130550: the Brest list has eleven goods, English and French | ADDS NUANCE: once the boat has been, the list does show them |
| "A worse figure shouldn't replace a better one" | 25200: a good noon latitude failed to replace an account eight miles out; 111660: a sight four miles out was rightly not adopted | ADDS the other half: the rule goes by miles run by account, not by comparing the two doubts |
| "Lead standing orders fight for hands" | 113401 once in the Goulet; eight "still waiting its turn" at the two anchorings | SUPPORTS, mildly |
| "no bottom at twenty fathoms" confuses | three such casts in the Goulet, and "And a quarter twenty" at 113553 | SUPPORTS, adds the contradiction |
| "brought up in no water" on the Harpy | 116377 "in six fathoms and a half" against 12½ and 12¼ | SUPPORTS by its twin, with a likely cause |
| The reckoning advanced at anchor | "9 miles by account" to the road of Bertheaume at both 126000 and 133200; but a bearing every five minutes would mask it | CANNOT BE SEEN |
| "Each boat trip carries one bargain and takes about 4½ hours" | 123364 to 139604: 4 h 30 m 40 s for the sale; 3 h 51 m at Falmouth | SUPPORTS |
| "Other ships keep a fixed distance" | each stranger has one distance; both cutters closed steadily | NOT REPRODUCED here; untestable for the strangers |
| "Number words above twelve fail" (orders) | "buy forty tons of tin" and "sell forty tons of tin" were taken (57, 123004) | ADDS NUANCE: forty parses. The depth's output words do stop at twelve |
| The schooner's `get under way` does not cast her | cast and under way in eight minutes both times (15497 to 16005; 110180 to 110675), wind across the tide | NOT REPRODUCED here |
| "'Trim sails' acts before the helm has swung" | the book works round it with 'at steady on the course then trim sails', 27 firings | SUPPORTS as design evidence |
| The contrary-orders warning fires on ordinary sequences | four `standing.conflict` lines of "contrary orders on the ship" between anchoring, the boat and the sale | SUPPORTS, in the book's own detector |
| Worked well: bearings once the land came up; the noon latitude | bearings held the account in pilot water. The first noon latitude was good and unused; the second was four miles out | SUPPORTS the first; ADDS NUANCE to the second |

## 9. New findings not in the notes

Ranked by weight. This run is the gate's reference run to the line (6.1), so every item here but 7 is a property of the build and the book at seed 7, not an accident of this play.

1. **A sight is weighed or adopted by miles run by account, and a log hove while hove to stops the account.** 18038 "Hove the log: no way."; 25200 noon 49° 54' N observed, 50° 02' N reckoned, and in the same tick "the distance to falmouth is 8 miles by account"; 28800 no course shaped; 32400 "97 miles". The account was 8 to 10½ miles out for ten hours (9.6 at noon by the gate; the rest reconstructed) in clear weather with a good noon sight in hand. Cause in the source: `reckoning.py:675` to 727 (`FIX_RUN_NM`) and the stale read (6.5a). The book could cure the read (the log hove again once she has gathered way after filling, or every glass while the land is in sight); the rule itself wants the two doubts compared.
2. **Ushant's light was raised right ahead and the land five miles from the account.** 61020 "A light right ahead, bearing S by W."; 61200 the account moved about 10½ miles east; 80220 Ushant "distant six miles"; 82800 the course rule held by its own guard; 85500 to 86700 Béniguet "a mile by estimation". The gate's account says only "Ushant's light at night". `TuningNotes.md` says the first noon's error was "set right ... within the glass"; the log says otherwise.
3. **The anchor's depth is read from another place.** 116377 "six fathoms and a half" against 12½ at the let-go and 12¼ by the lead two minutes after (6.10 item 1). The same code prints "no water". It may also feed the anchor's holding; I did not follow it.
4. **The book's anchoring rules read the world's depth and her way through the water.** 115285: anchored on "By the mark thirteen" under a rule that says "under 12 fathoms"; then 54 refused anchorings at anchor (6.6). A captain's book that consults "the truth's chart, which ... the master does not see" is not the test of the lead that it looks like.
5. **Nine of forty rules never fired**, among them both turning marks at sea and the deep-sea cast that the scenario's header and primer 15 describe (6.6).
6. **The inward pilot never leaves and is never paid**; the outward one is hailed as "a pilot for Falmouth" with the way in; a second cutter appears at eight cables; the letter left at Brest at 06:00 is aboard at 06:26 from a cutter already at sea (6.2).
7. **On the schooner the master is the captain and nothing says so.** `send for the master` refused twice (130224, 139685); nine tries to leave the cabin (139648 to 139699); 22 of the owner's 47 lines refused, 14 of them for want of a word.
8. **The log at anchor.** 924 lines, a third of the log, after 07:47 on the 13th; 116 notable casts at anchor; and at sea the same three notable trim lines every hour, while "Ushant bearing N, distant six miles." is routine (6.9).
9. **The master's day's work takes him below through the Goulet** (113460), and he is the captain (6.5e).
10. **Four false "contrary orders on the ship"** between the boat, the sale and the anchor (6.6).
11. **The purse.** The gate's item 1 says it moves by £6,000; it moves by £10,800 at the sale and £5,995 over the voyage. The sale has no line for the tin leaving, and the money comes before the goods go (6.8).
12. **Wording**: a ship's evolution words on a schooner; "taken aback" for sails backed by order; a topsail taken in under a standing topgallant; "13 fathoms" beside "twelve fathoms"; "1 knots"; "And a quarter twenty" from a twenty-fathom lead; "took charge of her" of a pilot who does not con (6.10, 6.2).
13. **The run is the reference run to the line** (2,460 lines + his 7 + the server's 1 at or before tick 129,600): a reading typed at the prompt changes nothing, and the passage is the same at any compression. Useful to know when comparing saves.

## 10. Could not determine

- **The truth.** The save is inputs only; no line of the log gives her true place. The errors in 6.5 are reconstructed from the log's "by account" figures, the bearings, and the marks' charted positions, with headings taken as true (the lookout's opening bearings of Pendennis, St Anthony and Falmouth fit true bearings). The 10½ miles at 22:00 rests on two helm lines and the mark's charted place and is the firmest; the five miles at 03:17 rests on two bearings quantized to a point.
- **Whether the water a mile south of the chart's Béniguet is foul** on the game's depth grid, and so whether 04:45 to 05:05 was a near miss or only a short cut. No lead was going there (the lead's rule begins six miles from the Goulet).
- **The cause of "six fathoms and a half"** for certain. The two ways of turning metres into longitude are in the source; my figure for the offset is arithmetic on a reconstructed track, and I did not load the chart to read the depth there.
- **Her speed and the cutter's distance when each pilot boarded.** Neither is logged.
- **Which of the scenario's dozen ships** the five sails were, and which loss line belongs to which sail.
- **Whether the estimated distances of Ushant's light were long by a quarter or more** all night, as the 03:17 cross suggests. The source draws the eye's error once for a sighting episode (`freesail/world/lookout.py:114`, 0.15 one sigma); a quarter to a third would be an unlucky draw.
- **What the owner saw**: the chart's labels and track, the state pane, the compression he used, and the real time the session took. Notes 6, 7 and 8 are judged from the source and the log, not from the screen.
- **Whether the pilot staying aboard is meant.** Primer 14 is silent; the source fetches him only outward bound.
- **Why the nearest land at anchor changed from Brest to Portzic at 16:40**, and why St Matthew's Point was newly sighted at 17:11.
