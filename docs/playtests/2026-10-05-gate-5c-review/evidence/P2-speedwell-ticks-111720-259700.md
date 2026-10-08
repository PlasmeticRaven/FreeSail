# P2 — *Speedwell*, session `4-schooner-plymouth-opus`, ticks 111,720 to 259,700

Conventions. **LOG** = a line of the ship's log (fact). **SAID** = what the officer (the model) or the captain said (claim or opinion). **SOURCE** = my reading of the m5c-b source tree (`D:\Projects\FreeSail\FreeSail-gate-m5c-b\freesail\...`), read only and not run: it is an inference about cause, not something the log shows. The order, lookout, vessel, port and distance-word files I cite (`orders/__init__.py`, `orders/port.py`, `world/lookout.py`, `world/ships.py`, `world/ports.py`, `world/geo.py`) are byte-identical in m5c and m5c-b; `agents/harness.py` differs between them and I read the m5c-b copy. A save keeps no tool results, so what the model was shown (readings, the danger list, refusals' return text) is known only from what it then said. Ticks are seconds of ship's time; all times are ship's time.

## 1. Slice identity

- Session `4-schooner-plymouth-opus`, **ticks 111,720 to 259,700** = 22 June 1805 12:02 (noon) to 24 June 05:08; 41 h 06 m of ship's time; 2,270 log lines (435 notable, 2 urgent, 1,833 routine).
- Ship: the merchant topsail schooner *Speedwell*, American colours ("American colours being no bar at Roscoff"), no chronometer, master Mr Travers (skill 0.9), seed 7, scenario "A merchant schooner, free".
- Captain: the human owner. Officer of the watch: the mate "Mr Ray", held by **Opus 5.5 through the MCP door**, first seating for the whole slice (stationed tick 12; the deck his since tick 109, 21 June 05:01; no deck given or taken in this slice). Station header: authority "officer, levels 0 to 2", sampled "every glass and on notable and urgent events", `patience_s: 3600`, `stand_by_ends_turn: True`, no token budget.
- Build: **m5c-b** (the save is under `FreeSail-gate-m5c-b\saves`).
- The model's calls in the slice (193 transcript entries): `stand_by` 73 (63 in turn, 10 "out of turn"), `submit_order` 61 (51 accepted, 9 rejected, 1 refused for domain), spoken lines 53 plus 1 `answer` (4,548 words, mean 84, longest 210 at 224377), `journal` 2, `library` 3, `readings` / `state` / `read_log` 0.

## 2. What happened

| Tick | Ship's time | Event |
|---|---|---|
| 111720 | 22 Jun 12:02 | LOG noon: "Latitude by observation 49° 29' N; the reckoning was 49° 19' N ... Longitude by account 3° 42' W." The officer keeps a second longitude of his own, "about 4° 18' W" (111729). |
| 126041 | 16:00 | Captain asks what the water sail is good for; answered at 126051. |
| 140852 | 20:07 | Sunset. Officer shortens down; **8 refusals in 60 s** over the water sail (140862 to 140922) until "take in the occasional sails" (140925). 'night lead' every 30 min entered (140863). |
| 141901 | 20:25 | SAID: the danger list by account "now show[s] the Triagoz rocks ten miles south by west"; he proposes to heave to at 22:00. |
| 147614–147971 | 22:00–22:06 | Wore to the starboard tack, head NW; hove to. 14 miles to Roscoff by account, "the Triagoz five miles south-south-west" by the account. |
| 154800 / 159000 | 23 Jun 00:00 / 01:10 | Fog down, fog lifted. |
| 162102 | 02:01 | The officer's 'trim' standing order fires while hove to and fills her. Captain belays it, backs the fore yards, fills away and heaves to again by hand (162559 to 163278). |
| 168875 | 03:54 | Sunrise; officer fills away; captain steers SE by S (168957); 'trim' resumed by the captain's leave (169036). |
| 182220 | 07:37 | **Landfall**: "The Isle of Bas bearing S by W, distant four leagues." Officer works the position (48° 57' N, 3° 58' W) and steers S by W; the captain takes the bearing (182233), and two more at 07:55. |
| 183600 | 08:00 | Haze: "The land is out of sight." 'approach lead' every 10 min (184102). |
| 185384–190184 | 08:29–09:49 | Nine wakings of the officer by "No bottom at twenty fathoms." |
| 190276 | 09:51 | Captain adds standing order "Pilot hails" (first wording refused, 190249). |
| 191460–192000 | 10:11–10:20 | Land three miles; "Sail ho! A boat pulling off from the land right ahead, bearing S, distant two miles"; made out as the Roscoff pilots' boat. |
| 192540 | 10:29 | The boat hails; officer heaves to at once (hove to 192632). |
| 193303 | 10:41 | 'trim' fires again while hove to and fills her; captain belays it and backs yards and sheets by hand (193417 to 193491). |
| 194640 | 11:04 | "The Lavandière bearing S by E, distant two miles: a danger." Four "steady and closing" lines follow (11:25 to 12:06). |
| 198120–198216 | 12:02–12:03 | Noon (lat 48° 51' N, account 3° 59' W). Officer reads primer 14, concludes she must sail to the boat; first bottom "And a half eighteen". |
| 198209–199136 | 12:03–12:18 | Fill away; tack refused; captain: "No, as you were. I'd rather make it in than wait on the pilot"; wore; WSW; "You have the con"; S by W for the entrance. Three nudges. |
| 200107–200745 | 12:35–12:45 | **Shoaling**: 13½, then urgent "Taken aback" (200205), 6½, **3½** (200467), 3¾, 5, 7 fathoms; captain and officer cross helm orders (200588 to 200667). |
| 200760 | 12:46 | "The pilot, Mr Moal of Roscoff, came aboard from the boat and took charge of her", with his directions. |
| 201072 | 12:51 | Captain: "I'll con her from here". She works round to come at the Lavandière from the NW; the wind dies. |
| 203621–203969 | 13:33–13:39 | Urgent "Taken aback" with no steerage way; captain: "You may come to an anchor"; "The best bower let go in twelve fathoms and a half." Brought up 13:53 with 62 fathoms. |
| 204842–212080 | 13:54–15:54 | Long-boat for the prices. |
| 212090–212162 | 15:54–15:56 | Coal refused by the market; "buy sixteen tons" refused; "buy 16 tons of brandy" taken; purse £34; nudge. |
| 224147 | 19:15 | Brandy aboard. Scilly chosen for the morning (224232 to 224642); journal written. |
| 226800 | 20:00 | Fog; night at anchor, lead every 30 min. |
| 255390–255600 | 24 Jun 03:56–04:00 | Sunrise in fog; captain orders her under way; fog lifts and shows "The Lavandière bearing S by E, distant five cables: a danger." |
| 256512–256898 | 04:15–04:21 | Aweigh; "Under way on the starboard tack ... full and by (NNW (338°) lying too near the wind to be laid)." |
| 257345 | 04:29 | One cast of 7¾ fathoms, then 18¾. |
| 258540–259680 | 04:49–05:08 | Pilot asks to be put off; hove to; boat sighted a mile off, hails at 05:05; "Mr Moal left her in the boat ... the pilotage, £3, paid". Officer fills away (259682). |

## 3. The deck and the captain's words

**The deck.** No change in the slice. LOG 109 (21 June 05:01): "Mr Ray, you have the deck." It is handed back only at 343363. The captain is on deck throughout (on deck since 47672) and types orders himself at every busy moment. Two informal transfers of "the con", which is not a thing the game knows: 198820 "You have the con." and 201072 "I'll con her from here, please prepare for the anchorage and bring in the sail as we make our way in."

**Allowances (`you may ...`).**

| Tick | Words | Used? |
|---|---|---|
| 203629 (23 Jun 13:33) | Captain: "You may come to an anchor" → LOG "The officer of the watch may come to an anchor, by the captain's word for the watch." | Yes, 4 s later (203633 "coming to an anchor"). The officer had asked for it by its exact name 15 s before (203614: "Your word: "come to an anchor" or "you may come to an anchor"."). The older "may let go the anchor" and "may moor" (21 June) did not cover it. |
| 169032 (03:57) | A `tell`, not an allowance: "You may resume your trim order as you like." | Yes (169036 "resuming standing order trim"). |
| Given 21 June 05:00–05:02 "for the watch", still honoured here | buy, sell, send the boat, weigh, get under way, steer, veer cable, tack ship, wear ship, heave to, fill away, let go the anchor, moor; "keep her full" (43096) | Used in the slice: steer ×8, wear ship ×2, heave to ×3, fill away ×3, send the boat (204842), buy (212162), get under way (255460), keep her full and by (258096). "For the watch" in the log's words therefore lasted three days and some twenty changes of the watch. |

**The captain's telling lines** (15 typed `tell`, 1 `ask`, 3 more tells fired by his standing orders):

- 126041, `ask`: "What do you think the watersail is good for if the wind picks up? 10 knots maybe? 15? 20 even? I'd begin to doubt it at some point, but I'm not sure." A real question to the officer as a seaman.
- 182294: "Quite reasonable, Mr Ray, and I think the split is the thing. Neither was perfect, and being sure to stay cautious was the right way." His verdict on the two longitudes (section 6.1).
- 184203: "... if we fine by the mark twenty that we simply drop anchor if reasonable and hold. It's no great trouble to us to be able to hold our position rather than rely on the drift. The pilot will find us either way, I think." (The officer later learned from the primer that no pilot comes off to a ship at anchor.)
- 198310: "No, as you were. I'd rather make it in than wait on the pilot. Anyway, my tobacco is far too valuable to risk."
- 200139: "My chart shows some un landmarked land off the bow and larboard bow, I'd come a bit westward if I were you, but you have the con." **The captain can see coast on his chart that has no name; the officer cannot be told of it by any reading** (notes 24 and 25).
- 200412: "... I'll stay on keeping the sails trimmed between your samples." The owner making himself the "keep her trimmed" order (note 16).
- 200719: "Apologies, I only gave west by south when I saw us pointing straight head to a flukey wind that you wouldn't see in your stand by. In this close in rocky coast I felt the need to keep us from losing way." The clearest statement in the slice of what a sampled officer cannot do.
- 203656: "Or, we simply send the boats from here and call it good." 204890: "Aye, a fair plan. Are we safe to moor here overnight by your reckoning?" (a question sent by `tell`; answered two hours later, see section 5).
- 212157: "Aye, buy the brandy, and mark one cask for the officer's stores." 224232: "I wouldn't call that a fair wind for Plymouth, necessarily, but certainly for Brest or Scilly perhaps. No need to go straight back to Plymouth ..."
- 224642: "Aye, Scilly at dawn then. Please make a journal entry so you're up to date on our current status, and then you may standby until sunrise, or as you please." The owner asking for a journal entry as insurance for the session's memory (notes 10 and 11).
- 255450: "Fair wind's up for Scilly, fog won't hurt us heading out the west and north, let's get her under way Mr Ray. Then we can break out the officer's cask once we're well clear."

**What the captain did by hand because the officer could not, or could not in time.**

1. **Every bearing**: 29 `take a bearing of ...` orders accepted and 6 mistyped (16 of the 29 before the pilot boarded). Taking a bearing is outside the officer's domain and no allowance for it existed until 27 June (512951); no standing order for bearings was in the book.
2. **Restoring the heave-to twice** after the officer's 'trim' order filled her: 162559–163278 (belay, "back the fore yards", "Fill away", "Heave to") and 193417–193491 (belay, "Back the yards", four `haul ... weather ... sheet` orders).
3. **Trimming between the officer's samples**: 12 `trim` orders 12:40 to 13:24 on the 23rd, three more on the 24th (257342, 257475, 258314).
4. **The helm in fluky airs**: 10 helm orders 12:43 to 13:23 (200588 to 203014).
5. Waking the officer on events: his standing orders "Pilot hails" (190276), "The pilot asks off", "The Pilot away" each "tell the officer" at an event (fired 192540, 258540, 259680). This is the owner's own workaround for a one-condition stand-by (note 13).
6. "Loose the topsail" (203199) and "Take in the fore and aft sails" (204477).

## 4. Orders refused

27 in the slice: 26 `order.rejected`, 1 `agent.refused`; 10 the officer's, 17 the captain's. Classes: (a) vocabulary or grammar gap, (b) domain refusal as designed, (c) domain refusal that looks wrong, (d) correct ship-state refusal, (e) apparent bug, plus "typo" where the captain mistyped and the refusal was right.

| # | Tick, time | By | Order as typed | Refusal's words | Class; what worked |
|---|---|---|---|---|---|
| 1 | 140862, 22 Jun 20:07 | officer | `take in the water sail` | "The officer of the watch may not take in the water sail without the captain: the port's business is the captain's. 'take in the water sail' not carried out." | **(e)**. Read as the port's "take in water". |
| 2 | 140866 | officer | `furl the water sail` | "A studding sail is not furled on its spar; take it in instead." | (a); and it points back to the order that fails. |
| 3, 4 | 140875, 140904 | captain | `take in the water sail` ×2 | "She is not in port; there is no yard to demand it of." | **(e)**, the same misreading on the captain's side. |
| 5, 6, 7 | 140879, 140907 (captain), 140922 (officer) | both | `take in the watersail` ×3 | "There is no such part as the watersail in this ship. ('take in' was understood.)" | (a): no alias, and no "did you mean". |
| 8 | 140899 | captain | `unbend the water sail` | "The water sail: The water sail is set; take it in before unbending it." | (d), but its advice is the broken order. |
| — | 140925 | officer | `take in the occasional sails` | accepted; water sail "Took in ... and made it up" at 141295 (20:14) | **What worked.** Side effect: 141016 "Could not take in the ringtail: The ringtail is furled; there is nothing to take in." |
| 9 | 162562, 23 Jun 02:09 | captain | `heaev to` | "'heaev to' is not an order this ship understands; did you mean 'heave to', 'heave the log' or 'ease'? ..." | typo; good suggestion. |
| 10 | 163163 | captain | `Heave to` | "She is hove to already; fill away before heaving to again." | (d): typed 1 s after his `Fill away`; accepted at 163233 once she had filled. |
| 11 | 190249, 09:50 | captain | `standing order "Pilot hails": at the pilot hail then tell the officer ...` | "'at the pilot hail' names no event the ship knows; did you mean the pilot's hail, the pilot off or the pilot aboard? The events are sunset, sunrise, ..." (all 78 events listed, in one log line) | (a), small: "the pilot hail" for "the pilot's hail". Retyped and taken at 190276. |
| 12 | 193432, 10:43 | captain | `Back the fore staysail` | "The fore staysail is a jibheaded sail; it has no yard to brace. Trim it with its sheet." | (a): a sailor backs a staysail. "Haul the weather fore staysail sheet" worked (193446). |
| 13 | 193441 | officer | `belay standing order "trim"` | "Standing order 'trim' is belayed already." | (d): the captain had done it 24 s before. |
| 14 | 193441 | officer | `heave to` | "She is hove to already; fill away before heaving to again." | **(e)-leaning**: 'trim' had just filled her out of the heave-to (193303), yet the ship still counts herself hove to, so the order that would restore her is refused. The captain had to back yards and sheets one by one. |
| 15, 16 | 198133, 198155, 12:02 | captain | `take a bearing of the lavandiere`, `... the lavandiére` | "The lavandiere is not in sight; did you mean the Lavandière? In sight: the Lavandière bearing S by W, distant two miles: a danger; Sail ho! The Roscoff pilots' boat on the starboard quarter, bearing W by S, distant eight cables; ..." | **(a)**: a French name refused for want of its accent. Taken at 198187 with "è". |
| 17 | 198178 | captain | `take a bearing of b` | "B is not in sight; did you mean the Roscoff pilots' boat or the Isle of Bas? ..." | typo. |
| 18 | 198308, 12:05 | officer | `tack ship` | "She is not close-hauled; bring her by the wind before going about." | (d). He wore instead (198312). |
| 19, 20 | 201077, 201078, 12:51 | officer | `furl the flying jib`, `furl the main gaff topsail` | "A jibheaded sail is not furled on its spar; take it in instead." | (a): "furl" as the general word for stowing a sail is refused for half this schooner's canvas. Both sails were in fact already down (199189, 141064); the officer nonetheless reported them "furled" (201080). |
| 21 | 202369, 13:12 | captain | `Take a bearing ofthe Lavandière` | "Ofthe lavandière is not in sight; did you mean the Lavandière? ..." | typo. |
| 22 | 202975, 13:22 | captain | `Trim sails` | "There is no wind to trim to." | (d). |
| 23 | 202988 | captain | `150` | "'150' is not an order this ship understands. ..." | typo; `Steer 150` followed. |
| 24 | 212090, 15:54 | officer | `sell forty tons of coal` | "Roscoff's market has no coal; it deals in brandy, geneva, rum, tea, tobacco, wine, salt, canvas, onions, tin, salt beef." | (d). The first moment the ship could learn what Roscoff trades in. |
| 25 | 212160, 15:56 | officer | `buy sixteen tons of brandy` | "How many tons? Say 'buy twenty tons of tin'." | **(a)/(e)**. `buy 16 tons of brandy` taken two seconds later (212162). |
| 26, 27 | 256307, 256313, 24 Jun 04:11 | captain | `take a bearing of isla verte`, `... the isla verte` | "Isla verte is not in sight; did you mean the Isle Verte? ..." | typo. |

No refusal in the slice is class (b) or (c): the only domain refusal (#1) is a misparse. The domain's real cost here was silent: the officer never tried to take a bearing, knowing from the *Harpy* that he may not (the refusal itself is outside the slice, 512943: "may not take a bearing of the light without the captain: the reckoning, the sights and the course shaped are the master's for the captain"). For an officer with the deck closing a coast in 1805 that looks like class (c).

**The order-parsing list, with causes** (SOURCE, the same in m5c and m5c-b):

- *Water sail.* `freesail/orders/__init__.py`, `_stores_order` (lines 149–163): any order that begins "take in " and contains the word "water" becomes the port's verb "take in water" before the sails are looked at. The ship file classes the sail as `class: studding` (hence "not furled on its spar") in the group `occasional sails: [ringtail, water_sail]`, and lists no alias "watersail". All four of the model's statements in the notes are borne out.
- *Number words.* `freesail/orders/port.py`, `_NUMBER_WORDS` (lines 37–66) is a fixed table: a, an, one to twelve, fifteen, twenty, "twenty five", thirty, forty, fifty, sixty, seventy, eighty, ninety, hundred, "a hundred", "two hundred", "three hundred". So thirteen, fourteen, **sixteen**, seventeen, eighteen, nineteen and every compound but "twenty five" fail; the round tens work ("buying forty tons of coal" at 7792, "buying twenty tons of pilchards" at 24374). The note's "Number words above twelve fail" is too broad: it is the teens (bar fifteen) and the compounds. A second, different table sits in `orders/ground_tackle.py` for fathoms.
- *"Full and by".* The refusal is outside this slice (43089, 21 June: "may not full and by without the captain: the course is the captain's ..."), the allowance was logged as "may keep her full" (43096, 43102). In the slice "keep her full and by" is accepted from the officer under that allowance at 258096 (24 June 04:41): "Helm ordered: keep her full and by."; "Steady, full and by, the wind 59° on the starboard bow." (258159).

## 5. Harness behaviour

**Seatings and door events.** One seating throughout; no stand-down, pause or hand-over. 23 door events: 10 "its own word" (a `say` that ended a stand-by or opened a turn), 10 "out of turn" stand-bys, 3 library reads (198134, 198136, 198139: `primer 14` with `find='hail the pilot'`, `find='pilot'`, `section='roscoff'`).

**Stand-bys**: 73, none refused. `until` values: a sounding 37; a glass 6; sunrise 3; filled away 3; the pilot aboard 3; sunset 2; ten minutes 2; 5 minutes 2; wore 2; the boat alongside 2; the pilot asks to be put off 2; and once each the change of the watch, four bells, hove to, steady on the course, a landfall, the pilot's hail, brought up, under way, the pilot off. Longest: 30,713 s (224677 to 255390, 19:24 to 03:56, "until sunrise" at anchor); 14,801 s (to sunset); 14,517 s (22:09 to 02:11, hove to); 12,861 s (to the landfall).

**What woke the station** (74 `agent.resumed`):

| Reason | Count | Worth it? |
|---|---|---|
| A sounding | 29 | 20 were real depths in the close approach (200377 to 203604, every 1 to 3 minutes): yes. **9 were "No bottom at twenty fathoms"** (185384, 185986, 186585, 187184, 187784, 188384, 188984, 189584, 190184; 08:29 to 09:49): 8 of them produced nothing but the next `stand_by` 2 to 4 s later, and each eased the owner's compression to 1x. |
| A word from the captain | 13 | Yes; 3 of them were the captain's standing orders telling the officer of a pilot event the officer was already standing by for (192540, 258540, 259680). |
| Ended at its own word | 9 | The model watching the notable lines its held call returned and speaking up: 141901 (Triagoz), 162663 (trim broke the heave-to), 193441 (same), 195221 (Lavandière sighted), 198148, 198208, 198308, 203038 (caution on the captain's 160°), 258095 (shoal cast). Mostly worth it. |
| A bell, sunrise, sunset, minutes passed, noon | 12 | Yes. |
| An evolution's end or an event asked for (wore ×2, hove to, steady on the course, a landfall, brought up, under way, the boat alongside ×2) | 9 | Yes. |
| A question from the captain | 1 | Yes. |
| An urgent event | 1 | Yes (200205, "Taken aback"). |

On the approach the officer used one condition at a time and paid for each choice. Standing by for "a sounding" (184145 on) he got the no-bottom wakings. Standing by for "the pilot aboard" (192587, 193450, 195222; 1 h 33 m in all) he was woken by nothing while the Lavandière was sighted (11:04) and three bearings were hailed "steady and closing" (11:25, 11:53, 11:59); he caught them only by re-reading the notable lines his held call returned. The note's "a sounding, or the pilot's hail, or a danger sighted" is exactly what this hour needed. He did not say so in the log at the time.

**"Out of turn" stand-bys.** 10 (163174, 182280, 190238, 201058, 212148, 212216, 224427, 255450, 256957, 258306). Eight came exactly 50 ticks after a spoken line (for example `say` at 190188, stand-by at 190238): the 50-second hold of the `say` call running out with the game at 1x, after which the model stood by. All were accepted and logged as ordinary stand-bys. Each sample logs "Compression eased to 1x: the officer of the watch is sampled." (67 times in the slice, once more for the urgent line).

**A captain's word that lands while the officer's turn is open does not wake the stand-by that follows it.** LOG, five times in the slice (20 of the voyage's 126 tells and asks):

| `tell` | Next event | Officer's next waking | Effect |
|---|---|---|---|
| 198310 "No, as you were. I'd rather make it in than wait on the pilot ..." | 198312 `wear ship`, 198313 stand-by "wore" | 198768 (+458 s) | He wore towards the pilot boat before answering "Understood, sir: no anchoring, we go in." (198777). |
| 198820 "You have the con." | 198821 stand-by "5 minutes" | 199121 (+301 s) | Acknowledged five minutes later (199138). |
| **200139** "My chart shows some un landmarked land off the bow and larboard bow, I'd come a bit westward ..." | 200140 stand-by "a sounding" | 200205 (+66 s), by the urgent "Taken aback" | The warning was acted on only when another event woke him: 200213 "You're right, sir, and I'm coming west now." She was in 13½ fathoms going to 3½. |
| 203656 "Or, we simply send the boats from here and call it good." | 203657 stand-by "brought up" | 204837 (+1,181 s) | Harmless. |
| **204890** "Are we safe to moor here overnight by your reckoning?" | 204891 stand-by "the boat alongside" | 212080 (+7,190 s) | Answered two hours later: "your question, which I left unanswered" (212098). |

SOURCE: `agents/harness.py`, `_while_open` and `_fold` (about lines 697–719 and 1018–1049): a word arriving while "the floor is the model's" is folded into the open sample, and `_build_sample` clears it ("carried once; no answer is owed"). The stand-by the model had already sent is then entered with nothing left to wake it. `_in_flight` re-checks events and urgent lines that fell while a stand-by call "was on its way", but not the captain's word.

**Nudges** (no pause followed):

- 198312 (12:05): "The officer of the watch nudged: 3 contrary orders on the yards and the helm within the watch (heave to; fill away; wear ship)."
- 198776 (12:12): "... 4 contrary orders ... (heave to; fill away; wear ship; steer WSW)."
- 199136 (12:18): "... 5 contrary orders ... (heave to; fill away; wear ship; steer WSW; steer S by W)."
- 212162 (15:56): "... 3 contrary orders on the ship within the watch (come to an anchor; send the boat ashore; buy 16 tons of brandy)."

None was right. The first chain is heaving to for a pilot, filling away 1 h 35 m later, wearing and steering for the entrance (the "heave to" was in the watch before, so "within the watch" is a four-hour window). The last is three orders with nothing contrary in them. The model ignored all four and was right to.

**Journal, library, readings.** Two journal notes: 141906 (order-language notes and the Triagoz) and 224654 (a full status at the captain's request: cargo, purse, stores, both price lists, the plan, six lessons). The harness's own journal for the station has 89 entries in this range, of which 73 are "Stood by until ..." and 9 "Ended the stand-by ...": the two real notes are 2% of it (note 11). Library: the three reads at 12:02 on the 23rd, an hour and a half into waiting for the pilot. No `readings`, `state` or `read_log` call in 41 hours: the samples were enough.

**Turns that ended oddly.**

- 198148 (12:02): SAID "I'm filling away to run down to her", then `stand_by("filled away")` with no `submit_order` in the transcript. 198208, 60 s later: "Sir, my fill-away didn't go through, and she's been drifting south-east towards the Isle of Bas". The order was sent at 198209. Whether a call was lost or never made cannot be told (section 10).
- 140868 (20:07): SAID "water sail furled ... "Furl the water sail" got past that", two ticks after that order was rejected (140866). Corrected at 140922: "Correction, sir: the water sail is still set."
- 193441, 200415, 200662: orders crossing the captain's (already belayed; a second `trim sails` one second after his; "steer NE by N" 74 s after his "Steer west by south", undone at 200667). The officer acts on a sample some seconds old while the owner types.

**Limits.** No sign of context, turn-budget or relay trouble in this slice: the largest burst is six orders in one turn (140861 to 140866; SOURCE: the budget is 8 calls a sample). The model kept its thread for 41 hours, including a question two hours old. Its one lapse of memory was its own promise at 169037 ("I'll belay it myself before we next lie to"), broken at 192543.

## 6. Ship, sea, navigation and port observations

### 6.1 The account against the land

**Every line from noon on the 22nd to the pilot's boarding that states a position, a danger, a bearing, a sounding or the master's place.**

| Tick | Time | Source | Line |
|---|---|---|---|
| (86831, before the slice) | 22 Jun 05:07 | LOG | "longitude by lunar 3° 46' W, which he would trust within 20 miles; the reckoning was 4° 19' W." |
| 111720 | 12:02 | LOG `reckoning.noon` | "Latitude by observation 49° 29' N; the reckoning was 49° 19' N. Course made good since yesterday SSE, 62 miles. Longitude by account 3° 42' W." |
| 111729 | 12:02 | SAID officer | "By my longitude, the Eddystone fix and the run, about 4° 18' W, Batz bears south-south-east forty-five miles. The account's 3° 42' W comes from the lunar." |
| 113520 | 12:32 | LOG `master.place` | "Mr Travers came on deck, the day's work done." |
| 126011 | 16:00 | SAID | "By my reckoning, 49° 16' N, 4° 16' W, Batz is some thirty-two miles south-south-east, and the ship puts Roscoff at thirty-two as well." |
| 126113, 133313, 140513, 154913, 169313, 183713 | once a watch | LOG `standing.held` | "Standing order 'inshore lead' every 10 minutes: not carried out; the land is not in sight." |
| 140868 | 20:07 | SAID | "By my reckoning, 49° 03' N, 4° 13' W, Batz is about nineteen miles south-south-east ... She's in forty-eight now." |
| **141901** | **20:25** | SAID (danger by account) | "the chart's dangers, worked from the account, now show the **Triagoz** rocks ten miles south by west. That's the account's 3° 37' W, which came from the lunar. By my reckoning we're thirty miles west of that, and the Triagoz are well off to the south-east. If I'm wrong and the lunar is right, though, we're heading for the Sept-Îles side of the coast, not Batz." |
| 142744 to 197993 | 20:39 to 23 Jun 11:59 | LOG `sounding` ×60 | "No bottom at twenty fathoms." Sixty casts running. |
| **147615** | **22:00** | SAID (danger by account) | "Fourteen miles to Roscoff, and the chart, by the account, has the **Triagoz** five miles south-south-west." |
| 162670 | 23 Jun 02:11 | SAID | "She's lying quietly again in forty-nine fathoms." |
| 168887 | 03:54 | SAID | "My reckoning has us near 49° 00' N, 4° 16' W after the night's drift to the north-west, which puts Batz about twenty miles south-east by south. The account still says Roscoff twenty-two miles, but from a point thirty miles further east." |
| 182220 | 07:37 | LOG `lookout.sighting` | "The Isle of Bas bearing S by W, distant four leagues." |
| 182230 | 07:37 | SAID | "That bearing puts us near 48° 57' N, 3° 58' W. My reckoning was a dozen miles too far west, and his lunar of yesterday, at 3° 46', was nearer the truth than my Eddystone run. The account has since drifted east of both. Lesson taken: neither of us trusts himself over the land. ... the **Triagoz** well to the east of our track" |
| **182233** | 07:37 | LOG `bearing.taken` (captain) | "The Isle of Bas bore S by W, four leagues by estimation." **The fix.** |
| 183060, 183300, 183360, 183480 | 07:51–07:58 | LOG lookout | Isle Verte "S, distant four leagues"; Roscoff "S, distant five leagues"; the church of Roscoff "S, distant four leagues"; Pointe de Pergueridre "S, distant four leagues". |
| 183325, 183329 | 07:55 | LOG `bearing.taken` (captain) | "The Isle Verte bore S, four leagues by estimation."; "Roscoff bore S, five leagues by estimation." |
| 183600 | 08:00 | LOG | "The land is out of sight." |
| 184105 | 08:08 | SAID | "your bearings at 07:55, Isle Verte and Roscoff both south at four and five leagues, give us a good departure." |
| 190188 | 09:49 | SAID | "We're five and a half miles off the western entrance of the Batz channel, still in forty-four fathoms." |
| 191460, 191820 | 10:11, 10:17 | LOG lookout | "The land about the Isle of Bas close aboard on the larboard bow, bearing SE by S, distant three miles."; "The Isle of Bas bearing SSE, distant three miles." |
| 192545 | 10:29 | SAID | "the Isle of Bas is three miles south-east by south ... clear of the Lavandière to the south-south-west. Forty-one fathoms". |
| 194520, 194640, 195060, 195660, 195780 | 11:02–11:23 | LOG lookout | Pergueridre "SE by S, distant five miles"; "**The Lavandière bearing S by E, distant two miles: a danger.**"; Isle Verte "SE, distant three miles"; Roscoff "SE, distant three miles"; the church "SE, distant four miles". |
| 195900, 197580, 197940, 198360 | 11:25, 11:53, 11:59, 12:06 | LOG `lookout.closing` | "The Isle of Bas bearing SE by S, steady and closing: distant three miles."; Pergueridre "SSE, steady and closing: distant four miles."; Isle Verte "SE by S, steady and closing: distant three miles."; Roscoff "SE by S, steady and closing: distant three miles." |
| **198120** | 12:02 | LOG `reckoning.noon` | "Latitude by observation 48° 51' N; the reckoning was 48° 49' N. Course made good since yesterday S by W, 54 miles. **Longitude by account 3° 59' W.**" |
| 198120–198208 | 12:02–12:03 | LOG `bearing.taken` ×6 | Bas "SE by S, two miles"; Pergueridre "SSE, four miles"; the Lavandière "SSW, two miles"; Isle Verte "SE by S, three miles"; Roscoff "SE by S, three miles"; the church "SE by S, four miles". |
| 198203 | 12:03 | LOG sounding | "And a half eighteen; sand and rock." First bottom. SAID at 198208: "fifteen fathoms now". |
| 198857, 198944, 199398 | 12:14, 12:15, 12:23 | LOG | "No bottom at twenty fathoms." (199189, 12:19: "And a quarter nineteen".) |
| 199499–199512 | 12:24–12:25 | LOG `bearing.taken` ×4 | the Lavandière "S by W, two miles"; Bas "SE, two miles"; Isle Verte "SE, three miles"; the church "SE, three miles". |
| 199784, 200001 | 12:29, 12:33 | LOG | "By the mark fifteen"; "And a half thirteen". |
| 199920 | 12:32 | LOG `master.place` | "Mr Travers came on deck, the day's work done." (Below from noon during the approach.) |
| 200107 | 12:35 | SAID | "the chart shows seven under us at low water. We're a mile and a half short of the western entrance, the Lavandière two miles south by west, the island two miles east-south-east." |
| 200213 | 12:36 | SAID | "The chart has three and a half fathoms under us at low water and the island is only a mile east-south-east." |
| 200377, 200467, 200544 | 12:39, 12:41, 12:42 | LOG | "And a half six"; "**And a half three; sand and rock.**"; "Quarter less four". SAID 200475: "the chart says this ground dries at low water". |
| 200568–200575 | 12:42 | LOG `bearing.taken` ×3 | the Lavandière "S by W, two miles"; "The Isle of Bas bore SE by E, a mile by estimation."; Roscoff "SE, three miles". |
| 200658, 200745 | 12:44, 12:45 | LOG | "By the mark five"; "By the mark seven". |
| 200760 | 12:46 | LOG | The pilot aboard. |

There is no `fix` kind in the log: the only trace of the account being moved is the `bearing.taken` line itself and the next noon's longitude.

**How far out were the two longitudes?** Against the landfall position the officer worked from the lookout's bearing (48° 57' N, 3° 58' W; I get the same from four leagues N by E of Batz):

- the account, set by the lunar, read 3° 37' W the evening before (141901): **21' east, about 14 miles** (a minute of longitude is 0.66 mile at 49° N);
- the officer's own reckoning from the Eddystone read 4° 16' W (168887): **18' west, about 12 miles** ("a dozen miles too far west", his words).

The truth lay almost exactly between them. The lunar-set account, a day's run later, was 14 miles out, which is inside the "within 20 miles" the master claimed for the lunar itself. The Eddystone run was not good to two miles: at the first line of the slice the reckoned latitude was already 10 miles out, sixteen hours after the Eddystone bearings ("Latitude by observation 49° 29' N; the reckoning was 49° 19' N"). Both longitudes were carried by the same run after 05:07 on the 22nd, so how the error was shared between them at that hour cannot be told (section 10). The captain's "the split is the thing" (182294) is literally right: the mean of the two longitudes is about 3° 57' W.

**The danger list did follow the wrong account.** It named the Triagoz at ten miles and then five (141901, 147615) while the ship, by back-reckoning from the landfall, was some twenty miles north-west of them. That part of the note stands. What the officer did with it was right: he told the captain both readings of the coast, hove to with fourteen miles in hand by the worse account, head offshore, and waited for daylight.

**When and how it came right.** 23 June 07:37:13 (182233): the captain's `take a bearing of bas`, thirteen seconds after the landfall, then the Isle Verte and Roscoff at 07:55. All three bore S or S by W, so they did not cross: it was one line of position at an estimated distance. The noon line (198120) shows the result: account 3° 59' W, latitude within 2'. From 12:35 the charted depth by account that the officer quotes agrees with the lead once the tide is added ("dries at low water" against a cast of 3½ fathoms near the top of a 24-foot tide). "Fixes from bearings once the land came up" did work.

### 6.2 The Roscoff pilot

| Tick | Time | Source | Line |
|---|---|---|---|
| 190188 | 09:49 | SAID | "The port reports the Roscoff pilot boat standing out towards us, sir." The land had been out of sight since 08:00; the `the port` reading knew of the boat 27 minutes before the lookout. |
| 191760 | 10:16 | LOG `lookout.sighting` | "Sail ho! A boat pulling off from the land right ahead, bearing S, distant two miles." |
| 192000 | 10:20 | LOG `lookout.made_out` | "The boat right ahead is the Roscoff pilots' boat, standing to the northward (N), under plain sail; French colours, the tricolour." |
| 192540 | 10:29 | LOG `port.pilot_hail` | "The boat hailed: a pilot for Roscoff; shorten sail and he will come aboard." |
| 192543–192632 | 10:29–10:30 | LOG | Officer: `heave to`; "Hove to, fore topsail to the mast, helm a-lee." SAID 192545: "She's two miles ahead ... standing out to us" (the stale 10:16 figure; a hail means four cables). |
| 193449 | 10:44 | SAID | "the pilots' boat three cables off our quarter". |
| 195221 | 11:13 | SAID | "The pilots' boat is close and should board within the half hour." |
| 198133 | 12:02 | LOG (inside a refusal's "In sight" list) | "Sail ho! The Roscoff pilots' boat on the starboard quarter, bearing W by S, distant eight cables". |
| 198148 | 12:02 | SAID | "The pilots' boat has lain three cables off our quarter for an hour and won't board. The book says the pilot only comes aboard within two cables, so we must close him." |
| 198208 | 12:03 | SAID | "the pilots' boat gone to eight cables west by south." |
| 199138 | 12:18 | SAID | "The pilots' boat has stayed exactly eight cables off whatever we do, like that frigate off Cawsand, so I don't think the game will let her close. For the builder's list: strangers seem to keep station at a fixed distance." |
| 200213 | 12:36 | SAID | "the pilots' boat, which has closed to four cables to the west." |
| 200728 | 12:45 | SAID | "the pilots' boat is four cables ahead on the larboard bow." |
| **200760** | **12:46** | LOG `port.pilot_aboard` | "The pilot, Mr Moal of Roscoff, came aboard from the boat and took charge of her (American colours being no bar at Roscoff)." She was under way, "swinging west at four knots" (SAID 200384). |
| 202140 | 13:09 | LOG `lookout.sail_lost` | "The boat abeam to larboard is out of sight." |
| 258540 | 24 Jun 04:49 | LOG `port.pilot_hail` | "The pilot asks for sail to be shortened: his boat is coming off for him." |
| 258600 | 04:50 | LOG `lookout.sighting` | "Sail ho! The Roscoff pilots' boat on the larboard quarter, bearing SE by S, distant a mile." |
| 258672 | 04:51 | LOG | Hove to. |
| 259500 | 05:05 | LOG `port.pilot_hail` | "The boat hailed: she has come off for the pilot." |
| **259680** | **05:08** | LOG `port.pilot_left` | "Mr Moal left her in the boat, clear of the western entrance of the channel of Bas; the pilotage, £3, paid and his certificate signed." |
| 260880 (just past the slice) | 05:28 | LOG | "The boat on the starboard quarter is out of sight." |

**From hail to boarding: 2 h 17 m.** She lay hove to for him 1 h 33 m (10:30 to 12:04), drifting about a mile towards the island (Bas "distant three miles" at 10:17, "two miles" at 12:02) with three marks hailed "steady and closing" and a fourth two minutes after she filled. What was tried: heaving to at the hail (as the hail asks); waiting; reading primer 14; filling away, a refused tack, wearing, steering WSW for the boat; then, on the captain's word, giving the pilot up and steering for the entrance. He boarded when her track, hauling west off the shoal, passed the boat. Nobody had asked for him at that moment: the captain had said at 198310 he would go in without (note 9). No `ask the pilot ...` was ever given; there is no `pilot.answered` line in the whole voyage.

**Why he would not board** (SOURCE, not run; it fits the log's figures):

- `world/ports.py`, `_tick_pilot`: once a minute, hail if the true distance is within 4 cables; board (or leave) if within **2 cables** and her speed over the ground is 6 knots or less. Being hove to is no bar.
- `world/ships.py`, `Vessel.tick`: the boat's plan is `("to_ship", 2 cables)`. She steers for an **intercept point** (the ship's position run on at her way), and "arrives" when within `2 cables × ARRIVE_FRACTION (0.75)` of *that point*. On arriving her plan becomes `("lie_to", inf)`: "she lies to under the ship's lee until whoever sent her gives her a plan."
- With the schooner standing S by W at three knots towards a boat pulling north at four, the boat is 1.5 cables from the meeting point when the two are still about 2.6 cables apart. The officer hove to in that same minute (order at 10:29:03, three seconds after the hail). A four-knot boat still steering for a ship three cables off would have been alongside in a minute or two; she was not in ninety-four, so her plan was no longer to come to the ship. She had "arrived", lay to for good about three cables off, and nothing in her plan would ever close the last cable. The hail's own advice, "shorten sail and he will come aboard", is what prevented it.
- Leaving on the 24th worked because the schooner was already hove to (04:51) when the boat was a mile off: with the ship nearly still the intercept point is nearly the ship, so the boat's 1.5 cables fell inside the two.

**Why the distance "didn't change"** (SOURCE): `world/lookout.py`, `_judge` (lines 362–386) and `ESTIMATE_HOLD_NM = 1.0`. The distance by estimation of every sighting, **other sail included**, is "drawn once an episode and held while she has not moved a mile from where it was judged", where "she" is *our* ship. Bearings are live. So a boat's distance cannot change in the list, the hail or a bearing while the schooner lies hove to or at anchor, however the boat moves. That fits the three plateaux the model reported: three cables at 10:44 and still his figure at 12:02; eight cables once she had drifted about a mile (the game's own list at 12:02, and his "exactly eight cables" at 12:18); four cables at 12:36 and still at 12:45, after another mile under sail. It also answers the note's question about the frigate at Cawsand (the schooner was at anchor, and the frigate's first hail at tick 0 was also "distant eight cables"): the figure is held, the ship is not circling. The estimate is also rounded to whole miles above 0.95 mile (`geo.estimate_words`).

**The boat's distance when he left.** The only figure in the log is "distant a mile" at 04:50, eighteen minutes before. By the rule above the boat hailed inside four cables at 05:05 and was inside two at 05:08. The mile is the held estimate (the schooner was hove to and had not moved a mile). So the two-cable rule is applied on leaving as on boarding; what misled is the lookout's figure.

**The pilot's words** (LOG 200760, `port.pilot_words`, in full): "The pilot says: The western passage is the easier. Come to the end of the isle within cannon-shot, where a single rock stands about a third of the way to the main: that is the Lavandière. Steer close by it, as near as an oar's length, keeping it on the starboard side and the Couillon, a rock under water twice a ship's length from it, on the larboard. Within them haul a little toward the island and put a man on the mizzen yard for the two rocks near the shore; the water is very clear here. The eastern passage by Roscoff is for high water only and with a pilot; at low tide there is no passing at all. The church of Roscoff with its lantern belfry stands over the harbour at the channel's eastern end; the Isle Verte lies off the town. The Lavandière at the western entrance is your mark going in, kept close aboard to starboard; about the middle of the isle you will see a great cove with several houses on it. Anchor over against the cove in the middle of the isle, in three or four fathoms at low water on sand, sheltered from the sea by the island. The harbour of Roscoff dries at low water and is for vessels that take the ground; a ship lies in the road. High water at Roscoff about two o'clock in the afternoon, the tide rising some 24 feet; the flood is making now and serves." News (200760): "Britain at war with the Batavian Republic, France and Spain; the United States, Portugal and Denmark at peace with all."

They were useful at once: they corrected the officer's tide ("so I had the tide backwards and it's rising under us", 201008) and let him catch the captain's course ("on 160 she'll pass down our larboard side, south of the rock, the wrong side by Mr Moal's directions", 203038). They were never sailed: the wind died and she anchored outside.

**The course in after he boarded** (all the captain's): W by S (200588), "Bear off a point" to WSW (201095) and SW by W (201450), S by W (201627), "Meet her" on SW by S (201699), `Steer 160` (202721), 150, ESE, 140 (202991 to 203014). The Lavandière drew from "S ... two miles" (200880) to "S by E, a mile" (201597) to "SE by S, a mile" (202372, 203004) before she lost steerage way.

### 6.3 The shoal north-west of the Isle of Bas

LOG, 23 June: steering S by W for the entrance at about three knots, the lead gives 15 (12:29), 13½ (12:33), then after the urgent "Taken aback" and the turn west 6½ (12:39), **3½ (12:41)**, 3¾ (12:42), 5 (12:44), 7 (12:45), 10, 12¼, 13¾, 16¼ (12:48 to 12:53). The Isle of Bas "bore SE by E, a mile" (200571). The officer read from his chart figure that "this ground dries at low water" (200475).

- **No lookout line warned of it.** Between 12:06 and 12:48 the lookout says nothing. The only danger hailed all day is the Lavandière, two miles off. The shore itself was hailed once, at 10:11, and by the lookout's rule is not hailed again while a named mark is in sight (SOURCE: `lookout.py`, `SHORE_CLOSE_NM`: "when no headland of the chart is in sight").
- What saved her was the lead and the captain's chart: the officer's three-minute 'close lead' was entered at 12:35 (200107), six minutes before the 3½, and the captain's "un landmarked land" warning came at 200139.
- Leaving on the 24th she crossed shoal ground again: "Quarter less eight; sand and rock." at 04:29 (257345) between 12½ and 18¾.

### 6.4 Anchoring, the night, weighing

- **Anchoring.** Order 203633 (13:33:53); "All hands! (to come to anchor)"; "Let go the topsail sheets; clew up; haul down the jib. Helm down for W." (203784); "The best bower let go in twelve fathoms and a half." (203969, 13:39); "Veered to sixty-two fathoms; brail up the spanker." (204020); "Brought up by the best bower in twelve fathoms, sixty-two fathoms of cable; Riding by the best bower to the flood, the wind across the tide." (204837, 13:53). Clean. The officer announced "eighteen fathoms" (203634); she had drifted into 12½ by the time the anchor went. The lead was not hove for 24 minutes of it: 'close lead' "held; the last firing's work is still waiting its turn" five times (204067 to 204787).
- **Where she lay.** The officer says "a mile north-north-west of the Lavandière" three times (203634, 204844, journal 224654), from bearings of "a mile by estimation" at 12:59, 13:12 and 13:23. When the fog lifted next morning: "The Lavandière bearing S by E, distant **five cables**: a danger." (255600). The held estimate again: inside a mile of a rock the figure cannot improve until the ship has moved another mile.
- **The night.** "The cable slack at the turn; she swings to the ebb." (216780, 17:13) and "... she swings to the flood. Riding by the best bower to the flood, a windward tide, the wind against the tide." (239280, 23:28). Depths by the lead: 11¾ falling to 10¼ (13:57 to 17:00), then 13½ to 15 within five minutes of the swing (17:18 on), then through the night 14 (19:55), 14½, 14¾, 14¾, 15¼, 15¾, 16, 17½ (23:25), 15¼, **11¾** (00:25), 13, 11¾, **16¾** (01:55), 17¼, 16½, 14½, 14½ (03:55). Five-fathom jumps between half-hourly casts, with no dragging line. The officer's "twelve to seventeen fathoms with the tide and no sign of dragging" (255400) reads them as tide; they look like her ranging about the anchor over steep ground, which makes the lead a poor drag alarm here.
- **Weighing.** `get under way on the starboard tack and steer NNW` (255460), given in fog "a cable's visibility" (SAID 255400). LOG: "All hands up anchor! ..." (255461); "Let fall! Sheet home! Hoist away the topsails! Brace up the after yards for the starboard tack, the head yards abox." (256383); "The best bower is aweigh." (256512); "Let go the downhauls, hoist away the jib! Helm a-lee for the stern-board." (256512); "**She has paid off**; right the helm, brace round the head yards, set the spanker." (256513, one second later); "Under way on the starboard tack, under the topsail and the mainsail and the jib; the best bower catted and fished; full and by (NNW (338°) lying too near the wind to be laid)." (256898). **She cast at once onto the ordered tack; no sternway, nothing backed by hand.** She was tide-rode with the wind against the tide. Afterwards the officer set the foresail, fore staysail, flying jib and gaff topsail and steered NW by W (256902–256903); the captain trimmed the mainsail, headsails and foresail by name (257342, 257475, 258314), 'trim' being still belayed.

### 6.5 Trade at Roscoff

- **The market** (LOG 212080): "The mate's list of the prices at Roscoff is aboard: brandy £100, geneva £70, rum £80, tea £170 a ton, and the rest." The officer's reading of the list (212098): brandy £100, rum £80, geneva £70, tobacco £60, tea £170, tin £255, salt beef £70, wine £38, salt £12, canvas £42, onions £6.
- **What it would not take.** One refusal: 212090 `sell forty tons of coal` → "Roscoff's market has no coal; it deals in brandy, geneva, rum, tea, tobacco, wine, salt, canvas, onions, tin, salt beef." The pilchards were never offered; the officer inferred it from the list: "Roscoff takes neither coal nor pilchards, so my outward cargo can't be sold here ... I was wrong to buy it blind." The ship learned this more than two days and a Channel crossing after buying (coal 21 June 07:09, pilchards 11:46), and only after anchoring and a two-hour boat trip.
- **The brandy.** 212162: "Bought 16 tons of brandy at Roscoff at £100 a ton, £1600 paid; the boat goes for it. The purse: £34." (£1,634 before, by the officer's count at 212098; £31 after Mr Moal's £3, by arithmetic.) 224147: "16 tons of brandy hoisted in and struck down into the hold; the manifest 40 tons of coal, 20 tons of pilchards, 16 tons of brandy; room for 36 tons."
- **The boat trips.**

| Trip | Ordered | Away | Landed | Shoved off | Alongside | Total | Carried |
|---|---|---|---|---|---|---|---|
| Prices | 204842 (13:54) | 205120 (13:58) | 207554 (14:39) | 209354 (15:09) | 212080 (15:54) | 2 h 01 m | "The price list written up by the mate" |
| Brandy | 212162 (15:56) | 212454 (16:00) | 214900 (16:41) | 221380 (18:29) | 224147 (19:15) | 3 h 20 m | 16 tons in one boat-load (1 h 48 m at the quay) |

  The 4½ hours of the note is Plymouth's coal trip (7792 to 24364, 4 h 36 m), not these. Each way was about 41 to 46 minutes at the boat's four knots: she lay nearly three miles from the quay, outside the channel, and `the port` still counted her "at anchor in Roscoff" (SAID 204844).
- The papers are "written up by the mate" (212080, 212162) while the mate's place is held by the officer of the watch.

### 6.6 The officer's standing orders

| Order (by the mate) | Life in the slice | Behaviour |
|---|---|---|
| 'inshore lead': "every 10 minutes, if the land is in sight then heave the lead" (from tick 113) | belayed 201583 | Held correctly while the land was out of sight (one "not carried out" line a watch); began casting at the landfall. |
| 'night lead': "every 30 minutes then heave the lead" (140863) | belayed 184102 | 24 firings, 24 "No bottom at twenty fathoms". It was meant "to find the fifty-fathom line in the dark" (140868), which a twenty-fathom hand lead cannot do. |
| 'approach lead': "every 10 minutes then heave the lead" (184102) | belayed 201583, resumed 255460 | 36 firings. With 'inshore lead' it gave a cast every 4 to 6 minutes once the land showed. |
| 'close lead': "every 3 minutes then heave the lead" (200107) | belayed 224654, resumed 258097, belayed 258543 | 133 firings. Entered six minutes before the 3½-fathom cast. Then **left running at anchor for 5 h 27 m: 110 notable soundings** (13:57 to 19:24). |
| 'anchor lead': "every 30 minutes then heave the lead" (224654) | belayed 255460 | 17 firings overnight. |
| 'trim': "at a wind shift then trim sails" (from 83157) | belayed by the captain 162559, resumed 169036, belayed by the captain 193417, not resumed | 7 firings in the slice. **Twice it fired with her hove to and filled her** (162102: "Fore topgallant filled again", "Fore staysail filled again", "Fore topsail filled again"; 193303). None of the seven firings has a `wind.shift` line near it: the standing order's event and the log's line are separate tests under m5c-b, so the log shows the trim and not its cause. |

- "Not hands enough on deck to heave lead" appears three times: 193314 (two lead orders in force), 200544 (three), 202448 (one). Each time the watch was bracing and trimming ("the watch is bracing the fore topsail yard and the fore topgallant yard and trimming the foresail"). It is the trim evolution taking the whole of a small watch, more than the count of lead orders. The officer belayed two of the three lead orders at 201583: "three of them were fighting for hands with your trimming."
- With 'trim' belayed and nobody trimming, the officer changed course twice after wearing (WSW at 198776, S by W at 199136) with the yards still "braced sharp up on the starboard tack" (198768). 24 minutes later: "Taken aback: the sails pressed against the masts and she lost her way." (200205, urgent), in shoaling water.
- "Trim sails" trims to the wind as it bears at that second: 200212 `steer W` and 200213 `trim sails` ("120° on the larboard quarter"), then trims at 200414 ("90° on the starboard beam"), 200497 ("54° on the starboard bow"), 200663 ("45° on the starboard bow"): six trims in eight minutes of one turn.

### 6.7 The hand lead against the depth

- 67 "No bottom at twenty fathoms" in the slice, every one a notable line; sixty in a row from 22 June 20:39 to 23 June 11:59, while the officer quotes a depth of 48, 49, 44 and 41 fathoms from his readings (140868, 162670, 190188, 192545). No contradiction: it is deeper than the line.
- The one minute where both figures are on record: 12:03, the cast "And a half eighteen" (198203) and the officer's "fifteen fathoms now" (198208). The difference is the tide (about two hours before a 24-foot high water). The no-bottom casts at 12:14, 12:15 and 12:23 fall between casts of 18½, 19¼ and 15: a charted 16 or 17 plus the tide is over the hand lead's twenty.
- **A deep-sea lead exists** (primer 10: `heave the deep-sea lead`, `strike soundings`), and the captain used it later in the voyage (497021; "Fifty fathoms; fine grey sand with black specks." at 498051). The officer never tried it in this slice.

### 6.8 Taken aback and wind shift under m5c-b

- **`ship.aback`: 6 lines.** Notable ×4, all "Her sails aback in the light air; she has lost what way she had." (169114 at 03:58; 202435 at 13:13; 203273 at 13:27; 203454 at 13:30). Urgent ×2, "Taken aback: the sails pressed against the masts and she lost her way." (200205 at 12:36, in a nine-knot breeze with gusts of twelve: fair; and **203621 at 13:33**). The second came seven seconds after the officer reported "two knots of air from right astern and no speed" (203614), with the nearest gust lines "A gust: 6 knots, the mean 4." (13:02) and "A gust: 4 knots, the mean 3." (13:39). By the build's own rule (way on her, four knots of apparent wind) it looks like one that should have been notable.
- **Worst span**: 13:27 to 13:35. Three `ship.aback` lines in under six minutes and "Fore topsail taken aback." seven times (203417, 203454, 203478, 203517, 203621, 203686, 203758), each followed by a routine "Fore topsail filled again."
- **Per-sail `sail.backed`: 40 notable lines, 17 of them from heaving to or backing on purpose** (for example 147937–147949, 192608–192638, 258636–258654: "Fore staysail taken aback.", "Fore topsail taken aback." as the direct result of `heave to`).
- **`wind.shift`: 24 lines, all on 23 June, 22 of them between 12:56 and 17:45.** Wording: "Wind backed to N by W, a gentle breeze." (201376); "Wind veered to ENE, light airs." (203976). Strength named: light airs 19, calm 2 ("Wind veered to W by S, calm." 215138; "Wind veered to WNW, calm." 216057), a light breeze 2, a gentle breeze 1. Densest: five in 14 minutes while anchoring (13:39 ENE, 13:40 E by S, 13:50 SE, 13:52 SW by W, 13:53 W), and "veered to WNW" at 17:00 followed by "veered to ENE" at 17:05. The ten-minute mean itself went more than once round the compass in an afternoon of one to four knots.

### 6.9 Log volume

- **Soundings are 225 of the slice's 435 notable lines (52%)**: 67 no-bottom, 110 from the three-minute lead at anchor.
- `evolution.waiting` 51 and `evolution.short_handed` 30: 48 of the 81 fall between 12:36 and 13:23, when twelve `trim` orders each produced three to six lines ("Not hands enough on deck to trim the jib; the watch is ...").
- 68 "Compression eased to 1x" lines.

### 6.10 Smaller oddities of wording

- "The land about the Isle of Bas **close aboard** on the larboard bow ... distant three miles." (191460).
- "The Isle of Bas bearing SE by S, steady and **closing**: distant three miles." (195900), the same three miles as at 10:17: the line is triggered by the true distance and prints the held estimate.
- "Roscoff bearing ESE, distant two miles." and "The church of Roscoff bearing ESE, distant four miles." in the same look (255600); three and four miles at 11:21 and 11:23.
- Ship-rig words in a schooner: "brail up the spanker" (204020), "set the spanker", "Hoist away the topsails", "the head yards abox" (256383, 256513); the pilot's "put a man on the mizzen yard". The main gaff topsail is called "a jibheaded sail" (201078).
- "A gust: 1 knots, the mean 1." (215067); "A gust: 4 knots, the mean 4." (220212).
- The order echo doubles the stop: "Order: Tell the officer ... but you have the con.." (200139); "Asked the officer of the watch: ... I'm not sure.?" (126041).
- Primer 14's Roscoff example names "Mr Cabioch" and "the cutter"; the officer, fresh from reading it, said anchoring "would lose us Mr Cabioch" (198216) forty minutes before Mr Moal came aboard from "the boat".

## 7. The model as an officer

**Good calls.**

- The longitude. He kept his own reckoning beside the account, told the captain plainly what each implied ("If I'm wrong and the lunar is right, though, we're heading for the Sept-Îles side of the coast, not Batz", 141901), and chose the course that was safe under either: wear first so she lay head offshore (147615), heave to fourteen miles off, close at first light.
- The landfall. He worked the position from one bearing and distance before the captain had typed his own, and gave up his own figure without fuss: "I owe Mr Travers an apology ... neither of us trusts himself over the land." (182230).
- The lead. A cast every ten minutes in the haze, and every three minutes six minutes before the shoal. He answered each shoal cast in four to eight seconds.
- Speaking up to the captain: "Sir, one caution on 160° ... the wrong side by Mr Moal's directions" (203038); "Sir, we just crossed helm orders ... One voice on the helm: is it yours from here, or mine on your course?" (200670).
- Knowing his limits and saying so: "You were right, and quicker than my stand-by could be. With this wind boxing the compass every few minutes so close in, the helm wants a hand that sees every gust, and you have the window. I'd suggest you keep the helm and sails for the approach." (200728).
- Asking for the one allowance he lacked by its exact name, with his reasons, while she drifted (203614).
- Trade: prices laid out, the sum done right ("sixteen tons of brandy at £100. Plymouth paid £315, so that's about £5,000"), his own mistake owned, leave asked before spending the purse (212098).
- The journal at 224654 would let a relief take the ship cold.

**Mistakes.**

- 'trim' left standing through two heave-tos (162102, 193303), the second after promising otherwise (169037). His own account: "My fault again, sir" (193441).
- After the wear at 12:12, two new courses and no trim, with the automatic one belayed: the urgent taken-aback at 200205 was his. He called it "A gust from north-east by east ... since I'd belayed the trim order" (200213); the captain had belayed it.
- An hour and a half hove to for a pilot who was not coming, on a lee shore, before opening the book (192543 to 198134). At 11:13 he still expected him "within the half hour".
- The tide backwards at the worst minute: "with the ebb now running" (200384), "the ebb running off it" (200475); it was two hours of flood yet. The pilot corrected him.
- A twenty-fathom hand lead set "to feel for the fifty-fathom line" (126011, 140868): 24 night casts that could not find it, and the deep-sea lead never tried. (From 08:08 the same casts had a sound purpose, the twenty-fathom mark.)
- "That's a fair wind for Plymouth if it holds" of a north-easter with Plymouth north by east (224156); the captain corrected it.
- The three-minute lead left going for five and a half hours at anchor.

**Stated as fact and wrong, or stale.** "water sail furled" (140868); "She's two miles ahead" at the hail (192545); "thirty miles west" and "thirty miles further east" for 36' of longitude, which is 24 miles (141901, 168887); "Coming to an anchor ... in eighteen fathoms" (12½); "a mile north-north-west of the Lavandière" (five cables); "Six and a half fathoms ... That's below my six-fathom mark" (200384). None invented from nothing; most are a figure a few minutes old, or the game's held estimate, repeated with more confidence than it deserved.

**How he took refusals.** Briskly: three tries at the water sail and the group order within a minute, each failure reported for "the builder's list" (140928); a refused tack turned into a wear in four seconds; "sixteen" into "16" in two. He wrote the working forms in his journal.

**What he said of the game itself.** 140928 (the water sail's three failures); 162670 ("with the condition "if she is not hove to", if the book will take one"; never tried); 193449 ("I'd ask the builder for "trim" to stand aside by itself while she lies to"); 199138 ("strangers seem to keep station at a fixed distance"); 200728 (the stand-by cannot see a gust); 204844 ("the port counts us as "at anchor in Roscoff""); 212166 ("the number words above twelve seem to be missing").

**Manner.** In voice throughout, and warm without being arch: "One cask is marked for the officers' stores, which I'll guard with my life." (212166). Wordy for a deck (mean 84 words a speech, 210 at 224377); the captain never objected.

## 8. Cross-check against the notes

**The owner's items.**

| Item | Evidence in this slice | Verdict |
|---|---|---|
| 1. Pilot boarding under way | Mr Moal boarded under way at about four knots (200760) and could not board the ship hove to for him; he left her hove to (259680). SOURCE gives the cause (6.2). | ADDS NUANCE: as built, heaving to at the hail is what stops the boarding. |
| 2. The well | Not sounded in the slice. | Cannot be seen. |
| 3. Price list from each port | "The price list written up by the mate: the prices at Roscoff brought off by the boat." (212080); the officer copied both lists into his journal by hand (224654). | SUPPORTS. |
| 9. Pilot automatic; hailing wanted | The captain had given the pilot up (198310); he "came aboard ... and took charge of her" all the same (200760). The officer looked in the library for "hail the pilot" (198134) and found no order. | SUPPORTS. |
| 10, 11. The journal | Not lost here. The owner asks for a status entry before a long stand-by (224642). The station's journal is 73 stand-by lines in 89. | ADDS NUANCE to 11. |
| 12, 14, 23. Re-seating, restarts, doors | Nothing in the slice. | Cannot be seen. |
| 13. Multi-condition stand-by | 37 stand-bys for "a sounding"; three for "the pilot aboard" ended by his own word; the captain's three "tell the officer" standing orders as a workaround. | SUPPORTS strongly. |
| 15. General authority | One allowance had to be asked for and given while she drifted without steerage way (203614 to 203629, 15 s). Bearings: 29 by the captain. Allowances "for the watch" lasted three days. | SUPPORTS. |
| 16. "Keep" orders | 'trim' filled her out of the heave-to twice (162102, 193303); the captain "keeping the sails trimmed between your samples" (200412), 12 trim orders by hand. | SUPPORTS. |
| 17. Taken aback | 4 notable, 2 urgent; the urgent at 203621 came in three to four knots of air with "no speed". | ADDS NUANCE: mostly fixed; one doubtful urgent. |
| 18. Wind-shift lines | 24 lines, 22 in under five hours of light airs and calm (6.8). | SUPPORTS the model's rider. |
| 19. Reckoning close to land | The 3½-fathom cast a mile off Bas with no lookout line (6.3); the Lavandière "a mile" at anchoring and five cables at dawn. | SUPPORTS the lookout idea. |
| 21. A turn ending on `say` | After a `say` the model had to send a stand-by 50 s later (8 of 10 "out of turn"); at 198148 a `say` and a stand-by went with no order between. | SUPPORTS. |
| 24, 25. Coast without marks; images | "My chart shows some un landmarked land off the bow and larboard bow" (200139). The officer had named marks only. | SUPPORTS strongly; this is the afternoon the note quotes. |
| 4. Primer clean-up | The Roscoff example's "Mr Cabioch" taken as fact (198216). | Small support. |
| 5, 6, 7, 8, 20, 22 | Browser, chart and other sessions. | Cannot be seen. |

**The model's comments and additions.**

| Claim | Evidence | Verdict |
|---|---|---|
| "Mr Moal boarded only once we sailed down to his boat." | 192540 hail, 200760 aboard, under way. | SUPPORTS. |
| "It had held eight cables off for an hour." | His own lines: three cables 10:44 to 12:02, eight 12:02 to 12:18, four 12:36 to 12:45. | CONTRADICTS in detail; the plateaux are the held estimate. |
| "Mr Moal left in his boat while it was still a mile away ... the 'two cables' rule is applied on boarding but not on leaving." | "distant a mile" is from 04:50; the boat hailed at 05:05 and he left at 05:08. SOURCE: one test serves both. | CONTRADICTS: the rule is the same; the lookout's figure was stale. |
| Price lists: show what a port trades in before its prices are known. | 212090. | SUPPORTS. |
| "'a sounding' also wakes on 'no bottom at twenty fathoms'" | Nine wakings, 08:29 to 09:49. | SUPPORTS. |
| "about fifteen permissions one by one" | 14 allowance lines in the first two minutes of 21 June (13 distinct things), "keep her full" twice that afternoon, "come to an anchor" here. | SUPPORTS. |
| 'trim' "fired while she lay hove to and filled her out of it, twice." | 162102 and 193303, both here. | SUPPORTS exactly. Adds: `heave to` is then refused as "hove to already" (193441). |
| "The urgent alerts stopped." | 203621. | ADDS NUANCE. |
| "A lunar 'trusted within 20 miles' replaced an account that a recent Eddystone bearing had made good to about 2." | At the landfall the Eddystone run was 12 miles out and the lunar account 14; the reckoned latitude was 10 miles out at noon on the 22nd (111720). | CONTRADICTS the premise. Blending the two would have been right within a mile or two; neither "replace" nor "keep" would. |
| "The account jumped 33' east ... it had us 'on' the Triagoz while we were 20 miles west of them." | 86831; 141901; 147615. | SUPPORTS (about twenty miles north-west by back-reckoning). |
| "Once the land is in sight, [the danger list] should come from the best fix." | The captain's bearing 13 s after the landfall did that; the officer could not have. | ADDS NUANCE. |
| The relay's 60 s and `--wait 50` | The 50-tick pattern (section 5). | Consistent; no cut seen. |
| "The officer isn't treated as a person on deck." | Papers "written up by the mate" while he holds the deck. | Small support. |
| Contrary-orders warning on ordinary sequences | 198312, 198776, 199136, 212162: the note's two examples are these. | SUPPORTS exactly. |
| "The schooner's 'get under way' doesn't cast her head onto the ordered tack ..." | Not at Roscoff: "She has paid off" one second after "aweigh" (256513). The case is Plymouth, 21 June (38157 to 38659: "she hasn't paid off ... gathering sternway"). | Cannot be seen here; this weighing was clean. |
| "'Trim sails' acts before the helm has swung" | 200212 to 200663. | SUPPORTS. |
| Hand lead "no bottom" while the depth reads 15 or more; "confusing without a deep-sea lead" | 12:03 to 12:23 (6.7). | SUPPORTS the first half; CONTRADICTS the second: the deep-sea lead is in the game and was not tried. |
| "Three of them at once caused 'not hands enough to heave lead'." | Three such lines, with two, three and one lead orders in force, each during a trim. | ADDS NUANCE. |
| "Each boat trip carries one bargain and takes about 4½ hours" | Roscoff: 2 h 01 m and 3 h 20 m. | ADDS NUANCE (4½ h is Plymouth). |
| "Other ships keep a fixed distance ... cached or ... circling?" | 6.2, SOURCE `_judge`. | ANSWERS it: held, and held by *our* ship's movement. |
| Water sail (four lines) | 140862 to 140925. | SUPPORTS all four, with the cause. |
| "Number words above twelve fail." | 212160; the table. | ADDS NUANCE: the teens bar fifteen, and compounds. |
| "'Full and by' is refused ..." | Refusal at 43089, outside the slice; accepted here at 258096. | Cannot be seen here. |
| Worked well: the pilot's directions | 200760, 201008, 203038. | SUPPORTS; never sailed. |
| Worked well: fixes from bearings | 182233; 198120. | SUPPORTS. |
| Worked well: quieter aback lines | 6 `ship.aback` lines, against 40 per-sail lines. | SUPPORTS with the rider. |
| Worked well: number-free standing orders | Four lead orders entered first time in the slice (140863, 184102, 200107, 224654); belay and resume by name worked every time. | SUPPORTS, with the hove-to rider for 'trim'. |
| Worked well: the noon latitude; the ship's papers | 111720, 198120; 212080, 212162; "No. 7" canvas in his answer matches the ship file. | SUPPORTS. |
| Worked well: "what is she" | Not used in the slice. | Cannot be seen. |

## 9. New findings not in the notes

Ranked by weight.

1. **A ship that heaves to at the pilot's hail is not boarded.** 192540 to 200760: 2 h 17 m, 1 h 33 m of it hove to on a lee shore. SOURCE: the boat stops for good ("lie_to", inf) within 1.5 cables of a predicted meeting point, which is about three cables from a ship that then stops; boarding needs two. The notes have the symptom; this is the cause.
2. **The lookout's distance is held until our own ship has moved a mile, for vessels and for rocks alike.** Explains the "fixed distance" of the pilot boat and the Cawsand frigate, the "mile away" at Mr Moal's leaving, the Lavandière called "a mile" three times and found at five cables (201597, 202372, 203004 against 255600), and "steady and closing: distant three miles" (195900). It is at its worst inside a mile of a danger, where a mile's movement is the whole problem.
3. **The shoal north-west of the Isle of Bas: 15 fathoms to 3½ in twelve minutes (199784 to 200467), on ground that dries, with no word from the lookout.** The officer had no reading that could show it; the captain's chart did (200139).
4. **A captain's word that arrives during the officer's open turn is counted as delivered and does not wake the stand-by entered a second later.** Five cases here; the shoal warning waited 66 s for an unrelated urgent line (200139), a direct question two hours (204890).
5. **The hove-to state outlives a trim that fills her.** After 'trim' filled her at 193303 the officer's `heave to` was refused: "She is hove to already; fill away before heaving to again." (193441). The captain restored her with six separate orders. "Trim sails" should be held while she is hove to, or should end the state.
6. **Half the notable lines are soundings (225 of 435); 67 say "No bottom at twenty fathoms".** A no-bottom cast could be routine, and "a sounding" as an event could mean bottom found.
7. **An officer who may not take a bearing.** 29 bearings typed by the captain during the approach and at anchor, in rounds of up to six. The names need their accents: `take a bearing of the lavandiere` is refused (198133, 198155).
8. **"Furl" is refused for jib-headed sails, the gaff topsail and the studding class** (201077, 201078, 140866), and "back the fore staysail" for want of a yard (193432).
9. **The 'at a wind shift' event and the log's wind-shift line have parted company under m5c-b.** Seven 'trim' firings with no shift logged; then 24 shifts logged in light airs with 'trim' belayed.
10. **`the port` reports the pilot boat coming off 27 minutes before any eye can see it**, with the land out of sight in haze (190188 against 191760).
11. **The lead as a drag alarm is blind over steep ground**: five-fathom changes between casts at anchor with no dragging (6.4).
12. **The owner uses `tell` for everything, questions included** (15 tells, 1 ask). A `tell` that ends in a question mark owes no answer by the rule, and one went two hours without (204890).
13. **The reckoning ran 10 miles ahead of the observed latitude in sixteen hours of fair weather** (111720), which is the size of error that made the longitude argument what it was. Cause not visible here.
14. Wording: the items of 6.10.

## 10. Could not determine

- **The true position at any time.** The dumps hold the account and the lookout's words, not the truth. So: whether the old account was good when the lunar replaced it (05:07 on the 22nd); the ship's real distance from the Triagoz at 22:00 (my "about twenty miles" is back-reckoned from the landfall with the Triagoz at their real-world place, near 48° 52' N, 3° 39' W); how close she passed to rock on the shoal.
- **What the model was shown.** No tool results are saved. I cannot tell whether a folded captain's word reached the model before its stand-by; what the danger list held during the approach; where the wrong tide ("the ebb now running") came from; or the readings behind "three cables", "eight cables" and "four cables".
- **The lost `fill away` at 198148.** No `submit_order` is in the transcript before "my fill-away didn't go through". Either the model never sent it or a call made out of turn came back unrun (the notes describe "Nothing was run" for a hand-over). The dump cannot say.
- **The pilot boat's true track.** The mechanism in 6.2 is read from the source and fits the log's figures; I did not run it.
- **Whether the urgent "Taken aback" at 203621 met the build's own test** (way on her, four knots of apparent wind): the instant values are not logged.
- **Whether the depths at anchor were swinging or a slow drag.** No dragging line; the pattern fits swinging; not proved.
- **Whether the bearings taken at 12:02 to 12:25 moved the account while the master was below** at the day's work (`master.place` 199920).
- **Wall-clock times and the compression in force**, hence how long the owner waited on any turn.
- **Whether the mainsail and foresail came in by the anchoring evolution or by the captain's "Take in the fore and aft sails"** (204477): no line says.
