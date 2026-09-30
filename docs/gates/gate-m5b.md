# Gate M5b: The chart and the reckoning

**Verdict:** Pending.

**As cut (2026-09-30):** packages 31b (all hands manned in parallel with a party bound on any one job; the heavy-weather routine's order of work; parted running rigging rove afresh or spliced; the pinned form under the air-mass rule), 31c (the watcher's watch: a sample carries only what changed, the Desktop door's wait under the client's cut, the weather's events to stand by for, `tell` and `ask` a station in a standing order, the unattended wait in ten real minutes only), 32 (the geographic frame, the chart data of the western Channel, the queries and the lookout), 32b (the cutter *Sherbourne* and the brig *Harpy* as ship files, the running bowsprit, the orders' grammar across four ships, the hierarchy truths 73 to 76), 32e (staying and sheets: yaw that scales with the vessel, Luce's recovery when she hangs in stays, the headsail sheets held to windward, the sheet holding the trim) and 33a (the reckoning, the noon sight, the captain's chart, the checkpoint save, the passages of this gate), with the lead's own work between them (`docs/dev/M5-CloseOut-5b.md`). By decision 29 this gate is the passage by the reckoning and the noon sight alone: the chronometer, the lunar, the tide, grounding's consequences and anchoring are gate 5c's set. Two items are carried from gate 5a and count for both: `--load` of a saved day with a station (item 7) and the two days from the climatology (item 8). The report for this gate is your playtest, on the form in `docs/playtests/README.md`; four rulings are asked of you (item 11).

## Headline

Milestone 5b claims (spec M5 §8): *a passage is a game: the ship crosses a real sea by the period's means, the captain's account of where she is diverges from where she is, and the lead, the land and the sun each collapse the doubt by their own measure. A landfall is made by the reckoning, and one is made wrong.*

1. **A real sea.** The western Channel and the Western Approaches, Falmouth to Ushant, from open bathymetry (EMODnet 2024 with GEBCO 2025 under it) at three arc-seconds with four harbour patches at half a second, the shore of 1805 patched in at Falmouth, Plymouth, Scilly and Brest from the period surveys, and two hundred features in the pilots' words (Faden 1793, White 1835, Imray 1874): headlands, rocks, marks, lights with the year each was first lit. The chart data's sources and licences are printed by `py tools/chart_manifest.py`. The world level and the Atlantic are built on your machine by the tool when wanted; the region is in the zip.
2. **Two positions, kept apart.** The world keeps the truth from the physics; the master keeps the reckoning, advanced each hour by the log-line along the compass course with the chart's variation a decade old, the leeway allowed for, and every error term of the study seeded and named. A sounding, a bearing and a noon sight each collapse it by their own measure. No reading, no snapshot and no drawing ever gives the truth: the chart in the browser is the captain's, drawn at the reckoned position with the ellipse of the master's doubt.
3. **The lookout.** What is in sight from the masthead by the horizon formula, the visibility and the daylight: "The Lizard bearing NNW, distant four leagues", a light at night by its range and its year, a danger within three miles, in the log at the moment it is raised.
4. **Four ships.** The cutter and the brig sail through the same orders as the frigate and the schooner, from the same files' rules. The cutter is about in under two minutes and spins in her own length; the frigate hung in stays in a light breeze is boxed off as Luce has it; a course is refused while she lies hove to; a sheet let fly stays let fly until hands haul it.
5. **A save loads in seconds.** A checkpoint is written beside every save and `--load` reads it directly, proven equal to the replay.

Truths 58, 59, 65 and 73 to 76 were added; all pass. Truth 73 is worded as you ruled it (a cutter points as a schooner does, or closer).

## What you need

As before: Python 3.11 or newer (`py`) and the gate zip extracted to a fresh folder. The chart data is in the zip (17 MB); nothing is downloaded. Two of the local packages you approved (32c, the suite in two tiers, and 32d, the `freesail` command) were written for your local sessions and are not in this cut, so the setup is the module form as at gate 5a.

## Setup

In a terminal in the extracted folder:

```
py -m pip install -e ".[dev,server,agents]"
```
*Ends with "Successfully installed ...".*

```
py -m pytest -n 4
```
*Ends `2063 passed, 7 xfailed` or a few more (the build machine: about twenty-five minutes on four workers; the count is on the release page's notes if it moved at the cut). The seven expected failures are your earlier rulings (truth 3 for the schooner, truth 11's ground, truth 18's times, and truths 24, 26, 28 and 31). A `failed` is a fault. The three passages of this gate run in it, and the day under systems.*

## The passages

**The frigate, clear** (`data/scenarios/gate-5b-passage.yaml`, seed 7, the weather pinned SW 15 knots and the sky clear): *Amazon* off the Stiff at 04:00 on 10 June 1805, plain sail, heading north for Falmouth, a sextant aboard and no chronometer. Her captain's book (`gate-5b-passage.orders`) beside the starter routines: a bearing of the land every glass while it is in sight, the ship brought to at noon and the deep-sea lead hove, the course for Falmouth shaped from the account, the hand lead going in every glass and then every ten minutes past the Manacles, and at the first cast under twenty fathoms she wears and lies to on the starboard tack, forereaching off the land, since the anchor is package 34's. **The frigate, thick** (`gate-5b-passage-thick.yaml`): the same passage in fog, no sight, no bearings, the course shaped by account when the run since noon says she is off the Lizard, and at the first land seen close aboard she stands off to the southward. **The schooner** (`gate-5b-passage-schooner.yaml`): the same passage in *Speedwell* with an octant, no glass, the log every two hours; the cutter and the brig sail six hours of it through the same orders with `--ship`.

The account against the truth, at seed 7 (the author's view; the game never shows it):

| Moment | Frigate, clear | Frigate, thick | Schooner |
|---|---|---|---|
| Noon, 11:59 | latitude observed 49° 25′; the reckoning was 49° 27′; 4.8 miles from the truth | no sight, the sun hid in fog; 5.7 miles | observed 49° 21′, the reckoning was 49° 28′; 3.6 miles |
| The deep-sea lead, 12:18 | fifty-two fathoms, fine grey sand with black specks; 4.5 miles | fifty-two fathoms; 5.5 miles | fifty-two fathoms; 2.4 miles |
| The landfall | 16:28, the Beast and the Lizard lights NNW four leagues; 8.1 miles by account, 6.2 after the bearing | 19:08, the land about Black Head close aboard, a mile; 10.9 miles wrong, she believed herself off Falmouth | 16:15, the Beast and the Lizard, four leagues; 4.0 miles |
| The end | 20:11 sixteen fathoms in the outer road; wore, hove to on the starboard tack at 20:18, no bottom at twenty after; within a mile | standing off S from 19:08 | 18:51 fourteen fathoms; wore, hove to at 18:59 |

The reckoning's doubt after thick weather (truth 58, 150 miles a day): one day 10 × 4 miles, two days 20 × 6, four days 39 × 9, east-west by north-south, inside the study's 30 to 50; a clear noon collapses the north-south axis to 4.

## Items

- [ ] **1. The frigate's passage in the browser.**
  ```
  py -m freesail.ui.server --scenario data/scenarios/gate-5b-passage.yaml
  ```
  Open the address. *The log opens `The passage for gate 5b, Ushant to Falmouth. Wind SW, 15 knots, a moderate breeze. Heading N (357°).`, then the lookout's first look (`Ushant bearing SW, distant three miles.` and the rest), the departure bearing (`The light on Ushant bore SW by S, a mile by estimation.`) and `Shaped a course for Falmouth: N by account, 99 miles.` The map is the captain's chart: the coast of the western Channel with its names, the hull drawn at the reckoned position with a faint ellipse about it, the track by account behind her; nothing marks where she truly is.* Press **60x**. *Every hour `Hove the log: six knots and a half.` (or so); at 11:59 `Noon. Latitude by observation 49° 25′ N; the reckoning was 49° 27′ N. Course made good since the departure N, 58 miles. Longitude by account 4° 57′ W.`; the book brings her to (`Hove to, main topsail to the mast, helm a-lee.`) and heaves the deep-sea lead: 12:18 `Fifty-two fathoms; fine grey sand with black specks.`, the account moved on to the chart's contour; `Filled away`, and `Shaped a course for Falmouth: N by W by account, 44 miles.`*

- [ ] **2. The readings of the reckoning.** At any moment type `the reckoning` (*`49° 52′ N, 5° 08′ W by account` or the like*), `the reckoning's uncertainty` (*the master's words, "I would not trust the reckoning within ... miles east or west, nor ... north or south", the miles growing through the afternoon and shrinking with each bearing*), `the depth` and `the ground` (*from the last cast, with its age: `Fifty-two fathoms, fine grey sand with black specks, an hour ago` or `no bottom by the last cast`*), `the distance run since noon`, `the course made good`, `the latitude by observation`, `the master` (*`Mr <name>`, his skill*). Before the landfall, `the bearing of the Lizard`: *refused, `not in sight`.* Say in the form whether the master's words for his doubt are the words you would want from him.

- [ ] **3. The landfall and the run in.** At 300x from the afternoon: *16:28 `The Beast bearing NNW, distant four leagues.` and `The Lizard lights bearing NNW, distant four leagues.` (the landfall, notable), `The Beast bore N by W, two leagues by estimation.` and `Shaped a course for Falmouth: N by E by account, 17 miles.`; a bearing every glass thereafter (Black Head, Lowland Point, Manacle Point, St Anthony's Head), the lead every glass (`No bottom at twenty fathoms.`) and every ten minutes past the Manacles; the dangers hailed as she passes them (`The Manacles bearing NNW, distant three miles: a danger.`); 20:11 `And a quarter sixteen; good ground.` and `By standing order 'the outer road': wearing ship.`; 20:17 `Wore ship; braced sharp up on the starboard tack, heading S (175°).`; 20:18 `Hove to, main topsail to the mast, helm a-lee.`; then `No bottom at twenty fathoms.` every ten minutes as she forereaches off.* The ellipse on the chart shrinks with each bearing to less than a mile. Say in the form whether wearing and lying to off the road, with no pilot and no anchor yet, is what her captain would do at dusk.

- [ ] **4. The passage in thick weather.**
  ```
  py -m freesail.ui.console --scenario data/scenarios/gate-5b-passage-thick.yaml
  ```
  `go`, `speed 300`. *11:59 `Noon. No sight; the sun was hid at noon in fog. Latitude by account 49° 27′ N.`; the same cast at 12:18; 16:37 `By standing order 'off the Lizard by account': shaping a course for falmouth.`; the lead every glass with no bottom; 19:08 `The land about Black Head close aboard on the starboard bow, bearing N, distant a mile.` and `By standing order 'the land': steering S.` She believed herself off Falmouth; she was eleven miles short, and the Manacles a few miles to the west of her.* Type `the reckoning's uncertainty` after the landfall: *the master's doubt, three miles each way.* `hold` when she is standing off. Say in the form whether the fog's landfall reads as the thing that happened to *Apollo*'s convoy.

- [ ] **5. The schooner with her octant.**
  ```
  py -m freesail.ui.console --scenario data/scenarios/gate-5b-passage-schooner.yaml
  ```
  `go`, `speed 300`. *The log hove every two hours (06:00, 08:00, 10:00); 11:59 `Noon. Latitude by observation 49° 21′ N; the reckoning was 49° 28′ N.` (the octant's two to three miles); the Lizard at 16:15; 18:51 fourteen fathoms and the wear, hove to on the starboard tack at 18:59.* Then the cutter and the brig through the same orders:
  ```
  py tools/day_log.py data/scenarios/gate-5b-passage-schooner.yaml --hours 6 --reckoning --ship data/ships/cutter.yaml
  py tools/day_log.py data/scenarios/gate-5b-passage-schooner.yaml --hours 6 --reckoning --ship data/ships/brig.yaml
  ```
  *Each ends with the account against the truth at each bearing and no order refused; the cutter's plain sail is her mainsail, foresail, jib and topsail, the brig's the frigate's less a mast.*

- [ ] **6. Staying and sheets, on the cutter and the frigate.** A fresh console game in the cutter, close-hauled: `py -m freesail.ui.console data/ships/cutter.yaml --seed 7 --wind 0,15 --heading 293`, `go`, `set plain sail`, then after five minutes `tack ship`: *`Ready about. Helm's a-lee; ease off the head sheets; haul aft the mainsail sheet.`, `Topsail taken aback.` at about 17 s, `Let go and haul. Draw jib; trim aft the head sheets.` at about 22 s, `Tacked; braced up on the larboard tack` inside two minutes.* In the frigate in a light breeze (`data/ships/frigate-36.yaml --seed 7 --wind 0,7 --heading 293`, plain sail, `tack ship` once she has 2.5 knots): *`Her way is gone; she hangs in stays. Helm kept a-lee; the head yards aback to box her off; the head sheets held to windward; the spanker boom hauled over to windward.`, then `Her head is through the wind; the head sails aback pay her off.`, and she tacks in about seven minutes.* In 6 knots she misses stays as before, but the yards are squared as a brace over forty-five seconds and the log says so. Then the sheets: `let fly the main sheet` on the schooner (`data/ships/topsail-schooner.yaml`), `the mainsail` (*the sheet free, the sail flogging*), `trim the mainsail` (*the afterguard haul the sheet back with hands and time; the sail draws again*). Say in the form whether the frigate boxed off reads as Luce's page.

- [ ] **7. Save, checkpoint, load** (carried from gate 5a). In the browser game of item 1, at any moment, `save passage.json`: *`Saved to passage.json at tick <N>; the log's digest is <sixteen characters>.` and a file `passage.checkpoint` beside it.* Stop the server and
  ```
  py -m freesail.ui.server --load passage.json
  ```
  *`Loaded passage.json: from its checkpoint at tick <N>, <the ship's time>; the log's digest is <the same>.` in a second or two, not the minutes a replay took; press go and the passage goes on.* With `--watcher fake` on the save, the watcher is at its station after the load.

- [ ] **8. Two days from the climatology** (carried from gate 5a, item 7 there): the two small scenario files as that item gives them, run at 300x in the console for a day each, and `py tools/climatology_check.py --months 1000 --seed 7`. Say in the form whether the two days read as winter and summer in the Channel.

- [ ] **9. The chart's sources.** `py tools/chart_manifest.py`: *every source with its licence and what it was used for, the region's bounds, the world and the Atlantic as not committed with the command that builds each, the study's unverified list as checked, and the attribution the game shows.* The browser's chart carries the same attribution in its corner.

- [ ] **10. The truths of this gate.** `py -m pytest tests/test_known_truths.py -k "truth_58 or truth_59 or truth_65 or gate_5b" -n 4` and `py -m pytest tests/test_ships_hierarchy.py tests/test_staying.py -n 4`: *all pass; the hierarchy file's four are truths 73 to 76 (the cutter as close to the wind as the schooner, the brig as a ship, the two beam reaches), the staying file's the turning circles and the tacks by ship.*

- [ ] **11. Rulings wanted.**
  - **Lying to at the passage's end.** With no anchor until package 34, both clear passages end with the ship wearing at the outer road and lying to on the starboard tack, forereaching off the land at a knot or two. Hove to on the tack she arrived on she forereached on to the Roads' banks in four minutes (the lead's finding of 2026-09-30), so the book wears her first. Rule whether that is the ending to keep until 34's anchor, or whether the passage should end earlier, in the offing.
  - **The variation.** The reckoning's compass variation for the Channel in 1805 is 24° west, the study's unverified figure (no field model is computed by the chart build and no azimuth observation is built). Rule whether an azimuth (`observe an amplitude`, the master finding the variation at sunrise) comes with 33b or waits.
  - **The small vessels' tacks and turns.** The schooner about in two and a half minutes, the cutter quicker, the brig as a ship, and each ship's turning circle in her own lengths, are judgement bands with the sources named as far as they go (Luce 1884 ch. XXXIV for the schooner; the type's reputation for the cutter; Appendix L's trials are steamships'). Rule whether the bands stand or whether you have figures.
  - **The sheet-tending routine.** The starter book now tends the sheets every glass with the afterguard, since the free tending is retired; a standing order's firing on a cadence is a routine line in the log. Rule whether every glass is the cadence, or whether a shift of a point should tend them instead (both are in the dialect).

## The report

Fill `docs/playtests/README.md`'s form in a new folder, `docs/playtests/<date>-gate-5b-<the passage>/notes.md`, with the save beside it. Anything a navigator would call wrong in the master's words or the lead's, and any place the chart's names or the pilots' words jar, is what section 7 of the form is for.

## What this gate does not do

- **The chronometer, the lunar and the moon** (package 33b, gate 5c's set): no longitude but by account.
- **The tide** (34): the stream does not set her and the lead reads the datum's depth; **grounding's consequences** (34): taking the ground is an urgent line and a stop, no more; **anchoring** (34): she lies to instead.
- **The pilot, the port and its people** (35): the passage ends off the road.
- **Sail in sight** (36): the lookout sights the land and its marks only.
- **The `--casual` display of the truth**: a later display choice, not built.
- **A per-sail pointing from the sail's own geometry** (spec M5 open item 12's last paragraph): the cutter points as the schooner does, by your ruling.
