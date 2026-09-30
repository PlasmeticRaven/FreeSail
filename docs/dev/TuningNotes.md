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


## Milestone 4c: the ship sails herself

Package 29 (spec M4 §18 to §23): the weather script, compression to 300 with the hourly roll-up, auto-slow on alarm, the day saved and replayed, the performance budget. Truths 48 to 51 in `tests/test_known_truths.py`.

### Package 29: the gate's day at seed 7, measured

`data/scenarios/gate-4c-day.yaml`: the frigate from 04:00 on 1 June 1805 at 50 N, heading 135 (south-east), the M2 wind's gustiness and wander at 0.3, plain sail and the royals ordered at four; the starter routines and the captain's three for the passage (four in the first measurement, before the topgallants moved into the starter book) (`data/scenarios/gate-4c-day.orders`). The script: W 17 knots at 04:00, 18 at 14:00, 19 at 19:30; veering to WNW and 29 by 22:00, NW 36 by midnight, 45 at 01:00 and held to 03:00; easing to 26 at 05:00 and 18 at 07:00. Run to 09:00 on 2 June (104,400 ticks):

| Ship's time | Tick | What |
|---|---|---|
| 19:50:52 | 57052 | Sunset (by the sun at her easting); the night routine takes in the royals on the same tick |
| 21:43:57 | 63837 | "shorten sail for weather": the topgallants in and the topsails reefed once (the topgallants moved into this line by the owner's ruling at gate 4c; the first measurement had them as a captain's order firing on the same tick) |
| 21:58:39 | 64719 | Wind veered to WNW, a moderate gale |
| 22:56:28 | 68188 | "shorten sail for weather" again (the wind back under thirty for the dwell between): a second reef (the first measurement had a firing at 22:16 too, three reefs by midnight) |
| 23:55:46 | 71746 | Wind veered to NW |
| 00:14:25 | 72865 | The captain's "gale canvas": the jib, the spanker and the mainsail in |
| 00:38:56 | 74336 | "heavy weather": the topgallant masts sent down, the fore topmast staysail taken in, the storm staysail bent, the topsails close-reefed (two reefs were in; the first measurement had three and the close reef refused). The script's forty knots plus five minutes is 00:32 |
| 01:15:02 | 76502 | "storm staysail" sets the fore storm staysail as it is bent |
| 03:22:54 | 84174 | "heavy weather" again (the wind under forty for the dwell and over it again): all four orders refused in words, everything done already |
| 03:41:30 | 85290 | Sunrise ("morning sail" holds: the wind is 45 knots) |
| 05:55:04 | 93304 | The captain's "make sail after the gale": storm staysail in, topgallant masts up, reefs out, plain sail |
| 06:34:10 | 95650 | The captain's "topgallants again" |

Nothing blown out, carried away or parted; 79 strain warnings over the day (notable), none urgent. 480 log lines; digest `70a0be9b664f382c` at 09:00 on 2 June (the first measurement, with the topgallants a captain's order: 479 lines, `f2191f3328f1914d`). At seeds 1 and 2 the same day loses nothing either; the heavy-weather routine fires at 00:08 and 00:27 (the wind's wander about the scripted base, some four knots at variability 0.3, moves the forty-knot crossing by twenty minutes either way).

**Without the captain's orders** (four in the first measurement, three since the owner's ruling moved the topgallants into the starter book), under the starter routines alone, the day lost canvas (the first runs, heading south with the wind on the beam then the quarter): two topgallants blew out and the fore topgallant yard carried away at 35 knots in the first watch, and the mainsail, the spanker and the jib blew out at 45 in the middle watch. The starter's "shorten sail for weather" takes in the studding sails and royals and reefs once, and nothing in the starter book takes in the topgallants or the courses before forty. Heading south-east the gale comes aft and she scuds; heading south she reached across it. Truth 48 is asserted with the captain's four, and the gate report says so.

**The roll-up at 300x (truth 50):** 30 roll-ups for the 29 hours and the hour begun at 09:00 (the last "so far"); 284 routine lines summed in them; 195 lines kept as they are (172 notable, 23 routine lines of the captain's and the driver's, the book read at four). An hour at sea under standing orders rolls up to a line like "All hands up 5 times, piped down 4 times, the hands at their work (18 steps), standing orders 'shorten sail for weather' and 'topgallants' found nothing to do 5 times; 34 routine entries."

### Package 29: the performance budget, measured

Spec §20: `TICKS_PER_SECOND_HEADLESS = 3000` for the frigate under standing orders on the owner's machine. The build machine is a 2.1 GHz cloud Xeon on Python 3.11; the assumed ratio to the owner's 4090 desktop is 2.0 a core (`OWNER_TO_BUILD_RATIO`, judgement from single-thread benchmarks of the two classes of processor, to be measured at the gate), so the budget asks 1,500 here.

- **Before** (the head of package 28d): 420 ticks a second, best of seven runs of 500, the frigate under plain sail and the starter routines at 08:00 in 18 knots (package 25 measured 457 with five rules and 503 bare).
- **After**: 1,000 (best of seven, alone); 800 to 900 through the whole gate's day with its gale. On the owner's machine at the assumed ratio, 1,600 to 2,000. **The budget is not met**; truth 51 asserts the build machine's floor, `BUILD_MACHINE_FLOOR = 500` (half the measured 1,000, `BUILD_MACHINE_MARGIN = 0.5`, so four workers sharing the cores do not fail it and a return to 420 does). The lead sets the budget with the owner.

**Where the time went** (cProfile over 2,000 ticks, before): 97 per cent in the physics, `integrate.step`, of which `compute_sail_forces` (four substeps a tick) was 88 per cent. In it: the ship graph's role queries (`spar_chain`, `parent_of`, `mast_of`, `lines_of`, answered afresh 750,000 times) about a third; the apparent wind at each sail's and spar's height (57 heights a substep, each asking the wind for its speed, vector and the heading's sines) 15 per cent; the spar windage loop, the load paths, the blanketing pairs and the strain loop over 310 parts the rest. The standing orders' runtime was under one per cent with seven rules armed (9 microseconds a tick); `action_parts` re-parsing at firing is not on the path. The crew's routine is 3 per cent.

**What was made faster**, every number the same to the last bit (every digest the tests assert, and three voyages of the frigate and the schooner compared state and digest before and after):

1. The graph's role queries are memoised on the ship (`ship/graph.py`): its shape is fixed once loaded; callers get fresh lists.
2. The apparent wind is worked once a height a substep (`sails._FlowField`), the wind's direction, gust and the heading's sines read once, the shear factor kept by height, the arithmetic `Wind.vector_at_height`'s step for step; windage reads only what it needs (no angle).
3. The rig as the wind meets it is read once a tick for its four substeps (`sails._Rig`, `hold_rig`/`release_rig` in `integrate.step`): which sails draw, their reefed areas and chords, the idle canvas and spars with their windage areas, heights and levers. Nothing in these changes between substeps (the evolutions and the sheets move before them, the strain model after); a bowline is read afresh.
4. Each sail's load path (spars, sheets, halyards, braces, stay) is kept per ship; the blanketing loop reads local values; the strain loop classes each part once per ship and skips the unloaded.

Next, if the owner wants 3,000: the same exactness forbids reordering the sums, so the remaining ~200 microseconds a substep are Python's own; the ways on are fewer substeps in steady conditions (numbers change, a truth run), `numpy` over the sails (numbers change in the last bits), or a compiled core for `compute_sail_forces`. Each is a ruling, not a tuning.

### Found on the way (package 29)

- **A refused order and a query replay now.** Package 26 noted that a refused order was not journaled and so a day that read the starter file replayed to a log one line shorter (the well's refusal). The spec's "save at any tick; replay reproduces the digest" wants the log the player watched, so a save now holds `inputs`: every order in the order given, refused and queries too, and every line a driver writes (a save, a file read, the compression eased). A replay gives them again; the journal is kept as it was. A save without `inputs` replays its journal as before.
- **Auto-slow's floor is 1x** (`ALARM_SPEED`, `freesail/ui/console.py`; spec M4 open item 8 (b) offers 1 or 10). An urgent line is a sail blown out, a spar carried away or a line parted, and the next often follows within seconds of ship's time: the first run of the day blew out two topgallants and carried away the fore topgallant yard eleven seconds later. At 1x the player has the ship's own pace to see it and answer; at 10x those eleven seconds are one real second. The line in the log: "Compression eased to 1x: <the urgent line's words>." The client shows it beside the clock until the player sets the speed again.
- **Gusts in a gale.** The M2 wind's gust factor is 1.1 to 1.5 whatever the base (`physics/wind.py`), so in the day's 45 knots a gust reaches 67 knots, logged as "A gust: 67 knots". A sailor would call that high for a gale's gusts (gusts of a third over the mean are more usual); recorded for milestone 5's weather, which replaces the random wind.
- **The veer's log lines.** A scripted turn of exactly four points logs its second "Wind veered" a tick late or not at all when the interpolation leaves the turn a hair short of two points since the first line (the threshold is `>=`); a real day's wander carries it past. The tests turn five points.

### Package 29b: the gate's day again, after playtest 7's findings

The same day at seed 7 (`data/scenarios/gate-4c-day.yaml`, run to 09:00 on 2 June), with the package's changes in: all hands a pool action and only a manoeuvre belaying the sail work in hand (the owner's ruling of 2026-09-29 at gate 4c, spec M3 §3.4), the starter's "trim on a shift", the mean wind in the gust line, the grouped strain and brace lines, and sails set from the gear without loosing them aloft.

| Constant (`tests/test_known_truths.py`) | Package 29 | Package 29b | Why |
|---|---|---|---|
| `GATE_DAY_SUNSET_TICK` | 57052 | 57052 | unmoved: the sun |
| `GATE_DAY_HEAVY_WEATHER_TICK` | 74336 | 74336 | unmoved: the wind's forty knots and the five minutes |
| `GATE_DAY_TOPGALLANTS_AGAIN_TICK` | 95650 | 95650 | unmoved |
| `GATE_DAY_SHORTEN_SAIL_TICKS` (new) | 63837, 68188 (in the notes) | 63837, 65773, 68188 | the reefs are taken one topsail after another under one call with the whole deck, so the firing's work ends at 22:07 instead of 22:12; the wind is back under thirty for the five minutes' dwell before 22:16 and over it for two minutes, so the order fires again at 22:16:13 (as it did in package 29's first measurement) |
| `GATE_DAY_TRIM_ON_A_SHIFT_TICKS` (new) | none | 60148, 64720, 68248, 71749 | the new starter line: 20:42, 21:58, 22:57 and 23:55 as the wind veers from west to north-west, each a point from the wind of the firing before |

Truth 48's heavy-weather assertion moves with the third reef: at 00:38:56 the routine gives its four orders on one tick; three are carried out and "close reef the topsails" is refused in words, the topsails being close-reefed already (three reefs in by 23:22). The day still loses nothing, the heavy-weather routine still fires within a quarter of an hour of the script's forty knots plus five minutes, and she is under plain sail with no reef in by the second forenoon.

The day's digest at 09:00 on 2 June is `f9c70341c3c84f99` over 427 lines (package 29: `70a0be9b664f382c`, 480 lines). The lines fell by the grouped strain warnings: 14 lines name 68 parts' warnings where package 29's day had 79 lines, one a part. The roll-up at 300x (truth 50): 30 roll-ups for the 29 hours and the hour begun at 09:00; 298 routine lines summed in them; 129 lines kept as they are (106 notable, 23 routine lines of the captain's and the driver's). An hour now reads like "The hands at their work (30 steps), leeway nil, 2 gusts, the strongest 28 knots on a mean of 18; 39 routine entries."

Where the all-hands rule shows: at 21:43:58 the fore topsail's reef begins with 108 of the 128 hands on deck fit to go aloft, the rest taking in the three topgallants, and speeds up to the whole deck's pace as the watch below comes up and the topgallant men come down at 21:46:36; the topgallants are in eight minutes before the first reef is done, where package 29's day had them standing until 22:12. The three topsails are reefed under the one call and piped down once, at 22:07:47.

### Package 29b: fatigue recovery on the gate's day (playtest 7, finding 1)

Measured on the gate's day at seed 7, the mean fatigue of each watch every half hour (`FATIGUE_*` in `freesail/crew/routine.py`, unchanged). Package 29's day turned all hands up ten times: in the first watch the starboard watch, below, was turned up six times, because "reef the topsails" is three reefs taken one after another and the runner piped down after each and called all hands again on the same tick, and each call at night costs a hand turned out of his sleep `FATIGUE_ALL_HANDS_AT_NIGHT` (0.20). The watch below went from 0.04 to 0.99 by 23:30, kept the deck through the middle watch (its own watch) at 0.93 to 0.99, went below at four and rested at the day's rate (0.08 an hour) to 0.73 at eight, and came up for the forenoon still worn out: the watcher's "worn out by 01:00 and stayed there until morning".

The finding is that the rates were not at fault; the repeated call was. With the runner's rule of package 29b (the hands are not piped down while another all-hands evolution waits its turn, spec M3 §4.2), each firing is one call: five calls in the day, three in the first watch (one for each of the three firings). The starboard watch now reaches 0.60 (worn out) at 23:00, holds there through its middle watch on deck, falls to 0.45 (tired) by six and 0.32 by eight, and comes up for the forenoon tired (0.33 at nine), to be fresh again after its next watch below. That is the model working as the sources have it: a watch that lost its sleep in the first watch keeps its own middle watch, and gets its rest only after it.

No constant is moved. The one the sources point at is the end of the night: Luce's daily routine at sea has the watch below sleep through the morning watch until "At 6 bells, call all hands and pipe hammocks up" (Luce 1866, ch. XXXII, Daily Routine at Sea, Morning Watch, art. V), seven o'clock, where the game's night (`NIGHT_ENDS_HOUR`) ends at four. Moving it to seven was tried: the watch below would rest at the night's rate (0.12 an hour) until seven, but the same constant sets when a call costs broken sleep, and the compatibility rule (spec M3 §1: one evolution with the watch on deck takes milestone 2's time to the tick) then failed for the tack, the wear and the reef, which the default scenario starts at 04:00 with the watch below asleep. Splitting the night into the hours of sleep and the hours a call costs it is a structural change to the crew model, which this package does not make; it is recorded here for the owner. Truth 20 is unchanged (the morning watch's crew factor 1.128, measured at 04:01).

## Milestone 5a: weather systems, the glass and the sky

Package 30 (spec M5 §2, §3, §5; the study `docs/design/WeatherSystems.md`): pressure systems with fronts, seeded from a monthly climatology or scripted by the scenario; the surface wind at the ship as the base the wind's gusts and wander ride on; the glass, the tendency, the sky, the weather and the visibility as readings; the gust factor by air mass, squalls as events, the mean-reverting wander. Truths 52 to 55 and 57 in `tests/test_known_truths.py`; the mechanics in `tests/test_weather.py` and `tests/test_wind.py`.

### The constants and their sources

Every number from the study was checked against its "verified / not verified" list; those from an unverified figure, and the judgements the study does not make at all, are marked so here and in the code's comments.

| Constant | Value | Source | Verified |
|---|---|---|---|
| `SURFACE_TURN_DEG`, `SURFACE_SCALE` (`world/weather.py`) | 15°, 0.7 | W §1.3 (S8, the textbook statement: 10 to 20 degrees, about two thirds); the spec fixes the middle of each | yes |
| `GEOSTROPHIC_MS_PER_HPA_PER_100KM` | 7.2 m/s | W §1.3; checked here from the air density and the Coriolis parameter at 50 N (7.16) | yes |
| `CORIOLIS_50N` | 1.117e-4 /s | 2 × 7.292e-5 × sin 50°; the gradient-wind cap is the textbook rule (Holton) | yes |
| `WARM_FRONT_VEER_DEG`, `COLD_FRONT_VEER_DEG`, `COLD_FRONT_PRE_BACK_DEG` | 22.5°, 45°, 11.25° | W §1.3 (S7): "south to south-west" at the warm front, "veers sharply, west to north-west" at the cold, "backs a little" close ahead of it | yes, as the sequence; the points are the sequence read in points |
| `FRONT_LENGTH_KM`, `WARM_FRONT_APPROACH_KM`, `WARM_FRONT_RAIN_KM`, `WARM_FRONT_GLOOM_KM`, `COLD_FRONT_BAND_KM`, `COLD_FRONT_SHOWERS_KM`, `COLD_FRONT_VEER_FADE_KM` | 1000, 300, 200, 120, 60, 400, 400 km | judgements from the Norwegian model's proportions (S7; the study gives the sequence and no distances) | no (judgement) |
| `WARM_FRONT_TURN_DEG_PER_H`, `COLD_FRONT_TURN_DEG_PER_H` | 2, 6 °/h | judgement: a warm sector of a hundred degrees occludes in about a day (S7's life cycle) | no (judgement) |
| `BOX_HALF_KM`, `SYSTEM_REACH_KM`, `UNDER_HIGH_RADII` | 250, 900 km, 1 | W §1 (the box); the reach a judgement (a low of 500 km is felt at twice its radius) | partly |
| `HPA_PER_INCH` | 33.86 | W §3; the physical constant 33.8639 | yes |
| `GLASS_NOISE_IN` | 0.005 in | W §3 "a hundredth or two" for a glass pumping in a seaway; half a hundredth for the reading alone, the seaway's pumping being package 31's | the figure yes, the split a judgement |
| `TENDENCY_FAST_IN_PER_3H` | 0.10 in | W §1.7, "a fall of a tenth in three hours means much wind": sailing-school teaching whose period source the study could not find | **no** (unverified in the study; says so in the code) |
| `TENDENCY_STEADY_IN_PER_3H`, `TENDENCY_MIN_RECORD_H`, `SKY_NOISE_HOURS` | 0.03 in, 1 h, 4 h | judgements | no (judgement) |
| `VISIBILITY_NM` | horizon 12, a few miles 4, a mile 1, a cable 0.1 | judgement; the numbers 5b's sighting reads | no (judgement) |
| `SKY_WORDS`, `WEATHER_WORDS` | Beaufort's letters as words | W §1.6 (S19) | yes |
| `SKY_SIGNS` | a high dawn; hard-edged and oily-looking; small inky clouds; a light scud driving across; streaked and spotty clouds | Luce 1884, "The Weather, the Barometer, Laws of Storms", read in `docs/references/luce/` at line 32090 and on | yes |
| `CALM_KN` (the climatology's count) | 1 kn | judgement: a log records light airs' direction | no (judgement) |
| `GUST_FACTOR_RANGES` (`physics/wind.py`) | warm 1.10 to 1.20, neutral 1.15 to 1.30, unstable 1.20 to 1.30 | W §4 from S29 to S31 (Kramer 2013, Blaes 2013, MWL 2008: 1.21 to 1.25 over water, rising with instability); the spec's ranges, the unstable top given to squalls | the figures yes; the WMO 1.23 (S32) not reached and not relied on |
| `SQUALL_FACTOR_RANGE`, `SQUALL_VEER_POINTS` | 1.30 to 1.45; 1 to 2 points | W §4 ("the top of the range reserved for squalls", "veering the wind a point or two") | the study's recommendation |
| `SQUALL_RATE_PER_S`, `SQUALL_DURATION_S` | one an hour; 3 to 8 minutes | judgement ("their own events lasting minutes"; the study gives no rate) | no (judgement) |
| `WANDER_SPREAD_DEG`, `WANDER_TIME_CONSTANT_S` | warm 3°, neutral 5°, unstable 8°; 20 min | W §4 "5 to 10 degrees in unstable air and less in stable" (the study's judgement); the time constant a judgement | no |
| `M2_WALK_RAD_PER_SQRT_S` | 0.0002 | the M2 wind, unchanged; its docstring corrected (0.69° an hour at variability 1, not "a point an hour", W §4); retired by package 31b, every wind wandering by its air mass since | yes |
| `CLIMATOLOGY_TOLERANCE_PCT` (`tools/climatology_check.py`) | 5 | spec M5 §2 | — |
| `STRONG_BREEZE_KN`, `STRONG_GALE_KN` | 22, 41 kn | W §1.2: Ushant's 31- and 54-knot gusts at a gust factor of about 1.25 | yes (the counts); the conversion the study's |
| `GALE_DAYS_BAND` (`tests/test_known_truths.py`) | 0.2 to 1.0 of Ushant's | judgement: the station is on a cliff and reads high for the open sea (W §1.2) | no (judgement) |

`data/weather/climatology.yaml`, every row: the direction shares (W and E from the 1750 to 1854 row, S and N from the 1795 to 1815 row) and Ushant's gust-day counts are the study's (S1, S4, verified); the lows a month are the study's guess ("six to eight in winter, three to four in summer", unverified); the speeds and central pressures are W §1.3's classes (S9); the tracks, radii, lives, the highs' probability, bearing, distance, strength and life, the background pressure by month and the mean gradient are judgements set so that the check passes. The file says `provisional: true`, and spec M5 §33 item 1 stands: the *Channel Pilot*'s tables replace it when the owner has a printed copy.

### The seeding, measured

`tools/climatology_check.py --months 1000 --seed 7` (8 seconds), the wind read hourly at the box's centre, a day's prevailing quarter the plurality of its hours when it holds at least half:

| Month | W | (table) | E | (table) | S | (table) | N | (table) | none | strong-breeze days | (Ushant 31-kn gusts) | strong-gale days | (Ushant 54-kn) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| January | 33.2 | 29 | 19.7 | 22 | 26.6 | 25 | 12.7 | 17 | 7.7 | 10.8 | 23.6 | 3.1 | 4.5 |
| June | 36.5 | 33 | 19.7 | 15 | 23.1 | 16 | 13.7 | 14 | 7.0 | 2.2 | 7.0 | 0.1 | 0.2 |
| October | 35.9 | 34 | 18.6 | 19 | 26.7 | 26 | 10.9 | 17 | 7.9 | 6.2 | 16.0 | 0.7 | 1.2 |

All twelve months are within five points on W and E (truth 53); the easterly runs 13 to 15 in high summer and 20 to 21 in late winter. Three things the first pass shows and the second pass (the *Channel Pilot*, or the CLIWOC extraction of W §1.5) should settle: the north quarter is four to eight points short in most months (the lows' cold sectors give north-westerlies that fall on the W quarter's edge at 315°); the strong-breeze days are about half of Ushant's in winter and a quarter in summer, which a cliff-top station reading high for the open sea can explain in part but not whole, and deeper or more frequent winter lows would close it; and a day with no prevailing quarter is seven or eight per cent against the study's "some ten per cent", by a counting rule (plurality of at least half the hours, light airs under a knot excluded) that the study does not give.

How it was arrived at: the bells alone left the field flat between lows (half of January's hours under five knots, six days in ten with no prevailing quarter); the mean flow the box sits on, between the Azores high and the Icelandic low, was added as a monthly gradient, which alone gave a westerly on eight days in ten; the shares of the table are nearly uniform across the four quarters, so the large-scale pattern is carried by a high present most of the time at a broad, seasonal bearing (the Azores ridge to the south-west in summer, the Scandinavian high to the north in winter and spring), with a light gradient (about a tenth of a hectopascal in a hundred kilometres) under it and the lows swinging the wind through S, W and N as they pass.

### The gate's day as a system, fitted

`data/scenarios/gate-4c-day.yaml`, the `systems` beside the pinned `wind`: the background 1015 hPa with half a hectopascal in a hundred kilometres toward the south (a westerly of five knots); "the low" of 420 km radius from the previous noon at (20, 920) km and 1004 hPa, at (150, 800) and 998 at four, (250, 700) and 990 at seven in the evening, (330, 540) and 980 at ten, (400, 400) and 968 at one in the morning, (520, 370) and 968 at three, (720, 320) and 978 at five, (950, 280) and 988 at seven; its fronts at 207° and 56° from the centre at the first waypoint; "the old ridge" over Biscay at the previous noon, 1022 hPa, gone east over France by the morning; "the ridge" from the Atlantic, 1024 to 1026 hPa, from midnight. Read hourly at the ship's start, beside the pinned wind:

| Ship's time | The systems' wind | The pinned wind | Sector | The glass |
|---|---|---|---|---|
| 12:00, 31 May | W by S 14 kn | (before the day) | under the old ridge | 30.17 |
| 15:00 to 22:00, 31 May | W by S to WSW, 15 to 16 kn, backing a point; rain from five | | ahead of the warm front | 30.14 falling to 30.07 |
| 22:15, 31 May | veers two points to W | | the warm front | |
| 04:00, 1 June | W 18 kn | W 17 kn | the warm sector, hazy, drizzle | 30.02 |
| 14:00 | W by N 19 kn | W 18 kn | the warm sector | 29.97 |
| 19:00 | W by N 26 kn | W 19 kn | the warm sector | 29.90 |
| 22:00 | W by N 38 kn, veering to NNW; squally | WNW 29 kn | the cold front | 29.72 |
| 00:00, 2 June | NW 45 kn | NW 36 kn | behind, unstable, passing showers | 29.57 |
| 01:00 to 03:00 | NW 48 to 46 kn | NW 45 kn | behind | 29.50 to 29.65, rising fast |
| 05:00 | NW 32 kn | NW 26 kn | behind, clear | 29.93 |
| 07:00 | NW 18 kn | NW 18 kn | open sea, then the ridge | 30.10 |

The systems' gale comes an hour or two before the pinned one and peaks three knots higher; the warm sector's wind is a point north of the pinned west (the surface turn on the bell's west-south-westerly, plus the mean flow); the glass falls slowly all day (five hundredths from four to two), faster in the evening, bottoms at one in the morning and rises two tenths by dawn, fastest in the gale, as the study asks. It does not "check" at the cold front: the pressure at the ship is the sum of bells, and the low is still deepening and approaching as the front passes; a trough along the front (which the study's option (b) allows for and this package did not build) would give the check. Recorded for the owner.

Truth 52 at seed 7, the day from the previous noon in a point ship with the day's gustiness and wander: the wind backs 18° from three in the afternoon to ten at night ahead of the warm front while the glass falls from 30.14 to 30.07; veers 23° at the front, through by eleven; holds within a point of W by N through the day (steady or falling on the glass, never falling fast); veers 33° between nine and midnight with the cold front; the first squall at 22:17 in the first watch, notable, "A squall: the wind veers a point to N by W and freshens to 61 knots, with rain", the second at 23:01; the glass from 29.52 at one to 29.82 at four, "rising fast"; 266 log lines and 94 gusts in the 45 hours.

### The M4c note on the gust factor, closed

The note ("Gusts in a gale": 1.1 to 1.5 whatever the base, so a 45-knot gale gusted to 67) is closed by spec M5 §3: over the open sea the gust factor is 1.2 to 1.25 and nearly flat with wind speed (S29 to S31), so the answer is not to ease the factor with the mean but to draw it about the air mass, with the top of the unstable range given to squalls that the log names. Under the systems the 45-knot gale gusts to 55 at most outside a squall (1.30 of the ten-minute mean, and by construction of the ten-minute mean, which the studies define the factor over) and to 65 in one. The M2 draws are kept, bit for bit, when the wind has no air mass: a fixed wind or the pinned `wind` form, which is what every truth from 1 to 51 is measured on (`tests/test_wind.py`, the regression against the old step). This is a reading of the spec's "as every truth is measured": the brief asks that truths 48 to 51 not move, and a gust factor by air mass under the pinned wind would have moved them; so with both forms in a scenario the systems supply only the sky and the glass, as the spec says, and the pinned day still gusts to 67 in its gale. The lead may rule otherwise. (The owner did, at gate 5a: package 31b brought the pinned form under the air-mass rule and retired the M2 draws with `M2_WALK_RAD_PER_SQRT_S`; the section on package 31b below has the re-measured constants.)

### The pace, measured

The gate's day from the scenario file, the frigate under the starter routines, a thousand ticks to settle and the best of three thousands (`tests/test_known_truths.py`, truth 51's measure), on the build machine with the suite running beside it: 817 ticks a second as milestone 4 ran it (the pinned wind, the systems dropped); 837 with both forms (the systems giving the sky and the glass: the systems advanced every tick and the conditions read once a minute); 781 under the systems alone (the surface wind at the ship every tick, some five microseconds a tick, and the ten-minute mean summed for the gusts). Truth 51's floor of 500 holds; the spec's "microseconds a tick" holds.

### Found on the way (package 30)

- **The curvature cap bites.** The cyclonic gradient wind at one radius from a 500-km low is three quarters of the geostrophic, so a 45-knot surface wind needs a low of about 965 hPa within 400 km, which is what a force-nine Channel gale comes with; the study's flat-isobar arithmetic (a gale at three to four hectopascals in a hundred kilometres) understates it by a quarter. The gate's day's low is 968 at its deepest.
- **The mean flow.** The study's seeding table has the lows, the highs and the easterly share but not the mean gradient the box sits on; without it the sea between systems is calm and most days have no prevailing quarter. Added as a row of the climatology, marked as the judgement it is.
- **The tendency's first hour.** A glass read once a minute has no tendency until it has an hour's record, and the reading says so ("the glass has not been watched an hour yet"); the watch's-change line says "since the morning watch" only when the day began in one.

## Milestone 5a: the sea and the ship's motion

Package 31 (spec M5 §4, §5, §6 truth 56, §7; `docs/design/ThreeDimensions.md`): the sea state as a field at the ship raised by the wind's ten-minute mean (`freesail/world/sea.py`), the ship's motion as three reduced quantities (`freesail/physics/motion.py`), the consequences each one line where it lands, the sea and the motion as readings, the day under systems alone (`data/scenarios/gate-5a-day.yaml`) and the windage under bare poles measured (M4 open item 7). Truth 56 and the day's constants in `tests/test_known_truths.py`; the mechanics in `tests/test_sea.py`, `test_strain.py`, `test_hands.py`.

### The constants and their sources

The wave-growth relations were not read from a page in this package: the Pierson-Moskowitz constants were worked here from the spectrum's published parameters, and every figure that rests on a text not in `docs/references/` says so. The period's words are Falconer's and Luce's, read in the repository's copies; the one phrase not found there is marked.

| Constant | Value | Source | Verified |
|---|---|---|---|
| `SEA_FULL_M_PER_MS2` (`world/sea.py`) | 0.0247 m per (m/s)² | the fully developed sea of Pierson and Moskowitz 1964 as WMO-No. 702 reproduces it: Hs = 4 √m0 with m0 = α U⁴ / (4 β g²), α 8.1e-3, β 0.74, gives 0.0213 U19.5², and U19.5 = 1.076 U10 by the wind model's own shear (`Wind.SHEAR_EXPONENT`) | the derivation checked here; the sources not read (unverified against the page) |
| `SEA_BUILD_HOURS`, `SEA_DECAY_HOURS` | 6 h, 4 h | a first-order lag; judgement bounded by the duration-limited growth of the Bretschneider and JONSWAP relations as textbooks give them (a sea of twenty knots fully developed in about ten hours, one of forty in a day and more) | no (judgement; the relations unverified here) |
| `SEA_PERIOD_PER_ROOT_M`, `SWELL_PERIOD_PER_ROOT_M` | 4.0, 6.0 s per √m | the developed relation is 5.0 (Tp = 0.785 U10 with Hs = 0.0247 U10², the same spectrum); a growing sea is steeper (JONSWAP's young seas near 3.6); the wind sea between them at a steepness of one in twenty-five, the swell at one in fifty-seven | the 5.0 derived; the rest judgement |
| `SWELL_DECAY_HOURS`, `SWELL_RECORD_HOURS` | 12 h, 48 h | the brief's "decaying over a day"; Falconer 1780, 'Swell' ("the fluctuating motion of the sea, which remains after the expiration of a storm"); the record two days so the swell goes by its decay | no (judgement) |
| `CROSS_SEA_POINTS` | 5 points | judgement: beyond a cold front's veer of four, so the sea a front leaves is the same water turned | no (judgement) |
| `SEA_START_SHARE` | 1 − 1/e | judgement: a scenario opens on the sea the wind would have raised in a build time | no (judgement) |
| `SMOOTH_UNDER_M`, `MODERATE_UNDER_M`, `SHORT_UNDER_M`, `HEAVY_UNDER_M`, `SWELL_FROM_M`, `SWELL_DOMINANT_RATIO` | 0.5, 1.5, 2.5, 6 m; 1 m; 1.5 | judgement, laid beside the Douglas bands the words stand where; the game never says a number (W §3, S28) | no (judgement) |
| the sea's words (`SEA_WORDS_SOURCES`) | a smooth sea, a short sea, a heavy sea, a great sea, a long swell, a heavy swell, a confused sea, a head sea | Falconer 1780, 'Sea', 'Swell', 'Trying'; Luce 1884, 'In a Gale', 'The Weather' | yes, read in `docs/references/`; "a short chopping sea" is the spec's phrase and 'chopping' is not in the repository's references (unverified) |
| `ROLL_GYRATION_OF_BEAM` (`physics/motion.py`) | 0.40 of the beam | the naval architect's rule of thumb for the roll period, T = 2πk/√(gGM) with k 0.35 to 0.40 B (the "Weiss formula", T = 0.8 B/√GM); the frigate 8.2 s, the schooner 5.8 s | no (not read from a text here) |
| `ROLL_DAMPING` | 0.20 | judgement: a bare hull's ratio is 0.05 to 0.15 in the textbooks, but a one-period model must carry the sea's spread of periods, so a magnification of two and a half at resonance; at five a moderate sea would roll her on her beam ends | no (judgement) |
| `MOTION_GAIN` | 1.27 | the highest tenth of a train's waves are 1.27 times the significant height (the Rayleigh distribution): the roll a captain names | the standard result; unverified against a page here |
| `ROLL_MAX_DEG`, `ROLL_OFF_BEAM_SHARE`, `PITCH_WAVE_LENGTHS`, `MOTION_TIME_CONSTANT_S` | 35°, 0.3, 2 lengths, 90 s | judgements: the cap; a ship rolls some with the sea astern; a ship pitches fully to waves twice her length and hardly to shorter; a dozen periods to build | no (judgement) |
| `ROLL_EASY_DEG`, `ROLL_ROLLING_DEG`, `ROLL_HEAVY_DEG`, `PITCH_EASY_DEG`, `PITCH_HEAVY_DEG` | 3°, 6°, 12°; 2°, 7° | judgement: a frigate's lee ports near the water at twelve degrees, her lee guns under at twenty; the bowsprit into it at seven | no (judgement) |
| the motion's words | easy; rolling easily, rolling, rolling heavily; pitching a little, pitching into it, pitching heavily into it (or, the sea under her stern); labouring heavily | Falconer 1780, 'Rolling', 'Sea-boat' ("without labouring heavily"), 'Sending' ("pitching precipitately into the hollow"); Luce 1884, 'In a Gale' ("labors much in a seaway", "if the pitching is hard and quick"), the boat chapter ("the ship is rolling heavily") | yes |
| `STRAIN_ROLL_PER_DEG`, `STRAIN_PITCH_PER_DEG`, `STRAIN_DEAD_BAND_DEG`, `STRAIN_FACTOR_MAX` | 0.01, 0.015 per degree; 2°; 1.4 | Luce 1884, 'In a Gale' (in a seaway the jerk of the masts carries away braces and sheets or springs the yards; forcing her through a head sea strains every mast and yard) for the direction; the figures judgement, set so the day under systems costs canvas in the gale's squalls and no spar before it (below) | the direction yes; the figures no |
| `HEAD_SEA_RESISTANCE_PER_M` | 0.10 per metre above a smooth sea, by cos² of the sea's angle on the bow | judgement bounded by the modern rules of thumb for involuntary speed loss in head seas (a tenth to a quarter for small ships at Beaufort six to seven); a three-metre head sea costs the frigate about a tenth of her speed | no (judgement; the rules unverified here) |
| `GLASS_PUMP_PER_DEG`, `GLASS_PUMP_MAX_IN` (`world/weather.py`) | 0.15 per degree of roll and pitch; 0.02 in | W §3, "a hundredth or two" in a seaway (the figure the study verified); the rate a judgement (twenty degrees of motion reaches the two hundredths) | the figure yes; the rate no |
| `SIGHT_ERROR_PER_DEG` | 0.1 per degree | N §5's "a quarter of a degree for a good master on a quiet day, a degree ... in a seaway": about three in a heavy seaway; read by nothing until 5b | no (judgement) |
| `SEAWAY_FACTOR_TABLE` (`crew/hands.py`) | (3°, 1.0, 1.0), (6°, 1.15, 1.05), (9°, 1.4, 1.15), (12°, 1.6, 1.25), (16°, 1.9, 1.35), (25°, 2.2, 1.5): roll, aloft, on deck | judgement set to truth 56 (a reef half as long again in a heavy sea); Luce 1884, 'In a Gale' for the direction; no period source gives times | no (judgement) |
| `MOTION_WORDS_HOLD_S` (`core/world.py`) | 300 s | judgement: a roll hovering about a word's threshold is not a line a minute | no (judgement) |
| the lookout's horizon (`Sea.horizon_nm`) | 2.08 √(height of eye − half the sea's height) miles | spec M5 §11 (the refracted horizon of the navigation tables); the trough a judgement; inert until 5b | the figure the spec's |

### The sea and the motion on the gate's day, measured

The day under systems alone at seed 7 (`gate-5a-day.yaml`, the frigate under the same standing orders as the pinned day, heading south-east): the sea opens as a moderate sea of 1.2 m (the wind W by N 18 knots), a short chopping sea from 05:04, a heavy sea from 20:45 (2.5 m) as the wind passes a strong breeze, a very heavy sea from 01:51 in the gale (6 m; the peak 7.6 m at four, the wind having been 45 to 48 knots from midnight to three), going down to a heavy sea at 08:22 and still a heavy sea at nine (5.2 m) with the wind a fresh breeze since seven: the sea outlasts the gale by three hours in the log's words and the heavy sea lasts into the afternoon. The motion, scudding with the sea on the starboard quarter and then right astern: rolling and rolling easily through the day (six to eight degrees, the sea on the quarter), rolling heavily from 21:57 (twelve and more), labouring heavily on and off from 22:54 to midnight as the pitch passes seven, pitching heavily with the sea under her stern from 01:04 (the sea dead astern from the north-west), labouring again at 04:15 as the ridge's wind hauls, and pitching heavily still at nine. The glass pumps to a hundredth and a half in the gale.

The model's roll at a glance (the frigate, her period 8.2 s): a fresh breeze's sea of 1.4 m on the beam, 6 degrees, "rolling easily"; a moderate gale's sea of 3.5 m, the resonant one, 23 degrees; the gale's sea of 7.6 m, 15 degrees on the beam and 5 with it astern; a day-long gale's sea of 10 m at 12.6 s, 13 degrees. The roll is greatest in the sea whose period is the ship's own and not in the highest sea, which is the driven oscillator's answer and the period's experience of a long swell.

### The day under systems, its constants

The same day as the pinned one but for the wind's cause: the systems' wind at the ship (W by N 18 through the day, a point north of the pinned west; the cold front's veer at 22:00; 45 to 48 knots from midnight to three; 18 by seven), the gust factor by air mass, squalls in the unstable air behind the front, the sea and the motion. Measured at seed 7, 29 hours, 493 lines, the digest `87c9d80a3b477233 (re-pinned 2026-09-30 when the digest began rounding floats to nine significant digits; it was 45eac662eaad0f17 before)`:

| Ship's time | Tick | What |
|---|---|---|
| 05:04 | 3840 | a short chopping sea getting up |
| 19:50 | 57039 | sunset; the night routine takes in the royals |
| 20:45 | 60300 | a heavy sea getting up |
| 21:33 | 63200 | "shorten sail for weather": the topgallants in, one reef (the systems' wind passes thirty a quarter of an hour before the pinned one) |
| 21:57 | 64620 | rolling heavily |
| 23:11 | 69115 | "gale canvas": the jib, the spanker and the mainsail in |
| 00:37 | 74245 | the heavy-weather routine, its four orders on one tick, the close reef carried out (one reef was in) |
| 01:17 | 76673 | the first squall, 65 knots: the close-reefed mizzen topsail blows out, the main topsail's larboard brace and sheet part in the minute after |
| 01:21 | 76914 | the fore storm staysail set |
| 01:51 | 78660 | a very heavy sea getting up |
| 08:14 | 101644 | "make sail after the gale" |
| 08:22 | 102120 | a heavy sea, the sea going down |

What the seaway costs, beside the pinned day's "nothing lost": the pinned day never blows a squall (its gusts are the M2 draws, 67 knots at most and short), and under the systems the squalls of the cold air are the top of the unstable range, 1.30 to 1.45 of the mean, so a 45-knot mean gusts to 65 (spec M5 §3 as built; the owner's ruling at gate 5a). Without the sea the same day blows out the mizzen topsail in the same squall; the sea's extra load on the gear (the strain factor at "pitching heavily", about 1.1) parts the main topsail's brace and sheet as well, and nothing else. With the strain factor at the first draft's figures (0.015 and 0.02 a degree, 1.6 at most) and the roll's first calibration (a damping of a tenth, the gain 1.67), the day lost the main royal mast at 19:47 in twenty knots and both topgallant yards at 21:33 while they were being taken in, which is not the day the sources describe for a ship shortening sail in time; the figures were eased to what stands, and the calibration of the roll to a fifth and 1.27, with the reasons in the table.

The starter's "topgallants again" has not fired by nine (it fired at 08:46 without the sea): the reefs come out of the topsails more slowly in the swell (the roll's table), so the ten minutes with the fore topsail unreefed had not run.

### Windage under bare poles, measured (M4 open item 7)

The frigate under bare poles from rest, a steady wind, thirty minutes (`tests/test_sea.py`, the bare-poles test):

| Wind | Running dead before it | Lying a-hull (the wind abeam, the helm a-lee) |
|---|---|---|
| 15 kn | 2.86 kn | 0.53 kn to leeward, bodily (she falls off five degrees and lies broadside) |
| 30 kn | 5.65 kn | 1.33 kn |
| 45 kn | 8.11 kn | 2.73 kn (her head falling to 68° off, a little sternway) |

Before this package the same: 2.86 knots at fifteen dead astern. The rig's windage was not moved. The arithmetic: the furled sails present 77 m² (the classes' `furled_windage` of their areas, a rolled bundle on each yard) and the bare spars with their rigging 137 m² (`spar_area_factor` 0.025 of the length squared, a yard of 24 m twelve square metres), 214 m² at a drag coefficient of one; the hull above the water, which the model does not count, would add fifty more. At fifteen knots dead astern the push is 6 kN, and the hull's resistance (`C_F` 0.008, tuned at eight knots and quadratic below it) balances 6 kN at 2.9 knots. To make a few tenths of a knot the rig would have to present a thirtieth of that area, which no frigate's did, or the hull resist thirty times more at two knots, which would move every truth under sail; the brief's own rule, that a truth under sail moving means the windage is in the wrong term, is the reason nothing was moved.

Against the sources: Luce 1884 gives no rate of drift under bare poles; his ship lying to in a gale ('In a Gale') is "drifting bodily to leeward", which is the a-hull column, and his Beaufort table ('The Weather') has a ship "going from one to two knots" in a light breeze under all sail. Steel 1794 (vol. II, 'Scudding under a fore sail, to come to an anchor', Bourdé de Villehuet's manoeuvre) has the foresail furled "at a great distance" from the berth because "the velocity of the ship will, by the violence of the wind, be but too much kept up", and the ship then runs "half a league, under bare poles, the wind being nearly aft": a mile and a half under bare poles before her way can be deadened, in a wind hard enough to anchor in. Falconer 1780, 'Scudding', has a ship "scudding under bare poles" when "the storm is excessive", flying "with amazing rapidity"; Lever 1808 has ships "lying to under bare Poles" and wearing under them. The sources describe a ship under bare poles with the wind aft as a ship with way on her, knots and not tenths, and a ship a-hull as one driven to leeward; the "few tenths" of the open item is the a-hull drift in a fresh breeze, which the model gives at half a knot. Recorded for the owner's ruling at gate 5a; if the lead rules that the running speed should fall, the honest term is the spars' shielding of one another with the wind on the axis, a fifth at most, which brings the fifteen-knot figure to about two and a half knots and no lower.

### The pace, measured

Truth 51's measure on the build machine with the suite running beside it, a thousand ticks to settle and the best of three thousands: the pinned day 884 ticks a second before this package (the code at the branch point) and 862 after (the sea is not kept under a pinned wind: the difference is the machine's); the day under systems 934 before (the file run on the branch point's code: no sea) and 843 after, the sea once a minute, the motion every tick (three exponentials), the strain's factor a multiply a part and the hull's a multiply a substep. Truth 51's floor of 500 holds on both; the spec's "microseconds a tick" holds.

### Found on the way (package 31)

- **The sea's direction.** A sea kept as a scalar with the wind's direction turns instantly with a front's veer; kept as a vector it lags, but then the old sea is counted twice against the swell record when the wind has turned across it. The wind sea is the vector's part along the wind now, the rest of the vector being what the swell record carries; a shift of the wind sees its sea die as the new one builds, and the swell is judged against the wind and not against the dying vector.
- **The motion's words flicker.** A roll hovering about six degrees said "rolling" and "rolling easily" by turns every few minutes; the words now hold five minutes before the log says they changed (`MOTION_WORDS_HOLD_S`). The sea's words do not need it: the sea moves over hours.
- **The head-sea factor in a smooth sea.** A smooth sea on the bow added a quarter of a per cent to the resistance and moved the loads at the seventh figure; the factor now counts the sea above a smooth one, so a scenario that keeps a smooth sea judges the same loads as one that keeps none.
- **The squall's veer and the cross sea.** A squall's two-point veer, on top of a front's four, took the swell across the wind at the four-point threshold and the log said a confused sea for the squall's minutes and then the sea going down and getting up again; the threshold is five points, past a front's veer.

## Milestone 5b: the geographic frame, the chart data, the queries and the lookout

Package 32 (spec M5 §9 to §12, §17's first half, §30; the study `docs/design/ChartData.md`; the study `WeatherSystems.md` §1.4 for the sea breeze and the fog). The source of every constant, and whether the source was verified.

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| `geo.EARTH_RADIUS_M` | 6,366,707 m | the sphere on which a minute of arc is the nautical mile of 1852 m (`units.NAUTICAL_MILE`; the sun's `METRES_PER_DEGREE` is sixty of them); the WGS 84 mean radius is seven parts in ten thousand more | arithmetic |
| `geo.LEAGUE_M` | 3 nautical miles | Falconer 1780, "League" | the reference text |
| `geo.HORIZON_NM_PER_ROOT_METRE` | 2.08 | spec M5 §11 and C §5.5: d = 2.08 (√h_eye + √h_object) miles, heights in metres; Bowditch's 1.17 √h(feet) is 2.12 √h(m) | the spec's figure, kept |
| `chart.AGROUND_HIGHEST_TIDE_M` | 7.0 m | the short-circuit's highest tide: Brest's spring range, about seven metres (T §1) | judgement from the study; package 34 pins it with the tide |
| `chart.AGROUND_MARGIN_M` | 2.0 m | the heel and the sea, on top of the draught | judgement |
| `chart.DANGER_SEEN_NM` | 3 miles | a rock or ledge above water made out by day | judgement |
| `chart.NIGHT_LAND_NM` | 1 mile | a dark coast seen close aboard at night in clear weather | judgement |
| `chart.TWILIGHT_FACTOR` | 0.5 | marks seen at half the day's range in twilight | judgement |
| `chart.DEFAULT_HEIGHT_M` | by kind | heights for the horizon where a feature gives none | judgement |
| `lookout.DEFAULT_HEIGHT_OF_EYE_M` | 30 m | a frigate's topmast head, for a ship without a rig | judgement |
| `lookout.LOOKOUT_REPEAT_MIN` | 30 minutes | a feature lost and found again is not hailed twice within it | judgement |
| the lights' ranges (`features/channel-west.yaml`, `range_nm`) | St Agnes 15, the Lizard 20, the Eddystone 13, the Longships 12, the Stiff 20, Saint-Mathieu 15 | White 1835 p. 13 for St Agnes ("five leagues"); the rest from the elevation and the period lamp | St Agnes verified; the rest judgements |
| `weather.SEA_BREEZE_MAX_KN` | 10 knots | W §1.4: "some 10 knots at most" (Simpson 1994, S11, not read) | the study's words |
| `weather.SEA_BREEZE_MONTHS` | May to September | W §1.4: "a summer ... wind" | judgement on the study's word |
| `weather.SEA_BREEZE_ONSET_H`, `_END_H` | 10:00, 20:00 | W §1.4: daylight, strongest in mid-afternoon, dying at dusk; the peak of the hump between them at 15:00 | judgement |
| `weather.SEA_BREEZE_FULL_KM`, `_REACH_KM` | 5, 15 km | W §1.4: "felt a few miles to sea" | judgement |
| `weather.SEA_BREEZE_GRADIENT_FREE_KN`, `_CAP_KN` | 5, 20 knots | the gradient wind that leaves the breeze alone and the one that overrides it | judgement (the study gives none) |
| `weather.FOG_CHANCE_BY_MONTH` | 1.5% to 4% | W §1.4, S10: fog west of the UK in nearly 4% of observations June to August, under 2% December to February; the months between drawn through | the two figures from the study; the curve a judgement |
| `weather.FOG_CONDITIONAL_FACTOR` | 6 | the observations' fog falls in the hours that meet the conditions, about a sixth of all hours | judgement |
| `weather.FOG_COAST_KM`, `FOG_MAX_WIND_KN` | 30 km, 12 knots | W §1.4: "near the coasts", "a fresh wind lifts it to low cloud" | judgement |
| the overrides' `datum_above_chart_datum_m` | 0.8 (Devonport), 0.6 (Falmouth), 0.7 (St Mary's), 1.0 (Brest) | mean low water springs above chart datum, from memory of the modern tide tables | unverified (C §7): the tables were not reachable |
| `build_charts.BRASSE_M` | 1.624 m | C §3.3: five pieds du roi | unverified, and unused (Faden's translation is in fathoms) |
| `build_charts.OVERRIDE_TOLERANCE_M` | 3 m | where a period depth and the modern grid disagree in open water by more, the tool prints the place | judgement |
| the world level's unit and clip | 2 m, land clipped at 50 m | measured: 40 MB at one metre unclipped, 26 MB so | measured |

### The chart data, measured

The region `channel-west` (48 to 51 N, 7 to 3 W): level 2 at 3″, 80 tiles of 512 cells, 11.9 MB compressed (83.9 MB raw with the distance field); level 3 at 0.5″, 69 tiles in four harbour patches, 5.1 MB (72 MB raw); the coast 2,593 pieces of 19,901 points, 710 KB; the features 200 entries (headland 35, rock 42, island 22, anchorage 17, light 12, place 10, bottom 9, town 8, drying 7, castle 6, church 6, shoal 6, transit 6, ledge 5, bank 4, hill 2, beacon 1, mill 1, tower 1); the overrides 7 patches in 4 files. The region on disk: 17.8 MB, under the brief's 25. The world at level 0 (2.5′), built by `--world` on the developer's machine and not committed (spec M5 §10; the lead's ruling at the merge): 150 tiles (the three all land dropped), 26.5 MB in two-metre steps with the land clipped at fifty metres (40.4 MB at one metre unclipped, 28.3 at five metres, 26.1 clipped at two). The Atlantic at level 1 is built by `--atlantic` and not committed either; the runtime reads whichever of their tiles are present under `tiles/0/` and `tiles/1/`, which git ignores, and nothing in gate 5b needs them (the passage is inside the region, which answers first). Horizontal differencing before the compression (TIFF's predictor 2, undone by a cumulative sum at load) took level 2 from 18.3 MB to 11.9 and level 3 from 10.3 to 5.1.

The build on the build machine: the region in about a minute (the distance field over 21 million cells in 1.4 s by the chamfer transform with the in-row running minimum; the coast's 57,000 segments chained and simplified in 3.5 s); the world in about twelve minutes (the eight GEBCO tiles decimated strip by strip); the fetches 5 MB for the region's GEBCO extract, 62 MB for each EMODnet variable, 4.2 GB for GEBCO's global GeoTIFF zip (15 MB/s from CEDA).

The queries on the build machine, alone: depth here 10 µs with the tile in the cache (5 to 20 ms the first time a tile is read); the grounding check 4 µs at sea (the short-circuit) and 33 µs inshore (the keel's three cells); the coast's distance and bearing 17 µs from the field; the named coast 0.4 ms (the index's search, read when the log wants a name and never every tick); a look from the masthead, once a minute, under a millisecond.

### The pace, measured

Truth 51's measure (a thousand ticks to settle, the best of three thousands) on the gate's day under systems given a position off Falmouth (49° 57′ N, 5° 00′ W) and the region, taken in one process beside the pinned day and the day under systems so that the machine's load falls on all three alike. With the sibling packages' suites running (a load of six to eight on the build machine's four cores): the pinned day 637 ticks a second, the day under systems 588, the day under systems with the region loaded 605. The region costs nothing the measure can see: the chart's cost a tick is the grounding check's short-circuit (a tile lookup) and, in the season and the hours of the sea breeze, the coast hook's field read from the weather's `surface_wind_at`, microseconds together, with the lookout once a minute. Alone, the earlier days measured 862 and 843 (package 31); the test asserts truth 51's floor of 500, which the loaded machine held at 605.

### Found on the way (package 32)

- **The study's "Imray 1848" is the 1874 edition.** The Internet Archive item's catalogue date is 1848; its title page reads 1874 and its variation note 1873. Cited as Imray 1874 throughout, and used as the study meant it, for the completeness of the dangers and transits; the period's words are White's and Faden's.
- **EMODnet's per-cell shoalest sounding is the per-tile minimum.** The DTM's `elevation_max` (the shoalest value in each 1/16′ cell) is fetched beside the mean and gives each tile's minimum depth, so the short-circuit is conservative where a rock stands in a deep cell.
- **A sea breeze in a calm.** `surface_wind_at` returned no wind at all under the exact centre of a high before the breeze was added; now a calm gradient gives the breeze alone.
- **The lookout's first look is at the start.** `what is in sight` read nothing until the first minute struck; the World now asks the lookout once at tick 0, after the log's first line.
- **A light not yet built is nothing by day.** St Anthony's lighthouse (1835) was in sight as a tower off Falmouth in 1805 until a light's `lit.from` was read for the tower too.
- **The features' positions.** Two hundred positions from memory of the modern chart and the pilots' bearings were checked against the EMODnet coast and shoalest cells and 96 moved within the rule the features file states (most under 300 m; the largest 800 m for a headland's tip); eight sunken rocks the grid cannot resolve stand where the pilot puts them and say so. The lead's review is against the sources, not the grid.
- **Crow Bar moved.** The tool's override check prints the one place a period depth and the modern grid disagree: White's three feet on Crow Bar against the modern grid's four to five metres, which is the sands moving as the study says they do.
- **The scratchpad is shared.** The build's cache lives in the session's scratchpad, which the sibling packages' sessions share; the tool's own default cache is `.cache/charts/` under the repository, ignored by git.

## Milestone 5: the cutter and the brig

### Package 32b: where the four ships stand

The cutter Sherbourne (`data/ships/cutter.yaml`, 85 tons, one mast, a running bowsprit) and the brig Harpy (`data/ships/brig.yaml`, 316 tons, the frigate less a mast), measured as the known truths measure the frigate and the schooner: plain sail in 15 knots of true wind, the yards trimmed to the wind, settled twenty minutes on each heading (`tools/measure_loads.py` for the loads; the polar and the pointing sweep of `tests/test_known_truths.py`). The frigate's and the schooner's rows were measured again on the same build, so the four are one table.

Polars, plain sail, 15 kn, yards trimmed (speed in knots):

| off the true wind | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 | 150 | 160 | 170 | 180 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| frigate | 1.9 | 4.0 | 5.9 | 7.3 | 8.0 | 7.7 | 7.7 | 7.5 | 7.3 | 6.9 | 6.6 | 6.3 | 5.9 | 5.9 |
| schooner | 4.4 | 6.2 | 7.0 | 7.5 | 7.9 | 7.9 | 7.7 | 7.4 | 6.9 | 6.4 | 5.9 | 5.7 | 5.5 | 5.5 |
| cutter | 4.0 | 5.8 | 6.5 | 7.1 | 7.3 | 7.2 | 7.1 | 6.9 | 6.5 | 6.1 | 5.7 | 5.5 | 5.5 | 5.4 |
| brig | 0.9 | 4.0 | 5.7 | 7.0 | 7.7 | 7.6 | 7.5 | 7.4 | 7.1 | 6.7 | 6.3 | 6.1 | 5.9 | 5.7 |

The same, heel and weather helm in degrees at the beam reach (90°) and close-hauled at the best course: frigate 5.9° heel, helm 1.8° at 90°; schooner 8.9°, 5.2°; cutter 6.7°, 6.8°; brig 7.8°, 1.3°. The cutter's helm runs from 0° at 60° off to 12° at 120°, the schooner's from 0° to 8°, the brig's 5° at 60° falling to 1° at 100°: the cutter carries her weather helm off the wind as her mainsail's centre moves aft with the sheet, the brig's spanker is balanced by her head sails on every point.

The centre of lateral resistance was set as the schooner's was: from the weather helm close-hauled and abeam, moving `clr_x_m` until the helm was a degree or two to weather close-hauled and stayed to weather on a reach. The cutter's at −0.2 m gave 1.0° close-hauled and 7.4° abeam; at −0.4 m (the file) 0.2° and 6.8°. The brig's at 1.5 m gave 7.3° and 3.1°, at 2.3 m 9.6° and 4.5° (moving the centre forward increases the weather helm); at 0.5 m (the file) 5.3° and 1.3°.

| # | Truth | Target | Measured | Passes |
|---|---|---|---|---|
| 73 | A cutter lies closer than a topsail schooner | best course half a point closer than the schooner's | cutter 58° (holds 3 kn to 46°); schooner 58° (to 44°): the same to the degree | no (strict xfail) |
| 74 | A brig lies as a ship does | 60° to 72°, within half a point of the frigate, less close than the schooner | brig 64° (holds 3 kn to 54°); frigate 64° (to 56°); schooner 58° | yes |
| 75 | The cutter's beam reach | 6 to 8 kn in 15, slower than the frigate, under 10° of heel | 7.3 kn; frigate 8.0; heel 6.7° | yes |
| 76 | The brig's beam reach | 7 to 9 kn in 15, within a knot of the frigate, her fastest point | 7.7 kn; frigate 8.0; fastest at 90° | yes |

The bands of 75 and 76 are judgement: the sources give no polars for either, only the rig's reputation and the hull speeds (the cutter's 9.5 kn on 50 ft of water-line, the brig's 11.5 on 88), and the bands are drawn a knot either side of what a hull of the size makes in fifteen knots on the frigate's and the schooner's scale.

**Truth 73, why it fails.** How close a ship lies is set by the lift curves of the sail classes and the trim floors in `freesail/physics/sails.py`, which the four ships share, not by anything in a ship file: the cutter's mainsail is a `gaff` sail as the schooner's is, her jib a `jibheaded` sail as the schooner's, and her one square topsail trims to the same floor. Her great mainsail and long boom give her the area (270 m² of plain sail on 106 t, against the schooner's 608 on 211) and her balance, and the sweep shows it in the speed she holds close to the wind (4.0 kn at 50° off where the frigate makes 1.9 and the brig 0.9), but not a higher-pointing sail. Meeting it wants a per-rig or per-sail pointing factor (a cutter's flat-cut mainsail, her bowsprit's length giving the jib a longer foot), which is a physics change outside this package; the truth is recorded as a strict xfail with the measured values in its reason, in `tests/test_ships_hierarchy.py`.

**Loads.** In 20 knots abeam under plain sail nothing on either ship is within half of its rating but the brig's topgallant yards (0.71) and the cutter's topsail (0.45, the cloth); in 35 knots under all sail the cutter's gaff topsail goes (1.21 of its rating) and her topsail stands at 0.94, and the brig's topgallant yards (1.64) and topgallant masts (1.26, 1.18), main topgallant staysail (1.21) and flying jib (1.06) go, as the frigate's light spars do (truth 9). The cutter's square-sail yard reaches its rating exactly (1.00) in 22 knots at 110° off under all sail: it is rated for its sail in the design wind, as every yard is, and the square sail is a sail for going free in a moderate breeze.

**Manoeuvres.** The cutter wears in 512 s and heaves to with her topsail to the mast (2.3 kn of headway at 45° off after five minutes: a cutter forereaches under her mainsail); the brig wears in 596 s once the spanker is brailed up as the helm goes up and hauled out when she is by the wind (see below), box-hauls, and heaves to with the main topsail aback, lying about 76° off the wind and forereaching at 2.4 kn where the frigate lies 60° off at 1.2: her main is her after mast and the backed topsail is on it, so she lies broader than a ship whose backed sail is amidships. None of the cutter, the schooner or the brig tacks in the real physics: each loses her way before her head comes through (the engine has no jib-sheet-to-windward state and the minimum of 0.8 kn is not enough for a small vessel's sternboard), so truth 10 stays the frigate's; the three box-haul and wear instead. Recorded, not fixed: it is in the physics of staying, not in the grammar.

### Found on the way (package 32b)

- **The driver was found by counting masts.** `after_gaff_sails` kept the driver on a vessel of fewer than three masts, so the brig heaving to came head to wind with sternway under her 162 m² spanker, and wearing she would not pay off. The driver is now found by place: the gaff sail on the aftermost lower mast when that mast carries square yards and another mast forward of it does too. The schooner's mainsail and the cutter's, on a vessel whose yards are all on one mast, stand as their driving sails.
- **Wearing, the driver hauled out too soon.** With the spanker hauled out as the wind came aft, the brig rounded up through the wind on the new tack before the helm could meet her (1.7 kn, then sternway at 40° off); it is now hauled out once she is by the wind, "By the wind. Haul out the spanker!", as Luce's sequence has it. The frigate, whose spanker is now brailed up and hauled out the same way, wears in 519 s from the same start (557 s before; truth 11's band is 6 to 12 minutes and it still passes) with the two lines added to her log.
- **`reef` of a bowsprit.** "Reef the bowsprit" went to the sail reef, which asked for a sail; it now goes with `rig out` and `rig in` to the boom evolutions, which look the spar's class up in the vocabulary's table (`reef_bowsprit`, `rig_out_bowsprit`); the frigate's and the brig's standing bowsprits are refused by the evolution ("gammoned fast to the stem").
- **A standing order's sail name.** "When the fore topsail is shaking" on the cutter, who has no fore topsail but whose foresail answers to "the fore", read as "the fore" compared "topsail shaking" and refused in those words; a part's name must now be followed by its comparison, so the unknown name is refused as unknown with the nearest suggested.
- **The log's names for the cutter's square sails.** An alias "the crossjack" for the square sail and "the main topsail" for the topsail made the log say "the crossjack" and "main topsail" for sails a cutter's people call the square sail and the topsail; an alias that begins with "the " is a name the parser takes and the log does not use, and the generator writes them so.
- **Thirty hands.** The cutter's watch is short for the larger parties (a whole watch to furl the mainsail), and the crew orders say so ("SHORT") rather than refuse; her topmen fall back to the deck stations, having no tops.
## Milestone 5a: all hands in parallel, the ship's cost, the rig's repairs, the pinned form under the air-mass rule

Package 31b (spec M3 §3.2 as revised; spec M5 §3 as revised; gate 5a's rulings, decision 28; playtest 11's findings 7 to 11 and 14). The party bound on an all-hands sail evolution and the parallel manning of a group's jobs (`crew/hands.py`, `evolutions/runner.py`); the heavy-weather routine's order of work; `reeve a new <line>` and `splice the <line>` (`reeve_line.yaml`, `scripts.ReeveScript`, `parts.Cordage`); the trim line with yards on deck; the primer's chapter 9 free of the gate's day; the pinned form under the air-mass rule, the milestone 2 draws retired. Both gate days re-measured at seed 7.

### The parties, and where they show

| Constant | Value | Source | Verified |
|---|---|---|---|
| `reef_square.yaml`, `party` | 40 | Luce 1884, ch. XVIII Organization, 'Station Billet' ("Reefing topsails: topsail buntlines, reef topsail, on deck to halliards": the yard's own topmen lay out on it) and ch. XXVII Reefing, 'Reefing and Hoisting' (the clewlines, buntlines, weather braces, halliards and reef-tackles manned on deck); the frigate's tops are 24, 30 and 14 men both watches (her ship file) | the stations yes; the number judgement: the sail's own top and about as many again on deck, so that a frigate's deck of a hundred and twenty and more mans her three topsails at once |
| `furl_all.yaml`, `party` | 182 | every yard and every lower sail manned at once: the frigate's tops (68), forecastlemen (28), afterguard (50) and waisters (36) by her ship file's stations; every man has a station for furling sail (Luce 1884, ch. XVIII), the marines and the idlers never aloft (ch. XX) | the stations yes; the sum judgement (the whole deck: it holds every sail, so nothing runs beside it) |
| `loose_sails_to_dry.yaml`, `party` | 146 | the sail loosers ("Aloft sail loosers! ... Let fall!", Luce 1884, ch. XX Port Drills): the tops, the forecastlemen and the afterguard; the waisters tend the gear on deck | judgement |

The rule (`hands.request`, `hands.top_up`): an all-hands job with a party takes at most the party from the idle hands, the subject's own top and the rating wanted first, and leaves the rest idle for the next job of the same order and then for whatever else waits; the top-up joins hands only up to the party; the numbers term is the party over the hands at it. A smaller ship's deck clamps a party (the schooner's whole company is under forty, so her reef takes her deck as before). The manoeuvres and the masts say no party and take everyone. Where it shows: the frigate at 04:20 in fifteen knots, "reef the topsails, one reef" and "take in the jib" behind it, begins the three reefs on one tick with forty hands each and the jib's take-in with the four idle hands left, and reefs the three together in six minutes and twelve seconds, the time one topsail took alone; nothing waits and nobody is over the party as the watch below comes up. Given while the watch is setting the royals, the third reef begins with twenty-two hands ("Only 22 hands to the mizzen topsail; the rest are setting the fore royal, the main royal and the mizzen royal and at other work") and is at its forty within a minute and a half. Truth 18 (plain sail, twelve-hand evolutions) and truth 19 (the tack belays the royals) do not move; the compatibility rule holds (one reef with the watch on deck: the watch's ninety-one hands aloft are more than the party, so it is at the file's pace to the tick). Truth 56's ratio (a reef half as long again in a heavy sea) holds by construction, the roll's factor multiplying the party's pace.

### The heavy-weather routine's order of work, measured

The day under systems at seed 7 with the parties in and the starter book as it stood (send down the topgallant masts; take in the fore topmast staysail; bend the fore storm staysail; close reef the topsails): the routine fires at 00:37:25; the send-down takes every idle hand and everyone who comes up, the three close reefs wait for hands ("the watch is sending down topgallant masts and taking in the fore topmast staysail"), begin when the send-down is done at 00:59, and are in at 01:19:12 to 01:19:15, eighty seconds after the first squall of the middle watch (01:17:53, 65 knots) had come on. Nothing was lost even so at seed 7 (the topsails were clewed down and being reefed as the squall struck), but the book's order left the topsails unreefed at the squall, which is what the brief asked to be measured. With the close reef first the three reefs begin at 00:37 with the deck (forty, forty and forty; the watch below's first third comes up at the call), the send-down begins short with eighteen hands and fills as the reefs are done, the close reefs are in at 00:51:19 to 00:51:43, twenty-six minutes before the squall, the masts are down and the hands piped down at 01:15, and the storm staysail is set at 01:26 (01:21 before). Nothing lost. The starter book has the close reef first; the reason is in the book's comment and in the primer's chapter 7 ("the order of an order's clauses is the order of the work"), with Luce's order of shortening sail, the reefs before the light spars come down (ch. XXVII, XXIX).

### The day under systems, re-measured

The same scenario (`gate-5a-day.yaml`), the parties in and the close reef first. 487 lines, the digest `d2c9e73c52a1e1fd`:

| Constant (`tests/test_known_truths.py`) | Package 31 | Package 31b | Why |
|---|---|---|---|
| `GATE_5A_SUNSET_TICK`, `GATE_5A_SHORTEN_SAIL_TICK`, `GATE_5A_GALE_CANVAS_TICK`, `GATE_5A_HEAVY_WEATHER_TICK`, `GATE_5A_FIRST_SQUALL_TICK` | 57039, 63200, 69115, 74245, 76673 | unmoved | the wind's and the sun's |
| `GATE_5A_CLOSE_REEFS_IN_TICK` (new) | (01:19:15, after the squall) | 75103 (00:51:43) | the close reef first, by three parties together |
| `GATE_5A_LOST` | the mizzen topsail blown out; the larboard main topsail brace and sheet parted | nothing | the squall met close-reefed topsails |
| `GATE_5A_MAKE_SAIL_TICK` | 101644 | 101624 | the fore storm staysail's set and the night's work end a little sooner, so the half hour under twenty-five knots is up twenty seconds sooner |
| `GATE_5A_TOPGALLANTS_AGAIN_TICK` (new) | not fired by nine | 103976 (08:52:56) | the reefs come out of the three topsails together, so the ten minutes with the fore topsail unreefed run before nine |
| `GATE_5A_SEA_TICKS`, "the sea going down" | 102120 (08:22) | 102360 (08:26) | the ship's track differs a little through the night (the trims and the canvas), and with it the systems' wind at her and the sea's minute |
| `GATE_5A_DAY_LINES`, `GATE_5A_DAY_DIGEST` | 493, `87c9d80a3b477233` | 487, `d2c9e73c52a1e1fd` | the three lost lines and their consequences gone, the reefs' lines together |

The day's cost in canvas: nothing. The first squall of the middle watch (65 knots on a 47-knot mean, the sea a heavy one and the ship pitching heavily with it under her stern) met the topsails close-reefed and the topgallant masts coming down; the four squalls after it, 67 knots at most, cost nothing either. The sea's words and the motion's are the day's as package 31 measured them (a heavy sea from 20:45, a very heavy sea from 01:51, still a heavy sea at nine).

### The pinned form under the air-mass rule

The milestone 2 draws (a gust factor of 1.1 to 1.5 whatever the mean, an unbounded walk of the direction) are retired: every wind is in an air mass, the systems' sector when they drive it, else neutral unless the scenario says (`Scenario.air_mass`; a pinned waypoint's `air_mass`, which holds from its moment on). The pinned gate day (`gate-4c-day.yaml`) says its air: the warm sector's by day (as the systems it also carries have the ship in the warm sector until the cold front), neutral from the front's waypoint at 22:00. Re-measured at seed 7, the parties in and the close reef first: nothing lost; 466 lines, the digest `9047a71c678421b1` (package 29b: `f9c70341c3c84f99`, 427 lines); 65 gusts, the strongest 59 knots on a mean of 46 (the M2 draws gusted the same gale to 67).

| Constant | Package 29b | Package 31b | Why |
|---|---|---|---|
| `GATE_DAY_SUNSET_TICK` | 57052 | 57052 | unmoved: the sun at her easting, her track by day the same (no trim by day in the warm sector's air) |
| `GATE_DAY_HEAVY_WEATHER_TICK` | 74336 | 74336 | unmoved: the pinned wind's forty knots and the five minutes; neutral air's gusts, 1.30 of the mean at most and half a minute long, never fill a dwell |
| `GATE_DAY_TOPGALLANTS_AGAIN_TICK` | 95650 | 95650 | unmoved |
| `GATE_DAY_SHORTEN_SAIL_TICKS` | 63837, 65773, 68188 | the same | unmoved, for the same reason |
| `GATE_DAY_TRIM_ON_A_SHIFT_TICKS` | 60148, 64720, 68248, 71749 | 55866, 56843, 59062, 64840, 66022, 68980, 77099, 78222, 80789, 82056, 82680, 87053, 98501, 98938 | the wander: the M2 walk moved the direction a fraction of a degree an hour, so the point rule fired only on the script's veers; the air-mass rule's wander is five degrees about the base in neutral air (three in the warm sector, eight in unstable air), and it carries the rule over its mark and back every twenty to forty minutes through the gale, none by day |

Truth 48's assertions stand as they were (nothing lost, the routines at the script's times, plain sail by the second forenoon), and truths 49 to 51 with them; truth 50's counts are computed, not pinned. Every other truth was checked by the whole suite: none moved but the trim-on-a-shift test of `tests/test_weather_script.py`, whose firings on a scripted veer of two points in an hour came at 13 and 60 minutes into the veer (30 and 60 under the M2 walk, its windows of three minutes); the windows are now the veer's hour with the wander allowed, the count and the steady two hours without a firing being what holds. Truth 36's hour of a wandering wind at full variability (a spread of seventeen degrees) still fires "keep her full" between one and four times.

Two forms of the pinned day were measured and not chosen, for the record. **Neutral air all day** (no waypoint says): the same ticks but the sunset's (56974: ten trims by day changed her track a little) and twenty trims in the day, 512 lines. **Unstable air behind the front** (the waypoint at 22:00 says `unstable`, the systems' own air there): eight squalls from 23:29, up to 61 knots, and nothing lost, but the starter's "heavy weather" and the captain's "gale canvas" fired at 23:34:07 on a seven-minute squall of 46 knots, an hour before the script's forty knots (00:27, so 00:32 with the dwell), "make sail after the gale" at 06:28 and "topgallants again" at 07:14, thirty trims, 552 lines. The book's five-minute dwell tells a gale from the M2 wind's gusts of half a minute; it does not tell one from a squall of three to eight minutes (`SQUALL_DURATION_S`), and on the day under systems it is seed 7's luck that the first squall came after the routines had fired. Recorded for the owner: the pinned day keeps neutral air behind its front so that truth 48 measures the script, and the squalls live on the day under systems.

### The rig's repairs: the constants

| Constant | Value | Source | Verified |
|---|---|---|---|
| `scripts.LINE_FATHOMS` | sheet 30, tack 15, halyard 40, throat halyard 30, peak halyard 40, brace 35, lift 20, clewline 30, buntline 30, bowline 25, downhaul 25, reef tackle 20, vang 15, outhaul 15 fathoms; `DEFAULT_LINE_FATHOMS` 25 | judgement from each line's lead on a frigate's rig (a topsail sheet from the clew through the yardarm sheave and the quarter block to the deck, both parts; a halyard's tye and fall; a brace's pendant and fall led aft); Steel 1794's tables of the lengths of running rigging by rate are at the end of his second volume and their figures did not survive the OCR; his note to the tables is the practice ("cut to proper lengths when reeved on board"; the fore and main tacks doubled, "twice the length of the single tacks") | no (judgement) |
| `scripts.REEVE_REFERENCE_LENGTH_M` | 41.8 m | the frigate's length on the waterline (her ship file); the fathoms scale by the ship's length against it, the schooner's lines about three fifths | yes (the file's) |
| `scripts.SPLICED_STRENGTH` | 7/8 | Luce 1884, ch. II Knotting and Splicing, 'Splicing': "the splice is weaker than the main part of the rope by about one-eighth" | yes, read in `docs/references/` |
| `parts.DEFAULT_CORDAGE_FATHOMS` | 120 | one coil, for a ship whose file gives no `cordage_fathoms`: rope for running rigging laid to "stand 120 to 130 fathoms" (Steel 1794, vol. I, 'Rope-making', of hawser-laid rope); the frigate's file carries 600 (five coils) and the schooner's 150, both there since milestone 3 as judgements | the coil's length yes; one coil judgement |
| `reeve_line.yaml` timing | cut 60 s, reeve 240 s, splice 300 s; six able hands | judgement: a hand at the yardarm and the rest rousing up and overhauling on deck; a long splice is slow work with a fid (Lever 1808, 'The Long Splice') | no (judgement) |

### Found on the way (package 31b)

- **A sail with one sheet parted said "sheeted home already."** `sheet home` filtered the parted sheet out and found the other hauled; it now refuses in words that name the sheet and the remedy, as the set evolutions do.
- **"Trim on a shift" and the wander.** Under the M2 walk the starter's point rule fired only on a scripted veer; under the air-mass rule it fires on the wander through a gale in neutral air (fourteen times on the pinned night, five on the day under systems, whose warm sector wanders three degrees). The rule reads the instant true wind; a rule on the ten-minute mean's direction, or a dwell on the veer, would quiet it. Left as measured for the owner.
- **The five-minute dwell and a squall.** Above: a squall of a few minutes fills the starter's "for 5 minutes", which was written against gusts of half a minute.
- **"Topgallants again" on the day under systems** now fires by nine (08:52): the reefs come out of the three topsails together in the swell, where package 31 had them one after another and the ten minutes unreefed had not run.

## Milestone 5: staying and sheets, the fore-and-aft rig at the small vessels' scale

### Package 32e: the constants and their sources

Spec M5 open items 12 and 13, from the owner's playtest of 2026-09-30 and the lead's probe the same day. Every scenario below is the four ships as the known truths measure them: plain sail in 15 knots of true wind, seed 7, the yards and sheets trimmed by the `trim sails` order every two minutes while she settles, then the manoeuvre from close-hauled on the starboard tack at 67.5 degrees off.

| Constant | Was → is | Source, or the confession |
|---|---|---|
| `hull.C_YAW_LIN`, `hull.C_YAW` | 2.5, 2.0 on `A L (u r, L r|r|)` → 0.06, 0.048 on `A L² (u r, L r|r|)` | The standard slender-body form (Principles of Naval Architecture, the controllability chapter: the yaw derivatives made dimensionless by ρ L⁴ U and ρ L⁵): a cross-flow force on the lateral plane, ρ A u (r L), acting at a lever of order L. Package 10's expression was a force, not a moment, and its constants hid the frigate's 41.8 m waterline, so every hull turned in the frigate's circle in metres (the cutter at a degree and a third a second). The new constants are package 10's divided by 41.8: the frigate keeps truth 16 (4.9 to 5.1 lengths), the size is judgement fitted to her band. |
| `hull.C_R` | 2.5 → `RUDDER_EFFECTIVENESS` 0.685 × Helmbold's slope for the blade's aspect ratio (`RudderSpec.span_m`, new; `RUDDER_DEFAULT_ASPECT` 3.0 when a file gives no span) | Helmbold 1942, 2π AR / (2 + √(AR² + 4)), quoted from memory of Hoerner's *Fluid-Dynamic Lift*, ch. 3, the page not verified: judgement in the form. The effectiveness (the wake of the deadwood and the sternpost, the flow's angle in a turn) is fitted so the frigate's blade (15 ft by 4 ft 3 in, AR 3.5, slope 3.65) keeps package 10's 2.5 per radian; the schooner's 11 ft by 2 ft gives 3.07, the cutter's 9 ft by 1 ft 6 in 3.11, the brig's 12 ft by 3 ft 2.81. The spans are the ship files' blade notes; the generator writes them. |
| `hull.RADIUS_OF_GYRATION` | 0.25, unchanged | The rule of thumb for yaw (a quarter of the waterline). No source gives it by hull type; judgement for all four. |
| `tack.yaml` `min_speed_kn` 0.8 → `way_gone_fraction` 0.25, `way_gone_lengths_per_min` 1.0, `hang_after_s` 5 | new | Her way is gone when she has made less than a quarter of her speed at "helm's a-lee" or less than a length a minute (the frigate 1.4 kn, the schooner 0.8, the cutter 0.5, the brig 0.9), whichever is the more, for five seconds. Judgement: no period source gives the way a ship must keep to stay; a hull moving under a length a minute has no steerage-way, and the dip as she comes head to wind is the ordinary tack. The dwell was fifteen seconds first; at fifteen the frigate in six knots of wind, whose head was two points short of the wind when her way went, counted as hung and was boxed through, where truth 10 has her miss. |
| The tack's sheets: `ease_off_sheets` at "helm's a-lee", `full_and_by_apparent` at "let go and haul" | new | The head sheets are eased right off at "helm's a-lee" (Luce 1866: the head sheets let go as the helm goes down), not let fly: a sail let fly carries the flogging windage (package 23's stall, a loose sail's) all the way through the wind, and with it the frigate came through with less way, gathered sternway, luffed back with none and lost seventeen metres to windward in a tack of 455 s; eased right off the jibs lift quietly. At "let go and haul" and again when the head yards are round, the sheets are drawn for the apparent wind of the close-hauled course she is coming to, from the true wind and the way she carried to "helm's a-lee" (the triangle; `close_hauled_true_angle`): not the rig's luffing angle of the moment, which reads the yards where they stand (squared, as the wind comes aft in a wear, it had the head sheets eased for a wind two points too broad, and the frigate griped up and would not come to, truth 11 failing), and not the way she has in stays, which is none (the schooner and the brig were then called tacked with their sheets eased for a reach and under a knot on them). Eased a point fuller than that "until she has way" was tried and is wrong in this model, whose jibs want their working angle of attack to draw at all: every ship lost a hundred and fifty metres. |
| `trim.read_sheet`: a sheet eased right off holds nothing | new | A sided sheet with no scope taken in (`hauled` 0) on the weather side does not hold its sail aback: the sail blows over to leeward. Physics: a sheet with all its scope out has nothing to hold by. Found on the schooner's circle, where the eased sheets read as an aback plate at the ceiling angle helped her round (5.4 lengths; 6.2 honest). |
| `TrimSheetScript` re-aims each tick, and yields | new | The party trims to the wind as it stands when it belays, not the wind at the order (the frigate's spanker landed four degrees off after a minute's hauling as she gathered way); and a party whose sheet other hands move (a manoeuvre's, an order at the pin) gives way and the sheet stands where they put it. |
| `tack.yaml` `stays_timeout_s` 180 | from "helm's a-lee" → from the moment her way is gone | Luce 1866, ch. XXIV, 'Missing Stays': "lie in that position dead in the water (in irons, as it is termed), and eventually fall off the wrong way". Three minutes is package 7's number, kept. |
| The miss: `TackScript._miss_stays` | the yards to 0° in a tick → a `YardSwing` over `brace_s` (45 s), the head sheets flattened in, the driver's sheet eased right off, the helm to the old heading as an order | Luce 1866, 'Missing Stays': "Flatten in the head sheets! ease off the spanker sheet"; the yards squared as "mainsail haul" swings them, with hands and time. |
| The recovery: `TackScript._hang` | new | Luce 1866, 'Tacking', pp. 450-451: "it should be kept so until she loses entirely her headway; then, Right the helm! and if she gathers sternboard, Shift the helm!" (the helmsman's `STERNWAY_SHIFT_SPEED` rule does the shifting); "haul the spanker boom well over to the windward"; Luce 1884, ch. XXXIV, 'Sloops': "If she hangs in stays, trim the jib sheet to windward again as she passes the direction of the wind"; 1884, ch. XXIV, 'Missing Stays': "BRACE ABOX THE HEAD YARDS, leaving the helm hard a-starboard for sternboard ... As she goes off with sternboard, DRAW JIB!". |
| `trim.TRIM_OFFSET`, `TRIM_RANGE` | unchanged | Package 10's change 6; the floors are now the sheet flat aft, the ceilings the sheet eased right off. |
| `trim.SheetGeometry` | new | The boom's length and height (the ship file), the horse's breadth (`horse_m`, new: half the beam, judgement; Steel 1794 vol. I, p. 167, HORSE, "a thick iron rod, fastened at the ends to the inside of the stern ... for the main sheet to travel on"), the purchase's parts (`parts`, new: the generator's rope sizes, a twofold purchase on the frigate's and the brig's spanker sheets, threefold on the schooner's and the cutter's main sheets); a loose-footed sail's clew on a foot of 0.8 √area with its sheet's block a fathom abaft the clew's place at the floor angle (`LOOSE_FOOTED_LEAD_AFT_M`, judgement). Scopes: the frigate's spanker 15 fathoms of fall, the schooner's main 31, the cutter's main 25, the brig's spanker 19, a jib two to four. |
| `trim_gaff_sheet.yaml`, `trim_jib_sheet.yaml` | new | `seconds_per_m2` 0.4 and 0.3, between 20 and 120 s, 15 and 60 s: judgement, no period timing for a sheet found (the frigate's spanker 67 s, her jib 39 s, the cutter's staysail 15 s). Hands: six of the afterguard to a purchase, four forecastlemen to a head sheet (Luce 1884, ch. XVIII, the duties of the afterguard and the forecastlemen); judgement in the numbers. |
| `sails.SHEET_LOAD_FRACTION` 0.6 | kept for loose-footed sails, on the working sheet only | A boomed sail's sheet now carries the sail's pull times its centre's distance abaft the mast over the sheet's lever (`SheetGeometry.lever_m`). In 15 knots on a wind the frigate's spanker sheet stands at 0.04 of its rating, in 35 knots running at 0.2: no sheet parts in ordinary sailing, and a gybe's snatch is not in this model (below). |
| `scripts.HOVE_TO_DRIVER_APPARENT` | new, 6 points | A driver kept hove to has its sheet eased to the trim of a wind six points on the bow: judgement, measured on the brig (below). |
| `starter.orders` "tend the sheets" | new, every glass | Luce 1866, ch. XXIV, 'Tacking': "trim aft the sheets"; the cadence is judgement. |

### Where the four ships stand

The polars, the pointing sweeps and the beam reaches were measured again after the change, by the tests' own sweeps: **the pointing truths did not move**, so the helmsman's margin (`FULL_AND_BY_MARGIN`, 8 degrees, package 10's change 5) stands. Before (package 32b's table) → after:

| Ship | best course to windward | holds 3 kn to | beam reach |
|---|---|---|---|
| frigate | 64° (4.8 kn) → 64° (4.8 kn) | 56° → 56° | 8.0 kn → 8.0 |
| schooner | 58° (5.9) → 58° (5.9) | 44° → 46° | 7.9 → 7.9 |
| cutter | 58° (5.4) → 58° (5.4) | 46° → 46° | 7.3 → 7.3 |
| brig | 64° (4.7) → 64° (4.7) | 54° → 54° | 7.7 → 7.7 |

The polars are the same to the tenth of a knot at every point but the brig's 50° (0.9 → 2.3 kn: her jib and staysails sheeted for the wind she has, not flat) and the cutter's 80° (7.1 → 7.0). Truth 73 keeps its expected failure: the cutter and the schooner point the same to the degree, as package 32b found, since the sail classes' curves and floors are shared.

**Turning circles**, hard a-weather from a beam reach at about eight knots, the transfer when her head has come round sixteen points, in her own lengths (truth 16's measure), before → after:

| Ship | at | before | after | swung at most | source |
|---|---|---|---|---|---|
| frigate | 8.0 kn | 5.1 lengths (212 m) | 4.9 lengths (207 m) in 119 s | 2.1°/s | truth 16's band of four to six lengths: judgement, kept; Luce 1884 App. L, read, is steamship trials only (the Hankow, the German Admiralty's pamphlet, the Stratheden, the Tennessee, Quinnebaug and Enterprise) |
| schooner | 7.9 kn | 5.7 lengths (147 m) in 80 s | 6.2 lengths (161 m) in 127 s | 2.9°/s | band four to seven: judgement (a long shallow hull, a small rudder). 5.4 lengths while a sheet eased right off on the weather side read as an aback plate (above) |
| cutter | 7.3 kn | 5.0 lengths (77 m) in 45 s | 4.9 lengths (75 m) in 47 s | 5.0°/s | "spins on her heel": the type's reputation, no figure; band three and a half to six, swung twice as fast as the frigate |
| brig | 7.7 kn | 4.9 lengths (132 m) in 77 s | 4.8 lengths (130 m) in 78 s | 3.3°/s | as a ship in little: band four to six |

The "before" column is the same build with the yaw fixed and nothing else, which is why the small vessels' circles in lengths hardly move between the two: the fix put each hull's circle in her own lengths (the probe of 2026-09-30 had the cutter turning in the frigate's metres); what the rest of the package changed is how fast she swings and what she does in stays.

**Tacks**, from close-hauled at 67.5° off in 15 knots, "helm's a-lee" to steady on the new tack within five degrees, with the moment her head passed the wind ("let go and haul"):

| Ship | from | through the wind | tacked | source, or band |
|---|---|---|---|---|
| frigate | 5.4 kn | 107 s | 328 s, 2.6 kn on the new tack, 62 m gained to windward (298 s before the package) | truth 10, Luce's five to ten minutes; half a minute slower than before because her jibs lift, eased right off, from "helm's a-lee" to "let go and haul" instead of drawing for free |
| schooner | 6.9 kn | 38 s | 141 s, 5.0 kn | "a schooner about in under two minutes": through within a minute, the yards round and the sheets over within two, steady within three (judgement; Luce 1884, ch. XXXIV) |
| cutter | 6.3 kn | 22 s | 103 s, 4.5 kn | quicker than the schooner: through within half a minute, tacked within two (judgement) |
| brig | 5.3 kn | 93 s | 355 s, 3.5 kn | as a ship: five to ten minutes |

In eight knots at 3.4 knots the frigate carries her way through and tacks plainly in 399 s. In seven at 2.6 knots she hangs (her way gone 114 s after "helm's a-lee", her head within a point of the wind), her head is through 17 s later with the head sails aback paying her off, and she is boxed through by the recovery in 424 s; in six knots at 2.2 knots her way goes with her head still thirteen degrees short of the wind, a plain miss at 111 s, the yards squared over the next 45 s and she falls off on the old tack: truth 10's second half stands. No case was found in which she hangs and then falls back: Luce says the recovery "will in most cases insure the evolution". The swing she carries through the wind with no way on her is the hull's: at rest the model damps yaw by the quadratic term alone (`C_YAW`), some seventy seconds from a third of a degree a second to none, which is about what a ship in irons does.

**Hove to** in 15 knots, five minutes after the order: the frigate 61° off at 1.5 kn from four knots, 62° at 1.4 after ten minutes (truth 12, re-pinned from under 1.5 kn and 45 to 60 degrees to under 1.6 and 45 to 65: package 10 had her at 58 to 61 at about a knot; from five knots, the truth's own fixture, she lies 61° to 62° off at 1.50 kn, the last hundredth over the old line), with her head sheets hauled aft; eased off, or let fly, or the jibs down, she came head to wind and gathered three knots of sternway, so `heave_to` now hauls them aft ("regulate by easing off, or hauling aft, the spanker and jib sheets", Luce 1866, ch. XXVI). The brig, whose backed main topsail is on her aftermost mast, fell off to a run in five minutes with her spanker brailed up whatever her jibs did (172° off at 3.3 kn); with the spanker kept and its sheet eased for a wind six points on the bow she lies 66° off at 1.3 kn (five points: 24° off then falling off; eight points: 86°). The brig lies 66° off at 1.6 kn. The schooner, hove to the fore-and-after's way (Luce 1884, ch. XXXIV: the main sheet flat aft, the staysail sheet to windward, her fore topsail to the mast too), lies 49° off forereaching 2.7 kn (78° at 4.5 kn before); the cutter 47° off at 1.9 kn (45° at 2.3). With the staysail down instead, both come head to wind with two knots of sternway. The frigate's three-knot sternway with the jibs eased is the one number here that surprised: a jib that luffs early lets her mizzen topsail bring her up. The jibs hauled flat aft are stalled at five points of apparent wind, and it is the stalled jib that holds her: as she comes up it draws more and pushes her head off again; trimmed for the wind they luff as she comes up and she comes head to wind (tried at twenty, twenty-five and thirty degrees: 48°, 59° and 54° off at five minutes, head to wind and falling off to a run by ten). Before the package the free tending flattened them as she came up, a trim no hands had set, and she lay at 59°.

**Wears** (truth 11 and the catalogue's three): the frigate in 510 s, the schooner 487 s, the cutter 504 s, the brig 494 s, the sheets shifted over as the wind comes aft ("when the wind is aft shift over the boom and head sheets", Luce 1884, 'To Wear'). Before the shift was added the head sails ended aback on every ship and the frigate and the brig would not come to.

### The pinned days, re-measured

The gate's day (truths 48 to 51) keeps every tick it had: sunset 57052, the heavy-weather routine 74336, the three shortenings 63837, 65773, 68188, the topgallants again 95650, nothing lost. "Trim on a shift" fires twelve times, not fourteen: its last two firings, at 03:22 and 03:29 on 2 June, fell while all hands were making sail after the gale, and a trim now begins sheet evolutions that wait for hands, so the order's work had not ended and it could not stand again before the wind settled. "Tend the sheets" fires 57 times, every glass, finding the sheets standing as trimmed most glasses (the line says so). The day under systems keeps every tick (sunset 57039, the shortening 63200, the gale canvas 69115, the heavy-weather routine 74245, the close reefs in by 75103 before the first squall at 76673, make sail 101624, the topgallants again 103976, the sea's four changes); its lines are 616 (487 before: the tending routine's firings and the sheet evolutions) and its digest 043501476a3cc7f3.

Three truths and a test were re-pinned besides, each with its reason at the test: truth 12's band (above); truth 37, where the mizzen topsail now blows out at forty-five knots while the hands are still aloft sending down the topgallant masts, because with her spanker's sheet standing as trimmed at thirty-seven knots the frigate holds her course and eleven knots as the gale tops out, her whole topsails loaded half again over their rating, where before the free tending flattened the spanker as the jibs blew out, she griped up and lay shaking at forty degrees off with her topsails unloaded (the test now asks the reefs of the topsails still set); the readings test's schooner, who brought up to north with her sheets as trimmed luffs, loses her way and goes through the wind into irons with her canvas aback by its sheets, where before the tending kept her fore-and-aft canvas drawing and she stalled at thirty-four degrees; and the crewed voyage of truths 22 and 39, which now tends its sheets every minute while she gathers way from rest, since head sheets eased for the wind of two minutes before luff as the apparent wind draws ahead, and left so with the spanker coming on her she griped up into the wind at a knot and a half and had not the way to stay.

### Found on the way (package 32e)

- **Fixed sheets through a manoeuvre.** With the free tending gone, a sheet set once at "let go and haul" for the wind of that moment (near the eye, so flat) stalled the brig at four points off with a knot and a half after seven minutes; a spanker or a main kept flat aft holds her head up while the head yards come round (Luce 1866, 'Tacking': "if she flies up into the wind, let go the main sheet"). The tack now trims the head sheets and the boom's sheet for the apparent wind of the course she is coming to (the constants' table above), on the new tack's lee side by name, since the deck's reading lags as her head passes the wind; the trim order and the book take them from there.
- **A foresail's sheet not shifted.** The schooner's loose-footed foresail, neither a head sail nor a boom sail, stayed sheeted on the old lee side through a tack and was aback all the way down the new tack (200 s to steady, 3.7 kn); the tack now lets go the sheets of the staysails abaft the fore mast at "rise tacks and sheets" and shifts them over at "let go and haul" (Lever 1808, p. 78: "all the Staysail Tacks and Sheets abaft the Fore Mast are let go, and the latter shifted over the Stays"). 156 s and 5.7 kn after.
- **The deck's reading before the first tick.** A sail set before the physics has read a wind (the tests' worlds, a scenario's first orders) had its sheet put on the lee side of an apparent wind of zero, which is larboard, and lay aback on a larboard-tack wind: the strain test's frigate and schooner wore their head sails at the flogging rate for twenty minutes. Before the deck has read a wind both sheets of a pair are belayed alike and the sail lies to leeward of whatever wind comes (`set_sheet_angle`'s "either").
- **Four order-table entries failed at the base commit** (the merge of 31b and 32b): "brace the yards to the wind" on the cutter and the brig expected "3 yards" and "8 yards" where `number_words` has written "three" and "eight" since 31b, and "splice the mainbrace" expected a verb unknown where `splice` has been a verb since 31b. Their expectations are corrected here.
- **The tending routine's firing line is notable.** The standing runtime logs every firing of a standing order as a notable line, so "By standing order 'tend the sheets': trimming the sheets." appears at every glass, fifty-seven times a day, mostly followed by "the sheets ... stand as trimmed". The severity is the standing module's (not this package's files); for the lead.
- **Not done: a main sheet parting in a gybe.** The load a belayed boom sheet carries is quasi-static (the pull over the lever); a gybe's snatch is the boom's swing arriving on the sheet, which wants the boom coming over on a timeline (the rig-motion item), outside this package. In 35 knots running the frigate's spanker sheet stands at a fifth of its rating.
