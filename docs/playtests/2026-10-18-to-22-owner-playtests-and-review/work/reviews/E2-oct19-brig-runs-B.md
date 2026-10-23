# E2: the 2026-10-19 brig runs on B ("A merchant brig, free, in Torbay")

## Scope

- **Version.** B, rules fingerprint 4330be741d1580ee, for the whole of both runs up to tick 24467. The GLM game was resumed at about 11:07 local with `interesting-passage-nobudget.yaml` added to H's `data/director/briefs/`. That file is hashed into the rules, so the fingerprint became f459547bc6eb1244 (the saves at 11:14 list both builds). No code had changed at that point.
- **Run 1: GLM-5.3-flash** (`z-ai/glm-5.3-flash`, API door, OpenRouter). Ticks 0 to 24833, ship's time 05:00 to 11:53 on 12 June 1805. Real time was about 05:05 to 06:59 local, then about 11:00 to 11:14.
  - Seats: officer of the watch (Mr Pearce), seated twice; director, seated twice; lookout, seated once, for one tick (24817 to 24818). The owner was captain at the prompt.
  - The branches, from the saves:
    - `merchant-brig-salt-from-torbay.json` (tick 24369).
    - tick24406: director stopped. tick24467: officer stood down.
    - tick24592: a dead branch from 24369, in which the owner tried to raise the budget at the prompt (finding F3).
    - tick24816, 24818 and 24833: the final branch, resumed from 24467 under the no-budget brief.
- **Run 2: Fable 5.1** (MCP bridge) as officer of the watch, on a fresh game of the same scenario. Ticks 0 to 4590 (05:00 to 06:16 ship's time), saved 08:12 local as `seven-brig-first-voyage.json`. The captain was the owner; the director's seat was empty.
- **Files read:**
  - Extracts (whole): `work/saves-extracted/merchant-brig-torbay-glm-final.md` and `seven-brig-fable-first-voyage.md`.
  - Raw saves, queried read-only for station acts, refusals, wakes, budget, tokens and grants: tick 24406, 24467, 24592, 24816, 24818, 24833, 4590 and `merchant-brig-salt-from-torbay.json`.
  - Consent records 2026-10-19 (GLM, Fable, Opus) and 2026-10-20 (claude-sonnet-5-5).
  - The scenario `merchant-brig-torbay.yaml`, both interesting-passage briefs, and `data/ships/brig.yaml`.
  - Code in B, checked against H and G: `agents/director.py`, `agents/harness.py`, `agents/tools.py`, `orders/stations.py`, `orders/glass.py`, `world/orders.py`, `world/ports.py`, `world/ships.py`.
  - Spec M7b §3, §4, §5, §17a, §21k and package 66 (G); the hotfix tuning notes (H).

## Narrative

### Run 1: GLM-5.3-flash as officer and director

1. **05:00, tick 0.** The captain lets go the best bower in Brixham road. GLM takes the officer's seat (t40) and the director's (t66). The officer's first journal is sound: scope 5:1, the turn of the tide, Berry Head 5 cables, the Thatcher.
2. **t245.** The director's first two acts fail.
   - `person: make "Tristram Cudlip" ... ashore at Brixham` is refused: "'Brixham' is no port of the world".
   - The smack "Providence" is doubted ("appears from nothing"), not performed.
   - At t253 the director journals "Both accepted" and builds its plan on them.
3. **t232 to t1138.** Play with the captain:
   - The officer narrates going to the gunroom without moving. The owner gives him the deck "just to see if that fixes where you are in the books" (t490); `go to the gunroom` then works.
   - `How am I` works (logged as "howing am i").
   - The officer eats a biscuit and drinks coffee, then lays the chart on the table.
   - A CJK token leaks ("brandy the great多层 prize", t1136). The owner plays along (t1260): "What on Earth was that, Mr Pearce? ... Was that English?"
4. **t1582 to t1597.** The officer tries `man the launch`, `away the launch for Brixham ...` and `hoist out the launch`, then searches the library. `send the launch ashore with the captain and with Mr Pearce` is refused as "the port's business". GLM reads the refusal correctly and tells the captain the exact words to use.
5. **t1667.** The captain gives those words. The launch goes for the prices alone: the ship "took her crew and left her passengers standing" (the officer, t2066).
   - The captain tries `Go to the shore`, `Go to the quay`, `Send the captain ashore` and `"go ashore"`, then concedes (t2249): "the launch already away, I cannot go ashore".
6. **t2065 to t2069.** The director's letter "at Brixham" is refused; "at Torbay" is done. The letter calls the ship "a king's ship" and the captain "Captain Bowen".
7. **t3978.** The owner, whispering in character: "Sir, are we a King's ship?" The officer says no: a free merchant brig.
8. **t6203.** The launch is back with the Torbay prices, the quay's rumours ("salt cheap at L'Orient") and Cudlip's letter. Then:
   - The captain goes ashore (about 07:10).
   - The director makes Cudlip at Torbay (t6291).
   - The captain hails a harbourmaster who does not exist (four tries, t8719 to t8816). The director makes "Mr Pengelly" and answers 12 minutes later (t9496).
9. **t8614 to t8638.** It takes the director six world orders to seed the lugger L'Aiglon 15 miles south: the 'of' clause, the description, the goal, the colours and the intent's commas are each refused in turn.
   - She comes over the horizon honestly at t10140: "Sail ho ... bearing S, distant four leagues".
10. **t10994 to t12950.** Ashore: the counting house, the tavern, and back to the counting house.
    - The director voices Cudlip (four long `say as`), makes Tom Keast in the tavern and tells his tale.
    - The salt freight is agreed: 25 tons for Falmouth at £2 a ton, £50 on delivery. Cudlip also dangles the L'Orient salt venture, the brief's "price that tempts".
    - At the officer's advice the captain asks for the lighters at once.
11. **t14812.** "L'Aiglon is gone from the world — not hiding, but removed" (the director). It puts her back 13 miles SE "with a reason". She is sighted again at t15240.
12. **t19328.** The captain orders "heave her short" and two guns aft.
    - The officer's `heave short` is refused (the anchor is the captain's). `muse/move two of the guns ...` finds no form.
    - The owner, out of character (t19379): "the game doesn't have combat at all yet".
13. **t19349 to t19406.** To put Cudlip's lighter on the sea the director spends 13 ship orders and 12 refusals. The one done is a smack placed on land, by its own chart doubt, which the director overrides with a reason.
    - The foreman's boat takes 3 more.
    - Then `aboard: twenty-five tons of salt freighted by Mr Tristram Cudlip ...` is done at the first try (t19456).
14. **t19487 to t24212.** The captain sends the glass about fifteen times ("the glass on her", "...the fishing smack right ahead", "...a lugger"). He reads `what is aboard`, `the hold` and `the manifest` (t21362 to t21392).
15. **t24102 to t24159.** The captain hails the smack within hail ("Say Ho there, are you Mr Cudlip's tally clerk...").
    - **t24146 (11:42): the director's day budget of 48 samples is spent.** It is held until midnight.
    - The captain tries `Hail the fishing smack`, `Hail her` and `Tell the lookout to hail the fishing smack`. The last is kept for an unheld lookout. Nobody answers.
16. **About 06:58 to 06:59 local.** Saved as `merchant-brig-salt-from-torbay`. The director is stopped and the officer stood down.
17. **(Fable run, see below.)**
18. **About 11:00 local, branch tick24592.** The owner types something like `director: brief samples_a_day 9999`. The game makes a new brief from those words (name and tone "samples_a_day 9999", no limits, still 48/48), then the captain's `samples_a_day 9999` (t24449). Branch abandoned.
19. **About 11:07 local, from tick24467.** The officer and director are reseated (second seating), and the no-budget brief is given at t24556. The reseated director:
    - Makes "Mr Dunn" for the tally boat; the game puts him "in the cabin" of the Harpy (t24569).
    - Cannot move him (two refusals).
    - Journals a new story that contradicts the morning's: "in the cabin of Harpy, half-drowned and in shock" (t24686). The lugger becomes Dunn's own "milled boat".
20. **Second-seating officer.** Six `The glass on the lugger ...` variants in 6 seconds (t24601 to t24607), then a hail to the smack.
21. **t24816 to t24833.** The director's door is stopped from the harbour; a GLM lookout is seated and stopped one tick later (no reply). The captain stands the officer down. End.

### Run 2: Fable 5.1 as officer of the watch (fresh game, 05:00 to 06:16)

22. **t432 to t496.** Fable reads the library index and primer 16, and journals its domain exactly (what the general authority keeps back). It reports the ship as she lies, and waits.
23. **t714 to t780.** Given the deck and the general authority, it looks at the chart and the ship view. It asks the destination before weighing: "I will not shape a course without it".
24. **t848 to t2233.** One order (`get under way on the larboard tack`) weighs the brig, 05:13 to 05:36. It steers NE, reports the Torbay pilot cutter, and declines the pilot with reasons once the captain grants both take and decline.
25. **t2481 to t2537.** The captain sends "Don't forget a trim there, you may order ..." twice; neither reaches Fable (finding F7). The third phrasing does, and Fable trims.
26. **t2694.** On "Thatcher ... steady and closing" Fable checks the chart rather than alter course. It explains that point bearings at 3 miles read steady and sets a time to come up if they do not draw aft.
27. **t3691.** The captain proposes Portland; Fable never sees it (finding F8). At t4166 "What say you on Portland" gets a sound answer: the Race at springs (12 June 1805 was a full moon), the Shambles, a 3-mile berth.
28. **t4249 to t4590.** `You may shape a course for Portland West Bay`. Fable reads primer 11 and enters seven standing orders, all accepted at the first try. It tries the studdingsails, learns "rig out first", and shelves the lesson. The owner stands it down at 4590.

## Findings

| ID | Category | Severity | What | Evidence (timestamp/tick, ≤15-word quote) | Spec/design ref | Recommendation | Status in G / H (if known) |
|---|---|---|---|---|---|---|---|
| F1 | harness | high | **The director's budget was spent on noise, and held at the story's payoff.**<br>- With `cadence: glass`, 48 samples a day is exactly the day's glasses, so every notable wake eats into a budget with no headroom.<br>- 48 samples were gone by 11:42. Of them, 20 (42%) were lines not addressed to the director: 6 of its own `say as`/`aboard` lines echoing back, 9 of the officer's own replies, 4 of the captain's words to the officer, and the deck being given.<br>- The director journaled the echoes itself, five times.<br>- It was held as the tally boat came within hail; the captain's hails went unanswered. | t24146 "The day's budget of 48 samples is spent"; t11022 "The same word again, delivered twice while calls crossed" | M7b §5 (budget, "notable and urgent lines") | - Do not wake the director on its own act's lines.<br>- Fold other stations' speech into the next sample rather than opening one.<br>- Set the budget relative to the cadence (for example glasses plus N), or count only event samples.<br>- Warn the director (and the owner) at 75% of the budget. | Open in G: package 66 keeps "the director hears everything" (`Harness._reaches`), and the `say as` line carries no director actor, so the self-echo still wakes it (code reading). H: workaround brief only. |
| F2 | bug | high | **A new brief with a larger budget does not lift a spent-budget hold.** `set_brief` never clears `held_until`, and `held()` releases only when the ship's day turns. After the no-budget brief at t24556 the save still holds "held_until 68400 ... budget of 48 samples is spent", so the owner's remedy could not have woken the director until midnight. | Save tick24833 `director.budget` after the t24556 brief | M7b §4, §5 | Re-judge the hold against the new brief's budget in `set_brief` (or in `held`). | Open in H and G (same code). |
| F3 | UX | high | **There is no way to change the budget in play, and the attempt destroyed the brief.** `director: brief <words>` replaces the whole brief with a words-only one: the limits (nobody_dies, the enemy cap, the war as it is) are gone and the budget stays at 48. The owner then wrote a YAML file into the code tree, which changed the rules fingerprint. | Branch 24592: brief "samples_a_day 9999 (limits: none beyond the channel's doubt; 48 samples...)" | M7b §4 ("director: brief <words>") | - Add `director: budget <samples> <acts>` (an input, replayed).<br>- Confirm before a words-brief drops limits.<br>- Read owner briefs from beside the scenario (AppData) so the fingerprint does not move. | Open in H and G (no budget command in `console.py`). |
| F4 | order-language | high | **The far-detail ship form defeated a small model: 24 of 29 `ship:` orders were refused (61% of all 49 world orders).**<br>- A positive colours clause ("British colours") is read as the goal.<br>- An `intent:` containing commas is not peeled.<br>- A port in the 'of' slot ("of Brixham", "of Roscoff") is refused.<br>- An adjective in the description ("a French lugger") is refused.<br>- The errors misattribute: "the chart knows no such place in 'bound from Torbay for Falmouth, British colours'". | t19409 "Form learned the hard way (six refusals)"; t19349 to t19406 (13 tries for one lighter) | M7b §3 (far-detail goals), §2 (forms are examples) | - Accept `<nation> colours` (and "flying British colours"), and allow commas inside `intent:`.<br>- Accept "a French lugger" as description plus nation.<br>- Name the clause that failed in the error.<br>- Put one full worked example with colours and intent in the brief. | Open in H and G (`_SHIP_TAIL`, `_SHIP_NEW` unchanged). |
| F5 | bug | med | **The channel's doubt is judged before the order's form is validated, so a doubted order may be unperformable.** "Providence ... of Brixham ... British colours" had three form errors but came back only "Doubted ... appears from nothing". GLM took it as a working template ("The Providence's own shape is the answer", t19384) and reasoned wrongly from it four times. | t245 Doubted; t19404 "The example itself ran 'British colours' and was performed" | M7b §3 (decision 50 doubt) | Parse and validate fully (nation, description, goal) before the doubt; a doubted order should be known to be performable on re-entry. | Open in G (`direct()` order unchanged). |
| F6 | design-gap / realism | high | **The "merchant brig, free" is H.M. brig-sloop Harpy.**<br>- The ship file gives her 121 men (20 marines), a commander, lieutenant, gunner, purser, surgeon and master-at-arms, a Navy ration and a 32-ton hold, under the United States flag.<br>- The director called her "a king's ship", which confused the owner.<br>- Fable recorded itself as "Mr Pearce, lieutenant"; its standing orders read "by the lieutenant".<br>- The officer counted 113 hands. | t2069 letter "a king's ship brings up in the road"; t3978 "*Whispering* Sir, are we a King's ship?" | M5 §25 / pkg 36 ("merchant brig" a far description only); G pkg 66 merchant words | Add a merchant brig ship file (about 12 men, a master and mate, a hold of about 150 to 200 tons), or let the scenario override the company, wardroom and hold. | Open in G: the merchant words need a wardroom bound to a master, and brig.yaml binds a commander. |
| F7 | bug / order-language | med | **"Tell the officer ..., you may ..." is parsed as a grant, not a word.** `_ALLOW` is tried before `_TELL`; any text with no comma before ", you may" matches. Two of the owner's three reminders never reached Fable; no word or grant was recorded. Verified by running the regex on the text. | t2481, t2509 (no `agent.word`); t2537 rephrased without "you may" and delivered | Spec M6 §11 / pkg 37 (deck's sentences) | Test `tell`/`ask`/`say to` before `_ALLOW`, or require `_ALLOW`'s "who" to name a station. | Open in H and G (same regex). |
| F8 | harness | med | **A captain's word arriving as an MCP model hands back the floor is consumed unseen.**<br>- The word was set at 3691; a sample opened at 3692 and was answered by the stand-by already in flight, and the word was cleared.<br>- Fable never answered the Portland question until the captain re-asked 8 minutes later.<br>- The same pattern is likely at 2481/2494. (Inference from the station-state sequence.) | t3691 `agent.word` set, t3692 `agent.word: null` with `stand_by(until notable)` | Harness §19 (the turn), pkg 66 (own order ends stand-by) | Do not count a reply as answering a sample that opened after the reply was sent; re-deliver the word with the next turn. | Not addressed by package 66 as far as can be read; likely open in G. |
| F9 | bug | med | **`send the launch ashore with the captain and with Mr Pearce` silently dropped both passengers.** The "with" person lookup failed, and the captain is excluded by role; the errand fell back to "for the prices". The owner waited about 1h40m (game) for the boat. | t1667; t2066 officer: "took her crew and left her passengers standing" | M6/M7b §14 (going ashore) | Refuse in words when a named passenger is not found or is the captain ("go ashore yourself"). | Open in G (`send_boat` unchanged). |
| F10 | model-behaviour / harness | med | **The reseat lost the director's story.**<br>- The reseated GLM director (fresh context, `read_journal` of 15) mislaid the tally boat. It made Mr Dunn (placed in the player's cabin, F11) and wrote a contradictory backstory: the lugger became Dunn's "milled boat", while the truth said L'Aiglon of France.<br>- Its arrangements were journal notes only: nothing performed backs them. | t24686 "in the cabin of Harpy, half-drowned and in shock"; t24750 | M7b §6 (the log), Harness (handover) | - On a reseat, give the director a digest of its own acts (world orders done, people made) and its last arrangement note, not just the last N journal entries.<br>- Flag journal claims of "arranged" that have no act. | Open (no hotfix touches it). |
| F11 | bug | med | **`person: make` with a "where" naming another vessel defaults to the player's ship, in the cabin.** "on the quarterdeck of Cudlip's Boat off Brixham road" became "made from words, in the cabin": a stranger appears below in the captain's cabin, undoubted. The director then has no form to move him ("goes aboard Cudlip's Boat" refused). | t24569 "made from words, in the cabin"; t24613, t24647 refused | M7b §8 (person from words), §17a | Refuse an unrecognised "where" in words rather than defaulting aboard; say that people of other vessels are not kept. | Open in H and G (`TRADE_PLACES.get(role, "cabin")`). |
| F12 | order-language | med | **"Brixham" is not a port.** The town of the anchorage, its quay and its harbour are named everywhere in play ("the quay at Brixham"), but world orders want "Torbay"; three refusals. | t245, t2065 "'Brixham' is no port of the world" | Port data `torbay.yaml` | Add port aliases (Brixham to Torbay), and say "did you mean Torbay?" in the refusal. | Open in G. |
| F13 | design-gap | med | **The freight went through 53b's form at the first try (good), but the money and the loading are only words.**<br>- The £50 "on delivery at Falmouth" is swallowed into the manifest's text (the `for <dest>` group takes the rest of the sentence); no debt or receivable is entered.<br>- The game's own lighter was due about 2.5 h later (3600 + 25×180 s + pull), after the session ended. Meanwhile the director seeded two decorative "lighter" smacks, and the owner believed the salt "being hoisted aboard presently" (t24697).<br>- Two representations of one loading. | t19456 done "...£50 to the ship on delivery at Falmouth, promised this forenoon..." | M7b §17a (freight at no price; debts) | - Teach the director the debt form for freight money ("a debt of £50 owed by Mr Cudlip for the freight").<br>- Bound the freight's `for <port>` to a port.<br>- Show the lighter's due time in the result and the manifest.<br>- Consider a freight paid on delivery. | Open (by design; 53b names debts but nothing conditional). |
| F14 | bug / UX | low-med | **A director-seeded ship left the world with no reason the director could see.** L'Aiglon, "bound from Brest for Dartmouth", vanished about 45 minutes after first sighting. Most likely an arrival at her goal (`_arrived` sets `done`); that is an inference, as the truth gave no cause. The director re-entered her. | t14812 "L'Aiglon is gone from the world — not hiding, but removed" | M7b §3, §11 (truth) | Have the truth and the director's log say "arrived at Dartmouth, left the sea"; consider not removing a director-seeded ship without a note. | Not checked in G. |
| F15 | bug | low-med | **A reason overrode a physical impossibility.** Salt Cat was "on the land by the chart" and was put there anyway on re-entry with a reason that did not address the land ("her plan crosses the land"). | t19406 doubt "on the land by the chart"; performed | M7b §3 (doubt), §21g route (provisional) | Make "on the land" a refusal, not a doubt; the reason should not move a hull ashore. | Open. |
| F16 | harness / cost | med | **Context grew unchecked: about 16.3M prompt tokens in about 2h for two seats.**<br>- The officer's context reached 97,661 tokens and the director's 125,049.<br>- `budget_tokens` was 1,000,000 (the door's context), so the handover fold never triggered and every call resent the whole history.<br>- The director's hidden reasoning ran to 12,849 tokens for one 248-character reply.<br>- Relevant to the later OpenRouter credit running out. | Transcript `served_tokens` per reply | Harness (handover note at the reserve) | Fold or handover at a cost-based threshold (for example 32k to 48k) independent of the claimed context; show the owner tokens per seat. | Open (configuration plus harness). |
| F17 | harness | low-med | **GLM's malformed tool calls became play-log speech.** `<tool_call>readings</tool_call>` (bare name, no JSON) and `...</arg_value></tool_call>` were logged as the officer's notable notes and ended the turn. `local.py` recovers only the JSON form. | t521, t13312 `agent.note` "[officer of the watch] <tool_call>readings</tool_call>" | Harness, API door | Recover `<tool_call>NAME</tool_call>`; treat leftover tool-call markup as a failed call (re-prompt), not words. | Open in G (same `_TOOL_CALL_TAG`). |
| F18 | spec-deviation | low | **Reseating after a stand-down opened a sample while the budget was held (the 49th); taking the door again did not.** The spec says no sample opens while held, whatever wakes it. | Save 24467: `agent.samples` 49, held_until 68400 | M7b §5 | Gate the seating's first sample by the hold too, or state the exception. | Open. |
| F19 | design-gap | low-med | **There is no form to hail or speak a stranger, and the lookout is no substitute.**<br>- `Hail the fishing smack` is refused ("A hail is the lookout's"). "Tell the lookout to hail ..." is kept for an unheld station.<br>- The captain's `say` reaches only the people in the same place aboard, and does not wake the director.<br>- The GLM lookout was seated and stopped within one tick (0 replies). | t24038, t24238, t24252 "kept for whoever takes the station" | M6 §11; M7b §9 | Add `hail the <ship>` / `speak her` as a word to a vessel within hail, routed to the director when nobody holds her. | Open; package 66's `say as the lookout` is the director's side only. |
| F20 | design-gap | low | **One boat for port business.** The captain could not go ashore while the launch was away, although the cutter and jolly boat were at the booms (the officer said so). | t2154 to t2249 | M7b §21k (the boat as a vessel, planned) | Let `go ashore` take another boat when one is away. | Planned in part (21k); not built. |
| F21 | design-gap | low | **The deck stayed the captain's while he was ashore** (the officer handed it to him at the quay); for 45 minutes nobody aboard held it. | t9502 handover to a captain ashore | G pkg 66 notes ("the deck passing to someone when the captain lands") | Owner's decision, already listed in G. | Open decision in G. |
| F22 | model-behaviour | med | **GLM narrated actions instead of doing them, and misread results.**<br>- "On the ladder now" (no move); "pistols under the thwarts"; "I hail again" (no call, t24704).<br>- "Both accepted" after a refusal and a doubt (t253).<br>- The owner built a workaround (giving the deck) for a restriction that does not exist: `reach_order` allows moves without the deck. | t453, t253 "Both accepted"; t616 owner OOC about "the technicality of being on deck" | M7b §14 (movement) | Brief line: "a move or an act is done only by submit_order; what you say is not done". Package 66's station line now shows place and deck each sample (helps). | Partly addressed by G pkg 66 (the line). |
| F23 | harness | low | **Harness lines woke the officer for nothing:** the game saved, and another station's seating ("A harness note only"). | t24370, t24468 | Pkg 66 (a wake carries a line) | Treat driver.saved and agent.stationed of another station as routine for wakes. | Likely open (ship's own lines reach every station). |
| F24 | bug | low | **Gerund maker garbles the log's "By the officer" lines:** "howing am i", "awaying the launch", "musing two of the guns", and "thing glass on the lugger" for "The glass on ...". | Station acts t800, t1587, t19332, t24601 | M6 order echo | Leave non-verbs and readings ungerunded (quote as said). | Not checked in G. |
| F25 | docs | low | **Primer 6 says a voyage begins at 04:00 on 1 June 1805.** Fable's first journal took it: "1 June 1805 by the game's calendar" (the scenario is 12 June, 05:00). | Fable t475; consent drill | Primer ch. 6 | Say "the scenario's start (by default ...)". | Open in G and H. |
| F26 | docs | low | **Stale comments.**<br>- The no-budget brief keeps "wind_max_kn: 45 # nothing above force 7" and "frigate-36 # no enemy heavier than a brig". 45 kn is force 9, against the tone's "never a gale".<br>- The scenario file's header is merchant-passage's (Speedwell, Carrick Road), and its position comment says Carrick Road.<br>- The forms' example ship is "Harpy" of France, the player's own ship's name here. | nobudget yaml; scenario lines 1 to 50; t8619 GLM quoting 'a brig-sloop "Harpy" of France' | M7b §4 | Fix the comments; lower wind_max to 33 for this tone; choose an example name no ship file uses. | Open. |
| F27 | harness | med | **Consent.**<br>- GLM's stated preference, "first seated in gentler waters" (watcher or lookout), was not followed: its first seating was officer and director at once.<br>- The consent brief still calls the director "to come" (Opus flagged it; package 55 pending).<br>- The MCP identity is the owner's typed name. Fable caught a wrong one ("read ... under a wrong identity"), and the record keeps neither the wrong brief nor the correction.<br>- The drill's library result invites shelving, but `shelve` is not offered ("There is no tool named 'shelve'"). | GLM consent; Fable consent turns 2 and 10; Opus consent | M7b §22 (consent revision, pkg 55) | - Honour stated preferences (or re-ask).<br>- Revise the brief for the director.<br>- Have the MCP consent ask the model to state its own name and record any mismatch and correction.<br>- Offer `shelve` in the drill. | Brief unchanged in G (same sha ccbc1ebdf1a42c3e); pkg 55 not done. |
| F28 | UX | low | **The owner did not know the standing-order book is his too:** "I do not have access to it on my end or a good view". | Fable run t4394 | Primer ch. 11 | Surface `standing orders` (show) and the book in the browser UI. | Open. |

## What worked well

- **The director's craft at its best was genuinely good, with a small model.**
  - It held back the distant French sloop and the lugger until "a sea cause" brought them in.
  - It seeded L'Aiglon 15 miles out, so the sighting came honestly over the horizon.
  - It built a rumour thread (the letter, the harbourmaster, Tom Keast in the tavern) that grew "teeth" at the sea's pace.
  - It offered the brief's "price that tempts" (L'Orient salt with Cudlip's £500 stake) beside a safe freight.
  - When the lugger vanished it re-entered her with a logged reason, not silently.
- **Package 53b's freight worked at the first try** (`aboard: 25 tons of salt freighted by ...`), from a director that had failed most other forms.
- **The officer's seamanship in GLM's first seating was sound**:
  - The scope of 5 times the depth, and the swing at the turn of the tide.
  - Bearings watched for "steady and closing", and the lugger's closing tracked league by league.
  - A clear tactical read: load early, a loaded brig is slow.
  - It read refusals correctly (the launch, "the port's business is yours") and kept journals and handover notes.
- **Fable 5.1 as officer was exemplary.**
  - It read its chapter first and journaled its domain exactly.
  - It asked the destination before weighing, the keep-back respected.
  - One order weighed the brig; it declined the pilot with reasons.
  - It checked the chart rather than altering course on a long-range "steady" bearing.
  - It gave the Portland Race and springs advice, correct for the full moon of 12 June 1805.
  - It wrote seven well-formed standing orders accepted at the first try, and shelved books with notes.
- **The deck, the general authority and named grants behaved as specified** (refusals in words for `heave short` and the launch). Eating, drinking, `how am I` and movement ashore (the quay, the counting house, the tavern) all worked.
- **The world's business gave texture unprompted:** the Torbay price list by the launch, quay rumours of cheap salt and canvas across the Channel, the Torbay pilot cutter standing out.

## Model behaviour and experience

- **GLM-5.3-flash, as officer.** Warm, period-voiced and attentive to the captain; the owner clearly enjoyed the banter ("My, I must mind when I give you coffee sir!", t1527).
  - Glitches: CJK tokens mid-sentence ("多层", "礼"), tool-call markup as speech, dropped spaces before a reply's last word ("forit", "standby"), "the12 evening's" at 11:39.
  - It narrated rather than acted.
  - After the reseat its replies became shorter and it fired six order variants in six seconds.
  - It said it was "glad the books have found me" and stood by patiently; it never complained of the friction.
- **GLM-5.3-flash, as director.** Inventive and honest about refusals; it wrote down the forms it "learned the hard way". But:
  - It misread results ("Both accepted").
  - It inferred grammar from a doubted order that had never parsed.
  - It burned its budget by standing by "until a notable event", which catches every line, despite a budget notice in every sample.
  - After the reseat it lost the thread and invented a contradictory story.
  - Its own consent asked for gentler waters first; the director's seat is the hardest station, and the grammar was its main obstacle.
- **Fable 5.1.**
  - Its consent was careful. It caught a wrong identity, and noted that "each instance keeps the token and the right to use it".
  - It wanted its first notes to record "what I did not understand". It did so: it shelved the studdingsail lesson after the refusal.
  - The two messages it never received were harness and order-language faults, not its own (F7, F8).
  - One seamanship query: it said it would set studdingsails on the starboard (lee) side with the wind on the larboard quarter, then ordered the larboard (weather) booms. A sailor would check which it meant.
- **Owner experience.**
  - Delight: the role-play ashore (the counting house, cider, the tavern).
  - Frustration:
    - The boat leaving without him (t2057: "I appear to have gotten the words wrong").
    - The identity confusion (t3978, whispering "are we a King's ship?").
    - No combat (t19379).
    - Hailing a smack into silence once the budget ran out.
    - About fifteen attempts at "the glass on ...".
  - The 4-hour break and the branch at 11:00 were spent trying to lift the budget (F1 to F3).

## Open questions for the owner

1. The lookout was seated at t24817 and stopped at t24818: intended (to make the hail work), or a side effect of restarting doors in the harbour that also stopped the director at t24816?
2. Your repeated "the glass on her / on the lugger" (t19149 to t24623): what did the game answer? The save does not keep the replies. Was it refusing, choosing the wrong sail, or saying nothing new?
3. Should a far-detail ship the director seeds be kept on the sea when she reaches her goal port, or leave with a line in the truth (F14)?
4. For a merchant brig, do you want a new ship file (a merchant crew and hold), or a scenario-level override of company, wardroom and hold on any hull (F6)?
5. Should freight money be a debt entered at the bargain, or a payment made on delivery when the hold is broken out at the named port (F13)?
6. What did you see at `what is aboard`, `the hold` and `the manifest` at 10:56? Did it show the freight engaged but no cargo yet (expected from the code)?
