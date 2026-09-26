# Milestone 3 work packages: contracts between them

Milestone 3 is specified in `docs/TechnicalSpec-M3.md`; read it whole before your section here, then the parts of `docs/TechnicalSpec-M0-M2.md` it points to (§3 tick and determinism, §6 ship file format, §8 Orders, §8.4 the runner). The code on the branch you are given is milestone 2 as passed at its gate: `freesail/evolutions/runner.py` runs twenty evolutions with fixed durations times a weather factor; `freesail/api/session.py` composes the systems; `freesail/core/clock.py` already strikes bells and names the watch.

## Working rules for this milestone

These are tighter than milestones 1 and 2 on purpose. Each package is one seam of the design; the value of the milestone is in the seams being clean, not in any package being clever.

- **Stay inside your files.** Each package lists the files it owns. Do not edit a file you do not own; if you need a change there, write the exact change you need in your report and the lead makes it at integration. The one exception is a new test file, which you may always add.
- **Build what the specification says, at the size it says.** Where the spec gives a number, use it and name the constant. Where you believe the spec is wrong, say so in your report and build it as specified unless it cannot work; then build the smallest thing that does and say why.
- **No new dependencies.** Python 3.11, the standard library, and what `pyproject.toml` already lists.
- **Determinism.** No randomness outside a named stream from `core/rng.py` handed to you; the crew draws only at muster. Iterate dicts and sets in a fixed order when the order reaches the log or the state.
- **Log voice.** Ship's-log sentences, period words, no jargon from the code. Look at the existing evolution files' `log:` lines and match them.
- **Do not retune milestone 2.** Sail curves, hull constants, ship particulars and the twenty existing evolutions' durations are frozen. The compatibility rule (spec §1) is a test, and it must pass with your work in.
- **Before you finish:** `ruff check .`, `ruff format .`, and the full `python -m pytest` clean (the suite takes two to three minutes; run it whole, and read the summary line, do not pipe it through anything that can hide a failure). Commit in your worktree with the attribution lines you were given.
- **Report** at the end, in this order: what you built; the exact commands to see it work on both ships; assumptions and judgements; the changes you need in files you do not own, as diffs or exact sentences; what the owner should check at the gate. Keep it to a page.

## Waves and dependencies

```
wave 1:  16 crew data and model          19 catalogue to forty
wave 2:  17 hands and the crew factor    18 the watch routine
wave 3:  20 orders, queries, client, gate report, truths 18 to 23
```

Wave 2 begins when 16 has landed on the branch (17 and 18 both import `crew/model.py`). 19 is independent of 16 and edits none of the same files. 20 begins when everything else has landed.

## Package 16: crew data and model (`freesail/crew/model.py`, `crew/muster.py`, `crew/bill.py`, `data/crew/names.yaml`, `ship/schema.py` crew section, `tools/gen_ships.py`, `data/ships/*.yaml`, `tests/test_crew_model.py`)

Spec §2.

- `schema.py`: `CrewSpec` (complement, names, stations, ratings, posts, stores) parsed from the ship file's optional `crew:` key with the validation the spec describes (stations plus posts equal the complement; ratings sum to one; known station names). `ShipSpec.crew: CrewSpec | None`. Loading a file without the key gives `None` and no warning.
- `tools/gen_ships.py`: write the `crew:` sections for both ships with the numbers in spec §2.3 (stations, ratings, posts, `idlers_by_trade`, `stores`), each number commented with its source or "judgement" like every other number in the file; regenerate both files; `tests/test_ship_particulars.py`'s generator test must still pass (it compares text).
- `data/crew/names.yaml`: two lists, `english` and `american`, of at least sixty given names and two hundred surnames each, period-plausible for 1795 to 1815 (parish-register names, not modern ones; a few Welsh, Scots and Irish among the English list; a few Dutch and German among the American, which was a Baltimore crew). Given names may be abbreviated as a muster book would ("Wm.", "Jno.", "Thos.") at the muster's discretion, deterministically.
- `crew/model.py`: the dataclasses in spec §2.1 with the enums, including `trade` (idlers are mustered by trade from `idlers_by_trade`; seamen have none) and `post`; `Crew` holds `sailors: list[Sailor]` in id order, `by_station`, `by_watch`, `posts`, `all_hands_called: bool`, `on_deck(clock) -> list[Sailor]` delegating to `bill.py`, and `describe()` for `muster` (spec §5.1) as lines of text.
- `crew/muster.py`: `muster(spec: CrewSpec, stream) -> Crew`. Ratings are assigned to stations in the order spec §2.3 gives (topmen from able and ordinary first, waisters from landsmen first); skills from rating with a seeded spread of ±0.05; watches split each station evenly, odd one to starboard; posts named from the list unless the file names them. The same stream state gives the same crew, byte for byte in `describe()`.
- `crew/bill.py`: who is on deck at a given clock: the watch on duty (`units.watch_of`), idlers by day per spec §4.1, everyone when `all_hands_called`. Pure functions of the clock and the crew's flags; no side effects; the routine (package 18) will call and set.
- Tests: schema validation errors in words; both ships muster to their complement with the stated station counts; determinism of `muster`; `on_deck` through a full day including the dog watches and the idlers' hours; `describe()` output for the frigate as a golden text the owner can read.

## Package 17: hands and the crew factor (`freesail/crew/hands.py`, `freesail/evolutions/runner.py`, `freesail/evolutions/registry.py` for the `aloft` step flag, `tests/test_hands.py`, the compatibility test)

Spec §3. Begins when 16 has landed.

- `crew/hands.py`: `request(crew, inst_id, want: CrewRequest, subject_mast: str | None) -> Assignment` and `release(crew, inst_id)`; `CrewRequest` parsed from the evolution file's `crew:` mapping (hands int or "all", rating, stations list with `topmen` and `all hands` resolved as spec §3.1); `crew_factor(assignment, want, aloft: bool) -> float` per spec §3.3 with the constants named at module top (`FATIGUE_WEIGHT = 0.5`, the reference skills). Allocation in id order.
- `runner.py`: request hands in `_begin` and release in `_complete` and `_fail`; the three outcomes of spec §3.2 (enough, short but workable with its routine log line, too few with `waiting_for = "hands"` and its notable line once); the crew factor multiplied into the rate in `_tick_steps` and passed to scripts with the weather factor; the pause and resume of spec §3.4 (`Instance.paused`, the belay line once, resume when hands can be had again); `in_progress()` reporting `paused` and `waiting_for`. All-hands evolutions call `routine.call_all_hands` and, when they end, `routine.pipe_down` unless the captain called all hands (read `crew.all_hands_called_by_order`, a flag package 18 sets). If `ship.extra` has no `"crew"`, every request is satisfied and the factor is 1.0: the milestone 2 behaviour, exactly.
- `registry.py`: parse an optional `aloft: bool` on steps (default false). Nothing else.
- Tests: allocation preference order and determinism; the three short-handed outcomes on the schooner; the factor's values for the rating table; pause and resume across a tack; **the compatibility test**: every one of the twenty milestone 2 evolutions run alone on the crewed frigate with the watch on deck finishes on the same tick as on the uncrewed frigate.

## Package 18: the watch routine (`freesail/crew/routine.py`, the `crew` hook in `freesail/core/world.py` tick, `tests/test_routine.py`)

Spec §4. Begins when 16 has landed. Runs in parallel with 17; you share `crew/model.py`'s fields and nothing else, and you do not edit `runner.py`.

- `crew/routine.py`: `Routine(crew, clock)` with `tick(ship, dt) -> list[note]` producing the log notes the World records (the same 3- or 5-tuple shape `ship.step` yields); watch changes with the relief line and the rule that hands at work finish first; idlers up and down; `call_all_hands(reason)` with the staged arrival over `ALL_HANDS_DELAY_S = 90` and its notable line; `pipe_down()`; `all_hands_called_by_order` set only by the order path; fatigue and rest per the table in spec §4.3 with every rate a named constant, applied per tick as rate × dt / 3600. Who is "at work" is any sailor whose `at` is set (package 17 sets it; before 17 lands, nobody is, and your tests set it by hand).
- `world.py`: one call per tick, after `ship.step` and before the bells, if the ship carries a routine (`ship.extra.get("routine")`), recording its notes. Nothing else in `world.py`.
- Tests: a day's watch changes in the log with the dog watches right; idlers' hours; the arrival curve of all hands; fatigue after a quiet night versus three all-hands calls in the middle watch (the numbers behind truth 20); determinism.

## Package 19: the catalogue to forty (`data/evolutions/*.yaml`, `freesail/evolutions/scripts.py`, `freesail/ship/parts.py` for the two new sail states and the boom's rigged-out flag, `freesail/physics/sails.py` for `GOOSE_WINGED` only, `data/vocabulary.yaml` and `freesail/orders/verbs.py` for the verbs your files need, `docs/primer/03-*.md` and `05-*.md` sentences, `tests/test_evolutions.py`)

Spec §6. Independent; starts in wave 1.

- Every **existing** file: check its `crew:` hands and stations against Luce 1884 ch. XX and the relevant evolution chapter, correct them with a comment naming the passage, and add `aloft: true` to the steps that are aloft. Do not change any `duration_s`.
- The **new** files in the spec's table, each with `crew:`, `aloft:` flags, preconditions and requires in the existing style, a source line, and log lines in the log's voice. Read the corresponding Luce passage before writing each one (`grep -n -i` the OCR texts under `docs/references/`); where Luce's sequence is longer than the game's states can express, compress it and say so in the file's header comment.
- `parts.py`: `SailState.UNBENT` and `SailState.GOOSE_WINGED`; `Spar.rigged_out: bool` for studding sail booms (default true so that milestone 2 behaviour holds until the split lands; the `set_studding` file then requires it and `rig_in` clears it). `sails.py`: `GOOSE_WINGED` gives half the effective area and shifts the centre a quarter of the yard's length to the set side; nothing else in the physics.
- Scripts (`boxhaul`, `lie_a_try`, `scud`, `back_and_fill`): follow the `Script` contract in `scripts.py` exactly (timings from the file's `timing:` block, `status` and `reason`, `holds()`, `data()`); watch the compass, do not touch the physics.
- Verbs: `send down`, `sway up`, `strike`, `fid`, `rig out`, `rig in`, `bend`, `unbend`, `shift`, `goose-wing`, `box haul`, `lie a-try`, `scud`, `back and fill`, `loose ... to dry`, `furl all`; in `vocabulary.yaml` first and in `verbs.py` only as far as the existing `_sail_evolution` and `_ship_evolution` paths need. The crew orders (`call all hands`, `pipe down`, `muster`, `send the ... watch`) are package 20's; leave them.
- Tests: every file loads; each new evolution runs on the ship that has the parts and leaves the states the spec says; `shift_sail` consumes a spare sail and refuses when there are none; the gale of gate M2 item 9 with `send down the topgallant masts` ordered at once loses nothing (the mechanism behind truth 23; package 20 writes the truth itself). Primer sentences for chapters 3 and 5 so that `tests/test_primer.py` exercises the new verbs.

## Package 20: orders, queries, client, truths and the gate (`freesail/orders/*` for the crew orders, `freesail/api/queries.py`, `freesail/core/world.py` `summary_lines`, `freesail/ui/console.py`, `client/instruments.js` and `client/app.js`, `docs/primer/06-*.md`, `tests/test_known_truths.py` truths 18 to 23, `docs/dev/TuningNotes.md`, `docs/gates/gate-m3.md`)

Spec §5, §7, §8. Begins when 16 to 19 have landed.

- The orders in spec §5.1 with their errors, through the existing grammar as modifiers (`with the starboard watch`, `send the fore topmen to`), and `muster` as a query that prints `Crew.describe()`. Completion (`orders/complete.py`) learns the new nouns (watches, stations) and verbs.
- `summary_lines` and `snapshot` per spec §5.2; the client shows the watch on deck and hands at work in the instrument panel, and nothing else new.
- Truths 18 to 23 as tests in the style of the existing ones (scenario through `make_world`, orders through the language, a measured value asserted within a range), and the measured values recorded in `TuningNotes.md`. Where a truth's range cannot be met without changing a constant owned by 17 or 18, do not change it: report the value and the constant, and the lead decides.
- Primer chapter 6 gains the watch, the muster, all hands and piping down, in the chapter's voice, every order in a tested block.
- `docs/gates/gate-m3.md` in the form of `gate-m2.md`: headline claims, setup, a checklist of about fifteen items across the two ships following spec §8 with fresh expected numbers from your own seed-7 runs, guide, not-in-this-milestone, what to report. Say `py` where the owner types Python.

## Integration (the lead)

The lead owns `freesail/api/session.py` (attaching muster and routine per spec §2.4), merges each wave, runs the full suite between waves, and makes the cross-file changes the reports ask for. Conflicts between 17 and 18 on `crew/model.py` are not expected; if one needs a field the other adds, it goes through the lead.
