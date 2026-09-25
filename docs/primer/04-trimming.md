# 4. Trimming

"Trim, when applied to the sails, denotes the general arrangement which is best calculated to accelerate the ship's course, according to the direction of the wind" (Falconer, *Trim*). On a square-rigger it is two jobs: the yards are *braced* to the wind, and the fore-and-aft sails are *sheeted* to it. A third, keeping the ship herself balanced so that she needs little helm, is what the other two are for.

## Bracing the yards

The braces swing a yard round in the horizontal (Falconer, *Brace*). The order names how far and, when it matters, for which tack:

| Word | The yard goes to | When |
|---|---|---|
| **sharp up** | its brace limit, about 55° from square below and up to 62° aloft | close-hauled |
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
  Morning watch (04:06)  Order: brace sharp up on the starboard tack.
  Morning watch (04:06)  Man the fore yard braces.
  Morning watch (04:06)  Man the fore topsail yard braces.
* Morning watch (04:06)  Braced the fore yard; 55° from square.
* Morning watch (04:06)  Braced the fore topsail yard; 58° from square.
* Morning watch (04:06)  Braced the fore topgallant yard; 60° from square.
* Morning watch (04:06)  Braced the fore royal yard; 62° from square.
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
  Morning watch (04:21)  Order: back the main topsail.
  Morning watch (04:21)  Man the main topsail yard braces.
  Morning watch (04:21)  Laid the main topsail yard aback, braced up for the larboard tack; the main topsail to the mast.
* Morning watch (04:21)  Main topsail taken aback.
* Morning watch (04:22)  Braced the main topsail yard; 58° from square.
```

To fill it again, `brace the main topsail sharp up` for the tack she is on. The refusals: "Back what? Name a yard or a square sail, such as the main topsail"; the spanker "is a gaff sail; it has no yard to brace."

### How sharp, and which yards sharper

Luce's rule for a stiff breeze is to brace the lower yards up sharp and trim each yard above by the one below, "with the weather yard arm about a half point abaft the lower yard", because the upper sails are flatter and the lighter yards need the support; in light airs with smooth water "the yards of no ship can lie braced up too sharp"; with the wind abaft the beam the after yards should be braced sharper than the head yards so that the wind fills the forward sails (Luce 1866, ch. XXIV Working to Windward, 'To Trim Yards', and the 'Table of best angles of yard with keel'). Lever adds that in practice the yard is braced up sharper than the six-point geometry needs, "to make the Sail stand to the most advantage" (Lever, figure 397).

What the game does now is simpler. Each yard has its own limit in the ship file, and the limits are set from the standing rigging's clearance, which lets the upper yards go a few degrees *sharper* than the lower, not less; `brace sharp up` takes every yard to its own limit. The steering advantage Luce describes, upper yards a little in so that the royal lifts first and "all the other sails are a clean full and by", is not modelled. A player who wants Luce's trim can brace mast by mast (`brace the fore yards sharp up`, then haul a weather topgallant brace a little), but nothing in the physics yet rewards it.

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

A fore-and-aft sail is trimmed by its sheet: hauled in for the wind ahead, eased off as it draws aft (Falconer, *Sheet*). The game measures a gaff sail's or jib's trim as the angle of its foot from the centreline, and each haul or ease moves it five degrees:

```orders frigate plain-sail
# rejected: haul the spanker sheet
ease the spanker sheet a fathom
ease the spanker sheet two fathoms
haul the spanker sheet
haul in the spanker sheet handsomely
haul aft the spanker sheet
# rejected: haul the spanker sheet aft
ease the jib sheet, lee
haul the jib sheet aft, lee
ease the fore topmast staysail sheet, lee
```

"The mizzen spanker sheet is already hard in" is the first refusal: the sheet was hauled flat when the sail was set. The second line puts the boom 5° off the centreline, the third 15°, the fourth back to 10°. **Haul aft** (or *aft* after the sheet's name) hauls it all the way: "Hauled the mizzen spanker sheet flat aft; the mizzen spanker now amidships", and a sheet already flat is refused a second time.

A square sail's sheets, tacks and bowlines are hauled home when it is set and stay there; ease one and the log counts it off in tenths ("Eased the larboard (lee) main course sheet; now nine-tenths hauled"). **Sheet home** the sail, or **haul home** its sheets, and they are hauled home again and belayed; the plural names both sheets at once. Their trim is the yard's business.

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

Between your orders **the watch on deck tends the fore-and-aft sheets for you**: each set jib, staysail and gaff sail is sheeted to the apparent wind as she comes up or falls off, at about a degree a second (`freesail/evolutions/trim.py`). Square sails are never touched without an order. So after a tack the spanker and jib will find their trim by themselves, but the yards will sit where the tack left them until you brace.

## The `trim` order

Package 13 adds the order the owner reached for at the gate. It braces every yard that has sail set to the best angle for the present apparent wind, each as its own `brace` evolution, and sheets the fore-and-aft sails at once:

```orders frigate plain-sail
trim the yards
trim the sheets
trim sails
```

`trim the yards` is what Luce means by "trim the yards, haul taut the lifts and braces" after a tack or a wear; `trim the sheets` is "trim aft the head sheets"; `trim sails` is both. `brace the yards to the wind` is `trim the yards` by another name, and takes the yards you name.

## Weather helm and lee helm

A ship whose after sails press harder than her head sails wants to come up into the wind; the helmsman must hold the helm to leeward to keep her off, and she is said to *carry a weather helm* or to *gripe*. One whose head sails overpower her after sails falls off and needs the helm to windward: a *lee helm*, which every seaman dislikes, because a ship that will not come to the wind of her own accord is a ship that cannot be trusted in a squall. Luce: "seamen have more patience with a ship disposed to approach the wind than with one needing the continued action of the helm to keep her from falling off... a midship helm is still the golden mean, though tending, as it should, towards the former" (Luce 1866, ch. XXIV, 'Tacking'). Lever, before tacking: "to have her so suited with Sail as nearly to steer herself, with little assistance from the Rudder: by which management her way will be more powerful through the Water" (Lever, 'Tacking Expeditiously').

### Reading it in `state`

`helm` in `state` is the rudder angle, positive to starboard. Read it against the tack: helm held toward the lee side means she is carrying weather helm.

| Tack | Weather helm | Lee helm |
|---|---|---|
| starboard (wind from starboard) | helm negative | helm positive |
| larboard | helm positive | helm negative |

The frigate under plain sail close-hauled on the starboard tack shows `helm -2°`: a touch of weather helm, which is right. The schooner in the same breeze shows `helm +5°` on the starboard tack: a lee helm, which is a fault of her present tuning (her centre of lateral resistance is under review in package 8 and 10) and worth watching when you sail her.

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
