# Research note: the corvette *Diana*, the Danish light frigate of 1804 kept by Spain (November 2026)

Package 90's preliminary work (the lead's note of 2026-11-18, nudge 15, `docs/dev/M7-WorkPackages.md`):
research and planning only, no code, no ship file. This is the note the design for her
(`docs/design/Design-Ship-Diana.md`, second draft of 2026-11-18) works from, in the form of
`Research-Bilander-2026-10.md`. The owner's settling of 2026-11-06 binds and is not reopened
here: **the Danish frigate *Diana* built in 1804, taken at Cartagena with the declaration of war
and kept by the Spanish navy to 1832, Winfield p. 930; her three fits dated (twenty 24-pounder
carronades as captured, twenty 30-pounder carronades as first rearmed, and on 31 October 1817
twelve 12-pounders, eight 30-pounder carronades and four 3-pounder obuses); her plan the Spanish
navy's own of 1809-1810, held in the tree.** One source found here disagrees with the first fit
(§4, §8): it is set down for the owner, not acted on.

**The ladder** (Build-Ships.md §5.0 principle 3; the lead's words in the brief): **rung A** her own
original plans (§5.0's S), **rung B** a historian's or a period writer's particular of her (a
figure of hers that is not her drawing), **rung C** judgement, marked **JUDGEMENT**, including a
named period rule applied to her particulars (§5.0's R) and a type's figure carried to her (§5.0's
S† or T, said which). A source on file but unread is no rung.

**The marks**, as each fact was found (never upgraded):
- **read**: the page, image or code was seen. **read (OCR)** where only the text layer was seen.
- **measured**: off an image, with the image, the scale and the uncertainty given.
- **observed**: printed by a scratch probe run on the engine (the scripts in the session's scratch,
  `scratchpad/p90/diana/probe/`, not filed; nothing in the tree was changed by them).
- **catalogue**, **secondary**, **memory**, **judgement**: as they say.

**Units.** Her Spanish figures are in **pies de Burgos**. Winfield's metres for her row (34.55 by
9.06 by 4.46 m on 124 ft by 32 ft 6 in by 16 ft) give 0.27863 to 0.27877 m a pie, the pie of a
third of the vara de Burgos (0.835905 m, memory: 0.278635 m); `VesselReferences-2026-11-Spanish.md`
and the tree's tide notes hold 0.2786 m. The game's constants are **Winfield's metres** where the book
gives one, as the lead ruled; a measured figure of this note is converted at **0.278635 m** (the
two differ by 0.01%). A pulgada is a twelfth of a pie (0.02322 m). The **libra castellana** is
0.4601 kg and the **tonelada** of the plan's table is 2,000 libras (proved by the table's own carry,
§2.3), 920.2 kg (the libra memory). The **Danish pund** of her guns is about 0.50 kg (memory,
unverified). An English foot is 0.3048 m. Nothing in this note reads a Spanish foot as an English
one.

**In short.**

- **Her lines are held at rung A.** The Spanish plan (`docs/references/images/corvette-diana-1809-plano-bvmdefensa.jpg`,
  CC BY 4.0) is a sheer with the inboard works in red, a body plan, a half-breadth and a table. Its
  own scale bar of 32 divisions, the body plan's frame of 32 pies 6 pulgadas and the length of 124
  pies agree on **11.40 px a pie (±0.5%)**: 1 px is 2.44 cm of her.
- **The table on the sheet is Winfield's row**: eslora 124 pies, manga 32 pies 6 pulgadas, puntal
  16 pies (read), so Winfield's 124 ft by 32 ft 6 in by 16 ft is this sheet's, in pies de Burgos.
  It adds her **displacement, 540 toneladas 691 libras, about 497 t** (read; the forebody 281 t,
  the afterbody 258 t), which no other source gives.
- **She floats at the line the sheet marks with an arrow**, level, 3.19 m above the rabbet:
  **draught 3.57 m (12 pies 9¾ pulgadas) to the keel's lower edge on an even keel**, her gun deck
  1.40 m above the water at midships, her port sills 1.78 m, her waist rail 2.69 m (measured;
  the line's meaning JUDGEMENT, checked against the displacement table: §2.4).
- **Eleven ports a side**: ten broadside ports evenly spaced at 2.87 m and a bow port, on one flush
  deck under a bulwark with hammock nettings above it; a small square opening between each pair
  of ports, read as sweep ports (JUDGEMENT).
- **Her masts** stand on the plan at x +12.47 m (the fore, plumb), −2.31 m (the main, raked about
  5° aft) and −11.40 m (the mizen, about 5½° aft) from the middle of her waterline; the plan
  draws only their stumps, so **her spars are rung C**: Luce's chain (the generator's own rule for
  the frigate) on her particulars, Falconer's yard rule and Chapman's the checks.
- **A Danish source is read** (rung B): Carl Roos, 1957, from her own papers (the log in four
  folio volumes, the provision journal, the captain's order book). She was built in 1804 at
  Bodenhoff's yard in Copenhagen, a "let fregat" (light frigate) with her guns on **one half-open
  deck**; **her Danish armament was four 8-pounder long guns and sixteen 30-pounder carronades**,
  her war establishment 120, with 161 aboard when she sailed in July 1807 (Roos pp. 90, 94-95).
  This differs from Winfield's "twenty 24-pounder carronades as captured" (§8; the owner's).
- **Her captain's own report of her** (Captain Meyer, 1809, after the seizure; Roos p. 94): she
  carried her sail superbly, was stiff, steered splendidly and rode easily at anchor; her best
  speed **10 to 11 (Danish) miles in the four-hour watch with the wind 2 to 3 points free, a
  freshening breeze from a stiff topgallant breeze to double-reefed topsails**: 10 to 11 knots.
- **The engine sails her today as it sails the frigate**: a ship rig of three square masts, no
  lateen, no schooner's mast. Built in memory from the frigate's file by Luce's rule on her
  particulars, she makes 2-4% less than the frigate on every point, 10.6 knots at 118° in 25
  knots of wind (Meyer's 10-11), tacks in 349 to 379 s (one tack of 164 s, under truth 10's
  floor), wears in 491 s and heaves to as the frigate does (observed, §7). **With the frigate's
  metacentric height scaled by her breadth (1.0 m) she heels 1.7 times the frigate** (19° on a beam
  reach in 22 knots), which Meyer's "stiff" refutes; 1.5 to 1.8 m brings her to the frigate's heel.

## 0. The sources

**Held in the repository:**

| Short form | Work | Rung and standing | What it gives here |
|---|---|---|---|
| The plan | "Plano de la Corbeta de Guerra la Diana, del porte de 20 Carronadas de á 30, mandada por el Teniente de Navío de la R.l Armada D.n José de Julián por los años de 1809 y 1810": `docs/references/images/corvette-diana-1809-plano-bvmdefensa.jpg` (2000 × 705 px) | **A**; CC BY 4.0, "Fuente: Archivo Histórico de la Armada Juan Sebastián de Elcano / Biblioteca Virtual de Defensa" (the images README) | Her lines, her deck, her ports, her masts' places and rakes, her displacement and her dimensions in pies (§2) |
| Winfield | Winfield and others, *Spanish Warships in the Age of Sail 1700-1860*, Seaforth 2023, p. 930, as set down in `VesselReferences-2026-11-Spanish.md` §5 (the book is not in the tree; the owner's) | **B**; in copyright, facts cited by page | Her row (124 × 32½ × 16 ft, 34.55 × 9.06 × 4.46 m, 335 t, 167 men), her three fits by date, built 1804, taken at Cartagena, last mentioned 1832 |
| Babron 1817 | J. B. A. Babron, *Précis des pratiques de l'art naval, en France, en Espagne et en Angleterre*, Brest 1817 (`docs/references/signals/babron-1817-precis-des-pratiques-de-l-art-naval-ocr.txt`) | **C** (a period table of the Spanish navy's practice, carried to her as a check); public domain | The Spanish rakes of a frigate of 18 and a brig-rigged corvette of 18 (pp. 86-87, OCR l. 7612-7640, read (OCR)) |
| Chapman 1781 | F. H. af Chapman, *Traité de la construction des vaisseaux*, 1781 (`chapman/...-ocr.txt`) | **C** (a named rule); public domain | Ch. VIII §30 (pp. 98-100, OCR l. 11601-11724, read (OCR)): the main yard of a frigate-built merchant ship 0.52 of the length from stem to post; the mizen's centre 0.181 of the length from the post; the mast rakes and the bowsprit's steeve |
| Falconer 1780 | *An Universal Dictionary of the Marine*, art. YARD (`falconer/...-ocr.txt`) | **C**; public domain | The main yard 0.575 of the gun-deck length for ships below 44 guns (the generator's module docstring, `tools/gen_ships.py` l. 45-48, read) |
| Luce 1866 | S. B. Luce, *Seamanship*, ch. VII (`luce/...-ocr.txt`) as the generator applies it (`tools/gen_ships.py` l. 49-63 and `frigate()` l. 2235-2280, read) | **C** (a named rule; later than the period, the generator's chain for the frigate) | Every spar in proportion to the main mast, (LWL + extreme breadth) / 2 |
| Steel 1794 | *The Elements and Practice of Rigging and Seamanship*, vol. I, "Dimensions of Masts and Yards in the Royal Navy" (pp. 49-50), the "20 Guns" column (`steel/...-vol1-ocr.txt` l. 5208-5240 and 5245 onward) | **unread**: the OCR of the table is not legible; no rung until the page image is read | A British 20-gun ship's masts and yards, the check on Luce for her rig (the builder's step 1, §9) |

**Read online, not held:**

| Short form | Work | Rung and standing | Where |
|---|---|---|---|
| Roos 1957 | Carl Roos, "Orlogsfregatten DIANA og dens besætning under krigen med England 1807-14", *Handels- og Søfartsmuseets årbog* (M/S Museet for Søfarts årbog) vol. 16, 1957, pp. 87-138 | **B**: a historian's reading of her own papers (the log, the provision journal, the order book; p. 88) with her captain's report and three pictures of her; a work of 1957, taken as in copyright: facts by page, one short quotation of her captain's report of 1809 | tidsskrift.dk, *M/S Museet for Søfarts årbog*, article 96105 (published online 2017; the page states no licence). The PDF's page images read (the text layer is OCR and was checked against the page image on p. 94); a copy is in the session's scratch, not in the tree |
| The record | Biblioteca Virtual de Defensa, record 1037832 | catalogue | Shelfmark PB-021, Archivo Histórico de la Armada Juan Sebastián de Elcano; "1 plano: manuscrito; 38 x 107 cm"; the note "cálculo del desplazamiento y dimensiones principales en el ángulo inferior derecho"; the date "1809-1810"; CC BY 4.0 on the condition the source is named (read on the record's page, 2026-11-17) |
| Wikipedia | "HDMS Diana (1804)" | secondary, not used for a figure | Its one source is Roos 1957; its "left Copenhagen on 7 July" is Roos's hoisting of command on the 6th and weighing on the 17th misread (§1) |

**Pictures of her, for the eye only** (Build-Ships.md §5.8: a check for the eye, never a source
of points, holding no rung; reproduced in Roos 1957, read on its page images; none is held):

| | What | Artist, date, where |
|---|---|---|
| Roos fig. 2 (p. 95) | "Fortuning af Fregatten Diana, under Seil i Spanske Søen": a sketch of her under sail in the Spanish sea | Hans Bertel Riber (1789-1850), her third mate, 1807, in the third mate's cipher book ("Ciffre-Bog") |
| Roos fig. 3 (p. 101) | "Diana. Kongelig Dansk Fregat": under all plain sail, Danish ensign at the gaff and pendant; its caption gives her guns (16 × 30-pdr carronades, 4 × 8-pdr guns), her 120 men "prima Plan", Captain Meyer, from Algiers to Cartagena 18 September 1807, taken in that harbour 26 September 1809 by "the Spanish insurgents" | Coloured drawing signed "Thomsen pinx 1809" (perhaps her officer of that name, Roos), Det Nationalhistoriske Museum på Frederiksborg, inv. no. 3561 |
| Roos fig. 4 (p. 105) | Her entering Cartagena under salute, September 1807, the Spanish guardship *San Sebastián* inside | Gouache by N. J. Pedersen (perhaps one of her people of that name), 26.7 × 39.4 cm, Handels- og Søfartsmuseet |

**Not reached:**
- **Her Danish draught.** Roos p. 94 cites "konstruktionstegningen" (the construction drawing),
  which speaks of "kulen" (the waist). It is her as built, rung A beside the Spanish plan. Where it
  is now was not found (the Danish naval drawings are in the National Archives, Rigsarkivet, or the
  former Orlogsmuseet's collection: memory). Whom to ask: §9.
- **navalhistory.dk**, the Danish naval history site's ship pages (503 on 2026-11-17).
- **A larger image of the plan**: the record serves its pages through a viewer (two image groups,
  350668 and 350671); the tree's 2000-px file is the only one read.
- **Spanish sources of her service** (O'Scanlan 1831 for the words; the Museo Naval; the archive's
  other records of her): not searched beyond one query.

## 1. Her history, by source

| Date | What | Source and mark |
|---|---|---|
| 1804 | Built at Bodenhoff's yard ("Bodenhoffs Plads"), Copenhagen; "a light frigate" carrying her guns on one half-open deck | Roos p. 94, read; Winfield p. 930 ("built 1804") |
| 6 and 17 July 1807 | Captain-lieutenant Christian Nicolai Meyer hoists command and warps her out; she weighs on the 17th, to relieve the frigate *Fylla* in the Danish West Indies, by way of Algiers with the Dey's tribute | Roos p. 87, read |
| 1 and 7 September 1807 | At Málaga; at anchor in Algiers roads | Roos p. 87, read |
| 12 to 17 September 1807 | Bound for Málaga; between Cape Gata and Cape Palos a heavy swell springs her bowsprit two feet outside the gammoning; on the 17th, 6 (Danish) miles to windward of Cartagena, a British frigate of 44 guns that had chased her for 24 hours and carried away her main topgallant mast in it comes up under her lee; Meyer takes in the courses and staysails, clears for action and lies to; a British officer tells them of the war and the fall of Copenhagen; she bears up for Cartagena, the British ship following under her three topsails | Roos pp. 98-100, read |
| 18 September 1807 | Into Cartagena (the 1809 drawing's caption), never to leave it under Danish colours | Roos pp. 87, 101, read |
| 26 September 1809 | Seized by the Spanish (the Junta at war with Denmark after Spain's alliance with Britain of July 1809); her people prisoners of war; 87 left of her 161 | Roos pp. 87, 90, read; Winfield p. 930 ("taken at Cartagena with the declaration of war") |
| 1809 and 1810 | The Spanish navy's "corbeta de guerra la Diana, del porte de 20 carronadas de á 30", commanded by Teniente de Navío José de Julián; her plan drawn | The plan, read |
| November 1810 | Sails under Spanish colours across the Atlantic for South America | Roos p. 87, read |
| 31 October 1817 | Armed with 12 × 12-pdr, 8 × 30-pdr carronades and 4 × 3-pdr obuses | Winfield p. 930 (VesselReferences §5) |
| 1832 | Last mentioned | Winfield p. 930 |

## 2. Her hull: the Spanish plan read and measured

### 2.1 The sheet

Sheer plan with the inboard works in red (the decks, the hatches, the masts below the deck and
their steps, the pillars, the bowsprit inboard), the body plan to the right (the after body on the
left half, the fore body on the right, the diagonals in red), the half-breadth plan under the sheer,
a scale bar and the table at the lower right (read). The stations are numbered on the keel: aft 11
to 1, three midship frames "m", fore 1 to 11, every 51.1 px (4.49 pies, 1.25 m; measured). The masts
are drawn as stumps that end under the title; the bowsprit is drawn short; no sail, yard or rigging
but the chains and deadeyes is drawn (read).

### 2.2 The scale (measured)

| Measure | Pixels | Pies | px a pie |
|---|---|---|---|
| The scale bar: 32 divisions, lines found at 1591.0 to 1955.5 | 364.5 | 32 (judgement: the divisions are pies; the left one carries a diagonal for pulgadas) | 11.39 |
| The body plan's frame, the extreme breadth (x 1587 to 1958) | 371 | 32½ (the table's manga) | 11.42 |
| The gun deck from the post's after face (x 110) to the stem's fore face (x 1530) | 1,420 | 124 (the table's eslora, if that is its measure: judgement) | 11.45 |

**Taken: 11.40 px a pie**, 0.02444 m a pixel, ±0.5% between the three. A point is read to ±2 px
(±5 cm) where the line is clear, ±5 px where it is crowded (the stern, the forefoot). The sheet is
1:46 if the catalogue's 107 cm is the image's width (judgement; no scale is written on the sheet).

### 2.3 The table against Winfield (read; measured where marked)

| The table ("Cálculo del Desplazamiento"; "Dimensiones Principales") | Pies de Burgos or toneladas | Metres or tonnes | Winfield p. 930 |
|---|---|---|---|
| Eslora | 124 pies 0 | 34.55 | 124 ft (34.55 m) |
| Manga | 32 pies 6 pulgadas | 9.06 | 32 ft 6 in (9.06 m) |
| Puntal | 16 pies 0 | 4.46 | 16 ft (4.46 m) |
| Cuerpo de proa (the fore body) | 281 t 1,462 lb | 259.2 t | — |
| Ídem de popa (the after body) | 258 t 1,229 lb | 238.0 t | — |
| Diferencia | 23 t 233 lb | 21.3 t | — |
| Total | **540 t 691 lb** | **497.2 t** | 335 t (a burthen or arqueo, not this) |

- The libras' last digits are blurred at this resolution; the fore body's "1,462" is read with its
  hundreds digit 4 because only that makes the table's own difference (23 t 233 lb) and total
  (540 t 691 lb) hold, and the carry of 2,691 libras to 1 tonelada 691 proves the tonelada of 2,000
  libras (read; arithmetic, judgement). The toneladas are certain.
- **The table is Winfield's row** (Winfield's three figures are the sheet's, in pies). Winfield's 335 t is not
  the displacement; it is a tonnage of another rule (arqueo or a Danish lästing; to ask: §11).
- **The definitions** (judgement, to confirm with a Spanish source): the eslora is matched within
  0.5% by the gun deck from the post's after face to the stem's fore face (§2.2); the puntal of 16
  pies is matched by the rabbet (image y 441.5) to the underside of the gun deck's beams (y about
  259), the deck's surface at side standing at y 253.5 (§2.5).

### 2.4 The load line and the displacement

The sheet marks one line with an arrowhead outside the stem, pointing at the body plan (image y
310 at x 1572). In the sheer it is a thin level line at y 311 ±2, seen clear at the stern (x 200)
and forward (x 1150, 1420) and lost in the middle in the main wale's lower edge, which lies at y
307 there (measured). **It is taken as her load line** (JUDGEMENT on the arrow's meaning; no word
on the sheet names it). Above the rabbet it stands 130.5 px, 11.45 pies, **3.19 m**; the keel's
lower edge is 15.5 px under the rabbet (0.38 m; the line at y 457; a line at y 462 is read as the
half-breadth plan's middle line, judgement). **Her draught is 3.57 m (12.8 pies, 11.7 English ft),
even keel**: the keel is level on the sheet (y 440 to 442 from x 160 to 1460, measured), so the
drawing floats her without drag.

**The check against the table.** The midship section was traced on the body plan's fore half
(measured; the half-breadths in §2.6): its area under the line is 251 square pies, its midship
coefficient 0.67, a sharp rising floor with about 21° of deadrise. The table's 497.2 t is 484.6 m³
of sea water, 470.5 m³ without 3% for the keel and plank (judgement), 21,750 cubic pies; on the
line's length between the rabbets (1,373 px, 120.5 pies) and the breadth at the line (32.4 pies)
that is a **block coefficient of 0.48 and a prismatic of 0.72** (arithmetic). A sharp midship
section (0.67) with three identical midship frames and full ends gives a high prismatic for a low
block (judgement), so the arrow's line and the table agree. **This is a check, not a proof**: a line
an English foot higher would need a prismatic of about 0.63 on the same section, nearer a frigate's
usual figure, and only the drawn volume itself, the sections integrated to the line, decides between
them. That is the builder's first measuring task (Design §3.6 task 2), as Research-74's §3.5 did for
the 74.

**Her waterline**: 1,407 px from the post's after face (x 123) to the stem's fore face (x 1530) at
the line, **34.39 m**; 1,373 px between the rabbets, 33.56 m (measured).

### 2.5 The profile (measured; x forward of the middle of the waterline, image x 826.5; z above the line, image y 311)

| Feature | Points (x m, z m) | Note |
|---|---|---|
| The waist rail, the top of the bulwark | (−18.25, 3.52), (−16.78, 3.50), (−15.31, 3.35), (−12.87, 3.13), (−10.42, 2.96), (−7.98, 2.84), (−5.54, 2.74), (−3.09, 2.74), (−0.65, 2.69), (1.80, 2.69), (4.24, 2.69), (6.68, 2.74), (9.13, 2.81), (11.57, 2.88), (13.53, 3.01), (16.46, 3.01), (17.44, 3.10) | Traced on the second dark line from the top (y 201 at midships); a flush rail, no step for a quarterdeck or forecastle |
| The hammock rail above it | (−18.73, 4.23) the taffrail's top, (−15.31, 3.89), (−12.87, 3.67), (−10.42, 3.50), (−7.98, 3.40), (−5.54, 3.28), (−3.09, 3.20), (−1.14, 3.18), (1.80, 3.23), (4.24, 3.23), (6.68, 3.28), (9.13, 3.35), (11.57, 3.40), (14.01, 3.59), (15.48, 3.74), (17.44, 3.79) | The top line (y 179 at midships), with vertical stanchions to the bulwark below it: read as the hammock netting's rail (JUDGEMENT) |
| The gun deck at side (the red line) | (−16.78, 2.08), (−15.31, 1.91), (−12.87, 1.78), (−10.42, 1.66), (−7.98, 1.54), (−5.54, 1.49), (−3.09, 1.44), (−0.65, 1.39), (1.80, 1.39), (4.24, 1.42), (6.68, 1.44), (9.13, 1.44), (11.57, 1.54), (14.01, 1.59), (15.97, 1.69) | Taken as the deck at side (judgement: the red line may be the middle line; the camber is not drawn) |
| The lower deck (berth deck, red) | z −0.17 to 0.0 from x −15 to +7 | Her people's deck at the waterline; no gun on it |
| The main wale | lower edge z 0.10 at midships, 0.95 at the bow (x 17), 0.81 at the stern (x −17.8); upper edge 0.95, 1.22 and 1.47 | The wale's lower edge 10 cm above the line at midships |
| The keel | rabbet z −3.19, lower edge −3.57, level from x −16.6 to +15.2 | Image y 441.5 and 457 |
| The stern post | after face (−17.20, 0.0) at the line, (−16.59, −3.57) at the keel, (−17.71, 3.21) at its head; raked 9.4° | The rudder's pintles drawn on it |
| The counter and taffrail | From the post's head about 1.0 m aft and up to the taffrail at (−18.73, 4.23) | A square stern; her name is read on the transom of the 1807 gouache (Roos p. 94) |
| The stem | fore face (17.20, 0.0) at the line, nearly upright above it to the head, (17.33, 4.91) at its top; the forefoot meeting the keel about x +15.2 (±0.5) | |
| The head | A knee with two head rails forward to about x +18.7, z 2.4 to 3.3; no figure drawn | |
| Hawse holes | Two, (16.70, 2.35) and (16.90, 2.35) | |
| The rudder | About 0.68 m from the post at the line to 1.0 m at the heel: about 3.0 m² under the line | ±0.3 m² |

### 2.6 The midship section (measured on the body plan's fore half; z above the line, half-breadth outside the plank)

| z (m) | −3.20 | −3.11 | −2.96 | −2.81 | −2.67 | −2.37 | −2.08 | −1.79 | −1.49 | −1.20 | −0.91 | −0.61 | −0.32 | 0.0 | +2.6 |
| half-breadth (m) | 0.13 | 0.25 | 0.54 | 0.86 | 1.25 | 1.98 | 2.67 | 3.28 | 3.72 | 4.04 | 4.26 | 4.40 | 4.44 | 4.51 | 4.45 |

The greatest half-breadth 4.53 m (the manga's half) lies just above the line; the side is nearly
upright from there to the rail, with a few centimetres of tumblehome (measured, ±5 cm). The body
plan's after sections are deeply hollow at the garboard (read).

### 2.7 The ports (measured; image ports' bottoms traced; z of the sill above the line)

| Port (aft to fore) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 (bow) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| x (m) | −13.46 | −10.69 | −7.78 | −4.84 | −2.11 | +0.76 | +3.63 | +6.53 | +9.30 | +12.25 | +16.07 |
| sill (m) | 2.33 | 2.11 | 1.98 | 1.87 | 1.81 | 1.78 | 1.78 | 1.83 | 1.91 | 2.04 | 2.33 |

- **Each port about 0.87 m wide and 0.66 m deep** (35½ by 27 px; 3.1 by 2.4 pies). The ten
  broadside ports are 2.87 m apart (117.2 px, 10.3 pies); the bow port 3.8 m beyond the tenth.
- **Sill above the deck**: 0.37 to 0.45 m on the red line (judgement: low for a carronade's slide;
  if the red line is the deck at the middle line the sills stand about 0.15 m higher above the deck
  at side). Above the water at midships **1.78 m**; with the half-breadth there of 4.46 m the
  midship lee port **dips at about 21.8° of heel** (arithmetic).
- **Ports for twenty guns**: ten a side for the "20 carronadas", the bow port a chase or bridle port
  (judgement).
- **Between each pair of ports a small square opening**, about 0.25 m, its foot level with the
  sills (five forward of the main and two or three abaft it, measured). Read as **sweep ports**
  (JUDGEMENT; small men-of-war of the period were often pierced for sweeps between their guns,
  memory, unverified for her), not as scuttles for the berth deck, which lies below the gun deck
  (read). The Danish draught would settle it.

### 2.8 The masts, the bowsprit and the deck (measured)

| | At the deck, x (m) | Rake aft | Heel (z m) | Checks |
|---|---|---|---|---|
| Fore | +12.47 | 0° ±1° | −1.69 | Babron's Spanish corvette 1.1°, frigate 1.6°; Chapman: plumb |
| Main | −2.31 | about 5° ±2° (the drawn outline is woolded and uncertain) | −2.10 | Babron's corvette 6.2°, frigate 4.4°; Chapman 1 in 30, 1.9° |
| Mizen | −11.40 | about 5½° ±1½° | −1.69 | Chapman twice the main's; Chapman's mizen at 0.181 of the length from the post gives 22.4 pies against her 21.9 |

- The fore stands 4.72 m abaft the stem's fore face at the deck, the main 14.78 m abaft the fore,
  the mizen 9.09 m abaft the main and 6.11 m before the post (measured).
- **The bowsprit** steeves about 21° (±2°; Babron's Spanish corvette 17.3°, frigate 30.2°;
  Chapman 4 in 7, 29.7°). Its heel runs down inboard to the bitts about x +13.5.
- **The chains** at the rail: deadeyes and chain plates for the fore, the main and the mizen, the
  channels at the rail above the ports (read).
- **Inboard**: hatchways in red along the deck; pillars with step-cleats under the main hatch; the
  masts stepped on the keelson; an hourglass-shaped fitting rising above the rail at x +7.05, read
  as the galley's funnel or the capstan (JUDGEMENT).

### 2.9 What the plan does not give

Her masts' heights, her yards, her sails, her boats and her ground tackle; the camber of her deck;
the height of her stern windows (none drawn in the profile); her figure (none drawn); her paint
(the 1809 drawing shows a light band along the ports with dark lids, eye only).

## 3. Her rig

### 3.1 What the pictures show (eye only, never a point)

The 1809 drawing (Roos fig. 3) and the 1807 sketch (fig. 2): **a ship**, three masts square-rigged;
courses, topsails, topgallants and royals on the fore and main; a topsail and topgallant (and a
royal, uncertain) on the mizen over a bare crossjack yard; a gaff driver with the ensign at its
peak; three headsails on the bowsprit and jib-boom; the main topmast staysail set (read on the page
images, the reproductions dithered). That is the frigate's rig in the game, sail for sail.

### 3.2 Her spars by rule (rung C)

No spar of hers is on any source read. The rules on her own particulars (LWL 34.39 m, 112.8 English
ft; extreme breadth 9.06 m, 29.7 ft; the gun deck 124 pies, 113.4 English ft):

| Rule | Main yard | Basis |
|---|---|---|
| Luce 1866 ch. VII, the generator's chain for the frigate: the main mast (heel to head) = (LWL + breadth) / 2 = 71.3 ft (21.73 m); the main yard 10/11 of it | **19.76 m** | `tools/gen_ships.py` `frigate()`, read; every spar of hers is then the frigate's times **0.8132** |
| Falconer 1780, YARD: 0.575 of the gun-deck length below 44 guns | 19.87 m | The generator's docstring, read |
| Chapman 1781 §30: 0.52 of the length stem to post for frigate-built merchant ships | 17.97 m | read (OCR); the main topsail yard by the same rule 0.79 of it, 14.20 m |
| Steel 1794's 20-gun column | to read | the page image (§0) |

Luce and Falconer agree within 0.6%; Chapman, a Scandinavian builder's rule for merchant
frigates, is 9% shorter (judgement: a Danish naval light frigate is likelier to be lofty than a
merchantman). Her masthead by Luce's chain stands **29.1 m** above the water (the frigate's 35.9;
observed, `world.ships.rig_height_m`); her plain sail **1,047 m²** (the frigate's 1,584).

**Spanish practice, for the eye of the rakes** (Babron 1817 pp. 86-87, read (OCR)): a Spanish
frigate of 18 rakes her main 25 in 325 (4.4°), her fore 9 in 325 (1.6°), her bowsprit 189 in
325 (30.2°); a brig-rigged corvette of 18 her main 35 in 325 (6.2°), her fore 6 in 325 (1.1°), her
bowsprit 101 in 325 (17.3°). Her measured rakes (§2.8) lie within that practice. Babron's corvette
is brig-rigged, so the corvette's spar table in Babron is not hers (read).

### 3.3 Her handling, and the package's rig rules

- **No lateen**: her mizen carries a gaff driver and a crossjack; package 75's B3.1 (the lateen
  worn, not tacked, the yard dipped round) does not reach her.
- **The schooner's-mast rule** (B3.4, `Ship.on_schooner_mast`; Design-ShipsEngineExtensions.md):
  an after mast with yards and no yard on its lower mast handles as a fore-and-after's. Her mizen
  carries the crossjack on its lower mast, so **all three masts class square** (observed on the
  scratch file: fore, main and mizzen `False`, as the frigate's). Neither classing limit touches
  her.
- **Taking in the courses and staysails to fight under topsails** is what her captain did on 17
  September 1807 (Roos pp. 98-100): the game's "clear for action" and fighting sail as the
  frigate's.

## 4. Her guns, by date

| Date | Guns | Source | Note |
|---|---|---|---|
| 1807 to 1809, Danish | **4 × 8-pdr long guns and 16 × 30-pdr carronades** (Danish pounds) | Roos p. 94 (the ship's papers); the 1809 drawing's own caption (Roos p. 101) | Two sources of 1807-1809, one written aboard in 1809. **Not in the owner's three fits** (§8) |
| 26 September 1809, as captured | 20 × 24-pdr carronades | Winfield p. 930 | Conflicts with the line above for the same day; Winfield's source for it is not in the passage set down (§11) |
| 1809-1810, first rearmed | **20 × 30-pdr carronades** | Winfield p. 930; the plan's title, "del porte de 20 carronadas de á 30" | Ten a side in the ten broadside ports (§2.7) |
| 31 October 1817 | 12 × 12-pdr, 8 × 30-pdr carronades, 4 × 3-pdr obuses | Winfield p. 930 | 24 pieces for 22 ports: two pieces over the rail or in the bow ports (judgement) |

- **The pounds.** A Spanish 30-pounder fires 30 libras (13.8 kg, 30.4 English lb); a Danish
  30-pund carronade about 15 kg (33 lb, memory on the pund); Winfield gives Spanish broadsides in
  libras with English pounds beside them at a ratio of 1.079 (`VesselReferences-2026-11-Spanish.md`
  §4: 1,212 libras as 1,308 lb; the lead: take Winfield's pairs and do not re-derive). The game's guns
  carry one `pounder` figure, read as English pounds by its ballistics (`combat/shot.py`
  `ballistics_of`, continuous in the pounder, read) and by the weight of a broadside
  (`combat/hits.py` l. 441). How a foreign pounder is filed is a rule for the owner (Design §17).
- **No gun weights** for any of these are in a source read: the drawn length of each follows the
  pattern of nearest weight in Adye's tables (package 81's checklist), the 32-pdr carronade's
  17.1 cwt for a 30 (Adye 1804 p. 72 as `tools/ships/period.py` holds it, read).
- **Obús**: a howitzer; a "3-pdr obús" as Winfield's English renders it (to ask what it fired).

## 5. Her company

| | Number | Source |
|---|---|---|
| Danish war establishment, "prima plan" | **120**: the captain, seven lieutenants, a petty officer with ten soldiers, three trumpeters and a drummer, a surgeon and a surgeon's mate, three mates (styrmænd), quartermasters, the boatswain, the hold's petty officer (skibmand), the sailmaker, the purser, the clerk and the ratings | Roos p. 94; the 1809 caption, p. 101 |
| Aboard when she sailed, July 1807 | **161** (41 over the establishment: men taken from Danish-Norwegian merchantmen lying in port) | Roos pp. 90, 95 (the provision journal's mess roll) |
| Left at the seizure, 1809 | 87 | Roos p. 90 |
| Spanish | **167** | Winfield p. 930 |

The Spanish company's make-up (officers, warrant officers, gunners of the brigades, seamen, ship's
boys, soldiers) is in no source read; the Spanish navy's establishment for a corvette is the passage
to ask for (§11). **She is a man-of-war in every fit**: package 75's ruling 11 (a merchantman's
master and mate counted a hand of their own watch where the watch is too small) does not reach her.

## 6. How she sailed

- **Her captain's report** after the seizure, made under article 195 of the articles of war (Roos
  p. 94, read on the page image): "Fregatten Diana bærer sine sejl superbe, er stiv, styrer
  prægtig" (Meyer, 1809: she carries her sail superbly, is stiff, steers splendidly), and rides
  easily at anchor. **Her best speed**: 10 to 11 miles in the watch with the wind 2 to 3 points
  free ("rumskøds"), a freshening wind from a stiff topgallant breeze to double-reefed topsails.
  Roos: a watch is four hours, the miles are Danish miles and not sea miles, and the speed was a
  good ship's ordinary one. A Danish mile is about four nautical miles (memory: the land mile of
  7.53 km is 4.07 nm; a sea mile of fifteen to the degree is 4.00), so **10 to 11 knots** (±2%;
  arithmetic). "Rumskøds" is read as the wind abaft the beam, so **112° to 124° off the wind**
  (JUDGEMENT on the idiom); the wind about 18 to 27 knots (judgement on the period's sail-carrying
  words).
- **The chase of 16-17 September 1807**: a British 44 chased her for 24 hours and carried away her
  main topgallant mast pressing after her; Meyer "could not sail from him" (Roos p. 98) with a
  sprung bowsprit. A ship of the period's ordinary good speed, not a flyer (judgement).
- **No Spanish report** of her sailing was found.

## 7. The engine, run (observed; details in Design §9)

A scratch file built in memory from `data/ships/frigate-36.yaml` (scratch only, validated by
`spec_from_dict`): her hull block from §2 (LWL 34.40, beam 9.06, draught 3.58, displacement
497,200 kg, deck 1.39 m, lateral area 104.7 m², rudder 3.84 m² scaled, hull speed 11.8 kn by the
frigate's √L, `clr_x_m` 2.5), every spar and sail the frigate's times 0.8132 (Luce's chain on her),
her masts at the plan's first reading (x +12.47, −2.38 and −11.42, raked 1.0°, 4.4° and 5.5°; §2.8's
final reading moves the main 7 cm and 0.6°, which no figure below would feel: judgement), her
company 167 on the frigate's stations scaled, the frigate's guns moved to her length, no profile.

| Measure | Her (GM 1.0 / 1.5 m) | The frigate |
|---|---|---|
| Static polar (`polar_of`), best in 15 / 25 kn | 7.96 kn at 90-100° / 11.11 at 100° | 8.19 / 11.63 |
| Closest course; `beat_deg(15)` | 50°; 60° | 50°; 60° |
| Sailed, 15 kn, 66° / 90° / 112° (speed, heel) | 4.71 kn 5.7°; 7.74 kn 9.2°; 7.52 kn 6.2° (GM 1.0) | 4.80 3.4°; 7.97 5.5°; 7.73 3.7° |
| Sailed, 15 kn, 66° / 90° at GM 1.5 | 4.72 kn 3.8°, helm +1.8°; 7.76 kn 6.1°, helm +2.0° | helm +1.3°, +2.0° |
| Sailed, 22 kn, 90°, heel | **19.0°** at GM 1.0; **12.9°** at 1.5; 10.8° at 1.8 | 11.3° |
| Meyer's case, 118° in 18 / 25 kn, plain sail | 8.67 / 10.66 kn (GM 1.5) | — |
| Tack (truth 10's three headings) | 349, 369 and **164 s** (GM 1.5); 351, 370, 379 s (1.0); each losing 9 to 42 m | 343, 447, 370 s; +51, −37, +25 m |
| Wear | 491 s, 259 m to leeward (GM 1.5) | 513 s, 234 m |
| Heave to and fill away, 15 kn | hove to in 132 s, 61° off at 1.3 kn after ten minutes; filled in 59 s | 220 s, 62°, 1.3 kn; 59 s |
| Plain sail from furled, the watch / all hands | 11.5 / 9.6 min | 16.4 / 5.6 min |
| Masts classed (`on_schooner_mast`) | fore, main, mizzen all square | the same |

- **Meyer's speed is met** at the stronger end of the report's wind; the frigate's hull speed scaled by √L
  (11.8 kn) holds it (11.0 gives 10.35 at 25 kn, 12.5 gives 10.90).
- **Meyer's "stiff" is not met at the frigate's GM ratio**: her displacement is 0.39 of the
  frigate's while Luce's rig gives her 0.54 of its heeling moment; she heels 1.7 times as much.
- **The tack from 295° in 164 s** is under truth 10's 285-second floor: a knife-edge tack (her
  sharp hull, judgement), for the builder's tuning, not a finding against the engine.
- **All hands make her plain sail slower than the frigate's** (9.6 against 5.6 minutes) while the
  watch alone is faster (11.5 against 16.4): the sails' wants are per sail, not per square metre,
  so her smaller company tells with all hands; why the watch is faster was not found (for the
  builder; observed, not explained).

## 8. Conflicts

| Subject | The sources | Reading |
|---|---|---|
| Her guns when taken, September 1809 | Winfield p. 930: 20 × 24-pdr carronades. Roos p. 94 (her papers) and the 1809 drawing's caption: 4 × 8-pdr long guns and 16 × 30-pdr carronades, Danish | Two sources of her own time against one historian's summary; the owner ruled Winfield's three fits on 2026-11-06 before this was found. Owner's question 1 (Design §17) |
| Her company | Winfield 167 (Spanish); Danish establishment 120, 161 aboard in 1807 | Not in conflict: different services. 161 and 167 are within 4% |
| Her tonnage | Winfield 335 t; the plan's displacement 540 t 691 lb (497 t) | Different measures (§2.3); ask Winfield's rule (§11) |
| Her rate | Winfield and the plan: a corvette; Roos and the 1809 caption: a frigate, "a light frigate" | A Danish light frigate rated by Spain a corvette by her guns and size; both true |
| Her sailing date | Roos p. 87: command hoisted 6 July, weighed 17 July 1807; Wikipedia: left on 7 July | Roos |
| Her main yard by rule | Luce 19.76 m, Falconer 19.87 m, Chapman 17.97 m | Luce (the generator's chain), Chapman the check; Steel to read |
| The pie | Winfield's metres 0.27863-0.27877 m; the tree's 0.2786 m; the vara de Burgos's third 0.278635 m | Winfield's metres for the book's figures; 0.278635 m for the measured ones |

## 9. What is open, and whom to ask

- **Her Danish draught** (Roos p. 94's "konstruktionstegningen"): her lines as built, the sweep
  ports, her stern and head, her spars if the sail plan survives. *Whom to ask:* the owner (whether
  to seek it); the Danish National Archives (Rigsarkivet) or the M/S Museet for Søfart, whose
  yearbook printed Roos; nothing of the request needs any personal detail.
- **The plan's own words not read**: the sheet may carry small lettering in the body plan's
  margins (the diagonals' numbers 1 to 5 were read; nothing else) that a larger image would show.
- **Steel 1794's 20-gun column** on the page image (the builder's step 1).
- **The Spanish company's make-up and watches**, the Spanish carronade's and obús's weights and
  shot, and the meaning of Winfield's 335 tons: Winfield's passages (§11).
- **The 1809 drawing for the tree**: the original (Frederiksborg, inv. no. 3561) is public domain
  by age; a direct image from the museum with its terms, vetted as the README's rows are (artist,
  date, licence, namesake), would let it be held as the reference picture of her rig. Roos's 1957
  reproduction is not offered until its status (a photograph of 1957 of a two-dimensional work, in
  a work taken as in copyright whose page states no licence) and its artist ("Thomsen pinx 1809",
  perhaps her officer of that name: not known to have been drawn aboard) are vetted (revised
  2026-11-18 on the critic's F14). Not added here: the images README is not this step's to change.
  Its row, when added: *"Diana. Kongelig Dansk Fregat": the Danish light frigate under all plain
  sail, 1809, the corvette Diana's own picture; Thomsen pinx 1809 (perhaps her officer of that
  name), coloured drawing, Det Nationalhistoriske Museum på Frederiksborg inv. no. 3561; public
  domain by age; its source and licence as found.*
- **The British 44 of September 1807**: her name (James vol. 4 or 5, the Mediterranean in
  September 1807: not searched), for a scenario of the chase.

## 10. The owner's questions

They are in the design (Design-Ship-Diana.md §17.1), each with the design's pick: her first fit
(the Danish papers or Winfield); how a foreign pounder is filed; her stiffness; her spars' rule; a
Danish fit and colours; her people's names.

## 11. Winfield passages to ask for (by title and class; the owner sources them)

*Spanish Warships in the Age of Sail 1700-1860* (Winfield, Tredrea, García-Torralba Pérez, Blasco
Felip; Seaforth 2023), the owner's edition:

1. **The *Diana*'s whole entry, p. 930** (the corvettes acquired by capture): her service line by
   line (her commanders, the voyage of November 1810 and where she served, the date of the 1817
   inventory's survey, her end in 1832), **the source note for "20 × 24-pdr carronades as
   captured"**, and the rule of the "335 t".
2. **The introduction to the chapter of corvettes** (the class of *corbetas*, about pp. 900-930):
   the Spanish navy's establishment of men for a corvette of 20 (officers, warrant officers,
   gunners of the brigades, seamen, boys, soldiers) and how corvettes were rigged and armed after
   1800.
3. **The pages on Spanish carronades and obuses** (the ordnance section of the book's front
   matter, if it has one): the 30-pounder carronade's weight and shot, the 3-pounder obús, and the
   libra against the English pound in Winfield's practice.
4. **Any other ship seized in 1808-1809 from France's allies in Spanish ports**, if the book lists
   them beside her, for her companions in a scenario of 1809-1810.
