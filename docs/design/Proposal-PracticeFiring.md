# Proposed spec: practice at the great guns (2026-10-25)

Written at the owner's ask, for the lead: "practice firing, or blind firing, for the gun
evolutions … the most elegant way to use all the same orders and mechanics, but simply
firing at no target." It is meant for familiarising the models with the gun deck, for the
player's own fun, and for a ship working up her gun crews. Nothing here is decided. Spec M7
§8 and §8a (the gunnery's cycle and the quarter bill), §9 (the hit model), rule 2 ("a gun is
served by the bill") and rule 7 ("nothing pre-defines a battle's timing") bind.

## 1. The period

A King's ship exercised her great guns often, mostly in dumb show: cast loose, sponge,
load, run out, point and "fire" with the match not put to the vent, then run in and do it
again, the gun captains timed by the officer of the division. Powder for live practice was
allowed sparingly. The Regulations of 1806 give the gunner, each month for the first six
months after the guns come aboard, "one charge of powder and one round shot for one third
of the number of the upper deck guns, in Ships of two or three decks; or one fourth for
Ships of one deck", and half that after (Admiralty, *Regulations and Instructions*, 1808
printing, Sect. VII ch. II art. XXI, `docs/references/admiralty/
regulations-and-instructions-1808-ocr.txt` l.13122-13144). Keen captains spent their own
or begged more, and fired at a mark: an empty cask with a flag on a staff, dropped over the
side and fired at as the ship went about it at a cable or two, then four or five. Broke of
the *Shannon* is the famous case, firing at a cask most days of the years before 1813.
(Douglas 1820 on the exercise; the cask and Broke from memory, UNVERIFIED against a page.)

## 2. What the game already does

- The cycle runs with no mark at all. `beat to quarters`, `cast loose the guns`, `load with
  round` (chain, grape, double, a blank), `run out` and `secure the guns` all work alone at
  sea.
- A gun ordered by name fires with no mark (`fire No. 3 gun`). Shotted, its line says "a
  shot across her bows", which is the wrong words with nothing there (§6).
- `fire` at the word, `fire the starboard broadside`, `fire as they bear` and `by divisions`
  refuse: "Fire at what? No mark is engaged", or fire nothing, since there is nothing to
  bear on.

So the gap is the mark, not the gunnery.

## 3. The proposal: a mark that is not a ship

**One new kind of target, and nothing else new.** The battery's target is a ship's id today
(`Battery.target`, resolved each tick by `combat/action.target_of` into a `Target`).
Practice adds marks, ids under `mark:`, resolved by the same function into the same
`Target`. Every order, the arc and training, the elevation for the range, the heel and the
roll, the scatter, the hit chance by range and aspect, the minute's line of the fall of shot,
the magazine and the bill then work unchanged, because they already work on a `Target`. Two
kinds of mark:

1. **The cask** (live practice). `heave a cask overboard for a mark`: two hands and a minute
   from the deck, an empty cask with a flag on a staff, dropped from the quarter. It is a
   small floating body, about a metre, which drifts with the stream and a little to leeward
   (judgement). The lookout makes it out as "the mark" within about a mile by day in clear
   weather (judgement), and loses it in haze, at dusk and beyond. Then `engage the mark to
   starboard`, and every gunnery order as in action.
   - **Struck:** a hit knocks it to staves. The line says so ("the mark struck and knocked
     to pieces"), the mark is gone, the battery holds its fire for want of one, and the
     fighting book's "she strikes" never fires for a cask.
   - **Missed:** the fall of shot is the action's own: short, over, wide.
   - The ship may leave it astern, go about and run past it again at the range she wants:
     sail handling and gunnery together, which is the point of the exercise.
2. **The notional mark** (blind firing). `engage a mark four cables on the starboard beam`:
   a mark with no body at a fixed bearing and range from the ship, which moves with her,
   always there, in any weather, by night. It is the cheapest way to teach a crew, or a
   model, the elevation for a range. The shot is drawn exactly as at a ship of a stated
   length (a cutter's, judgement). The line says "on the mark" for what would have struck,
   and short, over or wide. Nothing is resolved against a body.

**Dumb show** (no powder at all). `exercise the guns`, or `exercise the starboard battery`:
the battery runs its cycle in exercise. The cartridge phase takes nothing from the
magazine, and the "fire" ends the cycle with no discharge: the gun run in by the tackles as
if it had recoiled, and served again. The minute's line gives what the officer of the
division would note: the rounds in the minute, the quickest gun and the slowest
("Exercising the starboard battery in dumb show: nine rounds in the minute, No. 3 the
quickest, a minute and twenty seconds from sponge to point"). `cease exercising` or `secure
the guns` ends it. Any mark, or none, will serve, and no shot leaves the ship.

## 4. What it costs and what follows

- **Powder and shot.** Live practice spends the magazine as an action does, counted by the
  gunner. There is no way to fill it again yet: see `Proposal-MagazineResupply.md` for the
  Ordnance's issue and the merchants' sale. Until then, practice is a real decision: the
  shot spent at a cask is not there for the Basque. A King's ship's practice beyond the
  Regulations' monthly allowance (§1) is the captain's own word, and the log keeps it.
- **Fatigue.** The cycle tires the hands as in action (the crew factor's fatigue). An
  afternoon at the guns is an afternoon's work.
- **Noise.** Gunfire is heard (the hearing of package 71's fog gun and the signal guns). A
  ship exercising her guns in sight of the coast or a squadron is heard and remarked, and
  near an enemy's cruising ground it may bring one down on her. The director may use that.
  The period's rule against firing in sight of a fleet without leave is the director's or
  the regime's to voice.
- **Skill (an open decision, not proposed here).** The hit chance reads the gun captains'
  ratings (`shot.aim_of`). Whether practice should make a crew better (a gun crew's drill
  count raising its pace and its aim a little, falling off without practice) is the owner's
  question of realism against pacing. It is true of the period, and it would make practice
  matter beyond the fun of it. The drill counts are proposed to be kept either way, so the
  question can be answered later from play.
- **No captain's doctrine for a mark.** A rules captain never engages a cask. A mark is not
  a stranger in his perception, and the fighting book's rows ("return her fire", "she
  strikes", "the colours") skip marks, as do the morale's rows.

## 5. Readings, the director and the primer

- **A reading, `the practice`.** For each gun or pair: the rounds fired, the mean and best
  time from sponge to fire, the fall of shot at the mark by range (on, short, over, wide).
  For dumb show, the rounds and the times only. It is what a model at the officer's station
  can learn from, and what the player reads to see his crews improve or not.
- **The director.** It may put a cask over the side by `aboard:` ("the cooper has an empty
  cask for a mark"), voice the gunner on the powder spent, and use the noise. Nothing new in
  its channel is needed.
- **A scenario: "Exercising the great guns."** A frigate on a quiet forenoon off the Lizard,
  the starter book and the fighting book loaded, no stranger, a cask in the cooper's store.
  The scenario for a model's first seat at the gun deck, and for the primer's new section in
  chapter 22.

## 6. Small things found on the way

- **A shotted gun fired by name with no mark logs "a shot across her bows"**
  (`Battery._discharge`: no target and not blank gives "across her bows"). With no mark the
  words should be "the shot into the sea" (or "on the mark" under the notional mark), and
  "across her bows" kept for the order that says it.
- The minute's line with no target names none ("Fired two guns, a blank charge"), which is
  right. Under exercise the same line takes the dumb show's words.

## 7. The pieces, for a package

| Piece | Where | Size |
|---|---|---|
| Marks: the cask (a body, its drift, its life) and the notional mark (bearing and range from the ship) | `freesail/combat/marks.py` new; `action.target_of` resolves `mark:` ids | small |
| A shot at a mark resolved: knocked to staves, or "on the mark" | `combat/hits.resolve_shot` (a mark's own branch) | small |
| The lookout makes out a cask within its range | `world/lookout.py` | small |
| Orders: `heave a cask overboard for a mark` (an evolution in `data/evolutions/`), `engage the mark`, `engage a mark N cables on the starboard beam`, `exercise the guns`, `cease exercising` | `orders/gunnery.py`, `data/vocabulary.yaml` | small–medium |
| Dumb show: no cartridge taken, no discharge, the cycle counted | `combat/guns.Battery` (an `exercise` intention beside `mode`) | small |
| `the practice` reading; the drill counts kept | `api/readings.py`, `combat/guns.py` | small |
| Captains, the fighting book and morale skip marks | `world/captains.py`, `data/standing_orders/fighting.orders`, `combat/morale.py` | small |
| Powder and shot to buy, and the Ordnance for a King's ship | `world/ports.py`, `data/ports/*.yaml` | medium (a decision first) |
| Truths: the frigate at a cask at two and four cables; dumb show's rate against the action's; a notional mark by night; the cask lost in haze | `tests/test_known_truths.py` | small |
| Primer chapter 22's section, the scenario | `docs/primer/`, `data/scenarios/` | small |
