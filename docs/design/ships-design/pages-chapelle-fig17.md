# Pages: Chapelle 1930, fig. 17 and its plates, H.M. schooner *Musquidobit*, late *Lynx* (October 2026)

Stage 0 research for package 75, the page named by `Build-Ships.md` §19.1 item 11 and by the
shared draft (`ships-design/shared-design.md` §1.5, the schooners' row at line 201; §5). It
serves `data/ships/topsail-schooner.yaml` and `data/ships/privateer-schooner.yaml`, both built
on *Lynx*'s draught by `topsail_schooner()` and `privateer_schooner()` in `tools/gen_ships.py`,
and the builder B8, who draws a sourced hull profile for each (`Build-Ships.md` §5). Their
sills are already sourced to *Spider* (Chapelle pp. 166-167; `gen_ships.py:4152-4156` at
99a91b8); §5.4 measures the plates against that. Facts only: the images are kept outside the
repository (§1.1).

The marks:

- **read**: the page's printing or drawing was seen on the image. "read (OCR)" is the held
  text layer only. "tentative" is a reading at the limit of the image.
- **measured**: off the image at the scale of §3; the uncertainty is stated.
- **judgement**: reasoning by this note.

**Units and datums.** English feet and inches, with metres in brackets. Along the ship, "ft
from AP" is measured along the keel as drawn, from **AP**, the after of the two dashed
perpendiculars drawn on the sheer plan, whose distance apart is the length on deck (§3.2).
The draught is drawn with the keel level and the waterline at **3.72°** to it (the drag, §4),
so for the profile the frame is turned to the water: **`x`** is measured along the drawn load
water line (LWL) from the point where the mid-perpendicular meets it, positive forward, and
**`z`** square to that line, positive up. On this frame AP and FP fall at x = ∓14.47 m. A
point above the line lies aft of its station by z·0.065 (0.12 m at the rail); every `x` in §6
is the point's own. Half-breadths are moulded, to the outside of the frames; the plank adds
about 2 in a side (the stated extreme breadth less the moulded, halved: read, arithmetic).

## 0. In brief

- **Fig. 17 is the body plan alone** (p. 83, read). The sheer and half-breadth plan, with
  the draught's title, table of dimensions and a scale, and the longitudinal section with
  the deck plan, are two unnumbered plates after p. 83 (IA leaves 108 and 109). All three are
  Chapelle's redrawings of the Admiralty draught taken off at Portsmouth in May 1816, the
  inboard and outboard profiles separated (preface p. v, read (OCR) l. 73-76; the sheer plate
  signed "Chapelle 29", read, tentative on the digits).
- **The scale checks.** The plate's ruled bar gives 28.36 px to the foot over 97 ft; the
  moulded half-breadth measures 11 ft 10.1 in against the stated 23 ft 8 in moulded (+0.1%),
  and the perpendiculars stand 94 ft 9 in apart against the stated 94 ft 7 in on deck (+0.2%)
  (§3).
- **The load water line is drawn**: the one waterline carried past both ends of the sheer
  plan; the inboard plate marks the same line at its ends with the water sign, and the two
  agree within 1 in amidships (§4). **Draught** to the keel's lower edge: **12 ft 10 in at the
  heel of the post, 8 ft 8 in at the forefoot**, mean 10 ft 9 in (3.28 m), against the files'
  3.3 m.
- **The side.** The rail's top stands 6 ft 1½ in (1.87 m) above the line at its lowest, just
  abaft the middle, 8 ft 0 in (2.44 m) at the taffrail and 8 ft 10 in (2.70 m) at the stem
  head; the bulwark is about 3 ft from the rail's top to the sill line throughout. **Seven
  ports a side**, cut from the sill line to the rail, 2 ft 1 in wide; sills 3 ft 1 in to 5 ft
  0 in above the line, the lowest, 0.95 m, at port 3 just before the main mast (§5).
- **Against *Spider*** (§5.4): *Spider*'s 3 ft 5 in amidships stands 3 to 4 in above *Lynx*'s
  midship sills; her ends (3 ft 7 in aft, 4 ft 7 in forward) lie below *Lynx*'s (3 ft 11 in,
  5 ft 0 in), the drag giving *Lynx* more freeboard at the ends.
- **Half-breadths**: 11 ft 10 in at the sill line and 11 ft 5 in at the water at the
  broadest, about 2 m forward of the middle; the rail tumbles home about 2 in amidships and
  flares out up to 1.1 ft in the bow. A midship section from the body plan, deadrise about 28°
  (§5.6).
- **The deck** is flush; at the middle line it lies within 2 in of the sill line from the
  stern to the fore mast and 5 to 7 in below it in the bow. Its round up is not drawn (§5.5).
  **No wale is drawn** (§8).
- **Against the files** (§7, recorded, not moved): the line is 88 ft rabbet to rabbet (26.84
  m) against the files' 85 ft (25.9 m); the sills 0.95 to 1.53 m against 1.04 m at every port;
  the rail 1.87 to 2.3 m against the swivels' 1.7 m; the fore mast at +8.27 m against +7.8 m.

## 1. The source

### 1.1 The book, the images and the cache

| | |
|---|---|
| Work | Howard I. Chapelle, *The Baltimore Clipper: Its Origin and Development*, Salem, Mass.: Marine Research Society, 1930; the held OCR is `docs/references/chapelle/chapelle-1930-the-baltimore-clipper-ocr.txt` |
| Copy scanned | Internet Archive item `baltimoreclipper00howa`, https://archive.org/details/baltimoreclipper00howa : the Bonanza Books (New York) reprint, whose imprint page gives the copyright as 1930, the Marine Research Society's, and Library of Congress card 76-27148 (read (OCR) l. 41-52). Scanned 2013 at 350 ppi, 234 leaves (metadata) |
| Rights shown | None. The item page and its metadata carry no rights, licence or copyright-status field; the item is in the open `internetarchivebooks` collection and its files download without a loan (fetched 2026-10-28). Published in the United States in 1930, in the public domain there from 1 January 2026 (judgement: 95 years; as `docs/references/README.md:12` says). The reprint adds nothing to the plates (judgement) |
| Leaves used | Leaf 107, p. 83, fig. 17 (body plan); leaf 108, unnumbered plate (the draught's sheer and half-breadth plans); leaf 109, unnumbered plate (longitudinal section and deck plan); leaves 202-204, pp. 166-168 (*Spider* and the class specification). In the online reader these are `page/n105` to `n107` and `n200` to `n202` (the reader skips two leaves) |
| Images used | The processed page images, 2756 x 3715 px each, from the item's `_jp2.zip`: https://archive.org/download/baltimoreclipper00howa/baltimoreclipper00howa_jp2.zip/baltimoreclipper00howa_jp2%2Fbaltimoreclipper00howa_0107.jp2 and the same with `_0108`, `_0109`, `_0202`, `_0203`, `_0204` |
| Also fetched | The camera original of leaf 108, 5616 x 3744 px: https://archive.org/download/baltimoreclipper00howa/baltimoreclipper00howa_orig_jp2.tar/baltimoreclipper00howa_orig_jp2%2Fbaltimoreclipper00howa_orig_0108.jp2 (viewed, not measured). Previews https://archive.org/download/baltimoreclipper00howa/page/n104_w700.jpg to `n109_w700.jpg` (finding the leaves). Metadata: https://archive.org/metadata/baltimoreclipper00howa , `.../download/baltimoreclipper00howa/baltimoreclipper00howa_page_numbers.json`, `..._scandata.xml`, and the item page |
| Cache | `D:/Projects/FreeSail/reference-cache/chapelle-fig17/`: `leaf0107/`, `leaf0108/`, `leaf0109/` (one JP2 each), `orig-leaf0108/`, `spider-pp166-168/` (three JP2s), `previews/` (`n104_w700.jpg` to `n109_w700.jpg`), `meta/` (`metadata.json`, `page_numbers.json`, `scandata.xml`, `details.html`). Fetched 2026-10-28 with a generic user-agent |

### 1.2 What is on the pages (read)

- **Leaf 107, p. 83, fig. 17**, captioned as the lines of H.M. schooner *Musquidobit*: the
  body plan, the after body on the left with the transom and one of its two ports, the fore
  body on the right; dashed lines at the moulded breadth and the base; the keel below.
- **Leaf 108**, printed sideways (bow to the right once turned): the sheer plan with the rail,
  the sill line (planksheer), seven ports, the main channel with three deadeyes and the fore
  with four, two mast stumps raking aft, the bowsprit's stump, the hawse bolster, the rudder
  with three pintle straps, 24 stations square to the keel, three waterlines, the keel, and
  two dashed perpendiculars joined by a dashed base along the keel; a ruled bar (§3.1);
  the half-breadth plan below it, with the outer lines, three waterlines and the stations;
  the title, the table of dimensions (§2) and the signature.
- **Leaf 109**, captioned as the longitudinal section and deck plan, as taken off at
  Portsmouth Yard, May 1816: the inboard works (the deck and its beams, a platform about 5 ft
  below it amidships, hatches, capstan, pumps, bitts, the keelson, the masts stepped on it),
  the dashed stations and perpendiculars, and a short water line with the water sign under
  it beyond each end; the deck plan below. No scale is drawn on it.
- **Not drawn** on any of the three: no wale; no draught marks or figures; no station
  numbers; no sweep ports; no spars aloft (Chapelle: the spar dimensions are not to be found,
  p. 82, read (OCR) l. 4832-4833).

## 2. The title and the dimensions (read)

The plate's title calls her a draught of His Majesty's schooner *Musquidobit*, formerly the
*Lynx* privateer. Its table, read on the image (each figure as in the text, p. 82, OCR
l. 4826-4829):

| Dimension | Stated |
|---|---|
| Length on deck | 94 ft 7 in |
| Length of keel for tonnage | 73 ft 1¼ in |
| Breadth extreme | 24 ft 0 in |
| Breadth moulded | 23 ft 8 in |
| Depth of hold | 10 ft 3 in |
| Burthen in tons | 223 91/94 |

The plate gives no draughtsman; the text names N. S. Diddams at Portsmouth (p. 82, OCR
l. 4829). The plates spell her *Musquidobit*, the text *Mosquidobit*.

## 3. The scale and its check

### 3.1 The bar (measured)

A bar is ruled across leaf 108 between the sheer and half-breadth plans, 97 ft long: single
feet for 21 ft at each end and eleven 5-ft spaces between, the first and last foot crossed by
a diagonal (read; judgement: a scale of feet in the draught's manner). Its inner box runs from
533.0 to 3283.7 px: **28.36 px to the foot** (1 px = 0.42 in). The local spacing is 28.18 to
28.47 px/ft (the after feet 28.24-28.37, the 5-ft spaces 28.47, the fore feet 28.18): ±0.5%,
the hand of the ruling. The bar lies 0.5° to the keel; the stations and the half-breadth plan's
middle line are square and parallel to the keel within 0.15°, so x is read along the page.

### 3.2 The stated dimensions measured back

| Dimension | Stated (read) | Measured | Basis |
|---|---|---|---|
| Breadth moulded | 23 ft 8 in (11 ft 10 in a side) | **11 ft 10.1 in** a side (11.84 ft) | the half-breadth plan's heavy outer line at its broadest, 335.7 px from the middle line (±1 px) |
| Length on deck | 94 ft 7 in | **94 ft 9 in** (94.75 ft) | the two dashed perpendiculars, 2687 px apart (±1 px). Each is dropped from the stem's fore edge and the post's after edge (with the rudder) about a foot below the sill line (judgement: the length on deck's ends) |
| Depth of hold | 10 ft 3 in | about 10 ft 1 in | leaf 109 at its own scale (§3.3), the deck's underside to the line taken as the ceiling beside the keelson (judgement on the line; a weak check) |

### 3.3 The other drawings' scales

- **Leaf 109** has no bar. Its perpendiculars stand 2773 px apart (×1.032 of leaf 108's) and
  its rail-to-keel depth amidships is ×1.038; taken as **29.43 px/ft** for heights (measured,
  ±0.5%). It is registered on leaf 108 by its perpendiculars (x) and by the rail (heights).
- **The body plan** (leaf 107) is printed larger. Its dashed moulded-breadth lines stand
  790.9 px apart: **33.42 px/ft** for the stated 23 ft 8 in (measured). The rail of its
  outermost section comes 0.25-0.45 ft lower above the rabbet than the sheer plan's at the
  broadest station; the body plan is used only where the lines plate has nothing (§5.6).

## 4. The waterline and the draught

**The line.** Of the three waterlines in the sheer plan only the top one is carried beyond
the hull, about 9 ft past the rudder and 11½ ft past the stem (read). The inboard plate marks a
short line with the water sign beneath it beyond each end (read). Fitted along the plate
(`c17_track.py`, 320 columns), the line is y = 1281.76 + 0.060411 x + 1.205e-6 x² px, rms 0.46
px; a straight fit leaves 1.0 px rms (a sag of 3 px mid-length, the scan or the drawing:
±0.1 ft). It lies at **3.72°** to the keel, falling to the bow. It is unlabelled; it is taken as
the load water line (judgement): the inboard plate's marks, its freeboard against *Spider*'s
load-line port heights (§5.4) and its draughts against Marestier's (below) all fit it.
Chapelle remarks that load and light lines are rarely drawn on these draughts (p. 86, of
*Alban*, read).

**The two plates agree** (measured): the height of the line above the keel's lower edge is
10.69 ft on leaf 108 and 10.63 ft on leaf 109 at the mid-perpendicular; at AP 13.31 and 13.11
ft, at FP 7.98 and 8.15 ft (both lines extended there). Leaf 109's line, drawn straight
between its end marks, lies at about 0.2° to leaf 108's.

**The other two waterlines** lie 2.32 ft (2 ft 4 in) and 4.52 ft (4 ft 6¼ in) below the load
line, parallel to it (measured, ±0.03 ft). The keel's top (the stations' foot) is a straight
line; the keel's lower edge diverges from it by 0.36°, the keel deeper forward (1 ft 5 in at
the heel, 1 ft 9 in near the forefoot, read and measured): **the draughts are to the lower
edge**.

| Where | ft from AP | x (m) | Below the line |
|---|---|---|---|
| The post's heel, the keel's after end | 8.74 | −11.54 | **12 ft 10 in** (12.82 ft, 3.91 m) |
| The rudder's heel | 5.82 | −12.44 | 12 ft 11 in (12.93 ft, 3.94 m) |
| The keel under the mid-perpendicular | 47.37 | +0.21 | 10 ft 8 in (10.66 ft, 3.25 m) |
| The forefoot (the keel's lower edge meets the stem's fore edge) | 81.52 | +10.60 | **8 ft 8 in** (8.70 ft, 2.65 m) |
| The keel's top line at the heel | 10.30 | −11.10 | 11 ft 4 in (3.45 m) |

±0.1 ft (measured). Mean of heel and forefoot 10 ft 9 in (3.28 m). *Spider*, 80 ft on deck,
drew 9 ft 2 in forward and 11 ft 8 in aft at load (p. 166, read); Marestier's Baltimore
schooners 0.35 and 0.56 of the beam (the files' 8 ft 5 in and 13 ft 4 in, Chapelle p. 113,
read there).

**The line's length** (measured, along the line): rabbet to rabbet 88 ft 1 in (88.06 ft, 26.84
m); the post's after edge to the stem's fore edge 90 ft 11 in (27.71 m); with the rudder 92 ft
5 in (28.16 m). *Spider*'s class: 77 ft 8 in rabbet to rabbet on 80 ft on deck (p. 167, read).

## 5. The profile, measured

### 5.1 The lines of the side (read; identification as marked)

- **The rail**: a thin line (the rail cap's top, used here) and a heavy line 0.27 ft below
  it. The ports' sides run up to the heavy line.
- **The sill line**: a thin line with a heavy one 0.19 ft below it (the planksheer, judgement);
  the ports' sides stop on the thin line (read, at 4x), so it is taken as the sill. The
  stations rise from the keel to the heavy line.
- **The half-breadth plan's outer lines**: a heavy and a thin line, 4-5 px apart amidships.
  Abaft about station 15 the heavy line is outside; they merge at stations 15-18; forward of
  them the thin line is outside by up to 31 px (1.1 ft). Taken as the sill line, or
  planksheer (heavy), and the rail (thin), the rail tumbling home aft and flaring forward
  (judgement: unlabelled). The three curves inside them are the three waterlines, the load
  line outermost (traced from where each meets the post).
- **No wale**, no moulding and no sheer strake are drawn between the sill line and the water
  (read).

### 5.2 By station (measured)

Stations numbered 0 to 23 from aft by this note (the plate numbers none). Heights above the
load line (§4); half-breadths moulded. ±0.05 ft for the lines' positions, ±0.5% scale; the
outer lines' identification is judgement (§5.1). "x" is where the station meets the line.

| Stn | ft from AP | x (m) | Rail top z (ft) | Sill line z (ft) | Rail to sill | ½-br. LWL | ½-br. sill line | ½-br. rail | ½-br. WL2 | ½-br. WL3 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 5.28 | −12.86 | 7.31 | 4.23 | 3.08 | 1.10 | 8.39 | 8.39 | 0.28 | — |
| 1 | 8.89 | −11.75 | 7.11 | 4.03 | 3.08 | 3.19 | 8.82 | 8.82 | 1.36 | 0.70 |
| 2 | 12.74 | −10.58 | 6.89 | 3.83 | 3.06 | 5.56 | 9.25 | 9.17 | 2.70 | 1.38 |
| 3 | 16.46 | −9.44 | 6.70 | 3.63 | 3.07 | 7.31 | 9.66 | 9.50 | 4.13 | 2.20 |
| 4 | 20.24 | −8.29 | 6.51 | 3.48 | 3.03 | 8.51 | 9.99 | 9.83 | 5.65 | 3.10 |
| 5 | 24.08 | −7.11 | 6.38 | 3.36 | 3.02 | 9.39 | 10.32 | 10.13 | 6.93 | 4.10 |
| 6 | 27.87 | −5.96 | 6.28 | 3.24 | 3.04 | 9.95 | 10.59 | 10.42 | 7.92 | 5.00 |
| 7 | 31.63 | −4.81 | 6.20 | 3.19 | 3.01 | 10.43 | 10.87 | 10.68 | 8.68 | 5.81 |
| 8 | 35.42 | −3.65 | 6.15 | 3.14 | 3.01 | 10.73 | 11.12 | 10.95 | 9.29 | 6.48 |
| 9 | 39.29 | −2.47 | 6.13 | 3.12 | 3.01 | 10.94 | 11.31 | 11.15 | 9.69 | 6.94 |
| 10 | 43.05 | −1.32 | 6.13 | 3.09 | 3.03 | 11.14 | 11.51 | 11.35 | 9.99 | 7.33 |
| 11 | 46.80 | −0.18 | 6.13 | 3.13 | 2.99 | 11.30 | 11.67 | 11.51 | 10.21 | 7.54 |
| 12 | 50.61 | +0.99 | 6.18 | 3.19 | 2.99 | 11.39 | 11.80 | 11.63 | 10.31 | 7.61 |
| 13 | 54.43 | +2.15 | 6.25 | 3.28 | 2.97 | **11.40** | **11.84** | 11.67 | 10.24 | 7.43 |
| 14 | 58.13 | +3.29 | 6.35 | 3.39 | 2.96 | 11.29 | 11.80 | 11.64 | 9.96 | 7.00 |
| 15 | 61.97 | +4.46 | 6.50 | 3.53 | 2.97 | 11.04 | 11.67 | 11.67 | 9.45 | 6.37 |
| 16 | 65.74 | +5.61 | 6.66 | 3.73 | 2.94 | 10.61 | 11.45 | 11.45 | 8.61 | 5.57 |
| 17 | 69.45 | +6.74 | 6.84 | 3.93 | 2.90 | 9.95 | 11.09 | 11.09 | 7.57 | 4.59 |
| 18 | 73.29 | +7.92 | 7.06 | 4.14 | 2.92 | 8.93 | 10.53 | 10.53 | 6.34 | 3.50 |
| 19 | 77.04 | +9.06 | 7.30 | 4.36 | 2.95 | 7.56 | 9.66 | 9.87 | 4.96 | 2.42 |
| 20 | 80.89 | +10.24 | 7.55 | 4.61 | 2.93 | 5.85 | 8.48 | 8.89 | 3.43 | 1.36 |
| 21 | 84.56 | +11.36 | 7.81 | 4.87 | 2.94 | 3.94 | 6.79 | 7.64 | 1.94 | 0.42 |
| 22 | 88.33 | +12.51 | 8.04 | 5.17 | 2.87 | 1.77 | 4.68 | 5.70 | 0.30 | — |
| 23 | 92.14 | +13.67 | 8.43 | 5.38 | 3.04 | — | 2.19 | 3.32 | — | — |

- Stations 3.78 ft apart (107.1 px), the aftmost space 3.61 ft. At stations 0-1 one outer
  line only; at 15-18 the two merge (one value given twice). Station 23 lies forward of the
  line's end at the stem: its "½-br. LWL" is the stem.
- The rail and the sill line were read 6 px forward of each station line. Where something
  crosses them they are interpolated (±0.1 ft): the rail's top at stations 3 (a box on the
  rail) and 18 (the fore channel); the sill line at 7 and 16 (the channels) and 9 (the main
  mast).

### 5.3 The ends and the keel (measured)

| Point | ft from AP | x (m) | z (m) | z |
|---|---|---|---|---|
| The taffrail, the rail's after end | −4.09 | −15.88 | +2.44 | 8 ft 0 in |
| The transom's foot (knuckle), where the raking transom meets the post | −0.71 | −14.77 | +1.34 | 4 ft 5 in |
| The rudder's after edge at the line | 0.49 | −14.32 | 0.00 | |
| The post's after edge (the rudder's fore edge) at the line | 1.97 | −13.87 | 0.00 | |
| The post's rabbet at the line | 3.56 | −13.38 | 0.00 | |
| The post's heel | 8.74 | −11.54 | −3.91 | −12 ft 10 in |
| The forefoot | 81.52 | +10.60 | −2.65 | −8 ft 8 in |
| The stem's rabbet at the line | 91.43 | +13.46 | 0.00 | |
| The stem's fore edge at the line | 92.70 | +13.85 | 0.00 | |
| The stem's fore edge under the bowsprit | 96.16 | +14.79 | +1.65 | 5 ft 5 in |
| The stem head, the rail's fore end | 96.58 | +14.86 | +2.70 | 8 ft 10 in |

- ±0.1 ft where a single line is followed; the stern's lines are close together and
  **the division of rudder and post is tentative**: the rudder (three pintle straps) is
  taken as the band between the aftermost raking line and a hatched double line, the post
  as the band from there to the rabbet (read at 4x). The rudder is 1.5 ft wide at the line
  and 2.9 ft at its heel, measured along the line.
- The transom rakes about 45° (taffrail to knuckle); its half-breadth at the taffrail is 7 ft
  5 in (2.25 m), the plan's outer line at its after end (measured). Two ports in it (p. 83,
  read (OCR) l. 4855; one on the body plan's after half, read).
- The stem rakes hard: its fore edge runs 3.25 m forward from the forefoot to the line and
  1.0 m more to the head (measured). The head is a small knee under the bowsprit (read).
- The masts' axes at the sill line: **main −2.60 m** (39.1 ft from AP), **fore +8.27 m** (74.7
  ft from AP), ±0.05 m (measured). Both stumps rake aft; the rakes were not measured.

### 5.4 The ports, against *Spider*

Seven a side (read; p. 83, OCR l. 4856), cut in the bulwark from the sill line up to the
rail's heavy line (read at 4x: no port head below the rail). Measured ±0.05 ft (sill),
±0.1 ft (x):

| Port (from aft) | ft from AP | x (m) | Width | Sill above the line | Opening, sill to rail | ½-br. at the sill (sill line) |
|---|---|---|---|---|---|---|
| 1 | 10.78 | −11.25 | 2.03 ft | 3.93 ft, 3 ft 11 in (1.20 m) | 2.77 ft | 9.03 ft (2.75 m) |
| 2 | 24.00 | −7.20 | 2.10 ft | 3.37 ft, 3 ft 4 in (1.03 m) | 2.78 ft | 10.31 ft (3.14 m) |
| 3 | 40.51 | −2.16 | (2.01 ft) | 3.11 ft, 3 ft 1 in (0.95 m) | 2.75 ft | 11.37 ft (3.47 m) |
| 4 | 50.76 | +0.97 | 2.08 ft | 3.19 ft, 3 ft 2 in (0.97 m) | 2.66 ft | 11.80 ft (3.60 m) |
| 5 | 63.90 | +4.98 | 2.17 ft | 3.63 ft, 3 ft 8 in (1.11 m) | 2.60 ft | 11.56 ft (3.52 m) |
| 6 | 76.45 | +8.80 | 2.03 ft | 4.32 ft, 4 ft 4 in (1.32 m) | 2.63 ft | 9.80 ft (2.99 m) |
| 7 | 86.40 | +11.82 | 2.10 ft | 5.02 ft, 5 ft 0 in (1.53 m) | 2.64 ft | 5.76 ft (1.76 m) |

- Port 3's after side is hidden by the main mast and its chains; its width is the others'
  (judgement). The ports stand unevenly, between the channels and the masts.
- The half-breadth at the sill is the sill line's (judgement, §5.1).

| | *Spider* (Chapelle p. 166, read; p. 167, read) | *Lynx*'s plate (measured) |
|---|---|---|
| Height of ports, aft | 3 ft 7 in | 3 ft 11 in (port 1); 3 ft 4 in (port 2) |
| amidships | **3 ft 5 in** | 3 ft 1 in to 3 ft 2 in (ports 3-4) |
| forward | 4 ft 7 in | 4 ft 4 in (port 6); 5 ft 0 in (port 7) |
| Load draught, forward / aft | 9 ft 2 in / 11 ft 8 in | 8 ft 8 in / 12 ft 10 in (forefoot / heel) |
| Port, fore and aft by deep | 2 ft 6 in by 2 ft 1 in (the class specification, p. 167) | about 2 ft 1 in by 2 ft 8 in to the rail |
| Sill above the deck | 0 ft 10 in (the class specification, p. 167) | within 2 in of the deck at the middle line amidships (measured); with the class's round up, 4 to 5 in above the deck at side amidships and aft, 9 to 12 in at ports 6-7 (judgement, §5.5) |

- **The citation, for B8**: the port heights and draughts are *Spider*'s own table (p. 166,
  read; OCR l. 10335-10343). The 10-in sill, the ports' size and the round up are the
  specification of "one of the Royal Navy schooners of this class", 80 ft on deck and 23 ft
  3 in extreme (p. 167, read), *Spider*'s own breadth being 23 ft 2 in (p. 166): a sister's,
  possibly (judgement). `gen_ships.py:2569` and `:4152` cite both as *Spider*'s.
- *Spider*'s heights are not stated to be above the load line; they follow the load draughts
  in the table (judgement: the load line).

### 5.5 The deck

Leaf 109's section is at the middle line (its caption, read): a flush deck from the transom
to the stem, its plank 0.2 ft thick and its beams below (read). Its top was read below the
rail's top on leaf 109 at its own scale (§3.3), at twelve places, and set on leaf 108's rail
(measured, ±0.15 ft):

| x (m) | −13.48 | −11.60 | −10.55 | −9.50 | −7.41 | −4.80 | −2.19 | −0.62 | +4.07 | +9.79 | +11.35 | +13.42 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Deck at the middle line, z (m) | 1.20 | 1.26 | 1.14 | 1.16 | 1.05 | 0.98 | 0.99 | 0.97 | 1.03 | 1.27 | 1.33 | 1.45 |
| Below the sill line (ft) | 0.19 | −0.15 | 0.05 | −0.18 | −0.06 | −0.04 | −0.13 | −0.05 | 0.12 | 0.39 | 0.54 | 0.60 |

- From the stern to about the fore mast the deck at the middle line lies within 2 in of the
  sill line (the noise of the reading); in the bow it falls 5 to 7 in below it (measured).
  So the deck has less sheer forward than the side.
- **The deck at side** is not drawn: the round up is the class specification's 5½ in (p. 168,
  read on the image; the OCR's "5^4", l. 10604, is garbled), taken for *Lynx* (judgement):
  the deck at side 0.14 m below the middle line, about 0.83 m above the line amidships.

### 5.6 The midship section

From the body plan's outermost fore-body section, taken as the dead flat (judgement); heights
above the rabbet set on the load line by the sheer plan's station 13, where the rabbet lies
8.58 ft below the line (measured, ±0.15 ft at the body plan's scale):

| z (m) | −2.52 | −2.39 | −2.20 | −1.98 | −1.75 | −1.52 | −1.29 | −1.06 | −0.84 | −0.61 | −0.38 | −0.15 | +0.08 | +0.30 | +0.53 | +0.76 | +0.99 | +1.44 | +1.67 | +1.76 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ½-breadth (m) | 0.32 | 0.53 | 0.85 | 1.24 | 1.77 | 2.12 | 2.52 | 2.80 | 3.01 | 3.25 | 3.40 | 3.48 | 3.57 | 3.58 | 3.60 | 3.61 | 3.60 | 3.60 | 3.58 | 3.55 |

- The deadrise is about 28° from the rabbet to 5 ft above it (measured); Chapelle gives about
  30° (p. 82, read). The bilge is slack (read).
- **The lines plate disagrees by up to 0.10 m**: at station 13 its waterlines give 3.47 m at
  z 0 (the body plan 3.54), 3.12 m at −0.71 (3.15) and 2.26 m at −1.38 (2.36); the sill line
  3.61 m at +1.00 and the rail 3.56 m at +1.90 (measured). Judgement: take the lines plate's
  five points where they exist, the body plan's below −1.4 m.

## 6. For the profile (B8): the points in metres

`x` forward of the mid-perpendiculars along the load line, `z` above it (§0's frame), moulded;
from §4-§5 (measured unless marked).

- **`rail_m`** (the rail cap's top): [−15.88, 2.44], [−13.00, 2.23], [−11.90, 2.17],
  [−10.71, 2.10], [−9.57, 2.04], [−8.42, 1.98], [−7.24, 1.94], [−6.08, 1.91], [−4.93, 1.89],
  [−3.77, 1.88], [−2.59, 1.87], [−1.44, 1.87], [−0.30, 1.87], [0.87, 1.88], [2.03, 1.90],
  [3.16, 1.94], [4.33, 1.98], [5.48, 2.03], [6.61, 2.08], [7.78, 2.15], [8.92, 2.23],
  [10.09, 2.30], [11.20, 2.38], [12.35, 2.45], [13.51, 2.57], [14.30, 2.64], [14.86, 2.70].
- **`breadth_m`** [x, at the line, at the rail]: [−12.86, 0.34, 2.56], [−11.75, 0.97, 2.69],
  [−10.58, 1.70, 2.80], [−9.44, 2.23, 2.89], [−8.29, 2.59, 2.99], [−7.11, 2.86, 3.09],
  [−5.96, 3.03, 3.18], [−4.81, 3.18, 3.25], [−3.65, 3.27, 3.34], [−2.47, 3.33, 3.40],
  [−1.32, 3.40, 3.46], [−0.18, 3.45, 3.51], [0.99, 3.47, 3.54], [2.15, 3.47, 3.56],
  [3.29, 3.44, 3.55], [4.46, 3.36, 3.56], [5.61, 3.23, 3.49], [6.74, 3.03, 3.38],
  [7.92, 2.72, 3.21], [9.06, 2.30, 3.01], [10.24, 1.78, 2.71], [11.36, 1.20, 2.33],
  [12.51, 0.54, 1.74]. Plank on: add 0.05 m to each. Beyond the line's ends the rail is
  2.25 m a side at the taffrail and 1.01 m at station 23 (+13.67).
- **`keel_m`** (the lower edge): [−11.54, −3.91], [−8.93, −3.76], [−4.63, −3.52],
  [−0.34, −3.28], [3.95, −3.04], [8.24, −2.80], [10.60, −2.65].
- **`stem_m`** (the fore edge): [10.60, −2.65], [10.98, −2.49], [12.08, −1.77],
  [12.91, −1.06], [13.55, −0.37], [13.85, 0.00], [14.21, 0.53], [14.61, 1.21],
  [14.79, 1.65], [14.86, 2.70] (the head).
- **`stern_m`** (the post's after edge, the transom, the taffrail; tentative, §5.3):
  [−11.54, −3.91], [−12.11, −2.91], [−12.73, −1.87], [−13.36, −0.83], [−13.87, 0.00],
  [−14.11, 0.41], [−14.77, 1.34], [−15.88, 2.44]. The rudder's after edge, for the drawing:
  [−12.44, −3.94], [−12.90, −2.96], [−13.40, −1.91], [−13.90, −0.86], [−14.32, 0.00],
  [−14.72, 0.83].
- **`wales_m`**: none drawn (§8).
- **`section_m`** [z, half-breadth], from §5.6 with the lines plate's points where they
  exist (judgement): [−2.52, 0.32], [−2.39, 0.53], [−2.20, 0.85], [−1.98, 1.24],
  [−1.75, 1.77], [−1.52, 2.12], [−1.38, 2.26], [−0.71, 3.12], [0.00, 3.47], [1.00, 3.61],
  [1.90, 3.56]. Plank on: add 0.05 m.
- **`decks_m.upper`** (at side; judgement, §5.5: the middle line less 0.14 m): [−13.48, 1.06],
  [−11.60, 1.12], [−10.55, 1.00], [−9.50, 1.02], [−7.41, 0.91], [−4.80, 0.84],
  [−2.19, 0.85], [−0.62, 0.83], [4.07, 0.89], [9.79, 1.13], [11.35, 1.19], [13.42, 1.31].
  Every port's sill stands above it (by 0.10 to 0.31 m).
- **`ports_m.upper`** [x, sill, half-breadth]: [−11.25, 1.20, 2.75], [−7.20, 1.03, 3.14],
  [−2.16, 0.95, 3.47], [0.97, 0.97, 3.60], [4.98, 1.11, 3.52], [8.80, 1.32, 2.99],
  [11.82, 1.53, 1.76].
- **`port_size_m.upper`**: [0.63, 0.82], the mean opening from the sill to the rail
  (§5.4). *Spider*'s class: [0.76, 0.64].

## 7. Against the two files (recorded, not moved)

`topsail-schooner.yaml` and `privateer-schooner.yaml` share the hull (`gen_ships.py`
`topsail_schooner()`, at 99a91b8 l. 2542-2618); the guns are the privateer's
(`schooner_armament()`, l. 4139 on).

| Field | The files (their note) | The plates |
|---|---|---|
| `length_waterline_m` | 25.9 (85 ft, judgement between keel and deck) | 26.84 m rabbet to rabbet; 27.71 m post to stem outside (§4) |
| `beam_m` | 7.3 (24 ft extreme) | 24 ft 0 in extreme, read; 22 ft 10 in moulded at the line, 23 ft 2 in plank on (measured) |
| `draught_m` | 3.3 (10.9 ft mean, Marestier's ratios) | 3.28 m mean of the heel's 3.91 m and the forefoot's 2.65 m (§4) |
| `deck_height_m` | 0.9 (*Spider*'s 3 ft 5 in less 10 in, `:2569`) | 0.97-0.99 m at the middle line amidships; about 0.83 m at side (judgement) |
| The port sills (the guns' `height_m`, `:4155`) | 1.04 m (3 ft 5 in, *Spider*) at every port | 0.95 m to 1.53 m by port (§5.4) |
| The swivels' and pivot's `rail` (`:4156`) | 1.7 m (deck + 2 ft 8 in, judgement) | rail top 1.87 m at its lowest, 1.92 m at +2.6 m (the pivot), 2.06 m at −10 m and 2.29 m at +10 m (the swivels) |
| `fore.mast` / `main.mast` `x_m` | +7.8 / −2.6 | +8.27 / −2.60 at the sill line |
| The six long 6s' `x_m` (ports 2, 4, 6) | +8.4, 0.0, −8.4 | ports 2, 4, 6 at −7.20, +0.97, +8.80 |
| The carronades' `x_m` (forward of the fore mast, abaft the main) | +10.5, −7.5 | port 7 at +11.82; port 2 at −7.20 |
| `rudder` | 2.0 m², span 3.4 m ("about 11 ft by 2 ft") | the blade 3.9 m deep from the line to the heel, 0.45 to 0.9 m wide (tentative, §5.3) |

These are for the lead and the owner. Stage 0 moves no figure; the hull's figures carry the
files' sailing pins.

## 8. What the source cannot give

- **A written load line or draught**: neither plate labels the line or gives draught figures;
  the line is identified by judgement (§4).
- **A wale**: none drawn; the plain finish is Chapelle's remark (p. 83, read). The class
  specification gives main wales 4 in thick (p. 168, read): an English-built schooner's, not
  *Lynx*'s draught.
- **The deck at side**: the round up is not drawn (§5.5).
- **Which outer line is the rail**: the half-breadth plan's two outer lines are unlabelled
  (§5.1).
- **The post and the rudder apart**: the division is a reading of close lines (§5.3).
- **The original draught**: these are Chapelle's redrawings (signed '29, tentative); the
  Admiralty's sheet (Portsmouth, 10 May 1816) was not looked for here, and any error of the
  redrawing carries.
- **The spars, the masts' rake, the sweeps, port lids and scantlings**: not on the plates
  (the spars: p. 82, read).
- **The body plan at the plate's scale**: printed at its own size, scaled by the moulded
  breadth only (§3.3).

## 9. Method and files

The images were read with crops, enlargements and gridded crops, and measured by scripts kept
outside the repository in the session's scratch directory under `stage0/pages/`, each taking
the cached image's path (or a grey copy made from it by `c17_convert.py`) as its argument:
`c17_fetch.py` (the fetches), `c17_info.py` (the images' sizes), `c17_convert.py`, `c17_crop.py`
and `c17_grid.py` (the views), `c17_profile.py` (the bar's ticks and the stations),
`c17_runs.py` (lines crossing a column or row, by darkness centroid), `c17_track.py` and
`c17_trackv.py` (following a line), and `c17_ports.py` (the ports' sides between the rail and
the sill line). `c17_compute.py`,
`c17_deck.py` and `c17_profile_out.py` hold the values read and make the tables and lists
above; they read no image.
