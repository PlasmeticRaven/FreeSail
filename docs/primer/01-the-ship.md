# 1. The ship

Every noun the parser accepts is a part of the ship, a group of parts, or an alias for one, and all of them come from the ship file (`data/ships/frigate-36.yaml`, `data/ships/topsail-schooner.yaml`). This chapter walks the two ships from forward to aft and from the deck upward, naming each part as an officer of 1805 would have named it, so that you can point at anything. Definitions are Falconer's unless another source is given.

## How names work

A part has an id in the file, such as `fore.topsail.yard`, and the parser accepts it as words: "fore topsail yard". It also accepts the contractions a seaman would use (Falconer prints them; Luce speaks them): *tops'l*, *t'gallant*, *stuns'l*, *cro'jack*, *stays'l*, *halliard*. Apostrophes may be left out. "Port" is accepted for larboard and echoed in the log as larboard. "The" is ignored.

Some rules that will save you refusals:

- A name that fits only one part is enough: `set the topsail` names the fore topsail on the schooner, which has one, and is refused on the frigate, which has three.
- A sided part (a brace, a sheet of a jib, a studding sail) needs its side: *starboard*, *larboard*, *weather*, *lee*, or *both sides*. The side may come before the noun or after a comma. *Weather* and *lee* are worked out from the tack she is on at the moment you speak.
- The name of a sail names the lines of that sail and of its yard: "fore topsail sheet", "main brace" (for `main.yard.brace`), "spanker peak halyard".
- The plural of a sided line means both sides: "the fore topsail sheets", "the main braces"; with a side word it means that side ("the lee fore topsail sheets" is the one lee sheet). A plural shorthand names all of them: "the topsail sheets" is six lines on the frigate.
- Two things may be named with *and*: "the topsails and topgallants", "the jib and the spanker", and, distributed, "the fore and main yards" for the fore yards and the main yards.

```orders frigate
set the fore tops'l
set the main t'gallant
haul the weather main brace
ease the jib sheet, lee
let go the fore topsail sheet, port
ease the fore topsail sheets
ease the lee fore topsail sheets
set the topsails and topgallants
brace the fore and main yards square
# rejected: set the topsail
# rejected: haul the main brace
# rejected: set the fore topsail yard
```

The three refusals are the three commonest: an ambiguous shorthand ("The topsail could be the fore topsail, the main topsail or the mizzen topsail; say which"), a sided line without its side ("Which main brace: the starboard, the larboard (the weather or the lee), or both sides?"), and a verb used on the wrong kind of part ("You set sails; the fore topsail yard is a yard. Did you mean the fore topsail?").

## The frigate *Amazon*: a ship-rigged 36

*Ship-rigged* means three masts, all square-rigged. The parts:

### Masts

Each mast is made in sections, one stepped on the head of the one below (Falconer, *Mast*; Luce 1866, ch. VII The Mast): the **lower mast**, the **topmast**, the **topgallant mast** and the **royal mast**. The game names them `fore.mast`, `fore.topmast`, `fore.topgallant_mast`, `fore.royal_mast`, and the same for **main** and **mizzen**. The **bowsprit** runs out over the bow with the **jib-boom** and **flying jib-boom** beyond it. You do not give orders to masts in this milestone (sending down topgallant masts is later work), but their names appear in the log when something carries away.

### Yards and the sails on them

A **yard** is the spar a square sail hangs from, slung across the mast (Falconer, *Yard*). From the deck up on each mast:

| Yard | Sail on it | Reef bands |
|---|---|---|
| fore yard | **fore course**, also *foresail* | 1 |
| fore topsail yard | **fore topsail** | 3 |
| fore topgallant yard | **fore topgallant** | none |
| fore royal yard | **fore royal** | none |
| main yard | **main course**, also *mainsail* | 1 |
| main topsail yard | **main topsail** | 3 |
| main topgallant yard | **main topgallant** | none |
| main royal yard | **main royal** | none |
| crossjack yard (*cro'jack*) | none: it spreads the foot of the mizzen topsail | |
| mizzen topsail yard | **mizzen topsail** | 3 |
| mizzen topgallant yard | **mizzen topgallant** | none |
| mizzen royal yard | **mizzen royal** | none |

The **courses** are the lowest square sails (Falconer, *Courses*); the mizzen carries no course, which is why the crossjack yard is bare. The **topsails** are the working sails of the ship and carry three reefs (Falconer, *Reef*: "the top-sails of ships are usually furnished with three reefs"). The **topgallants** and **royals** are the light sails, first in and last out.

Abaft all is the **spanker** on the **mizzen gaff** and **mizzen boom**, a gaff sail with two reef bands. Falconer's *Driver* is a lighter sail set in its place in fair winds; by 1805 the two words meant the same thing and the game takes *spanker*, *driver* or simply *the mizzen* for it (Falconer, *Mizen*: "the aftermost or hindmost of the fixed sails of a ship, extended sometimes by a gaff").

### Headsails and staysails

Set on the stays running forward from the masts (Falconer, *Stay*, *Jib*): the **fore topmast staysail** on the fore topmast stay, the **jib** on the jib stay, the **flying jib** on the flying jib stay. These three are the **headsails**. The **main topmast staysail** sets between the masts. Together with the spanker they are the ship's **fore-and-aft sails**.

### Studding sails

*Stuns'ls*: "light sails extended, in moderate and steady breezes, beyond the skirts of the principal sails, where they appear as wings upon the yard-arms" (Falconer, *Studding-sails*). Each is named for the mast section it belongs to and the side it is on: **fore lower**, **fore topmast**, **fore topgallant**, **main topmast** and **main topgallant** studding sails, starboard and larboard, ten in all. Each has its **studdingsail boom** on the yard beneath it. There are none on the mizzen.

```orders frigate
set the fore topmast studdingsail, starboard
set the larboard fore topmast stuns'l
set the main topgallant studdingsails
set the studdingsails, lee
# rejected: set the fore topmast studdingsail
# rejected: set the mizzen topgallant studdingsail
```

### The lines of a square sail

Every square sail and its yard carry the same set of lines, and the parser knows them all by the sail's name (Falconer under each head; Luce 1866, ch. X Rigging Ship):

| Line | Sided | What it does |
|---|---|---|
| **halyard** (*halliard*) | no | hoists the yard; the courses' yards do not hoist and have none |
| **braces** | yes | swing the yard round in the horizontal: "a rope employed to wheel, or traverse the sails upon the mast" (Falconer, *Brace*) |
| **lifts** | yes | hold up the yardarms |
| **sheets** | yes | haul the lower corners (the *clews*) out to the yardarms below, or, for a course, aft |
| **tacks** | yes | courses only: haul the weather clew forward and down (Falconer, *Tack*) |
| **bowlines** | yes | courses only: hold the weather edge (the *leech*) steady when close-hauled |
| **clewlines** | yes | haul the clews up to the yard to take the sail in |
| **buntline** | no | hauls the middle (the *bunt*) up to the yard |
| **reef tackles** | yes | topsails and courses: haul the reef band out to the yardarm for reefing |

The courses' sheets, tacks and bowlines go by the old short names as well (Falconer, *Main-sheet*, *Tack*, *Bowline*): "the main sheet" on a ship-rigged vessel is the main course's sheet, and asks for its side like any sided line; "the fore tack", "the main bowline" likewise. The plural, "the main sheets", is both.

Standing rigging, the **stays**, **shrouds** and **backstays** that hold the masts up, and the **bobstay** and **martingale** under the bowsprit, is named too, but the parser will not let you haul on it: "The starboard main shrouds are standing rigging; set up with deadeyes and lanyards, not hauled."

```orders frigate
ease the fore topsail halyard
haul the lee main brace
ease the weather fore topsail brace a fathom
let go the fore course tack, weather
belay the main topsail halyard
ease the weather main sheet
ease the lee fore tack
ease the main sheets
# rejected: haul the main shrouds, starboard
# rejected: haul the fore topsail
# rejected: haul the fore tack
```

The second refusal is instructive: "You haul lines; the fore topsail is a sail. Name one of its lines: the fore topsail sheet, the fore topsail clewline, ..." The ship tells you what she has. The last is the sided line without its side: "Which fore tack: the starboard, the larboard (the weather or the lee), or both sides?"

### The lines of a gaff sail and a jib

The spanker has a **throat halyard** and a **peak halyard** for the two ends of its gaff, a **sheet**, an **outhaul** along the boom, and **vangs** either side to steady the gaff ("a sort of braces to support the mizen gaff", Falconer, *Vangs*). A jib or staysail has a **halyard**, **sheets** on each side, and a **downhaul**. A studding sail has a **halyard**, a **tack** to its boom end, a **sheet** and a **downhaul**.

```orders frigate
ease the spanker sheet a fathom
ease the spanker peak halyard
ease the mizzen gaff vang, lee
ease the jib sheet, lee
let go the jib halyard
ease the fore topmast staysail sheet, lee
```

### Groups

A group name orders every member at once, and each member gets its own evolution. The frigate's groups:

| Group | Members |
|---|---|
| **courses** | fore and main course |
| **topsails**, **topgallants**, **royals** | the three of each |
| **headsails** | fore topmast staysail, jib, flying jib |
| **staysails** | fore and main topmast staysails |
| **studdingsails** (*stuns'ls*, *kites*) | all ten; add a side to take one side |
| **square sails** | courses, topsails, topgallants, royals |
| **fore-and-aft sails** | headsails, main topmast staysail, spanker |
| **plain sail** | courses, topsails, topgallants, fore topmast staysail, jib, spanker |
| **all sail** | everything |
| **fore yards**, **main yards**, **mizzen yards** | the yards on that mast |
| **head yards** | the fore yards |
| **after yards** | the main and mizzen yards |
| **yards** | all twelve |

```orders frigate
set the topsails
set the courses
set the headsails
brace the head yards sharp up on the starboard tack
brace the after yards square
brace the mizzen yards up
```

## The schooner *Speedwell*: a Baltimore topsail schooner

Two masts, **fore** and **main**, each with a lower mast and a topmast, and a topgallant mast on the fore. The working sails are fore-and-aft; the fore topmast crosses two yards, which is what makes her a *topsail* schooner (Luce 1884, ch. XXXIV Handling Fore-and-Afters, for the rig's parts).

| Part | What it is |
|---|---|
| **foresail** (*the fore*, `fore.sail`) | gaff sail on the fore gaff, loose-footed (no boom); two reef bands |
| **mainsail** (*the main*, `main.sail`) | gaff sail on the main gaff and main boom; three reef bands |
| **gaff topsail** (`main.gaff_topsail`) | a jib-headed sail set above the mainsail on the main topmast |
| **fore topsail** | square, on the fore topsail yard; two reef bands. *The topsail* is enough |
| **fore topgallant** | square, on the fore topgallant yard. *The topgallant* is enough |
| **fore staysail** (*the staysail*) | on the fore stay |
| **jib**, **flying jib** | on the jib stay and flying jib stay |
| **fore topmast studdingsails** | one each side of the fore topsail |

Lines follow the same rules. The mainsail's sheet is one line (a boom sail sheets from the boom end): "the main sheet". The foresail, being loose-footed, has a sheet each side. The gaffs have throat and peak halyards; the main gaff has vangs. The groups are **topsails**, **topgallants**, **square sails**, **headsails**, **fore-and-aft sails**, **studdingsails**, **plain sail** (foresail, mainsail, fore topsail, fore topgallant, fore staysail, jib), **all sail**, and **yards** or **fore yards** (the two yards).

```orders schooner
set the foresail
set the main
set the topsail
set the topgallant
set the gaff topsail
set the staysail
ease the main sheet a fathom
ease the fore sheet, lee
ease the main peak halyard
haul the weather fore topsail brace
brace the yards square
# rejected: set the mizzen topsail
# rejected: set the royals
# rejected: brace the main gaff sharp up
```

The last: "The main gaff is a gaff, not a yard; the gaff sail on it is not braced; it is trimmed with its sheet and vangs." Chapter 4 says how.

## The cutter *Sherbourne*: a revenue cutter of 85 tons

One mast, **the main** (*the mast* will do: there is no other), a lower mast with a topmast and a short topgallant pole above it, no tops, and a **running bowsprit** that is run in and out along the deck through the gammoning rather than fixed to the stem (Fincham 1843, art. 86; Luce 1884, ch. XXXIV, for the cutter's rig). The working sails are the great boom mainsail, the foresail and the jib; three square sails cross the one mast for going free.

| Part | What it is |
|---|---|
| **mainsail** (*the main*, `main.sail`) | gaff sail on the main gaff and main boom, the boom reaching well over the taffrail; four reef bands (Steel 1794) |
| **foresail** (*the fore*, *the staysail*, `fore.staysail`) | a staysail on the fore stay, not a gaff sail: a cutter's foresail is her staysail |
| **jib** | on the jib stay, its tack at the bowsprit end, so it comes and goes with the bowsprit |
| **gaff topsail** | jib-headed, above the mainsail on the topmast |
| **square sail** (*the crossjack*, `square_sail`) | on the square-sail yard under the mast head, set only off the wind |
| **topsail** (*the main topsail*) | square, on the topsail yard on the topmast; one reef band |
| **topgallant** | square, on the topgallant yard on the pole |
| **storm trysail**, **storm jib** | in the sail room, bent in the mainsail's and the jib's places for a storm |

She has no flying jib, no royals, no studding sails and no spanker: **plain sail** is the mainsail, the foresail, the jib and the topsail; **all sail** adds the gaff topsail, the square sail and the topgallant, which are her **light sails**. Her three yards are **the yards** (or *the main yards*); she has no head or after yards to brace apart. The bowsprit has a **heel rope** to run it out with, and chapter 3 says how it is reefed.

```orders cutter
set the mainsail
set the foresail
set the jib
set the topsail
set the square sail
set the gaff topsail
reef the mainsail, two reefs
ease the main sheet a fathom
ease the fore sheet, lee
haul the weather topsail brace
brace the yards square
strike the topmast
# rejected: set the spanker
# rejected: set the fore topsail
# rejected: set the studdingsails
# rejected: brace the head yards square
```

The refusals name what she has instead: "There is no such part as the fore topsail in this ship; did you mean the foresail, the gaff topsail or the topsails?"

## The brig *Harpy*: a brig-sloop of 316 tons

The frigate less a mast: **fore** and **main**, each a lower mast, topmast, topgallant mast and royal pole, three yards and a royal yard on each, tops on both, a bowsprit with a jib-boom and a flying jib-boom, and a gaff and boom on the main for the **spanker** (*the driver*, *the boom mainsail*, *the trysail*: a brig's is all four), which is the largest sail she has. Everything in the frigate's table that is not the mizzen's is hers, at her size: the courses, topsails, topgallants and royals, the fore topmast staysail, jib and flying jib, the main staysail, main topmast staysail (*the middle staysail*) and main topgallant staysail, ten studding sails, and the storm staysails and storm trysail in the sail room. The **head yards** are the fore's and the **after yards** the main's, so *square the after yards* and *back the main topsail* work as they do on the frigate; there is no crossjack, no mizzen and nothing of the mizzen's to name.

```orders brig
set the fore topsail
set the topsails
set the courses
set the royals
set the spanker
ease the spanker sheet
brail up the driver
set the middle staysail
set the fore topmast studdingsail, larboard
square the after yards
back the main topsail
brace the fore and main yards square
haul the weather main brace
send down the topgallant masts
# rejected: set the mizzen topsail
# rejected: set the crossjack
# rejected: brace the mizzen yards square
```

The refusal: "There is no such part as the mizzen yards in this ship; did you mean the main yards, the head yards or the fore yards?" Her bowsprit is gammoned fast to the stem, so *reef the bowsprit* is refused on her ("only a cutter's running bowsprit reefs").

## What you cannot yet name

There is no anchor, cable, boat, gun, pump or log-line in any of the four files yet, and no crew; `let go the best bower` is refused with "There is no such part as the best bower in this ship." Those come with later milestones (`docs/DesignProposal.md` §11). The masts can be named but not sent down.
