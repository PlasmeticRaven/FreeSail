# Pages: Chapman 1768, Pl. LIX No. 3, the English smack for flatfish (October 2026)

Stage 0 research for package 75, the page named by `Build-Ships.md` §19.1 item 11 and by the
shared draft (`ships-design/shared-design.md` §1.5, the smack's row; §5 item 13). It serves
`data/ships/smack.yaml` (the *Culloden*, `smack()` in `tools/gen_ships.py`) and the builder B8,
who draws a sourced hull profile for the file (`Build-Ships.md` §5). The dimensions this note
measures back are those read in `docs/design/VesselReferences-2026-10.md:315` (Chapman's text,
the 1971 edition p. 69): 39¼ Swedish ft between the perpendiculars, breadth moulded 13⅔,
draught 6½. Facts only: the images are the museum's photographs, kept outside the repository
(§1.1).

The marks:

- **read**: the plate's drawing or the record's text was seen on the image or page.
- **catalogue**: from the museum's record only.
- **measured**: off the image at the scale of §2; the uncertainty is stated.
- **judgement**: reasoning by this note.

**Units and datums.** Swedish feet (0.2969 m; 0.974 English ft), to two decimals, with metres
in brackets. Positions along the vessel are feet forward of the **mid-perpendiculars**, the
middle of the two dashed perpendiculars drawn on the profile (§1.2), positive forward, as the
profile's `x`; they are taken along the keel, as the plate draws its stations. Heights are
above the **load water line** (LWL, §3), positive up, as the profile's `z`, taken square to the
keel at that `x`, that is along the station lines. The LWL lies 2.58° to the keel (her drag), so
in a frame level with the water a point stands at `x − 0.045 z` and `0.999 z` (judgement: the
stem head moves 0.39 ft aft, the taffrail 0.29 ft aft, the post's heel 0.29 ft forward; §4.5
gives both for the ends). The image is turned 0.23° on its page; every reading was rotated
about it so that the keel's lower edge is level (residuals 0.4 px or less).

## 0. In brief

- **The plate is public domain and was fetched at full size**: Sjöhistoriska museet,
  Stockholm, "Architecturan LIX", three photographs under the Public Domain Mark; the
  6000-px colour photograph is measured (§1.1).
- **The scale checks, once the plate's vertical is allowed for.** The bar gives 47.82 px a
  Swedish foot. Measured back: 39.12 ft between the perpendiculars against 39¼ (−0.3%);
  13.68 ft moulded breadth against 13⅔ (+0.1%); 6.56 ft draught at the after perpendicular
  against 6½ (+0.9%). Lengths up the page read 3% short against lengths along it (the
  half-breadth plan against the body plan, 0.970 to 0.974 at three stations), and every height
  and half-breadth below is taken at 46.39 px a foot (§2).
- **The draught**: 6.56 ft aft (1.95 m), 4.80 ft forward (1.43 m), 5.68 ft at the middle
  (1.69 m), to the keel's lower edge at the perpendiculars; 1.76 ft of drag. The stated 6½ is
  the after draught (§3).
- **The sheer**: the rail stands 4.49 ft (1.33 m) above the water at its lowest, 4.6 ft abaft
  the middle; 5.60 ft at the transom's side, 7.24 ft at the stem; the stem head 8.68 ft and the
  taffrail 6.54 ft (§4.3, §4.5).
- **The decks** are drawn only at the ends: an after deck from the transom to 14.3 ft abaft
  the middle at 2.48 to 2.62 ft at side (0.74 to 0.78 m), nearly parallel to the water line;
  a fore deck from 6.0 ft abaft the middle to the stem, 3.05 rising to 4.96 ft. None is drawn
  in the waist between (§4.4).
- **The wale**'s lower edge stands 0.40 to 0.49 ft above the water from station 9 to station 3
  and 0.70 ft at ⊕; the band is 0.82 to 0.89 ft deep (§4.2).
- **No ports** are drawn (§4.8).
- **Against the file** (§6, recorded, not moved): the file's deck at 0.75 m is this plate's
  after deck; the file's 12.2 m waterline, 4.3 m beam and 1.9 m mean draught stand against the
  plate's 11.46 m, 4.06 m and 1.69 m.

## 1. The source

### 1.1 The object, the images and the cache

| | |
|---|---|
| Object | Sjöhistoriska museet, Stockholm: "Ritning", identifier "Architecturan LIX", DIMU code 011024789741, UUID 31d08552-222c-41d7-9a5d-90e18b9d4e63; Plate LIX of F. H. af Chapman's *Architectura Navalis Mercatoria* (1768); producers Lars Bogeman and F. H. af Chapman; copperplate engraving on paper; collection Sjöhistoriska museets arkiv, "Samling: Chapman" (catalogue) |
| Record | https://digitaltmuseum.org/011024789741 (redirects to https://digitaltmuseum.org/011024789741/ritning); published on the site 15 August 2014 (catalogue) |
| Rights shown | "Public domain mark (CC pdm)", linked to https://creativecommons.org/publicdomain/mark/1.0/, with the credit "Photo: Sjöhistoriska museet" (read). The site's general notice says many of its images are in copyright; this record's are marked public domain. Its download button reads "Accept license and download photo"; the image addresses below were fetched directly |
| Image measured | `069ELifgcWc6J`: https://ems.dimu.org/image/069ELifgcWc6J?filename=Architecturan%20LIX.jpg&dimension=max&quality=100&dpi=300&mediatype=image/jpg, 6000 x 3975 px, JPEG, 18,933,293 bytes, sha256 `10ee733e11eba2cd0e165f5386fd145aae81dee051d83220474285fabc4c1333`. Colour; the whole sheet with its margins and stains |
| Image checked | `022uK3KjAwHr`: the same address with that id, 4000 x 2562 px, 7,881,162 bytes, sha256 `1dd96b8bd6909a547e3b94c4f53181690b68e024f2e56411fcc008b9878f6630`. Colour, white-balanced, the plate area |
| Image not used | `022uK3KjAwHs`: the same address with that id, 4000 x 2951 px, 3,952,486 bytes, sha256 `48db7647b3341c781af244958c228d94e22abcd5ab7490e001df71c84e8c2b40`. Black and white, high contrast; its heights read about 6% long (§2.4) |
| Also fetched | The record page as served (`record/`); the Internet Archive's metadata for the 1971 Adlard Coles reprint, `architecturanava0000fred` (https://archive.org/metadata/architecturanava0000fred), to see what of it is open; not used (the reprint is in copyright) |
| Cache | `D:/Projects/FreeSail/reference-cache/chapman-pl59/architecturan-LIX-069ELifgcWc6J-max.jpg`, `.../architecturan-LIX-022uK3KjAwHr-max.jpg`, `.../architecturan-LIX-022uK3KjAwHs-max.jpg`; `.../record/digitaltmuseum-011024789741.html`; `.../ia-metadata/architecturanava0000fred-metadata.json`. Fetched 2026-10-28 with a generic user-agent |

**What the record says** (catalogue): the plate's three figures are a Dutch hooker (No. 1), an
English herring buss (No. 2) and No. 3, given in Chapman's original description as "Engelsk
Flurder-Sump (Ritn N:o 3)", an English well-boat for flounders; the museum's summary calls it a
"sump". `VesselReferences-2026-10.md` calls it the English smack for flatfish, after the 1971
edition. The record gives no dimensions.

### 1.2 What No. 3 is on the plate (read)

No. 3 takes the lower left of the plate, bow to the right:

- **The profile** (sheer plan): the side from the transom to the stem head, the rail, a second
  moulded band below it, the wale, the deck lines dashed, the LWL as a single straight line
  inclined to the keel, other water lines below it, the keel, a raked post with the rudder hung
  on it, the stem, a channel with three deadeyes and their chain plates, inboard works dashed,
  and a heavy curve running down from the ends to the floor amidships (Chapman's rising line,
  judgement). Two **dashed perpendiculars** run from above the rail to below the keel: the
  after one touches the after side of the post where it meets the counter, the fore one the fore
  side of the stem above the water, where the stem stands square to the keel. A dashed base line
  runs between them along the top of the keel.
- **The stations**: every third frame is drawn and lettered under the keel, 14, 12, 9, 6, 3
  abaft the midship frame ⊕ and C, F, H before it, 1.54 ft a frame (measured: 220.5 px for
  three). ⊕ is drawn as two lines 0.59 ft apart with the sign between them; its `x` is taken at
  their middle. The mid-perpendiculars fall on station 3 (+0.02 ft).
- **The half-breadth plan**, under the profile on the same stations, its centre line at the
  bottom: the side's lines and the water lines, the station lines rising from the centre line
  to the outermost line.
- **The body plan**, above the profile, the after body to the left and the fore body to the
  right of a centre line, inside a dashed rectangle whose sides are the moulded breadth; the
  LWL's height at ⊕ is marked by a short line outside each side; diagonals lettered with the
  stations.
- **The scale bar** for No. 3 (bar B), between the body plans of No. 2 and No. 3, with three
  rows lettered S, E and F (Swedish, English and French feet), each with a first foot divided
  in quarters. A second bar (bar A), under No. 1's body plan, is not No. 3's (§2.1).

## 2. The scale and its check

### 2.1 The bar (measured)

| Row | Px a foot (fit over the divisions) | rms | In the true ratio of the feet |
|---|---|---|---|
| S, 0 to 10 ft | 47.80 (end to end 47.82) | 0.5 px | — |
| E, 0 to 6 ft | 49.43 | 0.6 px | S/E 0.967 against 0.974 |
| F, 0 to 7 ft | 52.42 | 0.4 px | S/F 0.912 against 0.914 |

The S row's 47.82 px is used throughout (one pixel 0.021 ft, 6.2 mm). Bar A gives 45.97 px a
Swedish foot; with it No. 3 would measure 40.7 ft between the perpendiculars and 14.2 ft in
breadth, against 39¼ and 13⅔, so it is not No. 3's (measured; judgement on its figure).

### 2.2 The plate's vertical (measured)

The same breadth is drawn twice: across the half-breadth plan (up the page) and across the body
plan (along it). The half-breadth plan's main breadth line, the outermost of its lines amidships,
on which the station lines end, against each frame's greatest half-breadth in the body plan:

| Station | Half-breadth plan, up the page | Body plan, along the page | Ratio |
|---|---|---|---|
| ⊕ | 317.3 px | 327.0 px (the frame on the dashed side, both halves) | 0.970 |
| C | 312.0 px | 321.1 px | 0.972 |
| F | 281.5 px | 289.0 px | 0.974 |

The second colour image gives the same 0.970 at ⊕ (475.4 px against 490 px across the body
plan). So lengths up the page read 3% short against lengths along it, on the sheet, not in one
photograph (judgement: the paper's shrinkage across the plate after printing). Every height and
every half-breadth from the half-breadth plan is taken at 47.82 × 0.970 = 46.39 px a foot;
lengths along the page at 47.82. Unscaled, the heights would be 3% lower: the after draught
6.36 ft instead of 6.56.

### 2.3 The stated dimensions measured back (measured)

| Dimension | Stated (`VesselReferences-2026-10.md:315`) | Measured | Difference |
|---|---|---|---|
| Between the perpendiculars | 39¼ Sw ft | 1870.5 px = 39.12 ft (11.61 m; 38.1 English ft) | −0.3% |
| Breadth moulded | 13⅔ | the body plan's dashed sides, 654.1 px = 13.68 ft (4.06 m; 13.3 English ft); the ⊕ frame lies on them from 2.3 ft above the water to 0.6 ft below it | +0.1% |
| Draught | 6½ | 6.56 ft at the after perpendicular to the keel's lower edge (1.95 m; 6.4 English ft) | +0.9% |

The length and the breadth check the scale along the page; the draught checks the factor of
§2.2. With the breadth on the dashed sides and the frame on them, the stated breadth is the
moulded one, as read; the plank is not drawn.

### 2.4 The other images (measured)

- `022uK3KjAwHr` reads 35.00 px a foot on its bar; on it the length comes to 39.63 ft and the
  body plan's breadth to 14.0 ft, 1.3 and 2.3% long, so its bar and its figure do not agree as
  well as on the measured image. Its vertical ratio is the same (§2.2). Used as that check only.
- `022uK3KjAwHs` reads 36.40 px a foot; the length 38.87 ft, but the heights (keel to rail,
  keel to LWL, the half-breadth plan) 8.7 to 9.3% longer than the measured image's against the
  same bar, 5 to 6% longer than §2.2 allows. A distorted copy (judgement); not measured.

## 3. The load water line and the draught

The LWL is the single straight line drawn from the rudder's after edge to the stem, crossing
the post and the stem and continued by the short marks outside the body plan at ⊕ (read; its
height in the body plan agrees with the profile within 4 px, 0.09 ft). Thirteen points along it
fit one straight line within 0.7 px. It lies 2.58° to the keel.

| | After perpendicular | Middle (mid-perpendiculars) | Fore perpendicular |
|---|---|---|---|
| Draught to the keel's lower edge | 6.56 ft (1.95 m) | 5.68 ft (1.69 m) | 4.80 ft (1.43 m) |

- The keel's lower edge is one straight line from the post's heel to the forefoot (residuals
  0.7 px or less); the drag over the perpendiculars is 1.76 ft.
- The dashed base line, at the top of the keel, stands 0.87 ft above its lower edge
  (measured, at ⊕); the frames of the body plan meet the keel there.
- The LWL meets the post's after edge 19.31 ft abaft the middle and the stem's fore edge
  19.27 ft before it: 38.58 ft (11.46 m; 37.6 English ft) on the line (measured). The moulded
  water line ends at the rabbets, about 18.3 ft from the middle at each end (measured, the
  half-breadth plan).
- The rudder's after edge stands 1.5 ft abaft the post at the water and 2.35 ft at the heel
  (measured); it is not part of the profile.
- Uncertainty: ±0.05 ft from the lines' width and ±1% from the scale and §2.2 (judgement).

## 4. The profile, measured

### 4.1 The lines of the side (read; identification as marked)

From the top: **the rail**, a moulded band of three lines about 0.27 ft deep, its top line
taken as the rail; **a second band**, also of three lines, 0.26 ft deep, parallel to the rail
and 0.70 ft below it end to end (measured at every station); **the deck lines**, dashed, three
lines: a pair 0.1 ft apart and a third 0.17 to 0.37 ft below the pair (§4.4); **the wale**, a
band between a light upper line and a heavy lower line, ending square at the stem and in a
scroll at the post; **the LWL**.

- The second band is not at the deck: the deck at side lies 0.4 to 0.5 ft below its foot
  amidships, 0.9 ft at H and 1.5 ft at station 14. It is taken as a moulding on the topside, or the
  top of the planked side with an open rail above it (judgement).
- The band taken as the wale has its lower edge a few inches above the water amidships, which
  is Steel's rule for the main wale (`ships-design/shared-design.md` §1.5, read there;
  judgement on the identification).

### 4.2 By station (measured)

Heights above the LWL, ft (m in brackets); `x` the station line's. ±0.03 ft in reading, ±1%
in scale.

| Station | x | Rail | Band, top | Band, foot | Deck at middle line | Deck at side | Wale, upper | Wale, lower | Keel, lower edge |
|---|---|---|---|---|---|---|---|---|---|
| 14 | −16.85 (−5.00) | 5.05 (1.50) | 4.36 (1.29) | 4.06 (1.20) | 2.90 (0.86) | 2.55 (0.76) | 1.77 (0.53) | 0.95 (0.28) | −6.44 (−1.91) |
| 12 | −13.81 (−4.10) | 4.81 (1.43) | 4.09 (1.21) | 3.85 (1.14) | not drawn | not drawn | 1.53 (0.45) | 0.70 (0.21) | −6.30 (−1.87) |
| 9 | −9.22 (−2.74) | 4.57 (1.36) | 3.87 (1.15) | 3.61 (1.07) | not drawn | not drawn | 1.31 (0.39) | 0.47 (0.14) | −6.09 (−1.81) |
| 6 | −4.58 (−1.36) | 4.49 (1.33) | 3.79 (1.13) | 3.54 (1.05) | 3.42 (1.02) | 3.07 (0.91) | 1.25 (0.37) | 0.40 (0.12) | −5.88 (−1.75) |
| 3 | 0.02 (0.01) | 4.58 (1.36) | 3.88 (1.15) | 3.60 (1.07) | 3.54 (1.05) | 3.17 (0.94) | 1.35 (0.40) | 0.49 (0.14) | −5.68 (−1.69) |
| ⊕ | 4.34 (1.29) | 4.79 (1.42) | 4.09 (1.21) | 3.82 (1.13) | 3.72 (1.11) | 3.38 (1.00), hidden by the channel: interpolated | 1.57 (0.47) | 0.70 (0.21) | −5.48 (−1.63) |
| C | 8.65 (2.57) | 5.22 (1.55) | 4.52 (1.34) | 4.26 (1.26) | 4.06 (1.21) | 3.72 (1.10) | 1.97 (0.59) | 1.09 (0.32) | −5.29 (−1.57) |
| F | 13.27 (3.94) | 5.90 (1.75) | 5.20 (1.54) | 4.97 (1.47) | 4.51 (1.34) | 4.23 (1.26) | 2.66 (0.79) | 1.77 (0.52) | −5.08 (−1.51) |
| H | 16.32 (4.85) | 6.54 (1.94) | 5.84 (1.73) | 5.58 (1.66) | 4.87 (1.45) | 4.68 (1.39) | 3.29 (0.98) | 2.40 (0.71) | −4.94 (−1.47) |

The wale's ends: aft, at the post's scroll, x −18.34, lower 1.02, upper 1.93 (−5.45 m, 0.30,
0.57); forward, cut square at the stem, x 18.47, lower 2.99, upper 3.87 (5.48 m, 0.89, 1.15)
(measured).

### 4.3 The sheer, end to end (measured)

The rail's top line, `x` and `z` in ft (m):

| x | z | | x | z |
|---|---|---|---|---|
| −21.29 (−6.32), at the transom's side | 5.60 (1.66) | | 4.36 (1.29) | 4.79 (1.42) |
| −20.83 (−6.19) | 5.52 (1.64) | | 8.68 (2.58) | 5.22 (1.55) |
| −19.58 (−5.81), the after perpendicular | 5.36 (1.59) | | 13.30 (3.95) | 5.90 (1.75) |
| −18.33 (−5.44) | 5.21 (1.55) | | 16.35 (4.85) | 6.54 (1.94) |
| −16.83 (−5.00) | 5.05 (1.50) | | 17.43 (5.18) | 6.83 (2.03) |
| −13.79 (−4.09) | 4.81 (1.43) | | 18.27 (5.43) | 7.08 (2.10) |
| −9.20 (−2.73) | 4.57 (1.36) | | 18.86 (5.60), at the stem | 7.24 (2.15) |
| −4.56 (−1.35) | 4.49 (1.33) | | | |
| 0.04 (0.01) | 4.58 (1.36) | | | |

The lowest reading is at station 6, 4.6 ft abaft the middle; stations 9 and 3 stand 0.08 and
0.09 ft higher. The sheer rises 1.1 ft from there to the transom and 2.75 ft to the stem.

### 4.4 The decks (measured; identification judgement)

The three dashed lines are taken as the deck at the middle line (the upper of the pair) and the
deck at side (the third): the gap between them is 0.34 to 0.37 ft amidships and closes towards
the stem, 0.19 ft at H and nothing at its end, as the round of a deck does where the breadth
runs out; a beam's depth would not close (judgement). A round of 0.35 ft on 13.7 ft of breadth
is about a third of an inch to the foot.

- **The after deck**, from the transom to a dashed bulkhead line 14.26 ft abaft the middle, at
  side: −20.32: 2.62; −19.49: 2.62; −18.23: 2.58; −16.85: 2.55; −16.14: 2.52; −14.47: 2.49;
  −14.26: 2.48 (−6.03 m, 0.78 to −4.23 m, 0.74). At the middle line 0.20 to 0.35 ft higher
  (2.82 at −19.48, 2.90 at −16.85, 2.78 at −14.47). It runs nearly parallel to the water line,
  0.16 ft above the counter's foot at the post.
- **No deck line** is drawn from −14.26 to −6.00 ft. Over that length a double dashed outline
  stands from about 0.3 ft above the rail to about 0.9 ft below the water line, its upper and
  lower sides roughly parallel to the rail and the water line (read; measured at two
  stations). Not identified (judgement: a well's trunk, an open hold with its coaming, or
  washboards are all possible; none is read).
- **The fore deck**, from −6.00 ft to the stem, at side: −6.00: 3.05; −4.58: 3.07; −3.07: 3.10;
  −0.56: 3.16; 0.02: 3.17; 4.34: 3.38; 6.55: 3.54; 8.65: 3.72; 11.57: 4.02; 13.27: 4.23; 14.71:
  4.42; 16.32: 4.68; 17.85: 4.96 (−1.78 m, 0.91 to 5.30 m, 1.47). At its after end it stands
  0.57 ft above the after deck's fore end.

### 4.5 The ends (measured)

**The stem's fore edge**, low to high, `x`, `z` in ft (m): the forefoot, where the keel's lower
edge ends, 17.49, −4.88 (5.19, −1.45); 17.77, −4.53; 18.41, −3.54; 18.75, −2.66; 18.98, −1.79;
19.15, −0.92; 19.27, 0.00 at the water; 19.36, 0.81; 19.43, 1.68; 19.49, 2.97; 19.51, 4.70;
19.50, 6.85 (5.79, 2.04). Above about 3 ft the stem stands square to the keel on the fore
perpendicular.

**The stem head** rises 1.4 ft above the rail's end: its top slopes from 8.31 ft at its after
edge (x 18.17) to **8.68 ft at its fore edge** (x 19.47; 5.78 m, 2.58 m).

**The stern**, low to high: the post's after edge from its heel, −18.39, −6.52 (−5.46, −1.94),
through −18.60, −5.05; −18.84, −3.33; −19.08, −1.62; to the water at −19.31, 0.00
(−5.73, 0.00); the counter meets the post at −19.59, 2.46 (−5.82, 0.73), on the after
perpendicular; the counter runs aft to the transom's foot at −20.84, 2.92 and −21.32, 3.29
(−6.33, 0.98); the transom, raked aft and rounded, rises to **the taffrail at the middle line,
−22.44, 6.54** (−6.66 m, 1.94 m). The rail meets the transom's side at −21.29, 5.60, so the
taffrail stands 0.94 ft above the rail's after end. The post rakes about 8° from square to the
keel (measured: 0.14 ft aft in each foot of height).

**The keel's lower edge**: from the post's heel, −18.39, −6.52, to the forefoot, 17.49, −4.88,
straight.

In a frame level with the water (the units paragraph above §0): the stem head 19.08, 8.67;
the taffrail −22.73, 6.54; the forefoot 17.71, −4.87; the post's heel −18.10, −6.51; the
rail's ends −21.54, 5.59 and 18.53, 7.23 (judgement on applying it).

### 4.6 The half-breadths (measured; identification as marked)

From the half-breadth plan, at 46.39 px a foot from its centre line (§2.2), ft (m). Three of
its lines are named here: **the main breadth line**, the outermost amidships, on which the
station lines end; **the rail line** (the top-timber line), inside it everywhere, which with
the main breadth line meets the transom's corner aft and the stem forward; **the load water
line**, drawn heavy, ending at the post's rabbet aft and the stem's rabbet forward.

| Station | x | Main breadth | Rail | Load water line |
|---|---|---|---|---|
| 14 | −16.85 (−5.00) | 4.59 (1.36) | 4.30 (1.28) | 3.24 (0.96) |
| 12 | −13.81 (−4.10) | 5.36 (1.59) | 4.96 (1.47) | 4.93 (1.46) |
| 9 | −9.22 (−2.74) | 6.13 (1.82) | 5.71 (1.69) | 5.99 (1.78) |
| 6 | −4.58 (−1.36) | 6.56 (1.95) | 6.19 (1.84) | 6.55 (1.95) |
| 3 | 0.02 (0.01) | 6.78 (2.01) | 6.39 (1.90) | 6.67 (1.98) |
| ⊕ | 4.34 (1.29) | 6.84 (2.03) | 6.44 (1.91) | 6.73 (2.00) |
| C | 8.65 (2.57) | 6.73 (2.00) | 6.32 (1.88) | 6.65 (1.98) |
| F | 13.27 (3.94) | 6.06 (1.80) | 5.68 (1.69) | 5.36 (1.59) |
| H | 16.32 (4.85) | 4.52 (1.34) | 4.33 (1.28) | 2.69 (0.80) |

- **The transom**: the main breadth and rail lines meet it at 2.63 ft (0.78 m) half-breadth,
  at x −21.9 in the plan, against −21.3 for the rail's after end in the profile; the plan's
  transom may stand for a lower height than the rail's (judgement; ±0.7 ft in `x` there).
- **The identification**: the lines cross near the stern and near station 12, where the rail
  line and the water line come within 0.03 ft; they were followed through the crossings by
  their ends and their weight. Elsewhere ±0.03 ft in reading. The rail's half-breadth at ⊕
  agrees with the body plan's frame head (6.47 ft, §4.7) within 0.03 ft, and the main breadth
  with the body plan at ⊕, C and F within 0.03 ft (by §2.2's factor).
- The side tumbles home everywhere: the rail stands 0.2 to 0.4 ft inside the main breadth.

### 4.7 The midship section (measured)

The ⊕ frame in the body plan, moulded (the plank is not drawn), the mean of its two halves,
which agree within 0.1 ft; heights at 46.39 px a foot above the LWL mark at ⊕, half-breadths at
47.82, ft (m):

| z | Half-breadth | | z | Half-breadth |
|---|---|---|---|---|
| 4.74 (1.41), the frame head | 6.47 (1.92) | | −1.57 (−0.47) | 6.60 (1.96) |
| 4.25 (1.26) | 6.58 (1.95) | | −1.90 (−0.56) | 6.48 (1.92) |
| 3.92 (1.17) | 6.64 (1.97) | | −2.33 (−0.69) | 6.24 (1.85) |
| 3.60 (1.07) | 6.70 (1.99) | | −2.54 (−0.75) | 6.08 (1.80) |
| 3.28 (0.97) | 6.75 (2.01) | | −2.76 (−0.82) | 5.88 (1.75) |
| 2.95 (0.88) | 6.80 (2.02) | | −2.98 (−0.88) | 5.62 (1.67) |
| 2.63 (0.78) | 6.82 (2.02) | | −3.19 (−0.95) | 5.31 (1.58) |
| 2.31 (0.69) to −0.60 (−0.18) | 6.83 to 6.84 (2.03), on the dashed side | | −3.41 (−1.01) | 4.89 (1.45) |
| −0.93 (−0.28) | 6.75 (2.01) | | −3.62 (−1.08) | 4.38 (1.30) |
| −1.25 (−0.37) | 6.69 (1.99) | | −3.84 (−1.14) | 3.70 (1.10) |
| | | | −4.05 (−1.20) | 2.86 (0.85) |
| | | | −4.27 (−1.27) | 1.93 (0.57) |
| | | | −4.48 (−1.33) | 1.00 (0.30) |

The frame meets the keel at the base line, 4.61 ft below the water at ⊕; the keel's lower edge
is 5.48 ft below. The floor rises steeply and the bilge is round and full (judgement on the
figures). The frame head stands at 4.74 ft against the rail's 4.79 in the profile.

### 4.8 Ports and the rest (read)

- **No gun ports** are drawn on No. 3's side, and no guns.
- **The channel**, from 0.5 to 5.6 ft before the middle, just under the second band, carries
  **three deadeyes a side** with their chain plates, at 2.0, 3.5 and 5.1 ft before the middle
  (measured).
- **A tall post**, drawn dashed, stands at 12.9 ft before the middle (3.84 m), 1.15 ft wide at
  the deck and tapering to 0.6 ft at its foot, from 7.54 ft above the water (1.7 ft above the
  rail there, its head notched) down to 3.2 ft below it, near the floor (measured). Whether it
  is the mast's stump or the bitts is not read; with the chains 8 to 11 ft abaft it, the bitts
  is the likelier (judgement). No mast or spar is otherwise drawn on No. 3.
- **A tapered post**, dashed and solid, about 4 ft abaft the middle, from the deck down to the
  top of a box low in the hold amidships (the box from about 7 ft abaft to 5 ft before the
  middle, its top about 1.2 ft below the water): not identified (a pump and the well are
  possible; judgement).

## 5. For the profile (B8): the points in metres

At the plate's own size (39.12 Sw ft between the perpendiculars, 11.61 m), unscaled: the file
is a larger vessel (§6), and how the plate is carried to her is B8's judgement. `x` forward of
the mid-perpendiculars along the keel, `z` above the LWL square to the keel (the units
paragraph above §0). Measured unless marked.

- **`rail_m`**: [−6.32, 1.66], [−6.19, 1.64], [−5.81, 1.59], [−5.44, 1.55], [−5.00, 1.50],
  [−4.10, 1.43], [−2.74, 1.36], [−1.36, 1.33], [0.01, 1.36], [1.29, 1.42], [2.58, 1.55],
  [3.95, 1.75], [4.85, 1.94], [5.18, 2.03], [5.43, 2.10], [5.60, 2.15].
- **`breadth_m`** [x, at the water, at the rail]: [−5.00, 0.96, 1.28], [−4.10, 1.46, 1.47],
  [−2.74, 1.78, 1.69], [−1.36, 1.95, 1.84], [0.01, 1.98, 1.90], [1.29, 2.00, 1.91],
  [2.57, 1.98, 1.88], [3.94, 1.59, 1.69], [4.85, 0.80, 1.28]. The rail's half-breadth at the
  transom 0.78 (§4.6); the water line closes to the rabbets about 5.4 m from the middle at each
  end.
- **`keel_m`**: [−5.46, −1.94], [5.19, −1.45].
- **`stem_m`**, the fore edge, low to high: [5.19, −1.45], [5.28, −1.35], [5.47, −1.05],
  [5.57, −0.79], [5.64, −0.53], [5.69, −0.27], [5.72, 0.00], [5.75, 0.24], [5.77, 0.50],
  [5.79, 0.88], [5.79, 1.40], [5.79, 2.04], [5.78, 2.58] (the stem head's fore top).
- **`stern_m`**, low to high: [−5.46, −1.94], [−5.52, −1.50], [−5.59, −0.99], [−5.66, −0.48],
  [−5.73, 0.00], [−5.82, 0.73] (the counter at the post), [−6.19, 0.87], [−6.33, 0.98] (the
  transom's foot), [−6.66, 1.94] (the taffrail at the middle line).
- **`wales_m`** [x, lower, upper]: [−5.45, 0.30, 0.57], [−5.00, 0.28, 0.53], [−4.10, 0.21, 0.45],
  [−2.74, 0.14, 0.39], [−1.36, 0.12, 0.37], [0.01, 0.14, 0.40], [1.29, 0.21, 0.47],
  [2.57, 0.32, 0.59], [3.94, 0.52, 0.79], [4.85, 0.71, 0.98], [5.48, 0.89, 1.15].
- **`section_m`** [z, half-breadth], moulded; with the plank, add its thickness (not drawn;
  judgement about 1¼ in, 0.03 m): [1.41, 1.92], [1.26, 1.95], [1.17, 1.97], [1.07, 1.99],
  [0.97, 2.01], [0.88, 2.02], [0.78, 2.02], [0.69, 2.03], [0.59, 2.03], [0.00, 2.03],
  [−0.18, 2.02], [−0.28, 2.01], [−0.37, 1.99], [−0.47, 1.96], [−0.56, 1.92], [−0.69, 1.85],
  [−0.75, 1.80], [−0.82, 1.75], [−0.88, 1.67], [−0.95, 1.58], [−1.01, 1.45], [−1.08, 1.30],
  [−1.14, 1.10], [−1.20, 0.85], [−1.27, 0.57], [−1.33, 0.30].
- **`decks_m`**, the deck at side, in two pieces with the waist between not drawn (§4.4): the
  after deck [−6.03, 0.78], [−5.79, 0.78], [−5.41, 0.77], [−5.00, 0.76], [−4.79, 0.75],
  [−4.30, 0.74], [−4.23, 0.74]; the fore deck [−1.78, 0.91], [−1.36, 0.91], [−0.91, 0.92],
  [−0.17, 0.94], [0.01, 0.94], [1.29, 1.00], [1.94, 1.05], [2.57, 1.10], [3.43, 1.19],
  [3.94, 1.26], [4.37, 1.31], [4.85, 1.39], [5.30, 1.47]. Whether the two are one `upper` deck
  with a step, or the waist is open, is judgement.
- **`ports_m`, `port_size_m`**: none drawn.

## 6. Against `data/ships/smack.yaml` (recorded, not moved)

| Field | The file (its note) | The plate (at its own size) |
|---|---|---|
| `length_waterline_m` | 12.2 (40 ft, judgement between the *Culloden*'s keel and gun deck) | 11.46 m (37.6 English ft) on the LWL; 11.61 m between the perpendiculars |
| `beam_m` | 4.3 (14 ft, Charnock) | 4.06 m moulded (13.3 English ft) |
| `draught_m` | 1.9 (6.25 ft mean; 7.0 aft, 5.5 forward, judgement; the note gives Chapman's draught as 6.3 ft) | 1.69 m mean; 1.95 m aft, 1.43 m forward (5.5, 6.4 and 4.7 English ft) |
| `deck_height_m` | 0.75 (2 ft 6 in, judgement) | the after deck 0.74 to 0.78 m at side; the fore deck 0.91 to 0.94 m amidships, 1.00 m at ⊕ |
| The rail above the water | — | 1.33 m at its lowest, 1.66 m at the transom, 2.15 m at the stem |
| `main.shrouds` | 3 shrouds a side (judgement) | three deadeyes a side (§4.8) |

The plate's vessel is about 5 to 6% shorter and narrower than the file's, and draws 11% less
at the mean. These are for the lead and the owner. Stage 0 moves no figure.

## 7. What the source cannot give

- **Port sills and port sizes**: no ports and no guns on No. 3.
- **The deck in the waist**, from 14.3 to 6.0 ft abaft the middle: no deck line is drawn
  there, and the dashed outline over it is not identified (§4.4).
- **The plank**: every line is moulded; the outside of the plank is not drawn.
- **The mast and spars of No. 3**: none drawn, unless the dashed post of §4.8 is the mast's
  stump; the channel and its three deadeyes are the only rigging.
- **The stated dimensions' own text**: the 1768 explanation was not seen; the three figures are
  those read from the 1971 edition (`VesselReferences-2026-10.md:315`). That the 6½ is the
  after draught is judgement on the measure (§2.3); the mean is 5.68.
- **A square plate**: the sheet reads 3% short up the page (§2.2); the factor rests on three
  stations of one breadth and on the stated draught.
- **The vessel's own name or a dated ship**: the figure is a type, as the record says.

## 8. Method and files

The image was read with crops and enlargements, and measured by scripts kept outside the
repository in the session's scratch directory, under `stage0/pages/`: `chapman_fetch.py`
(the fetch), `chapman_crop.py` (crops with a pixel grid), `chapman_ticks.py` (the bar's
divisions), `chapman_col.py` and `chapman_rows.py` (the lines crossed by a column or a row,
to sub-pixel by darkness centroids), `chapman_trace.py` (a line followed across the plate),
`chapman_reduce.py` (the frame, the fits and the reduction to feet), `chapman_tables.py` (the
tables above) and `chapman_overlay.py` (the readings drawn back on the image, checked by eye).
Each takes the cached image's path as its argument or holds the readings it reduces.
