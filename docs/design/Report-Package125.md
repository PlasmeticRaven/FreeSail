# Package 125: the moment of the haul (report)

The brief: `docs/dev/briefs/Brief-Package125.md`. The lead's rulings on the ground report (2026-11-24): A by her way, the figure settled by the measure below; B closed and nothing built; C as given; D as given; E built, every captain's. The pins moved are in `docs/dev/TuningNotes.md` under "Package 125".

Every measure is at seed 7, made with the truths' own helpers (`close_hauled_on_starboard`: the wind from the north, no gusts, plain sail set and braced up). Tacks are from 290, 292.5 and 295 degrees, in 8, 12, 15, 20 and 25 knots. "Shortened" means the game's own `shorten sail` run to its end, then sixty seconds, then the helm put down. **S**n means stayed in n seconds; **m** means missed stays; **F** means refused; **·** means no end in 900 s.

The light corvette of the ships' package (her file on `claude/pkg-90-diana`) was used as a probe only, in a scratch copy. Nothing of hers is committed; her figures here are what her builder will find.

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
- The trunk moved under this package (the lateen hulls' list, at 7c1773e). The whole sweep was run again on it and is the same to the second.

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

- **The committed ships:** the hermaphrodite brig alone (TuningNotes gives every cell old beside new). Every other committed ship's tacks are the same to the second, plain and shortened.
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
- Reported and left: the runner queues an all-hands tack behind the watch's work of setting sail.
- The smack's tacks are refused at those headings ("She is not close-hauled"): her apparent wind there is more than ten degrees from her close-hauled angle. Put full and by first, she lies 48 to 51 degrees off and stays in 8 to 25 kn, in 103 to 176 s.

## 4. C: a failed tack's words

- **Before:** a tack ended by its steady timeout was "Tacked; braced up on <the tack she lies on>", whatever that tack was.
- **Now:** at the timeout's end, on every rig the script serves, with the whole-lateen hulls' own reading left as it was:
  - lying on her old tack more than two points: "Missed stays: she came through the wind and fell back on her old tack.";
  - within two points of the wind: "Missed stays: she lies in irons, her head in the wind.";
  - each with a missed stay's severity (urgent) and recovery ("Up helm; square the yards; ...").
- It is read at the end, so a tack that comes round before the timeout is still a tack.
- In the fleet only the brig's four 20-kn lines change (§1). The in-irons words did not arise, so truth 7-765 holds a cutter there to show them.

## 5. D: the jib she cannot be held without

- **Before:** `shorten sail` took in every jib loaded to `HEAD_SAIL_IN_RATIO` (0.75) of its rating. In the fleet that happens in 25 kn close-hauled. The corvette, with her jib in, gripes to 21 to 25 degrees of helm and lies 22 to 50 degrees off at about a knot.
- **The rule** (`storm.loaded_jibs`, `storm.helm_without`):
  - her helm as she carries it, plus the jib's yaw moment about her centre of lateral resistance, taken over by her rudder at her present way (`physics.hull.rudder_forces`, read and not changed);
  - where that would be more than `HELM_IN_HAND_SHARE` (a quarter) of her rudder's travel, and the jib is under its whole rating, the jib is left set;
  - it is said in the order's reply, and so in the log: "The jib is left on her: she gripes, and her helm will not hold her without it.";
  - a kept jib is not a "strained" head sail for the storm staysails clause. On the trunk the storm staysails, set in its place, would take that very jib in, and the spanker with it.
- **When the kept jib passes its rating:**
  - the strain model warns of it ("straining at the bolt-ropes"), and it blows out for certain at 1.8 of its rating;
  - `shorten sail` given again takes it in (truth 7-767);
  - the game's own captain takes it in over `shorten_sail_kn` (`_head_sails_straining`, as before).
- **The player's own `take in the jib`** is an order of its own, obeyed whatever the rule thinks (truth 7-767).
- **What moves (25 kn, shortened):**
  - the frigate keeps her jib from all three headings, 309/205/231 -> 233/252/265 s;
  - the razee from 295, 486 -> 261 s;
  - the corvette 1 -> 3 of 3 (184, 187, 189 s), lying 65 to 70 degrees off at 6.9 to 8.1 kn where the trunk left her 47 to 50 off at 1.2 to 2.2.

## 6. E: the captain and a straining topgallant yard

- **What the code does:**
  - `shorten sail` takes in the loftiest first already: studding sails, square sail, royals, flying jib, topgallants, then the topsails' reef; the jibs by their ratings.
  - A watch too small takes the sails in turn: the frigate's three topgallants come in together, about 200 s after the order; the corvette's one by one, 213 to 300 s.
  - The captain begins by the glass and the wind (the wind risen by `worsening_wind_kn` within the hour, over `shorten_sail_kn` less `worsening_sooner_kn`). In this probe's wind that fired at 1,440 to 3,120 s across seeds 1 to 8.
- **Built:** `Captain._topgallant_yards_working`. A strain warning on a topgallant yard, in a wind over that same line, is answered at once by "take in the topgallants" ("By the captain, ...: taking in the topgallants (the topgallant yards working)."). It is given once, until the wind falls under the line again, and never under it. It is every captain's, by his own book's two figures (24 kn in every committed book), as `_head_sails_straining` is every captain's. No book of a role differs, so no role is left out.
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

## 7. Pins

- **Before the build, each rule alone:** the 46 test files that tack or shorten, plus the captain trials' file, ran in the fast tier on the trunk and under each rule. Every run had 5,485 tests.
  - The trunk: all pass.
  - The haul by her way: all pass.
  - The jib: all pass.
  - The captain: all pass.
  - The words: one moves (TuningNotes), and one tide-gauge timing test failed in that run, timing alone.
- **The build:** the fast tier whole, and the slow tier of what it touched and of the captain trials (the build report gives the counts).

## 8. For the lead, measured and not built

**The captain's `lie a-try` behind the shortening's reefs** (package 126's builder's finding):
- **What the code does:** on entering "hove to for weather" the captain gives `shorten sail` and then `lie a-try` (`Captain._on_enter`). The runner starts a waiting evolution only when no earlier one holds a part of its (`_start_waiting`). `lie a-try` hands every square sail but the a-try topsail, so it holds the sails the shortening is still reefing, and waits for every reef given before it. In the corvette's seed 7 it is given at 2,100 s and begins at 4,826 s; "'Reef the foresail' will follow 'lie a-try'" in the meantime.
- **Candidates, not measured:**
  - the captain gives `lie a-try` alone on entering, with only the a-try topsail's reef before it;
  - or `lie a-try` belays the waiting work on the sails it will hand.
- Either moves every hove-to of every captain's ship in a gale, and the gale trials' pins.

## 9. Differences a player or a seat is served

1. "Mainsail haul" called later, with the wind ahead, for a ship that comes slack into stays (of the committed ships, the hermaphrodite brig), and her tacks' times (§2.4).
2. "Missed stays: she came through the wind and fell back on her old tack." and "Missed stays: she lies in irons, her head in the wind.", urgent, where "Tacked; braced up on ..." was said of a ship that had not come round (§4). After them, the missed stay's own lines ("Squared the yards; she fell off on ...").
3. "The jib is left on her: she gripes, and her helm will not hold her without it." in the reply to `shorten sail`, and the jib left set, where a jib was taken in by its rating and her helm needs it (§5). The storm staysails are no longer set in its place on that account.
4. "By the captain, ...: taking in the topgallants (the topgallant yards working)." for every ship the game's captain sails, in a wind over his worsening line, with what follows from it: the topgallants in sooner, and the shortening's own "take in the topgallants" then finding them in (§6).

Nothing else is served differently. The fleet's sweeps (§1, §2.4) are the same to the second for every committed ship but the hermaphrodite brig; the fast tier of every file that tacks or shortens passes but for the one moved pin.
