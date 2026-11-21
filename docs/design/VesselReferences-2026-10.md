# Design note: references for the lugger, the smack and the later rigs (October 2026)

The research spree the owner asked for: public-domain hull, rig and type references for the
vessels planned that had none, the lugger and the smack first (spec M6 §19, package 43b),
then the later rigs of the vessel library (proposal §9, decision 11), then the owner's
wishlist (`VesselCandidates.md`, its end). Each figure below says where it was read. The
marks:

- **read**: read by this package from a page image or a catalogue entry, with the page or
  the object number. A figure read from a hand-written plan at catalogue resolution says
  how legible it was.
- **OCR**: taken from an OCR text and not checked against the page image; check before it
  becomes a game constant.
- **memory, unverified**: the lead's notes or general knowledge, not read here.

Quotations from the French and English texts of the period print the long s as s and keep
the period's spelling and accents otherwise; the OCR files have it as f.

Units. Lengths are English feet and inches unless stated. Forfait's *pied* (pied du roi)
is 0.3248 m, 1.066 English feet; Chapman's Swedish foot is 0.2969 m, 0.974 English feet
(the 1971 edition of Chapman rounds it to 0.296 m). Tons are tons burthen by the Navy's
rule ((keel for tonnage − 3/5 breadth) × breadth × half-breadth / 94; on the plans the
keel for tonnage is already the reduced keel, so burthen = keel × breadth × breadth/2 / 94).

## 0. The sources

**Fetched into the repository this package** (rows in `docs/references/README.md`):

| Text | What it gives |
|---|---|
| Forfait 1788, *Traité élémentaire de la mâture des vaisseaux* | The French lugger and chasse-marée in period: the lug sail and how it is shifted in going about (pp. 5 to 6), the chasse-marée, the taille-vent and the lougre (pp. 52 to 55), and three tables of proportions: Table V the schooners (p. 73), Table VI the chasse-marées and fishing boats (p. 74), Table VII the luggers (p. 75). Forfait was a French naval constructor (memory, unverified); this is the source Fincham 1843 abridges in his footnote on p. 60. |
| Lescallier 1791, *Traité pratique du gréement des vaisseaux et autres bâtimens de mer*, tome I | The rigging of every craft on the widened list, in period: the polacre (pp. 370 to 373), the lateen yard and how it is shifted (pp. 377 to 380), the bilander's sail (p. 390), the lug sail (pp. 391 to 392), galleys, feluccas, xebecs, pinks, barques and tartanes (pp. 394 to 401), snows (pp. 401 to 402), brigantines (pp. 402 to 403), bilanders (p. 404), ketches and doggers (pp. 407 to 408), luggers and chasse-marées (pp. 408 to 409), sloops, smacks and cutters (pp. 418 to 421). |
| Holdsworth 1874, *Deep-Sea Fishing and Fishing Boats* | The smack's trade: the welled smack and its well (pp. 139 to 141), working the longlines from a smack (pp. 137 to 139), the trawl smacks and trawling (pp. 65 to 72), Harwich's welled smacks from 1712 with their numbers to 1798 (pp. 231 to 232); and the English and Scotch luggers (pp. 104 to 105, 291 to 294). Later than the period, but he describes the old smacks of 23 to 36 tons as well as the new. |

**Held already and read again for this package**: Steel 1794 vol. I (the LUGGER, SCHOONER,
SNOW, HERMAPHRODITE, BILANDER and KETCH entries on the page before p. 221, cited below as
p. 220, the number not checked; the proportions for sloops, smacks and hoys and for
launches with lug-sails and settee-sails, p. 41; the POLACRE and BARK entries of the three-masted vessels; the smack's foresail and jib);
Fincham 1843 (On Luggers and Vessels of the Lateen Rig, pp. 59 to 61, read from the page
images because the OCR of the table is garbled); Falconer 1780 (BILANDER, BARK, HOY,
KETCH, LUG-SAIL, PINK, POLACRE, SAIC, SCHOONER, SETTEE, SLOOP, SMACK, SNOW, TARTANE).

**Consulted, figures quoted, not held whole**:

- Chapman, *Architectura Navalis Mercatoria* (Stockholm 1768), in the bicentenary edition
  (Adlard Coles, London 1971; Internet Archive `architecturanava0000fred`). The plates are
  Chapman's and public domain; the edition's introduction and its tables of each plate's
  data are the editors' and not, so the text is not held. The figures are facts from
  Chapman's plates and are quoted with the plate.
- Steel, *The Elements and Practice of Naval Architecture* (1805; the 1822 printing, IA
  `elementspractice00stee`): Hutchinson's remarks on the cod smack (Book I, § 10, p. 154),
  the glossary's WELL, and the list of draughts (a Berwick smack, a Southampton fishing hoy
  of 13 tons, a London trader of 60 tons, a Virginian pilot boat of 53 tons, a Bermuda
  schooner of 83 tons). The draughts are a separate folio not in that scan; not reached.
- Charnock, *An History of Marine Architecture*, vol. III (1802; IA
  `bim_eighteenth-century_an-history-of-marine-arc_charnock-john-author-o_1802_3`): the Navy
  lists with dimensions, read from the page images (pp. 267, 274, 277).
- Willaumez, *Dictionnaire de marine* (3rd ed., 1831; IA `dictionnairedem00willgoog`):
  CHASSE-MARÉE (pp. 145 to 146), TAILLE-VENT, SMACK, SEMAQUE, BÉLANDRE, POLACRE, BASTAQUE,
  CHICABAUD. OCR only, and rough; the entries quoted are legible.
- The Royal Museums Greenwich collections catalogue (rmg.co.uk): the catalogue text of the
  plans, and the figures written on the plans read from the catalogue's images (the images
  are the museum's and are not copied).
- E. W. Cooke, *Fifty Plates of Shipping and Craft* (London 1829; IA
  `fiftyplatesofshi00cook`): four etchings held as pictures (§ 5).
- Baugean, *Collection de toutes les espèces de bâtiments de guerre et de bâtiments
  marchands* (Paris 1814 on): the plate "Chasse Marée au plus près", from Wikimedia
  Commons, held as a picture.

**Not reached from this machine**: Gallica (BnF) refuses with a Cloudflare block, so the
Bonnefoux and Pâris *Dictionnaire de la marine à voile* (1856), Pâris's *Souvenirs de
marine* and Baugean's other plates on Gallica were not read; HathiTrust is behind a browser
check; the Google Books API answers with no quota; Wikimedia Commons answered 429 for most
of the session (the one picture was fetched as a standard thumbnail, which the error page
recommends). Pâris's plates were not found on Commons in the one search made. The Encyclopédie
méthodique, *Marine* (1783 to 1787, IA `bub_gb_yq0oOuVXpyUC`, 4.5 MB of OCR) and Lescallier's
*Vocabulaire* of 1783 were fetched to the cache but not read for this note.

## 1. The lugger: the chasse-marée of 1805

### 1.1 The candidates

| Candidate | What she was | Figures | Source |
|---|---|---|---|
| **L'Éclair, 1795** | A French gun-lugger taken by Captain Sir Richard Strachan, "Carrying No. 3 – 1? Pounder Guns" (the second digit of the calibre not legible), later H.M. lugger *Safety* (1802); "Profile and Plan of the Gun Lugger ... as taken off afloat", Portsmouth Yard, 2 July 1795, signed by the master shipwright | Length on the range of the deck 59 ft 3 in; keel for tonnage 45 ft 11 in; breadth extreme 20 ft 4 in, moulded 20 ft 0 in (each inch figure followed by a mark that may be ½); depth in hold 7 ft 0 in; burthen 101 or 105 and a fraction over 94 (the third digit unclear; the rule on 45 ft 11 in by 20 ft 4 in gives 100 92/94, so 101) | **read**, RMG ZAZ6306 (image j0576), catalogue: "Eclair (1795), a 59 ft, 3 gun Lugger, later renamed Safety (1802), as taken off while afloat at Portsmouth" |
| Le Coureur, 1778 | The French lugger taken in June 1778 (the action and the date from memory, unverified), modified as an 8-gun schooner; plan signed by Henslow, Plymouth, 18 September 1778 | Range of the deck 68 ft 10 in; keel for tonnage 52 ft 5¾ in; breadth extreme 22 ft 3¾ in; depth in hold 9 ft 10½ in; burthen 138 and a fraction (the rule gives 138 91/94) | **read**, RMG ZAZ6170 (image j0873) |
| Experiment, 1793 | A lugger in the Navy's list, "Built 1793, Liverpool" | Gun deck 72 ft 6 in; keel 56 ft 0 in; breadth 18 ft 6 in; depth 9 ft 0 in; 101 tons | **read**, Charnock vol. III p. 267 |
| La Gloire | A lugger "Taken 1781, from the French" | Gun deck 70 ft 3 in; keel 60 ft 7½ in; breadth 18 ft 10 in; depth 7 ft 10 in; 114 tons | **read**, Charnock vol. III p. 277 (the page number by the leaf count; the header is cut off in the scan) |
| Defender, 1809 | "H.M. Lugger Defender, late Bonne Marseill[aise]", a French lugger taken in 1809 and taken off at Sheerness in April 1810 before fitting as an 8-gun lugger; the plan carries a table of the masts and yards | Not legible at the catalogue's resolution (tentatively: mizen mast 37 ft 3 in, mizen topmast 17 ft 0 in, bowsprit 3? ft 6 in) | catalogue **read**; figures not; RMG ZAZ4734 (image j4832), ZAZ4735 and ZAZ4736 for her fitting |
| Forfait's lougre | The French navy's lugger by rule, two sizes | 72 pieds (76.7 ft) and 60 pieds (63.9 ft) long; breadth 0.288 and 0.258 of the length | **read**, Forfait 1788 p. 75, Table VII |
| Forfait's chasse-marée | The fishing chasse-marée and pilot boat by rule | 36 pieds (38.4 ft) and 24 pieds (25.6 ft); breadth 0.300 and 0.259 of the length | **read**, Forfait 1788 p. 74, Table VI |
| Fincham's examples | Three worked examples of the lugger rig | "Common" lugger 55.0 by 16.75 ft; lugger 77.0 by 22.7 ft; chasse-marée 38.6 by 11.6 ft (Forfait's 36-pied chasse-marée in English feet) | **read**, Fincham 1843 p. 61 |

**A correction to the lead's starting note.** RMG image J4582 is not the lugger: it is
ZAZ4272, "Eclair (captured 1793), a captured French corvette, as taken off at Sheerness in
April 1797 prior to being hulked" (and J4583 is its pair, ZAZ4273). The lugger is ZAZ6306,
taken off at Portsmouth in 1795. Of the lead's figures, 59 ft 3 in, 45 ft 11 in and 20 ft 4
in agree with the lugger's plan; the depth reads 7 ft 0 in (not 6 ft 11 in) and the burthen
101 (not 107); "built 1785 in southern Brittany" is on neither the plan nor the catalogue
entry and stays unverified.

### 1.2 The rig's proportions as read

**Forfait 1788, Table VII, *Lougres ou woguers* (p. 75), read.** Masts in terms of the
breadth, yards in terms of the length; the 72-pied column first, the 60-pied second.

| Spar | 72 pieds | 60 pieds |
|---|---|---|
| Main mast | 3.603 B | 3.455 B |
| Fore mast | 3.176 B | 2.759 B |
| Bowsprit | 2.794 B | 2.649 B |
| Mizen (tapecul) mast | 2.313 B | 1.888 B |
| Main topmast | 1.794 B | 1.091 B |
| Fore topmast | 1.470 B | 1.091 B |
| Main yard | 0.742 L | 0.573 L |
| Fore yard | 0.661 L | 0.454 L |
| Main topsail yard | 0.495 L | 0.424 L |
| Fore topsail yard | 0.429 L | 0.393 L |
| Mizen yard | 0.379 L | 0.364 L |
| Mizen outrigger (bout-dehors de tapecul) | 0.420 L | 0.364 L |
| Main mast's place | 0.072 L abaft the middle | 0.040 L abaft |
| Fore mast's place | 0.396 L before the middle | 0.364 L before |
| Mizen's place | "le plus près qu'on peut du couronnement" (as near the taffrail as can be) | the same |
| Rake: main, fore, mizen | 1¼ in, 8 lignes, 2½ in per foot | 1 in, 4 lignes, 2 in per foot |
| Bowsprit's steeve | 2 in per foot | 1¾ in per foot |
| Sail area / (L × B) | 5.242 | 4.037 |
| Centre of effort | 0.037 L before the middle | 0.024 L abaft |
| Height of the centre of effort | 1.902 B | 1.576 B |

The table also gives each spar's diameter and the yards' arms as fractions; they are on the
page image (IA `bub_gb_AQUHAAAAQAAJ`, leaf 120).

**Forfait 1788, Table VI, *Chasse-marées, bateaux de pêche et lamaneurs* (p. 74), read.**
Two masts, no topsails; 36-pied column first, 24-pied second: main mast 3.870 B and
3.586 B; fore mast 2.442 B and 2.069 B; main yard 0.712 and 0.678, fore yard 0.474 and
0.357, taille-vent yard 0.508 and 0.405 (the header says "with the breadth" but the figures
and Fincham's reading of them are of the length); main mast at the middle and 0.022 L
abaft; fore mast 0.415 L and 0.389 L before the middle; the main mast raked 6 in and 3 in
per foot, the fore 3 in and 1 in; sail area 2.408 and 2.172 times L × B, with the
taille-vent 1.609 and 1.071; the centre of effort 0.189 L and 0.181 L abaft the middle,
with the taille-vent 0.096 L and 0.042 L, and its height 1.439 B and 1.186 B, with the
taille-vent 1.146 B and 1.113 B. Forfait's rule for the merchant chasse-marée (p. 55): her
masts from Table VII's second column and her yards from its first, "parce que ces Navires
ne portent pas de huniers"; the taille-vent's area about half the mainsail's; her whole
area a quarter more than Table VI's first column, the centre of effort placed as there.

**Forfait 1788, Table V, the *lougre en goëlette* (p. 73), read**: the lugger's
schooner suit of Lescallier's heavy-weather note (§ 1.3), 55 to 72 pieds, breadth 0.285 to
0.257 of the length; main mast 3.580 B, fore 3.080 B, bowsprit 2.700 B, topmasts 1.230 B
and 1.200 B, mizen 2.280 B; main gaff 0.336 L, fore gaff 0.294 L, dry main and fore yards
0.517 L and 0.490 L, topsail yards 0.434 L and 0.394 L, mizen outrigger 0.420 L, mizen yard
0.369 L; main mast 0.064 L abaft the middle, fore 0.380 L before, the mizen on the taffrail;
sail area 3.519 L × B; the centre of effort at the middle.

**Fincham 1843 p. 61, *Proportions for the Masts, Yards, &c., for the Lugger and Lateen
Rig*, read** (the OCR of this table is unusable). For the 77-ft lugger (Ex. 2) and the
chasse-marée (Ex. 3): main mast hounded 3.5 B and 3.87 B, headed 0.1 and 0.076 of the
hounded length; fore mast hounded 0.77 and 0.63 of the main mast, headed 0.11 and 0.12;
mizen hounded 0.56 of the main, headed 0.08 (the lugger only); main topmast hounded 0.33 of
the main mast, pole 0.16 of the hounded length; fore topmast 0.8 of the main topmast, pole
0.19; mizen topmast 0.68 of the main topmast, pole 0.2; bowsprit 0.87 of the fore mast;
main yard 0.724 and 0.71 of the length; fore yard 0.860 and 0.65 of the main yard; mizen
yard 0.51 of the main yard; main topsail yard 0.66 of the main yard, fore topsail yard 0.9
and mizen topsail yard 0.57 of the main topsail yard; **the second (small) suit: main yard
0.8 and 0.7 of the large, fore yard 0.9, mizen yard 0.7, main topsail yard 0.7**; outrigger
0.42 of the length, fore-boom 0.45, "Menacle or boom" 0.38 (the word as printed); yard-arms
0.030 and 0.05 of the yard; main mast 0.04 L abaft the middle and at the middle; fore mast
0.396 L and 0.4 L before; mizen 0.396 L abaft; rakes (in 12 feet) main 12 in and 6 in, fore
6 in and 3 in, mizen 24 in; bowsprit steeved 6 in in 12 feet; heels below the load line
0.25 B and 0.26 B (main), 0.15 B and 0.17 B (fore), 0.08 B (mizen); centre of effort 0.037
L before the middle and 0.19 L abaft (as printed; Forfait's 0.189), its height 1.6 B and
1.44 B; sail area 3.95 and 3.44 times the load-water section; moment of sail 139.3 and 60.
His "common" lugger (Ex. 1, 55 by 16.75 ft) differs: main hounded 3.024 B, the mizen 0.63
of the main, the second main yard 0.84 of the large.

**Steel 1794 vol. I p. 41, "Launches and cutters with lug-sails", read** (the boat's rule,
for comparison): main mast 2¾ the breadth; fore mast 8/9 and mizen 5/8 of the main; main
yard 9/17 of the main mast, fore yard 9/17 of the fore mast; sprit 2 ft longer than the
mizen mast; outrigger 2/3 of the mizen mast.

### 1.3 How she is handled: the passages

- **The lug sail and going about.** Forfait 1788 pp. 5 to 6, read: in the *voiles au
  tiers* or *à bourcet* the halyard is made fast at one third of the yard, "de forte qu'il y
  a toujours deux tiers de la voile d'un côté du mât & sous le vent, & un tiers seulement de
  l'autre côté"; no braces or lifts, only halyard, sheet and tack; the tack and sheet
  cannot change roles as a square sail's do, so "il faut, quand on vire de bord, amener
  tout-à-fait la vergue, démarrer la drisse, changer la voile de côté pour la hisser
  ensuite" (lower the yard right down, cast off the halyard, shift the sail to the other
  side and hoist again), which is why large ships cannot be so rigged. Lescallier 1791
  pp. 391 to 392 says the same: in going about, "amener la vergue tout bas, démarrer sa
  drisse, & changer la voile de côté".
- **What carries her round.** Forfait p. 53: since the sails must be lowered to shift them,
  "le Bâtiment seroit forcé de virer sur son aire, c'est-à-dire avec sa vîtesse acquise,
  sans l'addition des focs & du tapecul qui favorisent & accélèrent efficacement le
  mouvement giratoire" (she would have to go about on her way alone without the jibs and
  the mizen, which drive the turn); the bowsprit runs in and out on a *chevalet* and an iron
  collar at the stem, so the jibs' effect can be set "plus ou moins" as the passage needs.
- **The English account.** Steel 1794 vol. I p. 221, read: the lugs "hang obliquely to the
  masts, their yards being slung at one-third their length, one on each lower-mast and
  topmast: the topmast fixes abaft the mast-heads, as those of schooners. Luggers sail well
  close hauled, and very near the wind. ... To the lee-clue of the sail is a sheet, and to the
  windward-clue a tack, which is occasionally shifted as the vessel goes about. When this is
  often repeated, they loose ground in stays. Some luggers have a small mast and a
  ring-sail set to it over the stern, and the foot spread by a small boom. In blowing
  weather they have small lug-sails, the tack of which hauls down by the mast, as their large
  sails would endanger them, should they chance to get up in the wind."
- **Taken aback, and the storm lug.** Forfait p. 52: the chasse-marée's sail "demande à
  être manœuvrée avec précaution & discernement: car un bateau à bourcet coëffé, ne se peut
  sauver que par un miracle quand il vente beaucoup"; to prevent it a much smaller mainsail,
  the *taille-vent*, is carried in bad weather, which "au lieu de border sur le côté du
  bateau, borde au pied du mât: par ce moyen, quand le Bâtiment vient vent devant, la plus
  grande portion de la voile se range dans la direction du vent, & celle qui recouvre le mât
  est trop petite pour produire de mauvais effets". The merchant chasse-marées of the
  Brittany coast and the Channel "ne déploient jamais leur grande voile dans l'hiver: il
  arrive même souvent qu'ils la laissent à terre pendant toute la mauvaise saison"
  (p. 53). Lescallier pp. 408 to 409: the taille-vent's foot is shortened and it tacks at
  the foot of the mast instead of at the side, and it keeps these small craft out of danger
  in heavy weather "s'ils faisoient chapelle ou prenoient vent devant"; "Quelques Lougres
  ont un jeu de voiles en façon de goëlette, pour être substituées dans les gros temps".
  Willaumez 1831, TAILLE-VENT (OCR): a bourcet sail about half the size of the mainsail,
  tacked near the main mast, set in luggers, chasse-marées and fishing boats "quand le vent
  souffle bon frais". Fincham 1843 p. 59, read: luggers have "commonly two sets of sails,
  large and small"; the rig "can afford but little support to the masts"; "The lug-sail
  likewise requires the most delicate management, and, under some points of sailing, the
  greatest care and attention, from its liability to be taken aback."
- **The lougre.** Forfait p. 53, read: "On voit dans la figure 29 un chasse-marée de guerre
  appellé lougre, ou par les Anglois woguer; il diffère des autres en ce qu'il porte un
  beaupré surmonté de deux ou plusieurs focs, un tapecul pour contrebalancer leur effet, &
  deux huniers." His rule for drawing the lug: the yard hoisted to a foot below the sheave
  and peaked at 60° to 70° to the mast; a few shrouds, "dont ceux de l'avant se décrochent pour permettre d'orienter mieux
  les voiles basses"; a stay to each mast and a halyard to each sail; no braces or lifts,
  "les ralingues en font l'office", the topsails alone having braces, lifts and bowlines.
  "Il n'y a point de Bâtimens qui portent proportionnellement autant de voilure que les
  chasse-marées, & particulièrement que les lougres"; they carry it high "quand les autres
  Navires sont obligés de prendre des ris". The French navy first used luggers in the war of
  1778 and soon gave them up: the masting is costly "& sujette à des accidens fréquens,
  parce qu'elle est mal appuyée & fatigue beaucoup; d'ailleurs ils exigent un équipage
  d'élite & fort nombreux" (p. 54). Lescallier p. 408: luggers are "bâtimens de guerre le
  plus souvent construits pour la marche, pour servir de Paquebots, d'Avisos, ou de
  Mouches", each mast with a topmast fidded abaft it in an iron ring, lug topsails, a long
  and little-steeved bowsprit with two or three jibs.
- **The chasse-marée herself.** Willaumez 1831 pp. 145 to 146 (OCR): the largest of about 100
  tonneaux go as far as the Antilles; the middling ones are decked; the smallest of the
  Morbihan are open amidships; two masts, the main at the middle "très incliné sur
  l'arrière", the fore upright two or three feet abaft the stem head; the mainsail "d'une
  grandeur énorme, qu'on amène sur le pont"; the foresail smaller than the mainsail and
  larger than the taille-vent; "les plus grands chasse-marées ont souvent tapecu, hunier et
  foc volans". BASTAQUE: in luggers, the shrouds with a runner; CHICABAUD: the spar the
  foresail tacks to in luggers.
- **The English fishing lugger.** Holdsworth 1874 p. 104, read in the OCR: the Yarmouth
  luggers, the largest about 36 tons, 52 ft keel, 17 ft beam, 7 ft hold, carry "a large
  dipping fore-lugsail with the tack hooking on to an iron bumkin outside the stem, and a
  working mizen and topsail", the mizen stepped a little to port to clear the tiller.

### 1.4 Recommendation for package 43b

**Base vessel: L'Éclair of 1795** (RMG ZAZ6306), a French gun-lugger of the war, taken by a
British squadron and taken off by a Royal Dockyard, so that her hull is on a British plan:
59 ft 3 in on the range of the deck, 45 ft 11 in keel for tonnage, 20 ft 4 in extreme
breadth, 7 ft 0 in in the hold, about 101 tons, three guns. **Rig: Forfait's Table VII,
the 60-pied column** (masts on her breadth, yards on her length), three masts with lug
topsails on the main and fore, a lug mizen sheeted to an outrigger, two or three jibs on a
running bowsprit; Baugean's "Chasse Marée au plus près" (§ 5) is the picture of exactly
this. On her breadth the column gives a main mast of 70 ft, fore 56 ft, mizen 38 ft,
topmasts 22 ft and a bowsprit of 54 ft; on her length, main yard 34 ft, fore yard 27 ft,
topsail yards 25 ft and 23 ft, mizen yard and outrigger 22 ft. One caution: her breadth is
0.343 of her length, beamier than Forfait's luggers (0.258 to 0.288) or his chasse-marée
(0.300), so masts set on her breadth come out tall for her length; the builder should
check the sail area against Forfait's 4.037 L × B and the centre of effort against his
0.024 L abaft the middle, and may scale the masts on the length instead (judgement). Experiment
(1793) and La Gloire (1781) are the English and French luggers of about her tonnage with
Charnock's dimensions, if a second hull is wanted.

**The rig's rules for the builder:**

1. **The lugs are dipping lugs, not standing lugs** (correcting the starting note). Every
   period source read (Forfait, Lescallier, Steel, Willaumez) slings the yard at a third of
   its length with the tack to windward and two thirds of the sail to leeward of the mast,
   and Forfait, Lescallier and Steel each say the tack must be shifted in going about. Going about, as an
   evolution: the jibs and the mizen bring her head to wind; the fore and main lugs are
   lowered (Forfait and Lescallier say right down; the dip round the mast without lowering
   fully is the boatmen's practice of later accounts, not read here), their tacks shifted
   to the new weather side and the yards passed round to the new lee, and the sails hoisted
   again; the lug topsails, which have braces, are trimmed like square topsails. Each tack
   costs ground: "When this is often repeated, they loose ground in stays" (Steel). The
   mizen may be left standing through the tack (judgement; Holdsworth's "working mizen").
2. **Taken aback is the lugger's danger.** A large lug aback in a blow ("coëffé") is the
   accident Forfait says only a miracle saves; the engine should make a lug aback press the
   mast and heel her much harder than a square sail aback (judgement on the size of the
   effect), and the master's standing orders should keep her off the wind's eye.
3. **The storm suit.** In blowing weather the mainsail is replaced by the **taille-vent**,
   about half its area (Forfait, Willaumez), its yard about 0.7 of the large main yard
   (Fincham's chasse-marée; 0.8 for the larger lugger), **tacked at the foot of the mast**,
   so that it is in effect a standing lug that does not need shifting and is safe aback
   (Forfait, Lescallier, Steel). Fincham's second suit gives the other yards (fore 0.9, mizen
   0.7, main topsail 0.7 of the large). In winter the merchant chasse-marée leaves her great
   mainsail ashore. A lugger may also shift to a schooner suit (Lescallier; Forfait's Table
   V for its spars), a later option.
4. **The rigging.** A few shrouds a side with runners (BASTAQUE), the lee shrouds slacked
   and the forward ones unhooked to trim the lower sails (Forfait); a stay to each mast;
   topmasts fidded abaft the lower mast heads in iron rings (Steel, Lescallier); the
   bowsprit runs, as the cutter's does.
5. **What she does well**: lies very near the wind and carries a great deal of sail high
   when others reef (Forfait, Steel); needs an elite and numerous crew (Forfait; no figure
   found for the complement, so the crew is judgement).

## 2. The smack

### 2.1 The candidates

| Candidate | What she was | Figures | Source |
|---|---|---|---|
| **The Culloden smack, 1746** | A Navy smack stationed in Scotland, built at Plymouth in 1746 by B. Slade | Gun deck 43 ft (the inches read 0 or 6); keel 34 ft 0 in; breadth 14 ft 0 in; depth 5 ft 6 in; 35 tons; 8 men; 2 guns | **read**, Charnock vol. III p. 274 (Hoys and Transports) |
| Chapman's English smack for flatfish | A plate of the type, 1768 | 39¼ Swedish ft between perpendiculars (38.2 ft), breadth moulded 13⅔ (13.3 ft), draught 6½ (6.3 ft) | **read**, Chapman 1768 plate LIX No. 3 (the 1971 edition p. 69) |
| Chapman's Stockholm *sumpar* | A fishing boat "with a well in which 150 lisponds of fish can be carried" (the well drawn with its holes) | 44 × 13½ × 4½ Swedish ft | **read**, Chapman plate LX No. 4 (1971 edition p. 70) |
| Holdsworth's old smacks | The trawl smacks before the 1850s: "Formerly the smacks were much smaller than at the present time, and ranged from 23 to 36 tons N.M. They were built with the principal object of living through anything" | 23 to 36 tons | **read** in the OCR, Holdsworth 1874 p. 66 |
| Holdsworth's welled cod smacks | The line smacks of the 1870s, about 68 tons, nine to eleven hands of whom six or seven apprentices | about 68 tons | **read** in the OCR, Holdsworth pp. 137, 141 |
| Saucy Jack, 1836 | The owner's candidate, a Barking well smack (from the kit) | 60 ft, 51 tons, crew 7 or 8 | **memory, unverified**: in no source reached |
| Mary, 1728 | A royal smack yacht | "a single-masted thirty-eight foot smack yacht", rebuilt at Plymouth from the Mary of 1702 | **read**, RMG ZAZ5842 (catalogue) |

### 2.2 The rig as read

Steel 1794 vol. I p. 41, "Proportions of masts, yards, &c. for sloops, smacks, and hoys",
**read** from the page image (the OCR lost the fractions; the small type of the last two
is uncertain): mast and topmast in one, 3¾ the breadth; mast to the hounds ¾ of the whole;
to the stop of the topmast 40/41 of the whole; topgallant mast to its stop 4/7 of the
length of the mast; boom 2/3 of the mast; gaff 3/5 of the boom; spread-yard 5/8 of the
mast; cross-jack yard 3/5 of the mast; topsail yard 4/5 of the cross-jack yard; topgallant
yard 5/6 (or 5/8) of the topsail yard; bowsprit 5/9 (uncertain) of the mast. Steel's
smack's foresail (vol. I, sail-making): triangular, No. 1 or 2 canvas, two reef bands
"sometimes", "but a bonnet is more frequently used to this sail" (OCR, legible). Lescallier
1791 p. 420: "Les Smacks, ou Semaques, sont de gros Bâtimens de pêche & de cabotage des
mers d'Écosse & d'Angleterre dont le Gréement est semblable à celui des Sloops; il n'y a de
différence entr'eux que celle de leur construction: celle des Smacks est plus renforcée, &
leur bout de beaupré est mobile dans un cercle de fer qui le contient, & peut se rentrer
très-facilement en-dedans du Bâtiment." Willaumez 1831, SMACK (OCR): one mast, with a
square sail (*voile de fortune*) hoisted and lowered with its yard; her topsail, when she
carries one, hollow in the foot and sheeted to the deck. Falconer 1780: "SMACK, a small
vessel commonly rigged as a sloop or hoy, used in the coasting or fishing trade; or as a
tender in the King's service."

### 2.3 The well and the trade: the passages

- **The well.** Holdsworth 1874 pp. 139 to 140 (OCR, read): "the well not being a tank
  fitted into the vessel, but a part of the smack itself. Two strong water-tight bulkheads
  are built entirely across the vessel from keelson to deck, enclosing a large space in the
  centre of the vessel; this is the 'well,' and a constant supply and circulation of water
  from the sea is kept up within it through large auger holes bored in the bottom of the
  vessel at various distances below the water line. The entrance to the well is on deck,
  through a hatchway; and in front and on each side of it runs what is called the
  'well-deck', which keeps the level of the water within certain limits when the smack is
  rolling about or pressed down under sail." Steel 1805 (1822 printing), WELL (OCR): "The
  Well in a fishing smack is a strong apartment to contain live fish, built water-tight in
  the middle of the hold, with a number of holes through its bottom, by means of which the
  fish are continually supplied with water, and preserved alive." A welled smack cost
  about £300 more than a dry-bottomed trawler of the same class (Holdsworth p. 141).
- **Harwich, the welled smacks' port.** Holdsworth pp. 231 to 232, quoting Groom: "In the
  year 1712, at Harwich ... welled-smacks were first constructed, suitable for fishing in
  the North Sea for cod-fish"; 12 by 1720, 30 by 1735; in 1745 four were taken up to carry
  troops across the Moray Firth; in 1766 Olibar of Harwich first fished the Dogger Bank
  with longlines; "in 1774 the number of smacks had increased to 62, of which 40 went
  regularly to the Dogger Bank to fish with longlines. In 1788 there were 78 smacks, and in
  1798 the number had increased to 96." Barking, Gravesend and Greenwich then built smacks
  of the kind and Harwich declined.
- **How a smack fishes with lines.** Holdsworth pp. 137 to 139: a string of 180 lines of
  40 fathoms, 7,200 fathoms with 4,680 hooks, baited with whelks; "When a 'shot' is to be
  made, the smack is put under easy sail, and kept as much as possible with the wind free,
  so as to make a fair straight course whilst the line is being paid out"; the line is laid
  across the tide, anchored every 40 fathoms and buoyed every mile; "when the operation has
  been completed the smack heaves-to in the neighbourhood till the tide has nearly done.
  Then the hauling up begins. The foresail of the smack is lowered, and the end buoy being
  taken on board, the vessel makes short tacks along the course of the line"; the cod are
  put alive into the well.
- **How a smack trawls.** Holdsworth pp. 70 to 71: the trawl is towed with the tide and a
  little faster than the stream, for five or six hours, under easy sail, "and this can
  only be done when the wind is generally fair, or more or less abaft the beam"; the mast
  stepped well forward for a large mainsail and room for the beam.
- **Why the cod smack must be weatherly.** Hutchinson in Steel 1805 (Book I, § 10, p. 154,
  OCR): a second cod smack built with sharper bows and a broader transom was "both a better
  sailer, and a better stormy weather vessel, than the other, which cod smacks require to
  be; for they are obliged to lie-to, to catch their fish, and to beat the sea in all
  weather possible, to get them alive to market."

### 2.4 Recommendation for package 43b

**Base vessel: the Culloden smack of 1746** (Charnock vol. III p. 274): 43 ft on deck, 34
ft keel, 14 ft breadth, 5 ft 6 in depth, 35 tons, 8 men, built at Plymouth by B.
Slade, the top of the spec's 25 to 35 tons and the only smack of the period found with a
printed set of dimensions; Chapman's English smack (38 by 13 ft) is the check on her shape.
The owner's Saucy Jack is 1836 and 51 tons (unverified), larger than the spec asks; she
could be a later, larger smack. **Rig: Steel's proportions for sloops, smacks and hoys**
(p. 41) rather than Fincham's revenue cutter: on 14 ft of breadth, mast and topmast in one
52½ ft, hounds at 39⅜ ft, boom 35 ft, gaff 21 ft, cross-jack (square sail) yard 31½ ft,
topsail yard 25 ft; a running bowsprit (Lescallier); the foresail with a bonnet (Steel).
Cooke's "Fishing Smack &c." (§ 5) shows this rig under sail in 1829.

**Her trade and her well:** a Harwich welled cod smack of the North Sea (in 1798, 96 of
them; the live cod to London), working longlines on the Dogger, or a Barking trawler. The
well, by Holdsworth: a watertight compartment between two bulkheads amidships, open to the
sea through holes in the bottom, its water level held by the well-deck. For the engine
(judgement): the well's volume below the water line gives no buoyancy, so her displacement
is her hull's less the well's, and the water in the well moves with her as part of her
mass; its catch is not a cargo to stow but a count of live fish, some of which die in bad
weather (Holdsworth p. 140: "some mortality also among the healthy fish ... from their
being knocked about in the vessel during bad weather"). Her evolutions: shoot the lines
under easy sail with the wind free; heave to while the tide runs; haul by short tacks with
the foresail lowered; tow a trawl with the tide, the wind fair or abaft the beam. Crew 8 (the
Culloden's); the 1870s cod smacks of twice her tonnage carried nine to eleven.

## 3. The later rigs

Thinner than §§ 1 and 2: the figures found and the passages, a base vessel where one has
measured figures, and what is missing. Chapman's figures are read from the 1971 edition's
tables of each plate unless marked OCR.

### 3.1 The tartane

- **Figures**: Chapman 1768 plate LVIII No. 16, "A French tartane (Vessels of war)", **read**:
  62¼ Swedish ft between perpendiculars (60.6 ft), breadth moulded 17 7/12 (17.1 ft),
  draught 6⅔ (6.5 ft); eight 4-pounders, four swivels; "used in the Mediterranean both to
  carry merchandise and as a fighting ship". Chapman's figure of the rigs includes a "Tartane with lateen
  sails" (OCR; the plate not checked). Lateen proportions: Fincham 1843 p. 61 (read) for the galley
  with two lateen yards (Ex. 6, 74.5 by 17 ft): main mast hounded 2.3 B, headed 0.06; main
  lateen yard 0.9 L, fore 0.88 of the main; main yard arms 0.0117 (weather) and 0.0234 (lee)
  of the yard; the fore mast raked forward. Steel 1794 p. 41, launches with settee-sails (read):
  main yard 3½ the breadth.
- **Passages**: Lescallier 1791 pp. 400 to 401 (OCR, read): one mast *à calcet* with a lateen
  sail like a galley's, shrouds *à colonne*, a jib to the *berthelot*; Provence, sometimes to
  the ocean ports and America; "Les Tartanes peuvent aller, soit avec le vent arrière, soit
  avec un vent trop fort, en gréant une voile quarrée, appelée tréou." The lateen yard
  (pp. 377 to 380): slung at about a third of its length; worked at the lower end by two
  *ourses* (vangs), at the upper by a brace and a vang; the shrouds *à colonne* (a pendant and
  a runner tackle) "se dépassent facilement, lorsqu'on veut changer la voile de côté pour
  virer de bord; ce qu'on appelle trelucher ou muder l'antenne"; a lateen vessel lies at five
  points, 56° 15', a square-rigger at six. Fincham p. 59 (read): the lateen "does not present
  so great a surface of sail in relation to the moment, as the lug; but possesses advantages
  in light winds, when close-hauled. When sailing before the wind, and in a rough sea, it is
  the most disadvantageous of all sails; and when by the wind, it is more liable to be taken
  aback than the common lug"; p. 60: the shrouds "set up as runners ... that they may be
  shifted when the vessel goes about". The rule the brief names, that the lateen's tack is
  shifted round the mast and the settee's is not, was not found in the texts read (memory,
  unverified).
- **Base vessel**: Chapman's French tartane, with the Roux-school watercolour already held.

### 3.2 The bilander

- **Passages**: Falconer 1780 BILANDER (read): the main-sail "a sort of trapezia, the yard
  thereof being hung obliquely on the mast in the plane of the ship's length, and the
  aftmost or hinder end peeked or raised up to an angle of about 45 degrees, and hanging
  immediately over the stern; while the fore end slopes downward, and comes as far forward
  as the middle of the ship"; the tack to a ring-bolt in the middle of the ship's length,
  the sheet to another in the taffarel; "Few vessels, however, are now rigged in this
  method". Steel 1794 p. 220 (OCR): "A merchant-ship with two masts, but different from
  others in the shape of the mainsail, which resembles a settee-sail. The head is bent to a
  yard, similar to the mizen yard of a ship, and hangs to the main-mast, as a ship's does to
  the mizen-mast. This method has proved inconvenient, and is now seldom used". Lescallier
  p. 390: the yard has a parrel, a halyard, a lift, two vangs and a brace; the sail tacks to
  the weather side and sheets to the taffrail, and is clewed up by buntlines and clewlines
  like a square sail; p. 404: the bilander is a Dutch cargo vessel rigged as a brigantine but
  for that mainsail. Willaumez, BÉLANDRE (OCR): flat-bottomed, built for cargo, northern,
  with leeboards; smaller ones of about 60 tonneaux rigged as a *heu*.
- **Figures**: none found with measured dimensions. **Base vessel**: none; a brig's hull of
  her size (judgement), with the two pictures held.

### 3.3 The xebec and the felucca

- **Figures**: **Minorca (1779)**, RMG ZAZ4270 (image j0234), **read**: "Zebeck of Eighteen
  Carriage Guns 6 Pdrs & Twenty Swivels", warrant for building at Mahon 10 November 1777,
  draught approved by the Board's warrant of 3 February 1778; length on the lower deck 96 ft
  9 in; keel for tonnage 78 ft 6 in; breadth extreme 30 ft 6 in, moulded 30 ft 2 in; depth in
  hold 10 ft 0 in; burthen 388 40/94 (the third digit read by the rule). Chapman plate LVIII
  No. 17, "An Algerian xebec", read: 130⅓ Swedish ft (126.9 ft), 25¼ (24.6 ft), draught 9⅔
  (9.4 ft); 28 guns (sixteen 6-pounders on deck, four 12-pounders on the forecastle, eight
  3-pounders on the quarterdeck), 30 musquetoons, 9 pairs of oars. Chapman plate LX No. 8,
  "French felucca with 10 pairs of oars", read: 43⅚ × 8⅚ × 2 7/12 Swedish ft. Fincham 1843
  p. 61 (read), the xebec (Ex. 4, 125 by 32 ft): main mast hounded 2.4 B, fore 0.95 of the
  main, mizen 0.6; main lateen yard 0.96 L, fore 0.9 of the main, mizen 0.45; main arms
  0.0125 and 0.033, fore 0.014 and 0.038, mizen 0.0136 and 0.0343 of the yard (weather and
  lee); main mast at the middle, fore 0.407 L before, mizen 0.407 L abaft; the fore mast
  raked forward; sail area 2.63 times the load-water section.
- **Passages**: Lescallier pp. 397 to 399: feluccas "n'ont guères que cinquante pieds de
  longueur, & que douze avirons par bande"; xebecs have a main and a fore mast with lateen
  sails, "le mât de trinquet est incliné sur l'avant", the shrouds *à colonne*; "Lorsque le
  vent est trop fort, on grée sur chacun de ces mâts deux voiles quarrées l'une sur l'autre";
  a mizen with a small top and topmast; xebecs rigged as polacres "perdent une partie de
  l'avantage de leur marche" (p. 373). Fincham p. 60: xebecs have sometimes three suits: a
  great square sail before the wind, large lateens by the wind, small lateens in bad weather.
- **Base vessel**: Minorca, an xebec designed for the Royal Navy to be built at Port Mahon,
  with a complete plan (whether and how she was completed was not read); Chapman's Algerian
  xebec for a larger corsair.

### 3.4 The polacre

- **Passages**: Lescallier pp. 370 to 373 (read): three pole masts of one piece without tops,
  caps or crosstrees, a rope ladder with wooden rungs on each side in place of topmast
  shrouds; "Leurs voiles de hune & de perroquet, n'ayant rien qui arrête leur descente le
  long du mât, s'amènent toutes deux jusques sur la vergue basse, ce qui est avantageux pour
  amener promptement dans une surprise de vent, ce qu'on appelle amener en paquet"; a broken
  pole mast means unrigging the whole mast; common in Provence and Languedoc. Falconer 1780
  POLACRE (read): "generally furnished with square sails upon the main-mast, and lateen sails
  upon the fore-mast and mizen-mast. Some of them however carry square sails upon all the
  three masts, particularly those of Provence"; "the men stand upon the top-sail-yard to
  loose or furl the top-gallant-sail, and on the lower-yard to reef, loose, or furl the
  top-sail, whose yard is lowered sufficiently down for that purpose". Steel 1794 vol. I,
  POLACRE (OCR) agrees. Willaumez, POLACRE (OCR): his plate C fig. 13 shows a square-rigged
  polacre going about.
- **Figures**: none found. RMG holds drawings (PAI2265 "Polacre Vaisseau Provencal", and
  others) but no plan with dimensions. **Base vessel**: none; a merchant ship's hull of about
  200 tons with pole masts (judgement).

### 3.5 The snow

- **Passages**: Steel 1794 vol. I p. 220 (OCR, legible): "A SNOW is the largest two-masted
  vessel ... The sails and rigging on the main and fore mast are similar to those on the same
  mast in a ship, the braces of the sails on the main-mast leading forward: besides which,
  there is a small mast, close behind the main-mast, that carries a trysail, resembling the
  mizen of a ship. This mast, called the trysail-mast, is fixed in a step of wood upon deck,
  and the head fixed by an iron clamp to the aftside of the main-top." Falconer SNOW (read)
  the same. Lescallier pp. 401 to 402: used for vessels under 150 tonneaux, chiefly by the
  French, English and Swedes.
- **Figures**: Chapman's snow privateer (the privateer plates, OCR, not checked): 93 × 25 Swedish ft,
  draught 10 ft 6 in to 11 ft 9 in (Swedish), 74 heavy lasts, fourteen 4-pounders, twelve 3-pounder
  swivels, 115 men.
- **Base vessel**: Harpy's hull (the brig file) with a trysail mast is the cheapest; Chapman's
  privateer if a snow of her own is wanted. Cooke's Prussian snow of 1829 is held.

### 3.6 The barque

- **Passages**: Falconer 1780 BARK (read): "a general name given to small ships: it is however
  peculiarly appropriated by seamen to those which carry three masts without a mizen
  top-sail". Steel 1794 vol. I, BARK (OCR): a Mediterranean vessel with three masts and no
  bowsprit, a lateen on a fore mast raking forward, a pole main mast with three square
  sails, a small mizen; and a line, garbled in the OCR, that English ships without a figure-head
  are called barks (Falconer says the same of the north-country coal trade).
  Lescallier p. 400: the Mediterranean *barque*, xebec-like, the main a pole mast with three
  square sails. The rig of the later barque (square fore and main, fore-and-aft mizen) is
  Cooke's "Barque, free trader, London Docks" of 1829 (held).
- **Figures**: Chapman's merchant "barks" of several classes (the merchant-ship plates, OCR only).
- **Base vessel**: none chosen; the term's two senses should be settled with the owner first.

### 3.7 The brigantine

- **Passages**: Steel 1794 vol. I p. 220 (OCR): "An HERMAPHRODITE is a vessel so constructed
  as to be, occasionally, a snow, and sometimes a brig. It has therefore two mainsails; a boom
  mainsail, when a brig; and a square mainsail when a snow". Lescallier pp. 402 to 403: two
  masts, the main raked aft and the fore a little forward, each with topmast and topgallant
  mast and the same square sails as a ship, "excepté que le grand mât n'a en bas qu'une
  vergue sèche, & point de voile quarrée, mais à sa place une grande voile à gui"; 80 to 150
  tonneaux, or 200 at most; the English use them most, and the Americans; a brigantine with
  a square mainsail added and her boom mainsail reduced is a *langard*. Willaumez BRIGANTIN
  (OCR): only flying topgallants, no royals.
- **Figures**: Dolphin (1836), RMG ZAZ5214 (midship section), ZAZ5215 (inboard profile, "a
  3-gun (originally 8-gun) brigantine (hermaphrodite-rig)", Symonds), ZAZ5226 (lower deck,
  with Bonetta), ZAZ5357 (sail plan as fitted at Sheerness, signed by John Fincham, the
  Treatise's author; re-rigged with larger sails at Chatham in 1840); catalogue read,
  figures not read. Steel 1805 has "Bodies of a brigantine of 10 guns, 16 swivels, and 201
  tons" and a building contract for an armed brigantine of sixteen carronades (OCR, not
  read).
- **Base vessel**: Dolphin for the owner's 1836 exception; for 1805, Steel's 201-ton
  brigantine when its figures are read.

### 3.8 The fore-and-aft schooner

- **Passages**: Steel 1794 vol. I p. 221 (read): two masts raking aft, two or three jibs, a
  square foresail on the fore, a gaff sail abaft each mast and a topsail above; "The
  main-stay leads through a block, at the head of the foremast, and sets up upon deck by a
  tackle. By these means, the sail abaft the foremast is not obstructed when the vessel goes
  about, as the peek passes under the stay. Schooners sail very near the wind, and require
  few hands to work them." Falconer SCHOONER (read).
- **Figures**: Forfait 1788 Table V (read): the *aviso en goëlette*, 55 to 65 pieds, breadth
  0.286 to 0.280 L; main mast 3.000 B, fore 2.907 B, bowsprit 1.500 B, topmasts 1.597 B and
  1.541 B, jib-boom 1.000 B; main boom 0.660 L, gaffs 0.344 L and 0.288 L, dry yards 0.464 L,
  topsail yards 0.352 L, topgallant yards 0.224 L; main mast 0.024 L abaft the middle, fore
  0.372 L before; sail area 3.642 L × B; centre of effort 0.091 L before the middle.
  Chapman's schooner privateer (OCR, not checked): 96 × 23¾ Swedish ft, 66 heavy lasts, 100
  men. Chapelle 1930 (held) has the pilot schooners.
- **Base vessel**: from Chapelle 1930 (held), a pilot schooner of the period; Forfait's aviso
  for the rig's proportions.

### 3.9 The sloop

- **Passages**: Lescallier pp. 418 to 420 (read): one mast with a boom mainsail and sometimes a
  flying topsail, a long, little-steeved bowsprit with three or four jibs; "ils portent à
  quatre aires de vent, & même encore plus près. Ils virent de bord fort lestement; il suffit
  pour cela de changer la barre, le Bâtiment fait bientôt tête au vent, qui donnant aussi-tôt
  sur l'autre côté de la voile, fait de lui-même passer le gui à l'autre bord; on ne fait que
  retenir un moment le petit foc ou trinquette pour laisser abattre"; before the wind the
  mainsail is lowered and a square *voile de fortune* set with a topsail above it. Falconer
  SLOOP (read).
- **Figures**: Chapman plate LVIII No. 15, a Bermuda sloop, **read**: 65½ × 21¾ Swedish ft
  (63.8 × 21.2 ft), draught 12⅔ (12.3 ft), displacement 4,751 cubic Swedish feet; ten
  4-pounders, twelve swivels. Steel p. 41 for the spars.
- **Base vessel**: Chapman's Bermuda sloop.

### 3.10 The ketch

- **Passages**: Steel 1794 vol. I p. 220 (OCR): two masts; the main mast with a topmast,
  carrying a mainsail, topsail and topgallant sail like a ship's, and sometimes a gaff
  "wingsail" abaft it; the mizen sometimes with a topmast and topsail and a mizen like a
  ship's. Falconer KETCH (read): "usually from 100 to 250 tons burthen", principally used as
  yachts and as bomb-vessels. Lescallier p. 407: main and mizen each with a top and an upper mast, which carry a
  topsail and a mizen topsail (*perroquet de fougue*) shaped like a ship's; the main and
  mizen sails gaff sails; a long bowsprit of one piece for large jibs.
- **Figures**: Chapman's ketch privateers (the privateer plates, OCR, not checked): 85 × 23 Swedish ft,
  54 heavy lasts, twelve 4-pounders, 9 pairs of oars, 90 men; and 76 × 21, 42 lasts, eleven
  guns, 70 men.
- **Base vessel**: Chapman's ketch privateer, when the plate is read.

## 4. The owner's wishlist

The catalogue entries read; the plans' figures where legible.

- **HMS Indefatigable, 1784.** RMG ZAZ1953: "the body plans, stern board outline ..., sheer
  lines with inboard detail, and longitudinal half-breadth for Indefatigable (1784), a 64-gun
  Third Rate, two-decker, as built and launched at Bucklers Hard by Henry Adams", fitted at
  Portsmouth July to November 1784; ZAZ1407, her lines with Stately's, "based on the lines
  for 'Raisonable' (1768)"; ZAZ1280, the class's inboard profile. The razee's plans were not
  found in the one search made. No figures read.
- **HMS Sphinx, 1775.** RMG ZAZ3917, the proposed draught, 23 April 1773, signed by Williams,
  with a table of mast and yard dimensions (not legible at catalogue resolution); read from
  it: length on the lower deck 108 ft 0 in; keel for tonnage 89 ft (the inches unclear);
  breadth extreme 30 ft 0 in, moulded 29 ft 6 in; depth in hold 9 ft (the inches 0 or 6);
  burthen about 429 tons; twenty 9-pounders on the upper deck. Her as-built lines (j4272),
  decks and platforms are in the same series (RMG objects 83709 to 83714 and 83769).
- **The Duchess of Kingston's yacht.** RMG HIL0239: "an unnamed 81ft three-masted Yacht (no
  date), for the Duchess of Kingston", signed by James Martin Hilhouse; the catalogue dates it
  between 1772, when Hilhouse set up in business, and 1773, when the duchess left England on
  the duke's death. This disagrees with the "1778" of the wishlist; the owner's kit page
  should be checked against it.
- **HM brigantine Dolphin, 1836.** See § 3.7.

## 5. Pictures held

Five new public-domain pictures in `docs/references/images/` with their provenance in that
folder's README: Baugean's "Chasse Marée au plus près" (the lugger's rig exactly: three
masts, lug topsails on the fore and main, the mizen lug to an outrigger, a jib on the
bowsprit), and four of E. W. Cooke's etchings of 1829: "Fishing Smack &c." off Calshot
Castle (the smack under sail: gaff mainsail on a long boom, topsail, foresail and jib on a
running bowsprit), "Lugger on the Beach at Brighton" (an English two-masted beach lugger),
"Prussian Snow" (the trysail mast abaft the main) and "Barque, Free Trader, London Docks".
Not held, the museum's: RMG PAJ1574, Baugean's "Chasse-Marée, au plus du vent"; RMG N18919, a
model of the Gravelines chasse-marée Jupiter (1885 to 1900), the late three-masted type with
a dipping fore lug and two lugs on the main.
