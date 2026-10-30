# 22. An action

From clearing for action to the colours struck, in the player's words. What the game can fairly do with a fight between two ships in 1805, and no more: the guns as parts of the ship with their crews from the muster, served by a cycle that runs while hands and powder last; the shot's fall by the range, the heel and the sea; a hit as a change of the state the ship already has (a line parted, a spar carried away, a sail holed, a gun dismounted, a shot hole, a man hurt); the company's temper, and the colours that come down when it fails. The marines' fire, the fight on deck, the water from the holes and the surgeon are chapter 25's; the prize is not yet in the game.

## The guns

Your ship carries what her file gives her, through the generator with the source beside each figure (`tools/gen_ships.py`). The cutter has two fits the scenario chooses between: the 12-pounder carronades the Admiralty gave its cutters from the 1790s, the default of 1805, and the hired cutters' long 3-pounders with eight swivels (`fit: long guns`). The frigate of the *Amazon* class has her twenty-six long 18-pounders, her 32-pounder carronades on the quarterdeck and forecastle and her 9-pounder chasers; the brig-sloop her 32-pounder carronades; the merchant brig her four 6-pounders. Each gun is a part by its number and side ("No. 3 starboard gun", "the starboard bow chaser", "the No. 2 larboard swivel"), with a load state (empty; loaded with round, chain, grape or double; run in or out; primed), and the magazine and the shot lockers are stores the gunner counts.

```
the guns
```

```
The guns: 6 12-pounder carronades; secured.
```

## The quarter bill

At quarters every man has a station by a quarter bill the ship's file carries beside her watch bill: the gun crews (one crew to each pair of guns, who serve whichever side is engaged), the sail trimmers (the hands told off to work the ship), the helm, the powder, the marines, the carpenter at the wings and the surgeon below. The drum is a crew order and never queues behind the work in hand:

```
beat to quarters
```

```
Beat to quarters! Quarters: three gun crews manned, the trimmers 9, the helm 1, the powder 4. Six of the guns' hands at the work in hand, to go to their guns as it is done.
```

`clear for action` is the longer form: the bulkheads down, the galley fire out, the decks wetted and sanded, the boats towed astern, and then the drum; a frigate's quarter of an hour, a cutter's five minutes. `cast loose the guns` has the crews cast off the tackles and provide the guns (a minute with the crews at them; longer while the company is still coming up the hatchways), and from then the guns are served by themselves: loaded, run out and primed as your standing intentions have it. `the quarter bill` reads the bill as beaten.

The work of an action is continuous and concurrent, never a queue. You give an order and the bill finds the hands, saying from where: a sail order at quarters draws first on the trimmers and then on the guns by the fighting book's priority. Under `sail before guns` (the default) a tack takes half of every gun's crew and goes at its full pace while the guns go short ("Tacking ship at quarters: 84 hands taken from the guns, half of each crew; the guns go on short-handed"); under `guns before sail` the trimmers alone have the ship, and the frigate's tack that took 447 s cleared takes 642. The hands go back to their guns as the work is done.

## The standing intentions and the one-shot orders

The gun deck's orders are of two kinds. The standing intentions the battery keeps until you change them, logged when they change something:

| Order | What it sets |
|---|---|
| `engage her to starboard` / `engage the brig to larboard` / `engage on both sides` | the mark and the side; 'her' is the nearest enemy, else the nearest sail |
| `load with round shot` / `chain` / `grape` / `double` / `a blank cartridge` | the charge the guns take from now (a loaded gun keeps its charge until fired; a swivel takes round or grape) |
| `aim at her hull` / `her rigging` / `between wind and water` | the aim's doctrine: where the hits are allotted |
| `fire as they bear` / `fire by divisions` / `hold your fire` | the firing's doctrine: each gun as it is loaded and bears (the period's independent fire); the forward and the after division by turns; no gun but by name or at the word |
| `fire on the up roll` / `fire on the down roll` | the gun captain's moment: the up-roll for the rigging, the down-roll for the hull |
| `run out the guns` / `run in the guns` | whether the guns are run out when loaded (run in, a tack is the easier) |
| `guns before sail` / `sail before guns` | the fighting book's priority when sail work wants hands |

The one-shot orders ride over them:

| Order | What happens |
|---|---|
| `fire` / `fire the larboard broadside` / `fire both broadsides` | the broadside at the word: the side's guns that are loaded and bear, together, once; the word stands until one bears |
| `fire No. 3 gun` / `fire the bow chaser` / `fire the swivels` | a gun by its number or its place, once |
| `fire a shot across her bows` / `fire a gun to leeward` | the ranging or the signal shot: strikes nothing, and her log says so |
| `cease firing` | the firing's doctrine back to hold; the mark is kept |
| `secure the guns` / `pipe down` | the guns housed and the hands back under the watch bill |
| `strike the colours` | never refused; the consequence told |

A gun captain fires at nothing beyond his gun's throw (a 12-pounder carronade's random shot is 800 yards, a long 3-pounder's 1,200, a swivel's 400), whatever the order.

## The fall of shot

Each shot is laid for the range by its gun captain, the quoin answering only so far: the lee battery fires lower and shorter and the weather battery higher and longer by the heel, and the sea scatters the shot by its height and the roll (no lee port is shut by the heel yet: a lee gun is served however far she lies over, and its shot falls short where the quoin cannot answer the heel). The hit chance falls with the range from nine in ten at pistol shot to one in two at point blank (380 yards for a long 18-pounder, 250 for a long 3-pounder, 230 for a 12-pounder carronade) and a fifth at twice it. Your log says what your people can see of your own fire, once a minute; the ship fired at says what hers can see of it:

```
* Forenoon watch (10:04)  Three shot at a cutter: one struck her and two wide. A shot struck her between wind and water.
! Forenoon watch (10:05)  Shot from a cutter: two shot through the side to starboard; three killed and one wounded.
```

The minute's line of your own fire is notable (marked `*`) when a shot struck her or when it opened the fire on her, and routine when the minute's shot all fell short, over or wide; the line of shot that struck you is notable, and urgent (`!`) when it killed a man or carried away a spar or the helm. So a station standing by until *a notable event* in action is woken for what matters, a hit, a strike, a change of state, and not for every discharge at the clock's pace; at quarters the trimmers' bracing yard by yard is routine too, and a trim's one line for all the yards notable as ever.

`the enemy` reads the mark in the lookout's words with her range in cables by his estimate; `the range` compares in the standing dialect (`when the range is under 2 cables then fire as they bear`).

## The damage

No second model of the ship exists for the fight. A hit is a change of state the game already has: a line shot away comes down as a parted line does, a spar shot away is cleared as a wreck is, a sail holed draws the less, a gun dismounted is out of the bill, the wheel shot away loses you the helm until the relieving tackles are rove, a shot hole is written with its place against the waterline for the well to read when the water comes (chapter 25), and the men at the part struck are killed and wounded in the muster, off the bill. The carpenter's and the boatswain's report:

```
the damage
```

```
The damage: the main topgallant mast, the square sail yard and the topgallant yard carried away; eight lines parted; the topsail, the main sail and the jib holed.
```

```
the bill
```

```
The bill: one killed and four wounded of 30; the hands shaken.
```

## The fighting book, and the colours

The rules captain fights by his doctrine as data (`data/captains/*.yaml`, the `engaging` book and its figures): whether he engages at all (a merchantman runs or strikes by the odds; a privateer takes what pays and runs from a man of war; a King's ship engages her class and hauls off from a heavier), from which side, at what range (the British close, the French at long shot), his aim, and when he breaks off. On entering the state he beats to quarters, casts loose, loads and lays the guns by his doctrine, engages the mark on the side she bears, and keeps her on the engaged beam at his range each minute; his book opens the fire and ceases it. Your own fighting book is `data/standing_orders/fighting.orders`, loaded beside the starter's in the first action's scenario, to read and rewrite:

```
standing order "open fire": when the range is under 2 cables then fire as they bear
standing order "return her fire": at she opens fire then fire as they bear
standing order "she strikes": at the enemy strikes then cease firing
```

Morale is the one new quantity: the company's readiness to fight on, from the captain's doctrine (a King's ship's company starts high and fights to a wreck; a merchant crew's starts low and strikes to the first broadside into her), the losses, the guns dismounted, the masts gone and the odds while under fire. When it falls under the doctrine's line while she is under fire and a shot has told, the colours come down by rule and the log says why:

```
! Forenoon watch (11:12)  The colours are struck: five of 30 hurt, against a broadside of 36 pounds to our 13; the hands will not stand to the guns. The guns fall silent and she lies to for her captor.
```

What follows the colours down (the prize crew, the prisoners, the captive's channel) is not yet in the game; this chapter ends at the colours struck and the firing ceased.

## The first action

`data/scenarios/first-action.yaml`: the King's cutter *Sherbourne* cruising off the Lizard on a June forenoon, the French privateer cutter *Renard* a mile and a half to the south-east. Played by the rules captains alone at seed 7, the privateer engages at 10:07 and opens at long shot at 10:13; the King's cutter closes, returns her fire, and the colours come down at 11:43 with four of thirty hurt and seven shot holes. At a cable the same two cutters settle it in three minutes. Nothing pre-defines which: the range the captains keep decides it, and the seed.

## Practice at the great guns

A captain of 1805 was "to exercise the Ship's company frequently at the guns", and to have the times of it written in the log (the Regulations, the Captain, Art. IX); the gunner was to teach the men at their quarters to point the guns (Art. XI), and to issue for it, each month of her first six, a charge of powder and a round shot for a fourth of the upper deck's guns in a ship of one deck (the Gunner, Art. XXI: the frigate's six, the brig-sloop's four, the King's cutter's one). `data/scenarios/exercising-the-great-guns.yaml` is such a forenoon: the frigate south of the Lizard with nobody in sight. Under the rules captains with no model seated nothing happens there; the practice is the player's. It comes in two kinds, and practice improves no skill of the crews': the gun deck keeps each gun's drill and nothing reads it for pace or aim.

**Dumb show.** At quarters, `exercise the guns` (or `exercise the starboard battery`, `exercise both batteries`; with no side said, the engaged side, else both) has the crews serve every phase by its time, the sponge to the point, with no powder taken from the magazine and no shot leaving the ship. Given before `cast loose the guns`, the cycle begins empty; a gun already loaded is run out and pointed only, and keeps its charge. It is refused while a sail is engaged. The broadside at the word is refused while the guns are exercised; a gun fired by name, or the gun to leeward, fires as it would. `cease exercising`, any `engage`, `secure the guns`, the hands piped down from quarters and the colours struck end it.

```
Exercise the starboard battery in dumb show: the guns served without powder, and no shot leaves the ship. The guns are not yet cast loose: say 'cast loose the guns'.
The battery is exercising in dumb show: no gun is fired at the word; say 'cease exercising' first.
```

**A cask for a mark.** `heave a cask overboard` (from the lee quarter unless you name one: `heave a cask overboard from the starboard quarter`) is two hands' work for a minute at the quarter, and holds nothing of the ship's: she may tack while they are at it. A cask already in the water is given up. By night, and in a world with no chart, it is refused, since nobody could see the cask:

```
Hands to the quarter: an empty cask over the side for a mark.
The mark is over the side from the larboard quarter, an empty cask with a flag on a staff.
```

The cask floats where it fell, set by the tide's stream and a little to leeward by the wind. The masthead makes it out by day within a mile and the visibility, at twilight within half that, and never by night; it is never hailed, `what is in sight` names it "the mark", and `the bearing of the mark` reads where it lies. `engage the cask to larboard` lays the battery for it ("the mark" and "the target" mean the cask while one is in the water, and a sail otherwise), and the gun captains lay for it by the truth, as for a ship, and fire as it bears and within their reach: bring it onto the beam. A cask is a small mark, about a sixth of a frigate's hull for the hit chance, and the first shot that strikes it knocks it to staves. It is lost to sight and made out again once each way, and given up when she is three miles from it:

```
The mark struck by No. 3 starboard gun at two cables and knocked to staves; the guns hold their fire for want of a mark.
The mark is lost to sight in the haze.
The mark is made out again, bearing SE by S, about three cables.
The mark is lost astern, three miles off.
```

A mark is no sail: nobody is fired into, nobody's colours are judged, no ship or port hears of it, and nobody's temper moves.

**A notional mark.** `engage a mark four cables on the starboard beam` (on the bow, the beam or the quarter, where a gun of hers bears; from a cable to the longest random shot of the guns that bear) lays the battery for a mark that is only the captain's word: a cutter's length, beam-on wherever she heads, by night and in fog alike. The minute's line says the fall of shot "on the mark", and `the range` is the range you laid it at. The mark keeps its bearing from her head as she turns, so it is refused where no gun of hers can bear: a broadside gun bears within about three points of the beam, and a chaser within about two of right ahead or astern, so the frigate's guns bear on neither the bow nor the quarter, while a swivel or a pivot gun may. The guns that do not carry so far are named, and a mark beyond them all is refused:

```
Engage the mark six cables on the starboard beam: the starboard battery, the guns to fire as they bear; her 32-pounder carronades do not carry six cables.
No gun of hers carries ten cables: her long 18-pounders' random shot is 9.9 cables.
No gun of hers bears on the starboard bow, and a notional mark keeps its bearing from her head as she turns: say 'engage a mark four cables on the starboard beam'.
```

`fire at the mark` is not the way to it ("to fire at the mark, say 'engage the mark to starboard' and 'fire'").

**The reading.** `the practice` (or `the exercise`, `the gun drill`) gives each gun's rounds in dumb show and live, the mean and the best from the sponge to the point, the falls of shot at the mark by cables, the mark with its bearing and range and whether it is in sight, and in a King's ship the month's live rounds against the allowance; "none" when there has been none. The first live round beyond the month's allowance is said once and entered in the gunner's account: "Beyond the allowance for exercise this month (six charges by the Regulations, the Gunner, Art. XXI): the powder past it is spent on the captain's word, and the gunner's account keeps it." `the guns` says "exercising the starboard battery in dumb show" while it lasts.

**The gunner's filling.** The magazine holds filled cartridges by gun and loose powder in the barrels below, and the gunner fills more as the guns use them. `fill cartridges` has him report when they are filled to the allowance again, and `cease filling` shuts the magazine until he is ordered:

```
The gunner fills cartridges from the powder below: 181 of 330 for the 12-pounder carronades, 2 barrels below; by day, and at quarters with a man of the powder to spare.
The gunner fills no more cartridges until he is ordered; the magazine shut.
```

## Where to read more

Douglas, *A Treatise on Naval Gunnery* (1820), for the exercise of the guns and the effect of shot; Lavery, *The Arming and Fitting of English Ships of War*, for the guns and their carriages; the Establishments and Winfield for what each class carried; Falconer for the words; every figure is in the files with its source or marked judgement.
