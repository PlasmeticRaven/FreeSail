# Pages: Chapman 1768, Pl. LVII No. 16, the French tartane, and Pl. LXII No. 16, her rig (November 2026)

Package 90's step 1 for the tartane (`Plan-Package90.md` §8.0 step 1, §8.1; `Design-Ship-Tartane.md` §3's
measuring tasks and §4's heights above the deck). It serves `data/ships/tartane.yaml` and
`data/ships/coastguard-tartane.yaml` when her builder writes them. Facts only: the plates are measured
outside the repository on the Sjöhistoriska museet's photographs (§1, §10) and cited by plate and
record; Forfait 1788 is cited by page; nothing in this note copies an image or a source's text, and no
book is quoted beyond a few words. The figures that her design carries are written into it, old
beside new (`Design-Ship-Tartane.md`, revised 2026-11-20). **Finished 2026-11-20 with the lead's
rulings of that day (13:35 UTC, nudge 29)**, each set down where it falls (§0, §4.1 to §4.3, §5.2,
§5.4, §5.6, §5.7, §7 to §10).

**The head of this note is the lead's rulings of 2026-11-20 (nudge 29) on the plate's number, her load
line and her deck.**
- **The French tartane is No. 16 of Pl. LVII, not of Pl. LVIII (ruling 5).** The engraved number on
  the sheet reads "Pl. LVII" and the museum's record of the same sheet names the Flemish privateer (No.
  14), the Bermuda sloop (No. 15) and the French tartane (No. 16); Pl. LVIII holds the Algerine xebec
  (No. 17) and the Maltese galley (No. 18) (read, §1.2). The tree's "Pl. LVIII No. 16" (and "LVIII No.
  15" for the Bermuda sloop) was a citation fault carried from one note into the others (§8),
  **corrected 2026-11-20** wherever it stood; the xebec's Pl. LVIII No. 17 is right and stands.
- **Her load line is H, the line the sheet marks, as the *Diana*'s is (ruling 1).** H is the heavy
  straight line of the profile, run out to the post's after face and the stem's fore face, drawn
  inclined to the keel: it rises 0.29° to the keel's lower edge going forward (0.0051), **drag 0.29
  Swedish ft over the waterline, 0.11 m in hers**. **H′ is recorded beside it**: the two drawn
  waterlines under H, the body plan's three waterlines and the plan's own load waterline follow a
  steeper line (0.63°, 0.0110) that meets H amidships within 2 px and leaves it by 7 px (0.23 ft) at
  the post. In hers H′ stands **+0.085 m at the post, +0.022 m amidships and −0.041 m at the stem**
  against H; the body plan, the half-breadth plan and Chapman's stated draught of 6⅔ ft (his after
  draught, §4.2) follow it (§4.1). **The ruling's condition**: her displacement, KM and lateral area
  are reckoned to H, the line her file's draught is given on. They are (§4.3, §5.6), with one part
  named in §4.3: the waterplane's half-breadths are the plan's load waterline, which lies on H′.
- **Her deck: `deck_height_m` is the measured 0.54 m (ruling 2)**, the deck at side (the plate's dashed
  line) at the midship station, 1.43 ft above H (its lowest 1.38 ft, 0.52 m in hers), against the
  design's 0.9 m. The lead read its readers: the wind taken at the deck and on the hull
  (`physics/sails.py`, `physics/hull.py`) and the lookout's eye (`world/lookout.py`); none is a
  flooding edge or a freeboard. The waist is closed by a high bulwark carrying the ports, **its top
  1.72 m above her water** (§5.2), recorded here by the plate; no new key.
- **The rest, ruled the same day**: the beak 10½ pieds, 3.41 m (ruling 3, JUDGEMENT; §5.4); the
  draught, the waterline and what follows from them accepted as measured (ruling 4; §4.2, §4.3, §5.6);
  the main's rake the owner's 3° forward, Chapman's upright recorded (ruling 6; §7); no raised after
  deck, the four ports a side, Pl. LXII's two-masted rig, and the mizen's rake still JUDGEMENT, written
  into the design (ruling 7; §5.2, §5.7, §7).

The marks:

- **read**: the plate's drawing, its engraved writing or the record's text was seen on the image.
- **catalogue**: from the museum's record or its manifest.
- **measured**: off the image at the scale of §3, by a script or on a gridded crop; the uncertainty is
  stated.
- **computed**: arithmetic on measured or read figures.
- **memory, unverified**: not checked during this measuring.
- **JUDGEMENT**: reasoning by this note, a figure a file would carry; *judgement* where it only
  identifies a line.

**Units and datums.** Swedish feet (0.2969 m), with metres. Chapman's stations are the sheet's own
labels on the keel: aft 8 to 1, ⊕, fore 1 to 7, and fore 8 and 9 written on the stem's curve, with a
tenth line forward of them (read). **The file's frame (Build-Ships §5.1; the design's §3, "lengths by the
waterlines' ratio, sections by the beams'"): x in metres forward of the middle of her load waterline,
between the post's after face and the stem's fore face on it; z in metres above it, square to it;
half-breadths (hb) in metres.** Checked before writing (§4.1): the design names no datum line, and its
draught (2.50 m) is Chapman's stated 6⅔ ft taken as level; the drawn line is inclined, so every point
here is measured from the heavy line itself, x along it and z square to it, its middle the origin.
Every figure is given twice where it matters: **Chapman's own** (Swedish feet, or metres at his size,
"ch m") and **hers** (metres, scaled by §3.4's factors). The photograph is turned 1.2° on its page and a
little sheared (§3.3); both are taken out by measuring along the drawn lines, not along the image's rows.

## 0. In brief

- **Fetched at full size, public domain**: the Sjöhistoriska museet's photographs of Pl. LVII and Pl.
  LXII, 6,000 × 4,258 px, under the Public Domain Mark (§1.1); Forfait's Table II leaf from the Internet
  Archive (§1.3).
- **Scale**: **33.47 px a Swedish foot**, from the S bar's fifteen whole feet; the E and F bars read in
  the true ratios of the English and French foot (0.978, 0.917 against 0.974, 0.914). The bars end at
  the 15-ft division although the engraved figure at the end reads "20" (read; §3.1).
- **Checked against the 1971 reprint's table** (`VesselReferences-2026-10.md` §3.1, read there): between
  the perpendiculars **62.39 ft against 62¼ (+0.2%)**; breadth **17.51 ft on the body plan's dashed sides,
  17.60 on the half-breadth plan's outer line, against 17 7/12 (−0.4%, +0.1%)**; draught 6.47 ft at the
  after perpendicular to the keel's lower edge on the heavy line (−3.0%), 6.70 on the steeper line
  (+0.5%) (§3.2, §4.2). Heights up the page read as lengths along it within 0.7% (§3.3).
- **Her waterline is 16.79 m on the plate (56.55 ft), not about 18.5 m**: the design's figure was
  Chapman's length between the perpendiculars (18.52 m measured, 18.48 stated). The stem rakes forward
  4.6 ft from the water to the stem head, the post aft 1.5 ft (§4.1). On her 20.38 m between the
  perpendiculars, **her load waterline is 18.47 m** (§3.4).
- **Her factors** (principle 7; §3.4): **lengths 1.100**, **sections 1.268**; above the water the side's
  height at midships by the sections' factor and the sheer's rise by the lengths', so heights above
  water are scaled by 1.265 amidships falling to 1.14 to 1.15 at the ends (JUDGEMENT on principle 7's
  words).
- **Her draught**: **2.38 m** at the middle of her waterline to the keel's lower edge, 2.43 m at the
  post, 2.32 m at the stem (§4.2). Displacement drawn to the line: **about 135 t** (±6%), block 0.51,
  midship 0.83, waterplane 0.69; KB 1.48 m above the keel, BM 1.66 m, **KM 3.15 m**, all on H (§4.3). Accepted
  as measured, with her waterline and her lateral area (the lead, 2026-11-20, ruling 4).
- **Her deck and side**: the deck at side 0.54 m above her water at midships, rising to 1.77 m at
  x −9.15 and 1.45 m at x +7.19 (where the dashed line ends); a waist bulwark from x −7.06 to +6.5 m,
  its top 1.72 m above the water amidships and 2.61 m at its after end; a lower rail aft of it, 2.24 m
  at the step, rising to the taffrail at (−9.72, 3.30); the bow rail to (10.38, 3.67) (§5.2).
- **The wale** is a band 0.16 m deep that straddles the load line from x −2.5 to +2 m: its lower edge
  0.20 m under the water at the middle (§5.3).
- **The stem** rakes forward from the forefoot at (6.71, −2.32) through (9.25, 0.00) to a tall stem
  head whose top stands at (10.58, 4.74); **the beak** runs out level to an eye at **(14.36, 2.85)**,
  the berthelot ending at 14.10: **3.53 to 3.79 m beyond the stem head** in hers (Chapman's 10.8 to 11.6
  ft) (§5.4). Forfait's Table II prints 10½ pieds and the ratio 0.151 for the *Humble* on the page itself
  (read on leaf n179, §1.3): the two disagree on the page, as the research note had them. **Ruled**
  (the lead, 2026-11-20, ruling 3): **10½ pieds (3.41 m)**, the printed ratio taken as the misprint
  (JUDGEMENT).
- **The stern** is sharp: the post's after face raked 8.4° from the square of the keel runs straight to
  the taffrail; the planking closes on the post with no transom, the rail flaring out to 4.3 ft of
  half-breadth by station aft 8 (§5.5).
- **The ports**: **four a side**, closed lids with two strap hinges each, hinged on the side away from
  midships; centres at x −4.66, −1.94, +3.21, +5.93 m, sills 1.11 to 1.57 m, **0.52 by 0.54 m** in hers
  (§5.7). No swivel is drawn.
- **No mast is drawn on Pl. LVII No. 16.** Pl. LXII No. 16, the tartane among Chapman's 24 rigs, is a
  **two-masted lateen with no topsail, no mizen and no headsail**: the main **upright** (0.6° to 1.1°
  aft, ±0.5°) at the middle of her length, a fore mast **raked 23° forward** 0.34 of her length before
  the middle, the main yard 1.20 of the hull's length (Forfait's *Humble* 1.195) (§7). **The mizen's rake
  cannot be read on either plate**: neither has a mizen. The design keeps the owner's 3° forward for
  the main (ruling 6), and the mizen's rake stays JUDGEMENT (ruling 7).
- **The heights above the deck** (design §4): at Forfait's main (x +3.87 m in hers) the deck is 0.85 m
  above her water and the keel's upper edge 2.12 m below it: **2.97 m from the deck to the keel's upper
  edge**, so the design's "stepped about 2.8 m below the deck" stands with a keelson of 0.2 to 0.25 m
  (JUDGEMENT); the masthead 16.2 to 16.4 m and the hounds 7.7 to 8.0 m above the deck (§6.4).

## 1. The sources

### 1.1 The images

| | Pl. LVII (the hull, No. 16) | Pl. LXII (the 24 rigs, No. 16) |
|---|---|---|
| Record | Sjöhistoriska museet, "Ritning", Plansch LVII of *Architectura Navalis Mercatoria* (1768), https://digitaltmuseum.org/011024789749; manifest https://ems.dimu.org/api/iiif/011024789749/manifest.json (catalogue) | Plansch LXII, https://digitaltmuseum.org/011024789758; manifest https://ems.dimu.org/api/iiif/011024789758/manifest.json (catalogue) |
| Rights shown | "Public domain mark (CC pdm)", credit "Photo: Sjöhistoriska museet" (read on the record page) | the same |
| Image measured | `0136NR46qsqT`: https://ems.dimu.org/image/0136NR46qsqT?filename=Architecturan%20LVII.jpg&dimension=max&quality=100&dpi=300&mediatype=image/jpg, **6,000 × 4,258 px**, 21,221,475 bytes, sha256 `d049432b390cfee864f507dac7f9a3a5dc09f9a1bba3a0591bc52f6ae892e807`; the whole opening, colour | `0136NR46qszG`: the same address with that id, **6,000 × 4,258 px**, 22,810,668 bytes, sha256 `1a6061ddbc50bd929599cbed4dcb0fe83494d6c084ae064cfd73b4b8aad39653` |
| Image fetched, not used | `022uK3KjAwHw`, 4,000 × 2,896 px, 3,201,041 bytes, sha256 `6dd3a015abdf9a7bcf4f4b63849bb7685fde8589d66b860cb6ef06564b4c29b7` | `042uK3KjAwNF`, 4,000 × 2,862 px, 4,058,334 bytes, sha256 `eba9a65fdc6ebf4827c8bd4ad42e5e89687575b89ab442f8db83e0aa541e14b4` |
| Also fetched | Pl. LVIII's record (https://digitaltmuseum.org/011024789752) and its 1,200-px view of `0136NR46qsqW`, to read its plate number and figures | — |
| Cache | `D:/Projects/FreeSail/reference-cache/tartane/chapman-pl57/`, `.../chapman-pl62/`, `.../chapman-pl58-check/`; the record pages and manifests in `.../record/`. Fetched 2026-11-20 with a generic user agent | |

**How the records were found.** The museum's search page sits behind a browser challenge, which this
step did not pass; its records and image service answer directly. Pl. LIX's record (the smack's, held
in the cache) was 011024789741; the IIIF manifests of the neighbouring record numbers, 011024789700 to
011024789900, were read one by one (201 small requests at a polite pace, `scan_dimu.py`), and the
plates of *Architectura Navalis Mercatoria* were found among them by their descriptions (catalogue).
Wikimedia Commons holds no copy of Pl. LVII; it holds a reduced Pl. LXII whose description gives
Chapman's own caption for the rigs (read: https://commons.wikimedia.org/wiki/File:Chapman_sammmanst%C3%A4llning_fartygstyper_1768.jpg).

### 1.2 What is on the sheets (read)

- **Pl. LVII.** "Pl. LVII" engraved at the upper right; No. 14 (the Flemish privateer *Neptunus*) across
  the top, No. 15 (the Bermuda sloop) at the lower left with her spars drawn between the two (a mast,
  a boom, a gaff with its jaws, lettered A to G), **No. 16 at the lower right**: a body plan above her
  sheer, the half-breadth plan hung under the keel with its hatches and fittings drawn, and three scale
  bars lettered S, E and F to her upper right. The museum's description names No. 16 a French tartane
  (catalogue).
- **Pl. LVIII**: "Pl. LVIII" engraved; Nos. 17 and 18, the Algerine xebec and the Maltese galley *La
  Capitana* (read; catalogue). No tartane.
- **No. 16 as drawn** (read): the sheer with the stations' lines; two dashed perpendiculars, the after
  one touching the post's after face at the taffrail, the fore one the stem head's fore face; a dashed
  base line from the after perpendicular joining the keel's upper edge; the keel's lower edge under the
  station numbers; one heavy straight line run out to the post's and the stem's faces, and two thin
  straight lines under it; a heavy curve from the post down nearly to the keel amidships and up to the
  stem (a rising line or a diagonal's trace, *judgement*; not used); the side's bands; a dashed deck
  line; four ports with closed lids; a tall stem head; the beak with its berthelot to an eye; **no
  mast, no rudder**. The body plan: frames ⊕ and aft 1 to 8 on the left, ⊕ and fore 1 to 9 on the
  right, a diagonal each side with the frames' numbers along it, three waterlines in each half, the
  heaviest run out beyond the dashed sides.
- **Pl. LXII**: "Pl. LXII", twenty-four rigs to one scale with a diagonal scale bar of S, E and F feet
  at the bottom (read). Chapman's caption (read on the Commons page, Sjöhistoriska museet's copy): No. 16
  is the "Tartane"; the drawings share one scale; square yards are drawn braced at 60° to the middle
  line, so that their true lengths are twice what is drawn. A lateen yard lies in the plane of the
  drawing and is drawn at its length (*judgement*).

### 1.3 Forfait 1788

Forfait, *Traité élémentaire de la mâture des vaisseaux*, Paris 1788, Internet Archive item
`bub_gb_AQUHAAAAQAAJ` (the item states the Public Domain Mark; catalogue): leaf **n179** (p. 134, Table
II), https://archive.org/download/bub_gb_AQUHAAAAQAAJ/page/n179.jpg, 2,500 × 3,531 px, sha256
`b16c8fdf35e1fe999ab28db52f88506e4110888c50de52a32e7f8450759a0a87`, cached in
`.../reference-cache/tartane/forfait-1788/`. Read on it: the éperon's row of the *Humble* (both her
columns) prints the ratio **0.151** and the length **10½** pieds; the *Espiègle*'s 0.196 and 10
(read). 10½ ÷ 62¾ = 0.167 and 0.151 × 62¾ = 9.48 (computed): the disagreement is the page's own, not a
misreading. **Forfait's figures (figs. 9 and 35) were not reached**: the item's last leaves (n398 to
n404, fetched) are blank and end papers; no plate leaf was found in the time given (§9).

**Leaf n166 (p. 121)**, read on its page image for the tartane builder's question 1 (the cut of her
lateens): https://archive.org/download/bub_gb_AQUHAAAAQAAJ/page/n166.jpg, 2,500 × 3,500 px, sha256
`0fdf7d6cccd7d75b11b88e0cc2f7a558ec608da3084fa79b96d24e75da19e5c1`, cached beside n179 with its
neighbours n165 and n167 (pp. 120 and 122). Read on it, in our words:
- the lateen's head is the yard less its two ends, which the page gives as 2 to 3 pieds at the
  penne and 10 to 15 pouces at the car;
- with the yard fully peaked, as in the vessels of figs. 35 to 38, the clew falls on the deck at
  the foot of the mast;
- the yard is hoisted until its jeers' block meets the return block at the mast's head, or the
  sheave cut in the mast for the jeers;
- of fig. 35's rig (one mast at the middle or a little forward): the car is tacked at the stem.

So the design's reading, which the builder took literally, is the page's (the clew on the deck at
the mast's foot, the car at the stem). The *Humble*'s own ends in Table II (1½ pieds and ¾ pied)
lie under p. 121's general band; her own row stands. Page 122 (n167) is on the use of fig. 35's rig
and its Table I, not the cut.

## 2. The table and the figures read

- **The 1971 reprint's table** was not re-read here (in copyright; the tree's reading, `VesselReferences-
  2026-10.md` §3.1, stands as "read there"): 62¼ Swedish ft between the perpendiculars, 17 7/12 moulded,
  draught 6⅔; eight 4-pounders and four swivels.
- **Written on the sheet** (read): the plate number, "No 16", the station figures, the frames' numbers on
  the diagonals, the bars' letters and figures. No line is named and no draught is marked.

## 3. The scale and its checks

### 3.1 The bars (measured)

The three bars to No. 16's upper right, each a foot at the left divided in quarters, then whole feet:

| Bar | Px a foot (fit over the divisions) | End to end | In the true ratio of the feet |
|---|---|---|---|
| S (Swedish) | **33.47** (0 at x 4,149.5, the 15th division at 4,651.5; 5 and 10 at their engraved figures) | 15 ft | — |
| E (English) | 34.23 (14 divisions from 1, 34.32) | 15 ft | S/E 0.978 against 0.974 |
| F (French) | 36.5 (13 divisions, 36.50) | 15 ft | S/F 0.917 against 0.914 |

- **The bars' end figure reads "20" at the 15th division** on all three (read, zoomed); the 5 and 10
  stand at their divisions. Taken as an engraver's slip (JUDGEMENT): the divisions, their ratios and the
  length between the perpendiculars (§3.2) agree on feet of 33.47 px.
- **The stations** stand 99.58 px apart (aft 8 to fore 7, 15 spaces), **2.975 ft** (measured, ±0.1
  px): not a round 3 ft. Were they 3 ft, the scale would be 33.19 px and the length 62.91 ft (+1.1%);
  the bar is kept.
- **Taken: 33.47 px a Swedish foot (±0.2%)**; one pixel is 0.030 ft, 8.9 mm of Chapman's tartane.
  Point readings ±1 px on a traced line, ±2 to 3 px by eye on a gridded crop; traced lines carry their
  fit's rms, stated where used.

### 3.2 The stated dimensions measured back (measured)

| Dimension | Stated (the 1971 table, read there) | Measured | Difference |
|---|---|---|---|
| Between the perpendiculars | 62¼ ft (18.48 m) | 2,088.1 px along the base line, **62.39 ft (18.52 m)**; 2,088.9 px on the load line | +0.2% |
| Breadth moulded | 17 7/12 ft (5.22 m) | the body plan's dashed sides 586.1 px, **17.51 ft**; the half-breadth plan's outer line at ⊕, 2 × 8.80 = **17.60 ft** | −0.4%; +0.1% |
| Draught | 6⅔ ft (1.98 m) | to the keel's lower edge at the after perpendicular: **6.47 ft** on the heavy line, **6.70 ft** on the steeper line (§4) | −3.0%; +0.5% |

### 3.3 The sheet's vertical and its lean (measured)

- **Up the page against along it.** The plan's load waterline at ⊕ stands 290.1 px from the plan's
  centre line (up the page); the body plan's ⊕ frame at the load line's height stands 288.0 px from its
  centre line (along the page): **1.007**. The plan's outer line at ⊕, 294.4 px, against the body plan's
  half-breadth on its sides, 293.0 px: **1.005**. Heights are taken at the bar's 33.47 px (±0.7%), with
  no factor: unlike Pl. LIX's photograph (`pages-chapman-pl59.md` §2.2, 0.970), this one is not short up
  the page.
- **The turn.** The keel's lower edge runs at 0.02149 of the image's rows (1.23°), the base line at
  0.02202, the bars at 0.019 to 0.021, the body plan's base at 0.0185 to 0.019.
- **The shear.** The perpendiculars and the station lines lean −0.0143 to −0.0177 (dx/dy) where a line
  square to the keel would lean −0.0215: the sheet's "verticals" stand 0.2° to 0.4° off the square of its
  "horizontals" (measured). Every reading is therefore taken along the drawn lines: x along the load
  line, z square to it, each station's x where its own line crosses the load line.

### 3.4 Her factors (computed; JUDGEMENT on the choice)

- **Lengths, F_L = 1.1003**: her 20.38 m (Forfait's *longueur*, taken as Chapman's between the
  perpendiculars, JUDGEMENT as the design's) over the measured 18.52 m. On the stated 62¼ ft it would be
  1.1027 (+0.2%).
- **Sections, F_B = 1.2682**: her 6.61 m over the measured breadth, the mean of §3.2's two, 17.56 ft
  (5.212 m). On the stated 17 7/12 ft it would be 1.2663 (the design's 1.27).
- Both are taken on the measured figures so that the drawn hull is her file's length and breadth
  exactly (principle 7's last sentence).
- **Heights.** Under the water, ×F_B. Above it, principle 7: "the height of her side above the water
  from her own source ... and the sheer's rise above it by the length ratio". She has no source of her
  own for the side, so at midships the height is scaled as the section (×F_B), and the rise of the
  deck's sheer above its lowest point (1.384 ft, at x +1.2 ft) by F_L. Every z above the water at x is
  multiplied by **k(x) = (F_B·1.384 + F_L·(s(x) − 1.384)) / s(x)**, s(x) the deck at side's height at x
  in feet (§5.2; held at the deck line's ends beyond them). k is 1.265 amidships, 1.198 at Forfait's main,
  1.145 at the taffrail and 1.155 at the deck line's fore end (computed). JUDGEMENT on the way principle 7
  is applied; the builder may choose another, from Chapman's feet in this note.

## 4. The load line, first

### 4.1 The lines and the frame (measured)

Each fitted straight on the image (`fitline.py`, three-px steps, outliers past 2.5 sd dropped):

| Line | Fit (image px, y = k x + b) | rms | What it is |
|---|---|---|---|
| H, the heavy straight line | k 0.02657, b 2,908.13, x 2,760 to 4,530 | 0.44 px | run out to the post's after face aft; forward, a branch 3 to 4 px under it runs to the stem's fore face from x 4,400 while it ends on the heavy curve at 4,600: **the load line as drawn** (*judgement*, by its weight and its ends) |
| WL2, thin | k 0.03247, b 2,932.90 | 0.62 | a waterline, from the post's fore face to the stem's rabbet |
| WL3, thin | k 0.03247, b 2,981.53 | 0.58 | the next waterline, 48.6 px under WL2 |
| Base line | k 0.02202, b 3,115.28 | 0.72 | dashed from the after perpendicular, solid along the keel: the keel's upper edge (*judgement*) |
| The keel's lower edge | k 0.02149, b 3,138.39 | 0.57 | under the station figures; the half-breadth plan's centre line (its hatches hang from it) |

- **H is inclined to the keel's lower edge by 0.00508 (0.29°)** and to the base by 0.00455 (0.26°),
  deeper aft. WL2 and WL3 are inclined by 0.0110 (0.63°), parallel to each other.
- **The steeper line (H′).** A line parallel to WL2 and 48.6 px above it (the waterlines' own spacing)
  is not drawn aft; forward, the branch from x 4,400 to the stem's face lies on it within 1 px. The body
  plan's three waterlines are drawn as straight lines inclined in each half (inner ends higher aft,
  lower forward, as drag draws them), and their heights at their ends fit H′, WL2 and WL3 within 1 to 3
  px, where H misses the body plan's load line by 6 to 8 px at the end frames (measured). The plan's
  heavy load waterline is the body plan's (§5.1). So the plate is not at one with itself: **the lines
  used to build her body (the waterlines, the body plan, the plan) follow H′; the profile's heavy line
  is H.** H′ stands Δ(x) = 0.059 − 0.00589·x ft above H (x in ft): +0.23 ft (7 px) at the post, +0.06
  at the middle, −0.11 at the stem (computed). In hers, **+0.085 m at the post, +0.022 m at the middle,
  −0.041 m at the stem**.
- **The perpendiculars** (fitted): after, x = −0.01427 y + 2,757.10 (rms 0.18 px); fore, x = −0.01771 y +
  4,856.45 (rms 0.14). The after one meets the post's after face at the taffrail, (2,718.7, 2,655.0); the
  fore one the stem head's fore face.
- **The ends of the load line on H**: the post's after face (x = 0.12517 y + 2,386.41, rms 0.23 px)
  meets H at (2,759.6, 2,981.4); the stem's fore face (traced, §5.4) meets it at (4,651.6, 3,031.7).
  **The waterline: 1,892.7 px, 56.55 ft, 16.79 m** at Chapman's size; **18.47 m in hers**. Its middle,
  the origin of this note's frame, is image (3,705.6, 3,006.6), 26 px (0.78 ft) forward of station ⊕
  and 1.49 ft abaft the middle of the perpendiculars (computed).
- **Taken for the frame: H**, the line drawn (JUDGEMENT, by the *Diana*'s ruling of 2026-11-20 that her
  load line is "the arrowed line as drawn"). Every z of this note is above H; on H′ subtract Δ(x).
  The difference is 3 to 9 cm in hers.
- **Ruled (the lead, 2026-11-20, ruling 1): her load line is H**, the line the sheet marks, as for the
  *Diana*. H′ is recorded beside it: inclined 0.63° to the keel's lower edge against H's 0.29°; above
  H by +0.085 m at the post, +0.022 m amidships and −0.041 m at the stem, in hers; the body plan, the
  half-breadth plan and Chapman's stated after draught follow it. **The condition**: her displacement,
  KM and lateral area are reckoned to H, the same line her file's draught is given on (§4.3, §5.6).

### 4.2 The draughts (measured, in the frame)

| To | After perpendicular | The post's after face | Middle of the waterline | The stem's fore face | Fore perpendicular |
|---|---|---|---|---|---|
| The keel's lower edge, on H (ft) | 6.468 | 6.461 | **6.317** | 6.174 | 6.151 |
| The base line, on H (ft) | 5.820 | 5.814 | 5.685 | 5.557 | 5.536 |
| The keel's lower edge, on H′ (ft) | **6.701** | 6.686 | 6.376 | 6.066 | 6.016 |
| **Hers, to the keel's lower edge, on H (m)** | 2.44 | **2.43** | **2.38** | **2.32** | 2.32 |

- ±0.03 ft. The keel's lower edge is 0.63 ft (0.24 m in hers) under the base line (21.2 px).
- **The stated 6⅔ ft fits the after draught on H′** (6.70, +0.5%), as Pl. LIX's 6½ fitted the smack's after
  draught (`pages-chapman-pl59.md` §2.3). On H the after draught is 6.47 ft, 3.0% short. Chapman's table
  names no place (read there); JUDGEMENT that it is the after draught.
- **Hers**: `draught_m` **2.38 m**, the mean to the keel's lower edge at the middle of her waterline;
  2.43 m at the post and 2.32 m at the stem (drag 0.11 m over her waterline). On H′: 2.40 m mean, 2.52
  m at the post, 2.28 m at the stem. The design's 2.50 m was Chapman's after draught scaled and taken as
  level (§8). **Accepted as measured** (the lead, 2026-11-20, ruling 4): her draught is the mean on the
  drawn line H, Chapman's stated 6⅔ ft his after draught.

### 4.3 The drawn displacement and stability (measured, computed)

**Method** (`disp.py`): sections below H at the nineteen stations: at the ten whose frames were traced
on the body plan (§6.1) integrated from the base line to H; at the others the plan's load-line
half-breadth times the depth times the section coefficient interpolated from the traced ones (held at
the end values, 0.58 aft and 0.69 forward); the sections joined by trapezoids from the post's after face
to the stem's fore face; the keel below the base line added (12 ft³). Sea water 1.026 t a cubic metre.

| | Chapman's (ft³; t) | Hers (t) |
|---|---|---|
| The body to H, moulded | 2,841 ft³; 76.3 t | 134.6 |
| With the keel | 2,853 ft³; 76.6 t | **135.2** |

- **Error ±6%**: the ends' sections are coefficients, not traces (stations aft 7 and 8, fore 6 to 9),
  and are likely a little full (computed; JUDGEMENT on the band). On H′ about 1% more.
- **Coefficients**, to the base line: block 0.51, midship 0.83, waterplane 0.69; the centre of buoyancy
  0.33 ft abaft the middle (computed).
- **Hers**: displaced volume 131.7 m³; KB 1.48 m above the keel's lower edge; transverse BM 1.67 m
  on the plan's load-line half-breadths (H′), KM 3.16 m; **on H, BM 1.66 m and KM 3.15 m**, below. The
  design's GM of 0.8 m would put her centre of gravity 2.35 m above the keel, about at her waterline;
  KG is JUDGEMENT (computed).
- The design's 155 t (Cb 0.48 on 19.0 × 6.61 × 2.50 m) was on the longer waterline and the deeper
  draught. Measured: 135 t, −13%.

**Reckoned to H** (ruling 1's condition; accepted as measured, ruling 4). The sections are integrated
from the base line to H and the keel's depth is taken under H, so the volume, KB and the draught are
H's (`disp.py`). **One part is not**: the waterplane's half-breadths, for BM and for the untraced
stations' sections, are the plan's heavy load waterline, which is drawn on H′ (§4.1). Carried down to
H by the flare of §6.3's traced sections near the water (H′ standing Δ(x) above H), the waterplane on
H is narrower a side in hers by 0.03 m at aft 6 and aft 7, 0.02 m at aft 5 and about 0.01 m elsewhere
aft, under 0.01 m amidships, and wider by up to 0.02 m at fore 8 and fore 9; its second moment is 0.6%
less, **BM 1.66 m and KM 3.15 m on H**; the volume moves by under 0.1% (computed 2026-11-20 on §6.2's
and §6.3's figures; no image measured again). **By ruling 1's condition her figures are H's, so KM
is 3.15 m** (3.16 m on H′'s waterplane, recorded), the displacement 135 t either way. The same cause
reaches `breadth_m`'s half-breadths at the water (§6.2), which the plan draws on H′: they are carried
down to H by the same flare, station by station, and §6.2 now gives H's (H′'s beside them here: aft
to fore 0.87, 1.60, 2.19, 2.60, 2.89, 3.09, 3.21, 3.26, 3.27, 3.26, 3.21, 3.10, 2.90, 2.57, 2.13, 1.55,
0.93, 0.38). Where a frame is traced, its half-breadth at z 0 (§6.3) is H's already.
Looked for in the *Diana*: her load line is her plan's own first waterline, and her body plan draws it
at the heights her sheer gives (`pages-diana.md` §3.2, §4.1), so the cause does not reach her.

## 5. The profile, measured

### 5.1 By station: the water, the rail and the keel (measured)

x and z in the frame; Chapman's feet, and hers in metres. hb at the water is the plan's heavy load
waterline (traced end to end, `hD`), read at each station's line in the plan, ±0.03 ft; the plan's
outer line (`hE`) is the half-breadth plan's main breadth line; the rail's hb is the body plan's frame
cut at the profile's rail (§6.1).

| Station | x ft | Keel z ft | hb water ft | hb main line ft | Deck z ft | Rail z ft | Rail hb ft | Hers: x, keel z, hb water, deck z, rail z, rail hb (m) |
|---|---|---|---|---|---|---|---|---|
| aft 8 | −24.55 | −6.44 | 2.31 | 3.07 | 4.47 | 7.54 | 4.30 | −8.02, −2.43, 0.87, 1.53, 2.58, 1.62 |
| aft 7 | −21.55 | −6.43 | 4.26 | 4.75 | 3.89 | 6.91 | 6.00 | −7.04, −2.42, 1.60, 1.34, 2.38, 2.26 |
| aft 6 | −18.56 | −6.41 | 5.83 | 6.03 | 3.36 | 6.79 | 6.96 | −6.06, −2.41, 2.19, 1.17, 2.36, 2.62 |
| aft 5 | −15.61 | −6.40 | 6.92 | 7.04 | 2.90 | 6.16 | 7.45 | −5.10, −2.41, 2.60, 1.02, 2.16, 2.81 |
| aft 4 | −12.65 | −6.38 | 7.69 | 7.84 | 2.50 | 5.63 | 7.74 | −4.13, −2.40, 2.89, 0.89, 1.99, 2.91 |
| aft 3 | −9.67 | −6.37 | 8.21 | 8.45 | 2.17 | 5.22 | 7.88 | −3.16, −2.40, 3.09, 0.78, 1.87, 2.97 |
| aft 2 | −6.70 | −6.35 | 8.51 | 8.70 | 1.89 | 4.94 | (7.95) | −2.19, −2.39, 3.21, 0.69, 1.79, (3.00) |
| aft 1 | −3.72 | −6.34 | 8.65 | 8.78 | 1.60 | 4.72 | (8.02) | −1.21, −2.39, 3.26, 0.59, 1.75, (3.02) |
| ⊕ | −0.71 | −6.32 | 8.68 | 8.80 | 1.43 | 4.58 | 8.07 | −0.23, −2.38, 3.27, 0.54, 1.72, 3.04 |
| fore 1 | 2.23 | −6.31 | 8.66 | 8.77 | 1.45 | 4.66 | 8.01 | 0.73, −2.37, 3.26, 0.54, 1.74, 3.02 |
| fore 2 | 5.21 | −6.29 | 8.52 | 8.64 | 1.72 | 4.93 | 7.93 | 1.70, −2.37, 3.21, 0.63, 1.81, 2.99 |
| fore 3 | 8.18 | −6.27 | 8.24 | 8.43 | 1.99 | 5.28 | 7.80 | 2.67, −2.36, 3.10, 0.72, 1.91, 2.94 |
| fore 4 | 11.15 | −6.26 | 7.69 | 8.08 | 2.30 | 5.70 | 7.65 | 3.64, −2.36, 2.90, 0.82, 2.03, 2.88 |
| fore 5 | 14.13 | −6.24 | 6.83 | 7.58 | 2.71 | 6.21 | 7.37 | 4.62, −2.35, 2.57, 0.96, 2.19, 2.77 |
| fore 6 | 17.10 | −6.23 | 5.64 | 7.05 | 3.19 | 6.81 | 6.98 | 5.59, −2.35, 2.13, 1.11, 2.37, 2.63 |
| fore 7 | 20.08 | −6.21 | 4.11 | 6.51 | 3.78 | 7.47 | (6.2) | 6.56, −2.34, 1.55, 1.30, 2.58, (2.3) |
| fore 8 | 23.04 | −6.20 | 2.48 | 5.06 | — | 7.35 | (5.0) | 7.53, −2.33, 0.93, —, 2.52, (1.85) |
| fore 9 | 26.01 | −6.18 | 1.00 | 3.51 | — | 7.92 | 3.42 | 8.50, −2.33, 0.38, —, 2.72, 1.29 |
| fore 10 | 28.53 | −6.17 | — | 2.13 | — | 8.96 | — | 9.32, −2.32, —, —, 3.07, — |

- **Station spacing** 2.975 ft (§3.1); ⊕ stands 0.71 ft abaft the waterline's middle. Fore 10 lies 0.26
  ft forward of the stem's fore face at the water: the stem at the water lies between fore 9 and 10.
- Figures in brackets are interpolated between traced frames, not traced (JUDGEMENT).
- **The frames' heads in the body plan stand 0 to 0.57 ft above the profile's rail at the same station**
  (mean +0.2 ft; aft 7, at the bulwark's after end, +0.89) (measured): cut at the profile's rail, as
  `pages-diana.md` §6.3 found the *Diana*'s body plan's tops 0.4 pie off her sheer.
- **The body plan against the plan** at the load line: the traced frames' half-breadths at each
  station's load-line height against the plan's load waterline: aft 3 −0.12, aft 4 −0.05, aft 5 −0.17,
  aft 6 −0.17, aft 8 +0.22, ⊕ +0.07, fore 1 to 3 −0.13 to −0.27, fore 4 −0.08, fore 5 −0.05 ft
  (measured): within 0.1 to 0.27 ft (3 to 9 px). The plan's figures are taken for the water.
- **The plan's lines at the ends.** Abaft aft 6 and forward of fore 5, the half-breadth plan's outer
  thin lines lie outside its main breadth line (at aft 8, 4.34 and 4.53 ft against 3.07): the topsides
  flare to the rail at the ends (measured; the body plan's aft 8 frame reaches 4.30 ft at its head).

### 5.2 The rail, the bulwark, the planksheer and the deck (measured; ±0.03 ft)

Traced end to end by a curve follower (`follow.py`) and drawn back on the image (`ov.py`); z at x
(ft; hers in metres below each row):

| x ft | −29.75 | −28 | −24 | −22 | −21.6 | −20 | −16 | −12 | −8 | −4 | 0 | +4 | +8 | +12 | +16 | +20 | +24 | +28 | +31 | +31.8 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Top of side (rail) | 9.72 | 8.95 | 7.33 | 6.63 | 6.49 / 7.57 | 7.11 | 6.24 | 5.52 | 5.05 | 4.74 | 4.56 | 4.81 | 5.25 | 5.83 | 6.57 | 7.48 | 7.42 | 8.70 | 10.28 | 10.71 |
| hers (m) | 3.30 | 3.04 | 2.51 | 2.28 | 2.24 / 2.61 | 2.46 | 2.18 | 1.96 | 1.82 | 1.75 | 1.71 | 1.80 | 1.94 | 2.11 | 2.33 | 2.58 | 2.54 | 2.98 | 3.53 | 3.67 |
| Planksheer band, top | | | 6.21 | 5.50 | | 4.85 | 3.69 | 2.76 | 2.16 | 1.76 | 1.51 | 1.71 | 2.12 | 2.73 | 3.60 | 4.79 | 6.22 | 7.87 | 9.26 | 10.14 at +32.7 |
| Deck at side | | 5.20 | 4.36 | 3.97 | | 3.61 | 2.95 | 2.42 | 2.02 | 1.62 | 1.41 | 1.59 | 1.98 | 2.40 | 2.99 | 3.76 | 4.22 at +22 | | | |
| hers (m) | | 1.77 | 1.49 | 1.37 | | 1.25 | 1.03 | 0.86 | 0.73 | 0.60 | 0.53 | 0.59 | 0.71 | 0.85 | 1.05 | 1.30 | 1.45 at +22 | | | |

- **The top of the side is two lines.** Aft, a rail (a thin top line over a heavy one, 0.3 ft apart)
  falls from the taffrail at (−29.75, 9.72) to x −21.60, where it stands at 6.49 ft; there **a waist
  bulwark** begins 1.08 ft higher, at 7.57 ft, with an upright after edge, and runs forward, its lowest
  4.56 ft at x 0, to a small rise at x +19.8 to +20.0 (7.43 to 7.48 ft), then on as the upper bow rail to
  its end at (31.78, 10.71) by the stem head. A second, shorter bow rail runs under it to the stem head
  (read; measured where traced).
- **The planksheer band** (two lines 0.47 ft apart, the upper thin) runs from the stern to the stem head,
  (32.70, 10.14) (read; *judgement* on the name).
- **The deck at side is the dashed line** (*judgement*, as on the other Chapman plates): faint and broken
  (readings at 22 places by column scans, darkness 17 to 57; hidden inside the planksheer band from x −7.5
  to +5.8 ft, where it is taken 4.5 px under the band's top, as read on either side of the gap, ±2 px).
  Its sheer is flatter than the side's: it lies under the wale band at the stern (x −28), crosses the
  wale band and then the planksheer band going forward, and runs inside the planksheer band amidships.
  **Its lowest is 1.38 ft at x +1.2 (0.41 m; hers 0.52 m); at ⊕ 1.43 ft (hers 0.54 m).** The dashed
  line ends at x +22.1 ft (hers 7.19 m, 1.45 m above the water); forward of it the deck is not drawn.
- **No raised after deck is drawn**: the deck line runs on aft unbroken (read). The bulwark over the deck
  is 3.0 to 3.2 ft high in the waist (0.94 m; hers 1.18 m) and the rail aft 2.5 to 3.6 ft. Written into
  the design (the lead, 2026-11-20, ruling 7).
- **Ruled (the lead, 2026-11-20, ruling 2): `deck_height_m` is the measured 0.54 m**, the dashed deck at
  side at the midship station (its lowest 0.52 m, at x +1.2 ft). The lead read its readers: the wind
  taken at the deck and on the hull (`physics/sails.py`, `physics/hull.py`) and the lookout's eye
  (`world/lookout.py`); none is a flooding edge or a freeboard. **The bulwark's top, 1.72 m above her
  water amidships** (4.56 ft at x 0 on the plate), is recorded here by the plate; no new key.

### 5.3 The wale (measured; ±0.03 ft)

A band of two lines, the upper thin, 0.47 to 0.53 ft deep (0.16 m in hers). Traced from the stern to
x −7.4 ft by the follower; forward of it read by column scans at eleven places (the follower ran onto
the load line there).

| x ft | −26 | −22 | −18 | −14 | −10 | −6 | −2 | 0 | +2 | +6 | +10 | +14 | +18 | +22 | +26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Upper edge | 5.46 | 3.96 | 2.68 | 1.63 | 0.84 | 0.35 | 0.23 | 0.17 | 0.12 | 0.30 | 0.81 | 1.59 | 2.65 | 3.99 | 5.56 |
| Lower edge | 4.97 | 3.50 | 2.19 | 1.15 | 0.37 | −0.12 | −0.46 | **−0.52** | −0.48 | −0.14 | 0.36 | 1.13 | 2.18 | 3.51 | 5.10 |

- **The wale straddles the load line from x −7 to +7 ft**: its lower edge 0.52 ft under the water at the
  middle (hers 0.20 m), its upper edge 0.17 ft above (measured). Forward it rises into the beak's upper
  lines and runs out with them to the eye (read).

### 5.4 The stem, the stem head and the beak (measured; ±0.03 ft traced, ±0.1 ft by eye)

The stem's fore face traced from the keel (`stem_back`, `stem_fwd`):

| z ft | −6.16 | −6 | −5 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 | +5 | +6 | +7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| x ft | **20.54** (the forefoot) | 20.87 | 22.73 | 24.22 | 25.46 | 26.51 | 27.45 | **28.31** | 28.98 | 29.74 | 30.46 | 31.20 | 32.00 | 32.98 | 34.72 |
| hers x, z (m) | 6.71, −2.32 | 6.82, −2.26 | 7.43, −1.88 | 7.91, −1.51 | 8.32, −1.13 | 8.66, −0.75 | 8.97, −0.38 | 9.25, 0.00 | 9.47, 0.34 | 9.72, 0.69 | 9.95, 1.03 | 10.19, 1.37 | 10.45, 1.71 | 10.77, 2.06 | 11.34, 2.40 |

- **The forefoot**: the stem's fore face leaves the keel's lower edge at (20.54, −6.16) (±0.2 ft along).
- **The stem head**: a tall timber standing above the rails, its fore face from (32.35, 8.83) to its
  rounded top at **(32.40, 13.82)** (hers (10.58, 4.74)), a notch on its after side at (31.63, 12.39)
  (read; by eye).
- **The beak**: above z +6 ft the stem's fore face sweeps forward into the beak's lower edge, which runs
  out nearly level (7.4 to 8.1 ft, rising 0.7 ft over 7 ft) to an eye at **(43.97, 8.30)** (hers (14.36,
  2.85)); over it the beak's top line, 8.72 ft at x 33.97 and 8.57 at 42.94, and inside it a laid spar
  ending in a point at (43.16, 8.34) (hers (14.10, 2.86)), the berthelot (*judgement*, Forfait p. 125's
  word). Depth of the beak 0.75 ft at the stem head, 0.46 ft at the eye: its lower edge rises and its
  top falls, **its middle line level at 8.35 ft** above the water from x 34 to 43 (measured): no steeve.
- **Its length** (computed): the eye 11.62 ft beyond the stem head's fore face (0.186 of the length
  between the perpendiculars), the berthelot's point 10.81 ft (0.173); 11.05 ft beyond the fore
  perpendicular at its height. **Hers, ×F_L: 3.79 and 3.53 m beyond the stem head.** Forfait's *Humble*,
  10½ pieds (3.41 m) or by its printed ratio 9½ (3.09 m) (§1.3). Chapman's LXII No. 16 draws hers 6.7 ft
  beyond the stem head on a hull of 43.7 ft (0.153) (§7).
- **Ruled (the lead, 2026-11-20, ruling 3): the beak is 10½ pieds (3.41 m)**, Forfait's printed length,
  the printed ratio 0.151 taken as the misprint (JUDGEMENT). The cross-check: Forfait's leaf n179
  prints both figures (§1.3), and Chapman's beak, scaled, is 3.53 m to the berthelot's point (3.79 m to
  the eye).
- **The head's carving**: none drawn but the eye (read); Falconer's CAGOUILLE stays in words.

### 5.5 The stern (measured)

| Point | Chapman's (ft) | Hers (m) | How |
|---|---|---|---|
| The post's after face at the load line | (−28.27, 0.00) | (−9.23, 0.00) | fitted straight, rms 0.23 px, **raked 8.37° from the square of the keel** (8.66° from the square of H) |
| The post's heel (its after face on the keel's lower edge) | (−27.29, −6.46) | (−8.91, −2.43) | computed on the fit |
| The post's fore face on the keel's lower edge | (−26.43, −6.45) | (−8.63, −2.43) | fitted, rms 0.23 px; the post 0.86 ft thick at its heel, 0.72 ft at the load line |
| The taffrail's top (the post's after face at the after perpendicular) | **(−29.75, 9.72)** | (−9.72, 3.30) | by eye ±2 px |
| The post's after face at z −3.53, +2.42, +5.40, +8.38 | x −27.74, −28.64, −29.10, −29.55 | −9.06, −9.36, −9.51, −9.65 | on the fit |

- **No transom, no counter, no rudder drawn** (read). In the half-breadth plan the lines close on the
  post: the rail's half-breadth falls from about 4.4 ft at aft 8 to near nothing at the taffrail (read;
  measured at aft 8). A sharp stern with flaring topsides (*judgement*).

### 5.6 The profile's area under the line (measured, computed)

The polygon of the post's after face from the line to its heel, the keel's lower edge to the forefoot
and the stem's fore face up to the line: **332.8 ft², 29.34 m² at Chapman's size, 40.9 m² in hers**
(no rudder; the keel's lower edge the deepest line). It fills 0.93 of the waterline times the mean
draught, as the other drawn hulls do (0.93 to 0.99, `pages-diana.md` §5.6); the generator's rule (0.85 ×
18.47 × 2.38) would give 37.4 m² (computed). **Reckoned to H** (ruling 1's condition), and **accepted
as measured** (the lead, 2026-11-20, ruling 4): 40.9 m².

### 5.7 The ports (measured)

Four a side, each a closed lid drawn as a parallelogram (upright sides, top and bottom along the sheer)
with two strap hinges whose eyes stand outside its edge: **aft of the lid on ports 1 and 2, forward of it
on ports 3 and 4** (read). Edges found by row and column scans, ±1 px.

| Port | x (centre) ft | Sill z ft | hb at the sill ft | Above the deck ft | Rail above the sill ft | Hers: x, sill, hb (m) |
|---|---|---|---|---|---|---|
| 1 | −14.26 | 3.90 | 7.68 | 1.18 | 2.00 | −4.66, 1.37, 2.89 |
| 2 | −5.92 | 3.05 | 8.34 | 1.25 | 1.82 | −1.94, 1.11, 3.14 |
| 3 | +9.82 | 3.30 | 8.02 | 1.14 | 2.21 | 3.21, 1.18, 3.02 |
| 4 | +18.16 | 4.51 | 6.35 | 1.12 | 2.53 | 5.93, 1.57, 2.39 |

- **Size: 1.61 by 1.45 ft** (53.8 ± 0.9 px by 48.4 ± 0.3), 0.48 by 0.43 m at Chapman's size; **hers 0.52
  by 0.54 m** (width ×F_L, depth ×F_B; or 0.61 by 0.54 m on F_B alone, JUDGEMENT for the builder).
- Spacing 8.33, 15.74, 8.34 ft: two pairs, the waist between them clear (computed). The ports are cut in
  the waist bulwark, their sills 1.1 to 1.25 ft above the deck at side (measured).
- **The half-breadths at the sills** are the traced frames' at the sill's height, interpolated along the
  length (±0.1 ft; port 4's ±0.3 ft, between fore 6 and fore 9 with fore 7 and 8 not traced).
- **The swivels**: none drawn (read).
- **Accepted** (the lead, 2026-11-20, ruling 7): the war tartane's four ports a side, as measured,
  written into the design's §7.

## 6. For the profile: the points in metres (hers)

### 6.1 Their marks and their frame

Every point is in the file's frame, built on H (§4.1), scaled by §3.4. Rung S† (`stand-in`), Chapman's
plate of her type. **Measured** where traced by a script (±0.03 ft, 1 cm in hers) or read by eye (±0.1
ft, 3 cm); the identifications marked *judgement* in §5. The body plan's frames traced (`follow.py`
from one row, up and down, drawn back on the image): aft 3 to 8 and ⊕ (the after half's outermost), fore
1 to 6 and 9; the frame first started at fore 4's place in the row was not traced, and fore 7 and 8 were
not reached. **Not traced, so not given as sections**: aft 1 and 2, fore 7, 8 and 10.

### 6.2 The lines

```
rail_m (the top of the side; the step at x -7.06 given as two points 1 cm apart):
  [-9.72, 3.30], [-9.15, 3.04], [-8.49, 2.76], [-7.84, 2.51], [-7.19, 2.28], [-7.07, 2.24],
  [-7.06, 2.61], [-6.53, 2.46], [-5.88, 2.32], [-5.23, 2.18], [-4.57, 2.06], [-3.92, 1.96],
  [-3.27, 1.88], [-2.61, 1.82], [-1.96, 1.78], [-1.31, 1.75], [-0.65, 1.73], [0.00, 1.71],
  [0.65, 1.74], [1.31, 1.78], [1.96, 1.83], [2.61, 1.90], [3.27, 1.98], [3.92, 2.07], [4.57, 2.18],
  [5.23, 2.30], [5.88, 2.43], [6.53, 2.58], [7.19, 2.49], [7.84, 2.54], [8.49, 2.72], [9.15, 2.98],
  [9.80, 3.33], [10.13, 3.53], [10.38, 3.67]
breadth_m (x, hb at the water, hb at the rail; brackets interpolated; hb at the water on H, carried
  down from the plan's load waterline on H′ by the sections' flare, computed 2026-11-20: §4.3):
  [-8.02, 0.86, 1.62], [-7.04, 1.57, 2.26], [-6.06, 2.16, 2.62], [-5.10, 2.58, 2.81],
  [-4.13, 2.88, 2.92], [-3.16, 3.08, 2.97], [-2.19, 3.20, (3.00)], [-1.21, 3.26, (3.02)],
  [-0.23, 3.27, 3.04], [0.73, 3.26, 3.02], [1.70, 3.21, 2.99], [2.67, 3.10, 2.94], [3.64, 2.90, 2.88],
  [4.62, 2.57, 2.77], [5.59, 2.14, 2.63], [6.56, 1.56, (2.3)], [7.53, 0.94, (1.85)], [8.50, 0.40, 1.29]
decks_m.upper (the dashed line; it ends at x 7.19):
  [-9.15, 1.77], [-8.49, 1.62], [-7.84, 1.49], [-7.19, 1.37], [-6.53, 1.25], [-5.88, 1.14],
  [-5.23, 1.03], [-4.57, 0.95], [-3.92, 0.86], [-3.27, 0.79], [-2.61, 0.73], [-1.96, 0.66],
  [-1.31, 0.60], [-0.65, 0.55], [0.00, 0.53], [0.65, 0.54], [1.31, 0.59], [1.96, 0.66], [2.61, 0.71],
  [3.27, 0.78], [3.92, 0.85], [4.57, 0.95], [5.23, 1.05], [5.88, 1.17], [6.53, 1.30], [7.19, 1.45]
ports_m.upper (x, sill, hb at the sill): [-4.66, 1.37, 2.89], [-1.94, 1.11, 3.14], [3.21, 1.18, 3.02],
  [5.93, 1.57, 2.39]
port_size_m.upper: [0.52, 0.54]
keel_m (the keel's lower edge): [-8.91, -2.43], [0.00, -2.38], [6.71, -2.32]
rabbet_m (the base line, the keel's upper edge; half-siding not measured): z -2.20 at x -8.8,
  -2.14 at 0, -2.08 at +6.5
stem_m (the forefoot, the stem's fore face, the stem head):
  [6.71, -2.32], [6.82, -2.26], [7.43, -1.88], [7.91, -1.51], [8.32, -1.13], [8.66, -0.75],
  [8.97, -0.38], [9.25, 0.00], [9.47, 0.34], [9.72, 0.69], [9.95, 1.03], [10.19, 1.37], [10.45, 1.71],
  [10.57, 3.03], [10.58, 4.74]
head_m (the knee's and the beak's lower edge, from where it leaves the stem to the eye):
  [10.77, 2.06], [11.34, 2.40], [11.82, 2.54], [12.28, 2.63], [12.75, 2.68], [13.22, 2.72],
  [13.68, 2.75], [14.15, 2.79], [14.36, 2.85]
the beak's top line (no key): [11.10, 2.99], [14.03, 2.94]; the berthelot's point (14.10, 2.86)
stern_m (the post's after face, the heel to the taffrail):
  [-8.91, -2.43], [-9.06, -1.33], [-9.21, -0.21], [-9.23, 0.00], [-9.36, 0.82], [-9.51, 1.84],
  [-9.65, 2.85], [-9.72, 3.30]
wales_m (x, lower edge, upper edge):
  [-8.49, 1.70, 1.86], [-7.84, 1.44, 1.60], [-7.19, 1.20, 1.36], [-6.53, 0.97, 1.14],
  [-5.88, 0.76, 0.93], [-5.23, 0.58, 0.74], [-4.57, 0.41, 0.57], [-3.92, 0.26, 0.42],
  [-3.27, 0.13, 0.30], [-2.61, 0.04, 0.21], [-1.96, -0.05, 0.13], [-1.31, -0.11, 0.11],
  [-0.65, -0.17, 0.09], [0.00, -0.20, 0.06], [0.65, -0.18, 0.04], [1.31, -0.14, 0.03],
  [1.96, -0.05, 0.11], [2.61, 0.04, 0.20], [3.27, 0.13, 0.29], [3.92, 0.25, 0.42], [4.57, 0.40, 0.56],
  [5.23, 0.56, 0.72], [5.88, 0.76, 0.92], [6.53, 0.97, 1.14], [7.19, 1.20, 1.37], [7.84, 1.47, 1.63],
  [8.49, 1.75, 1.91]
planksheer band (no key; x, lower edge, upper edge):
  [-8.49, 2.22, 2.39], [-6.53, 1.51, 1.68], [-4.57, 0.96, 1.13], [-2.61, 0.61, 0.78], [0.00, 0.39, 0.57],
  [2.61, 0.61, 0.77], [4.57, 0.94, 1.10], [6.53, 1.49, 1.65], [8.49, 2.25, 2.41], [9.80, 2.86, 3.01],
  [10.62, 3.38, 3.42]
section_m (the midship frame, at x -0.23; z, hb):
  [-2.07, 1.09], [-1.88, 2.05], [-1.69, 2.42], [-1.51, 2.64], [-1.32, 2.81], [-1.13, 2.93],
  [-0.94, 3.02], [-0.75, 3.09], [-0.56, 3.15], [-0.38, 3.19], [-0.19, 3.23], [0.00, 3.26],
  [0.19, 3.27], [0.38, 3.29], [0.56, 3.30], [0.75, 3.30], [0.94, 3.25], [1.13, 3.19], [1.31, 3.12],
  [1.50, 3.06], [1.69, 3.03], [1.71, 3.04]
  (traced from 0.13 ft above the base line; the base line at z -2.14)
form.stern: round (no transom; the planking closes on the post) (JUDGEMENT on the schema's word)
form.head: knee (a plain beak to an eye, no carving drawn) (JUDGEMENT)
hull (for the hull block, not the profile; rulings 1, 2 and 4, every figure on H):
  draught_m 2.38 (the mean to the keel's lower edge; 2.43 at the post, 2.32 at the stem; on H' 2.40)
  length_waterline_m 18.47 (the post's after face to the stem's fore face on H)
  lateral_area_m2 40.9 (the post's after face, the keel's lower edge, the stem's fore face; no rudder)
  deck_height_m 0.54 (the deck at side at the midship station; ruling 2; the bulwark's top 1.72, no key)
  (displacement about 135 t drawn to H, KM 3.15 on H: §4.3; accepted, ruling 4)
```

### 6.3 The sections (`sections_m`; x, z, hb in hers)

Each traced frame at whole feet of Chapman's z, from the base line to the rail (§6.1); hers:

```
aft 8 (x -8.02):  [-0.19, 0.93], [0.17, 0.97], [0.51, 1.10], [0.86, 1.25], [1.20, 1.36], [1.54, 1.45],
                  [1.88, 1.52], [2.22, 1.58], [2.58, 1.62]   (traced from z -0.48 up)
aft 7 (x -7.04):  [0.17, 1.66], [0.52, 1.81], [0.86, 1.94], [1.21, 2.05], [1.55, 2.13], [1.89, 2.20],
                  [2.24, 2.24], [2.38, 2.26]   (traced from z 0.08 up)
aft 6 (x -6.06):  [-2.07, 0.25], [-1.69, 0.69], [-1.32, 1.11], [-0.94, 1.48], [-0.56, 1.79], [-0.19, 2.03],
                  [0.17, 2.21], [0.52, 2.34], [0.87, 2.44], [1.22, 2.50], [1.56, 2.56], [1.91, 2.59],
                  [2.26, 2.62], [2.37, 2.62]
aft 5 (x -5.10):  [-2.07, 0.38], [-1.69, 1.05], [-1.32, 1.57], [-0.94, 1.97], [-0.56, 2.26], [-0.19, 2.46],
                  [0.18, 2.61], [0.53, 2.71], [0.88, 2.78], [1.23, 2.82], [1.58, 2.82], [1.93, 2.82],
                  [2.16, 2.81]
aft 4 (x -4.13):  [-2.07, 0.51], [-1.69, 1.47], [-1.32, 2.06], [-0.94, 2.40], [-0.56, 2.64], [-0.19, 2.82],
                  [0.18, 2.92], [0.53, 2.98], [0.89, 3.01], [1.24, 2.99], [1.59, 2.95], [1.95, 2.91],
                  [1.99, 2.91]
aft 3 (x -3.16):  [-2.07, 0.71], [-1.69, 1.86], [-1.32, 2.38], [-0.94, 2.68], [-0.56, 2.87], [-0.19, 3.00],
                  [0.18, 3.08], [0.54, 3.13], [0.90, 3.15], [1.25, 3.07], [1.61, 2.99], [1.88, 2.97]
fore 1 (x 0.73):  [-2.07, 1.31], [-1.69, 2.33], [-1.32, 2.73], [-0.94, 2.95], [-0.56, 3.09], [-0.19, 3.18],
                  [0.19, 3.24], [0.56, 3.27], [0.94, 3.24], [1.31, 3.10], [1.68, 3.02], [1.75, 3.02]
fore 2 (x 1.70):  [-2.07, 1.02], [-1.69, 2.20], [-1.32, 2.62], [-0.94, 2.87], [-0.56, 3.02], [-0.19, 3.12],
                  [0.18, 3.19], [0.55, 3.22], [0.92, 3.19], [1.28, 3.06], [1.65, 2.99], [1.83, 2.99]
fore 3 (x 2.67):  [-2.07, 0.73], [-1.69, 1.93], [-1.32, 2.41], [-0.94, 2.68], [-0.56, 2.87], [-0.19, 3.00],
                  [0.18, 3.09], [0.54, 3.14], [0.90, 3.12], [1.26, 3.03], [1.63, 2.96], [1.90, 2.94]
fore 4 (x 3.64):  [-2.07, 0.53], [-1.69, 1.57], [-1.32, 2.09], [-0.94, 2.41], [-0.56, 2.64], [-0.19, 2.80],
                  [0.18, 2.92], [0.54, 3.00], [0.89, 3.02], [1.25, 2.97], [1.61, 2.90], [1.96, 2.88],
                  [2.05, 2.88]
fore 5 (x 4.62):  [-2.07, 0.34], [-1.69, 1.14], [-1.32, 1.66], [-0.94, 2.03], [-0.56, 2.29], [-0.19, 2.48],
                  [0.18, 2.63], [0.53, 2.74], [0.88, 2.81], [1.23, 2.81], [1.58, 2.77], [1.94, 2.76],
                  [2.19, 2.77]
fore 6 (x 5.59):  [0.52, 2.37], [0.87, 2.49], [1.22, 2.56], [1.57, 2.58], [1.92, 2.59], [2.26, 2.62],
                  [2.37, 2.63]   (traced from z 0.33 up)
fore 9 (x 8.50):  [0.51, 0.53], [0.86, 0.69], [1.20, 0.84], [1.54, 0.96], [1.89, 1.08], [2.23, 1.19],
                  [2.57, 1.27], [2.71, 1.29]   (traced from z 0.31 up)
```

- **Her midship section**: the greatest half-breadth 3.30 m at 0.56 to 0.75 m above the water (her 6.61
  m), 3.27 m at the water, 3.04 m at the rail: **0.26 m of tumblehome** from the greatest breadth to the
  rail (measured). Coefficient 0.83 to the base line (§4.3).
- Chapman's own feet for every section are in `tables.py`'s print (§10), for the builder's module.

### 6.4 The heights above the deck (the design's §4)

At Forfait's places (Table II: the main 10 pi 5 po before the middle, the mizen 15 pi 2 po abaft it),
taken from the middle of her perpendiculars, which stands at x +0.49 m in hers (computed):

| | x (hers) | Deck at side | The keel's upper edge | The keel's lower edge | Deck to the keel's upper edge |
|---|---|---|---|---|---|
| The main | **+3.87 m** | **0.85 m** | −2.12 m | −2.36 m | **2.97 m** |
| The mizen | **−4.44 m** | **0.93 m** | −2.17 m | −2.40 m | **3.10 m** |

- **The main's heel** on the keel's upper edge: the masthead (59 pieds, 19.17 m, raked 3°) 16.17 m above
  the deck, the hounds (the head's foot, 33 pieds up) 7.73 m; on a keelson of 0.25 m (JUDGEMENT; none is
  drawn), 16.42 and 7.98 m. The design's "head about 16.4 m, hounds about 8 m" and "stepped about 2.8 m
  below the deck" stand within 0.2 m (computed).
- These are heights over the deck at side; over the deck's middle line a camber would lower them (none
  is drawn; JUDGEMENT).

## 7. Pl. LXII No. 16, her rig (measured, on the 6,000-px photograph)

- **The scale**: the diagonal bar's S row gives **8.09 px a Swedish foot** (seven tens, 566.6 px from 10 to
  80); E 8.30 and F 8.85 px a foot, S/E 0.975 and S/F 0.915 (measured; ±0.3%). One pixel is 3.7 cm: the
  rig plate is four times coarser than Pl. LVII.
- **The horizontal**: the water band's top line under No. 16, fitted at 0.01946 of the rows (rms 0.61 px);
  every angle below is taken to it.
- **The hull** drawn under the rig: 354 px from the taffrail to the stem head, **43.7 ft (12.99 m)**, not
  the 62¼-ft vessel of Pl. LVII: Chapman's rig of the type, not of No. 16 (*judgement*). No breadth marks
  are drawn for it (Chapman marks the breadth on No. 1 only, by his caption).

| What | Measured | As a proportion | Against Forfait's *Humble* (Table II) and the design |
|---|---|---|---|
| **The main mast's place** | at the deck, x 2,234.5 px | **0.499 of the length from the taffrail: at the middle** (±0.01) | Forfait 0.167 of the length before the middle (her x +3.87 m); Chapman's in hers at x +0.49 m |
| **The main's rake** | its after edge upright on the image (dx/dy −0.0009, rms 0.09 px over 160 px); its fore edge −0.0082 | **upright: 0.6° to 1.1° aft of the square of the water, ±0.5°** | the design's 3° forward (the owner's pick of question 3) |
| The main above the deck | 27.6 ft (223 px) | 0.63 of the hull's length | — |
| The main yard | 52.4 ft (419 px), slung 0.45 of its length from the car, peaked about 55° | **1.20 of the hull's length** | Forfait 1.195 of the length |
| **A fore mast** | at the deck 0.842 of the length from the taffrail | **0.34 of the length before the middle; raked 23° forward** (a stout spar, 22.2 ft from the deck to its head) | none in Forfait's *Humble* or the owner's rig |
| The fore yard | 40.3 ft, slung 0.39 from the car, peaked about 62° | 0.92 of the hull's length, 0.77 of the main yard | — |
| **A mizen** | none | — | Forfait's *tapecul* 0.242 abaft the middle; the design's 10° aft (JUDGEMENT on Forfait p. 128) |
| A square topsail | none | — | Forfait's *Humble* and the owner's rig carry one |
| A headsail | none drawn | — | one great jib (the design, the owner's reading of the prints) |
| The beak | the eye 6.7 ft beyond the stem head | 0.153 of the hull's length | Forfait's printed ratio 0.151; Pl. LVII 0.186 |
| A short spar over the stern | from the rudder head forward, 7 ft | — | a tiller (*judgement*) |

- **Read so, Chapman's tartane of Pl. LXII is Röding's two-masted tartane under two lateens**, the fore
  mast raked well forward, and not the owner's rig (main, topsail, mizen). It answers the design's
  question of the main's rake (upright) and of the masts' places only for that rig. **The mizen's rake
  cannot be read on Chapman**: neither plate draws a mizen; the design's 10° aft stays JUDGEMENT on
  Forfait p. 128 (§8).
- Angles ±1° (the yards' ends by eye, ±3 px); places ±0.01 of the length.
- **Ruled (the lead, 2026-11-20, rulings 6 and 7).** Her main's rake is the owner's answer, **3°
  forward**, kept in the design as the owner's; Chapman's upright (0.6° to 1.1° aft, ±0.5°) is recorded
  beside it, and the owner has been asked whether to revisit it. Pl. LXII's tartane is written into the
  design as two-masted, with no topsail, no mizen and no headsail; the mizen's rake stays JUDGEMENT.

## 8. Against the design (written into it 2026-11-20, old beside new, with the lead's rulings)

**The cause the *Diana*'s measuring found, looked for here: found.** Her load line is drawn inclined to
the keel, and the design took Chapman's stated 6⅔ ft as a level draught (2.50 m on her breadth). The
stated figure fits the after draught (§4.2), as Pl. LIX's did. **Mended at the cause**: the file's
draught is the mean on the drawn line, 2.38 m, with its drag recorded (2.43 / 2.32 m). Looked for
elsewhere:
- in the design's displacement and GM, which rested on the same draught (§4.3);
- in her heights above the deck (§6.4), which rested on no drawn deck (now measured);
- in the xebec's design, whose `draught_m` (3.0 m, JUDGEMENT) cites Chapman's 9⅔ ft of Pl. LVIII No.
  17: that figure is likely an after draught too, to be measured on Pl. LVIII at the xebec's step 1 (not
  measured here). Ruled so (the lead, 2026-11-20, ruling 7), and written as one line in the xebec's
  design where it cites the figure.

**A second cause: a length between the perpendiculars taken for a waterline.** The design's factor read
"lengths 19.0 ÷ Chapman's waterline (about 18.5 m, to read)"; 18.5 m is Chapman's length between the
perpendiculars. His waterline is 16.79 m, the stem raking 4.6 ft forward of it above the water and the
post 1.5 ft aft. Her waterline is therefore 18.47 m on her 20.38 m, not 19.0, and her hull speed 10.4
knots, not 10.6. Looked for elsewhere: the design's §16.1 sketch ("a third longer on the water" than
the cutter's 15.2 m) becomes "a fifth longer"; the research note's §2.2 ratio of 3.54 is on the length
between the perpendiculars and is right as written. **Accepted as measured** (the lead, 2026-11-20,
ruling 4), with the figures that follow.

**A third cause: the plate's number.** "Pl. LVIII No. 16" stood in the design (six times, in five
lines), the research note (seven), the plan (§1.1, §1.2, §8.1) and `VesselReferences-2026-10.md` §3.1;
the same note's "Chapman plate LVIII No. 15, a Bermuda sloop" (its §3.9) is the same fault (No. 15 is
on Pl. LVII). The xebec's "Pl. LVIII No. 17" is right. The 1971 reprint's table, read through the
browser in an earlier round, is the likely source (memory, unverified); the engraved number and the
museum's record agree on LVII (read). **Corrected 2026-11-20** in all of them (the lead's ruling 5),
with a dated line in `VesselReferences-2026-10.md` §3.1; the xebec's left as it is.

**Changed by measurement, each with its reason (the design has them old beside new, 2026-11-20):**
- her lines: rung S† (`stand-in`) now, from T;
- the factors: lengths 1.100, sections 1.268, heights above the water by principle 7's split;
- the waterline 18.47 m; the draught 2.38 m mean; the displacement about 135 t; KM 3.15 m on H;
- the deck at side 0.54 m at midships, not about 0.9 m: `deck_height_m` (ruling 2);
- the drawing's description: a waist bulwark, no raised after deck, a sharp stern, a tall stem head;
- the ports' places and size;
- the beak: 3.53 to 3.79 m on Chapman's plate in hers, against Forfait's 3.41 (10½) or 3.09 (9½);
  the page of Forfait prints both 10½ and 0.151 (read); ruled 10½ pieds, 3.41 m (ruling 3, JUDGEMENT);
- the main's rake: Chapman's rig upright, recorded; the owner's 3° forward kept, and the owner asked
  whether to revisit it (ruling 6);
- the mizen's rake: no plate gives it; it stays JUDGEMENT (ruling 7).

## 9. What the sources cannot give

- **Which line is her load line**: H as drawn, or H′, the line her body is built to (§4.1). **Ruled H**
  (the lead, 2026-11-20, ruling 1), H′ recorded; the plan's load waterline, on H′, stands in for H's
  waterplane (§4.3).
- **The deck forward of x +22 ft** (hers +7.19 m) and **at the middle line**: not drawn (camber unknown).
- **The rudder**: not drawn on No. 16 (read); her rudder is the builder's by the generator's rule.
- **The masts on her own hull**: Pl. LVII draws none; Pl. LXII is another vessel and another rig (§7).
  A box at the fore end of the midship hatch in the half-breadth plan, at about x +1.9 ft, may be the
  main's partners (unverified; *judgement*, not used).
- **The frames aft 1, aft 2, fore 7, fore 8 and fore 10**, and the lower parts of aft 7, aft 8, fore 6
  and fore 9: not traced (crowded by the diagonals and the waterlines); the plan's load waterline gives
  their half-breadth at the water.
- **Whether the lines are moulded or outside the plank**: the dashed sides of the body plan carry the
  moulded breadth (read there, "breadth moulded"); the plank is not drawn.
- **Forfait's figs. 9 and 35**: not reached; the Internet Archive item's last leaves hold no plate
  (fetched n398 to n404). Lescallier's Pl. XXII fig. 5 and Röding's Fig. 289 were not sought in this
  step.
- **The second photographs** (4,000 px) were fetched and not measured.

## 10. Method and files

Everything is in the session's scratch, `scratchpad/p90/tartane/step1/`; nothing is in the repository.
The images are in `D:/Projects/FreeSail/reference-cache/tartane/` (§1.1, §1.3). Run with `py -I`, paths as
arguments, nothing run from the download folders. `npy/` holds the two plates' grey channels; `tr/` the
traces (JSON); `crops/` the crops and overlays looked at (`ov_*.png`).

- `scan_dimu.py` (the records' manifests), `mknpy.py`, `thumb.py`, `gc.py`, `gcs.py` (crops with a
  grid), `ov.py` (traces drawn back on the image);
- `ticks.py`, `vticks.py`, `bar.py`, `srow.py` (the scale bars), `col.py`, `row.py` (dark minima down
  columns and along rows, to a tenth of a pixel), `fitline.py` (straight lines with outliers dropped),
  `htrace.py`, `follow.py` (line followers);
- `common.py` (the sheet's model: the scale, the fitted lines, the frame, `to_ft`; the body plan's centre
  and base), `stations.py` (the stations' lines), `model.py` (her factors, the deck line, k(x));
- `final.py` (the sheer lines), `tables.py` (the stations, the frames' heads and sections), `ports.py`,
  `block.py` (§6.2's points), `disp.py` (§4.3).

The followers went wrong where lines crowd (the wale forward of x −7 ft, where they ran onto the load
line; the body plan's inner frames; the plan's lines at the stern); every trace used here was drawn back
on the image and looked at, and the wrong parts were replaced by column readings (the wale, the deck) or
left out (the frames named in §9).

**Finished 2026-11-20 (the rulings).** No image was measured again. The waterplane carried from H′ to
H (§4.3) is arithmetic on §6.2's half-breadths and §6.3's sections, in the session's scratch
(`scratchpad/p90/tartane/docs-check/bm_h.py`).
