# Tuning notes for package 10

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

Method for package 10: encode the truths table as tests first, then tune one constant at a time, recording each change and its effect here.
