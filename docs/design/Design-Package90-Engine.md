# Design note: the engine for package 90 (November 2026; third draft, revised)

**Revised 2026-11-18 on the owner's decision of A1d (the lead's note of 22:35 UTC, nudge 19).** The
owner decided that A1d is built, in these words: "A lateen taken aback should increase the strain
on the mast, as a backed square sail does, so that on the worse tack and not dipped, the sail may
strain the mast and, in high enough wind, risk damage." This revision:
- writes A1d as a step that is built, not an option (§2.4.3, §12 item 2, §14): the rule of force
  in `physics/sails.py` named as a physics addition, what it reads (the whole lateen, the side, the
  wind's face), and its strain on the mast as well as the yard, by the engine's existing strain and
  carrying-away and no new kind of damage, each part of that road read and named;
- gives the strain aback and on the bad hand in the same terms, the winds at which each strains
  and risks the spar and the two factors, each JUDGEMENT for the lead's ruling, checked against the
  rules captain's 22 kn, 12 kn and 1,800 s, with the margins (§2.4.3);
- measures what the rule moves (a new §2.2b, run in scratch): the polacre's 407 s traced, a failed
  tack under nudge 18's process rule and not a long one; the probes' going about with the rule,
  moved by −9 to +13 m; the strain aback and on the bad hand on the probes rated by the generator's
  rule;
- reads what the tack and the wear do to a whole lateen in stays (nothing) and says what they
  should (a new §2.4.3a), with the words where a sail is aback;
- brings into line the "In brief" row, §2.1, §2.2a, §2.3 items 1, 2 and 7, §2.4.2, §2.4.5, §13 and
  §14, and adds "How this revision answers the owner's decision" below the lead's table, and §13
  items 13 and 14.

The new measures were run in the session's scratch (`p90/n19/`), on the tree at e39b84a8 (its code
that of 68e769ef), with `PYTHONDONTWRITEBYTECODE=1` and no tracked file changed.

**Revised 2026-11-18 on the lead's note of 11:35 UTC (nudge 18).** The lead had the note read
independently against the code at 5b987acd and found most of it confirmed: item 37 exactly, the
lateen tack and the bad hand's figures, `dipping` and `against_the_mast` as read, the square
topsail over a lateen, the sweeps, the third deck and the pace floor. The lead ruled the plan's
§13.1 (each ruling written below as JUDGEMENT, as the note had it) and sent one list back of six.
This revision:
- writes the rulings into §2.3, §2.4.4 and §14 (the car abaft the mast; the bad hand the lug's
  two-thirds; the change's time the lugger's own rate, **8.7 seconds a metre of yard**, her 90 s
  for 10.3 m, in place of 7½; one able hand for 2½ m, at least four; the rules captain's 12 kn and
  1,800 s read with defaults and written in no committed book; the course's judgement wearing a
  lateen over 22 kn; a tack's end waiting for her to pay off keyed on a whole lateen only; the
  order's words);
- recomputes every figure that used 7½ seconds a metre: the hulls' change times (§2.4.4), the
  changed variants at the hulls' own seconds and the short boards' break-even (§2.2a, run again
  in scratch at 5b987acd), the polacre's (§2.4.5) and the costs (the plan's §11 and §14);
- answers the six items of the list: A1d re-drafted as **an option for the owner** (§2.4.3), the
  "aback" loads of §2.2a corrected; the routing of `shift`, `change` and `dip` (§2.3 item 3a);
  A2's moves of the lugger's pinned transcripts, old beside new (§2.3 item 9); every place the
  settee's change is woven in that the lateen's must mirror, and A1b re-estimated (§2.3a); A1a's
  edges (§2.3 item 1); A1c's figures, where they are read (§2.3 item 6);
- adds a table, "How this revision answers the lead", below the owner's, and §13 items 10 to 12.

The new measures were run in the session's scratch (`p90/n18/`), on the tree at 5b987acd, with
`PYTHONDONTWRITEBYTECODE=1` and no tracked file changed.

**Third draft, 2026-11-18, on the owner's answer to question 3** (the decisions sheet,
`Decisions-Package90-2026-11.md` §3 and Part F; the lead's note of 2026-11-18, 04:30 UTC, nudge
17, items 2 to 4). The owner agreed nine of the ten questions as picked and answered the third
with a shape of their own: a vessel with a lateen main tacks and wears as other vessels do, each an
ordered evolution, and the change of the yard round the mast is "preferred but not necessary".
No source read says a lateen vessel could not tack (`Research-LateenGoingAbout-2026-11.md`,
cited **GA**, §3.4 and §4), so their knowledge stands as the judgement, said as one. This draft
changes §2 (its title; §2.1's last two paragraphs; a new §2.2a of measures run for it; §2.3
re-drafted on their shape; a new §2.4, what going about costs and risks under a lateen), the "In
brief" row of the lateens, §12's list, §13 (items 8 and 9, new) and §14 (A1 re-planned as A1a to
A1d; the A0 row's "under the owner's (a), agreed"), and adds "How the third draft answers the
owner" below the critic's table. Everything else is the second draft's.
The measures of §2.2a were run in the session's scratch (`p90/goabout/redraft/`), on the tree at
9fe1b37d, with no tracked file changed.

Package 90's preliminary work, the engine's part (the lead's note of 2026-11-18 at 00:50 UTC,
nudge 15; `docs/dev/M7-WorkPackages.md`, row 90). It does two things. It reports item 37 of the
ships session's list of 79, the generator's own copy of the sail-force law, as the lead asked
(what it is read for, what would move if it were the engine's, what reads those figures, what I
would do), without changing it. And it sets down what the engine does **today** with each thing
the five hulls ask of it (the tartane, the polacre, the xebec, the corvette *Diana* and the
*Purísima Concepción* class three-decker), each run in scratch and not guessed, with what the
build would want. **This is the second draft (2026-11-18)**, by the plan's form
(`Plan-ShipsWorkflow.md`): it answers the critic's reading of the first ("How this draft answers
the critic", after the brief), takes the settlements of package 90's plan
(`docs/design/Plan-Package90.md` §4) and, as the plan asks of it (its §3, Phase 2), sets down the
engine's steps by the plan's names, A0 to A9 with the viewer's V1 to V4, as **one design for the
lead's approval before stage 0L** (§14), as `Design-ShipsEngineExtensions.md` was before package
75's stage 0E.

Nothing is built here. No code, no ship file, no generator change, no test, nothing the suite
reads: this note is a new document, with the package's other new documents the only change to the
tree.

## 0. Marks, probes, the tree

**The marks**, as `Research-ShipsEngine-2026-10.md` uses them: **read** (the code or the page at
the place cited), **observed** (seen in a run), **measured** (a figure from a run), and
**judgement** (reasoning, mine unless said). A JUDGEMENT that a file or a design would carry is
written so.

**The tree** is package 90's branch at 68e769ef (the trunk at nudge 15). Every line cited is that
tree's.

**The probes** were run with `py` from scratch folders outside the repository, the worktree first
on `sys.path` and `freesail.__file__` asserted under it; no tracked file changed (`git status`
clean but for the new documents), the only things written in the worktree being Python's bytecode
caches, which git ignores (later probes run with `PYTHONDONTWRITEBYTECODE=1`). Every speed in knots
in §2 and §4 is the ship's speed, `dyn.speed`, the measure truth 12 reads (`knots()`,
`tests/test_known_truths.py:120-121`). The rigs in
memory were made from the committed files by the lead's helpers in `tests/rig_fixtures.py`
(imported, not changed): the lead's `tartane_probe` and `polacre_probe` (made for classing and
never sailed; sailed here in scratch to see what the engine does with them), and two made the same
way for this note, a **xebec probe** (the polacre probe with her square main replaced by a third
whole lateen on a 19 m yard, 150 m², scratch figures) and a **three-decker probe** (the 74's file
with her upper deck renamed `middle`, a new `upper` deck and her upper works raised 2.3 m, each
fit's upper-deck guns copied onto the new deck, her stations scaled to a company of 839: scratch
figures, not the *Concepción*'s). The harness is the settee tests' (`tests/test_settee.py`,
`_world`): `make_world` at seed 7, a steady northerly, no gusts, the ship on the starboard tack
67.5° off the wind, plain sail set, trimmed every two minutes after the first five, settled 1,800
s, then the order and 900 s. Item 37's measure ran on a copy of `tools/` in scratch (§1.3), and
its suites against the scratch files by a read redirect in scratch (§1.4). The probes' scripts and
their outputs are kept with the session's scratch, not in the repository.

## In brief

| Need | What the engine does today (measured unless marked) | What the build wants |
|---|---|---|
| Item 37, `PEAK_COEFF["studding"]` | 1.25 where the engine's curve peaks at 1.4396 at 35°; read by the rating pass alone, for the studding-sail booms and the ringtail booms. Made the engine's: **74 figures in 9 of the 18 files move**, every one a studding-sail boom's or a ringtail boom's `rating_kn`, up 15 per cent; nothing else in any file | The generator reading the engine's curves (§1.5). In both tiers on the moved files: truth 35's last clause and `test_studding`'s frigate brought up to six points move (no boom carries away), five records of "no figure moved" name the booms, seven byte pins hold again by the regeneration; truth 9 and truth 14 hold. For the owner, before any new file is generated |
| Whole lateens tacked and worn, the yard changed or left (the owner's answer to question 3) | No dip: the schema refuses `dipping` on any sail but a lug. The tartane, the polacre and the xebec probes **tack** in 89, 164 and 101 s, the lateens swung over as gaff sails with no word, drawing alike on both tacks (5.07 and 5.02 kN, the polacre's fore lateen); a wear says nothing of them. In 15 kn a tack loses them 205 to 249 m to windward and a wear 519 to 602 (§2.2a). **A whole lateen is never aback**: with the wind on its wrong face it collapses and flogs (`physics/sails.py:1136-1141`); her head in the wind's eye costs her way and no spar (§2.2a) | The plan's A1a to A1c (§14): `dipping` allowed on a whole lateen for its side and its loss on the bad hand; the tack and the wear each with the yard's change as a part, done or left by the order's words or the ship's practice ("shift" by default), at 8.7 s a metre of yard (the lead's ruling); `shift the mainsail` alone, the sail room's replacement kept by "for"; the rules captain's choice; the lateen mizen worked as a ship's mizen and kept set hove to; the words (§2). **A1d, built by the owner's decision** (nudge 19): a whole lateen held aback against its mast once the wind has come round onto the side its cloth lies on, and one on the bad hand, load its yard and its mast by two factors, so that aback it strains from about 28 kn and on the bad hand from about 45, by the engine's own strain and carrying-away; the tack and the wear draw a left lateen over at "let go and haul" and "wind aft" (§2.4.3, §2.4.3a) |
| A square topsail over a lateen (the tartane) | Classed as the cutter is, by B3.4's rule as the lead read it: her main her one mast with yards, the topsail her head yard, no after yards, not square-rigged; hove to with it aback **on the probe, whose topsail stands on the cutter's topmast**; on her design's pole main (the yard on the lower mast's head) the topsail is a course today and is hauled up hove to (Tar-D §5.1a) | Nothing new for the classing; A5 and A6 for her topsail on a pole main (§14); her *tréou* for her document; her boat in tow, which no boat's entry can say today (§3) |
| The pole mast (the polacre) | No such thing in the engine: every square sail is furled aloft by topmen; her main topsail yard put on the lower mast classes as the probe does | The pole known to the square sails' take-in and furl, the topmast evolutions and the viewer, read from the parts as filed (the polacre's design's reading); item 8 settled in her document (§4) |
| Sweeps | A ship's file may carry a boat's `oars:`, and is then a boat to the game (no bells, "a boat under oars, with no rig to draw"); `give way` mans every oar at once from nobody (the probe's 121 men untouched), no evolution, no time; 20 oars at a boat's figures move the xebec probe 1.6 kn in a calm | Sweeps of a ship's own, apart from a boat's oars; as a fit; an evolution drawing the men from the company; men to a sweep; the guns' crews against the oars (§5) |
| Three gun decks | The probe loads, names, beats to quarters by deck, fires by deck, shuts its lee ports by deck and passes the viewer's check. Two readers of the quarter bill single out the lower deck (the crews behind shut ports, the order the crews are robbed in); the clearing time stops at the frigate's; the viewer says "a lower port", "a middle port"; a first rate has no words or rank | The few two-deck places generalised; her words, her rank, her bill by deck (§6) |
| A first rate's company and the pace | In truth 7-196's world three 74s crewed run 79 to 81 ticks a second, three three-decker probes of 839 run 72 to 75, the floor 60; alone, 514 and 487 | Nothing of its own: the cap and the floor serve her (§7) |
| The regency's cruiser | A role is a book of `data/captains/` with `thresholds:`; package 116 put the prize doctrine's thirteen keys there and read seven | A `corsair` (or `regency`) book on the cruiser's and the privateer's form (§8) |
| The harbour's shelves | Every ship file is offered for a bare start; a scenario on no shelf goes to "Not yet sorted" and fails `tests/test_harbour.py:131` | A shelf line for each new scenario (§9) |
| The wheel and the tackles | Every hull, the tiller-steered cutter and tartane among them, says "the wheel is shot away", rigs the tackles "to the tiller" and repairs "the wheel" with "new wheel-ropes" | A hull's helm read from her file, a tiller's words (§10) |
| Package 81's viewer checklist | The xebec probe and the three-decker probe pass `tools/check_viewer_guns.py`; a whole lateen is drawn as a four-sided sail under its yard, or as a lug | Each hull's ports and decks to the checklist; the whole lateen drawn as its own; the obús is no gun kind (§11, §6.3) |

## How this draft answers the critic

| Finding | What the first draft said | This draft |
|---|---|---|
| F7: the lateen mizen | §2.3 item 5: the mizen "read by the driver's paths ... handled hove to by the driver rule" | **Held.** Restated as the plan's §4 row 4 settles it on the polacre's measure: hauled aft as she comes to (and at helm's a-lee on a square main), eased at "up helm", kept set hove to, never read by the driver rule (§2.3 item 5, §14 A1) |
| F3: the tartane's topsail | §3: she "heaves to with the topsail aback" | **Held.** So on the probe, whose topsail yard is on the cutter's topmast; on her own design's pole main the topsail is a course to the engine and is hauled up (the critic's run, re-run for the tartane's second draft: Tar-D §5.1a). A5 and A6 come before her file (§3, §14) |
| F25: "nothing in the tree written" | §0 | **Held.** Reworded: no tracked file changed; Python's git-ignored bytecode caches were written by the probes (§0) |
| F22 (with the plan): the far body's pace | §5 named no file for it | `world/ships.py`'s far pace (`VESSEL_MIN_SPEED_KN`, l. 98, read at l. 849 and 865) is A7's (§14; Plan §7.1) |
| The plan's settlements | the dip's key or the settee's machinery, "the lead's choice"; the Spanish pound "the English pounds" | the plan's proposal for A1 (§2.3 item 1, §14); the Spanish pound the owner's, the pick the nominal pounder (§6.3; Plan §4 row 8, Dec 9) |

## How the third draft answers the owner (question 3, 2026-11-18)

| The second draft | What the sources and the owner say | This draft |
|---|---|---|
| "Worn, not tacked" where the main is a whole lateen (§2.3 item 3); `Ship.wears_only()` | The rule came from the brief, not a source (GA §4); the owner: she tacks and wears "normally with their evolutions" | **Dropped.** Every lateen rig tacks and wears; `wears_only()` is not laid (§2.3, §14) |
| `tack ship` answered "She does not stay under her lateen; wear her." and nothing done | No source says so (GA §6) | **Dropped.** `tack ship` tacks; `put her about` and the course's judgement wear her only over `lateen_tack_kn` (§2.3 item 6) |
| The yard changed only in the wear, at "wind aft" | "it being preferred but not necessary"; the yard changed "pour virer de bord", either way (Lescallier p. 378; GA, the words) | **A part of either**, done in stays or in the wear by the order's clause or the ship's practice ("shift" by default), or left (§2.3 items 2-3) |
| A lateen left on the wrong side lies against its mast (A1 (1)) | the board on the mast named in four dictionaries and sailed (Stratico, O'Scanlan, Romme, Willaumez: GA §3.3) | **Kept**, and measured: 4 to 17 per cent of her speed close-hauled (§2.2a) |
| The heel passed abaft the mast | Willaumez abaft; O'Scanlan's CIMAR forward (GA §3.3) | **Not agreed**: the viewer's only; the lead's (§2.3 item 2). *Ruled abaft by the lead, 2026-11-18 (nudge 18), O'Scanlan's forward recorded* |
| Nothing on the costs | Forfait p. 119 (taken aback in a strong wind); no figure of way, wind, loss, hands or time (GA §5) | **§2.4**: the game's figures, each JUDGEMENT, measured where they can be (§2.2a); a lateen aback in a breeze strains her yard (A1d); the rules captain's practice (A1c). *Revised on nudge 18: A1d's premise does not hold in the engine, and it is now an option for the owner (§2.4.3). Decided by the owner on nudge 19: built, as a new rule of force (§2.4.3)* |
| The bare xebec's tack (her probe stalls 39° off) | the mizen added to bring lateen vessels to the wind (Lescallier pp. 393-394) | **Her mizen eased as she pays off** where she has no head sail: measured, 192 m lost against 1,064 (§2.2a, §2.3 item 5) |

## How this revision answers the lead (nudge 18, 2026-11-18, 11:35 UTC)

**The rulings on the plan's §13.1**, each written where it lives and each JUDGEMENT, as the note had
them:

| Ruling | Where |
|---|---|
| The machinery: the lean, with the list below (`dipping` widened; the change in the tack and the wear on the settee's model, the yard peaked and not lowered; `change_lateen` by itself) | §2.3 items 1-2, §2.3a, §14 A1a-A1b |
| The car passes **abaft** the mast (Willaumez, MUDER); O'Scanlan's forward (CIMAR) recorded | §2.3 item 2, §14 A1b, V1 |
| The bad hand: **the lug's two-thirds** (`LUG_AGAINST_MAST_AREA`) | §2.3 item 1, §14 A1a |
| The change's time: **the lugger's own rate, 8.7 s a metre of yard** (her 90 s in a manoeuvre for her 10.3-m main yard), not 7½; **one able hand for 2½ m, at least four** | §2.4.4 (every figure recomputed), §2.2a, §2.4.5 |
| The rules captain's **12 kn and 1,800 s**: read with defaults and written in no committed book that would move a count. The **22 kn**: see item 6 of the list, below | §2.3 item 6, §14 A1c |
| **The course's judgement** wears a lateen over 22 kn, and tacks her regardless where there is no room | §2.3 item 6, §14 A1c |
| **A tack's end waiting for her to pay off**: keyed on a whole lateen only, so that no other rig's pin moves | §2.3 item 5, §13 item 8, §14 A1b |
| **The order's words**: on a hull with a whole lateen, `shift the <lateen>` and the clause "and shift the lateens" mean the yard's change; the sail room's replacement keeps its form with "for" (`shift the mainsail for ...`); `dip` stays refused for a lateen that is not whole; "and leave the lateens" after the order, no form beginning with a clause and a comma | §2.3 items 3-3a, §14 A1a-A1b |
| Items 2 to 7: the leans. Item 8 (the relieving tackles at a first rate's helm): the hands proposed as JUDGEMENT, as for item 3 | the plan's §13.1 |
| A1d not ruled: its premise does not hold in the engine (*nudge 19: decided built by the owner*) | §2.4.3 |

**The list of six:**

| # | The lead's item | This revision |
|---|---|---|
| 1 | A1d: a whole lateen is never aback in the engine; the "aback" loads are the drawing peaks | **Agreed and measured** (§2.2a, re-run): over 240 s of "steer north" the tartane probe's lateens were backed for no tick in 15, 25 and 35 kn; within 30° of the wind her main yard carried 0.009, 0.025 and 0.048 of its rating against 0.15, 0.35 and 0.58 close-hauled; the 35-kn "aback" peak was 0.58 at 66 s, 71° off the wind, as she filled. §2.2a and §2.4.3 corrected. **A1d re-drafted as an option for the owner** (§2.4.3): the rule of force for a lateen held aback against its mast and where it lives, its size (one and a half to two days, the reader's guess and mine), what it moves (made in process, it turned the polacre probe's tack in 15 kn from 164 s and 249 m to 407 s and 725 m), and what the game says and does without it. *Nudge 19: the owner decided it built; the 407 s traced, a failed tack under the process rule, not a long one (§2.2b)* |
| 2 | `shift`, `change` and `dip` today, and the routing key | **Run** (§2.3 item 3a): on the 74 and the 64 `shift the mizen` and `change the mizen` shift the mizzen course for a spare in 1,002 s and 999 s; `dip the mizen` is refused, "'dip' has no meaning for a lateen sail."; on the tartane probe `shift the mainsail` goes to the sail room. The key: `verbs.evolution_key` gains `whole_lateen` on the settee's model, for a lateen with `dipping`, read unless the order says "for"; what is lost and kept |
| 3 | A2 moves pins A1b calls a guard set | **Agreed, and wider** (§2.3 item 9): the lugger's two pinned transcripts (`tests/test_settee.py:1418-1456`, read by the test at l. 1459-1489), run as they are in scratch, move by four lines at A2's cause (the tack's last, the wear's first, its "wind aft" line and its last), every tick the same, and the lugger's case of `tests/test_evolutions.py:1169-1171` by one; the cutter's and the smack's by the wear's first line only (run). A1b's claim corrected; A2 merged alone before A1a, so the guard set is moved once and then holds |
| 4 | A1b is larger than a day and a half | **Agreed** (§2.3a): eighteen places where the settee's change is woven in, eleven of them for the lateen's to mirror; the wear's own timing (at wind aft, not "up helm": its own code path, not a flag); each yard's hands and seconds and "one after another, the main first", which `SetteeChange` has not; the change built only when one is needed, a plain class, or truth 7-606 moves. **Three and a half days** (the reader's three to four) |
| 5 | A1a's edges | **Agreed** (§2.3 item 1): the side found once in `set_lateen` for a whole lateen alone (the 64's and the 74's mizen course and driver untouched), kept aloft by `take_in_lateen` and `furl_lateen` as the settee's is; the heave-to's refusal keyed on a whole lateen set (the five boats are refused today in other words, run); the stern watch deaf to a shift through the bow (read), a line for it at its cause |
| 6 | A1c's figures and where they are read | **Agreed** (§2.3 item 6): `put_about_choice` and `judge_course` read no book, so the 22 kn is a module constant of `orders/navigation.py` beside `WEAR_WIND_KN`'s 30, read for every voice; the 12 kn and 1,800 s are the rules captain's alone, from their book with defaults; "leave under 12 knots" is their practice, set as the wind crosses it, so that every tack by any road reads it; `tests/test_subtypes.py:463-490` named |

## How this revision answers the owner's decision of A1d (nudge 19, 2026-11-18, 22:35 UTC)

The owner, verbatim: "A lateen taken aback should increase the strain on the mast, as a backed
square sail does, so that on the worse tack and not dipped, the sail may strain the mast and, in
high enough wind, risk damage."

| # | The lead's item | This revision |
|---|---|---|
| 1 | A1d written as a step that is built: the rule of force in `physics/sails.py` named as a physics addition, what it reads, and the strain to the mast as well as the yard by the engine's existing strain and carrying-away, no new kind of damage | **Written** (§2.4.3; §14 A1d). The rule: **a whole lateen held aback against its mast**. It reads the whole lateen (class `lateen`, no `cut_at_mast`, A1a's `dipping` and `lug_side`), the side (its cloth kept on its yard's side by the mast while the wind comes round ahead, carried over to leeward abaft the beam, drawn over by hands), and the wind's face at its own height (`on_drive_face`); held, it is a plate aback by `_plate_force` as it stands. Its pull on its spar chain (yard, then mast) is multiplied in `_apply_loads` by `LATEEN_ABACK_LOAD` aback and `LATEEN_BAD_HAND_LOAD` on the bad hand; the strain, wear, warnings, chance, certain failure and `_wreck_spar` are `physics/strain.py`'s as they are. A backed square sail's road, read and named part by part: `_plate_force`, `_apply_loads` and `_load_path`, the generator's ratings, `apply_strain`, `failure_probability`, `_carry_away` and `_wreck_spar`, the cloth's wear and `_record_backed` |
| 2 | The bad hand's strain in the same terms, beside the aback figures, each JUDGEMENT; checked against the captain's 22 kn, 12 kn and 1,800 s | **Given and measured** (§2.4.3, §2.2b). Aback: strains from about 28 kn, may carry away from about 35, `LATEEN_ABACK_LOAD` about 2½ (in stays, from about 30 and 36). The bad hand: from about 45 kn and 55, `LATEEN_BAD_HAND_LOAD` about 2 on the two-thirds' pull (the third draft's 1.5 forgot the two-thirds). The mast: with its yard where it carries only its lateen; from about 38 kn aback where it carries more (the tartane's main). **Margins**: in her own tack under 22 kn the yards at 0.55 to 0.60 of their ratings, 0.92 to 0.98 in its top gust (28.6 kn), 1.12 to 1.21 in a squall's top (31.9 kn), never at risk; on the bad hand in 12 kn for 1,800 s at 0.07 to 0.10, nothing worn; from 22 kn to the risk about 14 kn, from 12 kn to the bad hand's strain about 33 kn |
| 3 | What the rule moves: the going about re-measured, the polacre's 164 s to 407 s looked at, what the evolution does to spill or shift the sail in stays and what it should; the words where a sail is aback; any pin | **Measured and read** (§2.2b, §2.4.3a). The 407 s is a failed tack, not a long one: nudge 18's process rule held both lateens aback in their luffing band on both bows (35 to 112 s), she was pushed back across the wind and the helm took her round before the wind; the tack script, having called her through at 49 s, calls no miss after it. The tack and the wear do nothing to a whole lateen today (it is no head, boom or shifted sail); with A1d they draw a left lateen over at "let go and haul" and "wind aft" or begin its change, so that it is aback only from her head through the wind to that order. So worked, the probes' going about moves by −9 to +13 m (the polacre's tack in 15 kn 164 s and 277 m with the yards left, 238 s and 316 m changed). Left undrawn, it holds her aback (588 m on the polacre). The words (§2.4.3a). **No committed pin** |
| 4 | The estimates and the calendar | **A1d two and a half days** (two to three), inside the engine track, merged alone after A1c; the track **about fifteen and a half working days** (fourteen and a half to sixteen and a half), the calendar **three and a half to four and a half weeks** (the plan's §11, §14) |

---

## 1. Item 37: the generator's copy of the sail-force law

### 1.1 What it is

`tools/gen_ships.py:134-140` (read):

```
# The engine's force coefficient at the peak of each class's curve (data/sail_classes.yaml,
# |(C_L, C_D)| at the best angle). Package 10: if the curves change, change these and rerun.
PEAK_COEFF = {"square": 1.23, "studding": 1.25, "gaff": 1.29, "jibheaded": 1.32, "lug": 1.29}
...
PEAK_COEFF["lateen"] = 1.25
```

The engine's own peaks, from its curves as it reads them (`freesail.physics.sails.SAIL_CLASSES`,
`_interp` sampled every 0.01° from 0 to 90°; measured):

| Class | The engine's peak of \|(C_L, C_D)\| | at | `PEAK_COEFF` |
|---|---|---|---|
| square | 1.2265 | 40° | 1.23 |
| gaff | 1.2903 | 30° | 1.29 |
| jibheaded | 1.3220 | 28° | 1.32 |
| lug | 1.2851 | 35° | 1.29 |
| lateen | 1.2462 | 35° | 1.25 |
| sprit | 1.2000 | 90° (the drag alone) | none (a KeyError at the rating pass, `map-engine.md` §4) |
| **studding** | **1.4396** | **35°** (1.35 and 0.50) | **1.25** |

Five agree to the second place; the studding class is 13 per cent short. The cold review's
evidence traces the drift to one table of package 10 (`docs/dev/TuningNotes.md` l. 131, the
studding peak raised to 1.35 for truth 14, and l. 142, `PEAK_COEFF` set to 1.25 in the same
table; `docs/reviews/ColdReview-M7-evidence/records-04-tuning-notes.md`, row 1b). The other
copies of the law the generator keeps agree today: `RHO_AIR` 1.225 and `KNOT` 0.514444
(`gen_ships.py:396-397`; `freesail/units.py:26, 33`), and the shear `(h / 10) ** 0.11`
(`gen_ships.py:444`; `freesail/physics/wind.py:123-124`) (read).

### 1.2 What it is read for

Read, in order:

1. `PEAK_COEFF` is read in one place, `static_kn` (`gen_ships.py:439-446`): the static force of a
   list of (area, centre height, class) sails at a design wind, each sail at its class's peak
   coefficient, with the engine's shear.
2. `design_kn` (449-451) is `static_kn` times `SUSTAINED_FRACTION` (0.85), returned as a
   `DesignLoad` carrying its design wind. A ship's script calls it for every rated spar, naming the
   sails it thinks the spar carries; for a studding-sail boom and a ringtail boom the script names
   the boom's own sail as class `"studding"` at `DESIGN_WIND_KN["studding"]`, 18 kn ("light spars,
   fair-weather sails", 161).
3. `Builder.rate_spars` (1421-1511), **the rating pass**, loads the document through the engine's
   own loader and re-rates every `DesignLoad` spar from every sail whose spar chain the engine
   hangs on it, at the spar's design wind, times 0.85, at least 1 kN. **Studding sails are counted
   only on a spar of class `studdingsail_boom`** (1468-1471): a yard or a mast never carries its
   studding sail's load in the rating. A spar the graph loads nothing on keeps the script's own
   `DesignLoad` (1497-1503). So the studding entry reaches the files in two ways: the studding-sail
   booms and the ringtail booms by the pass, and any boom whose fallback is the script's figure.
4. The `rating_kn` so written is the strain model's yardstick (`freesail/physics/strain.py:1-20,
   94-100`): the load over the rating; above 1.0 the spar wears and the log is warned, above 1.5
   it may carry away at any substep (`0.002 × (ratio − 1.5)²`), and it goes for certain when its
   condition reaches nought.

What it means at sea (arithmetic on the rating, not sailed; judgement on the reading): a boom is
rated for its sail at the peak coefficient in 18 kn, times 0.85. Its sail at the engine's real
peak loads it 1.44 / (1.25 × 0.85) = 1.355 times its rating in that wind, so at the curve's peak
the boom begins to strain at 15.5 kn and may carry away from 18.9 kn. With the engine's 1.44 the
same boom strains from 16.6 kn and may carry away from 20.3 kn. Before the wind the studding
sail works at its drag of 1.25 at 90° and the gap closes; it is widest on the quarter and the
beam, where the sail is near its peak.

### 1.3 What moves if it is made the engine's (measured)

The method: `tools/` copied whole to a scratch tree with `data/` (all but `data/charts/`, which
the generator does not read); the copy's generator run into a scratch folder by a runner that
imports `freesail` from the worktree (asserted) and the copy's `gen_ships.py` and `ships/` after
it; every output compared with `data/ships/` byte for byte, and then parsed and compared figure
by figure (every leaf of every document, lists by `id`).

- **The baseline:** the copy unchanged writes all eighteen files **byte for byte** as committed.
- **`PEAK_COEFF["studding"]` = 1.44**, everything else as it is: **nine files change, nine do
  not.** In the nine, **74 figures move, every one a `rating_kn`**: 70 of studding-sail booms and
  four of ringtail booms (the frigate's, the razee's and the two schooners'), each up by the ratio
  1.44 / 1.25 (15 per cent; 9 to 18 per cent as the tenths round). The byte diffs also carry each
  boom's comment line, "Rating: ... in 18 kn -> N kN.", where the file has one (the hermaphrodite
  brig's booms have none). Nothing else changes: no other spar, no line, no sail, no figure of the
  hull, the crew or the guns.
- **The unrounded 1.4396** gives the same eighteen files as 1.44, byte for byte.
- **Unchanged:** `bilander`, `cutter`, `lugger`, `smack` and the five boats (no studding sails).

| File | Figures | The booms, old → new (kN) |
|---|---|---|
| `frigate-36` | 11 | fore lower 4.2 → 4.9, fore topmast 5.6 → 6.4, fore topgallant 1.8 → 2.1, main topmast 7.0 → 8.1, main topgallant 2.3 → 2.6 (each a pair); ringtail 4.0 → 4.6 |
| `razee-44` | 11 | fore lower 6.0 → 6.9, fore topmast 7.9 → 9.0, fore topgallant 2.7 → 3.2, main topmast 9.4 → 10.9, main topgallant 3.4 → 3.9 (pairs); ringtail 3.7 → 4.2 |
| `sixty-four` | 10 | fore lower 6.1 → 7.0, fore topmast 8.0 → 9.2, fore topgallant 2.8 → 3.2, main topmast 9.5 → 11.0, main topgallant 3.4 → 4.0 (pairs) |
| `seventy-four` | 10 | fore lower 8.4 → 9.7, fore topmast 10.9 → 12.5, fore topgallant 3.9 → 4.5, main topmast 15.0 → 17.3, main topgallant 4.9 → 5.7 (pairs) |
| `brig`, `merchant-brig` | 10 each | fore lower 2.1 → 2.4, fore topmast 2.9 → 3.3, fore topgallant 1.1 → 1.2, main topmast 3.1 → 3.6, main topgallant 1.1 → 1.3 (pairs) |
| `hermaphrodite-brig` | 6 | fore lower 3.4 → 3.9, fore topmast 3.5 → 4.0, fore topgallant 1.3 → 1.5 (pairs) |
| `privateer-schooner`, `topsail-schooner` | 3 each | fore topmast 2.2 → 2.6 (a pair); ringtail 3.9 → 4.5 |

**The cause's mend, measured the same way:** the copy's generator computing its table from the
engine's curves (the greatest \|(C_L, C_D)\| over each class's tabulated points, which is the
curve's peak, the curves being piecewise linear and the norm convex along each piece), rounded to
two places as the table is now: the same eighteen files as 1.44, byte for byte, the sprit class
gaining its 1.20. **Unrounded**, it moves 208 figures in 13 files, 134 of them the rounding's dust
in every class (0.1 to 1.0 kN on masts, yards and bowsprits: the frigate's main mast 669.1 →
668.5); so the mend rounds, as the table's comment always meant.

### 1.4 What reads those figures (measured)

The files read through a redirect in scratch (`sitecustomize` on `PYTHONPATH`, answering every
read of `data/ships/<name>.yaml` from the scratch file of that name, the worktree first on the path
and `freesail` asserted under it, `-p no:cacheprovider`, nothing written to the tree), then the
tests failing there run again on the files as committed. First the studding sails' readers by
name (truths 9, 14, 35 and 7-185, the *Neufchatel*'s truth 9, `tests/test_studding.py` whole: 45
tests), then both tiers whole:

- **Truth 7-185** (`tests/test_known_truths.py:10765`), the generator run into a scratch folder and
  every file compared as text: fails on the moved files, as it must; it is the pin that the files
  are the generator's, and it holds again once the generator and the files move together.
- **Truth 35** (`tests/test_known_truths.py:1587-1633`): its last clause, "every boom whips on
  the first second of the blow and one carries away on the second, before the routine can fire",
  the main topmast boom first. With the booms at the engine's figure **no boom carries away** in
  the 121 s at 32 kn before "shorten sail for weather" takes the studding sails in; every clause
  before it holds. Passes on the committed files.
- **`tests/test_studding.py::test_brought_up_to_six_points_they_shake_strain_and_carry_away[frigate]`**:
  kept at six points for half an hour, her studding sails shivering and flogging, "no boom went".
  Passes on the committed files. (Its schooner case is an expected failure on both.)
- **Held with the moved files:** both of truth 9's (`test_truth_9_royals_and_topgallants_carry_away_in_thirty_five_knots`,
  the frigate and the schooner's `test_truth_9_nothing_carries_away_in_twenty_knots_under_plain_sail`),
  both of truth 14's, the *Neufchatel*'s truth 9 (`tests/test_neufchatel.py:1626`), and the other
  35 cases of `tests/test_studding.py` (its two schooner cases expected failures on both, "the
  schooner's setup in irons").
- **The fast tier whole** on the moved files (`-n 8`, 51 min): **13 failed, 8,337 passed**, 13
  skipped, 1 expected failure; the 13 run again on the committed files: all 13 pass. They are of
  three kinds:
  - **seven byte pins**, the files compared with what the tree's generator writes: truth 7-185;
    `tests/test_ship_particulars.py::test_generator_reproduces_the_committed_files`;
    `tests/test_profile.py::test_the_hook_runs_the_four_ships_modules_after_the_eight_each_writing_its_own`;
    `tests/test_neufchatel.py::test_the_generator_writes_her_file_as_committed_and_reports_its_checks`
    (the hermaphrodite brig's booms); and the generators' reports of the 74
    (`tests/test_bellerophon.py`), of the 64 and the razee (`tests/test_indefatigable.py`) and of
    the schooners (`tests/test_hull_schooner.py`). Each holds again when the generator and the
    files move together, by construction: the moved files are the moved generator's own output,
    byte for byte (§1.3);
  - **five figure pins against the record**, each file compared with git at a commit before its
    profile, every key but the drawing's equal: `test_no_figure_the_physics_or_the_gunnery_reads_moved`
    of the frigate (`tests/test_hull_frigate.py:499`), the brig and the merchant brig
    (`tests/test_hull_brig.py`), and `test_no_figure_the_physics_reads_moved` of the two schooners
    (`tests/test_hull_schooner.py`). These are the pinned figures that move: each would have the
    booms' ratings named in it, old beside new;
  - **one artefact of the probe**: `tests/test_replay.py::test_the_fingerprint_is_of_the_code_and_the_data_and_not_of_the_line_endings`
    failed on its time limit (0.51 s against 0.5 s) under the redirect's extra work at every
    `open` and a loaded machine; it passes on the committed files.
- **The slow tier whole** on the moved files (`--slow -m "slow and not pace"`, `-n 8`, 54 min):
  **12 failed, 530 passed**, 14 skipped, 11 expected failures. Two are the change's: truth 35 and
  the frigate brought up to six points (above). The other ten fail on the committed files too,
  run again there with the same messages, digest for digest: this machine's, not the change's (the
  merchant passage's, the schooner's and the intent's constants, truths 77, 78 and 79 on the
  cruise, the captain's three trials' digests, among them `TRIAL_TRADE_THICK`'s de00808076d8cccf
  the notes already name for re-pinning on the build machine, and the harbour maker's refusal
  worded with the absolute path). The pace tests are not in it; they read no rating.

**Truth 9's strain**, as the lead asked: it is untouched by the change (its two clauses hold). Its
35-knot clause is the royals and topgallants carrying away under all sail, and the studding
booms are not what it counts on; its 20-knot clause sets plain sail, no studding sail. Package
10's `SUSTAINED_FRACTION` of 0.85 was measured on the topgallant yards (TuningNotes l. 142), not the
booms, and does not move.

### 1.5 What I would do (for the owner)

**The plain account.** The game rates each studding-sail boom for the wind it should stand in,
18 knots with its sail drawing its hardest. To do that sum, the ship-building script keeps its own
copy of how hard each kind of sail pulls, and its figure for a studding sail is about a seventh
lower than the figure the sailing itself uses. So every studding-sail boom in the game is rated a
seventh weaker than intended: with its sail drawing its hardest, a boom begins to strain at about
15½ knots where the rule meant 16½, and may carry away from about 19 knots where it meant 20. It
was a slip in one table in package 10, not a choice.

**What I would do:** mend the cause, not the number. The generator reads the engine's own curves
for its peaks (and its air density, knot and shear from the engine's modules), rounded to two
places as the table is, and a test holds the two together, which the cold review found missing
(`code-08-core-ship-physics.md` l. 329). Measured: only the studding-sail booms and the ringtail
booms move (74 figures in nine files, §1.3); the sprit class gains a peak; every other figure of
every file stays byte for byte.

**Where a pinned ship moves**, the owner's to rule:

1. **Truth 35's last clause**, the frigate before the wind in 32 knots: today a boom carries away
   in the first seconds of the blow, before the routine's two minutes can take the studding sails
   in; with the booms rated as intended, the routine takes them in first and nothing carries away.
   The truth's sentence was written to the old figure ("the routine's two minutes are long for
   studding sails before the wind in 32 knots"); I would re-measure it old beside new and keep the
   routine's firing, its count and its timing pinned as they are, the clause about the boom
   carrying away re-stated for the new figure (or moved to a stronger blow where a boom still
   goes before the routine).
2. **The frigate brought up to six points** (`tests/test_studding.py`): today her shivering
   studding sails carry a boom away within half an hour; with the booms as intended, none goes in
   the half hour. Re-measured: how long it takes now, or in what wind it happens in half an hour.
3. **The five records of no figure moved** (`tests/test_hull_frigate.py:499`, the brig's and the
   merchant brig's in `tests/test_hull_brig.py`, the two schooners' in `tests/test_hull_schooner.py`),
   each its file against git before its profile: the booms' ratings named in them as moved, old
   beside new, with this ruling as the reason.
4. **The seven byte pins** (truth 7-185 and its kin, §1.4): passed again by the regeneration
   itself, the files being the generator's.

Nothing else of either tier moves (measured, §1.4); truth 9 and truth 14 hold.

**The other ways**, for the owner's choice: (b) keep 1.25 and write it as a JUDGEMENT with a
reason (light booms rated below their sail on purpose, so that they whip and go first, which is
truth 35's story); or (c) lower the studding curve's peak to 1.25 instead, which moves every
polar with studding sails set and truth 14's "fifteen per cent on a broad reach" (not
recommended). **My pick: (a), the mend**, because the rule the table's comment states ("the
engine's force coefficient at the peak of each class's curve") is the right one and the drift is
a slip.

**Why it is settled before any new file** (the lead's word): of package 90's hulls the *Diana*
and the *Concepción* are ship-rigged and would carry studding sails; generated before the ruling,
both files would be generated again after it.

---

## 2. The lateens: tacked and worn, the yard changed round the mast or left (the owner's answer to question 3)

**Plainly:** the second draft's title was the brief's, B3.1's "worn, not tacked, the yard dipped
round the mast". The owner's answer of 2026-11-18 replaces it (the decisions sheet's question 3 and
Part F, their words verbatim). §2.1 and §2.2 are the second draft's reading and measures, §2.1 with
the machinery the change would take as its model; §2.2a is new, run for this draft; §2.3 is
re-drafted on their shape; §2.4 is new.

### 2.1 What the engine has

Read: a whole lateen is the `lateen` class, on a `lateen_yard` slung at its truss, with its own
curve (peak lift 1.15 at 35°), its sheet floor and its evolutions from package 75's B3.1
(`set_lateen`, `take_in_lateen`, `furl_lateen`, `reef_lateen`, `shake_out_lateen`,
`trim_lateen_sheet`; Ext §3.6 and §3.7). The yard is out of `is_yard` (`parts.py`; Ext §3.3), so
it is no braced yard: no brace order touches it and it makes no mast "a mast with yards". The
dip, the lug's going-about, keys on the sail's `dipping` and its class: `schema.py:2363-2364`
refuses `dipping` on any sail but a lug ("only a lug is dipped"); `dipping_lugs`,
`lugger_lugs` and `_lugs_all` take `cls == "lug" and dipping` (`evolutions/scripts.py:343-366,
8062-8072`); `LugDip` (486) works the dipping lugs of a manoeuvre; `against_the_mast`
(`physics/sails.py:673-680`) loses the cloth of a dipping sail on the weather side of its mast,
and is False for any sail without `dipping`. The settee came into the dip by the `settee` key
(B3.3, Ext §5.4); the 64's and the 74's mizen course, a lateen cut at the mast (`cut_at_mast`),
is not dipped and goes about as a ship's mizen, its curve the gaff's.

**The machinery a change of the yard would take as its model** (read, for this draft). The engine
already changes two yard-sails in going about. The lugger's dipping lugs are lowered at helm's
a-lee, dipped as her head passes the wind and hoisted on the new lee (`LugDip`, `scripts.py:486`;
the manoeuvre's `dip_s`, 90 s by the crew's factor). The bilander's settee is kept drawing in
stays as a ship's mizen and changed last, once the head yards are swung: lowered on deck, passed
round abaft the mast and hoisted on the new lee, and she is not tacked till it is up
(`SetteeChange`, `scripts.py:394`; `SETTEE_DIP_S`, 120 s for a yard of 15 to 17 m, held out of
`tack.yaml` so that `tests/test_catalogue.py`'s pin of the tack's timings does not move). In the
wear the settee is lowered as she bears up and hoisted once the wind is past the stern. Each has
its order by itself: `dip_lug.yaml`, 150 s; `dip_settee.yaml`, 180 s, six able hands,
`too_few: all hands`.

**The rules round going about, every rig's** (read):
- **The stays rule** (`tack.yaml`): she is put in stays only with two knots through the water
  ("She has not way enough on her to stay"). Her way is gone under a quarter of her speed at
  helm's a-lee, or under a length a minute. Hung 180 s from then, or fallen back two points on the
  old side, she has missed stays: her yards are squared and the helm put up, and she falls off on
  the old tack.
- **`put her about`** chooses the tack or the wear by package 45's rule
  (`orders/navigation.py:1132`, `put_about_choice`). It wears with no head sail set, the topsails
  close-reefed, the wind over 30 kn, or after missing stays within the hour. It tacks regardless
  with the land to leeward within two miles. The rules captain gives the order
  (`world/captains.py:3403`).
- **The helm's judgement** for a course across the wake (`navigation.py` l. 565-600) wears a
  vessel with square sail set and gybes a fore-and-after by the helm; a lateen rig gybes, as the
  lugger does.
- **The stern watch** says when a gybe or a shift has left a dipping lug against its mast
  (`navigation.watch_the_stern`), and the rules captain dips it (`Captain._across_the_stern`).
- **A sail taken aback** is said ("Taken aback: the sails pressed against the masts and she lost
  her way.", `physics/hull.py`, `ABACK_SECONDS`). Its cloth wears at three times the rate
  (`physics/strain.py`). Its load on its yard and mast is the load it has, judged against their
  ratings as any load is.
  - **Revised on nudge 18 (read):** only a square sail, or a fore-and-aft sail held on the weather
    side by its sheet, is ever aback. In `_plate_force` (`physics/sails.py:1136-1141`) a
    fore-and-aft sail with the wind on its wrong face and no sheet holding it there "collapses and
    flogs": no lift, and the drag of a plate edge-on. A whole lateen is fore-and-aft and its sheet
    lets it lie to leeward, so it is never `backed`. The ship's line is the integrator's
    (`physics/integrate.py:425-500`): thrust astern for 10 s with a square sail backed or **no set
    sail drawing ahead**, which a rig of collapsed lateens meets.
  - **Nudge 19:** with A1d (§2.4.3) a whole lateen with a side is held aback against its mast once
    the wind has come round onto the side its cloth lies on, and its load on its yard and mast is
    multiplied; today's rule stands for every other sail.

### 2.2 What it does with whole lateens today (measured)

Each rig from the starboard tack, 67.5° off a steady 15 kn northerly, settled under plain sail
(§0); the order given and 900 s run. The files they come from sailed in the same harness for the
comparison.

| Rig | Tack: done at | Tack: what is said of the lateens | Lateens drawing, before → after (kN, force) | Wear: done at | Heave to: lying at 900 s |
|---|---|---|---|---|---|
| Tartane probe (lateen main under a square topsail, lateen mizen) | 89 s | nothing | main 6.66 → 6.70, mizen 1.05 → 1.05 | 487 s | 54.5° off, 3.14 kn; "Hove to on the starboard tack, topsail to the mast" at 125 s |
| Polacre probe (fore and mizen lateens, square main) | 164 s | nothing | fore 5.07 → 5.02, mizen 2.08 → 2.06 | 464 s | 58.6° off, 1.65 kn; main topsail to the mast at 182 s |
| Xebec probe (three lateens) | 101 s | nothing | fore 5.13 → 5.14, main 6.49 → 6.50, mizen 2.10 → 2.10 | 254 s | 53.5° off, 2.89 kn; "under her fore-and-aft canvas" at 126 s |
| The cutter (as filed) | 106 s | | | 458 s | 46.9° off, 1.92 kn |
| The lugger (as filed) | 180 s, her lugs lowered and dipped | | | 171 s, dipped | 83.8° off, 1.65 kn |
| The brig (as filed) | 454 s | | | 474 s | 64.1° off, 1.38 kn |

(A wear with a braced yard waits for it to come round at the wear's brace rate, as B3.4's ruling
3 recorded, so the tartane's, the polacre's, the cutter's and the brig's take 458 to 487 s and the
xebec's, with no braced yard, 254 s. The xebec's research note sailed a probe of its own with no
head sail, `Research-Xebec-2026-11.md` §9: she tacks in 346 s, her leeway to 37° in stays, wears in
167 s and is refused the heave-to; this one keeps the brig's head sails, which carry her round in
101 s and give her heave-to a head sheet to windward. The two agree on what this section draws
from them: no dip, no word of the lateens, the lateens flipped over with nothing done at the
yards.)

What this shows:

1. **No lateen is dipped, lowered, peaked or changed.** Offered `dipping: true`, all three rigs are
   refused at load ("sail 'fore.lateen' is a lateen sail; only a lug is dipped").
2. **Every whole-lateen rig tacks**, faster than the lugger that dips, the lateens' sheets shifted
   over as a gaff sail's are. The tack's lines are a fore-and-after's ("Ready about. Helm's a-lee;
   ease off the head sheets.", "Draw jib; trim aft the head sheets.", "Tacked; braced up on the
   larboard tack"); the polacre's and the tartane's add "Let go and haul" for their square yards.
3. **No lateen loses anything on the tack where it would lie against its mast**: its force is
   the same within one per cent on both tacks (the table), since `against_the_mast` reads
   `dipping` alone.
4. **The wear** shifts the sheets over ("Wind aft. Shifted over the sheets; hauled out and braced
   up.") and says nothing of the lateens. Its first line, "Stand by to wear ship. Up helm; brace in
   the after yards." (`scripts.py:1987-1994`, said whatever the rig), is said by the xebec, which
   has no braced yard; the lugger as filed says the same (observed), and so does any rig with no
   after yards (read), so it is older than package 90 and of the kind the lead's (3) of 2026-11-07
   named for the dismasted rigs' words.
5. **Hove to**, the lateens keep drawing: the xebec forereaches at 2.9 kn and the tartane at 3.1 kn
   after a quarter of an hour, where the cutter lies at 1.9 and the lugger at 1.7. The heave-to's
   driver rule (`after_gaff_sails`) reaches none of the three rigs' lateens (each rig's list is
   empty), so a lateen mizen is kept as a fore-and-after's mizen hove to: item 8's first half, for
   the polacre's document.

### 2.2a Going about today, and with the yard's change modelled (measured, 2026-11-18)

**The harness** is §0's. Seed 7, a steady northerly, no gusts, the starboard tack 67.5° off,
plain sail, settled 1,800 s; the settee brig settled 2,400 s braced sharp up, as
`tests/test_settee.py`'s `_world`. Then the order and 900 s run, in 15 kn unless said.

**Lost to windward** is the cost of going about in metres. It is the ground she would have made
to windward in 900 s holding her board at her settled speed, less what she made.

**The rigs:**
- the three probes of §2.2;
- the xebec note's own probe with no head sail (`Research-Xebec-2026-11.md` §9; "bare" below);
- the cutter, the lugger and the brig as filed;
- the settee's test rig (`tests/rig_fixtures.py`'s `brig_with_settee_doc`), the engine's one yard
  changed in stays today.

**The variants**, made in the process only, nothing in the tree changed (the scripts in the
session's scratch, `p90/goabout/redraft/`):
- **left**: each whole lateen is given a side after load. `dipping` is set on the `Sail` object
  and `lug_side` is its lee side before the order. The schema refuses the key, so no file carries
  it. She comes out of the tack or the wear on the bad hand at the lug's two-thirds.
- **changed in stays**: as left, and each whole lateen draws nothing (`in the gear`) from the
  moment her head is through the wind, for a stated time. It is then set on the new lee with its
  sheet drawn for the close-hauled wind: the settee's act, done by the script.
- **changed in the wear**: the same, from the moment the wind is within 30° of the stern.

The times are the lugger's 90 s and the settee's 120 s, each on every whole lateen of the probe at
once, and **the hulls' own by the lead's ruled rate** (nudge 18: 8.7 s a metre of yard, one able
hand for 2½ m, at least four; §2.4.4), each lateen at its hull's yard's seconds and party,
together where she has hands for all and one after another, the main first, where she has not
(the scripts `p90/n18/measure_seq.py`, run again at 5b987acd). They are JUDGEMENT; no source gives
one, and the probes' own yards are shorter than the hulls' (the tartane probe's main 16.0 m and
mizen 7.0 m; the polacre's fore 17.0 and mizen 10.0; the xebec's main 19.0, fore 17.0 and mizen
10.0; the bare xebec's 27.3, 24.6 and 12.3). The hulls' own seconds:
- **the tartane** with the trader's eight hands: her main 265 s (212 s for its ten hands, by the
  party's numbers term 10/8), then her mizen 133 s, ended 398 s after the change began; with hands
  for both (the coastguard's), 212 s and 133 s together;
- **the polacre**: her fore 165 s and her mizen 83 s together (twelve of the trader's fourteen
  hands);
- **the xebec**: with the King's hands, her main 261 s, fore 235 s and mizen 117 s together;
  with the trader's eighteen, one after another, ended 613 s after it began.

Re-run at 5b987acd, the "left" variants and the third draft's tartane change of 180 s on both yards
at once give its figures again to the metre (326 m and 529 m in stays).

**The tack** (her settled speed beside the rig; then when it was done, her least way, and when she
was back at nine tenths of her speed; the ground lost to windward; for the changes, at 90 s / 120
s / the hull's own seconds at the ruled rate):

| Rig | Today | Yard left | Changed in stays |
|---|---|---|---|
| Tartane probe (6.21 kn) | 89 s; 1.52 kn at 44 s; 107 s; **227 m** | 157 s; **326 m** | **428 / 463 / 521 m** (her eight, the change ended at 420 s; 535 m with hands for both, ended at 234 s) |
| Polacre probe (4.65 kn) | 164 s; 0.12 kn at 92 s; 261 s; **249 m** | 165 s; **275 m** | **291 / 296 / 318 m** (ended at 215 s) |
| Xebec probe, head sails (5.14 kn) | 101 s; 1.64 kn at 84 s; 201 s; **205 m** | 101 s; **309 m** | **370 / 443 / 500 m** (the King's, ended at 305 s; 464 m with the trader's eighteen in turn, ended at 657 s) |
| Xebec, bare (5.02 kn) | 347 s; out at 39° off and 1.1 kn, never back; **1,064 m** | **988 m** | **1,107 / 1,123 / 1,138 m** (the King's) |
| Cutter (6.12 kn) | 106 s; **184 m** | | |
| Lugger, her lugs dipped (7.55 kn) | 180 s; **467 m** | | |
| Settee brig (4.36 kn) | 318 s, the settee changed in stays (down at 155 s, up at 314 s); **327 m** | | |
| Brig (4.88 kn) | 454 s; **552 m** | | |

**The wear** (the same; the changes at the same seconds):

| Rig | Today | Yard left | Changed in the wear |
|---|---|---|---|
| Tartane probe | 487 s; **551 m** | **715 m** | **628 / 658 / 801 m** (her eight; 729 m with hands for both) |
| Polacre probe | 464 s; **602 m** | **647 m** | **599 / 617 / 679 m** |
| Xebec probe, head sails | 254 s; **519 m** | **610 m** | **548 / 575 / 641 m** (the King's; 680 m with the trader's eighteen) |
| Xebec, bare | 150 s; **412 m** | **533 m** | **455 / 489 / 1,311 m** (the King's: she came to stalled 41° off at 1.1 kn, §13 item 12) |

(At the third draft's 7½ s a metre the hulls' seconds were 180, 140 and 225 s, each on every
lateen at once: 529, 306 and 554 m in stays and 726, 649 and 653 m in the wear. They are replaced
by the figures above.)
| Cutter | 458 s; **439 m** | | |
| Lugger, dipped | 171 s; **612 m** | | |
| Settee brig | 478 s, the settee changed (hoisted at 152 s); **590 m** | | |
| Brig | 474 s; **725 m** | | |

**On the bad hand.** Close-hauled 67.5° off, 900 s after, at the lug's two-thirds:
- the tartane probe 6.17 → 5.83 kn, 5½ per cent less;
- the polacre 4.84 → 4.64, 4 per cent;
- the xebec 5.12 → 4.59, 10½ per cent;
- the bare xebec 5.03 → 4.17, 17 per cent, all three lateens on the mast.

The changed variants come out a few per cent under today's speed (the tartane 6.0 kn against
6.17). The scratch change draws the sheet by rule and does not trim it: an artefact of the probe,
not of the change.

**In other winds** (the tack, today; and with the lateens changed in stays at 120 s, "ch."; lost
to windward):

| Wind | Tartane | Polacre | Xebec | Bare xebec | Cutter | Brig |
|---|---|---|---|---|---|---|
| 6 kn | 114 s, 94 m; ch. 179 m | refused: 1.88 kn of way, under the two knots | 227 s, 112 m; ch. 130 m | 401 s, out at 47° off, 143 m | 180 s, 76 m | refused: 1.97 kn |
| 10 kn | 83 s, 152 m; ch. 322 m | 206 s, 159 m; ch. 178 m | 143 s, 147 m; ch. 277 m | 366 s, out at 39° off, 572 m | 117 s, 124 m | 410 s, 217 m |
| 22 kn | 89 s, 341 m; ch. 653 m | 284 s, 592 m; ch. 617 m | 75 s, 286 m; ch. 597 m | 336 s, out at 42° off, 1,614 m | 106 s, 289 m | 179 s, 490 m |
| 28 kn | 98 s, 430 m; ch. 723 m | 184 s, 540 m; ch. 605 m | 65 s, 358 m; ch. 707 m | 333 s, out at 36° off, 1,980 m | 109 s, 390 m | 200 s, 733 m |

**Paying off with no head sail** (the bare xebec, 15 kn, in the process only). Her mizen lateen
was let draw nothing from the moment her head was through the wind until she lay within 10° of
67.5° off, then set again. She tacked in 297 s and made 5.0 kn at 600 s, losing **192 m**. Today
she takes 347 s, lies at 39° off at 1.1 kn and loses 1,064 m. Holding her fore lateen aback for
30 s after the wind made no difference.

**Her head in the wind's eye** (the third draft's "taken aback"). Each probe was settled
close-hauled, then given "steer north" and run 240 s. The table gives the greatest load on each
great yard, its mast and its cloth over its rating (the probes' own ratings, scratch figures),
close-hauled and then over the 240 s after the order:

| Rig | 15 kn | 25 kn | 35 kn |
|---|---|---|---|
| Tartane probe, main yard / mast / cloth | 0.15 / 0.05 / 0.06, the same after | 0.35 / 0.12 / 0.14, the same | 0.58 / 0.21 → 0.22 / 0.24 |
| Polacre probe, fore | 0.09 / 0.05 / 0.05, the same | 0.24 / 0.13 / 0.13, the same | 0.45 → 0.44 / 0.23 / 0.23 |
| Xebec probe, main | 0.12 → 0.13 / 0.01 → 0.02 / 0.05 | 0.30 / 0.04 / 0.13, the same | 0.57 → 0.68 / 0.07 → 0.09 / 0.24 → 0.28 |

In every run "Taken aback: the sails pressed against the masts and she lost her way." came within
18 to 31 s, and nothing strained or carried away.

**Corrected on nudge 18 (re-run, `p90/n18/aback_trace.py`): no lateen was aback.** The table's
"after" figures are not loads aback: they are **the drawing peaks as she fell off and filled**.
- The tartane probe's lateens were `backed` for **no tick** of the 240 s, in 15, 25 or 35 kn. A
  fore-and-aft sail with the wind on its wrong face collapses and flogs (`_plate_force`,
  `physics/sails.py:1136-1141`; §2.1).
- With her head within 30° of the wind her main yard carried **0.009, 0.025 and 0.048** of its
  rating on average in 15, 25 and 35 kn (at most 0.013, 0.032 and 0.055), against **0.15, 0.35
  and 0.58** close-hauled: the drag of a sail edge-on, about a twentieth of the rating in 35 kn.
  Her mizen's the same (0.007 to 0.036 against 0.095 to 0.37).
- The 35-kn peak, 0.58, came at 66 s with the wind 71° on her bow, as she paid off and filled.
- The ship's line came because nothing set drew ahead (the topsail backed, the lateens collapsed:
  `physics/integrate.py:425-500`), not because a lateen was aback.

So the third draft's factor of 3.9 would have multiplied almost nothing: 0.048 × 3.9 is under a
fifth of the rating in 35 kn. The lead's reader found the same.

**A lateen held aback, made in process** (nudge 18's process rule; `p90/n18/aback_held.py`). The
same runs with `_plate_force` told, in this process only, to take a whole lateen with the wind on
its wrong face as held there (the rule a fore-and-aft sail held to windward by its sheet has
today), in place of collapsing:
- under "steer north" in 35 kn the xebec probe's three lateens were aback 31 s, the main yard at
  0.52 of its rating (0.67 at its drawing peak), its mast 0.07; the polacre probe's two 38 s, the
  fore yard 0.32 (0.46); the tartane probe's head never came within 15° of the wind, so hers
  never was;
- in the tack in 15 kn the polacre probe went round in **407 s and lost 725 m**, against 164 s and
  249 m: her lateens aback in stays as her head passed the wind, she paid off to S (175°) before she
  was steadied; the tartane's and the xebec's tacks moved 2 s (91 and 103 s) and 2 and 12 m; in 25
  kn the tartane 93 → 95 s and 387 → 402 m, the polacre 227 → 216 s and 567 → 548 m, the xebec 70 →
  71 s and 320 → 336 m; their wears in 15 kn not at all.

The process rule took a lateen aback whichever side of its mast the cloth lay, which the rule now
designed would not (§2.4.3), so these say only that such a rule reaches the going about and must
be measured there: it is no small key in the strain alone. *Traced on nudge 19 (§2.2b): the
polacre's 407 s is a failed tack, the process rule holding her lateens aback in their luffing band
on both bows; under §2.4.3's rule, which holds a lateen only once the wind has come round onto the
side its cloth lies on, her tack in 15 kn is 164 s and 277 m with the yards left.*

**What this shows:**
1. **The tack is the cheaper today** for every lateen probe with head sails, and their lateens
   cost nothing either way. The tartane probe loses 227 m in a tack and 551 in a wear. The
   period's general rule holds for them as for any vessel (Falconer, VEERING; Röding, WENDEN).
   The bare xebec is the other way: 412 m worn against 1,064 tacked (item 5).
2. **The owner's shape has its trade in the game**, with the lug's two-thirds and the ruled rate.
   On the tartane probe, in the first quarter-hour:
   - a tack with the yard left loses 326 m;
   - a tack with it changed in stays 521 m at her own seconds with the trader's eight hands (535
     with hands for both yards; 428 and 463 at the lugger's and the settee's seconds);
   - a wear with it changed 801 m with her eight (729 with hands for both);
   - a wear with it left 715 m.

   The bad hand goes on costing as the board goes on: the tartane 0.34 kn, about 240 m to
   windward an hour; the xebec 0.54 kn, about 380 m; the polacre 0.19 kn, about 135 m. So leaving
   the yard pays on a short board and the change pays on a long one. Taking today's good-hand
   speed for the changed yard, **the break-even comes, at the hulls' own seconds by the ruled
   rate**:
   - on the tartane probe about **an hour** after the order (63½ minutes with her eight, the main
     and then the mizen; 67 with hands for both);
   - on the xebec's about **45 minutes** (the King's, together; 40 with the trader's eighteen in
     turn, whose wait keeps her other lateens drawing on the bad hand meanwhile);
   - on the polacre's about **34 minutes**.

   At the settee's 120 s on every yard at once they were 49, 36 and 24 minutes, the third draft's
   "three quarters of an hour, 35 and 25". That is arithmetic on the tables, JUDGEMENT on the two
   figures it rests on. It is the 2018 inventory's practice (long boards on the bad hand avoided),
   given by the game's own numbers and not tuned to it. The rules captain's ruled `bad_hand_s`,
   1,800 s (§2.3 item 6), falls a little before every probe's break-even: they shift a little early,
   which errs on the inventory's side.
3. **The same seconds of change cost two to four times as much in stays as in the wear.** On the
   tartane probe 120 s cost 236 m in stays and 108 m in the wear; on the xebec's, 238 and 56. In
   stays she loses way while the sail is out of drawing; in the wear she is running. So the change
   needs no second figure for stays to be dearer there (§2.4.4).
4. **The polacre's square main carries her through her tack**, and her lateens' change costs
   little: 291 to 318 m against 249 (318 at her own seconds). Her probe stops dead in stays today
   (0.12 kn at 92 s) and is refused in 6 kn.
5. **The bare xebec cannot pay off from her tack.** She lies 36° to 47° off at about a knot for ten
   minutes in every wind from 6 to 28 kn, and is called "Tacked" by the steady timeout. Easing her
   mizen lateen as she pays off cures it: 192 m against 1,064. With no head sail, the after lateen
   must be worked to bring her off, as a ship's spanker is eased (§2.3 item 5).
6. **A lateen is never aback in the engine**; her head in the wind's eye costs her way and nothing
   else, her lateens collapsed and flogging (corrected on nudge 18). Forfait's danger is not in the
   engine, and a factor on its load would find almost nothing to multiply: A1d is a new rule of
   force or nothing (§2.4.3). *Nudge 19: built, as §2.4.3's rule, measured in §2.2b.*
7. **No probe missed stays from 6 to 28 kn.** The engine's two-knot floor refused the polacre and
   the brig in 6 kn.

### 2.2b A1d made in process: the going about and the strain (measured, 2026-11-18, nudge 19)

**The harness** is §2.2a's: seed 7, a steady northerly, no gusts, the starboard tack 67.5° off,
plain sail, settled 1,800 s, then the order and 900 s. It was run at e39b84a8 in the session's
scratch (`p90/n19/`: `rules.py`, `a1d.py`, `trace_tack.py`), with `PYTHONDONTWRITEBYTECODE=1`, the
worktree first on the path and `freesail.__file__` asserted under it; no tracked file changed.
- **The side**: each whole lateen given A1a's side in memory (`dipping`, and `lug_side` its lee
  before the order), as §2.2a's variants are.
- **The rule** of §2.4.3, made in the process by wrapping `read_sheet` and `_apply_loads`: the
  cloth kept on its yard's side while the wind comes round ahead, held aback once it has; carried
  over to leeward abaft the beam; shaking, as today, in the luffing band.
- **The evolution's part** (§2.4.3a), done by the script: at "let go and haul" (in the wear, the
  wind within 30° of the stern) each lateen to be left has its sheet drawn over to the new lee; each
  to be changed goes into its gear for its hull's seconds (§2.4.4) and is set on the new lee; one
  waiting its turn is drawn over first.
- **The ratings for the strain**: the probes' whole-lateen yards and masts rated in memory by the
  generator's rule (`tools/gen_ships.py`, `design_kn`: 0.85 of the static load at the class's peak,
  1.25 for a lateen, in 55 kn; a lower yard for its own sail, a lower mast for every sail on it).
  The tartane probe's main yard 59.5 kN and mast 122.8 kN, her mizen's 11.2 kN each; the polacre's
  fore 61.1 and 139.4 kN, her mizen's 21.7; the xebec's fore 61.1 and 139.4, mizen 21.7, main 77.3
  and 276.5 (her main mast counted for the square sails the probe's file still carries, so its
  figure is not a xebec's). Loads below are over those ratings. The factors, where given, are §2.4.3's:
  `LATEEN_ABACK_LOAD` 2½ and `LATEEN_BAD_HAND_LOAD` 2.

**The polacre's 407 s, traced** (`p90/n19/trace_tack.py`; nudge 18's process rule, the probe with
no side, as nudge 18 ran it; reproduced to the second and the metre, 407 s and 725 m):
- from 35 s, her head 17° off the wind and still on the old bow, to 112 s, both lateens were held
  aback in their luffing band, on the old bow and then on the new, their cloth a plate at its best
  angle on the wrong face: the fore lateen's force 2.96 kN at 40 s and 5.02 kN at 48 s, against
  0.50 kN today;
- she lost her way (0.29 kn at 90 s) and was pushed back across the wind: 22° on the old bow at
  140 to 160 s;
- the helm, steering for the new course with the tack already called through the wind at 49 s,
  took her round the long way: 105° off at 250 s, 165° at 300, the wind astern at 400;
- "Tacked; braced up on the larboard tack, heading S (175°)." at 407 s is the steady timeout's end
  of a wear made by accident; she was steady on ENE at 592 s. The tack script did not call it
  missed stays, since it had marked her through the wind at 49 s, and its checks of a miss run only
  before that (`TackScript.tick`, `evolutions/scripts.py:1530-1567`).

**So the 407 s is not a long tack but a failed one**, and the rule, not the seamanship, held her
aback: it held the cloth aback where a seaman lets a sail lift, and on both bows. The same tack
under §2.4.3's rule, which holds a lateen only once the wind has come round onto the side its cloth
lies on: 164 s and 277 m with the yards left, 238 s and 316 m changed. Under the rule as nudge 18
drafted it (the good hand held, the cloth's side left to the deck's lee) no lateen was aback for a
tick: 166 s and 279 m.

**The going about, A1a alone beside A1a with A1d** (lost to windward in the first 900 s, and when
the order was done; this harness draws a left lateen's sheet over at "let go and haul", so its A1a
figures differ by a few metres from §2.2a's, the tartane's tack with the yard left 334 m against
326; the comparison is within the harness, old beside new):

| 15 kn | Tack, yard left | Tack, changed in stays | Wear, left | Wear, changed |
|---|---|---|---|---|
| Tartane (her trader's eight: the main 265 s, then the mizen 133 s) | 149 s, 334 m → 152 s, 337 m | 295 s, 518 m → 297 s, 524 m | 479 s, 688 m → 480 s, 691 m | 476 s, 797 m → 476 s, 799 m |
| Polacre (fore 165 s and mizen 83 s together) | 166 s, 278 m → 164 s, 277 m | 239 s, 317 m → 238 s, 316 m | 462 s, 639 m → 462 s, 641 m | 463 s, 679 m → 463 s, 679 m |
| Xebec, head sails (the King's: 261, 235 and 117 s together) | 101 s, 308 m → 101 s, 309 m | 101 s, 500 m → 101 s, 502 m | 288 s, 613 m → 280 s, 604 m | 333 s, 641 m → 333 s, 641 m |
| Xebec, bare | 347 s, 983 m → 347 s, 993 m | 347 s, 1,138 m with A1d (§2.2a's 1,138 m) | | |

| 25 kn | Tack, yard left | Tack, changed in stays | Wear, left | Wear, changed |
|---|---|---|---|---|
| Tartane | 135 s, 522 m → 137 s, 531 m | 241 s, 693 m → 247 s, 706 m | 593 s, 999 m → 594 s, 999 m | 589 s, 1,136 m → 589 s, 1,143 m |
| Polacre | 277 s, 680 m → 230 s, 604 m | 288 s, 698 m → 293 s, 704 m | 548 s, 1,097 m → 549 s, 1,098 m | 551 s, 1,036 m, the same |
| Xebec | 70 s, 455 m → 70 s, 457 m | 70 s, 759 m → 70 s, 761 m | 220 s, 781 m → 214 s, 772 m | 311 s, 884 m, the same |

- **With the evolution's part, the rule moves the probes' going about by −9 to +13 m**, so that
  A1b's figures (§2.2a) stand within about two per cent. The polacre's 25-kn tack with the yards
  left moves 76 m, in a run in which she falls back across the wind both ways (with A1a alone her
  lateens, drawn over, are aback by their sheets from 58 to 100 s).
- **In an ordinary tack a lateen is aback only from her head through the wind to "let go and
  haul"**, under the 10-s dwell of `_record_backed`, so no "taken aback" line is said. It shows in
  the yard's peak: the polacre's fore yard in 25 kn at 0.29 of its rating against 0.23 with A1a
  alone.
- **If nothing draws them**, the rule holds them aback on the new board: in 15 kn the polacre is
  round in 127 s (her fore lateen aback pays her head off) and sails on at 3.12 kn with both
  lateens aback, 588 m lost; the xebec 96 s and 558 m, aback from 52 to 131 s; the tartane 379 s
  and 764 m; in 25 kn the tartane's great lateen aback holds her head up and she falls back on the
  old tack (1,494 m). The evolution's draw is what keeps the rule from holding her aback longer
  than a seaman would let it.
- **Her head in the wind's eye** ("steer north", 240 s): a lateen is aback only if her head goes
  through the wind. The tartane's and the polacre's did not, in 15 to 35 kn: their lateens were
  never aback and they lost only their way (the tartane's great yard at no more than its
  close-hauled peak, 0.11, 0.22, 0.32 and 0.43 of its rating in 15, 22, 28 and 35 kn). The xebec's
  went through in 15 kn, and her lateens were aback 75 s.

**Taken aback by a shift** (the wind shifted so that it came 20° on her other bow, 120 s, nobody
shifting the sail; the great yards, then the mast where it carries more than its lateen, then the
mizens):

| Wind | No factor: tartane main / polacre fore / xebec main yard | With 2½: the same yards | With 2½: tartane main mast / polacre fore mast | With 2½: the mizens |
|---|---|---|---|---|
| 15 kn | 0.14 / 0.12 / 0.13 | — | — | — |
| 22 kn | 0.28 / 0.25 / 0.26 | 0.70 / 0.62 / 0.65 | 0.46 / 0.36 | 0.72 / 0.63 / 0.66 |
| 28 kn (with 2½, 28.6) | 0.41 / 0.39 / 0.40 | 1.06 / 1.02 / 1.04 | 0.69 / 0.59 | 1.08 / 1.03 / 1.06 |
| 31.9 kn | — | 1.22 / 1.24 / 1.26 | 0.80 / 0.72 | 1.26 / 1.25 / 1.29 |
| 34.3 kn | — | 1.35 / 1.41 / 1.43 | 0.89 / 0.81 | 1.39 / 1.43 / 1.46 |
| 35 kn | 0.56 / 0.58 / 0.59 | — | — | — |
| 40 kn | — | 1.87 / 2.10 / 1.81 | 1.11 / 0.92 | 1.72 / 1.81 / 1.83 |

Nothing carried away in these runs of 120 s (over 1.5 the chance is the strain stream's, 0.002 ×
(ratio − 1.5)² a substep). The log said what the strain model says: "The mizzen mast and the main
and mizzen lateen yards working under the press of sail." in 28.6 kn, "bending like whips; she will
carry them away if sail is not shortened." in 40.

**In the rules captain's winds, with the factors** (peaks over the ratings; the great yard of the
tartane, the polacre's fore and the xebec's fore; nothing carried away in any run):
- **Her tack, the yards changed** (the captain's practice over 12 kn), its seconds aback in stays
  included: 12 kn 0.16 / 0.16 / 0.17; 22 kn 0.55 / 0.56 / 0.60 (with A1a alone 0.22 / 0.18 /
  0.19); 28.6 kn 0.95 / 0.92 / 0.98; 31.9 kn 1.12 / 1.13 / 1.21. The mizens 0.14 to 0.15, then
  0.48 to 0.51, 0.79 to 0.84 and 0.95 to 1.04.
- **Her tack, the yards left** (the captain's practice under 12 kn): 12 kn 0.16 / 0.16 / 0.17;
  15.6 kn, a 12-kn wind's top gust, 0.26 / 0.28 / 0.30.
- **A board on the bad hand**, each yard on the weather side, its sheet drawn round to leeward,
  close-hauled: in 12 kn for 1,800 s the tartane's main yard 0.10 and the polacre's fore and mizen
  0.07 and 0.08; in 15.6 kn the polacre's 0.12 and 0.14. With no factor, in 22, 28 and 35 kn, the
  tartane's 0.15, 0.22 and 0.30 and the polacre's 0.12, 0.18 and 0.28; with 2, in 39 kn the
  tartane's 0.68 (her mizen 0.57), in 45.5 kn the tartane's 0.81 (heeled; mizen 0.70) and the
  polacre's 0.99 and 1.01. The xebec probe, all three lateens on their masts, loses her way and is
  taken aback by her own sheets in most of these runs, so her figures are not the bad hand's.
- **Waiting its turn after a wear** (the trader's yards one after another; the captain wears over
  22 kn): the tartane, her mizen waiting 265 s, in 28.6 kn 0.36 and 0.37, in 39 kn 0.59 and 0.67;
  the trader xebec, her fore waiting 261 s and her mizen 496 s, in 28.6 kn 0.38 to 0.47 and in
  39 kn 0.66 to 0.83.

These are the figures §2.4.3 rules by. They are the probes', with scratch sails on the
generator's rule; each hull's file measures her own.

### 2.3 What the build wants (re-drafted on the owner's shape)

**Plainly:** the second draft built the brief's "worn, not tacked". `tack ship` was answered on a
lateen main in her words with nothing done (`Ship.wears_only()`), and the yard was changed only in
the wear. The owner's answer of 2026-11-18 replaces both. What follows is their shape:
- she tacks and wears as other vessels do, each an ordered evolution with her own words, hands
  and time;
- changing the yard round the mast is a part of either, which may be done or left;
- done, it is done in stays or in the wear, as her practice is by default;
- left, she sails the new board on the bad hand, the sail against the mast and drawing less, until
  she is ordered to shift it.

The engine's parts, in the order I would build them (§14, A1a to A1d; A1d built by the owner's
decision of 2026-11-18, §2.4.3). **The lead ruled them on 2026-11-18 (nudge 18)**: the machinery as
below, each figure JUDGEMENT as written.

1. **The side, and the bad hand's drawing** (A1a).
   - `dipping: true` is allowed on the `lateen` class with no `cut_at_mast` (`schema.py:2363`).
     The side's machinery reads it from `dipping`, not from `cls == "lug"`, wherever the lateen
     needs it. The lug-keyed readers of Ext §5.4 are each read again: `dipping_lugs`,
     `lugger_lugs` and `_lugs_all` stay the lug's.
   - `Sail.lug_side` is kept for it. **Its edges (the lead's item 5, read):** `set_lateen` sets no
     side today and `take_in_lateen` and `furl_lateen` clear none, and the same file sets the 64's
     and the 74's mizzen course and driver (both lateens cut at the mast, read in their files). So:
     - `set_lateen` gains the settee's step `find_its_side` (`set_settee.yaml`: "Its yard aloft
       keeps the side of the mast it hangs on; one never yet hoisted is hoisted to leeward"), of
       nought seconds, **under `if: sail.dipping and sail.lug_side == none`**. A lateen cut at the
       mast never carries `dipping`, so the course's and the driver's set is as it is, and
       `tests/test_lateen.py`'s pins of the set (90 s, no hoist) hold;
     - `take_in_lateen` and `furl_lateen` **clear nothing**: brailed up or furled, the yard stays
       aloft on its side of the mast, as a settee's does (JUDGEMENT: a lateen is never lowered,
       so the lug's clearing at the take-in, `take_in_lug.yaml`, is not its case). Their step
       lists, which `tests/test_lateen.py:395-397` pins, are untouched. A lateen set again after
       she has gone about with it brailed is set where its yard hangs, on the bad hand if so, and
       its set's line says so for the shift ("Set the mainsail; it lies on the mast.", JUDGEMENT on
       the words, a whole lateen's alone, so that the course's and the driver's line is as it is).
   - `against_the_mast` reads it as it is. A lateen on the weather side of its mast draws with
     `LUG_AGAINST_MAST_AREA`'s two-thirds (**ruled: the lug's two-thirds**, JUDGEMENT: Stratico's
     two bellies, one each side of the mast, read as a third lost; GA §5.5). Measured above: 4 to
     17 per cent of her speed. A lateen's own figure, if one is wanted, is set once at A8's tuning.
   - **The watch's line.** The stern watch and the rules captain's `_across_the_stern` read whole
     lateens with a side as they read dipping lugs: a gybe by the helm that leaves a lateen on the
     bad hand is said once ("The wind has come across the stern to the larboard quarter: the
     mainsail lies on the mast; shift it when you will."), and the rules captain shifts it (A1c).
     **The stern watch hears a gybe and not a shift through the bow** (the lead's item 5, read:
     `navigation.watch_the_stern`, `orders/navigation.py:791-812`, records the new side and says
     nothing when the wind has come round "through the eye or before the beam"). A shift of wind
     ahead that takes her round onto the other tack outside a manoeuvre would leave a lateen on
     the bad hand with no word, the silent bad hand of B3.3b over again. So the watch gains the
     bow: the wind come through the eye outside a manoeuvre, and a lateen (or a dipping lug) left
     on its mast, one line for the crossing ("The wind has come round ahead to the larboard bow:
     the mainsail is aback against the mast; shift it when you will.", A1d's rule holding it aback
     till it is shifted or drawn over, §2.4.3a), an event the rules captain reads
     as they read the stern's. Mended at its cause (the owner's rule on mends), the lugger's lugs
     gain the line in that case too: no pinned passage of hers shifts the wind through her bow
     (to grep at the build), and it is named in the card as what moves. The other way is the line
     for a whole lateen alone, the lugger's gap booked.
   - **The heave-to's refusal** in the xebec's words ("She will not lie to under her lateens: there
     is no sail to bring her to.", her A1 (7)) is **keyed on a whole lateen set**, not on "neither
     head sail nor braced yard" alone (the lead's item 5). The five boats (`boat-cutter-23`,
     `-28`, `boat-launch-25`, `-31`, `boat-yawl-16`, one standing lug each) and the bare xebec
     probe are refused today in the same words, run in scratch: "No head sail is set to haul to
     windward, nor a topsail to lay aback." (`scripts.py:2849`; the schooner's case pinned by
     `tests/test_evolutions.py:1102`). Keyed on the lateen, those words stand for every rig but a
     lateen one.
2. **The change, a part of the tack and of the wear** (A1b).
   - **In stays**: once her head is through the wind (after "let go and haul" where she has head
     yards, as the settee is changed last), each lateen to be changed draws nothing while it is
     changed:
     - its parrel eased and its weather runners cast off;
     - its yard peaked up by its halyard and ourses;
     - its car passed round the mast and the tack shifted to the new weather side;
     - the runners set up, the parrel hauled taut and the sheet drawn on the new lee.

     The sources are Lescallier pp. 378-379, Willaumez MUDER and O'Scanlan CIMAR (GA §3.3). The
     yard is **never lowered**: the lug and the settee are lowered, the lateen is peaked
     (Willaumez; the 2018 inventory).
   - **The car passes abaft the mast** (ruled by the lead, 2026-11-18: Willaumez's MUDER;
     JUDGEMENT on the choice). O'Scanlan's CIMAR passes it forward, recorded. The 2018 inventory and
     Lescallier's dinga pass the sheet forward of the mast, which does not settle the car's side
     (GA §3.3). It changes the drawing (V1), not the time.
   - **In the wear**: once the wind is aft, the same, the sail flying before the wind (the
     inventory). **Not the settee's timing**: a settee is lowered at "up helm" and hoisted once the
     wind is past the stern (`WearScript`, `scripts.py:1972-1983`, `may_hoist` at 2057-2062); the
     lateen keeps drawing as she bears up and its change *begins* at wind aft. So the wear takes the
     lateen's change at its own point in its own code path, beside the settee's, and a flag on
     `SetteeChange` would not serve (the lead's item 4).
   - She is tacked or worn when the change is done, as she is not tacked till a settee is up
     (`TackScript._lugs_down`).
   - **A lateen to be left** has its sheet drawn over to the new lee at "let go and haul", with the
     head sheets, or at "wind aft" in the wear (A1d, §2.4.3a): it then fills on the bad hand against
     its mast. Till then, her head through the wind, it lies aback against its mast.
   - **The machinery** is the settee's model with the yard peaked and not lowered: **a new
     `LateenChange` beside `SetteeChange`** (ruled: the lean). `SetteeChange` has one timer for
     every settee and no count of hands (`scripts.py:394-484`: `left_s`, advanced by the
     manoeuvre's factor). The lateen's has, for each yard, its seconds by the ruled rate and its
     party of able hands (§2.4.4), drawn from the hands the going about has called, the party's
     numbers term applied to each, and the yards changed together where the hands serve all and
     **one after another, the main first**, where they do not. Its lines are its own. **It is built
     only when a lateen is to be changed**, as `SetteeChange` is (a `TackScript` holds
     `settee_change = None` until a settee is set and she is through the wind), and it is a plain
     class: not a dataclass of `evolutions/scripts.py` and no subclass of a class the census meets
     (`LugDip` is admitted), since truth 7-606's census of kin takes every dataclass of a module it
     meets and every class of a family it meets (`tools/checkpoint_names.py`, `kin`). Built
     always, or as a record, it would move truth 7-606 (§2.3a).
     The order by itself is a new evolution, `change_lateen`, its scripts on the settee's model
     (the plan's §4 row 3, as before).
3. **How each choice is ordered** (A1b). **The order's words as the lead ruled them (nudge 18)**:
   on a hull with a whole lateen, `shift the <lateen>` and the clause "and shift the lateens" mean
   the yard's change; the sail room's replacement keeps its form with "for"; `dip` stays refused for
   a lateen that is not whole; leaving them is "and leave the lateens" after the order, and no form
   begins with a clause and a comma, since the grammar reads a leading clause with a comma as a
   hail (the lead's reading; read: `orders/grammar.py`'s `_parse` splits the line at its commas and
   matches the verb in the first segment alone, a division's hail, `DIVISION_HAILS`, being the one
   leading phrase it reads away; so "in stays, leave the lateens" was answered "'in stays' is not
   an order this ship understands", observed in scratch at the third draft).
   - **The order's own words, for one going about.** `tack ship`, `wear ship` and `put her
     about` take a clause after the order:
     - "and shift the lateens" or "and leave the lateens";
     - "and shift the mainsail" or "and leave the mizen" names one;
     - "change" is a synonym of "shift", and "and leave the lateens on the mast" of "and leave the
       lateens".

     On a hull with no whole lateen the clause is answered as it is today ("'tack ship' was
     understood, but not 'and leave the lateens'"), so no other ship's answer moves.

     The period's English for the change is "change" or "shift the mizen" (Steel 1794 II, CHANGE
     THE MIZEN; Röding's English for DURCHKAIEN; earlier, Mainwaring c. 1620). No English word for
     leaving it was read (*aller à bido*, *a bisdosso*, *llevar la vela sobre el palo*: GA §2.2),
     so the words are plain. The log says which: "Ready about ...; the lateens to be shifted in
     stays." or "...; the lateens left on the mast."

     The clause is a new kind of modifier. `orders/grammar.py` reads modifiers by kinds written in
     code (`_parse_modifiers`), and today it answers `tack ship and leave the lateens` with "'tack
     ship' was understood, but not 'and leave the lateens'" (observed in scratch, on the lugger as
     filed). So A1b adds the kind there, its words a table in `data/vocabulary.yaml` loaded by
     `orders/vocabulary.py`.
   - **The ship's practice, the default.** It is held on the ship as two settings, in stays and in
     wearing, each "shift" or "leave" (`ship.extra["lateen_practice"]`, a plain dict saved with
     her). **"Shift" in both by default**: the owner's "preferred".
     - It is set for the cruise by an order of its own, **the verb first and the occasion after it,
       with no comma** (revised on the ruling): `leave the lateens in stays`, `shift the lateens in
       stays`, `shift the lateens in wearing`, `leave the lateens in wearing`, and "in going about"
       for both. `shift the lateens` with no occasion is the change itself (item 3a); with "in
       stays", "in wearing" or "in going about" it is the practice. Given while a tack is in hand
       and before its change has begun, the practice set is the one that tack reads.
     - It is answered "Her practice: the lateens left on the mast in stays, shifted in wearing."
     - It is shown in the readings, so that a model at the conn knows what `tack ship` will do.
     - Its orders are a new verb, `leave` (the lateens), and a new modifier kind, the occasion, for
       it and for `shift` on a whole lateen. The verb and the practice's reading are named in the
       primer's going-about chapter (`docs/primer/05-going-about.md`), since
       `tests/test_grammar_book.py` asks every verb of the vocabulary and every reading of the
       registry to be named in the primer.
     - No file key. A hull whose sources give her a practice of her own would take one then
       (JUDGEMENT).
   - **A standing order.** The practice's order is an ordinary order, so the standing dialect takes
     it unchanged. A `when` fires at each coming to hold (`freesail/standing/grammar.py`), so a
     practice set by the wind is a pair:
     - `standing order "fine weather boards": when the true wind is under 12 knots then leave the
       lateens in stays`;
     - `standing order "fresh weather boards": when the true wind exceeds 12 knots then shift the
       lateens in stays`.

     The practice is set as the wind crosses the figure, not held while it stays under it. The
     captains' books already write their standing orders from their thresholds
     (`data/captains/commodore.yaml` l. 156).
   - **The shift alone** (item 3a). `shift the mainsail`, `shift the mizen` and `shift the
     lateens`, with `change` and `dip` as its words for a whole lateen, serve for a lateen left on
     the bad hand by a going about with the yard left, a gybe by the helm or a shift of wind.
     - Refused in words on the good hand: "The mainsail lies to leeward of its mast already."
     - Held while a manoeuvre is in hand, as `settees_held` holds a settee.
     - Kept apart from the sail room's `shift the mainsail for ...` by its "for" (item 3a).
     - "The lateens" is a group of each lateen hull's file (the polacre's design names it, Pol-D
       §4.6; the tartane's and the xebec's files take it too). On the tartane probe, which has no
       such group, `shift the lateens` is answered "There is no such part as the lateens in this
       ship; did you mean the main lateen or the mizzen lateen?" (run).
   - **Every voice gives the same orders**: the player's, a model's at a station, the director's
     and the rules captain's.
3a. **`shift`, `change` and `dip` today, and the whole lateen's routing key** (the lead's item 2).
   - **Today (read: `data/vocabulary.yaml` l. 1924-2000, its `evolutions:` table, `dip` at 1963 and
     `shift` at 1993; `orders/verbs.py:420-430, 473-475`).** A sail verb finds its evolution by
     `verbs.evolution_key(sail, mapping)`: `"settee"` for a settee where the verb's mapping has a
     settee row, `"flying"` for a sail set flying where it has one, else the sail's class. `shift`
     (and `change`, its synonym) maps `lateen` to `shift_sail`, the sail room's replacement; `dip`
     maps `lug` and `settee` and no `lateen`, so a lateen is refused by the default sentence. So
     every lateen goes to the sail room by its class, or is refused.
   - **Run today** (`p90/n18/shift_today.py`, seed 7, 15 kn, plain sail settled 600 s):
     - **the 74 and the 64**: `shift the mizen` begins "Stand by to shift the mizzen course! Aloft
       topmen; lay out, furl and unbend.", clews it up at 116 s, unbends it at 347 s (346 s the
       64), sways the new one aloft at 540 s (538 s) and ends at 1,002 s (999 s): "Shifted the
       mizzen course; the mizzen course bent (No. 2 canvas, new) and set, 20 spare sails left in
       the sail room." `change the mizen` and `shift the mizen for a new one` do the same, line for
       line. `dip the mizen` is refused: "'dip' has no meaning for a lateen sail.";
     - **the tartane probe**: `shift the mainsail`, `change the mainsail` and `shift the mainsail
       for a new one` go to `shift_sail` ("Could not shift the mainsail: There is no spare sail
       left in the sail room ...", the probe's sail room being empty); `dip the mainsail` and `dip
       the mizen` are refused in the same words.
   - **The key, on the settee's model.** `evolution_key` gains **`"whole_lateen"`** for a lateen
     with `dipping` (which the schema allows only on a lateen not cut at the mast), where the
     verb's mapping has that row: `shift: {whole_lateen: change_lateen}` and `dip: {whole_lateen:
     change_lateen}`, beside the class rows as they are. The sail room's replacement keeps its form
     by its "for": `_take_canvas_words` (`orders/grammar.py:396-430`) today takes "for a new one",
     "for another", "for a spare" and "for a new spare" with no trace (only "for the heavy one",
     "for the No. 2" and a sail's name leave a modifier), so it gains a mark that "for" was said,
     and an order of `shift` that carries it is routed by the class, `shift_sail`, before the
     whole lateen's key is read.
   - **What a player on such a hull types** to replace a lateen from the sail room: `shift the
     mainsail for a new one` (or `for a spare`, `for the No. 2`, `for the heavy one`, or the sail
     by its name: `shift the mainsail for the bouffette`, Tar-D §4.1). `shift the mainsail` alone
     there changes its yard round the mast.
   - **Kept:** every order of every committed ship as it is. The 64's and the 74's mizzen course and
     driver are lateens cut at the mast and carry no `dipping`, so `shift the mizen` and `change
     the mizen` on them still shift the course for a spare, and `dip the mizen` is still refused
     in the same words (run above, as today). `bend` and `unbend` of a whole lateen are the class's
     (no `whole_lateen` row); `set`, `take in`, `furl`, `reef`, `shake out` and `trim` too. A lug's
     and a settee's `dip` as they are.
   - **Lost, on a hull with a whole lateen alone:** `shift the mainsail` and `change the mainsail`
     with no "for" no longer go to the sail room. A whole lateen blown out or unbent has no yard's
     change to make, and is answered so: "The mainsail is blown out; there is no yard to shift
     round. Shift it for a new one." (JUDGEMENT on the words, which name the form).
4. **Her own words, hands and time** (A1b).
   - **Words.** The tack's and the wear's lines name the lateens, with A2's words for a rig with no
     braced yard:
     - "Ready about. Helm's a-lee; ease off the head sheets; haul aft the mizen sheet."
     - "Shift the mainsail: ease the parrel, cast off the runners, peak up the yard and pass the car
       round."
     - "Shifted the mainsail; it stands to leeward of the mast."
     - "Tacked; full and by on the larboard tack, the mainsail on the mast." where it was left.
   - **Hands.** All hands, as the tack and the wear call them today (observed for the probes); the
     change's own by the yard: **one able hand for each 2½ m of yard, at least four** (ruled;
     §2.4.4).
   - **Time.** The tack's or the wear's own, and the change's seconds by the yard's length at **the
     lugger's rate, 8.7 s a metre** (ruled; §2.4.4), in the change's own file. So `tack.yaml`'s and
     `wear.yaml`'s timings, which `tests/test_catalogue.py` pins whole, do not move.
5. **The lateen mizen and the fore lateen** in stays and in the wear (A1b; the plan's §4 row 4, on
   the polacre's measure, kept).
   - **A whole lateen on the aftermost mast**, with a mast before it:
     - hauled aft at helm's a-lee (the polacre probe 157 s against 164: Pol-D §5.3);
     - **eased as she pays off on the new board where she has no head sail set**. This is new,
       measured on the bare xebec in §2.2a (192 m lost against 1,064); JUDGEMENT on the act, the
       spanker's "ease off" carried to it;
     - eased at "up helm" in the wear and hauled aft as she comes to.
   - **A tack's end waits for her to pay off, on a rig with a whole lateen set alone** (ruled by
     the lead: keyed on a whole lateen only, so that no other rig's pin moves; §13 item 8). Today
     the steady timeout (`tack.yaml`'s `steady_timeout_s`, 300 s on the new course order) ends a
     tack whether she has paid off or not, and the bare xebec probe is called "Tacked" lying 36° to
     47° off at about a knot (§2.2a). With a whole lateen set, the timeout ends her tack only once
     she has paid off to within 10° of full and by on the new board (the measure of §2.2a's mizen
     eased, JUDGEMENT on the figure); if she has not within a further `stays_timeout_s` (180 s),
     the tack ends in words that say how she lies ("Tacked, but she has not paid off: she lies
     39° off the wind with a knot of way."), so that no tack hangs for ever. Every other rig's
     timeout as it is.
   - **A whole lateen on the foremost mast**, before a square main (the polacre): eased with the
     head sheets at helm's a-lee and drawn at "let go and haul" (Pol-D §5.3 item 1).
   - **Hove to** (the second draft's item 5, unchanged) the mizen is kept set, and
     `after_gaff_sails` never takes a whole lateen, a guard over every file holding it. Taken in
     hove to, the polacre probe falls off past the beam and does not heave to at all
     (`Design-Ship-Polacre.md` §5.2), so the driver rule must not reach it. The engine's heave-to
     forereaches the probes at about three knots today (§2.2, 5); the period's way of lying to
     under lateens (the *cape*) is the hulls' research. A hull that forereaches past truth 12's
     band is mended by her own file's lever (the tartane's great lateen's trim; the polacre's fore
     lateen's sheet), measured on her file.
6. **The rules captain and `put her about`** (A1c). **Revised on the lead's item 6 (read):**
   `put_about_choice` (`orders/navigation.py:1132-1206`) and `judge_course` (l. 469-625) read no
   captain's book: the choice's wind is a module constant, `WEAR_WIND_KN = 30.0` (l. 1041), read
   against the readings' mean true wind (l. 1189-1196), and the course's judgement reads the
   ship's way and `stay_kn`, not the wind's strength. So the third draft's `lateen_tack_kn`, a
   book's key, could not reach either for any ship, and for a ship with no rules captain (the
   player's, a model's at the conn, the director's) there is no book at all.
   - **Package 45's choice gains one reason to wear**: a whole lateen set and the wind over
     **`LATEEN_TACK_KN = 22.0`, a module constant of `orders/navigation.py` beside `WEAR_WIND_KN`**,
     read against the same mean true wind, for every voice that says `put her about` (the player,
     a model, the director, the rules captain, who gives it at `world/captains.py:3403`). It is
     said: "the wind 24 knots: a lateen is not put in stays in a strong wind" (Forfait p. 119;
     JUDGEMENT on the figure, 22 kn, Beaufort's strong breeze; the ruling's "read with defaults"
     is met by the constant, which no book carries).
   - **The tack regardless** with the land to leeward stands, at Forfait's risk (§2.4.3).
   - **The course's judgement takes the same reason.** A course across the wind's eye is put
     about through `judge_course` (`orders/navigation.py`, its eye branch), not through
     `put_about_choice`, and today it tacks any vessel with way to stay at any wind. `steer`,
     `shape a course` and the captains' hourly "shape a course for {mark}"
     (`data/captains/commodore.yaml` l. 151) all come to it. So its eye branch wears a vessel with
     a whole lateen set over `LATEEN_TACK_KN`, read against the same mean true wind (the readings
     it shares with `put_about_choice`), in the same words, and tacks her regardless where there is
     no room to wear (`no_room_to_wear`), as `put_about_choice` does with the land to leeward
     (ruled by the lead; JUDGEMENT: the officer's choice of how to come to a course, not an order
     to tack).
   - **`tack ship` is never turned into a wear.** The player's, the model's and the director's tack
     is a tack.
   - **The rules captain keeps the ship's practice as filed** ("shift" in both), with three
     judgements of their own **from their book, read with defaults** (ruled: written in no committed
     book that would move a count; `Doctrine.threshold(key, default)`, `world/captains.py:968`):
     - **in stays they leave the yards while the wind is under `lateen_leave_kn`** (12 kn,
       Stratico's "con tempo bello"; JUDGEMENT). They do it **by the practice**, not by a clause: as
       the mean true wind falls under 12 kn they give `leave the lateens in stays`, and as it rises
       over 12 `shift the lateens in stays`, each once at the crossing, as a standing order would.
       So when they say `put her about` and the choice tacks her, or their hourly "shape a course
       for {mark}" comes to the course's judgement and it tacks her, that tack reads the practice
       they set, as any tack does; neither road carries a clause, and none is needed;
     - **they shift them when a board on the bad hand has run `bad_hand_s`** (1,800 s, ruled;
       JUDGEMENT: the inventory's long boards avoided; at the ruled rate the probes' break-even is
       34 to 67 minutes, §2.2a, so they shift a little before it) or when the wind rises over
       `lateen_leave_kn`, by `shift the lateens`;
     - after the wind has come across the stern, or round ahead through the bow (item 1), they shift
       a lateen left on the mast as they dip a lug.
   - **The keys**: `lateen_leave_kn` and `bad_hand_s` only, read with their defaults where a book
     lacks them, and **written in no committed book**. The corsair's new book (N2) may carry them
     with their sources (package 116's road), since it moves no committed count but its own. If a
     committed book ever gains one, `tests/test_subtypes.py:463-490` moves with it: the indiaman's
     book must hold the merchant's thresholds key for key (l. 465) and the revenue cutter's must
     differ from the cruiser's by `man_of_war_nm` alone (l. 487), so a key in the merchant's or the
     cruiser's book is a key in its fellow too, or those two pins fail.
7. **Taken aback, and the bad hand, in a breeze** (A1d): **built, by the owner's decision of
   2026-11-18** (§2.4.3). A whole lateen held aback against its mast once the wind has come round
   onto the side its cloth lies on; its pull on its yard and mast multiplied by `LATEEN_ABACK_LOAD`
   (about 2½) aback and by `LATEEN_BAD_HAND_LOAD` (about 2) on the bad hand; the tack and the wear
   draw a left lateen over at "let go and haul" and "wind aft" (§2.4.3a). The figures are the lead's
   to rule.
8. **The lateens' own evolutions** (A1a). `set_lateen`, `take_in_lateen`, `furl_lateen` and
   `reef_lateen` are sized by the ship's data or `too_few: all hands` (the second draft's item
   7); `set_lateen` finds a whole lateen's side (item 1). The heave-to's refusal in the xebec's
   words is keyed on a whole lateen set (item 1).
9. **The words** (A2), **widened to its cause, and the pins it moves** (the lead's item 3). The
   third draft named two lines: "brace in the after yards" left out where she has no after yards,
   and "braced up on the ... tack" where she has no braced yard. The same cause says "braced" of a
   rig with no braced yard in two more: the wear's end (`{braced}` in `wear.yaml`'s
   `on_complete`, "braced sharp up" from `WearScript.words`, `scripts.py:2140-2150`) and the
   wear's wind-aft line ("hauled out and braced up", `scripts.py:2051-2054`). Under the owner's
   rule on mends all four go. **Run as they are** in scratch (`p90/n18/transcripts.py`, the test's
   own harness: seed 7, 15 kn, 292.5°, plain sail braced sharp up, settled 2,400 s), the lugger's
   lines are her pins line for line; **what A2 makes of them** is by reading (the new words
   JUDGEMENT), every tick the same:

   | Pin | Tick | Today (run) | With A2 |
   |---|---|---|---|
   | `LUGGER_TACK` (`tests/test_settee.py:1418-1437`) | 180 | "Tacked; braced up on the larboard tack, heading ENE (68°)." | "Tacked; full and by on the larboard tack, heading ENE (68°)." |
   | `LUGGER_WEAR` (l. 1438-1456) | 1 | "Stand by to wear ship. Up helm; brace in the after yards." | "Stand by to wear ship. Up helm." |
   | `LUGGER_WEAR` | 36 | "Wind aft. Shifted over the sheets; hauled out and braced up. Lowered the foresail and the mainsail to dip them." | "Wind aft. Shifted over the sheets. Lowered the foresail and the mainsail to dip them." |
   | `LUGGER_WEAR` | 171 | "Wore ship; braced sharp up on the larboard tack, heading ENE (68°)." | "Wore ship; full and by on the larboard tack, heading ENE (68°)." |
   | `tests/test_evolutions.py:1169-1171`, the lugger's case of `test_with_no_head_yards_the_wear_squares_none` | — | "Wind aft. Shifted over the sheets; hauled out and braced up." | "Wind aft. Shifted over the sheets." |

   Every other line of the two transcripts stands as it is (the tack's nine others; the wear's
   six others). The third draft's two lines are the first and second rows; the third, fourth and
   fifth are the cause's.
   - **The cutter and the smack** (run, the same harness): each has head yards and so a braced
     yard, and neither has after yards. Their wear's first line, "Stand by to wear ship. Up helm;
     brace in the after yards.", becomes "Stand by to wear ship. Up helm."; their wind-aft line
     ("Wind aft. Squared the head yards; shifted over the sheets; hauled out and braced up.") and
     their ends ("Tacked; braced up ...", "Wore ship; braced sharp up ...") are true of them and
     stand. **The wear's first line only**, as the lead's reader found. No test pins it for either
     (grepped: `tests/`). The smack was refused `tack ship` from the harness ("She is not
     close-hauled; bring her by the wind before going about.").
   - **The claim corrected.** The third draft's A1b row said the lugger's and the settee's paths
     stood "with their guard sets" (`tests/test_settee.py`, `tests/test_lug.py`, truth 7b-111).
     They stand under A1a to A1c, which key on a whole lateen; but A2 moves the lugger's two
     pinned transcripts in that same guard set, by the lines above. So **A2 is merged alone,
     before A1a**, its moves recorded old beside new and passed by another reader, and the guard
     set then holds unmoved through A1a to A1c (the plan's §9.1 and §10.2).

**What it moves:** nothing of the eighteen files by A1a to A1c. None carries a whole lateen; the
64's and the 74's mizen courses are `cut_at_mast` and stay a ship's mizen. Every part is keyed on
a whole lateen with `dipping` (A1a, A1b) or on a whole lateen set (A1c's reason and judgements),
but for the bow's line if it is mended at its cause (item 1: the lugger's lugs, in a case no pin
is expected to hold). What moves by count:
- the library's evolutions, by `change_lateen` (`tests/test_agents.py`);
- the vocabulary's order lists: the clause, the practice's orders and its verb `leave`, `shift`
  and `dip` for a whole lateen;
- the primer's going-about chapter, which names the practice's new verb and its reading, so that
  `tests/test_grammar_book.py`'s two primer tests pass again (item 3);
- no captain's book (the two keys read with defaults; item 6).

A2 moves the five pinned lines of item 9, words only.

**No checkpoint name moves.** `lateen_practice` is a plain dict of strings, as `COURSE_PENDING`
is, and the checkpoint's list (`freesail/core/checkpoint_names.py`, `ADMITTED`) holds the classes
and functions a pickle's loading calls, not the keys of `ship.extra`. A `LateenChange` becomes a
name only if one of the game's own checkpoints holds one, so it is built only when a lateen is to
be changed, and is a plain class, neither a dataclass of `scripts.py` nor of a family the census
meets (item 2; §2.3a): truth 7-606's `kin` case reads every dataclass of a module the census met
and every class sharing a base with one it met, built or not. No scenario of this card sails a
lateen hull, so the census meets none in play.

### 2.3a Where the settee's change is woven in, and the lateen's (the lead's item 4)

Read: `SetteeChange`, `settees`, `settees_held` and their callers grepped through `freesail/` (306
lines name the settee, comments among them: 233 in `evolutions/scripts.py`, the rest in `runner.py`,
`orders/verbs.py`, `ship/schema.py`, `ship/parts.py`, `api/queries.py`, `evolutions/trim.py`,
`world/ships.py` and `crew/hands.py`). Eighteen places carry the settee's change or its kin; the
lead's reader counted about fifteen. The last column says what the lateen's change does there.

| # | Place (read) | The settee there | The whole lateen's |
|---|---|---|---|
| 1 | `settees`, `settees_held` (`scripts.py:362-378`) | the settees set, by id | **mirror**: `whole_lateens`, `lateens_held` (a whole lateen with `dipping` set) |
| 2 | `Script._hold_settees`, `order_settees` (`scripts.py:982-1004`); `Runner._settees_only` (`runner.py:900-916`, read at l. 426 and 1078-1087) | a manoeuvre that may change one holds it from the order, and work given before on it alone does not keep the manoeuvre waiting | **mirror**: the lateens held from the order by every manoeuvre that may change one, and the runner's rule for them (the shift alone held while a manoeuvre is in hand, §2.3 item 3) |
| 3 | `SetteeChange` (`scripts.py:394-484`) | one timer, no hands counted, lowered and hoisted | **its own**: `LateenChange`, each yard's seconds and party, together or the main first, peaked and never lowered (§2.3 item 2) |
| 4 | `TackScript`: kept drawing with the booms till changed (1464-1484), begun last after "let go and haul" once through the wind (1638-1656), advanced (1520-1522), the end held for it (`_lugs_down`, 1494-1497), its seconds in `remaining_s` (`_settee_to_change_s`, 1817-1848), its sheet's lead (1767-1771) | changed last in stays | **mirror**, the aftermost lateen hauled aft and the fore eased as §2.3 item 5 says; and the end waiting for her to pay off (item 5) |
| 5 | `WearScript`: lowered at "up helm" (1972-1983), hoisted with `may_hoist` once past the stern (2057-2062), the end held (2122), trimmed for the course (2126) | lowered as she bears up | **its own point**: the change begun at wind aft, the lateen drawing till then (§2.3 item 2); the end held and the trim mirrored |
| 6 | `FillAwayScript`: `_dip_settee` and the phase `dip_settee` (3237-3392), `remaining_s` (3491-3498), `left_words` (3508-3512) | one on the weather side of the tack she fills on is dipped first, as she lies | **mirror**: a lateen on the weather side of that tack shifted first (else she fills with it on the bad hand) |
| 7 | the hove-to watch: `_settees_against_their_masts` and `_hove_to_no_longer`'s forced-round dip (`scripts.py:2505-2700`) | forced round lying to, the watch dips a settee left on its mast (package 75, the lead's ruling (3)(i) of 2026-11-10) | **mirror**: leave it out and B3.3b's silent bad hand comes back, a lateen forced round hove to sailing on against its mast with no word (`docs/dev/TuningNotes.md`, B3.3b's "Found on the way" 1) |
| 8 | `BoxHaulScript` (`_settee_at_box`, `_settee_at_come_to`, 5251-5415), which `wear_short_round` also runs (`data/evolutions/wear_short_round.yaml`, `script: boxhaul`) | lowered at the box, hoisted as she comes to | **mirror**, the change begun as the box-haul's wind comes aft |
| 9 | `BoxOffScript` (5467-5535) | one on the weather side of the tack she is boxed off on is changed; left set, it stayed on the mast unsaid (B3.3's review) | **mirror**, for the same silent case |
| 10 | `HeaveToScript` (2930-2938), `SETTEE_KEPT_HOVE_TO`, `_kept_after_sails` (2266-2269) | kept set as the driver | **not mirrored**: a lateen mizen is kept set hove to by its own rule, `after_gaff_sails` never taking it (§2.3 item 5) |
| 11 | `ScudScript` (5888-5958): brails the drivers, `after_gaff_sails`, which `after_gaff_sails_all` widens to the settee (8634-8645) | brailed up with the drivers | **not mirrored**: the lateen is no driver; a scud that takes the wind across her stern is the stern watch's (item 1) |
| 12 | `LieATryScript` (5699-5734) | clewed up lying a-try | **not mirrored**: a lateen lies a-try as she is today; forced round, the hove-to watch's (row 7) |
| 13 | `BackAndFillScript` (6011-6016) | handed with the courses | **not mirrored** |
| 14 | `ComeToAnchorScript` (7275, 7341-7342) | in its gear with the square sails | **not mirrored** (the lateen's take-in, as today) |
| 15 | `GetUnderWayScript` (8248-8250), `_set_fore_and_aft` (8055-8056), `_lugs_all` (8062-8072) | loosed aloft with the topsails; its yard aloft; never among the lugs | **its side found** by `set_lateen` (item 1); no more |
| 16 | `runner.py`: the class routing (`wanted == "settee"`, l. 707), the sheet's trim range (l. 789), the great sail's all-hands files (l. 1510, 1922) | the settee's own evolutions and trim | **mirror** for `change_lateen`'s routing and its `too_few: all hands`; the trim as the lateen's today |
| 17 | `orders/verbs.py`: `evolution_key` (420-430), `_take_in_kind` (525-537), the brace refusal (1593-1608) | its rows; its take-in words; "trimmed with its sheet" | **mirror** `evolution_key` (§2.3 item 3a); the rest as the lateen's today |
| 18 | `evolutions/trim.py` (282, 401), `api/queries.py` (336-340, 450-461), `ship/parts.py` (`Sail.settee`, the checkpoint's state, 302-370) | its sheet's lead; `yard_lowered` and the sheet's side served to the viewer; its flag saved | **the viewer's** (V1: the yard peaked while it is changed, its side); `lug_side` already saved |

**Eleven are mirrored or given their own** (rows 1 to 9, 16 and 17), and one is the viewer's
(18). Rows 10 to 15 are the settee's as a ship's mizen or course, which a lateen is not; each is
named so that the builder reads it and leaves it on purpose.

**What `SetteeChange` lacks for the lateen** (the lead's item 4): the hands for each yard, and "one
after another, the main first". It has one timer for all its sails and counts no hands, advancing
by the whole manoeuvre's crew factor. The lateen's carries a party for each yard from the ruled
rate (§2.4.4) and the order of the yards.

**Built only when one is needed**, as `SetteeChange` is, a plain class: or truth 7-606 moves
(item 2 above).

**The estimate.** The third draft gave A1b a day and a half. Item by item (JUDGEMENT, on the
places above and the settee's tests beside them, `tests/test_settee.py`, which A1b's tests
mirror):
- `LateenChange`, its parties and its order: half a day;
- rows 1, 2, 4 and 5 (the holds, the tack, the wear at its own point): one day;
- rows 6 to 9 (fill away, the hove-to watch's forced round, the box-haul and wear short round, box
  her off) with their silent cases' tests: one day;
- the clause, the practice's verb and its occasion, the readings' row and the primer: half a day;
- the tack's end waiting for her to pay off: a quarter;
- the probes' going about re-measured old beside new and the guard set: a quarter.

So **three and a half days**, within the reader's three to four. (A1a's edges, item 1, and its
routing, item 3a, are A1a's: about half a day more there than the third draft allowed.)

All of it is judgement, to be measured at the build as B3.3 was.

### 2.4 What going about costs and risks under a lateen (the lead's item 3)

From GA §5 where the sources speak; JUDGEMENT where they do not; the game's figures measured on
the probes where they can be (§2.2a).

#### 2.4.1 Her way and the wind she needs to stay

- **The sources** give no figure for a lateen vessel (GA §5.1). A lateen lies at five points, a
  square-rigger at six (Lescallier p. 380; Steel I p. 237). The mizen was added to lateen vessels
  to bring them to the wind (Lescallier pp. 393-394). In general a ship misses stays for want of
  way (Steel II p. 316), and in a violent wind and sea she wears (Falconer, VEERING; Röding,
  WENDEN).
- **The game** keeps the stays rule as it is for every rig: two knots to be put in stays; her way
  gone at a quarter of her speed or a length a minute; 180 s hung. There is no figure of the
  lateen's own (JUDGEMENT: none is sourced, and the tartane and xebec probes stay from 6 to
  28 kn, the polacre's from 10, refused for want of way in 6: §2.2a). Two things are her own:
  - her mizen eased as she pays off where she has no head sail (§2.3 item 5);
  - `put her about`, and the course's judgement, wearing her over `LATEEN_TACK_KN`, 22 kn (§2.3
    item 6);
  - on a rig with a whole lateen set, her tack's end waiting for her to pay off (§2.3 item 5).
- **Whether a hull tacks slower or less surely than her probe** is her file's to measure against
  her truth. The tartane probe tacks faster than the cutter today (89 s against 106). GA §5.1's
  judgement that the tartane is slower in stays than the xebec is not the probes'; her truth's band
  is set on her file.

#### 2.4.2 Missing stays

- **The sources** speak in general only (Steel II, MISS STAYS; Stratico, RICUSARE DI VIRARE, then
  worn; GA §5.2).
- **The game** keeps the rule as it is. The yard's change is begun only once her head is through
  the wind (§2.3 item 2), so a miss costs a lateen what it costs any vessel: the yard was never
  moved and lies on the good hand for the old board. That is the settee's own case, pinned in
  `tests/test_settee.py`: a miss before she is through leaves `settee_change` None. After a miss
  `put her about` wears her within the hour (package 45).
- **Hanging head to wind in a breeze**, her lateens shake in their luffing band and she loses her
  way (§2.2a, corrected on nudge 18). With A1d (built, §2.4.3) a lateen is held aback against its
  mast once her head is through the wind, until "let go and haul" draws it over or begins its
  change (§2.4.3a); hung in stays, a foremost lateen is kept aback to pay her head off.

#### 2.4.3 Taken aback, and the bad hand, in a breeze (A1d: built, by the owner's decision)

**Decided by the owner, 2026-11-18** (through the lead's note of 22:35 UTC, nudge 19), verbatim:
"A lateen taken aback should increase the strain on the mast, as a backed square sail does, so
that on the worse tack and not dipped, the sail may strain the mast and, in high enough wind,
risk damage." It asks two things, and A1d builds both: **a lateen taken aback** loads its mast as a
backed square sail does; and **a lateen on the worse tack and not dipped**, left on the bad hand
lying against its mast, may strain the mast too, and in wind enough risk damage. A1d is a step of
the card, not an option (nudge 18's option, set out in this section's last revision, is
withdrawn). The lead's recommendation and the plan's pick were the other way; this is the
owner's, and it is settled.

- **The sources:**
  - in a strong wind, lateens taken aback ("coëffées", making "chapelle") cost the masts or the
    vessel, the canvas wrapping the mast so that the yard cannot be lowered (Forfait p. 119);
  - the long weak yard is broken by the first squall in a storm (p. 120);
  - the lateen is more liable to it than a lug (Fincham p. 59);
  - the yard left on the mast is dangerous but in fine weather (Stratico, BISDOSSO);
  - which goes first, and at what wind, none says (GA §5.3).

**How a backed square sail's load reaches its yard and its mast today** (read; the road A1d
takes, as the owner asks):
- **The force.** A square sail with the wind on its fore face is a plate aback: `_plate_force`
  (`physics/sails.py:1104-1152`) gives it the class curve's lift and drag at its incidence and
  sets `backed` once the incidence passes the luff angle (l. 1136-1139). No factor is put on a
  backed sail's force; it is the plate's.
- **The load.** `_apply_loads` (l. 1515-1538) puts the sail's whole pull on each spar of its chain,
  `_load_path` (l. 1463-1491, `ship.spar_chain(sail)`: its yard, then the mast it hangs on, then
  any spar beneath, "each spar carries everything above it"); its sheet carries
  `SHEET_LOAD_FRACTION` (0.6) of it or the boomed sail's lever, its halyards
  `HALYARD_LOAD_FRACTION` (0.5), its braces `BRACE_LOAD_FRACTION` (0.3), its stay 1.0.
- **The ratings.** The generator's rule (`tools/gen_ships.py`): a spar's rating is the sustained
  load in its design wind, `design_kn` (l. 449-451), the static force at the class's peak
  coefficient (`static_kn`, l. 441-447; `PEAK_COEFF["lateen"]` 1.25, l. 140) times
  `SUSTAINED_FRACTION` (0.85, l. 149), in 55 kn for a lower mast and its yard (`DESIGN_WIND_KN`,
  l. 153-162): a lower yard for its own sail, a lower mast for every sail on it.
- **The strain and carrying away.** `physics/strain.py`, `apply_strain` (l. 186-230), judges each
  part's load over its rating once a tick (`Part.strain_ratio`, and a spar's with the catharpins'
  `rating_factor`, `ship/parts.py:160-162, 271-274`; the seaway's factor on spars and lines):
  - over 1.0 (`DECAY_RATIO`) the part loses 2 points of condition a minute for each unit over
    (`DECAY_POINTS_PER_MINUTE`), and is warned once in ten minutes: "working under the press of
    sail." (`_warn`, l. 368-415);
  - over 1.5 (`CARRY_AWAY_RATIO`) it may carry away at any substep of 0.25 s, with the chance
    0.002 × (ratio − 1.5)² (`CARRY_AWAY_COEFFICIENT`; `failure_probability`, l. 296-305; `_fails`,
    l. 347-355), drawn from the strain stream, and is warned "bending like a whip; she will carry
    it away if sail is not shortened.";
  - at nought condition it carries away for certain;
  - carried away, `_carry_away` (l. 510) and `_wreck_spar` (l. 613) wreck the spar and every part
    `Ship.dependents()` gives for it: a yard takes its sail and its lines, a mast its yards, sails
    and everything above it.
- **The cloth** is judged against its own cloth rating with the plain force (a set sail blows out
  over `BLOW_OUT_RATIO`, 1.8) and wears at three times the rate while aback (`cloth_wear_per_hour`,
  l. 260-277; `CLOTH_WEAR_FLOGGING_FACTOR`, l. 121). `_record_backed` (`physics/sails.py:1281-1325`)
  says "Main course taken aback." once the sail has been aback `BACKED_DWELL_S` (10 s, l. 332).

**Today a whole lateen is never aback** (§2.1, §2.2a): its one sheet, held to no side, lies on the
deck's lee (`read_sheet`, `evolutions/trim.py:473-478`), so its cloth goes over the moment the
deck's wind crosses the bow, as a gaff sail's boom swings over in stays; with the wind on its wrong
face in the narrow band where the wind at its own height and the deck's disagree it "collapses and
flogs" (`physics/sails.py:1140-1141`). And no evolution touches it in going about (§2.4.3a, below).

**The rule of force (A1d), a physics addition in `physics/sails.py`** (JUDGEMENT throughout: the
reading of Forfait p. 119 and of the period's "the sail on the mast"; GA §3.3). **A whole lateen
held aback against its mast.** What it reads:
- **the whole lateen**: a sail of class `lateen` with no `cut_at_mast`, carrying A1a's `dipping`
  and a side (`Sail.lug_side`: the side of its mast its yard and cloth hang on). No committed sail
  carries the key, so no other sail's force moves;
- **the side**, kept by the mast. Its one sheet, held to no side, holds its cloth on its yard's
  side, not on the deck's lee: the mast stands between the cloth and the other side, so it cannot
  blow over as a gaff boom does. It goes to the other side only when its sheet is drawn over by
  hands (§2.4.3a: the tack at "let go and haul", the wear at "wind aft", `trim`, the watch's
  shift), when its yard is changed round (A1b), or when the wind comes round **abaft the beam**
  onto the side it lies on, which carries the cloth over against its mast to leeward, its sheet
  with it, as a gybe does (the bad hand of A1a if it is not the yard's side). A sheet drawn to a
  side keeps that side (`held_side`), the lee included, for a whole lateen alone
  (`evolutions/trim.py`, `set_sheet_angle`, l. 513-558, which today records a single sheet's side
  only when it is not the lee);
- **the wind's face**, at the sail's own height, as `_plate_force` reads it (`on_drive_face`,
  l. 1134). With the wind come round **ahead** onto the side its cloth lies on (her head through
  the wind with the yard not yet changed or the sheet not yet drawn, a shift of wind, the helm
  carrying her head through), its sheet's side is the weather side and `_read_rig` takes it as
  held (l. 600-606), as a fore-and-aft sail held to windward by its sheet is held today. It stands
  as a plate aback, its cloth pressed on its mast, its force aft and to the other side;
  `_plate_force` (unchanged) sets `backed` when its incidence passes its luff angle (l. 1138-1139),
  and `_record_backed` says "Main lateen taken aback." after 10 s, as of a square sail.
- **Not in the luffing band.** With her head luffed inside its sheet's angle and the wind still on
  the far bow, a lateen lifts and shakes, as today, and is not held: the cloth can swing in to the
  mast's line and no further, so it is not pressed until the wind has crossed. Nudge 18's process
  rule held it there too, on both bows, and made the cloth a plate drawing backwards at its best
  angle: that is what threw the polacre probe back (§2.2b).

**The strain: to the mast as well as the yard, by the engine's existing strain and carrying-away.**
In `_apply_loads` (l. 1515-1538), the whole lateen's pull on each spar of its chain (`_load_path`:
its lateen yard, then its mast and any spar beneath) is multiplied:
- by **`LATEEN_ABACK_LOAD`** while it is held aback;
- by **`LATEEN_BAD_HAND_LOAD`** while it lies against its mast on the bad hand (`against_the_mast`,
  l. 673-679: its yard on the weather side, its cloth drawn round the mast to leeward at the lug's
  two-thirds, `LUG_AGAINST_MAST_AREA`).

Both are module constants of `physics/sails.py` beside `LUG_AGAINST_MAST_AREA`. The cloth and the
lines take the plain pull as now. Nothing in `physics/strain.py` changes: the ratio, the wear over
1.0, the warning, the chance over 1.5, the certain failure at nought and `_wreck_spar` with its
dependents are the engine's as they are. **No new kind of damage**: a yard or a mast carried away
as any spar is, its sail and gear with it. *Widened 2026-11-23 (the lead's nudge 55; the lateen
hulls' list, items 1 and 3):* `physics/strain.py` changes in its warning alone, never a figure of
load, strain or damage. `_apply_loads` marks each spar of the chain with what presses it, aback or
the bad hand (`lateen_pressed`, under `strain.LATEEN_PRESSED`, for each substep as its load), and
`_warn` counts the ten minutes' rate against the part and its cause, so a lateen coming aback or
onto the bad hand is warned for as it comes, whatever was said before, in words that say why and
what eases it: "Main lateen yard bending like a whip, the mainsail lying on the mast; she will
carry it away: let fly its sheet or shift it." (aback, "..., the mainsail aback against the mast:
let fly its sheet, shift it or box her off."). Before, the one warning a part in ten minutes let a
yard warned on the good hand carry away on the bad hand unwarned (the xebec probe in 57 kn), and
"if sail is not shortened" pointed the wrong way of a lateen whose taking in the game holds while
it is aback. No committed sail is a whole lateen, so their warnings keep the rule as it was (the
eighteen in gales, old beside new, in the engine's report).
- **Why a factor at all** (measured, §2.2b). "As a backed square sail does", the plate's force on
  the chain and no more, a lateen taken aback with her way on (the wind shifted onto her other bow)
  carries on its yard 0.12 to 0.15 of the generator's rating in 15 kn, 0.25 to 0.29 in 22, 0.39 to
  0.42 in 28 and 0.56 to 0.60 in 35: one and a half to two times the sustained design load by the
  wind's square. It would strain only from about 45 kn and could carry away only from about 56 kn,
  and a backed square sail, loaded and rated by the same rule, no sooner (read, not run): the danger
  would come in no wind a lateen is carried in (the tartane's great lateen is in before 30 kn, Tar-D
  T-6). On the bad hand, at its two-thirds, the load is about half that (0.7 of the design load by
  the wind's square), straining only from about 65 kn. The owner asks that in high enough wind it
  risk damage. The factor is the sail pressed on its mast bearing on it directly and the yard bent
  across the mast at its parrel (Forfait pp. 119-120), JUDGEMENT on the reading.
- **The figures, each JUDGEMENT for the lead's ruling** (measured on the probes rated by the
  generator's rule, §2.2b):

  | | Strains its yard from | May carry its yard away from | The factor | The earlier draft's |
  |---|---|---|---|---|
  | **Aback**, taken by a shift with her way on | **about 28 kn** (1.02 to 1.08 of the rating in 28.6 kn) | **about 35 kn** (1.35 to 1.46 in 34.3; 1.72 to 2.14 in 40) | `LATEEN_ABACK_LOAD` **about 2½** | 28 and 34 kn by 3.9, set on the drawing load, which the engine never put on a lateen aback |
  | **Aback in stays**, from her head through the wind to "let go and haul" | about 30 kn (0.92 to 0.98 in 28.6; 1.12 to 1.21 in 31.9) | about 36 kn | the same | — |
  | **The bad hand**, close-hauled against the mast | **about 45 kn** (the polacre probe's 0.99 and 1.01 in 45.5 kn; the tartane's, heeled, 0.81) | **about 55 kn** | `LATEEN_BAD_HAND_LOAD` **about 2**, on the two-thirds' pull | about 45 kn by 1.5, which forgot the two-thirds: at 1.5 it strains only from about 53 kn |

  - **The mast.** On the generator's rule a mast that carries only its lateen (the polacre's and
    the xebec's mizens, and the xebec's three in her own file) is rated for the same sail as its
    yard, so the two strain in the same wind and the strain stream's draw decides which goes
    first. A mast that carries more is rated higher (the tartane probe's main, with her topsail,
    122.8 kN against its yard's 59.5; the polacre's fore 139.4 kN against 61.1): taken aback by a
    shift, the tartane probe's main mast
    stood at 0.69 of its rating in 28.6 kn, 0.89 in 34.3 and 1.11 in 40, so it strains from about
    38 kn and may carry away from about 46. There the great yard goes before the mast (Forfait
    p. 120's weak yard); a hull's module that rates its lateen yard below the rule (Forfait p. 120)
    moves the yard's winds, not the mast's. Measured again on each hull's file, and its truth's
    band is hers (Tar-D T-9).
  - **The winds are the target, not the factors**: if a hull's measure gives other winds, the
    factor is set again on the tartane's file (the first) and checked on the polacre's and the
    xebec's, and the lead rules a difference.
- **Against the rules captain's own book** (§2.3 item 6; measured, §2.2b), so that a captain who
  follows it is not dismasted by it:
  - **22 kn.** Over it, `put her about`, the course's judgement and the rules captain wear a lateen
    hull, and a wear never takes a lateen aback (the wind comes round the stern). Under it they
    tack, and in stays a lateen is aback only for the seconds from her head through the wind to "let
    go and haul" (§2.4.3a). Measured in that tack at 22 kn, the great yards stood at 0.55 to 0.60 of
    their ratings; in 28.6 kn, the top gust of a 22-kn wind (1.30 of the mean, the neutral air's
    highest, `GUST_FACTOR_RANGES`, `physics/wind.py:63-67`), at 0.92 to 0.98; in 31.9 kn, a squall's
    top on it (1.45, `SQUALL_FACTOR_RANGE`, l. 72), at 1.12 to 1.21, a few seconds' wear and no
    chance of carrying away. **The margin: from 22 kn to the strain in stays about 8 kn, to the
    risk about 14 kn**; the worst squall on a 22-kn wind (31.9 kn) is 3 kn short of the shift's
    risk wind (35 kn) and 4 kn short of the stays' (36 kn).
  - **Taken aback outside a manoeuvre at 22 kn** (a shift or the helm): the yards at 0.62 to 0.72;
    at its top gust 1.02 to 1.08; at a squall's top 1.22 to 1.29: strained, not at risk, until the
    rules captain shifts it at the bow watch's word (§2.3 item 1), when its change takes it out of
    drawing.
  - **12 kn and 1,800 s.** The rules captain lies on the bad hand only by choice under 12 kn,
    shifting after 1,800 s or as the wind rises over 12. Measured on the bad hand with the factor:
    in 12 kn for 1,800 s the yards at 0.07 to 0.10 of their ratings; in 15.6 kn, the top gust of a
    12-kn wind, the polacre probe's at 0.12 and 0.14; and a tack in 15.6 kn with the yards left, its
    seconds aback in stays included, at 0.26 to 0.30. Under
    its rating a part loses nothing (the strain model wears it only over 1.0), so the board's length
    costs no condition. **The margin: from 12 kn to the bad hand's strain about 33 kn.**
  - **A lateen waiting its turn** on the bad hand after a wear (the trader's yards changed one after
    another, §2.4.4: the tartane's mizen 265 s, the trader xebec's fore 261 s and mizen 496 s):
    measured worn in 28.6 kn, 0.36 to 0.47 of the ratings; in 39 kn (a 30-kn wind's top gust),
    0.59 to 0.83. The bad hand strains from about 45 kn, a 35-kn wind's top gust, and the great
    lateen is taken in before 30 kn (Tar-D T-6; A8's small lateens at the second reef).
- **The sail.** `take in the mainsail`, begun while it is aback over `LATEEN_TACK_KN`, waits: "The
  mainsail is aback against the mast; it will not come in till she pays off." (Forfait p. 119), and
  goes on when it fills or is drawn over (JUDGEMENT on the words).
- **What it moves** (measured, §2.2b): nothing of the eighteen files (no committed sail carries
  `dipping` on a whole lateen; the 64's and the 74's mizen courses are cut at the mast, and every
  other sail's force and load are as they are); `tests/test_strain.py`, `tests/test_lateen.py` and
  `tests/test_settee.py` as they are; **the probes' going about by −9 to +13 m** in 15 and 25 kn,
  with the evolution's part (§2.4.3a), so that A1b's figures (§2.2a) stand within about two per
  cent; the hulls' truths of going about and of the strain (Tar-D T-3, T-9; Xeb-D X4; Pol-D P5)
  measured after it, old beside new.
- **Its size: two and a half days** (two to three; JUDGEMENT): the rule (the side kept ahead and
  carried over abaft the beam, the hold, the two factors in `_apply_loads`), half a day; the sheet's
  side kept when drawn (`set_sheet_angle`) and the draw at "let go and haul", "wind aft", `trim` and
  the watch's shift, at A1b's places (§2.3a rows 4 to 9), half a day; the take-in's wait and the
  words (§2.4.3a), a quarter; its tests in `tests/test_lateen_whole.py` (aback through the eye and by
  a shift; not in the luffing band; over through the stern; drawn at "let go and haul"; the two
  factors' winds on a probe rated by the generator's rule; the bad hand), half a day; the probes'
  going about re-measured with it and the factors set, old beside new, half a day; the reading of a
  new rule of force by a reader of the other tier, a quarter. Nudge 18 guessed one and a half to
  two days; it is larger because the rule must keep the cloth's side and the evolution must draw
  it (measured: the rule as nudge 18 drafted it, the cloth's side left to the deck's lee, took no
  lateen aback in a tack, the polacre's in 15 kn 166 s and 279 m, §2.2b). It is A1d, after A1c and
  before the tartane's merge, merged alone.

#### 2.4.3a What the tack and the wear do to a whole lateen in stays, and what they should do

**Today (read).** The tack and the wear work three lists of fore-and-aft sails, and a whole lateen
is in none of them:
- `head_sails` (`evolutions/scripts.py:207-216`): jib-headed sails forward of the foremost mast;
- `boom_sails` (l. 230-248): gaff sails on a boom, lateens cut at the mast, standing lugs;
- `shifted_sails` (l. 314-331): fore-and-aft sails with a sheet a side. A whole lateen has one
  sheet with no side (the probes' `fore.lateen.sheet`, read).

So at "Helm's a-lee" (`_ready_about`, l. 1445-1491) its sheet is neither eased with the head sheets
nor hauled aft with the booms; at "mainsail haul" (l. 1577) it is not let fly with the shifted
sails; at "let go and haul" (`_draw_on_new_tack`, l. 1608 and 1740-1747) it is not drawn on the new
tack; hung in stays (`_hang`, l. 1749 on) it is neither held to windward with the head sheets nor
eased; in the wear `shift_sheets_over` (l. 334-340, at "wind aft", l. 2036) takes the same three
lists. **The evolution neither spills nor shifts it**: its sheet's reading does both, free and at no
cost, the moment the deck's wind crosses.

**With A1d (what it should do, as a seaman would; A1b's places, §2.3a rows 4 to 9; JUDGEMENT on the
words):**
- **At helm's a-lee**, as A1b has it: the aftermost whole lateen hauled aft with the boom sails, a
  foremost one before a square main eased with the head sheets (§2.3 item 5).
- **As her head comes to the wind**, every lateen lifts and shakes in its luffing band; none is
  held.
- **Her head through the wind**, each lateen lies aback against its mast (the rule): a foremost
  one pays her head off, as the head sails do; an aftermost one holds it up.
- **At "let go and haul"** (the first tick she is through, where she has no head yards), with the
  head sheets: each lateen to be **left** has its sheet drawn over to the new lee, and fills on the
  bad hand against its mast; each to be **changed** begins its change and hangs out of drawing in
  its gear while its car is passed round (A1b's `LateenChange`); one **waiting its turn** is drawn
  over first. The words: "Let go and haul. Draw jib; trim aft the head sheets; draw the mainsail on
  the mast." where it is left, A1b's "Shift the mainsail: ease the parrel, cast off the runners,
  peak up the yard and pass the car round." where it is changed.
- **Hung in stays** (`_hang`): a foremost lateen is left aback with the head sails to pay her head
  off ("Her head is through the wind; the head sails and the fore lateen aback pay her off."); an
  aftermost one is **hauled to windward with the booms** till "let go and haul", as the mizen
  course and the settee are. *Corrected 2026-11-23 (the lead's nudge 55; the lateen hulls' list,
  item 5):* this draft and A1d had it eased. That was A1d's own judgement, that a whole lateen
  cannot be hauled over its mast as a boom is, and no source gave it. Measured over 1,536 probe
  tacks, the 22 that hang in stays (all the polacre's) all missed stays with it eased and all came
  round with it hauled, the yard well under its rating either way. So the ease cost her stays for
  nothing, and it is put back (the engine's report, "The lateen hulls' list (nudge 53)", item 5).
- **In the wear**, at "wind aft", each lateen to be left goes over against its mast with the other
  sheets ("Wind aft. Shifted over the sheets; the mainsail over against the mast."), each to be
  changed begins its change; a wear never holds one aback.
- **Outside a manoeuvre**, a shift of wind or the helm that brings the wind round ahead leaves it
  aback until it is drawn over or shifted: the bow watch's line (§2.3 item 1) says "The wind has
  come round ahead to the larboard bow: the mainsail is aback against the mast; shift it when you
  will.", and the rules captain shifts it (A1c). Through the stern it goes over against its mast,
  and the stern watch's line is A1a's ("the mainsail lies on the mast").

**Measured** (§2.2b): so worked, a lateen is aback in an ordinary tack only from her head through
the wind to "let go and haul", under the 10-s dwell of `_record_backed`, so no "taken aback" line
is said; it shows in the yard's peak (the polacre probe's fore yard in 25 kn at 0.29 of its rating
against 0.23 without the rule). Left undrawn, it holds her aback on the new board: the polacre
probe round in 127 s but sailing on at 3.1 kn with both lateens aback, 588 m lost against 277; the
tartane's great lateen aback holds her head up and in 25 kn she falls back on the old tack.

#### 2.4.4 The hands and the time to change a yard of her length, in stays and in the wear

- **The sources:**
  - the xebec's labour is that of three square-rigged ships (Falconer, XEBEC);
  - the change of a ship's whole mizen was "eine beschwerliche Arbeit" (Röding I col. 494);
  - the column shrouds are cast off for it (Lescallier p. 378), and the yards worked round by the
    parrels (Fincham p. 60);
  - it is not for one man (the 2018 inventory, B);
  - no count of hands and no seconds (GA §5.4).
- **JUDGEMENT, ruled by the lead on 2026-11-18 (nudge 18).**
  - **Time: the lugger's own rate, 8.7 seconds a metre of yard** (her 90 s in a manoeuvre,
    `dip_s`, `evolutions/scripts.py:1534` and 2044, for her 10.3-m main lug yard, read in
    `data/ships/lugger.yaml`), by the crew's factor. The third draft took the settee's 120 s for
    a yard of 16 m, 7½ seconds a metre; the lead's reason for the lugger's: peaking a thirty-metre
    yard round is no lighter work than dipping a lug.
    - The same in stays and in the wear (the lean, standing). §2.2a shows the same seconds cost two
      to four times the ground in stays, which is the period's reason to leave the yard there
      (Stratico), without a second figure.
    - At that rate on the hulls' own yards, with the hands they want: **the tartane's 24.4-m main
      212 s and 15.3-m mizen 133 s; the xebec's 30.0-m main 261 s, 27.0-m fore 235 s and 13.5-m
      mizen 117 s; the polacre's fore of about 19 m 165 s and mizen of about 9½ m 83 s** (the
      third draft's 183, 115, 225, 202, 101, 140 and 70 s).
    - **By itself** (`change_lateen`, standing on her course), the sail drawing nothing while it is
      shifted: **not ruled.** The third draft took the settee's dip by itself, 180 s for 16 m
      (`dip_settee.yaml`), 11¼ seconds a metre. On the ruling's own reason the lugger's by itself
      is `dip_lug.yaml`'s 150 s (30, 60 and 60) for her 10.3-m yard, **14.6 seconds a metre**: the
      tartane's main 356 s with its ten hands, against 275 s at 11¼. My lean is now the lugger's,
      so that both of the change's figures are hers; the lead's word asked (the plan's §13.1).
  - **Hands: one able hand for each 2½ metres of yard, at least four** (ruled; the settee's six
    for 16 m), from the hands the tack or the wear has called; `too_few: all hands`.
    - The tartane's main ten, her mizen six. She can put at most eight to her main: her six
      seamen, the boy and the cook. Her master and mate are at the conn, since by ruling 11 a post
      is never taken for all-hands work (`crew/hands.py`). So her main's change goes by the
      party's numbers term (`crew/hands.py:504`, wanted over got, never faster for more), **10/8
      of 212 s, about 265 s**, and her mizen's 133 s after it: **398 s for both** (the third
      draft's 230 s for the main).
    - The xebec's main twelve, fore eleven, mizen five.
    - The polacre's fore eight, mizen four.

    With hands for all, her yards are changed together, the change done when the longest is (the
    xebec's 28 of her 75 seamen, 261 s after it began; the polacre's twelve of the trader's fourteen
    hands, 165 s; the coastguard tartane's, 212 s). With too few, **one after another, the main
    first** (the trader xebec's eighteen: 261, then 235, then 117 s, 613 s in all; the tartane's
    eight: 398 s). A lateen waiting its turn draws where it lies, on the bad hand after a tack.
    Measured on the probes at these seconds: §2.2a.

#### 2.4.5 The polacre's square main with her lateens

- **The sources:** the main "ever keeps the rigging of the polacre" (Steel I p. 236); nothing on
  how her lateens are worked going about (GA §5.6).
- **The game:**
  - she tacks and wears as a brig of her size with her main, `TackScript` as it is: "mainsail
    haul" for her main yards, then "let go and haul";
  - her fore lateen is eased with the head sheets at helm's a-lee and drawn at "let go and haul";
    her mizen is hauled aft at helm's a-lee (§2.3 item 5);
  - both are changed after "let go and haul" by her practice, or left, by two parties together
    (the forecastlemen at the fore, the afterguard at the mizen); in the wear, at "wind aft".
- **Measured** (§2.2a):
  - her tack: 164 s and 249 m today; 180 to 181 s and 291 to 296 m with both changed at the
    lugger's and the settee's seconds (90 and 120 s); **238 s and 318 m at her own seconds by the
    ruled rate** (the fore 165 s and the mizen 83 s together, done 215 s after the order; the
    third draft's 140 s gave 306 m); 165 s and 275 m with both left, and 4 per cent off on the
    bad hand;
  - her wear: 464 s and 602 m today; 599 and 617 m changed at 90 and 120 s, **679 m at her own
    seconds** (the third draft's 649).
  - Leaving them pays on a board shorter than about **34 minutes** (§2.2a; 25 at the settee's
    seconds).
- **With A1d** (§2.2b, nudge 19): her tack in 15 kn 164 s and 277 m with both left, 238 s and
  316 m with both changed (A1a alone 166 s and 278 m, 239 s and 317 m in the same harness); her
  fore lateen aback from her head through the wind to "let go and haul" pays her head off.
- **Her probe stops dead in stays** (0.12 kn at 92 s) and is refused in 6 kn. Her helm and her
  lever are her file's to measure (Pol-D §5).

---

## 3. A square topsail over a lateen on one mast (the tartane), and B3.4's classing

**Today (measured, on the lead's probe, whose topsail yard stands on the cutter's topmast,
`on: main.topmast`):** the tartane probe classes exactly as the lead read her under B3.4's rule and
as `tests/test_schooner_mast.py:259` holds: masts with yards `[main.mast]`; head yards
`[topsail.yard]`; no after yards; the topsail the yard laid aback hove to; not square-rigged; no
driver; `on_schooner_mast` true of no part (her main is the foremost mast with a braced yard, the
lateen yard being no braced yard). She tacks in 89 s, swinging her topsail at "Let go and haul" at
23 s as a cutter swings hers; she heaves to with the topsail aback ("Hove to on the starboard tack,
topsail to the mast, helm a-lee") and forereaches at 3.1 kn, her two lateens drawing (§2.2).
**Her own design's main is a pole** (`Design-Ship-Tartane.md` §4.1: the topsail yard hoisted on the
lower mast's head, no topmast). With the probe's topsail yard so filed, the engine counts the
topsail a course (`scripts.lowest_square_sails`, `evolutions/scripts.py:860-868`): hove to she
hauls it up ("Hauled up the courses.") and lies "under her fore-and-aft canvas", 51.8° off at
3.29 kn at +600 s (the critic's run, re-run for her second draft: Tar-D §5.1a). Her classing is the
same either way; her handling is not, so A5 and A6 (§14) come before her file.

**B3.4's two limits** (the lead's note of 2026-11-06; the list of 79, item 8): a lower square-sail
yard on an after mast, and a pole main with its topsail yard on the lower mast, each still a brig
by the rule. Neither reaches the tartane: whether her topsail yard stands on a topmast or on the
lower mast's head, the main is her foremost mast with yards, and the rule reads only after masts.
Measured on the polacre (§4): with her main topsail yard's parent moved onto the lower mast, her
classing is the same, field for field.

**What the build wants:** nothing new for the classing. For her own document: the topsail's
handling on her short main (set flying or on a yard hoisted on the mast's head, Monleón's print
and the Roux-school watercolour, `VesselReferences-2026-11-Spanish.md` §1); her heave-to (§2.3, 5);
and her *tréou*, the square sail Lescallier says tartanes rig to run or in a wind too strong
(pp. 400-401, `VesselReferences-2026-10.md` §3.1): a sail of the sail room bent in the lateen's
place, the settee's and the driver's road (`in_place_of`), if her document takes it.

**Her boat in tow** (the brief: "the boat in tow"). Today a ship's boats are a list with no place:
a boat's entry takes `id`, `kind`, `name`, `length_ft`, `oars`, `crew`, `tons` and `file`
(`schema.BOAT_KEYS`), and one offered `towed: true` is refused at load ("boat #1 has 'towed',
which a boat does not take"; measured on the tartane probe). The only thing towed astern with a
drag is the trawl (`physics/integrate.py:126-130`, `gear_drag`); "the boats are out and towing
astern" at the clearing for action is words alone (`action_scripts.py:134`). For her document: the
boat's place (on deck or towed) as a key of the boat, read by the boat's orders (manned from
alongside, not hoisted out) and by the words; a towed boat's drag left out as small beside her
hull's at her speeds (JUDGEMENT, to be measured against the trawl's form if it is not).

---

## 4. The pole mast (the polacre): cross-reference

Item 8 of the list of 79 (the polacre's pole masts; her lateen mizen kept hove to as a
fore-and-after's and whether the heave-to's driver rule reaches it; a whole lateen hauled aft at
helm's a-lee by nothing; the schooner's-mast rule's limits for whichever file has a pole main
first) is the lead's for **the polacre's design document** (`Design-Ship-Polacre.md` §5, with
her research note, `Research-Polacre-2026-11.md`), which settles it with what the engine does run
and not guessed.
What this note measured, for that document to cite or measure again:

- **There is no pole mast in the engine** (read: no key, no class; `schema.py`, `graph.py`).
  Every square sail's furl is aloft by topmen (`data/evolutions/furl_square.yaml`, "Lay aloft and
  furl the {sail}", its step `aloft: true`); `strike_topmasts`, `send_down_topgallant_masts` and
  their kin assume a topmast to strike; the viewer draws a topmast's doubling and its cap.
- **A pole main, as the classing reads it** (the polacre probe with her main topsail yard's parent
  moved from the topmast to the lower mast, at its own height; her topmast and the mast's height
  left as they were, the classing reading only the yards' parents) loads, and classes field for
  field as the probe does: masts with yards `[main.mast]`, head yards `[main.yard,
  main.topsail.yard]`, no after yards, not square-rigged, no driver, nothing on a schooner's mast
  (measured). Her square main is her foremost mast with yards between two lateens, so B3.4's rule
  never reads it. A whole pole (one spar, no topmast, its stays and staysails re-led) was not
  built here; it is her document's to make and sail.
- **Her lateen mizen hove to** is kept drawing as a fore-and-after's mizen: `after_gaff_sails` is
  empty for her, so the driver rule does not reach it; she lies 58.6° off at 1.65 kn at 900 s, the
  main topsail to the mast (measured, §2.2): her speed by truth 12's measure, 0.05 kn over its
  1.6 kn. The polacre's second draft agrees (her headway is 1.49 kn: `Design-Ship-Polacre.md`
  §5.2).
- **At helm's a-lee nothing hauls a whole lateen aft** (the tack's lines for her, §2.2: "Ready
  about. Helm's a-lee; ease off the head sheets.", and no line of the lateens).

**What a pole mast would want of the engine** (judgement): the pole known to the square sails'
take-in and furl (the yard lowered to hand the sail), to the topmast evolutions (refused in words:
there is no topmast to strike), to the viewer (no top, no cap, no doubling), and, if the sources
give it, to the strain (Winfield's "a mast less able to stand a strong wind", pp. 1083-1084). My
first reading was a key on the mast with the sails handed from the deck. The polacre's design,
drafted beside this note (`Design-Ship-Polacre.md` §5.1), reads it better: **no key**, the pole
read from the parts as filed (a lower mast with braced yards above its lowest and no topmast), for
B3.4's own reason ("a file that forgets a key makes her a brig with no word said"), and the
furlers **on the yard below**, not on deck (Falconer; Steel p. 236). I take her reading; the lead
rules it in her document.

---

## 5. Sweeps

**Today (measured).** The oars are the boats' (package 82, item 4): an `oars:` section of a ship's
file (`schema.py:1638-1655`: a number, a pull on the blade at no way, a power and the hours that
halve a man's strength) read by `physics/oars.py` as a thrust along the axis,
`min(F_0, P / max(u, 0.3)) × manned × stroke × fatigue` (124-130), and worked by the boat's
orders (`orders/boat.py`: `give way`, `easy all`, `lie on your oars`, `out oars`, `boat your
oars`). The schema does not keep it to boats. The xebec probe given a boat's figures for twenty
oars (50 N, 60 W, four hours, one man an oar: scratch figures):

| Wind, sail | Way at 60 s / 300 s / 900 s / 1800 s |
|---|---|
| Calm, no sail | 0.27 / 1.10 / 1.60 / 1.58 kn |
| Calm, lateens set | 0.28 / 1.11 / 1.60 / 1.58 kn |
| 3 kn, lateens set | 0.52 / 1.23 / 1.57 / 1.54 kn |

- `give way` ships every oar and mans it at once ("Give way together: the full stroke."):
  `manned = number`, from nobody: her company of 121 is untouched, no hand is drawn from the watch
  or the bill, and no evolution or time stands between the order and the stroke.
- The men tire as a boat's crew do: half an hour's pulling is half an hour at the oars.
- A lateen drawing does not stop the stroke: only a set lug does (`_lug_drawing`, `boat.py:265`).
- A ship without `oars:` is told "this hull has no oars" and sent to her boat.
- **A file with `oars:` is a boat to the game**: `world.boats.is_boat` and
  `world.movement.is_boat_hull` are both "her file has oars" (`boats.py:97-100`,
  `movement.py:911-914`), true of the xebec given them and false of her without (measured); with
  them she struck no bell in an hour, where without she struck one bell and two (measured), and
  the readers that ask it read her as a ship's boat manned as a hull: the viewer's server would
  say "a boat under oars, with no rig to draw" (`ui/server.py:213`), the readings name a boat of
  her ship's (`api/readings.py:2727`), and the command, the knowledge and the movement readers
  treat her as a boat (read). The xebec's research note found the same with figures of its own
  (`Research-Xebec-2026-11.md` §9, item 8: no bell, the boat's tick and its swamping run on her).

**What the build wants** (judgement): **a ship's sweeps kept apart from a boat's oars**, so that
the boat predicates stay "a ship's boat" and a xebec with sweeps is still a ship (a key of their
own, or the boat predicates read from the file's rig, `rig: boat`, as the harbour's `_is_boat`
already reads it, `ui/harbour.py:198-206`); sweeps **as a fit** of the xebec (the brief: her
sweeps a fit), so a file says whether she carries them and how many; **an evolution** to get them out and
in, its men drawn from the company (all hands, or a watch, by the fit), several men to a sweep (the
figure from the sources: Winfield's picture of oarsmen "crowded between the gunports on the gun
deck", `VesselReferences-2026-11-Spanish.md` §3; the men to a sweep and the sweeps' number are the
xebec's research, and a passage of Winfield's to ask for, §12); **the guns against the oars**: the
sweeps worked from the gun deck by the men who would fight the guns, so the quarter bill and the
oars share the deck and the men, which the boat's model knows nothing of; **the thrust**: the boat's
form serves (a pull and a power a sweep, its men's sum), its figures fitted to what the sources say
a xebec makes under sweeps; and **the words** of the ship's own orders ("out sweeps", "in sweeps",
the stroke's), the boat's kept for the boat.

---

## 6. Three gun decks

### 6.1 The probe (measured)

The three-decker probe (§0): six decks with guns in her profile (`lower`, `middle`, `upper`,
`quarterdeck`, `forecastle`, `roundhouse`), 28 guns on each of the three gun decks: 102, 110 and
106 guns in the 74's three fits so raised, 110 in her default (the 74's 1795 fit).

- **It loads.** `schema.DECK_WORDS` already holds `middle` (`schema.py:339`).
- **Her guns are named by deck**, the 74's `numbering: by deck` carried: "No. 1 starboard gun of the
  middle deck".
- **The beat to quarters says each deck**: "The lower deck: 14 gun crews, 182 men." "The middle
  deck: 14 gun crews, 126 men." "The upper deck: 14 gun crews, 126 men.", then the quarterdeck's
  seven, the forecastle's three and the poop's three; 504 of 839 at the guns (`_deck_lines`,
  `crew/quarters.py:497`, wants a lower and an upper deck and takes a middle between them).
- **The guns' orders by deck are understood**: "fire No. 3 gun of the middle deck" ("No. 3
  starboard gun of the middle deck and No. 3 larboard gun of the middle deck to fire as soon as cast
  loose and ready"); "fire the middle deck" with no side engaged asks which side, as on a 74.
- **The lee ports shut deck by deck** in their order, each in the log's words: "The lee lower-deck
  ports are shut", "The lee middle-deck ports ...", "The lee upper-deck ports ..."
  (`combat/ports.py:79`, `_DECKS_SAID_SO`), heeled by hand, at 10.5°, 32.5° and 66.5° on the
  probe's scratch sills.
- **The viewer's check** (`tools/check_viewer_guns.py`) is clean on her file, every port gun on its
  triple, the over-the-rail notes the 74's.

### 6.2 What the code assumes of two decks (read: `lower`, `upper`, `middle` grepped)

| Place | What it assumes | For a three-decker |
|---|---|---|
| `crew/quarters.py:418-435`, `_shut_crews` | only the lower deck's crews can be robbed for their shut ports | a middle deck's crews behind shut ports are not counted |
| `crew/quarters.py:668-687`, `_rob_order` | the lower deck's shut crews first, "the other decks" next, the lower deck's last | her middle deck ranks with her upper works; the order by deck to be her document's (judgement) |
| `crew/quarters.py:559-563`, `_keeps_its_deck` | the crews keep their deck where a broadside gun stands on `lower`, or the guns are numbered by deck | holds for her |
| `orders/gunnery.py:222-225` | "the main deck" is the upper (Cumby's word for a 74) | which deck the word names on a three-decker is her document's, from the period's usage; the Spanish *baterías*' words are hers too |
| `client/projection.js:3956` | "upper-deck port", and any other deck its bare word | "a lower port", "a middle port" (the 74's "a lower port" is said today); the log's "-deck" form would serve |
| `evolutions/action_scripts.py:49-57`, `clear_seconds` | the time to clear by length, capped at the frigate's quarter of an hour | a first rate clears as the 74 and the frigate do: cleared at 1,086 s and beat to quarters at 1,195 s, the 74 as filed to the second (measured) |
| `world/ships.py:380` | "a ship of the line" names the 74's file | a three-decker wants her own words beside it |
| `world/captains.py:296-359`, `SIZE_RANK`, `size_rank_of` | ranks to 4, the ship of the line | "a three-decker" and "a first rate" rank nothing (measured: `None`); "a xebec", "a polacre", "a tartane", "a corvette" nothing either |
| `tools/ships/bellerophon.py:2499` (`GUN_DECKS`), 2506 | the 74's module's own list of decks; the exercise allowance "a third in a ship of two decks" | `gen_ships.exercise_allowance(n, decks=3)` already takes three (the Regulations' "two or three decks", 4425-4436); a new module lists its own decks |

### 6.3 What the build wants

Each of §6.2's places read again for a third deck (none needs more than its list widened or its
words; judgement); her words and rank in the two tables (the rank of a first rate against a 74's
4 is the owner's, §12); her quarter bill by deck from the Spanish sources (the probe's is the 74's
bill on 839 men and says nothing of hers); the clearing time of a first rate, if her sources give
one longer than a 74's; and **the obús** (the 1803 and 1817 fits' howitzers): today "a gun is one
of long, carronade, swivel" (`schema.py:271`; measured: refused at load), while a 48-pounder
carronade is accepted. Whether the obús is a new kind or carried as a carronade by JUDGEMENT is her
document's (and the *Diana*'s, whose 1817 fit has four 3-pounder obuses), and the magazine's, the
far fight's and the viewer's tables are to be measured for a 48-pounder before her file.

**The pound of a Spanish gun.** The engine reads a gun's `pounder` as the weight of its shot in
English pounds: the broadside by package 70's rule sums it (`combat/action.py:469, 487`), the ball's
diameter is the 18-pounder's 5.04 inches scaled by it (`combat/hits.py:106-109`), the magazine keys
its cartridges and shot on it (read). Winfield gives the Spanish broadsides in *libras* with their
pounds beside (1,212 libras as 1,308 lb, 1,188 as 1,282, 1,508 as 1,627:
`VesselReferences-2026-11-Spanish.md` §4), the same ratio in all three. The lead's note says to
take the book's pairs as it gives them and not to re-derive the ratio. **The owner's** (the
decisions sheet's question 9); the plan's pick (its §4 row 8) is the gun filed as her navy named it
(`pounder: 36`), the book's pairs in the note as it gives them, the broadside then reading a little
light in English pounds and the notes saying so; the other way is the English weight in `pounder`,
from Winfield's volume by calibre if it gives them (a passage to ask for, §12), with the words
taken from a separate key. Either way the gun's calibre in libras is in its words and its note. The
generator's weight tables (`gen_ships.py:4295-4296`, `period.py`) are English patterns, and the
Spanish guns' weights come from the Spanish sources.

---

## 7. A first rate's company and the pace

**The measures** (measured on this machine, quiet: the two suites of §1.4 finished, the processor
at 1 to 5 per cent before each; seed 7; a thousand ticks to settle, then the best of three timed
thousands, truth 51's form):

| World | The 74 as filed (590) | The three-decker probe (839) |
|---|---|---|
| Her file alone on the gate's day (`tools/pace.py`'s `seventy_four_alone`, truth 51's form) | 514 ticks a second | 487 |
| Truth 7-196's own world (its body run in scratch: the frigate hove to off the Lizard, three of the file in her squadron one to three miles off; `CREWED_CAP` 3) | 79 and 81 (two runs; the thousands 55 to 81) | 72 and 75 (the thousands 47 to 75) |

In truth 7-196's world every run kept the cap at three, the three in company within 2.8 miles at
each thousand's end (S2 at 2.79, as the truth's docstring has it), every company whole and no line
of an action in any log; the truth itself passes on this tree (78.7 s). Its floor,
`CREWED_FLOOR_TICKS_S`, is 60 (`world/crews.py:99`); truth 51's, `BUILD_MACHINE_FLOOR`, 500, the
74's own clause recorded and not pinned (the docstring of truth 7-196).

**What it says** (judgement on the figures): three crewed first rates of 839 cost about a tenth
more a tick than three 74s of 590 (72 to 75 against 79 to 81), for 42 per cent more men: a crewed
ship's tick is not in proportion to her company (what is most of it, her hull, her rig or her
captain's brain, was not profiled here). Alone, the first rate runs a twentieth slower than the 74 (487 against 514), as the 74
runs a twentieth slower than the frigate (the docstring). So **839 wants nothing of its own of the
engine for its pace**: the crewed cap of three and the floor of 60 serve her as they serve the 74,
on this machine with a margin of a fifth; on the build machine the figure is the cloud's pace job
to give, not this note.

**Two things found, for the lead:**
1. Truth 7-196's world gives 79 to 81 here against the 150, 151 and 147 its docstring records on
   the owner's machine on 13 November, the same world to the mile. Whether the machine or the
   tree since then makes the difference is not measured here.
2. `tools/pace.py seventy-four`'s crewed measure is not truth 7-196's world: it puts the three 74s
   beside the frigate with no squadron, and they fight her ("A frigate has struck her colours!" at
   tick 2,280 of 4,000; her company 264 to 44, a 74's 590 to 546 over the measure), so its figures
   (167 with three 74s, 86 with three of the probe) time an action. The truth's docstring says why
   its own world was changed; the tool's was not.

---

## 8. The regency's cruiser as a role (package 116's road)

**Today (read, and the doctrines loaded):** a role is a book of `data/captains/` (`role:`, `name:`,
`source:`, `thresholds:`, its transitions and books), read by `load_doctrine`
(`world/captains.py:1017`), each threshold `{value, source}`, and named in the code's `ROLES`
(`world/captains.py:137-150`, ten roles). Loaded: the cruiser's book has 65 thresholds, the
revenue cutter's 66 and the privateer's 70 (`board_odds` 1.3, 1.3 and 1.0; `engage_nm` 1.0, 1.0
and 1.5; `man_of_war_nm` none, 6 and 2.5); a role of no book is refused in words ("There is no
doctrine for the role 'corsair'; the roles: kings-ship, merchant, ..."). Package 116 moved the prize
doctrine's thirteen keys under `thresholds:` in `cruiser.yaml` and the revenue cutter's
`revenue.yaml` (whose book is the cruiser's), seven of them read by the code and six not
(`mans_prizes`, `divide_prisoners`, `prisoners_most`, `burns_when`, `worth_least`, `fit_least`;
its record). The revenue book is the form for a role that is another's book with its differences
stated at its head (four, each judgement).

**What the build wants:** a role's name in `ROLES` and its book (code and data, the revenue
cutter's step of SW-4 the precedent); the Barbary regency's cruiser as a book on that form, the corsair's
differences from the privateer's and the cruiser's said at its head, each with its source: whom she
chases (a Christian merchantman of a nation at war with her regency, or without a passport), her
boarding (the xebec's company boards: `board_odds`, `board_when`), her prize doctrine (the thirteen
keys, the prisoners the cargo: the six unread keys matter to her more than to any King's ship, and
what acts on them is not built), her `engage_nm` and `man_of_war_nm`; and the Spanish navy's
xebec on the King's ship's or the cruiser's book with the coastguard's station. The regency as a
nation for the world's business (its flag, its ports, its relations with each power by the year)
is the nations' table's and not the engine's; the lead's to place (§12).

---

## 9. The harbour's shelves (package 96)

**Today (observed):** the harbour offers every ship file of `data/ships/` but the boats for a bare
start, her fits read from her file, her kinds and roles from `world/ships.py`'s `DESCRIPTIONS`
(seventeen rows); a scenario is offered from `client/harbour-shelves.yaml` with one sentence, and
one that no shelf names stands on "Not yet sorted" (`Harbour._shelve`: a scenario named
`xebec-off-algiers` went to `unsorted`, `mahon` to `passages`). `tests/test_harbour.py:131`
asserts that no scenario of the game is unsorted.

**What the build wants:** a shelf line for each new scenario, a sentence each, in the shelf it
belongs to (the Mediterranean passages' or the trade's); a `DESCRIPTIONS` row for each new kind
(her rig's word, her roles), which the harbour reads for her kinds and roles. The ship's whole
configuration as one thing (`Design-Harbour.md`) is designed and not built, and nothing of this
package waits on it.

---

## 10. The wheel shot away, and the relieving tackles (package 116)

**Today (observed, on the cutter as filed and the tartane probe):** the hit sets `helm_lost` to "the
wheel shot away" for every hull (`combat/hits.py:216-229`); the helm orders and the manoeuvres are
refused in the ship's words ("The wheel is shot away and the helm does not answer: rig the
relieving tackles ... or repair the wheel ..."); `rig the relieving tackles` waits for hands while
the watch is at other work ("Not hands enough on deck to rig the relieving tackles"), begins 151 s
(the cutter) and 47 s (the tartane) after the order and is done at 515 s and 412 s: "The relieving
tackles are rove to the tiller and manned below: the helm answers again, steered by the tackles,
and more slowly than by the wheel."; `repair the wheel` takes the carpenter's crew of four, "new
wheel-ropes to be rove", done in 2,387 and 2,410 s. **On a tiller-steered hull every one
of those words is a wheel's**: the cutter's own file says "One man at the tiller (a cutter steers
with a tiller; judgement)" (`data/ships/cutter.yaml` l. 869), and she is told her wheel is shot
away and repaired with new wheel-ropes.

**What the build wants:** the hull's helm read from her file (a wheel, or a tiller worked from the
deck by hand or by tiller ropes, by her sources: the small lateen craft by tiller, the
three-decker and likely the *Diana* by a wheel), and the tiller's words: the tiller (or its ropes)
shot away, the relieving tackles hooked to the tiller as now, and the repair a spare tiller shipped
or new tiller ropes rove, its time and hands the hull's. It is every tiller-steered hull's
(the cutter, the lugger, the smack, the schooners), and moves their words where a helm is shot
away (truth 7-626 is the one recorded passage with a wheel shot away); the owner's whether it is
built for all of them at once (§12).

---

## 11. Package 81's viewer checklist for a lateen hull and a three-decker

The checklist (`Build-Ships.md` §6, its postscript): `hull.profile` with `rail_m`, `breadth_m` and
`decks_m`; `ports_m.<deck>` a triple at every broadside gun's and chaser's `x_m`; `port_size_m` a
deck; every gun's kind, pounder, place, side, `x_m`, `weight_cwt` and deck; then
`tools/check_viewer_guns.py` clean, and the test.

- **A lateen hull** (the xebec probe, the brig's hull and guns under three lateens): clean, "18 guns:
  18 port; empty ports a side: upper 1" (measured). Nothing in the checklist reads the rig. For the
  xebec's own file: the sweep ports between the gun ports are no gun's and are not in `ports_m`
  (the viewer draws ports where guns stand); if her document draws them, that is a viewer change
  beyond the checklist (judgement). **Her lateens are not drawn as lateens yet** (read): with no
  `corners_m` a lateen is drawn as a four-sided sail hanging under its yard, "from its yard's ends,
  its area over the yard" (`projection.js:1536-1541`), the yard at a fixed tilt of 0.8 rad (904);
  with `corners_m`, by the lug's cut as a standing lug on its lee side (1506-1509), the code's own
  comment saying "until the package that builds a whole lateen draws it as its own" (815-816). A
  whole lateen's triangle, its side read from the sail as a dipping lug's is, and the yard's own
  peak are viewer work of this package's (Ext §3.7), beyond package 81's checklist.
- **A three-decker** (the probe): clean, every port gun on its triple, the notes the 74's
  over-the-rail ones (measured). The viewer reads `ports_m` and `decks_m` by their keys
  (`projection.js:2499, 3037`), so three tiers are drawn as two are; its words for a port are the
  one place it names a deck (§6.2). Her stern's three tiers of lights and galleries are her
  profile's (`galleries_m`, a tier each: `projection.js:3357-3389`) and the viewer takes any number.

---

## 12. For the owner, and passages to ask for

**Decisions** (my pick first; the decisions sheet, `Decisions-Package90-2026-11.md`, puts them to
the owner as its questions 2 (item 37), 3 (going about), 6 (the sweeps) and 8 (the rank), and takes
5 and 6 as recommended in its Part E):

1. **Item 37.** (a) The generator reads the engine's curves, rounded to two places, with a test
   holding them together; truth 35's last clause and the frigate's six-points test re-measured old
   beside new, and the five records of no figure moved naming the booms; or (b) 1.25 kept as a
   stated JUDGEMENT; or (c) the studding curve lowered. Before any new file is generated.
2. **Going about on a lateen rig: answered by the owner, 2026-11-18** (the decisions sheet's
   question 3 and Part F). They re-opened the second draft's pick ("`tack ship` answered in her
   words and nothing done, naming the wear"; or "taken as a wear") and gave their own shape: a
   vessel with a lateen main tacks and wears as others do, each an ordered evolution, and the
   change of the yard round the mast is preferred and not necessary. It is designed in §2.3 and
   §2.4 and built as A1a to A1c (§14), the lead having ruled its figures (nudge 18). No rig of the
   package is kept from the tack.
   - **A1d, the strain of a lateen held aback and on the bad hand: decided by the owner on
     2026-11-18, built** (the lead's note of 22:35 UTC, nudge 19; their words verbatim in §2.4.3).
     Put to them as (a) not built or (b) built, with (a) my pick, they chose (b), in their own
     words. Designed in §2.4.3 and §2.4.3a and measured in §2.2b; its figures (aback from about
     28 kn and at risk from about 35, the bad hand from about 45 and 55, the factors about 2½ and 2)
     are the lead's to rule.

(Questions 2, 6 and 8 of the decisions sheet, which carry items 1, 3 and 4 here, were agreed by
the owner on 2026-11-18 as picked; items 5 and 6 stood in its Part E and are taken as
recommended, no word having been given against them.)
3. **The sweeps' men.** (a) Drawn from her company by an evolution, so many to a sweep by the
   sources, and not at the guns while they pull; or (b) the boat's model as it is.
4. **A first rate's rank** in the captains' judgement: (a) a rank of her own above the 74s', or (b)
   the ship of the line's 4.
5. **The tiller's words** for every tiller-steered hull at once, or for the new hulls alone.
6. **The obús**: a gun kind of its own, or a carronade by judgement.

**Passages of Winfield's Spanish volume to ask for** (the owner sources them; by title and class):
- *Jabeques* (the xebecs), the 30- and 32-gun classes and the 14- to 22-gun classes by name: the
  number of sweeps (*remos*) and the men to each, and anything on going about under the lateens.
- The *Purísima Concepción* class (pp. 406-410 held): her masting and sails if given (whether she
  crossed studding sails), her steering, and the division of the 839 (seamen, gunners, marines).
- Wherever the volume gives it (its introduction to the artillery, or the Artillery Regulation of
  1752's table, pp. 1134-1136 held): the weight of shot of each Spanish calibre in English pounds,
  for the guns' `pounder` (§6.3), and the weights of the guns and of the obuses.
- The *Diana* (p. 930 held): her rig and masting, and her steering, if the entry gives them.
- *Tartanas* (pp. 1249-1252 held): the companies of the navy's seven, for the coastguard role.
- *Polacras* (pp. 1083-1084 held): the eight in the records, any that gives her masts' and yards'
  handling.

---

## 13. Found on the way

1. Every wear begins "Up helm; brace in the after yards." whether she has after yards or not (the
   lugger as filed; `scripts.py:1987-1994`); words only, older than package 90 (§2.2, 4).
2. Every tiller-steered hull is told of a wheel and its wheel-ropes when her helm is shot away
   (§10).
3. The viewer says "a lower port" of the 74's and the 64's lower-deck ports where the log says
   "the lee lower-deck ports" (`projection.js:3956`; §6.2).
4. The sprit class has no `PEAK_COEFF` entry, so a sprit sail on a rated spar raises at generation
   (`map-engine.md` §4, read); the mend of §1.5 gives it the engine's 1.20.
5. The generator's helpers are English feet (`gen_ships.FT`, `ft()`, the proportions' rules from
   Steel and Fincham in feet). A Spanish hull's module takes Winfield's metres for its constants and
   states its own pie de Burgos (0.2786 m) for the plans' figures, as the 74's module keeps its own
   constants (`VesselReferences-2026-11-Spanish.md`, "Units"); the ship file itself is in metres.
6. Truth 7-196's world runs at 79 to 81 ticks a second on this machine against the 150 its
   docstring records for 13 November; and `tools/pace.py seventy-four` times a fight, not that
   world (§7).
7. A ship file with `oars:` is taken for a ship's boat by every boat predicate (§5).
8. **Third draft.** A rig with no head sail and her centre of effort aft (the xebec's own probe)
   is called "Tacked" by the steady timeout while she lies 36° to 47° off the wind at about a knot,
   in every wind from 6 to 28 kn (§2.2a): the tack ends without her having paid off. A1b's mizen
   eased as she pays off answers it for a lateen rig; whether the tack's end should wait for her to
   pay off, for any rig, is the lead's. *Ruled 2026-11-18 (nudge 18): keyed on a whole lateen only,
   so that no other rig's pin moves (§2.3 item 5).*
9. **Third draft, corrected on nudge 18.** A lateen is never aback in the engine: with the wind on
   its wrong face it collapses and flogs (`physics/sails.py:1136-1141`), and her head in the wind's
   eye costs her way and nothing else. The third draft's "aback" loads were the drawing peaks as
   she fell off and filled (§2.2a). Forfait's danger wants a new rule of force: A1d, the owner's
   option (§2.4.3). *Nudge 19: decided by the owner, built (§2.4.3).*
10. **Nudge 18.** The stern watch hears the wind across the stern and not round ahead through the
    bow (`orders/navigation.py:791-812`): a shift that takes her onto the other tack outside a
    manoeuvre leaves a dipping lug (and, with A1a, a whole lateen) on its mast with no word, and
    the rules captain does not dip it. Mended at its cause in A1a (§2.3 item 1).
11. **Nudge 18.** The sail room's "for a new one", "for another", "for a spare" and "for a new
    spare" leave no mark on the order (`orders/grammar.py:396-430`, `_take_canvas_words`): `shift
    the mainsail` and `shift the mainsail for a new one` are one order today. A1a gives "for" a
    mark, for the whole lateen's routing (§2.3 item 3a); nothing else reads it.
12. **Nudge 18.** The bare xebec probe worn with her three yards changed at the King's seconds
    (261 s for the longest) came to stalled 41° off at 1.1 kn and lost 1,311 m (§2.2a): with no
    head sail and every yard out of drawing a long while, she luffed into the wind as they were
    set again, as her tack does. Her mizen eased as she comes to in the wear, the counterpart of
    §2.3 item 5's for the tack, is the xebec's file's to measure (Xeb-D §5).
13. **Nudge 19.** The tack and the wear do nothing to a whole lateen's sheet: it is no head sail,
    boom sail or shifted sail (`evolutions/scripts.py:207-331`), so at helm's a-lee, "mainsail
    haul", "let go and haul", a hang and "wind aft" its sheet is left alone, and its reading
    (`evolutions/trim.py:473-478`) carries the cloth over at the deck's crossing at no cost. With
    A1d the evolution draws it over or begins its change (§2.4.3a).
14. **Nudge 19.** The tack calls a miss only before she is through the wind (`TackScript.tick`,
    `evolutions/scripts.py:1540-1567`): a vessel thrown back across the wind after it is through is
    not said to have missed stays, and the helm, steering for the new course, takes her round the
    long way, the tack ended by its steady timeout. The polacre's 407 s under nudge 18's process
    rule was such a tack (§2.2b). For every rig; not built here, and not reached by A1d as designed
    (no probe was thrown back with the evolution's draw); a mend at its cause is the lead's to give
    a package.

---

## 14. The steps, as the plan names them: the design for the lead's approval

The plan's A0 to A9 and V1 to V4 (`Plan-Package90.md` §6) as one design, drawn from §1 to §11 above
and from the hulls' second drafts. **The lead approves it, A1's above all, before stage 0L** lays
the whole lateen's interfaces (the plan's §5.2). Each step is keyed on what no committed file
carries except where its last column says what moves, each is merged alone and measured old beside
new, and the files each may change are the plan's §7.1.

**Third draft: A1 re-planned on the owner's answer to question 3** (§2.3, §2.4). The second
draft's A1 was one step built to "worn, not tacked". It is now four, built and merged in order on
the engine track before the tartane's file:
- **A1a**: the side and the bad hand;
- **A1b**: going about with the yard's change a part, and how it is ordered;
- **A1c**: the rules captain;
- **A1d**: taken aback and the bad hand in a breeze (since nudge 19 built, by the owner's decision: below).

The owner has said it is "a larger engine addition" and accepts it in the planning. What it adds
to the cost and the card is the plan's (§11, §14). Each is keyed so that no committed file moves.
Gone from the second draft: `Ship.wears_only()`, `tack ship` answered in words and nothing done,
and the yard changed only at "wind aft".

**Revised on nudge 18.** The lead ruled A1's figures (the rows below carry them, each JUDGEMENT).
**A1d was set apart as the owner's option** (§2.4.3), with its own size; **on nudge 19 the owner
decided it built**, so A1a to A1d are the card's, A1d after A1c and merged alone, two and a half
days (§2.4.3). **A2 is merged alone, before A1a**, since it moves the lugger's pinned
transcripts that A1a to A1c then hold as their guard (§2.3 item 9). A1b is re-estimated at three
and a half days (§2.3a).

| Step | The design | Key | What it moves (measured at the ground report) | Here |
|---|---|---|---|---|
| **A0** | Item 37: the generator's `PEAK_COEFF` read from the engine's curves (`data/sail_classes.yaml`), rounded to two places as now; a test holding the two together; the sprit class gaining the engine's 1.20. Under the owner's (a), agreed on 2026-11-18 | the generator | 74 `rating_kn` figures in 9 files (the studding-sail and ringtail booms, about 15 per cent up); truth 35's last clause and `test_studding`'s frigate at six points re-stated; five "no figure moved" records naming the booms; seven byte pins passing again by the regeneration; truths 9 and 14 hold | §1.3-§1.5 |
| **A1a** | **The whole lateen's side and the bad hand.** `dipping` allowed on a whole lateen (class `lateen`, no `cut_at_mast`); `Sail.lug_side` kept for it, **found once by `set_lateen`'s new nought-second step under `if: sail.dipping and sail.lug_side == none`** (the settee's `find_its_side`; the 64's and the 74's mizzen course and driver untouched) and **kept aloft by `take_in_lateen` and `furl_lateen`**, which clear nothing (their step lists, pinned by `tests/test_lateen.py:395-397`, unchanged); `against_the_mast` reads it, the loss **the lug's two-thirds** (ruled; JUDGEMENT; measured on the probes, 4 to 17 per cent of her speed close-hauled: §2.2a). `shift the mainsail` (`shift the mizen`, `shift the lateens`; `change` and `dip` its words for a whole lateen) by itself: refused on the good hand, held while a manoeuvre is in hand, its evolution `change_lateen` (peaked, never lowered; by itself 11¼ s a metre of yard, the settee's dip's, or the lugger's 14.6, not ruled: §2.4.4; one able hand for each 2½ m of yard, at least four; `too_few: all hands`). **The routing** (§2.3 item 3a): `verbs.evolution_key` gains `whole_lateen` for a lateen with `dipping` where the verb's mapping has the row (`shift` and `dip` to `change_lateen`), and `_take_canvas_words` marks a "for", so that `shift the mainsail for a new one` (or `for a spare`, `for the No. 2`, `for the bouffette`) goes to the sail room as today; `dip` refused for a lateen not whole, in today's words. The watch's line for a lateen left on the mast **after a gybe across the stern and after a shift round ahead through the bow**, which the stern watch does not hear today (at its cause: a dipping lug too, the lugger's case named in the card). `set_lateen`, `take_in_lateen`, `furl_lateen` and `reef_lateen` sized by the ship's data or `too_few: all hands`. The lateen mizen kept set hove to, `after_gaff_sails` never taking a whole lateen. **The heave-to refused, for a rig with a whole lateen set and neither head sail nor braced yard**, in the xebec's words ("She will not lie to under her lateens: there is no sail to bring her to."), her lying to booked; the five boats' and the schooner's refusal as today | `dipping` on a whole lateen | nothing of the eighteen files (none carries a whole lateen; the 64's and the 74's mizen courses are `cut_at_mast`); the library's count of evolutions by `change_lateen` (`tests/test_agents.py`); the vocabulary's lists by `shift` and `dip` for a whole lateen; the probes' tests as filed; `tests/test_lateen.py` and `tests/test_evolutions.py:1102` as they are; the bow's line for the lugger's lugs if mended at its cause (no pin expected; to grep) | §2.3 items 1, 3, 3a, 5 (hove to), 8 |
| **A1b** | **Going about with the yard's change a part, and how it is ordered.** The tack and the wear, and their kin that may change a settee, take the change on the settee's model, the yard peaked and not lowered, **at every place of §2.3a's table marked to mirror** (the holds and the runner's rule; the tack; the wear at its own point, the change begun at wind aft where the settee's is lowered at "up helm"; the fill away; the hove-to watch's forced round, without which B3.3b's silent bad hand comes back; the box-haul and wear short round; box her off): in stays once her head is through the wind (after "let go and haul" where she has head yards), in the wear once the wind is aft; she is tacked or worn when it is done. **`LateenChange`, a plain class beside `SetteeChange`** (ruled), with each yard's seconds and party and the yards together where the hands serve all, **one after another, the main first**, where they do not, which `SetteeChange` (one timer, no count) has not; **built only when a lateen is to be changed**, never a record of `scripts.py`, or truth 7-606 moves. Which yards are changed: by the order's clause after the order ("and shift the lateens", "and leave the lateens", one named), else by the ship's practice (`ship.extra["lateen_practice"]`: in stays and in wearing, each "shift" or "leave", **"shift" in both by default**), set by its own orders, **the verb first and no comma** (`leave the lateens in stays`, `shift the lateens in wearing`, "in going about" for both), and shown in the readings; a standing order sets it as any order. A lateen left lies on the bad hand (A1a) and the log says so. The change's seconds **8.7 a metre of yard** (ruled: the lugger's own rate) by the crew's factor, the same in stays and in the wear, in its own file, `tack.yaml`'s and `wear.yaml`'s timings untouched; its hands **one able hand for 2½ m, at least four** (ruled). **The car passed abaft the mast** (ruled: Willaumez; O'Scanlan's forward recorded). Her words name the lateens (§2.3 item 4). The clause and the occasion new modifier kinds in `orders/grammar.py` (`_parse_modifiers`), their words a table loaded by `orders/vocabulary.py`; the practice's verb named with its reading in the primer's going-about chapter (`docs/primer/05-going-about.md`) for `tests/test_grammar_book.py`. The aftermost whole lateen hauled aft at helm's a-lee and **eased as she pays off where she has no head sail set** (measured: the bare xebec 192 m against 1,064), eased at "up helm" and hauled aft as she comes to in the wear; a foremost whole lateen before a square main eased with the head sheets at helm's a-lee and drawn at "let go and haul" (the polacre). **A tack's end waits for her to pay off on a rig with a whole lateen set alone** (ruled; §2.3 item 5). **Three and a half days** (§2.3a) | `dipping` on a whole lateen | nothing of the eighteen files: the settee's and the lugger's paths as they are, **their guard sets (`tests/test_settee.py`, `tests/test_lug.py`, truth 7b-111) holding unmoved after A2's merge, which moves the lugger's two transcripts first** (§2.3 item 9; the third draft's "with their guard sets" corrected); the vocabulary's order lists (the clause, the practice's verb and occasion); the primer's going-about chapter naming the new verb and reading, `tests/test_grammar_book.py`'s two primer tests passing again; no checkpoint name (`lateen_practice` a plain dict of strings; `LateenChange` built only when needed); truth 7-606 and `tests/test_catalogue.py` unmoved by construction; every other rig's tack's end as it is | §2.3 items 2-5, §2.3a; §2.4.4, §2.4.5 |
| **A1c** | **The rules captain and `put her about`.** `put_about_choice` (`orders/navigation.py:1132`) wears where a whole lateen is set and the mean true wind is over **`LATEEN_TACK_KN`, 22 kn, a module constant beside `WEAR_WIND_KN`** (Forfait p. 119; JUDGEMENT on the figure; neither it nor `judge_course` reads a captain's book, so the constant serves every voice: the player's, a model's, the director's and the rules captain's), said ("a lateen is not put in stays in a strong wind"), the tack regardless with the land to leeward kept; the course's judgement (`judge_course`'s eye branch, the road of `steer`, `shape a course` and the captains' hourly leg) wears her in the same wind and words, and tacks her regardless where there is no room to wear (ruled); an ordered `tack ship` over 22 kn obeyed and warned once, words only; `tack ship` is never turned into a wear. The rules captain keeps the ship's practice, and from their book **read with defaults, written in no committed book** (ruled): **they set the practice by the wind**, `leave the lateens in stays` as the mean true wind falls under `lateen_leave_kn` (12 kn, Stratico's fine weather) and `shift the lateens in stays` as it rises over it, so that every tack, by `put her about` or by the course's judgement, reads it; they shift them by `shift the lateens` when a board on the bad hand has run `bad_hand_s` (1,800 s: the 2018 inventory; a little before §2.2a's break-even, 34 to 67 minutes at the ruled rate) or the wind rises over 12 kn; in wearing they are shifted by the practice; a lateen left on the mast after the wind has crossed the stern, or come round ahead through the bow, they shift, as they dip a lug (`Captain._across_the_stern`, `world/captains.py:3548`). The two keys read by `Doctrine.threshold(key, default)` (`world/captains.py:968`), in the corsair's new book only if anywhere | a whole lateen set | nothing of the eighteen files (none sets one); no committed book's count (`tests/test_subtypes.py:463-490` holds: the indiaman's thresholds must be the merchant's key for key and the revenue cutter's the cruiser's but `man_of_war_nm`, so a key in a committed book would move it); the captain's trials and `tests/test_captains.py` as a lens | §2.3 item 6 |
| **A1d** | **Built, by the owner's decision of 2026-11-18** (nudge 19; their words in §2.4.3): **a whole lateen held aback against its mast, a new rule of force in `physics/sails.py`.** It reads the whole lateen (class `lateen`, no `cut_at_mast`, with `dipping` and `lug_side`), the side (its one sheet, held to no side, holds its cloth on its yard's side while the wind comes round ahead, not on the deck's lee as `read_sheet` lays a single sheet today, `evolutions/trim.py:473-478`; carried over to leeward abaft the beam; drawn over by hands, a sheet drawn to a side keeping it, the lee included, in `set_sheet_angle`, l. 513-558, for a whole lateen alone) and the wind's face at its own height (`on_drive_face`, l. 1134). With the wind come round ahead onto the side its cloth lies on, `_read_rig` takes it as held (l. 600-606) and `_plate_force` (unchanged) makes it a plate aback and sets `backed` (l. 1136-1139); in the luffing band it shakes as today. **The strain**: in `_apply_loads` (l. 1515-1538) its pull on each spar of its chain (`_load_path`: its yard, then its mast) multiplied by `LATEEN_ABACK_LOAD` (about 2½) held aback and by `LATEEN_BAD_HAND_LOAD` (about 2) against its mast on the bad hand, module constants beside `LUG_AGAINST_MAST_AREA`; the cloth and the lines the plain pull; `physics/strain.py` unchanged, its wear over 1.0, chance over 1.5, certain failure at nought and `_wreck_spar` with its dependents the damage, no new kind. **The figures, JUDGEMENT for the lead**: aback strains its yard from about 28 kn and may carry it away from about 35 (in stays about 30 and 36); the bad hand from about 45 and 55; a mast that carries only its lateen with its yard, one that carries more from about 38 kn aback (the tartane's main); checked against the rules captain's 22 kn, 12 kn and 1,800 s, never at risk in their own handling (§2.4.3). **The evolution's part, at A1b's places**: a left lateen drawn over at "let go and haul" and "wind aft", a changed one's change begun there, a foremost lateen kept aback hung in stays; the bow watch's "aback against the mast"; `take in` begun on a lateen aback over `LATEEN_TACK_KN` waiting till it fills or is drawn (Forfait p. 119) (§2.4.3a). **Two and a half days** (two to three), merged alone after A1c | a whole lateen with `dipping` | nothing of the eighteen files; `tests/test_strain.py`, `tests/test_lateen.py` and `tests/test_settee.py` as they are; **the probes' going about by −9 to +13 m** in 15 and 25 kn with the evolution's part, so that A1b's figures stand within about two per cent (§2.2b; the polacre's 407 s of nudge 18's process rule a failed tack, not the rule's); A1b's figures and the hulls' truths of going about and the strain (Tar-D T-3, T-9; Xeb-D X4; Pol-D P5) measured after it, old beside new | §2.4.3, §2.4.3a, §2.2b |
| **A2** | The words of a rig with no yards, **at its cause** (widened on nudge 18), for every rig: the wear's "brace in the after yards" said only where she has after yards; "braced" said only where she has a braced yard, in the tack's end ("braced up on the ... tack"), the wear's end ("braced sharp up", `WearScript.words`) and the wear's wind-aft line ("hauled out and braced up"); the new words JUDGEMENT ("full and by on the ... tack"). **Merged alone, before A1a**, so that the guard set is moved once and then holds | the rig as filed | **the lugger's two pinned transcripts** (`tests/test_settee.py:1418-1456`): the tack's line at 180 s and the wear's at 1, 36 and 171 s, words only, every tick the same, old beside new in §2.3 item 9 (the transcripts run as they are in scratch); the lugger's case of `tests/test_evolutions.py:1169-1171`; **the cutter's and the smack's wear's first line only** (run; pinned by no test) | §2.3 item 9; §13 item 1 |
| **A3** | The helm's kind, for every tiller-steered hull: `helm: wheel` or `tiller` (default `wheel`); on a tiller the hit says the tiller or its ropes are shot away, the relieving tackles hook to the tiller as now, and `repair the wheel` is answered as the tiller's repair (a spare tiller shipped, or new tiller ropes rove), its time and hands JUDGEMENT for the lead | `helm: tiller` | the six files whose notes say tiller (the cutter, the lugger, the smack, the two schooners, the hermaphrodite brig), regenerated with the key; their words where a helm is shot away; truth 7-626 measured | §10 |
| **A4** | The boat in tow: a boat's `towed: true`, manned from alongside and not hoisted out; its words; its drag left out as small beside the hull's at her speeds (JUDGEMENT, measured against the trawl's form) | a boat's `towed` | nothing (no file tows a boat) | §3 |
| **A5** | A yard's level read from its place: `Ship.yard_level(yard)`, the rank by height of a braced yard among the braced yards on its own lower mast (0 the course), the yards under the bowsprit apart, read once a ship from the parts and held beside her as B3.4's memo is; read at the twelve places that read the parent's class today (`Design-Ship-Polacre.md` §5.1). A square yard over a whole lateen on the same mast with no braced yard below it (the tartane if her tréou is left out) counts the lateen yard as the level below (JUDGEMENT; the lead rules: Tar-D §5.1a). **Before the tartane's file**, the package's first pole main | the parts as filed | the smack: her topsail a topsail, not a course, in the heave-to, lie a-try and the take-in words with it set (no pinned passage sets it); a guard over every file's yard levels, old beside new, equal but for the smack | §4; Pol-D §5.1 |
| **A6** | The pole mast's quick handing ("amener en paquet"): the upper square sails of a pole lowered together onto the yard below, furled and reefed from it, the men on the yard below (Falconer; Steel p. 236); the topmast evolutions refused in words; times JUDGEMENT for the lead | a lower mast carrying braced yards above its lowest, with no topmast (the smack's, the tartane's and the polacre's mains) | the smack's topsail taken in and furled so (measured) | §4; Pol-D §5.1 |
| **A7** | Sweeps of a ship's own, never `oars:`: the `sweeps:` section (number, men each, a man's thrust and power, the tiring), package 82's law in the ship's substep, its state in `ship.extra["sweeps"]`; `out sweeps`, `in sweeps`, `give way`, `easy all`, `lie on your sweeps` where the hull has sweeps; an evolution manning `number × men_each` from the watch or all hands, the men taken from the sails and the guns while they pull; **the far body's pace in a calm** (`world/ships.py`'s `VESSEL_MIN_SPEED_KN`, l. 98, read at l. 849 and 865); the boat predicates kept a boat's | `sweeps:` | the library's count of evolutions; the vocabulary's order lists; the checkpoint's names list; the primer naming the sweeps' orders, for `tests/test_grammar_book.py` (an older gap, found at the third draft) | §5 |
| **A8** | The lateen in a gale: the reduction shifts storm canvas set `in_place_of` a whole lateen (the xebec's small lateens, the tartane's bouffette) at the topsails' second reef (Luce p. 476's level), in place of reefing; a whole lateen in no "courses" group. **The lateen row tuned** once, before the xebec's merge, on the truths of the lateen hulls on the branch then (the polacre's re-measured old beside new when she lands); the lead's leftover 4 of 2026-11-07 (the second reef queued on a course already being reefed) if the lead gives it here | storm canvas `in_place_of` a whole lateen; the lateen row, which no committed sail reads | nothing committed; the lateen hulls' own figures; `PEAK_COEFF["lateen"]` follows the row by A0 (a) | Tar-D §5.4 item 6; Xeb-D §5 |
| **A9** | Three decks: `_shut_crews` and `_rob_order` for a middle deck (`crew/quarters.py:418-435`, `:668-687`), the upper deck's crews robbed before the middle's; "the second deck" and "the third deck" in `orders/gunnery.py`; "the main deck" refused on a three-decker in words naming her decks; her words and rank are her rows (stage 0 and her builder) | a `middle` deck | nothing (no file has one) | §6.2-§6.3; Con-D §5.5, §6.3 |
| **V1** | The whole lateen drawn: three corners on its yard slung at a third on the mast's raked line, on its lee side; peaked up its mast while it is changed, its car passed abaft the mast (ruled); against its mast on the bad hand (`client/projection.js:815-816`, `904`, `1506`, `1537`) | as A1 | every committed file's picture unchanged | §11 |
| **V2** | The pole mast drawn with no doubling; the upper yards drawn down on the lower while lowered | as A6 | the smack's picture with her topsail lowered | Pol-D §13 |
| **V3** | The towed boat drawn astern on its painter | as A4 | none | §3 |
| **V4** | A port's words in the log's "-deck" form ("a middle-deck port") | the deck words | the 74's and the 64's "a lower port" become "a lower-deck port": words, old beside new | §6.2; §13 item 3 |
