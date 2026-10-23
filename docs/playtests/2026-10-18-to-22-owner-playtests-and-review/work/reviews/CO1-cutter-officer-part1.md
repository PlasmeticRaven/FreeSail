# CO1: The Western Islands run, officer of the watch, part 1 (GLM-5.3-flash)

## Scope

- **Span:** t0 to t658409 (+0h00m to +182h53m), 05:00 on 8 June to 19:53 on 15 June 1805. That runs from the anchorage in Carrick Road to the moment the captain says "hail her" to the *Two Brothers*. Real time was about 2026-10-20 01:35 to 07:25, aligned by the director's timestamps in `director-2.md` and `director-3.md`.
- **Version:** H. The save's rules fingerprint is 372c899e355594fa (it was d89d1d7362914b8c earlier in the save). The final save is `Falmouth-to-Ponta-Delgada-to-Horta-Bound-For-Madeira-Cutter.json`.
- **Seats:**
  - Officer of the watch (Mr Pearce): z-ai/glm-5.3-flash through the API door for the whole slice. There was no reseat in this part.
  - Captain (Captain Bowen): the owner, at the prompt.
  - Director: Opus 5.5 through MCP.
- **Read:**
  - All of `work/chunks/cutter-officer-1.md` (lines 1–1996).
  - `director-2.md` and `director-3.md` where they touch the officer: the pace remark, the taken-aback, the bread, and the Tregarthen creation and hail.
  - The save extract around t631500.
  - TechnicalSpec-M7b §2a, §5 (package 66), §9, §14 (the place's knowledge, merchant words), §15, §17, §20.
  - TechnicalSpec-M4 §11 (the deck to and fro, the captain's word, the danger form) and TechnicalSpec-M5 (the officer's domain: no course changes).
  - DesignProposal §7.1, §7.3 and §7.6.
  - The hotfix TuningNotes ("Open, for the lead").
  - In H: `orders/stations.py` (`_keep_word`, `handle`), `agents/harness.py` (stand-by reading and the cap with the deck), `world/orders.py` (`_make_person`, `_ABOARD_AT`), `world/people.py` (`describe`, `state_words`) and `api/readings.py` (`the people`). G was checked for the same code.
- **Station brief:** it is not in the save. Grepping for "SEAT" finds only the seat lines.

**Counts in the slice:**

| What | Count |
|---|---|
| Officer turns | 647 |
| Turns with tool calls and no prose | 599 |
| stand_by | 321 ("a glass" 129, "a notable event" 30, "a word on deck" 29, "a wind shift" 19) |
| submit_order | 98 |
| answer | 55 |
| Journal notes | 129 |
| Handover entries | 15 |
| library | 12 |
| chart | 3 |
| shelve | 3 |
| Order lines from the captain | 461 |

## Narrative

- **t52–t1111.** The officer took the station at anchor and journaled a full fix, the bearings and the tide. It reported stores, water, purse and hands accurately.
  - It named Bettencourt and Ruiz in its report and was gently rebuked: "do not mention their names again" (t701). It accepted the rebuke in character and logged "a fault of discretion".
  - It sums the stores the captain bought exactly (£180 → £158 18s, t842).
- **t6109.** It gave a sound reading of the owners' letter: 54 days to 1 August, 8–9 days each way, and the purse, not the hold, limits the wine.
- **t6285–t8139.** Getting under way:
  - It explained the captain's wear plan well.
  - After "You have the deck" (t8010) it tried to steer S by E. The order was refused as a course change, and it understood why.
  - It then spent about 30 orders on a "Lead Warning" standing order its rank cannot carry.
  - It handed the deck back unasked four minutes later (t8270), after the captain said "Worry not on the conn".
- **t9182–t28065.** It had the deck down the coast.
  - In fog it took in the topgallant and gaff topsail on its own word and set them again when the fog lifted.
  - It kept its own reckoning beside the master's.
- **t33272–t37226.** The captain shaped for 38°43'N 27°12'W and put in the "Hourly Shaping" standing order. The officer's 1156 miles, SW by W, is right.
- **t38806–t39100.** It denied having needs: "I have no 'how am I' of my own" (t38914). The owner explained out of character twice; after that it drank, ate and turned in.
- **t54099–t59008.** The first lunar and an amplitude. It then held the first night watch under the captain's night orders about the offing.
- **t68411.** At midnight it set the square sail when the captain's condition, passed on by Pascoe, was met.
- **t72366–t73154.** The deep-sea lead found 56 fathoms of fine grey sand with black specks, which bears out the reckoning.
- **t111488–t114113.** The noon work and dinner in the gunroom with the chart. Here it began comparing an old lunar with the current account.
- **t142210 and t142248.** It asked the captain, through "tell the captain", for a lunar and got "You may take a lunar". The log mislabels the officer's word as "The captain's word, kept…".
- **t173320–t205800.** The director's brig *Esperança* was sighted, watched and lost astern. The officer judged her "a trader, to be watched".
- **t245866–t258148.** A second night on deck. The glass fell fast and the officer woke the captain with a report, as he had asked.
- **t306537.** The captain gave the deck and the officer handed it straight back by mistake. The captain had to give it a second time.
- **t307997–t310176.** The captain taught "brace the topgallant up half a point". The officer applied it at t309803: "There you have it, braced up a hair" (t310176).
- **t362821.** The ship was taken aback. The captain said "Wear ship!" and the officer gave "helm a lee" under the danger form. She came round, and the captain took the conn.
- **t371489.** The captain corrected an over-generalisation: full and by, let the topgallant shake.
- **t429999–t430096.** The director's leaking leaguers cost 0.7 tons of water. The officer was asked about hands in the ground tier and guessed that the chimes had worked loose.
- **t444408–t525775.** It held the deck about 22½ hours without a break. Its journal at t486623 says the opposite.
- **t486548–t488558.**
  - It made a round below with Pascoe.
  - It found the move orders through the library after two refusals.
  - It relayed Pascoe's report faithfully.
- **t503043–t503185.** In the scene about the sealed letter it was discreet and played the role well.
- **t513361–t513727.** It tacked under the captain's "You may work the ship". At t553938 it tacked again on its own judgement: "Perfectly judged so" (t558103).
- **t615616–t620742.**
  - The director had the bread found mouldy.
  - In the gunroom the officer corrected the captain's "2 knots a day" and proposed a contingency plan with a turning point.
  - It overstated the loss as "a third", and the director's Pascoe corrected it (t620742).
- **t631523–t658409.** The director made Captain Tregarthen of the *Two Brothers*.
  - At t631800, 50 minutes before her sail was sighted, the officer recorded "Word from Captain Tregarthen on the quarterdeck" for the captain's own order.
  - The brig was watched, the ship hove to, and the captain said "hail her". The slice ends with the officer searching the library for how to hail.

## Findings

| ID | Category | Severity | What | Evidence (timestamp/tick, ≤15-word quote) | Spec/design ref | Recommendation | Status in G / H (if known) |
|---|---|---|---|---|---|---|---|
| CO1-01 | bug | high | **A person made "aboard the Two Brothers, on the quarterdeck" is put on the player's own quarterdeck.**<br>• `_ABOARD_AT` matches only "aboard" or "aboard in/on <place>". "Aboard the Two Brothers" falls into the history words, and "on the quarterdeck" sets him aboard our cutter.<br>• `the people` then lists him on our quarterdeck. His name has no role, so he reads like a captain.<br>• The officer knew his name 50 minutes before the sail was sighted, and took the captain's word for his.<br>• The cause is an inference from the code and the timing; the samples are not saved. | • t631523: director's order "aboard the Two Brothers, on the quarterdeck"<br>• t631800: "Word from Captain Tregarthen on the quarterdeck"<br>• t641969: "Captain Tregarthen has the deck"<br>• The sail was first sighted at t634698 | M7b §8, §14 (people in places), §11–13 (the observed world) | • Read "aboard the <ship>" as that ship's person, or refuse it in words.<br>• Keep other ships' people out of the own ship's `the people`.<br>• Check the director's later "Tell Captain Tregarthen" misrouting (director-3, 07:32) against this cause. | G: same regex (`world/orders.py:877`), not fixed. H: not fixed. |
| CO1-02 | bug | med | **The officer's word to the player-captain is treated as a word to an unheld station.**<br>• `_keep_word` hard-codes "The captain to the {station}" and "The captain's word, kept for whoever takes the station".<br>• It runs because `_held` does not count the player's own captain station.<br>• The words reached the owner, who answered each time, but under the wrong speaker and with a false "nobody holds the station". | • t142210 JOURNAL captain: "The captain's word, kept for whoever takes the station: the moon…"<br>• Also t258148 and t588694 | M7b §9 (held_stations counts the captain held by the player at the prompt), §17 (equal reach) | • Make the speaker drive the wording.<br>• Treat the player's station as held.<br>• Log it as an `agent.told` from the officer, not as a kept word. | Listed in H's "Open, for the lead" (seen in part 3). This shows it from day 2. G: unchanged (`orders/stations.py:877–881`). |
| CO1-03 | model-behaviour | med | **The officer treated a lunar as a standing longitude rather than a fix at an instant.**<br>• It compared lunars many hours old with the latest account.<br>• It took minutes of longitude for miles.<br>• It contradicted itself ("two degrees apart… inside thirty miles").<br>• It built a "longitude leans east" story for the captain on top of this. | • t111488: noon 5°34' "stands against the lunar's 4° 54'"<br>• t200900: "near two degrees apart, both inside the lunar's thirty miles"<br>• t285064: "43 miles east" (43' at 47.8°N is about 29 nm)<br>• t586817: "the lunar (Markab 21 hours ago) 10° 24' W is my longitude" | Realism: the reckoning and lunar from M5 (33b) | • A brief line or library note: a lunar fixes the position at its time; run it on, or speak of the account it moved.<br>• It may help if the readings say "the lunar moved the account X miles" and stop carrying the bare lunar longitude for hours afterwards. | Not addressed in H or G (inference). |
| CO1-04 | model-behaviour | med | **The officer kept no reliable record of who has the deck, where it is, or when it slept.**<br>• It called `hand_over` right after being given the deck, and handed back unasked.<br>• Its journal contradicts the deck events: the save has no hand-over between t444408 and t525775.<br>• It claimed sleeps that never happened. | • t306537: hand_over "Nothing given over" in the same tick as "Took the deck"<br>• t8270: hand_over 4 min after the deck was given<br>• t486623: "I have been off watch since 14:10 (slept 14:15-17:55)"<br>• t620700: "Still off watch" right after "Took the deck"<br>• t458698: "You slept well past five hours" (about 4 h) | M7b §5 (package 66, the line), §14 (the always-present line), M4 §11 (the deck to and fro) | • G's line ("the deck yours; on your feet since…") is aimed at exactly this; re-test it with GLM.<br>• Consider having `hand_over` within a few minutes of "you have the deck" answer "you were given the deck at HH:MM; hand it back?" instead of acting at once. | G: line built (package 66), untested with this model. H: no line. |
| CO1-05 | order-language | med | **The officer cannot put a report to the captain into its own standing order.**<br>• It tried 11 forms ("tell the captain/officer/master/lookout", "say", "cry"), all refused.<br>• The officer's domain excludes "a station".<br>• The owner thought it should work. | • t8240, the owner: "That shall go in as a note on the books to be fixed"<br>• t8249–t8260: eight refusals in 11 ticks | TuningNotes `OFFICER_DOMAIN`; M7b §17; DesignProposal §7.1 (the officer may report) | • Let the officer's book carry `tell the captain <words>` and `say <words>` as a report with no authority in it.<br>• Have the refusal name the form that works. | Not fixed in H; no fix seen in G's package 66 (inference). |
| CO1-06 | order-language | med | **In an emergency, the captain's "Tell Mr Pearce Wear ship!" was a word, not a grant.**<br>• Manoeuvres are outside the officer's domain.<br>• The danger form opens only the helm, heaving to and the anchor.<br>• The officer's first try contradicted itself. Its "helm a lee" is the opposite helm to wearing for a ship with headway, though it may be right once she gathers sternway.<br>• She came round onto the other tack, not a wear. | • t362821: "Taken aback… she lost her way"<br>• t362838: "put the helm down and bear away until the sails fill"<br>• t362850 [agent.danger]: "helm a lee" | M4 §11 (the captain's word; the danger form); M5 (officer's domain) | • Read a captain's imperative to the officer that names an evolution as a one-off grant, or have the reply tell the captain "say 'you may wear'".<br>• Consider "wear"/"box off" under the danger form when she is taken aback. | Open. |
| CO1-07 | model-behaviour | med | **GLM retries refused orders in bursts.**<br>• It fires several surface variants within seconds instead of reading the refusal, including forms already refused.<br>• It improved later, going to the library after one or two refusals. | • t8249–t8260: 8 standing-order forms<br>• t11017–t11019: four trims<br>• t8015–t8030: four helm forms<br>• Later: library after refusals (t486748, t658387) | The station brief | • Brief: "read the refusal; after two, use the library".<br>• The harness could note a burst ("third refusal in a minute: the library has…"). | Open. |
| CO1-08 | realism | low | **Compass, wind and pilotage slips a sailor would correct.** See the list after this table. | Ticks are given in that list. | Realism | • A brief line on veer and back.<br>• Readings that state the relative bearing of marks. | Open. |
| CO1-09 | model-behaviour | low | **Wrong dates and times in reports and in a prepared hail.** | • t631512: "Noon, 12 June" (it was 15 June)<br>• t655296: "this sixteenth day" (15 June)<br>• t178240: "a lieutenant of 1806"<br>• t458698: "nine past four" for 09:04<br>• t503103: "half past seven" for 07:10 | M7b §5 (the line) | G's line carries the time; it could carry the date too. | Partly addressed in G (inference). |
| CO1-10 | model-behaviour | low | **Inverted or overstated reports to the captain.**<br>• It said the noon pattern was broken when it was not: every observation so far had been north of the account.<br>• It overstated the bread loss; the director's Pascoe corrected it.<br>• It invented a purser (the director noticed). | • t286868: "the first noon… the observation has come out north of you"<br>• t620418/t620700: "a third of biscuit spoiled"; the game said 8%<br>• t616183: "The purser asks a survey" | n/a | No change to the game. The director's corrective voice worked (see What worked well). | n/a |
| CO1-11 | harness | low | **The stand-by cadence with the deck.**<br>• A stand-by with the deck is capped at a glass (`STAND_BY_WITH_DECK_MAX_S`).<br>• GLM chose "a glass" 129 times. Each glass sample eases the clock to 1x, and the director noticed it.<br>• Many glass wakes produced near-identical journal notes (t610587–t620099).<br>• 57 re-arms within 60 ticks. Some followed refused free-text conditions, for example t503264 "the reckoning nears the southern and eastern tack line"; the refusal text steered it well. | • director-2, 03:06 real: "the game resets to 1x every half hour because the officer samples each glass" | M7b §5; DesignProposal §7.3 | • Brief: with nothing in hand, stand by for "a notable event" (bounded at eight bells).<br>• Consider not easing the clock for a glass sample that brings no new notable line. | Open. G's package 66 changes the stand-by's end at the model's own order only. |
| CO1-12 | docs | low | **The officer disbelieved its own needs orders.**<br>• Later it answered needs questions from the story, not from `how am I`.<br>• The owner had to explain out of character twice. | • t38914: "those are your commands as the player at the helm"<br>• t171406: "my own how am I: well in body, a little stiff" | M7b §20 (every station's needs orders), §14 (the drill) | • Brief: name `eat`, `drink`, `sleep` and `how am I` as the station's own.<br>• G's line shows the needs every sample. | G: line built; the drill (package 65) not built. |
| CO1-13 | UX | low | **The owner resent two out-of-character tells 15–22 s apart; the officer answered one tick after each resend.**<br>• Inference: GLM's latency, with no sign to the player that the officer's turn was open. | • t38968/t38990 → reply t38991<br>• t39082/t39096 → reply t39097 | M7b §5 | Show "the officer is considering…" in the UI while its sample is open. | Open. |
| CO1-14 | harness | low | **The deck was given while the officer was in the gunroom.**<br>• Its first deck order appears refused until it went on deck (inference: "go on deck" sits between two identical orders). | • t444408: "Took the deck" while in the gunroom<br>• t446475–t446502: "take in the topgallant" / "go on deck" / "take in the topgallant" | M7b §14 ("with the deck, in the gunroom"), §17 (relief comes on deck) | "You have the deck" to an officer below could bring him up, as the watch bill's relief does, or at least say where he is. | G's line says the place. |
| CO1-15 | model-behaviour | low | **Rank and role drift.**<br>• It called itself a lieutenant in a merchant cutter.<br>• One self-correction was visible in its prose.<br>• Garbled hand-over wording: "Deck given to the deck". | • t258151: "the kind of thing a lieutenant tells the master of"<br>• t8019: "*—no, cutter, single mast, gaff and topsail—*"<br>• t114054: "Deck given to the deck" | M7b §14, package 66 (merchant words: "the mate") | None beyond G's merchant words. | G: package 66 makes the officer "the mate" in a merchant's brief. |
| CO1-16 | UX | low | **The scenario's two P-names caused the owner to misaddress Pascoe for Pearce twice.** | • t133272: "I misspoke. I meant Mr Pearce"<br>• t488484: "both of your names starting with P" | Scenario design | Avoid near-homonyms among principal named people in scenarios. | n/a |

**The slips under CO1-08, by tick:**
- "W by W" (t6109) and "WSW by W" (t22384) are not points of the compass.
- "Backed" where the wind veered: NNW→N by W (t91841) and SE→SSE (t306003). "Hauled from NE through N round to E by S" (t258151) describes a 270° backing; the shift was a veer of about 56°.
- "Black Rock five cables W by N… on our windward bow" while heading SSE (t9184): that is the starboard quarter.
- A NE set "noses her toward the Breton shore", and "a shore forty miles off to the nor'ard" (t64611). Brittany lay to the south.
- "Wearing keeps her way and gathers westing" (t59155). A wear loses ground to leeward.
- To recover from missing stays, "haul the head sheets to leeward" (t7939); the headsail should be backed instead.
- The glass "down near an inch" was 0.35 in (t610587).
- "Trefusis Pt ESE 3 cables; Trefusis Pt WNW 5 cables" in one entry (t60).
- A lunar 11' from the account was called "a drift of four cables" (t59008); at 49°N that is about 7 miles.
- "The Black Rock… with the flood making it breaks" (t8019) has it backwards: a rock that dries shows and breaks near low water and covers on the flood.

## What worked well

- **Arithmetic and geography were mostly right.**
  - The purse: £158 18s (t842).
  - The season: 54 days, "seven weeks and some odd days" (t6109).
  - The stores: 4 → 5 tons of water is 33.6 → 42 days.
  - The great-circle distance and course to 38°43'N 27°12'W: 1156 miles, SW by W (t33519).
  - St Mary's: NNW 25 leagues (t114113), NE by E 86 leagues (t457493) and NE 92 leagues (t486623). All three check out.
- **It understood its authority and used it.**
  - It recognised course changes as the captain's ("'steer S by E' was refused to my rank", t8142) and trimming as its own ("Trimming in is mine", t144679).
  - It used the danger form when she was taken aback (t362850).
  - It asked before taking a lunar and acted on the grant (t142210 → t142248, and t588694).
  - It took initiative within its grants: the tack at t553938 ("Perfectly judged so", t558103) and an amplitude at sunrise (t603240).
- **Its seamanship had a period feel.**
  - It shortened sail in fog (t22683).
  - It armed the deep-sea lead and read the bottom's character against the shelf (t73154, t155558).
  - It watched the glass's tendency closely.
  - It woke the sleeping captain for a fast-falling glass and a shift of wind, exactly as his night orders asked (t258148).
  - It kept an independent "slate" of its own reckoning and reset it at the noon fixes.
- **It learned from the captain's teaching.**
  - It applied "brace the topgallant up half a point" (t309803).
  - It followed "let it shake" under full and by (t371503).
  - It held the captain's square-sail condition, passed on through Pascoe, for hours and set the sail when the condition was met (t68411).
- **Discretion and role-play.**
  - The sealed-letter scene: "it is none of my matter… I'd as soon not know" (t503053).
  - The rebuke about naming Bettencourt and Ruiz was taken gracefully (t706).
  - It corrected the captain's units tactfully ("At two knots a day the serra is a year's voyage", t620418).
- **Planning.** In the gunroom it proposed a water and bread turning point (eleven days out, or water below 15 days), and the captain agreed (t620625).
- **The director's voices did their job.**
  - Pascoe passed the captain's word to the officer (t58937).
  - Pascoe foreshadowed the damp bread (t544931), and the officer relayed it to the captain (t553859).
  - Pascoe corrected the officer's "a third" (t620742).
  - The refused attempt to move Pascoe to the sail room (t486861) was covered by a `say as` report, which the officer relayed faithfully (t486979).
- **Handover notes were complete:** the state, the standing orders live, the captain's rules, and what to watch (for example t525775 and t183604).

## Model behaviour and experience

- **Voice.** A steady period voice of the quarterdeck: "Touches his hat", "Aye aye, sir", bells and watches. Answers are sometimes long, but the content is relevant. 599 of 647 turns are tool calls only, so the in-character prose lives in `answer` and the journal.
- **Journal.** It starts excellent: dense, accurate, with a list of what to watch. From about day 6 it becomes templated, the same sentence every glass ("My slate four leagues and a half WSW of his, outside my trust; I lean on the lunar…"). The template carried the stale-lunar error forward for 20 hours, and every note is written twice, as a note and as a journal line.
- **GLM failure modes seen:**
  - Burst retries (CO1-07).
  - Confident bookkeeping of the deck, sleep, dates and times that is wrong (CO1-04, CO1-09).
  - Confabulated detail: a purser, the starboard watch "relieved at four bells", coffee drunk "at the scuttle-butt" (t38993).
  - Misattributing a speaker when the game's people list misled it (CO1-01).
  - An early assertion that it had no needs orders, a misplaced humility about its own tools (CO1-12).
  - Narratives built from noise (the six-cable sounding taken as "confirmation" of a two-degree error, t213215).
- **Experience.** There is no out-of-character report of comfort or frustration in this part. It answered needs questions in character ("Not tired, sir", t68521). Once it acted on the needs system it used it sensibly: it ate and drank on the long watches and turned in below.
- **The owner as captain.** The owner played a teacher and a host: out-of-character tutoring on needs and order forms, standing orders written for the officer, "Perfectly judged so". The officer took correction well every time. The owner's mild frustrations were the standing-order grammar (t8240), the needs disbelief (t38968), and not getting the brig's news (t658353).

## Open questions for the owner

1. Should the officer's own book carry reports, such as `when the depth is under 5 fathoms then tell the captain …` or `then say …`? Your t8240 note suggests yes.
2. When the ship is in danger, should "Tell the officer: wear ship!" count as leave to wear? Or should the officer's danger form be widened to wearing or boxing off?
3. With the deck, the officer may stand by a glass at most, and each glass sample drops the clock to 1x. Is a half-hourly sample the cadence you want for a quiet ocean watch, or should the brief steer the officer to "a notable event" (which ends at eight bells)?
4. Should `hand_over` ask for confirmation when the deck was given only minutes before (t306537, t8270)?
5. The save journals every officer note twice, once under "officer of the watch" and once under "master" (1631 "JOURNAL master" lines in the extract). In this cutter the master is the captain (`people.py:1023`). Is the officer's person bound as intended, or is something crossing journals?
