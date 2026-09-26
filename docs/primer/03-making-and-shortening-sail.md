# 3. Making and shortening sail

## Plain sail

*Plain sail* is the working canvas of the ship: on the frigate the courses, the three topsails, the three topgallants, the fore topmast staysail, the jib and the spanker; on the schooner the foresail, mainsail, fore topsail, fore topgallant, fore staysail and jib. Everything beyond it, the royals, the flying jib, the main topmast staysail, the gaff topsail and the studding sails, is *light sail* or *all sail*. The ship file's `plain sail` and `all sail` groups say exactly which sails these are for each ship.

One order does it:

```orders frigate
set plain sail
```

and the log answers with one line per sail as the hands go to work, and one, marked `*`, as each is set:

```
  Morning watch (04:06)  Order: set plain sail.
  Morning watch (04:06)  Hands aloft to loose the foresail.
  Morning watch (04:06)  Hands aloft to loose the mainsail.
  Morning watch (04:06)  Hands aloft to loose the main topsail.
  ...
  Morning watch (04:06)  Clear away the fore topmast staysail; man the halyards.
  Morning watch (04:06)  Clear away the jib; man the halyards.
  Morning watch (04:06)  Hands to the spanker halyards and outhaul.
  Morning watch (04:07)  Laid aloft and loosed the foresail.
* Morning watch (04:07)  Set the fore topmast staysail.
* Morning watch (04:07)  Set the jib.
* Morning watch (04:09)  Set the spanker.
* Morning watch (04:09)  Set the foresail.
* Morning watch (04:09)  Set the mainsail.
* Morning watch (04:11)  Set the main topsail.
```

`make all sail` (*crowd sail*, *crack on*) sets plain sail and then the royals, flying jib, staysails, gaff topsail and studding sails both sides, passing over anything the ship has not got. `shorten sail` (*take in sail*, *snug her down*) takes in the studding sails, royals, flying jib, topgallants and gaff topsail and puts one reef in the topsails. These three are lists of ordinary orders in `data/vocabulary.yaml`; anything they cannot do is reported in the same log line after "Not done:".

## The order of setting

A ship sets sail from the middle out and takes it in from the outside in. Luce's chapter on the officer of the deck at sea gives the evolutions in the order they are wanted (Luce 1866, ch. XXIII At Sea, 'Making and Taking in Sail': courses, topsails, royals, topgallant sails, head sails, studding sails), and the sequence is:

1. **Topsails**, the sails that do the work and stand the most wind.
2. **Courses** and **head sails**, the drivers and the balance.
3. **Spanker**, to hold her up to the wind.
4. **Topgallants**, then **royals**, as the breeze allows.
5. **Studding sails**, in a fair wind only.

```orders frigate
set the topsails
set the courses
set the fore topmast staysail
set the jib
set the spanker
set the topgallants
set the royals
set the flying jib
set the main topmast staysail
```

Taking in runs the other way: light sails first. *Take in* leaves a square sail *in the gear*, hauled up to its yard by clewlines and buntlines but not yet stowed (Falconer, *Buntlines*); *furl* sends the topmen out on the yard to pass the gaskets and make it fast (Falconer, *Furling*). A sail in the gear can be set again quickly; a furled sail must be loosed first.

```orders frigate all-sail
take in the studdingsails
take in the royals
take in the flying jib
take in the topgallants
furl the royals
furl the topgallants
haul down the main topmast staysail
# rejected: take in the royals
```

The last is refused with "Nothing done: the fore royal is already furled; the main royal is already furled; the mizzen royal is already furled."

The period words for taking in are particular to the sail, and the parser keeps them so (Luce 1866, ch. XXIII, 'To take in a Course', 'To take in a Topsail', 'The Spanker': "Up mainsail and spanker!"). A course is **hauled up** by its clew garnets and buntlines; a topsail or a light sail is **clewed up**; a spanker is **brailed up**; a jib is **hauled down**; a studding sail is taken in. `take in`, `douse` and `hand` suit any sail. Use the wrong word and the ship corrects you: "A gaff sail is brailed up, not clewed up; say 'brail up the mizzen spanker' or 'take in the mizzen spanker'."

```orders frigate plain-sail
haul up the mainsail
haul up the courses
brail up the spanker
clew up the topsails
haul down the jib
# rejected: clew up the spanker
# rejected: haul up the topsails
# rejected: lower the mainsail
```

What the log says:

```
  Morning watch (05:20)  Order: take in the fore topgallant.
  Morning watch (05:20)  Hands to the fore topgallant clewlines and buntlines.
  Morning watch (05:21)  Clewed up the fore topgallant.
* Morning watch (05:22)  Took in the fore topgallant; hanging in the gear.
  Morning watch (05:22)  Order: furl the fore topgallant.
  Morning watch (05:22)  Lay aloft and furl the fore topgallant.
* Morning watch (05:25)  Furled the fore topgallant.
```

## The words of command

Each evolution is a data file in `data/evolutions/` with the steps a working watch goes through, and the log prints the step names as Luce prints the orders. For a square sail (`set_square.yaml`; Luce 1866, ch. XXIII, 'To set a Topsail'; Lever, 'Setting the Topsails'):

| The log says | What is happening |
|---|---|
| *Hands aloft to loose the fore topsail.* | the topmen lay aloft and cast off the gaskets |
| *Laid aloft and loosed the fore topsail.* | the sail hangs loose from the yard |
| (sheet home) | the sheets haul the clews out to the yardarms below |
| *Set the fore topsail.* | the halyard hoists the yard; the sail is drawing |

A course's yard does not hoist: its tack is hauled aboard and its sheet aft instead. A gaff sail (`set_gaff.yaml`): "Hands to the spanker halyards and outhaul", "Cast off the gaskets and cleared away the brails", "Set the spanker". A jib (`set_jibheaded.yaml`): "Clear away the jib; man the halyards", "Set the jib". A studding sail (`set_studding.yaml`): "Stand by to set the...", "Got the ... out and bent on the halyards and tack", "Set the ...".

Every step has a fixed time in this milestone (about four and a half minutes for a topsail, three for a course or a spanker, under two for a jib, four for a studding sail, five for a reef), scaled up to double in a strong breeze and a heavy heel. **The crew's part in these timings is not yet modelled**: it makes no difference who is aboard or how many hands are on deck, and every sail of a group is worked at once, as if the ship had hands for all of them. Milestone 3 replaces the fixed times with crew-derived ones (`docs/TechnicalSpec-M0-M2.md` §8.4).

## Reefing

"The intention of the reef is to reduce the surface of the sail in proportion to the increase of the wind; for which reason there are several reefs parallel to each other in the superior sails" (Falconer, *Reef*). The topsails have three reef bands; the courses one; the spanker two; the schooner's mainsail three and her foresail and topsail two. Royals, topgallants and head sails have none and cannot be reefed.

To reef a topsail the halyards are settled and the yard clewed down, the reef tackles hauled out, the topmen lay out along the yard, pass the earings at the yardarms and tie the points along the band, and the yard is hoisted again (Luce 1866, ch. XXVII Reefing, 'Reefing and Hoisting'; Lever, 'Reefing Topsails'). The log:

```
  Morning watch (04:31)  Order: reef the topsails, one reef.
  Morning watch (04:31)  All hands reef the fore topsail.
  Morning watch (04:32)  Settled the fore topsail halyards and clewed down; hauled out the reef tackles.
  Morning watch (04:36)  Laid out and passed the earings of the fore topsail.
* Morning watch (04:38)  Reefed the fore topsail; now set, 1 reef.
```

You say how many reefs, or *close* for all of them (a *close-reefed* topsail has every reef in), after the sail or in the verb: `close reef`, `double reef`, `single reef`, `treble reef`, or Luce's `take in one reef in the topsails`. A reef comes out with `shake out`; `shake out the reefs` shakes out all of them:

```orders frigate plain-sail
reef the topsails, one reef
reef the fore topsail, two reefs
# rejected: reef the fore topsail
reef the main topsail, close
take a reef in the spanker
reef the courses
shake out a reef in the mizzen topsail
# rejected: shake out the reef in the mizzen topsail
shake out two reefs in the fore topsail
shake out all reefs in the main topsail
# rejected: reef the fore royal
close reef the topsails
# rejected: close reef the topsails
shake out the reefs in the topsails
double reef the fore topsail
take in one reef in the main topsail
single reef the mizzen topsail
```

The refusals: the fore topsail with three reefs in is "already close reefed (3 reefs in)"; the mizzen topsail with none in has "no reef in the mizzen topsail to shake out"; the royal "has no reef bands; it is set whole or not at all"; and the second `close reef` finds every topsail "already close reefed". A sail must be set to be reefed; reef a furled sail and the runner refuses it.

The schooner's boom mainsail reefs by settling the throat and peak halyards, hauling out the reef earing along the boom and tying the points (Luce 1866, ch. XXVII, 'Boom Mainsail'):

```orders schooner plain-sail
reef the mainsail, two reefs
reef the foresail
reef the topsail, close
shake out a reef in the mainsail
```

## Studding sails

Studding sails need the sail on their yard set (a fore topmast studding sail extends the fore topsail) and a steady breeze abaft the beam; they are the first thing to come in when it freshens (Luce 1866, ch. XXIII, 'The Topmast Studding-sail'; Lever, 'Studding Sails'). Set them on the weather side, the lee side, or both:

```orders frigate plain-sail
set the fore topmast studdingsails
set the studdingsails, lee
set the fore lower studdingsail, weather
# rejected: set the fore topmast studdingsail
take in the studdingsails
```

A studding sail comes in made up and stowed, so `take in` is enough; there is no `furl` for it.

Each studding sail has its boom, run out along the yard by an in-and-out jigger before the sail can go up: "Set taut! Rig out! Hoist away!" (Luce 1884, ch. XXIII At Sea, 'The Topmast Studding-sail'). `rig out` and `rig in` take the boom or the studding sail it carries; a boom cannot be rigged in with its sail set, and a sail cannot be set on a boom rigged in ("The starboard fore topmast studdingsail boom is rigged in; rig it out first"). Every boom starts rigged out, as the booms were before they had orders of their own.

```orders frigate plain-sail
rig in the starboard fore topmast studdingsail boom
rig out the starboard fore topmast studdingsail boom
rig in the fore topmast studdingsails, both sides
rig out the lee fore topmast studdingsail
# rejected: rig out the fore topsail
```

## Goose-winging

A course or a topsail with its lee clew hauled up to the yard and its weather clew still set is *goose-winged*: half the sail draws, and its centre lies out to windward, so it pays her head off. Luce uses it to help a ship off the wind in wearing in a gale: "haul aboard the weather clew of the foresail; which will increase her headway, and with her helm still a-weather, will serve to pay her off. A foresail in this state is 'goose-winged'" (Luce 1884, ch. XXIV, 'To Wear in a Gale'). From a set sail the lee clew is hauled up; from a sail hanging in its gear the weather clew is hauled aboard. `set` hauls the other clew aboard again and `take in` hauls both up. (Falconer's *goose-wings* are the other way about, both clews set and the bunt furled, "only used in a great storm to scud before the wind".)

```orders frigate plain-sail
goose-wing the foresail
goose wing the main topsail
# rejected: goose-wing the spanker
```

## Bending, unbending and shifting sails

A sail blown out of its bolt-ropes gives nothing and cannot be set again: it must be **shifted**, the rags unbent and sent down and a new sail sent up from the sail room and bent to the yard (Luce 1884, ch. XXXII Shifting Sails and Spars, 'To Shift a Topsail': "Lay out! Furl and unbend! ... Send up the new sail ... Bring to and bend the sail"). `unbend` and `bend` do the two halves alone (ch. XX Port Drills, 'To Unbend Sail', 'Bending Sail'). The new sail is left furled on its yard; setting it is your next order. A sail must be taken in before it is unbent or shifted, and only square sails are bent and unbent in this milestone.

The ship carries a few made-up sails in the sail room, three unless her ship file says otherwise, and bending one uses one; the log keeps the count. A sound sail unbent goes back to the sail room for the sailmaker, the rags of a blown-out one do not, and with none left the order is refused: "There is no spare sail left in the sail room to bend in place of the main royal; the sailmaker must make one first."

```orders frigate
unbend the fore royal
bend the fore royal
shift the main topsail
bend a new mizzen royal
# rejected: bend the jib
# rejected: unbend the spanker
```

```
  Morning watch, 8 bells (04:00)  Order: shift the fore royal.
  Morning watch (04:00)  Stand by to shift the fore royal! Aloft topmen; lay out, furl and unbend.
  Morning watch (04:03)  Unbent the fore royal and lowered it down on deck.
  Morning watch (04:06)  Swayed aloft the new fore royal.
* Morning watch (04:11)  Shifted the fore royal; the new sail bent and furled, 3 spare sails left in the sail room.
```

Eleven minutes in a 15-knot breeze. The old royal was sound, so it went down to the sail room and the count still stands at three; had it been blown out, it would stand at two.

## Light spars in a blow

"It is recommended to send down top-gallant masts in a heavy gale, when the vessel has much top-hamper, as it eases her considerably" (Luce 1884, ch. XXIX In a Gale). `send down the topgallant masts` clews up whatever is still drawing on them, sends the topgallant and royal yards down on deck with the sails furled on them, and unfids and lowers the masts; the spars sent down carry no strain and catch no wind, and nothing on them can be set until `sway up the topgallant masts` has them aloft and crossed again. In a 35-knot gale under all sail that is the difference between the royals carrying away and nothing going at all: ordered as the sails go up, it waits for the royals to be set and has them clewed up again before the second ten minutes. `send down the topgallant yards` sends down the light yards alone and `cross the topgallant yards` crosses them again. One level lower, `strike the topmasts` lowers each topmast with its topsail yard on the cap, and `fid the topmasts` sways them up; a topmast is struck only with its topgallant mast already down and no sail set on it.

```orders frigate plain-sail
send down the topgallant yards
cross the topgallant yards
send down the topgallant masts
sway up the topgallant masts
strike the topmasts
fid the topmasts
```

```
  Morning watch, 8 bells (04:00)  Order: send down the topgallant masts.
  Morning watch (04:07)  Clew up the fore topgallant, the fore royal, the flying jib, the main topgallant, the main royal, the mizzen topgallant and the mizzen royal; stand by to send down.
  Morning watch (04:07)  Down topgallant masts! Topgallant and royal yardmen in the tops.
  Morning watch (04:09)  Clewed up the fore topgallant, the fore royal, the flying jib, the main topgallant, the main royal, the mizzen topgallant and the mizzen royal; hands aloft to send down.
  Morning watch (04:18)  Sent down on deck the fore topgallant yard, the fore royal yard, the main topgallant yard, the main royal yard, the mizzen topgallant yard and the mizzen royal yard, with their studding sail booms.
  Morning watch (04:32)  Unfidded and lowered away the fore topgallant mast, the main topgallant mast and the mizzen topgallant mast.
* Morning watch (04:32)  Sent down the fore topgallant mast, the main topgallant mast and the mizzen topgallant mast; the upper spars on deck.
```

That is the frigate in 35 knots with all sail just made, the order given with the others: half an hour of work at the weather's pace. Order `strike the topmasts` with the topgallant masts aloft and it is refused ("Send down the topgallant masts first: the fore topgallant mast, the main topgallant mast and the mizzen topgallant mast are still aloft."); with sail set on the topmasts, it names every sail and asks for them to be taken in first.

## Loosing to dry and furling everything

After rain the furled sails are loosed to hang in their gear and dry: "Loose sail! ... Let fall!", the topsails and courses hanging by their buntlines, the topgallant sails and royals down, the head sails spread on the booms (Luce 1884, ch. XX Port Drills, 'To Loose Sail to the Buntlines'). Every furled sail but the studding sails is loosed; it is refused when it blows more than 20 knots across the deck. `furl all` (Luce's call is *Furl sail!*) clews up what is drawing and furls or stows everything in the ship.

```orders frigate
loose sails to dry
loose the sails to dry
```

With every sail already furled, as the ship starts, `furl all` is refused: "Every sail is furled already."

```orders frigate
# rejected: furl all
```

## The schooner

Her sails are named in chapter 1; the verbs are the same. Her gaff sails are not furled on a yard but brailed up or lowered onto the boom, so `furl` is refused for them ("A gaff sail is not furled on its spar; take it in instead") and `lower the mainsail` is taken in its place; her square topsail behaves exactly as the frigate's do (Luce 1884, ch. XXXIV Handling Fore-and-Afters). What she cannot do is **scandalise** a sail, dropping the peak of the mainsail to spill the wind, as Luce does before wearing her: the physics has no state for a gaff sail with its peak down, and the order says so. She has one topgallant mast, on the fore, and sends it down and sways it up with the frigate's words; she has no lower studding sails, so their booms are not hers to rig out.

```orders schooner
set the foresail
set the mainsail
set the jib
set the fore staysail
set the topsail
set the topgallant
set the gaff topsail
set the flying jib
take in the gaff topsail
take in the topgallant
furl the topgallant
send down the topgallant mast
sway up the topgallant mast
haul down the flying jib
lower the mainsail
brail up the foresail
# rejected: furl the mainsail
# rejected: scandalise the mainsail
```

The refusal: "The main sail cannot be scandalised: the physics has no state for a gaff sail with its peak dropped yet, only set, reefed or taken in. Ease the sheet, reef it or take it in instead."
