# The owner's local work of 2026-10-25 to 27: a review for the lead

Reviewed 2026-10-27 against the project's line at `a196936` (the branch has since moved to
`908741f`, which is docs only and is taken into account below) and package 73's pushed
branch (`pkg-73` on the remote) at `d28716f`. The owner's tree was taken from `2774be3`; its
`docs/dev/M7-WorkPackages.md` already carries `7da0c0e`'s line for package 72's figures, so
his copy probably came from `7da0c0e`, which differs from `2774be3` in that one docs line.
His files were read as data and none of his code was run from his folder. The integration
check copied his tree into a worktree off `a196936` and ran the suite there.

## 1. What the owner's tree holds

**The practice-and-resupply package and the pivot gun.** On 2026-10-25 the owner had a
provisional pivot gun and a privateer schooner built ahead of package 75. The pivot gun is
a new gun place, `pivot`, with no side. Its crew trains it round to the mark at 3 degrees a
second, slower when short-handed, and it bears over either side between 60 and 140 degrees
off the bow. The schooner is a new generated file, `data/ships/privateer-schooner.yaml`:
Speedwell's hull with a "long tom" fit (a long 12 on the pivot, four 12-pounder carronades,
four swivels) and a "letter of marque" fit (six long 6s and four swivels). Arming the
schooner showed a defect in package 70's magazine, which drew the long 12's cartridges from
the same pool as the carronades'. On that he approved two proposals of his own, and the
package "practice and resupply" was built from them in stages by three builders and a lead.
Stage B keeps filled cartridges by gun kind and calibre, with loose powder below in 100 lb
barrels, and the generator writes the charges, the barrels and a King's fit's monthly
exercise allowance into the fits. The gunner and his party now fill cartridges at quarters
and by day (`freesail/combat/filling.py`), and a gun with no filled cartridge of its kind
waits at the cartridge phase. Stage A lets a ship take in powder and shot at eleven ports.
The Ordnance issues free and vouched to a King's ship of Britain at Plymouth (only in the
Sound or Cawsand Bay) and at Gibraltar, and merchants sell to everyone else, a King's ship
buying only "of necessity". The hoy is a two-stage port job; the galley fire is out while
she is alongside, which the meals read; and the gunner's account is a new paper. Practice
adds a cask hove over the side (it drifts, the lookout makes it out, and the first hit
knocks it to staves), a notional mark at a bearing and range, dumb show at the action's
pace with nothing spent, drill counts that nothing reads, a `practice` reading and a new
scenario, "Exercising the great guns". The package adds truths 7-161 to 7-171, about 130
unit tests in ten new files, and long records in the tuning notes, the spec, the Harness
and the work packages. It extends spec §7's magazine and §8's cycle, keeps §9's hit model
unchanged when the new size keyword is not given, and keeps marks out of §10's recognition,
morale and captains by construction. It changes no physics.

**The fixes.** After his playtests of 2026-10-26 and 27, most of them with a model as
captain of the frigate Amazon's armed tender, the cutter Raven, the owner made six fixes.
Two are to the door, and both bugs are also on the project's line today: a door seated on
another ship now names that ship when it re-reads its turns after a book is shelved
(`freesail/agents/remote.py`), and the door's terminal now reports a fold only for the
handover note, not for every sample added to an open turn (`freesail/agents/api.py`). The
hail is fixed in two ways (`freesail/world/hail.py`): `model_holds_her` called the property
`Captain.commands` as a method, so the error was swallowed and the player's ship was always
answered by table; and the table's heave-to was carried out on every hail, where the spec
says it is obeyed only on a demand. A new "free" intent lets a model captain on another
ship be given any goal, by the director's `ship "X": intent <words>` or by a scenario
ship's `free_intent:`; the far rules captain lies her to and lays no plan. Last, `keep
station ... of the Amazon` and `... of the frigate` now find the player's ship by her name
and any sail by her kind. The owner's debrief of 2026-10-27 (filed on the project's line
at `d6563db`) says how he holds these: the door fixes are key to keep, the free intent is
wanted in substance but provisional in form, and resupply and practice may be merged as
stopgaps for 75 and 77 to rewrite or redesign as they judge.

## 2. The saves mapped to the tree's states

The fingerprint of the owner's final tree is `965816e5af0d57bb`. It matches none of the
fingerprints in his playtest saves, so no save ran on his final tree. The intermediate
trees were rebuilt by reverting the fix commits' hunks to their `2774be3` text, and a
reimplementation of `fingerprint_of` (the script `fpscripts/fp.py` in the review's scratchpad,
which reproduces `965816e5af0d57bb` for the final tree) matched each save's fingerprint
exactly.

| Fingerprint | Tree state | Saves that ran on it |
|---|---|---|
| `fbe6b9264aee4097` | The whole ordnance package with the frigate's quarterdeck marked INCORRECT, before any of the six fixes | Eight: the naval cruise at ticks 318, 120919 and 120942; the privateer brig in Torbay at 138464; the privateer schooner out of Roscoff at 80693 and 80824; the frigate and cutter in Torbay at 387; the Raven at full detail, seed 609627938, tick 238 |
| `156d6782036194ca` | The above plus "Name the ship when a door reads its turns again" | The Raven at tick 1266 |
| `0a0c76dfa72752ed` | The above plus both free-intent commits (at sea and in a scenario) | m7-cutter-tender-test at tick 38587; the Raven at tick 38494 |
| `965816e5af0d57bb` | The final tree: the above plus the hail fix, the fold message and keeping station by name or kind | None |

The last three fixes therefore came after every save, which fits their docstrings citing the
playtest of 2026-10-27. Nothing the owner played exercised the hail fix, the fold message or
the station-keeping fix.

## 3. Every change and the recommendation

### The ordnance package

| Change | Files | Recommendation | Reason |
|---|---|---|---|
| The pivot gun (PROVISIONAL) | `freesail/ship/schema.py`, `ship/parts.py`, `ship/graph.py`, `combat/guns.py`, `combat/hits.py`, `crew/quarters.py`, `orders/gunnery.py`; `tests/test_pivot_gun.py`; `docs/design/Proposal-PivotGun.md` | Merge with changes | Self-contained and inert on every ship without a pivot, since every branch needs `place == "pivot"`; tested, and asked for by the owner. Keep it marked PROVISIONAL, fold it in after 73 (which also edits `hits.py` and `quarters.py`), and give 75 the per-gun arcs explicitly: the 60 to 140 band is one global constant today, so the Dolphin's pivot would inherit the schooner's arc. |
| The privateer schooner: generator, ship file and vessel type | `tools/gen_ships.py` (`schooner(armed=True)`, `privateer_schooner`, `schooner_armament`, `pivot_gun`), `data/ships/privateer-schooner.yaml`, `freesail/world/ships.py`, `world/captains.py` (`SIZE_RANK`); `tests/test_ships.py`, `test_ship_particulars.py` | Merge with changes | The generator reproduces the file byte for byte and `topsail-schooner.yaml` is untouched. The type cannot be held back alone without breaking the pivot gun's and the ship tests, so take it whole and PROVISIONAL. Fix the stale `schooner_armament` docstring (it still says the pivot is "no place the schema knows yet"). The description alias "a letter of marque" names a commission, not a rig, and claims a role word 75's sub-types will want: an open question for the owner. 75's brief must say whether it replaces this file with the Prince de Neufchatel or keeps both. |
| The frigate's quarterdeck marked INCORRECT against Winfield | `tools/gen_ships.py` (`frigate_armament` notes and source), `data/ships/frigate-36.yaml` (comments and source string only), `docs/dev/TuningNotes.md` | Merge as is | Comments and the source string only, written through the generator; nothing the game reads moves. It records a known error honestly for 75. |
| The magazine by gun kind and calibre, powder below (stage B) | `freesail/ship/parts.py` (`Magazine` layout 2, `charge_lb`, `_convert_70` and the rest), `ship/schema.py` (`FitSpec` charges, `powder_barrels`, `exercise_charges`, `QuarterBillSpec.filling`), `tools/gen_ships.py` (`fit_magazine`, `exercise_allowance`, `filling_party`), regenerated `brig`, `cutter`, `frigate-36` and `merchant-brig` files; `tests/test_magazine.py` | Merge with changes | It fixes a real defect of §7's magazine, is reproducible from the generator, and converts old pickles once without logging or drawing. It collides with 73 in `parts.py`, `schema.py`, `gen_ships.py` and the ship files, so rebase it on 73 and regenerate the ship files from the merged generator, never merging them as text. Add a line to §7 itself (the as-built note sits under §8) saying the magazine is now by kind. `schema._gun_words` repeats `parts.gun_words` and may go. The charges' shares stay UNVERIFIED until Table No. 29 is read. |
| The gunner's filling | `freesail/combat/filling.py` (new), `combat/guns.py`, `combat/action.py`; `tests/test_filling.py` | Merge with changes | Needed for stage B and well guarded (it returns at once while the magazine is full, and a test proves it). Fix the stale comment at the call in `action.py` ("stage 0: neither says or does anything yet"). The fillers are read and never moved, so they take no hands from other work; that sits against rule 2 and is documented as decision 5 of the build. Put the fillers as real posts in 75's or 77's brief. |
| Powder and shot taken in at a port (stage A) | `freesail/world/ordnance.py`, `orders/ordnance.py`, `world/service.py` (new); `orders/port.py`, `orders/__init__.py`, `world/ports.py`, `world/places.py`, `world/needs.py`, `crew/victuals.py`; eleven `data/ports/*.yaml`; `data/papers/papers.yaml`; `tests/test_ordnance.py`, `test_powder_orders.py`, `test_service.py` | Merge with changes | Sound, cited by article, every refusal tested word for word. Three things to settle at the fold-in: `Papers._merge` mends the catalogue from `PAPERS_PATH` on every miss, even for a `Papers` built from another path, which should read the catalogue's own path or be limited to the old-checkpoint case; `block_of` gives a pickled `Port` this build's ordnance block silently, which is acceptable but should be said in the as-built note; and the duplicated helpers (`_a`, `_cap`, `_and`, `_barrels_words`) should use the existing ones. The owner's judgement figures (prices, Plymouth's town, Lisbon's knob, the hoy's hours) stand until he rules otherwise. |
| Practice at marks: the cask and the notional mark | `freesail/combat/marks.py` (new), `combat/action.py`, `combat/hits.py`, `combat/shot.py` (`hit_chance` size keyword), `combat/guns.py`, `world/lookout.py`, `world/reckoning.py`, `evolutions/action_scripts.py`, `data/evolutions/heave_mark.yaml`, `orders/gunnery.py`, `api/practice_readings.py` (new), `api/action_readings.py`; `tests/test_practice.py`, `test_practice_lookout.py`, `test_practice_orders.py` | Merge with changes | Well isolated by the `practice:` prefix and a `practice` random stream opened lazily, so no existing draw moves. Fold it in with the rest after 73, and give 77 the evolution. A rules captain's fighting book will open fire on a cask by the range reading; that is accepted by design and should stay in the as-built note. |
| Dumb show and the drill | `freesail/combat/guns.py`, `orders/gunnery.py`, `api/action_readings.py`, `api/practice_readings.py`; `tests/test_dumb_show.py` | Merge with changes | Correct and tested, including old pickles. Remove the duplicated word helpers at the fold-in: `_seconds_words` is in both `guns.py` and `practice_readings.py`, `_cardinal` repeats `crew.model.number_words`, and `gunnery._rank` repeats `parts._kind_rank`. |
| "The shot into the sea" for a shotted gun with no mark | `freesail/combat/guns.py` (`_discharge`, `minute_line`) | Merge as is | It corrects wrong words ("a blank charge" for a shotted gun). Truth 7-147's fog gun reads new text, but nothing asserts it, and a test keeps today's text for any minute without such a volley. |
| The scenario "Exercising the great guns" | `data/scenarios/exercising-the-great-guns.yaml` | Merge as is | Data only, following `first-action.yaml`'s header form. |
| The package's edits in shared world and order files | `freesail/world/lookout.py`, `world/reckoning.py`, `world/needs.py`, `world/places.py`, `world/ports.py`, `orders/port.py`, `standing/runtime.py`, `api/readings.py`, `data/vocabulary.yaml`, `data/scenarios/merchant-ship.yaml` (`papers: {service: merchant}`) | Merge with the package | They belong to the ordnance fold-in and should be judged and merged with it, not as separate fixes. `data/vocabulary.yaml` and `api/readings.py` are also changed by 73 and will need a hand merge. |

### The fixes

| Change | Files | Recommendation | Reason |
|---|---|---|---|
| Name the ship when a door reads its turns again | `freesail/agents/remote.py`; `tests/test_crews.py` | Merge as is | A one-line fix of a real bug that is on the project's line today; `reread` now passes `**self._ship_param()` like every other call, and a test drives the real server. Neither file is touched by 73, so it can land now. |
| Say a fold at the door's terminal only for the handover | `freesail/agents/api.py`; `tests/test_api_door.py` | Merge as is | A real bug in what the terminal says, also on the line today; no game state touched; both cases tested. Comparing `folded` to the handover marker, rather than testing `handover` for truth, would be more exact, but the note is never empty in practice. Can land now. |
| A hail of the player's ship waits for him, and moves no sail unasked | `freesail/world/hail.py`; `tests/test_signals.py` | Merge with changes | Both bugs are real and the fix matches spec M7 §4's as-built words. Two changes first. The `commands` branch applies to any world, so a crewed ship under the director's hand, or a captain standing aside, now keeps a hail pending that nobody answers; limit it to the player's ship (`getattr(other_world, "parent", None) is None`, as its docstring says) unless the owner wants that silence. And the heave-to gating also changes `exchange_words`, the exchange between two far rules captains: before, the hailed far ship was hove to indefinitely or made sail at every first meeting within hail. That very likely moves recorded passages where far brains meet (the convoy truths 7-145, 7-151, 7-152 with its pinned ticks `(2760, 2866, 3000, 5280)`, 7-155, 7-157, 7-159, and the privateer's 7-153). The owner's whole slow tier predates this fix and the fast tier does not run those truths, so re-run them before merging. It may also bear on the convoy's stall in his debrief. |
| Free intents for ships on the sea | `freesail/world/orders.py`, `world/captains.py`, `world/brains.py`, `agents/agent.py`; `tests/test_brains.py`, `test_crews.py` | Merge with changes | The owner wants it in substance and it builds toward 82. Before merging: the crewed `Captain` should short-circuit a free intent as the far one does (today it re-plans every minute and writes a NOTABLE "plan ... no legs" line each time, which the 61-second test misses); a free intent should keep the ship's service role, since today a King's cutter or tender falls to the merchant's doctrine; `FREE_WARNING` should say she is lain to, not kept as she is; and the director's form text in `agents/director.py`, the spec, the Harness and the tuning notes should record it. Whether a director's unreadable `intent` should still be refused, with the free form given by an explicit word, is an open question; as built a misspelt port becomes a free intent and she lies to indefinitely. |
| Free intents for a scenario's ships | `freesail/world/scenarios.py`, `world/ships.py`, `world/captains.py`, `world/brains.py`; `tests/test_scenarios.py` | Merge with changes | Clean, validated in the loader's pattern and tested, but it rests on the free-intent core and must take the changes above with it. |
| Keep station on the player's ship by her name, and on a sail by her kind | `freesail/orders/station.py`; `tests/test_crews.py` | Merge with changes | It fixes a real refusal and is tested. The kind match searches the whole sea by truth, so "keep station on the frigate" finds a frigate nobody aboard can know of; limit it to sails in sight through `_sighting_of` in the same module. Also tighten the word match, since `\bbrig\b` takes a brig-sloop. The name match leans on `player_shadow` and the "the ship" id, which 82 and the one-world work will rework. |

### The tests and records

| Change | Files | Recommendation | Reason |
|---|---|---|---|
| Truths 7-161 to 7-171 and their slow-tier entries | `tests/test_known_truths.py`, `tests/conftest.py` | Merge with changes | Strong truths that pin states, kinds, counts and bands, never digests (the owner's machine gives different digests, decision 26); no existing truth line changed. They collide with 73's numbers and must be renumbered after 73's last truth, everywhere they are cited. Run the six slow ones (7-161, 7-166, 7-167, 7-168, 7-170, 7-171) on the build machine and record the build machine's digests in the docstrings beside the owner's. Correct the carried docstring slip in 7-164 (the chasers' 56 s is their best, not their 70 s mean). |
| The ten new test files | `tests/test_dumb_show.py`, `test_filling.py`, `test_magazine.py`, `test_ordnance.py`, `test_pivot_gun.py`, `test_powder_orders.py`, `test_practice.py`, `test_practice_lookout.py`, `test_practice_orders.py`, `test_service.py` | Merge with the code | They stand or fall with what they test; no skip, xfail or digest pin. `test_practice.py` checks that the docs carry the as-built text, so record edits at the fold-in (renumbering, hashes) must keep it passing. |
| Unit pins moved by the new paper, evolution and brief size | `tests/test_agents.py`, `test_places.py`, `test_server.py`, `test_officer.py` | Merge with changes | Legitimate moves with reasons: 88 evolutions (87), 11 papers (10), the handover budget 19,000 (18,500) with the brief at 11,214 tokens at the seat. The old figures are in the tuning notes and, for the budget, derivable from the comment chain ("five hundred more"), which is how earlier packages wrote that comment. Write the old figure beside the new in each comment anyway, and correct the stale "package 71: the hoist beside 70's three" on the 88 line. All four counts will move again with 73's evolutions and brief, so recompute them on the merged tree. |
| The ship-file and privateer tests | `tests/test_ship_particulars.py`, `tests/test_ships.py` | Merge with changes | The generator comparison now also covers `privateer-schooner.yaml` and `merchant-brig.yaml`, which strengthens the no-hand-edit guard. Merge with the schooner; 75 will churn the provisional fits. |
| The fixes' tests | `tests/test_crews.py`, `test_api_door.py`, `test_signals.py`, `test_scenarios.py`, `test_brains.py` | Merge as is, with the fixes | Each pins a bug found in play. The reversed assertion in `test_brains.py` (`intent fish the Wolf` now taken as free, with the warning) follows a deliberate change, and `read_intent`'s refusal of the same words is still asserted in `test_crews.py`, so it is not a weakening. Add tests for the changes asked above: the director's hand still answered by table, the crewed captain quiet under a free intent, and a station refused on an unseen frigate. |
| The design notes | `docs/design/Proposal-PivotGun.md`, `Proposal-MagazineResupply.md`, `Proposal-PracticeFiring.md`, `Build-PracticeAndResupply.md` | Merge with changes | Thorough, sourced, UNVERIFIED marked. Replace the owner's local commit hashes with the fold-in's own and renumber the truths. |
| The as-built records | `docs/TechnicalSpec-M7.md` (§8 "As built"), `docs/agents/Harness.md` (§21f), `docs/dev/M7-WorkPackages.md` ("Practice and resupply as merged"), `docs/dev/TuningNotes.md`, `docs/primer/14-the-port.md`, `docs/primer/22-an-action.md` | Merge with changes | Reword the one line that names a model (section 4). Recast the local hashes (`4a12e97`, `b492580`, `3414581`, `fde16fb`, `b71d20a`, `53fd23e`, `0127253`, `df31dcd`, `d4ad917`, `610901b`) as the project's own commits. Settle primer 22's "engages at 10:07" against truth 7-133's 10:06. Add the §7 note on the magazine by kind. Take the work-packages section by hand into the project's current file (section 7), never the owner's file whole. |
| Package 72's whole-tier figures line | `docs/dev/M7-WorkPackages.md` | Already on the line | Identical to `7da0c0e`'s text; nothing to take. |
| Squadrons design: pace truths renumbered | `docs/design/Design-Squadrons.md` | Merge as is | "Truths 7-161 and 7-162" becomes "7-159 and 7-160", which is right; the project's line still has the wrong numbers, and they would otherwise point at 73's truths. Can land now. |
| The owner's consent records | four new files under `docs/agents/consent/`, dated 2026-10-25 and 2026-10-26 | Leave out | His own records, not to be merged, and their file names carry model and vendor names. The other twenty files in that folder are already on the line and unchanged. |

## 4. Rule breaches

**A model name in a repository file.** `docs/dev/TuningNotes.md`, about line 10415, in the
new section "Open, for the lead: found directing the owner's Roscoff station (2026-10-26;
not fixed)", names a model as the frigate-36's officer of the watch. Reword it to "a model
at the officer of the watch's station" before the fold-in. It is the only new match the
owner added outside the consent folder; none of the 23 new files carries one. The sweep
also matched 127 files already on the project's line at `a196936`, among them the package
labels in the work-packages table that the owner's copy repeats; those are not his and are
the lead's to judge as a separate matter.

**The consent records.** Four new files under `docs/agents/consent/` carry model and vendor
names in their file names. They are the owner's records and are left out of the fold-in;
nothing to do beyond not copying them.

**Hand-edited ship files.** None. The integration check ran the owner's `tools/gen_ships.py`
in the worktree and into a separate folder: all eight ship files came out byte for byte the
same. Every changed figure in `brig.yaml`, `cutter.yaml`, `frigate-36.yaml`,
`merchant-brig.yaml` and the new `privateer-schooner.yaml` traces to the generator, and
`topsail-schooner.yaml` is identical to the line's. What remains is procedural: when 73
lands, its own generator changes and his must be merged in `tools/gen_ships.py` and the ship
files regenerated, not merged as text.

**Recorded-passage pins.** None moved in the diff: no digest, line count or tick changed in
any test, and the new truths record digests only in docstrings. The unit-count pins that
moved carry reasons, and their old figures are in the tuning notes but not beside the new in
every test comment; a soft departure, to be mended at the fold-in. The real risk is the hail
fix: by removing the far-to-far heave-to it very likely moves pinned passages (7-152's ticks
among them) that were last run before it. That is not yet a breach, but it becomes one if the
fix is merged without re-running them; any pin that moves must be moved with the old figure
beside the new and the reason, proven by reverting the gating.

**Skipped, disabled or weakened tests.** None. No skip or xfail was added. Six new truths go
to the slow tier, and the two new `pytest.importorskip("fastapi")` calls in `test_crews.py`
follow that file's pattern. The one reversed assertion, in `test_brains.py`, follows a
deliberate change with the refusal still asserted elsewhere.

**The physics.** Not changed. No file under `freesail/physics` is touched; `combat/shot.py`'s
`hit_chance` gains an optional size keyword whose default keeps every figure, checked by a
table of inputs. `freesail/ship/parts.py` (526 changed lines) was read for the magazine and
the gun but not line by line for anything else; nothing in the diff touches hull, sails or
sea.

## 5. Collisions with the packages in flight or briefed

**Package 73, building now.** Its brief and its design (`Design-WaterAndHealth.md`, line 481
on 73's pushed branch) take truths "7-161 onward", so the numbers collide directly. On
its three commits so far, 73 already changes thirteen of the files the owner changed:
`data/ships/brig.yaml`, `cutter.yaml`, `frigate-36.yaml`, `merchant-brig.yaml`,
`data/vocabulary.yaml`, `freesail/agents/agent.py`, `api/action_readings.py`,
`api/readings.py`, `orders/__init__.py`, `ship/parts.py`, `ship/schema.py`,
`world/orders.py` and `tools/gen_ships.py`. Its brief points at more (`combat/hits.py`,
`crew/quarters.py`, `combat/action.py`, `world/needs.py`). It will also move the same unit
counts (evolutions, likely papers, the brief's size). Resolve it by letting 73 merge first,
since its builder is writing 7-161 now and the new 84 row says "73 and the owner's local
work merged first": rebase the ordnance package on merged 73, renumber its truths after
73's last, merge the generator by hand and regenerate the ship files, and recompute the unit
counts on the merged tree. The door fixes and the squadrons correction touch none of 73's
files and need not wait.

**Package 74 (prizes, the strike and the far fight; now after 84 and 82).** `world/ports.py`
and the port files now carry an `ordnance:` block and the hoy as a port job, and the owner
ruled captured powder as prize goods to 74. Resolve it by a line in 74's brief naming the
block, the hoy job and `world/service.py`'s rules of who may buy, so 74 builds on them rather
than beside them.

**Package 75 (the ships and their armament).** Four collisions. The provisional
`privateer-schooner.yaml`, its "privateer schooner" description and the "a letter of marque"
alias sit where 75's Prince de Neufchatel and its "sub-types as fits and roles" will go; the
owner's trade-trial finding (arming `topsail-schooner.yaml` made the merchant schooner engage)
argues for separate files, 75's brief for fits. The pivot gun's global arc must become a
per-gun arc. Table No. 29's charges replace the UNVERIFIED shares through the generator. And
correcting the frigate's quarterdeck against Winfield moves the quarter bill, the magazine,
the filling party and the allowance, and so truths 7-133 to 7-164 and the renumbered
practice truths. Resolve all four by adding them to 75's brief, with the owner's answer on
file versus fit.

**Package 77 (the gunnery's evolutions).** Practice's `heave_mark` evolution, dumb show and
the notional fillers are the gunnery's evolutions in a first, stopgap form; the debrief says
75 and 77 may redesign them as they judge. Resolve it by a line in 77's brief that it takes
them over, makes the gunner and the quarter gunners posts that compete for hands, and keeps
or replaces truths 7-162 to 7-166 (renumbered) with its own.

**Package 82 (the boat, and the player aboard another ship; now re-briefed after 83 and run
with or after 84).** The free intent, the hail's "held by the player" rule and keeping station
on the player's ship by name all lean on today's player-centric seam (`player_shadow`, the
"the ship" id, a crewed ship as a World of her own). The hoy as a vessel was deferred to 82.
None of this pre-empts 82. Resolve it by merging the fixes in the form asked above and naming
the three in 82's re-brief as things it reworks.

**Packages 83 and 84 (the one-world study and refactor, on the line since `908741f`).** 83
writes no code, so there is no file collision, but it maps the player-centric assumptions in
the code, and the free intent, the hail rule and the station match add to that list. 84's row
says the owner's local work merges before it. If the fold-in lands while 83 is studying, tell
83 so its map reads the merged tree.

## 6. The integration check's figures

The check copied 840 files (714 from `freesail`, `data`, `tests` and `tools`, and 126 from
`docs`) over a worktree detached at `a196936` (`verify-owner` in the review's scratchpad, left in
place). Against `a196936` the worktree shows 70 modified files and 23 new ones; the
owner's tree deletes no file. None of the 24 consent files was copied; the worktree keeps the
line's 20.

`ruff check .` (ruff 0.15.8) passed with no findings, and `ruff format --check .` reported
269 files already formatted.

The fast tier gave 3,826 passed, 0 failed, 0 skipped and 0 xfailed, with 361 slow tests left
out as usual. One file did not collect: `tests/test_pictures.py` stops on
`ImportError: cannot import name '_imaging' from 'PIL'` at its `importorskip` on line 39.
Pillow is broken on the check's machine (the same import fails from outside the project), and
the owner did not change that file, so this is the machine's, not his. The log is `verify-fast.log` in the review's
scratchpad.

The ten new test files, run with `--slow -n 4`, gave 183 passed, 0 failed, 0 skipped, 0
xfailed and no errors. The log is `verify-slow.log` in the review's scratchpad.

The generator reproduced all eight ship files byte for byte, both in place (md5 sums and
`git status --short data/ships` the same before and after) and into a separate folder
(`cmp` matched all eight).

The forbidden-name sweep found one new match, the tuning-notes line at 10415, and one
apparent addition in `docs/dev/M7-WorkPackages.md` line 42 that is only the line's own older
text put back by the copy.

Not run: the six slow known truths of the package (7-161, 7-166, 7-167, 7-168, 7-170,
7-171), the rest of the slow tier, and in particular the convoy and privateer truths the hail
fix may move. For comparison, the owner's own record of the whole slow tier, on his local
`610901b` (before the hail fix), with `--slow -n 2` and the pace tests in 107 minutes: 4,183
tests, 10 failed and 14 skipped. He reports the ten failing the same way on his baseline
`4a12e97`: the trade trial in thick weather (`df5f02eb6e6ce68a` for `cfa538b19cb0d2fe`), the
Ushant lee shore (`eb06bd7b36cbeff8` for `ed48ca3d61e52f20`), the trade stranger (1,248 lines
for 1,246), the gate 5c cruise's four (96,480 for 96,540; truth 77's digest
`ea265e4704a06726` for `6abbbff4d7fa1a57`; truths 78 and 79), gate 6a (110,400 for 110,340),
gate 5b (767 lines for 766), and truth 7b-108, where the server printed nothing. He puts them
down to his machine. Package 72's record on the build machine was 3,973 passed, 11 expected
failures, 2 skipped and none failed.

One correction to the check's note on `docs/dev/M7-WorkPackages.md`: the owner's copy already
has package 72's figures from `7da0c0e`, so it lacks two of the line's later edits, not three
(the builders' push permission and 73's lost and relaunched run), and now also `908741f`'s
rows and briefs for 83 and 84. A whole-file copy would undo all of them.

## 7. The merge plan

1. **Now, ahead of 73.** On a branch off the line's head, take whole the two door fixes
   (`freesail/agents/remote.py` and `freesail/agents/api.py` with their tests in
   `tests/test_crews.py` and `tests/test_api_door.py`, the hunks for those tests only) and
   the correction to `docs/design/Design-Squadrons.md`. None of these files is touched by
   73. Run the fast tier and merge. This gives the owner the door fixes he calls key for
   model-captain testing at once.
2. **Still ahead of 73, if the lead wishes.** The free intents, the hail fix and station
   keeping by name or kind, with the changes in section 3 made: the crewed captain's
   short-circuit, the service role kept, the warning's words, the records; the hail's
   `commands` branch limited to the player's ship; the kind match limited to sails in sight.
   Two of their files (`world/orders.py`, `agents/agent.py`) are also 73's, so these may wait
   for 73 instead; the conflict is small either way. Before merging the hail fix, run the
   whole slow tier with the pace tests on the build machine, and check truths 7-143 to 7-160
   and the convoy and blockade scenarios in particular. If a pin moves, bisect to the gating
   (revert it and see the old figure come back), move the pin with the old figure beside the
   new and the reason, and record it in the tuning notes.
3. **After 73 merges: the ordnance package.** Branch from the merged line. Take whole the new
   files: `freesail/combat/filling.py`, `combat/marks.py`, `world/ordnance.py`,
   `orders/ordnance.py`, `world/service.py`, `api/practice_readings.py`,
   `data/evolutions/heave_mark.yaml`, `data/scenarios/exercising-the-great-guns.yaml`, the
   eleven port files, `data/papers/papers.yaml`, and the ten new test files. Take with edits,
   hunk by hunk on top of 73: `ship/parts.py`, `ship/schema.py`, `ship/graph.py`,
   `combat/guns.py`, `combat/action.py`, `combat/hits.py`, `combat/shot.py`,
   `crew/quarters.py`, `crew/victuals.py`, `evolutions/action_scripts.py`,
   `orders/gunnery.py`, `orders/port.py`, `orders/__init__.py`, `standing/runtime.py`,
   `api/action_readings.py`, `api/readings.py`, `world/lookout.py`, `world/reckoning.py`,
   `world/needs.py`, `world/places.py`, `world/ports.py`, `world/ships.py` and
   `world/captains.py` (the privateer type and `SIZE_RANK`), `data/vocabulary.yaml`,
   `data/scenarios/merchant-ship.yaml`, and `tools/gen_ships.py`. The edits are the ones
   named in section 3: the stale docstring and comment, the duplicated helpers, and
   `Papers._merge` reading its own path. Merge `tools/gen_ships.py` by hand, then run it and
   commit the regenerated `data/ships/*.yaml` with the new `privateer-schooner.yaml`; never
   take the owner's ship files as text. Check that `test_ship_particulars.py` passes against
   the regenerated files.
4. **Renumber and re-pin.** Renumber truths 7-161 to 7-171 to follow 73's last truth, in
   `tests/test_known_truths.py`, `tests/conftest.py`'s `SLOW_TESTS`, the design notes, the
   spec, the Harness, the tuning notes and the primers, keeping `test_practice.py`'s
   documents test passing. Recompute the evolution and paper counts and the officer's handover
   budget on the merged tree, writing the old figure beside the new in each comment.
5. **The records.** Take the four design notes whole, with the local hashes replaced and the
   truths renumbered. Take the owner's sections of the spec (§8's "As built", plus a new line
   in §7 on the magazine by kind), the Harness (§21f), the tuning notes and primers 14 and 22
   into the line's current files, with the model-named line reworded, the local hashes recast
   as the fold-in's commits, and 10:06 or 10:07 settled. Add the "Practice and resupply as
   merged" section to the line's current `docs/dev/M7-WorkPackages.md` by hand; do not copy
   the owner's file. Add the lines to 74's, 75's, 77's and 82's briefs from section 5.
6. **Run.** `ruff check` and `ruff format --check`; the fast tier; the whole slow tier with
   the pace tests on the build machine, including the renumbered six slow truths; and record
   the build machine's digests and line counts for the new truths and the practice scenario
   in their docstrings, beside the owner's.
7. **Leave out.** The four new consent files under `docs/agents/consent/`; the owner's
   `docs/dev/M7-WorkPackages.md` as a whole file. Nothing needs doing about
   `tests/test_pictures.py`: the owner did not touch it, and its failure to collect is the
   check machine's broken Pillow.

**Open questions for the owner.**

1. Truths 7-161 to 7-171 collide with 73's. May they be renumbered after 73's, with the
   practice and resupply work folded in after 73?
2. After the hail fix, did you run truths 7-143 to 7-160 and the convoy and blockade
   scenarios? Before it, every first exchange between two far rules captains hove the hailed
   ship to indefinitely or made her sail, which may also bear on the convoy's stall you
   reported.
3. Is it intended that a crewed ship under the director's hand now keeps a hail pending and
   gives no answer, where the table answered before?
4. Should a King's cutter or tender given a free intent keep her King's-ship doctrine rather
   than the merchant's? And under a free intent, should the crewed rules captain lie her to
   as the far body does, or keep her as she is, as the warning says?
5. Should an unreadable `ship "X": intent <words>` from the director still be refused, with
   the free form given only by an explicit word, as the scenario's `free_intent:` is?
6. Should "keep station on the frigate" take only a sail in sight?
7. Should 75 replace the provisional privateer schooner with the Prince de Neufchatel, or
   build her beside it? Should armed variants be fits of one file or separate files, given
   your trade-trial finding? And should "a letter of marque" stay a description alias?
8. Should the gunner and the quarter gunners become real posts competing for hands, and in
   75 or 77?
9. Do you want Table No. 29's charges read from the page before the fold-in, or left to 75?
   And should 75 correct the frigate's quarterdeck against Winfield, moving truths 7-133
   onward?
10. Do your judgement figures in the port files stand: Plymouth's town selling none,
    Gibraltar selling, Lisbon's `sells_in_war_to` unset, the prices (£5 and £12 at home, £6
    and £14 abroad), and the hoy's hours?
11. `shot.lee_port_shut` is still never called, against spec §9. Which package wires it? The
    pivot gun should be left out of it.
12. Your whole slow tier gave 14 skipped where the build machine gives 2. Which tests skipped
    on your machine, and why?
13. Primer 22 says the privateer engages at 10:07, truth 7-133's docstring 10:06. Which did
    you measure?
14. May the Roscoff line in the tuning notes say "a model at the officer of the watch's
    station" in place of the model's name?
15. Was your copy taken from `7da0c0e` rather than `2774be3`? Its work-packages file carries
    `7da0c0e`'s line.
16. No save ran on your final tree with the hail, fold and station fixes. Do you want a short
    replay on it before the hail fix is relied on?
