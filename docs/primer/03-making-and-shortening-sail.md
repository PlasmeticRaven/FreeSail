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

`make all sail` (*crowd sail*, *crack on*) sets plain sail and then the royals, flying jib, staysails, gaff topsail and studding sails both sides, passing over anything the ship has not got or cannot yet set: the studding sails go up only on booms already rigged out (below). `shorten sail` (*take in sail*, *snug her down*) takes in the studding sails, royals, flying jib, topgallants and gaff topsail and puts one reef in the topsails. These three are lists of ordinary orders in `data/vocabulary.yaml`; anything they cannot do is reported in the same log line after "Not done:".

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

Every step has its time (about four and a half minutes for a topsail, three for a course or a spanker, under two for a jib, four for a studding sail, five for a reef), scaled up to double in a strong breeze and a heavy heel, and taken with the hands the file asks for. Short-handed, the work goes slower and the log says so; with too few it waits for hands, and all hands called do it at the file's pace (chapter 6).

### Belaying work

Work in hand, or waiting for hands, is stopped with `belay`. "Avast" is the period's word, "the order to stop, or pause, in any exercise" (Falconer, *Avast*); "belay that" is the sea's later way of saying it, and both are taken. Name the work as the log names it (`belay setting the mainsail`) or as you ordered it, by its kind (`belay the reef`) or by its sail (`belay the mainsail`, every job on it); `belay that`, or a bare `belay`, stops the last order whose work is still in hand or waiting, and `belay all work` everything. Belayed work is gone, not paused as "Ready about!" pauses it (chapter 6): its hands are free, and the steps finished stay done, so a topsail belayed after the topmen loosed it hangs from the yard until you set or furl it. Said of a line, `belay` is the line order it always was. The schooner's watch, told to set three sails at once:

```
* Morning watch (04:10)  Not hands enough on deck to set the mainsail; the watch is setting the fore topsail and the foresail.
  Morning watch (04:10)  Order: belay setting the mainsail.
* Morning watch (04:10)  Belayed setting the mainsail; not begun, it was waiting for hands.
  Morning watch (04:11)  Laid aloft and loosed the fore topsail.
  Morning watch (04:11)  Order: belay all work.
* Morning watch (04:11)  Belayed all work, the ship left as she is: setting the fore topsail (the fore topsail left loosed and hanging from the yard) and setting the foresail (the foresail left furled).
```

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

Studding sails extend a sail beyond its yardarms (a fore topmast studding sail extends the fore topsail, so the topsail must be set), and they are for a steady, moderate breeze from abaft the beam; they are the first thing to come in when it freshens (Luce 1866, ch. XXIII, 'The Topmast Studding-sail'; Lever, 'Studding Sails'). Each has its boom, run out along the yard by an in-and-out jigger before the sail can go up: "Set taut! Rig out! Hoist away!" (Luce 1884, ch. XXIII At Sea, 'The Topmast Studding-sail'). Every boom starts rigged in, as at sea, so **rig out first, then set**: a `set` given to a studding sail whose boom is still in is refused with what must be done first ("The starboard fore topmast studdingsail boom is rigged in; rig it out first."). Set them on the weather side, the lee side, or both; before the wind, with the yards square, both:

```orders frigate plain-sail
brace the yards square
rig out the studdingsails, both sides
set the fore topmast studdingsails
set the studdingsails, lee
set the fore lower studdingsail, weather
# rejected: set the fore topmast studdingsail
take in the studdingsails
rig in the studdingsails, both sides
```

The refusal: a studding sail wants its side ("Which fore topmast studdingsail: the starboard, the larboard (the weather or the lee), or both sides?"). The test that runs this book finishes each order the moment it is given and does not look at the booms, so the refusal of a `set` before `rig out` is shown here in words rather than in the block; the console gives it.

A studding sail comes in made up and stowed, so `take in` is enough; there is no `furl` for it. `rig out` and `rig in` take the boom or the studding sail it carries; a boom cannot be rigged in with its sail set. With the yards braced up more than 45 degrees the lee boom will not go out past the lee rigging ("The fore topsail yard is braced too sharp for the boom to go out."), nor is a yard braced sharper with its lee boom out ("Rig in the studdingsail boom before bracing the fore topsail yard sharper."); the weather boom goes out, for the weather studding sails that Luce sets a point free. These two are the only rules: the rigging is a thing the physics cannot yet collide with.

```orders frigate plain-sail
rig out the starboard fore topmast studdingsail boom
rig in the starboard fore topmast studdingsail boom
rig in the fore topmast studdingsails, both sides
rig out the weather fore topmast studdingsail
# rejected: rig out the lee fore topmast studdingsail
# rejected: rig out the fore topsail
```

### How close they may be carried

Luce: the weather topmast and topgallant studding sails may be set "with the wind one point free, or forming an angle of seven points with the keel", the lower studding sail "only ... with the wind abaft the beam" (Luce 1866, ch. XXIII; Luce 1884, ch. XXIII). The game refuses none of it. The wind does: forward of its angle a studding sail's lift falls away over a point and it shakes in its gear, the snatching comes on its boom, and kept so the boom carries away. The frigate in 13 knots of wind with her five weather studding sails drawing at nine points, brought up to six:

```
  Morning watch (04:38)  Order: steer 292.
* Morning watch (04:38)  Starboard fore lower studdingsail shaking in its gear; she is too near the wind to carry it.
* Morning watch (04:38)  Starboard fore lower studdingsail boom whipping as the starboard fore lower studdingsail flogs; she is too near the wind for it.
* Morning watch (04:39)  Starboard fore topmast studdingsail shaking in its gear; she is too near the wind to carry it.
  ...
* Morning watch (04:39)  Starboard fore topmast studdingsail boom whipping as the starboard fore topmast studdingsail flogs; she is too near the wind for it.
! Morning watch (04:40)  Starboard main topmast studdingsail boom carried away; the starboard main topmast studdingsail hanging to leeward.
! Morning watch (04:41)  Starboard fore topmast studdingsail boom carried away; the starboard fore topmast studdingsail hanging to leeward.
  Morning watch (04:43)  Order: steer 259.
  Morning watch (04:44)  Starboard fore topgallant studdingsail drawing again.
  Morning watch (04:44)  Starboard main topgallant studdingsail drawing again.
  Morning watch (04:44)  Starboard fore lower studdingsail drawing again.
```

Two booms gone in three minutes; borne away to nine points again, the three still aloft draw. In 12 knots every boom whips and none goes in ten minutes; in 15 they go within minutes. A studding sail shaking in its gear also wears three times as fast as one drawing (below). Going about takes them in and the booms in before anything else (chapter 5).

## The ringtail, the save-alls and the water sail

Three more light sails for a fair wind and smooth water, each in the sail room until wanted and each a studding sail to the physics, with the same stall and the same boom (Luce 1884, ch. XXIII: "a ring-tail, which sets abaft the spanker; a save-all, under the lower studding-sail boom"; `docs/references/RigGeometryNotes.md` §8):

- the frigate's **ringtail**, a narrow sail bordering the spanker's after leech, its head on a short yard hoisted to the gaff end and its foot hauled out on a **ringtail boom** run out on the driver boom (Kipping: it "sets like a topmast studding sail, outside of the after-leech of the main-trysail"); No. 5 canvas;
- the frigate's two **save-alls**, one under each fore lower studding sail boom, No. 7;
- the schooner's **ringtail** on her main boom (Steel's "sloop's ringtail sail ... occasionally hoisted abaft the mainsail in calm weather") and her **water sail** under the main boom (Steel's "sloop's water-sail"), No. 5 and No. 7.

They start unbent, so the order is bend, rig out the boom, set:

```orders frigate
# rejected: set the ringtail
bend the ringtail
rig out the ringtail boom
bend the save-alls
```

```orders schooner
bend the ringtail
bend the water sail
rig out the ringtail boom
```

The refusal: "The ringtail is unbent; there is no sail on the yard. Bend one first." Once bent, `set the ringtail` (and `set the water sail`, `set the save-alls`) as for any studding sail. The schooner running before 15 knots under plain sail makes 5.5 knots; with the ringtail set, 5.7, and 6.1 against 5.9 with the wind on the quarter. The ringtail boom lies along the driver boom and never fouls a brace.

## Goose-winging

A course or a topsail with its lee clew hauled up to the yard and its weather clew still set is *goose-winged*: half the sail draws, and its centre lies out to windward, so it pays her head off. Luce uses it to help a ship off the wind in wearing in a gale: "haul aboard the weather clew of the foresail; which will increase her headway, and with her helm still a-weather, will serve to pay her off. A foresail in this state is 'goose-winged'" (Luce 1884, ch. XXIV, 'To Wear in a Gale'). From a set sail the lee clew is hauled up; from a sail hanging in its gear the weather clew is hauled aboard. `set` hauls the other clew aboard again and `take in` hauls both up. (Falconer's *goose-wings* are the other way about, both clews set and the bunt furled, "only used in a great storm to scud before the wind".)

```orders frigate plain-sail
goose-wing the foresail
goose wing the main topsail
# rejected: goose-wing the spanker
```

## Bending, unbending and shifting sails

A sail blown out of its bolt-ropes gives nothing and cannot be set again: it must be **shifted**, the rags unbent and sent down and a new sail sent up from the sail room and bent to the yard (Luce 1884, ch. XXXII Shifting Sails and Spars, 'To Shift a Topsail': "Lay out! Furl and unbend! ... Send up the new sail ... Bring to and bend the sail"). `unbend` and `bend` do the two halves alone (ch. XX Port Drills, 'To Unbend Sail', 'Bending Sail'). A sail must be taken in before it is unbent; a *shift* of a drawing sail takes it in itself and sets the new sail in its place when the work is done, as Luce's shift of a topsail by the wind opens "Clew up!" and ends "Let fall! Sheet home!"; a furled or hauled-up sail is shifted where it hangs and the new one left furled, setting it your next order. Any sail can be bent and unbent, square, gaff, jib-headed or studding.

```orders frigate
unbend the fore royal
bend the fore royal
shift the main topsail
bend a new mizzen royal
bend the jib
unbend the spanker
```

```
  Morning watch, 8 bells (04:00)  Order: shift the fore royal.
  Morning watch (04:00)  Stand by to shift the fore royal! Aloft topmen; lay out, furl and unbend.
  Morning watch (04:03)  Unbent the fore royal and lowered it down on deck.
  Morning watch (04:06)  Swayed aloft the fore royal (No. 8 canvas, new).
* Morning watch (04:11)  Shifted the fore royal; the fore royal bent (No. 8 canvas, new) and furled, 21 spare sails left in the sail room.
```

Eleven minutes in a 15-knot breeze. The old royal was sound, so it went down to the sail room and the count still stands at twenty-one; had it been blown out, its rags would have been condemned and the count would stand at twenty.

## Canvas and its condition

Sailcloth was woven in numbers, No. 1 the heaviest and strongest, No. 8 or 9 the lightest, and each sail was made of the number its work wanted. Luce's table of a frigate's suit (1884, ch. X, p. 171) makes the courses, topsails and spanker of No. 2 and every storm sail of No. 1; Steel (1794) and Kipping (1847) give the navy's older numbers for the lighter sails, which the frigate's file follows (`docs/references/RigGeometryNotes.md` §4). Every sail in the ship files has its number, and the strength of the cloth follows Luce's Appendix E, which tested an inch strip of each: No. 1 bore 470 lb, No. 2 420, a No. 8 royal little more than half of that (`docs/references/Tables.md`).

| The frigate's sails | Canvas |
|---|---|
| courses, fore and main topsails, spanker | No. 2 |
| mizzen topsail | No. 4 |
| topgallants (the mizzen's No. 7) | No. 6 |
| royals | No. 8 |
| jib, flying jib | No. 6, No. 7 |
| studding sails (topgallant No. 7) | No. 6 |
| storm canvas | No. 1 |

Canvas wears. A sail set and drawing wears slowly, three times as fast when it is aback or shaking, and not at all furled or in the sail room. Worn cloth bears less: a sail at half its condition bears seventy per cent of what it bore new, and it is baggier, so it lies less close to the wind. Nothing in the ship repairs canvas yet (the sailmaker's mending comes with milestone 8), so the only remedies are the old ones: shift a worn sail for a better one, and keep the best canvas for a blow. The words for a sail's condition are *new*, *sound*, *worn*, *much worn* and *worn out*.

What that means in a gale: in the 35-knot gale of gate M2, all sail made and braced up, a new royal holds until its yard and mast carry away; a royal of half its condition blows out of its bolt-ropes first, and the spar is saved for a new sail (`docs/dev/TuningNotes.md`, truth 27). The console cannot yet bend a worn sail by order: canvas wears by the hour, and a scenario is too short to wear it.

## The sail room

The sail room holds the spare canvas: on the frigate, Luce's allowance for a ship of her class, a second of each working sail in its working number, a heavy-weather foresail and fore and main topsails of No. 1 canvas, the storm canvas and the occasional sails; on the schooner a second foresail, fore topsail and jib, a storm trysail and storm jib, a ringtail and a water sail. `the sail room` at the prompt lists them, and `muster` ends with a line for them:

```
The sail room holds 21 sails.
Spares of the working canvas: mainsail, No. 2 canvas, new; mizzen topsail, No. 4 canvas, new; fore topgallant, No. 6 canvas, new; ...
For heavy weather: foresail, No. 1 canvas, new; fore topsail, No. 1 canvas, new; main topsail, No. 1 canvas, new.
Storm canvas: fore storm staysail, No. 1 canvas, new; mizzen storm staysail, No. 1 canvas, new; storm mizzen, No. 1 canvas, new.
For light fair winds: ringtail, No. 5 canvas, new; starboard fore save all, No. 7 canvas, new; larboard fore save all, No. 7 canvas, new.
```

`shift` and `bend` take the best spare of the sail's working number, or the one you name: **for the heavy one** takes the No. 1, and a number takes that number. The sail unbent goes back to the room with its condition. Bending more than the room holds is refused ("There is no spare sail left in the sail room to bend in place of the main royal; the sailmaker must make one first."), and so is a number the room has not got ("There is no main topsail of No. 3 canvas in the sail room; it holds ...").

```orders frigate
shift the fore topsail for the heavy one
unbend the main topsail
bend the No. 1 main topsail
shift the fore royal
```

```
  Morning watch (04:15)  Order: shift the fore topsail for the heavy one.
  Morning watch (04:15)  Stand by to shift the fore topsail! Aloft topmen; lay out, furl and unbend.
  Morning watch (04:18)  Unbent the fore topsail and lowered it down on deck.
  Morning watch (04:21)  Swayed aloft the fore topsail (No. 1 canvas, new).
* Morning watch (04:26)  Shifted the fore topsail; the fore topsail bent (No. 1 canvas, new) and furled, 21 spare sails left in the sail room.
```

## Storm canvas

For a storm the ship bends sails that are hers for nothing else: on the frigate a **fore storm staysail** on the fore stay, a **mizzen storm staysail** on the mizzen stay, and a **storm mizzen**, a small sail bent in the spanker's place; on the schooner a **storm trysail** on the main and a **storm jib**. All are No. 1 canvas and live in the sail room until bent (Luce 1884, ch. X, "Storm-Sails are made of the strongest canvas"). The storm staysails are bent where they stand; the storm mizzen needs the spanker unbent first, which `shift the spanker for the storm mizzen` does in one order, and `shift the storm mizzen for the spanker` undoes it.

```orders frigate
# rejected: set the fore storm staysail
bend the fore storm staysail
bend the mizzen storm staysail
shift the spanker for the storm mizzen
```

```orders schooner
bend the storm trysail
bend the storm jib
```

The refusal: "The fore storm staysail is unbent; there is no sail on the yard. Bend one first." Once bent, each is set and taken in like any staysail: `set the fore storm staysail`, `set the storm mizzen`, `haul down the mizzen storm staysail`.

```
  Morning watch (04:35)  Order: bend the fore storm staysail.
  Morning watch (04:35)  Bend sail! Rouse up the fore storm staysail from the sail room.
  Morning watch (04:37)  Roused up the fore storm staysail from the sail room (No. 1 canvas, new) and swayed it aloft.
* Morning watch (04:42)  Bent the fore storm staysail (No. 1 canvas, new) and furled it; 20 spare sails left in the sail room.
```

Luce's ship lies to in a gale "under close-reefed main topsail, fore storm staysail, and probably single reefed trysail" (Luce 1884, ch. XXIX In a Gale), and that is what `lie a-try` does once the main topsail is set, close-reefed as the weather wants (chapter 5): the other square sails and the jibs are taken in, the staysails stand, and she comes up to about four points with the helm a little a-lee. In a steady 45-knot storm with the topgallant masts sent down and the storm staysails set, nothing carries away in an hour, though the storm staysails stand at nine tenths of what their cloth will bear and the console's gusts blow them out of their bolt-ropes (the owner is judging that too). **What the game does not yet do** is let her lie quietly: she goes astern at four knots and more where a ship of the period drifted bodily to leeward at a knot or two, a question for the physics that the owner is judging (`docs/dev/TuningNotes.md`, truth 28).

## Light spars in a blow

"It is recommended to send down top-gallant masts in a heavy gale, when the vessel has much top-hamper, as it eases her considerably" (Luce 1884, ch. XXIX In a Gale). `send down the topgallant masts` clews up whatever is still drawing on them, sends the topgallant and royal yards down on deck with the sails furled on them, and unfids and lowers the masts; the spars sent down carry no strain and catch no wind, and nothing on them can be set until `sway up the topgallant masts` has them aloft and crossed again. It is work for all hands: the watch below is turned up, and the sail work the watch had in hand on the topgallant and royal masts is belayed until it is done (a royal is not set on a mast being struck); the rest of the work in hand goes on, and its hands join the send-down when they are free. In a 35-knot gale that is the difference between the royals carrying away and nothing going at all: ordered with `make all sail`, it takes the hands off the light sails before the royals are set, and when the work in hand is taken up again the royals are refused, their yards being on deck. `send down the topgallant yards` sends down the light yards alone and `cross the topgallant yards` crosses them again. One level lower, `strike the topmasts` lowers each topmast with its topsail yard on the cap, and `fid the topmasts` sways them up; a topmast is struck only with its topgallant mast already down and no sail set on it.

```orders frigate plain-sail
send down the topgallant yards
cross the topgallant yards
send down the topgallant masts
sway up the topgallant masts
strike the topmasts
fid the topmasts
```

```
  Morning watch, 8 bells (04:00)  Order: make all sail.
  Morning watch, 8 bells (04:00)  Order: brace up on the starboard tack.
  Morning watch, 8 bells (04:00)  Order: send down the topgallant masts.
  ...
* Morning watch (04:00)  Belayed setting the fore topgallant: down topgallant masts! Topgallant and royal yardmen in the tops.
  ...
  Morning watch (04:00)  Down topgallant masts! Topgallant and royal yardmen in the tops.
  Morning watch (04:01)  All hands on deck.
  Morning watch (04:07)  Sent down on deck the fore topgallant yard, the fore royal yard, the main topgallant yard, the main royal yard, the mizzen topgallant yard and the mizzen royal yard, with their studding sail booms.
* Morning watch (04:07)  Could not set the fore royal: the fore royal's yard or mast is wrecked or sent down.
  ...
  Morning watch (04:18)  Unfidded and lowered away the fore topgallant mast, the main topgallant mast and the mizzen topgallant mast.
* Morning watch (04:18)  Sent down the fore topgallant mast, the main topgallant mast and the mizzen topgallant mast; the upper spars on deck.
```

That is the frigate in 35 knots, the order given with `make all sail`: eighteen minutes of all hands' work at the weather's pace, and she lies with no canvas set while it is done, until the sail work belayed is taken up again. Given once the light sails are drawing, it clews them up first. Order `strike the topmasts` with the topgallant masts aloft and it is refused ("Send down the topgallant masts first: the fore topgallant mast, the main topgallant mast and the mizzen topgallant mast are still aloft."); with sail set on the topmasts, it names every sail and asks for them to be taken in first.

## Clearing a wreck and shifting a spar

A spar that carries away takes with it everything that stands on it or hangs from it: a studding-sail boom its studding sail, a topmast the topgallant mast and the yards above it and every sail on them. The wreck hangs to leeward and drags, and nothing in it can be set, taken in or braced; the log says what went ("Larboard fore topmast studdingsail boom carried away; the larboard fore topmast studdingsail hanging to leeward."). "No explicit rule can be given for sending down broken spars. The first thing to be attended to is their being steadied and prevented from falling on deck or tearing the sails" (Luce 1884, ch. XXXI Carrying Away Masts and Spars).

**`cut away`** the wreck, naming any part of it: `cut away the larboard fore topmast stuns'l`, `clear away the wreck of the fore topmast`, `clear away the larboard fore topmast studdingsail boom`, or `clear the wreck` for every wreck aboard. Cutting away is the old word for clearing a ship of what is gone ("the mizen-mast must instantly be cut away", Falconer 1780, *Veering*). The hands steady the wreck with burtons and tripping-lines, cut the robands and earings of each sail in it and lower it on deck ("Cut adrift the clewlines from the clews, cut robands and head earings, and lower", Luce, 'Topgallant Yard Carried Away'), and send the remains of the spars down after it ("Send the wreck down ... Send the stump down next", 'Main Topmast Carried Away'). What can be saved is saved: a sail that is whole goes to the sail room, the rags of one blown out go over the side. A lower mast or the bowsprit carries away at the deck and its wreck lies in the water, so it is cut adrift with everything on it, as Luce's ship does when "a mast goes over the side, first, get clear of the wreck". The log names what was saved and what went over the side. A sail blown out of its bolt-ropes on spars that stand is cut away the same way, its rags over the side.

`unbend` takes a sail out of a wreck where it hangs, to the sail room if it is whole, and `send down the <spar>` sends a spar's wreck down on deck: the same work as cutting it away, refused for a wreck that is over the side. A sound spar is not sent down by itself; the refusal names the order that sends it down with its fellows ("The fore topgallant mast stands sound; the topgallant masts go down together: 'send down the topgallant masts'.").

Cleared, the spar is still gone. The ship remembers it until a spare is put in its place: a studding sail is not bent to a boom that carried away, nor its boom rigged out, and the refusal says why ("The larboard fore topmast studdingsail boom is carried away; shift it for a spare first."). **`shift the <spar>`** (or `... for a spare`) sends a spare of its class up from the booms, the spare spars stowed amidships ("the spare topmasts, yards, &c. stowed on the boat skids", Steel 1794), and rigs it as the old one was (Luce 1884, ch. XXXII Shifting Sails and Spars, 'To Shift a Topmast Studding-sail Boom', 'To Shift a Topsail Yard', 'To Shift a Topmast'); then the sail that belongs on it can be bent again. A spar that went with another waits for that one ("The fore topsail yard went with the fore topmast; shift the fore topmast first."). The frigate carries Luce's spares (1866, ch. XVII, 'Stowing Booms'): two topmasts, two stump topgallant masts, the fore and main topsail yards, four topmast studding-sail booms, a jib-boom and a flying jib-boom; the schooner a topmast, a topsail yard and two studding-sail booms. With none of the class aboard the shift is refused: "No spare studding-sail boom aboard; the dockyard must supply one." `the booms` (or `the spare spars`) at the prompt says what is left, as `the sail room` does for canvas.

```orders frigate
the booms
the spare spars
# rejected: cut away the fore topsail yard
# rejected: clear the wreck
# rejected: shift the fore topmast
# rejected: send down the fore topgallant mast
```

With nothing carried away every one of these is refused in words: "The fore topsail yard stands sound; there is no wreck to cut away.", "There is no wreck aboard to clear: every spar stands and no sail hangs in rags.", "The fore topmast is sound; only a spar carried away is shifted for a spare." The schooner of the tenth playtest, in 19 knots with a boom gone:

```
! Morning watch (04:00)  Larboard fore topmast studdingsail boom carried away; the larboard fore topmast studdingsail hanging to leeward.
  Morning watch (04:00)  Order: cut away the larboard fore topmast stuns'l.
  Morning watch (04:00)  Clear away the wreck of the larboard fore topmast studdingsail boom! Hands aloft with burtons and tripping-lines.
  Morning watch (04:01)  Steadied the wreck of the larboard fore topmast studdingsail boom with burtons and tripping-lines.
  Morning watch (04:04)  Cut the robands and earings; lowered the larboard fore topmast studdingsail on deck for the sail room.
  Morning watch (04:06)  Sent down on deck the remains of the larboard fore topmast studdingsail boom; the gear that went with it unrove and cleared.
* Morning watch (04:06)  Cleared the wreck of the larboard fore topmast studdingsail boom: its remains sent down on deck; the larboard fore topmast studdingsail saved to the sail room; nothing went over the side. The booms hold 2 spare studding-sail booms.
  Morning watch (04:06)  Order: shift the larboard fore topmast studdingsail boom for a spare.
  Morning watch (04:07)  Got the spare studding-sail boom out of the booms and put its gear on it.
  Morning watch (04:10)  Landed the new larboard fore topmast studdingsail boom in its irons and clamped it.
  Morning watch (04:12)  Rove the larboard fore topmast studdingsail boom's gear and set up the rigging.
* Morning watch (04:12)  Shifted the larboard fore topmast studdingsail boom for a spare, 1 spare studding-sail boom left on the booms; the larboard fore topmast studdingsail may be bent to it again.
  Morning watch (04:12)  Order: bend the larboard fore topmast studdingsail.
* Morning watch (04:19)  Bent the larboard fore topmast studdingsail (No. 6 canvas, new) and furled it; 7 spare sails left in the sail room.
```

Twenty minutes from the carry-away to a studding sail ready to set again. A boom is the lightest of it: the wreck of a topmast, with the yards and the sails above it, takes the better part of an hour to clear in a fresh breeze, and a new topmast six times a boom's work to send up, each at the pace the weather and the hands allow. The spars that went with it are shifted one by one, the topmast first.

## Loosing to dry and furling everything

After rain the furled sails are loosed to hang in their gear and dry: "Loose sail! ... Let fall!", the topsails and courses hanging by their buntlines, the topgallant sails and royals down, the head sails spread on the booms (Luce 1884, ch. XX Port Drills, 'To Loose Sail to the Buntlines'). Every furled sail but the studding sails is loosed; it is refused when it blows more than 20 knots across the deck. `furl all` (Luce's call is *Furl sail!*) clews up what is drawing and furls or stows everything in the ship. Both are all hands' work, for every man has a station for loosing and for furling sail in his billet (Luce 1884, ch. XVIII, 'Station Billet'): order them by day, or the watch below loses its sleep.

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
