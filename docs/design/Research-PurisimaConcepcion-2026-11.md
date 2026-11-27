# Research note: the *Purísima Concepción* class three-decker (package 90, November 2026)

**Corrected 2026-11-20 by her measuring** (`docs/design/ships-design/pages-concepcion.md`,
**Pages**). Her own plan, PB-039, was measured at the library's full size (12,932 × 4,574 px, 39.75 px
a pie), and her sister's sheets at Greenwich, ZAZ0100 to ZAZ0103, at the 1,280 px the museum serves.
The owner chose PB-039 for her hull the same day ("Use PB-039 (Recommended)"), and the lead ruled on
the measuring (nudge 30, item 4). Only what the measuring corrects is corrected here. Each correction
is set after the reading it corrects, which stands as it was found (the marks are never upgraded):
- what PB-039 holds: a body plan and a half-breadth plan, not a section only (§0.2, §2.4);
- its scale (§2.4) and her drawn length, 219.8 pies post to stem, not about 214 (In short, §2.4);
- its two dashed lines, neither a waterline, and her load line (§2.4, §2.6);
- her displacement, her draught and her sills, now measured (§2.5, §2.6, §9, §10);
- the Greenwich sheets, viewed at 1,280 px: their length, and the sixteenth lower pair's place (§0.3,
  §2.2, §2.3, §9, §10);
- her source, the owner's (§2.3, §11).

**Revised 2026-11-19 on Winfield's passages sent by the owner, and the owner's answers of that
day.** The units (Winfield et al. 2023, pp. 41-46), the complements of 1 January 1788 (p. 1446 and
the two pages following) and of the Regulation of 16 October 1803, and the ordinance of 1803's guns
by deck came, set down in `VesselReferences-2026-11-Spanish.md` §7, §15 and §16. **Her company by
kind is the regulations'** (a 112: 877 in 1788, of whom 225 soldiers; 1,015 in 1803, of whom 275);
**the libra is 0.4608 kg**, one ratio for every calibre; **the ordinance's 112 carries 118 pieces**,
and its own note gives her 18-pounders in her third battery. The class's pages (pp. 406-410) were
not sent again: the keel's and the rebuilt length's digits, her draught, sills, trials and the
sixteenth pair's place stay open, to be measured (ZAZ0101) or judged, by the owner's word. The
units, §3.3, §3.5, §4, §10 and §11 are brought into line; nothing else is changed.

The research for the fifth and largest hull of package 90, the Spanish navy's *Purísima
Concepción* class of three-deckers, the game's first ship of three gun decks. It is the note her
design document (`Design-Ship-PurisimaConcepcion.md`, second draft of 2026-11-18) works from, in the form of
`Research-Bilander-2026-10.md` and `Research-74-2026-10.md`. Nothing here is built.

**What binds.** The lead's note of 2026-11-18, 00:50 UTC (nudge 15), the last paragraph of row
90 in `docs/dev/M7-WorkPackages.md`: package 90's preliminary work only, research and planning,
new documents under `docs/design/` and `docs/references/`, on `claude/pkg-90`; no code, ship file,
generator change, scenario or test, and nothing the suite reads. The package's own words for this
hull (the notes of 2026-10-29, 2026-11-06 at 18:00 and the row): the first three-decker, "three gun
decks, a first rate's complement and her stations, the great ship's handling"; the 1797 fit of 112
for St Vincent and the 1803 fit of 116 for the war's scenarios; her company of 839; built to
`Build-Ships.md` §5.0's principles and its ladder of evidence.

**The ladder.** The lead's notes name three rungs: **rung A** the original plans, **rung B** a
historian's particular, **rung C** judgement, marked JUDGEMENT. They sit on `Build-Ships.md`
§5.0's ladder for the drawing as follows: rung A is §5.0's **S** (her own lines, her class's or a
sister's) or **S†** (a period plan of her type, scaled); a named period rule applied to her own
particulars is §5.0's **R**, and is given here as "rule" with its book and page (it is not rung B:
it is a rule, not a particular of hers); rung C is §5.0's **T**. Every figure below carries one.

**The marks** (as the 74's note; never upgraded):
- **read**: the page, image, code or catalogue text was seen. *read (OCR)* is a text layer under
  `docs/references/` read without its page image. *read on screen* is an image viewed at its full
  served resolution in the browser and measured there, not downloaded and not held.
- **catalogue**: from a catalogue entry only; the document itself was not seen.
- **via Winfield**: a fact the owner read in Winfield and the lead set down by page in
  `VesselReferences-2026-11-Spanish.md` ("VR-Sp"); the book is not in the tree and was not seen.
- **measured**: off an image, with the scale and the uncertainty stated.
- **observed**: in a run of the game's engine (scratch scripts outside the repository).
- **judgement**, **secondary**, **memory**: as they say. No memory is used for a figure.

**Units.** Winfield's dimensions for Spanish ships are in **pies de Burgos** of 0.2786 m (VR-Sp,
"Units"; the game's own figure, `docs/dev/TuningNotes.md`, package 39d). The game's constants are
metres from Winfield's metres where the book gives them. James, Falconer and Steel are in English feet
of 0.3048 m. A Spanish gun's calibre is in *libras*; Winfield gives each broadside in libras with
the book's English pounds beside, and the lead's rule is to take the book's pairs as it gives them (VR-Sp,
"Units"). Tons: *arqueo* (Spanish measure) and *bm* (English builder's measure) are different
things and are never compared as one. **2026-11-19** (Winfield et al. 2023, pp. 41-46): the pie is
278.635 mm; the libra 0.4608 kg; a row's length is the *eslora*, on the lowest planked deck over
both overhangs; the *puntal* the depth in hold, about half the *manga*; the *tonelada de arqueo* a
capacity of about 1.42 m³ (VR-Sp §7).

**The scratch.** Every probe is under `scratchpad/p90/concepcion/` in the session's scratch ("the
scratch", not filed), run with `py` from the scripts' own folder, the pkg-90 tree first on `sys.path`
and `freesail.__file__` asserted under it (`common.py`); no tracked file in the tree was changed by
a probe (Python's git-ignored bytecode caches aside). The scratch three-decker (`build_td.py`) is the 74's file with a middle deck put in, her
ports at the places read off her own plan, Winfield's two fits and a company of 839: a question
put to the engine, never a design figure.

---

## In short

- **Her own plan is online and openly licensed.** Francisco Gautier's *Plano del Navío de S.M.C.
  Nombrado Nuestra Señora de la Concepción del Porte de 112 Cañones*, Ferrol 1779, Archivo
  Histórico de la Armada, signature **PB-039**, a section and an elevation in black ink and
  carmine, 29 × 82 cm, its digital copy **CC BY 4.0** on the Biblioteca Virtual de Defensa (record
  1026905; credit "Fuente: Archivo Histórico de la Armada Juan Sebastián de Elcano / Biblioteca
  Virtual de Defensa"), its note "Tipo: Purísima Concepción y San José, Ferrol, 1783. Sistema
  francés" (catalogue, read). Read on screen at 12,932 × 4,574 px: **three tiers of 15, 16 and 16
  ports a side** (lower, middle, upper), the upper works pierced besides, a scale of sixty pies de
  Burgos at 39.8 px a pie, the drawn hull about 214 pies long, the lower ports 12¾ pies apart
  (3.56 m) (measured, §2.4). It is the rung-A source for her as built. It is not in the tree; the
  owner decides whether it is held (§11).
  **Corrected 2026-11-20** (Pages §1, §3, §5.1): the sheet holds a body plan of eighteen sections and
  a half-breadth plan as well as the sheer; its scale is 39.75 px a pie; her drawn length is **219.8
  pies (61.26 m)** from the post's after face to the stem's fore face on her line, the 214 having
  stopped short of the stem. **By the owner's choice of 2026-11-20 her hull is drawn from it.**
- **Her sister's lines as rebuilt are at Greenwich**, the *San Josef* as fitted at Plymouth for a
  114-gun first rate: **ZAZ0101** (body plan, sheer and half-breadth, 1:48, 25 February 1801,
  signed by John Marshall), **ZAZ0102** (middle, gun and orlop decks, 1:96), **ZAZ0103**
  (quarterdeck, forecastle and upper deck, 1:96), and **ZAZ0100**, the full colour plan Winfield
  reproduces as J1945, which Greenwich dates **1799**, not 1797 (catalogue, read). Crown copyright;
  cited by object number, never copied. **Corrected 2026-11-20:** viewed at 1,280 px, the only size
  the museum serves free (Pages §1.2, §11); her comparison, not her hull, by the owner's choice.
- **Winfield's figures** (via Winfield, pp. 406 to 410): as built 213 ft 9 in by 58 ft by 29 ft
  (59.55 × 16.16 × 8.08 m); as rebuilt at Cádiz 1786 to 1793, 220 ft 6 in, keel 186 ft, 58 ft 4 in
  by 28 ft 9 in (61.30, 51.82, 16.25, 8.01 m), 2,771 tons; 5,167 t displacement; 839 men. Two of
  the book's metres do not follow from its feet (§2.1).
- **James on the San Josef as taken** (read (OCR), vol. 2 pp. 51 and 59): 194 ft 3 in on the gun
  deck, 54 ft 3 in extreme, 24 ft 5 in in the hold (59.21, 16.54, 7.44 m), 2,457 tons bm; 30 long
  36s (Spanish calibre), **32 long 18s** on the second deck, 32 long 12s, 18 long 8s, 112 guns,
  **917 men and boys** by the head-money warrants. Winfield has 24s on the middle deck, and the book's
  broadside of 1,188 libras holds only with 24s (§3.2).
- **The two fits.** Winfield's 1780s establishment of 112 (the 1797 fit) and the book's 1803 alteration
  of 116 (the 1809 fit) each sum, side by side, to exactly the book's broadside in libras: 1,188 and
  1,508 (observed, the scratch's fits; §3.1).
- **Her sailing.** Brenton (1823) and Nelson on the *San Josef*, via Winfield: a ship of the line
  with "the sailing abilities of the fastest frigate", and "the finest ship in the world". James
  (read (OCR), vol. 6 pp. 3 to 4, 1813): the *Caledonia*, the *Boyne* and the *San Josef* "far ahead
  of the remainder of their fleet" off Toulon.
- **No Spanish masting, company breakdown, gun weights, draught or sill height was found.** The
  masts rest on Steel 1794's rule (half the lower deck and the extreme breadth for the main mast:
  vol. I p. 39, read (OCR)), British and applied to her by judgement; the rest are passages to ask
  for (§11). **Corrected 2026-11-20:** her draught and her sills are measured on her own plan, PB-039
  (§2.6).
- **The engine, run.** It already takes a third gun deck: the deck word `middle`, the guns
  numbered by deck, the beat's deck lines, the orders by deck and the viewer's check all work on
  the scratch three-decker (observed, §7). What it lacks is hers to give: a description and rank
  ("a three-decker" names no vessel and ranks nothing today), the words "second deck" and "third
  deck", a bill that mans all her guns from 839, a tack no quicker than a 74's (the scratch file
  tacks in 181 to 189 s against the 74's 237 to 258 s), and a polar at least the 74's (the
  scratch file is 0.4 kn slower abeam). Pace and checkpoint hold: in truth 7-196's own world three
  three-decker probes crewed run 72 to 75 ticks a second against three 74s' 79 to 81, about 0.92, over
  the floor of 60 (the engine note's §7; this note's own p5c.py ran a world of its own, below), and her checkpoint at quarters is 174 KB gzipped against the 74's 168 KB.

---

## 0. The sources

### 0.1 Held in the repository (rows in `docs/references/README.md`)

| Short form | Work, standing | Rung | What it gives here |
|---|---|---|---|
| VR-Sp | `docs/design/VesselReferences-2026-11-Spanish.md`: the lead's words for Winfield's facts, by page (Rif Winfield and others, *Spanish Warships in the Age of Sail, 1700–1860*, Seaforth 2023; copyright; the owner's book, not in the tree) | B (via Winfield) | §4: the class whole, pp. 406 to 410: her two ships, the design systems, the rebuild, the figures, the three armaments, 839 men, her service, the plans he reproduces, Brenton's and Nelson's words |
| James | William James, *The Naval History of Great Britain*, vols 1, 2 and 6 (1837 text; 1886 and 1902 printings), public domain, `docs/references/james/` | B | vol. 1 pp. 29 to 30 (foreign builders' lower batteries "higher from the water"; Spain's ships built higher and broader than any other nation's); vol. 1 p. 46 (the Spanish nominal pound, 1/72nd to be added); vol. 2 pp. 36 to 61 (St Vincent: the Spanish line, the prizes' damage, losses, force, men and dimensions); vol. 6 pp. 3 to 4 (the *San Josef* off Toulon, 1813) and pp. 405 to 407 (her rating and 850 men in British service) |
| Nicolas | Sir N. H. Nicolas, *The Dispatches and Letters of Vice Admiral Lord Viscount Nelson*, vol. 2 (1845), public domain, `docs/references/nicolas/` | B (Nelson's own narrative) | pp. 341 to 347: the St Vincent narratives (the *San Josef*'s admiral's stern gallery, her main chains, her quarterdeck; the *Captain*'s wheel shot away) |
| Falconer | William Falconer, *An Universal Dictionary of the Marine* (1780), public domain, `docs/references/falconer/` | B (a period definition) | DECKS (first and second rates "furnished with three whole decks", "the second or middle deck"); RATES (a first rate of 100 guns manned with 850 men; six lieutenants, six master's mates, twenty-four midshipmen; the *Victory*'s dimensions) |
| Steel 1794 | David Steel, *The Elements and Practice of Rigging and Seamanship*, vol. I (1794), public domain, `docs/references/steel/` | rule | p. 39 (OCR l. 4459-4495): the Royal Navy's rule for the main mast, half the lower deck and the extreme breadth, and the other masts' fractions (the fractions lost in the OCR); p. 49: the masts and yards of a 100-gun ship of 2,164 tons, "taken at the partners; which are at the middle deck in three-decked ships" (OCR garbled: to read on the page image) |

### 0.2 Read online, not held

| Short form | Work, where, standing | Rung | What it gives here |
|---|---|---|---|
| **PB-039** | Gautier, *Plano del Navío de S.M.C. Nombrado Nuestra Señora de la Concepción del Porte de 112 Cañones*, Ferrol 1779, manuscript, colour, 29 × 82 cm, "1 sección y 1 alzado"; Archivo Histórico de la Armada J. S. de Elcano, PB-039; Biblioteca Virtual de Defensa, record 1026905 (image group path 348289; image id 4140128, 12,932 × 4,574 px); **CC BY 4.0** with the credit above | A (her own plan, as built) | §2.4: her tiers and their ports, her scale, her length as drawn, the upper works, the channels, the head and the quarter galleries; read on screen only. **Corrected 2026-11-20:** fetched at full size from the record's second image group (356204, a one-page PDF) and measured, kept outside the tree; the sheet holds a body plan of ten after and eight fore sections with five diagonals, and a half-breadth plan under the sheer (Pages §1.1, §1.3) |
| ZAZ0100 | RMG, *San Josef (captured 1797)*, the full colour plan, dated 1799, 654 × 1,960 mm; image J1945; © Crown copyright, NMM | A (her sister as fitted), catalogue | the plan Winfield reproduces (p. 410); the catalogue dates it 1799 and the fitting at Plymouth June 1799 to January 1801 |
| ZAZ0101 | RMG, *San Josef (captured 1797)*, body plan, sternboard with its decoration, sheer with inboard detail, quarter decoration, figurehead and half-breadth, 1:48, 25 February 1801, "as fitted at Plymouth Dockyard for a 114-gun First Rate, three-decker", pencil alterations of April 1808 for her large repair of 1807 to 1809, signed by John Marshall; image J1950, 678 × 1,982 mm; Crown copyright | A (her sister's lines as rebuilt), catalogue | the source for her lines as she sailed in 1797 and after. **Corrected 2026-11-20:** viewed at 1,280 px (RMG object 79892) and measured coarsely, 7.5 cm a pixel (Pages §11.2); her comparison by the owner's choice |
| ZAZ0102 | RMG, the *San Josef*'s middle, gun (lower) and orlop decks with the platforms, 1:96, 25 February 1801; image J1949; Crown copyright | A, catalogue | her decks |
| ZAZ0103 | RMG, the *San Josef*'s quarterdeck, forecastle and upper deck, 1:96, 25 February 1801; image J1948; Crown copyright | A, catalogue | her upper works |
| PB-049 | Tomás Bryant, *Plano de aloxamientos y cubiertas del Navío de tres puentes del porte de 112 cañones nombrado la Reyna Luisa*, Ferrol, 29 October 1791, 65 × 100 cm, Romero Landa's project; its note "Tipo: Mejicano, Conde de Regla, Salvador del Mundo, Real Carlos, San Hermenegildo y Príncipe de Asturias"; the verso "Repartimiento de Cubiertas para Navios de 3 puentes"; AHA; BVMDefensa record 1027262; CC BY 4.0 | A for the type (S†), catalogue | the Santa Ana class 112s' decks and quarters: the next class, the same establishment |
| PB-078 | Romero Landa, *Plano del navío de S. M. nombrado la Reyna Luisa*, Ferrol 1791, 27 × 32 cm, "with the sums of the effects of her sails" (the title's subtitle: her canvas, its weight, making and value), scale "por pulgada por cada 8 pies"; AHA; BVMDefensa record 1016201; CC BY 4.0 | A for the type (S†), catalogue | a Spanish 112's sails: the one Spanish rig source found |
| PB-344 | Romero Landa, *Aloxamientos para navíos de tres puentes del porte de 112 cañones*, Madrid, 13 May 1792, 143 × 31.5 cm, a copy; AHA; BVMDefensa record 1042790; CC BY 4.0 | A for the type (S†), catalogue | the 112s' accommodation by the establishment of 1792 |
| PB-060 | Joan Smith, *Plano de los alojamientos de un navío de tres puentes*, Cartagena, 28 January 1794, 48 × 67 cm; AHA; BVMDefensa record 1038902; CC BY 4.0 | A for the type (S†), catalogue | a three-decker's accommodation, 1794 |
| Ibargüen 1785 | Joaquín Ibargüen, *[Plano de la máquina de la rueda de timón]* and *Plano de la Muestra del Timón para Buques de 74 cañones*, 26 November 1785; AHA; BVMDefensa image groups 348549, 348551 and 348550 (the records' licences not opened) | A for the navy (catalogue) | the Spanish navy fitted a steering wheel with its machinery and a helm indicator by 1785: package 116's wheel shot away stands for her |
| ZAZ0170 | RMG, *Unnamed 112-gun Spanish three-decker*, signed by Julián Martín de Retamosa, the record dated 1 December 1812; image J1872; Crown copyright | catalogue | a later Spanish 112's lines; not hers |
| Stanfield | Clarkson Stanfield, *The Breaking up of the San Josef, 1849*, watercolour, RMG PW6066; on Wikimedia Commons as public domain | for the eye | her hull at the end of her British life; not vetted beyond its title and source (§11) |
| Brenton | E. P. Brenton, *The Naval History of Great Britain* (1823), public domain, Internet Archive `navalhistorygre02brengoog` (vol. II) and the other volumes | B via Winfield | the phrase VR-Sp cites from Winfield; not found in the first 300,000 of vol. II's 917,838 characters (read); its page is to find |

### 0.3 Cited and not reached

- **Museo Naval, Madrid, PB_0050**: her deck plans of 1795 with 110 guns laid out, the admiral's
  cabins on the *toldilla* and the captain's and lieutenants' on the *alcázar* (via Winfield, p.
  409). Not found online under any form of its number (searched); its terms unread.
- **Nelson's "the finest ship in the world"**: via Winfield; Nicolas's later volumes (1798 to 1801,
  when Nelson's flag flew in her) are not in the tree.
- **A Spanish masting rule** (*reglamento de arboladura*) for a 112, **a Spanish complement
  table** (*dotación*) and **the Spanish guns' weights** were searched for and not found in any
  public-domain or open source; a university thesis on Romero Landa's 112s (core.ac.uk) was
  refused (403) and is a modern work in any case.
- **The images of ZAZ0100 to ZAZ0103**: not viewed. Under the Greenwich rule they are read and
  cited by object number, as *Minorca*'s ZAZ4270 is for the xebec; what is the owner's is whether
  her hull is drawn from them (her sister's as rebuilt) or from PB-039 (her own as built) (§11).
  **Corrected 2026-11-20:** viewed and measured at 1,280 px, RMG objects 79891 to 79894, the only
  size served free (Pages §1.2, §11); the owner chose PB-039 (§11).

---

## 1. The class and her two ships

**The two ships** (via Winfield, pp. 406 to 410):
- ***Purísima Concepción***: ordered at Ferrol 2 June 1778 (yard no. 64), keel laid 29 February
  1779, launched 24 December 1779.
- ***San José***: ordered 28 July 1781, launched 1783; taken at Cape St Vincent on 14 February 1797
  by Nelson from the *Captain*, by way of the *San Nicolás*; HMS *San Josef* to 1846, then
  harbour service at Plymouth until she was broken up in 1849 (RMG ZAZ0100's and PW6066's
  catalogues).

**The design.** Begun to Jorge Juan's *sistema inglés*, as the *Santísima Trinidad* was; amended
by Francisco Gautier as 90-gun three-deckers with no guns on the quarterdeck or forecastle; built
by José Joaquín Romero Fernández de Landa, who thinned the upper works' scantlings for stability
and speed and for want of great timber. They were the only three-deckers of the *sistema
francés* (via Winfield). PB-039's own note says the same, "Sistema francés" (catalogue, read).

**The rebuild.** Sea trials from Cádiz, 20 August to 18 September 1784, led to both being rebuilt
at Cádiz in the later 1780s (the *Concepción* 1786 to 1793): eighteen 8-pounders added on the
upper works, the upper deck's 18-pounders replaced by 12-pounders, the broadside from 1,212 libras
(1,308 lb) to 1,188 (1,282 lb), the standard of every later 112. A sixteenth pair of lower-deck
ports was cut for both at Cádiz in 1791, unarmed in Spanish service and armed by the British in
the *San Josef*. In 1803 at Ferrol the *Concepción* was altered to 116 (§3.1) (via Winfield). What
the trials found wanting is not in VR-Sp (§11).

**Her service, for the scenarios** (via Winfield): flagship out of Ferrol 18 May 1780 and with
Córdova's combined fleet in the Channel campaigns of 1780, 1781 and 1782; Córdova's flagship
October 1781 to April 1782; the siege of Gibraltar in 1782 and present, not engaged, at Cape
Spartel on 22 October 1782; in ordinary at Cartagena to 1784; rebuilt at Cádiz 1786 to 1793;
Lángara's flagship to Toulon, October to December 1793; Mazarredo's flagship from 1795; at Cape
St Vincent in 1797 as Morales de los Ríos's flagship, 8 dead and 21 wounded; with the combined
fleet to Brest in August 1799 and blockaded there to April 1802; in ordinary at Ferrol from 1802;
recommissioned to Cádiz in September 1809; driven ashore on the French-held shore of Cádiz Bay in
the storm of 7 March 1810, burnt by French troops and sunk 9 March 1810. James lists the
*Concepcion* among Córdova's 112s at St Vincent (vol. 2 p. 36, read (OCR)).

**The *San Josef* at St Vincent** (read (OCR)): she fell on board the *San Nicolás* as that ship
luffed up (Nicolas vol. 2 pp. 341 and 345); her admiral's stern gallery fired on the boarders (p. 345); she
was boarded by her main chains and surrendered on her quarterdeck, her admiral "dying with his
wounds below" (p. 346); she lost her mizen mast and main topmast (James vol. 2 p. 49), 46 killed
and 96 wounded (p. 50). The *Captain* had "her wheel shot away" before Nelson boarded (Nicolas vol.
2 p. 341; "the wheel shot away", p. 345): the wheel of package 116 at the class's own battle.

---

## 2. The hull

### 2.1 Winfield's figures, in pies de Burgos and the book's metres (via Winfield, p. 407)

| Figure | Winfield's feet | × 0.2786 | Winfield's metres | Agreement (judgement) |
|---|---|---|---|---|
| Length, as built | 213 ft 9 in | 59.55 m | 59.55 m | exact |
| Keel, as built | 190 ft 10 in | 53.17 m | 53.12 m | 0.05 m off; 190 ft 8 in gives 53.12 |
| Breadth (*manga*), as built | 58 ft 0 in | 16.16 m | 16.16 m | exact |
| Depth (*puntal*), as built | 29 ft 0 in | 8.08 m | 8.08 m | exact |
| Length, as rebuilt | 220 ft 6 in | 61.43 m | 61.30 m | 0.13 m off; 220 ft 0 in gives 61.30 |
| Keel, as rebuilt | 186 ft 0 in | 51.82 m | 51.82 m | exact |
| Breadth, as rebuilt | 58 ft 4 in | 16.25 m | 16.25 m | exact |
| Depth, as rebuilt | 28 ft 9 in | 8.01 m | 8.01 m | exact |
| Tons (*arqueo*) | 2,476 and 2,456 as built; 2,771 rebuilt | | | the two as-built figures not explained in VR-Sp |
| Displacement | | | 5,167 t | which load, not said (§2.5) |
| Men | 839 | | | §4 |

Two of the lead's transcribed pairs do not agree with the foot: the keel and the rebuilt length.
Either a digit of the feet or of the metres is wrong in the transcription or in the book; the
owner's re-reading of p. 407 settles it (§11). Until then the design takes Winfield's metres, as
the lead's rule says.

Which length Winfield's "length" is: VR-Sp labels it "Length overall" (the lead's transcription).
Set against James's gun-deck length for the *San Josef* (§2.2), and against the *Diana*'s plan,
where Winfield's 124 pies measure as her gun deck from post to stem (`Research-Diana-2026-11.md`
§2.2-§2.3), it reads as the *eslora* on the gun deck (JUDGEMENT); the owner's re-reading of the
passage is asked (§11).

### 2.2 James's figures, in English feet (read (OCR), vol. 2 p. 59)

| | Gun deck | Extreme breadth | Depth in hold | Tons bm |
|---|---|---|---|---|
| *San Josef* (built 1783) | 194 ft 3 in (59.21 m) | 54 ft 3 in (16.54 m) | 24 ft 5 in and a fraction (7.44 m) | 2,457 |
| *Salvador del Mundo* (1787) | 190 ft 0 in (57.91 m) | 54 ft 3 in (16.54 m) | 23 ft 3 in (7.09 m) | 2,398 |
| *Ville de Paris*, the largest English-built ship | 190 ft 2 in (57.96 m) | 53 ft 2 in (16.21 m) | 22 ft 2 in (6.76 m) | 2,352 |
| *Victory* | 186 ft 0 in (56.69 m) | 52 ft 0 in (15.85 m) | 21 ft 6 in (6.55 m) | 2,162 |

- **The breadths.** James's 16.54 m extreme for the *San Josef* is 0.29 m over Winfield's rebuilt
  *manga* of 16.25 m and 0.38 m over the book's as-built 16.16 m. The *manga* is read as taken inside
  the planking, so that two thicknesses of outer plank of about 15 to 19 cm close the gap
  (judgement; the Spanish definition to confirm, §11).
- **The lengths.** James's 59.21 m for the *San Josef* as taken (so as rebuilt) is 0.34 m under
  Winfield's as-built 59.55 m and 2.1 m under the book's rebuilt 61.30 m. Either the *San José*'s rebuild
  did not lengthen her as the *Concepción*'s did, or the two measure differently (judgement);
  ZAZ0101's scale settles it for the sister, and PB-039's for the *Concepción* as built.
  **Corrected 2026-11-20** (Pages §5.1, §11.2): ZAZ0101 and ZAZ0100 draw the *San Josef* **195.9 ft
  (59.71 m)** from the post's after face to the stem's fore face, 1 ft 8 in over James's gun deck;
  PB-039 draws the *Concepción* **61.26 m** on her line: the sisters' drawings differ by 1.55 m. Her
  length is ruled PB-039's (the lead, 2026-11-20).
- **The tons.** James's 2,457 bm and Winfield's 2,456 for one of the book's as-built figures are one ton
  apart: Winfield's 2,456 may be the British measure of the *San Josef* (judgement, §11).
- **Spanish ships broad and high.** James vol. 1 p. 29 (read (OCR)): Spain built "higher" and
  "broader, than those of any other nation", and a ship so built had her lower battery "higher
  from the water". No figure is given for these ships.

### 2.3 What the drawings at Greenwich are (catalogue, read)

ZAZ0100 to ZAZ0103 (§0.2) are the *San Josef* in British hands: the colour plan of 1799 and the
three Plymouth sheets of 25 February 1801 for a 114-gun first rate. **Winfield's "draught of *San
José* as taken" (VR-Sp §4, J1945)** is, by Greenwich's own record, the 1799 colour plan, drawn
after two years in British service and during her fitting at Plymouth, not on her capture: the
"sixteenth pair of lower ports" it shows is the pair cut at Cádiz in 1791 and armed by the
British (via Winfield). `docs/references/images/README.md` repeats "as taken in 1797"; the lead may
wish to amend it (this note writes nothing else; §9).

ZAZ0101 is the rung-A source for her lines as she sailed from 1793 once it is read: her sister's,
after the rebuild, at 1:48, with the body plan, the sheer and the half-breadth (§5.0's **S**: a
sister's lines). Not viewed yet, it holds no rung until then (principle 3). PB-039 is her own plan,
read on screen, but of the hull before the rebuild: scaled to her rebuilt length it is her
stand-in (S†) meanwhile.

**Corrected 2026-11-20** (Pages §1.2, §5.1, §11): ZAZ0101 was read only at Greenwich's 1,280 px
(7.5 cm a pixel); its sections, load line, sills and decks are not measurable at that size. PB-039
already draws her about 220 pies outside the stem and post, so the scaling to her rebuilt length
would count the rebuild twice. **The owner chose PB-039 for her hull** the same day ("Use PB-039
(Recommended)"): her own lines, rung S, unscaled; the Greenwich sheets her comparison.

### 2.4 Her own plan, PB-039, read on screen (measured)

The plan was viewed at the full resolution the library serves (12,932 × 4,574 px) by drawing
regions of it to a canvas in the browser and reading the columns of its scale bar by a pixel
profile; nothing was downloaded or saved. It shows, from the left: a midship section; a scale
of sixty pies de Burgos ("Escala de ... Pies de Burgos", its first ten feet numbered singly, then
every second foot to 60); and the sheer elevation, stern to the left, her title across the top
("del Porte de 112 Cañones").

**Corrected 2026-11-20** (Pages §1.3): not a midship section but a **body plan** of eighteen
sections (ten after, eight fore) with five diagonals, in a frame 58.25 pies wide; and a
**half-breadth plan** under the sheer. Pages reads the bar as 58 pies, its first pie split by a
diagonal scale; the count of 57 divisions over about 2,268 px is the same (Pages §3).

| Reading | Figure | How |
|---|---|---|
| The scale | **39.8 px a pie de Burgos** (142.9 px a metre), ±1% | 57 even divisions over 2,268 px between the bar's 356th and 2,624th columns (the first foot or two split by a diagonal scale). **Corrected 2026-11-20:** 39.75 px a pie, ±0.4% (the bar's lines fitted at 39.69, 39.80 end to end, the body plan's frame its 58 pies at 39.92: Pages §3) |
| Her drawn length, the stern's after edge to the head's fore edge | about 214 pies (59.6 m), ±2 pies | the hull from about x 3,150 to 11,700 px at the water's height, rough; agrees with Winfield's 213 ft 9 in as built. **Corrected 2026-11-20:** **219.8 pies (61.26 m)** from the post's after face (x 3,131) to the stem's fore face (x 11,870) on her line, the 11,700 having stopped 170 px short of the stem; 220.0 pies outside them at the lower deck and 215.5 between the rabbets there (Pages §5.1, measured). **Ruled her length, 61.26 m** (the lead, 2026-11-20) |
| The lower tier | **15 ports a side**, 12¾ pies apart centre to centre (3.56 m), spanning 178.7 pies (49.8 m) | centres at x 3,982 to 11,095 px |
| The middle tier | **16 ports a side**, staggered between the lower and the upper, spanning 191.8 pies (53.4 m) | x 3,713 to 11,346 px |
| The upper tier | **16 ports a side**, over the lower tier's ports and one more aft, spanning 191.8 pies | x 3,453 to 11,086 px; its centre 6.8 pies (1.9 m) abaft the lower tier's |
| The upper works | small ports in the waist's and the quarterdeck's bulwarks, with the main and fore channels' deadeyes at that height and their chain plates down across the upper tier | seen; not counted |
| The forecastle | a rail with a row of timberheads standing above it | seen |
| The head | a beakhead with its rails and a figure | seen |
| The stern | quarter galleries in two closed tiers with a third tier of lights above | seen |
| The inboard | the decks in carmine, a pump in the waist from the lower deck to the hold | seen |
| Below the lower tier | two dashed lines along the wales, one about 1 m and one about 2.5 m below the lower sills at midships, neither labelled in what was read | **not identified**: either may be a waterline; so the lower sill's height above her load line is not read (§10). **Corrected 2026-11-20:** **neither is a waterline**: both curve up toward both ends, as a deck's or a ribband's sheer does. Her drawn load line is L0, the top of seven faint ruled waterlines, inclined 0.47° to the keel (Pages §4.1); **ruled her load line as traced** on it, 8.02 m to K aft and 7.94 m at the middle, the straight fit recorded beside it (the lead, 2026-11-20; Pages §12.1) |

Her as-built ports, 15, 16 and 16 a side, are Winfield's 30, 32 and 32 guns on the three decks
exactly (94 as built). The plan's title says 112, and its upper works are pierced: so the sheet
was drawn, or titled, for the establishment of 112 that the rebuild gave her, while Winfield says
she was built as a 90-gun ship with nothing on her quarterdeck or forecastle (judgement; §9).

### 2.5 The displacement

Winfield's 5,167 t is about twice a 74's (the *Bellerophon*'s file holds 2,600 t at 51.2 m by 14.25
m) where her length and breadth are 1.20 and 1.14 times the 74's. At the 74's block (2,600 t on
51.2 × 14.25 × 6.46 m, 0.537 with sea water at 1.025) her length and breadth give about 4,000 t
at a draught of 7.5 m and about 4,300 t at 8.0 m (judgement, arithmetic). To float 5,167 t she
would draw some 9.6 m at that block, or carry a block of about 0.69 at 7.5 m. Either Winfield's
figure is at a deeper load than the game's sailing water, or the block of a Spanish three-decker
is much fuller than a British 74's. Her lines (ZAZ0101, PB-039) give the answer when measured; the
design carries 5,167 t beside the measured figure (§10).

**Corrected 2026-11-20** (Pages §4.3, §12): measured on PB-039's sections, her body to her drawn line
is 4,325 t moulded, 4,349 t with her keel, 4,443 to 4,473 t outside 3 to 4 pulgadas of plank
(JUDGEMENT on the plank); on the line as traced, 4,421 to 4,452 t. **Ruled (the lead, 2026-11-20):
her file's displacement is that body, about 4,440 t** (the range 4,421 to 4,473 t). To float 5,167
metric tonnes her own body would draw **8.70 to 8.85 m to K** at the middle, not 9.6, a line 0.8 to
0.9 m above her drawn one, in the wale's band, drawn nowhere on the sheet. Read as toneladas of
2,000 libras, 5,167 is about 4,762 t, most likely reckoned level near her after draught (JUDGEMENT;
the book's own mark on the figure, p. 407, would settle it).

### 2.6 Her draught and her lower sills

Not found. VR-Sp gives no draught (*calado*); James gives none; PB-039's two dashed lines are not
identified (§2.4). The lower sills' height above her water decides when her lee ports shut
(package 70's rule, the 74's 5 ft 2 in being the *Bellona*'s report): for her it is to be measured
on ZAZ0101 or PB-039 once a waterline is identified, or read from Winfield if the book gives a battery
height (*altura de la batería*) (§11).

**Corrected 2026-11-20** (Pages §4.2, §5.2, §12.1): measured on PB-039's drawn line, **7.94 m to K at
the middle on the line as traced** (8.02 m at the post's after face, 7.65 m at the stem's fore face;
7.92 m on its straight fit), and her lower sills **1.89 to 2.48 m above it, 1.91 m amidships**; the
midship lee port dips at 13.3°. No source read gives her draught at sea.

---

## 3. The guns by date

### 3.1 The establishments (via Winfield, p. 407)

| Fit | Lower | Middle | Upper | Quarterdeck | Forecastle | Poop | Pieces | Broadside (Winfield) |
|---|---|---|---|---|---|---|---|---|
| As built, 1779 to 1786 | 30 × 36 | 32 × 24 | 32 × 18 | — | — | — | 94 | 1,212 libras (1,308 lb) |
| **1780s, the 1797 fit** | 30 × 36 | 32 × 24 | 32 × 12 | 12 × 8 | 6 × 8 | — | **112** | **1,188 libras (1,282 lb)** |
| **1803, the 1809 fit** | 30 × 36 | 32 × 24 | 32 × 18 | 4 × 8 and 6 × 48-pdr obuses | 4 × 8 and 2 × 48-pdr obuses | 6 × 24-pdr obuses | **116** | **1,508 libras (1,627 lb)** |

**Checked** (observed: `build_td.py`, the fits laid on the scratch three-decker): half of each
fit's pieces by calibre sum to 1,188 libras and 1,508 libras, Winfield's broadsides exactly; the
as-built fit gives 15 × 36 + 16 × 24 + 16 × 18 = 1,212. So the book's three establishments are
self-consistent, and the lower deck's 30 guns are 15 pairs, the sixteenth pair cut in 1791
standing empty in Spanish service (via Winfield).

### 3.2 James's force of the *San Josef* at her capture (read (OCR), vol. 2 p. 51)

"First or lower deck" 30 long 36s ("Spanish caliber"), "Second deck" 32 long 18s, "Third deck" 32
long 12s, "Q.-deck & forecastle" 18 long 8s: 112 carriage guns, 917 men and boys "as enumerated
in the head-money warrants". The *Salvador del Mundo*: 30 long 36s, 32 long 18s, 30 long 12s, 20
long 8s, 112, 850 men. **Conflict** (§9): the second deck's 18s against Winfield's 24s. Winfield's
broadside of 1,188 libras holds only with 24s (with 18s it is 1,092). The design takes Winfield's
(rung B against rung B, the book's figure checked by its own sum; judgement), James in the note.

### 3.3 The calibre in English pounds

The engine reads a gun's `pounder` as its shot's weight in English pounds (the engine's note,
`Design-Package90-Engine.md` §6.3). Two readings are on file:
- **Winfield's pairs:** 1,212 libras as 1,308 lb, 1,188 as 1,282, 1,508 as 1,627: each 1.079 (the book's
  ratio, read off its pairs and not re-derived for use, by the lead's rule).
- **James's rule:** add 1/72nd to the Spanish nominal weight to give the English (vol. 1 p. 46,
  read (OCR)): 1.014.

They differ by 6.4%. The lead's rule binds: the file takes Winfield's pounds, by calibre if the book gives
them (a passage to ask for, §11), else by the book's broadside's pair (judgement: each calibre at the
broadside's ratio), each gun's calibre in libras in its note.
- **The book's own libra, read 2026-11-19** (Winfield et al. 2023, pp. 41-46): **0.4608 kg**, 1.5873
  per cent heavier than the English pound (1.0159), one ratio for every calibre; a gun the book calls
  a "32pdr" fires 32 libras. It agrees with James's 1.014 to within a fifth of a per cent, and not
  with the book's own broadside pairs (1.079), which stay as the book gives them. The owner settled
  the file's way (Dec 9: as her navy named it); the other way's English figures are now the libra's
  (a 36, 36.57 lb: Con-D §5.3).

### 3.4 The obús

The 1803 alteration's 48- and 24-pounder *obuses* (howitzers) are a piece the game does not have:
"a gun is one of long, carronade, swivel" (the engine's note §6.3, measured there: an `obus` kind is
refused at load), while a 48-pounder carronade is taken. No weight, length, charge or crew for
either obús was found. The design carries them as carronades (judgement, §9 of the design), the
*Diana*'s 3-pounder obuses of 1817 the same way, and asks for Winfield's account of the Spanish
obús (§11).

### 3.5 Weights and crews

No weight of a Spanish 36, 24, 18, 12 or 8 was found; the English patterns (`tools/ships/period.py`,
Adye 1804) have no 36. Falconer's QUARTERS (`period.FALCONER_CREW`) has no 36 either: 15 men for a
42 and 13 for a 32. Both are to be asked for (§11); until then judgement (the design's §5).
**2026-11-19:** not in Winfield's passages. By the owner's word they come from other research (the
period's Spanish artillery treatises, for example) or judgement.

**The ordinance of 1803, read 2026-11-19** (Winfield et al. 2023, the table of the ordinance; VR-Sp
§16): a three-decker of 112 carries 30 × 36, 32 × 24 and 32 × 12 in her batteries, 4 × 8 and 8 ×
48-pdr obuses on the quarterdeck, 4 × 8 and 2 × 48-pdr obuses on the forecastle, 6 × 24-pdr obuses
on the poop: 118, the poop's six outside the nominal 112. Its note: *Concepción* carried 18-pounders
in her third battery. Beside §3.1's 1803 alteration (116), two 48-pounder obuses more on the
quarterdeck; her own record stays her fit.

---

## 4. The company

| Source | Figure | Rung |
|---|---|---|
| Winfield p. 407 | **839 men** | B (via Winfield) |
| James vol. 2 p. 51 | 917 men and boys in the *San Josef* at her capture, by the head-money warrants | B (read (OCR)) |
| James vol. 6 p. 407 | the *San Josef* "still allowed her 850 men (50 more than a 110-gun ship's complement)" in British service | B (read (OCR)) |
| Falconer, RATES | a British first rate of 100 guns "manned with 850 men, including their officers, seamen, marines and servants"; six lieutenants, six master's mates, twenty-four midshipmen, five surgeon's mates | B (read (OCR)) |

The 839 is not broken down in VR-Sp: officers, the *marinería* (seamen, ordinary, *grumetes*,
boys), the *tropa* (marine infantry) and the *brigadas de artillería* (the navy's gunners) are
unknown, and so is whether a flagship's figure includes an admiral's staff. James's 917 by the
warrants includes everyone aboard on the day, her admiral's people among them (judgement). James
vol. 2 p. 59 says the Spanish government sent its fleet to sea "so badly manned" (read (OCR)),
which a scenario of 1797 may carry in its people, not her file (judgement).

**Read 2026-11-19: a 112's company by kind** (Winfield et al. 2023, p. 1446 and the two pages
following; the table of the Regulation of 16 October 1803; rung B; VR-Sp §15). The book's columns:
commissioned officers; major officers (pursers, chaplains, surgeons, pilots); sea officers
(boatswains, guardians, caulkers, carpenters, cooks, divers, armourers, lamp men, sailing masters,
quartermasters); infantry; infantry-artillery (the artillery's infantry corps); artillery; seamen;
landsmen; boys. Its "Total" leaves out the commissioned and the major officers.

| A 112 | Commissioned | Major | Sea | Infantry | Inf.-art. | Artillery | Seamen | Landsmen | Boys | Total | All (computed) | Soldiers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1788 | 19 | 10 | 23 | 168 | 57 | 130 | 200 | 230 | 40 | 848 | 877 | 225 |
| 1803 | 19 | 14 | 37 | 200 | 75 | 190 | 240 | 200 | 40 | 982 | 1,015 | 275 |

- The commissioned officers: a brigadier, a capitán de navío, a capitán de fragata, four tenientes
  de navío, four tenientes de fragata, four alféreces de navío and four de fragata.
- The 1788 complements were for peace; in war, as many men again as guns in the main batteries,
  half infantry and half landsmen, and more surgeons (907 or 971 for a 112 by the reading: VR-Sp
  §15).
- **Against her own figures:** her 839 lies 4 per cent under 1788's 877 and within nine of its
  Total of 848; James's 917 at her sister's capture lies nearest the war increase's lower reading
  (907). What her 839 counts her entry does not say (judgement).
- The design files the regulations' company and soldiers (Con-D §6.1).

**Watches.** No Spanish source on her watches was read. The game's King's ships keep two watches,
starboard and larboard; the design takes the same for her (judgement). **Ruling 11** (package
75: a merchantman's master and mate counted as hands of their own watch where the watch is too
small) does not reach her: she is a King's ship.

---

## 5. The rig

**No Spanish source for her masts, yards or sails was read.** What is on file:

- **Steel's rule for the main mast** (Steel 1794 vol. I p. 39, OCR l. 4459-4467, read (OCR)): "The
  length of the lower deck and extreme breadth added together, the half is the length of the
  main-mast", worked for a 74 of 176 ft and 48 ft 8 in (the OCR prints "156"; 224 ft 8 in less 48
  ft 8 in is 176 ft) as 112 ft 4 in. On James's *San Josef* (194 ft 3 in and 54 ft 3 in) it gives
  **124 ft 3 in (37.87 m)**; on Winfield's rebuilt *Concepción* in English feet (201.1 ft and 53.3
  ft) **127 ft 2 in (38.77 m)** (rule; arithmetic). The other masts' and the topmasts' fractions
  follow on the page, lost in the OCR: to read on the page image.
- **Steel's 100-gun column** (vol. I p. 49, OCR garbled): the masts and yards of a 100-gun ship of
  2,164 tons, "taken at the partners; which are at the middle deck in three-decked ships". The
  nearest British first rate's list; to read on the page image. Her 2,457 tons bm are 1.14 times
  its 2,164.
- **PB-078** (catalogue): Romero Landa's sheet of the *Reina Luisa*, a Spanish 112 of 1791, gives
  the sums of her sails' canvas, weight, making and value. Read, it would be the one Spanish
  figure for a 112's canvas (§11).
- **The mizen.** The 74 sails a lateen mizen yard with the course cut at the mast (package 75's
  B3.1; Steel 1794's 74, the *Bellerophon* of 1794). Whether a Spanish three-decker of 1797 or 1809
  set her mizen course on a lateen yard or a gaff (*cangreja*) was not found; the design takes the
  lateen yard for both fits (judgement) and asks (§11).
- **The spritsail and sprit topsail**: not found for her; Nelson's boarders were "supported from
  our spritsail-yard" (Nicolas vol. 2 p. 345), the *Captain*'s, a British 74's. The design takes
  the 74's two yards under the bowsprit (judgement).
- **Royals and studding sails**: not found; the 74's set taken (judgement).

So her rig is rung C throughout, with Steel's rule as its one named rule (British). A Spanish
masting rule of the 1780s, if Winfield or the owner's other books give one, replaces it (§11).

---

## 6. How she sailed

| Account | What it says | Rung |
|---|---|---|
| Brenton (1823), on the *San Josef* | "uniting all the superior qualities of a ship of the line with the sailing abilities of the fastest frigate" | B via Winfield (Brenton's page not found, §0.2) |
| Nelson, on the *San Josef* | "the finest ship in the world" | B via Winfield |
| James vol. 6 pp. 3 to 4 (1813, off Toulon) | the *Caledonia*, the *Boyne* and the *San Josef* "far ahead of the remainder of their fleet" when they engaged the French rear | B (read (OCR)) |
| James vol. 2 p. 59 | of the four prizes of 1797 "only one of them, the San-Josef, became of any value as a cruising-ship" | B (read (OCR)) |
| Winfield (1784) | sea trials from Cádiz, 20 August to 18 September 1784, led to both ships being rebuilt | B via Winfield; the trials' findings not in VR-Sp |
| Winfield (1810) | driven ashore in the storm of 7 March 1810 in Cádiz Bay | B via Winfield |

**Truth candidates** (for the design's §14, judgement): as rebuilt she is a fast ship of the line,
at least the 74's speed on every point and nearer the frigate's; a first rate stays more slowly
than a 74 (no source found for her own time in stays: judgement on her size); she lies to and
wears as a ship. The 1784 trials' findings would be the one source against her as built, which
the game does not sail (§11).

---

## 7. The engine, run

The scratch three-decker (`build_td.py`): the 74's file (`data/ships/seventy-four.yaml`) with its
length scaled 59.2/51.2, its breadths 16.5/14.25, its upper deck made the middle deck and a new
upper deck 2.05 m above it, the quarterdeck, forecastle and poop raised with it; her three tiers at
PB-039's places (§2.4), her lower sills the 74's; Winfield's two fits as "concepcion 1797" and
"concepcion 1809", the obuses as carronades; the 74's rig scaled 1.06 and raised with the decks;
839 men (posts 18, marines 160 by the 74's share, JUDGEMENT, idlers 60, seamen 601), the 74's stations' shares; 4,200 t (and a
copy at Winfield's 5,167 t). Each figure below is observed, seed 7, in the tests' own worlds.

| Probe | Script | What the engine does |
|---|---|---|
| Load | `p1_load.py` | Both fits load; `numbering: by deck` taken; the guns by deck 30, 32, 32, 12 and 6 (1797) |
| The viewer's check | `tools/check_viewer_guns.py` on her file | **clean**: 1797, 106 guns in ports and 6 over the rail; 1809, 104 and 12; the notes those of the probe's own judged quarterdeck and forecastle places |
| The beat | `p2_quarters.py` | "The lower deck: 15 gun crews, 203 men. The middle deck: 16 gun crews, 165 men. The upper deck: 16 gun crews, 98 men. The quarterdeck: six gun crews, 36 men. The forecastle: three gun crews, 18 men." **Not every gun is manned**: "the upper deck, Nos. 15 to 16, and the middle deck, No. 16 gun stand unmanned" (1797; 552 men wanted at the long guns, the marines' 160 kept in their division); in 1809 the poop's No. 3 too (582 wanted) |
| Orders by deck | `p2_quarters.py` | "fire the starboard middle deck" (16 guns), "fire No. 3 gun of the middle deck", "the middle deck's No. 16", "the gun deck" (the lower, 15), "the upper deck", the quarterdeck's and the poop's guns: all taken. A bare "fire No. 3" is refused naming her five or six decks. **"The main deck" names the upper deck**, as on the 74. **"The second deck" and "the third deck"** (James's own words, vol. 2 p. 51) are refused as no order |
| Robbing | `p2_quarters.py` | heeled 12.5° and engaged to starboard, the lower deck's shut crews first ("from the lower deck, Nos. 9 to 13, their ports shut"); with none shut, the quarterdeck's, middle deck's and upper deck's crews by the end that bears least, mixed, the lower deck's last |
| The lee ports by deck | `p2b_heel.py` | on the 74's lower sills: 11 lower ports shut at 12.5°, all 15 at 18°, the middle deck's first 8 at 30°; the robbing's "shut first" reads the lower deck alone |
| Classing | `p3_sail.py` | as the 74: three masts with yards, six head yards (the spritsail and sprit topsail among them) and eight after, square-rigged, no gaff, no schooner's mast (B3.4's rule leaves her a ship) |
| Close-hauled, 15 kn, 67.5° off | `p3_sail.py` | 4.75 kn and 2.7° of heel (2.2° at 5,167 t); the 74 4.92 kn and 3.6° |
| The tack, truth 10's form | `p3_sail.py`, `p3b_variants.py` | **181, 184 and 188 s** from 290, 292.5 and 295° (182 to 189 at 5,167 t); the 74 237, 243 and 258 s. With 590 men the same seconds; with the 74's rudder 196 to 204 s. So her size does not slow her tack: her displacement and her company leave it, her rudder moves it 15 s |
| The wear | `p3_sail.py` | 498 s (the 74 499 s) |
| Hove to | `p3_sail.py` | 1.39 kn at most, 55 to 64° off, hove to and never aback (the 74 1.18 kn, 56.5 to 63.4°) |
| The static polar | `p9_polar.py` | 7.50 kn abeam in 15 kn against the 74's 7.87; best close-hauled 70° in 15 kn, as the 74 |
| The rig by Steel's rule | `p10_design_rig.py` (`v_design.yaml`: 61.3 m, the 74's rig scaled 1.15, hull speed 13.1) | 8.01 kn abeam in 15 kn, between the 74's 7.87 and the frigate-36's 8.19; close-hauled 4.92 kn and 3.4°; the tack 182, 230 and 189 s |
| Her company and her guns | `p11_bill.py` | with 160 soldiers (the bill keeping 135 or 40) four or five crews stand unmanned in either fit, the engine's marines serving no long gun; with 100 soldiers (the bill keeping 60) every crew of both fits is manned, the trimmers 105 and 103 |
| The wheel shot away | `p7_wheel.py` | "steer" refused in the ship's words; the relieving tackles rove in 380 s, the helm at half the wheel's rate; "repair the wheel" done in 2,279 s (the 74 385 and 2,310 s) |
| Her words | `p8_words.py` | "a three-decker", "a first rate", "a first-rate" name no description and rank nothing (`size_rank_of` None; `size_of_words` 0, "a sail"); "a ship of the line" names the 74's file and ranks 4 |
| The pace | `p5_pace.py`, `p5c.py` | alone in truth 51's form 386 and 371 ticks a second against the 74's 408 and 387 (0.95 to 0.96); the frigate hove to off the Lizard with three of the file added as patrolling vessels (a world of this note's own, not truth 7-196's): 68 and 68 against three 74s' 71 and 71 (0.96), three crewed at the first thousand and two after in both (one stands off past the demotion, as the 74's research found); **in truth 7-196's own world** (its body, the three in the frigate's squadron) the engine note measured 72 to 75 against 79 to 81, all three crewed throughout (`Design-Package90-Engine.md` §7), which is the figure the plan cites; **the owner's machine under other agents' load**: ratios only, against the crewed floor of 60 |
| The checkpoint | `p6_checkpoint.py` | at quarters with her guns cast loose, 688,319 bytes raw and 174,381 gzipped against the 74's 637,046 and 167,873; `test_checkpoint`'s bound 2 MB |

---

## 8. Scenarios on the chart

The chart `atlantic-east` holds Cape St Vincent (a mark of the `portugal` block), Cádiz (a port and
its bay's overrides), Cartagena, Ferrol, Toulon and Brest (ports). Spain has a nation and its own
signal book (`data/nations.yaml`; Mazarredo's, package 76).

| Candidate | Fit | On the chart | Notes |
|---|---|---|---|
| **Cape St Vincent, 14 February 1797** | 1797 | yes | Morales de los Ríos's flagship, Jervis's fifteen of the line; her sister taken by boarding; the *Captain*'s wheel shot away. The nations table is one year's picture (Britain at war with Spain from 12 December 1804): the war state is right for 1797, the dates of the table not |
| **Cádiz Bay, 7 to 9 March 1810** | 1809 | yes | the storm that drove her ashore on the French-held shore; a gale at anchor, her ground tackle and her company. Spain was Britain's ally then; the nations table says war (a limitation of the table's, not hers) |
| Brest, 1799 to 1802 | 1797 | yes (`biscay-north`) | the combined fleet blockaded |
| Toulon, 1793 | 1797 (rebuilt 1793) | Toulon is a port | Lángara's flagship with Hood's fleet |
| The Channel, 1780 to 1782 | as built (94) | yes | not a fit the design proposes |

---

## 9. Conflicts

| Subject | The sources | Reading |
|---|---|---|
| The middle deck's guns in 1797 | Winfield 32 × 24; James 32 × 18 (the *San Josef* at capture) | Winfield's, the book's broadside's sum the check (§3.2) |
| Her company | Winfield 839; James 917 at capture by the warrants; 850 in British service | Winfield's for her file; James's day includes a flag officer's people (judgement) |
| The keel and the rebuilt length | Winfield's feet and the book's metres disagree by 0.05 and 0.13 m | the owner re-reads p. 407 (§2.1) |
| The rebuilt length | Winfield 61.30 m (the *Concepción*); James 59.21 m (the *San Josef*) | ZAZ0101 measured; until then Winfield's (§2.2). **Corrected 2026-11-20:** ZAZ0101 59.71 m post to stem; PB-039 61.26 m, ruled her length (§2.2) |
| The breadth | Winfield's *manga* 16.25 m; James's extreme 16.54 m | the plank (judgement, §2.2) |
| The displacement | Winfield 5,167 t; her length and breadth at a 74's block, about 4,000 to 4,300 t | her lines measured (§2.5). **Corrected 2026-11-20:** her drawn body about 4,440 t, ruled; Winfield's figure most likely toneladas, about 4,762 t (§2.5) |
| The Spanish pound | Winfield's pairs 1.079; James's rule 1.014 | Winfield's, by the lead's rule (§3.3) |
| PB-039's title and Winfield | the plan says 112 and pierces the upper works; Winfield says built as 90 with nothing above | the sheet drawn or titled for the later establishment (judgement, §2.4) |
| J1945's date | Winfield and the images README "as taken in 1797"; Greenwich 1799, the fitting at Plymouth | Greenwich's (§2.3) |

---

## 10. What is open

- **Her lower sills above her water**, and her draught: not read anywhere (§2.6). The lee ports'
  truth waits on them. *Measured 2026-11-20 on PB-039* (§2.6).
- **Her displacement** at her sailing water (§2.5). *Measured 2026-11-20 and ruled, about 4,440 t*
  (§2.5).
- **The 839 by kind** (officers, seamen, marine infantry, the navy's gunners, boys). *Met
  2026-11-19 by the regulations of 1788 and 1803 (§4).*
- **Her guns' weights, lengths and crews** by Spanish practice; the obús's. *Not in the passages of
  2026-11-19: other research or judgement.*
- **Her masts and yards** by any Spanish rule; Steel's p. 39 fractions and p. 49 column on the page
  images; PB-078's sails.
- **The mizen**: a lateen yard or a gaff in 1797 and in 1809.
- **The sixteenth lower pair's place** (forward or aft), cut in 1791 and empty in Spanish service.
  *Read 2026-11-20 on ZAZ0100: the aftmost* (Pages §11.3).
- **The 1784 trials' findings.**
- **PB-039's dashed lines**: which is her load line, if either. *Neither, 2026-11-20; her load line
  L0, ruled as traced* (§2.4).
- **ZAZ0100 to ZAZ0103 not viewed**: her sister's lines, decks and colour plan; measured, they
  give the hull as rebuilt. *Viewed 2026-11-20 at 1,280 px only; her comparison* (§0.3).
- **PB_0050** (the Museo Naval): not online; the 1795 deck plan with the cabins.
- **Brenton's page** for the phrase Winfield quotes; **Nicolas's** volume and page for "the finest
  ship in the world".
- **Pictures for the eye**: Stanfield's *Breaking up* (RMG PW6066), the Cape St Vincent paintings
  at Greenwich (BHC0486 to BHC0493, PAG8949), Monleón's Spanish ships at the Museo Naval: none
  vetted for artist, date and licence in this window.

---

## 11. Whom to ask

**The owner** (their books, their decisions; the questions themselves are in the design's §17):
- whether **PB-039** goes into `docs/references/images/` (CC BY 4.0 with its credit line, as the
  *Diana*'s PB-021 did on 2026-11-06), and with it PB-049 and PB-078 when they are read;
- whether her hull is drawn from **ZAZ0100 to ZAZ0103** (her sister's as rebuilt), measured on
  Greenwich's site under the standing Greenwich rule (read and cited by object number, never
  copied, as the 74's draughts were and *Minorca*'s are), or from PB-039 alone (her own as built):
  viewing needs no permission, the choice of hull is the owner's (Dec 10 question 2). *Answered
  2026-11-20:* "Use PB-039 (Recommended)", to "Draw her hull from PB-039 instead?" (Dec Part F).

**Winfield, the passages to ask for by title and class** (the owner sources them; the lead asks):
1. ***Spanish Warships in the Age of Sail, 1700–1860*, the *Purísima Concepción* class, pp. 406 to
   410, re-read for**: the two figures of §2.1 (the keel's feet or metres; the rebuilt length's);
   which length the book's "length" is; any draught (*calado*) or battery height; the breakdown of the 839;
   what the 1784 trials found; where the sixteenth lower pair was cut; the captions of PB_0050 and
   J1945.
2. ***Spanish Warships*, the introduction's sections on measurement, ordnance and manning** (by
   whatever titles the book gives them): the *manga* and *eslora* as measured; *arqueo* and
   displacement; the libra and the English pound **by calibre**; the iron guns' weights by calibre;
   the *obús* (its weight, charge, crew and when it came in); the *dotación* of a 112 by kind; any
   masting or rigging rule (*reglamento de arboladura*), the mizen on a lateen yard or a gaff.
3. ***Spanish Warships*, the *Santa Ana* class (the 112s of 1784 on)**, for the establishment's
   crew and any masting figure, since PB-049 and PB-078 are that class's.
4. ***British Warships in the Age of Sail 1793–1817*, the first rates, the prize *San Josef*
   (1797)**: her British dimensions, armament (the 114 of 1801), complement and any sailing
   remark (the owner's volume; its entries already serve package 75).

**Marked 2026-11-19** (the decisions sheet's Part D): item 1 **not found** (the class's pages not
sent), but for which length the "length" is (the eslora, by the units: §0) and the 839 by kind (by
the regulations instead: §4); item 2 **partly supplied** (the measurements, arqueo and the libra;
the dotación of a 112 by kind; not the guns' weights, the obús or a masting rule); item 3 **not
found** as a class (a 112's crew by item 2's regulations); item 4 **not found**. By the owner's word,
what was not found is filled from other research (ZAZ0101 to ZAZ0103 at her step 1; the period's
Spanish artillery treatises for the weights) or judgement.

**The lead**: the images README's "as taken in 1797" against Greenwich's 1799 (§2.3); the words
"second deck" and "third deck" for the gunnery's owner (§7).
