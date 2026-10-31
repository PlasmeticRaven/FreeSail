# Pages: RMG ZAZ2587 and ZAZ2559, the *Amazon* class of 1795, her lines, frames and inboard works (October 2026)

Research for package 75's hull step, SW-2 with SW-2b.2 (`Build-Ships.md` §5, §5.4, §5.7, §5.9). It
serves `data/ships/frigate-36.yaml` and the builder of her hull, who takes the points of §8. Facts
only: the images are the museum's photographs, kept outside the repository (§1.1). It replaces
§5.9's rough reads with measures, and Steel's 36 stands beside it as a check, old beside new
(§9.2).

The marks:

- **read**: the sheet's writing or drawing was seen on the image. "tentative" is a reading at the
  limit of the image.
- **catalogue**: from the museum's catalogue: the six object pages of §1.1, read on 2026-10-30, and
  `Build-Ships.md` §5.9 for the rest of the sets.
- **measured**: off the image at the scale of §3; the uncertainty is stated in the table's heading
  or its section.
- **judgement**: reasoning by this note.
- **arithmetic**: figures of this note or the sheet's worked through.

**Units and datums.** English feet and inches, with metres where the file's profile takes them.
Positions along the ship are feet forward of **AP**, the after of the two perpendiculars the sheets
draw (§3.2). In metres they are **x forward of her middle**, the middle of WL1 rabbet to rabbet,
71.9 ft forward of AP (§4.3): `x = (ft from AP - 71.9) x 0.3048`. Heights on the sheets are taken
above **K**, the top border of the scale strip, which is the false keel's lower edge (§5.4). In
metres they are **z above WL1**, the load line (§4), at the point's own station, the line's fall of
1.46 ft over 143 ft taken out, as the 64's are (`tools/ships/indefatigable.py`): `z = (ft above K -
wl1) x 0.3048`, with `wl1 = 19.23 - 1.46 x (ft from AP) / 143`. Half-breadths in feet are moulded;
in metres they are plank on, with the 4 in of the table's extreme less moulded breadth (§2.1). The
line's tilt of 0.59° shifts x by at most 0.2 ft at the taffrail (judgement: ignored).

**Stations** are the sheets' own: 32 to 2 by twos abaft the dead flat ⊕, then B, D, F, H, K, M, O,
Q, S before it (read, §3.4), 4.87 ft apart but for 5.94 ft between 8 and 6. Two more stand before S
in the sheer and the half-breadth plan, with no letter that could be read: S+1 and S+2 here.

## 0. In brief

- **Six sheets, one scale.** Each sheet's perpendiculars stand 142.97 to 143.11 ft apart at its own
  strip's scale, against the table's 143 ft 0 in on the gun deck; the strips fit straight to
  0.17-0.30 px rms over 152 ft. The scale is 1:48 against the catalogued paper, measured; the
  catalogue states none (§3.1).
- **The sheets give more than was feared.** The sheer, the half-breadths and the ports repeat from
  sheet to sheet to about 0.05-0.1 ft for a clean line and 0.1 ft rms for the half-breadths, where
  §5.9 expected 0.2-0.4 ft. The body plan is crowded below the breadth, as expected, but its outer
  section and its topsides can be read on both copies (§3.3, §6). The limits are stated in §3.5.
- **The load line is WL1, the top green line** (judgement, §4.2): no sheet labels it. It is the
  only green line carried out to the knee of the head; the wale's lower edge lies 0 to 1 in above
  it amidships, as Steel's rule puts it; and it gives Steel's load draughts within 0.4 ft.
- **Her line stands high against the file.** To K, 19 ft 3 in aft and 17 ft 9 in forward, 18 ft 6
  in at the middle (5.64 m), with 1.46 ft of drag, against the file's 15 ft mean. WL1 is 143.5 ft
  long rabbet to rabbet (43.74 m), longer than §5.9's rough 140-142 ft, against the file's 137 ft
  (§4.3, §9.1). Recorded, not moved.
- **Thirteen upper-deck ports a side**, 9.75 ft apart and 10.92 ft across the main mast, 2 ft 11 in
  by 2 ft 5½ in; sills 7 ft 2 in above WL1 at their lowest (2.19 m) and 8 ft 4 in and 8 ft 6 in at
  the end ports (2.54, 2.59 m), 2 ft 1 in above the deck at side. Six ports a side on the
  quarterdeck, four for guns and two for carronades by their sizes and sills. None is drawn on the
  forecastle (§7).
- **A square stern with two counters**, 20 ft 5 in across at the taffrail and 25 ft 4 in at the
  wing transom (moulded), and one quarter gallery of three lights. The sheets draw no stern
  elevation, so the stern lights' count is judgement (§5.6). A knee of the head with no figure
  drawn (§5.5).
- **She is built on the points of §8** (`tools/ships/hull_frigate.py`). They pass the schema and
  `form.check`; the port triples lie within 0.02 m of the side so drawn, and the drawn displacement
  is 1,448 t against the filed 1,270 t, +14% (§8.4). Nothing was written from the drawing to a gun:
  the guns' `x_m`, calibres and numbers are the file's, and the triples at the file's own x are
  given beside the sheet's ports (§8.3).

## 1. The sources

### 1.1 The objects, the images and the cache

| Sheet | What (read) | Object, paper, vessels (catalogue) | Image in the cache, `D:/Projects/FreeSail/reference-cache/emerald-j5297/` | Size |
|---|---|---|---|---|
| **ZAZ2587** | The lines, the contract draught, stamped *Emerald* | RMG 82378, 530 x 1480 mm, *Amazon* and *Emerald* | `EMERALD_1795_RMG_J5297.jpg` | 1280 x 458 px, 128,485 bytes |
| **ZAZ2559** | The lines, *Amazon*'s own copy for Wells | RMG 82350, 525 x 1490 mm, *Amazon* | `related/j5270.jpg` | 1280 x 453 px, 135,588 bytes |
| ZAZ2588 | The frames, stamped *Emerald* | RMG 82379, 375 x 1100 mm, *Amazon* and *Emerald* | `related/j5295.jpg` | 1280 x 440 px, 137,561 bytes |
| ZAZ2560 | The frames, for Wells, stamped *Amazon* | RMG 82351, 334 x 1060 mm, *Amazon* | `related/j5264.jpg` | 1280 x 410 px, 165,709 bytes |
| ZAZ2589 | The inboard profile, stamped *Emerald* | RMG 82380, 365 x 1100 mm, *Amazon*, *Emerald*, *Glenmore* and *Trent* | `related/j5291.jpg` | 1280 x 427 px, 119,215 bytes |
| ZAZ2561 | The inboard profile, for Wells, stamped *Amazon* | RMG 82352, 355 x 1100 mm, *Amazon* | `related/j5265.jpg` | 1280 x 414 px, 120,425 bytes |

The object pages are https://www.rmg.co.uk/collections/objects/rmgc-object-<n>, read on 2026-10-30
for these fields and not kept. They give the type (lines, frame, inboard profile plan), the date
1794 and the paper; they state no scale. Each image's sides are the catalogued paper's within 2%,
so each is the whole sheet (arithmetic).

The sha256 of the images:

- ZAZ2587 `7c84fd6b41b242105c6a133981ff8af7a9bf1729673a9bd999d0c9ac005bc657`
- ZAZ2559 `941ad5b080ba200ef56a75d482437d8dfa8b41acd8fbf6f2dbc2bed608e2d6c3`
- ZAZ2588 `b5c46b535b734d6abd73a224d2ec35bbb42999a3ddfbe9965bdf4ea38e5c6564`
- ZAZ2560 `7b6da12cde5d3015eeee1ac69d8a829552384f34093de283bfe2ea52ada961a2`
- ZAZ2589 `0ebbf00724908bb84373b22e984ecd585a637dc159c06f1cfa2af9308140f428`
- ZAZ2561 `58a0636f8cb99c2e73d3d0295df636cf421eb397e780440bac8a46f4610285cc`

RMG credits every sheet "© Crown copyright. National Maritime Museum, Greenwich, London" and
licenses its images only through RMG Images (catalogue), so they are read and cited and this note
takes facts only. **Not fetched:** the deck sheets, ZAZ2562-2565 and
ZAZ2590-2593. Each download wants the owner's leave, which this step could not ask, and nothing
below rests on them (what they would add: §10). A sharper scan would be licensed from RMG Images;
the drawing does not need it (judgement).

### 1.2 What is on the sheets (read)

- **ZAZ2587 and ZAZ2559:** the body plan at the left, after body on the left of its middle line and
  fore body on the right; the sheer, bow to the right, with five green waterlines, the side's
  lines, the ports, channels, deadeyes and chain plates, the quarter gallery, the rudder, the head
  and the stumps of the masts; the scale strip; the half-breadth plan under it, with a dotted red
  line and a thin line for the floor. ZAZ2559 adds red diagonals across its half-breadth plan and
  body plan.
- **ZAZ2589 and ZAZ2561:** inboard works in red (the quarterdeck, forecastle, upper and lower
  decks, the orlop's platforms, beams, ladders, hatches, the masts, the capstan, the keelson and
  riders), the top of the side, the ports, the post, rudder and stem in black. No waterlines. The
  keel's line and the strip are as on the draughts.
- **ZAZ2588 and ZAZ2560:** every timber drawn, the ports, the deck lines in red. No waterlines.
- **On none of them:** a stern elevation, a labelled load line, a draught mark, or any figure on a
  line but the station's letter. The dead flat is marked by a crossed circle.

## 2. The captions and the dimensions

### 2.1 The dimension table (read, tentative: the figures are 5-8 px high; both copies alike; as `Build-Ships.md` §5.9 and Winfield p. 143 give them)

| | |
|---|---|
| Length on the gun deck | 143 ft 0 in |
| Length of the keel for tonnage | 119 ft 6 in |
| Breadth extreme | 38 ft 2 in |
| Breadth moulded | 37 ft 6 in |
| Depth in hold | 13 ft 6 in |
| Burthen in tons | 925 87/94 (925 read, tentative; the ninety-fourths not read, the rule's) |

The tonnage rule on these figures gives 925.9, which is 925 87/94, so the figures hang together
(arithmetic). They are Winfield 1793-1817 p. 143's for the class. The plank is 4 in, half of
extreme less moulded (arithmetic).

### 2.2 The guns

"Upper deck 26 of 18 Pounders; Quarterdeck 8 - 9; Forecastle 2 - " and a two-figure calibre, "36"
under them (read). The forecastle's calibre has two strokes on both copies, 12 or 18, not the 9
above it (tentative). Winfield p. 143 has 9-pounders on the forecastle of the first pair and
12-pounders on the second, and adds carronades, which the table does not name. Recorded only: the
file's fit keeps every calibre and number, its quarterdeck INCORRECT by the owner's ruling
(`Build-Ships.md` §11).

### 2.3 The titles and notes

- **ZAZ2587** (tentative in its words): "A Draught prepared for building by contract on the River
  Thames two Frigates to carry 36 Carriage Guns each", Navy Office, May 1794, signed by Rule; to
  the left, approved by the Lords Commissioners on 29 May 1794; top right, a copy to Wells at
  Rotherhithe for the *Amazon* and another to Pitcher at Northfleet for the *Emerald*, as §5.9 has
  it.
- **ZAZ2559:** the draught for building by Messrs John William and John Wells Junior at
  Rotherhithe, a ship to carry 36 carriage guns, Navy Office, May 1794 (the day tentative), signed.
- **ZAZ2589:** "Profile Draught for a Ship of 36 Guns", with copies to Wells for the *Amazon* and
  to Pitcher for the *Emerald*, June 1794, and a further line, a copy to Woolwich, July 1794
  (tentative); the catalogue files the sheet under *Glenmore* and *Trent* as well as *Amazon* and
  *Emerald*.
- **ZAZ2561:** the inboard works of the 36-gun ship building at Rotherhithe, Navy Office, June
  1794, with a note on an alteration, not read to its end. **ZAZ2588, ZAZ2560:** "Disposition of
  the Frames".
- The curator's stamps file ZAZ2587, ZAZ2588 and ZAZ2589 under *Emerald*, the others under
  *Amazon* (read); the catalogue files those three under *Amazon* as well (§1.1). No stamp or line
  separates the two ships' hulls (read). The stations, ports and lines
  of the two sets are one design to within the differences of §3.3 (measured).

## 3. The scale and its check

### 3.1 The strips (measured)

Each strip is labelled twice, 0 to 150 ft each way, ten feet to a number, with a foot tick and a
diagonal scale at each end (read). The foot ticks fit a straight line. The sheets are at one scale,
1:48 (measured): each strip against its sheet's catalogued length, the image's 1,280 px taken as
that length (§1.1), gives 1:48.3, 1:48.3, 1:48.1, 1:48.4, 1:48.1 and 1:48.4 in the table's order;
the catalogue states no scale, and the 1:48 of `Build-Ships.md` §5.9 is that document's word. Their
px to the foot differ because the photographs do.

| Sheet | px to the foot | Foot ticks used, over 152 ft | rms, largest (px) | 1 px is | Strip's top, K, as a row y at column x |
|---|---|---|---|---|---|
| ZAZ2587 | **5.4582** | 153 | 0.18, 0.65 | 0.18 ft | 3.2e-6 x² - 0.00408 x + 297.36 (rms 0.09) |
| ZAZ2559 | **5.4258** | 148 | 0.30, 0.83 | 0.18 ft | 2.3e-6 x² - 0.00179 x + 297.23 (rms 0.11) |
| ZAZ2589 | **7.3710** | 153 | 0.19, 0.49 | 0.14 ft | 2.4e-6 x² - 0.00412 x + 327.92 (rms 0.07) |
| ZAZ2561 | **7.3281** | 152 | 0.29, 0.73 | 0.14 ft | 4e-7 x² - 0.00021 x + 323.91 (rms 0.05) |
| ZAZ2588 | **7.3734** | 51 (the ticks show faint) | 0.17, 0.50 | 0.14 ft | 1.9e-6 x² - 0.00335 x + 338.70 (rms 0.07) |
| ZAZ2560 | **7.6123** | 47 (the same) | 0.30, 0.62 | 0.13 ft | 4e-7 x² - 0.00268 x + 328.18 (rms 0.08) |

### 3.2 The stated dimensions measured back

| Dimension | Stated (read) | Measured | Basis |
|---|---|---|---|
| Length on the gun deck | 143 ft 0 in | **143.05** ZAZ2587, **143.11** ZAZ2559, **143.00** ZAZ2589, **142.99** ZAZ2561, **142.97** ZAZ2588, **142.99** ZAZ2560 | the two perpendiculars, each a thin vertical (red on the draughts forward) drawn from the strip up: at x = 378.2 and 1159.0 px; 386.0 and 1162.5; 111.9 and 1165.9; 116.1 and 1163.9; 132.1 and 1186.3; 103.1 and 1191.6; ±0.5 px. They fall on the strip's foot ticks |
| Breadth moulded | 37 ft 6 in | **37.58** ft ZAZ2587, **37.43** ft ZAZ2559 | the body plan's outer section across its dead flat, the heavy line's centres (±0.1 ft) |
| The same, the half-breadth plan | 18 ft 9 in a side | 18.62 ft on both copies | the main-breadth line above the plan's middle line. It reads 0.13 ft (0.7 px) short at the middle, and the waterlines short by the same against the body plan at their own heights (0.6 to 1.2 px, with no trend in the breadth), so a constant, not a scale. **Every half-breadth in this note has 0.14 ft added for it** (judgement) |
| Breadth extreme | 38 ft 2 in | not drawn | the sheets draw the moulded lines; the plank is arithmetic (§2.1) |
| Depth in hold | 13 ft 6 in | 13.55 ft, ZAZ2589 | the lower deck's top line at the middle line down to a line over the keelson at ⊕, the ceiling (judgement on which line; a weak check) |
| Keel for tonnage | 119 ft 6 in | not a drawn length | K runs 134.4 ft from the post's heel to the knee's foot (§5.4); the rule's keel for tonnage is an arithmetic length |

**Where the perpendiculars stand** (measured): AP cuts the post's fore face, the rabbet, at WL1
(0.1 ft before it there). FP is 0.6 ft abaft the stem's rabbet at WL1, and cuts it about 15 ft
above K. Rabbet to rabbet at the height of the lower deck the length is 143.7 ft (143.68-143.79 on
four sheets), at the upper deck's about 146.1 ft (the post's line carried up from 25 ft). The
table's 143 ft is nearer the lower deck and equals neither; the two perpendiculars stand 143.0 ft
apart, AP on the rabbet at WL1 and FP on it about 15 ft above K (judgement on which deck).

### 3.3 Sheet against sheet (measured)

| What | Compared | Mean difference (ft) | rms (ft) | Largest (ft) |
|---|---|---|---|---|
| Top of the side, by station | ZAZ2561 against ZAZ2589 | 0.00 | 0.04 | 0.07 |
| The same | ZAZ2588, ZAZ2560 against ZAZ2589 | -0.03, -0.05 | under 0.05 | 0.12 |
| The same, the quarterdeck's rail only | ZAZ2587, ZAZ2559 against ZAZ2589 | -0.04, +0.11 | 0.04 | 0.14 |
| Upper deck, two lines | ZAZ2561 against ZAZ2589 | 0.00, -0.02 | 0.05, 0.04 | 0.11 |
| Quarterdeck, two lines | the same | 0.00, +0.02 | 0.04, 0.02 | 0.09 |
| Forecastle, two lines | the same | -0.04, -0.04 | 0.04, 0.02 | 0.11 |
| Lower deck, two lines | the same | -0.02, 0.00 | 0.04, 0.06 | 0.24 |
| Upper deck, on the sheer plans | ZAZ2587, ZAZ2559 against ZAZ2589 | -0.03, +0.09 | 0.08, 0.09 | 0.33 |
| The wale's lower edge | ZAZ2559 against ZAZ2587 | +0.09 | 0.04 | 0.15 |
| The wale's upper edge | the same | +0.15 | 0.12 | 0.36 |
| Heights of breadth, upper and lower | the same | +0.12, +0.08 | 0.07, 0.10 | 0.30 |
| Every half-breadth, 206 readings | the same | +0.02 | 0.10 | 0.41 (four over 0.3, at crossings) |
| Upper-deck ports' centres, 13 | all six sheets | | within ±0.15 ft of the mean | 0.19 |
| Upper-deck sills, 13 | the four inboard and frame sheets and ZAZ2587 | | within ±0.05 ft | 0.06 |
| Quarterdeck ports' centres and sills, 6 | all six sheets | | within ±0.15 ft | 0.19 (a centre); 0.16 (a sill on the draughts) |

- ZAZ2559's ports 5 to 9 and ZAZ2587's port 6 are not in the sills' row: their tops and sills lie
  among the heavy lines there and the finder took the wrong ones. Read on the columns at ⊕ they
  agree (read).
- **The waist's top, on the two kinds of sheet:** ZAZ2589, ZAZ2561, ZAZ2588 and ZAZ2560 have a
  heavy line, 29.87 ft above K at ⊕, with a thin one 0.25 ft above it. ZAZ2587 and ZAZ2559 have a
  thin line at 30.02 and 30.05 ft, between those two, with heavy lines at 29.30 and 29.45 and at
  28.5 and 28.6 ft below it. It is one line inked lighter on the draughts, and the inboard sheets'
  heavy line is taken as the rail (judgement). The top of the waist is good to ±0.15 ft.

### 3.4 The stations (read, tentative for each figure; measured for their places)

The letters are about 6 px high. They read best on the frame sheets at 7.6 px to the foot, and the
sequence settles them: 32, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, ⊕, B, D, F, H,
K, M, O, Q, S, every second timber, a timber's room being 2.43 ft (arithmetic). Their places agree
across the sheets within 0.1 ft: ⊕ stands 82.54 ft from AP on ZAZ2587 and 82.63 on ZAZ2589.

### 3.5 What the resolution gives, plainly

- **A clean line's height: to 0.05-0.1 ft between sheets** (§3.3), better than a pixel, since the
  sheets were copied closely and a line's centre can be found to a fifth of a pixel. A pixel is 2
  in on the draughts and 1½ in on the others; this is the fit's precision, not an eye's, and it
  says the copies agree, not that either is true to the inch.
- **Height above the load line: ±0.15 ft on top of that**, from WL1's own fit: its height above K
  at AP reads 19.23 ft on ZAZ2587 and 19.47 ft on ZAZ2559, at FP 17.77 and 17.83 ft.
- **A half-breadth: ±0.1 ft from S+1 back to 30**, and ±0.3-0.4 ft where two lines cross or run
  together and at the last few feet of the ends. Where WL1 runs in the main-breadth line (station
  20 to H) it cannot be told from it, and the water is taken from the section, 0.05 ft inside.
- **A station's section under the breadth: not from the body plan.** It is too crowded there. The
  sections are built from the waterlines by station as the 64's were (`Build-Ships.md` §5.7; Indf
  §3.5 item 8), five points under the water 3.32 ft apart; then, at the stations where §6.3 can
  follow the line between the water and the breadth, its rows; then the main breadth, then the
  topside.
- **Not given at all:** §10.

## 4. The waterlines and the load line

### 4.1 The five green lines (measured)

Fitted straight along their green ink alone, on columns clear of the black lines, in feet above K:

| Line | ZAZ2587, at AP | at FP | fall | ZAZ2559, at AP | at FP | rms (px) |
|---|---|---|---|---|---|---|
| WL1 | 19.23 | 17.77 | 1.46 | 19.47 | 17.83 | 0.50, 0.40 |
| WL2 | 15.89 | 14.51 | 1.39 | 15.86 | 14.72 | 0.29, 0.49 |
| WL3 | 12.60 | 11.10 | 1.50 | 12.56 | 11.17 | 0.43, 0.54 |
| WL4 | 9.27 | 7.84 | 1.43 | 9.46 | 7.83 | 0.33, 0.49 |
| WL5 | 5.96 | 4.67 | 1.29 | 6.15 | 4.68 | 0.29, 0.41 |

- ZAZ2559's WL4 is faint, and is fitted on the green less red index, not the green ink alone.
- They are parallel within the fit and stand **3.32 ft apart**, which is 3 ft 4 in as drawn
  (judgement); this note takes WL2 to WL5 as 3.32 ft each below the one above. The keel is level on
  the sheet: she is drawn with **1.46 ft of drag over the 143 ft** (0.59°), as the body plan shows
  too, its waterlines higher in the after body than in the fore body.
- A station's height of WL1 above K is in §5.2; subtract 3.32 ft for each line down.

### 4.2 Which is the load line, and how it was judged

No sheet labels it; §5.9 says so and this reading agrees. **WL1, the top green line, is taken as
the load line** (judgement), on six grounds:

1. **It alone runs out to the knee of the head** on both copies, to x = 1181 px on ZAZ2587, 147.1
   ft from AP; the other four stop at the stem's rabbet (read). The 64's WL1 is marked out the same
   way (Ind §2.3.1).
2. **Steel's definition:** the load water line is the highest of the waterlines (1805 text p. 188,
   read in Ind §2.3.1).
3. **Steel's rule for the wale:** its lower edge "nearly at the same height as the load-water
   line", a few inches higher (OCR `:15190-15193`). Here it stands 0.01 to 0.02 m above WL1 from
   station 6 to B, and 0.09 ft above it on ZAZ2559 at ⊕ (measured).
4. **Steel's draughts for the 36:** Folio I's 17 ft 4 in forward and 18 ft 4 in aft (read there,
   `Build-Ships.md` §5.4). WL1 stands 17.2 ft forward and 18.7 ft aft above the main keel's lower
   edge (K less about 0.55 ft: §5.4), within 0.1 and 0.35 ft (measured).
5. **Steel's height of the port:** 7 ft 8 in above the water amidships, here 7 ft 2 in to 7 ft 4 in
   (§7.1), and the lower deck just under the line amidships (§5.3), which is where a frigate of the
   time carried it (judgement).
6. **Steel's rule for the load line** (OCR `:15178-15187`, the ground `Build-Ships.md` §5.4 names):
   one-fifth of 143 ft is 28.6 ft, the top-timber line at its lowest, the draughts' second heavy
   line; five-eighths of that is 17.9 ft, against WL1's 17.8-17.9 ft above the main keel at ⊕
   (arithmetic, measured).

Winfield p. 143's 10 ft 3 in and 15 ft 3 in for *Amazon* as built name no condition. They are no
line on these sheets: at the drawn drag, a line 15 ft 3 in above K aft would stand about 4 ft below
WL1 aft and over 7 ft below it forward, near WL2 aft and near WL3 forward, with 5 ft of drag where
the sheets draw 1.46 ft. So they are not the design's load line (judgement); light, as the file's
note has it, fits them.

### 4.3 Its length and draught (measured; each ±0.3 ft)

| On WL1 | ft from AP | x (m) |
|---|---|---|
| The rudder's after edge | -4.5 | -23.29 |
| The post's after face | -1.3 | -22.31 |
| The post's rabbet | +0.1 | -21.88 |
| **The middle of the line, the file's x = 0 here** | **71.9** | **0.00** |
| The stem's rabbet (ZAZ2587, ZAZ2589 both 143.64; the plan's end 143.3) | +143.64 | +21.87 |
| The stem's fore edge | +144.2 | +22.04 |
| The knee of the head's fore edge | +147.1 | +22.92 |

- **Length:** **143.5 ft rabbet to rabbet** (43.74 m), 145.5 ft outside the post and stem (44.35
  m), 148.4 ft from the post's after face to the knee (45.23 m). §5.9's "about 140-142 ft" was a
  rough read; the file has 137 ft (41.8 m).
- **Depth:** WL1 stands **19.23 ft above K at AP (5.86 m), 17.77 ft at FP (5.42 m), 18.50 ft at x =
  0 (5.64 m)**. Above the rabbet's line, the heavy base line, 17.0 ft at x = 0. §5.9's "about 16-17
  ft above the keel" is that figure. The file has 15 ft (4.6 m).

## 5. The profile, measured

### 5.1 The lines of the side (read for what is drawn, measured for its figures; identification as marked)

- **The rail**, black and heavy: the quarterdeck's rail from the taffrail to its fore end at 63.2
  ft; a scroll down to the waist rail by 65.5 ft; the waist rail to 103.9 ft; a scroll up, its knob
  at 104.4 ft, to the forecastle's rail by 106.1 ft; that to the stem head. Read off ZAZ2589, ±0.05
  ft.
- **The plank-sheer**, black, under the quarterdeck's rail and broken at its ports: 1.8 ft under
  the rail at station 30, 2.3 ft at station 14, then dropping by a step at about 57 ft to run into
  the waist's scroll (judgement on its name).
- **The red lines of each deck**, two a deck (§5.3).
- **The line through the ports**, black, broken at each port, at mid-height of the upper-deck ports
  from stern to stem (judgement: a strake's edge; the only band drawn there; not the channel wale,
  §5.7).
- **The dashed lines**, two, under the upper-deck ports: Steel's upper and lower heights of breadth
  (§5.7).
- **The heavy line under them:** the main wale's lower edge, which sweeps up under the quarter
  gallery. A faint line parallel to it and 3.68 ft above it is the wale's upper edge (judgement;
  Steel's wale is 3 ft 9 in broad).

### 5.2 By station: the rail and the decks (measured)

Feet above WL1 at the station, but for the columns of place and WL1's own height above K. The rail
±0.05 ft, the decks ±0.1 ft, each on ZAZ2589 and within §3.3 of ZAZ2561, and each besides ±0.15 ft
for WL1 (§3.5).

| Station | ft from AP | m from x = 0 | WL1 above K | Rail | Upper deck, top line | Upper, second line | Quarterdeck, top | Quarterdeck, second | Forecastle, top | Forecastle, second | Lower deck, top | Lower, second |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 32 | 3.62 | -20.81 | 19.19 | 17.49 | 7.11 | 6.46 | 13.98 | 13.37 |  |  | 0.50 | 0.17 |
| 30 | 8.50 | -19.32 | 19.14 | 17.26 | 6.94 | 6.24 | 13.73 | 13.11 |  |  | 0.36 | 0.00 |
| 28 | 13.34 | -17.85 | 19.09 | 17.05 | 6.72 | 6.05 | 13.61 | 12.93 |  |  | 0.16 | -0.18 |
| 26 | 18.23 | -16.36 | 19.04 | 16.84 | 6.50 | 5.86 | 13.40 | 12.70 |  |  | -0.01 | -0.41 |
| 24 | 23.11 | -14.87 | 18.99 | 16.66 | 6.40 | 5.69 | 13.25 | 12.48 |  |  | -0.17 | -0.58 |
| 22 | 27.91 | -13.41 | 18.95 | 16.48 | 6.17 | 5.54 | 13.16 | 12.37 |  |  | -0.33 | -0.69 |
| 20 | 32.81 | -11.91 | 18.90 | 16.33 | 6.17 | 5.40 | 12.94 | 12.20 |  |  | -0.46 | -0.83 |
| 18 | 37.71 | -10.42 | 18.85 | 16.20 | 5.95 | 5.29 | 12.79 | 12.06 |  |  | -0.57 | -0.92 |
| 16 | 42.58 | -8.94 | 18.80 | 16.10 | 5.84 | 5.15 | 12.63 | 11.94 |  |  | -0.55 | -1.06 |
| 14 | 47.45 | -7.45 | 18.75 | 15.98 | 5.76 | 5.08 | 12.63 | 11.88 |  |  | -0.74 | -1.13 |
| 12 | 52.30 | -5.98 | 18.70 | 15.90 | 5.79 | 4.98 | 12.51 | 11.72 |  |  | -0.71 | -1.22 |
| 10 | 57.08 | -4.52 | 18.65 | 15.82 | 5.65 | 4.75 | 12.34 | 11.69 |  |  | -0.77 | -1.26 |
| 8 | 62.01 | -3.01 | 18.60 | 15.76 | 5.61 | 4.90 | 12.28 | 11.59 |  |  | -0.93 | -1.25 |
| 6 | 67.95 | -1.20 | 18.54 | 11.52 | 5.59 | 4.87 |  |  |  |  | -0.89 | -1.34 |
| 4 | 72.78 | +0.27 | 18.49 | 11.49 | 5.65 | 4.88 |  |  |  |  | -0.83 | -1.36 |
| 2 | 77.67 | +1.76 | 18.44 | 11.48 | 5.66 | 4.89 |  |  |  |  | -0.92 | -1.34 |
| ⊕ | 82.58 | +3.25 | 18.39 | 11.51 | 5.65 | 4.90 |  |  |  |  | -0.86 | -1.31 |
| B | 87.40 | +4.72 | 18.34 | 11.56 | 5.73 | 4.98 |  |  |  |  | -0.82 | -1.26 |
| D | 92.29 | +6.22 | 18.29 | 11.64 | 5.84 | 4.97 |  |  |  |  | -0.77 | -1.20 |
| F | 97.14 | +7.69 | 18.24 | 11.74 | 5.87 | 5.11 |  |  |  |  | -0.60 | -1.11 |
| H | 101.97 | +9.17 | 18.19 | 11.87 | 5.87 | 5.20 |  |  |  |  | -0.52 | -1.06 |
| K | 106.87 | +10.66 | 18.14 | 13.16 | 5.98 | 5.32 |  |  | 12.68 | 12.01 | -0.48 | -0.90 |
| M | 111.75 | +12.15 | 18.09 | 13.31 | 6.10 | 5.44 |  |  | 12.74 | 12.16 | -0.38 | -0.78 |
| O | 116.58 | +13.62 | 18.04 | 13.48 | 6.19 | 5.59 |  |  | 12.94 | 12.26 | -0.23 | -0.64 |
| Q | 121.48 | +15.11 | 17.99 | 13.72 | 6.32 | 5.74 |  |  | 13.00 | 12.41 | -0.14 | -0.50 |
| S | 126.33 | +16.59 | 17.94 | 13.94 | 6.51 | 5.87 |  |  | 13.17 | 12.60 | 0.03 | -0.32 |
| S+1 | 131.19 | +18.07 | 17.89 | 14.19 | 6.69 | 5.98 |  |  | 13.28 | 12.79 | 0.21 | -0.14 |
| S+2 | 136.09 | +19.56 | 17.84 | 14.46 | 6.81 | 6.23 |  |  | 13.45 | 12.96 | 0.43 | 0.06 |

- **The sheer** (measured): the waist rail is lowest at station 2, 11.48 ft above WL1 (3.50 m), and
  rises to 11.87 ft by its forward end at H; the quarterdeck's rail from 15.76 ft at its fore end
  to 17.49 ft at station 32, 18.9 ft at the taffrail's lower horn and 19.8 ft at its top, the upper
  horn (§5.6); the forecastle's from 13.16 ft at K to 15.17
  ft at the stem head. Against K the same rail is lowest at 29.90 ft at ⊕ and B. The sills, the
  deck and the wale are all lowest within a few feet of x = 0, by the 1.46 ft of drag taken out of
  them.

### 5.3 The decks and their ends (measured; identification judgement)

- **Each deck is drawn with two red lines**, on the inboard sheets and on the sheer plans alike.
  The top line is the deck's surface at the middle line, with the beams in section hung below the
  second. The two stand 0.75 ft apart on the upper deck, 0.61-0.69 ft on the quarterdeck, 0.5-0.7
  ft on the forecastle and about 0.44 ft on the lower deck.
- **The deck at side** is taken as **the second line and 0.25 ft**, the plank (judgement). The
  check: the upper-deck sills then stand 2.08 to 2.13 ft above it along the whole ship, against
  Steel's 36's 2 ft 2 in; the quarterdeck's gun-port sills 1.53-1.58 ft against Steel's 1 ft 7 in,
  and its carronade-port sills 0.94-0.96 ft against Steel's 11 in (`pages-steel-1805-bodies.md`
  §5.3). So the round-up is 0.5 ft on the upper deck, against Steel's 7 in.

| Deck | From | To | At the middle line at x = 0 (z, ft / m) | At side at x = 0 (ft / m) | Lowest at side |
|---|---|---|---|---|---|
| Quarterdeck | -8.9 ft from AP, the red lines' end on ZAZ2589 (at the stern's inner line) | its breast at 63.9 ft (x -2.44), a beam's box before it; the rail ends at 63.2 ft | | 11.8 / 3.61 at its breast | 3.61 m, at the breast |
| Upper | about -2 ft | the stem, about 144.5 ft | 5.65 / 1.72 | 5.09 / 1.55 | 1.55 m, stations 6 to 4 |
| Forecastle | 106.1 ft (x +10.42), at the scroll | the stem, about 144.5 ft | | 12.2 / 3.73 at its after end | 3.73 m, at its after end |
| Lower | about +2 ft | about 143 ft | -0.85 / -0.26 | -1.08 / -0.33 | -0.33 m, under the water from x -17 to +17 |
| Orlop's platforms | 23-43, 57-90 and 100-139 ft | | about -6.1 ft / -1.86 m (tentative) | | |

The open waist runs 65.7 to 103.9 ft between the scrolls, 38.2 ft. The quarterdeck is carried about
73 ft from its after end, the forecastle 38.4 ft (Steel's 36: 36 ft 0 in).

### 5.4 The keel and the rabbet (measured)

| Line, above K | ZAZ2587 | ZAZ2589 | ZAZ2559 | What (judgement) |
|---|---|---|---|---|
| K, the strip's top border | 0 | 0 | 0 | the false keel's lower edge; the post's heel ends on it |
| A pale line | 0.53-0.56 | 0.56-0.61 | 0.57-0.68 | the false keel's top, the main keel's lower edge: about 6½ in, Steel's 5 in |
| The heavy base line | 1.48 | 1.55 | 1.65 | the rabbet, which runs on up the stem as the same heavy line, where the waterlines end |
| A thin line just over it | 1.83 | 1.8 | | the main keel's top (the body plan's keel box has its top there too) |

- The heel of the post's after face stands **0.87 ft before AP**, on K (ZAZ2587 0.88, ZAZ2589
  0.85).
- The rabbet leaves the base line about 126-129 ft from AP. **The false keel ends square at 132.65
  ft** (132.7 on ZAZ2587, 132.6 on ZAZ2589). The knee's fore edge comes down to K at **135.25 ft**.
  The stem's fore edge is boxed into the keel 1.1 ft above K at 129.4 ft. A dashed line carries the
  rabbet's height on from the stem to FP (read).
- **The keel box** in the body plan: 1.2-1.3 ft sided (half-siding 0.6 ft), about 1.8 ft high to the
  keel's top, its bottom on K (measured, both copies). The section's line has already flared where
  it meets the box's top, §6.2's 0.87 ft. The post's rabbet in plan: the waterlines end 0.46-0.56 ft
  from the middle line.

### 5.5 The stem and the head (measured)

- **The stem's rabbet**, the heavy line, read by rows on ZAZ2589 and within 0.3 ft on ZAZ2587: from
  the keel at about 127 ft through 143.64 ft at WL1 to the top, 145.9 ft, 15 ft 2 in above WL1 at
  the rail's end.
- **The stem's fore edge**, the line 0.4-0.7 ft outside it, §8's `stem_m`: 144.2 ft at WL1. Its top
  is the **stem head at 146.2 ft, 15.0 ft above WL1 (x +22.66, z 4.58)**.
- **The knee of the head's fore edge**, a thin line on the two draughts only, §8's `head_m`: from K
  at 135.25 ft, through WL1 at 147.1 ft, and up to its top, **16.9 ft above WL1 at 159.4 ft (x
  +26.66, z 5.15)**. Both copies draw it alike (read).
- **On the knee** (read): the head rails, three short timbers, the cheeks, two hawse holes and the
  cathead. **No figure is drawn**: the knee's top is blank, with a small mark at the rail's end.
  The figure stays judgement (§8.5).
- **Two hawse holes** at 141.6 and 143.2 ft, 9.75 ft above WL1 (ZAZ2589). Timberheads stand above
  the forecastle's rail on the draughts, about 3 ft high.

### 5.6 The stern (measured)

- **The post's after face**, the heavy line: 0.87 ft before AP at K, 1.3 ft abaft it at WL1, raking
  6.5° to K. It runs straight on to 5.7 ft above WL1 at 1.98 ft abaft AP, where the counter leaves
  it.
- **The rudder** (the blade's after edge, heavy, on all four sheets that draw it): 4.5 ft abaft AP
  at WL1, down to 4.0 ft at the heel. Its breadth is 3.2 ft at the water and 4.7 ft at the heel,
  2.4 ft above the hance, which stands 1.0 ft above WL1. Its head is 7.1 ft above WL1. Immersed
  about 18.6 ft deep, about 73 sq ft (6.8 m²; ±10%). Five lines cross it (read), the braces and
  pintles.
- **The counters and the taffrail**, on ZAZ2587's outer line, ±0.2 ft, about 0.1 ft from ZAZ2589's
  thin line up to 33 ft above K:

| Point | ft from AP | ft above WL1 | x, z (m) |
|---|---|---|---|
| Where the counter leaves the post | -1.98 | 5.7 | -22.52, 1.74 |
| The lower counter's knuckle | -6.3 | 8.6 | -23.83, 2.63 |
| The upper counter's knuckle | -7.3 to -8.1 | 10.1 to 10.8 | -24.15 to -24.39, 3.07-3.29 |
| The taffrail's lower horn | -11.6 to -10.7 | 18.9 (ZAZ2559: the same, within 0.3 ft) | -25.33, 5.75 |
| The taffrail's top, the upper horn | -11.0 to -10.1 | 19.8 (both draughts) | -25.27 to -24.99, 6.03 |

Two horns stand one over the other on both draughts at the top of the stern; the names are
judgement.

- **The stern board in the after body** (body plans, both copies, ±0.1 ft), four lines across it,
  each rounded up to the middle line:

| Line (judgement on names) | At the middle line, ft above WL1 (m) | Round-up (ft) | Half-breadth at its end, moulded (ft) |
|---|---|---|---|
| The wing transom, the transom's foot | **4.50 (1.37)**; at its ends **4.10 (1.25)** | 0.40 | **12.65** (body 12.62, plan 12.66) |
| The lower counter | 8.53 (2.60) | 0.53 | 11.3 |
| The upper counter | 10.57 (3.22) | 0.60 | 10.85 |
| Under the taffrail | 14.27 (4.35) | 0.27 | 10.4 |
| The top | | | **10.2** (body 10.04, plan 10.32, Steel's Folio LI 10.38) |

- **The two are not reconciled, plainly:** the sheer's outline leaves the post 1.2 ft above the
  wing transom at the middle line, as the 64's does by 1 ft 3 in (`tools/ships/indefatigable.py`).
  The line above the wing transom may be the fashion piece's or the rudder trunk's. `knuckle_z_m`
  takes the wing transom's ends, as hers does.
- **In plan** (ZAZ2587): the wing transom's edge from 1.2 ft abaft AP at the middle line to 0.7 ft
  at its end, so rounding aft 0.5 ft; the stern's top from 8.9 ft abaft AP at the middle line to
  8.0 ft at its end. That is ZAZ2589's heavy inner line at the plank-sheer's height, 8.7 ft abaft
  AP. The sheer's outer line, with the rails on it, stands about 1.5 ft farther aft at that height
  and reaches 11.2 ft at the lower horn (measured; judgement on what each is).
- **The quarter gallery, one tier** (read on both draughts for what is drawn, measured for its
  figures): three lights, with a fore quarter-piece. The lights from 5.6 ft abaft to 2.7 ft before
  AP (ZAZ2587 -5.62, +2.62; ZAZ2559 -5.70, +2.76), their tops at 13.2 ft above WL1 and their foot
  10.0 ft at the aftmost, falling to 9.6 ft forward (±0.15 ft). The whole tier, the quarter piece at
  6.8 ft abaft AP (9.5 ft above WL1) to 4.1 ft before it, its top rail at 13.5 ft and base rail at
  8.6 ft, and the lower finishing to 5.7 ft under it. A small drop finial under that (read).
- **The stern lights: not on the sheets.** There is no stern elevation in the six, and the body
  plan's stern board shows none (read). **Judgement** in §8.5: a band from the upper counter at the
  middle line to the top of the gallery's aftmost light, by Steel's method, five lights as the 64
  has on her own elevation; marked `judged`.

### 5.7 The wales and the heights of breadth (measured)

Feet above WL1. The wale's lower edge ±0.05 ft, the rest ±0.1 ft, ±0.3 ft forward of S where they
cross; each besides ±0.15 ft for WL1.

| Station | ft from AP | Wale, lower edge | Wale, upper edge | Upper height of breadth | Lower height of breadth | Rising line | Line through the ports |
|---|---|---|---|---|---|---|---|
| 32 | 3.62 | 2.76 | 6.43 |  |  |  | 11.18 |
| 30 | 8.50 | 2.40 | 6.20 | 4.51 | 4.20 |  | 10.72 |
| 28 | 13.34 | 2.07 | 5.72 | 4.28 | 3.61 |  | 10.35 |
| 26 | 18.23 | 1.78 | 5.44 | 3.95 | 3.12 |  | 10.10 |
| 24 | 23.11 | 1.50 | 5.18 | 3.71 | 2.65 |  | 9.73 |
| 22 | 27.91 | 1.24 | 4.90 | 3.46 | 2.26 |  | 9.46 |
| 20 | 32.81 | 1.02 | 4.70 | 3.24 | 1.97 |  | 9.23 |
| 18 | 37.71 | 0.82 | 4.52 | 3.05 | 1.59 |  | 9.05 |
| 16 | 42.58 | 0.64 | 4.33 | 2.88 | 1.37 |  | 8.83 |
| 14 | 47.45 | 0.49 | 4.13 | 2.74 | 1.22 | -5.05 | 8.70 |
| 12 | 52.30 | 0.37 | 4.01 | 2.69 | 1.07 | -8.69 | 8.58 |
| 10 | 57.08 | 0.27 | 3.95 | 2.68 | 0.95 | -11.55 | 8.45 |
| 8 | 62.01 | 0.14 | 3.80 | 2.68 | 0.85 | -13.36 | 8.35 |
| 6 | 67.95 | 0.06 |  | 2.68 | 0.88 | -15.11 | 8.40 |
| 4 | 72.78 | 0.03 |  | 2.76 | 0.93 | -15.95 | 8.29 |
| 2 | 77.67 | 0.02 | 3.70 | 2.82 | 0.95 |  | 8.28 |
| ⊕ | 82.58 | 0.04 | 3.74 | 2.84 | 1.01 |  | 8.29 |
| B | 87.40 | 0.07 | 3.81 | 2.94 | 1.08 |  | 8.34 |
| D | 92.29 | 0.18 | 3.89 | 3.02 | 1.14 | -15.97 | 8.43 |
| F | 97.14 | 0.31 | 3.95 | 3.11 | 1.28 | -15.18 | 8.53 |
| H | 101.97 | 0.43 | 4.08 | 3.28 | 1.45 | -13.64 | 8.59 |
| K | 106.87 | 0.57 | 4.25 | 3.46 | 1.81 | -11.44 | 8.80 |
| M | 111.75 | 0.74 | 4.38 | 3.75 | 2.17 | -7.78 | 8.94 |
| O | 116.58 | 0.93 | 4.64 | 4.04 | 2.66 | -2.15 | 9.12 |
| Q | 121.48 | 1.15 | 4.85 | 4.39 | 3.23 |  | 9.38 |
| S | 126.33 | 1.38 | 5.06 | 5.06 | 3.86 |  | 9.64 |
| S+1 | 131.19 | 1.64 | 5.36 | 5.36 | 4.57 |  | 9.90 |
| S+2 | 136.09 | 1.93 | 5.59 | 6.12 | 5.50 |  | 10.19 |

At stations 2, ⊕ and B the rising line runs in the keel's top line, about -16.6 ft (tentative).

- **The main wale** is 3.68 ft broad (20.1 px, within 0.1 ft along the whole length). Its lower
  edge is lowest at stations 4 to ⊕, on WL1 within an inch; it rises 2.8 ft by station 32 and 1.9
  ft by S+2. Its upper edge runs into the gallery's lower finishing aft of 32, and the lower edge
  ends on the stem's rabbet at 144.2 ft.
- **The upper height of breadth** stands 2.7 to 2.9 ft above WL1 amidships and rises to 4.5 ft at
  station 30 and about 6 ft at S+2; **the lower** 0.9 to 1.0 ft, to 4.2 and 5.5 ft. They meet aft
  at the counter. Between them the midship section is straight (§6.2), which is what names them, as
  Steel's rule does (OCR `:15190-15194`).
- **No channel wale is drawn** (read). The chain plates end across the upper-deck ports' height and
  under, with no band there. `channel_wales_m` is left out by principle 9. If the viewer wants a
  band, the line through the ports stands in the table, marked `judged` if used.
- **The channels** (read; places ±1 ft, tentative): mizen about 10 to 21 ft from AP, main 34 to 62
  ft, fore 102 to 126 ft, at about 11 ft above WL1 (the body plan's stub at the side, 10.3 ft at
  ⊕). Deadeyes: six on the mizen with two backstays abaft, thirteen on the main and twelve on the
  fore with their backstays.

### 5.8 The masts and the bowsprit (measured, ZAZ2589, checked on ZAZ2561 and on the draughts' stumps)

| Mast | Centre at the upper deck, ft from AP | x (m) | Rake to K | Breadth drawn | ZAZ2561 | After edge on ZAZ2587 / ZAZ2559 at the stump |
|---|---|---|---|---|---|---|
| Fore | **126.32** | **+16.59** | none to 0.1° | 1.95 ft | 126.30 | 125.29 / 125.30 (ZAZ2589 125.36) |
| Main | **62.47** | **-2.87** | 0.8° | 2.35 ft | 62.5 | 61.04 / 61.05 (ZAZ2589 61.15) |
| Mizen | **21.44** | **-15.38** | 2.2° | 1.45 ft | 21.5 | 20.25 / 20.15 (ZAZ2589 20.35) |

- ±0.2 ft. The rake is off the one mast's after edge from above the rail to the hold, and is to K,
  so to WL1 each is 0.59° more.
- **The bowsprit** (ZAZ2589, ZAZ2587): steeved 19.5° to K (19 to 20.7° on its two edges), 2.2 ft
  deep where it crosses the stem, its axis there 13.7 ft above WL1 (4.17 m). Its heel stands at
  about 131.5 ft, 4 ft before the fore mast (ZAZ2589). Its outer end is cut off by a jagged line on
  the sheets that draw it, so its length is not given.

## 6. The lines

### 6.1 The half-breadths by station (measured)

Moulded, feet, the 0.14 ft of §3.2 added. On ZAZ2587, read at 3 px each side of the station, and
ZAZ2559 within §3.3. The floor's is the thin line that crosses the middle line at about stations 12
and M (judgement: the half-breadth of the floor). The last column is the side at the height of the
upper-deck port's sill (2.10 ft above the deck at side at the station), from §6.3, interpolated by
the station's main breadth where no line is read.

| Station | ft from AP | Main breadth | Top-timber line | Water (WL1) | WL2 | WL3 | WL4 | WL5 | Floor | At the sill height |
|---|---|---|---|---|---|---|---|---|---|---|
| 32 | 3.62 | 13.70 | 12.90 | 6.76 | 2.18 | 1.07 | 0.58 |  |  | 13.25 |
| 30 | 8.50 | 14.66 | 13.70 | 12.16 | 5.84 | 2.71 | 1.34 | 0.75 |  | 14.16 |
| 28 | 13.34 | 15.51 | 14.30 | 14.30 | 9.66 | 4.90 | 2.38 | 1.13 |  | 14.90 |
| 26 | 18.23 | 16.20 | 15.11 | 15.42 | 12.32 | 7.29 | 3.67 | 1.60 |  | 15.62 |
| 24 | 23.11 | 16.83 | 15.64 | 16.30 | 14.08 | 9.58 | 5.24 | 2.30 |  | 16.09 |
| 22 | 27.91 | 17.27 | 16.07 | 16.99 | 15.29 | 11.48 | 6.85 | 3.16 |  | 16.66 |
| 20 | 32.81 | 17.61 | 16.42 | 17.56 (in the main breadth) | 16.16 | 12.93 | 8.48 | 4.16 |  | 16.92 |
| 18 | 37.71 | 17.95 | 16.78 | 17.90 (in the main breadth) | 16.78 | 14.10 | 10.02 | 5.33 |  | 17.18 |
| 16 | 42.58 | 18.21 | 17.10 | 18.16 (in the main breadth) | 17.10 | 14.97 | 11.33 | 6.59 |  | 17.43 |
| 14 | 47.45 | 18.42 | 17.24 | 18.37 (in the main breadth) | 17.59 | 15.62 | 12.37 | 7.79 |  | 17.63 |
| 12 | 52.30 | 18.56 | 17.34 | 18.51 (in the main breadth) | 17.86 | 16.09 | 13.19 | 8.86 |  | 17.76 |
| 10 | 57.08 | 18.65 | 17.44 | 18.60 (in the main breadth) | 18.00 | 16.40 | 13.82 | 9.79 | 1.12 | 17.85 |
| 8 | 62.01 | 18.73 | 17.47 | 18.68 (in the main breadth) | 18.08 | 16.63 | 14.25 | 10.51 | 2.65 | 17.93 |
| 6 | 67.95 | 18.75 | 17.45 | 18.70 (in the main breadth) | 18.10 | 16.70 | 14.55 | 11.10 | 3.73 | 18.01 |
| 4 | 72.78 | 18.75 | 17.46 | 18.70 (in the main breadth) | 18.11 | 16.74 | 14.72 | 11.43 | 4.29 | 18.04 |
| 2 | 77.67 | 18.74 | 17.45 | 18.69 (in the main breadth) | 18.10 | 16.74 | 14.79 | 11.56 | 4.57 | 18.04 |
| ⊕ | 82.58 | 18.73 | 17.47 | 18.68 (in the main breadth) | 18.11 | 16.72 | 14.77 | 11.57 | 4.65 | 18.04 |
| B | 87.40 | 18.75 | 17.48 | 18.70 (in the main breadth) | 18.11 | 16.65 | 14.65 | 11.36 | 4.61 | 18.05 |
| D | 92.29 | 18.73 | 17.46 | 18.68 (in the main breadth) | 18.01 | 16.52 | 14.42 | 10.88 | 4.34 | 18.03 |
| F | 97.14 | 18.69 | 17.46 | 18.64 (in the main breadth) | 17.87 | 16.29 | 14.04 | 10.15 | 3.86 | 17.99 |
| H | 101.97 | 18.56 | 17.48 | 18.51 (in the main breadth) | 17.60 | 15.91 | 13.46 | 9.13 | 2.86 | 17.86 |
| K | 106.87 | 18.37 | 17.24 | 18.23 | 17.24 | 15.37 | 12.66 | 7.93 | 1.23 | 17.68 |
| M | 111.75 | 18.11 | 16.99 | 17.87 | 16.65 | 14.56 | 11.50 | 6.50 |  | 17.46 |
| O | 116.58 | 17.72 | 16.64 | 17.31 | 15.80 | 13.43 | 10.05 | 5.12 |  | 17.16 |
| Q | 121.48 | 16.93 | 16.13 | 16.13 | 14.52 | 11.81 | 8.19 | 3.73 |  | 16.45 |
| S | 126.33 | 15.73 | 15.26 | 14.70 | 12.58 | 9.65 | 6.12 | 2.48 |  | 15.44 |
| S+1 | 131.19 | 13.90 | 13.90 | 12.41 | 9.95 | 7.03 | 4.00 | 1.37 |  | 13.72 |
| S+2 | 136.09 | 10.85 | 11.54 | 8.75 | 6.35 | 3.93 | 1.76 | 0.76 |  | 10.93 |

- **The ends.** The lines reach the post's rabbet at about 0.3 ft (WL1), 0.8, 1.4, 2.1 and 2.5 ft
  (WL5) from AP in plan, and the sheer's rabbet at 0.1, 0.6, 1.2, 1.6 and 2.1 ft (measured; the
  difference is 1 to 2 px and is not settled). The stem's rabbet at 143.6 (143.3 in plan), 142.7,
  141.2, 139.0 and 135.2 ft (WL5), from the sheer and the plan's end notches, which agree within
  0.3 ft. The main breadth ends at 144.8 ft and the top-timber line at 145.5 ft.
- **At the fore end:** at 137.4, 139.6, 141.8 and 143.2 ft the top-timber line is 10.64, 8.73, 6.30
  and 4.29 ft, the main breadth 9.82, 7.63, 5.03 and 2.89 ft, and WL1 7.56, 5.20, 2.50 and 0.63 ft.
- **At the after end:** at AP, the main breadth is 12.85 ft and the top-timber line 12.23 ft. The
  top-timber line runs on past the wing transom toward the taffrail, 11.69 ft at 2.4 ft abaft AP,
  11.29 at 4.3 ft, 10.85 at 6.1 ft and 10.48 at 7.7 ft (ZAZ2587).
- **The top-timber line is the side at the top of the timbers**, not always at the rail. Amidships
  it stands at the waist's second heavy line, 10.1 ft above WL1 and 1.4 ft below the rail; under
  the quarterdeck, at the plank-sheer; and forward, at about the forecastle deck, 2 ft under the
  rail (judgement, by §6.3). So the rail's own half-breadth is that line less the tumblehome above
  it, about 0.2 ft in the waist. Forward the side flares above it, and §8's `breadth_m` takes the
  body plan's half-breadth at the rail for O to S+2. On the quarterdeck the bulwark above the
  plank-sheer is not drawn in the body plan.
- **The dotted red line** in the plan runs between WL4 and WL5 from about station 28 to S+1 (read):
  13.3 ft at ⊕. It is drawn with no heights on these sheets and is not used (judgement: a diagonal
  or a ribband).

### 6.2 The midship section (measured, the outer heavy line of the body plan on ZAZ2587, both sides, ±0.05 ft; ZAZ2559 within 0.1 ft)

The moulded half-breadth against feet above WL1 at ⊕: 17.48 at 10.03 (the top of the timbers, at
the channel's stub); 17.58 at 9.30; 17.75 at 8.38; 17.97 at 7.46; 18.22 at 6.55; 18.47 at 5.63;
18.62 at 4.72; 18.68 at 3.80; **18.76-18.80 from 2.9 to 2.0, about 18.7 from 1.05 to 0.14 (the dead
flat, between and at the two heights of breadth, 18.75 stated)**; 18.66 at -0.78; 18.54 at -1.70;
18.32 at -2.61; 18.07 at -3.53; 17.71 at -4.44; 17.32 at -5.36; 16.89 at -6.28; 16.38 at -7.19;
15.89 at -8.11; 15.35 at -9.02; 14.77 at -9.94; 14.07 at -10.86; 13.28 at -11.77; 12.41 at -12.51;
11.94 at -13.06; 11.19 at -13.61; 10.31 at -14.15; 8.81 at -14.77; 7.35 at -15.24; 5.88 at -15.52;
3.68 at -15.78; 2.22 at -16.02; 1.48 at -16.18; 0.87 at -16.55, the keel's top.

- **The floor** rises 1.4 ft in its 7.3 ft from the keel's edge, about 11°, and the bilge is easy.
  **The tumblehome** is 1.3 ft a side from the dead flat to the top of the timbers.
- WL1 meets it 18.70 ft out, WL2 18.1, WL3 16.7, WL4 14.8, WL5 11.6, against the plan's 18.11,
  16.72, 14.77 and 11.57, to which §3.2's constant has been added.

### 6.3 The topsides in the body plan (measured, ±0.1 ft on each copy, both alike; rows of ZAZ2587, the fore body the mean of both copies)

Above the wale the body plan is open enough to follow eight lines in the after body and five in the
fore, besides the midship section. Each was followed by rows and named by its greatest half-breadth against the plan's main
breadth (judgement; tentative for 22, with no line for station 20). Moulded half-breadths at rows
of the sheet, each row's height above K in the heading:

| Line | 32.3 ft | 31.4 | 30.4 | 29.5 | 28.6 | 27.7 | 26.8 | 25.9 | 24.9 | 24.0 | 23.1 | 22.2 | 21.3 | 20.4 | 19.4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 18 | | | | | | 16.91 | 17.11 | 17.32 | 17.48 | | | 17.77 | 17.86 | 17.90 | 17.93 |
| 22 | 15.97 | 16.13 | 16.22 | 16.30 | 16.39 | 16.46 | 16.68 | 16.82 | 17.03 | 17.23 | 17.31 | 17.39 | 17.28 | 17.26 | 17.17 |
| 24 | 15.61 | 15.67 | 15.74 | 15.81 | 15.90 | 16.04 | 16.11 | 16.30 | 16.59 | 16.68 | 16.79 | 16.84 | 16.90 | 16.71 | 16.44 |
| 26 | 15.03 | 15.09 | 15.22 | 15.30 | 15.40 | 15.53 | 15.73 | 15.88 | 16.05 | 16.15 | 16.18 | 16.15 | 16.14 | 16.01 | 15.70 |
| 28 | 14.42 | 14.51 | 14.57 | 14.68 | 14.75 | 14.86 | 15.05 | 15.24 | 15.36 | 15.45 | 15.46 | 15.46 | 15.28 | 14.97 | 14.49 |
| 30 | 13.69 | 13.81 | 13.90 | 13.98 | 14.08 | 14.17 | 14.31 | 14.39 | 14.51 | 14.58 | 14.55 | 14.46 | 14.18 | 13.69 | 12.86 |
| 32 | 12.90 | 12.99 | 13.05 | 13.11 | 13.18 | 13.28 | 13.35 | 13.47 | 13.55 | 13.59 | 13.54 | 13.17 | 12.49 | 11.36 | |
| About AP | 10.53 | 10.63 | 10.73 | 10.85 | 11.09 | 11.37 | 11.88 | 12.31 | 12.56 | 12.73 | 12.64 | | | | |
| O | 16.40 | 16.45 | 16.55 | 16.64 | 16.73 | 16.83 | 16.98 | 17.19 | 17.41 | 17.53 | 17.64 | 17.73 | 17.74 | 17.72 | 17.68 |
| Q | 15.92 | 16.01 | 16.05 | 16.09 | 16.14 | 16.22 | 16.34 | 16.48 | 16.65 | 16.80 | 16.90 | 16.94 | 16.87 | 16.89 | 16.78 |
| S | 15.30 | 15.25 | 15.20 | 15.20 | 15.24 | 15.28 | 15.38 | 15.47 | 15.60 | 15.69 | 15.75 | 15.76 | 15.72 | 15.64 | 15.45 |
| S+1 | 14.24 | 14.11 | 13.96 | 13.82 | 13.77 | 13.71 | 13.70 | 13.74 | 13.77 | 13.82 | 13.82 | 13.80 | 13.74 | 13.62 | 13.30 |
| S+2 | 12.23 | 11.87 | 11.58 | 11.35 | 11.17 | 11.05 | 10.96 | 10.89 | 10.87 | 10.88 | 10.92 | 10.81 | 10.65 | 10.38 | 9.98 |

- The fore body's lines are the mean of the two copies, the after body's ZAZ2587's, ZAZ2559's
  within 0.1 ft where it could be followed.
- **So her side flares forward:** at S+2 the top of the side is 1.4 ft outside the breadth at the
  wale, at S+1 0.4 ft outside, and it tumbles home from S aft (measured).
- The fuller lines between ⊕ and station 18 and between ⊕ and O run together above the wale and are
  not separated. There the half-breadth at a sill is interpolated (judgement), and the midship
  section gives the upper end.
- **The line marked About AP is no section.** It stands about AP only at its foot, the wing
  transom's end. Above that its half-breadths are the stern board's (§5.6): 11.37 ft at 8.5 ft above
  WL1 against the lower counter's 11.3, 10.85 ft at 10.3 ft against the upper counter's 10.85. So it
  is the stern's edge, its x going aft with the counters (judgement), and §8.4 does not take it.
- **The row at 19.4 ft** lies in the heavy level line the body plan draws across both bodies at that
  height (read), so §8.4 does not take it either. The rows at 20.4 ft and up pass into `sections_m`
  between the water and the breadth, for every line but 18, which lies in the main breadth there.
  They matter most at the ends: at station 32 the half-breadth goes from 6.76 ft at the water to
  11.36 ft 1.2 ft above it, so a chord from the water to the next point misses the line by up to
  1.27 m there, by 0.27 m at station 30 and by 0.24 m at S+2 (measured against the side so drawn).

## 7. The ports

### 7.1 The upper deck: thirteen a side (measured, all six sheets)

Each port is drawn as a box, heavy along its top and fore side and thin along its sill and after
side. Centres: the mean of six sheets, ±0.1 ft. Sills and tops: the mean of ZAZ2589, ZAZ2561,
ZAZ2588, ZAZ2560 and ZAZ2587, ±0.05 ft on the sheet, and ±0.15 ft for WL1. The half-breadth from
§6.3 at the sill's height.

| Port | ft from AP | m from x = 0 | Sill above K (ft) | Sill above WL1 (ft) | Sill (m) | Top above WL1 (ft) | Sill above the deck at side (ft) | Half-breadth at the sill, moulded (ft) | Plank on (m) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 10.98 | -18.57 | 27.62 | 8.50 | 2.59 | 10.95 | 2.11 | 14.53 | 4.53 |
| 2 | 20.52 | -15.66 | 27.16 | 8.14 | 2.48 | 10.58 | 2.11 | 15.85 | 4.93 |
| 3 | 30.28 | -12.69 | 26.76 | 7.84 | 2.39 | 10.30 | 2.12 | 16.79 | 5.22 |
| 4 | 40.05 | -9.71 | 26.41 | 7.59 | 2.31 | 10.04 | 2.13 | 17.30 | 5.37 |
| 5 | 49.80 | -6.74 | 26.11 | 7.39 | 2.25 | 9.85 | 2.12 | 17.69 | 5.49 |
| 6 | 59.50 | -3.78 | 25.89 | 7.27 | 2.22 | 9.72 | 2.12 | 17.88 | 5.55 |
| 7 | 70.42 | -0.45 | 25.70 | 7.19 | 2.19 | 9.64 | 2.09 | 18.03 | 5.60 |
| 8 | 80.05 | +2.48 | 25.63 | 7.22 | 2.20 | 9.66 | 2.09 | 18.04 | 5.60 |
| 9 | 89.85 | +5.47 | 25.63 | 7.32 | 2.23 | 9.75 | 2.08 | 18.05 | 5.60 |
| 10 | 99.60 | +8.44 | 25.70 | 7.49 | 2.28 | 9.94 | 2.08 | 17.93 | 5.57 |
| 11 | 109.32 | +11.41 | 25.83 | 7.72 | 2.35 | 10.17 | 2.09 | 17.57 | 5.46 |
| 12 | 119.05 | +14.37 | 26.01 | 8.00 | 2.44 | 10.45 | 2.09 | 16.80 | 5.22 |
| 13 | 128.80 | +17.34 | 26.25 | 8.34 | 2.54 | 10.80 | 2.13 | 14.56 | 4.54 |

- **Spacing:** 9.75 ft centre to centre (9.5 to 9.8), and 10.92 ft across the main mast between
  ports 6 and 7.
- **Size:** 2.90 ft wide (2.84-2.98; the heavy edge's centre on one side, so about 1 in under the
  opening) by 2.45 ft deep: **2 ft 11 in by 2 ft 5½ in**. Steel's 36: 2 ft 10 in by 2 ft 5 in.
- **The sill's lowest** is port 7, 7.19 ft above WL1 (2.19 m), Steel's 36 being 7 ft 8 in (2.34 m);
  it runs 7.2 to 7.3 ft from port 6 to port 9.
- **The half-breadths are judgement on measured lines**, not measured at the port, as the 64's are.
  The check at ⊕: the midship section at the sill's height gives 18.05 ft, as the table has at
  ports 8 and 9.

### 7.2 The quarterdeck: six a side (measured, all six sheets)

Each a blank box in the bulwark from the rail down past the plank-sheer. Centres ±0.1 ft, sills
±0.1 ft and ±0.15 ft for WL1. Two sizes, with two heights of sill:

| Port | ft from AP | m from x = 0 | Width (ft) | Kind (judgement) | Sill above K (ft) | Sill above WL1 (ft) | Sill (m) | Sill above the deck at side (ft) | Top-timber half-breadth, moulded (ft) | Plank on (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.40 | -21.49 | 3.03 | carronade | 33.88 | 14.66 | 4.47 | 0.96 | 12.48 | 3.90 |
| 2 | 12.24 | -18.18 | 2.27 | gun | 33.89 | 14.78 | 4.51 | 1.58 | 14.16 | 4.42 |
| 3 | 23.00 | -14.90 | 2.22 | gun | 33.33 | 14.33 | 4.37 | 1.56 | 15.63 | 4.87 |
| 4 | 32.45 | -12.02 | 2.97 | carronade | 32.30 | 13.40 | 4.08 | 0.94 | 16.39 | 5.10 |
| 5 | 42.35 | -9.01 | 2.24 | gun | 32.53 | 13.73 | 4.19 | 1.53 | 17.08 | 5.31 |
| 6 | 51.07 | -6.35 | 2.26 | gun | 32.27 | 13.56 | 4.13 | 1.54 | 17.31 | 5.38 |

- **Gun ports** 2 ft 3 in wide, their sills 1 ft 6½ in above the deck at side, 2 ft 4 in under the
  rail (2.25 by 2.33 ft). **Carronade ports** 3 ft 0 in wide, sills 11½ in above the deck at side,
  about 3 ft under the rail (3.00 by 2.95 ft). The sizes and sills fit Steel's quarterdeck guns'
  and carronades' (`pages-steel-1805-bodies.md` §5.3), so the names are Steel's (judgement).
- **Four gun ports a side** are the table's eight 9-pounders (judgement). The two wider ones a side
  would take four of Winfield's six carronades (p. 143); ports for the other two are not drawn.
- The half-breadth is the top-timber line (judgement: within 2 ft of the plank-sheer, as the 64's
  quarterdeck is: her port notes, `tools/ships/indefatigable.py`); abaft station 32 read on the line
  by column.

### 7.3 The forecastle: no port is drawn (read for what is drawn, measured for its heights)

No sheet shows a port there. The rail stands 0.5 ft above the deck's top line, about 1 ft above the
deck at side, with timberheads above it on the draughts, so her forecastle guns fire over the rail
(judgement), as the 64's do (`OVER_THE_RAIL_M`, `tools/ships/indefatigable.py`). For a triple, the 64's rule: **the sill 2 in under the rail**,
marked `judged`; §8.3.

## 8. For the profile: the points in metres

`x` forward of her middle, `z` above WL1, half-breadths plank on (Units and datums, above). In the
order of `schema.PROFILE_KEYS`. Rung of every line: **S** by §5.0, her own class's lines,
`sourced`, but where marked; §8.5 gives each line's word, by its weakest point (principle 4).

### 8.1 The first form

- **`rail_m`** (S; §5.1; the steps at the breast and the forecastle's scroll given as read, x
  rising):
  [-25.27, 6.03], [-24.99, 6.01], [-24.81, 5.55], [-23.98, 5.49], [-23.15, 5.45], [-22.32, 5.41], [-21.5,
  5.37], [-20.81, 5.33], [-19.32, 5.26], [-17.85, 5.2], [-16.36, 5.13], [-14.87, 5.08],
  [-13.41, 5.02], [-11.91, 4.98], [-10.42, 4.94], [-8.94, 4.91], [-7.45, 4.87], [-5.97, 4.85],
  [-4.52, 4.82], [-3.01, 4.81], [-2.66, 4.8], [-2.65, 3.9], [-2.28, 3.73], [-2.07, 3.67],
  [-1.95, 3.49], [-1.2, 3.51], [0.27, 3.5], [1.76, 3.5], [3.26, 3.51], [4.72, 3.52], [6.21,
  3.55], [7.69, 3.58], [9.17, 3.62], [9.78, 3.63], [9.85, 3.74], [10.05, 3.85], [10.21, 3.94],
  [10.43, 4.01], [10.66, 4.01], [12.15, 4.06], [13.62, 4.11], [15.11, 4.18], [16.59, 4.25],
  [18.07, 4.32], [19.57, 4.41], [21.01, 4.52], [22.56, 4.62]
- **`breadth_m`** (judged by its weakest points, S on the plan's lines; [x, water, rail]; the water from WL1, the rail the top-timber line, §6.1's
  caveat; the body plan's at the rail for O to S+2; from the post's rabbet to the stem's rabbet at
  WL1):
  [-21.88, 0.27, 3.83], [-20.81, 2.16, 4.03], [-19.32, 3.81, 4.28], [-17.85, 4.46, 4.46],
  [-16.36, 4.8, 4.71], [-14.87, 5.07, 4.87], [-13.41, 5.28, 5], [-11.91, 5.45, 5.11], [-10.42,
  5.56, 5.22], [-8.94, 5.64, 5.31], [-7.45, 5.7, 5.36], [-5.97, 5.74, 5.39], [-4.52, 5.77,
  5.42], [-3.01, 5.8, 5.43], [-1.2, 5.8, 5.42], [0.27, 5.8, 5.42], [1.76, 5.8, 5.42], [3.26,
  5.8, 5.43], [4.72, 5.8, 5.43], [6.21, 5.8, 5.42], [7.69, 5.78, 5.42], [9.17, 5.74, 5.43],
  [10.66, 5.66, 5.36], [12.15, 5.55, 5.28], [13.62, 5.38, 5.13], [15.11, 5.02, 4.96], [16.59,
  4.58, 4.77], [18.07, 3.88, 4.43], [19.57, 2.77, 3.85], [20.63, 1.69, 2.76], [21.3, 0.86,
  2.02], [21.74, 0.29, 1.41], [21.87, 0.25, 1.31]
- **`keel_m`** (S; K, the heel to the knee's foot, straight as drawn, falling toward the stern
  against WL1 by the drag):
  [-21.65, -5.86], [-12.77, -5.77], [-3.63, -5.67], [5.52, -5.58], [14.66, -5.49], [19.31,
  -5.44]
- **`stem_m`** (S; the fore edge, low to high, from its foot at the keel to the stem head):
  [17.53, -5.13], [18.36, -4.85], [18.65, -4.57], [19.4, -4.15], [20, -3.72], [20.47, -3.31],
  [20.8, -2.89], [21.09, -2.47], [21.33, -2.06], [21.51, -1.64], [21.68, -1.22], [21.81,
  -0.81], [21.92, -0.39], [22.04, 0.02], [22.12, 0.43], [22.19, 0.85], [22.26, 1.26], [22.32,
  1.68], [22.38, 2.09], [22.43, 2.51], [22.49, 2.92], [22.54, 3.33], [22.58, 3.75], [22.62,
  4.16], [22.66, 4.58]
- **`stern_m`** (S; the post's after face, the counters, the taffrail, low to high, on ZAZ2587's
  outer line):
  [-21.65, -5.84], [-21.71, -5.51], [-21.78, -4.95], [-21.84, -4.39], [-21.88, -3.84], [-21.95,
  -3.28], [-22, -2.72], [-22.09, -2.16], [-22.12, -1.6], [-22.21, -1.05], [-22.26, -0.49],
  [-22.32, -0.04], [-22.34, 0.18], [-22.37, 0.63], [-22.43, 1.07], [-22.47, 1.52], [-22.52,
  1.74], [-22.71, 1.97], [-23.05, 2.19], [-23.33, 2.41], [-23.83, 2.63], [-23.96, 2.85],
  [-24.15, 3.07], [-24.39, 3.29], [-24.43, 3.51], [-24.51, 3.74], [-24.58, 3.96], [-24.66,
  4.18], [-24.71, 4.41], [-24.86, 4.63], [-25.05, 4.85], [-25.2, 5.07], [-25.28, 5.29],
  [-25.39, 5.74], [-25.27, 6.03]
- **`wales_m`** (judged by its weakest points, S on the lower edge and on the upper edge where it
  is read, §5.7; the upper edge at its two ends and at stations 6 and 4 at the measured breadth; [x,
  lower, upper]):
  [-21.88, 1.13, 2.26], [-21.56, 1.01, 2.14], [-20.81, 0.84, 1.96], [-19.32, 0.73, 1.85],
  [-17.85, 0.63, 1.75], [-16.36, 0.54, 1.66], [-14.87, 0.45, 1.58], [-13.41, 0.38, 1.5],
  [-11.91, 0.31, 1.43], [-10.42, 0.25, 1.37], [-8.94, 0.2, 1.32], [-7.45, 0.15, 1.27], [-5.97,
  0.12, 1.24], [-4.52, 0.08, 1.2], [-3.01, 0.04, 1.16], [-1.2, 0.02, 1.14], [0.27, 0.01, 1.13],
  [1.76, 0.01, 1.13], [3.26, 0.01, 1.13], [4.72, 0.02, 1.15], [6.21, 0.05, 1.18], [7.69, 0.09,
  1.22], [9.17, 0.13, 1.25], [10.66, 0.18, 1.3], [12.15, 0.23, 1.35], [13.62, 0.28, 1.41],
  [15.11, 0.35, 1.47], [16.59, 0.42, 1.54], [18.07, 0.5, 1.62], [19.57, 0.59, 1.71], [22.02,
  0.69, 1.82]
- **`section_m`** (S; [z, half-breadth], §6.2, plank on, from the keel's top to the top of the
  timbers):
  [-5.05, 0.37], [-5.03, 0.43], [-4.93, 0.55], [-4.88, 0.78], [-4.81, 1.22], [-4.73, 1.89],
  [-4.65, 2.34], [-4.5, 2.79], [-4.31, 3.24], [-4.15, 3.51], [-3.98, 3.74], [-3.81, 3.89],
  [-3.59, 4.15], [-3.31, 4.39], [-3.03, 4.6], [-2.75, 4.78], [-2.47, 4.94], [-2.19, 5.1],
  [-1.91, 5.25], [-1.63, 5.38], [-1.35, 5.5], [-1.08, 5.61], [-0.8, 5.69], [-0.52, 5.75],
  [-0.24, 5.79], [0.04, 5.8], [0.32, 5.79], [0.6, 5.83], [0.88, 5.82], [1.16, 5.79], [1.44,
  5.78], [1.72, 5.73], [2, 5.65], [2.28, 5.58], [2.55, 5.51], [2.83, 5.46], [3.06, 5.43]
- **`decks_m`** (S on the two lines, the deck at side judgement by §5.3; each a fit through the
  second line and 0.25 ft, rms 0.04, 0.02, 0.01, 0.02 ft):
  - `upper`, from its after end to the stem, the second line and 0.25 ft, and at the fore end the
    lines' gap carried on where the top line alone can be read (judgement):
  [-22.52, 2.1], [-20.81, 2.04], [-19.32, 1.98], [-17.85, 1.92], [-16.36, 1.86], [-14.87, 1.81], [-13.41,
  1.76], [-11.91, 1.72], [-10.42, 1.68], [-8.94, 1.65], [-7.45, 1.62], [-5.98, 1.59], [-4.52,
  1.58], [-3.01, 1.56], [-1.2, 1.55], [0.27, 1.55], [1.76, 1.56], [3.25, 1.57], [4.72, 1.59],
  [6.22, 1.61], [7.69, 1.63], [9.17, 1.66], [10.66, 1.7], [12.15, 1.74], [13.62, 1.78], [15.11,
  1.82], [16.59, 1.87], [18.07, 1.92], [19.56, 1.97], [22.04, 2.08]
  - `quarterdeck`, from the deck's after end, 8.9 ft abaft AP:
  [-24.63, 4.3], [-23.44, 4.25], [-20.81, 4.14], [-19.32, 4.07], [-17.85, 4.01], [-16.36, 3.95], [-14.87,
  3.89], [-13.41, 3.84], [-11.91, 3.8], [-10.42, 3.75], [-8.94, 3.72], [-7.45, 3.68], [-5.98,
  3.66], [-4.52, 3.63], [-3.01, 3.62], [-2.44, 3.61]
  - `forecastle`:
  [10.42, 3.73], [10.66, 3.74], [12.15, 3.77], [13.62, 3.82], [15.11, 3.86], [16.59, 3.91],
  [18.07, 3.97], [19.56, 4.03], [22.13, 4.15]
  - `lower` (no ports; kept by principle 11), its two ends on the top line, the lines' gap carried on
    (judgement):
  [-21.31, 0.14], [-20.81, 0.13], [-19.32, 0.07], [-17.85, 0.01], [-16.36, -0.04], [-14.87, -0.09], [-13.41,
  -0.13], [-11.91, -0.18], [-10.42, -0.21], [-8.94, -0.24], [-7.45, -0.27], [-5.98, -0.29],
  [-4.52, -0.31], [-3.01, -0.32], [-1.2, -0.33], [0.27, -0.33], [1.76, -0.33], [3.25, -0.32],
  [4.72, -0.31], [6.22, -0.29], [7.69, -0.26], [9.17, -0.24], [10.66, -0.2], [12.15, -0.16],
  [13.62, -0.12], [15.11, -0.07], [16.59, -0.02], [18.07, 0.03], [19.56, 0.1], [21.67, 0.16]

### 8.2 The ports as the sheets have them (S for x and sill; the half-breadth judgement on measured lines)

For the record and for package 81, whose ports these are:

- `upper`:
  [-18.57, 2.59, 4.53], [-15.66, 2.48, 4.93], [-12.69, 2.39, 5.22], [-9.71, 2.31, 5.37],
  [-6.74, 2.25, 5.49], [-3.78, 2.22, 5.55], [-0.45, 2.19, 5.6], [2.48, 2.2, 5.6], [5.47, 2.23,
  5.6], [8.44, 2.28, 5.57], [11.41, 2.35, 5.46], [14.37, 2.44, 5.22], [17.34, 2.54, 4.54]
- `quarterdeck`:
  [-21.49, 4.47, 3.9], [-18.18, 4.51, 4.42], [-14.9, 4.37, 4.87], [-12.02, 4.08, 5.1], [-9.01,
  4.19, 5.31], [-6.35, 4.13, 5.38]

### 8.3 The port triples at the file's own guns (§5.3: no gun's `x_m` moves)

The file's fit has its upper guns 2.75 m apart, the sheet 2.97 m. Principle 8 and §5.3 keep each
gun's `x_m`, and truth 7-185 wants each port gun on a triple of its deck within 0.01 m. So a triple
for the file is **the gun's own x, and the sheet's sill line and side at that x** (judgement on
measured lines; mark `sourced` for the sill line, the place the file's). The file's quarterdeck
stands INCORRECT by the owner's ruling, so its triples follow its pairs as they are and name
nothing to change. Each port gun's `height_m` is now its triple's sill, by `Build-Ships.md` §5.3: a
height is read by nothing in the engine until SW-5's L2.

| The file's gun | `x_m` | ft from AP | Nearest port of the sheet, off by (ft) | Sill above WL1 (m) | Half-breadth at the sill, plank on (m) | The file's `height_m` before her lines |
|---|---|---|---|---|---|---|
| 13 | -16.5 | 17.77 | -2.75 | 2.51 | 4.84 | 2.4 |
| 12 | -13.8 | 26.62 | -3.66 | 2.42 | 5.13 | 2.4 |
| 11 | -11.0 | 35.81 | -4.24 | 2.35 | 5.30 | 2.4 |
| 10 | -8.2 | 45.00 | -4.80 | 2.28 | 5.44 | 2.4 |
| 9 | -5.5 | 53.86 | +4.06 | 2.24 | 5.52 | 2.4 |
| 8 | -2.8 | 62.71 | +3.21 | 2.21 | 5.57 | 2.4 |
| 7 | +0.0 | 71.90 | +1.48 | 2.19 | 5.60 | 2.4 |
| 6 | +2.8 | 81.09 | +1.04 | 2.20 | 5.60 | 2.4 |
| 5 | +5.5 | 89.94 | +0.09 | 2.23 | 5.60 | 2.4 |
| 4 | +8.2 | 98.80 | -0.80 | 2.28 | 5.57 | 2.4 |
| 3 | +11.0 | 107.99 | -1.33 | 2.34 | 5.48 | 2.4 |
| 2 | +13.8 | 117.18 | -1.87 | 2.42 | 5.31 | 2.4 |
| 1 | +16.5 | 126.03 | -2.77 | 2.51 | 4.83 | 2.4 |

- `upper`:
  [-16.5, 2.51, 4.84], [-13.8, 2.42, 5.13], [-11, 2.35, 5.3], [-8.2, 2.28, 5.44], [-5.5, 2.24,
  5.52], [-2.8, 2.21, 5.57], [0, 2.19, 5.6], [2.8, 2.2, 5.6], [5.5, 2.23, 5.6], [8.2, 2.28,
  5.57], [11, 2.34, 5.48], [13.8, 2.42, 5.31], [16.5, 2.51, 4.83]
- `quarterdeck`: the file's pairs 17 to 14, carronades, and its pair 19, the long 9s. Sill: the
  deck at side and 0.95 ft for a carronade, 1.55 ft for a long gun, the sheet's own heights (§7.2).
  No sheet port stands at these x; the sheet's gun ports fall at -18.18, -14.90, -9.01 and -6.35:
  [-17.5, 4.28, 4.52], [-14, 4.15, 4.95], [-10.5, 4.05, 5.21], [-7, 3.97, 5.37], [-4.5, 4.11,
  5.42]
- `forecastle`: the file's pair 18 at +14.0 and its chasers at +17.5, on no drawn port: the sill 2
  in under the rail (§7.3, `judged`):
  [14, 4.08, 5.08], [17.5, 4.25, 4.56]
- **`port_size_m`:** `upper` [0.88, 0.75]; `quarterdeck` [0.69, 0.71], the gun ports (the carronade
  ports [0.91, 0.90]); `forecastle` [0.69, 0.71], the quarterdeck's (judgement).

### 8.4 The shape keys

- **`head_m`** (S; ZAZ2587, ±0.3 ft; from the knee's foot on K to its top):
  [19.31, -5.41], [19.94, -5.05], [20.23, -4.77], [20.42, -4.49], [20.62, -4.21], [20.79,
  -3.92], [20.94, -3.64], [21.07, -3.36], [21.22, -3.08], [21.35, -2.8], [21.47, -2.52],
  [21.59, -2.24], [21.7, -1.96], [21.86, -1.68], [22.02, -1.39], [22.18, -1.11], [22.35,
  -0.83], [22.52, -0.55], [22.73, -0.27], [22.95, 0.01], [23.18, 0.3], [23.46, 0.58], [23.73,
  0.86], [24.03, 1.15], [24.39, 1.43], [24.81, 1.77], [25.21, 2.06], [25.54, 2.34], [25.78,
  2.62], [26, 2.9], [26.15, 3.19], [26.25, 3.47], [26.33, 3.75], [26.43, 4.03], [26.52, 4.31],
  [26.58, 4.59], [26.65, 4.87], [26.66, 5.15]
- **`breadth_line_m`** (S; [x, z, half-breadth]: the upper height of breadth with the main
  half-breadth; forward of x +15 the height ±0.3 ft):
  [-19.32, 1.37, 4.57], [-17.85, 1.3, 4.83], [-16.36, 1.2, 5.04], [-14.87, 1.13, 5.23],
  [-13.41, 1.06, 5.37], [-11.91, 0.99, 5.47], [-10.42, 0.93, 5.57], [-8.94, 0.88, 5.65],
  [-7.45, 0.84, 5.72], [-5.97, 0.82, 5.76], [-4.52, 0.82, 5.79], [-3.01, 0.82, 5.81], [-1.2,
  0.82, 5.82], [0.27, 0.84, 5.82], [1.76, 0.86, 5.81], [3.26, 0.87, 5.81], [4.72, 0.9, 5.82],
  [6.21, 0.92, 5.81], [7.69, 0.95, 5.8], [9.17, 1, 5.76], [10.66, 1.05, 5.7], [12.15, 1.14,
  5.62], [13.62, 1.23, 5.5], [15.11, 1.34, 5.26], [16.59, 1.54, 4.9], [18.07, 1.63, 4.34],
  [19.57, 1.87, 3.41]
- **`sections_m`** (S under the water and on the body plan's rows; [z, half-breadth] by station at
  each x, low to high: WL5 to WL1 where they exist; §6.3's rows from 20.4 ft above K, up to 0.1 m
  under the upper height of breadth, at stations 22 to 32 and O to S+2, and at station 32, its
  height of breadth unread, up to the sill; the upper height of breadth, the sill's height, the top
  of the timbers or forward the rail. WL2 to WL5 at 3.32 ft each; the sill's point judgement on
  measured lines, §6.1):
  - x -20.81: [-3.04, 0.28], [-2.02, 0.43], [-1.01, 0.77], [0, 2.16], [0.37, 3.56], [0.64, 3.91], [0.92, 4.12], [1.19, 4.23], [1.47, 4.24], [1.74, 4.23], [2.04, 4.21], [2.32, 4.17], [2.68, 4.14], [4.82, 4.03]
  - x -19.32: [-4.05, 0.33], [-3.04, 0.51], [-2.02, 0.93], [-1.01, 1.88], [0, 3.81], [0.38, 4.27], [0.66, 4.42], [0.93, 4.51], [1.21, 4.54], [1.37, 4.57], [2.62, 4.42], [4.72, 4.28]
  - x -17.85: [-4.05, 0.45], [-3.04, 0.83], [-2.02, 1.6], [-1.01, 3.05], [0, 4.46], [0.4, 4.66], [0.67, 4.76], [0.95, 4.81], [1.3, 4.83], [2.56, 4.64], [4.62, 4.46]
  - x -16.36: [-4.05, 0.59], [-3.04, 1.22], [-2.02, 2.32], [-1.01, 3.86], [0, 4.8], [0.41, 4.98], [0.69, 5.02], [0.96, 5.02], [1.2, 5.04], [2.5, 4.86], [4.53, 4.71]
  - x -14.87: [-4.05, 0.8], [-3.04, 1.7], [-2.02, 3.02], [-1.01, 4.39], [0, 5.07], [0.43, 5.19], [0.7, 5.25], [0.98, 5.23], [1.13, 5.23], [2.45, 5.01], [4.45, 4.87]
  - x -13.41: [-4.05, 1.06], [-3.04, 2.19], [-2.02, 3.6], [-1.01, 4.76], [0, 5.28], [0.44, 5.36], [0.72, 5.37], [1.06, 5.37], [2.4, 5.18], [4.38, 5]
  - x -11.91: [-4.05, 1.37], [-3.04, 2.69], [-2.02, 4.04], [-1.01, 5.03], [0, 5.45], [0.99, 5.47], [2.36, 5.26], [4.32, 5.11]
  - x -10.42: [-4.05, 1.73], [-3.04, 3.16], [-2.02, 4.4], [-1.01, 5.22], [0, 5.56], [0.93, 5.57], [2.32, 5.34], [4.26, 5.22]
  - x -8.94: [-4.05, 2.11], [-3.04, 3.55], [-2.02, 4.66], [-1.01, 5.31], [0, 5.64], [0.88, 5.65], [2.29, 5.41], [4.21, 5.31]
  - x -7.45: [-4.05, 2.48], [-3.04, 3.87], [-2.02, 4.86], [-1.01, 5.46], [0, 5.7], [0.84, 5.72], [2.26, 5.48], [4.16, 5.36]
  - x -5.97: [-4.05, 2.8], [-3.04, 4.12], [-2.02, 5.01], [-1.01, 5.55], [0, 5.74], [0.82, 5.76], [2.23, 5.51], [4.12, 5.39]
  - x -4.52: [-4.05, 3.09], [-3.04, 4.31], [-2.02, 5.1], [-1.01, 5.59], [0, 5.77], [0.82, 5.79], [2.22, 5.54], [4.07, 5.42]
  - x -3.01: [-4.05, 3.31], [-3.04, 4.45], [-2.02, 5.17], [-1.01, 5.61], [0, 5.8], [0.82, 5.81], [2.2, 5.57], [3.9, 5.43]
  - x -1.20: [-4.05, 3.48], [-3.04, 4.54], [-2.02, 5.19], [-1.01, 5.62], [0, 5.8], [0.82, 5.82], [2.19, 5.59], [3.07, 5.42]
  - x +0.27: [-4.05, 3.59], [-3.04, 4.59], [-2.02, 5.2], [-1.01, 5.62], [0, 5.8], [0.84, 5.82], [2.19, 5.6], [3.08, 5.42]
  - x +1.76: [-4.05, 3.63], [-3.04, 4.61], [-2.02, 5.2], [-1.01, 5.62], [0, 5.8], [0.86, 5.81], [2.2, 5.6], [3.07, 5.42]
  - x +3.26: [-4.05, 3.63], [-3.04, 4.6], [-2.02, 5.2], [-1.01, 5.62], [0, 5.8], [0.87, 5.81], [2.21, 5.6], [3.08, 5.43]
  - x +4.72: [-4.05, 3.56], [-3.04, 4.57], [-2.02, 5.18], [-1.01, 5.62], [0, 5.8], [0.9, 5.82], [2.23, 5.6], [3.09, 5.43]
  - x +6.21: [-4.05, 3.42], [-3.04, 4.5], [-2.02, 5.14], [-1.01, 5.59], [0, 5.8], [0.92, 5.81], [2.25, 5.6], [3.11, 5.42]
  - x +7.69: [-4.05, 3.2], [-3.04, 4.38], [-2.02, 5.07], [-1.01, 5.55], [0, 5.78], [0.95, 5.8], [2.27, 5.58], [3.15, 5.42]
  - x +9.17: [-4.05, 2.88], [-3.04, 4.2], [-2.02, 4.95], [-1.01, 5.47], [0, 5.74], [1, 5.76], [2.3, 5.55], [3.2, 5.43]
  - x +10.66: [-4.05, 2.52], [-3.04, 3.96], [-2.02, 4.79], [-1.01, 5.36], [0, 5.66], [1.05, 5.7], [2.34, 5.49], [4.01, 5.36]
  - x +12.15: [-4.05, 2.08], [-3.04, 3.61], [-2.02, 4.54], [-1.01, 5.18], [0, 5.55], [1.14, 5.62], [2.38, 5.42], [4.06, 5.28]
  - x +13.62: [-4.05, 1.66], [-3.04, 3.16], [-2.02, 4.2], [-1.01, 4.92], [0, 5.38], [0.72, 5.5], [0.99, 5.51], [1.23, 5.5], [2.42, 5.33], [4.11, 5.13]
  - x +15.11: [-4.05, 1.24], [-3.04, 2.6], [-2.02, 3.7], [-1.01, 4.53], [0, 5.02], [0.73, 5.25], [1.01, 5.24], [1.34, 5.26], [2.46, 5.12], [4.18, 4.96]
  - x +16.59: [-4.05, 0.86], [-3.04, 1.97], [-2.02, 3.04], [-1.01, 3.94], [0, 4.58], [0.75, 4.87], [1.02, 4.89], [1.3, 4.91], [1.54, 4.9], [2.51, 4.81], [4.25, 4.77]
  - x +18.07: [-4.05, 0.52], [-3.04, 1.32], [-2.02, 2.24], [-1.01, 3.13], [0, 3.88], [0.76, 4.25], [1.04, 4.29], [1.31, 4.31], [1.63, 4.34], [2.56, 4.28], [4.32, 4.43]
  - x +19.57: [-4.05, 0.33], [-3.04, 0.64], [-2.02, 1.3], [-1.01, 2.04], [0, 2.77], [0.78, 3.27], [1.05, 3.35], [1.33, 3.4], [1.6, 3.43], [1.87, 3.41], [2.61, 3.43], [4.41, 3.85]
- **`channel_wales_m`:** none (§5.7).
- **`floor_m`** (reserved, S as drawn, identification judgement; [x, z of the rising line in the
  sheer, the floor's half-breadth]; the rising line stands about 1 ft under the section at the
  floor's half-breadth at ⊕, so it is not a point of the surface):
  [-4.52, -3.52, 0.34], [-3.01, -4.07, 0.81], [-1.2, -4.6, 1.14], [0.27, -4.86, 1.31], [1.76,
  -5.09, 1.39], [3.25, -5.08, 1.42], [4.72, -5.05, 1.41], [6.22, -4.87, 1.32], [7.69, -4.63,
  1.18], [9.17, -4.16, 0.87], [10.66, -3.49, 0.37]
- **`rabbet_m`** (reserved; S; [x, z, half-siding]; the heavy line along the keel and up the stem;
  half-siding from the body plan's keel box and the plan's ends):
  [-21.12, -5.4, 0.14], [-18.87, -5.37, 0.19], [-15.82, -5.34, 0.19], [-3.63, -5.22, 0.19],
  [8.56, -5.09, 0.19], [16.18, -5.02, 0.19], [18.36, -4.57, 0.15], [19.18, -4.15, 0.15],
  [19.76, -3.73, 0.15], [20.23, -3.31, 0.15], [20.59, -2.89, 0.15], [20.9, -2.47, 0.15],
  [21.15, -2.06, 0.15], [21.35, -1.64, 0.15], [21.52, -1.23, 0.15], [21.66, -0.81, 0.15],
  [21.77, -0.4, 0.15], [21.87, 0.02, 0.15], [21.96, 0.43, 0.15], [22.04, 0.85, 0.15], [22.11,
  1.26, 0.15], [22.17, 1.68, 0.15], [22.23, 2.09, 0.15], [22.29, 2.5, 0.15], [22.34, 2.92,
  0.15], [22.39, 3.33, 0.15], [22.44, 3.75, 0.15], [22.49, 4.16, 0.15], [22.53, 4.57, 0.15]

**Checked against the tree at `bb60222`, and built:** these keys with either set of triples pass
`g.hull_profile` and `g.hull_form` with `form.check` (at the sheet's own ports in scratch, §11; at
the file's guns in `tools/ships/hull_frigate.py`, the generator's report and
`tests/test_hull_frigate.py`, which reads this section back). The helper reports a drawn
displacement of **1,448 t against the filed 1,270 t, +14%**, within §5.0's 15%, and drawn 5.05 m
deep at the greatest section (to the keel's top) against the file's 4.6 m. Every triple lies within
0.04 m of the side as drawn, 0.021 m at most at the file's own x; that is partly because the
sections carry the same sill points, so it is a check of the sum and not an independent measure of
the side. §6.3's lines from 20.4 ft above K lie within 0.10 m of the side as drawn at every row
under the rail, and her test holds them there. Under the breadth those rows are her own points;
from the breadth up they are the independent part of that check, as the sill's point at each
station is interpolated from them.

### 8.5 `form` and `marks`

```yaml
form:
  stern:
    type: square
    knuckle_z_m: 1.25     # sourced: the wing transom's ends, §5.6
    transom_hb_m: [3.21, 3.96]  # sourced: at the taffrail, at the knuckle: 10.2 and 12.65 ft and the plank
    round_up_m: 0.12      # sourced: the wing transom's 0.40 ft; the counters' are 0.53-0.60 ft
    galleries_m: [[-23.99, -20.67, 2.62, 4.11]]  # sourced: the tier, -6.8 to +4.1 ft, base rail 8.6 to top rail 13.5 ft, ZAZ2587 and ZAZ2559
    lights_m: [[3.22, 4.01, 5, 2.6]]  # judged: the count; from the upper counter at the middle line to the top of the gallery's aftmost light
  head: figure            # judged: the knee is drawn blank; its reach is head_m's, sourced
marks:
  rail_m: judged          # the inboard sheets' heavy line in the waist taken for the rail, §3.3
  breadth_m: judged       # the water from station 20 to H 0.05 ft inside the main breadth, not read; the rail the top-timber line but for O to S+2
  keel_m: judged          # that the strip's top border is the false keel's lower edge, §5.4
  stem_m: sourced
  stern_m: sourced
  wales_m: judged         # its upper edge at the two ends and at stations 6 and 4, at its measured breadth
  section_m: sourced
  decks_m: judged         # the deck at side, the second line and the plank
  ports_m: judged         # the half-breadths at the sills, the file's x, the forecastle's sills
  port_size_m: judged     # the forecastle's
  head_m: sourced
  breadth_line_m: sourced
  sections_m: judged      # the sill's point at each station; the waterlines and main breadth are measured
  floor_m: judged         # what the line is
  rabbet_m: judged        # that the heavy base line is it, §5.4; a half-siding held between its two places
  form.stern: sourced
  form.stern.knuckle_z_m: sourced
  form.stern.transom_hb_m: sourced
  form.stern.round_up_m: sourced
  form.stern.galleries_m: sourced
  form.stern.lights_m: judged
  form.head: judged
```

- **No fullness.** The default rule's (`form.py`'s), and the sections cover the body from x -20.8 to
  +19.6: first written as `fullness: [1.0, 1.0]`, `judged`, which drew nothing different, and no other
  hull writes it (the landing's review). **`rail_m`, `keel_m` and `rabbet_m`** were first `sourced`;
  principle 4 takes the word of the weakest point.
- **Steel's method for the lights** (1805 pp. 250-251; `Build-Ships.md` §5.0 principle 9): five is
  the 64's own elevation, ZAZ1953, as the count; the band's foot is the upper counter at the middle
  line, 3.22 m, since the counters end the stern below and the great cabin's windows stand between
  them and the taffrail (Steel, OCR `:15378-15382`); its top is the top of the gallery's aftmost
  light, 4.01 m; the half-breadth 8.5 ft, inside the stern's 10.4-11.3 ft at those heights. Judgement
  all. The gallery's aftmost light runs lower, its foot 3.06 m, and on a transom drawn flat the
  counter is not drawn, so the band's foot is that judgement alone.
- **`ports_m` taken at the file's x:** the note on the key says that the x is the file's and the
  sill line and side the sheet's (§8.3), and names the sheet's own ports by §8.2.
- **The transom's edge:** `transom_hb_m` holds two half-breadths and the hull is drawn straight
  between them. The stern board's edge (§5.6; §6.3's line marked About AP) lies inside that line at
  the counters, plank on: 3.55 m against 3.75 m at the lower, 3.41 against 3.65 at the upper, 3.27
  against 3.47 under the taffrail (measured against the side so drawn). The form has no third figure
  to give; recorded for the lead.

## 9. Against the file, and Steel's 36 beside

### 9.1 Against `data/ships/frigate-36.yaml` (recorded, not moved)

The file's column stands as the file stood before her lines. The one figure in it that has moved is
each port gun's `height_m`, now its triple's sill (§8.3; `Build-Ships.md` §5.3, read by nothing in
the engine until SW-5's L2). No gun's `x_m`, calibre or number moved.

| Field | The file (its note) | The sheets |
|---|---|---|
| `length_waterline_m` | 41.8 (137 ft, judgement, 0.96 of the gun deck) | 43.74 m (143.5 ft) rabbet to rabbet at WL1; 44.35 m outside post and stem; 45.23 m post to knee (measured) |
| `beam_m` | 11.7 (38 ft 4 in extreme, Winfield, *Amazon* as built) | 11.63 m (38 ft 2 in) extreme, the design's table (read); 37 ft 6 in moulded (read, measured). The as-built figure is no fault of the design's |
| `draught_m` | 4.6 (15 ft mean, judgement; 13 ft forward, 17 ft aft stored for sea) | 5.64 m (18 ft 6 in) at the middle to K, 5.86 m aft, 5.42 m forward; 5.47 m to the main keel's lower edge (measured, judgement on WL1) |
| `displacement_kg` | 1,270,000 (Cb 0.55) | the drawn hull 1,448 t, by the helper (§8.4) |
| `lateral_area_m2` | 160 | about 242 m² from the post's heel to the knee, K to WL1, no rudder (measured, ±3%), its centre about 0.4 m abaft x = 0 |
| `deck_height_m` | 1.8 (upper deck at midships, about 6 ft above the load line) | 1.72 m at the middle line, 1.55 m at side (measured) |
| `rudder` | 6.0 m², `span_m` 4.6 | about 6.8 m², 18.6 ft (5.67 m) deep (measured, ±10%) |
| `fore.mast` `x_m`, `rake_deg` | +14.0, 1.5 | **+16.59**, none to 0.1 to K (measured) |
| `main.mast` `x_m`, `rake_deg` | -2.0, 2.5 | **-2.87**, 0.8 to K (measured) |
| `mizzen.mast` `x_m`, `rake_deg` | -16.0, 4.5 | **-15.38**, 2.2 to K (measured) |
| `bowsprit` `x_m`, `height_m` | +21.0; 6.0, its outer end above the deck (7.8 m above the water) | crosses the stem at x about +22.6, its axis 4.17 m above WL1, steeved 19.5° to K; the outer end not drawn (measured) |
| The upper-deck guns | 13 a side, 2.75 m apart from -16.5 to +16.5, `height_m` 2.4 (judgement) | 13 a side (read), 2.97 m apart from -18.57 to +17.34, 3.33 m across the main mast; sills 2.19 to 2.59 m (measured). Steel's band's 2.34 m lies between; so does the file's 2.4 |
| The quarterdeck's guns | 8 × 32-pounder carronades, 2 long 9s, at -7.0 to -17.5 and -4.5, `height_m` 4.5: **INCORRECT by the owner's ruling, kept** | 6 ports a side from -21.49 to -6.35, sills 4.08 to 4.51 m (measured); the table's 8 × 9-pounders (read). The sills at the file's own x, 3.97 to 4.28 m. No calibre or number touched |
| The forecastle's guns | 2 long 9s as chasers at +17.5, 2 carronades at +14.0, `height_m` 4.5 | no port (read); the rail 4.13 m and 4.30 m at those x (measured); the table's 2 of a two-figure calibre (§2.2) |

These are for the lead and the owner. Nothing here moves a figure the physics or the gunnery reads
(principle 8, §5.6). **Plainly:** her hull is drawn at the sheet's length, sourced points winning
(principle 5), since principle 7's scaling is for a stand-in and this is no stand-in. So it runs 1.9
m longer at the water than the file's `length_waterline_m`, and her fore mast stands 2.6 m abaft the
sheet's place on it. **Ruled (the lead, 2026-10-31):** point 6, the points stay the sheet's and x is
not scaled to the file's, recorded and not moved; point 5, the guns as built, the triples at their
places `judged`, §8.2's ports kept for package 81.

### 9.2 Steel's 36 beside (the check; `pages-steel-1805-bodies.md` §4, §5.3; on Steel's load line)

Steel's 877-ton 36 on 137 ft of gun deck is no sister, but her type's table, and the sheet stands
close to it, a bigger ship of the same kind (judgement). By rung the draught replaces it: S stands
above S†, and Steel's figures stay here old beside new (principle 12).

| Item | Steel's 36 | This draught |
|---|---|---|
| Load draught, forward / aft | 17 ft 4 in / 18 ft 4 in, to the main keel | 17.2 / 18.7 ft to the main keel's lower edge (judgement on that line) |
| Keel's underside, at the perpendiculars | -5.28 / -5.59 m (main keel); false keel 0.13 m below | -5.42 / -5.86 m (K, the false keel) |
| Sill at midships | 7 ft 8 in, 2.34 m | 7 ft 2 in to 7 ft 4 in, 2.19-2.23 m |
| Ports | 13 a side, 10 ft apart, 2 ft 10 in by 2 ft 5 in | 13 a side, 9 ft 9 in apart, 2 ft 11 in by 2 ft 5½ in |
| Rail at the dead flat | 3.27 m | 3.51 m |
| Upper deck at side, least | 1.61 m | 1.55 m |
| Quarterdeck at side, fore end / AP | 3.67 / 4.19 m | 3.61 / 4.19 m |
| Quarterdeck rail above its deck at side | 4 ft 0 in | 3.9 ft |
| Forecastle at side | 3.67 m at +9.91, 4.00 m at FP | 3.73 m at +10.42, 4.12 m at FP |
| Forecastle's length | 36 ft 0 in | 38.4 ft |
| Wale | 3 ft 9 in broad, lower edge 0.07 m at the dead flat | 3 ft 8 in, 0.01 m |
| Lower counter's knuckle / upper | 2.70 / 3.39 m | 2.60-2.63 / 3.1-3.3 m |
| Taffrail's top | 5.92 m, 10 ft 3 in abaft AP | 6.03 m, 10.6 ft abaft AP, the upper horn |
| Stern at the top-timber line (Folio LI) | 20 ft 9 in | 20 ft 5 in (moulded) at the taffrail |

## 10. What the sheets cannot give

- **A labelled load line or a draught mark:** WL1 is judgement (§4.2).
- **The deck plans' checks**, on the sheets not fetched: the masts' holes, the ports in plan, the
  breadth at the rail and each deck, the hatches and the capstan's and galleys' places.
  ZAZ2562-2565 and ZAZ2590-2593 would give them; none is needed for the drawing (judgement).
  `Build-Ships.md` §5.9 names them.
- **The stern's face:** no elevation, no count of stern lights, no carving (§5.6). The body plan's
  stern board gives the outline and the counters only.
- **The figure:** none drawn. **Paint:** none shown on these sheets.
- **The bulwark's half-breadth on the quarterdeck**, above the plank-sheer: not drawn in the body
  plan.
- **Sections under the breadth from the body plan itself:** the outer one only. Between the
  waterlines a section is the rule's.
- **The lengths of the spars:** the masts and the bowsprit are stumps, cut off with a jagged line.
  No masting table.
- **Which ship:** nothing separates *Amazon*'s hull from *Emerald*'s on these sheets; the as-built
  2½ in and 2 in in Winfield p. 143 are under a pixel of one sheet.

## 11. Method and files

The images were read with crops and enlargements, and measured by scripts kept outside the
repository in the session's scratch directory, under `hulls/streams/frigate/`: `crop.py` (the
crops), `common.py` and `frame.py` (profiles, peaks, each sheet's frame and the two datums),
`ticks.py`, `fitscale2.py` and `keel.py` (the strips and K), `vlines.py` and `hlines.py` (the
perpendiculars and stations), `wlfit.py` and `tracer.py` (the green lines), `hbcols.py`,
`hbdata.py` and `hb2559.py` (the half-breadths, assigned by hand from the crops on ZAZ2587 and
found again on ZAZ2559), `sheercols.py` and `compile1.py` (the lines by station), `rows.py`,
`headrows.py` (stem, head, stern by rows), `mid_section.py`, `bodyrows.py`, `bodylines.py` (the
body plans), `portbox2.py`, `ports_all.py`, `qd_all.py` (the ports on six sheets), `rail_check.py`
and `checks.py` (§3.3), `compile2.py` and `final.py` (the points of §8), `overlay.py` (every traced
line drawn back on the sheets and checked by eye), and `loadtest.py` (§8.4, through the tree's own
`gen_ships.py` and `freesail`, writing nothing in it). Each takes the cached image by the table in
`common.py`. Winfield is cited by page; the text is not here.

A second reader measured the same lines by other routes, with none of those scripts read, under
`hulls/streams/frigate/xcheck/`; its findings are mended into this note, and its figures agree
within the limits stated here. The catalogue's six object pages were read as text on 2026-10-30
and not kept. The drawing, by the game's own viewer, and the crops beside it are under
`hulls/streams/frigate/build/` and `hulls/streams/frigate/sheets/`, in scratch. A review drew her
outlines over the profile, the plan and the body plan of both draughts, its frame taken from this
note and none of the measuring scripts run, under `hulls/streams/frigate/review/`; what it mended
is §6.3's last two bullets, the rows in §8.4, and the words that follow from them.
