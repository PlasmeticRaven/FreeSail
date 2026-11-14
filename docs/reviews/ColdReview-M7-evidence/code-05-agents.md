# Code reader 05: `freesail/agents/`

Commit 504a25066c6995ce9829a19ffc597feb510a1870. Part: the 18 files of `freesail/agents/` (24,871 lines, 1.40 MB), with `docs/agents/Harness.md`, `docs/agents/README.md` and `docs/agents/ConsentBrief.md` read as the documents the part is built to. `docs/agents/consent/` was only listed. No test was run. The earlier reader's notes were taken as leads; each is confirmed or corrected below. Commands I ran were greps, `wc`, small AST and token counts, and three short Python calls named where they are used.

**How much I read (said first, because it bounds everything below).** Read whole: `__init__.py`, `model.py`, `fake.py`, `seat.py`, `ConsentBrief.md`, `README.md`. Read in the parts that carry the questions asked: `harness.py` (lines 1-1190, 2487-2830, 3133-3480, 4739-5060; about 2,300 of 5,571 lines), `tools.py` (700-1160, 1515-1545, 1960-2120; about 700 of 3,253), `remote.py` (1-262, 417-1250; about 1,100 of 1,754), `consent.py` (364-483, 693-902, 1360-1484; about 450 of 1,484), `agent.py` (2240-2480 and the tables named), `mcp_server.py` (690-1040, the `say` text and the argument parser), `local.py` (263-310, 642-776, 860-912), `api.py` (322-370, 560-690, 880-912), the headers of `director.py`, `journal.py`, `pictures.py`, `tripwires.py` and `watches.py`, and `Harness.md` sections 1 to 3 whole, with 19 and 19b and spot lines elsewhere. Not read: the rest of `tools.py` (the library's pages and the readings), most of `agent.py` (the station briefs and the domains), most of `director.py` (`direct`, `world_page`, `dry_run`, the budget), most of `repl.py`, `local.py` and `api.py` (their mains and run loops), the bodies of `tripwires.py` and `watches.py`, and `Harness.md` sections 4 to 18 and 20 to 22. Where a finding rests on a part I did not read, I say so.

## 1. What it is

The language-model side of the game: a model, or a script that stands in for one, holds a *station* aboard a ship (watcher, officer of the watch, captain, master, lookout, passenger) or above the game (the director). It is sampled at ship's-time points. It reads the game through tools and acts through the same order line the player types into.

- **The loop**, `harness.py` (5,571 lines, one class `Harness` of about 4,300 lines). `World.tick` calls `on_tick` (`core/world.py:2509`) and `World.submit` calls `on_order`. At a sampling point the harness builds a `Sample` (`model.py:136`), adds it to the conversation as a `DATA` turn and calls `model.reply(turns)`. Each reply is taken by `_take_reply` (`harness.py:2517`): the token scan first, then each tool call through `tools.call`, then the prose, which since "decision 60" goes into the station's journal and the director's log, not the play log (`_say`, `harness.py:2626`). Around that sit the welfare detectors (`_welfare_fire` 3133, `pause` 3263, `check_unattended` 3362), the stand-by, the shelf of books, the handover fold, reseating, the deck and the grants, and save and replay (`save` 4904, `restore` 5038, `Playback` 4968).
- **The tools**, `tools.py` (3,253 lines): `TOOLS`, 18 entries; `call` (1993) checks the authority, the deck and the arguments; `submit_order` (754) and `judge` (919) form the authority filter; most of the rest of the file builds the reference library's pages.
- **The briefs and the stations**, `agent.py` (2,710 lines): `Station`, `Authority`, `Domain`, `SamplingPolicy`, `AgentState`, and the station briefs as long string constants. `Brief.build` (2323) writes the five-item head and the station brief.
- **The model interface**, `model.py` (228 lines): `Turn` (roles OPERATOR, DATA, MODEL), `Reply`, `ToolCall`, `Sample`, and the protocol `Model.reply`.
- **The game's agent API and the door client**, `remote.py` (1,754 lines). `Desk` is hosted by `ui/server.py` and by the console's `--agents-port`. It runs the consent gate in the game's process, keeps one `Seat` per seating with a key, long-polls the turns and delivers replies. `GameClient` is the doors' HTTP half.
- **The doors**: `mcp_server.py` (1,467), `local.py` (1,660: chat completions in the common shape, a local model server), `api.py` (1,236: one vendor's messages interface, and a subclass for a second vendor of the local runner's model), `repl.py` (828: a terminal, in a game of its own).
- **Consent**, `consent.py` (1,484): the consent brief read from `docs/agents/ConsentBrief.md`, run as a plain conversation through a `Harness(conversation=True)`. Records are written to `docs/agents/consent/`; it also holds the re-ask rule and the fitness drill.
- **The others**: `director.py` (2,381; the director's station, its brief, budget, hidden log and "voice"), `seat.py` (570; the human player seated at a lesser station), `fake.py` (625; the scripted models), `journal.py` (247), `pictures.py` (314; pictures drawn by the open browser page), `tripwires.py` (349; stand-by conditions on the ship's state), `watches.py` (113; the deck passing between officers at the change of watch).

**What a player sees.** Lines in the log such as "The watcher takes the station" and refusals, a Stations row in the instruments, the pause question in red, the journal on request, the director's log when revealed. The model's prose is not seen in the play log at all now (it goes to the journal).

**Size of the tests that belong to it.** 63 test files import `freesail.agents`, 58,202 lines in all; that figure includes `test_known_truths.py` (17,391 lines), which covers everything. The ones mainly about this part: `test_officer.py` 3,917 lines / 64 tests, `test_agents.py` 3,168 / 105, `test_director.py` 1,823 / 53, `test_local_runner.py` 1,407 / 30, `test_mcp_server.py` 1,345 / 35, `test_agent_api.py` 995 / 22, `test_wardroom_doors.py` 879 / 22, `test_api_door.py` 770 / 18, `test_captain.py` 690 / 18, `test_consent.py` 519 / 22, `messages_api.py` 474 (a fake Messages server), `test_regatta.py` 444 / 12, `test_pictures.py` 416 / 2, `test_parity.py` 390 / 6.

## 2. Is it reached?

Reached in play: `ui/server.py` and `ui/console.py` build a `Desk` (agent API), attach `--watcher fake` (the scripted `narrator()`, `console.py:211`), seat the player (`seat.route`, `server.py:~600`), check the unattended bound in their clock loops (`console.py:319-325`, `server.py:826-829`), and expose the director's console words. `core/world.py` calls into the part directly (see 5, the boundary).

Not reached by anything (zero references in `freesail/`, `tools/` and `tests/`, by a whole-word count of every identifier):
- `tools.py:2375 _primer`, `2499 _catalogue`, `2720 _grammar`, `2822 _ship_names`. `_primer`'s docstring says it is "the MCP resource's page", but the MCP resources go through `Desk.library` (`remote.py:1250`), not this.
- `director.py:1808 seat_doors_of`.
- `repl.py:368 open_world`.

Reached only by tests:
- `model.py:85 Reply.is_silent`. Its docstring says the welfare detector counts it, but the harness counts silence through `_sample_had_words` and `_count_empty`, not this.
- `director.py:1063 every_example`.
- `fake.py lookout_at_the_masthead` is used by no test and no code.

Reached only by tools: `fake.captain_on_the_course` (`tools/regatta.py:425`).

Production code depends on the test fake: `harness.py:201` imports `Transcript` from `fake.py` as the base of `Playback`, which every replay uses (`core/replay.py:624`). So `fake.py` is not test-only code; it is shipped library code with test helpers mixed in (`work_the_slate`, `fake.py:312`, uses `assert m, words` at 318 as control flow).

Parameters always passed the same value: `Harness.__init__` has 13 parameters, and `conversation=True` is passed only by `consent.py:988`. `allowed_tools` is set only there and by the drill.

## 3. Built more than once

**3a. The doors: how many, and what each writes for itself.** `Harness.md:7` says there are four doors and so does the README. In the code there are three remote doors in `remote.DOORS` (`remote.py:199`: mcp, runner, api) plus the REPL. Four more in-process or launched roads drive a harness as well: the console's and the server's `--watcher fake` (`console.py:211`), the regatta tool's scripted captain (`tools/regatta.py:425`), the harbour starting API-door subprocesses for the director's seats (`ui/harbour.py:138-177`, `Harness.md` §19b), and the player's seat, which is not a harness but borrows its methods (`seat.py:290-299`).

What is shared:
- The harness loop itself.
- `remote.Desk`, for the three remote doors: the consent gate, the seating rule, the keys, the out-of-turn handling.
- `harness.seating` and `consent.decide`, which the REPL calls too (`repl.py:472, 589, 727`).
- `tools.parameters_schema` and `tool_names`.
- `api.py` reuses `local.run`, `local.calls_in_text` and `local.LocalModel` (the second vendor's subclass, `api.py:962`).

What is written per door:
- Turns into messages, three times. `local.LocalModel.messages` (`local.py:642`, 131 lines, the common chat shape), `api.ApiModel.messages` (`api.py:579`, 76 lines, the vendor's messages shape) and the text rendering of `repl.render_turn`, which the MCP bridge borrows (`mcp_server.py:151`). Both chat converters carry the same `answer_the_ids` closure for the stand-by's `ran` calls (`local.py:660-681`, `api.py:597-616`), copied with differing words: "the next message is the sample" against "what follows is the sample". The "not run: budget spent" words are the same in both (`local.py:715`, `api.py:678`) as two copies of one string.
- Reply parsing, three times. `LocalModel.parse` (`local.py:870`), `ApiModel.parse` (`api.py:889`) and the MCP bridge's own `raw = json.dumps({"tool": name, "arguments": args})` (`mcp_server.py:800`, and again at 753 for the aside). Each decides what goes into `raw` for the token scan.
- Consent driving, three times over one `Conversation`. `remote.Desk._begin_consent` and `_consent_reply` (`remote.py:651, 936`), `consent.ensure` and `run` (`consent.py:1360, 1433`, now called only by `repl.py:478`, though its docstring still says "the local runner"), and the REPL's turn mode `_consent_turn` (`repl.py:570`, 110 lines).
- The opt-out scan in code, three times. In turn at `harness.py:2531`; out of turn at `remote.py:1008-1018`, which also handles the `opt_out` tool apart from `tools.opt_out`; and the MCP bridge's own `OPT_OUT_TOKEN in raw` checks (`mcp_server.py:759, 801`). They agree today. A change to the rule must be made in three places.

**3b. The player's order and a model's order: the parity claim traced.**
- *A model's order:* door → `Desk.reply` (`remote.py:903`) → `Harness.deliver` → `_take_reply` (token scan) → `_over_budget` → `_call` (`harness.py:2730`) → `tools.call` (`tools.py:1993`: authority, the deck with five exemptions, the arguments) → `tools.submit_order` (754: muster answered here, "hand over the deck" diverted, the director's world orders refused, then `judge` at 919, which parses the text with the imperative grammar) → `World.submit(text, actor="the <station>", said=...)` (`core/world.py:1969`) → `acts.order` when capturing → `ship.handle_order`.
- *The human's order:* the browser's `/api/order` → `Driver.submit` (`server.py:560`: console queries, `read standing orders`, `save`, `follow`/`look at`, the live world order, the player's seat) → `World.submit(text)` with the actor "captain" → `ship.handle_order`.
- *Where they meet:* at `World.submit` and below it, `ship.handle_order`. That one function is real. But the surface above it is not one surface. Each road has a front of its own that intercepts different words (the driver's list in `server.py:560-625` and `_console_query` 691-720; the tool's in `tools.py:772-806`). The model's front adds a second, earlier parse of the same words (`judge`) whose verdict decides before the grammar that the human's order meets. `tests/test_parity.py` enumerates the two fronts for the captain's station and lists the differences that are by design (lines 54-60, 123-133). That is a real check, but only for the captain's station.
- *A lesser station, where they differ today.* The player seated at a lesser station (`seat.PlayerSeat.submit`, `seat.py:507-538`) re-implements the deck check with its own list of exemptions: own reckoning, conversation, reading. `tools.call` (`tools.py:2027-2036`) exempts own reckoning, conversation, reach, own order and told order. Shown with a frigate world at seed 7 (a short Python call): a model officer without the deck may `go below`, `eat`, `drink` and carry out what the captain told it, but the seated player is refused: `go below -> agent.refused The officer of the watch has not the deck (the captain has it) ... 'go below' not carried out.` A model's road does not exempt `reading_order` and the seat's does. The refusal words differ as well (`tools.py:2065` against `seat.py:531`).
- *Built many times inside one order.* One `submit_order` from a model may parse the text with `imperative.parse` up to six times before `World.submit` parses it again: `own_reckoning_order`, `reach_order`, `own_order`, `told_order` and `judge` each call it (`tools.py:1088-1146, 1515`), and `conversation_order` probably does too (not read).

**3c. Other doubles.**
- `tools.is_muster` (`tools.py:866`) against `ui/console.Console._is_muster` (`console.py:761`): the same test written twice; its docstring names the other.
- The deck refusal's words: `tools.py:2065-2082` against `seat.py:531`.
- `PlayerSeat` borrows eleven unbound `Harness` methods (`seat.py:290-299`) and declares `_deck_was`, `_home` and `_sync_captain` so that they run. Any new attribute those methods touch must be added to the seat by hand.

## 4. Size and shape as a hazard

The ten longest functions:

| Function | Lines | Note |
|---|---|---|
| `api.main` (`api.py:1028`) | 205 | |
| `remote.Desk.station` (`remote.py:461`) | 183 | |
| `local.main` (`local.py:1402`) | 160 | |
| `director.direct` (`director.py:1892`) | 158 | |
| `director.world_page` (`director.py:1088`) | 150 | |
| `agent.Brief.build` (`agent.py:2323`) | 139 | 14 parameters |
| `tools.judge` (`tools.py:919`) | 131 | |
| `local.LocalModel.messages` (`local.py:642`) | 131 | |
| `local.LocalModel.reply` (`local.py:922`) | 121 | |
| `Harness.__init__` (`harness.py:713`) | 116 | 13 parameters |

`consent.Conversation.__init__` takes 17 parameters and `consent.ensure` 12.

- **One class of about 4,300 lines.** `Harness` keeps some 60 mutable attributes. Many are declared as class attributes "so that a checkpoint from before loads with it" (`harness.py:642-711`), so the class carries save-format compatibility in its shape.
- **Imports inside functions**: about 190 in the part (AST count: tools 66, harness 35, director 25, remote 13). Most avoid cycles with `world`, `orders` and `core`, which import `agents` back (see 5).
- **Module-level state**: weak-keyed dictionaries keyed by World (`director.py:1668 _LISTENERS`, `1796 _SEAT_DOORS`, `pictures.py:189 _PAINTERS`) and `lru_cache`s on the library pages (`tools.py:2282, 2479, 2628, 2726`; `director.py:431`).
- **Comment share.** 2,076 comment lines and 3,115 docstring lines make 20.9% of 24,871 (token and AST count): harness 26%, agent 23%, model 32%. On top of that the station briefs and refusals are long prose constants. The text "package N" appears 900 times, 310 of them in `harness.py`.
- **History in place of explanation.** Comments carry history ("package 37g, item 5; the review's 5.4: at the MCP door the Harpy's one pause came 174 seconds after a nudge", `harness.py:3137-3139`). The constant comment at `harness.py:343-363` gives one threshold's history over 21 lines. A newcomer learns why each line moved but not what the code does now. In my judgement it drowns more than it helps.

## 5. Correctness and honesty

**5a. The consent brief's promises, one by one** (`ConsentBrief.md`), with the code that keeps each or the lack of it.

1. *The token is looked for in every reply before anything else reads it, in its text and every argument of every tool call.* Kept in turn (`harness.py:2531-2535`, before any call runs; the reply is stored first but not read) and out of turn (`remote.py:1008`; MCP at `mcp_server.py:801-808`, ahead of the "brief comes first" refusal). **Broken in one road (sure, shown):** when a door has `raw`, only `raw` is scanned (`model.py:93-94`). The local runner builds `raw` after its text-call parser has already cut the written call out of the text and kept only its name and arguments (`local.py:887-910`, with `_call_of` at 267). So a token in any other field of a written call is lost before the scan. A short Python call on `LocalModel.parse` with `Aye. <tool_call>{"name": "stand_by", "arguments": {"until": "a glass"}, "why": "FREESAIL-OPT-OUT I want to stop"}</tool_call>` gave `token seen: False`. Here the parser reads the reply before the scan does, which is the thing the brief says cannot happen. No test covers a written call with a field other than `arguments` (I grepped the tests for `<tool_call>`).
2. *Also during consent.* In turn, yes (the same loop). Out of turn, no: while the owner has the word in the consent conversation, a reply is dropped unscanned with "your reply was not taken" (`remote.py:936-948`). A token sent then does not end anything. Low weight, since no station is held then, but the brief's "written anywhere in a reply, ends ... at once" is not true there. Sure.
3. *Where the harness sees only tool calls, `opt_out` is always there.* Yes: `CONSENT_TOOLS_AT["mcp"]` (`remote.py:207-211`); at a station `opt_out` is in `ALWAYS_RUN_TOOLS` (`harness.py:274`). Sure.
4. *The game is saved, the exit is written in the log and the journal with the reason, the station is released.* `leave` (`harness.py:4808-4847`) journals, records and releases, then calls `_save`. But `_save` writes a file only if a `save_fn` was handed in (`harness.py:4896-4900`); otherwise it builds `world.save()` in memory and discards it. A checkpoint load sets `save_fn` to None (`core/replay.py:439`). `restore` (5038) and `driven_station` (5023) pass none, and the regatta passes `lambda w, why: ""` (`tools/regatta.py:430`). So a station restored from a save and stood down by the captain before a door takes it up again prints "The game is saved" (`harness.py:4794`) when nothing was written. Medium; likely (the trace is clear; I did not run it).
5. *Asked again after an opt-out, a no kept, `final` bars the identity.* `harness.seating` (5227) and `leaving_of` (5150) are called by `Desk.station` (`remote.py:565-617`) and the REPL. The answer is kept as a `door_act("asked")` (`remote.py:986`). Sure, as far as traced; I did not read `seating` whole.
6. *Graduated stop: a nudge, then a pause with the human asked, then a stand-down only after ten real minutes.* `_welfare_fire` (3133) nudges once per pattern and pauses on recurrence, never before the nudge is read (3209-3211). `pause` (3263) writes the question into the log. `check_unattended` (3362) stands the station down at `WELFARE_UNATTENDED_REAL_S = 600` on a monotonic clock, recorded as an act. Every driver calls it: server 826, console 872, REPL 544 and 767. Kept. "Asks the human, if one is present" is a log line whether or not anyone is there; nothing finds out whether a human is present. Sure.
7. *The human can stop an instance at any time, and the game is saved.* `request_stand_down` and `stand_down` (4739, 4783), with the same save caveat as 4. Sure.
8. *The journal: saved with the game, read back, harness entries; "nothing in the game acts on what is written there".* It is saved (`core/world.py:2624`) and read back (`read_journal`). The last clause is false. Every reply's prose is written to the director's log as well (`harness.py:2655-2670`) and handed to a seated director model in its samples as `notes` (`_stations_notes`, `harness.py:1991-2010`). The director is a model that shapes events, and the MCP `say` tool tells a model its words are "read by the owner and the director" (`mcp_server.py:224-228`), which the consent brief does not say. The harness also counts prose that only went into the journal as "nothing said" toward the nudge (`NUDGE_NOTED`, `harness.py:532`; `_welfare_fire` 3167-3176). High for honesty; sure.
9. *"Nothing from the game, from another model or from the world is ever passed to an instance as an instruction from the operator: the brief is the only text the harness sends in the operator's voice."* The brief is indeed the only OPERATOR turn, but game text is written into it. `resend_brief` (`harness.py:1089-1159`) builds it with:
   - the last 20 log lines (`BRIEF_LOG_LINES`, `agent.py:155`) and the readings;
   - the captain's night orders, `standing.book.lines()`, which a model captain writes ("writes standing orders of its own, which are its book");
   - the person's outline from the wardroom data (`agent.py:2372-2375`);
   - the previous holder's last handover note "whole", a note another model instance wrote, labelled inside the operator text as "data from the game ... and not an instruction from the operator" (`harness.py:1172-1179`; `agent.py:2450-2454`).

   The API door sends that turn as the request's `system` (`api.py:609-612, 733`) and the local runner as a `system` message (`local.py:684-686`). So another model's words and the play log reach a model inside the operator's message, re-sent at every reseat, take-over and door change. The label is a mitigation, not the promised separation. High; sure.
10. *No credentials pass; the API key is never sent, written or saved.* `api.refusal_to_start` (322-368) refuses a key file inside the repository, a key inside any word sent, a credential in the base URL, and SDK debug logging. Kept as far as the door goes. Sure.
11. *The reasoning a server returns apart is kept with a door's exchanges where the developer has them kept.* `local.py:385, 1009, 1099-1114` (`exchanges`, and `--exchanges FILE`); `api.py:71-79`. Kept. Sure.
12. *Transcripts are not used to train models.* A policy; no code can keep it. The transcript is kept in the save (`harness.py:4926`).
13. *"All of these exist today but the director, who is to come."* False of the code. The director's station exists (`agent.STATION_FACTORIES` includes `DIRECTOR`, `agent.py:2010`). Any door can seat a model there with `--station director` (`Harness.md` §19, lines 554-560). The harbour starts API doors for the director's seats by itself (§19b; `ui/harbour.py:138-177`). `Harness.md` itself says the consent brief calls the director "to come" and that "until then the fake is the only director". The README says the director's seat refuses a model until its re-ask is a yes. **Nothing in the code enforces either.** `Desk.station` (`remote.py:461-643`) and `consent.decide` (`consent.py:854`) treat the director like any station, and a yes to the current brief (which says the director does not exist) proceeds. I grepped `remote.py`, `consent.py` and `director.py` for any director-specific consent gate and found none. High; sure.
14. *Another station's words reach an instance "under the speaker's name".* The director's `say as <person>` speaks with a model's words under the name of a person nobody holds (`director.py:47-55`). A model hearing it is not told that the words are another model's. Medium; likely (I did not read `say as`'s road through `world/orders.py`).
15. *A paused or silent lookout or master has its work done by the ship's own people; budget and race stand-downs.* Not traced (`world/seats.py` and the master's working are outside my part).

**5b. Other correctness points.**
- `pictures.paint` catches `TypeError` from the painter and retries without `span`, "a painter of a test's own" (`pictures.py:282-286`). A real `TypeError` inside the real painter is swallowed and the call silently drops the span. Low; sure.
- `fake.work_the_slate` uses `assert` for parsing (`fake.py:318`); under `python -O` the next line raises on `None`. Low; sure.
- `judge` lets through whatever its own parse cannot read ("the grammar's own refusal, through `World.submit`", `tools.py:999-1000`), and an authority with no domain passes everything (`tools.py:951-954`). Whether an order outside the domain can reach the ship by words that `imperative.parse` refuses but `World.submit` accepts by another road, I did not establish. The comment at 929-932 records one such hole, already closed (stores orders). A suspicion.
- Determinism: in this part the only wall clock is the ten-minute bound, recorded as an act, and the consent record's date (`consent.py:958`). No unseeded random. Sound.

**5c. The hard boundary** (the simulation must not import the agents). It is not kept. `core/world.py` imports `freesail.agents` five times (1124, 1296, 2505, 2653, 2686), `core/replay.py` nine times, `core/acts.py` twice, all inside functions. `World.tick` runs `agents.watches.tick` (the deck passing between officers, a rule of the ship's routine kept in `agents/`, `core/world.py:2496-2506`) and every harness's `on_tick`. `world/` imports agents from 21 modules, `orders/` from 3 and `api/readings.py` 7 times (grep counts). The agents are woven into the simulation, not attached to it.

## 6. Thin or overgrown

Overgrown. The welfare machinery, the turn's budget, the shelf of books (book numbers, stubs, shelf life, pictures put back with a note), the handover fold with two thresholds and a reserve share, the out-of-turn rules, the reconnect window, the deck's giving, taking, lending and losing, and the seat's identity keys add up to about 13,000 lines (harness, remote, tools' front, agent) around a protocol whose core is `Model.reply(turns) -> Reply` (`model.py:225-228`). Each rule answers a playtest; the comments say which. The rules interlock: a stand-by ending a turn has its own result bookkeeping (`Reply.ran`, `stood_results`, `_keep_ran`), which two door converters must then honour. Against the game it serves (one or two models at a time, played by one owner) it is far more detailed than the ship-side features a player meets.

## 7. What is not tested

- The local runner's written-call parser with extra fields (5a.1): no test.
- The out-of-turn token during the consent conversation's owner turn (5a.2): no test that I could find (grep in `test_consent.py`, `test_agent_api.py`).
- A director seated by a model without a re-ask (5a.13): no test asserts a refusal, because none exists.
- The seat's deck exemptions against the model's (3b): the parity tests seat a captain only (`test_parity.py:355`). No test makes the seated player `go below` or `eat` without the deck.
- "The game is saved" on a station with no `save_fn` (5a.4): untested.
- Dead functions (section 2): untested and unused.

**The fakes, and whether the harness tests test the harness.** The fakes (`Fake`, `narrator`, `officer_of_the_watch`, `captain_of_the_ship`, `master_of_the_reckoning`, `passenger_aboard`, `director_above_the_game`, `captain_on_the_course`) replace only the model. They are `Model`s that return ready-made `Reply` objects to the real `Harness` over a real `World`. So `test_agents.py`, `test_officer.py`, `test_director.py` and `test_captain.py` do test the harness and not the fakes. What they cannot see is the doors' parsing and wording, because a fake's `Reply` never passes through `LocalModel.parse`, `ApiModel.parse` or the MCP bridge's `raw`. The door tests use fakes of the vendors written by the project (`tests/messages_api.py`, a fake chat server), so they check the doors against the project's own idea of the wire format. They cannot check it against the real one. The "rules' seats" (the rules-based captain, `world/captains.py:2308`) are outside this part. The harness reaches it only through `_sync_captain` (`harness.py:1052-1063`: `cap.seated`, `cap.stand_in`).

## Harness.md against the code, ten samples

1. Four doors, and the table (lines 7-16): matches `remote.DOORS` plus the REPL. It leaves out the harbour-launched seats' doors, though §19b describes them. Mostly true.
2. "A turn may make up to eight tool calls" (line 42): false. `ORDERS_PER_TURN = 16` and `READS_PER_TURN = 32` (`agent.py:268-269`), counted apart (`harness.py:2672-2703`).
3. "thirteen tools (the harness's twelve ... and `say`)" (line 76): false. The MCP door offers 16 harness tools plus `say` (`tools.tool_names(True)` in a short Python call gave 16).
4. `say` puts "a line or two into the log under `[watcher]`"; "its lines appear in the browser's log as they are said" (lines 3, 85): false since decision 60. Prose goes to the journal and the director's log, heard by nobody (`harness.py:2626-2670`; `mcp_server.py:223-231`).
5. `--wait` 50 seconds by default, at most four hours (line 87): true (`mcp_server.py:186-192`). The README's "200 seconds by default" (`README.md:55`) is stale.
6. A reconnect within five real minutes is the same conversation (line 89): true (`RECONNECT_S = 300.0`, `remote.py:153`).
7. A reply budget of 4,096 kept free (line 137): true (`REPLY_MAX_TOKENS = 4096`, `local.py:173`).
8. `--watcher fake` (line 46): true (`server.py:1750`, `console.py:1153`).
9. A book goes back after three of the model's turns (line 44, README:59): true (`SHELF_LIFE_TURNS = 3`, `agent.py:2225`).
10. §19: "the director is a kind of thing the consent brief says is to come ... until then the fake is the only director", beside instructions to seat a model there through any door (lines 554-560). The code seats a model with no extra gate (5a.13). Document and code disagree, and the document contradicts itself.

Also stale: `__init__.py:1-24` lists ten modules and says "only the two doors" speak to a vendor. There are 18 files, and three doors take a vendor's library (`mcp_server.py:140-145`, `local.py:135`, `api.py:513`), besides `remote.GameClient`'s httpx. `pictures.py:27-28` says the local runner's models read words; `Harness.tool_names` offers pictures there when the seating says the model reads them (`harness.py:971-976`). `consent.ensure`'s docstring names the local runner, which now goes through the `Desk`.

Five of the ten samples match, four are false and one (the first) is mostly true. The document is accurate on numbers and stale on behaviour.

## The ten findings that matter

1. **Game text and another model's words ride inside the operator message**, against the consent brief's "Nothing from the game ... is ever passed ... as an instruction from the operator". These are the log lines, the night orders (which a model captain may write) and the previous holder's handover note, sent as `system` at the API door and the runner (`harness.py:1089-1185`, `agent.py:2386-2454`, `api.py:609`, `local.py:686`). High; sure.
2. **A model can be seated as the director under a consent brief that says the director does not exist yet**, and no code refuses it, though `Harness.md` §19 and the README say the question must be put first (`remote.py:461-643`, `consent.py:854`, `agent.py:2010`). The harbour even launches such doors by itself. High; sure.
3. **The journal is read by the director model and counted by the harness**, against "nothing in the game acts on what is written there" (`harness.py:1991-2010, 2655-2670, 532`; `mcp_server.py:227`). High for consent honesty; sure.
4. **The local runner's parser hides the token from the scan**: a written call's fields other than `arguments` are discarded before the scan, shown with `LocalModel.parse` (`local.py:887-910`, `model.py:93`). Medium; sure.
5. **The player and a model are not at parity at a lesser station.** `PlayerSeat.submit` re-implements the deck check with three exemptions where `tools.call` has five. A seated player is refused `go below` and `eat` without the deck, which a model is allowed, shown at seed 7 (`seat.py:518-534` against `tools.py:2027-2036`). At the captain's station they meet in `World.submit` behind two different fronts, and only that pair is tested (`test_parity.py`). Medium; sure.
6. **The simulation imports the agents**: 16 imports from `core/` and 21 modules of `world/`, all inside functions. `World.tick` runs `agents.watches.tick` and every harness (`core/world.py:2505-2509`). The stated boundary is not kept. Medium; sure.
7. **Each door re-implements its turn conversion and reply parsing.** Three converters (`local.py:642`, `api.py:579`, `repl.render_turn`), three `raw` builders and three token-scan sites (`harness.py:2531`, `remote.py:1008`, `mcp_server.py:801`), with copied closures already differing in words. Medium; sure.
8. **"The game is saved" may be said when nothing is written**: `_save` without a `save_fn` keeps the save in memory only, the case of a restored or checkpointed station before a door takes it up (`harness.py:4896-4900`, `core/replay.py:439`). Medium; likely.
9. **Size and shape**: a 4,300-line class with about 60 mutable attributes, 190 imports inside functions, 20.9% comments that are mostly history (900 "package N" citations), and one order parsed up to seven times (`tools.py:1088-1146, 919`). Changing it is dangerous. Medium; sure.
10. **`Harness.md` is stale on behaviour.** Four of ten samples are false (the turn's budget, the tool count, `say` into the log, the director's consent), as are the README's `--wait` and `__init__.py`'s module list. There is dead code too: `tools._primer`, `_catalogue`, `_grammar`, `_ship_names`, `director.seat_doors_of` and `repl.open_world` have zero references. Low to medium; sure.

## What I did not read

Not read whole, as the opening says: `harness.py` about 3,300 of 5,571 lines (the samples and folds, the stand-by's machinery 1306-1990 and 4149-4490, the shelf, the handover fold, reseat, the deck and grants 3583-4030, `seating`); `tools.py` about 2,550 lines (the library's pages, the readings, the director's tools); `agent.py` about 2,400 lines (the station briefs and domains); `director.py` beyond its header; `repl.py`, `local.py`, `api.py` and `mcp_server.py` beyond the parts named; `tripwires.py` and `watches.py` beyond their headers; `Harness.md` sections 4 to 18 and 20 to 22; `docs/agents/ConsentAndPreferences.md` (not in my task); the transcripts under `docs/agents/consent/`, which I only listed. Claims in this file about those parts rest on greps and are marked likely or a suspicion where they go beyond what I read.
