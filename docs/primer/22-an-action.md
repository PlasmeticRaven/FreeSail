# 22. An action

From clearing for action to the colours struck, in the player's words (package 70; spec M7 §7 to §12). What the game can fairly do with a fight between two ships in 1805, and no more: the guns as parts of the ship with their crews from the muster, served by a cycle that runs while hands and powder last; the shot's fall by the range, the heel and the sea; a hit as a change of the state the ship already has (a line parted, a spar carried away, a sail holed, a gun dismounted, a shot hole, a man hurt); the company's temper, and the colours that come down when it fails. The marines' fire, the fight on deck, the water from the holes and the surgeon are later chapters' (the milestone's next packages); the prize is another's.

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

Each shot is laid for the range by its gun captain, the quoin answering only so far: the lee battery fires lower and shorter and the weather battery higher and longer by the heel, a lee port whose sill is within a foot of the water is shut and its gun silent, and the sea scatters the shot by its height and the roll. The hit chance falls with the range from nine in ten at pistol shot to one in two at point blank (250 yards for a long gun, 230 for a carronade) and a fifth at twice it. Your log says what your people can see of your own fire, once a minute; the ship fired at says what hers can see of it:

```
* Forenoon watch (10:04)  Three shot at a cutter: one struck her and two wide. A shot struck her between wind and water.
! Forenoon watch (10:05)  Shot from a cutter: two shot through the side to starboard; three killed and one wounded.
```

`the enemy` reads the mark in the lookout's words with her range in cables by his estimate; `the range` compares in the standing dialect (`when the range is under 2 cables then fire as they bear`).

## The damage

No second model of the ship exists for the fight. A hit is a change of state the game already has: a line shot away comes down as a parted line does, a spar shot away is cleared as a wreck is, a sail holed draws the less, a gun dismounted is out of the bill, the wheel shot away loses you the helm until the relieving tackles are rove, a shot hole is written with its place against the waterline for the well to read when the water comes (the next package's), and the men at the part struck are killed and wounded in the muster, off the bill. The carpenter's and the boatswain's report:

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
! Forenoon watch (12:06)  The colours are struck: five of 30 hurt, against a broadside of 36 pounds to our 13; the hands will not stand to the guns. The guns fall silent and she lies to for her captor.
```

What follows the colours down (the prize crew, the prisoners, the captive's channel) is a later package's; this one ends at the colours struck and the firing ceased.

## The first action

`data/scenarios/first-action.yaml`: the King's cutter *Sherbourne* cruising off the Lizard on a June forenoon, the French privateer cutter *Renard* a mile and a half to the south-east. Played by the rules captains alone at seed 7, the privateer engages at 10:06 and opens at long shot at 10:13; the King's cutter closes, returns her fire, and the colours come down at 12:06 with five of thirty hurt and eight shot holes. At a cable the same two cutters settle it in three minutes. Nothing pre-defines which: the range the captains keep decides it, and the seed.

## Where to read more

Douglas, *A Treatise on Naval Gunnery* (1820), for the exercise of the guns and the effect of shot; Lavery, *The Arming and Fitting of English Ships of War*, for the guns and their carriages; the Establishments and Winfield for what each class carried; Falconer for the words; the spec's M7 §7 to §12 for what is built and what is judgement, and `docs/dev/TuningNotes.md` (package 70) for every figure with its source and its measure.
