# Proposed spec: the pivot gun and its arcs (PROVISIONAL, 2026-10-25)

Written for the lead at the owner's word ("you may write the design up as a proposed
spec"), after a provisional pivot gun was built between packages to test how far the
armament of package 70 extends. It says what was built, what was measured in one action, and
what is proposed for package 75 (the ships' armament from their own records) or whoever next
takes the gun deck. Nothing here is decided: the lead and the owner settle it. Spec M7 §7
(guns as parts), §8 and §8a (the gunnery's cycle and the quarter bill) and rule 1 ("damage
is just state") bind as they bind every gun.

## 1. What a pivot gun was

A long gun on a slide carriage that turns about a pivot bolt on the deck. Its trucks run on
iron racers, the rings let into the deck, so that it trains round to either side and fires
over the rail (en barbette) where a broadside gun fires through its own port. The Baltimore
privateers of the War of 1812 carried a long 12, 18 or 24 so mounted amidships between the
masts, the "long Tom", with a few carronades or light long guns on the broadside. Pivoting
carronade slides were older, and the pivot long gun of 1805 is at the early edge of the
type's period. (Chapelle, *The Baltimore Clipper*, 1930, on the type's armament; from
memory, UNVERIFIED against a page, as the generator's gun figures are.) The owner wants the
mounting later for HMS *Dolphin*, so it is built as a general place any ship file can give
a gun, not as the schooner's.

## 2. As built (provisional, outside any package)

- **The place.** `pivot` joins `broadside`, `bow`, `stern` and `rail` in `GUN_PLACES`
  (`freesail/ship/schema.py`). A pivot gun has no side, and the load refuses one; it may
  have a number. It is named "the pivot gun" ("the No. 2 pivot gun" when numbered) and has
  its own crew by the gun's rule (`pair_key` is its id).
- **The training.** `Gun.train_deg` is a pivot's relative bearing from the bow, starboard
  positive, nought secured fore and aft. Cast loose, its crew trains it round toward the mark
  the shorter way at `PIVOT_TRAIN_DEG_S` (3 degrees a second, half a circle in a minute) with
  the full crew. Short-handed it trains in proportion; with nobody at it, not at all; with no
  mark it holds where it points (`Battery._train_pivots`, `freesail/combat/guns.py`).
- **The arc.** It bears when the mark is within the open arc on either side and the gun is
  trained within `PIVOT_ON_DEG` (5 degrees) of her. The arc is one band for every pivot,
  `ARC_PIVOT_FROM_DEG` to `ARC_PIVOT_TO_DEG` off the bow. It was 30 to 150 at first, and is
  now **60 to 140** at the owner's word, the schooner's reasoned arc (§3). The owner's rule:
  the gun is fired only where that is safe enough.
- **The rest of the gun deck.**
  - The pivot is served whichever side is engaged, as a chaser is.
  - It fires in any broadside or "as they bear" when it bears.
  - It is on the lee side when trained to leeward (the heel's elevation rule).
  - A shot on the deck may strike it from either side.
  - The quarter bill draws its crew with the broadside guns' and names it "the pivot gun"
    when robbed.
  - The orders know `fire the pivot gun` and `fire the long Tom`.
  - The graph's export carries `train_deg` for a pivot alone, for the view.

  A pivot changes nothing on a ship without one.
- **The ship.** `data/ships/privateer-schooner.yaml` is the topsail schooner's hull, rig and
  company with two fits:
  - `long tom`, the default (the owner's loadout): a long 12-pounder on the pivot at +2.6 m,
    between the fore mast at +7.8 and the main at -2.6, four 12-pounder carronades two a side
    clear of its sweep, and four swivels;
  - `letter of marque`: six long 6-pounders and four swivels.

  The description `privateer schooner` (also "an armed schooner", "a letter of marque")
  sails it at far detail. The tops make her out "a schooner", the glass "a topsail schooner,
  pierced for guns". `topsail-schooner.yaml` is untouched: the trade trial's merchant
  schooner, armed, engaged the privateer where the trial has her haul off, so the guns live
  in a file of their own.
- **Tests.** `tests/test_pivot_gun.py` covers the arc, the training and its pace, serving,
  the lee side, the orders and the load's refusal. `tests/test_ships.py` checks both fits
  and that the privateer is the schooner's hull. `tests/test_ship_particulars.py` checks
  that the generator writes the new file.

## 3. The arc from the rig, worked for the schooner

From the pivot at +2.6 m, with a half-beam of 3.65 m:

| What stands in the way | Where | Bearing from the pivot, off the bow |
|---|---|---|
| The fore mast, the forestay, the jib stay and the bowsprit | the centreline, ahead | 0 |
| The fore shrouds, set up in the channel abeam of the fore mast | x +7.8, the rail | about 35 |
| The fore topmast backstays, in the channel abaft the shrouds | x about +4.8, the rail | about 55 to 60 |
| *open: over the rail* | | *60 to 140* |
| The main shrouds, abeam of the main mast and spreading aft | x -2.6 to about -4.5, the rail | about 140 to 150 |
| The main mast, the main boom amidships, the helm | the centreline, astern | 180 |

So the gun fires clear over the rail from just abaft the fore backstays to just forward of
the main shrouds, 60 to 140 off the bow on either side. Forward of that, the shot passes
through the fore rigging and over the forecastle's men; abaft it, through the main rigging
and over the quarterdeck. The pivot stands midway between the masts, 5.2 m from each, and
the arc is still lopsided toward the beam's after side. The fore topmast backstays lead aft
of the fore shrouds, toward the pivot, while the main rigging spreads aft, away from it.
Moving the pivot a metre or two aft would even it.

## 4. Proposed: each pivot's arcs from its own ship

1. **Arcs on the gun.** `arcs_deg: [[from, to], ...]` on a gun in the ship file, the open
   arcs off the bow, mirrored to both sides. A gun without it takes its place's default (the
   present constants), so every existing file keeps its figures.
2. **Written by the generator, with the reasoning beside each figure.** The generator
   computes the open arcs from:
   - each mast's x;
   - the half-beam at the rail;
   - each mast's channel: the shrouds abeam of the mast and spreading aft;
   - the topmast backstays further aft, their spread a stated judgement from Luce 1866
     (the channels and the chain plates) and Steel 1794 (the rigging's leads);
   - the stays and the bowsprit on the centreline;
   - a margin either side for the muzzle's blast on the rigging (judgement, say five
     degrees).

   It writes them into the gun's entry with the computation in the note, as it writes a
   spar's rating. The *Dolphin*'s pivot then gets its arcs from her own rig without a figure
   by hand.
3. **The boom, at runtime (optional).** The main boom broad off to one side blocks that
   side's quarter, from the main shrouds' bearing to the boom's end, while it is out. Read
   from the boom's angle (the main sheet's state), a mark in that sector does not bear, and
   the battery's line says so once ("the boom is in the way of the pivot"). A schooner on a
   broad reach with the boom out to leeward could not fire her long Tom on her lee quarter,
   which is true, and asks the captain to alter course or gybe.
4. **Elevation over the rail.** A pivot fires over the rail, not through a port, so the lee
   port's shutting (spec M7 §9) does not apply to it. Its height is the rail's. Note that
   `shot.lee_port_shut` is not called anywhere in the gunnery today (found on the way, §5):
   whoever wires it should leave the pivot out.
5. **Training at the racers.** The racers may not run the whole circle. On some ships the
   pivot could train only between the masts on each side, not across the centreline, and
   was shifted from one side to the other by a longer evolution (unshipping the slide). If
   a ship's sources say so, a `trains_across: false` on the gun makes the crossing an
   evolution of so many minutes instead of the training rate. The schooner's provisional
   pivot trains across the deck freely.

## 5. Found on the way (for the lead)

- **A long gun and a carronade of one calibre share one cartridge pool.** The magazine keys
  cartridges by the pounds of shot alone (`fit_magazine`, `parts.Magazine`). In the action
  the privateer's four 12-pounder carronades fired 157 rounds and emptied the 12-pound
  cartridges, silencing the long 12 on the pivot with them. A carronade's charge was a small
  fraction of a long gun's of the same shot (from memory: about a twelfth of the shot's
  weight against a third), so the two should draw on separate cartridges, keyed by kind and
  calibre, the shot shared.
- **A captain whose magazine is out stays engaging.** The privateer lay at three cables
  "engaging" for the last hour with nothing to fire; neither the role's doctrine nor the
  morale has a row for an empty magazine (break off, run, or close and board).
- **`shot.lee_port_shut` is defined and never called**, though spec M7 §9 and package 70's
  record say a lee port within a foot of the water is shut. The schooner's ports are 3 ft 5
  in above the water upright, so they would shut at about twelve degrees of heel.
- **"The wheel is shot away"** is said for a tillered ship (the cutter and the schooner
  steer with a tiller); `hits.py`'s helm line could take the ship's steering from her file.
- **A new vessel type touched code in two places**: the description's words
  (`world/ships.py` `DESCRIPTIONS`, `_DESCRIPTION_WORDS`) and the size rank
  (`world/captains.py` `SIZE_RANK`). Both could be read from the ship files' own
  `descriptions` (which the generator already writes for the brig), so that package 75's
  sub-types are data alone.

## 6. One action, measured

The first action (`data/scenarios/first-action.yaml`) at seed 7 with the Renard replaced by
the privateer schooner (the Basque), both rules captains, three hours, a scratch scenario
not committed:

| | Letter of marque (six long 6-pounders) | Long Tom (the pivot and four carronades) |
|---|---|---|
| Her fire | 133 rounds of 6-pound shot | 62 from the pivot, 157 from the carronades, the 12-pound cartridges out at 1 h 52 min |
| The King's cutter's fire | 37 | 38 |
| The King's cutter's damage | the main topmast, topgallant mast, gaff, boom and two yards carried away; a gun dismounted; two men killed | the main gaff carried away; five lines parted; five shot holes, one at the waterline; a gun dismounted |
| Her own | four shot holes, three hurt | two shot holes, three hurt; the pivot's carriage struck |
| The end | the range opened, both broke off, nobody struck | both still engaging at three cables at the end, her magazine out |

The pivot trained to the larboard quarter, 110 to 128 degrees off the bow, and held there,
abaft any broadside gun's arc. The King's cutter's carronades bore little of the
afternoon, which is the pivot's case in one action. These figures were taken with the first
arc of 30 to 150; the narrower arc moves them, and they are judgement for the tuning, not
pins.
