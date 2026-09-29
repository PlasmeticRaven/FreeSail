# Design note: candidates for the cutter and the brig

From the owner's list of 2026-09-29, drawn mostly from the Vanguard Models kits, with the
condition that each candidate be common enough to have information from several sources.
The lead's assessment from memory, to be verified against the sources named before a
file is generated (`tools/gen_ships.py`); every figure below is *unverified* until then
and says so. The two vessels are the first entries of the vessel library and the test of
pillar 2 (spec M5 §23, §25); the rest of the list is milestone 8's.

## The size hierarchy the catalogue needs

The two reference ships: the topsail schooner at 224 tons burthen (Chapelle 1930, 94 ft
7 in on deck), the frigate at 933 tons (143 ft on the gun deck). The owner's wish is a
hierarchy of size to build on, so the cutter and the brig should fall below and between
those, not beside them.

## The brig-sloop candidates

| Candidate | What she was (unverified) | Sources | Fit |
|---|---|---|---|
| **HMS Harpy, 1796** | A Diligence-class brig-sloop, launched 1796 and sold 1817, the longest-lived and most travelled of her class (Copenhagen 1801, Java 1811, privateers taken, a clasp to the Naval General Service Medal); from the kit's manual (the owner's notes, 2026-09-29): 316 tons burthen, 95 ft on the gun deck and 75 ft 1 5/8 in on the keel, beam 28 ft 1 1/2 in, depth of hold 12 ft 0 1/2 in, complement 121, sixteen 32-pounder carronades and two 6-pounder chase guns, sail plan brig. The kit's model (the owner's picture): three square yards on each mast, course, topsail and topgallant, a gaff and boom on the main for the spanker, the tops and the long jib-boom of a ship-rigged vessel in small | Winfield, *British Warships in the Age of Sail 1793–1817* (the class's dimensions); the Admiralty draught at Royal Museums Greenwich; the Vanguard kit's plans derive from it | **The brig.** In period exactly, the working brig-sloop of 1805, sized between the schooner and the frigate, with the full head-sail and staysail complement the owner asked for as the type carried it. First choice. |
| **HMS Speedy, 1782** and **HMS Flirt, 1782** | Sisters of one design (Thomas King, Dover): 14-gun brig-sloops of about 208 tons, 78 ft on deck, fourteen 4-pounders; Speedy the most famous small brig of the age under Cochrane in 1800 to 1801, captured 1801 | Winfield; Cochrane's *Autobiography of a Seaman*; the RMG draughts; the Vanguard kits of both | The older, smaller brig, at the schooner's size rather than between; a fine second brig for milestone 8 and a scenario of her own (Speedy against *El Gamo*). Not the base, because she does not fill the gap in the hierarchy; her fate in 1801 is no bar, since the game's era is 1792 to 1825 and a sister or a survivor of the design may serve in it (the owner's rule: not overly stickling where fun is served). |
| **HMS Adder, 1797** | A gun-brig (Conquest or Acute class), about 160 tons, some 75 ft, twelve 18-pounder carronades, flat-floored, some of the class with Schank's sliding keels; Channel and Downs service | Winfield; the RMG draughts; the Vanguard kit | Not a sailing brig so much as a floating battery that could sail; at a cutter's size. Milestone 8, as the gun-brig type for the Channel's coast war (M7 wants her). |

## The cutter candidates

| Candidate | What she was (unverified) | Sources | Fit |
|---|---|---|---|
| **HMS Alert, 1777** | A 12-gun naval cutter of about 205 tons, later rigged as a sloop; captured by the French in 1778 | Peter Goodwin, *The Naval Cutter Alert, 1777* (Anatomy of the Ship, Conway 1991), with the lines, the spar dimensions and the sail plan complete; the RMG draughts; the Vanguard kit | **The armed cutter**, and the best-documented small vessel of the age because of the Anatomy volume: every spar and sail is in print. At 200 tons she is a warship's cutter, the schooner's size, not a pilot's boat. |
| **HM Armed Cutter Sherbourne, 1763** | A 6-gun cutter built at Woolwich to Slade's design under Joseph Harris, launched 3 December 1763 for £1,581 8s 9d; her whole career in the Channel against smugglers for the Board of Customs, from Plymouth and the Dorset and Devon coast, under Lieutenant John Cartwright (1763 to 1766) and five more; laid up 1779, used in Tracey's attempt on the *Royal George* in 1783, sold at Portsmouth 1 July 1784; from the kit's manual (the owner's notes, 2026-09-29): 85 tons burthen, 54 ft 6 in, beam 19 ft, complement 30, six 3-pounders and eight swivels. The kit's model (the owner's picture): one mast with a long gaff and boom for the mainsail, three square yards above it (a course yard, a topsail yard and a topgallant yard, the two upper ones on the topmast), a very long running bowsprit, the stem plumb and the hull deep and beamy, the customs cutter's shape | The RMG draught (Slade's design); the Vanguard kit and its manual | **The pilot's cutter.** A pilot cutter or a revenue cutter of the Channel was of this size, forty to eighty tons; she is the bottom of the hierarchy and the one the ports need first (spec §23). Older than the period, but the type changed little. |
| **HM Trial Cutter, 1790** | An experimental cutter with Schank's three sliding keels, about 60 ft | The RMG draughts; Schank's own papers; the Vanguard kit | A curiosity of the "cool obscure" kind, and the sliding keels are a hull feature the engine does not model. Milestone 8 or later, if at all. |
| **HMS Bramble, 1822** | A 10-gun cutter of the 1820s, about 160 tons | The RMG draught; the Vanguard kit | Inside the game's era (1792 to 1825, the owner's correction of 2026-09-29; the lead had written 1805 too narrowly), at its late end: the cutter of the 1820s is fuller and taller-rigged than the century's turn, which makes her a good contrast to Alert for milestone 8, not a reason to leave her out. |

## Recommendation

Two files for milestone 5: **Sherbourne** as the cutter (the pilot's, package 35), and
**Harpy** as the brig (package 36), with the brig-sloop and the merchant brig as her two
descriptions at far detail. **Alert** as the third, an armed cutter at the schooner's size,
when the vessel library opens in milestone 8, since the Anatomy volume makes her the
cheapest well-sourced vessel there is and she tests the generator's cutter rules at a
second size; Speedy and Adder after her, for their scenarios. The hierarchy that results:
Sherbourne 85 tons, Alert and Speedy about 200, the schooner 224, Harpy 316, the frigate
933.

**The era.** The game's era is 1792 to 1825 (the owner, 2026-09-29), not 1805 alone; a vessel built early and serving in the middle of it, or one that well could have, is fair. The design proposal's §9 baseline reads "roughly 1793–1815, blended" and the consent brief "around 1793 to 1815"; both were narrower than the owner's statement and were amended the same day (decision 27): 1792 to 1825, a focus and not a wall, the early end admitting vessels built before that served in the window. The owner's first named exception beyond it is the brigantine *Dolphin* of 1836, for the vessel library when it comes; "never a hard rule on what we can do eventually".

**The owner's choice (2026-09-29):** Sherbourne and Harpy as the initial two.

Two cautions. The Vanguard kits are built from the Admiralty draughts and are a good
guide to what exists, but the game's files cite the draughts and the printed dimensions
(Winfield, Goodwin, Steel's tables for the spars), not the kits. And every number above
is from the lead's memory and must be read again from a source before it becomes a
figure in a ship file; the generator's comments carry the citation, as the frigate's and
the schooner's do.

## The owner's wishlist for later (noted 2026-09-29, not for rushing)

Named so they are on record for the vessel library and after; none belongs to a planned
milestone yet, and every figure is the lead's memory, unverified.

| Vessel | What she was (unverified) | Why she is interesting | Sources |
|---|---|---|---|
| **HMS Indefatigable, 1794** (the owner's pick: https://vanguardmodels.co.uk/products/hms-indefatigable-1794) | A 64-gun ship of 1784 cut down (razeed) in 1794 to a heavy frigate of 44 guns, 24-pounders on the gun deck; from the kit's manual (the owner's notes, 2026-09-29): 1,384 3/94 tons burthen, 160 ft 1 1/4 in on the gun deck and 131 ft 10 3/4 in on the keel, beam 44 ft 5 in, depth of hold 19 ft as a 64 and 13 ft 3 in as a frigate, complement 310 as a frigate; Pellew's ship, famous for the *Droits de l'Homme* action of January 1797 in the Bay of Biscay (the action unverified here) | The top of the size hierarchy above the 36: a razee's heavy scantlings and tall rig on a frigate's role, and the one ship the Western Approaches scenario most wants as a station ship off Ushant | Winfield; the RMG draughts (as built and as razeed); Pellew's biographies; the Vanguard kit |
| **HMS Sphinx, 1775** | A 20-gun sixth-rate (post ship) of the Sphinx class, about 430 tons and 108 ft, nine-pounders; a ship-rigged three-master smaller than a frigate | Fills the gap between the brig-sloop and the 36 with a full ship rig at a small size, and is the kind of vessel a young post-captain got first; in service into the period | Winfield; the RMG draughts; the Vanguard kit |
| **The royal yacht *Duchess of Kingston*, 1778** (one vessel, the owner's pick: https://vanguardmodels.co.uk/products/royal-yacht-duchess-of-kingston-1778) | Built by J. M. Hillhouse of Bristol in the late 1770s for the Duchess of Kingston; from the original plans (the kit's page, quoted by the owner 2026-09-29): keel 68 ft, range of deck 81 ft, moulded breadth 24 ft, depth of hold under beams 10 ft, 206 tons burthen; "this type of vessel seemed to retain many older, more classical features, compared to those built for the Royal Navy, making the yacht look more a product of the late 17th/early 18th century"; ship-rigged with a **lateen mizzen** on its long yard in the older manner rather than a gaff spanker, and finely decorated; later in naval service (unverified) | The first civilian ship: finer details, a better crew and a fuller sail complement than a working vessel, as the owner asks; the lateen mizzen exercises the engine's `lateen_yard` class on a ship rig before the tartane's, and the yacht's decoration is a test of what the viewer can carry; a passage with a royal or an ambassador aboard is a scenario for the director | The RMG draught and the Vanguard kit (its plans from the draught); the duchess's Baltic and Russian voyages for the story |
| **HM Brigantine Dolphin, 1836** | A brigantine of the anti-slavery squadron, about 320 tons, two masts, the fore square-rigged and the main fore-and-aft (the term's later sense), fast, built for chasing slavers | Beyond the window (decision 27's first named exception): the brigantine rig itself, a fore-and-aft main with a square fore, which the engine's classes already cover; a West Africa scenario far off | The RMG draughts; the Vanguard kit |

The hierarchy with these in it: Sherbourne 85 tons; Alert, Speedy, the yacht and the
schooner about 200 to 230; Harpy 316 and Dolphin about 320; Sphinx about 430; the
frigate 933; Indefatigable about 1,380. Each new size is a new test of the generator's
rules, which is what the library is for.
