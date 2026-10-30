# 8. Where to read more

The three books are in `docs/references/` as OCR text from Internet Archive scans (provenance in `docs/references/README.md`). They are searchable but not clean: expect garbled words and broken tables, and check anything numeric against the scan before you trust it. Luce's 1891 revision is cleaner to read in a browser at https://maritime.org/doc/luce/index.php.

To find a passage, search the text for its sub-heading; the OCR sets headings in capitals:

```
grep -n -i "box-hauling" docs/references/luce/luce-1866-seamanship-1877-printing-ocr.txt
grep -n "TACKING EXPEDITIOUSLY" docs/references/lever/lever-1827-young-sea-officers-sheet-anchor-ocr.txt
grep -n "^CLOSE-HAULED" docs/references/falconer/falconer-1780-universal-dictionary-of-the-marine-ocr.txt
```

Luce 1866's table of contents (about line 260 of the file) lists the sub-topics of every chapter, which is the quickest way in; `docs/references/LuceChapterMap.md` maps his chapters to the game's systems.

## The evolutions and their sources

Every file in `data/evolutions/` ends with a `source:` line. Read the passage and you have read what the game encodes.

| Evolution | Order | Source |
|---|---|---|
| `set_square` | `set the fore topsail` | Luce 1866, ch. XXIII At Sea, 'To set a Topsail', 'To set a Top-gallant sail', 'To set a Foresail'; Lever, 'Setting the Topsails' |
| `take_in_square` | `take in the fore topsail` | Luce 1866, ch. XXIII, 'To take in a Topsail', 'To take in a Top-gallant sail', 'To take in a Course' |
| `furl_square` | `furl the fore topsail` | Luce 1866, ch. XX In Charge of the Deck, 'To Furl Sails'; ch. XXIII, 'To take in and furl the mizzen-topsail in a gale' |
| `reef_square` | `reef the topsails, one reef` | Luce 1866, ch. XXVII Reefing, 'Reefing and Hoisting'; Lever, 'Reefing Topsails' |
| `shake_out_square` | `shake out a reef in the fore topsail` | Luce 1866, ch. XXVII, 'To shake out a Reef', 'To turn out Reefs' |
| `set_gaff` | `set the spanker` | Luce 1866, ch. XXIII, 'The Spanker' (setting); Luce 1884, ch. XXXIV Handling Fore-and-Afters |
| `take_in_gaff` | `take in the spanker` | Luce 1866, ch. XXIII, 'The Spanker' (taking in); Luce 1884, ch. XXXIV |
| `furl_gaff` | `furl the spanker` (refused: gaff sails are taken in) | Luce 1866, ch. XX, 'To Furl Sails'; ch. XXIII, 'The Spanker' |
| `reef_gaff` | `reef the mainsail` (schooner) | Luce 1866, ch. XXVII, 'In reefing a spanker', 'Boom Mainsail'; Luce 1884, ch. XXXIV |
| `shake_out_gaff` | `shake out a reef in the mainsail` | Luce 1866, ch. XXVII, 'To turn out Reefs', 'Boom Mainsail' |
| `set_jibheaded` | `set the jib` | Luce 1866, ch. XXIII, 'To set a Head Sail' |
| `take_in_jibheaded` | `haul down the jib` | Luce 1866, ch. XXIII, 'To set a Head Sail' (to take it in) |
| `furl_jibheaded` | `furl the jib` | Luce 1866, ch. XXIII, 'To set a Head Sail' ('Lay out and stow the jib') |
| `set_studding` | `set the fore topmast studdingsail, lee` | Luce 1866, ch. XXIII, 'The Topmast Studding-sail', 'To set a lower Studding-sail'; ch. XI Sails, 'Studding-sails' |
| `take_in_studding` | `take in the studdingsails` | Luce 1866, ch. XXIII, 'To take in the topmast studding sail', 'To take in [the lower studding-sail]' |
| `brace` | `brace sharp up on the starboard tack` | Luce 1866, ch. XXIV Working to Windward, 'To Trim Yards', 'Table of best angles of yard with keel'; ch. XXV 'Bracing Yards' |
| `tack` | `tack ship` | Luce 1866, ch. XXIV, 'Tacking', 'Missing Stays'; Lever, 'Tacking Expeditiously' |
| `wear` | `wear ship` | Luce 1866, ch. XXIV, 'Wearing', 'Second Method'; Lever, 'Veering or Wearing' |
| `heave_to` | `heave to` | Luce 1866, ch. XXVI Emergencies, 'To heave to' (mizzen topsail aback), 'To heave to with the fore topsail to the mast' |
| `fill_away` | `fill away` | Luce 1866, ch. XXVI, 'To fill away, after lying to with the main topsail to the mast' |

The rest of the handling, most of it from Luce 1884:

| Evolution | Order | Source |
|---|---|---|
| `boxhaul` | `box haul` | Luce 1884, ch. XXIV, 'Box-hauling'; Luce 1866, ch. XXIV 'Box Hauling'; Lever, 'Missing Stays, Waring Short Round, Box-hauling' |
| `wear_short_round` | `wear short round` | Luce 1884, ch. XXIV, 'To Wear Short Round'; Luce 1866, ch. XXIV |
| `lie_a_try` | `lie a-try` | Luce 1884, ch. XXIX In a Gale, 'Reducing Sail to a Gale', 'Lying to'; Falconer, *Trying* |
| `scud` | `scud` | Luce 1884, ch. XXIX, 'To Scud', 'Remarks on Scudding'; Falconer, *Scudding* |
| `back_and_fill` | `back and fill` | Luce 1884, Appendix I In a Tideway, 'Backing and Filling' |
| `send_down_topgallant_masts`, `sway_up_topgallant_masts` | `send down the topgallant masts` | Luce 1884, ch. XX Port Drills, 'To Send Down Topgallant-Masts'; ch. XXIX, 'Preparations for a Gale' |
| `send_down_topgallant_yards`, `cross_topgallant_yards` | `send down the topgallant yards` | Luce 1884, ch. XXIX, 'To Send Down Royal Yards'; ch. XX, 'To Cross Topgallant and Royal Yards' |
| `strike_topmasts`, `fid_topmasts` | `strike the topmasts` | Luce 1884, ch. XVIII, 'Station Billet' ("Strike and fid topmasts"); Luce 1866, ch. XXXIV 'Housing Topmasts' |
| `rig_out_studdingsail_boom`, `rig_in_studdingsail_boom` | `rig out the fore topmast studdingsail boom` | Luce 1884, ch. XXIII, 'The Topmast Studding-sail' ("Set taut! Rig out! Hoist away!") |
| `unbend_sail`, `bend_sail`, `shift_sail` | `shift the fore royal` | Luce 1884, ch. XX, 'To Unbend Sail', 'Bending Sail'; ch. XXXII Shifting Sails and Spars |
| `goose_wing` | `goose-wing the foresail` | Luce 1884, ch. XXIV, 'To Wear in a Gale ...' ("A foresail in this state is 'goose-winged'") |
| `loose_sails_to_dry`, `furl_all` | `loose sails to dry`, `furl all` | Luce 1884, ch. XX Port Drills, 'To Loose Sail to the Buntlines', 'To Furl Sail' |

The crew orders are not evolutions: `call all hands`, `pipe down` and `relieve the watch` reach the watch routine at once (Luce 1884, ch. XVIII Organization and ch. XX; the watch, quarter and station bills), and `muster` is the console's reading of the watch bill.

The anchor's evolutions (ch. XIV, XV, XXI, XXXIV), the port's and the fishing gear's, the action's and the repairs' are cited in the chapters that work them (13, 14, 21, 22 and 25), and the library's catalogue gives every evolution with its source. Not yet written: club-hauling (Luce 1866, ch. XXIV, 'Club Hauling') and chapelling (ch. XXV Wind Baffling).

## The words, by chapter of this book

**Chapter 1, the ship.** Falconer: *Mast*, *Yard*, *Bowsprit*, *Courses*, *Top-sails*, *Royal*, *Mizen*, *Driver*, *Jib*, *Stay*, *Studding-sails*, *Brace*, *Sheet*, *Tack*, *Lifts*, *Bowline*, *Buntlines*, *Reef-tackle*, *Gaff*, *Boom*, *Vangs*, *Peak*, *Earings*, *Gasket*, *Larboard*, *Starboard*. Luce 1866, ch. VII The Mast (spars), ch. X Rigging Ship (every rope in order), ch. XI Sails. Lever's plate of the square sails, figures 291 and 292, names them all with letters, and his early chapters rig the ship spar by spar.

**Chapter 2, the wind.** Falconer: *Wind*, *Close-hauled*, *Large*, *Tack* ("a ship is said to be on the starboard or larboard tack"), *Lee*, *Luff*, *Bearing*, *Sailing*. Lever, figures 396 to 398 (the six-point rule). Luce 1866, ch. XXIV, 'Steering' and 'Conning' (*No higher*, *Nothing off*, *Very well thus*, *Keep her a good full and by*); ch. I The Compass; ch. XXVIII Storms, 'Table of force and velocity of wind'.

**Chapter 3, making sail.** Falconer: *Reef*, *Reef-band*, *Reefing*, *Points*, *Furling*, *Studding-sails*, *Aback*. Luce 1866, ch. XXIII At Sea, the whole chapter, and 'General Remarks on making and taking in Sail'; ch. XX In Charge of the Deck, 'The Trumpet', 'Commands' (the words of command in port routine); ch. XXVII Reefing. Lever, 'Setting the Topsails', 'Reefing Topsails', 'Studding Sails'.

**Chapter 4, trimming.** Falconer: *Trim*, *Brace*, *Sheet*, *Luff*. Luce 1866, ch. XXIV, 'To Trim Yards', 'Table of best angles of yard with keel', and the remark on weather helm under 'Tacking'; ch. XXV Wind Baffling, 'Bracing in', 'Bracing up'. Lever, 'Tacking Expeditiously' (the ship suited with sail "as nearly to steer herself") and his opening pages on the effect of the sails before and abaft the centre of gravity.

**Chapter 5, going about.** Falconer: *Tack* (to tack), *Veering*, *Wearing*, *Lying-to*, *Aback*. Luce 1866, ch. XXIV, 'Tacking', 'To Haul of All', 'Missing Stays', 'Club Hauling', 'Wearing', 'Box Hauling', 'To Wear short round', 'Half Boards'; ch. XXV, 'Taken Aback'; ch. XXVI, 'To Heave to'. Lever, 'Tacking Expeditiously', 'Veering or Waring, Taken A-back', 'Lying to under different sails, Waring', 'Missing Stays, Waring short round, Box-hauling', 'Heaving to, Sounding', 'Sounding, Box and Club-hauling'. Luce 1884, ch. XXXIV Handling Fore-and-Afters (the schooner: 'To Wear', and tacking a sloop).

**Chapter 6, the watch.** Falconer: *Watch*, *Watch-glasses*, *Log*, *Log-board*. Luce 1866, ch. XVI Organisation, 'The Watch Bill', 'Calling the Watch'; ch. III The Log; Luce 1884, ch. XVIII Organization ('Duties of Men in Different Parts of the Ship', the station bill), ch. XX (the watch, quarter and station bills; "the marines of a ship are divided between the two watches"), 'The Officer of the Deck' (relieving and mustering the watch), App. G Routine.

## Where each thing is, for a reader at a station

The library a model reads (and `library(topic='contents')` lists) is this book and the game's own pages, each a topic:

| Topic | What it holds | Its chapter here |
|---|---|---|
| `primer` | this book, chapter by chapter, section by section | all |
| `grammar` | the whole order language in six parts, generated from the game's own tables: **the order language** (every verb and synonym, the free lines and your person's own), **the readings** (every reading with what it answers), **the standing dialect** (the sentence, every trigger, condition, duration and the book's orders), **the voice** (say, say to, tell, ask, the lookout's hail, the hail of a sail), **the stand-by** (every event, interval and tripwire a station may wait for) and **the world orders** (the director's forms with examples) | 3 to 5 (the orders), 6 and 10 (the readings), 11 (the dialect), 19 and 23 (the voice), 19 (the stand-by), 20 (the world orders) |
| `catalogue` | every evolution the ship can perform: its order, hands, time and source | 3, 5, 13, 14, 21, 22, 25 |
| `the ship` | this ship's spars, sails and lines by mast, her groups and aliases | 1 |
| `papers` | the ship's papers by handle: her muster, her orders, her epitome, her signal book, her prices and the news | 14, 23 |
| `standing orders` | the book as it stands | 11 |
| `books` | the books drafted aboard | 14 |
| `tools` | a model's tools, each with its words | 16, 19 |
| `the world` | how the world behaves, for the director | 20 |

What a station may do is its chapter's: the officer of the watch chapter 16, the captain 17, the master, the lookout and a passenger 19, the director 20; what every person aboard may do whatever his station (move about the ship, go ashore, eat, drink, sleep, read, say and say to, hail a sail) is chapter 14's places and reach, chapter 19's conversation and needs, and the grammar's first part.

## The game's own data

- `data/vocabulary.yaml`: every verb and synonym the parser knows, the brace modes, the group evolutions; the library's `grammar` topic is the same, rendered.
- `data/ships/*.yaml`: every noun of each ship, with the source beside each figure; the library's `the ship` topic lists the one you are aboard.
- `data/evolutions/*.yaml`: each evolution's steps, hands and times, its source at its head; the library's `catalogue` topic is the same, rendered.
- `docs/agents/Harness.md`: how a model is connected to a station, for whoever runs the game.
