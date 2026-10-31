# Research note: the British coasting bilander and her settee (October 2026)

Phase 1 of `Plan-ShipsWorkflow.md` (§ 2, agent R3, with the critic's gap round). This is the
note the design (Phase 3) and the build (B3 the settee, B4 the vessel) work from. The
owner's rulings in the plan's § 0 are binding and are not reopened here: **the British
coasting bilander of Gwyn's drawing** (RMG PAG3828), with **a real settee main** (the
four-cornered lateen on a long oblique yard) **built on the lug's yard and dipping
machinery, set and clewed up as Lescallier gives it** (p. 390); **unarmed by default, with
an armed merchant fit** of a few small guns and swivels, as the merchant brig's; the era
**about 1792 to 1820**, no year fixed in the file. What the engine needs beyond the lug is
R4's subject; this note gives the period's vessel, rig and handling.

The marks, as the checkers found each fact (never upgraded):

- **read**: the page, image or code was seen. **read (OCR)** where only the OCR text was
  seen and not the page image; check before it becomes a game constant.
- **catalogue**: from a catalogue entry or a catalogue's transcription only.
- **measured**: off an image; the image, the scale and the uncertainty are given.
- **snippet**, **secondary**, **memory**: as they say.
- **judgement**: this note's own reasoning, including arithmetic on read or measured
  figures.

Quotations print the long s as s and keep the period's spelling otherwise. Units: English
feet unless stated; Chapman's Swedish foot is 0.2969 m, 0.974 English feet. Tons by the
builder's old measure, (L − 3/5 B) × B × B/2 / 94.

**In short.**

- The type is real, English (also Swedish and Dutch), and already rare in the period:
  Falconer 1769 and 1780 say few vessels are so rigged, and Steel 1794 that the method "has
  proved inconvenient, and is now seldom used but by the Dutch". Lloyd's Register 1776 to
  1789 has seventeen bilanders verified on the page images, all but two small ones of **80
  to 160 tons, most 120 to 160, drawing 10 to 13 ft loaded**, in short-sea and coasting
  trades.
- **Chapman 1768 Pl. LXII No. 5 draws a bilander's rig to scale**, with her breadth marked:
  about 72.5 Swedish ft on the waterline by 19.9 broad (70.6 by 19.4 English ft), about 120
  to 130 tons (judgement). Her square yards are drawn at half length by Chapman's own
  convention; her settee yard is not. No lines, deck or draught of any bilander was found.
- **The settee's rigging is a ship's whole mizen yard's**: parrel and truss, halyard (jeers),
  peak lift (martinet, the English derrick), a peak brace (the English vangs), two heel ropes
  (ourses, the English bowlines), tacks to windward, the sheet to the taffrail, and buntlines
  and clewlines as for a square course (Lescallier p. 390; Steel 1794 I pp. 207 to 208).
- **Going about is the one real split.** Röding (c. 1795) says the bilander's sail is
  lowered and shifted like a lug's. The English and French practice for the whole mizen
  yard it copies was to **change** it without lowering, peaking it upright against the mast
  and passing the heel abaft (Röding's own DURCHKAIEN, Willaumez's MUDER, the English "change"
  and "peek the mizen"). Leaving it on one side is the third choice. The owner chooses.
- **The sail's cut also splits**: a short luff (Gwyn, Steel's and Kipping's settee rule) or a
  deep one (Lescallier, Chapman). The yard of Gwyn's drawing (about 44°, about 0.7 of the
  length) is what Falconer and Röding describe; Chapman's is flatter and shorter.
- **The armed fit in Lloyd's**: 4 × 3-pounders (Elizabeth, 130 tons), 6 × 4-pounders
  (Kerrison, 140 tons), 2 × 2-pounders (Essex, 160 tons); no swivels recorded.

## 0. The sources

**Held in the repository** (rows in `docs/references/README.md`):

| Short form | Work | File | What it gives here |
|---|---|---|---|
| Steel 1794 I, II | David Steel, *The Elements and Practice of Rigging and Seamanship*, 1794 (IA `bim_eighteenth-century_the-elements-and-practic_steel-david_1794_1` and `_2`) | `steel/steel-1794-rigging-and-seamanship-vol1-ocr.txt`, `vol2` | BILANDER p. 220; Plate 1 (snow, brig, bilander, ketch); the boat's settee sail p. 136; settee launches p. 41; yard proportions p. 40; the mizen yard's rigging pp. 207 to 208; the xebec p. 237; the terms of seamanship and working ship (vol. II) |
| Falconer 1780 | William Falconer, *An Universal Dictionary of the Marine*, 1780 (IA `universaldiction00falc`); the 1769 first edition consulted online (IA `bim_eighteenth-century_an-universal-dictionary-_falconer-william_1769`) | `falconer/falconer-1780-universal-dictionary-of-the-marine-ocr.txt` | BILANDER, YARD, VANGS, BRACE, BALANCE, the French BÉLANDRE; Pl. XII fig. 7 (1769 only) |
| Lescallier 1791 I | Daniel Lescallier, *Traité pratique du gréement*, tome I (IA `bub_gb_sj1QAAAAcAAJ`); tome II, the plates, consulted online (IA `bub_gb_u_FWAAAAcAAJ`) | `lescallier/lescallier-1791-traite-pratique-du-greement-vol1-ocr.txt` | The bilander's sail p. 390, the bélandre p. 404, the brigantin pp. 402 to 403, the lateen pp. 377 to 380, the Bombay dinga pp. 463 to 464, the ship's mizen yard (Livre II), Pl. XVII fig. 7 and Pl. XXII fig. 8 |
| Röding I, II | J. H. Röding, *Allgemeines Wörterbuch der Marine*, Hamburg (the Archive dates every volume 1794; vol. II may be 1795 to 1796) | `roeding/roeding-1794-allgemeines-woerterbuch-der-marine-vol1-ocr.txt`, `vol2` | BILANDER (I col. 304), BEKAJER (I col. about 273), DURCHKAIEN (I col. 494), Ruthen-Segel (II col. 578), Ewer- and Lugger-Segel (II col. 581); the plates (vol. IV, Tab. LXXXIX, IA `_1794_4` leaf 0213) consulted online |
| Chapman 1781 | F. H. af Chapman, *Traité de la construction des vaisseaux*, trans. Vial du Clairbois, 1781 (IA `bub_gb_KdnWSHfxqmUC`) | `chapman/chapman-1781-traite-de-la-construction-des-vaisseaux-ocr.txt` | The Tractat's rules for masts and yards (pp. 98 to 102) and the half-length convention of Pl. LXII (p. 102, § 32) |
| Kipping | Robert Kipping, *Sails and Sailmaking* (1898 printing of the 1847 text) | `kipping/kipping-1898-sails-and-sailmaking-ocr.txt` | Settee sails, pp. 127 to 128 (later than the period; confirms Steel) |
| Lever 1808 | Darcy Lever, *The Young Sea Officer's Sheet Anchor* (1827 printing) | `lever/lever-1827-young-sea-officers-sheet-anchor-ocr.txt` | The mizen yard rigged and its bowline; "to balance the mizen" |

**Consulted online, not held** (public domain unless marked):

| Short form | Work | Where |
|---|---|---|
| Chapman 1768 | *Architectura Navalis Mercatoria*, Pl. LXII (24 rigs to one scale; No. 5 "Billender") | IA `architecturanava0000fred` leaf 0141 (the 1971 Adlard Coles reprint, in copyright; the plate is Chapman's and public domain; only the plate's left half is scanned); Wikimedia Commons `File:Chapman sammmanställning fartygstyper 1768.jpg` (the whole plate, Sjöhistoriska museet, with the original Swedish description) and `File:Snow-rig.jpg` (No. 2) |
| Steel 1796, 1806 | *The Art of Rigging* | IA `bim_eighteenth-century_the-art-of-rigging_steel-david_1796`; `artofriggingcont1806stee` |
| Willaumez 1831 | *Dictionnaire de marine*, 3rd ed. | IA `dictionnairedem00willgoog`; `bub_gb_AMnACmgtRGYC` |
| Romme 1792 | *Dictionnaire de la marine françoise* | IA `bub_gb_w8yr5cT02GIC` |
| Bourdé 1765, 1788 | Bourdé de Villehuet, *Le Manoeuvrier*; Sauseuil's translation *The Manoeuverer* | IA `lemanoeuvrieroue00bour`; `manoeuvererorski00bour` |
| Mainwaring | Sir Henry Mainwaring, *The Seaman's Dictionary* (written c. 1620 to 1623), in *Life and Works*, vol. II, Navy Records Society 1922 | IA `henrymainwaring02manwuoft` |
| Boteler | *Boteler's Dialogues* (c. 1634), ed. Perrin, NRS 1929 | IA `botelersdialogue0000bote` (page images free to view) |
| Complaynt | "The Complaynt of Scotlande" (1549) in *The Naval Miscellany* vol. II (NRS) | IA `navalmiscellany02laug` |
| Lloyd's | Lloyd's Register 1776, 1779, 1781, 1782, 1783, 1784, 1787, 1789, 1790 (Gregg reprints) | IA `hecros1776_201910`, `HECROS1779`, `HECROS1781`, `HECROS1782`, `HECROS1783`, `HECROS1784`, `HECROS1787`, `HECROS1789`, `HEROS1790` |
| EB 1771 | *Encyclopaedia Britannica*, vol. III, SHIP | IA `bim_eighteenth-century_encyclopaedia-britannica_1771_3` |
| Papers | *Pennsylvania Packet*, 1 July 1781; *Caledonian Mercury*, 21 Jan and 11 Sept 1782 | IA `per_the-pennsylvania-packet-or-the-general-advertiser_1781-07-01`, `sim_caledonian-mercury_1782-01-21_9424`, `sim_caledonian-mercury_1782-09-11_9523` |
| TNA | The National Archives' Discovery catalogue: HCA 32 prize papers, ADM 354, ADM 106 (catalogue entries only; not public domain) | discovery.nationalarchives.gov.uk |
| RMG | Royal Museums Greenwich: PAG3828 (Gwyn), PAI2636 and PAI5045 (Isaac Taylor prints) | rmg.co.uk, objects 133776, 152576, 154985 |
| Tacking orders | Sturmy, *The Mariners Magazine* 1684; Newhouse, *The Whole Art of Navigation* 1685; Atkinson, *A Compleat System of Navigation* 1750; Moore, *The Practical Navigator* 1784; Cowley, *The Sailor's Companion* 1741 | IA `bim_early-english-books-1475-1640_the-mariners-magazine-_sturmy-samuel_1684`, `bim_early-english-books-1641-1700_the-whole-art-of-navigat_newhouse-daniel_1685`, `bim_eighteenth-century_a-compleat-system-of-nav_atkinson-james_1750`, `bim_eighteenth-century_the-practical-navigator-_moore-john-hamilton_1784`, `bim_eighteenth-century_the-sailors-companion-_cowley-john_1741` |

**Images downloaded to measure or read** (outside the repository, in
`D:\Projects\FreeSail\owner-notes\bilander\rmg\`; the checkers' copies in its `checker\`):
`PAG3828-gwyn-bilander-large.jpg` (1560 × 1181) with `PAG3828-crop-{hull,masts,settee}-grid.png`;
`chapman-1768-plate-LXII-rigs-No5-bilander-IA-architecturanava0000fred-leaf0141.jpg` (the
checker calls it leaf n140, the same leaf counted from zero), the round-2 overlay
`chapman-plate-LXII-No5-spars-measured-round2.jpg`, the Commons whole plate
`chapman-1768-plate-LXII-whole-commons-Sjohistoriska.jpg` (1772 × 1267) and
`chapman-1768-plate-LXII-No2-snow-crop-commons-Snow-rig.jpg`;
`lescallier-1791-tome2-pl-XVII-sails-fig7-bilander-IA-bub_gb_u_FWAAAAcAAJ-leaf0131.jpg`
with `lescallier-1791-tome2-pl-XVII-fig7-zoom-grid-measured.jpg`;
`lescallier-1791-tome2-pl-XXII-fig8-belandre-IA-bub_gb_u_FWAAAAcAAJ-leaf0141.jpg`;
`steel-1794-vol1-plate-I-snow-brig-bilander-ketch-IA-bim_steel-david_1794_1-n348.jpg` and its
`-crop.jpg`; `falconer-1769-plate-XII-vessels-fig7-bilander-IA-bim1769-leaf0352.jpg`;
`roeding-1794-vol4-tab-LXXXIX-figs521-527-lug-and-lateen-sails-IA-leaf0213.jpg`;
`roeding-vol2-col581-lugger-segel-bilander-IA-leaf0300-crop.jpg`; the Steel crops of pp. 41,
136 and 220; the Lloyd's keys and the row crops in `lloyds-rows\`.

**Held pictures** (`docs/references/images/`): `bilander-line-drawing-psf.webp`, a modern textbook
drawing (Pearson Scott Foresman), not period evidence (judgement).
Gwyn's PAG3828 was held there too until the owner's word of 2026-10-31; it is cited there now, and
kept privately (`owner-notes/bilander/rmg/`).

**Not reached**: HathiTrust (bot check), Gallica (403; so Bonnefoux and Pâris, Pâris's
*Souvenirs* and Baugean's plates there), the Google Books API (quota), DigitaltMuseum (403;
the right half of Chapman Pl. LXII at good resolution), Inman's 1820 English Tractat (no
public-domain scan found; his wording seen only in the 1971 reprint's OCR, secondary), Steel's
*Art of Rigging* Pl. 10 (missing from the one 1806 scan; the 1796 edition has no vessel
plates), and images of RMG PAI2636 and PAI5045 (none online).

## 1. The settee

### 1.1 What the period calls the sail

- **Falconer 1780, BILANDER** (read, OCR l. 2377 to 2396; the 1769 text the same): the
  main-sail a trapezium on a yard hung obliquely in the plane of the ship's length, the
  after end peaked to about 45° and "hanging immediately over the stern", the fore end
  sloping down as far forward as the middle of the ship; the tack to a ring-bolt in the
  middle of the ship's length, the sheet to another in the taffarel. "Few vessels, however,
  are now rigged in this method", probably found more inconvenient than others. "The middle
  of the ship's length" places the tack amidships fore and aft; it does not say on the
  centreline, so it is silent on which side the tack goes (judgement).
- **Steel 1794 I p. 220** (read, page image; the page number checked), "Progressive method
  of rigging two-mast vessels": a two-masted merchant ship whose mainsail resembles a
  settee-sail; the head bent to a yard like a ship's mizen yard, hanging to the main mast as
  a ship's does to the mizen mast; "This method has proved inconvenient, and is now seldom
  used but by the Dutch." The *Art of Rigging* repeats it word for word (1806 p. 110,
  "RIGGING A BILANDER. (Pl. 10.)"; 1796 p. 128 by its index, no plate reference) (read, OCR).
- **Lescallier 1791 I p. 390** (read, page image by the checker; Livre III ch. II art. VI,
  "Des voiles de Bélandre"): the mainsail of a vessel used by the Dutch, a long trapezium
  whose head is bent to a yard on the lower mast, oblique to the horizon and exactly like a
  ship's mizen yard. P. 404: the bélandre is a Dutch cargo vessel rigged exactly as the
  brigantin but for that mainsail (read).
- **Röding I col. 304, BILANDER** (read, page image): a two-masted merchantman used
  especially in England and Sweden; it differs from the brig and the snow in that the great
  sail is a trapezium and its yard "ungefähr einen Winkel von 45° mit dem Mast macht"; the
  upper yard-arm right over the stern or after-body, the lower about the middle of the ship,
  above the deck. French gloss "Espèce de Brigantine".
- **Falconer 1780, YARD** (read, OCR l. 21422 to 21429): lateen yards are usually of several
  pieces fastened by wooldings, which serve as steps to climb to the peek to furl or loose
  the sail; the ship's mizen yard and the bilander's main yard hang obliquely on the mast
  almost as a xebec's, settee's or polacre's lateen yard.

### 1.2 The yard and its rigging

Lescallier p. 390 lists the yard's gear with the letters of Pl. XVII fig. 7; the printed
page and the plate agree (the OCR's "P" and "l, l" are misreadings) (read). The ship's mizen
yard it copies is given in French by Lescallier's Livre II and in English by Steel 1794 I
pp. 207 to 208. Steel opens that section: the mizen yard "Is not often used, except in ships
above 50 guns, and in East-India ships" (read, page image p. 207); Lever 1808 likewise rigs
its bowline "when a Mizen Yard is carried" (read, OCR l. 7192 to 7194). By 1794 the whole
mizen yard was a large ship's fitting.

| Part | Lescallier (letter) | English name | Fitting as given | Source and access |
|---|---|---|---|---|
| Parrel and truss | racage, drosse de racage | parrel, truss | Two rows of trucks and ribs, closed by a truss tackle whose single block hooks to a thimble "tout au bas de la vergue" (the lower end or the underside near the slings; unclear) | Lescallier pp. 155 to 156, § 4 (read, page image; OCR l. 5820 to 5852); Steel's vol. II table lists a truss pendant (read, OCR, rough) |
| Halyard | drisse, p | jeers | French: made fast on the yard where it touches the mast, through a three-sheave block under the top and a two-sheave block on the yard. English: a double block on the yard and one at the masthead | Lescallier pp. 147 to 148, § 8 (read; OCR l. 5557 to 5582); Steel p. 207 (read) |
| Peak lift | balancine ou martinet, o | derrick (peak tackle) | French: from the mizen topmast head through a block at the yard's end and down to the deck, with a second part (also o on the plate) from the topmast head down to the top; "much more complicated in the old method, as still seen in merchant ships". English: the derrick-fall reeves through the double block at the mast-head (cap) and the single block on the yard, between the slings and the peak, and leads to the larboard mizen channel | Lescallier pp. 160 to 161, § 10 (read; OCR l. 5990 to 6020); Steel p. 207 (read, page image). Steel's vol. II table lists "Derrick … Double" and "Span … Single", so he is not wholly consistent (read, OCR) |
| Peak brace | bras, t, t | vangs | English: the bight over the peak end, double blocks and falls to an eye-bolt in the quarter-piece on each side, belayed on the taffrail fife-rail. Falconer: slackened in a fair wind, drawn in to windward in a foul; the mizen yard has vangs in place of braces | Lescallier p. 390 (read); Steel p. 208 (read, OCR); Falconer VANGS and BRACE (read, OCR l. 19724 to 19728, 3128 to 3131) |
| Heel ropes, two | ourses, q | bowlines (Romme also gives "Vang, or mizen bowline") | French mizen: one each side, made fast at the foot of the aftermost main shroud. English: through a single block at the lower end of the yard and a block hooked to an eye-bolt on each side abreast the lower end, or lashed to the mizen shrouds. Mainwaring: the mizen bowline, at the lower end of the yard, "doth serve for a brace to that yard" | Lescallier p. 170, § 12 (read); Steel p. 208 (read, page image); Romme 1792 OURSE, p. 464 (read, OCR); Mainwaring pp. 107 to 108, the brace sentence in the editor's square brackets (read, OCR); Bourdé's glossary HOURSE (read, OCR) |
| Tacks, two | amures, r, r | tack | Made fast below on the weather side. The plate shows the two splayed forward and aft in profile; that they go one to port and one to starboard is inference | Lescallier p. 390 and fig. 7 (read) |
| Sheet | écoute, s | sheet | Made fast at the taffrail (couronnement); Steel's ship's mizen has a horse for the sheets at the taffrail | Lescallier p. 390 (read); Steel p. 208 (read, OCR) |
| Clewing | cargue-fonds, cargue-points | buntlines, clewlines | "comme … pour les voiles quarrées", Livre II ch. III art. VIII §§ 1 and 2, printed "pag. 223 à 228" (the OCR's "115 à 118" is a misreading): art. VIII begins p. 221, clewlines p. 223, buntlines p. 225. Lescallier does not contrast this with the mizen's brails; that contrast is a gloss | Lescallier p. 390 and pp. 221 to 228 (read, page images leaves n248 to n255) |
| Yard's blocks | — | — | Ship's mizen yard: a single block at the peak for the martinet, two at the heel (port and starboard) for the ourses, five or six abaft the mast for the brails, one near the parrel for the clewline, a double block in the middle for the halyard | Lescallier pp. 138 to 139, § 6 (read; OCR l. 5240 to 5272) |

**The English names in this note.** The heel ropes are the **ourses** (English bowlines),
the peak ropes the **brace** (English vangs). Lescallier's ourses are not the English vangs,
though Romme gives both words for them; the plan's § 2 R3 row ("two vangs, brace") and
`VesselReferences-2026-10.md` §§ 3.1 and 3.2 call the ourses vangs (judgement on the
mapping, from Steel p. 208 and Mainwaring).

**Where the yard hangs.** It crosses the mast below the top: in Lescallier's fig. 7 below a
square dry yard; in Chapman about 6 Swedish ft below the main top; in Gwyn about 32 px (about
3 ft at the scale assumed in § 2.3) below it (measured). The share of the yard before the
mast: about a third in Chapman (32 to 33%, measured by the checker at the mast's own centre),
0.395 in Gwyn, 0.41 in Lescallier's fig. 7 (measured); lateen yards hang at about a third
(Lescallier pp. 377 to 380; Steel 1794 I p. 237) (read). So the sail is a whole sail with a
good part before the mast, not a half mizen. Steel's Plate 1 shows the same: the heel
forward of the main mast (read). The ship's lateen mizen yard of old hung on the starboard
side of the mizen mast, its heel 7 or 8 ft above the middle of the quarterdeck (Willaumez
1831 OURSE, read, OCR); Lever lays the mizen yard fore and aft on the starboard side for
rigging (read, OCR).

**The yard's length rules found** (none is the bilander's own):

- Steel 1794 I p. 40, Royal Navy: the mizen yard 6/7 of the main yard (read, page image at
  full resolution). It relates a ship's mizen to her main yard; carrying it to a main-mast
  settee is weak (judgement).
- Steel 1794 I p. 41, launches and cutters with settee-sails (read, page image): main yard
  3½ times the boat's breadth; main mast 4/7 of the main yard; fore mast 17/18 of the main
  mast; fore yard 9/10 of the main yard; masts 3/8 in and yards 1/4 in of diameter a foot.
  On a 19.4-ft breadth 3½ B would be a 68-ft yard, far beyond any drawing; the boat's rule
  does not carry to the vessel (judgement).
- The drawings themselves: § 2.5.

### 1.3 The sail: shape, cut and canvas

| Source | Luff / leech | Leech / head | Foot / head | Yard to horizontal | Access |
|---|---|---|---|---|---|
| Steel 1794 I p. 136, boat's settee sail; Kipping pp. 127 to 128 | 0.20 (the luff, Steel's "bunt", the depth of the reef) | 0.83 (5/6) | not given (foot cut with a circular sweep) | not given; yard at a third | read (Steel page image; Kipping OCR l. 18094 to 18122) |
| Gwyn, PAG3828 | 0.16 | 0.72 | 0.72 | 44° | measured, ±10 px a point |
| Lescallier Pl. XVII fig. 7 | 0.39 | 0.89 | 0.92 to 0.94; foot hollowed 3 to 4% | 32° | measured, ±5% (a schematic plate, ratios only) |
| Chapman Pl. LXII No. 5 | 0.46 | 1.06 | 0.74 | 35° to 36° | measured (the checker's corners, ratios here by arithmetic) |

- **Steel's rule in words** (read, page image p. 136): quadrilateral, of canvas No. 7 or 8;
  the head bent to a lateen yard hung obliquely at a third of its length, reaching to within
  6 in of the cleats; the cloth at the tack cut goring to the nock; "the bunt is of the depth
  of the reef; which is one-fifth of the depth of the leech. The leech is five-sixths of the
  length of the head." The foot cut with a circular sweep after sewing; the reef across the
  sail at one fifth of the leech from the foot, with cringles at the nock and peek. Kipping
  (read, OCR) confirms that "bunt" here is the luff.
- The English sources (Steel, Kipping, Gwyn) give a short luff; Lescallier and Chapman a
  deep one (judgement). The owner's question 2.
- Lescallier's heights in fig. 7 relative to a "deck" (0.63, 0.95, 0.39 of deck to cap, the
  yard 1.07 times it) are **not usable**: fig. 7 has no deck line, and its mast, tacks and
  sheet end on the plate's border (read).
- **Canvas.** Steel's No. 7 or 8 is a boat's canvas. A vessel's mainsail would be of the
  heavy numbers (judgement; the brig's mainsail in `data/ships/brig.yaml` is by Steel's
  "A brig's mainsail", p. 119).
- **Area** on Chapman: about 1,040 square Swedish ft (92 m², about 990 square English ft),
  ±8% (measured).

### 1.4 Setting, trimming, taking in and reefing

- **Setting** (judgement from the sources together): cast off the gaskets aloft (Falconer's
  wooldings are the steps to the peek); let go the buntlines and clewlines; haul the tack
  down on the weather side and the sheet aft to the taffrail (Lescallier p. 390); trim the
  yard. The 1549 *Complaynt*, making sail, hoists the mizen and changes it to leeward once
  the topsail bowline is hauled out (§ 1.5).
- **Trimming** (judgement from read sources): the heel by its ourses (bowlines), the peak by
  its brace (vangs), the peak held up by the martinet (derrick). Close-hauled the heel is
  hauled to leeward by its ourse (Bourdé p. 87; Steel 1794 II p. 316, "brace the bowline
  quite to leeward"), the peak drawn to windward by the vang, slackened when the wind frees
  (Falconer VANGS: "slackened when the wind is fair; and drawn in to windward when it
  becomes unfavourable to the ship's course"), the sheet aft. Steel's xebec (I p. 237, read,
  page image): lateen yards "worked at the lower end by bowlines", the sail extended by a
  sheet at the clue, the upper lee yard-arm by a brace, the strain taken by vangs nearer the
  mast.
- **Taking in**: ease the sheet and tack, haul up the clewlines and buntlines as for a square
  course (Lescallier p. 390, read), and furl on the yard aloft (judgement: Falconer's
  wooldings). No source says the yard was lowered to furl.
- **Reefing**: **one reef band parallel to the foot**, about a fifth of the leech above it,
  on all three drawings: Lescallier fig. 7 (about 0.22 of the leech), Chapman No. 5 (0.16
  to 0.19), Steel's Plate 1 (near the foot) (measured, ±0.05); Steel's rule puts it at one
  fifth (read). So the settee was reefed from the foot as a lug is (judgement; on Lescallier
  the band might be a bonnet's lacing). Lescallier gives the lateen proper "un ris placé
  obliquement" (p. 379), unlike the bilander figure (read, OCR). **The alternative is the
  ship's mizen's balance**: the yard "lowered a little" and the peak rolled up and made fast
  about a fifth in from the yard-arm (Falconer BALANCE, read, OCR l. 1938 to 1948; Lever,
  "Rolling up a Portion of it at the Peak", read, OCR); Steel 1794 II p. 245* says balancing
  is "peculiar only to the mizen of a ship, and the mainsail of those vessels wherein it is
  extended by a boom" (read, page image), and Falconer that it is used "in
  contradistinction to reefing". The owner's question 7.

### 1.5 Going about: dip or not

**The owner's ruling** builds the settee on the lug's yard and dipping machinery (plan § 0),
and the owner's confirmation of 2026-10-17 took "the settee and lateen rule alike" with the
dipped lug (`docs/dev/M7b-WorkPackages.md` l. 1056 to 1058, read). The sources give three
ways for a yard of this kind. Whatever the choice, **the tack goes to windward on every
board** (Lescallier p. 390, read; Steel's lugger, "to the windward-clue a tack, which is
occasionally shifted as the vessel goes about", Art of Rigging 1806 p. 111, read, OCR); the
question is what the yard does.

| Way | What is done | For it | Access |
|---|---|---|---|
| **(a) Dipped, lowered** | Lower the yard, shift the tack, pass the yard and sail round to the new lee, hoist again: the lug's way | **Röding II col. 581** (Ewer- and Lugger-Segel, sails hung at a third with the longer part to leeward): the lee sheet cannot serve as the tack, "so muss es beym Wenden erst gestrichen und durchgekaiet werden" (lowered first, then shifted), and "Das grosse Segel der in England, Schweden und Holland gebräuchlichen Bilander oder Belander ist auf solche Weise eingerichtet". **The only source that speaks of the bilander herself going about.** | read, page image (the column is uncut on the full scan; only the held crop is cut) |
| **(b) Changed, not lowered** | Top the yard up by its peak tackle until it stands up and down the mast, pass the heel round abaft the mast to the other side, haul the tack to the new weather side | The ship's whole mizen yard, which the bilander's copies: **Röding I col. 494 DURCHKAIEN** ("To shift or change the mizen"): in going about a yard with a whole mizen is topped up by the Bekajer and its lower end brought round abaft the mast, so the sail does not lie against the mast; laborious ("eine beschwerliche Arbeit"), hence the half mizen now carried. **Röding I col. about 273, BEKAJER** ("peek-haliard, or topping-lift of the mizen"): formerly the rope that topped up the yard when the mizen was to be changed, led through a block at the mizen topmast (Kreuzstenge), now called the Dirk; the English **derrick** is that tackle (judgement). **Steel 1794 II**: "CHANGE THE MIZEN. Bring the mizen yard over to the other side of the mast" (p. 248*); "To PEEK THE MIZEN. To put the mizen-yard perpendicular by the mast" (p. 255*). **Mainwaring** (c. 1620): "change the mizen, that is bring the yard to the other side of the mast, and so the tack to the other board" (pp. 187 to 188); peaking is the yard "right up and down by the mast", and spilling the mizen is letting go the sheet and peaking it (pp. 178, 187 to 188); Boteler's own version (printed p. 172) leaves out the tack. **Willaumez MUDER** (p. 406): Levant lateen yards changed in going about by standing them up in the mast's axis to pass the heel aft, so that on the other tack the sail is not pressed on the mast; said also of lug sails. **Lescallier p. 378**: the lateen's column shrouds cast off "lorsqu'on veut changer la voile de côté pour virer de bord; ce qu'on appelle trelucher, ou muder l'antenne" | Steel read, page images; Röding read, OCR (col. 494's "without lowering" implied by "auftoppen", not stated); Mainwaring read, OCR; Willaumez and Lescallier read, OCR |
| **(c) Left on one side** | The yard stays on one side of the mast; only the tack is shifted to windward; on one board the sail lies against the mast | Lescallier's two tacks r, r "au côté du vent" allow it, and Röding's own plate (Tab. LXXXIX fig. 521, a copy of Lescallier's fig. 7; vol. IV refers figs. 521, 522 and 527 to SEGEL) shows the fixed mizen-style rig although his text says dipped. The late-century ship's half mizen was so left: Bourdé (1765 pp. 91 to 92) hauls its heel to the lee aftermost main shrouds in stays and leaves it "orienté à demeure" for the new tack. No source says a bilander was worked so | judgement; Bourdé read, OCR |

**When the yard was changed.**

- **In tacking.** Boteler (c. 1634), the orders for going about close-hauled end "set in the
  lee braces fore and aft; shift the mizen; and keep the ship as near the wind as she will
  lie" (NRS 1929 printed p. 163, IA leaf n206; read, page image). The order for trimming
  close-hauled without tacking, on the same page, ends "hale aboard the mizen", so "shift the
  mizen" belongs to going about (read). Sturmy 1684, Newhouse 1685 and Atkinson 1750 put
  "shift the Mizen-tack" between the main bowlines and the fore bowline, and Sturmy and
  Newhouse "hawl over the Mizen-tack to Windward" when trimming by the wind after making
  sail (read, OCR). Cowley 1741 and Atkinson 1750 repeat Mainwaring's "Change the Mizen"
  (read, OCR).
- **Not in late-century tacking.** Moore 1784's ordinary tacking orders never mention the
  mizen; his "haul the After-sails about, shift the Mizen-sheet, and Stay-sail tacks" is
  from a note on being taken aback, and concerns the sheet (read, OCR). With the half mizen
  the yard was no longer changed (Röding cols. 494 and 578; Bourdé) (read). The silence is
  judged to mark the half mizen's coming (judgement).
- **In making sail.** The *Complaynt* (1549): "heise the mys3en and change it ouer to
  leuart", after the topsail bowline is hauled out (*Naval Miscellany* II p. 80; read, OCR).
  The sentence "the order was given to change the mizen, and get the yard to leeward" on
  p. 71 is the 20th-century writer's paraphrase, and the editor's note 5 on p. 80, that the
  evolution was the equivalent of dipping a lugsail, is commentary (secondary).
- **Only in wearing, an analogue.** Lescallier's Bombay dinga (pp. 463 to 464), whose single
  trapezoid sail is "à peu près comme une voile de bélandre", tacked at the stem head and
  sheeted at the mast foot, never goes about but by wearing; in wearing they stand the yard
  up against the mast to shift the sail and pass the sheet forward of the mast (read, OCR).
  Steel 1794 I prints the same account (BOMBAY BARKS, OCR l. 26745 to 26752), so it is not
  independent. An Indian boat; not evidence for the bilander.
- Röding's "Wenden" covers tacking and wearing both (vol. II WENDEN: through the wind, and
  before it, the latter Halsen) (read, OCR), so col. 581 does not say which.

**What the after sail does in stays and in wearing** (the late ship's mizen, the nearest
English rule; its carrying to the settee is judgement):

- Tacking to gain all she can to windward: the mizen hauled out as the helm goes a-lee,
  "brassant en même temps l'ource tout-à-fait sous le vent" (Bourdé 1765 p. 87; Steel 1794
  II p. 316 "brace the bowline quite to leeward") (read, OCR). Sauseuil's 1788 English (p. 77)
  says "to windward"; in the Archive's copy a reader has struck through "wind" and written
  "Lee" (read, page image), agreeing with the French.
- Tacking without trying to gain to windward (staying her suddenly near land or a danger):
  "the mizen is to be hauled quite in the lee braces" when the sails begin to shiver (Steel
  1794 II p. 319) (read, OCR).
- Veering: the mainsail and mizen hauled up and the mizen hauled out again as soon as the
  stern has passed the wind (pp. 321 to 322); the balanced mizen hauled out in a gale to
  keep her to the wind (p. 330) (read, OCR).

**For B3** (judgement): way (a) is the owner's machinery as it stands. Way (b) is the same
machinery with the yard peaked up rather than lowered, so the sail is never struck, and it
needs the peak tackle the settee already carries. Way (c) needs no evolution but makes the
sail's set depend on the board.

## 2. The vessel

### 2.1 The type and the name

- **The English bilander**: two masts, a square-rigged fore, the settee main with square
  topsail and topgallant above it (Falconer, Steel, Röding; the drawings of § 2.3 to § 2.6).
  Lescallier's brigantin, of which she is a variant (pp. 402 to 403, read, OCR): the main
  usually raked aft and the fore a little forward; each with topmast and topgallant mast
  and a ship's square sails, staysails and jibs, "excepté que le grand mât n'a en bas
  qu'une vergue seche, & point de voile quarrée"; mostly merchantmen of 80 to 150
  tonneaux, 200 at most; the English use them most.
- **Another type of the same name**, to be kept apart (read, OCR): Falconer 1780's French
  BÉLANDRE, a small vessel of about 80 tons worked by three or four men, "nowise like the
  English bilander"; Willaumez 1831 BÉLANDRE, a flat-bottomed northern cargo vessel with
  leeboards, the small ones of about 60 tonneaux rigged as a *heu*, whose sail "ressemble un
  peu à celle du senau"; *Encyclopaedia Britannica* 1771, SHIP: bilanders "seldom above
  twenty-four tons", rigged not unlike a hoy. Willaumez and Röding's French index say the
  Spaniards, and some places, call sloops or cutters *bélandre*, which throws doubt on the
  Spanish "bilandras" of § 3.
- **Rare in the period.** Falconer already wrote "Few vessels … are now rigged in this
  method" in 1769 (read), Steel "seldom used but by the Dutch" in 1794 and again in 1806
  (read). The ship's mizen yard itself was by 1794 only for ships above 50 guns and East
  Indiamen (Steel p. 207, read).

### 2.2 Named bilanders, their trades, and the register

Lloyd's Register's key gives "Br, – Billander" in 1781, 1783, 1787 and 1789 (read: 1781 and
1789 images, 1783 and 1787 OCR); the 1790 key drops it with the Maphrodite, Skoot, Pink and
Ketch, and the 1791,
1792 and 1797 keys lack it (read: 1790 image, the rest OCR). The 1781 key also gives the guns
(P after the number and weight for guns of the common construction, C for carronades, N.C.
for the new construction) and the seventh column as the draught loaded, in feet (read).
"Br" in the eighth column is Bristol, the survey port, another code (read).

**The bilanders verified on the row images** (read, from the row crops in
`owner-notes\bilander\rmg\lloyds-rows\`; names under a dash taken from the heading above):

| Name | Code | Tons | Built | Master; owner | Draught | Trade | Register (leaves) |
|---|---|---|---|---|---|---|---|
| Essex | Br s | 160 | River (Thames) 1753 | A. Buskin; Jn Twyman | 13 ft | London–Holland, constant trader | 1776; guns 1781 (leaf 0084) |
| King George | Br | 160 | River 1753 | R. Nicholson; Jn Twyman | 12 | London–Holland | 1776 (0171), 1781 |
| Martha | Br s | 140 | River 1753 | G. Hunter; M. Twyman | 12 | Twyman's trade | 1776; "Bg s" in 1779 and 1782 |
| Princess Royal | Br | 120 | River 1768 | Jn Adie; M. Twyman | 10 | London–Rotterdam | 1776 (0244) |
| Princess of Wales | Br s&d | 120 | River 1744 | Js Dixon; M. Twyman | 12 | Twyman's trade | 1776 (0244) |
| Queen Charlotte | Br | 150 | Shoreham 1762 | Jn Barwick; Twyman & Co | 12 | Twyman's trade | 1776 |
| Duke of York (Wilcox's) | Br | 120 | River 1766 | W. Wilcox; Twyman & Co | 12 | Twyman's trade | 1776 to 1779; "Bg", 130 tons, Baker & Co, London–Rotterdam, in 1784 and 1787 |
| Elizabeth | Br | 130 | Liverpool 1756 | B. M'Ghee, master and owner | 12 | London–Rotterdam, constant trader | 1776; guns 1779 (0079), 1782 |
| Diana | Br | 80 | Poole 1771 | W. Parsons; H. Start (1779: Wm Ferry; Tory & Co) | 10 | "Londn Br." (unclear); 1779 Poole–Newfoundland | 1776, 1779 |
| Hopewell | Br s | 150 | Poole 1749, lengthened 1756 | Jn Corbin, then Jn Gregory; J. & B. Lester (1779: B. Burton, then S. Linthorn) | 12 | Poole–Sunderland/Memel; 1779 "DuN'flnd" over "Po.N'fland", Dublin (not Dartmouth) and Poole to Newfoundland | 1776, 1779 |
| Speedwell | Br s | 100 | New England 1765 | T. Hawkins; Jefferies & Co | 12 | Poole–Newfoundland | 1776 |
| Vigilant | Br s | 150 | Poole 1751 | T. Gregory; Sam. Spratt | 12 | Poole–Newfoundland | 1776 |
| Bien Ami | Br | 30 | Dunkirk 1770 | J. Van Stein | unclear | Dunkirk–London | 1776 |
| (name unresolved) | Br | 50 | New England 1762 | S. Waters; Neave & Co | — | San Sebastián–Poole | 1776 (0176) |
| Kerrison | Br | 140 | Yarmouth 1778 | E. Thomas; Kerrison & Co | 10 | Yarmouth–Cork | 1779; guns 1781 (0163), 1782, 1783 (0186) |
| "(?) Return" | Br | 100 | Ipswich | J. Ellard; F. Dye & Co | 10 | Yarmouth–Cork | 1779 ("Happy Return" fits the neighbouring entries; unverified) |
| Duke of York of Bristol | Br | 130 | Bristol 1762/63 | J. White, James, R. Thomas, Jos. Oates, F. Cook in turn; Rd Cox & Co, then Lunnell | 11 | Bristol–Dublin, constant trader | "Bg" 1776 (0079) and 1779 (0071); "Br" 1782 (0078), 1784 (0079), 1787 (0080), **1789** (HECROS1789 n82); "Bg" 1790 (HEROS1790 n85, F. Cooke, "Br Bord'x") |

"s" and "s&d" after the code are as printed; the keys read do not explain them here.

**What the register shows** (judgement unless marked):

- The verified British bilanders were **80 to 160 tons, most often 120 to 160**, with a
  50-ton New England-built and a 30-ton Dunkirk-built one below; built 1744 to 1778, many on
  the Thames or at Poole; **drawing 10 to 13 ft loaded**, 10 to 12 ft for those of 120 to 140
  tons; in short-sea and coasting trades: Twyman's London–Rotterdam constant traders,
  Poole–Newfoundland fish, Yarmouth–Cork, Bristol–Dublin.
- An OCR search found about 14 "Br" entries in 1776, 11 in 1779, 4 in 1781, 3 in 1782 and
  1 each in 1783, 1784, 1787 and 1789 (lower bounds: the OCR misses rows; read, OCR, then
  verified on images).
- **The code changed both ways**: the Bristol Duke of York went Bg, Br, Bg under the same
  owner, and in 1790 the code left the key with others. So a re-coding to Bg is not proof
  that a vessel was re-rigged, and 1790 is a change in the register, not the rig's end
  (read for the entries; the reading judgement). The rarity rests on Falconer and Steel.
- **Poole and Newfoundland** (catalogue): the George "billander" of Mr Tito (or Teto) of
  Poole, with fish for England or Portugal, was impressed at Burin in 1762 by Captain Graves
  to carry his dispatches home (TNA ADM 354/170/17, C10258663; /32, C10258678); Gamaliel
  Stanning wrote in 1778 of 12 years as mate and master in "the Nancy bilander of Mr. Clark
  of Pool, deceased" (ADM 106/1245/41, C14182021).

### 2.3 Gwyn's drawing measured

**The drawing** (catalogue): RMG PAG3828, "British bilander showing sails and rigging and
separate view of the stern", Edward Gwyn, c. 1780, pen and ink and watercolour, 209 × 276 mm,
page 21 of the Gwyn sketchbook (PAG3807 to PAG3869), not on display; the sketchbook's title
page reads "E. Gwyn 1769" (PAG3869), so the drawings may be earlier than c. 1780. The
drawing is inscribed "A Bilander" (read). Free large image 1560 × 1181 px.

**What it shows** (read; the bow to the left):

- Fore mast: course, topsail and topgallant set; a jib on the jib-boom and a fore topmast
  staysail.
- Main mast: topsail and topgallant set, the topsail sheeted to a square dry yard
  (crossjack) just under the main top; a long pole with a pennant at the truck.
- The settee yard slung on the main lower mast just below the top; its peak high over the
  stern, its fore end about midships a few feet above the rail; the tack near midships, the
  sheet to the taffrail; the sail inside the near main shrouds.
- Hull: a raised quarterdeck with a rail from abaft the main shrouds to the stern; side steps
  in the waist just forward of the main mast; channels with about six deadeyes at each mast;
  a figurehead with head rails; no gun ports seen; a red ensign on a staff at the taffrail
  (not at the peak, as the images README has it). Something hangs just abaft the head,
  perhaps a catted anchor (judgement). No boat is shown.
- The stern, drawn apart: rounded, three oval windows on a blue ground, a red band, the
  rudder.

**Measured** (pixels on the 1560 × 1181 image, ±10 px a point, a freehand profile assumed
free of perspective; spot re-measured by the checker within the error):

| Feature | Pixels | As a fraction |
|---|---|---|
| Length at the rail, stem head to taffrail (figurehead excluded) | about 785 | 1 |
| Length on the waterline | about 695 | 0.89 of the rail |
| Main mast from the taffrail | — | 0.41 of the rail length |
| Fore mast from the taffrail | — | 0.81 (0.19 from the stem) |
| Settee yard | 564 (557 re-measured) | 0.72 of the rail length; 44° (43°) to the horizontal |
| Yard before the mast | — | 0.395 of the yard |
| Yard's fore end and the tack, from the taffrail | — | 0.60 and 0.58 of the length |
| Peak, inside the taffrail | about 70 | about 0.09 (measured by this note on the full image, ±15 px) |
| Sail: luff, leech, head, foot | 61, 385, 534, 387 | luff/leech 0.16, leech/head 0.72, foot/head 0.72 |
| Main mast, deck to top; deck to truck | 273; 743 | 0.35 and 0.95 of the rail length |
| Fore mast, deck to truck | 665 | 0.85 |
| Freeboard in the waist | 64 (68) | 0.08 |
| Quarterdeck rail above the waterline | about 112 | 0.14 |

**At an assumed scale** (judgement; the drawing has no scale, its two figures on deck would
make the hull about 290 ft and its ladder rungs suggest 6 to 10 px/ft): at 72 ft on the rail
(10.9 px/ft), the waterline is about 64 ft, the settee yard 52 ft, its leech 35, head 49,
luff 6 and foot 35 ft, the main mast 25 ft from the deck to the top and 68 ft to the truck,
the yard slung about 22 ft above the deck, the peak about 49 ft above the waterline, the
waist's freeboard about 6 ft. Seventy-two feet on the rail is about 139 tons at a 21-ft
breadth (judgement). Multiply every figure by the chosen scale's ratio.

### 2.4 Chapman's bilander, to scale

**What the plate is.** Chapman 1768 Pl. LXII draws the rigs of 24 types to one scale; No. 5
is the "Billender" (No. 1 Fregat, 2 Snaw, 3 Kitz eller Hukare, 4 Brigantin eller Brigg, 5
Billender, 6 Scooner) (catalogue: the Swedish description transcribed with the Commons
image). None of Chapman's hull plates is cross-referred to No. 5, so he gives no bilander
lines (read, OCR search of the 1971 edition).

**Its conventions** (catalogue for the 1768 description; read for the Tractat):

- The square yards are supposed braced at 60° to the middle line, so their real lengths are
  twice what is drawn: "Råernes värkeliga längder äro dubbelt större än hvad de synas på
  Ritningarne" (1768, as transcribed; the 1971 translation's "more than twice" is not what the
  Swedish says). The Tractat agrees: "Les vergues y ont leur demi-longueur" (Chapman 1781
  p. 102, § 32, read, page image; not p. 104, § 31, as the references README row has it).
- All the figures are to the one scale drawn on the plate; the two short vertical lines
  under each figure (a and b on No. 1) mark the vessel's breadth.
- **The settee yard is not halved** (judgement on measured figures): it lies fore and aft;
  drawn, it reaches from about midships to about 10 ft inside the taffrail, as the bilander's
  yard should; doubled it would be about 84 ft, longer than the hull. No. 6's main boom,
  also fore and aft, overhangs her stern by about 7.7 ft as drawn.
- **The ×2 rule checked**: No. 2's main topsail yard, drawn 108 to 110 px on the Snow-rig
  crop (5.66 to 5.72 px per Swedish ft), is 37.8 to 38.9 Swedish ft at ×2, against 37.4 to
  38.6 by Chapman's own frigate rule for a snow (measured; the rule read).

**The scale** (measured): the scale bar is diagonal with three rows, S (Swedish feet), E
(English) and F (French). On the Commons whole plate, 2.749, 2.81 and 2.98 px a foot, in the
true ratios of the feet within about 1%. The IA leaf, registered to the Commons plate by
five points (residuals under 1 px), is **9.72 to 9.79 px per Swedish ft horizontally**
(10.0 to 10.05 px per English foot); the IA leaf's own partial scale sits in the gutter and
under-reads. The two scans differ by 5.5% vertically; a third scan (Snow-rig) agrees with
the IA leaf within 1.5%, so the IA leaf is taken as square and **vertical lengths carry
±4%**. Round 1's 9.92 px per English foot is superseded. All figures below are Swedish feet
at 9.79 px, with English feet beside them.

**Hull** (measured):

| Figure | Swedish ft | English ft | ÷ waterline | Error |
|---|---|---|---|---|
| Breadth (the two marks, 194.9 px apart) | 19.9 | 19.4 | 0.274 | ±1.5% |
| Waterline, sternpost to stem | 72.5 | 70.6 | 1 | ±1.5 to 2 ft (where the stem is read) |
| Taffrail to stem head | 77.6 | 75.6 | 1.07 | ±2% |
| Overall to the head | about 85 | about 83 | 1.17 | ±2% |
| Rail above the waterline | 5.4 to 5.6 | 5.3 to 5.5 | 0.076 | ±0.5 ft |
| Waterline length / breadth | 3.6 | | | |
| Draught | not drawn (every figure stands on the sea band) | | | |

**Tonnage** (judgement): (L − 0.6 B) × B × B/2 / 94 with B = 19.4 English ft and L between
the waterline (70.6) and the taffrail-to-stem-head length (75.6) gives **about 118 to 128
tons**, the middle of the Lloyd's bilanders (Elizabeth 130, Kerrison 140). Round 1's 150 to
170 tons (an assumed 22-ft breadth) is withdrawn.

**Masts** (measured; heights above the waterline, ±4% and ±0.5 ft in reading; the deck is
somewhere under the rail, about 5.5 ft above the waterline):

| Figure | Main | Fore |
|---|---|---|
| At the rail: from the sternpost / from the stem | 0.41 of the waterline forward of the sternpost (29.7 Sw ft) | 0.148 abaft the stem (10.7 Sw ft; Steel's 3/20 is 0.15) |
| At the cap | 0.376 forward of the sternpost | 0.131 abaft the stem (the Tractat's 4/31 is 0.129) |
| Apart | 31.9 Sw ft (31.1 English) at the rail; 35.8 at the caps | |
| Rake | aft about 2.8° | nearly plumb (the two readings within their error) |
| Top | 46.5 (45.3 English) | 38.1 (37.1) |
| Lower cap | 54.1 (52.7) | 44.5 (43.3) |
| Masthead | 7.7 | 6.4 |
| Topmast, heel to cap | 31.2 (hounded 28.1, head 3.1) | 30.5 (hounded 27.3, head 3.3) |
| Topgallant mast with its pole, above the topmast crosstrees | 19.3 | 19.1 |
| Truck | 93.9 (91.5) | 84.5 (82.3) |

The main top is about level with the fore cap (46.5 against 44.5), Chapman's rule for brigs
(read, Tractat p. 102). The topsail yards are drawn hoisted close under the topmast
crosstrees. The mast positions first reported (0.376, 0.131, 35.8 ft apart) were taken at
the caps; **use the rail positions** for the hull.

**Square yards** (measured, at twice the drawn length, ±0.6 ft at the ends and ±1.5% in
scale):

| Yard | Drawn px | Swedish ft | English ft | Ratio |
|---|---|---|---|---|
| Fore yard | 206 | 41.9 | 40.8 | 0.578 of the waterline |
| Fore topsail yard | 150 | 30.8 | 30.0 | 0.735 of the fore yard (Tractat 0.79) |
| Fore topgallant yard | 101 | 20.6 | 20.1 | 0.67 of the topsail yard (Tractat 0.7) |
| Main topsail yard | 154 | 31.5 | 30.7 | equal to the fore's within error, as Chapman's brig rule has it |
| Main topgallant yard | 101 | 20.6 | 20.1 | |
| Main course or dry yard | **none drawn** | | | the main topsail's clews come down to the main top about 34 ft apart at ×2 |

Round 1's report of a dry yard on No. 5 is withdrawn; the checker found no lower yard on her
main (read). The game's Harpy has a fore yard of 52 ft on 88 ft of waterline, 0.59
(`data/ships/brig.yaml`, read), against No. 5's 0.578.

**The settee** (measured; the checker's corners: peak (198, 2032), heel (532, 2269), tack
(527, 2470), clew (223, 2464) in IA leaf pixels):

| Figure | Swedish ft | English ft |
|---|---|---|
| Yard (409.5 px) | 41.8 | 40.8 (12.45 m) |
| Angle to the horizontal | 35.4° (37° on the Commons plate's proportions) | |
| Share before the mast | 32 to 33% (at the mast's own centre where the yard crosses it) | |
| Slings above the waterline | 41.6, about 6 ft below the main top | 40.5 |
| Heel above the waterline; peak | 32.7; 57.2 | 31.8; 55.7 |
| Heel's place | about 3 ft forward of the waterline's middle | |
| Peak's place | about 10 ft inside the taffrail | |
| Horizontal span of the yard | 34.1 (0.44 of taffrail to stem head) | 33.2 |
| Luff (heel to tack) | 20.5 | 20.0 |
| Foot | 31.1 | 30.3 |
| Leech | 44.2 | 43.1 |
| Tack | about 6.8 above the rail, on a tackle, about midships | |
| Clew | near the taffrail | |
| Reef band above the foot | 0.16 to 0.19 of the leech | |
| Area | about 1,040 sq ft, ±8% | about 990 sq ft (92 m²) |
| Yard as a ratio | 0.58 of the waterline, 0.54 of taffrail to stem head, 2.1 × the breadth | |

On the plate the settee yard as drawn equals the fore yard's true length (41.8 and 41.9);
whether Chapman meant this is not stated (judgement).

**Bowsprit** (measured): from the stem head to the cap 26 to 29 Swedish ft by where the stem
is read (28.5 at the stem head), steeved about 29°; the jib-boom 15.3 ft beyond the cap, its
inboard part not visible. The Tractat's rule is shorter: outboard 1.15 times the breadth for
frigates and so for brigs (22.9 ft), 1.1 for barks; the steeve 4 in 7 (about 30°) for
frigates and 3 in 7 (about 23°) for barks (Tractat pp. 99 to 100, read, page images).

**The Tractat's rules for merchant masts and yards** (Chapman 1781 pp. 98 to 102, read, page
images): main yard 0.52 of the length from stem to sternpost (frigate-built); main topsail
yard 0.79 of the main yard; main topgallant yard 0.7 of the topsail yard; the fore yards 9/10
of the main's; topgallant masts to the stop 0.54 of the topmast; the foremast 4/31 of the
length from the stem. Brigs and snows take the frigate's foremast, its appendages and
bowsprit; a brig's main mast is such that its top is level with the fore cap, and her main
topmast, main yard and main topsail yard are the fore's; a snow's main yard and topsail yard
are a frigate's. Barques: main yard 0.6 × L^(20/21), L taken from head to head, topsail yard
0.81 of it. Schooners' and galeasses' main mast to the hounds three times the breadth. By the
frigate rule No. 5's fore yard would be about 0.47 of the length, 34 to 36 Swedish ft, against
41.9 measured; she is sparred more heavily than the rule, as her bowsprit is (judgement; the
length the rule means is uncertain by a few feet).

### 2.5 Her proportions compared

| | Gwyn | Chapman No. 5 | Falconer 1780 | Röding col. 304 | Lescallier fig. 7 |
|---|---|---|---|---|---|
| Yard to the horizontal | 44° | 35° to 36° | about 45° | about 45° to the mast | 32° |
| Yard's fore end | about midships (0.60 from the taffrail) | about 3 ft forward of midships | "as far forward as the middle of the ship" | "ungefähr in der Mitte des Schiffs" | — |
| Peak | high, about 0.09 of the length inside the taffrail | about 10 ft (0.13) inside the taffrail | "immediately over the stern" | over the stern or after-body | — |
| Yard ÷ length at the rail | 0.72 | 0.54 | about 0.7 (judgement: a 45° yard spanning half the length) | — | — |
| Yard before the mast | 0.395 | 0.32 to 0.33 | — | — | 0.41 |
| Luff / leech | 0.16 | 0.46 | — | — | 0.39 |
| Main mast from the stern | 0.41 of the rail length | 0.41 of the waterline (at the rail) | — | — | — |
| Main truck above the deck ÷ the rail length | 0.95 | about 1.14 (judgement: 88 ft over 77.6) | — | — | — |
| Access | measured | measured | read | read | measured |

Gwyn's yard, about 44° and about 0.7 of the length, from midships to over the stern, is what
Falconer and Röding describe; **Chapman's flatter, shorter yard is the outlier**, and the
round-1 remark that Gwyn exaggerates the yard is withdrawn (judgement). Gwyn's lower masts
are short beside Chapman's (the main top 0.35 of the rail length above the deck against
Chapman's 0.53, judgement) and his whole rig lower; Chapman's figure is a generic
Swedish-drawn type of 1768, not Gwyn's British coaster, so the two need not agree.

### 2.6 The square fore, the main topsail, and the headsails

| | Gwyn PAG3828 | Chapman No. 5 | Lescallier Pl. XXII fig. 8 | Steel 1794 Plate 1 | Falconer 1769 Pl. XII fig. 7 |
|---|---|---|---|---|---|
| Fore | course, topsail, topgallant set | fore yard, topsail and topgallant yards | course and topsail set; topgallant yard crossed bare | course, topsail, topgallant | three square sails |
| Main above the settee | topsail and topgallant set | topsail and topgallant yards | topsail set; topgallant yard bare | topsail and topgallant | topsail and topgallant |
| Main dry yard (crossjack) under the top | **yes** | **none drawn** | **yes** (fig. 7 too, with lifts u from the cap) | too dark to tell | not resolvable |
| Spritsail yard | not seen | not reported | yes | yes | — |
| Headsails | jib on a jib-boom, fore topmast staysail | jib and staysails | headsails | headsails | headsails |
| Access | read | measured | read (zoomed, the largest IA size) | read (a dark microfilm print; topgallant yards bare, the checker) | read (a small engraving) |

- **Lescallier Pl. XXII fig. 8** "Bélandre, Page 404" (read): a three-quarter view of a
  bluff, round-sterned Dutch-looking hull with no gun ports; the settee with one reef band,
  its lower end reaching forward to about the fore shrouds (uncertain in perspective). The
  plate heading reads "Pour le 3e Livre Chap. 3: Art. 3,7,8 et 10"; the notice of plates
  (tome II OCR l. 20937 to 20958) "Bélandre, sorte de bâtiment de Flandres & de Hollande".
- **Steel 1794 Plate 1** (read; facing pp. 220 to 221, engraved by V. Woodthorpe, No. 27
  Fetter Lane): snow, brig, bilander and ketch. The bilander: a square fore course, topsail
  and topgallant; main topsail and topgallant over the settee; a spritsail yard. The settee
  yard peaks aft high over the quarter, its heel forward of the main mast, the sail
  extending before the mast; two vangs from the peak down to the quarter, each with a
  tackle about halfway; one reef band parallel to the foot; the sail on the far side of the
  mast from the viewer; the heel ropes and tack lost in the dark print. The 1806 *Art of
  Rigging*'s Pl. 11 is the 1794 Plate 2 reused (read), so its missing Pl. 10 is very
  probably this Plate 1 (judgement).
- **Röding Tab. LXXXIX** (read): fig. 521 copies Lescallier's bilander sail, fig. 522 his
  lug.
- The game's brig (Harpy) has royals (`data/ships/brig.yaml`, read); no bilander drawing
  shows a royal.

### 2.7 Deck, boat and ground tackle

- **No deck plan, boat or ground tackle** for any bilander was found. Gwyn gives the deck's
  outline: a raised quarterdeck from abaft the main shrouds to the stern, an open waist with
  side steps forward of the main mast, a head with rails, perhaps a catted anchor (read; the
  anchor judgement). Lescallier's Dutch hull has no ports (read). Chapman's rail stands about
  5.5 ft above the waterline (measured).
- The generator already sizes a merchantman's ground tackle and boats by rule: the merchant
  brig's anchors by the ship's size with hemp cables (package 34; `data/ships/merchant-brig.yaml`
  l. 1779 to 1810) and her long-boat amidships and jolly boat at the stern by Luce's rule
  (package 35; l. 1980 to 1991) (read). Applying the same rules to the bilander's size is
  the fallback (judgement).

### 2.8 Crew

| Vessel | Tons | Men | Note | Access |
|---|---|---|---|---|
| Nancy, of Boston | 170 | 10 | Catalogued "brigantine or bilander": her Boston register of 29 Oct 1778 says bilander, the libel "the brigantine Nancy", another paper "the brig Nancy". Taken from the British by an American privateer in 1778; the 10 men were her American crew on a Charleston–Boston rice voyage in 1779 (TNA HCA 32/405/21, C13507024) | catalogue |
| De Jonge Nella (Dutch) | 32 | 3 | Ostend–Rouen, 1779 to 1780 (HCA 32/374/7) | catalogue |
| Vergine del Carmine (French) | 60 | 9, and 9 passengers | Toulon–Minorca, 1782 (HCA 32/471/2) | catalogue |
| The game's merchant brig | about 300 (Harpy 316) | 16 | "about five men to a hundred tons" (`tools/gen_ships.py` l. 6491 to 6520) | read |

For a British bilander of 120 to 140 tons, **about 7 to 9 men** (judgement on one doubtful
example and the merchant brig's rate; a settee changed by hand at every tack may want the
upper figure).

## 3. The armed merchant fit

**Lloyd's Register's guns for bilanders** (read, the gun line under each vessel's own owner
checked on the images):

| Vessel | Tons | Guns | Years (leaves) |
|---|---|---|---|
| Elizabeth | 130 | "4-3 P.": four 3-pounders of the common construction | 1779 (0079), 1782 |
| Kerrison | 140 | "6-4 P.": six 4-pounders | 1781 (n163), 1782, 1783 (0186; the line "4-6, 2-4P." above hers is the entry above) |
| Essex | 160 | "2-2 P.": two 2-pounders | 1781 (n84) |

The 1782 entries are on leaves 0087 and 0174 between them.

The register has no column for swivels, and **no British source found counts a bilander's
swivels**.

**Others, not merchant fits** (and probably not the English type; § 2.1):

- Spanish privateer bilanders taken in 1780 (catalogue): L'Activa, "a Spanish privateer or
  naval bilander", 100 tons, 12 carriage guns, 2 swivel guns, 85 men (HCA 32/260/12,
  C13504732; round 1's link C15126220 is a 1708 Dunkirk bilander of 18 tons, HCA 32/59/57);
  60 tons with 14 guns and 92 men (HCA 32/361/15); 60 tons with 8 guns and 59 men (361/16);
  60 tons with 19 men and 2 passengers (390/1).
- British "bilanders" supplying besieged Gibraltar, in Spanish reports (read, OCR, poor on
  the numbers): one of 16 guns (calibre garbled) and eighty men, attacked in a calm by the
  Fox lugger of Ceuta (10 two-pounders, 35 men) rowing up while the Algeciras xebecs were
  held off by the calm (*Pennsylvania Packet*, 1 July 1781); one with provisions, nails and
  coals under a lieutenant, taken by a xebec (*Caledonian Mercury*, 21 Jan 1782); a
  corvette and a bilander of 24 and 26 guns that got in (*Caledonian Mercury*, 11 Sept
  1782). Armed store ships, not coasters.

**The game's comparator** (read, `tools/gen_ships.py` l. 4174 to 4215): the merchant brig's
fit is four long 6-pounders, two a side, four men a gun, a trader's magazine
(`MERCHANT_ROUNDS`, 20 round and 4 grape a gun, l. 3466), no swivels. The owner's "a few
small guns and swivels, as the merchant brig's" means a few small long guns; for a bilander
of 120 to 160 tons the register's evidence is **2 to 6 guns of 2 to 4 pounds** (judgement).
The swivels' number is the owner's (question 6).

## 4. How bilanders sailed

**No dated account of a British bilander under way with a figure** (speed, angle, time in
stays) was found. What the period says (the access as marked; the carrying to the settee is
judgement):

- **Inconvenient**: Steel 1794 p. 220 and 1806 p. 110 ("has proved inconvenient"); Falconer
  1769 and 1780 ("probably been found more inconvenient than several others") (read).
- **Good by the wind, awkward in going about**: Röding II col. 581 says sails of this kind
  sail excellently by the wind but are inconvenient, since they must be lowered and shifted
  in going about (read). Changing a whole mizen by peaking was laborious (Röding I col. 494,
  read, OCR).
- **Lateen sails lie a point nearer the wind**: "Vessels with latteen-sails will lie one point
  nearer the wind than a square-rigged vessel" (Steel 1794 I p. 237, the xebec, read, page
  image); Lescallier p. 380: lateen craft lie at five points (56° 15'), square-riggers at six
  (67° 30'; the OCR's "50 minutes" is a slip) (read, OCR). The bilander keeps a square fore,
  so the vessel would not gain the whole point (judgement).
- **Each shift of the tack costs ground**, said of luggers: "When this is often repeated,
  they loose ground in stays" (Steel 1794 I p. 221, read; the 1806 *Art of Rigging* p. 111
  the same). It speaks of shifting the tack, not of dipping the yard.
- **Taken aback**: the lateen is "more liable to be taken aback than the common lug" when by
  the wind, and the most disadvantageous of sails before the wind in a rough sea (Fincham
  1843 p. 59, read; `VesselReferences-2026-10.md` § 3.1).
- **The after sail in stays**: the ourse braced quite to leeward as the helm goes down
  (Bourdé p. 87; Steel 1794 II p. 316, read, OCR); in veering, clewed up and set again as the
  stern passes the wind (Steel II pp. 321 to 322, read, OCR).
- **The other type**: *Encyclopaedia Britannica* 1771 says its small Low-Country bilanders
  "can lie nearer the wind than a vessel with cross-sails can do" (read, OCR). Not the English
  bilander; weak.
- **One account under way**: the Gibraltar bilander of 1781, becalmed, attacked by the rowing
  lugger, lay to to repair; the Fox sheered off with her mast sprung, and the bilander fled,
  was chased, and got in under the guns (read, OCR). The rig is uncertain and there is no
  figure.

**Truth candidates** (handling rules, not dated passages; each for the owner and Phase 5):

1. The settee close-hauled lies no worse than the square fore, and up to a point nearer
   alone (Steel I p. 237; Lescallier p. 380); the vessel as a whole lies as a brig of her
   size, or slightly better (judgement).
2. Going about costs the bilander more time and hands than a brig of her size (Steel p. 220,
   Falconer, Röding cols. 494 and 581); if the settee is dipped, each tack also costs ground
   as a lugger's does (Steel p. 221).
3. In stays the settee's ourse is braced quite to leeward as the helm goes down, so the
   after sail helps her round (Bourdé p. 87; Steel II p. 316); the yard is changed (way a
   or b) as the last act, after the head-yards are trimmed (Boteler p. 163).
4. In wearing the settee is clewed up and set again once the stern is past the wind (Steel
   II pp. 321 to 322).
5. Aback, the settee presses the mast harder than a square sail does (Fincham p. 59; the
   size of the effect judgement), as the lug's rule in `VesselReferences-2026-10.md` § 1.4
   item 2.

## 5. Conflicts

| Subject | The sources | Reading |
|---|---|---|
| Going about | Röding II col. 581: lowered and shifted. Röding's own plate, Lescallier fig. 7 and the English comparison with the ship's mizen yard: a yard changed by peaking, or left on one side. An earlier brief's rule that "the settee's tack is not shifted round the mast" was not found in any text (`VesselReferences-2026-10.md` § 3.1, memory) | The owner's question 1; § 1.5 |
| The sail's cut | Luff/leech 0.16 (Gwyn), 0.20 (Steel, Kipping), 0.39 (Lescallier), 0.46 (Chapman); leech/head 0.72 to 1.06 | English short, continental deep (judgement); the owner's question 2 |
| The yard's angle and length | 44° and 0.72 of the length (Gwyn), about 45° (Falconer, Röding), 35° to 36° and 0.54 (Chapman), 32° (Lescallier, schematic) | Gwyn agrees with the English and German texts (judgement) |
| The main dry yard | Gwyn and Lescallier have one; Chapman draws none | The owner's question 5 |
| The ourses' lead | Ship's mizen: the aftermost main shrouds (Lescallier p. 170) or eye-bolts abreast the heel (Steel p. 208); lateen: bow and stern on the weather side (Lescallier pp. 378 to 379) | For the bilander, to the side abreast the heel (judgement); not shown on any plate |
| The derrick's blocks | Steel I p. 207: double at the cap, single on the yard; Steel II's table: "Derrick … Double", "Span … Single" | Take the text (judgement) |
| "Ourse" in English | Steel and Mainwaring: bowline; Romme: "Vang, or mizen bowline"; the plan and `VesselReferences` §§ 3.1, 3.2: vangs | This note: ourses = bowlines, brace = vangs (§ 1.2) |
| The 1788 English Bourdé | "to windward" against the French "sous le vent"; Steel copies the English | The French is right; a reader corrected the Archive's copy by hand (read) |
| Chapman's scale and positions | Round 1: 9.92 px per English foot, masts at the caps; round 2: 9.79 px per Swedish foot, masts at the rail; the two scans 5.5% apart vertically | Round 2's figures (§ 2.4) |
| Chapman's spars against his rules | Fore yard 41.9 against about 34 to 36 by the frigate rule; bowsprit 28.5 against 22.9 | The plate is No. 5's; heavily sparred (judgement) |
| The register's code | Bg and Br both ways for one vessel; Br gone from the key in 1790 | A register's change, not a rig's end (judgement) |
| The name | English bilander; Dutch bélandre (flat, leeboards, 60 to 80 tons); Spanish *bélandre* a sloop; EB's 24-ton craft | Keep the English type; doubt the Spanish "bilandras" |
| Project files to correct (for the lead; this note writes nothing else) | `docs/references/README.md`, the Chapman row: p. 104, § 31 should be **p. 102, § 32**; `docs/references/images/README.md`: Gwyn's ensign is on a staff at the taffrail, not at the peak; `VesselReferences-2026-10.md` § 0: Steel's BILANDER page is now checked as p. 220; §§ 3.1 and 3.2 call the ourses vangs; the plan § 2 R3 row "two vangs" | — |

## 6. What is open

- **No lines, deck plan or draught** of any bilander. Chapman draws no underwater body;
  Lloyd's gives tons and the loaded draught only. The hull rests on Chapman's length,
  breadth and rail height and Gwyn's profile, or on the brig's hull scaled (the plan's
  fallback).
- **No English account of a British bilander going about**, of the period or any period.
  The method rests on Röding (German) and on the mizen yard's English practice of a century
  earlier.
- Whether the yard was **lowered at sea to reef or furl**; whether it was **one piece or
  several** (Falconer's lateen yards are several); how its **ourses led** on a bilander.
- **The heavier spars against the rules**: No. 4 (the brig) is only on the low-resolution
  Commons scan (2.75 px a foot, ±8%); a better scan of the plate's right half would test the
  ×2 convention on a brig and show whether No. 5's heavy sparring is real.
- **Steel's *Art of Rigging* Pl. 10** and a clearer Steel 1794 Plate 1 (HathiTrust or Google
  full view, not reached) would show the English bilander's heel ropes, tack and dry yard.
- **Inman 1820** (the English Tractat) in an original copy, to confirm the wording of the
  half-length rule.
- **Crew and guns together**: a letter-of-marque declaration (TNA HCA 26) for Kerrison,
  Essex or Elizabeth, not searched.
- **Bilanders after 1790**: whether any British vessel still so rigged sailed in 1790 to
  1820; the later registers' remarks and the newspapers not searched.
- **The Gibraltar bilander of 1781 to 1782**: her name and rig (Navy lists, Drinkwater's
  siege journal), not searched.
- **Not viewed**: RMG PAI2636 and PAI5045 (no image online), *Encyclopaedia Britannica* 1771
  Pl. CXLIX fig. 2, Chambers's *Cyclopaedia* 1786 vessels plate (fig. 12).
- **Lloyd's**: "(?) Return" and the 50-ton New England entry of 1776 (leaf 0176) are
  unresolved; "s" and "s&d" after the code are unexplained; the counts are lower bounds.
- **Röding vol. II's date**: no title leaf was found.
- **Not reopened by the checker**: Sturmy 1669 and 1679, Atkinson 1790, Mountaine 1744,
  Moore 1776 and the *British Encyclopedia* 1809 (snippets only), and Chapman's topmast
  heights (spot-checked, not all re-derived).
- **Not reached**: Bonnefoux and Pâris, *Dictionnaire de la marine à voile*, and Pâris's
  *Souvenirs de marine* (Gallica 403; copies found on the Défense ministry's digital
  library, not fetched).

## 7. The owner's questions

1. **Going about.** (a) Dipped as the lug is, the yard lowered and passed round (Röding II
   col. 581, said of the bilander herself; your confirmation of 2026-10-17); (b) changed
   without lowering, the yard peaked up and down the mast and its heel passed abaft it,
   the tack to the new weather side (the ship's whole mizen: Röding I col. 494, Steel 1794
   II, Mainwaring, Boteler, Willaumez); or (c) left on one side, only the tack shifted,
   the sail against the mast on one board (Lescallier's two tacks, Röding's plate). And in
   stays, in wearing, or both?
2. **The sail and its yard.** A short luff, about a fifth or a sixth of the leech (Gwyn,
   Steel, Kipping), or a deep one, two-fifths to a half (Lescallier, Chapman)? And the yard
   at about 45° and 0.7 of the length (Gwyn, Falconer, Röding), or Chapman's 36° and 0.54?
3. **Her size and spars.** Lloyd's bilanders were 80 to 160 tons, most 120 to 160, drawing
   10 to 13 ft; Chapman's is about 120 to 130 tons (judgement). Which tonnage (Elizabeth's
   130, Kerrison's 140)? And Chapman's spars scaled to her, or the brig's rules?
4. **Her hull.** Gwyn's English hull (raised quarterdeck, round stern with windows,
   figurehead) on Chapman's proportions (waterline 3.6 breadths, the rail 5.5 ft up), or the
   brig's hull scaled? No lines exist.
5. **The main dry yard and the topgallants.** A dry yard under the main top for the main
   topsail's sheets (Gwyn, Lescallier) or none (Chapman)? Topgallant sails on both masts, as
   Gwyn sets them?
6. **The armed fit.** Four 3-pounders (Elizabeth), six 4-pounders (Kerrison), two
   2-pounders (Essex), or the merchant brig's four 6-pounders? How many swivels (no British
   source counts them)?
7. **Reefing.** One reef band parallel to the foot (all three drawings), the mizen's balance
   (Falconer, Lever), or both, the reef for a fresh breeze and the balance for a gale?
8. **Her era and trade.** The rig was rare from 1769 (Falconer) and "seldom used but by the
   Dutch" in 1794 (Steel); the last register entry verified is 1789. Is she an old survivor
   (Thames-built in the 1760s, say) in a 1792 to 1820 scenario? And her trade and home port
   for the Falmouth to Plymouth passage: a London–Rotterdam constant trader, a Poole
   Newfoundlandman, or an Irish Sea coaster (Yarmouth–Cork, Bristol–Dublin)?
