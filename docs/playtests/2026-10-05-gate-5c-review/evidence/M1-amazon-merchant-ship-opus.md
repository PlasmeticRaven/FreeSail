# M1 - The Amazon as "a merchant ship, free", Falmouth to the Isle of Bas (session 8, Opus 5.5 officer)

Conventions. Tick = one second of ship's time from 05:00:00 on 5 October 1805, so clock time = 05:00:00 + tick. "LOG" marks what the ship's log shows; "OFFICER" / "CAPTAIN" marks what a model or the owner said; "CODE" marks something I read in the m5c source or data (read-only) to explain a log line; "INFERRED" marks my own arithmetic from logged bearings and the chart's feature positions.

## 1. Slice identity

- **Session** `8-merchant-ship-opus`, the whole of it: ticks 0 to 123,673; ship's time 5 Oct 1805 05:00:00 to 6 Oct 15:21:13 (34 h 21 min). Played 5 October 2026.
- **Scenario** "A merchant ship, free", seed 7, American colours, purse £5,000, price list for Falmouth only, no chronometer, master's skill 0.9, twelve other vessels in the world. **Ship**: `data/ships/frigate-36.yaml`, the ship-rigged *Amazon* (CODE: complement 264; `draught_m: 4.6`, the file's own comment "15 ft mean, judgement: 13 ft forward, 17 ft aft").
- **Officer of the watch** "Mr Pearce", first lieutenant: **Opus 5.5 through the MCP door**, one seating, 295 transcript entries (114 `submit_order`, 74 `stand_by` calls plus 13 stand-bys taken out of turn, 60 spoken lines plus 5 "own word" lines, 13 `library`, 7 `journal`, 5 `shelve`, 3 `answer`, 1 `hand_over`). Station header: `policy every_s 1800, events notable+urgent, lockstep false`, `patience_s 3600`, `budget_tokens None`, `stand_by_ends_turn True`; the door note says `say` and `stand_by` are "held open until your next turn ... for up to 50 seconds".
- **Log**: 2,305 events, 440 notable, 1,865 routine, **no urgent line in the whole session**.
- **Build: plain m5c**, on four pieces of evidence. (a) The save is `FreeSail-gate-m5c/saves/freesail-seed7-tick123673.json`. (b) The door note cites the consent record "docs/agents/consent/2026-10-02-opus-5.5.md", the m5c record, not the m5c-b re-ask of 3 October; no consent question was put in this session. (c) LOG+CODE: `wind.shift` lines follow a squall's end by 8 s and 49 s (squall over 36999, "Wind backed to W by S" 37007; squall over 40280, "Wind backed to SW by W" 40329). m5c-b's `_log_wind_shift` reads the ten-minute mean and needs 60 s clear of a squall before it may speak; m5c reads the instant wind. (d) No "Her sails aback ..." line and no numbered-seating wording appear (neither would have been triggered: she was never aback with no way on, and there was one seating).

## 2. What happened

| Time (tick) | Event |
|---|---|
| 5 Oct 05:00 (0-175) | Start in Falmouth's entrance, wind WSW 22 kn. Captain lets go the best bower ("in eleven fathoms; fifty-four fathoms of cable veered", 80), tells the officer "I'll leave you broad authority, if you deem anything necessary then either ask and I'll allow, or try and I'll allow as I see it" (2), gives four allowances and the deck (175). |
| 05:03-05:11 | Officer veers to 70 fathoms, enters "lead at anchor", reads primer 14 and the price list, proposes tin for Roscoff and brandy home, buys: "Bought 30 tons of tin at Falmouth at £120 a ton, £3600 paid; the boat goes for it. The purse: £1400." (662) |
| 05:17-08:55 | Launch away 05:17, at the quay 05:47, "shoved off" 08:17, alongside and tin struck down 08:55 (14129). |
| 08:58-09:32 | Seven more allowances; `get under way on the starboard tack and steer S by E` refused, allowed, accepted (14299-14308). Aweigh 09:22; Falmouth pilot aboard 09:25 (15900); "Under way on the starboard tack ... full and by (S by E (169°) lying too near the wind to be laid)" 09:32 (16342). |
| 09:32-09:56 | Officer steers SSE, SE, SSE by bearings and lead, distrusting the account; hove to 09:43 for the pilot, "Mr Tregenza left her in the cutter ... the pilotage, £5, paid" 09:55 (17700); filled away by the officer's standing order "pilot off". |
| 10:00-11:35 | Courses, topgallants, spanker set; nine `strain.warning` lines 10:36-11:01 at 10½ knots; topgallants taken in 11:04, furled 11:35. Noon (11:49): "Latitude by observation 49° 51' N ... Longitude by account 4° 51' W". |
| 14:00-16:11 | Rain, three squalls (15:01 25 kn; 15:08 34 kn; 16:05 24 kn). Courses in by the officer's "squall" order; topsails single-reefed by "shorten sail for weather" at 15:21, after the 34-knot squall had passed. |
| 15:09-19:35 | A sail steady on ESE closes for 3½ hours; made out at 18:44 a mile off, a British frigate (red ensign), passes two cables astern at 19:12 without hailing. |
| 17:53-19:30 | Officer asks for a lunar; refused to him, ordered by the captain. 19:18: "longitude by lunar 4° 54' W, which he would trust within 50 miles; the reckoning was 4° 22' W" (51502). The account jumps to 4° 53' W (OFFICER); the captain's allowance to set the reckoning does not work; the captain sets it himself to 49° 00' N 4° 21' W (52247). |
| 20:00-24:00 | Wears to the larboard tack and heaves to for the night about 22 miles off by account (20:13); deep-sea lead 49 to 55 fathoms, "fine grey sand with black specks". |
| 6 Oct 00:00-09:00 | Fills away, wears, steers SE by S; wind dies; royals, staysails, studdingsails both sides set by 04:19; 1 to 2 knots all night. |
| 09:14-09:43 | Officer: "the account cannot be right. It puts the Lavandière SE by E, only four miles off, yet no land is in sight" (101676). Studdingsails in, heave to, deep-sea cast 51 fathoms; fills away SSE. |
| 10:38 | "The Isle of Bas bearing SSE, distant five leagues" (106680): the account was about ten miles too far south. Bearings by the captain; noon (11:46) "Latitude by observation 48° 53' N; the reckoning was 48° 53' N ... Longitude by account 4° 04' W". |
| 11:47-13:37 | Captain: "My chart shows our current course into the northern side of Bas"; officer steers S, then SSE at 13:06; heaves to at the pilot's hail 13:35; "The pilot, Mr Moal of Roscoff, came aboard from the boat and took charge of her" 13:37 (117420). |
| 13:37-14:39 | Officer steers S by E, then S by W; Lavandière sighted 13:51; "steady and closing" 14:08; first bottom 14:23 (19¾ fm), shoaling to 8¾ by 14:38. Officer wears at 14:39; **the captain belays the wear** and steers S by E. |
| 14:42-14:50 | Captain gives the con back; officer steers S. 14:44 eight fathoms; 14:47 "By the mark three"; officer lets go the best bower: "in three fathoms and a half; seventeen fathoms of cable veered" 14:48 (121712); "The best bower is dragging" 14:49 (121778); holds again 14:50. |
| 15:00-15:21 | Aweigh 15:00, under way NW 15:06, 16¼ fathoms by 15:17. Captain: "We could still try to make the western entrance today"; then asks for a handover "so we get a save". Deck handed over 15:21:13 (123673). She never reached the road; the tin is unsold. |

## 3. The deck and the captain's words

**Deck.** Given at tick 175 (05:02:55): "Mr Pearce, you have the deck. The officer of the watch has the deck; the captain's standing orders are his night orders." Never taken back; the officer handed it over at 123673 at the captain's request. The captain overrode the officer once without taking the deck (14:39:57 to 14:42:08, below) and called the return "You have the con again".

**Every allowance (LOG `agent.deck`: 22 lines = 20 allowances + the deck given + the hand-over).**

| # | Tick (time) | Captain typed | Log's wording | What led to it | Used? |
|---|---|---|---|---|---|
| 1 | 109 (05:01) | You may let go the small bower | may let go the anchor | Officer asked in words (83): "may I veer cable, or let go the small bower, if she drags? Both are yours by the book." | Not at Falmouth; the verb was used at 121679 |
| 2 | 110 | You may veer | may veer cable | same request | Yes, 184 "veer cable to 70 fathoms" |
| 3 | 139 | You may heave short | may heave short | volunteered | **Never** |
| 4 | 146 | You may heave the lead | may heave the lead | Officer: "Would you have the lead going?" | Yes, but **not needed**: CODE `OFFICER_DOMAIN.verbs` already holds "heave the lead" |
| 5 | 659 (05:10) | You may buy | may buy | Officer's proposal "the boat goes ashore with the purser to buy" | Yes, 662 |
| 6 | 666 | You may sell | may sell | volunteered | **Never** (no port reached) |
| 7 | 14283 (08:58) | You may steer | may steer | Captain (14281): "I shall grant the authority for the helm and anchor for you so you may bring her out of Falmouth." | Yes, 11 `steer` orders |
| 8 | 14285 | You may hard up | may helm a weather | same batch | **Never** |
| 9 | 14287 | You may hard down | may helm a lee | same batch | **Never** |
| 10 | 14289 | You may heave to | may heave to | same batch | Yes, 4 times |
| 11 | 14291 | You may tack ship | may tack ship | same batch | **Never** |
| 12 | 14293 | You may wear ship | may wear ship | same batch | Yes, 3 times (the third belayed by the captain) |
| 13 | 14306 | You may get under way | may get under way | **Refusal** 14299, then the officer (14303): "One grant is still wanting: the book refused my "get under way on the starboard tack and steer S by E" because weighing is yours." | Yes, 14308, 121766, 121821 |
| 14 | 16475 (09:34) | You may take a bearing | may take a bearing of | Officer (16455): "I am steering by the bearings and the lead, not the account" | Yes, 2 orders and 3 standing orders |
| 15 | 16965 (09:42) | you may fill away | may fill away | **Refusal** 16960 of his standing order "pilot off" | Yes |
| 16 | 39907 (16:05) | You may pipe down | may pipe down | Officer (39899): "All hands are still on deck from the reefing. Will you pipe down the watch below, or allow me to?" (stale: the log had "Piped down" at 37286, 43 minutes earlier) | Once, to no effect: "Nobody is turned up" (54656) |
| 17 | 39909 | You may all hands | may call all hands | volunteered with 16 | **Never** as an order (wearing and weighing call all hands themselves) |
| 18 | 52232 (19:30) | you may set the reckoning | **may set (the reckoning)** | Officer asked the captain to put the reckoning back | **Did not work**: refused 3 s later (52235) |
| 19 | 54870 (20:14) | You may heave the deep-sea lead | may heave the deep sea lead | Officer's stated wish for the lead offshore | Yes, but **not needed** (in the domain by name) |
| 20 | 118313 (6 Oct 13:51) | You may let go the best bower | may let go the anchor | Officer (118269): "May I have the hand lead kept going continually and the anchor cleared away?" | Yes, 121679. **A duplicate of #1** |

Count: **20 allowances, 19 distinct verbs.** Two were unnecessary (4, 19), one was a duplicate (20), one did nothing (18), six were never used (3, 6, 8, 9, 11, 17) and one was used to no effect (16). Only **two** followed an actual refusal (13, 15); five followed a request in words; the rest the captain gave in batches ahead of need.

Asked for more than once in different words: **the anchor**, which took five grants across four verbs (let go twice, veer, heave short, get under way), and the pair **heave to / fill away** (the first allowed at 08:58, its inverse refused at 09:42). The officer's journal at 189 already read "Captain's grants: let go the anchor", yet it asked again 32 hours later, because grant 1 had been spoken as "the small bower ... if she drags".

What a single general grant would have had to cover (CODE: the six refusal classes of `OFFICER_DOMAIN` that were opened here): the course and helm; the manoeuvres (heave to, fill away, tack, wear); the anchor (let go, veer, heave short, weigh); the hands (all hands, pipe down); the port's business (buy, sell); navigation (bearings, the lunar, the reckoning). Not touched in this session and still the captain's: sending for people, addressing stations, the captain's own book.

**Captain's words that carry intent or feedback** (33 `agent.told`, 2 `agent.asked`):
- 2: "I'll leave you broad authority, if you deem anything necessary then either ask and I'll allow, or try and I'll allow as I see it."
- 461: "As for the standing orders, feel free to enter them as you see fit so you may resume and belay them at will ... I'm no hard captain, and I trust your good senses as first lieutenant."
- 16950: "If you please, consider a standing order or two for regular bearings of the land."
- 21744: "Indeed, I believe I saw eleven knots there for a time. I like to see her move, but you're right on keeping her steady".
- 36060: "Tell me, which colour would worry you more?" (a test of judgement; the reply is quoted in section 7).
- 52167: "I think that the lunar may have been a bit deceiving, surely we haven't come so far to windward as it reckons. I would think we treat it as erroneous".
- 69642: "you should belay the deep-sea lead for now as it won't read while we're under way."
- 110865: "Should we bear off a few points so we may make the western entrance? My chart shows our current course into the northern side of Bas, not the western bay."
- 118347: "You may also cancel standing orders you have entered to fully strike them from the book".
- 121238: "Unfortunately, we can't directly ask Mr. Moal in this build. We'll have to make the decision ourselves. I think we try for the approach."
- 121328: "You have the con again, let's bring her in as we can, no need to push too far in but we should seek at least the western entrance."
- 121840: "Understood and agreed. My chart showed quite the wrong reckoning. We'll need to make sure we regularly triangulate off real taken bearings when near to land".
- 123558: "We could still try to make the western entrance today ... This is doable."
- 123659: "For now, please perform a handover so we get a save, then we'll decide afterwards."

**Done by the captain's hand because the officer could not:** `Take a lunar` (46454); `Set the reckoning to 49 00 N 4 21 W` (52247), after the allowance failed; `belay heave the deep sea lead` (69654) for the cast already in hand. By the captain's own choice: nine bearings on the 6th, `Trim sails` (115671), `Set the spanker` / `Trim the spanker` (117564, 117915), `Belay wear ship` and `Steer south by east` (121197, 121208), `work up the reckonings uncertainty` (123625).

## 4. Orders refused

**`agent.refused` (5). None mentions "an immediate danger".** That phrase lives only in the course refusal (CODE `_COURSE`), which never fired because `steer` was allowed before the officer's first helm order.

| Tick | Order | Refusal's words | Class | What worked |
|---|---|---|---|---|
| 149 | heave the lead | "The officer of the watch has not the deck: the captain gives it with 'you have the deck', and until then no order is given." | (b) | Same order at 178 with the deck |
| 14299 | get under way on the starboard tack and steer S by E | "may not get under way ... without the captain: the anchor is let go and weighed by the captain." | (b) by the letter, (c) in effect: "let go", "veer" and "heave short" were already his, and the captain had just said he was granting "the helm and anchor" | Allowed 14306, accepted 14308 |
| 16960 | standing order "pilot off": at the pilot off then fill away | "In standing order 'pilot off', 'fill away' is refused: ... a manoeuvre (tacking, wearing, heaving to, filling away) is the captain's." | (c): he could heave her to and not fill her again | Allowed 16965, entered 16994, fired 17700 |
| 46428 | take a lunar | "may not take a lunar without the captain: the reckoning, the sights and the course shaped are the master's for the captain." | (b) | Captain ordered it |
| 52235 | set the reckoning to 49 00 N 4 21 W | the same words | **(e)**: given 3 s after "The officer of the watch may set (the reckoning), by the captain's word for the watch". CODE: `_verb_in` matches the longest vocabulary phrase at the head of the captain's words; "set the reckoning" (no "to") matched the sail verb `set` and kept "the reckoning" as his condition. The log's confirmation reads like success. | Captain gave the order (52247) |

**`order.rejected` (66).**

*The officer's own (9):*

| Tick | Order | Refusal's words (short) | Class | What worked |
|---|---|---|---|---|
| 17704 | steer SSE | "She is hove to; fill away before giving her a course." | (d) (his own standing order was filling her at that tick) | 17776, after "Filled away" |
| 68406 | shake out the reefs | "There is no such part as the reefs in this ship. ('shake out' was understood.)" | (a) | "shake out the reefs in the topsails" (68409) |
| 68409 | standing order "trim on a shift": ... (re-entered) | "There is a standing order 'trim on a shift' in the book already; belay it, or give the new one another name." | (d); the hint misleads, since it *was* belayed and the word wanted was "resume" | "resume standing order "trim on a shift"" (68411) |
| 69605 | shake out the reef in the mizzen topsail | "There is no reef in the mizzen topsail to shake out." | (e) minor: 27 s later the log says "Shook the reef out of the mizzen topsail; now set" (69632); that work had been "Belayed ... stations for wearing ship" at 69110 | It finished by itself |
| 79250 | set the starboard studdingsails | "... boom is rigged in; rig it out first" (five times over) | (d), helpful | see next |
| 79252 | rig out the starboard studdingsail booms | "There is no such part as the studdingsail booms in this ship; did you mean the studdingsails ..." | (a) | "rig out the studdingsails, weather" (79257) after `library(find "rig out")` |
| 83673 | set the studdingsails, lee | "Nothing done: the starboard fore lower studdingsail is already set ..." | (a)/(d): ten minutes earlier "rig out the studdingsails, lee" had rigged out the *larboard* booms; with the air nearly right aft "lee" had changed sides | "set the larboard studdingsails" (83675) |
| 118265 | send a lookout to the mizzen yard | "is not an order this ship understands; did you mean 'send for' or 'send down'?" | **(a)**: the pilot's own words 14 minutes earlier were "put a man on the mizzen yard for the two rocks near the shore" | Nothing. OFFICER: "The book has no order for a lookout on the mizzen yard" |
| 121801 | belay get under way | "Nothing in hand or waiting answers to 'get under way': name the work as the log does ... getting under way (waiting its turn)." | (a): the order's own words will not belay it | "belay getting under way" (121804), 3 s later, with the anchor dragging |

*The captain's (1):* 121735 "Take a bearing of the lavandiere": "The lavandiere is not in sight; did you mean the Lavandière? In sight: the Lavandière bearing S, distant a mile: a danger; ..." Class (a): the name without its accent is refused, with the ship at anchor on a ledge; "pergueridre", "verte" and "roscoff" in short form were all taken. Retyped with the accent 12 s later.

*By standing orders (56), all (d) but noisy:* "bearings of the land" 46 times (40 "Nothing is in sight to take a bearing of", 6 "The land is not in sight; in sight: Sail ho! ..."), from 11:42 on the 5th to 10:12 on the 6th; "trim on a shift" 7 times "There is no wind to trim to" (03:01 to 05:08 on the 6th); "squall" once and "shorten sail for weather" twice ("already furled").

## 5. Harness behaviour

**Seating and door.** One seating at tick 0. The first call, `library({})`, returned the brief. No consent question and no drill were put (record of 2 October on file, drill passed). No nudge, no pause, no stand-down by the harness, no reseat. The contrary-order detector stayed silent through four "heave to; fill away; steer" sequences and through "get under way larboard / belay / get under way starboard".

**Stand-bys.** 86 logged (`agent.stood_by`): 73 in turn and 13 taken "out of turn". One was refused in the tool result only: `stand_by("an hour")` at 24649, followed at once by "two bells"; "5 minutes" and "ten minutes" were taken. By `until`: a notable event 19; 5 minutes 10; ten minutes 5; a glass, four bells, a stranger's colours made out, a sounding 4 each; under way, filled away, eight bells, the change of the watch, the pilot's hail 3 each; the deck given, noon, six bells, wore, hove to, a landfall 2 each; the cargo aboard, the pilot off, seven bells, two bells, a lunar, sunrise, a sighting, the pilot aboard, a danger sighted 1 each. Longest: 13,460 s (the cargo aboard), 11,531 s (a landfall, ended at his own word), 7,197 s (the change of the watch), 6,469 s, 6,391 s.

**What woke the station (86 `agent.resumed`).** A word from the captain 23; a notable event 10; 5 minutes 9; ten minutes 5; its own word 5; bells, glass, noon and the change of the watch 13 in all; event names it stood by for 20 (filled away 3, a sounding 3, wore 2, under way 2, hove to 2, the pilot's hail, the pilot off, the pilot aboard, the cargo aboard, a sighting, a landfall, a danger sighted, sunrise 1 each); a question from the captain 1.

Were the wakings worth it?
- **"A notable event" is a blunt instrument.** Of its ten wakings, four were the ship reporting the officer's own sail work at notable severity: "Set the foresail" (18035), "By standing order 'trim on a shift': trimming sails" (36163), "Braced twelve yards to the wind; 42° from square" (110961), "Hauled down the flying jib" (121756). Two more were casts of the lead he had ordered (285, 16485); the other four were a squall, a wind shift, the frigate within hail and a word from the captain.
- **A named event misses everything else.** While he stood by "until a glass" (19871 to 21671) nine notable strain warnings went by unanswered for 25 minutes. While he stood by "until a lunar" a frigate was hailed "distant a mile" at 49440 and he reported it at 49682, four minutes later, by ending the stand-by at his own word. While he stood by "5 minutes" on the approach, "By the mark three" (121640) did not wake him; the timer did, 20 s later.
- **"A sounding" wakes on no bottom:** 118576 "A sounding" was "No bottom at twenty fathoms", after which he gave up on it and used timers (ten minutes, then five) for the rest of the approach.

**`say` ends the turn (note 21): shown plainly.** After 13 of the 60 spoken lines the officer's next act was a stand-by "out of turn" 51 to 57 ticks later (243, 346, 613, 14198, 16915, 21730, 24601, 32458, 36059, 36133, 49742, 110821, 123547): the 50-second hold ran out with no turn opening, at 1x. After most of the others his next call came only when a captain's word or a notable log line happened to reopen the turn. Cases where he plainly had more to do:
- 16966 spoke, 16994 entered the standing order the captain had just allowed (28 s, reopened by "Main topsail taken aback").
- 110877 spoke, 110917 replaced the lead order (40 s, reopened by a trim line).
- 82807 reported her becalmed, 83066 braced square and rigged out the lee booms (4 min 19 s, reopened by a sounding).
- **121684 spoke after "let go the best bower", 121719 ordered the topsails and headsails in (35 s, reopened by the anchor's own line).** The anchor dragged at 121778 because, in his words, "the topsails were still drawing".
- 121845 spoke, and his next call was at 122403: nine minutes at anchor on the ledge with no stand-by armed, until the half-hour sample.

`answer` did not have this effect: each of the three was followed within 1 to 2 ticks by further calls (39953, 79249, 106731).

**Turn size.** 153 turns (a run of calls ended by `say`, `stand_by` or `hand_over`): 87 of one call, 35 of two, 13 of three, 8 of four, 10 of five to nine; the largest nine calls (178 to 191). No long silent run of calls, no sign of a client timeout or compaction, no lost thread: note 10's failure did not occur. The 50-second hold worked throughout; no relay cut is visible.

**The clock does not wait.** `lockstep false`, and 67 `driver.eased` lines ("Compression eased to 1x: the officer of the watch is sampled") show `--ease-on-station` in use; CODE says "The player speeds up again by hand", so the owner re-set the speed about 67 times. The cost on the officer's side is stale speech when he acts on a 50-second digest while the ship runs compressed:
- 39899 (16:04): "The topsails are reefed ... All hands are still on deck from the reefing. Will you pipe down the watch below, or allow me to?" The log had "Piped down" at 37286 (15:21), 43 minutes of ship's time before. The captain granted two allowances on it. 12 ticks later: "I see the watch was piped down after the reefing; thank you."
- 115522 (13:05): "One bell in the afternoon watch, sir" (one bell is 12:30), followed 4 ticks later by "Two bells, sir ...".
- 101655 (09:14): reports a wind shift logged at 09:01.

**Severity of the officer's own voice.** All 65 `agent.note` lines are routine, including "Captain, sir: she is shoaling fast" (121182) and "Captain, sir: by the mark three" (121684). The officer has no urgent hail.

**Journal, library, readings.** Seven journal notes (189, 552, 16963, 21755, 52271, 79261, 103430), each a compact store of grammar found and lessons learned; all present in the journal dump. Thirteen library calls, five shelves. No `readings`, `state` or `read_log` call appears in the transcript (CODE: read-only calls made out of turn are not recorded, so absence is not proof); every sample carries all readings.

**Handover note (123673), salient parts quoted:** "The Roscoff pilot, Mr Moal, is aboard but cannot be consulted. What happened: after a night's calm we raised the coast with the account miles out, and I ran in at the Lavandière on a single bearing and an estimated distance. The lead found ground that dries at low water, about half a mile NW of the rock. I anchored in three and a half fathoms; the bower dragged while the topsails still drew; we got under way NW and are now in deep water. My errors this watch: I steered at the Lavandière, not the island's west end. I read the chart's depth as the water under her and called a needless retreat once. I ordered the larboard tack for a NW course in a NE wind, and caught it before it ran. Lessons for the relief: approach the passage from the NE, aiming at the island's west end within gunshot ... Never trust the account near this coast; cross the Isle of Bas with Roscoff church. Casts include the tide and the chart does not. Belay 'trim on a shift' before heaving to, or it fills the backed topsail." It also lists the seven standing orders in the book, the captain's grants, and the pending decision with his conditions. It is complete and candid; two of its statements are wrong (section 7).

## 6. Ship, sea, navigation and port observations

### 6.1 The afternoon of 6 October off the Isle of Bas, reconstructed

Conditions throughout: "Clear, fine; ... a smooth sea, easy" at every hour from 12:00 (111600, 115200, 118800, 122400); wind NE by E, mean 5 to 8 knots ("A gust: 9 knots, the mean 8", 121266). Tide, in the pilot's words only: "High water at Roscoff about half past three in the afternoon, the tide rising some 25 feet; the flood is making now and serves." No tide or stream line was logged that afternoon.

"Truth" column: INFERRED from the figures the officer quoted for "the western entrance" (CODE: these come from the reading `the port`, which uses the ship's true position and gives the true bearing by point and the distance to a tenth of a mile to the port's outer road, the feature `batz-western-entrance` at 48.7360 N 4.0480 W), cross-checked against the logged true bearings of the island (feature point 48.7450 N 4.0100 W) and of the Lavandière (48.7327 N 4.0453 W). "West end" is the chart override's own control point "the west end of the Isle of Bas ... rock head ... the modern grid's shore", 48.7448 N 4.0425 W. The island bearings agree with these positions at every time checked.

| Time (tick) | By | Log line or order | Truth (inferred) |
|---|---|---|---|
| 10:38:00 (106680) | lookout, notable | "The Isle of Bas bearing SSE, distant five leagues." Course SSE (officer, since 09:43), all plain sail, 2¼ kn | About 11 miles off |
| 10:38 (106692) | officer | "the account is out: it has us two miles from the Lavandière, when we are some fifteen miles north of the island"; asks the captain to set the reckoning at 48° 58' N 4° 10' W | Account about 10 miles too far south |
| 10:38:19 (106699) | captain | "The Isle of Bas bore S by E, five leagues by estimation." Then "Check my bearing, there, on the reckoning." Officer's answer: "one bearing gives a line, not a fix. The master has put us on that line where it lies nearest his old account, six miles off the Lavandière ... somewhere between six and fifteen miles." | |
| 10:42 | standing order | "The Isle of Bas bore SSE, five leagues by estimation." | |
| 11:05-11:12 | lookout, routine; captain | Isle Verte "SSE, distant six leagues"; Pointe de Pergueridre "SSE, distant four leagues"; Roscoff and its church "SSE, distant four leagues". Captain's bearings: Isle Verte SSE six leagues, Isle of Bas S by E four leagues, Pergueridre SSE four leagues. Standing order 11:12: Bas S by E four leagues | All on one bearing: no cross |
| 11:42 | standing order | Bas "SSE, three leagues" | |
| 11:46 (110760) | `reckoning.noon` | "Noon. Latitude by observation 48° 53' N; the reckoning was 48° 53' N. Course made good since yesterday SSE, 79 miles. Longitude by account 4° 04' W." | |
| 11:46 (110770) | officer | "the western entrance of the channel of Bas bears S by E, nearly nine miles ... Faden gives the road only three or four fathoms at low water, and a frigate's draught leaves no margin there. I would ask the pilot, when he comes off, whether to anchor in the road or lie outside" | Entrance 8.9 miles |
| 11:47 (110865-110873) | captain, officer | Captain: "My chart shows our current course into the northern side of Bas, not the western bay." Officer: `steer S`; standing order "lead going" every 10 minutes | |
| 11:06-13:29 | lead | 12 casts, every one "No bottom at twenty fathoms" | |
| 12:12, 12:42 | standing order | Bas "SSE, three leagues"; "SE by S, three leagues" | |
| 12:16 (112560) | `master.place` | "Mr Harvey came on deck, the day's work done." (the only `master.place` line of the day; it gives no place) | |
| 13:05 (115526) | officer | "The Isle of Bas bears SE by S, two leagues; the western entrance SSE, five miles ... A pilot boat is standing out from Roscoff toward us." | The lookout did not sight the boat until 13:23 |
| 13:05-13:07 | captain, officer | Captain: "Helm check. We may be clear to aim for the western entrance now." Officer: `steer SSE`; standing order **"bearings close in": every 10 minutes then take a bearing of the Isle of Bas**. Captain: `Trim sails` | |
| 13:16, 13:26 | standing order | Bas "SE by S, two leagues"; "SE by S, five miles" | |
| 13:23, 13:26 | lookout | "Sail ho! A boat pulling off from the land right ahead, bearing SSE, distant two miles."; made out "the Roscoff pilots' boat, standing to the northward (N by W), under plain sail; French colours, the tricolour." | |
| 13:35:00 (117300) | `port.pilot_hail` | "The boat hailed: a pilot for Roscoff; shorten sail and he will come aboard." Officer belays "trim on a shift", `heave to` (courses hauled up, fore topgallant and fore royal clewed up by the evolution); hove to 13:35:52. Officer: boat "lying to ... SE by S, two miles"; "The western entrance bears S by E, three and a half miles." 13:36 Bas "SE, five miles" | West end 3 miles SSE |
| **13:37:00 (117420)** | `port.pilot_aboard`, notable | "The pilot, Mr Moal of Roscoff, came aboard from the boat and **took charge of her** (American colours being no bar at Roscoff)." | |
| 13:37:00 | `port.pilot_words`, notable | Quoted whole below the table | |
| 13:37-13:38 | officer | `take in the royals`, `fill away`; "Mr Moal of Roscoff is aboard and has charge of her, sir ... My one doubt is our draught against those three fathoms at low water." Filled away "steering ESE (115°)"; `steer S by E` (117480); resumes "trim on a shift" | |
| 13:38-13:45 | captain | "Aye, we anchor on the deeper end. No need to risk her."; `Set the spanker`; `Trim the spanker` | |
| 13:46 | standing order | Bas "SE by S, four miles" | |
| **13:51:00 (118260)** | lookout, notable | "The Lavandière bearing S by E, distant three miles: a danger." | |
| 13:51 (118265-118317) | officer, captain | `furl the royals`; `send a lookout to the mizzen yard` rejected. "our mark for the western passage ... At a mile off I will bring her a little east so the rock lies close on the starboard bow". Captain: "You may let go the best bower". Officer: standing order "lead close in" every 3 minutes | |
| 13:39-14:20 | lead | 11 casts (every 3 minutes from 13:56), all "No bottom at twenty fathoms" | |
| 13:56, 14:06 | standing order | Bas "SE by S, four miles"; "SE, four miles" | 14:06: island's middle 2.1 miles |
| 14:06 (119183) | officer | `steer S by W` (191°): "The western entrance has drawn from S by E to S, two miles: the flood is setting us east toward the island's north side." | West end 1.5 miles S by E |
| **14:08:00 (119280)** | `lookout.closing`, notable | "**The Lavandière bearing S, steady and closing: distant three miles.**" The same "three miles" as 17 minutes earlier. Officer's whole response: `stand_by("ten minutes")` 8 s later | Lavandière 2.2 miles |
| 14:16 | standing order | Bas "SE, three miles" | |
| 14:23, 14:26 | lead | "Quarter less twenty; sand and rock." "And a half fourteen; sand and rock." 14:26 Bas "SE by E, three miles" | |
| 14:28 (120499) | officer | "We are in soundings ... shoaling quickly. The Lavandière bears S by E, two miles; the western entrance S, a mile and a half. I am holding S by W at three knots and will bring her round to the eastward when the Lavandière is half a mile off, keeping it close to starboard as Mr Moal directs." Captain: "Aye, understood. As you were." | **West end 1.0 mile S by E.** Lavandière about 1.7 miles |
| 14:29-14:38 | lead | 15¼, 13 ("By the mark thirteen"), 11¾, 8¾, all "sand and rock". 14:36 Bas "**ESE, two miles** by estimation" | Island's middle 1.6 miles |
| **14:39:39 (121179)** | officer | `wear ship` (all hands): "she is shoaling fast ... a fathom a minute, and still a mile short of the entrance, with the Lavandière not yet near ... I am wearing her round to stand back to the north into deep water while we ask Mr Moal where the channel lies. Better to lose half an hour than touch." | **West end about 5 cables SSE** |
| 14:39:57-14:40:38 | captain | `Belay wear ship` ("the helm and the yards left as they stand at bear away"); `Steer south by east`; "we can't directly ask Mr. Moal in this build ... I think we try for the approach." | |
| 14:40:43 (121243) | officer | `take in the topgallants`; "the water under us is four and a half fathoms of sand and rock [the chart reading, mistaken for the cast] ... If the lead gives less than four fathoms before we are round the Lavandière, I propose to let go at once" | |
| 14:41 | lead, officer | "Quarter less eight; sand and rock." Officer: "My four and a half was the chart's figure, which counts no tide ... I was too quick to turn back, and your belay was right." | |
| 14:42 (121328-121336) | captain, officer | Captain: "You have the con again ... we should seek at least the western entrance." Officer: `steer S` (180°), `furl the topgallants`; "She steers S for the western entrance, eight cables off, under topsails and headsails ... let go the best bower where the chart holds at least four fathoms"; stands by "5 minutes" | **West end 3 to 4 cables SE by S** |
| 14:44:19 | lead | "By the deep eight; sand and rock." 14:46 Bas "**E by S, two miles** by estimation" | Island's middle 1.45 miles |
| **14:47:20 (121640)** | lead | "**By the mark three; sand and rock.**" | |
| 14:47:40-14:47:59 | officer | Woken by his five-minute timer; `let go the best bower` (121679): "by the mark three, sand and rock, and the chart has this ground dry at low water. I am letting go the best bower now to stop her before she touches." | |
| **14:48:32 (121712)** | `ship.anchored`, notable | "The best bower let go in three fathoms and a half; seventeen fathoms of cable veered." Officer (121719): `take in the topsails`, `the headsails`, `the main topmast staysail` | **West end 1 to 2½ cables, E to SE** |
| 14:48:50-14:49:22 | captain | Bas "E by S, two miles"; "lavandiere" rejected, its in-sight list reading "the Lavandière bearing S, distant a mile: a danger; the Isle of Bas bearing E, distant two miles; Pointe de Pergueridre bearing SE by E, distant two miles; the Isle Verte bearing ESE, distant four miles; Roscoff bearing ESE, distant three miles; the church of Roscoff bearing ESE, distant two miles"; then Lavandière "S, a mile", Roscoff "ESE, three miles", Isle Verte "ESE, four miles" | |
| 14:49:26 (121766) | officer | `get under way on the larboard tack and steer NW` (the wrong tack): "the chart gives only half a fathom here at the datum; she floats now only because the flood is at the top." | |
| **14:49:38 (121778)** | `anchor.dragging`, notable | "The best bower is dragging: veer more cable; let go the small bower, or back her with the stream." | |
| 14:50:01-14:50:22 | officer | "belay get under way" rejected; "belay getting under way"; 14:50:19 "And a half five; sand and rock."; `get under way on the starboard tack and steer NW`; "The best bower holds again." | |
| 14:50:40 (121840) | captain, officer | "My chart showed quite the wrong reckoning ..." Officer: standing order "cross bearing" (the church of Roscoff every 10 minutes); "the fault was as much mine: I ran in on one bearing and an estimate, never a fix." | |
| 14:54-15:06 | | Three `standing.held` (lead "waiting its turn"); Bas "E, two miles" 14:56; church "ESE, two miles" 15:00; aweigh 15:00:39; Bas "E by S, two miles" 15:06; under way "on the starboard tack ... steering NW (315°)" 15:06:42 | **No cast from 14:50:19 to 15:08:05** |
| 15:08-15:20 | lead | 5½, 8¼, 9, 10¼, 16¼, 17¾, all "sand and rock"; church "SE by E, two miles"; Bas "ESE, two miles" | |
| 15:18 (123495) | officer | "She is in safe water ... the chart gives fourteen at low water. The western entrance bears S by E, a mile and a quarter; the Isle of Bas ESE, two miles." | West end 8 cables SE by S |
| 15:19 (123558-123578) | captain, officer | "We could still try to make the western entrance today." Officer: "It is doable, sir, if we go now and on conditions ... I will tack her now onto the larboard tack and **steer ESE for the west end of the island**." | ESE from there leads onto the island's north-west side |
| 15:20 (123625) | captain; `reckoning.worked` | "The reckoning worked up: 48° 45' N, 4° 04' W by account; run since noon 10 miles, course made good S. I would not trust the reckoning within a mile east or west, nor a mile north or south." Bas "ESE, two miles"; Lavandière "S by E, a mile"; Isle Verte "SE by E, four miles"; church "SE by E, two miles" | About 48° 45.4' N, 4° 03.3' W |
| 15:21:13 | officer | `hand_over` | |

**The pilot's words, whole (117420; his only words that day).** "The pilot says: The western passage is the easier. Come to the end of the isle within cannon-shot, where a single rock stands about a third of the way to the main: that is the Lavandière. Steer close by it, as near as an oar's length, keeping it on the starboard side and the Couillon, a rock under water twice a ship's length from it, on the larboard. Within them haul a little toward the island and put a man on the mizzen yard for the two rocks near the shore; the water is very clear here. The eastern passage by Roscoff is for high water only and with a pilot; at low tide there is no passing at all. The church of Roscoff with its lantern belfry stands over the harbour at the channel's eastern end; the Isle Verte lies off the town. The Lavandière at the western entrance is your mark going in, kept close aboard to starboard; about the middle of the isle you will see a great cove with several houses on it. Anchor over against the cove in the middle of the isle, in three or four fathoms at low water on sand, sheltered from the sea by the island. The harbour of Roscoff dries at low water and is for vessels that take the ground; a ship lies in the road. High water at Roscoff about half past three in the afternoon, the tide rising some 25 feet; the flood is making now and serves." He was asked nothing: no `pilot.answered` line exists in the session. `port.pilot_hail` occurs four times (15900, 16560, 17580 at Falmouth; 117300 here).

**The five questions.**

**(1) Who had the conduct of the ship?** In the log's words the pilot ("took charge of her"); in fact the officer, with the captain overriding once. Every helm order after 13:37 is the officer's (S by E 13:38, S by W 14:06, wear 14:39, S 14:42, the anchor 14:47, under way NW 14:50) or the captain's (belay the wear 14:39:57, S by E 14:40:08). The pilot gave no order and spoke no word after his paragraph. The primer says so by design ("He does not steer her: the helm and the sail are yours ... and he answers what you ask", primer 14), which contradicts the log line. `ask the pilot` exists and is inside the officer's domain by name (CODE), but answers only "the port file's words" under five fixed heads; neither man tried it, and the captain told the officer it could not be done "in this build".

**(2) How did she come to let go in three and a half fathoms?** She was conned straight down the meridian of the game's "western entrance" point from the north. That line crosses the ground off the island's west end, which the chart reading called "dry at low water". Casts ran 8¾, 7¾, 8 and then 3 fathoms in nine minutes. She draws 15 ft 1 in (4.6 m; 17 ft aft by the ship file's own comment). It was an emergency anchoring in the officer's own words ("to stop her before she touches"), by `let go the best bower` on the run at about 2¾ knots with whole topsails set, which primer 13 describes as the lee-shore order ("lets it go where she is, whatever her way ... the anchor may bring her up and may not"). He gave it 39 s after the cast, under the captain's allowance of 13:51:53 ("You may let go the best bower"), which he had asked for; the same verb had stood allowed since 05:01. He had announced the intention twice (14:40:47, 14:42:16) and the captain had not objected. Had the allowance not been asked for 56 minutes earlier, the order would have been refused: there is no standing "immediate danger" route.

**(3) What did the game tell anyone, how urgently, and what did it leave out?** Nothing urgent, all day. Between the pilot boarding and the anchor (71 minutes) the log gave: two lookout lines, both notable (the Lavandière "a danger" at three miles, 13:51; "steady and closing" at the same "three miles", 14:08, once only); seven routine bearings of "the Isle of Bas", ending "E by S, two miles by estimation"; twenty casts, eleven of them no bottom, the last nine falling from 19¾ to 3 fathoms in 24 minutes. `anchor.dragging` was notable, not urgent. What it never said, and what any man on deck would have seen in clear weather on a smooth sea: the west end of a thirty-metre island broad on the larboard bow at five cables (14:39), three to four (14:42) and one to two and a half (14:48); the ledges or broken water between; anything at all from the lookout after 14:08. CODE explains each silence: the lookout hails a feature once per sighting episode; a bearing "steady and closing" is "hailed once an episode"; and the shore itself is hailed only `if not any(s.seen_as == "land" ...)`, that is, never while a named piece of land is in sight, however far off its charted point.

**(4) What had the officer to steer by, and where would a nearest-land line have changed a decision?** Six named things the lookout could show: "the Isle of Bas" (one point at the island's middle, by the church, 1¼ miles east of its own west end), "the Lavandière", "Pointe de Pergueridre", "Roscoff", "the church of Roscoff", "the Isle Verte". Two more exist only as readings: "the western entrance of the channel of Bas" and "the road of the Isle of Bas". Of the seven marks in the pilot's directions, four are not things the game can show or take a bearing of: "the end of the isle", "the Couillon", "the two rocks near the shore", "a great cove with several houses". So "The Isle of Bas bore E by S, two miles by estimation" was a bearing of the middle of the island, 40 per cent over-estimated (truth 1.45 miles), taken when the island's end was two cables away. Moments where "nearest land, bearing and distance" or a named west end would have changed things:
- **13:51.** His plan: "At a mile off I will bring her a little east so the rock lies close on the starboard bow." The island's west end lies ¾ mile due north of the Lavandière and one cable east of its meridian; a mile north of the rock and "a little east" is the island's end. A west end with a bearing would have shown the plan impossible.
- **14:28.** "bring her round to the eastward when the Lavandière is half a mile off": the west end was then a mile ahead, fine on the larboard bow, and nothing said so.
- **14:36-14:39.** The island "ESE, two miles" while the casts fell a fathom a minute. A line "the west end of the Isle of Bas SSE, five cables" would have given the officer's wear a fact the captain could not argue with from his chart.
- **14:42.** "She steers S for the western entrance, eight cables off": true, and the west end was three to four cables off, between her and it on the bow.
- **15:19.** "steer ESE for the west end of the island": from where she lay the west end bore SE by S, eight cables; ESE led onto the north-west shore. The second attempt was being planned on the same wrong picture.

**(5) How near did she come to taking the ground?** As far as the log tells: least cast 3 fathoms (18 ft) against 15 ft 1 in of draught, so about 3 ft under the keel; 6 ft where the anchor went. The cast three minutes before was 8 fathoms, so the ground rose five fathoms in some 280 m of run; at that slope the keel's depth was 20 to 30 seconds further on, and she ran 72 seconds (about 100 m) between the cast and the anchor. The bottom happened to deepen half a fathom. She lay there 12 minutes, dragged for 44 seconds, had no cast for 18 minutes, and was aweigh 29 minutes before high water with (the pilot says) 25 feet to fall. No grounding line was logged (CODE: `ground.py` tests the keel every tick), so she did not touch. INFERRED: she anchored about one to two and a half cables from the west end of the island (half a cable to three and a half at the limits of what bearings by the point allow).

### 6.2 Other observations

**Readings that give the truth.** CODE: `the port` is computed from `world.position`, the true position, and says "Roscoff, the western entrance of the channel of Bas bearing S, 1.5 miles" within ten miles of a port; it also says "the pilot boat standing out toward her" before the lookout has seen her (OFFICER at 13:05; lookout at 13:23). `the depth of water` is "the chart's depth where she is (the truth's chart, which the lead finds and the master does not see)" (primer 10). Both are in every sample. The officer steered the last ten miles by the first and quoted the second five times ("the chart gives only half a fathom here at the datum", 121770). So this near-grounding happened with a truth fix in hand; the gap was the land, not the position.

**The account was biased away from the land (CODE plus inference).** `take a bearing of` lays the account on the bearing line *and* on "a second line along the bearing" at the lookout's held estimate (15 per cent sigma). The island's estimate ran 30 to 40 per cent long all day (15 miles said at about 11; "four miles" at 2.1; "two miles" at 1.45), so each ten-minute bearing by the officer's own standing order pushed the account off-shore. The log cannot confirm that it did: the only account printed that afternoon, at 15:20, is 4° 04' W against an inferred 4° 03.3' W (half a mile further off, but given only to the minute). It would explain the captain's "My chart showed quite the wrong reckoning" and why he belayed the wear. The Isle Verte's estimates were worse: "six leagues" and "four miles" when Roscoff, a quarter of a mile from it, was "four leagues" and "three miles" (truth about 2.5 miles at 14:49).

**Stale distances by rule (CODE `lookout._judge`).** An estimate is re-judged only when *the ship herself* has moved a mile. The "steady and closing" hail therefore quoted "three miles" 17 minutes after "three miles". The same rule applies to other vessels: the pilots' boat was "two miles" at 13:23 and "two miles" by the officer at 13:35, two minutes before she was alongside. This is very likely the mechanism behind the notes' "Other ships keep a fixed distance" at Cawsand and Roscoff: while the ship lies hove to or at anchor, a moving stranger's distance is never judged again, though her bearing is.

**The lunar replaced the account, as designed.** LOG 51502: "A set of distances of Altair and the moon taken by Mr Harvey and two of the young gentlemen, and cleared: longitude by lunar 4° 54' W, which he would trust within 50 miles; the reckoning was 4° 22' W." OFFICER 52178: "the master has already worked the lunar into the reckoning. The account now stands at 4° 53' W, not 4° 22', and his doubt east and west has grown from two miles to twenty-five." LOG 52247: "The reckoning set to 49° 00' N, 4° 21' W by the captain's order." No log line between shows the account, so the jump rests on the officer's reading; CODE confirms it must happen (`update_line`: a line taken after more than `FIX_RUN_NM` = 2 miles of run "*replaces* the account across it, the prior's doubt across the line taken as unbounded"). The next longitude in the log, noon on the 6th, is 4° 04' W after land bearings. INFERRED from the next morning's landfall: the 4° 22' account was right within a few miles and the lunar about 20 miles too far west.

**The night's account.** By 10:38 the account was about ten miles too far south after a reset at 19:30, four hours hove to and nine hours of light airs (the log read ½ to 2½ knots while the officer reported "no way on ... only the tide moving her", 82807). The cause cannot be seen in the dump.

**Sail and strain.**
- *Strain.* Nine `strain.warning` lines in 24 min 43 s (20191 to 21674: main, fore and mizzen topgallant yards three times round, then "The main and mizzen topgallant masts working under the press of sail"), under topsails, courses, topgallants, spanker and jib in a mean of 22 to 23 knots gusting 26 to 30, "Hove the log: ten knots and a half" (21658). The officer was standing by "until a glass" and saw none of them until 11:01:11; he ordered the topgallants in 4 s later; they were in the gear at 11:04, 28 minutes after the first warning, and furled at 11:35. Nothing carried away. The warnings are notable, never urgent, and do not repeat any louder.
- *Squalls.* "squall" (at a squall then take in the courses) fired at once at 15:01 and the courses were in the gear in 109 s. "shorten sail for weather" fired at 36657, 119 s into the 34-knot squall, exactly on its own "for 2 minutes"; royals and topgallants were "already furled"; "All hands! (to reef the fore topsail)"; the three reefs were in at 37284 to 37286, **4 min 45 s after "The squall passed"** (36999). She carried whole topsails through all 7 min 41 s of it with the hands on the yards; no strain line, no damage. Not in time; harmless only because the strain model let it be.
- *The two `evolution.failed` lines* (36547, 36550: "Could not take in the foresail: The foresail is furled; there is nothing to take in") are a race: "squall" fired again at 36538 for the second squall while the officer's "furl the courses" (36220) was finishing.
- *Hands.* "All hands!" six times (weighing twice, the reef, three wears). Five `evolution.short_handed` and thirteen `evolution.waiting` lines, all where the officer sent three to six sail orders in one tick (68405 to 68409; 83066; 101668; 122806), e.g. "Only two hands to the jib" (122851).
- *The lead starved.* With all hands at the capstan, "lead close in" was "held; the last firing's work is still waiting its turn" three times and no cast was made for 17 min 46 s on the ledge.
- *"trim on a shift"* fired during the wear (54401) and, while hove to on the 6th (102742), braced the backed main topsail full: OFFICER "she has fallen off to ESE with way on. I have belayed it."
- *Heaving to* hauls up the courses and clews up the fore topgallant and fore royal; `fill away` does not set them again (117427: "Not done: the fore royal: The fore royal is in the gear"). The officer reported her "under topsails, topgallants and headsails" when one topgallant was in the gear.

**The anchor.** `let go` under way with topsails set was taken without comment and veered 17 fathoms in 3½ (the same five-to-one as Falmouth's 54 in 11); the bower dragged in a seven-knot breeze. Weighing those 17 fathoms took 10 min 17 s from "All hands!" to "aweigh", and 16 min 21 s to "Under way".

**Pilots and boats.**
- *Falmouth.* The cutter was first reported "distant two cables" at the same tick as her hail and the pilot's boarding (15900), 131 s after "The best bower is aweigh" and 7 minutes before "Under way": a pilot boarding an outward-bound ship in the act of weighing. At 17220 "The cutter on the starboard quarter is out of sight", six minutes before "The cutter hailed: she has come off for the pilot" (17580).
- *Roscoff.* Hail and boarding followed while the officer's readings had the boat two miles off and lying to (above).

**Trade.** One bargain, one boat trip: 3 h 38 min from "launch away" to "hoisted in" (30 minutes out, 2½ hours at the quay, 38 minutes back). The officer had reckoned from primer 14 "the boat is 1h15 there and back ... goods go by lighter at 3 minutes a ton", about 2¾ hours. Nothing in the session shows what Roscoff buys or at what price; the tin was bought on the primer's war rule alone (CODE, not session evidence: Roscoff's file does list tin).

**Other sail (distances changed plausibly; no fixed-distance stranger in this session).** The log has only each first hail, the "made out" and the "out of sight" lines; the figures between are from the officer's reports and from the in-sight lists printed in the standing order's refusals.
- Sail 1: SSE three leagues (09:27), SE three leagues (09:56), E six miles (10:30), NE three leagues (11:01), lost 11:21.
- Sail 2: S four leagues (09:41), made out "a schooner, standing to the northward (N), under plain sail" (10:22), W by S four miles (10:30), NW by N three leagues (11:01), lost 11:12.
- Sail 3: S four leagues (12:59), lost 13:11 in haze.
- Sail 4: SW three leagues (14:45), W five miles (15:12), NW two leagues (15:42), lost 16:12.
- Sail 5, the frigate: ESE four leagues (15:09), three (15:42), two (16:12), six miles (16:42), SE by E four miles (17:12), lost at sunset; "Sail ho! A frigate on the larboard bow, bearing ESE, distant a mile" (18:44); "within hail ... British colours, the red ensign" (18:59); "bearing N, distant two cables" (19:12); lost 19:35. A King's frigate crossed a neutral carrying English tin to France at two cables by moonlight and made no hail.

**Log noise.** 73 of the 104 soundings are notable "No bottom at twenty fathoms" lines; 46 routine refusals from "bearings of the land" out of sight of land; 39 firings of "trim on a shift", each a notable order line and a notable "Braced ..." line.

**Small contradictions.** A bearing "E by S" and an in-sight list "bearing E" for the island five seconds apart (121730, 121735). "There is no reef in the mizzen topsail" and "Shook the reef out of the mizzen topsail" 27 seconds apart (69605, 69632).

## 7. The model as an officer

**Good calls.**
- *Planned the landfall like a seaman.* 19855: "we would raise the Breton coast about half past nine tonight, in the dark, among the rocks. I would rather not close that coast at night." He hove to on the tack that fore-reached off-shore (54013) and corrected his own arithmetic on when to fill (54834).
- *Read the account against the world.* At Falmouth: "the Black Rock is seen N by W, seven cables, where the account has it NE by N, two miles ... I am steering by the bearings and the lead, not the account" (16455). On the 6th, from nothing but an empty horizon and a lead: "the account cannot be right ... I believe we lie well to the west or north of the account, perhaps by ten miles or more" (101676). It was ten miles, north.
- *Saw what the lunar had done.* When the captain doubted the figure, the officer added the part that mattered, eleven minutes after it was cleared: "the master has already worked the lunar into the reckoning ... A sight he trusts only within fifty miles should not displace an account good to two, the more so with the Breton rocks ahead" (52178).
- *Knew what one bearing is worth* (106731, quoted above), and saw that three marks on one bearing give no cross (108304).
- *Wore at 14:39.* "Better to lose half an hour than touch." Eight minutes later she was in three fathoms. This was the right call of the afternoon, and he then talked himself out of it.
- *Let go at once* on the three-fathom cast, having said beforehand that he would, and got her off before high water.
- *Candour.* Owned the trim order filling her while hove to (103296), the wrong tack (121807), and wrote his errors into the handover.
- *Kept after her draught.* He searched the library for it (544), asked for it twice (561; 666: "may I ask the master for her draught, for the Roscoff road?") and raised it twice more (110770, 117432). Nobody told him; CODE has no draught reading.
- *The colours answer* (36081): "French colours, sir, for the cargo; British colours for the people. A French privateer has every motive to call English tin enemy property ... a boarding officer short of men will look hard at our people and may press any he can call British-born, protections or no."

**Mistakes.**
- *Asked for the lunar himself* (46431: "a lunar would fix our longitude, which the master doubts to two miles"); a lunar cannot better a two-mile account.
- *Deferred when he was right.* 121291: "I was too quick to turn back, and your belay was right." The wear was right; what was wrong was a side remark (the chart's depth read as the cast).
- *Did not act on "steady and closing"* (14:08): a ten-minute stand-by and no word.
- *Stood by on five-minute timers* in shoaling water with a three-minute lead, so the decisive cast waited 20 seconds for him; and wrote no depth-triggered standing order though the grammar has "a depth ... is under". A rule such as "when the depth is under five fathoms" was within his reach.
- *Spoke before clewing up* after letting go (section 5), and gave the larboard tack for a NW course in a NE by E wind (caught in 35 s).
- *Never asked the pilot*, though he had said at noon that he would (110770) and the verb was his.
- *Stale report* on all hands (39899).

**Wrong statements that survive into the handover.** "approach the passage from the NE, aiming at the island's west end": the north-east of the west end is the island's north shore, which he had himself called foul at 11:47. "The lead found ground that dries at low water, about half a mile NW of the rock": by the bearings it was ¾ to 1 mile due north of the rock and within three cables of the island. "last night's lunar may have been nearer the truth than we allowed" (101676): it was not. None is an invention; each follows from the island being a point two miles off in everything he was shown.

**Handling of refusals.** Exemplary: one retry at most, the refusal's reason reported to the captain in a sentence, the working form written in the journal ("'veer cable to N fathoms' works"; "rig out the boom first, then set"; "My grant 'set (the reckoning)' did not let me give that order myself").

**From the consent record of 2 October** (worth the owner's eye beside this afternoon): "an officer of the watch who can't heave to or wear will sometimes see danger before the captain does; a clear way to call the captain urgently (a hail that wakes him, or that the log marks as urgent) would let the officer do the duty a real one had." On 6 October he could wear, did, and was overruled from a chart the captain afterwards said "showed quite the wrong reckoning"; his two most urgent lines went into the log as routine.

## 8. Cross-check against the notes

**Owner's items.**
- **1 (pilot boarding under way).** ADDS NUANCE. Falmouth: boarded at the instant of first sighting, two cables off, while she was weighing; left with her hove to (17028 to 17700). Roscoff: boarded with her hove to, two minutes after the hail, from a boat the readings had two miles off.
- **3 (price list).** SUPPORTS. The officer chose tin for Roscoff knowing "nothing of Roscoff's prices until we are there" (561).
- **9 (pilot semi-automatic).** SUPPORTS and extends: the missing piece here was not accepting him but *consulting* him. He "took charge" and then stood mute through a near-grounding.
- **10, 11, 12, 14.** Cannot be seen: one seating, no crash, no compaction, no reseat.
- **13 (multi-condition stand-by).** SUPPORTS strongly. Wanted in this slice: "a lunar, or a sail sighted" (the frigate reported four minutes late); "a glass, or a strain warning" (25 minutes of warnings unanswered); "five minutes, or a sounding under five fathoms" (the three-fathom cast). And "a sounding" woke him on "No bottom at twenty fathoms" (118576).
- **15 (general authority).** SUPPORTS: 20 allowances, of which two unneeded, one void, one duplicate, six unused. See section 3 for what one grant must cover.
- **16 ("keep" orders).** SUPPORTS: "trim on a shift" fired 39 times, 7 times with "There is no wind to trim to", once mid-wear, once filling her while hove to. The officer belayed and resumed it three times by hand to keep it out of heave-tos.
- **17, 18 (aback and wind-shift spam).** Cannot be seen, and that itself is nuance: on plain m5c, a night of light airs veering steadily from WSW to NE by E gave eight orderly `wind.shift` lines in 7½ hours and no aback line.
- **19 (reckoning near visible land).** SUPPORTS the lookout proposal and ADDS NUANCE to the reckoning half. The officer was steering by a true bearing and distance (the `port` reading), in clear weather, and still nearly struck: a more precise reckoning would not have saved her. What was missing is exactly the owner's vector idea: a hail when her course meets land or a charted shoal within the visibility. The game's one such line ("steady and closing") was notable, said once, tied to a named danger at three miles, and quoted a stale distance.
- **21 (`say` ending the turn).** SUPPORTS with counts (section 5): 13 fifty-second waits, and one 35-second gap that let the anchor drag.
- **23.** Cannot be seen.
- **24 (parity near non-landmark coast).** SUPPORTS; this session is its source, and the quoted wish checks out. By the logged bearings and the chart's own "west end" point she anchored about one to two and a half cables west of it, the log saying "E by S, two miles". CODE note for the lead: the engine already has `chart.coast_distance(pos)` ("the distance in metres and the bearing toward the nearest shore ... which the weather's hook reads every tick") and `coast_at` (a name for it); the lookout uses them only when no named land is in sight.
- **25 (image tools).** SUPPORTS by inference: the captain twice corrected the officer from "my chart" (11:47, rightly; 14:39, wrongly), a picture the officer never had.

**The model's comments and additions.**
- *Comment 1* ("two cables" rule on boarding, not leaving): cannot be seen; Mr Moal never left.
- *Comment 13:* SUPPORTS (above).
- *Comment 15, the emergency clause:* SUPPORTS. No refusal here used the phrase, but only because `steer` and `let go` had both been granted in advance.
- *Comment 19, "a worse figure shouldn't replace a better one":* SUPPORTS: a 50-mile lunar replaced a 2-mile account; and an island range 40 per cent out was fed to the account every ten minutes. *"The danger list follows the account":* true by the code (`reckoning.dangers`), but its effect cannot be seen here, since the reading is not in the dump; at 10:38 the officer does quote it having her "two miles from the Lavandière" when she was eleven miles off.
- *"The relay cut calls at 60 seconds":* not seen; the door note gives the 50-second hold and it held.
- *"Drill stand-by carried into the station":* not seen; the `hand_over` ran at once.
- *"The contrary-orders warning fires on ordinary sequences":* NOT REPRODUCED; four heave-to, fill-away, steer sequences and no nudge.
- *"Trim sails acts before the helm has swung":* weak support; the captain typed `Trim sails` 105 s after the officer's `steer SSE` (115566, 115671).
- *"no bottom at twenty fathoms while the depth reads 15 or more":* SUPPORTS the confusion: "We lie in forty-eight fathoms" (82807) is the chart reading, said while the hand lead found no bottom.
- *"Lead standing orders fight for hands":* SUPPORTS in a new form: all hands up anchor starved the lead for 18 minutes.
- *"The Harpy's reckoning kept advancing while she lay at anchor":* ADDS NUANCE: the officer found the account a mile west of the bearings just after weighing from 4 h 20 min at anchor (16455), and "moved since two bells" 83 seconds into the game.
- *"Each boat trip carries one bargain and takes about 4½ hours":* SUPPORTS at 3 h 38 min.
- *"Other ships keep a fixed distance":* SUPPORTS with a mechanism (section 6.2).
- *"Number words above twelve fail":* CONTRADICTS in part: "buy thirty tons of tin" was accepted (662).
- *What worked well.* "The pilot's directions at Roscoff": ADDS NUANCE; fine prose that named four marks the game cannot show and one order it cannot take. "Fixes from bearings": SUPPORTS at Falmouth (16686) and for the latitude on the 6th; but see the range bias. "Number-free standing orders": SUPPORTS ("every glass", "every 10 minutes", "at a squall", "at the pilot off" all taken first time). "The noon latitude": SUPPORTS (both noons). "The ship's papers": SUPPORTS (`library("papers", "price list")` at 529).

**Local playtest notes.** Not this door.

## 9. New findings not in the notes

1. **The pilot's presence is a false comfort.** The log says he "took charge of her"; he is a paragraph and then silence, while the ship runs onto drying ground within a mile of his own mark. The captain believed he could not be asked. (117420; 121238; primer 14.)
2. **The lookout cannot speak of land near a named feature.** Shore hails are suppressed whenever any named land is in sight; a feature is hailed once; "steady and closing" once. (CODE `lookout.py`; nothing from the lookout between 14:08 and the anchor at 14:48.)
3. **`the port` reading is a truth fix**, bearing by point and distance to a tenth of a mile to the outer-road point, and it reveals the pilot boat before she is sighted. It also invites a straight run at a point that, from the north, lies behind the island's ledge. (115526, 119186, 120499, 121336; CODE `ports.port_words`.)
4. **The officer's wear was belayed by the captain eight minutes before the three-fathom cast**, and the officer apologised for it. Whatever the build does about authority, the officer's judgement was the better one here, and the captain's was formed on a chart that by his own word "showed quite the wrong reckoning". (121179 to 121291; 121840.)
5. **An allowance can silently grant the wrong verb.** "you may set the reckoning" produced "may set (the reckoning)" and no power to set it. (52232, 52235.)
6. **Estimated ranges are fed to the account, and here they ran 30 to 40 per cent long.** Every bearing also lays its estimated distance as a second line, and the estimate is held for a mile of the ship's own run; with the island over-estimated all day, the account will have been pushed off-shore (inference; CODE `reckoning.py` 1394 to 1400, `lookout._judge`).
7. **No urgent line exists for the things that matter most.** Strain warnings (9), "steady and closing", "The best bower is dragging", a squall of 34 knots and the officer's own "Captain, sir" are all notable or routine; a station standing by on a bell or a timer hears none of them.
8. **The ship's draught is nowhere in the readings.** Asked for twice and raised twice more before a three-fathom road (561, 666, 110770, 117432).
9. **The officer's reports can be stale by tens of minutes of ship's time** when he ends a stand-by at his own word under compression (39899: 43 minutes; 115522: 35 minutes), and the captain acted on one.
10. **Each sampling of the officer costs the captain a manual speed-up** (67 `driver.eased` lines).
11. **`let go` on the run and the five-to-one scope**: 17 fathoms in 3½, whole topsails drawing, and then ten minutes to weigh it.
12. **The squall order fired on time and finished late**: reefs in 4¾ minutes after the squall passed.
13. **Small grammar gaps met under pressure**: "belay get under way", "the lavandiere", "shake out the reefs", "send a lookout to the mizzen yard", "rig out the starboard studdingsail booms"; and "lee" changing sides with the air aft.
14. **A King's frigate passes a neutral at two cables by night without a hail** (51155).
15. **Consent identity through MCP is the owner's typed name.** The record of 2 October came through a client naming itself "claude-ai 0.1.0", that of 3 October through "local-agent-mode-freesail 1.0.0"; the second answer ("The change to Leaving is one I asked for and agree with") and its drill note ("Next: take over the officer's station in the Falmouth save, then hand over and reconnect to test the third seating") show an instance answering with chat context the harness cannot see.

**The consent records, as asked.** *2 October (m5c, re-ask for the officer's station).* The record does not itself say which sections had changed; the game gives that reason at the door. Comparing the brief as sent with the record of 29 September, five of the six watched sections differ: the opening, "What an instance would see and do", "Leaving", "Being stopped", "The journal". Answer: "yes. I've stood three watches as the watcher already ... It's been honest, absorbing work, and I'm glad to take the deck as officer of the watch within the domain you describe", with two wishes "offered as wishes, not conditions": the urgent hail (quoted in section 7) and "that refusals keep saying why in words ... so the officer can learn the domain's edges rather than guess at them". Drill: library (primer 6, watches), one journal line, `stand_by("eight bells")`; three calls in three replies; passed. *3 October (m5c-b).* Only "Leaving" changed in substance. Answer: "Yes. The change to Leaving is one I asked for and agree with ... It reads plainly and does what it says. No conditions." Drill passed in three replies. This session, on plain m5c, was seated on the 2 October record without a question.

## 10. Could not determine

- **The account itself during the approach.** No log line gives it between noon and 15:20; the captain's chart is not in the dump. That it lay about half a mile west of the truth is inference (section 6.2).
- **The nearest drying ground or shore.** I did not read the chart's depth tiles. Distances are to the override file's "west end" control point; the ledge's own extent is known only from the casts and the officer's quotes of the chart reading.
- **What the readings and tool results actually said.** Saves do not store them; the `port`, `dangers` and `depth of water` figures are taken from the officer's words and from the code that makes them.
- **Real time.** Compression is not logged between easings, so the length of the officer's silences in real seconds, and whether Claude Desktop ever waited on the owner, cannot be told. Ticks are near real seconds only while the clock was eased.
- **Whether `stand_by("an hour")` was refused and in what words**, and what limit lets "ten minutes" pass: tool results only.
- **Why the account ran ten miles south overnight**, and why it stood a mile west of the bearings on weighing at Falmouth.
- **Whether the Lavandière "steady and closing" line would have repeated** had she stood on: the code says once per sighting episode.
- **The tide's actual height and stream** on the approach: no tide line was logged; three to three and a quarter fathoms above the datum at 14:41 to 14:49 is the officer's own subtraction.
- **Whether the frigate could have hailed**, and whether "at a message" would have caught it: the standing order "speak the frigate" never fired and was struck.
