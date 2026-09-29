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
| **HMS Harpy, 1796** | An 18-gun brig-sloop of the Diligence class (Henslow), about 330 to 340 tons, some 96 ft on the gun deck, 30 ft beam, sixteen 32-pounder carronades and two long sixes; in service through the war | Winfield, *British Warships in the Age of Sail 1793–1817* (the class's dimensions); the Admiralty draught at Royal Museums Greenwich; the Vanguard kit's plans derive from it | **The brig.** In period exactly, the working brig-sloop of 1805, sized between the schooner and the frigate, with the full head-sail and staysail complement the owner asked for as the type carried it. First choice. |
| **HMS Speedy, 1782** and **HMS Flirt, 1782** | Sisters of one design (Thomas King, Dover): 14-gun brig-sloops of about 208 tons, 78 ft on deck, fourteen 4-pounders; Speedy the most famous small brig of the age under Cochrane in 1800 to 1801, captured 1801 | Winfield; Cochrane's *Autobiography of a Seaman*; the RMG draughts; the Vanguard kits of both | The older, smaller brig, at the schooner's size rather than between; a fine second brig for milestone 8 and a scenario of her own (Speedy against *El Gamo*). Not the base, because she does not fill the gap in the hierarchy; her fate in 1801 is no bar, since the game's era is 1792 to 1825 and a sister or a survivor of the design may serve in it (the owner's rule: not overly stickling where fun is served). |
| **HMS Adder, 1797** | A gun-brig (Conquest or Acute class), about 160 tons, some 75 ft, twelve 18-pounder carronades, flat-floored, some of the class with Schank's sliding keels; Channel and Downs service | Winfield; the RMG draughts; the Vanguard kit | Not a sailing brig so much as a floating battery that could sail; at a cutter's size. Milestone 8, as the gun-brig type for the Channel's coast war (M7 wants her). |

## The cutter candidates

| Candidate | What she was (unverified) | Sources | Fit |
|---|---|---|---|
| **HMS Alert, 1777** | A 12-gun naval cutter of about 205 tons, later rigged as a sloop; captured by the French in 1778 | Peter Goodwin, *The Naval Cutter Alert, 1777* (Anatomy of the Ship, Conway 1991), with the lines, the spar dimensions and the sail plan complete; the RMG draughts; the Vanguard kit | **The armed cutter**, and the best-documented small vessel of the age because of the Anatomy volume: every spar and sail is in print. At 200 tons she is a warship's cutter, the schooner's size, not a pilot's boat. |
| **HM Armed Cutter Sherbourne, 1763** | A small 8-gun cutter of about 78 tons, some 55 ft, of the revenue-cutter build | The RMG draught (the well-known Sherbourne plan); the Vanguard kit | **The pilot's cutter.** A pilot cutter or a revenue cutter of the Channel was of this size, forty to eighty tons; she is the bottom of the hierarchy and the one the ports need first (spec §23). Older than the period, but the type changed little. |
| **HM Trial Cutter, 1790** | An experimental cutter with Schank's three sliding keels, about 60 ft | The RMG draughts; Schank's own papers; the Vanguard kit | A curiosity of the "cool obscure" kind, and the sliding keels are a hull feature the engine does not model. Milestone 8 or later, if at all. |
| **HMS Bramble, 1822** | A 10-gun cutter of the 1820s, about 160 tons | The RMG draught; the Vanguard kit | Inside the game's era (1792 to 1825, the owner's correction of 2026-09-29; the lead had written 1805 too narrowly), at its late end: the cutter of the 1820s is fuller and taller-rigged than the century's turn, which makes her a good contrast to Alert for milestone 8, not a reason to leave her out. |

## Recommendation

Two files for milestone 5: **Sherbourne** as the cutter (the pilot's, package 35), and
**Harpy** as the brig (package 36), with the brig-sloop and the merchant brig as her two
descriptions at far detail. **Alert** as the third, an armed cutter at the schooner's size,
when the vessel library opens in milestone 8, since the Anatomy volume makes her the
cheapest well-sourced vessel there is and she tests the generator's cutter rules at a
second size; Speedy and Adder after her, for their scenarios. The hierarchy that results:
Sherbourne about 80 tons, Alert and Speedy about 200, the schooner 224, Harpy about 340,
the frigate 933.

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
| **HMS Indefatigable, 1794** | A 64-gun ship of 1784 cut down (razeed) in 1794 to a heavy frigate of 44 guns, 24-pounders on the gun deck, about 1,380 tons and 160 ft; Pellew's ship, famous for the *Droits de l'Homme* action of January 1797 in the Bay of Biscay | The top of the size hierarchy above the 36: a razee's heavy scantlings and tall rig on a frigate's role, and the one ship the Western Approaches scenario most wants as a station ship off Ushant | Winfield; the RMG draughts (as built and as razeed); Pellew's biographies; the Vanguard kit |
| **HMS Sphinx, 1775** | A 20-gun sixth-rate (post ship) of the Sphinx class, about 430 tons and 108 ft, nine-pounders; a ship-rigged three-master smaller than a frigate | Fills the gap between the brig-sloop and the 36 with a full ship rig at a small size, and is the kind of vessel a young post-captain got first; in service into the period | Winfield; the RMG draughts; the Vanguard kit |
| **The Royal Yacht** (which one to be settled; the Vanguard kit is *Royal Caroline*, 1749, a ship-rigged yacht of about 230 tons) | The royal yachts of the century were ship-rigged, lavishly finished, fast for their size; *Royal Caroline* is the best documented, with a full set of draughts and a famous model | A vessel with no guns to speak of and every gilded thing the "cool obscure" pillar enjoys; a passage with a royal or an ambassador aboard is a scenario for the director | The RMG draughts and model; the Vanguard kit; Winfield for the later yachts |
| **Duchess of Kingston, 1778** | A ship-rigged yacht built for the Duchess of Kingston, about 200 tons, later in naval service | A private yacht of the 1770s, and a story: the duchess's voyage to the Baltic and Russia | The RMG draught; the Vanguard kit |
| **HM Brigantine Dolphin, 1836** | A brigantine of the anti-slavery squadron, about 320 tons, three masts? (no: two, the fore square-rigged, the main fore-and-aft; the term's later sense), fast, built for chasing slavers | Beyond the window (decision 27's first named exception): the brigantine rig itself, a fore-and-aft main with a square fore, which the engine's classes already cover; a West Africa scenario far off | The RMG draughts; the Vanguard kit |

The hierarchy with these in it: Sherbourne about 80 tons; Alert, Speedy, the yachts and
the schooner about 200 to 230; Harpy and Dolphin about 320 to 340; Sphinx about 430; the
frigate 933; Indefatigable about 1,380. Each new size is a new test of the generator's
rules, which is what the library is for.
