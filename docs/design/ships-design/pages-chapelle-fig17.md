# Pages: Chapelle 1930, fig. 17 and its plates, H.M. schooner *Musquidobit*, late *Lynx* (October 2026)

Stage 0 research for package 75, the page named by `Build-Ships.md` §19.1 item 11 and by the
shared draft (`ships-design/shared-design.md` §1.5, the schooners' row at line 201; §5). It
serves `data/ships/topsail-schooner.yaml` and `data/ships/privateer-schooner.yaml`, both built
on *Lynx*'s draught by `topsail_schooner()` and `privateer_schooner()` in `tools/gen_ships.py`,
and the builder B8, who draws a sourced hull profile for each (`Build-Ships.md` §5). Their
sills were first sourced to *Spider* (Chapelle pp. 166-167; `gen_ships.py:4152-4156` at
99a91b8); §5.4 measures the plates against that, and the lead's ruling of 2026-10-31 takes the
plate's own (§6.2). Facts only: the images are kept outside the
repository (§1.1).

The hull step (SW-2 with SW-2b.2) read it again against the image and added what `Build-Ships.md`
§5.1 and §5.7 still wanted: the head, the deck traced and its ends, the main breadth, the sections
by station, the stern's face, the masts' rakes and the rabbet (§5.3, §5.5 to §5.11), the points in
the files' own frame (§6.2 to §6.5), and her two checks, Steel's schooner of 133 tons and
*Flying Fish*, each recorded beside her and moving nothing (§10). The owner's photographs of the
replica (`Build-Ships.md` §5.8) are for the eye: no point here comes from a picture. A second reader
then measured the sheets again by its own route, and this note stands as mended by what it found (§9).
The hull's review laid the built hull back on the plates and followed the sections again: its mends are
§5.8's third reader and §6.3's mark.

The marks:

- **read**: the page's printing or drawing was seen on the image. "read (OCR)" is the held
  text layer only. "tentative" is a reading at the limit of the image.
- **measured**: off the image at the scale of §3; the uncertainty is stated.
- **arithmetic**: computed from read figures by a scratch script (§9); the method is stated.
- **judgement**: reasoning by this note.
- **catalogue**: from the item's metadata and page only.

**Units and datums.** English feet and inches, with metres in brackets. Along the ship, "ft
from AP" is measured along the keel as drawn, from **AP**, the after of the two dashed
perpendiculars drawn on the sheer plan, whose distance apart is the length on deck (§3.2).
The draught is drawn with the keel nearly level: its top line 0.15° and its lower edge 0.50° to the
page, the waterline **3.72°** to the page, so 3.57° and 3.22° to them (the drag, §4). So for the
profile the frame is turned to the water: **`x`** is measured along the drawn load
water line (LWL) from the point where the mid-perpendicular meets it, positive forward, and
**`z`** square to that line, positive up. On this frame AP and FP fall at x = ∓14.47 m. A
point above the line lies aft of its station by z·0.065 (0.12 m at the rail); every `x` in §6
is the point's own. Half-breadths are moulded, to the outside of the frames; the plank adds
about 2 in a side (the stated extreme breadth less the moulded, halved: read, arithmetic).
**The files' frame** (§6.2 to §6.4): the same `x` and `z`, each point carried by §6.2's factors to
`length_waterline_m` 25.9 and `beam_m` 7.3, the half-breadths with the plank on, as
`hull.profile` takes them: `x` forward of midships, `z` above the file's waterline, metres.

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
  (§3). The table's keel and breadth give 223.98 tons by the rule against the stated 223 91/94
  (arithmetic).
- **The sheets agree with each other.** Leaf 109's stations, ports and masts lie on leaf 108's
  within 0.17 ft; the body plan's five curves cross the plate's half-breadths at the plate's
  heights within 0.04 ft rms in the fore body and 0.11 ft in the after body, the after body's
  rail the worst at 0.29 ft (§3.4: a check on heights only, §5.1).
- **The load water line is taken, by judgement, as the one waterline carried past both ends** of
  the sheer plan; the inboard plate marks the same line at its ends with the water sign, and the
  two agree within 1 in amidships (measured). Neither plate labels it. On it the midship port sills stand 3 ft 1 in, the figure of
  Steel's schooner of 133 tons to the inch (§4, §10). **Draught** to the keel's lower edge:
  **12 ft 10 in at the heel of the post, 8 ft 8 in at the forefoot**, mean 10 ft 9 in (3.28 m),
  against the files' 3.3 m.
- **The side.** The rail's top stands 6 ft 1½ in (1.87 m) above the line at its lowest, just
  abaft the middle, 8 ft 0 in (2.44 m) at the taffrail and 8 ft 10 in (2.70 m) at the stem
  head; the bulwark is about 3 ft from the rail's top to the sill line throughout. **Seven
  ports a side**, cut from the sill line to the rail, 2 ft 1 in wide; sills 3 ft 1 in to 5 ft
  0 in above the line, the lowest, 0.95 m, at port 3 just before the main mast (§5.4).
- **Against *Spider*** (§5.4): *Spider*'s 3 ft 5 in amidships stands 3 to 4 in above *Lynx*'s
  midship sills; her ends (3 ft 7 in aft, 4 ft 7 in forward) lie below *Lynx*'s (3 ft 11 in,
  5 ft 0 in), the drag giving *Lynx* more freeboard at the ends. *Spider* is of 1835 (p. 165,
  read (OCR) l. 10302), twenty-three years after *Lynx*.
- **Half-breadths**: 11 ft 10 in at the sill line and 11 ft 5 in at the water at the broadest,
  about 2 m forward of the middle; the rail tumbles home about 2 in amidships and flares out up
  to 1.1 ft in the bow. The heavy outer line is the moulded breadth, at the sill line abaft about
  station 16 and a little inside the section forward of it (§5.1). The **main
  breadth** stands about 0.84 m above the line amidships, rising to 1.15 m aft and 0.95 m at station
  16, on a section flat within an inch from about 0.65 m to the sill line (§5.7). **The sections** are given by station, from the keel to the
  rail (§5.8); the deadrise about 28° (§5.6).
- **The deck** is flush, traced now from the transom to the stem; at the middle line it lies
  within 2½ in of the sill line from the stern to about station 15 and 4 to 9 in below it in the
  bow. Its round up is not drawn (§5.5). **No wale is drawn** (§8).
- **The ends.** The stem rakes hard, with a small knee of the head on its fore side, 2 ft 4 in
  forward of the stem at the bowsprit (§5.3); the transom rakes about 38° to the water's square, 7 ft 5 in a side moulded on
  the lines plate and 7 ft 8½ in on the body plan, with two ports and neither lights nor
  galleries (§5.9). The masts rake 9.9° and 13.5° to the keel's square (§5.10).
- **For the file** (§6): lengths by 0.965, sections by 0.998, the lowest sill at the plate's own
  3 ft 1 in, her own sheet over *Spider*'s 3 ft 5 in of 1835, as the lead ruled on 2026-10-31 (§6.2;
  `Build-Ships.md` §5.4). As built by
  `tools/ships/hull_schooner.py`: drawn 198 t against the filed 211 t, 3.10 m deep at the greatest
  section against 3.3 m, eight port triples for the plate's seven, the guns' `x_m` unmoved (§6.3),
  each within 0.02 m of the drawn side (§6.5).
- **Against the files** (§7, recorded; only the guns' `height_m` move, by `Build-Ships.md` §5.3): the line is 88 ft rabbet to rabbet (26.84
  m) against the files' 85 ft (25.9 m); the sills 0.95 to 1.53 m against 1.04 m at every port;
  the rail 1.87 to 2.3 m against the swivels' 1.7 m; the fore mast at +8.26 m against +7.8 m.
- **Her two checks** (§10, recorded, moving nothing): Steel's schooner and *Flying Fish* carry
  the type's low sill (3 ft 1 in, 2 ft 10 in), its cut-away ends (the keel about 77% of the length
  on deck in all three) and its waterplane (0.67 to 0.72 of the length by the breadth). *Lynx* has
  the most deadrise of the three (28° against 25° and 18-20°), the most drag and the widest
  transom.

## 1. The source

### 1.1 The book, the images and the cache

| | |
|---|---|
| Work | Howard I. Chapelle, *The Baltimore Clipper: Its Origin and Development*, Salem, Mass.: Marine Research Society, 1930; the held OCR is `docs/references/chapelle/chapelle-1930-the-baltimore-clipper-ocr.txt` |
| Copy scanned | Internet Archive item `baltimoreclipper00howa`, https://archive.org/details/baltimoreclipper00howa : the Bonanza Books (New York) reprint, whose imprint page gives the copyright as 1930, the Marine Research Society's, and Library of Congress card 76-27148 (read (OCR) l. 41-52). Scanned 2013 at 350 ppi, 234 leaves (catalogue) |
| Rights shown | None (catalogue). The item page and its metadata carry no rights, licence or copyright-status field; the item is in the open `internetarchivebooks` collection and its files download without a loan (fetched 2026-10-28). Published in the United States in 1930, in the public domain there from 1 January 2026 (judgement: 95 years; as `docs/references/README.md:12` says). The reprint adds nothing to the plates (judgement) |
| Leaves used | Leaf 107, p. 83, fig. 17 (body plan); leaf 108, unnumbered plate (the draught's sheer and half-breadth plans); leaf 109, unnumbered plate (longitudinal section and deck plan); leaves 202-204, pp. 166-168 (*Spider* and the class specification); for the check of §10.2, leaves 68 and 69, the unnumbered plates of *Flying Fish* listed in the book's table of plates at pp. 48-49. In the online reader these are `page/n105` to `n107`, `n200` to `n202`, `n66` and `n67` (the reader skips two leaves) |
| Images used | The processed page images, 2756 x 3715 px each, from the item's `_jp2.zip`: https://archive.org/download/baltimoreclipper00howa/baltimoreclipper00howa_jp2.zip/baltimoreclipper00howa_jp2%2Fbaltimoreclipper00howa_0107.jp2 and the same with `_0108`, `_0109`, `_0202`, `_0203`, `_0204`, `_0068`, `_0069`. Leaf 107: 360,023 bytes, sha256 a723472a6adbcd4cd3ffb87c98613e9c760a60bdaa6fd2abb629397ce5bacbad; leaf 108: 207,258, 03539561750281173995559c3ee97cd43ae2f160e41803c88c764fbcc379c92f; leaf 109: 191,740, 78d60024cb314b7862f5814a2efa5f13681a1fc81f368675bee763fe2df8005f; leaf 68: 253,394, 9ddaf540da13c7098c34a8168fdf0b9d51b9dee1dc33004a291183cb4c5a4b7b; leaf 69: 190,183, b46ec0ed28d5a6c7c51f891343e8ea7625dfa2b7e9e9671efc11a8c3b8cb2b14 |
| Also fetched | The camera original of leaf 108, 5616 x 3744 px: https://archive.org/download/baltimoreclipper00howa/baltimoreclipper00howa_orig_jp2.tar/baltimoreclipper00howa_orig_jp2%2Fbaltimoreclipper00howa_orig_0108.jp2 (viewed; the processed leaf 108 is a 1:1 crop of it, every vertical at a constant 996.7 px: measured). Previews https://archive.org/download/baltimoreclipper00howa/page/n104_w700.jpg to `n109_w700.jpg` (finding the leaves). Metadata: https://archive.org/metadata/baltimoreclipper00howa , `.../download/baltimoreclipper00howa/baltimoreclipper00howa_page_numbers.json`, `..._scandata.xml`, and the item page |
| Cache | `D:/Projects/FreeSail/reference-cache/chapelle-fig17/`: `leaf0107/`, `leaf0108/`, `leaf0109/` (one JP2 each), `orig-leaf0108/`, `spider-pp166-168/` (three JP2s), `previews/` (`n104_w700.jpg` to `n109_w700.jpg`, and `n62` to `n71`, finding *Flying Fish*'s leaves), `leaf0068/`, `leaf0069/`, `meta/` (`metadata.json`, `page_numbers.json`, `scandata.xml`, `details.html`). Fetched 2026-10-28, and on 2026-10-30 for the check, with a generic user-agent |
| Steel's check | David Steel, *The Elements and Practice of Naval Architecture* (1805 text), Internet Archive item `elementspractice00stee` (`ships-design/pages-steel-1805-bodies.md` §1: No Copyright, United States): tables p. 25 (scan leaf `_0484.jp2`, fetched 2026-10-30 to `D:/Projects/FreeSail/reference-cache/steel-1805-bodies/`), and the right leaves of Folios I, II, VII, XXXI, XXXII, LI and LV already cached there (`_0489`, `_0491`, `_0501`, `_0549`, `_0551`, `_0589`, `_0597`) |

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
the hand of the ruling. The bar lies 0.5° to the page, parallel to the keel's lower edge; the stations and the half-breadth plan's
middle line are square and parallel to the keel within 0.15°, so x is read along the page.

### 3.2 The stated dimensions measured back

| Dimension | Stated (read) | Measured | Basis |
|---|---|---|---|
| Breadth moulded | 23 ft 8 in (11 ft 10 in a side) | **11 ft 10.1 in** a side (11.84 ft) | the half-breadth plan's heavy outer line at its broadest, 335.7 px from the middle line (±1 px) |
| Length on deck | 94 ft 7 in | **94 ft 9 in** (94.75 ft) | the two dashed perpendiculars, 2687 px apart (±1 px). FP stands on the stem's rabbet lines at about the deck, AP on the post's after edge (judgement: the length on deck's ends) |
| Depth of hold | 10 ft 3 in | about 10 ft 2½ in | leaf 109 at its own scale (§3.3), the deck's underside to the line taken as the ceiling beside the keelson (judgement on the line; a weak check) |

### 3.3 The other drawings' scales

- **Leaf 109** has no bar. Its perpendiculars stand 2773 px apart (×1.032 of leaf 108's) and its
  rail's top to its keel stands ×1.0225 to the keel's top line and ×1.025 to its lower edge; taken as
  **29.04 px/ft** for heights (measured, ±0.2%), against ×1.032 to ×1.0335 along the page. It is
  registered on leaf 108 by its perpendiculars (x) and by the rail (heights).
- **The body plan** (leaf 107) is printed larger. Its dashed moulded-breadth lines stand
  792.4 px apart (re-read; the first reading was 790.9 px), about a middle line at 1698.2 px:
  **33.48 px/ft across** for the stated 23 ft 8 in (measured). Upright it is **33.26 px/ft** in the
  fore body and 32.77 in the after body (§3.4), so its heights are registered by each station's
  curves and not by the one scale. Its dashed base is the keel's top line of leaf 108 within
  0.01 ft in the fore body (measured).

### 3.4 The sheets against each other (measured)

| What | Leaf against leaf | Result |
|---|---|---|
| The dashed stations, 1 to 21 | 109 against 108, on x109 = 769.0 + 1.0335 (x108 − 820) px | within 5 px (0.17 ft), the middle of the page the worst; a straight scale ×1.0335, against ×1.032 by the perpendiculars alone |
| The ports' sides seen inboard | 109 against 108, on the same line | ports 1, 2, 4, 5 and 7 within 4.7 px (0.17 ft); port 6's fore side within 0.1 px; port 3's after side and port 6's are hidden by the masts |
| The masts at the sill line | 109 against 108 | main 2.1 px, fore 2.6 px forward on leaf 108 (0.09 ft); dx/dy 0.175 against 0.175 (main), 0.233 against 0.240 (fore) |
| The load line | 109 against 108 | §4 |
| The deck | 109, set on 108's rail | §5.5; the first twelve readings lie on the trace within 0.06 m |
| The five curves on the body plan: rail, sill line, LWL, WL2, WL3 | 107 against 108: each curve fitted across the sections (rms 0.2 to 0.4 px; the fore WL3 3 px) and read at the half-breadth the plate gives each station, against the plate's height above the keel's top line | fore body, 33 nodes: y = 1400.3 − 33.26 H px, rms 1.38 px (0.04 ft). After body, 54 nodes: y = 1390.4 − 32.77 H px, rms 3.64 px (0.11 ft); its rail lies up to 9.5 px (0.29 ft) low amidships and its sill line 4 px high. A check on heights only: each curve is nearly level where it is read, so it cannot say which plan line is which (§5.1) |

- **Which body plan section is which station** (measured): the waterlines' half-breadths place
  stations 0 to 12 on the after half and 13 to 23 on the fore half, station 13 the outermost of
  the fore half (11 ft 10 in), as §5.6 took it.
- **The half-breadth plan on the deck plan** (leaf 109): at the broadest the deck plan's outer
  line stands 351.5 px from the middle line, 29.29 px/ft if that line is the 24 ft 0 in extreme, against
  29.04 px/ft for its heights (measured); the first is a reading of the line and does not rule against
  the second. Its lines are rail, side and waterway, not the moulded lines of
  leaf 108.

## 4. The waterline and the draught

**The line.** Of the three waterlines in the sheer plan only the top one is carried beyond
the hull, about 9 ft past the rudder and 10 ft past the stem's fore edge (read). The inboard plate marks a
short line with the water sign beneath it beyond each end (read). Fitted along the plate
(`c17_track.py`, 320 columns), the line is y = 1281.76 + 0.060411 x + 1.205e-6 x² px, rms 0.46
px; a straight fit leaves 1.0 px rms (a sag of 3 px mid-length, the page's own curve, common to
every long line, so that heights between lines are free of it). It lies at **3.72°** to the page
(3.22° to the keel's lower edge), falling to the bow. It is unlabelled; it is taken as
the load water line (judgement): the inboard plate's marks, its freeboard against *Spider*'s
load-line port heights (§5.4) and its draughts against Marestier's (below) all fit it.
Chapelle remarks that load and light lines are rarely drawn on these draughts (p. 86, of
*Alban*, read (OCR) l. 4929-4930).

**How it was judged, the three tests** (measured, read, arithmetic): (1) the plate carries it past
both ends and the inboard plate marks its ends with the water sign, as no other line; (2) on it the
midship sills stand 3 ft 1 in, where Steel's schooner of 133 tons has 3 ft 1 in above the water in
midships (Folio I, row Q, read: §10.1) and *Flying Fish*'s sills 2 ft 10 in above her top waterline
(§10.2), *Spider*'s 3 ft 5 in (p. 166, read); (3) its draughts, 12 ft 10 in and 8 ft 8 in, against
*Spider*'s 11 ft 8 in and 9 ft 2 in on 80 ft, Steel's schooner's 9 ft 3 in and 7 ft 3 in on 77 ft,
and Marestier's ratios below. None of these labels the line; it stays a judgement.

**The two plates agree** (measured): the height of the line above the keel's lower edge is
10.68 ft on leaf 108 and 10.62 ft on leaf 109 at the mid-perpendicular; at AP 13.30 and 13.28
ft, at FP 7.97 and 7.96 ft (both lines extended there). The two lines lie 0.03° apart, each to its
own keel's lower edge.

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
m), on the heavy lines; thin line to thin line 87 ft 11 in (26.79 m), k_L 0.9668, recorded (§5.11); the post's after edge to the stem's fore edge 90 ft 11 in (27.71 m); with the rudder 92 ft
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
  them the thin line is outside by up to 31 px (1.1 ft). The plate does not label them.
  The heavy line is the moulded breadth (it measures 23 ft 8 in at its broadest). It lies at the sill
  line abaft about station 16. Forward of that it stands up to 0.22 ft inside the section at the sill's
  height (the sections crossed directly on the body plan, net of the body's excess at the water); the
  thin line is the rail, tumbling home aft and flaring forward (judgement). §3.4's fit is a check on
  heights and cannot say which line is which. The three curves inside them are the three waterlines, the load line outermost
  (traced from where each meets the post).
- **No wale**, no moulding and no sheer strake are drawn between the sill line and the water
  (read).

### 5.2 By station (measured)

Stations numbered 0 to 23 from aft by this note: the sheets carry no station letter or number
(read). Heights above the load line (§4); half-breadths moulded. ±0.05 ft for the lines' positions,
±0.5% scale. "x" is where the station meets the line. A checker, reading each line afresh 6 px
either side of each station with only the station's x given (`chk108.py`), found the table's pixel
values within 1 px wherever nothing crosses them. The waterlines stand at z 0, −2.32 ft and −4.52 ft
(§4).

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
| 22 | 88.33 | +12.51 | 8.11 | 5.17 | 2.94 | 1.77 | 4.68 | 5.70 | 0.30 | — |
| 23 | 92.14 | +13.67 | 8.43 | 5.47 | 2.96 | — | 2.19 | 3.32 | — | — |

- Stations 3.78 ft apart (107.1 px), the aftmost space 3.61 ft. At stations 0-1 one outer
  line only; at 15-18 the two merge (one value given twice). Station 23 lies forward of the
  line's end at the stem: its "½-br. LWL" is the stem.
- The rail and the sill line were read 6 px forward of each station line. Where something
  crosses them they are interpolated (±0.1 ft): the rail's top at stations 3 (a box on the
  rail), 18 (the fore channel) and 22 (the cathead); the sill line at 7 and 16 (the channels), 9 (the
  main mast) and 23 (the hawse bolster).
- The "½-br. sill line" column is the plan's heavy line (§5.1): at stations 17 to 21 it stands inside
  the section at the sill's height.

### 5.3 The ends and the keel (measured)

| Point | ft from AP | x (m) | z (m) | z |
|---|---|---|---|---|
| The taffrail, the rail's after end | −4.09 | −15.88 | +2.44 | 8 ft 0 in |
| The taffrail's cap, its top: not in `rail`, for the lead | about −4.3 | −15.94 | +2.53 | 8 ft 4 in |
| The transom's face, its lower end, where the band begins | −2.13 | −15.22 | +1.62 | 5 ft 4 in |
| The transom's foot (knuckle), where the band meets the post | −0.71 | −14.77 | +1.34 | 4 ft 5 in |
| The rudder's after edge at the line | 0.49 | −14.32 | 0.00 | |
| The post's after edge (the rudder's fore edge) at the line | 1.97 | −13.87 | 0.00 | |
| The post's rabbet at the line | 3.56 | −13.38 | 0.00 | |
| The post's heel | 8.74 | −11.54 | −3.91 | −12 ft 10 in |
| The forefoot | 81.52 | +10.60 | −2.65 | −8 ft 8 in |
| The stem's rabbet at the line | 91.43 | +13.46 | 0.00 | |
| The stem's fore edge at the line | 92.70 | +13.85 | 0.00 | |
| The knee of the head leaves the stem | 94.00 | +14.21 | +0.53 | 1 ft 9 in |
| The stem's fore edge at the bowsprit's underside | 95.91 | +14.71 | +1.77 | 5 ft 10 in |
| The knee's top, under the bowsprit | 98.20 | +15.41 | +1.85 | 6 ft 1 in |
| The stem head, the rail's fore end | 96.58 | +14.86 | +2.70 | 8 ft 10 in |

- ±0.1 ft where a single line is followed; the stern's lines are close together and
  **the division of rudder and post is tentative**: the rudder (three pintle straps) is
  taken as the band between the aftermost raking line and a hatched double line, the post
  as the band from there to the rabbet (read at 4x). The rudder is 1.5 ft wide at the line
  and 2.9 ft at its heel, measured along the line.
- The transom rakes about 38° to the water's square (§5.9); its half-breadth at the taffrail is 7 ft
  5 in (2.25 m), the plan's outer line at its after end (measured). Two ports in it (p. 83,
  read (OCR) l. 4855; one on the body plan's after half, read).
- The stem rakes hard: its fore edge runs 3.25 m forward from the forefoot to the line and
  1.0 m more to the head (measured).
- **The head** (read and measured at 4x; the first reading carried the stem's line along the
  knee's). The outer curve up from the forefoot is the fore edge to where a thin joint leaves it at
  +0.53 m, 1 ft 9 in above the line. From there the joint is the stem's own fore edge, up to the
  bowsprit's underside at [+14.71, +1.77]; above the bowsprit the stem's edge runs on to the rail's
  fore end. The outer curve goes on as **the knee of the head**, sweeping forward to end under the
  bowsprit at [+15.41, +1.85], 2 ft 4 in before the stem there. Nothing stands on it: "a small
  head for the gammoning" (p. 83, read), no figure, no rails, no trail boards (read).
- The rudder head and the stern are §5.9, the masts §5.10.

### 5.4 The ports, against *Spider*

Seven a side (read; p. 83, OCR l. 4856), cut in the bulwark from the sill line up to the
rail's heavy line (read at 4x: no port head below the rail). Measured ±0.05 ft (sill),
±0.1 ft (x):

| Port (from aft) | ft from AP | x (m) | Width | Sill above the line | Opening, sill to rail | ½-br. at the sill (sill line) |
|---|---|---|---|---|---|---|
| 1 | 10.78 | −11.25 | 2.03 ft | 3.93 ft, 3 ft 11 in (1.20 m) | 2.77 ft | 9.03 ft (2.75 m) |
| 2 | 24.00 | −7.20 | 2.10 ft | 3.37 ft, 3 ft 4 in (1.03 m) | 2.78 ft | 10.31 ft (3.14 m) |
| 3 | 40.51 | −2.16 | 2.01 ft | 3.11 ft, 3 ft 1 in (0.95 m) | 2.75 ft | 11.37 ft (3.47 m) |
| 4 | 50.76 | +0.97 | 2.08 ft | 3.19 ft, 3 ft 2 in (0.97 m) | 2.66 ft | 11.80 ft (3.60 m) |
| 5 | 63.90 | +4.98 | 2.17 ft | 3.63 ft, 3 ft 8 in (1.11 m) | 2.60 ft | 11.56 ft (3.52 m) |
| 6 | 76.45 | +8.80 | 2.03 ft | 4.32 ft, 4 ft 4 in (1.32 m) | 2.63 ft | 9.80 ft (2.99 m) |
| 7 | 86.40 | +11.82 | 2.10 ft | 5.02 ft, 5 ft 0 in (1.53 m) | 2.64 ft | 5.76 ft (1.76 m) |

- Port 3's after side stands clear at 1688.3 px, the chains aft of it. The ports stand unevenly,
  between the channels and the masts.
- The half-breadth at the sill is the plan's heavy line (judgement, §5.1). At ports 6 and 7 the
  section at the sill's height stands about 9.96 and 5.84 ft, +0.05 and +0.02 m (measured).

| | *Spider* (Chapelle p. 166, read; p. 167, read) | *Lynx*'s plate (measured) |
|---|---|---|
| Height of ports, aft | 3 ft 7 in | 3 ft 11 in (port 1); 3 ft 4 in (port 2) |
| amidships | **3 ft 5 in** | 3 ft 1 in to 3 ft 2 in (ports 3-4) |
| forward | 4 ft 7 in | 4 ft 4 in (port 6); 5 ft 0 in (port 7) |
| Load draught, forward / aft | 9 ft 2 in / 11 ft 8 in | 8 ft 8 in / 12 ft 10 in (forefoot / heel) |
| Port, fore and aft by deep | 2 ft 6 in by 2 ft 1 in (the class specification, p. 167) | about 2 ft 1 in by 2 ft 8 in to the rail |
| Sill above the deck | 0 ft 10 in (the class specification, p. 167) | within 2 in of the deck at the middle line amidships (measured); with the class's round up, 5 to 7 in above the deck at side at ports 1 to 4, 8 in at port 5, 10 to 12 in at ports 6-7 (judgement, §5.5) |

- **The citation, for B8**: the port heights and draughts are *Spider*'s own table (p. 166,
  read; OCR l. 10335-10343). The 10-in sill, the ports' size and the round up are the
  specification of "one of the Royal Navy schooners of this class", 80 ft on deck and 23 ft
  3 in extreme (p. 167, read), *Spider*'s own breadth being 23 ft 2 in (p. 166): a sister's,
  possibly (judgement). `gen_ships.py:2569` and `:4152` cite both as *Spider*'s.
- *Spider*'s heights are not stated to be above the load line; they follow the load draughts
  in the table (judgement: the load line).
- **Which *Spider***: "H. M. schooner *Spider* of 1835", apparently a sister of *Cockatrice* and
  *Viper*, launched 1831 from Seppings's designs, "rather similar to the American type, but not at
  all extreme" (p. 165, read (OCR) l. 10301-10305; p. 166, read). She is later than the
  game's years and no Baltimore vessel. The two sources of the type within them, *Lynx*'s plate and
  Steel's schooner, stand at 3 ft 1 in (§6.2, §10).

### 5.5 The deck and its ends

Leaf 109's section is at the middle line (its caption, read): a flush deck from the transom to the
stem, its plank 0.2 ft thick and its beams below (read). The top of the plank was followed column by
column below the rail's top, 288 columns kept of 396 where a plank's two lines stood clear of the
hatches and bitts, and fitted smooth (rms 0.45 px, 0.015 ft: `deck109.py`), then set on leaf 108's
rail at leaf 109's own height scale (§3.3; §3.4's registration in x). ±0.05 ft on the fit, ±0.2% on
the scale; the first twelve readings lie on it within 0.06 m (measured). The x column is the rail's at
the station (the deck's own lies up to 0.06 m forward of it).

| Stn | x (m) | Deck at the middle line, z (m) | Below the rail's top (ft) |
|---|---|---|---|
| aft end | −14.44 | 1.30 | 3.39 |
| 0 | −13.00 | 1.23 | 3.28 |
| 1 | −11.90 | 1.19 | 3.22 |
| 2 | −10.71 | 1.14 | 3.17 |
| 3 | −9.57 | 1.09 | 3.12 |
| 4 | −8.42 | 1.04 | 3.08 |
| 5 | −7.24 | 1.02 | 3.04 |
| 6 | −6.08 | 1.00 | 3.01 |
| 7 | −4.93 | 0.98 | 2.99 |
| 8 | −3.77 | 0.97 | 2.97 |
| 9 | −2.59 | 0.96 | 2.97 |
| 10 | −1.44 | 0.96 | 2.98 |
| 11 | −0.30 | 0.95 | 3.00 |
| 12 | 0.87 | 0.96 | 3.02 |
| 13 | 2.03 | 0.97 | 3.05 |
| 14 | 3.16 | 1.00 | 3.09 |
| 15 | 4.33 | 1.03 | 3.12 |
| 16 | 5.48 | 1.07 | 3.16 |
| 17 | 6.61 | 1.11 | 3.21 |
| 18 | 7.78 | 1.16 | 3.26 |
| 19 | 8.92 | 1.22 | 3.31 |
| 20 | 10.09 | 1.27 | 3.39 |
| 21 | 11.20 | 1.32 | 3.47 |
| 22 | 12.35 | 1.38 | 3.57 |
| 23 | 13.51 | 1.44 | 3.69 |
| fore end | 14.06 | 1.47 | 3.75 |

- **The ends** (read and measured): aft, the plank runs to the transom's inner face, at about the
  post's head; forward, to the stem's inner line. No step, no raised quarterdeck (read). Aft, a
  curved line rises from the transom to a small circle just under the rail's top at x about −12 m
  (read, unidentified: inboard, not the side).
- From the stern to about station 15 the deck at the middle line lies within 2½ in of the sill line,
  a little above it amidships; it falls 3 to 4 in below it at stations 16 to 18 and 4 to 9 in forward of
  them (measured). So the deck has less sheer forward than the side.
- **The deck at side** is not drawn: the round up is the class specification's 5½ in (p. 168,
  read on the image; the OCR's "5^4", l. 10604, is garbled), taken for *Lynx* (judgement): the deck
  at side 0.14 m below the middle line, 0.82 m above the line amidships. Steel's schooner has 5 in
  (Folio XXXI, row X, read); *Flying Fish*'s midsection about 11 in (§10.2), so ±0.1 m is honest.

### 5.6 The midship section

Station 13, the outermost of the body plan's fore half, is the dead flat (§3.4). From the keel's
lower edge, the rabbet, the body plan to WL3, the lines plate's waterlines, the body plan to the sill
line, and the rail (moulded, metres; ±0.05 m; the same table in §5.8):

| z (m) | −3.14 | −2.69 | −2.40 | −1.90 | −1.38 | −0.71 | 0.00 | 0.35 | 0.70 | 1.00 | 1.91 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ½-breadth (m) | 0.11 | 0.11 | 0.50 | 1.41 | 2.27 | 3.12 | 3.47 | 3.55 | 3.61 | 3.61 | 3.56 |

- The deadrise is about 28° from the rabbet to 5 ft above it (measured); Chapelle gives about 30°
  (p. 82, read (OCR) l. 4837). The bilge is slack (p. 82, read (OCR) l. 4838).
- **The first reading's disagreement of up to 0.10 m** between the body plan and the lines plate is
  gone from this table: each is tied to the plate at its nodes (§5.8). It stands in the sheets, as
  §3.4's after body shows.

### 5.7 The main breadth (measured; its height judgement)

The widest of each section, read off the body plan between the water and the sill line. A section
amidships is flat within 0.012 ft over a band, so the height of the widest is a band and not a point;
the height given is a smooth curve through the bands' middles, as a share of the height from the
water to the sill line (a cubic in the station: 1.0 at station 2, about 0.9 amidships, fitted through
station 18 and used to station 16).
Abaft station 2 and forward of station 16 the section is widest at or above the sill line, and there is
no main breadth inside it (measured): stations 17 and 18 are given at the sill line and are not in the
file's line.

| Stn | x (m) | Main breadth, z (m) | ½-breadth (m) | The band, z (m) |
|---|---|---|---|---|
| 2 | −10.58 | 1.15 | 2.83 | 1.15 to 1.16 |
| 3 | −9.44 | 1.06 | 2.95 | 1.07 to 1.10 |
| 4 | −8.29 | 1.00 | 3.05 | 0.89 to 1.06 |
| 5 | −7.11 | 0.95 | 3.15 | 0.80 to 1.02 |
| 6 | −5.96 | 0.90 | 3.25 | 0.80 to 0.97 |
| 7 | −4.81 | 0.88 | 3.35 | 0.74 to 0.93 |
| 8 | −3.65 | 0.86 | 3.39 | 0.93 to 0.96 |
| 9 | −2.47 | 0.85 | 3.45 | 0.91 to 0.95 |
| 10 | −1.32 | 0.84 | 3.52 | 0.67 to 0.91 |
| 11 | −0.18 | 0.84 | 3.57 | 0.62 to 0.93 |
| 12 | 0.99 | 0.85 | 3.60 | 0.94 to 0.97 |
| 13 | 2.15 | 0.87 | 3.61 | 0.65 to 0.98 |
| 14 | 3.29 | 0.89 | 3.61 | 0.69 to 1.01 |
| 15 | 4.46 | 0.91 | 3.58 | 0.82 to 0.94 |
| 16 | 5.61 | 0.95 | 3.51 | 0.91 to 1.11 |
| 17 | 6.74 | at the sill line, 1.20 | 3.38 | the widest at or above it |
| 18 | 7.92 | at the sill line, 1.27 | 3.23 | the widest at or above it |

- The half-breadth is the plan's heavy line within 0.04 m at every station from 2 to 16 (measured):
  the lines plate's heavy line is the main breadth for all but the eye.
- **The narrow bands** at stations 3, 8, 9 and 12 are one trace's, its 0.012 ft under half a pixel. A
  second reader's traces gave 0.92 to 1.29 m at station 5, 0.63 to 1.02 at 8, 0.53 to 1.03 at 10 and 0.85
  to 1.44 at 16 (measured). So the smooth curve may leave a narrow band, by up to 0.09 m: the bands are
  no limits, and the height is judgement.
- No line on any sheet marks a height of breadth (read). Steel's rule puts it a few inches above the
  load line (`Build-Ships.md` §5.3): *Lynx*'s stands about 2 ft 9 in above hers, as a low-sided
  vessel of slack bilge with a straight side above the water may (judgement).

### 5.8 The sections by station

[z, half-breadth] in metres, moulded, on planes square to the water at each station's x (so a line's
half-breadth is taken at its own x along the line, the drawing's stations being square to the keel:
arithmetic). The water and the rail at each x are §6.1's `breadth_m`.

- **Below WL3**: off the body plan at fixed heights above the keel's top line, the dark run nearest
  where the section's slope puts it (`secs.py`), then at −1.9, −2.4 and −2.9 m by the stations' own
  x's: ±0.15 ft, worse where the outer sections of each half merge into one band below about 3 ft
  above the rabbet (stations 9 to 16; read). The lowest given is 0.10 m above the rabbet.
- **WL3, WL2, the sill line**: the lines plate (§5.2), at the plane.
- **Between the water and the sill line**: at 0.35 and 0.7 of the height, off the body plan, followed
  up from the LWL node and down from the sill node, each over the half nearer its start, the ends on
  the plate's half-breadths (`upper.py`, `upper2.py`, `upper3.py`): ±0.2 ft where the body plan stands
  off the lines plate (the third reader, below). The stern's S shows
  here, the hollow of the run reaching the sill line at stations 0 to 3.
- **Station 23** stands in the stem below z +0.39 m, where it leaves the stem's siding (read).
- **The sill line's half-breadth is the plan's heavy line** (§5.1). The section crossed directly at the
  sill's height, on the plane, net of the body plan's excess at the water, stands at stations 17 to 21
  at 3.38, 3.23, 2.95, 2.60 and 2.09 m (measured, by a second reader), against the list's 3.37, 3.19,
  2.92, 2.54 and 2.02 m. The list stays on the plate by this note's rule, and is marked so here; the
  most of it, 0.07 m, is under the 2 px of `Build-Ships.md` §5.0 principle 2 at her scale (judgement).
- **The third reader** (the hull's review, §9) followed the sections from station 3 to station 22 on the
  body plan, by columns below the water and by rows above it, numbered them by their crossings of the
  plate's waterlines, and read them at y = 1400.3 − 33.26 H px on both halves, the line that meets the
  dashed base. At WL3 the body plan's stations 9, 10 and 11 stand 0.11, 0.10 and 0.08 m outside the lines
  plate (measured). A point of this table should lie between the section as drawn on the body plan and
  the section moved to the plate's node (that difference straight to nothing at the rabbet, below WL3).
  Seven did not, and station 9's at z −1.90 stood on the section as drawn where its neighbours stand on the
  moved one (0.25 m of second difference along the ship). The eight are mended here (measured), the first
  reading's figures being: station 5 at z 0.36, 3.11; station 8 at z 0.33 and 0.67, 3.30 and 3.35; station 9
  at z −1.90 and −2.40, 1.47 and 0.83; stations 10, 11 and 12 at z −2.40, 0.79, 0.70 and 0.58. Each now stands
  on the moved section. The others lie within 0.06 m of it above the water and within 0.05 m below it. The
  first three are in the band that heel lifts out of the water; none moves the owner's picture by 2 px, since
  the drawn side is filled and its widest at each height is amidships (judgement; the sheets drawn again
  show none).

| Stn | x (m) | [z, half-breadth], moulded |
|---|---|---|
| 0 | −12.86 | [0.45, 0.79], [0.90, 2.11], [1.29, 2.57] |
| 1 | −11.75 | [−1.90, 0.12], [−0.71, 0.40], [0.43, 1.71], [0.86, 2.48], [1.22, 2.70] |
| 2 | −10.58 | [−2.90, 0.11], [−2.40, 0.16], [−1.90, 0.26], [−1.38, 0.41], [−0.71, 0.81], [0.41, 2.36], [0.82, 2.73], [1.16, 2.83] |
| 3 | −9.44 | [−2.90, 0.14], [−2.40, 0.25], [−1.90, 0.40], [−1.38, 0.65], [−0.71, 1.24], [0.39, 2.66], [0.77, 2.90], [1.10, 2.95] |
| 4 | −8.29 | [−2.90, 0.17], [−2.40, 0.33], [−1.90, 0.55], [−1.38, 0.92], [−0.71, 1.70], [0.37, 2.87], [0.74, 3.02], [1.06, 3.05] |
| 5 | −7.11 | [−2.90, 0.21], [−2.40, 0.43], [−1.90, 0.74], [−1.38, 1.23], [−0.71, 2.10], [0.36, 3.02], [0.72, 3.14], [1.02, 3.15] |
| 6 | −5.96 | [−2.90, 0.22], [−2.40, 0.53], [−1.90, 0.92], [−1.38, 1.50], [−0.71, 2.40], [0.35, 3.17], [0.69, 3.25], [0.99, 3.23] |
| 7 | −4.81 | [−2.40, 0.60], [−1.90, 1.11], [−1.38, 1.75], [−0.71, 2.64], [0.34, 3.29], [0.68, 3.34], [0.97, 3.32] |
| 8 | −3.65 | [−2.40, 0.69], [−1.90, 1.30], [−1.38, 1.96], [−0.71, 2.82], [0.33, 3.34], [0.67, 3.39], [0.96, 3.39] |
| 9 | −2.47 | [−2.40, 0.70], [−1.90, 1.38], [−1.38, 2.11], [−0.71, 2.95], [0.33, 3.41], [0.66, 3.44], [0.95, 3.45] |
| 10 | −1.32 | [−2.40, 0.68], [−1.90, 1.39], [−1.38, 2.22], [−0.71, 3.04], [0.33, 3.48], [0.66, 3.51], [0.94, 3.51] |
| 11 | −0.18 | [−2.40, 0.59], [−1.90, 1.40], [−1.38, 2.29], [−0.71, 3.11], [0.33, 3.54], [0.67, 3.57], [0.96, 3.56] |
| 12 | 0.99 | [−2.40, 0.51], [−1.90, 1.42], [−1.38, 2.32], [−0.71, 3.14], [0.34, 3.53], [0.68, 3.57], [0.97, 3.60] |
| 13 | 2.15 | [−2.40, 0.50], [−1.90, 1.41], [−1.38, 2.27], [−0.71, 3.12], [0.35, 3.55], [0.70, 3.61], [1.00, 3.61] |
| 14 | 3.29 | [−1.90, 1.26], [−1.38, 2.14], [−0.71, 3.04], [0.36, 3.53], [0.72, 3.61], [1.04, 3.60] |
| 15 | 4.46 | [−1.90, 1.13], [−1.38, 1.96], [−0.71, 2.89], [0.38, 3.44], [0.76, 3.57], [1.08, 3.55] |
| 16 | 5.61 | [−1.90, 0.98], [−1.38, 1.72], [−0.71, 2.63], [0.40, 3.39], [0.80, 3.49], [1.14, 3.48] |
| 17 | 6.74 | [−1.90, 0.72], [−1.38, 1.42], [−0.71, 2.32], [0.42, 3.28], [0.84, 3.38], [1.20, 3.37] |
| 18 | 7.92 | [−1.90, 0.49], [−1.38, 1.09], [−0.71, 1.95], [0.44, 3.05], [0.89, 3.20], [1.27, 3.19] |
| 19 | 9.06 | [−1.90, 0.33], [−1.38, 0.76], [−0.71, 1.53], [0.47, 2.73], [0.93, 2.92], [1.33, 2.92] |
| 20 | 10.24 | [−1.38, 0.44], [−0.71, 1.06], [0.49, 2.27], [0.99, 2.52], [1.41, 2.54] |
| 21 | 11.36 | [−1.38, 0.15], [−0.71, 0.61], [0.52, 1.64], [1.05, 1.97], [1.49, 2.02] |
| 22 | 12.51 | [−0.71, 0.11], [0.55, 0.88], [1.11, 1.16], [1.59, 1.36] |
| 23 | 13.67 | [0.39, 0.12], [1.67, 0.60] |

### 5.9 The stern (read and measured)

- **The transom** is a flat face seen from the side (read), the type `raked`, and no counter worth a
  key (below). The drawn face rakes 34.1° to 34.9° to the page on leaf 108, 34.7° to 34.8° on leaf 109
  and 33.9° by the plan's two line ends; **37.8° to 38.6° to the water's square** (measured). The chord from the
  taffrail to the post's head, 41.4° and 45.1°, crosses the band and is no drawn line. The face's lower
  end is §5.3's, 0.17 m abaft that chord.
- **Its half-breadths**, by three sheets (measured):

| At | Lines plate, moulded | Body plan | Deck plan |
|---|---|---|---|
| The taffrail | **7.40 ft (2.26 m)**, the plan's thin line ending square at the taffrail's x | 7.71 ft (2.35 m), the outline's corner | 7.38 ft, 7.72 ft and 7.94 ft (its three lines, 2.25, 2.35 and 2.42 m) |
| The sill line's end, the knuckle | **7.48 ft (2.28 m)**, the plan's heavy line ending square 66 px forward, at x −15.00, z 1.31 on the face's plane | 7.77 ft (2.37 m) | |
| The widest of the face, about two-thirds down | | 8.13 ft (2.48 m) | |

  The lines plate's and the deck plan's innermost agree, moulded; the body plan and the deck plan's
  second line stand 0.3 ft outside them, nearly the plank and more (judgement). §5.7's 2.25 m is the
  lines plate's and is kept: the body plan's 2.35 m is recorded (`Build-Ships.md` §5.7).
- **Its crown** (measured on the body plan): the taffrail rises 0.44 ft (5 in) from the corner to the
  middle line; the foot, a band of two lines 0.25 ft apart crossing at the sill line's level, rises
  **0.57 ft (0.17 m)**.
- **Below the band** the outline closes in a U to a flat foot at the middle 1.4 ft below the band's
  side, the hull's short counter meeting the post's head (read; the replica's "short counter",
  `Build-Ships.md` §5.8, for the eye). `form.stern` has no key for it; `knuckle_z_m` is the band's
  side, where the side plate's sill line ends (§5.3).
- **Two ports in the transom** (p. 83, read (OCR) l. 4855; one on the body plan's after half, read),
  each 1.94 ft wide by 1.78 ft high as seen (2.5 ft along the rake),
  centred 3.86 ft (1.18 m) off the middle line, the sill 0.79
  ft and the head 2.56 ft above the band's side (measured). A box on the
  side view's transom marks them (read). Neither file's fit puts a gun in them: not triples
  (judgement, §6.3); for package 81.
- **No lights and no galleries** on any sheet (read); "a very plain transom" (p. 83, read).
- **The rudder**: §5.3; with three pintle straps (read); its head rises to about 0.9 m above the line
  beside the knuckle (measured, tentative); she apparently steered with a tiller (p. 83, read).

### 5.10 The masts, the channels and the bowsprit (measured)

| | Main | Fore |
|---|---|---|
| The axis at the sill line, x (m) | −2.60 | +8.26 |
| At the water; at the rail, x (m) | −2.37; −2.83 | +8.66; +8.08 |
| The rake on the plate, to the keel's square (fit over ten rows; leaf 109 agrees within 0.4°) | 9.9° | 13.5° |
| The rake to the water's square, the drag added | **13.6°** | **17.2°** |
| Across the stump, along the row | 1.51 ft | 1.55 ft |
| Channel: x from, to (m); its top z (m) | −5.18 to −2.54; 1.53 to 1.49 | +5.26 to +8.45; 1.64 to 1.84 |
| Deadeyes a side | three | four |

- The channels stand on the bulwark about 1¼ ft below the rail (read, measured), abaft each mast's
  place, not on a wale.
- Chapelle has both masts raking the same and very sharply aft (p. 82, read (OCR) l. 4839-4840). On
  the plate they differ by 3.6°, the fore raking the more (measured, both plates). The files'
  11.3° (1 in 5, for both) lies between them to the keel and under both to the water.
- **The bowsprit** passes over the stem head and through the bulwark, its upper edge steeved 9.2° and
  its lower edge 10.5° to the water, its heel inboard (measured). Its stump ends about 2 m beyond the
  knee (read); no length is on the plates.

### 5.11 The keel and the rabbet (measured)

- **The rabbet** is one line of a pair along the post, the keel and the stem, 0.2 ft apart. On the keel
  and the stem the thin line lies inside the heavy; on the post it lies aft of the heavy, toward the post.
  The plan's waterline hooks stop on the thin line at both ends, so which member is the rabbet is
  tentative (judgement). §6.1's `rabbet` and the waterline's length (§4) are on the heavy line, and
  §5.8's levels stop above it. It steps about 0.07 m at the heel, from the keel's upper line to its heavy
  line, and the post's pair ends at the strap near y 1455.
- **The siding** (the body plan's keel, below its base): 23.9 px, **8.6 in** at the keel; the lines at
  which the sections end stand 0.29 ft off the middle line aft and 0.39 ft forward (measured). Steel's
  schooner: 9, 10½ and 9 in (Folio I, rows R-T, read).
- **The keel's depth**: 1 ft 5 in at the heel to 1 ft 9 in at the forefoot, a joint 0.3 ft above its
  lower edge the false keel's (the body plan 0.2 ft; judgement).
- **The rising line** and the floor's half-breadth: not drawn (read).

## 6. For the profile (B8): the points in metres

### 6.1 On the plates (*Lynx*'s own frame)

`x` forward of the mid-perpendiculars along the load line, `z` above it (§0's frame), moulded;
from §4-§5 (measured unless marked). `tools/ships/hull_schooner.py` holds these lists.

- **`rail`** (the rail cap's top): [−15.88, 2.44], [−13.00, 2.23], [−11.90, 2.17], [−10.71, 2.10],
  [−9.57, 2.04], [−8.42, 1.98], [−7.24, 1.94], [−6.08, 1.91], [−4.93, 1.89], [−3.77, 1.88], [−2.59,
  1.87], [−1.44, 1.87], [−0.30, 1.87], [0.87, 1.88], [2.03, 1.90], [3.16, 1.94], [4.33, 1.98],
  [5.48, 2.03], [6.61, 2.08], [7.78, 2.15], [8.92, 2.23], [10.09, 2.30], [11.20, 2.38], [12.35,
  2.47], [13.51, 2.57], [14.30, 2.64], [14.86, 2.70].
- **`breadth`** [x, at the line, at the rail], each on the plane of the station: [−12.86, 0.34,
  2.57], [−11.75, 0.97, 2.70], [−10.58, 1.70, 2.81], [−9.44, 2.23, 2.91], [−8.29, 2.59, 3.00],
  [−7.11, 2.86, 3.10], [−5.96, 3.03, 3.19], [−4.81, 3.18, 3.26], [−3.65, 3.27, 3.34], [−2.47, 3.33,
  3.41], [−1.32, 3.40, 3.46], [−0.18, 3.45, 3.51], [0.99, 3.47, 3.54], [2.15, 3.47, 3.56], [3.29,
  3.44, 3.55], [4.46, 3.36, 3.55], [5.61, 3.23, 3.48], [6.74, 3.03, 3.36], [7.92, 2.72, 3.18],
  [9.06, 2.30, 2.97], [10.24, 1.78, 2.66], [11.36, 1.20, 2.25], [12.51, 0.54, 1.64], [13.67, 0.12,
  0.90]. The last is station 23, in the stem, carried to the plane as the others; the taffrail is
  §5.9.
- **`sill line`** [x, z, half-breadth of the plan's heavy line] by station, from the knuckle forward
  (§5.1, §5.2): [−14.77, 1.34], [−12.94, 1.29, 2.56], [−11.83, 1.23, 2.69], [−10.65, 1.17, 2.82],
  [−9.51, 1.11, 2.94], [−8.36, 1.06, 3.05], [−7.18, 1.03, 3.14], [−6.02, 0.99, 3.23], [−4.87, 0.97,
  3.31], [−3.71, 0.96, 3.39], [−2.53, 0.95, 3.45], [−1.38, 0.94, 3.51], [−0.24, 0.96, 3.56], [0.93,
  0.97, 3.60], [2.09, 1.00, 3.61], [3.22, 1.03, 3.60], [4.39, 1.08, 3.56], [5.54, 1.14, 3.49],
  [6.67, 1.20, 3.38], [7.83, 1.26, 3.21], [8.98, 1.33, 2.95], [10.15, 1.41, 2.58], [11.26, 1.49,
  2.07], [12.41, 1.58, 1.43], [13.57, 1.67, 0.67].
- **`keel`** (the lower edge): [−11.54, −3.91], [−8.93, −3.76], [−4.63, −3.52], [−0.34, −3.28],
  [3.95, −3.04], [8.24, −2.80], [10.60, −2.65].
- **`stem`** (the fore edge; the knee is apart, §5.3): [10.60, −2.65], [10.98, −2.49], [12.08,
  −1.77], [12.91, −1.06], [13.55, −0.37], [13.85, 0.00], [14.21, 0.53], [14.26, 0.75], [14.39,
  0.98], [14.48, 1.20], [14.58, 1.42], [14.65, 1.64], [14.71, 1.77], [14.67, 2.07], [14.75, 2.29],
  [14.82, 2.51], [14.86, 2.70]. The fifth from the top is the bowsprit's underside.
- **`head`** (the knee of the head, §5.3): [14.21, 0.53], [14.35, 0.76], [14.48, 0.98], [14.61,
  1.21], [14.75, 1.43], [14.88, 1.55], [15.00, 1.62], [15.13, 1.65], [15.26, 1.70], [15.32, 1.73],
  [15.38, 1.80], [15.41, 1.85].
- **`stern`** (the post's after edge, the post's head at the knuckle, the transom's lower corner,
  the taffrail; tentative, §5.3): [−11.54, −3.91], [−12.11, −2.91], [−12.73, −1.87], [−13.36,
  −0.83], [−13.87, 0.00], [−14.11, 0.41], [−14.77, 1.34], [−15.22, 1.62], [−15.88, 2.44]. The
  rudder's after edge, for the drawing: [−12.44, −3.94], [−12.90, −2.96], [−13.40, −1.91], [−13.90,
  −0.86], [−14.32, 0.00], [−14.72, 0.83].
- **`rabbet`** [x, z, half-siding] (§5.11, tentative on the post, stepped at the heel): [−13.79,
  0.54, 0.09], [−13.55, 0.23, 0.09], [−13.32, −0.07, 0.09], [−13.09, −0.38, 0.09], [−12.63, −1.00,
  0.09], [−12.23, −1.62, 0.09], [−11.76, −2.24, 0.09], [−11.27, −2.85, 0.09], [−10.86, −3.44, 0.11],
  [−8.52, −3.36, 0.11], [−4.23, −3.09, 0.11], [0.06, −2.82, 0.11], [4.35, −2.56, 0.11], [8.64,
  −2.29, 0.11], [9.71, −2.15, 0.11], [10.77, −1.84, 0.12], [11.81, −1.36, 0.12], [12.84, −0.63,
  0.12], [13.85, 0.48, 0.12], [14.38, 1.41, 0.12], [14.50, 1.74, 0.12].
- **`deck` at side** (judgement, §5.5: the middle line less 0.14 m): [−14.44, 1.16], [−13.00, 1.09],
  [−11.90, 1.05], [−10.71, 1.00], [−9.57, 0.95], [−8.42, 0.90], [−7.24, 0.88], [−6.08, 0.86],
  [−4.93, 0.84], [−3.77, 0.83], [−2.59, 0.82], [−1.44, 0.82], [−0.30, 0.82], [0.87, 0.82], [2.03,
  0.83], [3.16, 0.86], [4.33, 0.89], [5.48, 0.93], [6.61, 0.97], [7.78, 1.02], [8.92, 1.08], [10.09,
  1.13], [11.20, 1.18], [12.35, 1.24], [13.51, 1.30], [14.06, 1.33].
- **`ports`** [x, sill, half-breadth], with the width: §6.3's table.

### 6.2 The factors (`Build-Ships.md` §5.0 principle 7)

The two files stand for the type and not for *Lynx*: S† (§5.7), scaled, the mark `stand-in`.

| Factor | Figure | From |
|---|---|---|
| Lengths, k_L | **0.9650** | the files' `length_waterline_m` 25.9 over *Lynx*'s 26.84 m rabbet to rabbet (§4), the way *Spider*'s class states it (arithmetic). x' = k_L x. On the thin lines, 26.79 m, it would be 0.9668, recorded (§5.11) |
| Sections, k_B | **0.9979** | the files' `beam_m` 7.3 over *Lynx*'s 24 ft 0 in (7.315 m) (arithmetic). Below the water z' = k_B z; each half-breadth, with its plank, by k_B |
| Plank | **0.051 m** a side | 2 in, the extreme breadth less the moulded, halved (read, arithmetic), added to every half-breadth but the keel's and the stem's siding |
| The side's height | **none** at the lowest sill | the lowest sill, port 3's 0.948 m, stands where the plate has it: `Build-Ships.md` §5.4's source for these files' sills as the lead ruled it, as principle 7's third line takes it |
| The sheer's rise above it | k_L | the sill line S'(x) = 0.948 + k_L (S(x) − 0.948), S the plate's |
| Between the water and the sill line | z' = z S'/S | straight (judgement), so that the water keeps its half-breadths and the side meets the sill line |
| Above the sill line | z' = S' + k_B (z − S) | the bulwark by the sections' factor (judgement) |

- **Ruled (the lead, 2026-10-31): the plate's 3 ft 1 in over *Spider*'s 3 ft 5 in of 1835, her own
  sheet over a later ship's.** §5.4 and the file's own note first named *Spider*, and the plate's own
  3 ft 1 in is Steel's 3 ft 1 in to the inch (§10.1). The lift is one figure, the lowest sill, and
  everything else follows. Old beside new: the lowest sill 1.04 m, *Spider*'s, +0.09 m, shut at 12.1°
  on the lowest port's own half-breadth and 11.6° on half the beam; now 0.95 m, shut at 10.6° and
  10.2°. Every `z` above the water falls by the lift, 0.09 m at the sill and straight to nothing at the
  water: rail, deck, sills and head all take §6.1's heights with the rise by k_L. With the lift, ports
  2, 3 and 6 stood within 0.03 m of *Spider*'s aft, midship and fore figures (§5.4 keeps them beside
  the plate's).
- **The depth so drawn**, recorded (§6.5): the keel at z −3.14 m at the dead flat against the files'
  3.3 m mean draught.

### 6.3 The port triples (`Build-Ships.md` §5.1, §5.4)

Seven a side on the plate (§5.4). The sill is the sill line's at the port's centre, the half-breadth the
plate's heavy line there, each measured on the plate and never from the drawing; the bold columns are
the files' frame, deck word `upper`. "Shut" is the heel at which the sill falls to `PORT_SHUT_M` above
the water on the triple's half-breadth, heel alone (arithmetic: its sine is the sill less 0.3048 m over
the half-breadth, `shot.lee_port_shut`, as `Build-Ships.md` §5.4's table).

| Port | x, plate | Sill, plate | ½-br., plate | **x** | **Sill** | **½-br., plank on** | Shut |
|---|---|---|---|---|---|---|---|
| 1 | −11.25 | 1.20 | 2.75 | **−10.86** | **1.19** | **2.79** | 18.5° |
| 2 | −7.20 | 1.03 | 3.14 | **−6.95** | **1.03** | **3.18** | 13.2° |
| 3 | −2.16 | 0.95 | 3.47 | **−2.08** | **0.95** | **3.51** | 10.6° |
| 4 | 0.97 | 0.97 | 3.60 | **0.94** | **0.97** | **3.64** | 10.5° |
| 5 | 4.98 | 1.11 | 3.52 | **4.81** | **1.11** | **3.56** | 13.1° |
| 6 | 8.80 | 1.32 | 2.99 | **8.49** | **1.31** | **3.03** | 19.4° |
| 7 | 11.82 | 1.53 | 1.76 | **11.41** | **1.51** | **1.81** | 41.7° |

- **`port_size_m.upper`**: [0.61, 0.82], the mean width by k_L and the mean opening from the sill to the
  rail's heavy line, by k_B (§5.4). *Spider*'s class: [0.76, 0.64]; Steel's schooner: [0.56, 0.53]
  (Folio XXXII, rows S and T, read).
- **The half-breadths are the plan's heavy line** (§5.1): the section at the sill's height stands +0.05 m
  at port 6 and +0.02 m at port 7 (measured). The list stays on the plate.
- **The two transom ports** are no triples (§5.9): neither file has a gun in them, and at the rake
  a triple's half-breadth is not the side's. In the files' frame their sills stand at z 1.57 m,
  x about −14.6 m on the face, 1.18 m off the middle line.

**The guns' places.** `Build-Ships.md` §5.3 says that no gun's `x_m` moves, and its §4.4 and truth 7-185
that every port gun stands on a triple of its deck to the centimetre. None of the five places of the
privateer's two fits stands on a port of the plate. So the file keeps both rules: ports 1, 3 and 5, in
which no gun of either fit stands, are the plate's, and each other port stands at its guns' own place,
sill and half-breadth read on the same measured lines (judgement). The second port stands at two places,
one for each fit, so the plate's seven are **eight triples**, 0.90 m apart at the pair, wider than the
port by 0.29 m. Five of the eight stand where the plate has no port, so `ports_m` takes the word `judged`
(a line takes the word of its weakest point, `Build-Ships.md` §5.0 principle 4), its sills and half-breadths
still measured. The file's notes say so. Nothing else of the guns moves; their `height_m` is the sill, as
§5.3 has it, read by nothing before the lee port's L2.

| Guns | **`x_m`**, unmoved | The plate's port | Its place in the file's frame | **Sill** | **½-br., plank on** | Rail | Shut |
|---|---|---|---|---|---|---|---|
| long 6s, 3rd pair | **−8.40** | 2 | −6.95 (off by 1.45 m) | **1.07** | **3.06** | 1.98 | 14.5° |
| carronades, 2nd pair | **−7.50** | 2 | −6.95 (off by 0.55 m) | **1.04** | **3.14** | 1.95 | 13.5° |
| long 6s, 2nd pair | **0.00** | 4 | 0.94 (off by 0.94 m) | **0.96** | **3.61** | 1.87 | 10.5° |
| long 6s, 1st pair | **8.40** | 6 | 8.49 (off by 0.09 m) | **1.30** | **3.06** | 2.20 | 19.0° |
| carronades, 1st pair | **10.50** | 7 | 11.41 (off by 0.91 m) | **1.44** | **2.29** | 2.34 | 29.7° |

- **For the landing:** the other way is to move the guns to the plate's ports, which moves `x_m`, read by
  the quarters and the divisions (`Build-Ships.md` §5.3): not this step's to do. The viewer's strake of
  ports ends at the foremost triple, so it stops 0.91 m short of the plate's port 7 until the guns move.
  The pivot's and the swivels' `height_m` take the rail at their own x's: 1.92 m at +2.6, 2.30 m at +10,
  2.07 m at −10 (§5.3).

### 6.4 The files' points

For both files, alike (`Build-Ships.md` §5.0 principle 10), as the generator writes them. `x` forward
of midships, `z` above the file's waterline, half-breadths plank on (§6.2), to the centimetre.

- **`rail_m`**: [−15.32, 2.42], [−12.54, 2.22], [−11.48, 2.16], [−10.33, 2.09], [−9.23, 2.03],
  [−8.13, 1.97], [−6.99, 1.94], [−5.87, 1.91], [−4.76, 1.89], [−3.64, 1.88], [−2.50, 1.87], [−1.39,
  1.87], [−0.29, 1.87], [0.84, 1.88], [1.96, 1.90], [3.05, 1.94], [4.18, 1.97], [5.29, 2.02], [6.38,
  2.07], [7.51, 2.14], [8.61, 2.21], [9.74, 2.28], [10.81, 2.36], [11.92, 2.45], [13.04, 2.54],
  [13.80, 2.61], [14.34, 2.67].
- **`breadth_m`**: [−12.41, 0.39, 2.62], [−11.34, 1.02, 2.75], [−10.21, 1.75, 2.85], [−9.11, 2.28,
  2.95], [−8.00, 2.64, 3.04], [−6.86, 2.90, 3.14], [−5.75, 3.07, 3.23], [−4.64, 3.22, 3.30], [−3.52,
  3.31, 3.38], [−2.38, 3.37, 3.45], [−1.27, 3.44, 3.50], [−0.17, 3.49, 3.55], [0.96, 3.51, 3.58],
  [2.07, 3.51, 3.60], [3.17, 3.48, 3.59], [4.30, 3.40, 3.59], [5.41, 3.27, 3.52], [6.50, 3.07,
  3.40], [7.64, 2.77, 3.22], [8.74, 2.35, 3.01], [9.88, 1.83, 2.71], [10.96, 1.25, 2.30], [12.07,
  0.59, 1.69], [13.19, 0.12, 0.95]. The last is station 23: its water figure is the stem's
  half-siding.
- **`keel_m`**: [−11.14, −3.90], [−8.62, −3.75], [−4.47, −3.51], [−0.33, −3.27], [3.81, −3.03],
  [7.95, −2.79], [10.23, −2.64].
- **`stem_m`**: [10.23, −2.64], [10.60, −2.48], [11.66, −1.77], [12.46, −1.06], [13.08, −0.37],
  [13.36, 0.00], [13.71, 0.52], [13.76, 0.74], [13.89, 0.97], [13.97, 1.18], [14.07, 1.40], [14.14,
  1.62], [14.19, 1.74], [14.16, 2.04], [14.23, 2.26], [14.30, 2.48], [14.34, 2.67].
- **`stern_m`**: [−11.14, −3.90], [−11.69, −2.90], [−12.28, −1.87], [−12.89, −0.83], [−13.38, 0.00],
  [−13.62, 0.41], [−14.25, 1.33], [−14.69, 1.61], [−15.32, 2.42]. The rudder's after edge, for a
  later drawing: [−12.00, −3.93], [−12.45, −2.95], [−12.93, −1.91], [−13.41, −0.86], [−13.82, 0.00],
  [−14.20, 0.82].
- **`wales_m`, `channel_wales_m`**: none (§8). The planksheer's band, 0.19 ft under the sill line, and
  the channels (§5.10) are recorded in words; neither is a wale.
- **`section_m`** [z, half-breadth], the keel to the rail at station 13: [−3.13, 0.11], [−2.68,
  0.11], [−2.40, 0.55], [−1.90, 1.46], [−1.38, 2.32], [−0.71, 3.16], [0.00, 3.51], [0.35, 3.59],
  [0.70, 3.65], [1.00, 3.65], [1.91, 3.60].
- **`decks_m.upper`**: [−13.93, 1.15], [−12.54, 1.08], [−11.48, 1.04], [−10.33, 0.99], [−9.23,
  0.95], [−8.13, 0.90], [−6.99, 0.88], [−5.87, 0.86], [−4.76, 0.84], [−3.64, 0.83], [−2.50, 0.82],
  [−1.39, 0.82], [−0.29, 0.82], [0.84, 0.82], [1.96, 0.83], [3.05, 0.86], [4.18, 0.89], [5.29,
  0.92], [6.38, 0.96], [7.51, 1.01], [8.61, 1.07], [9.74, 1.12], [10.81, 1.17], [11.92, 1.22],
  [13.04, 1.28], [13.57, 1.31]. Every sill stands above it (by 0.13 to 0.28 m).
- **`ports_m.upper`** (§6.3: eight triples for the plate's seven): [−10.86, 1.19, 2.79], [−8.40,
  1.07, 3.06], [−7.50, 1.04, 3.14], [−2.08, 0.95, 3.51], [0.00, 0.96, 3.61], [4.81, 1.11, 3.56],
  [8.40, 1.30, 3.06], [10.50, 1.44, 2.29].
- **`port_size_m.upper`**: [0.61, 0.82].
- **`head_m`**: [13.71, 0.52], [13.85, 0.75], [13.97, 0.97], [14.10, 1.19], [14.23, 1.41], [14.36,
  1.53], [14.47, 1.60], [14.60, 1.63], [14.73, 1.67], [14.78, 1.70], [14.84, 1.77], [14.87, 1.82].
- **`breadth_line_m`** [x, z, half-breadth], stations 2 to 16: [−10.21, 1.14, 2.87], [−9.11, 1.05,
  2.99], [−8.00, 1.00, 3.09], [−6.86, 0.95, 3.19], [−5.75, 0.90, 3.29], [−4.64, 0.88, 3.39], [−3.52,
  0.86, 3.43], [−2.38, 0.85, 3.49], [−1.27, 0.84, 3.56], [−0.17, 0.84, 3.61], [0.96, 0.85, 3.64],
  [2.07, 0.87, 3.65], [3.17, 0.89, 3.65], [4.30, 0.91, 3.62], [5.41, 0.94, 3.55].
- **`sections_m`**, by x, each [z, half-breadth]: WL3, WL2 and the sill line by the plate, the rest by
  the body plan (§5.8). The water and the rail at each x are `breadth_m`'s.
  - −12.41: [0.45, 0.84], [0.89, 2.16], [1.28, 2.62]
  - −11.34: [−1.90, 0.17], [−0.71, 0.45], [0.43, 1.76], [0.85, 2.53], [1.21, 2.75]
  - −10.21: [−2.89, 0.16], [−2.40, 0.21], [−1.90, 0.31], [−1.38, 0.46], [−0.71, 0.86], [0.41, 2.41], [0.81, 2.78], [1.15, 2.87]
  - −9.11: [−2.89, 0.19], [−2.40, 0.30], [−1.90, 0.45], [−1.38, 0.70], [−0.71, 1.29], [0.39, 2.71], [0.77, 2.94], [1.09, 2.99]
  - −8.00: [−2.89, 0.22], [−2.40, 0.38], [−1.90, 0.60], [−1.38, 0.97], [−0.71, 1.75], [0.37, 2.91], [0.74, 3.06], [1.06, 3.09]
  - −6.86: [−2.89, 0.26], [−2.40, 0.48], [−1.90, 0.79], [−1.38, 1.28], [−0.71, 2.15], [0.36, 3.06], [0.72, 3.18], [1.02, 3.19]
  - −5.75: [−2.89, 0.27], [−2.40, 0.58], [−1.90, 0.97], [−1.38, 1.55], [−0.71, 2.45], [0.35, 3.21], [0.69, 3.29], [0.99, 3.27]
  - −4.64: [−2.40, 0.65], [−1.90, 1.16], [−1.38, 1.80], [−0.71, 2.69], [0.34, 3.33], [0.68, 3.38], [0.97, 3.36]
  - −3.52: [−2.40, 0.74], [−1.90, 1.35], [−1.38, 2.01], [−0.71, 2.86], [0.33, 3.38], [0.67, 3.43], [0.96, 3.43]
  - −2.38: [−2.40, 0.75], [−1.90, 1.43], [−1.38, 2.16], [−0.71, 2.99], [0.33, 3.45], [0.66, 3.48], [0.95, 3.49]
  - −1.27: [−2.40, 0.73], [−1.90, 1.44], [−1.38, 2.27], [−0.71, 3.08], [0.33, 3.52], [0.66, 3.55], [0.94, 3.55]
  - −0.17: [−2.40, 0.64], [−1.90, 1.45], [−1.38, 2.34], [−0.71, 3.15], [0.33, 3.58], [0.67, 3.61], [0.96, 3.60]
  - 0.96: [−2.40, 0.56], [−1.90, 1.47], [−1.38, 2.37], [−0.71, 3.18], [0.34, 3.57], [0.68, 3.61], [0.97, 3.64]
  - 2.07: [−2.40, 0.55], [−1.90, 1.46], [−1.38, 2.32], [−0.71, 3.16], [0.35, 3.59], [0.70, 3.65], [1.00, 3.65]
  - 3.17: [−1.90, 1.31], [−1.38, 2.19], [−0.71, 3.08], [0.36, 3.57], [0.72, 3.65], [1.04, 3.64]
  - 4.30: [−1.90, 1.18], [−1.38, 2.01], [−0.71, 2.93], [0.38, 3.48], [0.76, 3.61], [1.08, 3.59]
  - 5.41: [−1.90, 1.03], [−1.38, 1.77], [−0.71, 2.68], [0.40, 3.43], [0.80, 3.53], [1.13, 3.52]
  - 6.50: [−1.90, 0.77], [−1.38, 1.47], [−0.71, 2.37], [0.42, 3.32], [0.83, 3.42], [1.19, 3.41]
  - 7.64: [−1.90, 0.54], [−1.38, 1.14], [−0.71, 2.00], [0.44, 3.09], [0.88, 3.24], [1.26, 3.23]
  - 8.74: [−1.90, 0.38], [−1.38, 0.81], [−0.71, 1.58], [0.47, 2.78], [0.92, 2.96], [1.32, 2.96]
  - 9.88: [−1.38, 0.49], [−0.71, 1.11], [0.48, 2.32], [0.98, 2.57], [1.39, 2.59]
  - 10.96: [−1.38, 0.20], [−0.71, 0.66], [0.51, 1.69], [1.04, 2.02], [1.47, 2.07]
  - 12.07: [−0.71, 0.16], [0.54, 0.93], [1.09, 1.21], [1.57, 1.41]
  - 13.19: [0.38, 0.12], [1.64, 0.65]
- **`rabbet_m`** [x, z, half-siding] (reserved, not drawn; principle 11): [−13.31, 0.53, 0.09],
  [−13.08, 0.23, 0.09], [−12.85, −0.07, 0.09], [−12.63, −0.38, 0.09], [−12.19, −1.00, 0.09],
  [−11.80, −1.62, 0.09], [−11.35, −2.24, 0.09], [−10.88, −2.84, 0.09], [−10.48, −3.43, 0.11],
  [−8.22, −3.35, 0.11], [−4.08, −3.08, 0.11], [0.06, −2.81, 0.11], [4.20, −2.55, 0.11], [8.34,
  −2.29, 0.11], [9.37, −2.15, 0.11], [10.39, −1.84, 0.12], [11.40, −1.36, 0.12], [12.39, −0.63,
  0.12], [13.36, 0.47, 0.12], [13.88, 1.39, 0.12], [13.99, 1.71, 0.12].
- **`floor_m`**: none; the rising line is not drawn (§5.11).
- **`form.stern`**: `type: raked`; `knuckle_z_m: 1.33`, the band's side (the face's lower corner stands
  at z 1.61 in `stern_m`); `transom_hb_m: [2.30, 2.33]`, the lines plate's 2.26 and 2.28 m, plank on (the
  body plan's 2.35 and 2.37 m recorded, §5.9); `round_up_m: 0.17`; no `galleries_m`, no `lights_m` (§5.9).
- **`form.head`**: `knee`. **`form.fullness`**: none: the ends are drawn through the sections.
- **`marks`**: `keel_m`, `port_size_m`, `form.stern`, `form.stern.knuckle_z_m`,
  `form.stern.transom_hb_m`, `form.stern.round_up_m`, `form.head`: `stand-in`; **`rail_m`, `breadth_m`,
  `stem_m`, `stern_m`, `section_m`, `decks_m`, `ports_m`, `head_m`, `breadth_line_m`, `sections_m` and
  `rabbet_m`: `judged`** (a line takes the word of its weakest point, principle 4): every height above
  the water by §6.2's two judged steps, the rail's half-breadth the plan's thin outer line (§5.1), the
  round up the class's, the main breadth's height a band and five of the eight triples at the guns'
  places and not the plate's ports. **Old beside new, at the landing:** only `decks_m`, `breadth_line_m`
  and `ports_m` were first `judged`. In the notes:
  `stern_m` tentative between the post and the rudder (§5.3); `rabbet_m` tentative on the post (§5.11);
  `sections_m` ±0.15 ft below WL3 (§5.8).
- **`SAME_HULL_BY_INTENT`**: the pair (`topsail-schooner`, `privateer-schooner`) at the landing, with
  the owner's reason of 2026-10-28 (§5.0 principle 10). Nothing in the hull differs between them: the
  privateer's details are her guns, and those are not the profile's.

### 6.5 Through the tree's own helpers, as built

The lists of §6.4 are the files', through `g.hull_profile` and `g.hull_form` from
`tools/ships/hull_schooner.py`, `freesail` imported from this worktree: no refusal, and `form.check`
passes. The generator's report and `tests/test_hull_schooner.py` hold these; they are in no note of the
files.

| | Drawn | The file | |
|---|---|---|---|
| Displacement | 198 t | 211 t | −6%, within 15% |
| Depth at the greatest section (x +1.5) | 3.10 m | 3.3 m | the drawn section's foot at the nearest station, x +1.96, where `keel_m` stands at 3.14 m (`form.py` scales `section_m`, station 13's, by the keel's depth at x +1.5: 3 cm, under the water, recorded); `keel_m` keeps the drag: 3.90 m at the heel, 2.64 m at the forefoot |
| The water, the post's after edge to the stem's fore edge | 26.74 m | 25.9 m | rabbet to rabbet is 25.90 m |
| The greatest half-breadth, section | 3.65 m | half of 7.3 m | |
| The deck at side at x = 0 | 0.82 m | `deck_height_m` 0.9 | recorded, not moved (0.90 m with *Spider*'s lift, §6.2) |
| Each port triple against the drawn side at its sill | +0.01, −0.01, −0.01, +0.00, +0.00, +0.00, −0.02, +0.01 m | | the plate's three `measured`: a gap over 0.05 m would raise; the five at the guns' places reported, as the cutter's three, and `tests/test_hull_schooner.py` holds all eight within 0.02 m |
| The stations drawn | 51 | | |

## 7. Against the two files (recorded, not moved)

`topsail-schooner.yaml` and `privateer-schooner.yaml` share the hull (`gen_ships.py`
`topsail_schooner()`, at 99a91b8 l. 2542-2618); the guns are the privateer's
(`schooner_armament()`, l. 4139 on).

| Field | The files (their note) | The plates |
|---|---|---|
| `length_waterline_m` | 25.9 (85 ft, judgement between keel and deck) | 26.84 m rabbet to rabbet; 27.71 m post to stem outside (§4) |
| `beam_m` | 7.3 (24 ft extreme) | 24 ft 0 in extreme, read; 22 ft 10 in moulded at the line, 23 ft 2 in plank on (measured) |
| `draught_m` | 3.3 (10.9 ft mean, Marestier's ratios) | 3.28 m mean of the heel's 3.91 m and the forefoot's 2.65 m (§4) |
| `deck_height_m` | 0.9 (*Spider*'s 3 ft 5 in less 10 in, `:2569`, a sum of 0.79 m, not the file's 0.9) | 0.96 m at the middle line amidships; 0.82 m at side (judgement); 0.82 m at side in the files' frame (§6.4) |
| The port sills (the guns' `height_m`, `:4155`) | 1.04 m (3 ft 5 in, *Spider*) at every port | 0.95 m to 1.53 m by port (§5.4); the triples 0.95 to 1.44 m in the files' frame, each gun's `height_m` now its triple's (§6.3) |
| The swivels' and pivot's `rail` (`:4156`) | 1.7 m (deck + 2 ft 8 in, judgement) | rail top 1.87 m at its lowest, 1.92 m at +2.6 m (the pivot), 2.06 m at −10 m and 2.29 m at +10 m (the swivels); 1.92, 2.07 and 2.30 m in the files' frame, the `height_m` of each now the rail's (§6.4) |
| `fore.mast` / `main.mast` `x_m` | +7.8 / −2.6 | +8.26 / −2.60 at the sill line; +7.97 / −2.51 by k_L (§6.2) |
| The masts' `rake_deg` | 11.3 and 11.3 (1 in 5) | 13.5° and 9.9° to the keel's square; 17.2° and 13.6° to the water's (§5.10) |
| The six long 6s' `x_m` (ports 2, 4, 6) | +8.4, 0.0, −8.4 | ports 2, 4, 6 at −7.20, +0.97, +8.80; −6.95, +0.94, +8.49 by k_L; the `x_m` unmoved, the triples at the guns (§6.3) |
| The carronades' `x_m` (forward of the fore mast, abaft the main) | +10.5, −7.5 | port 7 at +11.82, port 2 at −7.20; +11.41, −6.95 by k_L; the `x_m` unmoved, the triples at the guns (§6.3) |
| The bowsprit | `length_m` 3.6, its end at `height_m` 3.0 above the deck: from the drawn stem head, as the viewer stands it, about 20° | 9.2° and 10.5° to the water, its edges (§5.10) |
| `rudder` | 2.0 m², span 3.4 m ("about 11 ft by 2 ft") | the blade 3.9 m deep from the line to the heel, 0.45 to 0.9 m wide (tentative, §5.3) |
| `Build-Ships.md` §5.7, the stern (not a figure of the files) | "raked about 45°", as first written | about 38° from the upright, the 45° the chord from the taffrail to the post's head across the band (§5.9); §5.7 amended so by the lead's ruling, 2026-10-31 |

These are for the lead and the owner. No figure the physics or the gunnery reads moves; the hull's
figures carry the files' sailing pins. The guns' `height_m` move, by `Build-Ships.md` §5.3, and nothing
reads one before the lee port's L2.

## 8. What the source cannot give

- **A written load line or draught**: neither plate labels the line or gives draught figures;
  the line is identified by judgement (§4).
- **A wale**: none drawn; the plain finish is Chapelle's remark (p. 83, read). The class
  specification gives main wales 4 in thick (p. 168, read), Steel's schooner one strake, 1 ft 8 in
  broad and 4 in thick, its lower edge 1 ft above her water (§10.1): another's. `wales_m` is left
  out: the plate is silent and the owner's eye has the replica (`Build-Ships.md` §5.8).
- **The deck at side**: the round up is not drawn (§5.5).
- **The height of the main breadth**: a band on a flat section (§5.7).
- **The post and the rudder apart**: the division is a reading of close lines (§5.3).
- **The sections below about 3 ft above the rabbet** at stations 9 to 16, merged on the body plan into
  one band (§5.8).
- **The rising line**: not drawn (§5.11).
- **The original draught**: these are Chapelle's redrawings (signed '29, tentative); the
  Admiralty's sheet (Portsmouth, 10 May 1816) was not looked for here, and any error of the
  redrawing carries.
- **The spars aloft, the sweeps, port lids and scantlings**: not on the plates (the spars: p. 82,
  read (OCR) l. 4832-4833).
- **The body plan at the plate's scale**: printed at its own size, its stern 0.3 ft wider than the
  lines plate's and its after rail low (§3.4, §5.9).

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
of the first reading; they read no image.

The hull step's scripts are in the session's scratch directory under
`hulls/streams/schooners/`: `lib.py`, `crop.py`, `conv.py`, `rot.py`, `scan108.py` and `brow.py` (the
views, dark runs by columns and rows), `chk108.py` (the checker of §5.2), `overlay108.py` (the first
reading's points drawn back on the plate and looked at), `nodes.py` (the body plan's five curves and
§3.4's registration), `secs.py`, `upper.py`, `upper2.py` and `upper3.py` (the sections, §5.8),
`deck109.py` and `x109.py` (the deck and leaf 109 on leaf 108), `masts.py` (§5.10), `ff.py` and
`ff9.py` (*Flying Fish*), `folio.py` and `foliozoom.py` (Steel's columns); `compute.py`, `checks.py`
and `emit.py` hold the values read and make the figures of §5.5 to §6.4 and §10, reading no image;
`dry.py` is the first dry run; `stations.py` and `frame108.py` hold the first reading's values and
frame; `trace.py`, `bodytrace.py`, `lower.py`, `lower2.py`, `st108.py`, `ffbar.py` and `montage.py` were
working views; `fetch.py` the fetches; `assemble.py` and `patch1.py` to `patch3.py` wrote this note. The
image readers take each cached image's path as an argument and run from outside the cache.

The mending against the second reader (`hulls/streams/schooners/checker2/`, its own scripts over the same
images): `m/verify1.py` (its strongest claims read again), `m/stations.py` (stations 22 and 23 off the
cathead and the hawse bolster), `m/compute2.py` and `m/emit2.py` (`compute.py` and `emit.py` with its
findings), `m/dry2.py` (§6.3 to §6.5 from the tree's own file) and `m/notepatch.py` (each edit here).
The sheets, the hull alone laid over the plates' crops in scratch: `build/states.py`, `build/sheets.py`
and `build/against.py`.

The hull's review (`hulls/streams/schooners/review/`), its own scripts over the same images: `prep.py`,
`frame.py` and `overlay.py` (the file's lines carried back by §6.2's factors and laid on the three plates,
and looked at), `cols3.py`, `upper_mine.py` and `up2.py` (the third reader's sections, §5.8); `cross.py`
(the note's tables against the file), `physdiff.py` (every key of the two files against git) and
`pairs.py` (the pair check as `Build-Ships.md` §5.6 words it), which read no image.

## 10. Her two checks, each recorded beside her (`Build-Ships.md` §5.7)

These move no figure of §6. They say how far *Lynx*'s lines are the type's and how far her own.

### 10.1 Steel's fast sailing schooner of 133 6/94 tons (tables p. 25; Folios)

The tables' title gives "a Post Office packet of 201 64/94 tons, and a fast sailing schooner of 133
6/94 tons" (read; the OCR's "133,53" is garbled). Steel names no builder or vessel. **The scale** is the
tables' own, in feet and inches (read). It checks: FP to the dead flat 38 0, the foremost timber 6 0
and the after timber 5 0 are Folio I's E, F and G; the dead flat's half-breadth 10 1 is half of K's
20 2; the keel and breadth give 133.07 tons by the rule against 133.06 (arithmetic).

**The bodies, schooner** (read on the image, crops at 1:1; ft in; "..." Steel's blank):

| Fore body, timber | ⊕ | C | G | L | N | P |
|---|---|---|---|---|---|---|
| Station from FP | 38 0 | 30 0 | 22 0 | 14 0 | 10 0 | 6 0 |
| Lower height of breadth | 9 5 | 9 3 | 9 3 | 9 5 | 9 6½ | 9 9 |
| Cutting down line | 0 10½ | 1 0 | 1 2½ | 1 5¾ | 1 9¾ | 2 11 |
| Main half-breadth | 10 1 | 9 11 | 9 6 | 8 5½ | 7 4½ | 5 6 |
| 1st diagonal | 2 10½ | 2 10 | 2 6½ | 1 11½ | 1 4½ | 0 6½ |
| 2nd | 5 5¼ | 5 4½ | 4 10 | 3 10¼ | 3 0 | 1 9 |
| 3rd | 8 0½ | 7 11½ | 7 3¼ | 5 11½ | 4 11 | 3 5½ |
| 4th | 9 4 | 9 3 | 8 6½ | 7 0 | 5 9½ | 4 2 |
| 5th | 10 2½ | 10 1½ | 9 6 | 8 0½ | 6 8½ | 4 11½ |
| 6th | 10 7 | 10 5¾ | 9 11½ | 8 8½ | 7 5½ | 5 6½ |

| After body, timber | 1 | 5 | 9 | 13 | 15 | 16 | Tuck |
|---|---|---|---|---|---|---|---|
| Station from AP | 35 0 | 27 0 | 19 0 | 11 0 | 7 0 | 5 0 | ... |
| Lower height of breadth | 9 7 | 10 0 | 10 6½ | 11 3½ | 11 7 | 11 9½ | ... |
| Topside or top-timber line | ... | 10 6 | 11 4½ | 12 7 | 13 4 | 13 8½ | ... |
| Cutting down line | 0 10½ | 1 1 | 1 11 | 2 10 | 4 2 | 5 10 | ... |
| Main half-breadth | 10 1 | 9 10 | 9 1½ | 7 11 | 7 2¼ | 6 8½ | ... |
| Top-timber half-breadth | ... | 9 10 | 9 1 | 7 9½ | 6 11½ | 6 6½ | ... |
| Lower breadth sweep | 10 6 | 6 9 | 4 8½ | 3 1 | 2 2½ | 1 10 | ... |
| 1st diagonal | 2 10 | 2 4¾ | 1 7½ | 0 8¾ | 0 3¼ | ... | ... |
| 2nd | 5 3½ | 4 7 | 3 3 | 1 8½ | 0 10 | 0 3½ | ... |
| 3rd | 7 10 | 6 10 | 5 2½ | 3 4¼ | 2 1 | 1 3½ | ... |
| 4th | 9 2 | 8 2 | 6 4¾ | 4 2½ | 2 9 | 1 11 | 0 8½ |
| 5th | 10 1¼ | 9 3½ | 7 8 | 5 5½ | 3 9 | 2 10 | 1 5 |
| 6th | 10 6¼ | 9 11½ | 8 9½ | 6 10½ | 5 3½ | 4 4 | 2 5½ |

The diagonals, 1st to 6th: up the middle line 2 10¾, 5 5, 7 11, 8 11, 9 10½, 10 10; out on the base
2 7¾, 4 11½, 7 3 (the first three); up the side line 1 2, 4 3½, 7 0 (the last three). The fore body's
top-timber line and half-breadth and its sweeps are Steel's blanks for the schooner (read).

**The folios, schooner** (read, the right leaves; the rows' meanings as
`pages-steel-1805-bodies.md` §4 reads them):

| Row | Figure |
|---|---|
| Length on the range of the deck (I, B); keel for tonnage (I, D) | 77 0; 59 6⅜ |
| Tread of the keel (I, H); length extreme (I, I) | 60 6; 84 9 |
| Breadth moulded; extreme (I, K, L); depth in hold (I, M) | 20 2; 20 6; 7 11½ |
| Load draught afore; abaft (I, O, P) | 7 3; 9 3 |
| **Lower ports above the water in midships (I, Q)** | **3 1** |
| Main keel sided afore, midships, abaft; deep (I, R-V); false keel one, 0 3 (I, D2, E2) | 0 9, 0 10½, 0 9; 1 6 |
| Head of the stem's fore part above the rabbet (II, N); stem moulded, sided (II, O, P) | 10 2; 1 4, 1 1 |
| Main wale's lower edge at the stem, dead flat, after timber (VII, M-O); broad, strakes, thick (VII, P-R) | 8 7, 7 9, 10 9; 1 8, one, 0 4 |
| Deck beams to round up (XXXI, X); plank (XXXII, A) | 0 5; 0 2 |
| Depth of the waist from the plank (XXXII, H) | 0 9 |
| Upper side of the deck beam at the middle line above the rabbet, afore, midships, abaft (XXXII, I-L) | 9 3, 9 0, 15 0 |
| A rise afore AP; deep; its flat thick (XXXII, M, O, P) | 23 6; 1 9; 0 2 |
| Ports deep; fore and aft; apart; number both sides (XXXII, S-X) | 1 9; 1 10; 6 0; 16 |
| The foremost port's fore side abaft FP; the after port's aft side abaft AP (XXXII, Z, A2) | 12 9; 0 4 |
| The lower counter's touch above the rabbet (LI, D); the taffrail's top (LI, H); the stern's breadth at the top-timber line (LI, I); the touch abaft AP (LI, K) | 14 0; 16 9; 8 3; 3 10 |
| Sheer rail's upper edge above the rabbet, afore, midship, abaft (LV, L-N) | 10 3; 9 6½; 15 9 |

**Her load line** is the judgement of `pages-steel-1805-bodies.md` §5.1's method: the draughts from the
main keel's underside, the rabbet either at its upper edge (a King's ship) or half way (a merchant
ship), the folios not saying (arithmetic):

| At the dead flat | Rabbet at the keel's upper edge | Half way |
|---|---|---|
| The load line above the base | 6 ft 9 in | 7 ft 6 in |
| Half-breadth at the water | 9.74 ft | 9.93 ft |
| The wale's lower edge above the water | 1 ft 0 in | 3 in |
| The deck at the middle line above the water | 2 ft 3 in | 1 ft 6 in |
| The sheer rail above the water | 2 ft 9½ in | 2 ft 0½ in |
| Folio I's sill above the deck | 10 in | 1 ft 7 in |
| Waterplane, of the length by the moulded breadth | 0.67 | 0.72 |

The first reading fits the class's 10-in sill above the deck, the second Steel's rule for the wale; the
sill's 3 ft 1 in above the water is printed either way (judgement).

### 10.2 *Flying Fish*, taken off at Portsmouth, September 1806 (Chapelle pp. 48-49)

Built at Baltimore in the last years of the eighteenth century, in the Royal Navy a 10-gun schooner of
three masts (pp. 46, 50, read (OCR)). Her plates are leaves 68 and 69: sheer with the *Shamrock* class's
profile above it, half-breadth, a ruled bar, and her title and dimensions (68); inboard profile,
midsection, body plan, deck plan (69). A note reads that the topsides from the deck up were added to
her original build (read).

**The scale** (measured): the bar 31.05 px to the foot over 80 single feet, rms 0.86 px; the
perpendiculars 2444.8 px apart, 78 ft 9 in against the stated 78 ft 8 in on deck (+0.1%); the plan's
outer line 10.75 ft a side against the stated 10 ft 9½ in extreme (−0.4%); the table's keel, 60 ft 8⅛ in
(read at 2x; the text's 8½, p. 50, read (OCR), is a slip of the one or the other), and its breadth give
150.35 tons by the rule against 150 32/94 (arithmetic). **Leaf 69 against leaf 68** (measured): the
perpendiculars 2517 px apart, ×1.030; its body plan's dashed lines 663.9 px apart, 31.15 px/ft for the
21 ft 3¾ in moulded.

**Beside *Lynx*:**

| | *Lynx* | *Flying Fish* | Steel's schooner | *Spider*, 1835 |
|---|---|---|---|---|
| On deck; keel for tonnage | 94 7; 73 1¼ | 78 8; 60 8⅛ | 77 0; 59 6⅜ | 80 0; 64 5½ |
| Breadth extreme; moulded | 24 0; 23 8 | 21 7; 21 3¾ | 20 6; 20 2 | 23 2; 23 0 for tonnage |
| Depth in hold; burthen | 10 3; 223 91/94 | 7 10; 150 32/94 | 7 11½; 133 6/94 | 9 10; 182 89/94 |
| On deck by the extreme breadth | 3.94 | 3.64 | 3.76 | 3.45 |
| Keel for tonnage, of the length on deck | 0.77 | 0.77 | 0.77 | 0.81 |
| Draught aft; forward (ft in) | 12 10; 8 8 | about 9 2; 7 0 (to her top waterline, tentative) | 9 3; 7 3 | 11 8; 9 2 |
| The keel's lower edge to the water, drawn | 3.22° | 2.01° | not drawn | not drawn |
| The draughts' difference over the length on deck | 2.49° | 1.58° | 1.49° (arithmetic) | 1.79° (arithmetic) |
| **Sills above the water: midships; aft; forward** | **3 1**; 3 11; 5 0 | **2 10**; 3 0; 4 3 (her top waterline) | **3 1**; not given | **3 5**; 3 7; 4 7 |
| Ports a side; fore and aft | seven; 2 1 | six, arched, with sweep ports between; 2 2 | eight; 1 10 | six guns; 2 6 (class) |
| The rail's top above the water: lowest; aft; forward | 6 1½; 8 0; 8 10 | 5 3½; about 7 1; 7 4 | not given | |
| Rail to sill | about 3 0 | about 2 6 | | |
| The deck's round up | not drawn | about 11 in (the midsection, 0.9 ft) | 5 in | 5½ in (class) |
| Deadrise near the keel | about 28° | about 25° (the midsection) | 18° to 20° at the dead flat (arithmetic) | |
| The greatest breadth, before the middle | about 7 ft | about 6 ft | ½ ft | |
| Waterplane, of the length by the greatest half-breadth | 0.71 | 0.72 | 0.67 to 0.72 | |
| The rudder's after edge to the water's square | 25.8° | 34.9° | | |
| The stem's forward reach by the depth at the forefoot | 1.23 | 1.25 | | |
| The transom | raked about 38° to the water's square, flat, 7 5 a side moulded, 0.63 of the half-breadth | square, raked about 28° (25.5° to the page, 2.29° of water), the post outside it at its head (p. 52, read (OCR)), about 5 9 a side, 0.54 | 8 3 across at the top-timber line, 0.41, on a tuck | |
| The wale | none drawn | two bands drawn, about 0.3 and 1.8 ft above her top waterline amidships, neither named (read) | one strake, 1 8 broad | 4 in thick (class) |
| The head | a small knee | none: the stem runs up to the bowsprit (read; Chapelle's privateers without a head had "bows like the Flying Fish", read (OCR) l. 3345) | not given: the stem's head 10 2 above the rabbet | |
| Masts | two, raking 9.9° and 13.5° to the keel | three, about 11°, 7.4° and 6.6° to the keel | | |

Measured off the plates at ±0.1 ft where a single line is followed; *Flying Fish*'s draughts and stern
±0.2 ft. *Flying Fish*'s top waterline is carried a little past both ends (read) and is taken as her load
line (judgement), the *Shamrock* profile above it drawing the same line long: Chapelle calls her freeboard
very low and her bulwarks high (p. 52, read (OCR)).

### 10.3 What they say of her (judgement)

- **The sill.** Three vessels of 77 to 95 ft stand at 2 ft 10 in to 3 ft 1 in amidships, whatever
  their length; *Spider*, twenty-three years on and not extreme, at 3 ft 5 in. The plate's sills are the
  type's. *Spider*'s lift, the design's first letter, stood at the edge of what they allow; the lead's
  ruling takes the plate's own (§6.2).
- **The ends and the length.** The three carry the same keel on the same deck, 0.77, the same waterplane
  and much the same reach of stem: *Lynx*'s length and fineness are the type's.
- **What is her own.** The sharpest floor, the greatest drag and the widest stern of the three, a raked
  flat transom where *Flying Fish*'s stands square and Steel's narrows to a tuck, and a small knee where
  *Flying Fish* has none. The stern view is where a
  file standing for the type is most *Lynx*, and it is marked `stand-in` for that reason.
- **Nothing moves by them.** §6's figures are *Lynx*'s, as `Build-Ships.md` §5.7 has it.
