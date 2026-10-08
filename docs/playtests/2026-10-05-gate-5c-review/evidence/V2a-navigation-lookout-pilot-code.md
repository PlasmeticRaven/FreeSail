# V2a: navigation close to land, read in the code

Reader: code reader V2a. Tree: `D:\Projects\FreeSail\FreeSail-gate-m5c\` (all `path:line`
references are to m5c). **m5c-b changes none of the modules read here** (`m5c-b.diff` touches
`agents/*`, `core/replay.py`, `core/world.py` for the wind-shift line, `physics/hull.py`,
`physics/integrate.py` for the aback rule, tests and docs; nothing in `world/reckoning.py`,
`sights.py`, `lookout.py`, `chart.py`, `ports.py`, `ships.py`, `orders/navigation.py`,
`api/readings.py`), so every finding below holds for both trees.

Method. I read whole: `world/reckoning.py`, `sights.py`, `lookout.py`, `chart.py`, `geo.py`,
`ground.py`, `ships.py`, `orders/navigation.py`, `orders/people.py`; and the relevant parts of
`world/ports.py`, `core/world.py`, `api/readings.py`, `evolutions/scripts.py`,
`evolutions/runner.py`, `physics/anchor.py`, `physics/integrate.py`, `standing/runtime.py`,
`agents/tools.py`, the port files, the features file, the spec §11 to §18 and §23 to §25, the
navigation study §3, primer 10, 12, 14, 15 and `docs/dev/TuningNotes.md`. I ran nothing of the
game or the suite. Three throwaway read-only Python queries against the chart tiles and one
piece of plain arithmetic gave the numbers marked [QUERY] and [ARITH]. The logs never state the
truth's position; where I say where she "really" was, it is worked from the lookout's true
bearings, and I say so. Where another reader's report (H5, P2, M1, which had the saves' data)
bears a number that settles one of my inferences, I name it as theirs.

---

## 0. What the lead should know first

Six mechanisms account for nearly everything in this area. Four of them are small.

1. **The lookout's distance is frozen until the *observing* ship has run a mile**
   (`lookout.py:362-386`, `ESTIMATE_HOLD_NM = 1.0`). It was written so that a calm does not
   re-draw a headland's distance. It is applied unchanged to land a few cables off and to
   *moving vessels*. Within a mile and a half of anything, "distant a mile" can stand all the
   way to the beach. This one rule is behind: "Penlee Point ... a mile" 27 seconds before the
   Harpy struck; "the Isle of Bas ... two miles" for 44 minutes off Roscoff; the frigate at
   "eight cables" for hours; the pilot boat "eight cables"; "Mr Moal left while his boat was a
   mile away"; the Black Rock "two cables" frozen.
2. **That frozen distance is written into the reckoning at every bearing taken**, as a second
   line of position trusted to 15 per cent (`reckoning.py:1395-1400`). So "fixes from
   bearings" pull the account onto the right bearing and then pin it at the *stale* distance,
   and repeated bearings (a standing order every five or ten minutes) make the master ever
   surer of the wrong place. This, not the dead reckoning, is why the chart "showed quite the
   wrong reckoning" close in, and why the dangers list was wrong with the land in sight.
3. **Any line of position taken after two miles' run replaces the account across that line,
   whatever its quality** (`reckoning.py:696-708`). That is claim A's lunar. It is deliberate
   and documented in the module; it contradicts the letter of spec §13 ("the simplest Kalman
   form"). The same rule makes the first sounding after a run jump the account.
4. **Nothing warns of land ahead.** The lookout hails each named feature once per sighting
   episode, hails "steady and closing" once per episode at about three miles, never mentions
   the coast itself while any named headland is in sight, never sees shoal water, and has no
   urgent line at all. All the queries a look-ahead alarm needs exist and cost about 5 µs
   each [QUERY].
5. **The pilot is a person who speaks.** "Took charge of her" is a phrase in one log line
   (`ports.py:816-819`). He does not steer, warn, refuse or fix her position; his one
   mechanical effect is to supply the tack and the course *out* to `get under way`, which he
   did for the inward-bound Harpy. The primer says he does not steer (`14-the-port.md:75`);
   the primer's chapter 12 and a comment in the reckoning call him "the better answer" to
   standing into danger.
6. **Anchors are placed on the chart by a different arithmetic from the ship**
   (`core/world.py:581`), which is why she was "brought up ... in no water" and which also
   feeds a wrong depth to the cable's physics.

Two honesty findings sit beside these and bear on how to design the fixes: the reading
`the port` gives the **true** bearing and distance of the port's roads to a tenth of a mile
(`ports.py:983-1000`), and `the depth of water` is the **true** charted depth under the keel
(`api/readings.py:557-566`); both are in every sample a model receives
(`agents/tools.py:153-162`). And `take a bearing of` a *sail* fixes the reckoning on her true
position (K.3).

---

## A. A worse fix replacing a better account

**Claim.** "A lunar 'trusted within 20 miles' replaced an account that a recent Eddystone
bearing had made good to about 2. The account jumped 33' east ... A new fix should only
replace the account when its uncertainty is smaller."

**Verdict: CONFIRMED in code** as to the mechanism (the lunar replaces the account's longitude
without comparing doubts). It is the module's documented rule, not an accident, and it
disagrees with the spec's wording. Two qualifications from the logs: in session 2 the same
kind of lunar was *blended* and did nothing, because of the same rule's other branch; and in
session 4 the old account was not in fact good to 2 (the landfall put the truth between the
two figures).

**How the account is held.** `Reckoning` (`reckoning.py:556-580`): a position (`lat_deg`,
`lon_deg`), a 2×2 covariance `P` in square miles east and north, two bias accumulators
(`set_doubt`, `leeway_doubt`), and `run_since_fix_nm`, "the run since the last observation".
The master's sentence is the east and north standard deviations rounded
(`uncertainty_words`, `:805-813`).

**What each observation does.** Everything goes through one function,
`Reckoning.update_line` (`reckoning.py:675-727`), a line with a normal and a sigma:

```
696        if self.run_since_fix_nm > FIX_RUN_NM:
697            self._move(n_e * z, n_n * z)
...
704            self.P = [
705                [along_var * t_e * t_e + r * n_e * n_e, ...
...
709        else:
710            pn_e = p[0][0] * n_e + p[0][1] * n_n  # P n
...
713            k_e, k_n = pn_e / s, pn_n / s  # the gain
```

`FIX_RUN_NM = 2.0` (`:224`). So:

| Observation | Call | Sigma used | After more than 2 miles' run since the last observation | Within 2 miles of the last |
|---|---|---|---|---|
| Noon latitude | `update_latitude` `:729-732` | instrument, horizon, sea: about 2 to 3.5 | **replaces** the latitude; N-S doubt becomes the sight's | Kalman blend |
| Time sight (chronometer) | `update_longitude` `:734-739`, from `take_time_sight` `:1908` | hypot(2.5 × skill factor, a second a day since rating) | **replaces** the longitude | blend |
| Lunar | `update_longitude`, from `_lunar_cleared` `:2001` | 0.25° × skill × sea × moon's rate, 10 to 39 miles at 50 N (`sights.py:688-719`) | **replaces** the longitude; E-W doubt becomes the lunar's | blend |
| Bearing of a mark | `update_bearing` `:741-746`, then `update_distance` `:748-755` (from `take_bearing` `:1394-1400`) | across: distance × tan 1.5° (`:2385-2388`); along: 15% of the lookout's distance | bearing **replaces** across its line; it zeroes the run, so the distance line that follows is always a **blend** | both blended |
| Transit | `update_bearing` with 0.1 mile (`:1445`) | a cable | replaces | blend |
| Sounding with bottom | `update_line` `:1291` | 3 miles across the contour | **replaces**: moved onto the nearest matching contour point within max(5 miles, twice the ellipse) (`:1263-1277`), across-doubt set to 3 | blend |
| "No bottom" cast | none (`:1252-1255`) | | nothing, and the run is not reset | |
| `set the reckoning` | `set_position` `:757-765` | 1 mile | sets, and arms the next line to replace (`:764`) | |

Nothing compares the measurement's sigma with the account's doubt. The choice between
"replace" and "blend" is made on the distance run alone. The module says why
(`reckoning.py:682-692`): "A line taken after the account has run on ... *replaces* the
account across it, the prior's doubt across the line taken as unbounded ... a weighing by
that doubt would let a bad account outvote a good sight (N §3, the Apollo)." The tuning
notes record the constant as judgement (`docs/dev/TuningNotes.md:813`).

**The lunar's stated trust is never compared.** `_lunar_cleared` (`reckoning.py:1989-2026`)
does `self.bring_up()`, then `moved = r.update_longitude(lunar.longitude_deg,
lunar.sigma_nm)`, then writes the line. The trust words are two sigma to the nearest five
miles (`sights.py:580-582`), used only in the text.

**Against the logs.**

- Session 4, tick 86,831: "A set of distances of Altair and the moon taken by Mr Travers and
  two of the young gentlemen, and cleared: longitude by lunar 3° 46' W, which he would trust
  within 20 miles; the reckoning was 4° 19' W." Before: 49° 42' N, 4° 19' W by account (the
  officer at 82,296). After: the account's longitude was 3° 46' W (officer at 87,063: "the
  account has been moved to it. That's thirty-three minutes east ... about twenty-one
  miles"); noon line 111,720 "Longitude by account 3° 42' W"; 3° 37' W by 141,901. The last
  observation before it was the Eddystone bearing at 54,242, some thirty miles of run
  earlier, so the replace branch ran: 33' × cos 49.7° = 21 miles moved, and the east doubt
  set to the lunar's ten.
- Session 8, tick 51,502: "longitude by lunar 4° 54' W, which he would trust within 50
  miles; the reckoning was 4° 22' W." The officer at 52,178: "The account now stands at 4°
  53' W, not 4° 22', and his doubt east and west has grown from two miles to twenty-five."
  That is `P` across the line set to `r` (`:704-707`), exactly. The captain undid it by
  hand (`set the reckoning`, 52,247).
- Session 2, tick 159,648: "longitude by lunar 4° 29' W, which he would trust within 25
  miles; the reckoning was 4° 06' W." Here the account did **not** move: "The reckoning
  worked up: 48° 45' N, 4° 05' W by account ... I would not trust the reckoning within a
  mile east or west" (168,002). She had run little since a bearing at 153,316 and lay hove
  to from 156,084, so `run_since_fix_nm` must have been under two miles: the blend branch
  ran, with a gain of a few thousandths. Same code, opposite outcome, decided by whether
  she had sailed two miles.

**What the landfalls say of the premise.** Session 4, 182,230, the officer on raising the
Isle of Bas: "That bearing puts us near 48° 57' N, 3° 58' W. My reckoning was a dozen miles
too far west, and his lunar of yesterday, at 3° 46', was nearer the truth than my Eddystone
run." So the account before the lunar (which is what the officer had carried on privately)
was about 12 miles out with a stated doubt of 2 or 3, and the account after it about 13
miles out the other way (3° 37' to 3° 40' W by account against 3° 58' W by that bearing;
worked from the officer's figures, not from a save). In session 8 the old account was right
in longitude and the lunar some 21 miles wrong (my reading of the landfall bearings; M1,
which had the save, says of the officer's later doubt "it was not" nearer).

The master's east-west doubt after a land fix is small by construction
(`SET_DOUBT_EAST_KN = 0.2`, `:202`, against Channel streams of one to three knots), which
is the "ellipse drawn too small" the module itself describes (`:23-29`). A rule "replace
only when better" judged on the *stated* doubt is right in session 8 and neutral in session
4; it does not make the account good.

**Root cause.** One switch (`run_since_fix_nm > 2`) stands in for "is this sight better than
the account". It was tuned for a noon latitude after a day's run, where the answer is yes.
For a lunar a few hours after a land fix the answer is no.

**A second, smaller fault in the same code.** The lunar's longitude is drawn at the moment
the distances are taken (`_lunar_taken`, `:1978`, "the moment of the observation is the
moment that matters") and applied an hour later to the reckoning brought up to *then*
(`:1998-2001`). It is not carried forward by the hour's run. At seven knots on an
east-going course that is four or five miles of longitude added to the lunar's error.

**Documents against code.** Spec §13 (`TechnicalSpec-M5.md:290-294`): "updated by each
observation as a line or a point measurement, the simplest Kalman form". Study §3
(`Navigation1805.md:278-282`) the same. A Kalman update would have moved session 4's account
about a mile. The spec also says "A time sight by chronometer and a lunar collapse east and
west, by their own errors" (`:316-317`), which is what the code does. The primer
(`12-the-longitude.md:62`) says "The reckoning is updated by it, east and west" and that
whether to believe a lunar "is the judgement the period's captains made"; the code makes
that judgement for the captain and the log line does not say that it has.

**Fix.** Three ways, smallest first.

1. *Lunar only, "blend unless better" (S).* In `_lunar_cleared`, if `lunar.sigma_nm >=
   r.sigma_east_nm`, take the blend branch; else replace as now. Needs a `replace: bool |
   None` argument on `update_line`/`update_longitude` (about 15 lines in `reckoning.py`).
   Have the line say what the master did ("... which he would trust within 20 miles; the
   reckoning, which he trusts within 5, was 4° 19' W, and he lets it stand" or "and he has
   put the reckoning there"). Carry the result forward by the account's run in the clearing
   hour. Session 4: the account would have moved about a mile; session 8: about a cable.
2. *The same for the time sight and the sounding (S more).* A sounding's three miles should
   not replace a bearing-fixed account either (session 2, 149,667: the first cast with
   bottom after a run "jumped" the reckoning, the captain's word at 149,865).
3. *A general rule in `update_line` (M, and I would not).* "Replace only if the sight's
   sigma is under the prior's across the line" also catches the noon latitude, whose sigma
   (2 to 3.5) is often above the stated N-S doubt after a few hours (about 1). The latitude
   would then be blended, the 5b passage's noon correction would shrink, and Falconer's rule
   ("the observed latitude replaces the reckoned one", `:685-687`) would be lost. If a
   general rule is wanted, exempt the latitude and the bearings by name.

**Risk.** Option 1: no pinned book takes a lunar (`data/scenarios/*.orders` have none), so
the six recorded digests in `tests/test_known_truths.py` (`:2494`, `:2863`, `:2870`, `:2873`,
`:3707`, `:3733`) stand. `tests/test_longitude.py:281-322` sets the account's doubt to 15
miles before its lunar, so "the account on its line" still holds. Option 2 reaches the naval
cruise, whose book takes a time sight daily (`naval-cruise.orders:38`); by my arithmetic the
sight (about 2.2) stays better than the account (about 4 to 5 after a night), so the replace
branch still runs and the digest should not move, but that has to be measured. Old saves
replayed under any new rule diverge from the first lunar onward, as with every change of
behaviour (a save is seed and journal; `ENGINE_VERSION` is still "0.0.1",
`core/world.py:27`). No change to the consent brief.

---

## B. The dangers list follows the account even with the land in sight

**Claim.** "it had us 'on' the Triagoz while we were 20 miles west of them ... Once the land
is in sight, it should come from the best fix, whether bearings or the lookout."

**Verdict: CONFIRMED in code.** The list, the "line passes" warning and every "by the chart"
query read the account and nothing else. There is no second estimate to prefer: no object in
the code is a "fix".

**The code.**

- `the dangers` (`api/readings.py:1399-1409`) calls `Navigation.dangers`
  (`reckoning.py:1707-1744`): `now = self.account_now()` then
  `chart.dangers_near(now, radius)` (`:1717-1718`; `chart.py:1078-1086`). Kinds: rock,
  ledge, drying, shoal (`HAZARD_KINDS`, `chart.py:110`). Ten miles unless said. The words
  end "by account, within 10 miles". Distances are whole miles through `miles_words`
  (`:351-356`): under half a mile is "half a mile", under a quarter "no distance". That is
  the Lugo rock "no distance" at Falmouth (session 2, 16,052) and the Gilstone "N by W, no
  distance" at St Mary's (session 4, 549,190).
- `shape a course for <place>` (`reckoning.py:1617-1665`): `chart.line_passes(r.position,
  feature.position, within)` from the account (`:1653-1664`); for a pricked position,
  `nav.account_now()` (`orders/navigation.py:110-128`). "The line passes X within a mile"
  is a line on the chart from where the master thinks she is.
- `the bearing of <mark> by the chart`, `the distance to <mark>`: `by_chart`,
  `reckoning.py:1682-1705`, from `account_now()`.
- A bearing taken feeds them at once, because it moves the account (`take_bearing`,
  `:1392-1400`) and the next reading reads the account. Nothing else does. The lookout
  having the land in sight changes nothing by itself; bearings are by order (and the order
  is outside an officer's domain: session 2, 15,573, "'Take a bearing' is refused to me as
  the master's").
- A danger the lookout actually sees is listed separately, first, in `what is in sight`
  (`lookout.py:718-738`).

**Why it misled with the land in sight.** Three things, in order of weight.

1. The bearings themselves were carrying the stale distance (section 0, item 2; section C).
   At St Mary's the schooner lay at anchor with bearings taken and "the account is wrong
   again" (549,190). At Cawsand the Harpy's last handover says "Trust the bearings over the
   chart's reckoning" (689,841); H5's data has the lookout saying "Cawsand ... seven cables"
   at a true 2.7.
2. Each scenario starts with the account a mile out, at anchor in a named road.
   `Navigation.__init__` (`reckoning.py:929-933`) draws the departure "a mile in doubt"
   (`DEPARTURE_SIGMA_NM = 1.0`) unconditionally. Sessions 2, 4 and 8 all open at anchor in
   Carrick Road or off Plymouth, and the first dangers reading is already wrong (session 8,
   tick 83: "the reckoning ... now puts the Black Rock and the Governor about a mile off").
3. In session 4's Triagoz case no land was in sight; the list followed the lunar's
   longitude (A). By the next morning's landfall she was about a dozen miles of longitude
   west of where that account had her.

**What "the best fix" could mean in this code.** There are two honest designs.

- *Make the account follow the land* (preferred; nothing downstream changes). Fresh
  distances (C, fix 1), and the master taking his own bearings in pilot waters: when a land
  or mark sighting lies within a league by day, do what `take_bearing` does for the two
  best-cut marks every few minutes, with one routine line a glass. Period-true additions
  that cost little: **anchor bearings** at `ship.anchored`/`ship.brought_up` (a master
  always took them), and a harbour departure of a cable, not a mile, when the scenario
  opens at anchor in a port. Size M. Then the dangers list, the shaped course's warning, the
  distance readings and the browser's chart all follow with no special case.
- *A second list "by the land in sight"* (M): in `dangers()`, when the lookout has land or
  marks in sight, work a position from their bearings and estimates without touching the
  reckoning (a reading must not move the account, `:1078-1083`), and list from that, saying
  "by the land in sight". It needs fix 1 first or it inherits the stale distances.

**Risk.** Automatic bearings draw from the `reckoning` stream and move the account that the
pinned books shape their courses from: the three 5b passages and both 5c ones would need
re-measuring (ticks, lines, digests). Drawing them from a stream of their own keeps the other
draws in place but not the tracks. A shorter harbour departure moves both 5c digests.

---

## C. No alarm when standing into visible land

**Claim (owner's note 19).** A lookout who would reasonably cry out should produce at least an
urgent alert; perhaps a vector cast ahead from the true course, scaled by speed, clamped by
visibility; and perhaps the reckoning made precise close to land.

**Verdict: CONFIRMED in code.** No such call exists, and nothing the lookout says is urgent.

### C.1 What the lookout calls today

`World._tick_chart` asks the lookout to look once a game minute
(`core/world.py:709-711`). `Lookout.look` (`lookout.py:251-360`) gets the chart's features in
sight (`chart.py:1005-1052`), adds the shore itself under one condition, adds other sail, and
logs only what is *newly* in sight.

| Thing | Seen as | When | Range | Line and severity |
|---|---|---|---|---|
| headland, island, hill, town, place (`LAND_KINDS`, `chart.py:160`) | land | day; twilight at half range; night within a mile, three if moonlit (`:1045-1048`) | least of the visibility (12, 4, 1 or 0.1 miles, `weather.py:182-187`) and the horizon 2.08(√eye + √height) | once per sighting episode (again only after 30 minutes out of sight, `lookout.py:88`); routine, notable in the look that makes a landfall (`:329`) |
| castle, tower, church, mill, beacon, mark, a lighthouse by day | mark | day and twilight; never at night (`chart.py:1147-1148`) | as land | routine |
| a light lit in 1805 | light | twilight and night | its luminous range in the weather (`:1039-1042`) | "A light on the ... bow, bearing ..." |
| rock, ledge, drying rock (`DANGER_KINDS`, `:161`) | danger | **by day only** (`:1143-1144`); only while the tide leaves its head above water (`:1034-1035`) | three miles at most (`DANGER_SEEN_NM`, `:77`, `:1043-1044`) | "... : a danger." notable |
| shoal, bank, anchorage, bottom note, transit | nothing | never (`_seen_as` returns None) | | |
| the shore itself, unnamed | land, "The land about X close aboard ..." | **only when no land-kind feature is in sight** (`lookout.py:294-297`) | three miles, the visibility, a mile by night (`:624-647`) | once per episode |
| other sail | sail | by day to her masthead's horizon; a boat within two miles; within a mile at twilight and night (`ships.py:1018-1041`) | | "Sail ho!" notable; made-out lines routine |
| shoal water, breakers, the depth | | never | | |

At most six new things are hailed in a look (`LOOKOUT_HAIL_MAX`, `:94`). The reading `what is
in sight` shows eight, dangers first (`:718-738`); `the land` says only "in sight" in words
(`:764-775`; `api/readings.py:2387-2388`).

**"Bearing ..., steady and closing"** (`lookout.py:388-419`; constants `:123-126`) fires for a
danger at any range it is seen, or a land feature or a light within three miles, when the
sighting episode is ten minutes old, the bearing is within one point of **the bearing at the
episode's first look**, and the distance is no more than four fifths of **the distance at the
first look**; once per episode; notable (`:418`). The shore sighting is excluded (`:395`),
marks are excluded. It is a one-shot hail at about a league, measured against where the thing
first bore, possibly hours before. It is not a collision test and it never repeats.

**Nothing in `lookout.py` is `Severity.URGENT`.** The only urgent kinds in the game are
`ship.aground`, `ship.waterlogged` (`ground.py:198`, `:265`), `ship.aback`, `ship.beam_ends`
(`integrate.py:253`, `:265`), parted lines, spars and sails (`strain.py`), and a parted cable
(`anchor.py:271`). An urgent line is what wakes a station from any stand-by
(`agents/harness.py:790-795`) and eases the compression for the human (`ui/server.py:204`,
`ui/console.py:227`).

### C.2 Why the Harpy got nothing

The line: "She has taken the ground forward, on sand, foul and rocky in the north part: two
fathoms of water by the chart, and she draws 11 feet; she struck at three knots" (636,653).

- It was the tiles' test, `Chart.aground` (`chart.py:786-828`), not a named rock:
  `danger_under` would have named it ("... (rock)", `:866`). The words "sand, foul and
  rocky in the north part" are the bottom note of the Cawsand Bay anchorage, the nearest
  within three kilometres (`bottom_near`, `:930-938`; `features/channel-west.yaml:708`).
  "By the chart" in that line is in fact the depth plus the tide (`:822`, `:433`).
- The ground is the foot of Penlee Point itself. [QUERY] Along the reciprocal of "Penlee
  Point bore NNE", the tiles are land out to 250 m from the feature's coordinate, and at
  300 m there are 7.8 m of water fifteen metres from the shore. The water shoaler than her
  draught plus a metre reaches 25 to 300 m to seaward of the point and no further. She ran
  onto a steep-to headland in a four-mile visibility by day.
- No feature of the chart is there: the Dragstone (`channel-west.yaml:688-698`) is a sunken
  rock charted nearly half a mile east-north-east of the point's coordinate, always covered
  (`dries_m: -3.4`), so never sighted, and with 3.4 m over it at the datum and the tide on
  top a brig drawing 3.5 m floats over it at all but the lowest water.
- What the lookout did say: "Rame Head bearing NNE, steady and closing: distant three
  miles" (633,060), the same of Penlee Point (633,420) and Cawsand (633,840), 59, 53 and
  46 minutes before; then nothing, because each episode had said its once. Seven seconds
  after she struck: "Drake's Island bearing NNE, steady and closing: distant three miles"
  (636,660).
- What the readings said: "Penlee Point bore NNE, a mile by estimation" at 636,493 and
  again at 636,626, twenty-seven seconds before the strike. H5's data puts the truth at 2.9
  and 1.7 cables. The estimate had last been judged when she was about a mile off and was
  held (`lookout.py:381-384`):

  ```
  381            moved = _miles_between(ep.judged_at, here)
  382            if moved >= ESTIMATE_HOLD_NM:
  383                ep.estimate_m = s.distance_m * ep.factor
  384                ep.judged_at = here
  ```

- The distance is in any case to the feature's *coordinate*, which for Penlee Point lies
  250 to 300 m inland of the shore she touched [QUERY], so a fresh figure would have read
  "two cables" at the moment of striking.
- "The land about Penlee Point close aboard" could not be said: Rame Head, Penlee Point and
  Cawsand were in sight, so the shore's own hail was suppressed (`:294-297`).

So nothing in the lookout's rules could have seen that ground, and the one number that could
have warned was frozen.

### C.3 The owner's cast-ahead, against the code

Every piece exists.

- *The true course and speed over the ground:* `ships._ship_velocity(world)`
  (`ships.py:1047-1062`), metres a second east and north with the stream, nothing at anchor.
  `Ports._ground_speed_kn` (`ports.py:654-665`) is the same sum.
- *The sight limit:* the rule `_shore_close_aboard` already uses (`lookout.py:637-643`):
  least of a constant, the visibility, and a mile by night (three moonlit).
- *The ray:* `pos.advanced(dx, dy)` (`geo.py:72-84`) or `destination` (`:139-149`).
- *The tests along it:* `chart.depth_at(p)` (`chart.py:767-771`) for the water's edge
  (depth plus `world.tide_height_m` at or under nought is land now);
  `chart.coast_distance(p)` (`:942-952`) to skip everything when the coast is beyond the
  ray; `chart.line_passes(a, b, within)` (`:1088-1115`) for charted rocks on the line,
  filtered by `Feature.covered(tide)` (`:287-297`) so that only a rock that shows is
  "seen".
- *Cost:* [QUERY] 5.4 µs a `depth_at` and 5.6 µs a `coast_distance`, including the
  position arithmetic. A ten-minute ray sampled every 50 m is 20 to 40 samples: about 0.2
  ms. A tick takes some 1.2 ms (843 ticks a second, `test_known_truths.py:2631`). At the
  lookout's minute the cast is a quarter of one per cent of that; every ten seconds inside
  a mile, between one and two per cent. One `coast_distance` first makes it free offshore.
- *What it would have given the Harpy:* [QUERY] steering NNE at four knots for the point, a
  ten-minute ray first meets the land when she is 1,400 m short, 9.3 minutes before; at
  1,000 m, 6.1 minutes; at 500 m, two minutes. The "water under her draught plus a metre"
  test fires at the same sample as the land test, because the shore is steep-to: the land
  test alone is enough there.

*Where raised.* In `Lookout.look` (it has the position, the visibility, the daylight and
the heading), returning a line as the others do. A ladder keeps it from being noise: a
notable line when the land is under ten minutes ahead ("Land ahead, on the larboard bow,
distant five cables"), urgent under four ("Land close aboard right ahead!"), urgent again
under two; re-armed only after the ray has been clear for some minutes or her course over
the ground has changed two points; silent at anchor, aground, and hove to with no way. It
needs that care: the m5c-b notes show what an urgent line that fires in ordinary conditions
does to a station (the aback alarm). Standing in for an anchorage every ray ends on land, so
the first rung should be notable and the urgent rungs short.

*What it says.* Only what an eye sees: relative words (`relative_words`, `:160-173`) and a
distance by estimation (`estimate_words`, `geo.py:250-260`), as the existing shore line does
("The land about Penlee Point close aboard on the larboard bow, bearing N by E, distant two
cables", `lookout.py:662-663`). Land ahead; a rock showing ahead; perhaps "broken water"
where there is under a fathom over the ground. **Not** water merely shoaler than her
draught: nobody at a masthead sees four fathoms from two in the Channel, and that is the
lead's business (and the pilot's, E).

*Honesty.* It reads the truth as every sighting does (a headland's bearing is already the
true bearing and its distance the true distance within a sixth). It gives no position and
does not touch the reckoning. In fog it is clamped to a cable or a mile, so it is late, as
it should be.

*Size and risk.* M: `lookout.py` (about 80 lines), an event row or two in
`api/readings.py` (`:2123-2143`) so a book can say `at land ahead then heave to`, tests,
primer 10 or 12. No random draws, so no stream moves. New lines change the digests and line
counts of any pinned passage that stands toward land (the thick 5b passage raises "the land
about Black Head close aboard" and would gain lines; the others anchor in a road). Ticks move
only where something reacts to the new line.

### C.4 "The reckoning very precise close to land"

There is already a rule by which bearings tighten the account in proportion to the distance:
across the bearing, the distance times tan 1.5° (`_bearing_sigma_nm`,
`reckoning.py:2385-2388`: half a cable at two miles); along it, 15 per cent of the lookout's
distance (`:1397-1400`); a transit a cable (`:257`). Close to a mark that is a cable or two.
Two things defeat it today:

1. the distance is the held one (section 0, items 1 and 2);
2. it happens only by order, and an officer has not the order.

So "precise near land" is not a new mechanism. It is: (a) **fix the hold** (S), (b) have the
master take his bearings himself in pilot waters (M; B above), and optionally (c) measure a
big feature's distance to its near shore and not its middle (D). I would not add a rule
that shrinks the ellipse by proximity alone: that would be the truth leaking into the
account with no observation behind it.

**Fix 1, the hold (S; the single most useful change in this report).** In `_judge`, judge
afresh when the true distance has changed by a tenth since it was last judged (keep the
episode's own factor, so no new draw and no flicker in a calm). That one rule serves land
and sail alike: a sail moves when the observer may not, and it is her distance that counts.
(For land alone, holding for the lesser of a mile and a tenth of the distance of the ship's
own run does much the same.) One field more on `Episode` (a class default keeps old
checkpoints loading). `tests/test_longitude.py:567-597` (the Lizard at ten miles: held at
half a mile on, judged afresh a mile and a half on) passes unchanged under "a tenth, a mile
at most". Risk: no stream moves, but every `bearing.taken` after the first of an episode
lays the account differently, the books shape their courses from the account, and the
`lookout.closing` and `lookout.made_out` lines carry the estimate: all five pinned passages
with land or a cutter in them need re-measuring. Documents to change: primer
`12-the-longitude.md:99` ("held until the ship has made a mile"), `15-other-sail.md:29`,
`TuningNotes.md:1064` (which gives the intent as "held while she makes under a knot").

**Fix 2, the shore always (S).** Drop the condition at `lookout.py:294`: keep the nearest
shore as a sighting whenever it is within the sight limit, whatever headlands are in sight,
judged each look. It is then in `what is in sight` and can be the `nearest` of `the land`.
`tests/test_reckoning.py:551` asserts the old rule ("a headland in sight: no shore hail") and
would change. This is also D's cheapest answer.

---

## D. Parity near unnamed coast and area landmarks

**Claim (owner's note 24).** A general way to give a model what it needs near coast that is no
landmark, and near landmarks that stand for whole areas; "nearest land" in the readings;
features named by their parts.

**Verdict: CONFIRMED in code** that the need is real: a feature is a point, the coast has no
words at all while a headland is in sight, and the only numbers a model gets are distances to
feature coordinates, held.

**What a feature is.** `Feature` (`chart.py:240-268`): id, kind, name, modern name, one
latitude and longitude, a height, `extent_m`, a light's dates, a transit's marks, a bottom
note, a depth, `dries_m`. No outline and no parts. `extent_m` is a radius used only for
striking and for the shaped course's line (`:863`, `:876`, `:1111`); 25 of the 206 features
have one. The Isle of Bas (`features/channel-west.yaml:2207-2215`) is `kind: island` at
48.7450, -4.0100, height 30, **no extent**. [QUERY] In the tiles the island's land runs from
about 4.03 W, with detached rocks out to 4.04 W, to 3.98 W (some two miles) and from 48.742
to 48.756 N; the coordinate is its middle, 0.8 of a mile from the west end of the main body
and 1.3 from the outlying rocks. Penlee Point's coordinate is 250 to 300 m inland.

**The coast** exists twice and is anonymous both times: as 2,595 polylines (19,893 points,
properties `source` and `level` only) for the browser (`chart.coast_lines`, `:1153-1158`;
`api/queries.py:104-130`), and as a distance-to-shore field in the tiles (15 m cells near
the ports at level 3, 93 m elsewhere), read by `coast_distance` in microseconds
(`:942-952`). `coast_at` (`:954-974`) puts a name to it from the nearest land-kind feature
within twice the distance, a mile at least.

**How "the Isle of Bas bearing E, distant two miles" is made.** `chart.in_sight`:
`bearing, distance = bearing_and_distance(pos, f.position)` (`chart.py:1036`), to the
coordinate. The distance by estimation is that distance times the episode's factor (one
sigma 0.15, `lookout.py:114`, `:375`), held for a mile of the ship's run (`:381-384`), then
worded to the cable under a mile, the mile under two leagues, the league beyond
(`geo.py:250-260`). The bearing is true and fresh each look.

So two or three cables off the island's westernmost rocks the list reads "the Isle of Bas
bearing E, distant a mile" [QUERY: a true 1.3 to 1.5 miles to the coordinate at two sample
points there], and with the hold, "two miles".

Session 8: "The Isle of Bas bore ..., two miles by estimation" at 120,966, 121,566, 121,730,
122,166, 122,766, 123,366 and 123,625, forty-four minutes in which she ran in to three
fathoms, anchored, weighed and stood out to sixteen. "The Lavandière bore S, a mile by
estimation" at 121,747 beside a cast of three fathoms.

**What the readings say of the land today.** `what is in sight`: up to eight sightings in
those words. `the land`: "in sight" or "not in sight"; the nearest is in the data and not in
the words. `the dangers`: by account, whole miles. `the depth of water`: the true charted
depth under her (G). `the port`: the true bearing and distance of the port's nearest road
(K.1). Nothing gives the distance or direction of the nearest shore, unless no headland at
all is in sight. The harness's own example of a captain's allowance is "you may tack ship if
the land closes within two miles" (`orders/stations.py:339`; `agents/harness.py:1734-1736`,
"judged by the officer"), a condition no reading supplies.

**What the human has that the model has not.** The chart pane (`client/map.js`) draws the
coastline and the features, with the reckoned position, the ellipse, the track by account,
the bearings as lines from their marks, the soundings and the strangers. The human sees the
*shape* of the coast; the model has words only. But the pane is drawn about the account, so
when the account is out the picture misleads (owner, 636,831: "I was reading the reckoning
on my chart that was wrong"; 121,840: "My chart showed quite the wrong reckoning"). Neither
sees the truth. In the Harpy's last minutes the model, from bearings and the depth reading,
called the danger four minutes before the strike.

**What the requested readings would need.**

1. *"The nearest land": cheap (S).* `chart.coast_at(world.position)` already returns the
   distance, the bearing toward the shore and a name. `_shore_close_aboard` already turns it
   into "The land about X close aboard on the larboard bow, bearing SE by S, distant three
   miles" under the visibility and night rules. Fix 2 of C makes it a standing sighting; a
   registry row (`the nearest land`, kind `sight`) puts it in every sample
   (`agents/tools.py:159-162` carries every non-parametric row). The standing dialect reads
   `in_sight` from the value (`standing/rules.py:241-245`), so richer words break no rule.
   Three details: the shore's distance is "judged true" today (`lookout.py:366-367`) and
   might take the eye's factor for consistency; the bearing comes from the gradient of an
   integer field and is coarse [QUERY: steps of twenty degrees and more], good for "on the
   larboard bow", weak for a point of the compass; and the name fails close to a big
   feature, because the search is a mile about the ship: [QUERY] two cables off the west end
   of the Isle of Bas `coast_at` returns no name. Widening the search toward the shore's
   direction, or giving islands an `extent_m`, mends that (S).
2. *"Rocks breaking close aboard to larboard":* the same query on the danger kinds with
   relative words; S once 1 exists.
3. *Features by their parts, by hand: data, not code.* "The west end of the Isle of Bas" as
   its own point feature (`kind: headland`) is sighted, listed and takes a bearing like any
   other, and a bearing of a point is a better fix than a bearing of an island. About eight
   lines of YAML each, with a source as every entry has; the features index
   (`charts/features/channel-west.index.json`, read at `chart.py:718-727`) must be rebuilt
   by the chart tool or the new features are not found by `nearby`. A dozen for the five
   ports' approaches is a day's work.
4. *Features by their parts, derived: L.* The coast's polylines carry no names, so "the west
   end of X" needs each named feature tied to its landmass and the extremes computed at
   build time. A design decision first.
5. *Distance to the near shore of a big feature (S to M):* word the distance as the
   coordinate's less `extent_m`, and use the same in `update_distance`. Only worth it if 3
   is not done.

**Risk.** A new reading row changes no log line; the registry is listed in documents and the
tools' descriptions, not in the consent brief's file. New features move sightings near them
(only Roscoff's approach is in no pinned passage). Fix 2 changes the lookout's lines near any
coast.

---

## E. The pilot's conduct

**Verdicts.**

- Automatic, with no way to accept or refuse: **CONFIRMED in code**.
- "Took charge of her" does nothing to the helm: **CONFIRMED in code**; it is as the primer's
  chapter 14 describes, and against the log's own words, the same chapter's "where he takes
  her" and chapter 12's "the better answer".
- "The two-cables rule is applied on boarding but not on leaving": **NOT REPRODUCED from
  code**. One test governs both. The appearance comes from the held distance.
- "It had held eight cables off for an hour": **CONFIRMED in code**, a fault in how the
  pilot vessel "arrives".

**What brings him off** (`Ports._tick_pilot`, `ports.py:684-716`, once a minute): no pilot
aboard and no cutter out; the ship within the port's `cruising_nm` of its *outer road*
(Falmouth 6, Plymouth 8, Brest 7, Roscoff 6, St Mary's 8); not at anchor or aground; the
port not refused or left within six hours (`PILOT_AGAIN_H`); daylight (every port file has
`comes_off_by_night: false`); the port not hostile; a knot of way through the water and some
sail set. Then `_launch_cutter(port, "bring")` (`:622-652`) puts a vessel at the outer road
with the plan `[("to_ship", 2 cables)]`. Nobody asks for him. A ship *leaving* a port under
way by day gets one too (session 2: Mr Le Saout boarded the Harpy outward bound from Roscoff
at 212,220 and left 47 minutes later, £3).

**The boarding rule** (`ports.py:720-742`): within four cables she hails ("a pilot for
Plymouth; shorten sail and he will come aboard", routine). Then

```
736            if dist <= PILOT_BOARDS_WITHIN_M and self._ground_speed_kn() <= PILOT_BOARDS_UNDER_KN:
737                cutter.alongside = True
738                if self.cutter_errand == "bring":
739                    self._pilot_boards(port, cutter, now)
740                else:
741                    self._pilot_leaves(port, cutter, now)
```

Two cables of true distance and six knots or less over the ground (`:94-98`). No heaving to
is asked. "Mr Tozer boarded the Speedwell under way at about four knots" is the rule working
as written (primer `14-the-port.md:61`: "Within two cables, with your way under six knots,
he boards"). **Leaving is the same line of code** with the errand "fetch".

**Why it looked otherwise.** Session 4, Roscoff: "The pilot asks for sail to be shortened:
his boat is coming off for him" (258,540); "Sail ho! The Roscoff pilots' boat on the
larboard quarter, bearing SE by S, distant a mile" (258,600, the first look, a fresh
estimate); "The boat hailed: she has come off for the pilot" (259,500, within four cables);
"Mr Moal left her in the boat" (259,680, within two). In those eighteen minutes the schooner
ran under a mile, so the lookout's "a mile" was never judged again. The boat was two cables
off; the reading said a mile.

**Why the boat lay off and would not board.** `Vessel.tick` for a `to_ship` leg
(`ships.py:563-578`):

```
568            target = self._intercept(world, target)
...
571            arrive_m = (float(leg[1]) if len(leg) > 1 else units.CABLE * 2.0) * ARRIVE_FRACTION
...
575        bearing, distance = bearing_and_distance(self.position, target)
576        if distance <= arrive_m + 1.0:  # a metre: she stops at the mark
577            self._arrived(world, leg)
```

`target` is the **intercept point**, where the ship will be if she holds her way
(`_intercept`, `:492-523`), and `ARRIVE_FRACTION` is 0.75 (`:106`). On arriving,
`_arrived` (`:618-631`) leaves her with `[("lie_to", math.inf)]`: she lies to for ever,
drifting to leeward at a knot with the stream (`:553-562`, `LYING_TO_KN`). Nothing in
`_tick_pilot` sends her on again. With the ship and the boat closing head-on at four knots
each, the meeting point is midway, so she "arrives" a cable and a half from *it* while the
ship is three cables from *her*. If the ship then does what the hail asks and stops, the gap
never closes. Session 4: hail at 192,540, "Hove to" at 192,632, "the pilots' boat three
cables off our quarter" at 193,449, "has lain three cables off our quarter for an hour and
won't board" at 198,148, drifted to eight cables, and the pilot aboard at 200,760 only when
the schooner had sailed down to within two cables. The same held estimate made "eight
cables" look fixed. (P2 reads the code the same way.)

**Accept or refuse.** There is no order for either. The vocabulary's pilot verbs are `ask
the pilot` and its synonyms (`data/vocabulary.yaml:693-695`); "call the pilot" is a synonym
of `send for` (`:681`). The only ways not to take a pilot are to stay above six knots or
more than two cables from the cutter. `declined_until` is set only by a closed port's
refusal and after a pilot has left (`ports.py:798`, `:875`). The fee is taken from the purse
without a word (`:857`). Session 2 tried `hail the pilot`, `You may hail the pilot`, `You
may pilot` (15,428 to 15,442), all refused by the grammar.

**What "took charge of her" does.** `_pilot_boards` (`ports.py:778-846`):

- makes a `Person` (role pilot, skill 0.9 or 0.95, place quarterdeck). His skill is read by
  nothing.
- logs "The pilot, Mr X of P, came aboard from the cutter and took charge of her" (notable),
  then "The pilot says: ..." with the port file's `channel`, `marks` and `anchorage` words
  and a computed tide sentence (`pilot_words`, `:922-938`), then the news and any letters.
- sends the cutter to lie to ten minutes and go home.

After that the pilot is consulted by exactly three things: `ask the pilot <question>`
(`orders/people.py:66-72`; `Ports.answer`, `ports.py:946-972`), the readings `the pilot` and
`the port`, and `GetUnderWayScript.check` (`evolutions/scripts.py:4584-4594`), which takes
his `cast` and his `course_out_deg` when `get under way` is said bare.

He does **not** steer or set a course inward; refuse or question an order; warn of the
ground, the land or a rock; know or say where the ship is; improve the reckoning; alter the
lookout; or enter the grounding test (`ground.py` has him only in a comment, `:7`).

Three consequences seen in the logs:

1. *The speech, three times.* `answer` matches substrings of the question against six lists
   of keywords and returns a set paragraph; a question that matches none returns the whole
   boarding speech (`:972`), and an empty one the channel words (`people.py:71`). Session
   2: "ask the pilot off" (18,031) returned all of it. The Plymouth words are about 180
   words before the tide sentence. The port files' `pilot.words.tide` (for example
   `plymouth.yaml`, the "tide:" line under `words:`) is read by nothing; the tide answer is
   computed (`_tide_words`, `:882-920`).
2. *His course out, given to a ship coming in.* Session 2, 632,153, the Harpy weighing off
   Rame Head, inward bound, with Mr Tozer aboard: "Under way on the larboard tack ... full
   and by (SSW (200°) lying too near the wind to be laid)". That is Plymouth's `cast:
   larboard` and `course_out_deg: 200` (`plymouth.yaml:47-48`), the course *out of the
   Sound*. Had the wind allowed she would have been steered away from the port.
3. *He leaves by geometry.* With him aboard and the ship not at anchor, a cutter is sent to
   fetch him when she is more than the roads' distance plus a mile from the port's
   anchorage, further from it than a minute ago, and within the cruising ground
   (`ports.py:743-776`). There is no notion of inward or outward. Session 2, 20 June: the
   Harpy, afloat again and working into Cawsand Bay, steered south for a while; "The pilot
   asks for sail to be shortened: his cutter is coming off for him" (681,780) and "Mr Tozer
   left her in the cutter, clear of Cawsand Bay; the pilotage, £6, paid" (683,520). She
   anchored in Cawsand Bay ninety minutes later without him. At Roscoff on the 13th Mr Moal
   left the same way while she stood off for the night (150,480 to 153,240). The fetch has
   no daylight test, so he is fetched at night though not brought.

**A pilot aboard a ship standing into danger.** The code makes nothing of it. Mr Tozer was
aboard from 578,880 to 683,520; she struck at 636,653. In the hours before, he "said" one
thing, when asked (634,700), and it was his channel paragraph. Mr Moal was aboard the
merchant ship from 117,420 when she let go in three fathoms and a half on ground with half
a fathom at the datum (121,712); the captain: "Unfortunately, we can't directly ask Mr. Moal
in this build" (121,238).

**What the documents promised.** Spec §23 (`TechnicalSpec-M5.md:486-488`): "Arriving is a
sequence the log tells: the pilot cutter, the pilot aboard as a person, the anchorage, the
boat, the shore." §29: "Brest entered by the pilot". The module (`ports.py:5-19`): he comes
aboard "as a person ... with his skill, his words". So the spec promised a person and words,
and that was built. But:

- the log says "took charge of her" (`ports.py:817-818`);
- the primer says "the **anchorage**, where he takes her" (`14-the-port.md:100`) and, in
  the same chapter, "He does not steer her: the helm and the sail are yours, as the
  Regulations of 1806 left them to the captain, and he answers what you ask" (`:75`);
- on standing into danger the primer says "That is the warning the master could give; the
  pilot of a later chapter is the better answer" (`12-the-longitude.md:95`), and the code
  says the same (`reckoning.py:1647-1650`: "the pilot of package 35 is the better answer").

The better answer was never given a voice. In the pinned merchant passage it is the *book*
that pilots her through the Goulet, by waypoints shaped from the account
(`merchant-passage.orders:103-110`), with the pilot aboard as a passenger.

**Fixes, smallest first.**

1. *The cutter closes with the ship, and closes again (S).* Measure arrival against
   `world.position`, not the intercept point (`ships.py:575-578`); and in `_tick_pilot`, when
   the errand is bring or fetch, the vessel is lying to and the ship is beyond two cables,
   give her `[("to_ship", PILOT_BOARDS_WITHIN_M)]` again. About ten lines. Risk: the pinned
   pilot ticks (`GATE_5B_PILOT_HAIL_TICK` 56280, `..._ABOARD_TICK` 56340, the schooner's
   55380, `test_known_truths.py:2860-2866`) may move by a minute or two, and the digests
   with them.
2. *Say what he does (S, words only).* "came aboard from the cutter" and no "took charge",
   until he does; or keep it and do 4. Shorten the unmatched answer to "Mr X has nothing to
   say to that" plus the heads he can speak to.
3. *Inward or outward (S to M).* Give the pilot aboard a sense of which way she is bound
   (boarded beyond the roads: inward; boarded inside or from an anchor in port: outward).
   Use the course out only when outward; fetch him only when outward or when the captain
   says. This also stops a pilot being put aboard and paid for a ship that is leaving.
4. *Give him the warning (M).* The cast-ahead of C.3, spoken by the pilot when he is aboard
   in his own port's waters, and for him alone extended to what he knows and a lookout
   cannot see: water under her draught plus a margin along the ray (`chart.aground`'s own
   arithmetic, `chart.py:809-824`) and sunken rocks (`danger_under`, `:830-867`), in fog as
   well as clear. "Mr Tozer: you are standing into the Penlee shore, sir; bear away." That
   is the "better answer" the primer names, it keeps the helm with the captain as the
   Regulations had it, and it gives a pilot a reason to be paid.
5. *Accept or refuse (M).* A state between the hail and the boarding: `take the pilot` /
   `decline the pilot` (or "we want no pilot"), an event for the book, the refusal setting
   `declined_until`. The owner's note 9 ties this to hailing and signals; the minimum does
   not need them.
6. *The pilot cons her (L, a design decision).* An agent-like station that gives helm orders
   on the captain's allowance. The owner's note 1 expects the director to cover this later.

---

## F. Other vessels keeping a fixed distance

**Verdict: CONFIRMED in code, and it is the cache.** The vessels move. The lookout's distance
does not.

- *How they move.* A far-detail vessel follows a plan of legs at the speed her file's polar
  gives, once a game minute; within two miles of the player she is ticked every second
  (`ships.py:543-600`, `:944-966`, `:118-119`). Goals make the legs (`_goal_plan`,
  `:764-824`): bound for a place; trading between two; "patrolling off X within n miles" is
  a square of four marks about the station (`:795-805`), which from a ship lying at the
  station would be a real circling at 0.7 to 1.0 of the radius; but the frigate of the
  playtest was not patrolling. `merchant-schooner-plymouth.yaml` has "indefatigable ...
  position: Cawsand Bay, goal: bound for the soundings south-west of Ushant": she sailed
  away. A pilot vessel steers for the ship and then lies to (E).
- *How the distance is made.* `Lookout._judge` (`lookout.py:362-386`) treats a sail as it
  treats a headland: one draw per sighting episode (from the `sail` stream), and
  `ep.estimate_m` judged again only when `_miles_between(ep.judged_at, here) >=
  ESTIMATE_HOLD_NM`, where `here` is the **player's** position (`:369`, `:381-384`). A ship
  at anchor or hove to never moves a mile, so every other vessel keeps its first distance
  for the whole episode, while the bearing, which is computed fresh each look
  (`ships.py:1031`), swings. The words then quantise: cables under a mile, whole miles to
  two leagues, leagues beyond (`geo.py:250-260`).
- *Session 4.* Tick 0: "Sail ho! A frigate abeam to starboard, bearing W by N, distant eight
  cables." The schooner lay at anchor. The frigate stood out to sea and was lost at 11,760:
  "The sail on the larboard bow is out of sight." For as long as the schooner lay still the
  reading said eight cables.
- *Session 2, the two facts from the session reader.* (1) "Sail ho! A cutter standing out
  from the land right astern, bearing S, distant two miles" (15,120), judged with the brig
  barely under way. The pilot came aboard from her at 16,020, which needs her within two
  cables; at 16,084 the list still had "the Falmouth pilot's cutter on the larboard bow,
  bearing SSE, distant two miles", and at 16,220 "ESE, distant two miles". Cached. By
  17,340 the brig had run more than a mile and the figure had been judged again, so "two
  miles" there may be honest. (2) "Out of sight" two minutes before the hail: there were
  **two cutters**. The one that brought him was going home; `_tick_pilot` launches a second
  for the fetch "while the one that brought him is still going home" (`ports.py:748-765`),
  with a new id, hailed as a new sail at 17,700 ("Sail ho! The Falmouth pilot's cutter on
  the starboard quarter ... distant a mile"). At 18,300 the first reached her mark, was
  removed (`ships.py:630-631`, `:954`), and the lookout said "The cutter on the larboard bow
  is out of sight"; at 18,420 the second hailed. The lookout names both "the cutter"
  (`lookout.py:486-493`), so the log reads as one vessel vanishing and hailing.

**Fix.** C's fix 1 with the sail's own rule: for `seen_as == "sail"`, judge again whenever
her true distance has changed by a tenth (or every look; the factor is the episode's, so
there is no new draw). S, in the same few lines. Optionally say "the other cutter" or use
her errand when two of one name are in sight.

**In passing: a bearing of a sail is a fix.** See K.3.

---

## G. The hand lead and the depth

**Verdict: CONFIRMED; the model's explanation is right, and it WORKS AS DESIGNED.** One part
of the note is not right: there is a deep-sea lead.

| Number | Where | What it is |
|---|---|---|
| The lead's cast | `Navigation._cast`, `reckoning.py:1230-1293` | the chart's depth at the **true** position **plus the tide's height** (`:1238-1242`), with a quarter-fathom error for the hand lead and a fathom for the deep-sea (`:1256-1258`), rounded to the quarter fathom or the fathom |
| "No bottom at twenty fathoms" | `:1243`, `:1252-1255` | that sum is over the line's length: `HAND_LEAD_FATHOMS = 20.0` (`:237`), `DEEP_SEA_LEAD_FATHOMS = 120.0` (`:239`) |
| `the depth` | `depth_reading`, `:2226-2228` | the last cast, to the half fathom in words |
| `the depth of water` (`the water`) | `api/readings.py:557-566`, `:1089-1099` | `chart.depth_at(world.position)`: the chart's depth at the **true** position **at the datum**, no tide, no error |
| "let go in N fathoms" | `scripts.py:4062-4071`, `_water_depth` `:3813-3815` | `ship.extra["water_depth_m"]`, the chart's depth at the true position plus the tide, kept once a minute (`core/world.py:570-571`) |
| "N fathoms of water by the chart" (aground) | `chart.py:822-828`, `:433` | depth plus tide at the end that touched, despite the words |
| The chart in the browser | `api/queries.py:104-130` | no soundings but the casts taken |

So with fifteen to nineteen fathoms at the datum and one to five of tide, the hand lead
finds no bottom while `the depth of water` reads fifteen or more. Session 8, 121,291, the
officer working it out: "My four and a half was the chart's figure, which counts no tide".

**The deep-sea lead exists.** `heave the deep sea lead` (`data/vocabulary.yaml:503-510`:
also "heave the deep-sea lead", "strike soundings", "try for soundings");
`heave_deep_sea_lead.yaml`: twelve hands, fourteen minutes; no bottom with more than four
knots of way (`reckoning.py:240`, `:1245-1251`). Session 8 used it hourly. On the schooner
twelve hands are most of a watch, which may be why it was not reached for.

**Two things worth the lead's attention.**

1. `the depth of water` is a reading of the truth, in every sample. It makes the lead
   redundant except for the tide, and the difference between it and a cast *is* the tide's
   height, which spec §16 says is never read out (`TechnicalSpec-M5.md:385`: "no tide
   readout, ever"). The officers navigated by it: "11, 9½, 5½, now 4½ fathoms in six
   minutes" (636,618) are, by their half fathoms and by the want of any such casts in the
   log, its values and not the lead's; "The chart has three and a half fathoms under us at
   low water" (session 4, 200,213) is it by name. Whether it stays is a design question; if
   it stays, its words should say "by the chart at low water".
2. A "No bottom" cast is logged notable (`reckoning.py:1341-1342`) and is the event `a
   sounding` (`api/readings.py:2125`), so it wakes "stand by until a sounding" offshore, as
   the model's comment 13 says. Making a no-bottom cast routine and a separate event is S,
   and moves the pinned digests' severities.

---

## H. "Brought up by the best bower in no water"

**Verdict: CONFIRMED in code.** Not a missing figure: a depth of nought, taken at the wrong
place.

- The words: `come_to_anchor.yaml`, `on_complete: {log: "Brought up by {anchor} in {depth},
  {fathoms} of cable; {riding}"}`. `{depth}` is `_depth_words(self.anchor.depth_m)`
  (`scripts.py:3904-3912`), and `fathoms_words` (`chart.py:168-193`) says "no water" for
  anything under a quarter of a fathom (`:190-191`).
- The let-go line at 688,836, "The best bower let go in four fathoms", used the depth at
  the ship (`_water_depth`), and was right.
- Between the two, once a minute, `World._tick_tide` rewrote the anchor's depth
  (`core/world.py:578-584`):

  ```
  581            at = self.origin.advanced(anchor.ground_x, anchor.ground_y)
  582            d = self.chart.depth_at(at) if self.chart is not None else None
  583            if d is not None:
  584                anchor.depth_m = max(0.0, d + state.height_m)
  ```

  `ground_x`, `ground_y` are the anchor's place in the ship's flat plane, metres from the
  start (`physics/anchor.py:144-147`; `ship/parts.py:858-859`). The ship's own position is
  kept another way: each tick's run is turned to latitude and longitude at the latitude she
  is then on (`_tick_geo`, `:658-682`, `self._position.advanced(dx, dy)`). One flat step
  from the origin does not land where the sum of the small steps does, once she has made
  easting at one latitude and westing at another. [ARITH] A path like the Harpy's (Falmouth,
  Roscoff, westward off the Breton coast, north to Falmouth, east to Cawsand) puts the one
  step 540 m **west** of the ship; other plausible paths give 180 to 950 m either way. H5
  has it from the save at about 740 m west. She lay seven cables east of Cawsand, so the
  "anchor" was on the foreshore, `d + height` was under nought, `max(0.0, ...)` made it
  nought, and the line said "no water".

**It is more than words.** `anchor.depth_m` is the depth the cable's geometry and holding use
(`physics/anchor.py:175-184`: `length = hypot(dist, depth)`, `theta = atan2(depth, dist)`,
`holding_n(anchor, theta)`), and the short stay at weighing (`scripts.py:4599-4600`). After
any passage with easting in it, anchors hold or drag by the depth of some other spot. [ARITH]
Along the pinned merchant passage's own waypoints (Falmouth, 49° 52' N 5° 06' W, the
soundings south-west of Ushant, the Passage de l'Iroise, Bertheaume road, the Rade de Brest)
the one step lands 1.0 km east of the ship at Bertheaume and 1.3 km east in the Rade, so
that passage's anchor is sounded a kilometre from where she lies. On the 5b passage, which
runs north and south, the difference is about 12 m. The tests assert only
`startswith("Brought up by the best bower in ")` (`tests/test_anchor.py:127`,
`test_known_truths.py:3157`), so nothing catches it.

**Fix (S).** Take the anchor's place from the ship's: `self._position.advanced(ground_x -
ship_x, ground_y - ship_y)`. Two lines in `core/world.py`, a test that anchors after a
dog-leg. `_coast_of_plane` (`:684-694`) and `Vessel._wind_at` (`ships.py:459-472`) make the
same kind of conversion for the weather, where a few hundred metres do not matter. Risk: the
anchor's depth changes where a pinned passage anchors after easting: the 5c merchant
passage's last lines and digest will move, and perhaps a tick if her cable then holds
differently; the two 5b passages should move little or not at all (12 m), which has to be
measured.

---

## I. "The Harpy's reckoning kept advancing while she lay at anchor"

**Verdict: PARTLY.** The *run since noon* does advance at anchor. The *position* does not
run on, by a rule built for the purpose, but it does creep. The model's explanation (the log
reading the tide) is not what happened, though it is what would happen by order.

**How the step gets its speed and course.** Every tick `Navigation.tick` pegs the traverse
board (`reckoning.py:1009-1012`: sums of the sine and cosine of her heading, and a count),
and counts a tick as "no run" when she is at anchor or aground (`_riding`, `:1018-1020`,
`:1056-1063`) or hove to with under two knots of way (`:1021-1024`). The log is hove at the
hour (two-hourly in a vessel with no marines, `:992-999`, `:1051-1053`), and not at anchor.
`bring_up` (`:1110-1157`) advances the account by the *last log read* times the hours since
the last step less the part not under way (`_hours_under_way`, `:1159-1165`), along the
*mean heading since the last step*, corrected for variation, deviation and leeway.
`account_now` (`:1078-1108`) does the same for a reading without changing anything.

**What that does at anchor.** The Harpy: "Hove the log: one knot and three quarters" at
572,431; anchor down by 574,020; no heave at 21:00, as designed.

1. *The run since noon grows.* `since_noon_reading` (`:2243-2256`):

   ```
   2253        run = r.run_since_noon_nm + (self.last_log_read_kn or 0.0) * (
   2254            (self.world.clock.tick - r.last_step_tick) / 3600.0
   2255        )
   ```

   No discount for the time at anchor or hove to. 1.75 knots for an hour is the "run since
   noon from 23 to 24 miles" of the officer's journal (576,750). `no_noon_words`
   (`:2262-2264`) has the same sum. It corrects itself at the next step.
2. *The position creeps.* The length of the run laid down is fixed (the under-way part of
   the interval), but its direction is the mean heading over the *whole* interval, and the
   board goes on being pegged while she rides (`:1009-1012` are before the riding test).
   As she swings to her anchor the mean heading turns and the last under-way stretch (0.7
   mile here) swings with it. That is "it went from 50° 16' N to 50° 15' N". The same
   contamination reaches the close-hauled test and the leeway allowed (`:1095`, `:1122`).
3. *The log by order at anchor would read the stream.* `_log_hove` reads `dyn.u`
   (`:1198`, `_speed_through_water` `:2378-2382`), and at anchor in a tideway `u` is the
   stream past her (`physics/integrate.py:138-157`). Nobody hove it in that session.

**A related staleness, the other way.** After lying to, the last read is "no way", and
`account_now` returns the last worked position while the read is nought (`:1090-1091`), so
the account stands still after she has filled away until the next heave: an hour in the
brig, two in a merchantman. Session 2, 504,015: "the reckoning, even freshly worked up,
hasn't moved since midnight ... It seems the run isn't counted once she's been hove to, even
after filling away"; 505,815: "The reckoning has caught up". And her drift while hove to is
never counted (`HOVE_TO_WAY_KN`, `:141`; by design, `:1160-1162`: "her drift hove to is the
set he does not know"). That, and not the lunar, is the likeliest cause of session 8's
account lying some miles south of her after a night hove to (my reading of the bearings at
her landfall, 101,676 to 106,699; the longitude the captain had restored proved about right).

**Fix (S).** Use `_hours_under_way` in `since_noon_reading` and `no_noon_words`; do not peg
the board (nor count close-hauled ticks, nor sum the leeway) on a tick that is riding or hove
to; and have the master heave the log, or judge her way by eye (`_speed_by_eye_kn`,
`:1167-1170`), at `ship.filled_away`, `ship.under_way` and `ship.hove_to`. Risk: the second
and third change the account in every pinned passage that heaves to (the 5b passages bring
her to for the deep-sea lead), so digests and probably ticks move.

---

## J. Lead standing orders fighting for hands

**Verdict: PARTLY.** Casts are never made in parallel. A second `heave the lead` is accepted
and queued behind the first, and the line about hands is said when its turn comes and the
watch is busy. The "fight" is with the trimming, not between leadsmen.

**The code.** `Navigation.heave_lead` (`reckoning.py:1215-1228`) starts the evolution
`heave_lead` on the subject `her`. The file wants two able hands for 75 seconds
(`data/evolutions/heave_lead.yaml`). The log, the lead, the deep-sea lead and the lunar all
hold `her` (`reckoning.py:917`, `:1188`, `:1228`, `:1959`). In `Runner.start`
(`evolutions/runner.py:320-331`):

```
320        blockers = [
321            other for other in self.instances if other.holds & inst.holds and other is not inst
322        ]
323        if blockers:
...
326            self.instances.append(inst)
```

the newcomer is appended and waits its turn; no limit, no merging. When the first is done,
`_start_waiting` begins it (`:690-709`), and `_take_hands` (`:961-996`), if two able hands
are not free, logs notable: "Not hands enough on deck to heave lead; the watch is ..."
(`_waiting_line`, `:1015-1028`). The standing runtime holds a rule back while *its own* last
firing is still queued (`standing/runtime.py:254-264`, "held; the last firing's work is
still waiting its turn") but knows nothing of another rule's cast.

**The log.** Session 4 had three such rules. 200,467: "By standing order 'close lead':
heaving the lead"; 200,513: "By standing order 'inshore lead': heaving the lead", 46 seconds
later, queued behind it; 200,544: "Not hands enough on deck to heave lead; the watch is
trimming the foresail, the mainsail and the fore staysail and at other work"; 200,551: "A
hand into the chains with the lead." Every such line in the eight sessions (fourteen of
them) names sail work (bracing, trimming, setting, furling) or the boat as what the watch
is at; none can name another cast, since the one before it has finished by the time the
next one asks for hands. And because a lunar holds the same subject for a quarter of an
hour, a cast ordered during one waits for it (P1 found this at ticks 3,314 to 4,023).

**The sensible rule (S).** One cast in hand at a time: a `heave the lead` given while a cast
of the same lead is in hand or waiting is answered "the lead is going already" and not
queued; from a standing order that is a quiet "held". The lunar and the log should not hold
the leadsman's subject. Risk: the 5b books have two lead rules ("lead going" every glass and
"lead going in" every ten minutes, `gate-5b-passage.orders:42-50`) which coincide on the
glass. Today that is two casts, each a draw from the `reckoning` stream (`:1257`). Merging
them removes a draw, every later draw shifts, and the passages' ticks and digests move.

---

## K. Found in passing

1. **`the port` reads the truth.** `Ports.port_words` (`ports.py:976-1018`): `pos =
   self.world.position`, then "{port}, {spot} bearing {point}, {d_spot:.1f} miles" (`:994-
   1000`), a true bearing and a distance to the tenth of a mile to a charted spot. It is in
   the state window and in every sample. The officers found it and used it as their
   position: "the readings put Roscoff harbour SW, 7.9 miles, and that can't come from the
   reckoning ... So the game seems to know where we truly are" (session 2, 139,853); "the
   lead and the port line must be our guide" (500,467). The primer documents the reading
   (`14-the-port.md:93`) without saying whose position it is from. Against the module's own
   rule (`reckoning.py:4-6`: the truth, "which no reading, no snapshot and no drawing
   gives"; `core/world.py:539-540`) and spec §17. Mending it (by account when not at anchor
   in the port; S) takes away the one true number the officers had near land, so it belongs
   with C and D, not before them.
2. **`the depth of water` reads the truth** (G).
3. **A bearing of a sail fixes the reckoning on her true position.** `lookout.find` returns
   a sail by her name or rig (`lookout.py:694-713`); `take_bearing` then uses
   `found.feature.position` (`reckoning.py:1394-1400`), which for a sail is the vessel's
   true place (`ships.py:682-700`). The record keeps `mark_lat_deg`, `mark_lon_deg`
   (`:1402-1411`) and `to_dict` sends them to the browser as a bearing's mark. Session 2,
   153,316: "The Roscoff pilots' boat bore W by S, a cable by estimation", and the handover
   at 156,132: "Reckoning 48°46'N 4°07'W (good to a mile; fixed by a bearing of the pilots'
   boat at 23:35)". The lookout's own header says of other sail "never her position"
   (`lookout.py:44-47`). For a pilot's boat one could argue it in the fiction (he knows
   where he is); for a stranger it is a position fix from nowhere. S: give the bearing and
   leave the account alone when the sighting is a sail.
4. **The true distance of every landmark in sight is on the wire.** `Sighting.to_dict`
   carries `distance_m` (`chart.py:384-393`); `_data` strips it for sails only
   (`lookout.py:424-433`); the snapshot's `lookout` block and each event's `data` go to the
   browser (`api/queries.py:206`; `ui/server.py:507-512`). Not shown, and not sent to
   models (`agents/tools.py:136-144`), but spec §17's "the true position is not in the
   snapshot" is not quite so.
5. **The lunar's words do not say what the master did with it** (A), and its result is an
   hour stale when applied.
6. **Soundings drawn "NaN fm"** (owner's note 6; another reader's, noted since I met it):
   `client/map.js:450` divides by `U.FATHOM`, which `client/units.js` does not export.
7. **Stale comments in two port files:** `roscoff.yaml:81-82` and `st-marys.yaml:78` say the
   `vessel:` block is "not yet" read; `ports.py:638-640` reads it.
8. **A merchantman's dead reckoning in pilot waters runs on a two-hourly log**
   (`reckoning.py:146-147`, `:992-999`), so between bearings the account moves at a speed up
   to two hours old.

---

## Documents against code, in one list

| Document | Says | Code |
|---|---|---|
| Spec §13 `TechnicalSpec-M5.md:290-294`; study §3 `Navigation1805.md:278-282` | each observation a Kalman update | a line after two miles' run replaces outright (`reckoning.py:696-708`); stated only in the module and `TuningNotes.md:813` |
| Primer `12-the-longitude.md:62` | believing a lunar is the captain's judgement | the master replaces the longitude and the line does not say so |
| `TuningNotes.md:1064` | the estimate "held while she makes under a knot" | held for a mile of run at any speed and any range (`lookout.py:381-384`); primer 12:99 states the mile |
| `lookout.py:44-47`; primer `15-other-sail.md:29` | "never her position" | a bearing of a sail uses and stores it (K.3) |
| `reckoning.py:4-6`; `core/world.py:538-541`; spec §17 `TechnicalSpec-M5.md:396-398` | no reading and no snapshot gives the truth | `the port`, `the depth of water` (K.1, G); landmarks' true distances and a sail's true place on the wire (K.3, K.4) |
| Spec §16 `:385` | no tide readout, ever | a cast less `the depth of water` is the tide |
| `ports.py:817`; primer `14-the-port.md:100` | "took charge of her"; "where he takes her" | he takes her nowhere; primer `14:75` says so |
| Primer `12-the-longitude.md:95`; `reckoning.py:1649` | the pilot "is the better answer" to a course toward a rock | the pilot says nothing of it |
| `chart.py:433` | "N fathoms of water by the chart" | depth plus tide |

---

## A suggested order, by effect for the size

| # | Change | Where | Size | Pinned digests |
|---|---|---|---|---|
| 1 | Judge the distance afresh at a tenth's change; sails by their own distance | `lookout.py:362-386` | S | re-measure all with land or a cutter |
| 2 | The anchor's place from the ship's | `core/world.py:578-584` | S | 5c merchant; 5b little or none |
| 3 | The pilot vessel closes with the ship and closes again | `ships.py:563-578`, `ports.py:717-742` | S | pilot ticks may move |
| 4 | The lunar blended unless better, said in the line, carried forward | `reckoning.py:1989-2026`, `:675-739` | S | none |
| 5 | No fix from a bearing of a sail | `reckoning.py:1358-1415` | S | none |
| 6 | The shore always a sighting; `the nearest land` | `lookout.py:294-297`, `api/readings.py` | S | lines near any coast |
| 7 | Land ahead: the cast, notable then urgent | `lookout.py`, `api/readings.py` | M | lines where she stands in |
| 8 | Run since noon, the board at anchor, her way by eye after a manoeuvre | `reckoning.py:1003-1170`, `:2243-2265` | S | those that heave to |
| 9 | One cast in hand at a time | `reckoning.py:1215-1228` | S | all 5b |
| 10 | The pilot: words, inward or outward, the warning, accept or refuse | `ports.py`, `scripts.py:4584-4594`, vocabulary | S to M each | 5b and 5c pilot lines |
| 11 | The master's own bearings in pilot waters; anchor bearings; a harbour departure | `reckoning.py` | M | all |
| 12 | `the port` and `the depth of water` by the captain's means | `ports.py:976-1018`, `api/readings.py:557-566` | S, after 6 and 7 | none (readings) |

Items 1, 2, 8 and 9 each move the recorded passages; done together they cost one
re-measuring. None touches `docs/agents/ConsentBrief.md`, so the brief's hash and the
re-ask rule are not in play unless the lead chooses to describe a new reading there.
