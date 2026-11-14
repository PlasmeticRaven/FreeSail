# Code reader 07: the evolutions and the crew

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. Read under READERS.md and CODEREADERS.md. Nothing
under docs/dev, docs/design, docs/playtests or docs/gates was opened; the test suite was not run.
Every command below was short. One in-memory experiment (section 1.3) loaded a YAML file from my
scratch directory into the registry's dictionary inside one Python process; no file of the tree was
touched.

## 1. What it is

### 1.1 Size

| Part | Files | Lines |
|---|---|---|
| `freesail/evolutions/` | 9 | 13,512 (`scripts.py` 9,095; `runner.py` 1,659; `repair_scripts.py` 895; `trim.py` 565; `expr.py` 411; `action_scripts.py` 359; `registry.py` 347; `fight_scripts.py` 160; `__init__` 21) |
| `freesail/crew/` | 9 | 3,493 (`health.py` 1,076; `quarters.py` 661; `hands.py` 435; `model.py` 334; `routine.py` 329; `victuals.py` 314; `muster.py` 237; `bill.py` 97; `__init__` 10) |
| `data/evolutions/` | 108 YAML | 3,988, of which 1,851 (46%) are comment lines |
| `data/crew/` | 3 YAML | 252 (`names.yaml` 106, `ration.yaml` 76, `needs.yaml` 70) |
| tests that import either package | 45 of 174 test files | 65,545 lines in those files (the biggest: `test_known_truths.py` 17,391, `test_view_geometry.py` 7,056, `test_indefatigable.py` 2,959, `test_orders.py` 2,877, `test_bellerophon.py` 2,198, `test_bilander.py` 2,119, `test_evolutions.py` 1,937, `test_catalogue.py` 1,013, `test_hands.py` 1,060, `test_routine.py` 560, `test_crew_model.py` 502) |

Code comment lines are 8% and docstrings 13% of the 17,005 lines (tokenizer count). There are 517
references to packages, rulings, gates, playtests or "the lead" in the code and the evolution data,
355 of them "package NN" in the code alone, and eight pointers into `docs/dev/TuningNotes.md`.

### 1.2 How it works

- `registry.py` reads every `data/evolutions/*.yaml` at import into `EVOLUTIONS` (registry.py:364).
  A file gives either `steps:` (a list) or `script:` (the name of a Python class), never both
  (registry.py:276-279).
- `runner.py` `Runner` (one per ship, `ship.extra["evolutions"]`, runner.py:302) is stepped by the
  World each tick before the physics. `start` resolves the subject, checks the class and the
  preconditions, asks `crew/hands.py` for hands, and either begins, queues behind work holding the
  same parts, or waits for hands (runner.py:306-362). Step-list evolutions walk their steps
  (runner.py:837-921); scripted ones call `Script.tick` (runner.py:925-935).
- `expr.py` is a small safe expression language for preconditions and `sets:`/`ramp:`.
- `scripts.py` and the three `*_scripts.py` hold 49 script classes registered in `SCRIPTS`
  (scripts.py:9044-9095), plus about 120 free helpers that read the rig by role and geometry
  (head and after yards, drivers, head sails, courses) which other packages also import (21 imports
  from `orders/`, `world/` and `core/world.py`).
- `crew/model.py` holds `Sailor`, `Crew`, `Rating`, `Station`, `Watch`; `muster.py` draws a company
  from the ship file and a seeded stream; `bill.py` says who is on deck; `routine.py` keeps watch
  changes, all-hands calls and fatigue; `hands.py` fills an evolution's crew line from the deck and
  gives the crew factor; `quarters.py` the quarter bill at action; `health.py` wounds, the surgeon,
  the sick list, burial; `victuals.py` the meals' fall of the stores and the hardship.

What a player sees: every order line about sail, yards, anchors, boats, fishing, repairs and
quarters is said by this part ("Hands aloft to loose the fore topsail", "Not hands enough on deck
to ...", "Only seven hands to ...", "Belayed reefing the mainsail: ...", "Missed stays"), the muster
reading (`Crew.describe`, model.py:253-313), and the health and burial lines.

### 1.3 The claim: is the catalogue data?

Answer: about two fifths of it is, in a narrow sense; the rest is a Python class with its durations
in a YAML file.

- **Count.** 108 evolution files load (command: `python3 -c ... len(registry.EVOLUTIONS)` gave 108).
  44 have `steps:`, 64 name a `script:` (49 distinct classes; `fishing_gear` serves 8 files,
  `trim_sheet` 4, `send_down`/`sway_up` 3 each). The 44 step files hold 112 steps in all, about
  2.5 each.
- **Where the task tree lives.** Ten files read whole: tack, wear, reef_square, furl_square,
  set_square, brace, let_go_anchor, heave_lead, take_lunar, haul_nets. In `tack.yaml` the 85 lines
  are 57 lines of comment, two preconditions, nine timing numbers and three log lines; the
  sequence ("helm's a-lee", "mainsail haul", "let go and haul", the miss, the hang in stays, the
  settee dip, the course to steer) is `TackScript`, scripts.py:1156-1852, 697 lines, whose `tick`
  alone is 178 lines (scripts.py:1470-1648). `wear.yaml` is four numbers and `WearScript` 261 lines.
  For every `PhasedScript` (sending spars down, bending, reeving, repairs, quarters) the phase
  names, their order and what each changes are Python (`start_phases` / `end_phase`,
  scripts.py:3580-3648); the YAML only gives `<phase>_s` durations, read by an f-string
  (scripts.py:3602). 55 timing keys in the YAML are never named in the code as strings because
  they are found that way (script over all data, e.g. `fish_spar.yaml: fishes_s, woold_s`), so a
  reader of the YAML cannot tell which keys are live.
- **No tree.** The step list is linear with an optional `if:` and `instead_of:` (registry.py:116-129).
  There is no parallel or nested task, no per-task hand count or rating: a whole evolution has one
  `crew:` line (e.g. set_square.yaml:64, `{hands: 12, rating: ordinary, stations: [...]}`).
- **Aliases.** No evolution file has an `aliases` key (grep: 0 of 108). The `verb:` field is used
  only to build log words (`_describe`, runner.py:1551-1559; `_check_applies`); no order parser reads
  it (grep for `.verb` on an evolution outside the package: none). The words a player types live
  in `data/vocabulary.yaml` (`verbs:` line 25, `evolutions:` line 1894) for 69 of the ids, and for
  the other 35 only in Python tables or calls in `orders/ground_tackle.py` (e.g. lines 74-83),
  `orders/damage.py`, `orders/work.py`, `orders/fight.py`, `orders/signals.py`, `orders/gunnery.py`,
  `world/fishing.py`, `world/reckoning.py` (list in 2.2).
- **What "can go wrong" is.** For step files, `requires:` and a parted `via:` line fail the work
  (runner.py:849-862); that is all the data can say. Every miss, hang, drag, foul or refusal of the
  64 scripted ones is Python.
- **Experiment: a player's data-only evolution.** I wrote `overhaul_gear.yaml` (a step evolution on
  a square sail, `crew: {hands: 4, rating: able, stations: [topmen]}`) to my scratch directory,
  loaded it with `registry.load_file`, put it in `registry.EVOLUTIONS` in memory, made a frigate
  world (`make_world(7, "data/ships/frigate-36.yaml")`), set the main topsail and called
  `Runner.start`: "Hands aloft to overhaul the main topsail buntlines.", four hands taken, done
  within 120 ticks. `orders.handle(ship, "overhaul the main topsail")` then raised
  `UnknownVerbError`. So a step evolution on an existing class of part, that only assigns existing
  attributes, can be added with two data files (its YAML and entries in `vocabulary.yaml`'s `verbs:`
  and `evolutions:`), and nothing more. Anything with judgement (a manoeuvre, anything that reads the
  wind or the ground, any outcome not a plain attribute assignment) needs Python, and so does any new
  sail class (`SAIL_CLASSES`, ship/schema.py:137) or a new function in the expressions (runner.py:683-710).
  Some lists in Python also name evolution ids and would not know a new one: `HANDING_EVOLUTIONS`
  (scripts.py:570-586), `QUARTERS_OWN` (runner.py:272), `CALLS_HANDS_WHEN_SHORT` (runner.py:150),
  `HELM_MANOEUVRES`, the `get_under_way` special case (runner.py:1480-1485).
- **Source citations.** All 108 have a `source:`; the registry refuses a file without one but checks
  only that the string is not empty (registry.py:268-270), not that it names a chapter. Most cite a
  chapter and a named section or a page (Luce 1866/1884, Lever 1808, Steel 1794, Falconer 1780,
  Holdsworth 1874, Forfait 1788). 22 source lines call some figure "judgement"; 230 uses of
  "judgement" across the files; three cite "from memory", two of them "UNVERIFIED"
  (heave_mark.yaml:10, :25; make_signal.yaml:20, :28; serve_small_arms.yaml:22). Several cite only
  another file's times ("dip_lug's times lengthened (judgement)", dip_settee.yaml; furl_settee.yaml;
  set_settee.yaml; take_in_settee.yaml).

### 1.4 The crew against the proposal's individuals

| Field | Per sailor? | Changes anything a player sees? |
|---|---|---|
| rating | yes (model.py:144) | yes: the crew factor reads the rating's table figure (hands.py:430-434), who goes aloft (hands.py:231-238) |
| skills `skill_aloft`, `skill_deck` | yes, seeded ±0.05 (muster.py:204-206) | `skill_aloft`: **read by nothing** after it is made (grep: only muster.py and world/dealings.py write it). `skill_deck`: not by evolutions (`crew_factor` deliberately reads the rating table, hands.py:408-410), but by gunnery (combat/shot.py:216), boarding (combat/boarding.py:273), the master's reckoning (world/reckoning.py:1994), prizes and people |
| fatigue | yes, 0..1 (model.py:149) | yes but small: crew factor `1 + 0.5 * max(0, mean - 0.05)` (hands.py:425-426), at most 1.475; muster words fresh/tired/worn out (model.py:179-184); also read by guns, oars, pumps, readings |
| morale | **no** per-sailor field; morale is company-level in `combat/morale.py` (not my part) | n/a here |
| health | a word `hurt` plus `wound`, `hurt_until`, `dressed`, `treated`, `hurt_how` (model.py:163-176); `fit` | yes: unfit men leave the deck and the pool (bill.py:309; hands.py:234-237); "hurt" men never aloft |
| watch | yes, starboard/larboard/none (model.py:146) | yes: the bill (bill.py:308-315) decides the pool for every evolution |

Tasks do compete for hands: `hands.request` takes idle fit hands on deck, marks `Sailor.at`, and a
second evolution sees fewer; under half its want it waits, between half and all it goes slower
(hands.py:292-337; runner.py:1135-1184). The competition is per evolution, not per task within one.

## 2. Is it reached?

2.1 Reached from play: `core/world.py` constructs the runner, routine, health, quarters; the runner
is stepped each tick; `orders/*` call `Runner.start`. Health and victuals tick once a minute
(core/world.py:2441-2445, 2516-2533).

2.2 Evolutions only Python can start (not in `vocabulary.yaml`, started by name from Python): 35, e.g.
back_anchor, cat_and_fish_anchor, come_to_anchor, get_under_way, heave_in, heave_short,
lay_out_kedge, let_go_anchor, moor, unmoor, veer_cable, weigh_anchor (orders/ground_tackle.py);
batten_down, cut_away_mast, fish_spar, fother_sail, jury_mast, plug_shot_hole, rig_preventers,
set_up_rigging (orders/damage.py); the eight fishing files (world/fishing.py); heave_lead,
heave_deep_sea_lead (orders/work.py, world/reckoning.py); take_lunar (world/reckoning.py);
make_signal, heave_mark, serve_small_arms, send_boat. Command: a script over the 108 ids, testing
`vocabulary.yaml` with `\bid\b` and the Python tree for the quoted id.

2.3 Dead data:
- `furl_gaff.yaml` and `furl_jibheaded.yaml` are started by nothing in play. `vocabulary.yaml`'s
  `furl:` maps only square, lateen, settee (lines 1917-1920) and its refusal (line 2019) says "A
  {class} sail is not furled on its spar; take it in instead." The only code mention is the
  `HANDING_EVOLUTIONS` list (scripts.py:579-580); tests name them (test_catalogue.py:85-86, 162).
- The other way: `vocabulary.yaml` maps `set: sprit: set_sprit` and `take in: sprit: take_in_sprit`
  (lines 1902, 1914) and neither file exists. No ship file carries a sprit sail today, so it is
  dormant; the first one added gets "There is no such evolution as 'set_sprit'" (runner.py:318).
- `Routine.set_aloft` and `Routine.set_instance_aloft` (routine.py:114-123) are called only by
  `tests/test_routine.py` (lines 329, 330, 359, 446, 448). So `FATIGUE_AT_WORK_ALOFT = 0.10`
  (routine.py:55) never applies in the game: every hand at work, aloft or not, tires at the deck
  rate 0.06 an hour (routine.py:212). The comment at routine.py:107 ("package 17 knows the step")
  promises a wiring that does not exist.
- `Sailor.skill_aloft`: written, never read (table in 1.4).
- `ship.extra["close_hauled_angle"]` is read (scripts.py:204) and set by nothing (grep); every
  ship is taken to be close-hauled at six points true.
- In health.py, `DIE_FLUX_AFTER_D` (95), `PROVISIONS_OUT_LAG_D` (109) and
  `HealthState.provisions_out_since` (167) are declared and never used (grep over freesail and tests).
- Python fallbacks that the YAML always overrides and that disagree with it: in `TackScript.tick`
  `hang_after_s` defaults to 15.0 (scripts.py:1520) where tack.yaml:45 says 5, and
  `steady_timeout_s` to 120.0 (scripts.py:1636) where tack.yaml:60 says 300. Dead while the file
  carries the key; wrong the day a key is misspelt (see 5.2).

## 3. Built more than once

1. **Close-hauled, four times.** `close_hauled_true_angle` 6 points true (scripts.py:202-204);
   `close_hauled_apparent_angle` luff + 5° (runner.py:1635-1640) used by the expression
   `close_hauled()` with a ±10° band (runner.py:653-656); `_by_the_wind_now` luff + 5° + 10°
   one-sided (scripts.py:1131-1136) re-deriving the runner's figure by hand; and
   `orders/verbs.py:966` `"close hauled": 67.5`. They differ today: the expression is two-sided, the
   script's one-sided. Joining: one function in one module, the others calling it.
2. **Two sailor makers.** `muster.muster` (muster.py:161-220) and the recruits in
   `world/dealings.py:2820-2850`. The second re-implements the name draw with an unbounded
   `while name in used` (no `NAME_REDRAWS` cap), the spread with literal `0.05` and no clamp or
   rounding (muster's `_spread`, muster.py:234-237), ids fixed at three digits where muster widens
   them, and its own station rule (landsmen to the waisters, else the afterguard). Joining: a
   `muster.enter_recruit(crew, rating, stream, names)` both use.
3. **Three `number_words`.** crew/model.py:187 (words to twelve, "no" for nought, then figures),
   world/reckoning.py:649 (words to 199), agents/agent.py:2236. The evolutions use both: the
   runner says "Only 13 hands", the anchoring lines in scripts.py import reckoning's
   (scripts.py:6426, 6690, 6773, 6818) and say "a hundred and thirty fathoms". `_and` and `_cap`
   are re-written in some fifteen modules across the tree (runner.py:1627, quarters.py:660,
   scripts.py:6438 among them).
4. **Three ways to apply the work factor.** Step lists and `PhasedScript` and `YardSwing` integrate
   `progress += dt / (duration * factor)` (runner.py:882, scripts.py:1629, 923); `LugDip` and
   `SetteeChange` subtract `dt / factor` (scripts.py:462, 535); `FishingGearScript` compares the
   raw elapsed time with `duration * factor` at the current tick (scripts.py:9003), so a factor that
   falls (hands arriving to an all-hands haul) can finish the work at once, and its `remaining_s`
   ignores the factor (scripts.py:9032). Joining: every script on one progress helper.
5. **Two fatigue models.** `Sailor.fatigue` 0..1 kept by the routine for hands, with words at 0.2 and
   0.5 (model.py:95-96); and the named people's hours-owed fatigue in `world/needs.py` from
   `data/crew/needs.yaml` (lines 32-50), which reads a hand's 0..1 at other bounds
   `[0.3, 0.5, 0.7, 0.85]` (needs.yaml:50). Officers are skipped by the routine (routine.py:209),
   so they have only the second.
6. **Evolution ids named in Python** (2.2, 1.3): the catalogue's ids are a second time in
   `HANDING_EVOLUTIONS`, `QUARTERS_OWN`, `CALLS_HANDS_WHEN_SHORT`, the order modules' dicts; 70 of
   the 108 ids are quoted somewhere in Python.
7. **The verb's words** for an evolution: the YAML `verb:`, `vocabulary.yaml` (twice: `verbs:` and
   `evolutions:`), and Python dicts in `orders/ground_tackle.py:66-84` and the other order modules.

## 4. Size and shape as a hazard

- `scripts.py` 9,095 lines, 49 script classes plus ~120 helpers, and also a library of rig queries
  other packages import. Its docstring (scripts.py:1) still says "Scripted manoeuvres: tack, wear,
  heave to and fill away", as do runner.py:41 and `__init__.py:8`; it now holds anchors, boats,
  fishing, masts, sails, reeving and more.
- Longest functions: `GetUnderWayScript.tick` 279 (scripts.py:8058), `TackScript.tick` 178
  (1470), `HeaveToScript.begin` 156 (2802), `ComeToAnchorScript.tick` 133 (7087),
  `WearScript.tick` 127 (1973), `_judge_lying_to` 114 (2435), `tend_lying_to` 96 (2215),
  `Runner._env` 96 (runner.py:616), `Quarters.beat` 95 (quarters.py:196), `_hove_to_no_longer` 87
  (2559). Classes: `TackScript` 697 lines, `GetUnderWayScript` 519, `FillAwayScript` 401,
  `HeaveToScript` 348; `Runner` 1,311.
- Function-local imports: 113 in the two packages, 67 in scripts.py alone, 21 of them
  `from freesail.evolutions.runner import ...` "to avoid a cycle" (runner imports scripts at the
  top, scripts.py:843, 895). The late imports at scripts.py:9083-9095 exist for the same reason.
- The runner's tick reaches up into the orders layer every tick: `orders.storm.keep_storm_canvas`,
  `orders.navigation.keep_course_pending`, `orders.navigation.watch_the_stern` (runner.py:392-405),
  while `orders` imports the runner. Scripts import `orders.prompt.world_of` to find the World from
  a ship (action_scripts.py:77, 255, 324; fight_scripts.py:20; repair_scripts.py:65).
- State is passed through `ship.extra` by string keys (`"evolutions"`, `"crew"`, `"routine"`,
  `"quarters"`, `"battery"`, `"hove_to"`, `"lying_to.hands"`, `"storm_canvas_pending"`,
  `"course_pending"`, `"true_wind_kn"`, `"health"`, ...), read with `getattr(..., None)` guards
  throughout, so a renamed key fails silently. `quarters.py:408` reads `battery._shut`, a private
  field of another package.
- Settee special cases: 232 lines of scripts.py and 13 of runner.py mention the settee, a sail
  that one ship file carries (`data/ships/bilander.yaml`), with six evolution files and a 1,566-line
  test file. The lug: 126 lines in scripts.py, two ship files.
- Comments carry history in place of explanation (section 1.1): e.g. runner.py:756-766 explains
  `_settees_only` through "the lead's ruling (3)(iii) of 2026-11-10" and a TuningNotes heading;
  reef_square.yaml:32-59 is 28 lines of rulings above one crew line. A newcomer is told why each
  number was argued, not what the machinery is; the YAML is half comment.

## 5. Correctness and honesty

5.1 **Thirst kills only when the food is gone too.** health.py:868-871 sets
`water_out = water_tons <= 0 and provisions_days <= 0`; the deaths and the thirst sick list follow
it (872-883). The docstring (health.py:31-34) and the constants' comment (104-108) say the water
expended alone counts the days. A ship with water out and bread left never sickens or dies of
thirst. Weight medium, confidence likely (sure about the code; the intent is the docstring's).

5.2 **The registry says typos fail at import; most do not.** registry.py:25-27 claims "parses
every expression in it once (so a typo fails at import)". A bare unknown word is a string
(expr.py:305), so `sail.state != fruled` parses, loads and is always true; an unknown function name
parses and fails only when evaluated, mid-game; `timing:` keys are not checked against anything,
and a misspelt one silently takes the Python default (60 s for any phase, scripts.py:3602) or a
stale one (2.3); a bad `crew:` line is read only when a crew exists at `start` (runner.py:333-337).
Shown in one process: `parse_evolution` accepted a file with `sail.state != fruled`,
`wreckd(...)`, a `sets: sail.stat` and `timing: {brace_ss: 45}`; the first evaluated `True`, the
second raised "'wreckd' is not a function" only at evaluation. Weight medium (it is the claim that
makes the catalogue safe for a keen player), sure.

5.3 **A person dead of thirst is logged as killed by a shot.** health.py:1010-1017 records
"{name} died of thirst", then calls `_station_killed` with a stand-in
`Sailor("x", person.name, None, None, None, 0.0, 0.0)` whose `hurt_how` is empty; `_station_killed`
takes `how = sailor.hurt_how or "a shot"` (health.py:353) and records a second urgent line
"... is killed: a shot." and tells the agent "You are killed: a shot". Only for a stationed person
who is not on the muster. Weight low, sure.

5.4 **Aloft fatigue never charged** (2.3). Weight low to medium: the routine's own numbers say work
aloft tires most; in play it never does. Sure.

5.5 **Individual skill is decoration for evolutions.** The muster draws two skills a man; the crew
factor uses the rating's table figure on purpose (hands.py:408-410) so that milestone 2's times
hold. So two able seamen are identical in every evolution; `skill_aloft` is read by nothing. Weight
medium against the proposal's "individuals", sure.

5.6 **Rig-agnostic, with name-bound tops.** The evolution code does not name sails or masts by id:
a grep for literal `"fore"`, `"main"`, `"mizzen"` ids in the code finds only the topmen table
(hands.py:104-108) and docstrings; it works by `cls`, `roles`, `x_m`, `mast_of`, and per-part flags
(`settee`, `dipping`, `heave_to_aback`, `cut_at_mast`, `on_schooner_mast`). No branch on a ship's
name. But the crew model fixes three tops (`Station.FORE_TOP/MAIN_TOP/MIZZEN_TOP`, model.py:43-45,
60) and maps a mast to its top by the id's first word (runner.py:1110-1118, hands.py:104-108): the
lugger's `mizen.mast` (data/ships/lugger.yaml) finds no top; a four-master could not have one.
And because `close_hauled_angle` is never set (2.3), the tack's and wear's new course is six points
off the true wind for a cutter as for a 74; only the physics makes them differ. Weight low, sure.

5.7 **Omniscient helm.** The tack sets the new course from the true wind each tick
(`wind.direction_from`, scripts.py:1590, 1633), and `Runner.step` stores the true wind's speed
(runner.py:391). The deck is not reading a vane. Weight low, sure.

5.8 **Faked outcomes behind step files.** `take_lunar.yaml` is one 900 s step; its comment says the
World "draws the result from the truth and the seed (never computing a distance)"
(take_lunar.yaml:8-12). `heave_lead` is two timers; the depth is the World's. Not this part's fault,
but the catalogue's "what it changes" is empty for them: the data says nothing of the result.
Weight low, sure (from the files; world/reckoning not read).

5.9 **Swallowed exceptions.** Nine `except Exception` in my part: health.py:267, 376, 410, 423, 738,
745, 750 (around agent and station calls), repair_scripts.py:571, 799. The last turns any bug in
`orders.resolve` into the refusal text shown to the player (`return str(e)`). Weight low, sure.

5.10 **Determinism.** No wall clock, no unseeded random: the muster draws only from its stream
(muster.py:202-206), health from the World's "health" stream (health.py:211-215). Sets of string
ids are used for membership only in what I read (runner `holds`, repair_scripts.py:798). Sound.

5.11 **The boundary.** Neither package imports `client`, `agents`, `ui` or `api` (grep of all import
lines). Both import upward into `orders` and `world` (21 function-local imports, list in 4), and
`crew/health.py` writes into an agent's state by duck typing: `agent.notices.append(...)`
(health.py:367-369, 405-407), `agent.deck = False` (739), `holder.stand_down(...)`,
`holder._lose_deck(...)`. The letter of the boundary holds; the spirit does not. Weight medium,
sure.

5.12 Smaller: `quarters.lend` adds "and the marines" to the line (quarters.py:392-399) without
putting any marine in `freed`; they are taken, if at all, by the next request because they are
idle, so the words can name marines who were not taken. Weight low, likely. `_check_party` counts
the named party over the whole company (runner.py:545-550) while the request draws only from the
deck (runner.py:1077-1082), so a named watch below passes the check and then waits. Weight low, a
suspicion.

## 6. Thin or overgrown

Overgrown. The evolutions are the most detailed part of the game I can see: a tack is 697 lines
with Luce's words for each phase, settee dips, lugs, schooner masts, a course to steer and the
recovery from irons; a settee for one ship has some 245 lines. Against that, the crew it runs on is
thin where the proposal is specific: no morale per man, skill not used for the work, aloft fatigue
not charged, a fatigue whose largest effect on a job is under 1.5x and in practice a few per cent
(0.06 an hour at work; 0.2 for a broken night). The data catalogue is thinner than it is said to be
(1.3): it is the place for durations, hand counts and log lines, while the seamanship is Python.

## 7. What is not tested

- 26 evolution ids are named in no test file (back_anchor, batten_down, cast_loose_guns,
  cat_and_fish_anchor, cut_away_mast, dip_lug, fish_spar, haul_lines, haul_nets, haul_seine,
  haul_trawl, heave_deep_sea_lead, heave_log, heave_short, lay_out_kedge, let_go_anchor,
  make_signal, rig_preventers, send_boat, set_lug, set_up_rigging, shoot_nets, shoot_seine,
  shoot_trawl, take_in_lug, veer_cable), but most are reached by order words in tests ("cut away"
  in 9 files, "let go the" in 30, "veer" in 15, "set up the rigging" in 1, "back the anchor" in 1,
  "batten down" in 1). I did not run the suite, so I cannot say which branches are covered.
- `furl_gaff`, `furl_jibheaded` are tested (test_catalogue.py) and unreachable in play: tests keep
  dead data alive.
- `Routine.set_aloft` is tested and unwired: the test proves a seam the game does not use.
- No test names `expr.tokenize`, `expr.evaluate`, `expr.split_target` directly (grep); the
  expression language is tested through the catalogue. No test I found checks that the registry
  refuses an unknown bare word or an unknown timing key (it does not).
- The health paths in 5.1 and 5.3 (water out with provisions left; a non-muster person dying of
  thirst): grep finds no test of `water_out_since` or of the "died of thirst" line for a person.

## The ten findings that matter

1. **The catalogue is not the seamanship.** 64 of 108 evolutions are Python classes (49, in 9,095 +
   1,414 lines) whose YAML holds only durations, a crew line and log text; the 44 data ones are
   linear lists of about 2.5 steps with one crew line for the whole job. No file has aliases; the
   words live in `vocabulary.yaml` and, for 35 ids, only in Python. (1.3; tack.yaml vs
   scripts.py:1156-1852.) High, sure.
2. **A player can add a data-only evolution only of the simplest kind**, and must edit
   `vocabulary.yaml` twice as well; shown in memory (1.3). Any judgement, outcome or new sail class
   needs Python, and several id lists in Python would not know the new one. High, sure.
3. **The registry's typo safety is not true**: unknown bare words are strings, unknown functions fail
   mid-game, timing keys and crew lines are unchecked at load (registry.py:25-27, expr.py:305,
   scripts.py:3602). Medium, sure.
4. **Sailors are less individual than the proposal says**: no per-man morale, `skill_aloft` never
   read, the crew factor reads the rating table not the man (hands.py:408-434). Medium, sure.
5. **Aloft fatigue is never charged in play**: `set_aloft` is called only by tests (routine.py:114-123,
   55, 212). Low to medium, sure.
6. **Thirst kills only when provisions are out too** (health.py:868-871 against 31-34). Medium,
   likely.
7. **Close-hauled is defined four times and differs** (scripts.py:202, 1131; runner.py:653, 1635;
   orders/verbs.py:966), and the per-ship hook `close_hauled_angle` is never set. Medium, sure.
8. **Dead and missing catalogue entries**: `furl_gaff`, `furl_jibheaded` unreachable in play;
   `set_sprit`, `take_in_sprit` named in vocabulary.yaml:1902, 1914 with no file; three dead health
   constants (health.py:95, 109, 167); stale Python timing defaults (scripts.py:1520, 1636). Low,
   sure.
9. **Layering and size**: 113 function-local imports (67 in scripts.py), the runner calling into
   `orders` each tick (runner.py:392-405), `crew/health.py` writing into agents' state by duck typing
   (health.py:367, 405, 739), state passed by string keys in `ship.extra`. Medium, sure.
10. **Duplicated helpers with drift**: a second sailor maker in world/dealings.py:2820-2850 without
    the muster's clamp or redraw cap; three `number_words` with different ranges used side by side
    in evolution lines; three ways of applying the work factor, `FishingGearScript`'s finishing early
    when hands arrive (scripts.py:9003). Low to medium, sure.

## What I did not read

- `scripts.py`: read whole lines 1-1160, 1470-1650, 3580-3660, 8955-9095, and its full function and
  class map with line counts (AST). Lines 1160-1470 and 1650-3580 and 3660-8955 (about 7,500 lines:
  most of the tack's other methods, wear, heave to, fill away, lying to, send down and sway up, the
  sail work scripts, clear wreck, box-haul, lie a-try, scud, back and fill, reeve, trim sheet, all the
  anchor and port scripts) were not read line by line; findings about them are from grep and the map.
- `repair_scripts.py`, `action_scripts.py`, `fight_scripts.py`, `trim.py`: mapped and grepped, read
  only at repair_scripts.py:785-840.
- `victuals.py`: lines 1-64 and 175-270 read; the rest not.
- Read whole: `registry.py`, `expr.py`, `runner.py`, `crew/model.py`, `muster.py`, `bill.py`,
  `routine.py`, `hands.py`, `quarters.py`, `health.py`.
- Data: ten evolution files read whole (listed in 1.3), the other 98 by grep and a loader script.
  `data/crew/needs.yaml` read to line 70; `names.yaml` and `ration.yaml` not read.
- The proposal itself was not opened; its words are as the reviewer quoted them to me.
- `combat/morale.py`, `world/needs.py`, `world/reckoning.py`, `world/fishing.py`, the `orders/*`
  callers: grepped only.
