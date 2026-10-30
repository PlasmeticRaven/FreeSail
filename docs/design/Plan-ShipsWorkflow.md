# Plan: three ships by workflow (drafted 2026-10-25, to launch after practice and resupply are in)

**Package 75's brief binds over this plan** (`docs/dev/M7-WorkPackages.md`, "Package 75", 2026-10-28). Where the two differ, the brief stands. The main differences:
- a 74 is added;
- the *Prince de Neufchatel* is an American of 1812;
- every ship gets a hull profile through the generator, including the existing seven;
- the sub-types become fits and roles;
- the settee's design goes to the lead before it is built;
- the work is done on `claude/pkg-75` in a fresh clone, not in the local repository named below.

This plan was carried into the clone by file, from the `ships/research` worktree of 2026-10-25, together with the research notes, the decision sheet and the texts they cite.

HMS *Indefatigable* as built (a 64 of 1784) and as razeed (a 44 of 1795), the privateer
*Prince de Neufchatel*, and a British bilander. All three are built by the workflow method
that built practice and resupply: research, the owner's decisions, design, a
behaviour-free stage 0, builders in worktrees, review by lenses, adversarial verification,
fixes, truths, docs. They are compared afterwards with the ships built so far by single
agents. This plan is for the owner to approve before anything launches. Nothing here is
built.

## 0. The owner's decisions (settled 2026-10-25)

| Question | Ruling |
|---|---|
| The privateer | **The *Prince de Neufchatel*,** for her rig: as the owner understands it, a hermaphrodite brig, mostly square-rigged on the fore with a small loose-footed gaff sail, which the game does not have (*Grecian* would repeat the topsail schooner already held). The research confirms the rig from the sources. |
| Online research | **Yes, public domain only:** catalogue entries and page images (Royal Museums Greenwich, the Internet Archive and the like), each filed with its provenance in `docs/references/README.md`; nothing behind a login, and nothing in copyright held whole. |
| The bilander | **The British coasting bilander** of Gwyn's drawing (c. 1780, NMM PAG3828), with a **real settee main**: the four-cornered lateen on a long oblique yard, built on the lug's yard and dipping machinery, set and clewed up as Lescallier gives it (p. 390). |
| The *Indefatigable* | **The 64 first, then the razee derived from her,** as the dockyard did it. The sources decide which gets the most depth, but **the razee is the main goal.** The owner provides figures and pictures from the Vanguard Models kit (high quality, but not the full plans; it may show the razee's hull plan without a scale). |
| The era | **General, about 1792 to 1820.** The game is most built out in 1805, but no file should fix a year where a scenario could want another. The *Neufchatel*'s file carries no nation, so a scenario can sail her as a French privateer, an American, or anything between; fits and dates by the scenario. |
| The bilander's arms | **Unarmed by default, with an armed merchant fit:** a few small guns and swivels, as the merchant brig's. |
| Scenarios | **One each,** under rules captains at seed 7 with pinned weather, as the first action is (below). |
| The viewer | **The same standard as the current ships.** Every sail but the settee is a type the viewer and the engine already know, and the settee builds on the lug's dipping. Design and build agents verify the rendering with screenshots in the built-in browser, and **the owner checks along the way** (§4, the human checks). |

**Given by the owner (2026-10-25):**
- The Vanguard notes, pictures and reference list for the *Indefatigable*, in `D:\Projects\FreeSail\owner-notes\indefatigable\`.
- Winfield's entries from the owner's own copies, in `owner-notes\winfield\`. These are private reference: agents may read them in full, and only facts cited by page go into the repository.
- **No full-resolution Greenwich images** (the lead's advice; the owner's to confirm). The free 1280 px images are finer than the game needs.
- **The frigate-36's armament stays as it is,** marked as incorrect pending correction to Winfield (§4).

## 1. What the project already holds

- **The *Indefatigable*:**
  - `docs/design/VesselCandidates.md` has the kit manual's figures (1,384 tons burthen, 160 ft 1¼ in on the gun deck, 131 ft 10¾ in on the keel, 44 ft 5 in beam, depth of hold 19 ft as a 64 and 13 ft 3 in as a frigate, 310 men).
  - `VesselReferences-2026-10.md` §4 has the Greenwich draughts of her as built (ZAZ1953, and ZAZ1407 with *Stately*'s lines after *Raisonable*'s, ZAZ1280 the class's inboard profile). The razee's plans were not found in the one search made.
  - Steel 1794 holds the masting and rigging tables by rate.
  - **The owner's Vanguard notes and pictures (2026-10-25)**, in `D:\Projects\FreeSail\owner-notes\indefatigable\`: the armament by date, 14 quarterdeck ports, the poop shortened, the 64's masts kept with the lower masts shortened at the heels, and a Greenwich draught of the razeeing (picture 2).
  - **Winfield 1793-1817 pp. 99-100 (the owner's copy, `owner-notes\winfield\`)** confirms the build dates, costs and as-built dimensions. It adds:
    - the Admiralty Order of 8.9.1794;
    - the design's figures and the 64's guns and men;
    - the razee's established guns: 26 × 24-pdr; quarterdeck 8 × 12 and 4 × 42-pdr carronades; forecastle 4 × 12 and 2 × 42-pdr carronades;
    - her captains and stations to 1816. She was on the Brest blockade under Rodd from 10.1805, and with *Amazon* (the game's frigate-36) in Pellew's squadron in 1796-97.
  - **The research note of 2026-10-25** (`owner-notes\indefatigable\research-note-2026-10-25.md`; nine agents; Winfield folded in as its §9). It has:
    - the razee's draughts found: RMG ZAZ2371-2375, with the Anson and Magnanime sets;
    - the armament and complement by date;
    - Osler's account of the reduced rig, slow and unmanageable until Pellew altered it;
    - ten dated sailing accounts for truths.

    Phase 1's R1 starts from it and from its §7, the list of what is still open, rather than from nothing.
- **The *Prince de Neufchatel*:**
  - Not in the held Chapelle (*The Baltimore Clipper*, 1930), whose index has *Grecian* with full plans.
  - **Winfield 1793-1817 pp. 335-336 (the owner's copy):**
    - 110 ft 8 in, 93 ft 8¼ in keel, 25 ft 8 in by 11 ft 6 in, 328 22/94 tons; 16 × 12-pdr carronades and 2 × 6-pdrs;
    - built by Christian Bergh, New York, 1812-13; taken 28.12.1814; surveyed at Deptford and broken up in 1815;
    - a copy ordered at Woolwich 10.4.1815 and never built. So her lines were taken off, and the research looks for that draught in Greenwich's catalogue.
  - Winfield calls her a schooner; his caption calls her a "schooner-brigantine". Philip Reed's model in it shows a square fore with topsail, topgallant and royal, a boomed gaff main with a gaff topsail, and what looks like a small square sail at the main masthead.
- **The bilander:**
  - The period's words in Falconer 1780 (BILANDER), Steel 1794 (p. 220), Lescallier 1791 (p. 390 the sail, p. 404 the vessel) and Willaumez (BÉLANDRE).
  - The two pictures in `docs/references/images/`.
  - No measured dimensions. The base, until the research finds better, is a brig's hull of her size.
- **The engine:**
  - The lug's yard and its dipping (package 43b), and the gaff, square and staysail types.
  - The generator's builders, the armament of package 70, the quarter bill, the magazine by kind (practice and resupply), and the pivot (`Proposal-PivotGun.md`) if the *Neufchatel* carried one.

## 2. The workflow's phases

Each phase is its own workflow, so the lead and the owner read each result before the next
begins.

### Phase 1: research (one workflow, parallel)

| Agent | What it finds |
|---|---|
| R1, the *Indefatigable* | The 64's lines and dimensions from Greenwich (ZAZ1953, ZAZ1407, ZAZ1280, read at the best resolution public); the razeeing of 1794-95 (what was cut away, what the masts became, her armament by year as a razee, her complement), from public-domain lists (Charnock 1802 vol. III, the Navy lists) and the owner's Vanguard notes; the 64's masting by Steel's tables for her rate |
| R2, the *Prince de Neufchatel* | Her rig confirmed (hermaphrodite brig or otherwise), her dimensions, lines and spars from any public-domain draught (Greenwich's catalogue for the draught taken off after capture), her armament and complement, with every figure marked read, OCR or memory |
| R3, the bilander | Lescallier's settee in full (yard, parrel, halyard, lift, two vangs, brace, tack to weather, sheet to the taffrail, buntlines and clewlines), any British bilander's dimensions or tonnage in a public-domain list (Lloyd's Register, prize records, Chapman's plates if one is a bilander), the proportions measured off Gwyn's drawing, and her crew and trade |
| R4, the engine | How the generator builds a ship (and how the razee could be derived from the 64 in code); the lug's yard and dipping and what a settee yard needs beyond it; the sail physics for an oblique yard; the evolutions to set, take in, brace and dip; the crew stations each new rig needs; and **how the viewer draws sails and yards** (`client/`: from `corners_m` or otherwise), with screenshots of the current ships in the built-in browser as the standard to match |
| R5, a completeness critic | Reads R1 to R4 and asks what is missing: an unread source, an unverified figure, a feature of a rig the engine cannot carry. Its list is the next round of research, until a round turns up nothing new |

The output is a research note per ship in `docs/design/` (like `VesselReferences-2026-10.md`)
and the sources filed in `docs/references/`.

### Phase 2: the owner's second round (human)

The research's open questions go to the owner, in one short round. Likely ones:
- the *Indefatigable*'s armament year;
- the *Neufchatel*'s rig if the sources disagree with the owner's understanding;
- the bilander's size;
- whether the settee is tacked to windward always, or shifted.

### Phase 3: design (one workflow)

- A design per ship, drafted from two angles (fidelity first, and buildability first) and judged.
- One design for the settee as an engine extension, the riskiest piece, drafted from three angles and judged.
- A synthesis into one build document with:
  - stage 0;
  - **file ownership**;
  - the interface contracts;
  - the tests and truths;
  - the pins expected to move (none of the existing ships' passages should).

**One structural decision, the lead's:** the new ships go into per-ship generator modules
(`tools/ships/indefatigable.py`, `neufchatel.py`, `bilander.py`) that `tools/gen_ships.py`
imports and calls. The existing ships stay where they are. The generator is one 8,000-line
file today, and parallel builders in it would collide.

### Phase 4: stage 0 and build (one workflow)

- **Stage 0 on main:**
  - the per-ship module hooks;
  - the descriptions and size ranks;
  - any settee interfaces as inert stubs;
  - the event specs.

  Checked independently to change nothing.
- **The builders, in git worktrees:**

  | Builder | Builds | Depends on |
  |---|---|---|
  | B1 | The *Indefatigable*: the 64, then the razee derived from her, in one module, with her fits by year | — |
  | B2 | The *Prince de Neufchatel*, with her fits | — |
  | B3 | The settee in the engine: the sail type, its yard, its physics, its evolutions, and its crew stations | — |
  | B4 | The bilander's hull, rig and fits | B3's interfaces |
  | B5 | The viewer: the three ships drawn to the current standard, the settee and its yard included, verified by screenshots | B1 to B4's files |
  | B6 | The scenarios, one each (below) | — |

- **Each builder's branch:** reviewed by lenses as soon as it is done, then fixed.
- **The review lenses:**
  - **sources and fidelity:** every figure cited or marked;
  - **sailing:** the polars, the balance, and truth 9's strain behaviour against what the period says of the type;
  - **the generator:** every existing ship file byte-identical;
  - **the gun deck:** armament, quarter bill and magazine;
  - **the viewer:** screenshots against the current ships.

### Phase 5: merge, truths, review, docs (one workflow)

- **Merge** in dependency order.
- **The known truths**, numbered after the last at the time. Each:
  - sails the existing passages with the new ships beside them, moving nothing;
  - pins each ship's best point of sailing and speed against the period's accounts;
  - pins the razee against the 64 (lighter, stiffer, faster: what the razeeing did);
  - pins the settee's handling (setting, dipping or shifting, and going about);
  - checks each scenario round-trips and runs.
- **A whole-change review:** six lenses, two skeptics per finding, one fixer.
- **The as-built notes:** TuningNotes, the spec's as-built text, Harness, and the primer's vessel pages.

### Phase 6: the owner's checks, and the comparison

- **The human checks:**
  - after Phase 1, the research notes;
  - after B5's first screenshots, the viewer;
  - after the merge, sailing each ship in the harbour.
- **The comparison:** one evaluator agent compares the three new files with the ships built so far by single agents (the cutter, the brig, the lugger, the smack, the topsail schooner), by a stated rubric:
  - figures cited per figure;
  - the share marked UNVERIFIED;
  - the defects the review caught before the merge;
  - truths per ship;
  - sailing against the period's accounts;
  - the viewer's fidelity;
  - and the owner's own impressions from the harbour.

## 3. The scenarios

| Ship | Scenario | Who else |
|---|---|---|
| *Indefatigable* (the razee) | On the Ushant station in a westerly, a French frigate seen standing out of the Iroise; the 64 as a second fit or a second scenario | A French frigate of the 36's file, under her own colours |
| *Prince de Neufchatel* | Cruising the western Channel for prizes, a convoy of four under a brig-sloop working up from the Lizard; her nation the scenario's (French by default in 1805) | Package 72's convoy and its escort |
| The bilander | Coasting from Falmouth to Plymouth with a cargo, a summer forenoon, a lugger about | A trader or two of the business |

## 4. Guards, from the last build

- **One test suite at a time on this machine, at two workers.** Two at once crashed workers before.
- **Every new attribute a plain class default; nothing drawn on existing paths.**
- **Ship files through the generator only.** Every existing file byte-identical at every stage.
- **The frigate-36's armament stays as it is** (the owner, 2026-10-25). Its quarterdeck differs from Winfield's establishment (p. 143), and it is marked as incorrect, pending correction, before this build starts. No builder corrects it. A scenario that puts *Amazon* beside the *Indefatigable* uses her as she is, and the comparison notes the mark.
- **Bisect in a copy**, never the folder a game runs from.
- **Phases 1 to 3 work in a docs-only worktree:**
  - where: `D:\Projects\FreeSail\FreeSail-ships-worktrees\research`, branch `ships/research`, cut from main at 0127253 (launched 2026-10-25);
  - why: the review workflow for practice and resupply was still working on main, and this way nothing touches it;
  - when it merges: into main with Phase 4's stage 0, once practice and resupply are reviewed and the whole slow tier has passed.
- **Images downloaded for measurement stay outside the repository,** in `owner-notes\<ship>\rmg\`. These are Greenwich's free 1280 px images, and the photographs are the museum's.
- **Builders run Python from their own worktree's root.** The stale editable install points at the old Downloads folder, so imports work only from a tree's root.
- **The owner's folder, `FreeSail-claude-dreamy-darwin-d77nty`, is never touched.** The build goes on a branch of the local repository `FreeSail-claude-dreamy-darwin-d77nty-m7-practice-resupply`, from its main once practice and resupply are reviewed and the owner has tested them, or in a fresh copy if the owner prefers. Nothing goes to GitHub.

## 5. Scale, and cost

From the last build:
- **Agents:** about 60 across the six phases (the last build took 35 in three workflows).
- **Tokens:** about 15 to 30 million.
- **Wall-clock:** most of a day, dominated by the research's page reading, the builds' test runs, and the owner's checks between phases.

The research and the settee's design are where the money is best spent. The builds are
mostly the generator's existing method.
