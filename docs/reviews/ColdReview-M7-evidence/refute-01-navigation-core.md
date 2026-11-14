# Second reader: refutation of code-01 (navigation) and code-08 (core/ship/physics)

Commit under review 504a25066c6995ce9829a19ffc597feb510a1870 (the tree is checked out at a
later review commit; the files cited are unchanged). Read under READERS.md and REFUTERS.md.
Nothing opened under docs/dev, docs/design, docs/playtests, docs/gates. No test suite run;
three single greps of tests, a few seconds of python (`-I`), and reads of the cited lines.
Only this file written.

## The table

| finding (short) | reader wt | my verdict | my wt |
|---|---|---|---|
| 08-1 A checkpoint can run code | high | STANDS IN PART | medium |
| 08-3 A save survives no change of build | high | STANDS | high |
| 08-4 Ships are generator output, not data a person edits | med-high | STANDS IN PART | medium |
| 08-6 Cross-platform determinism assumed, not secured | medium | STANDS | medium |
| 08-5 Generator re-implements sail-force law, drifted | medium | STANDS | medium |
| 08-2 Boundary not kept (core imports agents/api) | high | STANDS | high |
| 08-8 Same fact in several places | medium | STANDS | medium |
| 08-9 Rig-agnosticism fails for crew/mast | low-med | STANDS | low-med |
| 08-10 Dead and stale | low | STANDS IN PART | low |
| 01-4/08 Two frames for one position (sun lon vs true lon) | medium | STANDS | medium |
| 01-5 Noon line pairs course made good with distance sailed | medium | STANDS | medium |
| 01-9 `time_words(12.5)` "half past twelve at noon" | low | STANDS | low |
| 01-10 Estimator detail on sights that are truth+draw | low-med | STANDS | low-med |
| 01-1 World layer not a boundary | high | STANDS | high |
| 01-6 Number/distance words built 8+ times, disagree | medium | STANDS | medium |
| 01-7 Account run-on computed four ways; doubt ghost | medium | STANDS | medium |
| 01-3 Chart tiles 359 MB of plain git blobs | medium | STANDS | medium |

## The findings I was asked to press hardest

### 08-1 A checkpoint can run code on the player's machine (high, sure) -> STANDS IN PART

The mechanism is real and I reproduced it. `_Unpickler.find_class` (replay.py:491-501)
admits any `(module, name)` whose module starts `freesail.` or `numpy`, plus a fixed
`_ALLOWED_EXACT`/prefix set. Pickle resolves dotted `name` through the named module's
namespace, so a name imported into a `freesail.` module is reachable. Run with `python -I`:

```
freesail.settings . os.getcwd  ->  /home/user/FreeSail
```

i.e. the STACK_GLOBAL `freesail.settings` / `os.getcwd` resolved and I called it through a
hand-built REDUCE. `freesail.settings` does `import os`, so `os` (and thence `os.system`)
is an attribute of that module; the same holds for any stdlib name any `freesail` module
imports at top level. `tests/test_checkpoint.py:125-130` tests only the direct
`os.system` (a GLOBAL `posix system`), which is correctly refused; it does not test the
dotted route. So the allow-list is porous exactly as the reader says.

**What refutes the consequence, in part.** The reader's one-line summary is "a save shared
with its checkpoint is a program." Two things narrow that:

1. **No pre-verification, but also no network delivery of the checkpoint.** `read_checkpoint`
   (replay.py:532-544) unpickles *before* any check: the digest and the
   seed/tick/journal match in `load_report` (815-905) run only on the already-built
   object. So the digest is no guard, confirming the reader. But the only channel the
   game offers to *hand a save to another person* is the browser download `GET /api/save`
   (server.py:1557-1563), which returns `world.save()` as JSON **and no checkpoint**. A
   save obtained that way replays its journal (safe). The `.checkpoint` sidecar exists
   only on local disk beside a `save file.json` written by `save_to_file`
   (replay.py:68-81). The server binds `127.0.0.1` by default (server.py:1744).

2. **To be exploited the victim must receive the `.checkpoint` file itself** (e.g. a
   zipped save directory from a stranger) and run `--load` on the matching `.json`, or
   paste that path into their own localhost harbour (harbour.py:522-527). Nothing verifies
   a save's provenance before the checkpoint is unpickled, so if that file is present and
   belongs to the save, it runs. The project's own premise ("a saved log is a saved game",
   and saves are meant to be kept and compared) makes checkpoint-sharing a foreseeable use.

So the vulnerability is genuine and the "safety claim is false" part stands flatly
(replay.py:27-28, 448-450 say "a checkpoint from elsewhere cannot run code here", which is
untrue). The *reach* is narrower than the summary implies: the ordinary share path strips
the checkpoint, so the attacker needs file-level access to hand over the sidecar. I lower
the weight to **medium**: real arbitrary-code-execution on a hostile sidecar, but not
reachable through the game's own save-sharing feature, and no verification would help once
the file is on disk. The fix (an allow-list of classes, not modules, or an HMAC over the
pickle) is cheap and the claim in the docstring should be struck regardless.

### 08-3 A save survives no change of build (high, sure) -> STANDS

Confirmed on every point. The fingerprint hashes every `freesail/**/*.py` and every
`data/` file but the tiles, read from the working tree (world.py:54-72); an untracked file
under `data/` would be included (the glob is `data.rglob("*")`), so any edit to any Python
file or data file, and any stray file, changes the stamp. `check_replay` (replay.py:739-812)
refuses another build's game that holds a station transcript unless `--replay-anyway`, and
otherwise warns "the log may differ". The checkpoint from another build is accepted with a
one-line notice (load_report:898-905), relying on class defaults and `_rebind`'s converters.
`save_to_file` (68-81) swallows `PicklingError`/`TypeError`/`AttributeError` and unlinks any
stale checkpoint, and no driver reports whether the checkpoint was written
(server.py:756-773 catches only `OSError`; console.py:719-722 reports only the path). I ran
a fixture: `m5c-cutter-tick34091` loads from its checkpoint under this build (`m6c`) in
~6.8 s with the notice "written by another build (unstamped, before 37d) ... the game goes
on ... under this build's rules." So the only *exact* road across a build change is the
very pickle that 08-1 shows is dangerous and that can vanish silently. This is the
strongest finding in the pair. Weight **high**.

### 08-4 Ships are generator output, not data a person edits (med-high, sure) -> STANDS IN PART

The core claim holds: every file carries "Generated by tools/gen_ships.py ... do not edit
this file", `tests/test_ship_particulars.py:554-592`
(`test_generator_reproduces_the_committed_files`) subprocesses the generator into a temp
dir and asserts byte-for-byte (as UTF-8 text) equality for every committed YAML, so a hand
edit fails the suite and a regeneration undoes it. The schema drops unknown keys silently
on spars/sails/lines/hull (schema.py:71 and the `_parse_*` bodies), and `Spar.from_spec`
reads a misspelt `x_m`/`height_m` as 0.0 (parts.py:242-243), so a hand would slip unseen.
All confirmed.

Two refinements, neither fatal: the reader's abstract says "All 18 YAML files are generator
output"; 15 of 18 open with "Generated by", and the three that do not
(`privateer-schooner.yaml`, `merchant-brig.yaml`, `bilander.yaml`) carry a long provenance
header first and then "Generated by tools/gen_ships.py" lower down, so the count "18" is
right in substance. And the reader's own body already says the game *will* load a
hand-edited file (the suite failure is a developer gate, not a runtime block), so a
determined player editing their own working copy is not stopped at play time. The finding
stands as "the source of truth is 28,810 lines of Python, not the data a non-programmer
owner can touch", which is the point the owner cares about. Weight **medium**.

### 08-6 Cross-platform determinism assumed, not secured (medium, likely) -> STANDS

Confirmed and if anything understated. `events._canonical` (events.py:123-136) rounds every
float to 9 significant digits for the digest; its own comment concedes a Windows/glibc
last-bit libm difference "found at gate 5a" that the rounding only sometimes hides. The one
determinism test (`tests/test_determinism.py`, 37 lines) drives a bare `World` with the M0
point-ship orders (steer/speed/stop), never a rigged ship's physics. More telling, the
project's own known-truths file pins *different* digests per platform rather than asserting
cross-platform equality: `test_known_truths.py:2991` "c8905673... before package 37k
(78eec3dc... on Windows then)", :4094-4096 "the merchant passage ... differs from the
owner's Windows figures by two lines and two ticks ... the difference recorded as an open
item", :9335-9341 "The digests differ on the owner's Windows machine ... two digests are
compared only when both are made in the same run." So the maintainers already know a ship's
log is not bit-identical across platforms; the digest rounding is a partial mask, not a
guarantee, exactly as the reader says. CI runs Windows (`ci.yml:52`) but the whole suite
pins Linux figures and only optionally runs Windows (`whole-suite.yml:16-17, 58`). Weight
**medium**.

### 01-4 / 08 Two frames for one position: sun longitude vs true longitude (medium, likely) -> STANDS

Confirmed by code and arithmetic. `Sun.longitude_deg` (sun.py:132-138) turns `ship_x` (plane
easting, world.py:1304-1308) into degrees by dividing by `METRES_PER_DEGREE * cos(latitude)`
with the *current* latitude, and nothing adds the start meridian or tracks the convergence
of meridians as she sails; the sun's longitude is purely a function of plane easting.
Meanwhile `_tick_geo` (world.py:1554-1575) advances the true `Position` on the sphere by the
same plane run **plus** the scenario's stated `current` and the tide stream, neither of which
`ship_x` ever sees. I ran the drift: a plane heading ~207 deg from 50N 5W down to 32.6N (a
Channel-to-Madeira track) puts the sun's longitude ~1.39 deg east of the true longitude,
about 5.6 minutes of noon time. A 1-knot stated current would add up to ~240 nm of
east-west divergence over ten days that the sun never learns of. The weather's Coriolis is
fixed at 50N (`CORIOLIS_50N = 1.117e-4`, weather.py:118-125, used in the gradient-wind cap
at 1360-1362) though the climatology boxes run to the Canaries, where f is ~0.6 of that.
All as the reader states; "likely" is the honest confidence since it is arithmetic, not a
played passage. Weight **medium**.

### 01-5 The noon line pairs course made good with the distance sailed (medium, sure) -> STANDS

Confirmed. `Reckoning.advance` accumulates each board's length:
`run_since_noon_nm += hypot(de, dn)` (reckoning.py:1136), the straight-line magnitude of
each worked step. `since_noon` (1793-1801) returns that **sum** as the run, paired with
`bearing_and_distance(noon_mark, position)` for the course made good (a single
start-to-now bearing). The noon line (reckoning.py:3851-3855) prints "Course made good
since yesterday <point>, <run> miles" with `run` = that sum. So after a day of tacking the
printed distance is the total through the water along the boards, not the distance along
the made-good course it is named with; the two belong to different quantities. This is a
period-realism defect in a log line the player reads at every noon. Not run as a passage,
but the code is unambiguous. Weight **medium**.

### 01-9 `time_words(12.5)` gives "half past twelve at noon" (low, sure) -> STANDS

Reproduced exactly (tide.py:1110-1127):

```
12.0  -> 'noon'
12.25 -> 'a quarter past twelve at noon'
12.5  -> 'half past twelve at noon'
12.75 -> 'a quarter to one at noon'
0.25  -> 'a quarter past twelve in the middle watch'
```

The branch `elif h < 17: part = "in the afternoon" if h > 12 else "at noon"` tags the whole
12:00-12:59 hour "at noon". It feeds `the tide by the almanac` and a shaped course's tide
turn (reckoning.py:4794, dealings.py:1751/2044/2053). Visible, low cost, the pinned-line
tests did not catch it (no test names `time_words` or "half past twelve"). Weight **low**.

### 01-10 Estimator detail on sights that are the truth plus a draw (low-med, sure) -> STANDS

Confirmed. The noon latitude is `pos.lat_deg + stream.gauss(0, sigma)/60` (sights.py:212-213);
the time sight's longitude is `pos.lon_deg + error` where the error is the chronometer's
plus `stream.gauss(0, sigma)` (sights.py:558-562); the lunar is `pos.lon_deg +
stream.gauss(0, sigma_deg)` (sights.py:724), each "drawn and not computed" in its docstring.
Against that, the estimator (reckoning.py Reckoning/Navigation) carries a 2x2 covariance,
bias vectors resolved along observation lines, a 36-mark best-pair/triple fix search, a ghost
reckoning for the doubt, and a period tide worked by the quarter hour. The elaborate
`moon_at` (nine lunar stars, moon.py) only gates whether a lunar is allowed and sets the
error's spread; no lunar distance is ever cleared. So the error model is grafted onto
ground-truth-plus-noise rather than onto a computed observation. The reader marks the
judgement as his own; the facts are sound. This is a design-weight observation, not a bug;
cost to the owner if left is nil beyond the wasted machinery. Weight **low-med**.

## The other kept findings, checked more briefly

### 08-2 / 01-1 The simulation boundary is not kept (high, sure) -> STANDS

`grep -nE '^\s*(from|import) freesail\.(agents|api|ui|client)' freesail/core/*.py` = 19
imports, all inside functions (world.py imports `agents.director`, `api.readings`,
`agents.watches`, `api.queries`, `agents.harness`; replay.py imports `agents.harness`,
`agents.director`, `agents.seat`, `api.session`; acts.py imports `agents.journal`,
`agents.director`). The same grep over ship/physics/crew = 0, so the reader's "ship,
physics and crew are clean" holds. physics imports `evolutions.trim` (sails.py:96) and
`world.sea` (motion.py:38) at module level. In the world layer: `freesail.world` imports
`freesail.agents` 62 times and `freesail.orders` 76 times; reckoning.py:4037 imports
`agents.agent.door_words` and writes the model's name and door into the ship's log
(:4035-4053); movement.py holds `VISITOR_BRIEF`, a verbatim model prompt (:1028-1043).
There is no import-linter or test enforcing the boundary (grep of tests and pyproject
finds none). All confirmed. Weight **high**: this is architecture debt the owner was
promised against, and nothing guards it.

### 08-5 Generator re-implements the sail-force law and its copy has drifted (medium, sure) -> STANDS

`PEAK_COEFF` (gen_ships.py:136) gives `studding: 1.25`; recomputing `max |(C_L, C_D)|`
over `data/sail_classes.yaml` gives studding **1.44** (square 1.227 vs 1.23, gaff 1.29,
jibheaded 1.322 vs 1.32, lug 1.285 vs 1.29, lateen 1.246 vs 1.25 all agree; sprit 1.2 has
no `PEAK_COEFF` entry). So studding gear is rated against ~13% less force than the engine
puts on it, and a sprit sail would `KeyError` the rating pass (gen_ships.py:445
`PEAK_COEFF[cls]`). The generator also hard-codes shear 0.11, its own `RHO_AIR` and `KNOT`
(gen_ships.py:396-397, 440-446). The comment at 134 ("if the curves change, change these
and rerun") admits the hand-copy. No test compares `PEAK_COEFF` to the YAML. Confirmed.
Weight **medium**.

### 08-8 / 01-6 The same fact in several places, already disagreeing (medium, sure) -> STANDS

I reproduced the word divergence the reader flagged: `chart.fathoms_words(23.77)` = "13
fathoms" vs `reckoning.fathoms_said(23.77)` = "thirteen fathoms"; `fathoms_words(-1.0)` =
"dry at the datum" vs `fathoms_said(-1.0)` = "no water". Both reach the player (the
grounding line chart.py:505-516 via `_fathoms_words`, the cast line reckoning.py:3096).
Note the two are not fully independent: `evolutions/scripts.py:6425` wraps
`chart.fathoms_words`, and chart.py:255 aliases `_fathoms_words = fathoms_words`, so the
numeral style "13" vs "thirteen" is a genuine two-speller split in player-facing text.
Gravity 9.80665 (units.py:32) vs 9.81 (ground.py, water.py), cwt 50.802 vs 50.8023,
interpolation repeated, and the discarded 0.9 cloth fallback kept at parts.py:351 all
confirmed by the reader's cites. Weight **medium** (log-text inconsistency the player sees).

### 01-7 The account run on from the last working computed four ways; the doubt ghost (medium, sure) -> STANDS

`account_now` (:2716), `_account_with` (:2663), `_in_hand` (:4111), `_run_since_step_nm`
(:5473) each recompute the run since the last step. `_account_with` re-derives course and
run itself (no eye-allowance, no hove-to drift) and is the position the master's tide is
looked up at (`_tide_between`), so the water he works can come from a slightly different
place than the account shown. `doubt_now` (:2742) builds a `ghost = Reckoning(...)` and
copies ~10 fields by hand (:2755-2765); any new field on `Reckoning` not added here
silently misstates the doubt the player reads. `doubt_now`/`account_now` are tested for
caching stability (test_reckoning.py:1263-1290) but not for field-copy completeness.
Confirmed. Weight **medium**.

### 01-3 Chart tiles 359 MB of plain git blobs (medium, sure) -> STANDS

`du -sh data/charts` = 359M; `.gitattributes` has no LFS, only `* text=auto eol=lf` and a
note that git detects the tiles as binary; `git count-objects` size-pack = 427.44 MiB;
`git log --oneline -- data/charts/tiles | wc -l` = 9 commits (of 435). Every regional
rebuild adds its megabytes to history for good and every clone pulls all of it. Confirmed
on the facts; the growth rate is a reasonable inference. Weight **medium**.

### 08-9 Rig-agnosticism fails for crew and mast levels (low-med, sure) -> STANDS

`CREW_STATIONS` (schema.py:394-403) fixes `fore_top`, `main_top`, `mizzen_top` (three named
tops); mast levels are the four of `YARD_LEVELS`; `strain._MAST_WORDS = ("fore", "main",
"mizzen")` (strain.py:449). `grep -c mizen data/ships/lugger.yaml` = 33, and the lugger
files `mizen.mast`, `mizen.lug` etc. against every other file's `mizzen`, so its strain
warnings never group under `_MAST_WORDS`. Confirmed. Weight **low-med**.

### 08-10 Dead and stale (low, sure) -> STANDS IN PART

`_ship_length_m`, `_ship_draught_m`, `_ship_heel` have 0 callers; `shown_dict` 0;
`_blanket_factors`/`_chord` named only in docstrings; `Clock.bells` tests only. All
confirmed dead. One correction to the reader's list: `_ship_speed` is **not** dead in the
same way; `grep` shows `world/ships.py:1941` calls `_ship_speed_ms(ship)` (a differently
named helper), but the specific `world.py:2858-2877 _ship_speed` the reader cites has no
caller (`grep -c` for `_ship_speed` across freesail/client excluding defs = 1, and that one
is `_ship_speed_ms`, a different function). So the reader's `_ship_*` quartet is genuinely
unreached; the near-name collision is worth noting but does not rescue them. Stale words
(`BUILD_NAME = "m6c"` while comments say m5c-c; "four reference ship files" while 18 are
written; the fingerprint's "thirty milliseconds") all confirmed. Weight **low**.

## Found on the way

**The checkpoint digest is checked after unpickling, so it is no defence at all, and the
project treats that digest as the integrity gate.** The docstring and `load_report` speak as
if a checkpoint that "belongs to the save beside it ... and its log's digest is the one it
was written with" is trusted. But `read_checkpoint` (replay.py:536-544) calls
`_Unpickler(f).load()` and `_rebind(world)` *before* returning, and the digest/`matches`
comparisons in `load_report` (857-876) run only on the already-constructed object. A hostile
or corrupt checkpoint has already executed its REDUCE opcodes by the time the digest is
looked at. So for finding 08-1 the digest cannot be offered as mitigation (the reader did
not lean on it, but a defender might); it is purely a staleness check, not an integrity one.
Medium.

**`restore_python_rules` runs only on the replay road, not the checkpoint road**
(console.py:993-994: `if report.how == "replay": restore_python_rules(...)`). A game whose
standing orders were written in Python (`spec M4 §4`) and loaded from a *checkpoint* relies
on those rules being pickled into the object graph instead of restored from the save's
`standing_orders`; if a checkpoint from an older build lost a rule's state to a dropped
`__getstate__` field, the two load roads would diverge in the standing book, and no test I
found compares the standing book across the two roads for a Python-rule save. A suspicion,
not demonstrated; low, worth a test.

## What I did not do

- I did not run the test suite or any passage; the checkpoint load I timed was a single
  fixture (`m5c-cutter-tick34091`, ~6.8 s). The cmg/run, two-frames and determinism
  findings I checked by code and short arithmetic, not by a played game.
- I did not read tools/gen_ships.py or tools/ships/*.py whole; I checked only the cited
  lines (PEAK_COEFF, DESIGN_WIND_KN, static_kn) and recomputed the peak coefficients from
  `data/sail_classes.yaml`.
- I did not open any chart tile, the manifest beyond a head, or docs under dev/design/
  gates/playtests (cold rule).
- I did not independently audit the 62/76 world->agents/orders import counts beyond the
  grep totals, nor read reckoning.py or world.py whole; I read the cited stretches.
