# P5. Speedwell off St Mary's, ticks 521,460 to 558,434 (27 June 1805, 05:51 to 16:07)

## 1. Slice identity

- **Session** `4-schooner-plymouth-opus`, **ticks 521,460 to 558,434** (36,974 s, 10 h 16 m), ship's time **27 June 1805, 05:51:00 to 16:07:14**, the end of the game (save `freesail-seed7-tick558434`).
- **Ship**: the merchant topsail schooner *Speedwell* (scenario "A merchant schooner, free", seed 7, American colours, complement 40; cargo 40 t coal, 20 t pilchards, 16 t brandy; purse £28 after the pilotage).
- **Station**: officer of the watch, the mate ("in the place of Mr Ray"), **Opus 5.5 through the MCP door**, the **third seating** (seated tick 343,551; deck held without a break since tick 398,710, 25 June 19:45). The captain is the human owner.
- **Build**: m5c-b.
- **Size**: 1,459 log lines in the slice (the condensed file shows about 1,000); 221 transcript entries (nos. 607 to 827).

**Sources, and how each statement below is marked.**
- **[LOG]** the dumps (`log-full`, `condensed.part6`, `transcripts`, `inputs`, `agent-journals`). Tool results are not stored, so what the officer was shown is known only from what he then said.
- **[SAID]** a claim by the officer or the captain, not otherwise confirmed.
- **[CODE]** the m5c-b source and data, read only (`freesail/world/ports.py`, `freesail/evolutions/runner.py` and `scripts.py`, `freesail/world/reckoning.py`, `lookout.py`, `weather.py`, `geo.py`, `core/world.py`, `api/readings.py`, `data/ports/st-marys.yaml`, `data/charts/features/channel-west.yaml`, `data/ships/topsail-schooner.yaml`, `data/evolutions/*.yaml`).
- **[CKPT]** the final checkpoint `saves/freesail-seed7-tick558434.checkpoint`, read in memory with a stub unpickler that imports nothing from the game (no game code was run, nothing written). It gives the truth at the last tick: true position, the account, the boat, the pilot, the purse, the anchors, the hull's motion, and the reckoning's stored bearings and track.
- **[RECON]** my own reconstruction: least-squares cross-bearing fixes from the exact bearings the reckoning stored for each of the captain's bearing rounds [CKPT], against the feature positions in the chart file [CODE]. Residuals are 0 to 3 degrees; take the fixes as good to about a cable. This is the only "truth" I have for times before the last tick.

## 2. What happened

All times 27 June, ship's time; ticks in brackets.

1. **05:51** (521460) Mr Ellis, the St Mary's pilot, "came aboard from the gig and took charge of her" as she lay hove to about 3 miles SE of Peninnis; his directions are logged in full. **05:52** (521548) the captain: "don't mind the pilot too much ... he's not able to steer her properly yet. His message is the extent of it".
2. **05:54** (521644) the officer fills away; `clear away the bowers` is refused with "('let go' was understood.)" and the captain asks "Wait, did you mean to drop anchor here?" (521669).
3. **05:55 to 06:49** she stands in NW by W at about 3 knots under fore topsail, staysail and (by the captain's hand) gaff topsail, the officer's `close lead` casting every three minutes: 19 casts, all "No bottom at twenty fathoms." Six course orders (300 at 05:55, then 295, 302, 335, 315 and 320 between 06:17 and 06:37) as the officer and the captain try to match the account's danger bearings to the unnamed marks on the captain's chart; four nudges.
4. **06:49** (524964) at the mouth (RECON: the fairway gap 1.6 miles ahead, bearing 322; she was steering 320) the officer proposes to stand off for the flood. **06:51** (525094) `tack ship`; **06:52** (525177) "Squared the yards; she fell off on the larboard tack" (no tack was begun; see 6.6). He sets mainsail and jib; **06:56** `tack ship` is refused "She is not close-hauled"; `keep her full and by`; **07:02** (525776) "Tacked ... heading S by E (169°)."
5. **07:04** (525860) the captain asks him to "come out to the app chat for a second so I can send a picture of my chart". **07:05:00** (525900) "The pilot asks for sail to be shortened: his gig is coming off for him." **07:05:12** the officer, having seen the picture, tacks back for the Sound; **07:09** (526189) "Tacked ... heading NW by W (303°)."
6. **07:09 to 07:12** two voices on the helm: the captain types `hard a lee`, `Belay that` (refused), `Hard up`, `Meet her`, `Steer north`, `Steer north east`; the officer `steer 5`, then `steer 355` (526355). **07:13** (526382) "OK, you have the con fully, whatever happens happens, I trust you."
7. **07:15** (526500) "The gig hailed: she has come off for the pilot." **07:17:00** (526620) "Mr Ellis left her in the gig, clear of the mouth of St Mary's Sound; the pilotage, £3, paid" while she stood in at five knots, steering 355 for the outer road 0.7 mile ahead (RECON).
8. **07:17:52** "And a quarter fourteen"; **07:20:49** (526849) "And a quarter five; loose sand, not very tenacious." Seventeen seconds later (526866) the officer orders `steer 135` and turns out; **07:23:36** "Quarter less ten"; **07:24:00** (527040) "Fog came down."
9. **08:00** (529204) `heave to` four miles off; **08:37** (531421) the officer reports two knots of sternway hove to; the captain orders `Heave the deep sea lead`, answered at **08:52** (532344) "Forty-two fathoms; fine grey sand with black specks."
10. **08:53** (532389) the captain asks whether to anchor; **08:56** (532560) `come to an anchor`; **09:03** (532983) "The best bower let go in 46 fathoms."; **09:22** (534171) "Brought up by the best bower in 45 fathoms, 230 fathoms of cable".
11. **09:23 to 09:24** the captain asks to "un-veer"; the officer's `heave in the best bower cable to 160 fathoms` is refused by the domain, allowed by the captain as "heave short", refused twice by the grammar, and accepted as `heave in 70 fathoms` (534284). **10:00** (536457) "Hove short on the best bower: sixty-seven fathoms of cable". The officer stands by "until a notable event" from 09:30 to 12:00.
12. **12:00** (543600) "The fog lifted." The officer weighs (543609): aweigh **12:05** (543914). His `get under way on the larboard tack and steer 315` (543919) fails at **12:14** (544495) "Could not get under way: no anchor is down"; she drifts under bare poles until the captain's "Nudge." at **12:17** (544660). Plain sail is set by 12:25.
13. **12:41 to 13:03** the officer steers 335, 307, 343, 349 for "the gap" by the account. The captain's six bearings at **13:03** show her on the Peninnis side, the Gilstone 0.85 mile ahead (RECON). **13:05** (547512) `tack ship`, **13:06** (547564) "she fell off on the larboard tack" (again no tack was begun); `wear ship`, **13:13** (548037) "Wore ship ... heading WSW (248°)". The wind goes SW by W, W, NW by W in eight minutes.
14. **13:15** (548111) the captain: "drop anchor as soon as possible if it's safe here and try to send the boat in". **13:16** (548205) he says the attempt "will come better once some changes to the reckoning near shore come in".
15. **13:18** (548280) a second gig is sighted; **13:22** (548569) "The best bower let go in 37 fathoms."; **13:33** (549180) the gig hails; **13:36** (549360) "The pilot, Mr Pender of St Mary's, came aboard from the gig and took charge of her" as she lies at anchor.
16. **13:33** (549185) `sell 16 tons of brandy` refused (no prices); (549186) `send the boat ashore` accepted; (549187) "Not hands enough on deck to send boat; the hands are coming to anchor." The boat never leaves and is never free again (6.9).
17. **13:42** (549749) "Brought up by the best bower in seven fathoms, a hundred and eighty-five fathoms of cable".
18. **14:46** (553567) the captain: "I'm afraid the boat got stuck again"; (553594) "Let's weigh and try for the road". `weigh` (553598); aweigh **15:27** (556029), 40 minutes later.
19. **15:27 to 15:49** `set plain sail`, `steer 220`; the sails are set between 15:37 and 15:49. **15:46** (557169) `tack ship`; **15:52** (557569) "she fell off on the starboard tack"; (557579) urgent "Taken aback"; `wear ship`, belayed by the captain at **15:56** (557785) as the wind goes SW by S; `steer 309`.
20. **15:57** (557858) the captain: "We're just going to send it and pray." **15:59** (557978) urgent "Taken aback" again; **16:03** (558236) the officer's "honest report" against going on; **16:05** (558312) "Her sails aback; she had no way on to lose."
21. **16:06** (558407) the captain: "with our boat stuck as it is, I fear we can't sell or buy anything again with this particular Speedwell. Go ahead and hand over". **16:07** (558434) `hand_over`; "The game is saved." [CKPT] she then lay 5.6 cables S by E of Peninnis Head and 4.5 cables SSW of the Gilstone, making 1.2 knots of sternway.

She came from 3 miles SE of the Sound at 05:51 to within 0.7 mile of the outer road at 07:17 and never nearer.

## 3. The deck and the captain's words

**The deck.** [LOG] The officer held the deck for the whole slice (given at tick 398,710). It was given back once, by his own `hand_over` at 558434: "The officer of the watch hands over the deck; the captain has it." The captain never typed `I have the deck`, yet gave 12 accepted ship's orders of his own while the officer held it; the game takes both without remark.

**Allowances.** One in the slice:

| Tick, time | Captain's words | What the log made of it | Used? |
|---|---|---|---|
| 534260, 09:24 | `you may heaev in the best bower cable to 160 fathoms` | refused: "names no order the officer of the watch could be allowed; say the order's words first" (a typing slip) | no |
| 534267, 09:24 | `you may heave in the best bower cable to 160 fathoms` | "The officer of the watch may heave short (the best bower cable to 160 fathoms), by the captain's word for the watch." | yes, 534284, and it hove in 163 fathoms, not 70 (6.4) |

Everything else the officer did outside his domain rode on allowances six days old "for the watch" (21 to 25 June: steer, tack ship, wear ship, heave to, fill away, come to an anchor, weigh, get under way, send the boat, sell, keep her full). All were still honoured through two re-seatings and some forty-five watches. He used none of: buy, veer cable, let go the anchor, moor, come up, bear away, shape a course, and, notably, the bearings of "(the land)" and "(the light)" allowed at 03:29: he took no bearing in the slice.

**The captain's lines that carry intent, design or feedback** (41 `tell`, 3 `ask`):

- 521548, 05:52: "don't mind the pilot too much. As with it all, he's not able to steer her properly yet. His message is the extent of it, largely. As for our colours ... we purchased an American ship and we're making good use of the colours to trade freely."
- 521704, 05:55 (on `clear away the bowers`): "Understood, as I expected, good instinct, the game didn't close the gap."
- 525082, 06:51: "If my markers were all named, I would feel more confident. What I see is a line of three + markers, a slightly long vertical |, and another + slightly east southeast of Peninnis head. Are we sure which is which by deduction?"
- 525860, 07:04 (ask): "Can you perform a stand by and then come out to the app chat for a second so I can send a picture of my chart?" then 525964: "Now I get it! Fantastic!"
- 526346, 07:12: "Noted, I paniced on the chart again, we're not as close as I thought."
- 526898, 07:21 (after the turn-out): "I Think you had it, actually, it was tight maybe".
- 527128, 07:25 (can the chart show soundings?): "It can't".
- 543725, 12:02: "You have the con and my trust, and you should trust your bearings as they've been better than mine."
- 544882, 12:21: "My only tip for you is to stand by on as short a basis as you can, and don't rely on a specific event if it won't definitely occur first."
- 546431, 12:47: "don't use say for now unless you absolutely must as it can end your turn before you stand by, I believe."
- 548205, 13:16: "it was a good attempt, but I think it will come better once some changes to the reckoning near shore come in. I'm thinking we need a circle around the ship that, when it has landmarks or land within it, make the reckoning very precise to represent the fact that we can see what's around us and know where we are pretty well."
- 553567, 14:46: "I'm afraid the boat got stuck again, I don't see it in the 'in hand' tasks and perhaps sending it while coming to anchor broke it like the belay." (He was right; 6.9.)
- 556129, 15:28: "We'll need to make a new scenario to fix the stuck boat anyway, so nothing to lose."
- 557858, 15:57: "I'm not going to take any more bearings. We're just going to send it and pray. We make it or we break it."
- 558333, 16:05: "I think God might be saying 'Don't go to Scilly', at this point".

**What the captain did by hand** (116 typed inputs in the slice):

- **All the bearings**: 53 typed, 47 taken. Each one moves the account (6.11), so they were the navigation. The officer's allowance covered only "the land" and "the light"; he never tried.
- **The chart**: the officer has none. The captain described unnamed marks in words, then sent a picture through the Claude Desktop chat, outside the game (07:04).
- **Balancing the rig** after the officer took in mainsail and foresail: `set the gaff topsail` (521862), `Take in the jib` (522140), `Trim sails` (522419). Officer, 522290: "With the mainsail off she was carrying 23° of helm".
- **The helm, 07:09 to 07:12** (526190 to 526323), on seeing "land straight ahead, St agnes" on his chart.
- **`Heave the deep sea lead`** (531454), which the officer never ordered though it lies in his domain.
- **Waking the officer**: "Nudge." (544660) from a stand-by on an event that could no longer happen.
- **`belay wear`** and `meet her` (557785, 557793), when the wind shifted in the middle of the officer's wear.
- **Four attempts to free the boat** (550494, 553622, 553626, 553637), all refused.

## 4. Orders refused

55 refusals in the slice: 54 `order.rejected` (officer 7, captain 12, standing orders 35) and 1 `agent.refused`. Classes: (a) vocabulary or grammar gap, (b) domain refusal as designed, (c) domain refusal that looks wrong, (d) correct ship-state refusal, (e) apparent bug.

**By the officer (8).**

| Tick, time | Order as typed | Reply | Class | What followed |
|---|---|---|---|---|
| 521645, 05:54 | `clear away the bowers` | "There is no such part as the bowers in this ship. ('let go' was understood.)" | (a) | A preparatory order read as the verb "let go"; nothing was let go, but it alarmed the captain. |
| 521648, 05:54 | `clear away the best bower` | "There is no such part as the best bower in this ship. ('let go' was understood.)" | (a) | Dropped. |
| 521707, 05:55 | `steer 303` | "She is hove to; fill away before giving her a course." | (d) | Given 63 s after his own `fill away`, before it ended. He then told the captain she was "Filled away and steering NW by W (303°)" (521708); the evolution itself put her on 305 at 521726 and `steer 300` followed. |
| 525364, 06:56 | `tack ship` | "She is not close-hauled; bring her by the wind before going about." | (d) | `keep her full and by` (525492), "Steady, full and by, the wind 55° on the larboard bow", `tack ship` accepted (525518), tacked 07:02. The same failed check, when the order has to wait, is logged as a missed stay instead (6.6). |
| 534248, 09:24 | `heave in the best bower cable to 160 fathoms` | agent.refused: "may not heave in the best bower cable to 160 fathoms without the captain: the anchor is let go and weighed by the captain." | (c) | He already had leave to weigh, veer cable, come to an anchor, let go and moor. Officer, 534252: "veering and heaving in should probably be one grant." |
| 534277, 09:24 | the same, after the allowance | "'heave short' takes nothing after it; 'the best bower cable to' was not understood." | (a) | |
| 534281, 09:24 | `heave in 70 fathoms of cable` | "'heave short' takes nothing after it; 'of cable' was not understood." | (a) | `heave in 70 fathoms` was then accepted, the number read and thrown away: (e), see 6.4. |
| 549185, 13:33 | `sell 16 tons of brandy` | "The prices at St Mary's are not known; send the boat ashore first, and the purser will bring the list off." | (d) | `send the boat ashore`, which stuck (6.9). |

**By the captain (12).**

| Tick, time | Order | Reply (shortened) | Class |
|---|---|---|---|
| 526199, 07:09 | `Belay that` (to undo his own `hard a lee`) | "There is no work in hand or waiting to belay." | (a): a helm order is not "work"; he typed `Hard up` |
| 526283 and 526289, 07:11 | `Take a bearing of the light` (twice) | "The light is not in sight; in sight: ..." | (d) by day, though `st agnes light` had been taken at 06:17 and 06:29 |
| 526305, 07:11 | `Take a beaing of hugh town` | "is not an order this ship understands; did you mean 'take in', 'take a lunar' or 'take a bearing of'?" | typing slip |
| 526309, 07:11 | `Take a bearing of hughs town` | "Hughs town is not in sight; did you mean Hugh Town?" | slip; the right guess is offered and not taken |
| 534260, 09:24 | `you may heaev in ...` | "names no order the officer of the watch could be allowed" | slip |
| 543624, 12:00 | `take a bearing of st agn'es` | "did you mean St Agnes or St Martin's?" | slip |
| 545523, 12:32 | `take a bearing of st marys` | "St marys is not in sight; did you mean St Mary's or St Martin's?" | (a): a missing apostrophe |
| 550494, 13:54 and 553626, 14:47 | `send the boat ashore` | "The long-boat is away already." | (e) |
| 553622, 14:47 | `belay send the boat ashore` | "Nothing in hand or waiting answers to 'send the boat ashore' ... The work in hand: weighing anchor." | (e) |
| 553637, 14:47 | `belay hoist out the boat` | "Nothing in hand or waiting answers to 'hoist out the boat'" | (e) |

**By standing orders (35).**

- The captain's `light sails` ("every 10 minutes if the mean wind is above 10 knots then take in the occasional sails"): **34 times**, 06:00:01 to 15:50:01, each "order not carried out ('take in the occasional sails'): Nothing done: the ringtail is already furled; the water sail is already furled." 90 in the whole session. A rule already satisfied is logged as a refusal every ten minutes: (e) as log noise.
- The officer's `studding`: once, 556218, 15:30, "Nothing done: the starboard fore topmast studdingsail is already furled".

**Not exercised here**: number words, taking in the water sail by name, a refusal of "full and by" (`keep her full and by` was accepted at 525492 under the old "keep her full" allowance). Every course the officer gave was in degrees (`steer 5` became "steer N (5°)"); the captain's `Steer north`, `Steer north east`, `hard a lee`, `Hard up`, `Meet her` were all taken.

## 5. Harness behaviour

**Volume.** [LOG] 79 samplings (`agent.resumed`); 76 orders (68 accepted, 7 rejected, 1 refused); 59 spoken lines (55 `agent.note`, 4 `agent.said`); 79 stand-bys; journal 1, readings 2, state 1, library 2, read_log 0, hand_over 1. The officer was on a stand-by for 33,413 of the 36,974 seconds. The median open turn was 18 s; his reaction when it mattered was quick: 17 s from the five-fathom cast to `steer 135` (526849 to 526866), 4 s from the urgent "Taken aback" to `wear ship` (557579 to 557583).

**What woke him** (79):

| Reason | Count |
|---|---|
| "A word from the captain" (three of them the captain's standing orders that `tell the officer` when the pilot hails, asks off or leaves) | 33 |
| Timers: ten minutes 7, five minutes 7, two minutes 6 | 20 |
| Named events: a sounding 3, tacked 2, filled away 2, a glass 2, and one each of wore, hove to, brought up, the anchor aweigh, steady on the course, a sighting, the change of the watch | 16 |
| "A notable event" | 5 |
| "A question from the captain" | 2 |
| "An urgent event" (both real: taken aback with way on, 15:52 and 15:59) | 2 |
| His own word | 1 |

The captain's three relay standing orders are a workaround for the lack of a stand-by on several conditions. One of them (13:33, the pilot's hail) woke the officer into the middle of the anchoring evolution, where he ordered the boat away (6.9).

**Stand-bys** by `until`: 2 minutes 13, a message 9, ten minutes 9, 5 minutes 8, a sounding 7, a glass 7, a notable event 6, tacked 4, brought up 4, filled away 3, the anchor aweigh 2, wore 2, and one each of a sighting, steady on the course, the change of the watch, hove to, got under way. None is logged as refused.

- **The longest**: 8,988 s, 09:30:12 to 12:00:00 (534612), "until a notable event". Nothing notable happened in fog at anchor. In particular "Hove short on the best bower: sixty-seven fathoms" (536457) is a routine line, so he slept through his own order going wrong, and through four glasses (a stand-by suspends the every-glass sampling).
- **A stand-by on an event that had become impossible**: 543919, 12:05, "until got under way". The evolution failed at 544495 with a notable `evolution.failed` line that did not wake him; the captain's "Nudge." did, 12 m 21 s after the order.
- **"Brought up" as an event comes late**: the evolution says "Brought up. Stations for furling sail" at 09:10:33 and 13:29:56, but the event and its notable line wait for the furl, 12 minutes later (534171, 549749).
- **"A sounding" wakes on no bottom**: 524096, 06:34, woken by "No bottom at twenty fathoms."

**`say` ends the turn.** The transcript marks 11 stand-bys "out of turn": 521525, 521616, 523101, 525837, 526343, 547117, 548263, 549240, 553651, 556093, 557851. Each follows a spoken line by 50 to 53 ticks. That is the door's 50-second hold: a spoken line closes the turn, the call is held up to 50 s for a new one, and only then can he set a wake condition. Eleven times, about nine minutes in all, the officer had spoken and had no stand-by set; the game ran at 1x through each. The captain saw it (546431, above). After that tip the officer made one course change with no word at all (546743, `steer 307`), the only unexplained order of the day.

**Nudges: 10; pauses: 0.**

- 523151, 523899, 524163, 524224 (06:19 to 06:37): "3 ... 4 ... 5 ... 6 contrary orders on the helm within the watch (steer 300; steer 295; steer 302; steer 335; steer 315; steer 320)". This is conning in pilot water.
- 543919, 12:05: "3 contrary orders on the ship within the watch (heave in 70 fathoms; weigh; get under way on the larboard tack and steer 315)". One purpose, and the first order was in the forenoon watch, the others in the afternoon.
- 547512, 547605, 548046 (13:05 to 13:14): steer 343; steer 349; tack ship; wear ship; steer 200.
- 553598, 14:46: "(come to an anchor; send the boat ashore; weigh)", ninety minutes apart.
- 557801, 15:56: "(tack ship; wear ship; steer 309)".

None marks a real contradiction. A chain of six raised no pause, and the chain carried on across turns that held no contrary order, both against primer 16 ("the chain going on after it the pause"; "A turn without a contrary order ends the matter"). No nudge shows in anything the officer said.

**Journal and library.**
- One journal entry (543746, 12:02), at the captain's prompting: the approach, the pilot's directions, the lessons, and seven order-language notes, all accurate.
- `library({"find": "draught", "topic": "papers"})` and `library({"find": "draws"})` (527027, 527030) did not give him the ship's draught: "I don't know her draught: I can't find it in the papers. Do you know what she draws?" (527040). The ship file has 3.3 m, 10.9 ft [CODE]. The captain did not answer, and the question decided the morning (6.8).

**Handover.** `hand_over` at 558434, 27 seconds after the captain asked. Salient parts:

> "Speedwell is about a mile south of the line of ledges at the mouth of St Mary's Sound, Scilly, in 33 fathoms. Peninnis Head is N by W a mile and St Agnes W two miles. The Gilstone is about a mile NNE by account, but the account has jumped a mile at a time all day, so trust bearings over it. ... the true wind is boxing the compass minute to minute (SSW, S by E, NNW, W within ten minutes), so she is taken aback over and over and missed stays twice. ... The long-boat was sent for prices while the anchoring evolution held all hands. It is stuck 'away, hoisting out' and cannot be recalled, so no trade is possible in this game. ... Pilot Mr Pender (second pilot) is aboard. Purse £28. ... Belay 'trim' and 'steady trim' before heaving to. ... For the book (details in my journal): base wind chatter near the islands; the account jumps; ranges by estimation; the gig's fixed range; 'heave in N' runs on to heave short; 'come to an anchor' veers 5:1; a boat order given while all hands are busy gets stuck; 'get under way' fails once the anchor is catted; 'full and by' holds a fixed apparent angle; heaving to makes sternway; 'brought up in seven fathoms' was logged in 37; the anchor line said 'riding to the ebb' at noon though the pilot gives the flood from 10:30."

Against [CKPT]: bearings right, distances about double the truth (Peninnis 0.56 mile at 345, the Gilstone 0.45 mile at 027, the ledges 0.67 mile north); "33 fathoms" is exactly the chart's depth at the datum at the true position (61.15 m); the boat, the pilot and the purse are as he says; "missed stays twice" is not what happened (6.6). The game ended here, so there was no next seating.

**Context and relay.** No sign of a lost thread, a lost journal or lost permissions in 221 entries. One unexplained slow turn: after his note at 534289 no stand-by until 534612, 5 m 23 s later, at the glass. Every sampling dropped the game to 1x ("Compression eased to 1x: the officer of the watch is sampled", 51 times, plus 2 for the urgent lines), so the owner had to raise the speed again about fifty times.

## 6. Ship, sea, navigation and port observations

### 6.1 Why she never reached St Mary's Road: the day by legs

Wind and tide: SW to SW by W, 11 to 14 knots, steady, all morning (no `wind.shift` line before 12:27); 23 shifts of the mean wind from 12:27 to 16:05. High water about 04:20 to 04:45 and again at 16:45, low water about 10:30, springs, "rising some 19 feet".

| Leg | Courses, and who gave them | Lead and marks | Truth [RECON] | What stopped her |
|---|---|---|---|---|
| **A. 05:54 to 06:51**, in from the SE, ebb | Officer: 300, 295, 302, 335, 315; 320 on the captain's "By my reckoning, 320 would shoot right into the gap" (524219) | 19 casts, all no bottom. Peninnis NW 3 miles to N by W 1 mile. The leading marks never reported. | 05:55: outer road 3.7 miles at 302. 06:35: steering 335 with Peninnis at 335 (captain, 524150: "on a direct course for peninnis head"). 06:49: gap 1.64 miles at 322, steering 320. | Nothing physical. The marks could not be named (525082); the officer: "Matching your unnamed + marks to those names by deduction would be a guess" (525095). He stood off to wait for the flood. |
| **B. 06:51 to 07:09**, out and back | Officer: tack (phantom failure), tack refused, full and by, tack; then tack back at 07:05 | One cast, no bottom | 07:03: outer road 0.84 mile at 336 | Three minutes on the seaward board lost the pilot (6.3). |
| **C. 07:09 to 07:24**, in, ebb | Captain: hard a lee, hard up, meet her, N, NE. Officer: 5, then 355; then 135 | No bottom 07:14; 14¼ at 07:17:52; 5¼ at 07:20:49; 9¾ at 07:23:36. Officer: "the chart under her is now two and a half fathoms" (526903). | 07:17: outer road 0.73 mile at 353, gap 1.03 at 354, steering 355; St Agnes's centre 0.64 mile, so the nearest shore (Gugh, by the real island's shape) perhaps two or three cables to larboard. | The officer turned out at the shoaling (6.8). Fog at 07:24. |
| **D. 07:24 to 12:00**, off, hove to, anchored | Officer: 135, heave to 08:00, fill away, come to an anchor 08:56 | Deep-sea lead 42 fathoms; let go in 46 | 12:00: outer road 4.5 miles at 320 | Fog to noon. `heave in 70 fathoms` left her on 67 fathoms in 45. |
| **E. 12:00 to 13:15**, in again, flood | Officer: 315, 305, 335, 307, 343, 349; tack (phantom failure); wear; 200 | 7 casts, no bottom | 12:31: gap 4.5 miles at 326. 13:03: **the Gilstone 0.85 mile at 352, steering 349**; gap 1.72 miles at 310. The account was 1.2 miles out (6.11). | Twelve minutes adrift before sail was ordered, after the failed `get under way`. He steered by the account up the Peninnis side. The wind went SW by W, W, NW by W (13:06 to 13:14) and headed her. |
| **F. 13:15 to 14:46**, anchored off Peninnis | Officer: come to an anchor | Let go in 37; "brought up in seven" | 13:31: Peninnis 0.78 mile at 317, Gilstone 0.46 at 336, outer road 1.42 at 286 | The game counts her "at anchor in St Mary's, the mouth of St Mary's Sound" (officer, 549190), so the port was open; the boat stuck. |
| **G. 14:46 to 16:07**, last try, near high water | Officer: weigh, 220, tack (phantom failure), wear (belayed by the captain), 309 | 7 casts, no bottom | 15:55: gap 1.49 miles at 309, as he judged it. End: gap 1.2 miles at 304. | 40 minutes to weigh 185 fathoms, 22 more before she was steady under sail; then the wind went W by N, NW by W, W by S, SW by S, S by E, SW by S, W, NW by W in 35 minutes; taken aback three times. |

### 6.2 What in the game's words or rules stood between the officer and the anchorage

1. **The pilot is a paragraph.** He "took charge of her" (521460) and did nothing else. His directions hang on a transit ("Bring the Great Minalto directly in one with the north-east side of the Great Mincarlo") and an opening ("until the white daymark on St Martin's opens to the westward of Bants Carn"). No line in the log ever reports the Great Minalto, the Great Mincarlo, the daymark or Bants Carn, and nothing says "in one". The chart file holds the transit (`st-marys-sound`, bearing 330) [CODE]; nothing brought it to the deck.
2. **He leaves by a rule that cannot tell a board to seaward from a departure**, and no other comes for six hours (6.3).
3. **The chart's own data contradict him.** He says "the Woolpack to starboard and the Spanish and Bartholomew ledges to larboard". The features file puts the Spanish Ledge at 49.90704 N, 6.31755 W, east of the Woolpack (6.32392 W), so on the starboard hand, beyond the Woolpack; its own `says` text has it "on the larboard hand". The officer saw this unaided (journal, 543746: "The game's layout contradicts Ellis's starboard/larboard wording, so trust the positions, not the wording"). The real fairway in the game is the gap, 2.9 cables wide, between the Woolpack and the Bartholomew.
4. **The dangers come by account, in whole miles and compass points.** [CODE] `miles_words` gives "no distance" under a quarter mile, "half a mile" to a half, "a mile" from 0.5 to 1.5. "The Woolpack N by E and the Bartholomew N by W, both a mile" (526625) is as fine as it gets for two ledges 2.9 cables apart.
5. **The account itself was 0.1 to 2.3 miles out** and moves in jumps (6.11).
6. **The captain's chart has unnamed marks; the officer has no chart.** One picture sent outside the game did more than three hours of rounded bearings (525919).
7. **The lookout ranges an island by its centre.** "St Agnes bore WNW, nine cables" (526637) while the nearest shore, Gugh, was by my estimate two or three cables off. Gugh is not a feature.
8. **The ledges and the Gilstone are never sighted.** They are drying rocks, covered at these tides, which is fair; but it leaves the lead and the depth reading as the only warning.
9. **The hand lead** finds nothing beyond 20 fathoms; a cast takes about 110 s (526740 to 526849). The bottom came up from 14¼ to 5¼ fathoms between two casts.
10. **The cost of every evolution**: 27 minutes to come to an anchor, with all hands held and other work dropped; 36 and 40 minutes at the capstan; 10 to 22 minutes to make sail after weighing (6.4, 6.5).
11. **Three "missed stays" that were not** (6.6), which the officer took as proof that she would not tack in the Sound.
12. **The afternoon wind** (6.12), **the fog** (07:24 to 12:00), and **the stuck boat** (6.9), which closed the port even from the outer berth.

### 6.3 The pilots

**Mr Ellis.**
- [LOG] Gig sighted 05:38 (520680) "A gig pulling off from the land ... distant two miles"; hail 05:48; aboard 05:51:00 with the ship hove to. Officer (521473): "He came over the side with the gig still logged two miles off". [CODE] the lookout's estimate is re-judged only when the *ship* has moved a mile from where it was judged (`lookout.py`, `ESTIMATE_HOLD_NM = 1.0`), so a boat pulling up to a ship hove to keeps its first distance to the end.
- His words (521460) are the port file's `channel`, `marks` and `anchorage` paragraphs and a made-up tide sentence: "High water at St Mary's about a quarter to five in the afternoon, the tide rising some 19 feet; the flood will serve from about half past ten in the morning."
- [CODE] The file also has a `tide` paragraph: "in St Mary's Sound the stream sets out south-east by east until two hours' ebb on the shore, then runs north-west by west. Take the Sound on the flood." Nothing in `ports.py` reads it; neither `pilot_words` nor `ask the pilot` can say it. It is the one plain instruction that would have settled the morning's argument.
- **Nobody asked the pilot anything through the game.** There is no `ask the pilot` and no `pilot.answered` in the whole session. The captain's word at 05:52 turned the officer away from him; every question about tide, marks and depth went to the captain.
- **Leaving.** [CODE] `ports.py` 743 to 776: each minute, with a pilot aboard and the ship not at anchor, if she is more than (the outer road's distance from the anchorage, 1.38 miles) + `PILOT_OFF_BEYOND_NM` (1.0) from St Mary's Road *and that distance grew in the last minute*, the gig is launched to fetch him. [LOG] She tacked to seaward at 07:02; at 07:05:00 (525900) "The pilot asks for sail to be shortened: his gig is coming off for him." [RECON] She was then about a mile SSE of the outer road, having been within about 0.8 mile of it and never inside. The fetch cannot be called back: she tacked for the Sound 12 seconds later, and the gig took him off at 07:17:00 with the ship steering 355 at "five knots" (526625) and the outer road 0.7 mile ahead. The words "clear of the mouth of St Mary's Sound" are fixed text. He boards or leaves at any speed up to 6 knots over the ground (`PILOT_BOARDS_UNDER_KN = 6.0`).
- **The six hours.** [CODE] `PILOT_AGAIN_H = 6.0`. [CKPT] `declined_until['st-marys'] = 548220`, which is 13:17:00. No pilot could be had for the clear-weather attempt on the flood from 12:05 to 13:15.
- Fee: £3 [CKPT purse entry at 526620]. Four minutes after he left the lead found five fathoms.

**Mr Pender.**
- [LOG] Sighted 13:18:00 (548280), the first minute after the six hours ran out, as she rounded to to anchor: "Sail ho! The St Mary's pilots' gig abeam to starboard, bearing WNW, distant a mile."
- Hailed 13:33:00 (549180) "a pilot for St Mary's; shorten sail and he will come aboard", to a ship that had let go at 13:22 and was furling.
- Aboard 13:36:00 (549360), "took charge of her", at anchor in 37 fathoms outside the Sound. [CODE] launching needs her under way; boarding does not.
- The same words, ending "the flood is making now and serves". Nobody asked him anything. The officer's one idea for him (548321: "he can at least go in with the boat and show it the way") has no order.
- He was not fetched when she weighed, since she never opened 2.38 miles from the Road. [CKPT] still aboard at the end, unpaid; purse £28.

**So the pilotage was paid once in this slice, not twice**: £3 at 07:17. Over the voyage, three times: Plymouth £6, Roscoff £3, St Mary's £3.

**Oddities.** Two gigs of the same name in sight at 07:11 (526283: "The St Mary's pilots' gig right ahead, bearing NNW ... The St Mary's pilots' gig on the starboard bow, bearing N by E"), each with "Sail ho!" inside the list. `what is she` (527024) makes the six-oared gig out "under plain sail; British colours, the red ensign".

### 6.4 Anchoring, the ground tackle, and "heave in"

- **Who ordered it and how the scope was chosen.** The captain proposed anchoring (532389); the officer agreed and said "let go the best bower with 130 fathoms" (532406), then typed a bare `come to an anchor` (532560). [LOG] 533193: "Veered to 230 fathoms; brail up the spanker." [CODE] the evolution veers five times the depth at letting go (`RIDING_SCOPE_PER_DEPTH = 5.0`): 5 x 46 = 230, and 5 x 37 = 185 in the afternoon. Officer (534177): "the evolution veered 230 of the 240 fathoms, five to one, not the 130 I meant." The primer's form with a number sets the scope; he did not use it.
- **Is 230 fathoms a thing she carries?** [CODE] Yes: the best bower has `cable_fathoms: 240.0`, `cable_in: 12.0` ("two cables of 120 fathoms spliced on the best bower"); the small bower, sheet, stream (8-inch) and kedge (6-inch hawser) have 120 each. The officer's "240 fathoms" and "twelve-inch cable" are right. The game refuses to anchor deeper than a third of the cable, 80 fathoms.
- **The evolution holds all hands for 27 minutes** (08:56:00 to 09:22:51; 13:15:20 to 13:42:29), ten of them furling after she has brought up, and at its end silently drops any work that waited (6.9).
- **`heave in 70 fathoms`** (534284). [CODE] "heave in" is a synonym of `heave short` (`data/vocabulary.yaml`), which takes no number; the grammar reads "70 fathoms" and the script ignores it. [LOG] "All hands! (to heave short)"; 36 minutes later "Hove short on the best bower: sixty-seven fathoms of cable, the cable a-stay in 45 fathoms." 163 fathoms came in. She lay two hours at a scope of 1.5 in 45 fathoms. Officer at noon (543609): "too short to hold, and she's moving a knot ENE, so I think the anchor is dragging" [SAID]; no dragging line is logged. There is no order to heave in to a stated scope (`veer to ninety fathoms` only lets out).
- **"Brought up ... in seven fathoms"** (549749), twenty minutes after "let go in 37 fathoms". Officer (550508): "looks like a slip in the book ... the chart shows 34 under her now". It is not a slip of words:
  - [CODE] `world.py` 587 to 593: once a minute the anchor's depth is read from the chart at `origin.advanced(anchor.ground_x, anchor.ground_y)`, the scenario's origin moved in one step by the anchor's plane coordinates. The ship's true position is integrated tick by tick.
  - [CKPT] After this voyage the two differ: `origin.advanced(ship_x, ship_y)` is 49.89593 N, 6.33746 W; the true position is 49.89593 N, 6.30183 W. That is **1.377 miles, due west**.
  - So the anchor's depth was read in the mouth of the Sound, 1.4 miles west of where it lay. [CKPT] the best bower's last `depth_m` is 14.56 m (8 fathoms) while the water under the ship was 66.8 m.
  - The weighing used that depth: "The cable is up and down" came at 15:25:52, which by the capstan's rate that morning leaves only four to eight fathoms out (my arithmetic), and from aweigh to "up to the bows" took 50 s (556029 to 556079), against 241 s in 45 fathoms that morning. At 09:22 the same error did not show ("46 fathoms" then "45 fathoms"), the bottom being flat.
  - [CODE] `chart.fathoms_words` returns "no water" for less than a quarter fathom, and the anchor's depth is floored at zero; the Harpy's "brought up in no water" would be the same path if her displaced point fell on the shore (not checked against her save).
  - [CODE] `world.py` 699: the weather's coast hook uses the same conversion (6.12).
- Small things: "brail up the spanker" (533193, 548756) on a schooner; "Brought up by the best bower in 45 fathoms, 230 fathoms of cable; Riding by ..." beside "in seven fathoms, a hundred and eighty-five fathoms of cable" (digits above twelve for a depth and from 200 for a cable; a capital after the semicolon).

### 6.5 Getting under way

`get under way` never ran in this slice, so the note about casting cannot be tested here (it ran at Plymouth, tick 38651, and Roscoff, tick 256898).

**First weighing, from a short stay of 67 fathoms in 45.**

| Time (tick) | Line |
|---|---|
| 12:00:09 (543609) | officer `weigh`; "All hands up anchor! Man the bars; heave round." |
| 12:04:10 (543850) | "The cable is up and down." |
| 12:05:14 (543914) | "The best bower is aweigh." |
| 12:05:19 (543919) | officer `get under way on the larboard tack and steer 315`, accepted as "getting under way on the larboard tack and steer 315"; he stands by "until got under way" |
| 12:09:15 (544155) | "The best bower up to the bows; avast heaving, pawl the capstan. Hook the cat." |
| 12:14:55 (544495) | "The best bower catted and fished; she is under way." and, the same tick, "Could not get under way: no anchor is down: she is under way already, or adrift." |
| 12:17:40 (544660) | captain: "Nudge." |
| 12:17:45 (544665) | officer `set plain sail`, `steer 315`; 12:20:37 `steer 305`, standing orders resumed |
| 12:20:29 to 12:25:49 | mainsail, foresail, fore staysail, jib, fore topsail, fore topgallant set; 12:21:25 "Steady on NW by W (305°)." |

[CODE] `runner.start`: an order whose subject is busy waits its turn and its preconditions are tested when it begins. The `get under way` waited behind `weigh` and failed when `weigh` ended. She was adrift under bare poles from 12:05 to 12:17 (leeway lines 2° to nil; no heading or speed line exists in the log). Nothing had to be done by hand to get her head round: the wind was abeam of the course. Officer (544666): "'get under way' given while weighing should carry on into making sail once the anchor's up, not fail." During these minutes the account ran on at five and a half knots (6.11).

**Second weighing, from 185 fathoms.**

| Time (tick) | Line |
|---|---|
| 14:46:38 (553598) | officer `weigh` |
| 15:25:52 (555952) | "The cable is up and down." |
| 15:27:09 (556029) | "The best bower is aweigh." "Leeway 18° to larboard." |
| 15:27:19 (556039, 556040) | officer `set plain sail`, `steer 220`; five lines "Not hands enough on deck to set the mainsail [fore topsail, fore topgallant, fore staysail, jib]; the hands are weighing anchor." |
| 15:34:13 (556453) | "catted and fished; she is under way." |
| 15:37:41 to 15:49:07 | foresail, mainsail, fore topsail, jib, fore staysail, fore topgallant set; leeway 29°, 19°, 15°, 16° (15:30 to 15:33), 47° (15:42) |
| 15:39:00 (556740, 556741) | officer orders `set the jib`, `set the fore staysail`, `set the fore topsail` again; they produce "Could not set the fore topsail: The fore topsail is set already." and two like it (557026, 557141, 557226) |
| 15:49:22 (557362) | "Steady on SW (220°)." |

Ten minutes adrift with no sail, 22 from aweigh to steady. He did not use `get under way` at all, having taken from noon that it fails; the lesson was that it replaces `weigh`, not that it follows it.

**Sternway.** No `ship.*` line reports it. [SAID] 531421, 08:37: "Hove to, she's making two knots of sternway, heading SW by S and going astern towards the NE ... easing the main sheet hasn't changed it"; 558343, 16:05: "She's in irons now, making sternway with the sails aback". [CKPT] at the last tick: heading 268°, ordered course 309°, u = -0.63 m/s (1.2 knots astern), rudder at -35°, the opposite side to what headway would want. [CODE] `hull.py` 370 to 374 shifts the helm when sternway passes 0.15 m/s. So for a steered course the helmsman does shift his helm in this build.

### 6.6 The three "missed stays" that were not

[LOG] The whole session has three `ship.fell_off` lines, all in this slice, and no `ship.missed_stays`:

| Tack ordered | "Squared the yards; she fell off on the ... tack, to try again or to wear." | At the same tick |
|---|---|---|
| 06:51:34 (525094), steering 320 with the wind SW, a beam reach | 06:52:57 (525177) | "No bottom at twenty fathoms." |
| 13:05:12 (547512) | 13:06:04 (547564), 52 s later | "No bottom at twenty fathoms." |
| 15:46:09 (557169), plain sail still being set | 15:52:49 (557569) | "No bottom at twenty fathoms." |

None is preceded by "All hands! (to tack ship)", "Ready about. Helm's a-lee" or "All hands about ship.", the lines the two real tacks have (525519, 525913). Both real tacks succeeded (525776, 526189).

[CODE] `heave_lead` is an evolution on the ship and holds her while the leadsman casts. A `tack ship` given during a cast waits for it; when the cast ends the tack's preconditions are tested ("She has not way enough on her to stay", "She is not close-hauled"); if one fails, the tack's `on_fail` line is logged, and that line (`tack.yaml`: "Squared the yards; she fell off on the {old_tack} tack, to try again or to wear.") has no place for the reason. With `close lead` every 180 s and a cast taking 110 s, most orders on the ship are queued. Given with no cast in hand, the same failed check is a plain refusal (525364).

So no helm was put down and no yard squared. What it did to the day:
- 525185, 06:53: "She's missed stays, sir. Under the fore topsail, staysail and gaff topsail alone she hadn't the sail to come through the wind."
- 548046, 13:14: "it's a dead beat up a gap of two or three cables, and she has missed stays twice today in light airs. I don't think we should try to tack her through the ledges." This is the argument on which the second attempt was given up.
- 557585, 15:53: "She missed stays, sir ... In the four minutes she was in stays, the true wind went from W through to SE by S and back".
- The hand-over note: "missed stays twice".

### 6.7 "Trim sails" and the helm

- **One instance of a trim before the helm had swung**: `steer 135` at 07:21:06 (526866), `trim sails` 76 s later (526942), logged "Braced two yards to the wind, 121° on the starboard quarter, abaft the beam"; yards "9° from square" at 07:23:04; "Steady on SE (135°)" only at 07:26:07, with the wind then about 100° on the side. No second trim was ordered (he hove to at 08:00). Mild.
- **His standing workaround** `steady trim` ("at steady on the course then trim sails") fired five times after course changes (544885, 546262, 546843, 547145, 547375). At 13:02 it and `trim` ("at a wind shift then trim sails") fired three seconds apart on the same sheets (547375, 547378: "the yards are being trimmed already").
- **A trim to a passing wind, in the middle of other work.** `trim` fired at 15:50:57 (557457), 95 s after she steadied on 220 with a tack waiting: "Braced two yards to the wind, 114° on the larboard quarter, abaft the beam". That is a wind from ESE for that instant, against a mean of W by N. At 15:52:06 "Trimmed the sheets of the fore staysail, the jib, the foresail and the mainsail; 60° to 85° off the centreline." 53 seconds later, with the wind back, "Taken aback: the sails pressed against the masts and she lost her way" (557579).
- The officer's own `trim sails` at 16:01:44 (558104) braced for a wind "92° on the starboard beam" while the mean was SW by S, the other side.
- `trim sails` and the `trim` rule read the instant wind [CODE, CHANGES-m5c-b: "Standing orders on the true wind still read the instant wind"]. In a wind that swings, each trim is wrong within the minute. The officer belays both rules by hand before anchoring (548119) and says so in the note.

### 6.8 The lead, and the depth reading

- **Casts**: 53 soundings, every one notable. 49 are "No bottom at twenty fathoms." Three found bottom, all in six minutes (07:17:52, 07:20:49, 07:23:36). The one deep-sea cast was the captain's: ordered 08:37:34, answered 08:52:24, fifteen minutes.
- **A deep-sea lead exists.** `Heave the deep sea lead` works; the officer never used it.
- **Lead rules and hands.** In this slice he ran one lead rule at a time (`approach lead` every 10 minutes, `close lead` every 3), swapping nine times, so "Not hands enough on deck to heave lead" does not occur (the nearest is 520820, 05:40, just before the slice). What does occur: "held; the last firing's work is still waiting its turn" eight times (533742; 547823, 548003; 556400, 556760, 556940, 557300, 557480) and "Only one hand to heave lead" twice (556453, 556971). While she manoeuvres or makes sail the lead stops: no cast from 13:06 to 13:15, none from 15:27 to 15:42, close to the Gilstone both times.
- **The depth the officer quotes is the truth.** [CODE] `api/readings.py` 557 to 566: `the depth of water` is `chart.depth_at(world.position)`, the chart's depth at the ship's true position, at the datum. [CKPT] At the last tick the water under her was 66.83 m with the tide 5.68 m above the datum: 61.15 m, 33.4 fathoms; the officer's note says "in 33 fathoms". He used it knowingly (547065, 12:57): "The chart's depth under her updates as we go, so I'm treating it as a sounding machine." It is an exact sounder at the true position, in a game whose own source calls the position "the truth, which no reading gives", and it is why "no bottom at twenty fathoms" can stand beside a reading of 15 to 19.
- **He misread it once, and it decided the morning.** 527040, 07:24: "Two and a half fathoms is fifteen feet now, and with twelve feet more of ebb to come it'll be about three feet at low water. That would be too thin for any schooner." The reading is already at the datum: about fifteen feet at low water for a vessel drawing 10.9. From this he took "there's a bar or shoal across the Sound" and that the morning water was the best of the day, and planned to wait for one o'clock. Three things were missing: the reading is not labelled where he sees it (or he missed it), he could not find her draught, and the captain's chart shows no soundings.
- **The shoaling was real** (5¼ fathoms by the lead with the tide about 1¾ fathoms above the datum), on a north-going line close under Gugh. Turning out on it is what a seaman does. The captain's "I Think you had it" (526898) is also fair: she was aimed at the outer road, where the port file has 7 fathoms and the Road beyond 4 to 5.

### 6.9 The boat

No boat trip happened in this slice. (The session's five trips were at Plymouth and Roscoff, 1 h 56 m to 4 h 31 m each.) No boat was belayed in the hoist here: the note's case is from the earlier, restarted run. This slice shows a second way to the same end.

1. 13:33:06 (549186) "By the officer of the watch: sending the boat ashore." given while the anchoring evolution still held the hands (let go 13:22:49; "Brought up. Stations for furling sail" 13:29:56; done 13:42:29).
2. 13:33:07 (549187) "Not hands enough on deck to send boat; the hands are coming to anchor."
3. Nothing more. No "Away the long-boat's crew! Hoist out the long-boat.", no `boat.away`.
4. 13:54 (550494) captain's `send the boat ashore`: "The long-boat is away already."
5. 14:47 (553622) `belay send the boat ashore`: "Nothing in hand or waiting answers to 'send the boat ashore' ... The work in hand: weighing anchor." (553626) `send the boat ashore`: "The long-boat is away already." (553637) `belay hoist out the boat`: the same refusal.

[CODE] `ports.py` 1446 to 1462: the boat's state is set to away, phase "hoisting out", *before* the evolution is started. `scripts.py` 3923 to 3936 and 4117: the anchoring evolution ends with `_belay_held_work`, which belays every waiting piece of work and discards what it belayed without a line. So the waiting boat was dropped at 13:42 and its state never reset. [CKPT] at the end: `away: True, phase: 'hoisting out', errand: 'prices', port_id: 'st-marys', since_tick: 549186`. The captain's guess was exact. `boat_spec` always picks the largest boat, so the yawl in the ship file cannot be sent instead; and laying out a kedge is refused while the boat is "away" (`scripts.py` 5091).

Words: officer (549273, 13:34): "I won't recall the boat mid-hoist (the Roscoff lesson), so the long-boat goes for the prices"; (550508, 13:55): "The long-boat has been 'hoisting out' for twenty minutes ... so I'll watch that it actually leaves and doesn't stick"; (553533, 14:45): "the long-boat is away for the prices, or still hoisting out"; (553600): "an order refused for want of hands should either wait in the queue properly or be refused outright, not left half-begun."

The cost: at 1.4 miles from the outer road she was "in port"; the list would have come off and the brandy been sold from that berth (St Mary's pays £160 a ton by its file). The stuck boat ended the game.

### 6.10 Kedging and warping

Nothing. No order about a kedge, the stream anchor, towing, warping or sweeps in the slice or the session; the gate leaves them to M8. The last forty minutes (a mile from the gap, at high water, in baffling airs) are where a boat ahead or a kedge would have been tried; with the boat stuck, the kedge would have been refused.

### 6.11 The reckoning against the truth

[CKPT + RECON] The account's position after each of the captain's bearing rounds (the reckoning's stored track), against my cross-bearing fix from the same bearings. "First" is the error still left after only the first bearing of the round, a lower bound on what it was before.

| Round | Bearings (spread) | After the first | After the round | Truth then |
|---|---|---|---|---|
| 05:55 | 4 (33°) | 0.47 | 0.41 | outer road 3.7 at 302 |
| 06:17 | 3 (30°) | 1.25 | 0.84 | |
| 06:29 | 3 (35°) | 1.31 | 0.81 | |
| 06:35 | 4 (52°) | 0.64 | 0.35 | steering 335, Peninnis at 335 |
| 06:49 | 4 (73°) | 0.52 | 0.12 | gap 1.64 at 322 |
| 07:03 | 2 | 0.33 | 0.17 | outer road 0.84 at 336 |
| 07:11 | 3 | 0.50 | 0.23 | |
| 07:17 | 3 | 0.20 | 0.11 | outer road 0.73 at 353 |
| 12:00 | 3 (28°) | 1.20 | 0.32 | at anchor, outer road 4.5 |
| 12:31 | 5 (38°) | 2.26 | **1.21** | gap 4.46 at 326 |
| 13:03 | 6 (78°) | 1.23 | 0.03 | Gilstone 0.85 at 352 |
| 13:31 | 4 (81°) | 1.45 | 0.29 | at anchor; Gilstone 0.46 at 336 |
| 15:55 | 2 (64°) | 2.17 | 0.98 | gap 1.49 at 309 |
| 16:07, end | | | 0.24 | [CKPT] |

(miles)

- **The account runs at the log's last read.** [CODE] `reckoning.py`, `account_now` and `bring_up`: "the last worked position run on at the log's last read". [LOG] The log was hove three times: 06:00:42 "three knots and three quarters"; **08:00:41 "five knots and a half"**, 37 seconds after `heave to`; 16:00:36 "a quarter of a knot". None at 10:00, 12:00 or 14:00, at anchor. So after both weighings the account ran at 5½ knots while she drifted or made one to three. [CKPT] Between the 12:00:35 bearings and the noon line at 12:10 the account moved 0.44 mile; she was adrift for 4.8 of those minutes: 5.5 knots. At 13:31, at anchor, the account lay ashore on St Mary's until the bearings came. Between the bearing at 15:55:21 and the heave at 16:00:36 it moved 0.84 mile east, while she made a quarter of a knot. Nobody ordered `heave the log`, which is in the officer's domain.
- **Four or five bearings do not make a fix.** After five at 12:32 it was still 1.2 miles out (the marks within 38° of each other); after four well-spread ones at 13:32, at anchor, 0.29. Each bearing moves the account part of the way. [CKPT] At the end it was 0.24 mile out and rated itself at about 0.06 (the square roots of P's diagonal, if P is in square miles).
- **A near miss the log does not show.** Officer, 12:57 (547065): "The ledges are a mile off and I'm heading into the gap at 343°". [RECON] At 13:03 she was 0.85 mile from the Gilstone, steering 349 at about five knots, the rock bearing 352: ten minutes off, covered, never sighted. The captain's bearings caught it; officer (547515): "Your bearings have shifted the account a mile east: the Gilstone is now dead ahead, N one mile ... So we've been running up the Peninnis side, not the Sound".
- **The danger list follows the account.** 549190, 13:33, four bearings just taken: "The account now puts the Gilstone 'N by W, no distance', right on top of us"; the truth was 0.46 mile at 336. The captain's chart agreed with the account (549253: "about a cable and a half to our north").
- **The noon latitude did no harm.** [CKPT] observed 49° 52.6' with a rated error of 2.1 miles; the account's latitude went from 49.85168 to 49.85177. [RECON] the truth was about 49° 50.7', so the sight was two miles out and the account right. The update is properly weighted here.

### 6.12 The wind

[LOG] No `wind.shift` from 05:51 to 12:27; then 23 in 3 h 38 m. These are m5c-b's ten-minute means that have held two points for a minute:

- 12:27 SW by S; 13:06 SW by W; 13:11 W; 13:14 NW by W
- 13:37 W; 13:38 N by W; 13:42 NW
- 14:18 N by W; 14:22 NNE; 14:26 NE; 14:37 N by E; 14:49 NE by N; 14:55 N; 14:57 NW by N
- 15:15 NW by W; 15:30 W by N; 15:42 NW by W
- 15:54 W by S; 15:56 SW by S; 15:58 S by E; 16:01 SW by S; 16:03 W; 16:05 NW by W

Strengths are "light airs" twice, "a light breeze" three times, otherwise "a gentle breeze" or "a moderate breeze" (gusts 17, the mean 13, at 15:07). The mean cannot move so fast unless the instant wind reverses for minutes at a time, and the trim lines show that it did (6.7: ESE at 15:50:57 against a mean of W by N). 39 per-sail "taken aback" lines, 22 of them after 15:48; three `ship.aback`, two urgent and real, one notable "Her sails aback; she had no way on to lose." (558312), as m5c-b intends.

**A likely cause, from the code; not tested.** [CODE] `weather.py`, `sea_breeze`: from May to September, between 10:00 and 20:00, in fine weather, within 15 km of a coast (full within 5), up to 10 knots, peaking at 15:00, and "The onshore direction is the bearing to the nearest coast". Every condition held from about 13:00, when she first came within two miles of the land on a clear afternoon with a high glass. Among islands and rocks the nearest coast changes by a right angle as she moves a cable. And the coast is looked up through the same plane conversion that was 1.38 miles west of her [CKPT], which put the point on or beside St Agnes and Gugh while she lay off Peninnis. This would explain why the chatter began when she closed the land, why it struck a moderate breeze as well as light airs, and why it was absent all morning (before the onset hour, and in fog). It would not explain the Harpy's night off Penlee.

Also: "A smooth sea, the sea going down." (557880, 15:58), then at 16:00 the hourly line "a smooth sea" and, the same tick, "A moderate sea getting up." (558000).

### 6.13 The lookout

- Distances are the eye's, with an error drawn once per sighting and held until the ship has moved a mile [CODE]. Peninnis Head was "a mile" in all seven bearings taken within a mile and a half of it (06:49 to 15:55), while the truth ran from 0.78 to 1.44; the Nut Rock was "four miles" in all its lines, 06:49 to 13:44, at 2.4 to 3.0. Honest to a period eye, but inside two miles of rocks an estimate that waits for a mile of her own movement can outlast the danger.
- "The Crow Rock bearing N, steady and closing: distant three miles." (549720, 13:42) and "The Nut Rock bearing NW, steady and closing: distant four miles." (549840, 13:44) were hailed while she lay at anchor.
- When the fog lifted (543600), six sightings were logged of at least fifteen things in sight ("and 7 more in sight", 543624). Whether the leading marks were ever among the unlisted I cannot tell.

### 6.14 Words, slips and noise

- "By the officer of the watch: whatting is she." (527024; also 83160).
- "getting under way on the larboard tack and steer 315" (543919).
- "The gig hailed ... shorten sail and he will come aboard" to a ship at anchor (549180); "clear of the mouth of St Mary's Sound" to a ship standing in (526620).
- "Asked the officer of the watch: ... Maybe that will help a bit.?" (525860); "Order: Tell the officer If you please.." (534245).
- Two data files disagree about Peninnis Head: the feature at 49.90500 N, 6.30550 W; the Scilly patch's control point at 49.8985 N, 6.3050 W, four cables south.
- **Noise in ten hours**: 34 `light sails` refusals; 49 notable "No bottom at twenty fathoms."; 39 notable per-sail aback lines; 23 wind shifts; 17 `standing.held`; 53 "Compression eased to 1x".

## 7. The model as an officer

**Good calls.**
- **He would not guess among rocks.** 525095: "A guess about rocks with a falling tide on them is what put the Harpy ashore." And at the end, against the captain's "send it and pray" (558236): "we'd be at the mercy of whichever way the wind is pointing when we reach the ledges. That's the 'pray' part, and I'd rather not pray a mile from the Gilstone." The truth then was half a mile.
- **He acted first at the shoaling**: `steer 135` 17 seconds after the cast (526866), "Acting first and reporting after", turning "by the east, away from the Gugh side". The rule is in his journal from the Harpy.
- **He took the con from the captain when the captain was wrong, and said why** (526355): "NE would run her towards the Gilstone (NE by E, a mile) and the Spanish Ledge (NNE, a mile)." RECON bears him out. Earlier (526231): "One voice on the helm: you have it now, and I'll hold my orders."
- **He caught the chart contradicting the pilot** (6.2), and named the two false passages on the captain's chart from his own knowledge (526291: "Gugh is joined to St Agnes by a sand bar that dries at half tide. The gap between them is a blind bay, not a passage"; journal: the Garrison "an isthmus in reality, though the game draws the Garrison as an island"). His account of Crow Sound from memory (525160) agrees with the chart patch's "three feet at low water".
- **His course for the gap was right when he worked from the eye**: 557801, "about NW by W (309°), a mile and three-quarters off"; RECON 309°, 1.5 miles.
- **Candour about his own errors**: "my tide advice was backwards" (525919); "So I was wrong this morning" (527040); "I should have thought of it" (532406).
- **His reports for the book are accurate and specific**; code or checkpoint confirms seven: heave-in running to a short stay, the 5:1 scope, the boat left half-begun, `get under way` failing after `weigh`, the fixed range of the gig, "seven fathoms", the jumping account.
- **The trade advice was sound**: 558343, brandy "£315 a ton" at Plymouth against £100 paid (St Mary's file: £160).

**Mistakes.**
- **The tide, three ways in an hour.** 06:49 wait for the flood (right, and the port file's own unspoken advice); 07:05 go in now because there is more water over the ledges (true of the depth, not what the pilot meant); 07:24 wrong again, by taking a depth at the datum for the present depth and subtracting the ebb a second time (6.8).
- **He did not know her draught, asked once, and went on without it** (527040).
- **He took in mainsail and foresail at 05:55** (521708), leaving her unbalanced ("23° of helm") for the captain to cure.
- **He gave `tack ship` three times when she could not tack** (a beam reach; under fore-and-aft sail headed by the wind; while sail was still being set), and each time explained the failure line with a cause of his own. The line misled him (6.6); the orders were still poor ones.
- **He trusted an order's wording over its result.** `heave in 70 fathoms`, then two and a half hours on "a notable event" without looking (534612); "until got under way" on an order given too late (543919).
- **From 12:41 to 13:03 he conned by the account alone, towards the Gilstone**, though the captain had just told him his bearings were the better (543725), though he could have asked for a round, and though `heave the log` was his to give after weighing (6.11).
- **He ordered the boat away before the anchoring was done** (549186), told the captain "Brought up at 13:22" (the time she let go), noticed twenty minutes later that the boat had not left (550508), and did nothing about it for fifty more.
- **He repeated sail orders already in the queue** (556740, 556741).
- **He never used the deep-sea lead, a bearing, or `ask the pilot`.**

**Small invented or loose statements.** "Fog signals on the bell as the custom is" (532406), no such order given. "Mr Ellis is coming back out by the look of it" (548321); it was Mr Pender. "she's drifting ENE about two miles an hour" hove to (532406): the 12:00 fix puts the berth near where she hove to; I could not confirm it. The hand-over's "a mile" for half a mile.

**Wished for** [SAID]: a draught in the papers; soundings on the chart; named marks; "veering and heaving in ... one grant"; `get under way` to follow a weigh; a waiting order to wait or be refused; and, to the captain's circle idea (548213): "two or three bearings of known marks, crossed on the chart, give a fix good to a cable or two within a few miles of land, however poor the account ... The trouble today was the distances 'by estimation' and the bearings rounded to the point."

**On balance.** A careful, honest, quick officer who was safe and did not get in. With a rock half a mile off and the readings he had, safe was the right side to err on. His errors of substance were about what the game's words meant, not about seamanship.

## 8. Cross-check against the notes

**The owner's items.**

| Item | Evidence | Verdict |
|---|---|---|
| 1. Pilot boarded while under way | Ellis boarded hove to (05:51); left at "five knots" (07:17); Pender boarded a ship at anchor (13:36). [CODE] any ground speed up to 6 knots within two cables. | Adds nuance: speed is the only test, for boarding and for leaving. |
| 6. Soundings on the chart read "NaN fm" | Not visible to me. [CKPT] a no-bottom cast is stored with `depth_m: None`; 49 of 53 casts here are such. | Supports, as the likely source. |
| 9. Pilot automatic; wants hailing or signalling | Ellis left by rule and could not be kept; no pilot could be called for six hours; Pender came unasked and boarded at anchor (6.3). | Supports strongly. |
| 13. Stand-by on several conditions | "until got under way" on a dead event (543919); 13 two-minute timers as the substitute; the captain's relay standing orders; the captain's tip (544882). | Supports strongly. |
| 15. General authority | One more grant needed (534267), mis-parsed; all else on grants six days old "for the watch". The officer could "act first" at 07:21 only because `steer` had been granted. | Supports. Adds: "for the watch" already means until taken back. |
| 16. "Keep" orders | `trim` fired with a tack waiting and eased the sheets to 60° to 85° (557457); fired three seconds after `steady trim` (547378); belayed by hand before anchoring (548119). | Supports. Adds: should also stand off during a manoeuvre, and should not trim to an instant wind. |
| 17. Taken aback urgent in a calm (m5c-b) | Two urgent, both with way on; the third notable "no way on to lose" (558312). 39 per-sail lines. | Supports the fix, and the redacted addition about per-sail lines. |
| 18. Wind-shift spam (m5c-b) | 23 notable shifts in 3 h 38 m, in gentle to moderate breezes. | Adds nuance: a floor on strength would not have stopped these; the wind itself reverses. Likely cause in 6.12. |
| 19. Reckoning close to visible land | The whole slice; the table in 6.11; the captain's own words (548205); the 13:03 near miss. | Supports strongly. |
| 20. Chart tools | "If my markers were all named, I would feel more confident" (525082). | Supports. Adds: names on the danger marks. |
| 21. A turn need not end at say or answer | Eleven stand-bys set 50 to 53 s after a spoken line; the captain's tip (546431). | Supports strongly. |
| 24. Nearest land, and features by their parts | "St Agnes ... nine cables" with Gugh perhaps two or three cables off (526637); the captain's "little islets to the east" (526279); the Garrison drawn as an island. | Supports strongly. |
| 25. Chart or ship view as an image | The captain sent a picture through the chat (525860); a new plan followed at once (525919), and "Now I get it! Fantastic!" | Supports strongly. |

Items 2, 3, 7, 8, 10, 11, 12, 14, 22, 23: nothing in this slice. (For 3: prices were never fetched; the St Mary's file does trade coal at £3, pilchards at £13, brandy at £160.)

**The model's comments and additions.**

| Note | Evidence | Verdict |
|---|---|---|
| "The 'two cables' rule is applied on boarding but not on leaving" | [CODE] leaving also needs two cables; the "mile away" is the lookout's held estimate. Here the gig was "distant a mile" at 07:11 and took him at 07:17. | Contradicts as to the rule; supports as to what the log shows. |
| "'a sounding' also wakes on 'no bottom at twenty fathoms'" | 524096. | Supports. |
| "A worse figure shouldn't replace a better one" | No lunar here. The noon latitude, two miles out, moved the account 0.0001° (6.11). | Adds nuance: the noon update is weighted properly. The trouble here is the stale log speed and bearings that only part-correct. |
| "The danger list follows the account, so it misleads" | 549190, 547065 (6.11). | Supports strongly. |
| The relay's 60 seconds and `--wait 50` | The 50 to 53 s gaps after each spoken line. | Consistent. |
| "The contrary-orders warning fires on ordinary sequences" | All 10 nudges, including the note's own example again (553598). | Supports strongly. |
| "Kedging is refused while aground" | Not exercised. [CODE] also refused while the boat is "away". | Cannot be seen; adds a second refusal. |
| "With sternway, the helm steers as if she had headway" | Not visible in the log. [CKPT] the rudder is on the shifted side at the last tick; [CODE] the helmsman shifts at 0.15 m/s. | Contradicts for a steered course; a fixed helm (hove to) is not tested here. |
| "'get under way' doesn't cast her head onto the ordered tack" | Never ran here. | Cannot be seen. Adds: given after `weigh`, it fails outright. |
| "'Trim sails' acts before the helm has swung" | One mild instance (526942); `steady trim` is the workaround. | Supports weakly. Adds the worse case: trims to an instant wind. |
| "The hand lead says 'no bottom' ... while the depth reads 15 or more" | 6.8. | Supports, and corrects: the reading is the chart's depth at the datum at the true position, without the tide; a deep-sea lead exists and works. |
| "Lead standing orders fight for hands" | One rule at a time here; "held" eight times, "Only one hand" twice. | Adds nuance: with one rule the lead still stops during manoeuvres. More serious, the lead blocks other orders (6.6). |
| "The Harpy log said 'brought up in no water'" | "in seven fathoms" after "let go in 37" (549749) and its cause (6.4). | Adds the likely cause. |
| "The Harpy's reckoning kept advancing while she lay at anchor" | [CKPT] the account moved 0.44 mile between 12:00:35 and 12:10; all of it fits the 4.8 minutes adrift after the anchor came aweigh. | Not shown at anchor; shows the related fault (the stale log speed). |
| "Belaying a boat mid-hoist leaves it stuck" | No belay here; the same stuck state by another road, with its cause (6.9). | Supports the state; adds a second cause. |
| "Each boat trip ... about 4½ hours" | No trip in the slice. | Cannot be seen. |
| "Other ships keep a fixed distance" | The gig "still logged two miles off" (521473); [CODE] the estimate waits for the ship's own movement. | Supports, with the cause: a held estimate, not a circling ship. |
| "The water sail", "Number words above twelve", "'Full and by' is refused" | Not exercised. The captain's `light sails` workaround produced 34 refusals. `keep her full and by` was accepted. | Cannot be seen. |
| "What worked well: the pilot's directions at Roscoff" | At St Mary's the directions could not be followed with what the deck is given (6.2). | Adds nuance: fine words, not usable when they rest on transits. |
| "Fixes from bearings once the land came up" | They were the navigation here, and still left 0.1 to 1.2 miles. | Adds nuance. |
| "The new quieter 'aback' lines" | 558312. | Supports. |
| "Number-free standing orders" | `close lead`, `approach lead`, `steady trim` did real work. | Supports, with the costs in 6.6 and 6.7. |
| "The order 'what is she'" | Used at 527024; the acceptance line reads "whatting is she". | Supports, with a slip. |
| "The noon latitude" | Logged 544200; two miles out, and ignored by the account. | Adds nuance. |

## 9. New findings not in the notes

Ranked by weight.

1. **A tack that has to wait fails in the words of a missed stay.** All three `ship.fell_off` lines of the session (525177, 547564, 557569) are a `tack ship` queued behind the leadsman's cast, failing a precondition when the cast ended, and logged as "Squared the yards; she fell off on the ... tack" with no reason and no attempt (6.6). The officer gave up tacking in the Sound on the strength of it (548046). The general fault: an order that waits has its preconditions tested late and its failure told as a physical one; and the lead, an evolution on the ship, makes most orders wait.
2. **The pilot's leaving rule and the six-hour bar.** One three-minute board to seaward lost the pilot (525900); he left as she stood in, 0.7 mile from the outer road (526620); none could come until 13:17; one then came unasked and boarded at anchor (549360). The port file's "Take the Sound on the flood" is never spoken (6.3).
3. **The account runs at a stale log read.** 5½ knots, read at 08:00:41 as she hove to, was used after both weighings until 16:00:36. The account was 1.2 to 2.3 miles out through the afternoon and lay inland while she was at anchor. Hence the 13:03 run at the Gilstone (6.11). The log is not hove when she gets under way.
4. **A boat ordered during an all-hands manoeuvre is dropped and left "away".** `_belay_held_work` at the end of the anchoring, and a boat state set before the work starts; no log line (6.9). It ended the game and would also refuse a kedge.
5. **The plane and the sphere disagree by 1.38 miles after this voyage**, and the anchor's depth is read through the disagreement: "Brought up ... in seven fathoms" in 37, the cable "up and down" with eight fathoms or fewer out in 34 (6.4). The weather's coast lookup uses the same conversion.
6. **`heave in 70 fathoms` is accepted and the number ignored** (534284): 163 fathoms came in; the result is a routine line that wakes nobody; there is no order to shorten scope to a figure (6.4).
7. **`the depth of water` is the truth.** An exact sounder at the true position, at the datum, unlabelled where the officer reads it; he navigated by it and misread it once, decisively (6.8).
8. **The Spanish Ledge is charted on the wrong hand** for the pilot's words and for its own description (6.2).
9. **The afternoon wind reversals are probably the sea breeze** blowing "toward the nearest coast" among islands, perhaps from the displaced point (6.12). To be tested.
10. **Her draught is not to be found in the papers** by "draught" or "draws" (527027, 527030), and the Pool he proposed at 05:52 is closed to her by the port file (over nine feet).
11. **`come to an anchor` always veers five times the depth** unless told, holds all hands 27 minutes, and its event comes 12 minutes after she has brought up (6.4, 5).
12. **`get under way` after `weigh` fails** rather than making sail (544495); a `weigh` alone leaves her adrift 10 to 12 minutes (6.5).
13. **`clear away the bowers` is read as `let go`** (521645). Refused only because the object was not a "part".
14. **Two can con at once.** Seven helm orders from two hands in 2 m 45 s (526190 to 526355), with no line about the deck and no nudge.
15. **A rule already satisfied is logged as a refusal each time it fires**: `light sails`, 34 lines.
16. **Each sampling drops the game to 1x** (53 lines).
17. **Slips of wording** (6.14).

## 10. Could not determine

- **What the officer was shown.** Every statement about his readings is from his own words; in particular whether the depth reading says "at the datum" where he reads it, and what a nudge looks like to him.
- **Which precondition failed** for each of the three queued tacks. The reason is in the event's data, not in the dump.
- **Her true track between bearing rounds**: how close she passed to Gugh at 07:21, where the 2½-fathom patch lies, and so whether holding on at 07:21 would have taken her in. The geometry says she was aimed at the outer road with 15 feet at the datum under a keel of 11; I cannot say more.
- **Whether the Great Minalto, the Great Mincarlo or the daymark were ever in the lookout's list** ("and 7 more in sight").
- **Whether she dragged** on 67 fathoms between 10:00 and 12:00. The officer says so; no line does.
- **The sea-breeze explanation.** Code reading and coincidence of time and place only. It needs the coast lookup evaluated at the true and at the plane position for ticks 547500 to 558434.
- **Whether the plane and sphere disagreement touches anything else** (other vessels, the gig's approach). I checked only the anchor's depth and the coast hook.
- **The two knots of sternway hove to** (531421): his word only; no checkpoint from that hour belongs to this game.
- **The tide.** "Riding ... to the ebb" at 09:22 and, by the officer, still at noon, with low water at about 10:30 and no "she swings" line while at anchor. Whether the stream offshore should turn so late I cannot judge.
- **Whether `come to an anchor in 130 fathoms`** would have given a 130-fathom scope (the primer suggests so), and whether `ask the pilot` is within the officer's domain; neither was tried.
- **Real time.** Ticks are ship's seconds; the owner could hold the clock (he seems to have done so while the chart picture was sent: only 44 ticks pass between 525868 and 525912), so I cannot say how long the model took in wall time, nor explain the 5 m 23 s turn at 09:24.
- **Why a chain of six contrary orders raised no pause**, against primer 16.
