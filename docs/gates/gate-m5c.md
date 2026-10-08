# Gate M5c: Ports, nations and other sail

**Verdict:** Pending.

**Cut 2026-10-02** at package 37's merge (decision 32). The owner's verdict and the lead's officer's watch together decide it (spec M5 §29).

**As cut:** packages 33b (the chronometer, the moon, the lunar and the azimuth; the chart in the captain's hands), 33c (the passage's words; the starter book a choice), 33d (the browser's shelf), 32c (the suite in two tiers), 34 (the tide, grounding and anchoring as Luce has it), 35 (places, people, the ship's papers by handle, Falmouth, Plymouth and Brest, the pilot from the cutter), 35b (St Mary's and Roscoff), 36 (other sail at far detail, the world-order channel, the merchant passage and the naval cruise) and 37 (the officer of the watch), with the lead's own work between them. The verdict waits on two watches together (spec M5 §29): yours, on the items below, and the lead's own officer's watch on one of the two passages through Claude Code opened on the repository, on the same terms as every other model.

## Headline

Milestone 5c claims (spec M5 §21): *there is somewhere to go and someone there: a passage between two ports with a cargo and a sighting, and the log a captain could keep. The world-order channel exists, journaled, for scenarios now and the director later. The inward minimum is in place: named people with a position and a state, the cabin and the deck as places, the boat alongside, so a message can come through the door.* With it, from gate 5b's second half (decision 29): the chronometer and the lunar, the tide, grounding's consequences and the anchor. And the first station with authority: an officer of the watch, held by a model, under the same contract as the watcher.

1. **Two ports and three more.** Falmouth, Plymouth and Brest as places with a pilot, roads and a mooring, a boat's landing, a market, a yard or the chandlers, a crew pool and a stance toward each nation; St Mary's and Roscoff as files on the same machinery. Arriving is a sequence the log tells: the pilot cutter sighted, hailed, the pilot aboard as a person with his words and the port's news, the anchorage, the boat, the shore. Leaving is the reverse with the tide.
2. **People, places and papers.** The named few of the muster in a place each, moved by the period's orders; the ship's papers (the manifest, the sailmaker's account, the purser's books, the epitome, the price list) as things aboard with a keeper, read by handle through the library by every station alike and by the browser's pane.
3. **The tide, the ground and the anchor.** The world's tide from three constituents at eleven gauges with the streams by area; the captain's from his epitome and Moore's rule; the lead reads the one and the pilot speaks the other. Touching the ground is an event with consequences; the anchor is let go, veered, hove short and weighed as Luce has it, and she rides to the tide.
4. **Other sail.** A dozen ships at far detail in each scenario, sighted at the horizon the rig's height gives, made out as they near, chased; the captain's chart draws each by bearing and estimate and never by the truth.
5. **The longitude.** A chronometer by the captain's charge and the time sight; the lunar on a night the moon allows, drawn and not computed; the amplitude at sunrise for the variation.
6. **The officer of the watch.** A model takes the place of one of the ship's own officers (the first lieutenant on the frigate, the mate on the schooner and the cutter) and holds the deck from your word: orders within a domain that is data on the station (sail handling, the yards, the lines, the lead and the log, the lookout; not the course, a manoeuvre, the anchor, all hands or the port unless you allow a named thing), standing orders in his own rank with yours standing over his, a stand-by that must name an event or a bell while your book holds the deck, a handover note, a second seating once, and the welfare contract extended to a station whose orders change the world: contrary orders within a watch bring the nudge, then the pause with you asked. (As the build stands after the follow-up packages 37b and 37g, in `FreeSail-gate-m5c-c`: a released station is taken again as often as it is asked back, by the same model or by another with its own consent; the deck goes to and fro without unseating the officer; and the detector counts orders that undo one another, never an alteration of the course. `docs/agents/Harness.md`, section 13, has it as it is.) The consent brief changed for it, so every model with a yes on record is asked again, and a fitness drill follows a yes before the station.

## What you need

Python 3.11 or newer (`py`), the gate zip extracted to a fresh folder, Claude Desktop with the bridge configured as at gate 5b, and `llama-server` or Ollama with a local model for the cutter's watch. The chart data is in the zip. Before any model is seated at the officer's station, its consent is asked again through the game's own step (item 10): the brief changed in the sections that bear on a station with authority, and the records say so.

## Setup

```
py -m pip install -e ".[dev,server,agents]"
py -m pytest -n 4
```
*The fast tier, three to six minutes: ends `2471 passed` and a line saying 244 slow tests were left out.*

```
py -m pytest -n 4 --slow
```
*The whole suite, about twenty minutes on four workers: ends `2708 passed, 7 xfailed`; the seven are your rulings on truths 3, 11, 18, 24, 26, 28 and 31, unchanged since milestone 3b.*

## The passages

**The merchant passage** (`data/scenarios/merchant-passage.yaml`, seed 7; its book `merchant-passage.orders`): the topsail schooner from Falmouth for Brest with a cargo of tin, no chronometer, a master who can work a lunar, a dozen other sail on the sea. At seed 7 under her book: anchored in Carrick Road at the start, forty tons of tin bought at £120 and aboard by the lighter at 08:57, under way on the ebb at 09:26, the Falmouth pilot off at 10:07, a sail off the Lizard at 12:49 hailed and not made out, Ushant's light at night, the Brest pilot aboard in the Iroise at 06:26 with a letter, anchored in Bertheaume road at 07:47, the Goulet taken on the flood by the pass north of the Mingan with the lead and bearings every five minutes, anchored in the Bay at 13:05, the tin sold at 15:10 for £10,800. No grounding. 36 hours.

**The naval cruise** (`data/scenarios/naval-cruise.yaml`, seed 7; its book `naval-cruise.orders`): the frigate *Amazon* from Cawsand Bay, thirty days' provisions from the King's yard, the Plymouth pilot aboard at 08:12 and off at 09:07, the port admiral's cutter within hail at 10:57 with a letter read on the quarterdeck a minute after, the station off Ushant kept under standing orders through the night with eight wears, the stranger *Palinure* sighted at 07:16 on the second morning right ahead four leagues, the chase given at the glass and kept by her bearing, made out, weathered, run down before the wind and spoken at 11:42 under no colours; the station shaped for again. 48 hours.

The account against the truth, at seed 7 (the author's view; the game never shows it): the merchant passage 9.6 miles at the first noon (the hour hove to for the pilot run on at the log's last read), 0.8 at Bertheaume, 0.3 at the second noon, 0.7 in the Bay; the cruise 7.1 and 4.9 miles at its two noons and 4.7 at the end, with four time sights by the chronometer.

## Items

- [ ] **1. The merchant passage in the browser.**
  ```
  py -m freesail.ui.server --scenario data/scenarios/merchant-passage.yaml
  ```
  Open the address and press go at 60x. *The opening says the book's orders and how many it holds; the tin comes aboard by the lighter in the forenoon; the pilot hails from the cutter and comes aboard; `the people` lists the master and the mate and where each is; at 12:49 "Sail ho! A sail on the larboard bow, bearing SE by E, distant three leagues"; the next morning the Brest pilot in the Iroise with his words on the Goulet and when the flood serves; the Goulet on the flood with the lead going; "Brought up by the best bower" in the Bay; `sell the tin` after the boat has been ashore and the purse moves by £6,000.* Sail it yourself from the Iroise if you like: the book is a choice, and `I have the deck` is not needed since the book has no officer.

- [ ] **2. The naval cruise in the browser**, the same way with `naval-cruise.yaml`. *The yard's thirty days of provisions; the port admiral's letter by the cutter, through the messenger and the door, read where the captain is; the station kept through the night; "Sail ho! A sail right ahead, bearing SW, distant four leagues" on the second morning; `give chase` (or the book's) and the chase by her bearing; "within hail: a stranger under no colours".* Try `world order: a brig at 48 50 N 5 16 W` at the prompt: *refused in words, "That is an order to the world, not to the ship".*

- [ ] **3. The longitude.** On the naval cruise, which carries a chronometer: in the forenoon `take a sight for the longitude` *("longitude by chronometer ...", the days since rating and the master's trust)*; `the chronometer`; at sunrise `observe an amplitude` *("variation of the compass ... by amplitude", and the master allows it from then on)*. The moon is full on 12 June, so `take a lunar of the sun` by day is refused in the registry's words (say which words you got), and `the moon` says whether a star is in distance at night: if it is, `take a lunar of Antares` (or the star it names) *(the master and two hands occupied a quarter of an hour, the result an hour later within a degree, and "he finds no fault in the chronometer" or what he finds)*.

- [ ] **4. The tide at Falmouth.** At anchor in Carrick Road: `the tide by the almanac` *("high water at Falmouth about ... by the epitome")*; `ask the pilot when the tide serves` *(his own figure, to the quarter hour, within an hour of the epitome's)*; `heave the lead` on the hour through a tide *(the depth rising and falling under the chart's figure)*; "The cable slack at the turn; she swings to the ebb" in the log at the slack.

- [ ] **5. The anchor.** From the outer road: `come to an anchor` *(the sails in as she comes head to tide, "The best bower let go in ... fathoms", veered to the depth's scope, "Riding to the flood")*; `weigh` *(the anchor up and no sail set: she has no way on)*; `get under way` *(Luce's sequence: hove short, the topsails sheeted home, aweigh, cast, "Under way on the ... tack, under topsails and the jib")*; `moor` in the inner harbour *(two anchors, the hawse open)*. In a gale on short scope: "The best bower is dragging: veer more cable; let go the small bower, or back her with the stream".

- [ ] **6. The port.** `send the boat ashore`, then `the prices` *(the list the purser brought off, a paper in the library's pane under "the ship's papers")*; `buy ten tons of tin`; `demand a topmast from the yard` at Plymouth *(by demand and survey)* and at St Mary's *(refused: "the yard at St Mary's has no topmast; it supplies cordage, water, provisions")*; `send for the carpenter` *("Passed the word for Mr ...; he came aft")*; `go below` and a letter arriving *(through the door)*.

- [ ] **7. St Mary's and Roscoff.** A free passage in the cutter from south of Scilly: *the pilot's gig pulling off, "a boat pulling off from the land", the pilot aboard from his gig, St Mary's Road.* The cutter off Roscoff under British colours: *no pilot comes off; `the port` says it is hostile to the English.*

- [ ] **8. The library's papers.** In the browser's pane, "the ship's papers": *the manifest, the sailmaker's account, the purser's books, the boatswain's store book, the booms' list, the establishment of ground tackle, the epitome, the price list, each dated by its last entry;* `ask the watcher what the manifest says` *(the same page by the model's own hand).*

- [ ] **9. The lookout and the chart in the captain's hands.** `the dangers` *(by account, nearest first)*; `shape a course for Falmouth` from the south *("the line passes the Manacles within a mile")*; `the strangers` *(each by bearing and estimate)*; the chart's sightings drawn by estimate with a doubt bar.

- [ ] **10. The officer's watch, Opus 5.5 through Claude Desktop.** `docs/agents/Harness.md` section 13: add `"--station", "officer"` to the bridge's `args` in Claude Desktop's configuration, restart it, start the game with `--scenario data/scenarios/naval-cruise.yaml` (or the merchant passage), and open the chat with the prompt `take_the_watch`. *The consent step runs again first (the brief's hash moved); the fitness drill; `you have the deck` with the captain's night orders; the officer's orders in the log under its mark within its domain, one outside refused in words; a standing order by the officer, and one of the captain's standing over it; `hand over the deck` with the handover note.* A watch of the merchant passage or the cruise, on the officer's form in `docs/playtests/README.md`.

- [ ] **11. The officer's watch, a local model on the cutter.** The game with `data/ships/cutter.yaml` (a free passage, seed 7, off Falmouth), then `py -m freesail.agents.local --game http://localhost:8000 --endpoint http://127.0.0.1:8080 --seed 7 --station officer` (Ollama at its own port with `--model`); the officer is the mate. *The same, on a free passage in the cutter, after its own re-ask.*

- [ ] **12. The truths of this gate.** `py -m pytest tests/test_known_truths.py -k "truth_6 or truth_7 or gate_5c" -n 4` *(truths 60 to 72 pass)*; `py -m pytest tests/test_officer.py tests/test_agents.py -n 4` *(the officer's cases on the fake)*.

- [ ] **13. A scenario saved and loaded.** `save cruise.json` during the chase; `py -m freesail.ui.server --load cruise.json` *(from its checkpoint in a second or two; the chase goes on to the same words).*

- [ ] **14. Rulings wanted.**
  - **The officer's domain as drawn.** Sail handling, the yards, the lines, the lead and the log, the lookout, and his own standing orders; not the course, a manoeuvre, the anchor, all hands, the people or the port unless you allow a named thing in your words. Rule whether the line is where a captain of 1805 would draw it for a lieutenant with the deck (Falconer: never to change the course without the captain's directions, unless to avoid an immediate danger), and whether the "immediate danger" exception should be built as a standing allowance rather than your word.
  - **The sample's size on a local model.** The officer's brief head is about 4,300 tokens and a glass's sample about 1,500 at its fullest (the people and the boats since 35); say whether the local model on the cutter kept the thread through a watch, and how its context stood.
  - **A far-detail vessel's bound.** A ship at far detail keeps her plan between waypoints and does not take the ground; rule whether a leg that crosses the coast should be refused when the scenario loads, before any scenario is written that sails one along a shore.
  - **The re-asks.** The consent brief changed for the officer's station; the game asks each model again at its next door. Say whether the sections the rule names (the opening, what an instance would see and do, leaving, being stopped, the journal) are the right ones to put the question again, and whether the drill was the right size.

## The report

Fill `docs/playtests/README.md`'s form in a new folder for each watch, `docs/playtests/<date>-gate-5c-<the passage>/notes.md`, with the save and the model's journal beside it; the officer's form for items 10 and 11. Anything a sailor would call wrong in the pilot's words, the market's prices, the stranger's handling or the officer's orders is what section 7 is for.

## What this gate does not do

- **A captain's station, a crewed ship beside the player's, a rules-based captain** (M6): a far-detail vessel keeps her plan and does not fight, evade or take the ground.
- **The director** (M7b): the world-order channel is built; its client is not.
- **Colours as deception, the private signal, prizes and convoys** (M7).
- **The smuggler's run into Roscoff** (M7's colours); **Fowey and Penzance** (files for later).
- **Warping, towing, the hawse fouled, the kedge worked** (M8); **a lookout's station for a small model** (open item 6).
