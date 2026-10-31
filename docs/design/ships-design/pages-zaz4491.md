# Pages: RMG ZAZ4491 and ZAZ4492, the brigs of the *Diligence* class, 1795 (October 2026)

Package 75's hull step, SW-2 with SW-2b.2 (`Build-Ships.md` §5, §5.4, §5.7, §5.9, §5.0 principle
10). It serves `data/ships/brig.yaml` and `data/ships/merchant-brig.yaml`, one hull in two roles,
and replaces the *Raven* stand-in of that §5.7 with her class's own lines. Facts only: the images
are the museum's photographs of Crown copyright sheets, read and cited and kept outside the
repository (§1.1). Winfield's figures are cited by page. Nothing in this note moves a figure the
physics or the gunnery reads (`Build-Ships.md` §5.0 principle 8, §5.6).

The marks:

- **read**: the sheet's writing or drawing was seen on the image.
- **catalogue**: from the museum's catalogue entry, as Commons gives it.
- **measured**: off the image at the scale of §3; the uncertainty is stated.
- **memory, unverified**: not checked during this measuring (none below).
- **judgement**: reasoning by this note.

**Units and datums.** English feet and inches, with metres in brackets. Stations are the sheet's own
letters and numbers. Positions along the ship are feet forward of **AP**, the after of the two
perpendiculars on the sheer plan, at the scale strip's mark 95 (§3.1), measured square to the keel
as the sheet's station lines stand; **FP** is the other, 95 ft forward. In metres they are from the
**mid-perpendiculars**, 47.50 ft forward of AP, positive forward, as the profile's `x`. Heights are
above **WL1** (§4), the top green waterline, at each station, along the sheet's station lines,
positive up, as the profile's `z`. WL1 slopes 1.81° to the page and 1.88° to the keel, so a point 11
ft from WL1 stands 0.35 ft (0.11 m) from where a level water would put it along the ship; ignored,
as the 64's module ignores it (judgement). Half-breadths are **moulded** in the tables of §5 (inside
the plank); the points of §6 carry 3 in of plank, the difference between the breadths moulded and
extreme (§2.2).

## 0. In brief

- **Scale checks.** ZAZ4491's strip gives 100.11 px to the foot; its body-plan box comes to 27 ft
  6.0 in against 27 ft 6 in moulded; the strip's marks 95 are the sheet's perpendiculars, 95 by
  count; the rabbets at the deck stand about 95 ft 4 in apart against 95 ft 0 in (§3.1). ZAZ4492's
  gives 100.89; the depth in hold comes to 11 ft 11 in against 12 ft 0 in, a weak check (§3.2).
- **The two sheets agree**, station by station, to 0.1 ft amidships and 0.2 ft at the ends (§3.3).
  *Diligence*'s ZAZ4320 and *Hound*'s ZAZ4262 have the same waterlines and half-breadths to 0.05 ft;
  their deck, sheer and ports stand 0.2 to 0.4 ft lower, with ticked lines over them that ZAZ4491
  draws solid (§3.4). ZAZ4491 is the class's final form (judgement).
- **The load line is WL1** (judgement, §4.2): the top green line, the only green one drawn through
  the rudder and to the knee's fore edge on all three sheets; the lowest sill stands 5 ft 2 in above
  it, near Steel's four to five feet. No line is labelled. To K it draws 9.69 ft forward and 12.80
  ft aft at the perpendiculars, 11.25 ft at the middle. **A faint ruled grey line lies just above
  it** on ZAZ4491 alone, 0.14 to 0.30 ft higher, with a short bar on the forward perpendicular 10.00
  ft above K (measured, tentative; §4.1): **the lead ruled WL1, the faint line recorded** (2026-10-31;
  §4.2).
- **Her drag is 3.11 ft in the 95 ft (read from the waterlines; 3.2 ft on the sisters), against
  Winfield's 3 ft 7 in for *Harpy***. Winfield's 7 ft 3 in / 10 ft 10 in falls near **WL2** (WL2
  2.39 ft below WL1; Winfield's mean 2.2 ft), not on WL1 (§4.3). The file's 11.5 ft mean is 0.25 ft
  deeper than WL1's 11.25 to K: recorded, not moved.
- **Ten ports a side** (read; the description's "sixteen ports a side" is wrong), 2 ft 9 in by 2 ft
  4 in, 8 ft 5 in apart. Sills 5.15 to 6.53 ft (1.57 to 1.99 m) above WL1 against the file's 2.1 m,
  1 ft 4 in above the deck at side at every port (§5.7). The eight sweep ports stand between ports 1
  and 9. The file's triples stand at the guns' x, which never move, within 0.12 m of the sheet's
  centres and 0.43 m at the chase gun (§6.2).
- **The deck**: 4.51 ft (1.38 m) above WL1 at its lowest at the middle line, 3.79 ft (1.16 m) at
  side, against the file's 1.5 m (§5.3). The rail: 8.35 ft (2.55 m) at its lowest, 11.93 ft at the
  stem and 12.07 ft at the taffrail (§5.2).
- **The body is a sharp man-of-war's:** a floor rising about 25° from the rabbet, dead flat 12 to 14
  ft above the rabbet at ⊗, 4 in of tumblehome at the rail amidships, flaring forward of M (§5.10,
  §5.11).
- **Square stern, plain:** a tuck with a wing transom, a counter, a raked transom, flat in the rake
  and rounded in plan, with two stern ports, no galleries and no lights; a **scroll head** (§5.5,
  §5.6).
- **Masts** on the sheet at -3.96 m and +9.62 m; in green, *Harpy*'s change of 1799, -4.07 m and
  +9.37 m; the file's -3.9 m and +8.9 m (§5.9). Not moved.
- **Length and displacement.** WL1 is 91.9 ft moulded, 95.2 ft outside the post and the knee,
  against the file's 88 ft. Drawn to WL1 she displaces about 303 t against the file's 413 t, 27%
  under: recorded, never moved (§7).
- **The points of §6 pass** the tree's `g.hull_profile` and `g.hull_form` as they stand at
  `bb60222`, as `tools/ships/hull_brig.py` writes them, every triple within 0.06 m of the drawn side
  (§6.1). Rung S throughout (`Build-Ships.md` §5.0 principle 3), with the words of §6.2's marks.

## 1. The sources

### 1.1 The objects, the images and the cache

| | ZAZ4491 | ZAZ4492 |
|---|---|---|
| Object | RMG object 84282; "Diligence (1795) ... RMG J4419"; Admiralty Curator Number 3447; stamped *Harpy*; sheet 354 x 1018 mm; 1:48; April 1795 (catalogue) | RMG object 84283; "... RMG J4420"; Curator Number 3448; stamped *Harpy*, Box 50; sheet 543 x 730 mm; 1:48; 1 May 1795; traditional repair (catalogue) |
| Image used | Commons, original, 16,158 x 5,644 px, PNG, 44,505,440 bytes, sha1 `705344e8e3dc90a5dc5160ddb422cfedd453df8f` | Commons, original, 11,684 x 8,626 px, PNG, 59,773,130 bytes, sha1 `a321cccbe164a49cc2806356cb5334ea515db1b2` |
| Cache | `D:/Projects/FreeSail/reference-cache/diligence-j4420/J4419-original.png`, with `J4419-imageinfo.json`, `J4419-wikitext.txt` | `.../diligence-j4420/J4420-original.png`, with `imageinfo.json`, `commons-wikitext.txt` |
| Rights | The museum credits its sheets "© Crown copyright. National Maritime Museum, Greenwich, London" and licenses them through RMG Images, whatever Commons's tag (`Build-Ships.md` §5.9), so each is read and cited, never copied | The same |

The checks, at full size in the same cache, fetched 2026-10-30 with a generic user-agent:
`J4525-original.png` (ZAZ4320, *Diligence*'s own, "Navy Office 17 April 1795", 16,177 x 5,657 px,
sha1 `28fecc7c...`) and `J4574-original.png` (ZAZ4262, *Hound*'s own, "28 April 1795", 16,224 x
5,668 px, sha1 `a46353bb...`). They are checks, not sources of points.

### 1.2 What is on the sheets (read)

**ZAZ4491**, left to right:
- **The body plan** with the stern board over it: aft sections on the left (⊗, 4, 6, 8 ... 22, 23),
  fore sections on the right (⊗, D, F, H, K, M, O, Q, S), in black; the waterlines in green; the
  diagonals in red, solid and dashed; the keel's section under it; a heavy level line at the dead
  flat's height of breadth (§5.11).
- **The sheer plan**, bow to the right: rail, plank-sheer, the band through the ports, wale, height
  of breadth, ten ports, eight sweep ports, channels and chains, the deck's three lines in red, four
  green waterlines, the deadwood and cutting-down in red, the rudder with its braces, the scroll
  head and the bowsprit; two mast stumps with their centres in red.
- **The scale strip**, under the keel, its upper border doubling as K (§5.4).
- **The half-breadth plan**: main breadth, top-timber line, four green waterlines, the cant frames
  in red, the transom's two arcs.
- Station lines from 23 to S through the sheer and the plan. At ⊗ two lines are drawn, at 53.09 and
  53.86 ft, with the label between them (§5.2).
- A faint ruled grey line just above WL1, overshooting the rudder aft, with a short bar on the
  forward perpendicular (§4.1).
- Green: dead-eyes in the fore channel, and a note on them (§2.3); a green hatched band with a thin
  green line at about 57.6 and 58.1 ft, from the rail down to the wale's upper edge (read,
  unexplained).
- A black hatched band with a thin line at about 41.2 and 41.5 ft, over the same height (read,
  unexplained). Neither band stands on ZAZ4492 at those places (the green one checked).

**ZAZ4492**: the inboard profile above its own strip, in red with black and green; the upper deck
and, below it, the lower deck with hold and platform, in plan; ten ports and the sweep ports in the
side; the masts' centres in red, and *Harpy*'s moved centres in green with the note on them (§2.3).
No lines, no waterlines (read).

## 2. The caption and the dimensions

### 2.1 The titles (read)

- **ZAZ4491:** Navy Office, April 1795; a draught for building by contract in the merchants' yards
  three brigs with oak and two with fir, to carry 16 carronades, 32-pounders, by Admiralty order of
  the 22nd instant. **ZAZ4492:** Navy Office, 1 May 1795; a profile draught of the inboard works and
  plans of the brigs building by contract in the merchants' yards.
- The design was approved on 22 April 1795 (Winfield 1793-1817, p. 255), the order the title names.

### 2.2 The dimensions (read, ZAZ4491's table; the same on both sisters)

| | Stated | Measured here | Basis |
|---|---|---|---|
| Length on the range of the deck | 95 ft 0 in | about 95 ft 4 in rabbet to rabbet at the deck | §3.1; the strip's marks 95 are the perpendiculars, 95 by count |
| Keel for tonnage | 75 ft 2½ in | not drawn | a rule's figure: 75 ft 2½ in x 28 x 14 / 94 = 313.6, the table's burthen |
| Breadth extreme | 28 ft 0 in | 27 ft 6 in moulded + 2 x 3 in plank | §3.1; the plank is Steel's *Raven* (1805 p. lix) and the difference of the table's two figures |
| Breadth moulded | 27 ft 6 in | **27 ft 6.0 in** (box); 27 ft 5.6 in (plan at ⊗) | §3.1 |
| Depth in hold | 12 ft 0 in | **11 ft 11.2 in** | ZAZ4492, §3.2 |
| Burthen | 313 59/94 tons | | Winfield p. 255 the same |

*Harpy* as built, Winfield p. 256: 95 ft 0 in, 75 ft 1 5/8 in by 28 ft 1½ in by 12 ft 0½ in, 316
13/94 tons, draught 7 ft 3 in / 10 ft 10 in. The file stands for *Harpy*: its beam, 8.6 m, is her 28
ft 1½ in against the class's 28 ft 0 in extreme, recorded, never moved.

### 2.3 The notes on the sheets (read; paraphrased)

- **ZAZ4491, top left:** the shift of timbers in ticked lines was for the vessels built with fir;
  the dead-eyes in green in the fore channel are as all the brigs were built. Top right: copies
  given to Mr Parsons, Bursledon (*Diligence*), Mr King, Dover (*Harpy*), Mr Hills, Sandwich
  (*Hound*), Messrs Wells (*Sea Gull*) and Randall & Brent (*Curlew*), the last two fir; *Kangaroo*
  in pale ink. So the sheer draught is the class's and *Harpy*'s builder had a copy.
- **ZAZ4492, top right:** copies sent to Messrs Wells and to Randall, Brent & Sons on 9 May 1795,
  another to Mr Parsons on 29 June, Mr King on 2 July and Mr Hills on 24 July 1795: so *Harpy*'s
  builder had the inboard works by July.
- **ZAZ4492, right:** the alteration of the masts' centres in green was made on board *Harpy* in
  January 1799 at Captain Bazely's request to the Board; the report of the following 30 June says
  she sailed much better and was considerably easier in a head sea. The file's masts are not moved
  for it (§5.9).
- **ZAZ4320:** the deck, sheer, ports and so on as shown by ticked lines are to be conformed to.
  **ZAZ4262:** the deck, ports and so on are to be raised agreeably to the ticked lines (§3.4).

## 3. The scale and its checks

### 3.1 ZAZ4491 (measured)

- **The strip:** all 98 of its one-foot ticks (feet -1 to 96), a straight fit of tick against foot
  over 97 ft: **100.111 px to the foot**, rms 1.62 px (0.016 ft), largest residual 5.0 px; by
  twenty-foot lengths 99.97 to 100.24 px/ft. 1 px is 0.12 in.
- **The perpendiculars** are the strip's two marks 95: x 4953.6 and 14464.1 at row 3240. The marks
  and the sheet's verticals are one line, running up through the sheer and on through the plan, so
  their 95 ft is by count of the strip's own ticks and is no check on its scale (read, measured).
  The independent length is the rabbets at the deck: AP is where the fore side of the post's rabbet,
  carried up, meets the deck at side (row 1613 against 1609), and the stem's rabbet meets it at about
  95.35 ft: **about 95 ft 4 in** against the table's 95 ft 0 in. So the length is on the range of
  the deck, as the table says (judgement), within 4 in.
- **Across the page:** the scale's real check. The body plan's box is 2753.5 px wide, 27.50 ft; the
  half-breadth plan's main breadth at ⊗ is 1374.6 px, 13.73 ft, 0.02 ft short of half the moulded
  breadth. The heights are taken at 100.11 px/ft; 99.97 would change 11 ft by 0.015 ft (judgement:
  ignored).
- **The sheet:** at a quarter-inch to the foot, 15.77 px/mm; the image is 1025 x 358 mm against the
  catalogue's 1018 x 354 mm (+0.7%, +1.1%).
- **Skew:** the strip's border and the keel rise 0.0012 to 0.0015 to the right, the station lines
  lean 0.0009 to 0.0021: a turn of about 0.08°. Stations are read along their own lines; every x off
  a station carries the lean (`model.py`).

### 3.2 ZAZ4492 (measured)

- **The strip:** 55 of 98 ticks found clear of the red rulings; ticks 1 and 96 stand 9584.1 px
  apart, **100.886 px/ft**, 0.77% larger than ZAZ4491's; the straight fit gives 100.874, rms 3.65
  px; by lengths 100.66 to 101.39. The sheet is repaired and wavers, so x is read here from its
  station lines, each fitted to its own lean, and heights from its own rabbet line (a cubic through
  1,610 points, rms 2.1 px; its border rises 0.0027 to the right and its stations lean up to 0.008,
  a skew of about 0.2°).
- **The sheet:** 15.89 px/mm; the image is 735 x 543 mm against the catalogue's 730 x 543 mm.
- **The depth in hold** at x 6300: the upper side of the deck beam at the middle line (§5.1) to the
  dashed red line in the hold, 2419.6 less 1215.6 px: **11.93 ft, 11 ft 11.2 in**, against 12 ft 0
  in. The dashed line is taken as the hold's floor (judgement); the keelson's top and the
  cutting-down line give 11.56 and 12.50 ft, so this is a weak check. Steel's *Raven* takes the depth
  so, from the strake next the limbers to the upper side of the beam at the middle (1805 p. lx, OCR
  l. 44366).

### 3.3 The two sheets against each other (measured)

| What | ZAZ4492 less ZAZ4491 |
|---|---|
| The 21 stations, read on ZAZ4492 by its own strip alone | -0.13 to +0.02 ft, mean -0.08 ft |
| The ten ports' centres (stations registered) | -0.02 to +0.04 ft |
| The ports' width; depth | -0.04 to +0.08 ft; -0.07 to +0.05 ft |
| The ports' sills, above each sheet's rabbet line | -0.21 to +0.08 ft, mean -0.05; within 0.08 from port 4 to port 10 |
| The rail | -0.19 to +0.05 ft: within 0.06 from station 2 to K, 0.09 to 0.19 low toward the ends |
| The deck's lines | -0.19 to +0.01 ft: within 0.07 from station 8 to O, 0.09 to 0.19 low toward the ends |
| The masts' centres at the deck | main +0.05 ft, fore +0.02 ft |
| The post's after edge; the stem's fore edge and rabbet, by the strip, at the same heights above each sheet's rabbet line | -0.01 to +0.04 ft; +0.09 to +0.25 ft (the sheet's station S reads +0.03 there, so 0.1 to 0.2 ft of the stem's stays unexplained) |
| The upper deck plan's outline against ZAZ4491's main breadth, at 20, 12, 4, D, H, M | -0.02, -0.04, -0.03, -0.06, -0.07, -0.11 ft |

The ends' lag may be the repaired sheet's own, or its rabbet line's fit toward its ends (judgement).
ZAZ4491 is taken wherever both read; ZAZ4492 alone gives the lower deck, the depth in hold and the
masts' change.

### 3.4 The sisters (measured, at full size; checks only)

- Each sheet's own perpendiculars: ZAZ4320 100.07 px/ft, ZAZ4262 100.33 px/ft, both over 95 ft.
- **Waterlines:** WL2, WL3 and WL4 stand 2.34-2.39, 4.70-4.78 and 7.05-7.18 ft below WL1, within
  0.05 ft of ZAZ4491's. WL1 to K: 12.87 and 9.66 ft on ZAZ4320, 12.83 and 9.65 on ZAZ4262, 12.80 and
  9.69 here; drag 3.21, 3.18, 3.11 ft.
- **Half-breadths** at 4, 12 and F: WL1 to WL4 within 0.05 ft of ZAZ4491's on both (12.79, 11.25,
  8.44, 3.68 and 12.77, 11.23, 8.39, 3.66 at F, against 12.79, 11.29, 8.43, 3.73).
- **The upper works** differ: the sisters' solid rail, plank-sheer line, band and the deck's lines
  stand 0.20 to 0.37 ft lower than ZAZ4491's, and their ticked lines lie within 0.07 ft of ZAZ4491's
  solid ones at the deck and 0.1 ft at the rail; the wale's edges agree within 0.1 ft (0.16 at one
  place). At ZAZ4320's port 6 the solid port is 2.35 by 2.11 ft, sill 5.09 ft above WL1, the ticked
  port 2.75 by 2.39 ft, sill 5.20 ft, against ZAZ4491's 2.76 by 2.31 ft, sill 5.18 ft. So the
  sisters' solid lines are the first form, their ticks the raising their notes order, and ZAZ4491
  draws the raised form solid (judgement).
- **Pencil on ZAZ4320:** levels at 2-ft steps above the rabbet line, "12" at 11.97 ft and "2" at 2.03
  ft, with pencil figures by the stem (read, measured, unexplained). They bear out §5.4's "the body
  plan's base is this line".

### 3.5 The checker (measured)

A second reading by columns, off the tables' stations and not along the traces, with another ink
model (grey, against a 70th-percentile background) and its own fit of WL1 (slope 0.03151, 2156.3 and
2456.1 px at the perpendiculars, against 0.03152, 2156.3, 2456.0). Rms and largest difference, ft:
rail 0.03, 0.12; plank-sheer 0.01, 0.02; each deck line 0.01, 0.02; wale's upper edge 0.01, 0.02;
height of breadth 0.02, 0.08; wale's lower edge 0.02, 0.03; half-breadths WL1 0.03, 0.06; WL2 0.01,
0.03; WL3 0.02, 0.03; WL4 0.01, 0.02; main breadth 0.01, 0.03; top-timber 0.01, 0.05. Over-plots of
the traces on the image were looked at, at every line named here. **So: ±0.05 ft (about half an
inch) along the sheer and on the waterlines' half-breadths between 16 and K, ±0.1 ft at the ends,
±0.15 ft on the body plan where its lines crowd (§5.11).**

## 4. The waterlines and the draught

### 4.1 The lines (measured)

Four green lines, straight and parallel, unlabelled, none named a load line (read), and a fifth
line, faint, ruled and grey, on ZAZ4491 alone. On ZAZ4491:

| Line | Slope to the page | Below WL1 | To the sheer plan's ends, ft from AP | To K: at AP; at FP; at the middle | To the main keel's lower edge: at AP; at FP; at the middle |
|---|---|---|---|---|---|
| WL1 | 0.03152 | | -2.03 to 95.58 | 12.80; 9.69; 11.25 | 12.39; 9.26; 10.83 |
| WL2 | 0.03144 | 2.39 | 2.36 to 92.07 | 10.41; 7.30; 8.86 | 10.00; 6.88; 8.44 |
| WL3 | 0.03155 | 4.75 | 3.24 to 90.07 | 8.05; 4.93; 6.49 | |
| WL4 | 0.03094 | 7.13 | 4.12 to 86.72 | 5.65; 2.59; 4.12 | |
| Faint ruled line (measured, tentative) | 0.0297 | 0.14 above at AP, 0.30 above at FP | -6.3 to FP; tentative on to about 100 | 12.94; 10.00; 11.47 | |

The faint line (measured): aft it is plain in ordinary and contrast-stretched crops, ruled from
-6.5 ft to the rudder, 0.12 to 0.13 ft above WL1; along the hull it is mottled but traceable, 44 of
50 windows on one straight line, rms 2.2 px; a short bar about 48 px long crosses the forward
perpendicular 0.30 ft above WL1, **10.00 ft above K**. Its ink is neutral grey, not green. Neither
sister has it: *Hound*'s ZAZ4262 shows nothing there, and *Diligence*'s ZAZ4320 has only its pencil
levels (§3.4).

### 4.2 Which is the load line (judgement)

**WL1, the top green line; probable, not labelled.** Taken as the 64's WL1 was
(`Research-Indefatigable-2026-10.md` §2.3.1):
1. **It alone of the green lines runs through.** WL1 alone of them crosses the rudder to its after
   edge and the stem to the knee's fore edge, on all three sheets (-2.03 to 95.58 ft here, -2.1 to
   95.6 on both sisters); the other three stop at the rabbets, and the plan's ends agree (§5.10). The
   faint line runs further, on this sheet alone.
2. **Steel** defines the load water line as the highest of the waterlines, when she is fully laden
   (1805 text, p. 188, read in `Research-Indefatigable-2026-10.md` §2.3.1).
3. **The sills.** The lowest stands 5.15 ft above WL1. Steel p. 124 gives "sloops, cutters, &c."
   four to five feet (`Build-Ships.md` §5.4); WL2 would make it 7.54 ft.
4. **The draught.** 11.25 ft to K at the middle against the file's 11.5 ft mean, itself a judgement
   from the depth in hold.
5. **Against it**, plainly: Steel's rule puts the wale's lower edge "a few inches" above the load
   line, and here it stands 1 ft 1 in above WL1 at its lowest; and *Harpy*'s recorded draught is 2.2
   ft lighter (§4.3). Steel's direct rule for "other ships" sets the load line at about five-eighths
   of the top-timber line's height at its lowest, up from the keel's underside (1805 text, OCR l.
   15184-15187): taking the plank-sheer line for the top-timber line (judgement), 19.09 x 5/8 = 11.93
   ft above K at station 4, 0.61 ft above WL1 and far above WL2.
6. **The faint line** is a candidate this judgement does not take. It is very faint, stands on this
   sheet and neither sister, and no plan or body plan carries it; but its bar stands 10.00 ft above K,
   a round figure, and its mean of 11.47 ft lies by the file's 11.5 ft. If it were the load line, the
   lowest sill would stand 4.90 ft (1.49 m), inside Steel's four to five feet, the band `Build-Ships.md`
   §5.4 first gave; the shut angle of §7 about 16.1° against 17.1°; every z of §6 less by 0.04 to
   0.09 m.

**Ruled (the lead, 2026-10-31): WL1, and the faint line recorded.** The profile is written on WL1, the
faint line stays as §4.1 measures it, and §5.4's band goes to the sheet (§7).

### 4.3 The drag, against Winfield and the file (recorded)

| | Forward, ft | Aft, ft | Mean, ft | Drag, ft | Source |
|---|---|---|---|---|---|
| WL1 to K | 9.69 | 12.80 | 11.25 | **3.11** | measured, at FP and AP; ±0.03 |
| WL1 to the main keel | 9.26 | 12.39 | 10.83 | 3.13 | measured |
| WL2 to K | 7.30 | 10.41 | 8.86 | 3.11 | measured |
| The faint line to K | 10.00 | 12.94 | 11.47 | 2.94 | measured, tentative |
| *Harpy*, as built | 7.25 | 10.83 | 9.04 | 3.58 | Winfield p. 256 |
| The file | 10.5 | 12.5 | 11.5 | 2.0 | judgement, `tools/gen_ships.py` (`draught_ft`) |

- **The drag measured is 3.11 ft in the 95 ft, 1.88°**, the waterlines' slope to the keel (the sheet
  states no drag); the sisters' 3.18 and 3.21.
- **Winfield's draughts lie near WL2** (forward 0.05 ft under it, aft 0.42 ft over it, mean 0.18 ft
  over it), 2.2 ft lighter than WL1 at the middle. By the drawn lines that is about 190 tons against
  about 300 at WL1, at about 56 tons a foot (WL1's waterplane 1,972 sq ft, 183 m², plank on; its
  centre 47.3 ft from AP). No page says at what state her draughts were taken; launched or with
  little aboard fits them (judgement). They are not her load draught on this reading, so
  `Build-Ships.md` §5.7's "drag T" is replaced by the waterlines' drag, rung S, and Winfield's
  stands beside it.
- **The keel they count to:** Steel's draughts are counted to the main keel's underside
  (`pages-steel-1805-bodies.md` §5.1), which takes 0.41 ft off each figure to K; Winfield's are not
  said.
- **The file's** 11.5 ft mean (3.5 m) is not moved; the profile's z stands on WL1, so that K is
  drawn 3.43 m below the water at the middle. Its `draught_m` differs by 0.07 m.

## 5. The profile, measured

### 5.1 The lines of the side (read; identification as marked)

From the top, at the lowest of the sheer:

- **The rail**, black, heavy, the top of the side: 8.35 ft above WL1 at station 4. A fine line lies
  0.21 ft under it. A few timber heads stand on it (read).
- **The plank-sheer's lower edge**, black, heavy, 0.58 ft (7 in) below the rail. Steel's *Raven*
  gives her waist to the underside of the plank-sheer as 20 ft forward, 19 ft midships and 22 ft 7½
  in aft above the keel's upper side; at her 95 to 100 ft these are 19.0, 18.05 and 21.5 ft, and
  this line stands 19.4, 17.8 and 21.8 ft: so the name (judgement). The ports' heads lie just under
  it amidships, as the *Raven*'s sheer strake is "to work down to the ports".
- **The band through the ports**, black, broken by them: its upper edge a fine line, its lower
  heavy, 0.34 ft (4 in) apart, 1.12 and 1.48 ft under the plank-sheer line, parallel to it within
  0.04 ft end to end. No name on the sheet; a moulding at the sheer strake's foot (judgement). Not
  written: it is no channel wale, and the viewer's band through the ports covers it but for two
  stubs (§6.3).
- **The deck's three lines**, red, taken, by judgement from the *Raven*'s plank and round and the
  16-in sill, as the deck plank at the middle line, the beam's upper side at the middle line and the
  beam's upper side at side (the sheets name none of them):
  - the top two are 0.24 ft (3 in, the *Raven*'s deck plank) apart;
  - the second and third are 0.71 ft (8.5 in) apart, the *Raven*'s 9-in round of the beams on her 30
    ft taken to these 28 ft, 8.4 in;
  - a beam in section on ZAZ4492 hangs from the second, about 1.35 ft deep, the round and a 7½-in
    beam;
  - with the plank added to the third, every sill stands 1 ft 4 in above the deck at side, the
    *Raven*'s "16 inches" (§5.7).
  So the third line + 0.24 ft is **the deck at side**, `decks_m.upper` (judgement on measured
  lines).
- **The wale**, black: upper edge a thin line, lower edge the heaviest line on the side, 2.11 ft (25
  in) apart at the lowest, the *Raven*'s two strakes of 12 in. The lower edge stands 1.08 ft above
  WL1 at station 4.
- **The height of breadth**, black, thin and dashed throughout, inside the wale amidships, leaving
  it forward and running on up to the hawse holes: it is the level line the body plan draws at ⊗
  (§5.11).
  Lowest 2.57 ft above WL1 at station 6, as Steel's rule lifts it to the ends (`Build-Ships.md`
  §5.3).
- **Below the wale**: nothing on the side down to the water; the waterlines; the deadwood, the
  cutting-down line and the keelson in red (§5.4).

### 5.2 By station (measured)

Feet above WL1 at each station, ±0.05 ft (rail, ±0.05; the deck lines, ±0.03), negative below it.
The deck at side is the third deck line + 0.24 ft (§5.1).

| Stn | ft from AP | m from mid | Rail | Plank-sheer, lower edge | Deck plank, middle line | Beam, middle line | Beam, at side | Deck at side | Wale, upper edge | Height of breadth | Wale, lower edge | Rabbet line | Keel, upper edge | Main keel, lower edge | K |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 23 | 5.38 | -12.84 | 10.37 | 9.77 | 5.50 | 5.25 | 4.86 | 5.10 | 5.25 | 4.87 | 3.15 | -11.06 | -11.31 | -12.22 | -12.63 |
| 22 | 7.50 | -12.19 | 10.16 | 9.56 | 5.40 | 5.15 | 4.72 | 4.96 | 5.05 | 4.66 | 2.95 | -10.99 | -11.24 | -12.15 | -12.56 |
| 20 | 11.76 | -10.89 | 9.78 | 9.19 | 5.20 | 4.94 | 4.47 | 4.71 | 4.66 | 4.08 | 2.56 | -10.85 | -11.10 | -12.01 | -12.42 |
| 18 | 15.98 | -9.61 | 9.46 | 8.86 | 5.03 | 4.77 | 4.26 | 4.50 | 4.33 | 3.64 | 2.22 | -10.71 | -10.96 | -11.87 | -12.28 |
| 16 | 20.14 | -8.34 | 9.17 | 8.58 | 4.88 | 4.64 | 4.07 | 4.31 | 4.04 | 3.29 | 1.92 | -10.57 | -10.83 | -11.73 | -12.14 |
| 14 | 24.40 | -7.04 | 8.93 | 8.34 | 4.76 | 4.53 | 3.91 | 4.15 | 3.79 | 3.00 | 1.68 | -10.43 | -10.68 | -11.59 | -12.00 |
| 12 | 28.60 | -5.76 | 8.72 | 8.14 | 4.67 | 4.43 | 3.79 | 4.03 | 3.58 | 2.80 | 1.47 | -10.29 | -10.55 | -11.45 | -11.87 |
| 10 | 32.78 | -4.49 | 8.56 | 7.98 | 4.60 | 4.35 | 3.67 | 3.91 | 3.41 | 2.66 | 1.31 | -10.15 | -10.41 | -11.31 | -11.73 |
| 8 | 37.02 | -3.19 | 8.44 | 7.86 | 4.55 | 4.31 | 3.61 | 3.85 | 3.29 | 2.58 | 1.19 | -10.01 | -10.27 | -11.17 | -11.59 |
| 6 | 41.20 | -1.92 | 8.38 | 7.80 | 4.52 | 4.28 | 3.57 | 3.81 | 3.22 | 2.57 | 1.11 | -9.88 | -10.13 | -11.04 | -11.45 |
| 4 | 45.41 | -0.64 | 8.35 | 7.77 | 4.51 | 4.27 | 3.55 | 3.79 | 3.19 | 2.61 | 1.08 | -9.74 | -9.99 | -10.90 | -11.32 |
| 2 | 49.65 | +0.65 | 8.37 | 7.80 | 4.52 | 4.28 | 3.57 | 3.81 | 3.20 | 2.70 | 1.10 | -9.60 | -9.85 | -10.76 | -11.18 |
| ⊗ | 53.48 | +1.82 | 8.43 | 7.86 | 4.55 | 4.31 | 3.63 | 3.87 | 3.25 | 2.81 | 1.16 | -9.47 | -9.72 | -10.63 | -11.05 |
| B | 57.28 | +2.98 | 8.51 | 7.94 | 4.59 | 4.35 | 3.68 | 3.92 | 3.33 | 2.94 | 1.24 | -9.35 | -9.60 | -10.51 | -10.93 |
| D | 61.48 | +4.26 | 8.65 | 8.08 | 4.68 | 4.44 | 3.77 | 4.01 | 3.46 | 3.15 | 1.37 | -9.21 | -9.46 | -10.37 | -10.79 |
| F | 65.67 | +5.54 | 8.84 | 8.27 | 4.78 | 4.54 | 3.90 | 4.14 | 3.63 | 3.49 | 1.55 | -9.07 | -9.32 | -10.23 | -10.65 |
| H | 69.86 | +6.81 | 9.08 | 8.51 | 4.91 | 4.67 | 4.07 | 4.31 | 3.86 | 3.96 | 1.76 | -8.93 | -9.18 | -10.09 | -10.51 |
| K | 74.05 | +8.09 | 9.38 | 8.80 | 5.07 | 4.84 | 4.25 | 4.49 | 4.14 | 4.44 | 2.04 | -8.79 | -9.04 | -9.95 | -10.38 |
| M | 78.27 | +9.38 | 9.72 | 9.15 | 5.23 | 5.01 | 4.48 | 4.72 | 4.48 | 5.07 | 2.39 | -8.65 | -8.90 | -9.81 | -10.24 |
| O | 82.45 | +10.65 | 10.12 | 9.54 | 5.43 | 5.20 | 4.74 | 4.98 | 4.88 | 5.87 | 2.79 | -8.52 | -8.77 | -9.68 | -10.10 |
| Q | 86.65 | +11.93 | 10.59 | 10.02 | 5.65 | 5.41 | 5.04 | 5.28 | 5.34 | 6.85 | 3.25 | -8.38 | -8.63 | -9.54 | -9.96 |
| S | 90.83 | +13.21 | 11.11 | 10.55 | 5.88 | 5.65 | 5.37 | 5.61 | 5.85 | 8.04 | 3.76 | -8.24 | -8.49 | -9.40 | -9.83 |

- **⊗** has no line at its 53.48 ft: two are drawn, at 53.09 and 53.86 ft, and the row is at their
  mean (read, measured). The aft body's stations are spaced from the fore line and the fore body's
  from the after line.
- **The sheer** of the rail: lowest at station 4, 45.41 ft (8.35 ft); rising 2.58 ft to AP (10.93
  ft) and 3.58 ft to its end at the stem head; of the deck plank at the middle line, lowest at
  station 4 (4.51 ft), rising 1.29 ft to AP (5.80) and 1.63 ft to FP (6.14).
- **Bulwark**: rail above the deck at side, 4.56 ft at the lowest, 5.27 ft at 23, 5.50 ft at S.
- **Its ends:** the rail starts at the side's after edge at -4.65 ft, 11.50 ft above WL1 (§5.6);
  forward it runs on at 92.38 ft 11.34, 93.87 ft 11.53, 95.37 ft 11.76, to the moulded end at the
  stem head at 96.62 ft, 11.93 ft.
- The waterlines' heights by station are WL1's: WL2, WL3 and WL4 stand at -2.39, -4.75 and -7.13 ft
  at every station, ±0.02 ft (the last rising to -7.08 at Q).

### 5.3 The decks and their ends (measured; ±0.05 ft)

- **Upper deck, flush**: no quarterdeck or forecastle (read; both plans and both profiles). Its
  lines run from the counter to the stem: the plank's upper side from -1.88 ft to FP, the third line
  from -0.7 ft to FP, the deck at side there 5.49 ft above WL1 aft and 6.13 ft at FP.
- **At the middle** (47.50 ft): the plank at the middle line 4.51 ft (1.38 m), the deck at side 3.80
  ft (1.16 m) above WL1. The lowest of the deck at side is 3.79 ft, at station 4.
- **Lower deck** (ZAZ4492 only, its two red lines; not read for the profile, being under the water,
  judgement; ±0.1 ft): the upper line -1.10 ft at 33 to 50 ft, -0.97 at B, -0.80 at F, -0.55 at K,
  -0.22 at O, +0.18 at S; stepped down aft to about -1.4 ft at 19 ft and rising to about -0.95 ft at
  3 ft. Its plan names a bread room, cabins, a magazine, the well, the sail room and stores. It
  stands about 4 ft 8 in under the upper deck's beams at side: not a gun deck, and no port is cut
  for it (read).

### 5.4 The keel and the rabbet (measured)

- **The rabbet line**, dashed, straight, from the post's rabbet at 5.59 ft, -11.02 ft, to the stem's
  at about 82.7 ft, -8.50 ft. **The body plan's base is this line**: its keel section's shoulder
  stands 26 px under the base and the sheer's keel 25 px under the dashed line (read, measured). So
  §5.11's heights are from it.
- **The keel's upper edge**, heavy: 0.25 ft (3 in) under the rabbet line, straight.
- **The main keel's lower edge**, thin: 0.91 ft (11 in) under its upper edge, straight, to about 87
  ft (Steel's *Raven*: 12 in).
- **K, the false keel's lower edge**: the heavy upper border of the scale strip, 0.42 ft (5 in)
  under the main keel (the *Raven*'s false keel 5½ in; the body plan's keel section gives a main
  keel 11.5 in deep under its shoulder and 5.3 in of false keel). That the border is K is judgement:
  no other line is drawn there, the post's after edge ends on it and the knee of the head runs out
  along it. It runs straight and drags 3.11 ft against WL1, from the post's heel at 4.59 ft, -12.65
  ft, to the knee's foot at 87.56 ft, -9.93 ft.
- **Sided** 1 ft 0 in at the keel section; 0.34 ft (4 in) half-siding at the rabbet at ⊗, 0.46 to
  0.48 ft where the waterlines end on the stem's, 0.16 to 0.76 ft on the post's (§5.10).
- **The cutting-down line**, red: 1.25 ft above the rabbet line at ⊗ (18 in above the keel's upper
  edge; the *Raven*'s 19½ in), sweeping up to about 10 ft above it 3 ft from AP; the **keelson's
  top** 1.0 ft above that at ⊗. The floors' rising line is not drawn (read), so `floor_m` has no
  source.

### 5.5 The stem and the head (measured; ±0.05 ft)

Bow to the right; feet from AP, above WL1. All on ZAZ4491.

- **The rabbet**, heavy, from the keel at 82.7 ft: 91.24 ft at -3.55, 93.47 ft at -0.05 (WL1 here),
  95.22 ft at +5.56, the head of it under the rail's moulding at 96.24 ft, 11.14.
- **The stem's fore edge**, thin, 0.8 to 1.1 ft before the rabbet, foot boxed into the keel at 84.2
  ft, -8.93: 85.38 at -8.53, 89.01 at -6.62, 92.24 at -3.52, 94.29 at the water, 96.0 at +5.59,
  96.84 at +10.11, to **the stem head**, 97.03 ft, 11.30 ft (x +15.10 m, z 3.44 m).
- **The knee of the head's fore edge**: leaving K at 87.56 ft, -9.93; 91.14 at -7.55; 94.23 at
  -2.46; **95.67 ft at the water**; 97.92 at +3.15, 101.0 at +5.74, 102.28 at +6.78, 103.12 at
  +7.81; a notch under the scroll at 103.53 ft, 10.03.
- **The scroll**: a volute curling forward and in over the knee's top, its fore side 103.86 ft at
  11.75, its top 103.11 ft, 12.38 ft. **`form.head`: scroll** (read; Steel's *Raven* has "a small
  scroll head, with cheeks and rail"). No figure. Two cheeks and a rail of the head with two
  standards; no carving is drawn beyond the scroll.
- **Bowsprit**: its lower edge from the stem head's fore side at 10.88 ft, steeved 13.9° to the
  page, 15.7° to WL1; 1.5 ft through; drawn broken off at about 108 ft (read). It stands by the
  knighthead, whose hatched top stands 13.3 ft above WL1 beside it.
- **Two hawse holes**, hatched, at 94.1 and 95.0 ft, about 8.0 ft above WL1; the height of breadth
  meets them (§5.1). A cathead, its square end at 93.5 to 94.4 ft, about 13 ft above WL1.

### 5.6 The stern (measured; ±0.1 ft)

**Square, with a tuck, a counter and a raked transom, flat in the rake and rounded in plan; plain**
(read). No galleries; no lights
but the two stern ports; a taffrail with a horn each side and a quarter piece each side. The stern
board is laid over the body plan.

Along the middle line (`stern_m`), feet from AP, above WL1:
- **The post's after edge**: heel at K, 4.59 ft, -12.65; 2.87 at -7.34; 1.59 at -3.38; 0.46 at the
  water; -0.66 at 3.54; -1.17 at 5.22, a rake of 17.9° to the page. The rudder hangs on it by three
  braces, its after edge -2.03 ft at the water and 0.59 ft at its foot, its blade 2.5 ft broad at
  the water and 3.8 ft at the foot, by the rudder's own lines.
- **The post's rabbet** (fore side), 1.2 to 1.5 ft before the after edge: 5.59 ft at -11.02 to 0.59
  ft at 3.68, the **wing transom's crown**.
- **The counter**, heavy: from where the post comes through, -1.17 ft at 5.22; -3.03 at 6.23; -4.62
  at 6.88, to a moulded rail, its after end -4.86 ft at 7.23.
- **The transom's face at the middle line**, 0.75 ft abaft its edges (the plan's arcs round aft by
  0.59 to 0.65 ft): -4.84 ft at 7.90; -5.38 at 9.38; -5.90 at 10.86; a rake of about 20° to the
  page.
- **The taffrail at the middle line**: **-6.55 ft, 12.07 ft (x -16.47 m, z 3.68 m)**. Its horns
  stand 0.32 ft above that, at their top 12.39 ft above WL1 at -5.8 to -5.0 ft.
- **At the side**: the transom's edge from the counter at -3.49 ft, 6.47 ft to -5.4 ft at the rail's
  height; the side's after edge meets the rail at -4.65 ft, 11.50.

On the stern board, half-breadths in feet, heights above the rabbet line (read, measured; the sheer
plan's z = this less 11.21 at the post):
- **The wing transom** (the lower heavy arc, the knuckle): crown 14.99 ft (sheer plan 14.89), ends
  14.56 ft at half-breadth 9.35; round-up **0.43 ft (5 in)**. Above WL1: crown 3.68 ft, ends 3.25
  ft.
- **The counter's upper rail** (the upper heavy arc): crown 18.30 ft, ends 17.80 ft at half-breadth
  9.3 to the outermost line, 8.3 to the moulded one; round-up 0.51 ft.
- **The taffrail** (two arcs): 23.50 and 23.17 ft at the middle line, falling 0.26 ft by
  half-breadth 5.3, turning down to the horns at about 7.3; the horns' top about 23.93 ft (the sheer
  plan's 23.82).
- **The two stern ports**: head 20.79 ft, sill 18.42 ft; their inner edges at half-breadths 1.85 to
  1.97 ft, outer 4.50 to 4.66 ft. Above WL1, 9.34 and 7.00 ft. Steel's *Raven* has stern ports and
  "a neat plain taffrail".
- **The rudder's head** comes through under a hatched coat at the middle line, about 16.4 to 17.7 ft
  above the rabbet line, and is drawn broken off below at 13.2 ft.

The stern board's outline has **nested lines**: the moulded stern timbers, 7.43 ft at 22.83 ft to
8.30 at 18.13 ft, agreeing with the half-breadth plan's arcs (§5.10); and outside them, in the outer
heavy line, the quarter pieces, about 1.0 ft wider, 9.30 at 17.83 and 10.0 ft at 15.85 ft, closing
in to the wing transom's end at 9.35 ft.

### 5.7 The ports (measured)

**Ten a side** (read, both sheets and both sisters). Centres, widths and depths at the side; ±0.03
ft along, ±0.05 ft up. Half-breadths from the body plan at the sill's height between the stations
either side (§5.11), ±0.1 ft.

| Port, from aft | ft from AP | m from mid | Width, ft | Depth, ft | Sill above WL1, ft (m) | Head above WL1, ft | Sill above the deck at side, ft | Half-breadth at the sill, moulded, ft | ZAZ4492: ft from AP; width; depth; sill less ZAZ4491 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 9.61 | -11.55 | 2.74 | 2.35 | 6.20 (1.89) | 8.55 | 1.36 | 10.89 | 9.64; 2.81; 2.36; -0.13 |
| 2 | 18.02 | -8.98 | 2.72 | 2.36 | 5.77 (1.76) | 8.12 | 1.36 | 11.99 | 18.06; 2.75; 2.39; -0.21 |
| 3 | 26.47 | -6.41 | 2.71 | 2.32 | 5.44 (1.66) | 7.75 | 1.34 | 12.76 | 26.49; 2.76; 2.25; -0.11 |
| 4 | 34.89 | -3.84 | 2.78 | 2.29 | 5.24 (1.60) | 7.52 | 1.36 | 13.30 | 34.93; 2.75; 2.31; -0.03 |
| 5 | 43.29 | -1.28 | 2.79 | 2.32 | 5.15 (1.57) | 7.47 | 1.35 | 13.58 | 43.33; 2.75; 2.28; -0.01 |
| 6 | 51.72 | +1.29 | 2.76 | 2.31 | 5.18 (1.58) | 7.48 | 1.34 | 13.69 | 51.73; 2.73; 2.28; +0.01 |
| 7 | 60.29 | +3.90 | 2.78 | 2.33 | 5.33 (1.62) | 7.66 | 1.35 | 13.56 | 60.32; 2.74; 2.32; -0.00 |
| 8 | 68.69 | +6.46 | 2.77 | 2.29 | 5.58 (1.70) | 7.87 | 1.32 | 13.35 | 68.68; 2.73; 2.28; +0.08 |
| 9 | 77.04 | +9.00 | 2.77 | 2.28 | 6.00 (1.83) | 8.28 | 1.35 | 12.31 | 77.02; 2.85; 2.33; -0.01 |
| 10 | 85.45 | +11.57 | 2.72 | 2.27 | 6.53 (1.99) | 8.80 | 1.34 | 9.77 | 85.47; 2.76; 2.32; -0.06 |

- **Spacing** 8.35 to 8.57 ft, mean 8.43 ft (2.57 m); the row is even about the middle, ±37.9 ft.
- **Size:** 2.75 by 2.31 ft on the mean, 2 ft 9 in by 2 ft 4 in; Steel's *Raven* 2 ft 9 in by 2 ft 6
  in.
- **Sills above the deck at side:** 1.35 ft, ±0.03, 1 ft 4 in at every port; Steel's *Raven* 16 in.
  So the sills run parallel to the deck, and the sheet's sills are the class's (judgement).
- **Which is which** (judgement; the fit stays as the file has it): on the file's eight carronades a
  side the guns stand on ports 2 to 9 within 0.12 m, the chase gun nearest port 10, port 1 empty
  (§7). Each port with a gun in it is written at the gun's x (§6.2).
- **The sweep ports:** eight, small, 0.8 by 0.7 ft, between ports 1 and 9 and none between 9 and 10:
  at 13.8, 21.9, 30.6, 39.0, 47.5, 56.2, 64.6 and 71.8 ft, sills 5.97, 5.60, 5.32, 5.17, 5.15, 5.25,
  5.44, 5.72 ft above WL1 (±0.1 ft). They are 81's to draw and hold no triple.

### 5.8 The channels and the chains (read)

A main and a fore channel at the plank-sheer, with dead-eyes on them, chains down to bolts about 1
ft above the wale's lower edge; in green, extra dead-eyes on the fore channel (§2.3). Not asked for
by the form; left for a later viewer.

### 5.9 The masts (measured)

Centres in red on both sheets; each is the fit of a dozen rows, rms under 0.5 px.

| Mast | ZAZ4491: ft from AP at the deck (at K) | ZAZ4492 | m from mid | Rake, to the page; to the keel; to WL1 | In green, 1799 (ZAZ4492) | The file |
|---|---|---|---|---|---|---|
| Main | 34.51 (34.84) | 34.56 | **-3.96** | 1.22°; 1.30°; 3.03° | 34.13 ft at the deck, **-4.07 m**: 0.43 ft aft at the deck | -3.9 m, 4.0° |
| Fore | 79.06 (79.23) | 79.08 | **+9.62** | 0.65°; 0.73°; 2.46° | 78.23 ft at the deck, **+9.37 m**: 0.85 ft aft at the deck | +8.9 m, 1.2° |

No green is drawn below the deck (read): the green is at the deck's X marks alone. Faint grey ticks
low in the hold stand about 0.24 ft abaft the main's red line, some 2 ft above its step, and about
0.87 ft abaft the fore's, at its step (measured, tentative; neutral ink, the paper's own colour).

The sheer plan also carries a fine plain vertical at 31.77 ft, on the profile and the plan,
unlabelled (read; unexplained).

### 5.10 The half-breadths, moulded (measured)

Off the half-breadth plan; ±0.03 ft between 16 and K, ±0.1 ft at the ends. The stations are the
sheer's, carried down with the plate's lean. "WL" half-breadths are at the height the sheer gives
each line at its station (§5.2).

| Stn | ft from AP | m from mid | WL1 | WL2 | WL3 | WL4 | Main breadth | Top-timber line |
|---|---|---|---|---|---|---|---|---|
| 23 | 5.38 | -12.84 | 4.24 | 1.25 | 0.57 | 0.27 | 10.24 | 9.83 |
| 22 | 7.50 | -12.19 | 6.09 | 2.25 | 1.02 | 0.47 | 10.61 | 10.20 |
| 20 | 11.76 | -10.89 | 8.86 | 4.62 | 2.16 | 0.97 | 11.26 | 10.87 |
| 18 | 15.98 | -9.61 | 10.39 | 6.87 | 3.54 | 1.57 | 11.79 | 11.42 |
| 16 | 20.14 | -8.34 | 11.29 | 8.64 | 5.10 | 2.24 | 12.25 | 11.88 |
| 14 | 24.40 | -7.04 | 11.95 | 9.88 | 6.55 | 2.98 | 12.65 | 12.28 |
| 12 | 28.60 | -5.76 | 12.38 | 10.74 | 7.72 | 3.69 | 12.97 | 12.62 |
| 10 | 32.78 | -4.49 | 12.71 | 11.34 | 8.57 | 4.33 | 13.23 | 12.88 |
| 8 | 37.02 | -3.19 | 12.95 | 11.70 | 9.16 | 4.82 | 13.44 | 13.09 |
| 6 | 41.20 | -1.92 | 13.11 | 11.93 | 9.52 | 5.07 | 13.58 | 13.24 |
| 4 | 45.41 | -0.64 | 13.20 | 12.05 | 9.74 | 5.18 | 13.65 | 13.31 |
| 2 | 49.65 | +0.65 | 13.25 | 12.09 | 9.81 | 5.20 | 13.71 | 13.36 |
| ⊗ | 53.48 | +1.82 | 13.25 | 12.06 | 9.76 | 5.11 | 13.73 | 13.39 |
| B | 57.28 | +2.98 | 13.23 | 11.98 | 9.54 | 4.88 | 13.71 | 13.37 |
| D | 61.48 | +4.26 | 13.09 | 11.75 | 9.10 | 4.39 | 13.61 | 13.30 |
| F | 65.67 | +5.54 | 12.79 | 11.29 | 8.43 | 3.73 | 13.46 | 13.16 |
| H | 69.86 | +6.81 | 12.29 | 10.56 | 7.49 | 2.95 | 13.15 | 12.94 |
| K | 74.05 | +8.09 | 11.46 | 9.49 | 6.30 | 2.19 | 12.67 | 12.55 |
| M | 78.27 | +9.38 | 10.27 | 8.03 | 4.89 | 1.49 | 11.95 | 11.94 |
| O | 82.45 | +10.65 | 8.54 | 6.13 | 3.36 | 0.86 | 10.88 | 10.92 |
| Q | 86.65 | +11.93 | 6.06 | 3.83 | 1.73 | 0.33 | 9.27 | 9.42 |
| S | 90.83 | +13.21 | 2.81 | 1.21 |  |  | 6.76 | 7.03 |

- **The waterlines' ends**, read on the rabbets, half-breadth in ft: aft WL1 0.76 at 1.61 ft, WL2
  0.28 at 2.44 ft, WL3 0.20 at 3.38 ft, WL4 0.16 at 4.13 ft; forward WL1 0.48 at 93.47 ft, WL2 0.46
  at 92.03 ft, WL3 0.46 at 89.97 ft, WL4 0.37 at 86.85 ft. The sheer plan's ends agree within 0.3 ft
  (§4.1).
- **WL1** is 91.86 ft long moulded, rabbet to rabbet. Greatest half-breadth 13.25 ft, from 49.65 to
  53.48 ft.
- **The main breadth** is greatest, 13.73 ft, at ⊗, 6 ft before the middle.
- **Its two ends:** aft the main breadth runs to 8.28 ft at -3.53 ft, the top-timber line to 7.36 ft
  at -5.13 ft, the transom's arcs from there to the middle line at -4.24 and -5.80 ft (§5.6).
  Forward both run on to the stem: main breadth 4.35 ft at 93.36 ft, top-timber 4.61 ft at 93.47 ft,
  and both end 0.4 to 0.5 ft from the middle line at 95.9 to 96.2 ft.
- **The two cross** at about 78 ft: the top-timber line is inside the main breadth to M and outside
  it forward, by 0.27 ft at S: tumblehome abaft, flare before. Tumblehome 0.34 ft (4 in) at ⊗, 0.41
  ft at 23.

### 5.11 The sections (measured)

The body plan, by level above the rabbet line, moulded half-breadth in feet. Sections B and 2 are
not drawn (read). D above about 12 ft is not separated from ⊗ (read), and 14 and 10 cross other
lines low down: blank there. ±0.1 ft where they stand apart, ±0.15 ft where they crowd, in the bilge
of ⊗, 4 and 6.

| Stn | 0.5 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 23 | 0.24 | 0.24 | 0.26 | 0.29 | 0.34 | 0.40 | 0.50 | 0.65 | 0.93 | 1.49 | 2.56 | 4.29 | 6.60 | 8.65 | 9.65 | 10.11 | 10.25 | 10.25 | 10.19 | 10.10 | 10.00 | 9.88 |
| 22 | 0.30 | 0.33 | 0.40 | 0.48 | 0.58 | 0.71 | 0.92 | 1.24 | 1.78 | 2.74 | 4.25 | 6.28 | 8.35 | 9.63 | 10.26 | 10.55 | 10.63 | 10.61 | 10.55 | 10.45 | 10.35 | 10.24 |
| 20 | 0.35 | 0.40 | 0.55 | 0.76 | 1.05 | 1.46 | 2.03 | 2.86 | 3.97 | 5.71 | 7.55 | 9.24 | 10.27 | 10.86 | 11.16 | 11.25 | 11.24 | 11.19 | 11.10 | 11.01 | 10.91 |  |
| 18 |  |  |  |  | 1.87 | 2.69 | 3.71 | 4.89 | 6.46 | 8.08 | 9.58 | 10.62 | 11.24 | 11.62 | 11.79 | 11.83 | 11.80 | 11.73 | 11.63 |  |  |  |
| 16 | 0.44 | 0.61 | 1.11 | 1.85 | 2.83 | 4.04 | 5.42 | 6.90 | 8.41 | 9.77 | 10.83 | 11.51 | 11.95 | 12.20 | 12.28 | 12.28 | 12.24 | 12.15 | 12.06 | 11.95 |  |  |
| 14 |  |  |  | 2.65 | 4.02 | 5.57 | 7.13 | 8.57 | 9.68 | 10.88 | 11.63 | 12.14 | 12.47 | 12.62 | 12.66 | 12.64 | 12.58 | 12.50 | 12.41 |  |  |  |
| 12 |  | 0.97 | 2.09 | 3.54 | 5.16 | 6.80 | 8.36 | 9.71 | 10.82 | 11.66 | 12.25 | 12.65 | 12.89 | 13.01 | 13.01 | 12.99 | 12.92 | 12.84 | 12.75 | 12.66 |  |  |
| 10 |  | 1.15 | 2.66 | 4.40 | 6.22 | 7.92 | 9.39 | 10.59 | 11.48 | 12.22 | 12.69 | 13.02 | 13.19 | 13.25 | 13.26 | 13.22 | 13.15 | 13.05 | 12.95 |  |  |  |
| 8 |  | 1.44 | 3.14 | 5.10 | 7.05 | 8.74 | 10.10 | 11.17 | 11.99 | 12.59 | 13.00 | 13.28 | 13.41 | 13.47 | 13.47 | 13.42 | 13.34 | 13.24 | 13.12 |  |  |  |
| 6 |  | 1.65 | 3.59 | 5.77 | 7.77 | 9.38 | 10.65 | 11.59 | 12.32 | 12.84 | 13.21 | 13.44 | 13.56 | 13.61 | 13.59 | 13.54 | 13.46 | 13.35 |  |  |  |  |
| 4 |  | 1.81 | 3.93 | 6.29 | 8.31 | 9.86 | 11.02 | 11.88 | 12.53 | 13.01 | 13.34 | 13.56 | 13.64 | 13.68 | 13.66 | 13.61 |  |  |  |  |  |  |
| ⊗ | 1.02 | 1.94 | 4.20 | 6.71 | 8.76 | 10.26 | 11.34 | 12.12 | 12.74 | 13.17 | 13.49 | 13.68 | 13.76 | 13.77 | 13.75 | 13.69 | 13.61 | 13.51 |  |  |  |  |
| D |  |  |  |  | 8.54 | 10.04 | 11.15 | 12.00 | 12.62 | 13.08 | 13.40 | 13.60 | 13.69 |  |  |  |  |  |  |  |  |  |
| F |  | 1.75 | 3.84 | 6.13 | 8.05 | 9.60 | 10.79 | 11.68 | 12.34 | 12.83 | 13.18 | 13.42 | 13.54 | 13.57 | 13.56 | 13.51 | 13.42 | 13.32 |  |  |  |  |
| H | 0.84 | 1.58 | 3.42 | 5.47 | 7.30 | 8.88 | 10.15 | 11.14 | 11.88 | 12.44 | 12.82 | 13.09 | 13.25 | 13.30 | 13.29 | 13.25 | 13.18 | 13.10 | 12.99 |  |  |  |
| K |  | 1.34 | 2.85 | 4.58 | 6.31 | 7.85 | 9.17 | 10.27 | 11.11 | 11.75 | 12.21 | 12.52 | 12.72 | 12.81 | 12.83 | 12.81 | 12.76 | 12.71 | 12.64 |  |  |  |
| M | 0.58 | 1.06 | 2.27 | 3.66 | 5.09 | 6.53 | 7.83 | 8.95 | 9.87 | 10.63 | 11.19 | 11.60 | 11.87 | 12.01 | 12.08 | 12.10 | 12.10 | 12.09 | 12.07 |  |  |  |
| O |  | 0.71 | 1.55 | 2.58 | 3.72 | 4.88 | 6.06 | 7.18 | 8.17 | 9.02 | 9.70 | 10.22 | 10.58 | 10.82 | 10.93 | 10.99 | 11.02 | 11.03 | 11.04 |  |  |  |
| Q |  |  | 0.64 | 1.30 | 2.10 | 3.00 | 3.92 | 4.85 | 5.77 | 6.64 | 7.43 | 8.08 | 8.58 | 8.93 | 9.16 | 9.31 | 9.39 | 9.44 | 9.47 |  |  |  |
| S |  |  |  |  |  | 0.68 | 1.31 | 2.00 | 2.71 | 3.42 | 4.11 | 4.78 | 5.39 | 5.92 | 6.30 | 6.54 |  |  |  |  |  |  |

- **Against the half-breadth plan:** at each station and waterline the plan's half-breadth, at the
  sheer's height, gives a place on the body plan, and the nearest line was read there, 80 places
  (`xcheck2.py`): median +0.01 ft, rms 0.07 ft. The aft body's lines lie within about 0.05 ft; the
  fore body's stand out 0.05 to 0.2 ft on the plan, most at H to O. The fore body is a true
  difference of the two views of the sheet (judgement). **Where both read, the plan's waterlines are
  the points of §6.**
- **Section S** ends on the stem's rabbet, about 4.2 ft above the rabbet line carried on (-1.22 m,
  half-breadth 0.27 ft, stepping out to the stem's siding, 0.5 ft; read, measured, ±0.1 ft), so its
  row stops at 5 ft.
- **The floor** rises: at ⊗, 1.94 ft out at 1 ft, 4.20 at 2, 6.71 at 3, 8.76 at 4, about 25° from
  the rabbet to the turn; hollow aft of 16, with a long S at 20 to 23. Bilge turns between 6 and 9
  ft; dead flat at 13.75 to 13.77 ft from 12 to 14 ft; 13.39 ft at the rail.
- **The height of breadth at ⊗** on the body plan is the heavy level line at 12.27 ft above the
  base; the sheer's line stands 12.28 ft above the rabbet line there (read, measured).

## 6. For the profile: the points in metres

### 6.1 How they were made, and that they pass

`x` forward of the mid-perpendiculars, `z` above WL1, both in metres to the centimetre, from §5;
half-breadths with 3 in of plank (§2.2, 0.08 m). Rung **S**: her class's own lines (`Build-Ships.md`
§5.0 principle 3). Marks in §6.3.

**As built:** `tools/ships/hull_brig.py` holds these points, and `tools/gen_ships.py` writes them
through the tree's `g.hull_profile` and `g.hull_form` at `bb60222` (`freesail` imported from the
worktree), which report: the side at each sill, aft to forward, off the half-breadth by -0.02, -0.02,
-0.03, -0.03, -0.02, -0.03, -0.01, -0.05, -0.03, -0.02 m, the one at x 6.5 a hair over
`form.PORT_GAP_M` (-0.051 m: the fore body's difference of the two views, §5.11, reported and not
moved); drawn displacement 303 t against the filed 413 t, -27%, "recorded, not moved"; drawn 2.87 m
deep at the greatest section against the file's 3.5 m (the drawn body stops near the rabbet line; K
stands 0.48 m under it). Those figures are the generator's report and `tests/test_hull_brig.py`'s,
not the file's notes.

**The body above the water.** The first form of these points ran straight from WL1 to the main
breadth, which at the ends stands 3 ft 8 in to 8 ft above WL1, and missed the body plan by up to
0.56 m at section 23 and 0.21 m at Q and S: more than 2 px on the owner's picture, where the side
shows. So at the ten stations where the height of breadth stands more than 3 ft 6 in above WL1 (23
to 18, H to S) `sections_m` also takes the body plan's whole-foot levels between them (§5.0
principle 5). Against every cell of §5.11 above the water the drawn side is now off by 0.02 m rms,
0.05 m at the most (it was 0.10 and 0.56).

**The run's hollow.** Under the water the points run straight between WL2 and WL1, 2 ft 5 in apart,
and at 23 and 22, where the section is hollow, that missed the body plan by 0.11 and 0.08 m. So those
two also take the body plan's two whole-foot levels between them. Against every cell of §5.11 under
the water the drawn side is now off by 0.03 m rms, 0.08 m at the most; the largest stand where the
body plan's lines crowd or the fore body's difference of the two views lies (§5.11).

### 6.2 The lines

```
rail_m:
  [-16.47, 3.68], [-15.90, 3.51], [-15.54, 3.45], [-14.93, 3.38], [-14.48, 3.33], [-12.84,
  3.16], [-12.19, 3.10], [-10.89, 2.98], [-9.61, 2.88], [-8.34, 2.80], [-7.04, 2.72], [-5.76,
  2.66], [-4.49, 2.61], [-3.19, 2.57], [-1.92, 2.55], [-0.64, 2.54], [0.65, 2.55], [1.82,
  2.57], [2.98, 2.59], [4.26, 2.64], [5.54, 2.70], [6.81, 2.77], [8.09, 2.86], [9.38, 2.96],
  [10.65, 3.09], [11.93, 3.23], [13.21, 3.39], [13.68, 3.46], [14.14, 3.52], [14.59, 3.58],
  [14.97, 3.64]
breadth_m:
  [-13.99, 0.31, 2.84], [-12.84, 1.37, 3.07], [-12.19, 1.93, 3.19], [-10.89, 2.78, 3.39],
  [-9.61, 3.24, 3.56], [-8.34, 3.52, 3.70], [-7.04, 3.72, 3.82], [-5.76, 3.85, 3.92], [-4.49,
  3.95, 4.00], [-3.19, 4.02, 4.07], [-1.92, 4.07, 4.11], [-0.64, 4.10, 4.13], [0.65, 4.12,
  4.15], [1.82, 4.12, 4.16], [2.98, 4.11, 4.15], [4.26, 4.07, 4.13], [5.54, 3.98, 4.09],
  [6.81, 3.82, 4.02], [8.09, 3.57, 3.90], [9.38, 3.21, 3.72], [10.65, 2.68, 3.40], [11.93,
  1.92, 2.95], [13.21, 0.93, 2.22], [14.01, 0.22, 1.48]
keel_m:
  [-13.08, -3.86], [12.21, -3.03]
stem_m:
  [11.19, -2.72], [11.55, -2.60], [12.13, -2.34], [12.65, -2.02], [13.05, -1.70], [13.37,
  -1.39], [13.64, -1.07], [13.86, -0.76], [14.05, -0.45], [14.20, -0.14], [14.26, -0.01],
  [14.33, 0.17], [14.44, 0.47], [14.54, 0.78], [14.63, 1.09], [14.71, 1.40], [14.78, 1.70],
  [14.84, 2.01], [14.87, 2.16], [14.90, 2.32], [14.95, 2.56], [14.98, 2.74], [15.01, 2.93],
  [15.04, 3.08], [15.06, 3.23], [15.08, 3.36], [15.10, 3.44]
stern_m:
  [-13.08, -3.86], [-13.60, -2.24], [-13.80, -1.63], [-13.99, -1.03], [-14.19, -0.43],
  [-14.34, 0.02], [-14.48, 0.48], [-14.68, 1.08], [-14.77, 1.38], [-14.83, 1.59], [-14.90,
  1.65], [-15.40, 1.90], [-15.89, 2.10], [-15.96, 2.20], [-15.95, 2.41], [-16.01, 2.56],
  [-16.06, 2.71], [-16.12, 2.86], [-16.17, 3.01], [-16.23, 3.16], [-16.28, 3.31], [-16.33,
  3.46], [-16.40, 3.58], [-16.47, 3.68]
wales_m:
  [-14.21, 1.10, 1.75], [-12.84, 0.96, 1.60], [-12.19, 0.90, 1.54], [-10.89, 0.78, 1.42],
  [-9.61, 0.68, 1.32], [-8.34, 0.59, 1.23], [-7.04, 0.51, 1.15], [-5.76, 0.45, 1.09], [-4.49,
  0.40, 1.04], [-3.19, 0.36, 1.00], [-1.92, 0.34, 0.98], [-0.64, 0.33, 0.97], [0.65, 0.34,
  0.98], [1.82, 0.35, 0.99], [2.98, 0.38, 1.01], [4.26, 0.42, 1.05], [5.54, 0.47, 1.11],
  [6.81, 0.54, 1.18], [8.09, 0.62, 1.26], [9.38, 0.73, 1.37], [10.65, 0.85, 1.49], [11.93,
  0.99, 1.63], [13.21, 1.15, 1.78], [13.98, 1.25, 1.90], [14.29, 1.29, 1.94]
section_m:
  [-2.89, 0.18], [-2.73, 0.39], [-2.58, 0.67], [-2.28, 1.36], [-1.97, 2.12], [-1.67, 2.75],
  [-1.36, 3.20], [-1.06, 3.53], [-0.75, 3.77], [-0.45, 3.96], [-0.14, 4.09], [0.16, 4.19],
  [0.47, 4.25], [0.77, 4.27], [0.86, 4.26], [1.08, 4.27], [1.38, 4.27], [1.69, 4.25], [1.99,
  4.22], [2.29, 4.19], [2.57, 4.16]
decks_m.upper:
  [-14.69, 1.67], [-14.48, 1.67], [-12.84, 1.55], [-12.19, 1.51], [-10.89, 1.44], [-9.61,
  1.37], [-8.34, 1.31], [-7.04, 1.27], [-5.76, 1.23], [-4.49, 1.19], [-3.19, 1.17], [-1.92,
  1.16], [-0.64, 1.15], [0.65, 1.16], [1.82, 1.18], [2.98, 1.19], [4.26, 1.22], [5.54, 1.26],
  [6.81, 1.31], [8.09, 1.37], [9.38, 1.44], [10.65, 1.52], [11.93, 1.61], [13.21, 1.71],
  [14.48, 1.87]
ports_m.upper, the sheet's, as §5.7:
  [-11.55, 1.89, 3.40], [-8.98, 1.76, 3.73], [-6.41, 1.66, 3.97], [-3.84, 1.60, 4.13], [-1.28,
  1.57, 4.21], [1.29, 1.58, 4.25], [3.90, 1.62, 4.21], [6.46, 1.70, 4.14], [9.00, 1.83, 3.83],
  [11.57, 1.99, 3.05]
ports_m.upper, the brig's file, each port with a gun in it at the gun's x:
  [-11.55, 1.89, 3.40], [-9.10, 1.77, 3.71], [-6.50, 1.66, 3.96], [-3.90, 1.60, 4.13], [-1.30,
  1.57, 4.21], [1.30, 1.58, 4.25], [3.90, 1.62, 4.21], [6.50, 1.70, 4.14], [9.10, 1.84, 3.80],
  [12.00, 2.02, 2.87]
ports_m.upper, the merchant brig's file, the same but her own two guns' ports:
  [-11.55, 1.89, 3.40], [-9.10, 1.77, 3.71], [-6.50, 1.66, 3.96], [-4.00, 1.60, 4.12], [-1.30,
  1.57, 4.21], [1.30, 1.58, 4.25], [4.00, 1.62, 4.21], [6.50, 1.70, 4.14], [9.10, 1.84, 3.80],
  [12.00, 2.02, 2.87]
port_size_m.upper: [0.84, 0.70]
head_m:
  [12.21, -3.03], [12.50, -2.94], [12.81, -2.77], [13.01, -2.62], [13.30, -2.30], [13.52,
  -1.99], [13.72, -1.68], [13.90, -1.37], [14.07, -1.06], [14.24, -0.75], [14.42, -0.44],
  [14.68, 0.01], [15.00, 0.49], [15.37, 0.96], [15.87, 1.43], [16.31, 1.75], [16.70, 2.07],
  [16.95, 2.38], [17.08, 3.06], [17.18, 3.58], [16.95, 3.77]
breadth_line_m:
  [-12.84, 1.48, 3.20], [-12.19, 1.42, 3.31],
  [-10.89, 1.24, 3.51], [-9.61, 1.11, 3.67], [-8.34, 1.00, 3.81], [-7.04, 0.92, 3.93], [-5.76,
  0.85, 4.03], [-4.49, 0.81, 4.11], [-3.19, 0.79, 4.17], [-1.92, 0.78, 4.22], [-0.64, 0.79,
  4.24], [0.65, 0.82, 4.25], [1.82, 0.86, 4.26], [2.98, 0.90, 4.25], [4.26, 0.96, 4.23],
  [5.54, 1.06, 4.18], [6.81, 1.21, 4.08], [8.09, 1.35, 3.94], [9.38, 1.55, 3.72], [10.65,
  1.79, 3.39], [11.93, 2.09, 2.90], [13.21, 2.45, 2.14], [13.98, 2.71, 1.40]
rabbet_m:
  [-12.78, -3.36, 0.10], [-10.89, -3.31, 0.10], [-5.76, -3.14, 0.10], [-0.64, -2.97, 0.10],
  [1.82, -2.89, 0.10], [4.26, -2.81, 0.10], [6.81, -2.72, 0.10], [9.38, -2.64, 0.10], [10.73,
  -2.59, 0.10], [11.56, -2.36, 0.15], [12.21, -2.03, 0.15], [12.68, -1.71, 0.15], [13.04,
  -1.40, 0.15], [13.33, -1.08, 0.15], [13.58, -0.77, 0.15], [13.78, -0.46, 0.15], [13.95,
  -0.15, 0.15], [14.01, -0.01, 0.15], [14.21, 0.47, 0.15], [14.39, 1.08, 0.15], [14.55, 1.70,
  0.15], [14.71, 2.39, 0.15], [14.79, 2.94, 0.15], [14.86, 3.39, 0.15]
```

`sections_m`, by station, aft to forward, each point `[x, z, half-breadth]`: at low levels off the
body plan (0.5, 1, 2, 3 ft above the rabbet, where they stand below WL4), then WL4, WL3, WL2 and WL1
off the half-breadth plan at the sheer's heights, at 23 and 22 with the body plan's two whole-foot
levels between WL2 and WL1 (§6.1), then at stations 23 to 18 and H to S the body plan's whole-foot
levels between WL1 and the main breadth (§6.1), then the main breadth and the rail. S, with no WL3 or
WL4, starts from its lowest cell of §5.11:

```
  23 [-12.84, -3.22, 0.15], [-12.84, -3.07, 0.15], [-12.84, -2.76, 0.15], [-12.84, -2.18, 0.16], [-12.84, -1.45, 0.25], [-12.84, -0.73, 0.46], [-12.84, -0.63, 0.53], [-12.84, -0.32, 0.86], [-12.84, 0.00, 1.37], [-12.84, 0.29, 2.09], [-12.84, 0.59, 2.71], [-12.84, 0.90, 3.02], [-12.84, 1.20, 3.16], [-12.84, 1.48, 3.20], [-12.84, 3.16, 3.07]
  22 [-12.19, -3.20, 0.17], [-12.19, -3.04, 0.18], [-12.19, -2.74, 0.20], [-12.19, -2.18, 0.22], [-12.19, -1.45, 0.39], [-12.19, -0.73, 0.76], [-12.19, -0.61, 0.91], [-12.19, -0.30, 1.37], [-12.19, 0.00, 1.93], [-12.19, 0.31, 2.62], [-12.19, 0.61, 3.01], [-12.19, 0.92, 3.20], [-12.19, 1.22, 3.29], [-12.19, 1.42, 3.31], [-12.19, 3.10, 3.19]
  20 [-10.89, -3.15, 0.18], [-10.89, -3.00, 0.20], [-10.89, -2.70, 0.24], [-10.89, -2.39, 0.31], [-10.89, -2.18, 0.37], [-10.89, -1.45, 0.73], [-10.89, -0.73, 1.48], [-10.89, 0.00, 2.78], [-10.89, 0.35, 3.21], [-10.89, 0.66, 3.39], [-10.89, 0.96, 3.48], [-10.89, 1.24, 3.51], [-10.89, 2.98, 3.39]
  18 [-9.61, -2.18, 0.55], [-9.61, -1.45, 1.15], [-9.61, -0.73, 2.17], [-9.61, 0.00, 3.24], [-9.61, 0.39, 3.50], [-9.61, 0.70, 3.62], [-9.61, 1.00, 3.67], [-9.61, 1.11, 3.67], [-9.61, 2.88, 3.56]
  16 [-8.34, -3.07, 0.21], [-8.34, -2.92, 0.26], [-8.34, -2.61, 0.42], [-8.34, -2.31, 0.64], [-8.34, -2.18, 0.76], [-8.34, -1.45, 1.63], [-8.34, -0.73, 2.71], [-8.34, 0.00, 3.52], [-8.34, 1.00, 3.81], [-8.34, 2.80, 3.70]
  14 [-7.04, -2.18, 0.98], [-7.04, -1.45, 2.07], [-7.04, -0.73, 3.09], [-7.04, 0.00, 3.72], [-7.04, 0.92, 3.93], [-7.04, 2.72, 3.82]
  12 [-5.76, -2.83, 0.37], [-5.76, -2.53, 0.71], [-5.76, -2.18, 1.20], [-5.76, -1.45, 2.43], [-5.76, -0.73, 3.35], [-5.76, 0.00, 3.85], [-5.76, 0.85, 4.03], [-5.76, 2.66, 3.92]
  10 [-4.49, -2.79, 0.43], [-4.49, -2.49, 0.89], [-4.49, -2.18, 1.40], [-4.49, -1.45, 2.69], [-4.49, -0.73, 3.53], [-4.49, 0.00, 3.95], [-4.49, 0.81, 4.11], [-4.49, 2.61, 4.00]
  8  [-3.19, -2.75, 0.51], [-3.19, -2.44, 1.03], [-3.19, -2.17, 1.55], [-3.19, -1.45, 2.87], [-3.19, -0.73, 3.64], [-3.19, 0.00, 4.02], [-3.19, 0.79, 4.17], [-3.19, 2.57, 4.07]
  6  [-1.92, -2.71, 0.58], [-1.92, -2.40, 1.17], [-1.92, -2.17, 1.62], [-1.92, -1.45, 2.98], [-1.92, -0.73, 3.71], [-1.92, 0.00, 4.07], [-1.92, 0.78, 4.22], [-1.92, 2.55, 4.11]
  4  [-0.64, -2.66, 0.63], [-0.64, -2.36, 1.27], [-0.64, -2.17, 1.65], [-0.64, -1.45, 3.04], [-0.64, -0.73, 3.75], [-0.64, 0.00, 4.10], [-0.64, 0.79, 4.24], [-0.64, 2.54, 4.13]
  2  [0.65, -2.17, 1.66], [0.65, -1.45, 3.07], [0.65, -0.73, 3.76], [0.65, 0.00, 4.12], [0.65, 0.82, 4.25], [0.65, 2.55, 4.15]
  ⊗  [1.82, -2.73, 0.39], [1.82, -2.58, 0.67], [1.82, -2.17, 1.63], [1.82, -1.45, 3.05], [1.82, -0.73, 3.75], [1.82, 0.00, 4.12], [1.82, 0.86, 4.26], [1.82, 2.57, 4.16]
  B  [2.98, -2.17, 1.56], [2.98, -1.45, 2.98], [2.98, -0.73, 3.73], [2.98, 0.00, 4.11], [2.98, 0.90, 4.25], [2.98, 2.59, 4.15]
  D  [4.26, -2.17, 1.41], [4.26, -1.45, 2.85], [4.26, -0.73, 3.66], [4.26, 0.00, 4.07], [4.26, 0.96, 4.23], [4.26, 2.64, 4.13]
  F  [5.54, -2.46, 0.61], [5.54, -2.17, 1.21], [5.54, -1.45, 2.65], [5.54, -0.73, 3.52], [5.54, 0.00, 3.98], [5.54, 1.06, 4.18], [5.54, 2.70, 4.09]
  H  [6.81, -2.57, 0.33], [6.81, -2.42, 0.56], [6.81, -2.17, 0.97], [6.81, -1.45, 2.36], [6.81, -0.73, 3.29], [6.81, 0.00, 3.82], [6.81, 0.33, 3.98], [6.81, 0.63, 4.07], [6.81, 0.94, 4.11], [6.81, 1.21, 4.08], [6.81, 2.77, 4.02]
  K  [8.09, -2.38, 0.49], [8.09, -2.17, 0.74], [8.09, -1.45, 2.00], [8.09, -0.73, 2.97], [8.09, 0.00, 3.57], [8.09, 0.37, 3.80], [8.09, 0.67, 3.89], [8.09, 0.98, 3.95], [8.09, 1.35, 3.94], [8.09, 2.86, 3.90]
  M  [9.38, -2.49, 0.25], [9.38, -2.33, 0.40], [9.38, -2.16, 0.53], [9.38, -1.45, 1.57], [9.38, -0.72, 2.52], [9.38, 0.00, 3.21], [9.38, 0.11, 3.32], [9.38, 0.41, 3.49], [9.38, 0.72, 3.61], [9.38, 1.02, 3.69], [9.38, 1.33, 3.74], [9.38, 1.55, 3.72], [9.38, 2.96, 3.72]
  O  [10.65, -2.29, 0.29], [10.65, -2.17, 0.34], [10.65, -1.45, 1.10], [10.65, -0.73, 1.94], [10.65, 0.00, 2.68], [10.65, 0.15, 2.83], [10.65, 0.45, 3.03], [10.65, 0.76, 3.19], [10.65, 1.06, 3.30], [10.65, 1.37, 3.37], [10.65, 1.67, 3.41], [10.65, 1.79, 3.39], [10.65, 3.09, 3.40]
  Q  [11.93, -2.16, 0.18], [11.93, -1.45, 0.60], [11.93, -0.73, 1.24], [11.93, 0.00, 1.92], [11.93, 0.19, 2.10], [11.93, 0.49, 2.34], [11.93, 0.80, 2.54], [11.93, 1.10, 2.69], [11.93, 1.41, 2.80], [11.93, 1.71, 2.87], [11.93, 2.09, 2.90], [11.93, 3.23, 2.95]
  S  [13.21, -0.99, 0.28], [13.21, -0.72, 0.45], [13.21, 0.00, 0.93], [13.21, 0.23, 1.12], [13.21, 0.54, 1.33], [13.21, 0.84, 1.53], [13.21, 1.15, 1.72], [13.21, 1.45, 1.88], [13.21, 1.76, 2.00], [13.21, 2.06, 2.07], [13.21, 2.45, 2.14], [13.21, 3.39, 2.22]
```

`form` and `marks`:

```
form:
  stern:
    type: square
    knuckle_z_m: 0.99
    transom_hb_m: [2.33, 2.93]
    round_up_m: 0.13
  head: scroll
marks:
  rail_m, breadth_m, stem_m, stern_m, wales_m, section_m, port_size_m, head_m,
  breadth_line_m, sections_m, form.stern, form.stern.knuckle_z_m, form.stern.transom_hb_m,
  form.stern.round_up_m, form.head: sourced
  keel_m, decks_m, ports_m, rabbet_m: judged
```

### 6.3 Plainly

- **`stern_m`'s top and `rail_m`'s first point** are the taffrail at the middle line (§5.6), one
  point. The horns, 0.32 ft above that, are not in the rail: at their place, -5.8 to -5.0 ft, the
  drawn top of the side stands about 0.66 ft (0.20 m) under them, a small hump the sheet has abeam and
  the drawing has not (measured). Left for the owner's eye.
- **`rail_m`** ends at the rail's moulded end, abaft `stem_m`'s top, the stem head (`Build-Ships.md`
  §5.1 allows it).
- **`knuckle_z_m`** is the wing transom's ends, as the 64's; **`transom_hb_m`** the moulded
  taffrail's and the knuckle's, each + plank. Straight between them `form.py` gives 8.95 ft at the
  counter's upper rail against the moulded 8.55 and, with the quarter piece, 9.55 ft: between the
  two.
  `round_up_m` is the wing transom's.
- **No `lights_m`:** the two stern ports are ports, 81's, the only openings on the stern board, with
  no window on it; the viewer's light marks would also spread them evenly across the face, not where
  the sheet has them. `Build-Ships.md` §5.7's "no galleries or lights" stands as read, and §5.6 keeps
  the ports' places for 81.
- **The marks.** Rung S throughout, her class's own lines; by §5.0 principle 4 a line takes the word
  of its weakest point, so four lines are `judged`, as the 64's are for the like reasons: `keel_m`
  (that the strip's border is K, §5.4), `decks_m` (the plank added to the third red line, itself
  identified by judgement: §5.1), `ports_m` (the half-breadths at the sills; a gun's port at the
  gun's x) and `rabbet_m` (the half-sidings between their two places). **Old beside new, at the
  landing:** `keel_m` was first `sourced`, the 64's K being so on the same kind of judgement; the
  64's stands, her bytes not moving.
- **`decks_m.upper`** is the third red line + 0.24 ft (§5.1). `deck_height_m` is not moved.
- **`ports_m.upper`:** no gun's `x_m` moves (`Build-Ships.md` §5.3) and each port gun stands on a
  triple of its deck within 0.01 m (truth 7-185), so a port with a gun in it is written at the gun's
  x, its sill and half-breadth read along the sheet's ten there. The sheet's own centres stand in
  §5.7 and in the module. Off them: the eight by 0.12, 0.09, 0.06, 0.02, 0.01, 0.00, 0.04 and 0.10
  m; the merchant brig's two by 0.16 and 0.10 m. **The chase port** is written at the gun's +12.0,
  0.43 m before port 10's centre, on the port's fore edge: beyond the sheet's last port, so its sill
  is port 10's + the deck's rise there, 2.02 m (judgement, §5.7's parallel sills), and its
  half-breadth off the body plan between Q and S at that height, 2.87 m (±0.03). Port 1 holds no gun
  in either file and stands at the sheet's x. Each gun's `height_m` is its triple's sill and its
  `deck` is `upper` (`Build-Ships.md` §5.3; §7: L1, no reader until L2).
- **No `channel_wales_m`:** the band through the ports (§5.1) is no channel wale by anything on the
  sheet, a moulding by judgement, and drawn under that key it showed only as two dark stubs beyond
  the viewer's band through the ports (seen on the drawn sheets). It stands 1.12 and 1.48 ft under
  the plank-sheer line of §5.2, if a later viewer wants it.
- **`breadth_line_m`** starts at section 23. The plan and the sheer carry it on abaft the post at the
  water, to [-14.48, 1.80, 2.86] and [-15.53, 2.06, 2.61], and those two are not written: `form.py`
  makes every x of the line a station drawn down to the water, which drew a box under the counter
  abaft the post, where the sheet has the rudder (seen on the drawn sheets; `form.py` is not this
  step's to change, and the 64's line stops at AP, forward of her post). The transom's half-breadths
  and the rail close the side there, within 0.12 m of those two.
- **`rabbet_m`** is reserved and not drawn; half-sidings 0.34 ft in the keel, 0.48 ft on the stem
  (read at their two places, judgement between).
- **`floor_m`, `form.fullness`, `galleries_m`** are not given: no rising line on the sheet; the ends
  are drawn through her waterlines; no galleries.
- **`port_size_m`** the mean of the ten (§5.7).
- **`sections_m`** at stations 2 and B come off the plan and the sheer alone. Between the body
  plan's low points and WL4, and between WL1 and the upper points at H to S, the fore body's 0.05 to
  0.2 ft stands (§5.11).

## 7. Against the files (recorded, not moved)

`data/ships/brig.yaml` and `merchant-brig.yaml` give one hull to the byte in these figures (read:
`hull` compared). Where the merchant brig differs in detail the existing code decides: her four long
6-pounders stand at x ±4.0, near ports 4 and 7 (-3.84 and +3.90 m), her ports painted, by her
description.

| Field | The file (its note) | The sheets |
|---|---|---|
| `length_waterline_m` | 26.8 (88 ft, judgement) | WL1 91.86 ft moulded (28.00 m); 95.2 ft (29.02 m) from the post's after edge to the knee's fore edge |
| `beam_m` | 8.6 (28 ft 1½ in, *Harpy* as built, rounded) | class 28 ft 0 in extreme (8.53 m); 27 ft 6 in moulded (8.38 m) |
| `draught_m` | 3.5 (11.5 ft mean, judgement) | WL1 to K 11.25 ft at the middle (3.43 m), 9.69 and 12.80 ft; WL1 to the main keel 10.83 ft. Winfield p. 256's 7 ft 3 in / 10 ft 10 in near WL2 (§4.3) |
| drag | 2 ft (judgement) | 3.11 ft in the 95 ft (§4.3) |
| `deck_height_m` | 1.5 (5 ft, judgement) | the plank at the middle line 4.51 ft (1.38 m), the deck at side 3.80 ft (1.16 m) at the middle |
| guns' `height_m` | 2.1 (deck + `PORT_SILL_M`): **now written** from the triples, with `deck: upper`, as `Build-Ships.md` §5.3 and §7's L1 have it (no reader until L2) | sills 1.57 m (port 5) to 1.99 m (port 10). At the eight's x, from forward: 1.84, 1.70, 1.62, 1.58, 1.57, 1.60, 1.66, 1.77 m; the chase guns 2.02 m; the merchant brig's 1.62 and 1.60 m |
| guns' `x_m`, the eight a side | +9.1, 6.5, 3.9, 1.3, -1.3, -3.9, -6.5, -9.1 | ports 9 to 2 at +9.00, 6.46, 3.90, 1.29, -1.28, -3.84, -6.41, -8.98: off by 0.10, 0.04, 0.00, 0.01, 0.02, 0.06, 0.09, 0.12 m |
| guns' `x_m`, the two chase guns | +12.0 | port 10 at +11.57, the gun on its fore edge |
| `displacement_kg` | 413,000 (Cb judgement) | about 303 t drawn to WL1 (`form.py`), 302 to 307 by the stations (moulded, with plank and keel), about 184 at WL2; -27% |
| `fore.mast` `x_m`, `rake_deg` | +8.9, 1.2 | +9.62 (ZAZ4492, +9.62), to WL1 2.5°; green 1799 +9.37 |
| `main.mast` `x_m`, `rake_deg` | -3.9, 4.0 | -3.96 (-3.94); to WL1 3.0°; green 1799 -4.07 |
| `bowsprit` | `x_m` 13.4, `height_m` 4.5 | root at the stem head, +15.10 m, 3.44 m; steeved 15.7° to WL1 (§5.5) |
| `rudder` | blade 12 ft by 3 ft (`span_m` 3.7, judgement) | the blade 17.9 ft up the post from K to the counter, 2.5 to 3.8 ft broad (§5.6) |
| `what`, the description | "a brig-sloop of war, sixteen ports a side" | ten a side (read). See below |
| the era note | "Hull from the kit's manual (Winfield and the Greenwich draught not reached)" | now reached: mended in the generator, with the `beam_m` note (no behaviour reads either) |

**The word "sixteen" (a report).** `tools/gen_ships.py` (`brig()`, `b.descriptions`) writes it to
`data/ships/brig.yaml`. A pin holds it, so it is reported and not mended:
- The file's `what` is the words the world says (`world/ships.py`, `description`): the order's "put
  on the sea" line (`world/orders.py:675`) and the lookout's `lookout.made_out` (`world/lookout.py`).
- `tests/test_captain_trials.py`'s `TRIAL_STATION_STRANGER_DIGEST` (:82, asserted :110) holds them:
  `Log.digest` hashes each event's words, and that trial puts a brig-sloop on the sea by the
  scenario's order and makes her out (read; `docs/playtests/2026-10-11-gate-m6a-owner-runs/saves/
  trial-station-stranger-chase-complete.json` keeps the order's words; not run). The fixed digests of
  `tests/test_known_truths.py` (:2524 to :4875) may hold them too, for the fast tier to name.
- `freesail/world/ships.py:192`, a second copy in `DESCRIPTIONS`, in the same words, and
  `freesail/world/captains.py:329`, a docstring.
- `tests/test_profile.py:938` gives the string to `captains.size_of_words` as a literal: not a pin on
  the count (it reads the words before the first comma), but the same words.
- `docs/primer/15-other-sail.md:7` and `:47`, in the served primer; `docs/dev/TuningNotes.md`,
  `docs/gates/gate-m5c.md` and old saves in `docs/playtests/` as records.

So mending it moves two code copies, a test's literal, the primer and those digests at once, with no
behaviour meant, for the landing to take as one word.

**Truth 7-185 and §5.4's band (ruled, the lead, 2026-10-31).** §6.2's triples stand at the guns' x, so
7-185's "every port gun's `(x_m, height_m)` on a triple of its deck within 0.01 m" holds with no gun
moved; the price is the file's ten centres off the sheet's as §6.3 lists, as built by the lead's point
5. The lowest sill, 1.57 m, stands 0.05 m above §5.4's first band of 1.22-1.52 m (Steel p. 124, rung R);
the sheet is rung S and decides (§5.0 principle 12). **Truth 7-185's band, old beside new: old
1.22-1.52 m, Steel p. 124's four to five feet; new 5 ft 2 in ±0.05 ft, 1.555-1.585 m, on this sheet**
(`tests/test_profiles.py`), the one pin this step moves, and `Build-Ships.md` §5.4 is re-sourced to it.

**The sills, for L2 (`Build-Ships.md` §5.4, §7):** on §5.4's reckoning (heel alone, half the beam,
`PORT_SHUT_M`) the sill of 1.57 m shuts at 17.1° against the file's 24.7°, and 1.99 m at 23.1°; the
sheet stands just above Steel's band of 12.3 to 16.4°. On §7.1's own rule, with each triple's
half-breadth, the ports at x ±1.3 shut first, at 17.5°, then -3.9 and +3.9 at 18.3° and 18.2°, ±6.5
at about 20°, ±9.1 at about 24°, the chase port at 36.7°. Reported only, before L2 reads them.

These are for the lead and the owner. This step moves no figure the physics or the gunnery reads.

## 8. What the sources cannot give

- **Which waterline she floated at** for certain: no line is labelled, the sheets have no draught
  marks, Winfield's draughts are not said to be at load, and the faint ruled line above WL1 is not
  explained (§4.1, §4.2, §4.3). WL1 stands by the lead's ruling, on the judgement of §4.2.
- **What state Winfield's draught** was taken in; the contracts ADT0015 and ADT0029 are manuscript
  and were not read.
- **The floors' rising line** (§5.4): not drawn. The diagonals are drawn in the body plan and were
  not read: the waterlines and sections serve.
- **The sections at stations 2 and B**, and D above about 12 ft: not separately drawn (§5.11).
- **The cant frames** in red on the plan were not read: no line of the form wants them.
- **The sweep ports' and the ports' lids, the paint**: outlines only, no colour but the inks.
- **The sisters' as-built changes:** "as all the Brigs were built" speaks only of the fore channel's
  dead-eyes; ZAZ4626, the sheer draught of the eight, is at RMG only and was not reached.
- **The Fir ships' timbers:** in ticked lines on the sheet (§2.3), not *Harpy*'s, oak-built by the
  catalogue, and not read.

## 9. Method and files

The images were read with crops and enlargements, and measured by scripts kept outside the
repository in the session's scratch directory, under `hulls/streams/brigs/`: `lib.py` (loads the
cached sheets, crops), `strip.py` and `strip92b.py` (the strips), `vprof.py` and `kscan.py` (peaks
by columns and rows, to sub-pixel by darkness centroids), `track.py`, `trace91.py`, `trace91b.py`,
`trace91c.py`, `trace_hb.py`, `trace_ends.py`, `trace92.py` (the lines, followed along their ink,
black, red or green apart), `trace_body.py`, `bracket.py`, `fillbody2.py`, `clean_sections.py` (the
sections, those crowded between their neighbours), `model.py` and `model92.py` (the sheets'
coordinates), `compile91.py`, `railfix.py`, `final.py`, `note_data.py` (the tables), `ports91.py`,
`ports92.py`, `xc92.py`, `masts.py`, `masts2.py`, `sternboard.py`, `sis2.py`, `sis3.py` (the sheets
against each other), `checker.py`, `xcheck2.py` (the checker), `hydro.py` (the integration),
`profile_json.py` (§6's first points, and the run through the tree's helpers) and `ov.py` (the traced
lines drawn back on the image and looked at). Each reads the cached image through `lib.py`. No crop
or trace is in the repository. The points as built are `tools/ships/hull_brig.py`'s, read against
§6.2 by `tests/test_hull_brig.py`; the drawn sheets beside the sheet's crops are in the same scratch
directory, under `sheets/`, and an overlay of the file's outlines on the sheer, the plan and the body
plan, made by the review with its own script, under `review/`.
