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

