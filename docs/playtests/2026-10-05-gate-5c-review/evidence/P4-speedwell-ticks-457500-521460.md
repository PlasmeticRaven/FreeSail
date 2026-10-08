# P4. *Speedwell*, session `4-schooner-plymouth-opus`, ticks 457500 to 521460

**How to read the evidence.** Three kinds of statement are kept apart:

- **[log]** a line of the ship's log, the inputs file or the transcript. Fact.
- **[officer]** / **[captain]** something the model or the owner said. Claim or opinion. Tool results are not stored in a save, so anything the officer says it "read" is its own report of a reading.
- **[source]** something I read in the m5c source or data files (read-only) to explain a log line. I did not run anything. The lead may want these confirmed against the save.

Ship's time = 12:05:00 on 26 June plus (tick − 457500) seconds.

---

## 1. Slice identity

| | |
|---|---|
| Session | `4-schooner-plymouth-opus`, part 5 of 6 |
| Ticks | 457500 to 521460 (63,960 s, 17 h 46 min) |
| Ship's time | 26 June 1805 12:05:00 to 27 June 05:51:00 |
| Ship | merchant topsail schooner *Speedwell*, American colours, complement 40; cargo 40 t coal, 20 t pilchards, 16 t brandy; purse £31 |
| Station | officer of the watch = the mate, "Mr Ray" |
| Model, door | Opus 5.5 through MCP; third seating (since 343551, 25 June 04:25) |
| Deck | the officer's since 398710 (25 June 19:45) and throughout the slice |
| Build | m5c-b |
| Volume | 1,001 log events (128 notable, 1 urgent); 141 transcript entries; 44 captain's inputs |

The officer's calls in the slice: 46 `submit_order`, 50 stand-bys (45 in turn, 5 "out of turn"), 37 spoken lines, 4 `library`, 2 `answer`, 1 `journal`, 1 `state`, no `readings`, no `read_log`.

The captain's 44 inputs: 23 `tell`, 2 `ask`, 2 `you may`, 8 trims, 5 bearings (1 refused), 2 standing-order attempts (1 refused), `ease the bowlines` (refused), `heave the deep sea lead`.

---

## 2. What happened

| Tick | Time | Event |
|---|---|---|
| 457500 | 26 Jun 12:05 | Noon, no sight. "Latitude by account 49° 13' N ... Longitude by account 4° 54' W." She steers NW by W (309°), the course shaped for St Mary's at 10:52. Wind SW by S, 3 knots; glass 30.41. |
| 457584 | 12:06 | Captain gives leave to set all she will bear. Officer: the light sails are bent already. |
| 458034 to 470725 | 12:13 to 15:45 | The captain trims by hand six times as the wind draws aft (apparent wind 53° to 85°). The officer's `trim` standing order fires once (12:56). |
| 461645 to 462398 | 13:14 to 13:26 | Officer sets the ringtail (after one "rig it out first" refusal) and the water sail. |
| 463986 | 13:53 | Officer queries the yard angle. Captain answers with `Trim the yards` (13:54). |
| 467644 to 468698 | 14:54 to 15:11 | Stuns'l boom rigged out. The officer stands by for "a notable event" that never comes; the captain tells him at 15:07; stuns'l set 15:11. |
| 469859 | 15:30 | At the captain's request the officer enters `steady trim`: "at steady on the course then trim sails". |
| 478078 to 478201 | 17:47 to 17:50 | The `light sails` standing order: five wordings refused to the officer, four library searches, one refused to the captain, then the captain finds "is above". |
| 478818 | 18:00 | Officer enters `studding` (after an apostrophe refusal). Log: five knots. |
| 480648 | 18:30 | Journal entry at the captain's prompting ("just in case"). |
| 483601 to 483795 | 19:20 to 19:23 | `light sails` takes in the ringtail and the water sail, mean wind above 10 knots. |
| 484222 | 19:30 | Plan agreed: shorten about midnight to close the islands at first light. |
| 491220 | 21:27 | "The sky threatening, small inky clouds." "Rain set in." |
| 491474 | 21:31 | Officer takes in the stuns'l and the gaff topsail early, on the sky. |
| 493038 | 21:57:18 | **Urgent.** "Taken aback: the sails pressed against the masts and she lost her way." Officer in 5 s: `keep her full and by`, `take in the fore topgallant`. |
| 493372 to 494012 | 22:02 to 22:13 | Captain: steer the course, not full and by. Officer steers 309, takes in the flying jib, then 318 because the topsail shook. Log 6¼ knots. |
| 496809 to 497002 | 23:00 to 23:03 | The danger list shows the Wolf NNE ten miles by account. Officer tacks (139 s) and heaves to on the starboard tack. |
| 497021 to 498051 | 23:03 to 23:20 | Captain: `heave the deep sea lead`. "Fifty fathoms; fine grey sand with black specks." |
| 498957 to 502640 | 23:35 to 00:37 | Three squalls: 17, 20 and 19 knots. Log at midnight, hove to: 3¼ knots. |
| 503495 | 00:51 | Captain asks whether she is reaching too far south. Officer answers from the account. |
| 505803 to 506079 | 01:30 to 01:34 | `fill away`, `tack ship` (190 s), `steer 309`. Three nudges. Trim orders resumed. |
| 506189 | 01:36 | Stand by "a landfall" (runs 1 h 52 min). Log at 02:00: seven knots; sky clear. |
| 512940 | 03:29 | "A light right ahead, bearing NW." Officer refused a bearing; captain takes it: "St Agnes light bore NW, five leagues by estimation." Two allowances. Account corrected. |
| 514800 | 04:00 | Sunrise; "The sky hazy."; "The land is out of sight." Officer resumes `approach lead`, sets the flying jib and fore topgallant. Log 4½ knots. |
| 515521 to 521009 | 04:12 to 05:43 | Ten casts, all "No bottom at twenty fathoms." |
| 516688 to 517154 | 04:31 to 04:39 | Danger list against the captain's chart. Officer steers 315, then 310. The captain's Thames-barge word lands one second before a stand-by. |
| 519118 to 519127 | 05:11 to 05:12 | Officer ends his own stand-by, answers that word, shortens sail: "the pilot gig is standing out towards us!" Nothing in the log says so yet. |
| 520680 | 05:38 | "Sail ho! A gig pulling off from the land ... bearing WNW, distant two miles." "Peninnis Head bearing NW by W, distant four miles." Bearings; officer steers 292 for the gig. |
| 520860 | 05:41 | Made out: "the St Mary's pilots' gig ... British colours, the red ensign." |
| 521280 | 05:48 | "The gig hailed: a pilot for St Mary's; shorten sail and he will come aboard." Officer belays the trims and heaves to (hove to 05:49). |
| 521303 to 521423 | 05:48 to 05:50 | Lookout and bearing still give the gig "two miles". Officer proposes going to her; captain: "stay hove to". |
| 521460 | 05:51 | "The pilot, Mr Ellis of St Mary's, came aboard from the gig and took charge of her". |

---

## 3. The deck and the captain's words

### The deck

Not given or taken in the slice. The officer holds it throughout. At 521460 the log says the pilot "took charge of her"; the deck stays the officer's.

### Allowances (`agent.deck`)

| Tick | Time | Words | Used? |
|---|---|---|---|
| 512951 | 27 Jun 03:29 | "The officer of the watch may take a bearing of (the light), by the captain's word for the watch." | Not on the light, which was lost at 04:00 |
| 512955 | 03:29 | "...may take a bearing of (the land), by the captain's word for the watch." | Yes: 520694 (05:38), "By the officer of the watch: taking a bearing of peninnis head." |

- [source] An allowance is keyed by the verb alone (`agent.py` lines 153 to 161), so the first already covered every bearing. The bracketed object is only the captain's words kept.
- Earlier grants were still honoured: `steer` six times, `keep her full and by` once, `tack ship` twice, `heave to` twice, `fill away` once. [log] All five were given on 21 June (ticks 63, 80, 92, 96, 43096), two stand-downs and two re-seatings earlier. "For the watch" in the log's words is not a limit in practice.
- [log] No bearing had been allowed to the officer at any time before 03:29 on the 27th.

### Leave given by `tell` only

- 457584 (12:06) [captain]: "You absolutely have my leave to set as many sails as she'll bear once we're off the wind. You may ensure they're bent and ready." No order needed; sail handling is the officer's.
- 491530 (21:32) [captain]: "Understood, you have permission to keep her safe as necessary. If I see a refusal I'll allow it ASAP." This is the general authority of owner's note 15, said in words because no order gives it.

### Captain's lines that carry intent, design thinking or feedback

- 468473 (15:07): "Stuns'l boom rigged out, no notable event dropped I think." He is watching the event stream and sees why the officer is stuck.
- 469856 (15:30): "please enter a standing order under your name to trim the sails at steady on the course, so you may belay and resume it at your pleasure. I think it would be useful, so that when you enter a course and stand by you get a trimmed end result."
- 478074 (17:47): "if the wind breaks 10 knots in more than a gust, I'd bring in the watersail and ringtail. The stuns'l can take a bit more, but not much."
- 478205 (17:50): "GOT IT!" (the standing-order grammar).
- 480631 (18:30): "Go ahead and journal if you please, no handover necessary, just in case." Insurance against a lost session.
- 493363 (22:02): "I wouldn't trust full and by here, just keep her on our course and adjust as necessary."
- 496854 (23:00): "Wise, I'd say. Our wide reckoning leaves it uncertain, so it's the safer course of action until we get a landfall or light fix."
- 516902 (04:35): "I don't see Gilstone or the Spanish Ledge by those names on my chart ... I see the Bishop's Ridge, the Old Wreck, St. Agnes and the light, the Nun Deeps, and the Crim".
- 517005 (04:36): "Ah, I see unnamed danger markers on my map which are likely what you're referencing."
- 517153 (04:39): "we'll probably want to try and sail in as the Thames barges do, topsail only and enough up front to keep steerage way."
- 521384 (05:49): "all other ships are very simple polar simulations with basic rules as I understand it now, so strangeness is expected. We're still basically on the very first test version for the whole port, pilot, and navigation systems."
- 521419 (05:50): "I say we stay hove to for now and wait for the pilot to board." Right, 41 seconds before the pilot boarded.

### Done by the captain's hand

- **Because the officer could not:** the first bearing of the light (512946, three seconds after the officer's refusal); the `light sails` standing order (478201, after the officer's five refused wordings).
- **Because the officer did not:** eight trims (458034, 462201, 464046, 466638, 469042, 470725, 493056, 514833); the deep-sea lead (497021); bearings of Peninnis Head, Peninnis mill and the gig (520689, 520752, 521310).

---

## 4. Orders refused

76 in the slice: 75 `order.rejected` and 1 `agent.refused`. 64 of the 75 are standing orders rejecting themselves.

| # | Tick, time | By | Order | Refusal's words | Class | What worked |
|---|---|---|---|---|---|---|
| 1 | 461645, 13:14 | officer | `set the ringtail` | "The ringtail boom is rigged in; rig it out first." | (d), borderline (a): a sailor's "set the ringtail" includes the boom | `rig out the ringtail boom`, then `set the ringtail` (461952) |
| 2 | 467642, 14:54 | officer | `set the larboard fore topmast studdingsail` | "...studdingsail boom is rigged in; rig it out first." | (d), same | `rig out the ... boom`, then set (468477) |
| 3 | 478078 to 478091, 17:47 to 17:48 | officer, 5 times in 13 s | `standing order "light sails": every 10 minutes if the mean wind above 10 knots then ...`; also "above 10", "speed above 10 knots", "the wind above", "the wind over" | "'the mean wind' cannot be 'above 10 knots'; a wind is compared in knots or points." | **(a)** The missing word was "is". The message never says so. | see 4 |
| 4 | 478159, 17:49 | captain | `... if the mean wind is 11 knots then ...` | "'the mean wind' cannot be '11 knots'; a wind is compared in knots or points." | **(a)** | 478201: `... if the mean wind is above 10 knots then ...` accepted |
| 5 | 478815, 18:00 | officer | `standing order "stuns'l": every 10 minutes if the mean wind is above 14 knots then take in the stuns'ls` | "After the name say a colon and then when, at or every: standing order "stuns": ..." | **(e)** The quoted name is cut at the apostrophe; the message is about a colon that is there. | name `studding`, `the studdingsails` (478818) |
| 6 | 496969, 23:02 | captain | `ease the bowlines` | "Nothing done: the starboard fore topsail bowline is already eased right off; ..." | (d) | none needed |
| 7 | 512943, 03:29 | officer | `take a bearing of the light` | "The officer of the watch may not take a bearing of the light without the captain: the reckoning, the sights and the course shaped are the master's for the captain." | **(c)** A mate with the deck at a night landfall takes the bearing of the light. Here a bearing also corrects the account, which is why it sits with navigation. | captain took it (512946) and allowed it (512951, 512955) |
| 8 | 521303, 05:48 | captain | `take a bearing of the pilot gig` | "The pilot gig is not in sight; did you mean the St Mary's pilots' gig? In sight: Sail ho! The St Mary's pilots' gig right ahead, bearing W by N, distant two miles; ..." | **(a)** Near-name not matched. The did-you-mean and the list are helpful. | `take a bearing of the st mary's pilots' gig` (521310) |
| 9 | 486001 to 521401, 20:00 to 05:50 | standing order `light sails`, **56 times** | `take in the occasional sails` | "Nothing done: the ringtail is already furled; the water sail is already furled." | (d), and log spam | none |
| 10 | 498018 to 502818, 23:20 to 00:40 | standing order `studding`, **8 times** | `take in the studdingsails` | "Nothing done: the starboard fore topmast studdingsail is already furled; ..." | (d), and log spam | none |

No refusal of class (b) in the slice. No refusal of a number in words, the water sail, a studding sail by name, or "full and by": `set the water sail` (462176), `take in the larboard fore topmast studdingsail` (491474) and `keep her full and by` (493043) were all accepted. The water sail came in by the phrase the notes say works, "take in the occasional sails", through the captain's standing order (483601).

---

## 5. Harness behaviour

### Seatings and door events

- No seating change. Six door events: five `stand_by` "out of turn" (457554, 464037, 478072, 478163, 517068) and one "its own word" (519118).
- The five out-of-turn stand-bys each follow a spoken line that had already closed the turn. They were taken as ordinary stand-bys. This is the pattern of owner's note 21: speak, the turn ends, then a second call to stand by.

### Stand-bys

50 in the slice. None refused.

| `until` | Count | Notes |
|---|---|---|
| a glass | 26 | Thirty minutes from the call, not the ship's bell |
| ten minutes | 5 | Logged "until ten minutes have passed" |
| a notable event | 3 | |
| tacked | 3 | |
| three bells | 3 | Re-issued twice after the captain's question and word |
| hove to | 2 | |
| a message | 2 | |
| a sighting | 2 | |
| six bells, filled away, a landfall, the pilot's hail | 1 each | |

The longest ran 6,751 s: "a landfall", 506189 to 512940 (01:36 to 03:29). It woke on the light. Apart from the tail of a trim in its first minute, the log has nothing notable in between.

### What woke the station

51 `agent.resumed`.

| Reason | Count | Worth it? |
|---|---|---|
| A glass | 20 | Ten were followed at once by another stand-by with nothing said or done (459836, 465837, 472605, 474407, 476210, 486060, 487864, 489666, 499855, 501658). One more (503462) only changed the wait to "three bells". Nine led to a report or an order, including the shortening of sail at 21:31. |
| A word from the captain | 15 | Twelve substantive. Three were acknowledgements that only cost a re-issued stand-by (491531, 496855, 503549). |
| A question from the captain | 2 | Both answered in 8 s with figures. |
| An event asked for (tacked ×2, hove to, filled away, six bells, three bells, ten minutes ×2, a landfall, a sighting) | 10 | All used. |
| A notable event | 1 | 461951, a wind shift; used to set the ringtail. |
| An urgent event | 1 | 493038, taken aback; orders 5 s later. |
| Noon | 1 | |
| Its own word | 1 | 519118; see the unheard word below. |

- Reply latency after a waking: 1 to 17 ticks, median 4. No long silences.
- Each sampling eases the driver to 1x: 45 `driver.eased` lines.

### A captain's word that did not wake the stand-by begun one second after it

- 517152 (04:39:12) [log]: `steady trim` fires, a notable line.
- 517153 (04:39:13) [log]: "The captain to the officer of the watch: Aye, we'll probably want to try and sail in as the Thames barges do ..."
- 517154 (04:39:14) [log]: "The officer of the watch stands by until a sighting". The transcript shows this call in turn, not "out of turn".
- No "A word from the captain" waking follows.
- 519118 (05:11:58) [log]: "The officer of the watch ends its stand-by (until a sighting) at its own word". Its words answer the Thames-barge line.

My reading: the notable line at 04:39:12 opened the turn, and the stand-by was the officer's reply to that sample. The game was at 1x just then (the captain was typing, and the three samples before it logged no easing), and one second is too short for a reply to the captain's word. So a `tell` that lands after the sample is built and before the stand-by begins does not wake the station. The officer answered it 32 min 45 s of ship's time later, on ending the stand-by himself. The other reading, that he saw the word and chose to stand by in silence, cannot be ruled out from the save.

Primer 16 says the captain's word wakes the officer whatever he stood by for. In that gap the pilot gig put off, and he learnt of it only on waking himself (519127).

### Nudges

Three, all wrong.

| Tick, time | Words |
|---|---|
| 505803, 01:30 | "The officer of the watch nudged: 3 contrary orders on the yards and the helm within the watch (tack ship; heave to; fill away)." |
| 505881, 01:31 | "... 4 contrary orders ... (tack ship; heave to; fill away; tack ship)." |
| 506078, 01:34 | "... 5 contrary orders ... (tack ship; heave to; fill away; tack ship; steer 309)." |

- The sequence was a planned night heave-to off a landfall, announced and approved: "Understood and agreed" (495921), "Wise, I'd say" (496854), "I like your plan" (503548).
- "Within the watch" is loose. The tack and heave-to were in the first watch (23:00, 23:02) and the fill-away in the middle watch (01:30). [source] The window is four hours back from the latest order (`harness.py` lines 253 to 254 and 1470).
- The chain grew to five with no pause. The officer ignored all three and carried on.
- No nudge at 22:13 for `keep her full and by; steer 309; steer 318`, because sail orders came between them and broke the chain.

### Journal, library, state

- **`journal`** once, 480648 (18:30), about 2,900 characters: position, plan, standing orders, the 18 grants, order-language lessons. Written because the captain asked.
- **`library`** four times in 8 s (478098 to 478106): "wind is compared", "if the wind", "standing order condition", "knots" in topic grammar. Four seconds later the officer reported failure, so the searches did not surface "is above".
- **`state`** once, 519135, after learning of the gig.
- No handover note in the slice.

### Thread and limits

- No sign of a lost thread, journal or permission across 141 entries. The officer recalled days-old matter unprompted: the two-cables boarding rule from Roscoff (517116), the frozen range of "the pilot boat off Plymouth and the frigate at Cawsand" (521291).
- Nothing points at a context, budget or relay limit. The one visible effect of the 50-second hold is the gap above.

---

## 6. Ship, sea, navigation and port observations

### 6.1 The landfall, tabulated

No sight, lunar or time sight was taken in the slice. The only `master.place` line carries no position: 459300, "Mr Travers came on deck, the day's work done."

| Tick | Time | Source | Position, bearing, distance or depth |
|---|---|---|---|
| 457500 | 26 Jun 12:05 | [log] noon | "No sight ... Latitude by account 49° 13' N ... Longitude by account 4° 54' W." |
| 457503 | 12:05 | [officer] | "St Mary's is about 70 miles NW by W" |
| 480648 | 18:30 | [officer] journal | "By account 49°29'N, 5°21'W (... uncertainty 10 miles E–W, 3 N–S). St Mary's about 45 miles NW by W ... The shaped line passes within a mile of the Gilstone"; "Lead orders all belayed (54 fathoms)" |
| 484222 | 19:30 | [officer] | "Scilly is 41 miles off" |
| 491478 | 21:31 | [officer] | "St Mary's is 32 miles off by account, but the longitude could be fifteen miles out either way" |
| 493377 | 22:02 | [officer] | "St Mary's is 28 miles off"; "at fifty fathoms" |
| 495889 | 22:44 | [officer] | "St Mary's is 23 miles by account" |
| 496813 | 23:00 | [officer], from the danger list | "the Wolf NNE ten miles by account, an unlit rock" |
| 497010 | 23:03 | [officer] | "The danger list is clear within ten miles." |
| 498051 | 23:20 | [log] deep-sea lead | "Fifty fathoms; fine grey sand with black specks." |
| 503503 | 27 Jun 00:51 | [officer] answer | "the account has gone from 49°47'N to 49°42'N, five miles south, and St Mary's from 21 to 24 miles" |
| 505804 | 01:30 | [officer] | "St Mary's, 25 miles" |
| 512940 | 03:29 | [log] lookout, notable | "A light right ahead, bearing NW." |
| 512946 | 03:29 | [log] bearing, captain | "St Agnes light bore NW, five leagues by estimation." |
| 512948 | 03:29 | [officer], before he saw the fix | "St Mary's 15 miles by account" |
| 512963 | 03:29 | [officer] | "the account has been corrected to 49°43'N, 6°04'W, now good to two miles. So we were some seven miles west of the truth in longitude" |
| 514800 | 04:00 | [log] lookout, routine | "The land is out of sight." |
| 514822 | 04:00 | [officer] | "St Mary's is 12 miles by account, still on 309" |
| 515521 to 521009 | 04:12 to 05:43 | [log] hand lead, ten casts | "No bottom at twenty fathoms." |
| 516688 | 04:31 | [officer], from the danger list | "the Gilstone and the Spanish Ledge both NW by N, nine and ten miles, by account" |
| 516915 | 04:35 | [officer] | "The book now gives the mouth of St Mary's Sound bearing NW (315°), 9.9 miles, with the Spanish Ledge and the Woolpack NW by N." |
| 517116 | 04:38 | [officer] | "The mouth of the Sound has drawn to NW by W" |
| 519127 | 05:12 | [officer] | "The mouth of the Sound is NW by W, 6.9 miles by account ... the danger list is filling with the Western Rocks and the ledges six to eight miles off" |
| 520680 | 05:38 | [log] lookout, notable | Gig WNW two miles. "Peninnis Head bearing NW by W, distant four miles." |
| 520689, 520694 | 05:38 | [log] bearings, captain then officer | "Peninnis Head bore NW by W, four miles by estimation." |
| 520740, 520752 | 05:39 | [log] lookout; bearing, captain | "Peninnis mill ... NW by W, ... four miles" |
| 520980 | 05:43 | [log] lookout | "St Mary's bearing NW, distant four miles." |
| 521220 | 05:47 | [log] lookout | "Hugh Town bearing NW, distant three miles." |
| 521280 | 05:48 | [log] lookout | "The Garrison bearing NW by W, distant four miles." |
| 521310 | 05:48 | [log] bearing, captain | "The St Mary's pilots' gig bore WNW, two miles by estimation." |
| 521400 | 05:50 | [log] lookout | "St Agnes bearing WNW, distant four miles." |
| 521423 | 05:50 | [officer] | "forereaching W by N at about three knots, towards the gig, with the Gilstone three miles off" |

**Course and sail, and by whom.**

| Time | By | Order |
|---|---|---|
| (10:52) | officer | steer NW by W (309°), the shaped course |
| 13:14 to 13:22 | officer | ringtail, water sail set |
| 15:07 | officer | larboard fore topmast stuns'l set |
| 19:20 | captain's `light sails` | ringtail and water sail in |
| 21:31 | officer | stuns'l and gaff topsail in |
| 21:57 | officer | full and by; fore topgallant in |
| 22:02 | officer | steer 309; flying jib in |
| 22:13 | officer | steer 318 |
| 23:00 to 23:03 | officer | tack; heave to on the starboard tack |
| 01:30 to 01:34 | officer | fill away; tack; steer 309 |
| 04:00 | officer | flying jib and fore topgallant set |
| 04:35, 04:38 | officer | steer 315; steer 310 |
| 05:12 | officer | fore topgallant and flying jib in |
| 05:38 | officer | steer 292, for the gig |
| 05:48 | officer | heave to |

### 6.2 How good the account was, and how it was corrected

- **Before the light.** [log] The last bearings were taken off the Isle of Bas at 05:34 on the 24th (261247), and the land was lost at 08:00 that day. The last observed latitude was at noon on the 25th (371100). So the longitude had run about 70 hours on account and the latitude about 39.
- The master's stated doubt was 10 miles east and west at 18:30 [officer]. At the light the officer put the error at "some seven miles" of longitude. The stated doubt was honest.
- **The correction.** One bearing of one light with the lookout's estimated distance moved the account to 49°43'N, 6°04'W. That is exactly "NW, five leagues" from St Agnes light (49°53.6'N, 6°20.7'W in the chart file). [source] A line taken after a run of more than two miles replaces the account across it (`reckoning.py` lines 682 to 727). A 15% estimate at 15 miles gives about two miles along the bearing, which is the officer's "good to two miles".
- **At the land.** Peninnis Head came up at four miles in haze at 05:38. [officer]: "which agrees with the account."
- **How close.** Nothing nearer than about three miles by the lookout's estimates: Hugh Town three miles (05:47), the Gilstone "three miles off" [officer, 05:50]. The Wolf was ten miles NNE by account at 23:00.
- **Opportunity not taken.** The light was in sight for 31 minutes (03:29 to 04:00). Only the captain's one bearing was taken. The officer had leave from 03:29 and took none.

**What the game said as she closed the land, and how loudly.**

- Two notable lookout lines for the landfall (03:29 the light, 05:38 the land and the gig), five routine sightings, and one routine "The land is out of sight."
- Nothing urgent. No `lookout.closing` in the slice. The first came four minutes after it (521700, 05:55, notable): "Peninnis Head bearing NW, steady and closing: distant three miles."
- [source] That hail is notable, not urgent. It needs ten minutes of a steady bearing and, for land, a range within three miles (`lookout.py` lines 117 to 126 and 388 to 419).
- No danger was ever sighted. [source] The Gilstone, the Woolpack, the Spanish and Bartholomew ledges are low-water rocks. She never came within three miles of them, and it was within two hours of high water ([officer] 512948: "the high water at Scilly about half past four"). The officer knew of them only from the danger list, which is by account.
- The slice never put notes 19 and 24 to the test: she was never within three miles of anything.

### 6.3 Two readings that carry the truth

**"The port."**

- [source] `ports.py` `port_words` (lines 976 to 1018) measures from `self.world.position`. `core/world.py` lines 538 to 541 call that "the truth, which no reading gives". Every sample carries the readings that have changed since the last (`agents/tools.py` lines 153 to 172; `agents/harness.py` lines 971 to 993).
- [source] Beyond ten miles the reading says "the nearest is St Mary's, N miles off". Within ten it says "St Mary's, the mouth of St Mary's Sound bearing NW, 9.9 miles; ...; the pilot gig standing out toward her".
- [log, officer] The figure arrives at the ten-mile switch in the reading's own form: 516915 (04:35), "The book now gives the mouth of St Mary's Sound bearing NW (315°), 9.9 miles".
- [log, officer] It disagrees with the by-account danger list in the same breath. The mouth bore NW at 04:35 and "NW by W" three minutes later, so it bore about 309°. The Spanish Ledge and the Woolpack bore "NW by N", 321° or more. [source] Those rocks lie 0.3 and 0.5 mile from that mouth (`st-marys.yaml`, `channel-west.yaml`). At ten miles they should bear within three degrees of it. Two positions are in play, about 1½ to 2 miles apart.
- [log, officer] The officer steered by it in haze with the land out of sight: 516911 `steer 315` ("straight for the mouth of the Sound"), 517116 `steer 310` ("to stay on the middle of the line"). He called the figures "by account".
- [log, officer] It told him of the gig 26 minutes before the lookout did: 519127 (05:12), "the pilot gig is standing out towards us!" The first lookout line is 520680 (05:38). No log line marks the boat's launch.

**"The depth of water."**

- [source] `api/readings.py` lines 557 to 566: the chart's depth at `world.position`.
- [log, officer] The officer wrote "Lead orders all belayed (54 fathoms)" at 18:30 and "at fifty fathoms" at 22:02. No cast had found bottom since Roscoff; the last seven before the slice were "No bottom at twenty fathoms" (259746 to 263347, 24 June). The deep-sea cast at 23:20 then found "Fifty fathoms".

So the parity for a model that owner's note 24 asks for already exists by accident, for ports and for depth, and it bypasses the reckoning.

### 6.4 The deep-sea lead and the hand lead

- **The deep-sea lead exists.** 497021 (23:03) [log]: "Order: heave the deep sea lead." 497022: "Pass the deep-sea line forward; hands to the spritsail yard and the chains." 498051 (23:20): "Fifty fathoms; fine grey sand with black specks." The cast took 17 min 10 s, hove to.
- [source] 120 fathoms of line; no bottom with more than four knots of way (`reckoning.py` lines 237 to 240). It is in the officer's own domain (`agent.py` lines 191 to 198).
- **The officer never used or mentioned it.** A search of the whole session's transcript (828 entries) finds no "deep sea". The captain ordered it twice (here and at 531454, 27 June 08:37). The 23:20 sounding was put in front of the officer; he stood by without comment (498055).
- **The hand lead.** `approach lead` ("every 10 minutes then heave the lead") was resumed at 514819 (04:00) and fired 11 times. Ten casts at 4½ to 7 knots, all notable, all "No bottom at twenty fathoms."
- **Depth readings beside the casts.** Only the two figures in 6.3. The officer quoted none on the morning approach.
- **Wakings by a sounding.** None. No stand-by named "a sounding". Stand-bys for "a glass" and "a sighting" slept through the notable no-bottom lines.

### 6.5 The standing orders through the night

| Name, by, text | In the slice |
|---|---|
| `trim` (mate): "at a wind shift then trim sails" | Fired 3 times: 460568 (12:56), 493184 (21:59), 517935 (04:52). Belayed 23:00 to 01:34 and from 05:48. |
| `steady trim` (mate, entered 469859 at the captain's request): "at steady on the course then trim sails" | Fired 7 times, each on a "Steady on ..." line: 493181, 493419, 494089, 506186, 516953, 517152, 520784. Belayed with `trim`. |
| `light sails` (captain, 478201): "every 10 minutes if the mean wind is above 10 knots then take in the occasional sails" | Did its work once (483601, 19:20). Then 56 "Nothing done" rejections and 3 `standing.held`. |
| `studding` (mate, 478818): "every 10 minutes if the mean wind is above 14 knots then take in the studdingsails" | Never needed. 8 "Nothing done" rejections and 5 `standing.held`. |
| `approach lead` (mate): "every 10 minutes then heave the lead" | Resumed 04:00. 11 firings, 10 casts. |
| `Pilot hails` (captain): "at the pilot's hail then tell the officer the pilot has hailed, proceed as the situation demands" | Fired once, 521280. It woke the officer as "A word from the captain". |

- No standing order for bearings: the officer had no leave for them until 03:29 and set none up after.
- **`standing.held` is quiet; "Nothing done" is not.** A condition that is false logs once a spell (8 lines). An order with nothing left to do logs a rejection every period (64 lines).
- **`trim` and the log's wind-shift line run on different clocks.** `trim` fired at 12:56, 21:59 and 04:52. The log's `wind.shift` lines are at 13:19, 22:02, 22:07 and 23:53. None coincide.
- **`trim` and `steady trim` overlap harmlessly.** 493181 and 493184, three seconds apart: "the yards are being trimmed already, 2 still to brace taking the new angle."
- **Fights for hands.** One trim takes the whole watch. 75 of the 77 `evolution.waiting` lines are trims waiting on trims. The log waited once (493201, 22:00: "Not hands enough on deck to heave log"). The lead waited once (520820, 05:40: "Not hands enough on deck to heave lead; the watch is bracing the fore topsail yard and trimming the foresail and the mainsail"); that cast came at 05:43. Only one lead order was running.
- The officer belayed both trim orders before each heave-to and resumed them after the first. Neither filled her out of a heave-to.

### 6.6 Sail handling and trim

- **Trim before the helm has swung.** 493043 (21:57:23) `keep her full and by`. The captain's `Trim the sails` 13 s later braced to "47° on the larboard bow" (493056) while she was still swinging. At 493181 the helm was "Steady, full and by, the wind 60° on the larboard bow" and `steady trim` braced again to 62°. After that every course change was followed by `steady trim` at the "Steady on" line, 36 to 108 s after the order.
- **The yard-angle query (463986).** [officer]: "'trim' said it braced the yards "to the wind, 69° on the larboard bow", yet the log has them at 58° to 60° from square". The log's pairs show a rule, not a fault: 53°, 64°, 68° and 69° give 58° to 60°; 76° gives 54°; 77° gives 53°; 85° gives 45°. The yards ease once the wind is abaft about 70°, keeping the wind about 40° on the sail. The officer expected "about 40°" from square at 69°. The log is consistent; which figure is the better seamanship is the owner's call.
- **Tacking.** Two tacks, both clean, both piping all hands and piping down: 496809 to 496948 (139 s, "heading S (182°)") and 505881 to 506071 (190 s, "heading WNW (287°)"). No wear in the slice.
- The second tack was ordered four seconds after "Filled away" from lying-to. A leeway line in stays reads "Leeway 53° to starboard" (505998). She went round anyway.
- **Lying-to forereaches fast.** "Hove to" at 497002, yet 500444 (00:00) "Hove the log: three knots and a quarter", and five miles of southing in 1 h 48 min by the officer's own account figures. She lost four miles of her distance (21 to 25) in 2½ hours.
- **Occasional sails need two orders.** Rig out the boom, then set. The boom's completion line is routine (`spar.rigged_out`), so "a notable event" cannot wait for it: 467647 to 468474, 13 min 47 s, ended only by the captain's word.

### 6.7 Other sail

- None but the pilot gig: one "Sail ho!" in 17 h 46 min and about 100 miles. No `what is she` or `make her out` was ordered. The gig was made out unasked three minutes after she was sighted (520860).
- **The gig's distance stayed fixed.**

| Tick | Time | Line | Distance |
|---|---|---|---|
| 520680 | 05:38:00 | sighting, bearing WNW | "distant two miles" |
| 521280 | 05:48:00 | the hail | [source] sent only within four cables |
| 521303 | 05:48:23 | in-sight list, bearing W by N | "distant two miles" |
| 521310 | 05:48:30 | captain's bearing, WNW | "two miles by estimation" |
| 521460 | 05:51:00 | pilot aboard | [source] only within two cables |

- [source] The cause: the lookout draws one estimate per sighting and holds it "until she has moved a mile from where it was judged" (`lookout.py` lines 107 to 115 and 362 to 386). "She" is the Speedwell. The rule was written so that land does not wander in a calm, and it is applied to sails as well. A vessel that closes a slow, hove-to or anchored ship keeps her first distance while her bearing changes.
- It misled the officer. 521291 [officer]: "after a mile and a half sailed straight at her she's still "two miles" ... Chasing her would take us into the Spanish Ledge and the Gilstone". He proposed the long-boat, then taking the Sound without a pilot, then (521394) filling away to run down to her. By the hail rule the gig was within four cables when he wrote the first of these.
- Small words: the gig is "pulling off from the land" at 520680 and "under plain sail" at 520860. "Sail ho!" appears inside the in-sight list (521303).

### 6.8 The St Mary's pilot

- **Sighted** at two miles in haze (05:38), "A gig pulling off from the land", ten minutes before the hail. **Made out** at 05:41.
- **Hail** 521280 (05:48), a routine line: "The gig hailed: a pilot for St Mary's; shorten sail and he will come aboard."
- **The officer's answer** in ten seconds: belay the trims (521289), `heave to` (521290). "Hove to" at 521347.
- **Aboard** 521460 (05:51), three minutes after the hail, with the ship hove to. [officer, 39 s earlier]: "forereaching W by N at about three knots, towards the gig". No log line gives her speed at the boarding.
- [source] The rule is two cables and six knots over the ground (`ports.py` lines 94 to 100). The boat runs in to about a cable and a half and then lies to (`ships.py` lines 563 to 629). The officer's "the book has her "lying to" now" (521329) agrees.
- So the gig had come up and lay to, and the boarding waited on the ship. Had the captain not said "stay hove to", the officer would have filled away (521394).
- **The pilot's words** (521460) are one notable line of about 1,700 characters. They end: "the flood will serve from about half past ten in the morning." By his own words he boarded some four and a half hours before the tide would serve.
- The pilot came off unasked. [source] The port file sets the cruising ground at eight miles. The officer offered to "hoist the signal for a pilot" (517015); owner's note 9 says signalling is not yet built.

### 6.9 Taken-aback and wind-shift lines under m5c-b

**Taken aback.**

- One `ship.aback`, urgent and real: 493038 (21:57:18), "Taken aback: the sails pressed against the masts and she lost her way." She was making about six knots when the wind went from SSW to W by S [officer].
- "She lost her way" overstates: 493316 (22:01:56) "Hove the log: six knots and a quarter."
- No line says when she is out of it.
- None of the three notable forms ("at anchor", "no way on to lose", "in the light air") occurred, though the mean wind was 3 to 6 knots from 12:05 to about 16:00 (the gust lines give the mean).
- Six notable per-sail lines, all in deliberate evolutions: "Fore topsail taken aback." (496845, 496972, 505921, 521312) and "Fore staysail taken aback." (496961, 521300). The real aback at 21:57 produced no per-sail line.

**Wind shifts.**

- Four `wind.shift` lines in 17 h 46 min, with the mean's point and strength: 461951 "Wind backed to SSW, light airs."; 493355 "Wind veered to SW by W, a gentle breeze."; 493676 "Wind veered to W by S, a moderate breeze."; 500034 "Wind backed to SW by W, a moderate breeze."
- The line is now late for a sudden shift. The shift that took her aback at 21:57:18 was logged at 22:02:35 and 22:07:56.
- No squall line announced that shift. "Squally" came 42 s after it (493080). The three logged squalls came later.
- The only warning was the sky at 21:27. The officer acted on it.

### 6.10 Log noise, counted

| Kind | Count | Span | Remark |
|---|---|---|---|
| Standing orders' "Nothing done" rejections | 64 | 20:00 to 05:50 | 85% of all rejections in the slice |
| `evolution.waiting` | 77 (16 notable) | every trim | 14 are "Bracing the yards: not hands enough for all at once" |
| `evolution.short_handed` | 37 | every trim | |
| `yard.braced` | 17, all notable | every trim | |
| "No bottom at twenty fathoms" | 10, all notable | 04:12 to 05:43 | |
| `ship.leeway` | 79 | 44 while hove to | Flipping between 17° and 21° |
| `wind.gust` | 31 | | 4 where gust equals mean, e.g. 457553 "A gust: 3 knots, the mean 3." |

- There were 18 trims (8 by the captain, 3 by `trim`, 7 by `steady trim`). One trim is about 15 log lines, three of them notable.
- About 57 of the slice's 128 notable lines are by-products of trimming, no-bottom casts and deliberate backing.

### 6.11 Smaller oddities

- "Hands to the spritsail yard" (497022) on a topsail schooner. [source] Her file has a bowsprit and jib boom and no spritsail yard.
- `sea.change` three times in 12 minutes round one squall: 498780 "A moderate sea getting up."; 499320 "A smooth sea, the sea going down."; 499500 "A moderate sea getting up."
- `weather.sky` 494700: "The sky detached clouds, hard-edged and oily-looking." The sentence lacks a verb where the others read naturally ("The sky clear.").
- The sky words earned their place: "small inky clouds" at 21:27 was the only warning of the shift.
- The captain's chart shows "unnamed danger markers" (517005) where the officer's list names the Gilstone and the Spanish Ledge.
- [source] The chart has one Gilstone, off Peninnis, and no Western Rocks.
- Noon is made at 12:05 by the ship's clock, five minutes into the afternoon watch.

---

## 7. The model as an officer

### Good calls

- **Shortened on the sky.** 491474 (21:31), stuns'l and gaff topsail in: "rain, small inky clouds ... That's squall weather". This was 26 minutes before the shift that took her aback and ahead of his own midnight plan.
- **Planned the landfall for daylight and said so early.** 469913 (15:31): "If it freshens tonight and we come up on them in the dark, I'll heave to well to the south-east of St Agnes and wait for dawn, not feel for the Western Rocks at night." He revised the arithmetic at each change of speed and asked before acting: 484222, "Will that serve?"
- **Changed the tack of the heave-to at the last minute.** 496813 (23:00): "Hove to on the larboard tack she'd drift NE, straight down onto [the Wolf], so the larboard tack is the wrong side."
- **Quick and right on the urgent line.** Two orders in 5 s (493043).
- **Managed his standing orders.** Both trims belayed before each heave-to (496809, 521289) and resumed after (506079).
- **Hove to at the pilot's hail** within ten seconds, though he believed the gig two miles off.
- **Candid about the game, briefly and with fixes.** The routine boom line (468480); the missing "is" (478209); the apostrophe (478822); the frozen range and the near-name (521329).
- **Quiet when there was nothing to say.** Ten glass wakings passed with a bare stand-by.

### Mistakes and weaknesses

- **Left the trimming to others.** Through the afternoon the wind drew from 53° to 85° and the captain trimmed six times. The officer woke each glass and did not trim.
- **Called truth "by account".** He took the port reading's figures for the account and steered by them (516911, 517116). The reading does not say where it measures from, so this is the game's fault more than his. But at 04:35 he had the mouth bearing NW and its ledges NW by N in one sentence (516915), and read the gap as geography: "Those lie on the St Mary's side, east of the Sound."
- **The Gilstone.** From 18:30 he took it for the Western Rocks' Gilstone, from knowledge outside the game. That made him "doubt the account" at 04:31 (516688). He put it right himself at 05:39 (520743): "The Gilstone in the list must be the rock off Peninnis Head".
- **A limit that moved.** 04:00: stand off "by about six miles off" if no land shows (514822). 04:35: "haul off at about six or seven miles" (516915). 04:36: "close to about three miles from the mouth if the haze allows" (517015). At 05:12, 6.9 miles off with no land, he stood on under less sail. The land showed at four miles. He told the captain each time, but gave no reason for the change.
- **Never found the deep-sea lead.** Ten hand-lead casts found no bottom. The order that would have found it is in his own domain, and the captain had used it in front of him five hours earlier.
- **No second bearing of the light** in the 31 minutes he had leave.
- **Misjudged the gig.** His reading of the frozen figure was correct; his proposals from it were wrong, and the captain overruled him.
- **Understated the forereach.** "About two knots" and "a mile and a half an hour" (497010, 503503), against five miles in 1 h 48 min by his own figures and 3¼ knots by the log.
- **Words and deeds.** He twice said he would "wear" (503503, 505804) and ordered `tack ship` (505881). He reported "Tacked, sir" correctly.
- **Premature praise of the account.** 512948: "Since it's dead on our course, the account has served us well". Fifteen seconds later: "we were some seven miles west of the truth".
- **Guessing in bursts.** Five wordings in 13 s and four library searches in 8 s, then gave up. The captain found it in two tries.

### What he wished for

- A stand-by on two conditions. 506079 [officer]: "I'll stand by for a landfall or a glass, whichever comes first." He could submit only "a landfall". Likewise 495889, "Meanwhile I'll stand by for a landfall", then `stand_by("six bells")`.
- An event for "the boom rigged out".
- A refusal that names the fix.
- Near-name matching for bearings.
- Deliberate backing not logged as "taken aback".

On balance: a careful, communicative watch whose seamanship decisions were sound and whose errors mostly trace to readings that do not say where they come from.

---

## 8. Cross-check against the notes

### The owner's items

| Note | Evidence in the slice | Verdict |
|---|---|---|
| 1. Pilot boarding under way | Mr Ellis boarded at 521460 with the ship hove to since 521347, forereaching about three knots [officer]. The gig had come up and lay to; the boarding waited on the ship. | **Adds nuance.** Here she was hove to, by the officer's own order at the hail. |
| 2, 3, 7, 8, 20, 22, 23 | | Not seen in the slice |
| 6. "NaN fm" on the chart | The log's soundings read correctly. Ten casts were "no bottom". | Cannot be seen; see section 10 |
| 9. No way to accept or refuse the pilot | The pilot came off unasked. The hail is one-way and routine. The officer offered to hoist a signal for him (517015). | **Supports** |
| 10, 11. Journal | The captain asked for a journal entry "just in case" (480631). Nothing was lost. | The worry is live; no failure seen |
| 12. Re-seating | None in the slice | Not seen |
| 13. Multi-condition stand-by | 506079: "a landfall or a glass, whichever comes first", submitted as "a landfall" alone. 495889 likewise. From 03:29 to 05:48 he cycled through six single conditions. | **Supports**, strongly |
| 15. General authority | 491530 [captain]: "you have permission to keep her safe as necessary. If I see a refusal I'll allow it ASAP." The 03:29 landfall took one refusal and three captain's inputs in 12 s. | **Supports** |
| 16. "Keep" orders | Eight hand trims by the captain. `steady trim` added at his request (469856). Two pairs of belays and one of resumes round the heave-tos. 64 "Nothing done" lines. | **Supports**, and adds: a "keep" order must be silent when already satisfied |
| 17. Taken aback in calms | One urgent line, real. None in four hours of 3 to 6 knots. | **Supports the fix.** Nuance: six notable per-sail lines from deliberate tacks and heave-tos |
| 18. Wind-shift spam | Four lines in 17 h 46 min | **Supports the fix.** Nuance: the line now trails a sudden shift by 5 and 10 minutes |
| 19. Reckoning near visible land | The account was about seven miles out at the light [officer] and was put right by one bearing. No alarm was needed. At 04:35 the danger list by account put two ledges 11° from the port reading's bearing of the Sound's mouth, where 3° at most is possible. | **Adds nuance.** The slice never tested the alarm. The disagreement supports "the danger list follows the account". Here the replacing figure was the better one. |
| 21. `say` ends the turn | Five out-of-turn stand-bys after spoken lines. The unheard word at 517153. | **Supports** |
| 24. Parity near land; "nearest land" | The port reading already gives a true bearing and distance. "The Gilstone" unqualified misled the model for eleven hours. The captain's chart leaves those dangers unnamed. | **Adds nuance** |
| 25. Chart snapshot for the model | 516902 to 517005: the captain describes his chart to the officer in words | **Supports** |

### The model's comments and additions

| Note | Evidence in the slice | Verdict |
|---|---|---|
| "Fifteen permissions one by one" | Two more at 03:29, the second redundant | **Supports** |
| "'A sounding' also wakes on 'no bottom'" | No stand-by named "a sounding". The ten no-bottom lines are notable. | Cannot be seen directly; consistent |
| Contrary-orders warning on ordinary sequences | Three nudges at 01:30 to 01:34 for a planned heave-to | **Supports** |
| "'Trim sails' acts before the helm has swung" | 493056 (47°) against 493181 (62°). `steady trim` is the working remedy, seven firings. | **Supports** |
| "Confusing without a deep-sea lead" | The deep-sea lead exists, is in the officer's domain, and was used by the captain at 23:03. The model never used it in the whole session. | **Contradicts the premise; supports the confusion** |
| "Lead standing orders fight for hands. Three of them at once ..." | One lead order running. It waited once on a trim (520820). The log waited once (493201). | **Adds nuance:** the trim is what takes the hands |
| "Other ships keep a fixed distance" | The gig: "two miles" three times over 10½ minutes, with the hail and boarding between | **Supports, and explains** (6.7) |
| Water sail by name; "furl"; "watersail" | Set by name (462176). Taken in by "the occasional sails" (483601). | Consistent; the failing phrases were not tried |
| Number words above twelve | | Not seen |
| "'Full and by' ... the permission had to be 'keep her full'" | `keep her full and by` accepted (493043) | Consistent |
| Worked well: fixes from bearings | The 03:29 fix | **Supports** |
| Worked well: quieter "aback" lines | One urgent, real | **Supports** |
| Worked well: number-free standing orders | A numeric one worked too (`light sails`, 483601), once "is above" was found | **Supports**, with the grammar caveat |
| Worked well: "what is she" | | Not used |
| Worked well: the noon latitude | No sight on the 26th, said plainly | Handled; not tested |
| Relay cut; handover in the brief; officer as a person; boats; kedging; sternway | | Not seen in the slice |

---

## 9. New findings not in the notes

Ranked by weight.

**1. Two readings give the truth, and the officer navigated by one.**
"The port" measures from the true position; "the depth of water" is the chart at the true position. Evidence: the 9.9-mile switch (516915); the 11° disagreement with the danger list (516915, 517116); the gig known 26 minutes early (519127); "54 fathoms" with no cast (480648). Detail in 6.3.

**2. The lookout's distance to another vessel is frozen until the Speedwell has moved a mile.**
This is the mechanism behind the notes' "other ships keep a fixed distance". Evidence: gig "two miles" at 520680, 521303 and 521310, with the hail at 521280 and the boarding at 521460. It led the officer to three wrong proposals. Detail in 6.7.

**3. A captain's word can go unheard in the gap between a sample and a stand-by.**
517153 against 517154; answered at 519118, 32 min 45 s later. This is my reading of the ticks, not a logged fault. Detail in section 5.

**4. A standing order with nothing left to do rejects itself every period.**
64 lines from two orders in ten hours (486001 to 521401), against 8 quiet `standing.held` lines. Detail in 6.5.

**5. One "trim sails" is about 15 log lines, three of them notable.**
18 trims in the slice. With no-bottom casts and deliberate backing, about 45% of the slice's notable lines are noise. Detail in 6.10.

**6. Standing-order conditions need "is", and the refusals hide it.**
Six refusals (478078 to 478159) say "a wind is compared in knots or points". An apostrophe in a quoted name gives a refusal about a colon (478815). Four library searches did not help.

**7. Evolutions that end on a routine line cannot be awaited.**
The boom: 467647 to 468474, 13 min 47 s, ended by the captain.

**8. The pilot boat's launch is not in the log, and her hail is routine.**
The captain keeps a standing order (`Pilot hails`) to turn the hail into a word to the officer, and the log credits that word with the waking (521280). The officer learnt of the launch only from the port reading (519127).

**9. Lying-to is not much of a stop.**
3¼ knots by the log at 500444; four miles of distance lost in 2½ hours.

**10. The bearing refusal at the landfall.**
512943. Harmless only because the captain was at the prompt at 03:29. Allowances are per verb and outlive the watch, so the log's "(the light)" and "for the watch" both mislead.

**11. The urgent aback line's words and timing.**
"She lost her way", then 6¼ knots 4 min 38 s later. No all-clear. No squall line for the shift that caused it. The wind-shift line 5 and 10 minutes after.

**12. `trim`'s "at a wind shift" and the log's `wind.shift` are different detectors.**
Three firings and four lines; none coincide (6.5).

**13. Names.**
One unqualified "Gilstone"; no Western Rocks in the chart; the captain's chart with unnamed markers (516902, 517005).

**14. Small wording.**
"Spritsail yard" on a schooner (497022). A gig "pulling" then "under plain sail" (520680, 520860). "Sail ho!" inside a list (521303). Gusts equal to the mean (457553). The sea state flapping (498780 to 499500). "Within the watch" across two watches (505803).

---

## 10. Could not determine

- **What the readings said, word for word.** Tool results are not in the save. The truth-reading finding rests on the source and on the officer's quotes, which agree. A check of the save's true position against the account at 03:29 and 04:35 would settle it.
- **The true track**, and so how far the account was out through the night. "Seven miles" is the officer's figure. My own back-plot from the Wolf's bearing gives about six, south-east rather than east, and is rough.
- **Which source the officer's "St Mary's N miles" came from before 03:29.** After about 19:30 the figures behave like the port reading. They show no jump at the fix (15 before, 12 half an hour later), though the account moved some seven miles. At 18:00 he gave "51 miles to go" and "48 miles to run" 33 seconds apart (478822, 478855), which looks like two sources.
- **Her speed at the moment the pilot boarded**, and the gig's true distance at each line.
- **Whether "the pilot's hail" wakes a stand-by on its own.** The captain's standing order fired in the same second.
- **The compression in use**, and so the real-time cost of 45 easings and the real length of the 32-minute gap.
- **Whether the model was shown the captain's 04:39 word before its stand-by took effect.**
- **Why `trim` fired at 12:56 and 04:52** with no logged shift.
- **What the chart showed.** The unnamed markers are the captain's report. Whether a no-bottom cast is what plots as "NaN fm" (note 6) cannot be told from the log.
- **Whether the 21:57 shift was a front or the weather-system chatter** that CHANGES-m5c-b describes.
- **Why no other sail was sighted in 100 miles.** The scenario lists twelve vessels; their positions on the sixth day are not in the dump.
