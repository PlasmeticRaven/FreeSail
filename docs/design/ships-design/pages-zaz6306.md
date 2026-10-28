# Pages: RMG ZAZ6306, the gun lugger *Éclair* as taken off afloat (October 2026)

Stage 0 research for package 75, the page named by `Build-Ships.md` §19.1 item 11 and by the
shared draft (`ships-design/shared-design.md` §1.5, the lugger's row; §5 items 12 and 13). It
serves `data/ships/lugger.yaml` (`ships-design/map-generator.md`, the lugger's rows: `lugger()`
in `tools/gen_ships.py`), and the builder B8, who draws a sourced hull profile for the file
(`Build-Ships.md` §5). The catalogue reading this note builds on is
`docs/design/VesselReferences-2026-10.md:85` and `:258`. Facts only: the image is the museum's
photograph, kept outside the repository (§1.1).

The marks:

- **read**: the sheet's writing or drawing was seen on the image. "tentative" is a reading at
  the limit of the image.
- **catalogue**: from the museum's catalogue entry only.
- **measured**: off the image at the scale of §3; the uncertainty is stated.
- **memory, unverified**: not checked during this research.
- **judgement**: reasoning by this note.

**Units and datums.** English feet and inches, with metres in brackets. Positions along the
ship are feet forward of **AP**, the after of the two perpendiculars drawn on the profile, whose
distance apart is the length on the range of the deck (§3.2); in metres they are given from the
**mid-perpendiculars**, 29.63 ft forward of AP, positive forward, as the profile's `x`. Heights
are above **the drawn waterline** (the green line, §4), positive up, as the profile's `z`. Both
are taken along and across the page (the scale strip is level on the image to 0.2 px); the
green line is tilted 1.05° to the page, which moves no height by more than 0.002 ft and shifts
`x` by at most 0.17 ft at the rail's ends (judgement: ignored).

## 0. In brief

- **The caption's calibre reads "No. 3 – 18 Pounder Guns"** (read, probable): the second
  digit is a closed figure with a waist, an 8, not a 0; a 10-pounder was no calibre of either
  service (judgement). Three 18-pounders (§2.1).
- **The scale checks.** The strip gives 11.231 px to the foot over 60 one-foot divisions (rms
  0.18 px); the two perpendiculars stand 59 ft 3.1 in apart against the caption's 59 ft 3 in on
  the range of the deck, and the sheet's height comes to 325 mm against the catalogue's 324 mm
  at 1:48 (§3).
- **The sheet gives the sheer, the deck and the deck plan, not the body.** Rail, deck and the
  side's lines are measured at stations 2½ ft apart; the plan gives the side's half-breadth at
  the rail or deck end to end. There is no body plan, no half-breadth plan, no keel, no wale
  below the deck and no ports (§5, §8).
- **The draught is not on the sheet.** The keel is not drawn (she was taken off afloat); the
  post and forefoot are dashed below the line and run into the scale strip at least 6.9 ft
  below it aft and 5.9 ft forward (§4).
- **Against the file** (§7, recorded, not moved): the drawn line is 59.3 to 60.3 ft long (18.1
  to 18.4 m) against the file's 55 ft (16.8 m); the deck stands 2 ft 10 in (0.86 m) above it
  at the middle line against the file's 1.0 m; the masts stand 4.4 ft abaft and 25.9 ft before
  the middle against the file's 2.4 ft and 21.6 ft (Forfait's stations).

## 1. The source

### 1.1 The object, the image and the cache

| | |
|---|---|
| Object | RMG ZAZ6306, "Eclair (1795)", technical drawing, Ship Plans and Technical Records, Admiralty Collections; paper, black, red and green ink; sheet 324 x 482 mm; dated 2 July 1795 (catalogue) |
| Object page | https://www.rmg.co.uk/collections/objects/rmgc-object-86097 (found by https://www.rmg.co.uk/collections/search/ZAZ6306; the old address https://collections.rmg.co.uk/collections/objects/86097.html redirects to it) |
| Image used | https://collections.rmg.co.uk/media/413/796/j0576.jpg, 1280 x 587 px, JPEG, 138,733 bytes, sha256 `fcb0ffd5ada4f997de976b19f73b2e3c33f7c2e0831049d5cd413c6dc84d059b`; the largest the page offers |
| Also fetched | https://collections.rmg.co.uk/media/413/796/mid_j0576.jpg, 519 x 238 px (not used) |
| Rights shown | The page's credit line: "© Crown copyright. National Maritime Museum, Greenwich, London", with "Buy a print" and "License an image" and a note to contact RMG Images about using its images. Free to view; reuse is not offered, so the image stays in the cache and this note takes facts only |
| Other copies | None found on Wikimedia Commons (searches for J0576, ZAZ6306 and the vessel's two names, 2026-10-28) |
| Cache | `D:/Projects/FreeSail/reference-cache/zaz6306/j0576/j0576.jpg`; `.../zaz6306/mid_j0576/mid_j0576.jpg`; the object page as fetched, `.../zaz6306/page/object-86097.html` (sha256 `06f66d07...e49ac`). Fetched 2026-10-28 with a generic user-agent |

**What the catalogue says** (catalogue, paraphrased): the sheet is at 1:48 and shows the
vessel's inboard works in profile, with a single waterline, and her whole deck in plan; she is
the *Eclair* of 1795, a lugger of 59 ft and three guns, renamed *Safety* in 1802, measured
while lying afloat at Portsmouth; the dockyard's master shipwright, Robert John Nelson, signed
it. A folder made in conservation at the sheet's left edge holds a document of her scantlings
and dimensions, which has been neither scanned nor catalogued.

### 1.2 What is on the sheet (read)

- **The profile**, bow to the right: the side's outline from the taffrail to the
  stem head, inboard works in red (the deck, beams, pillars, ladder, bulkheads, platforms and the
  hold's floor), one green waterline, the rudder hung on a raked post, the channels and chain
  plates, the stumps of a main and a fore mast and a bowsprit run out over the stem head.
- **The deck plan**, below the strip, to the same scale: the side's outline, a cabin each side
  aft, the ladderway, the galley, the main hatch, the fore hatch, two mast holes, two small
  circles beside the main mast (pumps, judgement) and a Y-shaped fitting on the rudder head.
- **A scale strip** between the two, 60 ft of one-foot divisions with a diagonal scale at each
  end.
- **The writing**: the caption and the vessel's name top left; the title, the yard and date, the
  signature in red and the table of dimensions top right (§2).
- **Not drawn**: no body plan or half-breadth plan; no keel; the post, rudder and forefoot below
  the line only dashed; no wale below the deck; no gun ports or sweep ports; no gun; no mizen
  mast; no draught marks or figures.

## 2. The caption and the dimensions

### 2.1 The calibre

The caption reads "L'Eclair — Carrying No. 3 – 18 Pounder Guns" (read; the calibre's second
digit **probable**). The figure is 6 px high. Read pixel by pixel (`pix.py`, §9) it is closed at
the upper right and down both sides, so not a 2, 3 or 6; its two counters are parted by a
darker waist across the middle, which a 0 does not have and an 8 does. The writer's 0 of
"7 – 0" in the dimensions is an open oval with no waist. JPEG noise at an 8 x 8 block edge
could make a waist, so "10" is not ruled out by the pixels alone; but a 10-pounder
was no calibre of the British or the French service, and the 18-pounder was a calibre of both
(judgement). How sure: **18, probable**; 10 possible only as a slip of the pen.

Where the three guns stood is not drawn: no port, no slide and no carriage appear in the
profile or the plan (read). French gun-vessels of these years carried a few heavy guns firing
over the bow and stern (memory, unverified).

### 2.2 The title and the dimensions, re-read

- **Title** (read): Portsmouth Yard, July 2nd 1795; "Profile and Plan of the Gun Lugger", taken
  by Captain Sir Richard Strachan, "as taken off afloat", followed by a word read tentatively
  as "June"; signed in red by the master shipwright.
- **Dimensions** (read, as `VesselReferences-2026-10.md:85` has them): length on the range of
  the deck 59 ft 3 in; of the keel for tonnage 45 ft 11 in; breadth extreme 20 ft 4 in, moulded
  20 ft 0 in; depth in hold 7 ft 0 in. The mark after each inch figure reads here as the
  abbreviation for feet carried down the column, not ½ (tentative). The burthen's third digit
  and its ninety-fourths are still not settled at this resolution (the rule gives 100 92/94 on
  the figures above).

## 3. The scale and its check

### 3.1 The strip (measured)

- 60 of the strip's 61 one-foot ticks found (the one at 695.5 px is too faint); a straight
  fit of tick against foot over feet 0 to 60 gives **11.2311 px to the foot**, rms 0.18 px,
  largest residual 0.38 px (`ticks.py`, `fitscale.py`). Every fifth tick is longer and
  numbered; the numbers are too small to read and are not needed.
- 1 px is 0.089 ft (1.07 in). The strip is level on the image: its top border lies at 277.0 px,
  ±0.2 px, from end to end.
- **1:48 checked.** At a quarter-inch to the foot, 11.2311 px/ft is 1.769 px/mm; the paper's
  height on the image, 575.5 px, is then 325 mm, against the catalogue's 324 mm (+0.4%).

### 3.2 The stated dimensions measured back

| Dimension | Stated (read) | Measured | Basis |
|---|---|---|---|
| Length on the range of the deck | 59 ft 3 in | **59 ft 3.1 in** (59.26 ft, 18.06 m) | the two perpendiculars: a red vertical at the post and an ink vertical at the stem, both running from the side down to the strip, 665.5 px apart (±0.5 px, ±0.6 in) |
| The same, on the plan | 59 ft 3 in | 59 ft 2.2 in (59.18 ft) | the plan's outline at the middle line, stern to stem (664.7 px) |
| Breadth extreme | 20 ft 4 in | not measurable | the plan's outline is the side at the rail or the deck, 19 ft 7 in outside at its broadest (220.1 px), 9 in less: tumblehome of about 4½ in a side (judgement). No body plan |
| Depth in hold | 7 ft 0 in | 6 ft 4 in from the deck at the middle line to the hold's floor line amidships | the floor line is the top of the keelson if the ceiling at the limbers lies 8 in below it (judgement); a weak check |

The length check holds to the image's resolution; the breadth cannot be checked on this sheet.

## 4. The waterline and the draught

**The line.** The single green line is straight from the rudder to the stem: y = 188.04 +
0.01825 x px, rms 0.33 px over 47 columns (measured, `greenline.py`). It is not labelled. It is
taken as the line she floated at when taken off afloat in July 1795 (catalogue: "one
waterline"); whether she was laden, light or in ballast as a prize is not stated (judgement:
not her sea-going load line for certain).

**Its tilt.** It falls 1.08 ft toward the bow over the 59.25 ft between the perpendiculars
(1.05°) relative to the page and the strip (measured). If the draughtsman drew the keel level,
as draughts were drawn, she floated about 1.1 ft deeper aft than forward against her keel
(judgement; the keel is not drawn).

**The draught is not given.** She was taken off afloat, and nothing below the line is drawn
solid but the hold's inboard works (read). Measured below the line:

| What | ft from AP (m from mid) | Below the line |
|---|---|---|
| The post's after edge, dashed, where it meets the strip | 1.21 (−8.66) | 6.91 ft (2.11 m) |
| The post's fore edge, dashed, at the strip | 2.75 (−8.19) | 6.88 ft (2.10 m) |
| The rudder's after edge, dashed, at the strip | −1.60 (−9.52) | 6.96 ft (2.12 m) |
| The forefoot, dashed, at the strip (still falling at about 18°) | 56.07 (+8.06) | 5.88 ft (1.79 m) |
| The hold's floor line at the middle line, amidships | 29.63 (0.00) | 3.52 ft (1.07 m) |
| The top of the strip | 0 / 59.26 | 7.11 ft / 6.02 ft |

- The dashed lines run into the strip; the keel, if drawn at all, would lie under it. So the
  sheet bounds the draught only from below: **at least 6.9 ft aft and 5.9 ft at the forefoot**
  (measured, ±0.3 ft, as far as the dashed lines are true).
- Judgement: from the floor line amidships (3.5 ft down), with the keelson, floors and keel
  below it (2.5 to 3 ft for a vessel of a hundred tons), a draught of 6 to 6½ ft amidships to the
  keel's lower edge. The file's 7 ft mean, 8 ft 6 in aft and 5 ft 6 in forward (judgement there
  too) is not contradicted; its 3 ft of trim is more than the 1.1 ft the line's tilt suggests.
- The scale used is §3's throughout; the check is the length on the range of the deck (§3.2).
  No stated draught exists to measure back; the scantling document in the conservation folder
  (§1.1) may carry one and was not scanned.

## 5. The profile, measured

### 5.1 The lines of the side (read; identification as marked)

From the top, at the mid-perpendiculars:

- **The rail (A)**, black: the top of the side, 4.92 ft (1.50 m) above the line. It steps: raised
  aft from the taffrail to 15.07 ft from AP (a step of 1.83 ft) and forward from 43.04 ft to the
  stem head (a step of 0.83 ft). The raised after part covers the cabins of the plan, whose
  fore ends stand at about 13.6 to 14.8 ft; the fore step falls on a thwartship line of the
  plan at 42.9 ft (measured).
- **Line B**, black, heavy: 0.59 ft (7 in) below the rail in the waist, from the post (6.80 ft
  above the line at 0.36 ft abaft AP) to near the stem (6.71 ft at 57.2 ft), with no steps
  (measured).
- **Line C**, grey, faint: parallel to B and 0.80 ft (9½ in) below it from the post to the stem
  (5.13 ft at 0.71 ft; 5.73 ft at 55.9 ft); the main and fore channels lie along it (measured).
  Judgement: B to C is a strake band at the top of the side, a sheer strake or rubbing band; it
  is the only band drawn on the side.
- **The deck (D)**, red: the deck at the middle line, an inboard line, 2.83 ft (0.86 m) above
  the line amidships (read: the ladder from the hold ends on it, and the beams in section hang
  under it). Traced from 12.5 to 42.5 ft; aft of about 10 ft it runs into the second red line.
- **Line D2**, pale red: 0.35 to 0.39 ft (4 to 4½ in) below D between 17.5 and 37.5 ft, traced
  from 2.5 to 57.5 ft (measured). Judgement: the deck at side (the beams' round-up) or the
  underside of the deck plank; either way it is the deck at side to within about an inch.
- **Nothing between D2 and the line**: the side below the deck is blank (read).

### 5.2 By station (measured)

Heights in feet above the drawn line. ±0.05 ft for the rail and B, ±0.1 ft for C, D, D2;
the plan's half-breadth ±0.03 ft, its stations ±0.5 ft (the plan is registered to the profile by
its two ends on the perpendiculars, plan x + 4.1 px).

| ft from AP | m from mid | Rail (A) | B | C | Deck, middle line (D) | D2 | Half-breadth of the plan's outline |
|---|---|---|---|---|---|---|---|
| −1.39 | −9.45 | 9.31 (taffrail) | | | | | |
| 0.00 | −9.03 | 8.99 | | | | | 0.00 |
| 2.50 | −8.27 | 8.55 | 6.14 | 5.34 | | 3.84 | 5.34 at 2.59 |
| 5.00 | −7.51 | 8.15 | 5.78 | 4.95 | | 3.67 | 7.24 |
| 7.50 | −6.74 | 7.83 | 5.41 | 4.64 | | 3.52 | 8.37 |
| 10.00 | −5.98 | 7.58 | 5.17 | 4.41 | | 3.24 | 8.95 |
| 12.50 | −5.22 | 7.35 | 4.94 | 4.16 | 3.20 | 3.10 | 9.30 |
| 15.00 | −4.46 | 7.14 | 4.77 | 3.99 | 3.17 | 2.92 | 9.48 |
| 15.07 (step) | −4.44 | 7.14 / 5.31 | | | | | |
| 17.50 | −3.70 | 5.21 | 4.62 | 3.82 | 3.05 | 2.74 | 9.61 |
| 20.00 | −2.93 | 5.09 | 4.48 | 3.68 | 2.96 | 2.58 | 9.70 |
| 22.50 | −2.17 | 4.98 | 4.37 | 3.65 | 2.92 | 2.56 | 9.75 |
| 25.00 | −1.41 | 4.92 | 4.31 | 3.60 | 2.85 | 2.51 | 9.79 |
| 27.50 | −0.65 | 4.89 | 4.34 | 3.52 | 2.83 | 2.47 | 9.79 |
| 29.63 | 0.00 | 4.92 | 4.32 | 3.51 | 2.83 | 2.44 | 9.79 |
| 32.50 | +0.88 | 5.00 | 4.37 | 3.61 | 2.84 | 2.46 | 9.79 |
| 35.00 | +1.64 | 5.02 | 4.47 | 3.67 | 2.87 | 2.51 | 9.76 |
| 37.50 | +2.40 | 5.15 | 4.57 | 3.74 | 2.94 | 2.55 | 9.76 |
| 40.00 | +3.16 | 5.29 | 4.69 | 3.94 | 2.99 | 2.66 | 9.77 |
| 42.50 | +3.92 | 5.43 | 4.84 | 4.07 | 3.02 | 2.76 | 9.76 |
| 43.04 (step) | +4.09 | 5.53 / 6.36 | | | | | |
| 45.00 | +4.69 | 6.50 | 5.03 | 4.25 | | 2.91 | 9.74 |
| 47.50 | +5.45 | 6.73 | 5.31 | 4.54 | | 3.17 | 9.53 |
| 50.00 | +6.21 | 7.03 | 5.57 | 4.82 | | 3.54 | 9.08 |
| 52.50 | +6.97 | 7.38 | 5.98 | 5.16 | | 3.75 | 8.18 |
| 55.00 | +7.73 | 7.84 | 6.41 | 5.63 | | 3.96 | 6.78 |
| 57.50 | +8.50 | 8.53 | | | | 4.20 | 4.45 |
| 59.26 | +9.03 | 9.29 (stem head) | | | | | 0.00 at 59.22 |

- **The sheer** of the rail: lowest at 27.5 ft (4.89 ft), rising 4.4 ft to the taffrail and
  4.4 ft to the stem head; of the deck at the middle line, lowest amidships (2.83 ft), rising
  0.4 ft by 12.5 ft aft and 0.2 ft by 42.5 ft forward; of D2, 1.4 ft aft and 1.8 ft forward at
  2.5 and 57.5 ft.
- **The bulwark** above the deck (rail less D2): 2.5 ft in the waist, 4.2 to 4.7 ft aft over
  the cabins, 3.5 to 4.3 ft forward (measured, judgement on D2 as the deck at side).
- **The plan's ends** (measured by rows): aft, half-breadths of 0.89, 1.78, 2.67, 3.56 and 4.45
  ft at 0.03, 0.26, 0.62, 1.12 and 1.97 ft from AP; forward, the same half-breadths at 59.12,
  59.06, 58.65, 58.14 and 57.50 ft. Both ends are round in plan at the rail or deck: a round
  stern and a full bow (read).
- **The plan's inner line**, 0.45 ft (5½ in) inside the outline (18.71 ft across amidships):
  the inside of the side at the rail (judgement).

### 5.3 The ends (measured)

- **Taffrail**: the rail's after end, 9.31 ft (2.84 m) above the line, 1.39 ft (0.42 m) abaft AP;
  the post's head, shaded, stands under it.
- **The post**: its after edge from the taffrail to the line at 0.13 ft abaft AP, a rake of 7.7°
  to the page (8.7° to the line); below the line, dashed, raking about 11° and broadening to
  1.5 ft at the strip (§4).
- **The rudder**: hung outside the post on two braces, its after edge 2.07 ft abaft AP at the
  line; its blade 1.9 ft broad at the line and 2.8 ft at the strip; its head about 5.8 ft above
  the line. On its head a Y-shaped fitting with two arms reaching 2¼ ft out to either side and
  2 to 3 ft abaft, sloping down, ending in rings (a yoke for steering lines, judgement; or the
  guys of a mizen outrigger, which is not otherwise drawn).
- **The stem**: plumb. Its fore edge stands 0.93 ft (11 in) before FP from the line up to about
  7.9 ft (measured, a faint line); the head is at FP, 9.29 to 9.38 ft (2.83 to 2.86 m) above
  the line, with a shaded timber (the stem head or knighthead) and a rounded fitting at the
  bowsprit (the collar for the running bowsprit, judgement). Below the line, the dashed
  forefoot sweeps aft from the fore edge: 2.72 ft down at 59.63 ft, 3.62 at 59.18, 4.34 at
  58.59, 4.98 at 57.96, 5.53 at 57.07, 5.88 at 56.07 ft (measured, tentative, ±0.2 ft).
- **The bowsprit**: its upper edge crosses the stem head 9.17 ft (2.79 m) above the line, 4.8 to
  5.0 ft (1.47 to 1.51 m) above D2 near the stem; steeved 5.5° to the page (6.6° to the line);
  it runs off the drawing's frame 6.4 ft before FP, so its length outboard is not given.

### 5.4 Ports, sweeps and the uprights on the rail

- **No port** is drawn in the side, the waist or the raised ends, and none in the plan (read).
  The sill a profile wants has no source on this sheet; the lowest place a gun could fire over
  is the waist rail, 4.9 to 5.4 ft (1.49 to 1.66 m) above the line (measured; judgement that
  the guns fired over it). Steel's four to five feet for the ports of sloops and cutters
  (`Build-Ships.md` §5.4) is close to it.
- **Uprights** stand on the rail about 0.7 ft (8 in) high, about 0.4 ft broad (measured): in
  the waist at 19.6, 22.7, 25.9, 29.0, 32.4, 35.3, 38.6 and 41.6 ft from AP, 3.1 to 3.4 ft
  apart; aft at about 0.5, 2.8, 4.6, 6.7, 9.7, 11.3 and 14.7 ft; forward at 46.3 and 49.9 ft.
  Thole pins for sweeps or timberheads for belaying (judgement; the even 3.2-ft spacing of
  the waist suits a rowing room). No sweep port is cut in the side.

### 5.5 The deck plan and the masts

Stations from AP in the profile's frame (the plan registered as in §5.2, ±0.5 ft):

| Item | ft from AP | m from mid | Basis |
|---|---|---|---|
| Cabins, either side | 2.8 to 14.8 | −8.18 to −4.52 | read ("Cabin"), measured |
| Ladderway | 16.8 to 19.8 | −3.91 to −3.00 | read, measured |
| Main mast hole | **25.24** (circle 1.4 ft across) | **−1.34** | measured; the profile's stump meets the deck at 24.25 ft (−1.64 m) |
| Galley | 26.0 to 28.0 | −1.10 to −0.50 | read, measured |
| Main hatch | 28.2 to 32.9 | −0.44 to +1.00 | read, measured |
| Fore hatch | 45.9 to 49.4 | +4.96 to +6.03 | read, measured |
| Fore mast hole | **55.56** (circle 1.4 ft across), 3.7 ft abaft FP | **+7.90** | measured; the profile's stump at 54.56 ft (+7.60 m) |
| Mizen mast | not drawn | | read |

- The masts are drawn in the profile only as single stumps above the rail, raking 7.5° (main)
  and 1.8° (fore) to the page, 8.6° and 2.8° to the line (measured). They stand about 1 ft
  abaft the plan's holes; the plan's holes are taken as the stations (judgement: the plan is
  registered by its ends on the perpendiculars, the stumps are sketched).
- The fore mast 3.7 ft abaft FP fits Willaumez 1831 pp. 145 to 146 on the chasse-marée, the
  fore mast two or three feet abaft the stem head, and the main mast near the middle, much
  raked (`VesselReferences-2026-10.md:244-247`, read there).

## 6. For the profile (B8): the points in metres

`x` forward of the mid-perpendiculars, `z` above the drawn line, both in metres; from §5
(measured unless marked). Where the schema wants x increasing, the two steps are given 0.01 m
apart.

- **`rail_m`**: [−9.45, 2.84], [−9.03, 2.74], [−8.27, 2.60], [−7.51, 2.48], [−6.74, 2.39],
  [−5.98, 2.31], [−5.22, 2.24], [−4.44, 2.18], [−4.43, 1.62], [−3.70, 1.59], [−2.93, 1.55],
  [−2.17, 1.52], [−1.41, 1.50], [−0.65, 1.49], [0.00, 1.50], [0.88, 1.52], [1.64, 1.53],
  [2.40, 1.57], [3.16, 1.61], [3.92, 1.66], [4.09, 1.69], [4.10, 1.94], [4.69, 1.98], [5.45, 2.05],
  [6.21, 2.14], [6.97, 2.25], [7.73, 2.39], [8.50, 2.60], [9.03, 2.83].
- **`breadth_m`**, the rail's half-breadth only (the plan's outline; whether it is the rail or
  the deck is judgement): [−9.03, 0.00], [−9.02, 0.27], [−8.95, 0.54], [−8.84, 0.81],
  [−8.69, 1.09], [−8.43, 1.36], [−8.24, 1.63], [−7.51, 2.21], [−6.74, 2.55], [−5.98, 2.73],
  [−5.22, 2.83], [−4.46, 2.89], [−2.93, 2.96], [−1.41, 2.98], [0.00, 2.98], [1.64, 2.97],
  [3.16, 2.98], [4.69, 2.97], [5.45, 2.90], [6.21, 2.77], [6.97, 2.49], [7.73, 2.07], [8.26, 1.63],
  [8.50, 1.36], [8.69, 1.09], [8.85, 0.81], [8.97, 0.54], [8.99, 0.27], [9.01, 0.00]. **The
  half-breadth at the water is not on the sheet**: the caption's extreme breadth gives 3.10 m
  (10 ft 2 in) at most; the shape of the waterline at the ends is judgement.
- **`decks_m.upper`** (the deck at side): D2, judgement (§5.1): [−8.27, 1.17], [−7.51, 1.12],
  [−6.74, 1.07], [−5.98, 0.99], [−5.22, 0.94], [−4.46, 0.89], [−3.70, 0.83], [−2.93, 0.79],
  [−2.17, 0.78], [−1.41, 0.76], [−0.65, 0.75], [0.00, 0.74], [0.88, 0.75], [1.64, 0.76],
  [2.40, 0.78], [3.16, 0.81], [3.92, 0.84], [4.69, 0.89], [5.45, 0.97], [6.21, 1.08], [6.97, 1.14],
  [7.73, 1.21], [8.50, 1.28]. The deck at the middle line (D) stands 0.11 to 0.12 m higher
  amidships: [−4.46, 0.97] to [3.92, 0.92], 0.86 at 0.00.
- **`stem_m`**, the fore edge, low to high: [8.06, −1.79], [8.37, −1.69], [8.64, −1.52],
  [8.83, −1.32], [9.01, −1.10], [9.14, −0.83] (dashed, tentative); [9.32, 0.00], [9.32, 2.40]
  (measured); the head [9.04, 2.86].
- **`stern_m`**, the post's after edge, low to high: [−8.66, −2.11] (dashed, at the strip),
  [−9.07, 0.00], [−9.45, 2.84] (the taffrail). No counter: the post rises straight to the
  taffrail.
- **`wales_m`**: no wale is drawn below the deck. The only band on the side is B to C
  (judgement): lower edge C, upper edge B, at x −8.27: 1.63 / 1.87; −5.98: 1.34 / 1.58;
  −2.93: 1.12 / 1.36; 0.00: 1.07 / 1.32; 3.16: 1.20 / 1.43; 6.21: 1.47 / 1.70; 7.73: 1.72 / 1.95.
- **`keel_m`, `section_m`, `ports_m`, `port_size_m`**: not on the sheet (§8).

## 7. Against `data/ships/lugger.yaml` (recorded, not moved)

| Field | The file (its note) | The sheet |
|---|---|---|
| `length_waterline_m` | 16.8 (55 ft, judgement between keel and deck) | 18.4 m (60.3 ft) from the post to the stem's fore edge on the drawn line; 18.06 m between the perpendiculars (measured) |
| `beam_m` | 6.2 (20 ft 4 in extreme) | the extreme breadth is not drawn; 5.97 m (19 ft 7 in) outside at the rail or deck (measured) |
| `draught_m` | 2.1 (7 ft mean, 8 ft 6 in aft, 5 ft 6 in forward; judgement) | not given; at least 2.1 m aft and 1.8 m at the forefoot (§4); 1.8 to 2.0 m amidships (judgement) |
| `deck_height_m` | 1.0 (3 ft 3 in, judgement) | 0.86 m at the middle line, 0.74 m at side (D2) amidships (measured) |
| `fore.mast` `x_m`, `rake_deg` | 6.6 (21.6 ft before the middle, Forfait); 1.6 | +7.90 (the plan's hole); 1.8 to the page, 2.8 to the line |
| `main.mast` `x_m`, `rake_deg` | −0.7 (2.4 ft abaft, Forfait); 4.8 | −1.34 (the plan's hole); 7.5 to the page, 8.6 to the line |
| `mizen.mast` `x_m` | −8.7 (Forfait) | not drawn |
| `bowsprit` `height_m` | 1.5 | 1.47 to 1.51 m above D2 near the stem (measured) |
| The gun fit "gun lugger 1795" (`Build-Ships.md` §9.1) | three guns, calibre unread | three 18-pounders (read, probable) |

These are for the lead and the owner. Stage 0 moves no figure; the hull's figures carry the
file's sailing pins.

## 8. What the source cannot give

- **The load draught and the keel**: not drawn (§4); the scantling document attached to the
  sheet, not scanned, may give the draughts.
- **The half-breadths at the water**, the body sections and the midship section
  (`section_m`): no body plan or half-breadth plan.
- **A main wale** below the deck: none drawn.
- **Port sills and port sizes**: no ports; where the guns stood is not drawn.
- **The deck at side** for certain: inferred from D2 (§5.1).
- **The mizen mast, the outrigger, the spars aloft**: only two mast stumps and the bowsprit's
  inner part are drawn; no masting table is on the sheet.
- **The calibre** beyond doubt: "18" is the probable reading of a 6-px figure (§2.1).

## 9. Method and files

The image was read with crops and enlargements, and measured by scripts kept outside the
repository in the session's scratch directory, under `stage0/pages/zaz6306/`: `crop.py` and
`enhance.py` (the crops, enlarged and stretched), `pix.py` (a box's grey values, for the
calibre's figure, §2.1), `ticks.py` and `fitscale.py` (the strip), `greenline.py` (the line),
`vprof.py`, `hprof.py` and `trace.py` (the lines, to sub-pixel by darkness centroids, in grey
or in the red ink alone), `measure.py`, `table.py` and `metres.py` (the stations and points
above), `planends.py` (the plan's ends), `uprights.py`, `colour.py` (the ink of each line) and
`overlay.py` (the traced lines drawn back on the image and checked by eye). Each takes the
cached image's path as its argument.
