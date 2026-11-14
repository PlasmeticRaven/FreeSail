# Spec reader 05: `docs/TechnicalSpec-M7b.md` (the director) against the code

Commit 504a25066c6995ce9829a19ffc597feb510a1870. The specification read whole (2,315 lines,
182,146 characters). Code read: `freesail/agents/director.py` lines 1-580 and 1240-2060 whole
(the brief, its limits, the station brief, the budget, the log, the channel, `direct`);
`freesail/world/orders.py` lines 100-580, 1406-1515, 2520-2640, 3167-3224, 3380-3440,
3609-3720, 4087-4266 (the channels, `apply`, the hand's reach, `reach`, the aboard effects,
`doubt`); `freesail/world/captains.py` 2380-2550 (`set_intent`, `carry_on`, `player_hand`);
`freesail/agents/fake.py` 558-625 (the fake director); `freesail/agents/agent.py` 871-896
(`DIRECTOR_DOMAIN`); `data/director/aboard.yaml` (the boat and hurt entries) and the six
starter briefs. Everything else was checked by grep or by a few seconds of python (scripts in
the session scratchpad, nothing written to the tree). No test suite was run.

## 0. The questions put, answered first

**Which of the five parts are built.**

| part | verdict | evidence |
|---|---|---|
| 7b-i the director proper | built in part | station, brief limits, doubt, budget, hidden log, reveal, `two stories`, seat through the API door, the player's channel, the hand: all present (`director.py` 200-2049; `seats.py`; `crews.hand`). Not built: the director seated in a ship (spec 407-408, says so), the director's own chart (§12a; `tools.py:1598` `at_director` only describes the player's chart), focus/unfocus (§12b; no `focus` anywhere in `freesail/`), `read_log` by kind (`tools.py:1614-1624` takes ship, ticks, severity, count; no kind) |
| 7b-ii the voice | built as specified | `orders._make_person`, `_say_as`, `Voice`, `director.ask_unheld`/`answer_questions` exist and are driven by truths 7b-95 to 7b-97 (`tests/test_known_truths.py:5745-5816`) |
| 7b-iii the observed world | built (by later packages 82 and 84) except the director's chart and focus | `tests/test_observer.py` ten tests, among them `test_a_day_observed_runs_with_the_business_on...` (line 304); truths 98, 99, 99a, 99b do not exist under those numbers (grep `7b_98\|7b_99` over `tests/`: nothing) |
| 7b-iv people in places | built, and grown past the spec | `world/movement.py` 1,276, `places.py` 1,022, `things.py` 818, `orders/free.py` 858, `hearing.py` 299, `books.py` 475, `agents/watches.py` 113, and package 65's `knowledge.py` 1,248 and `reports.py` 835: the locational knowledge §15 says is "dropped" |
| 7b-v needs | built as specified up to the urgent line | `world/needs.py` 837 (`NeedsKeeper`), `crew/victuals.py` 314, `orders/needs.py` 82, `data/crew/needs.yaml`, `data/crew/ration.yaml`; truths 7b-103, 7b-104 (`test_known_truths.py:5887, 5913`) |

**Are the guardrails enforced in code.** In part. The brief's limits are checked in code at
the director's door (`director.direct`, `director.py:1984-1993`, after the budget and the rule
of reach, before the doubt), the doubt is code (`orders.doubt`, `orders.py:4087`), and the
station's `DIRECTOR_DOMAIN` admits only queries and readings (`agent.py:871-896`). But the
rule the whole milestone stands on ("cannot move the player's ship, change a sail or
countermand an order", spec 38-41, the station brief `director.py:1305-1307`) is not
enforced: see finding 1. Two of the five limits refuse nothing (finding 4), one is evaded by
a word the ranking does not know (finding 3), and the rule of reach does not cover a held
person's body (finding 2).

**The road by which a director's world order moves the player's ship.** Found, and it is
advertised to the director. `captain: intent <words>` is a channel of the world orders
(`orders.py:125-131`, `_captain` 390-416); `reach` returns None for it (`orders.py:2595`:
only `say` and `person` are judged, `ship` only for the hand, `aboard` only for things and
money); `doubt` never doubts it (`orders.py:4099-4102`); no brief limit names it
(`DirectorBrief.limit_of`, `director.py:322-357`). The director's own table of forms offers
it: `Form("captain", ..., "captain: intent <words>", ..., "the followed ship's rules-based
captain given an intent")` (`director.py:918-924`), and the followed ship is the player's by
default. Probe (frigate at seed 7 off the Lizard, the player at the prompt having ordered
`set plain sail` and `steer west`, the quiet-passage brief):

```
held: the captain (Captain Bowen, the player at the prompt)
D.direct(w, "captain: intent bound for Plymouth")
RESULT: Done: the captain's intent: bound for Plymouth ... (47 acts of the day's 48 left.)
after: active True commands True aside False
[900 s later] LOG sail.set | Set the spanker.  sail.set | Set the fore topgallant.
helm.steady | Steady on NE (48°).  sail.set | Set the main topgallant. ...
```

The director's order set her sails and turned her from west to north-east under the player's
hand. `captain: carry on` (`captains.py:2510-2521`) is the second road: it ends the captain's
standing aside that the player's own order made (`player_hand`, 2487-2508), which is
countermanding the player in so many words. Nothing in `tests/` gives `captain:` through
`director.direct`; `tests/test_captains.py:359` gives it as the owner's `world_order`, which
is meant to bypass the director's door.

**What the fake director does, and whether anything else drives the machinery.**
`fake.direct_the_voyage` (`fake.py:558-617`) plays a fixed list of world-order strings, one a
sample, through the `world_order` tool; any answer beginning "Doubted" or "The game has no
way" is re-entered with the canned reason "the story wants it; the fake's"; when the list is
spent it stands by for a watch; with `answers` it answers a pending question as the person in
the map's words or "Aye, sir.". It reads nothing (no truth, no log), so it tests the plumbing
and never the judgement the brief asks for. Apart from it, the tests call `director.direct`
by hand (the player's-seat road) and drive the API door and the MCP bridge against stand-ins
(`tests/test_agent_api.py`, `test_mcp_server.py`, `tests/messages_api.py`). No recorded real
model's director run is in `tests/` or `tests/fixtures/` (grep: the only director-bearing
fixture is a save, `pre-100-step-2-letter-in-hand.json`). `director_above_the_game` is used
only in `tests/test_director.py`, `test_known_truths.py`, `test_observer.py`.

**How large "small once both exist" became.** Git history cannot apportion it: every file
was added in commits dated 2026-11-10 with record messages (`git log --diff-filter=A`), so the
figures below are by file. The director proper's own new modules: `agents/director.py` 2,381,
`world/seats.py` 786, `agents/tripwires.py` 349 = **3,516 lines**, beside its share of the
grown shared modules (`world/orders.py` 4,746, much of it this channel's doubt, reach, aboard
table and hand; `world/crews.py` 1,779 with the hand and the hold; `harness.py`, `tools.py`,
`remote.py`, `api/readings.py` with the truth). All the milestone's new modules together
(the five parts, fishing and the glass, the harbour and settings, the boat): **16,026 lines**
(3,516 + people in places 6,944 + needs 1,233 + fishing/glass 1,365 + harbour/settings 1,802
+ boat 1,166), about a tenth of the package's 164,607 lines of Python. Tests: `test_director.py`
1,823 lines and 53 tests; the 7b truths in `test_known_truths.py` 44 functions over some
2,500 lines (5517-8000 and 13235-13500); with the part files (`test_people` 971,
`test_orders_places` 482, `test_stores` 184, `test_fishing` 323, `test_harbour` 702,
`test_settings` 214, `test_observer` 316, `test_knowledge` 2,104, `test_tell` 390,
`test_seat_hook` 175, `test_boat_*`/`test_tow` 695, `test_world_orders` 1,070) about
**12,000 lines of tests**. The specification itself is 182,146 characters.

**The unbuilt and deferred, as the specification names them**: §4 of this file, 36 items.

## 1. The commitments

| § | what the specification says is built | verdict | where | how I know |
|---|---|---|---|---|
| intro, §2 | the director cannot move the player's ship, change a sail or countermand an order | **not built** (not enforced) | `orders.py:390-416, 2580-2633`; `director.py:918-924` | probe above: `captain: intent` done at the director's door, sails set and course changed |
| §2 | a station `director` bound on the World, no person, kind in `STATION_FACTORIES`/`WORLD_KINDS` | built as specified | `director.py:1406-1428`, `set_brief` 485-487 | read |
| §2 | its domain refuses every order of any ship | built as specified for `submit_order` | `agent.py:871-896` (objects query and reading only) | read |
| §2 | tools `world_order`, `truth`; never `hand_over`; chart with its own words | built as specified | `tools.py:491-508`, `at_director` 1598, 1957 | grep, read |
| §2 | the truth surface `readings.director_readings` | built (exists) | `api/readings.py` | grep |
| §2a | seat through the API door started by the harbour, budget enforced, uncallable model refused | built as specified (not run) | `seats.py`, `Harbour.tend_seats`, `director.uncallable_seat` 1812-1836 | grep; read |
| §2a | seats on the player's own ship allowed unless the grant says false | built as specified, and a risk | `seats.py:384-387` | read: a model seated as an officer of the player's own ship by the director's order (suspicion only: a road to sail orders if the deck passes to it by the watch bill, `agents/watches.py:51-86`; not probed) |
| §2a | the player's word to the director apart from the play log; the answer back | built as specified | `director.py:1714-1785` | read |
| §3 | weather bounded "a wind not stronger than the season's record" refused | built otherwise | `limit_of` 327-333 judges one system alone against the brief's knots; season's floor/ceiling only doubted (`_doubt_weather` 4359) | read; spec 461-462 itself keeps the summed field out |
| §3 | a ship put on the sea not inside the horizon unless hidden, not aground | built otherwise | `_doubt_ship` 4159-4190 doubts (performable with a reason); the land refused (`new_ship_spec`) | read |
| §3 | the aboard table, 24 things + 2 repairs, each with plausibility, doubt, harm | built and grown (34 entries) | `data/director/aboard.yaml` | `grep -c "id:"` = 34 |
| §3 | doubted not refused; re-entered with a reason, performed and logged | built as specified | `director.py:2000-2039` | read; probe 2 |
| §3 | a reason given on the first entry answers no unseen doubt | built as specified | `director.py:2001-2005` | read |
| §3 | an order in no form answered honestly, logged unperformed/attempted, no act | built as specified | `_no_way` 1861-1882 | read |
| §3 | the hand: refused for the player's ship and a held captain | built as specified for `ship "X": order` | `orders.py:1438-1477` | read |
| §3 | the hand's doubt: anchor > 30 fathoms, plain sail > 34 kn, a peaceful master's chase | built as specified | `orders.py:4204-4263` | read |
| §3 | the hand held a glass or until an event | built (names exist) | `crews.HAND_HOLD_S`, `HOLD_EVENTS`, `HOLD_UNTIL_MAX_S` | grep |
| §3 | new ship's form read clause by clause before the doubt | built as specified | `form_error` 1406-1419; probe 4 answers "no description a far-detail ship takes" | probe |
| §3 | the world orders "kept for the record only" | built (lines carry `the director` actor and `world.order` kind) | `core/events.for_the_record`; truth 7b-91 | grep, test name |
| §4 | limits enforced by the channel, not trusted to the model | built in part | `director.py:1984-1993` | read; findings 2-4 |
| §4 | `wind_max_kn` by the bell's steepest gradient: 965 hPa/450 km 42 kn, 1000 hPa 16 | built as specified | `_peak_wind_kn` 375-401 | python: 41.2 and 16.0 knots (background default) |
| §4 | `enemy_heaviest` ranked as the tops rank a sail | built, with a hole | `_enemy_heavier` 404-428 | probe 4: under "no enemy heavier than a cutter", `a French line-of-battle ship` is **Done** ("a seventy-four, a ship of the line ... put on the sea"); `size_rank_of('line-of-battle ship')` is None |
| §4 | `nobody_dies` | built, refuses nothing | `limit_of` 338-341; no `harm: deadly` in `aboard.yaml` | grep; probe 2 (the player's captain dangerously hurt under `nobody_dies`) |
| §4 | `the_war_as_it_is` | built as specified | `limit_of` 346-356 | read |
| §4 | `the_chart_as_it_is` | declared, refuses nothing (spec says so) | `limit_of` has no branch | read |
| §4 | the four starters: quiet passage force 6, a cutter, **four** acts; interesting 7, brig, six; hard 9, frigate, eight; chase 7, brig, six | built otherwise | `data/director/briefs/*.yaml`: acts 48, 48, 72, 72; six starters (captive and dispatches added) | grep |
| §5 | budget in samples and acts a day, held until the day turns | built as specified | `DayBudget`, `count_sample`, `direct` 1952-1962 | read |
| §5 | budget "so that it cannot make every day a hurricane" | built otherwise | defaults 48/48 (`director.py:125-128`) "a tuning point, not a constraint" | read |
| §5 | the cadence glass or watch | built as specified | `director()` 1413-1415 | read |
| §5 | the director's own lines wake it not | built (attribute exists) | `harness.py:683, 1369-1399` | grep |
| §6 | the log hidden from every station and the player, revealed on request | built as specified | `log_of`, `reveal`, `noticed_reveal` 1584-1632 | read |
| §6 | the log inline in replays, two stories | built as specified | `two_stories` 1635-1648 | read |
| §6 | kept in the save as a station's journal | built (claimed by truth 7b-94) | `tests/test_known_truths.py:5650` | test name only |
| §7 | truths 7b-90 to 7b-94 | built as tests, against the fake only | `test_known_truths.py:5517-5650` | grep |
| §8 | person made from words, moved, bound; doubt beyond boat's reach (6 nm) | built as specified | `_make_person` 1804, `BOAT_REACH_NM` 1697 | grep, read |
| §8 | a person aboard another ship refused | built as specified | `_ship_said` 1739 | grep |
| §9 | `say as` anyone nobody holds; never a held station | built as specified | `reach` 2600-2614 | read |
| §9 | the rule of reach covers moving and binding a held person | built as specified, but not his body | `reach` 2615-2633; `_fx_person_hurt` 3609-3631 has no reach check | read; probe 2 |
| §9 | ask/tell an unseated person waits for the director, a glass bound | built (names exist) | `ask_unheld`, `QUESTION_BOUND_S` 2206 | grep |
| §11 | `ship: none` / `director: observe`, readings "no ship followed", follow/look at | built as specified (by package 82) | `tests/test_observer.py` 65-304 | test names |
| §12 | the player at a station on another ship, replay by both roads | built (by 82, 84) | `PlayerSeat.move_to` exists | grep |
| §12a | the director's own chart, by truth | **not built** | `tools.py:1598` (`at_director` words: the player's chart) | grep |
| §12b | focus, ships' logs by kind, demoted ship's sealed log | built in part | `read_log(ship=)` yes (`tools.py:1622`); kind, focus, sealed log: grep nothing | grep |
| §12b | a far ship's short story | built | `Vessel.story` (`ships.py:672`) | grep |
| §14 | places aboard and ashore, movement, what a man can do where | built as specified | `movement.check`, `PORT_PLACES` | grep |
| §14 | the place's knowledge (package 65) | built, and contradicts §15 | `world/knowledge.py` 1,248 lines | wc |
| §16 | the papers kept in a place "not built" | built (by 65), contradicting §16 | `knowledge.paper_place` 1179-1227 | grep |
| §16 | books drafted, posted, given to the boat | built (names exist) | `world/books.py` 475 | wc, grep |
| §17 | the equal reach; several officers; the deck by the watch bill | built (names exist) | `tools.reach_order`, `STATION_ALIASES`, `agents/watches.py` | grep |
| §17a | things, free lines, transactions; no setter of the purse | built as specified | `things.py`, `orders/free.py`, `Purse.receive`, `read_sum` | grep |
| §19 | the ration from the 1806 Regulations, figures "to be checked", sugar left out | built in part (the spec says so) | `data/crew/ration.yaml` | spec 1574-1576 |
| §20 | three needs in steps, notable/urgent lines to the stationed person only | built (names exist) | `NeedsKeeper`, `harness.ASLEEP_BELOW` 399 | grep |
| §20 | the ends (death, collapse, surgeon) are M7's | overtaken in part | `world.health.hit` used by `_fx_person_hurt` 3627: M7's health is in the tree | read |
| §21a | fishing, one catch function at both details | built (names exist) | `fishing.take`, `far_work`, `FAR_ONLY_ROLES` | grep |
| §21b | the glass by tiers | built (names exist) | `lookout.glass_tier`, `glass_on` | grep |
| §21d-f | the harbour, settings, the scenario maker | built; the refinement (64) struck for 96 | `ui/harbour.py` 1,236, `settings.py` 566 | wc |
| §21g-h | a ship bought (package 60), truths 99c, 99d | **not built** | grep `for sale at\|buy the ship\|transfer the people`: nothing | grep |
| §21i-j | the land-avoiding route (61), truth 99e | **not built** | no route graph found by grep in `freesail/world/` | grep (cannot rule out a differently named one) |
| §21k | the boat as a vessel, the oar force, the tow | built (by 82) | `physics/oars.py` 130, `world/boats.py` 1,036 | wc |
| §21k | the boat lost by the director's `aboard:` | built, and kills under "nobody dies" | `_fx_boat_lost` 3672; `lose_boat` 893-927 sets `p.dead = True` for people in her; `aboard.yaml` `boat_swamped` `harm: none` | read |
| §22 | the consent brief revised for the milestone | not built | `consent.DRILL_WALK = False` (`consent.py:244`) "off until package 55 re-briefs" | grep |
| §23 | gate 7b | not run (the spec carries no result) | | spec 2143-2150 |

## 2. The pointers

I checked some 110 names the specification gives (functions, constants, classes, test
names) by grep over `freesail/ tests/ tools/`: every one exists under its name; three
(`Harness._own_lines`, `_lapsed`, `_replied_tick`) are attributes, not functions, which the
spec does not claim otherwise. Twenty read for behaviour: `direct`'s order (budget, reach,
brief, form, doubt) holds as §3-§5 say; `limit_of` holds for wind and war; `_enemy_heavier`
holds for the words the ranking knows and fails for "line-of-battle ship"; `nobody_dies`
holds only vacuously; `_hand_reach` holds; `reach` holds for `say` and `person` but the
spec's general reading ("the director ... cannot move the player's ship", and the brief's "no
order goes through ... any of the player's own ship") is not what `reach` checks; the fake's
behaviour is as `fake.py` says; `DIRECTOR_DOMAIN` holds. **19 of 20 hold; the one that does
not is the station brief's own promise against `captain:`** (`director.py:1305-1307` vs
`918-924`).

## 3. The numbers

- 965 hPa at 450 km blows 42 knots, 1000 hPa 16 (spec 489-490): python gives 41.2 and 16.0
  (default background). Held by no test I found by name; truth 7b-90 holds the refusal.
- The starters' acts a day (4, 6, 8, 6): the data say 48, 48, 72, 72. Not held to the spec.
- `BOAT_REACH_NM` 6, `HAND_ANCHOR_FATHOMS` 30, `HAND_GALE_KN` 34, `HARBOUR_NM` 1.5: as the
  spec says (`orders.py:1697, 4204-4205, 621`).
- The needs' steps (hunger 12/30/40/48 h etc.) and 7b-103's "water 99 tons for 94.5 days,
  provisions for 119 days": held by truth 7b-103/104 by their names; not run.

## 4. The open items (named in the spec as unbuilt, deferred, not taken or provisional)

Still open or dropped unless marked:

1. The director seated in a ship (62's second item): not built (spec 407-408).
2. The director's own chart (§12a): not built.
3. Focus and unfocus (§12b): not built.
4. `read_log` by kind family (§12b): not built.
5. A demoted ship's sealed log (§12b): not found.
6. Truths 98, 99 under those numbers: covered otherwise (7-322 to 7-334 per the spec; `test_observer.py`).
7. Truths 99a, 99b: not built.
8. A ship bought, package 60 (§21g), truths 99c, 99d: not built.
9. The land-avoiding route, package 61 (§21i), truth 99e: not built.
10. The consent revision (§22): not built.
11. Gate 7b (§23): not run.
12. Package 55 (the solo director, the local-model director's run, the directed regatta): cannot tell; no directed regatta found.
13. Package 64, the harbour's second pass: struck for 96.
14. `the_chart_as_it_is` refuses nothing.
15. `nobody_dies` refuses nothing (no deadly thing in the table).
16. R-41's second case (a reason that does not answer the doubt still overrides): not taken.
17. The hard half of 61 (a route laid clear of the land): not taken.
18. "whaler" and the forms the directors asked for (R-42): not taken.
19. The free intent: provisional; the owner's open question (refuse an unreadable intent?) open.
20. The summed field's seasonal bound and the climatology's drift onto Iberia: kept out to M7.
21. A person aboard another ship as a seat or a voice: refused, not built.
22. Binding a person to another crewed ship's World: not taken.
23. Moving a held person "the lead's to confirm" (spec 806-807): open.
24. Things: weight in boat or hold, value at market, search, locks and seals: not done.
25. The waterman's fare by port: not data.
26. The ration's figures from the OCR "to be checked", the sugar column left out.
27. The needs' ends and the surgeon: to M7 (part of M7's health is already in).
28. The papers kept in a place: §16 says not built; package 65 built it (contradiction).
29. The drill's walk: built behind `DRILL_WALK`, off.
30. The tow's "half a knot" for the lugger: put to the owner (spec 2115-2117).
31. The gale trials' expected failures (57, 58b): left for the lead.
32. §25: two directors competing; the supply-and-demand loop; the orders system's review.
33. §26: the chart's drawn coast at the harbours (Bas, Santoña, Passages).
34. §26 from M6: the Goulet on a flood, Torbay's stream, the held gauges' blend, the deep-sea tiles' rule.
35. §26: the test battery's cost; the orders review (deferred again).
36. The director's chart words: "a director's own chart is a package to come" (spec 93).

Thirty-six items, ten of them whole features. A milestone of five parts named in its
opening has grown to ten parts (7b-vi to 7b-x) and carries its own unbuilt tail.

## 5. The document as a document

- It is mostly history. The commitments (§2-§21) are each followed by one to five "As built
  (package N; the cold review of ..., R-xx)" paragraphs, dated and attributed, which say what
  was done, taken another way, found and mended. A newcomer could not build from it; he could
  maintain from it only by reading every "as built" in order, because later ones overrule
  earlier ones (§3's starter budgets, §15 against package 65, §16 against package 65).
- It contradicts itself: §15 "Locational knowledge ... is dropped" (1224-1229) beside §14's
  package 65 built whole (1095-1172); §16 "The papers kept in a place are not built" (1274)
  beside §14's "Books, papers and pictures in their places" (1141-1149); §4's "four acts a
  day" (496) against the data's 48.
- It contradicts the proposal it serves: the proposal's director "cannot ... countermand an
  order"; the director's form table offers `captain: intent` to the followed ship
  (`director.py:918-924`), and the spec nowhere reconciles §3's channel list (which leaves
  out `captain:`, though `CHANNELS` carries it) with its own rule.
- The spec does not record that the milestone was frozen open with its gate not run
  (decision 51): §23 is an outline and §24's last line ("Gate 7b after 55") stands.
- It names the builder models of each package by vendor name (§24); not repeated here.
- It is still the truth about the code where it names things: every pointer I tried exists.

## 6. What the specification never asked for

- The world-order channel carries M7's sets and proceedings: `squadron`, `convoy`, `cartel`,
  `court`, `command` (`orders.py:137-148`), each with its own doubt (`orders.py:4115-4124`),
  none of them in this spec and none judged by the brief's limits (`limit_of` names weather,
  ship, aboard, port only).
- The aboard table grew to 34 entries including the people's health (`man_taken_ill`,
  `fever_in_the_ship`, `person_hurt`, `person_badly_hurt`, `surgeon_taken_ill`) and the boat
  lost (packages 73 and 82): bodily harm by the director's hand, with `harm: hurt` or `harm:
  none`, which `nobody_dies` does not refuse.
- What the spec's own logic needed and nobody wrote: the rule of reach for a held person's
  body; a limit (or a refusal) for `captain:` from the director; a test that the director
  cannot touch the player's ship by any channel (there is one for the hand only, truth
  7b-113).

## The ten findings that matter

1. **The director can sail the player's ship.** `captain: intent <words>` at the director's
   door is performed on the player's own ship while he holds it at the prompt: no reach, no
   doubt, no limit; the probe set her spanker and topgallants and turned her from west to NE.
   `captain: carry on` undoes the player's own hand. The director's form table advertises it.
   `orders.py:390-416, 2595`; `director.py:918-924`. Weight high; sure.
2. **The rule of reach does not cover a held person's body.** `aboard: Captain Bowen is badly
   hurt [reason: probe]` wounded the player's own captain "dangerously" under a `nobody_dies`
   brief. `orders.py:3609-3631`, `aboard.yaml` `harm: hurt`. Weight high; sure.
3. **"No enemy heavier than a cutter" lets a seventy-four through** when she is called "a
   line-of-battle ship": `size_rank_of` returns None and the limit passes, while the ship
   maker reads her as a ship of the line. `director.py:420-422`. Weight medium-high; sure.
4. **Two of the brief's limits are empty.** `nobody_dies` refuses only `harm: deadly`, which no
   entry has, while `boat_swamped` (`harm: none`) kills whoever is in the boat (`boats.py:909-
   915`); `the_chart_as_it_is` refuses nothing. Weight medium; sure.
5. **The machinery has been driven only by a script that cannot judge.** The fake plays a list
   and re-enters every doubt with a canned reason; no real model's director run is in the
   tests. The guardrails a real model would test (finding 1) were never tried. `fake.py:558-
   617`. Weight medium; sure.
6. **"Small once both exist" became about 3,500 lines for the director proper and some 16,000
   for the milestone's new modules, with about 12,000 lines of tests and a 182,000-character
   spec**, before the growth in `orders.py` (4,746) and the shared harness. Weight medium
   (cost of upkeep); likely (by file, history unusable).
7. **The budget is not a guardrail.** The spec's starters had four to eight acts a day "so that
   it cannot make every day a hurricane"; the data give 48 to 72, by the owner's word "a tuning
   point". `data/director/briefs/*.yaml`. Weight medium; sure.
8. **Ten named features are unbuilt**: the director seated in a ship, its own chart, focus, the
   log by kind, the sealed log, a ship bought, the route, the consent revision, the gate, the
   solo director; 36 open items in all (§4). Weight medium; sure.
9. **The specification contradicts itself and is mostly history**: §15 and §16 say "dropped"
   and "not built" for what package 65 built; §4's budgets are overruled by data; decision 51's
   freeze is not recorded. Weight medium; sure.
10. **The director's channel carries M7's orders (squadron, convoy, cartel, court, command) with
    no brief limit over any of them**, scope the spec never asked for. `orders.py:137-148`,
    `director.py:322-357`. Weight low-medium; sure.

## What I did not read

- `freesail/agents/director.py` lines 580-1240 (the forms table: read only 905-935) and
  2060-2381 (dry run, questions) beyond their outline; `world/orders.py` beyond the ranges
  named at the head (about 2,800 of 4,746 lines unread); `seats.py`, `crews.py`, `harness.py`,
  `tools.py`, `remote.py`, `api/readings.py`, `people.py`, `movement.py`, `things.py`,
  `free.py`, `needs.py`, `victuals.py`, `knowledge.py`, `reports.py`, `fishing.py`,
  `harbour.py`, `settings.py`, `boats.py` read by grep and outline only.
- No test read whole; the truths judged by their names and the spec's account of them.
- Not probed: the seat on the player's own ship as a road to sail orders through the watch
  bill (a suspicion); whether a grave wound can kill under M7's health; the summed-field wind
  of two appended systems against the limit.
- `docs/DesignProposal.md` not read; the proposal's words are taken from the task.
