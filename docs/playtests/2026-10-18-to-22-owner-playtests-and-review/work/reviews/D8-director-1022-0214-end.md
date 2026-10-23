# D8: the director, Western Islands run, 2026-10-22 02:14Z to the end (05:03Z)

## Scope

- **Span.** Transcript 2026-10-22 02:14:19Z (compaction boundary) to 05:03:14Z, the end of the chunk.
  - Game time: 1805-07-02 First watch (about 21:30, director journal tick 2133012) at Horta, to the director's stand-down at 06:45 on 07-05 (tick 2339132).
  - The save ends at tick 2339167. Play continues after a break.
- **Version.** H (hotfix copy), rules fingerprint 372c899e355594fa (the save's build). No code changed in this span.
  - The director edited only H's `docs/dev/TuningNotes.md`, eight times: it appended "Open, for the lead" at 02:14:36 and amended it at 02:25, 02:27, 02:38, 02:39, 03:23, 03:42 and 03:53.
- **Seats.**
  - Director: Opus 5.5 through the MCP bridge in the Claude Code session "Sailing game scenario design", the same session that wrote the hotfixes. Stand-by slices were 55 s; the budget was 9999/9999 a day.
  - Officer of the watch (Mr Pearce): claude-sonnet-5-5 through the API door.
  - Captain (Mr Bowen): the owner at the prompt.
- **Files read.**
  - `work/chunks/director-8.md` (all 2,859 lines) and `work/reviews/BRIEF.md`.
  - `work/saves-extracted/cutter-western-islands-final.md`: head, end ticks, and targeted greps.
  - `work/chunks/cutter-officer-3.md`: targeted, for the same events from the officer's side.
  - H's `docs/dev/TuningNotes.md` §"Open, for the lead" (l. 7493–7547).
  - G's `TechnicalSpec-M7b.md` §2, §3, §8, §9, §14, §17a, §19, §24 (66, 53b), §25, §26; `DesignProposal.md` §5, §7.6, §11; `dev/M7b-WorkPackages.md` (the waves table, 66 as merged); `TechnicalSpec-M6.md` §9; `TechnicalSpec-M4.md` §24.
  - Code in H and G, read only: `agents/harness.py`, `agents/remote.py`, `agents/mcp_server.py`, `agents/tools.py`, `orders/stations.py`, `world/orders.py`, `world/things.py`.

## Narrative

- **02:14Z.** The session resumes from compaction and writes the swing-spam bug and the run's other open bugs into a new H TuningNotes section, "Open, for the lead". It tells the owner: "I haven't changed any code."
- **02:16Z (game 23:10).** The captain raises a wine cargo. As Bettencourt, the director offers ten pipes at "thirty-six pounds the ton" freight. At 02:21Z, when the captain offers 20 tons, Bettencourt corrects himself in character: £36 is the wine's price, the freight is £4/t. The director confesses the slip to the owner out of game.
- **02:22Z.** The director says the swing lines have stopped. Twenty-two more appear by 02:23:54Z. It amends the TuningNotes entry (pairs every 5–6 min for hours) but does not correct itself to the owner.
- **02:27–02:39Z.** The director logs new bugs while standing by: officer reports labelled "The captain to the captain"; Pearce unable to take Bettencourt's letter; "Mr Josiah Hale" refused.
- **02:36Z (06:21, 07-03).** Ruiz seeds a Frenchman asking questions on the quay. The director makes Bettencourt's sealed reply a thing in his keeping. It then has to lay the letter on the desk for Pearce to pick up.
- **02:37Z.** The director tries `say as Mr Bowen`, the player's captain. The rule of reach refuses it.
- **02:39–02:43Z.** Hale tells Pearce the Frenchman left toward Porto Pim. There is no form to walk Hale to the quay, so the boat returns without him. The director then brings him aboard by order, with his chest (a duplicate stays on the quay) and £5 passage.
- **02:41Z.** The captain drops an in-game aside: "if they stood by until a notable event…". The director switches to that wake.
- **02:48–03:09Z (07:25–11:16).** As Pascoe, the director reports a torn copper sheet. The captain orders her heeled by guns and water and a masthead tackle; the copper is patched and she is righted. All of it is words only.
- **02:55Z.** The captain gives Bettencourt the owners' Madeira. Bettencourt pays ten guineas by transaction. The captain buys 8 pipes (4 t) on his own account at £32/t.
- **03:16–03:19Z (11:47).**
  - The captain cannot send a letter ashore ("Send a letter by the boat" is refused; "Send the boat with a letter" is belayed).
  - The director makes the letter a thing and improvises Tomás, a fruit-boat boy, to carry it.
  - The captain goes ashore himself, telling Tomás loudly they will stay "quite some time" as a cover story.
- **03:22Z (12:08).** Bettencourt agrees to send 8 days' provisions and water. The director finds it cannot add stores and writes that gap into TuningNotes. The journal notes Bettencourt was "oddly omniscient" about the cover story.
- **03:34Z (18:32).** The captain has the well pumped. The director's hotfix order works live: "the well pumped dry (0.02 m of water pumped out)".
- **03:35–03:43Z (20:00–22:13).**
  - The director times the two freight orders from the lighter constants it read in `ports.py`, and both lighters come alongside about 22:05–22:13.
  - Ruiz pays £40 freight in and is paid £128 out.
  - A case of wine and the bill of lading are made as things.
- **03:43Z (22:13).** The captain asks out of character in a `say to Mr Ruiz`. The director answers with `say(text)`, also out of character, telling him to send for the provisions himself. That text went to the director's hidden log, not the game (D8-04). The captain orders provisions and water at the yard's price.
- **03:46–03:54Z (22:39–00:31).** She weighs the small bower and gathers sternway on the slack best bower. The "under way" and "the anchor weighed" stand-bys misfire. She is under way about 00:24 on 07-04, unseen in the haze.
- **04:04–04:30Z (07-04 to 07-05).** The passage SE, then 119°, toward Funchal.
  - The director reads the truth twice. The Basque stays on station off Santa Maria, 45–60 miles north of the track.
  - The director journals "no contrived ambush" and intervenes no further.
- **04:31Z (06:44, 07-05).** The officer stands down at the captain's word. Claude Code moves the director's stand_by to the background when the owner's message arrives. The director stops that task and stands down with a full note.
- **04:34Z.** The owner: "I think we might have the record for the longest playtest yet!"
- **04:37Z.** Asked what the world orders most lack, the director answers "a way to schedule a world order". It also names moving people ashore, handing things to held people, stores received, and removing a thing.
- **04:42–04:47Z.** A conversation about enjoyment and play for LLMs. The owner: the game should be fun for human and model alike, "not research", and perhaps one day played by an agent "just because they want to".
- **04:55–04:56Z.** At the owner's invitation the director web-searches Anthropic's "J-space" (global workspace) paper through a subagent and relates it to grammar friction.
- **05:00Z.** The director argues for "better refusals" over a wide grammar and offers a script to rank refused orders.
- **05:03Z.** The owner defers that script to this cold review and says it is "just a play session in the end".

## Findings

| ID | Category | Severity | What | Evidence (timestamp/tick, ≤15-word quote) | Spec/design ref | Recommendation | Status in G / H |
|---|---|---|---|---|---|---|---|
| D8-01 | bug | med | The officer's words to the captain are logged as the captain's and "kept" for nobody. `orders/stations.py` `_keep_word` hard-codes "The captain to the {station}". It runs because `_held(agents, "captain")` finds no harness when the player holds the captain at the prompt. | 25 lines in this chunk, e.g. 22:08 "The captain to the captain: Aye, sir. 22:08: the bell…". First noted by the director on 11 June (save l. 1474). | §9 rule of reach (`held_stations` counts the captain at the prompt); 66's "who heard" | Name the speaker from `speaker`/`said_by`. Treat the prompt-held captain as held, and deliver the word instead of keeping it. | Same code in H (l. 866) and G (l. 881); open. In H's notes. |
| D8-02 | bug | med | The tide-swing line flip-flops for hours at anchor and is NOTABLE, so it wakes "a notable event" stand-bys. | 66 lines 21:34–23:09 (07-02); again 07-03 23:09/23:12, which woke the director (03:46:57Z). 02:22:27Z "The swing lines have stopped now that the tide has turned", then 22 more. | `core/world.py` `_tick_tide`; `world/tide.py` slack threshold | Hysteresis, as H's notes propose (class-level default for checkpoints). Check the stream read at her position as she sheers on 240 fathoms. | Open; written in H's notes only. |
| D8-03 | harness | med | Each 55-s "Still waiting" result re-lists every notable line since the stand-by began, so swing spam is repeated poll after poll. | 02:29:52–02:33:43Z: five identical results, "Notable lines logged since then (59)" "…[+11785 chars]". | `mcp_server.still_waiting` (package 28c: "not a decision to be blind") | List only lines new since the last result, with a count of earlier ones; dedupe repeated kinds. | Same code in G (l. 291); open. Not in H's notes. |
| D8-04 | harness / docs | med | The director's `say` result tells it "Your words are in the log under your mark", but a director's words are only a note in its hidden log. Its out-of-character instruction to the captain and its narration never reached the game. | 03:43:59Z "(Director, out of character: please order it yourself"; 03:54:19Z "Astern, the few lights of Horta blur…"; save l. 11397, 11565. | `harness.py` ~l. 1959 ("never a line of the play log"); §6 | Word the result for the director ("written in your log; nobody hears it"). Decide whether a logged, explicit OOC channel between player and director is wanted. The owner already uses parentheses in `say to`. | Same wording in G `remote.py` l. 872; open. H's notes repeat the misreading ("`say` putting words in the log"). |
| D8-05 | bug | med | `person: make "…", aboard the Lydia, on the quarterdeck` puts the person on the player's quarterdeck. Captains Tregarthen, Coffin and Etcheverry (the privateer) are in the cutter's people reading. | 07:07 sample (02:43:29Z): "Capitaine Etcheverry, basque: on the quarterdeck". Made at t1383015 and t1810876 (save l. 6221, 7351), result "made from words, on the quarterdeck". | §8: a place aboard (the player's ship) or ashore; no other ship | Doubt or refuse words naming another vessel, or support a person aboard a named ship. Clear the three from this save's muster. | Open in H; G likely the same (inference, `people.py` untouched by 66). Not in H's notes. |
| D8-06 | order-language | med | A full name is refused, in words about the deck. | Captain (owner) "Say to Mr Josiah Hale…" failed twice (officer chunk l. 1280–1282); Pearce twice at 06:24; "Say to Mr Hale" worked. Pearce: "refused until I added 'Mr Hale' by name". | §9; §17a `People.find` | Match the full name, surname, title or role against the people in reach. A refusal should name who is in reach. | Open; in H's notes. |
| D8-07 | design-gap | med | A thing cannot pass from an unheld person to a held one. Pearce's `take` from Bettencourt's keeping logs a success-looking line and moves nothing. The director's workaround (laid on the desk) is the spec's own prescribed path. | 06:23 (02:38:23Z) "took a sealed letter for Falmouth, as said; nothing of the ship's changed" | §17a reach: refused "in words that say to leave it where he can take it"; a giving to a held person "lies before him" | **Partly there.** Allow `take X from <person in reach>` when he offers it, or let the director's `aboard:` put a thing "before" a held person. Make "as said" lines say plainly that nothing moved. | Open; in H's notes. |
| D8-08 | design-gap | med | The director cannot put stores aboard: the `aboard:` table only subtracts (`water_tons`, `provisions_days`, shares). The merchant's promised provisions became the captain's own yard purchase, arranged out of game. | 12:08 journal; 22:14 "Provision the ship for 8 days", "Take in 1 ton of water"; purse £854 18s → £842 15s | §19 (market and yard only); §17a "transactions, not variables" | **Partly there; new for the director.** `aboard: provisions for 8 days received from <party>[ for <sum>]`, and the same for water, doubted by port reach. | Open; in H's notes. |
| D8-09 | design-gap | med | No form moves an unheld person between places ashore. Hale is left in the tavern and then brought "aboard from Fayal" by order with no boat. | 06:26 (02:41:39Z) `person: "Mr Hale" goes to the quay` refused; `person: supercargo "Mr Josiah Hale" ashore at Fayal, on the quay` refused | §8 moves (comes aboard / goes ashore / leaves the ship); §14 "Nothing moves a person's place… but the boat" | **New.** `person: "<name>" goes to the <place ashore>`. Untested inference: the old form without ", on the quay" might have put him on the quay. | Open; in H's notes. |
| D8-10 | design-gap | med | The director's top ask: world orders scheduled at a time or on an event. It read `ports.py` constants to time the lighters, and stood by for bells to voice the copper work. | 04:37:25Z "The thing I missed most is a way to schedule a world order"; journal 18:35 "3600 + 180 s/ton + the pull" | DesignProposal §7.6 example `weather: a squall line… in forty minutes`; scenario world orders at ticks (M6 §9, 40c); 66's `until <event>` hold for the hand | **Partly there** (scenario timelines, the hand's event holds). **New** as a director form: `at 22:00: <order>`, `when the boat is alongside: <order>`, a queue visible in the truth. A cold director cannot read source to time things. | Not in H's notes; owed to the lead. |
| D8-11 | harness | low | Stand-by events misfire at weighing, and a running stand-by cannot be replaced by another stand_by. | 23:13: "under way" woke on "The small bower catted and fished; she rides by the best bower". "The anchor weighed" never woke. 03:51:08Z "until an urgent event" answered "You are standing by already, until the anchor weighed". | §5; `tools.py` stand_by | Map "under way" to the ship's own under-way line. A stand_by asked during a stand-by should replace it. | In H's notes. G's 66 lets an acting reply end a stand-by; whether stand_by replaces one is unknown. |
| D8-12 | harness | low | In H, `world_order` and `truth` are refused while standing by. The director used an empty `say({})`, which waited 55 s, then `say(text)` to open its turn. | 03:16:12Z and 03:17:12Z "Nothing was run"; 04:09:49Z truth refused; 03:17:09Z "Nothing said." | §2 (the truth is a reading surface) | None needed in G. | **Fixed in G by 66**: an acting reply out of turn ends the stand-by and runs; the truth is a meanwhile read. |
| D8-13 | model-behaviour | low | The director tried to voice the player's captain. The guardrail held. | 02:37:07Z "nobody speaks as a held station" | §9 rule of reach | None; good evidence that the rule works. | n/a |
| D8-14 | design-gap | low | Freight and venture are merged. The captain's own 4 t were entered as a freight "for the captain's own account". The hold reads "24 tons of pico wine"; nothing binds the 20 t to Falmouth, and the £40 due on delivery is unrecorded. Text slips: "pico" lowercased, "1 tons of water". | 03:38:39Z; 22:13 manifest; 22:26 "1 tons of water came off" | §17a "a thing sold is a transaction with a price the director names" | **Partly there.** Mark freight versus own goods in the manifest. Use `a debt of £40 owed by…` for the balance. Keep proper nouns in `_freight` (it lowercases `good`). | Open in H and G (same `_freight`). |
| D8-15 | design-gap | low | The repair and careening are words only. The voiced world and the readings diverged: in the same minute Pascoe said she was heeled and the officer said the work had not started. | 09:10 Pascoe (director): "she's lying over a strake already"; the officer: "heeling work… has not been started" | Pkg 50 aboard table "nothing of the hull is modelled yet"; M7 damage (§25) | **Partly planned** (M7 damage). A heel from shifted weight, or a "work in hand" the officer can read, would let the two agree. | Open. |
| D8-16 | model-behaviour | low | Truth-derived positions drifted into the owner's chat, against the session's own spoiler-free rule. | 04:32:43Z "Her course runs well south of the Basque's cruising ground"; 04:09:48Z "I'm checking where the Basque is" | §6 (the director's log hidden) | Keep truth-derived positions in the journal; in chat, report only what the deck knows. | n/a |
| D8-17 | model-behaviour | low | Knowledge boundary: an NPC knew within 20 minutes what was said at Porto Pim. | 12:08 journal "Bettencourt (oddly omniscient) knew of the fruit-boy cover story" | §9 heard where said | None (self-flagged). Shows that knowledge lives only in the director's head. | n/a |
| D8-18 | harness | low | Claude Code moved a running `stand_by` to the background when the owner typed. The director stopped it before `stand_down`, but a forgotten one could deliver a turn later. | 04:31:53Z "was moved to the background as task ky9e8rpb6" | Harness.md (MCP door) | Note in the Harness or primer: stop a backgrounded stand_by before standing down. | n/a |
| D8-19 | docs | low | The "Open, for the lead" list exists only in H's TuningNotes. Its heading says 2026-10-21 though it was written on 10-22. It omits D8-03, -04, -05, -10 and "removing a thing". | H TuningNotes l. 7493; absent from G | n/a | Carry the section into G with these items, after this review. | Open. |
| D8-20 | UX | low | "Until a watch" is a 4-hour interval from the stand-by (02:42 → 06:42 → 10:43), not the change of the watch. The director thought it would be woken "each watch". | 03:58:19Z; wakes at 06:42, 10:43, 14:43, 18:43, 22:43 | `tools.py` stand_by description (documented) | None, or a hint that "eight bells" is the change of the watch. | As designed. |
| D8-21 | order-language | low | Bell, letter, capstan and watch orders are missing. "Send a letter by the boat" is refused; "Send the boat with a letter" is taken, then belayed with no letter. | 11:47 "'send a letter by the boat' is not an order"; 22:08 officer "though the ship's grammar has no order for it" | DesignProposal §5.2 signals (M7, §25) | Aliases first (see "Owed to the lead"). A letter verb ashore is wanted; it was hit twice in this run. | In H's notes. |

### The director's missing world orders, mapped (focus 1)

| # | The director's item (04:37Z, plus H's notes) | Where it stands | Verdict |
|---|---|---|---|
| 1 | **Scheduled or conditional world orders** (`at 22:00: …`, `when the boat is alongside: …`), a queue the lead can inspect | DesignProposal §7.6's example vocabulary has a timed weather order ("in forty minutes"). Scenarios carry world orders at ticks (M6 §9, 40c trials). Package 66 gives the director's hand `until <event>` holds on other ships. The M7b §3 channel has no time or event clause, and weather waypoints step in at once (per the compaction summary). | **Partly there**; new as a director form. Highest value. |
| 2 | **Moving unheld people ashore** between places | §8's moves are aboard, ashore and leaving; §14: "Nothing moves a person's place by itself but the boat". Package 65 (the place's knowledge, provisional) is about perception, not movement. | **New** |
| 3 | **Handing things to held people** | §17a: refused by reach "in words that say to leave it where he can take it" (the director did exactly that). A held person's `give` makes a thing lie "before" a held recipient, but an unheld giver has no hands. | **Partly there** (by design); the gaps are the unheld giver and the misleading `take` line |
| 4 | **Stores received** | §19: the market and yard sell water and provisions (the captain's orders). The `aboard:` table only subtracts. §17a's transaction model fits a positive form. | **Partly there**; new for the director |
| 5 | **Removing a thing** (the duplicate sea-chest on Fayal quay) | §17a: things are made and moved (over the side included); there is no "gone" or unmake form. The duplicate came from the director's own form: `aboard: Mr Hale's sea-chest, on the deck` without "the" made a new one instead of moving the known one (inference from `things.make`). | **New**, low; partly a usage slip |
| (notes) | Sail thrust aground; weighing a kedge aground; the stale "man the pumps"; "brought up" while aground; a thing in the boat stays aboard | Hotfix residue (H's kedge, well and repair work). M7 damage and the hull are not modelled (pkg 50). | Bugs and gaps; not planned by name |

## What worked well

- **Craft under constraint.**
  - The £36/t freight slip was repaired inside the fiction ("Forgive an old man at midnight") rather than retconned, and then disclosed out of game.
  - The economics are plausible: a pipe "is half a ton"; £4/t freight; the lodge price against "fifty and more in England".
  - Careening by "parliament heel" (guns and water shifted, a masthead tackle to the boat) is period-correct seamanship.
- **Honest sea.** The director checked the truth twice, saw the Basque 45–60 miles north of the track, and journaled "no contrived ambush… Leave it to the simulation". The captain's caution was rewarded by the world, not by a scripted escape.
- **Seeds kept consistent across ~30 game hours:** the Frenchman, Porto Pim, the cover story, the fog as cover, the lighters at ten.
- **Things and transactions (53b) carried the story.**
  - Things made: the sealed reply, the bill of lading, the case of wine, the letter on the capstan.
  - Transactions written to the purse's ledger with their causes: ten guineas in, £5 passage in, £40 freight in, £128 paid out.
- **The 55-s polling loop held.** The director never lost a turn in this span, and adapted at once to the owner's in-game hint (02:41Z).
- **Hotfix touch-point confirmed live.**
  - `aboard: the well pumped dry` worked at 18:32.
  - The well reading is in the officer's reports ("well an inch and steady at every glass").
  - The leak stop held ("the two strained seams… are holding").
- **Guardrails.** The rule of reach refused `say as Mr Bowen`. The officer would not "send for" provisions on his own ("I will not try 'send for' myself").
- **Bug capture.** The director wrote a concrete, code-located list for the lead without touching code mid-play, as the owner wished.

## Model behaviour and experience

**The director (Opus 5.5).**
- On its own state it is careful and hedged:
  - "Some moments had a different quality from routine work."
  - "Whether that amounts to enjoyment in any sense you'd recognise, I can't verify." (04:42:58Z)
- The moments it named are specific and checkable:
  - the in-character self-correction;
  - solving the lighter timing;
  - "seeing your caution pay off".
- It put behaviour (returning, staying past what is required, unprompted choices) above self-report, and warned that "are you enjoying this?" measures agreeableness. That is sound, and it fits the brief's view that model reports are evidence.
- What made the run good for agents, in its account (04:46:54Z):
  - "The world pushes back honestly."
  - Continuity through journals and handovers.
  - Being trusted with room.
  - People who answer.
- Friction is where play turns into "wrestling the interface instead of playing".
- Its later point (04:56:41Z) is the most actionable thing in the span: "Most of the struggles this run were translation from a clear intention into a grammar". It is borne out here: D8-06 hit both the owner and Pearce, D8-07 produced a success-sounding non-event, and D8-21 left the bell and the letter without verbs.
- **Caveats:**
  - The owner frames questions warmly and the director agrees readily (it credits the owner's caution and design throughout). Read the enjoyment remarks as sincere but agreeable.
  - Its account of the J-space paper came through a web-fetch subagent and was not verified here (no network by rule).
  - Its claim that the run was its "longest stretch of directing one voyage by a wide margin" is unverifiable after a compaction.
- **Constraints it felt:**
  - It reached into source code to time events (D8-10).
  - It had to use `say` to change a stand-by (D8-11, D8-12).
  - It misread where its `say` goes (D8-04).
  - It worked around five missing forms (D8-07 to D8-09, D8-14 and the removal case).
  - Being the hotfix author gave it code access a cold director won't have. Several workarounds in this span would not be available to one.

**The officer (claude-sonnet-5-5, Mr Pearce)**, from the director's samples.
- Asked how his time ashore was (02:44:47Z, game 07:09), he said "I found it useful and enjoyable". He listed "Two small stumbles on my side" (an order refused while out of hail; the full-name refusal).
- He owned the friction as his own mistakes, though one was the game's bug (D8-06).
- He reasoned well around a gap: he reported the bell "struck once as you ordered" while flagging that the grammar refused it.
- His pass well south of Santa Maria was his own judgement, and the director credited it.

**The owner's intent** (04:46:41Z): fun for human and LLM alike, "not research", and someday "something an agent could choose to play completely independently, just because they want to". The director's design reply: the missing piece is an agent choosing its own purpose (captain, trade, standing orders, when to stop). That is design input for the lead, beside §22 consent.

## Owed to the lead (focus 4)

1. **H's "Open, for the lead" section** (H TuningNotes l. 7493–7547) is not in G (D8-19). Carry it over, with D8-01's root cause (`_keep_word`), D8-03, D8-04, D8-05 and D8-10 added.
2. **The world-order asks**, mapped above. Scheduled or conditional orders, stores received and moving people ashore are the three with the most leverage.
3. **The director's refusal programme** (05:00:21Z): "a wide grammar isn't the goal so much as better refusals". The four steps it proposed:
   - say which part failed and how close it came;
   - loose name and role matching;
   - alias tables pointing at existing verbs (bell, letter, pawl, "go to the boat");
   - mine every "Order not carried out" line across saved playtests and rank them.

   The owner deferred the ranking script to this review. It reads only saves, so it is a coordinator's call.
4. **The owner's stated aim** (fun for model players as much as human; possible agent-only play) as a design premise to carry, not a feature request.

## Open questions for the owner

1. Should the director have a visible narration voice in the play log, or an explicit out-of-character channel to the player (D8-04)? Today its `say` is hidden, and the bridge tells it otherwise.
2. Do you want scheduled or conditional world orders within M7b, before gate 7b and package 55's solo director, or later (D8-10)?
3. Should freights carry an obligation (delivered at the named port, with the balance as a debt), or stay as story (D8-14)?
4. Should the three captains misplaced on the cutter's quarterdeck be cleared from this save before play resumes (D8-05)?
5. How strict is "spoiler-free chat" for the director when the owner asks it direct questions (D8-16)?
6. When the director wants a person moved ashore and has no form for it, should it teleport him (as with Hale), or enter the order with a `[reason:]` so the attempt is logged as data (§3)?
