# Research note: the *Prince de Neufchatel* (Phase 1, October 2026)

Phase 1's note on the privateer for the three ships (`Plan-ShipsWorkflow.md` §2): her rig,
hull, spars, guns and people as the sources give them, her history, the accounts of her
sailing for the truths, and what is still open. The design and build phases work from this
note alone for her. It comes from two rounds of research, each checked by an independent
agent who re-opened every source. Where the two differed, this note gives the checker's
reading. By the owner's ruling (plan §0) her file carries no nation; §5.3 sets out what the
sources say on that.

The marks:

- **read**: seen on the page, the page image, the sheet or the code, with the page, line or
  object number;
- **OCR**: taken from an OCR text and not checked against the page image;
- **catalogue**: from a catalogue entry only;
- **measured**: taken off a free 1280-px image, with the sheet, the scale and the
  uncertainty. The checkers re-measured the figures that carry weight; those known not to have
  been re-measured are marked so;
- **snippet**: seen only in a search engine's extract;
- **secondary**: a modern work or Wikipedia, as a pointer only;
- **memory**: general knowledge, not read here;
- **judgement**: the research's own reasoning, including its arithmetic on figures read or
  measured.

Citations: "l." is a line of the OCR file filed in `docs/references/` (§0.1), and "(x, y)" is
a pixel on the 1280-px image. Winfield is the owner's copy, cited by page; his wording is not
copied. Quotations come from public-domain pages only.

Units: English feet and inches; metres in brackets for the engine's fields. Tons are tons
burthen unless stated otherwise. Displacement is given in tonnes (1,000 kg) and long tons, at
1,025 kg/m³ for salt water.

## 0. The sources

### 0.1 Filed in the repository (`docs/references/`, rows in its README)

| Short | Work | File | What it gives here |
|---|---|---|---|
| Cobb | [Josiah Cobb], *A Green Hand's First Cruise*, 2 vols., Baltimore, 1841 | `cobb/cobb-1841-a-green-hands-first-cruise-ocr.txt` | The account of a boy in her last crew, December 1814: rig, guns and men (vol. I pp. 37 to 41); putting to sea (pp. 53 to 54); the gale (pp. 77 to 93); the chase and the capture (pp. 93 to 109); after the capture (p. 138). The book is anonymous and never names the vessel. The identification rests on the captors he names, the boat fight, her sailing from Boston on 21 December, and Maclay 1899 pp. 384 to 387, who quotes the same memoir under her name. It is secure, but it is inference. |
| Coggeshall | George Coggeshall, *History of the American Privateers*, New York, 1856, and the 3rd edition of 1861 | `coggeshall/coggeshall-1856-...`, `coggeshall-1861-...` | pp. 241 to 244 (paged the same in both): 310 tons, "hermaphrodite rigged", 17 guns, the boat action. The 1861 edition adds the note from Ordronaux's papers (pp. 466 to 472) and is the text cited for the type's sweeps. |
| Niles | *Niles' Weekly Register*, vols. VI to VIII, Baltimore, 1814 to 1815 | `niles/niles-1814-...vol6`, `vol7`, `niles-1815-...vol8` | The American press of the day: her prizes, rig and tonnage, Ordronaux's account of the boat action, her sailing from Boston, and her capture. The OCR is rough. |
| James | William James, *Naval History of Great Britain*, new ed. 1837, vol. 6 (1902 printing) | `james/james-1837-...vol6-1902-printing-ocr.txt` | p. 237: the boat action. pp. 252 to 253: Collier's squadron (she is not named there). |
| Chapelle | Howard I. Chapelle, *The Baltimore Clipper*, 1930 | `chapelle/chapelle-1930-the-baltimore-clipper-ocr.txt` | The type's sweeps (p. 13); Marestier's proportions (pp. 112 to 114, 127 to 130); Rankine's rules (pp. 159 to 164); Herald's spars (p. 165); the gaff topsails (pp. 174 to 175); Fincham's 1829 tables (Appendix pp. 179, 184). Nothing on her. |
| Fincham | John Fincham, *A Treatise on Masting Ships*, 2nd ed., 1843 | `fincham/fincham-1843-treatise-on-masting-ships-ocr.txt` | p. 72: the proportions for schooners, with the "brig forward" examples. p. 78: the spars "Rigged as Brig Forward and Schooner Aft". p. 19: the moment of sail against stability. General Observations, arts. 19, 39 and 91. The OCR garbles the tables, so pp. 19, 72 and 78 are read from the page images (§0.2). |

### 0.2 Read online, public domain, not filed

| Short | Work | Where |
|---|---|---|
| Maclay | E. S. Maclay, *A History of American Privateers*, 1899, pp. 377 to 388 | IA `cu31924028732604` |
| Stevens | W. O. Stevens, "The Action between the Prince of Neufchatel and the Endymion", *USNI Proceedings* 41:1 (1915), pp. 25 to 32. He works from her log as printed in the Boston Advertiser of 17 and 18 October 1814 and from Nantucket accounts. | IA `sim_united-states-naval-institute-proceedings_january-february-1915_41_1` |
| Emmons | G. F. Emmons, *The Navy of the United States 1775-1853*, pp. 190, 191, 200 | IA `cu31924028730962`; page images of pp. 190 and 200 in `D:/Projects/FreeSail/owner-notes/neufchatel/rmg/` |
| NC | *Naval Chronicle* vol. 33 (1815), p. 72 | IA `navalchroniclefounse_5` |
| Gazette | *London Gazette* 17129 p. 729 (20 April 1816) and 17136 p. 911 (14 May 1816) | thegazette.co.uk |
| Fincham's pages | 1843 edition, pp. 19, 72, 78 | IA `bub_gb_z4QhGFh-7ZwC`, leaves n36, 0089, 0095; saved in `owner-notes/neufchatel/rmg/` |

### 0.3 Greenwich's three sheets

| Sheet | Catalogue | What | Image held (`owner-notes/neufchatel/rmg/`) | Scale at 1280 px |
|---|---|---|---|---|
| ZAZ6177 | rmgc-object-85968; Lines, 460 × 1140 mm, 1815 | Her lines as taken off at Deptford (body plan, sheer, half-breadth). The only source for hull form, ports, mast stations, rake and waterlines. | `ZAZ6177-j1261.jpg`, 1280 × 517 | 7.05 to 7.06 px/ft |
| ZAZ6178 | rmgc-object-85969; Lines, 445 × 1130 mm, 1815 | The Navy Office's draught for building a copy at Woolwich: the same lines and ports, with frame lines added | `ZAZ6178-j1259.jpg`, 1280 × 506 | not used for figures |
| ZAZ6179 | rmgc-object-85970; sail, 535 × 740 mm, 1815 | Her sail plan: every mast, spar and sail, the waterline, the mast heels | `ZAZ6179-j1260.jpg`, 1280 × 923 | 6.52 px/ft |

All **catalogue** for the entries; the images **read**. The catalogue's vessel name is "Prince de
Neuchatel fl.1814 (American, captured)". The museum's search page did not return the sheets;
they were found by object number. No deck plan or other profile was found. The neighbouring
numbers are other ships: ZAZ6174 is a 75-ft schooner-rigged gun vessel of 1795, ZAZ6176
*Ornen* and ZAZ6180 *Fair Rosamond* (1831); ZAZ6175 and ZAZ6181 were not re-opened. The
drawings of 1815 are out of copyright, but the photographs are the museum's: each catalogue
page carries "© Crown copyright. National Maritime Museum". So the images stay in
`owner-notes`, and only figures read or measured from them go into the repository. Commons
holds no copy of any of the three. The traced waterlines, the scripts and the overlays for
the hydrostatics (§2.5) are in `owner-notes/neufchatel/rmg/ZAZ6177-hydrostatics/`. They
retrace and recompute everything from the image; run them from a worktree's root with `py`.

### 0.4 The owner's

Winfield, *British Warships in the Age of Sail 1793-1817*, pp. 335 to 336, compiled from
Admiralty records, with the photograph of Philip Reed's model on those pages. The files are
`owner-notes/winfield/1793-1817-pp335-336-prince-de-neufchatel.txt` and `-model.png`.

### 0.5 Pointers only

- Mystic Seaport's Gregory plans library (ArchivesSpace, series 14.6): seven sheets of modern
  blue-line prints, giving lines, a sail plan with the belaying pins, and a rigging plan. The
  record names Adam and Noah Brown, 1812 to 1813, and gives "100'8" x 25'8"" (sic)
  (**secondary**).
- Chapelle, "Prince de Neufchatel, American schooner and privateer", *USNI Proceedings*, July
  1963: his own reading of these draughts. It is in copyright and was not read (**secondary**).
- Wikimedia Commons, `File:Prince_de_Neufchatel_1812-P3240002-white.JPG`: a body plan "as
  recorded by her British captors", from Briot, *Clippers français* p. 75. It is a modern
  redrawing, though Commons marks it public domain (**secondary**).
- RMG TRO/103/1 (rmgc-object-487194): Sir Edward Thomas Troubridge's papers, 5 to 26 January
  1815, six items on loan from a private lender. Watercolour 2 shows *Endymion*'s boats
  attacking her at night, 10 October 1814. No image is online (**catalogue**).
- Wikipedia: three jibs; 129 men at capture; her captain at capture "Nicholas Millin"
  (**secondary**).

### 0.6 Not reached

- Welsh Newspapers Online: a reprint of Collier's report of 29 December 1814, behind a
  Cloudflare check (HTTP 403). It was seen only as a **snippet**: a crew of 130 under Nicholas
  Millin, sailed from Boston on the 21st; "hermaphrodite" appears in the page's URL.
- 1812privateers.org (*Leander*'s log, the prisoner and muster lists): HTTP 403.
- usni.org: HTTP 403. Stevens 1915 was read on the Internet Archive instead; Chapelle 1963 is
  in copyright.
- HathiTrust full-text search: HTTP 403. The Google Books API: daily quota exhausted (HTTP
  429). Chronicling America: not reachable in machine form.
- NHHC image USN 902978, the boat attack: connection refused.
- The National Archives: the Deptford survey, the order of 10 April 1815 and the Navy Board's
  letters are not online.
- The London Gazette for 1814 and 1815: no notice of the capture. A search for her name over
  1813 to 1820 found only the prize notices of 1816.
- Full-resolution RMG images: not sought, by the owner's ruling (plan §0).

## 1. Her rig

### 1.1 What the period called her

| Source | Her rig named | Mark |
|---|---|---|
| Niles vol. VII p. 120, 29 October 1814 (l. 24194) | "hermaphrodite rigged" | read (page image) |
| Cobb p. 38 (l. 1365) | "hermaphrodite rigged, that is, her foremast was rigged as a brig, while her mainmast was rigged as a schooner". Also "hermaphrodite brig" (p. 23), "brigantine" (pp. 40, 117), and "the brig" throughout | read |
| Coggeshall p. 241 (l. 13090) | "hermaphrodite rigged" | read |
| Her log, as Stevens p. 26 quotes it | "privateer brig" | read |
| James vol. 6 p. 237 (l. 12393) | "American privateer brig" | read |
| Cobbett's *Weekly Register*, reprinted in Niles vol. VII, Supplement p. 170 (l. 106695) | "an American armed brig" | OCR |
| Emmons pp. 190, 200 | "Brig." | read (page images) |
| The Admiralty's sheets, 1815 | ZAZ6177 and ZAZ6179: "American Schooner"; ZAZ6178: "a Schooner from the Drawing of the Prince de Neufchatel" | read |
| Fincham 1843 pp. 72, 78 | A schooner, "brig for[ward]"; "Rigged as Brig Forward and Schooner Aft" | read (page images) |
| Winfield pp. 335 to 336 | A schooner of 18 guns; the picture's caption gives a compound of schooner and brigantine | read (owner's copy) |

The words do not all mean the same rig:

- **Chapelle p. 164 (l. 10048),** giving Rankine's rules (1866): "A brigantine or hermaphrodite
  brig has the bowsprit and foremast of a brig and the mainmast of a schooner". He adds that
  some have square topsails on the main (read).
- **Steel 1794 vol. I p. 220** uses HERMAPHRODITE for something else: a vessel that can be a
  snow or a brig as occasion serves, with two mainsails, a boom mainsail as a brig and a
  square one as a snow (OCR; `VesselReferences-2026-10.md` §3.7).
- **Lescallier 1791 pp. 402 to 403** describes the brigantine: square sails on both masts, but
  only a dry yard at the foot of the main, with a great boom sail in place of a main course
  (VesselReferences §3.7).

The American usage of 1814 (Niles, Cobb, Coggeshall) fits her; Steel's British usage of 1794
does not.

**The rig is settled** (read, from Niles, Cobb and Coggeshall and from the Admiralty's sail
plan): a brig's foremast and a schooner's mainmast. Cobb gives the reason for the rig: it is
"an advantage when on a wind, by bringing in use the enormous main-sail of the latter, and
when before the wind, by squaring the yards of the former" (p. 38).

### 1.2 What the sail plan shows

The sail plan is ZAZ6179 (j1260, 6.52 px/ft). The waterline is the horizontal line at y = 788,
level within 2 px across the sheet. The sheet was read at 2× to 8× and contrast-enhanced.

**The fore (a brig's mast).**

- **The mast.** A lower mast with a top, a fore topmast, and a topgallant mast with a royal
  pole in one piece. The fore channel on ZAZ6177 has about 7 chain plates a side (x 817 to
  927, measured), probably 4 shrouds and 3 backstays (judgement).
- **The square sails.** Course, topsail, topgallant and royal. The course was a working square
  sail (read):
  - after the surrender, while the sails were being furled, a seaman passed a lashing round
    "the foresail, on the windward yard-arm" (Cobb pp. 106 to 107);
  - as the wind eased after the surrender, Cobb reckons the frigates' guns would have reached
    them "before we could have sheeted down the foresail and filled away" (p. 105).
- **A boomless gaff sail,** Cobb's "fore-and-aft foresail" (pp. 33 to 34, 79), with its gaff
  jaws just below the fore yard. It is large (measured, ±0.6 ft):
  - gaff 32.9 ft, luff about 37.9 ft, leech about 50.2 ft;
  - foot about 46.6 ft, loose and drawn curved;
  - about 1,660 sq ft (±10%), as large as the fore topsail.

  Its leech crosses the mainmast at about y 660 and ends near (412, 705), 2.7 to 2.9 ft abaft
  the mast's line and 12.6 ft above the water. The stretch of leech behind the mast is drawn
  dashed, which may mean it laps the mast only in profile.
- **Studding sails** (measured):
  - booms run out 16.1 ft beyond the fore yardarm and 6.9 ft beyond the fore topsail
    yardarm;
  - a lower studding sail is drawn solid. Its outer leech runs from the fore-yard boom end
    (997, 483) down to "the Jack" at about (1059, 712), two-thirds of the way out along that
    spar. It is about 19 ft wide and 35 ft deep;
  - dashed outlines show a topmast studding sail and further light sails, only partly
    resolved.
- **"The Jack".** The label is read at 8×. It names a horizontal spar under the bowsprit near
  its cap, drawn double-line from x ≈ 997 to 1092 at y ≈ 711: 14.6 to 15.0 ft, or 30 ft if it
  is drawn halved like the yards (measured). Herald's spar list has a "jack yard for square
  sail" of 25 ft (Chapelle p. 165, read). That it spreads the foot of the lower studding sail
  or of a square sail is judgement.

**The main (a schooner's mast).**

- **The lower mast.** A long pole lower mast with crosstrees and no top: "her mainmast towering
  high in one piece, with no top as when square rigged, the cross-trees being the first
  landing place" (Cobb p. 91, read). About 3 chain plates a side on ZAZ6177 (x 537 to 620,
  measured).
- **The upper mast.** One upper mast with a long pole (§3.2). Cobb calls it the main
  "top-gallantmast" and says that in the gale it was housed to a little above the lower
  masthead (p. 91, read). That this is the same spar is judgement.
- **The mainsail.** A gaff mainsail on a very long boom, which overhangs the taffrail by about
  19.6 ft (boom end x ≈ 15, taffrail x ≈ 143; measured).
- **The gaff topsail** (measured). A triangle from the gaff peak to a short head spar, about
  4.3 to 4.6 ft as drawn, angled aft from near the topmast hounds. Chapelle pp. 174 to 175
  supports two readings (read): the "sliding gunter or jack yard topsail" of the American
  clippers, or the lug topsail that he says the Royal Navy usually used, which a Navy sketch
  could show. The head spar's form cannot be resolved at 1280 px.
- **Two light square yards on the topmast pole** (measured, ±1.2 ft doubled):
  - the lower one at the topmast hounds, 95.7 ft above the water, drawn 17.2 ft (34.4 ft
    doubled);
  - the upper one near the truck, 107.5 ft above the water, drawn 11.8 ft (23.6 ft doubled);
  - a square sail about 11.8 ft deep set between them.

  Reed's model shows a small square sail at the main masthead (read, owner's copy; a modern
  model). Against Fincham p. 78 (§3.2), the two yards are his main topsail yard (36.3 ft) and
  main topgallant yard (23.22 ft). So the sail drawn is a main topgallant, and Fincham's main
  square-sail yard of 48.4 ft, with a main topsail beneath the topsail yard, is not drawn. A
  square main topsail there would take the gaff topsail's place. All of this reading is
  judgement.
- **No studding sails** are drawn on the main.

**Between the masts** (measured; partly dashed and overlapping, so the reading is tentative):

- **A main staysail,** on a stay from the main masthead to the foremast near the deck. Its head
  is at about (503, 480), 60 ft above the water. About 530 to 540 sq ft.
- **A large main topmast staysail.** Its luff runs on the main topmast stay to the fore topmast
  crosstrees, and its leech is vertical at x ≈ 455. Its foot is drawn dashed at two depths,
  about 45 ft and 73 ft above the water.

**The head** (measured):

- **Bowsprit:** about 22.4 ft outboard, from the stem to the cap. Steeved about 15°: the lower
  edge at 15.8° and the jibboom at 15.1°; about 14.9° on ZAZ6177 corrected for drag.
- **Jibboom:** 38.7 ft from heel to end.
- **Flying jibboom:** reaches about 11 ft beyond the jibboom (±3 ft). Its end is 57.2 ft ahead
  of the stem head.
- **Headsails:** at least three are drawn, a fore staysail, a jib and a flying jib, with one or
  two more dashed. The count is tentative.

**The yards are drawn as half-lengths.** Every square yard and square sail on ZAZ6179 is drawn
from the mast forward only, while the booms and gaffs are drawn whole. So the drawn yard is
half the yard (judgement, high confidence). There are two grounds for this:

- doubled, the yards match Fincham's 110-ft row within 0 to 2 ft (p. 78);
- undoubled, the fore yard would be about 32 ft, 1.25 times her beam, far below Rankine's 0.48
  to 0.57 of the waterline length, which is 52 to 62 ft (Chapelle p. 161).

Because the halving was argued partly from Fincham, the yards' agreement with him cannot be
counted again as evidence that his example is her (§3.4).

**Storm canvas and reefs, as used** (Cobb, read):

- **In the gale:**
  - the topgallant masts were housed and the lighter yards sent down on deck (p. 78);
  - she lay-to under the fore-and-aft foresail (p. 79);
  - later she lay-to under a close-reefed storm staysail (p. 91).
- **On the morning of 28 December:**
  - every yard was on deck except the fore yard and the fore topsail yard (p. 93);
  - she had set a double-reefed foresail, and a fore-and-aft mainsail and a jib, "both
    likewise closely reefed" (p. 95). So the jib takes reefs. Which foresail was
    double-reefed, the course or the gaff sail, is not said.

### 1.3 How it squares with the owner's understanding

The owner chose her as a hermaphrodite brig: mostly square-rigged on the fore, with a small
loose-footed gaff sail (plan §0). The sources confirm the hermaphrodite brig (§1.1) and the
square fore with its topsail, topgallant and royal. They differ from the owner's picture in
two places:

1. **The loose-footed gaff sail is on the fore, and it is large:** a gaff of about 33 ft and
   about 1,660 sq ft, as large as the fore topsail, with its clew just abaft the mainmast
   (measured). The main's gaff sail is not loose-footed: it is the great boom mainsail, about
   2,770 sq ft. The game's topsail schooner already builds a loose-footed fore gaff sail that
   sheets abaft the mainmast and overlaps the main (`tools/gen_ships.py:2633` and `:2821`,
   read), so the generator has a precedent.
2. **The main is not wholly fore-and-aft.** ZAZ6179 and Reed's model show a square main
   topgallant on two light yards above the gaff topsail, and Fincham's table for the type
   also crosses a main square-sail yard (§3.2).

## 2. The hull and the draught

### 2.1 Principal dimensions and tonnage

| Figure | Value | Source | Mark |
|---|---|---|---|
| Length on deck | 110 ft 8 in | Winfield pp. 335 to 336; ZAZ6177's table, legible at 5× | read |
| Keel for tonnage | 93 ft 8¼ in | Winfield; ZAZ6177 reads 93 ft 8 in | read |
| Breadth extreme | 25 ft 8 in | Winfield; ZAZ6177's table "25-8?" | read; the table's breadth lines tentative |
| Breadth moulded | 25 ft 4 in | ZAZ6177's table; consistent with the transverse scale check (§2.2) | read, tentative |
| Depth in hold | 11 ft 6 in | Winfield | read |
| Burthen | 328 22/94 tons | Winfield; ZAZ6177 "No 328" | read |

**Check:** the Navy's rule on Winfield's keel and extreme breadth (93.69 × 25.67 × 12.83 / 94)
gives 328.3 tons (judgement, arithmetic).

**Other tonnages** (all read): 310 tons (Niles vol. VII p. 120, whose last digit is broken on
the page image; Coggeshall p. 241; Maclay p. 378); 311 tons (her log, Stevens p. 26); "about
three hundred and thirty tons" (Cobb p. 38). The American and British rules of measurement
differ (judgement), so these figures do not conflict with 328.

**The rest of Winfield's entry** (read):

- built 1812 to 1813 by Christian Bergh of New York (but see the builder in §7);
- 16 × 12-pdr carronades and 2 × 6-pdrs;
- taken on 28 December 1814 by *Leander*, *Newcastle* and *Acasta*;
- never commissioned;
- after her survey at Deptford, damaged in coming out of dock, and broken up in 1815;
- a copy ordered at Woolwich on 10 April 1815, never built.

### 2.2 The sheets and their scales

**ZAZ6177** (read):

- **Title:** "A Drawing of the Prince de Neufchatel, American Schooner. Taken off in H.M. D[ock]
  Y[ar]d Deptford, March". The year after "March" is hidden behind the drawn mast stump.
- **Inscription,** top left, read at 4×: "Deptford Yard 6th April 1815 W Jones". The 6th is
  favoured over the 4th.
- **Dimension table:** partly legible at 1280 px (§2.1).
- **Note at the stem,** read at 8×: "Draught of Water when in sailing Trim". A second line of
  figures under it cannot be read at 1280 px and lies partly under a tape stain. The note
  stands at the stem, so it may give only the forward draught.

**ZAZ6178** (read):

- **Heading:** "Navy Office 5 (or 3) May 1815". The 5 is favoured.
- **Title:** "A Draught for building in His Majesty's Yard at Woolwich a Schooner from the
  Drawing of the Prince de Neufchatel", in pursuance of an order of the Lords Commissioners
  of the Admiralty "of the 10 last month". This matches Winfield's 10 April 1815.
- **Signatures:** apparently J. Tucker and R. Seppings, which fits Joseph Tucker and Robert
  Seppings, the joint Surveyors of the Navy in 1815 (memory).
- **Its dimension table:** the row labels are legible; the figures are not.

**ZAZ6179** (read): "Sketch of the Masts, Yards and Sails of the Prince Neufchatel, American
Schooner", dated "Ap. 1815". It is signed by two people, read as "?. Robb[s]" and "W Jones".

**Scales** (measured):

- **ZAZ6177:**
  - the scale bar's 5-ft divisions are 35.30 px apart over 20 intervals (x 314 to 1020), with
    1-ft subdivisions at both ends, giving 7.06 px/ft;
  - transversely, the top-breadth half-breadth (88.7 to 88.8 px) and the body plan's dead flat
    (2 × 88.6 px), against a moulded breadth of 25 ft 4 in, give 7.00 px/ft. So the lines are
    drawn moulded, inside the plank;
  - 7.05 px/ft is used throughout (±0.7%). On the 1140-mm sheet that is about 6.29 mm to the
    foot, within about 1% of the usual ¼ in to the foot, 6.35 mm (judgement).
- **ZAZ6179:** the scale bar gives 65.15 px per 10 ft, with 1-ft subdivisions of about 6.5 px,
  so 6.52 px/ft. The second round read the hull outline at 6.48 px/ft, 0.6% different and
  inside the reading error.
- **Cross-checks:**
  - the hull's overall length agrees between ZAZ6177 and ZAZ6179 within 0.6 ft, at about 114
    to 115 ft;
  - the length on deck, rabbet to rabbet on ZAZ6177, is 110.8 ft against the table's 110 ft
    8 in.

Points are read to ±2 to 3 px, about ±0.4 ft on ZAZ6177 and ±0.5 ft on ZAZ6179.

### 2.3 Waterlines, draughts and keel (ZAZ6177)

All measured on ZAZ6177 at 7.05 px/ft unless stated otherwise.

- **The keel line.** The keel rabbet is drawn level (it slopes −0.03°). The heavy line at
  y ≈ 319 is the rabbet. The heavier line at y ≈ 330 to 332 is the scale-bar box, not the
  keel.
- **The waterlines.** Three green waterlines are drawn, parallel and equally spaced 18.57 px
  (2.63 ft) apart vertically. They slope down toward the bow at 1.645°, 1.629° and 1.609° to
  the rabbet, a mean of 1.63° (rms 0.4 to 0.5 px; the first round's 1.56° was slightly low).
  The top one is the sailing-trim waterline (§2.2).
- **The keel bottom.** The bottom of the false keel is taken as the scale bar's top border. The
  gripe curve and the rudder heel both run into that border, which supports the choice. The
  border slopes 0.19° to 0.22° to the rabbet and lies 1.53 ft below it aft, 1.70 ft amidships
  and 1.83 ft forward: the keel is deeper forward, as Marestier says of the type (Chapelle
  p. 127, read). A faint line 0.9 to 1.05 ft below the rabbet is probably the main keel's
  lower edge.
- **The keel's section.** In the body plan the keel is sided about 0.7 to 0.8 ft and stands
  1.7 to 1.9 ft below the base.
- **Sailing-trim draughts, to the bottom of the false keel** (±0.25 ft each):

  | Where | Draught |
  |---|---|
  | Aft, at the after side of the sternpost | 11.73 ft (3.58 m), about 11 ft 8¾ in |
  | Forward, at the fore side of the stem, with the keel line produced | 8.98 ft (2.74 m), about 9 ft 0 in |
  | Mean | 10.36 ft (3.16 m) |
  | Drag | 2.75 ft (33 in) |

  To the rabbet the draughts are 10.1 ft at the post, 7.5 ft at the forefoot and 8.3 to 8.6
  ft amidships. ZAZ6179, with its level waterline and dashed keel, gives about 11.8 ft aft and
  9.25 ft forward independently.
- **The other keel line.** If the faint line is the true keel bottom, every draught drops by
  about 0.5 ft and the lateral plane by about 5% (§2.6).

### 2.4 Form (ZAZ6177)

**Length and beam at the waterline** (measured, ±0.5 ft): 107.3 ft (32.7 m) between the post and
stem rabbets (x 321.6 to 1078.3); 110.1 ft (33.6 m) over the after side of the post and the
fore side of the gripe. The waterline beam is 24.47 ft moulded (7.46 m), or about 24.8 ft
outside the plank (7.56 m). The waterlines' ends in the half-breadth plan agree with the
profile's rabbets forward within 1 to 2 px.

**Half-breadths, in feet,** at 10-ft stations from the after rabbet along the waterline
(measured, ±0.1 ft):

| Waterline | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| LWL (sailing trim) | 6.29 | 9.45 | 10.80 | 11.52 | 11.90 | 12.23 | 11.97 | 11.37 | 9.50 | 5.26 |
| WL2 (2.63 ft below) | 2.72 | 6.11 | 8.57 | 9.71 | 10.34 | 10.37 | 10.01 | 9.02 | 6.82 | 3.12 |
| WL3 (5.27 ft below) | 1.25 | 2.78 | 4.61 | 5.86 | 6.40 | 6.26 | 5.64 | 4.57 | 3.17 | 1.03 |

All the lines run into the rabbets at about 0.3 ft.

**The dead-flat section,** as height above the rabbet against half-breadth, in feet: 0/0.37,
0.92/1.79, 2.06/3.91, 3.19/6.33, 4.33/8.45, 5.46/10.07, 6.60/11.15, 7.73/11.86, 8.21/12.17 (at
the LWL), 10.0/12.48. The floor is straight at 27° (±2°) from the keel out to about 6 ft, and
then turns at a firm bilge (measured; 26.9° on re-measurement).

**The top-breadth half-breadths,** in feet, by distance from the post (measured, not
re-measured): 8.3 at 2 ft, 9.1 at 12, 10.8 at 26, 11.7 at 41, 12.4 at 55, 12.55 at 65, 12.3 at
76, 11.8 at 83, 9.2 at 96, 6.9 at 101, 5.1 at 104.

**Other measurements:**

- **Maximum breadth:** 88.5 to 88.8 px, so about 25.1 ft moulded at 7.05 px/ft. It lies about 63
  to 69 ft forward of the post, about 10 ft (0.09 of the length) forward of the middle, within
  Marestier's range of 0.058 to 0.188 forward (Chapelle pp. 128 to 129, read).
- **Transom:** about 17 ft wide at the rail (not re-measured).

**Coefficients** (measured, ±0.02):

- the largest section is 127.2 ft² (11.8 m²) moulded to the rabbet, near mid-length (x 705);
- Cb is 0.41: the moulded volume over LWL × BWL × 8.63 ft, the depth to the rabbet at that
  station. On LWL × BWL × the mean draught to the false keel (10.37 ft) it is 0.34;
- Cp 0.68, Cm 0.60, Cwp 0.77.

### 2.5 Hydrostatics (ZAZ6177)

**Method.** The hydrostatics were integrated off the three traced waterlines, fitted in the
profile, and the rabbets of the keel, stem and post. Below the lowest waterline the shape was
calibrated on the body plan's dead-flat section, using a power law b = bk + (b3 − bk)·t^p with
p = 1.18 amidships, rising to 1.6 at the ends. That law matches the traced midship section
within 1 px at every height, though only with a +0.9 px shift of the body plan's base (areas
122.0 against 119.6 ft²).

**Checks:**

- Simpson's rule on the waterplanes between WL3 and the LWL gives 7,907 ft³; the sections give
  7,888 ft³;
- the checker re-ran the scripts on a copy and reproduced every figure below;
- the centreline was found independently at y 457.5 to 458.0, which supports the 457.7 used.

| Figure | Value | Mark |
|---|---|---|
| Moulded volume to the sailing-trim LWL | 9,297 ft³ (263.3 m³) | measured |
| Sensitivity of the moulded volume | scale 7.00 to 7.10 px/ft gives 9,100 to 9,500 ft³; the garboard exponent 1.0 to 2.2 gives 9,250 to 9,440 ft³; the centreline ±0.3 px gives ±60 ft³ | measured |
| Plank, 2 in over the wetted girth | 453 ft³ | measured. The 2 in is from 25-8 extreme less 25-4 moulded on the table, judgement |
| Keel, false keel, stem, gripe and post below the rabbet | about 167 ft³ (208 ft² sided 0.8 ft) | measured |
| Rudder | about 13 ft³ | measured |
| **Displacement at sailing trim** | **about 9,930 ft³ (281 m³): 288 t, 284 long tons, ±10 t** | measured |
| Displacement against burthen | 284 long tons / 328 tons = 0.87. HM schooner Spider of 1835 weighed 1.12 times her burthen fully equipped (Chapelle pp. 165 to 166, l. 10302 to 10377), but the Neufchatel was far sharper | measured; judgement |
| Weight budget for 130 men, 18 guns and stores | about 315 t: the drawn trim is plausible, perhaps a little light | judgement |
| Waterplane | 2,014 ft² (187 m²) moulded, about 2,050 ft² (190 m²) outside the plank. WL2 is 1,539 ft² and WL3 836 ft², so the waterplane shrinks fast with draught | measured, ±2% |
| Tons per inch immersion | 4.8 moulded, 4.9 outside the plank (long tons) | measured |
| LCF | 1.0 ft forward of the middle of the LWL between rabbets | measured |
| LCB | 0.7 ft (0.21 m) forward of that middle | measured, ±1.5 ft |
| Centre of buoyancy | 2.9 to 2.95 ft (0.90 m) below the LWL; KB 5.7 ft above the rabbet, about 7.4 ft above the bottom of the false keel. Morrish's approximation gives 2.98 ft | measured, ±0.2 ft |
| BM, transverse | 8.35 ft moulded; 8.2 ft (2.50 m) with the plank and appendages | measured (the 8.2 not recomputed) |
| **Transverse metacentre** | **5.2 ft (1.59 m) above the sailing-trim LWL** | measured, ±0.5 ft |
| BM, longitudinal | about 145 ft (44 m) | measured |

The game's rules for other hulls would be badly wrong for her (measured against
`tools/gen_ships.py`, read):

- the frigate's Cb of 0.55 (line 1513) would give about 434 t, 51% high;
- Speedwell's Cb of 0.33 (line 2538) would give about 260 t, 10% low.

**GM is in no source** (judgement throughout). GM is 1.59 m minus the height of G above the
LWL. Two estimates were made.

The first estimate uses Fincham's class ratios (read). Fincham p. 19 (the page image) gives
the moment of sail per foot-ton of righting moment at 10° of heel for each class of vessel.
Fincham p. 72 gives the "brig forward" Ex. 1 a moment of sail of 204 times the load-water
section, about 411,000 ft³ on her waterplane. With GM = moment of sail / (ratio ×
displacement × sin 10°), at 284 long tons each class's ratio gives:

| Fincham p. 19 class | Ratio | GM |
|---|---|---|
| Brigs of 18 guns | 1,058 as printed (1,082 from its own columns) | 7.9 ft (2.40 m); 7.7 ft on 1,082 |
| Brigs of 10 guns | 1,196 | 7.0 ft (2.12 m) |
| Corvettes | 1,013 | 8.2 ft (2.51 m) |
| Merchant brigs | 1,024 | 8.1 ft (2.48 m) |
| Yacht schooners | 913 | 9.1 ft (2.78 m) |
| Yacht brigs | 1,577 | 5.3 ft (1.61 m) |
| Yacht cutters | 1,728 | 4.8 ft (1.47 m) |

The second estimate is a rough weight budget, which puts G about 2 ft below the LWL, so GM
about 7.6 ft (2.3 m).

**What this rests on.** Both estimates rest on Ex. 1 being her (§3.4), and the first on which
class a privateer is like. Every figure is far stiffer than the 1.0 m in Speedwell's file
(`tools/gen_ships.py:2525`, there judged tender) and the frigate's 1.3 m (`:1500`). The
reasoning behind the first estimate (judgement):

- Fincham's moment divided by his area (204 / 4.59 = 44.4 ft = 1.73 × breadth) is his stated
  height of the centre of effort, so his moment is the sail area times its height above the
  LWL;
- that agrees in size with p. 19, which supports using the ratio.

### 2.6 Lateral plane, centre of lateral resistance and rudder (ZAZ6177)

**The lateral plane** (measured, ±5%):

- **to the bottom of the false keel, without the rudder: 1,100 ft² (102 m²).** Of this, 891 ft²
  lies inside the rabbets and 208 ft² is keel, false keel, stem, gripe and post;
- with the keel bottom at the faint line instead: 1,040 to 1,043 ft² (97 m²);
- with the rudder: 1,128 ft² (105 m²).

Its ratio to LWL × mean draught is 0.99: the stem is nearly upright at the waterline, and the
dragged keel runs deep aft. The frigate's 0.85 rule (`tools/gen_ships.py:1502`) would give
945 ft², 14% low; Speedwell's 0.78 rule (`:2527`) would give 867 ft², 21% low.

**The centre of lateral resistance** (geometric, measured, ±1 ft):

- **without the rudder:** 2.61 ft (0.80 m) abaft the middle of the LWL between rabbets, and
  5.14 ft (1.57 m) below the LWL;
- **with the rudder:** 3.9 ft (1.19 m) abaft that middle;
- **from Fincham's middle,** the middle of the waterline from the fore side of the stem to the
  after side of the post (x ≈ 703.5): about 3.1 ft abaft without the rudder, 4.4 ft with it.

Fincham's Ex. 1 puts the centre of effort 0.0163 of the length from the middle, which is 1.8
ft. It is abaft the middle if the heading of his mast rows applies to it. On that reading it
leads the geometric centre by about 1.3 ft (2.6 ft counting the rudder).

The engine's `clr_x_m` is positive forward (`freesail/physics/hull.py:327-329`, read). The
geometric value is −0.80 m on the rabbet middle. The engine's value is a tuned centre of
pressure, as the frigate's note explains (`tools/gen_ships.py:1516`), and is the designer's
to set.

**The rudder** (measured):

- **The stern's lines.** At 7× three lines are visible at the stern:
  - a thin, nearly plumb line (2.2°): the blade's after edge;
  - a raked line (12.1°), crossed by the pintle and gudgeon straps: the hinge, at the post's
    after edge;
  - a line raked more steeply (17.0°) that runs into the keel rabbet: the post's rabbet.
- **The blade** widens downward: 1.36 ft (0.41 m) wide at the LWL and 3.42 ft (1.04 m) at the
  heel.
- **Span and area.** The immersed span is 11.7 ft (3.58 m), from the LWL to the heel at the
  false keel (±0.3 ft). The area below the LWL is 28.1 ft² (2.61 m², ±3 ft²); up to the
  counter it is about 32 ft².
- **Proportions.** The area is 2.55% of the lateral plane, and the aspect ratio (span² / area)
  is 4.9.
- **The post** is 0.87 to 0.9 ft fore and aft at the LWL and about 1.8 to 1.9 ft at the heel.
- **ZAZ6179** shows the same wedge-shaped blade dashed: about 1.5 ft at the waterline, 3.2 ft
  at the heel, 11.9 ft of span.

The maximum helm angle and the rate of helm are in no source.

### 2.7 Ports, sweep ports, masts at the deck, deck and freeboard (ZAZ6177)

**Gun ports** (measured):

- **Count:** 11 a side, with lids drawn. ZAZ6178 has the same 11.
- **Positions:** centres 7.8, 17.2, 26.4, 36.0, 45.5, 54.9, 64.5, 74.2, 83.1, 92.5 and 101.7 ft
  forward of the post at deck height, about 9.4 ft (66.3 px) apart (±0.5 ft).
- **Size:** each about 2.7 ft wide by 2.4 ft high (±0.3 ft, not re-measured), opening just
  under the rail.
- **Sills:** about 1.3 ft above the deck at side. On the corrected freeboard below that puts
  them about 4.7 to 5.1 ft above the water amidships (judgement, arithmetic).
- **Stern ports:** two squares at the top of the transom on the body plans of both sheets.
  This is a tentative reading.

The Naval Chronicle has her "pierced for 22 guns, and mounting 18" (vol. 33 p. 72, read), which
agrees with 11 ports a side.

**Small ports** (measured): 11 a side, about 0.7 to 0.85 ft square (±0.2 ft), at x ≈ 338, 403,
468, 533, 602, 668, 735, 798, 870, 937 and 1002. There is one just abaft each gun port, about
4.6 ft from it, so the aftermost lies between the stern and the first gun port. They are
probably sweep ports (judgement), matching Chapelle's: "The use of sweeps in the Baltimore
Clippers was very common. The oar-ports were between the gun-ports, as a rule" (p. 13, read).
Pictou, a captured privateer of 299 tons, had 11 square oar-ports a side and 22 sweeps
(Chapelle pp. 95 to 96, read). So she was fitted for about 22 sweeps (judgement). No account
shows her using them (§6, T8).

**Masts at the deck** (measured, ±1 ft):

- **Positions:** the main centre is 42.3 to 42.6 ft and the fore 85.9 to 86.4 ft forward of the
  after side of the post at deck height, 43.6 to 43.9 ft apart; ZAZ6179 gives 43.9 ft. Red ink
  marks on the half-breadth plan's centreline at x 611 and 920 appear to mark them.
- **As fractions of the LWL at the waterline:** main 0.105 abaft the middle, fore 0.29 to 0.30
  before it. Fincham's Ex. 1 has 0.11 and 0.3.

**Rake** (measured, ±0.7°): main about 12.2° to 12.4° and fore about 10.3° to 10.6° from the
vertical, with the waterline level.

- On ZAZ6179, whose waterline is level, they are 12.4° and 10.3°, or about 31 and 26 in in 12 ft.
- On ZAZ6177 the stumps rake 10.6° and 9.0° from the keel's normal, and the drag angle adds to
  both.
- Fincham's Ex. 1 has 33 and 28 in in 12 ft (12.9° and 11.0°).

**Deck and freeboard** (measured, ±0.3 ft): the deck at side, the red line, stands above the
waterline:

| Where | Deck at side above the waterline |
|---|---|
| At the stern | 5.0 ft |
| Lowest, at and just forward of the mainmast | 3.4 to 3.5 ft |
| At mid-length | 3.8 ft |
| At the foremast | 4.4 ft |
| At the bow | 5.6 ft |

The rail is about 4 ft above the deck at side. On ZAZ6179 the rail is about 8.4 ft above the
water at the masts. A step of about 0.8 ft in the red line near the mainmast, higher aft, was
seen once and is not clear in the re-trace (unresolved).

Cobb gives "a flush deck fore and aft" (p. 38, l. 1373) and "the trunk of the quarter deck"
(p. 103) (read).

**Deck fittings.** Red rectangles lie along the centreline below the half-breadth plan; they
cannot be resolved at 1280 px. No pivot ring, slide or other pivot mounting shows on any of
the three sheets, but none of them is a deck plan, so the absence is very weak evidence
(judgement).

The depth in hold of 11 ft 6 in agrees with about 12 ft from the deck at side amidships to
the rabbet (judgement).

### 2.8 Checks against the period

- **Fincham's "load-water section" is the waterplane** (read; the reading is judgement). In art.
  39 he writes that "the area of the load-water section, and the depth of the centre of
  gravity of displacement, are the elements the most proper to be compared together" (l.
  2392). His rule that follows divides part of "the area of the load-water line"; the
  fraction is lost in the OCR.
  - Read on the midship section (about 130 ft²), Ex. 1's sail area would come out at about 600
    ft², which is impossible.
  - Read on the waterplane, Ex. 1's ratio (sail area 4.59 × load-water section, p. 72) gives
    9,240 to 9,410 ft² (858 to 874 m²) of sail.
- **Fincham's principal sails.** Fincham art. 19 (l. 1572, p. 7 by the page markers, not
  checked against the image) counts these sails in a sail plan:
  - for square rig, the courses, topsails, topgallants, driver and jib, and sometimes the
    fore topmast staysail;
  - for fore-and-aft rig, the mainsail, foresail and jib.

  For her, the fore course, topsail and topgallant and the mainsail come to about 7,050 sq ft
  (§3.3). That leaves about 2,200 to 2,400 sq ft for the jib and fore topmast staysail, which
  were not measured: plausible for headsails spread on a 57-ft reach of head spars
  (judgement). The test is unfinished (§8).
- **Marestier's Mammoth** (Chapelle pp. 112 to 113, read): 114 ft 11 in × 28 ft 8 in, drawing
  10 ft 0 in forward (0.348 of the beam) and 16 ft 0 in aft (0.557 of the beam). She was
  built as a schooner during the War of 1812. When Marestier wrote, about 1820, she was rigged
  as a brig and armed with 16 guns as the privateer *Independence of the South*. He notes
  that schooners larger than she were usually soon rigged as brigs.
- **Her draughts against Mammoth and Marestier** (measured against read; ratios judgement):
  - forward she draws 0.350 of the beam, an exact match with Mammoth; aft 0.457, so her drag
    is much less (2.75 ft against 6 ft);
  - against Marestier's general proportions (pp. 127 to 129), her midship draught is 0.091 of
    the length against "ordinarily 0.10 or 0.11", and her stern draught 0.106 against 0.14 to
    0.15. Chapelle's footnote (p. 127) says those depths are "apparently" from the deck to
    the rabbet, not draughts, so this comparison carries that doubt. Mammoth's own draught
    aft, 0.139 of the length, falls in Marestier's stern range, which favours reading them as
    draughts;
  - her stem rakes 0.63 of the beam (Marestier 0.4 to 0.8) and her post at the rabbet 0.19
    (0.2 to 0.4, the low end). The dead flat is forward of the middle, and the keel is deeper
    forward, as he says.

### 2.9 For the file: the engine's hull fields

`HullSpec` and `RudderSpec` are in `freesail/ship/schema.py:328-350` (read). The values below
are at her sailing trim. Which of them, and what tuning, is the designer's call.

| Field | From the sources | Mark |
|---|---|---|
| `length_waterline_m` | 32.7 (107.3 ft between the rabbets), or 33.6 (110.1 ft over the post and gripe faces) | measured |
| `beam_m` | 7.82 (25 ft 8 in extreme). BWL 7.46 moulded, 7.56 outside the plank | read; measured |
| `draught_m` | 3.16 mean to the false keel (3.58 aft, 2.74 forward) | measured |
| `displacement_kg` | 288,000 ±10,000 | measured |
| `gm_m` | No source. The metacentre is 1.59 m above the LWL (measured); GM 1.5 to 2.8 by Fincham's class ratios, 2.1 to 2.4 for his naval brigs, about 2.3 by the weight budget | judgement |
| `lateral_area_m2` | 102 without the rudder (97 if the keel bottom is the faint line); 105 with it | measured |
| `clr_x_m` | geometric −0.80 (−1.19 with the rudder) on the rabbet middle; the tuned value is the designer's | measured; judgement |
| `hull_speed_kn` | No figure in any source. The accounts: 12.5 kn once while running in the chase (T2), 12.5 "miles per hour" running out of Boston (T3), 10 kn scudding under bare poles (T4) | read |
| `deck_height_m` | deck at side 1.04 to 1.71 above the LWL (3.4 to 5.6 ft), 1.16 at mid-length; port sills about 0.4 above the deck | measured |
| `rudder.area_m2` | 2.6 | measured |
| `rudder.span_m` | 3.6 | measured |
| `rudder.max_angle_deg`, `rate_deg_s` | In no source. The generator uses 35° and 3 to 5°/s for the others (`tools/gen_ships.py:1505`, `:2530`, `:4737`, `:5626`) | read |

## 3. The spars

### 3.1 The sources

- **The sheet:** ZAZ6179, measured at 6.52 px/ft, with the yards doubled from their
  half-length drawing (§1.2).
- **Fincham p. 72:** a column headed "Ditto, brig for. Ex. 1. 110.6 ft. 25.6 ft." in his
  "Proportions for Masts, Yards, Booms, &c. of Schooners" (read on the page image; the same
  table, from the 1829 edition, is in Chapelle's Appendix p. 179).
- **Fincham p. 78:** "Rigged as Brig Forward and Schooner Aft, First Example", whose 110-ft
  row lists the yards, booms and gaffs (read on the page image; Chapelle Appendix p. 184).
  p. 78's yards are p. 72's proportions times the length (0.575 × 110 = 63.25), so they are
  not a second independent check.
- **Fincham's lengths below** are p. 72's proportions on 110.6 × 25.6 ft (judgement,
  arithmetic). p. 78's figure at 110 ft is given where it lists one.

### 3.2 The spars, measured and by Fincham

| Spar | Measured on ZAZ6179 | Fincham Ex. 1 |
|---|---|---|
| Main lower mast, heel to hounds | 80.5 ft | 79.6 (3.11 × breadth) |
| Main lower mast, head | 8.4; about 89 overall | 10.3 (0.13 of the hounded); 90.0 overall |
| Main heel below the waterline | 7.4 | 6.7 (0.26 × breadth) |
| Fore lower mast, heel to hounds | 58.4 | 58.4 (0.734 of the main) |
| Fore lower mast, head | 10.1; about 69 overall | 11.3 (0.193); 69.7 overall |
| Fore heel below the waterline | 6.1 | 5.6 (0.22 × breadth) |
| Main topmast | 39.6: 27.5 to the hounds and a 12.1-ft pole | 40.3: 28.2 hounded (1.1 × breadth) and a 12.1 pole (0.43) |
| Fore topmast | 34.8: 29.8 and a 5.1-ft head (not re-measured) | 35.2: 30.4 (1.08 of the main topmast) and a 4.7 head (0.156) |
| Fore topgallant mast with royal pole, in one | 29.6: 19.3 and a 10.4-ft pole (not re-measured) | 30.5: 19.7 (0.77 × breadth) and a 10.8 pole (0.55) |
| Lower mast diameters at the rail | about 20 to 21 in (±2 in, not re-measured) | — |
| Bowsprit | 22.4 outboard, stem to cap | 0.55 × the fore mast: 32.1 on the hounded mast, 38.3 on the whole; housed 0.35 × breadth (9.0) |
| Jibboom | 38.7, heel to end | 1.21 × the bowsprit: 38.9 on the hounded reading, 46.4 on the whole |
| Flying jibboom, beyond the jibboom | about 11 (±3) | 0.4 × the jibboom: 15.6 |
| Main boom | 64.2 (64 to 65) | 64.8 (0.586 × length); p. 78: 64.46 |
| Main gaff | 37.3, peaked at 24.0° | 38.0 (0.586 of the boom); p. 78: 37.1 |
| Fore gaff | 32.9 | equal to the main gaff; p. 78: 37.1 |
| Fore yard | about 65 (32.5 drawn) | 63.6 (0.575 × length); p. 78: 63.25 |
| Fore topsail yard | 46.8 | 46.8 (0.736); p. 78: 46.52 |
| Fore topgallant yard | about 26 (the second round, roughly 27.5) | 26.9 (0.574); p. 78: 26.67 |
| Fore royal yard | about 24.5 | 21.5 (0.8); p. 78: 21.3 |
| Main square-sail yard | not drawn | 48.7 (0.44 × length); p. 78: 48.4 |
| Main topsail yard (the lower main yard drawn) | 34.4 to 35 | 36.5 (0.75 of the square-sail yard); p. 78: 36.3 |
| Main topgallant yard (the upper) | 23.6 to 25 | 23.4 (0.48); p. 78: 23.22 |
| Swinging boom | not drawn | 43.2 (0.68 of the fore yard); p. 78: 43.01 |
| Studding-sail booms, beyond the yardarms | fore yard 16.1, topsail yard 6.9 | — |
| Bowsprit steeve | about 15° | 36 in in 12 ft (14.0°) |
| Rake, main and fore | 12.4° and 10.3° (31 and 26 in in 12 ft) | 33 and 28 in in 12 ft (12.9° and 11.0°) |
| Mast stations | main 0.105 to 0.117 of the LWL abaft the middle, fore 0.29 to 0.30 before | 0.11 abaft, 0.3 before |
| Drag | 33 in (ZAZ6177) | 24 in excess of draught aft |

Uncertainties of the measured column: masts ±1 ft; booms and gaffs ±0.7 ft; doubled yards
±1.5 ft; bowsprit and jibboom ±1 ft. The mast points used are the main heel (460, 836),
hounds y 323 and cap y 269, and the fore heel (744, 828), hounds y 452 and cap y 387.

### 3.3 Heights and sail areas (ZAZ6179)

**Heights above the waterline,** in feet (measured, ±0.5 ft):

| Spar | Height |
|---|---|
| Fore yard | 47.2 |
| Fore topsail yard | 78.5 |
| Fore topgallant yard | 97.7 |
| Fore royal yard | 108.1 |
| Fore truck | 110.4 |
| Fore gaff, jaws and peak | 46.9 and 61.7 |
| Main gaff, jaws and peak | 64.4 and about 79.5 |
| Main cap | 79.6 |
| Main square yards | 95.7 and 107.5 |
| Main truck | 110.1 |
| Main boom, at the mast and at its end | 10.4 and 16.4 |
| Rail at the masts | about 8.4 |
| Deck | about 4.0 |

**Square-sail depths:** fore course 33.3 ft (its foot 14 ft above the water); topsail 30.8;
topgallant 18.6; royal 10.4; main topgallant 11.7 to 11.8.

**Sail areas,** rough, from the measured corners (measured, ±10 to 15% each, the corners partly
judged; the mainsail, fore gaff sail and main staysail re-measured, the rest not), in square
feet:

| Sail | Area |
|---|---|
| Mainsail (luff 55, head 35, leech 65, foot 62 ft) | 2,770 to 2,790 |
| Fore course | 2,000 |
| Fore topsail | 1,700 |
| Fore gaff sail | 1,660 |
| Fore topgallant | 580 |
| Main staysail | 530 to 540 |
| Gaff topsail | 470 |
| Main topgallant (square) | 300 |
| Fore royal | 250 |

That is about 10,300 sq ft (957 m²) without the headsails, the topmast staysails and the
studding sails.

**Base of sail and Rankine** (Chapelle p. 160, read):

- **The base of sail,** from the flying-jib tack to the mainsail clew, is 186 to 189 ft
  (measured): about 1.75 times the LWL, above Rankine's 1.6 to 1.7 for schooners.
- **Against Rankine's other rules** (pp. 160 to 164, written in 1866; the comparison is
  judgement, and his rules are for two-masted schooners, not the hermaphrodite):
  - her mainmast to the hounds is 3.14 × breadth against his 2.6 to 2.8;
  - her fore yard is 0.61 of the LWL against 0.48 to 0.57;
  - her main gaff is 0.58 of the boom against 0.44 to 0.53;
  - her main boom is shorter, 0.60 of the LWL against 0.66 to 0.70;
  - her fore topsail yard (0.72 of the fore yard), mast stations and rakes fall within his
    ranges.

**Fincham art. 91,** for "a Brig forward, and Schooner aft" (l. 5204-5212; p. 37 or 38 by the
page markers; read):

- the nock of the mainsail is 2.3 to 2.5 × breadth above the water;
- the fore topgallant sails are 3.7 to 3.84 × breadth high;
- "The spread of the fore-course at the head, is from .4 to .48 the length of the
  water-line".

Hers, on a breadth of 25.67 ft (measured; that the second rule means the topgallant yard's
height is interpretation):

- nock 64.4 ft (2.51 × breadth);
- fore topgallant yard 97.7 ft (3.81 × breadth), so both at the top of his ranges;
- the head of the course about 59 ft, 0.55 of the LWL, above his range.

### 3.4 Is Fincham's Ex. 1 her? (judgement)

**Very probably,** or the 1815 Woolwich draught made from her (ZAZ6178). Fincham does not name
the vessel. The case:

- **Dimensions:** his 110.6 × 25.6 ft are her 110 ft 8 in × 25 ft 8 in.
- **Independent agreements within about 3%:**
  - main hounded 79.6 against 80.5;
  - fore hounded 58.4 against 58.4;
  - main topmast 40.3 against 39.6;
  - fore topmast 35.2 against 34.8;
  - topgallant and royal pole 30.5 against 29.6;
  - main boom 64.8 against 64.2;
  - main gaff 38.0 (37.1) against 37.3;
  - mast stations 0.11 and 0.3 against 0.105 to 0.117 and 0.29 to 0.30.
- **Chapelle's remark:** he says Fincham's rules "give a smaller rig than the American schooner
  usually carried" (p. 174, read), so a near-exact match to a captured American is telling.
- **A precedent:** Chapelle identifies Fincham's three-masted schooner example with the Royal
  Navy's "Bermudians" (p. 51, read).
- **Against:**
  - the yards' agreement is partly circular (§1.2);
  - the jibboom matches only if Fincham's "Fore-mast" is the hounded length;
  - the fore gaff (37.1 to 38.0 against 32.9) and the royal yard (21.3 to 21.5 against 24.5)
    differ;
  - the drag is 24 in against 33 in, and the rakes 33 and 28 in in 12 ft against 31 and 26.

If Ex. 1 is her, Fincham's pp. 72 and 78 serve as her own period proportions. They also give
spars the sketch does not draw: a main square-sail yard of 48.4 ft, a swinging boom of 43 ft,
and the centre of effort 1.72 × breadth (about 44 ft) above the LWL.

Fincham's **Ex. 2** in the same column (p. 72, read) is 102.5 × 25.8 ft, with more upright masts
(28 and 18 in in 12 ft) and 28 in of drag. It may be another captured American but is not
identified.

### 3.5 Other rules and a comparator

- **Marestier** (Chapelle pp. 112 to 114, 129 to 130, read), for American schooners of 1812 to
  1820. Applying his rules to her is judgement:
  - the mainmast is 3 × beam plus half the depth, or sometimes the whole depth. For her that
    gives 82.8 to 88.5 ft, against about 89 measured;
  - the diameter is about 1/50 of the length, about 21 in for her, against 20 to 21 in
    measured;
  - the fore is 0.6 to 0.9 m shorter and 2 to 4 cm thicker;
  - the rake is 15 to about 22 cm per metre (about 8.5° to 12.5°), the fore 1 to 2 cm per
    metre less.
- **Herald** (Chapelle p. 165, read): built in 1813 by Christian Bergh of New York, 230 tons
  American, 101 ft on deck, 24 ft 8 in beam, 10 ft 4 in hold, 18 guns. Her spars:
  - masts main 83 ft (head 9, 24 in diameter) and fore 80 ft (head 10, 24 in);
  - bowsprit 18 ft outboard, jibboom 32 ft, flying jibboom 26 ft;
  - square-sail yard 58 ft, square-sail booms 30 ft, a jack yard for the square sail 25 ft;
  - main boom 52 ft, gaffs 33 ft each;
  - topsail yard 36 ft, topgallant yard 25 ft;
  - fore topmast 28 ft (head 4), main topmast 38 ft 6 in (head 14);
  - a sliding-gunter fore topgallant mast of 34 ft (head 16); gaff topsail yard 31 ft;
  - studding-sail yards 14 ft 6 in and 9 ft 6 in, studding-sail booms 30 ft.

  C. H. S. Snyder found the figures in the Public Archives of Canada. Chapelle writes "it is
  highly probable that the Pictou is the Herald". She was a topsail schooner with masts of
  nearly equal height, not a hermaphrodite, so she is a comparator only, from the same
  builder (if Bergh built her, §7) and year.
- **Chapelle on the type** (pp. 100 to 102, read): large privateer topsail schooners of the War
  of 1812 often carried topgallants and royals above the fore topsail, and some a square main
  topsail. By the war's end many were built very nearly brigs, listed as "brig-schooners" in
  the Navy Lists.

## 4. Armament, complement and people by date

### 4.1 Guns

| When | Guns | Source | Mark |
|---|---|---|---|
| October 1814, at Boston after the cruise | "mounts 17 guns" | Niles vol. VII p. 120 (l. 24194); Coggeshall p. 241 | read |
| October 1814 | 14 guns, by her log | Stevens p. 26 | read |
| At the boat action (James's 9 October) | 18 guns | James vol. 6 p. 237 | read |
| Undated | 17 guns | Emmons pp. 190, 200 | read |
| 21 December 1814, sailing from Boston | 18 guns | Niles vol. VII p. 284, 31 December 1814 (l. 54081) | read |
| December 1814, aboard | "eighteen guns, of nine and eighteen pounders" | Cobb p. 39 (l. 1413) | read |
| At capture | "pierced for 22 guns, and mounting 18" | NC vol. 33 p. 72 | read |
| Undated (Admiralty record) | 16 × 12-pdr carronades and 2 × 6-pdrs | Winfield pp. 335 to 336 | read (owner's copy) |

- **Small arms:** blunderbusses, muskets and boarding pikes (Coggeshall p. 241). The boarders
  left arms on her deck enough for her next cruise (Cobb p. 39).
- **In the boat action** (read): Ordronaux "discharged one of his main-deck guns, loaded with
  canister shot and bags of musket balls" (Coggeshall 1861 p. 468), and was "slewing round
  one of his broadside guns" (Stevens p. 28). He double-shotted with "12-pound bags of musket
  balls" (Stevens p. 27), which fits 12-pdr carronades (judgement).
- **In the chase,** with the guns kept on deck for their weight, "the tier to leeward were most
  of the time under water" (Cobb p. 97, read): broadside guns on the flush deck.
- **No pivot gun** is mentioned in any source read, and none is drawn (§2.7). This is absence
  of evidence.
- **Ports against guns:** 22 ports (11 a side) for 18 guns, plus the two stern ports, leaves
  ports to spare (judgement).

### 4.2 People

| When | Men | Source | Mark |
|---|---|---|---|
| Leaving New York | "probably amounted to 150 souls", officers and marines included | Coggeshall p. 241 | read |
| The same | about 80 men and boys | Maclay p. 378 | read |
| At the boat action, 10/11 October 1814, after manning prizes | 33 at quarters, officers included; 37 prisoners aboard | Niles vol. VII p. 120 (l. 24238); Coggeshall p. 243 (its OCR has 87 prisoners, probably 37) | read; OCR |
| The same | 37 | Maclay p. 378 | read |
| The same | 38 by her log (35 tallied) | Stevens p. 27 | read |
| The same, by others | 100 (Emmons p. 200); "120 or 130" (James vol. 6 p. 237) | | read |
| After the action | 8 men fit for duty | Coggeshall p. 243; Maclay p. 384 | read |
| Undated | 127 | Emmons p. 190 | read |
| 21 December 1814, sailing from Boston | 130 | Niles vol. VII p. 284 (l. 54081) | read |
| The same, aboard | "a complement of one hundred and sixty-three men, all told" | Cobb p. 39 (l. 1415) | read |
| At capture | 130 (Collier's report as reprinted); 129 (Wikipedia) | | snippet; secondary |

- **December 1814** (Cobb p. 40, read): a captain, five lieutenants, nine prize-masters, and
  quartermasters, sailing masters, boatswains, gunners, carpenters and sailmakers. Below
  decks everything was cleared for prize goods except the water and provision casks, and
  the crew lived cramped.
- **The crew's terms:** all were on shares, from the captain down (p. 39).

## 5. Her history

### 5.1 Chronology

| Date | Event | Source | Mark |
|---|---|---|---|
| 1812 to 1813 | Built at New York, by Christian Bergh or by Adam and Noah Brown (§7) | Winfield; Mystic | read; secondary |
| 1814 | Owned by the estate of Mrs Charrten of New York, lately deceased (as of October 1814). Fitted out in France "by some Americans at Paris, and last from Cherbourg" | Niles vol. VII p. 120 (l. 24192) | read |
| Early 1814 | Nine prizes "on the enemy's coast, and sent into France or destroyed". March per Maclay p. 378 and Stevens p. 26 | Niles vol. VI p. 150, 30 April 1814 (l. 30740) | read |
| 4 to 10 April 1814 (at the latest May) | Six prizes into Havre: a London item under "London, May 18" with London dates to 1 June, so April. Maclay p. 379's "June" is a misreading | Niles vol. VI p. 368, 30 July 1814 (l. 78510) | read |
| By July 1814 | Chased into Cherbourg, and there "dismantled" by the French, who released a prize she had sent in | Niles vol. VI p. 304, 2 July 1814 (l. 62912) | read |
| 4 July 1814 | Left Cherbourg for home | her log, Stevens p. 26 | read |
| 21 August 1814 | Sank a brig by broadside in the Irish Channel | Niles vol. VIII p. 111 | read |
| August to September 1814 | Many prizes in the Channel and the Irish Sea | Niles vol. VII p. 120 | read |
| 6 September 1814 | Took the ship Douglass, 429 tons | Stevens p. 26 | read |
| 10/11 October 1814 | Becalmed off the south shore of Nantucket with Douglass. That night she beat off *Endymion*'s boats (§5.2) | James p. 237; Niles p. 120; Coggeshall pp. 241 to 244; Stevens pp. 25 to 32 | read |
| 14 to 15 October 1814 | Sailed from Holmes's Hole in plain view of *Endymion* at Tarpaulin Cove; reached Boston on the morning of the 15th | Stevens p. 31; Niles p. 120 | read |
| October to December 1814 | Ordronaux gave up the command and became a large shareholder; her first lieutenant took her | Cobb p. 40; Maclay p. 384 | read |
| 21 December 1814 | Sailed from Boston with 18 guns and 130 men, weighing at noon and running out at 6 pm | Niles p. 284; Cobb pp. 53 to 54 | read |
| About 26 to 27 December 1814 | A gale "at the closing of the fifth day from port" | Cobb pp. 77 to 93 | read |
| 28 December 1814 | Chased and taken by *Leander* and *Newcastle* (50-gun ships) and *Acasta* (40). *Leander* had left Halifax on 19 December and met the other two on the 24th | Gazette 17129 p. 729; Cobb pp. 93 to 109; James vol. 6 pp. 252 to 253 | read |
| Early 1815 | Fell astern of the frigates on the fourth night after her capture. Her arrival at Penzance, with praise of her sailing, was reported in the newspapers Cobb read in prison | Cobb p. 138 | read (hearsay) |
| March to April 1815 | Lines taken off at Deptford (ZAZ6177); masts and sails sketched (ZAZ6179) | RMG | read |
| 10 April 1815 | The Admiralty orders a copy built at Woolwich | Winfield; ZAZ6178 | read |
| 15 April 1815 | "has been captured and sent into England" | Niles vol. VIII p. 115 | read |
| 5 (or 3) May 1815 | The Navy Office draught for Woolwich (ZAZ6178) | RMG | read |
| 1815 | Surveyed at Deptford, damaged in coming out of dock, and broken up. The copy was never built | Winfield | read |
| 13 April and 10 May 1816 | Prize notices. The first, dated 13 April 1816, is the account of the hull, stores and head-money (agent Thomas Collier); the second, of 10 May, is *Newcastle*'s distribution, "Leander and Acasta in company" | Gazette 17129 p. 729; 17136 p. 911 | read |

Emmons p. 191 sums her up: she destroyed 13 prizes, sent some to France, and was finally
taken by Collier's squadron in December 1814 (OCR).

### 5.2 The boat action, 10/11 October 1814

All read; the conflicts are in §7.

- **The attack.** *Endymion*, 40-gun frigate, Captain Henry Hope, sent her boats under
  Lieutenant Abel Hawkins (James p. 237). There were five, one on each side, one on each bow
  and one at the stern (Niles vol. VII p. 120, l. 24217; the OCR has "stem"), with 104 men
  (Niles) or 111 (Coggeshall p. 242), officers and marines included.
- **The fight.** The boats were repulsed in about 20 minutes (Coggeshall p. 242). One was sunk
  with 43 men, of whom two were saved; three drifted off; one was taken with 36 men, of whom
  8 were killed, 20 wounded and 8 unhurt (Coggeshall pp. 242 to 243).
- **Her loss:** six killed and the Nantucket pilot Charles Hilburn; fifteen severely wounded,
  nine slightly, eight unhurt (Coggeshall p. 243).
- **The British loss, by James:** Hawkins, a midshipman and 26 men killed (28); the second
  lieutenant, a master's mate and 35 men wounded (37); the launch captured.
- **The calm.** She was becalmed and anchored with her prize nearby when the attack came
  (§6, T8).

### 5.3 Captains, owners, and her nation

**Her captains** (read):

- **John Ordronaux** commanded in 1814, through the boat action. Stevens p. 27 calls him a
  Frenchman. In 1812 he had commanded the privateer *Marengo*: a French privateer by Maclay
  pp. 379 to 380, and of New York by Emmons p. 200 and Niles Supplement p. 185.
- **The December captain** had been her first lieutenant. Cobb says Ordronaux gave her up
  "solely on account of indisposition" (p. 40). Cobb calls the new captain "a Frenchman by
  birth, an American for convenience" (p. 41).
- **Millen or Mellen.** In October her first lieutenant was "Mr. Millen" (Coggeshall 1861
  p. 469), or the first mate "Mellen", a Swede (Stevens pp. 27, 29). Cobb's Frenchman and
  Stevens's Swede cannot both be the same man, so whether the December captain was Millen is
  unresolved. "Nicholas Millin" is named only by Wikipedia and by the snippet of Collier's
  report.

**Her nation.** The sources make her a vessel of several nations (read):

- owned in New York;
- fitted out in France by Americans;
- dismantled by the French at Cherbourg;
- commanded by Frenchmen;
- her October first mate a Swede;
- in the last chase she showed no flag: "The brig carried no colours, nor showed any emblem
  of the country she hailed from, throughout the chase" (Cobb p. 104, l. 4204). She
  surrendered by rounding to and firing a gun to leeward.

Reed's modern model flies United States colours. The sources support a file that carries no
nation (judgement).

## 6. How she sailed: truth candidates

Each candidate is read unless marked otherwise; "strength" is judgement.

| # | When and where | What happened | Source | Strength |
|---|---|---|---|---|
| T1 | 28 December 1814, mid-Atlantic: a continuing gale and a heavy sea | Sighted soon after 8 am, she bore away under three reefed sails, then made sail and hauled close. The crew believed "we could haul closer upon the wind than the enemy", and on the wind she was gaining to windward of them (p. 96). Running from about 10 am, she saw *Leander* and *Newcastle* gain faster than *Acasta*: the light brig pitched while the heavy frigates drove through (p. 97). Shot first reached her about noon; she hauled on the wind again; the frigates closed as the wind rose, firing grape by 2 pm. She surrendered after 4 pm, nothing important lost aloft. A chase of about 8 hours | Cobb pp. 93 to 105; Maclay pp. 385 to 386; Gazette 17129 for the date and captors | Strong: her best evidence |
| T2 | The same chase | Cobb's own aside: "during the chase, she was once running off at the rate of twelve and a half knots per hour" | Cobb p. 138 (l. 5712) | Moderate: a single figure, not logged |
| T3 | 21 December 1814, 6 pm, running out of Boston Bay at night | The yards squared to the wind, "a stiff breeze, which bore us along at the rate of twelve and a half miles per hour". Cobb says "knots" elsewhere, so the unit here is loose (judgement) | Cobb p. 54 (l. 2045), read for this note | Moderate |
| T4 | About 26 to 27 December 1814, the gale | Topgallant masts housed and the lighter yards on deck (p. 78). Lying-to under the fore-and-aft foresail, she "made such bad weather" that the sail was taken in and she was put before the wind under bare poles (p. 79), scudding at about ten knots (p. 90). Later she lay-to under a close-reefed storm staysail only, "barely able to keep that to the wind" (p. 91). A sea over the larboard quarter carried away bulwark and deck gear (p. 93) | Cobb pp. 77 to 93 | Strong for the storm behaviour |
| T5 | Morning of 28 December 1814 | Storm canvas: a double-reefed foresail, a closely reefed fore-and-aft mainsail and a reefed jib. Every yard on deck but the fore and fore topsail yards. About 20 minutes to set those three and bear away (pp. 93 to 95). As the wind freshened in the chase she had to take in lighter sails aloft while the frigates held theirs "by their great strength and heavy dimensions" (p. 96); the lee guns were mostly under water (p. 97) | Cobb pp. 93 to 97 | Strong: her canvas against the frigates' |
| T6 | Evening of 28 December 1814 | Within a quarter of an hour of the surrender the wind began to ease, and by 10 pm it was "no more than a stiff wholesail breeze, the very one wanted for the brig; for with such, she could outsail any vessel in the British navy" | Cobb p. 105 (l. 4249) | A crew's opinion |
| T7 | Late December 1814 to early January 1815 | Under a British prize crew, and with rigging her own crew had cut, she made no more than 7 to 8 knots with the most favourable wind. The frigates hove-to every three hours for her, and on the fourth night she fell out of sight astern. The prize crew blamed "the too large size of her masts and spars, in comparison to her hull" | Cobb p. 138 | Weak: damaged and strangely handled |
| T8 | 10/11 October 1814, off the south shore of Nantucket | She lay becalmed while *Endymion* came up with a fresh breeze. She got the breeze at 2 pm (Niles) or 3 pm (Coggeshall, Maclay, Stevens) and stood on with the prize Douglass in tow, the frigate about 4 leagues (12 miles) off. At sunset it fell calm. At 7 pm both anchored, about a musket shot or a quarter mile apart, because the current set them ashore. She did not sweep | Niles vol. VII p. 120; Coggeshall p. 242; Stevens pp. 26 to 27; Maclay pp. 380 to 381 | Strong, for light airs |
| T9 | 14 to 15 October 1814 | With 8 men fit for duty, she weighed "as soon as the wind served". On the morning of the 14th she sailed from Holmes's Hole "in plain view of the Endymion", which was at anchor in Tarpaulin Cove, and reached Boston on the morning of the 15th | Maclay p. 384; Stevens p. 31 | Weak |
| T10 | 1814 cruise, March to October | "She has been chased by 17 different men of war, during the present cruise", and escaped all. Cobb heard on enlisting that she had been fortunate in sixty chases | Niles vol. VII p. 120; Coggeshall p. 242; Cobb p. 23 | Reputation, not a measurement |
| T11 | General | On a wind the great mainsail serves, and before the wind the square fore (Cobb p. 38). "A clipper of the first class" lying low in the water (p. 38) | Cobb p. 38 | The type's character |
| T12 | Design figures, not an account | Fincham's Ex. 1 (if her): the centre of effort 1.72 × breadth (about 44 ft) above the LWL and 0.0163 of the length from the middle; sail area 4.59 × the waterplane (9,240 to 9,410 ft²); moment of sail 204 × the waterplane | Fincham p. 72 | Balance checks for the build |

Not candidates:

- Penzance's newspapers called her a first-rate sailer (Cobb p. 138, hearsay).
- Maclay p. 380 has her "only a few days out of Boston" at the boat action, which is wrong.

## 7. Conflicts

- **Her rig's name:**
  - "hermaphrodite rigged" (Niles, Cobb, Coggeshall);
  - "brig" (her log, James, Emmons, Cobbett);
  - "brigantine" (Cobb);
  - "schooner" (the Admiralty's sheets, Winfield; Fincham's table of schooners).

  Steel's British "hermaphrodite" of 1794 is a different rig (§1.1). All describe the same
  rig.
- **Tonnage:** 310, 311, about 330 and 328 22/94 (§2.1): different rules of measurement
  (judgement).
- **The builder:** Christian Bergh (Winfield, read; Chapelle 1963, snippet) or Adam and Noah
  Brown (the Mystic record and Wikipedia, secondary). No period source names him.
- **The date of the boat action:**
  - 9 October (James p. 237);
  - 10 October (Stevens, from Nantucket accounts; the RMG catalogue of TRO/103/1);
  - 11 October (her log as published; Niles p. 120, where the page image reads "On the 1[?]th",
    the second digit damaged; Coggeshall; Maclay).

  Stevens explains the 11th as the log's sea day, which ran from noon to noon. A sea day
  begins at noon of the civil day before, so an action on the night of 10 October civil falls
  on 11 October by the log (memory for the custom; judgement for the fit). James's 9th is out
  by one more.
- **The boat action's numbers:**
  - men in the boats: 104 (Niles p. 120), 111 (Coggeshall p. 242), up to 146 in some accounts
    (Stevens);
  - the sunk launch: 43 men (Coggeshall; Cobbett via Niles Supplement p. 170), 48 by her log
    (Stevens p. 29);
  - her wounded: 15 severely and 9 slightly (Coggeshall p. 243), or 15 and 6 by her log
    (Stevens p. 29);
  - Emmons p. 200: 7 killed, 23 wounded, 30 minutes.
- **Guns** (§4.1): 14, 17 and 18 guns. Cobb's 9- and 18-pounders against the British record of
  12-pdr carronades and 6-pdrs. Were the guns changed between Boston and the survey, or is
  Cobb's memory wrong after 25 years? Unresolved. Winfield does not date his figures.
- **Her people:** §4.2. James's "120 or 130" is for October, not December, when she had 33 to
  38 aboard.
- **The December captain:** a Frenchman by birth (Cobb) against Millen or Mellen, a Swede
  (Stevens); §5.3.
- **The Havre prizes:** April 1814, not June as Maclay has it (§5.1).
- **Cobb's "Monday, December 21st"** (p. 53, l. 1913): 21 December 1814 fell on a Wednesday
  (memory and judgement: 8 January 1815 was a Sunday). The date agrees with Collier's report
  (snippet), so the weekday is the slip.
- **Leaving New York:** 150 men (Coggeshall) or about 80 (Maclay). Coggeshall's "when she left
  New York" sits oddly with her being fitted out in France (Niles); perhaps she crossed with
  few men and manned in France (judgement).
- **The sheets against Fincham's Ex. 1:**
  - drag: 33 in on ZAZ6177 against Fincham's 24 in;
  - rakes: 31 and 26 in against 33 and 28 in in 12 ft;
  - fore gaff: 32.9 against 37.1 ft;
  - royal yard: about 24.5 against 21.3 ft.
- **The gaff topsail's head:** a jack-yard or sliding gunter (the American usage) against a lug
  topsail (the Royal Navy's usage), on a Navy sketch (§1.2).
- **Marestier's depths:** draughts, or from the deck to the rabbet (Chapelle's footnote; §2.8).
- **Fincham p. 19:** the 18-gun brig's printed ratio (1,058) disagrees with its own columns
  (1,082).
- **The Mystic record:** "100'8"" against 110 ft 8 in (sic in the record).

## 8. What is open

**Unread sources:**

- **Collier's report of 29 December 1814,** reprinted in a Welsh newspaper: snippet only. It may
  give her rig, guns and men at capture.
- ***Leander*'s log, and the prisoner and muster lists:** HTTP 403.
- **Her log in the Boston Advertiser** of 17 and 18 October 1814: seen only through Stevens.
- **The Deptford survey report, the order of 10 April 1815, and the Navy Board's letters** (The
  National Archives): not online. They could give her guns, stores and spars at survey, and
  her condition.

**On the sheets:**

- **The dimension tables** on ZAZ6177 and ZAZ6178, and the figures of the sailing-trim note:
  illegible at 1280 px. The full-resolution image would confirm the measured draughts of
  about 11 ft 8¾ in aft and 9 ft 0 in forward (the owner's call, §9).
- **The keel bottom:** the scale bar's border or the faint line 0.6 ft higher. This changes
  the lateral plane by about 5% and the draughts by about 0.5 ft (§2.3).
- **"The Jack":** its function.
- **The headsails:** their count, and what each dashed light sail is.
- **The step in the deck line** near the mainmast, and the trunk.
- **The deck fittings.**

**Figures not finished:**

- **The Fincham sail-area test:** measure the jib and fore topmast staysail on ZAZ6179, then
  compare the principal sails with 9,240 to 9,410 ft². Measure the centre of effort's height
  against Fincham's 44 ft. A match would also strengthen the identification of Ex. 1 (§3.4).
- **Her centre of gravity:** in no source. GM rests on Fincham's class ratios and a weight
  budget.
- **Ex. 1:** her, or the 1815 Woolwich draught from her? Fincham does not say.
- **Ex. 2:** its identity (102.5 × 25.8 ft).
- **The rudder's maximum angle and rate:** in no source.

**On her history:**

- **Sweeps on her spring and summer cruises of 1814:** none found in Niles, Coggeshall, Maclay,
  Stevens or Naval Chronicle vol. 33. Vols. 31 and 32 were not re-opened.
- **The calibres at survey,** against Cobb's.
- **The builder.**

**Not re-checked by the checkers:**

- ZAZ6175 and ZAZ6181;
- the range of Fincham's second spar table (p. 79);
- the transom, the top-breadth offsets and the port sizes;
- the fore upper masts and the mast diameters;
- the smaller sail areas and the lower studding sail's size;
- the 8.2-ft BM with the plank.

**Not filed:** Stevens, Maclay, Emmons, the Naval Chronicle and the Gazette notices were read
online and are not filed in `docs/references/`. The librarian may want them.

**For the engine** (read, `freesail/` and `tools/` searched; R4's to judge):

- the engine has no sweeping, towing by boats or warping under way. Boats have oars, and the
  kedge heaves a grounded ship off;
- the schema has studding-sail booms and studding sails (`side`, `freesail/ship/schema.py:362`,
  `:394`);
- the topsail schooner has a precedent for a loose-footed fore gaff sail lapping the main
  (`tools/gen_ships.py:2633`);
- "the Jack" and a gunter or lug-headed gaff topsail may be new.

## 9. The owner's questions

One short round (plan §2, Phase 2). The research's lean is given after each question, and is
judgement.

1. **The fore gaff sail.** It is about a 33-ft gaff and 1,660 sq ft, with its clew drawn just
   abaft the mainmast. Build it to that size? If so, should it lap the mainmast and shift
   round it in stays, or be cut to clear it? *Lean:* to the sheet's size, lapping the main as
   the topsail schooner's foresail already does.
2. **Square sail on the main.** Carry the square main topgallant of the sail plan and Reed's
   model, set on two light yards (about 35 and 24 ft) above the gaff topsail? Carry Fincham's
   48-ft main square-sail yard, which the sketch does not draw? *Lean:* the topgallant yes;
   the square-sail yard as a later option.
3. **Light sails.** Carry the fore studding sails (lower, topmast and probably topgallant),
   "the Jack", and the large main topmast staysail? *Lean:* the lower and topmast studding
   sails and the main topmast staysail; "the Jack" only if R4 finds it cheap.
4. **The armament fit or fits:**
   - 16 × 12-pdr carronades and 2 × 6-pdrs (Winfield, undated);
   - 18 guns "of nine and eighteen pounders" (Cobb, December 1814);
   - 17 guns, or 14 by her log (October 1814).

   She had 11 ports a side and 2 stern ports, and no source shows a pivot gun. *Lean:*
   Winfield's as the default, the record nearest her capture.
5. **The complement for each fit:**
   - about 130 (163 all told) sailing from Boston in December 1814;
   - 33 to 38 after manning prizes in October 1814;
   - "probably" 150 leaving New York.

   *Lean:* 130 with the default fit.
6. **Spars.** Use Fincham's Ex. 1, which matches the sheet within about 3%, or the sheet's own
   figures where they differ? They differ on the fore gaff (33 against 37 ft), the royal yard
   (24.5 against 21.3), the drag (33 against 24 in) and the rakes. *Lean:* the sheet's, since
   it is her, with Fincham for what the sheet does not draw.
7. **The rig's name in the game:** "hermaphrodite brig" (the American usage of her day),
   "schooner" (the Admiralty and Winfield), or "brigantine" or "brig" (Cobb, James)? *Lean:*
   hermaphrodite brig.
8. **Load condition:** the draught's sailing trim (288 t; 9 ft 0 in forward, 11 ft 8¾ in aft),
   or something deeper, nearer Mammoth's proportions (about 13 ft mean on her beam)? *Lean:*
   the sailing trim, which is drawn on her own lines.
9. **Sweeps.** She was pierced for about 22 sweeps and the type used them often, but no account
   shows her sweeping; on 10 October 1814 she anchored in the calm. Make sweeps a new engine
   feature for her, or leave them out with the ports drawn? *Lean:* leave them out for now.
10. **Stiffness.** The metacentre is 1.6 m above her LWL, and the period's ratios and a weight
    budget suggest a GM of about 2.1 to 2.4 m, far stiffer than Speedwell's 1.0 m. But in the
    chase she shortened sail before the frigates did, and her prize crew thought her
    over-sparred (T5, T7). Accept a stiff hull, or tune lower? *Lean:* about 2 m, and let the
    truths for T1 and T5 decide.
11. **Images.** Is a higher-resolution RMG image of ZAZ6177 and ZAZ6179 worth buying, against
    the ruling of no full-resolution images? It would read the dimension tables and the
    sailing-trim figures and resolve the dashed sails. *Lean:* not needed for the build; the
    1280-px figures are consistent across both sheets and Fincham.
