# 4. Trimming

"Trim, when applied to the sails, denotes the general arrangement which is best calculated to accelerate the ship's course, according to the direction of the wind" (Falconer, *Trim*). On a square-rigger it is two jobs: the yards are *braced* to the wind, and the fore-and-aft sails are *sheeted* to it. A third, keeping the ship herself balanced so that she needs little helm, is what the other two are for.

## Bracing the yards

The braces swing a yard round in the horizontal (Falconer, *Brace*). The order names how far and, when it matters, for which tack:

| Word | The yard goes to | When |
|---|---|---|
| **sharp up** | its brace limit: on the frigate 60° to 64° from square for the lower yards and two degrees more for each yard above (below, *Pointing*) | close-hauled |
| **up** | 30° from square | the wind abeam |
| **in** | 15° from square | the wind on the quarter |
| **square**, *by the lifts* | across the ship | before the wind |

"On the starboard tack" or "on the larboard tack" says which yardarm goes forward: braced up for the starboard tack the starboard yardarm points forward and the larboard aft, so that the sail faces a wind from starboard. Leave it out and the yards are braced for the tack she is on. Without an object every yard is braced; name a yard, a mast's yards, the *head yards* or the *after yards* to brace some.

Three more forms are Luce's. **Square the yards** (or *lay the head yards square*) is `brace square`. **Brace round** with nothing else said swings the yards sharp up for the tack the wind is now on, which is what it means after a tack or a wear. **Brace the yards to the wind** braces each yard named to the best angle for the present apparent wind, as `trim the yards` (below) does for all of them.

```orders frigate
brace sharp up on the starboard tack
brace the yards square
brace the after yards in
brace up the head yards
brace the main yard in on the larboard tack
brace the fore topsail sharp up
brace round the cro'jack yard square
brace by the lifts
square the yards
square the after yards
lay the head yards square
brace round the yards
brace round the head yards on the larboard tack
brace the yards to the wind
brace the fore and main yards to the wind
# rejected: brace the fore yards
# rejected: brace the mizzen gaff sharp up
# rejected: brace the spanker square
```

Bracing takes the braces' hands three quarters of a minute per yard, and every yard named swings at once; the log reports each yard's angle when it is there:

```
  Morning watch, 8 bells (04:00)  Order: brace sharp up on the starboard tack.
  Morning watch (04:00)  Braced up for the starboard tack, the after yards two degrees sharper.
* Morning watch (04:03)  Braced the fore yard; 62° from square.
* Morning watch (04:04)  Braced the main yard; 64° from square.
* Morning watch (04:04)  Braced the fore topsail yard; 64° from square.
* Morning watch (04:04)  Braced the main topsail yard; 66° from square.
  ...
* Morning watch (04:04)  Braced the crossjack yard; 60° from square.
```

The refusals: "Brace them how? Say 'sharp up', 'up', 'in', 'square', 'aback' or 'to the wind'"; "The mizzen gaff is a gaff, not a yard; the gaff sail on it is not braced; it is trimmed with its sheet and vangs"; "The spanker is a gaff sail; it has no yard to brace. Trim it with its sheet."

### Laying a yard aback

A yard braced for the *other* tack has its sail pressed back against the mast, *aback*: no drive, and the ship checked or pushed astern. That is how she is hove to (chapter 5), and it is a thing you may order for one yard at a time: **back the main topsail**, *lay the main topsail aback*, *brace the main topsail yard aback*, *brace the head yards sharp aback* (Luce 1866, ch. XXIV, 'Box Hauling'; ch. XXVI, 'To heave to'). Name the yard or the square sail on it; a tack said is the tack she is taken aback *from*.

```orders frigate plain-sail
back the main topsail
lay the main topsail aback
brace the main topsail yard aback
brace the head yards sharp aback
# rejected: back
# rejected: back the spanker
```

```
  Morning watch (04:10)  Order: back the main topsail.
  Morning watch (04:10)  Man the main yard braces.
  Morning watch (04:10)  Man the main topsail yard braces.
  Morning watch (04:10)  Laid the main yard, main topsail yard, main topgallant yard and main royal yard aback, braced up for the larboard tack; the main course, main topsail and main topgallant to the mast.
* Morning watch (04:10)  Main course taken aback.
* Morning watch (04:10)  Main topsail taken aback.
* Morning watch (04:10)  Main topgallant taken aback.
! Morning watch (04:10)  Taken aback: the sails pressed against the masts and she lost her way.
```

Note that the order names one sail but the whole mast's yards come round together. That is the period sense of "back the main topsail": a single yard braced against the yards above and below it would foul their sails, so the main yards are laid aback as a set and the sails on them go to the mast. With the main aback and nothing else done she loses her way and rounds up with the helm hard over; to stop her properly, `heave to` (chapter 5) also hauls up the course and puts the helm a-lee. To fill again, `brace the main yards full` for the tack she is on. The refusals: "Back what? Name a yard or a square sail, such as the main topsail"; the spanker "is a gaff sail; it has no yard to brace."

### How sharp, and which yards sharper

Luce's rule for a stiff breeze is to brace the lower yards up sharp and trim each yard above by the one below, "with the weather yard arm about a half point abaft the lower yard", because the upper sails are flatter and the lighter yards need the support; in light airs with smooth water "the yards of no ship can lie braced up too sharp"; with the wind abaft the beam the after yards should be braced sharper than the head yards so that the wind fills the forward sails (Luce 1866, ch. XXIV Working to Windward, 'To Trim Yards', and the 'Table of best angles of yard with keel'). Lever adds that in practice the yard is braced up sharper than the six-point geometry needs, "to make the Sail stand to the most advantage" (Lever, figure 397).

What the game does: each yard has its own limit in the ship file, from Fincham's measured angles, the upper yards a few degrees *sharper* than the lower, not less; `brace sharp up` takes every yard to its own limit, and on a wind the after yards stand sharper than the head yards (*Pointing*, below). The steering advantage Luce describes, upper yards a little in so that the royal lifts first and "all the other sails are a clean full and by", is not modelled. A player who wants Luce's trim can brace mast by mast (`brace the fore yards sharp up`, then haul a weather topgallant brace a little), but nothing in the physics yet rewards it.

### Hauling on a single brace

Below the evolutions is level 0: one rope, hauled or eased, and the yard moves five degrees. On the starboard tack the larboard brace is the lee brace, and hauling it brings the yard sharper; hauling the weather brace brings it back toward square. *A fathom* is one such haul, *two fathoms* two; *handsomely* is slowly and carefully, *roundly* smartly, and the log repeats the word. `check` eases a little; `belay` makes fast; `let go` lets the rope run.

```orders frigate plain-sail
haul the weather main brace
haul the weather main brace, handsomely
ease the weather main brace two fathoms
# rejected: haul the lee main brace
haul the weather fore topsail brace a fathom
haul the lee fore topsail brace
check the lee fore brace
belay the lee fore brace
let go the lee main topgallant brace
```

The refusal: braced sharp up on the starboard tack, the main yard "is already braced sharp up that way; it will come no further" when you haul its lee brace; bring it in by the weather brace first, as the next two lines do for the fore topsail yard, and the lee brace then takes it back to sharp up.

## Tending the sheets

A fore-and-aft sail is trimmed by its sheet: hauled in for the wind ahead, eased off as it draws aft (Falconer, *Sheet*). The game measures a gaff sail's or jib's trim as the angle of its foot from the centreline, and each haul or ease moves it five degrees. When a sail is set its sheet is trimmed to the apparent wind at once, and there is a floor a boom on its horse cannot come inside: 18° for a gaff sail, 15° for a jib or staysail. Close-hauled at 49° apparent the spanker is sheeted to 24°, and `haul the spanker sheet` brings it to 19°:

```
  Morning watch (04:15)  Order: haul the spanker sheet.
  Morning watch (04:15)  Hauled the mizzen spanker sheet; the mizzen spanker now 19° off the centreline.
```

```orders frigate plain-sail
haul the spanker sheet
ease the spanker sheet a fathom
ease the spanker sheet two fathoms
haul in the spanker sheet handsomely
haul aft the spanker sheet
# rejected: haul the spanker sheet
# rejected: haul the spanker sheet aft
ease the jib sheet, lee
haul the jib sheet aft, lee
ease the fore topmast staysail sheet, lee
```

Each `ease` lets the boom off five degrees and each `haul` brings it in five; the block starts with the spanker sheeted at its 18° floor for a wind at 40° apparent, so the first haul takes it to 13°, the two eases to 28°, and the next haul to 23°. **Haul aft** (or *aft* after the sheet's name) hauls it all the way: "Hauled the mizzen spanker sheet flat aft; the mizzen spanker now amidships". Then come the two refusals: "The mizzen spanker sheet is already hard in", and a sheet already flat aft is refused a second time.

A square sail's sheets and tacks are hauled home when it is set and stay there (its bowlines are not: they start running free and are hauled on a wind; *Pointing*, below); ease a sheet and the log counts it off in tenths ("Eased the larboard (lee) main course sheet; now nine-tenths hauled"). **Sheet home** the sail, or **haul home** its sheets, and they are hauled home again and belayed; the plural names both sheets at once. Their trim is the yard's business.

```orders frigate plain-sail
ease the fore topsail sheets
ease the lee main sheet two fathoms
sheet home the fore topsail
haul the main sheet home, lee
ease the topsail sheets
haul home the topsail sheets
# rejected: sheet home the fore topsail
```

The last refusal: "The fore topsail is sheeted home already."

Between your orders **the watch on deck tends the fore-and-aft sheets for you**: each set jib, staysail and gaff sail is sheeted to the apparent wind as she comes up or falls off, at about a degree a second (`freesail/evolutions/trim.py`), and never inside the floors above. Square sails are never touched without an order. So after a tack the spanker and jib will find their trim by themselves, but the yards will sit where the tack left them until you brace or `trim`. It also means a sheet you haul by hand is eased again within the minute: hauled to 19° at 04:15, the spanker was back at 24° when `ease the spanker sheet a fathom` a minute later put it at 29°. Sheet orders by hand are for the moment, and for the crew work of milestone 3, which will make the watch do only what it is told.

## The `trim` order

Package 13 adds the order the owner reached for at the gate. It braces every yard that has sail set to the best angle for the present apparent wind, each as its own `brace` evolution, the after yards a little sharper than the head yards on a wind (*Pointing*, below), and sheets the fore-and-aft sails at once:

```orders frigate plain-sail
trim the yards
trim the sheets
trim sails
```

`trim the yards` is what Luce means by "trim the yards, haul taut the lifts and braces" after a tack or a wear; `trim the sheets` is "trim aft the head sheets"; `trim sails` is both. `brace the yards to the wind` is `trim the yards` by another name, and takes the yards you name.

## Pointing: how close she lies, and what it costs

How near the wind a ship will lie is not a number in her file. It comes out of how sharp her yards can be braced, how flat her sails stand, how her masts are trimmed against each other and how she is steered, and each of those is a thing the period did and the game does. What she makes of it: under plain sail in a 15-knot breeze the frigate's best course to windward is about 64° off the wind (5.7 points), and she holds two thirds of her beam-reach speed to 68°, six points, which is Fincham's "seldom within six points" for a long frigate; the schooner holds the same to 56°, five points (`docs/dev/TuningNotes.md`, truths 1, 2 and 32).

### The brace limits

"The shrouds, stays, and other causes connected with the rigging, will seldom allow the yards of square-rigged vessels to be braced sufficiently sharp" (Fincham 1843, art. 100). Each yard's limit in the ship file is Fincham's measured angle for a ship of her class (art. 102, Captain Hardy's squadron of 1827), turned from the keel to square: the frigate's fore yard 62°, main yard 64°, crossjack 60°, and each yard above its lower yard two degrees more, the shrouds converging aloft. `brace sharp up` takes each yard to its limit; so the main yards stand two degrees sharper than the fore without being told.

### The after yards sharper

"It will be found commonly the case, that the after-yards are braced sharper up than the fore-yards; which, by the stream of the wind being brought more a-head before it strikes the after-sails, produces an effect nearly the same as if the sails were in planes parallel to each other" (Fincham 1843, art. 94). On a wind, `trim sails` and `brace sharp up` brace each after yard up to three degrees sharper than the head yard at its level, as far as its own limit allows, and the log names the difference. With much way, little sea and a ship griping, Fincham has the reverse, "brace the head-yards sharper than the after-yards" (art. 96): say **with the head yards sharper**.

```orders frigate plain-sail
trim sails
trim sails with the head yards sharper
brace sharp up with the head yards sharper
trim the yards
```

```
  Morning watch (04:20)  Order: trim sails.
  Morning watch (04:20)  Braced 12 yards to the wind, 48° on the starboard bow, the after yards two degrees sharper; trimmed the sheets of the mizzen spanker; the fore topmast staysail; the jib.
  Morning watch (05:05)  Order: trim sails with the head yards sharper.
  Morning watch (05:05)  Braced 12 yards to the wind, 45° on the starboard bow, the head yards three degrees sharper; trimmed the sheets of the mizzen spanker; the fore topmast staysail; the jib.
```

What it is worth in the game is small: at 66° off the wind the frigate makes 5.2 knots with the after yards two degrees sharper and 5.0 with all alike, and 4.8 with the head yards sharper. Fincham's reason is the head sails bending the wind aft of them, and the game's sails all feel one wind, so the after sails gain only the little they gain by standing nearer their luff. The owner is judging it (truth 24).

### Bowlines

A bowline hauls the weather leech of a course or topsail forward, so that the sail stands flat and does not lift when she is close to the wind: "the flatter the sails the sharper they may be braced" (Fincham 1843, art. 98); "haul taut the weather brace and haul the bowline" (Luce 1884, ch. XXIII). The courses and topsails of the frigate and the schooner's fore topsail have a bowline each side. They start running free, and on a wind the weather ones are hauled: **haul the weather bowlines**, or Luce's **steady out the bowlines**, a minute's work for four hands at each. A bowline is only hauled on the weather side of a yard braced up: off the wind it will not stand, and it slacks by itself when its yard is braced in beyond 40° from square. **Let go the bowlines** (*clear away the bowlines*) lets them run; **ease** eases one a little.

```orders frigate plain-sail
# rejected: clear away the bowlines
haul the weather bowlines
# rejected: haul the lee fore bowline
```

```orders frigate plain-sail
steady out the bowlines
```

```orders frigate plain-sail
haul the weather fore topsail bowline
haul the fore bowline
```

```
  Morning watch (04:35)  Order: haul the weather bowlines.
  Morning watch (04:36)  Steadied out the starboard fore course bowline.
  Morning watch (04:36)  Steadied out the starboard fore topsail bowline.
  Morning watch (04:36)  Steadied out the starboard main course bowline.
  Morning watch (04:36)  Steadied out the starboard main topsail bowline.
  Morning watch (04:36)  Steadied out the starboard mizzen topsail bowline.
```

The refusals: bowlines not yet hauled cannot be let go ("Nothing done: the starboard fore course bowline is already running free; ..."), and "The larboard fore course bowline is on the lee side of the fore yard, which is braced up for the starboard tack; it is the weather leech that is hauled out." One bowline is hauled by naming it; "the fore bowline" is the foresail's weather one. This is the largest gain the frigate has: in 15 knots, 5.8 knots at 66° off against 5.2, and the same 5.2 about three degrees closer; the closest she holds three knots goes from 56° to 52°. The schooner gains next to nothing by hers, for she points with her fore-and-aft sails. The price is hands at every brace: going about lets the bowlines go and steadies them out again on the new tack (chapter 5), and bracing in slacks them.

### The catharpins

The lower shrouds, spreading from the mast to the channels, are what the lee yardarm fetches up against. Swiftering in the catharpins draws them in below the top so that the lower yard can come round further: a swifter rove through tail-blocks on each shroud "that is to be catharpined in", its fall led across the deck, "the shrouds are then bowsed in", and the catharpin legs seized to hold them (Lever 1808, fig. 182; Steel 1794, *Catharpins*); the measures Captain Hardy took in his short ship to brace her main yard to 17° from the keel, where she "could sometimes lie within 5 points" (Fincham, art. 102). The price is that the shrouds drawn in hold the mast less well athwartships.

**Swifter in the catharpins** (on one mast, or on all the lower masts) is twenty minutes' work a mast for the boatswain's party, eight hands from the forecastlemen and the carpenter's crew, some of them in the rigging; the lower yard on that mast then braces four degrees sharper. **Ease the catharpins** casts the legs off, and a yard braced sharper than its rigging now allows comes in with them.

```orders frigate plain-sail
swifter in the catharpins on the main
swifter in the catharpins
# rejected: ease the catharpins on the fore
```

```
  Morning watch (05:20)  Order: swifter in the catharpins on the main.
  Morning watch (05:20)  Boatswain's party to the main mast shrouds; reeve the swifter.
* Morning watch (05:45)  Swiftered in the catharpins on the main mast; the main yard will brace four degrees sharper.
  Morning watch (05:50)  Order: trim sails.
  Morning watch (05:50)  Braced 12 yards to the wind, 45° on the starboard bow, the after yards six degrees sharper; ...
```

and, eased again:

```
  Morning watch (05:11)  Order: ease the catharpins.
  Morning watch (05:11)  Boatswain's party to the main mast shrouds; cast off the catharpin legs.
  Morning watch (05:30)  Main yard came in to 64° from 68° as the lower shrouds went out.
* Morning watch (05:43)  Eased the catharpins on the main mast; the main yard braces as rigged again, four degrees less sharp.
```

The refusal: "The catharpins on the fore mast are not swiftered in." The gain is one yard in twelve four degrees sharper: a tenth of a knot at 66° off, less than a degree of pointing. The cost is in the mast: on a wind in 30 knots the main mast bears about thirty per cent more of its rating with the catharpins in, a sixth for the shrouds drawn in and the rest for the sharper yard's harder pull. A lower mast is rated for a whole gale, so in 30 knots the log says nothing of it; it is a price paid in a squall, when a mast strained with its catharpins in says so ("working under the press of sail, the catharpins swiftered in").

### Full and by, and not pinched

"Full and by" is sailing as close as the sails will stand full, and no closer. Seamen braced as sharp as they could and kept one point of the sail lifting, which Fincham allows only with five or six knots of way; with less, keep them full (Fincham 1843, art. 99). The game has the reason in it: in a light breeze of 8 knots the frigate at six points makes three knots and 0.9 of a knot good to windward over the ground; pinched to five points she makes a knot and three quarters, her leeway doubles, and she makes 0.75 good. **Keep her full** (*full and by*, *nothing off*) puts the helmsman to steering by the sails instead of the compass, as full as they stand plus a little; in a light wind that is fuller than six points, so a sailing master steering for windward in light airs gives a course.

```orders frigate plain-sail
keep her full
full and by
steer 294
```

So, to work to windward in the frigate: brace sharp up and `trim sails`, haul the weather bowlines, steer six points off, and keep her full rather than high; swifter in the main catharpins if she must claw off a lee shore and the masts will bear it.

## Weather helm and lee helm

A ship whose after sails press harder than her head sails wants to come up into the wind; the helmsman must hold the helm to leeward to keep her off, and she is said to *carry a weather helm* or to *gripe*. One whose head sails overpower her after sails falls off and needs the helm to windward: a *lee helm*, which every seaman dislikes, because a ship that will not come to the wind of her own accord is a ship that cannot be trusted in a squall. Luce: "seamen have more patience with a ship disposed to approach the wind than with one needing the continued action of the helm to keep her from falling off... a midship helm is still the golden mean, though tending, as it should, towards the former" (Luce 1866, ch. XXIV, 'Tacking'). Lever, before tacking: "to have her so suited with Sail as nearly to steer herself, with little assistance from the Rudder: by which management her way will be more powerful through the Water" (Lever, 'Tacking Expeditiously').

### Reading it in `state`

`helm` in `state` is the rudder angle, positive to starboard. Read it against the tack: helm held toward the lee side means she is carrying weather helm.

| Tack | Weather helm | Lee helm |
|---|---|---|
| starboard (wind from starboard) | helm negative | helm positive |
| larboard | helm positive | helm negative |

The frigate under plain sail close-hauled on the starboard tack shows `helm -1°`: a touch of weather helm, which is right (package 10 measured +0.9° of weather helm close-hauled, +1.9° on a beam reach, +5.0° with the headsails in and −2.1° of lee helm with the spanker in, which is truth 6 of `docs/dev/TuningNotes.md`). The schooner in the same breeze shows `helm -4°` on the starboard tack, a firmer weather helm, and hers wanders a few degrees either way as the gusts come.

### What to do about it

The game moves each sail's force at that sail's own position along the hull, so shifting canvas fore or aft really does shift the balance. The period remedies, all of which are orders you can give:

- **Too much weather helm** (she gripes): ease the spanker sheet or take in the spanker; set the jib and flying jib, or the fore topmast staysail; take a reef in the mizzen topsail; brace the after yards in a little.
- **Lee helm** (she falls off): the reverse; haul the spanker sheet aft or set the spanker; haul down the flying jib; brace the head yards a little in and the after yards sharp.

```orders frigate plain-sail
ease the spanker sheet two fathoms
set the flying jib
reef the mizzen topsail, one reef
haul down the flying jib
haul aft the spanker sheet
brace the after yards sharp up on the starboard tack
```

The helmsman will steer the course you gave regardless, up to the rudder's 35°, but a ship sailed with a big rudder angle drags, and the tack in the next chapter needs her to answer quickly. Lever's advice stands: balance her first.
