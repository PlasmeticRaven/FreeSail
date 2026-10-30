# 21. The fisherman

The smack and the lugger fish. Not a fishing simulation, but what the game can fairly do: the grounds of the Channel and of the north of the Bay as the period worked them, each with its fish, its season and its yield; the gear a fishing vessel carries and the evolutions that work it, with the hands at them and their hours; the catch into the well or the hold, the hold's salt, and the fish that will not keep; and the quay that buys it. The business's fishermen (chapter 15) fish the same grounds by the same rule and land their catch at home, and a fishing vessel near you is promoted like any other ship, so the glass on her shows the work truly.

## The grounds

A ground is a stretch of sea the fishermen knew: the oozy ground off the Eddystone where the Plymouth trawlers worked "only a few miles from the land" (Holdsworth 1874 p. 44), the Poll Bank off Scilly, the drift ground in Mount's Bay, the seine grounds of Gerrans Bay and St Ives Bay, the trawling ground off Berry Head where the Brixham men towed, the Iroise and the soundings off Ushant, and off Glenan and Belle Isle the Breton sardine. Each is keyed to a feature of the chart where the chart has one, else pricked at a position with its source (`data/fishing/channel-west.yaml`, `biscay-north.yaml`). Ask for them:

```
the fishing grounds
```

```
The grounds about her: The seine ground in Gerrans Bay, within a mile off (seine: pilchards July to December by day; mackerel June to August by day). The oozy ground off the Eddystone, 19 miles off (trawl: soles and turbot all the year at any hour; plaice and hake all the year at any hour; drift nets: mackerel April to July by night; herrings October to December by night; lines: ling and conger all the year at any hour). ...
```

The seasons are the sources': the pilchard "from July to December" off Cornwall (Holdsworth p. 130; the Britannica of 1810, "about the middle of July, disappearing the beginning of winter"), the St Ives seans "from September to November" (p. 188), the mackerel of the Cornish drivers "towards the end of February ... into June" and in the Channel "May, June, and July" (pp. 127 to 128). The yields are judgement, set out with their reasoning in the head of each table: a small sean's hour round a shoal takes some fifteen hogsheads of pilchards, three tons, where the great seans of St Ives took thousands; a fleet of drift nets six or eight hogsheads in a night; a trawl half a ton in a haul of five or six hours, a fifth of it soles and turbot. A bottom or a bank the tables do not name keeps a plain default of plaice, hake and ling.

## The gear

A vessel carries the gear her file says and no other, each piece with its source (`tools/gen_ships.py`): the smack a beam trawl of thirty-six feet, a string of longlines of 2,340 hooks and a small tuck-sean for her boat; the chasse-marée a fleet of sixty drift nets and her lines. The orders:

| Order | What the hands do | Its time |
|---|---|---|
| `shoot the trawl` | the beam over and the warp veered; she tows it with the tide under easy sail | a quarter of an hour |
| `haul the trawl` | all hands; she rounds to the trawl, two at the winch heave in the warp, the bag hoisted in | three quarters of an hour (Holdsworth p. 79), more in a seaway |
| `shoot the nets` | the drift nets over the quarter, before the wind, at sunset | half an hour |
| `haul the nets` | all hands at the capstan, the fish shaken out of the meshes | two hours |
| `shoot the seine` | the boat rows the sean round the shoal, by day, in a bay | twenty minutes |
| `haul the seine` | all hands; the circle closed, the bunt raised, the fish tucked into the boat | an hour |
| `set the lines` | the lines paid out across the tide under easy sail with the wind free | an hour |
| `haul the lines` | all hands; the end buoy aboard, short tacks along the line, the cod into the well | three hours |
| `shoot the gear`, `haul the gear` | the gear the ground she is on wants in this month, of what she carries | |

The shot is refused in words when she carries no such gear, is on no ground the master knows (the refusal names the nearest), finds nothing of it in season ("Nothing is taken on the seine ground in Gerrans Bay by the seine in February: pilchards July to December by day; ..."), or at this hour (the seine by day, the drift nets by night), or has more wind than the gear is worked in. While the gear is out she is at it in the work in hand ("towing her trawl", "riding to her nets", "her boat at the seine", "lying to her lines"), and a sail beyond its allowance is refused: "The trawl is in the water (towing her trawl); it allows plain sail, courses, storm canvas and no more. Haul the trawl first." The trawl drags: the smack that makes five knots and a half under plain sail in a moderate breeze tows at two and a quarter, as Holdsworth's smacks towed a knot or so faster than the tide (pp. 77 to 78); with more way than four knots it lifts off the ground and takes nothing. The other gear puts no drag on her: heave to and ride to it.

The gear fishes a minute at a time while it is in the water, by the ground's yield, the season, the hour (half as much again at the change of light for the night's fish, which "strike" the net "just after sunset and before sunrise", pp. 98 to 99) and the wind; a shot fishes so many hours and no more (the seine an hour, the trawl six, the nets a night).

## The catch, the well and the hold

Hauled, the take is struck below: into the well first, its running water keeping a cod or a sole alive for days (Steel 1805, WELL: "to contain live fish ... and preserved alive"; Holdsworth p. 138, the cod "put alive into the well"), and a pilchard or a mackerel, which dies when it is taken, cool for a day; then into the hold, salted while there is salt aboard (a third of the fish's weight, struck out of the manifest), green if there is none. Green fish keep twelve hours in summer for a pilchard, eight for a mackerel, more in winter and more for the flat fish; the catch's line every morning says what is aboard and how long it keeps, and a lot that turns is said once:

```
Hauled the seine: 1 ton of mackerel, 2.9 tons of pilchards. Struck down: 1 ton of mackerel in the well; 2 tons of pilchards in the well; 0.9 tons of pilchards in the hold, unsalted.
The pilchards in the hold have spoiled: 0.9 tons, fit for nothing but the farmers' dung.
```

`the catch` asks it at any time; the manifest and the purser's stores say it too.

## The quay

In a port with a fish quay (Falmouth, Plymouth, St Mary's, Torbay, Dartmouth, Weymouth, Brest, Roscoff, Morlaix, Lorient, Le Palais, St Malo: `data/fishing/fish.yaml`), `sell the catch` lands it by the boat and sells the sound fish at the quay's price, fresh or salted; the spoiled go over the side, and the line says both and the purse after. This is the fish quay, apart from the port's market of chapter 14, which deals in the cured and pressed hogshead.

## The business's fishermen, and a fisherman near you

The fishermen of the world's business (chapter 15) work the same grounds by the same gear's times and the same catch to the ounce, and land their catch at their home's quay. A fishing vessel within four miles is awake like any other ship: her captain shoots the gear the ground wants when it fishes at the hour, heaves to and rides to it, hauls when the shot is full or the hour no longer serves, and runs home when the trip's hours are done; all of it orders through her own channel and lines in her own log, never yours.

## Where it comes from

Holdsworth, *Deep-Sea Fishing and Fishing Boats* (1874; `docs/references/holdsworth/`), for the trawl (pp. 44 to 86), the drift nets (pp. 98 to 132), the seans (pp. 156 to 160), the lines (pp. 136 to 141) and the Cornish stations and the pilchard's curing (pp. 187 to 196); the Encyclopaedia Britannica's fourth edition (1810), CLUPEA, for the pilchard's season and the hogshead's price; the Musée de la Pêche at Concarneau for the Breton sardine taken with the cod's roe; Steel 1805 for the well. Every yield, keeping time and fish-quay price that no page gives is judgement and says so where it is written.
