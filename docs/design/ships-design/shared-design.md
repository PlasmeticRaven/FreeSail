# Design: the shared work of package 75 (Phase 3), for the build document

The work across all the ships, not one ship's: the hull profile in every file, the viewer
drawing it, the lee ports wired, the sub-types as fits and roles, every file's armament, bill
and marines, the privateer schooner's file, the charges by Table No. 29, what the frigate's
quarterdeck would move, and the scenarios' common ground. A scratch for the build document's
writer to fold in. Nothing is built.

**Where.** The clone `D:/Projects/FreeSail/FreeSail-pkg-75` on the package's branch at 6b94731 (the
lead's 3421829 merged: 73, 86, 84's steps 1 and 2). Every `file:line` is at that head. Paths
are from the repository root.

**What binds, in order:** the brief (`docs/dev/M7-WorkPackages.md:1540-1653`); the lead's
go-ahead of 2026-10-28 (the Indefatigable first; the gate on the three engine extensions
only; 84's World read through the names the Hull keeps); the plan
(`docs/design/Plan-ShipsWorkflow.md`, Phase 3; the new ships in `tools/ships/`); the decision
sheet (`docs/design/Decisions-ShipsRound2-2026-10.md:1-80` above all); the research notes
(**Ind**, **Neuf**, **Bil**, **Eng**, **Bel**); the two code maps (`map-generator.md`,
`map-engine.md`, this scratch directory).

**Marks.** *read*: the code or the page cited. *measured*: arithmetic or a scratch script
(`heels2.py`, this directory). *catalogue*, *secondary*, *memory*, *judgement*, *observed* as
the notes use them. "Plainly:" marks a choice that departs from a decision, a ruling or the
brief, with the reason.

**Two private pages read for this design** (facts only, cited by table; the images stay in
`D:/Projects/FreeSail/owner-notes/indefatigable/rmg/`):
- Steel 1805, *Naval Architecture*, **Folio I** (the dimensions table;
  `steel1805-naval-architecture-folio-I-load-draught-IAleaf487.jpg`). Read.
- The Regulations and Instructions 1806 (1808 printing), **Table No. 29**, the gunpowder for
  each nature of ordnance (`regulations1806-1808printing-table29-gunpowder-IAleaf533.jpg`;
  the repository's OCR has the title at `docs/references/admiralty/regulations-and-instructions-1808-ocr.txt:27498-27502`
  and lost the figures). Read; the 18-pounder's ounce figure checked on a crop.

---

## Decisions taken

| # | Decision | Why, in short |
|---|---|---|
| S1 | One new optional key, `hull.profile`, in every file through the generator, with the rail (sheer), the decks at side, the stem, the stern, the main wale, the half-breadths by station and one tier per gun deck (its sill line, the side's half-breadth at the sill, the port's size) | The brief's dozen points, plus the two the owner's rules need: the plan's half-breadths for a true side, the half-breadth at the sill for the lee port (Bel §13.1 answer 7) |
| S2 | Every profile height is metres above **the file's waterline, taken as the load line its sill source states**; x from midships, forward positive | The file's draught moves every sailing pin, so it stays; the freeboard figures the sources give are freeboards at load |
| S3 | Each gun's `height_m` is written by the generator from its tier's sill line at the gun's own `x_m`, to the centimetre. No gun's `x_m` moves | A gun's height is read nowhere in the engine today (grep), so new heights move nothing until the lee port reads them; an `x_m` is read by the quarters and the divisions |
| S4 | A `deck` key on a port gun (the tier's name), shared by the lee port and the 74's bill by deck | The owner's "a deck key on each gun" (Decisions:38); the 74's design gives the bill its meaning |
| S5 | **D18, proposed: (a) kept for every file.** `deck_height_m` stays the spars' and the physics' datum, the uppermost continuous deck at midships; the viewer draws the true sides from the profile, the lower masts down to the drawn deck and the bowsprit from the stem head | No existing spar moves, so no pin moves; the razee's two costs under (a) (side drawn below her rail, bowsprit rooted at the gun deck) both go with the drawn profile |
| S6 | The lee-port rule (Bel §13.1 answer 7): a port's dip is the heel toward its side plus the roll's amplitude; it shuts when its sill, lowered by the side's half-breadth at the sill times the sine of the dip, stands a foot or less above the water; it opens again six inches clear (judgement). Ports only: a pivot and a rail gun fire over the rail | The owner's rule; the six inches stop a port flickering in a gust |
| S7 | The lee port in three steps, each its own commit: L1 the sourced sills (data only), L2 the gate on heel, L3 the roll added | The ruling's proof by bisection falls on the commits |
| S8 | The armed Indiaman and the revenue cutter are **new roles** with doctrine files; the hired armed cutter, the packet and the privateer are existing roles on described fits; a scenario's far ship may name `role:` within its description's list | The brief item 4; "where a role is new" |
| S9 | `armament.default: unarmed`, a reserved word: the topsail schooner, the lugger and the smack carry fits for the editor and sail unarmed by default | The owner's trade trial: the armed Speedwell made the merchant schooner engage |
| S10 | `privateer-schooner.yaml` is **kept beside** the *Prince de Neufchatel*; her arc and fits come from her type's records | The owner's answer against a fit stands on file; the Neufchatel is another hull and rank |
| S11 | The charges are Table No. 29's, keyed by kind and calibre, in place of the shares | The table is read |
| S12 | The frigate's quarterdeck is not corrected; §8 says what correcting it would move | The owner's ruling of 2026-10-25 |
| S13 | A scenario may carry a `nations:` block that sets the table's wars and letters of marque at its date | The Neufchatel's 1814, the bilander's 1794 and the 74's 1815 each need a war table the 1805 file does not have |
| S14 | The gunner's fillers stay read and never moved; the posts that compete for hands are left to 77 | §5.3: it moves every armed ship's muster and quarters in the same build as the lee port |

---

## 0. The order of the shared work against the ship builds

The lead's go-ahead: the ships one at a time, the Indefatigable first. The shared work runs as
one track beside them, owned by one builder (the "shared builder"), except the scenarios.

| Step | What | After | Before | Moves pins |
|---|---|---|---|---|
| Stage 0 | The interfaces of §11, inert | the merge of 3421829 (done) | everything | none (proven) |
| SW-1 | Table No. 29's charges (§7) | stage 0 | B1's magazines, so the 64's 32-pounders come right first time | the frigate's, brig's, cutter's and privateer's charges and barrels; two `test_magazine` rows |
| SW-2 | The profiles of the existing eight and their sourced sills (§1), L1 | stage 0 | SW-3, SW-5 | none (bytes only) |
| B1 | The 64 and the razee, with their profiles from the first commit | stage 0 | | hers |
| SW-3 | The viewer draws the profile (§2) | SW-2, and B1's razee file | the owner's screenshot check | none expected; pictures measured |
| SW-4 | The sub-types, the roles, the fits and bills of the schooner, lugger and smack, the privateer's arc (§4-§6) | stage 0 | the scenarios | the privateer's pivot pins if her arc moves |
| SW-5 | The lee ports L2 then L3 (§3) | SW-2; every file then on the branch carrying a profile | the 74's and the razee's combat truths | combat pins, bisected |
| B2-B5 | The Neufchatel, the bilander (behind the engine gate), the 74 | each in turn | | theirs |
| Scenarios | One per ship (§9) | that ship's file, SW-4, stage 0's `nations:` | | none existing |

Judgement on the order: SW-1 early because `fit_magazine` calls `charge_lb`
(`tools/gen_ships.py:3629`), so every new file written after it is right without a second
regeneration; SW-5 before the 74's file is pinned, because the 74's port truth is measured
with the rule in.

---

## 1. (a) The hull profile through the generator, for every file

### 1.1 What the key holds

Under `hull`, after `rudder` (so the existing keys keep their order and bytes), written by
the generator alone. Illustrative figures:

```yaml
hull:
  ...
  rudder: {...}
  # The hull's profile (package 75): ... (the section's sources)
  profile:
    # The top of the side, taffrail to stem head: ...
    rail_m: [[-22.6, 4.95], [-12.0, 3.6], [0.0, 3.27], [12.0, 3.5], [22.9, 4.4]]
    # The decks at side over their extents: ...
    decks:
      upper deck: [[-21.0, 2.3], [0.0, 1.8], [21.0, 2.25]]
      quarterdeck: [[-21.5, 4.4], [-6.0, 4.1]]
    # The stem's fore edge, the forefoot to the head: ...
    stem_m: [[21.6, -4.6], [22.3, 0.0], [23.0, 3.0], [23.2, 4.4]]
    # The post at the water, the counter's knuckle, the taffrail: ...
    stern_m: [[-21.0, -4.6], [-21.3, 0.0], [-21.9, 2.4], [-22.6, 4.95]]
    # The main wale, its lower and upper edges: ...
    wales_m: [[-18.0, 0.25, 1.15], [0.0, 0.1, 1.0], [18.0, 0.3, 1.2]]
    # The half-breadths at the water and at the rail by station: ...
    breadth_m: [[-20.0, 4.2, 3.9], [0.0, 5.84, 5.45], [20.0, 3.4, 3.5]]
    tiers:
    # The upper deck's ports: ...
    - deck: upper deck
      sill_m: [[-16.5, 2.55], [0.0, 2.34], [16.5, 2.5]]
      half_breadth_m: [[-16.5, 5.1], [0.0, 5.6], [16.5, 4.8]]
      port_m: [0.86, 0.79]
```

- `rail_m` and `breadth_m` are required when a profile is given (the drawing needs both);
  the rest optional. A hand-written file may carry no profile at all, and is drawn and fought
  as today.
- `decks` names each deck at side over its own extent: the uppermost continuous deck, and any
  raised quarterdeck, forecastle or poop. The razee's gun deck runs the length; her
  quarterdeck and forecastle stand over their own extents (Ind §2.3.5).
- `tiers` has one entry for each deck that carries ports. `port_m` is the opening's width
  and depth, for 81's ports. A swivel and a pivot have no tier.
- Points are rounded to the centimetre. x runs aft to forward in `rail_m`, `decks`,
  `wales_m`, `breadth_m` and the tiers. `stem_m` and `stern_m` run from low to high.

Plainly: `decks`, `breadth_m` and the tier's `half_breadth_m` are beyond the brief's list
(sheer, stem, stern, wales, sills). They are there because the viewer cannot draw a true side
without the plan's half-breadths, and the owner's lee-port rule takes the side's half-breadth
at the sill from the profile (Bel §13.1 answer 7). Each is a few points.

### 1.2 The schema (`freesail/ship/schema.py`)

- New dataclasses `HullProfile` (`rail_m`, `decks`, `stem_m`, `stern_m`, `wales_m`,
  `breadth_m`, `tiers`) and `ProfileTier` (`deck`, `sill_m`, `half_breadth_m`, `port_m`),
  tuples of float tuples.
- `HullSpec.profile: HullProfile | None = None` (`schema.py:345-356`), a plain default, so
  that a `HullSpec` pickled before it loads with none.
- `_parse_hull` (`:1245-1267`) calls a new `_parse_profile(h.get("profile"), source)`.
  Unlike the hull, the profile is **strict**: `PROFILE_KEYS` and `TIER_KEYS` refuse unknown
  keys, as a gun and a fit do (map-generator §0 item 4; the hull itself drops them silently).
- It refuses, in words:
  - a point that is not two numbers (three in `wales_m` and `breadth_m`);
  - x not increasing where it should;
  - a tier's deck named twice;
  - a sill at or above the rail at its x;
  - a deck at side above the rail;
  - a half-breadth not positive.
- A gun's `deck` (§1.4) must name a tier when the hull has a profile with tiers; refused in
  `validate` beside the gun rules (`:1648-1670`).

### 1.3 The engine's reading (`freesail/ship/profile.py`, new, pure)

`interp(points, x)` (linear, held at the ends), `rail_at(profile, x)`,
`deck_at(profile, x)` (the uppermost deck there), `tier(profile, deck)`,
`sill_at(profile, deck, x)` and `half_breadth_at_sill(profile, deck, x)`.

The generator, the lee port and the tests all read the profile through these, so they agree.
The generator imports them inside its functions, as it imports the engine today
(`tools/gen_ships.py:3629`; Eng §1.2), so its module-level imports stay as they are.

### 1.4 The generator (`tools/gen_ships.py`)

- **`hull_profile(rail, decks, stem, stern, wales, breadth, tiers)`**, a new helper. Its
  arguments are in feet (the sources' unit) where the caller wishes, through `ft()`. It
  returns the profile mapping in the fixed key order of §1.1, metres to the centimetre. Each
  ship function adds it as the last key of its hull dict.
- **Notes.** One note per profile key, from `hull_notes` keyed `"profile.<key>"`, and one per
  tier keyed `"profile.tiers.<deck>"`. `dump` notes only two-space hull keys today
  (`:1072-1074`). A new branch notes the four-space keys inside `  profile:`, and fires only
  on those dotted keys. No existing file has them, so no existing byte moves.
- **One line per point list.** PyYAML lays a nested list out over many lines
  (map-generator §2.7). A second collapsing pass in `dump`, applied **only inside the
  `  profile:` block**, writes each list of number lists as one flow line, like `corners_m`'s
  pass (`:938-950`). A global flow representer would rewrite `arc_deg` and other lists in the
  existing files, so the pass is a regex over the block.
- **Gun heights.** The gun helpers gain `deck=None` and `round_to=0.1`, omitted from the
  mapping when `deck` is None:
  - `broadside_pair` `:3709-3727`;
  - `chasers` `:3730-3746`;
  - `pivot_gun` `:3749-3765`;
  - `swivels` `:3768-3790`.
  
  So the existing calls write the same bytes until SW-2 changes them. SW-2 passes
  `deck=<tier>`, `height_m=sill_at(profile, tier, x)` and `round_to=0.01` for every port gun
  of every fit, and `rail_at(profile, x)` for a swivel's and a pivot's height.
- **`PORT_SILL_M`** (`:3615`, judgement) then has no caller in the existing ships. It stays
  only if a new ship's builder uses it for a tier the sources leave open, and says so.

### 1.5 The sources of each existing file's points

The principle (S2): the profile is above the file's waterline. Where the sources give the
freeboard at load, that freeboard is taken at the file's line, whatever the file's draught.
Each existing file's notes record the difference where one shows.

| File | Rail and decks | Stem and stern | Wale | Half-breadths | Sill(s) | What the builder still reads |
|---|---|---|---|---|---|---|
| frigate-36 (*Amazon*) | Steel 1805, Tables for forming the bodies, "the frigate of 36 guns and 877 tons" (OCR `docs/references/steel/steel-1805-naval-architecture-1822-printing-ocr.txt:27071-27170`: the top-timber and topside lines by station; garbled). Steel's rule: the top-timber line at about a fifth of the length above the keel for ships of two decks and under, the load line at about five-eighths of it in "other ships" (`:15178-15187`, read). The quarterdeck and forecastle from Steel's frigate tables (heights from the plank to the beams) | Folio I's 36: tread of the keel 126 ft 2 in, length extreme 161 ft 9 in, gun deck 137 ft 0 in (read). Winfield p. 143's draught 10 ft 3 in / 15 ft 3 in (*Amazon* as built) | Steel: the wale's lower edge "nearly at the same height as the load-water line", a few inches higher (`:15190-15193`, read) | Steel's bodies table: the main and top-timber half-breadths (OCR; page image) | **Folio I, the 36: the lower ports 7 ft 8 in above the water in midships** at a load draught of 17 ft 4 in / 18 ft 4 in (read, page image). 2.34 m against the file's 2.4 | Steel's bodies table for the 36 from its page image (public domain; the Internet Archive item of the held OCR). Plainly: Steel's 36, not *Amazon*'s own lines (RMG, not reached) |
| brig, merchant-brig (*Harpy*'s hull) | The *Raven* brig's contract of 1804 (Steel 1805, pp. lix ff., OCR `:44331-44390`, read): the waist to the plank-sheer 20 ft afore, 19 ft midships, 22 ft 7½ in abaft above the keel; the deck at the stem 14 ft 7 in, at the post 18 ft 3 in. A brig of 100 ft and 382 tons, sixteen 32-pounder carronades and two 6s, the Diligence class's near successor; scaled to 95 ft (judgement) | The *Raven*'s deck ends and Winfield pp. 255-256's draught 7 ft 3 in / 10 ft 10 in | The *Raven*'s height of breadth, 13 ft 7 in above the keel (read) | The *Raven*'s moulded breadths: 30 ft 0 in; 29 ft 6 in at the top-timber line; 16 ft 9 in at the stern timber (read) | The *Raven*'s sills 16 in above the deck (read). Steel p. 124: "sloops, cutters, &c. from four to five feet" above the water at the lowest place (`:8268-8271`, read). **1.22-1.52 m against the file's 2.1** | The load line the *Raven*'s figures stand on: the contract gives none |
| topsail-schooner, privateer-schooner (*Lynx*'s draught) | Chapelle 1930 fig. 17, the Admiralty's *Musquidobit* draught, reproduced in the held scan (OCR p. 82 at `docs/references/chapelle/chapelle-1930-the-baltimore-clipper-ocr.txt:4820-4830`; the figure read from the scan's plate) | the same | the same | the same | Spider's specification: the sills 3 ft 5 in above the water and 10 in above the deck (Chapelle pp. 166-167; the file's own, `gen_ships.py:4152-4155`) | The plate's sheer and stations, measured |
| cutter (*Sherbourne*) | Steel 1805, "a cutter, on a new construction, of 273 tons" (the page image; the OCR at `:27779-27841` misreads 278: `ships-design/pages-steel-1805-bodies.md`), scaled by length (judgement). The file's hull is the kit manual's (map-generator §3.1) | Fincham 1843 p. 67, the revenue cruiser's draughts (the file's own) | Steel's rule, as the frigate's | Steel's cutter, scaled | Steel p. 124's four to five feet; the file's 1.5 m (4.9 ft) is within it | The cutter's bodies table from its page image; *Sherbourne*'s draught (RMG, not reached) |
| lugger (*Éclair*) | RMG ZAZ6306, "Profile and Plan of the Gun Lugger ... as taken off afloat" (Portsmouth, 2 July 1795; catalogue read by 43b, `docs/design/VesselReferences-2026-10.md:85`) | the same | the same | the same | the same; Steel p. 124's rule failing it | The free 1280-px image (Crown copyright, NMM: read and measured, never copied; `pages-zaz6306.md`), as Neuf and Bel measured theirs |
| smack (*Culloden*) | Chapman 1768 Pl. LIX No. 3, the English smack (read by 43b); Steel 1805, "a coasting sloop of 60 tons" (OCR `:28504-`), scaled | the same | Steel's rule | the same | no guns by default (§5.1) | Chapman's plate image |

**Measured** (`heels2.py`, heel alone, on half the beam):

| File | Sill now | Shut now | Sourced sill | Shut then |
|---|---|---|---|---|
| frigate-36 | 2.4 m | 21.0° | 2.34 m | 20.4° |
| brig | 2.1 m | 24.8° | 1.22-1.52 m | 12.3-16.5° |
| cutter | 1.5 m | 24.4° | 1.5 m | 24.4° |
| privateer-schooner | 1.0 m | 11.0° | 1.04 m | 11.6° |

A narrower side at the sill (the profile's half-breadth) raises each figure a little.

Plainly, for the lead:
- **The frigate's draught.** The file's 15 ft mean draught (judgement, `gen_ships.py:1525`)
  is shallower than Steel's 36's load draught of 17 ft 10 in mean (Folio I, read). The
  profile takes Steel's freeboard at the file's line. Moving her draught would move every
  sailing pin she has, so it is recorded, not moved: an item like the quarterdeck's.
- **The brig's sill.** It falls from 2.1 m to Steel's sloop band. This is the sourced figure
  and the largest move in the existing files. Where in the band it lands is the shared
  builder's measure of the *Raven*'s figures. The brig's deck datum (1.5 m, judgement) then
  stands above her deck at side by the *Raven*'s figures; S5 keeps the datum (§1.6).

### 1.6 D18, proposed against the owner's measure

The owner's measure: "whichever gives the best impression in the viewer and matches the
sources" (Decisions:22). The lead's reading: the viewer draws the true sides from the profile,
and the deck-height convention then serves the physics and the spar heights alone
(Decisions:59).

**Proposed: (a) kept for every file, existing and new.**
- `deck_height_m` stays the uppermost continuous deck at midships.
- **For a new file**, the generator takes the datum from the profile's deck at x = 0, so it
  lies on the drawn deck: the 64's upper deck (3.2 m), the razee's gun deck (1.36-1.42 m),
  the Neufchatel's deck at side at mid-length (1.16 m; Neuf §2.9). The bilander's and the
  74's come from their designs' profiles.
- **For an existing file** the datum stays as it is (the brig's 1.5 m, the frigate's 1.8 m).
  It is read by the physics:
  - the deck's apparent wind (`physics/sails.py:349`);
  - the spar windage height (`:1562`);
  - the hull's wind (`physics/hull.py:391`);
  - the lookout's height of eye (`world/lookout.py:215`);
  - the readings (`api/readings.py:382`).

  So moving it moves pins for no gain in the sources.
- **The viewer** draws the side, the sheer, the decks and the wales from the profile. It
  draws each lower mast down to the drawn deck at its x, its head unchanged, and the
  bowsprit's heel from the stem head, its outer end unchanged (§2). Every spar stays where
  its file puts it relative to the water.

Why not (b) or (c): under (b) the 64's datum falls to her lower deck (0.93 m) and every one of
her heights changes meaning. Under (c) the razee's datum rises to a deck that is not
continuous. With the profile drawn, neither buys anything (a) lacks. The razee's costs under
(a), "her side drawn below her real waist rail" and "her bowsprit rooted at the gun deck"
(Decisions D18), both go with S5's drawing. Judgement; the owner judges by the screenshots
(SW-3).

### 1.7 Files, pins, truths, order

- **Touched:**
  - `freesail/ship/schema.py`;
  - `freesail/ship/profile.py` (new);
  - `tools/gen_ships.py`: `hull_profile`, the dump's branch, the gun helpers, and each
    existing ship function's hull dict and gun calls;
  - the eight files, by regeneration only;
  - `tests/test_ship_particulars.py`;
  - `docs/dev/TuningNotes.md`.
- **Pins.** None move. The heights are read only by the lee port, which comes later (SW-5),
  and the profile only by the viewer (SW-3). The byte-identity test (`:555-581`) passes on the
  regenerated files. `tests/test_server.py:139-160` checks the graph's hull as a superset, so
  an added key stands.
- **New tests** (`tests/test_ship_particulars.py`):
  - every file carries a profile, and its rail stands above its decks and its sills;
  - every port gun's `height_m` equals its tier's sill at its `x_m` within 0.01 m, and names
    a tier;
  - each existing file's sill against its source within a band, with the source in a comment
    (the file's form, `:93-104`).
- **Order:** stage 0's keys, then SW-2. B1 writes the 64's and the razee's profiles with the
  same helper from its first commit.

---

## 2. (b) The viewer draws the hull from the profile

### 2.1 The drawing (`client/projection.js`)

- **`/api/ship`.** `queries.ship_graph` (`freesail/api/queries.py:380-406`) adds
  `hull["profile"]`, the spec's profile as plain lists, when the spec has one.
- **`hullFigures(hull)`** (`:1416-1448`) keeps today's lens for a graph with no profile, so a
  hand-written file and the tests' fixtures draw as now. With a profile it calls a new
  `profileHullFigures(hull)`:
  - **Stations.** The union of the x's of `rail_m` and `breadth_m`, with a grid of sixteen
    between the taffrail and the stem head. At each station: the rail's z, the half-breadths
    at the rail and at the water (`breadth_m`), and the low edge at −0.8 m at 0.92 of the
    water's half-breadth, today's cut ("the sea covers the rest", `:1413-1415`; the cut at `:1432-1433`).
  - **Sides** (`part: side`, starboard and larboard): along the rail from the taffrail to the
    stem head, down `stem_m` to the cut, back along the cut, and up `stern_m` to the taffrail.
  - **Decks** (`part: deck`): one polygon per entry of `decks`, at its own heights and over
    its own extent, at 0.95 of the rail's half-breadth (judgement: inside the bulwark). The
    razee's open waist shows her gun deck below the gangways.
  - **Transom** (`part: transom`): from the taffrail at the rail's half-breadth there, down to
    the counter's knuckle (`stern_m`'s second point from the top).
  - **Wales** (`part: wale`): a band on each side between the wale's edges. Its y is
    interpolated between the water's and the rail's half-breadths by height; it is sorted a
    hair nearer than its side (`sortAt`), so it is never hidden behind its own side at a
    depth tie (`DEPTH_TIE`, `:1529`).
  - **Port bands** (`part: band`, judgement and optional): each tier's strake from the sill to
    the port's depth above it, the strake 81's ports will open in. It is drawn only if the
    owner's screenshot check keeps it. Plainly: the ports themselves are 81's (Decisions:69),
    and this draws no port.
- **The lower masts** (`:501-511`): with a profile, the foot is drawn at
  `deck_at(profile, x)` along the mast's rake line, `r.xAt` unchanged; the head is unchanged.
- **The bowsprit** (`:528-533`): with a profile, the heel is drawn at the stem head
  (`stem_m`'s top point, or the rail at its x if lower). The outer end stays at
  `deck + height_m`, so `dz` becomes `deck + H − heelZ`. The jib-boom roots at its tip, as
  now.
- **Unchanged.** `fullRigFrame` (`:1383-1414`) already includes the hull's points, so the
  fixed scale takes the profile without a change. Every other spar, sail and line, and the
  physics, are untouched.

### 2.2 The rendering (`client/shipview.js`, `client/style.css`)

- `render` draws each hull figure as a polygon with the class `"hull " + part`
  (`shipview.js:58-60`), so `wale` and `band` need no new code there.
- `style.css` (`:155-158`) gains `.hull.wale` (the darker `--hull-far`) and `.hull.band`.
  An SVG polygon with no fill rule is filled black, so both rules are needed.
- The title text names the parts ("hull wale (starboard side)").

### 2.3 Tests, pictures, pins

- **New** (`tests/test_view_geometry.py`, under Node):
  - the side's top edge passes through every `rail_m` point within a millimetre;
  - the transom's top is the taffrail;
  - each deck stands at its own points;
  - a lower mast's foot lies on the drawn deck, and its head is unmoved;
  - the bowsprit's heel is at the stem head and its tip is unmoved;
  - a graph without a profile draws the same figures as before, compared point by point
    with today's lens;
  - every one of the files draws a closed side with no NaN.
- **Standing:**
  - the fixed frame's equality across states (`:181-203`, `:620-658`);
  - the cutter's hull ends, which read the graph's figures, not the drawing (`:445-478`);
  - a yard at its hoist (`:630`);
  - the lowered lug (`:778-781`).
- **The pictures.** The thresholds (`tests/test_pictures.py:57-59`: `BLANK_STD` 8.0,
  `DARK_LEVEL` 110, `DARK_FRACTION` 0.001) test that a picture is not blank. A taller hull
  only adds dark pixels (the side #4a3d31, mean 61; map-engine §5.4), so none is expected to
  move. The builder measures the frigate's picture before and after with
  `FREESAIL_KEEP_PICTURES` (`:186-189`) and records the std and the dark fraction old
  beside new. A threshold re-pins only if one fails, and then old beside new.
- **Screenshots.** The owner's measure for D18. All eight existing ships and the razee, from
  the beam to leeward, the quarter and ahead, furled and under plain sail, at 800 × 600 in the
  built-in pane, beside the same views at the head (Eng §6.2's standard).
- **Order:** after SW-2 and B1 (the razee is the hard case: her open waist and her bowsprit),
  before the owner's check; 81 starts from it.

---

## 3. (c) The lee ports wired, with sourced sills, for every ship

### 3.1 The rule

For a gun whose `place` is `broadside`, `bow` or `stern` (`PORT_PLACES`; a pivot and a rail gun
fire over the rail: `docs/design/Proposal-PivotGun.md` §4.4):

- **The dip**, degrees: the heel toward the gun's side plus the roll's amplitude, never below
  nought. The side the ship heels toward follows `_is_lee` (`combat/guns.py:1032-1040`); the
  other side's dip is the roll less the heel.
- **The sill lowered:** `gun.height_m` (the profile's sill at its x, S3) less the side's
  half-breadth at the sill times the sine of the dip. The half-breadth is
  `half_breadth_at_sill(profile, gun.deck, gun.x_m)`, held once per gun; with no profile it
  is the beam over two, today's `Firer.half_beam_m` (`combat/action.py:221`).
- **Shut** when the sill lowered is `PORT_SHUT_M` (0.3048 m, `combat/shot.py:65`) or less:
  `shot.lee_port_shut(sill, dip, half_breadth)` exactly (`:116-120`), whose `abs` takes the
  dip.
- **Opened again** when the sill lowered stands `PORT_REOPEN_M` = 0.15 m (six inches;
  judgement) above that.

Plainly: the owner's rule speaks of the lee port. The weather side is covered by the same
arithmetic, with its dip the roll less the heel. That shuts a weather port only when the roll
exceeds the heel by the port's whole margin, the *Droits de l'Homme*'s case of heavy rolling
on a low tier (Bel §6.1 item 1). On today's files it needs a roll of 20° and more beyond the
heel, so it moves nothing; it is said for the lead.

**The roll is each ship's own.**
- `Firer.roll_deg` is read from `world.motion` (`action.py:218`). That name is a field the
  Hull keeps (`world/hulls.py:52`, `PER_SHIP_FIELDS`), so the rule needs no change for 84.
- A crewed ship's World keeps no sea (`world/crews.py:312-330`, `sea=False`), so her roll is
  nought until 84 gives every hull its own sea (Design-OneWorld §1.3 item 24, `:346-349`).
  The player's ship rolls with the sea when the scenario keeps one (`core/world.py:643-656`).
- A truth on the roll uses the player's ship.

### 3.2 Where it is wired (`freesail/combat/ports.py`, new; `combat/guns.py`)

- **`ports.update(battery, firer) -> (shut, opened)`**, once a tick at the head of
  `Battery.tick` (`guns.py:446`). It recomputes each port gun's state against the rule's two
  lines and keeps the set in `Battery._shut`. That is a frozenset of gun ids, a class-level
  default, so a battery pickled before it loads with none shut.
- **`wants_work`** (`:331-340`): a shut gun is not wanted run out. A gun run out when its port
  shuts is run in at once (judgement: the lid lowered with the gun housed). Loading goes on;
  a loaded gun stays loaded.
- **`_fire`** (`:773-829`): the single guns (`:788-793`) and the `ready` list (`:803-810`)
  leave out a shut gun. A gun asked for by name whose port is shut is dropped with a line:
  "The No. 3 larboard gun's port is shut; the sea is at its sill."
- **The log.** Once a change of state per tier and side: `guns.ports_shut` ("The lee
  lower-deck ports are shut, the sea at their sills") and `guns.ports_opened`. The words
  name the tier by its `deck`; the event kinds are registered as 70's are.
- **The guns' reading** gains "ports shut" while any are.
- **The far fight** (`combat/far.py:97-121`) is untouched: a far ship has no heel. Plainly:
  rule 5 ("the far ships fight as the near do, coarsely") is kept by its coarseness; 74
  owns the far fight.
- **Pace.** A sine and a compare per port gun a tick (the 74's 74 guns): a per-tick path, so
  truth 51 and the crewed floor are measured after L2.

### 3.3 Steps, pins and the bisection

| Step | Change | Pins expected |
|---|---|---|
| L1 (= SW-2) | The sourced sills and the profile in every file | none: no reader yet |
| L2 | `ports.update` and the gate, on heel alone (the roll term held at nought) | any action whose firing ship heels past her new threshold with that side engaged |
| L3 | The roll's amplitude added | any action with a sea, on the player's ship |

- **The candidates**, run at the commit before L2, at L2 and at L3:
  - truths 7-133 onward (the first action and the frigate's actions);
  - 7-161 to 7-171 (86's practice and resupply);
  - the privateer schooner's truths (`tests/test_known_truths.py:9176` on);
  - `tests/test_pivot_gun.py`, `test_practice*.py`, `test_magazine.py`, `test_ordnance.py`.
- **What the measures say.** The most heel while firing in the first action was 2.7° (the
  cutter) and 6.2° (the *Renard*), and the frigate's on the gate's day 4.0° (Bel §6.1 P6,
  observed). That is below every new threshold but the privateer's (11.6°) and perhaps the
  brig's (12-16°). So the movers, if any, are expected in the privateer's and the brig's
  actions, and under L3 in a sea (judgement).
- **For each moved pin**, the tuning notes give:
  - the old figure beside the new;
  - the reason;
  - **the bisection:** the commit that moves it (L2 or L3); then, within L2, the same run
    with the gate on and the file's old heights (a scratch copy of the file, never
    committed). That separates "the gate" from "the sourced sill".
- **The pace tests** run after L2.

### 3.4 Truths it takes

- **The shared lee-port truth** (§10, 7-186): on every armed file, the lowest lee port of the
  default fit, set at its threshold's heel less half a degree, is open, and a degree later
  shut. The state is pinned, not the angle's digits (the owner's machine gives other digits).
  With a roll set on the World's motion, the threshold falls by the roll. The frigate's lee
  ports stay open at the 74's shut heel (Bel §6.1 P5).
- **The 74's own truth** ("the lower ports shut at the heel the sources give": 5 ft 2 in on
  22.7 ft, 10.6°; Bel §13.2) is the 74's, on this rule.

---

## 4. (d) The sub-types as fits and roles

### 4.1 What a sub-type is

A sub-type is a description, which already names a file (`world/ships.py:163-204`). It gains
two optional keys:
- `fit`: the fit a far ship of it carries when the scenario names none;
- `roles`: the roles a scenario may give her, the first the one the intent rules give.

A scenario's far ship may say `role:`; it must be one of her description's `roles` and of
`ROLES` (`world/captains.py:133-141`), or the load refuses it in words. "In their reasonable
degrees" is that bound: the fit among her file's fits (and `unarmed`), the role among her
description's roles, the nation, colours and intent as now.

- **Wiring.**
  - `Vessel.role: str = ""` (a plain default), read at `vessel_from_spec`
    (`world/ships.py:1126-1190`; `fit` at `:1184` takes the description's `fit` when the
    scenario names none).
  - `brains.role_of_vessel` (`world/brains.py:152-177`) returns `vessel.role` first.
    `FarCaptain` already takes a role (`:245`).
  - The crewed captain's `role_for` (`world/captains.py:914-926`) takes the vessel's role
    first where the crewed World is made.
  - The generator stays the one place a fit is written (the brief item 4). A test proves
    every description's `fit` is a fit of its file.

### 4.2 The table

| Sub-type (description) | File | Fit (default) | Roles | New |
|---|---|---|---|---|
| frigate | frigate-36 | amazon class 1795 | kings-ship, commodore | keys only |
| brig-sloop | brig | diligence class 1796 | cruiser, kings-ship, commodore | keys only |
| merchant brig | brig today; merchant-brig proposed (§4.4) | merchant | merchant, packet, indiaman | §4.4 |
| packet | merchant-brig | packet (new fit) | packet | description, fit |
| schooner | topsail-schooner | unarmed (§5.1) | merchant | keys |
| privateer schooner | privateer-schooner | long tom | privateer | keys |
| cutter | cutter | carronades | cruiser, kings-ship | keys |
| revenue cutter | cutter | long guns | revenue | description, **role** |
| hired armed cutter | cutter | long guns | cruiser | description |
| coasting cutter | cutter | unarmed | merchant | description |
| lugger | lugger | unarmed | fisherman, merchant | keys |
| privateer lugger | lugger | gun lugger 1795 (§5.1) | privateer | description |
| smack | smack | unarmed | fisherman | keys |
| armed Indiaman | none in 75 (§4.3) | | indiaman | **role** |

The new ships' descriptions, ranks and words are their own designs' (D15, D16).

- **The words.** The lookout's words (`_DESCRIPTION_WORDS`, `:205-242`) gain "a revenue
  cutter", "a hired cutter", "a packet" and "a privateer lugger". "revenue" is already a
  man-of-war word (`captains.py:190-198`), so a privateer keeps away from a revenue cutter
  made out.
- **The packet.** A Post Office packet as a role exists (`data/captains/packet.yaml`, a
  letter's intent). The packet fit on the merchant brig is judgement (a few long 6s). Plainly:
  the merchant brig's company of 16 is short of a packet's (from memory, about 28,
  UNVERIFIED). A fit cannot change a complement (`FIT_KEYS`, `schema.py:215-223`), so the
  packet's own hull is a later file, and the lead may prefer to leave the packet's description
  until then.

### 4.3 The two new roles and their doctrine files

**`indiaman`** (`data/captains/indiaman.yaml`), the merchant's book with the action's figures
of a ship that fights when brought to.
- **Thresholds**, all judgement against the merchant's (`data/captains/merchant.yaml`):
  - `yields_when_caught` false;
  - `engage_nm` 1.0;
  - `engage_range_cables` 4;
  - `morale_start` 0.65;
  - `strike_below` 0.25;
  - `engage_side` weather;
  - `board_odds` 0.
- **The accounts:**
  - Commodore Dance's China fleet held its line against Linois's squadron, February 1804
    (James vol. 3 pp. 249-251, the held OCR, `:13621-13770`);
  - the *Windham*, *Ceylon* and *Astell*, July 1810, fought two French frigates
    (vol. 5, OCR `:3445-3506`).
- The brief's intent is "an Indiaman is not a merchantman who strikes at the first telling
  broadside".
- **Plainly:** no Indiaman hull is in this package. Steel 1805 holds the bodies of East India
  ships of 800, 1,000 and 1,257 tons (OCR `:27842-28075`), a later ship's sources. The role
  is built and proven on the merchant brig's hull (§10, 7-187), and the description waits for
  her file.

**`revenue`** (`data/captains/revenue.yaml`), the cruiser's book (`cruiser.yaml`) with:
- every lugger, smack and coaster within reach investigated and spoken;
- a privateer of her size engaged;
- a man of war hauled off from;
- no station kept on a blockade.

Thresholds judgement. Plainly: the smuggler and the search are not modelled (no "search"
order exists), so the role's difference from the cruiser is whom she speaks. Fincham 1843
p. 67's revenue cruisers are the file's hull, not her doctrine.

**`ROLES`** gains both names. The test that runs every doctrine book on the four ships
(`tests/test_captains.py:111`) must pass them.

### 4.4 Found on the way: the merchant brig sails the brig-sloop's guns

`DESCRIPTIONS["merchant brig"]` names `data/ships/brig.yaml` (`world/ships.py:187-191`; "one
file, two descriptions", spec M5 §25), and that file has one fit, sixteen 32-pounder
carronades and two 6s with 121 men (map-generator §3.1). So every far merchant brig of the
trade and the convoys carries the brig-sloop's broadside in the far fight
(`far.far_ship`, `combat/far.py:97-121`, the default fit) and musters 121 when crewed. The
cutter is the same: a trader described "cutter" carries the King's carronades. 70 noted the
lookout's half of it.

**Proposed, for the lead's ruling before it is built:**
- the index's "merchant brig" sails `merchant-brig.yaml` (the same hull and rig byte for
  byte, `brig(merchant=True)`, so the same polar), her own company of 16 and her four 6s.
  Her file already carries the description's words (`gen_ships.py:6694-6704`), so the
  brig's own pair (`:6614-6632`) can stay as it is;
- `SHADOW_FILES`' one entry (`world/ships.py:283`, the player's merchant brig) becomes
  redundant;
- a trader cutter takes "coasting cutter".

It moves every pin with a far or crewed merchant brig (the convoys, the trade trials), and
`tests/test_ships.py:103` asserts the shared file. Each moved pin is shown old beside new,
bisected on its one commit. Plainly: it is outside the five ships, but it is what "the
sub-types as fits and roles" means for the merchant ship; if the lead rules it out, the table
of §4.2 keeps "merchant brig" on `brig.yaml` and the fault is recorded.

### 4.5 Files, pins, truths, order

- **Touched:**
  - `world/ships.py`: `DESCRIPTIONS`, the words, `Vessel`, `vessel_from_spec`;
  - `world/brains.py`;
  - `world/captains.py`: `ROLES`, `role_for`;
  - `world/scenarios.py`: the `role:` key;
  - `data/captains/indiaman.yaml`, `revenue.yaml`;
  - `tools/gen_ships.py`: the packet fit;
  - `tests/test_ships.py`, `test_captains.py`, `test_known_truths.py`.
- **Pins:** none until a scenario names a role or a new description (none does), except §4.4
  if ruled in.
- **Truth:** 7-187 (§10).
- **Order:** SW-4, after stage 0, before the scenarios.

---

## 5. (e) Every file's armament, quarter bill and marines

### 5.1 The schooner, the lugger and the smack: fits and bills

The schema refuses a fit with no guns (`schema.py:855-857`), so "unarmed" cannot be a fit. A
reserved default does it (S9):
- `armament.default` may be `unarmed`;
- `ArmamentSpec.fit(None)` (`:590-596`) returns None for it, and so does `fit("unarmed")`;
- `Ship.__init__` already builds no guns from None (`ship/graph.py:39-44`);
- `far_ship` already skips a None fit (`combat/far.py:103-108`).

Stage 0 checks every caller of `.fit(`.

| File | Default | Fits (the type's records) | Bill |
|---|---|---|---|
| topsail-schooner | unarmed | "letter of marque": *Lynx*'s six guns and forty men (Chapelle p. 82, read; calibres not given, the long 6s judgement). "musquidobit 1813": eight 18-pounder carronades and two 6s (Winfield p. 335, read; her naval company of 50 is not the file's 40, said in the fit's note) | trimmers by station, helm 1, powder 1, the bill's `filling` left to the reckoning, small arms and boarders as the privateer's (`gen_ships.py:4139-`) |
| lugger | unarmed | "gun lugger 1795": *Éclair* "carrying No. 3 – 1? pounder guns" (ZAZ6306's caption, the calibre's second digit not read; `VesselReferences-2026-10.md:85`). Three guns as her caption says; the calibre waits for the image (judgement until then) | the lugger's stations (`gen_ships.py:7649-`), judgement |
| smack | unarmed | "culloden 1746": two guns (Charnock vol. III p. 274, read by 43b; calibre not given: small long guns, judgement) | judgement for 8 men |

- **Pins:** none. The default is unarmed, so no battery is made (`battery_of`) and no captain
  engages ("a ship with no guns never engages", 70).
- **Kept:** `tests/test_ships.py:146-158` pops the armament and the bill from both files, so
  its claim stands.
- **To measure:** a scenario that beats to quarters in an unarmed schooner now meets the
  file's bill in place of the reckoned defaults (`crew/quarters.py:111-112`). The builder
  runs the schooner's, lugger's and smack's scenarios before and after.

### 5.2 The pivot's arc from its own rig

The arc has been per gun since 86 (`arc_deg`, `schema.py:1033-1056`; `pivot_gun`,
`gen_ships.py:3749-3765`). The privateer schooner's [60, 140] is the owner's ruling of the
day, reasoned (`Proposal-PivotGun.md` §3).

**`pivot_arc_from_rig(b, x_m, margin_deg=5.0)`** (generator) computes the open arc from the
file's own spars, as the Proposal's §4.2 proposes:
- each lower mast's `x_m`;
- the shrouds' channel, abeam of the mast and spreading aft;
- the topmast backstays further aft;
- the stays and bowsprit on the centreline;
- the rail's half-breadth at each obstruction's x, from the profile.

The channel's length and the backstays' place come from Steel 1794 vol. I and Luce 1866 (the
chain plates; the builder cites the pages). The arc and the computation go in the gun's note,
as a spar's rating does.

- **"The Dolphin's and the schooner's arcs sourced"** (brief item 5). The *Dolphin* is HMS
  *Dolphin*, the brigantine of 1836 the owner wants a pivot for (`Proposal-PivotGun.md` §1;
  `docs/playtests/2026-10-25-to-27-owner-playtests-70-72/review-of-the-local-work.md:85`).
  She has no file in 75. Plainly: her arc can be sourced only by this rule, from her own rig
  when her file comes. Her pivot's place is on RMG ZAZ5215 (catalogue only;
  `VesselReferences-2026-10.md:553-556`).
- **The global constant.** `ARC_PIVOT_FROM_DEG` and `ARC_PIVOT_TO_DEG` (`combat/guns.py:140-141`)
  are retired as a file's default: the schema refuses a pivot without `arc_deg`. They stay
  only for a gun pickled before 86 (`pivot_arc`, `:146-152`; `tests/test_pivot_gun.py:192-193`
  keeps proving that).
- **Pins.** If the privateer's computed arc differs from [60, 140],
  `tests/test_pivot_gun.py:184` and every pin of her pivot move, old beside new, bisected on
  the one commit.

### 5.3 The fillers as posts

Plainly: proposed **not taken in 75**, against the brief item 5's "the fillers as posts where
73 or 86 left them as a judgement". The brief's own last paragraph allows it: "77's unless 75
takes them first" (`M7-WorkPackages.md:1649-1653`).

The reasons:
1. Making the gunner's crew and the quarter gunners posts moves every armed ship's muster
   draws and quarters. That was the build's decision 5 (`Build-PracticeAndResupply.md:34`),
   and the lee port's bisection is cleaner without it.
2. The 74's bill by deck rebuilds the divisions, and the fillers belong in that design.
3. 77 owns the gunnery's evolutions, filling among them.

What 75 does instead: each new file's bill writes `filling` by Falconer's rule
(`filling_party`, `gen_ships.py:3665-3669`). The 74's and the razee's wardroom files name the
gunner's crew in their outlines for 77 to make into posts. The lead decides.

### 5.4 The marines and their kit

- **The kit** is the nation's already (`data/nations.yaml:48, 84, 122, 156, 189, 224, 257,
  295`; `Nations.marines_kit_of`, `world/nations.py:149-158`). A file names no kit, so the
  Neufchatel under American colours takes the basic kit, and the 74 and the razee the British
  (map-generator §1.9). Nothing to build.
- **The detachments** are the files' (`crew.stations.marines`):
  - the existing two stay: the frigate 40, the brig 20 (judgement, `gen_ships.py:4484-4488`,
    `:6852-6856`);
  - their notes gain the nearest print: a lieutenant and 50 marines embarked for the 44-gun
    *Doris* in March 1803 (*Naval Chronicle* vol. IX p. 245; Bel §4.4).
  
  Plainly: moving them is the lead's (the owner, 2026-10-28: "the existing files are the
  lead's"). The new ships' detachments are their designs'.

### 5.5 The shared tables the new ships need (byte-safe, stage 0)

- **`LONG_GUN_CWT`** (`gen_ships.py:3577`): 24 → 49.5 (Adye p. 155: the 9 ft 6 in gun of 49 cwt
  2 qr; Eng §1.4, read). The length for each ship is her design's: 52 for 10 ft, 47.5 for 9 ft.
  32 → 55 (Bel §13.1 answer 12: the 9 ft 6 in gun).
- **`CARRONADE_CWT`** (`:3578`): 42 → 22.25 (Adye p. 72: 22 cwt 1 qr).
- **`exercise_allowance(upper_deck_guns, decks=1)`** (`:3656-3662`): a third for two or three
  decks, as its own docstring cites. A second note, `MAGAZINE_NOTES_TWO_DECKS["exercise_charges"]`,
  so that the shared note (`:3694-3700`) is untouched (Eng §2.6).
- **Gun crews by the period sources** for the razee and the 74 (D31(c); Bel §13.1 answer 12)
  are a crew table in their modules. `gun_crew` (`:3591-3596`) stays the existing files'.
- **The caches** of eight (`world/ships.py:266, 297, 423`) go to sixteen (judgement). The
  pace is measured once with the twelve or thirteen files (Eng risk 12).

---

## 6. (f) `privateer-schooner.yaml`: kept beside the *Prince de Neufchatel*

- **Proposed: build beside, not replace.**
  - The owner's answer is on file against making her a fit of `topsail-schooner.yaml`: the
    owner's trade trial found the armed Speedwell made the merchant schooner engage
    (`M7-WorkPackages.md:1641-1644`). S9's unarmed default would answer that trial, but the
    owner's answer stands until the owner changes it.
  - The Neufchatel is another hull: 328 tons and a hermaphrodite rig, rank 2 by D15. Replacing
    the privateer schooner with her would change every scenario that sails "privateer
    schooner" (`convoy-six.yaml`) from a schooner of rank 1 to a brig of rank 2.
- **What 75 gives her:**
  - **her profile** (§1.5, *Lynx*'s plate and Spider's sills);
  - **her arc** from her rig (§5.2);
  - **her fits from the type's records:**
    - "long tom" kept as the owner's loadout, its note citing the type (Chapelle p. 13 on
      sweeps and ports; the long Tom from memory until a page is found, UNVERIFIED as now);
    - "letter of marque" re-cited to *Lynx*'s six guns and forty men (Chapelle p. 82, read).
  - **her PROVISIONAL marks** come off where a figure is now sourced.
- **Her wardroom file.** She keeps none (map-generator §0 item 15). Plainly: a
  `data/people/privateer-schooner.yaml` would bind outlines at runtime where today none bind
  (Eng §1.5), and move her pins, so it is left out unless the lead asks.
- **Pins:** her arc (§5.2) and the swivels' charge (§7).
- **Order:** SW-4.

---

## 7. (g) The magazine's charges by kind: Table No. 29 read

**The table** (the Regulations 1806, 1808 printing, Table No. 29, "A Table shewing the
quantities of Gunpowder to be used with different natures of Ordnance"; page image read; the
OCR's title at `regulations-and-instructions-1808-ocr.txt:27498-27502`). Cylinder powder for
service with one shot, the charge "⅓ the weight of one shot" for guns:

| Guns (pdr) | 42 | 32 | 24 | 18 | 12 | 9 | 6 | 4 | 3 | 2 | 1 | ½ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| One shot | 14 lb | 10 lb 10 oz | 8 lb | 6 lb | 4 lb | 3 lb | 2 lb | 1 lb 5 oz | 1 lb | 10 oz | 5 oz | 2 oz |
| Two shots (¼) | 10 lb 8 oz | 8 lb | 6 lb | 4 lb 8 oz | 3 lb | 2 lb 4 oz | 1 lb 8 oz | 1 lb | 12 oz | 8 oz | 4 oz | 2 oz |

| Carronades (pdr) | 68 | 42 | 32 | 24 | 18 | 12 |
|---|---|---|---|---|---|---|
| Service | 5 lb 10 oz | 3 lb 8 oz | 2 lb 10 oz | 2 lb | 1 lb 8 oz | 1 lb |

The table also gives salutes and scaling: for guns from 3 lb 4 oz (42-pdr) down to 1 oz; for
carronades from 2 lb (68) to 12 oz (12). Carronades have no two-shot charge.

**What it confirms and what it moves.**
- **Confirmed:** a long gun a third and a carronade a twelfth (`CHARGE_SHARE`,
  `ship/parts.py:583`).
- **Moved:** the table rounds down where `charge_lb` (`:596-599`) rounds to the nearest
  ounce. Three charges in the existing files change:
  - the 32-pounder carronade, 2 lb 11 oz → **2 lb 10 oz** (the frigate, the brig);
  - the half-pounder swivel, 4 oz → **2 oz**: the table's "½" gun takes a quarter of its
    shot's weight, not `CHARGE_SHARE`'s half (the cutter's "long guns" fit, both of the
    privateer's fits);
  - the long 32-pounder, 10 lb 11 oz → 10 lb 10 oz (none existing; the 74's).

**The change** (`freesail/ship/parts.py`): `CHARGE_TABLE_LB: dict[tuple[str, float], float]`
holds the table's service charges, by kind and calibre, in pounds. `charge_lb(kind, pounder)`
returns the table's figure, and the share only for a calibre the table lacks (none of the
game's). The swivel is the table's half-pounder. The note `MAGAZINE_NOTES["charges"]`
(`gen_ships.py:3680-3692`) and the parts' comment (`parts.py:573-582`) cite the table in
place of "UNVERIFIED".

**Pins:**
- **The files** (through the generator):
  - the frigate's, brig's, cutter's and privateer's `charges`, and their `powder_barrels`
    where the ceiling moves (`fit_magazine`, `:3618-3653`);
  - the cartridges' counts do not move.
- **The tests:**
  - `tests/test_magazine.py:59` (`("carronade", 32, 2.6875, 160)` → `2.625`, 159);
  - `:61` (`("swivel", 0.5, 0.25, 124)` → `0.125`, 122);
  
  each old beside new, with the reason. `fill_seconds` gives 159.4 and 121.9 against the
  test's ±0.5 (measured).
- **The truths:** 86's 7-161 to 7-171, measured where they pin filled powder, barrels or
  filling times.

**Left out, said:**
- the two-shot charge: a double-shotted round draws one service cartridge, as now
  (`parts.py:761-773`), where the table's charge is a quarter;
- the salute's charge: a blank draws a service cartridge;
- the table's recommendation to restrain double shot after twenty rounds.

Each is a change to the gunnery's cycle, 77's.

**Order:** SW-1, first after stage 0.

---

## 8. (h) The frigate-36's quarterdeck: what correcting it would move

Not corrected (the owner, 2026-10-25). Winfield p. 143's establishment against the fit
(`gen_ships.py:3819-3983`), with the arithmetic by the generator's own rules (measured):

| What | As the fit has it | Corrected |
|---|---|---|
| Quarterdeck | 8 × 32-pdr carronades (pairs 14-17), 2 × 9 (pair 19) | 8 × 9 (four pairs), 6 × 32-pdr carronades (three pairs) |
| Forecastle | 2 × 32-pdr carronades (pair 18), 2 × 9 bow chasers | unchanged |
| Pieces | 40 | 44 |
| Gun numbers | 1-13, 14-17, 18, 19 | renumbered from 14; every quarterdeck gun's id and name moves |
| Gun crews (`gun_crew`) | 176 | 192 (+16: a 9-pdr pair 7, a carronade pair 5) |
| The bill | 44 trimmers "the 264 leave" (the note at `:3945-3947`) | the trimmers and the marines at the carronades re-judged: 192 + 2 + 44 + 40 is more than 264 |
| Cartridges | long 9: 4 guns; 32 carronades: 10 | +474 long 9 (79 a gun), −158 carronade 32 |
| Shot | | +432 9-pdr, −144 32-pdr |
| Powder below | | about +5 barrels (half of ~1,000 lb) |
| Filling party | 10 | 11 |
| Exercise allowance | 6 (26 // 4: the upper deck's guns only, the generator's reading) | 6; 11 only if the quarterdeck's guns are counted |
| Broadside a side | 403 lb | 398 lb |

**The truths that move** are the brief's: 7-133 onward where the frigate fights, and 86's
7-161 to 7-171. With them goes the Indefatigable's truth that compares her broadside's rate
and weight with the frigate's (the brief item 6), which is measured against the fit as it
stands and says so.

**What 75 changes there:** only the quarterdeck tier's sill and the guns' heights from the
profile (SW-2), with the guns as they are. A later correction then changes the guns alone.

---

## 9. (i) The scenarios: one per ship, and what they share

### 9.1 The scenario's nations (stage 0, S13)

`data/nations.yaml` stands at June 1805 (`as_of: 1805-06-01`; the wars at `:315-333`, from
memory). A scenario may carry:

```yaml
nations:
  as_of: 1814-08-21
  wars: [[britain, united-states]]
  letters_of_marque: {united-states: true}
  source: "..."
```

- **The loader** (`world/scenarios.py`) validates the nations' ids as `nation:` is validated
  (`:390-401`).
- **The World** (`core/world.py:703`, `self.nations = load_nations()`) replaces the table's
  wars with the scenario's (each with its `since` and `source`), sets the letters of marque,
  and sets `as_of`.
- **Unchanged:** the pilot's news (`Nations.wars_words`, `world/nations.py:195-`), the ports'
  stance and `declare_war` and `make_peace` (`:176-193`) work on it as they do now.
- **Inert** while no scenario carries the block.

Plainly: the wars' dates are from memory, as the table's are. The builder checks each against
James (held, vol. 1 for 1793-96, vol. 6 for 1812-15) and cites the page.

### 9.2 The four scenarios (each ship's design settles the details)

| Ship | Frame | The other sail | Nations | Open |
|---|---|---|---|---|
| The razee | **D25 open.** Proposed: (c), off the Lizard, 20 April 1796, a fresh south-easterly: the *Virginie* chase with *Amazon* (the frigate-36) and *Concorde* in company (Ind §8.1; Gazette 13887 p. 388; Osler pp. 125-128). The lead's view, and the only frame where two of the game's own ships sailed together. (b), Brest August 1805, borrows one day's weather; (d), the *Droits de l'Homme*, waits for the French 74. The 64 sails it by the drivers' choice of file (D48(a)) | the frigate-36's file under French colours for the *Virginie*; the frigate-36 as *Amazon* | April 1796: Britain at war with France and the Batavian Republic; Spain at peace until October 1796 (memory, to check against James vol. 1) | D25 itself; *Concorde* (a second frigate-36 stands in, judgement) |
| The *Neufchatel* | An American privateer of 1814 in the western Channel, August, a convoy of four under a brig-sloop working up from the Lizard (the plan §3; Neuf §5.1: the Channel and the Irish Sea, August-September 1814, a brig sunk by broadside on 21 August, Niles vol. VIII p. 111) | 72's convoy; the brig-sloop's file | Britain at war with the United States only; France at peace with Britain from the spring of 1814 (memory); American letters of marque | the date; her names American (D39) |
| The bilander | D26: an old survivor out of Poole, coasting Falmouth to Plymouth, a summer forenoon early in 1793-1795, a lugger about | a French privateer lugger (§4.2, "privateer lugger", *Éclair*'s guns); a trader of the business | 1794: Britain at war with France only; Spain and the United Provinces allied (memory) | the lugger's calibre (§5.1) |
| The 74 | Basque Roads, July 1815, the 1815 fit (Bel §8.3; §13.1 answer 15) | the frigate-36's file under French colours for *Méduse* and *Saale*, the brig's for *Épervier* | Britain at war with France (the Hundred Days); the United States at peace (memory) | the stand-ins' names and fits |

**Each scenario:**
- is played by the rules captains at seed 7 with pinned weather, as the first action is
  (`data/scenarios/first-action.yaml:30-48`);
- names its fit;
- is checked by one round trip and its first hour run (§10, 7-188).

**Order:** after its ship's file, SW-4's roles and fits, and stage 0's `nations:` block.

---

## 10. The truths the shared work takes (a proposal for the synthesis)

The package owns 7-185 to 7-199. The last at this head is 7-184
(`tests/test_known_truths.py:10426`). Proposed, four shared, eleven left for the ships:

| # | Claim | Pins (states, counts, bands; never digests) |
|---|---|---|
| 7-185 | The generator reproduces every ship file byte for byte, and every file carries a profile whose sills agree with its guns | the file count; every port gun's height within 0.01 m of its tier's sill; each existing file's sill in its source's band |
| 7-186 | Every armed file's lowest lee port is open half a degree under its shut heel and shut a degree later; a roll set on the motion lowers the heel by itself; the frigate's lee ports stay open at the 74's shut heel | states at those heels, for each file's default fit |
| 7-187 | An armed Indiaman holds her colours through the broadside that brings a merchant brig's down | the merchant brig in the `indiaman` role and in the `merchant` role, under one scripted broadside: struck, not struck |
| 7-188 | Each new scenario loads, round-trips and sails its first hour under its pinned weather | loaded; the round trip's equality; the hour's ticks |

The ships' own: each ship's particulars against her sources within bands; the
Indefatigable's broadside rate and weight against the frigate's; the 74's lower ports at the
sources' heel; the 74's pace (named `..._holds_truth_51s_floor` or marked `pace`, so
`tests/conftest.py:490-500` routes it); the *Neufchatel*'s polar's best point; the settee's.

---

## 11. Stage 0: the interfaces the shared work needs

Each is inert: no file, scenario or path uses it until a builder does. Stage 0 proves it by
the byte-identity test and the suite unmoved.

1. **`freesail/ship/schema.py`:**
   - `HullProfile` and `ProfileTier`;
   - `PROFILE_KEYS` and `TIER_KEYS`;
   - `HullSpec.profile = None`;
   - `_parse_profile`, strict, with the refusals of §1.2.
2. **The gun's deck:**
   - `GUN_KEYS` gains `"deck"` (`schema.py:202-214`);
   - `GunSpec.deck: str | None = None`;
   - `Gun.deck: str | None = None` (`ship/parts.py:470-511`), copied in `from_spec`;
   - the gun-deck-names-a-tier check in `validate`.
3. **Unarmed:** `UNARMED = "unarmed"` as a reserved `armament.default`; `ArmamentSpec.fit`
   returns `FitSpec | None`, and stage 0 checks every caller of `.fit(`.
4. **`freesail/ship/profile.py`** (new, pure, with unit tests): `interp`, `rail_at`, `deck_at`,
   `tier`, `sill_at`, `half_breadth_at_sill`.
5. **`tools/gen_ships.py`:**
   - `hull_profile(...)`;
   - the dump's profile branch: flow lines and `"profile.<key>"` notes;
   - `deck=None` and `round_to=0.1` on `broadside_pair`, `chasers`, `pivot_gun` and
     `swivels`;
   - `pivot_arc_from_rig` as a named stub;
   - `LONG_GUN_CWT[24]`, `[32]`, `CARRONADE_CWT[42]`;
   - `exercise_allowance(upper_deck_guns, decks=1)`;
   - `MAGAZINE_NOTES_TWO_DECKS`.
6. **`freesail/api/queries.py` `ship_graph`:** `hull["profile"]` when present.
7. **`freesail/combat/ports.py`** (new):
   - `PORT_PLACES`, `PORT_REOPEN_M`;
   - `update(battery, firer)` returning nothing shut;
   - `Battery._shut = frozenset()` as a class default;
   - the call at the head of `Battery.tick` and the filters in `wants_work` and `_fire`, all
     reading the empty set.
8. **`freesail/world/ships.py`:**
   - optional `fit` and `roles` on a description;
   - `Vessel.role = ""`;
   - `vessel_from_spec` reads `role:` (validated) and the description's `fit`;
   - `brains.role_of_vessel` and `captains.role_for` take a set role first.
9. **`freesail/world/scenarios.py` and `core/world.py`:** the scenario's `nations:` block,
   parsed and applied.
10. **The caches** at `world/ships.py:266, 297, 423`: `maxsize=16`.
11. **The new files' hooks** (from the other designs, listed so the synthesis sees them
    together):
    - the per-ship modules' entry and their import of the generator's one copy (map-generator
      §1.10);
    - the test's file list (`tests/test_ship_particulars.py:565-574`);
    - the wardroom files;
    - `DESCRIPTIONS`, `SIZE_RANK` and `_SIZE_WORDS` ("ship of the line" before "a ship",
      moving `tests/test_ships.py:101`), `MAN_OF_WAR_WORDS`, and `_MAN_OF_WAR_DESCRIPTIONS`
      (Eng §1.5).

Not stage 0, because they move bytes or pins:
- Table No. 29 (SW-1);
- the profiles and sills (SW-2);
- the drawing (SW-3);
- the roles' doctrine files and `ROLES` (SW-4: `test_captains` runs every book);
- the gate's arithmetic (SW-5).

---

## 12. Pins expected to move

| Step | What moves | How shown |
|---|---|---|
| SW-1 | the frigate's, brig's, cutter's ("long guns") and privateer's `charges` and perhaps `powder_barrels`; `test_magazine.py:59, 61`; 7-161 to 7-171 where they pin powder | old beside new; the one commit |
| SW-2 | the eight files' bytes (profile, heights, `deck`); no behaviour | the suite unmoved but the regenerated files |
| SW-3 | the drawing; the pictures' std and dark fraction (measured, thresholds expected to stand) | old beside new in the tuning notes; screenshots |
| SW-4 | the privateer's arc, if it moves (`test_pivot_gun.py:184` and her pivot's pins); §4.4 only if the lead rules it in (far and crewed merchant brigs; `test_ships.py:103`) | old beside new; bisected on the commit |
| SW-5 L2 | actions heeled past the new thresholds (the privateer at 11.6°, the brig at 12-16°) | old beside new, the reason, bisected L1 → L2 and the gate on the old heights |
| SW-5 L3 | actions in a sea, the player's ship | bisected L2 → L3 |
| Pace | truth 51 and the crewed floor after L2 (a per-tick path) and with sixteen-slot caches | measured |

None of the existing ships' sailing passages moves: no hull figure, spar or sail of an
existing file changes.

---

## 13. Open, for the owner or the lead

1. **D18:** (a) kept, with the sides drawn from the profile, the masts drawn down to the deck
   and the bowsprit from the stem head (§1.6). For the owner's screenshots.
2. **D25:** (c), the Lizard of April 1796, proposed (§9.2); held open by the owner.
3. **The fillers as posts:** proposed left to 77 (§5.3), against the brief item 5's reading.
   The lead's.
4. **The merchant brig's description** sails the brig-sloop's file and guns (§4.4). Proposed
   moved to `merchant-brig.yaml`, with every moved pin; the lead's ruling before it is built.
5. **The frigate's draught** (15 ft mean, judgement) against Steel's 36's load draught of
   17 ft 10 in (Folio I). Recorded, not moved (§1.5).
6. **The brig's sill** falls from 2.1 m to Steel's sloop band (1.22-1.52 m), the biggest move
   among the existing files' sills. Her datum stays (§1.5).
7. **The weather side's ports** under a roll greater than the heel: the rule's arithmetic
   covers them (§3.1); the owner's words name the lee.
8. **The port's reopening margin** (six inches) and a port shutting on a gun run out (run in
   at once): judgement (§3.2).
9. **The armed Indiaman's hull:** none in 75. The role is built and proven on the merchant
   brig; the hull is a later ship (Steel's East India bodies).
10. **The packet:** the merchant brig's 16 against a packet's company (memory, about 28). The
    packet's description may wait for her own hull.
11. **The revenue cutter's guns:** no source in hand; the hired cutters' long guns stand in.
12. **The *Éclair*'s calibre** ("1?") for the lugger's gun fit: ZAZ6306's image, not yet
    fetched.
13. **Pages to read** (public domain, filed with provenance as Phase 1's were, if the owner's
    leave for online reading stands):
    - Steel 1805's bodies tables for the 36-gun frigate, the 273-ton cutter and the 60-ton
      coasting sloop;
    - ZAZ6306;
    - Chapelle's fig. 17;
    - Chapman's Pl. LIX.
14. **The swivel's charge** halves (4 oz → 2 oz) by the table's half-pounder (§7).
15. **The marines** of the frigate and the brig stay as they are (§5.4).
16. **The wars' dates** in the four scenarios' `nations:` blocks are from memory until
    checked against James (§9.1).
17. **The privateer schooner's wardroom file** is left out (§6).

---

## 14. Left out, and why

- **The ports themselves** (81's), the guns drawn, the flash and the smoke.
- **The double shot's and the salute's charges** of Table No. 29 (77's cycle; §7).
- **The far fight's lee ports:** a far ship has no heel (§3.2).
- **The fillers as posts** (§5.3).
- **Sweeps, searching and the smuggler.**
- **The frigate's quarterdeck** (§8).
- **The frigate's draught** (§1.5).
