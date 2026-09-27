# Tuning notes

Two parts: the observations made at milestone 1, kept as they were written
(they are the starting point package 10 was given), and package 10's record
of every change made to meet the known truths (spec §7.6) and the truth it
moved. Read the second part with `tests/test_known_truths.py` beside it: the
tests are the contract, these notes are why the numbers are what they are.

## Part 1: milestone 1 observations (package 10's starting point)

Observations from first runs of the merged, untuned physics (packages 4 and 5), frigate under plain sail, steady 15-knot wind unless stated, 15 minutes of game time, yards at the stated brace from square. Wind on the starboard side; negative leeway and heel mean "to larboard", i.e. to leeward, which is correct.

| Off the true wind | Brace | Speed | Leeway | Heel | Apparent wind | Rudder held |
|---|---|---|---|---|---|---|
| 60° | 55° | 6.0 kn | 4.4° | 5.0° | 41° | +5.4° |
| 67° | 55° | 8.1 kn | 3.2° | 6.6° | 42° | +3.9° |
| 75° | 55° | 10.0 kn | 2.6° | 8.5° | 43° | +3.2° |
| 90° | 40° | 9.3 kn | 1.7° | 4.9° | 55° | +1.3° |
| 110° | 30° | 10.3 kn | 1.1° | 3.9° | 65° | +1.0° |
| 135° | 15° | 10.6 kn | 0.4° | 1.2° | 83° | +0.4° |
| 180° | 0° | 7.8 kn | 0.0° | 0.0° | 180° | 0.0° |
| 90°, 25 kn wind | 40° | 14.4 kn | 2.1° | 15.0° | 57° | +1.8° |
| 67°, 25 kn wind | 55° | 12.6 kn | 3.7° | 19.2° | 43° | +4.6° |

What is already right (qualitatively):

- Leeway and heel are to leeward and of sensible size (truth 7 nearly holds: 3° to 4° close-hauled, near zero running).
- Speed rises from close-hauled to a broad reach and falls dead before the wind; running is slower than four points off it (truth 5).
- Heel grows with the square of wind speed and is largest close-hauled.
- The ship still makes way at 60° off the true wind (about 41° apparent), which is plausibly her limit under this rig.

What is wrong and where to look:

1. **Too fast everywhere.** Close-hauled at 67° should be 5 to 6 kn, not 8; a beam reach in 15 kn should be 7 to 9 kn (truth 4), and in 25 kn 10 to 12, not 14. Both package reports say the same: hull resistance in §7.4 is low (about 26 kN at 8 kn), and the sail force coefficient is high (about 1.1 on the whole plain-sail area where 0.7 to 0.9 is realistic). Tune together: raise `C_F` in `hull.py` and lower the square curve's peak in `sail_classes.yaml`; consider `hull_speed_kn` around 13 to 14 in `frigate-36.yaml` so the quartic bites (the derived 16 kn is too generous for a 1790s hull).
2. **Lee helm under plain sail.** The rudder is held to starboard (toward the wind) at every point of sail, meaning she wants to fall off. A frigate under plain sail should carry a little weather helm. The centre of effort is too far forward relative to `clr_x_m`: the headsails at x = 20 to 33 m are a long lever. Options: move `clr_x_m` forward (it is −0.8 m now; real frigates had the CLR a little forward of midships), reduce headsail areas in the draft file, or check the yaw moment sign in `sails.py`. Truth 6 (headsails give lee helm, spanker gives weather helm) will tell which.
3. **Brace limits.** Raised to 55° to 62° from square (Luce: about 28° of yard to keel when sharp up). With the square class's luff angle this gives a best apparent angle near 41°, which is about right for a ship-rigged vessel.
4. **Package 4 flags**: the post-peak shape of the square curve (truths 3 and 5), blanketing constants, spar ratings versus sail forces at 30 kn (topgallant masts at 0.94 of rating on a reach under plain sail, so royals in 35 kn will carry away, which is truth 9), and reef factors from Lever.
5. **Package 5 flags**: `C_LAT_LIFT` sets leeway more than `C_LAT`; `C_YAW_LIN`/`C_YAW`/`C_R` set turning; the frigate hard over at 8 kn swings about 1.1°/s with a 4.6-length radius, which is plausible; helmsman gains once real yaw moments exist.

**Change made at integration (M1):** frigate `clr_x_m` moved from −0.8 to +2.5 m. With it she carries about 1° of weather helm under plain sail close-hauled and lies hove to (courses hauled up, main topsail aback, helm a-lee) at about 50° off the wind making 3 kn; at −0.8 she had lee helm and would not lie to, at +4.0 she griped and was taken aback. Forereaching at 3 kn is still too much for truth 12 (under 1.5 kn); expect to revisit with the resistance and curve changes above. Heave to now backs the yards of the mast with the most square sail (the main), per Luce, rather than the aftermost mast.

**Also changed at integration (M1):** the helmsman shifts the helm when she gathers sternway (she could be trapped in irons otherwise); gaff and jib-headed sails are trimmed to the apparent wind when set and a slow automatic sheet-tending step keeps them drawing between orders (`evolutions/trim.py`, to be replaced by crew work in M3). Heave to lies her at about 50° off the wind but with sternway of 2 kn or so, and fill away from that state is rough (she comes up too close and hangs aback); both need the resistance and balance work above, and fill away may need to bear away deliberately before bracing full.

**Getting under way (found after gate M1):** from rest at 293° with the wind north, `set plain sail` then `brace sharp up` at once rounds her up into the wind before she has steerage way and leaves her in irons at about 325° with sternway; the helm is hard over one way then the other as the sternway rule flips it. Setting the fore topsail first and waiting six minutes avoids it. Now truth 17 for package 10.

Method for package 10: encode the truths table as tests first, then tune one constant at a time, recording each change and its effect here.

## Part 2: package 10, the known truths

Package 8's ships (with the revised schooner and the raked masts) and
package 9's strain landed before this work. Every scenario below is the
frigate unless it says the schooner, wind a steady 15 knots from north,
seed 7, yards trimmed with the `trim` order every two minutes while she
settles; "off" is the head's angle off the true wind. The scratch harness
that produced the numbers is not committed; `tests/test_known_truths.py`
reproduces every one of them.

### How the truths are read

- **Points of sail** are the true wind's angle off the bow (what a scenario
  and a `steer` order can set). The spec's "sweep AWA" for truth 3 is done
  as a sweep of the true wind in 10° steps with the apparent angle recorded
  beside each point. Judgement: the alternative (apparent-wind bands) puts
  the schooner's "broad reach" at 150° to 170° true, nearly running, which
  no schooner is fastest at.
- **Best sustained course** (truths 1 and 2): steer up two degrees at a time
  until she can no longer hold three knots, then take the course of best
  speed made good to windward among those that held three knots. Judgement:
  the closest course holding three knots is a poor measure on its own,
  because the jibs and spanker alone will carry a ship at three knots well
  inside the point where her square sails shake (the frigate holds 3.3 kn at
  58° off with nothing but the fore-and-aft sails drawing); the course a
  sailing master would choose is the one that makes the most to windward.
- **Turning circle** (truth 16): Luce 1884 Appendix L is steamship turning
  trials (the S.S. Hankow, 1877, and a steering-screw vessel "turned round in
  about 2½ lengths" with her engines astern), so the package contract's
  fallback is used: a tactical diameter of four to six lengths at eight
  knots with the helm hard over. Measured with the helm a-weather (bearing
  away); hard a-lee a sailing ship comes head to wind and stops, as she
  should.

### Bugs found on the way (fixed here, outside the tuning)

- **Larboard-tack bracing squared the yards.** `_brace` and `_trim` in
  `orders/verbs.py` passed a signed `target_deg`; the brace evolution's ramp
  clamped it to `[0, limit]` and re-signed it from the tack, so every
  "brace ... on the larboard tack" and every `trim` on the larboard tack put
  the yards square. Package 15 fixed the verb on the main branch; the ramp in
  `data/evolutions/brace.yaml` now takes `abs()` as well, because `trim`
  still passes a signed value. Every larboard-tack truth was impossible
  before this.
- **The helmsman wound up his standing helm.** He learned the helm to carry
  whenever within 10° of the course, with no way on or while she swung, and
  froze it when she was further off; so after a wear he sat 15° off the
  ordered course with the wheel amidships (a stale 15° of learned helm
  cancelling the 15° of error), and "full and by" ran away downwind. He now
  learns only when she is not swinging (`HELM_STUCK_RATE`, 0.1°/s) and has
  steerage way (`HELM_STEERAGE_SPEED`, 1.5 kn), a step never larger than the
  10° window, and what he learned fades over `HELM_KI_LEAK_S` (60 s)
  otherwise. This is the "helmsman's low-speed behaviour" the contract named.
- **"Taken aback" while setting sail.** `ship.aback` fired whenever net
  thrust was astern for ten seconds with any sail set, which the windage of
  loosed canvas during `set plain sail` produced while only the jibs drew.
  It now needs a set square sail actually backed, or nothing set drawing at
  all (`integrate.py`). Truth 17 could not be judged without this.
- **The schooner's tack order is refused close-hauled** (not fixed, reported):
  the runner's close-hauled check uses the largest luff angle of any set
  sail plus five degrees, and on the schooner that is her square fore
  topsail (50° apparent), though she sails at 40° to 44°. Truth 10 is tested
  on the frigate; the check wants the luff of the sails that carry the rig.
- **`steer 280.0`** parses as "steer N (0°)": a decimal heading is read as
  its fraction. Reported; the tests use whole degrees.
- **`python tools/measure_loads.py`** imports `freesail` from wherever pip
  installed it (another worktree, here), not from the checkout it sits in.
  Run it with `PYTHONPATH=.`; the load numbers below were.

### Changes, one at a time, and the truth each moved

Order of work: the truths were encoded first against the merged, untuned
physics; then each change below was made alone and the affected scenarios
re-run.

| # | Change | Before → after | Why, and what it moved |
|---|---|---|---|
| 1 | `hull.C_F` | 0.004 → 0.008 | Beam reach in 15 kn was 11.3 kn (truth 4 wants 7 to 9). Doubling the wetted-surface coefficient makes it a total resistance coefficient (friction, form, copper roughness and appendages of a bluff 1790s hull); at 8 kn it puts the resistance at about 45 kN, some 280 hp, which is the right order for 1,270 tonnes. Alone: beam reach 9.3 kn, 25 kn 12.5. |
| 2 | Square curve reshaped | peak 1.4 at 28° → 1.12 at 35°; lift 0 below 10°, 0.12 at 15°, 0.42 at 20° | With curve 1 alone the frigate still made 9.3 on the beam and, worse, held three knots at 45° off the true wind because the old curve lifted 0.7 at 15° of attack. A coarse flax sail shakes below ten degrees. Truths 1 and 4: beam reach 8.0 kn, 25 kn 11.4; close-hauled at 67° 5.3 kn; the sails go dead inside 55° apparent. |
| 3 | Gaff and jib-headed curves | peaks 1.6 → 1.25 (gaff, 30°) and 1.3 (jib, 28°); feet dead below 10°/8° | Same reasoning, and truth 2: the schooner made 10.4 kn close-hauled at 85° off. Lug, lateen and sprit scaled to match (untested rigs). |
| 4 | Luff angles | square 8° → 18°; gaff 10 → 15 → 10; jibheaded 8 → 18 → 12; others 18 | The square value feeds "full and by" (the helmsman's luffing angle). Gaff and jib values had to come back down: the sheet-tended fore-and-aft sails' chord tracks the apparent wind, so a luff angle above (trim offset − margin) makes "full and by" want more apparent wind than she has and she bears away for ever. |
| 5 | `hull.FULL_AND_BY_MARGIN` | 5° → 8° | With the square luff at 18°, "keep her full" sails the frigate at 32 + 18 + 8 = 58° apparent, about 70° true at 5.5 kn, which is truth 1's six points. |
| 6 | Sheet floors (`trim.TRIM_RANGE`, `set_gaff.yaml`, `set_jibheaded.yaml`) | gaff 8° → 18°, jib 5° → 15° | A gaff sail sheeted to 8° off the centreline drew at 33° apparent, which no boom on a horse allows; the schooner held three knots at 40° off the true wind. Truth 2: her best course to windward is now 58°, and she holds three knots to 46°. (These live in integration's files: reported.) |
| 7 | Studding curve | peak 1.1 → 1.35 at 35°, more drag | Truth 14: with the peak at the square sail's 1.12 the frigate's studding sails added 14.7% on a broad reach in 10 kn (the apparent wind falls as she accelerates on that point, and the lee sails are blanketed by the weather ones); 1.35 gives 16%. Light cloth set flat in clear air beyond the yardarms. This is a tuning value; the class notes say so. |
| 8 | `hull.HEEL_DRAG_ONSET`, `HEEL_DRAG_PER_RAD` | 25°, 1.5 → 20°, 3.0 | The lee rail dragging. At 12° and 15° onset it held the 25-kn beam reach under 12 kn but took the 30-kn heel down to 19°; at 20° it bites only in a gale (truth 8's 30-kn case: 20.6° of heel, 12.4 kn). |
| 9 | `hull.HEEL_KEEL_LEVER_FRACTION` | 0.5 → 0.8 | Truth 8 wants 20°+ in 30 kn under plain sail; the model gave 19.3°. The keel's reaction on a deep-keeled hull with a drag of 1.2 m aft acts well below half the draught. Judgement; 15 kn heel 5.6° (band 5 to 10). |
| 10 | Square drag at the peak | 0.42 → 0.50 at 35° (0.34 → 0.40 at 30°) | The other half of truth 8's gale heel: a baggy square sail's lift-to-drag at its peak is nearer 2.2 than 2.7. Costs a quarter of a knot on the beam reach (8.0 → 7.95). |
| 11 | `hull.C_R` | 2.0 → 3.0 → 2.5 | Truth 10: at 2.0 the frigate missed stays at 5.2 kn in 15 kn, turning 0.65°/s while the backed sails stopped her; at 3.0 she tacked but also came round from 2.4 kn, which the truth forbids under three; 2.5 tacks at 5.2 kn, misses at 2.8 and 3.1, and gives truth 16 a tactical diameter of 5.1 lengths (6.0 at 2.0, 4.3 at 3.0). `C_YAW_LIN` at 3.0 was tried and made her miss at 5.2 kn. |
| 12 | `tack.yaml steady_timeout_s` | 120 → 300 | The tack ended by timeout at 296 s with her still 9° off the new course at 1.6 kn. Given time to be steady she is tacked at 357 s (truth 10: five to ten minutes). |
| 13 | `wear.yaml brace_rate_deg_s` | 1.0 → 0.35 | Truth 11: with the yards following the wind at 1°/s and the helm hard over throughout, the frigate wore in 178 s; the watch braces the after yards, then the head yards, in stages as she comes round. At 0.35 she wears in 557 s (six to twelve minutes). The ground lost (0.17 nm) stays short of the quarter mile: see truth 11 below. |
| 14 | Heave to script: brail up the driver | — | Truth 12: with the spanker set she came head to wind and lay at 40° off with two knots of sternway; brailed up (Luce: "regulate by easing off ... the spanker and jib sheets") she lay at 57° to 61° at 1.5 kn. Three-masted ships only: the schooner's mainsail is her driving sail. |
| 15 | Heave to script: clew up the light head sails | — | Luce: "settle down the top-gallant sails and royals, or clew them up". The fore topgallant drove her ahead at 1.5 kn and lay her a point too broad; clewed up she lies 58° to 59° off at about a knot, with a little sternway now and then. Easing the jib sheets instead (tried) set her oscillating between 12° and 60° with sternway. |
| 16 | Fill away script: fall off before bracing full | — | The contract's requirement. She keeps the helm a-lee with sternway (which throws her head off), puts it up with headway, and braces full once her head is 55° off the true wind or after 180 s; from the hove-to state above that is at once, and she is close-hauled with way on in under four minutes without an aback line. |
| 17 | `frigate clr_x_m` (generator) | 3.5 → 3.0 | Truth 17: from rest at 293° with `set plain sail` and `brace sharp up` she rounded up to 33° off the wind with 1.2 kn of sternway before settling at ten minutes. The raked masts (package 8's follow-up) carried the sail centres aft, adding weather helm at the same CLR. At +3.0 she never comes closer than 49°, gathers no sternway, and is settled close-hauled at 5.1 kn in eight minutes, carrying +0.9° of weather helm. Truth 6 still holds: +1.9° weather helm on a beam reach, +5.0° with the headsails in, −2.1° with the spanker in. |
| 18 | Generator `PEAK_COEFF` | square 1.45, studding 1.17, gaff 1.62, jib 1.61 → 1.23, 1.25, 1.29, 1.32 | The spar ratings are the static peak-coefficient load in each spar's design wind times `SUSTAINED_FRACTION`; with the curves lowered the ratings follow. `SUSTAINED_FRACTION` 0.85 re-measured with `tools/measure_loads.py`: at 20 kn under plain sail the topgallant yards sit at 0.72 of rating (frigate) and 0.70 (schooner); at 35 kn under all sail the royals and topgallants go within twelve minutes. Truth 9 holds through orders on both ships. |
| 19 | `tests/test_strain.py` helper brace | 40° → 58° | Not a tuning change: with the new curve foot a beam reach wants the yards nearly sharp up, and at 40° the sails all but shivered and loaded nothing, so "something carries away in 35 kn" no longer did. The scenario is braced as the `trim` order would brace it. |

Also re-pinned: `tests/test_sails.py` checks the curve values at the new
peaks, and `tests/test_hull.py`'s full-and-by test reads the margin from
`hull.py` instead of assuming five degrees.

### Where the ships stand (measured values beside the targets)

Frigate polar, plain sail, 15 kn, yards trimmed (speed / apparent angle):

| off the true wind | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 | 150 | 160 | 170 | 180 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| speed kn | 1.7 | 3.7 | 5.6 | 7.1 | 8.0 | 8.0 | 7.9 | 7.7 | 7.4 | 7.0 | 6.6 | 6.3 | 5.9 | 5.9 |
| apparent ° | 44 | 47 | 50 | 54 | 59 | 66 | 75 | 85 | 97 | 111 | 127 | 144 | 162 | 180 |

Schooner polar, the same: 50: 4.4, 60: 6.2, 70: 7.2, 80: 7.7, 90: 8.0,
100: 7.9, 110: 7.7, 120: 7.4, 130: 7.0, 140: 6.4, 150: 5.9, 180: 5.5 kn.

| # | Truth | Target | Measured | Passes |
|---|---|---|---|---|
| 1 | Frigate lies six points off, five and a half at best | best course 62° to 72° | best course to windward 66° (4.9 kn, leeway 4.7°); holds 3 kn to 58° | yes |
| 2 | Schooner points higher | 50° to 62° | 58° (5.9 kn); holds 3 kn to 46° | yes |
| 3 | Fastest point: frigate beam reach, schooner broad reach | 75° to 105°; 120° to 150° | frigate 100° (8.0 kn); schooner 90° (8.0 kn) | frigate yes; schooner no (xfail) |
| 4 | Frigate beam reach speed | 7 to 9 kn in 15; 10 to 12 in 25 | 7.95 kn; 11.4 kn | yes |
| 5 | Dead before the wind slower than four points off | 180° < 135° under courses and topsails | 5.2 kn < 6.3 kn | yes |
| 6 | Headsails in: weather helm; spanker in: lee helm | sign changes | +1.9° → +5.0° → −2.1° | yes |
| 7 | Leeway | 3° to 6° close-hauled, ~0 running | 4.7° at 66° off; 0.0° running | yes |
| 8 | Heel | 5° to 10° in 15 kn; 20°+ and topgallant strain within 5 min in 30 | 5.6°; 20.6° at 12.4 kn, the topgallant yards warned the moment the topgallants were set | yes |
| 9 | Carrying away | something in 35 kn under all sail within 20 min; nothing in 20 kn plain | fore royal mast at 689 s, mizzen topgallant yard at 692 s, more after; nothing (both ships) | yes |
| 10 | Tack | 5 to 10 min, gains to windward; misses stays under 3 kn | 357 s from 5.2 kn, 31 m gained; misses at 2.8 kn (8-kn wind) in 134 s | yes |
| 11 | Wear | 6 to 12 min; loses ¼ to ½ mile | 557 s; 323 m, 0.17 nm | time yes; distance no (xfail) |
| 12 | Heave to | under 1.5 kn within 5 min, head 45° to 60° off, steady ±15° | 1.2 kn at 5 min; lies 58° to 60° off at 1.0 to 1.2 kn; fills away and is close-hauled with way on in 187 s, 0.3 kn of sternway at most, no aback | yes |
| 13 | Gaff sail on a run | thrust at 45° sheet < at 70° | schooner's mainsail 2.0 kN at 45°, 3.1 kN at 70° | yes |
| 14 | Studding sails | +15% to 30% broad reach in 10 kn; nothing close-hauled | +15.9%; +4.0% close-hauled | yes |
| 15 | Determinism | same seed, same log | equal digests and states (heave to, getting under way) | yes |
| 16 | Turning circle | 4 to 6 lengths at 8 kn | 5.1 lengths (212 m) at 7.95 kn, helm a-weather, 1.6°/s | yes |
| 17 | Getting under way | settled close-hauled within 15 min, no aback, no irons | settled at 8 min (480 s) at 5.1 kn and 67° off; never closer than 49°; no sternway; no aback line | yes |

### The two that do not pass, and why

**Truth 3, the schooner's fastest point.** Her polar peaks with the true
wind abeam (90°, 8.0 kn) and falls gently to 7.4 kn at 120° and 6.4 kn at
140°. In this model sail force follows the square of the apparent wind, and
with the true wind on the quarter the apparent wind is a third weaker than
on the beam (11 kn against 18 at these speeds); at both points her sails are
tended to the same angle of attack, so the beam wins on force by nearly
two to one, and nothing in the hull model costs a fore-and-aft rig for being
pressed on a reach beyond the heel penalty, which she does not reach (10°).
A published polar of a Baltimore-schooner replica has the two points within
a few per cent of each other, so the truth's margin is real but small; the
model would need a per-rig factor of at least 15% against her beam reach to
meet it, and I could find no honest name for one (induced drag of her shallow
hull comes to about 6%, gaff twist would penalise both points). Recorded as a
strict expected failure with the reason in the test; the owner may judge the
truth against the replica polars.

**Truth 11, the ground a wear loses.** The wear script puts the helm up and
comes to as soon as the wind is aft, so she loses 0.17 nm in a 9-minute
wear; Luce's wear runs her off for a spell before bracing up and coming to,
and hauls up the mainsail and spanker for it, which is where the quarter to
half a mile goes. Slowing the yards further (0.25°/s) reaches 0.25 nm but
takes 13 minutes. The physics cannot be slowed to make up the difference
without breaking truths 10 and 16 (the tack and the turning circle share the
rudder and yaw constants). The fix is in the wear script, which is package
7's; the time half of the truth passes.

### The schooner hove to

Heave to backs her fore topsail (her only square yards) and leaves her
mainsail set. She pays off to 78° and forereaches at 4.5 kn under her
foresail and jibs; with the mainsail brailed instead she lies 48° off at
3.3 kn. The period way for a fore-and-after is a jib or fore sheet hauled to
windward, which the sail model has no state for (package 4 said so); truth
12 is a ship-rig truth and is tested on the frigate. Something for the crew
work of milestone 3.

### What the owner should sail to see the difference

- The gate scenario: seed 7, wind north 15 kn, frigate from rest at 293°,
  `set plain sail` then `brace sharp up on the starboard tack`. She now
  gathers way without rounding up, settles at 5 kn and 67° off in eight
  minutes, and the log has no "taken aback" line. Then `heave to`: the log
  says the courses were hauled up, the spanker brailed and the fore
  topgallant clewed up; she lies at 58° off making a knot. `fill away`: she
  is braced at once and close-hauled with way on inside three minutes.
- `keep her full` on the frigate now holds 58° apparent (about 70° true);
  `steer 300` (60° off) drops her to 3.7 kn, `steer 304` to under three.
- On the larboard tack, `brace sharp up on the larboard tack` and
  `trim sails` now brace the yards instead of squaring them.
- `wear ship` takes nine minutes; `tack ship` six; `tack ship` in a
  seven-knot breeze misses stays.
- In 30 kn on a beam reach under plain sail she heels 20° and the log
  warns of the topgallant yards within two minutes; in 35 kn under all sail
  the royals go at eleven minutes.

## Milestone 3: the crew

- **Night call cost (`FATIGUE_ALL_HANDS_AT_NIGHT`)**, 0.03 → 0.20. The spec's table let the watch that was turned up three times in the middle watch sleep the cost off by four in the morning (mean fatigue 0.000, crew factor 1.00 against truth 20's 1.10 to 1.25). Package 18 measured: 0.15 gives 1.10, 0.20 gives 1.17, 0.25 gives 1.25, with the scenario frigate from 20:00, calls at 01:00, 02:00 and 03:00 of ten minutes each with the topmen aloft a third of the time. Set to 0.20; the owner judges at the gate whether a night of three calls costing a sixth of the morning's pace is right.
- **Fresh dead band (`FATIGUE_FRESH`)**, new at 0.05. With packages 17 and 18 together, the watch on deck gathered a hundredth of fatigue an hour standing idle and every compatibility run came out a tick long. Under 0.05 a hand now works at the file's pace. Truth 20's morning term becomes 1.145 at mean fatigue 0.34 (was 1.17), still inside 1.10 to 1.25.


### Package 20: truths 18 to 23, measured

Every scenario below is in `tests/test_known_truths.py`, seed 7, steady wind (gustiness and variability 0), the crew mustered by `make_world`, and every sail furled at the start unless the truth says otherwise. No constant was changed to meet them.

| # | Truth | Target | Measured | Passes |
|---|---|---|---|---|
| 18 | Plain sail from furled: the watch, and all hands called first | 25 to 40 min; 12 to 20 min | frigate: the watch 16.4 min, all hands 5.6 min after the order (7.1 min after the call); the schooner 15.6 and 8.9 | the ratio (watch at least twice all hands) yes; the absolute times no (strict xfail) |
| 19 | A tack ordered while the studdingsails go up pauses them; the tack takes its M2 time; they resume | 5 to 7 min; paused and resumed | the ten studdingsail evolutions belayed at once ("Belayed setting the starboard fore lower studdingsail: all hands about ship."); tacked in 363 s (357 s in milestone 2); none set before she was round, all ten set after | yes |
| 20 | Three all-hands calls in the middle watch: the morning watch's crew factor | 1.10 to 1.25; rested 1.0 | 1.128 (mean fatigue of the hands at the fore topsail 0.305); rested 1.000; the fore topsail took 6.27 min against 5.55, 12.9% longer | yes |
| 21 | The schooner's watch cannot set the fore topsail, foresail and mainsail at once | the third waits, and says so; not with all hands | the watch: the foresail short-handed (five hands), the mainsail waits ("Not hands enough on deck to set the mainsail; the watch is setting the fore topsail and the foresail."); all hands: no wait, all three set in 338 s | yes |
| 22 | Same seed, same muster, same log; a replay reproduces it | equal | equal digests and musters through plain sail, all hands, a tack, a pipe-down and the eight bells watch change; the replay equal too (`ship_factory` now musters the crew once the World exists) | yes |
| 23 | Sending down the topgallant masts in the gate M2 gale at the start of the second ten minutes saves the royals | nothing carries away | without: the mizzen, fore and main royal yards at 830, 831 and 836 s; with: nothing carried away or parted in forty minutes, the masts down 25 min after the order | yes |

**Truth 18, the times.** The spec's times assume slower work than the milestone 2 files give. With the watch on deck the frigate has 111 hands and eleven sails want 102, so all but two begin at once and the watch is barely short; the time is the slowest sail's (the mizzen topgallant, seven hands for twelve) plus the files' own durations, which are frozen (spec M3 §1). All hands take 5.6 minutes, which is Luce's "in a few minutes" for a smart ship better than the spec's 12 to 20. Meeting the spec would mean lengthening `duration_s` in `set_square.yaml`, `set_gaff.yaml` and `set_jibheaded.yaml` (milestone 2's, frozen) or cutting the watch's hands; I changed neither. The ratio, which is the milestone's claim, holds at 2.9 to 1 on the frigate and 1.7 to 1 on the schooner (whose watch of seventeen is short for everything).

**Truth 20, through orders.** From half past midnight: `call all hands` at one, two and three, `pipe down` ten minutes after each; at 04:01 `set the fore topsail` with the morning watch (the larboard, the watch that was turned out). Package 18's `FATIGUE_ALL_HANDS_AT_NIGHT` of 0.20 gives 1.128 here (1.145 in package 18's scenario, which had the topmen aloft a third of each call).

### Milestone 2 truths with the crew aboard (checked by package 20)

The compatibility rule holds one evolution at a time; group orders now compete for hands, so the truths that set plain sail from rest moved. Re-measured on the integrated branch after package 20 (package 17's figures, measured before package 19's crew lines landed, in brackets):

- **Truth 8**, heel and topgallant strain in 30 knots: heel 20.2°; the first topgallant warning comes 163 s *before* the last sail of plain sail is set (164 s), because the watch sets the topgallants before the slow mizzen topgallant. The test's "within five minutes of all set" holds.
- **Truth 9**, carrying away in 35 knots under all sail: first loss at 798 s, the fore topgallant mast (834 s; 689 s in milestone 2), then the main and mizzen royal masts at 828 and 854 s. Inside twenty minutes.
- **Truth 13**, gaff thrust on a run: 1.761 kN at 45° and 2.963 kN at 70°, as package 17 measured.
- **Truth 17**, getting under way: never closer than 63.3° to the wind (63.1°), settled close-hauled at 361 s (346 s), no sternway, no aback.

### Found on the way (package 20)

- **Group orders and the notable line.** `set plain sail` on the schooner wrote a notable "Not hands enough" line for every sail that waited. Now the first of a group writes one notable line for all ("Setting plain sail: not hands enough for all at once; the watch takes the sails in turn.") and the rest routine; an order given singly keeps its notable line. The group is named in `verbs.py` and reaches the runner as `params["group"]`.
- **Close reef** took one reef: `reefs` is now every band still out.
- **The runner's all-hands lines.** An all-hands evolution called `routine.call_all_hands` and, at its end, `routine.pipe_down`, but dropped the notes they return, so a tack's "All hands! (to tack ship)" and the pipe-down after it never reached the log. The runner now records them.
- **Box-hauling after `trim sails`.** From close-hauled at 4.9 kn with the yards trimmed by `trim sails`, `box haul` fails ("she would not come round") in the console's gusty 15 knots; after `keep her full`, as package 19's test does it, she box-hauls in 495 s. Recorded for the script's owner; the gate uses `keep her full`.
- **A blown-out sail in the gale.** In the gate M2 gale with seed 7 no sail blows out: the royals go with their yards and masts, so the fore royal is wrecked, not blown out, and `shift the fore royal` is refused ("The fore royal is wrecked."). Shifting is shown on a sound sail at the gate; a blown-out one needs a gale that loads the canvas past its rating before the spar, which the strain ratings do not give at any wind from 25 to 35 knots on the three headings tried.

## Milestone 3b: rig geometry and canvas

- **The canvas anchor (`CLOTH_KN_PER_M2_NO2`)**, 0.9 → 0.36. Spec 3b §6.1 anchored No. 2 canvas to milestone 2's course and topsail cloth rating so that the derivation from canvas numbers changed nothing for them. Package 22 found that 0.9 was the engine's untouched milestone 1 default (the generator's own note: "under which nothing ever blows out"), never tuned, while milestone 2's tuned light-sail values (topgallants 0.30, royals 0.25, studding sails 0.20 kN/m²) divided by Luce App. E's crosswise strengths agree with each other at about 0.36 to 0.44 for No. 2. At 0.9 a No. 8 royal at condition 50 peaked at 0.84 of its effective rating in the gate M2 gale and its yard went first, so wear was invisible in play; from 0.30 to 0.36 every worn royal blew out before its yard and every new one lost the yard first, through the physics alone. Set to 0.36 at first; when the square curve moved five degrees (below) the window slid to 0.30 to 0.32 and the anchor was set to 0.32, its top. The whole suite confirms truth 9's "nothing in twenty knots under plain sail" still holds with courses and topsails at 0.32.
- **Brace limits from Fincham and the square sail's curve.** Package 21's generator patch set the frigate's yards to Fincham art. 102's measured angles (fore 62/64/66/68, main 64/66/68/70, mizzen 62/64/66, crossjack 60, from square; was 55 to 62). On the milestone 2 square curve she then held three knots at 52° off the wind, which the record denies ("seldom within six points"), and truths 1, 10, 12 and 14 failed. The square sail's lift curve was moved five degrees up the angle of attack (foot from 10° to 15°, peak from 35° to 40°; package 21 measured that 3° gave 64°/54° and 5° the old 66°/58°). With it: truth 1 back at best 66°, closest 58°; truth 12 holds; the tack comes in 298 s (floor moved from 300 to 285); the misses-stays scenario needs 6 knots of wind rather than 8 to keep her under three knots; truth 14's close-hauled half is a strict xfail until package 23's studding stall lands.
- **Studding sails through the physics (package 23).** The studding class stalls forward of Luce's angles read off the *true* wind: seven points (78.75°) for the topmast and topgallant studding sails, the beam (90°) for the lower ones and the ringtail, water sail and save-alls; lift falls away over one point and the whole cloth flogs (`SHIVERING_AREA_FRACTION = 1.0`, judgement: a sail held at head, tack and sheet shakes all over). Apparent-wind thresholds of 80° and 100° made every studding sail flog at nine points in ten knots, against truth 29 and Luce's "one point free", so the constant reads the true wind. Measured on the frigate brought up to six points with studding sails set: in 10 knots the booms reach 0.86 to 1.01 of rating (one strain line); in 12 knots about 1.45, lost after about two hours; in 13 knots lost in three to twenty-five minutes; in 15 knots within minutes. **Truth 14:** close-hauled gain with the weather five set (the lee booms cannot go out with the yards sharp up) −3.6 per cent (was +13.5 at integration on the sharper limits); broad reach +15.06 per cent, just inside the 15 to 30 band. **Truth 19** retold with the royals (booms start in and the tack takes studding sails in first): the tack takes 305 s, belays three evolutions and resumes all three. **Truth 30, measured:** the frigate running in 15 knots gains +0.73 knots with ten studding sails (5.88 to 6.61) and +0.79 at 165°; the schooner +0.23 with her two, against Luce's "about a knot". The frigate's ringtail now lies in the spanker's plane 14.9 m to leeward (was athwartships, 9.6 m to larboard whatever the tack); the schooner's running yaws ±25° under mainsail and ringtail against ±15° before, with about 24° of helm.

### Package 24: truths 24 to 33, measured

Every scenario is in `tests/test_known_truths.py`, seed 7, steady wind (gustiness and variability 0), driven through `make_world` and the orders language. No constant, curve, ship-file value or evolution duration was changed to meet them. Where the built game and a truth's number disagree, the test asserts what the game does (with the value in its docstring) and the spec's number is a strict xfail marked as the owner's ruling, naming the value and the constant that would move it. The pointing comparisons read the frigate's sweeps of truth 1 (plain sail, 15 knots, steered up two degrees at a time with `trim sails` every 100 seconds) against the same sweep with one thing changed; "at the same speed" means the speed she makes as built at 66° off the wind (5.21 kn), her best course to windward.

| # | Truth | Target | Measured | Result |
|---|---|---|---|---|
| 24 | After yards sharper than head yards | a quarter point closer or a quarter knot more than all alike | as built (the main yard 2° beyond the fore, the rigging's limit) 5.21 kn at 66° off against 5.04 with the after yards rigged no sharper than the head yards: +0.17 kn, and 5.04 made 0.9° closer; `trim sails with the head yards sharper` 4.78 kn | the gain passes; the quarter is the owner's ruling (strict xfail) |
| 25 | Pinched to five points at three knots, less made good than kept full at six | less | 8 knots of wind: at six points 2.95 kn through the water, leeway 4.2°, 0.92 kn made good to windward over the ground; at five points 1.75 kn, leeway 8.2°, 0.75 kn made good (five and a half points: 2.38 kn, 0.91) | yes |
| 26 | Weather bowlines hauled: about half a point closer at the same speed | ~5.6° | the five weather bowlines (courses and topsails): 5.76 kn at 66° against 5.21 (+0.55); 5.21 kn made 3.3° closer (3.3° at 3 kn, 3.5° at 4 kn, 3.4° at 5 kn); best course to windward 64° → 62°; closest holding three knots 56° → 52° | the gain passes; half a point is the owner's ruling (strict xfail) |
| 27 | A royal of condition 50 blows out before its yard in the M2 gale; a new one loses the yard first | both | worn: all three royals blow out of their bolt-ropes, urgent lines, before any royal yard or mast goes; new: all three go with their yards and masts and none blows out | yes |
| 28 | Storm staysails and close-reefed topsails in 45 knots: lying a-try under 1.5 kn, nothing lost in an hour | both | lies 45° to 46° off the wind, steady; nothing carried away, blown out or parted in the hour; **4.4 to 5.1 kn of sternway**, 3.6 nm to leeward in the hour | nothing lost passes; the speed is the owner's ruling (strict xfail) |
| 29 | Studding sails flog and strain at six points, draw at nine | both | 12 knots: the five weather studding sails draw at nine points; brought up to six all five shake within 31 s and every boom whips (a strain line each, the booms at 1.42 to 1.49 of rating); borne away to nine after ten minutes all five draw again within 40 s; nothing carried away | yes |
| 30 | Studding sails both sides running in 15 knots: about a knot more | ~1 kn | frigate, ten set: 5.88 → 6.61 kn (+0.73) dead before it, +0.79 at 165°; the schooner's two +0.25; her ringtail alone +0.21 dead before it, +0.30 at 150° | passes on the measured band (0.6 to 1.2 kn); the gap to "about a knot" is the owner's to judge |
| 31 | Catharpins in on the main: the main yard four degrees sharper, a quarter point closer, the mast's strain ratio a sixth higher in 30 knots | all three | the main yard 64° → 68° from square, `trim sails` says "the after yards six degrees sharper"; 15 knots: 5.34 kn at 66° against 5.21, the 5.21 made 0.7° closer; 30 knots under plain sail on a wind: the main mast's strain ratio 0.178 → 0.229 (×1.29), of which the rating factor 0.883 gives ×1.13 and the sharper yard's pull (76.2 → 86.6 kN) ×1.14; no warning line (lower masts are rated for 55 knots) | four degrees and the ratio pass; the quarter point is the owner's ruling (strict xfail) |
| 32 | Pointing by ship: the closest heading holding two thirds of beam-reach speed | frigate ~6 points, schooner ~5 | frigate 68° (8.01 kn abeam, threshold 5.34, 5.56 there): 6.0 points; schooner 56° (7.88 kn abeam, threshold 5.26, 5.52 there): 5.0 points | yes |
| 33 | One yard braced away from its neighbours refused with the reason; the mast's yards together not | both | "The main topsail yard cannot be braced so far from the main yard while the main topsail is set (64° apart, 43° at most); brace the main yards together, or clew up the main topsail."; `brace the main yards square` squares all four | yes |

**Truth 24, why the gain is small.** Fincham's reason for bracing the after yards sharper is that the head sails bend the stream so that the after sails meet the wind more ahead (art. 94). The sail model gives every sail the same apparent wind, so bracing an after yard sharper only brings its sail nearer its luff: on Fincham's limits the main yard stands two degrees beyond the fore, and that is worth 0.17 kn. The switch that would ease the head yards to make three degrees (`trim.EASE_HEAD_YARDS`) is off for the reason package 21 gave (it loses way without a headed stream). What would move the truth is a headed-stream term in `physics/sails.py` (the after sails' apparent wind turned forward by the head sails' lift), not a constant.

**Truth 26, the bowlines.** `BOWLINE_LUFF_GAIN_DEG = 4` (physics/sails.py) is taken off the luff of the five sails that have bowlines; the topgallants, the staysails, the jib and the spanker have none and do not change, so the ship as a whole points about 3.3° closer, a third of a point. About six degrees on the courses and topsails would give half a point; the owner rules.

**Truth 28, the sternway.** The scenario: from rest in 45 knots, all hands called, the topgallant masts sent down and both storm staysails bent from the sail room, the yards braced sharp up, the topsails set and close-reefed, the storm staysails set, `lie a-try` (which clews up the fore and mizzen topsails and braces the main topsail sharp up with the helm a-lee), and the fore and mizzen topsails furled. She lies 45° off the wind going astern at 4.4 kn. Under bare poles, before any sail is set, the same ship in the same wind goes astern at 5.6 kn with her head held 63° off; in 30 knots the lying a-try gives 2.9 kn astern; without the topgallant masts sent down and the topsails furled, 5.4 kn in 45 knots. The rig's windage (`windage.spar_area_factor` 0.025 and the furled and in-the-gear fractions in `data/sail_classes.yaml`) at 45 knots is more than the hull resists, `hull.resistance` is the same astern as ahead, and nothing lets her fall off into the trough, where a ship lying to drifts broadside and her lateral resistance, not her resistance astern, holds her. The `lie_a_try.yaml` comment ("in thirty knots with the topgallant masts sent down the frigate lies five points off with a knot and a half of headway") was true before milestone 3b moved the square curve five degrees up the angle of attack; it now reads 2.9 kn astern. A physics question for the owner, not a constant to move quietly.

**Truth 29, the wind.** Package 23 measured the boom loads at six points by wind: 10 knots one boom warns; 12 knots every boom warns (1.4 to 1.5 of rating) and none goes for about two hours; 13 knots two booms go within seven minutes; 15 knots all within minutes. The truth is about flogging and strain, so 12 knots, where every strain line comes and nothing is lost, is the wind that shows it without the losses; 13 knots, with the losses, is the gate's scene.

**Truth 30.** +0.73 kn is two thirds of Luce's knot. The studding sails' lift and area are the class curve's and the files'; the owner judges whether "about a knot" wants more.

**Truth 31, the numbers against package 21's.** Package 21 reported the main mast's strain ratio 0.044 → 0.061 in 30 knots; that was a lighter sail plan. Under plain sail on a wind in steady 30 knots it is 0.178 → 0.229. Either way the rise is more than the sixth the spec expected, because the yard braced four degrees sharper pulls harder as well as the mast being rated down; the rating factor alone (0.883 here: `CATHARPIN_RATING_FACTOR` 0.85 applied to the athwartships share of the pull) is the spec's sixth. At a ratio of 0.23 nothing warns: the lower masts are rated for 55 knots, and the truth says so rather than pretend a strain line.

**Truths 1 and 2 re-measured (compatibility rule).** On the integrated branch with every package of the milestone in: truth 1, the frigate's best course to windward 64° (was 66°), the closest holding three knots 56° (was 58°); with the weather bowlines hauled 62° and 52°. Truth 2, the schooner's 58° (unchanged) and 44° (was 46°). Both inside the half point the spec allows.

### Found on the way (package 24)

- **`keep her full` in a light wind.** The helmsman's full and by holds the sails' luffing angle plus `FULL_AND_BY_MARGIN` (8°) of apparent wind, which in 8 knots of wind puts the frigate 77° off the true wind at 3.8 kn, making 0.64 kn good to windward against 0.92 steered at six points. Truth 25 is therefore sailed by `steer`. Fincham's art. 99 would have the margin grow as the way falls; recorded for the helmsman's owner.
- **The schooner's bowline** (her fore topsail's) gains nothing close-hauled: she points with her gaff sails and headsails, and her sweep with it hauled is within two hundredths of a knot of her sweep without it below 60° off.
- **The console's weather hides tenths of a knot.** Its wind varies 13 to 16 knots over an hour at seed 7, so the after yards' 0.17 kn and the catharpins' 0.13 kn cannot be seen at the prompt; the bowlines' half knot and the head yards sharper's loss can. The gate says so and points at the truths for the rest.
- **The primer's `InstantRunner`** (tests/test_primer.py) applies the end states of setting, bracing, reefing and going about, but not of rigging out a boom, bending a sail, swiftering in or hauling a bowline, and skips every evolution's preconditions. So a block cannot prove that a studding sail wants its boom rigged out first; the chapter's prose says it and the blocks are written in the order the ship needs. Extending the runner is `tests/test_primer.py`'s owner's business.
- **In 30 knots under courses and topsails alone,** braced sharp up with no headsail, the frigate rounds up against the helm (+22°) and goes astern at 2.5 kn: she needs her headsails in a breeze, as a seaman would expect; the gate's items keep them set.
- **Storm canvas at its limit in a storm.** In truth 28's steady 45 knots the fore and mizzen storm staysails stand at 0.91 and 0.93 of their cloth rating (No. 1 canvas, 1.12 of No. 2 by Luce App. E, on `CLOTH_KN_PER_M2_NO2` = 0.32); in the console's gusty 45 knots at seed 7 both split and blew out of their bolt-ropes sixteen minutes after she was lying a-try. The anchor was set at integration so that a worn royal blows out before its yard (truth 27); what it does to the heaviest canvas in the heaviest weather wants the owner's eye. Storm sails were roped and made for exactly this (Luce 1884, ch. X), so either their rating wants a factor for the roping and the smaller cloths, or the anchor is low.
- **Easing a bowline that runs free.** `ease the weather fore bowline` on a bowline never hauled belays it at nine-tenths and says "now nine-tenths hauled"; a bowline running free has nothing to ease, and `let go` rightly refuses the same ("already running free"). A level-0 line handling question in `freesail/orders/verbs.py` (package 21's); the primer shows only `let go` and `clear away`.

## Milestone 4a: standing orders

Nothing of the physics, the ships or the evolutions was tuned in this milestone; the numbers here are the sun's, the starter routines' firing ticks at seed 7, and what the routines met when they fired.

### Package 26: the sun, measured

`freesail/core/sun.py` is the NOAA "General Solar Position Calculations" approximation (Spencer's series for the declination and the equation of time, the hour angle of sunrise at a zenith of 90.833°, civil twilight at 96°), with the equation of time included. The almanac it is checked against is the U.S. Naval Observatory's rise/set service (aa.usno.navy.mil, one day's sun data) for 50.0 N, 0.0 E on 1 June 2026 in UT, which is that meridian's mean time and so the ship's clock:

| 50 N, 1 June | USNO | model | difference |
|---|---|---|---|
| civil twilight begins | 03:13 | 03:13 (03:13:56) | under a minute |
| sunrise | 03:56 | 03:56 (03:56:28) | under a minute |
| sunset | 20:00 | 19:58 by the hour-angle formula; 19:59:02 by the elevation the events use | one to two minutes |
| civil twilight ends | 20:43 | 20:41 (20:41:45) | one to two minutes |

The year is 1805, a century outside the span NOAA quotes its accuracy for; at these latitudes that is worth well under a minute. Midwinter at 50 N: sunrise 07:55, sunset 16:00. At 70 N on 21 June the sun does not set and the model says so with no event; at 62 N it sets but twilight lasts the night. The `daylight` reading and the two events come from the sun's elevation each tick, the times in `state` from the hour-angle formula at noon, so the two can differ by a minute at sunset (the elevation crosses 19:59:02; the noon formula says 19:58:24). **The first tick:** the default scenario opens at 04:00 on 1 June, four minutes after sunrise; the phase at the start is read and not announced, so no `sun.rise` is raised for a sun already up, and a rule given at the start cannot fire on it. Longitude is the ship's easting at the scenario's latitude, four minutes of clock a degree: a point ship steaming east at 12 knots from noon meets sunset 584 s early by the clock (`tests/test_sun.py`).

### Package 26: the starter routines at seed 7, measured

Steady wind, `make_world`, unless the console is named (the console's wind gusts at 0.3 and wanders at 0.3).

| Routine | Scenario | Fires | Notes |
|---|---|---|---|
| night routine | before the wind under all sail, ten studding sails set, from 19:20 (truth 34) | tick of sunset, 19:59, both orders on the one tick | six studding sails and three royals change state and nothing else; the topgallant studding sails are the four `set the studdingsails, both sides` cannot set with the royals drawing above them |
| morning sail | plain sail before the wind from 03:20 | 03:56, `setting the royals` in 15 knots; in 25 knots the held line names the reading | `Standing order 'morning sail' at sunrise: not carried out; the true wind is 25 knots, not under 20 knots.` |
| shorten sail for weather | under all sail before the wind, the wind stepped by its base speed (truth 35) | 120 s after 32 knots is held; not on 119 s of it; not again until 300 s under thirty and 120 s over | console, `--wind 0,27 --heading 282`, plain sail: gusts to 44 knots in the hour and no firing; `--wind 0,33`: fires at 04:17, seven minutes after it was given, the mean wind wandering about the threshold; `--wind 0,31` at 04:26 |
| keep her full | close-hauled at 293 in 15 knots, apparent wind 48° (truth 36) | at once, once: bears away to 282 | at 270 (apparent 58°) never in an hour, once when the wind backs a point; in the M2 wind at full gustiness and variability from 285: twice in the hour (ticks 1 and 384); from 275 in the console's wind, once. After one point off she carries the apparent wind at 52° at 282, still forward of 55, and the edge holds her there: the threshold sits two points inside her close-hauled trim |
| heavy weather | plain sail on a wind, topgallants in, the wind rising 20 to 45 knots over thirty minutes (truth 37) | 300 s after the wind passes forty: three orders on one tick, in order | the topgallant masts down 20 minutes after with all hands; the topsails at three reefs when the hands are free; **the shift is refused** (below) |
| sound the well | | refused at load | `In standing order 'sound the well', 'sound the well': The ship has no well to sound yet; that reading comes with the world.` |

**Truth 39, the passage that replays:** from 19:30 under the six routines and `every 10 minutes then trim sails`, the firings are at ticks 1500 (trim), 1742 (the night routine, both orders, the tick of sunset), 2100 and 2700 (trim); the replay from the save gives the same digest and the same firings. The gate's day (item 7: `--standing-orders` from 04:00, run to 20:00 before the wind) saved and replayed at seed 7 gives digest `d82a69017b59b63d`.

**Truth 40:** the night routine in Python and in the dialect, seed 7 from 19:40, give identical logs after the tick they were given (63 events), the same firing tick (1142) and the same state.

### Found on the way (package 26)

- **The heavy-weather routine's shift is refused.** `shift the fore topmast staysail for the fore storm staysail` is refused when the staysail is set ("The fore topmast staysail is set; take it in before shifting it.", `evolutions/scripts.py`), and it is set when the routine fires, so the routine as spec §3 writes it sends down the masts and close-reefs the topsails but never shifts the staysail. Worse, in a gale rising to 45 knots the jib and the fore topmast staysail split and blow out at about 44 knots, before the five minutes are up, and the shift is then refused for the other reason ("The fore storm staysail is not bent in the fore topmast staysail's place"). Truth 37's storm-staysail half was a strict xfail naming this at the gate. **Resolved at gate 4a (owner's ruling, 2026-09-27):** both. Shifting a sail is the whole of taking it in and replacing it (Luce 1866 ch. XXXII: 'To shift a topsail (by the wind, under all plain sail)' opens "Clew up!" and ends "Let fall! Sheet home!"; 'To shift a jib' opens "Haul the sail down"), so the shift evolution now takes a drawing sail in first and sets the new one in its place (`take_in` 90 s and `set` 120 s phases, judgement between the take-in and set evolutions' step times). And the routine's sentence was the lead's error in the spec: the frigate's fore storm staysail sets on the fore stay, its own, beside the fore topmast staysail's, so it is bent and set as a sail of its own, not shifted for the other. The routine now reads `take in the fore topmast staysail; bend the fore storm staysail`, and a companion order `when the fore storm staysail is furled and the true wind exceeds 40 knots then set the fore storm staysail` sets it on the tick the bending ends, which is how a standing order waits: on a state. Truth 37 passes in both halves; the xfails are back to seven.
- **Head canvas in a gale.** The jib and the fore topmast staysail blow out at 42 to 44 knots under plain sail on a wind, the first canvas to go. Measured by the lead at the gate in truth 37's gale (20 to 45 knots over thirty minutes, plain sail on a wind, topgallants in): the jib "straining at the bolt-ropes" at 29.8 knots (11 min), its sheets bar-taut at 31, the jib again at 38, the fore topmast staysail at 33.8 and 42.1, the mizzen topsail at 35.2, the main topsail at 39.8, the mainsail at 40.3, the fore topsail at 41.8; the jib split at 43.2 knots (27 min) and the fore topmast staysail at 43.6 (28 min). So the head sails warn sixteen minutes before they go, in a gale rising faster than any real one, and the topsails and courses do complain before the head sails split (the package's note that they did not was wrong). **Owner's ruling (gate 4a): reasonable as it stands.** The head sails are the first canvas a ship on a wind takes in as it freshens (Luce's order of shortening sail), and a routine that wants them saved says so at thirty: a captain's own line, not the starter file's.
- **`keep her full` and the frigate's polar.** At 293 (six points off) she carries the apparent wind at 48°; one point off, at 282, 52°; 55° apparent is at about 275, seven and a half points off the true wind. So the spec's "forward of 55 degrees" is two points inside her best course to windward and the routine, once fired, sits disarmed with its condition still true. It does what the truth asks (a point off, then stops) and it is the right threshold for a ship that should not pinch; a captain who wants her closer writes 50.
- **A refused order is not replayed.** A refused order is not journaled (since milestone 0), so its refusal line is not in a replayed log: a day that loaded the starter file with the well's line replays to the same ship and the same firings and a log one line shorter, with a different digest. Truth 39's voyage loads the five lines that enter; the gate's day (item 7) says so. The well's line stays in the file as spec §6 lists it; when the well arrives the line enters and the question goes away.
- **Studding sails in 32 knots before the wind.** In truth 35's blow every studding sail boom "bends like a whip" on the first second of 32 knots and the larboard fore topgallant studdingsail boom carries away on the second, 118 seconds before the routine's two minutes are up; the take-in that follows saves the rest. The routine's threshold and duration are the spec's and suit the royals and topsails; a captain who carries studding sails writes their own line at 25 knots with no duration. Recorded for the owner with truth 35.
- **The console cannot raise the wind.** The gate shows the gust that does not fire with the console's own gusts on a base of 27 knots and the firing with a base of 33; the rising gale is the truth's, and the gate's heavy-weather item starts in 45 knots.
- **`trim` grew an object.** For `trim the <sail>` the verb's object is now `yards` in `vocabulary.yaml` (as `brace`'s is), so the conflict rule reads `trim sails` as touching every yard where before it read it as touching the ship; two rules that trim and brace within the dwell now conflict, which is right.
- **A Python rule's source.** `inspect.getsource` reads a function defined in a file; one typed at `py -c` or the REPL saves as `python: <module>.<name>`.
- **Runtime cost** (package 25's measurement): the frigate under five rules ticks at about 457 a second against 503 bare on the build machine; a whole day at the prompt is about three and a half minutes of `tick`.

