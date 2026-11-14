# Spec reader 02: `docs/TechnicalSpec-M5.md` against the code

Commit 504a25066c6995ce9829a19ffc597feb510a1870. The specification was read whole (1514
lines, 122,396 characters). The code was read by section, not whole: `freesail/world` alone
is 63,810 lines, so what I read and what I did not is listed at the end. No test suite was
run; a handful of short python calls (under ten seconds each) are quoted where used. Nothing
under `docs/dev`, `docs/design`, `docs/playtests` or `docs/gates` was opened.

The proposal's words for this milestone: "Weather systems, a small map with coast and depth,
tides, dead-reckoning navigation, two ports with markets, a dozen NPC ships with LOD.
Proves: emergent play; a passage is a game", and "no true-position readout in the default
game ... the design keeps the two positions separate".

---

## 0. The four questions put to me, answered first

### 0.1 Can the true position reach the player or a model?

**The readings: no, as far as I could find.** `api/queries.reckoning_block`
(queries.py:139-170) gives the account, `snapshot` blanks `ship.x`/`ship.y` on the sphere
(queries.py:265, 299-300), and the lookout's reading strips the true distance and rounds a
mark's bearing to the point (`lookout.Lookout._data`, lookout.py:653-669). The model's tools
give log *text* only (`agents/tools.log_line`, tools.py:183-198) and refuse `truth` to all but
the director (tools.py:534-539). `Navigation.to_dict` (reckoning.py:5418-5439) carries the
account and the sights' own figures, no truth. The test
`tests/test_readings.py::test_no_reading_gives_the_true_position_by_any_road` (line 724) holds
the registry to it, but only the registry: it does not look at the log's data or the wire.

**The log's data: yes, to a few metres, and it reaches the browser.** The lookout's
sighting line is built by `_line_data` (lookout.py:634-650), which keeps `Sighting.to_dict`'s
`bearing_deg` (true, to 0.1 degree) and `distance_m` (true, to the metre) for every charted
mark (it pops the distance only for a sail). That event is not record-only
(`core/events.for_the_record`, events.py:198-203), and `/api/log` (server.py:1520-1535) and the
websocket's `shown_log` (server.py:538-550) send `event_dict(e)`, which is `e.to_dict()` with
its `data` (server.py:916-921). `/api/chart` sends every feature's true latitude and longitude
(queries.py:123-134). Measured (a brig at rest, 50.05 N 5.0 W, 600 ticks, seed 7): six
`lookout.sighting` events; from each, the feature's position less the logged bearing and
distance gives the ship's true position to 4.7, 9.2, 9.4, 12.4 and 15.4 metres. The
specification knows the road (§33 item 25, last bullet: "If the log's data reaches the
browser, it is a road the proof of §15 does not cover"); it does reach it. The client does
not draw it (client/log.js uses `data` only for a roll-up's ticks), so the player must open
the browser's developer tools; but the promise was "by any road".

Lesser roads, each *sure* as code and *low* in weight:
- `observe an amplitude` / `observe an azimuth`: the `reckoning.variation` event carries the
  sun's true azimuth (0.1 degree) and its altitude at the true place to 0.01 degree
  (`sights.amplitude_or_azimuth`, sights.py:795-800; `orders/navigation.py:1736-1738`). An
  altitude and an azimuth at a known instant are a position; the moon's altitude behind
  `the moon` is excepted by the test (`THE_SKYS_ROWS`), this one is not mentioned.
- `GET /api/save` (server.py:1557-1563) hands the browser the whole save, truth included. The
  specification allows "the truth is in the save" (§17); it is one click from the page.
- "The chart has nothing to the W of this" (lookout.py:545-556) is said from the true place
  against the chart's edge; land-ahead and the pilot's warnings read the true track by design
  (§12, ports.py:29-34).
- An observer's world draws its chart about the truth (queries.py:146-163), by design.

### 0.2 What a port's market, dockyard and crew pool actually do

- **Market** (`ports.Market`, ports.py:401-453): a base price per good from the port file
  times three factors: a month multiplier from the file (`season`), 1.5 when the good's
  origin nation is at war with the port's (`WAR_FACTOR`, ports.py:339), and supply, which
  is only the net tons sold to the port less bought from it, 1 per cent a ton, clamped 0.5
  to 2.0, decaying by a seventh a day when next read (ports.py:333-336, 410-418). There is no
  demand term apart from the same net tons, no stock, no consumption. Far traders of the
  world's business do move it (`business.transact`, business.py:80-134). Every price in the
  port files is "FROM MEMORY" by their own heads (falmouth.yaml:22-27). Buying needs the price
  list brought off by the boat (dealings.py:2294-2298); the goods come by the boat or a lighter.
- **The war is counted twice.** Brest's tin is 180 in the file "scarce under the blockade"
  (brest.yaml:70) and Falmouth's brandy 200 "a smuggler's price while France is at war"
  (falmouth.yaml); the rule then multiplies both by 1.5. Measured on 12 June 1805: tin 120 at
  Falmouth, 270 at Brest; brandy 110 at Brest, 300 at Falmouth. Each leg of a round trip more
  than doubles the money, before supply moves.
- **Dockyard** (`Dealings.demand`, dealings.py:2529-2610; `_apply_job`, 2734-2788): it
  *supplies* a spare topmast, topgallant mast or yard to the booms, a spare suit of sails to
  the sail room, cordage, water and provisions, after a time and at a cost (free at Plymouth's
  King's yard). **It repairs nothing**: no hull, no damaged spar or sail in place, no
  careening; grep for repair/refit/careen in `world/dealings.py` and `world/ports.py` finds
  nothing. Repairs remain the crew's own evolutions with the spares. Brest's arsenal is
  `kind: yard` with prices, so a neutral paying 45 pounds is told it was "by demand on the
  King's yard, surveyed and vouched" (dealings.py:2595-2598).
- **Crew pool** (`Dealings.enter_hands`, dealings.py:2612-2682): hands by rating (able,
  ordinary, landsman) at a bounty and a delay, mustered with names and skills by rating
  (2817-2863). The pool is decremented (`pool["hands"] = have - taken`, 2658) and nothing
  refills it except a dated row in the port file; Falmouth has 4 able seamen for the whole
  game.
- **Stance** (`Ports.stance`, ports.py:1238-1246): from the nations table, closures and a
  blockade; closed or hostile refuses trade, yard and hands in words.

### 0.3 The levels of detail and the cap

Three tiers, where the specification has two:
- **Far** (`ships.Vessel.tick`, moved every `VESSEL_TICK_S = 60` s, ships.py:93) by a polar
  drawn from her file.
- **Near** within `NEAR_DETAIL_NM = 2.0`, demoted beyond 3.0 (ships.py:128-129): ticked each
  second, a keep-course captain.
- **Crewed** within `CREWED_NM = 4.0`, demoted beyond 6.0 (crews.py:90-91): the full
  part-and-crew ship with a rules-based captain. The crewed range is wider than the near
  one, so the near tier serves only brainless vessels and those over the cap (likely; I did
  not trace `_promote_and_hail`).
- **The cap**: `CREWED_CAP = 3` beside the player's (crews.py:98), plus up to
  `HELD_OVER_CAP = 2` hulls whose captain a model holds (crews.py:106): at most five crewed
  hulls and the player's. The pace floor with the cap full is `CREWED_FLOOR_TICKS_S = 60`
  (crews.py:99); tests that name it: test_crews.py, test_brains.py, test_known_truths.py,
  test_director.py.
- The dozen: the two gate scenarios name 12 and 11 ships
  (`grep -c goal:` on merchant-passage.yaml and naval-cruise.yaml); the world's business may
  add more, to `most_ships: 16` (data/business.yaml:43).

### 0.4 The "small map, roughly a hundred by a hundred miles"

Measured from `data/charts/manifest.yaml` and the disk:
- **20 regions** at levels 2 and 3, plus two committed level-1 corridors (48 and 6 tiles):
  the Channel in three, Biscay in two, Portugal, the Strait, the western Mediterranean,
  Balearics, the Gulf of Lion, Ligurian, Tyrrhenian, Catalan, Sardinian, Tunis, Sicily,
  Madeira, the Salvages, the Canaries and the Azores.
- Their bounding boxes add to **about 804,000 square nautical miles** (some overlap), against
  the proposal's 10,000. The western Channel region alone is 156 by 180 miles.
- **2,325 tile files** (`find data/charts/tiles -type f | wc -l`; 1,587 at level 2, 684 at
  level 3, 54 at level 1), 2,398 files tracked under `data/charts`; **359 MB on disk**
  (tiles 352 MB by the manifest's bytes), a 398 KB manifest, and the repository's pack is
  427 MiB (`git count-objects -vH`). The specification's bound was "the region's tiles ...
  under 25 MB compressed" (§10); channel-west alone is 17.4 MB and within it.
- Around it: **121 port files** (the proposal said two), **100 tide gauges** and 82 stream
  areas (the specification said eleven gauges).
- What the game uses: of 69 scenarios, 31 say `region: channel-west`, 14 `chart:
  atlantic-east`; positions in the Mediterranean, Madeira and the Strait appear in a few.
  But every world with a chart loads every port file when the scenario names none
  (`Ports._load`, ports.py:1219-1220): a channel-west world was measured holding all 121
  ports, Ajaccio and Algiers among them, and took 6.3 s to make (`make_world`, brig, seed 7,
  with a timed suite running on the machine).

---

## 1. The commitments, one by one

| § | what the specification says is built | verdict | where it lives | how you know |
|---|---|---|---|---|
| 2 | Pressure systems, geostrophic wind turned 15 deg and scaled 0.7 | built as specified | world/weather.py (`SURFACE_TURN_DEG = 15`, `SURFACE_SCALE = 0.7`) | grep |
| 2 | Climatology per month, provisional | built as specified | data/weather/climatology.yaml:52 `provisional: true` | grep |
| 2 | Draws from a named `weather` stream | built as specified | core/world.py `stream("weather")` | grep |
| 2 | A thousand-month test within 5 points | built (test exists) | tests/test_known_truths.py `CLIMATOLOGY_TOLERANCE_PCT` | grep; not run |
| 2 | The glass checks at the cold front | not built | no trough in weather.py | `grep -i trough` empty; §2 and item 9 say open |
| 3 | Gust factor by air mass; squalls 1.30 to 1.45 | built as specified | physics/wind.py:64-75 | read |
| 4 | Sea state by lag; swell; roll capped | built as specified | world/sea.py:81-82; physics/motion.py:78 `ROLL_MAX_DEG = 35.0` | read |
| 4 | "The sea outlasts the wind by hours" (truth 56) | built otherwise (suspicion) | sea.py:81-82: `SEA_BUILD_HOURS = 6`, `SEA_DECAY_HOURS = 4` | the wind sea falls faster than it rises; the outlasting must come from the swell. Not measured |
| 5 | The glass in inches, the tendency, the sky, the sea as readings | built (not traced row by row) | api/readings.py | grep of the registry ids |
| 5 | No reading names a front, centre, isobar, hPa (truth 57) | cannot tell | a test exists by its truth number | not run |
| 5 (37f) | Wind-shift floor four knots; aback lines once; `done_already`; `say_held`; `check_places` | built as named | core/world.py `_log_wind_shift`, `WIND_SHIFT_FLOOR_KN`; physics/hull.py `aback_lesser`; evolutions/runner.py; standing/runtime.py; standing/book.py | grep, each found |
| 9 | Latitude and longitude frame; plane kept for tests | built | world/geo.py; `World.place_of_plane` | grep |
| 9 | One frame for plane points (37d) | built | core/world.py `place_of_plane` | grep |
| 10 | Tiles int16 decimetres in 512-cell tiles at four levels | built as specified | manifest.yaml `levels` (cell_sec 150, 30, 3, 0.5; tile_cells 512) | read |
| 10 | Build tool refuses disallowed licences; four sources | built (sources) | manifest.yaml `sources`: GEBCO, EMODnet, SHOM HOMONIM, Histolitt | read; the tool (3,099 lines) not read |
| 10 | Region's tiles under 25 MB | built for channel-west; overtaken for the chart | 17.4 MB channel-west; 352 MB in all | §0.4 |
| 10 | Unverified items checked "each a morning's work" | built in part | data/charts/unverified-checks.yaml: the Défense library and Gallica "Still unverified" | read |
| 11 | Depth, aground, nearest coast, in sight by 2.08(sqrt h + sqrt h) | built as specified | world/geo.py:186-191; chart.py | `horizon_nm(24.1)` = 10.21 nm = 2.08 x sqrt(24.1) |
| 11 | `Chart.nearest_shore`, `coast_trend` (37d) | built as named | chart.py | grep |
| 11, 17 | The captain's chart a separate product, degraded (a longitude error of the period's chart) | **not built** | queries.py:108-136 sends the modern coast and the features' true positions; the master's casts are matched against `world.chart`, the truth tiles (reckoning.py:2955-3061) | the scenarios' `papers: chart: {year: 1804}` (39 files) is read by nothing: `grep -rn 'year'` on the parser finds no reader (scenarios.py:546-603) |
| 12 | The lookout's words; distance re-judged as it changes; shore a sighting; land ahead | built | world/lookout.py | read in part |
| 12 (68) | `lookout.riding`, `RIDING_WAY_KN` | built as named | lookout.py | grep |
| 13 | Two positions apart, a two-by-two covariance, the master's words | built | world/reckoning.py | `to_dict` read; the account and truth differ in the measured run only by the departure |
| 13 (37e/37j) | One rule for every observation; `OBSERVATION_OUT_SIGMAS` = 2; kept under half a cable | built as specified | reckoning.py:385 `2.0`; :388 `0.05` | grep |
| 13 | `FIX_RUN_NM` and `weigh_line` gone | built as specified | `weigh_line` absent; `FIX_RUN_NM` survives only in a comment (reckoning.py:353) | grep |
| 13 | Compass allowance 2.5 deg; fix by marks cutting 30 deg | built as specified | reckoning.py:447, :574 | grep |
| 13 | The departure at the truth with a mile's doubt | built (not traced) | §13 last paragraph | not checked |
| 14 | Noon latitude; chronometer; lunar drawn, not computed | built | world/sights.py (`Sight`, `TimeSight`, `Lunar`) | read the records |
| 14 | "If the moon model runs past about a hundred lines" | built otherwise | core/moon.py is 219 lines | wc |
| 14 | `VARIATION_1805_DEG` from gufm1 at build | not built | reckoning.py:273 `24.0`, the study's figure | §33 item 14 says so |
| 15 | The orders and readings of 5b | built (sampled) | orders/navigation.py; api/readings.py | grep of verbs |
| 15 (37j) | `the depth of water` and `the port` by account | built as specified | tests/test_readings.py:758-797 | read the test |
| 15 (37j) | No reading gives the true position by any road | **built in part** | registry only; the log's data carries it (§0.1) | measured |
| 16 | M2, S2, N2 at eleven TICON gauges | built otherwise (grown) | data/tides/constituents.yaml: 100 gauges | python count |
| 16 | The master's tide from his book and his account, never `Tide.at` | built as named | reckoning.py `book_tide`, `_tide_between`; tide.py `Directions`, `BookStream`, `load_directions` | grep; a test reads the source |
| 16 | No tide readout, ever | built (as far as read) | no reading row for the tide's height found | grep of registry ids; not exhaustive |
| 17 | The truth not in the snapshot | built as specified for the snapshot | queries.py:253-300 | read; and see §0.1 for the log |
| 17 | `--casual` display of the truth | not built (deferred by the spec) | none | `grep -rn casual` finds only "casualties" |
| 18 | Grounding; anchoring as evolutions; dragging; the deep road; `LET_GO_STATES` | built as named | evolutions/scripts.py; physics/anchor.py (`judge_cables`, `GROUND_HOLDING`, `SHORT_SCOPE_PER_DEPTH`, `DRAG_HOLDS_AGAIN_S`) | grep |
| 18, 32 | The kedge later | overtaken: built | evolutions/scripts.py:8678 `LayOutKedgeScript` | grep |
| 22 | Places and people, the inward minimum | built otherwise (grown) | world/places.py (1,022 lines), people.py (1,763) | wc; not read whole |
| 23 | Two ports | built otherwise | 121 files in data/ports | ls |
| 23 | Market: prices that move with supply, demand, war, season | built in part | ports.py:401-453 | §0.2: supply is net tons; no separate demand; war counted twice in the data |
| 23 | Dockyard: repairs and stores by the part graph | built in part | dealings.py:2529-2788 | stores and spares only; no repair |
| 23 | Crew pool by rating at a price and a delay | built as specified, finite | dealings.py:2612-2682 | never refilled |
| 23 | Stance decides entry | built | ports.py:1238; truth 70's test | read |
| 23 | Arriving: pilot cutter, pilot as a person, anchorage, boat, shore | built | ports.py docstring; dealings.py | not traced in full |
| 23 | The cutter as a ship file, no engine change | built (file) | data/ships/cutter.yaml | ls; "no engine change" cannot tell |
| 24 | Nations table, war in 1805 | built | data/nations.yaml; nations.py `at_war`, `declare_war` | grep |
| 25 | A dozen at far detail, plans, polars, roll-up cadence | built as specified | ships.py:1-140, `VESSEL_TICK_S = 60` | read |
| 25 | Near detail within a stated range; the switch; crewed is M6's | overtaken | crews.py, spec M6 | §0.3 |
| 25 | Sighting at the horizon; "Sail ho!" bearing first; rig at 4 nm, colours 2, made out 1.5 | built as specified | ships.py:97-110 | read |
| 26 | World orders journaled; refused at the captain's grammar | built | world/orders.py `REFUSAL`; truth 71's test | read the docstring |
| 26 | The channel: append a system, a ship, a message, a stance or price, a person | built otherwise (grown) | world/orders.py is 4,746 lines with the director's `aboard:`, `say as`, `ship "X": order` | docstring 1-104 |
| 27 | Two scenarios: the merchant passage and the naval cruise | built | data/scenarios/merchant-passage.yaml, naval-cruise.yaml | ls |
| 28 | Truths 67 to 72 | built (tests exist) | test_known_truths.py:3654-4587 | grep names; not run |
| 29 | The officer of the watch, the general grant and its kept-back list | built as named | agents/agent.py `GENERAL_KEPT_BACK_WORDS` | grep |
| 30 | 500 ticks a second floor | built (one measurement) | none checked | 3,600 ticks of a brig in 2.77 s (about 1,300 a second) with a suite running |

---

## 2. The pointers

Twenty taken through the document: `SURFACE_TURN_DEG`/`SURFACE_SCALE` (§2),
`climatology.yaml provisional` (§2), `World._log_wind_shift` (§5), `HullState.aback_lesser`
(§5), `standing/book.check_places` (§5), `Chart.nearest_shore` (§11), `lookout.riding` (§12),
`Reckoning.observe_line` (§13), `OBSERVATION_OUT_SIGMAS` (§13), `Navigation.take_fix`,
`_choose_marks`, `_fix_of` (§13), `Reckoning.within_doubt`, `widen_toward` (§13),
`tide.BookStream`, `load_directions` (§16), `Chart.line_shore` (§15), `scripts.LET_GO_STATES`
(§18), `GroundTackle.carries` (§18), `DRAG_HOLDS_AGAIN_S` (§18),
`agent.GENERAL_KEPT_BACK_WORDS` (§33.23), `sights.RATE_DOUBT_S_PER_DAY` (§33.21),
`tests/test_replay.py::test_a_door_act_at_the_stationing_tick_is_made_by_a_replay` (§33.11),
`orders.navigation._course_not_laid` (§33.24).

**19 of 20 hold** by name (I grepped some fifty more names besides; all but the one below were
found). The one that does not: `orders.navigation._course_not_laid` (§33 item 24) does not
exist; the nearest is `not_laid` on a script, evolutions/scripts.py:1071-1105. I checked
what each does only where §0 needed it.

## 3. The numbers

- 2.08 (sqrt h_eye + sqrt h_obj) miles: holds (`horizon_nm(24.1)` = 10.21).
- `CREWED_CAP = 3`, `NEAR_DETAIL_NM = 2`, `CREWED_NM = 4`: read; held by tests by name.
- `OBSERVATION_OUT_SIGMAS = 2.0`, `COMPASS_ALLOWANCE_DEG = 2.5`, `FIX_MIN_CUT_DEG = 30`,
  `RATE_DOUBT_S_PER_DAY = 1.0`, `VARIATION_1805_DEG = 24.0`: as the document says.
- Gust ranges 1.10-1.20, 1.15-1.30, 1.20-1.30, squall 1.30-1.45: as the document says.
- Truth 69's war factor 1.5: held by `test_truth_69` (test_known_truths.py:3775-3783).
- Ticks a second: one run, about 1,300 for a brig with one vessel, on a loaded machine.
- Truths 52 to 76: tests exist by number; not run, so not checked.

## 4. The open items (§33)

The list is numbered 1 to 26 with a second item 16 after 26: **27 items**, five of them
(21 to 26) lists of six to nine sub-items each, so some **55 open points** in all. In outline:

| item | status at this commit | how I know |
|---|---|---|
| 1 climatology from printed tables | still open | `provisional: true` in the file |
| 2 quotations verified | cannot tell | needs the design notes |
| 3 chart study's unverified list | still open in part | unverified-checks.yaml "Still unverified" |
| 4 lunar constants | still open | the spec's own word; no new source seen |
| 5 the schooner's storm trysail | cannot tell | trysail appears in three brig files only (grep) |
| 6 a lookout station | built | the `lookout` row in THE_EYES_ROWS (test_readings.py:715-718) |
| 7 the sail room in the browser | likely built (papers) | not traced |
| 8 wave-growth sources from a page | still open | sea.py says "worked but not read" per §4 |
| 9 frontal trough; north quarter | still open | no trough in weather.py |
| 10 the lead at a station | cannot tell | gate record not read (forbidden) |
| 11 door act replay | closed (pointer holds) | test name found |
| 12 physics of staying | built in part | `RADIUS_OF_GYRATION = 0.25` a fixed fraction (physics/hull.py:97); `BoxOffScript` exists |
| 13 sheets and trim one record | **quietly built**: the item is not marked closed | evolutions/trim.py:294-562 (sheet geometry, `set_sheet_angle`); `tend_sheets` gone |
| 14 variation from gufm1 | still open | reckoning.py:273 |
| 15 | closed | marked so |
| 16 GEBCO fill sweep | cannot tell | tool not read |
| 17 replies placed by count | still open | `Playback._due` in agents/harness.py |
| 18, 20 | closed | marked so |
| 19 the sun reads `ship_x` | still open | core/world.py:1540, 1544 |
| 21 to 26 | mostly open by their own words; 22's relapsing drag built by 37k (`DRAG_HOLDS_AGAIN_S`); 25's last bullet (the log's data) **still open and real** (§0.1) | grep; measured |
| 16 (second) gripe and wear | open, narrowed | its own words |

The tail is long and is itself the finding: a specification whose open items run to a
quarter of its length (§33 is lines 1158 to 1482, about 32,800 characters of 122,396) and
whose numbering has broken (two items 16).

## 5. The document as a document

- **Mostly history.** 18 "As built" paragraphs, 76 package references, 39 dated rulings;
  §33 alone is about 27 per cent of the text and §34 is a record of rulings. My estimate is
  that half the document is account rather than contract. §31 says the specification "keeps
  the contract and points to the close-out rather than growing 'as built' paragraphs"
  (lines 1146-1149); the document then grows eighteen of them.
- **It supersedes itself in place.** §13 has four layers (33a, 37d, 37e, 37j), each saying
  what of the last is superseded ("What 37d's paragraph above says ... is superseded by this
  one", line 444; "amended by this one", line 529). A newcomer must read the history to find
  the rule.
- **It names model products and vendors** in §29 and §31 as the builders of packages; that
  is project management, not specification.
- **It is no longer the truth about scope.** "Two ports, Falmouth and Brest" (§23) against
  121; "eleven TICON gauges" (§16) against 100; "the western Channel" (front matter) against
  twenty regions to Sicily and the Azores. `ports.py`'s own docstring says "Falmouth, Plymouth
  and Brest" (ports.py:1-3) above a loader of 121 files.
- **Contradiction in the data's own comments**: data/business.yaml:17 "No supply and demand:
  what the ships carry moves no price" against :57-64 "`transact: true` ... each ton lowering
  the price by SUPPLY_PER_TON".
- Could a newcomer maintain the weather, the reckoning and the anchoring from it? The
  constants and functions are named and they exist (19 of 20 pointers), which is useful; the
  reasons are scattered across dated paragraphs and the tuning notes it points to.

## 6. What the specification never asked for, and what it needed and nobody built

**Grown outside the plan (in this specification's areas):** the chart to twenty regions and
two ocean corridors (about 80 times the proposal's area, 359 MB); ports from two to 121; tide
gauges from eleven to 100; a third, crewed level of detail with a cap (M6's by its own
word, but it fills this section's switch); the world-order channel grown into the director's
instrument (4,746 lines); the world's business (traders, fishermen, cruisers, convoys) that
trades into the markets.

**Needed by the specification's own logic and not built or not written:**
1. The period chart as a separate, erring product (§11, §17): the `chart: {year}` paper is
   accepted and ignored, so the chart the master works by is the sea itself; the only error
   between the two positions is the reckoning's.
2. The log's data scrubbed of the truth as the readings were (§33 item 25 saw it).
3. A crew pool that refills, and a market with demand or stock that is not the player's own
   net tons; a reason not to run the 120-to-270 tin trade for ever.
4. Port repairs: the dockyard sells spares and no hand of the yard touches the ship.
5. Loading only the ports of the chart in play: a Channel world loads the Mediterranean's.

---

## The ten findings that matter

1. **The true position reaches the browser in the log's data.** Every `lookout.sighting` of a
   charted mark carries its true bearing (0.1 deg) and distance (1 m) (lookout.py:634-650);
   `/api/log` and the websocket send it (server.py:916-921, 1520-1535, 538-550); with
   `/api/chart`'s feature positions it gives the ship's place to 5 to 15 m (measured). The
   proof test covers the registry only. *High; sure.*
2. **The captain's chart is the truth's.** No period error, no chart year read (39 scenarios
   give `chart: {year: 1804}` to nothing); casts are matched against the truth tiles
   (reckoning.py:2955-3061); the browser draws the modern coast (queries.py:108-136). Half of
   "the two positions kept apart" is missing. *High; sure.*
3. **The dockyard repairs nothing.** It delivers spares, sails, cordage, water and
   provisions (dealings.py:2734-2788); the proposal's "repairs" are not built. *Medium; sure.*
4. **The war is priced twice**: file prices already marked up for the war, then x1.5
   (`WAR_FACTOR`); tin 120 at Falmouth and 270 at Brest, brandy 110 and 300 (measured). Market
   "demand" is only the net tons sold. *Medium; sure.*
5. **The crew pool never refills** (dealings.py:2658): Falmouth's four able seamen are the
   game's. *Medium; sure.*
6. **The map has outgrown the plan by eighty times**: 20 regions, about 804,000 sq nm, 2,325
   tiles, 359 MB, a 427 MiB repository pack; and every port of every sea loads into a Channel
   world (ports.py:1219-1220; 121 ports, 6.3 s to make a world). *Medium; sure.*
7. **Levels of detail are three, with a cap of three crewed (five with model-held hulls)**
   (crews.py:90-106); near detail (2 nm) sits inside the crewed range (4 nm) and is left
   for brainless vessels. Sound, but the specification's two tiers no longer describe it.
   *Low; likely.*
8. **The sun's amplitude and azimuth log the true altitude and azimuth** (sights.py:795-800),
   a second, lesser road to the position. *Low; sure as code, likely as a practical leak.*
9. **The document is half history**, supersedes itself four times in §13, says it will not
   grow "as built" paragraphs and has eighteen; 27 open items (about 55 points), two numbered
   16, one quietly built (13), one pointer stale (`_course_not_laid`). *Medium; sure.*
10. **Scope statements are false to the code**: two ports, eleven gauges, the western Channel;
    `ports.py`'s docstring three ports; business.yaml contradicts itself on prices. *Low; sure.*

## What I did not read

- Whole files not read: `world/reckoning.py` (6,126 lines; read to_dict, the observation
  constants, the cast's opening and the own-reckoning lines), `world/lookout.py` (2,241; read
  the sighting and data paths), `world/chart.py` (1,934; read Sighting, coast_lines,
  chart_block's sources), `world/ships.py` (2,325; head and the tick), `world/crews.py`
  (head), `world/dealings.py` (3,954; trade, yard, pool, jobs), `world/ports.py` (head,
  market, Ports), `world/orders.py` (docstring only), `world/weather.py`, `world/tide.py`,
  `world/sights.py` (records and amplitude only), `world/sea.py`, `physics/motion.py`,
  `physics/wind.py` (constants), `api/readings.py` (4,865; not read beyond grep),
  `ui/server.py` (routes and event_dict), `agents/tools.py` (log_line, truth, journal).
- Not read at all: `tools/build_charts.py`, `world/places.py`, `world/people.py`,
  `world/business.py` beyond `transact`, `world/nations.py` beyond its signatures, the
  client's JS beyond a grep, the director (`agents/director.py`) beyond `reveal`, the MCP
  server, and every test but the true-position test and truth 69.
- Not checked: truths 52 to 76 by running them; the performance truths; the climatology's
  shares; whether the near tier is ever entered by a vessel with a brain; the director's log
  as revealed to the player as a road to the truth.
