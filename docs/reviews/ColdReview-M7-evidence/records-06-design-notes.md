# Records 06: the design notes (`docs/design/`)

Reader's evidence for the second sitting, by RECORDREADERS.md. Tree at 504a250 (the review's
branch head b72ed89 adds only the review). Nothing changed but this file. One short python run
(below, §1.3), one grep after another; no suite run. Paths under `docs/design/` unless given.

**Read whole:** `ColdReview-2026-09-30.md`, `NotesForM7.md`, `Design-SlaveryAndSuppression.md`,
`InwardAndOutward.md`, `Presentation.md`, `Plan-ShipsWorkflow.md`, `Design-FacadeReaders.md`.
**Read in part:** `Design-OneWorld.md` (head, §2.2, §2.13, §3, §4 step 1 and step 6, §5, the
as-built history whole from l.1390; §1 and most of §2 skimmed); the head, decisions and history of
`Build-Ships.md` (l.1-340, l.2155-2448 and §2.5), `Design-Prizes.md` (l.1-66, l.1074-1367),
`Design-ShipBought.md` (l.1-80, l.926-938, l.1046-1151), `Design-PlaceKnowledge.md` (l.1-72,
l.400-430, l.655-670, the step 4 postscript), `Design-Signals.md` (l.1-80, l.405-647),
`Design-Squadrons.md` (l.43-96, l.450-537). Decision 29 and 68 of `docs/DesignProposal.md`.

---

## 1. Where the record and the thing differ

### 1.1 Faults the record books as mended or to be mended, still in the tree

1. **The followed ship's far body is left behind (not in the review).** `Design-ShipBought.md`
   l.926-938: under `--ship` (or `follow`) the ship the player is aboard is never brought up to
   her truth on the sea; "every other ship's brain, lookout and hail reads her far body, so for
   them she is where she was". The lead reproduced it at the gate (l.1125-1129: 933.8 m at tick
   361, 3,803.4 m at 1,261) and booked it to package 60's step 1, "proved by 7-481 either way".
   Package 60 is not built (l.1148-1151: "Nothing is built yet"); truth 7-481 does not exist
   (grep of `tests/`: no match). **Run at 504a250** (scratch script over
   `tests/test_aboard_another.aboard_x`): 0.0 m at the start, **925.6 m after 300 ticks, 3,682.0 m
   after 1,200**. It belongs with the review's far-world head (F2.8) and its "player aboard
   another ship" items.
2. **"Every far captain perceives the player's sky"** (`Design-OneWorld.md` §5.1 item 6,
   l.1308-1312: "Step 6's `conditions_at` per hull mends the hulls"). As built, step 6 kept "the
   hull's sea and conditions ... the followed hull's (the study's findings 5 and 6 are the owner's
   knob)" (l.1790-1791); `Design-FacadeReaders.md` l.106 records the sea still "reading the followed
   hull's sky as its one visibility ... noted for M8's weather at each body". In code:
   `world/brains.py:99-102` reads `world.conditions`. So the study's mend was taken back to a knob
   and then to M8; the review's F2.8 should say the project knows it.
3. **The struck-colours line.** `Design-Prizes.md` step 3 (l.1214) built the captive's channel and
   step 2 the prize crew; `freesail/orders/gunnery.py:946-949` still tells the player who strikes
   that "the prize crew, the prisoners, the captive's channel" are "not in this game yet". Confirms
   the review's F2.11; the record calls the thing built and never touched the line.
4. **Decision 68's rules are kept only by absence** (detail §4c below): the note's first building
   package (l.699-713) is not begun; nothing in `freesail/` names a slaver or a corsair.

### 1.2 Decisions of the design notes the code does not keep (or the record re-ruled silently)

- **The façade built is not the façade costed.** The study's façade (`Design-OneWorld.md` §2.2
  l.559-568) is a `Hull` that *delegates the World's shared fields* to the World. What step 6
  built is the inverse: every per-ship name of the World a property to a *current hull* held on a
  thread-local stack, and `Hull.__getattr__` running any other World method "with the hull
  current" (l.1748-1762). The study's step 6 rule, "a moved pin is restored by the order, never
  re-pinned" (l.1216-1218), was broken by the step itself: three pins moved and were re-pinned
  (the bells, the hoists, the hit's tick: l.1848-1860). The study's §3.3 aim, "none moved"
  (l.998), likewise.
- **The two strict phases of the tick** (the design's §2.2) were "taken another way" and left a
  refinement for the owner to ask for (l.1782-1787); still open (l.2099).
- **The `world` to `hull` rename** the study allowed "file by file" was "made nowhere" (l.2077-2080).
- **The study's finding 5, a crewed firer has no roll** (l.1303-1307, "step 6 mends it") is in the
  same "owner's knob" sentence (l.1790-1791). Not checked further.
- **The shipwright's `PEAK_COEFF["studding"]` 1.25 against the engine's 1.44**, the review's F2.1
  drift, is in `Build-Ships.md` §18 l.2248 as "not this package's to change silently (map-engine
  §10)". Known since 2026-10-28; nobody's since.

### 1.3 Where the review's report is wrong, or should be narrowed, by the records

1. **Decision 59/62 (§1.4): "the map and the ship view ignore his place".** By ruling, not by
   omission: `Design-PlaceKnowledge.md` §11 l.413-420 ("the chart pane stays ... the ship view stays
   (the viewer is the owner's drawing of the world, not a reading)") and §12 l.662-664 ("The
   browser's chart pane hidden by place": decided against). The snapshot was never designed to be
   filtered either (§11 l.414-416: it "carries `knowledge: {place, hidden: ...}`" and the page
   greys). The review's finding that the figures are on the wire stands; the word "ignore" should
   say "by the design note's ruling". The note's own step 4 claims "there are not two views of one
   world, and a dimmed figure is still a figure" (l.883-885) while the figure is still in the
   snapshot: the review may quote that against it.
2. **Decision 14, "struck to".** The form that made the player's frigate strike to a cutter was
   added on purpose, for scenario starts (`Design-Prizes.md` step 7, l.1353-1357: "`ship
   "<name>": struck to the <captor>` ... doubted after the first minute"). The finding stands; the
   review should say the form is the director's by design and the guard is a doubt, not a limit.
3. **Decisions 52, 53: "eight forms of a ship".** Two of them are by ruling: "Merging `Vessel`
   into `Hull`" rejected, "one identity, two objects" (`Design-OneWorld.md` §2.13 l.863-864);
   `CrewedWorld` kept as "the builder's and the unpickler's name" (l.1747, l.2097). The review's
   count stands; its weight should note the two are chosen.
4. **Decision 68, "Not examined"**: now examined, §4c below.
5. The free sheet-tending, listed in decision 29 as "not now", **was mended** (package 32e:
   `freesail/evolutions/trim.py:16-20`, `freesail/api/session.py:36-38`). The review does not
   claim otherwise; noted so that the "not now" list is not read as all unmended.

---

## 2. What the project already knew

| Review finding | Known where, when | What was done |
|---|---|---|
| The boundary (F4.1) | Earlier cold review §2.1 (`ColdReview-2026-09-30.md` l.90-99): three crossings, `core/replay.py:52`, `world/scenarios.py:248`, `orders/stations.py:22`; "a registration hook ... would cost a day"; consolidation package §6 item 10 (l.557-564) | Decision 29 (`DesignProposal.md` l.614): "the consolidation package ... recorded as not now". All three crossings still there (`core/replay.py:143,283,291`; `world/scenarios.py:998`; `orders/stations.py:78`), now some 1,767 in-function imports (review). **Grown worse.** |
| The façade and the far/crewed fold | `Design-FacadeReaders.md` l.12-25: eighteen readers wrong under `follow` or another hull's block, "the fault is latent in every pin"; l.180-182: a test "passed on the trunk only by the fault"; `Design-OneWorld.md` l.1815-1862 (nine "player's things read under another hull's swap"), l.1943-1946 ("no act of any station on a hull was ever journaled since step 6") | Mended by package 97 with a guard (`tests/test_facade_readers.py`, l.130-137). The swap itself "stands as it is" (l.2062-2064). |
| The far world's faults (F2.8) | §1.1 items 1, 2 above; `Design-OneWorld.md` §5.1 item 7 (traders vanish), item 4 (far course across a cape) | Item 4 and 7 to step 4; items 5, 6 to a knob, then M8; the `--ship` drift booked to unbuilt 60. |
| The director's reach (decision 14) | `Design-Prizes.md` step 7 (the `struck to` form); step 0 ruling 8 (l.1168-1173, the adversarial seats) | Built as forms with a doubt. |
| Tests that cannot fail | `Design-Prizes.md` l.1272-1277: truth 7-361 "would have taken [the pace] under its own had it ever run: it stood on a world with no place on the chart"; FacadeReaders l.24-25 | 7-361 moved onto the chart; no audit of others. |
| The ships as code (§3.3) | Nowhere weighed (§4d) | The workflow was chosen and enlarged. |
| Performance | Earlier review §2.1 l.191-202 and §6 item 5: 800-1,000 ticks/s, "dearer at M6 than now" | "Not now" (decision 29). The review measures 480-650 and the 3,000 budget asserted unmet. **Grown worse.** |
| Sight across land, collision, settling halyards, the gybe | `NotesForM7.md` l.325-342, l.194-203, l.13-23, l.45-48 (the owner's, 2026-10-10 to 18) | None built (review F2.6, §1.3 M7 row). Known and wanted; left. |
| Specifications as histories | Earlier review §2.2 l.243-251 and §5 l.490-493 ("Stop appending 'as built'") | Not taken: every design note in this set ends in an "As built" postscript, and OneWorld step 11 writes "as built (package 84)" pointers into specs M6 and M7b (l.2069-2073). **Recurs** (review §5.4 last row). |
| The consent brief's "to come" | Earlier review §3 l.375-378 ("the brief says 'only the watcher exists today'") | Recurs as 17(d): the director built, the brief says "is to come". |

---

## 3. The method, as these records show it

- **Who writes, who rules.** The lead writes a brief in `docs/dev/M7-WorkPackages.md`; a builder
  session writes the note "before anything is built" (every note's first line); the lead rules at
  a "gate" (`Design-ShipBought.md` §13, `Design-Prizes.md` step 0); the owner answers numbered
  questions; postscripts per step say "Built as designed / Taken another way / Found on the way".
  The form is uniform and honest about departures.
- **What "green" meant.** OneWorld's steps: "the fast tier whole on its tree and the slow tier of
  the known truths, the trials and the files it touched" (l.1394-1396); Build-Ships §2.5
  (l.258-265): "each builder runs the fast tier once on its final tree and the slow tier of the
  files it touched ... The whole suite is the lead's". Step 1's proof was "pure delegation; the
  proof is the slow tier whole" (l.1139). Under that green the façade's readers were wrong for
  thirteen packages (84 to 97) and no station's act on a hull was journaled from step 6 to step 8.
- **A ruling put well** (`Design-SlaveryAndSuppression.md` §10, l.645-666): "Each answerable in a
  word or a line, the recommendation first", e.g. "Barbary ransom: redemption told as the
  captive's nation's act, its sum never charged to the purse ... (recommended), or the sum said
  from the sources?" The owner answered all nine in a day (§11).
- **A ruling put badly** (`Build-Ships.md` §19.1 item 7, l.2287-2289): "The engine's judgement
  figures (Ext §14 items 5-9): 'furl the mizen' furls it aloft; the settee's dip when the head
  yards' swing ends; its times and hands; the spritsails out of 'plain sail' and taken in first;
  lifts drawn on a lateen yard only." Also `Design-OneWorld.md` §5.2 item 6 (l.1375): "Whether a hull
  at anchor or in port may be awake (retiring `_NOT_CREWED_STATES`)": a code name put to a
  non-programmer.
- **Re-opened after merge, in these notes alone:** Prizes step 3 "mends from the owner's play"
  (l.1234-1247), step 4 "the pace mended at the resumption" (l.1272), step 6 "the lead's review"
  (l.1340-1349); B3.3 then B3.3b then "the review's mends (2026-11-09)" (`Build-Ships.md` l.2181);
  decision 29 of Build-Ships "*reopened*" (l.139); package 97 re-opening 84.
- **Process fault and remedy.** The earlier review's "a cold read of each specification before
  its packages are cut" (l.483-486) and "fewer places, not fewer words" (l.250-251) are not taken:
  the ships' build alone has a plan, a decisions sheet, five research notes, five design notes, a
  synthesis and ten scratch notes (§5).

## 4. The reviewer's particular asks

### (a) The earlier cold review, finding by finding

| Its finding (`ColdReview-2026-09-30.md`) | Owner's ruling (decision 29) | Now |
|---|---|---|
| `ship.extra` untyped bag (l.83-99) | consolidation: not now | 159 `ship.extra[` subscripts in `freesail/`. **Not mended.** |
| Boundary crossed three times (l.90-96) | not now | **Worse** (§2). Review head 4 F4.1. |
| `verbs.py` 2,167 and `scripts.py` 2,977 lines, split them (l.101-109) | not now | 3,248 and **9,095**. **Worse.** Review head 4 list. |
| `tend_sheets` free (l.112-118) | not now | **Mended** (32e). |
| Studding stall on the true wind (l.119-124) | not now | Still the true wind (`physics/sails.py:1011-1013`). Not mended. |
| Strain tuned to a narrative (l.124-130) | (none) | Not checked. |
| Determinism on one machine; a Windows job (l.132-145) | approved | Windows in `ci.yml:52`. The promise itself recurs (review §3.2). |
| Suite an integration suite; pins are change detectors; re-pin ritual (l.147-160) | two tiers approved | Two tiers built; the rest **recurs and grew**: 1,696 tests then, 8,138 cases now; 870 lines of re-pin comments in half one file (review 3.2). |
| Tests not proving their names (l.162-180) | (none) | **Recurs**, worse: 61 of 67 survived (review 3.3). |
| Pause at speed stands down in 48 s (l.182-189) | to be fixed | **Mended**: `WELFARE_UNATTENDED_REAL_S = 600` (`agents/harness.py:375`). |
| Performance (l.191-202) | not now | **Worse** (§2). |
| Consent identity a typed string (l.204-212) | not now | Not checked (outside these records). |
| Close-hauled three ways (l.216-225) | consolidation | **Recurs**: six points default (`evolutions/scripts.py:204`); review pillar 2 "every ship is treated as close-hauled at six points". |
| Documents drifted (l.227-241) | consolidation | `ThreeDimensions.md` mended (l.34-35). The general drift **recurs** (review §5.4, specs). |
| Specs become histories (l.243-251) | (none) | **Recurs** (§2). |
| Duplicates at boundaries (l.253-259) | consolidation | `_out_of_action` still twice (`api/readings.py:969`, `physics/strain.py:321`); `HALYARD_CLASSES` twice (`physics/sails.py:119`, `physics/strain.py:137`). **Recurs**, and head 4's F4.2 to F4.11 are the same disease larger. |
| M5b "three milestones in one coat" (l.385-406) | cut, gates lag | Gates lagged, then lapsed (review 5.2). The remedy for scope became the cause. |
| "The director is correctly sized as small" (l.438-439) | (none) | The earlier review **endorsed** the estimate the present review measures at 16,000 + 12,000 lines (F2.5). |
| "Budget M7 for the clearing and jury work, not the ballistics" (l.433-436) | (none) | M7 grew in every direction but the fine control and the jury work (review F2.6). |
| The `freesail` command (§6 item 9) | approved | Built another way: `py -m freesail` opens the harbour, which writes the client entries (`freesail/__main__.py:1-12`); no `[project.scripts]`. The packaging fault (decision 31) is new. |
| Verified checkpoint (§6 item 6) | approved (5b) | Built; the review's §5.4 first row is the hole in it. |

**On the four the reviewer asked for by name.** *Consolidation:* asked for "between milestones,
not inside one ... two days" (l.479-481); ruled not now; never done; everything it named is
larger. *Tests:* it named the cost and the pins exactly as the present review does, six weeks
earlier; only the tiers were taken. *The boundary:* three crossings named with lines and a
one-day remedy; now structural. *Scope:* it diagnosed one over-full milestone and prescribed
cutting it; the ruling ("gates lag the work") removed the brake for every milestone after.

### (b) Design-OneWorld: the cost foreseen against the result

The study costed **"about 4,000 lines touched and 2,000 moved in all, the size of package 70"**
(l.906-907), the pace "untouched by either" road (l.963-967), "the aim is none moved" for pins
(l.998), and named per-step risks of the kind "a property missed" (l.1139), "the order" (l.1218),
"the acts' keying" (l.1242). It did not cost a façade risk, because the façade it costed
delegates shared fields (l.559-568) and holds no "current hull". The swap was decided in the
building (l.1748). What that cost is in the history: nine shared readers wrong under the swap,
the privateer of the first action never firing, the player's guns firing on a struck ship
(l.1815-1847); three pins moved (l.1853-1860); no act journaled from step 6 to step 8
(l.1943-1946); package 97's eighteen readers "latent in every pin" (`Design-FacadeReaders.md`
l.24-25, l.39-73); a test passing only by the fault (l.180-182); and the `--ship` drift still open
(§1.1). The step 11 judgement that the swap "stands as it is ... the simpler contract"
(l.2062-2064) is the lead's, made on the pace alone. The review's "eight forms of a ship" and "the
fold between far and crewed" are the study's own §2.13 choices plus the names kept for the
unpickler (l.2097: `CrewedWorld`, `world` for a hull, `crew` for a hull in the tests).

### (c) Slavery: where the code keeps decision 68's rules

The note is a design only, dated 2026-11-12/13 (`Design-SlaveryAndSuppression.md` l.3, l.668),
answered by the owner; its building packages (l.699-730) are not begun.

| Rule (note l.14-19; decision 68, `DesignProposal.md` l.945-949) | Where kept |
|---|---|
| People never a cargo; nothing bought, carried or sold that is a person | **By the data alone.** A port's market is an open dict of whatever goods its file lists (`world/ports.py:403-442`); nothing refuses a person. One test, on Malta's files at five dates, asserts the goods hold none of `{"slaves", "slave", "captives"}` (`tests/test_known_truths.py:16614`). The note's own guard, a words table "with a test that no game string in it uses a word of the 'not used' list" (l.709-711), is not built. Port files carry decision 68's words in comments and `marks` (e.g. `data/ports/santa-cruz-de-tenerife.yaml:29`, `valletta.yaml:29`). |
| No price for a person but the bounty for freeing | No slaver, no bounty table (`slave_trade_bounty:` absent from `data/business.yaml`). Note: the prize court reckons **head money, £5 a head of the enemy's men** (`data/business.yaml:146`, `world/prize_court.py:237-243`), period-true for combatants and marked FROM MEMORY; decision 68's sentence "no money is reckoned for a person but the bounty" read literally forbids it. For the owner to say whether the sentence means the trade only. |
| No player and no model at a slaver's station | Kept by absence: no vessel of the trade exists in `freesail/`, `data/` or `tests/` (grep "slave" in `freesail/`: nothing). No guard waits for one. |
| A corsair's station only under a transparent brief | No regency cruiser exists (`data/nations.yaml:423`: "the regency's corsairs not modelled"). The general adversarial gate `ADVERSARIAL_SEATS_CONSENTED = False` (`world/seats.py:76`; `world/prizes.py:1121-1127`) would refuse a corsair captain's seat at war with a human's ship, but there is no corsair-specific refusal, and the §8.1 brief is not in the consent documents (as the note says, the owner's process). |

### (d) The ships workflow: what one ship costs

The method (`Plan-ShipsWorkflow.md`): six phases, research by five agents, the owner's round,
design "from two angles ... and judged", stage 0, builders in worktrees, review "by lenses",
"adversarial verification", truths, docs (l.13-17, l.74-169), on the owner's Windows machine,
"Nothing goes to GitHub" (l.186-192). Its estimate: "about 60 agents ... 15 to 30 million
tokens ... most of a day" (l.194-199). The record shows the plan of 2026-10-25, the synthesis of
2026-10-28 and the last dated work on 2026-11-10 (`Build-Ships.md`, `Design-Ship-Bilander.md`):
**sixteen days, not a day**; no actual agent or token count is recorded in these notes.

| | Research note | Design note | Generator module(s) | Tests | Total written | The generated ship file |
|---|---:|---:|---:|---:|---:|---:|
| The bilander | 840 (70 KB) | 1,826 (155 KB) | 2,616 (134 KB) | 2,119 (114 KB) | **7,401 lines, 473 KB** | 1,415 lines |
| her settee in the engine (shared) | (in `Research-ShipsEngine`) | (in `Design-ShipsEngineExtensions.md`, 2,363 lines) | `settee.py` 189 | `test_settee.py` 1,566 | | |
| The *Indefatigable* (64 and razee) | 1,316 (96 KB) | 1,356 (106 KB) | 5,085 + `mizen_yard.py` 322 + `spritsail_yards.py` 169 | 2,959 (163 KB) | **11,207 lines, 657 KB** | 3,896 + 4,546 lines |

Beside them `Build-Ships.md` (2,448 lines, 261 KB) and `Decisions-ShipsRound2-2026-10.md` (821).
**Two-thirds of `docs/design/` by bytes is the ships**: 1.79 MB of the top-level files plus
0.71 MB in `ships-design/`, of 3.74 MB. **No design note weighs this against the proposal's
"ships are data files, not code"** (grep of every note for "data file", "by hand", "§3.3",
"DesignProposal": the only hits forbid hand edits, `Build-Ships.md` l.29-30, l.622, l.1241). The
plan made the per-ship module a "structural decision, the lead's", because "the generator is one
8,000-line file today, and parallel builders in it would collide" (l.111-114): an argument from
parallel building, not from the player. The review's §3.3 verdict stands, and the record shows
it was never put to the owner as a choice.

### (e) Decisions sampled against the code (three notes, five each)

**`Design-Signals.md`:** (1) the lookout gives the nation *shown* (l.40-41): kept
(`world/lookout.py:824, 998, 1102`, `nation_shown`). (2) The private table a pure function of
the seed, not saved (l.442-443): kept (`world/signals.py:497`). (3) A brief's `limits:
{false_colours: false}` refuses the ruse (l.407-408): kept (`agents/director.py:292, 342`).
(4) Fog signals kept while another sail was in sight in the hour (l.474-476): built, but the
review's planted fault "ships never making fog signals" survived 7-147 and 7-150 (review 3.3).
(5) The far form `shake out the reefs` refused by the near dialect, "reported to the lead"
(l.641-643): the three books still carry `does: {order: "shake out the reefs"}`
(`data/signals/britain/numerary.yaml:104` and Spain's, the United States'); whether the grammar now
takes it (`orders/grammar.py:824-826` reads "reefs" as all) not settled by me.

**`Design-Squadrons.md`:** (1) `weather_bound` a top-level key (l.503-508): kept
(`world/scenarios.py:735-738`). (2) The set's pace the slowest member's: kept
(`world/squadrons.py:22, 75`). (3) `in company` doctrine in each role's file, not code: kept (ten
`data/captains/*.yaml`). (4) The business follows the player's ship across regions: present
(`world/business.py:319`), not tested by me. (5) The blockade blown off "to its lee rendezvous":
the review reproduced it steering for the Black Rocks (F2.8); the as-built note reads "the
plural to Brest's" Black Rocks (l.527-529): the decision held in data and broke in behaviour.

**`Design-Prizes.md`:** (1) The far ship's synthetic reply a fallback only, counted (step 0
ruling 4): kept (`combat/far_action.py:70`). (2) The adversarial seat behind a flag (ruling 8):
kept (`world/seats.py:76`). (3) Head money FROM MEMORY and marked (ruling 3): kept
(`data/business.yaml:146`). (4) The captive's channel built (step 3, l.1214): built, but the
strike's own line says it is not (§1.1 item 3). (5) `struck to` "doubted after the first minute"
(l.1356): built, and under the gentlest brief it went through (review decision 14).

## 5. The cost, and the record as a record

- **The size of the records against the work.** One package (75) has a plan, a decisions sheet,
  five research notes, five ship designs, an engine design, a synthesis of 261 KB and ten scratch
  notes: some 2.5 MB. One table cell of `Build-Ships.md` (§16.1, l.2181) is about 6,000
  characters. Nobody will read it twice.
- **Current against history.** Each note's head says "Nothing ... is built yet" and its foot says
  what was (Prizes l.17-18 against l.1147-1367; OneWorld l.3-5 against l.1390). A reader must read
  to the end to know the state. `Design-ShipBought.md` is a note of 1,151 lines for a package
  that does not exist, booking a fault the reader can reproduce today.
- **Honesty.** High, and even about the lead: the lead's own reproduction of the drift
  (ShipBought l.1125-1129); "taken another way, with the reason" everywhere; OneWorld step 6 says
  plainly that the swap broke the first action and the struck-ship fire. What the records leave
  out: actual hours, agents and tokens for the ships against the plan's estimate; any line that
  weighs a finding of the earlier cold review after its ruling; any register of the faults booked
  to unbuilt packages.

## The ten things that matter

1. **A known fault, reproduced by the lead, booked to an unbuilt package, still live**: the
   followed ship's far body 3.7 km behind in 20 minutes (`Design-ShipBought.md` l.926-938,
   l.1125-1129; my run at 504a250). The review should add it to F2.8.
2. **The earlier cold review named the boundary, the duplicates, the two big files, the tests'
   meaning and the performance six weeks before; each "not now" grew** (`ColdReview-2026-09-30.md`
   l.83-109, l.147-202, l.557-564; `DesignProposal.md` l.614).
3. **"Gates lag the work" was the remedy for one over-full milestone and became the loss of the
   brake** (decision 29, `DesignProposal.md` l.614; earlier review l.385-406).
4. **The façade built is the inverse of the façade costed**; its faults were latent under every
   green suite for thirteen packages (`Design-OneWorld.md` l.559-568 against l.1748-1762;
   `Design-FacadeReaders.md` l.24-25, l.180-182).
5. **Ships: 7,400 to 11,200 lines written per ship, two-thirds of the design records, sixteen days
   against "most of a day", never weighed against "ships are data files"** (`Plan-ShipsWorkflow.md`
   l.111-114, l.194-199; §4d).
6. **Decision 68 is kept by absence and by one test on Malta's markets**; the guard the note
   designs is unbuilt; head money is a price on a person by the letter of the decision
   (`tests/test_known_truths.py:16614`; `data/business.yaml:146`).
7. **The review should narrow two findings by ruling**: the browser's map and ship view
   (`Design-PlaceKnowledge.md` l.413-420, l.662-664) and `struck to` as a designed director's form
   (`Design-Prizes.md` l.1353-1357).
8. **The far world's sky is the player's by a knob deferred to M8**, though the study promised the
   mend at step 6 (`Design-OneWorld.md` l.1308-1312, l.1790-1791).
9. **"Green" was the fast tier plus the touched files' slow tier; the whole suite the lead's**
   (`Build-Ships.md` l.258-265); a truth never ran because its world had no place on the chart
   (`Design-Prizes.md` l.1272-1277).
10. **The record cannot be read for the state today** without reading every postscript; specs and
    notes stayed histories after the earlier review asked them not to (earlier review l.490-493;
    OneWorld l.2069-2073).

## What I did not read

Of the 56 files: whole or in part only those listed at the head. Not opened (sizes in bytes):
`Design-Ship-PrinceDeNeufchatel.md` 214,507 (her design); `Research-74-2026-10.md` 203,426 and
`Design-Ship-Bellerophon.md` 179,972 (the 74); `Design-ShipsEngineExtensions.md` 182,168 (settee,
lateen, bowsprit yards, driver); `Design-Ship-Bilander.md` 154,725 (head only);
`Decisions-ShipsRound2-2026-10.md` 110,961 (the owner's ship rulings); `Design-Ship-Indefatigable.md`
105,844; `Research-Indefatigable-2026-10.md` 95,948, `Research-PrinceDeNeufchatel-2026-10.md`
78,200, `Research-Bilander-2026-10.md` 70,237, `Research-ShipsEngine-2026-10.md` 68,682 (sources
per ship); `Build-PracticeAndResupply.md` 80,665 (practice firing and resupply synthesis);
`Design-BoatAndPersonAboard.md` 69,278 (package 82); `VesselReferences-2026-10.md` 51,081 and
`VesselReferences-2026-11-Spanish.md` 12,215 (draughts found); `Design-ViewerAction.md` 47,150
(guns, flags drawn); `Design-WaterAndHealth.md` 46,773; `ChartData.md` 40,827, `Navigation1805.md`
40,482, `WeatherSystems.md` 40,441, `Tides1805.md` 29,250 (milestone 5 studies);
`Design-WorkInAction.md` 15,577; `Proposal-MagazineResupply.md` 15,030, `Proposal-PivotGun.md`
11,189, `Proposal-PracticeFiring.md` 9,831; `Design-DoorAndVisitor.md` 14,965; `VesselCandidates.md`
14,453 (wish list); `Design-SailByName.md` 12,506; `ConsentRevision-AdversarialSeats.md` 8,927
(the draft for the owner); `Scenario-StrikingColours.md` 5,904; `ThreeDimensions.md` 5,458 (l.28-36
only); `Papers-and-Books.md` 3,282; `ships-design/` (ten files, 711,728: code maps and page notes).
Not checked: the consent identity item, the repeat detector's digest under live weather, the
strain constants, whether the grammar now takes the signal books' `shake out the reefs`.
