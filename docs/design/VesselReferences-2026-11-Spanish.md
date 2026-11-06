# Design note: the Spanish navy's sources for package 90 (November 2026)

The owner's shelf holds Rif Winfield (with John Tredrea, Enrique García-Torralba Pérez and
Manuel Blasco Felip), *Spanish Warships in the Age of Sail, 1700–1860*, Seaforth, 2023, a
modern work under copyright: it is not in the repository and is never copied into it. The
owner reads the passages package 90 needs and sends them to the lead; the facts in them are
set down here, in the lead's words, cited by the page of the owner's edition, for the ships
session's design documents (Build-Ships.md §5.0's ladder of evidence, where a particular
read from Winfield is a rung-B figure, and his reproductions of plans point at the rung-A
originals). The ships session asks the lead for further passages by title and class, and
the owner sources them if they exist (the owner's word, 2026-11-06).

**Units.** Winfield's dimensions for Spanish ships are in **pies de Burgos** (0.2786 m), not
English feet, as his own metres show: the *Purísima Concepción*'s 213 ft 9 in is 59.55 m
only at that foot (213.75 × 0.2786 = 59.55), and the *Diana*'s 124 ft is 34.55 m the same
way. The game's constants are metres from his metres; an English-foot figure from a Spanish
row is wrong by eight and a half per cent. The game already holds the pie de Burgos for
Tofiño's tides (`docs/dev/TuningNotes.md`, package 39d: 0.2786 m, the vara castellana
0.8359 m) and the braza of two varas. Weights of broadside are given by Winfield in libras
with his own pounds beside them (1,212 libras as 1,308 lb); take his pairs as he gives them
and do not re-derive the ratio.

## 1. The tartane (Winfield pp. 1249 to 1252)

Small coasting craft, almost all in trade, now and then taken up as coastguard vessels for
reconnaissance. The rig fore-and-aft: a large mainmast and a very small mizen. Monleón's
print of one at rest (p. 1249) shows the main spar big for the hull, a square topsail on the
mainmast "for stability", and the diminutive mizen that was the custom. The type was common
across the Mediterranean under other flags but found little favour in Spain: seven tartanas
are known in the Spanish navy's service, three bought or chartered from French builders and
two from a private builder in Spain. For the game: the Spanish navy's tartana is a role
(coastguard, reconnaissance) on a trader's hull, and the trader's and fisherman's fits come
first; a French-built hull is in keeping with the record. The square topsail over the lateen
is a fit to be read against the Roux-school watercolour (`docs/references/images/`), which
shows none.

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
the design document must say it before the file.

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
lateen experience could work them. Few xebecs before 1750; the type's expansion followed the
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
| Length overall, keel | 213 ft 9 in, 190 ft 10 in (59.55 m, 53.12 m) |
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
scenarios (116 guns, the 1803 alteration) and the 1797 fit (112) for St Vincent.

## 5. The *Diana*, corvette of 20 (Winfield p. 930)

The Danish frigate *Diana*, built 1804, taken at Cartagena with the declaration of war,
last mentioned 1832. 124 ft × 32 ft 6 in × 16 ft (34.55 × 9.06 × 4.46 m), 335 t, 167 men.
Guns: 20 × 24-pdr carronades as captured; 20 × 30-pdr carronades as first rearmed (the fit
of her plan of 1809 to 1810, "del porte de 20 carronadas de á 30"); on 31 October 1817, 12 ×
12-pdr, 8 × 30-pdr carronades, 4 × 3-pdr obuses. Her draught is held:
`docs/references/images/corvette-diana-1809-plano-bvmdefensa.jpg` (CC BY 4.0, Archivo
Histórico de la Armada Juan Sebastián de Elcano / Biblioteca Virtual de Defensa, record
1037832), the rung-A source for her lines, with a table of her particulars on the sheet in
the navy's units to be read against Winfield's row.

## 6. Pictures cited and not held

The three the owner sent on 2026-11-06 as photographed from Winfield's pages: Rafael Monleón
y Torres's print of a polacre under sail (p. 1084) and his print of a xebec under oars and
foresail (p. 1135), and the Greenwich draught of *San José* (J1945, p. 410). Monleón (1843 to
1900) is public domain by age, and the originals are the Museo Naval's; the book's
photographs of them are not copied into the tree. When a direct source of either print is
found (the Museo Naval's catalogue or a Commons file with its provenance) it goes into
`docs/references/images/` with the others; the Greenwich draught is cited by its object
number as Gwyn's bilander is.
