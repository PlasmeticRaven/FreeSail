# V1a. Seating, keeping and re-seating a model, and the doors: the code behind the claims

Reader: code. Trees: `FreeSail-gate-m5c` (all line numbers, unless marked **(b)**) and `m5c-b.diff`.

**How this was checked.** I read `freesail/agents/*`, `ui/server.py`, `orders/stations.py`, `core/replay.py`, the five test files named, the diff, and `docs/agents/Harness.md`. Parses and three behaviours were checked with read-only one-liners (`py -B`, `PYTHONDONTWRITEBYTECODE=1`) against the package in memory. Saves and checkpoints were read in memory for evidence. No game or suite was run, no `mcp__freesail__*` tool was called, and nothing was written under `D:\Projects\FreeSail`. Where a finding is derived from the code and was not seen in a playtest, it says so.

Sizes: **S** under about 30 lines in one place; **M** one module plus tests; **L** several modules, or a ruling first.

## Verdicts at a glance

| | Claim | Verdict |
|---|---|---|
| A | A station cannot read its own journal; `show the officers journal` refused | **CONFIRMED** |
| B | The handover note is not in the reseat brief | **CONFIRMED** (missing in 3 of the 7 reseat briefs kept in the checkpoints) |
| C | The drill's stand-by carried into the station | **PARTLY**: the symptom is real, the cause is the *loaded save's* stand-by, not the drill's |
| D | The journal is carried in the model's context | **PARTLY**: only as the model's own past calls. In the two local sessions that were never folded, all the model wrote is 4 to 8% of the conversation and the samples over 80% |
| E | One reseat a game (m5c); m5c-b's rule | **CONFIRMED**; m5c-b is as described, with three gaps |
| F | Claude Desktop must be restarted between sessions, saves, reloads | **CONFIRMED**: the bridge asks for its station once in its life |
| G | Several stations through one door | The game can (two processes); one door cannot; two Desktop entries work mechanically and are unsafe until H is fixed |
| H | Another door's calls landed in a seated model's place | **CONFIRMED** exactly: every call is matched to a seat by the station's name alone |
| I | The relay cut calls at 60 s | **CONFIRMED**; the bridge detects an *announced* cut and names the remedy, but does not adapt, and does not see a silent drop |
| J | Turns and the budget | **PARTLY**: `say` ends the turn at the MCP door only; `answer` never ends a station's turn; the budget is one constant, 8, no flag. **Two faults found**: the budget can refuse `opt_out`, and the silence detector ignores calls made in an open turn |
| K | The handover threshold | **CONFIRMED** (0.6, a constant); higher is safe only on large contexts |
| L | Image tools | Not present; feasible; no drawing exists in Python |

## How a seat works (shared by F, G and H)

- **The game.** `remote.Desk` keeps `seats: dict[str, Seat]` by the station's name (`remote.py:268`). `POST /api/agents/{station}` (`Desk.station`, `remote.py:272-365`) is the only request that carries an identity (`model_name`, `door`) and the only place the consent gate runs (`:348-354`). Every other route (`turns`, `reply`, `owner`, `release`, `library`) finds its seat with `Desk._seat(name)` (`:820-829`): the station's name in the URL and nothing more.
- **The MCP bridge.** One process, one `GameClient(args.game, args.station)` (`mcp_server.py:1113`), one `Bridge` holding `phase` (None, then `consent`, `station` or `stopped`), `briefed`, `seen` (every turn), `_shown`, and the client's `cursor`, `origin`, `revision` (`mcp_server.py:349-385`; `remote.py:947-954`). It asks for the station at first contact, only while `phase is None` (`:438-441`). Nothing sets `phase` back to None.
- **The local runner.** One process, one `game.station(...)` (`local.py:786-796`), then `run()` until the station is released, when it exits (`:842-844`).

---

## A. The returning session could not read its own journal

**Verdict: CONFIRMED**, both halves.

**No tool reads the journal.**
- `tools.journal` appends and returns `"Noted in the journal."` (`tools.py:554-559`). The table has twelve tools (`:596-733`); none reads it.
- `LIBRARY_TOPICS` (`:304-313`) and `_topic` (`:1375-1400`) have no journal.
- `read_log` reads `world.log` only (`:266-281`), and a `journal` note writes no log line.
- `state` is the ship's summary plus each station's state words (`:297-301`).
- The officer's own `submit_order("show the officer's journal")` is refused: `if stations.recognises(text, ship) is not None: return text, f"{who} may not {text}: {_STATION_WHY}."` (`tools.py:439-440`). Seen at the Harpy's tick 51557: `agent.refused ... may not show the officer's journal: a station is addressed by the captain`.

**What a returning model is given.**

| Situation | What it gets | Code |
|---|---|---|
| Same bridge, new or compacted chat (the owner's case) | Nothing. `briefed` stays True, so no brief comes first. The `brief` prompt re-renders the latest brief and every non-model turn since | `mcp_server.py:667-675`, `:490-515` (`_render` skips MODEL turns, `:510-511`) |
| Bridge restarted, seat still held | A fresh brief, and the open sample again if one was open | `remote.py:456-466`; `harness.py:623-638` |
| Released and seated again | A fresh brief, then a sample `seated again` with every reading, no log lines, no notices | `harness.py:1908-1943` |

In none of them is the journal included. The brief's situation item is `The last N lines of the log` and `The readings now` (`agent.py:761-764`).

Evidence for the first row: the Harpy's checkpoint at tick 207121 holds one brief only (turn 0), so nothing was sent again at the return near tick 51000. The model said so in the log (tick 51163): "Coming back I had no brief and none of my old journal."

**Why `show the officers journal` is refused and `show the officer of the watchs journal` is taken.**
- `_JOURNAL` wants `'s` or ` s` before `journal`: `^(?:show (?:me )?)?(?:the )?(?P<who>.+?)(?:'s| s)? journal\s*$` (`stations.py:89-92`).
- `_station_in(who)` takes a name, or a name or alias followed by a space (`:104-114`).
- Checked by running `stations.recognises`: `officers` names no station, so the sentence is not a station sentence. `officer of the watchs` begins with the alias `officer ` and so is taken, by the accident of the prefix rule (`show the officer of the watches journal` is taken too).
- The sentence then falls to the imperative grammar. Its vocabulary *does* know the phrase, because keys drop apostrophes (`vocabulary.py:117-119`; `data/vocabulary.yaml:853-856`). It refuses it as a station sentence that "names one", with examples that name only the watcher (`grammar.py:167-171`). Log, tick 51741.
- `You may show the officer's journal` is refused because `_verb_in` returns nothing for a station verb (`stations.py:366-367`).

**How the owner's order did reach the model.** `show ... journal` is a query, logged as one ROUTINE line whose text is the whole journal (`stations.py:272-280`; `world.py:1010-1011`). It is the captain's line, so it rides the officer's next sample. That was 46 entries on the Harpy and 200 on the Speedwell (tick 398818); by their ends the two long games' journals were about 9,800 and 12,500 tokens, each written into the log whole at every showing.

**Documents against code.** The brief and the tools tell the model the journal is where to keep what it needs: `SHELF_WORDS` "Your journal is where to keep what you took from a page" (`agent.py:619-620`); the shelve results (`harness.py:1342-1343`, `:1347`); the MCP door note (`mcp_server.py:223-226`); the tool's own "shown on request" (`tools.py:699-702`). The model cannot read it back.

**Root cause.** The journal was built as an audit trail for the owner (`journal.py:1-10`) and later recommended to the model as its memory, with no read path.

**Fix.**
1. A `journal` topic in the library: `LIBRARY_TOPICS`, `_topic`, `_contents` in `tools.py`, serving `world.agent_journals[station]`. `library()` already receives the station's name and does not use it. Serve "notes" (the model's notes and handover notes) apart from the whole: on the Harpy 348 entries, of which 16 are notes; the rest are the harness's "Stood by until ...". It is then a book with a handle, shelvable, and readable out of turn (`READ_ONLY_TOOLS`), with no harness change. **M**.
2. The grammar: try `who` and `who` less a final `s` in `_station_in` for the journal verb; name the officer in `grammar.py:169`. **S**.
3. With B: the brief names the journal and carries the last handover note. **S**.

**Risk.** None to replay (reads; no log line). Tests that pin the library's contents and sizes move. One ruling: may a station read another's journal? `_every_topic` (the library-wide `find`, and the browser's shelf as `BROWSER_READER`) has no station.

---

## B. The handover note is not in the reseat brief

**Verdict: CONFIRMED.**

- Every brief, first or later, is built the same way: `tools.read_log(world, self.station.name, since_tick=0)["lines"][-BRIEF_LOG_LINES:]` (`harness.py:592-597`; `BRIEF_LOG_LINES = 20`, `agent.py:94`), then the readings, the tools, the door note, and for the officer the book, the allowances and whose the deck is (`:598-619`). Nothing reads `self.journal`.
- The note is in the log as a notable `agent.handover` line (`harness.py:1794-1802`). It is in the brief only when fewer than twenty lines were logged between the note and the reseat.
- The sample after it carries nothing of the past: reason `seated again`, 0 log lines, no notices (`:1939-1943`).

**Evidence** (the briefs are kept in `Harness.turns`, read from the checkpoints):

| Game | Reseat at tick | It had | Note in the brief |
|---|---|---|---|
| Harpy | 216817 | handed over at 216549 | **no** |
| Harpy | 527389 | handed over at 527255 | yes |
| Harpy | 573851 | "stood down by the MCP bridge: the client disconnected" | **no** |
| Harpy | 602283 | handed over at 602100 | yes |
| Speedwell | 343381 | handed over at 343363 | yes |
| Speedwell | 343551 | "stood down by the captain: the captain has the deck" | **no** |
| Cutter (Gemma) | 14978 | handed over at 14978 | yes |

The two misses after a hand-over were by one line each: the note was the twenty-first line back at the Harpy's 216817 and at the Speedwell's 343551.

**Documents against code.** `OFFICER_BRIEF` promises it: "it is journaled and the relief reads it" (`agent.py:490-493`). Nothing delivers it to the relief.

**Side finding.** The twenty lines have no size cap. Reseat briefs measured 5,200 to 6,500 tokens against 4,000 to 4,400 for a first brief; Gemma's held one log line of 1,893 tokens. A `query.journal` line within the last twenty would add the whole journal to the brief.

**Fix.** `resend_brief` passes the last `agent.handover` entry of `self.journal`, and a line naming the journal, into `Brief.build`'s situation item; each of the twenty lines is cut to a length. **S** (`harness.py`, `agent.py`, the head's tests). No replay effect: the brief is in neither the log nor the save.

---

## C. The drill's stand-by carried into the station

**Verdict: PARTLY.** `hand_over` did come back "Nothing was run" until `say` opened a turn. The stand-by that caused it was the loaded save's, not the drill's.

**The drill cannot carry.**
- It runs in the consent conversation's own harness and World: `self.world = World(seed=0)`, `Harness(self.world, CONSENT_STATION, ..., conversation=True)` (`consent.py:793-803`). Passing it ends and releases that harness (`:1013-1016`, `:1066-1067`).
- A station is a new `Harness` with a new `AgentState` (`state = STATIONED`, `stand_by = None`; `harness.py:449`; `agent.py:821`, `:825`), and `start()` opens its first sample (`harness.py:575-577`). A reseat sets STATIONED and samples (`:1913`, `:1943`).
- The drill's journal line and its stand-by are in the consent record, not the game.

**What happened** (m5c-b, `Harpy-Back-At-Falmouth.json`):
1. The save's record of the officer reads `standing by until two bells; with the deck since First dog watch (17:13)`.
2. m5c-b's changed **Leaving** section put the question again; the drill followed, with `stand_by(until="eight bells")` (`FreeSail-gate-m5c-b/docs/agents/consent/2026-10-03-opus-5.5.md:178`).
3. The station existed and was not released, so `_take_station` called `existing.take_over(...)` (`remote.py:427-432`).
4. `take_over` sends the brief again, and a sample only if one was open (`harness.py:633-638`). It leaves `agent.state` and `agent.stand_by` as saved. The station was still standing by until two bells, with no turn open.
5. Nothing told the model. The bridge's `_outcome` renders the brief alone (`mcp_server.py:751-752`), without even the "Your turn has not come yet" line `brief_text` has (`:499-503`).
6. `hand_over` was therefore out of turn: `ran = " Nothing was run." if reply.calls else ""` (`remote.py:618-620`), after "You are standing by until ..." (`:664-669`).
7. `say` is the model's own word: it ends the stand-by and opens a turn (`remote.py:601-609`; `harness.py:2032-2070`).

The save shows steps 6 and 7: transcript entry 568 is `{"door": "speak", "reason": "Mr Pearce on deck. ... handing over the deck for the reseat test."}` at tick 527255, entry 569 the `hand_over`, and the journal has "Ended the stand-by until two bells at my own word."

**m5c.** The same path is reached by a save loaded by replay. It is not reached from a checkpoint, which m5c refuses outright (see F).

**Test gap.** `test_agent_api.py:571-600` covers a take-over with the turn open, never one standing by or paused.

**Fix.**
- Cheapest: say it. Put the station's state words in a take-over brief ("You are standing by until two bells, from before the game was saved; say(text) ends it"). **S**, no replay effect.
- Better: `take_over` ends a carried stand-by and opens a sample, recorded as a door act so a replay does the same. **M**, with a replay test. Note that `door_act`'s final `else` treats any act it does not know as a stand-down (`harness.py:1642-1643`).

---

## D. What is carried in the model's context

**Verdict: PARTLY.** The journal is never sent back in a sample. It is in a local model's context only as that model's own earlier `journal(...)` calls, and by measurement those are a small part of it.

**What a sample holds.** `tick, stamp, reason, notices, question, word, stood_by, log, log_omitted, readings` (`model.py:104-137`; `harness.py:935-993`). Every reading in the first sample; after that the changed ones, the sails in one line. No journal. The deck's giving carries the whole book as a notice (`harness.py:1703-1707`).

**At each door.**

| Door | What the model is sent | What is dropped |
|---|---|---|
| MCP | Each turn as text (`repl.render_turn`, `repl.py:127-190`) as a tool's result; one tool call is one reply | Nothing by the game: the client keeps the chat (`harness.py:374-376`) |
| Local runner | Brief as `system`; each sample as a `user` message holding its JSON; results as `tool` messages (the result text only); the model's replies as `assistant` messages with their `tool_calls` in full, so every journal and handover note it wrote (`local.py:408-490`). Reasoning is not sent back | `_budget` leaves out the oldest whole exchanges past `ctx - max_reply - tool definitions` (`local.py:492-542`); shelved books go as one line |
| REPL | As MCP, printed once | Nothing |

**The two folds.**
- `_fold` (`harness.py:1015-1051`): a sampling point reached while a turn is open adds a data turn with the new lines and the changed readings, marked `folded`.
- `_fold_handover` (`:1828-1863`): keeps the brief, one data turn (`tick, stamp, reason, handover, folded, readings`, with every reading) and the last 6 turns. Everything else since the brief goes, earlier journal notes and the earlier handover note included.

**The journal in the log today.** `journal(note)` writes no log line at all. The harness's own entries have lines of their own. A handover note is said in full, notable.

**Measured** (checkpoints, the harness's four-characters rule; what the runner would send):

| Session | Total | system | user (samples) | assistant (all the model wrote) | tool |
|---|---|---|---|---|---|
| Qwen, Ollama, tick 34091, never folded | 66,400 | 4,100 | 54,400 | 5,600 | 2,400 |
| Gemma, Ollama, tick 54107, never folded | 72,400 | 6,600 | 59,800 | 3,000 | 3,100 |
| Qwen, llama.cpp, tick 112613, folded twice | 19,400 | 4,000 | 12,000 | 2,700 | 600 |

- Inside the samples: Qwen/Ollama readings 21,500, log 16,500, stand-by digests 2,300. Gemma log 24,800, readings 13,900, stand-by digests 9,400.
- The stand-by digest lists notable lines that are also in `log`.
- Session 7's 22 journal notes are 4,800 tokens in all; its whole journal 7,600.

So in the two sessions that were never folded, the samples are over four fifths of the conversation, and everything the model wrote, journal included, is 4 to 8%. In the folded session the total is small, and the samples are still three fifths of it against 14% for the model's own words. Taking the journal out saves a few thousand tokens between folds. The readings' changes, the log lines and the repeated digest are where the room is.

**Size of what was asked.**

| Piece | Touches | Size | Risk |
|---|---|---|---|
| Read the journal like the library | A, item 1 | M | none to replay |
| A pointer line in each sample | `Sample` gains a field; `_build_sample`; `render_turn` | S | samples are in neither log nor save; tests that pin sample keys |
| Take a written note out of the conversation (local door) | Replace the call's `note` in the MODEL turn by a line after the turn ends and bump `revision`, as the shelf does (`harness.py:1261-1280`); the transcript keeps the original (`:1084-1086`) | M | not possible at MCP, as with `shelve` |
| "x made an entry in his journal" in the log | `tools.journal` | S | a new log line from a recorded call: every old save with journal calls replays to another digest; the scripted officer journals (`fake.py:218-222`) |

A read path (A) has to come before any removal: after a fold, a budget drop or a chat compaction the note is otherwise gone for the model.

There is no OpenRouter door in the code (`docs/dev/M5-WorkPackages.md:705` wants one). The local runner sends no credential by design (`local.py:72-76`).

---

## E. Re-seating

**Verdict: CONFIRMED** for m5c; m5c-b does what `CHANGES-m5c-b.md` says.

**m5c.**
- `MAX_SEATINGS = 2` (`agent.py:546`), enforced in `Harness.reseat` (`harness.py:1890-1894`: "which is all a game allows; start a new game to station it again") and in `Desk.station` (`remote.py:305-322`, 409).
- It counts every release, whatever the reason: the token, `opt_out`, `stand down the officer`, the door closing (`remote.py:732-733`), the ten minutes.
- **The deck's return is a release by design**: `take_deck` sets `_stand_down_requested = ("the captain has the deck", by)` (`harness.py:1731`), and `hand_over` calls `self.stand_down("the deck handed over", ...)` (`:1777`). The captain cannot take the deck for an hour and give it back to the model still seated.
- Seen: the cutter at tick 14978 and the Harpy at 216817, "the second seating, the last this game allows".

**Documents against code.** The documents justify the limit by the accident alone ("an instance that left by accident may be seated again, once": `agent.py:542-546`, `:628-633`; `Harness.md:258`). The code applied it to every amicable return.

**m5c-b** (from the diff).

| How it left | `left_by` | Seated again? |
|---|---|---|
| Stood down: the captain, `hand_over`, the door closing, the ten minutes | `STOOD_DOWN` | Yes, at once, any number of times, same identity |
| The token or `opt_out` | `OPTED_OUT` | Yes, after the consent question is put again (`ask_again or opted_out`); a passed drill is carried (`drill_carried`) and the new record's notes say so |
| `opt_out(final=true)` | `OPTED_OUT`, `no_return` | No: 409 "it left asking not to be seated again in this game" |

- **Recorded:** `final` in the reply's arguments (in turn), or `"final": true` on the `leave` door act (out of turn), only when set, so older saves read the same. `left_by` and `no_return` are not in `Harness.save()`; a replay rebuilds them and a checkpoint holds them.
- **What a returning session is told:** the brief again, with the rewritten opt-out sentence; a sample `seated again`; "The deck is the captain's now". The log says "takes the station again (Opus 5.5, through mcp): the third seating; it had stood down by ...". The journal says the same.
- **Also in the diff:** a station loaded from a checkpoint gets `Playback(world, [])` and can be taken over (see F); `opt_out` gains a boolean `final`.

**Gaps left in m5c-b.**
1. The deck's return still releases the station, and the bridge still cannot ask again (F), so every return is still a restart of the door and a fresh "you have the deck".
2. A station that opted out in an m5c game, loaded in m5c-b from its checkpoint, has `left_by == ""` (the class default) and is seated without the re-ask. A replayed load is right. (Derived from the code; not seen.)
3. `allowances` are never cleared: only `allow` and `disallow` touch them (`harness.py:1744`, `:1755`). "The captain's word for this watch" outlives the watch and every seating. `AgentState.told` is never written.

Small: the reseat line says "through mcp" or "through runner", the door's key and not its words (`door_act("reseat", identity, door or "the game")`), in both trees.

**The fix underneath.** Do not release the station when the deck goes back; release only on `stand down`, an opt-out or the door going. That is two functions in `harness.py`, and **L** in fact: old saves replay `I have the deck` as a stand-down and their recorded `reseat` acts would then meet a station that is not released, so it needs a per-save switch like `stand_by_ends_turn`. It also changes a sentence of the consent brief in a section that re-asks every model.

---

## F. Claude Desktop must be restarted between sessions, saves and reloads

**Verdict: CONFIRMED.**

**What the bridge holds.** No session id and no seat key. `phase`, `briefed`, `seen`, `_shown`, `stopped_words`, the calls in flight and the results never delivered (`mcp_server.py:349-385`), and the client's `cursor`, `origin`, `revision` (`remote.py:947-954`). The brief is the result of the first tool call (`:667-675`) and is flagged by `briefed`.

**What the same chat's next call gets.**

| After | The result, every time | Why |
|---|---|---|
| The game server restarted (a new game, or `--load`; the browser server has no load in process, `server.py:904`) | "The game did not take the call: No agent is stationed at the officer of the watch's station through the agent API; station one first" | `contact()` returns None, the phase being `station` (`:440-441`); the new Desk has no seat (`remote.py:820-829`); `_call` reports it (`:631-633`). **If another door has seated that station, the call is accepted instead: H** |
| The station stood down, handed over, or the deck taken | "The station is released: stood down by ...; nothing more is asked of you here." | `remote.py:586-587`, `:676-683`; `mcp_server.py:691-696` |
| Consent refused, or a 409 at first contact | "No station is offered in this session: ..." | `mcp_server.py:461-465` |
| The chat crashed or was compacted; bridge alive, station held | Calls run; no brief, no journal | A |

**Can it ask again without the client restarting it?** No. The only retry is a game that could not be reached at first contact (`:466-467`).

**Three things make it worse.**
- Quitting Desktop cleanly runs `bridge.close()`, which posts the release: the officer is stood down and the game saved (`mcp_server.py:885-893`, `:1126-1132`). Seen on the Harpy at tick 573848 ("stood down by the MCP bridge: the client disconnected"), then the fourth seating three ticks later. In m5c that spends the one reseat. A killed process leaves the seat held, and a new bridge attaches.
- **m5c only:** a save made with the station held, loaded from its checkpoint, refuses every door: `_rebind` gives the station `Transcript([])` (`replay.py:294-299`) and the desk takes anything not a `Playback` for the game's own script, 409 "manned already in this game (... --watcher fake)" (`remote.py:323-329`). Fixed in m5c-b.
- `--station` and `--model-name` are process arguments, so a change of either is an edit and a restart (`Harness.md:70`).

**The local runner** has the same shape: `run()` returns on a release (`local.py:842-844`) or when the game cannot be reached (`:888-890`), and the process ends.

**The smallest change.**
1. Bridge: a `_reset()` (phase None, `briefed` False, `seen` empty, the client's cursor, origin and revision to 0), called when a call gets 404 from the game. The next call then asks for the station through the ordinary gate and gets the brief first. About 30 lines in `mcp_server.py`. **S**, **M** with tests.
2. After a release: the same reset, on an explicit act and not on any next call. A model in a `stand_by` loop would otherwise seat itself again a moment after `stand down the officer`. A bridge tool or prompt (`return to station`), or the captain's word. **S**, and a ruling.
3. Runner: a `--stay` that keeps the model server and asks again after a release or a lost game. **S** to **M** in `local.py`.

**Risk.** A reseat and a take-over are already recorded and replayed; the reset is the door's alone. With H's lease, the reset must drop the old key.

---

## G. Several stations through one door

**Verdict.** The game seats several stations at once. One door process serves one station. Two entries in Claude Desktop's configuration would work mechanically and are unsafe until H is fixed.

- `--station` is a process argument (`mcp_server.py:1093-1098`; `local.py:754-759`); every path of that client carries the one name.
- One `Seat` per station name (`remote.py:268`, `:363`); one harness per station in a World (`harness.py:433-443`, `:516`).
- Seen: the Harpy's save at tick 216549 has the officer (Opus 5.5, MCP) and the watcher (qwen3.8:27b, the runner) seated together.
- Nothing compares identities across stations: one `--model-name` may hold both.

**What two Desktop entries would run into.**

| Point | Why |
|---|---|
| Which chat is which | Desktop starts one process an entry and every chat shares it (`Harness.md:92`). Both servers' tools are offered to every chat. The bridge cannot tell chats apart, nor which model answers (`Harness.md:70`) |
| Same names | Both announce the server name `freesail` (`mcp_server.py:1020`), the same tools, prompts and resource addresses. Only the configuration key differs |
| Identity and consent | Both belong to the entry's `--model-name`. A chat on another model that uses the entry acts under its record |
| Seated by accident | The first tool call on each server returns that station's brief; a chat that touches both is seated at both |
| Stations wake each other | Each is sampled on notable lines by anyone else (`harness.py:763-766`): the officer's answers and his handover note, in full, open the watcher's turn, and the reverse |
| Quitting | Stands both down |
| Claude Code | Two sessions on one folder start two bridges with one name and one station; the second attaches to the first's seat without a word in the log (`remote.py:297-304`, `:456-466`) |

**To make it workable.** The station in the MCP server's name and in the first line of every result (**S**); H's lease (**M**); one entry a role.

---

## H. Another door's calls landed in a seated model's place

**Verdict: CONFIRMED**, exactly as the owner describes.

**What is checked on each call: the station's name, and nothing else.** `api_turns`, `api_reply`, `api_owner`, `api_release` and `api_library` (`server.py:547-567`) go to `Desk.turns`, `reply`, `owner`, `release`, each of which does `seat = self._seat(name)` (`remote.py:496`, `:519`, `:693`, `:723`, `:820-829`). `model_name` is compared in `Desk.station` alone (`:297-303`). There is no token, session id or door id.

**Why the bridge's calls were taken.** This is the one path in the code by which a bridge's calls reach a seat it did not ask for, and it fits the owner's account and the transcript:
1. The Desktop bridge had `phase == "station"` from an earlier game and was never restarted.
2. `contact()` therefore returned None (`mcp_server.py:440-441`) and it never asked for the station. Had it asked, the answer was 409 "manned by Qwen..., through the local runner".
3. Its poll and its reply went to `/api/agents/officer/...`, which is the seat of that name: Qwen's.
4. Its old cursor was clamped to the stream (`remote.py:498`). The moved `revision` made it read the seat's whole stream again (`remote.py:988-997`; `mcp_server.py:480-483`), so it then held the other model's conversation.

**What the record says** (`saves/freesail-seed7-tick112613.json`).

| Where | What it says |
|---|---|
| The station's record | `model_name: Qwen3.8-27B-0814-Q4_K_M.gguf`, `door: runner`, `seatings: 1` |
| Transcript 0 to 148 | The runner's shape: the text, then `[{"name": ..., "arguments": "{...}"}]` (`local.py:590-592`) |
| Transcript 149 to 157, ticks 112483 to 112613 | The bridge's shape, `{"arguments": {...}, "tool": "submit_order"}` (`mcp_server.py:610`): belay standing order "trim by the wind"; heave to; a `say`; stand by; come to an anchor (refused by the domain); a `say`; stand by; the door act `speak` "Handing over now, sir."; `hand_over` |
| Between them | No door act, no log line, no journal entry. The shape of `raw` is the only trace |
| The log | Qwen silent after 97556; nudged 101104; paused 104704; "Resume the officer" 112463; then "By the officer of the watch: belaying standing order trim by the wind", "heaving to", the handover note and the stand-down, all under the officer's name |
| The journal | The handover note of 112613 stands as the seated officer's |
| Consent | The gate ran for Qwen alone (its door note names `2026-10-04-qwen3.8-27b-0814-q4_k_m.gguf.md`) |

Two precise points:
- "Heave to" passed because the captain had allowed it to Qwen's watch, and allowances are never cleared.
- Opus 5.5 does have a yes with a drill on record in this tree (`2026-10-02-opus-5.5.md`). What is missing is that it was never gated, briefed or seated in *this* game; the brief it acted under was another ship's.

**Derived from the code, not seen.**
1. `release` is open the same way. Quitting Desktop with a stale bridge posts `/api/agents/officer/release` and stands down whoever holds that station. The log would say "stood down by the local runner: the client disconnected", since `by` is the seat's door (`remote.py:733`).
2. A seat in its consent conversation takes replies the same way (`_consent_reply`, `remote.py:531-557`). A stale bridge's call would be written into another identity's consent record as its turn, and an `answer` would be its verdict.
3. Two live doors on one seat interleave. The runner appends the other door's reply to its turns and sends it to its model as that model's own (`local.py:822-836`). On the cutter the runner had already gone quiet, so this did not occur.

The tests post to these routes bare (`test_officer.py:901-908`).

**Fix.**
1. **A lease.** `Desk.station` mints `Seat.key` for a new seat, a reseat and a take-over, and returns it once. `GameClient` keeps it and sends it with every request. `_seat(name, key)` refuses a missing or wrong key with 409 in words: who holds the station, through which door, and "nothing was run". The bridge resets on that refusal (F).
2. **A second door for the same model** (the attach): mint a new key, so the newest door holds the seat and the older is refused at its next call. Write it in the log as a recorded door act, so a replay writes it too.
3. **The record.** The first `agent.stationed` line names neither the model nor the door; only a reseat's does.

**Size and risk.** **M**: `remote.py`, `server.py`'s routes, `GameClient` (both doors follow), `mcp_server.py`, and the tests that post bare, in four files. The key never enters a save or a transcript, so replay is untouched. A new log line appears only where a door changes. An event's `data` is inside the log's digest (`events.py:108-120`), so adding fields to an existing line moves every recorded digest with an agent in it; a new line of its own does not.

---

## I. The relay cut calls at 60 seconds

**Verdict: CONFIRMED** that the default is wrong for that client. **PARTLY** on "the bridge should detect the cut": it detects an announced cut and says what to do; it does not shorten its own wait, and it cannot see a silent drop.

- `MCP_WAIT_S = 200.0` (`mcp_server.py:163`), set under Claude Desktop's four-minute cut (`:152-162`). `--wait` overrides it up to 14,400 (`:1099-1108`, `:169`); its help text already says "50 for a client that cuts calls at a minute".
- A progress note goes every 15 s (`:174`), on the reasoning that clients reset their timeout on progress. Neither Desktop nor the relay does.

**What a cut does and does not do.**

| Question | Answer | Code |
|---|---|---|
| Is the stand-by lost? | No. The reply is delivered first and the game logs `agent.stood_by`; the wait is only the bridge polling for the next turn | `_hand_back` `:789`; `_wait` `:857-881` |
| Is the station stood down? | No. "the client disconnected" comes only from `close()`, when the stdio loop ends | `:885-893`, `:1126-1132` |
| A cut the client announces (`notifications/cancelled`) | The wait stops within 2 s. A result that brought a turn is returned first by the next call, which is not run. An empty one is noted after the next result, in words that name the remedy: "the owner may start the bridge with a shorter --wait, 50 for a client that cuts at a minute" | `cut_off` `:401-410`; `:876`; `_lost_first` `:896-909`; `_lost_note` `:912-920` |
| A silent drop | Not detected (the module's own words, `:70-72`). The held call keeps the lock up to `--wait`; the next call that is not a read waits behind it (`:554-562`); a turn returned to the dead call counts as shown (`:634`), so the model can answer a turn it never read | |

**The relay can be told apart.** The consent record of the cloud session names its client `local-agent-mode-freesail 1.0.0` (`FreeSail-gate-m5c-b/docs/agents/consent/2026-10-03-opus-5.5.md:6`), against `claude-ai 0.1.0` for Desktop. The bridge has the name at first contact (`mcp_server.py:928-935`, `:450`), before it states the wait in the door note (`:455`).

**The cost of the remedy.** At `--wait 50` a glass at 1x is about 36 chained `stand_by` calls. Those are the long runs of tool calls with nothing in the chat that preceded the crash in the owner's note 10. An MCP server cannot wake a model, so a long wait is a chain of calls at this door whatever the number.

**Fix.**
- A default by the client's name when `--wait` is not given. **S**.
- Adapt: in `cut_off`, shorten `self.wait` to a little under the cut just seen, and say so. **S**.
- Silent drops: a new call that is not a read, arriving while a wait holds the lock, marks that wait cut. **S** to **M**.

`test_mcp_server.py:990-1004` pins 200 as the default.

---

## J. Turns and the turn budget

**Verdict: PARTLY.** The budget is as the notes say, and it is the blocker they describe. Of the two tools named, only `say` ends a turn, and only at the MCP door.

**What a turn is.** An open sample, from `_sample` to `_end_sample`. It ends on:
- a reply with no tool call (`harness.py:1170`);
- a `stand_by` that takes, the calls after it in the same reply not run (`:1120-1132`);
- a release, or a pause for silence (`:705-707`);
- in the consent conversation only, an `answer` (`:1161-1168`).

**At each door.**

| Door | Ends the turn | Does not |
|---|---|---|
| MCP | `say`: it is sent as `Reply(text=text)` with no call (`mcp_server.py:774-776`), which is the harness's end of turn, and the call then waits for the next one. `stand_by` | `answer`, and every other tool. After a `say`, an acting call is out of turn: "It is not your turn ... Nothing was run" until another `say` opens one (`remote.py:601-620`) |
| Local runner, REPL | A reply with no tool call; `stand_by` (`TURN_ENDS_WORDS`, `agent.py:559`) | `answer`: the model is asked again, and must reply once more with no call |

`stand_by_ends_turn: true` in a save is the replay switch for saves from before package 28c (`harness.py:473-475`, `:2316`). It is not a setting.

**The budget.**

| Constant | Value | Where | Flag |
|---|---|---|---|
| `TOOL_CALLS_PER_SAMPLE` | 8, every station, every door | `harness.py:212` | none |
| `BUDGET_FREE_TOOLS` | `answer`, `say` | `:218` | none |
| Reply length | 4,096 tokens | `local.py:118` | `--max-reply` |
| Request timeout | 600 s; 3 failures stand the station down | `local.py:137`, `:142` | `--request-timeout` |
| Patience | watcher a watch, officer an hour, of ship's time | `agent.py:455-462`, `:502` | none |
| Stand-by with the deck | an interval of a glass at most | `harness.py:259` | none |
| Shelf-life; a book | 3 turns; 600 tokens | `agent.py:593`, `:599` | none |
| A sample's routine lines; `read_log`; `find` | 40; 200; 8 | `harness.py:288`; `tools.py:101`, `:111` | none |

- The count is reset only when a sample opens (`harness.py:1007`), not at a fold. A turn kept open through several sampling points has eight in all.
- Everything but `answer` and `say` counts alike (`:1098`): reads, `journal`, `shelve`, orders, `hand_over`, `handover_note`, `stand_by`, `opt_out`.
- Out of turn nothing is counted: reads, the journal and a shelve made while the game has the floor are free (`:1365-1382`).
- No flag reaches it: the server's parser has none (`server.py:897-934`) and the Desk builds the station itself (`remote.py:434-443`). The brief states it (`harness.py:640-645`).

**At the budget.** The result is "Not run: this sample's budget of 8 tool calls is spent; call it again in your next sample. answer and say are not counted and always run." (`:1101-1108`). The call is skipped and the model asked again. It can then only answer or end the turn, and its next sample is the next sampling point, up to a glass away.

Seen on the cutter:
- Qwen, ticks 8838 and 8855: the orders to get under way put off a sample, the eight having gone on library reads.
- Qwen, ticks 8910 and 93189: it wrote "Standing by for the anchor aweigh" as words; the `stand_by` itself had not run.
- Gemma, tick 8413 and twice more: it wrote its orders as a table of text, with a `say` that door has not got.

**Faults found** (each reproduced in memory with the scripted model).
1. **`opt_out` as a ninth call is "Not run", and the station is not released.** The brief promises the tool beside the token. The token itself is scanned first and still works.
2. `stand_by` as a ninth call is "Not run": the turn stays open and the model believes it stood by. `hand_over` the same.
3. **The silence detector does not hear calls made in an open turn.** `last_heard_tick` moves only when a turn ends (`:1205-1206`). `_while_open` nudges after the station's patience of an open turn and pauses after as much again, taking the floor (`:701-709`). A model that called a tool at ticks 500, 1000 and 1500 of one open turn was nudged at 1800 for "no reply". For the officer that is an hour of ship's time, a minute at 60x.

**What "say and answer do not end the turn; stand_by does; a larger, configurable budget per station" would touch.**

| Piece | Touches | Size | Risk |
|---|---|---|---|
| A budget per station, with a flag | A field on `Station` (saved and loaded with it, `agent.py:373-435`); `_take_reply`; the brief's sentence; a flag on the server and the Desk. Free `opt_out`, `stand_by` and `hand_over` at least; consider the reads; top it up at each fold | M | The budget decides which recorded calls run, so a replay must use the budget the save was made under. Saves without the field read as 8 |
| `say` no longer ends the turn (MCP) | Keep the harness's rule, so old transcripts replay. Either the bridge sends `say` as a logged call that returns at once and only `stand_by` waits; or an acting call opens a turn by itself when the game has the floor, as a recorded door act like `speak`. The second removes "Nothing was run" without changing what a turn is | M | `mcp_server._hand_back`, `remote._station_reply`, `Harness.door_act`, the door note, `SAY_DESCRIPTION`, the tests |
| `answer` | Nothing: it does not end a station's turn | none | |

**What in the welfare logic assumes the present rule.**
- The silence detector (fault 3), which today would stop the very thing asked for.
- `--lockstep`: the clock waits while the floor is the model's (`server.py:451-452`), so a turn held open stops the game.
- Everything kept at a turn's end: the shelf-life, counted in turns (`harness.py:1224`, `:1282-1292`); the handover ask and its fold (`:1225-1229`); the count of empty replies (`:1202`); the end of a repeat or a contrary-orders matter (`:1214-1223`); where the next stand-by's digest begins (`:1203-1204`). Turns that seldom end starve all of them.

---

## K. The handover threshold

**Verdict: CONFIRMED.** The threshold is a constant with no flag. It can be higher on a large context and is already at its limit on a small one.

- `HANDOVER_AT_FRACTION = 0.6`, `HANDOVER_ASK_AGAIN_FRACTION = 0.1`, `HANDOVER_KEEP_TURNS = 6` (`harness.py:268-273`). `test_officer.py:784` pins 0.6.

**How the context is measured.**
- The runner learns it from the server (`local.py:378-390`: llama-server's `/props`, or Ollama's `/api/ps` and `/api/show`, with `--ctx` as a cap) and says it when it stations (`:795`). The Desk puts it on the harness as `budget_tokens` (`remote.py:336-344`, `:447-448`), and it is saved (`harness.py:2230`).
- MCP sends none, so Claude is never asked.
- The two Ollama sessions' saves have `budget_tokens: null`. They were never asked, and the runner drops nothing without a context (`local.py:497-498`): the server cut the conversation unseen. That is why llama.cpp "was necessary".
- The size is `_conversation_size`: the JSON of each turn from the latest brief on, four characters a token (`harness.py:1804-1809`). It includes the brief, though the notice says "since the brief". It leaves out the tool definitions and the reply reserve. It counts each call's arguments three times (the call, `raw`, the result's `args`). On session 7 it came to 21,600 against 19,400 for what the runner would send.

**The asking.** At the end of a turn (`:1229`), as a notice in the next sample (`:1826`); again when the size has grown another tenth; never forced.

**If the note is not written in time.** Nothing, until the runner leaves out the oldest whole exchanges once the messages pass `ctx - 4096 - tool definitions` (`local.py:501`). The model is not told what went. The brief is never left out; if the brief and the latest sample do not fit, the run stops (`:526-530`).

**What the fold keeps:** see D. The previous handover note goes too unless the model carried it forward.

**The risk of a higher threshold, in numbers.** Measured: the brief 4,000 to 4,400 tokens (a reseat's up to 6,500); the tool definitions 2,222; the reply reserve 4,096. A sample's median is 330 to 570 and its largest 2,300 to 4,800; every reading at once is 1,144; a note is 530 to 590, about 1,100 as a turn. The room between the ask and the first exchange dropped is `ctx x (1 - f) - 6,318`, taking the harness's measure and the runner's as equal (they were within about a tenth of each other on session 7):

| Context | 0.6 | 0.75 | 0.8 | 0.9 |
|---|---|---|---|---|
| 16,384 | 240 | none | none | none |
| 32,768 | 6,800 | 1,900 | 240 | none |
| 65,536 | 19,900 | 10,100 | 6,800 | 240 |
| 102,400 (session 7) | 34,600 | 19,300 | 14,200 | 3,900 |

That room has to hold the sample that carries the ask, anything the model reads first, and the note itself. About 8,000 is comfortable and 4,000 the least. So 0.8 is sound at 100,000, 0.75 at 65,000, and 0.6 is already the most a 32,000 context bears. A fixed fraction is the wrong shape; a reserve in tokens is the same rule at every size.

The risk itself is quiet: past the limit the note is written after the oldest exchanges have gone, so it sums up less than the watch. On a small context the ask never comes first.

**A related fault.** The guard before stationing measures the *consent* brief (`local.py:343`), "the longer of the two briefs" when it was written. The officer's brief is now twice that, so the guard passes a 16,000 context the officer's station cannot use.

**Fix.** A flag on the runner, sent with the station request, kept on the `Seat` and the harness and saved beside `budget_tokens`; better as a reserve in tokens than a fraction. **S** to **M**. No log effect: the ask is a notice and the fold changes the turns only.

---

## L. Image tools for image-capable doors

**Verdict: not present; feasible.** There is no drawing in Python anywhere.

**How a result is carried today: as text.**

| Door | Today | Could it carry an image? |
|---|---|---|
| The tools and the agent API | A string or a small dictionary (`tools.py:1-5`), as JSON | Yes, as a handle, with the bytes served aside |
| MCP bridge | Tool functions return `str`, `structured_output=False` (`mcp_server.py:968-997`); a dictionary as JSON text (`:327-330`) | Yes. The installed SDK (mcp 2.2.0) exports `Image`, and its result conversion turns an `Image` or a list into image blocks. The wrapper would return the text and the image. The lost-result store is text (`:385`): ask again, do not store |
| Local runner | `tool` messages with string content (`local.py:463-478`) | For a multimodal model: servers of this kind take an image as a part of a `user` message, not of a tool message, so the result is text with a user message after it. `_budget` prices a message by its JSON length (`:499`); a picture in base64 would count as tens of thousands of tokens, so image parts need a price of their own |
| REPL | Text | A file's path |

**The shelf.** `library` returns a `Page` with a title and the call that reads it again (`tools.py:316-349`). The harness makes it a `Book` with a handle (`harness.py:1241-1250`). `shelve` replaces the result in the conversation by one line (`:1261-1280`, `:1308-1349`), and a book left open goes back after three turns. What is a book is `BOOK_TOOLS` and `book_of` (`tools.py:115`, `:822-841`). An image tool is shelvable by naming it there: **S**. Keep the bytes out of `Harness.turns`, which is written into every checkpoint (`replay.py:170-174`): the turn holds the handle.

**Where the views are drawn today: the browser.**
- `client/projection.js`, 1,170 lines: the ship as a skeleton and its projection. Pure functions, exported for Node; `project(skeleton, facing, heel)` takes any bearing.
- `client/shipview.js`, 89 lines: the scene as SVG, through the page.
- `client/map.js`, 733 lines: the chart on a canvas, from `/api/chart` and the snapshot.
- The page already takes `?facing=DEG` (`client/app.js:5`, `:274-276`).
- In Python: no SVG, PNG, Pillow or matplotlib in `freesail/` or `tools/`; no imaging dependency in `pyproject.toml`.

**The account, never the truth.** The snapshot carries the reckoning only: "The truth's position is not in the snapshot" (`api/queries.py:211-216`). `chart_block` has the coast and the features and never the depth tiles (`:105-133`). A renderer fed only `queries.snapshot` and `queries.chart_block` is the captain's chart by construction. Make that its signature and test it.

**Three ways to make the picture.**

| Way | Likeness to the player's view | Needs | Size |
|---|---|---|---|
| The owner's open browser captures it: the server asks over the socket, the page draws the asked view off screen and posts a PNG back, the tool waits with a time limit | Exact: the same code | An open tab, which a session with a captain has. No dependency | M: about 100 lines in the client, a route and a wait in the server |
| A headless browser on the game's own page (`/?facing=135`) | Exact | A browser to download, as an optional extra; a second or two a picture. Works with nobody at the game | Code S to M; installing it L |
| A renderer in Python from the snapshot | Only as good as the port | A port of about 1,250 lines of the ship's drawing and 430 of the chart's, and a rasteriser (models take PNG, not SVG). Two renderers to keep alike from then on | L; the chart alone M to L |

The plumbing common to all (the two tools, the handle and its bytes, the MCP image block, the runner's image part) is **M**. The first way is the least cost for the play the note describes.

**Determinism.** A tool's result is not recorded and a replayed call has no browser. The tools must write nothing in the log or the journal, and return words when no picture is to be had.

---

## Across the claims

**Where the documents and the code disagree.**

| Document says | Code does |
|---|---|
| The journal is where the model keeps what it needs (`agent.py:619-620`; `harness.py:1342`; `mcp_server.py:223-226`) | The model cannot read it (A) |
| "it is journaled and the relief reads it" (`agent.py:490-493`) | The relief gets it only within the last twenty log lines (B) |
| An instance "that left by accident" may be seated again once (`Harness.md:258`) | m5c counted every release, the deck's return included (E) |
| "You may also call the opt_out tool" (`agent.py:728`) | Refused as a ninth call (J) |
| The handover is asked for "since the brief" (`harness.py:312-318`) | The measure includes the brief (K) |
| The consent brief is "the longer of the two briefs" (`local.py:45-52`) | The officer's is twice it (K) |
| `--wait` "50 for a client that cuts at a minute" is the owner's to set | The bridge knows the client's name and could set it (I) |

**What belongs together.**
1. **The seat lease, the bridge's reset and the runner's `--stay`** (H, F, G): one package in `remote.py`, `mcp_server.py`, `local.py`. It makes the record honest, ends the restarts, and is the condition for two stations in one app.
2. **The journal read path, the note and the pointer in the brief, the grammar** (A, B, D): one package in `tools.py`, `harness.py`, `stations.py`. Removing notes from the context comes after it, and by the measurements is worth little.
3. **The budget per station with `opt_out` freed, and the silence detector hearing calls** (J): one package in `harness.py` and `agent.py`. The two faults are worth fixing whatever is ruled on turns.
4. **The deck's return without a release** (E): a ruling first; it is what makes every return a reseat.
