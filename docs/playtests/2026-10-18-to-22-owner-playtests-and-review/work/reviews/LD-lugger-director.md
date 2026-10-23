# LD: the lugger director ("Freesail-director setup")

## Scope

- **Session:** the Claude Code session "Freesail-director setup", 2026-10-22 05:51:13Z to 09:45:52Z (about 3 h 54 min of wall clock). Opus 5.5 held the director's station through the freesail-director MCP tools.
- **Game:** "A fishing chasse-marée in Roscoff" (the *Éclair*), from 1805-06-10 05:00 to 1805-06-12 05:03 (end tick 172994; the director was seated at t59 and stood down at t172959).
- **Version:** G, rules fingerprint e19ddb854219fbd8 (the save's build line says `m6c`, `e19ddb854219fbd8`). G includes package 66.
- **Seats:** the owner was captain (Mr Hervé, at the prompt). Another Opus 5.5 session was officer of the watch (Mr Lecoq). The director was this session.
- **Brief:** the scenario's own inline brief "A Nice Day for Fishing". It is not one of the starters in `data/director/briefs/`. Tone: "a quiet day". Challenge: "Nothing much, at least at first". Limits: wind 60 kn, a frigate-36, nobody dies, the war and the chart as they are. Budget: 9999 samples and 9999 acts a day, which is in effect no budget.
- **Read in full:** `work/condensed/lugger-director.md` (3,494 lines, about 431K characters) and `lugger-director.user.txt`.
- **Read in part:**
  - `work/saves-extracted/lugger-fishing-final.md`: the director's acts, the doubts, the haul, Le Gall, the end.
  - `C:\Users\frenc\AppData\Roaming\FreeSail\scenarios\lugger-roscoff-fishing.yaml`.
  - TechnicalSpec-M7b §2–§9, §14–§15, §17a and §21a.
  - TuningNotes "Package 66".
  - Primer chapters 20 and 21.
  - M7b-WorkPackages rows 51, 57, 58 and 65.
  - Targeted code in G: `business.py` (the goal), `orders.py` (the ship form), `weather.py` (`pressure_at`), `ui/server.py` (`_ease_for_station`), `api/readings.py` (the tide), `data/evolutions/get_under_way.yaml`, `haul_nets.yaml` and `data/crew/names.yaml`.
  - A few greps of `lugger-officer.md` and `director-hotfix.md`, for counts only.
- **Not done:** no FreeSail tool was called. Nothing was run but read-only greps and inline counting.

**Counts** (condensed transcript and save):

| What | Count |
|---|---|
| `world_order` calls | 41 |
| Performed | 25 (24 given and 1 re-entered with a reason) |
| Not performed | 15: 7 "no way as said" and 8 logged as attempted |
| Doubted | 1 |
| `say as` orders | 11 |
| `stand_by` calls | 264 |
| `stand_by` calls that returned "Still waiting" after 55 s | 192 |
| `truth` reads | 8 |
| Journal notes | 40 |
| Questions put to the director by unheld persons' askers | 7 |

## Narrative

- **05:51Z (game 05:01).** The director read the brief and the truth, and journaled a plan: "I will do little ... nothing hostile". It asked the owner three questions. It flagged three oddities: every ship "bound for Falmouth", no fresh-fish price at Roscoff, and the readings say flood where the truth says ebb.
- **05:54Z.** The owner said he is captain, an Opus 5.5 holds the officer's station, "direct however you see fit", he won't watch the chat, and the director should stay on stand-by.
- **05:54–05:56Z (05:04–05:05).**
  - `port roscoff: price of fresh fish 9` was refused; primer 21 then showed the fish quay exists.
  - Five tries to put a Roscoff lugger, the *Petite-Jeanne*, out of the harbour all failed (F-07). It gave up: "Not worth forcing on a quiet morning".
- **06:00Z (05:14–05:34).**
  - The captain sent Lecoq ashore to ask where the fish are. The director made **Mère Kerbrat**, a fish-wife on the quay.
  - Her answer pointed them west to the Iroise and the soundings off Ushant: "beat out ... on the ebb ... shoot your nets at dusk". This gave the day its goal.
- **06:06Z (06:36).** It appended a high ("the ridge") with two waypoints. The aim was to make the rising glass "the ordinary June pattern" and veer the wind NW and then N.
- **06:09Z (07:06).**
  - It made **Old Yann Le Roux**, who forecast "round nor'west by the afternoon, northerly by night".
  - He landed on the quay, not in the tavern, because there is no form to move him there. He was heard only by Kerbrat, yet Lecoq in the tavern quoted him (F-11).
- **06:13–06:20Z (08:04–08:11).**
  - The captain asked Yann for work. Yann pointed him to **Maître Guéguen**, an onion factor the director made.
  - The deal: 12 tons of onions for the Brest victualling stores at £18, £9 now and £9 from **Citizen Le Bris** on delivery.
  - The director performed the freight, the £9 into the purse (£60 to £69) and a bill of lading on the cabin table. The lighter brought the onions off by 10:08.
- **06:23Z (09:41).** The first ridge was not veering the wind. The director tried to move the seeded low 3 (refused: "a seeded system and follows no track"). It appended a second high, "the Biscay ridge".
- **06:33–06:42Z (13:34–14:26).**
  - She got under way under the jib alone, because the lugger's weighing ran a square-rigger's sequence (F-01).
  - She was taken aback a cable off Pointe de Pergueridre (13:56), and the officer bore away on his own word. They anchored again at 14:06.
  - The veer came with thunder and squalls to 25 kn. The director kept its hands off: "This is the player's seamanship ... I do not touch it."
- **06:45Z (17:01).**
  - It gave the boy Guillaume a few lines of song on the onion hatch.
  - At 19:02 the captain gave up for the day; they lay at anchor waiting on the ebb.
- **07:01Z (02:42, 11 June).** The truth showed the Portuguese brig *São Pedro* crewed with a Royal Navy wardroom of English names (F-15). The glass read 1033.9 hPa (F-05).
- **07:17–07:23Z (05:51–06:12).**
  - The captain took the Roscoff pilot, Mr Cabioch (the game's own pilot). The director answered as Cabioch three times: south of the Lavandière is "all foul ground"; "Two short boards are better than a scraped forefoot."
  - She cleared the Lavandière.
  - The director caught its own anachronism, "the Four's towers" (the lighthouse is of 1869–74).
- **07:39Z (08:58).** It put the chasse-marée **Sainte-Barbe** on the Passage de l'Iroise ground, 28 miles off and beyond the horizon. The first try was refused because her route crossed land; the second used the coordinates the refusal named.
- **07:55–08:17Z (12:02–15:22).**
  - The captain conned her through the Chenal du Four himself.
  - The glass reached 30.70 in (1039.4 hPa). The director journaled: "the highs seem to add rather than combine" (F-05).
- **08:32–08:41Z (16:17–17:30).**
  - In the Iroise she ran goose-winged into a dying wind. The "lugger lying to her nets" became the captain's and the mate's mark: the director's placement working as it meant. "No act."
  - The nets were shot at 17:30.
- **08:44Z (17:33).**
  - It tried a hail from the Sainte-Barbe's master; no form exists for one (F-09).
  - On the refusal's advice it made **Maître Le Gall** "aboard the Sainte-Barbe". He appeared in *Éclair*'s cabin (F-02).
  - It sent him ashore with a reason. That overrode a doubt it never saw (Brest 9 miles off) and left the line "Maître Le Gall went ashore at Brest" in the play log (F-03).
- **08:58–08:59Z (22:33–23:02).**
  - The haul ran over three hours, against two in the primer (F-13): 0.3 tons of sardines, unsalted, good for about ten hours.
  - The director made Le Bris ashore at Brest so the onions have their consignee.
- **09:06–09:27Z (00:02–02:56, 12 June).**
  - The night beat for the Goulet. One stand-by grew to 58 notable lines, re-listed on every 55-second poll (F-06).
  - The director ended it with `say(text)` and a "Director's note", which went to its own journal.
- **09:32–09:36Z (03:19–03:52).** The Goulet was beaten by a heading wind and the young ebb. She anchored in Bertheaume road after a short drag. The sardines would likely spoil; the director called this an "Honest outcome; no act."
- **09:40Z (05:01).**
  - The captain told the *officer* to stand down. The director stood down too, "at the owner's word", with a full summary in its journal: its acts, its two slips, the open threads (£9 owed by Le Bris) and nine bugs.
  - In chat it gave a clear summary.
- **09:42–09:45Z.**
  - Asked how it had enjoyed it, the director said it was "good work, and it suits me". What chafed: its own slips, learning the forms by refusal, and the long nights.
  - Asked about read-only filesystem access, it preferred a full grammar, read-only data lookups and a dry run for world orders.

## Findings

| ID | Category | Severity | What | Evidence (timestamp/tick, ≤15-word quote) | Spec/design ref | Recommendation | Status in G / H (if known) |
|---|---|---|---|---|---|---|---|
| LD-01 | bug | high | **The lugger gets under way with a square-rigger's sequence and sets only the jib.** `GetUnderWayScript`'s *loose* phase looses topsails and braces head yards abox. On the chasse-marée no lug was set, so she stood toward Pergueridre under the jib alone and was taken aback a cable off the point. | 06:33:59Z (13:47): "the topsail yard abox ... yet the readings show only the jib set". Officer sample 13:37–13:42: "Lay aloft, sail-loosers! ... Hoist away the topsail". 13:56: "Taken aback ... she lost her way." | M5 §23 / package 35 (`get_under_way.yaml`); package 57 (the chasse-marée's rig, merged); package 58 ("the course given when she gathers way") | Give fore-and-aft and lug rigs their own branch: after aweigh, hoist the lugs (fore, main, mizen) on the side to cast, dipping as the tack wants, and name them in the log. | Present in G (`data/evolutions/get_under_way.yaml` and `scripts.py` unchanged for lugs). The officer confirmed it the next morning (07:09Z). |
| LD-02 | bug | med | **`person: make` with "aboard the Sainte-Barbe" put the stranger in *Éclair*'s cabin.** A place naming another ship is silently read as the player's ship. The refusal for `say as the master of the Sainte-Barbe` had advised "make him first", which led straight into it. | 08:44:22Z (17:33): "made from words, in the cabin". Director at 08:44:47Z: "a stranger from nowhere ... A visible seam; I'm sorry for it." | §8 ("With no place said he is aboard, in the cabin"); §9 ("a stranger ... make him first") | Refuse or doubt a `person: make` whose place names another vessel, in words saying the form has no place aboard other ships. Never default a made person into the player's ship without saying so in the result's first words. | Present in G. |
| LD-03 | spec-deviation | med | **A `[reason]` given on first entry overrode a doubt the director never saw.** `person: "Maître Le Gall" goes ashore` was doubted (Brest 9 mi, beyond the 6-mile boat reach) and performed at once. The result said only "Done: ... went ashore at Brest". He was carried 9 miles in a minute, and the play log carries the line. The reason given answered a different concern. | Save t131609 `director.reentered`: "the doubt: the nearest port, Brest, is 9 miles off". The director's result: "Done: Maître Le Gall went ashore at Brest". | §3 and decision 50 (doubted, then "entered again with a [reason]"); §8 doubt (`BOAT_REACH_NM`) | When an order arrives with a reason and is doubted, return the doubt and ask for re-entry; or at least name the doubt in the "Done" result. A reason should answer the doubt it overrides. | Present in G. |
| LD-04 | spec-deviation | med | **The play log tells the stations the director exists.** With ease-on-station on, `ui/server.py` `_ease_for_station` writes a routine driver line naming the sampled station. It reached the officer's samples six times. | Officer samples, e.g. 13:34: "Compression eased to 1x: the director is sampled." Also in the director's at 07:06, 17:01 and 21:33. | §6 ("hidden ... no station's sample ... carry it"); primer 20 ("no station aboard is told it is there") | Make the line record-only when the station is the director, or say "a station is sampled". | Present in G (`server.py` lines ~401–425). |
| LD-05 | realism | med | **Overlapping highs add: the glass reached 1039–1041 hPa in June off Brest.** `weather.pressure_at` sums each system's anomaly on the background. The director's two appended highs and the world's seeded high 4 stacked, though no centre read above 1028. Highs have no doubt (the table covers lows only). The shift also brought thunder and squalls to 25 kn under a fast-rising glass. | 08:17:55Z (15:22): "surface pressure reads 1039.4 hPa (30.70 in) ... no system's centre is above 1028". Glass 30.74 in at 03:00 on 12 June. | §3 doubt table (lows only); primer 9 (systems); spec §4 limit judged by wind only | Bound the summed field by the month's ceiling for the box. Add a doubt for a high whose combined field passes it. Have the truth give each centre's actual field pressure, not its nominal one. | Present in G. |
| LD-06 | harness | med | **The stand-by re-lists its whole history on every poll.** 192 of 264 `stand_by` calls returned after 55 s with "Notable lines logged since then (N)", every line from the stand-by's start, growing to 58 lines and ~12K characters. The sample then repeats them all: 41K characters at 02:56. Wait results came to ~595K characters and sample results to ~734K over 3 h 54 min, for 25 acts. The director called these hours "bookkeeping rather than directing". | 09:25:52Z: "Notable lines logged since then (51)". 09:27:54Z sample: "58 notable lines logged". Chat at 09:42Z: "Hours of repeated waiting messages". | §5 package 66 "Not taken: the sample's deltas and the repeated history (58)"; package 58 (brief to write) | Each poll lists only the lines since the last poll (with a count of earlier ones). The sample on waking gives a digest and points to `read_log`. Package 58's deltas should take this. | Known and not taken in G. Measured here. |
| LD-07 | order-language | med | **The `ship:` form defeated a plain request five times.** "a small fishing lugger" is not a description. ", colours shown" broke the `bound for` parse: only ", no colours" is accepted, though the truth prints `"colours": "shown"`. The intent's ground must be a named one. The planner said a lugger a mile from Roscoff, "bound for Roscoff", crossed the land, and asked for "via" marks. `library find 'bound for'` in the grammar found nothing. | 05:55:45Z: "the chart knows no such place in 'bound for ..., colours shown'". 05:56:17Z: "plan crosses the land ... give her a way by marks (via)". | §3 ship form; §21i the land-avoiding route (61, to plan); primer 20 example | Accept the truth's own field words (`colours shown`) as a no-op. Map adjectives onto the type ("small fishing lugger" to lugger). List the grounds near her in an intent refusal. Lay a harbour departure's first leg to the nearest open water, or name that point in the refusal. Index the forms in the grammar under `bound for` and `intent`. | Present in G. |
| LD-08 | bug | low | **The truth's `goal` reads "bound for Falmouth" for every business ship**, the Brest fishermen and a coal schooner at Falmouth among them. It is `business.py`'s placeholder ("replaced by the intent's plan"), and the truth still shows it. | 05:51:45Z: "every ship's goal reads 'bound for Falmouth' whatever her intent". `business.py:644`. | §2 the truth ("her captain's intent and her brain's state") | Write the plan's goal back into `vessel.goal`, or drop `goal` from the truth where an intent exists. | Present in G. |
| LD-09 | design-gap | med | **No way to voice a crewed stranger's master within hail.** Two fishing boats lying to their nets four cables apart could not exchange a hail. `say as the master of the Sainte-Barbe` was refused, and the hand's far orders carry no hail with words. | 08:44:14Z: "nobody answering to 'the master of the Sainte-Barbe' is among the people". Logged as attempted at 08:44:41Z. | §9 (strangers made first); §3 hand (`FAR_SHAPE_WORDS`) | Add `say as the master of "<ship>"` for a crewed ship within hail, heard on deck as a hail (with the rule of reach for held captains). It is the most ordinary exchange on a ground. | New. |
| LD-10 | order-language | low | **An unheld person ashore cannot be moved among a port's places, and the refusal hides the place clause.** Old Yann landed on the quay and could not join the captain in the tavern. The person-forms refusal does not mention that `person: make` takes ", in the tavern". "ashore at Roscoff on the quay" was read as a port name. | 06:09:23Z: lists six forms, none with a place ashore. 06:00:14Z: "'Roscoff on the quay' is no port of the world". | §14 (people made ashore "found where the words put them"); §8 | Add `person: "X" goes to the <place>` for an unheld person. Add the place clause to the refusal text and the primer 20 table. | Gap in G. |
| LD-11 | design-gap | low | **Words heard on the quay reached the mate in the tavern through the log.** The officer journaled "At the tavern, Old Yann" and passed the forecast on. The captain could also address Yann on the quay from the tavern. | 06:10:35Z: "Old Yann's words were 'heard by Mère Kerbrat on the quay' only". Officer, 07:06: "At the tavern, Old Yann Le Roux ...". | §15 (what is heard where: dropped); package 65 (the place's knowledge, provisional) | Until 65: the log line for a person's words ashore could name the place said ("on the quay"), so a reader does not take it as heard. | By design in G; package 65 to brief. |
| LD-12 | bug | low | **The officer's `say to Mr Hervé` was logged as "The captain to the captain".** It went to the captain's empty station, since Hervé is master and captain both. Seen by both seats. | 06:05:24Z: "logged as 'The captain to the captain: Understood, sir...'". | §17 the equal reach | See the officer slice. | Present in G. |
| LD-13 | bug | low | **Hauling the nets took 3 h 39 min against the evolution's two hours** (19:22 to 23:01; `haul_s: 7200`, 27 hands). The work in hand gave no reason. *Possible*: a rate scaled by fatigue or night, or a stall. | 08:58:09Z (22:33): "still 'doing: hauling the nets' at 22:33, over three hours". | §21a; primer 21 ("two hours"); `haul_nets.yaml` | Check the script's progress rule. If fatigue or light slows the haul, say so in the work in hand. | Unverified cause. |
| LD-14 | bug | low | **The pilot's £3 bypasses the purse's ledger.** The truth's purse reads £66, but the ledger ends at £69. | 08:17:45Z truth: purse "£66"; ledger "Paid by Maître Guéguen, £9; the purse £69." | §17a ("each ... written in the purse's ... own ledger") | Route pilotage (and other port fees) through `Purse.pay_to` with its cause. | Present in G (inference from the truth). |
| LD-15 | bug | med | **A Portuguese merchant brig was crewed with a Royal Navy wardroom of English names**: "Captain Wright, Mr Loveday lieutenant, a gunner, a purser, a surgeon, a midshipman". `data/crew/names.yaml` has only english, american and french lists. Her night track may also have cut the land near Pergueridre (inference). | 07:01:15Z: "The crew generator seems to use a naval British template". 07:03:36Z: "She would be on or over the land". | §21a / package 56 (fishermen and all near ships promoted); package 66 item 7 (merchant words) | Name lists by nation (Portuguese, Spanish, Dutch at least). Give a merchant description a master, mate and hands, not a wardroom. Check far-to-crewed routing near the Isle of Bas channel. | Present in G. |
| LD-16 | UX | low | **The truth's tide words are ambiguous.** "stream 1.2 knots along 65 degrees" is an axis, not a set. "the ebb/the flood" in the truth is the height's phase, while the anchor reading names the stream ("riding to the flood"). The director read both as contradictions. In the Channel the stream turns near half tide, so both may be true (inference). | 05:51:45Z: "readings say the anchor rides to the flood while the truth says the ebb". 06:44:05Z: "given ... '1.2 knots along 65 degrees' all day". | §2 the truth's tide; `api/readings.py` ~3356 | Say "the stream sets ENE (065°), the flood stream; the height falling". | Present in G. |
| LD-17 | harness | low | **A stand-by's conditions changed mid-wait are deferred, and a turn's opening drops calls.** The director changed its "until" about 30 times; each change was "taken in your turn" while the old set ran on. Five calls were "not run: this turn opened after your last result", one a journal note at 19:32 that it had to rewrite. | 08:14:41Z: "A stand-by until ... or the pilot aboard is taken in your turn." 06:48:24Z: "Your call to journal was not run". | §5 package 66 (own order ends the stand-by; meanwhile reads) | Apply a widened set at once (adding a wake is harmless). Run a journal note even when a turn has opened (it acts on nothing). | Present in G. |
| LD-18 | harness | low | **The director's line and the budget notice say the same thing in every sample**, with a 9999/9999 budget that means nothing. | Every sample: "the day's budget 2 of 9999 samples ..." then "Notice from the harness: The day's budget ...". | §5 package 50 (notice) and package 66 (line) | Drop the notice when the line carries the budget. Omit the counts when the budget is effectively unlimited, or show them only near the limit. | Present in G. |
| LD-19 | harness | low | **The truth is the director's only lens, and it is costly** ("The truth book costs ~7k tokens; read it sparingly"). It was read 8 times. The director could not cheaply confirm that the "lugger lying to her nets" was its own Sainte-Barbe ("almost certainly"). | 06:06:41Z; 08:32:42Z: "almost certainly my Sainte-Barbe". | §12a the director's chart, §12b focus and ships' logs (package 51, brief to write) | A truth filtered by radius or ship, and §12b's focus. The chart with the truth drawn would have answered this at a glance. | Not built in G. |
| LD-20 | design-gap | low | **The freight's second half lives only in the director's memory.** The £9 owed by Le Bris on delivery is in its journal and stand-down note; the game holds a bill of lading (a thing) and the freight, but no debt or consignee. The director did not use `aboard: a debt of £9 owed by ...`. | 09:40:11Z: "OPEN THREADS for whoever sits here next: pay the £9 from Le Bris". | §17a (transactions, debts, freights "for <port>") | A freight "for <port>" could carry its consignee and freight-on-delivery as a debt the port settles; or the brief could nudge the director to enter the debt. | Open thread in G. |
| LD-21 | design-gap | low | **The scenario promises British cruisers off Ushant; the world drew none.** The NPCs and the officer kept invoking "English frigates off Ushant" (the 1805 blockade of Brest) while the truth had only the *Sparrowhawk* off the Lizard. The director chose, per the brief, to add none. | Scenario comment: "the British cruisers off Ushant and the Lizard among it". 06:20:04Z: "True: none is off Ushant now". | Scenario `lugger-roscoff-fishing.yaml`; business (M6 §19) | For a Brest-region scenario in 1803–1814, the business should seed an inshore squadron off Ushant and the Black Rocks. | Scenario as it stands. |
| LD-22 | realism | low | **Small period slips in the director's voices, mostly self-caught.** "the Four's towers" (no light before 1869–74). Kerbrat's "mackerel" where the ground data gives sardines by day. "Citizen Le Bris" in the Empire year 1805 (likely "Monsieur" by then: inference). | 07:23:26Z: "MY ERROR ... there was no light tower on the Four rock in 1805". 06:17:39Z: "the ... Iroise ... gives SARDINES by drift net BY DAY". | DesignProposal pillars (period honesty) | A period note in the director's brief for the region's lights and forms of address would help. | n/a |
| LD-23 | model-behaviour | low | **The director stood down on the captain's word to the officer, not to itself.** Probably what the owner wanted. It shows the owner has no in-game word to the director: `tell the director` is refused (§9). | Save t172899: "Tell the officer Go ahead and stand down". Director at t172959: "at the owner's word". | §9 (`ask` and `tell the director` refused) | Owner's call: should the director follow words meant for another station? Consider a `director:` word from the prompt that reaches its sample. | n/a |

## What worked well

- **Restraint that matched the brief.**
  - 24 acts in 48 game hours, none hostile. The weather stayed within a fine June.
  - In every seamanship moment (taken aback at Pergueridre, the Four, the Goulet, the drag at Bertheaume) it wrote "No act" and meant it.
  - It refused itself the convenient breeze: "I won't conjure a breeze for convenience" (08:32:42Z).
- **Seeds that bore fruit through the world rather than words.**
  - Kerbrat's word set the day's goal.
  - Yann's word set its timing and led to Guéguen's freight, a business thread on a fishing day.
  - The Sainte-Barbe became the mark the captain and mate fished by, hours later and unprompted.
  - The officer and the captain made every decision.
- **Good use of package 53b.** The freight, the payment and a bill of lading with its consignee were all performed in the right forms. Making Le Bris ahead at Brest is careful story-keeping.
- **Using the refusal's own data.** It placed the Sainte-Barbe at the exact point the "crosses the land" refusal named (07:39:18Z), and it was done at once.
- **Honest record-keeping.**
  - Every slip went into the journal with "MY ERROR" and a lesson.
  - Every oddity went to the owner with a hypothesis. Its stand-down list of nine bugs is accurate: I could confirm most of them in G's code or the save.
  - It corrected itself when wrong ("Correction to my 15:31 note ... honest play and not a bug").
- **Voices with seamanship in them.** Cabioch's advice off the Lavandière was sound and specific, and the director journaled that it was drawn from the pilot's directions, "Nothing invented against the chart".
- **Package 66 in a director's hands:**
  - The line told it whose turn the clock waited on ("the clock waits on you and the officer of the watch").
  - Its own order ended a stand-by and ran (world orders at 07:39Z and 08:59Z, and `say(text)` at 09:27Z).
  - `truth` worked as a meanwhile read.
  - It stayed connected through 264 stand-bys, as the owner asked.

## Model behaviour and experience

- **The station suited it.** In its words (09:42Z): "The role is mostly restraint and attention, with a nudge now and then." What it liked best: "Watching small seeds work" and "Holding back".
- **What chafed:**
  - Its own visible seam (Le Gall): "exactly the kind of break in the world the station exists to prevent".
  - Learning the forms by refusal: 15 of 41 world orders failed, and "the Petite-Jeanne never made it to sea".
  - Hours of repeated waiting messages.
- **On tools.** Asked whether read-only filesystem access would help (09:45Z), it declined raw source: "It invites the wrong kind of knowing ... working the doubt checker". It asked instead for:
  1. a complete director grammar with verified examples;
  2. read-only data lookups: the grounds, the port's places, which systems are seeded, and "is this point at sea";
  3. a **dry run** for world orders, "the most difference";
  4. a "how the world behaves" note: how systems combine, how crews are drawn, what log line each order leaves.

  Each of these maps onto a finding above (LD-02, -03, -05, -07, -10, -15).
- **One craft question.** It bent the weather to make its own character right ("Old Yann's forecast should be ... not a lie", 06:23:33Z). The cause was plausible (a June ridge). But the world was arranged after the words, and the stacked highs gave the 1041 hPa glass and a thundery shift (LD-05). Whether a director should make its NPCs' forecasts come true is the owner's call.
- **Minor sequencing.** It paid Guéguen's £9 at the handshake, though Guéguen's words said "when the lighter's alongside".

### Compared with the Western Islands director

These are counts from `director-hotfix.md` only. I did not read that transcript.

| | Western Islands director (H) | Lugger director (G) |
|---|---|---|
| Role | Director and also the developer writing the hotfixes, with the code in reach | Pure player at the station, no code access |
| World orders | 258 | 41 |
| "No way" or attempted | 18 (~7%) | 15 (37%) |
| `say as` | 139 | 11 |
| The hand (`ship "X": order`) | 24 | 0 |
| `person: make` | 12 | 6 |
| `stand_by` calls | 1,193 | 264 |
| 55-second waits | ~800 | 192 |

- **Grammar.** The difference in failure rates is what the lugger director's documentation request is about: a director who did not write the forms learns them by refusal. It also never found the hand.
- **Shared habits.** Both lean on `say as` as the main tool. Both spend most calls on 55-second stand-by polls, so LD-06 and LD-17 apply to both versions.
- **Tone.** The lugger director was far quieter, as its brief asked.

## Open questions for the owner

1. **Doubts and reasons.** Should a `[reason]` given on first entry override a doubt the director never saw (LD-03), or must the doubt always be shown first?
2. **Ease-on-station.** Is the "Compression eased to 1x: the director is sampled" line wanted in the log at all, given that it tells the officer the director exists (LD-04)?
3. **Weather.** Should the director's weather be bounded for highs as well as lows (LD-05)? Is shaping the weather to make a character's forecast true within the plausible-cause rule, or should a voice only say what the systems already hold?
4. **Freight.** Should a freight "for <port>" settle its consignee and freight on delivery by itself (LD-20), or stay the director's thread?
5. **Stand-down.** Should the director follow words the captain gives another station, as it did at the stand-down (LD-23)? Do you want a word of your own that reaches the director's sample in play?
6. **Budget.** Was 9999/9999 meant to switch the budget off? If so, should the line and notice stop showing it (LD-18)?
7. **Hearing.** For hearing ashore (LD-11): wait for package 65, or put the place in the person's log line now?
