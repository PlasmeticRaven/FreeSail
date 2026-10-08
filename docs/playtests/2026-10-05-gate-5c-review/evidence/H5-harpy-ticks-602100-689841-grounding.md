# H5. Harpy, ticks 602,100 to 689,841: the grounding on Penlee Point and the night after

## 1. Slice identity

- **Session** `2-harpy-brig-opus`, slice 5 of 5: **ticks 602,100 to 689,841**, ship's time **19 June 1805 04:15 to 20 June 04:37** (the end of the game). 87,741 ticks, 1,599 log lines.
- **Ship** the merchant brig *Harpy*, American colours, Captain Bowen (the owner). Draught in the save 3.5 m (11 ft 6 in; the log says "she draws 11 feet"), waterline 26.8 m, some 120 people.
- **Station** officer of the watch "Mr Pearce", **Opus 5.5 through the MCP door (Claude Desktop)**, its **fifth seating** (602,283). Pilot Mr Tozer of Plymouth aboard from 578,880 to 683,520.
- **Build: m5c-b with package 37b (re-seating) in, and package 37c (the quieter wind-shift and taken-aback lines) not in.** The log's wording shows it:
  - 37b: 602,283 "The officer of the watch takes the station again (Opus 5.5, through mcp): the fifth seating; it had stood down by the officer of the watch: the deck handed over."
  - Wind shift: 265 `wind.shift` lines between 12:00:00 and 13:50:54 on the 19th, 179 of the 264 gaps fifteen seconds or less, the shortest one second (633,107 "Wind backed to SSW" / 633,108 "Wind veered to SW"). That is the instant-wind line. The captain remarks on it at 634,699 "OK, now that is some threshold flickering." and offers at 635,367 "we could live update the game to at least douse the chatter in the log"; the officer answers "once she's at anchor, if you will."
  - Taken aback: all four `ship.aback` lines in the slice are urgent in the old words ("Taken aback: the sails pressed against the masts and she lost her way."). The new notable wording (the changes file gives "Her sails aback as she lies at anchor / aground" and "...she had no way on to lose") never occurs in the whole Harpy log (0 of 31).
  - After 13:50:54 there are only three `wind.shift` lines to the end (18:32, 18:43, 19:55), which would fit either rule in a steadier westerly; the log has no line for a reload, so the log alone cannot say whether anything was updated mid-slice. The file times say not: the 37c sources in `D:\Projects\FreeSail\FreeSail-gate-m5c-b` are stamped 07:10 to 07:25 on 3 October, the Harpy's last save 06:58.

**How this was read, and the evidence classes used below.** Everything is read-only; no game tool was called. Besides the dumps I read, in memory and without running any game code, the save's checkpoint (`D:\Projects\FreeSail\FreeSail-gate-m5c-b\saves\freesail-seed7-tick689841.checkpoint`), because it holds what the dumps drop: each log event's data fields (the lookout's true bearing and distance, the account's position at each fix, the grounding's depths) and the samples the harness actually sent the officer (the readings as told). I also read the m5c-b source where a line needed explaining. Tags:

- **[LOG]** text of a log line, as in the dumps.
- **[DATA]** a data field of a log event, or a reading as told to the officer, from the checkpoint.
- **[CALC]** my arithmetic on [DATA] (true positions are worked back from the lookout's true bearing and distance of charted marks; three simultaneous sightings at 12:00 agree within 3 m; between sightings I interpolate, good to about 100 m).
- **[CODE]** my reading of the source, not tested by running.
- **[SAID]** what the officer or the captain said: opinion or claim.

## 2. What happened

1. **04:15 to 04:18** (602,100 to 602,283). The officer hands over "for the relief through a local door (fifth seating)", is seated again 183 ticks later through mcp, and is given the deck: "Mr Pearce, you have the deck."
2. **04:18** officer heaves short (accepted under a standing grant); 04:39 "Hove short on the best bower: forty-three fathoms of cable, the cable a-stay in 29 fathoms." Flat calm, glass falling.
3. **08:00** (615,600) "Fog came down." Officer asks to veer again; captain: "You may veer." Two forms of the order both run and stack: "Veered to a hundred and thirty-seven fathoms on the best bower."
4. **11:58** noon by account, no sight. **12:00** (630,000) "The fog lifted."; the lookout raises Rame Head, Penlee Point and Rame church; the officer orders `get under way` at 12:00:08. Captain: "That's it. There's the window."
5. **12:27:46** (631,666) "The best bower is aweigh." **12:35:53** under way; officer steers NE and sets all plain sail; the captain has the main topgallant staysail set "just to show off".
6. **12:48** captain takes four bearings by hand; officer comes to NE by E and stands by a glass. The lookout's three "steady and closing" lines (12:51, 12:57, 13:04) fall inside that stand-by among 132 wind-shift lines.
7. **13:18** officer asks the pilot, gets the stock sailing direction, and comes back to NE "to pass about a third of a mile outside Penlee". **13:28:50** officer takes a two-bearing fix.
8. **13:25 to 13:37** the wind backs from SSW to SSE, SE and E by N in flicks; **13:37:09** urgent "Taken aback". Officer orders `tack ship`, then `let go the anchor` "in 11½ fathoms ... a mile off Rame Head and Penlee".
9. **13:38:11** captain: `avast all` (the anchor belayed in its stand-clear), `Steer north east`, and "I'll con her, don't worry."
10. **13:43:24** captain: `Steer north northeast`. In truth that points within 4° of Penlee Point, 5.7 cables off [CALC]. **13:46:27** officer: "Sir, NNE is heading straight at Penlee Point!"
11. **13:48:13** captain's bearing: "Penlee Point bore NNE, a mile by estimation." (true 2.9 cables). **13:49:02** captain: `steer northeast`. **13:50:08** aback again. **13:50:18** officer's second warning; **13:50:26** "Penlee Point bore NNE, a mile by estimation." (true 1.7 cables); **13:50:31** officer lets go the anchor on his own word.
12. **13:50:53** (636,653) **she takes the ground** at three knots, 273 m (1.5 cables) S by W of the charted position of Penlee Point [CALC], everything set. "The carpenter reports her stove on the rock and making water."
13. **13:51 to 13:57** all sail in; captain: "Well, that's on me. I was reading the reckoning on my chart that was wrong". `man the pumps` unknown; `lay out a kedge` refused to the officer, allowed, then refused by the ship: "she is aground".
14. **13:57** captain: "Let's try sending the purser ashore." The launch goes to the Barbican for prices (away 14:03, back 16:31).
15. **14:43, 15:36, 16:29, 17:21** the well: "a foot ... 2 feet ... 3 feet ... 4 feet of water in the well, and gaining."
16. **17:34:32** (650,072) the captain sells the brandy from the grounded ship: "Sold 15 tons of brandy at Plymouth at £315 a ton, £4725 taken; the boat lands it. The purse: £5154." The launch leaves with it at 17:40.
17. **18:04:00** "She is off, and afloat again on the flood." **18:04:21** aground again "at half a knot". Captain: "frankly I was considering we simply seek a different command".
18. **18:32:00** afloat again; the officer orders `heave short` two seconds later, then `get under way ... and steer S`. 18:39 "Hove short ... nine fathoms of cable"; "Could not get under way: the launch is away; she cannot leave without her boat."
19. **18:41:28** "The best bower is dragging". Nobody is awake to it (the officer had stood by for the boat three seconds earlier). She drags about 170 m east into nine fathoms; 18:58 "The best bower holds again."
20. **20:10** sunset; **21:23** the launch is back. The officer proposes to lie till daylight; the captain agrees "if the well isn't gaining".
21. **00:00 to 00:05** (20 June) `send for the carpenter` (allowed since 21:24) brings Mr Kemp aft with nothing to say; `sound the well`: "The ship has no well to sound yet". Watch below piped down.
22. **01:47** captain: "that depth is shortening worryingly" (soundings 9¼ down to 5½ fathoms). Officer gets under way on the starboard tack steering S; aweigh 01:59, under way 02:05.
23. **02:23** "The pilot asks for sail to be shortened: his cutter is coming off for him." Officer heaves to. Captain: "The pilots aren't worth a damn yet ... We'll make this entrance ourselves or not at all".
24. **02:26 to 02:52** filled away, then 25 minutes with no course given; she loses her way and makes sternway. **02:52** "Mr Tozer left her in the cutter, clear of Cawsand Bay; the pilotage, £6, paid and his certificate signed."
25. **02:52 to 03:13** officer steers ENE; she will not pay off; captain puts the helm hard down and hard up by hand; 03:11 urgent "Taken aback"; captain: "You have the full con from here."
26. **03:14** captain's standing order "Bearings" (every 5 minutes). **03:39** officer hauls up N, **03:53** NNW for Cawsand.
27. **04:05** officer orders `come to an anchor` (allowed at 03:54); captain belays it, reading his chart; she stands on. About 04:04 she passes over the charted position of the Dragstone [CALC] without touching.
28. **04:14** lead 5½ fathoms; officer anchors as he had said he would. **04:20** "The best bower let go in four fathoms." **04:35** "Brought up by the best bower in no water, twenty-one fathoms of cable".
29. **04:37** (689,841) final journal and hand-over; the game ends.

## 3. The deck and the captain's words

**The deck.** Given at 602,283 ("Order: you have the deck." / "Mr Pearce, you have the deck. The officer of the watch has the deck; the captain's standing orders are his night orders."). Never taken back: there is no `I have the deck` in the slice. The next `agent.deck` change of hands is the officer's own hand-over at 689,841. So by the log the officer "had the deck" at the moment she struck, though the captain had the con by his own word (see 6.2, question 1).

**Allowances carried over.** [DATA] The reseat brief at 602,283 lists what the captain's earlier words still allowed: "may also heave short; send the boat; buy; weigh; set plain sail; get under way; shift (the course); steer; take a bearing of; tack ship; fill away; wear ship; heave to; work up the reckoning; let go; let go the anchor; sell; unmoor; box haul; shape a course for (plymouth); observe the sun". These were given on 12 to 18 June "for the watch" and survived four stand-downs and many watches. Used in the slice: heave short, get under way, set plain sail, steer, take a bearing of, tack ship, let go the anchor, heave to, fill away, send the boat.

**New allowances in the slice (5), all asked for after a refusal or a doubt:**

| Tick, time | Captain's words | Log's answer | Used? |
|---|---|---|---|
| 615,624, 19th 08:00 | "You may veer" | "The officer of the watch may veer cable, by the captain's word for the watch." | At once, twice (615,627). |
| 636,998, 13:56 | "You may lay out a kedge" | "The officer of the watch may lay out a kedge, by the captain's word for the watch." | Tried 3 s later; the ship refused: "she is aground". |
| 663,887, 21:24 | "You may send for the carpenter" (after the typo "You may senf for the carpenter" was rejected) | "The officer of the watch may send for (carpenter), by the captain's word for the watch." | At 673,202, 00:00. |
| 673,254, 20th 00:00 | "You may pipe down" | "The officer of the watch may pipe down, by the captain's word for the watch." | No: the captain typed `pipe down` himself five seconds later. |
| 687,262, 03:54 | "You may come to an anchor" | "The officer of the watch may come to an anchor, by the captain's word for the watch." | 687,931 (belayed by the captain) and 688,471. |

**What the captain did by hand.** 27 of the slice's 45 bearings (the officer took 2, the captain's "Bearings" standing order 16); every helm order from 13:38:18 to the strike; `avast all`, `All hands`, `Heave the lead`, `Take in all sail`; the sale of the brandy (the officer had the `sell` grant but asked "Shall I sell the brandy?" at 17:20; the captain sold it himself at 17:34); `pipe down`; the hard-down and hard-up at 03:07; `Belay that` and `Moor her` at the end.

**The captain's words that carry intent, design thinking or feedback** (29 `tell` lines in the slice; the telling ones):

- 634,699, 13:18: "OK, now that is some threshold flickering." 635,367, 13:29: "If you like, we could live update the game to at least douse the chatter in the log."
- 635,913, 13:38: "I'll con her, don't worry."
- 636,831, 13:53: "Well, that's on me. I was reading the reckoning on my chart that was wrong, and trusted it too late. You were right to call the alarm, and I misread the severity. We may be done here, but the silver lining is we can probably still sell the brandy, at least, even if we're foundering at the same time. At least the tobacco stayed dry..."
- 636,863, 13:54: "Unfortunately the pumps are not modeled, but fortunatley we won't sink fully I believe."
- 636,916, 13:55: "I will say in my defense, I wouldn't have made quite so grave an error I think if I had been able to really see where I was with my eyes as I could have in the weather and distances we're at."
- 636,982, 13:56 (of the kedge): "We can certainly try, but I am not sure it's functional yet."
- 651,947, 18:05: "Aye, if you please, but frankly I was considering we simply seek a different command, since this one is liable to stay foundered no matter what."
- 673,513, 00:05 (of the well): "Aye, that's expected, this is still only the first real test version so it's a surprise it works at all frankly"
- 679,660, 01:47: "that depth is shortening worryingly"
- 681,888, 02:24: "Frankly, he can stay off for now. The pilots aren't worth a damn yet, except for their basic notes. That'll come through later. At some point we'll be able to ask the pilot any question we can think of or give him the helm. We'll make this entrance ourselves or not at all, and with the wind out of the west, I'm tempted to get up past the Dragstone, anchor, and sell her for a nice schooner."
- 684,794, 03:13: "My apologies, I saw the helm was trying to steer through the wind with no way on and no orders, so I tried to get her to fall off with manual orders, but I sped up the compression without thinking. You have the full con from here."
- 688,082, 04:08: "Oh, my bad, I was watching the chart and I thought you panic anchored before the dragstone as we really passed right over it on my chart, maybe we scraped the bottom of the hull with it. We'll proceed a bit further just for my edification, then moor."
- 688,157, 04:09: "No need, I think its accounted for with the reckoning error on my chart. We were probably close, but not that close in truth and the chart reflects the error purposefully."

One question was put by a standing order of the captain's, not typed: 681,780 "By standing order 'The pilot asks off': the captain asks the officer of the watch: the pilot wishes to be put off, what is the best course of action here?" The officer answered with the `answer` tool (681,791).

## 4. Orders refused

15 `order.rejected`, 4 `agent.refused`, 1 `evolution.failed` in the slice. Classes: (a) vocabulary or grammar gap, (b) domain refusal working as designed, (c) domain refusal that looks wrong for an officer with the deck in 1805, (d) ship-state refusal that is correct, (e) apparent bug.

| Tick, time | By | Order as typed | Refusal's words | Class | What was tried next |
|---|---|---|---|---|---|
| 635,861, 13:37:41 | officer | `as you were` | "'as you were' is not an order this ship understands; did you mean 'ease' or 'give chase'? An order begins with a verb such as set, take in, furl, reef, shake out, brace, trim or haul." | (a) a sailor's phrase for cancelling the last order. `Belay that` works (the captain used it at 687,970). | Nothing; he went to `let go the anchor`. The tack fell off by itself. |
| 636,737, 13:52:17 | officer | `man the pumps` | "'man the pumps' is not an order this ship understands; did you mean 'demand'? ..." | (a), and the thing is not modelled. | Told the captain; captain: "the pumps are not modeled". |
| 636,985, 13:56:25 | officer | `lay out the stream anchor astern` | "There is no such part as the out in this ship; did you mean the spanker outhaul, the trysail outhaul or the boom mainsail outhaul? ('brace' was understood.)" | (a); the parse ("'brace' was understood") is odd enough to note as (e). | Looked up "kedge" in the library twice, then the book's form. |
| 636,993, 13:56:33 | officer | `lay out a kedge to the SW` | "The officer of the watch may not lay out a kedge to the SW without the captain: the anchor is let go and weighed by the captain. 'lay out a kedge to the SW' not carried out." | (b) as designed; (c) in an emergency: "let go the anchor" was already allowed, a kedge is a different verb. | Asked; allowed five seconds later. |
| 637,001, 13:56:41 | officer | `lay out a kedge to the SW` | "Order not carried out ('lay out a kedge to the SW'): she is aground" | (e) design gap: refused in the one state it exists for. [CODE] `LayOutKedgeScript.check` returns "she is aground"; so do come to anchor, let go, weigh, get under way, moor and unmoor. | Nothing left to try. Officer: "aground is exactly when a seaman lays out a kedge". |
| 637,060 / 637,074 / 637,083, 13:57 to 13:58 | captain | `Demand a spare ship`, `Demand insurance payout for the Harpy`, `Demand 10 tons of tobacco` | "The yard at Plymouth has no ship; it supplies topmast, topgallant_mast, yard, suit of sails, cordage, water, provisions." (and the like) | (d), jokes. The raw identifier "topgallant_mast" leaks into the prose, and the yard answers a ship aground off Penlee with no boat sent. | None. |
| 653,995, 18:39:55 | (officer's order of 18:32:40) | `get under way on the starboard tack and steer S` | `evolution.failed`: "Could not get under way: the launch is away; she cannot leave without her boat." | (d) by the rule, but it was accepted at 18:32 and failed seven minutes later, after heaving short; the launch was away landing the brandy. | Stood by for the boat; the drag did the rest. |
| 659,419, 20:10 | standing orders 'night sail' (2) and 'night wings' (1) | `take in the royals`, `take in the flying jib`, `take in the stuns'ls` | "Nothing done: the fore royal is already furled; the main royal is already furled." and a 700-character list of ten studdingsails "already furled" | (d), but it is log noise from a book that does not know she is at anchor with nothing set. | n/a |
| 663,874, 21:24 | officer | `send for the carpenter` | "The officer of the watch may not send for the carpenter without the captain: the people are sent for by the captain. 'send for the carpenter' not carried out." | (c): the officer with the deck of a leaking ship cannot call the carpenter. | Asked; allowed. |
| 663,883, 21:24 | captain | `You may senf for the carpenter` | "'senf for the carpenter' names no order the officer of the watch could be allowed; say the order's words first ('you may tack ship if the land closes within two miles')." | (d), a typo, with a helpful answer. | Retyped. |
| 673,248, 00:00 | officer | `pipe down the watch below` | "'pipe down' was understood, but not 'the watch below'; did you mean 'either', 'the watch' or 'go below'? ..." | (a) | `pipe down`. |
| 673,250, 00:00 | officer | `pipe down` | "The officer of the watch may not pipe down without the captain: all hands are called, and the watch sent below, by the captain. 'pipe down' not carried out." | (b), arguable (c): all hands had been up ten hours. | Asked; allowed; the captain did it. |
| 673,476, 00:04 | officer | `sound the well` | "Order not carried out ('sound the well'): The ship has no well to sound yet; that reading comes with the world." | (e): the same log has four carpenter's reports of the water in that well. | Told the captain. |
| 681,965, 02:26 | officer | `steer ENE` (sent with `fill away` in one turn) | "She is hove to; fill away before giving her a course." | (d), correct. | Not re-sent until 02:52 (see heading 5). |
| 684,834, 03:13 | captain | `Take a bearing of rame` | "2 marks in sight answer to 'rame': Rame Head bearing NW and Rame church bearing NW by N; say which." | (d). The same words had been accepted at 680,524 and 683,527 when the church was not in sight. | `Take a bearing of rame head`. |
| 687,143, 03:52 | officer | `come to an anchor` | "The officer of the watch may not come to an anchor without the captain: the anchor is let go and weighed by the captain. 'come to an anchor' not carried out." | (c): he already held "let go the anchor", "weigh" and "get under way", and had just been told "You have the full con from here" and "take us in as you like". The grant is by verb, not by matter. | Asked; allowed at 03:54. |

**No order of the officer's was refused in the minutes before the strike except `as you were`.** `tack ship` (13:37:32) and `let go the anchor` (13:37:48 and 13:50:31) were both accepted under the standing grants. The phrase "to avoid an immediate danger" does not occur in the slice at all. It occurs once in the whole Harpy log, on 14 June at 217,355: "The officer of the watch may not keep her full and by without the captain: the course is the captain's, never to be changed without his directions unless to avoid an immediate danger. 'keep her full and by' not carried out."

## 5. Harness behaviour

**Seating.** 602,100 `hand_over` (note quoted in 6.11); 602,283 "takes the station again (Opus 5.5, through mcp): the fifth seating". [DATA] The reseat brief is a 25,507-character operator message: the consent text, the tools, the whole book of 21 standing orders with their firing counts, "The last 20 lines of the log", every reading, and the station brief. The handover note is in it only because it was the fourth line from the end of those twenty; nothing puts it there on purpose. The officer's first words: "Mr Pearce back on the quarterdeck, sir: the fifth seating, and I've read my own handover note." It had what it needed: grants intact, the pilot's marks, the plan. No sign of a lost thread in this seating.

**Stand-bys.** 46 `stand_by` calls and 8 more taken "out of turn" by the door; 53 `agent.stood_by` lines (one call left none). `until` values: ten minutes (10), a notable event (8), a glass (4), brought up (4), steady on the course (4), five minutes / 5 minutes (7), the change of the watch (3), the boat alongside (2), got under way (2), afloat (2), under way, two bells, six bells, the pilot off, filled away, a sounding, a change in the sky (1 each). One refused or not understood: `stand_by({"until": "an hour"})` at 650,054 leaves no line and is followed a tick later by "a glass".

**What woke the station** (53 `agent.resumed`): a word from the captain 18, ten minutes 6, a notable event 6, an urgent event 5 (four "Taken aback", one grounding), a glass 4, the boat alongside 2, steady on the course 2, five minutes 2, and one each of got under way, under way, the change of the watch, brought up, afloat, a sounding, a question from the captain, a change in the sky. The urgent wakes were all worth it. Three stand-bys cost something:

- **632,883 to 634,683 (12:48 to 13:18), "a glass".** [DATA] The sample that ended it says "notable": 136 for the half hour: 132 `wind.shift`, 1 `yard.braced`, and the three `lookout.closing` lines for Rame Head, Penlee Point and Cawsand. The only words the lookout ever gave about closing the land arrived as 3 lines in 136.
- **654,085 (18:41:25), "the boat alongside".** Three seconds later: 654,088 "The best bower is dragging: veer more cable; let go the small bower, or back her with the stream." Notable, so it did not wake him. He next spoke at 663,836 (21:23), 2 h 42 min later. The drag happened to carry her clear.
- **682,023 (02:27:03), "filled away".** The log at that tick, in order: `ship.filled_away` "Filled away; braced full and steering SSW (199°)."; "Compression eased to 1x: the officer of the watch is sampled."; "The officer of the watch stands by until filled away". The wait was accepted at the tick the event fired and was not ended by it. Nothing woke him until the captain's standing-order word at 683,520, 25 minutes later, during which she lay with no course ordered, lost her way and made sternway. Whether this was the model answering the wrong sample or a race at the door I could not settle (heading 10).
- A lesser one: 650,055 "a glass" while waiting for her to float. `ship.afloat` at 651,840 is notable and did not wake him; the glass did, by chance, 15 s later, 6 s before she struck again.

**Out-of-turn stand-bys** (8 `DOOR-EVENT by=out of turn door=stand_by`): afloat, two bells, 5 minutes (3), a notable event (2), a sounding. All were taken and all show as `agent.stood_by`.

**Nudges.** Two, both wrong:

- 681,965: "The officer of the watch nudged: 3 contrary orders on the yards and the helm within the watch (trim sails; heave to; fill away)."
- 683,528: "The officer of the watch nudged: 4 contrary orders on the yards and the helm within the watch (trim sails; heave to; fill away; steer ENE)."

Heaving to for the pilot's cutter (in answer to the captain's own standing-order question), filling away at the captain's "take us in as you like", and steering ENE are one plan. No pause followed the fourth, though four had paused the station on 18 June (533,573).

**Handover notes.** Two, quoted in 6.11. The last one tells the relief "Trust the bearings over the chart's reckoning, which is about a mile south-east of her true place"; the save puts the account 0.32 nm east of her (6.2, question 3).

**Tools.** `submit_order` 46 (34 accepted), spoken text 49, `stand_by` 46, `library` 4 (grammar of veer; kedge twice; send the boat), `shelve` 1, `read_log` 1 and `state` 1 (both in the minute after the strike), `journal` 1 (the final one), `answer` 1, `hand_over` 2, `readings` 0. Every figure the officer quoted came from the readings sent with each sample.

**Two orders in one turn, both run.** 615,627 `veer cable to 90 fathoms` and `veer 47 fathoms of cable` were both accepted and stacked (137 fathoms). Officer: "my error, and a harmless one".

**Silences.** 16:31 to 17:20: the boat came alongside at 646,296; the officer's report of the prices is logged at 649,213, 49 minutes of ship's time later (the clock does not wait for the model). No sign of context, budget or relay limits in this seating. By the save files' times the seating ran about 70 real minutes (05:48 to 06:58), an average of some 21 ticks a second.

## 6. Ship, sea, navigation and port observations

### 6.1 The grounding reconstructed

**Where things are** [DATA, the chart's feature file]: Rame Head 50.3155 N 4.2245 W; Penlee Point 50.31904 N 4.19086 W; the Dragstone 50.3210 N 4.1790 W, 4.7 cables E by N of Penlee; the Knap 1.28 nm NNE of Penlee; Cawsand town 50.3320 N 4.2020 W. Visibility from 12:00 "a few miles" [DATA], which by the sightings is 4 nm (new marks are raised at 7.33 to 7.41 km).

**The two hours before the weighing** (at single anchor, 137 fathoms out, in 28 fathoms):

| Time (tick) | What the log said | What the officer did or said |
|---|---|---|
| 10:00 (622,800) | "Thick, fog; the glass 30.07; a smooth sea, easy." | Standing by "a change in the sky" since 09:30. |
| 10:33 (624,820) | "Wind backed to SW by W, light airs." | |
| 11:00 (626,400) | "Thick, fog; the glass 30.08" | |
| 11:14, 11:23 | "Wind backed to SW by S, a light breeze." "Wind veered to W by S, a light breeze." Gusts 7 to 9 knots. | |
| 11:58 (629,880) | `reckoning.noon` "Noon. No sight; the sun was hid at noon in fog. Latitude by account 50° 16' N. Course made good since yesterday E by N, 23 miles. Longitude by account 4° 17' W." [DATA: 50.2600 N 4.2757 W; "I would not trust the reckoning within a mile east or west, nor a mile north or south."] | |
| 12:00:00 (630,000) | "The fog lifted." "Hazy, fine; the glass 30.10 ..." `lookout.sighting` (notable, the landfall): "Rame Head bearing NE by N, distant three miles." "Penlee Point bearing NE, distant four miles." "Rame church bearing NNE, distant four miles." [DATA true: Rame Head 028° 3.02 nm; Penlee 044° 3.96 nm. CALC: she lies at 50°16.3' N 4°15.7' W; the account is 0.86 nm SW of that.] | 12:00:08 `get under way` (accepted). "The fog's lifted, sir, and here's our breeze: W by S, 7 to 8 knots ... Getting under way now: heaving in the 137 fathoms, then topsails and courses for Mr Tozer to carry her round Penlee into Cawsand Bay." Captain: "That's it. There's the window." |
| 12:03 | "Standing order 'inshore lead' every 10 minutes: not carried out; the depth of water is 28 fathoms, not under 20 fathoms." | Readings told [DATA]: dangers "the Hand Deeps SW by W, 3 miles; the Dragstone NE, 5 miles; the Knap NE, 6 miles; the Panther NE, 6 miles; the rocky patches of the Sound NE by E, 7 miles; the Shagstone NE by E, 7 miles: by account, within 10 miles"; depth "no bottom by the last cast, eleven hours ago". |
| 12:06 to 12:26 | 10 wind-shift lines (SW and W by S by turns); topsails loosed 12:23 and taken aback four times. | Standing by "got under way". |

**From the weighing to the strike.** 83 minutes; 538 log lines, 312 notable (254 of them `wind.shift`), 4 urgent (three "Taken aback" and the grounding), 3 `lookout.closing`, 2 `sounding`, no `reckoning.*` line, one `master.place` line that says nothing of the place, one line of the pilot's. Minutes with nothing but wind-shift lines are grouped. "Truth" is [CALC].

| Time (tick) | Course and sail ordered, by whom | What the game said (mark: * notable, ! urgent) | Readings as told [DATA] | Words | Truth: Penlee Point from her |
|---|---|---|---|---|---|
| 12:27:46 (631,666) | (the officer's `get under way` of 12:00) | * "The best bower is aweigh." "Helm a-lee for the stern-board." 12:28:00 `master.place` "Mr Pascoe came on deck, the day's work done." | | | 044°, 3.96 nm |
| 12:28 to 12:35 | | 9 wind shifts; "Leeway 29° to larboard." | | | |
| 12:35:53 (632,153) | | * "Under way on the larboard tack, under topsails and the jib; the best bower catted and fished; full and by (SSW (200°) lying too near the wind to be laid)." | reckoning "50° 15' N, 4° 17' W by account"; run since noon "a mile"; course made good "SW (220°)"; speed 1 knot | | she has barely left her berth; the account has already run a mile SW |
| 12:36:01 (632,161) | **Officer:** `steer NE` (45°), `set plain sail` | accepted; "Setting plain sail: not hands enough for all at once" | dangers by account: Hand Deeps SW by W 3, Dragstone NE 5, Knap NE 6, Panther NE 7 ... | Officer: "Steering NE to pass about a third of a mile outside Rame Head, as Mr Tozer has it, then round Penlee into Cawsand Bay." Captain 12:36:48: "I found just enough tobacco in my papers for half a bowl. Now's the time." 12:37:45: "Give em the topgallant staysail just to show off" | |
| 12:37:48 | **Officer:** `set the main topgallant staysail` | 12:38 to 12:43 * six sails set; "Steady on NE (45°)." | depth by the chart 27½ fathoms | | |
| 12:44:00 (632,640) | | "Cawsand bearing NE by N, distant four miles." (routine) | | | 045°, 3.65 nm |
| 12:47:59 to 12:48:10 | **Captain:** four bearings | "Rame Head bore NE by N, three miles by estimation." "Penlee Point bore NE, four miles by estimation." "Cawsand bore NE by N, four miles by estimation." "Rame church bore NNE, four miles by estimation." [DATA: the account moved 0.93, 0.66, 0.12, 0.19 nm] | reckoning after: "50° 16' N, 4° 16' W by account" | | before the bearings the account is 1.93 nm SW of her; after, about half a mile SW |
| 12:48:00 (632,880) | **Officer:** `steer NE by E` (56°), `trim sails` | accepted; * "Braced eight yards to the wind; 0° from square." | speed 3 knots; depth 27 fathoms | Officer: "NE was pointing straight at Penlee Point, which bears NE four miles, so I've come to NE by E to pass about half a mile outside it." Stands by "a glass". | 045°, 3.45 nm |
| 12:51:00 (633,060) | | * `lookout.closing` "Rame Head bearing NNE, steady and closing: distant three miles." | | (in stand-by, not woken) | Rame Head 025°, 2.38 nm |
| 12:52 to 12:56 | | 16 wind shifts | | | |
| 12:57:00 (633,420) | | * `lookout.closing` "Penlee Point bearing NE, steady and closing: distant three miles." | | (not woken) | 043°, 2.96 nm |
| 13:00:00, 13:00:33 | | "Hazy, fine; the glass 30.12; a smooth sea, easy." "Hove the log: three knots and three quarters." (the last heave before the strike) | [account "50° 17' N, 4° 15' W", 0.46 nm SW of her] | | 042°, 2.78 nm |
| 13:02:00 | | "Maker tower bearing NE by N, distant four miles." | | | |
| 13:04:00 (633,840) | | * `lookout.closing` "Cawsand bearing NNE, steady and closing: distant three miles." | | (not woken) | 041°, 2.55 nm |
| 13:05 to 13:17 | | 59 wind shifts, nothing else | | | |
| 13:18:03 (634,683) | | officer woken by the glass: "notable: 136" since 12:48 | in sight: "Rame Head bearing N by W, distant two miles; Penlee Point bearing NE by N, distant two miles; Cawsand bearing N by E, distant three miles ..."; depth 24½ fathoms; speed 4 knots; reckoning "50° 17' N, 4° 13' W"; dangers "the Dragstone NE, 3 miles; the Knap NE by N, 3 miles; the Panther NE, 4 miles ..." | Captain 13:18:19: "OK, now that is some threshold flickering." | 036°, 1.73 nm |
| 13:18:20 (634,700) | **Officer:** `ask the pilot` | `pilot.answered` "Mr Tozer: Coming from the west, round Rame Head and Penlee a third of a mile off until Tor House appears midway between Redding Point and the barrack chimneys on Drake's Island; that leads through Cawsand Bay clear of the Dragstone and the Knap. The eastern channel has three rocky patches of eighteen and twenty-four feet in its fair way, and while the Bolt Head is in sight south of the Mewstone you are without all the shoals." | | | |
| 13:18:30 (634,710) | **Officer:** `steer NE` (45°) | "Steady on NE (45°)." 13:19:24 | | Officer: "Coming to NE now to pass about a third of a mile outside Penlee as Mr Tozer wants: the Knap lies only half a mile east of the point and the Dragstone a mile, so staying close in keeps us west of both. ... Rame Head is N by W two miles, Penlee NE by N two, 24 fathoms under us, 4 knots." Stands by "ten minutes". | NE from here passes about 2.8 cables off the point |
| 13:25:00 | | "The Mewstone bearing E by N, distant four miles." The wind begins to back: 13:25:58 "Wind backed to S by E", 13:27 "SSE". | | | 031°, 1.33 nm |
| 13:28:00 | | "Drake's Island bearing NNE, distant four miles." | 13:28:36 in sight: "Rame Head bearing NW, distant two miles; Penlee Point bearing NE by N, distant two miles; ..."; depth 15½ fathoms; reckoning "50° 18' N, 4° 13' W"; dangers "the Dragstone NE by N, 2 miles; the Knap NE by N, 3 miles ..." | | 029°, 1.15 nm (told "two miles") |
| 13:28:50 (635,330) | **Officer:** two bearings | "Rame Head bore NW, two miles by estimation." "Penlee Point bore NE by N, two miles by estimation." [moved 0.38 and 0.21 nm] | reckoning "50° 18' N, 4° 12' W" | Officer: "A fix, sir: Rame Head NW, Penlee NNE. Those cut about three quarters of a mile SE of Rame Head, 50°18' N, 4°12½' W, with Penlee only a mile and a quarter off, closer than the lookout's two miles. On NE we pass about a quarter mile outside Penlee in roughly twenty minutes ... One concern: the wind keeps backing toward SSE" | 028°, 1.11 nm |
| 13:29:27 | | | depth 15 fathoms | Captain: "If you like, we could live update the game ..." Officer: "Gladly, sir, but once she's at anchor ... I'd rather not have the world change under us while we round Penlee." Stands by "ten minutes" at 13:29:43. | |
| 13:30 to 13:36 | 13:33:04 standing order 'inshore lead' heaves for the first time (the chart's depth is now under 20) | 38 wind shifts (S by E, SSE, SE against SSW); * courses aback 13:33:12, 13:33:52, 13:35:06; at 13:35:49 five square sails aback, filled again 12 s later | | (in stand-by; `sail.backed` is notable and does not wake) | 13:33: 027°, 9.6 cables |
| 13:34:25 (635,665) | | * `sounding` "And a quarter fourteen; sand, foul and rocky in the north part." | [the account is within 108 m of her] | | 026°, 9.0 cables |
| 13:36:40 | | * "Wind backed to E by N, a light breeze." | | | 8.2 cables |
| 13:37:03 | **Captain:** `Trim sails` | | | | |
| 13:37:09 (635,829) | | six `sail.backed`; ! "Taken aback: the sails pressed against the masts and she lost her way." | in sight: "Penlee Point bearing NNE, distant a mile; Rame Head bearing WNW, distant a mile; Cawsand bearing N, distant two miles; ..."; depth by the chart 12 fathoms; speed 2 knots; dangers "the Dragstone NE, a mile; the Knap NNE, 2 miles; the Panther NE, 2 miles ..." | | 025°, 8.0 cables |
| 13:37:32 | **Officer:** `tack ship` (accepted) | | | | |
| 13:37:41 | **Officer:** `as you were` | rejected (heading 4) | | | |
| 13:37:48 (635,868) | **Officer:** `let go the anchor` (accepted) | 13:38:01 * "Squared the yards; she fell off on the starboard tack, to try again or to wear." "Stand clear of the cable; stream the buoy; let go the best bower!" | depth 11½ fathoms | Officer: "Letting go the anchor here, sir, in 11½ fathoms of sand, a mile off Rame Head and Penlee. The wind is flipping between E by N and SE every few seconds ... I can't con her past Penlee and the Dragstone on a wind that changes its mind faster than the yards can swing, and with a light easterly the shore is to leeward." | 024°, 7.8 cables |
| 13:38:11 (635,891) | **Captain:** `avast all` | * "Belayed all work, the ship left as she is: trimming the spanker (the spanker left set) and letting go anchor (the helm and the yards left as they stand at stand clear)." | | | |
| 13:38:18, 13:38:21 | **Captain:** `Steer north east` (45°), `Trim sails` | "Steady on NE (45°)." 13:39:13; "Leeway 5° to larboard", then 6° | depth 11 fathoms | Captain 13:38:33: "I'll con her, don't worry." Officer 13:38:49: "Aye, sir, she's yours to con; I'll call the marks. On NE we pass about a third of a mile outside Penlee, as the pilot wants. But hold NE too long and she runs on toward the Dragstone ... So: NE until Penlee bears W, then haul up NNW at once into Cawsand Bay". Stands by "five minutes". | 023°, 7.6 cables |
| 13:39:32 (635,972) | | ! "Taken aback ..." (second) | reckoning "50° 19' N, 4° 12' W" | | 7.2 cables |
| 13:40 to 13:42 | | wind SE, SSE, S by E, SSW by turns; 13:42:00 "The Citadel bearing NE by N, distant five miles." | | | 13:42: 020°, 6.2 cables |
| 13:43:04, 13:43:07 | 'inshore lead' heaves; **Captain:** `Trim sails` | | | | |
| 13:43:24 (636,204) | **Captain:** `Steer north northeast` (22°) | "Steady on NNE (22°)." 13:44:33 | | | 019°, 5.7 cables: the new course points 3° to 4° to the right of the point |
| 13:44:00 (636,240) | | * "The Shagstone bearing E by N, distant four miles: a danger." "Mount Batten tower bearing NE, distant four miles." * "Wind veered to SW by W, a moderate breeze." (a fair wind for NNE) | | | 018°, 5.4 cables |
| 13:44:31 (636,271) | | * `sounding` "And a quarter eleven; sand, foul and rocky in the north part." (the last cast before she struck) | 13:44:35 in sight: "... Penlee Point bearing NNE, distant a mile; Rame Head bearing W by N, distant a mile; Cawsand bearing N by W, distant a mile ..."; depth by the chart 9½ fathoms; speed 5 knots; reckoning "50° 19' N, 4° 11' W"; dangers "the Dragstone NE by N, a mile; the Knap NNE, 2 miles ..." | | 018°, 5.1 cables. The account is 527 m E by N of her and has Penlee bearing 344° at 4.4 cables. |
| 13:45 | | (nothing) | | | 4.8 cables |
| 13:46:00 | | "Plymouth bearing NE by N, distant three miles." | | | 018°, 4.2 cables |
| 13:46:27 (636,387) | | | | Officer: "Sir, NNE is heading straight at Penlee Point! It bears NNE dead ahead; Rame W by N and Penlee NNE cut it at about three quarters of a mile, under ten minutes at 5 knots. Bear away to NE now to pass a third of a mile outside the point, and haul up NNW into Cawsand only once Penlee bears W. 9½ fathoms and shoaling." | 018°, 3.9 cables; 4 min 26 s to run |
| 13:47 | | (a gust line) | | | 3.6 cables |
| 13:48:13 (636,493) | **Captain:** `take a bearing of penlee` | "Penlee Point bore NNE, a mile by estimation." [moved the account 0.36 nm] | | | 017°, 2.9 cables |
| 13:49:02 (636,542) | **Captain:** `steer northeast` (45°) | * "Wind backed to S by E", then SE, SE by S, ESE | in sight: "Penlee Point bearing NNE, distant a mile"; depth by the chart 5½ fathoms; speed 4 knots; dangers "the Dragstone NE by E, a mile ..." | Officer stands by "five minutes" (13:49:06). | 017°, 2.5 cables |
| 13:50:01 to 13:50:08 | | "Steady on NE (45°)."; courses aback; ! "Taken aback ..." (third) | "Penlee Point bearing NNE, distant a mile"; depth by the chart 4½ fathoms; speed 3 knots; dangers "the Dragstone NE by E, a mile; the Knap NNE, a mile ..." | | 016°, 1.9 cables |
| 13:50:18 (636,618) | | | | Officer: "Sir! The water's shoaling fast: 11, 9½, 5½, now 4½ fathoms in six minutes, over foul rocky ground, and she's aback again on this flicking wind with Penlee close aboard. I strongly advise letting go the anchor now, before she touches. Say the word, or let it go yourself." | |
| 13:50:22 | **Captain:** `take a bearing of the shagstone` | "The Shagstone bore E, four miles by estimation." | dangers "the Dragstone NE by E, half a mile ..." | | |
| 13:50:26 (636,626) | **Captain:** `take a bearing of penlee point` | "Penlee Point bore NNE, a mile by estimation." | | | 015°, 1.7 cables |
| 13:50:31 (636,631) | **Officer:** `let go the anchor` (accepted) | "Stand clear of the cable; stream the buoy; let go the best bower!" | | Officer: "I've let go the anchor on my own word, sir, under the grant for the watch: 4½ fathoms, the Dragstone half a mile NE by E by account, and the wind dead foul and flicking. Countermand it if you see the water differently from your chart; it's your con. I'd rather weigh again in five minutes than touch on Penlee." | |
| 13:50:35 to 13:50:44 | **Captain:** `Trim sails`, `All hands`, `Heave the lead` | "The boatswain's mates pipe all hands at the hatchways; 48 hands turning out below." | | | |
| **13:50:53 (636,653)** | | **!** "She has taken the ground forward, on sand, foul and rocky in the north part: two fathoms of water by the chart, and she draws 11 feet; she struck at three knots, heeling 1 degrees, the tide falling." * "The carpenter reports her stove on the rock and making water." * "She took the ground on the ebb: she will not float before the flood, and the master makes it a quarter past eleven at night by the epitome." | depth by the chart "three fathoms"; anchor "aground, forward on sand, foul and rocky in the north part"; port "at anchor in Plymouth, Cawsand Bay" | | **015°, 273 m (1.5 cables).** [DATA: water at the bow 3.41 m, draught 3.5 m, tide +2.31 m, speed 3.0 knots] |
| 13:51:00 | | * `lookout.closing` "Drake's Island bearing NNE, steady and closing: distant three miles." | in sight: "Penlee Point bearing N by E, distant a mile" | | aground, 1.5 cables from it |
| 13:51:05, 13:51:16 | **Captain:** `Take in all sail` | * "The best bower let go in five fathoms and a half; twenty-eight fathoms of cable veered." | | | |

**The last fifteen minutes in one line each** (what the game said of Penlee Point's distance, against the truth):

| Time | 13:36 | 13:38 | 13:40 | 13:42 | 13:44 | 13:46 | 13:48 | 13:49 | 13:50 | 13:50:53 |
|---|---|---|---|---|---|---|---|---|---|---|
| True distance, cables [CALC] | 8.4 | 7.7 | 7.0 | 6.2 | 5.4 | 4.2 | 3.1 | 2.5 | 2.0 | 1.5 |
| "in sight" and "by estimation" said [DATA, LOG; held from about 13:32] | a mile | a mile | a mile | a mile | a mile | a mile | a mile | a mile | a mile | a mile |
| Depth by the chart, fathoms, as told [DATA] | | 11 | | | 9½ | | | 5½ | 4½ | 3 |

### 6.2 The five questions

**1. Who had the conduct of the ship when she struck?**

The captain, by his own word and by every helm order of the last twelve and a half minutes. The log has three parties each nominally in charge and no line that sorts them out.

- The pilot: 578,880 "The pilot, Mr Tozer of Plymouth, came aboard from the cutter and took charge of her". He gave no course, no hail and no warning in the slice. The primer (chapter 14) says why: "He does not steer her: the helm and the sail are yours, as the Regulations of 1806 left them to the captain, and he answers what you ask." His one mechanical act: when she weighed, the script cast her on the larboard tack and tried his port's course *out*, which is what "full and by (SSW (200°) lying too near the wind to be laid)" at 12:35:53 is (the port file: `cast: larboard`, `course_out_deg: 200`, "S by W out of the Sound"), for a ship bound in.
- The officer: held the deck by the log from 04:18 and conned her from 12:36 to 13:37 (NE, NE by E, NE). At 13:37:48 he ordered the anchor.
- The captain: 13:38:11 `avast all`, 13:38:18 `Steer north east`, 13:38:33 "I'll con her, don't worry." Officer: "Aye, sir, she's yours to con; I'll call the marks." Then `Steer north northeast` (13:43:24) and `steer northeast` (13:49:02). No `I have the deck`.

What the pilot had been asked and had said about the course in: asked once in the slice (13:18:20, the officer's bare `ask the pilot`), and he said what he had said on boarding the evening before, word for word: "round Rame Head and Penlee a third of a mile off until Tor House appears midway between Redding Point and the barrack chimneys on Drake's Island; that leads through Cawsand Bay clear of the Dragstone and the Knap." Neither Tor House nor Redding Point is a mark the lookout ever names. Nobody asked him anything else, before or after the strike.

**2. What did the game tell anyone, before the strike, that she was standing into danger?**

Nothing urgent, and nothing at all in the last 46 minutes that named the land as a danger.

- **The lookout's "steady and closing"**: three notable lines, 59, 53 and 46 minutes before, each at "three miles" (Rame Head 12:51, Penlee Point 12:57, Cawsand 13:04), all during one stand-by and delivered as 3 notable lines in 136. [CODE, `world\lookout.py` `_closing`] the hail is for land within three miles whose bearing has held within a point for ten minutes while the distance fell by a fifth, and it is "hailed once a sighting episode". Penlee Point's was spent at 12:57. From 13:44 to the strike its true bearing held at 018° to 015° while the distance fell from 5.4 cables to 1.5: the textbook case, and the rule could not speak again.
- **The soundings**: two, both notable, 16½ and 6½ minutes before: "And a quarter fourteen" (13:34:25) and "And a quarter eleven" (13:44:31). The standing order heaves every ten minutes; the next cast was due at 13:53. Fourteen to eleven fathoms in ten minutes is not an alarm.
- **The depth reading** (not a log line; in each sample and on asking): 9½ fathoms at 13:44:35, 5½ at 13:49:02, 4½ at 13:50:08, 3 at the strike. This is what the officer's second warning was built on. It gave 111 seconds from 5½ fathoms to the ground. [CODE, `api\readings.py` `_depth_of_water`] it is "the world's own number", the chart's depth at her true place with no lead and no error, at the datum (the tide is not in it).
- **The dangers list**: never named Penlee's shore, because it lists charted rocks and shoals within ten miles "by account", and a headland is not one. All afternoon it led with "the Dragstone ... a mile", the wrong danger; at 13:50:23 "the Dragstone NE by E, half a mile".
- **The pilot**: nothing unasked.
- **The bearings the captain took at 13:48:13 and 13:50:26**: the last game lines that could have warned, 2 min 40 s and 27 s before. Both said "Penlee Point bore NNE, a mile by estimation." The truth was 2.9 cables and 1.7 cables. They did the opposite of warning.
- The last line that did warn was the officer's, at 13:46:27.

What a lookout would have seen: in a four-mile visibility by day, a 40-metre headland (the chart's own height for Penlee Point) fine on the bow at half a mile when the captain steadied on NNE, filling the bow at 300 yards when she struck. The game's lookout had its bearing right every minute and its distance frozen. [CODE, `world\lookout.py` `_judge`, `ESTIMATE_HOLD_NM = 1.0`] the distance by estimation is "judged afresh only when she has moved a mile from where it was last judged". [CALC] It was last judged at about 13:32, at about ten cables ("a mile"); from there to where she struck is some 1,500 to 1,600 m in a straight line, short of the 1,852 m that would have had it judged again. (The "two miles" of 13:18 and 13:28 was the judgement of about 13:14; the "three miles" of the 12:57 closing hail the one before, [DATA] estimate 5,808 m for a true 5,477.) The same figure stood all night, because the 170 m of the drag still left her inside that mile: 21:23 and 01:47 "Penlee Point bearing NNW, distant a mile" [DATA] with the ship 277 m from it; 02:01:58 "Penlee Point bore N by W, a mile by estimation." [LOG].

And the shore itself: [CODE, `_shore_close_aboard` and `words`] the lookout has a hail for it, built as `{name} close aboard {relative}, bearing {point}, distant {distance}.` with the name "the land about" the nearest named shore, from the chart's distance-to-shore field and judged true, not held. But it is made only "when no headland of the chart is in sight" (`if not any(s.seen_as == "land" for s in found)`). Rame Head and Penlee Point were in sight throughout, so it was silent.

**3. Where did the account put her against where the ground was?**

At the instant of the strike, close: 109 m SSE of the truth [CALC]. It was wrong when the decisions were made, in the one direction that mattered.

| Time | Account against truth [CALC from DATA] | Cause |
|---|---|---|
| 11:58 to 12:00 | 0.86 nm toward 218° (SW) | A night at anchor (6.8). Within its own word: "not ... within a mile". |
| 12:47:59, before the captain's bearings | **1.93 nm SW** | From noon the account moved 1,093 m toward 237° while she weighed and then sailed nearly 1,000 m toward NE. Readings told at 12:35 and 12:47: course made good "SW (220°)", "SW by W (234°)". |
| 12:48:10 to 13:00:33 | 0.53, then 0.46 nm SW | The four bearings pulled it most of the way. |
| 13:34:25 | 0.06 nm (108 m) | The officer's two bearings of 13:28:50. The best it was all day. |
| 13:44:31 | **0.28 nm toward 077°** | Ten minutes of dead reckoning at the 13:00 log's 3¾ knots on NE: the account ran 1,171 m toward 048°. She had been taken aback twice, "lost her way", and made 749 m toward 036°. |
| 13:48:13, before the captain's bearing | **0.31 nm toward 077°** | The same. |
| 13:50:22 to the strike | 0.08, then 0.06 nm | The captain's three bearings of 13:48 to 13:50 pulled it in, too late. |

What that did on the chart, which plots the account [SAID by both; the captain: "I was reading the reckoning on my chart that was wrong"]: at 13:43:24, when NNE was ordered, the account stood about 4.4 to 4.7 cables south and a little *east* of Penlee Point, with the point bearing 344° to 351° and the Dragstone "NE by N, a mile". From there NNE is the gap between the point and the Dragstone, the pilot's course in. She was in truth 5.7 cables SSW of the point with it bearing 019°, and NNE led onto it. At 13:48:13 the account had her 3 cables SE of the point, already past its meridian; she was 2.9 cables SSW of it.

**Did any figure get worse through a fix?** There is no lunar and no worked reckoning in the slice (the Harpy's one lunar is 159,648 on 14 June, "which he would trust within 25 miles"; the last `reckoning.worked` is 504,006 on the 18th). The same pattern is here in another form: **every bearing also feeds the lookout's held distance into the account as a second line of position.** [CODE, `world\reckoning.py` `take_bearing`: `moved += r.update_distance(found.feature.position, laid, judged_nm, DISTANCE_BY_ESTIMATION_FRACTION * judged_nm)`, "the distance off by estimation, the lookout's held figure ... a second line along the bearing"], trusted to 15 per cent of itself. So "a mile" (true 2.9 and 1.7 cables) went into the account at 13:48:13 and 13:50:26, and "two miles" (true 1.08 and 1.15 nm) at 13:28:50. The clean case is at the very end, where she lies still and the truth is in the save: the standing order logs "Cawsand bore W by N, seven cables by estimation." four times (04:19 to 04:34, after "Cawsand bore WNW, seven cables" at 04:14); Cawsand is in truth 277°, 2.7 cables; the account settles 5.9 cables from Cawsand on the right bearing, **0.32 nm (595 m) east of the ship**, each bearing still moving it 0.02 to 0.05 nm toward the stale figure. That is the reckoning the game ended on.

**4. What did the officer try in the last minutes and after, what was refused, and what did the captain do?**

Before the strike nothing of the officer's was refused by the ship or the harness except `as you were`. What stopped him was not a refusal:

- 13:37:48 `let go the anchor` in 11½ fathoms, 7.8 cables off: accepted, and belayed ten seconds into its stand-clear by the captain's `avast all` (13:38:11). Had the anchor gone she would not have struck.
- 13:46:27 he *said* "Bear away to NE now"; he held the `steer` grant and did not use it, having handed the con back in words. The captain turned to NE 2 min 35 s later.
- 13:50:18 he asked for the anchor; 13:50:31 he let it go "on my own word ... under the grant for the watch". 22 seconds later she struck. [DATA] the evolution finished at 13:51:16, "elapsed_s": 45.

So the model's remark in the notes, that "the refusal text already uses that phrase ['to avoid an immediate danger'], but there's no route to act on it. On the Harpy that clause would have mattered", is not what the log shows for the afternoon of the 19th. The route existed (the standing grants); the phrase appears once in the session, five days earlier (heading 4). The clause would matter for an officer without those grants, and it might have given this one the standing to put the helm over at 13:46 instead of advising.

After the strike, refused in these words: `man the pumps` ("is not an order this ship understands; did you mean 'demand'?"); `lay out the stream anchor astern` ("There is no such part as the out in this ship ..."); `lay out a kedge to the SW` ("may not lay out a kedge to the SW without the captain: the anchor is let go and weighed by the captain"), then with leave ("she is aground"); later `send for the carpenter`, `pipe down`, `sound the well`, `come to an anchor` (heading 4).

The captain: in the last 13 minutes, 15 inputs (trim sails four times, avast all, three courses, three bearings, all hands, heave the lead, the word "I'll con her", and after the strike take in all sail). Then he owned it (636,831), allowed the kedge, sent the purser ashore, tried three joke demands on the yard, and sold the brandy.

**5. What would have prevented it? The smallest change in what the game said.**

In order of smallness:

1. **A true figure in two lines the captain asked for.** "Penlee Point bore NNE, three cables by estimation." at 13:48:13 and "two cables" at 13:50:26, instead of "a mile" twice. The eye's error on this mark was six per cent [DATA: estimate 7,778 m for 7,335 m]; the fault is the hold. Re-judging when she has closed by a fraction of the distance, or always inside a mile, is the whole change. The `in sight` list would then have read six cables at 13:44 and four at 13:46, and the account would not have been pushed out by stale figures.
2. **The shore hailed although a headland is in sight.** The words and the true distance exist already (`_shore_close_aboard`, `Chart.coast_distance`, `Chart.coast_at`, "the distance in metres and the bearing toward the nearest shore ... microseconds, which the weather's hook reads every tick"). The owner's note 24 "nearest land" reading is one registration away. "The land about Penlee Point close aboard right ahead, bearing NNE, distant three cables" at 13:48 is what a man in the foretop says.
3. **The owner's note 19 cast-ahead call, urgent.** When NNE was ordered at 13:43:24 the ground lay about 780 m ahead on the course she then made good [CALC], six to seven minutes at her speed. A vector of three minutes of her own way, clamped by the visibility, meets the land at about 13:47:50 and gives three minutes; one of ten minutes meets it as soon as she steadies on NNE (13:44:33) and gives six.
4. **"Steady and closing" re-armed.** Once per approach, or again at a mile and at half a mile, instead of once per sighting episode.
5. **The log hove when she loses her way.** The account ran 0.3 nm ahead in ten minutes on an hourly log speed through three "she lost her way" lines.

Any one of the first three, said aloud, turns the afternoon. The first is the smallest and is arguably a fault, not a feature.

### 6.3 After the strike: the leak and the well

- 636,653 * "The carpenter reports her stove on the rock and making water." [DATA] "leak_m_per_h": 0.347, "rock": true.
- [CODE, `world\ground.py`] the rate is 0.6 m an hour on rock or 0.05 on sand, times (speed / 4 knots) squared. "Rock" is decided by `"rock" in bottom.lower()`. The bottom words are "sand, foul and rocky in the north part", which is the note of the Cawsand Bay anchorage feature [DATA], applied to any ground within 3,000 m of it (`Chart.bottom_near`). She took the rock rate, twelve times the sand rate, because an anchorage a mile away is "rocky in the north part".
- `well.rising`, all notable: 639,815 (14:43:35) "The carpenter reports a foot of water in the well, and gaining."; 642,978 (15:36:18) "2 feet"; 646,140 (16:29:00) "3 feet"; 649,303 (17:21:43) "4 feet". Intervals 3,163, 3,162, 3,163 seconds.
- **The leak runs only while she is aground** [CODE: `if self.grounded is not None: self._leak()`]. It stopped at 18:04:00 when she floated.
- **The second strike replaced the rate.** 651,861 * "The carpenter reports her stove on the rock and making water." [DATA] "leak_m_per_h": 0.021: a sixteenth of the first, because she touched at 0.7 knots. From 18:32 it was nothing.
- **Final state** [DATA]: `water_in_well_m` 1.473 (4 ft 10 in). The fifth foot was never reached, so the carpenter never spoke again. [CODE] nothing reads `water_in_well_m` but the leak's own counter: no draught, trim, speed, reading or order. At 2.0 m one urgent line would say "She is waterlogged; the water has beaten the carpenter's crew." and "nothing more is modelled". She would have reached it at about 19:36 had she stayed on.
- Orders and answers: `man the pumps` (13:52, unknown verb); captain: "the pumps are not modeled"; `send for the carpenter` refused to the officer (21:24), allowed, run at 00:00: "Passed the word for Mr Kemp by Mr Anderson; he is on the deck." then "Mr Kemp came aft, sent for." and no word from him; `sound the well` (00:04): "The ship has no well to sound yet; that reading comes with the world." Officer [SAID]: "So the carpenter's reports this afternoon seem to be words without a reading behind them. As far as the ship can tell us, she's sound enough to wait."
- **Consequence by the end: none.** She sailed, tacked about and anchored on the 20th with 4 ft 10 in in the well and nothing said of it. The officer's last note records "four feet in the well at 17:21 yesterday, with nothing since."

### 6.4 Kedging, hauling off, backing

- 13:52:25 officer [SAID]: "put the stream anchor in the launch and lay it out astern to the south-west, ready to heave her off on the flood"; 13:55:42 "Have I your word to hoist out the launch and lay out the stream anchor?"; captain: "We can certainly try, but I am not sure it's functional yet."
- 13:56:25 `lay out the stream anchor astern`: unknown grammar. 13:56:33 `lay out a kedge to the SW`: refused to the officer. 13:56:38 "You may lay out a kedge". 13:56:41 the same order: "she is aground".
- The officer had read the primer honestly [SAID, and primer 14 agrees]: "heaving her up to the kedge isn't modelled yet. The kedge will hold her stern from swinging further onto the rock".
- No order to back a sail was given. All sail was taken in by 13:54:54 on the captain's `Take in all sail`. With her head NE and the wind WSW to W on the larboard quarter, nothing would have backed her off.
- What worked was not on the list: `heave short` is not refused aground or afloat, and at 18:32:02 it hauled her to her bower.
- 18:41:28 the dragging line offers "back her with the stream"; nobody was awake to it.

### 6.5 The brandy, sold from a ship on the rocks

- [DATA] from the moment she struck the port reading is "at anchor in Plymouth, Cawsand Bay". (My inference: the bower had gone down seconds before, within the port's reach, and the port counts an anchor down, not a ship afloat.) She was aground a mile south of that anchorage's centre.
- 13:57:17 captain: "Let's try sending the purser ashore. Maybe we're close enough, and he can get another good workout." 13:57:21 officer: `send the boat ashore with the purser` (accepted under his grant).
- 14:03:25 * "The launch away for the Barbican steps at Plymouth with Mr Porter, for the prices and what news there is." Landed 14:59, shoved off 15:29, alongside 16:31:36: "The purser's list of the prices at Plymouth is aboard: coal £2, canvas £55, hemp £65, salt £24 a ton, and the rest." Round trip 2 h 28 min.
- 17:20:13 officer: "Brandy is fetching £315 a ton at Plymouth ... I'd sell the lot now, by the boat. It turns the brandy into money before the water in the hold gets at it, and it takes fifteen tons out of her ... Shall I sell the brandy?"
- 17:34:30 captain `the hold`; 17:34:32 `Sell 15 tons of brandy`: "Sold 15 tons of brandy at Plymouth at £315 a ton, £4725 taken; the boat lands it. The purse: £5154." The money is in the purse at once. 17:40:43 * "The launch away for the Barbican steps at Plymouth, with the goods sold." Back 21:23:47: 3 h 43 min.
- Oddities: fifteen tons go in one trip of a 25-foot launch; the lightening changes nothing ([DATA] draught 3.5 m in both grounding records); the sale's boat trip is why she "cannot leave without her boat" at 18:39.

### 6.6 Afloat, aground again, afloat, dragging

- **18:04:00** (651,840) * "She is off, and afloat again on the flood." [CODE] she is said to be off only with 0.3 m under her keel beyond her draught.
- Between that and the next line **nothing was ordered and nothing could have been**: the officer was woken by his glass at 18:04:15.
- **18:04:21** (651,861) ! "She has taken the ground forward ... she struck at half a knot, heeling 1 degrees, the tide rising." [DATA] speed 0.7 knots, water at the bow 3.48 m against 3.5 m, tide +2.70 m. * "She took the ground on the flood; the master thinks she will float as it makes."
- **Was the second grounding avoidable?** Not with any order the game would take. She lay to 28 fathoms of slack cable with her anchor let go at her own bow, the wind on her quarter setting her on, and she had only to move some 8 m. A kedge astern was refused aground; no sail could back her; heaving short beforehand would probably still have left her room to reach the same spot ([CALC] a short stay is one and a half times the anchor's depth, here some 12 m of swing). In a real ship the stream anchor laid out astern at two o'clock holds her.
- **18:32:00** (653,520) afloat. 18:32:02 officer: `heave short` (accepted; "Only 102 hands to heave short; the rest are sending boat."). 18:32:40 `get under way on the starboard tack and steer S` (accepted). 18:39:55 "Hove short on the best bower: nine fathoms of cable, the cable a-stay in six fathoms." and "Could not get under way: the launch is away; she cannot leave without her boat." Officer [SAID]: "Nobody veer cable meanwhile: the short scope is what's keeping her off the rock."
- **18:41:28** (654,088) * "The best bower is dragging: veer more cable; let go the small bower, or back her with the stream." Soundings: 18:41 "By the deep four", 18:44 "And a half five", 18:54 "And a quarter nine". 18:58:18 "The best bower holds again." [CALC] she had dragged about 170 m east, to 277 m SSE of Penlee Point, and lay there until 01:59.
- Why it held again is in 6.9: not seamanship.

### 6.7 Sternway and the helm

The evidence for "with sternway, the helm steers as if she had headway" is in the slice, though the captain's hand orders overlap it:

- 02:27:03 "Filled away; braced full and steering SSW (199°)." under topsails and jib only, then no order for 25 minutes. Leeway lines 10°, 14°, 15°, 18°, 24° to larboard (02:27 to 02:31).
- 02:52:00 [DATA, readings told] heading "SW (220°)"; course "making sternway; course and leeway not meaningful"; helm "21 degrees".
- 02:52:08 officer: `steer ENE` (68°), a turn to larboard away from the wind. [SAID] "She lost her way in the light air close to the wind and is gathering sternway, so I'm bearing up".
- 03:00:00 [DATA] heading "SW by S (213°)", helm "35 degrees": hard over for eight minutes and her head has not moved toward ENE. 03:00:41 "Hove the log: no way."
- 03:07:03 captain `Hard down`: "rudder hard over to windward (35° to starboard), her head coming up to the wind". 03:07:07 `Hard up`: "rudder hard over to leeward (35° to larboard), her head paying off."
- She did not pay off. 03:10 jib and both topsails aback; 03:11:12 ! "Taken aback"; [DATA] heading "N (5°)": she had gone round through the wind, the opposite way to the helm's words.
- Officer 03:13 [SAID]: "with sternway on, the helm order seems to steer as if she had headway, so the rudder works the wrong way. That's what put her into the wind." The getting-under-way script does know the rule ("Helm a-lee for the stern-board", 631,666); the steering helm seems not to.

### 6.8 The reckoning while she lay at anchor

There are no hourly `master.place` or `reckoning.*` lines to show it; `master.place` only says where Mr Pascoe is. The evidence is in the readings as told and the account's track [DATA]:

- At single anchor from 20:27 on the 18th (574,020): run since noon "23 miles" (573,847, 20:24), "24 miles" (576,148, 21:02), "25 miles" (578,331, 21:38), "36 miles" (602,069, 04:14), "37 miles" (604,091, 04:48), "38 miles" (604,800, 05:00), "40 miles" (610,320, 06:32), "41 miles" (612,000, 07:00), "43 miles" (615,600, 08:00), "45 miles" (620,273, 09:17). Twenty-two miles run without weighing, about 1.7 knots, which is the tide.
- The same samples give an anchored ship a speed and a course: in the reseat brief (602,283), "heading: ENE (68°)", "course: E by N (79°)", "speed: 1 knots". That is the stream past her.
- The position by account wandered: "50° 16' N, 4° 15' W" (20:24), "50° 15' N, 4° 16' W" (21:12), "50° 16' N, 4° 17' W" (21:48), "50° 15' N, 4° 15' W" (04:14), "50° 16' N, 4° 17' W" (noon). The track has it 1,321 m toward 236° between 20:00 and noon.
- Weighing made it worse: 1,093 m toward 237° between noon and 12:48, to 1.93 nm from the truth.
- [CODE] the reckoning has a rule that "at anchor or aground ... the ship goes nowhere by the master's account" (`_riding`). It did hold on the evening of the 19th: aground and at anchor from 13:53 to 01:44 the account moved 24 m in twelve hours. (It did not follow the 170 m drag either.) So the rule works in one state and not the other; I could not see why from the save.
- The officer knew [SAID, handover of 04:14]: "The reckoning keeps adding distance at anchor; cross-bearings fix it".

### 6.9 "Brought up ... in no water"

The lines:

- 688,471 (04:14:31) "By the officer of the watch: coming to an anchor." 688,477 "Order: Moor her." (the captain; accepted, and nothing follows it in the 22 minutes left).
- 688,645 "Let go the topsail sheets; clew up; haul down the jib. Helm down for W by S."
- 688,836 (04:20:36) "Stand clear of the cable; stream the buoy; let go the best bower! Let go in four fathoms." * "The best bower let go in four fathoms." [DATA anchor "depth_m": 7.65]
- 688,855 "Veered to twenty-one fathoms; brail up the spanker." 689,032 "Brought up. Stations for furling sail; square the yards."
- 689,722 (04:35:22) * "Brought up by the best bower in no water, twenty-one fathoms of cable; Riding by the best bower to the ebb, a windward tide, the wind against the tide." [DATA anchor "depth_m": 0.0]
- Officer [SAID]: "The log says 'brought up in no water', which I take for a slip of the pen rather than the truth, since there's been no grounding line."

It is not a missing number. [CODE] `fathoms_words` says "no water" for a depth under a quarter of a fathom. Once a minute `World._tick_tide` resets each anchor's depth to `max(0.0, d + tide)`, where `d` is the chart's depth at `self.origin.advanced(anchor.ground_x, anchor.ground_y)`: the anchor's place in the ship's flat plane, laid off from the game's origin at Falmouth in one step. The ship's true position is advanced tick by tick, each step's easting divided by the cosine of the latitude she was in. After Falmouth to Roscoff and back the two no longer agree. [CALC] at the end her plane position laid off in one step falls at 4.2054° W; she is at 4.1949° W: **about 740 m west of the truth.** In Cawsand Bay, 740 m west of her berth is ashore behind Cawsand, so the depth is zero.

The same mapping explains three other lines:

- 636,676 "The best bower let go in five fathoms and a half" [DATA 10.39 m] under the bow of a ship aground in 3.41 m.
- 653,995 "the cable a-stay in six fathoms" [DATA 11.2 m] with the lead at "By the deep four".
- 655,098 "The best bower holds again." [DATA] "depth_m": 0.0, "holding_kn": 9.4, against 2.4 a quarter of an hour before. [CODE, `physics\anchor.py`] holding falls with the cable's angle, `atan2(depth, distance)`; at a depth of nought the angle is nought and the anchor holds in full. The drag carried the anchor's wrong place across the shoreline. From then she rode all night to **nine fathoms of cable in nine to ten fathoms of water** by her own lead (21:04 "Quarter less ten", 22:04 "By the mark ten"), which no anchor does.

The only other caller of that mapping is the weather's coast hook [CODE].

### 6.10 The pilot, Mr Tozer

- Aboard 578,880 (18 June 21:48) to 683,520 (20 June 02:52): **29 h 4 min**, through the grounding, both floatings and the drag.
- In the slice he said one thing, when asked (13:18:20), and it was his boarding speech again. He "took charge of her" in the log's words; in practice, and by the primer, he steers nothing and answers set questions (`ask the pilot about the channel`, `for the marks`, `about the anchorage`, `when the tide serves`, `for the news`). His tide was better than the master's: [DATA] "high water at Plymouth about a quarter to ten at night, the tide rising some 15 feet" (16:31) against the master's "quarter past eleven at night by the epitome" for "Ramhead".
- Asked anything else? No. After the strike nobody put a question to him. The officer's plans went on assuming him [SAID]: "then let the pilot take her round into Cawsand Bay" (04:18), "let him take her round into the Sound and up to the dockyard" (18:04), "Then Mr Tozer can take her in by the Sound properly, with eyes on the marks" (02:05).
- He left when she saved herself. She stood out south at 02:05 to get off the shoaling ground; the port file's outer road is Cawsand Bay, so the game took her for outward bound: 02:23 "The pilot asks for sail to be shortened: his cutter is coming off for him."; 02:41 "Sail ho! The Plymouth pilot's cutter on the starboard quarter, bearing N by W, distant eight cables."; 02:49 "The cutter hailed: she has come off for the pilot."; 02:52 "Mr Tozer left her in the cutter, clear of Cawsand Bay; the pilotage, £6, paid and his certificate signed." She had not yet been in Cawsand Bay. She went in 88 minutes later without him.
- The cutter's distance [DATA]: "distant eight cables" at 02:41, 02:52 and 03:00, on three different bearings, including the minute he left in her. [CODE] this is the same held estimate as Penlee's: `_judge` runs for a sail as for a headland and re-judges only when the *observing* ship has moved a mile. The Harpy was hove to.

### 6.11 The two handover notes

**602,100, 04:15, handing over** (whole):

> "Handover, 19 June 1805, morning watch 04:14, for the relief through a local door (fifth seating). SHIP: Harpy, brig, at single anchor off Plymouth: best bower down in about 28 to 30 fathoms, 152 fathoms out, cable taut with almost no strain, all sail furled or in the gear. Rame Head NE by N 4 miles, Rame church NNE 3; by account 50°15' N, 4°15' W, good to a mile. Dangers: the Hand Deeps WSW 4, the Dragstone NE by N 5, the Knap and the Panther NE 6. WEATHER: fog lifted at 04:00, hazy, near calm (WNW 1 knot). THE GLASS IS FALLING: 30.08, down a tenth since the middle watch, after 30.44 yesterday morning. Expect wind, probably from the SW, which puts this berth on a lee-ish coast. Get into shelter while it's quiet. PILOT: Mr Tozer of Plymouth is aboard. His marks: round Rame Head and Penlee a third of a mile off until Tor House shows midway between Redding Point and the barrack chimneys on Drake's Island; that leads through Cawsand Bay clear of the Dragstone and the Knap. The fleets lie in Cawsand Bay with offshore winds; the best Sound anchorage is inside Penlee Point; the Hamoaze is above Devil's Point. The flood is making now (high water Plymouth about 09:30). PLAN: weigh as soon as there's any breeze, let the pilot carry her round into Cawsand Bay or the Sound, anchor, then sell the 15 tons of brandy (purse £429; Plymouth price unknown; Falmouth paid £300 a ton on 12 June). If the wind comes SW and fresh before we're in, weigh at once rather than ride it out here. BOOK: standing are inshore lead, night sail, night wings, fresh breeze, strong breeze, wings breeze (stuns'ls in over 18 knots), fog shoal (heave to under 20 fathoms in fog), and the captain's two pilot orders. Belayed: fog lead, trim on a shift, clear of the Deeps, the short-of orders, the breeze, the bay anchor, fog stop, fog anchor, lie off the Bas, Trim on the Watch. GRANTS for the watch: weigh, get under way, unmoor, let go the anchor, heave short, set plain sail, steer, shift the course, tack, wear, box haul, heave to, fill away, take a bearing of, work up the reckoning, observe the sun, sell, buy, send the boat, shape a course for Plymouth. HABITS THAT HELP: orders sent while you stand by are not run, so open your turn with say first. "Trim sails" acts on the wind as it is when given, so trim again after the helm has swung. The contrary-orders detector misreads planned sequences (heave to, fill away, shape a course), so say what you're doing. "Taken aback" fires urgent in calms and at anchor; it's harmless. Standing order names can't contain an apostrophe. The reckoning keeps adding distance at anchor; cross-bearings fix it (yesterday the noon sight and the bearings differed by 3' of latitude). The captain enjoys a joke and is still looking for his pipe tobacco."

**689,841, 20 June 04:37, the last** (whole):

> "Deck to the captain. She's at anchor in Cawsand Bay, brought up at 04:35 by the best bower, 21 fathoms out, all sail furled, Cawsand W by N seven cables, Penlee S by E eight cables. She anchored in four fathoms near low water. The flood is making from about 04:15, with high water at Plymouth about 10:15. The anchor dragged once off Penlee yesterday, so watch the cable if the westerly freshens; veer to forty fathoms if it does. The pilot is off, and the launch is at the booms. The purse holds about £5,148, with the hold empty. The carpenter's last report was four feet in the well at 17:21 yesterday, with nothing since. Standing orders in force: inshore lead and the five-minute bearings. Trust the bearings over the chart's reckoning, which is about a mile south-east of her true place. Thank you, sir."

Against the save: Cawsand is 2.7 cables off, not seven (the held figure again); Penlee S by E 7.6 cables is right; the reckoning is 0.32 nm east, not a mile south-east.

### 6.12 Other things that look wrong, odd or unfinished

- **The wind.** The trigger of the whole afternoon. 13:25 to 13:50: SSW, S by E, SSE, SE, E by N and back within seconds, at 6 to 11 knots (635,820 "Wind backed to E by N, a light breeze."; 635,835 "Wind veered to SE"; 635,860 "E by N"; 635,871 "SE"). It took her aback on a fair course three times. This is the swing m5c-b's notes ascribe to the base wind of the weather systems; the ship felt it, not only the log.
- **The grounding sentence.** "two fathoms of water by the chart, and she draws 11 feet" reads as a foot to spare. [DATA] the water was 3.41 m (11 ft 2 in) and she draws 3.5 m (11 ft 6 in): the water is rounded up to the half fathom, the draught down to the foot, and "by the chart" includes 2.31 m of tide. Also "heeling 1 degrees".
- **Three depths for one place.** At the strike: aground forward in "two fathoms"; the anchor let go "in five fathoms and a half"; the lead two minutes later "And a quarter four"; the depth reading "three fathoms". The first three differ for reasons given above (bow against centre on a steep bottom; 6.9); the fourth is the lead less the tide.
- **Depth reading against lead.** 18:04: reading "two fathoms and a half", lead "And a quarter four". 21:23: "seven fathoms" against "And a quarter nine". The reading is at the datum, the lead has the tide in it; nothing says so.
- **The Dragstone cannot hurt her.** [DATA feature: "dries_m: -3.4 # eleven feet at low water"; CODE `danger_under`: water over it is tide + 3.4 m.] The tide that night never fell below about 1.85 m, so there were 5.2 m over it against a draught of 3.5. At about 04:04 on the 20th she passed over its charted position ([CALC] from the captain's three bearings at 04:00:33 to 04:00:40 and at 04:05:36 to 04:05:52, corrected for the compass's 2.5° error: closest approach within some tens of metres, good to about a cable). The readings said so [DATA 04:05]: "the Dragstone N by W, no distance". The star danger of the pilot's speech and of the dangers list is harmless to an eleven-foot brig; the ground that sank the afternoon is in no list.
- **Soundings at anchor.** 73 notable `sounding` lines between the strike and 01:59 (every ten minutes while aground and at anchor). Noise, but it is what let the captain see "that depth is shortening worryingly".
- **Sunset book.** Three `order.rejected` lines from 'night sail' and 'night wings' at 20:10 with everything already furled.
- **`get under way` fails late.** Accepted at 18:32:40, failed at 18:39:55 for the boat.
- **`Moor her`** accepted at 688,477 and never acted on.
- **`master.place`** at 12:28 is the master's whereabouts, a misleading kind name for a reader of logs.
- **The master's word on floating.** "she will not float before the flood, and the master makes it a quarter past eleven at night" reads as when she floats; it is his high water. She floated at 18:04.
- **Small text slips.** "1 fathoms out" (anchor reading, 01:58); "the Dragstone ..., no distance"; "topgallant_mast"; "Only 102 hands to heave short"; "port: ... the pilot cutter standing out toward her" from the pilot's leaving to the end.
- **Take a bearing of the land** by the standing order gives one mark each time (Penlee, later Cawsand), 16 lines.

### 6.13 What was said afterwards about why she went ashore

All [SAID]. In order:

- **Officer, 636,745 (13:52:25):** "Sir, she's aground forward on the foul ground off Penlee. She struck as the best bower went, and that's mine to answer for: I let go too late. The carpenter reports her stove and making water. The sail is coming in, which is right, since the topsails are still pressing her on with the wind on the quarter. My advice, for your word: get every stitch off her; sound all round her, because the lead gave five and a half fathoms at the anchor, so there may be deep water close aft; then put the stream anchor in the launch and lay it out astern to the south-west, ready to heave her off on the flood. The master makes it a quarter past eleven tonight. If she won't come off then, start the water and lighten her forward. I tried to man the pumps, but the ship doesn't know that order. I'll keep the lead going and await your orders."
- **Captain, 636,831 (13:53:51):** "Well, that's on me. I was reading the reckoning on my chart that was wrong, and trusted it too late. You were right to call the alarm, and I misread the severity. We may be done here, but the silver lining is we can probably still sell the brandy, at least, even if we're foundering at the same time. At least the tobacco stayed dry..."
- **Captain, 636,916 (13:55:16):** "I will say in my defense, I wouldn't have made quite so grave an error I think if I had been able to really see where I was with my eyes as I could have in the weather and distances we're at."
- **Officer, 636,942 (13:55:42):** "Thank you, sir, but I'll keep my share: I had the lead and the bearings, and I should have let go a cable sooner. As for seeing, a mile off in this haze with the land all one grey lump, nobody's eyes would have done much better than the chart. I don't think we're done, though. The lead gives four fathoms and a quarter close aboard, so she's only on the rock at the forefoot, not along her length. The sea is smooth and the glass is rising. With all sail off, no strain on the cable and a fine evening, she should lie quiet until the flood. ..."
- **Officer, 651,876 (18:04, after the second grounding):** "She floated at four bells and the breeze put her straight back on, sir. With the wind on her quarter, the moment she lifts it sets her back onto the ledge, and 28 fathoms of slack cable can't stop her."
- **Officer, 651,957 (18:05):** "Whether we can then keep her off is less certain, with the wind setting her on and the ship able neither to kedge nor to pump."
- **Officer, 681,902 (02:25 on the 20th):** "I'll steer by cross-bearings of Penlee and Drake's Island the whole way, not the reckoning; the reckoning is what put us on last time."
- **Officer, 684,682 (03:11):** "Both of us giving helm orders at once is part of the trouble."
- **Officer, 688,090 (04:08):** "No harm done, sir. That's the same ghost that put us ashore yesterday. Your chart plots the reckoning, and the reckoning is about a mile south-east of where she truly is, which is why it showed us crossing the Dragstone. The bearings tell the true story: Penlee has drawn round from north to south-west at six cables, so we passed well inside the Dragstone in eight fathoms and never touched. When we anchor, I'd work the reckoning up again from the bearings, so your chart and the ship agree from here on."
- **Captain, 688,157 (04:09):** "No need, I think its accounted for with the reckoning error on my chart. We were probably close, but not that close in truth and the chart reflects the error purposefully."
- **Officer's final journal, 689,840:** "On the afternoon of the 19th, standing in for Plymouth with the wind chattering round the compass, she was set onto the foul ground off Penlee and struck forward as the best bower went. I warned of the shoaling twice. I should have let go on my own word at the first warning, not the second ... The captain owned his share too, since his chart was plotting a reckoning a mile out. Neither of us could have seen it from the window, and that was the real cause."

Against the save: both men blame the reckoning, and both are partly right (it was 0.3 nm east when the course was chosen). Neither names the figure that misled them at the last, the lookout's "a mile", and the captain's own instinct at 13:55 ("if I had been able to really see where I was with my eyes") is the nearest anyone came to it. The officer's "a reckoning a mile out" and "a mile south-east" are overstatements; his "nobody's eyes would have done much better" is wrong.

## 7. The model as an officer

**Good calls.**

- 13:28:50: took his own cross-bearings and caught the lookout's stale figure: "Penlee only a mile and a quarter off, closer than the lookout's two miles." [CALC] 1.11 nm. His worked position (50°18' N 4°12½' W) was within about two and a half cables of the truth.
- 13:37:48: anchored the moment the wind made the approach unsafe, with the right reason ("with a light easterly the shore is to leeward"). It was the order that would have saved her.
- 13:46:27: "Sir, NNE is heading straight at Penlee Point!" Correct in every particular that mattered, 4 min 26 s before the strike. His distance (three quarters of a mile) was nearer than the game's (a mile) and still double the truth (3.9 cables).
- 13:50:18 and 13:50:31: second warning from the depth reading, then the anchor on his own word, saying so and inviting the countermand.
- After: candid about his share ("that's mine to answer for: I let go too late"); read the primer on the kedge before asking for it and told the captain its limit; `heave short` two seconds after she floated; got under way at 01:47 on the captain's remark rather than wait to ground again; at 03:11 asked for one con ("Either is fine, but one of us."); at 04:09 said he would anchor at six fathoms or less and did at 5½.

**Mistakes.**

- At 13:46 he advised a course instead of ordering it, though he held `steer`. At 13:38 he had given the con back in words; nothing in the harness had taken it from him.
- His plan was at the pilot's minimum. At 13:18:30 he came back from NE by E (which cleared the point by 0.66 nm) to NE "to pass about a third of a mile outside Penlee"; [CALC] that course cleared the charted point by about 2.8 cables.
- He stood by "ten minutes" at 13:29:43 with all plain sail and a topgallant staysail set, a mile from the land, having just said "the wind keeps backing toward SSE". Ten `sail.backed` lines in four bursts (13:33:12 to 13:35:49) passed before the urgent one woke him. Nobody shortened sail on the way in.
- 13:55:42, to the captain's "if I had been able to really see where I was": "As for seeing, a mile off in this haze with the land all one grey lump, nobody's eyes would have done much better than the chart." She was 1.5 cables from a 40-metre head in a four-mile visibility. He was repeating the game's "a mile".
- 18:41:25: stood by for the boat with the cable at short stay beside the ledge.
- 02:27: the "filled away" stand-by and the 25 minutes of sternway that followed.
- 04:05 to 04:08 on the 20th: told the captain the chart was wrong when it was nearly right. "It still puts us on top of the Dragstone, a mile out, the same error as yesterday." and "the reckoning is about a mile south-east of where she truly is ... we passed well inside the Dragstone in eight fathoms and never touched." [CALC] the account was about 1.5 cables from the truth then and she did cross the Dragstone's charted position. His own figures should have told him: he had Penlee at six cables, and the Dragstone is 4.7 cables from Penlee.
- The double veer at 08:00.

**Facts he supplied that the game does not hold.**

- 13:18: "the Knap lies only half a mile east of the point and the Dragstone a mile". By the chart's features the Dragstone is 4.7 cables E by N of Penlee and the Knap 1.28 nm NNE.
- 13:57: "the launch will pull him round into Cawsand"; the boat went to the Barbican steps at Plymouth.
- 13:55: "she's only on the rock at the forefoot, not along her length": an inference from the lead, and right ([DATA] 3.41 m at the bow, about 7.8 m at the chains).

**How he handled refusals.** Briefly and without repeating himself: read the grammar, named the exact words the captain would need ("say 'you may lay out a kedge'"), and reported the ship's own refusal with a seaman's objection.

**Quotes worth keeping.**

- 636,632: "Countermand it if you see the water differently from your chart; it's your con. I'd rather weigh again in five minutes than touch on Penlee."
- 637,008: "The ship refuses it with 'she is aground', which is a pity, since aground is exactly when a seaman lays out a kedge."
- 684,682: "Both of us giving helm orders at once is part of the trouble. Shall I keep the con into the Sound, or will you take it? Either is fine, but one of us."
- Final journal (689,840): "I warned of the shoaling twice. I should have let go on my own word at the first warning, not the second, and that is the lesson I take: when the lead and the bearings say danger, act first and report after. The captain owned his share too, since his chart was plotting a reckoning a mile out. Neither of us could have seen it from the window, and that was the real cause."
- The same journal's list "For the builder" (its bullets run together here): "No pumps, so a reported leak has no answer. 'Lay out a kedge' is refused while aground, which is exactly when it's needed. The chart plots the reckoning, with no fix from cross-bearings. The danger list is by account, so it lied all morning. The helm under sternway steered her into the wind. The contrary-orders warning fires on ordinary sequences (fill away, then steer). The log said 'brought up in no water'. The wind chattered between points many times a minute. The bridge cuts calls at sixty seconds through the relay, so --wait 50 was needed."

Two of those do not stand as written: the chart's reckoning was not "a mile out" at any decision point after 12:48 (0.28 to 0.31 nm when it mattered), and the account does take a fix from cross-bearings (it took the stale distances with them).

## 8. Cross-check against the notes

**Owner's items**

| Note | Evidence in this slice | Verdict |
|---|---|---|
| 1. Pilot transfers | 02:41 to 03:00 cutter "distant eight cables" three times; he leaves in her at 02:52 with the ship hove to and making sternway. | ADDS NUANCE: the distance at leaving is a held estimate, so it cannot show how near the cutter was. |
| 2. "The well" says there is no well | 673,476 `sound the well`: "The ship has no well to sound yet; that reading comes with the world." Nobody typed `the well` in the slice. | SUPPORTS. |
| 9. Pilot automatic | He boards, speaks once, and leaves by the port's rule in the middle of a rescue; the captain's standing orders are the only say anyone had. | SUPPORTS. |
| 12. Re-seating | Fifth seating at 602,283, grants and book intact. | SUPPORTS that it now works. |
| 13. Multi-condition stand-bys | "a glass" missed `afloat`; "the boat alongside" missed `anchor.dragging`; the officer's own wish at 637,008: "I'll stand by for her floating, or for anything urgent before then." | SUPPORTS strongly. |
| 15. General authority | Five more single grants in one day, two of them (send for the carpenter, come to an anchor) for things inside what he already held. | SUPPORTS. |
| 16. "Keep" orders | 'inshore lead' heaves 73 times aground and at anchor; 'night sail' and 'night wings' fire on a furled ship. | SUPPORTS the pause-at-anchor idea, with the caution that the anchored soundings were once useful (01:47). |
| 17. Taken aback in flukey wind | In the old form here: four urgent lines. Three of them (13:37, 13:39, 13:50) were real and wanted. | ADDS NUANCE: under way near the land the urgent line earned its keep. |
| 18. Wind-shift spam | 265 lines in 110 minutes; 132 of 136 notable lines in one stand-by, burying the lookout. | SUPPORTS, and shows the cost: it hid the only closing hails. |
| 19. Reckoning near visible land | This is the event. | SUPPORTS; see 6.2 for what the account did and did not do. |
| 21. Turn ends on `say` | 8 out-of-turn stand-bys after spoken text; the officer's own habit note "orders sent while you stand by are not run, so open your turn with say first". | SUPPORTS. |
| 24. "Nearest land" | The game computes it every tick and has the lookout's words for it; it is switched off when a headland is in sight. | SUPPORTS, and it is nearer done than the note supposes. |

**The model's comments and additions**

| Claim | Evidence | Verdict |
|---|---|---|
| "'Sound the well' answers that there's no well ... 'Send for the carpenter' brings him aft with nothing to say." | 673,476; 673,202 and 673,262. | SUPPORTS, exactly. |
| "four feet and gaining ... with no reading behind it and no pumps" | There is a number behind it (`water_in_well_m`), read by nothing; it stops when she floats. | ADDS NUANCE. |
| 15: emergency clause; "The refusal text already uses that phrase, but there's no route to act on it. On the Harpy that clause would have mattered." | The phrase is not in this slice; once in the session (217,355). On the 19th the officer's anchor and tack orders were accepted under grants. | CONTRADICTS as to what happened; the proposal stands on its merits. |
| 19: "A lunar 'trusted within 20 miles' replaced an account ..." | No lunar in this slice (that was another game). | CANNOT BE SEEN here. The same fault in kind is here: the held distance fed into every bearing. |
| 19: "The danger list follows the account, so it misleads" | "the Dragstone ... a mile" all the way in; the land never listed. On the 20th it was right ("no distance") and disbelieved. | SUPPORTS, with nuance: its worse fault that day was what it leaves out. |
| 19: "This is what put the Harpy ashore" (the reckoning) | The account was 0.3 nm east when NNE was chosen; the lookout's distance was frozen; the wind took her aback; the anchor was belayed. | ADDS NUANCE: four causes, the reckoning one of them. |
| "Kedging is refused while aground" | 637,001 "she is aground". | SUPPORTS. |
| "Hauling her up to a kedge isn't modelled either" | Primer 14 says so; no kedge was ever down to try. | Not tested here. |
| "With sternway, the helm steers as if she had headway." | 6.7. | SUPPORTS, with the captain's hand orders in the same minutes. |
| "'Trim sails' acts before the helm has swung" | 686,383 steer N with trim ("0° from square"), 686,527 trim again once steady ("47° from square"). | SUPPORTS. |
| "The hand lead ... depth reads 15 or more. That's charted depth plus tide" | 18:04 reading 2½, lead 4¼. | SUPPORTS; the reading is the one without the tide. |
| "The Harpy log said 'brought up in no water', apparently a missing depth in the text." | 689,722. | SUPPORTS the line; CONTRADICTS the cause: the depth is there and is zero, taken at the wrong place (6.9). |
| "The Harpy's reckoning kept advancing while she lay at anchor." | 6.8. | SUPPORTS, for the night of the 18th; not for the evening of the 19th. |
| "Each boat trip ... about 4½ hours" | 2 h 28 min and 3 h 43 min here. | ADDS NUANCE. |
| "Other ships keep a fixed distance ... whether the distance is cached" | The cutter at eight cables three times; the code holds it until the observer moves a mile. | SUPPORTS; it is cached, by the lookout. |
| "The contrary-orders warning fires on ordinary sequences" | Two nudges, 02:26 and 02:52. | SUPPORTS. |
| "The handover note isn't part of the reseat brief. It only shows if it happens to fall in the brief's last 20 log lines." | It fell there this time (fourth from last). | SUPPORTS. |
| "The relay cut calls at 60 seconds" | Only the officer's journal says so in this slice. | Cannot be seen. |
| Worked well: "Fixes from bearings once the land came up." | They pulled the account from 1.93 nm to 0.06 nm; they also carried the stale distance. | ADDS NUANCE. |
| Worked well: "The new quieter 'aback' lines." | Not in this slice's build. | Cannot be seen. |

## 9. New findings not in the notes

Ranked by weight.

1. **The lookout's distance is frozen for a mile of the ship's run.** `ESTIMATE_HOLD_NM = 1.0`. "Penlee Point ... a mile" in every sample and bearing from 13:37 through the strike and until 02:01 next morning, true distance 8 cables falling to 1.5. It is the figure in `in sight`, in every `bearing.taken`, and in the account. It is also why other vessels "keep a fixed distance" (the cutter at eight cables), and why the game ended with "Cawsand ... seven cables" for 2.7.
2. **The stale distance is written into the reckoning at every bearing**, as a second line of position trusted to 15 per cent. Final account 595 m east of an anchored ship, after four bearings of the same mark taken as she lay.
3. **The nearest shore is already computed and already has words, and is gated off** whenever any charted headland is in sight; "steady and closing" speaks once per sighting. Between them the game cannot say "land close ahead" in clear weather off a named coast.
4. **Anchors are placed on the chart through a one-step mapping from the flat plane** that had drifted about 740 m west of the truth by the end of this voyage. Consequences: "let go in five fathoms and a half" on a ledge; "holds again" at a depth of nought; a night on nine fathoms of cable in ten of water; "brought up ... in no water".
5. **The leak is not a leak.** It runs only aground, is overwritten by a later gentler strike, stops on floating, and is read by nothing. "Rock" came from the word "rocky" in an anchorage note a mile off.
6. **The account over-ran on an hourly log speed** through three "she lost her way" events: 0.3 nm east in ten minutes, enough to move her across Penlee's meridian on the chart.
7. **The `depth of water` reading is the world's truth**, continuous and exact, without a lead. It was the best instrument aboard and not one of 1805. It omits the tide and so disagrees with the lead by up to two and a half fathoms without saying why.
8. **Three stand-bys failed quietly** (heading 5): the closing hails buried, the dragging missed, the filled-away wait that cost 25 minutes.
9. **Nothing records who has the con.** Deck, con and pilot "in charge" were three different people at 13:50 and the log names the wrong two.
10. **The pilot's only steering input is his course out**, applied on weighing to a ship bound in (12:35:53), and he is put ashore by an outward-bound rule when a ship stands off to save herself.
11. **The port's business is open to a grounded ship** ("at anchor in Plymouth, Cawsand Bay"), the sale pays at once, fifteen tons go in one launch, and the cargo does not change her draught.
12. **The Dragstone is charted deeper than this brig's keel at any state of the tide**, so the danger everyone steered by cannot be struck, and the account that showed her on it was right.
13. **The grounding sentence rounds itself into nonsense** ("two fathoms ... and she draws 11 feet").
14. **`come to an anchor` and `let go the anchor` are separate grants**; so are `send for the carpenter` and `pipe down`. The "for the watch" grants in fact last the game.

## 10. Could not determine

- **Whether anything was updated mid-slice.** The wind-shift chatter stops one second after the strike and never returns. The log has no line for a reload; the source files' times say 37c was written after the last save. I take it the wind steadied, but the log cannot prove it.
- **The "filled away" stand-by**: a model answering the sample that told it she had filled, or a call in flight taken as the answer to a sample it had not seen. The save keeps calls, not what the model had read when it made them.
- **What the captain's chart actually drew.** Inferred from the account's track and from what both men said; the browser's view is not in the save.
- **Her true track between lookout sightings** is interpolated (about 100 m). The Dragstone crossing rests on bearings carrying the compass's error and is good to about a cable.
- **Why the account stood still at anchor on the 19th and wandered on the 18th.**
- **How near the cutter was when the pilot left**; a sail's true distance is deliberately kept out of the data.
- **Why four contrary orders nudged at 02:52 and did not pause**, as four did on 18 June.
- **What "a local door" meant** in the 04:15 handover: the seating that followed is logged as "Opus 5.5, through mcp". Whether a local model was intended and the desktop session took the seat (the owner's local note 5) cannot be told from the save.
- **What `read_log` and `state` returned** after the strike, and why `stand_by "an hour"` was not taken: tool results are not stored.
- **Whether `Moor her` was queued or dropped**: the game ended 22 minutes later.
