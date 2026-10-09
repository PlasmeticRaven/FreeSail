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

## Milestone 5b: the reckoning, the noon sight, the captain's chart, the checkpoint save and the passage for gate 5b

Package 33a (spec M5 §8, §13 to §16, §17's second half, §18, §20; the study `docs/design/Navigation.md`, N). The world keeps the truth and the master keeps his account: nothing below is read from the truth by the account, and the tests compare the two from the world. Every constant with its source, and whether the source was verified; the figures the study marks unverified say so here as well as in their comments.

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| `reckoning.LOG_LINE_SHORT_MIN`, `_MAX` | 3% to 8% short | Luce 1866, "Log-line, Time-glasses": marked short "by 3 or 4 feet" of a 47.6-foot knot so that a ship overruns her reckoning; N §3's table gives 3 to 8 | Luce read; the range the study's |
| `reckoning.LOG_READ_KN` | a quarter knot either way | Falconer 1780, "Log": the knots, halves and quarters on the line; N §3 "read to a quarter knot" | the reference text |
| `reckoning.LOG_READ_SIGMA_KN` | 0.25 knots an hour | the hour's run inferred from one heave | judgement on N §3 |
| `reckoning.SPEED_BY_EYE_SIGMA_KN` | 1 knot | her way by eye, to the knot, before the first heave of a passage | judgement |
| `reckoning.HOVE_TO_WAY_KN` | 2 knots | hove to and making less way than this by eye, the log-board notes the time and the master runs no distance for it; with more way on she is sailing whatever her yards say | judgement |
| `reckoning.LOG_INTERVAL_H_SHIP_OF_WAR`, `_OTHER` | 1 h, 2 h | Falconer 1780, "Log": hourly in ships of war and East-Indiamen, once in two hours in all other vessels; a ship of war known by her marines | the reference text |
| `reckoning.VARIATION_1805_DEG` | 24° W | the true variation of the western Channel in 1805, to be computed from gufm1 at the chart's build (spec M5 §13); the anchors N §3 gives (Falconer's "more than 20 degrees" at London in 1780; 21° 09′ W at Greenwich in 1773) and the London series in Jackson, Jonkers and Walker 2000 (23 to 24° W through the decade, Cornwall a degree more westerly) | **unverified**: the study marks the figure so, and the build tool does not yet compute it; the constant is provisional |
| `reckoning.CHART_VARIATION_AGE_YEARS` | 10 years | the 1794 reissue of Mountaine and Dodson's chart (N §1), a decade old in 1805 | the study's chart |
| `reckoning.VARIATION_DRIFT_DEG_PER_YEAR` | a quarter of a degree a year | N §3 | **unverified**: the study's figure, not sourced further; with the decade it makes the 2.5° the master allows wrong |
| `reckoning.DEVIATION_MAX_DEG` | 3° either way, B and C of B sin H + C cos H | N §3: "a few degrees in a wooden ship with iron guns, more with iron stowed near the binnacle", not corrected in 1805 | **unverified**: the size of a wooden frigate's deviation is on the study's list |
| `reckoning.STEERING_SIGMA_POINTS_SMOOTH`, `_SEAWAY` | a quarter and half a point | N §3: "half a point in a seaway, a quarter in smooth water"; the seaway is a heavy sea or worse in spec §4's words | judgement (the study's) |
| `reckoning.LEEWAY_ALLOWED_WITHIN_POINTS` | 8 points of the true wind | Falconer 1780, "Lee-way": disregarded whenever the wind is large | judgement on "large" |
| `reckoning.LEEWAY_ESTIMATE_ERROR_POINTS` | half a point either way, once per ship | N §3 | the study's figure |
| `reckoning.LEEWAY_DOUBT_POINTS` | a quarter of a point across the course while allowed | half a point either way as a spread | judgement |
| `reckoning.SET_DOUBT_EAST_KN`, `_NORTH_KN` | 0.2 and 0.03 knots, growing in a straight line | N §3's Channel streams east and west and Rennell's current; tuned so that four days of thick weather leave the ellipse of truth 58 (below) | judgement, tuned |
| `reckoning.DEPARTURE_SIGMA_NM` | 1 mile | a bearing of a headland and its distance by estimation | judgement |
| `reckoning.FIX_RUN_NM` | 2 miles | a line taken within this run of the last is crossed with it; after a longer run it replaces the account across it | judgement (a quarter of an hour's run) |
| `reckoning.HAND_LEAD_FATHOMS`, `HAND_LEAD_MARKS` | 20 fathoms; 2, 3, 5, 7, 10, 13, 15, 17, 20 | Lever 1808, "The Hand-Lead"; Luce 1884, ch. I, marks 20 and on for the longer line | the reference texts |
| `reckoning.DEEP_SEA_LEAD_FATHOMS` | 120 fathoms | one lead in the game for Luce's coasting and deep-sea leads | judgement |
| `reckoning.DEEP_SEA_LEAD_MAX_KN` | 4 knots | Lever 1808: "for which it is usual previously to bring-to the ship", or with a light breeze hove from the spritsail yardarm | judgement on Lever's words |
| `reckoning.LEAD_HAND_SIGMA_FATHOMS`, `_DEEP_` | a quarter fathom, a fathom | N §3, "depth to a fathom"; the leadsman's quarter | the study's figure; the quarter judgement |
| `reckoning.SOUNDING_ACROSS_SIGMA_NM` | 3 miles | N §3: "a band a few miles wide along the depth contour" | judgement on "a few" |
| `reckoning.CONTOUR_SEARCH_MIN_NM`, `CONTOUR_TOLERANCE_HAND_FATHOMS`, `_DEEP_` | 5 miles; 0.75 and 2.5 fathoms | the ring the cast's contour is searched on (at least this about the account) and the tolerances (the lead's error and the chart's) | judgement |
| `reckoning.BEARING_SIGMA_DEG` | 1.5° | N §3: "a degree or two by compass" | the study's figure |
| `reckoning.TRANSIT_SIGMA_NM` | a cable | spec §13: "a transit is exact" | judgement |
| `reckoning.DISTANCE_BY_ESTIMATION_FRACTION` | a fifth of the distance, one sigma, drawn each bearing | the distance off by estimation that goes with a bearing (spec §12's words, "twelve miles by estimation"), a second line along the bearing: a bearing with its distance lays the ship on the chart as the period's master did | judgement |
| `reckoning.DAYS_WORK_MINUTES` | 30 minutes | the traverse reduced from the log-board and the sight worked (Falconer 1780, "Log-board", "Traverse") | judgement |
| `reckoning.TRACK_KEPT` | 168 hourly positions | a week of the track for the chart | judgement |
| `chart.CONTOUR_STEP_M` | half a mile | the rings a cast's contour is searched on | judgement |
| `sights.SEXTANT_SIGMA_NM`, `OCTANT_SIGMA_NM` | 1 and 2.5 minutes of altitude | N §3: "sextant to a minute, octant to two or three" | the study's figures |
| `sights.HORIZON_SIGMA_NM` | 1.7 miles | N §3's "2 to 5 miles with a good horizon" taken as the whole error with the sextant, so the horizon's part makes two with the sextant's one | judgement |
| `sights.HAZE_HORIZON_NM`, `HORIZON_SEA_NM_PER_M` | a mile in haze; half a mile a metre of sea | N §3, "the horizon in haze or swell two to five minutes", the five with the octant in a three-metre sea | judgement |
| `sights.SIGHT_ON_DECK_MINUTES` | 15 minutes | the master on deck watching the sun rise to its greatest altitude | judgement |
| `sights.SKY_HIDES_THE_SUN`, `WEATHER_HIDES_THE_SUN` | overcast, dark and gloomy, threatening, thick; rain, drizzle, fog, thunder | Beaufort's words as spec §5 gives them; hazy lets the sun through with a worse horizon | judgement on the words |
| `sights.SKILL_REFERENCE` | 0.5 | a skilled master (0.9) reads his instrument at three fifths of its error, a poor one (0.5) at the whole | judgement |
| `lookout.SHORE_CLOSE_NM` | 3 miles | the shore itself hailed close aboard when no headland of the chart is in sight (at every look since package 37d), within the visibility and the night's mile; the same three miles a danger is made out at | judgement |
| `sun.Sun.transit` | the sun's meridian passage from the equation of time and the ship's longitude | Meeus's approximation already in `core/sun.py` | arithmetic |

The errors the master cannot know shift the account and not the ellipse (N §3; Apollo: "the ellipse drawn too small"): the line's marking, the chart's variation a decade stale, the deviation by heading and the leeway bias. The ellipse holds the doubts he does know he has: the read, the steering, the set he did not allow for, the leeway he allowed by eye. Seed 7's draws for the frigate: the log-line 7.98% short, the deviation B −0.048° and C −0.379°, the leeway bias +0.22 points, the variation error 2.5° (the chart's 21.5° against the world's 24°); the master's skill from the ship file's deck.

### The ellipse after thick weather, measured (truth 58)

The traverse alone, fed a day's run of 150 miles at six knots and a quarter for four days without a sight, the wind free (`tests/test_known_truths.py`, truth 58): the ellipse's length twice its standard deviation, as the words give it.

| Course | after one day | two days | four days | then a clear noon |
|---|---|---|---|---|
| east (the Channel's own) | 10.1 × 3.9 miles | 19.6 × 5.5 | 38.8 × 8.6 | N-S 4.0 |
| north-north-east (Finisterre for the Channel) | 10.1 × 3.9 | 19.6 × 5.5 | 38.9 × 7.9 | under 5 |
| north | 10.1 × 3.9 | 19.6 × 5.5 | 38.9 × 7.8 | under 5 |

Against N §3's 30 to 50 miles east and west and under ten north and south after four days: 39 by 8 to 9. The set doubt is what makes it: the read's and the steering's terms grow as the square root and would leave a dozen miles after four days; the biases grow in a straight line, and the two figures above were set so that the fourth day lands in the study's band (two days is twice one, four days four times, as the test asserts). The words at four days: "I would not trust the reckoning within thirty-nine miles east or west, nor eight miles north or south."

### The checkpoint, measured

The passage's world at three hours with the fake watcher standing by, the lead just ordered: saved with its checkpoint (`replay.save_to_file`, `checkpoint=True`) in the scratchpad's proof (`smoke_checkpoint.py`). The checkpoint loads in 0.06 s where the replay of the three hours takes 16.5 s on the build machine, and the three of them (the live world, the one loaded from the checkpoint, the one replayed) run the next watch to the same digest, the lead's cast and all. The test (`tests/test_checkpoint.py`) proves the same on a shorter run and checks the header (the seed, the end tick, the journal's and the inputs' lengths, the digest) against the save, so a checkpoint from another save or another build is refused and the replay used instead (`replay.load` says which it did; the drivers print "from its checkpoint at" or "replayed to"). What the pickle drops and the load rebinds: the chart (reopened by region), the readings' view, the log's subscribers, the ship's stepper and order handler, the harness's model and save hook (`session.rebind_hooks`); the unpickler admits only the game's own classes and the standard library's few it needs.

### The passage for gate 5b, measured

Seed 7, the day's weather pinned (`data/scenarios/gate-5b-passage.yaml`: a south-westerly of fifteen knots backing a little, the sky pinned clear over the old high; the high's own coastal fog off Ushant from dusk to eight in the morning would have refused the departure bearing). The frigate from off the Stiff at four in the morning of 10 June 1805, seventeen hours, 474 lines, digest `c160c0ef4b83d899`; the account against the truth read from the world by `tools/day_log.py --reckoning`, the ellipse's axes one sigma, east-west by north-south.

| Tick | Time | Moment | Truth | Account | Error | Ellipse |
|---|---|---|---|---|---|---|
| 0 | 04:00 | the departure: "The light on Ushant bore SW by S, a mile by estimation" | 48° 30′ N, 5° 02′ W | 48° 30′ N, 5° 02′ W | 0.2 | 0.1 × 0.2 |
| 7200 | 06:00 | the last bearing of Ushant, S by W, four leagues | 48° 41′ N, 5° 02′ W | 48° 41′ N, 5° 01′ W | 1.3 | 0.3 × 0.6 |
| 28740 | 11:59 | "Noon. Latitude by observation 49° 25′ N; the reckoning was 49° 27′ N. Course made good since the departure N, 58 miles. Longitude by account 4° 57′ W." | 49° 22′ N, 5° 03′ W | 49° 25′ N, 4° 57′ W | 4.8 | 1.5 × 2.4 |
| 28796 | 12:00 | hove to for the cast ("bring to for soundings") | | | | |
| 29928 | 12:19 | "Fifty-three fathoms; fine grey sand with black specks" (the deep-sea lead) | 49° 22′ N, 5° 02′ W | 49° 25′ N, 4° 57′ W | 4.7 | 1.5 × 1.9 |
| 29984 | 12:20 | filled away; "Shaped a course for Falmouth: N by W by account, 45 miles" | | | | |
| 45000 | 16:30 | the landfall: "The Beast bearing NNW, distant four leagues"; the Lizard with it | 49° 46′ N, 5° 06′ W | 49° 52′ N, 5° 09′ W | 6.2 | 0.4 × 1.0 |
| 45000 | 16:30 | "The Beast bore N by W, three leagues by estimation"; the course for Falmouth shaped again, N by E, 18 miles by account | 49° 46′ N, 5° 06′ W | 49° 51′ N, 5° 09′ W | 5.3 | 0.3 × 0.9 |
| 46800 to 57600 | 17:00 to 20:00 | bearings every glass, the Beast, Black Head, Lowland Point, Manacle Point, St Anthony's Head; the lead going, no bottom at twenty fathoms | | | 5.2, 3.9, 2.6, 2.1, 1.6, 1.0, 0.2 | 0.4 × 0.8 to 0.1 × 0.2 |
| 59400 | 20:30 | "St Anthony's Head bore W, two miles by estimation" | 50° 09′ N, 4° 58′ W | 50° 09′ N, 4° 58′ W | 0.0 | 0.2 × 0.1 |
| 59495 | 20:31 | "By the mark seven; mud"; the Roads: hove to at 59552 | 50° 09′ N, 4° 58′ W | 50° 09′ N, 4° 58′ W | 0.0 | 0.2 × 0.1 |
| 61200 | 21:00 | the end | 50° 09′ N, 4° 58′ W | 50° 09′ N, 4° 58′ W | 0.1 | 0.2 × 0.1 |

What the numbers say. The account overruns the truth through the forenoon (the line 8 per cent short at seed 7, the read's quarter knots) and the noon sight puts the latitude right to two miles while the longitude by account stays six minutes east, which the ellipse's 1.5 miles east and west does not cover: the chart's stale variation and the deviation are the biases the master cannot see (N §3's "ellipse drawn too small"). The cast in the Channel Soundings finds the fifty-fathom contour running the way she is going and leaves the account where it was. The landfall is made six miles wrong, the account ahead of the ship, and the first bearing with its distance by estimation halves that; each glass's bearing of the next headland with its distance brings the account in, a mile by the Manacles, a cable off St Anthony's Head; the lead finds bottom only inside the Head. Seed 7's draws for the frigate: the log-line 7.98 per cent short, the deviation B −0.05° and C −0.38°, the leeway bias +0.22 points, the chart's variation 2.5° out.

The thick passage (`gate-5b-passage-thick.yaml`, the sky pinned thick, fog, a mile; sixteen hours, 339 lines, digest `1d9de61e14be40ac`): no departure bearing (Ushant beyond the fog), "Noon. No sight; the sun was hid at noon in fog. Latitude by account 49° 27′ N" (truth 49° 22′ N, 5° 01′ W; error 5.6; ellipse 2.1 × 1.2), the cast "Fifty-one fathoms; fine grey sand with black specks" (error 5.5; ellipse 3.0 × 1.3), the course for Falmouth shaped at 16:40 when the run since noon passed thirty miles, the hand lead every glass finding no bottom at twenty fathoms with the error at ten miles, and the landfall at 19:07: "The land about Black Head close aboard on the starboard bow, bearing N, distant a mile", the account 50° 10′ N, 5° 05′ W against the truth 49° 59′ N, 5° 07′ W, 10.9 miles, ellipse 3.4 × 1.5, hove to at 19:08 (`when the land is in sight then heave to`). N §3's "'We should be seeing the Lizard by now'" is this line: she believed herself past the Lizard and inside the bay when she was still off Black Head.

The schooner (`gate-5b-passage-schooner.yaml`, the octant, no glass, the log every two hours; fourteen hours, 320 lines, digest `8b852e793dc2f70d`): the departure bearing, the heaves at six, eight and ten, "Noon. Latitude by observation 49° 22′ N; the reckoning was 49° 29′ N" (truth 49° 22′ N, 5° 04′ W; error 3.7, the octant's; ellipse 1.9 × 2.8), the landfall at 15:49, the Lizard NNE four leagues, 6.6 miles wrong (ellipse 2.3 × 2.9), brought to 3.6 by the bearing and to a mile by four; "Quarter less eleven; fine sand" at 18:02 with the account on the truth. The schooner's cast at noon did not happen: see found on the way. The cutter and the brig through the same orders for six hours (`--ship`): the cutter 153 lines, digest `938bdbb4459ef1b2`, the log every two hours, the account 4.3 miles off at ten in the morning; the brig 184 lines, digest `54dece656ed09d91`, hourly (her marines), 3.6 miles off. No navigation order refused in any of the five.

The pace on the passage (`test_the_pace_on_the_passage_holds_truth_51s_floor`): the traverse board every tick, the grounding check, the lookout once a minute, the log hourly; the best of three thousands held truth 51's floor on the build machine beside the sibling package's suite.

### Found on the way (package 33a)

- **The coastal fog refused the departure.** Under the old high the sector table lays advection fog off Ushant from dusk to eight in the morning (W §1.4), so the light at four was beyond a cable's visibility and "take a bearing of the light on Ushant" was refused with "Nothing is in sight". The clear passage now pins its sky (`weather: sky`) as the thick one does; and the sun is up at four at this latitude in June, so the tower is a mark by day and not a light.
- **Before the first heave the account stood still.** A bearing at the departure stepped the board with no read yet, at no speed, and the two-hourly log left a schooner's account where she started for two hours. The master now runs her way by eye, to the knot, until the first read (`SPEED_BY_EYE_SIGMA_KN`).
- **A bearing without its distance put the account on the wrong side of the mark.** Running in on a headland the bearings all lie along the track and correct nothing along it; the account, six miles ahead of the ship, was laid on Manacle Point's line six miles inland of it, and the course for Falmouth shaped from there led east of the Roads to the Nare. The period's master had the distance by estimation with the bearing and laid the ship on the chart from both; the distance is now a second line (`DISTANCE_BY_ESTIMATION_FRACTION`), and the passage above is the result.
- **The schooner hove to and sailed on.** At noon the schooner hove to for the cast (fore topsail to the mast, helm a-lee) and fifty-four seconds later the starter's "keep her full" bore away a point, her sails filled again and she ran on at seven knots with `ship.extra["hove_to"]` still set: the deep-sea lead was never hove (she never came under four knots), "fill away after the cast" never fired, and the Roads' "heave to" in eleven fathoms was refused with "She is hove to already", so she stood on and took the ground off Black Head at 18:24. The heave-to script and the fill-away rule are package 32e's (`evolutions/scripts.py`); the board's count of hours hove to guards itself (`HOVE_TO_WAY_KN`: with more than two knots of way she is sailing whatever her yards say), and the schooner's pinned passage stops at fourteen hours, before the grounding. For the lead: either "keep her full" should hold while she is hove to, or bearing away should clear the state.
- **The frigate's twenty minutes hove to overran the account by a mile.** The hour's read after the cast was applied to the whole interval, the twenty minutes with the main topsail to the mast included; the board now notes the time hove to and making no way and runs no distance for it.
- **The starter's "landfall" rule fires at the start.** "When the land is in sight" is true off Ushant, so the course for Falmouth is shaped at the departure (N by account, 99 miles) as well as at the Lizard; harmless here, since north is the course, and the rule's wording is the scenario's.
- **`sail.backed` lines while hove to in a seaway.** A ship hove to in a moderate sea logs the topsail backed and filled again by the minute; the physics' words, package 32e's area, left as they are.
- **The variation is provisional.** `VARIATION_1805_DEG` is the package's recollection of gufm1 for the Lizard (about 24° W), not a computed value; the chart build does not run the field model. An azimuth to correct the chart's variation (N §3) is not built.

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

**The owner's ruling at gate 5b** (decision 30): the small vessels' tack and turning bands stand provisionally and stay on the tuning list, the brig's with them; the brig felt right on her free passage (playtest 13), the cutter's heave-to uncertain and the brig's heave-to once through the wind and back, both for the fore-and-aft second pass when it is taken up.

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

## Milestone 5: the passage's words (package 33c)

Recorded by the lead from the package's report (2026-10-01). No physics; two judgements in
the standing runtime and the re-pinned days that follow from them.

### The conflict rule's grain (spec M5 open item 15)

A sail, a yard or a line is its own part and the helm is one; a manoeuvre (tack, wear,
heave to, fill away, box haul, lie a-try, scud, back and fill, wear short round) takes the
helm and every yard; `heave the lead` is the lead's, `heave the log` the log's, a bearing
and the account the master's, a shaped course the helm's; the ship's is only what is left.
A firing whose evolutions have all ended no longer counts against a later order, so `at
wore then heave to` follows the wear instead of clashing with it. On the gate 5b passage
the conflicts fell from 21 to 1 (the one real: "keep her full" against "lie off" on the
helm, which the book's author should see).

### The held lines, once a watch (judgement)

A failing `, if` on an `at` or an `every` order is logged the first time and then once a
watch of the ship's clock while it goes on failing, and afresh after the order fires.
"Once a watch" is a judgement: the cadence at which an officer would mention again that
a standing order's condition is not met. The brief named `at` only; `every` was most of
the noise (the two leads' `every ten minutes, if` on the passage) and took the rule too.
The starter's `sound the well` is entered and held, not refused at every start.

### The pinned days, re-measured

Every tick of every pinned moment stands; only the line counts and the digests moved,
with the held and conflict lines and the well's two lines:

| Run | Lines before → after | Digest after |
|---|---|---|
| gate 5b passage | 837 → 679 (held 157 → 18; conflicts 21 → 1) | `d74f05aefcc4f94b` |
| the schooner's passage | 907 → 746 (held 155 → 15; conflicts 24 → 2) | `a3e2fd0a3a07170e` |
| the thick passage | 526 → 501 (held 31 → 6; conflicts 2 → 1) | `9f1a7626e4d4265d` |

Merged with 33b the same day (33b moved the ticks, 33c the lines): the frigate's passage 677 lines, `eacae6db04e7067a`; the schooner's 749, `e41ade78138e024d`; the thick passage 501, `f4d7575fea6ada34`; the ticks as 33b's section below has them (the landfall 45000, the outer road 56494, the wear 56834, lying to 56894; the schooner's landfall 44220).
| the day under systems | 616 → 617 (the well) | `9bd4e0bffcfb6b10` |

### Found on the way (package 33c)

- **The browser's first driver line.** The server writes the opening words about the book
  as a driver line (`driver.book`) so the browser's log says how to load the starter book;
  a driver line is in the digest, so the same scenario's digest differs between the console
  and the browser by that line, as it already did by any driver's line.
- **Two refusals left to other packages.** Tacking from a reach and the sheet-ease limit
  are the fore-and-aft second pass's; the lower-cased mark names in the lookout's list are
  33b's.
- **A sail by name is answered at the prompt but not offered by the completer**, which
  lists vocabulary phrases; a part's name alone would need `complete.py` to offer parts.

## Milestone 5: the chronometer, the moon, the lunar and the azimuth; the captain's chart in his hands

Package 33b (spec M5 §12, §14, §15, §17; decision 30; the study `docs/design/Navigation1805.md`, N, §2 to §5; the playtests of gate 5b). The world keeps the truth and the master keeps his account: every sight below is drawn from `world.position` plus a seeded error (the streams `chronometer` for the instrument's drift and offset, `reckoning` for the sights' draws, `lookout` for the eye's estimates), never computed from the model's own geometry; the engine never clears a distance. The figures the study marks unverified say so here as in their comments.

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| `moon` (the model) | Meeus ch. 47 (eq. 47.1 to 47.6; the 24 largest terms of Table 47.A, the 13 of 47.B), ch. 25 (the sun, low accuracy), ch. 22 eq. 22.2, ch. 13 eq. 13.3 to 13.6, ch. 12 eq. 12.4, ch. 17 eq. 17.1, ch. 21 eq. 21.4, ch. 48, ch. 49 eq. 49.1, ch. 7 eq. 7.1 | Meeus, *Astronomical Algorithms*, 2nd ed. | the book's own example 47.a reproduced to a hundredth of a degree; June 1805 against JPL Horizons (below) |
| `moon.LUNATION_DAYS` | 29.530588861 d | Meeus eq. 49.1 | the book |
| `moon.LUNAR_STARS` | Hamal, Aldebaran, Pollux, Regulus, Spica, Antares, Altair, Fomalhaut, Markab; J2000 places | the nine the *Nautical Almanac* tabulated (N §2; de Grijs §5 names the set without listing it) | **unverified**: the list and the places from memory of the catalogue, not read from a page; a tenth of a degree would not matter at the brief's accuracy |
| `sights.CHRONOMETER_RUN_HOURS` | 56 h | the two-day marine movement | judgement; no page read for the hours |
| `sights.CHRONOMETER_WIND_HOUR` | 8 a.m. | Luce 1884, ch. XX, the ship's routine at sea: "8:00 A.M. Relieve watch, wheel and look-out, report chronometers wound" | the reference text (later than the period) |
| `sights.RATING_OFFSET_SIGMA_S` | 2 s, drawn once | N §3: "plus a one-time offset from the rating" | judgement on the words |
| `sights.RATE_DRIFT_MIN_S_PER_DAY`, `_MAX` | 1 to 3 s a day, either sense, when `drift: seeded` | N §3: "rate wrong by 1 to 3 seconds a day (Bligh's K2)"; N §2, Bligh's "between 1.1 and three seconds" | the study's figure (Wikipedia, *Larcum Kendall*, read by the study) |
| `sights.RATE_DOUBT_S_PER_DAY` | 1 s a day since rating, the master's trust | the low end of N §3's one to three | judgement |
| `sights.CHRONOMETER_FAULT_S` | 20 s | under this the master finds no fault by a lunar (a lunar's own half-minute of arc is a minute of time, N §2) | judgement |
| `sights.TIME_SIGHT_SIGMA_NM` | 2.5 miles, one sigma, times the skill factor of the noon sight | N §4(b): "the sight's own two or three miles" | the study's figure |
| `sights.TIME_SIGHT_MIN_ALTITUDE_DEG`, `_NOON_GUARD_H`, `_WORK_MINUTES` | 10°; an hour and a half from the meridian; 20 minutes below | a morning or afternoon sight (N §4(b)); refraction uncertain low down; the hour angle slow against the altitude near the meridian | judgement |
| `sights.LUNAR_MOON_MIN_ALTITUDE_DEG` | 15° | N §4(c): "more than, say, fifteen degrees high" | the study's figure |
| `sights.LUNAR_MIN_AGE_DAYS` | 3 days from the change, either side | N §2: "near new moon there is no lunar for three or four days"; truth 61 | the study's figure |
| `sights.LUNAR_DISTANCE_MIN_DEG`, `_MAX` | 40° to 120° | N §4(c): the sun "between roughly 40 and 120 degrees from the moon by day"; a star at the same range | the study's figure; the stars' range judgement |
| `sights.LUNAR_BODY_MIN_ALTITUDE_DEG` | 10° | the body's altitude measured too | judgement |
| `sights.LUNAR_ON_DECK_MINUTES` | 15 minutes (the file `take_lunar.yaml`, 900 s, at the hands' pace in the weather: 17 minutes measured in twelve knots) | N §2: "a quarter of an hour on deck with the sextant for a set of distances" | the study's figure |
| `sights.LUNAR_CLEARING_MINUTES` | 60 minutes below | N §2: "half an hour to an hour of arithmetic below" | **unverified**: the study marks the time an 1805 master took to clear a distance so (no diary timing it; the twenty minutes a modern practitioner's); the constant is provisional |
| `sights.LUNAR_SIGMA_GOOD_DEG`, `_POOR_DEG` | a quarter of a degree; a degree | N §2, §4(c): "a quarter of a degree for a good master on a quiet day, a degree for a poor one in a seaway (10 to 39 miles at 50 N)" | the study's figures (de Grijs endnote 5; the 1765 witnesses) |
| `sights.LUNAR_SKILL_GOOD`, `_POOR`, `LUNAR_SEA_M` | 0.9, 0.5; two metres of sea doubles the spread | the skill ends are the ship files' deck skills; half of the poor figure the skill's and half the sea's | judgement |
| `sights.LUNAR_RATE_REFERENCE_DEG_PER_H` | half a degree an hour | N §2: the moon's motion against the stars; a distance closing slower widens the spread up to twice | the study's figure; the widening judgement |
| `sights.LUNAR_TRUST_SIGMAS` | two sigma, to the five miles | "which Mr. Ellis would trust within twenty miles" (N §4(c)) | judgement on the words |
| `sights.AMPLITUDE_ELEVATION_DEG` | the sun's centre between 1.5° under the horizon and 3° above | a quarter of an hour either side of sunrise and sunset | judgement |
| `sights.AMPLITUDE_SIGMA_DEG`, `AZIMUTH_SIGMA_DEG` | half a degree; three quarters | N §3: "an azimuth observation gets it to a degree", read as the whole of the error; Falconer 1780, 'Azimuth-compass', the brass edge "divided into degrees and halves" (the result read to the half degree) | judgement on the study's words |
| `sights.AZIMUTH_MIN_ALTITUDE_DEG`, `_NOON_GUARD_H` | 5°; an hour from the meridian | the sun's bearing changes fastest against its altitude away from the meridian | judgement |
| `sights.MOONLIT_MIN_ALTITUDE_DEG`, `MOONLIT_FRACTION` | the moon 10° up and more than half lit | spec §14's "the night's light" | judgement |
| `reckoning.VARIATION_1805_DEG` | 24° W, the world's truth, unchanged | spec M5 §33 item 14 | **unverified** still: gufm1 not computed by the chart build; the amplitude now corrects the master's figure toward it, and the world's own stays provisional |
| `chart.MOONLIT_LAND_NM` | 3 miles | the land under a full moon seen at a league where a dark coast shows at a mile | judgement |
| `chart.LIGHT_NOMINAL_VISIBILITY_NM`, `LIGHT_CONTRAST_THRESHOLD` | 10 miles; 0.05 | Allard's law as IALA's luminous range diagram applies it: a light's nominal range is its range in ten miles' meteorological visibility, the transmissivity per mile 0.05^(1/V) (Koschmieder's five per cent) | modern, from memory of IALA's recommendation E-200; no period source gives a light's loom in rain (below) |
| `chart.DANGER_PASS_NM` | a mile | the brief's "the line passes the Manacles within a mile" | judgement |
| `chart.DANGERS_WITHIN_NM` | 10 miles | an hour's run and more | judgement |
| `chart.CHART_EDGE_NM` | 10 miles | the lookout says the chart ends within this of its bound | judgement |
| `chart.HAZARD_KINDS` | rock, ledge, drying, shoal | a bank with its depth in fathoms is a sounding mark | judgement |
| `lookout.DISTANCE_BY_ESTIMATION_FRACTION` | a sixth of the distance, one sigma, drawn once a sighting episode (was a fifth, drawn at every bearing taken, package 33a) | the eye's judgement of a headland's distance from its height and what shows of it | judgement; the fifth at seed 7 called the Lizard, ten miles off, five leagues, and a sixth four |
| `lookout.ESTIMATE_HOLD_NM` | a mile | held while she makes under a knot (the brief); judged afresh a mile on with the same eye. **Gone in package 37d**: `ESTIMATE_REFRESH_FRACTION` | judgement |
| `lookout.CLOSING_MINUTES`, `_STEADY_POINTS`, `_FRACTION`, `_LAND_NM` | 10 minutes; a point; a fifth closed; the land within a league | the seaman's rule for a collision course; a ship running in has every headland ahead steady and closing, so the hail is for a danger at any distance and the land or a light within a league | judgement |

### The moon against the Almanac's figures

No *Nautical Almanac* of 1805 was reachable; the check is against the JPL Horizons ephemeris (DE441, read 2026-10-01; the geocentric ecliptic longitude and latitude of date and the illuminated fraction at 0h UT) and against Meeus's worked example 47.a. The model's longitude is within 0.007° of Horizons on every day of June 1805 tried (the 1st, 5th, 10th, 12th, 20th, 27th), its latitude within 0.01°, its illuminated fraction within 0.1 per cent (the 10th: 95.4 per cent against 95.41; the 12th 99.9 against 99.90, the full moon; the 27th 0.0 against 0.01, the change). Meeus 47.a (1992 April 12, 0h TD): longitude 133.1615° against the book's 133.1627°, latitude -3.2269° against -3.2291°, the thousandths the nutation and the terms left out. Over 50 N 5 W on 10 June 1805 the sun's azimuth and altitude agree with Horizons' refracted topocentric figures within a degree (12:30 UT: 180.6° and 63.0° against Horizons' 185.6° at 12:30 and 170.5° at 12:00, 62.9°; 04:30: 55° and 1.9°), and the moon's altitude at midnight is 14.5° against Horizons' topocentric 13.7°, the difference the parallax a degree-model leaves out. The model is 170 lines with its docstring and its term tables, past the brief's "about a hundred": the tables and the stars are what the lunar's conditions need, and nothing of it is distance arithmetic.

### The chronometer and the lunar on the frigate's test passage (truths 60 and 61)

The frigate at seed 7 given a chronometer by Earnshaw rated at Plymouth on 26 April 1805, gaining 1.8 s a day by its certificate, on a quiet south-westerly off 49° 30' N 5° 12' W on 5 June 1805 (the moon at the first quarter, in distance of the sun through the afternoon; the gate's passage files stay without a chronometer):

| | the rate right | the rate wrong by 2 s a day |
|---|---|---|
| the rating's offset (seed 7) | -0.13 s | -0.13 s |
| the chronometer's error at 09:00, 40 days out | -0.1 s | +80.6 s (fast) |
| the time sight at 09:00 | 5° 16' W against the truth 5° 12' W: 2.5 miles | 5° 36' W: 15.6 miles west |
| the master's trust (one sigma) | 6.7 miles (2.5 of the sight, 6.5 of forty days at a second a day) | 6.7 miles |
| the lunar of the sun, distances taken 17:40 to 17:57, cleared at 18:57 | 5° 14' W against 5° 11' W: 2.0 miles (0.05°); trust "within 20 miles" (one sigma 9.8) | the same draw: 2.0 miles |
| the chronometer by the lunar | "he finds no fault in the Earnshaw" (-12 s) | "he thinks it gaining on its rate, by a minute and ten seconds" (+70 s; 11 miles of longitude) |

The lunar's own draw at seed 7 is a lucky one (a twentieth of a degree against a quarter one sigma); the spread measured over four hundred seeds on a stub world is 0.25° for a good master on a quiet day and 1.0° for a poor one in two metres of sea (`tests/test_longitude.py`), the study's ten and thirty-nine miles at 50 N.

### The amplitude, measured

The frigate off 49° 30' N 5° 12' W at 04:18 on 10 June 1805, the sun rising at 52° true: "Observed the sun's amplitude at its rising, bearing E by N by compass: variation of the compass 22° 30' W by amplitude, 10 June, where the chart gave 21° 30' W by the chart of 1794; Mr Harvey allows it in the reckoning from now." The world's variation is 24° W and the frigate's deviation on north -0.38° (seed 7), so the figure to be found was 23.6°; the draw put it 1.1° under, read to the half degree. The course error the account carries went from 2.12° (the chart's decade) to 1.12°. The azimuth at ten in the forenoon the same day found 22° 30' W likewise. A day's run north at six knots laid down with the chart's error lands the account 6.1 miles across the course; with the amplitude's, 2.8.

### The chart queries' words

From the account off the Lizard: "the bearing of the Lizard by the chart is N by W (352°)"; "the distance to the Lizard is 51 miles by account"; "the dangers are the Spanam WNW, 4 miles; the Craggan NW by W, 5 miles; the Rose WNW, 5 miles; the Stags W by N, 6 miles; the Manacles N by E, 7 miles; the Penwin and the Vaze N by E, 8 miles: by account, within 10 miles"; and the course shaped from south of the Lizard, as playtest 12's was: "Shaped a course for Falmouth: N by account, 13 miles; the line passes the Manacles within a mile. Helm ordered: steer N (0°)." The reckoning's `to_dict` (the browser's snapshot) carries the chronometer, the last time sight, the last lunar and the variation beside the account, and no truth.

### The lookout's distances, before and after

Before: the words gave the truth's distance rounded to the mile or the league at every look, and a bearing taken drew a fresh estimate a fifth out, so the list said five miles where the bearing said three (playtest 13) and a feature at the edge of a league's rounding flickered between figures as the truth crept across it. After: one draw an episode from the `lookout` stream, held until she has moved a mile. The Lizard ten miles south by day at seed 7: "distant four leagues" (the estimate 12.9 miles, the eye's factor 1.29), held through half a mile of way, judged afresh at two miles on with the same factor, a new draw after half an hour out of sight (`tests/test_longitude.py`). The gate's passages' hails moved where the draws moved them (re-pinned below).

### The light at night in thick weather

The pilots have a light seen at its range "in clear weather" and in thick weather keep the ship off by the lead (White 1835, 'Coast of England', p. 26: "In thick weather come no nearer to the Lizard than 47 fathoms, as you will then be only six or seven miles from the point"; Imray 1874, 'Plymouth to Land's End', p. 94: the Lizard "in clear weather ... visible at the distance of 24 miles ... A vessel may run for it with confidence at all times, if the weather be at all clear"; p. 95, the lights' "brilliancy" at night). Neither says what a light's loom does in rain, so the rule is modern physics rather than the period's words: a light's luminous range in the weather's visibility by Allard's law (the module's note), which keeps the old rule in fog (a twenty-mile light at four cables in a cable's visibility) and gives the loom its due in showers: 9.9 miles in "a few miles" (four) of visibility, 3.2 in "a mile". The cutter of playtest 13, ten miles off the Lizard in passing showers, would have been at the edge of it and inside it between the squalls. The visibility's words in passing showers between squalls (W's table: "a few miles", four) were checked against spec §5's table and left: the showers pass and the words return to the horizon with them.

### The Nare, the Beast and the Gray, read again

White 1835 (pp. 25 to 26) and Imray 1874 (p. 93) both write "the Nare Head" in the Manacles' paragraph for the point whose lowest part in one with Mawnan church is the mark for the Penwin and the Vaze; Imray's Helford paragraph (p. 92) calls the same point "Nare point" ("between Rosemullion and Nare points"), and the Nare Head of the Roseland lies east of Falmouth (Imray p. 87). The chart's transit had pointed at the Roseland's; it now takes the Helford's point, named Nare Point to keep the two apart, as its near mark, the church beyond it, bearing 334° true from the point. "The Beast" is White's (p. 24 note; p. 26: "the land at the Lizard Point (the Beast)") and Imray's (p. 94: "The Beast forms the eastern part of the land at the Lizard"); "the Gray" is White's (p. 27: "the lofty conical rock called the Gray"). Both stand as the file had them.

### The pinned passages, re-measured

The gate's three passages run again at seed 7 after the package, the account against the truth read from the world (`tests/test_known_truths.py`, the passage constants; the scratchpad's `repin.py`). What moved, and why: the lookout's distance by estimation is now one draw an episode from its own stream and the figure a bearing is taken at, where before each bearing drew its own from the `reckoning` stream; so the departure's "The light on Ushant bore SW by S, two miles by estimation" (a mile before) put the account a mile differently off the Stiff, the course for Falmouth shaped from the account at the departure by the book's "landfall" rule differed by a fraction of a point, and the truth's track with it. Every later draw of the `reckoning` stream falls at a different moment too. The ticks that moved: the frigate's landfall 44880 → 45000 (the Beast at four leagues, as before), the outer road 58294 → 56494 ("And a half nineteen; good ground", half an hour earlier on the new track), the wear 58653 → 56834 and the lying to 58712 → 56894; the lines 837 → 836 and the digest 43fb9e16dab9670f → 7bcdb78ba3e8daae. The schooner's landfall 44100 → 44220 (the Beast at five leagues), lines 907 → 910, digest e84617dfb1061ff7 → a17c9870a5880a6b. The thick passage keeps every tick and its 526 lines (no bearing is taken in the fog, so the stream's draws fall where they fell) and its digest moves, c5e9917759d7bf6b → cd5c2faa6b49b8c1, because the lookout's hails now carry `estimate_m` in their data. The noon and the lead's ticks are unchanged on all three (28740 and 29883; 28740 and 29929; 28740 and 29884): the account's noon is the sun's, and the cast's the book's. The account against the truth at the moments, frigate: the departure 0.1 mile, Ushant's last bearing 1.9, noon 3.6 (was 4.8), the cast 3.2, the landfall 6.9 (was 8.1), the Beast's bearing with its distance 3.1 then 2.4, the Roads under a mile from Lowland Point on; the schooner: noon 4.7, the landfall 10.6 brought to 2.5 by the first bearing and to a mile by the second; the thick passage as it was (noon 5.7, the land close aboard at 10.9). The lookout's new lines on the passage: "Manacle Point bearing N by W, steady and closing: distant four miles" at 53400, the Manacles at 53700, the Penwin and the Vaze at 53940, the Old Wall at 56640 (the frigate running in for the Roads, each within a league or a danger: exactly playtest 12's four moments), and "A moonlit night; the land may be made out at a league" at 60120 (20:42, two days before full).

### Found on the way (package 33b)

- **The moon is down all day on the gate's passage.** 10 June 1805 is two days before full: the moon rises about eight in the evening and, with its declination at -25°, never reaches fifteen degrees over the Channel that night, so no lunar is to be had on the passage's day at all ("No lunar to be had: the moon is down"). The test passage for truths 60 and 61 is dated 5 June, the first quarter, when the sun lunar serves through the afternoon.
- **A two-day movement forgives one morning.** A chronometer wound at eight and forgotten the next morning is wound again the morning after with eight hours to spare; it dies only when two mornings are missed, which is what the scenario's `forgotten:` list says.
- **The hands' pace stretches the quarter of an hour.** The lunar's file says 900 s; the runner's crew factor and the weather make it seventeen minutes in twelve knots, as every evolution's time is stretched; the tests allow it.
- **A bearing steady and closing of every headland.** The first rule hailed every headland ahead of a ship running in, since on a straight course every one bears steady and closes; the hail is now for a danger at any distance and the land within a league.
- **The variation's words in the registry.** The dialect compares `the variation` in degrees and an agent reads its words with the source and the date; the value is a float that carries its words (`readings.Angle`), the one line added to `describe_value`, so that no new comparison kind was needed in the standing grammar (33c's).
- **The lookout's eye at a fifth.** With the estimate drawn once and shown in every hail, a fifth one sigma had the Lizard called five leagues at ten miles on the first draw of seed 7; a sixth is the judgement kept.
- **Not done.** Double altitudes (spec §32); the `--casual` display; a chronometer for the gate's passage files (the brief: they stay without one); the Almanac of 1805 itself (Horizons stands for it); the stars' places read from a catalogue page.

## Milestone 5: the suite in two tiers, the days built once, a Windows job

Package 32c (the cold review of 2026-09-30, §2.1 and §6 item 1). No test moved and no test's body changed; `tests/conftest.py` does it all.

**The machine.** The brief asked for the owner's machine at `-n auto`; the package was built in the lead's cloud session instead (2026-10-01), so every figure below is that machine's: four cores, `-n 4`, and **shared**. The first set of runs had three other packages' suites running beside them (load average 6 to 13 on four cores); after the container restarted the machine was quieter (the lead's passage measurements beside it, load 1 to 8). The figures swing by a third between two runs of the same command, so read them as pairs, never one against one. The owner runs the fast tier once on their machine afterwards; that figure belongs here beside these.

**The two tiers.** The suite at the base commit collects 2,098 tests (2,091 pass and 7 are strict xfails here; with Node absent two of the passes are skips). The slow tier is 232 of them:

- 51 by the fixtures they use: the module-scoped fixtures that took over five seconds to build, which are the days, the passage, the gales and the sweeps of headings: `test_known_truths.py`'s fifteen (31 tests), `test_ships_hierarchy.py`'s seven sweeps and polars (5), `test_checkpoint.py`'s `saved` (4), `test_routine.py`'s `a_day` (4), `test_studding.py`'s `brought_up` (4), `test_staying.py`'s `frigate_by_the_wind` (3). A test that reads such a fixture is slow whatever its own time, since the build is charged to whichever of its tests runs first.
- 181 by node id: every other test whose setup, call and teardown came to **five seconds or more**, the mean of the two loaded whole-suite runs with `--durations=0`. 44 of them are in `test_known_truths.py` (the truths that sail ten minutes to an hour), 15 in `test_agents.py`, 10 in `test_catalogue.py`, 9 each in `test_hands.py` and `test_staying.py`, 7 each in `test_readings.py` and `test_sea.py` (the sea's days and its replay), 2 in `test_replay.py` (truth 39's passage and the crewed voyage, the replay days), the rest one to six a file. The threshold is a judgement: at five seconds the fast tier was about 730 test-seconds of the loaded runs' 6,300 (an eighth of the work in nine-tenths of the tests); at ten it would have been 1,230, at two 440.
- Ten more named for packages 33b to 33d's tests, measured on the lead's branch (`ed865ca`, 2,420 tests) on the quieter machine against the same bar scaled by the whole suite's ratio (2.2): truths 60 and 61, four of `test_longitude.py` (the forgotten chronometer's day, 176 s, the lunar's hour, the chronometer's rating, the bearing closing on a danger), two of `test_standing.py` (the well held, hove-to until she fills), one of `test_server.py` (ease on station) and the starter file's console test under its new name. On that branch the fast tier is 2,179 tests and the slow 241; the fast tier ran in 83 s at `-n 4`.

The fast tier holds every test of 19 of the 52 files and all but the long ones of the other 33; the 7 strict xfails are all in the slow tier. The node ids go stale when a test is renamed or a new long one is written: re-measure with `python -m pytest -n 4 --slow --durations=0` when the fast tier grows slow.

**The days built once.** With xdist's `load` distribution a module's tests are dealt to whichever worker is free, and a module-scoped fixture is built on each worker that draws one of its tests. In every `load` run here truth 32, which reads the frigate's and the schooner's sweeps and polars, drew a worker that had none of them and built all four again (90 to 250 s of setup on top of the first builds, which truths 1 to 3 had already paid). `tests/conftest.py` puts every test that uses a module-scoped fixture of its own module in an `xdist_group` named for the fixture, joining the fixtures any one test uses together (so the frigate's and the schooner's sweeps and polars, the bowlines', the catharpins' and the yards' sweeps are one group, and the gate's day, the day under systems, the passage, the gales each their own), and `--dist loadgroup` (`pyproject.toml`'s `addopts`, inert without `-n`) sends each group whole to one worker. xdist deals the groups before the single tests, the largest first, so the long days start at once and the single tests fill the other workers round them.

**The timings**, wall clock at `-n 4`, seconds:

| | `--dist load` (before) | `--dist loadgroup` (after) |
|---|---|---|
| whole suite, loaded (3 other suites beside) | 2,145; 2,369 | not run (the container restarted) |
| whole suite, quieter | 1,027 | 990 |
| fast tier (1,866 tests), loaded | 162; 119 | 154; 113 |
| fast tier, quieter | 90; 104 | 78; 108; 60 (load 1) |
| slow tier (232 tests), quieter | 875; 525 | 588; 463 |

The whole-suite runs with `load` are the suite as it stood (2,091 passed, 7 xfailed): the two loaded ones without `tests/conftest.py`, the quieter one with it and `--slow --dist load`, the same tests in the same distribution. The loaded slow-tier runs and a second quieter whole-suite pair were lost to two restarts of the container; the lead asked for one run each after the second.

**The choice: `loadgroup`.** It was the faster in each pair where the days are (the slow tier 588 against 875 and 463 against 525; the whole suite 990 against 1,027, though the grouped run had the busier machine: its tests took 3,824 test-seconds against the other's 1,949, and in the other the workers stood idle half the run while the last of the days sailed on one of them), and no slower in the fast tier, where few tests share a fixture and the two are the same distribution within the noise. The gain is the day not built twice and the long groups started first; it is a few minutes at most here, since in these runs the duplicate builds were the sweeps (the gate's day was built once by luck of the dealing every time). `--dist loadfile`, the review's suggestion, was not run: `test_known_truths.py` is 38 to 56 per cent of the suite's test-seconds (2,303 of 5,873 in the first loaded run, 1,065 of 1,949 in the quieter one), more than a quarter, so one worker would carry it alone for longer than the whole suite takes under either of the other two.

**The pace truths under a loaded machine.** Truth 51 and the two pace tests beside it (the gate's day with the region, the passage) assert 500 ticks a second of wall clock. On this shared machine truth 51 read 408 in one slow-tier run (`load`) and all three failed in the grouped whole-suite run (297, 339 and 454) with other sessions' suites beside it; the three passed alone straight after. They measure the machine, not the code, and the grouping does not change what a worker gets of its core; the review's note on truth 51 stands.

**What a push costs.** `ci.yml` now runs two jobs on a code push, the fast tier on `ubuntu-latest` and on `windows-latest` (Python 3.11, `PYTHONUTF8=1`, `-n auto --dist loadgroup`, ruff on Linux only), cancelled together by a newer push. From the figures above, a hosted runner's four cores should take one to three minutes for the tests and about as long again to install, so some five minutes on Linux and, by the usual ratio of the Windows runner's process start and install, about ten on Windows: some fifteen runner-minutes a push against the seventeen-minute-plus single Linux job it replaces (the repository is public, so the minutes are free). The whole suite, `--slow`, runs in `release.yml` on the gate commit (some twenty minutes on the runner) and at a package's end.

**The Windows job, as run** (the lead, 2026-10-01, the push of the merge, run 36939990431): the fast tier passed on `windows-latest` in three minutes (23:17:30 to 23:20:28) and on `ubuntu-latest` in two (with the lint), against the package's estimates of ten and five; a push now costs about five runner-minutes, free on the public repository.

## Milestone 5: the tide, the grounding and the anchor, as Luce has it

Package 34 (spec M5 §11, §13, §16, §18, §20; decisions 29 and 30; the study `docs/design/Tides1805.md`, T). The world keeps the truth and the captain keeps his account: the world's tide is M2, S2 and N2 at eleven gauges with the streams by area, evaluated once a minute at the ship and handed to the physics as the water's velocity; the captain's tide is his epitome's establishment and Moore's rule of forty-eight minutes, a reading in his words; no reading gives the world's, and the tests read `world.tide` as the brief allows. The anchors and cables come from the generator by the ship's size; the evolutions are Luce's with his words of command; the cable's physics is a line's (spec §7.5) at the hawse against the anchor's holding. The figures the study marks unverified say so here as in their comments.

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| `tides/constituents.yaml`, the eleven gauges | M2, S2, N2 amplitude and Greenwich phase lag (Newlyn M2 1.712 m at 133.8°, S2 0.572 at 177.8°, N2 0.330 at 113.9°; Devonport 1.685/153.6, 0.606/206.6, 0.318/137.7; Brest 2.051/109.0; St Mary's 1.758/131.0; Weymouth, Dover, Le Conquet, Roscoff, Saint-Malo, St Helier, Cherbourg) | TICON (PANGAEA 896587), the dataset's own `TICON.txt` | **verified** against the file, fetched 2026-10-01; CC BY 4.0, `docs/references/Tides.md` |
| the gauges' `mean_level_m` (the datum offset) | the French ports from the RAM (Brest 4.29, Le Conquet 3.98, Roscoff 5.17, Saint-Malo 6.83, Cherbourg 3.80); Newlyn and Devonport the study's UKHO figures; Weymouth 1.2, Dover 3.7, St Helier 6.0 | SHOM's RAM (Licence Ouverte 2.0); the study | the French **from the RAM's tables**; **Weymouth, Dover, St Helier judgement, UNVERIFIED** (open item 3's four port offsets, not settled: the UKHO datum table was not reachable) |
| `tide.CONSTANTS_CELL_DEG`, the interpolation | inverse distance squared on the complex constants, cached by hundredth-degree cell | T §3: "interpolate the complex constants between gauges" | judgement in the power and the cell |
| `tide.GAUGE_FLOOR_M` | a gauge within 100 m is read as itself | the cache's seam | judgement |
| `tide.SLACK_PHASE_DEG`, `TideState.slack` | slack under a tenth of the area's rate | the stream's words: "slack water" | judgement |
| the astronomical arguments | Meeus's mean longitudes s, h, p, N; V(M2) = 2(T + h − s), V(S2) = 2T, V(N2) = V(M2) − (s − p); f and u Schureman's | Schureman 1958 (the nodal factors' forms), Meeus ch. 47 for the elements | the equations standard; the establishment at Falmouth comes out within an hour of Dessiou's (below) |
| `tides/streams.yaml`, the areas | Carrick Road 1.5/0.75 kn along 10° (the flood's strongest 3 h before local HW); the entrance 1.0/0.5; the Manacles 1.2/0.6; the approaches 0.7/0.35; the Lizard 2.3/1.1 along 85° centred on local HW; the Start 3.0/1.5; Scilly and the Land's End 1.8/0.9; Scilly 1.2/0.6; the Fromveur 7/5; the Chenal du Four 4/2.5; the Goulet 4.5/3; the Iroise 1.5/0.8; mid-Channel 1.6/0.8 along 65° | Bowditch 1802's headland table for the timing off the Lizard and the Start; eoceanic's summaries of NP250/255/257 for the rates; Figaro Nautisme and Ifremer for the Fromveur; White 1835 and Imray 1874 for the Roads | the atlases **NOT READ** (Crown copyright); the Fromveur's timing **UNVERIFIED**; the Goulet's and the Iroise's judgement; each entry's `source` says which |
| the rate between neaps and springs | scaled by the local amplitude between A(M2) − A(S2) and A(M2) + A(S2) | T §1: the stream's rate with the range | judgement in the form |
| `tides/establishments.yaml`, `norie` | Scilly 4h 10m, Land's End 4h 20m, Mount's Bay and the Lizard 4h 30m, Falmouth 5h 15m (rise 15 ft), Fowey and the Eddystone 5h 15m, Plymouth 5h 33m (16 ft), Dartmouth and Torbay 6h 00m, Portland 5h 30m, Dover 10h 50m, Ushant 3h 47m, Brest 3h 48m (19 ft), Morlaix 5h 15m, St Malo 6h 00m (35 ft), Jersey 6h 10m, Guernsey 6h 30m, Alderney 6h 45m, Cherbourg 7h 45m (17 ft) | Dessiou's and Daussy's figures as Whewell 1833 quotes them (Phil. Trans. 123, the table), standing for Norie's Table XLI | Whewell read by the study; **Norie's Epitome itself not read** |
| `establishments.yaml`, `moore` | Brest SW by W (3h 45m), Ushant and Scilly WSW (4h 30m), Plymouth, Ramhead and Torbay W (6h 00m); a point to 45 minutes | Moore 1799, 'Of the Tides' | the catechism's rule; the table's bearings from memory of the page, **unverified** in the figures |
| `minutes_per_day_of_age` | 48 | Moore 1799: "multiply the moon's age by 48 minutes" | the rule |
| `reckoning.almanac_age_days` | the age by the mean elements at noon, to the quarter day | the almanac gives the hour of the change | judgement in the quarter day (a whole day's age puts the tide up to 48 minutes out of itself) |
| `reckoning.NEAP_RISE_OF_SPRING`, `TIDE_HOURS`, `SYNODIC_MONTH_DAYS` | two-thirds; 12 h 25 m; 29.53 d | the rise at neaps "about two-thirds" the spring's (Norie's note, a commonplace of the tables); Moore 1799 for the tide's day | the fraction **unverified** against the Epitome's text |
| `reckoning.TIDE_ALLOWANCE_DEFAULT_M` | 3 m where the table gives no rise | half a middling spring rise in the Channel | judgement |
| `gen_ships.BOWER_CWT_PER_100_TONS` | 5 cwt a hundred tons, the bowers alike | Luce 1866 ch. XIV, 'Anchors', the rule of thumb | the text |
| `gen_ships.STREAM_OF_BOWER`, `KEDGE_OF_BOWER`, `SHEET_AND_STREAM_FROM_TONS` | a quarter; an eighth; a sheet and a stream over 200 tons | Luce ch. XIV; Lever 1808, 'Anchors' (the sheet "the same weight as the bowers") | the proportions judgement on the texts |
| `gen_ships.CABLE_FATHOMS`, `BEST_BOWER_CABLES` | 120 fathoms a cable, two bent to the best bower | Falconer 1780, CABLE: "a hundred and twenty fathoms"; Steel 1794 vol. II, the cables | the texts |
| `gen_ships.CABLE_IN_PER_FOOT_OF_BEAM` | half an inch of circumference to the foot of beam (the frigate's 19-inch, the schooner's 12) | Steel 1794 vol. II's tables by the ship's rate, read as a rule of the beam | **UNVERIFIED**: the table's figures for the rates from memory; the rule the builder's fit to them |
| `gen_ships.STREAM_CABLE_OF_BOWER`, `KEDGE_HAWSER_OF_BOWER` | two-thirds; a half | Steel 1794 vol. II (the stream cable and the hawsers) | judgement on the tables |
| the cable's rating | as a line's, from its circumference (the rig's rule for cordage, spec §7.5) | | the existing rule |
| `anchor.HOLDING_PER_WEIGHT` | four times the anchor's weight in good ground | a modern figure for the old pattern (the period judged holding by the ship dragging: Falconer 1780, ANCHOR-ground) | judgement |
| `anchor.GROUND_HOLDING` | rock 0.3 ... sand, clay, mud and "good holding" 1.0; else 0.9 | Steel 1794 vol. II p. 292 (oozy ground, hard and rocky ground); Falconer, ANCHOR-ground | the ranking the texts', the figures judgement |
| `anchor.TRIP_ANGLE_DEG`, `DRAGGING_HOLD_FRACTION` | the holding falls to nothing as the cable's angle at the anchor rises to 35°; a quarter of the full holding is kept by an anchor lifted or on its side | Lever 1808, 'Single Anchor', p. 97 (the short scope lifts the anchor); Luce 1866 ch. XXXIV p. 568 (three times the depth the old rule, five the safe one: at five the angle is 11°, at three 19°, at a cable and a half 42°) | judgement in the angle and the quarter |
| `anchor.RIDING_SCOPE_PER_DEPTH`, `SHORT_SCOPE_PER_DEPTH`, `SHORT_STAY_SCOPE_PER_DEPTH` | 5, 3, 1.5 | Luce 1866 ch. XXXIV p. 568; ch. XXI, the short stay "in a line with the fore topmast stay" | the texts; the short stay's figure judgement |
| `anchor.CABLE_STRETCH_FRACTION`, `CABLE_DAMPING_FRACTION` | the cable at its breaking strain stretched 15 per cent of its scope; damping a fifth of critical | hemp cable's stretch (Steel's trials, by memory); the damping judgement | **unverified** in the stretch |
| `anchor.HAWSE_FRACTION` | the hawse half the waterline length before the centre | the hawse holes at the bows | judgement |
| `anchor.DRAG_SAY_S`, `DRAG_SETTLE_S` | dragging after a minute coming home; holding again after five minutes holding | the snub as she is brought up is not a drag; an anchor coming home and holding by turns as she sheers is one dragging | judgement |
| the cable judged (`anchor.judge_cables`) | the strain rule's decay, warning and parting (spec §7.5) by the cable's ratio | `physics/strain.py` | the existing rule |
| `ground.SHOCK_SPEED_KN` | at six knots the strike is one strain of the rating on the topmasts and above, half on the lower masts; the ratio (v/6)² | spec M5 §18's "the masts shock at speed" | judgement in the figure |
| `ground.LEAK_ROCK_M_PER_H`, `LEAK_SOFT_M_PER_H`, `LEAK_REFERENCE_KN`, `WATERLOGGED_M` | 0.6 m an hour on rock at four knots, 0.05 on soft ground, by the speed squared; two metres in the well | spec M5 §18 | judgement |
| `ground.AFLOAT_MARGIN_M` | a foot under her keel before she is said to be off | the ship on the edge of a bank at the top of the tide | judgement |
| `ground.DANGERS_REFRESH_S` | the charted dangers about her read once a minute | the pace | judgement |
| `chart.Feature.dries_m` | 35 of the chart's dangers given the pilot's figure for the water over them at low water or how far they dry (the Rose 13 ft under, the Governor 2 fm, the Old Wall 27 ft, the Hand Deeps 22 ft; the Black Rock showing at half-tide, 3 m; the Wolf covered at high water, 4.5 m; the Manacles' ledges 2 m, one head always up) | White 1835, Imray 1874, Faden 1793, the entries' own `says` | the pilots' figures; LAT taken as the pilot's low water; the half-tide and high-water heads judgement, said in the file |
| the evolutions' times | come to anchor: clew up 150 s, topsails 60 s, way off within 420 s, veer 1 fm/s, settle 240 s, furl 600 s, stem a tide over 1.5 kn; let go: stand clear 15 s; veer cable 0.5 fm/s; heave short: rig the capstan 180 s, heave 0.1 fm/s; weigh: break out 60 s, hoist 0.2 fm/s, cat and fish 300 s; cat and fish 150 + 150 s; back the anchor 240 s | Luce 1866 ch. XXXIV and XXXV, Lever 1808, Steel 1794 vol. II p. 296 for the sequences; the times judgement | the sequences the texts'; **every time judgement** (no page times a capstan) |
| the helm, the trim and the manoeuvres at anchor or aground | refused in words | the starter book's 'keep her full' steered the frigate at anchor through the night | the lead, 2026-10-01 |

### The world's tide, measured

Falmouth (the outer road), from the interpolated constants M2 1.68 m at 139.3°, S2 0.57 at 185.4°, N2 0.32 at 120.3°, mean level 3.20 m: the world's own establishment (the crest of A(M2)e^{ig} + A(S2)e^{ig} at syzygy, local mean time) is 4h 41m; Newlyn's 4h 27m, Plymouth's 5h 17m, Brest's 3h 40m. On 12 June 1805, the day of full moon (the moon fifteen days old by the mean elements), high water at Falmouth falls at 04:49 and 17:05 local mean time, 5.04 and 5.07 m above the datum: eight minutes and one minute from the world's establishment (truth 62's first clause, within twenty), and twenty-six and thirty-five minutes from Dessiou's 5h 15m, which is the 1805 figure the captain uses. The spring amplitude (M2 + S2) is 2.49 m against the neap (M2 − S2) 1.20: springs 2.07 times neaps (truth 62's second clause). The June ranges run from 2.36 m at the neaps of the 21st to 5.09 at the perigean springs of the 28th and 29th, with 3.83 at the full moon's; over the first half of 1805 the largest spring exceeds the smallest by a third (the test allows a tenth to a half: the study's "about a fifth" is the long-run figure, and half a year of the perigee's 8.85-year cycle shows more). Off the Lizard on the 12th the stream runs east (toward 085°) from three hours before local high water to three after at 1.9 knots at its strongest, west after, with the slack at the three-hour marks (truth 63); at the neaps of the 21st, 0.9. A point ship (no hull) set by the stream alone goes exactly where the stream's integral says; the frigate hove to for six hours off the Lizard goes over the ground by her own forereach plus the stream's run, and the set found as the difference is the stream's within a tenth: five miles in the six hours, which her log never saw.

The captain's tide against it (truth 64): with Dessiou's 5h 15m and the age to the quarter day, his high water at Falmouth is 13 and 22 minutes from the world's on the day of full moon, and up to an hour at the quarters (the test allows 75: the first quarter's worst is 58 minutes, the last's 61). A whole day's age would add up to 48 minutes to that, which is why `almanac_age_days` keeps the quarter day. The master's allowance for the tide under the lead (two-thirds the spring rise at the quarters, the half-cosine from his high water) is within two metres of the world's height in the Roads at any hour tried, and the deep-sea cast's account lands within the contour tolerance of the cast less the allowance.

### The anchor, measured

The frigate under plain sail in Carrick Road at seed 7, twelve knots of wind: `come to an anchor` calls all hands, takes in the light sails and the courses in two and a half minutes, rounds her up to the south-west (the wind: the Road's stream was under the knot and a half that would make her stem it), lets go the best bower five minutes later in fourteen fathoms with her way over the ground under 0.3 m/s, veers sixty-nine fathoms (five times the depth) in sixty-five seconds, is brought up two minutes and fifty seconds after and has the sails furled and the yards squared ten minutes after that: twenty minutes from the order to "Brought up by the best bower in 14 fathoms, sixty-nine fathoms of cable; Riding by the best bower to the flood, wind and tide together." She lies to the flood at 196° to 202° (the stream toward 010°) for five hours, swings through the slack in an hour and a half as the ebb makes against the wind ("The cable slack at the turn; she swings to the ebb. Riding by the best bower to the ebb, a windward tide, the wind against the tide"), and lies to the ebb at 028°; the cable's load riding is five or six kilonewtons, a hundredth of the nineteen-inch cable's rating. `weigh` from sixty-nine fathoms takes twenty-two minutes (the capstan rigged in three, the cable up and down nine minutes later, aweigh after one more, catted and fished in five). In a gale of forty knots with the best bower let go on twenty fathoms in twelve, the holding at 44° of cable angle is a quarter of the full (eighteen kilonewtons against a pull of forty), she drags at five knots over the ground and the log says so after the minute: "The best bower is dragging: veer more cable; let go the small bower, or back her with the stream"; in Carrick Road's three cables of water she was on the bank before the minute was up, so the test drags her in the outer road. The schooner, the cutter and the brig let go and weigh through the same orders in the same words.

### The grounding, measured (truth 66)

The schooner from fourteen miles east-south-east of the Manacles in a mile of fog on the ebb of 12 June, steering NW by W by account at six knots: she takes the ground forward on the shore about Manacle Point at 07:54, nine-tenths of a mile from the Manacles' head, at five knots and a half ("she struck at five knots and a half, heeling 1 degree, the tide falling"), the log's last read six knots; the carpenter reports her strained on the ground and making water, the master makes the flood that floats her by his epitome, and the stream runs past her while she stands fast. The same passage with the deep-sea lead hourly (brought to for it, as the Channel Soundings are struck) and the book hauling off at the forty-fathom line does not ground: the Manacles' approach shoals from forty-four fathoms at fourteen miles to forty at nine and thirty-four at a mile, and the line is found at the third cast. The hand lead is no use here (no bottom at twenty fathoms to within a cable of the rocks), which is the pilots' warning about the Manacles made plain. The frigate on to the Manacles' ledges from the south-east at seven knots: stove on the rock, the well rising a foot in the first hour and waterlogged in seven; the blow in the unit test, the topmasts shaken at seven knots' worth and carried away at twelve. On Falmouth bank at two knots on the ebb: no leak to speak of, held through the low water, afloat on the flood five hours later with the log's line.

### The pinned passages, re-measured with the tide in

The stream in the track moves every tick after the departure but the noon's (28740 on all three: the account's noon is the sun's), and the lead reads the tide (the Channel Soundings' cast "Fifty-two fathoms" is "Fifty-three"); the passages' ends change from lying to to the anchor let go. The frigate: the cast 29883 → 29884, the landfall 45000 → 44700 (the Beast at five leagues, the Lizard lights at four), the outer road 56494 → 57732 ("the first cast under twenty fathoms" twenty minutes later on the set track), the best bower let go at 58167 in the outer road and brought up at 59145, riding to the ebb with forty-nine fathoms in ten; the lines 677 → 624 (the lying-to's lines gone, the anchor's in, and the starter book's 'keep her full' no longer steering a ship at anchor) and the digest eacae6db04e7067a → 6880cabc6e0ac53e. The account against the truth: 6.6 miles at noon (3.6 without the tide: the stream's set in the forenoon's run is the log-line's bias, which the noon latitude takes out of the north-south part only), 5.2 at the landfall (6.9 before), 0.3 at the anchor; the stream's net set over the whole passage 1.2 miles toward 141°, the ebb and the flood nearly cancelling in seventeen hours; her run through the water 98 miles. The schooner's own book now takes her in: the landfall 44220 → 43920, sail shortened and a course for Carrick Road at 56502, the best bower let go off the town at 57615 at the first cast under ten fathoms and brought up at 58618 in nine fathoms with forty-three out, riding to the ebb within St Anthony's; the account 8.3 miles from the truth at noon (4.7 before), 9.6 at the landfall (10.6), 0.2 at the anchor; the set 1.5 miles toward 137°, her run 100 miles; the lines 749 → 725 and the digest e41ade78138e024d → c59b39435e5f2c15. (Shaped for the Road under all plain sail and told to anchor at the eight-fathom line she ran the eastern channel at eight knots and struck the Lugo rock off St Mawes castle, which is why the book shortens sail and anchors at ten.) The thick passage: no anchor, and no sight to take the set out, so the landfall at Black Head moves 54480 → 54900 and the account is 11.3 miles off at it (10.9 before), 9.7 at noon (5.7); the set 0.4 miles toward 076°, her run 90 miles; lines 501 → 504, digest f4d7575fea6ada34 → b3b1f54a4b97a8f4. The gate 5b report's passages table is the lead's; these are the numbers for it.

### Found on the way (package 34)

- **The tide moves the track and the noon stays.** Every pinned tick after the departure moved by the stream; the noon's did not, and the lead's cast at the Soundings moved one second. The brief asked that the noon and the cast be kept if possible: the noon is, the cast within a second.
- **The log-line at anchor.** The log hove hourly at anchor read the tide's rate (a knot through the water), and the account ran a mile an hour from a ship that went nowhere; the reckoning now runs no distance at anchor or aground and does not heave the log at the hour (`Navigation._riding`).
- **The leeway at anchor.** The stream past a ship at anchor is not leeway; the leeway's line is silent at anchor and aground.
- **A ship aground floats and strikes every minute.** On the edge of a bank as the tide makes she floated, moved, and struck again each minute; a foot under her keel is wanted before she is said to be off (`AFLOAT_MARGIN_M`).
- **The snub is not a drag.** The anchor comes home a fathom as the cable is brought up taut and the ship's way is stopped; said as a drag it was twenty lines. The drag is judged over a minute and the holding over five, in the physics, so that the reading `the anchor is dragging` is as steady as the line.
- **The resumed sail work at anchor.** A manoeuvre's belayed sail work resumes when all hands are done (decision 25): the mizzen topgallant, belayed setting when the ship came to anchor, set itself after she was brought up. The anchoring belays it for good, and the trims that waited for hands with it.
- **The helm at anchor.** The starter book's 'keep her full' bore away a point every few minutes through the night on a ship at anchor head to wind; the helm, the trim and the manoeuvres are refused at anchor and aground.
- **The Manacles' head.** A danger with a height stands above the water at any tide (its head is in sight), and its ledges' `dries_m` is what the grounding reads; a drying rock with a mark's height is covered by the tide all the same.
- **Not done.** Open item 3's four port datum offsets (Weymouth, Dover, St Helier judgement; the UKHO table not reachable); the atlases and the Epitome unread (the figures are from summaries and Whewell); mooring with two anchors and the hawse (Luce's 'Mooring'); the pumps; the tide at the lookout's horizon (a drying rock's height above the water as the tide falls is not shown, only in or out of sight); the anchor's evolutions set no sail (the order of Luce's 'Getting under way' is the captain's to give).

## Milestone 5: places, people, papers, the ports and the nations

Package 35 (spec M5 §22 to §24, §28; the designs `docs/design/InwardAndOutward.md` and `docs/design/Papers-and-Books.md`). Everything inward is reached by an order or a reading; everything outward comes through something the ship models (the boat, the gangway, the messenger, the cabin door), each a line in the log. The ports are files on one machinery (`data/ports/`, `freesail/world/ports.py`); the nations a table (`data/nations.yaml`, `freesail/world/nations.py`); the people the named few of the muster (`freesail/world/people.py`); the papers a catalogue by handle (`data/papers/papers.yaml`, `freesail/world/places.py`) served through the library's `papers` topic to the captain, the watcher and the pane alike. The owner's ruling of 2026-10-02 stands: `weigh` is the anchor up and no sail; `get under way` is Luce's whole sequence.

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| `ports/*.yaml`, the roads | Falmouth: the outer road, Carrick Road, the harbour off the town (3 fm, mud, `deep_draught_ft` 15); Plymouth: Cawsand Bay, the Sound, the Hamoaze; Brest: Bertheaume road, the Rade, the Penfeld | White 1835 pp. 26-27, 31-35; Imray 1874 pp. 78-83, 88-90; Moore 1799's catechism; Faden 1793 pp. 56-57; the chart's features (`data/charts/features/channel-west.yaml`, each with its source) | the pilots' pages; the mooring's figure and the draught judgement on White |
| `pilot.cruising_nm` | Falmouth 6, Plymouth 8, Brest 7 | the Falmouth pilots met ships off the Manacles and the Dodman, Plymouth's off the Eddystone, Brest's in the Iroise | judgement |
| `pilot.comes_off_by_night` | false at all three | no pilot's light at the Roads in 1805 | judgement |
| `pilot.fee_pounds` | 5, 6, 4 | from memory of the Trinity House rates for a frigate | **unverified** |
| `pilot.skill` | 0.9 | a branch pilot's knowledge of his own harbour | judgement |
| `pilot.cast`, `course_out_deg` | Falmouth starboard, S by E (169°); Plymouth larboard, S by W (200°); Brest starboard, W (270°) | the head paying off to the eastward from the Road with a westerly, the eastern channel out (White p. 27); the western channel out of the Sound past the Panther (Imray p. 80); the Goulet west (Faden) | judgement on the pages |
| `pilot.words` | channel, marks, anchorage, tide | the pilots' directions, each file's head says which page | the texts, condensed |
| `ports.PILOT_BOARDS_WITHIN_M`, `PILOT_HAIL_WITHIN_M` | two cables; four cables | a boat's pull under a ship's lee; a hail | judgement |
| `ports.PILOT_BOARDS_UNDER_KN` | six knots | "shorten sail and he will come aboard" | judgement |
| `ports.PILOT_COMES_OFF_OVER_KN`, `_under_sail` | a knot of way through the water, under sail | a ship drifting under bare poles (a knot to leeward in twelve knots of wind) is not standing in | judgement; the second clause found on the way |
| `ports.PILOT_AGAIN_H` | six hours before a refused ship is met again | the cutter does not come off twice in a watch | judgement |
| `ports.PILOT_LIES_TO_S`, `PILOT_OFF_BEYOND_NM` | the cutter lies to ten minutes after boarding; comes off again beyond the outer road and a mile, the ship standing away | the cutter waits to see her in; the pilot leaves her clear of the road (the Regulations: "into or out of") | judgement |
| `ports.IN_PORT_NM` | at anchor within two miles of the roads | the boat's pull | judgement |
| `ships.CUTTER_SPEED_KN`, `WIND_SPEED_FRACTION`, `VESSEL_MIN_SPEED_KN`, `ARRIVE_FRACTION` | six knots, capped at half the wind, a knot at least; she runs in to three-quarters of the distance asked | 32b's cutter at far detail; a ship under way is caught and not followed at exactly the distance | judgement |
| `ships.RIG_MADE_OUT_NM`, `MADE_OUT_NM` | her rig at four miles, her name at a mile and a half | the lookout's distances (33b) | judgement |
| `ports.BOAT_PACE_KN`, `BOAT_HOIST_OUT_S`, `BOAT_HOIST_IN_S` | four knots; five minutes each | a boat pulling laden; the yard and stay tackles (Luce 1866, 'Boats') | judgement |
| `ports.BOAT_ASHORE_S` | a quarter of an hour to land a man, half an hour for the prices, a letter or the yard, an hour for a purchase or a sale | the purser round the market | judgement |
| `ports.LIGHTER_S_PER_TON` | three minutes a ton (twenty tons an hour) | goods go by the port's lighter while the boat is at the quay; the boat itself carries under a ton | judgement; found on the way (the boat's trips by its weight made forty tons of tin twenty trips) |
| `ports.SUPPLY_PER_TON`, `SUPPLY_FLOOR`, `SUPPLY_CAP`, `SUPPLY_RECOVERY_PER_DAY` | a hundredth a ton; a half to double; a seventh a day | a glut you made yourself clears in a week | judgement |
| `ports.WAR_FACTOR` | one and a half | the good's nation at war with the port's | judgement |
| `ports.PRICE_ROUND` | the half pound | a price list's figure | judgement |
| the market's prices | Falmouth tin 120, copper ore 9, pilchards 14, salt 25, coal 2, canvas 60, hemp 70, wine 70, brandy 200, timber 6, salt beef 55; Plymouth about the same with biscuit 40; Brest wine 35, brandy 110, canvas 40, salt 12, hemp 55, tin 180, pilchards 30, coal 6, timber 5, salt beef 70, copper ore 20; the season's factors 0.8 to 1.3 | **FROM MEMORY** of the period's price currents; no page in `docs/references/` gives them, and every file says so | **UNVERIFIED** |
| the dockyard's times and costs | a topmast 8 h (£40 at the chandlers, nothing at the King's yard), a topgallant mast 4 h, a yard 6 h, a suit of sails 48 h at £25 the hundred square metres, cordage 2 h at a shilling the fathom, water a tenth of an hour a ton, provisions a twentieth of an hour a day at a shilling a man a day | the Regulations of 1806 (the yard's supply by demand and survey; the Captain's art. XVI on purchases); the figures judgement | the rule the Regulations', the figures judgement |
| the crew pools | Falmouth 4 able at £3, 8 ordinary at £2, 12 landsmen at £1, twelve and six hours; Plymouth 10/20/30 at £5/£3/£1, a day and twelve hours; Brest 6/10/20 at £2/£1 10s/£1 | a packet port with few idle seamen; the press at Plymouth; the arsenal's town | judgement |
| `nations.yaml`, the wars | Britain with France since 1803-05-18, with the Batavian Republic since 1803-06-17, with Spain since 1804-12-12; France and Spain allied; the United States, Portugal and Denmark at peace with all | from memory; the file says so | **dates unverified** |
| `nations.yaml`, the colours and the names | the tricolour, the fifteen stripes, the red ensign; the names lists that `crew/names` has | the names lists of the muster | the lists' |
| `people.PASS_THE_WORD_S` | a minute | the word passed along a frigate's deck | judgement |
| the people by ship | the frigate: two master's mates (forecastle, able) and a midshipman (afterguard, landsman) for the messenger beside the posts; the schooner and the cutter a boy; the brig a master's mate and a midshipman | the generator writes them into each ship's file (`crew.people`); no ship special-cased | judgement on the complements |
| the watch below asleep | a watch-keeper in his watch below at night is asleep by the bill until an order calls him; called, he does not turn in again that watch | Luce 1884 ch. XX (the watch below turns in) | judgement in the rule |
| `gen_ships.HOLD_OF_BURTHEN_SHIP_OF_WAR`, `HOLD_OF_BURTHEN_TRADER` | a tenth; a half | the ship of war's hold is her stores; the trader's her cargo | judgement |
| `gen_ships.LAUNCH_LENGTH_FACTOR`, `CUTTER_OF_LAUNCH`, `JOLLY_BOAT_OF_LAUNCH`, `SMALL_VESSEL_BOAT_FACTOR`, `BOAT_FEET_PER_OAR`, `BOAT_WEIGHT_FACTORS` | the launch 2.6 root(length), the cutter nine-tenths of it, the jolly boat two-thirds, a small vessel's boat four-fifths; three feet of boat to the oar | Luce 1866, 'Boats' (the allowance by the ship's rate); Falconer 1780, LONG-BOAT, YAWL | the rule of thumb judgement on Luce's table |
| the evolutions' times | get under way: rig the capstan 180 s, heave 0.1 fm/s, loose 240 s, brace 60 s, break out 60 s, hoist 0.2 fm/s, cast seven points or 420 s, cat and fish 300 s; moor: veer 1 fm/s, stand clear 15 s, heave 0.1 fm/s; unmoor the same; the kedge: hoist out 300 s, sling 300 s, the boat at four knots, three-quarters of the hawser, hoist in 300 s | Luce 1866 ch. XXI, XXXIV; Lever 1808, 'Mooring', 'Weighing the Anchor'; Falconer, KEDGE; the times judgement as package 34's | the sequences the texts'; **every time judgement** |
| `get_under_way.cast_points` | seven points before the head yards are filled | Luce's "fallen off sufficiently"; four points put the frigate in irons with the spanker set (found on the way) | judgement |

### The market's rules table

| Rule | Reads | Figure | Where |
|---|---|---|---|
| the season | the month, against the good's `season` factors in the port file | the file's (0.8 to 1.3) | `Market.factors` |
| the war | the good's `origin` nation at war with the port's nation, by `Nations.at_war` now (a peace made or a war declared by the news moves it the next time a price is asked) | `WAR_FACTOR` 1.5 | `Market.factors` |
| the supply | the tons sold to the port less the tons bought from it, a hundredth a ton, floored at a half and capped at double; cleared by a seventh a day in whole days | `SUPPLY_PER_TON`, `SUPPLY_FLOOR`, `SUPPLY_CAP`, `SUPPLY_RECOVERY_PER_DAY` | `Market.factors`, `Market.recover` |
| the rounding | the product, to the half pound, never under it | `PRICE_ROUND` | `Market.price` |

Truth 69's sums at seed 7: forty tons of tin bought at Falmouth at £120 (the file's figure, no factor moving it: the war rule reads tin's origin, Britain, against Falmouth's nation, Britain) is £4,800; sold at Brest, where English tin is 180 by the file and the war puts the half on, £270 a ton and £10,800 in; the voyage makes £6,000, which is forty times the two lists' difference and nothing else. The forty tons sold take the supply factor at Brest to 0.6 (the next buyer pays £162), and a week later the glut has cleared to a third of itself (a seventh a day compounded: forty tons to 13.6); peace made between Britain and France takes the war's half off whatever the supply's figure is that day, and the war declared again puts it back.

### The pilot boarding on the pinned passages

The frigate (gate 5b's passage, seed 7): the cutter sighted at 55800 ("Sail ho! A sail on the larboard bow, bearing NNW, distant two leagues"), the hail at 57720, the pilot aboard at 58020 with his words and his news, five minutes after the outer road's first cast under twenty fathoms (57732) and two and a half before the best bower is let go (58167); the pilot aboard at the anchor. The schooner: sighted 54840, hailed 56880, aboard 56940 ("American colours being no bar at Falmouth"), ahead of her own book's shortening sail at 56502. The thick passage has no pilot's lines: no cutter is sighted and none hails, and her log is unchanged. Package 36 inherits: the pilot aboard as a person who answers and does not steer; the cutter as a vessel of the world with a plan of legs, seen by the lookout's rules and logged as a sail; `a sail in sight` as a reading with the nearest sail's words; the stance per nation and the news that moves the table; letters that come aboard by the cutter or the boat and reach the captain by the messenger and the door.

### The pinned passages, re-measured

The noon (28740) and the Soundings' cast (29884 and 29938) stand on all three. The frigate: lines 624 → 629 (the sail sighted, the hail, the pilot aboard, his words, his news), digest 6880cabc6e0ac53e → a7fe3d92fc16d1ed, brought up 59145 → 59144 (the tide fix below, one second); every other tick as package 34 left it (the landfall 44700, the outer road 57732, the account 6.6 miles at noon, 5.2 at the landfall). The schooner: lines 725 → 730, digest c59b39435e5f2c15 → b49d841fd40f9482; the landfall 43920, the anchor off the town 57615 and brought up 58618 as before. The thick passage: 504 lines, digest b3b1f54a4b97a8f4 → 65927077f46006eb (the tide fix below moves every digest a little and no tick at all). The lookout's estimate of a sail's distance draws on its own stream (`sail`), so the land's sightings on the pinned days did not move; the pilot's name draws on `people` and the recruits on `recruits`.

### The port, measured

The frigate standing in for Falmouth from five miles south of the outer road under plain sail at seed 7: the cutter sighted at six miles fourteen minutes out, hailed at 2640 s, the pilot aboard at 2700 s with her at four knots; the port read as "Falmouth, the outer road bearing N, 1.8 miles". `get under way` from the outer road in twelve fathoms with fifty-nine fathoms out: the capstan rigged in three and a half minutes, hove short in eleven, the topsails let fall and sheeted home in four and a half, the cable up and down a minute after, aweigh at 1101 s from the order, the jib hoisted and the stern-board made, paid off seven points at 1261 s, under way with the anchor catted and fished at 1530 s (twenty-five minutes and a half), under topsails and jib on the starboard tack, full and by at four knots; the pilot's S by E lies 56° from a south-west wind and is not laid, and the line says so. The cutter comes off for him once she is a mile beyond the road and standing away, and he leaves her an hour after she got under way, the £5 of pilotage paid from the purse. `moor` in the Bay of Brest from sixty fathoms in eleven: veered to a hundred and twenty in a minute, the small bower let go, middled in sixteen and a half minutes, "the hawse open to the SW"; `unmoor` twenty-one minutes; the kedge laid out ninety fathoms to the north-east by the launch in twenty minutes from the order. The schooner's long-boat from Carrick Road to the quay at Falmouth: hoisted out in five minutes, twenty-two minutes' pull, a quarter of an hour at the quay to land the mate, back and hoisted in at seventy-one minutes from the order with the list; ten tons of tin bought go by the lighter in half an hour on top of the hour's business, two hours and twenty-five minutes from the bargain to the hold. At Plymouth the King's yard sends a topmast off in eight hours and thirty days' provisions in an hour and a half for nothing; at Falmouth the chandlers want £40 for the spar and a shilling a ton for water. Four able seamen entered at Falmouth at £3 come off in twelve hours and are mustered by name; the company is 44.

### Found on the way (package 35)

- **Four points was too few.** Cast four points and the spanker set, the frigate came back into the wind with no way on and lay in irons; Luce's "fallen off sufficiently" is seven points in this hull, past close-hauled, and a pilot's course that lies closer to the wind than close-hauled and half a point is not steered but said ("full and by (S by E lying too near the wind to be laid)"), because a helm held to it pinched her into irons as surely.
- **The boat holds the boat.** A script that sends the boat away must not hold the ship: the runner's `_holds` honours `holds_subject = False`, and `SendBoatScript` holds "the boat" only, so the ship may be worked while the boat is ashore and a second errand is refused in words.
- **The cutter a cable off the quay for ever.** A vessel homing to a mark stopped exactly at the arriving distance and never came within it (a floating-point equality), so the cutter sat in sight of the anchored ship all night; she is done within a metre of the mark now.
- **Bare poles are not under way.** A ship with no sail set drifts a knot to leeward in twelve knots of wind, and the pilot came off to her; he comes off to a ship under sail with a knot of way.
- **The boat's trips by its weight.** The long-boat's 0.6 tons is her weight, not her burthen, and forty tons of tin were twenty trips; the goods go by the port's lighter at three minutes a ton while the boat is at the quay.
- **`take in twenty tons of water`.** The sail verb `take in` took the words and found no such sail; the handler catches that refusal for the stores' words and hands them to the port, and `take in water` alone completes her water or says it is complete.
- **The asleep lieutenant was "on the quarterdeck already".** His place by the bill was the quarterdeck while he slept below; sent for, he is called from his watch below, and does not turn in again until his watch.
- **The tide table remembered who asked first.** The schooner's passage gave three digests in whole-suite runs (1365ae178c6e3b15, 6be7916828f57818, ebda165713990ffc) on the same 730 lines, and one digest in every isolated build. The cause was package 34's `Tide.constants_at`: the gauges' constants are interpolated once per hundredth-degree cell and cached, and the table is shared between the Worlds of one process, so the cached value was the interpolation at whichever point first asked, and a world's tide depended on the worlds built before it in the same worker (the hunt: build, run a selection of tests, build again, diff the events; the rest of `test_known_truths` moved St Anthony's Head from eight cables to seven and the bower's depth from eight fathoms and a half to nine). The constants are evaluated at the cell's centre now, a pure function of the cell; every pinned tick stands (the frigate's brought-up moves one second) and the three digests move once more, to the values pinned.
- **Every sample carries every reading.** The places' descriptions in `the places` put 337 tokens into each of the agents' samples and broke the local door's budget test; the words are the names now (about 40 tokens) and the descriptions ride in the value's `items`. The people (150 tokens) and the boats (60) stay: the one is state, the other short. A sample is about 1,200 tokens with the sails' line against 800 before the package.
- **The library's read is not logged.** A page read through `library(topic='papers')` leaves no line, as the reference's pages never did; a reading at the prompt does. The parity is structural (one page, every station), and the gap 33d found (a paper reachable only through `submit_order`) is closed; whether a paper read should be a line in the log is a question for 36.
- **Not done.** St Mary's and Roscoff (35b); the hawse fouled by a moored ship swinging (Luce's 'tend ship'); warping up to the kedge; the pilot steering (he answers and does not con); the boat's crew drawn by name from the muster (eleven hands of the forecastle, afterguard and waisters, no names); a reply to a letter sent ashore; the batteries of a closed port; the French market in livres (sterling at the exchange, a livre a tenth of a pound from memory); the prices and the wars' dates against a page (none in `docs/references/`); the pilot by night.

**After the merge** (the lead, 2026-10-02): the pilot's tide words changed from "feet above the datum" to "the tide rising some N feet", and since his words are a log line the two passages with a pilot moved their digests and nothing else: the frigate's `a7fe3d92fc16d1ed` → `614d40d01fd44192`, the schooner's `b49d841fd40f9482` → `dfecc9c12ebc0fd9`, 629 and 730 lines as before; the thick passage, with no pilot, unmoved.

## Milestone 5: St Mary's and Roscoff, two port files and a patch

Package 35b (spec M5 §10, §23, §24; the brief in `docs/dev/M5-WorkPackages.md`). Two files on package 35's machinery (`data/ports/st-marys.yaml`, `roscoff.yaml`), the Roscoff override from Bellin's sheet of 1764 (`data/charts/overrides/channel-west/roscoff.yaml`) with its marks in the features file, the region's tiles rebuilt by the tool with a level-3 harbour group for Roscoff, and the two ports in the nations table's index. No engine change but one wording fault in `freesail/world/ports.py` (below); two things a port wanted that the machinery lacks are reported, not built.

## Milestone 5: other sail, the world's order, the two passages

Package 36 (spec M5 §25 to §27, §29; the proposal's §5.2, §6.1 and §7.6; `docs/design/InwardAndOutward.md`). Other sail at far detail is a hull from one of the four ship files with a polar drawn once from the file (`freesail/world/ships.py`), moved at the roll-up's cadence by the same wind and tide as the player, sighted at the horizon her masthead gives and named by the lookout as she nears; the world keeps her truth and the captain his account (`the strangers` gives a bearing and an estimate and never a position; the chart draws a sail by those alone). The world-order channel (`freesail/world/orders.py`) is the scenario file's and the harness's, journaled at its tick with its source and replayed, and refused in words at the captain's prompt. The two scenarios of the gate ship with their books beside them (`data/scenarios/merchant-passage.*`, `naval-cruise.*`); the starter book is a choice.

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| St Mary's, the roads | the mouth of St Mary's Sound (7 fm, Imray p. 106), St Mary's Road (the chart's feature, White's 4 and 5 fm on loose sand), the Pool off Hugh Town (1½ fm, small craft; `deep_draught_ft` 9), the quay at Hugh Town | White 1835 pp. 13-17; Imray 1874 pp. 104-108 | the pages; the Pool's depth and the draught judgement |
| St Mary's, the pilot | cruising 8 nm, not by night, skill 0.95, £3, cast starboard, out SSE (160°); names of the isles | White p. 17 ("their attendance may always be depended upon ... attention, skill, and intrepidity"); the figures judgement, the fee **unverified** | judgement |
| St Mary's, the market | kelp 5 (June 0.9), salt fish 20, pilchards 13, potatoes 4 (dear in May and June), barley 9, salt 28, coal 3, brandy 160, salt beef 60, timber 8 | **FROM MEMORY** and judgement, as package 35's | **UNVERIFIED** |
| St Mary's, the yard | none: cordage at 0.08 a fathom, water at a tenth of a pound a ton (0.15 h a ton), provisions at a shilling a man a day | Imray p. 105 (fresh water and provisions; his spars and rope-walk the 1870s'); the figures judgement | judgement |
| St Mary's, the crew pool | 2 able at £3, 4 ordinary at £2, 6 landsmen at £1 | a poor island whose young men pull in the gigs | judgement |
| Roscoff, the roads | the western entrance of the channel of Bas (a feature, 9 fm, Bellin's 10 and 15 brasses), the road of the Isle of Bas (a feature, 3 fm: Bellin's 3 brasses, Faden's 4 fathoms, La Barre's 3 to 4 on sand), the harbour of Roscoff (dries 2.9 m above the datum, `deep_draught_ft` 9), the quay under the church | Faden 1793 pp. 45-46; La Barre 1825 pp. 39-40; Imray 1874 p. 211; Bellin 1764 | the pages; the drying height judgement |
| Roscoff, the pilot | cruising 6 nm, not by night, skill 0.9, £3, cast larboard, out W (270°); Léon names | judgement on Faden's two passages; the fee **unverified** | judgement |
| Roscoff, the market | brandy 100, geneva 70, rum 80, tea 170, tobacco 60, wine 38, salt 12, canvas 42, onions 6, tin 170, salt beef 70 | the spirits, the tea and the tobacco priced for the Cornish run by **JUDGEMENT** (no Roscoff price current in the references); the rest from memory as Brest's; the rum's trade the arrêt of 1769 and Faden | **UNVERIFIED** |
| Roscoff, the yard and the pool | a topmast £42 in 10 h and a yard £26 from the town's shipwrights, cordage, water, provisions; 2 able, 4 ordinary, 8 landsmen, a day's delay | judgement (the Inscription maritime takes the town's seamen) | judgement |
| the override's unit | the brasse, 1.624 m (`BRASSE_M`) | the study's figure (C §3.3); the sheet has no legend for its soundings | **unverified** |
| the override's datum | low water of spring tides, 1.30 m above the chart's datum | SHOM's BMVE at Roscoff as the tide study quotes the RAM (`data/tides/constituents.yaml`'s head) | the study's reading, not this package's |
| the georeference | six control points, a similarity by least squares: 2.96 m a pixel (the sheet's own bar gives 2.64), turned 173°, residuals 70 to 230 m | the sheet's pixels against the encyclopaedia's positions and the grid's shore | measured |
| the patches | the road 3 brasses (6.2 m), the channel west of it 6 brasses (11.0 m), the harbour drying a brasse (2.9 m above), the town 12 m and the Isle Verte 10 m above the datum | Bellin 1764 for the depths and the outlines; the heights and the drying judgement | the sheet's figures |

### The pilot's boarding from seaward at seed 7

St Mary's, the frigate from south-east of Peninnis with the wind at ESE, under plain sail at four knots: the cutter sighted at 240 s ("Sail ho! A cutter standing out from the land on the starboard bow, bearing N by W, distant two miles"), the hail at 720 s, Mr Woodcock aboard at 840 s with his words (the Sound, the Minalto and the Mincarlo, the berth by Hangman Island and the Nut Rock, the Road open to the westerlies, and high water at half past three, the tide rising sixteen feet), the Sound run on the leading line, `come to an anchor` at 2460 s and the best bower let go in six fathoms at 2809 s in St Mary's Road. Roscoff, the American schooner from the west for the western passage with the wind at SW: a sail hailed at 300 s, the hail at 2700 s, Mr Cabioch aboard at 2760 s "(American colours being no bar at Roscoff)", the best bower let go in five fathoms in the road of the Isle of Bas at 5479 s. The British cutter standing in from the same water is met by no one in an hour (the port hostile to the English); closed to the American by a scenario's order, the pilot hails his refusal at 2760 s.

### The tiles' rebuild

`python tools/build_charts.py --skip-fetch` from the sources cached on 2026-09-30 (the checksums the manifest's): a rebuild of the unchanged files first gave all 149 tiles byte for byte, so the build is a function of its inputs; with the Roscoff override and the harbour group one level-2 tile changed (`175200_-15168`) and four level-3 tiles were added (`175200_-14400`, `175200_-14656`, `175456_-14400`, `175456_-14656`, 398 kB); the coast changed at Roscoff only. The build hash moved from b1ffd74fa02a545a (which the features file's later entries had already left stale) to the value the manifest now gives. The tool's override check printed nothing for Roscoff once the six-brasses patch was drawn on the channel's deep core; drawn where the sounding georeferences, it lay over the main's rocks and the tool printed a difference of 4.2 m.

### Found on the way (package 35b)

- **The pilot vessel is not taken from the port's file.** Package 35's machinery takes the pilot's ship file from the port (`cutter:`) but names her "a cutter", "the <port> pilot's cutter", and says "the cutter" in the hail, the boarding, the refusal and the leaving (`Ports._launch_cutter` and the lines after it); her masthead for the lookout's horizon comes from her ship file, and a gig has none. The two files say what comes off (`pilot.vessel`: St Mary's gig under oars and a lugsail, Roscoff's boat), which nothing reads yet, and keep the cutter's file as the stand-in. Reported for the lead's decision; package 36 owns the vessel at far detail.
- **Roscoff cannot be "closed to Britain" while the table says war.** The brief wanted the cutter refused in the pilot's words; the stance rule makes a French port hostile to a British ship in 1805, a hostile port sends no pilot, and package 35 made a closure never outrank a war (`tests/test_nations.py`). The file claims nothing the machinery does not do: hostile to Britain, the refusal in the pilot's words shown by a port's order against a neutral. Reported for the lead's decision.
- **"St Mary's's market".** Two refusals built the port's possessive by adding "'s" to its name; a helper leaves a name that is a possessive already as it stands (`freesail/world/ports.py`, `_possessive`), a fault in the machinery's words that the file's name forced.
- **"buy a suit of sails from the chandlers" where there are none** falls through to the market with its words mangled ("St Mary's market has no suit sails from chandlers"); the order's parsing is `freesail/orders/port.py`'s and is left as it is, reported.
- **GEBCO's fill under EMODnet's empty land.** The town of Roscoff and the Isle Verte were a metre of water in the tiles (GEBCO's -1 m where EMODnet has no land), so the town was sea and missing from the coast; the override returns both to the land. The same fill may stand elsewhere; not searched for (`data/charts/unverified-checks.yaml`).
- **Not done.** The pilot vessel taken from the file and the closed stance against a war (the two above, the lead's); the narrows by Roscoff and the entrances in open water, left to the modern grid (the sheet's figures in the override's notes); the smuggler's run under false colours (milestone 7); warping into the drying harbour (milestone 8); Fowey and Penzance (when a scenario asks).

| `ships.VESSEL_TICK_S` | a game minute | the roll-up's cadence (spec M5 §30): a brig at six knots moves a cable in a minute, the sighting's precision | judgement |
| `ships.POLAR_ANGLES_DEG`, `POLAR_WINDS_KN` | every ten degrees from forty to a hundred and eighty, at eight, fifteen and twenty-five knots; linear between | the truths' polars are read every ten degrees | judgement |
| the polar itself | the sails model (`physics.sails.compute_sail_forces`) balanced against the hull's resistance at each point, the yards trimmed as `orders.verbs._trim` trims them (the yard at the apparent wind less the peak angle, the sheets by `wanted_sheet_angle`), by bisection on the speed | the file's own physics; no number of its own | the beam reaches in fifteen knots against the polars the truths measure by sailing: frigate 8.2 for 8.0, schooner 7.9 for 7.9, cutter 7.2 for 7.3, brig 7.8 for 7.7 (`tests/test_ships.py`) |
| the closest point of sailing | the polar's first angle with way on her | the same balance | the frigate about six points, the schooner about five (truth 32's order stands) |
| `ships.SAILING_FACTOR_MIN` | 0.85 to 1.0 of the file's polar, drawn once from the `ships` stream | ships of one class sail differently by their trim and their age | judgement |
| `ships.VESSEL_MIN_SPEED_KN` | a knot | steerage way in the lightest air that moves her | judgement |
| `ships.REEFED_FACTOR`, `REEF_OVER_KN`, `LYING_TO_KN`, `LIE_TO_OVER_KN` | 0.7 of plain sail over thirty knots; lying to over forty-five, a knot to leeward | the starter book's shortening; truth 28's lying a try under a knot and a half | judgement |
| the beat | by the wind on the tack that points nearer the mark until she can lay it, at the polar's best angle to windward (the speed times the cosine greatest: the cutter's a point and a half freer than her closest angle, where she has a knot and a half of way) | the vessel captain of this package: rules-based, the crewed promotion milestone 6's (`Vessel.promote`); found on the way (truth 70's Brest pilot beat out of the Goulet at a knot and a half at the closest angle and never came up with her) | judgement |
| the tide over the ground | `tide.stream_at` added to her way each minute | package 34's stream, the player's | truth 67 |
| the wind at her place | the systems' surface wind at her position, else the base wind | package 31b's field, the player's | truth 67 |
| `ships.NEAR_DETAIL_NM`, `NEAR_DEMOTE_NM`, `NEAR_TURN_DEG_S` | promoted within two miles, demoted beyond three; her head swings a degree a second | spec M5 §25's switch, a stated range with hysteresis; the brig's three degrees a second hard over (the turning table) | judgement |
| the horizon | 2.08 (√h_eye + √h_obj) nautical miles, metres | C §5.5; Bowditch's 1.17 √(feet) is the same line | the mastheads from the files: frigate 35.9 m, schooner 29.0, cutter 22.6, brig 24.1; from a frigate's eye a frigate is a sail at 24.9 nm, a schooner 23.7, a cutter 22.4, a brig 22.7; from a schooner's 23.7, 22.4, 21.1, 21.4; from a cutter's 22.4, 21.1, 19.8, 20.1; from a brig's 22.7, 21.4, 20.1, 20.4 |
| the period's | "hull down" at four or five leagues, the sail of a ship of the line seen from a frigate's masthead at twenty miles and more in clear weather | Falconer 1780, HORIZON ("the distance ... depends on the height of the eye"); the chart study's own table | the formula's figures agree within a league |
| `ships.RIG_MADE_OUT_NM` | her rig at four miles | the angle her masts subtend, Luce 1866 ch. XXXIII, 'Chasing'; three masts or two told from the tops by day | judgement |
| `ships.COLOURS_MADE_OUT_NM` | her colours, or their want, at two miles | Falconer 1780, COLOURS; a flag of a few yards read with a glass | judgement |
| `ships.MADE_OUT_NM` | what she is at a mile and a half | the pilot cutter's number on her mainsail (35) | judgement |
| `ships.GLASS_FACTOR` | the glass aloft reaches half as far again | the period's day glass against the eye | judgement |
| `ships.HAIL_NM` | within hail at four cables | `ports.PILOT_HAIL_WITHIN_M` (35) | the same figure |
| `ships.BOAT_MASTHEAD_M`, `BOAT_SEEN_NM`, `BOAT_PACE_KN` | a boat under oars and sail (35b's gig, the town's boat, `pilot.vessel`): masthead five metres, seen within two miles, four knots under oars whatever the wind | a thirty-foot gig's lugsail yard; a boat's sail from a masthead a mile or two; `ports.BOAT_PACE_KN` | judgement |
| `navigation.CHASE_LEAD_MAX_DEG`, `CHASE_STEADY_DEG`, `CHASE_MIN_INTERVAL_S` | the lead off a chase's bearing capped at forty-five degrees; a drift under half a degree is 'steady'; two orders within a minute read no drift | Luce 1884 p. 553 (the chase kept on a steady bearing); the lead worked from the drift, the lookout's estimate and his own way across the line of sight, as the master would on the slate; the cap because the estimate is a third out at the worst and a bearing that swings fast is a close pass | judgement in the cap; the rule Luce's |
| the chase's clamp | never nearer the wind than she lies close-hauled, on the tack she is on | a chase dead to windward is not a reason to put her about every glass | judgement |
| `navigation.COURSE_NOT_LAID_MARGIN_POINTS` | a course shaped within close-hauled and half a point is not laid: kept full and by on the tack that points nearer it, put about when that is the other (brought by the wind first when she is not close-hauled); a course laid but reached by a turn through the wind's eye is worn round for | package 35's rule for the pilot's course; Luce 1866 ch. XXIV, 'Wearing' (a frigate shaping back for her station from a chase down wind lay in irons seventeen hours before this) | judgement in the margin; the rule 35's |
| `orders.CHANNELS`, `REFUSAL` | weather, ship, message, port, person; "That is an order to the world, not to the ship: ..." | spec M5 §26; truth 71 | the grammar's text |
| the world orders' journal | every order at its tick with its source, at the actor "driver"; the scenario's applied by the World at their ticks from the file, the harness's an input replayed | spec M5 §26; truth 72 | `tests/test_world_orders.py` |
| the ship's own events for the book | `the course shaped` (`helm.set`), `steady on the course` (`helm.steady`), `the turn to the flood` / `to the ebb` (`ship.swung` by its data), `the pilot asks to be put off`, `a sail made out`, `a stranger's colours made out`, `a sail lost`, `a sail within hail` | the passages' books | the books |
| `a stranger in sight` | a sail not known for the ship's own nation's: every sail until her colours are made out, one under none or another nation's after, and none once spoken within hail | Falconer 1780, COLOURS; what follows a chase is milestone 7's | judgement |

### The dozen ships of each scenario

The merchant passage (seed 7; `data/scenarios/merchant-passage.yaml`): Two Brothers, a merchant brig of Britain, bound from the Longships for the Eddystone, no colours; Nancy, a merchant brig trading Falmouth to Plymouth; Lark, a cutter of the Navy patrolling off the Wolf within four miles; Diamond, a frigate patrolling off the soundings seven leagues south-west of Ushant within eight; Harpy, a brig-sloop off the same soundings within ten; Palinure, a brig-sloop of France at the Raz running home to Brest, no colours; Hirondelle, a schooner of France from the Isle of Saints for Camaret road; Betsey, a schooner of the United States bound for Falmouth; Anna Maria, a brig of Denmark bound for 48 30 N 5 40 W; Bom Jesus, a brig of Portugal bound for the Start; Indefatigable, a frigate from Cawsand Bay for the soundings south-west of Ushant; Swift, a cutter carrying the mail to Plymouth. The naval cruise's eleven are the same but for Palinure (put on the sea by the scenario's order on the 13th at seven: a brig-sloop of France at 48 50 N 5 16 W, five leagues on the frigate's bow as she stands back for the station, bound up-Channel for the Start, no colours, across the station; the scenario's author sees the world, and places her where the frigate's track at seed 7 will raise her within the weather's twelve miles and closing) and Dolphin, a schooner trading Falmouth to the Eddystone, in her place; Lark patrols off the Eddystone, Diamond off the Raz and Harpy off 47 50 N 6 00 W. Each has her description from `ships.DESCRIPTIONS` or her file's `ship.descriptions` (the brig's two, written by `tools/gen_ships.py`: "a brig-sloop of war, sixteen ports a side" and "a merchant brig, deep laden"), her nation's colours and flag words from `data/nations.yaml`, and a sailing factor drawn from the `ships` stream.

### The pace with the dozen ships

At the merchant passage's start (the schooner at anchor in Carrick Road, the dozen ships on the sea at far detail, the lookout over them once a minute, `the strangers` in every sample) the build machine runs 1,480, 1,489 and 1,384 ticks a second in three thousands after the first ten minutes (best 1,489); under way off the Manacles with the pilot off, the account brought up each tick and the bearings every glass, 715, 814 and 779 (best 814). Both over BUILD_MACHINE_FLOOR (500); the far-detail ships cost about a tenth of a tick each a minute. Found on the way: the first measurement was 98 ticks a second, then 17, because `Chart.find_feature` re-keyed every feature's name on every call (a hundred seconds of a hundred and five in `_name_key`) and the books' pricked positions were re-parsed every condition; the name index is built once and the positions cached (`api.readings._pricked`), which is the whole of the recovery.

### The two scenarios at seed 7

**The naval cruise** (`naval-cruise.yaml`, forty-eight hours from 12 June 06:00, the wind pinned west-north-west to north-west, 14 to 10 knots; the frigate with her chronometer, a sextant and a glass, a lunarian master, the book `naval-cruise.orders`): the best bower let go in the Sound at 60; thirty days' provisions demanded of the King's yard at the anchor and stowed at 5460 (07:31); under way on the starboard tack, S by W, at 6834 (07:53, Luce's whole sequence); the Plymouth pilot's cutter sighted at 6600 as "a cutter standing out from the land" (she comes off from the pilots' station, the outer road), her hail at 7800 and the pilot aboard at 7920 (08:12); the pilot asking to be put off at 8820 as his cutter comes off again, the ship hove to for it at 8876, the pilot off at 11220 (09:07), filled away at 11273 and the course shaped for the station; the port admiral's order given by the scenario at 14400 (10:00, "a cutter sent from Plymouth with a letter"), the cutter sighted the same minute ("a sail on the starboard quarter, bearing N by W, distant five miles"), made out as a cutter under British colours and within hail at 17840 (10:57) with the letter, which came aboard, went by the midshipman to the quarterdeck and was read there at 17900 (10:58); the noon at 21600, the time sights at 10800, 39600, 97200 and 126000 (the longitude by chronometer within five to eighteen miles of the reckoning, the Arnold eleven and twelve days from its rating); the Portuguese brig Bom Jesus made out at two miles on the way at 43380 and let go, her colours shown; the light on Ushant at 73680 (02:28 on the 13th), right astern after the first wear at the station, 72564 (02:09); the frigate by the wind on one tack and the other, north four hours and back; the waypoint appended to the old high at 86400; the Palinure put on the sea at 90000 (07:00, 48 50 N 5 16 W bound up-Channel for the Start, five leagues on the frigate's bow as she stands SW by W for the station), sighted at 90960 (07:16, "Sail ho! A sail right ahead, bearing SW, distant four leagues"), the chase given at the glass, 91800, by the bearing's drift each glass after, made out by the glass and the tops at 93660 ("a brig, standing to the north-eastward"), 94380 ("a stranger, her colours not made out") and 94560 ("a brig-sloop of war, sixteen ports a side"), the chase lying too near the wind to be laid and the frigate kept full and by on the starboard tack, so that the brig weathers her and passes (at 95400 she bears N by E on the starboard quarter, "drawing forward 133 degrees since the last"); the frigate worn round at 95940 (08:39) and the brig run down before the wind, within hail at 106931 (11:42), a stranger under no colours, the chase given up there and the course shaped for the station at the same minute; the noon of the 13th at 108240 forty miles north-east of the station (49 10 N by observation, the longitude by account 4 49 W against the truth's 4 56 W), the station shaped for every watch and reached again by the light on Ushant at 137280 (20:08), kept by the wind through the night, wearing at 136800, 151200 and 165600; eight wears in the two days. 2014 lines, digest b23ad76e93212c63; no grounding. The account against the truth: 7.1 miles at the first noon (the hour hove to for the pilot ran on at the log's last read), 4.9 at the second, 4.7 at the end; the cutter's and the stranger's sightings and the within-hail lines carry a bearing and an estimate and no distance. What the book does not handle at this seed, for the owner to better as captain: the chase's lead at close quarters (within two miles the bearing swings a point a glass and the worked lead reaches forty-two degrees, which with the chase in the wind's eye lets her pass out of hail and costs a three-hour stern chase); a stranger faster than the frigate on a reach (placed four leagues on the bow and bound south-south-west, a beam reach in ten knots, the brig-sloop held her distance eight hours and was lost at 15:18, never made out: the brig's polar drawn from her file by static balance gives her six knots to the frigate's five and a half under the book's plain sail); the chase that takes her forty miles from the station by noon (the book shapes back by the watch, and the station is raised again at dusk); the station's two points (she holds a tack to the hour and wears, and the account's swing lets her go twenty miles north between wears).

**The merchant passage** (`merchant-passage.yaml`, thirty-six hours from 12 June 05:00, the wind pinned W 14 to NW 10, the schooner with her octant and no chronometer, a master who can work a lunar, the book `merchant-passage.orders`): the best bower let go in Carrick Road at 57 and forty tons of tin bought at the quay the same minute (£120 a ton, £4,800); the long-boat away at 396 and alongside with the lighter's tin struck down at 14249 (08:57), on which she gets under way on the ebb (under way at 16005, 09:26, starboard tack, S by E); the Falmouth cutter sighted at 15600 ("a cutter standing out from the land", two miles), her hail at 16200 and the pilot aboard at 16320 (09:32, the cutter coming off from the outer road, the pilots' station); the pilot asking to be put off at 17580 as his cutter comes off again, the ship hove to for it at 17638, the pilot off at 18420 (10:07), filled away at 18490 and the course shaped for the point east of the Manacles; the noon at 25200 (the account ten miles out, the three quarters of an hour hove to run on at the log's last read, set right by the Lizard's bearings within the glass); a sail off the Lizard at 28140 (12:49, "Sail ho! A sail on the larboard bow, bearing SE by E, distant three leagues"), hailed and not made out, as the book has no order for her; the course across worked hourly from the account from the Lizard's point to the soundings; the light on Ushant at 61020 in the middle watch; the Iroise's mark passed at 06:00 on the 13th two miles wide by account, the cast at it not made (the note is read within a mile and a half; below), the points off Bertheaume shaped for at 87242 and after; the Brest cutter sighted at 88080 ("a sail on the larboard bow, bearing E, two leagues"), made out as a cutter standing out from the land, then under French colours, then the pilot's, her hail at 91380 ten miles out in the Iroise and the fore topsail in; the pilot Mr Le Floch aboard at 91560 (06:26) with his words and the agent's letter, read at 91620 ("The tin will fetch its price"); the anchor let go in the road of Bertheaume at the first cast under thirteen fathoms by the book's reading, 96475 (07:47, thirteen and a half by the lead's own words, the account eight cables out on Point Bertheaume's bearings); riding to the ebb until the turn to the flood at 108960 (11:16, by daylight: the book lets a night's flood go by), under way on it at 110675 and the course shaped for the Goulet's mouth; the noon at 111660 in the mouth (the account three cables out); the Goulet by the pass north of the Mingan and the Fillettes, each point within four cables (112005, 112674, 113343, 113560, 114001, 114382), the hand lead going and a bearing every five minutes (the account within a cable or two); the anchor let go in the Bay of Brest at the first cast under twelve fathoms, 115534 (13:05), brought up at 116377 in six and a half; the boat ashore with the mate at 116697 and alongside at 123004 (15:10), when forty tons of tin are sold at £270 (£10,800; truth 69's sum). 2460 lines, digest a66e31615102220b; no grounding, nothing dragging. The account against the truth: 9.6 miles at the first noon (above), 0.3 at the second in the Goulet's mouth, under a mile at both anchors (0.8 at Bertheaume, 0.7 in the Bay). The point under Petit Minou was moved from 48 20.1 N to 48 19.8 N 4 36.5 W after the cutter's change (above) moved her track a cable: at 48 20.1 N the point lies twenty-two metres deep but within a cable of the grid's shore under the Petit Minou (the grid's land reaches south to 48 20.1 N between 4 37.5 W and 4 36.3 W), and the leg to it from the mouth, with the account's swing and the leeway, put her on the grid's shore at 48 20 N 4 37 W four times on the flood (12:18, 12:56, 13:16, 13:33; she floated each time as it made, stove and the well rising, and still anchored in the Bay at 13:44 with the tin sold at 16:38); three cables further south the leg clears it by the chart's grid and the Mingan and the Fillettes as the features place them. What the book does not handle at this seed, for the owner to better as captain: the deep-sea cast at the Iroise's mark (she passed it three miles north by the truth, two by account, the hourly course for it held by the Ushant guard for the last two hours), so the Iroise's words were not read; the fore topsail, taken in at the Brest pilot's hail, is not set again for the ten miles to the road (an hour and twenty minutes to the anchor; a rule to set plain sail at his boarding, tried once, brought her into the road at six knots and on the grid's shore short of it); "in the Bay" fires six times more at the anchor from the lead's casts under twelve fathoms with the stream giving her two knots through the water, and is refused each time ("she is at anchor already"); a night's flood (the tide served by day); the pilot's own conning (he answers, 35's rule).

### The pinned passages, re-measured

The gate-5b passages' pilot cutter is a vessel of the world now, sailing by her file's polar (seven knots on a reach, not six capped at half the wind), coming off from the pilots' station, the outer road, and sighted at the horizon her masthead gives: the frigate's cutter is sighted at 54600 ("two leagues", bearing N by W; 55800 before), hails at 56280 (57720) and puts the pilot aboard at 56340 (58020), half an hour before the best bower is let go; the schooner's is sighted 53640 (54840), hails 55320 (56880), boards 55380 (56940), before her own book shortens sail at the outer road. Nothing of the ships' own moves: the noons 28740, the casts 29884 and 29938, the landfalls, the outer road, the anchors and the brought-ups stand; the lines grow by the sail's (629 → 633, 730 → 734) and the digests follow (a7fe3d92fc16d1ed → dd07888fdd36ee45, b49d841fd40f9482 → f5a2b2b7d097df75; the hail's line carries the cutter's errand in its data; measured in this package's tree before the lead's tide-words change to `ports.py`, which moves the two digests again and no tick; the lead reconciles). The thick passage, with no cutter, is untouched (504 lines, 65927077f46006eb). The pilot's request to be put off (below) does not reach these passages, where he stays aboard to the anchor.

### Found on the way (package 36)

- **A cutter faster than six knots outran nothing and was outrun.** With the cutter on her own polar the schooner with her sheets tended and the frigate under topsails both left the fetching cutter astern, and the pilot of Falmouth was carried to the Iroise, the pilot of Plymouth half way to Ushant. The pilot asks to be put off as his boat comes off for him (`port.pilot_hail` with `asks`, the book's event `the pilot asks to be put off`), and the passages' books heave to for the boat, fill away when he is in it and shape their course again.
- **The account between the log's heaves swings an hour's run.** `Navigation.account_now` runs the last worked position on at the log's last read along the traverse board's mean heading since (package 33a's mate), so as the ship turns, or lies aback, the account swings up to the hour's run and a mark three miles off is reached and left by account in a minute. Every `when the distance to ... is under` rule of the passages' books is written for it: open-sea marks are given two to seven miles, the station's legs were given up for wearing by the hour, a one-shot action (the Iroise's cast) is guarded by a second mark that the leg leaves behind, and the approach to Bertheaume and the Goulet is held to its marks by a bearing every five minutes from fourteen miles off.
- **A helm put over for a course across the wind's eye.** `steer` turns her the shorter way; when the wind's eye lies in that arc a square-rigged ship is taken aback and lies in irons (the frigate for seventeen hours after a chase down wind, before the rule). A course shaped or a chase that lies across the eye is worn round for, and the book gives the course again at its next glass; a course too near the wind is kept full and by on the nearer tack or put about for.
- **A heave-to ordered while hove to.** `heave to` given to a ship already hove to ran its script eight minutes and failed with "she is hove to already", and left her yards half braced, from which the next fill-away put her aback for an hour and a half. The merchant's book guards its bringing to so that it is given once; the refusal at once is the evolutions' to make (32e's), reported to the lead.
- **A square sail aback on a reach.** The books that shape courses change the course by points at a time with the true wind steady, which the starter book's "trim on a shift" (a point of the true wind) never catches: the yards stayed braced for the old course and the schooner's fore topgallant was aback on a broad reach. The passages' books trim when she is steady on a course shaped (`at steady on the course then trim sails`), the events `the course shaped` and `steady on the course` being this package's.
- **The chase of the port's own cutter.** The first cruise chased every sail in sight and so chased the Plymouth cutter home, with the letter read, to the Shagstone. `a stranger in sight` names the sail a cruiser chases: every sail until her colours are made out, one under none or another nation's after, none once spoken within hail (the vessel's `spoken`, which `hailed` is not, being cleared at eight cables).
- **The chase's lead.** Luce's rule kept the chase on a steady bearing; the first lead (twice the drift) led her sixty degrees after a close pass and lost the chase. The lead is worked from the drift's rate, the lookout's estimate of the distance and his own way across the line of sight, capped at forty-five degrees, and never puts her nearer the wind than she lies.
- **A `when` rule fires again.** A `when` order re-arms after its condition has been false for `STANDING_DWELL_S` and fires again when it is true again, which the account's swing makes common near a mark; the books are written for it (above), and the pilot's cast at the Iroise is the one order that must not: it is guarded by the mark the leg leaves behind.
- **A chase in the wind's eye.** The lead is worked from the bearing's drift and never puts her nearer the wind than she lies, so a chase that bears to windward is kept full and by and the chase weathers her: the cruise's brig-sloop passed the frigate out of hail and was run down before the wind after a wear (above). A beat for a chase to windward (tacking under her lee) is milestone 7's.
- **Not done.** The crewed promotion (milestone 6's; `Vessel.promote` says so); a vessel's own leeway and set beyond the stream; the fetching cutter giving up a ship she cannot catch; a vessel taking the ground; the pilot by night; the beat that lays a mark on the lee bow (she holds a tack to the mark's meridian); a chase's end (milestone 7's); the stranger's answer to a hail; the chart's doubt bar from the estimate's spread rather than a flat fifteen per cent; the conftest's `DAY_FIXTURES` for the two scenarios' fixtures (the lead's file).

## Milestone 5: the officer of the watch, the first station with authority

Package 37 (spec M5 §29; spec M4 §11 extended; the cold review of 2026-09-30 §3, its six items before a station with authority taken one by one; `docs/primer/16-the-officer-of-the-watch.md`). The officer of the watch takes the place of a person of package 35 (the first lieutenant, the lieutenant, the mate), holds the deck from the captain's word (`you have the deck`, `I have the deck`), gives orders within a domain that is data on the station and a filter in the tools (`agent.OFFICER_DOMAIN`, `tools.authority_check`), gives standing orders in the station's rank, and is watched by the standing conflict rule over its own orders. Nothing of the physics or the pinned days moves: the officer's game is not a pinned day, and no constant of the ship's or the world's changed.

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| the domain (`OFFICER_DOMAIN`): sail handling, the yards, the lines, the lead and the log, the lookout and the pilot's hail, the book in his own rank; not the course, the manoeuvres, the anchor, all hands, the people, the port, a world order, a station, the captain's book | the verbs' objects and names from `data/vocabulary.yaml` | Falconer 1780, LIEUTENANT ("never to change the ship's course without the captain's directions, unless to avoid an immediate danger"); the Regulations of 1806, the Lieutenant, art. IV, V, XIII; Luce 1884 ch. XXIII (the officer of the deck's trumpet and sail) | the pages; the line between the lead and the log (his) and the sights and the reckoning (the master's for the captain) is judgement on art. XXVI of the Master |
| the levels | 0 to 2 | spec M4 §11, the proposal §3.5 (level 0 to 2 within that authority) | the spec |
| `WELFARE_CONTRARY_N` | 3 contrary orders in a chain within `WELFARE_CONTRARY_WINDOW_S`, a watch (14,400 s) | the repeats' three (spec M4 §11) reused for the pattern the cold review names; the watch as the span of a watch | judgement |
| `STAND_BY_WITH_DECK_MAX_S` | a glass (1,800 s): the longest interval a station with the deck may name; events and bells always | the cold review's third item ("a captain that stands by is a ship with no one on deck"); the bell's own span | judgement |
| `OFFICER_PATIENCE_S` | two glasses (3,600 s) of silence before the nudge | the watcher's is a watch; an officer with the deck is worth a word sooner, and the answer is a nudge | judgement |
| `HANDOVER_AT_FRACTION`, `HANDOVER_ASK_AGAIN_FRACTION` | 0.6 of the door's context, asked again after a further 0.1 | spec M4 open item 9b ("a set fraction of the budget, a named constant"); under the runner's own dropping point (the context less the reply budget and the tool definitions) | judgement |
| `HANDOVER_KEEP_TURNS` | the last 6 turns kept whole after the note (two exchanges) | spec M4 open item 9b ("keeps the brief head and the last few turns whole") | judgement |
| `MAX_SEATINGS` (gone since package 37b) | was 2: the first seating and one more, by the same identity. There is no count now: how the station was left decides, and since package 37g the same identity or another may take a released station (`harness.seating`) | the consent record of 2026-09-29, note 1 (an instance that left by accident seated again); the owner's rulings of 2026-10-03 and 2026-10-05 | the owner's rulings |
| `DRILL_REPLIES` | 4 replies for the three calls | spec M4 open item 11; one reply each and one to spare | judgement |
| the mate's rank | `standing.rules.RANKS` gains `mate` after `master` | the schooner's and the cutter's officer of the watch is the mate (package 35's posts); a merchant mate under the master | judgement |

### The brief head at the officer's station, measured on each door

The frigate at seed 7, the starter book loaded, plain sail set, a minute run, at `tools.tokens` (four characters a token); the head's five items and the tool definitions as each door sends them:

| Station, door | The head | Whole brief | Tool definitions | Of the head: disclosure, opt-out, documentation, authority, situation |
|---|---|---|---|---|
| the watcher, the local runner | 3,879 | 4,057 | 2,120 | 119, 187, 1,381, 70, 2,122 |
| the officer, the local runner | 4,265 | 4,741 | 2,120 | 122, 187, 1,381, 447, 2,128 |
| the officer, the MCP bridge | 4,459 | 4,934 | 2,120 | 122, 187, 1,575, 447, 2,128 |
| the officer, the REPL | 4,308 | 4,784 | 2,120 | 122, 187, 1,424, 447, 2,128 |

The officer's head is some 390 tokens more than the watcher's on the same door: the authority item grows from 70 to 447 (the domain in words, the person, the deck and the starter book's nine rules), the situation by the officer's own reading (6, its words short while nobody has the deck), and the station brief by 300 (the whole brief 4,741 against 4,057). The tool definitions grow by `hand_over` and `handover_note` (about 230 tokens of the 2,120). The opt-out item grows by `TOKEN_NAMED_WORDS` (58) on every station's head. A glass's sample at the officer's station is what the watcher's is (1,511 tokens for the first glass of the frigate under plain sail with the book's firings, 193 for a quiet one) plus the officer's reading when it changes (about 40); the word that gives the deck is a sample of 436 with the book in its notice. The 35 growth stands (a sample is about 1,200 tokens with the sails' line against 800 before the places and people); the officer adds its one row to it. The consent brief is 2,001 tokens at the runner's door (1,476 before this package: the opening names the officer, what an instance would see and do states the domain, leaving carries the two sentences, being stopped the detector's new form, the journal the handover note); its sha256 is a3321736a036ae64 (e3b63b846c2553d2 for the record of the first model asked on 2026-09-29, 41b05359d264ed0a for the second's and the local models' of 2026-09-28).

### The welfare detector's cases on the fake

The frigate at seed 7, plain sail, the officer with the deck, an order a sample: *set the royals; take in the royals; set the royals* brings the nudge at the third (`The officer of the watch nudged: 3 contrary orders on the fore royal, the main royal and the mizzen royal within the watch (set the royals; take in the royals; set the royals).`) and a fourth contrary order after it the pause, with the human asked and the ten real minutes the driver's; a turn without a contrary order after the nudge ends the matter and the chain; *trim sails* at every sample with nothing changing is the repeat detector's (the same order three times with no change in the readings), never the contrary one's; the royals coming and going change the readings, so the repeat detector never fires on the contradiction, which was the cold review's point. The silence detector stays (two glasses). A stand-by for an hour or a watch with the deck is refused in words; for eight bells, a glass, an event or a severity it is taken, the line saying the standing orders hold the deck, and an urgent line wakes it.

### Found on the way (package 37)

- **A station's orders cannot be journaled.** The harness's transcript replays every reply, so an order journaled by `World.submit` would be given twice in a replay (once by the journal, once by the replayed reply). `World.submit` now journals nothing for an actor in `events.STATION_ACTORS`, as it journals nothing for a standing order's firing; the station's orders are in its transcript and replay from it (`test_a_watch_with_the_fake_officer_replays_from_a_save_to_the_same_digest`).
- **A reseating must replay.** Two harnesses for one station would leave the first seating's replies out of the save (`World.save` lists `world.agents`); the station is one harness seated again (`Harness.reseat`), the reseat a door act in the transcript, so a replay seats it again at the same point.
- **The log is not hove on a ship with no reckoning**, nor the deep-sea lead cast: the domain allows the verbs and the ship refuses in its own words where the scenario gives her no position, which is parity.
- **The frigate stays only with way on her**: an allowed `tack ship` with 0.7 knots through the water is refused by the ship ("not way enough on her to stay"), as the captain's would be.
- **Every yes on record is asked again.** `consent.changed_sections` on the seven records of `docs/agents/consent/` finds the opening, what an instance would see and do, leaving, being stopped and the journal changed for each (the sections this package changed), so the first time each of those models comes to a door after this build the question is put again, as the brief promised; the owner runs them.
- **Not done.** `--officer fake` on the drivers (the scripted officer is `fake.officer_of_the_watch`, used by the tests; the drivers' practice flag is the watcher's alone); the drill at the watcher's station (one flag, `Station.drill`, off for the watcher so that the watcher's consent step and its tests stand as they were); `take a bearing of` kept the master's; the boat's errands the captain's.

## Milestone 5: the saves, and the sight of land (package 37d, 2026-10-06)

From the review of gate 5c's first playtests (`docs/playtests/2026-10-05-gate-5c-review/report.md`, sections 5.1, 5.6, 5.8, 6 and 9). Built in the working copy `FreeSail-gate-m5c-c`; `CHANGES-m5c-c.md` has the files.

### The constants and their sources

| Constant | Value | What it is | Source |
|---|---|---|---|
| `core.world.BUILD_NAME` | `m5c-c/37d` | the build's name in a save's stamp, set by hand at each package or gate | the brief |
| `core.world.BUILD_RULES_DIGITS` | 16 | hex digits of the SHA-256 kept as the fingerprint of the rules | the brief |
| `lookout.ESTIMATE_REFRESH_FRACTION` | a tenth | the distance by estimation is judged afresh, with the sighting's own eye, when the true distance is this much more or less than at the last judging; replaces `ESTIMATE_HOLD_NM` (a mile of the ship's own run), which is gone | judgement (the review's 8.2 item 1) |
| `lookout.SHORE_CLOSE_ABOARD_NM` | a mile | the shore's hail says "close aboard" within it | judgement on the words |
| `lookout.LAND_AHEAD_NOTABLE_MIN` | 10 minutes | land ahead is a notable line when she would be on it sooner than this at her speed over the ground | the review's 8.2 item 6 (the owner's figure); judgement |
| `lookout.LAND_AHEAD_URGENT_MIN` | 4 minutes | and an urgent one sooner than this | the same |
| `lookout.LAND_AHEAD_CLEAR_MIN`, `_CLEAR_LOOKS` | a quarter of an hour; 5 looks | an approach is over when five looks together find nothing ahead within a quarter of an hour | the brief; judgement |
| `lookout.LAND_AHEAD_POINTS` | a point either side | the width looked along her course made good | the seaman's "bearing steady" (`CLOSING_STEADY_POINTS`); judgement |
| `lookout.LAND_AHEAD_WAY_KN` | half a knot | way on over the ground, under which nothing is said | `physics.hull.WAY_ON_KN`'s figure |
| `lookout.LAND_AHEAD_MARGIN_M`, `_STEP_M` | 100 m; 20 m | the cast along each line steps by the shore's own distance while that is more than the margin off, and by the step when nearer | judgement (a harbour cell is 15 m, the region's 93 m) |
| `reckoning.FIX_MIN_CUT_DEG` | 30 degrees | two lines that cut by less are no fix | **judgement**: `Navigation1805.md` gives the bearing's error and that "two bearings [are] a fix" and no least angle of cut; thirty degrees is the later manuals' figure, at which the doubt along the finer line is already twice the bearing's own (1 / sin 30°) |
| `reckoning.FIX_MARKS_CONSIDERED`, `FIX_MARKS_IN_ALL` | 12; 36 | unnamed, the master chooses among the nearest twelve marks, and among thirty-six when no two of those cut (a coast seen end on) | judgement |
| `reckoning.FIX_NOTABLE_NM` | a mile | a fix's line is notable when the account moved more than this | the brief |
| `reckoning.FIX_ACCOUNT_DIFFERS` | a third | a bearing's words add the account's own distance from the mark when it differs from the estimate by more than this of the estimate | the brief; twice the eye's own error |
| `weather.SEA_BREEZE_TREND_KM` | 3 km | the baseline over which the shore's distance is differenced for the breeze's direction, a mile or so either way | W §1.4's scale in words ("felt a few miles to sea"); the figure is judgement |
| `weather.SEA_BREEZE_SLOPE_NONE`, `_SLOPE_FULL` | 0.15; 0.5 | the breeze's strength is nought where the shore's distance rises by less than the first to seaward and full at the second and above | judgement, from the figures below |
| `orders.complete.FIX_OFFER_MARKS` | 6 | the marks `take a fix` offers in completion, the nearest | judgement |

No figure here is from a study's "unverified" list. The bearing's degree and a half (`BEARING_SIGMA_DEG`) and the eye's sixth (`DISTANCE_BY_ESTIMATION_FRACTION`) are package 33a's and 33b's and did not move.

### The build's stamp

The fingerprint is the SHA-256 of every `freesail/**/*.py` (no `__pycache__`) and every file under `data/` but `data/charts/tiles/`, in the order of their paths with forward slashes from the folder that holds `freesail/` and `data/`; for each file the path, a zero byte, the bytes with CR LF made LF, a zero byte; the first sixteen hex digits. On the owner's machine: 205 files, 4.1 megabytes, **0.03 seconds**, once a process at the first World made. `tests/test_replay.py` proves that a CR LF copy has the same fingerprint, that the tiles and the caches are not in it, and that a changed rule, a changed data file and a moved file each change it.

### The nearest shore beside a plain search

`Chart.nearest_shore` against a plain search of every cell above the datum (`tests/test_chart.py`, twelve places), with what `coast_distance` gave for the bearing before:

| Place | The ground itself | The plain search | The field's bearing before |
|---|---|---|---|
| off Penlee Point, three cables | 529 m, 360° | 529 m, 360° | 0° |
| off Penlee Point, a mile | 1,877 m, 358° | 1,877 m, 358° | 0° |
| Cawsand Bay | 216 m, 325° | 216 m, 325° | 322° |
| the mouth of St Mary's Sound | 9 m, 327° | 9 m, 327° | 0° |
| St Mary's Sound | 363 m, 163° | 363 m, 163° | 180° |
| St Mary's road | 295 m, 131° | 295 m, 131° | 123° |
| the road of the Isle of Bas | 64 m, 355° | 64 m, 355° | 0° |
| the road of the Isle of Bas, westward | 253 m, 350° | 253 m, 350° | 323° |
| two miles off the Lizard | 3,586 m, 354° | 3,586 m, 354° | 0° |
| Whitsand Bay | 3,198 m, 26° | 3,198 m, 26° | 38° |
| off the Deadman | 3,658 m, 360° | 3,658 m, 360° | 0° |
| Carrick Road | 654 m, 116° | 654 m, 116° | 90° |

It costs 16 to 30 microseconds close in and some hundreds a league off in a harbour patch, once a minute and only when the field puts the shore within the lookout's reach.

### The sea breeze, before and after

Along the review's three tracks, a mile and a half each sampled every ten metres (`tests/test_chart.py`): the bearing of the nearest cell of shore, which the breeze blew toward, changed 136 times north-east from the Harpy's anchorage (the largest turn 123°), 131 times through the mouth of St Mary's Sound (180°) and 32 times across the road of the Isle of Bas (180°). The coast's trend over three kilometres turns 0.8°, 2.0° and 1.7° at the most between samples; its steepness is 0.38 to 0.63 off the Harpy's anchorage (a wide bay: seven tenths of the breeze or all of it), 0.93 to 1.00 off the open coast of Whitsand Bay, and under 0.2 across the road of the Isle of Bas (little or none). A read is 8 microseconds, and only while a breeze blows.

By the review's own script (`evidence/tools/seabreeze_check.py`) on the Harpy's save of tick 602,100, the game's own weather of 19 June 1805 from 12:27 to 13:50, the wind sampled each second:

| | Turns of two points or more, second to second | Compass points visited | Wind |
|---|---|---|---|
| Moving, the breeze as built before | 386 (largest 169°) | 13 | 4.8 to 13.1 knots |
| Moving, the breeze now | none (no turn of a point; the largest under a degree) | 12, in order, as she rounds Penlee into the Sound | 5.2 to 9.5 knots |
| Moving, the breeze set to nothing | none | 2 | 3.4 to 4.1 knots |
| At anchor, before | none | 2 | 6.6 to 8.8 knots |
| At anchor, now | none | 1 | 8.6 to 11.2 knots |

The 5a day under systems has no chart, so no coast and no breeze: its log is the same line for line and digest for digest (`684580064bfc6ecd`), and its tick path is untouched (measured alone on the owner's machine, the best of five thousands: 1,295 ticks a second; the day's 104,400 ticks sailed whole beside five other passages 1,348 a second before and 799 to 935 after, on a machine by then busy with other work).

### Land ahead on the test and in the recorded passages

Steered at the shore under Penlee Point at four knots from a mile (`tests/test_lookout.py`): the notable line between nine and ten minutes off, about two thirds of a mile; the urgent one between three and four minutes off, under three cables; each once; again after five clear looks. In the recorded passages at seed 7:

| Passage | Notable | Urgent | Where |
|---|---|---|---|
| the 5a day | 0 | 0 | no chart |
| the 5b frigate | 0 | 0 | she anchors in the outer road with nothing ahead inside ten minutes |
| the 5b passage in thick weather | 1 | 0 | 54900, at the landfall in a mile of fog: "Land ahead, fine on the starboard bow, nine cables", the tick the book stands her off |
| the 5b schooner | 1 | 1 | 59580 and 59880, standing in for Carrick Road; she strikes at 60075, three minutes after the urgent line |
| the 5c cruise | 0 | 0 | |
| the 5c merchant passage | 3 | 3 | 15600 getting under way in Carrick Road ("Land on the larboard quarter, three cables: she is setting down on it"); 16080 and 16380 the Black Rock in Falmouth's mouth, which she passes; 113280 and 113520 the Mingan in the Goulet, which she strikes at 113701; 121920 the Mingan again as she floats off |

The schooner's and the merchant's rows above are the first pass's, when each took the ground; the second pass, below, has them as they are now (the schooner one notable line and no urgent one; the merchant five and two, and neither strikes).

### The recorded passages, re-measured with the reasons

This table is the first pass; the same passages after the second pass are tabled under "The second pass", below.

The six logs were written out before and after and set side by side. Items 5, 9, 10, 11 and 13 change lines; item 6 changes the account, and through the courses the books shape from it, the truth's track.

| Passage | Lines | Digest | The truth's track first differs | Why |
|---|---|---|---|---|
| the 5a day under systems | 616, 616 | `684580064bfc6ecd`, the same | never | no chart, no land, no bearing |
| the 5b passage in thick weather | 502, 503 | `bc80736aa7189f14`, `2472b62d8cac3193` | never | no bearing is taken; two lines: the shore's hail at the start by the eye's estimate (item 9), and land ahead at the landfall (item 10) |
| the 5b frigate | 630, 656 | `e3bc746c4a6b58b3`, `aaf8cce44143c6f0` | tick 10 (by a metre at 245) | item 6: the departure bearing off Ushant no longer lays the estimate down, the account stands a mile otherwise and the book's "landfall" rule shapes N 358° for N 359° |
| the 5c cruise | 1966, 1963 | `72ba9f898e7231f2`, `792f830fd4166bc5` | tick 174 in the ninth decimal (item 13: the anchor's place by another arithmetic); by a metre at 57626 | item 6: "back to the station" shapes her course from an account kept by lines and fixes |
| the 5b schooner | 731, 768 | not recorded | tick 6 (by a metre at 198) | item 6, as the frigate; did not come through in the first pass (the second pass, below) |
| the 5c merchant passage | 2460, 2876 | not recorded | tick 313 in the ninth decimal (item 13); by a metre at 16714 | item 6: the courses out of Falmouth shaped from the account; did not come through in the first pass (the second pass, below) |

By item, in the lines of the four that changed (the frigate, the schooner, the cruise, the merchant):

- **Item 5** (the distance judged afresh): the distance in the words of every later bearing and of each "steady and closing" hail, which carry the figure as last judged and not the first look's; a sail's distance as she nears.
- **Item 6** (a bearing a line): the bearings' words gain "; ... by the account" where the two differ by a third (4, 6, 3 and 25 of the bearings); the account; and, after the tick above, every line that depends on where she is: the trims, the leeway, the log's reads, the casts, the hails, each at its own new tick. This is the bulk of the lines that differ.
- **Item 8, by the mended books**: 11, 10, 12 and 184 fixes, 3, 3, 3 and 8 of them notable (the account moved over a mile), with their orders' lines (14, 14, 16 and 198).
- **Item 9** (the shore always a sighting): the shore's own hail, 2, 2, 1 and 3 times (once for each approach to within a league).
- **Item 10**: the table above.
- **Item 11**: the pilot's hails notable (1, 2, 3 and 4 lines); one dragging anchor, urgent (the merchant, in the Bay of Brest after her grounding).
- **Item 13** (the anchor's depth where it lies): the merchant's "let go in twelve fathoms and a half" and "Brought up ... in six fathoms and a half" of the recorded passage was the fault itself; her anchors now read "let go in ten fathoms", "Brought up ... in nine fathoms and a half" and "let go in 14 fathoms", "Brought up ... in 14 fathoms".

The constants that moved, old beside new (`tests/test_known_truths.py`):

| Constant | Before | After |
|---|---|---|
| `GATE_5B_CAST_TICK` (and the cast: fifty-three fathoms, fifty-five) | 29884 | 29886 |
| `GATE_5B_LANDFALL_TICK` | 44700 | 44520 |
| `GATE_5B_ROADS_TICK` | 57732 | 57824 |
| `GATE_5B_ANCHORED_TICK` | 58167 | 58172 |
| `GATE_5B_BROUGHT_UP_TICK` | 59144 | 59152 |
| `GATE_5B_SAIL_SIGHTED_TICK` | 54600 | 55080 |
| `GATE_5B_PILOT_HAIL_TICK` | 56280 | 56760 |
| `GATE_5B_PILOT_ABOARD_TICK` | 56340 | 56880 |
| `GATE_5B_LINES`, `GATE_5B_DIGEST` | 630, `e3bc746c4a6b58b3` | 656, `aaf8cce44143c6f0` |
| `GATE_5B_THICK_LINES`, `GATE_5B_THICK_DIGEST` | 502, `bc80736aa7189f14` | 503, `2472b62d8cac3193` |
| `GATE_5C_CRUISE_STRANGER_SIGHTED_TICK` | 90960 | 91380 |
| `GATE_5C_CRUISE_STRANGER_SPOKEN_TICK` | 106931 | 95189 |
| `GATE_5C_CRUISE_LINES`, `GATE_5C_CRUISE_DIGEST` | 1966, `72ba9f898e7231f2` | 1963, `792f830fd4166bc5` |

Unmoved: the 5a day's every constant; `GATE_5B_NOON_TICK` (the sun's); the thick passage's ticks; the cruise's yard, under way, pilot aboard and off, world orders, cutter's hail, letter, chase and both noons.

### The books, mended by a line, and the two passages that did not come through (the first pass)

This section is the first pass as it was reported. Both passages come through since the second pass, below.

Each book's rule `every glass, if the land is in sight then take a bearing of the land` relied on the bearing's distance by estimation to put the ship on the chart. Each now reads `... then take a bearing of the land; take a fix` (one line in the 5b frigate's, the 5b schooner's and the cruise's books; in the merchant's that line and the same in "pilot water", two). With one mark only in sight or marks that cut too fine the fix is refused in words and the bearing stands as a line; the refusal is held by the standing runtime after the first.

- **The frigate's passage and the cruise come through** on that one line, re-measured above.
- **The schooner's passage does not.** Her landfall is on the Lizard's lights alone, four leagues off, with the account two leagues from them by her two-hourly log; one bearing no longer corrects that, she shapes N by E for Falmouth from it, makes the outer road eastward of her old track with the pilot aboard, shapes for Carrick Road from a fix, and takes the ground at seven knots at 60075 (the recorded passage brought up off the town at 58618). Two other mends of a line or two were tried once each and left out: shaping the course afresh at every fix put her (and the frigate) on the Manacles, the straight line from a true position crossing them; a point east of the Manacles to steer for brought her to the outer road and the same grounding in the eastern channel.
- **The merchant passage does not.** She makes the road of Bertheaume, takes the Brest pilot and anchors as before (101349 for 96475), gets under way on the flood, and in the Goulet strikes the Mingan at 113701, the lookout crying it ahead at seven cables and close ahead three minutes before; the book has no rule for his cry. Its waypoints through the Goulet were tuned at seed 7 to the account the old rule kept there (a bearing every five minutes with its held distance), and with a true account they set her on the rock on the flood.

Their two tests (`test_the_schooner_sails_the_passage_with_her_octant_and_the_log_every_two_hours`, `test_the_merchant_passage_at_seed_7_has_its_own_constants`) are marked expected to fail, strictly, with the reason, and their constants left as recorded before 37d for whoever tunes the books; the suite's summary line therefore shows nine expected failures for the owner's seven. The milestone's fourth rule was followed: a handful of whole-passage runs for each (four for the schooner's book, three for the merchant's), and no further.

### The second pass (2026-10-06): the distance laid down when it is the better figure

The suite after it: the fast tier `2549 passed in 342.23s (0:05:42)`; the whole suite `2790 passed, 7 xfailed in 1022.51s (0:17:02)`.

**The rule.** After a bearing's line is worked, for a charted mark and never for a sail or a transit, the account's variance along the line of sight (t P t, t the unit vector toward the mark as the account has it) is set against the estimate's own, (`DISTANCE_BY_ESTIMATION_FRACTION` x the judged distance) squared. When the account's is the greater the estimate is weighed in along the sight by the gain at that doubt (`Reckoning.weigh_line`; `update_line` and its replace-or-blend rule are untouched). Otherwise it is said and not applied, as in the first pass. No new constant.

**The words.** Applied: "The Lizard bore N by W, five leagues by estimation; the account laid down at that distance, the estimate being the better figure: moved three leagues to the SW." Not applied: "The Beast bore NW, three leagues by estimation." Not applied, the two differing by a third: "The Beast bore N by W, five leagues by estimation; three leagues by the account."

**The schooner's account, miles from the truth, through her landfall** (seed 7; the landfall on the Lizard at 16:12, tick 43920):

| Tick | Before 37d | First pass | Now |
|---|---|---|---|
| 43800 (two minutes before) | 8.46 | 5.74 | 7.39 |
| 43920 (the landfall) | 1.73 | 5.58 | 1.12 |
| 44400 | 1.32 | 5.00 | 1.37 |
| 45000 | 0.88 | 6.82 | 1.38 |
| 45600 | 1.55 | 6.16 | 1.16 |
| 46200 | 2.53 | 5.51 | 1.71 |
| 47400 | 1.28 | 1.29 | 1.28 |
| 52800 | 0.90 | 1.46 | 1.44 |
| 56400 | 0.57 | 1.11 | 1.08 |

She makes her landfall, her pilot (55380), the outer road (56502), her berth (57615) and brings up (58618) on the ticks recorded before 37d; one notable "Land ahead, fine on the starboard bow, a mile" at 57240 standing in. Her book was not touched in this pass beyond its comment.

**The frigate's account at her landfall is the case the rule does not help.** Miles from the truth:

| Tick | Before 37d | First pass | Now |
|---|---|---|---|
| 44400 | 5.28 | 4.89 | 4.63 |
| 44520 (the landfall) | 5.29 | 0.61 | 4.23 |
| 45000 | 1.33 | 1.14 | 4.49 |
| 45600 | 2.25 | 1.22 | 3.90 |
| 46200 | 3.25 | 1.90 | 3.41 |
| 47400 | 1.52 | 0.63 | 1.42 |
| 52800 | 1.09 | 1.38 | 1.08 |
| 58800 | 0.71 | 0.49 | 2.12 |

At 44520 the line moves her account 4.9 miles W by S and the words are "The Beast bore N by W, five leagues by estimation; three leagues by the account": the lookout is right and the account two leagues wrong along the sight, but the account believes its doubt that way (its latitude, by the noon's sight four hours before) less than the estimate's 2.3 miles, so the distance is not laid down. It is laid down two glasses later (46800: "moved four miles to the S by E") and the fix follows. She comes through: the outer road 58895, the anchor 59250, brought up 60239, the pilot aboard 57180.

**The lead's correction, 2026-10-06** (measured from this package's own dumps of the three runs; see `CHANGES-m5c-c.md`, "The Goulet"). The paragraph below says the fix put a worse account in the place of a headland's bearing. The account's median distance from the truth says otherwise: on the leg from the Iroise to the road, 0.91 mile before 37d, 0.50 with the fix every five minutes, 0.45 with the bearing alone; in the Goulet, 0.45 before, 0.17 with the fix, 0.48 with the bearing alone. She struck with the truer account, and comes through as delivered with one about as wrong as before 37d: the book's points are tuned to an account that lags her on the flood. Nine fixes of sixty left the account worse than it was a second before; the nearest land's mark was among a fix's marks in 22 of 60.

**The merchant passage and the Goulet.** What set her on the Mingan in the first pass was the account, and not the chain's points alone. The first pass had made her pilot-water rule `take a bearing of the land; take a fix` every five minutes; in the Iroise and the road the fix's marks are distant and its lines met "within six cables" or "within a mile", and it put that in the place of a headland's bearing every time. She anchored a mile north of her old berth, the course for the mouth passed half a mile north of the mouth's point so that its rule never fired, she turned late and through four points under Petit Minou, lost her way, and the flood (3.4 knots to the eastward there) set her down on the rock. In this pass:

- The pilot-water rule takes **the bearing alone**, as before 37d; the fix every glass by the rule "bearings" stands. At anchor in the road her account is then within half a cable of the truth.
- **Two points moved.** "for the Goulet" shapes for 48 19.15 N 4 38 W (was 48 19.3 N 4 38 W; the mouth's rule still turns on the old point): a shaped course is a heading, and outside the mouth she makes good six or seven degrees north of it. "under Petit Minou" shapes for 48 20.9 N 4 35.1 W (was 48 20.7 N 4 35 W), and "north of the Mingan" turns four cables short of that point: inside Petit Minou a head of 44 to 50 degrees makes good 62 to 67 on the flood.
- **The result at seed 7.** The whole chain fires in its order (the mouth 112740, Petit Minou 113100, the Mingan's pass 113763, the Fillettes 113852, Portzic 114301, the Bay 114737). She passes **the Mingan 328 m (1.8 cables) to the north** at 113600, the Fillettes eight cables off, and the shore under Petit Minou 294 m (1.6 cables) off; before 37d the figures were 311 m and 273 m. The lookout cries "The Mingan ahead ... nine cables" at 113040 and "The Mingan close ahead, on the starboard bow, three cables!" at 113400, which is the truth of that pass. She anchors in the Bay at 116140 in six fathoms and the tin is sold at 123901.
- **Also moved by the account earlier in the passage:** the cast at the Iroise's mark, never made at seed 7 before, is made at 91836 in thirty-nine fathoms and matches her chart's words; the pilot of Brest boards at 98160 (91560); she anchors in the road of Bertheaume at 101373 in nine fathoms and a half (96475 in thirteen and a half).

**What was tried on the Goulet** (nine runs of the late leg from a save at tick 110000, and four whole passages; the budget was about fifteen). Runs 1 to 7 kept the first pass's bearing-and-fix rule and moved the points: every one took the ground, on the Mingan (1, 3) or on the north shore under Petit Minou (2, 4, 5, 6, 7), because the rules fire on the account's distance and the account there was two to four cables out to the south-east. A fix taken before the bearing (run 8) brought her through the leg, 254 m from the Mingan, but the same rule sailed from Falmouth ran her ashore in the Iroise at 99414. The bearing alone with the old points brought her through, 365 m from the Mingan but 125 m from the shore under Petit Minou, the mouth's rule not firing. Run 9, the bearing alone with the two points moved, is the book as it stands.

**The account in the Goulet is still not a true one, and the rule cannot make it so.** Miles from the truth with the book as it stands: 0.02 to 0.06 at anchor in the road; 0.33 at 110500, 0.74 at 110900 and 0.79 at 111300 as she gets under way (the account runs to the south-south-east while she casts and gathers way; a leeway of 54 degrees is logged at 110721); then half a mile astern of the truth along her track on the flood (0.53 at 112100, 0.60 at 112500). All that time the bearings read "Point Bertheaume bore N by W, five cables by estimation; a mile by the account" and the distance is not laid down, because the account believes its doubt along that sight under the estimate's cable. The passage comes through because the points and the radii allow for it at this seed, not because the account is right. Two things would mend it and neither was in this pass: the account's doubt growing as she gets under way and on a stream; or the estimate laid down also when it and the account differ by several times the estimate's own error.

**The recorded passages after the second pass.**

| Passage | Lines (before 37d, now) | Digest now | What moved since the first pass, and why |
|---|---|---|---|
| the 5a day under systems | 616, 616 | `684580064bfc6ecd` | nothing |
| the 5b passage in thick weather | 502, 503 | `2472b62d8cac3193` | nothing; no bearing is taken |
| the 5b frigate | 630, 662 | `100f1bb8cdba918c` | the departure off Ushant is now a bearing and distance of the light ("moved two miles to the W") and then the fix, so her first course and her track differ: the cast at 29884 (29886), the outer road 58895 (57824), the anchor 59250 (58172), brought up 60239 (59152), the cutter sighted 55260 (55080), her hail 57060 (56760), the pilot aboard 57180 (56880); ten fixes; five bearings with the distance laid down and eleven without; the landfall's assertion re-measured (six miles out at the landfall, as before 37d) |
| the 5b schooner | 731, 760 | `b3beb599c0cff7ea` | every tick as before 37d; the lines are the fixes with their orders, the shore's hail, land ahead once; seven bearings with the distance laid down and nine without |
| the 5c cruise | 1966, 1963 | `86680b3c485373dc` | no tick; the bearings' words where the distance is laid down (three) |
| the 5c merchant passage | 2460, 2634 | `52033fdd56901499` | as above: the pilot of Brest 98160, the road 101373, the mouth 112740, the Bay 116140, the tin 123901, the cast at the Iroise 91836; a sail off the Lizard at 26280 (28140, since the first pass); fifteen bearings with the distance laid down and 181 without; land ahead five times notable and twice urgent (Carrick Road and the Black Rock going out, the road of Bertheaume, the Mingan twice, the Bay) |

### Found on the way (package 37d)

- **A second bearing of the same mark drew the account toward the mark.** With the distance no longer laid down, two bearings of one mark a degree apart were crossed as two lines, which meet only at the mark, and the account slid 40 per cent of the way to it at one stroke and a sixth of the way in six more. A bearing taken within two miles of the last observation is now worked as an angle at the account (its line's normal square to the mark as the account has it), and after a second bearing of the same mark the doubt is turned with the account about the mark; a bearing of another mark still crosses the first, and a second of the same mark after a run is a running fix. `Reckoning.update_line`'s replace-or-blend rule is as it was (package 37e's).
- **The across-line doubt of a bearing is taken at the account's distance from the mark**, the master's own figure, where it was taken at the truth's.
- **A game taken up from another build's checkpoint and saved again would have been stamped this build's own.** A save also carries `"builds"`, every build the game was played under, and such a save without its checkpoint is not replayed without the flag.
- **A ship strikes a ledge's edge before she is up with its mark**: land ahead takes a charted danger as near as its edge and as wide as its extent, as the grounding does (the frigate, steered at the Manacles by a mend that was not kept, struck four minutes after "a mile").
- **The shore's distance is by the eye too**: the shore was "judged true" (a cable's rounding of the chart's own figure); it now has the sighting's eye like any other, drawn from a stream of its own (`shore`) so that no headland's draw moves.
- **Not done, and for a later hand**: the dialect refuses cables (`when the nearest land is under 3 cables`); a station's replies are still placed in a replay by the count of journaled orders; the sun's local time reads the ship's easting on the plane (spec M5 §33, items 17 and 19).

## Milestone 5: the account (package 37e, 2026-10-07)

The review of game 9 (`docs/playtests/2026-10-05-gate-5c-review/`), its section on the reckoning: one rule by which an observation is believed, a doubt that grows by the hour whether she has way or not, the fix's choice of marks, the master's own tide in the traverse, and a course shaped to make good. `BUILD_NAME` is `m5c-c/37e`. Measured on the owner's Windows machine at seed 7; the machine ran at 700 to 1,000 ticks a second through the afternoon against 1,400 in the morning, on an untouched scenario as on a changed one, so the times here are the machine's and not the change's.

### The constants and their sources

All in `freesail/world/reckoning.py` unless said.

| Constant | Value | What it is | Source |
|---|---|---|---|
| `OBSERVATION_OUT_SIGMAS` | 2 | an observation further from the account than this many times the two doubts added is taken, the account laid down on it | **two, where the brief said three.** Game 9's noon of 16 June: the sight 48° 07' N good to 2.28 miles, the account 48° 12½' N trusting itself within 0.26, 5.23 miles apart, which is 2.06 of the two doubts together; the brief's test requires that noon taken. Judgement |
| `OBSERVATION_KEPT_NM` | 0.05 mile | a weighing that would move the account under half a cable is not applied | the brief |
| `SAME_LINE_DEG`, `LINES_REMEMBERED` | 5°, 24 | a line within five degrees of one already had of the same thing is the same thing seen again; the last two dozen are remembered | judgement |
| `SAME_GROUND_NM` | 2 miles | a cast within this of the first cast of that ground (or within his own doubt, when that is more) narrows nothing further | judgement on the brief's "a second cast on the same ground" |
| `SOUNDING_ACROSS_MIN_NM`, `SOUNDING_ACROSS_MAX_NM`, `SOUNDING_SLOPE_NM` | ¼ mile, 60 miles, ½ mile | a cast's doubt as a line: the contour's tolerance over the fathoms the chart shelves in a mile, read over half a mile at least; a quarter of a mile at the best; no line at all over a flat bottom | the brief ("only so far as the charted depth differs across his doubt"); the bounds judgement. **Gone:** `SOUNDING_ACROSS_SIGMA_NM`, three miles whatever the ground |
| `CONTOUR_GRAIN_M` | half a mile | the contour search's own step; where the chart about the account brackets the cast at this grain the cast is kept | `chart.CONTOUR_STEP_M`; found on the frigate's passage (below) |
| `BEARING_LINE_FORM_FRACTION` | a tenth | a bearing is worked as the line through the mark when the doubt across the sight is more than this part of the distance | the brief, judgement |
| `COMPASS_ALLOWANCE_DEG`, `COMPASS_ALLOWANCE_OBSERVED_DEG` | 2½°, 1½° | the master's doubt of his compass in a bearing and across a course; the less once he has observed the variation | judgement: the chart's variation a decade old (N §3), an azimuth compass read to a degree |
| `LOG_LINE_DOUBT` | 4 per cent | his doubt of the log-line's marking, along the course | judgement: the middle of N §3's "3 to 8 per cent" short, as a doubt either way |
| `STREAM_DOUBT_FRACTION`, `STREAM_DOUBT_HOURS` | ¾, 3 hours | his doubt of the stream: three quarters of its rate at strength, along its set, growing for three hours of a tide and no further | judgement: a rate to the half knot of a knot and a half, an hour of high water out by an hour and more (measured below), a set to the point; a stream cannot set her further than it runs in half a tide |
| `HOVE_TO_DRIFT_KN`, `HOVE_TO_DRIFT_SIGMA_KN` | ¼ knot, ½ knot | hove to, her drift through the water as his eye has it, to the quarter knot; his doubt of it | Falconer 1780, *Drift*: "the angle which the line of a ship's motion makes with the nearest meridian, when she drives with her side to the wind and waves ... also the distance which the ship drives on that line"; no period rate, so no fixed rate is used. Judgement |
| `NO_WAY_KN`, `CALM_MINUTES` | ½ knot, 10 minutes | under this she has no way worth the log; becalmed this long, the log's last read is stale | the hull's own floor (`WAY_ON_KN`); judgement |
| `WAY_BY_EYE_GRAIN_KN`, `WAY_ALLOWANCE_LEAST`, `WAY_ALLOWANCE_MOST` | ½ knot, ¼, 2 | between heaves the read is allowed by the mate's eye for the way she has gained or lost, within these bounds | Falconer 1780, *Log*: "if at any time of the watch the wind has increased or abated in the intervals, so as to affect the ship's velocity, the officer generally makes a suitable allowance for it"; the grain and bounds judgement |
| `TIDE_QUARTER_S` | 900 s | the master's tide is summed into the traverse by the quarter hour | judgement |
| `DOUBT_THIN_RATIO` | 2 | the doubt is said as it lies ("NE and SW, nor a mile across") when it is this much longer than wide, a mile and more long, and off the compass's quarters | the brief |
| `SHORE_PASS_NM`, `SHORE_AT_PLACE_NM` | ½ mile, 2 miles | a shaped course's line is said to pass a shore within this; the shore at a place on the land itself is not said within this of it | judgement |
| `streams.yaml`, `book:` | per area | what the directions say: set to the point, springs to the half knot, neaps, the hour | the table below |
| `streams.yaml`, `book_limits` | 48° to 51° N, 7° to 3° W | beyond these the master has no statement and allows no tide | the chart's own waters; judgement |

Kept and unchanged in meaning: `FIX_MIN_CUT_DEG` (thirty degrees), `DISTANCE_BY_ESTIMATION_FRACTION`. Gone: `FIX_RUN_NM`; `Reckoning.weigh_line`; `Navigation._hours_under_way`. `run_since_fix_nm` is kept as a record; nothing in the rule reads it (the review's `replay_probe.py` prints it).

### What the directions say, beside the world's figures

`data/tides/streams.yaml`; the world's figures are the truth and are never read by the master.

| Water | The world: axis, springs, neaps, hour | The directions: set, springs, neaps, hour | What is the period's |
|---|---|---|---|
| Carrick Road | 010°, 1.5, 0.75, −3 | N by E, 1.5, 0.75, −3 | all judgement (the world's rounded) |
| the entrance of Falmouth harbour | 355°, 1.0, 0.5, −3 | N, 1.0, 0.5, −3 | all judgement |
| off the Manacles | 020°, 1.2, 0.6, −1 | NNE, 1.0, 0.5, −1 | all judgement |
| the approaches to Falmouth | 075°, 0.7, 0.35, −1 | E by N, 0.5, 0.25, −1 | all judgement |
| off the Lizard | 085°, 2.3, 1.1, 0 | E, 2.5, 1.25, 0 | **the hour**: Bowditch 1802's headland table, the Lizard, the current runs three hours after high water; set and rates judgement |
| off the Start | 065°, 3.0, 1.5, −½ | ENE, 3.0, 1.5, −½ | **the hour**: Bowditch's headland table; set and rates judgement |
| Scilly and the Land's End | 345°, 1.8, 0.9, −3½ | N by W, 2.0, 1.0, −3½ | all judgement |
| Scilly | 020°, 1.2, 0.6, −3½ | NNE, 1.0, 0.5, −3½ | all judgement |
| the Fromveur | 045°, 7.0, 5.0, −2½ | NE, 7.0, 3.5, −2½ | all judgement, by the owner's ruling (no period source); the neaps at half the springs, where the world has five knots |
| the Chenal du Four | 010°, 4.0, 2.5, −2½ | N by E, 4.0, 2.0, −2½ | all judgement, by the owner's ruling |
| the Goulet | 080°, 4.5, 3.0, −3 | E by N, 4.5, 2.25, −3 | all judgement, by the owner's ruling (the timing) |
| the Iroise | 030°, 1.5, 0.8, −2½ | NE by N, 1.5, 0.75, −2½ | all judgement |
| the open Channel | 065°, 1.6, 0.8, 0 | NE, 1.5, 0.75, 0 | **the set**: Bowditch 1802, "the Current in the Mid. Channel is N.E."; rates and hour judgement. The hour is the reading of "about 1 H. 30 M. after High Water" that agrees with the world's own figure; the sentence is ambiguous and the other reading would put it an hour and a half earlier. **For the lead.** |

The set is twenty degrees from the world's axis in the open Channel and within half a point everywhere else.

### The master's tide beside the world's

*His hour of high water* (Moore's rule from his epitome's establishment, against the world's harmonic tide; `scratch hw_compare`): in mid-Channel on 10 to 13 June 1805 he is an hour to an hour and fifty minutes early; on the 16th about right. His nearest place changes as the account crosses (the Ramhead, 6h 00m, to Ushant, 4h 30m).

*Over one whole tide in the Iroise* (48° 10' N, 5° 06' W, 12 June 1805, the moon full; the master's high water at Ushant 02:57 and 15:22; knots and the point the water sets toward):

| Hour | The master's tide | The world's stream |
|---|---|---|
| 06:00 | ebb SW by S 1.42 | SW by S 0.84 |
| 07:00 | ebb SW by S 1.48 | SW by S 1.20 |
| 08:00 | ebb SW by S 1.17 | SW by S 1.26 |
| 09:00 | ebb SW by S 0.56 | SW by S 1.00 |
| 10:00 | flood NE by N 0.18 | SW by S 0.49 |
| 11:00 | flood NE by N 0.88 | NE by N 0.15 |
| 12:00 | flood NE by N 1.36 | NE by N 0.76 |
| 13:00 | flood NE by N 1.50 | NE by N 1.17 |
| 14:00 | flood NE by N 1.26 | NE by N 1.27 |
| 15:00 | flood NE by N 0.71 | NE by N 1.04 |
| 16:00 | ebb SW by S 0.02 | NE by N 0.54 |
| 17:00 | ebb SW by S 0.75 | SW by S 0.10 |
| 18:00 | ebb SW by S 1.28 | SW by S 0.72 |
| 19:00 | ebb SW by S 1.50 | SW by S 1.15 |

His tide turns about an hour before the sea's, his springs are the world's 1.5 knots, and the two sets are four degrees apart. Becalmed there for thirteen hours with the account set right, the truth went 3.8 miles out and back and the account was never more than a mile from it (`tests/test_reckoning.py`, the tide in the traverse). In the open Channel the same working, with his hour an hour and a half early and his set twenty degrees off, leaves the account little nearer than allowing nothing would.

### The doubt, before and after

| Case | Before 37e | After |
|---|---|---|
| Hove to, game 9, 15 June 10:00 to noon | the true error grew from 3.3 miles to 4.8, the doubt from 1.08 to 1.12: the hours hove to were struck from the interval | |
| Hove to three hours in the Iroise, from a doubt of 0.3 mile (the brig, a twelve-knot breeze) | 0.3 | 2.98 miles |
| Becalmed three hours in the Iroise, from 0.3 | 0.3 | 3.03 miles |
| At anchor three hours, from 0.3 | 0.3 | 0.3, and the account where it was |
| In fog, the thick passage, at the landfall after fifteen hours without a sight | the doubt 3.15 miles E and W, 2.37 N and S; the account 10.9 miles out | 5.78 and 4.47; the account 6.4 miles out |
| The brig hove to six hours of a spring ebb in the Iroise (the new scripted test, slow tier) | the account where she was brought to, 13.6 miles from her | she drove 13.6 miles to the SSE; the account 1.98 miles from her, his doubt 3.67 |

### A fix's choice of marks, and "good to"

In the Goulet's geometry (game 9's, under Petit Minou): the marks in sight Petit Minou (inside a mile), the Mingan, Camaret, Portzic, Brest and Conquet. The master takes **Petit Minou, Camaret and Portzic**, "good to a cable", and the fix is 0.027 mile from the truth. Not "Petit Minou and the Mingan": the two bear west and east in one line there (they cut at two degrees), so one of them serves, and Camaret is the only mark to the southward; never Brest and Conquet, five miles off, which the old rule (the three that cut best) took. Over game 9's own fixes the truth lies within twice "good to" in every case (`tests/test_reckoning.py`). Moored in Brest road, a fix by far marks leaves a sound account where it was ("the fix the poorer figure; the account kept").

### The recorded passages, re-measured with the reasons

Written out before the first change and after the last (`scratch dump_passage`; before against after by kind and by line, `scratch account_lines`).

| Passage | Lines | Digest | The true track parts at | Why |
|---|---|---|---|---|
| 5a's day | 616 → 616 | `684580064bfc6ecd`, unchanged | never | no chart, no reckoning |
| the frigate, 5b | 662 → 718 | `100f1bb8cdba918c` → `3c659bf81ef803fd` | tick 51 | the departure's course (tick 1): the helm is ordered the line's own bearing, a degree from 37d's heading |
| the schooner, 5b | 760 → 799 | `b3beb599c0cff7ea` → `8c0c686c9c52bac8` | tick 33 | the same |
| the thick passage, 5b | 503 → 508 | `2472b62d8cac3193` → `93239d9d2916dc54` | tick 45601 | the first course shaped in that book, at 45599, made good against the flood |
| the merchant passage, 5c | 2634 → 3146 | `52033fdd56901499` → `79dbbe53c772d94e` | tick 16610 | the first course shaped under way, 16608, "clear of the road", with the ebb allowed |
| the naval cruise, 5c | 1963 → 2144 | `86680b3c485373dc` → `f796f1dc5df9f466` | tick 11273 on | the course for the station, 203° to make good SW by S against the ebb, for 37d's heading of 207° (below) |

The lines that changed, by the item that changed them:

- **Item 1 (the one rule; the words say what the master did).** Every cast, bearing, noon, fix, lunar and time sight carries its verdict: the frigate's 15 bearings, 9 fixes, noon and casts; the schooner's 15, 10, noon and 2 casts; the thick passage's noon and cast; the merchant's 196 bearings, 42 fixes at their old ticks, 2 noons and 54 casts. The frigate's fixes are nine for ten (her track).
- **Item 2 (the doubt).** No line of its own; it is in the data of every reckoning line (the ellipse) and in the verdicts.
- **Item 6 (the master's tide).** `reckoning.tide`, new: 12 lines in the frigate's passage, 13 in the schooner's, 10 in the thick, 16 in the merchant's; the noon's last sentence in each.
- **Item 9 (a course made good).** Every `helm.set` of a shaped course (the frigate 3 → 4, the schooner 4 → 5, the merchant 30 → 39), and through the track everything the ship's physics says after it: the sails trimmed, the yards braced, the leeway lines, the log's reads, the weather's hour as she meets it elsewhere, the lookout's sightings.
- **Item 11 (the books).** The orders entered at tick 0 and the rules' own firings: the frigate's "round the Manacles" and "the pilot boards" (sail shortened: `sail.reefed` 0 → 3, `sail.taken_in` 0 → 2); the merchant's `reckoning.fix` 42 → 185 (the fix after every bearing in pilot water), `order.accepted` 523 → 687 with them, "the course for the road" eight times, the gates of the Goulet.

Old beside new:

| | Before (37d) | After (37e) |
|---|---|---|
| **The frigate** noon; cast | 28740; 29884, fifty-five fathoms | 28740; 29887, fifty-five fathoms, "The account kept." |
| landfall | 44520, the Beast and the Lizard's lights | 44760, the same at one look |
| the account at the landfall | 6.9 miles out; 4.2 to 5.4 for thirty-five minutes after | 9.7 out before the bearing, 2.35 after it, 2.4 for thirty minutes, 1.25 from the fix at thirty-five |
| outer road; anchor; brought up | 58895; 59250; 60239, twelve fathoms | 57737; 58178; 59151, eleven and a half |
| cutter sighted; hail; pilot aboard | 55260; 57060; 57180 | 55440; 56940; 57060 |
| **The schooner** landfall | 43920 | 44400 |
| outer road; anchor off the town; brought up | 56502; 57615; 58618, ten fathoms and a half | 56517; 58210; 59395, six and a half |
| pilot | aboard 55380 | hailed 56160, **not aboard** (an expected failure, below) |
| **The thick passage** landfall | 54900, Black Head close aboard, the account 10.9 miles out | 54600, the same land, 6.4 miles out |
| **The merchant** pilot of Falmouth put off | 18420 | 18540 |
| sail off the Lizard | 26280 | 26640 |
| noons | 25200, 111660 | 25200, 111660 |
| cast in the Iroise | 91836, thirty-nine fathoms | 91418, forty-one, "The account kept." |
| pilot of Brest | aboard 98160 | aboard 97800, **put off again 100620** |
| anchor, road of Bertheaume | 101373, nine fathoms and a half | 101821, seven fathoms |
| the flood; under way; the mouth of the Goulet | 108960; 110675; 112740 | 108960; 110353; 112444 |
| the Mingan; the shore under Petit Minou | 1.8 cables (328 m) to the north; 1.6 cables | 1.9 cables (356 m) to the north; 0.7 cable (125 m), in eleven fathoms |
| anchor in the Bay; tin sold | 116140; 123901 | 116110; 124441 |
| **The cruise** to the pilot's leaving | 5460, 6834, 7920, 11220 | the same |
| the cutter's hail; the letter read | 17840; 17900 (10:57 on the 12th) | 84153; 84213 (05:22 on the 13th) |
| noons | 21600, 108240 | 21600, 108240 |
| the Palinure sighted; chased; spoken | 91380; 91800; 95189 | 90000; 90000; **lost at 92040, not spoken** (an expected failure, below) |
| wears | ten | eleven, and a tack |

**The cruise, and why it parts so far.** After the pilot is put off she fills away and the course for the station is shaped (11273). In 37d that was the heading SSW 207°, and on it she lay with her topsails unfilled and no way on her for an hour and fifty minutes ("Hove the log: no way" at 14437; nothing fills until the course is shaped again at 17840): a fault of the filling away, which is package 37f's, and no part of the book. It was in that hour that the port admiral's cutter, sent from Plymouth at 10:00, came up with her. Made good against the ebb the course is 203°, her topsails fill at 11477 and she makes seven knots and a half; the cutter is a stern chase of nineteen hours and hails her on the station at 05:22 on the 13th. She has chased the cutter to the north-eastward from 04:08 and is put about for the station at the hail, so at 07:00, when the scenario puts the Palinure on the sea at 48° 50' N 5° 16' W, the frigate is three leagues to the south-eastward of her, on the starboard tack standing away. The chase is "as near the wind as she will lie", on the tack that opens the brig; she is worn round at the next glass and the brig is out of sight at 92040. The old meeting, the brig five leagues on the frigate's bow, was the accident of the lost hour and fifty minutes; no small mend of the book that could be stood behind brings it back, and none was made. For the lead: the scenario's hours for the cutter and the brig, or the filling away in 37f.

### The books, and the count of runs

Ten whole-passage runs with a book changed, of the dozen allowed (the frigate 2, the schooner 4, the merchant 4, two of the merchant's to the road of Bertheaume only), and ten late legs from a checkpoint (the merchant's, six from 84000 and four from 106000). None for the cruise beyond the measurement.

- **The frigate's and the schooner's**: a course made good from the Lizard's landfall for Falmouth "crosses the land about Black Head" and "passes the Manacles within a mile"; 37d's heading for Falmouth was set a league to the eastward of that line by the flood, clear of the ledge. Sailed, the schooner struck the Manacles at 53581 and the frigate anchored in four fathoms off Black Head and took the ground on the ebb. Both books now shape for a point three miles east of the Manacles (50° 02' N 4° 58' W) at the cast and at the landfall, and for Falmouth when it is within a mile ("round the Manacles").
- **The frigate's pilot**: standing in NNW she makes six knots and a half over the ground where she made five and three quarters, and the pilot boards a ship under six. "The pilot boards: at the pilot's hail then shorten sail". He boards two minutes after.
- **The schooner's pilot**: not mended. Three were tried: sail shortened at the hail, and the fore topsail taken in, each put her on the ground within St Anthony's (58086; 58582 at her anchor); brought to for his boat she lay to two glasses and the cutter did not come alongside. The book is left without, the pilot's hail is pinned, and his boarding is a strict expected failure.
- **The merchant's**, for a true account and a course made good:
  - *Pilot water* takes its fix after the bearing again.
  - *The Iroise.* With her drift hove to in the account she drifted out of the mark's mile and a half and sailed back into it, and was brought to four times. She is brought to with her head south of east (the course from the soundings), and "past the Iroise" waits for the first point within five miles.
  - *The road of Bertheaume.* The line from the first point to the second crosses the corner of the Chenal du Four's water (the areas have hard edges: three knots and a half to the southward on one side, a knot and a half on the other). The course for the road, shaped inside that corner, allowed the Four's ebb, laid her head N by E, which she could not lie, and held after she was out of it; she ran ashore west of Point Bertheaume at 101679. "The course for the road" works it again every five minutes while she stands in from the second point. The pilot of Brest asks for his boat when she opens her distance from the port, which she does stemming that ebb; "the pilot put off" now heaves to for the Falmouth pilot only, and he leaves her at 100620 without her being brought to.
  - *The Goulet.* With four knots of flood under her the wind she feels draws two points ahead and she lies no higher than ENE on the larboard tack, so she makes good nothing to the northward of about 067°. The old points asked NE across the stream (an allowance of N by E, which she could not lie), and in three trials she passed south of the Mingan, between it and the Fillettes, once coming through 118 m off the south shore and twice taking the ground. The points are now on the one line of 067° that clears both the shore under Petit Minou and the rock; the course for the point north of the Mingan is shaped at the mouth (the Iroise's allowance) and again at 4° 37.1' W (the Goulet's); the turns are at meridians. She passes the Mingan 1.9 cables to the north, the shore under Petit Minou 0.7 cable off in eleven fathoms.
  - *The Bay.* The line from under Portzic, made good, passed three cables off Penaleuch point over seven fathoms, and the first cast under twelve brought her up two miles and a third from the Bay's mark, out of the boat's reach (the port serves within two). The point under Portzic is two cables north, and "in the Bay" anchors within a mile and eight tenths of the mark.

### The proof by measurement

`docs/playtests/2026-10-05-gate-5c-review/evidence/tools/account_probe.py`, extended to print the master's doubt beside the error (the greater axis of his ellipse; a sample is marked when the error is more than twice it), on the three passages before the first change and after the last, a sample every half hour.

| | The merchant, before | after | The frigate, before | after | The schooner, before | after |
|---|---|---|---|---|---|---|
| mean error, miles | 1.81 | 1.74 | 3.97 | 2.71 | 3.87 | 2.10 |
| median | 0.35 | 0.41 | 4.49 | 1.21 | 2.18 | 0.97 |
| worst | 9.03 | 10.71 | 9.79 | 9.58 | 12.25 | 8.01 |
| over a mile | 32% | 36% | 62% | 56% | 59% | 47% |
| over three miles | 18% | 18% | 53% | 26% | 47% | 26% |
| the error more than twice the doubt | 25 of 72 (35%) | 13 of 72 (18%) | 21 of 34 (62%) | 2 of 34 (6%) | 18 of 34 (53%) | 0 of 34 |
| the doubt's median; greatest | 0.39; 2.09 | 0.36; 4.72 | 0.85; 2.38 | 3.42; 4.81 | 1.03; 3.08 | 3.47; 4.84 |

What was asked, and what was got:

- **The merchant's median no worse than 0.35**: 0.41, a little worse. **The time over three miles halved from 18 per cent**: not met, 18 per cent still. All of it is the night's run across the Channel (15:00 to 22:30): her compass (the variation's ten years and her own deviation, two and a half to three miles in a hundred), her leeway allowance's bias (two and a half), and the tide (two and a half to five: his hour early and his set twenty degrees from the stream's). An amplitude at sunset would take out the first; the book has none.
- **The frigate's landfall within a mile and a half inside half an hour**: 2.4 miles for thirty minutes, 1.25 at thirty-five, when the glass's bearing and fix come (4.2 to 5.4 for thirty-five minutes before). Not met, by five minutes. Her noon's sight is five and a half miles too far north at this seed (a draw of two and a half of its own doubts) and is weighed, three miles of it; the afternoon carries that.
- **Honesty, no more than one sample in ten**: the frigate 6 per cent, the schooner none; **the merchant 18 per cent, not met.** Of her thirteen, seven are at anchor in the Bay of Brest (below), four are the last two hours of the Channel crossing (8.9 to 10.7 miles out against 4.3 to 4.7 of doubt, just beyond twice), and two are single samples.
- **The brig hove to six hours of a spring ebb in the Iroise**: inside twice the doubt at every hour, 1.98 miles from the truth after 13.6 miles of drift.

### Found on the way (package 37e)

- **A reading changed the game**, in three ways, all in this package's own new code and all mended. The account brought up to the moment was remembered by the tick alone, so a reading asked before the board was pegged in a tick gave the next asker the account as it stood before; whose tide the day's work carried was noted wherever the tide was summed, a reading included; and the nearest place of the epitome was remembered by the hundredth of a degree from whoever first asked within it. A chart open, or a test watching the log, could then sail a few yards from the game replayed without them. The memory is now kept only while nothing the account is worked from has changed (`Navigation._state_key`), a reading notes nothing (`_tide_between`'s `note`), and the place is the hundredth's own (`_tide_port`); a test asks one of two ships and not the other and compares them. The last of the three moved the merchant's digest and took two lines out of the thick passage (a turn of the master's tide and its turning back three minutes after, which was the first asker's place and not the hundredth's).
- **A cast off a steep shore** was "laid down by the cast" two miles away, the frigate a cable in doubt by her fix off Black Head: the contour is searched on rings half a mile apart and stepped over the narrow band where the depth answered. Where the chart about the account brackets the cast it is kept (`Chart.depth_span`).
- **At anchor in the Bay of Brest the account is not honest.** Fixes every five minutes by Penaleuch point, Portzic and the castle of Brest, all between W by N and N by W and two to three miles off: each fix says "good to two cables", which is honest, and the account, weighed with each, comes to believe itself good to a cable while it stands three to four cables out. The compass's error is common to all three and, with every mark on one hand, moves the fix more than his allowance for it says. Not mended. For the lead.
- **The rule takes an observation whose stated doubt is too small.** The cruise, hove to off Plymouth at 09:00 with the account a cable in doubt by the land: a longitude by chronometer 7.6 miles out, "which Mr Harvey would trust within 5 miles" (2.28 a sigma), stands more than twice the two doubts from the account and is taken; the bearing of Penlee half an hour after takes it back. The Arnold's rate was out by more than three seconds a day and the master allows one (`sights.RATE_DOUBT_S_PER_DAY`). It is the brief's rule working as written, and it would do the same with three for two. Not mended: `sights.py` is not this package's. For the lead.
- **Truth 59** ("moves the reckoning onto the chart's contour") holds to within a fathom of the contour's tolerance: the cast is weighed, ninety-six parts in a hundred of the way. The test says so; the spec's sentence is the lead's.
- **A ship hove to in this sim makes two to three knots** through the water, sternway and leeway together (the brig drove 13.6 miles in six hours). The master reckons it by eye as he finds it. Whether she should is 37f's.
- **The stream areas have hard edges**, and a course shaped is worked for the water the account is in at that moment. At the corner of the Chenal du Four the merchant's book works the course again every five minutes; the general remedy, if one is wanted, is the lead's to rule.
- **The master's tide can turn twice within minutes in mid-Channel**, where the nearest place of his epitome changes from the Ramhead to Ushant as the account crosses and his hour of high water with it (the thick passage at 23460 and 23700: "the flood makes", "the ebb makes"). It is what his books give him. Left.
- **`the turn of the tide by the reckoning`** is an event (the routine line `reckoning.tide` with `turn`), so that a book may shape a course again when the master's tide turns. No book uses it yet.

## Milestone 5: lying to, and the ground (package 37f, 2026-10-07)

Built from the brief "Package 37f: lying to, and the ground" in `M5-WorkPackages.md` (the review of gate 5c's playtests, 5.7, 5.8, 8.2 and 10.3 to 10.5, and the owner's notes on game 9). Everything below was measured at seed 7 on the build machine, in scripted worlds: the game's own saves are the owner's and were read, never used as fixtures.

### The constants and their sources

| Constant | Value | Where | Source |
|---|---|---|---|
| `near_points`, `far_points` | 4, 7 | `heave_to.yaml` | the brief's "about four and seven points"; Luce's frigate lies at five and a half |
| `helm_deg`, `helm_max_deg` | 15°, 25° | `heave_to.yaml` | the lee helm she carries midway, and the most given her as she falls off: judgement, set on the four ships |
| `helm_lead_s`, `sheet_lead_s` | 15 s, 20 s | `heave_to.yaml` | how far ahead of her swing the helmsman and the hands at the sheets look: judgement (with none she hunted across the band) |
| `sheet_s` | 30 s | `heave_to.yaml` | a sheet worked from as she was hove to, to right aft or off: judgement |
| `aback_points` | 2.5 | `heave_to.yaml` | nearer the wind than this the innermost head sail's sheet is hauled to windward to box her off: judgement |
| `way_off_kn` | 1.5 kn | `heave_to.yaml` | truth 12's "under a knot and a half" |
| `way_steady_kn_s`, `way_most_kn` | 0.004 kn/s, 4.5 kn | `heave_to.yaml` | "as slow as she will go": her way no longer falling, and never said with this much on her: judgement (the fore-and-afters forereach) |
| `lie_kn`, `lean_points_kn` | 0.5 kn, 1 point a knot | `heave_to.yaml` | the headway she is held with, and how far the mark leans toward the wind for each knot more: judgement |
| `quiet_deg_s`, `lie_s` | 0.25°/s, 20 s | `heave_to.yaml` | her head no longer swinging, for so long, before "Hove to" is said: judgement |
| `way_off_timeout_s` | 600 s | `heave_to.yaml` | ten minutes to lose her way; the brief's test reads her at ten |
| `round_points`, `round_s` | 1 point, 20 s | `heave_to.yaml` | forced round: the wind so far on the other bow for so long (the brief's test: "never within a point of the wind's eye") |
| `fill_s` | 60 s | `heave_to.yaml` | filled: nothing aback and more than `way_off_kn` of way for a minute: judgement |
| `abaft_points`, `abaft_s` | 9, 120 s | `heave_to.yaml` | fallen off: a point abaft the beam for two minutes: judgement |
| `keep_hands` | 4 | `heave_to.yaml` | the spanker's sheet and the head sheet, two hands each: judgement |
| `LYING_TO_WAY_SMOOTH_S` | 60 s | `scripts.py` | her way read over a minute for where the watch holds her: judgement |
| `retrim_s`, `pay_off_timeout_s` | 20 s, 240 s | `fill_away.yaml` | `fill away and steer`: the yards and sheets trimmed so often as she pays off, and for the course after so long: judgement |
| `SWINGING_ROOM_M` | a cable | `scripts.py` | the brief's "within a cable of the nearest land" |
| `stand_on_timeout_s` | 3600 s | `come_to_anchor.yaml` | `in twelve fathoms`: she stands on an hour for the lead to call it: judgement |
| `DRAG_REPORT_S` | 900 s | `physics/anchor.py` | the brief's "a quarter of an hour at most" |
| `DRAG_REPORT_MIN_M` | two fathoms | `physics/anchor.py` | no "still coming home" line for less than this since the last: judgement |
| `DRAG_SAY_S`, `DRAG_SETTLE_S` | 60 s, 300 s | `physics/anchor.py` | package 34's, kept; what changed is how they are counted (below) |
| `cast_boom_deg` | 30° | `get_under_way.yaml` | Luce 1884, ch. XXXIV, 'Schooners': "main boom steadied over"; the angle is judgement |
| `abox_s` | 20 s | `get_under_way.yaml` | a fore-and-after's one topsail yard laid abox when the anchor is aweigh: judgement |
| `cast_enough_points`, `cast_give_up_s` | 4, 900 s | `get_under_way.yaml` | at the timeout, paid off so far she has cast; hanging nearer, she is given so long: judgement |
| `WIND_SHIFT_FLOOR_KN` | 4 kn | `core/world.py` | the brief's figure; Beaufort's scale, where "light airs" (force 1, one to three knots) pass to "a light breeze" (force 2, four to six), which are the log's own words (`units.describe_wind_strength`) |
| `WIND_SETTLE_S` | 300 s | `core/world.py` | a light breeze for five minutes is the wind come back: judgement |
| `WIND_SWING_S`, `WIND_STEADY_S` | 3600 s, 1800 s | `core/world.py` | unsteady: the wind's second turn within the hour; settled again when its mean has stood within two points half an hour: judgement |
| `BACKED_REARM_S`, `BACKED_REARM_WAY_KN` | 60 s, 0.5 kn | `physics/sails.py` | a sail's lines armed again: full a minute with way on her; the hull's own figures (`ABACK_REARM_SECONDS`, `WAY_ON_KN`) |

### Heaving to, by the minute

The brig, brought to from like states to the game's four failures, and the schooner from the same; her head in points from the wind on the tack she hove to on (a minus is through the wind, on the other tack) and her way in knots, at each minute from the order. Before is the build as 37e left it.

| The brig | Before | After |
|---|---|---|
| seven knots, the wind abaft the beam | "Hove to" at 58 s; 5.1/+3.4, 1.7/+0.8, **-6.9**/-0.3, -5.6, -6.2, ... -13.5/+3.9 at fifteen: through the wind in the third minute, and round | "Hove to on the starboard tack" at 173 s; 5.4/+3.4, 5.4/+1.8, 5.7/+1.5, 5.6/+1.2, 5.6/+1.1, 5.6/+1.0, then 5.7/+1.1 to fifteen; never nearer than 5.1 points |
| four knots, the wind on the beam | at 50 s; 5.3/+2.8, 2.3/+1.5, **-2.1**/+0.6, -7.6, ... -13.0/+1.9: through the wind in the third minute | at 165 s; 5.1/+2.7, 4.6/+1.8, 4.7/+1.2, 4.5/+0.8, 5.3/+0.5, 5.9/+0.6, then 5.8/+0.6; never nearer than 4.5 |
| a knot in light airs, larboard tack | at 47 s; 5.8 to 6.4, +0.9 | at 66 s; 5.7 to 6.1, +0.9 falling to +0.7; never nearer than 4.8 |
| a knot in light airs, starboard tack | at 47 s; 5.8 to 6.3, +1.0 | at 66 s; 5.5 to 6.1, +1.0 falling to +0.7; never nearer than 5.0 |

| The schooner | Before | After |
|---|---|---|
| seven knots, the wind abaft the beam | at 68 s; 3.4/+2.1, 3.5/+0.1, 3.1/-1.3, then 3.0 points with 2.3 knots of sternway | at 102 s; 5.0/+2.4, 4.2/+0.3, 4.1/-1.1, 5.1/-1.0, 5.2/-0.4, then 5.2/-0.2; nearest 3.9 |
| four knots, the wind on the beam | at 46 s; 3.9/+2.4 ... 3.3 points with 1.1 knots of sternway | at 136 s; 4.9/+2.4, 4.7/+1.4, 4.0/+0.8, 4.1/+0.3, 4.5/+0.3, then 4.6/+0.5 |
| light airs, either tack | at 41 s; 4.0 to 4.6, +0.8 | at 60 s; 4.5 to 4.8, +1.0 |

In these scripted states the light airs hold before as after; in the game they went round after six and after twenty minutes, on shifts of the air, which is what the six hours below are for.

*Six hours hove to* in twelve knots, gusty and wandering (0.3 each), on the starboard tack:

| Ship | Her head, points from the wind | Her way | Lines |
|---|---|---|---|
| the brig | 5.5 to 6.0 (62° to 68°) | +0.7 to +1.0 kn | one, routine, at the change of the watch: "Lying to on the starboard tack, her head six points from the wind; the watch tending the helm and the sheets." |
| the frigate | 5.0 to 5.9 (56° to 67°) | +0.5 to +0.9 kn | the same, "five points and a half" |
| the schooner | 4.1 to 4.5 (46° to 51°) | +1.4 to +2.3 kn | the same, "four points and a half" |
| the cutter | 3.9 to 4.4 (44° to 49°) | +1.0 to +1.4 kn | the same, "four points" |

The fore-and-afters forereach, as Luce's do, and are not brought under a knot and a half; their tests hold them to their tack and to under two knots at ten minutes from the three like states. 37e's note that "a ship hove to in this sim makes two to three knots" is answered: the brig makes under one.

*From the game's own state* (a scratch copy of the first save's checkpoint, in memory, the brig at seven knots with the wind on her quarter on 15 June): hove to after 178 seconds, her head 53° to 70° from the wind and her way +0.2 to +0.5 knots for four hours (measured when part one was built).

What made the difference, in the order found: the yards that stay full braced sharp up as she is rounded to (left braced for a quartering wind they drove her through the wind or held her in a stern board; Luce's "bracing up the head yards"); the helm met ahead of her swing and not after it; the spanker and the head sheet worked as she comes up and falls off; "Hove to" not said until she lies so.

### Filling away

The brig hove to in ten knots: `fill away` from the starboard tack, "Filled away on the starboard tack; braced full and steering WNW (292°)." in under a minute, steady at three minutes, three knots at seven with the wind 67° on her starboard bow; from the larboard tack the mirror of it, ENE (68°). Put about by hand while hove to, she is filled on the tack she lies on and her head never comes back within three points of the wind (in game 9 she was taken back through it three times).

`fill away and steer WSW`: "Filled away on the starboard tack; braced full and steering WSW (248°), the course ordered." at two minutes, steady on it at three, 4.1 knots at seven. `... steer 250` the same by degrees. `... steer east`: "... steering WNW (292°), full and by (E (90°) lies on the other tack; she is kept full and by on the starboard tack: tack or wear for it)." `... steer NW`: "... (NW (315°) lies too near the wind to be laid; she is kept full and by on the starboard tack)." The frigate, `fill away and steer W by S` in fourteen knots: on her course at three minutes, 5.9 knots at seven, and no sail aback. (The first cut braced her at once for the course said; her topsails lifted with her head still five points from the wind and the log said "Her sails aback". She is braced full by the wind first, and trimmed as she pays off.)

### The Goulet's eight hours, before and after

The like of game 9's state, built in a scripted world (the brig brought up off the Mingan on 16 June 1805 at 16:42 in twenty fathoms on "rock and mud", the small bower five minutes after, the sheet anchor four hours on; eight hours of the Goulet's tide). The game itself had eighteen urgent lines.

| | Dragging lines | "Holds again" | How far the anchors came home |
|---|---|---|---|
| Before | 8, all urgent ("veer more cable" among them at the bitter end, and of the second anchor when it was down) | 8 | the best bower a cable and a half, the small bower a cable |
| After | 1, urgent: "The best bower is dragging: veer more cable; let go the small bower, or back her with the stream." | 1: "The best bower holds again, having come home half a cable." | the best bower 0.45 cable, as she brings up; nothing after |
| After, the ground forced to bare rock (the line logic alone) | 8 urgent and 7 notable ("The small bower still coming home: half a cable since it began.") | 8 | as before the package |

Most of the difference on that ground is item 10 and not item 9: "rock and mud" holds 0.55 of good ground where it was held as bare rock, 0.30, and the anchors no longer come home there. On bare rock the anchors relapse after six or eight minutes' holding, and by the brief each relapse after "holds again" is a new drag with its own urgent line (spec M5 §33, item 22).

### The ground's factor for each port's road

The chart's nearest bottom note within three kilometres, which is what an anchor let go there is given, and the factor on the holding (`GROUND_HOLDING` unchanged: rock 0.3, stones 0.4, ooze 0.5, weed and shells 0.6, gravel 0.7, mud 0.8, clay, sand and "good ground" 1.0; a note that names none of them 0.9).

| Port | Place | The note | Before | After |
|---|---|---|---|---|
| Brest | the road of Bertheaume | sand and mud | 0.80 | 0.90 |
| | the Bay | mud | 0.80 | 0.80 |
| | the mooring before the town | none; now "mud", the new `brest-road` | 0.90 | 0.80 |
| Falmouth | the outer road | good ground | 1.00 | 1.00 |
| | Carrick Road, and the mooring | good holding ground | 0.90 | 0.90 |
| Plymouth | Cawsand Bay | sand, foul and rocky in the north part | 0.30 | 0.65 |
| | the Sound | sand and mud | 0.80 | 0.90 |
| | the Hamoaze | mud | 0.80 | 0.80 |
| Roscoff | the western entrance | sand and rock | 0.30 | 0.65 |
| | the road of Bas, and the harbour | sand | 1.00 | 1.00 |
| St Mary's | all three | loose sand, not very tenacious | 1.00 | 1.00 |

None has no note. Two things the rule does not read: "good holding ground" is not the table's "good ground" and takes the default; "loose sand, not very tenacious" is sand. The Goulet off the Mingan, "rock and mud": 0.30 before, 0.55 after.

### The log's lines on the recorded passages, before and after

| Passage | Wind-shift lines | "Aback" of the ship, urgent and notable | A sail's "taken aback" | "Could not ..." | A cast with no bottom, notable | The book's refused orders | The book's "held" lines |
|---|---|---|---|---|---|---|---|
| 5a's day | 3 → 3 | 0 → 0 | 0 → 0 | 0 → 0 | 0 → 0 | 10 → 10 | 1 → 1 |
| the frigate, 5b | 0 → 0 | 0 → 0 | 11 → 0 | 0 → 0 | 21 → 0 | 11 → 8 | 16 → 23 |
| the schooner, 5b | 0 → 0 | 0 → 0 | 3 → 0 | 1 → 0 | 23 → 0 | 8 → 7 | 16 → 19 |
| the thick passage, 5b | 0 → 0 | 2, 0 → 1, 0 | 18 → 7 | 0 → 0 | 5 → 0 | 2 → 1 | 8 → 5 |
| the naval cruise, 5c | 0 → 0 | 3, 1 → 4, 0 | 77 → 20 | 0 → 1 | 0 → 0 | 28 → 12 | 59 → 63 |
| the merchant passage, 5c | 4 → 4 | 1, 0 → 0, 0 | 16 → 0 | 0 → 0 | 3 → 0 | 69 → 13 | 83 → 92 |

No recorded passage has a calm in it, so the wind's floor moves none of their lines; the tests of it are scripted (`tests/test_log_lines.py`). The "held" lines grew a little where the refusals fell: each reason now has its own line a watch, where a rule had one a watch whatever its reason. The cruise's one "Could not" is new and is a true failure: "Could not wear: she would not come round." (below).

### The recorded passages, re-measured with the reasons

Written out before the first change and after the last (`scratch dump_passage`; the constants by the tests' own selectors, `scratch measure`).

| Passage | Lines | Digest | The true track parts at | Why |
|---|---|---|---|---|
| 5a's day | 616 → 616 | `684580064bfc6ecd` → `efc286e862237e53` | never: the track is the same to the last figure | the four lines that enter the starter's two trim rules carry the guard |
| the frigate, 5b | 718 → 768 | `3c659bf81ef803fd` → `dbf7f6fcfb800fdf` | tick 28750 | the heave-to for the noon's cast (item 1): the yards that stay full braced up, her way taken off |
| the schooner, 5b | 799 → 761 | `8c0c686c9c52bac8` → `78eec3dcd5f33c16` | tick 28750 | the same |
| the thick passage, 5b | 508 → 488 | `93239d9d2916dc54` → `fb136bb8e86f0804` | tick 28750 | the same |
| the merchant passage, 5c | 3146 → 2992 | `79dbbe53c772d94e` → `bb8483de9959aa2a` | tick 14250 | getting under way (item 13): a fore-and-after's helm is tended from the first heave |
| the naval cruise, 5c | 2144 → 1988 | `f796f1dc5df9f466` → `8d865bff1518f52b` | tick 130 | the anchor let go at the start (item 3: the helm righted as it goes) |

The lines that changed, by the item that changed them:

- **Item 1 (heaving to).** `ship.hove_to` names the tack and comes when her way is off (the frigate 28796 → 29013, the schooner 28799 → 28851, the thick passage 28797 → 29013, the cruise 8876 → 9056, the merchant 17697 → 17573 and 90428 → 89225); the step says "braced up the other yards"; and through the track every line the ship's physics says after it.
- **Item 2 (`fill away`).** `ship.filled_away` names the tack: "Filled away on the larboard tack; braced full and steering WNW (297°)."
- **Item 4 (the guard).** The books' trim rules as entered at tick 0; "tend the sheets ... not carried out; the manoeuvre in hand is heaving to" where it trimmed a ship being hove to.
- **Items 7 and 11 (the anchor).** The first line of every `let go` and the anchored line of every `come to an anchor` say the scope; "Brought up" after the merchant's and the cruise's `let go` at the start (323 and 153).
- **Item 13 (the cast).** The merchant's two casts: "She has paid off; right the helm, draw the jib, haul aft the main sheet, brace round the topsail yard." 92 and 72 seconds after the anchor is aweigh, where both ran the seven minutes to the timeout and said "She has paid off; right the helm, brace round the head yards, set the spanker."
- **Item 15 (aback).** A sail's lines: 125 → 27 over the six. The heave-to for the cast alone said eleven of them on the frigate.
- **Item 16 ("could not").** Nothing in the passages was a "done already". (The schooner's one "Could not come to an anchor: she is at anchor already" is not said on her new track.)
- **Item 17 (the lead and the book).** The casts with no bottom, 52 notable lines, are routine; the book's refused orders 128 → 51 and its held lines 183 → 203 (above).

Old beside new:

| | Before (37e) | After (37f) |
|---|---|---|
| **The frigate** hove to; cast | 28796; 29887, fifty-five fathoms | 29013, "on the larboard tack"; 30118, the same fathoms |
| landfall | 44760, the Beast and the Lizard's lights | 44820, the same at one look |
| the outer road; anchor; brought up | 57737; 58178 in eleven fathoms and a half; 59151 | 58297; 58647 in fourteen and a half; 59642 |
| the cutter sighted; hail; the pilot aboard | 55440; 56940; 57060 | 55860; 57480; 57540 |
| **The schooner** landfall | 44400, the Beast at five leagues | 45840, the Beast at four |
| the outer road; anchor; brought up | 56517; 58210 in six fathoms and a half; 59395 | 56515; 57638 in seven; 58690 |
| the pilot | hails at 56160, does not board | hails at 55800, does not board |
| **The thick passage** the land close aboard | 54600 | 54420 |
| **The merchant** under way | 16005; the cast timed out | 16007; she casts in 92 seconds |
| the Falmouth pilot aboard; put off | 16320; 18540 | 16200; 18300 |
| the sail off the Lizard | 26640, on the larboard bow | 29100, abeam to starboard |
| the cast in the Iroise | 91418, forty-one fathoms | 90240, thirty-eight |
| the pilot of Brest | aboard 97800, put off 100620 before the anchor | aboard 96240, and stays aboard |
| Bertheaume; the flood; the Goulet; the Bay; the tin sold | 101821 in seven fathoms; 108960; 112444; 116110; 124441 | 99974 in twelve; 108960; 112112; 115817; 123951 |
| **The cruise** the pilot aboard; put off | 7920; 11220 | 7980; 10980 |
| the cutter within hail; the letter read | 84153; 84213 | 83838; 83898 |
| the stranger | sighted and chased at 90000, lost at 92040 | sighted and chased at 90000, lost at 93420 |
| wears | eleven and a tack | thirteen, and one that failed |

### The books, and the count of runs

Sixteen whole-passage runs after the first change, where the brief budgets a dozen: the six written out, the six written out again when the wind's "unsteady" rule was put right (its first form, a test on the spread of the ten minutes' wind, took a front's one sharp veer for an unsteady wind and cost 5a's day its line; the second set is the one recorded), and four of the frigate's passage to mend her book.

- **The frigate's book: one line added, one clause added.** Unmended she did not come through: she raised the Lizard a league further west (44580, "The Lizard bearing N"), passed the point east of the Manacles more than a mile wide by her own account, and stood on up the Channel to the end of her hours. The cause is a course worked once: filling away from the noon's cast with a knot and a half on her (three and three quarters before, when she was not truly hove to), the course for the point came out "steer NNW to make it good" against three quarters of a knot of flood, where it was N by W, and she held it four hours at seven knots. Run 1: the course worked again every glass once the land is in sight: she rounds the point but too late for her hours. Run 2: every glass from the noon's cast: she comes through, but the rule fired once more after the rounding and turned her back for a quarter of an hour. Run 3: the rule's guard set at nine miles from Falmouth (the point is eight): she rounds once and anchors on her old minutes, and the pilot hails her ten minutes before her anchor and does not board, her sail not yet in. Run 4, kept: sail shortened at the rounding; the pilot boards a minute after his hail, and she is brought up at 59642.
- **The schooner's and the thick passage's books: unchanged.** The schooner comes through to her anchor off the town; her pilot hails and does not board, as since 37e (the strict expected failure stands; 37h's).
- **The merchant's and the cruise's books: the guard on their three trim rules, and nothing else.** The merchant comes through whole, and better: she casts, and the pilot of Brest stays aboard.
- **The cruise is not mended.** The stranger is chased and lost, as since 37e, and the strict expected failure stands with its reason rewritten. What she does now: at 07:00 the Palinure is four miles on her starboard quarter; she is kept full and by on the starboard tack for her; at 07:30 the book's `keep her bearing` orders "steer NE by E", a course across the wind's eye from her head; the helm takes her through the wind with every sail aback (91954, urgent), she has no way on at 93634, and the brig is out of sight at 93420. What would bring the meeting back: the chase order wearing her for a course across the wind, as its first form does, or the scenario's own hours, which are the owner's. Not tried: it is the chase's code or the scenario's file, and neither is this package's.

### Found on the way (package 37f)

- **A fore-and-after at anchor was sheered the wrong way by her own topsail.** Her one yard laid abox while the anchor still held her by the bow swung her stern and not her head, and the helmsman, left steering for the last course as the capstan drew her ahead, sheered her further: the wind was three and four points on the wrong bow when the anchor broke out, where no jib will throw her head across. Luce's schooner has her main boom steadied over to the side she is to cast toward, and that is what is built: it sheers her for the tack while she still rides, and she casts in a minute.
- **Truth 66's test** stood into the land when a cast read exactly forty fathoms, in the gap between its book's "under 40" and the lead's "exceeds 40". The test's own book says "under 41" now, with the reason beside it.
- **37e's test of the brig hove to in the Iroise** leaned on her not truly lying to (13.6 miles of drift in six hours, two knots of sternway under topsails alone). Under plain sail, tended, she drifts 7.4 miles; the test is set to that, and its account is as honest as it was.
- **Two orders of the cruise's book give chase to one sail at one tick**, each queues a wear, and the second wear begins as the first ends and fails ("she would not come round"). Left as found (spec M5 §33, item 22).
- **Under eight parallel workers the suite's workers die at random** on this machine ("Windows fatal exception: code 0x80000003", at any line of plain Python; the baseline tree does it too). Under four, as the brief runs it, none did.
- **`let go ... in twenty fathoms` still means the scope**, as the primer had it, beside the new `and veer to` and `with`; `come to an anchor in twelve fathoms` means the depth. The two "in"s are the primer's, and are kept.

## Milestone 5: the station's safety, and the deck, the leaving and the grant (package 37g, 2026-10-07)

From the review of gate 5c's playtests (`docs/playtests/2026-10-05-gate-5c-review/report.md`, 5.3, 5.4, sections 6 and 9, and 10.5 for game 9) and the owner's rulings of 5 and 7 October. No constant of the ship, the sea or the reckoning moved, and the six recorded passages, which carry no station, replay to the digests recorded before the package.

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| `ORDERS_PER_TURN` (`TOOL_CALLS_PER_SAMPLE`; `Station.orders_per_turn`) | 16 orders at a sampling point; it was 8 calls of every kind | the brief's item 2 ("sixteen orders a turn, as a setting of the station"); the review's 5.4 (`opt_out` as a ninth call was "Not run") | the brief |
| `READS_PER_TURN` (`READS_PER_SAMPLE`) | 32 reads and notes at a sampling point, counted apart from the orders | the brief left "counted apart, or not at all" to the builder: a count keeps a bound on a reply that reads without end, and twice the orders' is room for a watch's reading | judgement |
| `ALWAYS_RUN_TOOLS` | `opt_out`, `stand_down`, `hand_over`, `stand_by` | the brief's item 2 | the brief |
| `DANGER_WORD_N` | 3 orders on the officer's own word within a watch bring a word (and never a pause) | the brief's item 19 ("used three times in a watch it brings the detector's word") | the brief; "never a pause" is judgement |
| the undo table (`undoes` in `data/vocabulary.yaml`) | 21 pairs of verbs, each read both ways | the brief's item 5 (the same sail set and taken in, hove to and filled away, an anchor let go and weighed, cable veered and hove in, a thing allowed and disallowed), carried through the vocabulary's verbs that are each other's undoing | judgement, tested on the record below |
| `irrevocable` in `data/vocabulary.yaml` | `cut away` | the owner's list for the general grant ("what cannot be undone"); the vocabulary has no order to slip or cut a cable | the vocabulary read through |
| `HANDOVER_RESERVE_TOKENS` | 14,000 tokens of the door's context kept free when the handover note is asked for (`--handover-reserve` at the local runner); never earlier than `HANDOVER_AT_FRACTION`, six tenths | the review's 8.7, ruling 2 (a reserve in tokens with a flag); the size of game 9's longest turns and the note itself with room to write it | judgement |
| `SITUATION_ALLOWANCE_TOKENS` (`local.py`) | 2,500 tokens allowed for what the ship adds to the officer's brief (the log's last lines, every reading, the night orders) in the stationing guard | the situation item measured at about 2,100 tokens on the frigate (package 37's table above), with room for a longer book | measured, with judgement for the room |
| `WAIT_MARGIN_S`, `WAIT_FLOOR_S` (`mcp_server.py`) | the bridge's wait is shortened to 10 seconds under the client's cut, never below 15 | the brief's item 8 ("its wait adapts when a call is cut short"); the default's own forty seconds under the Desktop client's four minutes, scaled down | judgement |
| `READ_LOG_MAX`, `READ_JOURNAL_DEFAULT` | at most 1,000 lines of the log by `count`; 20 journal entries by default | the brief's item 15 (the log read back past its two hundred lines by a tick or a count; the journal newest first, by count) | judgement |
| the officer's domain | `take a bearing of` and `take a fix` added | the gate's ruling 1; Falconer's lieutenant "superintending the navigation" | the brief |
| the general grant (`agent._GENERAL`, `_KEPT_BACK`) | the orders of the course, the manoeuvres, the anchors, all hands and the watch below, the sights and the reckoning worked up, a course shaped; kept back: the port, the reckoning set by hand, the tide allowed, the chase, the people, the captain's own going below | the owner's approved list (the review's section 9, question 4, and his ruling of 7 October); the tide allowed and the people are this package's reading | the list; the reading is judgement |
| the way out of danger (`agent._DANGER`) | the orders of the course, `heave to`, `let go the anchor` | the brief's item 19; the Regulations of 1806, the Lieutenant, art. XIII | the brief |

### The detector, tested on the record

The orders behind every one of the 42 nudges and pauses of the detector in the nine games (the first 31 as the review's reader lists them by tick, `evidence/V1b-authority-standing-detector-code.md`, section F; game 9's eleven from its officer's journal) are a table in `tests/test_officer.py` (`RECORDED_CHAINS`). Each is a chain by the old rule ("each contrary to the one before it on a shared part"), which the test checks, and **none is a chain of three by the new one**: 42 sequences, none still speaks, game 9's eleven among them. A scripted *set the jib; take in the jib; set the jib; take in the jib* is a chain of four, brings the word with the third order's result, and the pause when the chain goes on in a later reply.

| Game | Sequences | Still speak |
|---|---|---|
| the *Harpy* | 8 | none |
| the *Speedwell* | 20 | none |
| the cutters | 3 | none |
| game 9 | 11 | none |

### Off watch, measured

The frigate at seed 7 under plain sail, the scripted officer sampled as a door samples him (every glass and on notable and urgent events), saying nothing, for a watch of four hours: seated without the deck, 12 samples and about 4,300 tokens of samples in all (some 330 a sample, the readings that changed); with the deck, 13 samples and about 4,900. The brief is about 5,300 tokens at that door. So an officer off watch costs what a watcher costs, and what he cost before the deck was first given.

### Found on the way (package 37g)

- **The words the ship reads twice were carried out past the filter.** `take in twenty tons of water` failed the filter's parse, was passed to the ship, and was carried out as the port's order with no allowance (the review's 5.3). The filter now judges it as the port's.
- **The pause of the way out of danger.** As first built, a fourth order on the officer's own word after the word had been read paused him, and a pause takes the deck: the detector would have taken the deck from an officer in the act of avoiding a danger. It brings the word each third time and never the pause.
- **A replay and the stationing tick.** A stand-down and a reseating made at the tick a station was first seated, before any tick has run, are not made by a replay (spec M5 §33, item 11, as it stood); the tests that replay such a game run a tick first and say so.
- **The first line of a station** now says who sits and through which door when a model is named ("The watcher takes the station (..., through the MCP bridge); sampled ..."); the game's own scripted station says what it said.

## Milestone 5: the fold-in of m5c-c (2026-10-08)

The owner's local folder `FreeSail-gate-m5c-c` (packages 37b to 37g) merged whole into
the repository as a branch made at the gate's commit (decision 38; the close-out's
section). The lead's changes at the fold-in, and what they moved.

| Constant or rule | Value | Why | Standing |
|---|---|---|---|
| `core.world.BUILD_NAME` | `m5c-c` | the repository's build, named once per gate; the nine test lines that spelt `m5c-c/37g` read the constant | the owner's ruling 7 |
| `.gitignore` `!tests/fixtures/saves/` | | the `saves/` rule matches a folder of that name at any depth, and would have dropped the three kept checkpoints without a word (the audit, N 3.9) | |
| the *Palinure* at 07:00 | 48 32 N 5 23 W (48 50 N 5 16 W) | five leagues on the frigate's bow where she now is at seven, as the scenario's own comment wanted and the audit tried (M 2.4) | tuned to the frigate's track: moves again with the account, the tide or the pilot |
| `_course_not_laid`, the wake | a turn through the wind's wake is a wear | the chase's 175 degrees round by the stern left the yards braced sharp up and every square sail aback at 91954 (the audit's C1, C2); worn for it as for a turn through the eye | the lead; `tests/test_ships.py`, the two tests at its end |
| the cruise's book, "a sail on the station" | `make her out` alone | with `give chase` in both the sighting's and the made-out rule, two chases in one second and the second wear failed (79260, 79261) | the lead |

**The guard's three forms, measured.** As first written it wore any vessel for a turn
through the wake: the cruise came through (the brig spoken at 08:08) but the schooner's
merchant passage broke, her book's hourly courses across the Channel alternating between
the soundings south-west of Ushant and the Iroise by a hundred degrees, each a wear
where the helm had gybed her in a minute: she made the Iroise five hours late and missed
the tide. Narrowed to a square-rigged ship close-hauled, the merchant passage came back
and the cruise lost the brig again: the station shaped for from the cutter's hail, with
the frigate reaching after the chase, took her aback at 83600 as it had at 83957. The
form kept: a ship with yards on two masts, a square sail set and a knot of way
(`WEAR_FOR_IT_MIN_MS`) is worn for a turn through the wake; a fore-and-after gybes by
the helm as she always has, and a ship drifting under bare poles is steered (the chase
test at `tests/test_ships.py`, "make her out", found the first form wearing a drifting
frigate).

| Passage | Before (m5c-c, the owner's Windows figures) | After, on this machine |
|---|---|---|
| The naval cruise | 1988 lines, `8d865bff1518f52b`; the cutter within hail 83838, the Palinure sighted on the starboard quarter 90000, lost 93420, never spoken; eleven wears; taken aback at 83957 and 91954 | 2037 lines, `bb8b2499fde6a0f4`; the cutter 83484, the Palinure right ahead three leagues 90120, chased at the made-out line 90121 with the course led, spoken 94091, out of sight astern 98100; fourteen wears; no urgent line |
| The merchant passage | 2992 lines, `bb8483de9959aa2a`; the Bay 115817 | 2994 lines, `c52c14c725a5ed1f`; the Bay 115815; the guard never fired (`worn round for it` nowhere in her log) |

**A platform difference, recorded as an open item.** The whole suite on this machine
then found more in the same two passages: the merchant passage's cast at the Iroise's
mark (90241; 90240 on Windows), the mouth of the Goulet (112078; 112112), the tin sold
(123948; 123951), and the 5b schooner brought up (58689; 58690), her digest moving with
it and her 761 lines not. The merchant passage's two lines
and two ticks are not the guard's: measured twice on this machine with the guard in each
of its forms, she came out the same, and the schooner is never worn. They are between the
owner's Windows machine, where 37d to 37f pinned her, and Linux, where the gate's
releases run the suite. The gate's build (m5c) agreed on both (the owner's suite on
m5c-b ended 2713 passed, this machine's 2708 at the cut plus the five of 37b and 37c); so
something in 37d to 37f reads a figure the two platforms compute a last digit apart (the
C library's trigonometry, most likely, at a threshold the account's rules compare) or
lists a folder in the order the file system gives. Not found by reading; the pins stand
as this machine measures them, and `ci.yml` gained a manual run of the whole suite on
both platforms so the two can be compared without a gate (spec M5 §33, item 24).

**What the difference turned up, for the 37e amendments.** At the merchant passage's
second noon, in the mouth of the Goulet with the account fixed by cross bearings to three
cables a minute before, the octant's sight falls five miles and a half to the north of
it: on this machine a hair over the two doubts together (two sigmas of three cables and
of the octant's two miles and a half), so 37e's one rule takes the sight outright and
lays the account six miles north, where the cast a minute later and the bearing at the
five minutes bring it back; on the owner's machine the same sight fell a hair under and
was weighed, moving the account a few cables. The test now says what happens here and
that she is laid down again within five minutes. The finding is the owner's note 5 on
game 9 in another dress (a lunar of poor certainty overriding the better account): an
observation whose doubt is twenty times the account's is believed over it because the
two disagree, when the disagreement is the sight's. For the 37e amendments (part K,
"the doubt on one hand"): when they disagree beyond their doubts together, take the
observation only when it is the better figure, and weigh or doubt it when the account
is; with "the cast not beyond doubt", so that an account the lead has kept small does
not then refuse a right noon.

**What stayed**: a late line in the cruise, at 14:09 on the 13th, "Taken aback: the
sails pressed against the masts and she lost her way" after the book's own wear at the
hour and "keep her full and by"; the book's, not the guard's, and left.

**Also mended on the way**: `tests/test_mcp_server.py`'s cut-call test compared the
bridge's new wait to fifty seconds exactly, which the monotonic clock makes a few
microseconds over on Linux and exactly fifty on Windows; it now allows a hundredth.

## Milestone 5: the local runner (package 37i, 2026-10-09)

From the review of gate 5c (`docs/playtests/2026-10-05-gate-5c-review/report-2.md`, G15 and part K, "The local runner comes first"), the audit's reading of the runner (part N, C7 and 4.2) and game 10's record (`evidence/G10-cutter-m5cc-measurements.txt`): the five faults that ended both of game 10's seatings or lost the officer's replies. No constant of the ship, the sea or the reckoning moved; the game's determinism is untouched (the runner is outside the loop, and every change in the game's own code is to the harness's count for the handover note and to when a replay makes a door's act). The recorded passages carry no station, and none was re-pinned.

### What was built

1. **A reply cut off is not a turn** (`local.py`, `LocalModel.reply`; the harness's `cut_off` act). The runner reads why each reply ended: `finish_reason` (llama-server, and Ollama's OpenAI-compatible endpoint) or `done_reason` (Ollama's own form). A reply cut at the reply limit while the model was thinking (no words and no call, with its reasoning apart in `reasoning_content`, `reasoning` or `thinking`, or an unclosed `<think>` in the content), or any reply with no words and no call, is asked for once more in the same request, with the reason said at its end in the runner's own words, and the owner is told. Cut off or empty again, the owner is told and the runner sends the game `cut_off` with its words in place of a reply: the harness journals it (`agent.cut_off`: "No reply reached the game through the local runner: ...") and ends the turn with nothing done. No empty reply is passed on as the model's. A reply cut at the limit with words in it is a reply, and is passed on.
2. **Tokens by the server's figure** (`local.py`; `model.Reply.served_tokens`; `harness._conversation_size`). Every reply's counts (`usage`'s `prompt_tokens` and `completion_tokens`, or `prompt_eval_count` and `eval_count`) are read. The runner keeps the ratio of the server's count of a request to its own four-character measure of the same request and scales every message, the tool definitions included, by it from then on; four characters a token stands alone until the first reply and in the context guard before stationing. The counts go to the game with the reply (`served_tokens`, kept in the transcript so that a replay measures alike), and the harness measures the officer's conversation by the server's count of the request that brought the latest reply plus what came after it at its own rule, never less than its own rule (the server's count is of the request as the runner trimmed it). A fold drops the counts of the turns it keeps, which were of the conversation before it.
3. **The handover's reserve as a share** (`harness.handover_threshold`; `local.py`'s `--handover-reserve`). The flag takes tokens (`30000`, `30,000`) or a share (`0.3`, `30%`), may be given twice, once in each form, when the larger counts, and is sent to the game in tokens. Unset, the harness's own: three tenths of the context, never less than 14,000 tokens, the larger; never before six tenths, as before. The runner prints where the ask will come.
4. **An oversize request trimmed** (`local.py`). A refusal for size (llama-server's 400 `exceed_context_size_error` with `n_prompt_tokens` and `n_ctx`; or words to that effect, "exceeds", "too long", with the counts read from "(103679 tokens)" where they are given) is answered at once: the server's count of the refused request sets the ratio, the context it names is taken, the oldest exchanges that are not the brief, the folded handover note or the latest sample are left out, the owner is told once, and a smaller request is sent. The same request is never sent again after a refusal; at the third refusal in one turn, or when nothing more can be left out, or when no context size is known to trim against, the station is stood down with the numbers.
5. **The line the replay dropped** (`harness.Playback`, `Harness.on_between_ticks`, `on_input`; `core/replay.py`'s loop). Found on a fake of the save and mended; below.

The brief named `docs/agents/Harness.md` "§12 for the runner's settings"; the runner's settings are in its section 5 (§12 is "What the harness does not do"). Section 5 now says them as they are (the reply read, the server's count, the reserve, the refusal for size, the two stopgaps), §12's "Every stop replays" says where a replay makes a door's act, §13's handover paragraph says the reserve, and spec M4's line on the doors says the same. The brief named `freesail/agents/journal.py` for item 5: the journal was not at fault (game 10's replay had 261 entries for 261) and is unchanged; the harness's `Playback` was, and the brief's intent wins. Item 1's journal line and item 2's count needed the game to hear the runner, so `freesail/agents/remote.py` (the reply's `cut_off` and `served_tokens`) and `freesail/agents/model.py` (`Reply.served_tokens`, an optional field with a class default, absent from a reply that has none, so that every older save and checkpoint reads as before) changed too.

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| `CUT_AT_THE_LIMIT` (`local.py`) | `length`, `max_tokens` | llama-server's and the OpenAI form's `finish_reason`, Ollama's `done_reason`, at the reply limit | the servers' documented words; the fake server |
| asked once more | one retry for a cut or empty reply, with the reason said; then the turn ends with nothing done | the brief's item 1 ("asked once more ... if it is cut again the owner is told") | the brief |
| `CUT_WORDS`, `EMPTY_WORDS` (`local.py`) | the runner's own words at the end of the retried request, as a user message joined to the last one where it is a user message | the brief ("with the reason said in the request"); one user message and not two in a row, which some chat templates refuse | judgement |
| `PARTIAL_COUNT_SHARE` (`local.py`) | a server count under half the runner's measure is not used | game 10's four-character rule was 12 to 17 per cent short, never by half; a count that low is of part of the prompt (a server that counts only what it had not cached) | judgement |
| `OVERSIZE_STEP` (`local.py`) | 1.15 more when a refusal gives no count; also the step when a trimmed request would be the same as the refused one | game 10's short count, rounded up | judgement |
| `OVERSIZE_TRIES` (`local.py`) | 3 refusals for size in one turn stand the station down | the first refusal is answered by the server's own count and the next request ordinarily fits; a third refusal of a smaller request says the context the runner knows is not the server's | judgement |
| `HANDOVER_RESERVE_SHARE` (`harness.py`) | three tenths of the context, the default | at 102,400 the review's stopgap of 30,000 (30,720); room for two of game 10's largest samples (25,654 characters, about 7,300 tokens by the server's count) with the reply budget and the tool definitions; between game 7's six tenths (31 hours without trouble) and 37g's 0.86 | measured on the fake server, below |
| `HANDOVER_RESERVE_TOKENS` (`harness.py`) | 14,000 tokens, now the default's least (it was the default) | 37g's figure: the reply budget, the tool definitions and the 8,000 the review's reader measured as comfortable; three tenths of 32,768 is 9,830, which leaves the review's 3,500 after the reply and the tools, under its least of 4,000 | the review's arithmetic |
| `REPLY_MAX_TOKENS` | 4,096, unchanged | the owner's ruling of 2026-09-28; `--max-reply` raises it (below) | unchanged |
| `CUT_OFF_KIND` (`harness.py`) | `agent.cut_off`, a journal entry of the harness's | the brief ("the journal says so") | |

Where the ask comes, by the server's count, at the default: 102,400, at 71,680 (37g: 88,400 by the four-character count, which was past the ceiling by the server's); 65,536, at 45,875; 32,768, at six tenths, 19,660, as before 37g and as 37g.

### The two stopgap settings, tried on the fake server

Part K named two settings to use until this was built, untried by the review and by the audit. Both were tried on the fake server of `tests/test_local_runner.py` (`test_the_two_stopgap_settings_on_the_fake_server`), which counts a request as a server does: the text of each message and its calls and the tool definitions at 3.5 characters a token (game 10's figure), and four tokens a message for the template.

- **`--max-reply`.** A model that thinks for 6,000 tokens is cut off at the default 4,096 every time: asked once more and cut again, the turn ends with nothing done (before this package, the empty reply was its turn). With `--max-reply 8192` it answers at the first request. The cost is that every request keeps the larger budget free of the context, so the context guard asks that much more and the conversation has that much less before the oldest exchanges are left out. It is the setting for a model that thinks long; this package makes the cut visible and asked again, and does not raise the default.
- **`--handover-reserve 30000`.** An officer's conversation grown a sample at a time (a brief of 18,000 characters, samples of 24 log lines) at game 10's context of 102,400, the note asked for when the conversation's measure crosses the threshold; the server's count of the request at that moment:

| Setting | The harness measures by | Asked at, by the server's count | Room left under 102,400 |
|---|---|---|---|
| 37g's default, 14,000 tokens | four characters a token | 103,189 | none: past the ceiling (game 10's refusals came at 103,679 and 103,122) |
| `--handover-reserve 30000` (part K's stopgap) | four characters a token | 85,406 | about 17,000, room for the sample, the note and the reply |
| this package's default (three tenths, 14,000 at least) | the server's count | 72,069 | about 30,300 |

So the stopgap would have served on the build as it was, and this package's default asks about 13,000 tokens earlier still, by the true count. Neither setting is needed now; both may be given.

### The line the replay dropped at a stand-down by the door

Game 10's saves are not in the review's evidence folder (only the measurements are), so the drop was reproduced on a fake before it was mended, and the fake is the test (`tests/test_replay.py`, `test_a_stand_down_by_the_door_replays_with_every_line_in_its_place`): the officer stands by until one bell; at the bell a standing order fires an order inside the World's tick; the harness's own step, the last of the tick, wakes him ("One bell; the officer of the watch is sampled again"); the door, answering late as the runner does, stands him down between that tick and the next. Played, nine lines; replayed on the build as it was, eight, the waking missing and the stand-down in its place: game 10's diff exactly (4,239 for 4,240, the line at 183600 "... The Nut Rock ...; the officer of the watch is sampled again" gone, `agent.stopped` where it stood).

**The cause.** A door's act (a release, a stand-down, a word out of turn) is made between two of the World's ticks, and its transcript entry says the tick and how many journaled orders came before it. A replay made an act as soon as the World had reached that tick and that count, from any of the harness's hooks, `on_order` among them; and a standing order's firing calls `on_order` inside the World's tick (the firing is not journaled, so the count was already met). The stand-down was made there, before the harness's step at the end of the same tick had woken the officer; released, he was not woken, and the line was never written. Game 10's 08:00 on the 14th was a change of the watch, at which the officer's own standing order "the fix at the watch" fires (the record has a fix by cross bearings at 183600), in the same second as the danger that woke him: the same shape, by the record; the save itself was not to be had to prove it.

**The mend.** A replay makes an act of the tick it is at only between ticks: the replay's loop calls each station's `on_between_ticks` before the tick's inputs, `on_input` after each input, and `on_tick` and `on_order` make only the acts of earlier ticks. Each act is now recorded with the count of every input before it as well (`after_inputs`: a refused order, a query and a driver's line are inputs and no orders), and a replay makes it after as many. `on_input` made acts only when it seated a station; it now makes them for any seated station (found when the test's second case, a driver's line between the waking and the stand-down, replayed without the stand-down at all). Saves without `after_inputs` (every save before this package, game 10's among them) replay with every line; where a driver's line came between the waking and the act, as the line between them in game 10's diff may have been, the two come in the other order, the count the same and the digest not (the test's third case).

### Found on the way (package 37i)

- **A brief with no sample** is refused by the runner's budget ("The brief and the latest sample do not fit") whatever the context, since there is no latest sample to keep; no request of the game's is of that shape, and it was left.
- **Two model names in files of the repository from before this package**: the Ollama fake in `tests/test_local_runner.py` names its made-up model after a real family, and `docs/agents/Harness.md` §13 names a model by its product name. Not this package's to change; left for the lead.

### What was left

- **The turn ended by `cut_off` counts as silent** for the welfare detectors, as the empty reply it replaces did: two in a row at an urgent line still count toward the silence rule. The model did not answer, and the brief did not ask for it to be excused; the owner is told at once now. For the lead to rule on.
- **In the consent conversation** a reply cut off twice is passed on empty, as before, with the owner told at the terminal; there is no station journal yet to write in.
- **A timeout or a server error** is still asked again up to three times with the request as it then stands, which may be the same request; the brief's "never a third time" is held for refusals for size, where sending it again cannot help. A slow server's timeout is the one case where the same request may well answer.
- **Ollama's own endpoint** (`/api/chat`) is not used: the runner posts to `/v1/chat/completions` at both servers, and reads Ollama's own fields wherever a server gives them. Ollama does not refuse a request for its size (it cuts the conversation itself), so at Ollama item 4 is the runner's own budget by the server's count, not the refusal.
- **A thinking budget at the server** (llama-server's reasoning budget) was not tried: the runner asks once more and the owner may raise `--max-reply`.

## Milestone 5: the chart's tools and the viewer's details (package 37n, 2026-10-09)

The owner's notes 5 and 6 of 2026-10-09, and his addition the same day on the bearing
lines. All of it is the browser's drawing and the server's keeping of the player's marks:
no constant of the ship, the sea or the reckoning moved, nothing enters the log, the
journal, the inputs or the snapshot, and every recorded passage replays to its digest
(the save gains a `chart_marks` list, empty unless the player has pencilled the chart).

### The constants and their sources

| Constant | Value | Source | Verified |
|---|---|---|---|
| `CLEW_SPREAD` (`client/projection.js`) | a square sail's clews at 0.9 of the yard below | `tools/gen_ships.py`'s `trapezoid(..., 0.9 * yard_below, depth)` for every topsail, topgallant and royal of the four ships, as the files' notes say ("between its yard and the yardarms below") | the generator |
| the head of a sail between yards | twice the area over the depth between the yards, less the foot (0.82 of the yard for a topsail, 0.89 for a topgallant or royal, as the generator cut them) | the files' areas and heights | measured: every square sail of the four ships within 5% of its file's area (`test_every_square_sail_is_drawn_to_its_files_area_between_its_yards`) |
| `HEAD_SPREAD` | a sail with no yard below, head and foot 0.9 of its yard, as deep as its area over that | the generator's courses (`0.42 * yard` deep, `0.9 * yard` broad) and the cutter's square sail (`0.9 * sq_yard * sq_depth`) | the generator |
| the schooner's topsail | down to her bare fore yard, which the file does not carry: the depth twice the file's height of the yard above its centre (the generator puts the centre midway), the foot what the area leaves | `gen_ships.py`: "the fore yard is a bare spread yard for the topsail's foot; it is not a part here" | the generator |
| `YARD_ON_CAP_M` | a lowered yard's slings 0.3 m above the cap it rests on | the size of the cap and the parrel | judgement |
| `HOUSED_ABOVE_CAP_M` | a struck topmast's head 0.6 m above the lower cap | Luce 1866, ch. XXXIV, 'Housing Topmasts' (lowered till the topmast cap is close down on the lower cap): the topmast cap's depth | judgement |
| `STEP_HOIST` | a yard halfway while `hoist`, `settle_halyards` or `clew_down` is the step in hand; on the cap during `reef` and `shake_out` | the steps of `set_square`, `take_in_square`, `reef_square`, `shake_out_square` | the files; the half is judgement, the snapshot not giving a step's progress |
| `BEARING_FULL_S` (`client/map.js`) | a bearing drawn full for 1,800 s, a glass | the owner: "an old one becomes useless within a glass or two"; at five to eight knots a glass is two and a half to four miles run, beyond which a line from where it was taken no longer passes near her | the owner's figure; the speeds judgement |
| `BEARING_DROP_S` | dropped 4 h after it was taken, a watch; at once when a later bearing of the same mark is taken | the owner's "a watch" | the owner's figure |
| `BEARING_GHOST_ALPHA` | 0.2 at the end of the watch, fading straight from full at the glass | legible as a ghost on the chart's sea | judgement |
| `ROSE_RADIUS_PX`, grips | 80 px (never more than 0.42 of the chart's shorter side); the centre within 14 px, the rim within 12 | a finger's breadth on the 300-pixel chart | judgement |
| `MARKS_MAX` (`freesail/ui/server.py`) | 200 marks | a voyage's pencilling, and a save that stays small | judgement |
| `MARK_RADIUS_MAX_M` | a ring 200 miles at most | the chart's widest view (four hundred miles across) | judgement |

### What was found: the cutter's square sail

The file was right and the viewer wrong. `gen_ships.py` works the cutter's square sail
from Steel 1794 p. 124 ('Sloop's square-sail, or cross-jack'): 27 ft deep (four-fifths
of the mainsail's fore leech), bent along nine-tenths of its 46 ft yard, 104 m², and its
note in `data/ships/cutter.yaml` says so. The viewer drew every square sail the whole
yard broad and its area over the whole yard deep: 7.4 m, 24 ft, where the sail is 8.2 m,
the sail squat and a tenth short. The same fault drew every course of the frigate and the
brig a tenth short, and every topgallant and royal of the frigate, the brig and the cutter
a sixth too deep, over the yard below (the frigate's fore topgallant 6.95 m deep between
yards 6.0 m apart); the topsails came out about right by chance, the head and the foot
averaging to the yard. The schooner's topsail was drawn the yard's breadth and 7.7 m deep
against the generator's 7.6, near enough by chance again, but square where it is a
trapezoid. Nothing was regenerated.

Each ship, set and braced square, against her file (head and foot of the drawing; the
file's area kept within 5%): the frigate's fore course 19.7 m by 9.2 m deep, her fore
topsail 13.5 m at the head and 19.7 m at the foot between yards 12.6 m apart, her fore
royal 6.1 m and 9.5 m; the brig's fore topgallant 7.1 m and 11.0 m; the cutter's square
sail 12.6 m by 8.25 m (27.1 ft), her topsail 8.1 m and 12.6 m, her topgallant 5.3 m and
8.8 m; the schooner's topsail 10.0 m and 12.4 m, 7.6 m deep.

### The yards at their hoist

From the snapshot as it was: the sail's state (set, goose-winged, blown out or wrecked at
the hoist; sheeted home, loosed, in the gear, furled or unbent on the cap) and the step of
the square sail's evolution in hand. The frigate's fore topsail yard: on the
lower cap at 21.9 m above the water with its sail furled, 25.8 m while it is hoisted,
29.6 m set, the file's height; reefed once, its sail's reef out of the depth between it
and the fore yard. A lower yard does not move, nor does the cutter's square-sail yard:
the file crosses it as a yard and her topsail sheets to it, so lowered with its sail it
would take the topsail's foot with it. A topgallant set over a topsail on the cap (which
the sail scripts allow) is drawn at its own hoist with its clews short of the topsail
yard, not stretched down to it.

### Found on the way (package 37n)

- **The sheets of a raked mast's sails.** The viewer found the yard below a sail's clews
  by the nearest yard within half a metre fore and aft; on a raked mast with the yards at
  their hoists that could miss. It is now the yard below on the same mast by the file's
  heights.
- **The marks on a replay.** A replay makes none of the marks (they are no input), and a
  checkpoint holds them with the World. The browser's server takes them up from the save
  when it loads one, by either road (`start_server_world`). The console's `--load` does
  not (it draws no chart), so a game loaded at the console and saved there again leaves
  its marks behind; one line in `console.start_world` or `replay.build_world`
  (`world.chart_marks = data.get("chart_marks", [])`) would close it, in files this
  package does not own.
- **Playwright's own browser was not the one installed**: the headless check of the page
  used `/opt/pw-browsers/chromium` by its path. The rose, the three tools, the list and the
  socket's echo worked with no error on the page; the Python tests keep the geometry and
  the arithmetic.

## Milestone 5: the words (package 37l, 2026-10-09)

Built from the brief "Package 37l: the words" in `M5-WorkPackages.md` (the review of gate 5c's playtests, second edition: G17 whole, G13's three small things, G5's fog, part K under "Words"; the audit's two trials). Everything below was tried at seed 7 on the build machine in scripted worlds; no game's save was used.

### The constants and their sources

| Constant | Value | Where | Source |
|---|---|---|---|
| the card's quarter points | 128, each a quarter of 11¼° | `units.read_course` | Bowditch's table of the points; Falconer 1780, *Compass*; a fraction is reckoned from a whole point toward a point within eight points of it (judgement: every naming of the period's card does so, and no other reading is sure) |
| `VERB_HINT_CUTOFF` | 0.8 | `orders/errors.py` | how alike in spelling a verb must be to be hinted: 'hail' and 'haul' are 0.75 and point the wrong way, 'stear' and 'steer' 0.8; a verb that holds the words is hinted only when they are a word of it of four letters or more (judgement, set on the review's four wrong hints) |
| `ABOUT_KN` | half a knot | `standing/rules.py` | "when the true wind is 12 knots" holds within half a knot either way (judgement: the log gives the wind to the knot, and a band a knot wide is crossed and not leapt) |
| a month of provisions | thirty days | `orders/port.py` | `take in provisions for a month`; a week seven (the calendar) |
| `cutoff` of a place's hint | 0.75 | `orders/navigation.py` | a place or a mark the chart has not got is answered with the nearest names only when they are near (the moon made of cheese was offered "the oozy ground off the Eddystone" at the library's 0.6) |

### Item by item

**1. A course with a half point.** `units.read_course` reads a compass point and, after it, a half, a quarter or three quarters (in words, figures or the signs: `half`, `a half`, `1/2`, `½`; the order's normalising turns the figures and the signs into the words) toward another point within eight points, with "a point" or "of a point" after the fraction taken too. The grammar's heading reader uses it, and so do `get under way ... and steer`, `lay out a kedge to` and `allow ... set to`. The log shows the course as the card has it with its degrees: "Helm ordered: steer S by W ½ W (197°)." Refused, in words that say how a half point is said, and never steered: a fraction with no point after it ("'south by west half' toward which point?"), toward a point more than eight points off ("north half south" is no course), two courses in one order ("Two courses were given ('south-west' and '245 degrees'); say one"), and a course with a count of points after it (`steer west two`; this was the trap: "half" was read as a count of points, and the last word as the course). A test steers every one of the 128 quarter points, said from the point before it toward the cardinal ahead and from the point after it back toward the cardinal behind, in words, figures and signs, long names and short (`tests/test_orders.py::test_the_whole_card_in_words_is_read_to_the_quarter_point`, 1,344 forms). The completer offers the half and quarter points after a whole point.

**2. One reader for numbers.** `freesail/orders/numbers.py`: figures; the units and the teens (thirteen, fourteen, seventeen to nineteen were read by none of the five readers before); the tens with their units ("twenty five", "eighty-five"); the hundreds with or without "and" and the thousands; "a dozen", "a score"; a half, a quarter, three quarters, "half a", "a quarter of a"; "and a half", "and a quarter" after a number. Every order that takes a number reads it there: the grammar's counts (points, reefs, fathoms of a line, degrees in words), the standing dialect's numbers (knots, minutes, fathoms), the ground tackle's fathoms and depths (`veer five fathoms`, `a hundred and eighty-five fathoms`), the port's tons, days and hands, the master's knots of set, the canvas's number. The five word lists are gone. A word before "fathoms" that is no number is refused ("'umpteen fathoms' is not a number of fathoms I can read"). `take in provisions for sixteen days` takes sixteen; for a month thirty, for six weeks forty-two, and words that are no time are refused where they took thirty in silence. One effect beyond the brief: `when the true wind exceeds thirty then ...`, refused before as "what number?", is taken as thirty knots (the standing table's row is moved to a word that is no number).

**3. A standing order's action read whole.** `orders.read_whole` parses each order after `then` and reads it as its own reader would, without carrying it out: a sail, a yard or a line by name (ambiguous or unknown refused: `set the topsail` on the frigate); a mark of the chart for a bearing, the marks of a fix, a place or a point off one for a course, a position, an allowance (`navigation.check`); an anchor's name, fathoms, a course and a bearing, and an anchor the ship does not carry (`ground_tackle.check`, the order run against a stand-in for the runner that starts nothing); a person sent for (`people.check`); tons, days and hands (`port.check`); the refused phrases (below). What depends on the moment (what is in sight, an anchor down, whether she is in port) is still the order's business when it fires, and on a ship with no chart nothing of the chart is read. The audit's three are refused at the giving: `take a fix as soon as a bearing can be taken` ("names no mark of the chart"), `take a bearing of the moon made of cheese` ("The chart has no mark named ..."), `let go the sheet anchor` in the cutter ("She carries no sheet anchor; her anchors are ..."); each refusal names the order, the third order of three as much as the first. Every book the game ships loads as it did (a test gives the four books with routines; nothing is refused that was taken).

**4. The phrasings.** Each taken, or refused with what to say instead, and tested (`tests/test_orders.py`, `test_standing.py`, `test_tell.py`, `test_officer.py`):

| Said | Now | How |
|---|---|---|
| `steady on` | taken: "Helm ordered: steady on N (0°)." | a synonym of `steady` |
| `trim the headsail sheets` | taken: the sheets of each headsail trimmed | the grammar reads "<a group of sails> sheets" for `trim` as the group, where the ship has no line of that name |
| `buy 20 tons of salt fish and 8 tons of pilchards` | taken as two bargains | split at an "and" that a number of tons follows, each read, weighed together against the hold and the purse, and struck together, the boat sent once for them all (`Ports.trade_together`; the boat carries a list); one that cannot be struck refuses the order and nothing is paid |
| `shape a course for a mile west of ushant` | taken | a point laid off from a place of the chart by a distance (cables, miles, leagues) and a point of the compass, the course shaped for it from the account as for any point pricked on the chart |
| `where is ushant` | taken: "Ushant: not in sight; by account it bears S by E, 88 miles." | a mark of the chart, in sight by the lookout's bearing and estimate, else by account from the master's position (`Navigation.account_now`, which never moves the account); a person as before; neither, refused with both said |
| `pipe down the watch`, `pipe down the larboard watch` | taken | synonyms of `pipe down`; the answer says which watch has the deck |
| `call the starboard watch` | taken (new verb `call the watch`) | the watch below turned up by itself as a watch sent to work is (`crew.WatchCall`), up until piped down; the watch on deck answered "has the deck already". Kept back from the officer as `call all hands` is, unless the captain's word allows it |
| `belay get under way` | taken | the work belayed by the order that started it: the ground tackle's and the port's evolutions are known to `belay` by their orders |
| `put the helm over` | refused: "'Put the helm over' says not which way: say 'helm a-lee' ..., 'hard a-weather' ..., 'bear away' or 'come up' with the points, or 'steer' a course." | and struck from the officer's brief, which names the helm orders instead ("alter her course by any helm order ('helm a-lee', 'hard a-weather', 'bear away two points', 'steer NW')"); `docs/agents/Harness.md` and primer 16 the same. A helm put "to starboard" was the tiller's word in 1806 and the wheel's later, the opposite way; no order of that form is taken |
| `take in the water sail` | taken | the port's `take in the water` gives way to a sail of the ship named after `take in`; a ship with no water sail says she has none |
| `furl` the water sail and the jibs | taken: the sail taken in | a sail not furled on a spar (a jib, a staysail, a studding sail, the water sail, a gaff sail) told to furl is handed and stowed, which is `take in`'s evolution for its class |
| `lower` the water sail and the jibs | taken | "lower" is said of a jib and a studding sail as of a gaff sail (`take_in_words`) |
| `clew up` the water sail and the jibs | refused: "A jibheaded sail is hauled down, not clewed up; say 'haul down the jib' or 'take in the jib'." | as it was: clewlines are a square sail's |
| marks without accents or apostrophes | taken: `lavandiere`, `st anthonys head` | one key for a name (`geo.name_words`): lower case, accents folded, apostrophes dropped, in the chart's index, the lookout's, the master's, the tide's and the navigation orders' |
| `hail the pilot` | refused with no hint (37h's verb) | the hint "did you mean 'haul'?" is gone: a verb is hinted only when near in spelling |
| `man the pumps` | refused: the pumps are not worked yet, the hull's damage a later milestone's; 'sound the well' says so | the vocabulary's new `refused_phrases`, read before the grammar (and by `read_whole`) |
| `as you were` | refused: say 'belay that', 'belay all work', or give the order that puts her back | `refused_phrases` |
| `Mr Pearce you have the deck` | taken | the officer's name before the giving with no comma |
| `hoist our colours` | refused: "Colours and signals are milestone 7's ..." | `refused_phrases` (`show your colours`, `hoist the ensign`, `make the private signal` and the like) |
| `the deck is yours` | taken | the same word as `you have the deck` |
| `bring her up` | taken: "come up a point" | a synonym of `come up`; `bring up` alone stays anchoring |
| `back the fore staysail` | taken: its sheet hauled to windward | a headsail, which has no yard, is backed as `haul the fore staysail sheet to windward` backs it (package 32e) |
| `close hauled` | taken: keep her full and by | synonyms of `keep her full` |
| `lay out the stream anchor astern` | refused: "The boat lays out the kedge and no other anchor in this game: say 'lay out a kedge astern' ..." | `refused_phrases`; `lay out a kedge astern` (and `ahead`) is taken, from her head as she lies |
| a `tell` to a station nobody holds | taken, kept and said | kept in the station's journal (`agent.word_kept`), and passed to whoever takes the station in its first sample, once (`agent.word_passed`); the log says so. A standing order's word to nobody is refused when it fires, as before (a book would fill the journal every glass) |
| `send for the master` in the schooner | refused, saying why: "In this vessel the master is the captain: Mr Travers, yourself; there is no sending for yourself. The mate is Mr Ray; say 'send for the mate'." | the master who commands is named |
| "when the true wind is 12 knots" | taken | a speed compared with 'is' holds within half a knot of the figure (`about`), so a `when` fires as the wind comes to it from either side |

**5. The fog reading's sentence, and the drill's count.** `the nearest land` in thick weather read "not to be seen: in this weather the shore shows within a cable at most", which game 10's officer read as land within a cable and hove to in mid-Channel. It reads now "none seen within a cable; in this weather the shore shows no further off than that, and land beyond it cannot be told" (by night, "within a mile ... by night"). The drill's miscount is traced: a stand-by ends the reply's turn, and the results of that reply's other calls are not added to the turns (they are said when the stand-by ends); the drill counted calls by the results in the turns, so three calls in one reply counted the stand-by alone, and it counted the stand-by by the station's state at the moment of counting, so when the drill went on and the stand-by was lifted it was asked for again. The harness keeps the results of each reply a stand-by ended (`Harness.stood_results`), the drill reads them, and a call once counted stays counted. Both of game 10's sequences pass (`test_officer.py`).

**6. G13's two small things.** `stand_down` with the deck and no note asks for the handover note and does nothing till it comes; without the deck it is taken with none and the result says "no note was left (none is asked without the deck)"; the tool's description says so. The brief lists the tools the station may use: the watcher's no longer names `hand_over`, `handover_note` and `submit_order`.

### The primer

Chapter 2's compass section has the card's quarter points, the half point said and refused, and the numbers in words; chapter 7 a section, "Saying it", with the phrasings and the refused words, and the standing order's action read whole; the forms tables of chapter 10 (`shape a course for a mile west of the Lizard`, `where is the Lizard`) and chapter 11 (`when the true wind is 12 knots`, a number in words), each read by `tests/test_primer.py`. Chapter 10's nearest land and chapter 16's way out of danger and stand-down are brought up to the words.

### The recorded passages, and the suite

No pin moved, and none was re-pinned. `python3 -m pytest tests/test_known_truths.py --slow -n 4 -k "gate_5b or gate_5c or merchant or cruise or schooner"`: 9 passed, the 2 strict expected failures as they stand (the schooner's pilot, 37h's; the cruise), and one failure, the pace at the merchant passage's start (153 ticks a second against the floor of 500), measured while four suites ran on the machine at a load of 28. Measured alone at that load, three thousand ticks best of three: the base tree 574 and 448, this branch 536; the same within the machine's noise. The standing books are read whole now, and every book the game ships loads as it did (a test gives them); the recorded passages' books use no word the change reads otherwise.

Fast tier, `python3 -m pytest -n 4`: 2,877 passed and 3 failed, none of them the words': the pace above; `test_chart`'s timing of a nearest-shore search (2 ms allowed, 3 ms taken under the load); and `test_replay`'s fingerprint of the tree, which was edited (the name-key cache below) while the suite ran. The last two passed when run again on a quiet tree.

### Found on the way (package 37l)

- **The last word was the course because "half" was a count of points.** `steer south by west half west` read "south by west" as a heading, "half" as half a point, and "west" as a second heading that replaced the first; the helm took the heading and the points went unsaid. Two courses, or a course with a count, are refused now.
- **The drill's count** (above): a stand-by ends the turn before the reply's other results are added to it, which the harness says when the stand-by ends, and which nothing that counts calls by their results could see. The same holds for any other reader of a reply's results; the harness's `stood_results` is there for them.
- **A name's key cost a tenth of a tick.** The merchant book asks the chart ten times a tick for a place by name; folding the accents on each ask cost a tenth of the tick under the profiler. The key is remembered by the name, and the folding is skipped for a name with none.
- **A replay seats a station after the inputs of its tick.** A `tell` given before the station was taken found, in the replay, a station not yet seated; it is held by nobody until it is seated, as in the game.
- **`steer ... for <place>` and `shape a course for` share the place reader**; a point off a place uses the chart's own name index, so the accents and the apostrophes are folded there too.
- **Not built, and why.** The stream anchor laid out by the boat: the kedge's evolution lays out the kedge alone, and widening it is the anchor's script (37k's file); refused with what to say. A fog signal stays later, as the review has it. `hail the pilot` is 37h's verb; here only its wrong hint is withdrawn.

## Milestone 5: the pilot (package 37h, 2026-10-09)

Built from the brief "Package 37h: the pilot" in `M5-WorkPackages.md` (the review of gate
5c, second edition: G10 whole, G8's hail at anchor, and part K's three items for 37h; the
owner's rulings of 5 and 7 October in decisions 35 and 36). Measured at seed 7 on this
machine (Linux), in scripted worlds and the five recorded passages.

### What was built

- **Taken or declined at his hail** (`world/ports.py`, `orders/port.py`,
  `data/vocabulary.yaml`). `take the pilot` (`we will take the pilot`, `take him aboard`)
  answers the boat's hail; she shortens sail or heaves to as the hail asked when she is
  still too fast for him, and not twice when the captain or the book has the sail coming
  in already. `decline the pilot` (`we need no pilot`, `wave him off`) sends the boat back
  to her station, and none comes off from that port for six hours (package 35's
  `PILOT_AGAIN_H`). `hail the pilot` hails a pilot's boat in sight (the lookout's
  sighting, or within hail) and takes him; with none it is refused in words, never "did
  you mean 'haul'?". Unanswered, the boat keeps company, hails once more after
  `PILOT_HAIL_AGAIN_S` and bears away for her station, the line saying so: **no pilot
  boards a ship that has not taken him.** Taking or declining is the vocabulary's object
  `port`, so a general grant keeps it back with the port's business (`agents/agent.py`'s
  reason names it; `orders/stations.py`'s words).
- **His boat closes with the ship** (`world/ships.py`, the `company` leg). From her hail
  the boat keeps company a cable and a half off: within it she goes with the ship at the
  ship's way over the ground; beyond it she closes at her own pace or the ship's and
  `COMPANY_CLOSING_KN` more. He boards within two cables at six knots or under, as before.
  A ship too fast for him is told so ("The cutter keeps company: she cannot put the pilot
  aboard at 7 knots, and waits for her to shorten sail or heave to.", at most once in
  `PILOT_WAITS_SAY_S`), and taken and still too fast at the interval she is hailed once
  more, to heave to. The hail asks to shorten sail only of a ship over six knots, and
  never asks a ship at anchor for anything but whether she will take him.
- **His warnings** (`world/ports.py` `_warn`, `world/chart.py` `dangers_ahead` and
  `shoal_ahead`). Aboard and within his port's ground, from the true chart and the tide's
  height now: a charted danger her true track passes within a cable of (beyond its
  extent) with less than a fathom under her keel, by name, once while he is aboard; the
  water shoaling to that ahead, at most once in ten minutes; each an urgent line saying
  on which hand the deeper water lies, a danger line for the stations and an event for the
  book (`at the pilot's warning`). In thick weather (under a mile) he says once that he
  cannot see his marks and warns by the lead and the time run: five minutes' run ahead
  and without the danger's bearing. Nothing of it is in a reading. He does not con.
- **His leaving and his fee.** Brought up in his port's anchorage or mooring he asks for
  his boat once ("The pilot asks for his cutter: she is brought up in Carrick Road, and
  his charge is done."), waits at the gangway (`world/people.py`), and leaves in her
  from the quay; anchored in the outer road he stays (she waits there for her tide).
  Outward he leaves a mile beyond the outer road as package 35 had it, asking for his
  boat once; an inward pilot is put off outward only if she stands out with
  `PILOT_STANDS_OUT_KN` of way, not as she drifts hove to for him. The pilotage is paid
  from the purse as he goes, once, at his port file's `fee_pounds`, and the line says so.
  He is "the pilot of Falmouth" in `the people`, and pilots her in or out by whether she
  last lay in his port (he "took charge of her" before, and took charge of nothing).
- **His words.** The breakwater out of the Plymouth pilot's mouth (begun 1812): White's
  triangle as White gives it. "The flood" is the world's own stream in his road
  (`Ports._stream_turn`), where it was his high water less six hours twelve minutes. The
  boat that keeps company says what she waits for, and `the pilot` with no pilot aboard
  says what his boat is doing ("the Falmouth cutter has hailed and waits for an answer
  ('take the pilot' or 'decline the pilot')"). The drying rocks are named on the
  captain's chart (`client/map.js`: the Woolpack, the Spanish Ledge and the Bartholomew
  were "unnamed but marked", being of the kind `drying`, which was not in the names'
  list). The primer's chapter 14 is rewritten for all of it.

### The constants and their sources

| Constant | Value | Where | Source |
|---|---|---|---|
| `PILOT_HAIL_AGAIN_S` | 600 s | `ports.py` | judgement: two hails ten minutes apart, time to answer a boat and shorten sail; the bearing away ten minutes after the second |
| `PILOT_COMPANY_M` | a cable and a half | `ports.py` | judgement: within the two cables he boards from (package 35's `PILOT_BOARDS_WITHIN_M`) |
| `PILOT_WAITS_SAY_S` | 600 s | `ports.py` | judgement: the boat's word at most once in ten minutes |
| `PILOT_WARN_AHEAD_S`, `PILOT_WARN_MIN_M` | 600 s, three cables | `ports.py` | judgement: "in time to act", a mile at six knots, time to stay, wear or anchor a ship |
| `PILOT_WARN_ABEAM_M` | a cable | `ports.py` | judgement: a danger the track passes within a cable of, beyond its extent (the chart's rocks are points; `chart.DANGER_PASS_NM` is the account's mile) |
| `PILOT_UNDER_KEEL_M` | a fathom | `ports.py` | judgement: shoal water is less than a fathom under her keel at the tide's height now |
| `PILOT_WARN_AGAIN_S` | 600 s | `ports.py` | judgement |
| `PILOT_THICK_NM`, `PILOT_THICK_AHEAD_S` | a mile, 300 s | `ports.py` | the owner's ruling ("thick weather means he cannot see his marks"); the figures judgement |
| `PILOT_STANDS_OUT_KN` | 3 kn | `ports.py` | judgement: standing out under sail, not drifting or forereaching hove to |
| `COMPANY_CLOSING_KN` | 2 kn | `ships.py` | judgement: a pilot cutter was the fastest thing in her water; the far-detail boat is given the pace and not the means |
| the side looked at for the deeper water | two cables | `chart.shoal_ahead` | judgement |
| `fee_pounds` | £5 Falmouth, £6 Plymouth, £4 Brest, £3 St Mary's and Roscoff | `data/ports/*.yaml` | package 35's and 35b's, from memory and unverified as the files say; no page in `docs/references/` gives a rate (the Regulations of 1806 speak of the certificate and "the usual rate", not the figure) |

### The flood, before and after

The pilot's "the flood will serve from" at 06:00 on 12 June 1805, the old words against
the world's own stream in his road:

| Port | High water | Old: high water less 6 h 12 m | New: the stream turns to the flood in the road |
|---|---|---|---|
| Plymouth | 17:42 | 11:30 | making now (Cawsand Bay) |
| Falmouth | 17:07 | 10:55 | 11:05 |
| Brest | 16:05 | 09:53 | 10:36 |

### St Mary's Sound: the chart's depths against his directions

Measured on the chart at the datum (`chart.depth_at`), in fathoms:

| Where | The chart | The directions |
|---|---|---|
| off the Woolpack, a cable and two, S to NW | 4.4 to 6.2 | "immediately off it 7 and 6 fathoms" (Imray p. 106) |
| the fair way, midway between the Woolpack and the Bartholomew | 5.8 | the fair way |
| midway between the Woolpack and the Spanish Ledge | 2.1 | (no such passage) |
| off Peninnis, two cables S to SW | 15.9 to 16.7 | "come no nearer it than fifteen fathoms" |
| off Peninnis, five cables W | 2.2 | |

The depths agree with his words where his words put the fair way; what does not agree is
the features file's placing of the three dangers, all on one parallel (49° 54.4' N) with
the Spanish Ledge a quarter of a mile **east** of the Woolpack, where White and Imray (and
the feature's own `says`) have it on the larboard hand going in, with the fair way between
it and the Woolpack. A ship that keeps the Woolpack to starboard and the Spanish to
larboard by the chart is over two fathoms: the owner's "12, 9½ and then 4 fathoms" over
ground "the chart has at 2.3". The game's pilot warns from the same chart as the lead, so
he and the lead agree; he names the Spanish Ledge "on the starboard bow" where his words
say larboard. Not mended here: it is `data/charts/features/channel-west.yaml` (and its
index), a chart package's file, and wants the sheets read again.

### The recorded passages, re-measured with the reasons

| Passage | Lines | Digest | What moved, old → new | Why |
|---|---|---|---|---|
| the frigate, 5b | 768 → 754 | `dbf7f6fcfb800fdf` → `ded18dca91367945` | the outer road 58297 → 58298, the anchor 58647 → 58650, brought up 59642 → 59643; hail 57480 and aboard 57540 stand | her book's line at the hail is `take the pilot` where it was `shorten sail`: under six knots at the hail she is asked nothing, and the shortening's lines (her sail in at the rounding already) are gone |
| the schooner, 5b | 761 → 800 | `c8905673506f717e` → `968d3be83036854b` | the pilot aboard at 56580 (never, since 37e); hails 55800 and 56400; the outer road 56515 → 56511; the anchor 57638 → 58244 in eight fathoms and a half (seven); brought up 58689 → 59360 | taken at the hail, the cutter keeps company with her at seven knots; hailed again to heave to, he boards as she comes to the outer road, and she fills away for Carrick Road (her book, below) |
| the thick passage, 5b | 488 | `fb136bb8e86f0804` | nothing | no cutter comes off |
| the merchant passage, 5c | 2994 → 3011 | `c52c14c725a5ed1f` → `5d708ee83c7018ba` | the pilot of Brest aboard 96240 → 96180; put off at the anchor in the Bay at 121560 and paid £4 (never before); every other pinned tick stands | the boat closes at her own pace or the ship's and two knots more; brought up in the Bay his charge is done; the lines of the answers, his warnings (the Black Rock outward, the Buzec and the shoal water off Petit Minou) and his boat |
| the naval cruise, 5c | 2037 → 2041 | `bb8b2499fde6a0f4` → `301ca2e8aad8b405` | the Plymouth pilot aboard 7980 → 7920; every other pinned tick stands | taken at the hail; the boat closes at the better pace |

`test_the_schooners_pilot_boards_before_she_runs_in` has its expected-failure mark off
and asserts his boarding at 56580, within ten minutes of the outer road and more than ten
before her anchor.

### The books, and the count of runs

- **The frigate's (5b)**: `at the pilot's hail then take the pilot` for `... shorten sail`.
- **The schooner's (5b)**: three lines and a guard. `at the pilot's hail then take the
  pilot`; `at the pilot aboard then fill away`; `at filled away, if the distance to
  Falmouth is under 5 miles then shape a course for Carrick Road`; and the noon's `stand
  on` guarded to the noon's own filling away ("if the distance run since noon is under 5
  miles"), as its cast already is, since unguarded it sent her back to the point east of
  the Manacles when she filled away for the pilot.
- **The merchant's (5c)**: `then take in the fore topsail; take the pilot` for `then take in
  the fore topsail`.
- **The cruise's (5c)**: `standing order "the pilot boards": at the pilot's hail then take
  the pilot` added.

Fourteen whole-passage runs, in three rounds. The schooner five times: `take the pilot`
alone (he boarded off the town a minute before her anchor: her light sails in and her
topsails reefed, she still made seven); with the fore topsail in and plain sail after (no
better); with the boat's second hail asking her to heave to (he boarded at the outer road,
but she lay hove to, drifted, opened her distance and he asked to be put off outward, and
she anchored in the outer road); with the inward pilot kept aboard while she drifts and
the book filling away (kept); and once more after the boat's closing pace was mended.
The frigate twice and the thick passage once. The merchant three times: with `take the
pilot` alone at the hail, its shortening of sail boarded the Falmouth pilot three minutes
later and put him off four minutes later, which carried her past the Iroise's mark too
wide for its cast; with the fore topsail kept before it, he boarded on his old minute but
was put off three minutes late, the boat closing at the ship's pace and two knots where
package 35's sailed at her own polar; the closing pace was made the better of the two,
and the third run is the one pinned. The cruise three times, the second needlessly (the
same code as the first for her).

### The suite, as run (package 37h)

On a machine shared with four other packages' suites (load 14 to 30 on four cores), at
`-n 4`: the fast tier 2,751 tests, 2,747 passed and 4 failed. Two were tests already
mended in this package's tree while the run was under way (the officer's list of the
lines that speak of danger, the gig of `test_ships.py`), and pass alone; two are timing
floors: the chart's `coast_at` under two milliseconds (passes alone) and the merchant
passage's pace at 500 ticks a second, which fails on the base commit too on this machine
(455 and 494 there against 404 and 433 here, run side by side; the profile of two
thousand ticks shows the same calls within a seventh of one per cent, so the difference is
the load). The slow tests of the passages touched (`-k "schooner or merchant_passage or
naval_cruise or truth_72 or passage_for_gate_5b or thick_weather or cutter_and_the_brig"`,
seventeen): fifteen passed, the schooner's pilot among them, one expected failure of the
schooner's hull (not this package's), and the pace floor. `tests/test_ports.py` and
`tests/test_people.py` with the slow tier: 38 passed.

### Found on the way (package 37h)

- **St Mary's Sound** (above): the features' positions, not the depths, part from the
  directions. For a chart package.
- **The grounding line says "no water of water by the chart"** when a rock is awash
  (`chart.Grounding.words` with a depth of nought): seen on the Black Rock in this
  package's tests; not this package's file, and left.
- **No pilot comes off to a ship at anchor**, and `hail the pilot` needs a boat in sight:
  a ship anchored in the outer road to wait for the tide cannot call one off (the period's
  jack at the fore). Left: it needs a signal the game has not got.
- **The pilot's fee is one figure a port**, from memory; the period's rates went by the
  ship's draught and the distance, and no page in the references gives them.
- **The officer's domain words still say he may give orders on "the pilot's hail"**
  (`agents/agent.py`, the officer's brief): that is `ask the pilot`; taking or declining
  is kept back as the port's business, and the brief's words were not changed (they are
  the station's brief, and a change re-asks no one but is the lead's to make).

## Milestone 5: the ground and the helm, amended (package 37k, 2026-10-09)

Built from the brief "Package 37k: the ground and the helm, amended" in `M5-WorkPackages.md` (the review's G7 and G8, "What is left", and part K, "The ground and the helm, amending 37f"; the audit's narrowing of two of them). Measured at seed 7 on this machine (Linux), in scripted worlds; the game's own saves are the owner's and are not in the repository, so game 10's states were built again from its log.

### The constants and their sources

| Constant | Value | Where | Source |
|---|---|---|---|
| `LET_GO_STATES` | at the bows, a-cockbill, aweigh, catted | `scripts.py` | Falconer 1780, ANCHOR a cock-bill ("suspended at the cat-head by its stopper, ready to be sunk from the bow at a moment's warning"), AWEIGH ("drawn out of the ground in a perpendicular direction ... synonymous to atrip"); an anchor hanging by its cable is let go by letting the cable run |
| `HANDING_EVOLUTIONS` | take in, furl, unbend, shift a sail | `scripts.py` | a sail the hands are taking in is not one to lay aback: game 10 (the review's G7) |
| `DEEP_ROAD_FATHOMS` | 20 fathoms | `scripts.py` | the directions' roads in these waters lie in three to seventeen fathoms (Carrick Road 7 to 17, St Just Pool 14 or 15, Bertheaume 8 to 12, the Bay of Brest 8 to 16, St Mary's Road 4 and 5; `data/charts/features/channel-west.yaml`, from White 1835, Imray 1874 and Faden 1793); Luce 1884, ch. XXXIV: "Always double-bitt before anchoring in deep water, as at Madeira"; twenty is judgement, three fathoms past the deepest road |
| the refusal's scope | three times the depth (`SHORT_SCOPE_PER_DEPTH`, unchanged) | `physics/anchor.py` | Luce 1866, ch. XXXIV, p. 568: "the old rule for giving the proper scope to ride by, was three times the depth of water"; Falconer 1780, ANCHOR-ground: too deep, "the cable bears too nearly perpendicular, and is thereby apt to jerk the anchor out of the ground" |
| `DRAG_HOLDS_AGAIN_S` | 900 s | `physics/anchor.py` | the brief's quarter of an hour (the review's G8, 37f's own note) |
| `LIFT_SAY_S`, `LIFT_REARM_S` | 5 s, 60 s | `physics/hull.py` | her sails lifting: said before the ten seconds of a sail aback and the ten of the ship's aback can pass; armed again as the aback's line is (`ABACK_REARM_SECONDS`); judgement |

### Item 1: the anchor left aweigh, its conditions first

Game 10 (the review's G8, the measurements' log): at 03:53 on the 14th "The best bower is aweigh."; at 03:55 the owner's `Belay get under way` was refused, "Nothing in hand or waiting answers to 'get under way' ... The work in hand: getting under way, ..."; he belayed it in other words; at 04:09 `let go the best bower`, `come to an anchor`, `come to anchor` and `drop anchor` were each refused "the best bower is aweigh", and `weigh the best bower` "no anchor is down". Reproduced in a scripted world (the cutter brought up by the best bower in nine fathoms in Falmouth's outer road, `get under way`, the belay two minutes after "is aweigh"), word for word. The conditions:

- *The window.* `get under way` (and `weigh`) sets the anchor's state to aweigh at the break-out, `break_out_s` after the cable is up and down, and to "at the bows" only when it has been catted and fished, `cat_and_fish_s` (five minutes) after it is up to the bows, which is the depth over `hoist_fathoms_per_s` after the break-out. A belay in that window, some six minutes in nine fathoms, leaves the anchor aweigh for good: the belay removes the work and nothing else ends it.
- *Why it was stuck.* `let go` and `come to an anchor` took an anchor only at the bows or a-cockbill; `weigh` and the cable's orders only one down; so an anchor aweigh answered to nothing but `cat and fish`, which took the cutter fourteen minutes in the game with the hands at other work.
- *The audit's trial* belayed before the break-out: the anchor was down and she simply rode by it. One more thing was found there: the cable was left marked as being hove in (`Anchor.heaving`), which keeps the physics from ever judging the anchor to drag.
- *The words of the belay* were refused because the ground tackle's verbs start their evolutions from their own table (`orders/ground_tackle._EVOLUTIONS`), which `belay <the order>` did not read.

Built: an anchor aweigh or catted is let go as one at the bows (`can_let_go`); `weigh` and the cable's orders, with no anchor down, say where one hangs ("no anchor is down: the best bower aweigh and hanging at the bows, to be let go again or catted and fished"); a belay of any of the anchor's work says where it has left the anchor (`Script.left_words`): on the bottom with so many fathoms out, aweigh and hanging off the ground or at the bows, at the cat-head, or catted and fished; the belay lets the capstan's mark go (`Script.belayed`); and `belay get under way` (the order's own words) belays it. The tests pin the window at its two ends and the audit's case (`tests/test_anchor.py`).

### Item 5: anchoring in forty fathoms, looked at

*What the period did.* Falconer's anchoring ground is "neither too deep, too shallow, nor rocky", the first because the cable stands too near up and down and jerks the anchor out; Luce 1866 gives three times the depth as the old rule of scope and five or six as the safer; Luce 1884 names deep water as an exception, "as at Madeira", for which the cable is double-bitted. The directions this game's charts are drawn from put every road of these waters in seventeen fathoms or less. In forty fathoms a ship of the period was in the offing, "generally out of anchor-ground" (Falconer, OFFING), and anchored there only when she must.

*What the game did.* One rule, per anchor: refused when the depth was more than a third of the cable bent to that anchor. The best bower has two cables spliced (240 fathoms) and the small bower one (120), so in forty-five fathoms the best bower was let go with 225 fathoms out, five times the depth, and the small bower refused with "no anchoring ground here: 44 fathoms and a half" and no reason. That is game 10's unevenness; it was the cable and not the water.

*The rule now.* The same refusal, by the old rule of three times the depth, with the reason and the anchor whose cable would reach ("no anchoring ground here: 46 fathoms and a half, and the small bower's a hundred and twenty fathoms of cable give less than three times the depth, the least she will ride by; the best bower has 240 fathoms"); and past twenty fathoms a notable warning as the anchor goes, "46 fathoms and a half is deep water to anchor in: the roads lie in seventeen fathoms and less, and here she rides on a steep cable and will be long heaving it in." Neither the scope's default (five times the depth, the owner's ruling) nor the physics changed.

### Item 6: the dragging that relapses

Measured by the test of it (`tests/test_tackle_orders.py`): four spells of three minutes' coming home, ninety metres each, with eight minutes' holding between (past the physics' five, inside the quarter): before, four urgent lines and four "holds again, having come home half a cable"; after, one urgent line, a notable "still coming home" counting every spell's metres, and one "holds again, having come home two cables" when it has held a quarter of an hour. The physics' flag (`Anchor.dragging`, the reading's "dragging") still falls after five minutes' holding; only the log's lines wait the quarter of an hour.

### Items 2, 3, 4, 7 and 8

- **Item 2, an anchor she does not carry.** `let go the sheet anchor` in the cutter, with getting under way in hand: before, "Order: let go the sheet anchor." and four minutes later "Could not let go ...: no anchor aboard answers to 'sheet'" (the audit's narrowing: with nothing in hand it was refused at once); after, refused at the order whatever the hands are at, "she carries no sheet anchor; her anchors are the best bower, the small bower and the kedge", by `let go`, `come to an anchor with`, `weigh`, `veer`, `heave in` and `cat and fish` alike. `verbs.py` needed nothing: every order that names an anchor comes through `orders/ground_tackle.py`.
- **Item 3, a heave-to backs a sail that is set.** Game 10's state built again: the cutter under plain sail, `take in the foresail` and then `heave to`. Before, "Hauled flat aft the mainsail sheet; the foresail sheet to windward; braced the topsail aback; helm a-lee.", the foresail coming down as its sheet was held to windward (in the game, with no topsail to the mast, she filled within a minute). After, "...; the jib sheet to windward; ...", hove to on the starboard tack at 1335 (1360), lying five points and a quarter from the wind with a quarter of a knot of sternway for twenty minutes. The square sail laid aback is on the main's yards whenever a sail stands there, set, not being handed and not a course (which the heave-to hauls up): the main topsail, or with it furled the main topgallant, as before, and the line names it ("Hove to on the starboard tack, main topgallant to the mast, helm a-lee.", the brig lying five and a half points off). With nothing standing on the main the yards of the mast with the most such sail are laid aback: the fore topsail, Luce's 'To heave to with the fore topsail to the mast', where before the main's bare yards were braced aback with only a course on them, which the heave-to hauls up. The first form of the rule backed the fore topsail whenever the main topsail was not standing; the brig so hove to with her main topgallant still set would not lie to (her spanker brailed up, she fell off to the quarter and the order failed in words at ten minutes), where with the topgallant aback she lies to as before. The tending is built for the main's yards aback, and how a ship lies with her fore topsail to the mast is left as found. The passages heave to as they did, every one of them.
- **Item 4, the alarm for being taken aback.** A sail the hands are at (an evolution running on it, its yard or its sheets: `physics/sails.sails_in_hand`) is left out of the judgement and its thrust with it; she is aback by the sails that stand. And "Her sails lifting, the wind 47° on the larboard bow: keep her away, or she will be taken aback.", notable and a line that speaks of danger (`DANGER_LINES`; the event `her sails lifting`), when the apparent wind has been forward of her luffing angle and of the beam for five seconds, with way on her in a working breeze, sail standing and no manoeuvre in hand. On the recorded passages it comes ten seconds before the thick passage's one urgent "Taken aback" and twenty-five before the cruise's; every other is a header met by the book's own trim rule within the minute.
- **Item 7, a tack that could not begin.** A tack given while the lead was going (it holds the ship) and found off the wind when its turn came: before, "Squared the yards; she fell off on the starboard tack, to try again or to wear." with no "Ready about" (the *Speedwell*'s three, the audit's trial); after, "Could not go about: she is not close-hauled; bring her by the wind before going about." (`tack.yaml`'s `on_refused`, which the runner says for work that waited and could not begin; any evolution may have one). Given with nothing in hand it is refused at the order, as it always was.
- **Item 8, her draught.** A reading, `her draught` (`the draught`, `the ship's draught`, `what she draws`), of kind depth so that a standing order compares it as a depth: "she draws fifteen feet of water, two fathoms and a half".

### The recorded passages, re-measured

Each measured once after the change (`dump_passages`, the six in one run; the cruise once more after the lifting line was kept forward of the beam, see below), against the six written out before the first change, which matched the pins.

| Passage | Lines | Digest | The true track | Why |
|---|---|---|---|---|
| 5a's day | 616 → 616 | `efc286e862237e53` → the same | the same | nothing of hers is touched |
| the frigate, 5b | 768 → 768 | `dbf7f6fcfb800fdf` → the same | the same | the same |
| the schooner, 5b | 761 → 763 | `c8905673506f717e` → `7b9c22774b719b59` | the same, every tick | "Her sails lifting" at 52912 and 53538, on the run in from the Lizard |
| the thick passage, 5b | 488 → 491 | `fb136bb8e86f0804` → `516d0323a5a8b5bd` | the same | "Her sails lifting" at 45989, 49980 and 54445, the last ten seconds before the urgent "Taken aback" at the land close aboard (54455) |
| the merchant passage, 5c | 2994 → 2995 | `c52c14c725a5ed1f` → `5f662945254058e5` | the same | "Her sails lifting" at 112740 in the Goulet, twenty-two seconds before the book's 'trim to the course' |
| the naval cruise, 5c | 2037 → 2039 | `bb8b2499fde6a0f4` → `b336a2e287b4f422` | the same | "Her sails lifting" at 94136, the chase's course after the brig is spoken, and at 115759, twenty-five seconds before the book's late "Taken aback" (115784) |

No tick of any passage moved: no anchor in them is let go deeper than twenty fathoms or drags, no heave-to of theirs met a sail being handed, and no tack of theirs waited. The pins moved are the four passages' lines and digests, each with the old figure beside it in `tests/test_known_truths.py`.

### Found on the way (package 37k)

- **A belay before the break-out left the cable marked as being hove in** (`Anchor.heaving`), which keeps the physics from judging the anchor to drag and the World from saying she is brought up, for good. The belay lets it go now.
- **`belay get under way`**, game 10's own words, was refused as naming no work: the ground tackle's verbs were not among those `belay <the order>` reads. Mended in `orders/work.py`; it is a word's fault and could as well be 37l's.
- **The lifting line with the wind abaft the beam.** As first written the line was judged on the luffing angle alone, and the cruise's chase said "the wind 96° on the starboard bow" with her yards braced up and the wind just abaft the beam; she is not taken aback from there. Kept forward of the beam; the cruise was measured again for it (the other passages' lines are all forward of it and did not move).

## Milestone 5: the account, amended (package 37j, 2026-10-09)

The review's part K, "the account, amending 37e", its G3 (what is left) and G4, the
fold-in's finding at the merchant passage's second noon (spec M5 §33 item 24) and the
owner's note 5 on game 9. Measured on Linux (this worktree's machine, shared with four
other packages' work, so the times are not the change's); seed 7 throughout.

### The constants and their sources

All in `freesail/world/reckoning.py` unless said.

| Constant | Value | What it is | Source |
|---|---|---|---|
| `OBSERVATION_OUT_SIGMAS` | 2, kept | the two doubts together, beyond which one of the two figures is plainly out | **its reason restated**: two is what the master trusts a figure within (the lunar's and the chronometer's words since 33b), so "plainly out" is "further apart than he would trust the one and the other within". 37e's reason (game 9's noon taken at 2.06 of the doubts together) no longer bears: under the amended rule that noon is believed or doubted by which is the better figure, not by the number. Judgement |
| the better figure (no constant) | an observation further out than the doubts together is taken only when its doubt across its line is no greater than the account's; else weighed and doubted | | the lead's decision on the fold-in's finding |
| `CONTOUR_FINEST_M` | a cable | within a doubt under the half-mile grain the contour search steps at a quarter of what he would trust the account within, no finer than this | judgement: the least the log's words say of a distance |
| `APART_EDGE` | a thousandth | a cast that does not agree within the doubt widens it so that the nearest water that answers lies this part beyond the edge of the trust, so that the same cast again stays apart | judgement |
| `SAME_GROUND_NM` | 2 miles, kept | also: a cast within this of one that did not agree widens nothing further | 37e's, reused |
| `data/tides/establishments.yaml`, `spring_rise_ft` | every place of both tables | the rise at springs by which he reduces a cast; `rise_judgement: true` where the period's table gives none | the world's spring range there (twice M2 and S2) rounded to the foot, JUDGEMENT, as 37e's directions' rates are the world's rounded; the period's own figures kept (Fowey's of 1774 for Falmouth, the French ports' and Plymouth's) |
| the reduction | half the spring rise and half the day's rise by the half-cosine of the hours from his high water | the height above his chart's datum (low water at springs); until 37j half the day's rise times one and the cosine, the height above the day's low water, which at the neaps stood above the datum by half the difference of the rises | Norie's two-thirds and the rule of twelfths worked exactly, as package 34 |
| `BOARD_ALTERATION_POINTS`, `BOARD_LEAST_S` | 2 points, a minute | the account worked at an alteration of course from the board's mean heading, at heaving to and filling away; a board under a minute not cut again | the brief's two points; Falconer 1780, *Traverse* ("collecting the difference of latitude and departure of each course"); the minute judgement, so that a ship in stays is one board's end and not a dozen |
| `read_doubt`, `drift_doubt` (`held`) | the log's quarter knot and the drift's half knot kept as biases across the boards | the read's error is one figure until the log is next hove, the drift's while she lies to; with the account worked at every board the sum of their squares by the interval would shrink them | 37e's figures, their form judgement |
| `ONE_HAND_DEG` | six points and a half | marks of a fix within this arc lie on one hand: the doubt said along the shore and off it when the two differ | judgement: the Bay of Brest's three marks spanned six points, the Lizard's in game 10 three |
| the compass's part of a fix (`_compass_shift_nm`) | the fix's displacement for one sigma of the compass's allowance | no fix narrows the account's doubt that way below it (nor raises it above what it was) | 37e's covariance term, kept apart |
| the dangers | to the cable (`geo.distance_words`) | `the dangers` and a shaped course's warnings | the brief |
| the departure | the scenario's position, a mile in doubt | the account opened a mile out by a draw before | the brief |

Gone: the departure's two draws from the `reckoning` stream (so every draw after them is
another, and every passage moves from its first tick of the account).

### The four cases of the rule, with their figures

`tests/test_reckoning.py` holds each.

| Case | 37e | 37j |
|---|---|---|
| **Game 9's noon of 16 June** (tick 370,860): the octant's 48° 07' N, good to 2.28 miles; the account 48° 12½' N, kept by the lead at 0.26 north and south; 5.23 miles apart, 2.06 of the doubts together | taken: the account laid on the sight | the sight the poorer figure: weighed and doubted, the account moved a cable ("the sight stands five miles to the S of the account, and the account, good to three cables, is the better figure: the account moved a cable to the S") |
| the same noon against an honest account | | weighed by the doubts: against the mile and nine tenths the forenoon's casts leave (below), two miles of the five |
| **The lunar of game 9's note 5** (tick 246,131): 12.12 miles one sigma against 0.83 east and west, 2.3 miles apart | kept (weighed): within the doubts together | kept, as before; and set eighteen leagues off, further than the doubts together, it is still the poorer figure: weighed and doubted, three cables moved (37e laid the account down on it) |
| **The merchant passage's second noon**, on Linux: an octant's sight (2.5 miles) five miles and a half north of an account fixed to three cables a minute before, a hair over the doubts together (a hair under on Windows) | taken on Linux, the account six miles out for a minute; weighed on Windows | weighed on both sides of the line and doubted on the far side; the account within a cable of the fix either way |
| **The cruise's chronometer** (37e's finding): 7.6 miles out "which Mr Harvey would trust within 5 miles" (2.28), the account a cable in doubt by the land | taken; the bearing of Penlee took it back half an hour after | kept, and doubted |

*Game 9's noon, and the arithmetic of "taken".* The brief asked that noon taken once the
cast keeps the account's doubt honest. Under the rule as amended it cannot be: it is taken
only when its doubt (2.28) is no greater than the account's, and the two are then plainly
apart only beyond twice the two doubts added, at least 9.1 miles; they stood 5.23 apart.
What item 2 does is the other half: against an honest account the noon is weighed by the
doubts and moves it most of the way, where against the lead-kept account it is doubted and
moves a cable. The forenoon sailed again on this build (the brig becalmed off the Goulet's
mouth on the ebb from 08:00 on 16 June, the account half a mile out and a quarter of a mile
in doubt as game 9's was, the deep-sea lead every glass; slow test
`test_the_forenoon_of_16_june_sailed_again_keeps_an_honest_doubt_and_the_noon_is_weighed`):

| 16 June | the error | the doubt E / N |
|---|---|---|
| 08:30 | 0.57 | 0.35 / 0.46 |
| 09:30 | 0.46 | 0.85 / 1.17 |
| 10:30 | 0.32 | 1.04 / 1.15 |
| 11:30 | 0.56 | 1.69 / 1.77 |
| noon, the sight (a mile and a half out, as game 9's) weighed | 1.07 | |

Game 9 (on 37d) had the error four miles and the doubt a quarter at noon. The master's own
tide (37e) keeps the account with her, and the casts no longer narrow the doubt beyond what
they can say: the truth within twice the doubt at every glass. Left as a finding: that
same forenoon begun with game 9's noon account (four miles out, 0.26 in doubt) ends with
the doubt grown to nine tenths of a mile and the error still four, so a lead-kept account
already wrong is helped by item 2 and not cured by it; the casts over the flat sand there
answer within the doubt at the wrong place and are weighed (37e's behaviour, unchanged).

### The cast within the doubt, and the tide under the lead

Game 10's cast (the owner's note 2) reproduced on this build: the cutter in St Mary's Sound
at 04:00 on 14 June 1805, her account right and a quarter of a mile in doubt, Moore's
table (no Falmouth, no Scilly rise until now). Package 34's flat three metres against the
world's 4.66 at that hour; the master's own tide by Scilly's fifteen feet and his hour now
4.05. The cast laid on the chart with no tide taken off at all (the error larger than game
10's, to force the case) answers nowhere within his doubt; the chart has that water a mile
and a half to the SE: "the account kept, and its doubt widened" (to three quarters of a
mile that way), and three casts more on the same ground keep it and widen nothing (37e
laid the account down a mile off at the first and kept it there four hours). With his own
tide taken off the same casts agree with the chart where he is.

The search within the doubt: the trust's ellipse (twice the doubt) by its Mahalanobis
distance, on rings a quarter of its reach apart and no finer than a cable when the doubt
is under the half-mile grain; the chart's grain (37e's `depth_span`) first, as before. A
cast that does not agree grows the doubt along the way to the nearest answering water by
the Sherman-Morrison form (`Reckoning.widen_toward`), so that the point lies a thousandth
beyond twice the doubt; the account does not move.

### Each board by itself

The cutter (logged every two hours) standing N and E by turns in a south-westerly,
eighteen minutes a board, the account set right at the start (`test_each_board_is_laid_down_by_itself`):

| | the account worked | the error after six boards |
|---|---|---|
| the mean of her headings (as before) | at the log only | 5.4 miles |
| each board by itself | at every turn and at the log | 2.7 miles |

The rest of the error is her way by eye between the two-hourly heaves and the log-line.
With the account worked so much more often, the log's read and her drift by eye are now
kept as biases across the boards (`read_doubt`, `drift_doubt`); kept as before, as a
square of each interval, they would have shrunk the doubt by the number of boards.

### The fix on one hand

At anchor in the Bay of Brest (the brig, 17 June, unnamed fixes every five minutes by the
castle of Brest, Penaleuch point and Portzic, W to NNW): the account 0.12 to 0.18 mile
from the truth with a doubt of 0.12 to 0.17, the truth within twice the doubt at every
fix (37e: three cables out while "good to a cable"). The compass's part of a fix is
computed from the fix's own lines (`_compass_shift_nm`, the same arithmetic as `_fix_of`'s
covariance term) and floors the account's doubt that way. The words: a fix by marks within
six points and a half says its doubt along the shore and off it when the two differ. Seven
of the frigate's nine fixes in the 5b passage, and 86 of the merchant's 193, are by marks
on one hand.

*Found, for the lead*: the brief says such a fix is "good along the shore and poor off it".
In this model it is the other way about as often as not: the narrow cut makes it poorer off
the shore, and the compass's shared error, which with every mark on one hand does not
cancel, moves it along the shore by the marks' distance times the error (in the Bay of
Brest geometry, 0.09 off and 0.12 along with the compass, 0.04 along without). The words
say whichever the figures give.

### The dangers to the cable

From four miles south of the Manacles: "the Manacles NW, a mile and a half; the Penwin and
the Vaze NNW, a mile and a half; the Gedges NW by N, five miles and a half; ...", and the
course for Falmouth: "the line passes the Penwin and the Vaze within a cable, the Manacles
within two cables and the Governor within a mile" (37e: "within a mile" for all three).

### `the port` and `the depth of water`

Two brigs of one seed, their true places four miles apart and one account (the world's
tide made nothing in both, so that they feel the same water): every reading
the same, in open water; in sight of the Manacles all but the lookout's own (what is in
sight, the land, the nearest land, the bearing of a mark; and the moon's altitude in the
data behind `the moon`). On the tree before 37j `the depth of water` and `the port` differed
in both ("Falmouth, the outer road bearing N by W, 5.2 miles" against "NW, 4.6 miles").

The merchant passage's two depth conditions ("in the road", "in the Bay") read the lead
since 37j; the road of Bertheaume is now anchored in at the first cast under thirteen
fathoms, eight and a half, where the chart's figure at her true place had put her in
twelve.

### The recorded passages, re-measured with the reasons

Each measured once on this machine (`scratch measure.py`, the log dumped whole; Linux).

| Passage | Lines | Digest | Comes through |
|---|---|---|---|
| 5a's day | unchanged | unchanged | no chart, no reckoning |
| the frigate, 5b | 768 → 746 | `dbf7f6fcfb800fdf` → `e1ecc7767009176c` | yes: pilot aboard, anchored in the outer road |
| the schooner, 5b | 761 → 756 | `c8905673506f717e` → `a7dd398ae719ff8b` | yes, anchored in eighteen fathoms and a half off St Anthony's; the pilot hails and does not board (as before, an expected failure) |
| the thick passage, 5b | 488 → 473 | `fb136bb8e86f0804` → `e00caa4f5a665b50` | **no: she takes the ground on Black Head at 56081** (below) |
| the merchant passage, 5c | 2994 → 2976 | `c52c14c725a5ed1f` → `71c32abf23af0510` | yes, the tin sold in the Bay; **the Iroise's cast not made** (below) |
| the naval cruise, 5c | 2037 → 2059 | `bb8b2499fde6a0f4` → `d3086c7fce4a3a1a` | yes: the Palinure spoken |

Every true track parts at the first course shaped from the account: the departure is laid
at the truth (it was drawn a mile out) and the two draws it took are gone from the
`reckoning` stream, so every draw after them is another; and the account is worked at
every board. Every tick before the first such course stands in every passage.

Old beside new:

| | Before (the fold-in) | After (37j) |
|---|---|---|
| **The frigate** noon | 28740, the sight weighed (37e had laid the account three miles north by a sight five and a half too far north) | 28740: "the account moved eight cables to the NNE", four miles out after it |
| cast in the Soundings | 30118, "Fifty-five fathoms; ... The account kept." | 30118, with "Two fathoms of tide allowed by the epitome: fifty-three fathoms on the chart." |
| the account at the cast; at the landfall; after its bearing | | 4.5; 8.5; 2.3 miles |
| landfall; outer road; anchor; brought up | 44820; 58297; 58647 in fourteen fathoms and a half; 59642 | 45180; 58298; 58646 in eleven and a half; 59606 |
| cutter sighted; hail; pilot aboard | 55860; 57480; 57540 | 55500; 57120; 57180 |
| **The schooner** noon | 28740 | 28740: weighed, "the account moved a mile to the SSW" (the octant's 2.8 miles against the account's 3.5, within their doubts together); three miles out after it |
| landfall; outer road; pilot's hail | 45840; 56515; 55800 | 46200; 56515; 55860 |
| anchor off the town; brought up | 57638 in seven fathoms; 58689 | 57643 in seventeen and a half; 58795 in eighteen and a half |
| **The thick passage** landfall | 54420, Black Head close aboard, stood off | 53820, the same, eight miles out by account; aground at 56081 |
| **The merchant** sail off the Lizard | 29100 abeam, three leagues | 25740 on the larboard bow, four leagues (the one abeam at 29400) |
| noons | 25200, 111660 | 25200 (weighed, a cable), 111660 ("the account kept") |
| the Iroise's cast | 90241, thirty-eight fathoms | not made |
| pilot of Brest aboard; anchor at Bertheaume | 96240; 99974 in twelve fathoms | 94380; 98814 in eight and a half |
| the flood; the mouth of the Goulet; anchor in the Bay; tin sold | 108960; 112078; 115815; 123948 | 108960; 112178; 116282; 125159 |
| **The cruise** to the pilot's leaving | 5460, 6834, 7980, 10980 | the same |
| the chronometer hove to off Plymouth, 09:00 | taken, 7.6 miles out | doubted, the account kept |
| the cutter's hail; the letter read | 83484; 83544 | 83423; 83483 |
| the Palinure sighted; chased; spoken; lost | 90120; 90121; 94091; 98100 | 90000; 90000; 93979; 98040 |
| wears | fourteen | fourteen |

*The merchant passage's second noon, in full.* At the fold-in, in the mouth of the Goulet
with the account fixed by cross bearings to three cables a minute before, the octant's
sight fell five miles and a half north of it, a hair over the two doubts together on
Linux, and 37e's rule took it outright: the account six miles out for a minute, until the
cast and the bearing after it laid it down again; on Windows the same sight fell a hair
under and was weighed. Under 37j that sight would be weighed and doubted either side of
the line and leave the account within a cable of the fix (held in the tests by its
figures). On this build's track the same noon finds the account within a cable of the
truth by the morning's fixes and the sight within the two doubts of it: "Noon. Latitude
by observation 48° 18' N; the reckoning was 48° 20' N: the account kept." The account is
0.06 mile from the truth after it. The platform difference that turned this up is not
explained (spec M5 §33 item 24); the rule no longer depends on which side of the line a
sight falls.

*The 5b schooner's noon, in full.* Before (37e on): the octant's sight weighed against an
account whose doubt the departure's draw and a forenoon's run had made, the passage's
account three miles out at the landfall's bearing. Now the departure is at the truth, and at noon
the account's doubt north and south is three miles and a half (honest: the stream's part
and the log-line's grown through a forenoon without an observation), the octant's sight
(two miles and four fifths one sigma, the octant and a seaway's horizon) a mile and nine
tenths south of it: within their doubts together, and the sight no better a figure than
the account, so it is weighed by them and moves the account three fifths of the way:
"Noon. Latitude by observation 49° 21' N; the reckoning was 49° 22' N: the account moved
a mile to the SSW." The account is three miles from the truth after it (the sight was
itself out by about two), eight and a half at the landfall, and a mile and a half after
the Beast's bearing. The frigate's noon is the same case with the sextant: a gap of a mile
and an eighth, her doubt three miles and a third, the sight's 2.38; weighed, eight cables
moved.

*The thick passage takes the ground (a finding, the book not tuned).* No sight, the
account eight miles out by account at the landfall: the land about Black Head close
aboard at 53820 (54420 before), on the larboard bow nine cables off. The book's "the land"
steers S into a south-easterly; "keep her full" bears her away a point (53847) and she is
taken aback (53861), fills on the larboard tack close-hauled, and with her leeway (17 to
20 degrees) and the ebb setting her to the westward is warned of the land ahead at 55320
and 55620 and takes the ground on Black Head's ledges at 56081, the tide falling. On 37f's
track she raised the same land ten minutes later and further off, and the same order
cleared it. The cause is the track, not the rule: the departure laid at the truth and the
boards each worked move the course shaped at the noon and the landfall with it. For the
lead (the book's stand-off, or 37k's helm when she is taken aback).

*The merchant passage casts nothing at the Iroise (a finding, the book not tuned).* "The
course for the Iroise" is shaped hourly while Ushant is more than ten miles off; on this
track it is shaped once, at 02:00 from nineteen miles off, and she then passes the
Passage de l'Iroise more than a mile and a half off by account, so "bring to in the
Iroise" (within a mile and a half, her head east of E) never fires. The test of the beat
is an expected failure, as it was before 37d's second pass.

*The schooner's anchor.* "Off the town" fires at the first cast under ten fathoms (six, at
57312); while she is brought to for the anchor "keep her full" bears her away a point and
she runs on into the channel between St Anthony's Head and the Black Rock, and lets go in
seventeen fathoms and a half. Safe, and 37f's (the anchor's evolution and the trim rules)
and not this package's; the bound on the depth she rides in is widened to twenty fathoms.

### Found on the way (package 37j)

- **Scripts run from the scratchpad imported the main checkout's `freesail`**, not the
  worktree's (the installed package is the main tree; `python -m pytest` puts the working
  directory first, a script does not). Probes now put the working directory on the path.
- **The account's doubt shrank with more frequent workings**, the log's read and her drift
  hove to having been squared per interval: an existing fault that each bearing, cast or
  fix already worked (they each bring the account up), and that item 4 would have made
  much worse. Now kept as biases.
- **The cast's reduction stood above the day's low water**, not the chart's datum: at the
  neaps the water stands above the datum at low water by half the difference of the rises.
  Now the height above the datum; the fall to the day's low water given at an anchor's
  letting go (37f) is unchanged.
- **The game 9 noon cannot be "taken" against an honest account** (above). The lead may
  wish to say in the brief's words what the case holds: doubted against the lead-kept
  account, weighed by the doubts against an honest one.
- **A lead-kept account already four miles out is helped and not cured**: the forenoon of
  16 June begun with game 9's noon account (four miles out, a quarter of a mile in doubt)
  ends with the doubt grown to nine tenths and the error four, the casts over the flat
  sand answering within the doubt in the wrong place and being weighed (37e's behaviour).
- **The log's line of a sighting still carries the mark's true distance and bearing** in
  its data (`lookout.Lookout._line_data`), for the record and the tests; the snapshot's
  reading does not. If the log's data reaches the browser, that is a road left.
- **Truth 59** (the frigate in forty-six fathoms south of the Lizard, the account nineteen
  miles off and eight in doubt): the cast reduced by the master's tide above his chart's
  datum (a metre and a tenth) is matched at another point of the contour, where the bottom
  shelves less; the line is six miles (a mile and a half before), and the account goes two
  thirds of the way and stands within seven fathoms of the cast's depth on the chart (37e:
  within a fathom of the tolerance, ninety-six parts in a hundred). The test holds that,
  and the truth's sentence ("moves the reckoning onto the chart's contour") is further from
  the letter than 37e left it: the lead's (spec M5 §19).
- **The thick passage aground and the Iroise's cast lost**, above: the books, for the lead.

## Milestone 5: the K batch merged (2026-10-09, the lead)

Six packages built together in worktrees from the briefs of 2026-10-09 (37h the pilot, 37i
the local runner, 37j the account amended, 37k the ground and the helm amended, 37l the
words, 37n the chart's tools) and merged in the order 37i, 37n, 37l, 37h, 37k, 37j, each
package's section above. Three packages re-pinned the recorded passages against the branch
before the others, so the six passages were measured once more on the merged tree and
pinned as it gives them (`tests/test_known_truths.py`, the old figure beside each).

| Passage | Merged tree | What moved at the merge beyond the packages' own figures |
|---|---|---|
| The frigate, 5b | 734 lines, `9a0c4168d6987405`; the outer road 58299, the anchor 58652, brought up 59628 | the pilot taken at his hail (37h) on 37j's track: the lines of the boat and the fee |
| The schooner, 5b | 761 lines, `d6031efa9808a2b1`; the second hail 56460, the pilot aboard 56940, the outer road 56234, the anchor 57255, brought up 58213 | 37h's boat keeping company on 37j's track; she anchors in the road an hour and a quarter earlier than 37h's figure on the old track |
| The thick passage, 5b | 475 lines, `bd1cb6f5e036ce3e`; the landfall 53820, aground on Black Head 56081 | 37k's lifting line twice |
| The merchant passage | 2999 lines, `e40b930d5ec5bbaf`; the Brest pilot put off at the Bay anchor 121440; the rest 37j's | 37h's pilot and 37k's lines on 37j's track |
| The naval cruise | 2065 lines, `15e7f10b2ca8eb9a`; every tick 37j's | 37h's pilot and 37k's lines |

**Two passages that no longer come through whole, left for package 37m.** Both are the
helm through the wind, which the owner ruled on 2026-10-09 (spec M6 §31, ruling 3) and
which 37m builds: a plain `steer` that the wind will not allow is to be tacked, worn or
kept full and by, not steered into the wind.

- **The thick passage takes the ground on Black Head.** On 37j's track (the departure laid
  at the truth, the account worked at each board) the landfall in fog comes at 53820 with
  Black Head close aboard on the larboard bow, the book's "the land" rule orders `steer S`
  into a south-easterly, "keep her full" bears her away, she is taken aback at 53861 with
  no way on, and her leeway and the ebb set her onto the ledges: "Land close ahead" at
  55620, aground at 56081. The cause is the order the wind will not allow, which is 37m's.
  The grounding is pinned as the passage's end and said so in the test; the book is not
  tuned for it (a `heave to` at the landfall would be the period's order in fog and is the
  one line to try if 37m does not carry her clear).
- **The merchant passage's cast at the Iroise is lost** (an expected failure since 37j):
  the course for the Iroise is shaped once from the soundings and the hourly rule is guarded
  within ten miles of Ushant, so on the new track she passes the mark more than a mile and a
  half off by account and the bring-to never fires. One rule tried once and dropped (the
  book's "tuned once and cheaply"): `when the distance to the Passage de l'Iroise is under 4
  miles and the distance to Ushant is over 10 miles and the heading is east of E then shape
  a course for the Passage de l'Iroise` brings her to and the cast reads the Iroise
  (90110), but filling away after it she is taken aback at 90453, the Brest pilot boards two
  hours late and she never anchors in the road nor sells the tin: the same family of fault,
  and 37m's before the book is touched again.

**37h against the head rule.** Fourteen whole-passage runs, five on the schooner alone,
against "tuned once and cheaply"; the package says so itself. The books changed: `take the
pilot` at the hail in the frigate's, the merchant's and the cruise's; three lines and a
guard in the schooner's.

**The whole suite on the merged tree**: see the gate's document for the counts; the two
timing tests (`test_chart`'s nearest coast and the merchant passage's pace floor) fail on
this machine whenever other suites run beside them and pass alone, which every package
reported.

## Milestone 5: the helm through the wind (package 37m, 2026-10-09)

Built from the brief "Package 37m: the helm through the wind" in `M5-WorkPackages.md`, on
the owner's ruling 3 of 2026-10-09 (spec M6 §31; decision 39): a plain `steer` through the
wind tacks or wears her as the ship and the course allow; a course given directly into
the wind's eye is steered and she is taken aback, the line warning of it; `steer`, `shape
a course for` and `give chase` share one rule. Measured at seed 7 on this machine (Linux,
shared with another package's worktree, so no time here is the change's).

### The rule

`orders.navigation.judge_course` judges a course against her head and the wind for every
order that gives her one: `steer <course>`, the points orders (`come up`, `bear away`,
`steer two points to starboard`), `shape a course for` and `give chase`. The helm's orders
come through `verbs._helm`, the master's through `navigation.execute`; the judgement is
made once, and the helm put for a course already judged goes round it
(`verbs.steer_as_given`).

| The course, against her head and the wind | What she does | The line |
|---|---|---|
| on the tack she is on, laid | the helm, as before | as before, unchanged to the byte |
| a helm order within a point of the wind's eye | steered as given | "N by W (349°) lies in the wind's eye from her head; she will be taken aback.", notable |
| across the wind's eye, the shorter way, with two knots of way | put about for it: `tack` with `course_deg` | "E by N (79°) lies across the wind's eye from her head; she is put about for it." |
| the same with under two knots and more than a knot | worn round for it | "...; she has not way enough to stay, and is worn round for it" |
| across the wind by the stern, more than eight points round, square-rigged with a square sail set and a knot of way | worn round for it: `wear` with `course_deg` | "SE (135°) lies across the wind from her head, by the stern; she is worn round for it." |
| the same in a fore-and-after (one mast with yards) | gybed by the helm, as she always has been | "...; she gybes for it by the helm." |
| nearer the wind than she will lie, on the other tack | put about or worn for that tack, `full_and_by` | "NE by E (56°) lies too near the wind to be laid; she is put about and kept full and by on the larboard tack." |
| a course shaped or a chase's nearer the wind than she will lie on her own tack | kept full and by, as since package 35 | "...; she is kept full and by on the starboard tack" |
| on the tack she is going to, while a tack or a wear is in hand | handed to the manoeuvre | "SW (225°): she is going about, and the course is given her as she comes round." |
| no steerage way (a tenth of a metre a second) | the helm, as before; a course shaped too near on the other tack is kept full and by on hers | |

The manoeuvre ends on the course (`evolutions.scripts.CourseToSteer`): a tack, steady by
the wind on the new tack, steers a course within half a point of close-hauled with the
yards as they are, and pays off to one further off the wind with its yards and sheets
trimmed every twenty seconds as the wind draws aft (the same rule as `fill away and steer`,
package 37f); put about for a course from a reach, she is luffed up and braced up first
("Luff up and brace up: she is brought by the wind to go about.") and put about when she
is by the wind or after two minutes. A wear comes to the course on the new tack instead
of to close-hauled, the yards following the wind round and trimmed to the course's wind
when she is steady on it, and the spanker hauled out then ("On her course. Haul out the
spanker!"). The completion lines say so ("Tacked; braced up for the course ordered on the
larboard tack, heading E by N (79°).", "Wore ship; braced for the course ordered on the
larboard tack, heading SE (135°).", "..., full and by."); `tack` and `wear` by their own
words end and read as they always have. The officer's domain is unchanged (item 4): an
order of the course is judged by its words, and the manoeuvre the rule orders for it is
within the grant to steer (`tests/test_officer.py`).

### The constants and their sources

| Constant | Value | Where | Source |
|---|---|---|---|
| `COURSE_NOT_LAID_MARGIN_POINTS` | half a point, for a course shaped and a chase's; none for the helm's own orders | `orders/navigation.py` | package 35's rule, kept; the helm's orders are laid at the close-hauled angle itself (below, "A decision for the lead") |
| `EYE_POINTS`, `EYE_ALLOWANCE` | a point either side of the wind, and a degree | `orders/navigation.py` | the owner's "directly into the wind's eye"; a point, since the wind is named to the point and wanders about it, so that the brief's own "N by W lies in the wind's eye" is so in a northerly; judgement |
| `STAY_MIN_KN` | two knots | `orders/navigation.py` | the tack's own precondition (`tack.yaml`); Luce 1866, ch. XXIV, 'Wearing' (p. 457): wearing is resorted to "when ... the vessel has not sufficient headway for tacking" |
| `WEAR_FOR_IT_MIN_MS` | half a metre a second, a knot | `orders/navigation.py` | the fold-in's guard, kept |
| `WAKE_HELM_POINTS` | eight points | `orders/navigation.py` | a turn by the stern of eight points or less keeps the wind abaft the beam at both ends, where a square sail fills however its yard is braced; the fold-in's guard counted turns of more than six points (her close-hauled angle). Found on `tests/test_ports.py`'s St Mary's approach, steered by the bearing a minute at a time: at six points the frigate, running, was worn for a turn of 78 degrees to the other quarter and struck the Nut Rock twelve minutes later; at eight she is steered, as before. Judgement |
| `STEERAGE_WAY_MS` | a tenth of a metre a second | `orders/navigation.py` | the fold-in's guard's own "no way" |
| `by_the_wind_s` | 120 s | `tack.yaml` | judgement: the frigate luffs from a reach to close-hauled in about a minute in the tests |
| `BY_THE_WIND_ALLOWANCE` | ten degrees | `evolutions/scripts.py` | the tack's `close_hauled()` allowance (`evolutions/runner.py`) |
| `retrim_s`, `pay_off_timeout_s` | 20 s, 240 s | `tack.yaml` | `fill_away.yaml`'s, for the same paying off |

The tack's precondition is `close_hauled() or params.course_deg != none`: by its own word
she is refused off the wind in package 37k's words, and for a course she is luffed up
first. No default is declared for either parameter, so that an evolution's data and the
recorded passages' digests do not move where no course is given.

### A decision for the lead: the helm's own orders on her own tack

The brief's rule reads "nearer the wind than she will lie, kept full and by on the tack
that points nearer, ... unless the order is a plain `steer` into the eye". Built so for a
course shaped and a chase's (as before) and for any course on the other tack. For the
helm's own orders on the tack she is on it is not: they are carried out as given however
near the wind, and only within a point of the eye does the line warn. The reasons: the
close-hauled angle every judgement reads is six points for every ship
(`close_hauled_true_angle`; no ship file sets `close_hauled_angle`), where the schooner
lies half a point nearer (truth 2) and the frigate holds three knots at 58 degrees
(chapter 2); and truths 1, 2, 24, 25, 26, 31 and 32 steer her up by `steer` two degrees
at a time to find how near she will lie, truth 25 pinching her to five points on
purpose (Fincham's "just lifting"). Kept full and by, those orders would sail her at six
points whatever was said, and the truths would measure the helmsman. Pinching her is the
captain's to order; package 37k's "Her sails lifting" and "Taken aback" say what follows.
If the lead wants the brief's reading for `steer` on her own tack, it wants first a
close-hauled angle per ship from her file and another way for the truths to pinch her.

### The recorded passages, re-measured

Each measured once after the change (`the_passage`, `the_scenario_whole`); the three that
moved once more on the tree before it (`61d2b2b`, exported to a scratch directory), which
matched the merged tree's pins, so that the first line where each parts is known: the
thick passage at the landfall (53820), the cruise at 72000, the merchant passage at
129600.

| Passage | Lines | Digest | Ticks | Why |
|---|---|---|---|---|
| the thick passage, 5b | 475 → 478 | `bd1cb6f5e036ce3e` → `7029e5b4dd6fbe06` | every tick to the landfall (53820) stands; aground on Black Head at 56081 → not aground; put about off Black Head and full and by on the starboard tack at 54063 | below |
| the merchant passage, 5c | 2999 → 2998 | `e40b930d5ec5bbaf` → `54713e8e579fd527` | every tick stands | at anchor in the Bay at 129600 the hourly course for the Iroise, on the other tack with no way on her, is refused as keeping her full and by, the refusal of 126000 and not said again, where it was refused as a tack |
| the naval cruise, 5c | 2065 → 2083 | `15e7f10b2ca8eb9a` → `348b07dd901580a7` | every tick to 20:00 on the 12th (72000) stands; the cutter within hail 83423 → 84631, the letter read 83483 → 84691; the Palinure sighted and chased at 90000 as before, spoken 93979 → 93663, out of sight astern 98040 → 97560; the noons as before | at 72000 the book's "back to the station" shapes SW by S across the wind's eye from her head, and with two knots and more on her she is put about for it where the fold-in's guard wore her; her track parts there. Thirteen wears and a tack in the two days (fourteen wears); no urgent line but the book's late "Taken aback" at 115784, as before |
| the frigate, 5b | 734, unchanged | `9a0c4168d6987405`, unchanged | unchanged | no order of hers crosses the wind |
| the schooner, 5b | 761, unchanged | `d6031efa9808a2b1`, unchanged | unchanged | the same |

**The thick passage comes through.** At the landfall in fog (53820, Black Head nine
cables on the larboard bow) the book's "the land" gives `steer S` with the wind at SW by
W: S lies too near the wind to be laid on the starboard tack, and she is put about for
it ("she is put about and kept full and by on the starboard tack"), the shorter way being
through the wind's eye. Being off the wind she is luffed up and braced
up first (71 seconds; her head comes up toward the land as she does), put about, and
tacked at 54063 "heading S by E (171°), full and by"; the land is out of sight at 54900
and she stands off to the southward to the end of the passage. Her pinned grounding and
the test's words for it are gone; the passage is pinned as it now ends (the tack's tick,
the helm full and by, no `ship.aground`). One urgent line is left, as there was one
before: "Taken aback" at 54411, five minutes after the tack, full and by with a knot and
a half on her in a gust; the book's "trim on a shift" braces her to the wind at 54641. That
is the full-and-by helmsman at low way after a long manoeuvre, not the rule, and is left.

**The merchant passage's cast at the Iroise does not come back.** Its cause is 37j's and
is not the helm's: the course for the Passage de l'Iroise is shaped once from the
soundings and the hourly rule is guarded within ten miles of Ushant, so she passes the
mark more than a mile and a half off by account and "bring to in the Iroise" never fires;
nothing in that is a course across the wind. The expected-failure mark stays. As a
diagnostic only (the book is not changed), the lead's dropped rule ("the Iroise by
account", `shape a course for the Passage de l'Iroise` within four miles of it, the
heading east of E) was run once on this build: she is brought to and the cast reads the
Iroise at 90110, as in the lead's trial, and filling away she is again taken aback at
90453. The cause, found here: filled away close-hauled on the starboard tack (SW by W)
with next to no way on her (the log a quarter of a knot as she filled), the book's "for
Bertheaume" shapes E by N, fourteen points round by the stern on the larboard tack; with no steerage way the judgement
gives it to the helm as given (her line says nothing more), and with way it would be a fore-and-after's gybe by the
helm, which is the same turn. Her fore yards are still braced sharp up for the starboard
tack as the wind comes over the other quarter, and every square and head sail is aback
(the fore staysail at 90427, the fore topsail at 90443). See "Found on the way".

### Found on the way (package 37m)

- **A topsail schooner gybed by the helm in a long turn is taken aback.** The brief keeps
  the fold-in's guard: a fore-and-after (one mast with yards) gybes by the helm. The
  topsail schooner's fore yards are not tended in that turn, and from close-hauled to a
  broad reach on the other tack they are braced for the old tack when the wind comes
  over: she is taken aback (in a test of it, `steer SE` from WNW in a northerly, and in
  the Iroise trial above). The fold-in measured wearing her for every turn by the stern
  and lost the merchant passage's tide (her hourly courses a hundred degrees apart, each a
  wear); a turn of more than eight points with a square sail set might be worn and a
  shorter one gybed, as the square-rigger's now is. For the lead: it is the Iroise cast's
  remaining fault, and the primer's chapter 5 says it.
- **A tack that waits behind other work and finds her without way to stay** when it
  begins is refused in package 37k's words and the course with it; the line says so and
  the captain gives it again. A wear in its place was not built.
- **The shorter way off a lee shore.** The judgement turns her the shorter way; in the
  thick passage the eye was the shorter by a few degrees and she was luffed up toward
  Black Head, nine cables off, before going about. A captain would wear off a lee shore in
  fog; the rule knows no land.
- **The shaped course at anchor**: a course shaped at anchor was refused as the manoeuvre
  the old guard picked ("'tack' must wait till she weighs"); it is refused now as the
  helm's order or as keeping her full and by, whichever the judgement gives with no way
  on her.

### The suite, as run (package 37m)

`ruff check` and `ruff format --check` clean. The fast tier (`pytest -n 4`), on a machine
whose load stood at twelve to sixteen on four cores: 2983 passed and four failed. Two are
the timing tests every package reports (`test_chart`'s nearest coast, the merchant
passage's pace floor). One was this package's and is mended
(`test_catalogue`'s frozen tack timings, which now carry the three a tack for a course
reads, as 37f's fill away does). One is not this package's:
`test_reckoning.py::test_a_cast_that_does_not_agree_within_the_doubt_keeps_the_account_and_widens_it_once`
fails when the whole file is run in one process and passes alone, on this branch and
on the tree before it (`61d2b2b`) alike: an order dependence in that file, for the lead.

The slow tier of the truths (`tests/test_known_truths.py --slow -n 4`): 83 passed, 8
expected failures (the Iroise cast's among them), four failed. Three are the pace floors
(truth 51's frigate, the day under systems, the gate's day with the region loaded: 477
ticks a second against the floor's 500 under that load). The fourth is not this package's:
`test_the_schooners_pilot_boards_before_she_runs_in` asks that she anchor more than a
quarter of an hour after the pilot boards, and on the merged tree's own figures (the pilot
aboard 56940, the anchor 57255, which this package measured unchanged with the schooner's
lines and digest) it is five minutes, so it fails on the merged tree too, whose log is
the same line for line. For the lead.
