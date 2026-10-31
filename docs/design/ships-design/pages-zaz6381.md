# Pages: RMG ZAZ6381 and its fellows, the cutter *Sherbourne* of 1763 (October 2026)

Research for package 75's hull step, SW-2 with SW-2b.2 (`Build-Ships.md` §5, §5.7, §5.9). It serves
`data/ships/cutter.yaml`: the hull's profile and its shape keys, each line's rung by §5.0, and the
port triples of §5.4. No figure the physics or the guns read moves (§5.0 principle 8, §5.6); §7
records where the file and the sheets differ. Facts only: the images are the museum's photographs,
kept outside the repository (§1.1).

The marks:

- **read**: the sheet's writing or drawing was seen on the image. "tentative" is a reading at
  the limit of the image.
- **catalogue**: from the museum's catalogue entry only.
- **measured**: off the image at the scale of §3; the uncertainty is stated.
- **judgement**: reasoning by this note.

"As built" names a figure off the CHN sheets, or ZAZ6381's measure moved by them.

**Units and datums.** English feet and inches, with metres where the file takes them. Positions
along the ship are feet forward of **AP**, the after of the two red perpendiculars on the sheer,
whose distance apart is the length on the range of the deck (§3.2); in metres they are given from
**mid**, the middle of the load waterline rabbet to rabbet, 27.16 ft forward of AP, positive
forward, the profile's `x`. Heights are feet above **WL1**, the top green line, taken as the load
line (§4), at the same station, positive up, the profile's `z`. Half-breadths are moulded, without
plank, unless a list in §6 says "with plank". The stations are read as the sheet writes them: 17,
16, 14, 12, 10, 8, 6, 4, 2, O, B, D, F, H, K, M.

**A shear, not a turn.** WL1 lies 3.24° to the page and 3.12° to the keel, far more than the
1.05° of ZAZ6306. As `tools/ships/indefatigable.py` takes her frame, `x` here stays along the page
and `z` is the height above the line at that `x`. Turning the ship until WL1 is level would move
a point aft by z x 0.057: the taffrail 0.33 ft (10 cm), the stem head 0.52 ft (16 cm), and the post's
heel forward 0.57 ft (17 cm); the rakes in §5.6 and §5.9 are given both ways (judgement: the shear
kept, a matter of 1 to 5 px in the owner's picture; for the builder to weigh).

## 0. In brief

- **The scale checks.** The strip gives 15.687 px to the foot along the page over 59 feet (rms
  0.39 px). The two red perpendiculars stand 54 ft 6.1 in apart against the sheet's 54 ft 6 in; the
  body plan's moulded breadth of 18 ft 7 in with 2½ in of plank a side comes to the sheet's 19 ft 0 in
  (§3.2). Heights across the page run 1% small (15.536 px to the foot; four checks, §3.3), and are
  corrected.
- **The load line is the top green line, WL1** (judgement, on measures). Taken to WL1 she displaces 107 tons (109 t) against the file's 106 t; to the second line 54 tons, less than her 85 tons
  burthen. Steel's five-eighths of the top-timber height picks WL1 by itself: 8.4 to 8.7 ft at O against WL1's 8.58 ft and the second line's 6.11 ft. The wale's lower edge comes down to 0.03 ft (⅓ in) above WL1 at its lowest, and the height
  of breadth stands 7½ to 10 in above it amidships, as Steel's rule has them (§4).
- **The first reads' 2 ft between the body plan and the sheer is resolved.** At one station the two views agree: 42 crossings of the three greens, mean +0.02 ft, sd 0.08 ft, largest 0.26 ft,
  the body plan's base being the upper of the keel's two lines. WL1 climbs 3.0 ft along the keel from the
  fore perpendicular to the after, so a read of it at two stations differs by up to that (§4.3).
- **Her deck was raised, and the sheets show it.** The sheet's own note: the deck 3 in higher by
  letter of 21 June 1763 (read). The red deck lines stand 2.6 in (2.3 to 2.9) above a dashed black
  line the whole length (measured). The as-built sheets stand the top of her rail and her sills alike about 5½ in
  higher than ZAZ6381 draws them, the sills landing within 0.1 ft of deck top + 1 ft 3 in at all four
  ports, the sheet's own "should be" (§5.3, §5.8).
- **The sections can be read:** sixteen stations, measured against the half-breadth plan at 47
  crossings of the waterlines, mean -0.02 ft, sd 0.05 ft (0.6 in), largest 0.20 ft, and each cell against the ink of its row, 199 cells, mean 0.00 ft, sd 0.07 ft (§5.7). About 25° of floor.
- **Four ports a side** at -4.75, -2.35, 0.02 and 3.58 m from mid, 1 ft 11 in broad, open up to the rail's
  underside; four sweep ports between; sills as built 1.00 to 1.23 m above the line (§5.8).
- **A square tuck that rounds aft, a short flat counter and a flat transom raked about 20° to the line:** no galleries, no lights, no head
  (§5.5, §5.6). The rough "45°" of §5.9 is the whole stern, wing transom to taffrail, 46.6°.
- **Against the file** (§7, recorded, not moved): WL1 54 ft 1½ in against 50 ft; 3 ft 0 in of drag against 2 ft;
  8 ft 9 in deep at mid to the keel's lower edge against 8 ft 6 in mean; the mast 8 ft 8 in before mid
  against 4 ft 11 in; four ports against three guns a side; the keel for tonnage 44 ft 7 in against
  44 ft 3 in; the sill 1.00 to 1.23 m against 1.5 m, which is 14.5° to 19.4° to shut a port by the
  lee-port rule against 24.3°.

## 1. The source

### 1.1 The objects, the images and the cache

All under `D:/Projects/FreeSail/reference-cache/sherbourne-1763/`; pages read 2026-10-30 at
`https://www.rmg.co.uk/collections/objects/rmgc-object-<number>`, with a generic user-agent.

| Object | Page number | Catalogue | Image, as cached | Size, sha256 |
|---|---|---|---|---|
| ZAZ6381, "Sherborne (1763)" | 86172 | Ship Plans and Technical Records, Admiralty Collections; technical drawing; black, red and green ink; 380 x 510 mm; circa June 1763; 1:48 | `rmg-zaz6381-j7809.jpg` (https://collections.rmg.co.uk/media/2/444/461/j7809.jpg) | 1280 x 949 px; `5d495d4d2f85cbe4a4e2c25a8394442088f4fd33b0dcc33093a044a6a7429157` |
| ZAZ6382, "Sherborne (1763)" | 86173 | as above; black and red ink, pencil; 441 x 477 mm; circa June 1763; 1:48 | `rmg-zaz6382-j7810.jpg` (https://collections.rmg.co.uk/media/2/444/462/j7810.jpg) | 1280 x 1185 px; `256eb43e3a501a329c41946c9cafa337bad90ac0e1ffa17238873621a341d617` |
| CHN0102, "Sherborn [Sherbourne] (1763)" | 387185 | drawing; black and red ink; 502 x 645 mm; 1:48 | `rmg-prints-j8462.jpg` | 1024 x 800 px; `930c909fc0e2e8ecc13a26db66dc58464d9c68cea44e8cdfddfd719ddb2edb7b` |
| CHN0224, "Sherborne [Sherbourne] (1763)" | 387187 | as CHN0102 | `rmg-prints-j8467.jpg` | 1024 x 766 px; `338bf0793744311f64998a91f5e0af1c6577f0d0c663af18a02c1bae4a61ba63` |
| CHN0103, "Sherborn [Sherbourne] (1763)" | 387188 | drawing; black and red ink; 466 x 592 mm; 1:24 | `rmg-prints-j8463.jpg` | 1024 x 808 px; `9ac1ad7ccca0f2ec80404559b37602a009376e5409438b3a92f8894529a4d043` |
| ZAZ6343, "Pitt (1763)", her kin | 86134 | Ship Plans and Technical Records; black and red ink; 377 x 527 mm; circa 1763; 1:48; signed John Williams | `rmg-zaz6343-j0577.jpg` (https://collections.rmg.co.uk/media/413/800/j0577.jpg), fetched for this note | 1280 x 905 px; `5bc933b03c9fdf9a3b9a3494689ee411dbd868449409195bd3a2ffd6f325ec44` |

Also in the folder and read for §2.2: Charnock, *History of Marine Architecture*, vol. III (1802), p. 269, a table of cutters (`charnock-1802-vol3-p269-n323.jpg`, 2326 x 3194 px, `ee355191bfd3fadfa6f7ddeba725323f0a96965b5a827a148595fc87555a5927`): her row only, no drawing.

The CHN images are 1024-px previews, cached earlier in the session; their source address is not
in the cache, the file name's number being RMG's. **Rights** (read on the pages): the ZAZ sheets'
credit is "© Crown copyright. National Maritime Museum, Greenwich, London", with print and image
licensing offered; the CHN sheets' is "National Maritime Museum, Greenwich, London". All are read
and cited, never copied (§5.9 of `Build-Ships.md`).

**What the catalogue says** (catalogue, paraphrased): ZAZ6381 is for building her at Woolwich, a
single-masted 6-gun armed cutter, on the lines of the purchased cutter *Pitt*, with the deck, waist
and windlass altered; ZAZ6382 is her hold with its bulkheads and her deck. CHN0102 and CHN0224 show
her body, inboard profile, half-breadth, upper deck and platforms, their heading "Built at Woolwich
& Launched 3rd December". CHN0103 gives the partial body, the profile at the stern, the transom and
the half-breadth at the stern with a long explanation of the terms and the method, which the catalogue
takes for instruction rather than practice. A manuscript of hers, CHN0105, stands in the same folder
and was not read.

### 1.2 What is on the sheets (read)

- **ZAZ6381:** the body plan; the sheer with inboard works in red, bow to the right, with sixteen
  stations lettered under the keel; a scale strip of about 60 ft, numbered both ways, from the fore end on its upper row, its
  zero on the fore perpendicular, and from the after end on its lower; the half-breadth plan. Three green waterlines in all three views. Two solid red diagonals in the body
  plan, expanded in red in the half-breadth plan, and dashed diagonals not expanded (judgement).
  Top left, a note on the sills and the waist; top right, the deck's note and the dimensions (§2).
- **ZAZ6382:** no strip. The hold and platforms above, the deck below, with the stations lettered on
  the middle line, red beams, hatches, the mast, the windlass; the ports crossed in the side's band.
  Patches of yellowed paper cover part of the hold plan forward.
- **CHN0224 and CHN0102:** the as-built copies: the body plan, with level red lines where ZAZ6381
  has the greens; the sheer and the half-breadth; the upper deck and the platform; a strip of about 60 ft; a
  table of masts and yards (§2.3) and on CHN0224 a note on the hammocks. No inclined waterline.
- **CHN0103:** at 1:24, the stern in profile (stations 17 to 10), in plan, and in two further figures,
  with two blocks of writing, a long paragraph at the lower left and a description of Fig. 3 at the right (§2.4).
- **ZAZ6343:** *Pitt*'s lines, the same three waterlines in red: a check only (§4.2).
- **Not drawn on any of her own sheets:** galleries, stern lights, a knee of the head, a figure, draught marks (*Pitt*'s ZAZ6343 has two lights, §5.6).

## 2. The writing

### 2.1 ZAZ6381 (read)

- Top: "Sherbourn Cutter". Top right, the deck's note: "Deck rais'd 3 Inches & the Draught was sent
  by Ltr 21 June 1763" (tentative after "Inches").
- Top left: "Height of the Port Sills should be 1-3 and not 1-0½ as drawn and height of the waste
  3-2", feet and inches marked over the last figure (tentative at "Height").

### 2.2 The dimensions (read)

| | ZAZ6381 | CHN0224 and CHN0102 | Charnock 1802 |
|---|---|---|---|
| Length on the range of the deck | 54 ft 6 in | 54 ft 6 in | gun deck 54 ft 7 in |
| Of the keel for tonnage | 44 ft 7 in | 44 ft 7 in | keel 42 ft 0 in |
| Breadth extreme | 19 ft 0 in | 19 ft 0 in | 19 ft 0 in |
| Depth in hold | [8] ft 1 in (first figure damaged, tentative) | [8] ft 4 in (first figure tentative) | 8 ft 4 in |
| Burthen | 85 60/94 (tentative) | 85 and a fraction, not read | 86 tons |
| Men, guns, built | | | 31 men; 6 carriage guns, 10 swivels; "Built 1762, Wool. Jos. Harris"; Sir T. Slade |

By the rule, 44 ft 7 in x 19 ft x 9 ft 6 in / 94 = 85 57/94 (judgement, the rule's sum), so the burthen's figure holds
to its last digits' reading. Charnock's "Built 1762" stands against the sheets' 1763 (read), the year her lines were drawn and she was launched; Charnock is a later compiler (judgement). Charnock's 8 ft 4 in settles the as-built depth; ZAZ6381's 8 ft 1 in is 3 in less, the
deck's 3 in (judgement). From the rising line at O (§5.4) the dashed line stands 8.19 ft and the deck's underside 8.41 ft
(measured, a weak check, the ceiling not being drawn).

### 2.3 The masts and yards (read, CHN0224, tentative at 1024 px)

Yards and inches, and inches' diameter: main mast to the pole head 22-10, 17½; topgallant mast 7-20, 6½;
boom 17-3, 10½; spread yard 14-19, 7½; topsail yard 11-9, 7½; gallant yard 9-0, 4½; gaff 10-0, 7½;
topsail gaff 7-24, 4½; cross-jack yard 12-0, 6½; bowsprit 15-24, 13½; flying jib boom 9-15, 6½. A note
below: ringtail boom and studding sail yards and booms of the usual dimensions; the mast head 13 long, which length is included in the pole head (tentative, unit not sure); "She was not fitted
with Hanging Cabbins on the Platform they lay in Hammocks". The drawn mast and bowsprit check it: 16.6 in and
13.7 in across on ZAZ6381 (§5.9).

### 2.4 CHN0103 (read, tentative)

Two blocks of writing. A paragraph of more than a dozen lines at the lower left is headed (tentative where it is marked): "A [Mechanical] Method for Finding the Shape and Taking the Bevelling of a Square Tuck that Rounds Aft". Its opening lines say that a tuck with no round aft is no difficulty, being one raking plane, and that here the plane is oblique, to leave wood for the post's round aft (tentative). A separate block at the right, "Description of Fig. 3", is too small at 1024 px to read but for words here and there. These are the catalogue's very detailed explanation of terms and method: the sheet is explaining this tuck. Its figures carry lettered points. No line is named a load line in the paragraph's first lines; the rest is read only in part (tentative).

### 2.5 The as-built headings (read, tentative at 1024 px)

CHN0224: "Sherborne Cutter, built at Woolwich & launch'd the 3d Dec 1763". CHN0102: "Sherborn Cutter, Built at Woolwich & Launched" and a date in December 1763. Each gives the dimensions of §2.2.

## 3. The scale and its checks

### 3.1 The strip of ZAZ6381 (measured)

- 59 ticks of the strip's one-foot divisions from feet 0 to 59 give **15.687 px to the foot**, rms 0.39 px,
  largest residual 0.99 px. 1 px is 0.064 ft (0.77 in). The strip's edges lie 0.13° to the page.
- **1:48 checked.** At a quarter-inch to the foot the paper's 1263 px across is 511 mm against the
  catalogue's 510 mm.

### 3.2 The stated dimensions measured back

| Dimension | Stated (read) | Measured | Basis |
|---|---|---|---|
| Length on the range of the deck | 54 ft 6 in | **54 ft 6.1 in** (54.51 ft) | the two red perpendiculars, 855.06 px apart, ±0.7 in |
| The same on ZAZ6382 | 54 ft 6 in | 54 ft 6.7 in (54.56 ft) | stern corner to the stem's inner point, at the scale its stations give (§3.4); not independent |
| The same on CHN0224 | 54 ft 6 in | 54 ft 7½ in (54.62 ft) | its own two red perpendiculars, faint, at x 368.3 and 903.9, 535.6 px at its strip's 9.805 px to the foot (57 ticks, rms 0.35 px; a second count of 63 ticks gives the same), ±1.5 in; its stations run 0.2% tighter than its strip |
| Breadth extreme | 19 ft 0 in | **18 ft 7 in moulded** (18.57 to 18.60 ft) | the body plan's box, 291.2 px, and its widest sections, 9.28 to 9.30 ft a side; with 2½ in of plank a side, 19 ft 0 in (judgement on the plank) |
| The same on CHN0224 | 19 ft 0 in | 18 ft 9 in moulded | its body plan's box, 183.7 px, ±1.5 in |
| Keel for tonnage | 44 ft 7 in | 44 ft 1 in as drawn | the post's fore edge at the top of the keel (1.95 ft from AP) to where the stem's rabbet meets it (46.06 ft); the tonnage figure is a rule's, not a drawn length, so a rough check |

### 3.3 Across the page the sheet runs 1% small (measured)

Four checks agree:

- The body plan's half-breadths, along the page, against the half-breadth plan's, across it, at the waterlines:
  a slope of 1.0097 through the origin (47 crossings, rms 0.07 ft).
- The paper's height, 931 px, at the scale so given (15.536 px to the foot) is 380.5 mm against the catalogue's
  380 mm; at the strip's scale it would be 376.9 mm.
- CHN0224's wale's lower edge stands a mean of 0.12 ft higher than ZAZ6381's at the strip's scale, and 0.04 ft at
  this one (§3.4).
- The body plans' base to the heavy level line is 127.7 px on ZAZ6381 and 80.65 px on CHN0224, a ratio of 1.5834, against
  15.536 / 9.805 = 1.5845 and 15.687 / 9.805 = 1.5999.

So **every height and every half-breadth off the plan on ZAZ6381 is at 15.536 px to the foot, and every length
and body-plan half-breadth at 15.687** (±0.3%, at most 0.05 ft on the largest height). Paper shrinking unevenly
(judgement). It moves no height above the line by more than 0.06 ft, and the keel by 0.10 ft. CHN0224's own scale across the page agrees with its strip within 0.1% by the fourth check; CHN0102's and CHN0103's are not tested, and each is taken at its strip.

### 3.4 The sheets against one another (measured)

**ZAZ6381's three views.** Body plan against sheer: §4.3. Body plan against half-breadth plan: §5.7. The
stations of the half-breadth plan stand within 0.9 px (0.06 ft) of the sheer's. They are 3 ft 5½ in apart from 16 to M, with 17 at 1 ft 9 in abaft 16; O is two lines 0.70 ft apart with its letter between them, the tables taking the middle (read, measured).

**ZAZ6382.** It has no strip. Fifteen stations against ZAZ6381's give 16.664 px to the foot (rms 0.70 px), and its
scale is that. On it the outline's half-breadths (§5.7's table, columns on the right) follow ZAZ6381's main breadth
within 0.05 ft from station 17 to F, and fall inside it by 0.10 to 0.24 ft at H, K and M, as a side at the deck
rather than at the main breadth would (judgement). Its ports and sweep ports stand within 0.10 ft of the sheer's (§5.8), its mast
within 0.02 ft (§5.9).

**CHN0224** at its own strip, 9.805 px to the foot (preview, 1 px is 1.2 in): the rail's top above the wale's lower edge, ft:

| St | ZAZ6381, its heavy line | CHN0224, its upper line | Higher as built |
|---|---|---|---|
| 17 | 4.51 | 5.00 | +0.49 |
| 16 | 4.51 | 5.00 | +0.49 |
| 14 | 4.50 | 4.99 | +0.49 |
| 12 | 4.49 | 5.00 | +0.51 |
| 10 | 4.49 | 4.98 | +0.49 |
| 6 | 4.46 | 4.94 | +0.48 |
| 4 | 4.44 | 4.92 | +0.48 |
| 2 | 4.41 | 4.98 | +0.57 |
| B | 4.39 | 4.89 | +0.50 |
| D | 4.39 | 4.91 | +0.52 |
| F | 4.40 | 4.94 | +0.54 |
| H | 4.42 | 4.95 | +0.53 |
| K | 4.42 | 4.92 | +0.50 |
| M | 4.41 | 4.85 | +0.44 |

**Each sheet's rail is a pair of lines, and the ports run up to the lower of the two (read).** On ZAZ6381 the upper is the heavy one, on CHN0224 and CHN0102 the lower; so like is top against top, as here. Above the keel's own line on each sheet the same comparison gives +0.53 ft on CHN0224 (a second reader's route, stations 17 to M). The upper line is not resolved from the heavy one at 8 and O. At 1.2 in a pixel its 3-px gap may stand a little high.

**CHN0102** (9.784 px to the foot, 42 ticks; a noisier preview): the rail's upper line above the wale's lower edge is 4.81 to 4.86 ft against ZAZ6381's 4.41 to 4.49, +0.40 ft, its sills 3.18, 3.16 and 3.08 ft above that edge against CHN0224's 3.21, 3.17 and 3.13 (a second reader's figures, in part read again here). So **the rail's top stands 0.46 ft (5½ in) higher as built**, ±0.1 ft, the mean of the two sheets, the same rise as the sills' (§5.8): sill, port head and rail's top went up together, as the ports' unchanged depth of about 1.5 ft requires.

The wale's lower edge above the keel's line on each sheet differs by -0.01 to +0.10 ft, a mean of +0.04 ft, and its upper edge by -0.01 to +0.06 ft but for +0.19 at K: within a pixel, so the wale was not raised. The band of §5.1 stands 0.35 ft higher on CHN0224.

**CHN0103** (21.55 px to the foot over 11 ft of its bar; stations 17 to 10 at 21.52, against ZAZ6381): rail at station 16,
13.79 ft above the keel against 13.90 as drawn; wale's lower edge 9.36 against 9.39; taffrail, knuckle and wing transom
within 0.1 to 0.4 ft (§5.6). So it follows the draught, not the raised rail.

## 4. The load line

### 4.1 The lines

Three straight green lines cross the sheer from the rudder to the stem. They are not labelled (read). On the page
(measured, rms 0.27 to 0.33 px over 730 to 790 columns):

| Line | Slope | Above the top of the keel (§5.4) at AP / at the fore perpendicular | Length, rabbet to rabbet |
|---|---|---|---|
| **WL1** | 0.05654 | 9.22 / 6.22 ft | 54.13 ft (56.08 ft over the post's after edge and the stem's fore edge) |
| WL2 | 0.05604 | 6.74 / 3.76 ft | 52.36 ft |
| WL3 | 0.05612 | 4.27 / 1.29 ft | 49.5 ft |

They lie parallel, 2.47 ft (2 ft 5½ in) apart, 3.24° to the page and 3.12° to the keel: 3.0 ft of drag over the
perpendiculars. WL1's after end runs through the post to the rudder's after edge, and its fore end past the rabbet to the stem's fore edge; the others stop at the rabbet and the post (read). The rudder's after edge steps exactly there, -2.38 to -2.19 ft at 0.39 to 0.06 ft below WL1 (§5.6; measured).

### 4.2 Which is the load line (judgement, on measures)

**WL1, the top line.** No writing says so, and no draught is written on any sheet. The evidence:

1. **Displacement.** Integrating the traced sections (§5.7) to each line, with 2½ in of plank and the keel:

   | To | Moulded, cu ft | With plank and keel | Tons at 35 cu ft | Against 85 tons burthen |
   |---|---|---|---|---|
   | **WL1** | 3457 | 3740 | **107** (109 t) | 1.26 times |
   | WL2 | 1668 | 1881 | 54 | 0.64 times: less than her burthen, and no vessel of 85 tons floats there |
   | WL3 | 467 | 599 | 17 | 0.20 times |

   The file's 106 t, itself reckoned on other figures, stands 3 t off; the worktree's drawing helper, on §6's points as the file gives them, gives 105 t.
2. **Steel's rule for the load line** (OCR l. 15184-15188, read): for ships other than two- and three-deckers, "about five-eighths of the height of the top-timber line, at the lowest place", set up from the keel's underside. Taking the rail for the top-timber line at O, 13.42 ft above the keel's lower edge as drawn and 13.88 ft as built, five-eighths is 8.39 and 8.67 ft, against WL1's 8.58 ft and WL2's 6.11 ft (measured): it picks WL1 by itself.
3. **The wale.** The wale's lower edge sweeps down to WL1 and meets it nearly at a tangent, 0.03 to 0.04 ft above it
   at stations 8 and 10, and 0.44 ft (5¼ in) at O, the midships Steel means (§5.2). Steel (OCR l. 15190-15193, read) puts the wale's lower edge "a few inches higher" than the load line in midships.
4. **The height of breadth.** It stands 0.63 to 0.84 ft (7½ to 10 in) above WL1 from station 6 to O (§5.2). Steel's rule
   (the same lines) has the lower height of breadth with the wale's lower edge in midships.
5. **The line itself.** Only WL1 runs past the post to the rudder's after edge and past the rabbet to the stem's fore edge, and the rudder's after edge steps there (§4.1; read, judgement on what it means).
6. **Her kin.** *Pitt*'s top waterline (ZAZ6343, about 14.9 px to the foot) lies at the same slope and comes to within about
   0.4 ft of her wale's lower edge at its lowest; a check only.

**Against it:** the sills. On WL1 they stand 2.84 to 3.65 ft above the water as drawn and 3.3 to 4.0 ft as built, under Steel's four to five feet for sloops and cutters (p. 124, OCR l. 8268-8271, read). On WL2 they would stand 5.3 to 6.1 ft. The sheet's own note raises the sills, which fits a low port on WL1, and the displacement rules out WL2; so she
falls below Steel's rule (judgement). The as-built sheets carry level red lines 1 ft 10½ in apart, parallel with the keel,
which mark no water.

### 4.3 The first reads' 2 ft between the body plan and the sheer: resolved

The figures of the first reads are in no file found; only this step's brief names the disagreement. At the same station the views
agree: taking each green's half-breadth from the plan and its height from the sheer predicts where it crosses each section
in the body plan, and at 42 crossings the ink stands a mean of +0.02 ft from the prediction, sd 0.08 ft, largest 0.26 ft:

| | WL1 | WL2 | WL3 |
|---|---|---|---|
| Mean (ft) | 0.00 | +0.05 | +0.05 |
| sd (ft) | 0.07 | 0.08 | 0.12 |
| Crossings | 13 | 15 | 14 |

The keel on the sheer is a pair of lines 2.4 px apart (§5.4), and the body plan's base is the upper of them, so no constant needs taking out: a first trace that read between the two found a false 0.10 ft. There is no 2 ft at one station. Three things could give a first read that figure (judgement): WL1 is
9.2 ft above the keel at AP, 7.5 at O and 6.2 at the fore perpendicular, so the top line read at the sheer's after end and at the body plan's
middle differs by 1.7 ft, and by 3.0 at the two ends; the body plan's heavy level line at 8.25 ft is the height of breadth, not water; and the keel's
1.1 ft under a rabbet adds its own difference.

### 4.4 The draught (measured)

Below WL1, to the keel's lower edge, ±0.1 ft: **10.0 ft at AP** (extended 0.8 ft from the post's heel), **8.75 ft at mid**, **7.3 ft at the fore perpendicular** (extended 3.9 ft from the forefoot): 2.7 ft of drag, the keel deepening from aft to forward. To the top of the keel, 9.22, 7.72 and 6.22 ft: 3.0 ft of drag.

## 5. The profile, measured

### 5.1 The lines of the side (read; identification as marked)

From the top, at O:

- **The rail**, black and heavy: the top of the side, with a thin line 2 in under it (its underside, judgement), unbroken from the
  taffrail to the stem. The ports run up to the underside (read). CHN0224 and CHN0102 draw the same pair with the weight the other way: a thin upper line, a heavy lower one, the ports' heads on the lower (read, §3.4).
- **A band**, two thin lines 2 in apart, broken at the ports: its top 0.71 ft and its lower edge 0.89 ft below the rail's top,
  throughout (measured; on CHN0224 it follows the rail, 0.35 ft higher than here, §3.4). The only band on the upper side (judgement: a moulding, or rubbing strake).
- **The deck**, two parallel red lines 2 in apart, R1 and R2: the top and underside of the deck's plank (judgement) at the middle line. Heavy red
  stretches on them are the hatches' coamings (judgement).
- **A dashed black line**, 2.6 in (2.3 to 2.9) below R2 the whole length (measured): the old deck's underside (judgement, §5.3).
- **A thin black line:** the wale's upper edge (judgement); short boxes hang between it and the deck, spaced as the beams of ZAZ6382's plan (beams in section, judgement).
- **A dashed black line lower still:** the height of breadth: the body plan's level lines stand at its heights by station within 1 px (measured, §5.7).
- **A heavy black line:** the wale's lower edge. The four chain plates' feet end between it and the thin line (read), which is why the band is called the wale
  (judgement). The kit's black wale agrees by eye (`Build-Ships.md` §5.8), which holds no rung.
- **WL1** just below, then WL2 and WL3, red hold works and a solid red curve (§5.4).

### 5.2 By station (measured)

Feet above WL1 at the station. ±0.05 ft for the rail, wale's lower edge and deck, ±0.1 ft for the rest. "Rail, as built" is the drawn rail + 0.46 ft (§3.4). "Top of keel" is the lower of its two lines (§5.4).

| St | ft from AP | m from mid | Rail, drawn | Rail, as built | Wale, upper | Wale, lower | Deck, top (R1) | Deck, under (R2) | Old deck (dashed) | Height of breadth | Top of keel |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 17 | 1.60 | -7.79 | 5.09 | 5.55 | 1.71 | 0.58 | 2.31 | 2.14 | 1.92 | 1.76 | -9.13 |
| 16 | 3.38 | -7.25 | 4.96 | 5.42 | 1.56 | 0.45 | 2.26 | 2.09 | 1.87 | 1.57 | -9.03 |
| 14 | 6.85 | -6.19 | 4.74 | 5.20 | 1.34 | 0.24 | 2.16 | 2.00 | 1.78 | 1.32 | -8.84 |
| 12 | 10.30 | -5.14 | 4.60 | 5.06 | 1.22 | 0.11 | 2.09 | 1.92 | 1.70 | 1.08 | -8.65 |
| 10 | 13.79 | -4.08 | 4.53 | 4.99 | 1.16 | 0.04 | 2.04 | 1.87 | 1.65 | 0.85 | -8.46 |
| 8 | 17.24 | -3.02 | 4.52 | 4.98 | 1.15 | 0.03 | 2.02 | 1.85 | 1.63 | 0.71 | -8.27 |
| 6 | 20.69 | -1.97 | 4.54 | 5.00 | 1.18 | 0.08 | 2.04 | 1.87 | 1.65 | 0.63 | -8.08 |
| 4 | 24.14 | -0.92 | 4.61 | 5.07 | 1.25 | 0.17 | 2.08 | 1.93 | 1.71 | 0.65 | -7.89 |
| 2 | 27.57 | 0.13 | 4.71 | 5.17 | 1.35 | 0.30 | 2.17 | 2.02 | 1.80 | 0.74 | -7.70 |
| O | 30.74 | 1.09 | 4.84 | 5.30 | 1.48 | 0.44 | 2.29 | 2.13 | 1.91 | 0.84 | -7.52 |
| B | 33.89 | 2.05 | 5.01 | 5.47 | 1.65 | 0.62 | 2.45 | 2.28 | 2.06 | 1.08 | -7.35 |
| D | 37.33 | 3.10 | 5.25 | 5.71 | 1.89 | 0.86 | 2.67 | 2.48 | 2.27 | 1.42 | -7.16 |
| F | 40.79 | 4.16 | 5.56 | 6.02 | 2.20 | 1.16 | 2.95 | 2.75 | 2.54 | 1.91 | -6.97 |
| H | 44.29 | 5.22 | 5.96 | 6.42 | 2.59 | 1.54 | 3.29 | 3.10 | 2.88 | 2.62 | -6.78 |
| K | 47.74 | 6.27 | 6.42 | 6.88 | 3.05 | 2.00 | 3.70 | 3.51 | 3.29 | 3.61 | -6.59 |
| M | 51.28 | 7.35 | 6.97 | 7.43 | 3.61 | 2.56 | 4.19 | 4.01 | 3.79 | 5.05 | -6.39 |

- **The sheer.** Above the water the rail is lowest at about 17 ft from AP, 4.52 ft (as drawn), and rises 1.0 ft to the taffrail's side
  and 3.2 ft to the stem. Against the keel, as the eye sees the draught on the page, it is lowest near 31 ft.
- **The ends:** (-3.12, 5.54) at the taffrail's side, (0.00, 5.24) at AP, (54.00, 7.45) and (55.18, 7.69) where it meets the stem (ft from AP, ft above WL1, as drawn).
- **The freeboard to the deck,** R1 at mid: 2.16 ft (0.66 m), the lowest 2.02 ft at station 8. **The bulwark,** the rail as built less R1: 2.95 to 3.24 ft along the side.

### 5.3 The decks and their ends, and the raising (measured; judgement as marked)

She is flush: one deck from the post to the stem, no step (read). R1 runs from 0.42 ft to 53.86 ft from AP, 2.35 and 4.61 ft above WL1 at its ends, stopped by the post and the stem's inner line (read). The beams' round-up is not drawn, so the deck at the side is not given. The wing transom's round-up is 2.7 in (§5.6), and ZAZ6306's deck 4 to 4½ in on her 20 ft (judgement that R1 stands that much above the side).

How the three reads of the raising fit (judgement, each figure measured above):

| Near station 2, above the keel's line on each sheet (on ZAZ6381 between its two lines, §5.4) | ZAZ6381 | CHN0224 |
|---|---|---|
| The heavy red hatch line, on the deck | 9.73 ft | 9.88 ft: the same deck within 1½ px (1.8 in) |
| The deck's top, R1; its underside, R2 | 9.82 and 9.67 ft | not parted at 1.2 in a pixel |
| The dashed line | 9.45 ft | not drawn |

| Sills above the deck | | The note |
|---|---|---|
| ZAZ6381, above R1 | 9.6 to 10.3 in, as drawn | |
| ZAZ6381, above R1 less 3 in | 12.6 to 13.3 in, as drawn | "1-0½ as drawn" |
| CHN0224, above its hatch line | 13.3 in, ±1.2 | "should be 1-3" |

So: the lines were drawn with the deck some 3 in below R1 and the sills 1 ft 0½ in above that deck. The deck went up 3 in, in red, on this sheet. The sills were to go up with it and 2½ in more, and did: as built they stand within 0.1 ft of R1 + 1 ft 3 in at all four ports (§5.8). The rail's top went up about 5½ in with them (§3.4). **Plainly:** the note's waist of 3 ft 2 in is then nearly reached: R1 to the rail's top as built is 3 ft 1½ in at O on CHN0224 and 3 ft 0 in on the two sheets' mean, within the previews' 1.2 in a pixel; it is 2 ft 10½ to 2 ft 11½ in from CHN0224's own hatch line.

### 5.4 The keel, the rabbet and the rising line (measured)

- **The keel's lower edge** (ft from AP, ft above WL1), ±0.1 ft: (0.80, -9.95), (4.63, -9.78), (12.28, -9.41), (19.93, -9.04), (27.58, -8.73), (31.40, -8.53), (39.69, -8.11), (50.65, -7.51). From 32 ft to about 50 ft it lies under the strip's top border, its depth taken from where it shows (judgement). It shows 0.8 ft below the top of the keel at the post's heel and 1.04 ft by 31 ft; the body plan's box, from the upper line, is 1.25 ft deep and 0.72 ft across (half-siding 0.36 ft).
- **The top of the keel is a pair of lines 2.4 px (0.16 ft) apart**, parallel with each other and with the strip, 0.12° to the page (read, measured): the upper y 646.87 at x 270 to 648.31 at x 930, and the lower y 649.33 to 650.62, each rms under 0.2 px. The upper is the body plan's base (§4.3); the lower is taken as the top of the keel in the tables, its heavier line (judgement).
- **The top of the keel**, the rabbet's line, the lower: (1.95, -9.11), (11.00, -8.61), (19.93, -8.12), (27.58, -7.70), (36.50, -7.21), (46.06, -6.68), straight.
- **The rabbet up the stem** (ft, ft): (49.05, -5.82), (50.45, -5.10), (51.41, -4.40), (52.11, -3.72), (52.64, -3.04), (53.15, -2.37), (53.52, -1.71), (53.84, -1.04), (54.09, -0.39), (54.21, -0.06), (54.34, 0.27), (54.54, 0.93), (54.64, 1.58), (54.77, 2.23), (54.86, 2.88).
- **The post's fore edge**, heavy, the rabbet's line aft: (2.02, -8.89), (1.37, -5.97), (0.87, -3.42), (0.39, -0.88), (0.10, 0.01).
- **The rising line** (judgement: the solid red curve, with a dashed fellow, sweeping from the post to the stem), ft above WL1 by station, ±0.1 ft: 17, -2.32; 14, -4.72; 12, -5.43; 10, -6.17; 8, -6.47; 6, -6.57; 4, -6.52; 2, -6.42; O, -6.28; B, -6.11; D, -5.91; F, -5.59; H, -5.12; K, -4.06.

### 5.5 The stem and the head (measured)

- **The stem's fore edge**, low to high (ft from AP, ft above WL1), ±0.05 ft: (50.65, -7.51), (51.18, -7.25), (51.66, -6.96), (52.09, -6.62), (52.42, -6.27), (52.68, -6.00), (52.95, -5.60), (53.38, -4.93), (53.73, -4.27), (54.05, -3.61), (54.30, -2.95), (54.54, -2.29), (54.76, -1.64), (54.94, -0.98), (55.10, -0.33), (55.19, 0.00), (55.24, 0.32), (55.37, 0.97), (55.45, 1.62), (55.53, 2.27), (55.63, 2.92), (55.68, 3.57), (55.74, 4.21), (55.77, 4.86), (55.80, 5.50), (55.82, 6.15), (55.86, 6.79), (55.86, 7.44), (55.87, 8.08), (55.88, 8.73), (55.88, 9.21). It leaves the keel's lower edge at 50.65 ft and runs in one sweep, 55.19 ft at WL1, almost plumb above the rail: 0.7 ft forward from the water to the head. The stem's breadth fore and aft is 1.0 ft at WL1.
- **The head of the stem:** a box above the rail, 1.3 ft fore and aft, its top from 54.5 to 55.88 ft at 9.21 ft above WL1; on ZAZ6382's plan it stands forward of the outline, 1.3 ft long and 0.7 ft across, notched for the stem (read). CHN0224 adds a knob on it (read).
- **No head.** No knee, no cheeks, no rails, no figure on any of her sheets or on *Pitt*'s (read). `form.head` is `none`.

### 5.6 The post, the rudder and the stern (measured)

- **The post's after edge**, thin, straight from the keel's lower edge to the counter: (0.68, -9.96), (0.42, -8.60), (0.04, -6.05), (-0.33, -3.49), (-0.73, -0.94), (-0.95, 0.33), (-1.12, 1.61), (-1.28, 2.57), (-1.30, 2.79): 8.83° to the page, 12.1° to the line. Its fore-and-aft breadth 1.5 ft at the heel, 1.0 ft at WL1, to the fore edge.
- **The wing transom** in section is the dark block on the post's head, at (-0.15, 2.05). In the body plan it is a level line rounding up from (6.42, 1.98) (half-breadth, ft above WL1) at its end to 2.23 ft at the middle line: a round-up of 0.22 ft (2.7 in).
- **The tuck**, below it, straight on the sheer, on the line of the post, and rounding aft in plan, 0.27 ft at the wing transom: CHN0103's own words, "a Square Tuck that Rounds Aft" (read, §2.4). Its outline in the body plan, the fashion piece (half-breadth, ft above WL1), ±0.1 ft: (0.31, -1.42), (0.31, -0.80), (0.60, -0.29), (1.06, 0.07), (1.59, 0.29), (2.15, 0.39), (2.72, 0.48), (3.29, 0.54), (3.86, 0.60), (4.43, 0.65), (5.00, 0.77), (5.55, 0.94), (6.06, 1.20), (6.42, 1.67), (6.42, 1.98). So it is broad: 3.3 ft out at half a foot above WL1, 5.5 at 0.9 ft, and its foot about 1.4 ft under the water. CHN0103's Fig. 3 draws it in true shape, S-curved as the body plan's, 6.50 ft out (6.73 in red) at the top (measured).
- **The counter**, flat, rising aft 28.6° on the page (25.4° to the line) from the wing transom to the knuckle: at the middle line (-3.34, 3.61); at the side (-2.64, 3.33) on the sheer, 3.61 at the body plan's kink, half-breadth 5.79.
- **The transom**, flat, above it, 16.4° from the vertical on the page (19.7° to the line): at the middle line to (-4.04, 5.95); at the side from the knuckle to the taffrail's side (-3.12, 5.54), half-breadth 5.55. Its edge (half-breadth, ft above WL1): (6.42, 1.98), (6.30, 2.97), (5.79, 3.61), (5.75, 3.94), (5.77, 4.26), (5.69, 4.58), (5.62, 4.90), (5.60, 5.22), (5.55, 5.55). The plan's taffrail: 5.58 ft out at the side's end (x -3.12) to the middle line at x -3.86, a round of 0.74 ft, and it rounds up 0.41 ft. The plan's wing transom: a heavy line from 0 ft at its end to -0.27 ft at the middle line. As a whole, wing transom to taffrail, 46.6° to the vertical: the "about 45°" of `Build-Ships.md` §5.9.
- **As built:** on the rail's upper line, top to top, CHN0224 has the taffrail 0.47 ft higher than ZAZ6381, the taffrail's side 0.47 ft, the knuckle 0.23 ft and the wing transom 0.18 ft (each within 2 px; the knuckle by the two lines' crossing, x 337.4, y 123.7). §6 takes the knuckle + 0.23 ft, the taffrail + 0.46 ft, the counter between, and leaves the wing transom as drawn. CHN0103 has them 0.05 to 0.37 ft lower (§3.4). No difference in plan that the previews can show: CHN0224's stern stands 0.2 to 0.4 ft forward of ZAZ6381's by its red perpendicular, and ZAZ6381's x's are kept.
- **What the form holds.** `Build-Ships.md` §5.1's form draws the transom flat, and has no place for the round aft: the 0.27 ft at the wing transom and the 0.74 ft at the taffrail are recorded here and not drawn.
- **No galleries, no lights.** The transom's face is plain on ZAZ6381, CHN0103, CHN0224 and CHN0102 (read). *Pitt*'s has two square lights in her body plan (read); hers are not drawn, and the owner's pictures for the eye (§5.8 of `Build-Ships.md`) show none.
- **The rudder**, hung on the post (ft from AP, ft above WL1), ±0.1 ft: (0.55, -9.94), (-2.00, -10.09), (-2.02, -10.03), (-2.12, -8.74), (-2.27, -6.18), (-2.43, -4.26), (-2.55, -2.33), (-2.26, -1.99), (-2.33, -1.03), (-2.38, -0.39), (-2.19, -0.06), (-2.17, 0.91), (-2.26, 2.19), (-2.38, 3.15). Its bottom is level with the keel, a step cut at about 2.3 ft under the line; 2.66 ft broad at the keel and 1.3 ft at WL1 to the post's after edge, 10 ft deep to the line: about 20 sq ft under water (1.9 m², judgement on the outline). Its head passes up behind the counter.

### 5.7 The half-breadths, the main breadth and the sections (measured)

**By station**, moulded, feet. The waterlines stand at 0, -2.47 and -4.94 ft (§4.1). ±0.06 ft; ZAZ6381's plan at §3.3's scale; ZAZ6382's at its own, ±0.1 ft. Where the plan's WL1 came out over the main breadth by a pixel at 2 and O, it is taken equal to it. At M the first read of the plan fell 3 px forward of the station's line; read on the line it is main 5.38, WL1 2.65 (between the plan's 2.69 and the body plan's 2.57), WL2 1.07. At 17 the plan's WL2 and its second red diagonal run together at about 0.8 ft (body plan 0.65).

| St | ft from AP | Main breadth | Rail | Load line, WL1 | WL2 | WL3 | Red diagonal 1 | Red diagonal 2 | ZAZ6382's outline | ZAZ6382's inner line |
|---|---|---|---|---|---|---|---|---|---|---|
| 17 | 1.60 | 6.87 | 6.56 | 5.79 | 0.77 | 0.29 | 2.31 | 0.80 | 6.86 | 6.40 |
| 16 | 3.38 | 7.22 | 6.89 | 6.64 | 2.02 | 0.48 | 3.50 | 1.41 | 7.19 | 6.74 |
| 14 | 6.85 | 7.78 | 7.52 | 7.57 | 4.33 | 1.14 | 5.21 | 2.65 | 7.76 | 7.27 |
| 12 | 10.30 | 8.21 | 8.00 | 8.12 | 6.05 | 2.15 | 6.35 | 3.70 | 8.19 | 7.72 |
| 10 | 13.79 | 8.57 | 8.27 | 8.53 | 7.08 | 3.27 | 7.30 | 4.43 | 8.57 | 8.10 |
| 8 | 17.24 | 8.86 | 8.57 | 8.82 | 7.68 | 4.37 | 7.92 | 5.11 | 8.85 | 8.38 |
| 6 | 20.69 | 9.07 | 8.80 | 9.06 | 8.09 | 5.16 | 8.54 | 5.57 | 9.06 | 8.57 |
| 4 | 24.14 | 9.21 | 8.93 | 9.18 | 8.30 | 5.62 | 8.92 | 6.00 | 9.21 | 8.73 |
| 2 | 27.57 | 9.28 | 9.07 | 9.28 | 8.35 | 5.77 | 9.15 | 6.35 | 9.26 |  |
| O | 30.74 | 9.29 | 9.04 | 9.29 | 8.36 | 5.73 | 9.19 | 6.36 |  |  |
| B | 33.89 | 9.30 | 9.11 | 9.26 | 8.22 | 5.38 | 9.13 | 6.36 | 9.26 | 8.79 |
| D | 37.33 | 9.25 | 8.98 | 9.00 | 7.66 | 4.51 | 8.80 | 6.20 | 9.21 | 8.75 |
| F | 40.79 | 8.98 | 8.73 | 8.45 | 6.64 | 3.33 | 8.25 | 5.78 | 8.93 | 8.45 |
| H | 44.29 | 8.45 | 8.20 | 7.35 | 5.07 | 2.05 | 7.44 | 5.10 | 8.35 | 7.86 |
| K | 47.74 | 7.33 | 7.13 | 5.48 | 3.09 | 0.96 | 6.01 | 4.13 | 7.20 | 6.69 |
| M | 51.28 | 5.38 | 5.26 | 2.65 | 1.07 |  | 4.06 | 2.73 | 5.03 | 4.41 |

- **WL1's ends** (ft from AP, half-breadth): aft 0.24, 0.94; 0.42, 1.58; 0.73, 4.07, round onto the tuck; forward 52.3, 1.77; 52.84, 1.26; 53.35, 0.89; 53.86, 0.60; rabbet 54.23.
- **The outline's ends:** the plan's outer line closes on the stem's fore edge at 55.1 ft: 51.87, 4.9; 52.54, 4.26; 53.1, 3.62; 53.61, 2.97; 54.05, 2.33; 54.44, 1.69; 54.76, 1.04; 55.0, 0.53. Aft, the outer line, the main breadth, reaches 6.62 at 0.22 ft and ends on the heavy line at AP.
- **The rail at the quarter.** Abaft 17 the plan's inner line, the rail, runs on to AP: 0.73, 6.42; 0.42, 6.36; 0.22, 6.31; 0, 6.28. Abaft AP it is the one line, straight to the taffrail's side: -1.0, 6.06; -2.0, 5.85; -3.0, 5.61; 5.58 at -3.12 ft (read, measured), read for the rail in §6.
- **The rail at the bow.** The plan's inner line, the rail, stands 3.0 to 3.5 px (0.20 ft) inside the outer at 50.5 to 51.8 ft, 5.17 at M, where the body plan's rail reads 5.33 and the table takes 5.26, and closes on it at about 52 ft. Forward of that they are the one line (measured), read for the rail in §6: 52.3, 4.48; 52.84, 3.93; 53.35, 3.32; 53.86, 2.62; 54.2, 2.08.
- **The main breadth is 9.28 to 9.30 ft** from 2 to B, greatest at O and B (read as flat within 0.02 ft). **Tumblehome** to the rail: 0.2 to 0.3 ft (2½ to 3½ in) (measured).
- **The height of breadth** is the table's column in §5.2, on both the sheer's dashed line and the body plan's level lines (within 1 px, ±0.05 ft): 0.63 ft above WL1 at its lowest at station 6, 1.76 at 17, 5.05 at M. Those level lines each run in from their section to a dashed curve, the centres of the breadth sweeps by Steel's method (judgement), and the heavy one is dead flat's.
- **The diagonals:** on the body plan the two solid red ones leave the middle line, aft at 9.5 and 6.5 ft above the base and 45.6°, 43.0° to the vertical, and forward at 9.7 and 6.7 ft and 44.1°, 37.9°. The plan's two red lines are their half-breadths measured along them (measured: they fall on the body plan's sections).

**The sections**, traced on the body plan: each from where the plan's and sheer's points predict it, then held to its ink. Half-breadth, moulded, feet, at heights above WL1. The plan's WL1 stands at 0. ±0.1 ft, ±0.2 ft in the last foot above the rabbet; the rail's own point is in §6. Stations 17, 16 and M run close to their neighbours near the keel, and read to about 0.2 ft there. M meets the stem's rabbet at about -4.45 ft and below that follows the stem's side at 0.32 ft. No cell is given above the drawn rail. The curves were told apart by their order along rows and columns; the cells in the hollows and near the rabbet were first interpolated towards the rabbet, and at the bow between the waterline and the height of breadth, and were read again on the ink at the cross-check. Station 2's three cells at -6, -5 and -4 had been read on O's heavy line, the next outside it, and were read again on its own at the review.

| St | -9 | -8 | -7 | -6 | -5 | -4 | -3 | -2 | -1 | 0 | +1 | +2 | +3 | +4 | +5 | +6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 17 |  | 0.32 | 0.32 | 0.32 | 0.32 | 0.42 | 0.48 | 0.84 | 1.93 | 5.79 | 6.55 | 6.82 | 6.78 | 6.70 | 6.60 |  |
| 16 |  | 0.32 | 0.45 | 0.45 | 0.48 | 0.67 | 1.15 | 2.41 | 5.08 | 6.64 | 7.10 | 7.20 | 7.13 | 7.02 | 6.96 |  |
| 14 |  | 0.29 | 0.45 | 0.68 | 1.09 | 1.72 | 3.37 | 5.40 | 6.42 | 7.57 | 7.75 | 7.75 | 7.68 | 7.57 |  |  |
| 12 |  | 0.41 | 0.66 | 1.13 | 2.03 | 3.47 | 5.18 | 6.59 | 7.41 | 8.12 | 8.20 | 8.19 | 8.10 | 7.98 |  |  |
| 10 |  | 0.28 | 0.87 | 1.75 | 3.16 | 4.95 | 6.43 | 7.48 | 8.04 | 8.53 | 8.58 | 8.55 | 8.48 | 8.38 |  |  |
| 8 |  | 0.29 | 1.12 | 2.37 | 4.21 | 5.98 | 7.21 | 8.01 | 8.47 | 8.82 | 8.85 | 8.83 | 8.75 | 8.67 |  |  |
| 6 |  |  | 1.35 | 3.07 | 5.11 | 6.63 | 7.67 | 8.36 | 8.77 | 9.06 | 9.05 | 9.04 | 8.98 | 8.91 |  |  |
| 4 |  |  | 1.48 | 3.53 | 5.60 | 6.97 | 7.93 | 8.55 | 8.92 | 9.18 | 9.26 | 9.20 | 9.13 | 9.06 |  |  |
| 2 |  |  | 1.45 | 3.71 | 5.67 | 7.05 | 8.02 | 8.63 | 9.01 | 9.28 | 9.29 | 9.28 | 9.22 | 9.16 |  |  |
| O |  |  | 1.28 | 3.63 | 5.64 | 6.97 | 7.96 | 8.58 | 8.92 | 9.29 | 9.28 | 9.27 | 9.22 | 9.16 |  |  |
| B |  |  | 0.87 | 3.23 | 5.31 | 6.71 | 7.76 | 8.47 | 8.90 | 9.26 | 9.29 | 9.28 | 9.22 | 9.16 | 9.11 |  |
| D |  |  | 0.59 | 2.23 | 4.37 | 5.97 | 7.16 | 8.00 | 8.53 | 9.00 | 9.22 | 9.25 | 9.18 | 9.11 | 9.05 |  |
| F |  |  |  | 1.62 | 3.12 | 4.72 | 6.10 | 7.08 | 7.81 | 8.45 | 8.79 | 8.94 | 8.90 | 8.79 | 8.71 |  |
| H |  |  |  | 1.20 | 2.00 | 3.24 | 4.47 | 5.61 | 6.56 | 7.35 | 8.01 | 8.30 | 8.41 | 8.35 | 8.26 | 8.17 |
| K |  |  |  | 0.67 | 0.77 | 1.66 | 2.58 | 3.58 | 4.58 | 5.48 | 6.25 | 6.90 | 7.17 | 7.27 | 7.20 | 7.09 |
| M |  |  |  | 0.32 | 0.32 | 0.40 | 0.69 | 1.31 | 1.92 | 2.65 | 3.30 | 4.05 | 4.78 | 5.21 | 5.39 | 5.36 |

- **The checks:** at 47 crossings of the three waterlines against the half-breadth plan, mean -0.02 ft, sd 0.05 ft, largest 0.20 ft (16, WL2), then 0.14 ft (K, WL3). Those crossings anchored the first trace, so they cannot test the rest: off them, each of the table's 199 cells clear of the heavy level line against the nearest ink on its row, mean 0.00 ft, sd 0.07 ft, nine beyond 0.15 ft: six in the last foot above the rabbet, the largest 0.39 ft (D, -6), two at station 17's sharp turn at the line, one at D against the box's edge. Of the 149 cells from 4 ft below the line upward, sd 0.06 ft, three beyond 0.15 ft. The nearest ink cannot tell one curve from the next, so the order was taken again on black ink alone, with the reds and greens dropped: from outside in, O, 2, 4, 6 and on to 17 aft, and B, D, F, H, K, M forward, each cell on its own curve; O and 2 run together in one line from about 3 ft below the water upward, 4 with them above the height of breadth, and B and D above the height of breadth, where the plan's main breadths differ by under 0.1 ft.
- **The form** (measured on the table): about 25° of floor at O from the rabbet to 5½ ft out, then a slack round bilge to the breadth at 0.8 ft above the line: not the hard flat floor of a big ship. Nearly wall-sided above; the sharp hollow run into the tuck at 17 and 16; and a full bow: at the water 7.35 ft out at H, 5.48 at K, 2.65 at M.

### 5.8 The ports (measured)

Off ZAZ6381 at §3's scale, centres ±0.05 ft, its sills ±0.05 ft. ZAZ6382 crosses each in the side's band (read), which gives the second x. Each port's head is the rail's underside (read).

| Port | ft from AP (ZAZ6381 / ZAZ6382 / CHN0224, from its fore perpendicular) | m from mid | Breadth, ft | Depth to the rail's underside, ft | Sill above the line, drawn | Deck top there | Sill above deck, drawn | Sill as built: deck top + 1 ft 3 in, the sheet's note (read), checked on CHN0224 below | Half-breadth at that sill, moulded |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 11.58 / 11.58 / 11.58 | -4.75 | 1.91 | 1.56 | 2.88 | 2.07 | 9.7 in | 3.32 | 8.21 |
| 2 | 19.43 / 19.44 / 19.47 | -2.35 | 1.92 | 1.54 | 2.84 | 2.03 | 9.7 in | 3.28 | 8.88 |
| 3 | 27.23 / 27.33 / 27.30 | 0.02 | 1.85 | 1.60 | 2.96 | 2.16 | 9.6 in | 3.41 | 9.19 |
| 4 | 38.92 / 38.97 / 38.95 | 3.58 | 1.90 | 1.49 | 3.65 | 2.79 | 10.3 in | 4.04 | 8.96 |

**As built** (CHN0224, ±1.2 in): sills 11.89, 11.39, 11.09 and 11.06 ft above the top of the keel against ZAZ6381's 11.36, 10.91, 10.62 and 10.70: higher by 0.53, 0.48, 0.47, 0.36 ft, a mean of 5½ in, so above WL1 at 3.41, 3.32, 3.43 and 4.01 ft against the deck top + 1 ft 3 in's 3.32, 3.28, 3.41 and 4.04: within 0.09 ft. The as-built sills in §6 are that sum, not a reading. Breadths 1.8 to 1.9 ft, depths about 1.5 ft to the rail's underside. CHN0224 draws the fourth with a heavy pair of lids (read).

**Sweep ports**, one abaft the first port and one between each pair: small squares, their sills in line with the ports'.

| Sweep port | ft from AP (ZAZ6381 / ZAZ6382) | m from mid | Breadth, ft | Depth, ft | Sill above the line, drawn |
|---|---|---|---|---|---|
| 1 | 7.60 / 7.56 | -5.96 | 0.69 | 0.64 | 2.98 |
| 2 | 15.53 / 15.54 | -3.55 | 0.64 | 0.67 | 2.88 |
| 3 | 23.36 / 23.40 | -1.16 | 0.65 | 0.69 | 2.96 |
| 4 | 33.06 / 33.16 | 1.80 | 0.64 | 0.72 | 3.26 |

**A fifth, smaller opening** at 52.65 ft (5.52 to 6.98 ft above WL1, 1.0 ft broad, shaded on its fore side), under the rail, is not a port for a broadside gun (judgement: a bridle or warping port). CHN0224 draws it and two small round holes forward (hawse holes, judgement).

**Uprights** stand on the rail, about 0.8 ft high, at 0.01, 4.31, 8.55, 41.89, 48.99 and 54.1 ft from AP on ZAZ6381; at -0.37, 4.13, 8.52, 41.85, 44.1, 46.4, 49.0, 51.9 and 53.5 on CHN0224 (measured, ±0.2 ft). Stocks for swivels or timberheads (judgement); no gun is drawn on any sheet (read).

**Where three guns stood** is not drawn. The file's guns stand at x -3.5, -0.5 and 2.5 m (`data/ships/cutter.yaml`), which fall between the sheet's ports: -3.5 on its second sweep port, and 2.5 among its deadeyes (0.66 to 2.76 m, §5.9). §6 gives the sill line there, by the same rule.

### 5.9 The masts and spars (measured)

| Item | ft from AP | m from mid | Basis |
|---|---|---|---|
| **The mast, at the deck** | **35.80** | **2.63** | ZAZ6381: centre by its dashed centre line and two faces, ±0.1 ft |
| The same, ZAZ6382's deck | 35.82 | 2.64 | circle 1.44 ft across on the middle line |
| The step, ZAZ6382's hold | 36.1 | 2.72 | circle, ±0.2 ft |
| Deadeyes, four a side | 29.34, 31.62, 33.95, 36.22 | 0.66 to 2.76 | ZAZ6381, on the rail's band; chain plates to the wale |

- **Rake**, head aft: 3.69° to the page (fore face 3.86°, after face 3.46°), 3.92° to the keel, **6.93° to the line**. **Across:** 1.38 ft (16.6 in), table 17½ in.
- **The bowsprit**, in red, its heel at 44.0 ft: across the stem head its centre stands 7.94 ft (2.42 m) above WL1 and 3.33 ft (1.01 m) above the deck there. It steeves 1.83° to the page, 5.07° to the line; 1.15 ft (13.7 in) across, table 13½ in. ZAZ6381 stops it about 7.8 ft before the stem head; CHN0224 and CHN0102 draw it further (read). The plans do not settle whether it runs on the middle line (the hold plan's patched forward); the owner's picture puts it beside the stem, for the eye only.
- **The hatches on ZAZ6382's deck** (ft from AP, ±0.1 ft): 4.5 to 8.2, 9.8 to 13.1, 18.3 to 21.7, 26.3 to 32.2 (the main hatch), 41.1 to 43.75; the windlass at about 45.8; the side's band 5½ in deep (read, measured).

## 6. For the profile: the points in metres

`x` from mid, `z` above WL1 at the station, in metres; from §5, measured unless marked; **as built**, the rail, deck and sills of one state (§5.3). Half-breadths **with 2½ in of plank** (0.06 m), the sheet's extreme breadth over its moulded. `tools/ships/hull_cutter.py` holds them, and `tests/test_hull_cutter.py` holds each against this section: the refusals none; each measured triple within 0.005 m of the drawn side; the drawn displacement 105 t against 106 t; drawn 2.29 m deep at the rabbet (2.66 m to the keel's lower edge at mid) against the file's 2.6 m.

- **`rail_m`**: [-9.23, 1.83], [-8.28, 1.74], [-7.79, 1.69], [-7.25, 1.65], [-6.19, 1.59], [-5.14, 1.54], [-4.08, 1.52], [-3.02, 1.52], [-1.97, 1.53], [-0.92, 1.54], [0.13, 1.58], [1.09, 1.61], [2.05, 1.67], [3.10, 1.74], [4.16, 1.84], [5.22, 1.96], [6.27, 2.10], [7.35, 2.26], [8.18, 2.41], [8.33, 2.44], [8.34, 2.81]. As drawn, less 0.14 m (§3.4). Its last two points are where it meets the stem head's box and the box's after edge at its top (§5.5); the box's fore edge is `stem_m`'s top. **Old beside new, at the landing:** first it ended on x 8.54, z 2.48, and the side closed straight to the stem head, a pointed fin 0.56 m across where her sheets draw a box 0.7 ft across (seen on the drawn sheets).
- **`breadth_m`** (x, water, rail): [-8.21, 0.35, 1.98], [-8.15, 0.54, 2.00], [-8.06, 1.30, 2.02], [-7.79, 1.83, 2.06], [-7.25, 2.08, 2.16], [-6.19, 2.37, 2.35], [-5.14, 2.54, 2.50], [-4.08, 2.66, 2.58], [-3.02, 2.75, 2.67], [-1.97, 2.82, 2.74], [-0.92, 2.86, 2.78], [0.13, 2.89, 2.83], [1.09, 2.89, 2.81], [2.05, 2.88, 2.84], [3.10, 2.81, 2.80], [4.16, 2.64, 2.72], [5.22, 2.30, 2.56], [6.27, 1.73, 2.23], [7.35, 0.87, 1.66], [7.66, 0.60, 1.43], [7.83, 0.45, 1.26], [7.98, 0.33, 1.07], [8.14, 0.24, 0.86], [8.24, 0.17, 0.69], [8.33, 0.11, 0.11]. The last is the stem head's box, the stem's half-siding at the water and the box's 0.7 ft across at the top (§5.5); in plan the form closes it straight to the stem's fore edge, as every stem head. Ends by §5.7; the rail's half-breadth abaft 17 off the plan's inner line; forward of M off that line until it closes on the outer at about 52 ft, and off the one line forward of that; abaft AP it is `transom_hb_m`'s.
- **`keel_m`** (the lower edge): [-8.03, -3.03], [-6.87, -2.98], [-4.54, -2.87], [-2.20, -2.75], [0.13, -2.66], [1.29, -2.60], [3.82, -2.47], [7.16, -2.29]. The part under the strip's border judged (§5.4).
- **`stem_m`** (fore edge, low to high): [7.16, -2.29], [7.32, -2.21], [7.47, -2.12], [7.60, -2.02], [7.70, -1.91], [7.78, -1.83], [7.86, -1.71], [7.99, -1.50], [8.10, -1.30], [8.19, -1.10], [8.27, -0.90], [8.35, -0.70], [8.41, -0.50], [8.47, -0.30], [8.52, -0.10], [8.54, 0.00], [8.56, 0.10], [8.60, 0.30], [8.62, 0.49], [8.65, 0.69], [8.68, 0.89], [8.69, 1.09], [8.71, 1.28], [8.72, 1.48], [8.73, 1.68], [8.74, 1.87], [8.75, 2.07], [8.75, 2.27], [8.75, 2.46], [8.75, 2.66], [8.75, 2.81]. Its top is the stem head.
- **`stern_m`** (the post's after edge, the counter, the transom, at the middle line, low to high): [-8.07, -3.03], [-8.15, -2.62], [-8.27, -1.84], [-8.38, -1.06], [-8.50, -0.29], [-8.57, 0.10], [-8.62, 0.49], [-8.67, 0.78], [-8.67, 0.85], [-9.00, 1.05], [-9.30, 1.17], [-9.37, 1.43], [-9.44, 1.70], [-9.51, 1.95]. As built from the counter up by §5.6, on ZAZ6381's x's.
- **`wales_m`** (x, lower, upper): [-8.19, 0.20, 0.55], [-7.79, 0.18, 0.52], [-7.25, 0.14, 0.47], [-6.19, 0.07, 0.41], [-5.14, 0.03, 0.37], [-4.08, 0.01, 0.35], [-3.02, 0.01, 0.35], [-1.97, 0.03, 0.36], [-0.92, 0.05, 0.38], [0.13, 0.09, 0.41], [1.09, 0.13, 0.45], [2.05, 0.19, 0.50], [3.10, 0.26, 0.58], [4.16, 0.35, 0.67], [5.22, 0.47, 0.79], [6.27, 0.61, 0.93], [7.35, 0.78, 1.10], [8.49, 0.98, 1.31]. Not raised (§3.4). The two lines run parallel to both ends (measured).
- **`section_m`** (station O, z, half-breadth with plank): [-2.29, 0.17], [-2.13, 0.45], [-1.83, 1.17], [-1.52, 1.78], [-1.22, 2.19], [-0.91, 2.49], [-0.61, 2.68], [-0.30, 2.78], [0.00, 2.89], [0.26, 2.89], [0.30, 2.89], [0.61, 2.89], [0.91, 2.87], [1.22, 2.85], [1.61, 2.81].
- **`decks_m.upper`** (R1, the deck's top at the middle line; the side is not drawn, §5.3): [-8.15, 0.72], [-7.79, 0.70], [-7.25, 0.69], [-6.19, 0.66], [-5.14, 0.64], [-4.08, 0.62], [-3.02, 0.62], [-1.97, 0.62], [-0.92, 0.64], [0.13, 0.66], [1.09, 0.70], [2.05, 0.75], [3.10, 0.81], [4.16, 0.90], [5.22, 1.00], [6.27, 1.13], [7.35, 1.28], [8.13, 1.41].
- **`ports_m.upper`** (x, sill as built, half-breadth at that sill with plank): the seven of this list in `x` order, four the sheet's ports and three the guns' places. **The sheet's four:** [-4.75, 1.01, 2.56], [-2.35, 1.00, 2.77], [0.02, 1.04, 2.86], [3.58, 1.23, 2.79]. Sill: R1 + 1 ft 3 in, the sheet's note (read), checked on CHN0224 within 0.09 ft. As drawn, the sills would be: [-4.75, 0.88, 2.58], [-2.35, 0.86, 2.78], [0.02, 0.90, 2.87], [3.58, 1.11, 2.81]. **The guns' three:** [-3.50, 1.00, 2.69], [-0.50, 1.03, 2.85], [2.50, 1.15, 2.85]: the same sill line and the side at the file's guns' own `x` (§5.8, §7), where the sheet draws no port (judged). No gun's `x_m` moves; each stands on a triple (`Build-Ships.md` §5.6), and `sill_at` runs straight along the one sill line. As built by the lead's point 5 (2026-10-31); package 81 would draw an opening at only the sheet's four.
- **`port_size_m.upper`**: [0.58, 0.47] (1 ft 11 in broad; 1 ft 6½ in, the mean depth of the four as drawn, sill to rail's underside).
- **`head_m`**: none. **`form.head`**: `none`.
- **`breadth_line_m`** (x, z, main half-breadth with plank): [-7.79, 0.54, 2.15], [-7.25, 0.48, 2.26], [-6.19, 0.40, 2.43], [-5.14, 0.33, 2.56], [-4.08, 0.26, 2.67], [-3.02, 0.22, 2.76], [-1.97, 0.19, 2.83], [-0.92, 0.20, 2.87], [0.13, 0.22, 2.89], [1.09, 0.26, 2.89], [2.05, 0.33, 2.90], [3.10, 0.43, 2.88], [4.16, 0.58, 2.80], [5.22, 0.80, 2.64], [6.27, 1.10, 2.30], [7.35, 1.54, 1.70].
- **`channel_wales_m`** (x, lower, upper; the only other band, §5.1; so named for the drawing, judgement; as built, 0.30 ft above ZAZ6381's, between the two sheets' rise, judgement): [-7.79, 1.37, 1.43], [-7.25, 1.33, 1.38], [-6.19, 1.27, 1.32], [-5.14, 1.22, 1.28], [-4.08, 1.20, 1.26], [-3.02, 1.20, 1.25], [-1.97, 1.21, 1.26], [-0.92, 1.23, 1.28], [0.13, 1.26, 1.31], [1.09, 1.30, 1.35], [2.05, 1.35, 1.40], [3.10, 1.42, 1.47], [4.16, 1.52, 1.57], [5.22, 1.64, 1.69], [6.27, 1.78, 1.83], [7.35, 1.94, 2.00].
- **`rabbet_m`** (x, z, half-siding 0.36 ft; along the keel's lower top line, then up the stem): [-7.68, -2.78, 0.11], [-4.92, -2.62, 0.11], [-2.20, -2.48, 0.11], [0.13, -2.35, 0.11], [2.85, -2.20, 0.11], [5.76, -2.04, 0.11], [6.67, -1.77, 0.11], [7.10, -1.55, 0.11], [7.39, -1.34, 0.11], [7.61, -1.13, 0.11], [7.77, -0.93, 0.11], [7.92, -0.72, 0.11], [8.03, -0.52, 0.11], [8.13, -0.32, 0.11], [8.21, -0.12, 0.11], [8.24, -0.02, 0.11], [8.28, 0.08, 0.11], [8.34, 0.28, 0.11], [8.38, 0.48, 0.11], [8.41, 0.68, 0.11], [8.44, 0.88, 0.11].
- **`floor_m`** (the rising line of §5.4 at the section's half-breadth there with plank; judgement on what the line is): [-7.79, -0.71, 0.28], [-6.19, -1.44, 0.45], [-5.14, -1.66, 0.56], [-4.08, -1.88, 0.55], [-3.02, -1.97, 0.60], [-1.97, -2.00, 0.70], [-0.92, -1.99, 0.81], [0.13, -1.96, 0.89], [1.09, -1.91, 0.97], [2.05, -1.86, 0.97], [3.10, -1.80, 0.80], [4.16, -1.70, 0.74], [5.22, -1.56, 0.64], [6.27, -1.24, 0.55].
- **`sections_m`** (x, z, half-breadth with plank): the keel's line, §5.7's table, the height of breadth and the rail as built, by station:
  - 17: [-7.79, -2.78, 0.17], [-7.79, -2.44, 0.16], [-7.79, -2.13, 0.16], [-7.79, -1.83, 0.16], [-7.79, -1.52, 0.16], [-7.79, -1.22, 0.19], [-7.79, -0.91, 0.21], [-7.79, -0.61, 0.32], [-7.79, -0.30, 0.65], [-7.79, 0.00, 1.83], [-7.79, 0.30, 2.06], [-7.79, 0.54, 2.15], [-7.79, 0.61, 2.14], [-7.79, 0.91, 2.13], [-7.79, 1.22, 2.10], [-7.79, 1.52, 2.07], [-7.79, 1.69, 2.06]
  - 16: [-7.25, -2.75, 0.17], [-7.25, -2.44, 0.16], [-7.25, -2.13, 0.20], [-7.25, -1.83, 0.20], [-7.25, -1.52, 0.21], [-7.25, -1.22, 0.27], [-7.25, -0.91, 0.41], [-7.25, -0.61, 0.80], [-7.25, -0.30, 1.61], [-7.25, 0.00, 2.08], [-7.25, 0.30, 2.23], [-7.25, 0.48, 2.26], [-7.25, 0.61, 2.26], [-7.25, 0.91, 2.23], [-7.25, 1.22, 2.20], [-7.25, 1.52, 2.18], [-7.25, 1.65, 2.16]
  - 14: [-6.19, -2.69, 0.17], [-6.19, -2.44, 0.15], [-6.19, -2.13, 0.20], [-6.19, -1.83, 0.27], [-6.19, -1.52, 0.39], [-6.19, -1.22, 0.59], [-6.19, -0.91, 1.09], [-6.19, -0.61, 1.71], [-6.19, -0.30, 2.02], [-6.19, 0.00, 2.37], [-6.19, 0.30, 2.42], [-6.19, 0.40, 2.43], [-6.19, 0.61, 2.42], [-6.19, 0.91, 2.40], [-6.19, 1.22, 2.37], [-6.19, 1.59, 2.35]
  - 12: [-5.14, -2.64, 0.17], [-5.14, -2.44, 0.19], [-5.14, -2.13, 0.26], [-5.14, -1.83, 0.41], [-5.14, -1.52, 0.68], [-5.14, -1.22, 1.12], [-5.14, -0.91, 1.64], [-5.14, -0.61, 2.07], [-5.14, -0.30, 2.32], [-5.14, 0.00, 2.54], [-5.14, 0.33, 2.56], [-5.14, 0.61, 2.56], [-5.14, 0.91, 2.53], [-5.14, 1.22, 2.49], [-5.14, 1.54, 2.50]
  - 10: [-4.08, -2.58, 0.17], [-4.08, -2.44, 0.15], [-4.08, -2.13, 0.33], [-4.08, -1.83, 0.59], [-4.08, -1.52, 1.02], [-4.08, -1.22, 1.57], [-4.08, -0.91, 2.02], [-4.08, -0.61, 2.34], [-4.08, -0.30, 2.51], [-4.08, 0.00, 2.66], [-4.08, 0.26, 2.67], [-4.08, 0.30, 2.68], [-4.08, 0.61, 2.67], [-4.08, 0.91, 2.65], [-4.08, 1.22, 2.62], [-4.08, 1.52, 2.58]
  - 8: [-3.02, -2.52, 0.17], [-3.02, -2.44, 0.15], [-3.02, -2.13, 0.40], [-3.02, -1.83, 0.78], [-3.02, -1.52, 1.34], [-3.02, -1.22, 1.88], [-3.02, -0.91, 2.26], [-3.02, -0.61, 2.50], [-3.02, -0.30, 2.64], [-3.02, 0.00, 2.75], [-3.02, 0.22, 2.76], [-3.02, 0.30, 2.76], [-3.02, 0.61, 2.75], [-3.02, 0.91, 2.73], [-3.02, 1.22, 2.70], [-3.02, 1.52, 2.67]
  - 6: [-1.97, -2.46, 0.17], [-1.97, -2.13, 0.47], [-1.97, -1.83, 1.00], [-1.97, -1.52, 1.62], [-1.97, -1.22, 2.08], [-1.97, -0.91, 2.40], [-1.97, -0.61, 2.61], [-1.97, -0.30, 2.73], [-1.97, 0.00, 2.82], [-1.97, 0.19, 2.83], [-1.97, 0.30, 2.82], [-1.97, 0.61, 2.82], [-1.97, 0.91, 2.80], [-1.97, 1.22, 2.78], [-1.97, 1.53, 2.74]
  - 4: [-0.92, -2.40, 0.17], [-0.92, -2.13, 0.51], [-0.92, -1.83, 1.14], [-0.92, -1.52, 1.77], [-0.92, -1.22, 2.19], [-0.92, -0.91, 2.48], [-0.92, -0.61, 2.67], [-0.92, -0.30, 2.78], [-0.92, 0.00, 2.86], [-0.92, 0.20, 2.87], [-0.92, 0.30, 2.88], [-0.92, 0.61, 2.87], [-0.92, 0.91, 2.84], [-0.92, 1.22, 2.82], [-0.92, 1.54, 2.78]
  - 2: [0.13, -2.35, 0.17], [0.13, -2.13, 0.50], [0.13, -1.83, 1.19], [0.13, -1.52, 1.79], [0.13, -1.22, 2.21], [0.13, -0.91, 2.51], [0.13, -0.61, 2.69], [0.13, -0.30, 2.81], [0.13, 0.00, 2.89], [0.13, 0.22, 2.89], [0.13, 0.30, 2.89], [0.13, 0.61, 2.89], [0.13, 0.91, 2.87], [0.13, 1.22, 2.85], [0.13, 1.58, 2.83]
  - O: [1.09, -2.29, 0.17], [1.09, -2.13, 0.45], [1.09, -1.83, 1.17], [1.09, -1.52, 1.78], [1.09, -1.22, 2.19], [1.09, -0.91, 2.49], [1.09, -0.61, 2.68], [1.09, -0.30, 2.78], [1.09, 0.00, 2.89], [1.09, 0.26, 2.89], [1.09, 0.30, 2.89], [1.09, 0.61, 2.89], [1.09, 0.91, 2.87], [1.09, 1.22, 2.85], [1.09, 1.61, 2.81]
  - B: [2.05, -2.24, 0.17], [2.05, -2.13, 0.33], [2.05, -1.83, 1.05], [2.05, -1.52, 1.68], [2.05, -1.22, 2.11], [2.05, -0.91, 2.43], [2.05, -0.61, 2.64], [2.05, -0.30, 2.77], [2.05, 0.00, 2.88], [2.05, 0.33, 2.90], [2.05, 0.61, 2.89], [2.05, 0.91, 2.87], [2.05, 1.22, 2.85], [2.05, 1.52, 2.84], [2.05, 1.67, 2.84]
  - D: [3.10, -2.18, 0.17], [3.10, -1.83, 0.74], [3.10, -1.52, 1.39], [3.10, -1.22, 1.88], [3.10, -0.91, 2.24], [3.10, -0.61, 2.50], [3.10, -0.30, 2.66], [3.10, 0.00, 2.81], [3.10, 0.30, 2.87], [3.10, 0.43, 2.88], [3.10, 0.61, 2.88], [3.10, 0.91, 2.86], [3.10, 1.22, 2.84], [3.10, 1.52, 2.82], [3.10, 1.74, 2.80]
  - F: [4.16, -2.12, 0.17], [4.16, -1.83, 0.55], [4.16, -1.52, 1.01], [4.16, -1.22, 1.50], [4.16, -0.91, 1.92], [4.16, -0.61, 2.22], [4.16, -0.30, 2.44], [4.16, 0.00, 2.64], [4.16, 0.30, 2.74], [4.16, 0.58, 2.80], [4.16, 0.91, 2.77], [4.16, 1.22, 2.74], [4.16, 1.52, 2.72], [4.16, 1.84, 2.72]
  - H: [5.22, -2.07, 0.17], [5.22, -1.83, 0.43], [5.22, -1.52, 0.67], [5.22, -1.22, 1.05], [5.22, -0.91, 1.42], [5.22, -0.61, 1.77], [5.22, -0.30, 2.06], [5.22, 0.00, 2.30], [5.22, 0.30, 2.50], [5.22, 0.61, 2.59], [5.22, 0.80, 2.64], [5.22, 0.91, 2.62], [5.22, 1.22, 2.61], [5.22, 1.52, 2.58], [5.22, 1.83, 2.55], [5.22, 1.96, 2.56]
  - K: [6.27, -2.01, 0.17], [6.27, -1.83, 0.27], [6.27, -1.52, 0.30], [6.27, -1.22, 0.57], [6.27, -0.91, 0.85], [6.27, -0.61, 1.15], [6.27, -0.30, 1.46], [6.27, 0.00, 1.73], [6.27, 0.30, 1.97], [6.27, 0.61, 2.16], [6.27, 0.91, 2.25], [6.27, 1.10, 2.30], [6.27, 1.22, 2.28], [6.27, 1.52, 2.26], [6.27, 1.83, 2.22], [6.27, 2.10, 2.23]
  - M: [7.35, -1.95, 0.17], [7.35, -1.83, 0.16], [7.35, -1.52, 0.16], [7.35, -1.22, 0.18], [7.35, -0.91, 0.27], [7.35, -0.61, 0.46], [7.35, -0.30, 0.65], [7.35, 0.00, 0.87], [7.35, 0.30, 1.07], [7.35, 0.61, 1.30], [7.35, 0.91, 1.52], [7.35, 1.22, 1.65], [7.35, 1.54, 1.70], [7.35, 1.83, 1.69], [7.35, 2.26, 1.66]

  The tuck's outline is not a station of these: tried as one at x -8.25, it moved the picture little and left a sliver where the wale ends on it, so it is kept here and not drawn (`Build-Ships.md` §5.0 principles 2 and 11). Half-breadth with plank, z: [0.16, -0.43], [0.16, -0.24], [0.24, -0.09], [0.38, 0.02], [0.55, 0.09], [0.72, 0.12], [0.89, 0.15], [1.06, 0.17], [1.24, 0.18], [1.41, 0.20], [1.58, 0.24], [1.75, 0.29], [1.91, 0.37], [2.02, 0.51], [2.02, 0.60].
- **`form`**:
  - `fullness`: none given; the ends are drawn through `sections_m`.
  - `stern.type`: `square`.
  - `stern.knuckle_z_m`: **0.60**, the wing transom at its ends, 1 ft 11¾ in above the line, as the 64's (`tools/ships/indefatigable.py`): where the side closes to the stern (judgement on which of the two; the counter's knuckle above it, 1.17 m at the middle line as built, goes in `stern_m`).
  - `stern.transom_hb_m`: **[1.75, 2.02]**, at the taffrail's side and the wing transom's end, with plank.
  - `stern.round_up_m`: **0.07** (the wing transom's, 2.7 in).
  - `stern.galleries_m`, `stern.lights_m`: none (read).
- **`marks`** (the word of the line's weakest point, `Build-Ships.md` §5.0 principle 4): `rail_m`, `breadth_m`, `stem_m`, `stern_m`, `section_m`, `port_size_m`, `breadth_line_m`, `sections_m`, `form.stern`, `form.stern.transom_hb_m`, `form.stern.round_up_m`, `form.head`: **sourced**. `ports_m` (sourced for the sheet's four; the guns' three are judged, and the line takes that word), `keel_m` (under the border), `decks_m` (the middle line for the side), `wales_m` (the name), `channel_wales_m` (the name), `floor_m` (the line's identity), `rabbet_m` (the lower of the keel's two top lines, one half-siding held along her), `form.stern.knuckle_z_m` (which of the two corners): **judged**. **Old beside new, at the landing:** `wales_m`, `rabbet_m` and `form.stern.knuckle_z_m` were first `sourced`; principle 4 takes the word of the weakest point.

## 7. Against `data/ships/cutter.yaml` (recorded, not moved)

| Field | The file (its note) | The sheets |
|---|---|---|
| `length_waterline_m` | 15.2 (50 ft, judgement between keel and deck) | 16.50 m (54 ft 1½ in) WL1 rabbet to rabbet; 17.09 m (56 ft 1 in) over all at the line (measured). WL3 happens to be 49.5 ft |
| `beam_m` | 5.8 (19 ft 0 in) | 19 ft 0 in (read); moulded 18 ft 7 in (measured) |
| `draught_m` | 2.6 (8.5 ft mean; 9.5 aft, 7.5 forward; judgement and Fincham) | 2.67 m (8 ft 9 in) at mid to the keel's lower edge; 10.0 ft at AP, 7.3 ft at the fore perpendicular (measured) |
| Drag | 2 ft (Fincham p. 67, 24 in) | 3 ft 0 in over the perpendiculars, 3.12° to the keel (measured) |
| `displacement_kg` | 106,000 (block coefficient 0.45 on waterline, beam and draught at 1025, judgement) | 109,000 by the sections to WL1 (measured), a block of 0.42 on the file's formula with the sheet's figures (0.45 moulded to the rabbet) |
| `deck_height_m` | 0.9 (3 ft, judgement) | 0.66 m (2 ft 2 in) at mid, the deck's top at the middle line, as built (measured) |
| Keel | "44 ft 3 in" (`tools/gen_ships.py`, a fifth less than the deck) | 44 ft 7 in for tonnage on all three sheets (read); Charnock's 42 ft 0 in |
| `main.mast` `x_m`, `rake_deg` | 1.5 (4.9 ft before the middle, Fincham); 5.2 | +2.63 (8 ft 8 in before mid); 3.7 to the page, 6.9 to the line (measured) |
| `bowsprit` `height_m`, near horizontal | 1.2 | 1.01 m above the deck at the stem; steeved 1.8° to the page, 5.1° to the line (measured) |
| Spars | mast 61 ft, boom 47, gaff 30, square-sail yard 46, topsail yard 32, bowsprit 43 | 66 ft 10 in to the pole head, boom 51 ft 3 in, gaff 30 ft, spread yard 43 ft 7 in, cross-jack yard 36 ft, topsail yard 33 ft 9 in, bowsprit 47 ft (read, tentative, §2.3), the mast head 13 within the pole head (tentative) |
| Guns' `height_m`, until this step | 1.5 (Steel's band, judgement) | sills 1.00 to 1.23 m as built, 0.86 to 1.11 as drawn; deck top + 1 ft 3 in at the guns' own x: 1.00, 1.03, 1.15 m, which the file now carries (`Build-Ships.md` §5.3: nothing reads a gun's height until L2) |
| Guns' `x_m` | three a side, -3.5, -0.5, 2.5 | four ports a side, -4.75, -2.35, +0.02, +3.58, with four sweep ports (measured); six carriage guns (Charnock, read), so three a side stands, on four ports |
| Swivels' `height_m` and count | 1.7; eight | the rail as built at the swivels' own x, 1.53 to 1.94 m (measured); stocks' places §5.8; ten swivels (Charnock, read) |
| `rudder` `area_m2`, `span_m` | 1.2; 2.7 (9 ft by 1 ft 6 in, judgement) | about 1.9 m²; 10 ft deep; 1 ft 4 in to 2 ft 8 in broad (measured) |
| §5.7's stand-in, not in the file today | Steel's 273-ton cutter: square counter 10 ft 9 in, about 2.1 m deep | her own, moulded: 12 ft 10 in across the wing transom, 11 ft 1 in at the taffrail's side |

**For L2, the lee ports, before the landing** (`Build-Ships.md` §5.4's reckoning, `PORT_SHUT_M` 0.3048 m: the sine of the heel is the sill less that, over the half-breadth; nothing moved): the file's 1.5 m on half its beam shuts at 24.3°. The sheet's four ports, as built, shut at 16.0°, 14.5°, 14.9° and 19.4°; the guns' own x at 15.0°, 14.7° and 17.3°; as drawn, 11.5° to 16.7°.

The rough reads of `Build-Ships.md` §5.9 hold: the top waterline 54 ft 1½ in against "about 52-53 ft", the drag 3 ft 0 in against "about 2.5-3 ft", the mast 8 ft 8 in against "about 7-8 ft", four ports a side, the transom 11 ft 1 in to 12 ft 10 in across against "some 11-13 ft".

These are for the lead and the owner. No figure moves here: the hull's figures carry the file's sailing pins (§5.0 principle 8, §5.6). **Ruled (the lead, 2026-10-31):** her length at the sheet's, recorded and not moved (point 6); guns and ports as built, the sheet's four kept for package 81 (point 5); the sills at 1.00 to 1.23 m and the lowest port's 14.5° flagged for the owner's test when L2 comes, a cutter's low freeboard perhaps the truth of it (point 7).

## 8. What the sources cannot give

- **The load line in words**: nothing names it; WL1 is a judgement on measures (§4.2). No draught mark, and no written draught, on any sheet; CHN0105, the manuscript in the folder, was not read and may hold some.
- **The deck at the side**: no beam's round-up is drawn (§5.3).
- **The waist's 3 ft 2 in** to the inch: 3 ft 0 in to 3 ft 1½ in on the as-built sheets, within what the previews can show (§5.3).
- **Where the three guns a side stood**: no gun, slide or carriage is drawn; four ports stand open to them (§5.8).
- **The bowsprit's side** and its outboard length on ZAZ6381: §5.9.
- **Sharper as-built figures**: the CHN images are 1024-px previews at 1.2 in a pixel; a full scan would be licensed from RMG Images. The draught's lines do not need it (judgement).
- **The depth in hold's first figure** on the sheets, Charnock settling the as-built's, and the burthen's fraction on the as-built sheets: tentative (§2.2).
- **The paint**: nothing is coloured but the inks; the wale's black is the kit's, for the eye.

## 9. Method and files

The images were read with crops and enlargements and measured by scripts kept outside the repository in the session's scratch directory, under `hulls/streams/cutter/`: `crop.py` (crops), `scale.py`, `m1.py`, `ticks.py` (the strips and perpendiculars), `sheer.py`, `sheer3.py`, `reds2.py`, `dash3.py` (the lines of the sheer, to sub-pixel by darkness centroids, in black, red or green), `greens_body.py` (the greens across the views), `hbtable.py`, `hb2.py`, `hb3.py`, `bow.py` (the half-breadth plan), `diag.py`, `horiz.py`, `bodyrefine2.py`, `tuck.py`, `final3.py` (the body plan: each section predicted from the plan and the sheer, then held to its ink, and overlaid to check by eye), `aniso.py` (§3.3), `disp.py` (§4.2), `ports.py`, `mast.py`, `mast2.py`, `ends.py`, `z82c.py`, `z82d.py` (ZAZ6382), `ch224d.py`, `ch224e.py`, `final4.py` (the as-built sheets), `ch103.py` (the stern), `points.py`, `frag.py` (the figures above), `validate.py` (§6's points through the worktree's helpers, importing `freesail` from the worktree). A second reader took the scale, the rail, the breadths, the sections, the ports, the load line, the stem and the post by its own route and scripts (`xcheck/`); this note was mended on what that found and was confirmed on the images: the rail's pair of lines, the bow's and the hollows' cells, the keel's pair of lines, the heading of CHN0103 (`mend/`). A review of the built hull laid her file and her drawn hull over the three views and took the section curves' order on black ink alone (`review/`): it mended station 2's three cells and the rail abaft 17. The owner's private pictures of the kit were looked at for the eye only (`Build-Ships.md` §5.8); no point comes from them and none was copied.
