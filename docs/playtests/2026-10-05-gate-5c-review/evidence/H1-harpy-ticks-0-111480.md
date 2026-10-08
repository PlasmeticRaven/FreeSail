# H1 - *Harpy* (session 2-harpy-brig-opus), ticks 0 to 111,480

Reader's conventions. "LOG" means a line of the ship's log (fact). "OFFICER SAID" / "CAPTAIN SAID" means words of the model or the owner (claim or opinion); what the model read in its `readings` is not stored in a save, so anything it says it read is a claim. Times are ship's time; a tick is one second from 05:00:00 on 12 June 1805.

## 1. Slice identity

- Session `2-harpy-brig-opus`, ticks 0 to 111,480: 12 June 1805 05:00 (morning watch, 2 bells) to 13 June 11:58 (the noon line). 1,375 log events in the slice, 276 notable, **0 urgent**. 161 transcript entries by the officer.
- Ship: scenario "A merchant brig, free" (`data/ships/brig.yaml`, seed 7), American colours; her officer's journal calls her the *Harpy*. Captain Bowen is the owner; Mr Pascoe master, Mr Porter purser.
- Station: officer of the watch "in the place of Mr Pearce", rank lieutenant, **Opus 5.5 through the MCP door (Claude Desktop), first seating**. Transcript header: policy `every_s 1800, events notable+urgent`, `patience_s 3600`, `stand_by_ends_turn: True`, `budget_tokens: None`, `station.drill: true`; the door note says a `say` or `stand_by` call "is held open until your next turn ... for up to 50 seconds".
- Build: **m5c as cut** (the old instant-wind `wind.shift` line and the old urgent `ship.aback` rule).
- Inside this one seating the Claude Desktop conversation died and a **new conversation** took over at about tick 50,860 to 50,908 (12 June 19:07 to 19:08). The harness logged no door event for it.

## 2. What happened

| Tick | Ship's time | Event |
|---|---|---|
| 0 | 12 Jun 05:00 | LOG `world.start` "Wind W by S, 12 knots ... Heading S by W (190°)"; captain `let go the best bower`; officer stationed and reports "ready to take the deck at your word". |
| 63 | 05:01 | LOG "The best bower let go in ten fathoms; forty-eight fathoms of cable veered." |
| 65-378 | 05:01-05:06 | Officer stands by "until the deck given"; on the captain's welcome (249) warns she has swung over "only three fathoms" by the chart; looks up `library(find "heave in the cable")`. |
| 389 | 05:06 | "Mr Pearce, you have the deck." 402 `heave short` refused; 407 allowed; 409 ordered (all hands; hove short at 989, 05:16, "fifteen fathoms of cable"). |
| 411-440 | 05:06-05:07 | Reads the library index, primer 14, primer 14 section 5, the papers, the readings; journals; proposes tin to Roscoff and brandy home. |
| 525-562 | 05:08-05:09 | `send the boat ashore with the purser` refused, allowed, ordered; captain pre-grants `buy`, `weigh`, `make sail`. |
| 1337-6141 | 05:22-06:42 | First boat trip (prices). |
| 6143 | 06:42 | `buy seven tons of tin`: "£840 paid ... The purse: £160." Harness nudge (3 "contrary orders"). |
| 6491-14337 | 06:48-08:58 | Second boat trip (the goods); tin struck down 08:58. |
| 14348-14368 | 08:59 | `get under way` refused although `weigh` was allowed; allowed; ordered; second nudge (4 "contrary orders"). |
| 14402-14590 | 09:00-09:03 | Captain allows course and steer; asks what a general grant should be called; officer enters four standing orders (a fifth name refused for its apostrophe). |
| 15017-15416 | 09:10-09:16 | Aweigh; pilot cutter sighted (15120); "Under way on the starboard tack, under topsails and the jib". |
| 15426-15663 | 09:17-09:21 | `steer south`; `hail the pilot` not understood; cast "And a quarter three; mud"; officer asks leave to tack; "Black Rock ... steady and closing" (15540); bearing refused to the officer; captain takes bearings himself; tack allowed, then refused by the ship ("1.6 kn through the water"); courses and fore topmast staysail set. |
| 15790 | 09:23 | OFFICER: water deepening, "I'll not tack after all". |
| 15900-16020 | 09:25-09:27 | Cutter hails; two minutes later "The pilot, Mr Tregenza of Falmouth, came aboard from the cutter and took charge of her". |
| 16048-16830 | 09:27-09:40 | S by E, then SSE with the Black Rock "abeam to starboard, two cables" (officer), SE by S for the Old Wall, topgallants set. Captain writes the standing order "the pilot put off" at the third try (16693). |
| 17640-18540 | 09:54-10:09 | Pilot asks to be put off; hove to by the captain's standing order; pilot leaves, "the pilotage, £5, paid". |
| 18542-18617 | 10:09-10:10 | `fill away` refused, allowed (with `wear ship`, `heave to`); SSE for Roscoff, courses and fore topgallant reset. |
| 20100-25612 | 10:35-12:06 | Strange sail; officer stands by "until a stranger's colours made out" for 81 minutes until the captain speaks. Noon: "Latitude by observation 49° 57' N; the reckoning was 49° 58' N." |
| 25616-27688 | 12:06-12:41 | Royals and flying jib; standing orders "lie off the Bas" and "night sail"; belay/resume test; CAPTAIN "This is really wonderful. Are you enjoying yourself so far?" |
| 28802-40648 | 13:00-16:17 | Stand-by "until sunset"; thunder, showers, three small squalls; officer ends the stand-by "at its own word" to report a sail. |
| 40740-50701 | 16:19-19:05 | A brig at three miles; captain tells the officer "Sail ho!"; `hoist our colours` not understood; stand-by "until a bearing steady and closing" for 2 h 33 min until the captain speaks. |
| 50755 | 19:05 | Officer belays "night sail" on the captain's hint. Last act of the first conversation (50758). |
| 50860-51042 | 19:07-19:10 | Conversation reset. New conversation calls `state`, `readings`, `library` x2, `read_log(notable, since 0)`, `journal`; proposes a standing order that already exists; dates the year 1806. |
| 51149-51798 | 19:12-19:23 | Officer cannot read its own journal; four captain attempts; `show the officer of the watchs journal` puts 46 entries in the log; officer corrects the year. |
| 51881-54401 | 19:24-20:06 | Captain below. Sunset 20:03. Officer stands by "until hove to". |
| 54401-74849 | 20:06-01:47 | 5 h 41 min with no sample. Wind veers W to NW and dies; "trim on a shift" fires six times; log 4 knots falling to 2. |
| 74801-75603 | 13 Jun 01:46-02:00 | Captain on deck; officer reports the readings list him "below, asleep"; talk of a sleep system; stand-by "until sunrise". |
| 82318-85357 | 03:51-04:42 | Sunrise; studdingsail booms out and all studdingsails set; spanker trial; stand-by "until a landfall". |
| 97200 | 08:00 | "Fog came down." Nothing wakes the officer. |
| 97797-98493 | 08:09-08:21 | CAPTAIN "Fogged in."; officer enters "fog lead" and "fog stop"; first "No bottom at twenty fathoms". |
| 101954-102767 | 09:19-09:32 | Captain suggests taking in the stuns'ls; officer does, then heaves to on his own judgement (102690), belays "trim on a shift", stands by "until a change in the sky". |
| 102794-103935 | 09:33-09:52 | Captain heaves the deep-sea lead: "Forty-nine fathoms; fine grey sand with black specks." |
| 104432-111480 | 10:00-11:58 | Lying to in fog, "Hove the log: no way" twice, the lead every ten minutes. "Noon. No sight ... Latitude by account 48° 47' N ... Longitude by account 4° 13' W." |

## 3. The deck and the captain's words

**The deck.** Given at tick 389 (05:06): LOG "Mr Pearce, you have the deck. The officer of the watch has the deck; the captain's standing orders are his night orders." Not taken back in the slice. Captain below 51881 (19:24) "The captain went below to his cabin; the deck is the officer of the watch's"; on deck again 74801 (01:46).

**Before the deck** the officer gave no order. It reported (tick 0), stood by "until the deck given" (65), raised the shoal ("That's yours to order", 261) and looked up the order's words (370).

**Every `you may` allowance (13 in five hours, all between 05:06 and 10:09 on 12 June).**

| # | Tick, time | Captain typed | LOG said he "may ..." | Why it was needed | Used in the slice? |
|---|---|---|---|---|---|
| 1 | 407, 05:06 | You may heave short | heave short | refusal at 402 | yes, 409 |
| 2 | 529, 05:08 | You may send the boat ashore | send the boat | refusal at 525 | yes, 532 |
| 3 | 550, 05:09 | You may buy | buy | pre-emptive (officer: "I'll ask leave to buy the tin", 536) | yes, 6143 |
| 4 | 553, 05:09 | You may weigh | weigh | pre-emptive | never; it did **not** cover `get under way` (14348) |
| 5 | 562, 05:09 | You may make sail | **set plain sail** | pre-emptive | no; single sails were already in his domain |
| 6 | 14366, 08:59 | You may get under way | get under way | refusal at 14348 | yes, 14368 |
| 7 | 14402, 09:00 | You may change the course | **shift (the course)** | officer: "Changing the course will also be yours to allow" (14358) | unclear what it opened |
| 8 | 14407, 09:00 | You may steer | steer | pre-emptive, 5 s after no. 7 | yes: 15426, 16048, 16518, 16725, 18611 |
| 9 | 15561, 09:19 | You may take a bearing | **take a bearing of** | refusal at 15559 | no; the officer never tried again |
| 10 | 15637, 09:20 | You may tack ship | tack ship | officer asked leave (15514) | tried once (15650), refused by the ship; never tacked |
| 11 | 18553, 10:09 | you may fill away | fill away | refusal at 18542 | yes, 18557 |
| 12 | 18566, 10:09 | you may wear ship | wear ship | officer asked (18545) | no |
| 13 | 18569, 10:09 | you may heave to | heave to | pre-emptive | yes: let "lie off the Bas" (27578) and "fog stop" (97815) be entered, and the officer's own `heave to` at 102690 |

Each line ends "by the captain's word for the watch", yet the allowances lasted across seven changes of the watch (no. 13 was used 23 hours later). Four further attempts to allow were rejected: `You may hail the pilot` (15434), `You may pilot` (15442), `You may show the officer's journal` (51568), `you may show the officers journal` (51578). The five pre-emptive grants given while the officer was standing by each woke it for nothing (563, 14403, 14408, 18567, 18570).

**The captain's words that carry intent, design thinking or feedback.**

- 249 (05:04): "I intend to let you lead the way here ... if you run in to any order refusals due to authority I'll look and allow them generally ... I'm not entirely sure myself how the pilotage procedure will function here".
- 367 (05:06): "if you try an order outside your technical authority (like a course change, or perhaps anchor orders?) then I can allow it generally. I haven't tested that yet".
- 523 (05:08): "Consider her yours for this voyage, I'll be onboard to ensure she stays safe".
- 1066 (05:17): the 1x feature, "which brings it to 1x every time you sample or speak".
- 14504 (09:01): "I'm putting it in my notes to add a feature that gives general authority, what would it be properly? \"You may have my authority\"?" OFFICER (14513): "'You have charge of the ship, Mr Pearce' ... I'd keep two things out of a general grant even so: belaying the captain's own standing orders, and anything that can't be undone, like cutting a cable or opening fire."
- 14576 (09:02): "you may give standing orders yourself ... I don't know if you could give a standing order outside your default authority, untested."
- 15502 (09:18): "The pilot mechanics are still a mystery to me, too".
- 15654 (09:20), on the tack: "Good luck, I wouldn't choose it here, but I'm curious how shes comes through."
- 16019 (09:26), **misaddressed to "the watcher" and lost**: "It appears the pilot system is a bit semi-automated right now, that'll go in the notes ... Up to you, I say ... Might be worth waiting for the pilot in on our next stop." One second later the pilot was aboard; 16040: "Pilot came aboard automatically it seems."
- 27637 (12:40): "I believe you can belay your own standing orders at least, you may give it a try now, then a resume. Good to check."
- 41496 (16:31): "things such as that will be in the next milestone or two (colours proper, signals, etc). I believe, basically, our colours are always flying for now."
- 50860 (19:07): "books that can be purchased and read, and musical instruments that you can play".
- 51031 (19:10): "It seems that perhaps our single tool use session got too long and caused an error which forced a reset."
- 51149, 51789 (19:12, 19:23): "did you receive a proper log of everything that had happened so far including your journal entries?" ... "that's a testing note."
- 51877 (19:24): "I'm going to see if retiring to my cabin works and if it changes anything."
- 75026 (01:50): "would you be OK with you having to sleep as a system in game? ... you would ONLY be woken by an urgent event, someone waking you directly, or your rest recovering to a threshold?"
- 83413 (04:10): "I think in our modeling, the blanketing effect could be weaker than what we get from the sail anyway." 84675: "My view showed only about a tenth better with the spanker."

**What the captain did by hand because the officer could not or did not.**

- Bearings: eight during the departure (15582 to 17337), since `take a bearing` was refused to the officer (15559) and the officer never used the allowance.
- The pilot: no order exists to accept, refuse or hail him; the captain wrote the standing order that hove her to for the pilot's leaving (16693) because heaving to was his.
- Showing the officer its own journal (51753), at the fourth form tried.
- Waking the officer from open-ended stand-bys with a `tell` (25611, 41427, 50700, 74848, 97797, 101954); `Nudge the officer` (25573) is not an order.
- The deep-sea lead in the fog (102794). This was within the officer's domain; he did not think of it.

## 4. Orders refused

27 in the slice: 6 `agent.refused`, 21 `order.rejected` (5 the officer's, 16 the captain's). Classes: (a) vocabulary or grammar gap, (b) domain refusal as designed, (c) domain refusal that looks wrong for an officer with the deck, (d) correct ship-state or input refusal, (e) apparent bug.

**The officer's.**

| Tick, time | Order | Refusal's words | Class | What happened next |
|---|---|---|---|---|
| 402, 05:06 | heave short | "may not heave short without the captain: the anchor is let go and weighed by the captain" | (b) | allowed 407, done 409 |
| 525, 05:08 | send the boat ashore with the purser | "the port's business is the captain's" | (b) | allowed 529, done 532 |
| 14348, 08:59 | get under way | "the anchor is let go and weighed by the captain" | (b) by the letter, (c) in effect: `weigh` had been allowed at 553 | allowed 14366, done 14368 |
| 14581, 09:03 | standing order "pilot's lead": every 10 minutes, if ... | "After the name say a colon and then when, at or every: standing order \"pilot\": when ..." | (e) the name is cut at the apostrophe | renamed "inshore lead", accepted 14584 |
| 15428, 09:17 | hail the pilot | "is not an order this ship understands; did you mean 'haul'?" | (a); the brief itself lists "the pilot's hail" in his domain | nothing worked; the pilot boarded unasked |
| 15559, 09:19 | take a bearing of pendennis point | "the reckoning, the sights and the course shaped are the master's for the captain" | **(c)** a bearing of a point of land is ordinary watch-keeping | allowed 15561; captain took the bearings |
| 15650, 09:20 | tack ship | "She has not way enough on her to stay: 1.6 kn through the water." | (d), a good message | set the courses; did not tack |
| 18542, 10:09 | fill away | "a manoeuvre (tacking, wearing, heaving to, filling away) is the captain's" | (b) by the letter, (c) in context: the captain's own standing order had hove her to | allowed 18553, done 18557 |
| 41431, 16:30 | hoist our colours | "There is no such part as the our colours in this ship. ('set' was understood.)" | (a) feature absent; garbled echo | dropped |
| 51557, 19:19 | show the officer's journal | "may not show the officer's journal: a station is addressed by the captain" | **(c)** a station cannot read its own journal by any route | captain's 51753 put it in the log |
| 82323, 03:52 | set the stuns'ls | "Nothing done: the starboard fore lower studdingsail: The ... boom is rigged in; rig it out first; ..." (ten sails, 1,243 characters) | (d); sent 2 s after `run out the stuns'ls` | re-sent 82377 and 83197 |

**The captain's.**

| Tick | Order | Refusal's words | Class |
|---|---|---|---|
| 15434, 15442 | You may hail the pilot; You may pilot | "names no order the officer of the watch could be allowed" | (a) |
| 15476, 16019 | Tell the watcher ... (twice) | "There is no watcher at the station; nobody has been stationed there." | (d); the second message never reached the officer |
| 15587 | Take a beasring of pendennis point | "did you mean 'take in', 'take a lunar' or 'take a bearing of'?" | (d), helpful |
| 15593 | Take a bearing of Pendennis | "2 marks in sight answer to 'pendennis': Pendennis castle bearing SW and Pendennis Point bearing SW; say which." | (d), helpful |
| 16084, 16220, 17340 | Take a bearing of the lugo rock / the governor / the old wall | "is not in sight (a danger of the chart); in sight: ... and 19 more in sight" | (d); the message dumps the whole in-sight list |
| 16587 | standing order "Falmouth Pilot Off": when the pilot asks off then heave to | "'the pilot' cannot be 'asks off'; the ground is compared by what the lead brings up: 'is sand', 'is not rock'." | (a), with a misleading message |
| 16630 | ... if the pilot asks off then heave to | "A standing order begins with when, at or every, not 'if'" | (a); clear message. Third try worked (16693): `at the pilot asks to be put off then heave to` |
| 25573 | Nudge the officer | "is not an order this ship understands" | (a): the captain has no way to wake a station but `tell` |
| 51341 | tools | "is not an order this ship understands" | (d) |
| 51568, 51578 | You may show the officer's journal (and without the apostrophe) | "names no order the officer of the watch could be allowed" | (a) |
| 51741 | show the officers journal | "is said to an agent's station, and names one: ask the watcher ...; show the watcher's journal" | (a): yet `show the officer of the watchs journal`, also without an apostrophe, worked 12 s later (51753) |

## 5. Harness behaviour

**Seatings and door events.** One seating (tick 0: "The officer of the watch takes the station; sampled every glass and on notable and urgent events."). One door event in the transcript: 40648 `by=its own word door=speak`. No consent or drill trace is in this save; the drill for these weights on m5c is in `docs/agents/consent/2026-10-02-opus-5.5.md` ("Drill: passed": a library section, a journal line, `stand_by(until='eight bells')`).

**The conversation reset (the owner's note 10), as the log shows it.**

- 50758 (19:05): last words of the first conversation. It had just come out of a 2 h 33 min stand-by, a wait the MCP door keeps by having the model renew the call every 50 seconds (the door note).
- 50860 (19:07): the captain's `tell` about instruments gets no answer.
- 50908 to 50941 (19:08): `state({})`, `readings({})`, `library(find "officer of the watch")`, `library(primer 16, "may order")`, `read_log(severity notable, since_tick 0)`, then a journal note: "Taking up the deck again in a new conversation at 19:08, last dog watch. The log is my thread from here".
- The harness logged nothing: no `agent.stationed`, no reseat. `docs/agents/Harness.md` says a new chat "uses the same bridge and the same station; the model in the new chat has not read the brief, so start it with the prompt `brief`". OFFICER SAID (51163): "Honestly, sir, not whole. Coming back I had no brief and none of my old journal. I rebuilt our business from the log's notable lines and the readings".
- What the rebuilt officer got wrong in its first message (50945): it proposed "one stop in the book: when the reckoning is south of 49° 00' N and it is night, heave to", which was already there as "lie off the Bas" (27578); it said "only the royals I'd hand at sunset", though its predecessor had belayed "night sail" 3 minutes earlier to keep them; it spoke of "a brig of 1806", and at 51163 warned of "Mr Fox's blockade of May" 1806. The station brief ("as a lieutenant of 1806 informed the captain") and primer 16 ("the practice of 1806") both name that year; the scenario is 1805. `standing.given` and `agent.note` lines are routine, so a notable-only `read_log` cannot show a returning model its own standing orders or its own words.
- What it kept, because the game holds them: the deck, all 13 allowances, the book.
- The journal: `journal` only writes (OFFICER 51560: "it returns 'noted' and shows nothing back"); `show the officer's journal` is refused to the officer (51557); the captain's `show the officer of the watchs journal` (51753) printed "The officer of the watch's journal (46 entries)" into the log, where the officer read it (51798: "I see it, sir, all 46 entries ... my journal dates us 12 June 1805, not 1806"). Of the 46 entries 24 were stand-by lines, 14 deck lines, 3 harness lines and 5 the officer's own notes. OFFICER: "the stand-by lines outnumber the real entries; they'd read better folded or left out."

**Stand-bys.** 37 in the slice, none refused. The `until` values: under way (4), sunset (4), ten minutes (4), the boat alongside (3), 5 minutes (3), filled away (3), hove to (3), a glass (2), a landfall (2), a change in the sky (2), and once each: the deck given, the pilot asks to be put off, the pilot off, a stranger's colours made out, a bearing steady and closing, a notable event, sunrise.

The long ones, and what ended them:

| Stood by | Until | Ran | Ended by |
|---|---|---|---|
| 1356, 05:22 | the boat alongside | 80 min | the event |
| 6496, 06:48 | the boat alongside | 131 min | the event |
| 20722, 10:45 | a stranger's colours made out | **81 min** | the captain's word |
| 28802, 13:00 | sunset | 197 min | the officer's own word (40648) |
| 41498, 16:31 | a bearing steady and closing | **153 min** | the captain's word |
| 54401, 20:06 | hove to | **341 min** | the captain's word |
| 75603, 02:00 | sunrise | 112 min | the event |
| 85357, 04:42 | a landfall | **207 min** | the captain's word ("Fogged in.") |
| 98493, 08:21 | hove to | **58 min** | the captain's word |
| 103970, 09:52 | a change in the sky | 367 min (ends at 126000, after the slice) | the event (fog lifted) |

Five stand-bys waited for an event that never came and were ended only because the owner spoke. During stand-bys these notable lines did not wake the station: "Sail ho!" (23340, 32580, 40740), three squalls (35970, 36448, 39869), every wind shift, and "Fog came down" (97200). That is the design ("an urgent line wakes you at once"), and the 50-second hold does show the model the notable lines logged since, but the patience rule (an hour for the officer; its nudge, "no reply for an hour", first appears at 353345 in a later slice) does not run during a declared stand-by, so nothing bounds the wait.

**What woke the station: 36 `agent.resumed`.** A word from the captain 18; a question from the captain 1; the awaited event 7 (boat alongside 2, under way, the pilot asks to be put off, the pilot off, filled away, hove to); a timed stand-by 5; a glass 2; sunset 1; sunrise 1; its own word 1. No urgent line (there was none). Five of the 18 words were `you may` grants: four only made the officer re-issue the same stand-by and one drew a thank-you. The captain's `tell` was the most useful waker in the slice (the shoal talk, bearings, "Sail ho!", "Fogged in.", the stuns'ls before heaving to).

**The night, sunset 20:03 to sunrise 03:51.** 157 log lines, 28 notable, none urgent. The officer was resumed three times: sunset (54216), the captain's word (74849, 01:47) and sunrise (82318). No event woke him between 20:06 and 01:47. Stand-bys used: "hove to" (20:06) and "sunrise" (02:00). Wind shifts logged: three (20:37 "veered to W, a light breeze", 22:41 "veered to WNW, light airs", 00:51 "veered to NW, light airs"). Taken aback: none; there is no `sail.backed` line between 09:57 on 12 June and 09:32 on 13 June.

**Nudges.** Two, both logged at routine severity, both in the same tick as the order they counted.

- 6143 (06:42): "The officer of the watch nudged: 3 contrary orders on the ship within the watch (heave short; send the boat ashore with the purser; buy seven tons of tin)."
- 14368 (08:59): "The officer of the watch nudged: 4 contrary orders on the ship within the watch (heave short; send the boat ashore with the purser; buy seven tons of tin; get under way)."

Neither was right. No order undoes the one before it; they are four steps of one plan, and `get under way` is the natural sequel of `heave short`. The detector seems to treat any two whole-ship orders as sharing the part "the ship". The second chain also spans a change of the watch (05:06 to 08:59). OFFICER'S JOURNAL (6494): "They aren't contrary; they are the steps of one plan (clear the shoal, fetch the prices, buy the cargo). A false positive in the stuck-detector for port business, worth a look by the developer. Continuing." No pause followed.

**Handover notes.** None in the slice; Claude through Desktop "is not asked" (primer 16). At the reset there was therefore nothing folded up to hand to the new conversation.

**Tools.** `submit_order` 52 (40 accepted, 6 refused by domain, 5 rejected, 1 query); spoken lines 48; `stand_by` 37; `library` 9; `journal` 5; `shelve` 3; `readings` 2; `answer` 2; `state` 1; `read_log` 1. The five journal notes were good ones (the papers, the Roscoff approach, the false nudge, five developer notes at 10:13, the note on taking up the deck again). None was written between 19:09 on 12 June and noon on the 13th.

**Turns that ended oddly.**

- A spoken line ends the turn, so a follow-up order waits for the next sample. At 82327 the officer said he would set the studdingsails "when they're out"; his next turn came only because the captain spoke 48 s later (82375). At 15573 he reported bearings "refused to me" 12 s after the allowance had been logged (15561), and never used it.
- 536: "The launch is away with the purser" when the LOG (533) said "Not hands enough on deck to send boat; the hands are heaving short"; she left at 1337.
- 51042 (19:10): "I'll look in each glass", then at 20:06 a stand-by "until hove to" that ran 5 h 41 min.

**Limits.** OFFICER SAID (75035): "a sleeping officer isn't sampled, which spares the length of my conversation, the thing that sank me yesterday." The first conversation lasted 14 hours of ship's time and 108 recorded transcript entries, plus the uncounted 50-second stand-by renewals. Library pages stay in the chat after `shelve` (the door note says so).

## 6. Ship, sea, navigation and port observations

**The pilot at Falmouth.**

- *Boarding.* She was under way: LOG 15416 "Under way on the starboard tack, under topsails and the jib"; 15650 "1.6 kn through the water"; courses set 15826 and 15866; 15900 "The cutter hailed: a pilot for Falmouth; shorten sail and he will come aboard."; 16020 the pilot aboard. She was making sail, not shortening it. No speed is logged at that minute; from 1.6 knots at 09:20 and the Black Rock "a mile" off at 09:19 and abeam at 09:35, about two to four knots. Primer 14's rule is "Within two cables, with your way under six knots, he boards". Nobody could accept or refuse him, and £5 left a purse of £160.
- *The cutter's distance does not change.* "distant two miles" at 15120 (bearing S), 16084 (SSE), 16220 (ESE) and 17340 (NW by N): 37 minutes in which she hailed and put the pilot aboard. The bearing moved, the distance did not. Then a fresh "Sail ho! The Falmouth pilot's cutter on the starboard quarter, bearing NW by W, distant a mile" (17700).
- *Leaving.* 18300 "The cutter on the larboard bow is out of sight."; 18420 "The cutter hailed: she has come off for the pilot."; 18540 "Mr Tregenza left her in the cutter".
- *His words.* The same paragraph of 174 words three times in 34 minutes: on boarding (16020), to `ask the pilot about the Old Wall` (16209, which it does not mention), and to the captain's `ask the pilot off` (18031, taken as a question). It is the inward directions for Carrick Road, said to a ship going out. "took charge of her" overstates; the officer steered throughout.

**Heaving to.**

- *For the pilot (17640).* LOG: "Braced the main topsail aback; hauled aft the head sheets; helm a-lee" (17674); "Hove to, main topsail to the mast, helm a-lee" (17726); leeway "18° to larboard" (17800); "Fore topsail taken aback", "Jib taken aback" (17834, 17846); **"Main topsail filled again" (17857)**; leeway "49° to starboard" (17927); "Hove the log: one knot and a half" (18035). These lines read as her going through the wind and lying on the other tack with way on; the main topsail was aback for 152 seconds. The pilot left 15 minutes after he asked, from a ship making a knot and a half. OFFICER SAID (18545): "She's lying to, though she has paid off to NE by N and is creeping two knots toward the Bizzies, five miles."
- *In the fog (102690), from a run with the yards square.* The fore topsail was aback almost the whole time ("Fore topsail taken aback" as a notable line at 102854, 103968, 105202, 105728, 107455, 110747, each within a minute of "filled again"), with "no way" by the log. By these lines she lay with both topsails aback. The evolution's logged steps (102691) brace the main topsail aback and put the helm a-lee; none braces up the head yards.

**The lookout's words.**

- 15120: "Sail ho! A cutter standing out from the land right astern, bearing S, distant two miles." She was heading between S by W and SE by S (190° at anchor; "Steady, full and by" at 15347) and making a stern-board in the cast ("Helm a-lee for the stern-board", 15017). Three minutes later the same cutter is "on the starboard bow" (15300). The relative bearing may be taken from her track.
- 20100 "A sail on the starboard bow, bearing S, distant three leagues"; ten minutes later the only line about her is 20700 "The sail on the starboard quarter is out of sight." There are seven `lookout.sail_lost` lines against six sightings, so at least one (54240, 20:04, "The sail on the starboard quarter is out of sight") is for a sail never reported.
- 26100: "The cutter on the larboard bow is a cutter".
- The in-sight list lags: the captain's bearing "The Black Rock bore SSW" (16212), and 8 s later the list in a refusal still has it "bearing S by W" (16220). OFFICER'S JOURNAL (18818): "The lookout's in_sight line froze".
- 15540: "The Black Rock bearing S by W, steady and closing: distant a mile." and "St Anthony's Head bearing SE by S, steady and closing: distant two miles." Both came 2 s after "Steady on S (180°)" (15538), at under two knots (1.6 through the water at 15650); the head was three points on the bow. Each fired once. Nothing more was said as she passed the rock at two cables.
- *What was done about the Black Rock line.* Nothing at once: the officer had asked leave to tack 26 s before (15514) and stood by "5 minutes" 3 s after. The captain asked for bearings and took them himself ("The Black Rock bore S by W, a mile by estimation", 15582). The tack was allowed, refused by the ship and given up. At 16048, with the pilot aboard, the officer altered one point: "the Black Rock dead ahead, so I've put her on S by E to fill and pass east of the Rock as he advises". At 16518 he came to SSE with the rock "abeam to starboard, two cables".
- OFFICER SAID (16052): "the danger list puts the Lugo rock at 'no distance' while the lead gives fifteen fathoms". The log has no `the dangers` output to check this.

**Standing orders and the hands.**

The officer's eight, all entered "by the lieutenant":

| Name | Entered | Text | Fired in the slice | How it behaved |
|---|---|---|---|---|
| inshore lead | 14584, 09:03 | every 10 minutes, if the depth of water is under 20 fathoms then heave the lead | 8 (09:13 to 10:23) | then held; one `standing.held` line a watch |
| trim on a shift | 14586, 09:03 | when the true wind shifts 1 point then trim sails | 29 | belayed and resumed as a test (27639, 27641); belayed on heaving to (102758) |
| fresh breeze | 14588, 09:03 | when the true wind exceeds 24 knots for 5 minutes then take in the royals; take in the topgallants | 0 | the most wind was 17 knots in a squall |
| strong breeze | 14590, 09:03 | when the true wind exceeds 30 knots for 5 minutes then reef the topsails, one reef; take in the flying jib | 0 | |
| lie off the Bas | 27578, 12:39 | when the reckoning is south of 49 00 N and daylight is night then heave to | 0 | OFFICER (82327): "49° 02' N at dawn" |
| night sail | 27580, 12:39 | at sunset then take in the royals; take in the flying jib | 0 | belayed at 50755 (19:05), before its first sunset |
| fog lead | 97811, 08:10 on 13 June | every 10 minutes, if the visibility is a cable then heave the lead | 22 | |
| fog stop | 97815, 08:10 | when the depth is under 20 fathoms then heave to | 0 | |

- Refused at entry: only the first name tried, "pilot's lead" (14581), for its apostrophe. The two rules that heave to were accepted because allowance no. 13 stood (a later slice shows the reverse: "fog anchor" was refused at entry at 169301 until the captain allowed the anchor). The captain's one rule, "the pilot put off" (16693), fired once (17640).
- Overnight (sunset to sunrise) only "trim on a shift" fired, seven times; "inshore lead" held. All the night's fights for hands came from those trims: 33 `evolution.waiting` (7 notable) and 5 `evolution.short_handed`.
- "trim on a shift" fired 29 times (09:33 on 12 June to 08:59 on 13 June) against 11 `wind.shift` lines. Each firing writes up to three notable lines. Together they are about 83 of the slice's 276 notable lines. "Bracing the yards: not hands enough for all at once" was logged as notable 27 times (25 of them from this order). 13 of the first 16 firings ended at the same "60° to 68° from square", so most daytime trims changed nothing.
- Through the night it did its work: as the wind veered from WSW to NW the yards went from 60° through 58°, 57°, 44°, 38° and 20° to 0° from square (20:07 to 01:43) with nobody sampled.
- "fog lead": 22 firings, 22 times "No bottom at twenty fathoms" as a notable line in 3 h 30 min, in 49 fathoms.
- `standing.held` for "inshore lead" is logged once a watch (8 lines) and each gives the depth: "the depth of water is 30 fathoms and a half", then 41½, 45½, 46½, 47½, 48½, 49½, 49½. The hand lead could only say no bottom at twenty, and the deep-sea lead took the captain's order and 15 minutes to say "Forty-nine fathoms" (103682). The held line gives the same figure for nothing: the rule judges the depth every ten minutes without a cast. "fog stop" ("when the depth is under 20 fathoms then heave to") presumably does the same.
- Fights for hands: 112 `evolution.waiting` (32 notable) and 29 `evolution.short_handed`. Real delays were few: the boat waited 7½ minutes for the heaving short to finish (533 to 989), and one cast took 7 minutes instead of 90 seconds ("Only one hand to heave lead", 102012).

**The port and the boat.**

- Trip 1, prices: ordered 532, hoisting out from 989, away 1337 (05:22), landed 2665 (05:44), shoved off 4465 (06:14), alongside 6141 (06:42). 80 minutes away, 94 from the order.
- Trip 2, seven tons of tin: bargain 6143, away 6491 (06:48), landed 7795 (07:09), shoved off 12655 (08:30), alongside 14337 (08:58). 131 minutes away, 137 from the bargain.
- The launch was "alongside from the shore and hoisted in" at 6141 and hoisted out again from 6144 (5.8 minutes to hoist out each time).
- One bargain per trip. The whole business took 3 h 50 min at a one-mile pull.
- She lay hove short on 15 fathoms of cable in ten fathoms from 05:16 to 08:59 in about 9 to 13 knots of wind on the ebb, and nothing dragged.

**Other things.**

- The "merchant brig" has a lieutenant, a purser, a master and, by the officer's journal, "provisions 120 days for 121 men" and a hold of "32 tons": a man-of-war's company and a tenth of her burthen for cargo.
- Echoes: "may shift (the course)", "may take a bearing of", "49 00 n", and the `order.accepted` echo of a standing order drops the quotes and semicolons.
- "A squall: the wind veers a point to WNW and freshens to 12 knots, with rain" (35970); 12 knots again at 39869. A 12-knot squall is a notable line.
- Fog came down at exactly 08:00 (97200). In the whole log 15 of the voyage's 16 fog changes fall exactly on eight bells; the one exception is 507720 (02:02 on 18 June).
- Light-air speed looks generous: gust lines give "the mean 3" at 23:51 to 00:18 and 02:41 to 03:13, and the log is hove at "two knots and a half" (00:00) and "one knot and three quarters" (03:00, wind right aft). This is a judgement, not a fault I can prove.
- The ground: 49 fathoms brought "fine grey sand with black specks". `freesail/world/reckoning.py` (`_GROUND_BY_DEPTH`) gives that for any depth from 30 to 60 fathoms with no chart note near, so the arming cannot tell one place from another. The officer said as much (103935).
- Readings: OFFICER SAID (84659) "The readings give speed in whole knots"; the captain's view shows tenths (84675).

**What read well.** High water at 05:00, the Black Rock "showing" at half ebb (11280, 08:08) and the pilot's "the flood will serve from about eleven" agree. Sunset 20:03 and sunrise 03:51 are right for the latitude; the second noon comes at 11:58 after 42' of easting. The first noon was a mile from the reckoning. `tack ship` was refused with her speed in the words.

## 7. The model as an officer

**Good calls.**

- Before he had the deck he noticed the swing over shoal water and left the decision where it belonged (261).
- He read the port chapter and the papers within two minutes of taking the deck, and proposed the trade that made the voyage: "Buy about eight tons of tin at £120, run down to Roscoff ... sell the tin and fill with brandy" (440). He bought seven to keep a margin.
- He journaled the Roscoff approach before sailing (1352). After the reset that note was what restored the plan.
- A coherent set of night orders within his authority: lead inshore, trim on a shift, sail off for 24 and 30 knots, then "lie off the Bas" so as not to make the land in the dark.
- He changed his mind in the open. He asked leave to tack in 3¼ fathoms, found she would not stay, set sail for way, saw the water deepen and said "I'll not tack after all" (15790). He had asked: "If you'd not tack here, sir, I'd value your reason" (15663).
- He bore away a point for the Old Wall when his first estimate proved too fine (16727).
- He belayed "trim on a shift" as he hove to (102758), as he had said he would at 12:39 and 20:03.
- In the fog he hove to on his own judgement with the allowance in hand and explained at once: "I've brought her to, sir, and I'd rather explain than ask forgiveness. On SSE she was standing straight for the mainland west of the Bas ... six or eight miles off by a reckoning five miles uncertain" (102695).
- Candour about the reset (51163) and useful developer notes (18818).

**Mistakes and weak points.**

- Open-ended stand-bys on one event near a foul coast (section 5). At 04:42 he stood by "until a landfall" 27 miles from Roscoff at two to three knots; the fog made that event impossible and the captain had to wake him.
- He lay 3 h 43 min at a short stay (15 fathoms in ten) and never veered again as he had proposed at 378.
- He never used the bearing allowance and never took the departure he announced (18617).
- He ordered `set the stuns'ls` 2 s after `run out the stuns'ls` (82321, 82323).
- He did not think of the deep-sea lead in fog.
- The shoal alarm at anchor was probably overstated. He read "the chart now gives only three fathoms under her" as the water at high water and feared grounding at low. The anchor "let go in ten fathoms" where his readings had "seven" suggests the chart figure leaves the tide out, and three fathoms is 18 feet against her 11 (LOG 636653, a later slice: "she draws 11 feet"). Heaving short was cautious and did no harm.

**Invented or unsupported facts.**

- "if this is the summer of 1806" (51163), withdrawn at 51798.
- "yesterday's fog lifted about then" (102695): the log has no fog on 12 June.
- "that's exactly the ground we had in mid-Channel and off the Start" (103935): no such casts were made this voyage.
- "stand-on ship" (41434) is a later century's phrase.
- "a quarter less... three and a quarter fathoms" (15514): he stumbled over the leadsman's "And a quarter three" and corrected himself in the same line.

**What he asked for or wished for.** A general grant for the port's business (528) and of authority (14513); leave to take bearings (15573); a hail for the pilot and colours to hoist (15428, 41431); "A read for the officer's own journal, or the last handover note given to him on taking the deck" (51560); stand-by lines folded out of the journal (51798); sleep only when another has the deck, and "a short handover from whoever had it" on waking (75035); "speed to a tenth of a knot in the readings" (84659); "Varied ground would make the deep-sea lead a true navigator in the fog" (103935); a measured veer of cable (378).

**Quotes worth keeping.** "It's different from watching: as watcher I could see a danger and only say so, and now the weight of it is mine, which I find I like" (27688). "The watch bill has put the officer of the watch to bed" (74857).

## 8. Cross-check against the notes

**The owner's items.**

- **1, pilot boarded under way.** SUPPORTS: 16020, two minutes after the hail, under way and making sail (section 6).
- **2, the well.** Cannot be seen in this slice.
- **3, price lists.** ADDS NUANCE: the officer bought for Roscoff on a guess, "tin £120 here, likely dear in Roscoff or Brest" (journal, 436), knowing only Falmouth's list.
- **4, the primer's go-through.** ADDS: the brief and primer 16 say "1806" and the returning model took that for the year.
- **5 to 8, 20, 22, 25.** Cannot be seen (another session, or the browser).
- **9, accepting or refusing the pilot.** SUPPORTS: `hail the pilot` and `You may hail the pilot` do not exist (15428, 15434); the captain's "Up to you, I say" (16019) was lost; "Pilot came aboard automatically it seems" (16040).
- **10, the long tool session and the journal.** SUPPORTS, and this slice is where it happened (section 5). The log has the exact words of the note: `show the officers journal` rejected (51741), `show the officer of the watchs journal` accepted (51753).
- **11, journal out of the context.** ADDS NUANCE: here the journal was not in the new conversation at all and no tool reads it; shown, more than half of it was stand-by lines.
- **12, re-seating.** Cannot be seen, but the reset was a return to the station that the harness never knew about.
- **13, multi-condition stand-bys.** SUPPORTS strongly: five stand-bys of 58 to 341 minutes ended only by the captain. What the watch called for was hove to or sunrise at 20:06, and a landfall or fog or a glass at 04:42.
- **14, restarting Claude Desktop.** ADDS NUANCE: a new chat without a restart keeps the station but gets no brief unless started with the `brief` prompt.
- **15, general authority.** SUPPORTS: 13 grants in five hours, and the conversation at 14504 and 14513 that the note comes from.
- **16, "keep" orders.** ADDS NUANCE: "trim on a shift" was the stand-in. Here is its benign case (29 firings in a steady breeze, belayed in time when she hove to) and its cost in log lines.
- **17, taken aback urgent in a calm.** Cannot be seen: 0 `ship.aback` lines. The 15 `sail.backed` lines belong to the cast (1), the two heavings to (8) and the fore topsail while lying to in the fog (6, 09:34 to 11:45).
- **18, wind-shift spam.** Cannot be seen: 11 `wind.shift` lines in 31 hours (10:29 on 12 June to 11:56 on 13 June), never closer than 13 minutes.
- **19, the lookout near visible land.** ADDS NUANCE: a `lookout.closing` line exists and fired at a mile (15540), notable, once, with nothing more at two cables. The danger list by account had a rock at "no distance" in fifteen fathoms (officer's claim).
- **21, a turn need not end with `say`.** SUPPORTS modestly: 82327 and 15573 in section 5.
- **23, several stations through one door.** Only that the captain twice typed `Tell the watcher` by habit.
- **24, parity near the coast.** SUPPORTS: the officer fixed her in the entrance from the lookout's rounded marks, "Trefusis Point NW by W five cables, Mylor Point N a mile ..." (15573).

**The model's comments and additions.**

- "The officer isn't treated as a person on deck ... listed 'below, asleep'": SUPPORTS, 74857 (officer's claim; the captain answered "Preposterous!").
- "The contrary-orders warning fires on ordinary sequences": SUPPORTS, 6143 and 14368.
- "Other ships keep a fixed distance": SUPPORTS, the pilot cutter at "two miles" for 37 minutes.
- "the 'two cables' rule is applied on boarding but not on leaving": ADDS: at Falmouth the cutter was logged "out of sight" two minutes before she hailed for the pilot (18300, 18420).
- "Each boat trip carries one bargain and takes about 4½ hours": ADDS NUANCE: one bargain a trip, yes; at Falmouth 80 and 131 minutes.
- "Lead standing orders fight for hands": ADDS NUANCE: two lead orders stood together here without trouble; one cast was late (102012).
- "The hand lead says 'no bottom at twenty fathoms' while the depth reads 15 or more": not seen as such; 19478 is a cast of no bottom from a rule that had just judged the depth under twenty.
- "The relay cut calls at 60 seconds": the door note here already says 50 seconds.
- "Drill stand-by carried into the station", "The handover note isn't part of the reseat brief", the mate in the boat, kedging, sternway, the water sail, number words, "full and by", "no water", the reckoning at anchor: cannot be seen in this slice.
- What worked well. SUPPORTS: the noon latitude (25200), the ship's papers (418, 436), number-free standing orders (the night's trimming). The rest lies in later slices.
- Local notes 2 and 4 (the handover as in-game compaction): SUPPORTS by contrast. Through Claude Desktop no handover is asked for, and the conversation was lost at 14 hours with nothing folded.

## 9. New findings not in the notes

Ranked by weight.

1. **A new chat is invisible to the harness and starts with nothing.** No door event, no brief, no journal, no handover note; the notable-only log hides the officer's own standing orders and words. In its first message the returning officer re-proposed an existing order, reversed its predecessor's sail plan and misdated the year (50908 to 51163).
2. **A stand-by on one named event has no bound and is deaf to fog and to a strange sail.** "Fog came down" (97200) did not wake an officer waiting for "a landfall" with studdingsails set; "Sail ho! A brig ... distant three miles" (40740) did not wake him either. Patience is not counted during a stand-by.
3. **Three refusals look wrong for an officer with the deck:** taking a bearing (15559), filling away after the captain's own standing order hove her to (18542), reading his own journal (51557). And `get under way` is refused when `weigh` is allowed (14348).
4. **The pilot cannot be accepted, refused or hailed**, though the brief puts "the pilot's hail" in the officer's domain; he costs £5 and a heave-to, and says one paragraph to every question.
5. **Hove to, she does not lie to.** For the pilot she passed through the wind, the backed main topsail "filled again" within 2½ minutes, and she made 1½ knots (17726 to 18035); in the fog she lay with both topsails aback for hours.
6. **The cutter's reported distance stayed at its first-sighting figure** for 37 minutes while the bearing moved, and she was "out of sight" two minutes before she hailed alongside (15120 to 18420).
7. **`standing.held` gives the depth of water** to half a fathom once a watch without a cast, and a depth rule can act on a depth nobody sounded.
8. **Two false "contrary orders" nudges** from four different whole-ship orders; "within the watch" spanned two watches.
9. **Log volume from good standing orders:** "trim on a shift" is about 30% of the slice's notable lines; "No bottom at twenty fathoms" 22 times in a morning.
10. **A `tell` to an unmanned station is rejected and its words lost** (15476, 16019), the second at the moment they mattered.
11. **Apostrophes:** a standing order's name is cut at one (14581); `the officers journal` fails where `the officer of the watchs journal` works (51741, 51753).
12. **Smaller:** the allowance echoes; "for the watch" that outlasts the watch; `when the pilot asks off` answered with words about the ground (16587); the 1,243-character studdingsail refusal; whole knots for the officer and tenths for the captain; the boat hoisted in and out again; the man-of-war's company in a "merchant brig"; one ground for every depth from 30 to 60 fathoms; relative bearings in the lookout's "right astern" and "sail lost" lines.

## 10. Could not determine

- **Why the first conversation died:** the length of one tool-use turn, the context, or a timeout. The save has ticks, not real time, and none of the chat.
- **Whether the new chat was started with the `brief` prompt.** The officer says it had no brief; the harness logs nothing either way.
- **Whether the first seating ran its own consent step and drill**, or relied on the record of 2 October. The transcript header names a 3 October record, which belongs to the later m5c-b re-ask.
- **Her true speed when the pilot boarded, and her heading while hove to.** Only the officer's "NE by N" and the leeway, sail and log lines.
- **Whether the cutter's "two miles" is a cached word or a real station kept.** Comparing two saves' stored positions would settle it.
- **Whether the readings' chart depth includes the tide**, and so whether the shoal alarm at anchor was warranted.
- **Whether "the depth of water" in a standing order is the true depth or the chart at the reckoning.**
- **Whether the first boat trip was needed:** the scenario's papers already list a Falmouth price list and the officer quoted "tin £120" before the boat left. Primer 14 says `buy` is refused "Until the boat has been ashore".
- **What "may shift (the course)" allowed** that `steer` did not.
- **How good the account was at noon on 13 June** (48° 47' N, 4° 13' W, no observation for 24 hours, 49 fathoms by the deep-sea lead). The next slice has the officer finding it badly out (transcript, 135725: "The reckoning says 3° 49' W, which is ashore in Morlaix Bay"); from this slice alone it cannot be judged.
- **Where the officer's "as watcher" memories come from** (27688, 103935). The consent record of 2 October has the same model saying it had "stood three watches as the watcher already", so earlier sessions may be in the chat.
- **Whether retiring to the cabin "changes anything"** (the captain's test at 51877). Nothing in the log differs while he is below.
