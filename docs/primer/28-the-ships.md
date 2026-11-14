# 28. The ships

Every ship in the game is a file of her own under `data/ships/`, drawn from her lines and the accounts of her day, and any of them may be yours: name her file to the console as the introduction names the frigate's, or in a scenario's `ship:`, and the orders of this book are hers by the parts she has. Chapter 1 named the parts of the frigate, the schooner, the cutter and the brig, and chapter 2 the lugger's and the smack's. This chapter is the whole list, with the ships of two decks, the razee, the hermaphrodite brig and the bilander, which the earlier chapters do not name; and the trades a hull serves under another name, which a scenario chooses.

```
python -m freesail.ui.console data/ships/seventy-four.yaml --seed 7 --wind 0,15 --heading 293
```

## The list

Each ship as she comes, her guns her file's first fit; a scenario's `fit:` names another of hers. The last column is what the tops make of her: her rig within four miles, and what she is within a mile and a half (chapter 15).

| Her file | Her name, and what she is | Her company | Her guns as she comes | What the tops make of her |
|---|---|---|---|---|
| `frigate-36.yaml` | the *Amazon*, a frigate of 36 guns | 264, 40 of them marines | 26 long 18-pounders, 10 32-pounder carronades, 4 long 9-pounders | a ship; a frigate |
| `brig.yaml` | the *Harpy*, a brig-sloop of war | 121, 20 marines | 16 32-pounder carronades, 2 long 6-pounders | a brig; a brig-sloop of war, ten ports a side |
| `merchant-brig.yaml` | the *Industry*, a merchant brig | 16 | 4 long 6-pounders | a brig; a merchant brig, deep laden |
| `cutter.yaml` | the *Sherbourne*, a cutter of 85 tons | 30 | 6 12-pounder carronades (`long guns`: 6 long 3-pounders and 8 swivels) | a cutter |
| `topsail-schooner.yaml` | the *Speedwell*, a Baltimore topsail schooner | 40 | none (`letter of marque`: 6 long 6-pounders and 4 swivels; `musquidobit 1813`: 8 18-pounder carronades and 2 long 6-pounders) | a schooner; a topsail schooner |
| `privateer-schooner.yaml` | the *Speedwell* fitted as a privateer | 40 | a long 12-pounder on a pivot amidships, 4 12-pounder carronades and 4 swivels (`letter of marque`: 6 long 6-pounders and 4 swivels) | a schooner; a topsail schooner, pierced for guns |
| `lugger.yaml` | the *Éclair*, a chasse-marée | 30 | none (`gun lugger 1795`: 3 long 18-pounders over the rail) | a lugger; a chasse-marée, three-masted under lugs |
| `smack.yaml` | the *Culloden*, a fishing smack | 8 | none (`culloden 1746`: 2 long 3-pounders) | a smack; a fishing smack, her well amidships |
| `sixty-four.yaml` | the *Indefatigable* as built, a sixty-four | 491, 84 marines | 26 long 24-pounders, 26 long 18-pounders, 12 long 9-pounders (`ardent class 1794`: 8 carronades more) | a ship of the line; a sixty-four, a ship of the line of two tiers of ports |
| `razee-44.yaml` | the *Indefatigable* razeed, a heavy frigate | 330, 50 marines | 26 long 24-pounders, 18 42-pounder carronades, 2 long 12-pounders (`as razeed 1795`: 12 long 12-pounders and 6 42-pounder carronades over her 24s) | a ship; a razee, a heavy frigate cut down from a sixty-four, one tier of twenty-four-pounders |
| `seventy-four.yaml` | the *Bellerophon*, a seventy-four | 590, 111 marines | 28 long 32-pounders, 28 long 18-pounders, 18 long 9-pounders, 8 carronades (`arrogant class 1793`: the long guns alone; `as the bellona 1812`: 8 long 12-pounders for her 9s, and 14 carronades) | a ship of the line; a seventy-four, a ship of the line, fourteen ports a tier |
| `hermaphrodite-brig.yaml` | the *Prince de Neufchatel*, an American privateer | 130, 16 marines | 16 12-pounder carronades, 2 long 6-pounders | a brig; a hermaphrodite brig, a brig's foremast and a schooner's main, long and low, pierced for eleven guns a side |
| `bilander.yaml` | the *Hopewell*, a coasting bilander | 9 | none (`armed merchant`: 4 long 3-pounders and 4 half-pounder swivels) | a bilander; a bilander, a merchantman under a settee main, deep laden |

## The ships of two decks: the sixty-four and the seventy-four

The *Indefatigable* as she was launched at Bucklers Hard in 1784, a sixty-four of the *Ardent* class, and the *Bellerophon*, a seventy-four of the *Arrogant* class launched in 1786, are the ships of the line of the list: three masts, two whole tiers of guns, and the heaviest on the lower deck, nearest the water (the sixty-four's 24-pounders, the seventy-four's 32-pounders). A gun of theirs is named by her deck as well as her number and side, each deck's pairs numbered from forward ("No. 3 starboard gun of the lower deck"), so that the lower deck's No. 3 is never the upper deck's.

**The lower ports.** The lower deck's sills stand some five feet above the water, so that a ship of the line heeling to a fresh breeze cannot fight her lee lower tier: heeled ten degrees and a third, the seventy-four's lowest lee port is shut, and the sixty-four's at ten and a half, where a frigate's upper-deck ports stand open to nearly twenty; a roll shuts them sooner by its swing. The guns behind a shut port are run in and fire nothing, and the port opens again only when its sill stands six inches clear and the sea has kept from it a full minute. With her guns cast loose the log says it once for the deck and side (chapter 22):

```
The lee lower-deck ports are shut, the sea at their sills.
```

**Their mizen is the older fashion:** a long mizen yard slung across the mast, never braced, and on it the mizzen course, a lateen cut at the mast, set, hauled aft at helm's a-lee and brailed up as a gaff's sail is; the driver lies in the sail room, and in a light fair wind `shift the mizen for the driver` sends the course down, sways the driver up and rigs out its boom, the work of a quarter of an hour and more. Under the bowsprit is the spritsail and beyond it the sprit topsail, each on its yard, which go round with the head yards at "let go and haul" and are clewed up when she heaves to.

```orders sixty-four plain-sail
set the spritsail
set the sprit topsail
brail up the mizzen course
set the mizzen course
shift the mizen for the driver
```

```orders seventy-four plain-sail
set the spritsail
set the sprit topsail
take in the mizzen course
```

**Who sees her.** The tops know a ship of the line by her two tiers at the distance they know a rig, and say "a ship of the line". A King's frigate or any lesser King's ship alone, knowing her an enemy (by her colours, the private signal unanswered, or a shot), hauls off from her within two leagues; a ship in a squadron leaves it to the squadron's book, and a ship under another's orders to her commander's.

## The razee

The *Indefatigable* razeed is the sixty-four cut down by a deck in 1795: her quarterdeck, her forecastle and their sides taken off, her old upper deck made her quarterdeck, her lower masts shortened, and her lower deck's twenty-six 24-pounders her one tier. She is rated a 44 and rigged as a frigate is, with a spanker on her mizen where the sixty-four has her mizzen course, and a spritsail under her bowsprit. She is lighter and stiffer than the ship she was cut from and faster on every point of sailing; her fits are the years', as razeed in 1795 and as carried from 1796 (her default, with the 42-pounder carronades). Her lee gun-deck ports shut at fourteen and a half degrees of heel.

```orders razee plain-sail
set the spritsail
ease the spanker sheet
```

## The *Prince de Neufchatel*

An American privateer built at New York in 1812-13 and taken by the *Leander*, the *Newcastle* and the *Acasta* in December 1814: a hermaphrodite brig, long and low, flush-decked, a brig's square foremast with her course, topsail, topgallant and royal, and a schooner's main with its gaff mainsail on a boom, a gaff topsail and a light topgallant above it; a large loose-footed fore gaff sail laps the mainmast. Close-hauled she outsails a frigate and lies nearer the wind; running, a frigate gains on her. Her company is a privateer's, a hundred and thirty men, a captain and five lieutenants among them, for the prizes they man, and her people are American. When she lies a-try her fore gaff sail is taken in. At a distance she is "a brig" to the tops; "a hermaphrodite brig" and "a privateer brig" name her.

```orders neufchatel plain-sail
set the main topgallant
set the main gaff topsail
set the royals
```

## The bilander

The *Hopewell* is a British coasting bilander of some hundred and twenty tons, a rig already old in the 1780s: a ship's square fore, with her course, topsail and topgallant, and on her main, under its topsail, topgallant and a dry yard, the settee, a long four-cornered lateen on a yard that stands, called her mainsail. It is set, clewed up and furled aloft on its yard. In stays it is kept drawing as a ship's mizen is, its ourse braced to leeward as the helm goes down, and once the head yards are swung its yard is lowered, passed round abaft the mast to the new lee side and hoisted again: "Dip the mainsail: lower the yard, pass it round abaft the mast ...". In wearing it is lowered as she bears up and hoisted on the new lee once her stern is past the wind. She heaves to with her main laid aback.

Her company is nine: six hands in two watches of three, the cook, the master and the mate. The master and the mate each head a watch, and haul with it at work on deck where the watch alone is too few for it, never aloft nor in a manoeuvre; where her watch is too few to begin her settee's work all hands are called for it and piped down after, and either watch alone heaves her to and fills away. She is unarmed as she comes; her armed merchant's fit gives her four long 3-pounders in her waist and four swivels on her quarterdeck rail.

```orders bilander plain-sail
take in the mainsail
set the mainsail
dip the mainsail
furl the mainsail
```

## The trades a hull serves

A hull may serve more than one trade, and a scenario names which by her description, in the words the lookout would use, and her captain's book with it where she is given an intent (chapter 15): `revenue cutter` puts the cutter's hull to sea with her long guns and the revenue's book, who speaks every sail she closes and keeps clear of the enemy's men of war; `hired armed cutter` the same guns and the cruiser's book; `coasting cutter` unarmed and the merchant's; `privateer lugger` the lugger with her three 18-pounders over the rail and the privateer's book; `privateer schooner` (also `letter of marque`) the armed schooner. `fit:` gives her another fit of her file, and `role:` another of her description's trades: the merchant brig's are the merchant's, the packet's and the armed Indiaman's, who holds her colours through the broadside that brings a merchantman's down. A role her description does not give is refused when the scenario loads.

```
ships:
  - {id: swift, description: revenue cutter, name: Swift, nation: britain,
     position: 49 55 N 5 45 W, goal: "patrolling off the Wolf within 4 miles",
     intent: "keep the station off the Wolf within 4 miles"}
  - {id: hindostan, description: merchant brig, role: indiaman, name: Hindostan,
     nation: britain, position: 49 40 N 5 30 W, goal: "bound for Falmouth",
     intent: "bound for Falmouth"}
```

## Where it comes from

Each ship's file carries the source of every figure beside it: her draughts and her lines where they survive, the lists of the Navy's ships for her dimensions and her guns, the period's tables for her masts, yards and sails, and the logs and letters of her own day for how she sailed. Where a figure has no source it is a judgement, and the file says so.
