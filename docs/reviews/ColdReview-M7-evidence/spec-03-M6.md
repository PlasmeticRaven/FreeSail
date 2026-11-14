# Spec reader 03: TechnicalSpec-M6 (officers and captains) against the code

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. I read `docs/TechnicalSpec-M6.md` whole
(2,301 lines). Against it I read `tools/regatta.py` whole, `data/regatta/*.yaml` whole,
`tests/test_parity.py` whole, the parts of `tests/test_regatta.py`, `tests/test_captains.py`
and `tests/test_crews.py` named below, `freesail/agents/seat.py` (lines 1-170 and 440-570),
`freesail/agents/tools.py` `submit_order` and `judge` (754-1050), the `Pace` class of
`freesail/ui/console.py` (348-436) with its docstring and `_handle_line`, `harness.open_samples`,
the head of `freesail/world/crews.py` (1-135), `tools/pace.py`'s docstring, `data/captains/
merchant.yaml` whole, and of `freesail/world/captains.py` (4,795 lines) lines 1-520, 925-1065,
1234-1525, 1816-2215, 2586-3055, 4024-4062, 4318-4340 and 4514-4795, with greps over the
rest. I ran no test. I ran three short python commands (each under fifteen seconds, with
`PYTHONDONTWRITEBYTECODE=1`, writing nothing): the doctrine files checked against the code's
names, a regatta course run for half an hour of ship's time, and a search for doctrine keys no
code reads. The model and vendor names of the specification are left out of this file.

Weights: high, medium, low. Confidence: sure, likely, suspicion.

## 1. The commitments, one by one

| § | what the specification says is built | verdict | where it lives (file:line) | how you know |
|---|---|---|---|---|
| 2 | Wardroom files per ship, stations bound by data, `People.holder` | built as specified (more ships than four) | `data/people/*.yaml` (12 files); `freesail/world/people.py` `holder` | `ls data/people`; grep `def holder` |
| 3 | Captain's station with the player's whole surface (every verb, every level) | built as specified for verbs | `freesail/agents/tools.py:919-1049`; `tests/test_parity.py:225-243` | read `judge`; the parity test asserts every vocabulary verb but the driver's passes `CAPTAIN_DOMAIN` |
| 3 | Silent captain's door lends the deck to his book; rules stand in | cannot tell beyond the names | `Harness._lose_deck`, `_sync_captain` exist | grep only; behaviour not read |
| 3 | Player's seat at lesser stations, judged "as a model's at the station would be" | built otherwise | `freesail/agents/seat.py:450-538` | `route` calls `self.submit(line)` with no `danger`; no console or server line passes one (grep `danger` in `ui/console.py`, `ui/server.py`: none). A model officer has `submit_order(text, danger=...)` (`tools.py:754`); the human officer has no road to the way out of danger |
| 3 | The player may take any station on any ship (ruling 1) | built (since M7) | `freesail/agents/seat.py:90` keeps captain out of `SEAT_STATIONS`, but `--seat captain --ship` is a driver's road (`ui/console.py:1048`; `tests/test_known_truths.py:13138`) | grep. §20's "Left undone" is overtaken |
| 4 | Intent read from words (trade, station, letter, home, passage; fish added) | built as specified | `captains.py:710-790` regexes, `INTENT_KINDS` :155 | read |
| 4 | Plan "derived at sea, never written in advance", over the chart's data | built in part | `captains.py:1234-1506` | the planner is a geometric shortest path over marks and common tracks; wind never enters it; only `channel-west.yaml` carries common `tracks:` (grep over 40 features files); §26 itself says "the planner routes nothing (a `via` lays the marks)" |
| 4 | Behaviour: a state machine whose states are books in the dialect | built in part | `captains.py:2703-2735` (`_enter` loads the book); `_on_enter` :2887-2978 and `_work` :2984-3054 in code | of ten doctrines with books, `in port`, `in distress` are empty in all ten, `chasing` in seven, `investigating a stranger` and `keeping station` in six (python count). Those states' behaviour is code, not book |
| 4 | Engaging present from the start, empty until M7 | overtaken (M7) | `captains.py:4163-4415` (`_engage_now`, `_engaging`, `_musketry`, `_boarding`, `_damage_work`) | read the outline; filled by packages 70-74 |
| 4 | Transitions as data rows, fired on perceived stimuli, once a minute | built as specified | `captains.py:1973-1991`, `JUDGE_EVERY_S = 60` :167; doctrine rows e.g. `merchant.yaml:231-280` | read; every `on`/`unless` in the eleven files names a stimulus in `STIMULI` (python check) and `tests/test_captains.py:101-103` holds it |
| 4 | Stimuli defined by data | not built (by design of the spec) | `captains.py:2013-2147` | the meaning of every stimulus is a branch of `_stimulus`; data can only re-wire rows and move thresholds |
| 4 | Doctrine thresholds as data, "the owner tunes it with a text editor" | built in part | `data/captains/*.yaml`; constants `captains.py:381-495` | 12 of 73 threshold keys are read by nothing in `freesail/` (python search, confirmed by grep): `road_cables`, `leg_reached_nm`, `anchor_within_nm`, `stranger_chase_nm`, `station_wear_hours`, `spell_minutes`, and six prize keys (`burns_when`, `divide_prisoners`, `fit_least`, `prisoners_most`, `worth_least`, `mans_prizes` named only in a comment). The figures actually used for those are code: `ROAD_CABLES = 3.0` :381, leg radii 2.0/0.6/1.5/0.4/0.5 hard-coded :1267-1274 and :1462, :1474, :1484 |
| 4 | Judgements' figures "in `captains.py` with their source in the tuning notes" | built as specified | e.g. `captains.py:4037` `purse * 0.95`; `OFFING_NM`, `DANGER_BERTH_NM` :391-392 | read. This contradicts "doctrine as data": the spec itself splits the figures between files the owner tunes and code he cannot |
| 4 | Doctrine roles: King's ship, merchant, packet, commodore (+cruiser, fisherman) | built, grown to eleven files | `captains.py:137-151`; `data/captains/` | `ls`; `merchant`, `prize-master` and `indiaman` books and transitions are copies (diff of `books:` onward: identical for prize-master, a comment line apart for indiaman); no inheritance, so a fix is made three times |
| 4 | Perception on the player's terms; "nothing in `captains.py` reads the world's truth"; a test greps for every road | built otherwise | `captains.py:4556-4559` (`getattr(self.world, "position")`, `v.position`), `:4576-4579` (`getattr(world, "vessels")`), `:4326-4335` (the enemy's fit company counted from her crewed body), `:4520-4532` (`struck` read off the vessel) | read. The grep test `tests/test_captains.py:276-294` looks for the literal strings `world.position` and `world.vessels`; the `getattr` spelling passes it. Added by M7 packages 73-74 in M6's module |
| 4 | Perception at far detail | built otherwise (declared) | `brains.perceive_vessel` | spec §4 (package 43) says the far captain perceives "from the vessel's own truth". Decision 40's "perception on the player's terms" holds for the near body only |
| 4 | Rule of the road as 1805 had it: starboard tack close-hauled stands on, larboard gives way, running keeps clear | built in part | `captains.py:4676-4712`, `_road_rule` :4763-4782 | read. No crossing is judged: any stranger within three cables whose course the lookout's words give triggers it, whether converging, diverging or overtaking. The only give-way is "bear away two points", whatever the geometry. Two ships neither by the wind both "stand on". Said once an encounter, never re-judged. Reach is `ROAD_CABLES`, not the doctrine's `road_cables` |
| 4 | Rule of the road: "a cheap check of crossings between plans at far detail" | not built | `freesail/world/brains.py` | grep `cross\|road` in brains.py: no crossing check |
| 4 | Rule of the road proved in play (gate 6a item 1: "the rule of the road at a few cables") | not built (untested) | `tests/test_captains.py:380-399` | the only test is of the arithmetic (`_tack_and_point`, `_road_rule`); grep for the line kind `captain.road` in `tests/`: no hit |
| 4 | One brain, two bodies (`Judgement` shared, `FarCaptain` the far body) | built as specified | `captains.py:1858`, `brains.py` | read the class head; `fold_in` exists |
| 4 | Floor: `merchant-intent.yaml` trades by rules alone | cannot tell | `data/scenarios/merchant-intent.yaml` exists | not run |
| 4 | Captain's trials (five scenarios) | built (files present) | `data/scenarios/trials/` (five files) | `ls`; tests not run |
| 4 | Player's hand: an order of the ship's makes the captain stand aside until `captain: carry on` | cannot tell beyond names | `captains.py:2487-2522` (`player_hand`, `carry_on`) | grep |
| 5 | Officer's own reckoning: `work my reckoning`, `my reckoning is`, slate as data | cannot tell beyond names | `reckoning.SLATE_BOARDS_KEPT = 48` (`reckoning.py:615`), `UNLOGGED_KINDS` in `core/world.py` | grep; behaviour not read |
| 6 | Primer chapter 18, lesson scenarios | built (files present) | `docs/primer/18-lessons.md`; `data/scenarios/lesson-*.yaml` (four) | `ls` |
| 11 | Stations bound at run time (`bind`, `unbind`), doors ask by name | built (names) | `freesail/world/stations.py:243, 293` | grep |
| 11 | Master's, lookout's, passenger's stations | cannot tell beyond names | `agent.LOOKOUT_PATIENCE_S` (`agent.py:1823`) | grep |
| 11 | Stand-by on several conditions | built (names) | `harness._read_stand_by` | grep |
| 12 | Pace rule the default: 1x while any model's sample is open | built as specified | `ui/console.py:348-393`; `harness.open_samples` `harness.py:5442-5463` | read: `rate()` returns 1.0 when any open sample is named, set compression otherwise; a `Playback` never counts |
| 12 | `--lockstep` a separate option; `--free-running` new | built as specified | `pace_rule_of` `console.py:428-435`; server flags `ui/server.py:5, 84` | read |
| 12 | Log says when the clock is held longer than a stated time | built as specified | `PACE_HELD_SAID_S = 120.0` `console.py:345`, `driver.pace` :386 | read |
| 12 | Pace rule lives in the drivers, World tick untouched | built as specified | `Pace` is a console object asked by both drivers | read; it is the drivers' rate only |
| 13 | API door: key from the credential store, environment, file outside the repo; refuses to start where the key would be written | built (names and tests present) | `freesail/agents/api.py:60-63, 139, 226`; `tests/test_api_door.py:71, 121, 284` | grep; not run |
| 13 | Image tools at image-capable doors, drawn by the open page | cannot tell beyond names | `ui.server.Easel`, `pictures.SPANS` | grep |
| 14 | Station acts journaled as inputs; replay by acts on a build whose sampling differs | built (tests present) | `core/acts.py`; `replay.road_of`; `tests/test_known_truths.py` truth 85, `tests/test_replay.py::test_five_stations_...` | grep; not run |
| 15 | Consent brief revised once, watched sections pinned | built (test name present) | `tests/test_officer.py` `WATCHED_SECTION_DIGESTS` | grep. The "once" was broken by 42b (a second revision), as the spec records |
| 19 | Range and cap "chosen from a measurement, not guessed" | built in part | `crews.py:85-99`; `tools/pace.py` | `CREWED_NM = 4.0` is justified in the code by the lookout's rig distance (`RIG_MADE_OUT_NM`), not by the measurement; `CREWED_DEMOTE_NM` by "half an hour's sailing"; only `CREWED_CAP = 3` is argued from ticks a second. The measurement itself is in `docs/dev/TuningNotes.md`, which I may not read. The cap was measured when a crewed ship was "a World of her own" (§19, package 43); package 84 made her a `Hull` of one World and the code does not say the cap was measured again for the cap order and `HELD_OVER_CAP = 2` (`crews.py:106`), which lets five hulls be awake |
| 19 | Truth 88: with the cap full the pace holds | built in part | `tests/test_crews.py:193-217` | marked `pace`, run only alone (`pyproject.toml:46`; `.github/workflows/release.yml:58`); the frigate is hove to (the cheaper body) and the three brigs merchant brigs; the docstring says "100 to 114 measured", the module head (`crews.py:94`) "about 140": one measurement, two figures |
| 19 | Promotion range and cap a setting after the gate (`crewed: {cap, range_nm}`, flags) | built as specified | `crews.py:755-798`; `ui/console.py:1173-1205`; `ui/server.py:1770-1823` | grep and read |
| 19 | Fisherman never crewed (`FAR_ONLY_ROLES`) | overtaken | `crews.py:120-126` (empty since package 56) | read |
| 19 | Demoted at anchor or in port | overtaken | `crews.py:112-119` (`_NOT_CREWED_STATES` empty since package 84) | read |
| 19 | Far-detail guard: a captain's plan across the land refused; a goal's straight leg only a warning | built as specified (names) | `ships.land_crossing` | grep |
| 19 | World's business (traders, fishermen, cruisers drawn under the seed); no price moved by cargo | cannot tell beyond names | `freesail/world/business.py` (1,316 lines), `data/business.yaml` | not read |
| 19 | Truth 87: promoted brig sails the far body's track within tolerance | built in part | `tests/test_crews.py:154-190` | tests easting only, on one point of sail (east before a westerly); docstring says a mile, comment says a mile, assertion allows 1.5 |
| 19 | Lugger and smack from the generator | built (files present) | `data/ships/lugger.yaml`, `smack.yaml` | `ls` |
| 20 | Model captain of another ship, `--station captain --ship` at three doors, far shape | built (flags present) | `mcp_server.py:1410`, `local.py:1456`, `api.py:1069`; `crews.station_world`, `submit_far`, `FAR_SHAPE_WORDS` | grep |
| 21 | Regatta harness: course file, judge from truth, score columns, agents rules/fake/local/api/replay | built as specified | `tools/regatta.py:155-593` | read whole; ran course one under `rules` for 1,800 s of ship's time: it loaded, sailed and scored (`finished False, miles_to_go 95.2, damage [], groundings [], fatigue 0.005, purse 0.0, lines 70`), the captain "kings-ship; bound for Falmouth; on passage" |
| 21 | Every agent runs at lockstep | built otherwise | `regatta.py:469-477, 571-587` | rules and fake answer within the tick; a door's model holds the clock as long as it likes; the human's `replay` was played at the console at any pace, with `hold` |
| 21 | Refuses a model whose consent is not on record | built as specified | `regatta.py:528`; `remote.py:454, 620` | read |
| 21 | Human replay agent | built, unguarded | `regatta.py:439-457` | checks seed and scenario only; a human's `world:` order (weather, ship, mark: `world/orders.py:125-149`), live at the console and journaled, is replayed and judged as a fair run |
| 21 | First table under `docs/playtests/regatta/2026-10-16/` | cannot tell | | the folder is under `docs/playtests/`, which I may not open |
| 21 | The courses: Ushant to Falmouth, Falmouth to Bertheaume, Falmouth to Funchal | built as specified | `data/regatta/*.yaml` | read: three files, seed 7, limits 30, 40 and 384 hours; only the Funchal course has marks (Ushant, Finisterre); the fake's orders are hand-written routes (`shape a course for ... via` four positions) |
| 22 | Parity: every reading the console answers the station answers the same | built in part | `tests/test_parity.py:196-221` | the test compares `world.submit(asked)` with the station's `submit_order`, both of which end in `World.submit`; the console's own `handle_line` is not the left side, so the comparison is near tautological for readings; `Console._handle_line` intercepts (`console.py:603-680`) are covered only by the separate command list |
| 22 | Parity: every verb, filtered only by authority | built as specified for the captain | `test_parity.py:225-243` | read |
| 22 | Parity for the other stations (officer, master, lookout) against the player's seat there | not built | | no test seats the player and a model at the same lesser station; the `danger` gap above is the result |
| 22 | Truth 91: same ten orders, same log | built as specified | `test_parity.py:355-390` | read; compares the order lines by kind only and drops the stores' answers by design |
| 23 | `seat:` and `unseat:` world orders, the director's budget | built (names) | `world/orders.py:451-470` | grep |
| 26 | Chart corridor; widening to 32 W "held uncommitted for the owner's word" | built otherwise | `git ls-files` shows 48 corridor tiles committed; `data/charts/manifest.yaml` corridor `west: -32.0` | the document is stale here |
| 27 | Compression to 1000 | built as specified | `MAX_COMPRESSION = 1000.0` `console.py:95` | read |
| 29 | Not done: combat, the director, Mediterranean beyond the Strait | overtaken | combat in `captains.py`, `freesail/combat/`; director `agents/director.py`; Mediterranean blocks recorded in §26 itself | ls and the spec's own §26 |

## 2. The pointers

I checked 36 names the specification points at (grep for the definition under that name, and
for the numbers below, the value): `People.holder`, `agent.voyage_words`, `Harness._lose_deck`,
`Harness._sync_captain`, `fake.captain_of_the_ship`, `captains.station_off`,
`Captain.player_hand`, `Captain._tide_serves`, `hull.helm_mark_staggered`,
`navigation.CHASE_LEAD_MAX_DEG` (70), `CHASE_CROSSED_DEG` (45), `Captain._stream_changed`,
`reckoning.SLATE_BOARDS_KEPT` (48), `core.world.UNLOGGED_KINDS`, `stations.Binding`,
`agent.LOOKOUT_PATIENCE_S` (a watch), `harness._read_stand_by`, `console.PACE_HELD_SAID_S` (120),
`api.refusal_to_start`, `replay.road_of`, `crews.CrewedWorld`, `crews.station_world`,
`business.Business`, `remote.Desk.on_record_only`, `agent.session_kind_of`,
`ships.land_crossing`, `FarCaptain.fold_in`, the truths 77-91 tests,
`test_five_stations_of_the_wardroom_replay_...`, `WATCHED_SECTION_DIGESTS`, `ui.server.Easel`,
`pictures.SPANS`, `crews.submit_far`, `crews.FAR_SHAPE_WORDS`, `STORM_CANVAS_APPARENT_KN` (70),
`COARSE_CELL_M` (300), `BOX_BLEND_H` (6), `CENTRE_STEP_KM` (500), `SEARCH_HEIGHT_M` (300),
`GATHERED_WAY_KN` (1), `MAX_COMPRESSION` (1000).

All exist under the names and the numbers match. `captains.resolve_state` is not a definition
in `captains.py` but is reached by the module `__getattr__` (`captains.py:4787-4795`), as the
spec says. Pointers whose description no longer holds: `crews.CrewedWorld` is now only "the
unpickler's name for a checkpoint of before" (`crews.py:11-12`), not the crewed body;
`FAR_ONLY_ROLES` and `_NOT_CREWED_STATES` exist and are empty; `FAR_DETAIL_STATES` is three
states (`captains.py:193`, "in company" added), where §4 says two; `doctrine road_cables` is
in every file and read by nothing. Count: 36 hold by name; 4 hold by name and not by what the
spec says of them.

## 3. The numbers

- Regatta limits and radii (30 h / 1.5 nm; 40 h / 3 nm; 384 h / 1.5 nm): in the course files and
  read by `load_course`; held by `tests/test_regatta.py:64-79` only for presence. Truth 90
  (`test_regatta.py:426-444`) holds the rules captain to finishing course one within 30 h with
  no grounding or damage; its assertion on the fake, `fake["finished"] or fake["miles_to_go"] >
  0`, holds nothing. I sailed course one for half an hour only.
- Crewed range 4 nm, demotion 6 nm (two miles of hysteresis), cap 3, floor 60 ticks a second:
  in `crews.py:90-99`; the floor is held by truth 88, a `pace` test run alone.
- "Twelve crewed ships near fifty ticks a second", "560 alone", "140 with three": not checkable
  without `tools/pace.py`, a long command; not run.
- Captain judges every 60 s after 300 s: `captains.py:167-168`. Rule of the road at 3 cables:
  `captains.py:381`. Pace hold said after 120 real seconds: `console.py:345`.
- Truth 87's tolerance: the spec says "within the stated tolerance"; the test states a mile and
  asserts 1.5 miles of easting.

## 4. The open items

Deferral phrases in the document: 24 by a grep for "not built", "left undone", "left:", "later
milestone", "is M7's", "M7b's", "M8's", "for a package of its own", "uncommitted" and kin. The
lists, item by item:

- §4, "Not built" (45): the Goulet by the pilot's conn; later built (45c and 58b, as the spec
  says). The station's circle through the land met by the offing line, not a mark: still open
  as far as I can tell (not checked). The frigate aback by turns after a gale: package 88's
  `_aback_with_no_way` (`captains.py:3056`) answers it, apparently.
- §4, "for a package of its own" (40c): the ship aback in a gale and `shorten sail` with the
  headsails: cannot tell.
- §13: the pictures "in 41 or 42": built (42, 45).
- §19: the world's business, lugger and smack "43b's": built (files present). The true supply
  and demand loop, "a later milestone's": still open (no price moved, by the spec's word; not
  checked). The vectorised hot loop: still open.
- §20, "Left undone": the player at `--seat captain --ship`: built since (truth 7-322). A save
  replaying only the parent's stations: overtaken by package 84 (`hulls` in the save), as the
  spec's own later note says.
- §26: "the planner routes nothing", "the blocks' ports want their tracks", "the regatta's
  course is still to be sailed whole": the first still open (wind never enters the planner);
  ports with `tracks:` are 82 of 121 (grep), so the second is mostly done; the third cannot
  tell (the table is under `docs/playtests/`).
- §26: the corridor's widening "held uncommitted": committed (48 tiles in git).
- §29, not done: combat, the director, the Mediterranean: all since built in M7 and M7b.
  Individual hands as people, the carpenter's, gunner's and surgeon's stations: not checked.
- §30, carried from M5: the far-detail leg across the coast (built in 43 as a warning for a
  goal's leg, a refusal for a captain's plan); the pumps and the well (built in M7,
  `world/water.py`); the plain `steer` through the wind (built: `navigation.py:481, 554`); the
  platform difference (item 24), the datum offsets at three ports, the hints of 37l: cannot
  tell; 140 port files still say `datum: unverified` (grep). The roach of the square sails: not
  built (no `roach` as a word in the code or the sail model; the only hits are one ship's
  headsail notes).

Nine of the items I could judge are built, four still open, and the rest I cannot tell. The
milestone left fewer loose ends than the document's length suggests, but the document does
not mark which of its own deferrals were closed later.

## 5. The document as a document

- It is a history, not a specification. Of 2,301 lines, the "As built (package N, date)"
  paragraphs are the bulk; rulings are dated and attributed to the owner and the lead;
  package numbers run from 38 to 101. A newcomer could not build the rules-based captain from
  it: the state machine's work per state, the stimuli's meanings and the planner's radii are
  in code and described only as a narrative of trials that went wrong.
- It is not frozen at the milestone. §26 records chart blocks of M7 (79b, 79c, 79d, 93, 101,
  dated up to 2026-11-10) under a heading dated "Draft of 2026-10-09". §19 and §20 carry
  "As built since package 84" notes. The engaging state, empty "until M7", is not marked as
  filled.
- It contradicts the code in at least six places: the corridor "held uncommitted" (committed);
  the fisherman "never crewed" (crewed since 56); demoted at anchor (not since 84); "Nothing in
  `captains.py` reads the world's truth" (it does, `captains.py:4326, 4556, 4576`);
  `FAR_DETAIL_STATES` two states (three); "the player at `--seat captain --ship`" left undone
  (built).
- It contradicts itself: §15 says the consent brief is revised "once ... on the owner's
  condition that it is not put again at the milestone's end", then records package 42b's
  second revision. §4 says the doctrine is "as data ... the owner tunes it with a text editor"
  and, a page on, that each judgement is "a rule with its figures in `captains.py`".
- It gives `docs/dev/TuningNotes.md` as the home of every measurement it relies on
  (the cap, the pace, the trials' figures), so the specification's numbers cannot be checked
  from the specification and the code alone.

## 6. What the specification never asked for, and what it needed and did not get

Grown outside the plan, in the areas this spec covers: eleven doctrine roles (privateer,
prize-master, indiaman, revenue, a hail table) where four or five were asked; the whole
engagement, boarding, musketry, pumps and prize-taking in `captains.py` (about 600 lines from
4163), which is M7 work landed in the M6 module and is where the truth leaks are; a seventy-four,
sixty-four, razee and others in `SIZE_RANK` (`captains.py:296-321`); `HELD_OVER_CAP`, a cap
allowance for model-held hulls (`crews.py:100-106`); the director's seat at the player's
`--seat director` (`seat.py:87`).

Needed by its own logic and not written or built:

- A definition of a crossing for the rule of the road (closing bearing, closest approach);
  without it the "reflex" fires on any ship within three cables.
- A doctrine schema check: thresholds the code never reads are accepted silently, so the owner
  may tune `road_cables` or `leg_reached_nm` and nothing changes.
- A parity test for the lesser stations against the player's seat at them, which ruling 1
  makes a requirement and which would have caught the missing `danger` road.
- A rule for what a human's regatta save may contain (no world orders, no reload to an earlier
  tick), since the human at the prompt is also the owner.
- Shared doctrine (inheritance or includes): three roles are copies.

## The ten findings that matter

1. **The rules-based captain reads the world's truth, and the test that says he cannot is
   evaded.** `captains.py:4556-4559` takes `getattr(self.world, "position")` and the prize's
   true `v.position`; `:4576-4579` reaches `world.vessels` by `getattr`; `:4326-4335` counts the
   enemy's fit men from her crewed body before boarding. `tests/test_captains.py:280-294` greps
   for `world.position` and `world.vessels` as literal strings, which the `getattr` spelling
   escapes. Breaks §4's and decision 40's perception rule. High; sure.
2. **Parity is not whole: the human officer has no way out of danger.** A model at the
   officer's station may give `submit_order(text, danger=...)` (`tools.py:754, 1036-1048`);
   `PlayerSeat.route` calls `submit(line)` with no danger and no console or browser line
   supplies one (`seat.py:450-472, 507-538`; grep). The parity tests cover only the captain's
   station against the console (`test_parity.py`). High; sure.
3. **The rule of the road is a reflex without a crossing, and untested in play.**
   `_rule_of_the_road` (`captains.py:4676-4712`) acts on any stranger within three cables whose
   course the lookout names, gives only "bear away two points", lets two ships neither by the
   wind both stand on, and never judges again; the far-detail crossing check is not built
   (brains.py); no test asserts a `captain.road` line (grep). Medium; sure.
4. **"Doctrine as data" is half true.** Transitions and most thresholds are data; the meaning of
   every stimulus, the work of every state (with `in port`, `in distress` empty books in all ten
   doctrines and `chasing` in seven) and the planner's radii are code. 12 of 73 threshold keys
   are read by nothing, among them `road_cables` and `leg_reached_nm`, whose real values are
   constants (`captains.py:381, 1267-1274`). Medium; sure.
5. **The crewed range was not chosen from the measurement; the cap's measurement predates the
   architecture it governs.** `CREWED_NM` is argued from the lookout's rig distance and the
   demotion from half an hour's sailing (`crews.py:85-91`); only the cap is argued from ticks a
   second, measured when a crewed ship was a World of her own, before package 84; truth 88 runs
   with the frigate hove to and its docstring and the module disagree on the figure (100-114
   against about 140). Medium; likely (the measurement is in docs/dev, unread).
6. **The regatta runs and scores today**, under the rules' seat on its course: I sailed course
   one for half an hour and it produced a row (`tools/regatta.py`). But it is not one contest at
   one pace: the rules and fake answer within the tick, a model holds the clock without limit,
   and a human's save is accepted on seed and scenario alone, world orders included
   (`regatta.py:439-457`). Truth 90 asserts nothing of the fake (`test_regatta.py:441`).
   Medium; sure.
7. **The planner is not the passage planner of decision 40.** It is a shortest path over marks
   with an offing, blind to the wind; one region of forty has common tracks; the spec's own §26
   says "the planner routes nothing". The behaviour is not a fixed route, which is what decision
   40 forbade, but the "plan" layer is thin. Medium; sure.
8. **Pace rule and lockstep are built as specified**: `Pace.rate` returns 1x while any model's
   sample is open, lockstep holds for the door with the floor, free-running is a flag, the long
   hold is logged once (`console.py:345-435`; `harness.py:5442-5463`). Sound. Low; sure.
9. **The specification is a running diary that is no longer true of the code** in at least six
   places (corridor committed, fisherman crewed, anchored hulls awake, the truth rule, the
   far-detail states, the player as captain of another ship), and it records M7 chart blocks
   under an M6 heading. Medium; sure.
10. **The parity test on readings is near tautological.** Both sides of
    `test_every_reading_the_console_answers_the_station_answers_the_same` end in `World.submit`
    (`test_parity.py:205-207`), so it proves the station's filter lets readings through, not that
    the console's own handling matches; and truth 87's tolerance is stated as a mile and
    asserted as a mile and a half, on easting only (`test_crews.py:154-187`). Low; sure.

## What I did not read

- The rest of `freesail/world/captains.py` beyond the line ranges given at the head (about
  2,600 of 4,795 lines unread: the passage work `_passage` to `_shape_leg`, the weather work,
  casts, the station, the engagement and the damage work), `freesail/world/brains.py` (read
  by grep only), `freesail/world/business.py`, most of `freesail/world/crews.py`,
  `freesail/agents/harness.py` (only `open_samples`), `agent.py`, `api.py`, `remote.py`,
  `mcp_server.py`, `local.py`, `core/acts.py`, `core/replay.py`, `world/stations.py`,
  `world/reckoning.py`, `world/ports.py`, `orders/navigation.py`.
- Every doctrine file but `merchant.yaml` was read by script only (stimuli, keys, empty books).
- The tests other than those named; no test was run.
- `docs/DesignProposal.md`, the primer chapters, `docs/agents/ConsentBrief.md`: not read.
- The regatta's recorded table and every measurement under `docs/dev/` and `docs/playtests/`:
  not opened, by the rules.
- I did not run a regatta course to its line nor `tools/pace.py`.
