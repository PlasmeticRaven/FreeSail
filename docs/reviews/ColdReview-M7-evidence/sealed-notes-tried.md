# The lead's sealed notes, tried at the commit under review

The tree at 504a250 (the trunk; HEAD adds only review files). Each item of the lead's running list and each of his head-4 examples tried from the code, the data, short runs in python and the console, and one test by its node id. No suite was run. "Reviewer" = whether `ColdReview-M7.md`, heads 1 to 5 as first written, had found it.

| # | The lead's item (short) | Verdict | Weight | Reviewer |
|---|---|---|---|---|
| G1 | "take the purse" a reading; refusals leak where a thing is or that it is gone | CONFIRMED | medium (player) | no |
| G2 | A rules captain waits for his tide (`leave_on`) without a word | CONFIRMED | medium-high (player) | no |
| G3a | The merchant passage's schooner takes the ground 13 times as recorded | REFUTED as the tree records it | — | no |
| G3b | The cutter left to cruise from Falmouth grounds on mud nine minutes after weighing | NOT TRIABLE HERE (fixture on package 60's branch) | medium | no |
| G4 | Vessels cross the land at far detail | CONFIRMED IN PART | medium | in part (the player's own ship) |
| G5 | A far ship woken at anchor sails off | NOT TRIABLE HERE (in flight, 60) | medium | no |
| G6 | A boat lost while carrying a person leaves him in no hull and not dead | CONFIRMED (on the trunk) | medium | no |
| G7 | A loaded game lost the chart it began with | CONFIRMED as history; mended before the commit | none now | no |
| G8 | Coarse layers at mean sea level; the level above low water added again | CONFIRMED IN PART (mechanism; the count not re-measured) | medium | no |
| G9 | The ocean outside the blocks reads the Channel's eleven gauges alone | CONFIRMED | low-medium | no |
| G10 | Decision 68's statement has no served field; it stands in comments | CONFIRMED IN PART | low (owner) | no |
| G11 | A book of orders cannot say a clock hour, only bells | CONFIRMED | low | no |
| G12 | Spain's "two flags at the main"; a yardarm hoist past the view's frame | CONFIRMED IN PART | low | no |
| D1 | Port tracks follow the land, not sounded channels | CONFIRMED | medium | no |
| D2 | Genoa, Cartagena, Oran, St Malo cannot be entered | CONFIRMED, and understated: 24 ports | medium | no |
| D3 | The nations' days: French from memory, British and Spanish mostly | CONFIRMED (Spain: all) | low (owner) | no |
| D4 | Canaries port datums unverified; Sicily's gauge levels judged | CONFIRMED; the open-ocean proposal NOT TRIABLE HERE | low-medium | no |
| T1 | The pace floors sit inside the machine's noise | NOT TRIABLE HERE | medium (owner) | yes, second sitting only |
| T2 | `_until` defined twice in the truths' file | CONFIRMED | low | no |
| T3 | Truths that only import and call tests of another file | CONFIRMED | medium (cost) | **yes** (3.x: 102) |
| T4 | Truth 7b-130 failed once under load | NOT TRIABLE HERE | low | no |
| T5 | No cloud run before run 81 played the browser plans | NOT TRIABLE HERE | medium | no |
| T6 | Independent readings found ~20 faults the green suites did not | NOT TRIABLE HERE | high (process) | no |
| P1-P6 | The process (stalls, containers, merges, suite cost, the ships session, run time) | NOT TRIABLE HERE | — | no |
| E1 | Head 4: the ways a ship is set up | CONFIRMED | medium | no |
| E2 | Head 4: the ways a thing is dated | CONFIRMED, with a latent fault found | medium | no |
| E3 | Head 4: hands called, work waits, a line said | CONFIRMED IN PART | low-medium | in part (3.5) |
| E4 | Head 4: the orders, the forms and the readings | CONFIRMED | medium | **yes** (F4.2, F4.3) |
| E5 | Head 4: regions of the chart, the tide and the weather | CONFIRMED IN PART | low-medium | no |
| E6 | The browser plan missed at package 109's step 1 | NOT TRIABLE HERE | medium | no |

---

## What the game does

### G1. "take the purse" is read as a reading. Refusals leak where a thing is, or that it is gone.
**What I did.** Console, `merchant-intent.yaml`: `take the purse` gave `The purse: £6000.` and `take the purse ashore` was refused with "'take the purse' is a question and takes nothing after it". For the leak I put a thing the captain was never told of, "a bag of guineas, ashore at Plymouth, at the counting house", into the world's things in `dispatches-falmouth.yaml` and gave `take the guineas` aboard at Falmouth. The answer: "nothing of the ship's changed (the bag of guineas is ashore at Plymouth, at the counting house)". And `throw the packet overboard` then `take the packet`: "there is no packet that you know of. The sealed packet went over the side."
**The code.** `things.find` (`world/things.py:356`) searches every thing in the world with no test of what the person knows; `things.reach_why` (`:582-597`) answers with `where_words` for any thing out of reach; `orders/free.py:724` `_gone_words` names a thing destroyed or overboard whether or not he saw it go. The refusal's own words ("that you know of") claim the knowledge test the code does not make.
**Verdict.** CONFIRMED. **Weight.** Medium for a player: the refusal is an oracle for where any named thing in the world is. Also seen: a refused take is still logged "By the captain ...: took the packet, as said; nothing of the ship's changed", an acceptance in form.

### G2. A rules captain waits for his tide (a port's `leave_on`) without a word.
**How he decides the tide serves.** `world/captains.py:3980-3987`:
```python
def _tide_serves(self, port, p, which):
    wanted = str((getattr(port, "tide", None) or {}).get(f"{which}_on") or "")
    ...
    serves = p.tide_is(wanted)
    ...
    return bool(serves) and p.daylight == "day"
```
The key is built as `f"{which}_on"`, so a grep for `leave_on` finds nothing; `which` is `"leave"` from `_ready_for_sea` (`:4002`) and `"enter"` from `_leg_reached` (`:3830`). The port's file reaches it through `Port.tide` (`world/ports.py:753`, `tide=dict(doc.get("tide") or {})`). The first reader's report that the key is read by nothing is wrong. "The tide serves" means: the master's almanac (`Perception.tide_is`, `:1792-1807`) puts it within about six hours after high water (the ebb) or six before it (the flood), and **it is day**. With no almanac, or no `leave_on`, he does not wait. All 121 port files give `leave_on` (`grep -L` finds none without it).
**Whether he speaks.** I ran `merchant-intent.yaml` from 08:00 instead of 05:00 (python, `dataclasses.replace` on the start). The tin was hoisted in at 12:21:57. He weighed at 17:59:47, the line reading "getting under way ... (the tide serves)". In the 5 h 38 min between there were 70 lines in the log: bells, gusts, the weather, a sail sighted, the watch relieved. Not one says why she lies there. The captain's reading through the wait: "Mr Travers, merchant; the intent: trade tin from Falmouth to Brest; in port; nobody at the captain's station; ...". `_in_port` (`:4004-4022`) returns in silence when `_ready_for_sea` is false. Arriving, by contrast, he says so: `give("come to an anchor", why=f"the tide does not serve to enter {port.name}")` (`:3831`). Going out he gives no such word, and the daylight condition holds her through a night the same way.
**Verdict.** CONFIRMED. **Weight.** Medium to high for a player who leaves a ship with orders: hours of nothing, with no reading that names the tide. The mend is one line in `_in_port` and a phrase in the captain's reading.

### G3a. The schooner of the recorded merchant passage takes the ground thirteen times as recorded.
**What I did.** Two truths pin the schooner's recorded passages and assert no grounding over the whole log: gate 5c's merchant passage under its book (`tests/test_known_truths.py:4443`, `assert not [e for e in log if e.kind in ("ship.aground", "anchor.dragging")]`) and the same passage on an intent alone (`:4804`, `assert not [e for e in log if e.kind == "ship.aground"]`). Neither is marked xfail. The only grounding event is `ship.aground` (`world/ground.py:236`). The measure the lead cites is in a ruling to a builder (`docs/dev/M7-WorkPackages.md:10510`) and in no file of the tree. I did not re-run the 36 game hours.
**Verdict.** REFUTED as the tree records it, unless the builder's measure counted something other than the logged grounding (a probe's own count, another seed or crew). The lead should name the measure.

### G3b. A cutter left to cruise from Falmouth weighed on the ebb and took the ground on mud at five knots nine minutes later.
The Sherbourne/Mr Pearce fixture is package 60's (`M7-WorkPackages.md:5166`) and not on the trunk. NOT TRIABLE HERE. **What bears on it:** in my 08:00 run the schooner weighed at 17:59, with "the Black Rock close ahead ... three cables!" in the morning run, but grounded neither time. The pilotage out of a berth has no truth of its own; G2 and G3b share the road (`_sail`, `:4062`).

### G4. Vessels cross the land.
**What I did.** `merchant-intent.yaml` at the start prints the far-detail guard for 5 of its 12 other sail ("her plan crosses the land on the leg to Brest at far detail, where no ship takes the ground"). The guard warns and does nothing for a ship with no brain (`world/ships.py:1671-1678`: "six of them sail across a cape at far detail"). It refuses only a ship with an intent (`:1660-1664`). A sample of the 13 hulls' chart depth every hour for 8 hours found two starting on drying cells (Palinure at the Raz, −0.1 m; Hirondelle, −0.03 m), the scenario's positions, and none on land at the hour after that. The "8 of 35 and 6 of 24" busy-day measure is not reproduced (it needs the world's business for a day). The sea-road guard's cost is package 61's, in flight.
**Verdict.** CONFIRMED IN PART: the guard knowingly lets brainless plans cross the land, and the scenarios start ships on drying ground. The busy-day count is untried. **Weight.** Medium: a player who watches the map sees it. The reviewer found the player's own ship sailing a course the game had warned crossed the land (5.3); the far ships he did not.

### G5. A far ship under a rules captain at anchor, woken, was not at anchor and sailed off.
NOT TRIABLE HERE: package 60 is in flight. **On the trunk:** `rides_as_she_lay` (the mend's function) is not in `freesail/`, so the fault the lead describes stands at this commit.

### G6. A boat lost while carrying a person leaves him in no hull and not dead.
**What I did.** `merchant-cutter.yaml`: `send the boat ashore with the mate`, then the director's `boat lost` effect (`world/orders.py:3672`, `_fx_boat_lost`). Before: `('Mr Pearce', hull None, dead False)`, and the boat's people `['mate']`. The log said "The boat stove against the side. A new one is the yard's." Nobody was named as lost. After: `('Mr Pearce', where 'boat', hull None, dead False, aboard False)`.
**The code.** `boats.lose_boat` (`world/boats.py:893-941`) kills only those `registry.aboard(hull.id)` of a manned boat's hull. The errand boat's passengers (`dealings.py:2997-3000`, `person.aboard = False; person.where = "boat"`, hull None) are never touched, and the new `BoatState` drops the people list.
**Verdict.** CONFIRMED on the trunk. **Weight.** Medium: a person stranded nowhere, with no word, and a save that carries him. The reviewer's "a purchase with the boat lost takes the money and delivers nothing" (head 1) is a sibling: the same function forgets the errand.

### G7. A saved and loaded game lost the chart it began with.
The mend was merged 2026-11-14 00:47 (9ab10a4, from 0d093ae: "a checkpoint loads a region's game on the chart that holds it"), before 504a250. I ran `tests/test_checkpoint.py::test_a_region_game_loaded_from_its_checkpoint_has_the_chart_it_began_with` and it passed. "Found by chance, not by any test" is true by the history: the two tests came with the mend. **Verdict.** CONFIRMED as history, mended at the commit. **Weight.** None now. The lesson for the suite is that no test loaded a region game's checkpoint until the fault was met.

### G8. The coarse chart layers stand at mean sea level and the game adds the level above low water again.
**What I found.** `data/charts/manifest.yaml:14,20` give levels 0 and 1 `datum: mean sea level`, and levels 2 and 3 lowest astronomical tide. Nothing in `freesail/` reads a level's `datum` (no `"datum"` key is read anywhere). `chart.depth_at` is the bed's height at whatever level is finest (`chart.py:1182`). The tide's height is the gauge's mean level plus the harmonics (`tide.py:657`, `height_m=level + z.real`), added to it for grounding (`ground.py:156-161`). So where only a coarse level covers the water, the mean level is counted twice. The figure of 765 shore cells is not re-measured.
**Verdict.** CONFIRMED IN PART (the mechanism, by code). **Weight.** Medium where coarse cells meet the shore: false water, and false landings.

### G9. The ocean outside the chart's blocks reads the Channel's eleven gauges alone.
`load_tide()` gives 11 gauges without a block (St Mary's, Newlyn, Devonport, Weymouth, Dover, Brest, Le Conquet, Roscoff, Saint-Malo, St Helier, Cherbourg) and 89 block gauges in 22 blocks. The module's docstring (`tide.py:43-52`) says it: "outside every block the eleven alone". A height at 40° N 20° W at noon on 12 June 1805 came out at 2.52 m, and 2.24 m at 45° N 12° W. **Verdict.** CONFIRMED. **Weight.** Low to medium: a mid-ocean tide nobody sounds, but the reckoning's tide and the grounding read it.

### G10. A port file has no served field for decision 68's statement; it stands in comments.
The 8 port files that cite decision 68: in Tenerife, Gomera and Favignana it is in comments only. In Valletta, Pantelleria, Girgenti, Palermo and Lipari it is folded into the pilot's `marks` words, which are served (for example Valletta's "the Order's galleys are rowed by enslaved men"). No field of its own exists (`Port`, `world/ports.py`). **Verdict.** CONFIRMED IN PART: no field, but in five of eight ports it is served by way of the pilot's words. **Weight.** Low for play; the owner's for decision 68.

### G11. A book of orders cannot say a clock hour, only bells.
Console: `standing order "b": when the time is 16:00 ...` was refused with "the time is compared in bells: 'is eight bells'", and `four o'clock` was refused the same way. `at four o'clock` names no event. `when the time is eight bells and the watch is the afternoon watch` was entered. The grammar's own summary agrees (`standing/grammar.py:13, 411`). **Verdict.** CONFIRMED. **Weight.** Low: bells and the watch name every half hour. A player who does not know the bells cannot say "at four".

### G12. Spain's "two flags at the main"; a yardarm hoist past the view's frame on three hulls.
`Signal.flags_words` (`world/signals.py:708-710`) returns `two flags ... at the main` for every numbered signal of a table book. I built a Spanish signal of one flag (No. 409, "Man overboard", one of Mazarredo's signals of one flag, `data/signals/spain/numerary.yaml:99`) and it read "two flags at the main". The yardarm hoist past the frame (0.12 m on the hermaphrodite brig, 0.25 m on the schooners) is the builder's record (`M7-WorkPackages.md:4803`). It needs the browser's projection and was not reproduced. **Verdict.** CONFIRMED IN PART. **Weight.** Low.

## The data

### D1. Port tracks are the way the land allows, not sounded channels.
I sampled every leg of every port's `tracks` (116 files loaded; marks resolved by `captains._mark`) every 20 m on the chart, leaving out each leg's first and last cable as the guard does. Of 260 legs, **24 touch ground dry at the chart's datum** (Alghero, Civita Vecchia, Gaeta, Hyères, Morlaix, Poole ...) and **15 more have under 3 m** (Calais 1.7 m, Dunkirk 2.5 m, La Goletta 2.0 m, Porto Palo 1.4 m ...). The chart audit (`tools/audit_chart.py`) tries tracks only against dry ground (`land_crossing`), not against a trader's draught. A caveat: the datum differs by level (G8) and grid cells are not soundings. **Verdict.** CONFIRMED. **Weight.** Medium: the rules captains and the business sail these tracks.

### D2. Genoa, Cartagena, Oran and St Malo cannot be entered on the chart as it is.
All four are in `data/charts/audit-known.yaml` ("the business draws no ship in"). But **24 ports** have an `f-in:` exception: Alghero, Cartagena, Civita Vecchia, Dartmouth, Ferrol, Gaeta, Genoa, Hyères, Lisbon, Morlaix, Oporto, Oran, Paimboeuf, Palma, Poole, Port Mahon, Rochefort, Santander, Setúbal, St Malo, St Mary's, St Peter Port, Toulon and Villefranche. Twelve fail on a track across the grid's land and twelve have no tracks. **Verdict.** CONFIRMED, and the lead's four are a sixth of it. **Weight.** Medium: Lisbon, Ferrol, Toulon and Rochefort are principal ports of the period.

### D3. The nations' days: the French all from memory, the British and Spanish dates mostly.
`data/signals/*/days.yaml` sources: France 5 of 5 FROM MEMORY; Britain 6 of 7 (only the King's birthday sourced); Spain **7 of 7** (the articles sourced, every date from memory). **Verdict.** CONFIRMED (Spain all, not mostly). **Weight.** Low; the owner's shelf.

### D4. Every port datum of the Canaries is unverified; gauge levels judged from constituents in Sicily and proposed for the open ocean.
All five Canary port files have `datum: unverified`. Sicily's gauges have `mean_level_m` "JUDGEMENT: M2 + S2 + N2 ... no published level read" (`data/tides/constituents.yaml:1167-1221`). The Canaries' own gauges have published levels (REDMAR, `:1263-1323`). The open-ocean proposal is not in the tree: NOT TRIABLE HERE. **Verdict.** CONFIRMED. **Weight.** Low to medium. Sicily's judged levels are some tens of centimetres in a sea of small tides.

## The tests

- **T1 Pace floors.** NOT TRIABLE HERE: a timed run is using the machine. **In the tree:** one absolute floor, `BUILD_MACHINE_FLOOR = 1000 * 0.5` ticks a second (`test_known_truths.py:2157-2163`), half of one measurement on one build machine, is asserted by truth 51, truth 7-159 (`:9269`) and the gate day's (`:2750`). The margin assumes the four-worker load and nothing more. The reviewer's 3.x names wall-clock assertions elsewhere (`test_chart.py:300...`), not these.
- **T2 `_until` twice.** CONFIRMED: `test_known_truths.py:6170` (`minutes=300`) and `:7124` (`most=240`). Python binds the name at call time, so the five calls at `:6195-6268`, written against the first, run under the second: a 240-minute cap, not 300. Nothing fails today. Weight low.
- **T3 Truths that only call tests.** CONFIRMED: by a strict count (body nothing but an import and a call), **76** truths. The reviewer's 3.x counted 102 by his own measure (found).
- **T4 Truth 7b-130 under load.** NOT TRIABLE HERE. It starts the API door as a live server subprocess (`:7641-7660`), the kind of test that races a loaded machine.
- **T5 Browser plans before run 81.** NOT TRIABLE HERE. **In the tree:** every browser test is guarded with `pytest.importorskip("playwright.sync_api")` (`test_pictures.py:38`, `test_browser_probe.py:18`, `test_harbour.py:479`, `test_known_truths.py:15087`), so a container without it is green with them skipped. Nothing fails on a skip. On this machine Playwright imports.
- **T6 Package 60's readings; 111's tracks.** NOT TRIABLE HERE (branches in flight). D1 bears on 111: the trunk's tracks are tried against no depth.

## The process (P1 to P6)

NOT TRIABLE HERE, all six: builders stalling, late messages, the containers' missing packages and the setup script of 2026-11-13, the merge-after-every-landing instruction, the suites' hours, the ships session's file road, one ninety-minute run. **In the tree:** T5's silent skips are the mechanism by which a container lacking Playwright or the websocket library goes green. The suite cost bears on the reviewer's 3.8.

---

## Head 4: matters handled in two or more places that do not know of each other

### E1. The ways a ship is set up. CONFIRMED.
Every road ends in `ships.vessel_from_spec` (`world/ships.py:~1500-1680`), but each builds its spec and checks it in its own way:

| Road | Where | Its own checks |
|---|---|---|
| A scenario's `ships:` | checked `world/scenarios.py:648-690`; made `core/world.py:1054` | description, role, position and goal, intent xor free_intent. **No land check**: in `merchant-intent.yaml` two ships start on drying cells. Brainless plans across the land only warned. |
| A world order's `ship:` | `world/orders.py:1270` `new_ship_spec` (its own regex `_SHIP_NEW`, `:601`); made `:826` | a place on the land refused with the nearest water named (`_on_the_land`, `:1352`); the guard's warning returned in the order's words. |
| The letter cutter (`message ... by`) | `world/orders.py:1550-1566`, a spec written inline | none of its own. |
| The business drawing a ship | `world/business.py:1180-1215` | its own sailing-factor stream; a `ValueError` from the guard is swallowed ("not drawn"), where the order raises it in words. |
| The harbour's scenario maker | `client/harbour.js:434` `SHIP_COLS` (id, description, name, nation, position, goal, colours) → `scenario_text` → the loader | the form offers no `intent`, `free_intent`, `departing`, `fit` or `role`, which the loader takes; proved by loading (`ui/harbour.py:1009`). |
| The director | through the world order's form, plus its own reading of `_SHIP_NEW` for the brief's heaviest enemy (`agents/director.py:410`) and a second private reading in the doubt (`world/orders.py:4170`) | three readers of one regex. |
| Also: the prize (`world/captive.py:905`), the pilot's cutter (`world/dealings.py:348`, `Vessel(...)` direct), the player's own vessel (`world/ships.py:1912`, direct) | | |

**How they differ today:** a ship on the land is refused by the order, accepted by the scenario, silently dropped by the business. A brainless plan across the land is warned by scenario and order, never drawn by the business. **What joining takes:** move `_on_the_land` and the guard's refusal into `vessel_from_spec` (or a `check_spec` beside it) that all six roads call, and make the harbour's columns the loader's keys. About a day.

### E2. The ways a thing is dated. CONFIRMED, with a latent fault.
There are at least eight readers and no common one:

| Data | Reader | Convention |
|---|---|---|
| Port dated rows (`since`/`until`) | `world/ports.py:869` `_dated_rows`, `:910` `_row_on` | ISO days, both ends inclusive, an open end is no bound; a source required; overlap refused. |
| A port's dated nation | `world/ports.py:943` `_nations`, `:960` `_dated_nation` | inclusive; **no source, no overlap check**; parsed separately from the rows above. |
| A port's events | `world/ports.py:930` `_event_between` | the day after `until` counts. |
| Blockades (`nations.yaml`) | `world/business.py:209` `_between` | inclusive; parses the ISO string at every call. |
| Prize shares (`business.yaml`, `from`/`until`) | `world/prize_court.py:95-111` `scheme_for` | **`until` exclusive** (`when >= until` skips); a value that is not a `date` is treated as an open end. |
| Wars (`nations.yaml`, `since`) | `world/nations.py:109` `at_war` | **ignores the date**: a war in the table is in force on any day. |
| Wars again | `world/prize_court.py:302` `_at_war_at` | `since` None is war; a `date` compared; **a string is not war**. |
| Signal days and books (`years: "1799-1803"`) | `world/flags.py:642` `_in_dates` | year strings, inclusive, "" always. |
| Scenario wars | `world/scenarios.py:416` `_day` | checked against `as_of`. |

`data/regimes.yaml` has no dated rows (its "until" is prose), so the lead's "regimes" is not borne out. **The latent fault, reproduced:** `Nations.declare_war(a, b, when="1805-06-01")` stores `since` as a string (`nations.py:186`), and `Nations.to_dict` writes every `since` as a string (`:261`). After it, `at_war` says True and the prize court's `_at_war_at` says False. `declare_war` has no caller today, so no player meets it yet; the first war declared by news would condemn no prize. **An open end and a missing year:** treated alike as unbounded by the port rows, blockades, prize shares and days. A missing `since` makes a war always so. The prize shares' `until` is exclusive where every other reader's is inclusive: their rows at `business.yaml:166,175` (`until: 1808-01-01`, `from: 1808-01-01`) would be refused as overlapping by the ports' reader. **What joining takes:** one `dated.py` with a `Span` (since, until, inclusive, from ISO or date, source), used by all nine. About a day, and the prize shares' rows moved to inclusive ends.

### E3. The ways hands are called, work waits and a line is said. CONFIRMED IN PART.
**Called:** all hands are one road. `crew/routine.py:226` `call_all_hands` serves the player's order (`orders/crew.py:107`) and the evolutions' runner (`evolutions/runner.py:1344`): the lead's guess fails there. But a sailor's place of work (`Sailor.at`) is set outside `crew/hands.py` in seven modules: `world/prizes.py` (8 places), `crew/quarters.py` (4), `crew/health.py` (4), `world/needs.py` (2), `world/water.py:835` (the pumps), `combat/hits.py`, `agents/harness.py` (3). The guns' "Not hands enough for every gun" (`crew/quarters.py:473`) and the runner's "Not hands enough on deck" (`runner.py:1306`) are separate sums. **Waits:** the runner's `evolution.waiting` (`runner.py:1176`), the storm orders' own `_waiting_for_hands` (`orders/storm.py:321`), the captain's `work_in_hand` reading (`captains.py:1622,1664`), and G2's silent tide wait, which is in none of them. **A line said:** some ten writers with their own severity and kind rules: `World.record` (`core/world.py:1262`), `Hull.record` (`world/hulls.py:399`), `Ship.note` (`ship/graph.py:318`) drained by `runner._record` (`:1620`), `routine._note` (`crew/routine.py:79`), `Script.note` (`evolutions/scripts.py:1034`), `dealings._record` (`:317`), `signalling._say`/`_record` (`:358, :760`), `prize_court._say` (`:606`), `stations._record` (`world/stations.py:332`). **What joining takes:** a single `assign(crew, sailor, work)` in `crew/hands.py` that the seven call; a single "waiting for X" record kind that the captain's silent waits also write. A few days. The writers of lines are the smaller hazard. The reviewer's 3.5 ("tasks compete for hands" between evolutions only) found part.

### E4. The orders, the forms and the readings. CONFIRMED; found by the reviewer (F4.2, F4.3).
G1 adds a player's instance: `take the purse` is answered by the readings' ladder before the take's reader sees it.

### E5. Regions of the chart, of the tide and of the weather. CONFIRMED IN PART.
- **The chart:** 20 regions with bounds in `data/charts/manifest.yaml:63`, read by `chart.load_manifest`.
- **The tide's blocks:** the same file's regions plus 4 `tide_regions` (Solent, gulf of Hammamet, Calabria north, Asinara west; `:14068`). The tide reads the manifest with **its own loader** (`tide.py:133, 807-831`, "read once a process"). The bounds are one set, but there are two readers.
- **The tide's streams:** 82 polygons in `data/tides/streams.yaml:126`, each tagged with a chart name. One names `atlantic-east`, which is no region of the manifest.
- **The weather:** 13 boxes with their own bounds (`data/weather/climatology.yaml`). Five copy a chart region's bounds literally (tyrrhenian, catalan-coast, sardinian-sea, tunis-coast, sicily); six of the same name differ (portugal, madeira, azores, mediterranean-west, gulf-of-lion, canaries; some by design, being ocean boxes); two (channel, biscay) have no chart region of the name; nine chart regions have no box.
- **The chart audit** keeps its own copy of the tide's blend (the reviewer's F4.11).

So there are three sets of bounds (the manifest's, the streams' polygons, the weather's boxes) read by four loaders. The copied bounds will drift when a region is moved. **What joining takes:** the weather boxes and stream polygons naming a manifest region where they mean one (`bounds: {region: sicily}`), one manifest reader shared by the chart, the tide and the audit, and a test that every name a data file gives is a region. Half a day to a day.

### E6. The browser plan missed at package 109's step 1.
NOT TRIABLE HERE (process). T5's silent skips are what bears on it in the tree.
