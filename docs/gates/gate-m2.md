# Gate M2: Two rigs, honest numbers, a window on the ship

**Verdict:** Pending.

**Download:** the release page for `gate-m2` at https://github.com/PlasmeticRaven/FreeSail/releases/tag/gate-m2, or the plain zip of the snapshot branch at https://github.com/PlasmeticRaven/FreeSail/archive/refs/heads/gates/m2.zip.

## Headline

Milestone 2 claims:

1. **The ships are real.** The frigate is an Amazon-class 36 of 1795, dimensions from Winfield, spars from Luce's masting rules, sail areas from the spars, every rope rated from the period rope tables. The schooner is built to the Admiralty draught of Kemp's *Lynx* of 1812 with Fincham's rig, from Chapelle's *The Baltimore Clipper*. Every number in the two ship files carries a source or says "judgement". Masts rake.
2. **She sails at honest speeds.** Seventeen "known truths" about how ships of the period behaved are now automated tests, and fifteen pass with measured values: about five knots close-hauled at six points off the wind, eight knots on a beam reach in fifteen knots of wind, leeway of four or five degrees, a touch of weather helm under plain sail that turns to lee helm when the spanker comes in, a tack in six minutes, a wear in nine, hove to at a knot with the head fifty-odd degrees off. The two that fail are recorded as honest exceptions, not hidden.
3. **Things break.** Every spar, sail and line carries a load and a rating. Overpress her and the log warns; keep pressing and something carries away, with everything that hung from it. In thirty-five knots under all sail the royals go inside a quarter of an hour. In twenty knots under plain sail nothing does.
4. **You can see her.** A local web page shows the log, instruments, a map, and a ship view drawn from the ship's own parts: every sail in its true state, every yard at its true angle, the masts at their true rake. The view can be turned to any bearing, which is how the yards read when she is hove to.
5. **You can learn her.** The Sailing Master's Primer (`docs/primer/`) teaches the period words and orders in eight short chapters, and every order in it is run through the parser by a test. The parser learned the orders the primer reached for: `square the yards`, `back the main topsail`, `haul up the mainsail`, `sheet home`, `hard a-lee`, `steady as she goes`, `close reef the topsails`, `set the topsails and topgallants`, and the new `trim sails`. The console suggests orders as you type.

## What you need

As before: Python 3.11 or newer (`py` works where `python` does not) and the gate zip extracted to a fresh folder.

## Setup

In a terminal in the extracted folder:

```
py -m pip install -e ".[dev,server]"
```
*Ends with "Successfully installed ...". This time it also installs the small web server the browser view needs.*

```
py -m pytest
```
*Takes two or three minutes now: the truths sail real voyages. Ends `696 passed, 2 xfailed` (the two xfailed are the recorded exceptions; a `failed` is a fault).*

## Checklist

Steady 15-knot wind from the north unless stated; seed 7 throughout, so your numbers should match these within a few tenths.

### Part A: the tuned frigate, in the console

```
py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

- [ ] **1. She gets under way without rounding up.** Type `set plain sail`, then `brace sharp up on the starboard tack`, then `tick 600`, then `state`. Expect about `speed 4.8 kn, leeway -5°, heel -4°`, `Apparent wind 50° on the starboard bow`, a helm of a degree or so, and *no* red `Taken aback` line. (At gate M1 this same sequence put her in irons; that was truth 17.)

- [ ] **2. Trim sails.** Type `trim sails`. Expect `Braced 12 yards to the wind, 50° on the starboard bow; trimmed the sheets of the mizzen spanker; the fore topmast staysail; the jib.` and a dozen `Braced the ... yard` lines as the yards come round.

- [ ] **3. Completion as you type.** Type `set the fore t` and pause without pressing Enter: a menu offers `set the fore topsail`, `set the fore topgallant` and the rest. Type `haul the weather ` and pause: the lines you could haul. Press Escape or keep typing to dismiss. (Piped or scripted input does not show the menu; only a real terminal does.)

- [ ] **4. Tack, six minutes, honest speed.** Type `tack ship`, `tick 480`, `state`. Expect `Tacked; braced up on the larboard tack, heading ENE (68°)` about six minutes after the order, then a state of about `4.4 kn`, `51° on the larboard bow`.

- [ ] **5. Back the main topsail.** Type `reef the topsails, one reef`, `tick 400`, then `back the main topsail`, `tick 200`, `state`. Expect `Laid the main topsail yard aback, braced up for the starboard tack; the main topsail to the mast.` and her speed a little down. Then `brace the main yards full` and `tick 120` to let her draw again.

- [ ] **6. Wear, nine minutes.** Type `wear ship`, `tick 700`, `state`. Expect `Wore ship; braced sharp up on the starboard tack, heading WNW (292°)` about eight minutes after the order, and a state near `5.3 kn`.

- [ ] **7. Heave to, properly this time.** Type `heave to`, `tick 600`, `state`. Expect `Hauled up the courses; brailed up the spanker.`, `Clewed up the fore topgallant.`, `Hove to, main topsail to the mast, helm a-lee.`, and a state of about `speed 1.5 kn` with the wind `56° on the starboard bow`. She lies to.

- [ ] **8. Fill away.** Type `fill away`, `tick 300`, `state`. Expect `Filled away; braced full and steering WNW (292°)` and a state near `4.6 kn, 52° on the starboard bow`, with no `Taken aback` line. Type `quit`.

### Part B: things break

- [ ] **9. A gale under all sail.** Start `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,35 --heading 270`. Type `make all sail`, `brace up on the starboard tack`, `tick 600`, `make all sail` (the studding sails, which wait for the sail beside them), `trim sails`, `tick 600`, `trim sails`, `tick 600`. Expect `*` lines such as `Starboard fore topmast studdingsail straining at the bolt-ropes` and then red `!` lines: `Fore royal yard carried away in the slings; the fore royal hanging to leeward.`, the mizzen royal yard, the main royal mast, and studding sail booms, all inside the second ten minutes. Type `state`: the `Sail set` list no longer shows the royals. `quit`.

- [ ] **10. A fresh breeze under plain sail.** Start the same with `--wind 0,20`. Type `set plain sail`, `brace up on the starboard tack`, `tick 600`, `trim sails`, `tick 600`, `trim sails`, `tick 600`, `state`. Expect about `9.8 kn`, `heel -10°`, and *no* red line at all. `quit`.

### Part C: the browser window

```
py -m freesail.ui.server data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```
*Prints an address, normally `http://localhost:8000`. Open it in a browser. Leave the terminal running; close it with Ctrl+C when you are done.*

- [ ] **11. The page.** Four panels: the log with all/notable/urgent filters, the ship (a side view, masts raked, every sail furled as bundles on the yards), the instruments, and a north-up map with a wind arrow. The command line at the foot of the log.

- [ ] **12. Sails appear as they are set.** In the command line: `set plain sail`, then click `60x` and `go`. Over a few real seconds the bundles open into sails, the headsails first. Then `brace sharp up on the starboard tack` and watch the yards swing and the braces brighten while the evolution runs. Then `hold`.

- [ ] **13. Turn the view.** Press `]` a few times, or add `?facing=45` to the address. The same ship from another bearing: from 45° off the bow the braced yards read at a glance; from ahead the hull narrows to its beam. Press `\` to return to the leeward beam.

- [ ] **14. Hove to, seen.** `go` at `60x`, wait for her to gather way (the instruments show 4 to 5 knots), then `heave to`, then after a real minute `hold`. Turn the view to `?facing=45`: the main yards lie aback against the fore yards full. That cross is the first of the four benchmark scenes in the design proposal.

- [ ] **15. The instruments and the strain line.** With the frigate hove to, the instruments show speed near a knot, the helm at 15°, and a `Strain` line reading `none above rating`. (To see it read otherwise, run the gale of item 9 through the server instead.)

### Part D: the schooner and the primer

- [ ] **16. The schooner sails full and by and tacks.** `py -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 300`, then `set the foresail`, `set the mainsail`, `set the jib`, `set the fore staysail`, `set the fore topsail`, `brace sharp up on the starboard tack`, `tick 900`, `keep her full`, `tick 600`, `state`. Expect about `6.4 kn`, `41° on the starboard bow`. Then `tack ship`, `tick 600`, `state`: on the larboard tack near `68°`, about `7 kn`. `quit`.

- [ ] **17. Read one primer chapter and type along.** Open `docs/primer/README.md` in the zip and follow its suggestion (chapter 2, then 4 and 5). Try three orders from the chapters on either ship. Note any that are refused: the primer's blocks are tested, so a refusal is a real finding.

## Guide

**Truths and xfails.** The seventeen truths are statements such as "a frigate lies about six points off the wind" turned into tests that sail the ship by orders and measure the result (`tests/test_known_truths.py`, with the measured values in `docs/dev/TuningNotes.md`). Two are marked *expected to fail* with the reason recorded: the schooner's fastest point of sail comes out on a beam reach rather than a broad reach (the model has nothing that costs a fore-and-aft rig for reaching beyond heel), and the wear loses a little less ground to leeward than the books say (the script comes to as soon as the wind is aft). They are judgement calls for you, not bugs hidden.

**Rating and strain.** Each spar and line has a load rating from the period rope tables with the customary one-third margin. Above the rating the part wears and the log warns (`straining at the bolt-ropes`); well above it, it can carry away, with a small chance each second that grows with the overload, drawn from the seed so the same voyage always breaks the same way. Nothing repairs itself yet.

**Rake.** Masts lean aft a little, the mizzen most (1.5°, 2.5°, 4.5° on the frigate; 11° on the schooner, from Chapelle). The ship file holds it, the view draws it, and a forward-raking mast (a polacre's fore) is a negative number.

**The ship view.** Not a picture of a ship: a projection of the ship's parts, rebuilt every tick from the same data the physics uses. If a sail shows as aback, the physics says it is aback. The hull is a placeholder shape until the art pipeline exists.

**Facing.** The viewer's bearing from the bow: 0 is from ahead, 90 the starboard beam, 270 the larboard beam. The default is the leeward beam so the set sails face you.

## Not in this milestone

- **Crew.** Evolutions still take fixed times. Milestone 3.
- **Repair, cutting away a wreck, shifting a blown-out sail.** A carried-away spar stays carried away. Milestone 8.
- **The world.** Still an endless plane with one wind. Milestone 5.
- **The ship view's art**, facings beyond the projection, movement and backgrounds. Milestone 8; the projection is the skeleton they will hang on.
- **The schooner's bare fore yard and a way to say "jib sheet to windward".** Two format gaps recorded in the specification's open items; the second is why the schooner cannot be hove to under a knot and a half yet.

## What to report back

- Pass or fail for items 1 to 16, what happened for 17.
- Your reading of the two xfails, and of any measured number in items 1, 4, 6, 7 and 16 that a sailor would call wrong.
- Anything in the browser window that confused you, or that you looked for and could not find.
