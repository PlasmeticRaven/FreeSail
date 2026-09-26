# Gate M3b: Rig geometry and canvas

**Verdict:** Pending (owner).

## Headline

Milestone 3b claims:

1. **Pointing emerges.** How close each ship lies comes from her brace limits (Fincham's measured angles), the flatness of her canvas (bowlines hauled, new or worn cloth), her trim (the after yards sharper than the head yards) and how she is steered, not from a number in a file. The frigate holds two thirds of her beam-reach speed to six points off the wind, the schooner to five.
2. **Practices have prices.** Bowlines hauled flatten the sails and cost hands at every tack. Swiftering in the catharpins braces the main yard four degrees sharper and loads the main mast harder until eased. Studding sails carried too close shake, strain their booms and carry them away. Bracing one yard away from its neighbours is refused, with the reason.
3. **Canvas is a thing.** Every sail has a canvas number from period practice and a condition that wears with use. A worn royal in a gale blows out before its yard goes; a new one holds until the yard goes. The sail room holds the spares, the heavy-weather sails and the storm canvas, and `the sail room` lists them.
4. **Studding sails know the wind.** Nothing refuses them on a wind; the wind does. Their booms start rigged in, and going about takes them in first.

Four of the ten new truths come to you as rulings rather than passes. Each has a strict expected failure naming the measured value (item 11).

## What you need

As before: Python 3.11 or newer (`py` works where `python` does not) and the gate zip extracted to a fresh folder.

## Setup

In a terminal in the extracted folder:

```
py -m pip install -e ".[dev,server]"
```
*Ends with "Successfully installed ...".*

```
py -m pytest
```
*Takes about eleven minutes. Ends `1032 passed, 7 xfailed`. The seven expected failures are three earlier ones (truth 3 for the schooner, truth 11's ground and truth 18's times) and four of this milestone marked as your rulings (truths 24, 26, 28 and 31). A `failed` is a fault.*

## Checklist

Seed 7, wind from the north, as at the earlier gates. The console's wind gusts, so a speed can differ from these by a few tenths of a knot; the log lines and their times should match within a minute. Commands after `>` are typed at the prompt; `tick` is game seconds.

### Part A: pointing, in the console

```
py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

- [ ] **1. The frigate's pointing before and after the bowlines.** Type `set plain sail`, `brace sharp up on the starboard tack`, `tick 1200`. Expect `Braced up for the starboard tack, the after yards two degrees sharper.` and, as the yards arrive, `Braced the fore yard; 62° from square.`, `Braced the main yard; 64° from square.`, `Braced the crossjack yard; 60° from square.`. These are Fincham's limits. Then `trim sails`, `steer 294`, `tick 600`, `trim sails`, `tick 300`, `state`: about `speed 5.7 kn`, `Apparent wind 48° on the starboard bow`. Now `haul the weather bowlines`. Expect five lines at 04:36, `Steadied out the starboard fore course bowline.` down to `Steadied out the starboard mizzen topsail bowline.`. `tick 600`, `trim sails`, `tick 300`, `state`: about `6.1 kn` at the same heading. Then `steer 298`, `tick 600`, `trim sails`, `tick 300`, `state`: about `5.2 kn` four degrees closer. That is roughly the speed she had at 294 before. In steady wind the truths measure +0.55 knots at 66° off the wind, and the same speed 3.3° closer (item 11). Keep this console.

- [ ] **2. The after yards' trim.** Continue: `trim sails with the head yards sharper`, `tick 600`, `state`. The log says `the head yards three degrees sharper`, and she falls to about `4.2 kn`. `trim sails`, `tick 300`, `state`: `the after yards two degrees sharper` again and about `4.8 kn`. The gain of two degrees sharper over all alike is 0.17 knots in steady wind, smaller than the console's gusts. It is truth 24, and it is your ruling (item 11). Keep this console.

- [ ] **3. The catharpins.** Continue: `swifter in the catharpins on the main`, `tick 1800`. Expect `Boatswain's party to the main mast shrouds; reeve the swifter.` at 05:20 and `* Swiftered in the catharpins on the main mast; the main yard will brace four degrees sharper.` at 05:45. `trim sails`: `... the after yards six degrees sharper; ...`. `tick 300`, then `ease the catharpins on the main`, `tick 2400`. Expect `Main yard came in to 64° from 68° as the lower shrouds went out.` at 06:09 and `* Eased the catharpins on the main mast; the main yard braces as rigged again, four degrees less sharp.` at 06:20. Type `quit`.

  The price is in the main mast, and the log stays quiet about it. A lower mast is rated for 55 knots, so no strain line comes in 30. To see the number, paste this at the terminal (not in the console) as one line:

  ```
  py -c "from freesail.api.session import make_world; from freesail.core.world import Scenario; w = make_world(7, 'data/ships/frigate-36.yaml', Scenario(wind_from_deg=0, wind_speed_kn=30, gustiness=0, variability=0, ship_heading_deg=292.5, ship_speed_kn=4)); m = w.ship.spars['main.mast']; w.submit('set plain sail'); w.submit('brace sharp up on the starboard tack'); w.run(1200); w.submit('trim sails'); w.run(120); print('out: %.3f' % m.strain_ratio); w.submit('swifter in the catharpins on the main'); w.run(2400); w.submit('trim sails'); w.run(300); print('in:  %.3f' % m.strain_ratio)"
  ```
  *Prints `out: 0.178` and `in:  0.229`.* The main mast bears 29 per cent more of its rating. A sixth of that is the shrouds drawn in; the rest is the harder pull of the sharper yard.

- [ ] **4. The schooner's pointing.** `py -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 300`. Type `set plain sail`, `brace sharp up on the starboard tack`, `tick 1200`, `trim sails`, `steer 294`, `tick 600`, `trim sails`, `tick 300`, `state`: about `7.3 kn` 66° off the wind. `steer 304` (five points), `tick 600`, `trim sails`, `tick 300`, `state`: about `5.8 kn`, still above two thirds of her beam-reach speed (8 knots). At the same heading the frigate would make under four. `haul the weather bowlines`: one line, `Steadied out the starboard fore topsail bowline.`. It gains her next to nothing, because she points with her fore-and-aft sails. Type `quit`.

### Part B: canvas

- [ ] **5. The sail room and the storm mizzen.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293`. Type `the sail room`. Expect `The sail room holds 21 sails.`, then lines for `Spares of the working canvas`, `For heavy weather: foresail, No. 1 canvas, new; fore topsail, No. 1 canvas, new; main topsail, No. 1 canvas, new.`, `Storm canvas: fore storm staysail, No. 1 canvas, new; mizzen storm staysail, No. 1 canvas, new; storm mizzen, No. 1 canvas, new.` and `For light fair winds: ringtail, ...; starboard fore save all, ...; larboard fore save all, ...`. Now type `shift the spanker for the storm mizzen`, `tick 1500`: `Unbent the spanker and lowered it down on deck.` at 04:03, `Swayed aloft the storm mizzen (No. 1 canvas, new).` at 04:06, and `* Shifted the spanker; the storm mizzen bent (No. 1 canvas, new) and furled, 21 spare sails left in the sail room.` at 04:11 (the spanker has gone below in its place). `set the storm mizzen`, `tick 300`: `Set the storm mizzen.` at 04:26. `muster`: its last line is `Sail room: 21 sails, 13 spares of the working canvas; ...; the storm canvas (fore storm staysail and mizzen storm staysail); ...`. Type `quit`.

- [ ] **6. The gale with a new royal and a worn one.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,35 --heading 270`. As at gate M2: `make all sail`, `brace up on the starboard tack`, `tick 600`, `make all sail`, `trim sails`, `tick 600`. The royals are new: `Mizzen royal yard carried away in the slings; ...` and `Main royal yard carried away in the slings; ...` at 04:12, and `Fore royal mast carried away; the fore royal, with the fore royal yard, hanging to leeward.` at 04:15. Type `quit`.

  The console cannot yet bend a worn sail. Canvas wears by the hour, and nothing at the prompt sets a sail's condition. So the worn royals are shown from the terminal, the same gale with the royals at half their condition (in steady wind, so the times are a minute earlier than the console's):

  ```
  py -c "from freesail.api.session import make_world; from freesail.core.world import Scenario; w = make_world(7, 'data/ships/frigate-36.yaml', Scenario(wind_from_deg=0, wind_speed_kn=35, gustiness=0, variability=0, ship_heading_deg=270, ship_speed_kn=0)); [setattr(w.ship.sails[r], 'condition', 50) for r in ('fore.royal', 'main.royal', 'mizzen.royal')]; w.submit('make all sail'); w.submit('brace up on the starboard tack'); w.run(600); w.submit('make all sail'); w.submit('trim sails'); w.run(1200); print(*[e.line() for e in w.log if e.kind in ('sail.blown_out', 'spar.carried_away')][:5], sep=chr(10))"
  ```
  *Prints `Mizzen royal split and blew out of the bolt-ropes.` at 04:11, the fore and main royals at 04:13, and only then the topgallant yards.* No royal yard goes: the worn canvas went first and took the load off its spar.

- [ ] **7. Storm canvas, lying a-try.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,45 --heading 293`. Type `call all hands`, `tick 90`, `send down the topgallant masts`, `bend the fore storm staysail`, `bend the mizzen storm staysail`, `brace sharp up on the starboard tack`, `tick 1500`, `set the topsails`, `tick 600`, `close reef the topsails`, `tick 1500`, `set the fore storm staysail`, `set the mizzen storm staysail`, `tick 300`, `lie a-try`, `tick 600`. Expect `Roused up the fore storm staysail from the sail room (No. 1 canvas, new) and swayed it aloft.`, the topsails reefed with three reefs each, and `* Lying a-try under the main topsail and the staysails, helm a-lee.` at 05:12. `furl the fore topsail`, `furl the mizzen topsail`, `tick 600`, `state`: about `4.7 kn`, with a leeway near 170°, which means she is going **astern**. In the console's gusts the storm staysails then blow out at 05:28. In steady 45 knots nothing is lost in an hour, and she goes astern at 4.4 knots 45° off the wind. That is truth 28, and both halves are for you to judge (item 11). Type `quit`.

### Part C: studding sails and the ringtail

- [ ] **8. Studding sails carried too close, and eased.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,13 --heading 259` (nine points off, the wind on the starboard quarter). Type `set plain sail`, `tick 600`, `trim sails`, `tick 200`, `set the studdingsails, weather`. It is refused: the booms start rigged in. `rig out the studdingsails, weather`, `tick 200`: five `Rigged out the starboard ... studdingsail boom.` lines. `set the studdingsails, weather`, `tick 600`, `set the studdingsails, weather` (refused as already set), `tick 600`, `trim sails`, `tick 120`, `state`: all five set at 04:20 to 04:22, about `8.2 kn`. Now bring her up to six points: `steer 292`, `tick 60`. Expect `* Starboard fore lower studdingsail shaking in its gear; she is too near the wind to carry it.` at 04:38, and a `... boom whipping as the ... flogs; she is too near the wind for it.` for each of the five. `trim sails`, `tick 240`: `! Starboard main topmast studdingsail boom carried away; ...` at 04:40 and the fore topmast's at 04:41. Ease her: `steer 259`, `tick 60`: `Starboard fore topgallant studdingsail drawing again.` and the other two still aloft at 04:44. `trim sails`, `tick 300`, `state`: back to about `7.6 kn`. Nothing refused any of it. (In 12 knots every boom whips and none goes in ten minutes, which is truth 29.) Type `quit`.

- [ ] **9. The schooner's ringtail running.** `py -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 180`. Type `set plain sail`, `tick 1200`, `trim sails`, `tick 300`, `state` (about `5.3 kn`). `bend the ringtail`, `tick 900`: `Roused up the ringtail from the sail room (No. 5 canvas, new) and swayed it aloft.` and `* Bent the ringtail ...`. `rig out the ringtail boom`, `tick 120`, `set the ringtail`, `tick 600`: `* Set the ringtail.` at 04:46, and after `trim sails` a notable `Ringtail boom working under the press of sail.`. `tick 300`, `state`: about `6.2 kn`. In steady wind it is worth +0.21 knots dead before it and +0.30 with the wind on the quarter; the frigate's ten studding sails are worth +0.73 knots running (truth 30, against Luce's "about a knot"). Type `quit`.

### Part D: the browser window and the primer

```
py -m freesail.ui.server data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

- [ ] **10. The view.** Type in the command line `set plain sail`, `brace sharp up on the starboard tack`, and run at `10x` until plain sail is set. **Fixed scale:** the ship does not grow or shrink as the yards swing round. Then `send down the topgallant masts` and run on until the log says they are down: the upper spars vanish and leave the sky they filled, and the ship is drawn at the same size. **Goose-wing:** `goose-wing the fore topsail`, `tick 60`. The fore topsail is drawn as a triangle from the weather clew, sheeted home, up to the lee yardarm, with its foot rising to the lee side and the lee clew hauled up to the yard (gate M3's finding). **Draw order:** press `]` a few times to look from the bow quarter. Sails nearer you cover sails beyond, and a staysail that crosses a mast is drawn in two parts, one either side of it. **Bowlines:** `haul the weather bowlines`. Faint lines run forward from the weather leeches of the courses and topsails.

- [ ] **11. The truths for your ruling.** Read `docs/dev/TuningNotes.md`, "Package 24: truths 24 to 33, measured". Rule on the four marked as yours:
  - **24**, the after yards: +0.17 kn, 0.9° closer, against a quarter knot or a quarter point.
  - **26**, the bowlines: 3.3° closer against half a point.
  - **28**, lying a-try: she goes astern at 4.4 kn against under 1.5.
  - **31**, the catharpins: 0.7° closer against a quarter point. The mast's strain rises by 29 per cent against the spec's sixth.

  Also rule on the two that pass on the measured number: **30** (+0.73 kn against about a knot) and **32** (six points and five, which is the record).

- [ ] **12. The primer's new sections.** Read and type along:
  - Chapter 3, `docs/primer/03-making-and-shortening-sail.md`: studding sails rigged out before they are set, how close they may be carried, the ringtail, save-alls and water sail, canvas and its condition, the sail room, storm canvas.
  - Chapter 4, `04-trimming.md`: "Pointing: how close she lies, and what it costs".
  - Chapter 5, `05-going-about.md`: "In studding-sails first, and the bowlines".

  Their blocks are tested, so a refusal the chapters do not predict is a real finding.

## Guide

**Brace limits.** Each yard braces to Fincham's measured angle for a long frigate of 1827, turned to degrees from square: the frigate's fore yard 62°, main 64°, crossjack 60°, and each yard above its lower yard two degrees more. These, with the square sail's lift curve moved five degrees at integration, keep truth 1 in its band: best course to windward 64°, closest holding three knots 56°.

**Bowlines.** A hauled weather bowline takes four degrees off its sail's luff angle while the yard is braced up. It slacks by itself when the yard is braced in past 40° from square. The tack lets the bowlines go at *Mainsail haul* and steadies them out again on the new tack.

**Catharpins.** Swiftered in, the lower yard on that mast braces four degrees sharper. The mast is rated at 0.85 for the athwartships part of its load until the catharpins are eased.

**Canvas.** Cloth strength follows Luce's Appendix E by canvas number. A sail wears 0.05 of its condition an hour set and three times that shaking or aback. It bears `0.4 + 0.6 × condition/100` of its new strength, and it lies a little less close as it wears. Nothing mends canvas yet.

**Studding sails.** A studding sail stalls a point forward of Luce's angles, reckoned off the true wind: seven points for the topmast and topgallant studding sails, the beam for the lower ones and the ringtail. A stalled sail flogs, and the strain model does the rest. Two things are refused, and both are geometry: a lee boom rigged out past the lee rigging, and a yard braced sharper with its lee boom out.

## Not in this milestone

- **A headed stream.** The head sails do not turn the wind the after sails meet, which is Fincham's reason for bracing the after yards sharper. So the practice gains little here (truth 24).
- **Lying quietly in a storm.** She goes astern where a ship of the period drifted bodily to leeward (truth 28). This is a physics question for your ruling, not a constant to be quietly moved.
- **Wearing canvas at the prompt.** Canvas wears by the hour. No order or console command sets a sail's condition, so a worn royal is shown from the terminal (item 6).
- **Geometric brace limits** from channel breadths and shroud spread, Fincham's Bouguer and Euler tables, Steel's spar tables, and Hardy's other measures: the spec's open items.
- **The sailmaker's mending**: milestone 8.

## What to report back

- Pass or fail for items 1 to 10, and what you read in 12.
- Your rulings on truths 24, 26, 28 and 31, and your reading of 30 and 32 (item 11).
- Whether the storm staysails blowing out in the console's gusty 45 knots (item 7) is right for No. 1 canvas, or whether the cloth anchor is low for the heaviest sails (`docs/dev/TuningNotes.md`, "Storm canvas at its limit in a storm").
- Whether the log's new lines read as a ship's log. These include the bowlines steadied out, the swifter, the studding sails shaking in their gear, the sail room, and "the after yards two degrees sharper".
