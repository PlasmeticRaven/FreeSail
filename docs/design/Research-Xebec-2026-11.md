# Research note: the xebec for package 90 (November 2026)

Package 90's preliminary work (the lead's note of 2026-11-18, 00:50 UTC, nudge 15: research and
planning only, documents alone). This is the research note for the third of the package's five
hulls, **the xebec**: a lateen on all three masts, her sweeps a fit, the 14 and the 30 the two
sizes to choose between for the file, the chambequín a fit if cheap, the Spanish navy's and the
Barbary regency's cruiser both (row 90 of `docs/dev/M7-WorkPackages.md`; the lead's notes to the
ships session of 2026-10-29 and 2026-11-06; `VesselReferences-2026-11-Spanish.md` §3). It is in
the form of `Research-Bilander-2026-10.md`, and the design document that follows it is
`Design-Ship-Xebec.md` (its second draft, 2026-11-18). Nothing here is built, and no tracked file in
the tree but the package's new documents was changed. **Revised 2026-11-18 on the critic's
reading:** the small class's span of length (§2.2; the critic's F10), the chebec's classing under
B3.4's rule (§9 item 9; F15), and the units of Forfait's and Willaumez's figures (F19).

**What binds, and is not reopened here.** Build-Ships.md §5.0's principles and its ladder of
evidence; the lateen handling package 75's B3.1 gives as the brief reads it (worn, not tacked; the
yard dipped round the mast); B3.4's schooner's-mast rule and its two classing limits
(`Design-ShipsEngineExtensions.md`; the lead's ruling of 2026-11-06); the regency's cruisers as a
role with their doctrine on package 116's road (a captain's doctrine read from `thresholds:`); the
harbour's shelves (package 96); the wheel shot away and `repair the wheel` (package 116); package
81's checklist for ports and guns (Build-Ships.md §6's postscript); the seats of
`Design-SlaveryAndSuppression.md` §8 (no human at a regency's cruiser's station; a model only
under the transparent brief, once the owner's process has opened it); decision 64 (Spain and the
Mediterranean's factions in every nation-keyed table).

**The ladder of evidence, as this note uses it.** **Rung A**: the period's own record of a hull or
her type, first an original plan or plate, then a period table or text that gives figures (Forfait's
table, Chapman's plate, Lescallier's and Falconer's accounts). **Rung B**: a historian's particular
(Winfield, set down by page in `VesselReferences-2026-11-Spanish.md`; James; Charnock; Shaler; a
newspaper's printed letter). **Rung C**: judgement, marked **JUDGEMENT**. For the hull's lines the
words of Build-Ships.md §5.0 principle 3 follow from these: a plan of her class or a sister's is
**S**, a plan of her type scaled **S†**, a period rule on her own particulars **R**, judgement **T**.

**The marks**, as each fact was found (never upgraded): **read** (the page or catalogue seen),
**read (OCR)** (the text layer only, to check on the page image before it is a game constant),
**catalogue**, **observed** (printed by a scratch probe of the engine, run with `py` from this
tree, the scripts under the session's scratch folder `p90/xebec/` and not filed),
**secondary**, **memory**, **judgement**. Quotations print the long s as s and keep the period's
spelling; none runs past a line or two.

**Units.** Each figure in its source's own unit and in metres: the English foot 0.3048 m; the
Swedish foot (Chapman) 0.2969 m; the *pied du roi* (Forfait, Willaumez, Lescallier) 0.3248 m, its
square 0.1055 m²; the French sea league (*lieue marine*, twenty to the degree) three nautical
miles; the *pie de Burgos* 0.2786 m, though for any Spanish row this note takes Winfield's own
metres and never converts the book's feet (`VesselReferences-2026-11-Spanish.md`, Units).

**In short.**

- **The type.** A long, narrow-floored, broad, low hull with a strong prow (a beak in place of a
  bowsprit) and a stern platform that "projects further behind the counter and buttock than that
  of any European ship" (Falconer 1780, XEBEC); three masts, the fore raked well forward, the fore
  and main "block-masts" with no tops, the mizen with a small top and a topmast; a lateen on each
  (Lescallier pp. 398 to 399; Steel 1794 I p. 237; Röding II cols. 430 to 431). The galley's
  successor, a sailing warship with sweeps (Winfield pp. 1134 to 1136; Charnock III p. 288).
- **The two sizes** (Winfield): 14 to 22 guns with 4-pounders, and 30 to 32 with 8-pounders, the
  larger with a frigate's count of guns but not her weight. The Artillery Regulation of 5 August
  1752 arms the 14 with fourteen 4-pounders and twenty 2-pounder pedreros, the 18 with eighteen
  6-pounders and thirty pedreros, the 30 with twenty 8s, eight 4s, four 2s and twenty-two pedreros.
- **The small class in the record of the period**: the *África* of 14 long 4-pounders and four
  brass 4-pounder swivels, 75 seamen and 38 soldiers, taken off Marbella on 22 February 1799
  (James II pp. 364 to 365); the *Vives* of 12 long 8- and 6-pounders and 65 men (James IV p.
  185); a xebec of 22 guns that out-pulled a British brig at her sweeps in a calm off Cabrera in
  1801 (James III p. 149); the Algerine xebec of 18 guns and 150 men in the squadron of 1815
  (*Niles* VIII p. 280). **The large**: the *Gamo* of 32, twenty-two long 12-pounders, eight long
  8s and two carronades, 319 men, which "sailed two feet to the Speedy's one" (James III pp. 132
  to 134).
- **The one plan of the small class at hand** is Greenwich's *Minorca* (ZAZ4270, c. February
  1778), a "Zebeck of Eighteen Carriage Guns" designed to be built at Port Mahon: 96 ft 9 in on
  the lower deck, 30 ft 6 in broad, 10 ft in the hold, 388 tons (29.49 × 9.30 × 3.05 m). No
  Spanish plan of a xebec was found; Winfield's reproductions are to be asked for.
- **The rig's figures**: Forfait 1788 Table IV (p. 136) gives a French xebec of 20 guns, the
  *Caméléon*, "tout en voiles latines": 118 by 30 *pieds* (38.3 by 9.7 m), the main mast 76 *pieds*
  and the main lateen yard 120 *pieds* (24.7 and 39.0 m), the fore 69 and 108, the mizen 40 and
  about 54, the fore and mizen 48 *pieds* before and abaft the main at the middle. Fincham 1843 (pp. 60 to 61)
  abridges the same table and is not a second source.
- **Handling.** Lateens lie a point nearer the wind than square sails (five points against six:
  Lescallier p. 380; Steel I p. 237); the xebec is the best of rigs close-hauled in a fine sea and
  "the worst of all" in a heavy sea or before the wind (Forfait p. 129; Fincham p. 59); she changes
  sails rather than reefing: large lateens, small lateens, and square sails before the wind
  (Falconer; Fincham p. 60; Lescallier p. 398; Steel); her shrouds are shifted and the yard changed
  round the mast in going about (Lescallier p. 378, "trelucher, ou muder l'antenne"; Steel; Fincham
  p. 60); her people have "at least the labour of three square-rigged ships" (Falconer, from an
  Algerine captain).
- **The sweeps.** A sweep port between every two guns (Willaumez 1831, CHEBEC); nine pairs on
  Chapman's Algerian xebec of 28 guns (Pl. LVIII No. 17); oarsmen crowded between the gunports
  (Monleón's print, Winfield p. 1135, cited). The one period figure of speed under oars is the
  galley's: the best-manned galley made at most a league and a half in the first hour of a perfect
  calm, then three quarters or half a league an hour for a few hours, and soon could make none
  (Forfait p. 126; about 4.5 knots, then 1.5 to 2.25). No figure of a xebec's own was found.
- **The regency's cruiser.** Algiers' navy "formerly consisted of numerous row-gallies and
  xebecs" (Shaler p. 36); in 1815 one xebec of 18 guns and 150 men "taken from the Portuguese, ten
  years old" (*Niles* VIII p. 280), or of 20 guns and 200 men in Cathcart's list (VIII p. 32); the
  Algerine xebecs of Falconer's day mounted 16 to 24 guns with 300 to 450 men, "two-thirds of whom
  are generally soldiers".
- **What the engine does today** (observed, §9): a hull lateen on all three masts loads and sails;
  she is classed a fore-and-after with no yards; her polar lies a point nearer the wind than the
  brig's; she tacks as a schooner does, the lateens flipping sides with no work at the yards (346 s
  in 15 knots, leeway to 37°), and wears in 167 s; she cannot heave to (no head sail, no yard); she
  cannot reef a lateen filed without a band, and `dip` has no meaning for one; and **she has no
  sweeps**: package 82's `oars:` section on a ship file makes her a boat (no bell struck, the
  boat's orders and its swamping), and "out sweeps" is not an order.

## 0. The sources

### 0.1 Held in the repository (rows in `docs/references/README.md`; all public domain by age)

| Short form | Rung | What it gave here (page; access) |
|---|---|---|
| Lescallier 1791 I (`lescallier/...-vol1-ocr.txt`, IA `bub_gb_sj1QAAAAcAAJ`) | A | The chebecs rigged as polacres and what they lose by it (pp. 372 to 373); the lateen mast, its column shrouds "qui se dépassent facilement, lorsqu'on veut changer la voile de côté pour virer de bord" (p. 378), the yard of two fished pieces slung at a third, the two ourses, the brace and the vang, one oblique reef, five points against six (pp. 377 to 380); the galley's marabout and bouffette, the "oreilles de lièvre" before the wind, the square *tréou* on the foremast, and the yards lowered to the deck for rowing (pp. 395 to 396); the feluccas' twelve oars a side (p. 397); **the xebec** (pp. 398 to 399): the galley's two lateens, the foremast raked forward, column shrouds, two square sails one over the other on each mast in too strong a wind, a mizen with a small top and a cap for a one-piece topmast, its shrouds set up on a channel as a ship's (Pl. XXI fig. 3); **the pink** "absolutely" the xebec's rig but less low and less fine, built for cargo, most common in the Neapolitans' and the Spaniards' trade (p. 399, Pl. XX fig. 1); the barque, a xebec's fore and mizen with a pole main (p. 400) (read (OCR); the running heads read as 373, 377 to 380, 395 to 400) |
| Forfait 1788 (`forfait/...-ocr.txt`, IA `bub_gb_AQUHAAAAQAAJ`) | A | Tartanes, polacres and barques re-rigged square in the Atlantic, and the Spanish chebecs of the last war with a square foresail (p. 118); the lateen's penne raised by lowering the heel in a calm to catch the air aloft (p. 120); the lateen the best rig for oared vessels, the yard lowered to the deck leaving only a short mast (pp. 120 to 121); **the galley's speed under oars** (p. 126); the chebec, figs. 37 and 38: the primitive rig of three lateens "le plus complet", kept by Algiers, Tunis and Tripoli, the fore raked forward and tacked on the beak, the after mast raked aft, the best close-hauled in a fine sea and "les plus mauvais de tous les Bâtimens" in a gale, a bad sea or before the wind; the barques and pinks of the same rig in trade, which unrig the lateens in a gale for two square sails of half the area; the Spanish chebec's mixed rig (a pole main of three or four square sails, a lateen mizen under a square topsail, a lateen fore with a square sail for strong winds), which sails well, pitches gently and hinders the oars more than the primitive (pp. 128 to 131); **Table IV, "Chébecs anciens et modernes"** (p. 136), the *Caméléon* of 20 guns in three rigs (read (OCR); the page numbers from the running heads, two of them misread by the OCR and set by their neighbours: to check on the page images) |
| Falconer 1780 (`falconer/...-ocr.txt`) | A | XEBEC (OCR l. 21222 to 21266): the hull, the stern platform, the narrow floor and great breadth, the cambered deck and its gratings, the three ways of sailing her (square sails before the wind, large lateens in a moderate foul wind, small lateens in a storm), the Algerine xebecs' 16 to 24 guns and 300 to 450 men, two-thirds soldiers, and the labour of three square-riggers; LATTEEN-SAIL (l. 11035); Pl. XII fig. 8 (the 1769 plate, not viewed); GALLEY (l. 8994 to 9026): six or seven to an oar in the galleass, the half-galleys of 25 banks, little use but in fine weather; OAR (l. 13085); PINK (l. 13555) (read (OCR)) |
| Steel 1794 I (`steel/...-vol1-ocr.txt`) | A | XEBEC, "Description of foreign vessels", p. 237 (the OCR prints 297; the page checked as 237 by the bilander's research): the block masts, the mizen topmast "lately added, to keep them better to the wind", no bowsprit but a boomkin on the prow to which the bowlines lead, the foremast raking with no stay, its shrouds set up as a cutter's runners "easily shifted when the vessels go about", the yards at a third, worked at the heel by bowlines, the peak by a brace, the strain by vangs; square sails in a fair wind and smaller lateens when it blows hard; "one point nearer the wind"; PINK, BARK and POLACRE among the same pages of foreign vessels (read (OCR); the xebec's page image read by the bilander's research) |
| Röding 1794 II (`roeding/...-vol2-ocr.txt`) | A | SCHEBECKE, cols. 430 to 431, Fig. 279: long, narrow and very sharp, for war and cruising; three masts, the foremost hanging far over; the main and fore rigged as a galley's; the mizen with a small topmast and shrouds set up as a ship's; square sails (*Breefocken*) in strong winds; a beak as a galley's in place of a bowsprit; the stern far overhanging; 12 guns in the smallest to perhaps 40 in the largest, all on one deck; the French begun to give them polacre rig, losing much of their sailing (read (OCR)); PINKE (vol. II, the trade's version; its column not read) |
| Fincham 1843 (`fincham/...-ocr.txt`) | A, derivative | pp. 59 to 61: the lateen in light winds close-hauled, its disadvantage before the wind in a rough sea and its liability to be taken aback; the xebec the most complete lateen rig; three suits; the shrouds shifted in going about and "the yards are worked round the mast by parallels"; the Spanish xebec's lateen fore with square main and mizen; **the table of Ex. 4, the xebec of 125 by 32 ft, which the author's own footnote says is Forfait's** (read (OCR)) |
| Charnock 1802 III (`charnock/...-vol3-ocr.txt`) | B | p. 288: the galley of Malta the representative of the class, the xebec "its sister vessel of war ... manifestly derived from the same stock", little altered in two centuries (read (OCR)) |
| James 1837 (`james/`, the 1886 and 1902 printings) | B | The *África* (II pp. 364 to 365); a merchant xebec of 60 tons laden with horn at Mahon in 1798 (II pp. 221 to 222); the *Gamo* (III pp. 132 to 134); the 20-gun xebec sunk at Oropesa (III pp. 134 to 135); the 22-gun xebec and the *Pasley* (III p. 149); the French xebec-privateer *Espérance* of 150 tons, 10 guns and 54 men (III pp. 267 to 268); the *Vives* (IV p. 185); the lateen xebec-privateer *César* of Barcelona, 4 guns and 59 men (V pp. 127 to 128); the brigs' sweeps in calms (IV pp. 181, 338 to 340) (read (OCR)) |
| *Niles' Weekly Register* VIII, 1815 (`niles/...-vol8-ocr.txt`) | B | The Algerine squadron in a letter from Lisbon of 2 May 1815 (p. 280): "Xebec, 18 guns, 150 men, taken from the Portuguese, ten years old"; Cathcart's list (p. 32): one zebeck of 20 guns and 200 men (read (OCR)) |
| Shaler 1826 (`shaler/...-ocr.txt`) | B | p. 36: the Algerine navy "formerly consisted of numerous row-gallies and xebecs"; before the peace of June 1815 frigates, sloops, a brig, a galley and gunboats; the list of March 1825 (p. 44) still has one xebec (read (OCR)) |
| Foss 1798 (`foss/...-ocr.txt`) | B | A privateer xebec at Algiers with a passport for a square-rigged vessel, condemned as Genoese with false papers (OCR l. 9806 to 9820): the regency's officers read a vessel's rig against her papers (read (OCR)) |
| Coggeshall 1856; *Niles* VI (1814) | B | The Baltimore privateer "Xebec *Ultor*" of 1814: a xebec under the American flag (read (OCR); her rig not described) |

### 0.2 The owner's book (copyright; facts by page in the tree, the text never)

| Short form | Rung | What it gave |
|---|---|---|
| Winfield et al., *Spanish Warships in the Age of Sail, 1700–1860* (Seaforth 2023), pp. 1134 to 1136, as set down by the lead in `VesselReferences-2026-11-Spanish.md` §3 | B (the book's reproductions of plans point at rung A) | The jabeque as the galley's successor against the Barbary xebecs; shallow draught, sweeps enough for the coast, a sailing ship's broadside; the first lateen on all three masts, mixed rigs tried through the century; Monleón's print of a sixteen-gun xebec under oars and foresail (p. 1135, cited, not held); the chambequín, square-rigged on light masting, faster than frigates and lateen xebecs in the waters between, with a smaller crew (*Volante* and *Andaluz* (ii) converted in 1765 for Buenos Aires); few before 1750, the expansion after the peace with Algiers of 1748; the two sizes; the Artillery Regulation of 5 August 1752 |

The ship entries that follow the book's introduction (her dimensions in *pies de Burgos* and its metres,
her men, her guns by date, her sweeps if they are given, the plans the book reproduces and their archive
numbers) are **not in the tree**, and are asked for by title and class (§11).

### 0.3 Consulted online, not held

| Short form | Rung | Standing | What it gave |
|---|---|---|---|
| RMG ZAZ4270, *Minorca* (1779), object 84061 | A (her type's plan) | Greenwich's image, Crown copyright; cited by object number, never copied into the tree | The catalogue: body plan, sheer and half-breadth of an "18-gun Zebec" to be built at Port Mahon, c. February 1778, 1:48, a scroll head; a pencil "Minerva" on it to be ignored (catalogue, read 2026-11-17). Her figures written on the plan were read by package 43b at catalogue resolution (`VesselReferences-2026-10.md` §3.3, read there): "Zebeck of Eighteen Carriage Guns 6 Pdrs & Twenty Swivels", warrant of 10 November 1777, draught approved 3 February 1778; 96 ft 9 in on the lower deck, keel for tonnage 78 ft 6 in, breadth extreme 30 ft 6 in (moulded 30 ft 2 in), 10 ft 0 in in the hold, 388 40/94 tons |
| Chapman 1768, *Architectura Navalis Mercatoria*, Pl. LVIII No. 17, "An Algerian xebec" | A (a period plate) | the plate public domain; read in the 1971 reprint's table of the plate (`architecturanava0000fred`, in copyright; its figures are Chapman's) by package 43b (`VesselReferences-2026-10.md` §3.3) | 130⅓ by 25¼ Swedish ft (38.70 by 7.50 m; 126.9 by 24.6 English ft), draught 9⅔ (2.87 m); 28 guns (sixteen 6-pounders on deck, four 12s on the forecastle, eight 3s on the quarterdeck), 30 musquetoons, **nine pairs of oars**. The plate itself not viewed here |
| Willaumez 1831, *Dictionnaire de marine*, CHEBEC (IA `dictionnairedem00willgoog`) | A (a period dictionary) | public domain | A chebec "armé de 20 bouches à feu" of 120 *pieds* of keel, 32 of beam and 10 deep (38.98 × 10.39 × 3.25 m), an *élancement* of 13 to 14 *pieds* and a *quête* of 8 (4.2 to 4.5 m, 2.6 m); rowed, with a sweep port between each gun; a lighter "demi-chebec" in one war; the foremast strongly raked (read (OCR), the entry found and read through a fetching tool's reading of the Archive's text layer, 2026-11-17: to check on the page image) |
| Wikimedia Commons, Category:Xebecs and Xebecs in art | pictures, checks for the eye | each file's page read for its author, date, source and licence (2026-11-17) | §0.4 |
| Biblioteca Virtual de Defensa; the RAE's archive of O'Scanlan's *Diccionario marítimo español* (1831) | — | — | Not reached: the library's search refused every query tried ("too many terms or not valid"), and the RAE's page answered 403. No Spanish plan of a xebec and no O'Scanlan entry were read (§11) |

### 0.4 Pictures (checks for the eye, never sources of points; none copied into the tree)

| Picture | Artist, date | Where, and its standing | Vetted, and what it is good for |
|---|---|---|---|
| Monleón's xebec under oars and foresail (Winfield p. 1135) | Rafael Monleón y Torres (1843 to 1900) | the Museo Naval's; the book's photograph cited, not held (`VesselReferences-2026-11-Spanish.md` §6) | A sixteen-gun xebec in a heavy sea, a large party at the mainsail, the oarsmen between the gunports on the gun deck. A direct source of the print was looked for and not found (Commons; the web) |
| "Baugean-Chebec espagnol.jpeg" (Commons) | Jean-Jérôme Baugean, engraving of 1814, *Collection de toutes les espèces de bâtimens*; the dealer's title "Chebec espagnol à voiles latines, courant vent largue" | Commons, public domain (PD-old-100, Public Domain Mark); source a dealer (rarecharts.com), 1317 × 951 px | **A candidate to hold** in `docs/references/images/` (public domain, in the period, a Spanish xebec under her three lateens): its artist's dates differ between sources (1764 to 1830 on Commons, 1764 to 1819 elsewhere), to be settled before it is held. Not held by this note: adding it means editing the images README, which this preliminary work does not do |
| "Chebec espagnol en 1826.jpg", "Chebec genois de 14 canons en 1826.jpg" (Commons) | Baugean, 1826 | Commons, sourced from RMG (objects 111560, 111544) | Greenwich's: cited by object number only. A Genoese xebec of 14 guns at anchor, and a Spanish xebec running under lateens |
| "Chebeck-Antoine Roux-p43.jpg" (Commons) | Antoine Roux (1765 to 1835), "Ottoman-Greek Shebek, 1796" | Commons, public domain; photographed from a modern book (Meissonnier 1991) | The Roux school, as the tartane's watercolour; a Levant xebec of the period. A candidate to hold, its source page to be traced first |
| Cammillieri's watercolours, 1804 to 1810 (Commons, Category:Xebecs in art) | Nicolas Cammillieri (1773 to 1860, as Commons gives the dates) | Genoa-Pegli, Civico Museo Navale (e.g. ITA DAG 1089920X, 1089913X), through the Watercolour World; public domain | **Merchant xebecs of the period by name**: "the Pinco *Conception* in battle with xebec *Le Volcan*, 1804" (the museum's title calls the *Conception* a pinco, Commons a xebec: the pink and the xebec side by side), "Xebec *Our Lady of Mount Carmel*, Captain Philip Caboara, 1810". Checks for the trader's fit |
| "Chebec par Nicolas Ozanne vers 1764.jpg" (Commons) | Nicolas Ozanne (1728 to 1811), *Marine militaire*, c. 1764 | Gallica btv1b8626114b; public domain | Before the period; the type changed little (Charnock p. 288). A check only |
| "FMIB 47771 Chebec de 24 canons (années 1750 à 1786)" (Commons) | from Clerc-Rampal 1913 | public domain | A twentieth-century redrawing: not period evidence |
| "JabequedeGuerraHacia1762.jpg" (Commons) | a contributor's own drawing, 2014 | CC BY-SA 3.0 | Neither period nor of a licence the tree takes (public domain or CC BY): not used |

## 1. The type

### 1.1 What the period calls her

- **The hull.** Falconer 1780, XEBEC (read (OCR)): the sails "in general similar to those of the
  polacre, but the hull is extremely different"; a strong prow; the stern "nothing more than a sort
  of railed platform or gallery" projecting beyond any European ship's; built with a narrow floor
  "to be more swift in pursuit" and a great breadth "to carry a great force of sail ... without
  danger of overturning"; very low; the deck cambered from the middle to the sides to clear the
  water, with a platform of gratings along it "whereon the crew may walk dry-footed". Röding II
  cols. 430 to 431: "Ein langes schmales und sehr scharfes Fahrzeug", the stern built far over,
  a beak in place of a bowsprit (read (OCR)). Falconer's QUARTER: a xebec's quarters nearly as a
  galleass's, only somewhat higher (l. 14253) (read (OCR)).
- **The family.** Charnock III p. 288 (read (OCR)): the galley the parent, the xebec its sister
  vessel of war and the intermediate class between it and the Mediterranean ship of war. Winfield
  p. 1134 (B): the galley's successor once the galley could neither match a broadside nor keep the
  sea in winter; a weapons platform and not, as the galley, a weapon.
- **The trade's relatives.** The **pink** (*pinque*) has "absolument aucune différence" of rig
  from the xebec but is less low and less fine, built for burden, most common in the merchant
  navigation of Naples and Spain (Lescallier p. 399; Steel 1794 I p. 237: pinks differ from the
  xebec "only in being more lofty, and not sharp in the bottom, as they are vessels of burthen";
  Forfait p. 129: barques and pinks of the chebec's rig in the Mediterranean's coasting trade)
  (read (OCR)). A merchant vessel called a **xebec** in the period: "a xebec of 60 tons, laden with
  horn" at Mahon in 1798 (James II p. 222) (read (OCR)); Cammillieri's named merchant xebecs of
  1804 to 1810 (§0.4).
- **The name.** Falconer gives CHEBEC and CHABEK for xebeck (l. 24348); Röding's synonyms, Dutch
  *Schebeck*, French *Chebec*, Italian *Sciambecco*, Spanish *Javeque*, English (OCR "Nebec")
  xebec (read (OCR)). Winfield's Spanish is *jabeque* (B).

### 1.2 Who sailed her, 1792 to 1820

- "Les Chébecs appartiennent à tous les Peuples maritimes qui ont des ports sur la Méditerranée,
  soit Chrétiens ou Mahométans" (Lescallier p. 399) (read (OCR)).
- **The regencies**: Algiers, Tunis and Tripoli kept chebecs of the primitive rig (Forfait p. 128);
  "formerly" in numbers at Algiers, later few (Shaler p. 36); one in 1815 (*Niles*) and one in 1825
  (Shaler p. 44) (read (OCR)).
- **Spain**: the navy's jabeques from the 1750s (Winfield, B); "très-grands & très-beaux" in the
  war of 1778, their rig altered (Forfait p. 128); in action through the wars of 1796 to 1808
  (James, §2.3).
- **France**: the King's chebecs built at Toulon, altered rigs (Forfait p. 128); the French
  re-rigged them as polacres (Lescallier p. 372; Röding); privateers (the *Espérance*, 1804).
- **Britain**: the *Minorca* designed for building at Port Mahon (1777 to 1778).
- **The United States**: the Baltimore privateer "Xebec *Ultor*" in 1814 (Coggeshall; *Niles* VI).
- **Genoa, Malta and the Italian coast**: merchant xebecs (Cammillieri; Baugean's Genoese xebec of
  14 guns, 1826).

## 2. The two sizes and the hulls on record

### 2.1 Winfield's classes and the Regulation of 1752 (B, as set down)

| Rate | Main battery | Quarterdeck and after castle | Pedreros |
|---|---|---|---|
| Xebec of 30 | 20 × 8-pdr | 8 × 4-pdr on the quarterdeck, 4 × 2-pdr in the after castle | 22 × 2-pdr |
| Xebec of 18 | 18 × 6-pdr (the 18-gun packet-boat's standard, understood the same) | | 30 × 2-pdr |
| Xebec of 14 | 14 × 4-pdr | | 20 × 2-pdr |

Two sizes: 14 to 22 guns with 4-pounders, and 30 to 32 with 8-pounders; the larger a frigate's
count of guns but not her weight of metal (Winfield pp. 1134 to 1136, B).

### 2.2 The hulls with figures

| Hull | Rung | Length | Breadth | Depth, draught | Guns, oars | Access |
|---|---|---|---|---|---|---|
| *Minorca*, RN, to be built at Mahon, 1778 (ZAZ4270) | A (plan) | 96 ft 9 in on the lower deck (29.49 m); keel for tonnage 78 ft 6 in (23.93 m) | 30 ft 6 in extreme (9.30 m), 30 ft 2 in moulded (9.19 m) | 10 ft 0 in in the hold (3.05 m); draught not read | 18 × 6-pdr, 20 swivels; oars not read | read by package 43b at catalogue resolution; catalogue re-read here |
| Chapman's Algerian xebec, 1768, Pl. LVIII No. 17 | A (plate) | 130⅓ Swedish ft (38.70 m) | 25¼ (7.50 m) | draught 9⅔ (2.87 m) | 28 guns; 30 musquetoons; 9 pairs of oars | read in the 1971 table by package 43b; the plate not viewed |
| The *Caméléon* of 20 guns, Forfait's Table IV | A (table) | 118 *pieds* (38.33 m) | 30 *pieds* (9.74 m; the OCR's "•3°", confirmed by Fincham's 32.0 English ft) | not given | 20 guns | read (OCR) |
| Willaumez's chebec of 20 guns | A (text) | 120 *pieds* of keel (38.98 m) | 32 *pieds* (10.39 m) | 10 *pieds* deep (3.25 m) | 20 guns; a sweep port between each gun | read (OCR, by a fetching tool) |
| *Gamo*, Spanish, 32 guns, 1801 | B | not given (James: "lofty") | | | 22 × 12-pdr, 8 × 8-pdr, 2 carronades | read (OCR) |

**The proportions spread widely.** Length over breadth: *Minorca* 3.2 (her deck over her extreme
breadth), Forfait 3.9, Willaumez 3.75 on the keel, Chapman 5.2. Falconer's "great breadth" and
Röding's "lang und schmal" pull opposite ways, and Chapman's plate is the outlier (judgement: the plate's
Algerian may be measured at a different length, or a narrower corsair; the plate is to be read).
**The small class itself spans about 29.5 to 38 m**: *Minorca*'s 29.5 m on deck for her 18 guns,
and the 20-gun French and Algerian xebecs' 38 to 39 m (the *Caméléon*, Willaumez's chebec), all
inside Winfield's 14 to 22 guns. **No length of a 30 is known** (the *Gamo*'s is not given):
Winfield's entries for the 30 to 32 guns are asked (§11). **Plainly:** the note's first version set
*Minorca* against the 20-gun hulls as small against large; they are both the small class.

### 2.3 The ships in the record, 1798 to 1815 (B)

| Ship, date, place | Guns | Men | What happened | Source |
|---|---|---|---|---|
| A merchant xebec at Mahon, Nov 1798 | — | — | 60 tons, laden with horn, taken in the port | James II pp. 221 to 222 |
| *África*, Spanish navy, 22 Feb 1799, off Marbella | 14 long Spanish 4-pdrs, 4 brass 4-pdr swivels | 75 seamen, 38 soldiers (113) | With a Spanish brig and a second xebec and a Moorish brig in tow, formed in line ahead to receive the British brig-sloop *Espoir* (14 × 6-pdr, 80 men); an hour and a half's fire, boarded and carried; her loss one officer and eight seamen killed, her commander, two officers and 25 seamen wounded | James II pp. 364 to 365 |
| *Gamo*, Spanish navy, 6 May 1801, off Barcelona | 22 long 12-pdrs on the main deck, 8 long 8s and 2 heavy carronades (probably 24s) on the quarterdeck and forecastle | 274 and 45 marines (319) | Decoyed the *Speedy* within hail by closed or hanging ports in April; the *Speedy* could not escape, "as the xebec sailed two feet to the Speedy's one"; tried twice to board; carried by boarding after 45 minutes' cannonade | James III pp. 132 to 134 |
| A xebec of 20 guns, 9 June 1801, Oropesa | 20 | — | Sunk at anchor protecting a convoy | James III pp. 134 to 135 |
| A man-of-war xebec of 22 guns, 21 July 1801, off Cabrera | 22 | — | Engaged the hired brig *Pasley* (54 men); in the calm after the firing "pulled away with her sweeps", and "having more sweeps and more men out-pulled the British brig", reaching Ivica before night | James III p. 149 |
| *Espérance*, French xebec-privateer, 3 Apr 1804 | 10 (perhaps carronades) | 54 | 150 tons; boarded and took the hired cutter *Swift* | James III pp. 267 to 268 |
| *Vives*, Spanish navy, 13 Dec 1806, off Cape San Martín | 12 long 8- and 6-pdrs | 65 | With the corvette *Neptuno* and a brig against the *Halcyon*; "nearly a calm", the brig and the xebec "assisted by their sweeps and boats, hauled off" | James IV p. 185 |
| *César* of Barcelona, a lateen xebec-privateer, 4 Nov 1810, off Cape Sicié | 4 | 59 | Taken by the *Blossom*'s boats in a calm | James V pp. 127 to 128 |
| The Algerine xebec, 1815 | 18 | 150 | Taken from the Portuguese, ten years old, in the squadron that put to sea in April 1815 | *Niles* VIII p. 280 |
| The Algerine zebeck, 1815 (Cathcart's list) | 20 | 200 | | *Niles* VIII p. 32 |

### 2.4 The 14 and the 30, compared for the file

| | The small class ("the 14": 14 to 22 guns) | The large ("the 30": 30 to 32 guns) |
|---|---|---|
| Regulation of 1752 (B) | 14 × 4-pdr, 20 pedreros; the 18: 18 × 6-pdr, 30 pedreros | 20 × 8 + 8 × 4 + 4 × 2, 22 pedreros |
| Ships of the period with their companies | *África* 1799 (14 guns, 113), *Vives* 1806 (12, 65), the 22-gun xebec of 1801, the regency's 18 of 1815 (150) | *Gamo* 1801 (32, 319) |
| A plan at hand | *Minorca*'s (ZAZ4270, 18 guns, rung A for her type once read) | none; the 20-gun French and Algerian figures (Forfait, Willaumez, Chapman) are of the 38 to 39 m hull, the small class's upper end |
| Roles the record gives her | the King's (Spain), the regency's, the privateer (the *César*, the *Espérance*), the trader (the xebec laden with horn; Cammillieri's) | the King's (Spain); the regency's largest |
| Her sweeps | they decide fights in calms (the *Pasley*, the *Halcyon*) | less: the hull is a quarter longer and twice the weight (judgement) |
| Scenarios on 79c's water | off Marbella 1799; off Cabrera 1801 (balearics); the coasting trade of Catalonia | off Barcelona 1801 (the catalan coast) |
| Her comparators in the game | the brig-sloop (26.8 m, 413 t) | the frigate-36 |
| What she asks of the engine beyond the 14 | — | a quarterdeck and forecastle battery and a bigger company; nothing new in the rig |

The design's pick and its reasons are in `Design-Ship-Xebec.md` §0 and its question 1.

## 3. The rig

### 3.1 Masts

- **Three masts**, "the fore-mast raking forward, and the mizen-mast aft, in order to extend the
  sail as much as possible" (Fincham p. 59); the after mast raked aft so that the opposite rakes
  spread the sails over a greater length and free the main's working (Forfait pp. 128 to 129);
  the foremost "weit vorüber" (Röding). The main nearly upright (Steel).
- **The fore and main are block masts**, short and square at the head with sheaves for the jeers
  (Steel; Fincham p. 60), with the galley's *gabie* (a caged top) abaft the masthead (Lescallier p.
  395, said of the galley) (read (OCR)). No tops, caps or crosstrees on them, no topmasts in the
  primitive rig.
- **The mizen** has a small top and a cap for a one-piece topmast, no topgallant over it, its
  shrouds set up on a channel as a ship's, the topmast with two shrouds, futtock shrouds and a
  backstay (Lescallier pp. 398 to 399); "fitted with a topmast, &c. similar to a small English
  ship, and which has been lately added, to keep them better to the wind" (Steel) (read (OCR)).
- **The shrouds** of the fore and main are *à colonne*: a pendant at the masthead, a runner rove
  through its block and set up by a tackle to an eyebolt on the gunwale, "easily shifted when the
  vessels go about" (Lescallier pp. 377 to 378; Steel; Fincham p. 60). The fore has no stay
  (Steel).
- **No bowsprit.** A boomkin woolded to the prow nearly horizontal, to which the bowlines lead
  (Steel); the fore lateen tacked on the beak, the *éperon* (Forfait p. 128); the beak sometimes
  lengthened by a spar, the *berthelot*, for the stays' standing parts and the jibs' tacks (Forfait
  p. 125, said of the galley's beak) (read (OCR)).

### 3.2 Forfait's Table IV, the *Caméléon* of 20 guns (A; read (OCR) on p. 136)

The table gives the one hull in three rigs: (1) "tout en voiles latines"; (2) "le même, avec ses
voiles carrées"; (3) "le même, n'ayant que l'artimon en voilure latine". The OCR of the first
column, its ratios to the breadth (masts) and to the length (yards), and Fincham's version of it:

| Part | Ratio | *Pieds* | Metres | Fincham 1843, Ex. 4 (125 × 32 English ft) |
|---|---|---|---|---|
| Length, breadth | | 118, 30 | 38.33, 9.74 | 125.0, 32.0 ft (the same hull in English feet) |
| Main mast (*mât de mestre*) | 2.533 B | 76, 26 *pouces* thick | 24.68, 0.70 | "hounded 2.4 B" (column 2's ratio, judgement) |
| Fore mast (*trinquette*) | 2.300 B | 69, 23 *pouces* | 22.41, 0.62 | 0.95 of the main (column 2's 69/72) |
| Mizen (*artimon*, "misaine" by the Levant's use) | 1.333 B | 40 | 12.99 | 0.6 of the main |
| The beak (*éperon*) | 0.187 L | 21 or 22 (OCR) | 6.8 to 7.1 | |
| Main lateen yard | 1.017 L | 120 | 38.98 | 0.96 L: Forfait's 120 *pieds* over 125 English feet, a ratio that mixes units (judgement) |
| Fore lateen yard | 0.915 L | 108 | 35.08 | 0.9 of the main (= 108/120) |
| Mizen lateen yard | (illegible) | about 54 (OCR of column 3; Fincham's 0.45 × 120) | about 17.5 | 0.45 of the main |
| The main mast's place | at the middle | | | at the middle |
| The fore's and the mizen's | 0.407 L before and abaft | 48 | 15.59 | 0.407 L |
| Rakes | "16 par pi. en arrière", "16 sur l'arrière", "18 sur l'avant" (OCR, the unit unclear) | | | the fore raked forward |
| Sail area | | 7,408 square *pieds* (OCR; which column unclear) | about 782 m² | 2.63 times a figure the OCR does not give |

Every figure here is to be read on the page image before it is a game constant (§11).

### 3.3 The yards and their gear (A)

- **The yard (*antenne*)**: two long thin pieces of fir side by side for most of the length, bound
  by woolded rope and iron hoops, thickest where it meets the mast; much longer than the mast and
  standing well above it; tapering to a point aloft; the upper end the *penne*, the lower the *car*
  (Lescallier p. 378; Falconer, YARD: the wooldings the steps to the peak). Slung not at its middle
  but at about a third of its length, by a parrel (*racage*) (Lescallier p. 379; Steel; Fincham p.
  60, "about one-third length of the yard from the weather-arm") (read (OCR)).
- **Its lines**: the jeers through the block mast's sheaves (Steel); at the heel two *ourses*,
  "ourse à proue" and "ourse à poupe" (the English bowlines), worked on the weather side; at the
  peak a brace (*osta*) of a pendant and a fall, on the lee side; a vang (*van*) of a pendant and a
  fall nearer the mast to take the strain; the sheet at the clue, sheeted aft and to leeward as the
  wind is more or less oblique (Lescallier p. 379; Steel; Fincham p. 60). The gaskets (*matafions*)
  (p. 380).
- **Taking in**: "Les voiles latines se carguent d'ailleurs comme les autres voiles" (p. 379).
- **Reefing**: "un ris placé obliquement" (p. 379), one reef band slanting across the sail. In
  practice the xebec changed sails rather than reefing (§3.5).
- **Peaking to the air aloft**: in a calm under the land or in the channels of the Archipelago, the
  penne raised by lowering the heel with its ourses lifts part of the sail into the air that moves
  aloft (Forfait p. 120) (read (OCR)).

### 3.4 Going about (A, with the brief's rule)

- **What the sources say**: the column shrouds are cast off "lorsqu'on veut changer la voile de
  côté pour virer de bord; ce qu'on appelle trelucher, ou muder l'antenne" (Lescallier p. 378);
  "these shrouds are easily shifted when the vessels go about" (Steel); "the shrouds ... set up as
  runners to cutters, that they may be shifted when the vessel goes about, and the yards are worked
  round the mast by parallels" (Fincham p. 60); Willaumez's MUDER, read by the bilander's research,
  stands the Levant's lateen yard up in the mast's axis to pass the heel abaft
  (`Research-Bilander-2026-10.md` §1.5, way (b)) (read (OCR)). *Virer de bord* is going about either
  way, tacking or wearing; none of these says which the xebec did.
- **The brief's rule** for the package: the lateen worn, not tacked; the yard dipped round the
  mast. No text read here says a xebec tacked; none says she never did. The rule is taken as
  given; its truth says what the sources say and no more (Design §15).
- **On one side.** A lateen whose yard is not changed lies against its mast on one board (the
  settee's way (c), `Research-Bilander-2026-10.md` §1.5); Fincham p. 59 has the lateen "more liable
  to be taken aback than the common lug" by the wind.

### 3.5 The suits of sails, and the weather (A)

| Source | Before the wind | By the wind, moderate | Strong wind, bad weather |
|---|---|---|---|
| Falconer 1780 | square sails on the main and often the fore, of "an extraordinary breadth" | the square yards and sails taken down and the large lateen yards and sails put up | the large lateens lowered and displaced, and small lateen yards and sails extended on all the masts |
| Fincham pp. 59 to 60 | an extensive square sail for the main, and sometimes the fore; a square main topsail often set when scudding (p. 59) | large lateens | small lateens (p. 60); the square sail "used when it is blowing hard" (p. 59) |
| Steel 1794 I p. 237 | square sails "when the wind is favourable" | the lateens | "smaller latteen-sails, when it blows hard" |
| Lescallier p. 398 | | the lateens | "deux voiles quarrées l'une sur l'autre" on the fore and main in place of the lateens |
| Lescallier p. 395 (the galley) | the two lateens sheeted on opposite sides, "en oreilles de lièvre"; the square *tréou* on the foremast | the ordinary sail | a smaller sail, the *bouffette*; in light airs a larger, the *marabout* or *grande bourde* |
| Forfait p. 129 | the worst of all | the best of all in a fine sea | the worst of all; barques and pinks unrig their lateens for two square sails of half the area |
| Röding II col. 431 | | | square sails (*Breefocken*); the lateens must be unrigged to set them, hence the French polacre rig |

**Reading** (judgement): the large and the small lateens are agreed by the English sources and by
Lescallier's galley; the square sails for running are agreed by all; Lescallier and Röding put the
square sails in a strong wind as well, where Falconer and Steel put the small lateens. Every
change is a sending down and swaying up of yards, not a reef.

### 3.6 The mixed rigs and the chambequín (A, B)

- **The Spanish chebec of the 1770s and after** (Forfait p. 130): a pole main mast with three or
  four square sails; a lateen mizen under a square sail (the ship's mizen topsail, *perroquet de
  fougue*); the fore a single lateen in fine weather and a square sail in a strong wind. It does not
  point as high as the all-lateen, but "boulinent mieux encore que la plupart des autres Navires",
  sails well large and passably before the wind, rises well to the sea and pitches gently; it
  hinders the oars more than the primitive rig (read (OCR)). Fincham p. 59 has the same ("a lateen
  fore, with a square main-sail and mizen"); Forfait p. 118, the Spanish chebecs of the last war
  with a square foresail. Winfield (B): mixed square and lateen plans tried through the century,
  trading the lateen's speed and weatherliness against the square rig's smaller crew.
- **The chebecs rigged as polacres** in France (Lescallier pp. 372 to 373; Röding): sail better
  handled and shortened by the wind's force, but the bowsprit overloads a thin bow, the masts' new
  places spoil her qualities, the lofty masts and more rigging hold the wind against the oars, and
  she "perd une partie de l'avantage de sa marche".
- **The chambequín** (Winfield p. 1135, B): a xebec hull entirely square-rigged on light masting;
  faster than frigates and lateen xebecs in the waters between the Mediterranean and the Atlantic,
  and with a smaller crew; *Volante* and *Andaluz* (ii) converted in 1765 for Buenos Aires, for
  seamen without lateen experience. No spar figures were found.

### 3.7 How she sailed (A, B)

1. **A point nearer the wind**: a lateen vessel lies at five points, 56° 15', a square-rigger at
   six, 67° 30' (Lescallier p. 380, the OCR's "50 minutes" a slip); "one point nearer the wind than
   a square-rigged vessel" (Steel) (read (OCR)).
2. **The best close-hauled in a fine sea, the worst in a heavy sea or before the wind** (Forfait p.
   129; Fincham p. 59: "When sailing before the wind, and in a rough sea, it is the most
   disadvantageous of all sails") (read (OCR)).
3. **Taken aback more readily** than a lug, by the wind (Fincham p. 59).
4. **Fast**: the *Gamo* "sailed two feet to the Speedy's one" (James III p. 132), the *Speedy* a
   14-gun brig of 4-pounders; the narrow floor "to be more swift in pursuit" (Falconer).
5. **Her labour**: "the crew of every xebec has at least the labour of three square-rigged ships,
   wherein the standing sails are calculated to answer every situation of the wind" (Falconer, said
   by a captain of Algiers); the lateen sails are hard to work and must be unrigged in a strong
   wind (Röding).
6. **Light aloft**: the yard can be peaked into the air aloft in a calm (Forfait p. 120); in a
   calm she takes to her sweeps (§4).

## 4. The sweeps

| What | Figure | Source | Rung, access |
|---|---|---|---|
| Sweep ports | one between each pair of guns | Willaumez 1831, CHEBEC | A, read (OCR, by a fetching tool) |
| Sweeps, a xebec of 28 guns | nine pairs | Chapman 1768 Pl. LVIII No. 17 | A, the 1971 table |
| Where pulled | on the gun deck, the oarsmen between the gunports | Monleón's print (Winfield p. 1135) | a picture, cited |
| A felucca's oars | twelve a side; the largest about 50 *pieds* (16 m) | Lescallier p. 397 | A, read (OCR) |
| A galleass's oars | six or seven men to an oar | Falconer, GALLEY | A, read (OCR) |
| The galley's speed | at most a league and a half in the first hour of a perfect calm; three quarters of a league or half a league an hour for some hours more; then nothing (the *chiourme* exhausted) | Forfait p. 126 | A, read (OCR; the fraction "¾" read from an OCR's "\") |
| The same, in knots | about 4.5 kn the first hour; 2.25 or 1.5 kn for a few hours | arithmetic on the French sea league of three miles | judgement |
| The xebec against a brig | "having more sweeps and more men out-pulled the British brig" | James III p. 149 | B |
| A brig's sweeps against sail | the *Wizard*, sweeping "with all her strength", could do no more than keep way with the *Requin* under sail in a light air | James IV pp. 338 to 339 | B |
| Endurance | the *Pitt*'s people upwards of 50 hours at their sweeps | James IV p. 181 | B |
| The rig and the oars | the lateen rig the best for oared vessels, the yards lowered to the deck leaving only a short mast; the mixed rig hinders the oars more | Forfait pp. 120 to 121, 130; Lescallier pp. 373, 396 | A |
| Sail and oar together | Monleón's xebec under oars and foresail | Winfield p. 1135 (B), cited | — |

**Not found**: the number of sweeps of a Spanish xebec of 14 or of 30, the men at each, the time
to ship them, or her own speed under them. Winfield's ship entries may give the oars (*remos*);
asked for (§11).

## 5. The guns

- **The Regulation of 1752** (§2.1, B): the 14's fourteen 4-pounders and twenty 2-pounder
  *pedreros* (swivels); the 18's eighteen 6-pounders and thirty; the 30's battery of 8s on the main
  deck, 4s on the quarterdeck and 2s in the after castle, and twenty-two.
- **As fought** (B): the *África*'s fourteen 4s and four brass 4-pounder swivels (1799); the
  *Vives*'s twelve 8s and 6s (1806); the *Gamo*'s twenty-two 12s, eight 8s and two carronades
  (1801), heavier than the regulation's 8s (a conflict, §10).
- **The regency's**: 16 to 24 cannon (Falconer, in the 1770s); 18 guns (*Niles* 1815).
- **Chase guns**: the galley's batteries in the bow (Falconer, GALLEY; Winfield's two to six bow
  guns, said of the galley); no source read gives a xebec's chasers (§11).
- **The ports**: closed or hanging ports that hid the *Gamo*'s battery until drawn up (James III p.
  132); a sweep port between each pair (Willaumez). The *Minorca*'s port count and sills are on her
  draught, not read here.
- **The weights** of Spanish 4-, 6- and 8-pounders, and the *pedrero*'s, were not found; Winfield's
  weights of broadside are in libras with English pounds beside them, to be taken as the book gives
  them (`VesselReferences-2026-11-Spanish.md`, Units).

## 6. Her companies by role

| Role | Men | Of whom | Source |
|---|---|---|---|
| The King's, the small class | 113 (*África*, 14 guns) | 75 seamen, 38 soldiers | James II p. 365 (B) |
| | 65 (*Vives*, 12 guns) | | James IV p. 185 (B) |
| The King's, the large | 319 (*Gamo*, 32 guns) | 274 officers, seamen, boys and supernumeraries, 45 marines | James III p. 133 (B) |
| The regency's | 150 (18 guns, 1815); 200 (20 guns, Cathcart) | | *Niles* VIII pp. 280, 32 (B) |
| | 300 to 450 (16 to 24 guns, the 1770s) | "two-thirds of whom are generally soldiers" | Falconer (A) |
| The privateer | 59 (*César*, 4 guns); 54 (*Espérance*, 10 guns, 150 tons) | | James V p. 128; III p. 267 (B) |
| The trader | not found | | §11; the game's rule for merchantmen, about five men a hundred tons (`tools/gen_ships.py`, the merchant brig), and Falconer's labour of three square-riggers, pull in opposite directions (judgement) |

## 7. The regency's cruiser

- **Her kind and her years**: §§1.2, 2.3; the regency's navy in 1815 and 1825 (Shaler; *Niles*).
- **Where and when the regencies took ships**: off Cape St Vincent and Lisbon, the Strait, the
  passage from Malta to Gibraltar, Sardinia, the Roman coast, in the months from May to November in
  every dated capture (`Design-SlaveryAndSuppression.md` §7.1, its sources).
- **How they fought**: the Algerine xebec's company two-thirds soldiers (Falconer); the *Gamo*
  tried twice to board before she was boarded (James III p. 133); the galleys "keeping off her
  quarter or bow, so as to be out of the direction of her cannon" in calms (Falconer, GALLEY);
  corsairs lying hid under rocks and in creeks to dart out "malgré le calme & même le vent
  contraire" under oars (Forfait p. 126) (read (OCR)). **Reading** (judgement): close and board,
  the guns and the sweeps to get there.
- **What they did with what they took**: the regency's officers read a vessel's passport against
  her rig and condemned a xebec carrying a square-rigger's papers (Foss); the people taken held as
  captives at the regency's port (`Design-SlaveryAndSuppression.md` §§7.2, 7.3, which this note
  follows and does not reopen).
- **The rule for her file** (`Design-SlaveryAndSuppression.md` §8.2): a regency's cruiser is a
  hull of the world under the regency's flag, never a kind of hull; the xebec is given to the
  player under at least one other flag the sources support (Spain's, France's, and the American
  privateer's).

## 8. Scenarios on 79c's water

| Date and place | Chart | Who | Source |
|---|---|---|---|
| 22 Feb 1799, three leagues off Marbella | `mediterranean-west` | the *África* and her consorts in line ahead; the British brig-sloop *Espoir* to leeward closing | James II pp. 364 to 365 |
| 21 July 1801, off Cabrera, the wind dying after the firing | `balearics` | a Spanish xebec of 22 guns at her sweeps against the hired brig *Pasley* at hers; Ivica before night | James III p. 149 |
| 6 May 1801, off Barcelona, light winds | `catalan-coast` | the *Gamo* (the 30) and the *Speedy* | James III pp. 132 to 134 |
| The coasting trade of Catalonia and the Balearics, any summer | `catalan-coast`, `balearics` | a merchant xebec from Barcelona to Tarragona or Mahon | judgement on Lescallier p. 399 and James II p. 222 |
| May to November, 1793 to 1815, off Cape St Vincent or in the Strait | `strait`, `portugal` | a regency's cruiser against a flag at war with Algiers that day | `Design-SlaveryAndSuppression.md` §7.1 |

## 9. What the engine does today (observed, run 2026-11-17)

The probes ran from this tree with `py`, the tree first on `sys.path` and `freesail.__file__`
asserted under it, writing only to the scratch folder; `git status` was clean before and after.
**The rig in memory**: `brig.yaml` (her hull, 26.8 m on the water, 413 t, the nearest committed
hull to *Minorca*'s size; her company of 121) with every yard, square sail, studding sail, headsail,
staysail, spanker, gaff and boom taken out, and a whole lateen on a lateen yard (package 75's
`tests/rig_fixtures.py` helper `_whole_lateen`, as the lead's tartane and polacre probes are
built) on each of her fore (raked 8° forward), her main and a small mizen stepped 13 m abaft
the middle: 155, 190 and 40 m² (Forfait's *Caméléon* scaled to her length, every figure
JUDGEMENT). It is a probe of the engine's paths, not of her speed.

1. **Classing**: no mast with yards, no head or after yards, no yard to lay aback, not
   square-rigged, no driver, no boom sails, no dipping lugs, no working yards, nothing on a
   schooner's mast; the three lateen yards are not yards (`is_yard` false); each sail is classed
   `lateen` (the untuned row of `data/sail_classes.yaml`) and fore-and-aft (observed).
2. **Her polar** in 15 knots (knots through the water by the angle off the wind): 2.58 at 40°,
   3.77 at 50°, 4.50 at 60°, 5.57 at 90°, 5.61 at 100° (her best), 4.65 at 180°; the closest angle
   with a knot of way 40°, her best to windward 50°. The brig: closest 50°, beat 60°, 7.92 at
   100°, 5.73 at 180°. The lugger: closest 40°, beat 50°, 8.30 at 90°, 6.10 at 180°. So the
   lateens lie a point nearer the wind than the brig's square sails, as Steel and Lescallier say;
   **but before the wind she loses less of her best than the brig does** (her 180° speed 0.83 of
   her best, the brig's 0.72, the lugger's 0.73), where Forfait and Fincham make the lateen the
   worst of all sails there (observed; the speeds low because the brig's hull is heavier than a
   xebec's and the areas are a probe's).
3. **Tack ship** (15 knots, settled 1,200 s close-hauled at 4.58 knots): all hands called; "Ready
   about. Helm's a-lee."; tacked at 346 s, her leeway growing to 37° in stays, coming out at 0.77
   knots; the three lateens flipped to the new lee side with no work at the yards or the shrouds;
   her last words "braced up on the starboard tack", though she has no yard to brace. In 8 knots
   tacked at 378 s; in 6 knots refused: "She has not way enough on her to stay: 1.9 kn through the
   water" (observed).
4. **Wear ship**: "Up helm; brace in the after yards." (she has none); "Wind aft. Shifted over the
   sheets; hauled out and braced up."; wore in 167 s, coming out at 2.79 knots (observed).
5. **Heave to**: refused, "No head sail is set to haul to windward, nor a topsail to lay aback."
   With a square topsail on a mizen topmast added she heaves to by it, the one yard she has being
   her head yards: "Hove to on the larboard tack, mizzen topsail to the mast, helm a-lee" at 600 s
   (observed).
6. **The sail orders**: set plain sail casts off the gaskets and clears away the brails of each
   lateen and hauls out sheet and tack; take in brails up to the yard; furl brails up and furls on
   the yard; trim sets each sheet at the lateen's floor ("the foresail 49° off the centreline");
   `reef` refuses a lateen filed with no band; `dip the mainsail`: "'dip' has no meaning for a
   lateen sail"; `brace up`: "This ship has no yards to brace" (observed).
7. **A second suit** (a small main lateen filed `in_place_of` the main lateen, unbent): the file
   loads; `bend the small mainsail` is refused with the engine's own remedy, "unbend it first, or
   shift the mainsail for the small mainsail"; `shift the mainsail` looks for a spare in the sail
   room (observed).
8. **Sweeps**: "out sweeps" is not an order ("'out sweeps' is not an order this ship
   understands"); "out oars" and "give way" are the boat's orders and refused for a hull with no
   oars. **With package 82's `oars:` section on her file** (28 oars, 150 N and 180 W an oar for
   three men, tiring 2 h, all JUDGEMENT) the engine takes her for a ship's boat manned as a hull
   (`world.movement.is_boat_hull` true): "Out oars: 28 oars shipped, the men lying on them"; "Give
   way together: the full stroke"; **no bell struck** in an hour from 04:10, where 04:30 and 05:00
   were due ("a boat strikes no bell"); the boat's tick (alongside, hoisted in, swamped in a sea
   above her weather) runs on her. Her speed in an air of half a knot: 1.09 knots at a minute, 2.89
   at five, 2.93 at ten, 2.85 at twenty, 2.62 at an hour (observed). The boat's rule that the oars
   are not shipped "with the lug drawing" is keyed on a lug and does not refuse her lateens.
9. **Her mixed rigs by B3.4's rule** (classing only): Forfait's Spanish chebec (a lateen fore, the
   main square with course and topsail, a lateen mizen under a square topsail) is classed with her
   main the one mast with yards, its yards her head yards, the mizen topsail on a schooner's mast
   and her after yard, not square-rigged, her main laid aback to heave to (the polacre's classing:
   her main is her foremost mast with braced yards, so neither of the rule's two limits reaches
   her, the mizen topsail on a schooner's mast being the rule as written); the chambequín, square
   on all three, is a ship (the frigate-36's row) (observed). **Plainly:** the note's first version
   called this "the rule's first limit"; the first limit is a lower square-sail yard on a
   schooner's main (`docs/dev/TuningNotes.md`, "Left, and for whom"), which no rig of hers has
   (Pol-D §5.4 states it once for the package).

## 10. Conflicts

| Subject | The sources | Reading |
|---|---|---|
| Her proportions | length over breadth 3.2 (*Minorca*), 3.75 to 3.9 (Willaumez, Forfait), 5.2 (Chapman); Falconer's "great breadth" against Röding's "lang und schmal" | *Minorca*'s for the small class, the only plan at hand (judgement); Chapman's plate to be read |
| Square sails: when | before the wind (Falconer, Fincham, Steel, Forfait); in too strong a wind as well (Lescallier p. 398, Röding, Fincham p. 59) | both: the square sails for running, the small lateens in a gale by the wind (judgement) |
| Going about | the yard changed round the mast "pour virer de bord" (Lescallier; Steel; Fincham), which says neither tacking nor wearing; the brief's rule, worn not tacked | the brief's rule (it binds), its truth limited to what the sources say |
| The *Gamo*'s guns | the Regulation's 30: 8-pounders (Winfield); James: twenty-two long 12s | a fit by date, not the Regulation's (judgement); Winfield's entry for her asked for |
| The *África*'s swivels | the Regulation's twenty 2-pounder pedreros; James: four brass 4-pounder swivels | two fits: the Regulation's (1752) and hers (1799) |
| Fincham's xebec | given as a second source in `VesselReferences-2026-10.md` §3.3 | the author's own footnote makes it Forfait's table; the 0.96 L mixes units; Forfait's figures stand |
| The mizen's topmast | the primitive rig's mizen a lateen (Lescallier, Steel, Forfait col. 1); the topmast "lately added" (Steel); a square topsail over the mizen lateen in the Spanish rig (Forfait p. 130) | the topmast filed bare in the all-lateen rig; the square topsail with the mixed rig (judgement) |
| Baugean's dates | 1764 to 1830 (Commons), 1764 to 1819 (elsewhere); prints dated 1826 under the name at Greenwich | settled before any of the prints is held |
| `VesselReferences-2026-10.md` §3.3 | calls Fincham's xebec (Ex. 4) independent; gives Steel's xebec page as p. 237 without the OCR's 297 | for the lead's list of corrections (this note edits no other file) |

## 11. What is open, and whom to ask

**From the owner, by title and class** (Winfield, *Spanish Warships in the Age of Sail,
1700–1860*, the owner's edition):

1. The **jabeques of 14 to 22 guns**: the ship entries after pp. 1134 to 1136, at least one class
   of 14 and one of 18, and the *África* (taken 22 February 1799) and the *Vives* (in service in
   1806) if the book has them: her dimensions in *pies de Burgos* with the book's metres, her tons, her men (the
   seamen and the soldiers apart if given), her guns by date, her oars (*remos*) and their
   ports if given, her builder and yard, and any plan the book reproduces with its archive and number.
2. The **jabeques of 30 to 32 guns**, the *Gamo* (taken 6 May 1801) first: the same.
3. The **chambequines** (*Volante*, *Andaluz* (ii), and any others): their masting if given,
   and their dates.
4. Anything of the book's on **how a jabeque was steered** (wheel or tiller), **how she lay to**, and the
   **packet-boat of 18** that the Regulation sets beside the xebec of 18.

**To read, public domain, not reached this time**: Forfait's Table IV on the page image (IA
`bub_gb_AQUHAAAAQAAJ`, p. 136) and the book's figs. 37 and 38; Lescallier's tome II Pl. XXI fig. 3 and
Pl. XX fig. 1 (IA `bub_gb_u_FWAAAAcAAJ`); Chapman's Pl. LVIII (the Sjöhistoriska museet's scan);
Willaumez's CHEBEC on the page image; *Minorca*'s draught at Greenwich's free 1280 px (her ports,
sweep ports if drawn, sills, waterline and draught, her stern platform and beak), kept outside the
repository; O'Scanlan 1831, JABEQUE, CAPA (lying to) and REMO; Bonnefoux and Pâris, CHEBEC;
Pâris's *Souvenirs de marine* for a xebec plan; the *Encyclopédie méthodique, Marine* CHEBEC
(fetched to the cache by package 43b, not read); the Museo Naval's and the Biblioteca Virtual de
Defensa's plans of jabeques (the search to be tried again by title, "Plano de un jabeque").

**Not found anywhere read**: a xebec's own speed under sweeps; the men at a sweep; how a xebec lay
to; the weight of a Spanish 4-pounder; a trader xebec's company.

## 12. The owner's questions

The design's questions (`Design-Ship-Xebec.md` §18) are put there with its picks and their plain
sketches. The research's own, in short:

1. **The size for the file**: the small class at *Minorca*'s size (the design's pick), or the 30?
2. **The sweeps**: a new key of the ship's own, as the boat's oars are hers but leaving her a
   ship (the design's pick), or words only for now?
3. **The passages of Winfield** asked for in §11, items 1 to 4.
