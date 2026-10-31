# Pages: RMG ZAZ6306, the gun lugger *Éclair* as taken off afloat (October 2026)

Stage 0 research for package 75, the page named by `Build-Ships.md` §19.1 item 11 and by the
shared draft (`ships-design/shared-design.md` §1.5, the lugger's row; §5 items 12 and 13). It
serves `data/ships/lugger.yaml` (`ships-design/map-generator.md`, the lugger's rows: `lugger()`
in `tools/gen_ships.py`), and the builder B8, who draws a sourced hull profile for the file
(`Build-Ships.md` §5). The catalogue reading this note builds on is
`docs/design/VesselReferences-2026-10.md:85` and `:258`. Facts only: the image is the museum's
photograph, kept outside the repository (§1.1). The hull step (SW-2 with SW-2b.2) added §10 to
§13, her body under the water from the sheets `Build-Ships.md` §5.7 names, and brought §6, §7 and
§8 up to what §5.1 takes. §6's lists are written into her file by `tools/ships/hull_lugger.py`, and
`tests/test_hull_lugger.py` holds the three to each other.

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
`x` by at most 0.17 ft at the rail's ends (judgement: ignored). §10 to §13 keep each sheet's own
frame, said at the head of each, and §6 is the file's: `x` forward of the mid-perpendiculars and
`z` above the green line, which is taken as the file's waterline (`Build-Ships.md` §5.1), both in
metres. The rungs S, S† and T are `Build-Ships.md` §5.0's.

## 0. In brief

**Her body under the water, read in the hull step (§10 to §13):**

- **Le Coureur is her type (judgement), and stands for her body at S†.** They share a stepped or
  panelled rail and a stem of one line: at her length factor 0.89 ft against her 0.90 ft before the
  perpendicular at the water, and 1.11 ft against her 1.11 ft at 5 ft up (§5.3, §11.6). *Éclair*'s
  floor is not drawn: the sharp floor is Le Coureur's, which rises 25° from the rabbet for her first
  3.6 ft, so Chapelle's "great deadrise" is measured. She is 16% longer and 10% broader than *Éclair*
  and proportionally deeper (depth in hold 0.44 of the breadth against 0.34). She cannot stand for
  her stern (a square tuck and counter, *Éclair* is round: S kept), her post (raked 20.6°, *Éclair*
  about 10°: S kept) or her depth (recorded, §13.3).
- **The two sheets of Le Coureur are taken as one hull** (judgement, on the measure). Pâris's plate in Chapelle (p. 7) and Henslow's
  ZAZ6170 agree in the waterlines to 0.19 ft rms after a shift of 1 ft along the ship; the French
  plate is 2.6% narrower. ZAZ6170's body plan is read for the sections (§11).
- **Scales check.** ZAZ6170 11.385 px to the foot, the range of the deck 68.88 ft against 68 ft
  10 in; Chapelle's plate 38.75 px to the foot, its perpendiculars 68.94 ft; ZAZ4734 13.00 px to
  the foot, 64.85 ft against about 65 ft. ZAZ4736 is at 1:32 by its own title and by measure, not
  the catalogue's 1:48 (§11.2, §12.1).
- **The load line** of ZAZ6170 is taken as the top of her four waterlines (judgement), the only one
  carried past the rabbet to the stem's fore edge and aft to the rudder; Pâris's is the top of five, carried past
  both ends. Henslow's has 2.9° of drag and Pâris's 1.87°. *Defender*'s single green line is a
  light line (44 tons against about 89 burthen, judgement), so she is a check, not the stand-in.
- **The drawing.** Between the water and her main breadth the side is Le Coureur's curve moved to her
  own plan (T, §6.2). Her points in §6 pass the tree's schema and `form.check`: drawn displacement
  101 t against the filed 101 t, partly a coincidence (§13.2); drawn 2.53 m deep amidships against
  the file's 2.1 m, recorded, not moved (§6, §7). Her own hold suggests about 6½ ft (§13.2), and is a
  depth of hold and no draught.
- **Ruled (the lead, 2026-10-31; §13.4):** the one factor of principle 7, 2.53 m; her line at her
  sheet's length, 18.33 m, a departure from principle 7's last sentence, whose words give 0.793 where
  §6.2 has 0.868; the hold's floor line no measure; `Build-Ships.md` §5.7's row T to S† under the water.
- **Ports.** No port on her sheet. Le Coureur has four half-ports a side, *Defender* eight, four
  as proposed; all are given as triples. The pick for her: three rail guns, no triple (§6.4).
- **The bowsprit's rating** (§7): 21.8 kN as filed; rule (3)'s words give 37.4 kN. Left and reported,
  a tuning pass's (the lead, 2026-10-31).

**Her own sheet, as first read (stage 0):**

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
- **Against the file** (§7, recorded, not moved): the drawn line is 59.3 to 60.1 ft long (18.1
  to 18.3 m) against the file's 55 ft (16.8 m); the deck stands 2 ft 10 in (0.86 m) above it
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
  keel's lower edge. **That line is a depth of hold and no draught, as the lead ruled (§13.4):** it is
  this reckoning's starting point and not the drawing's measure. The file's 7 ft mean, 8 ft 6 in aft and 5 ft 6 in forward (judgement there
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
  (5.73 ft at 0.71 ft, 6.16 ft at 0.36 ft abaft AP, tentative, where it meets the post's fore edge;
  5.73 ft at 55.9 ft, where it fades); the main and fore channels lie along it (measured).
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
- **The plan's length is the range of the deck** (§3.2), while the rail runs 1.39 ft past AP to the
  taffrail, so at its ends the outline is not the rail (measured; judgement that it is the side at
  the deck throughout).
- **The plan's inner line**, 0.45 ft (5½ in) inside the outline (18.71 ft across amidships):
  the inside of the side at the rail (judgement).

### 5.3 The ends (measured)

- **Taffrail**: the rail's after end, 9.31 ft (2.84 m) above the line, 1.39 ft (0.42 m) abaft AP;
  the post's head, shaded, stands under it.
- **The post**: its after edge from the taffrail to the line at AP (±0.1 ft), 8.6° to the page, 9.6°
  to the line; below it the same straight edge, dashed, 9.8° to the page and 10.8° to the line (15
  rows, rms 0.31 px, crossing the line at px 502.2), the post broadening to 1.5 ft at the strip
  (§4).
- **The rudder**: hung outside the post on two braces, its after edge 2.07 ft abaft AP at the
  line; its blade 1.9 ft broad at the line and 2.8 ft at the strip; its head about 5.8 ft above
  the line. On its head a Y-shaped fitting with two arms reaching 2¼ ft out to either side and
  2 to 3 ft abaft, sloping down, ending in rings (a yoke for steering lines, judgement; or the
  guys of a mizen outrigger, which is not otherwise drawn).
- **The stem**: its fore edge stands 0.90 ft before FP at the line, 1.11 ft from 4 to 6 ft up, 1.02
  ft at its top, 9.57 ft above the line, where it ends at a dot past the bowsprit (measured;
  tentative above 7.9 ft, a faint line). The side's rail ends at FP, 9.29 to 9.38 ft (2.83 to 2.86
  m) above the line, with a shaded timber (the stem head or knighthead) and a rounded fitting at the
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
| Main mast hole | **25.24** (circle 1.4 ft across) | **−1.34** | measured; the profile's stump's after edge meets the deck at 24.25 ft; its centre 24.87 ft (−1.45 m) |
| Galley | 26.0 to 28.0 | −1.10 to −0.50 | read, measured |
| Main hatch | 28.2 to 32.9 | −0.44 to +1.00 | read, measured |
| Fore hatch | 45.9 to 49.4 | +4.96 to +6.03 | read, measured |
| Fore mast hole | **55.56** (circle 1.4 ft across), 3.7 ft abaft FP | **+7.90** | measured; the stump's after edge at 54.56 ft; its centre 55.2 ft (+7.79 m) |
| Mizen mast | not drawn | | read |

- The masts are drawn in the profile only as stumps above the rail, each of two parallel lines 1.2
  ft apart, the after one heavy, raking 7.5° (main) and 1.8° (fore) to the page, 8.6° and 2.8° to
  the line (measured). Their centres stand 0.35 ft abaft the plan's holes, within the plan's
  registration; the holes are taken as the stations (judgement).
- The fore mast 3.7 ft abaft FP fits Willaumez 1831 pp. 145 to 146 on the chasse-marée, the
  fore mast two or three feet abaft the stem head, and the main mast near the middle, much
  raked (`VesselReferences-2026-10.md:244-247`, read there).

## 6. For the profile: the points §5.1 takes, in metres

`x` forward of the mid-perpendiculars, `z` above the drawn line, taken as the file's waterline
(`Build-Ships.md` §5.1), half-breadths plank on. Where the schema wants x increasing, the two steps
are given 0.01 m apart. Every list below is written into her file by `tools/ships/hull_lugger.py`
through the tree's own `g.hull_profile` and `g.hull_form`: they load and draw, **drawn displacement
101 t against the filed 101 t (+0%), drawn 2.53 m deep at the greatest section against the file's
2.1 m** (measured; recorded, not moved: §7).

### 6.1 Her own sheet (S; measured unless marked, from §5)

- **`rail_m`**: [−9.45, 2.84], [−9.03, 2.74], [−8.27, 2.60], [−7.51, 2.48], [−6.74, 2.39],
  [−5.98, 2.31], [−5.22, 2.24], [−4.44, 2.18], [−4.43, 1.62], [−3.70, 1.59], [−2.93, 1.55],
  [−2.17, 1.52], [−1.41, 1.50], [−0.65, 1.49], [0.00, 1.50], [0.88, 1.52], [1.64, 1.53],
  [2.40, 1.57], [3.16, 1.61], [3.92, 1.66], [4.09, 1.69], [4.10, 1.94], [4.69, 1.98], [5.45, 2.05],
  [6.21, 2.14], [6.97, 2.25], [7.73, 2.39], [8.50, 2.60], [9.03, 2.83].
- **`breadth_m`**, [x, hb_water, hb_rail]: the third figure is the plan's outline, S (whether it is
  the rail or the deck is judgement, §5.2); the second is the stand-in's at the water, S†, from
  −8.69 to +8.85 (§6.2); the three figures aft of −8.75 and the two at +8.97 and +8.99 are T, the
  line closed to 0.10 m at her post and 0.06 m at the stem's fore edge. The schema refuses a
  half-breadth of nothing, so the plan's two end points at 0.00 are left out and the round ends
  close by the stern's and the stem's lines: [−9.02, 0.12, 0.27],
  [−8.95, 0.22, 0.54], [−8.84, 0.39, 0.81], [−8.69, 0.58, 1.09], [−8.43, 0.89, 1.36],
  [−8.24, 1.12, 1.63], [−7.51, 1.69, 2.21], [−6.74, 2.04, 2.55], [−5.98, 2.30, 2.73],
  [−5.22, 2.50, 2.83], [−4.46, 2.65, 2.89], [−2.93, 2.88, 2.96], [−1.41, 3.00, 2.98],
  [0.00, 3.06, 2.98], [1.64, 2.99, 2.97], [3.16, 2.83, 2.98], [4.69, 2.51, 2.97],
  [5.45, 2.21, 2.90], [6.21, 1.88, 2.77], [6.97, 1.36, 2.49], [7.73, 0.84, 2.07],
  [8.26, 0.49, 1.63], [8.50, 0.37, 1.36], [8.69, 0.27, 1.09], [8.85, 0.19, 0.81],
  [8.97, 0.15, 0.54], [8.99, 0.14, 0.27].
- **`decks_m.upper`** (the deck at side): D2, judgement on what it is (§5.1); its ends are where the
  line can be traced, 2.5 ft from AP and 57.5 ft: [−8.27, 1.17], [−7.51, 1.12], [−6.74, 1.07],
  [−5.98, 0.99], [−5.22, 0.94], [−4.46, 0.89], [−3.70, 0.83], [−2.93, 0.79], [−2.17, 0.78],
  [−1.41, 0.76], [−0.65, 0.75], [0.00, 0.74], [0.88, 0.75], [1.64, 0.76], [2.40, 0.78],
  [3.16, 0.81], [3.92, 0.84], [4.69, 0.89], [5.45, 0.97], [6.21, 1.08], [6.97, 1.14], [7.73, 1.21],
  [8.50, 1.28]. The deck at the middle line (D) stands 0.11 to 0.12 m higher amidships:
  [−4.46, 0.97] to [3.92, 0.92], 0.86 at 0.00.
- **`stem_m`**, the fore edge, low to high: [6.86, −2.18] (the keel's fore end: her dashed line
  carried on at its 18° to the stand-in's keel, T); [8.06, −1.79], [8.37, −1.69], [8.64, −1.52],
  [8.83, −1.32], [9.01, −1.10], [9.14, −0.83] (dashed, tentative); [9.30, 0.00], [9.34, 0.42],
  [9.37, 1.07], [9.37, 1.83], [9.36, 2.42], [9.34, 2.91] (measured, §5.3); the head [9.04, 2.92].
- **`stern_m`**, the post's after edge, low to high: [−8.49, −2.98] (the heel: her dashed post
  carried on at its 11° to the stand-in's keel, T); [−8.66, −2.11] (dashed, at the strip);
  [−9.03, 0.00]; [−9.45, 2.84] (the taffrail). No counter: the post rises straight to the taffrail.
- **`wales_m`**: no wale is drawn below the deck. The only band on the side is B to C (judgement on
  what it is, §5.1), from the post's fore edge to where C fades: [−9.14, 1.88, 2.07],
  [−8.27, 1.63, 1.87], [−5.98, 1.34, 1.58], [−2.93, 1.12, 1.36], [0.00, 1.07, 1.32],
  [3.16, 1.20, 1.43], [6.21, 1.47, 1.70], [7.73, 1.72, 1.95], [8.01, 1.75, 1.99]. Le Coureur's and
  *Defender*'s main wale lies below the deck (§11.6, §12.3); none is given her: her sheet is an
  inboard profile and blank below the deck, which does not show she had none; Le Coureur's at the
  factors would stand 0.40 to 0.80 m at midships, across her deck at side (0.74 m). T, for the lead.

### 6.2 Under the water (S†, Le Coureur on ZAZ6170, §11 and §13)

**The factors** (principle 7):

- **Lengths 0.868** (not 0.793, §13.4): her line 60.32 ft as first read, the post's after edge to
  the stem's fore edge, over Le Coureur's 69.51 ft on line A (§11.6). Her ft from AP = −0.13 + 0.868 ×
  (Le Coureur's ft from AP − 0.40). Read again (§5.3) her line is 60.14 ft, which would give 0.865;
  that moves no station by more than 0.05 m, under principle 2's 2 px, so the stations stand as first
  measured (judgement).
- **Sections 0.9135**, heights and half-breadths alike: her moulded 20 ft 0 in over Le Coureur's 21
  ft 10¾ in, the body plan's rectangle (§11.2). Heights are read from line A at each station. The
  extreme breadths give 0.911.
- **Plank 2 in** added to each half-breadth, hers: 20 ft 4 in less 20 ft 0 in, halved. At the
  greatest section this gives 3.10 m, the file's half-beam.
- **Not done:** the body is not turned from Le Coureur's 2.9° of drag to her line's 1.05°. It would
  move the keel by about 0.3 m at the ends (judgement), and the drawn 3.0° agrees with the file's
  own 3 ft of trim.

**`sections_m`**, by Le Coureur's numbered stations, each [x] then [z, hb], low to high. Each is
read from the body plan at the heights given; a section's lowest point is where its curve reaches
the keel or the post.

**Above z = 0 the points are T, not S†:** the same station's curve (§11.4) at the factors, moved straight
in height by what her main breadth (§6.3) has over or under Le Coureur's there, and never past it,
stopping 0.05 m short of the main breadth's height. Her plan is fuller than Le Coureur's toward both
ends and narrower at station 12, so that with no point here the side runs straight from the water
to a hard corner at the main breadth, which neither body plan has (§11.4, §12.3) and which shows on
the quarter in the owner's picture. The curve moves the side off that straight line by 0.22 m at
station 12, 0.20 m at station 2, 0.13 m at stations 11 and 3 and 0.04 m or less from station 9 to
station 4 (measured), and moves nothing under the water, so the drawn displacement stands.

| Stn | Her x | [z, hb] |
|---|---|---|
| 12 | −8.23 | [−0.60, 0.18], [−0.40, 0.38], [−0.20, 0.73], [0.00, 1.13], [0.20, 1.41], [0.40, 1.59], [0.60, 1.68], [0.80, 1.70] |
| 11 | −7.43 | [−1.25, 0.19], [−1.00, 0.28], [−0.80, 0.34], [−0.60, 0.56], [−0.40, 0.92], [−0.20, 1.40], [0.00, 1.75], [0.20, 1.96], [0.40, 2.11], [0.60, 2.22], [0.80, 2.29] |
| 10 | −6.62 | [−1.50, 0.28], [−1.25, 0.39], [−1.00, 0.51], [−0.80, 0.75], [−0.60, 1.11], [−0.40, 1.54], [−0.20, 1.88], [0.00, 2.09], [0.20, 2.28], [0.40, 2.44], [0.60, 2.55], [0.80, 2.64] |
| 9 | −5.57 | [−2.25, 0.15], [−2.00, 0.26], [−1.75, 0.35], [−1.50, 0.50], [−1.25, 0.70], [−1.00, 1.04], [−0.80, 1.41], [−0.60, 1.80], [−0.40, 2.09], [−0.20, 2.29], [0.00, 2.42], [0.20, 2.58], [0.40, 2.71], [0.60, 2.82] |
| 8 | −4.24 | [−2.00, 0.35], [−1.75, 0.55], [−1.50, 0.85], [−1.25, 1.24], [−1.00, 1.73], [−0.80, 2.05], [−0.60, 2.31], [−0.40, 2.50], [−0.20, 2.62], [0.00, 2.70], [0.20, 2.81], [0.40, 2.89], [0.60, 2.96] |
| 7 | −2.36 | [−2.00, 0.48], [−1.75, 0.86], [−1.50, 1.40], [−1.25, 1.89], [−1.00, 2.29], [−0.80, 2.52], [−0.60, 2.71], [−0.40, 2.81], [−0.20, 2.90], [0.00, 2.96], [0.20, 3.01], [0.40, 3.06] |
| 6 | +0.27 | [−2.00, 0.50], [−1.75, 1.07], [−1.50, 1.67], [−1.25, 2.15], [−1.00, 2.49], [−0.80, 2.69], [−0.60, 2.83], [−0.40, 2.94], [−0.20, 3.02], [0.00, 3.07], [0.20, 3.09] |
| 5 | +2.64 | [−1.75, 0.68], [−1.50, 1.20], [−1.25, 1.72], [−1.00, 2.14], [−0.80, 2.40], [−0.60, 2.59], [−0.40, 2.74], [−0.20, 2.84], [0.00, 2.93], [0.20, 3.00], [0.40, 3.05] |
| 4 | +4.52 | [−1.50, 0.65], [−1.25, 1.04], [−1.00, 1.48], [−0.80, 1.81], [−0.60, 2.07], [−0.40, 2.29], [−0.20, 2.45], [0.00, 2.57], [0.20, 2.74], [0.40, 2.87], [0.60, 2.99] |
| 3 | +6.11 | [−1.50, 0.32], [−1.25, 0.53], [−1.00, 0.79], [−0.80, 1.02], [−0.60, 1.27], [−0.40, 1.53], [−0.20, 1.76], [0.00, 1.95], [0.20, 2.17], [0.40, 2.36], [0.60, 2.52], [0.80, 2.65], [1.00, 2.75] |
| 2 | +7.43 | [−1.50, 0.18], [−1.25, 0.27], [−1.00, 0.37], [−0.80, 0.48], [−0.60, 0.59], [−0.40, 0.74], [−0.20, 0.88], [0.00, 1.04], [0.20, 1.29], [0.40, 1.52], [0.60, 1.73], [0.80, 1.92], [1.00, 2.06], [1.25, 2.21] |
| 1 | +8.25 | [−1.00, 0.17], [−0.80, 0.23], [−0.60, 0.28], [−0.40, 0.35], [−0.20, 0.41], [0.00, 0.50], [0.20, 0.64], [0.40, 0.79], [0.60, 0.95], [0.80, 1.10], [1.00, 1.26], [1.25, 1.44], [1.50, 1.58] |

- **`section_m`**, the midship section, [z, hb], plank on: below 0.30 m Le Coureur's station 6, the
  mean of its two halves on the body plan, S†; then her own rail, S: [−2.53, 0.10], [−2.22, 0.15],
  [−2.00, 0.50], [−1.80, 0.95], [−1.60, 1.44], [−1.40, 1.88], [−1.20, 2.23], [−1.00, 2.49],
  [−0.80, 2.69], [−0.60, 2.83], [−0.40, 2.94], [−0.20, 3.02], [0.00, 3.07], [0.20, 3.10],
  [0.30, 3.10], [1.50, 2.98]. Deadrise 25° from the rabbet for the first
  1.0 m.
- **`keel_m`**, the keel's lower edge, the post's heel to the forefoot: [−8.49, −2.98],
  [−4.24, −2.77], [0.27, −2.53], [2.64, −2.40], [4.52, −2.30], [6.11, −2.22], [6.86, −2.18]. Le
  Coureur's keel at the factors; the two ends where her own dashed post and forefoot, carried on,
  meet it (T). Falls 3.0°.
- **`rabbet_m`**, [x, z, half-siding], not drawn: [−8.69, 0.00, 0.10], [−8.19, −2.10, 0.10] (her
  post's dashed fore edge, tentative), then the stand-in's: [−8.02, −2.67, 0.10],
  [−6.62, −2.59, 0.10], [−5.57, −2.53, 0.10], [−4.24, −2.46, 0.10], [−2.36, −2.36, 0.10],
  [0.27, −2.22, 0.10], [2.64, −2.10, 0.10], [4.52, −2.00, 0.10], [6.11, −1.91, 0.10],
  [7.43, −1.84, 0.10], [8.03, −1.60, 0.10], [8.36, −1.34, 0.10], [8.54, −1.09, 0.10],
  [8.66, −0.84, 0.10], [8.75, −0.59, 0.10], [8.84, −0.34, 0.10], [8.91, 0.00, 0.10]. The half-siding
  is Le Coureur's 0.37 ft at the factor (measured on the keel of her body plan).
- **`floor_m`**: not given. No sheet draws a rising line; the turn of the bilge on the body plan is
  not a line to read (judgement).

### 6.3 The shape keys above the water

- **`breadth_line_m`**, [x, z, hb], `judged`: the height is Le Coureur's at the factors (S†), the
  height of each station's greatest half-breadth on her body plan, above A (§11.4's table); the half-breadth is her
  own plan's outline plus a tumblehome fading from 0.114 m amidships, the difference between the
  caption's 20 ft 4 in and the plan's 19 ft 7 in, halved, in proportion to the plan's half-breadth. Le Coureur's own half-breadths are not used here:
  her ends are finer at the rail than *Éclair*'s (§13.2). [−8.23, 0.96, 1.70], [−7.43, 1.01, 2.33],
  [−6.62, 0.91, 2.68], [−5.57, 0.74, 2.89], [−4.24, 0.74, 3.01], [−2.36, 0.50, 3.08],
  [0.27, 0.40, 3.09], [2.64, 0.62, 3.09], [4.52, 0.77, 3.08], [6.11, 1.29, 2.89],
  [7.43, 1.50, 2.32], [8.25, 1.77, 1.70].
- **`form.stern`**: `type: round`, S (§5.2, §5.3): no transom, no counter, no galleries and no
  lights on her sheet; none is invented. Le Coureur's square tuck (§11.8) is not hers.
- **`form.head`**: `none`, S: the stem ends in a plain head above the rail. So do Le Coureur's and
  *Defender*'s. **`head_m`**: none.
- **`form.fullness`**: not given. The sections carry the ends; the rule fills only beyond stations
  12 and 1.
- **`channel_wales_m`**: none drawn. The channels lie along C (§5.1).

### 6.4 The ports (T: her sheet has none, §5.4)

- **The pick: no `ports_m` and no `port_size_m`.** *Éclair*'s draughtsman drew her rail's steps, its
  uprights and her channels, and no port, in the profile or the plan (read); the sheets of Le
  Coureur and *Defender* draw theirs. So she is taken to have fired over the rail or from slides
  (judgement). §5.1 gives a rail gun and a pivot no port, and §5.3 their height from `rail_at`: 1.49
  to 1.66 m in the waist. A sill at the rail is refused by the schema.
- **If ports were ever ruled** (the lead, 2026-10-31: as built, none), here is what can be said, every figure T: two a side at the two of
  *Defender*'s proposed places that fall in her waist (§12.5, at the length factor), each sill 0.27
  m (0.9 ft, unscaled: a gun's height does not scale) above her own deck at side, each half-breadth
  on her side between main breadth and rail. `ports_m.upper`: [−2.24, 1.05, 3.03],
  [1.34, 1.03, 3.03]; `port_size_m.upper`: [0.78, 0.45], the width *Defender*'s proposal's and the
  depth cut off by her rail. *Defender*'s places are taken though she is the check and not the
  stand-in, since her proposal states carronades' sills and Le Coureur's half-ports stand 8.7 to 10.4
  ft apart and differ between the sheets. Their gaps to the drawn side are −0.01 m each (measured).
  Three guns do not divide evenly between two sides, and no sheet says where the third stood.
- **The other sheets' triples**, their own and at her scale, are in §11.7 and §12.5.

### 6.5 The marks (`Build-Ships.md` §5.0 principle 4)

`rail_m: sourced`, `breadth_m: judged` (its water's two ends only, §6.1; between them the stand-in's,
and its rail her own), `keel_m: judged` (its two ends, carried on from her dashed lines; between them
the stand-in's), `stem_m: judged` (its foot only; above it her own), `stern_m: judged` (its heel
only; above it her own), `wales_m: judged` (its heights measured on her own sheet, S; that it is her
wale, T), `section_m: stand-in`, `decks_m: judged` (first `sourced`: its heights measured on her own sheet, S; what the line is, T), `breadth_line_m: judged`, `sections_m: judged`
(above the water only, §6.2; up to it the stand-in's), `rabbet_m: stand-in`, `form.stern: sourced`, `form.head: sourced`. Each line takes the
word of its weakest point, and the note says where along the hull it is. `decks_m` is measured on her
own sheet; what the line is, deck at side or the plank's underside, is judgement, and though both
readings lie within an inch (§5.1) principle 4 has no exception for a small one.

## 7. Against `data/ships/lugger.yaml` (recorded, not moved)

| Field | The file (its note) | The sheet |
|---|---|---|
| `length_waterline_m` | 16.8 (55 ft, judgement between keel and deck) | 18.33 m (60.14 ft) from the post to the stem's fore edge on the drawn line; 18.06 m between the perpendiculars (measured) |
| `beam_m` | 6.2 (20 ft 4 in extreme) | the extreme breadth is not drawn; 5.97 m (19 ft 7 in) outside at the rail or deck (measured) |
| Half-breadth at the water | 3.10 m (half of `beam_m`) | the stand-in 3.07 m at its greatest section, 3.06 m at x = 0; the main breadth reaches 3.10 m at the factor, 0.3 m above the water (§6.2, §6.3) |
| The waterline | z = 0, as the file has it | her green line is taken as z = 0 (§4, §6), recorded beside the file's line and not moved; whether it is her load line, §8 |
| `draught_m` | 2.1 (7 ft mean, 8 ft 6 in aft, 5 ft 6 in forward; judgement) | not given; at least 2.1 m aft and 1.8 m at the forefoot (§4); 1.8 to 2.0 m amidships (judgement). The stand-in draws 2.53 m amidships, 2.98 m at the heel, 2.18 m at the forefoot (§6.2, §13.3) |
| `displacement_kg` | 101,000 (LWL x beam x draught x Cb 0.45) | drawn 101 t on her points, +0%, partly a coincidence; 95 t moulded (§6, §13.2) |
| Trim, from the draught's note | 3 ft over 55 ft, 3.1° | the green line 1.05° to the page, 1.1 ft (§4); the stand-in's keel 3.0° (§6.2) |
| `deck_height_m` | 1.0 (3 ft 3 in, judgement) | 0.86 m at the middle line, 0.74 m at side (D2) amidships (measured) |
| `fore.mast` `x_m`, `rake_deg` | 6.6 (21.6 ft before the middle, Forfait); 1.6 | +7.90 (the plan's hole); 1.8 to the page, 2.8 to the line |
| `main.mast` `x_m`, `rake_deg` | −0.7 (2.4 ft abaft, Forfait); 4.8 | −1.34 (the plan's hole); 7.5 to the page, 8.6 to the line |
| `mizen.mast` `x_m` | −8.7 (Forfait) | not drawn |
| `bowsprit` `height_m` | 1.5 | 1.47 to 1.51 m above D2 near the stem (measured). **Drawn level**: the viewer roots the heel at the rail's end, 2.83 m, and takes the end's height from the file, 1.0 + 1.5 m above the water, below the heel, so it gives no rise; her sheet's steeve is 5.5° to the page (§5.3). A figure the physics reads: not moved |
| The lugs' feet, `corners_m` | 0.9 m above the datum, 1.9 m above the water, at each tack | her raised rail stands 2.18 to 2.84 m abaft −4.44 and 1.94 to 2.83 m before +4.10 (§5.2), so the feet of the fore, main and mizen lugs run under the rail through her raised ends in the drawing. Read by the physics: not moved |
| The gun fit "gun lugger 1795" (`Build-Ships.md` §9.1) | three guns, calibre unread | three 18-pounders (read, probable); no port on the sheet (§6.4) |
| `bowsprit` `rating_kn`, left and reported (the lead, 2026-10-31) | 21.8 kN: the flying jib alone, whose chain runs through it, in 55 kn (the lead's note of 2026-10-30, "hers for SW-2") | **old 21.8 kN, 37.4 kN by rule (3)'s words**, the larger of the rating named in the script (both jibs in 55 kn) and the sails' (measured: her file built into the scratch directory, the pass's figures printed): +15.6 kN. A figure the physics reads: not moved |

These are for the lead and the owner. Stage 0 moves no figure, and the hull step moves none (`Build-Ships.md`
§5.0 principle 8, §5.6); the hull's figures carry the file's sailing pins.

## 8. What the sources cannot give

- **Her own body**: no sheet of her has a body plan, a half-breadth plan or a keel. Everything under
  the water but her dashed post and forefoot is a stand-in (§6.2) or a judgement, and so is the curve of
  the side between the water and her main breadth (§6.2).
- **Her load draught**: not drawn (§4). The scantling document attached to her sheet, not scanned,
  may give the draughts; a sharper scan or that document would move the keel, not the sections.
- **Whether her green line is her load line**: the sheet does not say (§4). Against A on Le Coureur
  at the factors it stands nearer her deck at side (2.44 against 3.11 ft), farther below her rail
  (4.92 against 4.04 ft) and lower in proportion to her hold (0.55 against 0.60), so the measures do
  not settle it (judgement).
- **A main wale** below the deck: none drawn.
- **Port sills and port sizes of her own**: no ports; where the guns stood is not drawn (§6.4).
- **The deck at side** for certain: inferred from D2 (§5.1).
- **The mizen mast, the outrigger, the spars aloft**: only two mast stumps and the bowsprit's inner
  part are drawn; no masting table is on the sheet. *Defender*'s table (§12.6) and Le Coureur's sail
  plan (§10) are for a later reader of the rig.
- **The calibre** beyond doubt: "18" is the probable reading of a 6-px figure (§2.1).
- **Le Coureur's and *Defender*'s fine figures**: at 1280 px both Greenwich sheets read to about an
  inch at the scale of the ship, and several of *Defender*'s written figures not at all (§12.1). The
  museum licenses sharper scans; the drawing does not need them (judgement).

## 9. Method and files

The stage-0 image was read with crops and enlargements, and measured by scripts kept outside the
repository in the session's scratch directory, under `stage0/pages/zaz6306/`: `crop.py` and
`enhance.py` (the crops, enlarged and stretched), `pix.py` (a box's grey values, for the calibre's
figure, §2.1), `ticks.py` and `fitscale.py` (the strip), `greenline.py` (the line), `vprof.py`,
`hprof.py` and `trace.py` (the lines, to sub-pixel by darkness centroids, in grey or in the red ink
alone), `measure.py`, `table.py` and `metres.py` (the stations and points above), `planends.py` (the
plan's ends), `uprights.py`, `colour.py` (the ink of each line) and `overlay.py` (the traced lines
drawn back on the image and checked by eye). Each takes the cached image's path as its argument.

The hull step's are in the same directory under `hulls/streams/lugger/`: `view.py`, `enh.py` and
`grid.py` (crops, stretched, with a pixel grid), `strip.py`, `z70strip.py`, `c23b.py` and `d34a.py`
(the strips and bars), `lib.py` and `track.py` (lines to sub-pixel, followed along their length),
`bodies.py` (the body plans' curves picked row by row, 6 px apart), `overlay.py` (those picks drawn
back on the sheets and checked by eye: every pick lay on its curve), `tables.py` (§11 and §12's
tables, and the two sheets' cross-check), `vol.py` (the displacements), `eclair.py` and
`assemble.py` (§6's points), `profile_check.py` and `render.py` (those points through the tree's
schema and form, and drawn for the eye; freesail imported from this worktree), and `rating.py` (§7's
bowsprit, built into the scratch directory). The independent check's scripts are under `xchk/`, and
the build's under `build/`: the ends read again (`crop_ends.py`, `coureur_stem.py`), the depth's
options through the tree's form (`depth_try.py`, §13.4) and the sheets of the drawn hull. The review's
are under `review/`: `ov.py` to `ov6.py` (her points drawn back on the three sheets and looked at),
`upper2.py` and `off.py` (§6.2's points above the water and how far they stand off the straight line),
`mut.py` (her file and this note changed one figure at a time in a copy, to see which tests notice) and
`pair.py` (`Build-Ships.md` §5.6's pair check as read there). No image and no crop is in the repository.

## 10. The sheets read for her body

Under `Build-Ships.md` §5.7's row. The caches are outside the repository, under
`D:/Projects/FreeSail/reference-cache/`, fetched 2026-10-30 with a generic user-agent.

| Sheet | What | Image |
|---|---|---|
| Chapelle 1930, p. 7 | "Inboard Profile and Lines of the French Lugger 'Le Coureur,' of 1775. From Admiral de Paris, 'Souvenirs de Marine,' Vol. I" (read); printed sideways. The book's rights as `pages-chapelle-fig17.md` §1.1 | IA `baltimoreclipper00howa`, leaf 23, `baltimoreclipper00howa_0023.jp2`, 2756 x 3715 px, 146,046 bytes, sha256 `afe8169cd013a0c30fb1b5ad2f70ada52bfa5dc166765c8857fb2315ed5d141a`; `chapelle-fig17/leaf0023/` |
| Chapelle 1930, p. 6 | "Sail Plan of the French Lugger 'Le Coureur,' of 1775", the same source, in metres (read; the masts' places only) | Leaf 22, 217,220 bytes, sha256 `68c0cc61...ac56ac`; `chapelle-fig17/leaf0022/`. Leaf 24, p. 8, text, fetched and not used |
| RMG ZAZ6170 | "Coureur (1778)", object 85961: 1:48; body plan with stern board, sheer with inboard works and the proposed alterations in green, half-breadth, midship section showing the clinker framing (catalogue), for her as modified to an 8-gun schooner; signed by John Henslow, 18 September 1778; sheet 325 x 700 mm (catalogue) | https://collections.rmg.co.uk/media/415/474/j0873.jpg, 1280 x 597 px, 161,207 bytes, sha256 `b8b922f3277e128f0a7738fe91776a479d15ce52a3c5e95537bd02539468f0e3`; `zaz6306/j0873/`; also `zaz6306/mid_j0873/` |
| RMG ZAZ4734 | "Defender (captured 1809)", object 84525: 1:32; body plan with stern board outline, inboard profile with one waterline, half-breadth, table of masts and spars; taken off at Sheerness before fitting as an 8-gun lugger; signed by George Parkin, 25 April 1810; sheet 336 x 927 mm (catalogue) | https://collections.rmg.co.uk/media/2/438/502/j4832.jpg, 1280 x 463 px, 125,698 bytes, sha256 `d65c0d53495c771d82684791f49b4238c6526d0cf84446bfbcdde7ae5e15a323`; `zaz6306/j4832/` |
| RMG ZAZ4735 | Object 84526: 1:48; inboard profile, upper deck, section and platforms as proposed, with recoil or non-recoil carronades; 25 April 1810; sheet 369 x 639 mm (catalogue) | https://collections.rmg.co.uk/media/2/438/500/j4830.jpg, 1280 x 730 px, 179,328 bytes, sha256 `cd08821b8376e952649c069b06a65c896974fa570e0c87ccb3de2f8d2a5d69a8`; `zaz6306/j4830/` |
| RMG ZAZ4736 | Object 84527: upper deck as taken off, 25 April 1810; sheet 261 x 740 mm; the catalogue says 1:48, and the sheet is 1:32 (§12.1) | https://collections.rmg.co.uk/media/2/438/501/j4831.jpg, 1280 x 455 px, 84,354 bytes, sha256 `8a80d2965adb6bb2396faffc962d0834001612393ccae6b6098b7e16358a93d4`; `zaz6306/j4831/` |

The object pages as fetched are in `zaz6306/page/` (`object-85961.html`, `object-84525.html` to
`-84527.html`). **Rights:** each page credits "© Crown copyright. National Maritime Museum,
Greenwich, London" and offers licensing through RMG Images. Commons holds copies of these sheets
tagged public domain (`File:Plan du Lougre le Coureur en 1778.jpg`, `File:DEFENDER 1809 RMG
J4832.jpg` and its two fellows); as `Build-Ships.md` §5.9 rules, they are read and cited, never
copied. Commons also holds Clerc-Rampal 1913 p. 154, a picture of the Musée de Marine's model of
her, whose caption gives 22 metres, 120 tonneaux and eight guns of the calibre of 6 (read in the
Commons entry only, the picture not fetched; a check for the eye at most, §5.8). The plate's outer
perpendiculars stand 22.02 m apart by its own bar (§11.2); the caption is noted beside that, not used.

## 11. Le Coureur

**Frame in this section.** On ZAZ6170: ft forward of **AP**, the sheet's after red vertical, whose
distance from the fore one is the range of the deck; heights in ft above line A (§11.3) at the
station, along the page. A's tilt moves a point 8 ft below it by 0.4 ft along the ship (judgement:
ignored, as §4's). On the plate: ft forward of its inner after perpendicular (§11.2); heights above
WL1. Half-breadths are moulded, off the sheet's middle line. Stations are the sheets' own numbers;
the numbers do not stand at the same places on the two.

### 11.1 Who she is

- Chapelle (OCR l. 494-508): a three-masted lugger of the chasse-marée type, built in 1776 by M.
  Denys to a plan approved by the minister of the Marine, the order signed 22 December 1775; on the
  American coast in the Revolution and at the action of the *Belle-Poule*; "slightly raking ends,
  great deadrise and rather sharp waterlines". The plate carries "approuvé" and a signature read
  tentatively as de Sartine's.
- ZAZ6170 is the vessel the Navy took in 1778, drawn for her fitting as a schooner (catalogue).
  §5.7's "by name and date, inference" now has a measure behind it: the two sheets are one hull
  (§11.9).
- **ZAZ6170's alterations** are the green ticked lines, as its title says (read); the lines of the
  hull are not altered, and the green is ignored here.

### 11.2 The scales and their checks (measured)

| Check | Stated or expected | Measured | Basis |
|---|---|---|---|
| ZAZ6170's strip | 1:48 (catalogue) | **11.385 px to the foot**, rms 0.29 px, largest 0.72 px, 72 ticks over 71 ft | 1.793 px/mm; the paper 1,265 x 587 px comes to 706 x 327 mm against 700 x 325 mm (+0.8%, +0.7%) |
| Range of the deck, ZAZ6170 | 68 ft 10 in (read) | **68 ft 10.6 in** (68.88 ft) | the two red verticals, 784.2 px apart |
| Breadth, ZAZ6170 | extreme 22 ft 3¾ in (read) | moulded **21 ft 10¾ in** (21.89 ft), the body plan's rectangle, 249.25 px | a plank of 2½ in a side reconciles them (judgement); the midship section's outside, 22 ft 0½ in at 9.1 ft above the keel's top |
| Depth in hold, ZAZ6170 | 9 ft 10½ in (read) | 9 ft 8 in to 10 ft 4 in | the midship section, the ceiling beside the keelson to the deck beam's under and upper side |
| Burthen, ZAZ6170 | 138 and a fraction over 94 (read; the fraction not) | 139 | the rule on 52 ft 5¾ in by 22 ft 3¾ in (judgement: arithmetic) |
| The plate's metre bar | 22 m | **127.1 px to the metre, 38.75 px to the foot** | the bar's alternate metres, rms 1.8 px |
| The plate's foot bar | the French foot, 0.3248 m (memory, unverified) | 41.2 px to the foot, 126.7 px to the metre (−0.3%) | 18 divisions |
| Its two perpendiculars | none stated | inner pair **68.94 ft** (2,671.5 px) against ZAZ6170's 68 ft 10 in (+0.2%); outer pair 22.02 m by its own bar | dashed verticals, both plans |
| Its breadth | none stated | **10.66 ft a side**, 3.25 m, so 20 French feet across (judgement): 2.6% under ZAZ6170's | the plan's outer line at station 6 |
| The plate's page | | the station lines fan out by 0.5° toward the bow (7.8 px in 920 px): the page is warped | so every figure is read beside its own station line |

### 11.3 The load line, and how it was judged

- **ZAZ6170: line A**, the top of four straight parallel waterlines, 2.20 ft apart: y = 258.75 +
  0.0506 x px, rms 0.14 px over twelve stations (measured). Not labelled. Judged the load line
  because it alone is carried past the rabbet, to the stem's fore edge and aft to the rudder; the
  other three stop at the rabbet (read). It falls 2.9° to the keel. The displacement to it, moulded,
  is 4,507 ft³, 129 tons at 35 ft³ to the ton, 0.93 of her burthen (measured; judgement that this is
  a laden figure).
- **The plate: WL1**, the top of five, 1.43 ft apart, carried past both ends of the sheer (read). It
  falls **1.87°** to the keel. ZAZ6170's A stands 1.1 ft above it at the stern, 0.6 ft amidships and
  0.1 ft at the bow. Judgement: the plate's is the designer's line, Henslow's the ship as she was
  taken or trimmed. A is used here.

### 11.4 ZAZ6170 by station (measured)

Heights ±0.1 ft, half-breadths ±0.1 ft. The half-breadths are from the body plan, read row by row at
each line's height; the half-breadth plan's own lines agree within 0.2 ft where they part clearly
(stations 8 to 5). Station 12's mark on the sheer is faint; the body plan labels it (read).

| Stn | ft from AP | A above the keel's top | Raised rail | Rail | Panel cap | Wale top | Wale foot | B | C | D | Keel's foot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 | 3.57 | 9.63 | 8.56 | 5.52 | | | 2.42 | −2.20 | −4.32 | | −10.72 |
| 11 | 6.59 | 9.46 | 8.38 | 5.29 | | 3.68 | 2.19 | −2.20 | −4.41 | −6.57 | −10.56 |
| 10 | 9.64 | 9.30 | 8.21 | 5.02 | | 3.39 | 1.97 | −2.20 | −4.46 | −6.57 | −10.40 |
| 9 | 13.61 | 9.10 | 8.07 | 4.78 | | 3.21 | 1.76 | −2.19 | −4.40 | −6.58 | −10.20 |
| 8 | 18.67 | 8.84 | 7.80 | 4.58 | | 3.00 | 1.57 | −2.20 | −4.40 | −6.56 | −9.94 |
| 7 | 25.75 | 8.48 | | 4.42 | 5.45 (between panels) | 2.91 | 1.41 | −2.19 | −4.40 | −6.51 | −9.58 |
| 6 | 35.71 | 7.98 | | 4.42 | 5.45 | 2.88 | 1.42 | −2.20 | −4.39 | −6.49 | −9.07 |
| 5 | 44.68 | 7.53 | | 4.73 | 5.72 | 3.17 | 1.73 | −2.21 | −4.40 | −6.55 | −8.63 |
| 4 | 51.78 | 7.15 | | 5.26 | 6.32 (between panels) | 3.72 | 2.25 | −2.16 | −4.37 | −6.53 | −8.25 |
| 3 | 57.79 | 6.86 | | 5.99 | 7.01 | 4.43 | 2.92 | −2.20 | −4.32 | −6.58 | −7.96 |
| 2 | 62.78 | 6.64 | | 6.79 | 7.79 | 5.19 | 3.69 | −2.18 | −4.41 | | −7.74 |
| 1 | 65.87 | 6.46 | | 7.42 | 8.42 | 5.77 | 4.34 | −2.20 | −4.40 | | −7.56 |

| Stn | Half-breadth at A | B | C | D | Greatest (main breadth) | Its height above A | At the rail |
|---|---|---|---|---|---|---|---|
| 12 | 3.86 | 0.45 | | | 7.13 | +3.46 (top of the row read) | 7.13 |
| 11 | 6.10 | 1.78 | 0.51 | | 7.91 | +3.63 (the same) | 7.91 |
| 10 | 7.33 | 3.72 | 1.23 | | 8.48 | +3.26 | 8.48 |
| 9 | 8.53 | 6.23 | 2.44 | 1.02 | 9.26 | +2.67 | 9.13 |
| 8 | 9.51 | 8.06 | 4.40 | 1.55 | 9.88 | +2.66 | 9.74 |
| 7 | 10.44 | 9.52 | 6.75 | 2.49 | 10.58 | +1.79 | 10.39 |
| 6 | 10.85 | 9.97 | 7.71 | 3.15 | 10.94 | +1.42 | 10.71 |
| 5 | 10.33 | 9.07 | 6.15 | 1.75 | 10.58 | +2.22 | 10.36 |
| 4 | 9.06 | 7.25 | 3.73 | | 9.88 | +2.78 | 9.70 |
| 3 | 6.82 | 4.32 | 1.85 | | 8.42 | +4.65 | 8.22 |
| 2 | 3.56 | 1.93 | 0.80 | | 6.15 | +5.39 | 6.09 |
| 1 | 1.60 | 0.83 | | | 3.86 | +6.36 | 3.86 |

A ends square on the tuck, about 1.7 ft half-breadth at about 1.6 ft from AP, and comes in forward to
about 0.45 ft at about 68.2 ft from AP, past the last station and short of the stem (measured).

**The sections as read from the body plan**, half-breadth in ft at each height in ft above A; the
curves are read from 6 px rows and each height interpolated; station 6 is the mean of its two
halves. Upper parts past the transom's lower edge are not read.

| Stn | +6 | +5 | +4 | +3 | +2 | +1 | +0 | −1 | −2 | −3 | −4 | −5 | −6 | −7 | −8 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 |  |  |  | 7.02 | 6.53 | 5.63 | 3.86 | 1.92 | 0.57 |  |  |  |  |  |  |
| 11 |  |  |  | 7.84 | 7.60 | 7.06 | 6.10 | 4.16 | 2.08 | 1.01 | 0.68 |  |  |  |  |
| 10 |  |  |  | 8.46 | 8.34 | 7.99 | 7.33 | 6.17 | 4.13 | 2.30 | 1.46 | 1.03 | 0.46 |  |  |
| 9 |  |  | 9.13 | 9.25 | 9.18 | 8.96 | 8.53 | 7.79 | 6.54 | 4.62 | 2.98 | 1.90 | 1.14 | 0.83 | 0.39 |
| 8 |  |  | 9.78 | 9.86 | 9.85 | 9.77 | 9.51 | 9.09 | 8.28 | 7.00 | 5.15 | 3.45 | 2.11 | 1.21 |  |
| 7 |  |  | 10.39 | 10.51 | 10.58 | 10.55 | 10.44 | 10.10 | 9.61 | 8.74 | 7.44 | 5.67 | 3.49 | 1.77 |  |
| 6 |  | 10.60 | 10.79 | 10.88 | 10.93 | 10.94 | 10.85 | 10.56 | 10.09 | 9.36 | 8.26 | 6.62 | 4.38 | 1.98 |  |
| 5 |  | 10.32 | 10.46 | 10.55 | 10.56 | 10.53 | 10.33 | 9.89 | 9.24 | 8.28 | 6.88 | 4.97 | 2.80 |  |  |
| 4 |  | 9.72 | 9.79 | 9.86 | 9.76 | 9.51 | 9.06 | 8.42 | 7.44 | 6.13 | 4.37 | 2.72 | 1.30 |  |  |
| 3 | 8.22 | 8.40 | 8.38 | 8.26 | 8.01 | 7.55 | 6.82 | 5.82 | 4.60 | 3.34 | 2.20 | 1.27 |  |  |  |
| 2 | 6.13 | 6.14 | 6.01 | 5.70 | 5.16 | 4.43 | 3.56 | 2.78 | 2.03 | 1.47 | 0.96 | 0.58 |  |  |  |
| 1 | 3.85 | 3.70 | 3.39 | 2.91 | 2.45 | 1.97 | 1.60 | 1.21 | 0.88 | 0.60 |  |  |  |  |  |

**Station 6, the section as read**, [height above A, half-breadth], the mean of the two halves:
[−7.54, 0.95], [−7.01, 1.95], [−6.48, 3.18], [−5.96, 4.50], [−5.43, 5.73], [−4.90, 6.82],
[−4.37, 7.74], [−3.85, 8.48], [−3.32, 9.06], [−2.79, 9.55], [−2.27, 9.93], [−1.74, 10.25],
[−1.21, 10.49], [−0.69, 10.68], [−0.16, 10.83], [0.37, 10.91], [0.90, 10.94], [1.42, 10.94],
[1.95, 10.94], [2.48, 10.92], [3.00, 10.88], [3.53, 10.83], [4.06, 10.78], [4.58, 10.68],
[5.11, 10.58]. **Deadrise 25°** from the rabbet to 3.6 ft above it, straight; then the bilge. The
floors are hollow at the garboard only aft of station 9.

### 11.5 The plate (Chapelle p. 7) by station (measured)

Heights ±0.05 ft above WL1, half-breadths ±0.05 ft; the half-breadths at WL1 to WL5 by the plan's
five solid curves, whose centre line is the plan's lower line, and the outline by its two inverted
lines, whose centre line is its upper line, the sheer's base (read). Three dashed curves are
diagonals, not read. There is no body plan on the page.

| Stn | ft from the perpendicular | WL1 above the rabbet | Rail | Cap | Wale top | Wale foot | Deck | HB WL1 | WL2 | WL3 | WL4 | WL5 | Outline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 11 | 9.95 | 8.25 | 6.20 | | 4.61 | 3.24 | | 5.39 | 2.53 | 1.32 | 0.88 | 0.48 | 8.06 |
| 10 | 15.53 | 8.07 | 5.74 | | 4.15 | 2.80 | | 7.94 | 5.83 | 3.37 | 1.88 | 0.90 | 9.10 |
| 9 | 20.98 | 7.89 | 5.42 | | 3.81 | 2.50 | 4.67 | 9.19 | 8.00 | 5.88 | 3.37 | 1.55 | 9.78 |
| 8 | 26.55 | 7.69 | 5.21 | 6.56 | 3.56 | 2.28 | 4.59 | 9.96 | 9.14 | 7.83 | 5.22 | 2.40 | 10.32 |
| 7 | 32.19 | 7.53 | 5.11 | 6.40 | 3.46 | 2.16 | 4.47 | 10.45 | 9.72 | 8.69 | 6.37 | 3.01 | 10.57 |
| M 6 | 37.73 | 7.34 | 5.13 | 6.36 | 3.48 | 2.16 | 4.55 | 10.59 | 9.95 | 8.78 | 6.63 | 3.22 | 10.66 |
| 5 | 43.37 | 7.17 | 5.22 | 6.48 | 3.58 | 2.29 | 4.67 | 10.41 | 9.68 | 8.36 | 5.96 | 2.76 | 10.56 |
| 4 | 48.97 | 6.99 | 5.46 | 6.75 | 3.80 | 2.50 | 4.83 | 9.65 | 8.76 | 7.03 | 4.52 | 1.84 | 10.16 |
| 3 | 54.55 | 6.81 | 5.82 | 7.11 | 4.18 | 2.84 | 5.05 | 8.17 | 6.86 | 4.95 | 2.81 | 1.09 | 9.29 |
| 2 | 60.21 | 6.61 | 6.36 | 7.75 | 4.77 | 3.45 | | 5.57 | 4.05 | 2.53 | 1.23 | 0.57 | 7.55 |
| 1 | 65.78 | 6.40 | 7.08 | 8.52 | 5.53 | 4.17 | | 1.91 | 1.34 | 0.74 | 0.42 | 0.16 | 4.56 |

Stations 1.70 m apart, 5.57 ft. "M" at 6 is the plate's mark for the midship frame (read). The keel
below the rabbet line, 1.05 ft, to the base.

### 11.6 The stem, post, keel, decks and wale (measured)

- **The stem.** ZAZ6170's fore edge, ft forward of FP, above A: 1.27 at +10.3 and +5.0; 1.17 at
  +1.5; **1.03 at the line**; 0.68 at −2.0; 0.40 at −2.9; 0.04 at −3.8; −0.36 at −4.7; −0.97 at
  −5.6; −1.78 at −6.5; −2.79 at −7.3, where the strip takes it. It is plumb above about +4 ft. Its
  rabbet, a heavy double line, stands 1.55 ft abaft the fore edge at the line and meets the keel at
  station 2. The plate's fore edge rakes about 2° above the line, once the page's warp is taken off
  ("slightly raking ends": Chapelle). The stem's head stands 11 ft above A on ZAZ6170 and 9.8 ft
  above WL1 on the plate, past the rail: a plain timber, squared off, with the bowsprit's stump at it
  and no knee.
- **The post.** ZAZ6170's heavy after edge rakes **20.6°**, 0.40 ft from AP at A; its fore edge,
  thinner, 1.87 ft from AP at A, rakes 24.7°, the post widening toward its foot; the plate's 24.9°.
  The plate's after edge is 20.3° (the two within 0.3°). The
  rudder's after edge on ZAZ6170 is 1.32 ft abaft AP at A, raking 14.3°.
- **The keel.** Level to the page on both. On ZAZ6170 the strip hides its lower edge in the sheer;
  the body plan and the midship section give it 12.5 px, 1.10 ft, under the base; the plate 1.05 ft.
  So **9.07 ft from A to the keel's lower edge at station 6**, 10.72 at station 12, 7.74 at station
  2. Half-siding 0.37 ft. The rudder's foot stops 0.3 ft above the keel's lower edge.
- **The decks.** On ZAZ6170's midship section the deck's upper side stands +3.76 ft above A at the
  middle line and +3.40 at the side (round up 4¼ in), the rail's top +4.40 (the sheer's +4.42). In
  the sheer its two red lines are the same two within about 0.1 ft. The hold's red line, the
  keelson's top, is −5.56 ft in the sheer and −6.1 ft on the midship section (the two within 0.6
  ft). Forward the deck runs to the stem; aft, a bulkhead stands about 19 to 21 ft from AP on both
  sheets, and abaft it a raised quarterdeck, 1.4 ft above the main deck on the plate and about 1½ ft
  on ZAZ6170 (tentative), to the transom. The plate's dashed deck is 4.55 ft above WL1 at station 6,
  and the same place on ZAZ6170 is within 0.1 ft of it once A's 0.64 ft above WL1 is taken off.
- **The wale.** One band: top +2.88, foot +1.42 ft above A at station 6 on ZAZ6170 (1.46 ft deep),
  the foot a heavy line; on the plate 3.48 and 2.16 above WL1 (1.32 ft deep). Below the deck, unlike
  *Éclair*'s band (§5.1). No channel wale.

### 11.7 The half-ports and the masts (read; measured)

The rail carries raised panels with gaps between them, Chapelle's "half ports" (OCR l. 506); four
gaps a side, for eight guns (read, count). Each gap is a port whose sill is the rail's top, 1.0 ft
above the deck at side; a triple needs the rail taken at the panels' cap, since the schema refuses a
sill at the rail.

| Port | ZAZ6170: ft from AP | Sill above A | Half-breadth at the sill | The plate: ft from the perpendicular | At her scale, a triple on her side (T): x, sill, half-breadth |
|---|---|---|---|---|---|
| 1 | 26.15 | 4.41 | 10.39 | 25.17 | −2.26, 1.23, 3.00 |
| 2 | 34.76 | 4.40 | 10.71 | 35.65 | +0.02, 1.23, 3.01 |
| 3 | 43.28 | 4.66 | 10.38 | 46.04 | +2.27, 1.30, 3.00 |
| 4 | 52.24 | 5.29 | 9.60 | 56.43 | +4.65, 1.47, 3.01 |

Widths 1.9 to 2.1 ft on both; the panel's cap 1.0 ft above the sill on ZAZ6170, 1.2 to 1.4 ft on the
plate. The sills at her scale fall below her waist rail (1.49 to 1.66 m), and the cap's height at
her scale is about her rail's (§13.2). The plate's gaps stand 10.4 ft apart and ZAZ6170's 8.7 ft:
the largest difference between the sheets.

**The masts**, at the rail: main, ZAZ6170 32.1 ft from AP, 0.466 of the range, raking 4.3° on its
stump; the plate 33.8 ft, raking 6.2°. Fore, ZAZ6170 62.1 ft, 0.902; the plate 63.9 ft, plumb within
1°, and 1.5° on ZAZ6170's stump. Mizen, the plate and p. 6 only: a raked stump at the taffrail, none
being drawn on ZAZ6170 (as fitted for a schooner, catalogue).

### 11.8 The stern and the head

**The stern**, ZAZ6170 (read; measured; the stern board on the body plan). A square tuck: the
transom's foot, the knuckle, about 3 ft above A at the post, the arch of its top about 8.6 ft, raked
32° aft on the sheer. In the plan its half-breadth is 5.2 ft at the top and 5.8 ft at the knuckle;
on the stern board 6.3 ft at its greatest. Four lights across it, two a side of the arms, each about
1.4 ft wide and 1.75 ft deep, within 2.1 and 5.4 ft of the middle line, about +4.7 to +6.5 ft above
A at the post; the name "LE COUREUR" on the counter under them; a rail on turned posts above the
transom, to about 9.9 ft above A (read). No gallery. The plate has no stern view; its post, knuckle
and transom agree in plan within 0.1 ft of half-breadth at the top. **The head:** none (§11.6).

### 11.9 Sheet against sheet (measured)

Both sheets' half-breadths, at the same height above the keel's rabbet and the same place along the
ship, at the plate's stations and WL1 to WL5, 50 points:

| Shift along the ship | Mean, ZAZ6170 less the plate | Rms | Largest | Abaft / before the middle |
|---|---|---|---|---|
| none | +0.11 ft | 0.40 ft | 1.03 ft | +0.45 / −0.19 |
| **1.0 ft** | +0.10 ft | **0.19 ft** | 0.45 ft | +0.19 / +0.02 |
| 1.6 ft | +0.09 ft | 0.21 ft | 0.64 ft | +0.01 / +0.15 |
| 1.9 ft | +0.08 ft | 0.28 ft | 0.81 ft | −0.08 / +0.22 |

The masts register the sheets at 1.7 and 1.8 ft, the post at 1.5 ft and the stem's rabbet at 0.7 ft
(the plate forward of ZAZ6170, on its own frame). So: **one hull**, ZAZ6170 a little fuller aft than
the plan approved in 1775, the plate 2.6% narrower. Length within 0.2%, wale within 0.15 ft, rail
and deck within 0.1 to 0.3 ft once the two load lines are allowed for, the post's rake within 0.3°;
the half-ports up to 4 ft apart forward. ZAZ6170 is taken as the ship and the plate as a check on
it, since it is the ship as she was, with stated dimensions and a body plan (judgement).

## 12. *Defender*, late *Bonne Marseillaise*

**Frame in this section.** ft forward of **AP**, the post's after side at the deck, px 340 of
ZAZ4734 (§12.1); heights in ft above the green line at the place; half-breadths off the middle line.
Her stations' marks cannot be read at this resolution, so each is named by its column on the image.

### 12.1 The dimensions and the scales (read, tentative; measured)

- **The title** (read): "A Draught of H. M. Lugger Defender, late Bonne Marseillaise, as taken off
  in Sheerness Yard April 1810". Length on the main deck from the after side of the stem to the
  after side of the post, about 65 ft (the inch figure not read); keel for tonnage not legible;
  breadth extreme 17 ft 2¾ in; moulded 17 ft 0 in; depth in hold 7 ft 4 in (the digits read
  tentatively, the 17s by the measure below); burthen not legible. The rule on a keel of about 56 ft
  gives about 89 tons (judgement: arithmetic).
- **ZAZ4734's strip**: **13.00 px to the foot**, 70 ft (10, 50 and 10 by fives), so 1.365 px/mm at
  1:32; the paper 1,274 x 457 px comes to 933 x 335 mm against 927 x 336 mm (+0.6%, −0.3%). The
  title's "By a ⅜ Scale" (read).
- **Measured back**: 64.85 ft from the post's after side to the stem's after side at the deck (843
  px); the body plan's rectangle 17.14 ft (222.8 px), between the moulded and the extreme; 7 ft 0 in
  at the side from the deck to the hold's floor line, with the round up about the stated 7 ft 4 in.
- **ZAZ4735's strip**: **12.55 px to the foot**, 72 ft, "By a ¼ Scale" (read), 1:48 as catalogued.
- **ZAZ4736** has no strip. Its title reads "By a ⅜ Scale" and its masts stand at 16.4 to 16.5 px to
  the foot, against the two other sheets' spacing, which at 1.719 px/mm is **1:32, and the
  catalogue's 1:48 is a slip**.
- **Sheet against sheet**: main to fore 25.55 ft on ZAZ4735 and 25.6 on ZAZ4734; mizen to main 24.75
  and 25.1; the deck's greatest half-breadth 8.42 (ZAZ4734), 8.35 (ZAZ4735), 8.43 (ZAZ4736); the
  eight ports' spacing on the plan within 0.2 ft of ZAZ4734's.

### 12.2 The line

One green line, straight: 205.0 at px 387, 234.5 at px 1114, falling **2.32°** to the level part of
the keel (measured). Taken off in a yard, before fitting: **a light line** (judgement). Her
displacement to it, moulded, is 1,555 ft³, 44 tons, about half her burthen; the same reckoning gives
Le Coureur 0.93 of hers (§11.3). It is taken as not her load line.

### 12.3 By station (measured; ±0.1 ft)

| Column | ft from AP | Line above the keel's rabbet | Rail | Deck | Wale foot | Half-breadth at the line | Plan's outline | Greatest | Its height above the line |
|---|---|---|---|---|---|---|---|---|---|
| 420 | 6.13 | 6.04 | 5.88 | 3.85 | 2.98 | 1.57 | 5.23 | 5.18 | +3.35 |
| 485 | 11.13 | 5.74 | 5.65 | 3.64 | 2.71 | 3.57 | 6.12 | 6.08 | +3.18 |
| 550 | 16.15 | 5.54 | 5.42 | 3.43 | 2.48 | 5.41 | 6.96 | 7.04 | +3.85 |
| 615 | 21.15 | 5.33 | 5.33 | 3.28 | 2.38 | 6.59 | 7.60 | 7.70 | +3.83 |
| 680 | 26.18 | 5.13 | 5.35 | 3.31 | 2.37 | 7.35 | 8.00 | 8.19 | +3.33 |
| 745 | 31.16 | 4.93 | 5.41 | 3.54 | 2.44 | 7.76 | 8.35 | 8.35 | +1.68 (top of the rows read) |
| 810 | 36.16 | 4.65 | 5.52 | 3.76 | 2.64 | 7.86 | 8.42 | 8.58 | +3.27 (a flat run) |
| 875 | 41.16 | 4.36 | 5.88 | 4.06 | 2.94 | 7.49 | 8.26 | 8.30 | +2.09 (the same) |
| 940 | 46.17 | 4.00 | 6.27 | 4.38 | 3.33 | 6.58 | 7.87 | 7.95 | +4.02 |
| 1005 | 51.16 | 3.54 | 6.77 | 4.90 | 3.81 | 5.06 | 7.04 | 7.17 | +5.02 |
| 1070 | 56.19 | 2.93 | 7.47 | 5.35 | 4.47 | 2.62 | 5.90 | 5.85 | +5.48 |
| 1114 | 59.54 | 1.97 | 7.88 | 5.81 | 4.96 | 1.10 | 4.40 | 4.66 | +5.60 |

**The sections as read from the body plan**, half-breadth in ft at each height in ft above the line.
The curves are named by their half-breadth at the line against the half-breadth plan; two further
curves abaft column 420 are not read.

| Column | +5 | +4 | +3 | +2 | +1 | +0 | −1 | −2 | −3 | −4 | −5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 420 |  |  | 5.04 | 4.17 | 2.51 | 1.57 | 1.04 | 0.74 |  |  |  |
| 485 |  |  | 6.04 | 5.58 | 4.78 | 3.57 | 2.45 | 1.55 | 0.91 |  |  |
| 550 |  |  | 6.93 | 6.70 | 6.18 | 5.41 | 4.19 | 2.89 | 1.78 | 0.89 |  |
| 615 |  | 7.70 | 7.64 | 7.50 | 7.16 | 6.59 | 5.68 | 4.45 | 2.92 | 1.42 |  |
| 680 |  | 8.16 | 8.18 | 8.08 | 7.84 | 7.35 | 6.60 | 5.46 | 3.87 | 1.94 |  |
| 745 |  |  |  |  | 8.20 | 7.76 | 7.25 | 6.16 | 4.54 | 2.10 |  |
| 810 | 8.49 | 8.55 | 8.58 | 8.54 | 8.31 | 7.86 | 7.28 | 6.21 | 4.50 | 2.00 |  |
| 875 |  |  |  | 8.28 | 8.01 | 7.49 | 6.78 | 5.60 | 3.47 |  |  |
| 940 | 7.91 | 7.94 | 7.88 | 7.66 | 7.25 | 6.58 | 5.58 | 3.87 | 1.87 |  |  |
| 1005 | 7.16 | 7.07 | 6.90 | 6.62 | 5.96 | 5.06 | 3.64 | 2.03 | 0.71 |  |  |
| 1070 | 5.79 | 5.62 | 5.26 | 4.76 | 3.88 | 2.62 | 1.47 | 0.62 |  |  |  |
| 1114 | 4.22 | 3.92 | 3.42 | 2.71 | 1.86 | 1.10 | 0.51 |  |  |  |  |

**The midship section**, column 810, [height above the line, half-breadth]: [−4.58, 0.52],
[−4.12, 1.68], [−3.65, 2.96], [−3.19, 4.10], [−2.73, 5.06], [−2.27, 5.85], [−1.81, 6.47],
[−1.35, 6.98], [−0.88, 7.38], [−0.42, 7.71], [0.04, 7.88], [0.50, 8.13], [0.96, 8.29], [1.42, 8.46],
[1.88, 8.54], [2.35, 8.56], [2.81, 8.57], [3.27, 8.58], [3.73, 8.55], [4.19, 8.55], [4.65, 8.50],
[5.12, 8.48]. Deadrise 20° to 24°.

**The body plan's half-breadths and the half-breadth plan's** agree within 0.2 ft at the green line.
The rail is raised aft to px 526, 14.3 ft from AP, where it ends in a scroll (read). The heavy lower
black line is the foot of a wale band, as Le Coureur's, below the deck; its top a faint line about
0.8 ft above it. One flush deck from the post to the stem (read; ZAZ4736), the rail's raised after
part over the cabin, a platform below.

### 12.4 The stem, post, keel and stern (measured; read)

- **The stem** rakes and curves: its faint fore edge 14° at the line and above, 1.9 ft before the
  heavy rabbet at the line. **The post**: after edge raking **11.6°**, fore edge 14.1°; the
  rudder's after edge 8.1°. **The keel** is level on the page to about 33 ft from AP and rises from
  there to the stem in a long curve; its lower edge 1.18 ft under the rabbet line (the body plan).
- **The floor**: the hold's red floor line 3.2 to 3.5 ft below the line amidships. **The masts**, at
  the deck: mizen 5.7 ft from AP (0.087 of her length), main 30.8 ft (0.475), fore 56.4 ft (0.870),
  plumb on the sheet.
- **The stern** (read, tentative): a narrow transom, 3.3 ft a side at the top in the plan, on a
  round-topped counter whose foot is about 4.6 ft above the line; a round port on one side of the
  stern board; no lights or gallery shown. **No head:** a plain stem head.

### 12.5 Her ports (read; measured)

**As taken off, ZAZ4734**: eight a side, each 1.56 ft wide and 1.22 ft deep, the sill about 0.4 ft
above the deck, the top close under the rail; the plan ZAZ4736 shows the same eight.

| Port | Column | ft from AP | Sill above the line | At her length factor (0.953) and her deck, a triple on her side (T): x, sill, half-breadth |
|---|---|---|---|---|
| 1 | 458 | 9.05 | 4.27 | −6.69, 1.19, 2.63 |
| 2 | 549 | 16.08 | 3.96 | −4.65, 1.02, 2.95 |
| 3 | 641 | 23.15 | 3.86 | −2.60, 0.91, 3.03 |
| 4 | 726 | 29.69 | 3.89 | −0.70, 0.87, 3.04 |
| 5 | 811 | 36.23 | 4.17 | +1.20, 0.88, 3.04 |
| 6 | 903 | 43.31 | 4.63 | +3.25, 0.93, 3.06 |
| 7 | 987 | 49.77 | 5.19 | +5.13, 1.06, 3.00 |
| 8 | 1077 | 56.69 | 6.00 | +7.14, 1.28, 2.45 |

The last column keeps her own deck at side and adds the 0.4 ft unscaled (T).

**As proposed, ZAZ4735**: four a side for eight carronades, its title reading that the black lines
show the height required for carronades on the recoil and the green for the non-recoil (read, words
at the limit of the image). Each 2.6 ft wide; the sill by the black line 0.78 to 1.0 ft above the
deck, by the green 0.53 to 0.75 ft; 1.92 ft deep to the rail's foot. Ports at 13.2, 24.4, 36.7 and
48.0 ft from AP (±0.3, registered on the masts), which at her length factor are 11.6, 22.3, 34.0 and
44.8 ft from her AP: the middle two fall in her waist, clear of her ladder and hatches, and §6.4
takes them. The section shows both carronades on slides at the side (read).

### 12.6 The masting table (read, tentative)

For a later reader of the rig, length and diameter as far as they can be read: main mast about 58
ft, topmast 30 ft, yard 40 ft 6 in, boom about 20 ft 3 in, gaff about 29 ft; fore mast 51 ft, yard
40 ft 2 in, fore boom yard 20 ft 3 in; mizen mast 37 ft 3 in, topmast 17 ft, yard 25 ft and a
figure, boom 20 ft 3 in, gaff 17 ft 6 in; bowsprit 35 ft 6 in. Nothing here moves a spar of the
file.

## 13. How far they stand for her

### 13.1 Is Le Coureur her type?

**Yes (judgement, on the measures below).** Both are French luggers with a stepped or panelled rail
and a stem standing about a foot before the perpendicular; Chapelle calls Le Coureur a lugger of the
chasse-marée type, and the file calls *Éclair* one. *Éclair*'s floor is not drawn, so the sharp floor
is no likeness of theirs but what the stand-in lends her. The differences: twenty years; a vessel
built to the Marine's order, of 138 tons, against one of 101; length to breadth 3.08 against 2.91;
depth in hold to breadth 0.44 against 0.34; a square stern against a round one; a wale below the deck
against a band above it; and a post of 20.6° against about 10°.

*Defender* is the same family again, taken in 1809, fourteen years after *Éclair*: 3.8 to 1 in
length to breadth, longer and narrower than either, on a light line.

### 13.2 The measures beside her own sheet

Each at the factor that brings her moulded breadth to 20 ft 0 in: Le Coureur 0.9135, *Defender*
1.167.

| Check, ft unless marked | Her sheet (§3 to §5) | Le Coureur at the factors | *Defender* at the factors |
|---|---|---|---|
| Stem's fore edge before FP, at the water | 0.90 | 0.89 (1.03 × 0.868) | none: her stem rakes (§12.4) |
| Forefoot aft of the fore edge at the water, 3.62 down | 0.98 (dashed) | 0.91 | 1.33 |
| The same, 5.53 down | 3.09 (dashed) | 2.08 | 2.15 (at 5.4) |
| Post's rake to the line, above and below the water | about 10° (9.6° and 10.8°) | 20.6° | 11.6° |
| Hold's floor line below the water, amidships | 3.52 | 5.08 | 3.8 to 4.0 |
| Keel's lower edge below the water, amidships | 6 to 6½ (judgement, §4) | **8.3** | 6.8 |
| Deck at side above the water | 2.44 | 3.11 | 4.39 |
| Rail above the water, amidships | 4.92 | 4.04, and the panel's cap 4.98 | 6.44 |
| Half-breadth at the water, amidships, plank on | not given | 10.08 | 9.34 |
| Rail's half-breadth over its greatest, at 0.211 of the length from AP | 0.95 | 0.86 | 0.78 |
| Rail's half-breadth over its greatest, at 0.928 of the length | 0.69 | 0.49 | 0.49 |
| Water's fall to the keel | 1.05° to the page (the keel not drawn) | 2.9° | 2.32° |
| Displacement to the line at her size, moulded | the file's 101 t (judgement there) | 95 t; 101 t as drawn with plank and keel (§6) | 59 t |

**What it shows (judgement).** Above the water her own sheet stands, and needs nothing. Under it: the
forward part of Le Coureur's stem is hers down to about 4 ft below the water, and then *Éclair* cuts
away more. *Defender*'s depth and post are the nearer to hers, and her light line is not a line a ship
loads to. Le Coureur at one factor draws 101 t at her sheet's length and at 2.53 m, against a filed
101 t reckoned on 16.8 m and 2.1 m: the agreement is partly a coincidence, longer and deeper cancelling
a finer hull (Cb 0.343 against the file's judged 0.45). Le Coureur's line, at a place on the side
about like *Éclair*'s green line in proportion to her hold (0.60 up from the keelson's top to the
deck, against her 0.55 and *Defender*'s 0.45), is taken as a load line.

### 13.3 The rungs

- **S† from Le Coureur (ZAZ6170), by principle 7:** the sections and half-breadths under the water,
  from station 12 to station 1, the water's half-breadths, the midship section below the water, and
  the height of the main breadth.
- **T, where she cannot stand:**
  - **The depth.** Drawn 2.53 m at the middle, 2.98 m at the heel and 2.18 m at the forefoot,
    against the file's 2.1 m mean (8 ft 6 in aft, 5 ft 6 in forward), and about 2.0 m from her own
    hold (judgement). It is recorded, never moved. The band that 15° of heel lifts out of the water
    reaches about 0.8 m below it; there the stand-in's half-breadth is 2.68 m, and *Defender*'s at
    her factor 2.14 m, which is the nearer if her hold is true to her keel (judgement). The
    difference is the largest doubt in this drawing.
  - **The drag.** Le Coureur's is kept (drawn 3.0°), against her green line's 1.05° to the page
    (§6.2).
  - **The ends at the rail.** Her plan is fuller than Le Coureur's at both ends, so the main
    breadth's half-breadth is her own plan's (§6.3), and the water's half-breadths under it are Le
    Coureur's: her side flares out from the water to the rail by up to 0.5 m aft and 1.2 m forward
    (measured), which her own plan requires and no sheet of her confirms.
  - **The side between the water and her main breadth** (§6.2): Le Coureur's curve moved to meet her own
    plan's breadth. The points above the water in `sections_m` are this, and no sheet of her draws it.
  - **The water's two ends** (§6.1): the three half-breadths aft of −8.75 and the two at +8.97 and
    +8.99, the line closed to her post and the stem's fore edge. Le Coureur's A ends square on her
    tuck (§11.4), and *Éclair* is round.
  - **That B to C is her wale** (§6.1): its heights are hers; that it is the wale §5.1 means is not
    on the sheet.
- **Not hers, S kept from her own sheet:** the stern (round), the post (about 10°), the stem above
  the water and the forefoot's dashed line, the head (none), the band's heights, the rail and its
  steps, the deck, the masts' places.
- ***Defender* is a check, not the stand-in.** On a light line and at 3.8 to 1, she would draw 59 t
  and a water half-breadth 0.2 m narrower. She supports the post's rake and the shallow hold, and
  gives the only sill heights a lugger's fitting states.
- **Chapelle's "great deadrise"** is measured: 25° (ZAZ6170), 23° to 29° (the plate), 20° to 24°
  (ZAZ4734), and the §5.7 row moves from T to S† (ruled, §13.4). **Plainly:** this is her type's, not
  hers; the note's word for it is the stand-in's, and her own sheet still has no body.

### 13.4 Ruled by the lead (2026-10-31)

- **The depth: the one factor of principle 7, 2.53 m, as built.** The other ways, recorded: a smaller
  factor on the heights below the water alone, 0.78 to fit the file's draught (drawn 2.16 m, floor about
  22°, 87 t, −14%, inside the 15%), or 0.70 to fit her own hold's 6½ ft (drawn 1.94 m, floor about 20°,
  78 t, −23%). Measured through the tree's form in the scratch directory, every z below the water
  scaled. **The hold's floor line is a depth of hold and no draught, and is not the measure** (§4,
  §13.2). `Build-Ships.md` §5.7's row moves from T to S† under the water.
- **The length: her sheet's, a departure from principle 7's last sentence, said here.** Her line is
  18.33 m (60.14 ft, the re-read of §5.3), 9.1% over the file's 16.8 m; the beam kept. By the sentence's
  words the length factor would be **0.793**, beside the 0.868 of §6.2, and her own rail, plan and stem,
  S, would not stand on it, so S is kept (principle 5); the masts stay inside the drawn hull. The lead's
  note of 2026-10-31 quotes 18.39 m, the first reading's 60.32 ft: the re-read is 18.33 m, and the
  stations stand as first measured (§6.2).
- The ports: as built, none (§6.4), by the lead's point 5.
- The bowsprit's rating: left at 21.8 kN and reported, a tuning pass's (§7), by the lead's point 9.
