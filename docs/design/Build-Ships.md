# Build design: package 75, the ships (Phase 3's synthesis)

**Status (2026-10-28).** The one build document of package 75, as `Plan-ShipsWorkflow.md`'s
Phase 3 asks: stage 0, file ownership, the interface contracts, the tests and truths, the pins
expected to move. It binds three pieces of design into one road:
- **Ext**, `docs/design/Design-ShipsEngineExtensions.md`: the settee, the lateen class finished
  (with the mizen course cut at the mast) and the yards under the bowsprit, the one document
  for the lead's gate;
- **Indf**, `docs/design/Design-Ship-Indefatigable.md`: the first ship, the 64 of 1784 and the
  razee of 1795;
- **the shared work**: the hull profile in every file, the viewer drawing it, the lee ports, the
  sub-types as fits and roles, the small ships' fits and bills, the pivot arcs, Table No. 29,
  the frigate's quarterdeck and the scenarios' common ground. It was drafted in the session's
  scratch and has no document of its own, so it is folded in here whole, as Part B.

The *Prince de Neufchatel*, the bilander and the *Bellerophon* are designed later, each before
its build. This document lays what they need now and says what their designs must settle
(Part C). Nothing is built. Where the three designs disagreed, this document settles it (§1),
and where a settlement changed Ext or Indf, that document was edited to agree (§20).

**Where.** The clone `D:/Projects/FreeSail/FreeSail-pkg-75` on the package's branch at 6b94731, the
lead's 3421829 merged in (packages 73 and 86, and 84's steps 1 and 2). Every `file:line` is at
that head. Paths are from the repository root. A builder re-checks a line before editing it.

**What binds, in order:**
1. The brief, `docs/dev/M7-WorkPackages.md`: its head rules (l. 1-33) and "## Package 75"
   (l. 1540 to the end). No model or vendor identifier in any file. Nothing under
   `docs/agents/consent/` touched. The ship files never edited by hand, only through
   `tools/gen_ships.py`. Pins re-measured only where a change moves them, old beside new, with
   the reason, proven. Never a test skipped, disabled or quarantined. Realism, not pacing.
   Truths pin states, counts, ticks and bands, never digests (decision 26).
2. The lead's go-ahead of 2026-10-28. Phase 3, then the build one ship at a time, the
   *Indefatigable* first. The generator modules, the hull profiles and the ship files need no
   gate. The gate stands on the engine extensions only: Ext reaches the lead before their
   builders start, and the plain ships' builders do not wait for it. The physics' equations are
   not changed. The lee ports are wired for every ship with sourced sills, each moved combat
   pin shown old beside new with the reason and a bisection. The hull profile is drawn in the
   viewer for every ship, and package 81 starts from it. Anything written against `world.ship`
   or a `CrewedWorld` goes through the names the Hull keeps (`Design-OneWorld.md` §2.2).
3. The plan, `docs/design/Plan-ShipsWorkflow.md`: the per-ship modules under `tools/ships/`,
   imported by `tools/gen_ships.py`, the existing ships left where they are.
4. The owner's answers and the lead's rulings, `docs/design/Decisions-ShipsRound2-2026-10.md`
   l. 1-80. Every decision not named there is taken as recommended. **D18 and D25 are open:
   this document proposes, it does not settle them.**
5. The research notes: **Ind**, **Neuf**, **Bil**, **Eng**, **Bel**
   (`docs/design/Research-*-2026-10.md`).
6. The owner's private references (`D:/Projects/FreeSail/owner-notes/`): facts cited by book and
   page, never their text.

**Marks.** *read*: the code or the page cited. *measured*: arithmetic on the files or the notes,
or a scratch script run from the tree root with `py`, kept outside the repository (this
document's: `scratchpad/design/build/shut.py`). *observed*, *catalogue*, *secondary*, *memory*,
*judgement* as the notes use them. "Plainly:" marks a choice that departs from a decision, a
ruling or the brief, with the reason. No git was run and no test suite was run to write this
document. Nothing in the repository was written but this file and the edits of §20.

**The maps.** The code maps cited as *map-engine* and *map-generator*, and the shared-work
draft folded into `Build-Ships.md`, are filed beside this document in `ships-design/`. The
scratch scripts named are not.

---

## In brief

- **The order.** Stage 0, then the ships one at a time: the *Indefatigable* (B1), the *Prince
  de Neufchatel* (B2), the *Bellerophon* (B7), the bilander (B4). Beside them run three tracks,
  each one builder: the shared work (B8: Table No. 29, the profiles and sills of the eight
  files, the sub-types and small ships' fits, the lee ports in two steps), the viewer (B5) and,
  once the lead approves Ext, the engine (B3: the lateen, the bowsprit yards, the settee). The
  scenarios (B6) follow each ship.
- **The gate.** Only B3 and what it carries wait for the lead: the 64's mizen course on its
  yard and her spritsail yards (behind two module constants; Indf §0), the same pieces of the
  74, and the bilander's handling. The razee, the 64's stand-in, the Neufchatel and the 74's
  plain parts do not wait.
- **Stage 0 in four kinds.** Stage 0 now lays every un-gated hook, key, registry slot and stub
  (§3.1). Stage 0E lays Ext's own interfaces after the lead approves Ext (§3.2). Stages 0b, 0c
  and 0d lay what each later ship's design names (§3.3). Each is checked by an agent that did
  not write it to change nothing.
- **The merge.** The lead's branch is in at 6b94731. Before each later stage the integrator
  takes the brief's fetch and merge of the lead's branch into the package's branch again
  (§2.1).
- **Ownership.** No file has two open owners. A file passes only at a merge into the
  package's branch. The ship builders never edit `tools/gen_ships.py` (stage 0 names their four
  modules), never edit an existing ship's file, and add only their own rows to
  `freesail/world/ships.py` in their own window (§4).
- **The truths.** 7-185 to 7-199, by content (§15): seven for the *Indefatigable* and the shared
  work (7-185 to 7-191), eight reserved for the three later ships and the settee (7-192 to
  7-199).
- **The pins.** None of the existing ships' sailing passages move. The moves are named: Table
  No. 29's two magazine rows and the charges of four files; the lee ports' combat pins, each
  bisected; the privateer's pivot if her arc moves; the 74's three "ship of the line"
  assertions (§16).
- **Settled here** (§1): the profile's one form; where the gun tables live; the caches; where a
  new ship's description row is written; where a description's fit lives; the roll's read
  path; four lookups moved into stage 0 for ownership; the 64's stage B against Ext's answers;
  the truths' allocation.

---

## Decisions taken

| # | Decision | Source |
|---|---|---|
| 1 | The ships one at a time: the *Indefatigable*, the *Neufchatel*, the *Bellerophon*, the bilander | The go-ahead (the first); judgement on the rest, by what each waits on (§2.3) |
| 2 | The razee, the 64's stage A, the *Neufchatel* and the 74's plain parts wait for nothing gated. The gate holds B3 and the pieces it carries | The go-ahead, item 2; Indf §0; Ext §9.4 |
| 3 | Ext goes to the lead with this document's three edits to it (§20). B3 starts on the lead's approval, after stage 0E | The go-ahead; Ext E18-E19 |
| 4 | Stage 0 lays every un-gated inert hook now. Stage 0E lays Ext §8's interfaces after the approval. Stages 0b-0d lay what each later design names | The plan's behaviour-free stage 0; the gate. **Plainly:** Ext §8 put its interfaces in stage 0. They are laid after the approval because the gate is on that design and nothing un-gated needs them |
| 5 | The lead's branch fetched and merged before every later stage | The go-ahead, item 3; the brief |
| 6 | The shared work is one builder's track (B8), five steps beside the ships | The shared draft §0; the plan (parallel builders in one file collide) |
| 7 | One viewer builder (B5) draws the profile and the three rig drawings | Ext §9.2; the shared draft §2 |
| 8 | The profile's one form (§5.1): Indf's keys and port triples, with the shared draft's `breadth_m` added; Indf's deck words | Indf §3.1; the shared draft §1.1; settled here |
| 9 | Every profile height above the file's waterline. Every port gun's `(x_m, height_m)` equal to one port triple of its deck, to the centimetre | Indf §3.1, decision 9; the shared draft S2-S3 |
| 10 | D18 proposed **(a)** for every file. Open: the owner chooses on screenshots | Indf §2.2; the shared draft §1.6 |
| 11 | The new ships' gun patterns, crews and anchors live in `tools/ships/period.py`; the shared tables of `gen_ships.py` stay as they are | Indf §5.3, against the shared draft §5.5 |
| 12 | `exercise_allowance(upper_deck_guns, decks=1)` in stage 0; the two-deck note in `period.py` | The shared draft §5.5; Indf §5.4 |
| 13 | The three caches of eight raised to 32 | Indf §8, against the shared draft's 16 |
| 14 | The ship builders never edit `tools/gen_ships.py`: `SHIP_MODULES` names the four modules from stage 0, each a stub writing nothing until built | Settled here; Indf §1.2 had the tuple grow |
| 15 | A new ship's `DESCRIPTIONS` row and lookout words land with her file, by her builder. Every registry row keyed by a description (rank, size words, man-of-war sets, roles) is laid in stage 0 | Settled here: a description row names a file, and the harbour offers every row to the scenario editor (`ui/harbour.py:390`) |
| 16 | A description's default fit and roles are written in the file's own `ship.descriptions` by the generator, and read through `description()` | The brief item 4 ("the generator the one place a fit is written"); settles the shared draft §4.1, which put them in the index |
| 17 | `armament.default: unarmed`; the topsail schooner, the lugger and the smack carry fits and bills and sail unarmed by default | The shared draft S9; the brief item 5 |
| 18 | `privateer-schooner.yaml` kept beside the *Neufchatel* | The shared draft S10; the owner's answer on file |
| 19 | Table No. 29 enters through `freesail/ship/charges.py`, an empty table laid in stage 0, so that `ship/parts.py` stays B3's | The shared draft S11; ownership |
| 20 | The lee port: the heel toward the gun's side plus the roll's amplitude; sill and half-breadth from the profile; ports only; reopened six inches clear; built as L1, L2, L3 | Bel §13.1 answer 7; the lead's ruling; the shared draft S6-S7 |
| 21 | The roll is read as `Firer.roll_deg`, built from `world.motion`, a name the Hull keeps | `world/hulls.py:52-127`; `combat/action.py:212-223`; settles Indf §10 |
| 22 | The four `curve_class` lookups outside B3's files are made in stage 0, where they are inert | Settled here, for ownership; edits Ext §8 and §9.1 |
| 23 | Each builder's tests go in its own new files. Truths are drafted there under their reserved numbers and moved into `tests/test_known_truths.py` in Phase 5. The tuning notes are folded in Phase 5 | The plan, Phase 5; `Build-PracticeAndResupply.md` §7.2 (the shared files the lead's after the merge) |
| 24 | The byte test made two-way in stage 0 | Indf §12.1 item 6 |
| 25 | At each merge the integrator regenerates every file, and a file moved by a shared change is committed regenerated in that merge, with the reason | Settled here (a ship module reads shared notes) |
| 26 | The truths allocated as §15 | The brief item 6; the three designs |
| 27 | Each new scenario's round trip and first hour are B6's tests, not a truth | Settled here; the shared draft's 7-188 not taken (§15) |
| 28 | The 64's mizen course at stage B takes Ext's lateral offset (0.8√A); the move from the stand-in is shown old beside new | Ext §3.2; settles Indf §12.2 item 3 |
| 29 | Steel's occasional driver on the 64's mizen yard is left out (*reopened*: the owner asked for the driver, §19.1 item 13, and chose Steel's driver boomsail for both, Ext §17); brails and the truss are not lines | Ext §3.4, §14 item 10, §17; settles Indf §4.4 |
| 30 | The frigate-36's quarterdeck is not corrected | The owner, 2026-10-25; the shared draft S12 |
| 31 | The fillers as posts are left to 77 | The shared draft S14; the lead's call (§19.2) |
| 32 | The merchant brig's description moved to `merchant-brig.yaml`, and a packet description: for the lead before they are built | The shared draft §4.4 |
| 33 | A scenario's `nations:` block: for the lead; laid in stage 0b if ruled in | The shared draft S13. **Plainly:** `world/scenarios.py` and `core/world.py` are outside the brief's file list |
| 34 | D10(a)'s key for the *Neufchatel*'s main topgallant: her design reports it to the lead; B3 builds it as a fourth step if the lead agrees | D10; Ext §14 item 12 |
| 35 | One test suite at a time on the owner's machine | The plan §4; the brief's suites rule |

---

# Part A: the road

## 1. Where the designs disagreed, and how it is settled

| Question | Indf | Ext | The shared draft | Settled | Edit |
|---|---|---|---|---|---|
| The profile's form | `keel_m`, `stem_m`, `stern_m`, `rail_m`, `wales_m`, `decks_m` and `ports_m` by deck word, `port_size_m`, `section_m`; ports as `[x, sill, half-breadth]` triples | — | `rail_m`, `breadth_m` (half-breadths at water and rail by station), `decks`, `stem_m`, `stern_m`, `wales_m`, and `tiers` with sill and half-breadth lines | Indf's keys and triples, plus the draft's `breadth_m`, required with `rail_m`: the viewer needs half-breadths along the length to draw a true side, and Indf's `section_m` gives them at midships only (§5.1) | Indf §3.1, §3.5 |
| The deck words | `lower`, `middle`, `upper`, `quarterdeck`, `forecastle`, `roundhouse` | — | "upper deck", "quarterdeck" as tier names | Indf's, one tuple shared by the profile, the gun `deck` key and the 74's bill | none |
| The new guns' weights | `tools/ships/period.py`; the shared tables untouched (Adye's 18-pdr carronade 9 cwt and 9-pdr 24½ differ from the shared 10 and 26) | — | new keys in `LONG_GUN_CWT` and `CARRONADE_CWT` | `period.py`: one sourced table for the new ships, none of the eight files' figures moved | none |
| The exercise allowance of a two-decker | 26 // 3 computed in the module | — | `exercise_allowance(upper_deck_guns, decks=1)` | The function in stage 0, so the 64 and the 74 share it | Indf §5.4 |
| The caches | 32 | — | 16 | 32: thirteen files after the package, room to grow | none |
| `SHIP_MODULES` | empty at stage 0, grown by each builder | — | — | All four named in stage 0, each a stub, so no ship builder edits `gen_ships.py` | Indf §1.2, §12.1 |
| A new ship's index rows | stage 0 | — | stage 0 (with "ship of the line" moving three assertions) | Keyed rows in stage 0; the `DESCRIPTIONS` row and its words with her file; the 74's "ship of the line" words with hers (they move three assertions) | Indf §8, §12.1 |
| A description's fit and roles | — | — | keys on the index row | In the file's own `ship.descriptions`, written by the generator | none |
| The roll the lee port reads | `ship.extra["motion"]` | — | `Firer.roll_deg` from `world.motion` | `Firer.roll_deg`. Both are the ship's own `Motion` (`core/world.py:655` sets one from the other); the firer is already built per ship at `combat/action.py:212-223` | Indf §10 |
| The four `curve_class` lookups in `world/ships.py:391`, `api/queries.py:334`, `api/readings.py:873`, `tools/gen_ships.py:869` | — | stage 0 (the generator's) and B3.1 (the other three) | — | All four in stage 0: `curve_class` is `cls` until a key widens it, so they are inert, and their files have other owners | Ext §8, §9.1 |
| Ext's interfaces | — | stage 0 | — | Stage 0E, after the lead's approval | Ext §8 |
| The mizen course's lateral offset at stage B | from the yard's after part, as a gaff's from its gaff (§12.2 item 3) | 0.8√A, 3-8% short of Steel's foot, kept (§3.2) | — | Ext's: no physics change, and 0.8√A (8.16 m) is nearer Steel's foot (8.86 m) than the stand-in's 11.1-m head. The stand-in overstates the offset, and the move at stage B is shown old beside new | Indf §12.2 |
| The mizen yard's lines | lifts, truss and brails as lines | jeers, lifts, vangs, bowlines as guys, one sheet, one tack; no brace, no brails (§3.4) | — | Ext's: the schema has no `brail` or `truss` line (`schema.py:119-141`), and `take_in_lateen` brails without one | Indf §4.4 |
| Steel's occasional driver on the 64's mizen yard | added at stage B | no engine path hangs a sail from another sail's yard (§14 item 10) | — | Left out, noted in her file; the lead may ask for the path. *Reopened by the owner (§19.1 item 13):* Ext §17 proposes Steel's driver boomsail behind its own flip; the owner chose it, and the lead's read is open (its §17.9 item 1) | Indf §4.4, §12.2 |
| Where a ship's tests and truths go | `tests/test_ship_particulars.py`, `tests/test_ships.py`, `tests/test_known_truths.py` | B3's own test files | `tests/test_ship_particulars.py` | Each builder's own new files; truths moved into `tests/test_known_truths.py` in Phase 5 | Indf §6.3, §13 |
| The truths | five | three for the settee, one offered for the 64 | four shared (7-185 to 7-188) | §15 | Indf §14, Ext §10.3 |

## 2. The build order

### 2.1 The lead's branch

- **Done.** The package's branch merged the lead's head 3421829 at 6b94731, carrying 73, 86 and
  84's steps 1 and 2.
- **Before stage 0** the stage-0 agent checks that the head the go-ahead names, 8db8b9a, is an
  ancestor of the package's branch (`git merge-base --is-ancestor`). If it is not, the fresh
  merge below is taken first.
- **Before each later stage** (stage 0E; each of 0b, 0c, 0d; the fork of each builder's worktree;
  each B3 step; each B8 step) the integrator runs the fetch and merge the brief gives
  (`docs/dev/M7-WorkPackages.md`, Package 75: `git fetch origin`, then a merge of the lead's
  branch from the origin into the package's branch). It is a merge into the package's own
  branch, never a rebase. Then it runs the byte test and the stage-0 guards (§14.2), and the
  fast tier when the merge brought code. 84's later steps reshape the World under the package;
  the merge shows a conflict early, and every builder's code reads only the names the Hull
  keeps (§4.4).

### 2.2 The tracks

| Step | Builder | What | After | Before | Moves pins |
|---|---|---|---|---|---|
| S0 | stage-0 agent | §3.1 | the ancestor check | everything | none (proven) |
| **B1** | the *Indefatigable* | stage A: the razee final, the 64 with a stand-in mizen course and no sprit yards (Indf §0, §13 steps 1-6) | S0 | B2 | none |
| SW-1 | B8 | Table No. 29's charges (§10) | S0 | B7's magazine (the long 32) | §16 |
| SW-2 = L1 | B8 | the profiles and sourced sills of the eight files (§5.3, §5.4) | S0 | SW-5, and B5's drawing of the eight | bytes only |
| B5.1 | B5 | the profile drawn (§6) | the first profile on the trunk (B1's or SW-2's) | the owner's screenshot check | pictures measured |
| SW-4 | B8 | the sub-types, the roles, the small ships' fits and bills, the privateer's arc (§8, §9) | S0; its `world/ships.py` rows at the boundary after B1 | B2, B6 | §16 |
| 0E | stage-0 agent | Ext's interfaces (§3.2) | the lead's approval of Ext | B3 | none (proven) |
| B3.1, B3.2, B3.3 | B3 | the lateen, the bowsprit yards, the settee (Ext §9.1), each merged before the next | 0E | B1's stage B (3.1, 3.2); the bilander's handling truths (3.3) | none expected |
| B5.2-B5.4 | B5 | each of B3's drawings (Ext §6), after its step | each B3 step | — | none |
| **B2** | the *Neufchatel* | her design, stage 0b, her file | B1, SW-4 | B4 | none existing |
| B1 stage B | B1 | `MIZEN_COURSE = "gated"`, `BOWSPRIT_YARDS = True`, the 64 regenerated (Indf §13 step 7) | B3.1, B3.2; taken at a boundary between ships | — | the 64's own figures, old beside new |
| SW-5 L2, L3 | B8 | the lee port on heel, then with the roll (§7) | SW-2 | B7's port truth | combat pins, bisected |
| **B4** | the bilander | her design, stage 0d, her file | B2, B3.3 (for her handling truths) | B7 | none existing |
| **B7** | the *Bellerophon* | her design, stage 0c, her file | B4, SW-1, SW-5 (for her port truth) | — | three assertions (§16) |
| B6 | scenarios | one per ship (§12) | each ship's file, SW-4 | Phase 5 | none existing |
| Phase 5 | integrator | truths moved in, notes, spec §27 as built, the primer's chapter, the whole-change review | every merge | the lead | — |

### 2.3 Why this order

- **The *Indefatigable* first**, the lead's word. Her razee is the package's main goal (plan §0)
  and needs nothing gated.
- **The *Neufchatel* second.** She waits on nothing gated if her design takes D10(c) or the lead
  puts D10(a)'s key with B3 (§13.1). She needs SW-4's pivot rule if she carries a pivot.
- **The bilander third**, as the owner asked (the lead's ruling on stage 0's questions, item 8,
  in `docs/dev/M7-WorkPackages.md`). Her handling truths wait for B3.3, the last engine step,
  and she uses B1's `spritsail_yards.py`.
- **The *Bellerophon* last.** Her long 32s need Table No. 29 (SW-1: 10 lb 10 oz, not the share's
  10 lb 11 oz), her port truth needs the lee port wired (SW-5), and her mizen course and
  spritsail yards come from B1's stage-B helpers when B3.1 and B3.2 are in. If her window opens
  before B1's stage B, she takes the 64's stand-in pattern.

**One ship at a time** holds for the ship builders: each ship's window opens with the fresh
merge and her stage 0, and closes with her merge. B1's stage B is taken between two windows.
B8, B5 and B3 run beside the ship of the window, on files disjoint from hers (§4).

### 2.4 What waits on the gate, and what does not

| Piece | Waits on the lead's approval of Ext? |
|---|---|
| The razee, final | no |
| The 64 at stage A: hull, profile, rig, guns, people, the stand-in mizen course, no sprit yards | no |
| The 64 at stage B: the mizen course on its lateen yard, the spritsail and sprit-topsail yards, truth 7-189 | yes (B3.1, B3.2) |
| The *Neufchatel* | no (D10(a)'s key, if built, is the lead's call: §13.1) |
| The 74's file at stage A | no |
| The 74's mizen course and spritsail yards | yes (B3.1, B3.2) |
| The driver of the 64 and the 74 (Ext §17, the addendum) | yes: the lead's read of the addendum (the owner chose the sail, Ext §17.9 item 1), then its stage-0 commit, B3.5 and B5's drawing; the 64 takes it by its own flip (`DRIVER`), so her stage B is not held by it, and if it misses her stage B, B1 flips it at a later boundary (Ext §17.8) |
| The bilander's file | generates after stage 0E; her handling truths wait for B3.3 |
| Stage 0E, B3, B5.2-B5.4 | yes |
| The shared work (B8), B5.1, B6 | no |

If the gate slips past the package's merge, the 64 and the 74 ship on their stand-ins with no
spritsail yards. **Plainly:** that departs from D8(b) and D9(c). Their files, the tuning notes
and spec §27 as built say so, and their rig clauses are re-measured, old beside new, when stage
B lands (Indf §0).

### 2.5 Suites

The brief's rule: each builder runs the fast tier once on its final tree and the slow tier of
the files it touched; after a mend, only the mended test's file, and the pace tests when the
mend touches a per-tick path. The whole suite is the lead's, on the build machine. **One suite
at a time on the owner's machine** (plan §4): builders running beside each other queue their
suites. The pace tests are run on the owner's machine only to record a figure; the floor is the
build machine's.

## 3. Stage 0

### 3.1 Stage 0 now (one commit, behaviour-free)

Each item is inert: no file, scenario or path uses it until a builder does. The lines are at
6b94731.

**The generator (`tools/gen_ships.py`) and `tools/ships/`**

1. **The hook.** `import importlib` among the imports (:110-118). A module constant
   `SHIP_MODULES = ("indefatigable", "neufchatel", "bellerophon", "bilander")`. In the
   `__main__` block (:8479-8490), after `smack(out)`:
   `sys.modules.setdefault("gen_ships", sys.modules[__name__])`, then
   `importlib.import_module(f"ships.{name}").build(out)` for each name. A ship module begins
   `import gen_ships as g` and is imported only there, after the alias. Measured (Indf §1.2):
   with the alias the module's `gen_ships` is the running script and its spars are rated;
   mixing a `Builder` of one copy with a `DesignLoad` of another fails at `dump` with yaml's
   `RepresenterError`.
2. **The packages.** `tools/ships/__init__.py` (a docstring: what the package is, how it is
   imported). Stubs `tools/ships/indefatigable.py`, `neufchatel.py`, `bellerophon.py`,
   `bilander.py`, each `def build(out_dir: str) -> None` that writes nothing, its docstring
   naming its design. The file names they will write are proposed in §3.3.
3. **`tools/ships/period.py`**, constants with their sources, importing nothing (Indf §12.1
   item 4): Adye 1804's long guns by pounder and length and carronades by pounder;
   `FALCONER_CREW` {42: 15, 32: 13, 24: 11, 18: 9, 12: 7, 9: 6, 6: 5, 4: 4, 3: 3} and
   `DOUGLAS_CARRONADE_CREW` 4; the 74's patterns (Bel §13.1 answer 12: the long 32 of 9 ft 6 in
   and 55 cwt, the long 18 of 9 ft 0 in and 40 cwt, the 9 of 7 ft 6 in and 24½ cwt); Steel's
   ground tackle for the 64 (Indf §7); `REGULATIONS_COLUMNS` (491, 343, 294);
   `TWO_DECKS_EXERCISE_NOTE` (the Regulations, the Gunner, Art. XXI, a third in ships of two or
   three decks). After stage 0 the ship builder of the window may append to it.
4. **`PEAK_COEFF["lateen"] = 1.25`** (:135): the hypotenuse of the lateen row's 1.15 and 0.48 at
   its 35° peak is 1.246, by the rule the comment at :133-134 states (Ext §3.1). Without it the
   rating pass raises a `KeyError` on any lateen sail (:434-441).
5. **The rating pass's entry** (:869) reads `sail.curve_class` for `sail.cls`.
6. **`exercise_allowance(upper_deck_guns, decks=1)`** (:3656-3662): a third for two or three
   decks, a fourth for one, as its own docstring cites. Every existing caller passes one deck.
7. **The gun helpers** gain `deck=None` and `round_to=0.1`: `broadside_pair` (:3709-3727),
   `chasers` (:3730-3746), `pivot_gun` (:3749-3765), `swivels` (:3768-3790). `deck` is written
   last in the gun's mapping and omitted when None; `round_to` rounds `x_m` and `height_m`
   (today's 0.1 by default, :3722-3723), as `round(v, 1)` or `round(v, 2)`, never
   `round(v / step) * step`, whose floats would move the eight files' bytes.
8. **`hull_profile(rail, breadth, **parts)`**, a new helper beside `Builder`: the profile
   mapping in §5.1's key order, metres rounded to the centimetre, raising `ValueError` with a
   sentence on anything §5.2 would refuse, so that a module fails at generation, not at load.
9. **`dump`** (:933-1078): a pass that sets each list of number lists inside `  profile:` on one
   flow line, as the `corners_m` pass does (:938-950), and notes from `hull_notes` keyed
   `"profile.<key>"` and `"profile.<key>.<deck>"`. `dump` notes only two-space hull keys today
   (:1072-1074), so the new branch fires only on those dotted keys.

**The ship (`freesail/ship/`)**

10. **The profile in the schema** (`schema.py`): `DECK_WORDS = ("lower", "middle", "upper",
    "quarterdeck", "forecastle", "roundhouse")`; `PROFILE_KEYS`; a frozen dataclass
    `HullProfile` of tuples; `HullSpec.profile: HullProfile | None = None` (:345-356, after
    `rudder`); `_parse_profile`, called from `_parse_hull` (:1245-1267), **strict**: an unknown
    key inside `profile` is refused, as a gun's is (today an unknown hull key vanishes:
    map-generator §0 item 4). The refusals are §5.2's.
11. **The gun's deck.** `GUN_KEYS` gains `"deck"` (:202-214); `GunSpec.deck: str | None = None`
    (:538-560), parsed beside the arc (:1017-1029); in `validate` (:1648-1670) a gun's deck is a
    `DECK_WORDS` word, and where the hull's profile has `ports_m`, a gun placed broadside, bow or
    stern that names a deck names one of its keys. `parts.py`: `Gun.deck: str | None = None`
    (:462-494), copied in `from_spec` (:496-511).
12. **Unarmed.** `UNARMED = "unarmed"`, allowed as `armament.default` (:825-); `ArmamentSpec.fit`
    (:590-596) returns `FitSpec | None`: None for "unarmed", named or by default. Its callers:
    `ship/graph.py:40` builds no guns from None already; `combat/far.py:103` skips None already;
    `combat/action.py:466` is taught to. The checker reads every `.fit(` caller.
13. **The pivot's own arc.** A pivot gun without `arc_deg` is refused (checked after the side,
    so that `tests/test_pivot_gun.py:160-175` still meets "no side"). `ARC_PIVOT_FROM_DEG` and
    `ARC_PIVOT_TO_DEG` (`combat/guns.py:140-141`) remain only for a gun pickled before 86
    (`pivot_arc`, :146-152). The brief item 5: "86's global constant retired". The one pivot on
    file carries its arc.
14. **`Sail.curve_class`** (`parts.py`, `Sail` :257-): a property returning `self.cls`. Stage 0E
    widens it (§3.2). The lookups that read it in stage 0 are items 5, 20, 21 and 22.
15. **The charges hook.** `freesail/ship/charges.py` (new): `CHARGE_TABLE_LB: dict[tuple[str,
    float], float] = {}`, its docstring naming Table No. 29 and SW-1. `charge_lb`
    (`parts.py:596-599`) returns the table's figure where it has one, else today's share, and
    the comment at `parts.py:575-582` says so, pointing to `charges.py` (B8 does not own
    `parts.py`). Empty, it changes nothing.
16. **`freesail/ship/profile.py`** (new, pure): `interp(points, x)` (linear, held at the ends),
    `rail_at`, `deck_at` (the uppermost deck at x), `ports_of(profile, deck)`,
    `sill_at(profile, deck, x)` and `half_breadth_at_sill(profile, deck, x)` (interpolated
    between the deck's port triples). The generator's helpers, the lee port and the tests read
    the profile only through these.

**The gun deck (`freesail/combat/`, `freesail/api/`)**

17. **`freesail/combat/ports.py`** (new): `PORT_PLACES = ("broadside", "bow", "stern")`,
    `PORT_REOPEN_M = 0.15`, and `update(battery, firer) -> tuple[frozenset[str], frozenset[str]]`
    returning two empty sets (shut, opened).
18. **`combat/guns.py`**: `Battery._shut: frozenset[str] = frozenset()` as a class attribute
    (`Battery`, :269-); `ports.update` called at the head of `Battery.tick` (:446-); `wants_work`
    (:331-340), `_fire`'s single guns (:788-793) and its ready list (:803-810) leave out a gun in
    `_shut`. The set is empty.
19. **The events** (`api/practice_readings.py:309-325`): `ev("the lee ports shut",
    "guns.ports_shut")` and `ev("the lee ports opened", "guns.ports_opened")`. Never emitted
    yet.
20. **`api/queries.py`**: `ship_graph` (:380-406) adds `hull["profile"]` as plain lists when the
    spec has one; `_sail_entry` (:333-336) reads `SAIL_CLASSES.get(s.curve_class)`.
21. **`api/readings.py:873`** reads `sails_mod.SAIL_CLASSES.get(sail.curve_class)`.

**The world (`freesail/world/`)**

22. **`world/ships.py`**: the caches at :266, :297 and :423 from `maxsize=8` to 32; `_trim_for`
    (:391) reads `wanted_sheet_angle(sail.curve_class, awa)`; `file_descriptions` (:266-279) and
    `description` (:286-295) carry a file's own `fit` and `roles` for a description (`roles`
    kept a list, where :278 makes every value a string today);
    `Vessel.role: str = ""`; `vessel_from_spec` (:1126-1190) reads a far ship's `role:` (one of
    her description's `roles` and of `ROLES`, else refused in words) and takes her description's
    `fit` when the scenario names none and it is not her file's default (:1184; §8.1). No file gives a description a fit or roles, and
    no scenario names a role.
23. **The roles.** `brains.role_of_vessel` (`world/brains.py:152-178`) returns the vessel's own
    `role` first, and gives `"sixty-four"`, `"razee"` and `"seventy-four"` the King's ship's
    doctrine as `"frigate"` has it (:170-171). `captains.role_for` (:914-926) takes the vessel's
    role first where a crewed World is made from her.
24. **The size registries** (`world/captains.py:286-305`). `SIZE_RANK` gains `"razee": 3`,
    `"sixty-four": 4`, `"seventy-four": 4`, `"hermaphrodite brig": 2` and `"bilander": 1`.
    `_SIZE_WORDS` gains, first and in this order, `("razee", 3)`, `("sixty-four", 4)`,
    `("seventy-four", 4)`, `("ship of the line", 4)`, `("two-decker", 4)`, `("bilander", 1)`.
    "Razee" must come first: the razee's words hold "frigate" and "sixty-four", and
    `size_rank_of` matches the whole words in order (Indf §8). Inert: no text the game gives a
    sail holds these words (grep over `freesail/`, `data/`, `tests/`: "ship of the line" only in
    `MAN_OF_WAR_WORDS`, three test lines that go through `description_key`, and pilotage
    sources).
25. **The man-of-war sets.** `_MAN_OF_WAR_DESCRIPTIONS` (`world/regimes.py:158`;
    `world/squadrons.py:1520`) and the tuple at `squadrons.py:467` gain `"sixty-four"`, `"razee"`
    and `"seventy-four"`.

**The tests**

26. **The byte test made two-way** (`tests/test_ship_particulars.py:555-581`, its list at
    :563-572): every file the generator writes equals its committed file, and every
    `data/ships/*.yaml` is one the generator writes. The same eight are compared; no builder
    edits a list again. `test_period_names_resolve` (:475-552) keeps its list, since each
    file's phrases are written by hand: each ship's builder runs the same check on that ship's
    phrases in its own test file.
27. **`tests/test_rig_classing.py`** (new): Ext §10.1's golden classing table of the eight files,
    measured at this head (masts with yards, head and after yards, the mast backed,
    square-rigged, the stagger, the driver, the boom sails, the lugger's dipping lugs).
28. **`tests/test_profile.py`** (new): `profile.py` on a hand-built profile; §5.2's refusals; the
    gun deck rule; `unarmed`; the pivot without an arc refused and "no side" still first; the hook
    writing the same eight files with the four stubs in place.

### 3.2 Stage 0E (after the lead approves Ext, before B3 starts)

Ext §8, items 1-8, as written there, with the golden table already in place (item 27 above):
- **Schema** (`schema.py`): `SailSpec.settee`, `SailSpec.cut_at_mast`, with their refusals
  (Ext §3.1, §5.2), parsed in `_parse_sail` (:1364-1424); `SparSpec.heave_to_aback`, parsed in
  `_parse_spar` (:1270-1301), refused off a lower mast and on a second mast.
- **Runtime** (`parts.py`): `Sail.settee`, `Sail.cut_at_mast`, `Sail.yard_lowered`,
  `Spar.heave_to_aback`, plain class defaults; `Sail.curve_class` widened to `"gaff"` for a sail
  cut at the mast.
- **`Ship.under_bowsprit(part)`** (`ship/graph.py`, beside `mast_of` :174-182), defined, not
  called.
- **Runner** (`evolutions/runner.py`): `class: settee` in `_check_applies` (:566-); a
  `wanted_sheet(sail)` function in `_env`'s expressions (:605-686).
- **Served** (`api/queries.py`): `settee` and `cut_at_mast` in `_sail_entry`, `yard_lowered` in
  the snapshot's sail (:179-), each only when true.
- **Fixtures** `tests/rig_fixtures.py`: `frigate_with_mizen_yard()`, `brig_with_settee()`.
- **Guards** in `tests/test_rig_classing.py`: no file carries `settee`, `cut_at_mast`,
  `heave_to_aback`, a `lateen_yard` or a yard rooted at a bowsprit; the three keys' refusals; each
  fixture loads.

Stage 0E touches `schema.py`, `parts.py`, `graph.py`, `runner.py` and `queries.py`, none of which
has an open owner before B3 starts (§4.2).

### 3.3 Stages 0b, 0c, 0d (the ships designed later)

At the opening of each later ship's window, after the fresh merge, the stage-0 agent lays what
her design names as inert keys and hooks, checked as §3.4. What stage 0 already holds for each:

| Ship | Module (stub in stage 0) | File proposed | Description key (rank, in stage 0) | Vessel type (`ship.rig`; the far rig word) | What her stage 0 may add |
|---|---|---|---|---|---|
| *Prince de Neufchatel* | `tools/ships/neufchatel.py` | `data/ships/hermaphrodite-brig.yaml` | `hermaphrodite brig` (2; "brig" inside it: D15(a)) | "hermaphrodite brig"; "a brig" (D15(a)) | D10(a)'s spar key (schema and `Spar`, inert), if the lead agrees (§13.1); the `nations:` block (§12.1), if ruled in |
| *Bellerophon* | `tools/ships/bellerophon.py` | `data/ships/seventy-four.yaml` | `seventy-four` (4) | "ship"; "a ship" | the bill-by-deck keys (Bel §13.1 answer 9) and any `DECK_WORDS` word; the flag's place (answer 10) |
| The bilander | `tools/ships/bilander.py` | `data/ships/bilander.yaml` | `bilander` (1; D16(a)) | "bilander"; her design's | anything beyond stage 0E her design names |

A later design may rename a file or a key. Her stage 0 then renames the rows in the same
commit. The module keeps the name stage 0 gave it in `SHIP_MODULES`, since
`tools/gen_ships.py` is B8's after stage 0 (§4.1).

### 3.4 The checks (each stage-0 commit)

By an agent that did not write it:
- the eight files byte-identical (`tests/test_ship_particulars.py:555-581`, two-way);
- the golden classing table (and in 0E the key probe, the refusals, the fixtures);
- the fast tier green; `tests/test_pivot_gun.py`, `tests/test_magazine.py`,
  `tests/test_ships.py`, `tests/test_captains.py`, `tests/test_brains.py` and
  `tests/test_view_geometry.py` (Node) green;
- every caller of `.fit(` read against item 12;
- a diff read for any reach beyond its list: no behaviour, no pin, no `world.ship` or
  `CrewedWorld` read that the Hull does not keep, no model or vendor name.

## 4. File ownership and contracts

### 4.1 The owners

| Owner | Owns (edits only these) |
|---|---|
| **Stage-0 agent** | every file of §3.1, §3.2 and §3.3, at its commit; `freesail/ship/schema.py` for the whole package (a later need goes back to a stage-0 commit) |
| **B1, the *Indefatigable*** | `tools/ships/indefatigable.py`; `tools/ships/mizen_yard.py` and `tools/ships/spritsail_yards.py` (at stage B; Ext §9.3); `data/ships/sixty-four.yaml` and `razee-44.yaml` (generated); `data/people/sixty-four.yaml` and `razee-44.yaml`; `tests/test_indefatigable.py` (new); in her window, `freesail/world/ships.py`'s rows `sixty-four` and `razee` with their words (Indf §8) and appends to `tools/ships/period.py` |
| **B2, the *Neufchatel*** | `tools/ships/neufchatel.py`; her file and her people file; `tests/test_neufchatel.py`; in her window, her `world/ships.py` rows and `period.py` appends |
| **B7, the *Bellerophon*** | `tools/ships/bellerophon.py`; `data/ships/seventy-four.yaml`; her people file; `tests/test_bellerophon.py`; `tools/pace.py` (her mode); in her window, her `world/ships.py` rows with the words "a ship of the line", and the three assertions they move (`tests/test_ships.py:99`, `:188`; `tests/test_world_orders.py:98`); `period.py` appends; the files her bill by deck needs (`crew/quarters.py` and the orders her design names), taken after B3's merge where they are B3's; `world/captains.py` if her design takes a rank-4 rule for the frigates (Bel §7) |
| **B4, the bilander** | `tools/ships/bilander.py`, `tools/ships/settee.py`; `data/ships/bilander.yaml`; her people file; `tests/test_bilander.py`; in her window, her `world/ships.py` rows |
| **B3, the engine** | `freesail/ship/parts.py` and `ship/graph.py` (after 0E); `physics/sails.py`; `evolutions/scripts.py`, `trim.py`, `runner.py`; `orders/verbs.py`, `storm.py`, `orders/__init__.py`, `navigation.py`; `combat/hits.py`; `data/evolutions/` (the ten new files); `data/vocabulary.yaml`; `tests/test_lateen.py`, `test_bowsprit_yards.py`, `test_settee.py`; `tests/test_driver.py` (step B3.5, the driver, if Ext §17 is taken); `data/sail_classes.yaml` and `tests/test_sails.py:65-74` only under D44(c), the lead's (Ext §5.10) |
| **B5, the viewer** | `client/projection.js`, `client/shipview.js`, `client/style.css`; `tests/test_view_geometry.py`; `tests/test_pictures.py` only for a threshold that moves; the screenshots |
| **B6, the scenarios** | `data/scenarios/` (the four new files); `tests/test_scenarios_75.py` (new); `world/scenarios.py` only if the lead rules in D48's third way (Indf §11.1) |
| **B8, the gun deck and the sub-types** | `tools/gen_ships.py` after stage 0; the eight existing files (generated); `freesail/ship/charges.py`; `freesail/combat/ports.py`; `freesail/combat/guns.py` after stage 0 (§7.2: the gun run in, the named gun dropped with a line); `api/action_readings.py` (the guns' reading's "ports shut", :548-); `world/captains.py` (`ROLES` only) and `world/service.py` (`ROLE_SERVICE`, :54-) until SW-4 merges; `data/captains/indiaman.yaml`, `revenue.yaml` (new); `world/ships.py` at the boundary after B1 only (§4.2); `tests/test_magazine.py` (:59, :61); `tests/test_pivot_gun.py` (only if the arc moves); `tests/test_ships.py:103` (only if §8.4 is ruled in); `tests/test_profiles.py`, `test_lee_ports.py`, `test_subtypes.py` (new) |
| **The integrator** | the merges into the package's branch; the fresh fetch and merge; the regenerated files of §4.4's last row; Phase 5: `tests/test_known_truths.py` (the truths moved in by number), `tests/conftest.py` (`SLOW_TESTS`), `docs/dev/TuningNotes.md`, `docs/TechnicalSpec-M7.md` §27 as built, the primer's ships chapter, `docs/agents/Harness.md` (the two events) |

**Plainly:** the brief's heading names `world/ships.py`, `captains.py`'s `SIZE_RANK`,
`schema.py`, the generator, the files, the scenarios, the tests and the docs. The lead's
rulings bring in the rest: the viewer (`client/`), the lee ports (`combat/`, `api/`), the
engine extensions (`evolutions/`, `orders/`, `physics/sails.py`'s lookups), and the roles of
the brief's item 4 (`world/brains.py`, `regimes.py`, `squadrons.py`, `service.py`, and
`captains.py` beyond `SIZE_RANK`). Each is named in this table for the lead.

### 4.2 Files that pass, and when

A file passes only at a merge into the package's branch, never while two owners are open.
- `freesail/world/ships.py`: stage 0; then B1 in her window; then **B8 at the boundary after
  B1's merge** (SW-4's sub-type rows, and §8.4's move if the lead rules it in); then B2, B7 and
  B4, each in her window.
- `freesail/world/captains.py`: stage 0; B8 (`ROLES`) until SW-4 merges; B7 in her window if her
  design takes the rank-4 rule.
- `tests/test_ships.py`: B8 at the boundary after B1 (only `:103`, only if §8.4 is ruled in);
  B7 in her window.
- `tools/ships/period.py`: stage 0; then the ship builder of each window, appending.
- `tools/ships/mizen_yard.py`, `spritsail_yards.py`: B1 at stage B; then B7 or B4 in her window
  if she needs an extension.
- `freesail/ship/parts.py`, `graph.py`, `evolutions/runner.py`, `api/queries.py`: stage 0, then
  stage 0E, then B3 (`queries.py` has no owner after 0E).
- Anything B7's bill by deck needs from B3's files: after B3's merge.
- `freesail/world/scenarios.py`: B6, only if D48's third way is ruled in, merged before stage
  0b; then stage 0b, only if the `nations:` block is ruled in (§12.1).

**Nobody touches** after stage 0: `core/world.py` (unless §12.1 is ruled in, at 0b),
`core/replay.py`, `crew/` (but B7's `quarters.py`), `world/hulls.py`, the books, the consent
files, `BUILD_NAME`, any existing file under `data/ships/` but through the generator.

### 4.3 What each builder runs at the end of a step

Every builder: `py tools/gen_ships.py <scratch>` from the tree root, `cmp` of every committed
file not meant to change against the scratch, and `load_ship` on its new files (Indf §13). The
fast tier once on its final tree, and the slow tier of the files it touched (§2.5).

### 4.4 Interface contracts

| Provider | Contract the others may assume |
|---|---|
| Stage 0 | `build(out_dir: str) -> None` called after `smack(out)` and the alias; `import gen_ships as g` gives the running script; `g.hull_profile`, `g.broadside_pair(..., deck=, round_to=)` and its kin, `g.exercise_allowance(n, decks=)`; `period.py`'s constants; §5.1's form; `profile.py`'s readings; `DECK_WORDS`; `"unarmed"`; the keyed registries of §3.1 items 23-25; `CHARGE_TABLE_LB`; `ports.update`; `Sail.curve_class` |
| Stage 0E | Ext §7's table: the keys, fields, predicate, runner hooks and served fields, each inert until B3 |
| Every ship builder → B5, B8 | a `profile` in §5.1's form in each file; every port gun's `(x_m, height_m)` equal to one triple of its deck's `ports_m` to the centimetre, its `deck` named; every height above the file's waterline; the mast ids `fore.`, `main.`, `mizzen.` (two z's: the mizzen top's men, `crew/hands.py:104-108`) |
| Every ship builder → B6 | her description key and file, her fits and default, her date range, her wardroom file |
| B1 → B7, B4 | `mizen_yard.py` and `spritsail_yards.py` as Ext §9.3 gives them: pure, importing nothing from `gen_ships`, each asserting its geometry at generation |
| B3 → B1, B7, B4, B5 | Ext's file contracts (§3.4, §4.1, §5.1) and the behaviour on the keys; no existing file's behaviour moved (the golden table) |
| B8 → all | SW-1: `charge_lb` gives Table No. 29's figure for every calibre of the game; SW-4: a description's `fit` and `roles` read from its file, `pivot_arc_from_rig(b, x_m, margin_deg=5.0)` for any pivot (§9.2), the roles `indiaman` and `revenue`; SW-5: `ports.update` by §7's rule, `Battery._shut` the shut port guns' ids |
| B5 → the owner | screenshots: every ship before and after the profile; the razee and the 64 under D18 (a) and (c) (`datum_z` changed in a scratch regeneration, never committed); each rig drawing in each state |
| Every builder → the integrator | its truths drafted and measured in its own test file under its reserved numbers (`test_truth_7_NNN_<the claim>`), using only the names the Hull keeps (`world.ship`, `world.motion`, `world.sea`, `world.clock`), never `isinstance(..., CrewedWorld)`; its tuning notes as text in its branch's report |
| The integrator → all | at each merge, the generator run and every file it writes compared; a file moved by another builder's merged change (a shared helper or note) committed regenerated in that merge, with the reason. Ship files are never edited by hand |

---

# Part B: the shared work

## 5. The hull profile, in every file (SW-2 for the eight; each ship's builder for hers)

The brief asks for "a dozen sourced points for the sheer, the stem, the stern, the wales and
the port sills, beside the guns' `x_m` and `height_m`", so that package 81 draws real ports
from data. The lead's ruling adds the drawing (§6) and the lee port (§7) reads the same points.

### 5.1 The form

Under `hull`, after `rudder`, so that the existing keys keep their order and bytes. Written by
`g.hull_profile` alone, each list of points on one line.

```yaml
hull:
  ...
  rudder: {...}
  # The hull's profile: x forward of midships, z above the file's waterline (the sources' lines)
  profile:
    rail_m:      [[x, z], ...]                # required: the top of the side, taffrail to stem head
    breadth_m:   [[x, hb_water, hb_rail], ...]  # required: the half-breadths at the water and the rail
    keel_m:      [[x, z], ...]                # K, the post's heel to the forefoot
    stem_m:      [[x, z], ...]                # the stem's fore edge, low to high
    stern_m:     [[x, z], ...]                # the post, the counter, the taffrail, low to high
    wales_m:     [[x, z_lower, z_upper], ...] # the main wale
    section_m:   [[z, half_breadth], ...]     # the midship section, plank on
    decks_m:     {upper: [[x, z], ...], quarterdeck: [...], ...}   # each deck at side, over its extent
    ports_m:     {upper: [[x, sill_z, half_breadth], ...], ...}   # one side's ports, by deck
    port_size_m: {upper: [width, depth], ...}
```

- **Every z above the file's waterline**, taken as the load line its sill source states, so the
  profile does not depend on D18, and the viewer, which draws the water at z = 0, takes it as it
  stands. A source's freeboard at load is taken at the file's line whatever the file's draught;
  the notes record a difference (Indf §3.1; the shared draft S2).
- **Ports as triples** (Indf §3.1). Each is a port's x, its sill, and the side's half-breadth at
  the sill, so that the lee port reads a lookup with no geometry of its own (Bel §13.1 answer 7),
  and 81 draws the ports from the triples and `port_size_m`. A chaser's port is a triple of its
  deck at the chaser's x. A pivot and a rail gun have no port.
- **`breadth_m`** (the shared draft) is the plan's half-breadths by station. The viewer cannot
  draw a true side without them; `section_m` gives the midship section only.
- **The deck words** are `DECK_WORDS`, shared with the gun's `deck` key and the 74's bill. The
  razee's gun deck is `upper` (ZAZ2374's title; Winfield 1793-1817 p. 99: Indf §3.1). A frigate's,
  a sloop's and a cutter's single gun deck is `upper`.
- **Plainly:** `breadth_m`, `decks_m` and the triples' half-breadth go beyond the brief's list.
  The drawing and the owner's lee-port rule need them; each is a few points.

### 5.2 The schema's refusals (in words, stage 0)

- A key not in `PROFILE_KEYS`, or a deck word not in `DECK_WORDS`.
- `profile` without `rail_m` and `breadth_m`.
- A point that is not two numbers (three in `breadth_m`, `wales_m` and a port triple).
- x not increasing in `rail_m`, `breadth_m`, `keel_m`, `wales_m`, a deck or a deck's ports; z
  not increasing in `stem_m` and `stern_m`.
- A deck at side above the rail at its x; a sill at or above the rail, or below its deck, at
  its x.
- A half-breadth not positive.
- A `ports_m` or `port_size_m` deck that is not in `decks_m`.

The equality of a port gun and its triple is a test (truth 7-185) and the generator's assertion,
not a refusal: a hand-written file may carry guns between ports.

### 5.3 The generator

- `g.hull_profile(rail, breadth, **parts)` returns the mapping; each ship function or module adds
  it as the last key of its hull dict, with one note per key in `hull_notes`.
- **Gun heights.** SW-2 passes, for every port gun of every fit of the eight files,
  `deck=<its deck>`, `height_m=sill_at(profile, deck, x)` and `round_to=0.01`. **No gun's `x_m`
  moves**: an `x_m` is read by the quarters and the divisions (`crew/quarters.py:437-460`), a
  height nowhere in the engine today (grep: `parts.py:507` copies it, nothing reads it).
  Swivels and pivots take `rail_at(profile, x)`. A new ship's module reassigns or passes the
  port's own x and sill (Indf §5.2).
- **`PORT_SILL_M`** (:3615, judgement) then has no caller among the eight. It stays only if a
  new ship's builder uses it for a deck the sources leave open, and says so.

### 5.4 The eight files' sources (SW-2; read by the shared draft unless marked)

| File | Rail and decks | Stem, stern, wale, half-breadths | Sill | Still to read |
|---|---|---|---|---|
| frigate-36 (*Amazon*) | Steel 1805, the bodies of "the frigate of 36 guns and 877 tons" (OCR `docs/references/steel/steel-1805-naval-architecture-1822-printing-ocr.txt:27071-27170`, garbled); Steel's rules for the top-timber and load lines (`:15178-15187`) | Folio I's 36 (read); Winfield 1793-1817 p. 143's draughts; Steel: the wale's lower edge a few inches above the load line (`:15190-15193`) | **Folio I: 7 ft 8 in above the water at midships, 2.34 m**, at a load draught of 17 ft 4 in / 18 ft 4 in (read, page image) | Steel's bodies table for the 36 from its page image. **Plainly:** Steel's 36, not *Amazon*'s own lines (not reached) |
| brig, merchant-brig (*Harpy*'s hull) | the *Raven* brig's contract of 1804 (Steel 1805 pp. lix ff., OCR `:44331-44390`): waist, deck ends, height of breadth, moulded breadths; scaled from 100 ft to 95 ft (judgement) | the same; Winfield's draughts | the *Raven*'s sills 16 in above the deck; Steel p. 124, "sloops, cutters, &c." four to five feet above the water (`:8268-8271`): **1.22-1.52 m against the file's 2.1** | the load line the *Raven*'s figures stand on |
| topsail-schooner, privateer-schooner (*Lynx*'s draught) | Chapelle 1930 fig. 17, the *Musquidobit* draught (held scan, p. 82) | the same | Spider's 3 ft 5 in above the water, 10 in above the deck (Chapelle pp. 166-167; the file's own, `gen_ships.py:4152-4155`) | the plate's sheer and stations, measured |
| cutter (*Sherbourne*) | Steel 1805, "a cutter, on a new construction, of 273 tons" (the page image; the OCR at `:27779-27841` misreads 278: `ships-design/pages-steel-1805-bodies.md`), scaled (judgement) | Fincham 1843 p. 67 (the file's own); Steel's rule | Steel p. 124's four to five feet; the file's 1.5 m within it | the bodies table's page image |
| lugger (*Éclair*) | RMG ZAZ6306, the gun lugger taken off afloat, 2 July 1795 (catalogue: `VesselReferences-2026-10.md:85`) | the same | the same; Steel p. 124 failing it | the 1280-px image, measured (`ships-design/pages-zaz6306.md`; Crown copyright, never copied) |
| smack (*Culloden*) | Chapman 1768 Pl. LIX No. 3; Steel 1805's coasting sloop of 60 tons (OCR `:28504-`), scaled | the same | no guns by default (§9.1) | Chapman's plate |

Where a point is not yet measured it is written as judgement in its note, never left out
silently. **Plainly, for the lead:** the frigate's file draws 15 ft mean (judgement,
`gen_ships.py:1525`) against Steel's 36's 17 ft 10 in mean (Folio I); the profile takes Steel's
freeboard at the file's line, and her draught is recorded, not moved, since it moves every
sailing pin she has.

**Measured here** (`shut.py`, heel alone, half the beam, `PORT_SHUT_M` 0.3048 m,
`combat/shot.py:116-120`):

| File | Sill now | Shut now | Sourced sill | Shut then |
|---|---|---|---|---|
| frigate-36, upper deck | 2.4 m | 21.0° | 2.34 m | 20.4° |
| frigate-36, quarterdeck and forecastle | 4.5 m | 45.8° | the deck + the port's sill (to read) | — |
| brig, merchant-brig | 2.1 m | 24.7° | 1.22-1.52 m | 12.3-16.4° |
| cutter | 1.5 m | 24.3° | 1.5 m | 24.3° |
| privateer-schooner | 1.0 m | 11.0° | 1.04 m | 11.6° |
| the razee, lowest (Indf §3.4) | — | — | 1.98 m | 14.5° (on 6.67 m at the sill) |
| the 64, lowest (Indf §3.4) | — | — | 1.53 m | 10.6° (on 6.67 m) |

The side's half-breadth at the sill, narrower than half the beam, raises each figure a little.
The brig's sill is the largest move among the existing files; where in Steel's band it lands
is B8's measure of the *Raven*'s figures.

### 5.5 D18, proposed: (a) for every file (open, the owner's)

The owner's measure: "whichever choice gives the best impression in the viewer and matches the
sources". The lead's reading: with the profile drawn, the deck height serves the physics and the
spar heights alone.
- `deck_height_m` stays the uppermost continuous deck at midships, the datum of every spar
  height and every `corners_m` (`physics/sails.py:1560-1566`; `client/projection.js:275`).
- **A new file** takes it from her profile's deck at x = 0: the 64's upper deck 3.22 m, the
  razee's gun deck 1.39 m (Indf §2.1), the *Neufchatel*'s deck at side about 1.16 m (Neuf §2.9);
  the 74's and the bilander's from their profiles.
- **An existing file** keeps its datum (the frigate's 1.8 m, the brig's 1.5 m). It is read by the
  deck's wind (`physics/sails.py:349`), the spars' windage (:1562), the hull's wind
  (`physics/hull.py:391`), the lookout's eye (`world/lookout.py:215`) and the readings
  (`api/readings.py:382`), so moving it moves pins for no gain in the sources.
- **The viewer** draws the side, sheer, decks and wales from the profile, each lower mast down
  to the drawn deck at its x (its head unmoved) and the bowsprit's heel from the stem head (its
  tip unmoved) (§6).

Why (a) over (c) for the razee: her arrangement, a continuous gun deck with quarterdeck and
forecastle joined by gangways, is the frigate-36's, so the same rule (Indf §2.2). What (c) buys
reduces to the deck wind's eye 2.3 m higher; its other two gains (the bowsprit where it stood,
the side drawn to her rail) come with the drawn profile under (a). Under (b) the 64's datum falls
to her lower deck and every height of hers changes meaning. **The owner chooses on B5's
screenshots** of the razee beside the 64 and the frigate-36, abeam to leeward, under (a) and
(c) (one figure, `datum_z`). Under (c), **plainly**, the razee would depart from the
frigate-36's convention, and both files and the tuning notes would say so.

### 5.6 Pins, tests, order

- **Pins:** none. The heights are read only by the lee port (SW-5) and the profile only by the
  viewer (B5). `tests/test_server.py:139-160` checks the graph's hull as a superset, so the added
  key stands.
- **Tests** (`tests/test_profiles.py`, B8): every file carries a profile whose rail stands above
  its decks and sills; every port gun stands on a triple of its deck within 0.01 m and names it;
  each existing file's sill in its source's band, the source in a comment
  (`tests/test_ship_particulars.py:93-104`'s form).
- **Order:** SW-2 after stage 0. B1 writes her two profiles from her first commit, through the
  same helper.

## 6. The viewer draws the profile (B5)

**The drawing** (`client/projection.js`):
- `/api/ship` serves `hull["profile"]` (stage 0).
- `hullFigures(hull)` (:1416-1448) keeps today's lens for a graph with no profile, so a
  hand-written file and the tests' fixtures draw as now. With a profile it calls a new
  `profileHullFigures(hull)`:
  - **stations:** the union of `rail_m`'s and `breadth_m`'s x's with a grid of sixteen between
    the taffrail and the stem head; at each, the rail's z, the half-breadths at the rail and the
    water, and the low edge at −0.8 m at 0.92 of the water's half-breadth (today's cut,
    :1432-1433);
  - **sides** (`part: side`, both): along the rail from the taffrail to the stem head, down the
    stem to the cut, aft along the cut, up the stern to the taffrail;
  - **decks** (`part: deck`): one polygon per deck of `decks_m`, at its own heights and extent,
    at 0.95 of the rail's half-breadth (judgement: inside the bulwark). The razee's open waist
    shows her gun deck below the gangways;
  - **the transom** (`part: transom`): from the taffrail down to the counter's knuckle;
  - **the wales** (`part: wale`): a band on each side, its y between the water's and the rail's
    half-breadths by height, sorted a hair nearer than its side (`DEPTH_TIE`, :1529);
  - **port bands** (`part: band`, optional): each deck's strake from the sill up the port's
    depth, kept only if the owner's screenshot check keeps it. **Plainly:** no port is drawn;
    the ports are 81's.
- **The lower masts** (:501-511): with a profile the foot is drawn at `deck_at(profile, x)` along
  the mast's rake line, the head unchanged.
- **The bowsprit** (:528-544): with a profile the heel is drawn at the stem head (or the rail at
  its x, if lower), the tip at `deck + height_m` as now. This removes D18 (a)'s one visible cost
  on the razee (Indf §12.3).
- `fullRigFrame` (:1383-1414) already holds the hull's points; nothing else in the rig or the
  physics changes.
- **The lifts of every yard** (proposed after the owner's question, 2026-10-28; Decisions, "The
  design's questions"): each `lift` line the files already carry is drawn faint from its yard's
  arm to the masthead above, at the braces' opacity, in the same step as the profile, since the
  profile changes every picture anyway. This replaces Ext §6.1's lifts on a lateen yard alone.
  The pictures' figures are measured with the lifts and without, old beside new.

**The rendering:** `client/shipview.js:58-60` draws each hull figure with the class
`"hull " + part`; `client/style.css` (:155-158) gains `.hull.wale` and `.hull.band` (an SVG
polygon with no rule fills black).

**Then** Ext §6, after each B3 step: the mizen yard and course; the yards under the bowsprit;
the settee; the settee's sheet to the profile's taffrail.

**Tests** (`tests/test_view_geometry.py`, Node): the side's top through every `rail_m` point
within a millimetre; the transom's top at the taffrail; each deck at its points; a lower mast's
foot on the drawn deck and its head unmoved; the bowsprit's heel at the stem head and its tip
unmoved; a graph with no profile drawing today's figures point for point; every file drawing a
closed side with no NaN. Standing: the fixed frame across states (:181-203, :620-658), the
cutter's hull ends (:445-478), a yard at its hoist (:630), the lowered lug (:778-781).

**The pictures** (`tests/test_pictures.py:57-59`: `BLANK_STD` 8.0, `DARK_LEVEL` 110,
`DARK_FRACTION` 0.001): a taller hull adds dark pixels (the side #4a3d31, mean 61), so none is
expected to move. B5 measures the frigate's picture before and after with
`FREESAIL_KEEP_PICTURES` (:186-189) and records the standard deviation and the dark fraction old
beside new. A threshold is re-pinned only if one fails, old beside new.

**Screenshots** for the owner: all eight ships and the two new files, abeam to leeward, on the
quarter and ahead, furled and under plain sail, at 800 × 600 in the built-in pane, beside the
same views at this head; the razee and the 64 under D18 (a) and (c).

## 7. The lee ports (B8: L1 = SW-2, then L2 and L3)

### 7.1 The rule

For a gun placed broadside, bow or stern (`PORT_PLACES`; a pivot and a rail gun fire over the
rail: `docs/design/Proposal-PivotGun.md` §4.4):
- **The dip:** the heel toward the gun's side plus the roll's amplitude, never below nought. The
  side she heels to follows `_is_lee` (`combat/guns.py:1032-1040`); the other side's dip is the
  roll less the heel.
- **The sill lowered:** the gun's `height_m` (its port's sill) less the side's half-breadth at
  the sill times the sine of the dip. The half-breadth is `half_breadth_at_sill(profile,
  gun.deck, gun.x_m)`, held once a gun; with no profile or no deck, `firer.half_beam_m`, the beam
  over two (`combat/action.py:221`).
- **Shut** when the sill lowered is `PORT_SHUT_M` (0.3048 m, `combat/shot.py:65`) or less:
  `shot.lee_port_shut(sill, dip, half_breadth)` exactly (:116-120), today called nowhere.
- **Opened again** when the sill lowered stands `PORT_REOPEN_M` (0.15 m, six inches; judgement)
  clear of that, so that a port does not flicker in a gust.
- **The roll is the ship's own:** `firer.roll_deg`, built from `world.motion` (`action.py:218`),
  a field the Hull keeps (`world/hulls.py:52`, `PER_SHIP_FIELDS`); `ship.extra["motion"]` is the
  same `Motion` (`core/world.py:655`). A World that keeps no sea gives a roll of nought (map-engine
  §10 item 4); a crewed ship's World keeps none (`world/crews.py:312-330`) until 84 gives each
  hull its sea. A truth on the roll uses the player's ship. **Plainly:** the owner's answer
  (Bel §13.1 answer 7) asks that each ship have her own roll. Each reads her own World's
  motion and never another ship's, but a crewed ship's roll stays nought until 84 gives her a
  sea; building her a sea here would reach into 84's World.
- **Plainly:** the owner's rule speaks of the lee port. The same arithmetic covers the weather
  side, whose dip is the roll less the heel. On today's files it needs a roll 20° beyond the
  heel, so it moves nothing; it is said for the lead.

### 7.2 The wiring (B8 fills stage 0's hooks)

- `ports.update(battery, firer)`, once a tick at the head of `Battery.tick`: each port gun's
  state against the rule's two lines, kept in `Battery._shut`. The log, once a change of state a
  deck and side: `guns.ports_shut` ("The lee lower-deck ports are shut, the sea at their sills")
  and `guns.ports_opened`, the deck named by its word.
- `wants_work`: a shut gun is not wanted run out; a gun run out when its port shuts is run in
  (judgement: the lid lowered on a gun housed). Loading goes on; a loaded gun stays loaded.
- `_fire`: a shut gun does not fire; one asked for by name is dropped with a line ("The No. 3
  larboard gun's port is shut; the sea is at its sill.").
- The guns' reading (`api/action_readings.py:548-`) says "ports shut" while any are.
- **The far fight** (`combat/far.py:97-121`) is untouched: a far ship has no heel. The far fight
  is 74's.
- **Pace:** a sine and a compare a port gun a tick; truth 51 and the crewed floor are measured
  after L2.

### 7.3 The steps and the proof

| Step | Change | Pins expected |
|---|---|---|
| L1 (= SW-2) | the sourced sills and the profile in every file | none: no reader yet |
| L2 | `ports.update` on heel alone (the roll held at nought) | any action whose firing ship heels past her new shut heel with that side engaged |
| L3 | the roll's amplitude added | any action with a sea, on the player's ship |

- **The candidates**, run at the commit before L2, at L2 and at L3: truths 7-133 onward (the
  first action, the frigate's actions); 7-161 to 7-171 (86's); the privateer schooner's truths
  (`tests/test_known_truths.py:9176` on); `tests/test_pivot_gun.py`, `test_practice*.py`,
  `test_magazine.py`, `test_ordnance.py`.
- **What the measures say:** the most heel while firing in the first action was 2.7° (the
  cutter) and 6.2° (the *Renard*), and on the gate's whole day the frigate's 4.0° (Bel §6.1
  P6, observed): below every new
  shut heel but the privateer's 11.6° and perhaps the brig's 12-16°. The movers, if any, are
  expected in the privateer's and the brig's actions, and under L3 in a sea (judgement).
- **For each moved pin** the tuning notes give the old figure beside the new, the reason, and
  **the bisection**: the commit that moves it (L2 or L3); then, within L2, the same run with the
  gate on and the file's old heights (a scratch copy, never committed), which separates "the
  gate" from "the sourced sill".

## 8. The sub-types as fits and roles (B8, SW-4)

### 8.1 What a sub-type is

A sub-type is a description, which names a file (`world/ships.py:163-204`). It gains two
optional words, written **in the file's own `ship.descriptions`** by the generator: `fit`, the fit
a far ship of it carries when the scenario names none, and `roles`, the roles a scenario may give
her, the first the one the intent rules give. A scenario's far ship may say `role:`; it must be
one of her description's roles and of `ROLES` (`world/captains.py:133-141`), or the load refuses
it. "In their reasonable degrees" is that bound: the fit among her file's fits (and `unarmed`),
the role among her description's, the nation, colours and intent as now. A test proves every
description's fit is a fit of its file. A far vessel takes her description's `fit` only where
it is not her file's default: `Vessel.to_dict` writes a non-empty `fit`
(`world/ships.py:974-975`), so a default set on every far frigate, brig-sloop, cutter or
privateer would move their pinned forms with no change in their guns.

### 8.2 The table

| Description | File | Fit (default) | Roles | New |
|---|---|---|---|---|
| frigate | frigate-36 | amazon class 1795 | kings-ship, commodore | words in the file |
| brig-sloop | brig | diligence class 1796 | cruiser, kings-ship, commodore | words |
| merchant brig | brig (merchant-brig proposed, §8.4) | merchant, if §8.4 is ruled in; else none (`brig.yaml` has no merchant fit) | merchant, packet, indiaman | §8.4 |
| schooner | topsail-schooner | unarmed | merchant | words |
| privateer schooner | privateer-schooner | long tom | privateer | words |
| cutter | cutter | carronades | cruiser, kings-ship | words |
| revenue cutter | cutter | long guns | revenue | row, **role** |
| hired armed cutter | cutter | long guns | cruiser | row |
| coasting cutter | cutter | unarmed | merchant | row |
| lugger | lugger | unarmed | fisherman, merchant | words |
| privateer lugger | lugger | gun lugger 1795 (§9.1) | privateer | row |
| smack | smack | unarmed | fisherman | words |
| armed Indiaman | none in 75 | — | indiaman | **role** |

The new rows and their lookout words ("a revenue cutter", "a hired cutter", "a hired armed
cutter", "a coasting cutter", "a privateer lugger") go into `world/ships.py` at the boundary after
B1's merge. Rank 1 each in `SIZE_RANK`. "revenue" is already a man-of-war word
(`captains.py:190-198`), so a privateer keeps away from a revenue cutter made out. The new ships'
descriptions are their own designs' (D15, D16).

### 8.3 The two new roles

- **`indiaman`** (`data/captains/indiaman.yaml`): the merchant's book with the figures of a ship
  that fights when brought to: `yields_when_caught` false, `engage_nm` 1.0,
  `engage_range_cables` 4, `morale_start` 0.65, `strike_below` 0.25, `engage_side` weather,
  `board_odds` 0 (all judgement against `merchant.yaml`). The accounts: Dance's China fleet
  against Linois, February 1804 (James vol. 3 pp. 249-251); the *Windham*, *Ceylon* and *Astell*,
  July 1810 (vol. 5). The brief: an Indiaman is not a merchantman who strikes at the first telling
  broadside. **Plainly:** no Indiaman hull is in this package. The role is built and proven on the
  merchant brig's hull (truth 7-191); Steel 1805's East India bodies (OCR `:27842-28075`) are a
  later ship's.
- **`revenue`** (`data/captains/revenue.yaml`): the cruiser's book, with every lugger, smack and
  coaster in reach investigated and spoken, a privateer of her size engaged, a man of war hauled
  off from, no blockade station. Thresholds judgement. **Plainly:** the smuggler and the search
  are not modelled, so the role differs from the cruiser's in whom she speaks.
- `ROLES` and `ROLE_SERVICE` (`world/service.py:54-`) gain both. `tests/test_captains.py:87` and
  `:134` run every book on the four ships, and `tests/test_service.py:73` asserts the two sets
  equal; both must pass.

### 8.4 Found on the way: the merchant brig sails the brig-sloop's guns (for the lead)

`DESCRIPTIONS["merchant brig"]` names `brig.yaml` (`world/ships.py:187-191`), whose one fit is
sixteen 32-pounder carronades and two 6s with 121 men. So every far merchant brig carries the
brig-sloop's broadside in the far fight (`combat/far.py:97-121`) and musters 121 crewed.
**Proposed, for the lead's ruling before it is built:** the description sails `merchant-brig.yaml`
(the same hull and rig byte for byte, so the same polar), with her 16 men and four 6s;
`SHADOW_FILES` (:283) becomes redundant; a trader cutter takes "coasting cutter". It moves every
pin with a far or crewed merchant brig (the convoys, the trade trials) and
`tests/test_ships.py:103`, each old beside new on its one commit. If ruled out, the table keeps
`brig.yaml` and the fault is recorded. **The packet:** a packet fit on the merchant brig (a few
long 6s, judgement) is cheap, but her company of 16 is short of a packet's (memory, about 28,
UNVERIFIED) and a fit cannot change a complement (`FIT_KEYS`, `schema.py:215-223`); the lead may
prefer to leave the packet's description for her own hull.

## 9. Every file's armament, bill and marines (B8, SW-4)

### 9.1 The topsail schooner, the lugger and the smack

`armament.default: unarmed` (stage 0) lets each carry fits for the editor and sail unarmed:

| File | Default | Fits (the type's records) | Bill |
|---|---|---|---|
| topsail-schooner | unarmed | "letter of marque": *Lynx*'s six guns and forty men (Chapelle p. 82; the long 6s judgement); "musquidobit 1813": eight 18-pdr carronades and two 6s (Winfield 1793-1817 p. 335; her naval company of 50 against the file's 40, said in the note) | trimmers by station, helm 1, powder 1, filling reckoned, small arms and boarders as the privateer's |
| lugger | unarmed | "gun lugger 1795": *Éclair*'s three guns (ZAZ6306's caption; the calibre's second digit unread, judgement until the image is read) | her stations, judgement |
| smack | unarmed | "culloden 1746": two small long guns (Charnock vol. III p. 274; calibre judgement) | judgement for eight men |

No battery is made from an unarmed default, and a ship with no guns never engages (70).
`tests/test_ships.py:146-158` pops the armament and the bill from both schooner files, so its
claim stands. To measure: a scenario that beats to quarters in an unarmed schooner meets the
file's bill in place of the reckoned defaults (`crew/quarters.py:111-112`).

### 9.2 The pivot's arc from its own rig

`pivot_arc_from_rig(b, x_m, margin_deg=5.0)` (B8, in `gen_ships.py`) computes the open arc from
the file's spars, as `Proposal-PivotGun.md` §4.2 proposes: each lower mast's x, the shrouds'
channel abeam and aft of it, the topmast backstays further aft, the stays and bowsprit on the
centreline, and the rail's half-breadth at each from the profile. The channels' lengths and the
backstays' places come from Steel 1794 vol. I and Luce 1866, cited by page; the arc and its
working go in the gun's note. The privateer schooner's pivot takes it. **Plainly:** the brief's
"Dolphin's arc" belongs to HMS *Dolphin* of 1836, which has no file in 75; her arc can come only
from this rule when her file does.

### 9.3 The fillers as posts: left to 77 (the lead's call)

**Plainly:** against the brief item 5's "the fillers as posts where 73 or 86 left them as a
judgement", by the brief's own "77's unless 75 takes them first": making the gunner's crew and
the quarter gunners posts moves every armed ship's muster draws and quarters (practice and
resupply's decision 5), muddies the lee port's bisection, and belongs with the 74's bill by deck
and 77's evolutions. Each new file's bill writes `filling` by Falconer's rule (`filling_party`,
`gen_ships.py:3665-3669`; for the razee and the 64 it gives the Regulations' quarter gunners, 11
and 16: Indf §5.4), and the new wardroom files name the gunner's crew in their outlines.

### 9.4 The marines

The kit is the nation's already (`data/nations.yaml`; `Nations.marines_kit_of`,
`world/nations.py:149-158`): the *Neufchatel* under American colours takes the basic kit, the
74 and the razee the British. The detachments are each file's `crew.stations.marines`; the
frigate's 40 and the brig's 20 stay (the existing files are the lead's), their notes gaining the
nearest print (the 44-gun *Doris*'s lieutenant and 50 marines, March 1803: *Naval Chronicle* vol.
IX p. 245; Bel §4.4). The new ships' detachments are their designs' (Indf §6).

### 9.5 `privateer-schooner.yaml`: kept beside the *Neufchatel*

The owner's answer on file is against making her a fit of `topsail-schooner.yaml` (the trade
trial: the armed Speedwell made the merchant schooner engage). The *Neufchatel* is another hull,
of 328 tons and rank 2; replacing the privateer schooner would turn every "privateer schooner"
of the scenarios (`convoy-six.yaml`) into a brig of rank 2. What 75 gives her: her profile
(§5.4), her arc (§9.2), her fits from the type's records ("long tom" kept as the owner's loadout,
its note citing the type; "letter of marque" re-cited to *Lynx*'s six guns and forty men), and
her PROVISIONAL marks off where a figure is now sourced. Her wardroom file stays absent: one
would bind outlines where none bind today, and move her pins.

## 10. Table No. 29 (B8, SW-1)

**The table** (the Regulations 1806, 1808 printing, Table No. 29, read on the page image; the OCR
has its title at `docs/references/admiralty/regulations-and-instructions-1808-ocr.txt:27498-27502`
and lost its figures). Service charges, cylinder powder, one shot:

| Guns (pdr) | 42 | 32 | 24 | 18 | 12 | 9 | 6 | 4 | 3 | 2 | 1 | ½ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| One shot | 14 lb | 10 lb 10 oz | 8 lb | 6 lb | 4 lb | 3 lb | 2 lb | 1 lb 5 oz | 1 lb | 10 oz | 5 oz | 2 oz |

| Carronades (pdr) | 68 | 42 | 32 | 24 | 18 | 12 |
|---|---|---|---|---|---|---|
| Service | 5 lb 10 oz | 3 lb 8 oz | 2 lb 10 oz | 2 lb | 1 lb 8 oz | 1 lb |

- **Confirmed:** a long gun a third, a carronade a twelfth (`CHARGE_SHARE`, `parts.py:583`).
- **Moved:** the table rounds down where `charge_lb` (:596-599) rounds to the nearest ounce. The
  32-pdr carronade 2 lb 11 oz → **2 lb 10 oz** (the frigate, the brig); the half-pounder swivel 4
  oz → **2 oz**, a quarter of its shot (the cutter's "long guns", both of the privateer's fits);
  the long 32, 10 lb 11 oz → 10 lb 10 oz (the 74's).
- **The change:** `charges.CHARGE_TABLE_LB` filled by kind and calibre; `MAGAZINE_NOTES["charges"]`
  (`gen_ships.py:3680-3687`) and `charges.py`'s docstring cite the table in place of
  "UNVERIFIED". The comment at `parts.py:575-582`, B3's file, already points to `charges.py`
  (stage 0, item 15). The *Indefatigable*'s fits come out the same to the ounce (Indf §5.4).
- **Left out, said:** the two-shot charge (a double-shotted round draws one service cartridge,
  `parts.py:761-773`), the salute's charge, the advice to restrain double shot after twenty
  rounds. Each changes the gunnery's cycle, 77's.

## 11. The frigate-36's quarterdeck: not corrected

The owner's ruling of 2026-10-25 keeps it, marked INCORRECT against Winfield 1793-1817 p. 143
(`gen_ships.py:3819-3834`). What correcting it would move, by the generator's own rules
(measured by the shared draft):

| What | As the fit has it | Corrected |
|---|---|---|
| Quarterdeck | 8 × 32-pdr carronades (pairs 14-17), 2 × 9 (pair 19) | 8 × 9, 6 × 32-pdr carronades |
| Pieces | 40 | 44, renumbered from 14 |
| Gun crews | 176 | 192 |
| Cartridges; shot | | +474 long 9 and −158 32-pdr carronade; +432 9-pdr and −144 32-pdr |
| Filling party | 10 | 11 |
| Broadside a side, by 70's rule with every chaser | 421 lb (Indf §5.5) | about 416 lb (Indf) |

The truths that would move are 7-133 onward where the frigate fights and 86's 7-161 to 7-171,
and with them the *Indefatigable*'s broadside truth (7-188), measured against the fit as it
stands and saying so; its band holds the corrected figure too. What 75 changes there: only the
quarterdeck's sill and the guns' heights from the profile.

## 12. The scenarios' common ground (B6)

### 12.1 The scenario's nations (for the lead)

`data/nations.yaml` stands at June 1805 (`as_of: 1805-06-01`). **Proposed:** a scenario may carry
`nations: {as_of, wars, letters_of_marque, source}`; the loader validates the ids as `nation:` is
validated (`world/scenarios.py:390-401`), and the World (`core/world.py:703`) replaces the
table's wars and letters with the scenario's. Inert while no scenario carries it. **Plainly:**
`world/scenarios.py` and `core/world.py` are outside the brief's file list, so it is the lead's
to rule; the *Neufchatel*'s 1814 needs it (Britain at war with the United States), and the 74's
1815 and the bilander's 1794 are served by the 1805 table but for Spain. If ruled in, it is laid
in stage 0b. The wars' dates are from memory until checked against James (vol. 1 for 1793-96,
vol. 6 for 1812-15) and cited by page.

### 12.2 The four scenarios

| Ship | Frame | Others | Open |
|---|---|---|---|
| The razee | **D25 open.** Proposed (c), off the Lizard, 20 April 1796, a fresh south-easterly: the *Virginie* chase with *Amazon* and *Concorde* in company (Ind §8.1; Gazette 13887 p. 388; Osler pp. 125-128; the lead's view). Indf §11.2 lays out (a)-(d) and what each needs | the frigate-36 under French colours for the *Virginie*; two frigate-36s as *Amazon* and *Concorde* | D25; D48 against a named fit (§19.2) |
| The *Neufchatel* | an American privateer of 1814 in the western Channel, August, a convoy of four under a brig-sloop working up from the Lizard (plan §3; Neuf §5.1) | 72's convoy | the `nations:` block; her date; her names American (D39) |
| The bilander | an old survivor out of Poole, Falmouth to Plymouth, a summer forenoon of 1793-95, a lugger about (D26) | a "privateer lugger" (§8.2); a trader | the lugger's calibre |
| The 74 | Basque Roads, July 1815, the 1815 fit (Bel §8.3; §13.1 answer 15) | the frigate-36 under French colours for *Méduse* and *Saale*; the brig for *Épervier* | the stand-ins' names and fits |

Each is played by the rules captains at seed 7 under pinned weather (`first-action.yaml:30-48`),
names its fit, and is proven by B6's tests: it loads, round-trips, and sails its first hour. What
is built for the razee before D25 is answered: both files with both fits, the descriptions and
roles, and a test that each sails under rules captains at seed 7 in a world with no named fit
(Indf §11.2).

---

# Part C: the ships designed later

## 13. What is laid for them, and what their designs must settle

Each is designed before her build, by the plan's Phase 3 method (two drafts, judged), from her
note and the answers. Each design is written as `docs/design/Design-Ship-<name>.md` and names her
stage 0, her files, her truths' measures and her pins.

### 13.1 The *Prince de Neufchatel* (B2)

**Laid:** the stub `tools/ships/neufchatel.py`; the key `hermaphrodite brig` at rank 2; truths
7-192 and 7-193 reserved; her place second.

**Her design settles:**
- her file's name and description: "hermaphrodite brig" made out, "a brig" at a distance (D15(a));
- **D10, her main topgallant.** (a) is an opt-in key whose yards the handling ignores; it would
  sit beside `under_bowsprit` at Ext §4.2's places 1 and 3 and at the brace consumers of
  `is_yard` (map-engine §3.3), all in B3's files. **Proposed:** her design reports the key to the
  lead with her design (the brief: a rig the engine lacks is reported); if the lead agrees, B3
  builds it as a fourth step after B3.2, and her stage 0b lays the key; until then her file takes
  D10(c), leaving the sail out (about 3% of her canvas: D10), never (b). **Plainly:** the
  sheet keeps D10 at (a); (c) here is the sheet's own fallback ("(c), not (b)"), taken only
  while the lead has not ruled on a fourth engine step outside the gate's three;
- D21 her fore gaff sail, D22 her guns and fits (the privateer's; a pivot by §9.2 if she carries
  one), D23 her stiffness, D11 her sweep ports recorded, not swept;
- her profile from ZAZ6177 and ZAZ6179 (her deck at side about 1.16 m: Neuf §2.9), her sills;
- her company and prize crews, her names American, the basic marines' kit; no nation in her file
  (plan §0);
- her scenario's year and the `nations:` block (§12.1);
- the band of her polar's best point from her accounts (7-193).

### 13.2 The *Bellerophon* (B7)

**Laid:** the stub `tools/ships/bellerophon.py`; the key `seventy-four` at rank 4, with "ship of
the line" and "two-decker" among the size words; the man-of-war sets; the King's ship's doctrine
in `role_of_vessel`; `period.py`'s patterns for her guns (Bel §13.1 answer 12); `DECK_WORDS`;
`exercise_allowance(n, decks=2)`; the profile form and the lee port; truths 7-194 to 7-196
reserved; her place third.

**Her design settles:**
- one file, one rig (Bel §13.5): her mizen course through B1's `mizen_yard.py` (the same sail as
  the 64's), and her spritsail yards through `spritsail_yards.py`; the 1773 driver abaft the
  mizen course, which no engine path can hang (Ext §14 item 10): left out or asked of the lead
  (*reopened by the owner*, §19.1 item 13: Ext §17 proposes Steel's driver boomsail for her by
  the same function as the 64's, which the owner chose);
- **the foot between the drawing and the ship** (Bel §13.2): her profile reconciled with the
  *Bellona*'s reported 5 ft 2 in at Channel draught, the shut heel 10.6° on 22.7 ft (7-195);
- her displacement at the load line the file takes (answer 6);
- her fits: 1793 (74 pieces), 1795-1805 (82, the default), and the late fit after the *Bellona*'s
  1812 list (78) (the decisions sheet's summary of answer 3);
- **the bill by deck** (answer 9): a deck key on each gun, with orders, divisions, stations and
  robbing by deck, and two lieutenants on each gun deck. Numbering on across decks (Indf §5.2) or
  a deck-aware `pair_key` (`parts.py:553-559`); `crew/quarters.py`'s divisions; her stage 0c's
  keys. Her files are named in her design, and any of B3's files taken after B3's merge;
- the rear-admiral's flag (answer 10): a fit changes only guns and stores (`FIT_KEYS`), so the
  flag's 15 supernumeraries are not a fit; her design finds its place within the schema.
  **Plainly:** the decision sheet's summary says "as a fit"; Bel §13.1 answer 10 leaves fit or
  role to the design, and the schema cannot carry men in a fit;
- her company of 590 and her marines (answer 11); four bowers of 67 cwt and six boats by Steel
  and Lavery, through `b.ground_tackle` directly, since `ground_tackle_for` gives two bowers
  (map-generator §0 item 10);
- the tack at quarters (answer 17), her brace limits (answer 14), her best of about 11 kn and the
  close-hauled gap against the *Bellona*'s reports (Bel §13.2), before any polar truth;
- her description words: "a ship of the line" names her description, moving
  `tests/test_ships.py:99`, `:188` and `tests/test_world_orders.py:98`, old beside new;
- a rank-4-aware rule for King's frigates, or a truth that pins a cruiser's role (Bel §7: the
  King's ship's and commodore's books haul off from nobody);
- her pace: a mode in `tools/pace.py` (its `SHIPS` holds four files, :34-45), the 74 crewed against
  `CREWED_FLOOR_TICKS_S` 60 (`world/crews.py:88-91`) and alone against `BUILD_MACHINE_FLOOR` 500
  (`tests/test_known_truths.py:2143-2162`); her truth named `..._holds_truth_51s_floor` or
  marked `pace`, so that `tests/conftest.py:490-500` routes it (7-196).

### 13.3 The bilander (B4)

**Laid:** the stub `tools/ships/bilander.py`; the key `bilander` at rank 1 with its size word;
Ext's settee contract (§5.1 there) and 0E's keys; B1's `spritsail_yards.py` for her spritsail
yard; truths 7-197 to 7-199 reserved; her place last.

**Her design settles:**
- her size, spars and hull (D6, D7); the settee's cut to Gwyn (D5(a)) through her own
  `tools/ships/settee.py` (Ext §9.3); whether a sail is bent to her spritsail yard (D8(b));
- her company of eight (D43), with a main-top pair (Ext §5.1, risk 10); `heave_to_aback` on her
  main; her groups (the settee in "courses" and "plain sail", never "gaff sails");
- her fits: unarmed by default and an armed merchant fit (plan §0);
- her description: "merchant" in what she is made out to be, so that a cruiser takes her for a
  weaker mark (D16(a)); her far rig word;
- her scenario (D26; §12.2);
- B4's checks of Ext §5.7 (her lie hove to, both ways, before any pin) and §5.9 (the sheet's
  block against the taffrail);
- her truths' measures (7-197 to 7-199; §15).

---

# Part D: tests, truths, pins

## 14. Tests

### 14.1 Each builder's tests (in its own new files)

- **Stage 0:** `tests/test_profile.py`, `tests/test_rig_classing.py` (§3.1); 0E's fixtures and
  guards (§3.2).
- **B1** (`tests/test_indefatigable.py`), in the band form with the source in a comment
  (`tests/test_ship_particulars.py:93-104`): her hulls, profiles and sills against the measured
  lines; her spars against Steel p. 49; her sails against table IV (±10%); her guns, fits, crews,
  exercise and filling against Winfield, James, Adye, Falconer and the Regulations; her company,
  posts and marines against the columns and her wardroom files (the check of
  `tests/test_wardroom.py:42-57` on her two files); her ground tackle against Steel's 64; her
  descriptions and size ranks; her polars in `tests/test_ships.py:74-93`'s form with her own beam
  reaches; the round trip under rules captains at seed 7 with no named fit (Indf §14).
- **B2, B7, B4:** the same kinds, on their designs.
- **B3:** `tests/test_lateen.py`, `test_bowsprit_yards.py`, `test_settee.py` (Ext §10.2).
- **B5:** the new `tests/test_view_geometry.py` cases (§6; Ext §6.5).
- **B6:** `tests/test_scenarios_75.py`: each new scenario loads, round-trips and sails its first
  hour; the 64 sails the razee's scenario by the command line (D48(a)) under the way the lead
  chooses.
- **B8:** `tests/test_profiles.py` (§5.6); `tests/test_magazine.py`'s two rows (§16);
  `tests/test_lee_ports.py` (the rule at each file's shut heel, the reopening margin, a shut gun
  neither run out nor fired, the log once a change, an old `Battery` with no `_shut`, no sea no
  roll); `tests/test_subtypes.py` (every description's fit a fit of its file, its roles in
  `ROLES`, a far ship's `role:` refused outside them, the unarmed defaults, the arc from the rig).

### 14.2 The guard set every step runs

- The byte test, two-way.
- The golden classing table (and after 0E the key probe).
- **The lugger's guard set** at each B3 step: `tests/test_lug.py`, truth 7b-111
  (`tests/test_known_truths.py:6186`), her getting under way (:7256-),
  `tests/test_captains.py:583-588`, the lug cases of `tests/test_view_geometry.py` (:728-826).
- **The classing's** at each B3 step: `test_gale.py`, `test_rig_geometry.py`, `test_staying.py`,
  `test_lying_to.py`, `test_evolutions.py`, `test_captain_trials.py`, `test_catalogue.py`, and the
  truths that tack, wear or heave to the frigate and the brig (Ext §10.1).
- **A trace**, a lens check rather than a test: the lugger's tack and wear and the frigate's tack
  and heave-to at seed 7, their log lines and ticks before and after each B3 step.

## 15. The truths 7-185 to 7-199

The last at this head is 7-184 (`tests/test_known_truths.py:10426`). Each truth pins states,
counts, orders of events, ticks and bands, never a digest; its docstring gives the scenario, the
source, the figures measured at seed 7 and the machine. Each is written against the names the
Hull keeps. Each builder drafts its truths in its own test file under the numbers below; Phase 5
moves them into `tests/test_known_truths.py` by number and re-measures them on the merged tree.

| No. | The claim | What it pins | Builder; when | Source |
|---|---|---|---|---|
| **7-185** | the generator writes every ship file byte for byte, and every port gun stands on its port | the generated set equals the committed set; each file equal; every port gun's `(x_m, height_m)` on a triple of its deck within 0.01 m; each existing file's lowest sill in its source's band | B8 at SW-2; re-run in Phase 5 with every file | the brief item 6; the shared draft |
| **7-186** | the *Indefatigable*'s particulars hold their sources, and the razee is the 64 cut down | Indf §14 truth 1: beam 13.5 ± 0.1 m; LWL 48.8 ± 0.3 m; draughts 6.33 and 5.88 ± 0.1 m; the razee's profile below the old upper deck the 64's raised 0.44 ± 0.02 m; lowest sills 1.53 and 1.98 ± 0.03 m; the lower masts' heads lower by c less the rise; 26 × 24 in every fit; complements 491 and 330, marines 84 and 50; four bowers of 57 cwt | B1, stage A | the brief item 6 |
| **7-187** | the razee is lighter, stiffer and faster than the 64 she was cut from | Indf §14 truth 2: displacement less by 238-244 tons of 35 cu ft; draught less by 0.44 ± 0.03 m; righting moment at 10° greater by at least 4%; heel at 90° in 15 kn under plain sail less; speed greater from her closest to 180° in 15 and 25 kn. **And, only if Indf §9's measure bears it out after tuning within D24's bounds**, Indf's truth 4: her polar above the frigate-36's at 60-70° and 120-150° in 15 kn and her best in 25 kn at 11.2 kn or more; else reported, not forced | B1: the first four at stage A; the speed clauses after stage B (on the stand-in, said so, if the gate slips) | the plan, Phase 5 |
| **7-188** | her broadside's weight and rate against the frigate-36's, by 70's rule | Indf §14 truth 3: `far_ship(...).broadside_lb` 510 and 714 against 421 (ratios 1.21 and 1.70 ± 0.05); a starboard 24-pdr's mean interval over twenty minutes at a mark abeam in 7-135's form, 90-125 s with the full company and 140-210 s with a quarter of each crew struck down | B1, stage A | the brief item 6 |
| **7-189** | the 64 handles as a ship with her mizen yard and her spritsails | Ext §10.3 item 4: her classing as the frigate's row; "mainsail haul" swings the main and mizzen yards only; the mizen yard never braced; the mizen course hauled aft at helm's a-lee and brailed up hove to; the spritsails clewed up hove to; she lies to within truth 12's band | B1 at stage B, after B3.1 and B3.2 | D8(b), D9(c) |
| **7-190** | every armed file's lowest lee port is open half a degree below its shut heel and shut a degree above it, and a roll lowers that heel by itself | for each armed file's default fit, at its own threshold: open, then shut; with a roll set on the World's motion, shut a roll's amplitude sooner; the frigate's lee ports open at the 74's shut heel (Bel §6.1 P5) | B8 at L3 | the lead's ruling; Bel §13.1 answer 7 |
| **7-191** | an armed Indiaman holds her colours through the broadside that brings a merchantman's down | the merchant brig in the `indiaman` role and in the `merchant` role, under one scripted broadside: not struck, struck | B8 at SW-4 | the brief item 4 |
| **7-192** | the *Prince de Neufchatel*'s particulars hold their sources | her design | B2 | the brief item 6 |
| **7-193** | the *Neufchatel*'s polar's best point | her design, from her accounts | B2 | the brief item 6 |
| **7-194** | the *Bellerophon*'s particulars hold their sources | her design | B7 | the brief item 6 |
| **7-195** | her lower-deck ports shut at the heel the sources give | 5 ft 2 in at Channel draught on 22.7 ft: shut at 10.6° heel alone (Bel §13.1 answer 5, §13.2), and a roll's amplitude sooner | B7, after L3 | the brief items 3, 6 |
| **7-196** | a 74 crewed holds the floors | her design's measure against `CREWED_FLOOR_TICKS_S` and `BUILD_MACHINE_FLOOR`, routed as a pace test | B7 | the brief items 3, 6 |
| **7-197** | the bilander's particulars hold their sources, and by the wind she lies as close as a brig | her design; her polar's `closest_deg` and `beat_deg(15)` no wider than the brig's 50° and 60° (rule 1: Ext §5.9) | B4 | the brief item 6; D46 rule 1 |
| **7-198** | the settee in stays is kept drawing, its ourse to leeward, and dipped last | Ext §10.3 item 1 (D46 rules 2 and 3), and rule 5's case if Ext §5.10's measure holds (else that half goes to the lead) | B4, on B3.3 | D3(b), D46 |
| **7-199** | in wearing the settee is lowered as she bears up and hoisted on the new lee once the stern is past the wind | Ext §10.3 item 2 (D46 rule 4) | B4, on B3.3 | D46 |

**Not truths, said:**
- **Each scenario's round trip** (the shared draft's 7-188; Indf's truth 5): B6's tests. The
  fifteen numbers go first to the brief's named claims, and a round trip is a test of a file's
  form, not a claim of the period. **Plainly:** the plan's Phase 5 lists the round trip among
  the truths; the brief's item 6 names the fifteen claims, and binds first.
- **The bilander's heave-to** (D4(a)): a test, since no source says how a bilander lay to (Bil §4;
  Ext §10.3).
- **The razee's lee ports** (10.6° and 14.5°, heel alone: Indf §3.4) are lines of 7-190.

## 16. Pins expected to move, and the checkpoint and replay risks

### 16.1 By step

| Step | What moves | How it is shown |
|---|---|---|
| Stage 0, 0E, 0b-0d | nothing | the byte test, the guards, the fast tier |
| B1, B2, B7, B4 | nothing of the existing ships; their own files only | — |
| B7 | `tests/test_ships.py:99` and `:188`, `tests/test_world_orders.py:98`: "a ship of the line" names her description | old beside new, the reason |
| B1 stage B | the 64's own figures (her polar, her balance: the mizen course's offset from 0.8√A in place of the stand-in's 11.1-m head) | old beside new in her notes |
| B3.1-B3.3 | none expected: every change is keyed on something no existing file carries (Ext §11) | the guards; the trace |
| B3, B5 (conditional) | `tests/test_sails.py:65-74` (B3's), only if rule 5 fails and a settee row is added (D44(c)); `tests/test_view_geometry.py:572-602` (B5's), only if the new files join its list and the sprit topsail's trapezoid falls short | old beside new, bisected; never a sail left out of the test |
| B5 | the drawing; the pictures' standard deviation and dark fraction (thresholds expected to stand) | old beside new in the notes; screenshots |
| SW-1 | the `charges` and perhaps `powder_barrels` of the frigate, the brig, the cutter's "long guns" and the privateer's two fits (bytes); `tests/test_magazine.py:59` (`("carronade", 32, 2.6875, 160)` → `2.625`, 159) and `:61` (`("swivel", 0.5, 0.25, 124)` → `0.125`, 122): `fill_seconds` gives 159.4 and 121.9 against the test's ±0.5 (the shared draft, measured); 86's 7-161 to 7-171 where they pin powder, barrels or filling times (measured) | old beside new, on the one commit |
| SW-2 | the eight files' bytes (profile, heights, `deck`); no behaviour | the suite unmoved |
| SW-4 | the privateer's arc, if it moves from [60, 140]: `tests/test_pivot_gun.py:184` and her pivot's pins; quarters beaten in an unarmed schooner, lugger or smack (measured); §8.4 only if ruled in: far and crewed merchant brigs, `tests/test_ships.py:103` | old beside new, bisected on the commit |
| SW-5 L2 | actions heeled past their new shut heels (the privateer's 11.6°, the brig's 12.3-16.4°) | old beside new, the reason, the bisection of §7.3 |
| SW-5 L3 | actions in a sea, on the player's ship | the bisection L2 → L3 |
| The caches | none (the results unchanged) | the pace measured |

**None of the existing ships' sailing passages moves:** no hull figure, spar or sail of an
existing file changes in this package.

### 16.2 Checkpoints and replays (old saves must load)

| Risk | Mitigation |
|---|---|
| A `HullSpec`, `GunSpec`, `Gun`, `Sail`, `Spar`, `Battery`, `Vessel` or `TackScript` pickled before its new field | every new field a plain class default (`None`, `False`, `""`, `frozenset()`), never a `default_factory`, so an old object reads the class attribute (the plan §4's guard; Ext §10.4) |
| An old ship with no profile and no gun decks | the lee port falls back to the gun's pickled height and half the beam; the viewer draws the lens. Documented: an old save fights with its old heights |
| An old save resumed after L2 or L3 | the ports now shut by the rule: a behaviour change on resume, as any rule's. Documented |
| An old save's magazine after SW-1 | cartridges filled after the load take the table's charge (an ounce less for a 32-pdr carronade). Documented |
| `ArmamentSpec.fit` returning None | the three callers handle it in stage 0; old specs carry FitSpecs as before |
| Recorded replays across SW-1, L2, L3 | the replay truths (7-170, 7-171, 7-183) re-run at each of those commits; any move shown old beside new |
| The kept saves (`tests/fixtures/saves/`) | loaded by the fast tier at every step |
| 84's later steps merged under the package | the fresh merge before each stage; new code reads only the names the Hull keeps; `World.__setstate__` (`core/world.py:861-`) is 84's |

### 16.3 Pace

The per-tick additions: one `curve_class` read a driving sail in `_read_rig`, held for the tick's
four substeps; one predicate a square sail in the helm's mark (B3.2); one clause in `boom_sails`;
a sine and a compare a port gun (L2); the settee's change only in a manoeuvre. Measured with
`tools/pace.py` alone and crewed before and after B3.2 and L2, the runs alternated (Eng §2.7's
first-world artifact), and with thirteen files and caches of 32. The floors stand
(`BUILD_MACHINE_FLOOR` 500; `CREWED_FLOOR_TICKS_S` 60); the pace tests are the lead's on the build
machine.

## 17. Review lenses

Each builder's branch is reviewed as soon as it is done, then fixed (plan Phase 4):
1. **Sources and fidelity:** every figure cited or marked; private books as facts and pages only.
2. **Sailing:** the polars, the balance, truth 9's strain behaviour, against the period's
   accounts (the *Bellona*'s reports; the razee's chases; Lever on the spritsail).
3. **The generator:** every file not meant to change byte-identical; the call order kept.
4. **The gun deck:** armament, the bill, the magazine, the lee port's bisection.
5. **The viewer:** screenshots against the current ships; the drawing against the physics.
6. **The gate** (B3): `physics/` holds only Ext §1's lookups and memberships; the lugger unmoved.
7. **84's names, pace, checkpoints:** no `world.ship` or `CrewedWorld` beyond the Hull's names; the
   pace measured; an old checkpoint loads.

## 18. What is left out, and why

- **The ports themselves, the guns drawn, the flash and the smoke:** 81's, from the drawn hull.
- **The fillers as posts:** 77's, unless the lead says otherwise (§9.3).
- **Table No. 29's double-shot and salute charges:** 77's cycle (§10).
- **The far fight's lee ports:** a far ship has no heel; the far fight is 74's.
- **The frigate-36's quarterdeck and draught:** the owner's ruling; recorded (§5.4, §11).
- **The armed Indiaman's hull, the packet's hull:** later ships (§8).
- **The smuggler and the search; sweeps** (D11(a)): not modelled.
- **The razee's first rig** (D17): no file.
- **Steel's occasional driver on the 64's mizen yard, the 74's 1773 driver:** no engine path
  (Ext §14 item 10). *Reopened by the owner (§19.1 item 13):* Ext §17 proposes Steel's driver
  boomsail for both, which the owner chose (2026-10-28; its §17.9 item 1); the 1773 sail stays
  unbuilt.
- **The spritsail yard's topping, the sprit-topsail traveller, Steel's diagonal reefs, the
  spritsail yard got fore and aft:** Ext §4.4.
- **The vangs, ourses and derrick drawn:** the current standard (Ext §6.3).
- **The tartane's full lateen and its curve:** a later package (Ext §3.7).
- **The bowsprit's hands mapped to the forecastle:** could move pins (Ext §4.3).
- **`PEAK_COEFF["studding"]`'s 1.25 against the curve's 1.44:** not this package's to change
  silently (map-engine §10).
- **The privateer schooner's wardroom file** (§9.5); **HMS *Dolphin*'s arc** (§9.2).
- **The French 74, the Bermuda sloop, the boats as files:** later, by the brief and the owner.

## 19. Open

### 19.1 For the owner

**Answered by the owner (2026-10-28; Decisions, "The design's questions").** Item 3: "as carried
1796". Item 4: the spritsail yard only, out of plain sail. Items 5, 6 and 8: as proposed. Item 7:
as proposed, except the lifts, now drawn on every yard (§6). Item 10: the six-inch margin. Item
11: fetched and read (below). Item 13: carried (below). Still open: 1, 2, 9, the weather side
of 10, and 12. Item 13's second question, which sail, is answered: Steel's driver boomsail for
both (below, Ext §17).

1. **D18:** (a) proposed for every file (§5.5); the razee's gun deck at 1.39 m, or (c) her old
   upper deck at 3.66 m; decided on B5's screenshots.
2. **D25:** (c), the Lizard of April 1796, proposed (the lead's view and the shared draft; Indf
   §11.2 lays out all four); held open by the owner.
3. **The razee's default fit:** "as razeed 1795" by the brief, or "as carried 1796", her guns in
   every action read (Indf §5.1); it also settles D48's second way.
4. **The razee's spritsail yards:** Steel 1794 p. 49 gives the 44 and the 38 both yards; D8(b) as
   answered named the 64's and the bilander's (Indf §4.6).
5. **Steel's topgallants and royals** for the 64: Steel's spar and sail tables disagree above the
   topmast caps; proposed that the spars rule (Indf §4.3).
6. **The judgement figures** of the *Indefatigable* (Indf §17 item 10): the 64's 76 private
   marines; her 18-pdr at 40 cwt; the split of the 1795 establishment's 12s and carronades; the
   small-arms men; the exercise read as a third of her upper-deck guns.
7. **The engine's judgement figures** (Ext §14 items 5-9): "furl the mizen" furls it aloft; the
   settee's dip when the head yards' swing ends; its times and hands; the spritsails out of
   "plain sail" and taken in first; lifts drawn on a lateen yard only.
8. **The brig's sill** falls from 2.1 m to Steel's sloop band, 1.22-1.52 m (§5.4).
9. **The swivel's charge** halves, 4 oz to 2 oz, by the table's half-pounder (§10).
10. **The weather side's ports** under a roll beyond the heel, and the six-inch reopening margin
    (§7.1).
11. **Pages to read** (filed with provenance): Steel 1805's bodies tables for the 36-gun
    frigate, the 273-ton cutter and the 60-ton sloop; ZAZ6306; Chapelle's fig. 17; Chapman's
    Pl. LIX. *Done (2026-10-28):* the four notes `ships-design/pages-*.md`, the images cached
    outside the repository (`docs/references/README.md`). ZAZ6306 is Crown copyright: read and
    measured, never copied.
12. **The revenue cutter's guns** (the hired cutters' long guns stand in) and the *Éclair*'s
    calibre.
13. **The driver** of the 64 and the 74 (Indf §4.4; Ext §14 item 10): the occasional light-weather
    sail hoisted to the mizen yard's peak on its own small yard, abaft the mizen course. The
    mizen course itself stays her after sail. *Carried (the owner, 2026-10-28):* Lever sets it like
    a studding sail, its yard hoisted to the peak, the tack to the weather fife rail, the sheet to
    a pole run out over the taffrail
    (`docs/references/lever/lever-1827-young-sea-officers-sheet-anchor-ocr.txt:8264-8270`).
    Proposed as a ringtail whose host is the mizen course, which has no boom (`physics/sails.py`
    `_gaff_host` finds a ringtail's host by its boom): an addendum to Ext for the lead's gate,
    built with the 64's stage B and the 74. *For the owner (Ext §17, the addendum,
    2026-10-28):* from the evidence, the addendum proposes for both ships, in place of the sail
    above, Steel's driver boomsail of 1794: four-sided, its luff laced to the mast, its head
    along the mizen yard and on along a small driver yard, its foot on a boom over the stern
    (Ext §17.1; for the 64 the evidence is weak). In their day it was bent beside the course,
    which was brailed up while it drew; the game would shift one for the other (`in_place_of`),
    so the course would be unbent while the driver is bent, against "The mizen course itself
    stays her after sail" above (Ext §17.3). Which sail each ship carries was put to the owner.
    *Answered (the owner, 2026-10-28):* Steel's driver boomsail for both, as proposed, chosen with
    the two sails drawn side by side. Nothing of the addendum is built until the lead has read it
    (Ext §17.8, §17.9 item 1).

### 19.2 For the lead

1. **The gate:** Ext as it stands with this document's three edits (§20), above all its §14
   items 1-2: the mizen course as class lateen read through `curve_class` with the gaff's curve,
   and the physics' readings (`curve_class` at thirteen lookups; `_square_rigged`, the helm's mark
   and `_spar_x` leaving out the yards under the bowsprit) as within "the physics' equations are
   not changed".
2. **Stage 0E after the approval** rather than in stage 0 (decision 4), and the four
   `curve_class` lookups moved into stage 0 (decision 22).
3. **D48 against a named fit** (Indf §11.1): three ways. (1) the scenario names no fit; (2) the
   owner makes "as carried 1796" the default; (3) a command-line ship lacking the scenario's fit
   takes her own default with a line in the log (`world/scenarios.py:738-748`), which serves every
   file with named fits and changes behaviour only where today raises, but is world code outside
   the brief's list. Lean: (3), built by B6 if ruled in.
4. **The fillers as posts** left to 77 (§9.3).
5. **The merchant brig's description** moved to `merchant-brig.yaml`, and the packet's
   description (§8.4).
6. **The scenario's `nations:` block** (§12.1), outside the brief's list.
7. **D10(a)'s key** for the *Neufchatel* built by B3 as a fourth step (§13.1).
8. **The order of the ships** after the *Indefatigable* (§2.3), and whether the lead merges
   the package's branch after each ship or once at the end (the road works either way: no description
   row dangles, and each window closes with a merge).
9. **The names:** `sixty-four.yaml`, `razee-44.yaml`, `hermaphrodite-brig.yaml`,
   `seventy-four.yaml`, `bilander.yaml`; the modules; the fits "ardent class 1784", "ardent class
   1794", "as razeed 1795", "as carried 1796"; the description keys.
10. **The workflow's shape:** stage 0's ownership of `schema.py` for the whole package; truths
    drafted in the builders' files and moved in Phase 5; a file passing between owners only at a
    merge; the two-way byte test.
11. **The head:** the go-ahead names 8db8b9a and the clone merged 3421829; the ancestor check of
    §2.1 settles it before stage 0.
12. **The frigate's draught** (15 ft against Steel's 17 ft 10 in) and the frigate-36's trimmers,
    which spend her marines at the guns (Indf §18 item 13): recorded for the frigate's own file.

## 20. What this document changed in the two designs

The smallest edits that make each agree with a settlement above. Nothing else was changed.

**`Design-ShipsEngineExtensions.md`:**
1. §8's opening: its interfaces are laid as stage 0E, after the lead approves the document and
   before B3 starts, and the four `curve_class` lookups outside B3's files (`world/ships.py:391`,
   `api/queries.py:334`, `api/readings.py:873`, `tools/gen_ships.py:869`), with
   `PEAK_COEFF["lateen"]` and the property's first form, are in stage 0 (decisions 4 and 22).
2. §9.1, B3.1: "the thirteen `curve_class` lookups" becomes the nine in its own files; §13 risk
   4's mitigation says the same.
3. §10.3: the candidates' numbers (7-198, 7-199, rule 1 in 7-197, the 64's in 7-189).

**`Design-Ship-Indefatigable.md`:**
1. §1.2 and §12.1 item 1: `SHIP_MODULES` names the four modules from stage 0, each a stub.
2. §3.1: the profile's form gains `breadth_m`; the form is fixed in Build-Ships.md §5.1. §3.5
   item 2: the half-breadths by station at the water and the rail.
3. §4.4, stage B: the yard's lines are Ext §3.4's (no truss or brail lines), and Steel's
   occasional driver is left out (Ext §14 item 10).
4. §5.4: the 64's exercise by stage 0's `exercise_allowance(26, decks=2)`; her charges note
   overridden only until SW-1 lands.
5. §6.3, §13: her tests in `tests/test_indefatigable.py`, her truths drafted there and moved in
   Phase 5, her tuning notes folded in Phase 5; B1 also owns `mizen_yard.py` and
   `spritsail_yards.py`.
6. §8 and §12.1 item 5: her `DESCRIPTIONS` rows and words land with her files; the keyed rows in
   stage 0.
7. §10: the roll as `Firer.roll_deg`.
8. §12.1 item 6: the two-way byte test taken; the list's lines are :563-572 at this head.
9. §12.2: Ext's answers to items 3, 5, 8 and 9.
10. §14: the truths' numbers (7-186 to 7-189; her truth 4 a clause of 7-187; her truth 5 a test of
    B6's).

**The adversarial check's edits** (by an agent that wrote none of the three, against the code
at 6b94731 and the notes; the smallest that make each agree):
- *Here:* the import lines (:110-118); the rounding's exact form; the tuple at
  `squadrons.py:467`; the byte test's list (:563-572) and `test_period_names_resolve` kept as a
  hand list; a module keeps its `SHIP_MODULES` name; `combat/guns.py` given to B8 and
  `parts.py`'s charge comment laid in stage 0, so that no file is orphaned or shared;
  `world/scenarios.py`'s passing; the files beyond the brief's heading said plainly; the
  razee's shut heel 14.5° (1.98 m on 6.67 m); the slice 238-244 tons (Ind §2.3.3); the
  frigate's 4.0° placed on the gate's day (Bel §6.1 P6); a description's default fit not set
  on a far vessel; the merchant brig's fit; "Plainly" on the roll, D10, the flag and the round
  trip; the view test's owner; Steel named in place of a pronoun (§19.1 item 5).
- *Ext:* the opening's stage 0 pointer; §3.4's citation of a sail's centre; §5.9's line
  (`trim.py:266`); §9.4's stage 0E; §13 risk 6 without a quotation.
- *Indf:* §0's stage B (no truss or brail lines, no driver, as §4.4 settles); the slice
  238-244 tons in §1.5 and §14; the razee's shut heel 14.5° and 14.3° (§3.4, §14, §16); the
  mizen topmast's hoist 10.34 m; the path note of §1.2; §9's polar test and §15's lists in her
  own test file; §13's one edit under `freesail/world/`; §16 risk 3 as answered; §12.1 item 6's
  lines.
