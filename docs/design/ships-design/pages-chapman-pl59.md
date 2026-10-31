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
- **arithmetic**: computed from read or measured figures by a scratch script (§8); the method
  is stated.
- **judgement**: reasoning by this note.

**Read again, 2026-10-30, for the hull step** (`Build-Ships.md` §5.1, §5.4, §5.7): this note
was checked against its images and completed where those sections still wanted a figure. No new
source is named. A figure changed stands with the old one beside it (§5.0 principle 12 of that
design). What was added: the sheets against each other (§2.5), how the load line was judged
(§3), the water lines (§4.9), the frames by station (§4.10), the height of the main breadth
(§4.11), the keel and the rabbet (§4.12), the diagonals (§4.13), the stern (§4.14), the masts
(§4.15), the ports, galleries, lights and head (§4.16) and the points for the shape keys and for
the file (§5.1 to §5.3).

**Checked and built, 2026-10-30.** An independent reading of the three photographs found the note
sound, with a few real faults; those are mended here, the old figure beside the new. The file is
built from these points by `tools/ships/hull_smack.py` (`Build-Ships.md` §5.3); §5.3 here is what
the module makes. Four things the builder added, marked where they stand: the second band's ends
(§4.2), the plan's rail line on to the head and the head's half-siding (§4.6), the rail's stop
(§4.5, §5.3), and the word on the transom (§5.3).

**Reviewed, 2026-10-30.** Her outlines laid over the plate by this note's frames (§8) showed the
sheer, the stem, the post, the counter, the wale, the deck and the head on the plate's lines to the
eye at three times its size, and four faults, mended here, the old figure beside the new: the plan's
water and rail between stations (§4.6), the water's closure on the post (§4.6), the wale's after end
(§4.2), and §5.7's body, which drew the side above the water by the rule where the plate's frames
read it (§5.3). The review also found the sloop's timbers ending on a flat foot (§5.2), which was for
the lead's ruling and was not mended.

**Ruled, 2026-10-31.** The lead took the plate's own frames, sourced points over the rule: the file
draws them, `Build-Ships.md` §5.7's row says so, and the sloop stays beside them as a check (§5.2,
§5.3).

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
  (1.69 m), to the keel's lower edge at the perpendiculars; 1.76 ft of drag. The stated 6½ fits
  the after draught (judgement: the text names no place; §3, §7).
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
- **Against the file** (§6, recorded, not moved): the file's deck at 0.75 m matches this plate's
  after deck in figure (0.74 to 0.78 m, judgement); at midships the plate's deck stands 0.94 m, 1.00
  m drawn at her beam, 0.25 m above the file's datum. The file's 12.2 m waterline, 4.3 m beam and
  1.9 m mean draught stand against the plate's 11.46 m, 4.06 m and 1.69 m.
- **The body plan reads whole.** All nine frames were followed by their darkness ridges, so
  the plate gives her sections by station, not the midship section alone (§4.10). They meet the
  half-breadth plan's three water lines within a mean of 0.02 ft and an rms of 0.05 ft, and
  the second photograph's frames within an rms of 0.03 ft (§2.5).
- **Corrected** (§4.5, §4.6, §2.2): the load water line's half-breadth at stations 3 and ⊕ was
  read on the line below it, 6.67 and 6.73 ft for 6.78 and 6.85; station H's row read 0.1 ft wide
  beside its own station line; the counter at the post stands at 2.29 ft, not 2.46; and the
  second photograph does not give the 0.970. Corrected again on the check (§2.5, §4.2): frame H
  stands at x 16.47, not 16.60, its station line at 16.38, not 16.32, and the wale's fore end at x
  18.89, not 18.47.
- **The load line** is the top water line of three, the only one carried across the post and
  the stem and the one the stated draught fits; no word on the plate names it (§3). The other two
  lie 1.17 and 2.33 ft (0.35 and 0.69 m) below it, parallel (§4.9).
- **The stern** is raked and rounded above a short rounded counter, with no lights and no
  galleries: 2.64 ft (0.78 m) half-breadth at the rail's end, read on both plans, and 3.12 ft
  (0.93 m) at the transom's foot (§4.14). **No head**: the stem stands up squared, with no knee
  (§4.16).
- **No port triple** can be written: no port and no gun is drawn (§4.16). **No mast** is drawn;
  the chains put the mast about 1.6 to 2.1 m before the middle, and the file's +1.8 m falls there
  (§4.15).
- **Ruled (the lead, 2026-10-31): the plate's own frames under the water, sourced points over the
  rule.** Steel's coasting sloop, scaled as §5.7 of the design first had it, runs a mean of 0.47 m
  fuller under the water than the plate's own frames, at the same rung; drawn beside the plate's
  midship section it steps by 1.2 m in half-breadth within 3 cm of length; and its timbers end on a
  flat foot about a metre out from the middle line, on the plate's keel (§5.2). The sloop is kept as
  a check, one word away in the module (§5.2, §5.3).
- **Carried to the file** (§5.3): every key passes `g.hull_profile`, `g.hull_form` and
  `form.check`. Drawn, she is **38 t against the filed 46 t (−18%), past the line of `Build-Ships.md`
  §5.0 principle 8: reported, not moved**; on §5.7 as first written she drew 53 t (+15%).

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
  and a heavy curve running down from the ends to the floor amidships (first taken as Chapman's
  rising line; it is the body plan's diagonal drawn in the profile, §4.13). Two **dashed perpendiculars** run from above the rail to below the keel: the
  after one touches the after side of the post where it meets the counter, the fore one the fore
  side of the stem above the water, where the stem stands square to the keel. A dashed base line
  runs between them along the top of the keel.
- **The stations**: every third frame is drawn and lettered under the keel, 14, 12, 9, 6, 3
  abaft the midship frame ⊕ and C, F, H before it, 1.54 ft a frame (measured: 220.5 px for
  three). ⊕ is drawn as two lines 0.63 ft apart (first written 0.59) with the sign between them;
  its `x` is taken at their middle, 4.34 ±0.03. The mid-perpendiculars fall on station 3 (+0.02 ft).
- **The half-breadth plan**, under the profile on the same stations, its centre line at the
  bottom: the side's lines and the water lines, the station lines rising from the centre line
  to the outermost line.
- **The body plan**, above the profile, the after body to the left and the fore body to the
  right of a centre line, inside a dashed rectangle whose sides are the moulded breadth; the
  three water lines drawn across the frames as curves, the LWL heavy (read), rising aft and falling
  forward because the LWL lies 2.58° to the keel, and carried on outside each side as a long mark;
  diagonals lettered with the stations.
- **The scale bar** for No. 3 (bar B), between the body plans of No. 2 and No. 3, with three
  rows lettered S, E and F (Swedish, English and French feet), each with a first foot divided
  in quarters. A second bar (bar A), under No. 1's body plan, and a third beside No. 2's figure are
  not No. 3's (§2.1).

## 2. The scale and its check

### 2.1 The bar (measured)

| Row | Px a foot (fit over the divisions) | rms | In the true ratio of the feet |
|---|---|---|---|
| S, 0 to 10 ft | 47.80 (end to end 47.82) | 0.5 px | — |
| E, 0 to 10 ft (first fitted on 0 to 6, 49.43) | 49.34 | 0.5 px | S/E 0.970 against 0.974 |
| F, 0 to 10 ft (first fitted on 0 to 7, 52.42) | 52.34 | 0.4 px | S/F 0.914 against 0.914 |

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

So lengths up the page read 3% short against lengths along it. Every height and every
half-breadth from the half-breadth plan is taken at 47.82 × 0.970 = 46.39 px a foot; lengths
along the page at 47.82. Unscaled, the heights would be 3% lower: the after draught 6.36 ft
instead of 6.56.

**Corrected, 2026-10-30.** This section first said that the second colour image gives the same
0.970 at ⊕ (475.4 px against 490 px across the body plan), and so that the 3% lies on the sheet
and not in one photograph. That 475.4 px runs to the plan's second line, the second water line
of §4.9. To the main breadth it is 485.6 px, 0.992 (measured). That photograph's own ratio runs
from about 0.98 in its body plan (first written 0.970) to about 0.99 in its profile and its plan,
so it is distorted in its own way and cannot say whether the 3% is the paper's or the measured
photograph's (judgement). The factor rests on the measured image: the three stations above, the
stated draught if the 6½ is the after draught (§2.3; judgement) and the frames of the body plan
meeting the plan's water lines at the heights it gives (§2.5); and on the second photograph, whose
heights at its own bar, with no factor, meet §4.2's within an rms of 0.02 ft (36 points).

### 2.3 The stated dimensions measured back (measured)

| Dimension | Stated (`VesselReferences-2026-10.md:315`) | Measured | Difference |
|---|---|---|---|
| Between the perpendiculars | 39¼ Sw ft | 1870.5 px = 39.12 ft (11.61 m; 38.1 English ft) | −0.3% |
| Breadth moulded | 13⅔ | the body plan's dashed sides, 654.1 px = 13.68 ft (4.06 m; 13.3 English ft); the ⊕ frame lies on them from 2.3 ft above the water to 0.6 ft below it | +0.1% |
| Draught | 6½ | 6.56 ft at the after perpendicular to the keel's lower edge (1.95 m; 6.4 English ft), if the 6½ is the after draught (judgement) | +0.9% |

The length and the breadth check the scale along the page; the draught checks the factor of
§2.2, if the 6½ is the after draught (judgement: the text names no place; §3). With the breadth on the dashed sides and the frame on them, the stated breadth is the
moulded one, as read; the plank is not drawn.

### 2.4 The other images (measured)

- `022uK3KjAwHr` reads 35.00 px a foot on its bar; on it the length comes to 39.63 ft and the
  body plan's breadth to 14.0 ft, 1.3 and 2.3% long, so its bar and its figure do not agree as
  well as on the measured image. Its vertical ratio changes across the sheet (§2.2). Used as the
  checker of §2.5, by its own figure: its dashed sides, 489.5 px, taken as 13.68 ft.
- `022uK3KjAwHs` reads 36.40 px a foot; the length 38.87 ft, but the heights (keel to rail,
  keel to LWL, the half-breadth plan) 8.7 to 9.3% longer than the measured image's against the
  same bar, 5 to 6% longer than §2.2 allows. A distorted copy (judgement); not measured.

### 2.5 The sheets against each other (2026-10-30)

**Within the plate** (measured; the frames as §4.10 reduces them):

| Check | Compared | Result |
|---|---|---|
| The body plan against the half-breadth plan | each frame's half-breadth at the three water lines' heights (§4.9) against the plan's lines (§4.9), stations 14 to F, 24 points | mean −0.02 ft, rms 0.05 ft, largest 0.13 ft |
| The same at H | as above, 3 points | −0.18, −0.09, −0.06 ft: frame H stands about 0.1 ft forward of its station line (below; first written 0.3 ft) |
| The body plan's greatest half-breadth against the plan's main breadth | nine stations | within 0.02 ft |
| The frames' heads against the profile's rail and the plan's rail line | nine stations | within 0.10 ft in height (after body 0.03 to 0.10 low, fore body within 0.03) and 0.05 ft in breadth. First written within 0.08 ft and 0.06 ft but for C (−0.13) and H (+0.21, −0.14 in breadth): those heads were misread (§4.10) |
| Each frame crossed with the water-line curves in the body plan (§1.2) | heights above the base against the profile, 21 readings leaving ⊕ out, which runs parallel there; half-breadths against the plan | heights within 0.04 ft; half-breadths within 0.06 ft, but H's LWL at −0.13 ft, H standing forward of its line. The WL2 and WL3 ticks stand 158 and 105.4 px above the base against 159.4 and 105.7 from the profile, the LWL mark 2.8 px high: the base line's registration, shown directly |
| The body plan's LWL mark against the profile | at ⊕, each measured from the base line | the mark 3.4 px (0.07 ft) high |
| The plan's heavy lines against the body plan's diagonals | the length down the diagonal at each frame, ten points | within 0.11 ft (§4.13) |
| The profile's heavy curve against the same | the height where each frame crosses its diagonal | within 0.11 ft (§4.13) |

Since the LWL mark stands 0.07 ft high against the profile, the frames are registered by the base
line: a frame's height above the base, less the LWL's height above the base at that station in
the profile (4.60 ft at ⊕, rising 0.045 ft for each foot aft). Registered by the mark instead, the
same 24 points read a mean of +0.05 ft, largest 0.15 ft. Frame H: its head, its main breadth and
its water lines all fit the plan's lines at x 16.42 to 16.59, mean 16.47, against 16.38 for its
station line in the profile and 16.39 in the plan, so §4.10 stands it at 16.47 (judgement).
Corrected, 2026-10-30: first 16.6 against 16.32 and 16.37, on misread heads and on the top of that
line read in a frame turned only by the keel's tilt; the lean all the stations share is 0.0095 px a
px.

The first reading's "rms" figures in this section and in §5.2 were printed as standard deviations
(`stats.py`, `img2e.py`, `steel_cmp.py`). Where the mean is small, as here, the two agree within 0.004
ft and nothing moves; §5.2's, where the mean is large, is corrected there.

**The second photograph against the first** (measured; checker on `022uK3KjAwHr`, read by its own
figure: `img2c.py`, `img2f.py`, §8):

- Its ten frames at twelve heights each, 119 points, each frame's half-breadth from the first
  photograph looked for on the second's row: mean 0.006 ft, rms 0.032 ft, largest 0.15 ft.
- Checked again by an independent route: 340 frame points at an rms of 0.024 ft, its plan's lines 45
  points at 0.021 ft, its rail, wale and keel 36 points at its own bar at 0.021 ft (measured).
- At ⊕ its half-breadth plan shows the same lines in the same order, measured from the keel's
  lower edge in the profile above them: +2.0, +6.7, +17.3, +25.8 and +64.8 px, against +3.1,
  +7.0, +17.4, +25.9 and +64.2 px from the first photograph at its scale. So the lines of §4.9
  are on the sheet in both. Its plan's half-breadths read about 2% long against the first's (§2.2).

**The Steel table against its page** (read): `pages-steel-1805-bodies.md` §3.3 was laid against
leaf n485 cell by cell, and Folio I's and Folio LI's sloop columns against leaves n488 and n588:
all agree, the probable misprint of timber 4's third diagonal among them (printed 7 ft 4¼ in).
Two rows that note leaves out, kept here in case `floor_m` is ruled from the sloop: the rising line, ⊕ to G 0 5, 0 6½, 0 11, 1 11, 2 9½,
4 3½ and timbers 2 to 13 0 7¾, 0 11½, 1 6, 2 6, 3 11½, 6 0, 7 7; the cutting down line, ⊕ to E
0 10, 0 10¼, 1 0¼, 1 6 and timbers 2 to 12 0 10¼, 0 11½, 1 1¾, 1 6, 2 2, 3 8 (read). Its checks are
its own §6; a table has no drawn scale.

**The plate against Steel's sloop** (arithmetic; Steel's figures as `pages-steel-1805-bodies.md`
§4, §5 give them, the sloop's water length taken as Folio I's row C, 52 ft 0 in, judgement):

| | The plate | Steel's sloop | The file |
|---|---|---|---|
| Length on the water / breadth moulded | 38.58 / 13.68 = 2.82 | 52 0 / 16 4 = 3.18 | 12.2 / 4.3 = 2.84 |
| Mean draught / breadth | 5.68 / 13.68 = 0.42 | 8 0 / 16 4 = 0.49 | 1.9 / 4.3 = 0.44 |
| Drag / length | 1.76 / 39.12 = 0.045 | 2 0 / 50 3 = 0.040 | 1.5 ft / 40 ft = 0.038 |
| Rabbet below the water at the greatest section / its half-breadth | 4.62 / 6.85 = 0.67 | 7 4½ / 8 3 = 0.89 | |
| Rail above the water at its lowest / breadth | 4.49 / 13.68 = 0.33 | 3 3 / 16 4 = 0.20 | |
| The wale's lower edge at the greatest section | 0.70 ft above the water | 1 ft 5 in below it | |
| The stern's half-breadth at the rail / breadth | 2.64 / 13.68 = 0.19 | 5 0 / 16 4 = 0.31 | |

They are one type in name and two vessels in form (judgement): for her breadth the plate's is
shorter and shallower than Steel's, higher in the side and narrower in the stern, and the file's
proportions sit on the plate's. Steel's load line is itself judged (that note's §5.1).

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

**How it was judged the load line** (judgement, 2026-10-30). No word on the plate names it (read).
Four things say so:

1. It is the top one of the three water lines (§4.9), and Steel defines the load water line as
   the highest (the Indefatigable's research note, §2.3.1, read there).
2. It alone runs on across the post to the rudder's after edge and across the stem to its fore
   edge, it alone is carried outside the body plan as a long line, and it alone is heavy across the
   body plan; the other two stop at the rabbets, and their curves end on the dashed sides at ⊕
   (read; corrected 2026-10-30: first written as short ticks outside the sides). The Indefatigable's
   64 marks her WL1 the same way (same place).
3. Of the water lines it alone is drawn heavy in the half-breadth plan towards both ends (read;
   between them §4.6 has it one light line with the main breadth), and the frames meet it there at
   its height in the profile (§2.5).
4. The stated draught, 6½ ft, fits it at the after perpendicular at +0.9% (§2.3), and the wale's
   lower edge stands a few inches above it amidships, as Steel's rule puts it (§4.1).

That the 6½ is the after draught is itself judgement: the text names no place. Its grounds are 6.55
ft aft against 5.68 at the mean, the fit at +0.9%, and the heights of the second photograph at its
own bar agreeing with no factor (§2.2).

So it stands for her laden line as far as a type's plate can. The file's waterline is taken as this
line, as `Build-Ships.md` §5.1 has it: every `z` here is above it.

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
| H | 16.38 (4.86), first 16.32 (§2.5) | 6.54 (1.94) | 5.84 (1.73) | 5.58 (1.66) | 4.87 (1.45) | 4.68 (1.39) | 3.29 (0.98) | 2.40 (0.71) | −4.94 (−1.47) |

The wale's ends: aft, at the post's scroll, x −18.34, lower 1.02, upper 1.93 (−5.45 m, 0.30,
0.57), where its heavy lower edge stops; its light upper line runs on aft, 1.96 at −18.59, 1.99 at
−18.84, to end on the curve that carries the counter along the side, at x −19.18, 2.03 (−5.69 m,
0.60), and that curve is the band's after end, from there down to the scroll: 1.94 at −19.09, 1.73 at
−18.83, 1.53 at −18.62 (measured, the review, 2026-10-30, ±0.05 ft; first written as the band
stopping at −18.34). `wales_m` takes the upper line's end as one point, −19.18, lower 2.00, upper
2.03, since the viewer draws a band straight between stations and the curve is nearly straight.
Forward, cut square at the stem, x 18.89, lower 3.11, upper 4.04 (5.61 m, 0.92, 1.20)
(measured; corrected 2026-10-30: first read x 18.47, lower 2.99, upper 3.87, on the lines 20 px
short of their end).

The second band's ends (measured, the builder, 2026-10-30; ±0.05 ft): it runs parallel to the rail
end to end (§4.1). Aft it stops on the side's after edge at x −20.96, foot 4.57, top 4.83 (−6.22 m,
1.36, 1.43); forward beside the rail's end at x 18.86, foot 6.28, top 6.54 (5.60 m, 1.86, 1.94).

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
  0.33 ft above the counter at the post (corrected: §4.5; first written 0.16 ft).
- **No deck line** is drawn from −14.26 to −6.00 ft. Over that length a double dashed outline
  stands from about 0.3 ft above the rail to about 0.9 ft below the water line, its upper and
  lower sides roughly parallel to the rail and the water line (read; measured at two
  stations). Not identified (judgement: a well's trunk, an open hold with its coaming, or
  washboards are all possible; none is read).
- **The fore deck**, from −6.00 ft to the stem, at side: −6.00: 3.05; −4.58: 3.07; −3.07: 3.10;
  −0.56: 3.16; 0.02: 3.17; 4.34: 3.38; 6.55: 3.54; 8.65: 3.72; 11.57: 4.02; 13.27: 4.23; 14.71:
  4.42; 16.38 (first 16.32): 4.68; 17.85: 4.96 (−1.78 m, 0.91 to 5.30 m, 1.47). At its after end it stands
  0.57 ft above the after deck's fore end.
- **Their ends and what stands under them** (read; measured 2026-10-30). Six small dashed squares
  hang under the deck lines, about 0.6 ft fore and aft and 0.5 ft deep: at −19.1 to −18.5,
  −14.3 to −13.7, −6.3 to −5.7, −4.0 to −3.5, 5.6 to 6.3 and 13.3 to 13.7 ft. They are taken as
  beam ends (judgement). The second and the third stand at the deck lines' two ends in the waist.
  A second dashed outline, like the first, stands from 7.2 to 12.4 ft before the middle, from the
  fore deck down to 1.3 ft below the water; it is not identified either (judgement).

### 4.5 The ends (measured)

**The stem's fore edge**, low to high, `x`, `z` in ft (m): the forefoot, where the keel's lower
edge ends, 17.49, −4.88 (5.19, −1.45); 17.77, −4.53; 18.41, −3.54; 18.75, −2.66; 18.98, −1.79;
19.15, −0.92; 19.27, 0.00 at the water; 19.36, 0.81; 19.43, 1.68; 19.49, 2.97; 19.51, 4.70;
19.50, 6.85 (5.79, 2.04). Above about 3 ft the stem stands square to the keel on the fore
perpendicular.

**The stem head** rises 1.4 ft above the rail's end: its top slopes from 8.31 ft at its after
edge (x 18.17; read again 8.26 at 18.13) to **8.68 ft at its fore edge** (x 19.47; 5.78 m, 2.58 m;
read again 8.70 at 19.50). Its after edge stands plumb from the rail at about x 18.15. The rail
carries on past that edge to x 18.86, on the head's side (judgement; §4.6).

**The stern**, low to high: the post's after edge from its heel, −18.39, −6.52 (−5.46, −1.94),
through −18.60, −5.05; −18.84, −3.33; −19.08, −1.62; to the water at −19.31, 0.00
(−5.73, 0.00); the counter meets the post at −19.59, 2.29 (−5.82, 0.68), on the after
perpendicular (corrected 2026-10-30: first read 2.46, 0.73, 8 px above the line, which at that
column is at 2737.9 px); the counter runs aft to the transom's foot at −20.89, 2.91 (−6.20, 0.86)
and −21.30, 3.27 (−6.32, 0.97; first read −20.84, 2.92 and −21.32, 3.29); the transom, raked aft
and rounded, rises to **the taffrail at the middle line, −22.44, 6.54** (−6.66 m, 1.94 m). The
rail meets the transom's side at −21.29, 5.60, so the taffrail stands 0.94 ft above the rail's
after end. The post rakes about 8° from square to the keel (measured: 0.14 ft aft in each foot of
height). That line is the middle of a band of three to five close lines, about 7 px (0.15 ft)
broad, the rudder's fore edge and the post's after edge together (read; judgement on what they
are). §4.14 gives the stern's lines, re-read.

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
| 14 | −16.85 (−5.00) | 4.59 (1.36) | 4.31 (1.28) | 3.27 (0.97) |
| 12 | −13.81 (−4.10) | 5.37 (1.59) | 4.98 (1.48) | 4.92 (1.46) |
| 9 | −9.22 (−2.74) | 6.13 (1.82) | 5.72 (1.70) | 5.99 (1.78) |
| 6 | −4.58 (−1.36) | 6.56 (1.95) | 6.18 (1.83) | 6.56 (1.95) |
| 3 | 0.02 (0.01) | 6.78 (2.01) | 6.39 (1.90) | 6.78 (2.01) |
| ⊕ | 4.34 (1.29) | 6.85 (2.03) | 6.43 (1.91) | 6.85 (2.03) |
| C | 8.65 (2.57) | 6.72 (2.00) | 6.31 (1.87) | 6.66 (1.98) |
| F | 13.27 (3.94) | 6.05 (1.80) | 5.68 (1.69) | 5.34 (1.59) |
| H | 16.38 (4.86), first 16.32 | 4.41 (1.31) | 4.22 (1.25) | 2.54 (0.75) |

- **Corrected, 2026-10-30** (measured; read beside each station's own line in the plan, which
  leans about 0.5° on the image and stands 2 to 6 px forward of its place in the profile):
  - The load water line at 3 and ⊕ was first read as 6.67 (1.98) and 6.73 (2.00). Those two lines
    are the second water line of §4.9. From about 1540 to 1920 px one light line is drawn: the load
    water line cannot be told from the main breadth there (read). Its half-breadth at 3 and ⊕ is taken
    as that line's, 6.78 and 6.85 (judgement), supported by the frames at the water (6.78, 6.83,
    §4.10). This was first written as the heavy line lying on the main breadth within a pixel from
    about 1420 to 1950 px; on the check the top line is heavy only outside that stretch.
  - Station H was first read as 4.52 (1.34), 4.33 (1.28) and 2.69 (0.80), at 6 px abaft its line
    where the lines run steeply.
  - Station 14's water line was 3.24 (0.96), and the others moved by 0.02 ft or less.
- **The lines beyond the stations** (measured), `x`, main breadth, rail, the LWL: −17.97
  (−5.34): 4.24, 4.00, 1.36; −17.55 (−5.21): 4.38, 4.12, 2.40; −17.13 (−5.09): 4.52, 4.24, 3.00;
  16.96 (5.04): 3.88, 3.74, 1.85; 17.37 (5.16): 3.32, 3.32, 1.31; 17.79 (5.28): 2.67, 2.67, 0.87;
  18.21 (5.41): 1.82, 1.82, 0.45. Forward of about 17.4 the main breadth and the rail lie as one.
  Abaft the water's end, main breadth and rail: −18.38: 4.10, 3.87; −19.22: 3.78, 3.60; −19.58,
  the after perpendicular: 3.64, 3.48; −20.06: 3.44, 3.30; −20.68: 3.16, 3.07; −21.31: 2.84 as one.
- **The water's closure on the post** (measured, the review, 2026-10-30, ±0.05 ft, the line running
  steeply; the rail beside each): −18.10: 0.92; −18.20: 0.56, 3.93; −18.30: 0.38; −18.40: 0.26, 3.87;
  −18.50: 0.14, then the post's half-siding, about 0.23 (§4.12). So the water line closes at about
  −18.4, and `breadth_m` was first ended at −17.97, 1.36, which drew it straight on to the post's
  after edge at −19.31 and so 0.20 m too wide at the rabbet (0.29 against 0.08 m at her size).
- **The lines between the stations** (measured, the review, 2026-10-30, ±0.03 ft). The run and the
  entry curve, so a straight line from station to station stands inside the plan: the water by up to
  0.24 ft between 14 and 12, 0.22 ft between C and F and 0.29 ft between F and H, 0.09 m at her size,
  which is 3 px on the owner's picture. Three more columns take that to 0.09 ft or less, each read
  again on the second photograph by its own figure, in brackets: `x`, main breadth, rail, the LWL:
  −15.40: 5.00 (4.99), 4.67 (4.66), 4.30 (4.28); 11.50: 6.45 (6.44), and the rail and the LWL lying as
  one, 6.07 (6.07); 14.70: 5.51 (5.52), 5.20 (5.21), 4.33 (4.36). Only at 14.70 does the main breadth
  stand off its straight by more than 2 px (0.20 ft), so only there does `breadth_line_m` take a point.
- **The rail on to the head** (measured, the builder, 2026-10-30, ±0.03 ft; the plan's columns
  beside its stations): `x`, the rail, the water: 18.09: 2.08, 0.57; 18.20: 1.85, 0.47; 18.30: 1.59,
  0.35; 18.41: 1.30, 0.26; 18.51: 0.98; 18.62: 0.63; 18.72: 0.29; 18.83: 0.31; 18.93: 0.32. So the
  rail closes on the stem head's side about x 18.72, and **the head's half-siding is 0.30 ft** (0.09
  m), as the body plan's strip beside its centre line reads it, 0.28 ft. The head above the rail is
  that narrow, not as wide as the rail at its after edge (read; §5.3).
- **The transom**: the main breadth and rail lines meet it at 2.64 ft (0.78 m) half-breadth,
  at x −21.9 in the plan, against −21.3 for the rail's after end in the profile; the body plan's
  rail ends at 2.64 ft too (§4.14), and the corner in the plan falls on the transom's corner line
  in the profile (§4.14), so the two `x` differ because the rail's moulding stops short of it
  (judgement; ±0.7 ft in `x` there).
- **The identification**: the lines cross near the stern and near station 12, where the rail
  line and the water line come within 0.03 ft; they were followed through the crossings by
  their ends and their weight. Elsewhere ±0.03 ft in reading. The rail's half-breadth at ⊕
  agrees with the body plan's frame head (6.47 ft, §4.7) within 0.04 ft, and the main breadth
  with the body plan at every station within 0.02 ft (§2.5).
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

These heights are above the LWL mark of the body plan. Registered by the base line (§2.5), each
stands 0.06 ft higher; §4.10 and §5 carry them so.

### 4.8 Ports and the rest (read)

- **No gun ports** are drawn on No. 3's side, and no guns (§4.16).
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
- **The box** is taken as the well, by the figure's own name in the record, a *sump* or well-boat
  (§1.1), and by No. 1's perforated well in the same place on the plate (judgement, 2026-10-30).
  A second tapered post leans in to it, about 1.1 to 1.5 ft before the middle at the deck and 1.9
  to 2.2 ft at the box, so the two may be its trunks, not pumps (judgement). The half-breadth plan draws two
  rectangles on the middle line low in the same place, about ±1.7 and ±2.1 ft (measured; §5.1 of
  the design has no key for it).

### 4.9 The water lines (measured, 2026-10-30)

**Their heights.** Three water lines are drawn, each straight (read). Below the LWL, parallel to it
within 0.04 ft end to end:

| Line | Below the LWL | Runs from, to (x) | At the body plan's sides |
|---|---|---|---|
| LWL | | −19.31 to 19.27, the rudder's after edge to the stem's fore edge | its heavy curve carried on outside the side as a long mark |
| WL2 | 1.17 ft (0.35 m), each station within 0.02 | −18.4 to about 18.1, rabbet to rabbet | its curve ends on the dashed side at ⊕, inside it |
| WL3 | 2.33 ft (0.69 m), each station within 0.02 | −18.1 to about 17.6, rabbet to rabbet | its curve ends on the dashed side at ⊕, inside it |

(Corrected, 2026-10-30: the last column first read "a long mark" and "a short tick each side at ⊕".
All three are drawn across the frames as curves, §1.2.)

No higher line is drawn, and none between WL3 and the keel (read).

**Their half-breadths**, ft (m), from the half-breadth plan at each station's own line, each ±0.03
ft (±0.05 at H and 14, where the lines run steeply). Moulded. The main breadth and the rail are
§4.6's, for comparison:

| Station | x | LWL | WL2 | WL3 | Main breadth | Rail |
|---|---|---|---|---|---|---|
| 14 | −16.85 (−5.00) | 3.27 (0.97) | 0.75 (0.22) | 0.36 (0.11) | 4.59 (1.36) | 4.31 (1.28) |
| 12 | −13.81 (−4.10) | 4.92 (1.46) | 3.36 (1.00) | 1.29 (0.38) | 5.37 (1.59) | 4.98 (1.48) |
| 9 | −9.22 (−2.74) | 5.99 (1.78) | 5.32 (1.58) | 3.65 (1.08) | 6.13 (1.82) | 5.72 (1.70) |
| 6 | −4.58 (−1.36) | 6.56 (1.95) | 6.18 (1.83) | 5.31 (1.58) | 6.56 (1.95) | 6.18 (1.83) |
| 3 | 0.02 (0.01) | 6.78 (2.01), as the main breadth, judgement | 6.61 (1.96) | 6.04 (1.79), first 5.99 on the diagonal's heavy line | 6.78 (2.01) | 6.39 (1.90) |
| ⊕ | 4.34 (1.29) | 6.85 (2.03), as the main breadth, judgement | 6.73 (2.00) | 6.19 (1.84) | 6.85 (2.03) | 6.43 (1.91) |
| C | 8.65 (2.57) | 6.66 (1.98) | 6.31 (1.87) | 5.42 (1.61) | 6.72 (2.00) | 6.31 (1.87) |
| F | 13.27 (3.94) | 5.34 (1.59) | 4.17 (1.24) | 2.67 (0.79) | 6.05 (1.80) | 5.68 (1.69) |
| H | 16.38 (4.86), first 16.32 | 2.54 (0.75) | 1.52 (0.45) | 0.67 (0.20) | 4.41 (1.31) | 4.22 (1.25) |

The LWL lies on the main breadth line from about station 6 to about 2.5 ft before ⊕, so the main
breadth stands at or a little above the water amidships (§4.11). WL2 lies on the rail line at
stations 6 and C, and WL3 on the diagonal from about 6 to ⊕ (§4.13); those were told apart by their
courses either side.

### 4.10 The frames by station (measured, 2026-10-30)

The body plan draws all nine stations, the after body to the left and the fore body to the right
(read; §1.2), lettered on its two diagonals. Each frame was followed by its darkness ridge, a step
of 4 px along it and a search across it, from the head to the base, and the traces drawn back on
the image and checked by eye (`body.py`, §8). Half-breadths at 47.82 px a foot from the centre
line, which leans 0.65° on the image (fit to the thin line in the body plan; rms 0.2 px); heights
at 46.39 px, registered by the base line (§2.5). Moulded, ft, ±0.03 in the body and ±0.05 where a
frame runs nearly flat. ⊕ is the mean of its two halves, which differ by 0.05 ft. Each height is
above the LWL at that station, so a row of this table is a level water line:

| z | 14 | 12 | 9 | 6 | 3 | ⊕ | C | F | H |
|---|---|---|---|---|---|---|---|---|---|
| x | −16.85 | −13.81 | −9.22 | −4.58 | 0.02 | 4.34 | 8.65 | 13.27 | 16.47 |
| 4.00 (1.19) |  | 5.18 | 5.87 | 6.28 | 6.53 | 6.64 | 6.57 | 5.99 | 4.39 |
| 3.00 (0.89) | 4.57 | 5.31 | 6.04 | 6.46 | 6.70 | 6.79 | 6.68 | 6.05 | 4.27 |
| 2.00 (0.59) | 4.60 | 5.36 | 6.12 | 6.54 | 6.76 | 6.83 | 6.71 | 6.03 | 3.88 |
| 1.00 (0.30) | 4.40 | 5.32 | 6.13 | 6.58 | 6.79 | 6.84 | 6.71 | 5.84 | 3.20 |
| 0.50 (0.15) | 4.05 | 5.17 | 6.08 | 6.56 | 6.79 | 6.84 | 6.69 | 5.63 | 2.79 |
| −0.58 (−0.17) | 1.60 | 4.29 | 5.74 | 6.41 | 6.74 | 6.80 | 6.53 | 4.83 | 1.90 |
| −1.17 (−0.35) | 0.70 | 3.23 | 5.27 | 6.21 | 6.62 | 6.70 | 6.32 | 4.20 | 1.43 |
| −1.74 (−0.52) | 0.52 | 1.93 | 4.60 | 5.86 | 6.41 | 6.52 | 5.97 | 3.51 | 1.02 |
| −2.33 (−0.69) | 0.41 | 1.19 | 3.61 | 5.25 | 6.03 | 6.20 | 5.43 | 2.74 | 0.61 |
| −2.80 (−0.83) | 0.36 | 0.93 | 2.69 | 4.54 | 5.56 | 5.76 | 4.75 | 2.01 | 0.38 |
| −3.20 (−0.95) | 0.31 | 0.75 | 2.02 | 3.74 | 4.94 | 5.18 | 3.92 | 1.43 | 0.22 |
| −3.60 (−1.07) | 0.28 | 0.61 | 1.47 | 2.80 | 4.05 | 4.27 | 2.81 | 0.89 | 0.15 |
| −3.90 (−1.16) | 0.25 | 0.52 | 1.13 | 2.11 | 3.16 | 3.23 | 1.83 | 0.53 |  |
| −4.20 (−1.25) | 0.23 | 0.44 | 0.85 | 1.48 | 2.10 | 1.95 | 0.85 |  |  |
| −4.50 (−1.34) | 0.21 | 0.37 | 0.61 | 0.94 | 1.08 |  |  |  |  |
| −4.80 (−1.43) | 0.19 | 0.30 | 0.40 | 0.48 |  |  |  |  |  |
| −5.10 (−1.51) | 0.18 | 0.24 | 0.22 |  |  |  |  |  |  |
| −5.40 (−1.60) | 0.18 |  |  |  |  |  |  |  |  |

Heights are in ft (m). Frame H is stood at x 16.47 (§2.5; first 16.60). Where a column stops, the
frame has reached the rabbet (§4.12), where each frame's foot is 14: −5.58, 0.21; 12: −5.44, 0.21; 9:
−5.23, 0.23; 6: −5.02, 0.25; 3: −4.82, 0.27; ⊕: −4.62, 0.28; C: −4.42, 0.28; F: −4.19, 0.28. The
frames' heads, the `z` and half-breadth at which each meets the rail line in the body plan: 14:
5.03, 4.32; 12: 4.76, 5.01; 9: 4.48, 5.75; 6: 4.42, 6.17; 3: 4.49, 6.39; ⊕: 4.73, 6.45 (its after
half); C: 5.22, 6.29; F: 5.86, 5.66; H: 6.56, 4.17. Corrected, 2026-10-30: first 14: 5.07, 4.31; 9:
4.49, 5.76; 6: 4.46, 6.17; 3: 4.63, 6.41; ⊕: 4.80, 6.44; C: 5.09, 6.32; F: 5.93, 5.62; H: 6.75, 4.08,
the misread ones among them those of C, H and 3 (zoomed crops and crossings on the rail's curve).

What they show (judgement on the figures): a full round midship body with a short hard bilge,
the floor rising steeply from a sharp keel; a hollow run, the water line at 14 standing out of a
deep narrow deadwood; a sharp hollow entry at H under a flaring bow, whose breadth stands 4.3 ft
above the water there; and tumblehome everywhere above the breadth.

### 4.11 The main breadth's height (measured, 2026-10-30)

The plan gives the main breadth's half-breadth; only the frames give its height. Each frame is
nearly straight there, so the height is the middle of the band within 0.015 ft of its greatest
half-breadth (arithmetic). The band is 0.9 to 2.0 ft deep, so ±0.4 ft in height and next to nothing
in breadth:

| Station | x | z, ft (m) | Half-breadth, ft (m) |
|---|---|---|---|
| 14 | −16.85 | 2.15 (0.64) | 4.59 (1.36) |
| 12 | −13.81 | 1.77 (0.53) | 5.37 (1.59) |
| 9 | −9.22 | 1.38 (0.41) | 6.13 (1.82) |
| 6 | −4.58 | 0.91 (0.27) | 6.56 (1.95) |
| 3 | 0.02 | 0.60 (0.18) | 6.78 (2.01) |
| ⊕ | 4.34 | 1.04 (0.31) | 6.85 (2.03) |
| C | 8.65 | 1.32 (0.39) | 6.72 (2.00) |
| F | 13.27 | 2.69 (0.80) | 6.05 (1.80) |
| H | 16.47, its frame's own (first 16.32) | 4.32 (1.28) | 4.39 (1.30), its frame's own (first the plan's 4.41 at its line) |

As Steel's rule has it, it stands a little above the water amidships and lifts to both ends, more
forward (judgement; `Build-Ships.md` §5.3 step 2).

### 4.12 The keel and the rabbet (measured, 2026-10-30)

The keel's lower edge is §4.5's straight line. Two close lines run along the top of the keel, 0.16
ft apart, carry on up the stem inside its fore edge to the rail, and run from the keel up the post
inside its fore side to the wale's scroll (read). The upper is at the dashed base line's level, on
which the frames end; it is taken as the rabbet's upper edge and the lower as its lower edge
(judgement). `x`, `z`, ft (m):

| Station | x | Rabbet, upper | Rabbet, lower | Keel's lower edge |
|---|---|---|---|---|
| 14 | −16.85 (−5.00) | −5.58 (−1.66) | −5.74 (−1.70) | −6.44 (−1.91) |
| 12 | −13.81 (−4.10) | −5.44 (−1.62) | −5.60 (−1.66) | −6.30 (−1.87) |
| 9 | −9.22 (−2.74) | −5.23 (−1.55) | −5.39 (−1.60) | −6.09 (−1.81) |
| 6 | −4.58 (−1.36) | −5.02 (−1.49) | −5.17 (−1.53) | −5.88 (−1.75) |
| 3 | 0.02 (0.01) | −4.82 (−1.43) | −4.98 (−1.48) | −5.68 (−1.69) |
| ⊕ | 4.34 (1.29) | −4.62 (−1.37) | −4.78 (−1.42) | −5.49 (−1.63) |
| C | 8.65 (2.57) | −4.42 (−1.31) | −4.58 (−1.36) | −5.30 (−1.57) |
| F | 13.27 (3.94) | −4.19 (−1.24) | −4.33 (−1.29) | −5.08 (−1.51) |

- **Up the stem**, the upper line, `x`, `z`: 12.00, −4.27; 13.17, −4.20; 14.33, −4.03; 15.47, −3.70;
  16.53, −3.13; 17.42, −2.30; 17.97, −1.20; 18.26, −0.02; 18.44, 1.18; 18.53, 2.39, then nearly
  plumb to the rail at x about 18.6. The lower line stands 0.12 to 0.25 ft forward of it. So the
  stem is about 1.0 ft moulded at the water, and the water line ends on the rabbet about 18.3 to
  18.4 ft from the middle, as §3 has it.
- **Up the post**, the fore line (the upper line's continuation), `x`, `z`: −17.25, −5.60; −17.39,
  −5.00; −17.57, −4.14; −17.75, −3.29; −18.01, −2.01; −18.20, −1.15; −18.36, −0.30; −18.55, 0.56;
  −18.63, 0.99. The after line stands 0.15 ft abaft it. So the post is about 0.9 ft moulded at the
  water and 1.3 ft at the keel, from its after edge to that fore line.
- **The keel's depth**: 0.86 to 0.88 ft (0.26 m) from its lower edge to the upper line, 0.89 ft
  at F (arithmetic).
- **Its half-siding** (measured): 0.23 ft on the half-breadth plan's short line abaft the post and
  0.24 ft forward at the stem; in the body plan the after frames close on 0.18 to 0.21 ft and the
  fore frames on 0.27 ft. So 0.23 ft (0.07 m), ±0.05, is taken along her (judgement). The post's
  half-siding in the body plan, the thin line beside the middle line from the counter to the
  water, is 0.32 ft at the counter and 0.25 ft at the water (0.09 and 0.07 m).

### 4.13 The diagonals and the lines inside (measured, 2026-10-30)

**The diagonals.** The body plan draws one heavy straight diagonal a side, the frames lettered where
they cross it. The heavy curve that §1.2 took as the rising line is this diagonal drawn in the
profile, and the two heavy lines of the half-breadth plan below the water lines are it expanded,
one aft and one forward, parting at ⊕ (measured against each other; judgement on the reading):

| Frame | x | Crossing, z | Crossing, half-breadth | The profile's heavy curve, z | Along the diagonal | The plan's heavy line |
|---|---|---|---|---|---|---|
| 14 | −16.85 | −0.91 | 0.93 | −0.97 | 1.50 | 1.42 |
| 12 | −13.81 | −1.84 | 1.77 | −1.91 | 2.87 | 2.84 |
| 9 | −9.22 | −2.80 | 2.69 | −2.89 | 4.36 | 4.31 |
| 6 | −4.58 | −3.38 | 3.31 | −3.49 | 5.37 | 5.34 |
| 3 | 0.02 | −3.71 | 3.74 | −3.79 | 6.05 | 5.98, first 6.02 on the water line beside it |
| ⊕, after | 4.34 | −3.71 | 3.89 | −3.80 | 6.30 | 6.19 |
| ⊕, fore | 4.34 | −3.73 | 3.85 | −3.80 | 5.07 | 5.09 |
| C | 8.65 | −3.32 | 3.60 | −3.38 | 4.73 | 4.73 |
| F | 13.27 | −2.34 | 2.71 | −2.33 | 3.56 | 3.56 |
| H | 16.38, first 16.32 | −1.13 | 1.46 | −1.16 | 1.92 | 1.98 |

It crosses the frames at about the floor's head, so it is written for `floor_m` as the nearest thing
to a rising line the plate has (§5.1; judgement; not drawn).

**The dashed curve** low in the profile (read) is taken as the cutting-down line, the top of the
floors at the middle line (judgement): z −1.87 at 14, −3.22 at 12, −3.91 at 9, −3.99 at the
well's after end (x −6.9), broken by the well, −3.99 at its fore end (x 4.7), −3.74 at C, −3.09 at
F, −1.83 at H, then up inside the stem to the rail's height near x 18.

### 4.14 The stern (read and measured, 2026-10-30)

**What it is.** Raked and rounded above a short rounded counter (read). There is no square tuck, and
no wing transom is drawn. Three lines run up the side view from the transom's foot to one point,
the taffrail at the middle line:

| Line | Points, `x`, `z`, ft | Taken as (judgement) |
|---|---|---|
| Heavy, forward | the taffrail −22.42, 6.54; −21.67, 6.08; −21.46, 5.83; the rail's end −21.31, 5.60; straight to −20.32, 2.66 | the rail's sweep up to the taffrail, then the side's after edge |
| Middle | the taffrail; −21.88, 5.81; −21.67, 5.17; −21.26, 3.90; −20.89, 2.91 | the transom's corner |
| After | the taffrail; −22.09, 5.54; −21.67, 4.40; −21.30, 3.27 | the transom's face at the middle line |

The same from aft, in the body plan, `z`, half-breadth, ft, each ±0.05:

| Outline | Points |
|---|---|
| The transom's corner, the rail's end down to the foot | 5.55, 2.64; 5.04, 2.75; 4.52, 2.85; 4.18, 2.92; 3.66, 3.00; 3.27, 3.06; 3.06, 3.09; 2.88, 3.12 |
| The side's after edge | 5.58, 2.99; 5.24, 3.28; 4.90, 3.46; 4.55, 3.56; 4.21, 3.62; 3.86, 3.64; 3.52, 3.62; 3.09, 3.56; 2.65, 3.46 |
| The counter's outline, heavy | 2.52, 3.66; 2.30, 3.79; 2.09, 3.85; 1.87, 3.87; 1.66, 3.86; 1.44, 3.81; 1.23, 3.68; 1.12, 3.46 |
| The taffrail's arc, the rail's end to the middle line | 5.70, 2.80; 6.04, 2.31; 6.28, 1.23; 6.35, 0.64; 6.38, 0.01 |
| The transom's foot, heavy, to the middle line | 2.88, 3.12 rising to 3.09, 0.01 |

- **The half-breadth at the rail's end**: 2.64 ft (0.78 m), read in the body plan and in the
  half-breadth plan alike (read again 2.58 in the plan and 2.62 in the body plan, within ±0.05).
  `Build-Ships.md` §5.7's 0.78 m is this figure at the plate's own size; the file carries it so
  (§5.3).
- **At the transom's foot**: 3.12 ft (0.93 m), the corner's foot.
- **The foot's round-up**: 3.27 less 2.91, 0.36 ft (0.11 m), in the profile; 0.21 ft (0.06 m) in the
  body plan (measured). The profile's is taken, since `stern_m` stands on it (judgement).
- **The taffrail's round**: 0.94 ft (0.28 m) above the rail's end in the profile, 0.83 ft in the body
  plan, whose taffrail stands 0.16 ft lower. In plan the face is rounded by about 0.25 ft from the
  corner (x −21.9) to the middle line (x −22.2), against −22.44 in the profile (measured; ±0.2).
- **The counter**, from the foot's corner to the post: −20.89, 2.91; −20.43, 2.71; −20.01, 2.52;
  −19.59, 2.29 at the post, on the after perpendicular; and along the side on to −19.17, 2.01 and
  the wale's scroll at −18.30, 1.00. From aft it swells to 3.87 ft half-breadth at z 1.87, and is
  closed at its foot by a moulded band of three lines at z about 1.2, 0.24 ft deep, across to the
  post: the wale's scroll carried round (read; judgement on the reading).
- **Galleries and lights**: none (§4.16).

### 4.15 The masts' places (read and judgement, 2026-10-30)

No mast or spar is drawn on No. 3, in the profile, the plan or the body plan (read); §4.8's post
stands too far forward to be taken for one. The place is judged from the channel: three deadeyes
at 2.0, 3.5 and 5.1 ft before the middle (0.59, 1.04, 1.51 m; §4.8), and a mast stands a little
forward of its foremost shroud, so about 5.5 to 7 ft before the middle (1.6 to 2.1 m; judgement).
Two checks against the file (recorded, not moved; its figures carried back by §5.3's length ratio):
its `main.mast` at +1.8 m comes to 1.69 m on the plate, in that band; and its running bowsprit's
heel, 8.4 ft inboard of its `x_m` of +6.4 m, is at +3.84 m, against the dashed post of §4.8 at 3.84 m
on the plate, 4.09 m at her length, which fits the post as bitts (judgement).

### 4.16 Ports, galleries, lights and the head (read, 2026-10-30)

- **Ports**: no port, sweep port or gun is drawn on No. 3's side or in its body plan. So no centre,
  sill or size can be read, and **no triple of `Build-Ships.md` §5.4 can be written from this
  plate**. Steel's sloop has none either (Folio I's row Q and Folio XXXII's port rows are blank for her).
  The file has no gun at this commit, and its default is `unarmed` (§9.1 of the design). If the fit
  "culloden 1746" lands at SW-4, the side gives no room for a port: the rail stands only 1.4 to 1.5
  ft (0.42 to 0.45 m) above the fore deck at side amidships, so her two guns would be rail guns, by
  `rail_at`, with no triple (`Build-Ships.md` §5.1; judgement).
- **Galleries and lights**: none in the side, none on the transom's outline in the body plan (read).
  Her type did not certainly carry them, so none is placed (`Build-Ships.md` §5.0 principle 9;
  judgement).
- **The head**: none. The stem rises straight 1.4 ft above the rail's end, squared off, its top
  sloping from 8.31 to 8.68 ft (§4.5). No knee, no rails, no figure, no billet (read). The word is
  `none`, and `head_m` is not written.

## 5. For the profile (B8): the points in metres

At the plate's own size (39.12 Sw ft between the perpendiculars, 11.61 m), unscaled: the file
is a larger vessel (§6), and how the plate is carried to her is B8's judgement. `x` forward of
the mid-perpendiculars along the keel, `z` above the LWL square to the keel (the units
paragraph above §0). Measured unless marked.

- **`rail_m`**: [−6.66, 1.94], [−6.43, 1.81], [−6.37, 1.73], the taffrail's sweep (§4.14), then
  [−6.32, 1.66], [−6.19, 1.64], [−5.81, 1.59], [−5.44, 1.55], [−5.00, 1.50],
  [−4.10, 1.43], [−2.74, 1.36], [−1.36, 1.33], [0.01, 1.36], [1.29, 1.42], [2.58, 1.55],
  [3.95, 1.75], [4.85, 1.94], [5.18, 2.03], [5.38, 2.09], [5.39, 2.45]: it ends at the stem head's
  after edge, its stop and that edge's top (§4.5). First written [5.43, 2.10], [5.60, 2.15], which
  drew the top of the bow as a wedge 0.3 to 0.4 m low at the head.
- **`breadth_m`** [x, at the water, at the rail], corrected by §4.6: [−5.46, 0.08, 1.15], [−5.40,
  0.17, 1.17], [−5.34, 0.40, 1.19], [−5.21,
  0.71, 1.22], [−5.09, 0.89, 1.26], [−5.00, 0.97, 1.28], [−4.57, 1.28, 1.39], [−4.10, 1.46, 1.48],
  [−2.74, 1.78,
  1.70], [−1.36, 1.95, 1.83], [0.01, 2.01, 1.90], [1.29, 2.03, 1.91], [2.57, 1.98, 1.87], [3.41,
  1.80, 1.80], [3.94,
  1.59, 1.69], [4.36, 1.29, 1.54], [4.86, 0.75, 1.25], [5.04, 0.55, 1.11], [5.16, 0.39, 0.99], [5.17, 0.37, 0.96] (at the
  rail's point, between the lines either side, arithmetic), [5.28, 0.26, 0.79],
  then, the top of the side being the head from the rail's stop forward (§4.6), [5.38, 0.16, 0.09],
  [5.39, 0.15, 0.09], [5.41, 0.13, 0.09], [5.47, 0.08, 0.09], [5.56, 0.08, 0.09]. First written to
  end [5.41, 0.13, 0.54], the rail's half-breadth there, which stands now in `sections_m` (§5.3).
  The rail's half-breadth at the transom 0.78 (§4.6); the water line closes to the rabbets about
  5.4 m from the middle at each end. It was first written [−5.00, 0.96, 1.28], [−4.10, 1.46, 1.47],
  [−2.74, 1.78, 1.69], [−1.36, 1.95, 1.84], [0.01, 1.98, 1.90], [1.29, 2.00, 1.91],
  [2.57, 1.98, 1.88], [3.94, 1.59, 1.69], [4.85, 0.80, 1.28]; and it began at −5.34 and held no
  point between the stations (the review, 2026-10-30, §4.6).
- **`keel_m`**: [−5.46, −1.94], [5.19, −1.45].
- **`stem_m`**, the fore edge, low to high: [5.19, −1.45], [5.28, −1.35], [5.47, −1.05],
  [5.57, −0.79], [5.64, −0.53], [5.69, −0.27], [5.72, 0.00], [5.75, 0.24], [5.77, 0.50],
  [5.79, 0.88], [5.79, 1.40], [5.79, 2.04], [5.78, 2.58] (the stem head's fore top).
- **`stern_m`**, low to high, corrected by §4.5: [−5.46, −1.94], [−5.52, −1.50], [−5.59, −0.99],
  [−5.66, −0.48], [−5.73, 0.00], [−5.82, 0.68] (the counter at the post; first 0.73), [−6.20, 0.86]
  (the foot's corner; first [−6.19, 0.87]), [−6.32, 0.97] (the foot at the middle line; first
  [−6.33, 0.98]), [−6.66, 1.94] (the taffrail at the middle line).
- **`wales_m`** [x, lower, upper]: [−5.69, 0.59, 0.60] (the upper line's end, §4.2; first it began at
  the next), [−5.45, 0.30, 0.57], [−5.00, 0.28, 0.53], [−4.10, 0.21, 0.45],
  [−2.74, 0.14, 0.39], [−1.36, 0.12, 0.37], [0.01, 0.14, 0.40], [1.29, 0.21, 0.47],
  [2.57, 0.32, 0.59], [3.94, 0.52, 0.79], [4.86, 0.71, 0.98], [5.61, 0.92, 1.20] (§4.2; first [5.48,
  0.89, 1.15]).
- **`section_m`** [z, half-breadth], moulded; with the plank, add its thickness (not drawn;
  judgement about 1¼ in, 0.03 m). Registered by the base line (§2.5), low to high from the rabbet
  to the rail: [−1.37, 0.08], [−1.25, 0.58], [−1.16, 0.96], [−1.07, 1.27], [−0.95, 1.54], [−0.83,
  1.71], [−0.69, 1.84], [−0.52, 1.93], [−0.35, 1.99], [−0.17, 2.02], [0.00, 2.03], [0.15, 2.03],
  [0.30, 2.03], [0.59, 2.03], [0.89, 2.02], [1.19, 1.97], [1.42, 1.91].
  First written from the LWL mark, each 0.02 m lower, in §4.7's steps.
- **`decks_m`**, the deck at side, in two pieces with the waist between not drawn (§4.4): the
  after deck [−6.03, 0.78], [−5.79, 0.78], [−5.41, 0.77], [−5.00, 0.76], [−4.79, 0.75],
  [−4.30, 0.74], [−4.23, 0.74]; the fore deck [−1.78, 0.91], [−1.36, 0.91], [−0.91, 0.92],
  [−0.17, 0.94], [0.01, 0.94], [1.29, 1.00], [1.94, 1.05], [2.57, 1.10], [3.43, 1.19],
  [3.94, 1.26], [4.37, 1.31], [4.86, 1.39], [5.30, 1.47]. Whether the two are one `upper` deck
  with a step, or the waist is open, is judgement.
- **`ports_m`, `port_size_m`**: none drawn, none written (§4.16).

### 5.1 The shape keys, at the plate's own size (`Build-Ships.md` §5.1; 2026-10-30)

Each is measured as §4 says; what the marks in the file would be follows. All `x`, `z` as above.

- **`breadth_line_m`** [x, z, half-breadth], §4.11: [−5.00, 0.64, 1.36], [−4.10, 0.53, 1.59],
  [−2.74, 0.41, 1.82], [−1.36, 0.27, 1.95], [0.01, 0.18, 2.01], [1.29, 0.31, 2.03], [2.57, 0.39,
  2.00], [3.94, 0.80, 1.80], [4.36, 1.01, 1.64], [4.89, 1.28, 1.30], H at its frame's own place and
  half-breadth (§2.5; first [4.85, 1.28, 1.31]); the point at 4.36 is the plan's half-breadth (§4.6),
  its height straight between F's and H's (arithmetic).
- **`sections_m`** [z, half-breadth] at each station, §4.10, moulded, low to high; the water and the
  rail are `breadth_m`'s and not repeated, so that no place is given two half-breadths
  (`form.check`):
  - 14, x −5.00: [−1.66, 0.06], [−1.60, 0.05], [−1.51, 0.05], [−1.43, 0.06], [−1.34, 0.06],
    [−1.25, 0.07], [−1.16, 0.08], [−1.07, 0.08], [−0.95, 0.09], [−0.83, 0.11], [−0.69, 0.12],
    [−0.52, 0.15], [−0.35, 0.21], [−0.17, 0.47], [0.15, 1.20], [0.30, 1.31], [0.59, 1.37], [0.89,
    1.36];
  - 12, x −4.10: [−1.62, 0.06], [−1.51, 0.07], [−1.43, 0.09], [−1.34, 0.11], [−1.25, 0.13],
    [−1.16, 0.15], [−1.07, 0.18], [−0.95, 0.22], [−0.83, 0.27], [−0.69, 0.35], [−0.52, 0.57],
    [−0.35, 0.96], [−0.17, 1.27], [0.15, 1.54], [0.30, 1.58], [0.59, 1.59], [0.89, 1.58], [1.19,
    1.54];
  - 9, x −2.74: [−1.55, 0.07], [−1.51, 0.07], [−1.43, 0.12], [−1.34, 0.18], [−1.25, 0.25],
    [−1.16, 0.34], [−1.07, 0.44], [−0.95, 0.60], [−0.83, 0.80], [−0.69, 1.07], [−0.52, 1.37],
    [−0.35, 1.57], [−0.17, 1.70], [0.15, 1.80], [0.30, 1.82], [0.59, 1.82], [0.89, 1.79], [1.19,
    1.74];
  - 6, x −1.36: [−1.49, 0.07], [−1.43, 0.14], [−1.34, 0.28], [−1.25, 0.44], [−1.16, 0.63],
    [−1.07, 0.83], [−0.95, 1.11], [−0.83, 1.35], [−0.69, 1.56], [−0.52, 1.74], [−0.35, 1.84],
    [−0.17, 1.90], [0.15, 1.95], [0.30, 1.95], [0.59, 1.94], [0.89, 1.92], [1.19, 1.86];
  - 3, x 0.01: [−1.43, 0.08], [−1.34, 0.32], [−1.25, 0.62], [−1.16, 0.94], [−1.07, 1.20],
    [−0.95, 1.47], [−0.83, 1.65], [−0.69, 1.79], [−0.52, 1.90], [−0.35, 1.97], [−0.17, 2.00],
    [0.15, 2.02], [0.30, 2.01], [0.59, 2.01], [0.89, 1.99], [1.19, 1.94];
  - ⊕, x 1.29: [−1.37, 0.08], [−1.25, 0.58], [−1.16, 0.96], [−1.07, 1.27], [−0.95, 1.54],
    [−0.83, 1.71], [−0.69, 1.84], [−0.52, 1.93], [−0.35, 1.99], [−0.17, 2.02], [0.15, 2.03],
    [0.30, 2.03], [0.59, 2.03], [0.89, 2.02], [1.19, 1.97];
  - C, x 2.57: [−1.31, 0.08], [−1.25, 0.25], [−1.16, 0.54], [−1.07, 0.83], [−0.95, 1.16],
    [−0.83, 1.41], [−0.69, 1.61], [−0.52, 1.77], [−0.35, 1.88], [−0.17, 1.94], [0.15, 1.98],
    [0.30, 1.99], [0.59, 1.99], [0.89, 1.98], [1.19, 1.95];
  - F, x 3.94: [−1.24, 0.08], [−1.16, 0.16], [−1.07, 0.26], [−0.95, 0.42], [−0.83, 0.60],
    [−0.69, 0.81], [−0.52, 1.04], [−0.35, 1.25], [−0.17, 1.43], [0.15, 1.67], [0.30, 1.74],
    [0.59, 1.79], [0.89, 1.80], [1.19, 1.78];
  - H, x 4.89 (first 4.93): [−1.07, 0.04], [−0.95, 0.07], [−0.83, 0.11], [−0.69, 0.18], [−0.52, 0.30],
    [−0.35, 0.42], [−0.17, 0.56], [0.15, 0.83], [0.30, 0.95], [0.59, 1.15], [0.89, 1.27], [1.19,
    1.30];
- **`channel_wales_m`** [x, lower, upper]: the second band of §4.2, end to end, on which the
  channel lies: [−6.22, 1.36, 1.43], [−5.00, 1.21, 1.29], [−4.10, 1.14, 1.21], [−2.74, 1.07, 1.15],
  [−1.36, 1.05, 1.13], [0.01, 1.07, 1.15], [1.29, 1.13, 1.21], [2.57, 1.26, 1.34], [3.94, 1.48,
  1.54], [4.86, 1.66, 1.73], [5.60, 1.86, 1.94].
  That it stands for a channel wale is judgement.
- **`rabbet_m`** [x, z, half-siding], §4.12, the upper line along the keel and up the stem:
  [−5.00, −1.66, 0.07], [−4.10, −1.62, 0.07], [−2.74, −1.55, 0.07], [−1.36, −1.49, 0.07], [0.01,
  −1.43, 0.07], [1.29, −1.37, 0.07], [2.57, −1.31, 0.07], [3.56, −1.27, 0.07], [3.91, −1.25,
  0.07], [4.25, −1.20, 0.07], [4.59, −1.10, 0.07], [4.91, −0.93, 0.07], [5.17, −0.68, 0.07],
  [5.34, −0.36, 0.07], [5.42, −0.01, 0.07], [5.47, 0.35, 0.07], [5.50, 0.71, 0.07]. The post's
  fore line, for later: [−5.53, 0.29], [−5.51, 0.17], [−5.45, −0.09], [−5.40, −0.34], [−5.35,
  −0.60], [−5.27, −0.98], [−5.22, −1.23], [−5.16, −1.48], [−5.12, −1.66].
- **`floor_m`** [x, z, half-breadth]: z from the profile's heavy curve, half-breadth from the
  frame's crossing of the diagonal (§4.13), reserved and not drawn:
  [−5.00, −0.29, 0.28], [−4.10, −0.57, 0.53], [−2.74, −0.86, 0.80], [−1.36, −1.04, 0.98], [0.01,
  −1.13, 1.11], [1.29, −1.13, 1.15], [2.57, −1.00, 1.07], [3.94, −0.69, 0.80], [4.86, −0.34,
  0.43].
- **`head_m`**: none (§4.16).
- **`form.fullness`**: none is given; the frames draw the ends (as the 64's).
- **`form.stern`**, §4.14: `type: raked`; `knuckle_z_m` 0.86, the transom's foot at its corner;
  `transom_hb_m` [0.78, 0.93], at the rail's end and at the foot; `round_up_m` 0.11. No
  `galleries_m`, no `lights_m`.
- **`form.head`**: `none`.
- **`marks`** (`Build-Ships.md` §5.0 principle 4, a line taking the word of its weakest point):
  `stand-in` for `keel_m`, `form.stern`, `form.stern.knuckle_z_m`, `form.stern.round_up_m` and
  `form.head`, wholly the plate's by principle 7's own factors; `judged` for `rail_m`, `stem_m`,
  `stern_m`, `section_m` and `sections_m` (the side's height, §5.3, each ending on the rail),
  `breadth_m` (the water at 3 and ⊕, §4.6), `wales_m` (which band it is, §4.2), `breadth_line_m` and
  `sections_m` again (frame H's place, §2.5), `form.stern.transom_hb_m` (the plate's own, not carried
  by the ratio, §4.14), `decks_m` (the waist, §4.4), `channel_wales_m`, `floor_m` and `rabbet_m` (its
  lines and its half-siding on every point are judgement, §4.12). **Old beside new, at the landing:**
  all but the last four were first `stand-in`, on the grounds that the wale's other band is a moulding
  0.26 ft deep and that the two ratios put the rail's lowest 1.41 or 1.42 m up, under 1 cm apart.
  Principle 4 has no such exception: a line takes the word of its weakest point, however small.

### 5.2 Steel's coasting sloop, as `Build-Ships.md` §5.7 first had it (2026-10-30)

§5.7 and §5.3 of the design first put Steel's sloop under the water between the plate's stations, through
`g.from_steel_table`, the plate's section ruling at midships, because only the plate's midship
section had been read. The rows, read (`pages-steel-1805-bodies.md` §3.3; `x` on her judged length
of 50 ft 3 in, that note's §5.1 and §5.2). Timber 4's third diagonal goes in as 8 4¼, the fair
figure (judgement), the printed 7 4¼ making a kink of 0.4 m:

```python
rows = {
    "water": [[-7.66, "8 7"], [7.66, "6 7"]],
    "diagonals": [["4 6", ["4 11½", "0 0"]], ["5 10½", ["6 4½", "0 0"]], ["7 7", ["8 3", "0 10½"]],
                  ["9 4", ["8 3", "3 2½"]], ["12 3", ["8 3", "4 9"]]],
    "timbers": [  # name, x, lower height of breadth, upper, main half-breadth, down the diagonals
        ["13", -6.59, "9 4½", "9 8¼", "6 2", [None, "0 9", "1 10", "3 8", "6 11"]],
        ["12", -5.94, "8 8½", "9 3", "6 6", ["1 3¼", "2 2", "3 7", "5 5", "7 10"]],
        ["10", -4.66, "7 8", "8 6", "7 0", ["2 8", "3 9", "5 5", "7 2", "9 0½"]],
        ["8", -3.42, "6 10½", "8 0", "7 5", ["3 9", "5 0", "6 8", "8 1", "9 9"]],
        ["6", -2.11, "6 4", "7 7", "7 9¼", ["4 7", "6 0", "7 9", "8 11", "10 4"]],
        ["4", -0.85, "6 0½", "7 4", "7 11½", ["5 3", "6 9", "8 4¼", "9 4", "10 8¾"]],
        ["2", 0.47, "5 10½", "7 2½", "8 1", ["5 8", "7 2", "8 9", "9 7", "10 10"]],
        ["O", 1.74, "5 10", "7 2", "8 3", ["5 11", "7 5", "9 0", "9 10", "11 0"]],
        ["A", 2.87, "6 1½", "7 4½", "8 2½", ["5 9½", "7 3½", "8 11", "9 9", "10 11½"]],
        ["C", 4.17, "6 7", "7 8", "7 11½", ["5 2¾", "6 8½", "8 4", "9 3", "10 6"]],
        ["E", 5.44, "7 4", "8 3", "7 3", ["4 2¾", "5 7", "7 2¼", "8 2¾", "9 6"]],
        ["F", 6.08, "7 11¾", "8 7", "6 5", ["3 1½", "4 4", "6 0", "7 1", "8 5"]],
        ["G", 6.72, "8 9", "9 1", "4 9", ["1 1", "2 3", "3 8", "4 10", "6 2½"]],
    ],
}
```

The factors (`Build-Ships.md` §5.0 principle 7): `length_ratio` 12.2 / 15.85 = 0.770, her water
length taken as Folio I's row C, 52 ft 0 in (judgement, ±1 ft); `beam_ratio` 4.3 / 5.08 = 0.846, her
extreme breadth, 16 ft 8 in.

**What they make, beside the plate's frames at her length and beam** (arithmetic; the helper as it
stands, the plate's frames straight between stations):

- At Steel's 13 timbers, 65 of her 77 points (the other 12 lie below the plate's rabbet), Steel's
  half-breadth is more than the plate's by a mean of 0.47 m (standard deviation 0.39, rms 0.61,
  largest 1.55): Steel's is the deeper body by far. (Corrected, 2026-10-30: the 0.39 was first called
  an rms; `steel_cmp.py` printed the standard deviation under that word.)
- At the sloop's ⊕, x 1.34: z −1.41, 1.80 against 0.25; −1.00, 2.04 against 1.64; −0.65, 2.10 against 1.99;
  −0.39, 2.13 against 2.10. In the run, x −4.58: z −0.36, 1.50 against 0.86. In the entry, x 4.68:
  z −0.05, 1.61 against 1.20.
- That ⊕ falls 3 cm from the plate's midship section at x 1.37: at z −1.32 the side would step from
  about 1.85 m to 0.61 m. So "the plate's section ruling at midships" cannot run fair into hers.
- Passed through the helpers with the plate's rail, breadths and midship section: drawn 53 t against
  the filed 46 t (+15%) with Steel's ⊕ dropped for the plate's midship section, 54 t (+16%) with it
  kept (first written +17%); the plate's own frames 38 t (−18%). All pass `form.check`.
- Beside the plate's water, Steel's body stands outside it just under the water toward both ends: at
  x −5.07, z −0.22, 1.32 m against 1.21 m at the water (first 1.17 m); at x 4.68, z −0.05, 1.61 m
  against 1.33 m (first 1.24 m); at x 5.17, z −0.07, 1.00 m against 0.81 m. So the drawn section steps
  out below the water, and heel shows it (the builder's sheets, §8).
- **Its timbers end on a flat foot** (the review, 2026-10-30). The table gives no point below its first
  diagonal, and `g.from_steel_table` closes nothing to the keel. The plate's midship section, from
  which the rule fills below a given point, stops at the plate's rabbet, which stands above that
  diagonal. So from x −1.6 to x 4.2 each timber's lowest point is its lowest drawn, 0.81 to 1.11 m out
  from the middle line (at x 0.36, z −1.76, 1.08 m), and the bottom is drawn flat there, but for the
  notch up to −1.45 at the plate's ⊕. Steel's own base, the rabbet, scaled, falls about −1.94 m, under
  the plate's keel at −1.77 m, so no foot of the sloop's fits on this keel: at x 2.21 its diagonal
  already stands 2 cm below it. It shows only with the body drawn solid (`underwater`, sheet 04), and a
  foot on the plate's keel would be nearly as flat. So it is not mended; the plate's frames have none
  of it.
- Her main breadth stands lower than the plate's at every station, by 0.3 to 0.8 m: at ⊕ −0.05 m
  scaled against +0.33 m.
- Above the water §5.7 named only the plate, so neither body takes the sloop there (§5.3).

**The pick (judgement), for the lead:** the plate's frames for `sections_m` and `breadth_line_m`, Steel's
sloop a check. The rung does not move: both are S†, her type and not herself, and the stern and head
are as §5.7 has them. `Build-Ships.md` §5.0 principle 5 has sourced points win and principle 12 lets
a better reading replace the words. The departure was from §5.7's words on Steel, and from §5.6's
"`pages-chapman-pl59.md` §4.7" as the whole of what this plate gives. Steel's rows stand above as the
check. The checker's measures support the pick: the frames reproduce at an rms of 0.034 ft, cross the
plate's own water-line curves at the profile's heights within 0.04 ft, and agree on the second
photograph at an rms of 0.024 ft.

**The ruling (the lead, 2026-10-31): the plate's own frames, sourced points over the rule; the −18%
reported past the line; §5.7's row amended.** So `UNDER_WATER = "plate"` in
`tools/ships/hull_smack.py`, as §5.3 gives it, and `Build-Ships.md` §5.7's row and §5.6's reference
("§4.7" to "§4.10") are amended. Old beside new, drawn only: 53 t (+15%) on the sloop, her first build;
38 t (−18%) on the frames, past §5.0 principle 8's 15%, reported and never moved. `"steel"` still
draws the sloop, its timber O left out for the plate's ⊕ frame.

### 5.3 Carried to the file (arithmetic and judgement; 2026-10-30)

By `Build-Ships.md` §5.0 principle 7, the factors:

- **`length_ratio` 12.2 / 11.46 = 1.0646**, the waterlines': every `x`.
- **`beam_ratio` 4.3 / 4.06 = 1.0591**, the moulded breadth to the file's beam, so that the drawn hull
  is her file's beam with no plank added (`Build-Ships.md` §5.0 principle 7's last sentence): every half-breadth, and every `z` of the body:
  the sections, the main breadth's height, the wale, the bands, the deck, the keel, the rabbet, the
  floor, the stem below the rail's height, the post, the counter, the knuckle and the round-up.
- **The side**: principle 7 takes it from her own source for the sills, and she has none (§4.16). So
  the rail's lowest, 4.49 ft, by `beam_ratio`, 1.41 m (judgement: with the frames it stands on), and
  its rise above that by `length_ratio`; the taffrail and the stem head likewise.
- **The frame**: `x` along the keel, `z` square to it at `x`, as the units paragraph has it and as the
  64's module does it. Not turned level with the water; §0's `x − 0.045 z` is there if the
  pictures ask for it.

Her profile so carried, as `tools/ships/hull_smack.py` makes it through `g.hull_profile` and
`g.hull_form` on this tree (`freesail` read from this worktree), the file's own, the plate's frames
as ruled. In metres to the centimetre; `tests/test_hull_smack.py` holds the file to this block:

```yaml
rail_m: [[-7.09, 2.06], [-6.85, 1.91], [-6.78, 1.84], [-6.73, 1.76], [-6.58, 1.74], [-6.19, 1.69], [-5.79, 1.64], [-5.32, 1.59], [-4.36, 1.51], [-2.91, 1.44], [-1.44, 1.41], [0.01, 1.44], [1.38, 1.51], [2.74, 1.64], [4.2, 1.86], [5.17, 2.06], [5.51, 2.15], [5.73, 2.22], [5.74, 2.6]]
breadth_m: [[-5.82, 0.08, 1.22], [-5.75, 0.18, 1.24], [-5.68, 0.43, 1.26], [-5.55, 0.75, 1.3], [-5.41, 0.94, 1.33], [-5.33, 1.03, 1.36], [-4.87, 1.35, 1.47], [-4.36, 1.55, 1.57], [-2.91, 1.88, 1.8], [-1.45, 2.06, 1.94], [0.01, 2.13, 2.01], [1.37, 2.15, 2.02], [2.73, 2.09, 1.98], [3.63, 1.91, 1.91], [4.19, 1.68, 1.79], [4.65, 1.36, 1.64], [5.18, 0.8, 1.33], [5.36, 0.58, 1.18], [5.49, 0.41, 1.04], [5.51, 0.39, 1.02], [5.62, 0.27, 0.84], [5.73, 0.17, 0.09], [5.74, 0.16, 0.09], [5.76, 0.14, 0.09], [5.82, 0.08, 0.09], [5.92, 0.08, 0.09]]
keel_m: [[-5.81, -2.05], [5.53, -1.53]]
stem_m: [[5.53, -1.53], [5.62, -1.42], [5.82, -1.11], [5.93, -0.84], [6.0, -0.56], [6.05, -0.29], [6.09, 0.0], [6.12, 0.25], [6.14, 0.53], [6.16, 0.93], [6.17, 1.48], [6.16, 2.16], [6.15, 2.74]]
stern_m: [[-5.81, -2.05], [-5.88, -1.59], [-5.95, -1.05], [-6.03, -0.51], [-6.1, 0.0], [-6.19, 0.72], [-6.6, 0.92], [-6.73, 1.03], [-7.09, 2.06]]
wales_m: [[-6.06, 0.63, 0.64], [-5.8, 0.32, 0.61], [-5.33, 0.3, 0.56], [-4.36, 0.22, 0.48], [-2.91, 0.15, 0.41], [-1.45, 0.13, 0.39], [0.01, 0.15, 0.42], [1.37, 0.22, 0.49], [2.73, 0.34, 0.62], [4.19, 0.56, 0.84], [5.18, 0.75, 1.03], [5.97, 0.98, 1.27]]
section_m: [[-1.45, 0.09], [-1.32, 0.61], [-1.23, 1.02], [-1.13, 1.34], [-1.01, 1.63], [-0.88, 1.81], [-0.73, 1.95], [-0.55, 2.05], [-0.37, 2.11], [-0.18, 2.14], [0.0, 2.15], [0.16, 2.15], [0.31, 2.15], [0.63, 2.15], [0.94, 2.14], [1.26, 2.09], [1.51, 2.02]]
decks_m: {"upper": [[-6.42, 0.82], [-6.16, 0.82], [-5.76, 0.81], [-5.33, 0.8], [-5.1, 0.79], [-4.57, 0.78], [-4.51, 0.78], [-1.9, 0.96], [-1.45, 0.97], [-0.97, 0.97], [-0.18, 0.99], [0.01, 1.0], [1.37, 1.06], [2.07, 1.11], [2.73, 1.17], [3.66, 1.26], [4.19, 1.33], [4.65, 1.39], [5.18, 1.47], [5.64, 1.56]]}
breadth_line_m: [[-5.33, 0.68, 1.44], [-4.36, 0.56, 1.69], [-2.91, 0.43, 1.93], [-1.45, 0.29, 2.06], [0.01, 0.19, 2.13], [1.37, 0.33, 2.15], [2.73, 0.42, 2.11], [4.19, 0.85, 1.9], [4.65, 1.07, 1.73], [5.21, 1.36, 1.38]]
sections_m:   # [x, z, half-breadth], one station to a line: the plate's frames, the file's
  - [[-5.33, -1.75, 0.07], [-5.33, -1.7, 0.06], [-5.33, -1.6, 0.06], [-5.33, -1.51, 0.06], [-5.33, -1.42, 0.07], [-5.33, -1.32, 0.07], [-5.33, -1.23, 0.08], [-5.33, -1.13, 0.09], [-5.33, -1.01, 0.1], [-5.33, -0.88, 0.11], [-5.33, -0.73, 0.13], [-5.33, -0.55, 0.16], [-5.33, -0.37, 0.22], [-5.33, -0.18, 0.5], [-5.33, 0.16, 1.27], [-5.33, 0.31, 1.38], [-5.33, 0.63, 1.45], [-5.33, 0.94, 1.44]]
  - [[-4.36, -1.71, 0.07], [-4.36, -1.6, 0.08], [-4.36, -1.51, 0.09], [-4.36, -1.42, 0.12], [-4.36, -1.32, 0.14], [-4.36, -1.23, 0.16], [-4.36, -1.13, 0.19], [-4.36, -1.01, 0.24], [-4.36, -0.88, 0.29], [-4.36, -0.73, 0.37], [-4.36, -0.55, 0.61], [-4.36, -0.37, 1.02], [-4.36, -0.18, 1.35], [-4.36, 0.16, 1.63], [-4.36, 0.31, 1.67], [-4.36, 0.63, 1.69], [-4.36, 0.94, 1.67], [-4.36, 1.26, 1.63]]
  - [[-2.91, -1.64, 0.07], [-2.91, -1.6, 0.07], [-2.91, -1.51, 0.13], [-2.91, -1.42, 0.19], [-2.91, -1.32, 0.27], [-2.91, -1.23, 0.36], [-2.91, -1.13, 0.46], [-2.91, -1.01, 0.64], [-2.91, -0.88, 0.85], [-2.91, -0.73, 1.14], [-2.91, -0.55, 1.45], [-2.91, -0.37, 1.66], [-2.91, -0.18, 1.8], [-2.91, 0.16, 1.91], [-2.91, 0.31, 1.93], [-2.91, 0.63, 1.92], [-2.91, 0.94, 1.9], [-2.91, 1.26, 1.85]]
  - [[-1.45, -1.58, 0.08], [-1.45, -1.51, 0.15], [-1.45, -1.42, 0.3], [-1.45, -1.32, 0.47], [-1.45, -1.23, 0.66], [-1.45, -1.13, 0.88], [-1.45, -1.01, 1.18], [-1.45, -0.88, 1.43], [-1.45, -0.73, 1.65], [-1.45, -0.55, 1.84], [-1.45, -0.37, 1.95], [-1.45, -0.18, 2.02], [-1.45, 0.16, 2.06], [-1.45, 0.31, 2.07], [-1.45, 0.63, 2.06], [-1.45, 0.94, 2.03], [-1.45, 1.26, 1.97]]
  - [[0.01, -1.52, 0.08], [0.01, -1.42, 0.34], [0.01, -1.32, 0.66], [0.01, -1.23, 0.99], [0.01, -1.13, 1.27], [0.01, -1.01, 1.55], [0.01, -0.88, 1.75], [0.01, -0.73, 1.9], [0.01, -0.55, 2.02], [0.01, -0.37, 2.08], [0.01, -0.18, 2.12], [0.01, 0.16, 2.14], [0.01, 0.31, 2.14], [0.01, 0.63, 2.13], [0.01, 0.94, 2.11], [0.01, 1.26, 2.05]]
  - [[1.37, -1.45, 0.09], [1.37, -1.32, 0.61], [1.37, -1.23, 1.02], [1.37, -1.13, 1.34], [1.37, -1.01, 1.63], [1.37, -0.88, 1.81], [1.37, -0.73, 1.95], [1.37, -0.55, 2.05], [1.37, -0.37, 2.11], [1.37, -0.18, 2.14], [1.37, 0.16, 2.15], [1.37, 0.31, 2.15], [1.37, 0.63, 2.15], [1.37, 0.94, 2.14], [1.37, 1.26, 2.09]]
  - [[2.73, -1.39, 0.09], [2.73, -1.32, 0.27], [2.73, -1.23, 0.58], [2.73, -1.13, 0.88], [2.73, -1.01, 1.23], [2.73, -0.88, 1.49], [2.73, -0.73, 1.71], [2.73, -0.55, 1.88], [2.73, -0.37, 1.99], [2.73, -0.18, 2.05], [2.73, 0.16, 2.1], [2.73, 0.31, 2.11], [2.73, 0.63, 2.11], [2.73, 0.94, 2.1], [2.73, 1.26, 2.07]]
  - [[4.19, -1.32, 0.09], [4.19, -1.23, 0.17], [4.19, -1.13, 0.28], [4.19, -1.01, 0.45], [4.19, -0.88, 0.63], [4.19, -0.73, 0.86], [4.19, -0.55, 1.1], [4.19, -0.37, 1.32], [4.19, -0.18, 1.52], [4.19, 0.16, 1.77], [4.19, 0.31, 1.84], [4.19, 0.63, 1.9], [4.19, 0.94, 1.9], [4.19, 1.26, 1.88]]
  - [[5.21, -1.13, 0.05], [5.21, -1.01, 0.07], [5.21, -0.88, 0.12], [5.21, -0.73, 0.19], [5.21, -0.55, 0.32], [5.21, -0.37, 0.45], [5.21, -0.18, 0.6], [5.21, 0.16, 0.88], [5.21, 0.31, 1.01], [5.21, 0.63, 1.22], [5.21, 0.94, 1.34], [5.21, 1.26, 1.38]]
  - [[5.73, 1.98, 0.63], [5.73, 2.2, 0.63], [5.73, 2.22, 0.09]]
  - [[5.74, 2.0, 0.61], [5.74, 2.22, 0.61], [5.74, 2.24, 0.09]]
  - [[5.76, 2.0, 0.57], [5.76, 2.22, 0.57], [5.76, 2.24, 0.09]]
  - [[5.82, 2.02, 0.41], [5.82, 2.24, 0.41], [5.82, 2.26, 0.09]]
  - [[5.89, 2.04, 0.2], [5.89, 2.26, 0.2], [5.89, 2.28, 0.09]]
channel_wales_m: [[-6.62, 1.44, 1.52], [-5.33, 1.28, 1.37], [-4.36, 1.21, 1.29], [-2.91, 1.14, 1.22], [-1.45, 1.11, 1.19], [0.01, 1.13, 1.22], [1.37, 1.2, 1.29], [2.73, 1.34, 1.42], [4.19, 1.56, 1.64], [5.18, 1.75, 1.84], [5.96, 1.97, 2.06]]
floor_m: [[-5.33, -0.31, 0.29], [-4.36, -0.6, 0.56], [-2.91, -0.91, 0.85], [-1.45, -1.1, 1.04], [0.01, -1.19, 1.18], [1.37, -1.19, 1.22], [2.73, -1.06, 1.13], [4.19, -0.73, 0.85], [5.18, -0.36, 0.46]]
rabbet_m: [[-5.33, -1.75, 0.07], [-4.36, -1.71, 0.07], [-2.91, -1.64, 0.07], [-1.45, -1.58, 0.07], [0.01, -1.52, 0.07], [1.37, -1.45, 0.07], [2.73, -1.39, 0.07], [3.79, -1.34, 0.07], [4.16, -1.32, 0.07], [4.53, -1.27, 0.07], [4.89, -1.16, 0.07], [5.22, -0.98, 0.07], [5.51, -0.72, 0.07], [5.68, -0.38, 0.07], [5.77, -0.01, 0.07], [5.83, 0.37, 0.07], [5.86, 0.75, 0.07]]
form: {"stern": {"type": "raked", "knuckle_z_m": 0.92, "transom_hb_m": [0.78, 0.93], "round_up_m": 0.11}, "head": "none"}
marks: {"rail_m": "judged", "breadth_m": "judged", "keel_m": "stand-in", "stem_m": "judged", "stern_m": "judged", "wales_m": "judged", "section_m": "judged", "decks_m": "judged", "breadth_line_m": "judged", "sections_m": "judged", "channel_wales_m": "judged", "floor_m": "judged", "rabbet_m": "judged", "form.stern": "stand-in", "form.stern.knuckle_z_m": "stand-in", "form.stern.transom_hb_m": "judged", "form.stern.round_up_m": "stand-in", "form.head": "stand-in"}
```

The same with Steel's sloop, §5.7 as first written (§5.2), kept as a check: `UNDER_WATER = "steel"`
draws it. Every other key is as above:

```yaml
sections_m:   # [x, z, half-breadth], one station to a line: Steel's sloop, §5.7 as first written
  - [[-5.07, -0.79, 0.14], [-5.07, -0.52, 0.37], [-5.07, -0.33, 0.76], [-5.07, -0.22, 1.32], [-5.07, 0.16, 1.41], [-5.07, 0.31, 1.5], [-5.07, 0.63, 1.54], [-5.07, 0.94, 1.52]]
  - [[-4.57, -1.22, 0.24], [-4.57, -1.02, 0.41], [-4.57, -0.78, 0.72], [-4.57, -0.58, 1.12], [-4.57, -0.36, 1.5], [-4.57, 0.16, 1.58], [-4.57, 0.31, 1.64], [-4.57, 0.63, 1.65], [-4.57, 0.94, 1.63]]
  - [[-3.59, -1.41, 0.51], [-3.59, -1.25, 0.71], [-3.59, -1.04, 1.08], [-3.59, -0.81, 1.48], [-3.59, -0.52, 1.73], [-3.59, -0.14, 1.81], [-3.59, 0.16, 1.78], [-3.59, 0.31, 1.81], [-3.59, 0.63, 1.81], [-3.59, 0.94, 1.79], [-3.59, 1.26, 1.74]]
  - [[-2.63, -1.56, 0.72], [-2.63, -1.43, 0.95], [-2.63, -1.2, 1.33], [-2.63, -0.91, 1.67], [-2.63, -0.6, 1.86], [-2.63, -0.3, 1.91], [-2.63, 0.16, 1.94], [-2.63, 0.31, 1.95], [-2.63, 0.63, 1.95], [-2.63, 0.94, 1.92], [-2.63, 1.26, 1.87]]
  - [[-1.62, -1.66, 0.88], [-1.62, -1.56, 1.14], [-1.62, -1.33, 1.55], [-1.62, -0.99, 1.85], [-1.62, -0.66, 1.97], [-1.62, -0.39, 2.0], [-1.62, 0.16, 2.05], [-1.62, 0.31, 2.05], [-1.62, 0.63, 2.04], [-1.62, 0.94, 2.02], [-1.62, 1.26, 1.96]]
  - [[-0.65, -1.73, 1.0], [-0.65, -1.65, 1.28], [-0.65, -1.39, 1.67], [-0.65, -1.01, 1.93], [-0.65, -0.69, 2.05], [-0.65, -0.43, 2.05], [-0.65, 0.16, 2.1], [-0.65, 0.31, 2.11], [-0.65, 0.63, 2.09], [-0.65, 0.94, 2.07], [-0.65, 1.26, 2.02]]
  - [[0.36, -1.76, 1.08], [0.36, -1.68, 1.36], [0.36, -1.41, 1.75], [0.36, -1.01, 1.99], [0.36, -0.66, 2.07], [0.36, -0.42, 2.09], [0.36, 0.16, 2.14], [0.36, 0.31, 2.14], [0.36, 0.63, 2.13], [0.36, 0.94, 2.11], [0.36, 1.26, 2.06]]
  - [[1.37, -1.45, 0.09], [1.37, -1.32, 0.61], [1.37, -1.23, 1.02], [1.37, -1.13, 1.34], [1.37, -1.01, 1.63], [1.37, -0.88, 1.81], [1.37, -0.73, 1.95], [1.37, -0.55, 2.05], [1.37, -0.37, 2.11], [1.37, -0.18, 2.14], [1.37, 0.16, 2.15], [1.37, 0.31, 2.15], [1.37, 0.63, 2.15], [1.37, 0.94, 2.14], [1.37, 1.26, 2.09]]
  - [[2.21, -1.7, 1.11], [2.21, -1.62, 1.38], [2.21, -1.35, 1.78], [2.21, -0.95, 2.02], [2.21, -0.6, 2.09], [2.21, -0.28, 2.12], [2.21, 0.16, 2.12], [2.21, 0.31, 2.13], [2.21, 0.63, 2.12], [2.21, 0.94, 2.11], [2.21, 1.26, 2.07]]
  - [[3.21, -1.56, 1.0], [3.21, -1.47, 1.27], [3.21, -1.22, 1.67], [3.21, -0.83, 1.92], [3.21, -0.48, 2.0], [3.21, -0.12, 2.05], [3.21, 0.16, 2.03], [3.21, 0.31, 2.05], [3.21, 0.63, 2.07], [3.21, 0.94, 2.07], [3.21, 1.26, 2.03]]
  - [[4.19, -1.35, 0.81], [4.19, -1.23, 1.06], [4.19, -0.99, 1.44], [4.19, -0.63, 1.7], [4.19, -0.26, 1.81], [4.19, 0.16, 1.77], [4.19, 0.31, 1.84], [4.19, 0.63, 1.9], [4.19, 0.94, 1.9], [4.19, 1.26, 1.88]]
  - [[4.68, -1.13, 0.6], [4.68, -0.99, 0.82], [4.68, -0.77, 1.2], [4.68, -0.43, 1.47], [4.68, -0.05, 1.61], [4.68, 0.16, 1.41], [4.68, 0.31, 1.5], [4.68, 0.63, 1.63], [4.68, 0.94, 1.69], [4.68, 1.26, 1.7]]
  - [[5.17, -0.76, 0.21], [5.17, -0.61, 0.43], [5.17, -0.37, 0.73], [5.17, -0.07, 1.0], [5.17, 0.16, 0.89], [5.17, 0.31, 1.02], [5.17, 0.63, 1.23], [5.17, 0.94, 1.35], [5.17, 1.26, 1.38]]
  - [[5.73, 1.98, 0.63], [5.73, 2.2, 0.63], [5.73, 2.22, 0.09]]
  - [[5.74, 2.0, 0.61], [5.74, 2.22, 0.61], [5.74, 2.24, 0.09]]
  - [[5.76, 2.0, 0.57], [5.76, 2.22, 0.57], [5.76, 2.24, 0.09]]
  - [[5.82, 2.02, 0.41], [5.82, 2.24, 0.41], [5.82, 2.26, 0.09]]
  - [[5.89, 2.04, 0.2], [5.89, 2.26, 0.2], [5.89, 2.28, 0.09]]
```

So the water's ends stand at −6.10 and +6.09, her greatest half-breadth is 2.15 and the rail's lowest
1.41 at x −1.44.

- **The transom** (the builder's word, 2026-10-30). `transom_hb_m` is §5.7's 0.78 m at the plate's own
  size, and 0.93 m at the foot, not carried by `beam_ratio` (0.83 and 0.98 m if they were): §5.7 names
  the figure, the 5 cm is under principle 2's 2 px, and the two together keep the transom's own angle.
  This was first written 0.83 and 0.98. The plate's 0.78 stands at the rail's end, 1.76 m up at her
  size; the form has only a half-breadth at the taffrail and one at the knuckle, so the top is drawn
  flat across at the taffrail's height, its corners about 0.3 m above the plate's rounded arc (§4.14).
  No key carries that arc: recorded.
- **The counter's breadth under the transom** (the review's word, 2026-10-30). The plate's counter
  stands about 1.2 m out at her size from z 0.38 m up to the transom's foot (§4.14), a broad rounded
  surface over a narrow post. The form closes the side to the stern's line below the knuckle, so the
  drawn side at the wale's after end stands 0.36 m out, and on the quarter the transom reads as a box
  on a neck. Together with the flat top that is the one place her hull does not read as the plate. Two
  sections were tried at the post, x −18.40 and −19.22, from the counter's outline and the plan: they
  put the breadth there, and they tear the wale, a band being drawn straight from station to station
  on so hard a turn, with no gain to the eye (`look_a.png`, §8). So they are not kept, and the
  points are in §4.14. For the lead, with the arc: a key for the counter, or the viewer's band on a
  hard turn.
- **The bow** (the builder's word, 2026-10-30). The rail ends at the stem head's after edge, as §5
  has it. Drawn so with the rail's half-breadth, the head stood up as a block 1.2 m across from ahead,
  where the plate's is a timber 0.18 m across. So from the rail's stop forward the top of the side in
  `breadth_m` is the head's half-siding (§4.6), and `sections_m` carries the rail on along it: at each
  station the plumb side 0.70 ft under the rail, the rail's top, and the head's side stepping in 0.06
  ft above it (the step is the drawing's). `breadth_m` takes one more point, at the rail's x 17.43, so
  that the drawn side at that rail point is held to the plan.
- **The frame** stays the keel's. Laid over the plate turned level with the water, the stem head
  stands about 0.12 m forward of it and the taffrail 0.09 m, 3 to 4 px on the owner's picture, and the
  outline reads the same; a station cannot lean in the form. So the pictures do not ask for §0's turn
  (judgement).

- **The side above the water** (the review's word, 2026-10-30). As first built, the sloop's body drew the
  side above the water by the design's rule, up to 0.17 m inside the plate's frames near the ends,
  where the plate's own body plan reads it at the same rung; `Build-Ships.md` §5.0 principle 5 has
  sourced points win. A station given any point of its own is carried from no other (`form.py`), so the
  frames go at the sloop's timbers: as read at F, where a timber falls on the station, else straight
  between the two frames either side at each height both reach, moved by how far the plan's water and
  rail stand off the straight there (arithmetic). The plate's stations are then carried from those
  above the water and below it, as they were. The two bodies now differ by an rms of 0.016 m above the
  water, by 0.025 m at most within 5 m of the middle, and by 0.07 m at most at 14 and H; the sloop's body
  stands within an rms of 0.023 m of the frames there. So the lead's ruling moved what is under the
  water and nothing the eye sees above it. The sloop's figures under the water and its 53 t are as they
  were.

No `ports_m`, `port_size_m`, `head_m`, `galleries_m` or `lights_m` (§4.16). `decks_m.upper` joins the
after deck's fore end to the fore deck's after end straight across the waist, where no deck line is
drawn (judgement, so `judged`; §4.4). The other way to write it is the after deck under another deck
word and the waist open; none of `DECK_WORDS` fits it, and a flush line draws the less that is not
read (judgement).

**The generator's report:** every line in its schema's order, no refusal; `form.check` passed, each
given point drawn through. Drawn displacement 38 t against the filed 46 t (−18%, more than 15% off) on
the plate's frames, as ruled: reported past the line, not moved; 53 t (+15%) on the sloop, the first
build. Drawn 1.45 m deep to the
rabbet at the greatest section (x 1.37); the keel's lower edge there is 1.73 m down, and 1.78 m at the
middle on the file's rounded points (1.79 m by the plate's own figure, first written so), against the
file's 1.9 m (§6).

## 6. Against `data/ships/smack.yaml` (recorded, not moved)

| Field | The file (its note) | The plate (at its own size) |
|---|---|---|
| `length_waterline_m` | 12.2 (40 ft, judgement between the *Culloden*'s keel and gun deck) | 11.46 m (37.6 English ft) on the LWL; 11.61 m between the perpendiculars |
| `beam_m` | 4.3 (14 ft, Charnock) | 4.06 m moulded (13.3 English ft) |
| `draught_m` | 1.9 (6.25 ft mean; 7.0 aft, 5.5 forward, judgement; the note gives Chapman's draught as 6.3 ft) | 1.69 m mean; 1.95 m aft, 1.43 m forward (5.5, 6.4 and 4.7 English ft) |
| `deck_height_m` | 0.75 (2 ft 6 in, judgement) | the after deck 0.74 to 0.78 m at side; the fore deck 0.91 to 0.94 m amidships, 1.00 m at ⊕ |
| The rail above the water | — | 1.33 m at its lowest, 1.66 m at the transom, 2.15 m at the stem |
| `main.shrouds` | 3 shrouds a side (judgement) | three deadeyes a side (§4.8) |
| `displacement_kg` | 46,000 (Cb 0.45, judgement) | as drawn at her length and beam, 38 t (−18%) on the plate's frames, as ruled; 53 t (+15%) on the sloop, her first build (§5.3) |
| `draught_m` at her beam | 1.9 mean; 7.0 ft (2.13 m) aft, 5.5 ft (1.68 m) forward | 1.79 m mean; 2.06 m aft, 1.51 m forward, drawn |
| `deck_height_m` at her beam | 0.75 | the after deck 0.78 to 0.82 m at side; the fore deck 0.96 to 1.00 m amidships, drawn |
| `main.mast` `x_m` | +1.8 | not drawn; the chains put it at 1.6 to 2.1 m on the plate, 1.7 to 2.2 m at her length (§4.15) |
| `bowsprit` `x_m`, heel | +6.4; heel +3.84 | the stem head +6.15 at her length; the post of §4.8 +4.09 (§4.15) |
| `bowsprit` `height_m` | 1.0 above the datum, its end 1.75 m above the water | the viewer roots its heel at the stem head (`Build-Ships.md` §6), 2.60 m up at the rail's stop, and the spar runs level from there, its end drawn 0.85 m above the file's; the post of §4.8 is notched at 2.37 m at her size, so a spar about that height is what the plate shows (judgement). Drawn only |
| The head sails' tack, in `sails` | 1.31 m above the water at x 5.9 | under the rail there, 2.2 m; drawn so on old and new alike, and now over the side at the bow. Recorded, not moved |

The plate's vessel is about 5 to 6% shorter and narrower than the file's, and draws 11% less
at the mean. These are for the lead and the owner. Stage 0 moves no figure, and neither does the
hull step: nothing the physics or the gunnery reads moves (`Build-Ships.md` §5.0 principle 8, §5.6).

## 7. What the source cannot give

- **Port sills and port sizes**: no ports and no guns on No. 3.
- **The deck in the waist**, from 14.3 to 6.0 ft abaft the middle: no deck line is drawn
  there, and the dashed outline over it is not identified (§4.4).
- **Frames abaft 14 and forward of H**: the ends are given by the plan's lines and the stern's
  outlines (§4.6, §4.14), not by frames.
- **A wing transom, a tuck's flat, lights or galleries**: none drawn (§4.14, §4.16).
- **The floor's own half-breadth**: no rising half-breadth is drawn; the diagonal stands for it
  (§4.13).
- **The plank**: every line is moulded; the outside of the plank is not drawn.
- **The mast and spars of No. 3**: none drawn, unless the dashed post of §4.8 is the mast's
  stump; the channel and its three deadeyes are the only rigging.
- **The stated dimensions' own text**: the 1768 explanation was not seen; the three figures are
  those read from the 1971 edition (`VesselReferences-2026-10.md:315`). That the 6½ is the
  after draught is judgement on the measure (§2.3); the mean is 5.68.
- **A square plate**: the measured photograph reads 3% short up the page (§2.2); whether the paper
  does too is open. The factor rests on three stations of one breadth, on the stated draught and on
  the second photograph's heights at its own bar.
- **The transom's arc in the file**: the plate reads it (§4.14), and the form has no key for it (§5.3).
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

The second reading (2026-10-30), in the scratch directory under `hulls/streams/smack/`: `lib.py`
(§2's frame, kept to the first reading's anchors, whose Lpp and draughts it reproduces to 0.01 ft),
`follow.py` (a line followed by its darkness ridge), `peaks.py`, `plan2.py` and `plan_cols.py` (the
plan's lines beside each station's own line), `stline.py` (the station lines), `body.py` and
`sect.py` (the frames, followed, overlaid and reduced), `sections_out.py`, `heads.py`, `marks.py`
(the body plan's marks and base), `prof2.py` (the water lines, the heavy curve, the counter), `rab.py`
(the rabbet), `diag.py` (the diagonals), `final.py` and `points.py` (the reduction), `img2.py` to
`img2g.py` (the checker on `022uK3KjAwHr`), `steel_cmp.py` (Steel's rows through the helper) and
`dry.py` (the file's block through the helpers, from this tree, writing nothing). The Steel leaves
were read on `elementspractice00stee_0486_full.jpg`, `_0489.jp2` and `_0589.jp2`. The images stay in
the reference cache; the Cooke etching was not used for any figure (`Build-Ships.md` §5.8).

The independent reading (2026-10-30) is under `hulls/streams/smack/check/`. The build (2026-10-30) is
under `hulls/streams/smack/build/`: `ends.py` (the second band's ends and the plan's rail on to the
head, by `lib.py`'s frame), `blocks.py` (§5.3's blocks, from the module), `gen_variant.py` (a file of
the other body, in scratch), `states.py`, `sheets.py`, `sheet04.py` and `crops.py` (the game's own viewer
in headless Chrome, on her states as the game sailed them, beside the plate's crops). The sheets are
under `hulls/streams/smack/sheets/`; a crop of the plate stays in scratch.

The review (2026-10-30) is under `hulls/streams/smack/review/`: `ov.py` (her drawn outlines laid over
the profile, the plan and the body plan by `lib.py`'s frame and the frames' registration), `wl.py`,
`wl2.py` and `wl3.py` (the plan's lines between stations and at the post, on both photographs),
`wale.py` (the wale's after end), `cmp1.py` and `facts.py` (the two bodies against each other, the
sloop's feet, the figures of §5.2 and §5.3), `quarter_try.py` and `look.py` (the counter's sections
tried, and her ends close by the game's viewer).
