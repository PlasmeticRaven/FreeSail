# Pages: Steel 1805, the bodies of the 36-gun frigate, the cutter and the coasting sloop (October 2026)

Stage 0 research for package 75, the pages named by `Build-Ships.md` §19.1 item 11 and by the
shared draft (`ships-design/shared-design.md` §1.5, the frigate's, the cutter's and the smack's
rows; §5 item 13). It serves `data/ships/frigate-36.yaml`, `cutter.yaml` and `smack.yaml`, and the
builder B8, who draws a sourced hull profile for each file (`Build-Ships.md` §5). The source is
David Steel, *The Elements and Practice of Naval Architecture* (1805 text), the Internet Archive
item `elementspractice00stee` (catalogued 1822), whose text layer the repository holds as
`docs/references/steel/steel-1805-naval-architecture-1822-printing-ocr.txt`. The OCR is garbled
on every table, so every figure below was read on the page image. Facts only: the images stay
outside the repository (§8).

The marks:

- **read**: the figure was seen on the page image, on a crop at full resolution. "read (OCR)"
  is the text layer only.
- **arithmetic**: computed from read figures by a scratch script (§8); the method is stated.
- **judgement**: reasoning by this note, above all where Steel leaves a point open.
- **probable misprint**: read as printed, with the reason it looks wrong.

**Units and datums.** English feet and inches as Steel prints them, with metres where the
profile wants them (1 ft = 0.3048 m). Steel's heights are all above **the base**, the upper edge
of the rabbet of the keel (the tables' "base line or upper edge of rabbet"; the text, OCR
`:15581`, `:16130-16137`). Stations are Steel's: fore-body timbers from the foremost
perpendicular (**FP**), after-body timbers from the after perpendicular (**AP**); the
perpendiculars are the rabbets of the stem and post at the gun deck, the length between them the
length on the gun deck (Folio I, row A). The profile's **x** is forward of the
mid-perpendiculars, positive forward; its **z** is above the load line of §5.1, positive up.

## 0. In brief

- **The three tables are found and read.** IA leaves n467 (tables p. 9, the frigate of 36 guns
  and 877 tons), n476 (p. 18, the cutter) and n485 (p. 27, the coasting sloop of 60 tons), with
  the dimension folios the profile also needs: Folio I (lengths, breadth, draught, the lower
  ports above the water, the keel), II (the stem), VII and VIII (the wales, the sheer strakes),
  XIX, XXXI and XXXII (the decks, the ports), XLII, XLIII and XLVI (the quarterdeck and
  forecastle), LI (the stern, the taffrail) and LV (the sheer rail). §2 lists the leaves.
- **The cutter is of 273 tons, not 278.** The design's "278" is the OCR's: a foxing spot sits on
  the 3 of the table's title (read, crop at 3x). Folio I's burthen row for the cutter reads 273
  (read). The design's four mentions (`Build-Ships.md:593`, `:1273`;
  `ships-design/shared-design.md:202`, `:988`) should read 273.
- **The 36 checks.** The table's stations meet Folio I's dead flat, foremost and after timbers to
  the inch and its timber room sums to the 137 ft gun deck within an inch; the wale (lower edge
  16 ft 6 in, broad 3 ft 9 in) plus the sheer strakes' 6 ft 9 in comes to the top-timber line's
  27 ft 0 in at dead flat exactly; Folio LV's sheer rail, 29 ft 0 in / 27 ft 0 in / 31 ft 0 in,
  is the top-timber line extended to the perpendiculars within 1¼ in (§6).
- **The 36's sill.** Folio I: 7 ft 8 in above the water in midships, 2.34 m (read, as already
  read on n487). The deck folios give 7 ft 5½ in, 2.28 m: 2½ in lower, the folios' own spread
  (§5.2). The wale's lower edge stands 2½ in above the load line at dead flat, Steel's "a few
  inches higher" (text, OCR `:15190-15193`).
- **The cutter checks, except her sheer.** Stations, moulded breadth and the sill (derived 4 ft
  5½ in above the water against Folio I's 4 ft 6 in) agree. The folios set her sheer rail 4½ in
  above the table's top-timber line at midships, 8 in above it at FP and 1 ft 3 in at AP, and
  her dead flat 4 in further aft (§6).
- **The coasting sloop floats deep.** At Folio I's draught (7 ft 0 in / 9 ft 0 in) her load line
  lies above the upper height of breadth at midships and her wale is under water there
  (judgement on the rabbet, §5.1); her side rises 3 ft 5½ in above the water at dead flat, the
  deck 3 ft 0½ in, and Folio XXXII's 5-in waist is the top-timber line less the deck at side to
  the inch. Her length between perpendiculars is not printed (§7).
- **The profile points** (rail, half-breadths at the water, the rail and the sill, the decks at
  side, the sills, the wale, the stem, the stern, the keel, the midship section) are in §5 in
  metres. The half-breadth at the water is arithmetic on Steel's breadth sweeps and diagonals,
  never printed.
- **Three probable misprints:** the 36's timber 29, lower height of breadth 22 ft 9 in above the
  upper's 22 ft 6 in (§3.1); the sloop's timber 4, third diagonal 7 ft 4¼ in between 8 ft 9 in
  and 7 ft 9 in (§3.3); the 36's forecastle flat, 9 in thick where the 44, 38 and 32 have 3 in
  (§4).

## 1. The source

| | |
|---|---|
| Work | David Steel, *The Elements and Practice of Naval Architecture; or, a Treatise on Ship-building* (London: printed for W. Simpkin and R. Marshall; the IA copy is catalogued 1822; the text is of 1805) |
| Item | Internet Archive `elementspractice00stee`, https://archive.org/details/elementspractice00stee ; 738 images at 500 ppi; scanned at Boston, 2023 |
| Rights shown at the source | metadata `rights`: http://rightsstatements.org/vocab/NoC-US/1.0/ (No Copyright, United States); `possible-copyright-status`: "No known copyright restrictions as determined by the Peabody Essex Museum"; contributor and sponsor: Phillips Library at the Peabody Essex Museum (read, `elementspractice00stee_metadata.json`) |
| Held text | `docs/references/steel/steel-1805-naval-architecture-1822-printing-ocr.txt` (the same item's text layer) |
| Cache | `D:/Projects/FreeSail/reference-cache/steel-1805-bodies/` (§8) |

**Leaf numbering.** "IA leaf n*N*" is the book reader's page `n`*N* (as the earlier notes use it).
The image files in the item's JP2 archive are numbered by scan leaf, one more: n467 is
`elementspractice00stee_0468.jp2`. The scan's leaf 0 is a colour card, outside the reader
(`elementspractice00stee_scandata.xml`, read). Folio I, downloaded here as `_0488.jp2`, is the
image the owner's notes hold as `steel1805-naval-architecture-folio-I-load-draught-IAleaf487.jpg`
(arithmetic: mean grey difference 0.19 of 255 at 300 x 400 px). **Pitfall:** the IIIF short
form `.../iiif/3/elementspractice00stee$467/...` resolves to file `_0467`, which is n466.

## 2. The leaves

Every image 2954 x 3946 px, upright as served. Each folio is a spread: the left leaf has the row
labels and the King's ships from 110 guns to the 32, the right leaf ("Scantlings of ships of
each class") the 28 and smaller, the cutter, the merchant ships and the sloop of 60 tons, joined
by the row letters at the spread's edge.

| IA leaf | File | Page | What it gives here | OCR |
|---|---|---|---|---|
| n467 | `_0468` | Tables p. 9 | Bodies of the frigate of 36 guns and 877 tons | `:27068-27170` |
| n476 | `_0477` | Tables p. 18 | Bodies of a cutter, on a new construction, of 273 tons | `:27779-27841` |
| n485 | `_0486` | Tables p. 27 | Bodies of a coasting sloop of 60 tons | `:28504-28580` |
| n487, n488 | `_0488`, `_0489` | Folio I | Lengths, breadths, depth, burthen, load draught, the lower ports above the water, the main and false keels, the rabbet | `:28691-28800` |
| n489, n490 | `_0490`, `_0491` | Folio II | The stem's centre, its head's height, its moulding | `:29125-29140` |
| n499, n500 | `_0500`, `_0501` | Folio VII | The main wale's lower edge at the stem, dead flat and after timber; its breadth | `:30350-30360` |
| n501, n502 | `_0502`, `_0503` | Folio VIII | The sheer strakes: from the wale to the top-timber line | `:30557-30565` |
| n523, n524 | `_0524`, `_0525` | Folio XIX | The gun or lower deck at the middle line; the height to the deck above; round up | `:33203-33226` |
| n547, n548 | `_0548`, `_0549` | Folio XXXI | The upper deck's round up | (lost) |
| n549, n550 | `_0550`, `_0551` | Folio XXXII | The upper deck: plank, the heights to the quarterdeck and forecastle, the waist, the deck above the rabbet (single-decked vessels), the sills, the ports | `:36445-36489` |
| n569, n570 | `_0570`, `_0571` | Folio XLII | The quarterdeck's ports and sills, its length | `:39312-39351` |
| n571 | `_0572` | Folio XLIII | The quarterdeck's flat, the roughtree rail (left leaf only) | `:39492-39546` |
| n577 | `_0578` | Folio XLVI | The forecastle: round up, flat, ports, sills, length (left leaf only) | `:40025-40040` |
| n587, n588 | `_0588`, `_0589` | Folio LI | The stern: the counters, the taffrail, their positions abaft AP | `:41410-41444` |
| n595, n596 | `_0596`, `_0597` | Folio LV | The sheer rail above the rabbet, afore, midship and abaft; the waist and drift rails | `:42558-42576` |

The cutter's column is headed "Cutter, guns 16" on every folio read except Folio II, which heads
it "guns 18" (read).

## 3. The bodies tables as read

Every figure read on the page image (crops at full resolution, doubtful cells at 1.5-3x). Feet
and inches. "..." is Steel's own blank. The rising line, the rising half-breadth and the cutting
down line were read but are not transcribed; the profile does not use them.

### 3.1 The frigate of 36 guns and 877 tons (n467)

**Fore body**, stations abaft FP:

| Timber | ⊕ | C | G | L | P | T | W | X |
|---|---|---|---|---|---|---|---|---|
| Station from FP | 61 7 | 49 7 | 39 11 | 30 3 | 20 7 | 10 11½ | 6 1½ | 3 8½ |
| Lower height of breadth | 17 3 | 17 4¼ | 17 9¼ | 18 6½ | 19 11 | 22 1½ | 23 8 | 24 7 |
| Upper height of breadth | 18 11 | 18 11½ | 19 1 | 19 6½ | 20 7½ | 22 6 | 23 11¼ | 24 9½ |
| Top-timber line | 27 0 | 27 0 | 27 0½ | 27 3½ | 27 7 | 28 0½ | 28 4½ | 28 7½ |
| Topside line | ... | ... | ... | 29 1¼ | 29 5½ | 29 10½ | 30 3 | 30 6 |
| Main half-breadth | 18 10 | 18 10 | 18 10 | 18 5½ | 17 1½ | 13 9 | 10 7½ | 8 3 |
| Top-timber half-breadth | 16 9 | 16 9 | 16 9 | 16 6 | 15 9½ | 13 7 | 11 1 | 9 1 |
| Topside half-breadth | ... | ... | ... | 16 2½ | 15 8 | 13 9½ | 11 7½ | 9 10 |
| Lower breadth sweep | 14 2 | 13 8 | 13 1 | 12 8 | 12 9 | 13 5 | 14 0 | 14 0 |
| Upper breadth sweep | 11 3 | 11 3 | 11 3 | 11 3 | 11 3 | 11 3 | 11 3 | 11 3 |
| 1st diagonal | 9 4 | 9 3 | 8 10 | 7 11¼ | 6 6½ | 4 2 | 2 1 | 0 8 |
| 2d diagonal | 13 11½ | 13 9 | 13 1 | 11 10½ | 9 10½ | 6 9½ | 4 4½ | 2 8½ |
| 3d diagonal | 17 0 | 16 10 | 16 2¼ | 14 11½ | 12 10¾ | 9 4½ | 6 6½ | 4 7 |
| 4th diagonal | 19 4 | 19 1½ | 18 8 | 17 7½ | 15 7½ | 11 9½ | 8 8 | 6 5½ |
| 5th diagonal | 20 10½ | 20 9 | 20 5 | 19 6 | 17 7½ | 13 8½ | 10 4 | 7 11 |

**After body**, stations afore AP:

| Timber | 7 | 11 | 15 | 19 | 23 | 25 | 27 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| Station from AP | 58 5 | 48 9 | 39 1 | 29 5 | 19 9 | 14 11 | 10 1 | 5 3 | 2 10 |
| Lower height of breadth | 17 5½ | 17 9½ | 18 5 | 19 3 | 20 4 | 20 11½ | 21 8½ | 22 9 | 22 11 |
| Upper height of breadth | 18 10½ | 19 1 | 19 5½ | 20 1½ | 20 11 | 21 6 | 22 1 | 22 6 | 23 1½ |
| Top-timber line | 27 4 | 27 8 | 28 1 | 28 8 | 29 4 | 29 8½ | 30 2 | 30 6¾ | 30 9¾ |
| Topside line | 29 1½ | 30 0½ | 30 6 | 31 1 | 31 9½ | 32 1¾ | 32 7 | 33 0 | 33 4 |
| Main half-breadth | 18 9 | 18 6½ | 18 1½ | 17 5 | 16 5 | 15 9 | 15 0 | 14 0 | 13 7 |
| Top-timber half-breadth | 16 8½ | 16 6½ | 16 1 | 15 5 | 14 6 | 13 11 | 13 3½ | 12 7 | 12 2½ |
| Topside half-breadth | ... | 16 3 | 15 8½ | 15 0 | 14 1 | 13 6¾ | 12 11 | 12 2½ | 11 10½ |
| Lower breadth sweep | 12 7 | 12 0 | 10 6 | 9 1½ | 7 7 | 6 9 | 5 9½ | 4 6 | 3 9 |
| Upper breadth sweep | 11 3 | 11 3 | 11 3 | 11 3 | 11 3 | 11 3 | 11 3 | 11 3 | 11 3 |
| 1st diagonal | 8 10 | 8 3 | 7 1 | 5 6½ | 3 9 | 2 10 | 1 11½ | 1 1½ | 0 8 |
| 2d diagonal | 13 4 | 12 5 | 10 10 | 8 9½ | 6 4 | 5 0 | 3 6½ | 2 0 | 1 2 |
| 3d diagonal | 16 4¼ | 15 5½ | 13 10½ | 11 10½ | 9 2 | 7 7½ | 5 9½ | 3 8 | 2 3 |
| 4th diagonal | 18 10¾ | 18 8 | 16 8 | 14 9½ | 12 3 | 10 8 | 8 9½ | 6 3½ | 4 6 |
| 5th diagonal | 20 8 | 19 11 | 18 9 | 17 2½ | 14 11 | 13 5½ | 11 8 | 9 2½ | 7 4½ |
| 6th diagonal | ... | ... | ... | ... | 19 2 | 18 0 | 16 7¼ | 14 9½ | 13 5½ |

**The diagonals** (the body plan's lines; the side line stands at dead flat's main half-breadth,
18 ft 10 in): height up the middle line 8 0, 12 0, 15 8, 19 2½, 22 2, 28 0 for the 1st to the
6th; the 1st to 3d end on the base at 7 4, 13 2 and 18 1 from the middle line; the 4th to 6th
end on the side line at 3 8½, 7 10½ and 11 8 up (read).

**Probable misprint:** timber 29's lower height of breadth, 22 ft 9 in, stands above its upper,
22 ft 6 in (read twice, the second at 1.5x). Transposed, the two lines run smoothly (lower
21 8½, 22 6, 22 11; upper 22 1, 22 9, 23 1½) (judgement). The arithmetic of §5 uses the cells as
printed; timber 29's load line falls well below both.

### 3.2 The cutter, on a new construction, of 273 tons (n476)

Steel prints one row for both heights of breadth, one line for the top of the side (the
top-timber and topside lines in one) and one half-breadth there (read).

| Timber | ⊕ | D | F | H | K | M | N |
|---|---|---|---|---|---|---|---|
| Station from FP | 32 11 | 24 3 | 19 11 | 15 7 | 11 3 | 6 11 | 4 9 |
| Height of breadth | 11 4½ | 11 6¾ | 11 9 | 12 1 | 12 6½ | 13 2½ | 13 7 |
| Top-timber line | 16 1½ | 16 5½ | 16 8½ | 17 0½ | 17 5¼ | 17 10½ | 18 1½ |
| Main half-breadth | 14 7½ | 14 3 | 13 7½ | 12 7 | 10 10½ | 8 2 | 6 4 |
| Top-timber half-breadth | 14 3½ | 13 11 | 13 4¾ | 12 5¾ | 10 11 | 8 5 | 6 9 |
| Lower breadth sweep | 6 7 | 5 7¾ | 4 11½ | 4 1½ | 3 8½ | 3 4 | 3 0 |
| 1st diagonal | 6 8½ | 6 5¼ | 6 0 | 5 5¾ | 4 4½ | 2 11½ | 1 11¾ |
| 2d diagonal | 8 11 | 8 6 | 7 9½ | 6 11½ | 5 8½ | 4 1½ | 3 1½ |
| 3d diagonal | 11 4 | 10 9 | 9 10½ | 8 10½ | 7 5½ | 5 8 | 4 5½ |
| 4th diagonal | 13 5 | 12 8½ | 11 9 | 10 6¾ | 9 1¼ | 6 11½ | 5 6¾ |
| 5th diagonal | 15 2½ | 14 6 | 13 8 | 12 4½ | 10 10 | 8 4½ | 6 8½ |

| Timber | 4 | 8 | 10 | 12 | 14 | 16 | 18 | Tuck |
|---|---|---|---|---|---|---|---|---|
| Station from AP | 36 5 | 27 9 | 23 5 | 19 1 | 14 9 | 10 5 | 6 1 | |
| Height of breadth | 11 4¾ | 11 7¾ | 11 10 | 12 1 | 12 5¼ | 12 10½ | 13 6 | |
| Top-timber line | 16 0½ | 16 2½ | 16 4¾ | 16 7½ | 16 11 | 17 3¾ | 17 8¾ | |
| Main half-breadth | 14 6 | 13 11 | 13 5 | 12 9 | 11 11½ | 11 0 | 9 10 | 7 8 |
| Top-timber half-breadth | 14 2 | 13 7 | 13 1 | 12 5 | 11 7½ | 10 8 | 9 6 | |
| Lower breadth sweep | 6 7½ | 6 0¾ | 4 11½ | 3 6 | 2 7¼ | 2 0½ | 1 10½ | |
| 1st diagonal | 6 8 | 6 4¼ | 5 11½ | 5 5½ | 4 6¾ | 3 4 | 1 5½ | |
| 2d diagonal | 8 10 | 8 4¼ | 7 9½ | 6 11½ | 5 10¼ | 4 4½ | 2 5¾ | 0 9¾ |
| 3d diagonal | 11 2½ | 10 7 | 9 10½ | 8 10½ | 7 6½ | 5 10¾ | 3 11 | 2 4½ |
| 4th diagonal | 13 3½ | 12 6½ | 11 9 | 10 7½ | 9 1½ | 7 5¼ | 5 6 | 4 1½ |
| 5th diagonal | 15 0½ | 14 4¾ | 13 6½ | 12 5¼ | 11 0 | 9 4½ | 7 6½ | 6 4½ |

**The diagonals:** up the middle line 7 4, 9 7, 11 10, 13 6½, 15 3; the 1st to 3d end on the
base at 3 6¼, 7 0½ and 10 10½; the 4th and 5th on the side line (14 ft 7½ in out) at 1 1 and
4 11 up (read).

### 3.3 The coasting sloop of 60 tons (n485)

No breadth sweeps are printed; the diagonals are "length down" them (read).

| Timber | ⊕ | A | C | E | F | G |
|---|---|---|---|---|---|---|
| Station abaft FP | 19 5 | 15 8½ | 11 5½ | 7 3½ | 5 2 | 3 0¾ |
| Lower height of breadth | 5 10 | 6 1½ | 6 7 | 7 4 | 7 11¾ | 8 9 |
| Upper height of breadth | 7 2 | 7 4½ | 7 8 | 8 3 | 8 7 | 9 1 |
| Top-timber line | 10 10 | 10 11½ | 11 2½ | 11 6 | 11 9 | 12 0½ |
| Lower edge of the stem's rabbet | ... | ... | ... | 0 2½ | 1 2 | 3 4 |
| Main half-breadth | 8 3 | 8 2½ | 7 11½ | 7 3 | 6 5 | 4 9 |
| Top-timber half-breadth | 7 8 | 7 8 | 7 5 | 6 10 | 6 2 | 4 8 |
| 1st diagonal | 5 11 | 5 9½ | 5 2¾ | 4 2¾ | 3 1½ | 1 1 |
| 2d diagonal | 7 5 | 7 3½ | 6 8½ | 5 7 | 4 4 | 2 3 |
| 3d diagonal | 9 0 | 8 11 | 8 4 | 7 2¼ | 6 0 | 3 8 |
| 4th diagonal | 9 10 | 9 9 | 9 3 | 8 2¾ | 7 1 | 4 10 |
| 5th diagonal | 11 0 | 10 11½ | 10 6 | 9 6 | 8 5 | 6 2½ |

| Timber | 2 | 4 | 6 | 8 | 10 | 12 | 13 |
|---|---|---|---|---|---|---|---|
| Station from AP | 26 8 | 22 4 | 18 2½ | 13 11 | 9 10 | 5 7½ | 3 6 |
| Lower height of breadth | 5 10½ | 6 0½ | 6 4 | 6 10½ | 7 8 | 8 8½ | 9 4½ |
| Upper height of breadth | 7 2½ | 7 4 | 7 7 | 8 0 | 8 6 | 9 3 | 9 8¼ |
| Top-timber line | 10 10 | 10 11½ | 11 2 | 11 5 | 11 9 | 12 3 | 12 7 |
| Topside line | ... | ... | 11 6 | 11 9 | 12 1 | 12 7 | 12 11 |
| Main half-breadth | 8 1 | 7 11½ | 7 9¼ | 7 5 | 7 0 | 6 6 | 6 2 |
| Top-timber half-breadth | 7 8 | 7 6 | 7 4 | 7 0¼ | 6 8 | 6 2 | 5 9½ |
| Topside half-breadth | ... | ... | 7 3¼ | 6 11½ | 6 7½ | 6 1 | |
| 1st diagonal | 5 8 | 5 3 | 4 7 | 3 9 | 2 8 | 1 3¼ | |
| 2d diagonal | 7 2 | 6 9 | 6 0 | 5 0 | 3 9 | 2 2 | 0 9 |
| 3d diagonal | 8 9 | 7 4¼ | 7 9 | 6 8 | 5 5 | 3 7 | 1 10 |
| 4th diagonal | 9 7 | 9 4 | 8 11 | 8 1 | 7 2 | 5 5 | 3 8 |
| 5th diagonal | 10 10 | 10 8¾ | 10 4 | 9 9 | 9 0½ | 7 10 | 6 11 |

**The diagonals:** up the middle line 4 6, 5 10½, 7 7, 9 4, 12 3; the 1st and 2d end on the base
at 4 11½ and 6 4½; the 3d to 5th on the side line (8 ft 3 in out) at 0 10½, 3 2½ and 4 9 up
(read).

**Probable misprint:** timber 4's third diagonal, 7 ft 4¼ in, between timber 2's 8 ft 9 in and
timber 6's 7 ft 9 in (read at 2x); 8 ft 4¼ in would run fair (judgement). It does not reach the
load line's arithmetic.

The topside line abaft timber 6 is the raised quarter: Folio XXXII gives the sloop a rise of
8 in (0 ft 8 in deep, its flat 2 in thick) running 20 ft 3 in afore AP (read).

## 4. The dimension folios: what the profile needs

All read on the images; heights above the base unless the row says otherwise. "..." is Steel's
blank, "not read" a row this research did not reach. A folio's row letters run A to Z and then
again from A; "C2" is the second C.

| Row (folio, letter) | Frigate, 36 | Cutter, 273 tons | Sloop, 60 tons |
|---|---|---|---|
| Length on the gun deck, rabbet to rabbet (I, A) | 137 0 | ... | ... |
| Length on the range of the deck (I, B) | ... | 78 0 | ... |
| Stem at the hawse holes (merchant ships: at the wing transom) to the post's aft side at the wing transom (I, C) | 140 8 | 80 6 | 52 0 |
| Keel for the tonnage (I, D) | 113 3 | 58 6 | 40 6 |
| FP to the centre of dead flat (I, E) | 61 7 | **32 7** | 19 5 |
| FP to the foremost timber of the bodies (I, F) | 3 8½ | 4 9 | 3 0¾ |
| AP to the after timber of the bodies (I, G) | 2 10 | 6 1 | 3 6 |
| Tread of the keel, post's aft side to the forefoot (I, H) | 126 2 | 63 0 | 44 6 |
| Length extreme, taffrail to the figure (I, I) | 161 9 | 88 0 | 56 1 |
| Breadth moulded; extreme (I, K, L) | 37 6; 38 2 | 29 3; 29 8 | 16 4; 16 8 |
| Depth in hold (I, M) | 13 4 | 11 1 | 9 8 |
| Burthen, tons (I, N) | 877 | 273 | 60 |
| Load draught afore; abaft (I, O, P) | 17 4; 18 4 | 10 10; 10 10 | 7 0; 9 0 |
| Lower ports above the water in midships (I, Q) | **7 8** | **4 6** | ... |
| Main keel sided afore, midships, abaft; deep (I, R-V) | 1 2, 1 4, 1 1; 1 6 | 0 8, 1 1, 0 7½; 1 1 | 0 7, 0 10, 0 7; 0 10 |
| Rabbet sunk in, not more than (I, C2) | 0 3½ | 0 2½ | 0 1½ |
| False keels; upper false keel deep (I, D2, E2) | one; 0 5 | none | (blank) |
| Note under the keel rows (I) | in merchant ships the rabbet mostly at the middle of the keel's depth (paraphrased) | | |
| Stem's centre for sweeping its aft side: above the rabbet; abaft FP (II, L, M) | 18 6; 18 1 | ... | ... |
| Head of the stem's fore part above the rabbet (II, N) | **29 0** | **19 6** | **13 3** |
| Stem moulded; sided at the head (II, O, P) | 1 3½; 1 8 | 1 7; 1 1 | 1 0; 0 10 |
| Main wale's lower edge at the stem; at dead flat; at the after timber (VII, M-O) | 19 0; 16 6; 20 3 | 12 10; 10 3; 11 10 | 7 3; 5 11; 7 8 |
| Main wale broad; strakes; thick (VII, P-R) | 3 9; four; 0 6 | 2 0; two; 0 4 | 1 4; two; 0 4 |
| Sheer strakes: wale's upper edge to the top-timber line; broad; strakes (VIII, A-C) | 6 9; 1 11; two | 4 4; 0 10; one | ... |
| Gun or lower deck plank at the middle line, afore; midships; abaft (XIX, K-M) | 16 8; 15 9; 17 11 | 8 6; 7 0; 7 7 | ... |
| Its plank; to the underside of the plank above, afore, midships, abaft; round up (XIX, N-R) | 0 3; 6 2, 6 2, 6 2; 0 4½ | 0 2; 5 7, 5 7, 6 0; 0 2½ | ... |
| Upper deck beams to round up (XXXI, X) | 0 7 | 0 6½ | 0 6 |
| Upper deck plank (XXXII, A) | 0 3 | 0 3 | 0 2 |
| Upper deck plank to the quarterdeck beam's upper side in midships, afore; abaft (XXXII, B, C) | 6 5; 6 7 | ... | ... |
| The same to the forecastle beam, afore; abaft (XXXII, F, G) | 6 2; 6 2 | ... | ... |
| Depth of the waist from the plank at the lowest place (XXXII, H) | 6 9 | 4 1 | 0 5 |
| Upper side of the upper deck beam at the middle line above the rabbet, afore; midships; abaft (XXXII, I-L) | ... | 14 5; 12 9; 14 3 | 11 6; 10 9; 13 1 |
| Rise afore AP; deep; its flat thick (XXXII, M, O, P) | ... | ... | 20 3; 0 8; 0 2 |
| Plank to the port sills (XXXII, Q) | 2 2 | 1 9 | ... |
| Ports deep; fore and aft; apart; number, both sides (XXXII, S-X) | 2 5; 2 10; 7 2; 26 | 1 10; 2 0; 6 7; 16 | ... |
| Foremost port's fore side abaft FP; after port's aft side afore AP (XXXII, Z, A2) | 10 4; 4 6 | 9 0; 6 10 | ... |
| Sills deep, lower; upper (XXXII, B2, C2) | 0 6; 0 5 | 0 4; 0 3 | ... |
| Quarterdeck: plank to the sills of the gun ports; of the carronade ports (XLII, A, B) | 1 7; 0 11 | ... | ... |
| Quarterdeck gun ports a side; fore and aft; deep (XLII, C-E) | five; 2 5; 2 4 | ... | ... |
| Quarterdeck carronade ports a side; fore and aft; deep (XLII, F-H) | three; 3 4; 2 7 | ... | ... |
| Quarterdeck sills deep (XLII, I) | 0 5 | ... | ... |
| Quarterdeck: aft side of the midship stern timber to the fore side of its foremost beam (XLII, K) | 65 6 | ... | ... |
| Quarterdeck beams' round up (XLII) | "agreeably to the lights below" (no figure) | ... | ... |
| Quarterdeck flat, thick (XLIII, Y) | 0 3 | not read | not read |
| Roughtree rail broad; deep; underside above the deck (XLIII, C2-E2) | 0 8; 0 5; 3 7 | not read | not read |
| Forecastle beams' round up; flat thick (XLVI, B, C) | 0 6½; **0 9** (the 44, 38 and 32: 0 3; probable misprint) | not read | not read |
| Forecastle: flat to the gun port sills; to the carronade port sills (XLVI, D) | ...; 0 11 | not read | not read |
| Forecastle carronade ports a side, fore and aft; gun ports a side, fore and aft (XLVI, E, F and the next two rows) | two, 3 4; two, 2 7 | not read | not read |
| Length on the forecastle (XLVI, G) | 36 0 | not read | not read |
| Stern, above the rabbet: the lower counter's touch at the middle line; the upper counter's (LI, D, E) | 25 9; 28 0 | 17 0; 20 3 | 11 1; ... |
| Upper part of the taffrail (LI, H) | **36 4** | **20 3** | **14 6** |
| Breadth of the stern at the top-timber line (LI, I) | 20 9 | 10 9 | 10 0 |
| Abaft AP: the lower counter's touch; the upper counter's; the counter timber at the taffrail's height (LI, K-M) | 6 0; 7 6; 10 3 | 6 0; 7 6; ... | 0 6; ...; 1 11 |
| Depth of the taffrail (LI, G2) | 2 4 | not read | not read |
| Sheer rail's upper edge, following the top-timber line, above the rabbet: afore; midship; abaft (LV, L-N) | 29 0; 27 0; 31 0 | 19 4; 16 6; 19 7 | 12 4; 10 10; 13 5 |
| Waist rail's upper edge below the sheer rail's (LV, O) | 1 10 | 1 4 | 0 10 |
| Drift rail above the sheer rail, forward; aft; main drift above it (LV, Q-S) | 1 4; 1 1; 1 2 | ... | ... |

## 5. The profile points (arithmetic and judgement)

### 5.1 The load line

- **The datum.** Steel sets the load water line up "from the underside of the keel" (text, OCR
  `:15187-15188`). Folio I's draughts are taken from the underside of the **main** keel at the
  perpendiculars, the line straight between them (judgement). The base lies a main keel's depth
  above that in King's ships, where the rabbet is at the keel's upper edge, and about half the
  depth in merchant ships, by Folio I's note (judgement; the sloop's 10-in keel gives 5 in ±1).
- **The frigate:** the load line 15 ft 10 in above the base at FP, 16 ft 10 in at AP, 16 ft 3½ in
  at dead flat. Two checks fit it: the wale's lower edge 2½ in above it at dead flat (Steel's
  text: "a few inches higher"), and Steel's rule of five-eighths of the top-timber line's height
  at the lowest place, taken from the keel's underside, 5/8 x 28 ft 6 in = 17 ft 9¾ in against
  the draught at dead flat, 17 ft 9½ in (arithmetic). To the false keel's underside instead, the
  line would lie 5 in lower and the sill 7 ft 10½ in above it.
- **The cutter:** level, 9 ft 9 in above the base (no false keel).
- **The sloop:** 6 ft 7 in above the base at FP, 8 ft 7 in at AP, 7 ft 4½ in at dead flat
  (judgement on the rabbet). Her length between perpendiculars is not printed: **50 ft 3 in is
  taken** (judgement), from the after body's room of about 2 ft 1 in a timber and from Folio I's
  52 ft 0 in (row C) less the stem's 1 ft 0 in moulding and a post of about 9 in (not read). It
  places her after-body stations within about 4 in.

### 5.2 By station

**x** forward of the mid-perpendiculars, **z** above the load line, metres. **Rail** is the
top-timber line (the top of the side; Folio LV's sheer rail follows it), **topside** the topside
line (the top of the drifts over the quarterdeck and forecastle). **hb** half-breadths are
moulded, to the outside of the frame; add the plank (§5.4) for the outside. **hb water** is the
side at the load line: on Steel's lower breadth sweep where the section reaches it (an arc of
the sweep's length, centred on the lower height of breadth that far inside the main
half-breadth; it agrees with the nearest diagonal within 3 in at every such station of the
frigate but timber 7, 5 in at a diagonal 6¾ ft below the line), otherwise straight between the
two diagonal points that bracket the line ("diag"). The sweep and the straight line are lower
bounds on a convex section; the larger is given (judgement, ±2 in for the frigate, ±3 in at the
cutter's H and K, where the sweep falls 6-7 in inside the 5th diagonal). The **deck** is the
upper deck at side: Steel's three middle-line heights (afore at FP, midships at dead flat, abaft
at AP) joined by a parabola (judgement; Steel draws them with circular moulds, OCR
`:15581-15586`), less the beams' round up. The **sill** is the deck plus the plank-to-sill
height. **hb sill** is on the upper breadth sweep where the frigate has one, otherwise straight
between the breadth line and the top-timber line (judgement).

**The frigate of 36** (L 137 ft 0 in; FP at x = +20.88, AP at -20.88; the ports run from x =
+17.73, the foremost's fore side, to -19.51, the after port's aft side):

| Timber | x | Rail z | Topside z | hb water | hb rail | hb topside | hb water from | Deck z | Sill z | hb sill |
|---|---|---|---|---|---|---|---|---|---|---|
| 30 | -20.02 | 4.27 | 5.04 | 1.31 | 3.72 | 3.62 | diag 4th-5th | 2.07 | (no port) | |
| 29 | -19.28 | 4.20 | 4.94 | 2.37 | 3.84 | 3.72 | diag 5th-6th | 2.04 | 2.70 | 4.13 |
| 27 | -17.81 | 4.09 | 4.82 | 3.72 | 4.05 | 3.94 | sweep | 1.98 | 2.64 | 4.42 |
| 25 | -16.33 | 3.96 | 4.70 | 4.35 | 4.24 | 4.13 | sweep | 1.92 | 2.58 | 4.61 |
| 23 | -14.86 | 3.85 | 4.60 | 4.72 | 4.42 | 4.29 | sweep | 1.87 | 2.53 | 4.77 |
| 19 | -11.91 | 3.67 | 4.41 | 5.19 | 4.70 | 4.57 | sweep | 1.78 | 2.45 | 5.02 |
| 15 | -8.97 | 3.52 | 4.25 | 5.47 | 4.90 | 4.79 | sweep | 1.72 | 2.38 | 5.18 |
| 11 | -6.02 | 3.41 | 4.13 | 5.63 | 5.04 | 4.95 | sweep | 1.66 | 2.32 | 5.29 |
| 7 | -3.07 | 3.33 | 3.88 | 5.70 | 5.09 | ... | sweep | 1.63 | 2.29 | 5.35 |
| ⊕ | +2.11 | 3.27 | | 5.73 | 5.11 | | sweep | 1.62 | 2.28 | 5.41 |
| C | +5.77 | 3.29 | | 5.73 | 5.11 | | sweep | 1.64 | 2.30 | 5.42 |
| G | +8.71 | 3.33 | | 5.71 | 5.11 | | sweep | 1.68 | 2.34 | 5.42 |
| L | +11.66 | 3.43 | 3.98 | 5.55 | 5.03 | 4.94 | sweep | 1.74 | 2.40 | 5.36 |
| P | +14.61 | 3.54 | 4.11 | 5.03 | 4.81 | 4.78 | sweep | 1.81 | 2.47 | 5.05 |
| T | +17.54 | 3.70 | 4.26 | 3.73 | 4.14 | 4.20 | sweep | 1.90 | 2.56 | 4.15 |
| W | +19.01 | 3.81 | 4.38 | 2.52 | 3.38 | 3.54 | sweep (= 5th diag.) | 1.96 | (no port) | |
| X | +19.75 | 3.89 | 4.46 | 1.65 | 2.77 | 3.00 | diag 4th-5th | 1.99 | (no port) | |

The derived sill at dead flat, 2.28 m, is 0.06 m under Folio I's 2.34 m (7 ft 8 in). **Folio I's
figure is the source's statement** of the sill above the water; the derived column gives the
sill's sheer along the run, about 0.4 m from midships to either end (judgement: B8 may lift the
column by 0.06 m to meet Folio I at midships, and say so).

**The cutter of 273 tons** (L 78 ft 0 in; FP at +11.89, AP at -11.89; the ports run from +9.14 to
-9.80):

| Timber | x | Rail z | hb water | hb rail | hb water from | Deck z | Sill z | hb sill |
|---|---|---|---|---|---|---|---|---|
| 18 | -10.03 | 2.43 | 1.17 | 2.90 | diag 3d-4th | 1.14 | (no port) | |
| 16 | -8.71 | 2.31 | 2.28 | 3.25 | diag 4th-5th | 1.06 | 1.59 | 3.30 |
| 14 | -7.39 | 2.18 | 2.96 | 3.54 | diag 5th-breadth | 0.99 | 1.52 | 3.59 |
| 12 | -6.07 | 2.10 | 3.61 | 3.78 | sweep | 0.93 | 1.46 | 3.83 |
| 10 | -4.75 | 2.03 | 3.95 | 3.99 | sweep | 0.88 | 1.41 | 4.03 |
| 8 | -3.43 | 1.97 | 4.15 | 4.14 | sweep | 0.84 | 1.38 | 4.18 |
| 4 | -0.79 | 1.92 | 4.36 | 4.32 | sweep | 0.81 | 1.34 | 4.36 |
| ⊕ | +1.85 | 1.94 | 4.40 | 4.36 | sweep | 0.83 | 1.36 | 4.40 |
| D | +4.50 | 2.04 | 4.25 | 4.24 | sweep | 0.89 | 1.42 | 4.28 |
| F | +5.82 | 2.12 | 4.02 | 4.08 | sweep | 0.94 | 1.47 | 4.11 |
| H | +7.14 | 2.22 | 3.61 | 3.80 | sweep (±3 in) | 1.00 | 1.54 | 3.82 |
| K | +8.46 | 2.34 | 2.93 | 3.33 | sweep (±3 in) | 1.08 | 1.61 | 3.32 |
| M | +9.78 | 2.48 | 1.86 | 2.57 | diag 4th-5th | 1.17 | (no port) | |
| N | +10.44 | 2.55 | 1.24 | 2.06 | diag 3d-4th | 1.22 | (no port) | |

The derived sill at dead flat, 1.36 m (4 ft 5½ in), against Folio I's 1.37 m (4 ft 6 in).

**The coasting sloop of 60 tons** (L 50 ft 3 in, judgement; FP at +7.66, AP at -7.66; no ports.
Her table has no sweeps, so every half-breadth at the water is straight between the table's
points, judgement):

| Timber | x | Rail z | Topside z | hb water | hb rail | hb topside | hb water from |
|---|---|---|---|---|---|---|---|
| 13 | -6.59 | 1.26 | 1.36 | 1.71 | 1.77 | | diag 5th-breadth |
| 12 | -5.94 | 1.19 | 1.29 | 1.94 | 1.88 | 1.85 | diag 5th-breadth |
| 10 | -4.66 | 1.08 | 1.19 | 2.13 | 2.03 | 2.02 | between the breadths |
| 8 | -3.42 | 1.03 | 1.13 | 2.26 | 2.14 | 2.12 | upper breadth-top timber |
| 6 | -2.11 | 1.01 | 1.11 | 2.36 | 2.24 | 2.22 | upper breadth-top timber |
| 4 | -0.85 | 0.99 | | 2.41 | 2.29 | | upper breadth-top timber |
| 2 | +0.47 | 1.01 | | 2.45 | 2.34 | | upper breadth-top timber |
| ⊕ | +1.74 | 1.06 | | 2.51 | 2.34 | | upper breadth-top timber |
| A | +2.87 | 1.14 | | 2.50 | 2.34 | | between the breadths |
| C | +4.17 | 1.27 | | 2.43 | 2.26 | | between the breadths |
| E | +5.44 | 1.41 | | 2.19 | 2.08 | | diag 5th-breadth |
| F | +6.08 | 1.51 | | 1.91 | 1.88 | | diag 5th-breadth |
| G | +6.72 | 1.63 | | 1.22 | 1.42 | | diag 4th-5th |

### 5.3 The other points

**The frigate of 36** (x, z in metres; arithmetic on §4's figures):

- **Keel:** the main keel's underside at -5.59 at AP and -5.28 at FP (the draughts); the false
  keel 0.13 below. The tread is 126 ft 2 in from the post's aft side to the forefoot (read); where
  its ends stand against the perpendiculars is not printed.
- **Stem** (judgement): the aft side swept from the centre 18 ft 1 in abaft FP and 18 ft 6 in up,
  through FP at the lower deck's 16 ft 8 in afore (a radius of 18 ft 2 in); the fore side the
  moulding, 1 ft 3½ in, outside it. The fore side at [+21.25, 0.00], [+21.30, 0.82], [+21.14, 2.19]
  and the head at [+20.37, 4.01] (29 ft 0 in above the base). The circle carries the head 3 ft
  back from its foremost point; whether Steel's stem leaned so, or the knee and head rails hid it,
  is not on these pages.
- **Stern:** the lower counter's knuckle at [-22.71, 2.70], the upper counter's at [-23.16, 3.39],
  the taffrail's top at [-24.00, 5.92] (36 ft 4 in above the base, 10 ft 3 in abaft AP); the
  taffrail 2 ft 4 in deep. The post and the wing transom (Folio IV) were not read.
- **Wale** (x, lower edge, upper edge): [+20.88, 0.97, 2.11] at the stem, [+2.11, 0.07, 1.21] at
  dead flat, [-20.02, 1.05, 2.19] at the after timber; 3 ft 9 in broad, 6 in thick. Steel keeps
  the wales nearly parallel to the top-timber line fore and aft (text, OCR `:15206-15207`).
- **Sheer rail** (Folio LV): 4.01 at FP, 3.27 at dead flat, 4.32 at AP; the table's top-timber
  line, extended.
- **Upper deck at side** at FP and AP: 2.03 and 2.11; least, 1.61, near the middle.
- **Lower deck** (no ports): at the middle line +0.25 at FP, -0.16 at dead flat, +0.33 at AP;
  at side 4½ in lower.
- **Quarterdeck at side** (judgement: its round up taken as the upper deck's 7 in, "agreeably
  to the lights below"; its fore end at about 57 ft afore AP, x -3.5, taking the midship stern
  timber's aft side 8½ ft abaft AP at the deck's height): 4.19 at AP, 3.93 at -14.78, 3.67 at
  -3.51. Its gun-port sills 1 ft 7 in above it (4.67 at AP to 4.15 forward), its carronade-port
  sills 11 in (4.47 to 3.95); the roughtree rail's top 4 ft 0 in above it (5.41 to 4.89).
- **Forecastle at side** (judgement: its flat taken as 3 in, its 36 ft 0 in from FP): 3.67 at
  +9.91, 4.00 at FP; the carronade-port sills 11 in above it (3.95 to 4.28). Its gun ports' sill
  and depth are blank in Folio XLVI.
- **Port sizes:** upper deck 2 ft 10 in x 2 ft 5 in (0.86 x 0.74), quarterdeck guns 2 ft 5 in x
  2 ft 4 in (0.74 x 0.71), carronades 3 ft 4 in x 2 ft 7 in (1.02 x 0.79). Thirteen upper ports a
  side, 7 ft 2 in apart from the first's fore side 10 ft 4 in abaft FP: centres at 11 ft 9 in +
  10 ft *k* abaft FP, *k* = 0 to 12 (arithmetic). The run so laid ends 3 ft 10 in afore AP against
  the printed 4 ft 6 in (8 in long, judgement: the folio's rounding).

**The cutter:**

- **Keel:** underside at -3.30 at both perpendiculars (level draught, no false keel).
- **Stem head:** 19 ft 6 in above the base, +2.97; no centre is printed, so its x is not given
  (judgement: at FP, +11.89, until a draught is read).
- **Stern:** the lower counter's knuckle at [-13.72, 2.21]; the upper counter's at [-14.17, 3.20],
  where the taffrail's top also stands (both 20 ft 3 in; the counter timber's position is blank).
- **Wale:** [+11.89, 0.94, 1.55] at the stem, [+1.85, 0.15, 0.76] at dead flat, [-10.03, 0.64,
  1.25] at the after timber; 2 ft 0 in broad, 4 in thick.
- **Upper deck at side:** 1.33 at FP, 0.83 at dead flat, 1.28 at AP. **Lower deck** at the middle
  line: -0.38 afore, -0.84 at dead flat, -0.66 abaft.
- **Ports:** eight a side, 2 ft 0 in x 1 ft 10 in (0.61 x 0.56), 6 ft 7 in apart from the first's
  fore side 9 ft 0 in abaft FP: centres at 10 ft 0 in + 8 ft 7 in *k* abaft FP, *k* = 0 to 7; the
  last's aft side falls 6 ft 11 in afore AP against the printed 6 ft 10 in (arithmetic).
- **Folio LV's sheer rail:** 2.92 at FP, 2.06 at dead flat, 3.00 at AP (§6: above the table's
  top-timber line).

**The sloop** (x on the judged length):

- **Keel:** underside at -2.13 at FP and -2.74 at AP (Folio I's draughts).
- **Stem head:** 13 ft 3 in above the base, +2.03 at FP; no centre printed.
- **Stern:** the lower counter's knuckle at [-7.81, 0.76], the taffrail's top at [-8.24, 1.80]
  (14 ft 6 in above the base, the counter timber 1 ft 11 in abaft AP).
- **Wale:** [+7.66, 0.20, 0.61] at the stem, [+1.74, -0.44, -0.03] at dead flat, [-6.59, -0.24,
  0.17] at the after timber; 1 ft 4 in broad, 4 in thick. Under water amidships at the load
  draught (on the judged rabbet; to the keel's upper edge instead, 5 in less so).
- **Deck at side** (the beam at the middle line, plus the 2-in plank, less the 6-in round up):
  1.40 at FP, 0.93 at dead flat, 1.27 at AP on the rise. The waist rises 5 in above it.
- **Folio LV's sheer rail:** 1.75 at FP, 1.06 at dead flat, 1.47 at AP.

### 5.4 The midship sections (dead flat, z above the load line; half-breadth with the plank)

The plank is half of Folio I's extreme less moulded breadth: 4 in for the frigate, 2½ in for the
cutter, 2 in for the sloop (arithmetic). The first point is the keel's rabbet at half the keel's
siding amidships, no plank.

- **Frigate:** [-4.96, 0.20], [-4.62, 2.02], [-4.17, 3.25], [-3.58, 4.02], [-2.85, 4.65],
  [-2.05, 5.17], [0.29, 5.84], [0.80, 5.84], [3.27, 5.21].
- **Cutter:** [-2.97, 0.17], [-2.58, 0.95], [-2.24, 1.67], [-1.91, 2.40], [-1.50, 3.18],
  [-1.00, 3.85], [0.50, 4.52], [1.94, 4.42].
- **Sloop:** [-2.24, 0.13], [-2.08, 1.39], [-1.98, 1.71], [-1.66, 2.18], [-1.18, 2.46],
  [-0.76, 2.53], [-0.46, 2.57], [-0.06, 2.57], [1.06, 2.39].

## 6. The checks (the tables' scale)

A table has no drawn scale; its check is the printed dimensions measured back through it.

| Check | Frigate, 36 | Cutter | Sloop |
|---|---|---|---|
| Dead flat's station against Folio I, E | 61 7 = 61 7 | **32 11 against 32 7** | 19 5 = 19 5 |
| Foremost and after timbers against Folio I, F and G | 3 8½, 2 10: equal | 4 9, 6 1: equal | 3 0¾, 3 6: equal |
| Timber room, after body | 2 ft 5 in; seven to dead flat put it 75 ft 4 in afore AP, the gun deck 136 ft 11 in against 137 ft 0 in | 2 ft 2 in both bodies; the stations sum to 78 ft 0 in, Folio I's range of the deck | about 2 ft 1 in; no length printed |
| Main half-breadth at dead flat, doubled, against Folio I's moulded breadth | 37 8 against 37 6 | 29 3 = 29 3 | 16 6 against 16 4 |
| Wale's lower edge + its breadth + the sheer strakes, against the top-timber line at dead flat | 16 6 + 3 9 + 6 9 = 27 0, equal | 10 3 + 2 0 + 4 4 = 16 7 against 16 1½ | (no sheer strakes printed) |
| Folio LV's sheer rail against the top-timber line extended to FP, dead flat, AP | 29 0 / 27 0 / 31 0 against 29 0 / 27 0 / 31 1¼ | 19 4 / 16 6 / 19 7 against about 18 8 / 16 1½ / 18 3¾ | 12 4 / 10 10 / 13 5 against about 12 5½ / 10 10 / 13 5½ (aft, on the rise's topside line) |
| Waist depth against the top-timber line less the deck at side | 6 9 against 5 5 | 4 1 against 3 8 (the folios' rail less the deck: 4 0½) | 0 5 against 0 5 |
| Sill above the water from the deck folios, against Folio I's row Q | 7 5½ against 7 8 | 4 5½ against 4 6 | (no ports) |

**Read so:** the frigate's table and folios are one ship to an inch or two; the derived sill's
2½ in and the waist's 1 ft 4 in are the folios' own spread (the waist perhaps measured to a rail
above the side; judgement). The cutter's folios agree with one another (rail, waist, wale and
strake) and with her table's stations, breadth and sill, but carry her rail 4½ in higher at dead
flat, 8 in higher at FP and 1 ft 3 in at AP than her table's top-timber line, and her dead flat
4 in further aft: a cutter of the same burthen drawn with more sheer, or the rail standing on
the timbers (judgement). The profile's rail should follow the table, with the folios' rail
recorded (judgement). The sloop's table and folios agree where both speak.

## 7. What the source cannot give

- **None of the three is the file's own ship.** These are Steel's standard bodies: the 36 is not
  *Amazon*, the cutter not *Sherbourne*, the sloop not *Culloden* (the design's "plainly",
  `shared-design.md` §1.5). Scaling them to the files is the builder's judgement.
- **The half-breadth at the water** is printed nowhere; §5.2 computes it.
- **The load line's datum:** Steel's text names the keel's underside, not which keel; for the
  sloop the rabbet's place in the keel is a general note, not her figure.
- **The sloop's length between perpendiculars** (Folio I's rows A and B blank).
- **The stem's fore-and-aft line** for the cutter and the sloop (no centre printed), and for the
  frigate only through the judgement of §5.3.
- **The frigate's forecastle gun ports' sill and depth** (blank), **the quarterdeck's round up**
  (no figure), and the quarterdeck's and forecastle's ends as positions (lengths only).
- **The post and the wing transom** (Folio IV, OCR `:29579-29590`): not read in this research.
- **The cutter's and sloop's quarterdeck, forecastle and roughtree rows** on the right leaves of
  Folios XLIII and XLVI were not fetched (the cutter and sloop are blank in Folio XLII).
- **The tables' rising line and cutting-down line** are on the leaves (read), not transcribed.

## 8. Provenance

**Fetched** (2026-10-28; a generic user-agent; nothing personal in any request):

- Metadata: https://archive.org/metadata/elementspractice00stee
- The item's indexes: https://archive.org/download/elementspractice00stee/elementspractice00stee_hocr_pageindex.json.gz,
  `.../elementspractice00stee_hocr_searchtext.txt.gz`, `.../elementspractice00stee_scandata.xml`,
  `.../elementspractice00stee_page_numbers.json` (to find the leaves).
- n467 and n485, by the IIIF image service at full size:
  https://iiif.archive.org/image/iiif/3/elementspractice00stee%2felementspractice00stee_jp2.zip%2felementspractice00stee_jp2%2felementspractice00stee_0468.jp2/full/max/0/default.jpg
  and the same with `_0486`.
- Every other leaf from the item's JP2 archive (the IIIF service timed out on two):
  https://archive.org/download/elementspractice00stee/elementspractice00stee_jp2.zip/elementspractice00stee_jp2%2Felementspractice00stee_0477.jp2
  and the same with `_0488`, `_0489`, `_0490`, `_0491`, `_0500` to `_0503`, `_0524`, `_0525`,
  `_0548` to `_0551`, `_0570` to `_0572`, `_0578`, `_0588`, `_0589`, `_0596`, `_0597`.
- Each leaf in the reader: https://archive.org/details/elementspractice00stee/page/n467 (and
  n476, n485, and so on, by §2).

**Cache** (`D:/Projects/FreeSail/reference-cache/steel-1805-bodies/`, outside the repository):
`elementspractice00stee_0468_full.jpg`, `elementspractice00stee_0486_full.jpg` (JPEG), the 23
`elementspractice00stee_NNNN.jp2` leaves of §2, `info_0468.json` and `info_0486.json` (IIIF),
`elementspractice00stee_metadata.json`, `_scandata.xml`, `_page_numbers.json`,
`_hocr_pageindex.json.gz`, `_hocr_searchtext.txt.gz`.

**Scripts** (kept outside the repository in the session's scratch directory, under
`stage0/pages/steel/`): `steel_findleaves.py`, `steel_heads.py`, `steel_leaftext.py` (the
leaves from the indexes); `steel_info.py`, `steel_crop.py`, `steel_strip.py`, `steel_cols.py`
(the images' sizes and the crops read); `steel_compare.py` (Folio I against the owner's copy);
`steel_bodies.py` (the three tables as typed, §5.2), `steel_decks36.py` (§5.3) and
`steel_section.py` (§5.4).
