# CR1: Code review of the hotfix session's director-side changes (B→H)

## Scope

- **What was reviewed.** The hotfix session's director-side changes, B (`871e819`, rules 4330be741d1580ee) to H (rules 372c899e355594fa now; d89d1d7362914b8c and bd09b91e0ab871bc along the way):
  - **The aboard table widened.** Built 2026-10-20 00:06–00:28 UTC (transcript time); the table grew from 4 things to 22.
  - **The repair effects.** Built 2026-10-21 04:38–04:42 UTC; `leak_stopped` and `well_pumped` took the table to 24.
  - **The well reading.** `api/readings.py` and `agents/tools.py`.
  - **The scenarios.** Four, drafted 2026-10-20 01:11–01:27 UTC, with budgets set to 9999/9999 at 01:27.
- **Who wrote it.** Claude Code session "Sailing game scenario design" (Opus 5.5), which was also the director of the Western Islands run.
- **Files read.**
  - `work/diffs/hotfix-code.patch`: the hunks for `aboard.yaml`, the nobudget brief, `tools.py`, `readings.py`, `orders.py`, `places.py`, `ports.py`, `reckoning.py`, `sights.py`, `test_aboard_found.py`, `test_director.py` and `test_readings.py`, plus `test_ground.py`'s repair test.
  - `hotfix-docs.patch` (all), `hotfix-tuningnotes.patch` (all), and `github-pkg66.patch` for `orders.py`, `readings.py`, `tools.py`, `director.py` and `test_director.py`.
  - The full H files around each change: `world/orders.py` §aboard, `world/ground.py` (1–330), `world/sights.py` Chronometer, `ship/parts.py` (anchors, cordage), `physics/anchor.py` (cable parting), `physics/strain.py`, `agents/director.py` (`limit_of`, `_enemy_heavier`, `DIRECTOR_BRIEF`) and `world/scenarios.py` (docstring, `_stations`).
  - The merged tree's `orders.py`, `readings.py`, `tools.py`, `director.py` and `test_director.py`, diffed against H and G.
  - `work/chunks/director-1.md` in full; `director-6.md` for the grounding, the repair and the pin attribution (lines 1–420 and 2150–2460).
  - Spec M7b §3, §4, §17a, §19 and §20 (G).
  - The four scenarios in `%APPDATA%\FreeSail\scenarios` and `interesting-passage-nobudget.yaml`.
- **Nothing run.** No tests and no game; every behavioural claim below is from reading the code, and says so where it is an inference.

## Narrative

- 10-19 04:57: the owner asks for more things the director can find aboard. The session finds the four effects hard-coded in `_aboard_found`, and only the first `plausible_when` key read. It finds three bugs: foul water never clears; the foul doubt counts from the voyage start; report-only things all blame "the hull". It proposes data-only additions and new code effects (04:59).
- 10-19 05:07 to 22:41: the session snapshots the folder. The owner swaps in B (53b landed). The session diffs and confirms the aboard code is untouched by 53b, and notes that commas in forms would collide with 53b's thing path.
- 10-20 00:06: the owner says go ("back up files first, add tests, and run the relevant tests"). The session backs up each file before editing.
- 00:09–00:13, the code:
  - `Stores.watered_tick`, `Hold.losses`/`lose`, and the yard's water clearing `foul`;
  - `Chronometer.stopped`, cleared on `wind the chronometer`, and `GLASS_BROKEN_WORDS`;
  - in `orders.py`: slots (`SLOTS`, `_part_by_name`, `_anchor_by_name`, `_good_by_name`), an effect table (`_ABOARD_EFFECTS`), a lacks table (`_ABOARD_LACKS`), a plausibility table (`_PLAUSIBLE`, every condition held together), and checks at load for unknown keys and slots.
- 00:14–00:15: `aboard.yaml` rewritten with 22 things. A smoke test finds a plural bug ("1 tons"), fixed with `places._tons`.
- 00:17–00:19: `tests/test_aboard_found.py`, 10 tests. Two failures were the tests' own mistakes, fixed: a missing cable form, and cargo stowed outside the scenario breaking a replay.
- 00:19–00:27: the fast tier passes apart from the starter-briefs test, which the owner's `interesting-passage-nobudget.yaml` breaks.
- 00:48–01:08: nine slow-tier pin failures. The session proves them pre-existing by re-running them on a "pristine-new" copy with its backups restored. Good practice.
- 01:11–01:16: four scenarios drafted, each with its brief inline. A `prove.py` mimics the harbour's prove and checks every brief example parses.
- 01:27: the owner asks for 9999 budgets: "increase the budgets for samples a day and actions a day to 9999" (01:27:01). All four are changed, reloaded and checked.
- 10-21 04:30–04:35: after the grounding at Horta the owner says "if I weren't the developer, I would have just hard rage quit there" (04:33:34). Then: "I don't think repairing is implemented at all" (04:35:50).
- 04:36–04:37: the session reads `ground.py`. It sees the leak runs only while aground and the well's water moves nothing, and proposes `leak stopped` and `well pumped out`. The owner approves at 04:38:06.
- 04:38–04:42: two effects, two conditions (`leaking`, `well_above`), two table entries, a `test_ground.py` test with a replay, and updates to the primer and the tuning notes.
- Later on 10-21: the well becomes a reading, and the starter book loses `sound the well`. The tuning notes then put the pre-existing pin failures down to "the 2026-10-19 evening changes ... (package 65's era)" (director-6 L2205, L2431). That is wrong; see F2.

## Findings

| ID | Category | Severity | What | Evidence (timestamp/tick, ≤15-word quote) | Spec/design ref | Recommendation | Status in G / H (if known) |
|---|---|---|---|---|---|---|---|
| F1 | bug | med | **`enemy_heaviest: brig` refuses nothing.** `_enemy_heavier` finds the limit as the first `SIZE_RANK` key that is a substring of the brief's word. The keys are `frigate`, `brig-sloop`, `merchant brig`, `schooner`, `cutter`, `lugger` and `smack`, and none is inside "brig", so the limit is None and the order is allowed. A French frigate passes a "no heavier than a brig" brief. This was already in B (package 50), not the hotfix's doing. It touches the Western Islands run and the starters chase, dispatches and interesting-passage. Only "cutter" is tested. | `director.py` L389: `limit = next((k for k in SIZE_RANK if k in heaviest.lower()), None)`; G identical | §4: "its limits are enforced by the channel, not trusted to the model" | Rank the limit the way `captains._SIZE_WORDS` ranks words (it has `("brig", 2)`). Add a test per starter's limit. | Present in B, H and G |
| F2 | docs | med | **The tuning notes blame the failing pins on the wrong change.** They say the failures are "Likely the 2026-10-19 evening changes to `ports.py`, `reckoning.py`, `places.py` and `sights.py` (package 65's era)". Those mtimes (10-19 20:09/20:10 local, UTC−4) are the session's own aboard-widening edits, made 10-20 00:09:23–00:09:56 UTC. Package 65 is briefed, not built. And the session's own 10-20 run on the pristine copy already showed the same failures without those edits ([57, 100918] on both trees). The "Re-pin the known truths" session card (director-6 L2435) sends the lead after the same wrong cause. | director-6 10:32:12 listing "2026-10-19 20:09 freesail/world/places.py"; director-1 00:09:23 Edit places.py | TuningNotes, H's §"The well, sounded" | Correct the paragraph: the failures were present in B (53b's merge or this machine) and are independent of the hotfix. Drop the "package 65" lead from the re-pin brief. | H only |
| F3 | design-gap | med | **The director's station brief still shows only the old four things.** `DIRECTOR_BRIEF` lists sprung, stove, seam and foul only. A director coming in cold won't see the 20 new things, among them the leak and the well, unless a refusal's long list of forms or the primer shows them. In the run the director knew them because it had written them. | merged `director.py` L500–502: "'aboard: a cask found stove', 'aboard: a seam found working'" | §3: the forms are examples, not a rule | Add two or three new examples to the brief, e.g. `the leak stopped`, `the bread found damp`, `the chronometer found stopped`. | H and G |
| F4 | realism | med | **The leak and the well are fixed instantly.** `leak_stopped` and `well_pumped` set `leak_m_per_h = 0` and `water_in_well_m = 0` at once: no time, no hands, no fatigue. `leak_stopped` is accepted even while she lies on a rock with her planks stove (`leaking` is the only condition). The owner accepted this as a hotfix until M8, but it is a variable set by fiat. | orders.py `_fx_leak_stopped`, `_fx_well_pumped`; table: "plausible_when: {leaking: true}" | §3 decision 50 (plausible causes); §17a "transactions, not variables" | Keep as a labelled hotfix (it is labelled in the table, the primer, `ground.py` and the tuning notes). Doubt `leak_stopped` while `grounded.rock`. M8 should replace both with pump and carpenter work over time. | H |
| F5 | UX | low | **The master's report says what the game has not done.** It says the master "has it wound and will set it going by the account". The effect leaves the chronometer dead until someone orders `wind the chronometer`, so a captain reading the report may never give the order. | aboard.yaml `chronometer_stopped` report; `Chronometer.tick` never auto-winds one that is stopped | — | Reword: "he asks leave to wind it and set it going by the account". | H |
| F6 | bug | low | **`at_anchor` ignores which anchor is named.** "The best bower cable found chafed" is plausible whenever any anchor is down, the kedge included. The doubt it then skips says "a cable stowed in the tier does not chafe". | `_plausible_at_anchor` takes `target` and never reads it | §3 doubt | When the thing's slot is `{anchor}`, check that anchor's `down`. | H |
| F7 | bug | low | **The provisions doubts count from the voyage start.** `bread_spoiled` (`days_out: 7`) and `meat_rotten` (`days_out: 10`) say "she was victualled within the week", but they count from the start, not from the last victualling. The session fixed exactly this for water and not for provisions. | aboard.yaml: "doubt: she was victualled within the week" | §19 | Add `victualled_tick` set by the yard's provisions, and a `days_since_victualled` condition. | H |
| F8 | bug | low | **The well's word goes stale after pumping.** `well_pumped` leaves `ship.extra["well_sounded"]` as it was, so `the well` still reads the last sounding (say four feet) after "the well is dry". `casks_leaking` says "a good part of the water is in the well" and the well doesn't move. | `_fx_well_pumped`; readings `_well` reads `well_sounded` | — | Have `well_pumped` write a dry sounding. Reword the cooper's line, or raise the well a little. | H |
| F9 | spec-deviation | low | **`leaking` stays true after she floats.** `_afloat` never clears `leak_m_per_h`, and `_leak` runs only while aground. After she floats she gains no water, yet `leaking: true` holds. The docstring "making water from a grounding" overstates it. Harmless for the story. | ground.py `_afloat`, `tick` L193–194 | — | Note it in the docstring, or read `ground.aground`, and decide in M8. | H |
| F10 | harness | low | **The well reading comes into every sample.** `well` is now a present row, so `readings_words` carries "the well not sounded yet: 'sound the well' has the carpenter sound it" in every first sample, for every station on every ship. It is a nudge to sound a dry well. | tools.py `readings_words` skips only absent and driver rows; primer 06 now shows it | — | Carry `well` only once she has taken the ground or the well has been sounded (`none_words` returning None). Check that no G sample pins move after the merge. | H and merged |
| F11 | code | low | **`orders.py` writes `Ground`'s private fields.** `_fx_well_pumped` sets `ground._feet_said` and `_waterlogged_said`. | orders.py `_fx_well_pumped` | — | Add a `Ground.pumped_out()` method, as the module's own API. | H |
| F12 | bug | low | **`harm` isn't checked at load.** The session's new load checks refuse unknown `effect` and `plausible_when` keys, but not an unknown `harm` value. A typo like "deadley" would get past `nobody_dies`. | aboard_table validation | §4 "nothing found aboard that would kill" | Check `harm` ∈ {none, hurt, deadly} at load. | H |
| F13 | UX | low | **Doubt first, lack second.** The doubt is checked before the lacks. A director is first told "nothing has jarred the chronometer". Re-entered with a reason, it is then told "she carries no chronometer" and "Logged as attempted ... for whoever builds the next forms". That is wrong for "stopped already". | `director.direct` (doubt) then `_aboard_found` (lacks) | §3 "no way as said" | Check the lacks inside the doubt. Answer "already" cases as plain refusals of the state, not as attempted forms. | H |
| F14 | order-language | low | **Slot names must be written exactly.** Slots match only the exact display or family name. "the best bower's cable", "the fore-topsail" and the vocabulary's contractions fail, with a 24-form list in reply. A `{good}` not in the hold gets the same list, with no hint that the hold must have it. | `_part_by_name`, `_anchor_by_name`; test: "the brandy found wet", refused | — | Pass the slot through the resolver's variants and accept the possessive. Say "she has no brandy in the hold". | H |
| F15 | realism | low | **Any water clears the foul.** Taking in any quantity clears `foul` for the whole tier, and the line says "the foul water started overboard" while `water_tons` only grows by the new quantity. Fine with the default fill-up, wrong for `take in water 2 tons`. | ports.py yard job | §19 | Clear `foul` only on a fill-up, or set the tons to the new water. | H |
| F16 | docs | low | **The docs lag the code.** Spec §3's as-built paragraph still has four things and "five days out". Primer 20's doubt table omits the leak and the well. `aboard.yaml`'s "carries away, or a sail bears, the less" reads backwards; it means *sooner*. | spec L208–227; hotfix-docs 20-the-director L84 | §3 | Fold the widening into §3's as-built and fix the wording. | H; G lacks the widening entirely |
| F17 | test | low | **Test gaps.** The counts are hard pins (24 in two files). No tests for: `at_anchor` against the named anchor; the `provisions_days`, `cargo_tons` and `water_tons` texts; the lacks for spare canvas, cordage and stores; `harm`; `leaking` after floating off; the well reading after pumping. The starter-brief test now requires `nobody_dies` of every brief in the folder, the owner's own included. | test_aboard_found.py; test_director.py L335 | — | Add the cases. Count with `>=`, or name the ids. Exempt the owner's briefs from `nobody_dies`. | H |
| F18 | docs | low | **The nobudget brief contradicts itself.** `interesting-passage-nobudget.yaml` has `wind_max_kn: 45` with the comment "nothing above force 7", and `frigate-36` with "no enemy heavier than a brig". Its header and challenge say "a gale is not". It keeps the starter's name "An interesting passage". It is the owner's file, not the session's (11:06 on 10-19), and the merge adds it to the repo's starters. | diff vs interesting-passage.yaml | §4 | The owner chooses the values; then align the comments and the prose, and rename it. | H, merged |
| F19 | realism | low | **The inshore squadron starts heading toward Ushant.** The frigate starts at 48°20'N 5°05'W, heading 000 at 4 knots under plain sail, some 6–7 miles south of Ushant's rocks (an inference from positions). The prove script also showed the intent's rules captain taking her at tick 300 ("investigating a stranger", a tack, missed stays) before any player order. | director-1 01:15:11 prove output | — | Start her heading 200 or 270, as the Ushant trial does, or further west. Say in the file that the rules captain acts until the player's first order. | Scenario file |
| F20 | design-gap | low | **`enemy_heaviest: cutter` is empty for a neutral.** Under Danish colours no nation is at war with her in June 1805, so the limit never applies in free trade. The revenue cutter is the brief's design. | `_enemy_heavier` returns None when not at war | §4 | Accept as is, or let the limit read "any warship". | Scenario file |

## Per-change table

| File | What changed | Verdict | Reason |
|---|---|---|---|
| `data/director/aboard.yaml` (widening) | 18 things added (spars, sails, lines, cable, water and provisions shares, cargo, spare gear, chronometer, glass, report-only), the header documented field by field, a note that the table is "what the game can do, never the list of what the director may say", every `harm: none` | sound with notes | Sources cited, figures marked as judgement, matches §3 and §4. F5, F6, F7, F8 and F16 wording. |
| `aboard.yaml` (repair) | `leak_stopped`, `well_pumped` with `leaking` and `well_above` | sound with notes | Clearly labelled a hotfix until M8. F4. |
| `orders.py` load checks | Unknown effect or plausible key, one slot per thing, slot-bound effects need the slot in every form | sound | Good fail-fast. `harm` not checked (F12). |
| `orders.py` slots and matching | `_key`, `_part_by_name` (display name, then family), `_anchor_by_name`, `_good_by_name`, `SLOTS`, `_SLOT`, `_aboard_match` generalised | sound with notes | Correct; deterministic order; the frigate test proves each form finds its own thing. Exact-name only (F14). `_fill` passes the name as an `re.sub` replacement string (a backslash in a name would be read; very unlikely). |
| `orders.py` `_aboard_found` | All lacks checked before any change, then each effect in turn, report-only `unmodelled` words | sound | Atomic, honest refusals. F13 ordering. |
| `orders.py` effects | Condition cuts (only ever lowered), cable, water and provisions tons and shares, cargo struck off with its cause in `Hold.lose`, spare sails and cordage, chronometer, glass | sound with notes | Effects match how the model reads condition: sails lose effective cloth, spars, lines and the cable lose endurance under overload. Clamped and replayable. F5 report mismatch. |
| `orders.py` `_fx_leak_stopped`, `_fx_well_pumped`, `_lacks_hull` | Zero the leak rate and the well, reset the carpenter's counters | sound with notes | Works, and the test proves a replay. F4, F8, F9 and F11. |
| `orders.py` `_doubt_aboard` and `_PLAUSIBLE` | Every condition held together; new `days_since_watered`, `wind_above`, `at_anchor`, `leaking`, `well_above` | sound with notes | Fixes the only-the-first-key bug. F6, F7, F9. |
| `places.py` | `Hold.losses` and `lose`, losses in the manifest's lines; `Stores.watered_tick` (a class default) | sound | Fits §17a's "with its cause in the ledger"; safe on a checkpoint from before. |
| `ports.py` | The yard's water clears `foul` with a line, and stamps `watered_tick` | sound with notes | Fixes a real gap; §19 implies watering sweetens. F15. |
| `reckoning.py` | `wind_chronometer` clears `stopped` | sound | Matches how a run-down chronometer restarts. |
| `sights.py` | `Chronometer.stopped` (a class default); the reading says why it is dead | sound | Minimal, safe on a checkpoint. `to_dict` omits it, which is harmless. |
| `api/readings.py` | `GLASS_BROKEN_WORDS`; the well becomes a reading (`_well`, `none_words`, kind `well`, words-only description) | sound with notes | Correct and replayable. F10, noise in samples. |
| `agents/tools.py` | The "Not yet in the ship" line only when a row is absent; the well's held note removed | sound | Follows from the well reading; no conflict with package 66. |
| `tests/test_aboard_found.py` | 10 tests: matching, load errors, effects, report-only, chronometer, glass with replay, all conditions held, watering, replay | sound with notes | Good coverage of the happy paths and replays. F17 gaps. |
| `tests/test_director.py` | Table count 24; starter briefs as a subset, each brief checked | sound with notes | Needed for the owner's brief. F17 on `nobody_dies`. |
| `tests/test_readings.py` | The absent-rows test generalised; the well present, None before a sounding | sound | — |
| Primer 20 | Example list widened; doubt table rewritten | sound with notes | F16: leak and well missing from the doubt table. |
| Primer 14 | Kedge aground cross-referenced to chapter 13 | sound with notes | Says `weigh` takes it up, but weighing a kedge aground is still refused (the session's own open item). |
| TuningNotes (four sections) | House style, pins reported with old and new values, open items for the lead | problem (one paragraph) | F2's misattribution; the rest is careful and accurate. |
| Scenarios (4) | Western Islands, inshore squadron, free trade, Lisbon letter, each with its brief inline | sound with notes | Valid against the loader (keys, station holders, things' where-forms, port mappings, letters). Every example parses and every first order is accepted (the session's prove). 9999/9999 in all four, as the owner asked. F1, F19, F20. |
| `interesting-passage-nobudget.yaml` | The owner's copy at 9999 | sound with notes | F18. |

**Package 66 (G) against the merged result.** The textual merges in `orders.py`, `readings.py`, `tools.py` and `test_director.py` touch disjoint code:

| File | Package 66's change | The hotfix's change |
|---|---|---|
| `orders.py` | `say as` voices, ashore hearers, reach for a `Voice` | the `aboard` section |
| `readings.py` | the station's line at ~3130 | the well row and `describe_value` |
| `tools.py` | `said_tail` and the stand-by text | the standing-dialect page |
| `test_director.py` | tests appended at the end | lines 324 and 335 |

No semantic conflict found:

- `said_tail` acts only on the said kinds.
- G's `director_line` reads the budget, which shows "N of 9999".
- Neither side touched `_enemy_heavier` or the brief's aboard examples (F1, F3).
- One merge risk: the new `well` row in every sample's readings (F10) may move a G test or pin that lists a sample's readings. The coordinator's test run will show whether it does.

## What worked well

- **Careful engineering.** Backups before every edit, and a pristine copy used to prove pre-existing failures. Replay checks for the glass, the cargo and the repair. Ruff lint and format run. The house style of the code, comments and tuning notes matched closely.
- **A sound data-driven design.** Effect, lacks and plausibility tables keyed by the YAML, with errors at load. Matching with slots is general and deterministic. "No way as said" refusals are honest, and nothing changes on a lack.
- **Real bugs fixed.** Water fouled for the voyage; only the first condition read; "nothing of the hull" said of weevils.
- **The table's prose.** It is period-sourced (Falconer, Steel, the Regulations) and keeps decision 46: the people's report, never the order.
- **Honest scope.** The repair is labelled a hotfix everywhere. The tuning notes say what the well does not do (no trim, no handling). Open items are left for the lead.
- **The owner's ask met.** 9999/9999 in every scenario, reloaded to check, and remembered as a default.

## Model behaviour and experience

- **Good judgement on roles.** The session (Opus 5.5) chose the director's seat because it already knew the scenarios' secrets ("for that seat my knowledge is the job", 10-20 01:22:43).
- **Restraint.** It flagged the owner's brief file as "I didn't touch that file". It also asked before each step.
- **Candour with the player after the grounding.** It owned its part: "The wind was my fault" (10-21 04:30:47). It distinguished what the simulation leaves out from realism.
- **Weak spots.**
  - The timezone misreading (F2) became a confident cause in the notes and the session card.
  - It edited the game's rules mid-voyage while also directing that voyage. The owner asked for it, but it blurs director and developer.

## Open questions for the owner

1. Should `interesting-passage-nobudget.yaml` go into the repo as a starter? If so, which values are meant: 45 kn and a frigate, or the comments' force 7 and a brig?
2. Should the repair stay instant until M8? Or should `leak_stopped` be doubted on rock, and pumping take time and hands?
3. Should `the well` show in every sample, or only once she has taken the ground?
4. In the inshore squadron, should the intent's rules captain act before your first order, and should she start heading toward Ushant?
5. Should F1 (the brig limit) be fixed now as a hotfix? It affects the Western Islands run's brief and three starters.
