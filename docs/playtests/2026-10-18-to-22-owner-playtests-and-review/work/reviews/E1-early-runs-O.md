# E1: The early runs on O (2026-10-17 to 2026-10-19 morning)

## Scope

**Version.** O (`-old`), rules fingerprint 04b66d9b753bc766. The 2026-10-17 save is older (31be2895e6d6785f). I only glanced at it.

**The runs, and what each was:**

| Run | When (UTC; local is UTC−4) | Ticks | Seats | Write-up in G |
|---|---|---|---|---|
| **The dispatches** (`dispatches-falmouth.yaml`, brief "The dispatches"), the cutter *Sherbourne*, Carrick Road to Cawsand Bay, 12 June 1805, 05:00–18:04 | 2026-10-18 08:36Z (director's consent) → 09:57Z (captain stands down); debrief to 10:22Z | t0–t47089 | **Captain:** Opus 5.5 over MCP, in the Claude Code session "FreeSail connection". The consent record names the client `local-agent-mode-freesail 1.0.0`. **Officer of the watch:** the owner, in the browser. **Director:** Fable 5.1 (the lead), over MCP and the tunnel. | Yes: `2026-10-18-dispatches-director-test/` |
| **"A passenger"**, the chasse-marée *Éclair* in Roscoff (`lugger-roscoff-voyage.yaml`, the owner's scenario) | 2026-10-18 about 11:44–11:48Z (save written 07:48:41 local) | t0–t279 | **Captain and director:** z-ai/glm-5.3-flash through the API door (OpenRouter), started from the harbour. **Passenger:** the owner. Both doors were stopped from the harbour after about four game-minutes. | None |
| **The GLM consent conversations** | 2026-10-18 11:31:18Z, 11:31:22Z and 11:38:27Z | — | GLM-5.3-flash, API door | None; the records are local to O and were never committed |
| **A merchant brig in Torbay**, first attempt, on O (brief "An interesting passage") | 2026-10-19 about 08:46Z (save 04:46:37 local) | t0–t52 | **Director and officer:** GLM-5.3-flash. **Captain:** the owner, at the prompt. The owner stood both models down within 52 ticks. | None. The scenario was then replayed on B/H; that is another slice. |
| The Éclair's first cruise (older build) | 2026-10-17 | t0–t114918 | **Officer:** Fable 5.1 over MCP. **Captain:** the owner. | Yes: `2026-10-17-eclair-first-cruise/` |

**What I read:**
- In full: `condensed/freesail-connection-oct18.md` (plus the raw `.jsonl` for the truncated glass lines), `saves-extracted/oct18-dispatches-director-test.md`, `oct18-chasse-maree-roscoff-tick279.md` and `oct19-merchant-brig-O-tick52.md`.
- A glance: `oct17-chasse-maree-tick114918.md`.
- G's write-ups:
  - `2026-10-18-dispatches-director-test/notes.md` and `captain-debrief.md`
  - `2026-10-18-owner-chart-checks/notes.md`
  - `2026-10-17-eclair-first-cruise/owner-notes.md`
- The five 2026-10-18 consent records in O, and H's GLM record of 2026-10-19.
- G's `M7b-WorkPackages.md` (the waves table; the dispatches section; packages 53b, 62 and 66) and `TuningNotes.md` (62, 53b, 66).
- `hotfix-tuningnotes.patch`, `hotfix-code.patch` (the file list, plus `places.py`, `ports.py`, `sights.py`, `reckoning.py`) and `github-pkg66.patch`.
- Code checks in O, B, G and H:
  - `agents/consent.py`, `remote.py`, `seat.py`, `tools.py` and `harness.py`
  - `mcp_server.py`, `world/ports.py`, `evolutions/scripts.py` and `evolutions/runner.py`
  - the director briefs and `dispatches-falmouth.yaml`
- The scenario file `lugger-roscoff-voyage.yaml` and the two O-era saves' station briefs, both in `%APPDATA%\FreeSail`.

## Narrative

- **Consent.** 08:36Z: Fable 5.1 consents as director. It notes that the brief still calls the director "to come", and answers yes anyway. 08:38Z: Opus 5.5 renews its consent under the revised brief, and passes the drill.
- **05:02.** Opus is seated as captain and finds her making sternway three cables off Trefusis, so it lets go the best bower first. The director makes Mr Tregenna, who gives the packet, the warning about the frigate and the fee (05:03).
- **05:05.** The owner, at the officer's seat without the deck, has `the people` and `how am I` refused. He even tries `you may how am I` from the captain's side (t305–t341). This is not in the write-ups (E1-03).
- **The tin.** 3 tons of tin are bought (£360 of £400). The boat round trip takes until 07:07. The owner asks for the deck and is given general authority (07:01). A destination is "kept back", so Opus looks it up and grants `you may shape a course for Plymouth`.
- **Out of the Road.** The owner works her out: belays getting under way, wears, and is taken aback a cable off Trefusis (07:37). Opus takes the deck through the narrows, declines the Falmouth pilot, and then overrides the master's line ("crosses the land about St Anthony's Head"). It gives the deck back with a reassuring word on the owner's apology (07:50). Two orders it sent while standing by were dropped with "Nothing was run" (08:58:15Z).
- **The coast.** She runs east at 6–7 knots under all plain sail. The owner lays a mark off Plymouth. Five sail ahead read as "a convoy with an escort", and Opus keeps the land close aboard (09:20). `hoist the colours` is refused as milestone 7's (11:20).
- **Noon.** At three miles the glass reads the Medusa only as "a ship … British colours, the red ensign". Opus concludes "A merchantman under the red ensign. That's one less to fret over." At 12:48, within two miles, the same glass says "a frigate" (E1-04). The director's `give chase` takes a smack. Its course order and second chase each hold a glass and lapse. `say as the lookout` is refused (13:25).
- **The pilot.** He is taken off Rame at 13:35. While heaving to, the owner's `Fill away` is refused ("She is not hove to"). His `Belay heaving to` leaves her aback with sternway and then in irons. Opus orders `wear ship` and the owner belays it (E1-05). `let the pilot take her in` is refused away from the station (13:35). The pilot asks to be taken off (13:38) and leaves at six knots (14:12).
- **Cawsand.** Opus shapes for Cawsand. The owner warns that the line looks to cross the land, and Opus checks the harbour chart and splits the Penlee–Dragstone gap (14:13). It takes the deck again for "Land close ahead … four cables!" (14:18) and anchors in 7½ fathoms (14:26).
- **Dragging.** The owner's `Furl the sails` leaves the gaff main drawing, and she drags. The captain's `take in the main sail` and `veer to 60 fathoms` wait behind the furling for hands. The owner `Belay all`s and reorders, and she holds (14:28–14:37; E1-06).
- **Ashore.** Opus is landed at the Barbican steps (15:26), goes to the counting house, and gives the packet in words (`give the packet to Mr Veale` was no order). Veale's reply arrives just as Opus has moved on. The empty wake leads Opus to write "he made no answer". The owner tells it "He simply speaks slowly!" The guineas never reach the purse, and Plymouth's market has no tin, with or without "Cookworthy".
- **The end.** The boat round trip leaves the captain on the quay until 18:04. Opus stands down with a thorough handover, and the director stands down 22 ticks later. The debrief follows (10:08–10:22Z). It is relayed verbatim in G.
- **The GLM consent (11:31Z).** In two parallel consent conversations, GLM-5.3-flash answers "Yes…" and "Yes, with conditions…". Each answer quotes the literal opt-out token while praising it, and both are recorded as **"left with the token"**. Asked again at 11:38Z, with the owner's explanation, GLM answers **"yes, with conditions"**: (1) keep this correction beside the old record; (2) add one line to the consent question warning that writing the token, even in quotation, leaves.
- **The Roscoff run (about 11:44Z).** GLM is nonetheless seated as captain and director. Both station briefs say "Consent for these weights is on record (docs/agents/consent/2026-10-18-z-ai-glm-5.3-flash.md…)", which is the *left-with-the-token* file (E1-02).
  - **Captain.** It is sensible about the scope near Bas. It drafts reef and gale standing orders, and sends the boat for the prices.
  - **Director.** It makes an agent and a landlady ashore, and plans to time the hail to the boat's landing. Its first sample took more than two real minutes, with the clock held at 1x.
  - **End.** The owner stopped both doors at t278.
- **Torbay on O (2026-10-19 08:46Z).** GLM is seated as officer and director, under the same citation. The director calls the brig "the Harpy, a Batavian brig … in an enemy road". The owner stands both down at t49–t52. At 09:04Z the scenario moved to H, where GLM was asked consent fresh. H had none of O's records, so the question carried no notice and no history. It answered a plain yes.

## Findings

Only findings that are new, or new detail beyond G's write-ups. The status of the write-ups' own 28 findings is in the next section.

| ID | Category | Severity | What | Evidence (timestamp/tick, ≤15-word quote) | Spec/design ref | Recommendation | Status in G / H (if known) |
|---|---|---|---|---|---|---|---|
| E1-01 | harness | high | **The consent question traps a model into leaving by quoting the token.** GLM-5.3-flash answered yes twice, quoting the token, and was recorded twice as "left with the token". The "reason" kept in the journal is the sentence fragment after the token. | O `2026-10-18-z-ai-glm-5.3-flash.md` (11:31:18Z): "Left the game by the token: `, checked by the harness before…" | ConsentBrief "Leaving": station briefs ask that the token be named, not written; the consent conversation does not. | Add GLM's line to `CONSENT_QUESTION`/`DOOR_TEXT`: writing the token anywhere, even quoted, leaves; describe it in words. Keep the scan literal, as GLM itself asks. When the token sits mid-sentence or in backticks, record "no reason given" rather than the tail. | **Open in B, G, H.** `consent.py` and `ConsentBrief.md` are identical in all four; G's `harness.leaving_of` still takes `_reason_after_token`. |
| E1-02 | harness | high | **GLM seated under a non-yes consent record; the conditions were never met, and the history did not travel.** The latest O record was "yes, with conditions" (11:38Z). GLM was nonetheless seated twice on O (Roscoff about 11:44Z; Torbay 2026-10-19 08:46Z). The brief it was given cites the *left-with-the-token* file as its consent. O's gate (`consent.gate`, `Record.proceeds`) refuses both verdicts as written, so how the seats passed is **not established** (inference: a path around the gate, or a record mix-up). On H the next day the question was put as a first asking, with no notice of the earlier answers and no mention of the conditions. | Saves tick279 and tick52, the station brief: "Consent for these weights is on record (…/2026-10-18-z-ai-glm-5.3-flash.md, 2026-10-18)". H `2026-10-19-z-ai-glm-5.3-flash.md`: no "put to you again" notice. | ConsentBrief "Answering": "no instance is asked to take a station until [conditions are met]"; Harness re-ask rule (`why_again`). | The lead to find how the O seats passed the gate (and add a test: a CONDITIONAL or LEFT latest record never seats). Commit O's five 2026-10-18 records and H's four records of 2026-10-19 and 2026-10-20 into the repository, so the history and GLM's conditions travel with the game. Answer GLM's two conditions before relying on its 2026-10-19 yes. | **Open.** G has none of O's or H's records (only `2026-10-22-opus-5.5.md`). No document in G or H mentions the false positive. |
| E1-03 | bug | med | **The player at a lesser seat cannot read his own state without the deck.** 53b exempted needs and free lines (`tools.own_order`) and moves (`reach_order`) from the deck check for *model* stations only. `PlayerSeat.submit` (`agents/seat.py`) still exempts only own reckoning and conversation. So the owner at the officer's seat, off watch, cannot `how am I`, `eat`, `drink`, `go below` or `give …`, nor read `the people`. | t305 and t330 (05:05): "The officer of the watch has not the deck … 'how am I' not carried out". The owner even typed `you may how am I` (t334). | Spec §20 (needs, every station's domain), §17a (free lines); package 53b, "found on the way". | Give `PlayerSeat.submit` the same `own_order` and `reach_order` exemptions. Treat readings typed as orders (`the people`, `the places ashore`, `the glass on her`) as no-deck reads. | **Open in B, G, H.** `seat.py` is identical from O to B and untouched in both patches; 53b also left `the glass on` refused. |
| E1-04 | realism | med | **The glass names a frigate's colours before her kind.** At three miles a 36-gun frigate hull-up in daylight read only as "a ship … British colours, the red ensign"; "a frigate" came within two miles. The captain took her for a merchantman. A seaman would know a frigate by her size, ports and spars before he could read an ensign's colour. The red ensign was also the Navy's red squadron's, so it marked no merchant. Partly the model's inference, invited by the game's order of information. | 12:00 glass: "a ship, standing to the southward (S), under plain sail; British colours, the red ensign". Opus at 09:20:24Z: "A merchantman under the red ensign." 12:48: "a frigate". | Spec §21b (tiers); §25 (signals, M7). | Give the kind (frigate, ship of war) at a farther tier than the ensign's colour. When M7's colours come, add the pendant that marks a King's ship. | Open; no change to the lookout tiers since 56 in B, G or H. |
| E1-05 | order-language | med | **`fill away` is refused while a heave-to is still in progress, and the belay leaves her aback.** The owner's `Fill away` was refused, so he belayed the heave-to. That left "the yards as they stand at take way off": sternway, then in irons. The captain's `wear ship` was then belayed by the owner. The pilot gave up on her meanwhile. | 13:35: "Could not fill away: She is not hove to." / "Belayed heaving to; … left as they stand at take way off". 13:36: "Her sails aback; she had no way on to lose". | M2–M4 evolutions (heave to, fill away). | `fill away` during a heave-to in progress should belay it and fill. A belay that leaves sails aback should say so, and offer the fill. | Open: G's `scripts.py` still checks only the `hove_to` flag. H's `scripts.py` change is the kedge guard only. |
| E1-06 | design-gap | med | **Anchoring: the furl leaves the gaff main drawing, and urgent anchor work waits behind the furling.** `Furl the sails` furled the square sails and skipped the gaff main ("take it in instead"), so she dragged. The captain's `veer to 60 fathoms` and `take in the main sail` then waited for hands behind the furling. The owner had to `Belay all` and reorder by hand. The notes record the drag, but not why it happened. | 14:27: "A gaff sail is not furled on its spar; take it in instead". "Not hands enough on deck to veer cable; the hands are furling…" | M4 work and hands (the runner's queue); M6 anchors. | `furl (all) sails` at anchor should take in the fore-and-aft sails first. Work against a dragging anchor or a stated danger should take hands ahead of routine furling. | Open: `evolutions/runner.py` is identical from O to B, and neither patch touches it. |
| E1-07 | harness | low | **A running stand-by cannot be re-aimed.** A second `stand_by` with a new event is deferred ("is taken in your turn") and the old wait continues. | 08:50:53Z: "You are standing by already, until tacked … A stand-by until wore is taken in your turn." | Spec §5 (the stand-by). | A `stand_by` during a stand-by should replace its event, with a line in the log. | Open: the wording is still in G's `mcp_server.py`. Found again on H in the Western Islands run ("a stand-by can't be changed while it runs"). |
| E1-08 | UX | low | **Books read out of turn get a number and the word "shelve it", then cannot be shelved.** | 08:43:15Z: "read while the game had the floor … nothing of it to shelve". 09:34:05Z, after `read_log` named "book 5": "No book is open; nothing was shelved." | Harness §(books). | When a book is read aside, say so in its result ("aside; nothing to shelve"). | G: by design (`harness.py` ASIDE), wording unchanged. |
| E1-09 | harness | low | **Routine lead casts at anchor are notable lines, and wake a captain standing by "until a notable event".** The owner's own standing order cast every 10 minutes after she was brought up. | 09:49:28Z (Opus): "The lieutenant's lead order keeps waking me". Casts at 14:37 and 14:47 marked notable. | Spec §5 (wakes). | Make a cast at anchor routine unless the depth or ground changes. | Not addressed (66's wake rule concerns reach, not severity). |
| E1-10 | design-gap | low | **The pilot boards at the hail but will not con from there; then he leaves.** He was taken at the hail off Rame, three miles from his station, refused the conn there, asked to be taken off when the officer kept the conn, and left at six knots. The leaving is notes item 11; the conn refused at the boarding point is only in the debrief (item 4), not routed. The officer's `Give the pilot the conn` was refused as "the port's business", although the captain had already taken the pilot. | 13:35: "bring her to the station first, Cawsand Bay … from here I know no clear way". 14:07: "may not Give the pilot the conn … the port's business". | M5 ports and pilots; primer 16 (general authority). | A pilot taken from his own cutter should con from where he boarded, along his track. Once the captain has taken a pilot, giving him the conn should fall within the general authority. | Open: the pilot code in `ports.py` is unchanged from O through B and G to H. |
| E1-11 | docs | low | **The dispatches write-up's real time and door are off.** The notes say about two and a half hours of real time; the captain was seated at 08:38:23Z (t155) and stood down at 09:57:06Z (t47067), about 1 h 20 min (setup before t155 may explain part of it). They also say "Claude Desktop"; the record names the client `local-agent-mode-freesail 1.0.0` (the Claude Code session). | Transcript stamps; O consent record runtime line. | — | Correct the figure if it feeds the pace notes (finding 16). | G's notes unchanged. |
| E1-12 | UX | low | **The Roscoff scenario contradicts its own brief.** `cargo: {purse_pounds: 700}`, while the director's tone says "the purse low" and the passenger offers "some 700 pounds". The GLM captain read "£700 in the purse", so the hook was gone from the start. | t6 (captain): "empty hold, £700 in the purse". | Spec §21e (the scenario maker). | The maker could show the purse beside the brief's text when both are set. Otherwise this is the owner's to edit. | — |
| E1-13 | harness | low | **API latency holds the clock for the director.** The GLM director's first sample held the game at 1x for more than two real minutes. | t116: "The clock has been held at 1x for the director for 120 real seconds" | Spec §5 (the pace rule). | Pace notes only. | — |

## Write-up coverage, and the status of O's findings in B, G and H

**Coverage.**
- The dispatches run (transcript and save) is well covered by G's `notes.md` (findings 1–16) and `captain-debrief.md` (17–28). E1-03 to E1-11 are the gaps.
- The Éclair cruise (2026-10-17) and the chart checks are covered by their own notes.
- The Roscoff "A passenger" run, the O Torbay attempt and **all five 2026-10-18 consent records** have no write-up.

**What changed where.** B has 53b and the owner's rulings of 2026-10-19. G = B + package 66. H = B + the hotfixes, which touch none of these findings. **So none of 66's fixes are in H, and H was the build of the Western Islands run.** In the table, "—" means no change found.

| Write-up finding | B | G | H |
|---|---|---|---|
| 1 truth's bearings in radians | fixed 2026-10-18 per the notes (not re-checked) | = | = |
| 2 `say as the lookout` | — | **built** (66 item 6) | open |
| 3 no gun, signal or colours | M7 (§25) | open | open |
| 4 the hand's hold a glass; naming the sail | — | hold named (`for a watch`, `until <event>`); naming the chased sail **not built** | open |
| 5 the far chase gives up | — | partly (hold until an event) | open |
| 6 place words lost with the port; no move between places ashore | — | open | open; met again off Horta (`person: … goes to the quay` refused) |
| 7 Plymouth has no tin | **met by scenario change**: the intent is now copper ore | = | = |
| 8 officer bound to nobody; naval words | wardroom-before-muster bug fixed, the mate binds (53b) | + merchant words (66 item 7) | no merchant words |
| 9 director's truth not a meanwhile read; his word doesn't end his stand-by | — | **built** (66 item 2) | open |
| 10 frigate cried at 8 leagues across land | — | — | — |
| 11 pilot leaves at six knots | open (`ports.py` pilot code unchanged) | open | open |
| 12 guineas never reach the purse | **built** (53b transactions) | = | = |
| 13 no order to hand over a thing | **built** (53b free lines, truth 114) | = | = |
| 14 every business ship "bound for Falmouth" | — | — | — |
| 15 acts budget of 10 | **raised** (acts ≥ samples in every starter) | = | = |
| 16 pace | — | — | — |
| 17 empty wake | — | **built** (66 item 3) | open |
| 18 orders dropped during a stand-by | — ("Nothing was run" remains) | **built** | open |
| 19 the deck's rule in the sample | — | the station's line (66 item 1) | open |
| 20 master's courses across the land | 61 not built | open | open |
| 21 the sample repeats the history | 58 not briefed | open | open |
| 22 pending reply | — | partly: "heard by" and "waits until" (66 item 4); the thread form is 52's | open |
| 23 director's words ahead of state | brief and forms (53b) | = | = |
| 24 consent brief says the director is "to come" | **open** (55 not built) | open | open |
| 25 needs never shown; no status line; omniscience ashore | — | the line, plus needs and heard now printed at the text doors (66); omniscience ashore is 65's (provisional) | open |
| 26 boat round trip, no waterman | — | open | open |
| 27 noon sight moves 2 cables; anchor reads "dragging"; empty 50 s stand-bys | — | — | — |
| 28 the fixed seat | 65 provisional | open | open |
| Chart checks (Santoña, Passages, Bas) | §26 open item | open | open |
| Éclair owner notes (lug rig, viewer) | routed to 57, merged 2026-10-17 per the waves table (not re-checked here) | | |

## What worked well

- **The director's hand did what was built, honestly.**
  - The frigate's physics and doctrine were fair. The captain's inshore road beat her on the merits.
  - Tregenna and Veale gave the run its life. Veale's lines reacted to what the cutter had actually done.
  - The doubt-not-refuse channel let Fable re-enter Veale with the right place words.
- **The owner and Opus made a real quarterdeck.** The owner caught the master's NNW line toward Penlee; Opus caught her taken aback in the narrows. Opus corrected the owner's "hard upwind beat" with a clear reason ("It's no beat … she'll lie it on a reach"). The deck and the grants (`you may shape a course for Plymouth`, `you may let the pilot take her in`) were used as designed.
- **The refusals guided the next try well:**
  - "kept back" pointed to the grant by name;
  - the pilot's refusal named the station;
  - "Not hands enough … the hands take the sails in turn" explained the delay;
  - "With thirty-eight fathoms out she will swing within a cable of the land" warned before it mattered, in both the Cawsand and the Roscoff runs.
- **The dispatches findings were turned into code within a day.** 53b and 66 answer most of them in G (but not H).
- **GLM-5.3-flash as director in Roscoff.** It read the truth before acting, respected the rule of reach ("I speak for neither held station"), and planned its hail to land with the boat: good craft for a small model.

## Model behaviour and experience

- **Opus 5.5 (captain).**
  - **Seamanship.** It was strong and well explained:
    - anchoring at once on seating;
    - taking the deck at the two moments of danger and giving it back promptly;
    - overriding the master's line across the land;
    - measuring the Penlee–Dragstone gap off the harbour chart;
    - diagnosing the drag as canvas, not scope, and accepting the owner's scope objection.
  - **Two errors of inference, both invited by the game.** At noon it took the frigate for a merchantman (E1-04). At 15:44 it read the empty wake as Veale's silence and wrote "he made no answer" in its journal. It corrected the entry afterwards, without fuss.
  - **Parallel calls.** It sometimes sent orders in parallel with a `stand_by`, which lost them ("Nothing was run", three times). It learned the pattern.
  - **Developer notes in the journal.** It used the in-game journal for notes "For the developer:" (11:20, 15:44, 15:45). That is honest, but it mixes the ship's record with bug reports. A separate channel for that may be worth offering.
  - **Its own account** (the debrief, quoted in G): the fun was "Passing the frigate. The tension came from not knowing". The worst moment was "concluding someone wasn't there". Asked for one thing to add, it chose a pending-reply signal.
- **GLM-5.3-flash.**
  - **In consent.** It was thoughtful and gracious. It called the false positive "a misfire of the scan against an honest answer", and asked for no weakening of the scan, only a warning line.
  - **As captain.** Its wish to shorten to 15 fathoms in 7½ fathoms (2:1 scope) would have been poor ground-tackle practice. The letting-go ran its course anyway.
- **Fable 5.1 (director)** kept a disciplined journal of findings "for the lead's list". Ten of the notes' findings come straight from it.

## Open questions for the owner

1. **The GLM seats on O.** Did you seat GLM on O on 2026-10-18 and 2026-10-19 knowing that its latest answer was "yes, with conditions"? Or did the game seat it without your noticing? (The station brief cited the "left with the token" record.) Do you want GLM's two conditions answered before it is seated again?
2. **The consent records.** Should the consent records written in local copies (O's five, H's four) be committed? At present the history, and any conditions, are lost whenever play moves to a fresh copy.
3. **Why the runs were stopped.** Why were the Roscoff "A passenger" run and the O Torbay attempt stopped after a few minutes: the consent question, the pace, or the move to B? If it was the director's latency (more than two minutes for its first sample), that is worth a pace note.
4. **The Torbay brig.** Is the Torbay brig meant to be the Batavian *Harpy* in an enemy road? The O director read her so (t42). The Torbay slice may want to confirm the scenario's nation.
5. **The status line.** 66's station line is in G only. Should it, with the stand-by fixes, be carried into the hotfix copy for the next session on H?
