# Package 125: the moment of the haul (report)

The brief: `docs/dev/briefs/Brief-Package125.md`. The lead's rulings on the ground report (2026-11-24): A by her way, the figure settled by the measure below; B closed and nothing built; C as given; D as given; E built, every captain's. On the lead's list of 2026-11-27 E is taken out (§6), and the trunk at f2821c7 (package 127) is merged in; on the lead's second list of that day (the read of a8b2c3e, §11) the trunk at f09fe283 (package 126's part one) is merged in and D is mended; on the lead's ruling on rule A that evening (§12), A acts only for a ship whose file says she is slack in stays, and none of today's does. The pins moved are in `docs/dev/TuningNotes.md` under "Package 125".

Every measure is at seed 7, made with the truths' own helpers (`close_hauled_on_starboard`: the wind from the north, no gusts, plain sail set and braced up). Tacks are from 290, 292.5 and 295 degrees, in 8, 12, 15, 20 and 25 knots. "Shortened" means the game's own `shorten sail` run to its end, then sixty seconds, then the helm put down. **S**n means stayed in n seconds; **m** means missed stays; **F** means refused; **·** means no end in 900 s.

The light corvette of the ships' package was used as a probe only, in a scratch copy. Nothing of hers is committed; her figures here are what her builder will find.

## 1. The fleet on the trunk

Under plain sail; each wind's three cells are the headings 290, 292.5 and 295:

| Ship | 8 kn | 12 kn | 15 kn | 20 kn | 25 kn | Stayed |
|---|---|---|---|---|---|---|
| frigate-36 | S239 S239 S239 | S311 S174 S327 | S343 S447 S370 | S223 S232 S272 | S236 S248 S271 | 15 |
| razee | S515 m m | S336 S358 S390 | S434 S427 S484 | S375 S362 S358 | S247 S259 S271 | 13 |
| 74 | m m m | S208 S220 S237 | S237 S243 S258 | S288 S312 S296 | S260 S265 S240 | 12 |
| 64 | S364 m m | S210 S223 S243 | S244 S251 S266 | S279 S304 S311 | S257 S288 S192 | 13 |
| brig | S430 S414 S165 | S401 S385 S378 | S440 S454 S455 | S319 "S459" "S460" | S509 S459 S329 | 13 by what she did |
| hermaphrodite brig | S411 S405 S397 | S267 S266 S263 | S192 S189 S193 | S176 S170 S170 | S165 S163 S162 | 15 |
| cutter | S136 S138 S139 | S106 S107 S106 | S107 S106 S106 | S180 S179 S179 | S229 S258 S257 | 15 |
| lugger | S182 S180 S181 | S179 S179 S179 | S180 S180 S179 | S197 S196 S196 | S192 S197 S205 | 15 |
| both schooners | S245 S245 S249 | S168 S168 S171 | S142 S142 S142 | S233 m F | S157 S156 S157 | 13 |
| merchant brig, bilander | · | · | · | · | · | 0 (§3) |
| smack | · or F | | | | | 0 (§3) |
| *the corvette (probe)* | S351 m m | S187 S187 S184 | S232 S235 S238 | m m m | m m m | 7 |

- The brig's two cells in quotation marks were logged "Tacked", but she lay on her old tack at the end (§4).
- The trunk moved under this package: the lateen hulls' list at 7c1773e, then package 127 at f2821c7. The whole sweep was run again on each and is the same to the second.

Shortened, in 20 and 25 kn:

| Ship | 20 kn | 25 kn |
|---|---|---|
| frigate-36 | S267 S259 S261 | S309 S205 S231 |
| razee | S395 S376 S368 | S483 S485 S486 |
| 74 | S229 S186 S255 | S254 S286 S203 |
| 64 | S225 S244 S253 | S246 S278 S208 |
| brig | "S456" "S456" S203 | S467 S467 S438 |
| hermaphrodite brig | S138 S150 S149 | S162 S160 S159 |
| cutter | S101 S99 S100 | S103 S101 S100 |
| lugger | S198 S197 S197 | S221 S219 S218 |
| schooners | S119 S119 S119 | S116 S115 S115 |
| *the corvette (probe)* | S182 S175 S176 | S216 m · |

## 2. A: the moment of the haul

### 2.1 What separates a slack ship

At the moment the trunk calls "mainsail haul" (her head a point off the wind), her way as a share of the way she had at "helm's a-lee":
- every committed square-rigger: 0.48 to 0.58 (the frigate 0.50 to 0.56; the razee, the 74 and the 64 0.48 to 0.54; the brig 0.51 to 0.58);
- the hermaphrodite brig: 0.21 to 0.33;
- the schooners: 0.17 to 0.27, in 20 and 25 kn;
- the corvette: 0.37 at 8 kn, 0.30 to 0.36 at 12, 0.29 to 0.35 at 15, 0.28 to 0.33 at 20 and 0.25 to 0.30 at 25.

Her swing does not separate her: the ships of the line swing 0.40 to 1.13 deg/s at the point, the corvette 0.38 to 0.96.

### 2.2 The rule as built

`TackScript._time_to_haul`: the after yards are hauled with her head a point on the bow while she keeps `HAUL_WAY_FRACTION` of her way at "helm's a-lee"; under that, with the wind ahead (`WIND_AHEAD_RAD`, half a degree); and in any case once she is through the wind. These are Luce 1884's two readings (ch. XXIV, p. 417: the after yards hauled "with the wind ahead or a point on the bow"). The deck can read all of it: her way now and at the helm's a-lee, and where the wind is. It names no ship.

### 2.3 The figure

The lead's three terms:
1. she still stays in 20 and 25 kn;
2. no committed ship loses a tack, or changes one by more than 10 s, that 0.4 leaves alone;
3. her 12 and 15 kn tacks are no slower than the trunk's by more than 10 s.

| Figure | Her plain sail | (1) | (2) | (3) |
|---|---|---|---|---|
| 0.33 | S351 m m / S187 S187 S331 / S232 S235 S341 / **m** S229 S232 / S273 S220 S220: 12 | no: 20 kn from 290 is missed (she hauls at the point there with 0.33 of her way) | yes, but the hermaphrodite brig's 8 kn from 295 is 291 -> 397 s | no |
| 0.35 | S351 m m / S187 S319 S331 / S232 S313 S341 / S228 S229 S232 / S273 S220 S220: 13 | yes | yes: only her own tacks differ from 0.4 | no: 12 kn from 292.5 and 295 are 319 and 331 s against 187 and 184 |
| 0.4 | S369 m m / S312 S319 S331 / S208 S313 S341 / S228 S229 S232 / S273 S220 S220: 13 | yes | the measure | no |

No figure meets all three, so it is 0.4, as the lead ruled for that case. 0.35 would give her three tacks back at the trunk's times, but it does not meet (3), and the lead's ruling sets 0.4 in that case. Her cost: some of her 12 and 15 kn tacks are slower, 208 to 341 s, against 184 to 238 on the trunk.

### 2.4 What moves

- **The committed ships:**
  - the hermaphrodite brig (TuningNotes gives every cell old beside new);
  - both schooners, by one or two seconds: in 20 kn from 290 and in 25 kn from every heading. In those winds they keep 0.17 to 0.27 of their way at the point, so they now wait for the wind ahead. With no square after yards to swing, the haul then only lets fly the staysail sheets abaft the fore mast (A alone: the run with A alone gives the same seconds);
  - every other committed ship's tacks are the same to the second, plain and shortened.
- **The corvette:**
  - plain sail: 7 -> 13 of 15, staying in 20 and 25 kn from every heading (220 to 273 s);
  - shortened: 20 kn 182/175/176 -> 206/206/206; 25 kn from 290, 216 -> 197 s.

### 2.5 The brig in 20 knots, her rudder as she falls back

From 292.5:
- she comes through the wind to 91 degrees off by 85 s;
- the head yards are hauled at 95 s, with 0.3 kn of way;
- she gathers sternway from 120 s (0.5 kn, rising to 2.9 kn astern by 165 s);
- her helm is shifted for the sternway as she gathers it (Luce's "shift the helm"; the helmsman's own rule, `physics/hull.py`), and it is hard over the sternway's way, 35 degrees, from 145 s;
- her sails swing her back regardless, at 1.0 to 3.3 deg/s, through the wind on to her old tack.

So the script does shift the helm, and the helm is not keeping a heading against her sternway. Nothing was built for it (the lead's ruling): what turns her back is her canvas, hauled with no way on her. It is reported, and C says what she did.

## 3. B: the merchant brig, the bilander (and the smack)

Closed, nothing built (the lead's ruling).

- Under the truths' settle (600 s of plain sail and trims every 120 s) their tacks never begin. The tack waits in "ready" behind their own plain sail, which their watch (the merchant brig 6 of 16, the bilander 4 of 9) is still setting. The trims every two minutes then keep them at the braces.
- With the sail set, the ship idle and one trim (the setting 2,150 to 3,650 s, the trim 280 to 475 s), they come round:

| Ship | 8 kn | 12 kn | 15 kn | 20 kn | 25 kn | Stayed |
|---|---|---|---|---|---|---|
| merchant brig | S169 S171 S171 | S462 S373 · | S349 S457 · | S461 S176 · | S329 S325 S293 | 12 of 15 |
| bilander | S308 S313 · | S295 S296 S297 | S309 S310 S310 | S339 S339 S339 | S377 S377 S377 | 14 of 15 |

- The three · of the merchant brig began from 45 to 58 degrees off at 1.0 to 1.5 kn, not settled. Their haul comes at 0.56 to 0.60 of their way, so the haul rule leaves them as they were.
- **The merchant brig in 20 kn from 290** (sail set, idle, one trim). She did miss: "Tacked; braced up on the starboard tack, heading SW by W (232°)." at 461 s on the trunk -> "Missed stays: she came through the wind and fell back on her old tack." at 461 s. Her tack, read every 30 s:
  - 30 s: 9.5 degrees on the starboard bow, 3.1 kn ahead ("Mainsail haul" at 32 s);
  - 60 to 120 s: through the wind, 50 to 90 degrees on the larboard bow, with no way (headway -0.5 to 0.0 kn); "Let go and haul" at 97 s;
  - 150 s: 13.7 degrees on the larboard bow, 2.6 kn astern, helm hard over (35 degrees) for the sternway;
  - 180 s: back through the wind, 11.5 degrees on the starboard bow, 3.2 kn astern;
  - 210 to 460 s: on her old tack, 109 to 144 degrees off the wind, going astern at 0.6 to 2.4 kn and yawing between.
  - The other five cells of the six measured so are unmoved.
- Reported and left: the runner queues an all-hands tack behind the watch's work of setting sail.
- The smack's tacks are refused at those headings ("She is not close-hauled"): her apparent wind there is more than ten degrees from her close-hauled angle. Put full and by first, she lies 48 to 51 degrees off and stays in 8 to 25 kn, in 103 to 176 s.

## 4. C: a failed tack's words

- **Before:** a tack ended by its steady timeout was "Tacked; braced up on <the tack she lies on>", whatever that tack was.
- **Now:** at the timeout's end, on every rig the script serves, with the whole-lateen hulls' own reading left as it was:
  - lying on her old tack more than two points: "Missed stays: she came through the wind and fell back on her old tack.";
  - within two points of the wind: "Missed stays: she lies in irons, her head in the wind.";
  - each with a missed stay's severity (urgent) and recovery ("Up helm; square the yards; ...").
- It is read at the end, so a tack that comes round before the timeout is still a tack.
- In the fleet only the brig's four 20-kn lines change (§1), and the merchant brig's from 290 with her sail set (§3). The in-irons words did not arise, so truth 7-765 holds a cutter there to show them.

## 5. D: the jib she cannot be held without

- **Before:** `shorten sail` took in every jib loaded to `HEAD_SAIL_IN_RATIO` (0.75) of its rating. In the fleet that happens in 25 kn close-hauled. The corvette, with her jib in, gripes to 21 to 25 degrees of helm and lies 22 to 50 degrees off at about a knot.
- **The rule** (`storm.loaded_jibs`, `storm.helm_without`):
  - her helm as she carries it, plus the jib's yaw moment about her centre of lateral resistance, taken over by her rudder at her present way (`physics.hull.rudder_forces`, read and not changed);
  - where that would be more than `HELM_IN_HAND_SHARE` (a quarter) of her rudder's travel, and the jib is under its whole rating, the jib is left set;
  - it is said in the order's reply, and so in the log: "The jib is left on her: she gripes, and her helm will not hold her without it. It is carried at its limit: the next 'shorten sail' takes it in, or 'take in the jib'." (§11, item 2);
  - a kept jib is not a "strained" head sail for the storm staysails clause. On the trunk the storm staysails, set in its place, would take that very jib in, and the spanker with it.
- **When the kept jib passes its rating** (§11, item 2):
  - it is kept once (`storm.KEPT`): the next `shorten sail` takes it in, loaded or not (truth 7-767b);
  - its strain's line names the order that eases it: "Jib straining at the bolt-ropes: take in the jib." (and "stretched drum-tight; it will not stand much more: take in the jib."), said alone; it blows out for certain at 1.8 of its rating;
  - the game's own captain takes it in at its first strain's line in any wind (`_head_sails_straining`), and his own next `shorten sail` takes it in too;
  - a jib the storm canvas will take in or shift (`storm.replaced_by_storm_canvas`) is not kept at all: its own take-in line stands, as before (truth 7-768).
- **The player's own `take in the jib`** is an order of its own, obeyed whatever the rule thinks (truth 7-767).
- **What moves (25 kn, shortened):**
  - the frigate keeps her jib from all three headings, 309/205/231 -> 233/252/265 s;
  - the razee from 295, 486 -> 261 s;
  - the corvette 1 -> 3 of 3 (184, 187, 189 s), lying 65 to 70 degrees off at 6.9 to 8.1 kn where the trunk left her 47 to 50 off at 1.2 to 2.2.

## 6. E: the captain and a straining topgallant yard (built, measured, and taken out)

On the lead's list of 2026-11-27, E is taken out of this hash whole: the method `Captain._topgallant_yards_working` and its call, its truths (then numbered 7-768 and 7-769; the numbers now hold §11's items 3 and 4, never merged before), its slow-tier entry and the lee-shore trial's moved pin. Every captain-run day on today's ships is the trunk's, except by A, C and D. E is kept at 28375be, in this branch's history, and on a local branch.

**Why he fills away sooner under E, in the lee-shore trial.**
- With the topgallants in at 1,560 s (27 kn, both yards working), she keeps her station by the wind under less sail aloft.
- Three times in the next hour and a half she comes up into the wind and is caught aback with no way (3,720, 4,800 and 5,880 s). Each time she is boxed off, and with the spanker in and the storm staysails she keeps station at 5.6 to 5.9 kn where the trunk's makes 7.5 to 8.7.
- So she is some four miles further to leeward, nearer Ushant, when she heaves to at 9,720 s, and the lee sector holds land (her reckoning reads it at 10 to 12 miles, where the trunk's reads none).
- Drifting hove to, that closes to 6.0 miles, the lee-shore line, at 26,760 s. The lee-shore exit then fills her away into 42 kn, and she comes within 2.4 miles of the land by 28,200 s.

The measures of E as built, kept for the rule when it is carried with its cause:

- **What the code does:**
  - `shorten sail` takes in the loftiest first already: studding sails, square sail, royals, flying jib, topgallants, then the topsails' reef; the jibs by their ratings.
  - A watch too small takes the sails in turn: the frigate's three topgallants come in together, about 200 s after the order; the corvette's one by one, 213 to 300 s.
  - The captain begins by the glass and the wind (the wind risen by `worsening_wind_kn` within the hour, over `shorten_sail_kn` less `worsening_sooner_kn`). In this probe's wind that fired at 1,440 to 3,120 s across seeds 1 to 8.
- **As built (now taken out):** `Captain._topgallant_yards_working`. A strain warning on a topgallant yard, in a wind over that same line, is answered at once by "take in the topgallants" ("By the captain, ...: taking in the topgallants (the topgallant yards working)."). It is given once, until the wind falls under the line again, and never under it. It is every captain's, by his own book's two figures (24 kn in every committed book), as `_head_sails_straining` is every captain's. No book of a role differs, so no role is left out.
- **The probe:** the wind rising from 20 to 35 kn over the hour from 04:00 and held, gusts and shifts 0.3, a low coming in; 40 miles south of Falmouth, bound for it, the wind abeam, plain sail, no order given; seeds 1 to 8. Carried away or blown out:

| Ship | Trunk | This package |
|---|---|---|
| *the corvette* | seed 1: fore topgallant yard, 3,228 s | none |
| brig | seed 1: fore topgallant yard, 3,484 s; seed 3: fore topgallant yard, 3,019 s | seed 3 as before (below) |
| razee | seed 1: fore topmast staysail, 4,872 s | none |
| 74, 64 | seed 1: fore topmast staysail, 3,634 s | the same (not a topgallant's) |
| frigate | none | none |

- **The brig at seed 3:** the answer came at 1,495 s, but her watch still had not got her fore topgallant in when its yard went at 3,019 s. It is her hands, not the answer.
- **The topgallants come in sooner** for most ships in seeds 1, 2, 3, 4, 6 and 8, by 60 to 940 s. The captain's first three states and their times are the same in every run measured.
- **The captain's trials, under E.** Only the station off Ushant with the land under her lee moved:
  - her topgallant yards are reported working in 27 kn at 1,502 s, and the captain takes the topgallants in at 1,560 s;
  - her day runs otherwise from there: filled away from her first a-try at 26,760 s (30,780 before), no second a-try (41,880 before), beating to the station at 67,200 s;
  - never aground, and nothing lost;
  - **taken aback 32 times in the day (9 before), and five missed stays (one)**, beating the gale's tail off the land;
  - 1,940 lines (1,561 before).
  - Put to the lead: the answer is right for the yards, but the day after it is a worse one off a lee shore.

## 7. Pins

- **Before the build, each rule alone:** the 46 test files that tack or shorten, plus the captain trials' file, ran in the fast tier on the trunk and under each rule. Every run had 5,485 tests.
  - The trunk: all pass.
  - The haul by her way: all pass.
  - The jib: all pass.
  - The captain: all pass.
  - The words: one moves (TuningNotes), and one tide-gauge timing test failed in that run, timing alone.
- **The build:** without E, every captain trial's pin is the trunk's (f2821c7), unmoved. The fast tier whole and the slow tier of what it touched: the build report gives the counts.

## 8. For the lead, measured and not built

**The brig's and the merchant brig's fall-backs in 20 kn** (§2.5, §3): they come through the wind with no way, gather sternway and are turned back by their canvas, their helm shifted for it. It is their canvas and not their helm, and C says what they did. Not mended.

**The captain's `lie a-try` behind the shortening's reefs** (package 126's builder's finding):
- **What the code does:** on entering "hove to for weather" the captain gives `shorten sail` and then `lie a-try` (`Captain._on_enter`). The runner starts a waiting evolution only when no earlier one holds a part of its (`_start_waiting`). `lie a-try` hands every square sail but the a-try topsail, so it holds the sails the shortening is still reefing, and waits for every reef given before it. In the corvette's seed 7 it is given at 2,100 s and begins at 4,826 s; "'Reef the foresail' will follow 'lie a-try'" in the meantime.
- **Candidates, not measured:**
  - the captain gives `lie a-try` alone on entering, with only the a-try topsail's reef before it;
  - or `lie a-try` belays the waiting work on the sails it will hand.
- Either moves every hove-to of every captain's ship in a gale, and the gale trials' pins.

## 9. Differences a player or a seat is served

1. "Mainsail haul" called later, with the wind ahead, for a ship that comes slack into stays, and her tacks' times (§2.4, §10):
   - the hermaphrodite brig;
   - the two schooners by one or two seconds.
2. "Missed stays: she came through the wind and fell back on her old tack." and "Missed stays: she lies in irons, her head in the wind.", urgent, where "Tacked; braced up on ..." was said of a ship that had not come round (§4). After them come the missed stay's own lines ("Squared the yards; she fell off on ..."), and never "filled away". In the measured fleet: the brig's four 20-kn cases, and the merchant brig's from 290 with her sail set.
3. "The jib is left on her: she gripes, and her helm will not hold her without it. It is carried at its limit: the next 'shorten sail' takes it in, or 'take in the jib'." in the reply to `shorten sail`, and the jib left set, where a jib was taken in by its rating and her helm needs it (§5); never of a jib the storm canvas takes in or shifts. The storm staysails are no longer set in its place on that account. A kept jib is not taken in, so no countermand or belay is said of it (package 127's rule).
4. A kept jib's strain line ends ": take in the jib." and is said alone (§11, item 2); the captain's "taking in the jib (straining at the bolt-ropes)" for it in any wind.

Nothing else is served differently. Of the reader's 54 passages, 12 beats and the lee-shore trial, the passages and the trial are identical line for line and hash for hash, and the four beats that differ are A's and C's (§11).

## 10. Every cell old beside new

The trunk at f2821c7 is old; this hash is new. The measure covers 216 cells:
- the ten committed ships that tack under the truths' settle: 150 plain and 60 shortened;
- the merchant brig and the bilander with their sail set, in 20 kn: 6.

38 cells change, and no tack is lost by what she did. The lead's reader found no tack lost in 408 steady cells; that table is theirs.

| Ship | Case | Old | New | Rule |
|---|---|---|---|---|
| brig | plain 20 kn, 292.5 / 295 | "Tacked" 459 / 460 s (lying 149 / 135 degrees off on her old tack) | missed stays, at the same seconds | C |
| brig | shortened 20 kn, 290 / 292.5 | "Tacked" 456 / 456 s (111 / 110 off, old tack) | missed stays | C |
| merchant brig | sail set, 20 kn, 290 | "Tacked" 461 s (130 off, old tack) | missed stays | C |
| frigate-36 | shortened 25 kn, 290 / 292.5 / 295 | S309 / S205 / S231 | S233 / S252 / S265, her jib kept | D |
| razee | shortened 25 kn, 295 | S486 (NE by E, 52 deg off at the end) | S261 (ENE), her jib kept | D |
| hermaphrodite brig | plain 8 kn | S411 S405 S397 | S300 S296 S291 | A |
| hermaphrodite brig | plain 12 kn | S267 S266 S263 | S198 S198 S196 | A |
| hermaphrodite brig | plain 15 kn | S192 S189 S193 | S194 S186 S184 | A |
| hermaphrodite brig | plain 20 kn | S176 S170 S170 | S186 S184 S183 | A |
| hermaphrodite brig | plain 25 kn | S165 S163 S162 | S171 S169 S167 | A |
| hermaphrodite brig | shortened 20 kn | S138 S150 S149 | S186 S185 S183 | A |
| hermaphrodite brig | shortened 25 kn | S162 S160 S159 | S167 S166 S164 | A |
| both schooners | plain 20 kn, 290 | S233 | S235 | A |
| both schooners | plain 25 kn | S157 S156 S157 | S156 S155 S156 | A |

## 11. The lead's second list of 2026-11-27: the read of a8b2c3e

The lead's reader read a8b2c3e whole on the trunk with the default gusts, and found it sound and held it for one pass more. This section answers that list. The reader's harness (the scratch branch the lead named, `lead-backup/gate125/`) is used throughout, so the cells are the gate's: `tackmx.py` (1,512 cells a tree), `dprobe.py` (with seeds 7 and 11), and `run.py` with `cases125.py`. Old is the trunk at f09fe283. New is this hash.

**The tack matrix, old beside new.** 90 of 1,512 cells change, and no tack is lost: 787 come round on this hash against 780 on the trunk, with 7 gained. By rule (the reader's `tmxrule.py`):
- A: 65 cells. The hermaphrodite brig's 51 and the schooners' 2 are declared. Twelve are not, and they are item 1's below.
- C: 12 cells (the brig 8, the merchant brig 4). Every one is a "Tacked" said lying on her old tack on the trunk, now "Missed stays".
- D: 13 cells, all shortened. The frigate 25 kn seed 11 (3), declared since a8b2c3e for 25 kn; and the brig 30 kn seed 7 (4), the hermaphrodite brig 30 kn seed 11 (3) and the razee 30 kn seed 11 (3), declared here (item 2's table).

The cells as they stand on this hash against a8b2c3e: 13 differ, all D's above, and only in the reply's added sentence. Every end, second and line after it is the same.

### Item 1: A in a gust

**The twelve cells** (old, the trunk's haul at the point, beside new):

| Ship | Cell | Old | New |
|---|---|---|---|
| brig | 30 kn s11 292.5 plain | S275 | S281 |
| frigate-36 | 30 kn s11 290 short | S200 | S224 |
| merchant brig | 30 kn s7 295 plain | S538 | S531 |
| razee | 30 kn s11 290 plain | S349 | S302 |
| razee | 30 kn s7 full and by, short | S278 | S265 |
| 74 | 25 kn s11 295 short | S237 | S312 |
| 74 | 30 kn s7 full and by, plain | S250 | S264 |
| 74 | 30 kn s7 full and by, short | S288 | S549, 49 deg off at the end |
| 64 | 25 kn s11 295 short | S242 | S308 |
| 64 | 30 kn s11 292.5 short | S227 | S285 |
| 64 | 30 kn s11 295 short | S299 | S294 |
| 64 | 30 kn s7 full and by, plain | missed, 83 s | S255 |

**No reading tells them from the slack ship, and so A is left as built for the lead to rule.** Measured at the first tick her head is within a point of the wind (the trunk's haul):

| | Her way / her way at helm's a-lee | Mean way since / at helm's a-lee | Swing toward the wind (deg/s) | Apparent wind / at helm's a-lee |
|---|---|---|---|---|
| the corvette, 8 to 25 kn, plain (A made for her) | 0.25 to 0.37 | 0.63 to 0.69 | 0.38 to 0.96 | (no gusts) |
| the twelve cells | 0.15 to 0.40 | 0.62 to 0.77 | 0.52 to 1.37 | 0.79 to 1.07 |

- These cells are slack by the way, not checked for an instant. Her way falls smoothly from helm's a-lee, and the apparent wind at the point is within a few per cent of what it was (the 74 full and by, shortened: 9.0 kn at helm's a-lee to 1.37 at the point over 66 s, the apparent wind 28 to 31 kn throughout).
- What separates them comes after the haul, and the deck cannot read it before. The corvette in 20 kn, hauled at the point under the trunk's rule: her swing falls from 0.81 to -0.22 deg/s within six seconds, and she falls back and misses. The 74, hauled at the point: her swing holds at 0.33 to 0.39, she gathers sternway with her helm a-lee, and she goes through. It is the rig's answer to the swung after yards, not her way.
- **Tried and not taken:** the haul when she hangs (the way gone for `hang_after_s`) as a third reading. It gives back the 74's full-and-by cells (288 and 252 s, against the trunk's 288 and 250), but leaves the 74 and the 64 from 295 in 25 kn at 313 to 315 s, against 237 to 242. It costs the corvette two of her 25-kn tacks (11 of 15, against 13).
- Lower fractions of her way lose the corvette's 20-kn tacks (§2.3). The swing rate and the mean way overlap, as in the table.
- **For the lead:** A as built gains the corvette 6 tacks of 15 and the hermaphrodite brig a minute or two in light airs. It costs the 74 and the 64 one to four minutes in five cells and the frigate 24 s in one, and gives back the 64's full-and-by miss in 30 kn.

### Item 2: where D keeps a jib, and the jib kept at its limit

**The whole table** (`dprobe.py`, seeds 7 and 11, every ship with a jib, close-hauled 292.5 and abeam 270, 20 to 40 kn: 260 cells). It is kept and said in 7 cells, all close-hauled. Fifteen minutes on, old beside new:

| Ship | Cell | Jib at the order | Helm wanted without it | Old: off the wind, way, helm | New |
|---|---|---|---|---|---|
| brig | 30 kn s7 | 0.81 | 11.0 deg | 50 off, 2.2 kn, -10.6 deg | 68 off, 9.4 kn, 4.4 deg; the jib to 1.18 |
| frigate-36 | 25 kn s11 | 0.85 | 11.7 deg | 70 off, 8.2 kn, 7.8 deg | 70 off, 8.7 kn, 1.7 deg |
| hermaphrodite brig | 30 kn s11 | 0.86 | 17.4 deg | 45 off, 2.0 kn, -14.3 deg | 66 off, 11.2 kn, 3.7 deg |
| hermaphrodite brig | 35 kn s7 | 0.83 | 15.3 deg | 47 off, 2.1 kn, -13.6 deg | 70 off, 11.4 kn, 3.1 deg |
| both schooners | 35 kn s11 | 0.77 | 25.8 deg | 69 off, 9.1 kn, 16.7 deg | 71 off, 9.4 kn, 10.8 deg |
| razee | 30 kn s11 | 0.93 | (no way: her rudder holds nothing) | 41 off, 1.1 kn | 44 off, 1.8 kn |

- Not kept with the reader's gusts at seed 7: the frigate and the razee in 25 kn. They are kept in the truths' settle without gusts (truth 7-762), and at seed 11 for the frigate.
- Nothing abeam is kept. The reader's schooners, merchant brig and 74 abeam in 35 and 40 kn now keep nothing, because the storm canvas takes the jib in or shifts it (item 3). Their replies and lines are the trunk's.
- **In the tack matrix:**
  - the brig 30 kn s7 shortened: the trunk's tacks refused for want of way, or 368 s, are 186 to 288 s;
  - the hermaphrodite brig 30 kn s11 shortened: the trunk's refused for want of way; now accepted, and missed in 35 to 36 s ("she lost her way before her head came up to the wind");
  - the razee 30 kn s11 shortened: from 290 the trunk's miss is a miss; from 292.5 and 295 the trunk's misses in 27 to 35 s are refused for want of way.
- **The jib at its limit, built:**
  - the reply says so, and says what takes it in;
  - the next `shorten sail` takes it in (`storm.KEPT`, forgotten once it is in);
  - its strain line names "take in the jib";
  - the captain takes it in at its first strain line, in any wind. Before, only a head sail "straining at the bolt-ropes" over `shorten_sail_kn` was taken in, and the dire line, "stretched drum-tight", never.
- **An hour in rising wind under the game's own captain** (west of the Scillies, bound north, the wind from the north rising 12 kn in the hour, the default gusts; the cells where `shorten sail` keeps the jib there; `tests/test_captains.py`, slow tier). Each is kept at the order and taken in, never blown out:
  - brig 30 kn s11: taken in at 495 s by his own `shorten sail` (at most 0.96 of its rating);
  - brig 35 kn s7: its strain line at 310 s, his "taking in the jib" at 361 s, hauled down at 436 s (at most 1.04);
  - hermaphrodite brig 30 kn s11: taken in at 226 s by his own `shorten sail` (0.85);
  - razee 28 kn s11: its strain line at 224 s, his order at 241 s waiting behind the jib's trim for hands, hauled down at 643 s (at most 1.35).
- The reader's 54 passages, 12 beats and the lee-shore trial are run again on this hash. The passages and the trial are identical in every line and hash; the four beats that differ are A's and C's, as the reader found.

### Item 3: the false line in 40 knots

- `shorten sail` now reads its lines and the jibs it leaves on her together (`storm.shortening_plan`). A jib the storm canvas will take in or shift as it is set (`storm.replaced_by_storm_canvas`: the fore-and-after's jib shifted for her storm jib, and the head sails the foremost storm staysail replaces) is not kept. Its own take-in line stands, as before.
- No sail the order takes in or shifts is said to be left on her.
- The schooner abeam in 40 kn is truth 7-768.

### Item 4: the two surviving mutants

- `HELM_IN_HAND_SHARE = 0` is now killed by truth 7-769, the bilander close-hauled in 30 kn. Her jib is at 0.89 of its rating and she would want 4.4 degrees without it, so it is taken in, the order waiting for hands.
- The in-irons bound moved to one point is now killed by `tests/test_evolutions.py::test_a_tack_ended_within_two_points_of_the_wind_either_side_is_in_irons`: the stub frigate held 17 degrees off, either side.
- Eight mutants of this pass's mends were run against their pins, and all eight are killed: the share, the storm canvas's exclusion, kept once, the strain line's order, the forgetting, the limit's words, the captain's any-wind answer, and the bound.

### Item 5

The comment at the head of package 125's truths names no captain's rule now.

### Item 6: the cutter's and the schooners' "Tacked" after a box-off (answered, not mended)

- That tack's line is true. Under `keep her full and by` the cutter in 20 kn pinches up, is taken aback at 58 s, and the helm boxes her off at 231 s. Through the wind aft she is worn round on to the larboard tack.
- `tack ship` then finds her on the larboard tack: heading 070, the wind on her larboard bow, at "helm's a-lee". She comes through the wind at 49 s and ends on the starboard tack. The matrix's "old tack" is the tack she was settled on, not the one she was on when the order came.
- **The false line is the box-off's,** "Boxed her off; braced sharp up on the starboard tack, full and by.", said while she lies on the larboard tack. `BoxOffScript.words` names the tack she was on when the box-off began (`self.sign`), and a box-off that wears her round ends on the other. It is not C's few lines, so it is carried to the lead and not mended.

## 12. The lead's ruling on rule A (2026-11-27): the moment of the haul a habit of the ship

**The ruling.** At the point a slack ship and a gust-checked one cannot be told apart by her way, her swing or the wind (§11, item 1); they part only after the haul. That is a thing of the ship, her mass against her after yards, which her people know of her. So the second moment is said in her file.

**Built.**
- `ship.slack_in_stays` in the ship file's `ship:` section, read through the schema (`ShipSpec.slack_in_stays`): absent or false by default; true or false only, anything else refused in words ("'ship.slack_in_stays' is 'yes', which is not true or false."). Left out of the pickle while false, so a checkpoint of any of today's ships is as before. Its comment names the phrase (Falconer's Marine Dictionary, "Slack": slow in going about) and Luce 1884 p. 417.
- `TackScript._time_to_haul`: a ship without the habit is hauled at the point, whatever her way, as on the trunk. A ship with it is hauled as §2.2 built: at the point while she keeps two fifths of her way, else with the wind ahead, and in any case once through the wind.
- The reading `the ship` (`readings.ship_words`) says it in one line after her class, where the habit is set: "She is slack in stays: when her way is gone in going about, the after yards are hauled with the wind ahead, not a point on the bow." No reading said anything of a ship's handling before; this is the one that tells of the ship.
- No ship file and not `tools/gen_ships.py`: no ship of today's eighteen sets it. The ships' session sets it for the corvette through the generator when she joins.

**Today's eighteen are unmoved by A** (the reader's `tackmx.py`, 1,512 cells with the default gusts; old is the trunk at f09fe283; the reader's `tmxrule.py`): 25 cells differ from the trunk, and none by A.
- C: 12 (the brig 8, the merchant brig 4), each a trunk "Tacked" lying on her old tack, now "Missed stays", as in §11.
- D: 13, all shortened, as in §11 (the frigate 25 kn seed 11, 3; the brig 30 kn seed 7, 4; the hermaphrodite brig 30 kn seed 11, 3; the razee 30 kn seed 11, 3).
- A: 0. The 65 cells A moved on bd4fa9e4 (the hermaphrodite brig's 51, the schooners' 2, item 1's 12) are the trunk's again.
- Made (round at the end and at +300 s, the reader's measure): 786 of 1,512 against the trunk's 780, no tack lost. The six gained are D's: the brig 30 kn seed 7 shortened from 292.5, 295 and full and by (refused on the trunk), and the frigate 25 kn seed 11 shortened from every heading (round at +300 s now). The razee's and the hermaphrodite brig's D cells change between refusals and misses.

**Served:** the reader's `seat.py` on bd4fa9e4 beside this hash, every ship at the officer's station: 9,168 served items and 1,350 orders' answers, none differing.

**The truths of A, moved and new.**
- 7-763 now reads both moments and a ship without the habit: the frigate in 15 kn hauls at the point (0.53 of her way); the hermaphrodite brig as her file has her (0.16) hauls at the point too, her head 8 to 11.25 degrees off; with the habit set on her in memory she hauls with the wind ahead. A mutant that makes every ship slack fails the second case, and one that makes none fails the third; both are killed by this fast test.
- 7-763b: the line in `the ship` with the habit set, none without.
- `tests/test_ship_loader.py`: the key's default, its refusal of 'yes', 1 and null, the pickle, and no ship of the eighteen setting it.
- The hermaphrodite brig's rows of the fleet tables (7-761 and 7-762) are measured on the trunk's haul again (TuningNotes gives every band old beside new). The schooners' rows stand: their seconds are within one or two of the trunk's.

**What the habit costs and gains, by this package's measure, for whoever sets it for a ship:**
- The light corvette, set slack: plain sail 7 to 13 of 15 tacks, staying in 20 and 25 kn from every heading (220 to 273 s); some of her 12 and 15 kn tacks are slower, 208 to 341 s against 184 to 238 on the trunk (§2.3, §2.4).
- The hermaphrodite brig, had she been set slack: plain 8 kn 411/405/397 to 300/296/291 s and 12 kn 267/266/263 to 198/198/196, quicker; shortened 20 kn 138/150/149 to 186/185/183 s, slower.
- Had it been every ship's habit (the rule as built on bd4fa9e4, in gusts): the 74 and the 64 a minute to four slower in five cells (the 74 25 kn s11 from 295 shortened, 237 to 312 s; the 64 25 kn s11 from 295 shortened, 242 to 308 s; the 64 30 kn s11 from 292.5 shortened, 227 to 285 s; the 74 30 kn s7 full and by, 250 to 264 s plain and 288 to 549 s shortened), the frigate 24 s slower in one (30 kn s11 from 290 shortened, 200 to 224 s), and the 64's missed tack in 30 kn s7 full and by, plain, made in 255 s.
- A ship whose after yards swing her through when hauled at the point (the 74, the 64) loses by it; a light one whose swung yards turn her back (the corvette) gains.

## 13. The corvette joins (trunk 939de7d6): what D does for her

The corvette (`corvette-20`, the Diana) is the ship D was first measured for: a light ship with the least rudder of any. Merged with her in, three of her 59 tests fail, all of them truth E's "she gripes without her jib" shortened in 25 kn, at all three headings. The game's own `shorten sail` now leaves her jib on her there. Nothing else of hers moves: not by A (her `slack_in_stays` is unset) and not by C.

| | trunk 939de7d6 | this package |
|---|---|---|
| plain sail, 8 to 25 kn | 7 of 15 | 7 of 15, the same seconds |
| shortened, 20 kn | 3 of 3, jib kept, 186 to 193 s | the same |
| shortened, 25 kn | jib taken in; stays from 290 alone (235 s); gripes 30 to 62 off under 2.5 kn from 292.5 and 295 | jib left on her at 0.75 of its rating; 65 to 70 off at 6.9 to 8.1 kn with 0.4 to 2 degrees of helm; stays 3 of 3, 203 to 208 s |
| 25 kn, the jib then taken in by order | (as the row above) | gripes: stays from 290 (233 s), misses from 292.5 (62 off, 4.9 kn), refused from 295 (39 off, 1.0 kn) |
| 25 kn, `set the jib` after | obeyed; 3 of 3, 184 to 189 s, jib 0.68 to 0.78 | obeyed; 3 of 3, 184 to 187 s, jib 0.67 to 0.70 |

The pins moved are in `docs/dev/TuningNotes.md` ("the corvette's pins moved by D"), old beside new. Her rows are added to truths 7-761 and 7-762. Her ship file, her generator, her design note and her report are untouched. When the ships' session sets her `slack_in_stays`, A acts on her plain-sail tacks in 20 and 25 kn (§12's trade). D acts on her shortened sail whatever A does.

## 14. The reader's read of b5ddfa6a (2026-11-28)

**The finding, and the lead's ruling.** On a player's ship nothing took a kept jib in. It stood all hour at up to 1.73 of its rating, and the brig's in 35 kn at seed 7 blew out. The ruling: the order that left it on her sees it through, as the storm canvas is seen through.

**Built.** On a ship whose captain does not command, the hands take the kept jib in at its strain's first dire line: "Taking in the jib before it goes: she will gripe without it." Its lesser lines are the player's warning, with the order named.

Taken in at the second line instead, the jib came in during the matrix's long shortening, and the corvette lost her three tacks in 30 kn. At the dire line no tack is lost.

| an hour in rising wind, a player's ship (62 cells) | trunk e3d50aac | b5ddfa6a | now |
|---|---|---|---|
| jibs blown out | 11 | 12 | 11 |
| kept jibs blown out | 0 | 1 | 0 |
| kept jibs taken in by the hands | (none kept) | 0 of 8 | 4 of 8; the other 4 under the dire line all hour |

**The tack matrix.**
- Against b5ddfa6a: the razee's two shortened cells in 30 kn at seed 11 (D's), none lost.
- Against the trunk: 28 cells, C 16 and D 12, A 0; 838 made against 829.

**The two-fifths figure** is pinned for a ship slack in stays (truth 7-763c; the reader's M02 now dies).

**The corvette's gripe truth** says what is measured (TuningNotes).

**Truth 7-779b, the spar carried away on passage.** Rule D's kept jib moved two cell-seeds of the 140:
- the brig in 20-38 kn at seed 3 is now no worse than the trunk's captain (brought to 178 s before him, 7.61 nm against 2.70, 17 minutes astern against 44), so she leaves `PASSAGE_DECLARED`;
- the frigate's seed 3 stays outside with new figures.

The truth's file was not in my slow tier, so this was not seen; it is now. The figures are in TuningNotes.
