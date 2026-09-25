# Gate M1: A ship that sails by orders

**Verdict:** Pending.

**Download:** the release page for `gate-m1` at https://github.com/PlasmeticRaven/FreeSail/releases/tag/gate-m1, or the plain zip of the snapshot branch at https://github.com/PlasmeticRaven/FreeSail/archive/refs/heads/gates/m1.zip.

## Headline

Milestone 1 was specified as "one sail, one hull". It came out considerably further than that, because the four packages built in parallel each landed whole. The claims:

1. **Ships are data.** Two draft vessels, a 36-gun frigate and a topsail schooner, are described entirely in files: every spar, sail and line, with how they connect. The engine has no ship of its own. A file with a mistake in it is refused with a sentence saying what and where.
2. **The wind drives her and the water answers.** Each sail gives lift and drag from the apparent wind at its own height; the hull resists, makes leeway, heels, and turns to the rudder; a helmsman steers the ordered course. All of this is untuned: she is about a third too fast, and that is the next milestone's job.
3. **You sail her in Orders.** `set plain sail`, `brace sharp up on the starboard tack`, `reef the topsails, one reef`, `haul the weather main brace`, `tack ship`, `wear ship`. Nonsense and ambiguity are refused with a sentence that says what was understood and what was not.
4. **Seamanship takes time.** Setting a topsail takes minutes; tacking a frigate takes four or five; wearing takes longer and loses ground to leeward. The sequences follow Luce and Lever and are cited in the data files. The times are fixed for now; the crew system will make them depend on who is aloft.
5. **Everything from milestone 0 still holds.** Same seed, same orders, same log; a save rebuilds the identical voyage, now with a real ship in it.

## What you need

As for gate M0: Python 3.11 or newer with "Add python.exe to PATH" ticked, and the gate zip extracted to a folder. If you still have the M0 folder, this is a separate one; keep them apart.

## Setup

Open a terminal in the extracted folder (File Explorer, click the address bar, type `cmd`, Enter). Then:

```
pip install -e ".[dev]"
```
*Ends with "Successfully installed ...". One new package this time, prompt_toolkit, which fixes the typing problem you found in gate M0.*

```
python -m pytest
```
*A line reading `NNN passed in ...s` where NNN is in the high four hundreds. Any `failed` is a fault; note the test's name.*

## Checklist

Everything below uses a steady 15-knot wind from the north with no gusts, so that your numbers match these. Type exactly what is in code.

### Part A: the frigate

Start:

```
python -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

- [ ] **1. She has a name and no sail set.** First line: `* Morning watch, 8 bells (04:00)  Open water. Wind N, 15 knots, a moderate breeze. Heading WNW (293°).` Type `state`: three lines beginning `Amazon: heading WNW (293°), speed 0.0 kn`, then the apparent wind, then `Sail set: none`.

- [ ] **2. One sail takes minutes to set.** Type `set the fore topsail`. You see `Order: set the fore topsail.` and `Hands aloft to loose the fore topsail.` Type `tick 360`. Among the lines: `Laid aloft and loosed the fore topsail.` and then, marked `*`, `Set the fore topsail.` at about 04:05. The topsail alone, with the yards square, will not drive her to windward; she may drift and swing, and a `Taken aback` line is possible. That is honest.

- [ ] **3. Nonsense and ambiguity are refused usefully.** Type `splice the mainbrace`: `Order not carried out ... 'splice the mainbrace' is not an order this ship understands. An order begins with a verb such as set, take in, furl, reef, ...`. Type `set the topsail`: `... The topsail could be the fore topsail, the main topsail or the mizzen topsail; say which ('set' was understood).`

- [ ] **4. Plain sail, braced up, and she goes.** Type `set plain sail`, then `brace sharp up on the starboard tack`, then `tick 900`, then `state`. Expect: a dozen `Braced the ... yard; NN° from square` lines (55° to 62°), eleven `Set the ...` lines over about five minutes, and a state of roughly `heading WNW (293°), speed 8.0 kn, leeway -3°, heel -7°` with `Apparent wind 40° on the starboard bow` and a small helm angle. Your speed may differ by a few tenths. Negative leeway and heel mean to larboard, which is to leeward with the wind on the starboard side: correct.

- [ ] **5. A single line can be hauled.** Type `haul the weather main brace`. Expect `Hauled the starboard (weather) main brace; the main yard now braced 50° for the starboard tack.` The weather brace on the starboard tack is the starboard one, and hauling it brings the yard in five degrees from sharp up. (Note that this leaves the main yard less sharp than the others; it is fine for the tack that follows.)

- [ ] **6. Tack ship.** Type `tack ship`, then `tick 600`, then `state`. Expect `All hands about ship.`, then lines about the helm going down, sails `taken aback` one by one as she passes through the wind, `Rise tacks and sheets. Mainsail haul.`, `Let go and haul.`, and after about four minutes, marked `*`: `Tacked; braced up on the larboard tack, heading ENE (68°).` The state shows heading ENE, `Apparent wind 41° on the larboard bow`, and leeway and heel now positive (to starboard, the new lee side).

- [ ] **7. Reef the topsails.** Type `reef the topsails, one reef`, then `tick 400`. Expect three lines marked `*`: `Reefed the fore topsail; now set, 1 reef.` and the same for main and mizzen, after about six minutes.

- [ ] **8. Wear ship.** Type `wear ship`, then `tick 900`, then `state`. Expect the yards to follow the wind round as she runs off, then `Wore ship; braced sharp up on the starboard tack, heading WNW (292°).` The state is back on the starboard tack at about 41° apparent. She lost ground to leeward doing it; the map in milestone 2 will show that.

- [ ] **9. Heave to (observe, do not judge).** Type `heave to`, then `tick 900`, then `state`. Expect `Hauled up the courses.` and `Hove to, main topsail to the mast, helm a-lee.` The state should show her lying with the wind roughly 45° to 55° on the bow and little speed. She may show a large leeway number and be drifting astern: the balance of a hove-to ship depends on the untuned numbers and this evolution is known to be rough. Report what you see; it is data for the tuning work, not a pass or fail.

- [ ] **10. Save and replay with a real ship.** Type `save voyage.json`, then `replay voyage.json`. The rebuilt state must match the one printed before it, number for number, including every sail in the list.

Type `quit`.

### Part B: the schooner

Start:

```
python -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 300
```

- [ ] **11. Different rig, same language.** Type `set the foresail`, `set the mainsail`, `set the jib`, `set the fore topsail`, `brace sharp up on the starboard tack`, then `tick 900`, then `state`. Expect `Speedwell: heading NW by W (300°), speed 7.6 kn` or thereabouts, `Apparent wind 38° on the starboard bow`, and `Sail set: fore.topsail, fore.sail, main.sail, jib`. Two of those are gaff sails and one a jib; the parser and the physics never saw a schooner until they read the file.

- [ ] **12. She tacks too.** Type `tack ship`, then `tick 600`, then `state`. Expect `Tacked; braced up on the larboard tack, heading ENE (67°)` and a state on the larboard tack at about 42° apparent, around 8 knots.

- [ ] **13. Ask for something she has not got.** Type `set the mizzen topsail`. Expect a refusal naming the nearest things she does have. Type `quit`.

### Part C: your own orders

- [ ] **14. Speak to her in your own words.** Start either ship again and try five orders phrased as you would say them: reef by a different wording, brace a particular mast's yards, ease a sheet, steer by a compass point, take in a named sail. Note which were understood and which were not. Refusals that you think should have been understood are the most useful thing this gate can produce.

## Guide to the technical ideas in the checklist

**Apparent wind.** The wind as felt on deck, which is the true wind combined with the ship's own motion. A ship making 8 knots across a 15-knot wind feels it further ahead and stronger. The `state` line reports it as an angle from the bow and a side. A square-rigged ship cannot keep her sails full much closer than about 40° apparent; that is why she lies about six points (67°) off the true wind.

**Tack.** The side the wind is on. Wind from the starboard side means she is on the starboard tack. Tacking means turning the bow through the wind to the other tack; wearing means turning the stern through it, which is slower and safer and loses ground downwind.

**Brace.** The yards (the horizontal spars the square sails hang from) are swung by ropes called braces. "Sharp up" is as far round as they will go, for sailing close to the wind; "square" is straight across for running before it. The number in `Braced the fore yard; 55° from square` is that angle. On the starboard tack, hauling the *larboard* brace (the lee one) brings the yard sharper; hauling the starboard (weather) brace lets it come back toward square.

**Weather and lee.** Weather is the side the wind comes from; lee is the other. `haul the weather main brace` is resolved at the moment you say it, from the tack she is on then, and the log tells you which rope that turned out to be.

**Leeway and heel signs.** Positive is to starboard, negative to larboard. With the wind on the starboard side she leans and is pushed to larboard, so both are negative; after a tack both flip.

**Evolutions.** A named piece of seamanship (set a sail, reef, tack) that takes fixed, realistic minutes in this milestone. The log tells you when hands go aloft and when the job is done. Two orders for the same sail queue up; the second waits.

**In the gear.** A square sail hauled up to its yard by its lines but not yet furled. `take in` leaves a sail in the gear; `furl` stows it.

## Not in this milestone

- **Tuned numbers.** She is roughly a third too fast at every point of sail, and heave-to does not settle properly. Package 10 (the known truths) is next and will change constants, not behaviour.
- **Crew.** Every evolution takes the same time whoever is aboard. Milestone 3.
- **Strain and carrying away.** Nothing breaks yet however hard it blows. Package 9, in milestone 2.
- **The browser window** with map and ship view. Milestone 2.
- **Verified ship particulars.** Both ships are drafts with approximate dimensions and areas; package 8 checks them against the references.
- **Standing orders and scripts.** Milestone 4.

## What to report back

- Pass or fail for items 1 to 8 and 10 to 13; what you observed for 9; what you tried and what happened for 14.
- Any log line that reads wrongly to a sailor's ear, quoted.
- Whether the setup went smoothly on top of the M0 install.
