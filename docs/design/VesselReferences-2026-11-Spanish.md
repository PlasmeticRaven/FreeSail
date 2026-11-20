# Design note: the Spanish navy's sources for package 90 (November 2026)

**Revised 2026-11-19 on Winfield's passages sent by the owner, and the owner's answers of that
day.** The owner sent the passages of the decisions sheet's Part D that they found, with their own
readings of two of Monleón's prints, and said, verbatim: "I went through Winfield for some of the
requested passages, I was not able to find everything requested, so you shall have to fill in some
things from other research or judgement". What the passages give the package is set down in §7 to
§17 below, in the lead's form, by page, in this note's own words: the units and how a row is
measured (§7), the ranks (§8), the tartanas (§9), the coastguard (§10), the místicos (§11), the
polacras (§12), the xebecs after 1750 (§13), the corvettes' chapter (§14), the complements of 1788
and 1803 (§15), the ordinance of 1803's guns by deck (§16) and the *Diana*'s whole entry (§17). The
head's units, §1 to §6's pointers and §4's label of the length are brought into line with them. No
sentence of the book and no whole table of it is in this note; the owner's own readings of the
prints are quoted as theirs. Which of Part D's items were found is marked in the decisions sheet,
`Decisions-Package90-2026-11.md`, Part D.

The owner's shelf holds Rif Winfield (with John Tredrea, Enrique García-Torralba Pérez and
Manuel Blasco Felip), *Spanish Warships in the Age of Sail, 1700–1860*, Seaforth, 2023, a
modern work under copyright: it is not in the repository and is never copied into it. The
owner reads the passages package 90 needs and sends them to the lead; the facts in them are
set down here, in the lead's words, cited by the page of the owner's edition, for the ships
session's design documents (Build-Ships.md §5.0's ladder of evidence, where a particular
read from Winfield is a rung-B figure, and his reproductions of plans point at the rung-A
originals). The ships session asks the lead for further passages by title and class, and
the owner sources them if they exist (the owner's word, 2026-11-06).

**Units.** Winfield's dimensions for Spanish ships are in **pies de Burgos** (0.2786 m; the book's
own figure is 278.635 mm, Winfield et al. 2023, pp. 41-46, §7), not
English feet, as his own metres show: the *Purísima Concepción*'s 213 ft 9 in is 59.55 m
only at that foot (213.75 × 0.2786 = 59.55), and the *Diana*'s 124 ft is 34.55 m the same
way. The game's constants are metres from his metres; an English-foot figure from a Spanish
row is wrong by eight and a half per cent. The game already holds the pie de Burgos for
Tofiño's tides (`docs/dev/TuningNotes.md`, package 39d: 0.2786 m, the vara castellana
0.8359 m) and the braza of two varas. Weights of broadside are given by Winfield in libras
with his own pounds beside them (1,212 libras as 1,308 lb); take his pairs as he gives them
and do not re-derive the ratio. (2026-11-19: the book's own libra is 0.4608 kg, 1.59 per cent
heavier than the English pound, a ratio the pairs do not follow; the pairs stay as given, §7. One
row of the passages is in English feet, *Gitano*'s, marked so by the book: §13.)

## 1. The tartane (Winfield pp. 1249 to 1252)

Small coasting craft, almost all in trade, now and then taken up as coastguard vessels for
reconnaissance. The rig fore-and-aft: a large mainmast and a very small mizen. Monleón's
print of one at rest (p. 1249) shows the main spar big for the hull, a square topsail on the
mainmast "for stability", and the diminutive mizen that was the custom. The type was common
across the Mediterranean under other flags but found little favour in Spain: seven tartanas
are known in the Spanish navy's service, three bought or chartered from French builders and
two from a private builder in Spain. For the game: the Spanish navy's tartana is a role
(coastguard, reconnaissance) on a trader's hull, and the trader's and fisherman's fits come
first; a French-built hull is in keeping with the record. The square topsail over the
lateen is in the Roux-school watercolour too (`docs/references/images/`; the owner's
correction of 2026-11-06 to the lead's first reading), so the two sources agree: **the
tartane's rig is a lateen mainsail with a square topsail above it on the mainmast, a lateen
on the small mizen, and one or two headsails on the long bowsprit**, the count of headsails
by judgement from the sources together and the hull's proportions (the watercolour shows
two). (2026-11-19: **one headsail, and the topsail loose-footed with no lower yard**, by the
owner's reading of Monleón's print and the other tartane prints they have seen: §9.)

## 2. The polacre (Winfield pp. 1083 to 1084)

Spanish classification went by rig and not by hull or role, so "polacra" named a rig carried
by hulls as unlike as brig-schooners, corvettes and jabeques. The navy had few: eight in the
records between about 1780 and 1818. The rig's mark is the **pole mast**: a mast that reads
as one spar without separate topmast and topgallant, made of two or three poles scarfed
together and held by iron rings, so without tops and crosstrees. The weight aloft is less and
the ship handier; the yards can be lowered and raised without the obstruction of the tops
(the reason the square sails of a polacre are handed from the deck by lowering the yards,
Lescallier's account of the rig, `VesselReferences-2026-10.md`). The cost is a mast less able
to stand a strong wind, which kept the rig in the Mediterranean. Monleón's print (p. 1084;
the owner's copy sent 2026-11-06, cited and not held) shows the owner's chosen plan: a
lateen on a forward-raked foremast, square sail on a pole mainmast (course, topsail,
topgallant), a lateen mizen, and the jibs on a long bowsprit. For the game: the polacre's
engine model is the bilander's problem (a lateen and square sails on one hull, B3.1's
handling for the lateen) with the pole mast's handling for the square sails (the yard
lowered to hand the sail, no tops to send men to), a thing the generator does not yet say;
the design document must say it before the file. (2026-11-19: the eight polacras' entries, pp.
1083-1086, and the owner's own reading of the print, which gives three headsails on a reasonably
short bowsprit, the main and mizen raked aft, and a small loose-footed topsail over the lateen
mizen: §12.)

## 3. The xebec (Winfield pp. 1134 to 1136)

The Spanish jabeque was a warship built to meet the Barbary states' xebecs preying on the
trade through the Strait, the galley's successor once the galley could neither match a
broadside nor keep the sea in winter. A three-masted sailing ship of shallow draught with
sweeps enough for the coast and a broadside like a sailing ship's: a weapons platform, not a
weapon as the galley was (two to six bow guns and the ram). The first ones lateen on all
three masts; through the century mixed square and lateen plans were tried, trading the
lateen's speed and weatherliness against the square rig's smaller crew. Monleón's print (p.
1135, cited and not held) shows what reads as a sixteen-gun xebec under oars and foresail in
a moderately heavy sea, a large party at the mainsail, the oarsmen crowded between the
gunports on the gun deck: the labour the rig and the sweeps together ask. The
**chambequín**, late in the century and few, was a xebec hull entirely square-rigged on light
masting: faster than frigates and than lateen xebecs in the waters between Mediterranean
and Atlantic conditions, and with a smaller crew; *Volante* and *Andaluz* (ii) were converted
to it in 1765 at the governor of Buenos Aires's request, so that American seamen without
lateen experience could work them. (2026-11-19: the ship entries, §13, give *Aventurero*
converted in 1765 and *Andaluz* (ii) in 1778, both for Buenos Aires, and no conversion of
*Volante*: the difference is recorded, not resolved.) Few xebecs before 1750; the type's expansion followed the
peace with Algiers of 1748 that left the galleys without an enemy. Two sizes: 14 to 22 guns
with 4-pounders, and 30 to 32 guns with 8-pounders; the larger carried a frigate's count of
guns but not her weight of metal. Armament by the Artillery Regulation of 5 August 1752:

| Rate | Main battery | Quarterdeck and after castle | Pedreros (swivels) |
|---|---|---|---|
| Xebec of 30 | 20 × 8-pdr | 8 × 4-pdr on the quarterdeck, 4 × 2-pdr in the after castle | 22 × 2-pdr |
| Xebec of 18 | 18 × 6-pdr (the 18-gun packet-boat's standard, understood the same) | | 30 × 2-pdr |
| Xebec of 14 | 14 × 4-pdr | | 20 × 2-pdr |

For the game: the xebec is the Spanish navy's and the regency's cruiser both (decision 56's
role), the sweeps a fit, the 14 and the 30 the two sizes to choose between for the file; the
chambequín is a fit of the hull (square on all three) if the mixed-rig generalising makes it
cheap, else booked.

## 4. The *Purísima Concepción* class, three-decker of 94, later 112 guns (Winfield pp. 406 to 410)

Two ships: *Purísima Concepción*, ordered at Ferrol 2 June 1778, yard no. 64, keel 29
February 1779, launched 24 December 1779; *San José*, ordered 28 July 1781, launched 1783,
taken at Cape St Vincent 14 February 1797 by Nelson in *Captain* and HMS *San Josef* to 1846.
Begun to Jorge Juan's "sistema inglés" like the *Santísima Trinidad*, amended by Francisco
Gautier as 90-gun three-deckers with no guns on quarterdeck or forecastle, and built by José
Joaquín Romero Fernández de Landa, who thinned the scantlings of the upper works for
stability and speed and for want of great timber: the only three-deckers of the "sistema
francés". Sea trials from Cádiz 20 August to 18 September 1784 led to both being rebuilt at
Cádiz through the later 1780s (1786 to 1793 for the *Concepción*): 18 × 8-pounders added on
the upper works, the upper deck's 18-pounders replaced by 12-pounders, the broadside falling
from 1,212 libras (1,308 lb) to 1,188 libras (1,282 lb), which became the standard of every
later 112. A sixteenth pair of lower-deck ports was cut at Cádiz in 1791 for both, unarmed in
Spanish service and armed by the British in *San Josef*. In 1803 at Ferrol the *Concepción*
was altered to 116: 8 × 48-pdr obuses in place of ten 8-pounders, 6 × 24-pdr obuses on the
poop, the upper deck's 12-pounders back to 18-pounders; broadside 1,508 libras (1,627 lb).

| | Figure (Winfield's, pies de Burgos and his metres) |
|---|---|
| Eslora, quilla (the keel) | 213 ft 9 in, 190 ft 10 in (59.55 m, 53.12 m). **Revised 2026-11-19:** labelled "Length overall" until the book's definitions were read; the eslora is the length on the lowest planked deck over both overhangs, neither the length overall nor the British gun deck's length (§7) |
| Breadth, depth | 58 ft 0 in, 29 ft 0 in (16.16 m, 8.08 m) |
| Tons | 2,476 and 2,456 (arqueo); 5,167 t displacement |
| As rebuilt | 220 ft 6 in, 186 ft 0 in × 58 ft 4 in × 28 ft 9 in (61.30, 51.82 × 16.25 × 8.01 m); 2,771 tons |
| Men | 839 |
| Guns, as built, 94 | LD 30 × 36-pdr; MD 32 × 24-pdr; UD 32 × 18-pdr |
| Guns, 1780s, 112 | LD 30 × 36; MD 32 × 24; UD 32 × 12; QD 12 × 8; Fc 6 × 8 |
| Guns, 1803, 116 | LD 30 × 36; MD 32 × 24; UD 32 × 18; QD 4 × 8 + 6 × 48-pdr obuses; Fc 4 × 8 + 2 × 48-pdr obuses; poop 6 × 24-pdr obuses |

Her service, for the scenarios: flagship out of Ferrol 18 May 1780 and with Córdova's
combined fleet in the Channel campaigns of 1780 (the convoy of 52 taken 9 August 1780), 1781
and 1782; Córdova's flagship October 1781 to April 1782; the siege of Gibraltar September
1782 and present, not engaged, at Cape Spartel 22 October 1782; in ordinary at Cartagena to
1784; rebuilt at Cádiz 1786 to 1793; Lángara's flagship to Toulon October to December 1793;
Mazarredo's flagship from 1795; at Cape St Vincent 1797 as Morales de los Ríos's flagship (8
dead, 21 wounded); with the combined fleet to Brest August 1799 and blockaded there to April
1802; in ordinary at Ferrol from 1802; recommissioned to Cádiz September 1809; driven ashore
on the French-held shore of Cádiz Bay in the storm of 7 March 1810 and burnt by French troops,
sunk 9 March 1810. The plans Winfield reproduces: her deck plans of 1795 with 110 guns laid
out, the admiral's cabins on the toldilla and the captain's and lieutenants' on the alcázar
(Museo Naval, Madrid, PB_0050, p. 409); the draught of *San José* as taken, with the
sixteenth pair of lower ports (National Maritime Museum, Greenwich, J1945, p. 410), the
rung-A sources for her lines; the Greenwich rule holds for the one and the Museo Naval's
terms are to be read for the other before either file is held in the tree. Brenton (1823)
on *San Josef*: "uniting all the superior qualities of a ship of the line with the sailing
abilities of the fastest frigate", and Nelson's "the finest ship in the world": the handling
the file should give her. For the game: the first three-decker, three gun decks and the
poop's obuses, a first rate's complement of 839, the 1809 fit the one for the war's
scenarios (116 guns, the 1803 alteration) and the 1797 fit (112) for St Vincent. (2026-11-19:
a 112's company by kind by the regulations of 1788 and 1803, §15; the ordinance of 1803's guns by
deck beside her own, §16. The class's own pages were not sent again: the keel's and the rebuilt
length's digits stay as printed.)

## 5. The *Diana*, corvette of 20 (Winfield p. 930)

The Danish frigate *Diana*, built 1804, taken at Cartagena with the declaration of war,
last mentioned 1832. 124 ft × 32 ft 6 in × 16 ft (34.55 × 9.06 × 4.46 m), 335 t, 167 men.
Guns: 20 × 24-pdr carronades as captured; 20 × 30-pdr carronades as first rearmed (the fit
of her plan of 1809 to 1810, "del porte de 20 carronadas de á 30"); on 31 October 1817, 12 ×
12-pdr, 8 × 30-pdr carronades, 4 × 3-pdr obuses. Her draught is held:
`docs/references/images/corvette-diana-1809-plano-bvmdefensa.jpg` (CC BY 4.0, Archivo
Histórico de la Armada Juan Sebastián de Elcano / Biblioteca Virtual de Defensa, record
1037832), the rung-A source for her lines, with a table of her particulars on the sheet in
the navy's units to be read against Winfield's row. (2026-11-19: the whole entry, sent by the
owner, holds nothing more than this section has: §17.)

## 6. Pictures cited and not held

The three the owner sent on 2026-11-06 as photographed from Winfield's pages: Rafael Monleón
y Torres's print of a polacre under sail (p. 1084) and his print of a xebec under oars and
foresail (p. 1135), and the Greenwich draught of *San José* (J1945, p. 410). Monleón (1843 to
1900) is public domain by age, and the originals are the Museo Naval's; the book's
photographs of them are not copied into the tree. When a direct source of either print is
found (the Museo Naval's catalogue or a Commons file with its provenance) it goes into
`docs/references/images/` with the others; the Greenwich draught is cited by its object
number as Gwyn's bilander is.

**Added 2026-11-19.** The owner's photograph of Monleón's print of a místico at anchor (the
místicos' chapter, pp. 1195-1201) is held in the owner's private notes, not in the tree, a check
for the eye. Monleón's tartane print was not sent (the owner judged its reproduction too poor to
read) and the polacre print was not sent again; the owner's own readings of both are recorded
(§9, §12), in their words, as checks for the eye and never sources of points. The book reproduces
three Spanish xebec plans and two models (§13): the draught of *Gitano* (Museo Naval, Madrid,
PB_album_06_05), the plan of the *Cazador* class (plate 17 of the Marqués de la Victoria's album)
and *Aventurero*'s draught (its number cut off in the owner's copy); the models of *Cazador* (MNM
0367) and *Aventurero* (MNM 2653). None is held; each is cited by its number, and a direct source
is to be sought as for the others.

## 7. The units, and how a row is measured (Winfield et al. 2023, pp. 41-46)

**Length.** Before the Royal Ordinance of 25 July 1750 Spanish shipwrights measured in codos and
dedos; the book takes the codo de ribera of 33 dedos (574.68 mm), generalised from the Cantabrian
coast in 1590, as its codo, and converts every figure of that period into the later units (the
codo real de Castilla, of 32 dedos, was 557.27 mm). From 1750 the unit is the **pie de Burgos**,
half the codo real: **278.635 mm**, about 91.4 per cent of the English foot. A pie is twelve
**pulgadas** (23.219583 mm by the definition of 1801), a pulgada twelve líneas (1.935 mm), which
the book writes as parts of a pulgada. The **vara** is three pies (835.93 mm). The milla is
1,393 m and the legua three millas or 5,000 varas, 4,180 m. The book converts almost every
dimension into pies and pulgadas with metres in brackets, including those first recorded in codos,
in metres (the nineteenth century) or in English feet (the ships built in the English manner, and
those bought from Russia in 1817 and 1818); *Gitano*'s row is an exception the book marks (§13).

**Weight.** The Spanish ton of weight is given as about 1,150 kg, of 20 quintales of four arrobas
of 25 libras; the **libra is 0.4608 kg**, against the English pound's 0.4536 kg, 1.5873 per cent
heavier (36 libras are about 36 lb 9 oz). A gun the book calls a "32pdr" fires a shot of **32
libras**, not 32 English pounds. **Computed:** 20 × 4 × 25 is 2,000 libras, which at the book's
own libra is 921.6 kg, not 1,150 kg. The *Diana*'s plan proves a tonelada of 2,000 libras by its
own carry (`Research-Diana-2026-11.md` §2.3), so the 1,150 kg is recorded and not used.

**Tonnage.** The **tonelada de arqueo** is a measure of capacity, as the English ton burthen is,
of about 1.42 m³; the measuring is the arqueamiento, whose rule the passage does not give. A row's
tons are arqueo; a displacement, rarely recorded, is marked "(disp.)". (The metric system came by
the law of 19 July 1849, applied from 9 December 1852, after the game's years.)

**How a row is measured.** Where it can, the book gives four figures, written **eslora, quilla ×
manga × puntal**:
- **eslora**: the length on the **lowest planked deck**, the keel and both overhangs included (the
  lower deck's run beyond the keel at bow and stern); neither the British gun deck's length nor
  the length overall;
- **quilla**: the straight part of the keel, without its rising ends toward the stem (*roda*) and
  the sternpost (*codaste*);
- **manga**: the beam at its widest, at the middle of the length (the passage does not say whether
  inside or outside the plank);
- **puntal**: the depth of hold, taken down from beneath the lowest continuous deck to the hold's
  bottom; in this period it runs to about half the manga.

The two overhangs beyond the keel (*lanzamiento de proa* and *de popa*) together make the eslora
less the quilla; they, and the *plan* (the flat of the floor), are not given in the book.

**For the game:**
- **The pie, 0.278635 m.** The tree's 0.2786 m (package 39d) agrees to four figures, under a
  centimetre on the three-decker's 220 pies. The game's constants stay Winfield's printed metres,
  as this note's head rules; a figure measured on a Spanish plan is converted at 0.278635 m, as the
  *Diana*'s design already does.
- **The length of a row is the eslora.** §4's "Length overall" is relabelled. The *Diana*'s plan,
  where her 124 pies measure from the post's after face to the stem's fore face on her gun deck
  (`Research-Diana-2026-11.md` §2.2-§2.3), agrees with the definition.
- **The puntal is no draught**, and the tonelada de arqueo no weight: a row's tons are her
  capacity (the *Diana*'s 335 t about 476 m³, computed), never her displacement.
- **One ratio for every calibre: 1.0159** (the libra over the English pound). A Spanish 36 fires
  about 36.57 English pounds and a 30 about 30.48 (computed). The owner's decision 9 stands: a gun
  is filed as her navy named it, and her broadside reads light by about 1.6 per cent. Winfield's
  broadside pairs (§4: 1,212 libras as 1,308 lb, 1.079) do not follow the book's own libra; they
  stay as the book gives them and are not re-derived. **Computed, for the record only:** 1.079 is
  the French livre's ratio to the English pound (0.4895 kg over 0.4536), not the libra's.

## 8. The ranks (Winfield et al. 2023, pp. 52-53)

The Real Armada's commissioned ranks run roughly beside the British, with differences. Those the
package's ships and complements use, with the book's abbreviations and its nearest British word:

| Spanish rank | Abbreviation | British, nearest |
|---|---|---|
| brigadier | Brig | commodore, or a senior captain |
| capitán de navío | CdN | captain |
| capitán de fragata | CdF | commander |
| teniente de navío | TdN | lieutenant |
| teniente de fragata | TdF | sub-lieutenant |
| alférez de navío | AdN | ensign, or midshipman |
| alférez de fragata | AdF | the junior of the same |

Above the brigadier stand three flag ranks, and between the capitán de fragata and the teniente de
navío a capitán de corbeta; none is a post in the package's ships. Most Spanish sources write the
abbreviations without the "d". *Almirante* was a post, not a rank: the second in command of a
fleet, whose commander was the capitán general.

**For the game:** the ranks of the complements of §15 and of the commanders named in the entries
(the polacras' alféreces de fragata and a teniente de navío, §12). The game's posts are spoken in
the game's English ("the captain"), as the *Diana*'s design has it (Dia-D §6.1); the Spanish rank
belongs in a person's brief in the people file, and the ground report's grep for new rank words in
the game's text stands.

## 9. The tartanas (Winfield et al. 2023, pp. 1252-1253), and the owner's reading of the tartane prints

**The entries sent:**
- *San Cayetano*: a chartered French tartana, sailing from Cádiz on 7 August 1741 in company with
  three ships of the navy to spy out the enemy unseen; nothing more known.
- Approval of 27 February 1762 to buy three French-built tartanas, each to her own specification,
  built at "Mantega" as the owner's copy has it (perhaps Martigues, the Provençal tartane port:
  JUDGEMENT), for scouting. Two are confirmed bought: *San Nicolás* and *Santo Espíritu*.
  *Misericordia*, completed in 1762, was perhaps the third; she was sold at Algeciras on 3 June
  1783.
- *Dolores* and *Todos los Santos*: bought in 1778, struck off on 31 August 1779.
- *Las Ánimas*: a tartana armed as a gunboat, sunk in the Bay of Roses in 1795.

No dimensions, tons, guns, men, stations or builders' names are given in these entries. (§1's
seven, "three bought or chartered from French builders and two from a private builder in Spain",
was the chapter's opening as first read; the entries sent do not name the Spanish builder.)

**The owner's reading of the prints** (2026-11-19), in their words, of Monleón's print and the
others they have seen: "it, and other prints of Tartanes I have seen, show one headsail, and a
loose-footed (no lower yard) square topsail." They judged the book's reproduction of the print too
poor to send for reading.

**For the game:**
- **One headsail.** The tartane's design took one jib by judgement (Tar-D decision 11); the
  owner's reading of the prints now bears it out. The images README's "two headsails" is one
  reading of the watercolour (Plan §13.2).
- **The topsail loose-footed, with no lower yard in plain sail.** The tréou's yard is not crossed
  under it in plain sail; the tréou is still carried (Dec 4), its yard sent up with it (Tar-D
  decision 9). With no braced yard below, the lead's ruled reading of A5 (the lateen yard counted
  as the level below: Plan §13.1 item 2) makes her topsail a topsail.
- **Her company and guns stay judgement**, the trader's ten and the coastguard's Chapman eight
  4-pounders and 34 men: the entries give none, and by the owner's word what is not found is filled
  from other research or judgement. The místicos' companies (§11) are the nearest Spanish check.
- ***Las Ánimas*** puts an armed tartana in the Spanish navy in 1795, inside the game's years.

## 10. The coastguard (Winfield et al. 2023, pp. 168-169)

- **Its work**: to pursue contraband, to assist and defend merchant ships, to guard the coasts
  against pirates and smugglers, to survey and chart, and to rescue. Its vessels ranged from
  corvettes, brigs, brig-schooners and schooners down to smaller craft.
- **Whose it was**: a state service set up in the mid-eighteenth century under the Ministry of the
  Treasury, its vessels kept in the navy's arsenals, their commanders and officers often navy
  officers, paid for the while by the Treasury. The vessels were the Treasury's own or hired; many
  were bought merchantmen armed with whatever guns were to hand. Naval officers thought little of
  the service and its people.
- **Its dates in the game's years**: made over to the navy in 1802 on terms the two ministries
  agreed; back to the Treasury in April 1805, when the war with Britain took the
  navy's whole attention. (Its later contracts, 1829 to 1846, fall after the game's years.)

**For the game:** the coastguard tartane's role, `revenue`, the revenue cutter's book (Tar-D §8),
fits the service's work: contraband and the coast. Its survey and rescue are no part of any book
the game reads, so no doctrine of her own is wanted (Tar-D §8's condition is not met). Her
made-out words, "a King's tartane, armed, a guarda-costa", stand (JUDGEMENT): a smuggler feared
her whoever paid her, and from 1802 to April 1805 she was the navy's.

## 11. The místicos, a lateen comparator (Winfield et al. 2023, pp. 1195-1201)

Lateen craft of three masts, the mizen far the least of them; built much as a xebec is but without
oars, smaller and lighter armed. They joined the navy in the last years of the eighteenth century,
were liked for coastguard work as long as the navy sailed, and were all bought, in Spain or abroad.
Monleón's print (the owner's photograph, held privately): one at anchor, her three lateens furled
and her cargo lashed on deck for want of stowage below. The rows with figures, in the book's
metres:

| Místico | Eslora, quilla × manga × puntal (m) | Tons | Men | Guns | When |
|---|---|---|---|---|---|
| *El León* (a British prize, bought) | 16.72, 14.77 × 5.29 × 1.95 | 61 | 72 | 2 × 12, 8 × 4 (and 8 × 3-pdr obuses) | 13.2.1798 |
| *Cerbero* (28 oars) | 14.49 × 4.74 × 1.95 (one length given) | — | 24 | 2 × 4, 10 × 4-pdr obuses | taken by the *Anson* 14.7.1800, retaken |
| *Terrible* | 17.48, 16.07 × 5.15 × 1.72 | 45 | 31/48 | 6 × 8 (and 2 × 3-pdr obuses) | 1809-1815 |
| *Ligero* (místico or cangreja rig) | 17.18, 15.32 × 5.29 × 1.53 | — | 23 | 2 × 8, 4 × 4-pdr obuses | 1809 |
| *Águila* | 16.16, 15.32 × 4.53 × 1.67 | 43⅓ | — | 2 × 8, 6 × 8-pdr carronades | 1809-1815 |
| *Corzo* | 17.14, 14.67 × 5.11 × 3.11 | — | 59 | 2 × 6, 4 carronades (their calibre illegible in the copy) | 1814-1819 |

Other entries give companies only, or little more: 30 to 43 men for one to six guns (1799 to
1820).

**For the game** (computed on the rows; the place of each, JUDGEMENT): a comparator for the
lateen rig, no hull of the package. A místico of 16 to 17½ m is three to three and a half beams
long, the tartane's proportion (the *Humble*, 3.1) on a hull a fifth shorter; her puntal is a
third of her beam or a little more (*Corzo*'s 0.61 apart), shallower than the book's "about half"
for ships. Her companies, 23 to 72 for one to twelve guns, bracket the coastguard tartane's 34 for
eight 4-pounders: that judgement now stands inside the Spanish coastguard's own range. *Cerbero*'s
28 oars on 14½ m are the only oars in the passages sent.

## 12. The polacras (Winfield et al. 2023, pp. 1083-1086), and the owner's reading of Monleón's polacre print

**The eight entries sent:**
- *San Pedro*: ordered sold on 16 May 1783.
- *Dichosa* (her advocation *San Juan Nepomuceno*): bought at Algiers in March 1791 by the
  vice-consul, to bring home eighteen Spanish seamen cast away in two tartanas on the coast of
  Algiers; put up for sale on 1 January 1792; broken up at Cartagena on 17 March 1793.
- *Virgen del Carmen*, 8 guns: 79 ft 6 in, 68 ft 11 in × 15 ft 1 in (22.15, 19.20 × 4.20 m). A
  prize taken at Valencia, repaired at Cartagena from 26 October 1808 and commanded by an alférez
  de fragata, to carry the arsenal's timber and the army's provisions; 84 men (August 1816), 63
  (November 1819); 2 × 6-pdr as taken, 8 × 6-pdr as rearmed, 6 × 8-pdr and 2 × 16-pdr
  carronades (29 August 1809), 8 × 8-pdr (August 1816); given to the posts on 2 February 1819 in
  place of vessels gone with the great expedition to America; broken up at Havana on 13 July 1820.
- *Cupido*: at Jamaica in April 1814 under a teniente de navío.
- *Minerva*, 14 guns, 100 men: at Cumaná on 25 June 1816.
- *Industria*, 12 guns, 80 men: at Cumaná on 25 June 1816.
- *Concepción*, 12/16 guns: her puntal alone, 3.34 m (12 pies by the metres; the pies garbled in
  the owner's copy); 51 men; 16 × 8-pdr (and 4 × 3-pdr obuses) in November 1817, 12 guns
  (8-pounders?) in May 1818, at Valencia under an alférez de fragata.
- ***Angel de la Guarda***, 10 guns: **25.08, 22.15 × 7.52 × 3.34 m** (90 pies, 79 pies 6 pulgadas ×
  27 pies × 12 pies by the metres; the depth's pies garbled in the copy); **71 men**; **2 × 12-pdr
  and 8 × 8-pdr, bronze** (the copy sets "bronze" after the 8s); reported only in 1818.

**Virgen del Carmen's row is recorded as UNKNOWN.** It gives three figures where the book's form
has four, and whether 15 ft 1 in (4.20 m) is her manga or her puntal cannot be told from it. Asked,
the owner said on 2026-11-19, in full: "Quite honestly, I do not know." Either reading is odd
(computed): as a beam, 4.20 m on a 22.15-m eslora is over five beams long; as a depth, it is a
quarter more than *Angel de la Guarda*'s on a hull a ninth shorter. No file reads her row.

**Not in the entries sent:** a polacra *San José* (James's "national polacre-ship" taken at
Fuengirola in 1800); any bergantín-polacra or polacra-goleta; any account of how a polacra's masts
and yards were handled.

**The owner's reading of Monleón's polacre print** (2026-11-19), in full, in their words: "Three
headsails, a large lateen fore on a foreward-raked foremast, aft-raked mainmast with the course
clewed up, topsail and topgallant set, an aft-raked mizzen about the same height as the foremast
with a small loose-footed topsail and lateen sheeted to a short boom atop the transom. The hull has
reasonably aggressive sheer, a clear step in the rail for the raised quarterdeck area, no gunports,
and reasonably short bowsprit."

**For the game:**
- ***Angel de la Guarda* is the one whole row**, and the polacre is sized on her (Pol-D §2). Her
  71 men are the polacre of war's 71 (the *San Josef*'s 49 seamen and 22 soldiers, James), so the
  file's company stands on two sources. Her puntal is 0.44 of her manga (computed), near the book's
  half.
- **The owner's reading**, a check for the eye and never a source of points, settles what the
  designs held by judgement: **three headsails** (Pol-D: two); the main and the mizen **raked
  aft**; the mizen **about the fore's height**; **a small loose-footed topsail over the lateen
  mizen**, which the owner, asked whether she should carry it, answered on 2026-11-19: **"Carry
  it"**, built by the tartane's road (a square topsail over a whole lateen with no lower yard: A5
  and A6); the mizen lateen's sheet to **a short boom over the transom**; **a lively sheer** and a
  step in the rail for **a raised quarterdeck**; **no gunports** in the print (a trader's side; the
  lead's ruling of one hull pierced for every fit stands, Plan §13.1 item 4); and **a reasonably
  short bowsprit**, where §2 above (the lead's words of the print) had a long one.
- Her commanders, where named, were alféreces de fragata (*Virgen del Carmen*, *Concepción*) and a
  teniente de navío (*Cupido*).

## 13. The xebecs after 1750 (Winfield et al. 2023, pp. 1141-1158): her sizes and comparators

The navy built its own xebecs from 1750, when the galleys were done away with (decided 28 November
1748), and went on chartering others. Their builders and designers include Juan Real, a Mallorcan
master-builder without formal training who built many of the navy's xebecs at Mallorca, Cartagena
and Mahón from 1749 to 1788; Jorge Juan; Mateo Mullan, Ignacio Mullan and Eduardo Bryant. Antonio
Barceló (1717-1797), who carried the mail to the Balearics in a xebec of their own, beat off two
Algerian galiots in 1738, was commissioned for it and rose to teniente general, is credited with
bringing the navy to the type. The rows the package uses, in the book's metres:

| Xebec | Guns | Eslora, quilla × manga × puntal (m) | Tons | Men | Guns by calibre | Built, end |
|---|---|---|---|---|---|---|
| *Gitano* (Mallorca; Jorge Juan) | 14 | **27.43 × 6.71 × 3.10, English feet as designed** (90 ft, 22 ft × 10 ft 2 in) | — | — | 14 × 4 (and 20 × 2-pdr pedreros) | 1753; struck off 1760 |
| *Catalán* (i) (Palma) | 22 | 25.29, 22.40 × 6.32 × 2.67 | 134 | — | — | 1752-1753 |
| *Gavilán* (Cartagena; bought) | 20 | 33.32, 28.61 × 7.59 × 2.69 | 232 | — | 16 × 6, 4 × 4 | 1749; to the navy 1753 |
| *Garzota* (bought) | 22 | 38.87, 34.27 × 7.85 × 2.65 | 267 | — | 18 × 6, 4 × 4 | 1753-1762 |
| *Caballo Blanco* (an Algerian prize) | 14/24 | 27.58, 20.69 × 6.90 × 2.83 | 155 | — | 2 × 8, 12 × 4 | taken 1768; exchanged 1772 |
| *Nuestra Señora de África* (i) (Cartagena, the coastal mail) | 12 | 32.47, 28.44 × 7.89 × 3.16 | — | — | 12 × 6 | 1768-1774 |
| ***Nuestra Señora de África* (ii)** (Ceuta; Juan Real, **all lateen sails**) | 18 | **23.85, 19.02 × 6.34 × 2.41** | 102 | **127** | 14 × 4 (and 4 × 2-pdr pedreros) | 1775; fate not known |
| *San Blas* class (Cartagena) | 14/24 | 30.09 × 7.15 × 2.14 | — | — | 14 × 6 by the Regulation of 1793 | 1779-1804 |
| *Muralla* | 8 | 18.11, 15.88 × 6.13 × 1.67 | 57 | 55 | 2 × 12, 4 × 6 | from 1795 |
| *Diligente* | 12 | 21.73, 17.28 × 6.69 × 3.06 | 125 | 69 | 12 × 6 | 1808-1823 |
| *Aventurero* (Cartagena; Jorge Juan) | 30 | 36.87, 31.65 × 8.31 × 3.60 | 405 | — | 20 × 8, 2 × 6, 8 × 4 | 1753; a chambequín 1765; wrecked 1767 |
| ***Gamo*** (Mallorca) | 30/32 | **38.92, 32.00 × 9.38 × 3.53** | **435** | — | **24 × 8, 6 × 3** (and 12 pedreros) | 1770; taken by the brig *Speedy* 6.5.1801 |
| *Caimán* (Havana; Ignacio Mullan) | 30 | 33.99, 29.40 × 8.64 × 3.91 | 354 | — | 20 × 8, 10 × 4 by the Regulation of 1752; 22 × 8 in 1784 | 1770; rigged as a chambequín; broken up 1790 |
| *Mallorquín* class (Mahón; **lateen-rigged**) | 26/28 | 36.08, 33.16 × 10.03 × 3.90 | 418 | 251 | 20 × 8, 6 × 4 | 1786; to 1799 or 1800 |

Other facts of the entries:
- ***Gitano*'s figures are marked British dimensions as designed**, and the book's metres for them
  are English feet's (90 × 0.3048 = 27.43: computed): the one row of the passages not in pies.
  **Her draught is reproduced: Museo Naval, Madrid, PB_album_06_05.** The *Cazador* class (four
  xebecs launched at Cartagena in 1750) is shown on plate 17 of the Marqués de la Victoria's album
  (its entry names Juan Real as designer, the caption Jorge Juan); *Aventurero*'s draught is
  reproduced too (its number cut off in the copy), and models of *Cazador* (MNM 0367) and
  *Aventurero* (MNM 2653).
- **The chambequines** (square-rigged xebec hulls): *Aventurero*, converted in 1765 for Buenos
  Aires; *Andaluz* (ii), converted in 1778 for Buenos Aires; *Caimán*, built at Havana for Cartagena
  de Indias's coastguard and rigged as one; Barceló's own *San Antonio*, rigged as one
  and taken into the navy in 1772 against the Barbary corsairs; and the *Murciano* class (1779),
  ship-rigged after *Atrevido*, enlarged. No masting figure is given.
- Four 14-gun xebecs chartered at Mallorca in 1775, each of 100 to 150 men, were found too small
  for their ten 3-pounders and four 2-pounders and rejected; *Tigre* was a lateen-rigged xebec of
  the coastguard in 1819 (53 men; 2 × 12-pdr, 4 × 10-pdr obuses).
- **Not given:** her oars (*remos*), seamen and soldiers apart, how she was steered, lay to or went
  about. *Vives* (1806) is not among the entries sent; whether *África* (ii) is James's *África*
  taken in 1799 her entry does not say.

**For the game** (computed on the rows; their use, JUDGEMENT):
- **The small class.** The rows of 14 to 22 guns built from 1749 to 1779 run from 23.85 to 38.87 m
  of eslora and 6.32 to 7.89 m of beam, 3.8 to 5.0 beams long. *Minorca* (29.49 by 9.30 m, English
  feet), the xebec's hull by the owner's decision 5, is 3.2: broader for her length than any of
  them, and as broad as the *Gamo* of 30 guns. Only the later small rows, *Diligente* (12 guns,
  3.25) and *Muralla* (8 guns, 2.95), are as beamy. Xeb-D §2.2 takes them as her comparators.
- ***Gitano*'s draught** is a Spanish plan of the small class's 14: the plan Xeb-D §3.1 waits for
  "from Winfield's reproductions", to be sought where the Museo Naval's albums are served.
- ***África* (ii)** is the lateen small class itself: all lateen, 18 guns (14 mounted), 127 men,
  23.85 m.
- **The 30's length is known:** the *Gamo*'s eslora is 38.92 m (Dec 5, X2).
- **The Regulation of 5 August 1752** for a xebec of 30 (20 × 8, 10 × 4) is in *Caimán*'s entry,
  beside §3's table.

## 14. The corvettes' chapter (Winfield et al. 2023, pp. 904-906)

- **What they were:** small frigates (*fragatillas*) of under twenty guns and corvettes
  (*corbetas*), in effect frigates in small, for patrol, escort and dispatches on the sea roads to
  and from Spain's colonies, against smugglers and pirates in peace and privateers in war; after the
  wars, many against the insurgents' warships in America. On distant stations they cruised singly,
  or a few together with brigs and brig-schooners.
- **Their guns:** 6-pounders, even 4-pounders, on completion, with short guns of the carronade kind;
  many rearmed later with 8-pounders. Merchantmen and prizes were bought and armed in war as a
  cheap expedient, with light guns, carronades and gunnades, their holds giving room for men and
  stores; many ended as urcas, depot ships or hulks, or were sold back to their owners.
- **The words:** the regulations of 1739, 1750, 1752 and 1766 name no corvette; the word is used
  loosely from around 1760, and the first regulation to name corvettes is that of 1 January
  1788 on garrisons and crews (§15). *Fragatilla* was the informal word before 1760 for the small
  single-decked frigates later called corbetas.
- **The book's line:** twenty guns divides its frigates (chapter 6) from its fragatillas and
  corbetas (chapter 7), the main armament the yardstick (6-pounder ships here, 8-pounder there); the
  line blurs after 1800, when 8-pounder ships were called corbetas, and after the wars corvettes
  were as big and as heavily armed as the frigates of the eighteenth century had been.

**For the game:** the *Diana*, a Danish frigate of twenty carronades, stands in this chapter (p.
930, §17): a corvette in Spanish service by the book's line. How a corvette of twenty was rigged
after 1800 is not said (D2's rig not found); her establishment by kind is the 1788 regulation's
(§15).

## 15. The complements of 1788 and 1803 (Winfield et al. 2023, p. 1446 and the two pages following; the table of the Regulation of 16 October 1803, its page not on the owner's copy)

**What the columns count.** Each row gives the commissioned officers by rank, then by number the
**major officers** (pursers, chaplains, surgeons, pilots and junior pilots), the **sea officers**
(boatswains, guardians, caulkers, carpenters, cooks, divers, armourers, lamp men, sailing masters
and quartermasters), **infantry**, **infantry-artillery** (the artillery's infantry corps),
**artillery**, **seamen**, **landsmen** and **boys**. **The book's "Total" counts only those last
seven columns: it leaves out the commissioned and the major officers.** The complements of 1788
were peace establishments; **at war a ship of the line or a frigate took one more man for each gun
of her main batteries, half of them infantry and half landsmen**, and more surgeons besides.

The rows the package uses ("All" is the book's Total with the commissioned and major officers
added: computed):

| Rate (regulation) | Commissioned | Major | Sea | Infantry | Inf.-art. | Artillery | Seamen | Landsmen | Boys | Total (book) | All |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Navío of 112 (1788) | 19: 1 Brig, 1 CdN, 1 CdF, 4 TdN, 4 TdF, 4 AdN, 4 AdF | 10 | 23 | 168 | 57 | 130 | 200 | 230 | 40 | 848 | 877 |
| Navío of 94 (1788) | 15: 1 Brig, 1 CdN, 1 CdF, 3 TdN, 3 TdF, 3 AdN, 3 AdF | 9 | 23 | 168 | 57 | 120 | 200 | 200 | 34 | 802 | 826 |
| Navío of 112 (1803) | 19, as 1788's | 14 | 37 | 200 | 75 | 190 | 240 | 200 | 40 | 982 | 1,015 |
| Corvette of 18 to 22 (1788) | 5: 1 TdN, 1 TdF, 2 AdN, 1 AdF | 5 | 11 | 40 | 10 | 21 | 20 | 20 | 6 | 128 | 138 |
| Corvette of 14 to 16 (1788) | 4: 1 TdN, 1 TdF, 1 AdN, 1 AdF | 5 | 11 | 30 | 8 | 21 | 18 | 20 | 4 | 112 | 121 |
| Xebec of 30 to 32 (1788) | 8: 1 CdF, 1 TdN, 2 TdF, 2 AdN, 2 AdF | 5 | 13 | 60 | 15 | 42 | 100 | 42 | 8 | 280 | 293 |
| Xebec of 18 (1788) | 6: 1 TdN, 1 TdF, 2 AdN, 2 AdF | 5 | 13 | 45 | 10 | 31 | 35 | 40 | 4 | 188 | 199 |
| Xebec with lateen sails, 16 to 20 (1788) | 4: 1 TdF, 2 AdN, 1 AdF | 4 | 10 | 20 | 6 | 24 | 30 | 40 | 4 | 134 | 142 |

- **The xebec of 18's Total does not add:** its seven columns sum to 178, and the book prints 188
  (computed); recorded, not resolved (189 all, by the columns).
- 1788 also gives xebecs of 34 (Total 299) and of 26 to 28 (251); its xebecs fall in two lists,
  "xebecs" and "xebecs with fore-and-aft (lateen) sails", and the book does not say what the first
  list's rig was.
- **The 1803 regulation** covers navíos of 130 down to 54, frigates of 42, 40 and 34, and urcas: it
  has **no corvette and no xebec row**, and a 96 where 1788 has a 94. No war increase is printed with
  it in the owner's copy.
- **The war increase, for a 112** (computed, its reading JUDGEMENT): if her "main batteries" are her
  lower deck's 30 guns, 907 men (15 more infantry, 15 more landsmen); if they are her three gun
  decks' 94, the book's own word for a gun deck being a "battery" (§16), 971 (47 and 47).

**For the game:** the three-decker's company by kind, the soldiers her infantry and
infantry-artillery (Con-D §6.1: the 1788 regulation for her 1797 fit, 1803's for her 1809 fit);
the corvette's establishment by kind beside the *Diana*'s own 167 (Dia-D §6.1); the xebecs' as
comparators for the xebec's 113 (Xeb-D §8.1).

## 16. The ordinance of 1803: a three-decker's guns by deck, beside her own record (Winfield et al. 2023, the table of the ordinance of 1803, its page not on the owner's copy; pp. 406-410 for her own)

**The ordinance's three-decker of 112:** first battery 30 × 36-pdr; second battery 32 × 24-pdr;
third battery 32 × 12-pdr; quarterdeck 4 × 8-pdr and 8 × 48-pdr obuses; forecastle 4 × 8-pdr and
2 × 48-pdr obuses; poop 6 × 24-pdr obuses: **118 pieces**, the poop's six obuses outside the
nominal count. Its note: ***Concepción* carried 18-pounders in her third battery.** Its rules,
in short: as heavy an armament as each hull and her sailing would bear, in the fewest calibres,
the calibres free to differ between ships of one rate; the upper works' guns left to inspection;
corvettes, brigs and smaller craft still under the ordinance of 9 October 1793.

| Deck | The ordinance of 1803, a 112 | Her own, as altered at Ferrol in 1803 (pp. 406-410; §4) |
|---|---|---|
| Lower (first battery) | 30 × 36 | 30 × 36 |
| Middle (second battery) | 32 × 24 | 32 × 24 |
| Upper (third battery) | 32 × 12 | **32 × 18**, as the ordinance's own note says |
| Quarterdeck | 4 × 8, **8** × 48-pdr obús | 4 × 8, **6** × 48-pdr obús |
| Forecastle | 4 × 8, 2 × 48-pdr obús | 4 × 8, 2 × 48-pdr obús |
| Poop | 6 × 24-pdr obús | 6 × 24-pdr obús |
| Pieces | **118** (112 nominal) | **116** |

**For the game:** her 1809 fit stays her own record, 116 pieces (Con-D §5.1); the ordinance's 118
is noted, two more 48-pounder obuses on the quarterdeck. By the ordinance's count she was nominally
110 (computed: the poop's six outside it). The guns' weights by calibre are not in the passages:
they are to come from other research (the period's Spanish artillery treatises, for example) or
judgement.

## 17. The *Diana*'s whole entry (Winfield et al. 2023, p. 930)

The owner sent the entry whole ("this is the entirety of it", their words). **It holds only what
§5 already has:** her three dimensions (124 ft × 32 ft 6 in × 16 ft; 34.55 × 9.06 × 4.46 m), 335 t,
167 men, her three fits by date (twenty 24-pdr carronades as captured; twenty 30-pdr carronades as
first rearmed; on 31 October 1817 twelve 12-pdr, eight 30-pdr carronades and four 3-pdr obuses),
a Danish frigate built in 1804, seized at Cartagena when war was declared, and last heard of in
1832.
There is no service line, no commander, no voyage of 1810, no source for "as captured", no rule for
the 335 t, and nothing of her rig, masting or steering (D1's asks, not found). By §7, her 335 t is
toneladas de arqueo, a capacity (about 476 m³, computed), and not her displacement.
