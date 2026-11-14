# Code reader 05b: `freesail/agents/`, the second half

The tree is checked out at 89a6f72. `git diff --stat 504a2506..HEAD -- freesail tests tools data` is empty, so the code is the code under review. This file adds to `code-05-agents.md` and does not repeat its findings. Where one of mine touches one of the first reader's, I say so and add only what is new.

**What I read.**

- Whole: `director.py` (2,381 lines), `tripwires.py` (349), `watches.py` (113).
- `harness.py`, the ranges the first reader left: 1186-2490 (take-over, the tick, the stand-by's ending, wakes and reach, the sample and its deltas, the station's line, the director's notices, the fold), 2830-3133 (the shelf, the aside, the welfare counters), 3474-4149 (door acts, the deck, the grants, the handover and its fold, reseat), 4149-4739 (the stand-by, sleep, answers, questions, words) and 5060-5571 (restore's end, the seating rule, holders, the module's helpers). With the first reader's ranges, that is the whole file.
- `tools.py`: 1-760, 1150-1600, 1600-1932 (the table) and 2100-3253 (books, the library's pages, the grammar, the standing dialect).
- `agent.py`: 1-300 and 1276-2245 (every station brief and its factory, places, the voyage words, the brief's shared words).
- `local.py`: 774-870 and 1250-1660 (the budget, `main`, `run`).
- `api.py`: 540-1236 (the messages, the request, the reply, OpenRouter, `main`).
- `mcp_server.py`: 1239-1467 (the tool wrapper, `build_server`, `main`).
- `remote.py`: 262-417 and 1250-1754 (the seat, the library and stations endpoints, `GameClient`).
- `docs/agents/Harness.md`: sections 8-15, 20-21b and 22, sampled, with greps over the rest.
- For the director's road: `world/orders.py` `reach`, `_hand_reach`, `_aboard_reach`, `_taken`, `_doubt_taken` and `form_error`; `data/director/aboard.yaml`'s health entries; `core/world.py` `follow`.

**What I ran.** No test suite. I ran six short Python scripts, each under a minute, against `tests/test_director.directed` (the frigate at seed 7 off the Lizard under the quiet-passage brief), and they are quoted below. I tried a seventh, a long director run to see whether the handover note is asked for, and stopped it when the machine ran short of memory. The claim it was meant to test is marked *likely*.

## 1. What it is

**The director** (`director.py`) is a station above the game, held by the player, by a model through any door, or by nobody. Its main parts:

- `DirectorBrief` (199-357): the player's brief, with its tone, limits, cadence and budget. `limit_of` is where the limits are enforced.
- `WORLD_ORDER_FORMS` (595-1047): 41 forms with 96 examples, the one table that the station brief, the library's grammar page and the starter briefs are drawn from.
- `world_page` (1088-1237): a library page of the world's behaviour, its figures read from the code's constants.
- `DIRECTOR_BRIEF` and `SEAT_AND_CHANNEL_BRIEF` (1243-1403): about 13,000 characters of fixed brief.
- `DayBudget`, `renew`, `count_sample` and `_hold` (1444-1567): samples and acts per day of the ship's calendar.
- The hidden log (1575-1648): the `director` journal on the player's hull. `reveal` and `two_stories` read it out.
- The player-director channel (1651-1785).
- The harbour's seat doors (1788-1836).
- `direct` (1892-2049): the one road for every director order.
- `dry_run` (2064-2157): performs the order on a pickled copy of the world (`_would_do`, 2165).
- The unheld person's voice (2199-2381): `ask_unheld`, `answer_questions`.

It is called by `tools.world_order`/`truth` (a model), `ui/console.py` and `ui/server.py` (the player's `director:` words, `the director's log`, `two stories`, the `/api/director/*` endpoints), `ui/harbour.py` (briefs, seats), `core/world.py` (`noticed_reveal`), `world/orders.py` (`answer_questions`) and the harness (`_director_notices`, `_stations_notes`).

The data: `data/director/briefs/*.yaml` and `aboard.yaml`, 548 lines in all. The tests: `tests/test_director.py` (1,823 lines), parts of `test_world_orders.py` (1,070), `test_fight.py`, `test_prize_scenarios.py` (227) and `test_orders_places.py` (482, the deck passing). Sixteen test files import the director, tripwires or watches.

**The stand-by's tripwires** (`tripwires.py`): seven waits on the ship's own state. They are her way settled, depth, speed under and over, wind, a point of interest and a sail within cables. Only `harness._one_stand_by` and `_in_flight` reach them (`harness.py:4183`, `1785`).

**The watch bill's deck passing** (`watches.py`): `World.tick` calls it every tick (`core/world.py:2505`). It does nothing unless two stations are held, someone is mustered and the hour has turned (`watches.py:60-70`).

**The harness's second half** (read for the questions put):

- the stand-by and its wakes (`_stand_by_ended` 1487, `_in_flight` 1743, `stand_by` 4241);
- the sample with its deltas (`_build_sample` 1922, `_as_told` 2045);
- the shelf (2830-3013) and the welfare counters (3017-3131);
- the deck and the grants (3583-3826) and the handover (3827-4022);
- reseat (4026-4145) and the one seating rule (`seating` 5227, `barred` 5216).

## 2. Is it reached?

Reached in play:

- `direct`, through a model's `world_order` (`tools.py:491-508`) and the player's director seat (`seat.py:106`; the harbour's `SEATS` includes "director", `ui/harbour.py:86`).
- `reveal` and `two_stories`, at both drivers (`server.py:709-715`, `console.py:698-709`).
- `set_budget` and `brief_in_words`, through `console.give_director_brief` (`console.py:284-316`), which both drivers call (`server.py:724, 1826`).
- `uncallable_seat`, at `server.py` only.
- The tripwires: reached whenever a model stands by for one.
- `watches.tick`: on every tick, but it does nothing below two held officer stations. The only setting-up of two held officers I can find is in a test (`test_orders_places.py:350-358`). Reaching it in play takes a model at one officer's station and the player or another model at another.

Not reached at all (greps of `freesail/`, `tools/` and `tests/`):

- `tripwires.points_within` has no caller outside its own module (an internal helper, fine).
- `director.KINDS` lists the kinds of the log, but `direct` writes a kind it does not list, `director.follow` (`director.py:1921`). Low.

No test calls these by name (`grep -rlw` gives 0 test files): `brief_in_words`, `player_word`, `uncallable_seat`, `ask_unheld`, `noticed_reveal`, `held_officers`, `_as_the_officers_call`, `allow_general`, `take_up_after_replay`. Some are reached through driver words in tests (`director: brief` appears in `test_director.py` and `test_primer.py`).

## 3. Built more than once

- **Who is "held", by hull.** The seating rule's bar (`barred`, `harness.py:5216-5224`) and the latest-leaving search (`5256-5260`) walk `world.agents`, which is per hull (`world/hulls.py:145`). Everything else that asks "every harness of the game" walks `harnesses_of` or `all_agents` (`5390-5425`).
  - Today: `Desk.station` calls `seating(world, ...)` with the hull of the station asked for (`remote.py:485-493, 565`). So an identity that left "for good" on one hull is not barred on another.
  - The words given to the model say otherwise: `opt_out` says "not seated again in this game, at any station" (`tools.py:1430-1435`), and so does `seating`'s docstring.
  - Joining them is one line: walk `harnesses_of(world_of(world))`.
  - Likely; traced, not run.
- **The director's handover.**
  - `tool_names` withholds `handover_note` at the director's station: "no handover above the game" (`tools.py:1944-1947`).
  - `_say_handover` has a branch for the director's handover (`harness.py:3901-3911`).
  - `_ask_for_handover` asks every station with authority, the director among them (`Authority.DIRECTOR` is not `NONE`, `agent.py:965`; `harness.py:3964`), to "write the watch's handover note with handover_note(note)" (`HANDOVER_ASK`, `harness.py:509-515`).
  - These three disagree: the director is asked for a call it is not offered. See also 5f.
- **The figures in the prose.**
  - `world_page` reads every figure from a constant.
  - The grammar page and the station briefs hard-code theirs: "false for five minutes" against `standing/rules.py:44 STANDING_DWELL_S = 300` (`tools.py:3203-3205`); "four cables" for the hail (`tools.py:2589-2594`, `agent.py:2173`); "ten real minutes" and "three times" in six station briefs against `WELFARE_UNATTENDED_REAL_S` and `WELFARE_REPEAT_N` (`agent.py:1290-1296, 1361-1374`, and the rest).
  - All agree today. Each will drift alone.
- **The order a director gives, and its dry run.** `direct` (1892-2049) and `dry_run` (2064-2157) each write out the same judgement in the same order: budget, reach, brief, form, doubt. They are two copies of one sequence. They already differ: `dry_run` reads the budget without renewing it, and treats `follow` differently. A change to the order of judgement has to be made in both.

## 4. Size and shape

- Long functions in this half:
  - `director.direct` 158 lines, `world_page` 150, `dry_run` 94, `ask_unheld` 77;
  - `Harness._welfare_fire` 79, `_reseat_now` 78, `_in_flight` 72, `stand_by` 72, `_stand_by_ended` 69, `_build_sample` 68;
  - `tools.standing_dialect_lines` 95, `_contents` 91, `_grammar_topic` 89.
- **Prose for the models is a large share of the code.**
  - In `director.py`, lines 595-1403 (34% of the file) are text for the models: the forms, the world page and the brief. On top of that are 208 docstring lines and 117 comment lines, with 42 "package N" citations.
  - The station briefs in `agent.py` run 1,575 to 6,149 characters each; the tool descriptions, 16,012 characters; the grammar page, about 25,960 tokens whole.
  - The rules live twice: in code, and in prose that tells the model about the code. Section 5 finds three places where they have come apart.
- `dry_run` pickles the whole world through the checkpoint code at every call (`director.py:2178`). The dry run is the brief's own advice before every order ("world_order(text, dry_run=true) tells you what an order would do"), so a cautious director pays a full checkpoint per order it considers. I did not time it.
- Module-level state: `_LISTENERS` and `_SEAT_DOORS` (weak-keyed, already noted by the first reader), and `_starter`'s `lru_cache` of brief files (`director.py:431`). The cache is never invalidated, so a starter file edited while the game runs is not re-read. Low.

## 5. Correctness and honesty

### 5a. What a director can do, and whether it reaches the player's ship and crew

The station brief says: "You cannot move the player's ship, change a sail or countermand an order ... no order goes through a captain a model or the player holds, nor any of the player's own ship" (`director.py:1305-1321`). The module docstring says the same (`director.py:6-9`). The code keeps only part of it. The rule of reach (`world/orders.py:2580-2647`) checks the hand (`ship "X": order ...`), `say as`, `person:` moves and bindings, and things or money into or out of a held person's keeping. It does not check the rest of what follows.

1. **The player's own ship can be made to strike.**

   ```python
   w = directed("quiet-passage")   # brief: nobody_dies, no enemy heavier than a cutter
   for _ in range(120): w.tick()
   D.direct(w, 'ship: a cutter "Lark" of Britain at 49 31 N 5 31 W, bound for Plymouth')      # doubted
   D.direct(w, '... [reason: x]')                                                                # Done
   D.direct(w, 'ship "the ship": struck to the Lark')                                            # doubted
   D.direct(w, 'ship "the ship": struck to the Lark [reason: the story wants a captivity]')
   -> Done: Amazon struck to Lark: Mr Newton and 6 hands aboard her, 264 of her people prisoners, bound for Falmouth
   play log: "... The drivers follow Captain Bowen aboard the Lark ... Captain Bowen, lately commanding the Amazon, is brought aboard a prisoner ..."
   ```

   - `reach` returns None for `ship.struck`: only the hand is checked for the ship channel (`world/orders.py:2585-2591`).
   - `limit_of` looks only at `ship.new` and false colours (`director.py:334-345`).
   - `_doubt_taken` only doubts after the first minute (`world/orders.py:739-749`), and a doubt yields to a reason.
   - So a director model turned the player's 36-gun frigate over to a friendly 7-man cutter, and made the player's captain a prisoner. It took three acts, under the gentlest starter brief.
   - The form is listed to the model among its forms ("the player's own by her name or 'the ship'", `director.py:986-994`).
   - High; sure (shown).
2. **A held person can be wounded, gravely, under "nobody dies".**
   - With the player holding the captain (`held: the captain (Captain Bowen, the player at the prompt)`), `aboard: Captain Bowen is badly hurt` was doubted, then performed with a reason: `Done: found aboard: Captain Bowen wounded (a fall from the gangway, dangerously)`.
   - The table entry is marked `harm: hurt` (`aboard.yaml` `person_badly_hurt`), but a grave wound kills 30% treated and 60% untreated (`crew/health.py:84-85`).
   - `nobody_dies` refuses only entries marked `deadly` (`director.py:338-341`), and **no entry in `aboard.yaml` is `deadly`**: the one hit for the word is the comment at line 62.
   - All six starter briefs set `nobody_dies: true`. The limit refuses nothing.
   - `_aboard_reach` (`world/orders.py:3167-3221`) does not ask whether the person hurt is held.
   - High; sure (shown, and grep).
3. **The player's prompt can be moved to another ship.**

   ```python
   D.direct(w, 'ship "Lark": intent trade from Falmouth to Plymouth')   # Done
   D.direct(w, 'follow "Lark"')            -> "Following the Lark."
   acts used: 2 | world.ship now: Lark
   w.submit("heave to")                    -> "Order: heave to."
   ```

   - `follow` is taken before the budget, the reach, the brief and the doubt, and counts no act (`director.py:1909-1922`).
   - After it, the World's names read the followed hull (`core/world.py:584-621`), so the player's next order goes to the Lark and not to his own ship.
   - The brief calls it "the drivers' centre moved ... a driver's line, not a world order, costing no act" (`director.py:933-942`).
   - What it does to the player's agency is not said anywhere the model reads.
   - High; sure (shown).
4. **The hard limits are thinner than the brief says.** `limits_words` lists six limits "which the channel enforces whatever you ask" (`director.py:275-310`). In code:
   - `the_chart_as_it_is` has no branch in `limit_of` at all (`director.py:322-357`). It is described to the model only.
   - `nobody_dies`: vacuous, as in 2.
   - `enemy_heaviest` is checked only on `ship.new` (`_SHIP_NEW`, `director.py:410`). It is not checked on `ship "<name>": commissioned for ...` (a ship in ordinary put into service) or `convoy:`, and not on the hand turning a heavier enemy already at sea onto the player (`ship "Medusa": order give chase`). Likely; read, not run.
   - `wind_max_kn` judges the ordered system's own anomaly against the background (`_peak_wind_kn`, `director.py:375-401`) and ignores every system already present. The world page tells the model that "systems add" (`director.py:1101-1103`), so two lows each under the limit can make more wind than it. Likely; read, not run.
   - `the_war_as_it_is` covers only a port closed or opened to the ship's own nation (`director.py:346-356`).
5. **The doubt is a speed bump, enforced in code but never a refusal.**
   - An order that has been doubted once in the log may be entered again with any `[reason: ...]` and is performed (`director.py:2000-2016`).
   - The only guard is that a reason given before the doubt was shown is stripped (`_doubt_shown`, 2190-2196). That is a text-prefix scan of the whole log at each order.
   - So every doubted act is two calls away, and the doubt costs nothing.
   - That is the design (decision 50), and the code keeps it. But "the channel keeps the rule with you" (`director.py:1309`) overstates what it does.

**What the hidden log holds, and who reads it when.**

- It holds every director act with its reason, doubt or refusal, the director's thoughts (its free text, `answer`), the budget, the brief, the seats, the player's channel words and the director's answers, the unheld questions, and every station's prose. That last is the first reader's finding (`harness.py:2655-2670`) and is not repeated here.
- It is kept in the save as a journal.
- No model station can read it: `read_journal` reads the caller's own station's journal (`tools.py:1399`); `the director's log` and `two stories` are the drivers' words, not orders (grep: only `console.py` and `server.py`); and `state` hides the director (`tools.py:484-486`).
- The player reads it at any time with `the director's log`, which records a driver's line and tells the director (`reveal`, `director.py:1613-1632`).
- But **`two stories` in play shows every entry inline without `reveal`** (`server.py:710-715`, `console.py:706-709`). Nothing is recorded and the director is not told. The director's brief promises "you are told in your sample when he has [asked]" (`director.py:1348-1349`). Medium for honesty to the director; sure.
- `GET /api/director/log` records a reveal: a GET with a side effect (`server.py:1538-1546`). A reload or a prefetch tells the director the player looked. Low; sure.

### 5b. The welfare detector

The detector lives in the harness (`_note_submission` 3087, `_note_given` 3099, `_count_empty` 3047, the silence branches in `_end_sample` 2790-2830 and `_while_open` 1401-1423, `_welfare_fire` 3133, the pause and `check_unattended`, which the first reader read).

What it measures is **the model's own acts**, never the world's stillness:

- the same order text three times with an unchanged digest of the readings (`tools.readings_digest`, `tools.py:344-353`: the readings' words less the clock rows and the stores);
- three undoing orders in a chain within a watch;
- three empty or prose-only replies where an answer was owed;
- no reply at all (no text and no call) for the station's patience;
- three danger orders.

So a station that changes nothing for hours **for good reason** is not mistaken for a loop:

- a ship hove to, at anchor or becalmed, whose model stands by or replies with a word;
- with the deck, the stand-by is bounded (a glass at most, an event ending at eight bells, `harness.py:4251-4274`), but any call or text counts as a reply (`2587-2588`), so the silence count does not run;
- standing by resets the repeat count (`4306`).

The digest is the one place where game state enters: "no change in the readings" is what makes a repeat a loop. Two weaknesses:

- **The repeat count has no time window.** It is reset only by another order, a different digest, a stand-by or a reseat (`harness.py:3087-3097`). So at anchor or becalmed, where the readings' words are steady, a model that gives the same routine order in successive samples without standing by ('heave the lead', 'sound the well') would be nudged at the third and paused at the fourth, hours apart. A suspicion; I did not run it.
- **The count is taken before the authority check.** `_note_submission` runs in `_call` before `tools.call` refuses an order (`harness.py:2747-2751`). So a station's refused orders count as repeats. That matters at once for the watcher; see 5c.

The pause "asks the human" by a log line; the first reader found that nothing checks whether anyone is there. Nothing to add.

### 5c. The watcher is told to speak by a tool that refuses it

- `WATCHER_BRIEF`: "what the deck must hear you say with submit_order('say <words>')" (`agent.py:1281-1282`).
- The watcher's authority is `NONE` (`agent.py:1313`), and `submit_order` `needs_authority` (`tools.py:1690`). The authority check comes before every exemption (`tools.py:2015-2025`).
- Shown: `call(w, "watcher", "submit_order", {"text": "say the glass is falling"})` gives `The watcher has no authority to give orders.`, and the tool is in the watcher's offered list (`offered submit_order: True`).
- The watcher is the station the stock doors default to (`--station watcher`). Its brief's one road into the world is closed. Each attempt logs an `agent.refused` line, and by 5b three identical attempts bring the nudge and then the pause.
- Medium; sure (shown).

### 5d. The harness speaks in a held officer's name

`_as_the_officers_call` (`harness.py:1557-1585`) writes a NOTABLE `report.called` line, "*Mr Pearce* sends down to the captain: her way settled", whenever a tripwire fires for a station whose person cannot read its rows. It names the holder of the officer of the watch's station whoever holds it: the rules, the player, or a model that said nothing. That cuts across the rule the director is held to, that nobody speaks as a held station (`world/orders.py:2595-2612`). The line is notable, so it wakes other stations standing by for a notable line. Medium-low; sure by reading, not run.

### 5e. The handover and the context budget

There are three mechanisms, which do not know of each other:

1. **The harness asks.** `_ask_for_handover` (`harness.py:3959-3974`) measures the conversation since the latest brief as the larger of four characters a token and the server's last prompt count plus what came after (`_conversation_size`, 3920-3938). When that reaches the budget less the reserve, but never before 0.6 of it, the next sample carries `HANDOVER_ASK`. The fold happens only if the model then writes `handover_note`. The fold (`_fold_handover`, 3976-4022) keeps the latest brief, one turn holding the note and the readings, and the last 6 turns (`HANDOVER_KEEP_TURNS`). It leaves behind the books, the deltas' memory and the server's count.
   - It asks only stations with authority (`3964`). The watcher, the one station with `Authority.NONE`, is never asked, and nothing folds its conversation.
   - It needs `budget_tokens`, which only the runner and the API door send (`remote.py:571-589`, `local.py:1552`, `api.py:1215-1218`). The MCP door sends none, so no MCP station is ever asked (`harness.py:3949-3950`). That is defensible, since the client keeps its own copy.
   - A director is asked, but is not offered the tool (see 3). Likely: traced, not run, because my long run was stopped for memory.
2. **The local runner drops turns.** `LocalModel._budget` drops the oldest whole exchanges silently when the request will not fit (`local.py:785-849`), the brief and pinned turns kept. The model is not told what was dropped. Only `dropped_turns` is set.
3. **The API door does neither.** `ApiModel.messages` (`api.py:579-654`) sends the whole conversation from the latest operator turn on. Nothing is trimmed. A watcher or a director at the API door grows until the request is refused, and a 400 ends the seating (`api.py:829-832`, `final=True`). The only other relief is `remote.py:1086`, which folds after two replies are cut off at the reply limit (a different failure).

So the context budget is enforced for some stations at some doors, by mechanisms the model may not be told of. Medium; sure for 2 and 3, likely for the director's case.

### 5f. Smaller points

- `mcp_server.build_server` decides the director's tool set by `bridge.game.name == "director"` (`mcp_server.py:1287`). That is the raw `--station` text, but the desk normalises the station's name (`station_name`, lower-cased). `--station Director` would seat the director and offer the ship's tools, with no `world_order` and no `truth`. Low; likely.
- `parameters_schema` types a parameter "integer" or "boolean" by the first word of its description, and everything else "string" (`tools.py:1960-1981`). `truth`'s `within` is described as "number" and so is sent as a string. `truth` accepts it (`float(within)`, `tools.py:556`), so this is harmless today. Low.
- `watches._pass` puts the relief on the quarterdeck in a step: `relief.where = "quarterdeck"; relief.up = True` (`watches.py:99-101`). It bypasses the people's own moving and the needs keeper's waking. A relief asleep below is on deck at the turn of the hour. Low; sure by reading.
- `tripwires.py`'s docstring lists six tripwires; the code has seven (`TRIPWIRE_WORDS` adds "a sail within <n> cables", `tripwires.py:80-88`). Harness.md §21b lists the same six. Low.
- `DEFAULT_SAMPLES_A_DAY = 48` "a sample a glass through the day and the night" (`director.py:122-125`), but the director is also sampled on every notable and urgent line (`director.py:1415`). So on a busy day the default budget is spent before midnight, and the director goes unsampled until the ship's calendar turns. Likely; not run.

Determinism: nothing in this half reads the wall clock or an unseeded random. The dry run plays its order on a copy (sound). `uncallable_seat` reads the harbour's settings at run time, but pops its own input so that a replay gives nothing (`director.py:1948-1950`). Sound.

The hard boundary: `world/orders.py` imports `freesail.agents.agent` inside `_hand_reach`, and `World.tick` runs `agents.watches.tick`. These are more instances of the first reader's 5c finding.

## 6. Thin or overgrown

Overgrown, and unevenly so.

- **The director's surface is wide.** It has 41 forms, among them courts martial, cartels, new commands written to disk, squadrons, convoys, regimes and seats for other models at the player's own stations. The forms are explained to the model at length (the brief, the world page, the grammar). But the few lines meant to protect the player's game, the limits and the reach, are narrow and partly vacuous (5a).
- **The welfare machinery is large and careful about what the model does,** and blind to what the station is for: the watcher's own brief trips it (5c).
- **The context budget is three partial mechanisms** across three doors (5e).
- **How much of this exists for stations no playtest could have used.** I cannot answer that cold: the playtests are closed to me, and the comments are the project's own account. From the code alone:
  - the deck passing between officers needs two held officer stations, and only a test sets that up;
  - the director's seats need the owner's grant and the harbour;
  - the court, cartel and command forms are scenario-start machinery.

  Each is reached in play only under a configuration I found no driver default for. The reviewer should set this against the playtest records.

## 7. What is not tested

These are greps of `tests/`:

- No test makes a director strike the player's own ship, follow another ship, or wound a held person. The one test of `struck to` on the player's ship goes through the owner's `world_order` (`test_prize_scenarios.py:146-163`), not `direct`.
- No test shows that `nobody_dies` refuses anything. Its tests only check that the briefs set it (`test_director.py:395, 589`; `test_prize_scenarios.py:91`).
- No test covers `the_chart_as_it_is`.
- No test gives the director a handover ask.
- No test gives the watcher a `say` through `submit_order`.
- No test makes `two stories` reveal or not reveal.
- No test checks `barred` across hulls.
- No test covers the API door with an over-long conversation.
- No test covers the repeat detector at anchor.
- No test names `brief_in_words`, `player_word`, `uncallable_seat`, `ask_unheld`, `noticed_reveal` or `_as_the_officers_call`.

## Harness.md §§4-18 and 20-22, fifteen samples

1. §9, the watcher "stuck (the same order three times with nothing changing, or ... no reply for a watch)": the patience is right (`A_WATCH_S`). But the watcher's orders are all refused (5c), so the first pattern can only count refusals. **True in letter, hollow.**
2. §13, "After a yes, for the officer's station only, a short drill follows": **false.** `drill=True` for the officer, the captain, the master, the lookout and the director (`agent.py:1531, 1722, 1848, 1873`; `director.py:1426`). It is false for the passenger alone.
3. §13, the handover reserve "three tenths ... never less than 14,000 tokens ... never before six tenths": true (`harness.py:341, 364-365`).
4. §13, "Silence: no reply for an hour ...; a call made inside an open turn counts as a reply": true (`OFFICER_PATIENCE_S = 2 * A_GLASS_S`; `harness.py:2587`).
5. §13, the stand-by with the deck "must name an event or a bell (an hour or a watch is refused)": true (`STAND_BY_WITH_DECK_MAX_S = A_GLASS_S`, `harness.py:332, 4251-4264`).
6. §13, the turn's budget "sixteen orders ... thirty-two reads; answer, say, opt_out, stand_down, hand_over and stand_by always run": true (`agent.py:268-269`; `harness.py:258, 268, 274`).
7. §15, the master's figure "within thirty minutes of the working is the ship's account": true (`reckoning.py:594, 604`).
8. §15, the lookout's "cadence is the masthead's lines, an urgent line and each glass": true (`agent.py:1862`).
9. §15, the log says when the clock has been held at 1x "longer than two real minutes": true (`console.py:345`; the server uses the same `Pace`).
10. §16, `--max-reply` 16,000 and `--request-timeout` 600 seconds: true (`api.py:156, 159`).
11. §17, "within four miles ... a full ship ...; beyond six miles she is demoted": true (`crews.py:90-91`).
12. §21a, "The director, above the game, is told no ship": true (`harness.py:1156`).
13. §21b, her way settled is "a quarter of a knot and ... a quarter of a point for two minutes, measured afresh after every order": true (`tripwires.py:53-55, 262-265`). The list omits the seventh tripwire.
14. §21b, the dry run is "performing nothing, writing nothing": true (`director.py:2165-2187`, on a copy).
15. §21a, the reads made meanwhile (`truth` and `chart` at the director's station among them) do not end a stand-by: true (`remote.py:180-195`).

Thirteen are true, one is false and one is true but hollow. In this half the document is accurate on figures, as the first reader found of the first half. Where it goes wrong is on who is affected: "officer only", and the watcher's patterns.

## The ten findings that matter

1. **A director model can make the player's own ship strike.** Shown under the quiet-passage brief: the Amazon struck to a friendly 7-man cutter and her captain was taken prisoner, for three acts. The rule of reach checks only the hand (`world/orders.py:2585-2591`), and the doubt yields to a reason. This breaks the brief's "you cannot move the player's ship". High; sure.
2. **`nobody_dies` refuses nothing.** No `aboard.yaml` entry is `deadly`, so the player's own held captain was "dangerously" wounded, at 30-60% mortality (`crew/health.py:84-85`), under a brief with the limit set. All six starter briefs rely on it. High; sure.
3. **A director's `follow` moves the player's prompt to another ship.** It costs no act and is checked against nothing. Shown: the player's "heave to" went to the Lark (`director.py:1909-1922`, `core/world.py:584-621`). High; sure.
4. **The brief's hard limits are partly described only.** `the_chart_as_it_is` has no code at all. The wind limit ignores the systems already present, and the enemy limit covers only `ship.new` (`director.py:322-401`). Medium; sure for the first, likely for the others.
5. **The watcher is told to speak with `submit_order('say ...')`, which refuses it** (`agent.py:1281`, `tools.py:2015-2025`; shown). Each refusal also counts toward the repeat nudge and the pause, because the count is taken before the authority check (`harness.py:2747-2751`). Medium; sure.
6. **The context budget is three partial mechanisms.** The harness asks only stations with authority. The runner silently drops turns. The API door trims nothing, so a long watcher or director seating ends on a 400. The director is asked for a `handover_note` it is not offered (`harness.py:3964`, `tools.py:1944`, `api.py:579-654`, `local.py:785-849`). Medium; sure, the director part likely.
7. **The welfare detector measures the model's acts, not the world's stillness.** So hove to, at anchor or becalmed is told apart from a loop, as long as the model stands by or replies. But the repeat count has no time window and is reset only by another order, a stand-by or a reseat (`harness.py:3087-3097`). Low-medium; the false nudge at anchor is a suspicion.
8. **`two stories` shows the hidden log in play without a reveal.** Nothing is recorded and the director is not told, against the brief's promise (`server.py:710-715`, `console.py:706-709`, `director.py:1348`). The reveal endpoint, meanwhile, records on a GET. Medium; sure.
9. **`final` opt-out bars an identity on one hull only.** `barred` and `seating` walk `world.agents`, which is per hull, while the tool tells the model "at any station" in the game (`harness.py:5216-5260`, `tools.py:1430`). Medium for consent; likely.
10. **The harness writes NOTABLE lines in a held officer's name.** "Mr Pearce sends down to the captain: ...", whether or not the officer's holder said anything (`harness.py:1557-1585`). This is the voice the rule of reach forbids the director. Medium-low; sure by reading.

## What I did not read

- `tools.py` 760-1150 (the first reader's range, not re-read) and 1932-2100 beyond the parts quoted.
- `agent.py` 300-1276 (the domains, the policy, `Station`) and 2245-2710 (the first reader's `Brief.build` and the state classes).
- `local.py` 1-774 and 870-1250.
- `api.py` 1-540.
- `mcp_server.py` 1-1239.
- `remote.py` 1-262 and 417-1250 (the first reader's).
- `repl.py` (not in my task).
- `world/orders.py` beyond the functions named (4,746 lines; its doubt functions are not read).
- `world/seats.py` and `ui/harbour.py`.
- `docs/agents/ConsentBrief.md`: not re-read, as the first reader had checked it whole.
- Harness.md §§4-7, 16 beyond its flags, 17b, 18, 21c-21i and 22 beyond the listing.

Claims marked likely or a suspicion rest on reading without running. The long director run that would have tested the handover ask was stopped for lack of memory and not repeated.
