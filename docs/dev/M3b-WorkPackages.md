# Milestone 3b work packages: contracts between them

Milestone 3b is specified in `docs/TechnicalSpec-M3b.md`, whose research base is `docs/references/RigGeometryNotes.md` and `docs/references/Tables.md`. Read all three before your section. The code on the branch is milestone 3 as passed at its gate: the crew, the runner with hands, thirty-nine evolutions, the browser client, 886 tests.

## Working rules

The milestone 3 rules (`docs/dev/M3-WorkPackages.md`, top) hold: stay inside your files, build what the specification says at the size it says, no new dependencies, deterministic, ship's-log voice, run the whole suite and read the summary line yourself, report in the set order. Two rules are added for this milestone:

- **Every number names its source.** A constant, a ship-file value or a curve point carries a comment citing the work and article (Fincham art. 102, Luce App. E, `Tables.md` §1) or the word "judgement" with a sentence of reasoning. The research notes give the citations; do not cite from memory.
- **Physics before rules.** Where the specification says a behaviour comes through the physics (studding sails flogging, worn canvas blowing out, bowlines flattening the sail), do not shortcut it with a precondition. The only refusals allowed are the ones the specification names, and each says why in words.

The compatibility rule (spec 3b §1) is a test and it must pass with your work in: the milestone 2 and 3 truths keep passing, with truths 1 and 2 allowed to move within the stated band and their new values recorded.

## Waves and dependencies

```
wave 1:  21 rig geometry (brace limits, trim, catharpins, bowlines, adjacent yards)
         22 canvas (numbers, condition, wear, the sail room, storm canvas, ringtail and kin)
wave 2:  23 studding sails through the physics, booms rigged in, the view
wave 3:  24 truths 24 to 33, tuning notes, primer, gate 3b
```

21 and 22 are independent and edit different files, except the generator and the ship files, which both need: 22 owns `tools/gen_ships.py` and the ship files; 21 writes the brace limits and the bowline parts it needs as an exact patch in its report and the lead applies it to the generator before 22 regenerates, or 22 applies it if 21 lands first. 23 starts when both have landed (it needs the sail room for the boom state and the bowline machinery for the tack script's order of work). 24 starts last.

## Package 21: rig geometry (`freesail/physics/sails.py` for the bowline and trim effects, `freesail/physics/strain.py` for the catharpin rating factor, `freesail/ship/parts.py` for the new states, `freesail/orders/verbs.py` and `data/vocabulary.yaml` for the new orders and modifiers, `freesail/evolutions/trim.py`, `freesail/evolutions/scripts.py` for the tack and wear scripts' bowline and trim steps, `data/evolutions/` for the catharpin and bowline evolutions, `tests/test_rig_geometry.py`)

Spec 3b §2 to §5.

- **Brace limits:** the values in §2.1 with Fincham art. 102 cited; write them as a patch to `tools/gen_ships.py` in your report (the exact new numbers per yard for both ships and the comment text); do not edit the generator yourself.
- **Head and after yards:** `AFTER_YARDS_SHARPER_DEG = 3` in the trim order, in `brace sharp up` for the whole ship, and in the tack script's final trim; the `head yards sharper` modifier; the log line names the difference ("Braced up, the after yards three degrees sharper.").
- **Catharpins:** `Spar.swiftered_in` on lower masts; evolutions `swifter_in_catharpins` and `ease_catharpins` (boatswain's party, aloft, about twenty minutes a mast, judgement); the brace-limit gain on that mast's lower yard (`CATHARPIN_GAIN_DEG = 4`) read wherever the limit is read (find every reader: the scripts, `verbs._brace`, `trim.py`, `strain.py`'s swung-yard rule); the athwartships rating factor (`CATHARPIN_RATING_FACTOR = 0.85`) in `strain.py` for that mast while swiftered in; orders `swifter in the catharpins [on the main]`, `ease the catharpins [on the main]`.
- **Bowlines:** the topsail bowlines and the schooner's as a patch to the generator in your report (class `bowline`, `of` the sail, sided, rated like a topsail sheet's lighter rope, Luce ch. IV); `Line.hauled` for bowlines; orders `haul the weather bowlines`, `steady out the bowlines`, `haul the fore bowline`, `let go the bowlines`, `ease the bowlines`; the luff gain (`BOWLINE_LUFF_GAIN_DEG = 4`) and a small drag reduction in `sails.py` when hauled and braced up on that tack; slacked automatically past `BOWLINE_SLACK_ANGLE_DEG = 40` from square; let go and re-hauled by the tack and wear scripts at the period moments (Luce's sequences: "let go the bowlines" as the helm goes down; "steady out the bowlines" when braced up); hands from the forecastlemen and afterguard, a minute a bowline.
- **Adjacent yards:** the computed clearance of §5 with its floor, checked after the aback and studding sail rules, refused in words.
- Tests: each mechanism on both ships; the refusals' wording; the compatibility rule with your changes alone (truths 1 and 2 within the band, the rest exact); determinism.

## Package 22: canvas (`tools/gen_ships.py` and both ship files, `freesail/ship/schema.py` for `canvas_no` and the sail-room list, `freesail/ship/parts.py` for the sail-room model, `freesail/physics/strain.py` for wear and the effective rating, `freesail/physics/sails.py` for the baggy-luff term only, `freesail/evolutions/scripts.py` for `Shift`/`Bend`/`Unbend` choosing from the sail room, `data/evolutions/` for the storm-canvas and ringtail evolutions if the existing classes do not cover them, `freesail/crew/model.py` for the sail-room line in `muster`, `tests/test_canvas.py`)

Spec 3b §6.

- **Canvas numbers** per sail by the rule in the research notes §4, `canvas_no` in the ship file with the source comment; **cloth ratings derived** from Luce App. E so that No. 2 canvas gives exactly the present ratings (state the constant and show the identity in a test) and lighter numbers scale by the crosswise strength.
- **Condition and wear** per §6.2, constants named; the effective rating and the baggy-luff term; nothing repairs.
- **The sail room** per §6.3: the schema (a list under `crew.stores.sails`, each with kind, `canvas_no`, `condition`; keep `spare_sails` as a derived count for anything that reads it), the frigate's and schooner's contents from Luce's allowance, `shift`/`bend` choosing the best spare or the one named, the unbent sail returning with its condition, `muster`'s line and the `the sail room` query (report the console wiring you need if it is outside your files).
- **Storm canvas** as parts with gear on both ships per §6.4, and the **ringtail, water sail and save-alls** on the frigate as studding-class sails with theirs, each with a source or judgement comment; the evolutions they need through the existing classes where possible (a storm staysail is a jib-headed sail; a ringtail is a studding sail whose "yard" is the spanker gaff), new files only where not.
- Regenerate both ship files; the generator test must pass; **apply package 21's generator patch if it has landed before you finish** (the brace limits and bowlines), else say so and the lead applies it.
- Tests: the derivation identity; wear rates and the effective rating; a worn sail blowing out before its spar in the M2 gale scenario and a new one not (the mechanism behind truth 27); the sail room's contents and `shift` choosing; the new parts load and set; determinism.

## Package 23: studding sails through the physics, booms, the view (`data/sail_classes.yaml` for the studding class's stall, `freesail/physics/sails.py` for reading it and flogging, `freesail/ship/parts.py` for the boom default, `tools/gen_ships.py` for writing the boom state (coordinate: package 22 has landed), `data/evolutions/set_studding.yaml`, `rig_out_studdingsail_boom.yaml`, `freesail/evolutions/scripts.py` for the tack and wear scripts' first step, `freesail/orders/verbs.py` for the two boom refusals, `client/projection.js`, `client/shipview.js`, `tests/test_studding.py`, `tests/test_view_geometry.py` or equivalent)

Spec 3b §7 and §8. Starts when 21 and 22 have landed.

- **The stall** per level with Luce cited; flogging and strain through the existing model; **no refusal** for setting studding sails on a wind.
- **Booms:** default rigged in, the generator writes it; the two refusals named in §7 and no others; the tack and wear scripts' first all-hands work takes studding sails in and booms in, with Luce's order words; the gate M3 item 4 scenario retold with topgallants in the primer (one sentence; package 24 owns the primer's new section but this correction is yours).
- **The view:** goose-winging true, the fixed scale, the draw order, faint bowlines when hauled. Nothing else in the client.
- Tests: the stall curve and flogging at six points, drawing at nine (the mechanism behind truths 29 and 30); the refusals' wording; the projection's goose-wing shape and fixed scale as pure functions if `projection.js` allows, else a Python test of the ship-graph fields they read; determinism.

## Package 24: truths, notes, primer and gate (`tests/test_known_truths.py` truths 24 to 33, `docs/dev/TuningNotes.md`, `docs/primer/04-trimming.md` (a section on pointing, bowlines and catharpins) and `03-*.md` (canvas, the sail room, storm canvas, the ringtail and kin), `docs/gates/gate-m3b.md`, `README.md`)

Spec 3b §9 and §10. Starts last.

- Truths 24 to 33 in the existing style, values to `TuningNotes.md`; where a truth's range cannot be met without a constant you do not own, report the value and the constant and do not change it.
- The primer sections, every order in a tested block.
- `docs/gates/gate-m3b.md`: short, about ten items per §10, expected numbers from your own seed-7 runs, verdict pending, `py` where the owner types Python, the exact final test count.
- The whole suite; the summary line in the report and the gate.

## Integration (the lead)

The lead applies package 21's generator patch if 22 has not, merges each wave, runs the full suite between waves, reconciles the ship files after 21, 22 and 23 have each touched them through the generator, and writes the decisions log entries.
