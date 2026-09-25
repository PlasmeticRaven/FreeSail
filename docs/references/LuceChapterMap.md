# Luce chapter map

Which chapters of Luce's *Seamanship* feed which parts of FreeSail. Chapter numbers follow the **1866 edition** (its table of contents lists sub-topics); the 1884 chapter with the same subject is given where the numbering differs. Milestones refer to the roadmap in `docs/DesignProposal.md` §11.

Game system key:
**Parts** = part glossary and ship data files (§3.3). **Evolutions** = the level 1 catalogue (§4.4). **Physics** = tuning constants and "known truths" tests (§3.4). **Crew** = watches, stations, task timings (§3.5). **World** = navigation, weather, ports (§5). **Damage** = damage, jury rig, parting rigging (§3.4, §5.3). **Skip** = out of scope or out of period.

| Ch. (1866) | Subject | Sub-topics of interest | Feeds | Milestone |
|---|---|---|---|---|
| I | The compass and lead | Compass, dumb compass, the lead, drift lead | Parts, World (navigation instruments; sounding as an evolution) | M5 |
| II | Knotting and splicing | Knots, hitches, bends, seizings, serving, gaskets, reef beckets, mats, slings, parbuckle | Parts (line fittings), Crew (boatswain's tasks). Mostly flavour; a few items become tasks (passing gaskets, seizing) | M8 |
| III | The log | Log line and half-minute glass, ground log | World (dead reckoning), Parts | M5 |
| IV | Rope | Rope kinds and strength tables, list of names of ropes | Parts (line ratings for strain and failure), Physics | M2 |
| V | Blocks | Descriptive list of blocks, strapping | Parts (purchase definitions) | M2 |
| VI | Tackles | Theory of purchases, friction, whip, runner, luff, swigging off | Physics (hauling effort and speed per hands on a line), Crew | M3 |
| VII | The mast, the rudder | Mast-making, yards and booms, explanation of the plate of spars, the rudder | Parts (spar taxonomy and dimensions), Physics (rudder) | M2 |
| VIII | Cutting and fitting rigging | Standing vs running rigging, proportions, dead-eyes, tension of rigging, wire | Parts (standing rigging and its ratings). Wire rigging is out of period | M2 |
| IX | Masting | Sheers, getting in a lower mast, bowsprit | Skip for play; Damage (jury masting draws on it) | M8 |
| X | Rigging ship | Every spar and its rigging in order: bowsprit, gammoning, lower rigging, topmasts, jib-boom, topgallant masts, royal rigging, flying jib-boom, yards, whiskers, gaffs and booms, running rigging | **Parts.** This is the chapter the ship data file is built from | M2 |
| XI | Sails | Names and description of sails, cutting, roping, reef beckets, fitting and bending, head sails, fore-and-aft sails, **studding sails**, table of sails allowed, canvas table | **Parts** (sail definitions), Physics (areas, cloth), Evolutions (bending) | M2 |
| XII | Stowage | Stowing a hold, theory of stowage and construction | Physics (ballast, trim, stability), World (cargo) | M5 |
| XIII | Purchasing heavy weights | Securing yards, derrick, hoisting boats and guns, purchasing and transporting anchors | Evolutions (boats in and out, guns in), Crew | M7 |
| XIV, XV | Ground tackle | Anchors, cables, marking, bending, bitting, ranging, sea anchor, jury anchors, messenger, nippers, stoppers, compressors, heaving up, cat and fish gear | **Parts, Evolutions** (anchoring, weighing, catting and fishing). Chain vs hemp cable both allowed; the 1884 steam capstan chapter is skipped | M3, M5 |
| XVI | Organisation | Berthing, messing, **the watch bill**, calling the watch, **quarter bill**, stationing the crew, duties of seamen in different parts of the ship | **Crew.** Watch and station structure comes from here | M3 |
| XVII | Preparing for sea | Spare spars, stowing booms, hints | Evolutions (a port routine), Parts (spare spars) | M5 |
| XVIII | Boats | Types, lowering and hoisting, orders in charge, towing, warping, kedging, boats in surf, weighing anchor with boats | Evolutions (towing, warping, kedging), later boats as sub-vessels | M7, M8 |
| XIX | Rules to prevent collisions | Rules of the road, fog signals | World (NPC captain behaviour, lights). Later-period rules; use the spirit, not the 1860s text | M6 |
| XX | In charge of the deck | **The trumpet and commands**, bending sail, making sail after bending, furling, loosing, shortening sail, crossing and sending down topgallant and royal yards, unbending, rigging lower booms, awnings | **Evolutions.** Port-routine versions of the core sail evolutions, with the words of command in sequence | M3 |
| XXI | Getting under way | Casting, standing out on a wind or before it, lee shore, tideway cases, weighing in a gale, making sail from a spring | Evolutions (weighing and casting), World (tides) | M5 |
| XXII | In a tideway | Drifting, clubbing, backing and filling | Evolutions, World | M5 |
| XXIII | At sea | The officer of the deck, **making and taking in sail: courses, topsails, taking in in a gale, royals, topgallants, head sails, studding sails, trysails** | **Evolutions.** The at-sea versions of the first forty evolutions | M3 |
| XXIV | Working to windward | Steering, conning, **tacking**, trimming yards, **table of best angles of yard with keel**, hauling of all, missing stays, tacking under double-reefed topsails, tacking with a drag, clawing off a lee shore, **club-hauling, wearing, wearing in a gale, bare poles, box-hauling**, wearing short round, half boards, sailing in line, cracking on, towing | **Evolutions, Physics.** The yard-angle table is a tuning constant; the manoeuvre descriptions are task sequences | M2 (table), M3 |
| XXV | Wind baffling | Coming to against the helm, boxing off, chapelling, bracing in and up, taken aback, calm | Evolutions, Physics (aback behaviour is a "known truth" test) | M3 |
| XXVI | Emergencies | Heaving to wind aft, struck by a squall under all sail, man overboard, collision, sounding | Evolutions, World (squalls as events) | M5 |
| XXVII | Reefing | Reefing and hoisting, turning out reefs, reefing in stays, reefing with beckets and toggles, reefing topsails and courses | **Evolutions** | M3 |
| XXVIII | Storms | Squalls, laws of storms, barometer, record of weather, **table of force and velocity of wind** | **World** (weather model), Physics (Beaufort-style wind scale) | M5 |
| XXIX | In a gale | Reducing sail to a gale, down topgallant masts, scudding, brought by the lee, broaching to, lying to, steering by a cable, drag, knocked down, on beam ends | Evolutions, Physics (broach and knockdown as failure states) | M5 |
| XXX | Parting rigging | What to do when each major line carries away: braces, reef tackle, topsail sheet, clew garnet, parrel, bobstay, topmast stay, jib sheet, tiller rope, shroud, lift, truss, gammoning | **Damage.** Each entry is a part failure with a consequence and a repair task | M2 (failures), M8 (repairs) |
| XXXI | Losing masts | Bowsprit, lower mast, jury mast, topmast, sending down the wreck, topgallant mast, jib-boom, lower cap, trestle-trees, main chains, yards, fishing a yard, rudder gone | **Damage** (spar loss and jury rig) | M7, M8 |
| XXXII | Shifting sails and spars | Split sails, shifting a jib, a topsail, a course, in chase, shifting spars | Evolutions (sail replacement), Damage | M8 |
| XXXIII | Chasing | To chase to leeward and windward, chased | World (NPC captain tactics), Evolutions | M6 |
| XXXIV | Anchoring, tending ship | Entering port under various winds and tides, anchoring with a spring, on a lee shore, backing an anchor, veering, housing topmasts, cutting away masts, riding at single anchor | Evolutions, World (harbour approach) | M5 |
| XXXV | Mooring, clearing hawse | Mooring, clearing hawse | Evolutions (harbour) | M8 |
| 1884 XXXIV | Handling fore-and-afters | Schooner handling | Later rigs | M8+ |
| 1884 XXXV | Handling vessels under steam | | **Skip** | |
| 1884 XXXVI | Getting on shore, leaking | Grounding, fothering, leaks | Damage, World (grounding) | M5, M8 |
| 1884 XXXVII | Life-saving service | | **Skip** | |
| 1884 App. A, E | Rope dimensions, canvas tables | | Parts, Physics (ratings) | M2 |
| 1884 App. G | Routine, preparing ship for sea | | Crew (daily routine as starter standing orders) | M4 |
| 1884 App. I, K | In a tideway under sail, tending ship at single anchor | | Evolutions, World | M5 |
| 1884 App. L | Turning experiments, tactical diameters | | Physics (turning-circle "known truth" test) | M2 |
| 1884 App. M, N, O | Sounding machine, ship's papers, bugle calls | | Skip | |

## Cross-checks with the period sources

Luce is 1866 to 1891 and United States Navy. Two things to check against Lever (1808 to 1827, British merchant and naval practice) and Falconer (1769 to 1780) before a Luce practice becomes a game rule:

- **Vocabulary.** Luce says "port"; the game's era says "larboard" (the Royal Navy changed officially in 1844, the US Navy in 1846). Falconer and Lever are the authorities for names; Luce is the authority for procedure.
- **Rig details that moved in the period.** Chain cable, iron gammoning, patent anchors, wire rigging, rigging screws and steam capstans are later than or marginal to 1793 to 1815. Spritsails and sprit-topsails, bonnets, and hemp cables are earlier or fading. Lever shows the 1808 state; the ship data file decides per vessel.

## Suggested first forty evolutions, with sources

Grouped as the catalogue will be. Each will cite chapter and sub-heading as in `README.md`.

- **Setting and taking in** (Luce XXIII, XX; Lever): courses, topsails, topgallants, royals, jib and fore topmast staysail, spanker/driver, staysails, studding sails (lower, topmast, topgallant, each side), trysails. That is roughly 20 evolutions counting set and take in as pairs.
- **Reefing** (Luce XXVII; Lever): reef topsails (one, two, close), shake out a reef, reef courses.
- **Manoeuvres** (Luce XXIV, XXV; Lever): tack, wear, box-haul, club-haul, heave to, fill away, box off, brace up, brace in, square the yards, lie to, scud.
- **Ground tackle** (Luce XIV, XV, XXI, XXXIV; Lever): let go, veer, weigh, cat and fish, kedge, moor.
- **Routine** (Luce XVI, XX, App. G): call the watch, call all hands, pipe down, sound the well, heave the log, heave the lead.
