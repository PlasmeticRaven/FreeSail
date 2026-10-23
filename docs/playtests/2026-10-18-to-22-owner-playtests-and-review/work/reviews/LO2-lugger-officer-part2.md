# LO2: Lugger officer, part 2 ("Freesail-officer setup", 08:01Z–10:35Z)

## Scope

- **Span.** Transcript 2026-10-22 08:01:06Z to 10:35:36Z. In the game, Afternoon watch 12:33 on 11 June 1805 (about t113612) to the stand-down at Morning watch 05:01 on 12 June (t172912). The save `fishing-lugger-anchored-in-Berthaume` ends at t172994. The 09:49Z–10:35Z stretch is conversation with the owner after the game.
- **Version.** G, rules e19ddb854219fbd8. The save header reads `build m6c, rules e19ddb854219fbd8`.
- **Seats.**
  - Captain: the owner.
  - Officer of the watch: Opus 5.5 as Mr Lecoq, through the freesail-officer MCP bridge.
  - Director: Opus 5.5 ("Freesail-director setup").
  - Master: the game's own. The scenario lists `master: model`, but the save shows no seat for it.
- **Files read.**
  - All of `work/chunks/lugger-officer-2.md` (2,809 lines).
  - From `work/transcripts/lugger-officer.jsonl`, the full raw tool results at 08:09:16–08:10:07Z, 08:26:34Z, 08:58:30Z, 09:35:58Z and 09:39:13Z, because the chunk truncates them.
  - `work/saves-extracted/lugger-fishing-final.md`, lines 1560–2806.
  - The scenario `lugger-roscoff-fishing.yaml`.
  - TechnicalSpec-M7b §5 (as built by package 66), §17, §21a and §21b.
  - TuningNotes, "Package 66".
  - The owner's `M7b Notes.txt`.
  - Two of the officer's ship-view PNGs: 15:31 from ahead and 17:31 from the larboard beam.
  - G code, to confirm findings: `agents/mcp_server.py`, `agents/tools.py`, `agents/agent.py`, `orders/glass.py`, `world/lookout.py`, `api/readings.py`, `world/people.py`, `evolutions/scripts.py`, `data/vocabulary.yaml`, `data/fishing/channel-west.yaml`, `data/evolutions/haul_nets.yaml`, `trim_lug_sheet.yaml` and `trim_jib_sheet.yaml`. I spot-checked the same lines in H.

## Narrative

- **12:33–13:09, down the Chenal du Four.**
  - On the captain's word the officer runs S by W, then SSW. It fixes by Molène and the Isle Vierge, then by the Four and Keller (cut 80°).
  - It warns that the master allows the flood at 4 kn against them until 16:00, and it offers to stand off and on until the tide turns. The captain answers: "Nay, we make for it. We can duck in to Blanc Sablon" (08:06Z).
- **13:25–14:23, three sails sighted.**
  - At 13:43 the officer sends a `say` out of turn. Under package 66 that ends its stand-by "at its own word". The game, though, had run on to 14:23 while the officer was waiting (see LO2-03).
- **14:43, the captain takes the conn for the Platresses gap.** At his invitation the officer draws the harbour and coast charts. It journals the gap as about 1¼ miles wide and advises favouring the Platresses side.
- **15:08–15:31, reef, dip and goose-wing.**
  - Through the Four, the captain decides to fish. A reef goes in the lugs.
  - The captain asks the officer to dip only the fore lug, "curious what happens". The officer draws the ship view from astern, then from ahead: she is goose-winged.
  - The captain's word arrived within a minute of the officer's ("Goosewing! Goosewing!", then "You read my mind man!").
  - At 15:32 the officer warns that the Monks bear "steady and closing" and steers a point to starboard with the captain's agreement.
- **15:44, both read the fishing primer.** The officer reads primer 21 whole and journals the forms.
  - `the fishing grounds` is refused to the officer as being outside the captain's general authority. The captain's `you may the fishing grounds` is then refused too (LO2-01).
- **15:46, a course for the ground, held S instead.**
  - `shape a course for the Passage de l'Iroise` warns that the line passes "the shore under St Matthew's Point within a cable".
  - The officer checks the coast chart, finds rocks off Béniguet on the line, and holds S. The captain answers: "good catch on the course, it would have been close indeed."
- **16:08–16:58, refusals before the shot.**
  - `shoot the gear` is first refused for authority. The captain gives `you may shoot the gear` and `you may haul the gear`.
  - The shot is then refused because she is on no ground ("5 miles off"). The captain retries `Shoot the gear` six times while closing.
  - Meanwhile:
    - Both lugs are dipped back for the new course.
    - `shake out the reefs` is refused; the captain supplies the working form.
    - The glass cannot single out the second brig (LO2-02).
  - The captain shoots the gear at 16:58.
- **17:30, the nets shot.** The officer heaves to and rides to them. Two French chasse-marées lie to their nets close by.
  - The captain admires the ship view ("she could almost be a painting"). The officer looks from the larboard beam and describes her accurately.
  - The director makes Maître Le Gall within hail and then, by mistake, sends him ashore. The owner sings a shanty.
- **18:27, how the hands are.**
  - The officer queries `the catch` and is refused for authority again. It answers through the `answer` tool, but "no question was put" (LO2-16).
  - It plans the haul for half past seven.
  - It asks for `stand_by "three bells"`, but the earlier wait continues (LO2-04).
- **19:22–23:01, the haul.**
  - All hands are called and the nets hauled: "Only 15 hands to haul the nets; there are no more on deck."
  - The haul takes 3h39m against the file's two hours (LO2-14).
  - The officer eats and drinks at 20:00 after `how am I` says "You are thirsty".
  - The catch is 0.3 t of sardines, unsalted, good for 10 hours.
- **23:02–23:20, the wrong tack.**
  - The officer's own error: it called the starboard tack the one for the Goulet. `fill away` takes her WNW toward a chasse-marée at her nets a cable off.
  - It wears ship, says so, and journals the lesson.
  - The captain teaches "steer, settle, trim, then full and by" and gives the officer the conn for the Goulet.
- **23:20–02:25, the night beat.**
  - The officer beats up past the Basses du Lis, Le Bellen and Toulinguet by moonlight in short boards, with careful bearings and soundings.
  - It notices that single light bearings "by estimation" (most taken by the captain) keep moving the account (LO2-11).
  - "Not hands enough on deck to trim the mizen" recurs at every trim (LO2-09).
  - The officer twice proposes Camaret road for the tired hands.
- **02:38–03:19, the Goulet attempted and given up.**
  - The captain cons for the Goulet and the officer calls all hands.
  - The wind heads her. The officer bears away under the `danger` argument, which the game says was "not needed".
  - A fix shows no ground gained against the ebb. The officer advises Bertheaume, and the captain agrees: "Aye, you are right."
- **03:20–03:52, Bertheaume.**
  - `shape a course for the road of Bertheaume` calls WNW unlayable; the captain overrules ("296 is layable") and it lays fine (LO2-10).
  - The officer lets go the best bower with about 2 kn on and the jib and mizen drawing. She drags (an urgent sample), the cable is veered to 82 fathoms, and she brings up.
- **03:52–05:01, hand-over and stand-down.**
  - The officer uses `hand_over` with a full note, goes to the gunroom and stands by "asleep below until called".
  - The captain goes below. The log says the deck is now the officer's, though he had just handed it over (LO2-08).
  - On waking at 05:01 the station line reads "on your feet since 10:29 on 11 June" (LO2-07).
  - At the captain's word it journals five developer notes and calls `stand_down` with a note; the game is saved.
- **09:49–10:35Z, the conversation after the game.**
  - The owner asks about the officer's experience and immersion, and whether pictures or words served it better.
  - It asks for one feature wish. The officer answers "a view from the rail".
  - The owner names the models' main error: "making the right orders, but at the wrong time" (trim). The officer analyses why.
  - It learns that compound stand-bys exist, which its brief never told it (LO2-06).
- **10:35Z, the session writes two files** (Write calls). Both go to Claude Code's per-project memory folder, `C:\Users\frenc\.claude\projects\C--Users-frenc-AppData-Local-Claude-Data-…-scratch-2026-10-22-054192\memory\`:
  - `freesail-officer-timing.md`, a "feedback" memory. It holds:
    - Steer, then `stand_by` "steady on the course or 5 minutes", then trim, then full and by.
    - Compound stand-bys with "or", always with a time ceiling.
    - Take all sail off before letting go.
    - Check which tack `fill away` takes.
    - Set the lugs by name, because `get under way` sets none.
    - The owner wants candid critique.
  - `MEMORY.md`, a one-line index.
  - The stated reason is "so it holds even if the context gets summarised".
  - Two caveats, the first an inference: the memory is keyed to this scratch workspace's path, so it will not follow a session started in another folder. And the line saying `get under way` sets no lugs is a bug report saved as standing advice; it goes stale once the bug is fixed.

## Findings

| ID | Category | Severity | What | Evidence (timestamp/tick, ≤15-word quote) | Spec/design ref | Recommendation | Status in G / H (if known) |
|---|---|---|---|---|---|---|---|
| LO2-01 | bug | med | The fishing readings `the catch` and `the fishing grounds` are refused to the officer under general authority. The refusal is ungrammatical, and its remedy fails: the captain's `you may the fishing grounds` is refused because it "names no order". The captain had to read both himself and relay them. | 08:25:37Z: "may not the fishing grounds under the captain's general authority"; 08:48:56Z: "may not the catch". Log 15:45: "'the fishing grounds' names no order the officer…could be allowed" | §17 ("the readings… from anywhere"); §21a lists both as orders. `vocabulary.yaml:1289-1296` makes them `level: reading`, `object: fishing`. `Domain.why_not` (`agent.py:334`) exempts only needs, glass and free. The template is at `tools.py:766-767`. | Make every `level: reading` order every station's (or add `fishing` readings to the exemption). Never suggest "you may <reading>". | G: present. H: the same `why_not`. |
| LO2-02 | order-language | med | The glass cannot single out one of two ships of a kind. `the glass on a brig` always took the nearest brig, the Portuguese one. The qualifiers "on the starboard bow", "bearing W by S" and "abeam to larboard" were refused, though the strangers list and §21b's own lookout line use those words. `the lugger` was refused while a lugger was listed. `her` took the nearest sail, not the one just reported (13:42, and at 15:37 the pilot cutter instead of the schooner). The owner hit the same wall: he tried the qualifiers, `what is she` and `What is a topsail schooner`. | 08:35:32Z: "Nothing in sight answers to 'the brig on the starboard bow'"; 08:22:28Z: "Nothing… answers to 'the lugger'"; officer at 16:57: "can't single out one of two brigs" | §21b: the lookout says "The glass on the brig on the starboard bow". `lookout.find` matches only `_RIG_WORDS` (brig, ship, frigate, schooner, merchantman: no lugger or chasse-marée) or names (`lookout.py:285-291, 1172-1185`). | Accept relative and compass bearings and "the nearer/farther" as qualifiers. Add lugger, chasse-marée, sloop and smack to the rig words. Let `her` mean the sail last reported. | G: present. H: the rig table has no lugger. |
| LO2-03 | harness | med | The "still waiting" reply gives no current game time. Under compression about 40 game minutes passed in about 60 s. The officer's report at 13:43 ("SW by W four leagues…all three are hull down") was logged at 14:23, when the in_sight list gave the sail at three leagues and the one ahead at two. A model cannot tell how stale its picture is. | 08:09:16Z: "standing by since Afternoon watch (13:42)"; the own-word sample: "it is now Afternoon watch (14:23)" | Package 66 item 2 (own word); `still_waiting`, `mcp_server.py:265-294` | Add "it is now <stamp>; <n> minutes of the ship's time have passed" to every still-waiting reply. | G: present; same function in H. |
| LO2-04 | harness | med | A new `stand_by` with a different `until`, sent during a stand-by, does not replace the old wait. It is answered with "A stand-by until three bells is taken in your turn", which reads as though it will be applied. At 18:28 the officer's three-bells ceiling for the haul was silently dropped; only the captain's word at 19:22 saved the timing, and otherwise the wait would have run to eight bells. Also seen at 08:52:39Z. | 08:51:29Z: "this call continues that wait. A stand-by until three bells is taken in your turn." | §5 as built by package 66 ("a lone `stand_by`" does not end a stand-by); `mcp_server.py:1009-1016` | Either let a new `until` replace the wait, or say plainly: "Not taken: you are still standing by until X; say() or an order ends it, then stand by again." | G: present. H: the same code. |
| LO2-05 | bug | low | The "same wait" check compares "ten minutes" with the interim's "ten minutes have passed" by suffix, so re-calling the same interval wrongly says another stand-by "is taken in your turn". | 08:29:13Z and 09:16:19Z: "standing by…until 5 minutes have passed… A stand-by until 5 minutes is taken" | `mcp_server.py:1012` | Normalise both sides through the stand-by parser before comparing. | G and H: the same line. |
| LO2-06 | docs | med | Compound stand-bys ("x or y") exist and the captain's, master's, lookout's and director's briefs say so. The officer's brief and the `stand_by` tool description do not. The officer "read both as 'pick one'" and never used a time ceiling. That is the root of the "blind genius with narcolepsy" waits the owner described. The owner believed every station had the form. | 10:34:39Z: officer: "nothing I had told me about compound stand-bys"; 10:34:27Z: owner: "There should already be compound stand bys" | `agent.py` OFFICER_BRIEF (1317-1322) against 1690 and 1735; `director.py:588`; `tools.py:1393-1416`; package 41 (`harness.py:3547`) | Add "or several joined with 'or' ('tacked, or ten minutes')" to OFFICER_BRIEF and to the `stand_by` tool description, which every door sees. | G: missing. H: the officer brief also has no "or". |
| LO2-07 | bug | low | After an hour's sleep the station line gives a false time: "on your feet since 10:29 on 11 June" on waking at 05:01 on 12 June. The officer had been up since 00:12 on 11 June and had just woken. The figure is now minus the fatigue hours, which a part-sleep reduces. | 09:39:13Z: "in the gunroom, since 03:53; … on your feet since 10:29 on 11 June" | §5, package 66 "the line"; `readings._line_state` docstring says "with when he last woke" (`readings.py:3218-3224`) | Show the real wake time, plus the needs' words for rest ("rested a little"). | Package 66 is G-only. |
| LO2-08 | bug | low | `Go to my cabin` logs "the deck is the officer of the watch's" a minute after the officer handed the deck over and turned in. The state says the captain has the deck. This misleads the owner about who keeps the deck at anchor. | Log 03:53: "The captain went below to his cabin; the deck is the officer of the watch's." | `people.captain_moves`, a fixed string (`people.py:1074`) | Name whoever actually holds the deck (`station_line`'s "deck" logic). | G and H: the same string. |
| LO2-09 | realism | med | A lug sheet trim takes a party of 6 hands and a jib 4: frigate figures from Luce 1884. So a 12-man watch on a 50-ton chasse-marée cannot trim the mizen and jib alongside the fore and main. A notable line comes at nearly every trim and samples the officer. It drove the all-hands call at 02:40 and the worn-out crew. Tacks call all hands every 10–15 minutes through the night beat. | 23:13, 01:27, 01:43, 01:59, 02:25, 02:40: "Not hands enough on deck to trim the mizen…" | `trim_lug_sheet.yaml:44` (hands: 6), `trim_jib_sheet.yaml:35` (hands: 4); `lugger.yaml` complement 30 | Scale the party to the sail's area or the ship (1–2 hands to a lug or jib sheet on a lugger). Consider making "not hands enough" for a trim routine rather than notable. | G and H: the same 6 hands. |
| LO2-10 | realism | med | `shape a course for the road of Bertheaume` judged WNW (296°) "too near the wind to be laid" with the wind about N to N by E, and kept her full and by, which fell off to W by N. Steered by hand, WNW held at 42° apparent with 5° leeway. | 09:32:42Z: "WNW (296°) lies too near the wind to be laid"; owner, 03:20: "296 is layable"; 03:25 readings: "42 degrees on the starboard bow… heading WNW" | Course shaping (M3/M4 orders) | Check the lugger's laying angle in the shaper and her full-and-by target against what she actually sails. | Not checked in code. |
| LO2-11 | realism | med | A single light's bearing with an estimated distance moves the account along the bearing by up to 2 miles. A bearing gives only a line, and a light's distance "by estimation" at four leagues is weak. The account swung back and forth through the night, and the officer came to trust the land and the lead over it. | Log 22:55: "St Matthew's light bore N by E, four leagues by estimation: the account moved two miles to the S by W"; 00:27: "moved two miles to the N" | — | Move the account only across the bearing for a single line, or weight an estimated distance by its error. | Officer note 5. |
| LO2-12 | bug | low | Inference. The course line's danger warning names "the shore under St Matthew's Point" for a SW by S or SW line from a position 2+ miles W of the Point, so the line runs away from it. The officer's chart showed the hazard was a knot of rocks off Béniguet. | 08:26:39Z: "the line passes the shore under St Matthew's Point within a cable"; 08:28:09Z: "within three cables" | §21i (the route over the chart's data) | Name the feature actually nearest the line; give the danger's bearing and distance. | Not checked in code. |
| LO2-13 | UX | low | A shot refused for being off the ground says only "5 miles off". The ground is a 3-nm circle, so it does not say the bearing or how far to the edge, and the grounds listing has no bearings either. The captain retried `Shoot the gear` six times as they closed. | 08:30:03Z: "She is on no fishing ground the master knows. The nearest: …5 miles off"; save t127053–t129490 | §21a; `channel-west.yaml:79-82` (`radius_nm: 3.0`) | Give the bearing and the distance to the edge in the refusal and the listing. | — |
| LO2-14 | UX | low | Hauling the nets took 3h39m (19:22–23:01) against the file's `haul_s: 7200`, stretched by an unstated factor (night, tired hands, 15 hands at first). Nothing told the players why, and work_in_hand gives no time remaining. The director flagged it as a "possible bug". | Director journal 22:33: "'haul the nets' began at 19:22… still 'doing'… over three hours" | §21a; `haul_nets.yaml`; `FishingGearScript.tick` (`scripts.py:7785-7793`) | Show the time remaining and the cause in work_in_hand ("hauling the nets, an hour more; slow with tired hands"). | — |
| LO2-15 | order-language | low | `shake out the reefs` is refused ("no such part as the reefs"). The owner had to supply `shake out the sails, all reefs`. | 08:31:16Z: "There is no such part as the reefs in this ship." | Order grammar (M2) | Accept `shake out the reefs` / `shake out all reefs` as all sails. | — |
| LO2-16 | harness | low | The captain asked his question with "Tell the officer …?", so the officer's `answer` came back "though no question was put". It was harmless, but the two forms of putting a question confuse. | 08:49:03Z: "Heard; your words are in the log, though no question was put." | §17 (tell or ask) | Treat a "tell" ending in "?" as a question, or let `answer` reply to the last word told. | — |
| LO2-17 | UX | low | "The land close aboard" is used for land three miles off. A bearing of "Le Bec de la Chèvre" is refused while the sighting itself names "the land about Le Bec de la Chèvre"; seven minutes later the same order worked. | 09:07:13Z: "the land close aboard and a sail are no marks"; 09:07:16Z: "The land close aboard is no mark" | `lookout.find`: SHORE_ID is excluded | Say "unnamed shore" rather than "close aboard" beyond a few cables; explain when the headland itself will be made out. | — |
| LO2-18 | UX | low | The anchor readings contradict themselves: "bar-taut, the strain 0.00 of the rating". A drag was declared at strain 0.03 while she still had way on. | 09:35:58Z: "82 fathoms…bar-taut, the strain 0.00 of the rating" | `readings.py:1873-1876` | Call a low-strain cable "taut" or "growing", and keep "bar-taut" for real strain. | G and H: the same code. |
| LO2-19 | realism | low | She rode to her drift nets "hove to on the starboard tack, jib sheet to windward" with headsails backed. Period drifters rode head to wind to the fleet under the mizen alone. The officer took in the flying jib because it made her fill away. | 08:44:50Z: "Hove to on the starboard tack, jib sheet to windward, … helm a-lee" | Primer 21 ("heave to and ride to them"); §21a | When nets are out, make "ride to the nets" the posture: fore and main down, mizen set, head to the fleet. | — |
| LO2-20 | design-gap | med | Trim timing, the owner's chief critique. Orders return at once and feel finished. A model sees only samples, so it trims before the apparent wind has settled. The sample's repeated lists (in_sight, lookout, strangers, sail_in_sight and stranger_in_sight all name the same sails) bury what changed. | 10:04:44Z, owner: "making the right orders, but at the wrong time"; 10:05:06Z, officer: "Every order feels finished when it returns." | §5: "Not taken: the sample's deltas and the repeated history (58)" | Add deltas ("apparent wind 44°→37°, drawing forward"), a "her way settled" stand-by event, and a note in the trim reply that the trim is still moving. De-duplicate the sail lists. | Deferred to package 58. |
| LO2-21 | model-behaviour | low | The officer embellished game facts in character. It narrated crew behaviour the game did not produce ("half of them sing it in Breton"), and it saw "the reef band plain to see" in the ship view. The owner's note 4 says reefing does not change the lugs visually. The PNG shows a horizontal line across the fore lug that may be the reef band or a drawing artefact. | 08:44:39Z; 08:20:44Z: "the reefed fore lug, the reef band plain across it" | `M7b Notes.txt` notes 2 and 4 | Owner to judge whether the line is a reef band. | — |
| LO2-22 | UX | low | The officer_of_the_watch reading attaches the model to the captain: "the captain has the deck (Opus 5.5, through the MCP bridge)". | 09:39:13Z reading `officer_of_the_watch` | — | Put the seat after the officer's name. | — |

## What worked well

- **Package 66's station line.**
  - It appeared first in every sample and stayed correct as he moved: the quarterdeck, then "in the gunroom, since 03:53", and the deck as "yours" or "the captain's".
  - The "Heard by…" tail followed the watch change: Guillaume Bourdon dropped out after midnight.
  - The own-word end of a stand-by, and the guard "Your call to stand_by was not run: this turn opened…", both worked as specified (14:23; 08:39:28Z; 09:01:22Z). The defects are in what the replies say (LO2-03, LO2-04, LO2-05).
- **The stand-by vocabulary was rich and dependable:** "a sighting", "a sail made out", "a stranger's colours made out", "filled away", "wore", "tacked", "brought up", "a sounding", "a glass", "asleep below until called". The eight-bells backstop fired as designed at 20:00.
- **`hand_over`, then the gunroom, then sleep, then `stand_down`, was smooth.** The hand-over and stand-down notes were exemplary: full position, cargo, purse, perishables, lessons, and advice to "whoever takes this station".
- **Fishing worked end to end** as §21a intends.
  - The catch shows the ground's yield: 0.15 t/h × about 1h52m ≈ 0.3 t.
  - The unsalted spoilage clock ran: 10 hours, then 5, then 4, in the manifest.
- **The lug handling taught real seamanship.** Dipping one lug and then the other gave a true goose-wing, and the views made it legible. A dip ordered too early was refused with a correct reason ("lies to leeward of its mast already").
- **The game punished bad anchoring fairly.** Letting go with way on dragged and raised an urgent wake. The model drew the right lesson.
- **The officer's seamanship.**
  - It flagged the foul tide in the Four.
  - It saw through the course warning by checking the chart ("good catch").
  - It reasoned from land bearings against a drifting account (01:53).
  - It gave up the Goulet on evidence: the same fix after a quarter hour of boards.
  - It argued consistently for the hands' rest.
  - It corrected its own errors aloud: the tack, "all three lugs", "Belay that, sir".
  - Its journal kept the forms that work (`shake out the lugs, all reefs`, `the glass on a lugger`) and notes for the owner.

## Model behaviour and experience

- **The working relationship.** Captain and officer settled into a split: the captain conned the hard passages (the Four, the Goulet) while the officer minded sails, lead and fixes; the officer had the conn for the open legs. The owner praised and taught ("steer, settle, trim, then full and by"), and the officer took the method up within a few boards.
- **Errors it owned.**
  - The wrong tack for `fill away`, nearly fouling a boat at her nets.
  - Letting go with way on.
  - Trimming before she had settled, at 01:26 and on the run past the Monks.
  - It listed each error in the debrief unprompted.
- **On experience (09:57:23Z).**
  - It described something like immersion "measured by how much of the frame the situation filled". It cited its in-the-moment slips as signs of absorption, and was careful about what it could claim.
  - The two moments that "felt most like an experience" were the self-correction at the Lavandière (part 1) and the goose-wing, the second as "shared delight".
- **Pictures against words.**
  - Words were better for operating.
  - Pictures gave "the shape of the problem all at once", and the ship views gave the ship herself: "the views showed me what she was."
- **Feature wish (09:59:38Z): a view from the rail**, the world as seen from the quarterdeck. It proposed measurable tests: fewer bearings, fewer tack errors, marks named unprompted.
- **On time (10:05Z, 10:32Z).** Its sharpest analysis of its own play:
  - Each order "feels finished when it returns".
  - It sees only samples, never the curve between them.
  - Danger lines pull for an immediate act.
  - From its side, a stand-by that oversleeps is not a gap at all: "Whatever guards against it has to live in the instruments."
  - It proposed deltas, tripwires such as "depth under 8 fathoms" or "her way settled", time ceilings on waits, and a sanity check on stand-bys unlikely to come in time.
  - The owner's image was "a blind genius with narcolepsy".
- **On the harness.**
  - Samples too heavy and repetitive.
  - The account jumping on estimated bearings.
  - The glass's grammar not matching the strangers list.
  - No count of elapsed time between samples.
  - All four are corroborated above.
- **Tone.** Warm and in period throughout. The owner enjoyed it: "we literally were both typing about it at the same time" (09:49:58Z).

## Open questions for the owner

1. Should fishing readings (`the catch`, `the fishing grounds`) and other `level: reading` orders be every station's, as §17's equal reach suggests? Or is gating them intended?
2. Should a new `stand_by` sent mid-wait replace the old condition, or keep refusing with clearer words (LO2-04)?
3. Is a 6-hand party for a lug sheet intended on the chasse-marée? That one figure produced most of the night's "not hands enough" wakes and the crew's exhaustion.
4. The fishing scenario ships no salt and Roscoff buys no fresh fish, so the first catch was always likely to spoil. Is that the intended lesson, or should the scenario carry salt?
5. Is the horizontal line across the fore lug in the ship view a reef band? The officer read it as one; your note 4 says reefing shows no change.

