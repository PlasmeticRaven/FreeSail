# Spec reader 04: `docs/TechnicalSpec-M7.md` (Powder) against the tree

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. Read whole: `docs/TechnicalSpec-M7.md`
(1,400 lines, 121,841 characters). Read in part: `docs/DesignProposal.md` (the M7 line at
553, §5.3 combat at 324 to 329, decisions 49, 51, 56, 64 to 68). Not opened: `docs/dev/`,
`docs/design/`, `docs/playtests/`, `docs/gates/`, the sealed notes. No test suite run; one
short python call of a test helper (below). Nothing changed but this file.

Verdicts are mine from greps, reads of functions and data, and one measured call. "Spec
line" numbers are of `docs/TechnicalSpec-M7.md`.

---

## 0. The shape of the document, first

The specification is not one plan with "as built" notes. It is a plan of 2026-10-23
(spec lines 1 to 22: "Initial specification", "this draft") with forty-six "As built",
"As built out" and "As fixed" paragraphs grafted under it up to package 101 of
2026-11-10. Its own head still calls it the initial draft. Which parts are built and which
are plans:

| Part / § | State at this commit (my reading) |
|---|---|
| 7-i §1 colours, §2 private signal, §3 books, §4 hail | built (packages 71, 76, 86, 88) |
| 7-i §5 lights and bell | built; **sight across land not built** (spec line 351 says so; no code found) |
| 7-ii §7 to §11a guns, gunnery, quarter bill, shot, morale, marines, boarding, far fight | built (70, 73, 74, practice build, 86) |
| 7-iii §13, §14 water and damage control | built (73) |
| 7-iv §16, §16a health, station holder hurt | built (73) |
| 7-v §18, §19 prizes, captive, court martial, new command | built (74) |
| 7-vi §21, §22 squadrons, regimes | built (72, 79a, 84, 86, 88) |
| 7-vii §24 fine control of the sails | **plan only**: no as-built paragraph, no code found |
| 7-vii §25 collision | **plan only**: no as-built, no code (boarding.py:10 says the hulls overlap "until the collision is built") |
| 7-vii §26 the cold | deferred by the spec itself (line 1143) |
| 7-viii §27 ships | **built, with no as-built paragraph**; built otherwise in one point and grown past it (below) |
| 7-viii §28 chart and sources | built to package 101 in the text; the tree has gone on to packages 104, 105, 106a, 109, 111, 112 with no word in the spec |
| §29 consent | drafted, not applied; the refusal flag built |
| §30 gate | outline only; two of its items cannot be run at this commit (below) |
| §31 packages | 70 to 74, 76, 79 (as 79a to 79d) built; 75 built in part with no as-built; 77, 80 not reported on; 78 not built |

---

## 1. The commitments, one by one

| § | what the specification says is built | verdict | where it lives (file:line) | how you know |
|---|---|---|---|---|
| rule 1 | damage is just state; no second model of the ship | built as specified (for what I read) | `combat/hits.py` writes the line's parting through the strain model, holes as hull state; `combat/far_action.py:486` `far_damage_into_parts` | grep of `far_damage_into_parts`; the far record is a second, coarse model by design (§11a), carried into the parts once on waking |
| rule 2 | the gun's cycle served by the bill; rate falls out of the muster | built otherwise: the cycle is the battery's own, not an evolution (spec line 445 says so) | `combat/guns.py:93` `PHASES` | python: long 7 phases 85.0 s, carronade 60.0 s, swivel 35.0 s, matching spec line 446 |
| rule 3 | recognition before fire | built as specified | `combat/action.py:277` `_recognition` | function exists under that name |
| rule 5 | the far ships fight as the near, coarsely | built otherwise: "within two rounds" (spec line 647) where §12 asked "within a round" (line 659) | `combat/far.py:281` `round_once`, `combat/far_action.py` | spec text against itself; truth 7-359 exists |
| §1 | colours a state: shown, none, false, struck, distress (and 74's truce) | built as specified | `world/signals.py:71` `COLOURS_STATES`, `:541` `class Colours` | read |
| §1 | the lookout gives the nation shown, never the true one | built as specified (by name) | `world/ships.py:1130` `Vessel.nation_shown`; `world/lookout.py:824, 998` read it | grep |
| §1 | colours held once shown (88) | built | `world/signalling.py:847` `_true_colours_held` | grep |
| §2 | private table a pure function of seed, nation, year, month | built (by name; purity not tested by me) | `world/signals.py:497` `private_table` | grep; I did not call it |
| §2 | challenge judged right, wrong, none | built | `world/signalling.py:563` `_judge_challenges` | grep |
| §3 | one root per nation; "the same six files", the seventh `colours.yaml` | built otherwise: Britain, France, Spain carry nine files (`days.yaml`, `flags.yaml` beside the seven), basic carries `dressing.yaml` | `data/signals/*/` | `ls`; the spec's file list is stale |
| §3 | Britain 150 day signals, Popham 330 words (71); built out whole (76) | built, figures moved: 171 numerary entries, 1,444 dictionary words, 73 night, 24 fog, 32 convoy | `data/signals/britain/` | yaml counts by python |
| §3 | France 70 day signals, no dictionary | built: 74 entries, no dictionary | `data/signals/france/numerary.yaml` | yaml count |
| §3 | basic: 46 day signals | built as specified: 46 | `data/signals/basic/numerary.yaml` | yaml count |
| §3 | Spain, the United States, Naples built out (76) | built: 100, 69, 55 entries; no dictionaries | `data/signals/spain/`, `united-states/`, `naples/` | yaml counts |
| §3 | a nation's book added by data alone, checked by a tool | built (tool exists) | `tools/check_signals.py` | `ls tools` |
| §3 | the hoist an evolution, three hands, a minute | built (file exists) | `data/evolutions/make_signal.yaml` | `ls` |
| §3 | read by every lookout; the far body performs | built | `world/signals.py:1022` `read_flying`, `:1284` `far_perform`; `world/signalling.py:947` `brainless_minute` | grep |
| §4 | hail by table; nation read from the words | built | `world/hail.py:75` `nation_in_words`, `:634` `exchange_words`, `data/captains/hail.yaml` | read; see §6 below for the table's gaps |
| §4 | `Captain.commands` a property (the 86 fix) | built | `world/captains.py:2406-2407` `@property def commands` | read |
| §5 | lights; seen at three miles | built | `world/signals.py:80` `LIGHT_SEEN_NM = 3.0` | grep |
| §5 | **sight across land** ("7-i's and not later", line 336) | **not built** | none | grep for sight-line, profile and land-blocking terms in `freesail/` finds nothing; spec line 351 admits it is 78's; 78 has not been done |
| §7 | `Gun(Part)` with load state, elevation, train | built | `ship/parts.py:522` | grep |
| §7 | `GunSpec`, `FitSpec`, `ArmamentSpec`, `QuarterBillSpec` | built | `ship/schema.py:732, 805, 841, 862` | grep |
| §7 | magazine by gun kind and calibre | built (by name) | `ship/parts.py:818` `class Magazine`; `combat/filling.py` | grep; contents not read |
| §7 | pivot gun with `arc_deg`, 60 to 140 degrees | built | `combat/guns.py:144-145` `ARC_PIVOT_FROM_DEG = 60.0`, `ARC_PIVOT_TO_DEG = 140.0` | grep |
| §8 | the gun deck's orders | built | `orders/gunnery.py` | file present; not read whole |
| §8 | frigate's 18-pounder every 104 s full, 159 s a quarter down | built as specified, and measured | `tests/test_known_truths.py:8320` | one call of `_frigate_interval(0.0)`: **104.1 s** in 5.9 s; the test's band is 90 to 125 s (wide) |
| §8 | clear for action, a frigate's quarter hour, a cutter's five minutes "by her length" | built in part: the evolution file gives only `quarters_s: 90` and says the two figures are judgement | `data/evolutions/clear_for_action.yaml` | read; I did not find a test holding 15 min and 5 min |
| §8 | practice, resupply by hoy at eleven ports | built (by name) | `world/ordnance.py:203` `block_of`; `combat/marks.py` | grep; port count not checked |
| §8a | quarter bill; sail work robs the guns by the fighting book's priority | built | `evolutions/runner.py:1226` `_rob_the_guns`; `crew/quarters.py` | grep |
| §9 | ballistics by the log of calibre, point blank 250 / 230 yd | built as specified | `combat/shot.py:83, 91` | read: `pb = 250 + 50 log2(p/3)` for long guns, `230 + 70 log2(p/12)` for carronades |
| §9 | lee port shut within a foot of the water | built | `combat/shot.py:65` `PORT_SHUT_M = 0.3048`; `combat/ports.py:76` `PORT_HOLD_S = 60.0` | grep |
| §9 | the man struck: killed three in ten; quarterdeck 0.2 of hits, 0.4 of musketry | built | `combat/hits.py:330, 392`; `combat/small_arms.py:62` | grep |
| §10 | engaging doctrine as data, morale, strike by rule | built | `data/captains/*.yaml` (`morale_start`, `strike_below`, e.g. `merchant.yaml:57-58`); `combat/morale.py`; `combat/action.py:484` `strike` | grep |
| §10 | the nation's habit moved from code into `data/nations.yaml` | built as specified | `NATION_HABITS` absent from `freesail/`; `habits:` in all 16 nations | grep; python over nations.yaml |
| §10 | the player's fighting book | built | `data/standing_orders/fighting.orders` | `ls` |
| §11 | marines' kit by nation and period as data | **built in part**: three kits only (british, french, basic); Spain and every Mediterranean nation on basic | `data/marines.yaml:36-72`; `data/nations.yaml:159` (`spain: marines: {kit: basic}`) | read |
| §11 | musketry within a hundred yards | built | `combat/small_arms.py:56` `MUSKET_SHOT_M = 91.44` | grep |
| §11 | serve out the small arms, an evolution | built | `data/evolutions/serve_small_arms.yaml`; `evolutions/fight_scripts.py:115` | read |
| §11a | grapple, boarding rounds with the named constants | built as specified | `combat/boarding.py:70-84` (30.0, 1.0, 0.5, 15, 0.1, 1.0) | grep; every figure matches the spec |
| §11a | cutting out by the boats | **not built** (spec line 630: "stay 74's"; 74's as-built names no cutting out by boats) | none found | 74's paragraph (lines 632 to 649) is silent on it |
| §11a | far fight wired; `far_action.ENABLED` | built | `combat/far_action.py:63` `ENABLED = True`; `world/crews.py:721` `_in_action`; `world/brains.py:529` `FarCaptain._enemy_within` | grep |
| §11a | "Not built here (package 70) ... not wired" (line 626) | overtaken by 74's paragraph (line 632), left in the text | | read |
| §13 | water as tons; orifice law; pumps; foundering | built (by name) | `world/water.py` (952 lines); every hull file has `pumps:` | grep over `data/ships/` |
| §14 | the damage-control catalogue as evolutions | built | `data/evolutions/plug_shot_hole.yaml`, `fother_sail`, `fish_spar`, `rig_preventers`, `set_up_rigging`, `cut_away_mast`, `jury_mast`, `reeve_line`, `batten_down` | `ls`; `FOTHER_SHARE = 0.3` at `world/water.py:688` |
| §16 | health states, surgeon's queue, sick list | built (by name) | `crew/health.py` (1,076 lines); `crew/model.py:210` `dead: list[Sailor]` | grep |
| §16 | disease of its own | not built, by design (M8) | | spec line 731 |
| §16a | holder hurt, roads at parity; command passes | built | `world/needs.py:173` `NeedsKeeper`, `:483` `_tell`; `agents/harness.py:3213` `_lose_deck`; `world/people.py:992` `command_passed_to` (an attribute) | grep |
| §18 | possession; prize master role; prisoners | built | `world/prizes.py:655` `possess`; `data/captains/prize-master.yaml`; `class Prisoners` in `world/prizes.py` | grep |
| §18 | prize court by nation; eighths by date | built | `data/business.yaml:136-195` | read |
| §19 | the captive's channel, parole by nation | built | `world/captive.py` (1,061 lines); `data/captains/hail.yaml` `parole:` | read the table |
| §19 | cartel under a flag of truce | built | `world/signals.py:71` `truce`, `:566` | grep |
| §19 | court martial as the director's; `Person.record` | built otherwise: the record is not a declared field but a list stuck into the person's `__dict__` on first read | `world/court.py:119-130` `record_of` | read |
| §19 | a new command writes `saves/<name>` | built | `world/court.py:793, 820` | grep |
| §21 | `Squadron` set, formations, book, registry | built (by name) | `world/squadrons.py` (1,752 lines); `data/squadrons/{convoy,squadron,blockade}.yaml` | `ls`, grep |
| §21 | the line of battle's own book; the squadron shown to the player as an object; night and fog signals as a set's standing order | **not built** (the spec's own list, line 937) | | spec |
| §21 | pace cap on the commander's far body | built | `world/ships.py:691` `pace_cap_kn` | grep |
| §21 | near station law vs far (88) | built, two laws by design | `orders/station.py:280` `_course_clamped`, `:57` `LEAD_M`; `world/ships.py:862` `Vessel._course_for` | grep |
| §22 | eight regimes, each a rule | built as specified: in port, in ordinary, on station, on passage, in convoy, escorting, on blockade, in chase | `data/regimes.yaml:28-65` | read |
| §22 | ships in ordinary, sortie, commission by the business | built | `world/regimes.py:88` `commission`; `world/business.py:1146` `intents_for` | grep |
| §22 | Spain's stations "Ferrol, Cadiz, Cartagena" (§28, line 1196) | **built in part**: Ferrol and Cadiz only; nothing at Cartagena, and no blockade of Toulon though `data/ports/toulon.yaml` and `cartagena.yaml` exist | `data/nations.yaml` `naval:` | python: Britain blockades brest, rochefort, ferrol, cadiz (twice), lorient; Spain in ordinary ferrol, cadiz |
| §22 | the nations' fighting habits as regime rules; the commission's delay drawn | first built by 79a (commission); "every nation's `engages`, `single_actions` ... still judgement" | | spec line 1074 |
| §24 | settle the topgallant halyards, sway up, vangs on a gaff, a sail kept shivering by command, sheets checked by so much, the `keep <x> <state>` prefix, the gybe as an evolution | **not built** | none; `orders/grammar.py:253` makes "gybe" a wear; vangs exist only for the lateen and settee yards (`orders/verbs.py:1582`), not for spilling a gaff sail | grep for settle, sway up, shiver, keep prefix, gybe evolution; no `gybe` file in `data/evolutions/` |
| §25 | collision with consequences | **not built** | `combat/boarding.py:10` says the grappled hulls "overlap on the chart until the collision is built" | grep |
| §26 | the cold | deferred (spec's word) | | grep for snow and freezing in `freesail/` finds only `.pyc` hits |
| §27 | the *Indefatigable* razee 44 | built | `data/ships/razee-44.yaml` (and `sixty-four.yaml`, the 64 she was cut from, not asked for) | read the head |
| §27 | the *Prince de Neufchatel*, "the privateer schooner" | **built otherwise**: a hermaphrodite brig | `data/ships/hermaphrodite-brig.yaml:1` | read the head; the spec still calls her a schooner and has no as-built |
| §27 | a 74 of Slade's design, the *Bellerophon* as the name | built | `data/ships/seventy-four.yaml:1` | read |
| §27 | every file given armament, quarter bill and marines | built as specified | all 13 hull files carry `armament:` and `quarter_bill:`; marines on the frigate, brig, 64, razee, 74, Neufchatel | grep over `data/ships/` |
| §27 / §28 | package 90's five Spanish and Mediterranean hulls (tartane, polacre, xebec, *Diana*, *Purísima Concepción*) | **not built** | no such files in `data/ships/` | `ls` |
| §28 | Mediterranean first: 79b to 79d, 101 | built (by region id) | `data/charts/manifest.yaml`: channel-east, mediterranean-west, balearics, gulf-of-lion, ligurian-sea, tyrrhenian, catalan-coast | grep |
| §29 | adversarial seat refused behind one flag | built | `world/seats.py:76` `ADVERSARIAL_SEATS_CONSENTED = False`; `world/prizes.py:1115` `adversarial_seat_why` | grep |
| §29 | the consent revision applied | not built (drafted only, by the spec's word) | | spec line 1264 |
| §30 | gate 7 | outline only (see §6 below) | | |

---

## 2. The pointers

Twenty taken through the document and checked by grep or read:

1. `signals.Colours` (line 88): holds, `world/signals.py:541`.
2. `Vessel.nation_shown` (91): holds, a property, `world/ships.py:1130`.
3. `action._recognition` (103): holds, `combat/action.py:277`.
4. `signalling._true_colours_held` (113): holds, `world/signalling.py:847`.
5. `signals.private_table` (130): holds, `world/signals.py:497` (and a method at 270).
6. `signalling._judge_challenges` (143): holds, `world/signalling.py:563`.
7. `signals.read_flying`, `signals.far_perform`, `signalling.brainless_minute` (225 to 239): hold.
8. `nation_in_words`, `exchange_words` (304, 307): hold, `world/hail.py:75, 634`.
9. `LIGHT_SEEN_NM` three miles (342): holds, `world/signals.py:80`.
10. `combat/guns.py` seven phases, 85 / 60 / 35 s (445): holds (python).
11. `Runner._rob_the_guns` (510): holds, `evolutions/runner.py:1226`.
12. `hits.hit_man`, `QUARTERDECK_SHARE` 0.2 (552): holds, `combat/hits.py:330, 392`.
13. `GRAPPLE_RANGE_M`, `CROSSING_GUN_MEAN`, `ROUND_LOSS`, `CARRIED_RATIO`, `REPULSE_COST`, `CONTEST_ROUNDS` (630): all hold with the spec's figures, `combat/boarding.py:70-84`.
14. `DIVISION_HAILS` (613): holds, `orders/grammar.py:120`.
15. `far_action.ENABLED`, `far_damage_into_parts`, `crews._in_action`, `FarCaptain._enemy_within` (632 to 648): hold.
16. `NeedsKeeper._tell`, `_lose_deck`, `People.command_passed_to` (752): hold (`command_passed_to` an attribute, `world/people.py:992`).
17. `prizes.possess`, `prizes.adversarial_seat_why`, `seats.ADVERSARIAL_SEATS_CONSENTED` (780, 1276): hold.
18. `Captain._aback_with_no_way`, `Captain._danger_ahead_by_chart`, `navigation.no_room_to_wear` (995, 1107): hold, `world/captains.py:3056, 3132`, `orders/navigation.py:1074`.
19. `world/ordnance.block_of`, `Tide.gauges_at`, `Business.intents_for`, `regimes.commission` (472, 1249, 1046, 1049): hold.
20. Truth numbers cited (7-133 to 7-184, 7-200, 7-260 to 7-269, 7-340 to 7-342, 7-350 to 7-369, 7-426 to 7-435): every one has a `test_truth_7_<n>_...` in `tests/test_known_truths.py` (python over the file: none missing).

**Twenty of twenty hold by name.** Those that hold by name but not as described:

- "the same six files in each" root (line 197): nine files in three roots.
- `Person.record` (853): no declared field; `court.record_of` writes it into `__dict__`.
- `NATION_HABITS` "in the code" (579): gone, as the same sentence says it should be; the pointer is history.
- `combat/far.py` "not wired to the far brains" (627): overtaken, left standing.
- The comment at `combat/guns.py:90` says 105 s measured at seed 7; the test docstring and the spec say 104 s; I measured 104.1 s. A small comment-against-code drift.

---

## 3. The numbers

| number | held by a test? | checked by me |
|---|---|---|
| 18-pounder every 104 s full, 159 s a quarter down (§8, §12) | yes, truth 7-135, bands 90 to 125 s and 140 to 210 s (`tests/test_known_truths.py:8329-8333`) | full company: **104.1 s** measured |
| gun phases 85 / 60 / 35 s | not by name in a test I read | python: matches |
| tack cleared 447 s, 436 s robbing the guns, 642 s guns first (7-136) | truth exists | not run |
| two crewed cutters in action 538 ticks a second (7-138) | truth exists (`:8466`) | not run (would spoil the timings) |
| far fight: two cutters at two cables struck in 21 min (7-139) | truth exists | not run |
| Nelson's sentence twelve hoists, twelve minutes (7-146) | truth exists | not run |
| boarding constants, lights at three miles, lee port at a foot | constants in code | grep: all match |
| the owner's 95 ticks a second with twelve crewed ships, the six-on-six baseline (rule 5, §30 7d) | none found: grep for six on six or 7d in `tests/` finds nothing | not measurable by me |
| clear for action: frigate 15 min, cutter 5 min | none found | the evolution file carries only `quarters_s: 90` |

The test bands are wide (the frigate's interval may move 20 per cent either way and pass),
which the spec admits ("pinned with wide bands", line 663).

---

## 4. The open items

Counted from §5, §11a, §21, §22, §24 to §26, §27, §32, §33, §34 and the §31 table.

**§33, carried in from M7b (sixteen items):**

| item | state |
|---|---|
| R-17 the voice between ships | built (§4) |
| R-54 colours, a bluff, a fort | colours and the bluff built; no fort found |
| the pumps, the carpenter | built (73) |
| the capstan's purchases | cannot tell; grep for capstan with purchase in `freesail/` finds nothing |
| sail's thrust aground; the kedge's heave-taut | not found; grep for heave taut or thrust aground finds nothing |
| R-39 the weather's stacking and drift | placed (truth 7-158; the drift a PROVISIONAL note, line 1060) |
| the land-avoiding planner (61) | a "Merge package 61" commit exists; truths 7-545 and 7-563 are of the land guard |
| the boat as a vessel and towing (63) | built by the look of truth 7-330 (towed by her boat) |
| the place's knowledge (65) | built by the look of truths 7-370 to 7-392 |
| the harbour's second pass (64) | struck for package 96; no merge of 96 found |
| the cold (26) | deferred |
| the thermometer's first layer | deferred; grep finds nothing |
| the lay line (43b) | not found; grep for lay line finds nothing |
| the Windows pins (69) | cannot tell |
| the lead's playtest of the gale book and the owner's decisions in 58a, 58b, 67 | cannot tell (records under `docs/dev/`) |

**Other "not built", "deferred", "left to" items in the body:** sight across land (§5);
cutting out by the boats (§11a); the line of battle's book, the squadron as an object
shown, night and fog as a set's standing order (§21); fighting habits as regime rules
(§22, then "still judgement" with about a dozen knobs listed at lines 1065 to 1077);
disease (§16, M8); fine control and the gybe (§24); collision (§25); the cold (§26);
package 90's five hulls (§28); the consent revision (§29); the marines' kit data "75's"
(§34). **§34's nine undecided points**: seven are now decided in the as-built text (bands,
morale a ship's figure, the far fight as tables, the books' extent, the model's signal by
order, the chart's block, the kit's shape); the marines' kit data by nation is still at
three kits, and "what the later packages teach" is open by nature.

That is **some thirty open, deferred or left items**, of which about eighteen are still
open at this commit and four (the capstan's purchases, the thrust aground, the heave-taut,
the lay line) are nowhere in the code and nowhere marked done or dropped: quietly dropped,
so far as the specification shows.

---

## 5. The document as a document

- **Not buildable by a newcomer.** It names files and functions well (twenty of twenty
  pointers hold), but every as-built paragraph is a single breathless sentence of 300 to
  700 words (§11 line 613, §11a line 630, §13 line 693, §16 line 733 are each one line of
  the file); the "what" is buried under the "who and when".
- **History outweighs specification.** 67 package numbers, 27 dated rulings, 48 mentions
  of the owner, 46 as-built/as-fixed paragraphs, 8 pointers into `docs/dev/` and 16 into
  `docs/design/` for the figures and the reasons. The plan text and the as-built text
  disagree in places and both are left standing (§11a's "not wired" above the wiring; §3's
  six files; §12's "within a round" against 7-359's two).
- **Contradicts itself on the chart.** §32 (line 1343): this milestone does not do "the
  Lakes or any new chart block before the gate's scenarios choose one". §28 records seven
  regions built (79b to 101), and the tree holds more again (below).
- **Its status line is false.** "Initial specification of 2026-10-23" (line 3) and "this
  draft" (line 1392) over text dated to 2026-11-10.
- **Stale against the code.** The last package it reports is 101 (2026-11-10). The tree
  carries the merges of packages 102, 104, 105, 106a, 109, 111 and 112 (git log), and M7
  truths numbered up to **7-584** against the spec's last cited 7-435: some 150 truth
  numbers of this milestone with no word in its specification.
- **§27 has no as-built at all**, though package 75's three ships are in the tree; the
  *Prince de Neufchatel* is described as the wrong rig.

---

## 6. What the specification never asked for, and the gate

### How far M7 has grown past the proposal's "first target"

The proposal (`DesignProposal.md:324-329`, `:553`): "Guns, shot, damage into the part
graph, a two-ship action, prize resolution; and the sails at fine control"; "First target:
a single-broadside engagement between two small vessels"; "Boarding, prize crews, and
surrender are abstracted resolutions in the first version."

What M7 now holds, and whether the specification asks for it:

| holding | asked by the spec? | evidence |
|---|---|---|
| the single-broadside two-cutter action (the first target) | yes; built | truth 7-134 |
| signal books by nation: six roots (Britain, France, Spain, the United States, Naples, basic), nine files each at most, flags of command and dressing | yes in outline (§3, owner's note); the build-out to Naples, the United States and the `dressing.yaml`/`days.yaml`/`flags.yaml` files are as-built additions, not asked | `data/signals/` |
| squadrons as sets, convoys, divisions, blockades | yes (§21, the owner's note 8) | `world/squadrons.py` |
| regimes, ships in ordinary, commissioning, the business across regions | yes (§22) | `world/regimes.py`, `data/regimes.yaml` |
| prize courts by nation, eighths by date, salvage, head money, sharing in sight | yes (§18); far beyond "abstracted resolutions" | `data/business.yaml:128-195`, `world/prize_court.py` |
| captivity: parole, cartels, prisoners' agents, the court martial, a new command written as a scenario file, the career's record | yes (§19), with the career named as M8's; still a large world for "prize resolution" | `world/captive.py`, `world/court.py` |
| water in the ship, pumps, foundering | yes (§13, the owner's notes) | `world/water.py` |
| health: wounds, sick list, burial, the station holder hurt | yes (§16, §16a) | `crew/health.py` |
| boarding by rounds, marines, small arms | yes (§11, §11a), against the proposal's "abstracted" | `combat/boarding.py`, `combat/small_arms.py` |
| practice at the great guns, resupply by the Ordnance's hoy at eleven ports | added by the as-built of "between packages 72 and 73" (line 452), from a build note, not from the plan | `world/ordnance.py`, `combat/marks.py` |
| lee ports and the roll | yes (§9, owner's note 6) | `combat/ports.py` |
| boats as vessels (five boat hull files) | not in this spec (M7b's 63, and "package 82" in the file heads) | `data/ships/boat-*.yaml` |
| new ship classes: razee 44, the 64, the 74, the hermaphrodite brig, the bilander | the razee, the Neufchatel and the 74 asked (§27); **the 64 and the bilander not asked by this spec**; the five Spanish hulls asked (§28) and not built | `data/ships/` |
| the one-world refactor (hulls, registry, follow, the save holding every hull) | recorded in §21's as-built (package 84) but nowhere asked in the plan text | spec lines 949 to 988 |
| chart blocks: channel-east, the Mediterranean west, Gulf of Lion, Ligurian, Tyrrhenian, Catalan coast | recorded (§28), against §32's own rule | manifest |
| **chart blocks never named in the spec**: sardinian-sea, tunis-coast (104), sicily and gulf-of-hammamet, calabria-north (105), canaries and salvages (106a), atlantic-corridor, atlantic-south, asinara-west | **not asked**; the code ran ahead | `data/charts/manifest.yaml:11454-14090`; git log "Package 104", "Package 105", "106a" |
| sixteen nations, eight of them Mediterranean states (Algiers, Sardinia, Naples, Etruria, Liguria, the Papal State, Tunis, the Order of St John), with dated holdings of ports | not asked by the plan; §28's rule presupposes them | `data/nations.yaml` |
| letters and things written and read (truths 7-470 to 7-478), viewer drawings of flags, smoke and flashes (7-440 to 7-456), ports' records and dated history (7-580 to 7-584) | not asked by this spec; §32 excludes "a damage picture beyond the viewer's present honesty" | truth names in `tests/test_known_truths.py` |
| fine control of the sails, the proposal's own words for M7 | **asked, not built** | §24 above |

The growth is authorised mostly in the proposal's decisions (49 "M7 will expand as it
goes", 56, 64 to 68), not in the specification: the spec was amended for the work up to
package 101 and then stopped. The two things the proposal's own M7 line names that are
missing are the fine control of the sails and (for the gate) the lugger behind the headland.

### The gate (from the specification only)

§30 (lines 1281 to 1307) is an outline in five parts and a reminder. It would test:
7a a frigate action with the *Indefatigable* against a French frigate or privateer
**under a model captain**, to a strike, the damage, pumps, surgeon, the prize sailed in,
and the same at far detail; 7b the convoy and escort against a privateer, the signals,
hail and private signal, and **the lugger behind the headland unseen**; 7c the regimes;
7d six on six against the 95 baseline; the player struck to **a model's ship** and the
continuation; the lee ports and the roll as the first "not forgotten" figure.

At this commit: 7a and the player-struck item need a model at an adversarial captain's
station, which `seats.ADVERSARIAL_SEATS_CONSENTED = False` (`world/seats.py:76`) refuses
until the consent revision is applied (§29, not applied); 7b's headland needs sight across
land, not built; no scenario in `data/scenarios/` uses `razee-44`, `seventy-four` or
`hermaphrodite-brig` (grep), so 7a's ship has no scenario. The specification says nothing
of an interim gate.

### §28: Spain and the Mediterranean in every nation-specific extension

The rule (lines 1188 to 1207): any nation-keyed table writes Spain's row with its source,
and the relevant Mediterranean factions where it can, or says in the tuning notes what was
looked for and leaves the row at basic; "never silently British-and-French only".

Three tables sampled:

1. **`data/marines.yaml` (kits).** Rows: `british`, `french`, `basic` (lines 37, 49, 61).
   No Spanish row; Spain is pointed at `basic` (`data/nations.yaml:159`), as is every
   Mediterranean nation. The file predates the rule (package 73; the rule is 2026-11-06)
   and has not been revisited; §34 put the kits' data on package 75, which added none.
   Whether the tuning notes record a search: I may not look. **Not kept on the face of the
   table**: British and French only, the rest on the foundation, with no Spanish source
   or note in the file.
2. **`data/business.yaml` `prize_courts` and `prize_shares`.** Spain has a row in both
   (lines 141, 191 to 195), honest that the Spanish distribution was not read and the
   British eighths stand ("decision 64: the row present and honest"). No Mediterranean
   nation has a row; they fall to `default` (prize courts) or to nothing (shares).
   **Kept for Spain; not for the Mediterranean factions.**
3. **`data/captains/hail.yaml` (`navy`, `ports`, `lies`, `parole`).** Spain has a row in
   all four (lines 44, 168, 180, 214). Algiers, Tunis, Sardinia, Naples, Etruria, Liguria,
   the Papal State and the Order of St John have **no row in `navy`, `ports` or `lies`**,
   though Morocco does. The code falls back to `"the {kind} {name}"`, `"the port"` and the
   English name `"Nancy"` (`world/hail.py:489-500`), so a Neapolitan or Algerine ship lying
   under her own colours answers as the Nancy of "the port". **Kept for Spain; not for the
   Mediterranean factions**, and the fallback is not period-plausible.

Beside these: `habits:` and `naval:` are present for all sixteen nations, with `sources:`
maps only for the first five (britain to united-states); Spain and Naples have their own
signal roots. The rule is **kept for Spain in two of three sampled tables, and kept for the
Mediterranean factions in none** of the three, outside the nations file itself.

---

## The ten findings that matter

1. **The sails at fine control, named in the proposal's own line for M7, is not built**
   (§24: no settle, sway up, gaff vangs, sail kept shivering, sheets by so much, `keep`
   prefix or gybe evolution; grep). Weight high (a stated deliverable of the milestone);
   confidence sure.
2. **The gate as the specification writes it cannot be run at this commit**: 7a and the
   player struck need a model at an adversarial seat, refused by
   `world/seats.py:76`; 7b's headland needs sight across land, not built; no scenario uses
   the *Indefatigable*. Weight high; confidence sure.
3. **The specification stopped at package 101; the code did not.** Packages 102 to 112
   merged, about 150 more M7 truths (to 7-584), and eleven chart regions (Sardinian sea,
   Tunis, Sicily, the Canaries, the Salvages and others) that the spec never names and that
   its own §32 forbids before the gate's scenarios. Weight high (the document no longer
   describes the milestone); confidence sure.
4. **§28's rule is kept for Spain and not for the Mediterranean factions**: the marines'
   kits have no Spanish row (`data/marines.yaml:36-72`); the prize tables and the hail
   table have Spain but no Algiers, Tunis, Naples or Sardinia, and the hail falls back to
   an English "Nancy" of "the port" (`world/hail.py:489-500`). Weight medium; confidence sure.
5. **Collision is not built** (§25), so grappled ships overlap on the chart
   (`combat/boarding.py:10`) and a close pass has no consequence. Weight medium; sure.
6. **Scope has run far past the proposal's first target and its "abstracted resolutions"**:
   boarding by rounds, prize courts with dated eighths, parole, cartels, courts martial, a
   new command written as a save file, practice and resupply at eleven ports. Mostly asked
   by the spec; the practice-and-resupply build entered by a build note, not the plan.
   Weight medium (cost of keeping it); confidence sure.
7. **§27 has no as-built and is wrong in one point**: the *Prince de Neufchatel* is a
   hermaphrodite brig (`data/ships/hermaphrodite-brig.yaml:1`), not "the privateer
   schooner"; the 64 and the bilander are unasked; package 90's five hulls are absent.
   Weight medium; sure.
8. **The document is history more than specification**: 67 package numbers, 27 dated
   rulings, 46 grafted paragraphs, single-sentence paragraphs of hundreds of words, stale
   statements left above their corrections (§3's six files, §11a's "not wired"), and a
   head that still says "initial specification ... this draft". Weight medium; sure.
9. **About thirty open or deferred items, four of them dropped without a word** (the
   capstan's purchases, sail's thrust aground, the kedge's heave-taut, the lay line: no code
   found, no note of closure). Weight low to medium; likely.
10. **What is built holds to its pointers**: twenty of twenty names exist, the boarding,
    musketry, light and lee-port constants match the text, and the frigate's interval
    measures 104.1 s as the spec says; but the truths' bands are wide (90 to 125 s) and
    Spain's §28 stations stop at Ferrol and Cadiz (no Cartagena, no Toulon blockade).
    Weight low; sure.

## What I did not read

- The code bodies, beyond the functions and constants named above: I verified names and
  figures by grep and short reads, not behaviour. `combat/action.py`, `world/squadrons.py`,
  `world/prizes.py`, `world/captive.py`, `world/water.py`, `crew/health.py` were not read
  whole.
- The tests beyond truth 7-135 and its helper; no suite run; only one measured call.
- The other specifications (M7b, M6), the proposal beyond the lines named, and every
  `docs/design/` and `docs/dev/` file the spec points to (forbidden); so the "said in the
  tuning notes" escape of §28's rule could not be checked.
- The data files beyond those sampled: the ports, the people files, the squadron books, the
  signal books' contents (counted, not read), `data/regimes.yaml` beyond its keys.
- The chart manifest beyond its region ids.
