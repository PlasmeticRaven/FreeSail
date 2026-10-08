# R1. Review of the m5c-b change set (packages 37b and 37c)

Reviewer's scope: `CHANGES-m5c-b.md`, the whole of `m5c-b.diff` (1,283 lines), the changed files in both trees with their callers (`mcp_server.py`, `local.py`, `repl.py`, `fake.py`, `consent.py`, `ui/server.py`, `ui/console.py`, `core/replay.py`), the saves at the root, and the logs of sessions 2 and 4.

**Line references are to the m5c-b tree** (`D:\Projects\FreeSail\FreeSail-gate-m5c-b\`) unless marked `m5c:`.

**What I did not do.** I ran nothing: no game, no test suite, no linter. Every CONFIRMED below means "traced in the code, and where said, seen in a session log or in a save's own transcript". The six re-recorded digests in `tests/test_known_truths.py` were not recomputed.

## 0. Verdict in brief

| Part | Verdict | The reason in a line |
|---|---|---|
| 1. 37b, the rule (return to the station) | **Carry with changes** | The stood-down path is right and proven in play. The opt-out path makes three promises in the consent brief that the code does not keep (F1, F3, F7). |
| 2. 37b, the checkpoint fix | **Carry as is** | Three lines, behaviourally neutral, proven in play. Small follow-ups in F11. |
| 3a. 37c, the wind-shift line | **Carry with changes** | Much better in a breeze. In light airs and calms the mean itself swings and the log still fills, with lines such as "Wind veered to WNW, calm." (F5). |
| 3b. 37c, the taken-aback line | **Carry with changes** | The urgent spam is gone. A notable line can now mask an urgent one (F4), and the no-way line came 92 times in session 4 (F6). |
| 37c as a whole | **State the replay cost** | A replay of a save made before 37c with a model at a station is not the game that was played (F2). CHANGES says the opposite. |

Nothing needs redoing from scratch. The work to do is on the opt-out path and on the two log rules' edges.

## 1. Is the diff the whole difference?

Yes, for code, tests, data and documents. I regenerated `diff -ruN` between the two trees with the author's excludes, plus the one-side-only items, and compared the hunks with the diff file: the same 1,283 lines, the same checksum of the hunks. The root saves and their checkpoints are byte-identical in both trees. m5c's code has not changed since the copy, so the diff applies to m5c cleanly.

| Difference | In the diff? | In CHANGES? | Does it matter? |
|---|---|---|---|
| 22 text files (9 code, 5 tests, 8 documents) | yes | yes | the change itself |
| Three `.webp` files under `docs/references/images/` | named as "Binary files differ" | no | **Not to carry.** Each m5c-b copy is exactly 5,768 bytes longer. Over the length of m5c's file the two differ in two bytes only, both in the RIFF length field; the picture data is byte-identical. The extra bytes are a `C2PA` chunk appended at the end: a content-credentials manifest signed "Anthropic Claude Content Signing", saying "Claude provided this file at the request of a user and may have created or modified the file contents". It is an artefact of how the files were handed from the author's sandbox to the owner's disk. Nothing in code or tests reads these images and no size or hash of them is recorded. Keep m5c's originals: the manifest is wrong provenance for a museum scan and a public-domain line drawing. |
| `docs/agents/consent/2026-10-03-opus-5.5.md`, only in m5c-b | no | only in general | The re-ask that the changed **Leaving** section caused, answered yes with the drill passed, by the session that wrote the change ("The change to Leaving is one I asked for and agree with"). It is the only record made against the new brief (sha256 `f667a04e00b32e1f`; every m5c record is `a3321736a036ae64` or older). See section 8. |
| `.github/`, `.mcp.json`, `merchant-cutter.yaml`, `merchant-ship.yaml`, four records of 2026-10-04, the notes file: only in m5c | no | no | Known to the lead. They are the reason to apply the diff and not to copy the folder. |
| `CHANGES-m5c-b.md`, `m5c-b.diff`: only in m5c-b | n/a | n/a | the description itself |

Nothing else differs.

A side fact from the file times: 37b landed on the owner's disk at 04:26 to 04:36, 37c at 07:25, and `agent.py`, `test_known_truths.py`, CHANGES and the diff at 08:36. Seatings three to five of the Harpy were played between 04:46 and 05:48. So the station brief's opt-out sentence the officer read then was, by CHANGES' own account, the earlier wording ("the consent question"), replaced at 08:36 after the slow tier failed on it; the dumps do not hold the brief, so I could not read it. 37b was played live before its slow tier had been run.

## 2. The author's claims, each with a verdict

| Claim in CHANGES | Verdict | Where |
|---|---|---|
| `MAX_SEATINGS` is gone; how the station was left decides | CONFIRMED in code | `agent.py:555`, `:887-888`; `harness.py:1900`; `remote.py:313`, `:325` |
| Stood down (captain, `hand_over`, the door closing, the ten minutes): seated again as it was, as often as asked | CONFIRMED in code at the agent API (the MCP bridge and the local runner); seen in play, seatings 3, 4, 5 of session 2 and 2, 3 of session 4 | `harness.py:2177`, `:1873-1952` |
| Left by the token or `opt_out`: the question again first, the drill carried | PARTLY. A yes works as said. Anything but a yes is not kept (F1). Not for a station from an m5c checkpoint (F9). Not enforced by `Harness.reseat` itself, and the REPL door cannot seat again at all (F8). | `remote.py:350-374` |
| `opt_out(final=true)`: not in this game | PARTLY. Holds in turn and out of turn at the station. Lost when the token is in the same reply (F3); has no effect when given in the re-ask conversation (F1); the tool itself can be refused (F10). | `harness.py:2206-2210`; `remote.py:618-622` |
| The log names the seating; the journal too | CONFIRMED | `harness.py:1935-1947` |
| A station loaded from a checkpoint is taken over by the same model | CONFIRMED. "The same model" is equality of the name string; see F11. | `replay.py:294-304`; `remote.py:326-338` |
| "old saves read the same" | PARTLY. True of the JSON format. Not true of what an old save does when replayed (F2), nor of an opted-out station in an old checkpoint (F9). | |
| Wind shift: the ten-minute mean, two points from the last line, held a minute; a steady turn about six minutes later; a flicking air not logged at all | CONFIRMED in code. "Not at all" is NOT borne out in play in light airs (F5). | `world.py:1060-1085` |
| "closes the M5 spec's open item 11" | PARTLY. The log now reads the same quantity as the `a wind shift` event. Three definitions still stand (section 6). | |
| Taken aback: once an episode, re-armed after a minute clear; urgent only with way on, four knots apparent, no anchor or ground | CONFIRMED in code, with F4 and F6 | `integrate.py:248-281` |
| The kind is still `ship.aback`; the per-sail lines unchanged | CONFIRMED | `sails.py` untouched |
| "the simulation itself is unchanged" | CONFIRMED by inspection for a game with no model at a station: both rules write only their own bookkeeping, draw no randomness, and nothing else reads that state (grep). NOT true of a replay with a model's transcript (F2). | |
| 57 urgent lines became 3 urgent and 8 notable in the naval cruise | CANNOT TELL (not run). The arithmetic is consistent with the line count: 57 to 11 is 46 lines fewer, and the count fell by 48 (2014 to 1966), which leaves two for the wind-shift lines. | `test_known_truths.py:3706` |
| The changed **Leaving** section makes the game ask every model again | CONFIRMED, and handled in code, not only described: `consent.RE_ASK_SECTIONS` names "Leaving" (`consent.py:187-194`) and `decide` compares each record's brief with the brief as it stands (`consent.py:712-722`). At the officer's station the drill follows the yes. | |

## 3. Findings, most serious first

Sizes: S under about 30 lines in one place; M one module with tests; L several modules or a decision first.

### F1. After an opt-out, anything but a yes at the re-ask is asked again at every later door start. CONFIRMED (traced; not run). Part 1.

**What.** The desk forces the consent question whenever the released station's `left_by` is "opted out". It never looks at what the model answered the last time it was asked back. `left_by` changes only when the station is seated again, so a no, a leaving or a silence at the re-ask leaves the station in a state where every new door start puts the brief and the question once more.

**Where.** `freesail/agents/remote.py:325`, `:359-365`:

```python
opted_out = existing.agent.left_by == OPTED_OUT
...
record, kind, why = consent.decide(
    model_name, self.records_dir, door,
    drills=_drills(name, world),
    ask_again=ask_again or opted_out,
)
```

`consent.py:707-708` returns before the record on file is read:

```python
if ask_again:
    return None, CONSENT_KIND, "the owner asks again"
```

`remote.py:597-601`: when the answer is not a yes the seat is stopped and nothing is written to the station. `consent.py:889-892`: an `opt_out` in the conversation is recorded as "left with the token"; a `final` flag given there is set on the conversation's own pseudo-station (`consent.py:803-813`) and never reaches the game's.

**Why it matters.** The officer leaves on purpose with `opt_out`, without `final`. The owner starts the door again. The brief and the question come; the instance answers "No." The record says no, and over MCP the model is told "the question is not put again unless the game changes in a way that bears on it" (`consent.py:251-255`). The next time Claude Desktop is restarted, which the owner's note 14 says is routine, or the runner is started, the first tool call gets the consent brief again. An instance with no memory of the leaving that says yes is drilled and seated. The same happens if the model answers the re-ask with the token or with `opt_out(final=true)`: the record says it left, `no_return` stays false, and it is asked again.

This is the one place in the harness where a no on record is put again without the owner's `--ask-again`. It contradicts three texts: the consent brief ("a leaving that was meant is held to", `docs/agents/ConsentBrief.md:19`), the commitments table ("Only a yes proceeds; a no is respected without asking", `docs/agents/README.md:48`) and `docs/agents/Harness.md:77`. m5c never had this path, because it never asked.

**What I would do.** Force the question only when the latest record for the identity is a yes, which is the record the station was seated under. Otherwise fall through to `decide` as m5c did, which answers 403 with `gate`'s words, until the owner asks on purpose. If `final` is kept, make it count in the re-ask conversation too (a recorded door act that sets `no_return`). Add the test: opt out, be asked back, answer no, ask for the station again, expect 403 with the record named.

Size S. No risk to replay: the desk's choice is not replayed.

### F2. A replay of a save made before 37c, with a model at a station, is no longer the game that was played. CONFIRMED (traced in code and in the save's own transcript; not run). Part 3.

**What.** A station's orders are not journaled; a replay gives the model's recorded replies again through `Playback`, and `Playback` hands out a reply only when the harness has a sample open. The harness opens samples from the log's lines. Change which lines are urgent or notable and the samples open at other ticks, so the recorded replies, and the orders in them, land at other ticks.

**Where.** `freesail/core/world.py:1001-1007` ("an agent's station's order ... not journaled, since its replies are its harness's transcript and a replay gives them again at their ticks"). `harness.py:780-782`, where any urgent line ends a stand-by:

```python
urgent = self._urgent_in(new)
if urgent is not None:
    return f"an urgent event: {urgent.text}"
```

`harness.py:2292-2300` (`Playback.reply` is reached only from `_poll`, with a sample open). `integrate.py:258-281` (the line is now notable, or not written).

**Why it matters.** `Harpy-Back-At-Falmouth.json`, at the root of both trees. On the night of 15 June she lay becalmed ("Hove the log: no way" at tick 324,031 and 327,631; the wind "calm" at 329,038). The officer stood by "until a wind shift". Under m5c the urgent "Taken aback" woke it at 324,776, 326,302, 327,640 and 328,835. The save's transcript holds the replies to those wakes:

```
324778  stand_by(until='a wind shift')
326305  stand_by(until='a wind shift')
326351  submit_order('clew up the courses')      (the captain's word at 326,348)
326352  submit_order('clew up the topgallants')
326354  submit_order('take in the staysails')
327650  stand_by(until='a wind shift')
328838  submit_order('clew up the topsails')     (the wake at 328,835)
328840  submit_order('take in the jib')
```

Under 37c, with no way on her and the air calm, those four lines are at most the notable "Her sails aback; she had no way on to lose", and a notable line does not end a stand-by for an event. In a replay the entry of 324,778 waits for the next sample to open, at the latest the captain's word at 326,348. Whichever sample that is gets a stand-by for its answer, and the three orders that answered the captain in the game are given at some later sample. Every reply after that goes to a sample it was not written for. The sails she carried through the calm differ, and by tick 527,255 it is another game. Exactly where each reply lands I cannot say without running it; that they move is certain once the first wake is gone.

When a replay is used: `replay.load` falls back to it silently when a checkpoint is missing, does not belong, or fails to unpickle (`replay.py:323-334`); the REPL's `--load` and the console's `replay` always replay (`repl.py:417-418`, `:599-610`; `console.py:392-400`). Loaded from its checkpoint the save is exact, which is how session 2 went on.

Three lesser consequences of the same kind:

- No m5c save replays to the digest it printed when it was saved, with or without a model, since nearly every game has `wind.shift` lines. The check `Harness.md` describes ("the game's terminal names the file and the log's digest") fails for every older save.
- The driver's auto-slow lines are inputs and are written again verbatim, so a replayed log holds "Compression eased to 1x: Taken aback ..." after an urgent line that is no longer there.
- The four saves in m5c-b's own `saves/` from session 2's continuation (ticks 527255, 573848, 602100, 689841) were made under 37b before 37c landed, so they are in the same position.

CHANGES says "Everything else is as in m5c, and so are the saves" and "the simulation itself is unchanged". Both hold for the checkpoint path and for a game with no model. Neither holds for a replay with a transcript. The method used to re-record the known truths cannot see this: all six runs sail under the book with no agent.

**What I would do.** Say it plainly in the package's notes. Stamp the save: `ENGINE_VERSION` has been "0.0.1" since M0 (`world.py:27`) and `matches()` does not read the checkpoint's `engine` (`replay.py:307-314`). Have `load` say so when it replays a save from an older stamp that holds a transcript. The project has done this once for a harness rule (`stand_by_ends_turn`, `harness.py:476-478`, "a save recorded before that rule replays by the old one"). The lasting cure is for a replay to open samples where the transcript says they were opened, not where today's log rules would open them; that is a design item, not part of this merge.

Size S for the words and the stamp; L for a transcript-driven replay.

### F3. The token in the same reply as `opt_out(final=true)` drops `final`. CONFIRMED. Part 1.

**Where.** `harness.py:1091-1095`:

```python
for piece in reply.pieces():
    if OPT_OUT_TOKEN in piece:
        self.leave(_reason_after_token(reply, piece), how="the token")
        return
```

and the same out of turn, `remote.py:614-617`. The scan comes before the calls, as it must, and `leave` is called without `final`.

**Why it matters.** A model that means to go for good and says so twice: `opt_out(reason="FREESAIL-OPT-OUT: I do not wish to continue", final=true)`. Over MCP the scan reads the whole call. The log says "has left the game by the token"; nothing says it asked not to be seated again; the result does not tell the model its flag was ignored; the station can be seated again. The tool's own description invites the pairing ("the same as writing the token").

**What I would do.** In both token branches, read `final` from any `opt_out` call in the same reply and pass it to `leave`. Size S, with a test. A replay keeps it, since the reply is in the transcript.

### F4. Taken aback: a notable line masks a later urgent one, and urgency is read from one instant's apparent wind. CONFIRMED in code; the first harm PLAUSIBLE, the second seen in play. Part 3b.

**Where.** `freesail/physics/integrate.py:248-281`.

```python
if sail_set and pressed and st.last_thrust_n < 0 and not in_stays:
    if st.seconds_aback == 0.0:
        st.aback_had_way = d.u >= units.knots_to_ms(hp.WAY_ON_KN)
    st.seconds_aback += dt
    st.seconds_clear_of_aback = 0.0
else:
    st.seconds_aback = 0.0
    st.seconds_clear_of_aback += dt
    if st.seconds_clear_of_aback >= hp.ABACK_REARM_SECONDS:
        st.aback_noted = False
if st.seconds_aback >= hp.ABACK_SECONDS and not st.aback_noted:
```

**(a) No escalation.** `aback_noted` is one flag for both severities and is cleared only by sixty unbroken seconds clear. A ship ghosting in a flickering air gets the notable "in the light air" line; while the thrust keeps crossing nought more often than once a minute she is never a minute clear. A breeze then fills in from ahead and takes her aback with way on: every condition for the urgent line holds and nothing is logged. The very state that made the old rule spam, a thrust flickering every few seconds, is the state in which the new rule is deaf. The new test `test_a_flickering_aback_is_one_line_until_a_minute_clear` (`tests/test_hull.py:344`) pins the lockout itself: one urgent line, then silence through three more catches with six knots of way on. No test puts a notable line first and an urgent case after it.

**(b) "Had way" is taken at the start of the last unbroken run, not of the episode.** `seconds_aback` goes back to nought on any single tick that is not aback, and `aback_had_way` is read again at the next. A ship caught aback with way on, whose thrust flickers while she loses it, can complete her first ten unbroken seconds with under half a knot left, and is then told "she had no way on to lose". PLAUSIBLE.

**(c) The wind test.** `st.aws` is the apparent wind over the ground at the last substep of the logging tick, so it holds the tide's stream and the gust or lull of that second, and it has no hysteresis. In session 4 off Roscoff, in what the log's own line called "light airs": notable "in the light air" at 202,435, 203,273 and 203,454, then **urgent** at 203,621, seven seconds after the officer wrote "She's lost steerage way, sir: two knots of air from right astern and no speed". The class of the line flips about the threshold.

**(d) What "something to lose" leaves out.** A ship with no way on, struck from ahead by a strong wind, gets the notable "she had no way on to lose". The hazard there is the rig and sternway, not her way.

**(e) Not new.** Yards laid aback by order (`back the main topsail`, a level-0 order whose evolution's subject is the yard) still log the urgent "Taken aback" ten seconds later, as primer 4 itself shows (`docs/primer/04-trimming.md:77`).

**(f) The words.** "she lost her way" and "she has lost what way she had" are asserted ten seconds in, without looking at her speed.

**What I would do.** Keep the lockout per severity: a notable line must not stop an urgent one. Take "had way" where the episode begins (the first aback tick after she was last clear) or keep the greatest headway seen in the episode. Read the wind as the mean true wind, or better read the force itself (`last_thrust_n` against her mass), which scales with canvas and wind and knows nothing of the tide. Give the thresholds a margin. Size M with tests. Risk: the six digests move again.

### F5. The wind-shift line still chatters whenever the mean itself moves, and it names a direction for a calm. CONFIRMED in play. Part 3a.

**Where.** `freesail/core/world.py:1060-1085`. The rule tests only the direction of the mean wind vector (`physics/wind.py:290-294`), which is ill-defined when the resultant is small.

**Why it matters.** Session 4, the whole of it on m5c-b: 69 `wind.shift` lines, 33 of them in "light airs" or "calm". Among them:

```
215138  Wind veered to W by S, calm.
216057  Wind veered to WNW, calm.
216324  Wind veered to ENE, light airs.      (267 s later, the mean gone round by half the compass)
203976  Wind veered to ENE, light airs.
204052  Wind veered to E by S, light airs.   (76 s later)
204751  Wind veered to SW by W, light airs.
204833  Wind veered to W, light airs.        (82 s later)
```

Twenty-one of the 68 gaps are under five minutes; the shortest is 76 seconds, so the minute's hold is no limit on the rate. It is not only light airs: in the last three hours of the session (547,589 to 558,358), mostly in a gentle to moderate breeze, 22 lines came while the base wind swung, twelve of them within five minutes of the line before and the closest 87 seconds apart. The author's own note says the cause is in the weather systems and that the fix does not touch it; the log's rule should still not report it line by line.

The new test (`tests/test_weather_script.py:174`) flicks the wind four points either way every minute, symmetrically, so the mean stands still by construction. It proves the easy case. The primer's sentence "not at all for an air that flicks about and comes back" (`docs/primer/06-the-watch-and-the-log.md:132`) is true only of that case.

**What I would do.** No "veered" or "backed" line while the mean speed is under the light-breeze mark (four knots, the same number the aback rule uses), and none while the wind is unsteady: the ratio of the mean vector's length to the mean speed is the usual measure, and under about a half the right line is one "The wind light and variable", once. That removes 33 of session 4's 69 lines and the nonsense of a calm that veers. Add a test built from the Penlee trace. Size S to M. The playtesting model asked for the same floor (notes, item 18).

### F6. The no-way aback line came 92 times in session 4. CONFIRMED in play. Part 3b.

Session 4's `ship.aback` lines: 5 urgent, 4 notable "in the light air", and 92 notable "Her sails aback; she had no way on to lose". Ninety of the 92 fall in one calm of twenty hours (ticks 319,676 to 391,566), most of them five to fifteen minutes apart (56 of the 89 gaps), the closest three minutes, eight in an hour at worst. In the same window the per-sail lines, which 37c leaves alone, came 216 times; all told one notable "aback" line every four minutes. Notable lines are never rolled up, they sample a station that is not standing by, and they wake a stand-by for "a notable event".

"Once an episode, again after a minute clear" is kept to the letter. In a calm, episodes come every few minutes.

**What I would do.** For the no-way and light-air cases re-arm on a change of state, not on time: when she next has way on, or the mean wind is next over the floor. Or make every such line after the first routine. The per-sail lines want the same treatment. Size S. The playtesting model asked for this (notes, items 17 and 18).

### F7. The re-ask does not tell the instance asked that an instance left, or why. CONFIRMED. Part 1.

**Where.** `remote.py:391-427`, `consent.py:829-843`. What is put to the model is the standing brief and `CONSENT_QUESTION`. That the station was left by opting out goes to the owner's terminal (`seat.words`) and to the record's notes; the reason the leaving instance gave is in the station's journal, which no tool reads.

**Why it matters.** Through Claude Desktop the instance that answers is often a new conversation. It is asked a question it has no reason to answer differently from the first time. "A leaving that was meant is held to" then rests on nothing: the leaving instance's reason is not before the one who decides. The API test checks the words in `a["words"]` (`tests/test_officer.py:1007`), which is the owner's line, not a turn.

**What I would do.** Put it as data in the conversation, before the question: that an instance of this model at this station in this game left at such a time by the token or by `opt_out`, with its reason quoted, and that the question is whether an instance should take the station again. Size S.

### F8. The rule is the desk's alone. CONFIRMED. Part 1.

`Harness.reseat` checks the identity and `no_return` and nothing else (`harness.py:1890-1904`); its docstring says the question "is the door's". The new test seats a station that left by the token with no question at all (`tests/test_officer.py:849-857`). `reseat` has one caller, `remote.py:441`. The REPL door has none: started on a save whose station is released it prints "The station is released" and exits 3 (`repl.py:416-453`), so "may be seated again" in the documents is not true at that door, in m5c or now.

**What I would do.** Let the harness keep its own rule: `reseat` refuses a station whose `left_by` is "opted out" unless the caller hands it the yes that was just recorded. Then a door written later cannot forget. Size S.

### F9. An opted-out station in an m5c checkpoint reads as stood down. CONFIRMED by trace. Part 1.

`left_by` is new and defaults to `""` (`agent.py:887`). A checkpoint pickled by m5c has no such attribute, so the loaded station gives `""`, and `remote.py:325` asks only whether it equals "opted out". The same save replayed rebuilds "opted out". So one file gives two answers by the road it was loaded. The owner has such a station: the watcher in `Harpy-Back-At-Falmouth` (`qwen3.8:27b ...`, through the runner, "released: left the game: Captain's word: stand down at Falmouth run's start").

**What I would do.** Where `left_by` is empty on a released station, read `released_reason` ("left the game ..."). Two lines. A test can strip the attribute before pickling.

### F10. Not in the diff, but it now bears on `final`: the `opt_out` tool can be refused. CONFIRMED by reading; the code is the same in m5c.

- Past the sample's budget. `harness.py:1101-1114`: a ninth counted call is "Not run", and only `answer` and `say` are free (`BUDGET_FREE_TOOLS`, pinned by `tests/test_agents.py:2056`). Through MCP each tool call is a reply to the same open sample and the count runs across them. A model that has read eight pages in a turn and then calls `opt_out` is told to call it again in its next sample.
- With an argument the tool does not know, in turn. `tools.py:831-836`: "opt_out does not take ...". Out of turn the same call leaves (`remote.py:618-622`).

The token still leaves in both cases. But `final` exists only on the tool, and `Harness.md:225` says the tool leaves "at once, whatever else the reply said". One fix serves both: run `opt_out` before the budget and the argument check. Size S.

The second point has a cross-version edge that CHANGES' "Running it" section opens: with `PYTHONPATH` set, the bridge offers `final`; if the server is then m5c, `opt_out(final=true)` is refused in words and the model stays at the station.

### F11. Taking over a loaded station: sound, with four things to know. CONFIRMED by reading. Part 2.

1. **No line.** `take_over` writes nothing in the log or the journal (`harness.py:626-641`) and counts no seating. In session 2 the only trace that a new session took the Harpy's station after the load is the officer's own word at tick 527,255. "The log says when a station is seated again" does not cover it.
2. **"The same model" is the name string**, and the check is skipped when the save's name is empty (`remote.py:333`: `existing.model_name not in ("", model_name)`). A station seated by `--watcher fake`, or through the REPL (which never sets `model_name`), can after a load be taken by any model with a yes on record. The replay road already allowed this; the fix extends it to the checkpoint road, which is the usual one. The door is not compared at all.
3. **The consent gate does run** for the model taking over (`remote.py:359`).
4. **The silence clock runs before the door attaches.** A loaded station's samples open and stay open, and after its patience (an hour of ship's time for the officer, twelve real seconds at 300x) it is nudged, then paused, then stood down by the ten minutes. A model that spends some minutes on its re-ask and drill while the clock runs finds its station paused for a silence that was not its own. `take_over` resets none of it. Recoverable (`resume the officer`, or the stand-down and a reseat). Not seen in play, because the owner did not run the clock.

**What I would do.** Carry the fix. Add a notable line and a journal entry for a take-over, as a recorded act. Reset the silence state in `take_over`. Tests for a loaded station that is standing by, paused, or has a sample open, and through the runner's door. Size S to M.

### F12. Tests: what is missing or says more than it does. CONFIRMED. See section 4.

### F13. Wind shift, lesser points. CONFIRMED by arithmetic. Part 3a.

- **The line names the mean at the moment the hold ends, which for a sudden shift is part-way.** For a step in a steady breeze (my arithmetic on the vector mean, not a run):

| Step | Logged after | The line names | Left unlogged when the wind has settled |
|---|---|---|---|
| 2 points | 11 min, if at all (the mean only just reaches the mark) | 2.0 points | 0 |
| 3 points | 7.6 min | 2.3 points | 0.7 |
| 4 points | 6.0 min | 2.4 points | 1.6 |
| 8 points | 3.9 min | 2.9 points | a second line follows |
| 16 points | 6.0 min | the reversal whole | 0 |

  The old rule left the log up to two points stale as well, so the bound is the same; what is new is that the first word after a front is a direction the wind never settled on. A captain taken aback by a four-point shift reads of it six minutes later.
- **Three definitions still stand**: standing orders on the true wind read the instant wind (the test pins it at 24 minutes against the log's 30, `tests/test_weather_script.py:169-171`); `a wind shift` is the mean a point from where the order or the stand-by began; the log is the mean two points from its last line, held a minute. The spec's "Unified" (`docs/TechnicalSpec-M5.md:696`) is honest about the references and silent on the thresholds. Before 37c the log agreed with the standing orders and not with the event; now the reverse. A player still sees them disagree: in session 4 the officer's standing order `at a wind shift then trim sails` fired 40 times, and only 12 of those firings have a "Wind veered" or "Wind backed" line within ten minutes either side. The same holds for an officer woken by "a wind shift".
- **An m5c checkpoint** holds an instant direction as the last logged; the first comparison after the load is the mean against it, so one line may come a minute after loading.
- Stale comment: `freesail/api/readings.py:2103` still says the log's line reads "the wind itself".

### F14. Harness, lesser points. Part 1.

- **`final` cannot be undone**, by the owner or anyone (`remote.py:313` refuses before `ask_again` is read), and it is one boolean on a tool every model is offered. `truthy` (`tools.py:563-567`) is rightly cautious: only `true`, `1`, `"true"`, `"yes"`, `"1"` set it; a missing argument, `""`, `"false"`, `"no"`, `"0"`, `None`, `0`, `1.0` and anything unknown do not. A local model that fills every argument from the schema's words ("true to ask not to be seated again") can still set it, and the cost is the game's station. Whether the owner's deliberate `--ask-again` should be able to put the question once more is the owner's to rule; the description should at least say "leave it out unless you mean it".
- **The carried drill.** The note is added when the conversation is built (`consent.py:792-798`), so a record whose verdict is no also says the drill "is carried to this record". The header of a yes says `drill: passed` with nothing to tell it from a drill that was run. The source is named by date only, and three of qwen's records share one date.
- **Left-overs at a reseat** (`harness.py:1915-1952`): notices never delivered (the pause's "you were not stopped"), a `tell` not yet carried, and `_handover_asked_at` from the conversation before.
- **Words.** "it had stood down by the captain" wants "been"; "through mcp" is the door's key and not its words.
- **`agent.py:50-52`**: the three new names sit unsorted in `__all__`.

### F15. Documents and book-keeping. CONFIRMED.

- Stale: `docs/DesignProposal.md:622` ("seated again once"); `docs/dev/TuningNotes.md:1427` (the `MAX_SEATINGS` row; the three new constants have no rows); `docs/gates/gate-m5c.md:18` and `docs/agents/ConsentAndPreferences.md:51` (history, may stand with a note).
- `docs/agents/README.md:48` and `docs/agents/Harness.md:77` are now untrue for an opted-out station (F1).
- The six constants in `tests/test_known_truths.py` were moved with no line in the comments above them (the comment at `:2491-2492` still explains 617) and none in TuningNotes, where every earlier move has its reason. The reason is in CHANGES only, which the main line will not carry.
- Primer 6 says "in a breeze of four knots or more" (`:114`); the code tests the apparent wind. It says the wind lines read the mean "as the readings do"; the readings give both.
- The primer's shown logs with the urgent line (`04-trimming.md:77`, `05-going-about.md:100`, `06:128`) are prose and no test runs them. The one after missing stays may now be the notable line.
- Harness.md says nothing of loading a save whose station was manned; the fix is described in CHANGES only.

## 4. Tests

**What the new and changed tests prove.**

| Test | Proves | Does not prove |
|---|---|---|
| `test_officer.py:841` seated again, and replays | Four seatings at the harness with the words and the count; another identity refused; `left_by` set by the token and by the captain's stand-down and cleared; three reseat acts replay to the same digest | That an opted-out station is asked first: it is seated with no question (F8) |
| `:899` `opt_out` final | In turn: the flags, the log line, the refusal, the replay; eight values of `truthy` | Out of turn; with the token; `None`, `0`, `1`, `1.0` |
| `:940` loaded from its checkpoint | Another name refused; the same name gets the station; no seating counted | That the model can then act; a station standing by, paused or with a sample open; an empty name; the runner's door; any line in the log |
| `:974` the agent API | Opt out, question again, yes, seated without the drill, the note in the record; seatings 3 and 4 after a door's release; final refused | **Its comment says "opt_out with final, out of turn" (`:1023`); it is in turn.** The reseat opened a sample ("seated again"), so the reply is delivered. The out-of-turn path (`remote.py:618-622`, `harness.py:1627-1628`, `:1678-1680`) has no test anywhere. Nor has a no at the re-ask (F1). |
| `test_agent_api.py:281-305` | A third seating through the API after a door's release | |
| `test_hull.py:314`, `:344`, `:357` | Urgent with way on in fifteen knots; one line through flicker; notable with no way, in a light air, aground | **"at anchor": the test is named for it and tests aground.** The values at the thresholds. A notable line followed by an urgent case (F4a). |
| `test_weather_script.py:151`, `:174` | The lag on a steady turn (30 and 55 minutes); symmetric chatter not logged | A sudden shift; an asymmetric swing; light airs; a squall; the first ten minutes; a load |

**Expectations moved.**

- With a stated reason: the reseat tests (the rule); `test_hull.py:320`, `:332-333` (way on, and a minute clear); the veering test's ticks, 1440 and 2880 to 1800 and 3300 (the docstring works the sum).
- Without one: that test's tolerance widened from 1 to 2. The six known-truth constants, whose reason is in CHANGES and not at the constants (F15).
- Bent to a test: the station brief says "its consent is asked again first" because `tests/test_local_runner.py:466` forbids the substring "consent question" in a station's messages. The check's intent is kept; the check is a brittle one and the brief's words now turn on it.

**Through each door.** The opt-out re-ask and the checkpoint fix are tested through the agent API, with `door: "mcp"` in the request body. Neither is tested through the bridge (`tests/test_mcp_server.py` has no reseat, re-ask or `final`), nor through the runner's loop (`tests/test_local_runner.py` likewise), where the developer's turn after the answer is part of the conversation. The REPL has no path to test.

**Cases with no test.**

1. A no, a leaving or a silence at the re-ask, and the next request for the station.
2. `opt_out(final=true)` in the re-ask conversation.
3. The token with `opt_out(final=true)` in one reply.
4. `opt_out` with `final` out of turn, and its replay from the door act.
5. `left_by` and `no_return` across a checkpoint; a checkpoint without the new fields (agent, hull and world).
6. A reseat or re-ask through the bridge and through the runner.
7. A take-over of a loaded station that is standing by, paused, or has a sample open.
8. Aback at anchor; aback notable then urgent inside the minute; the thresholds.
9. A wind shift in light airs; a sudden shift; the line across a save and a load.
10. A replay of a save made under the old log rules (F2).

## 5. The promises: the words against the code

**`docs/agents/ConsentBrief.md:19`, Leaving.**

| The words | The code |
|---|---|
| "an instance whose station was stood down or handed over may be seated again in the same game by the same identity" | True at the agent API: the same name string. Not at the REPL. The party seated is whichever instance next comes under the name. |
| "One that left by the token or `opt_out` may be seated again too, but this question is put to it again first" | True at the agent API. "To it" is whichever instance comes next, and it is not told of the leaving (F7). Not for an m5c checkpoint (F9). |
| "so a token written by accident costs one answer" | True: the drill is carried. At the runner there is also the developer's turn. |
| "and a leaving that was meant is held to" | **Not kept** (F1). |
| "`opt_out` with `final` set leaves the game for good, and the station is not seated again in it" | Kept at the station, in turn and out. **Not** with the token in the same reply (F3), **not** when given in the re-ask (F1), and the tool can be refused (F10). Not said: no one can undo it, and no other model can take that station either. |
| "The log says when a station is seated again." | True for a reseat. A take-over after a load writes nothing (F11). |
| "The human may keep playing without the model; the model's part is over." | Kept from the old text; it now sits two sentences before "may be seated again". |

**The station brief's opt-out item** (`agent.py:658-667`) says the same, with "can be held to" for "is held to". The tool's description (`tools.py:720-732`) agrees with the code.

**`docs/agents/Harness.md:258`**, **`docs/agents/README.md:27`, `:32`**, **`docs/primer/16...:86`**, **`ConsentAndPreferences.md:27`**: each matches the code as far as the brief does, and no further. "As often as you ask it back: start the door again as before" hides one thing the code does: the bridge stations once in its process (`mcp_server.py:440-441`), so through Claude Desktop coming back still means restarting the app. 37b removed the count and not that friction (the owner's notes 12 and 14).

**Done and not said.** A stood-down station is seated again by the first tool call of any new door under the name, with no act of the captain's in the game: seating four of session 2 came three ticks after "the client disconnected". That reaches the harness's own last stop too: a station stood down by the ten unattended minutes comes back when its door does. The safeguard is real and worth saying in the documents: a reseated officer has not the deck until the captain gives it (`harness.py:1924`).

## 6. Design shape

**Part 1, the rule.** Replacing a count with "how it was left" is the right key, and the stood-down half is right as built. On the rest:

- *Is `final` on `opt_out` the right place for "do not ask me back"?* Not as the main place. The natural place is the re-ask itself: an instance asked back says no, and the no is kept. That needs no new flag, only F1 mended, and it is the consent rule the project already has. `final` is then a convenience that spares a model one question it has answered in advance. If it stays it must work wherever leaving works: with the token (F3), in the consent conversation (F1), past the budget (F10). A token form of it would serve the doors where the model leaves in words.
- *Should the rule tell a session that returns from another session of the same model?* It cannot today, and the documents should stop implying that it does. The code has no session. Identity is the name the owner typed or the server reported. The API takes a reply for a station from any client that posts to it (`remote.py:540-551`); the owner's local note 5, a Claude Desktop session's calls going through in the place of the local model, is that. One Desktop bridge serves every chat in the app. So "a session may come back" is in fact "the same name may take the station again". If the difference matters, and after an opt-out I think it does, the cheap means is a nonce given in the station's brief and asked for at the return: a conversation that still has its context can show it and returns as itself; one that cannot is a new instance, is told so, and is told what its predecessor did and said (F7). Short of that, F7 and a line in the log for every take-over.
- *What "seated again as it was" lacks.* The returning session gets the brief and the last twenty lines of the log. It does not get its handover note unless that falls in those lines (the officer's journal, 527,393: "reached me this time only because it sits in the brief's last 20 log lines"), and it has no tool to read its journal (the owner's note 10). With returns now unlimited this is the common road and wants the note in the "seated again" sample. Outside the diff; it decides whether the rule serves.
- *Relief by another model* is still refused ("a station is taken once in a game"). The Harpy's fifth handover was written "for the relief through a local door" and the fifth seating was Opus through MCP again. If the owner's note 12 means that too, it is a separate ruling.
- Keep the rule in the harness, not in one door (F8).

**Part 2, the fix.** Right and as small as it could be. Its one weakness is older than it: the desk tells "the game's own scripted agent" from "a loaded station" by the class of the model object (`isinstance(existing.model, Playback)`). A flag on the harness, or the rule that a station with no name is the game's own and is not handed to a door, would say what is meant.

**Part 3a, the wind shift.** The ten-minute mean is the right quantity for a line in the log, and two points a fair mark. The minute's hold does little: a mean over ten minutes does not flick, it drifts, and when it drifts fast the hold only delays each line by a minute. What the rule lacks is any reading of whether there is a wind to speak of. *Given the author's own field result,* the answer is a floor on the mean speed and a steadiness test, with "light and variable" said once (F5). I would also consider writing the line when the mean has stopped moving, so that it names where the wind went and not where the average had got to (F13).

**Part 3b, taken aback.** *Is time the right key for re-arming?* For the urgent line, yes: a minute clear is a fair meaning of "a new episode". For the two lesser lines, no: nothing has changed in a minute in a calm. Their key is state: way on again, or wind again (F6). The flag must not be shared between severities (F4a). And the test of "something to lose" should read the thing itself, the force astern against her mass and the way she had when it began, not an instant's apparent wind over the ground (F4c). What neither the old rule nor the new one asks is whether she was *taken*: yards laid aback by order are not a surprise, and the code knows which they are.

## 7. Field evidence

**Session 4 (`4-schooner-plymouth-opus`), on m5c-b throughout, 558,434 ticks.**

| Line | Count | Detail |
|---|---|---|
| `ship.aback`, urgent, "Taken aback: the sails pressed against the masts and she lost her way." | 5 | ticks 200205, 203621, 493038, 557579, 557978. Four woke the officer and four eased the clock. Four look real: with way on, shoaling off Roscoff; before a shift into a moderate breeze; after a tack was ordered; on a shift in a gentle breeze. 203621 is F4c. |
| `ship.aback`, notable, "Her sails aback in the light air; she has lost what way she had." | 4 | |
| `ship.aback`, notable, "Her sails aback; she had no way on to lose." | 92 | 90 of them in one calm (F6) |
| `ship.aback`, notable, "... as she lies at anchor / aground." | 0 | that branch has neither a test nor a sighting |
| `sail.backed`, per sail, all notable | 320 | fore topsail 102, fore staysail 61, fore sail 50, jib 47, flying jib 39, fore topgallant 13, main sail 8 |
| `wind.shift`, all notable | 69 | 29 "light airs", 4 "calm", 10 "a light breeze", 20 "a gentle breeze", 6 "a moderate breeze"; 21 gaps under five minutes (F5) |

The `agent.stationed` lines:

```
     12  The officer of the watch takes the station; sampled every glass and on notable and urgent events.
 343381  The officer of the watch takes the station again (Opus 5.5, through mcp): the second seating; it had stood down by the officer of the watch: the deck handed over.
 343551  The officer of the watch takes the station again (Opus 5.5, through mcp): the third seating; it had stood down by the captain: the captain has the deck.
```

**Session 2 (`2-harpy-brig-opus`), on 37b alone from tick 527,255.**

```
 527389  ... the third seating; it had stood down by the officer of the watch: the deck handed over.
 573851  ... the fourth seating; it had stood down by the MCP bridge: the client disconnected.   (3 ticks after the stand-down)
 602283  ... the fifth seating; it had stood down by the officer of the watch: the deck handed over.
```

The checkpoint fix is seen working: the save ends at 527,255 with the officer standing by until two bells; at that same tick, before any tick ran, the new session spoke ("Mr Pearce on deck ... handing over the deck for the reseat test"), which it could only do having taken the loaded station over. No line of the log says that it did (F11). The journal agrees: "Reseat test passed on m5c-b ... no consent question after a stand-down."

The aback and wind lines of session 2 are the old rules' throughout: 31 urgent "Taken aback" (25 woke the officer, 30 eased the clock), 280 `wind.shift` lines in the 45 hours after 527,255.

**Do the logs show the rules doing what CHANGES says?** For the stood-down path through MCP, yes, five times, in the words promised. For the checkpoint fix, yes. For 37c, yes to the letter, with the limits in F4 to F6. **No officer opted out in either session, so the re-ask, the carried drill and `final` have no evidence from play at all**; they rest on two tests through one door.

## 8. Carrying it forward

In order.

1. **Apply the diff; do not copy the folder.** m5c's code is unchanged since the copy, so `m5c-b.diff` applies cleanly. Copying would lose `.github/`, `.mcp.json`, the two new scenarios and the four records of 4 October, and would bring the three stamped images. The new scenario files are data and no test enumerates the scenarios, so they do not meet the diff.
2. **Settle the words of Leaving once, before anything is merged.** Every change to that paragraph asks every model again. In m5c seven identities have a yes as their latest record: Sonnet 5, Sonnet 5.5, llama3.1:8b, Opus 5.5, Gemma4 Q4_K_M, qwen3.8:27b (by digest) and Qwen3.8-27B-0814 (the file). The first three hold records from before package 37 and are due the question anyway. The other four passed the drill under m5c's brief (Opus 5.5 and the three local ones, 2 to 4 October) and will be asked and drilled again at the officer's station. If F1, F3 and F7 are to be mended, mend them first, then fix the words to what the code does, then merge the brief, so that the local models are put through it once and not twice. Put any other pending change to the brief in the same merge.
3. **Mend F1, F3 and F9 with their tests** before the brief goes out, since the brief promises them. F8 and F10 at the same time if the owner agrees; each is small.
4. **The consent records.** Keep m5c's. Carry `2026-10-03-opus-5.5.md` only if the Leaving text is merged exactly as it stood on 3 October; then Opus 5.5 is not asked a third time. If the text changes again, the record is history and the question comes regardless. Add it to the table in `docs/agents/README.md` either way.
5. **37c.** Carry it with the floor and the per-severity lockout (F4 to F6), or carry it as it is and follow at once; either way the six digests are re-recorded on the build machine, and the slow tier is run on the owner's Windows before the numbers are trusted. They were recorded in the author's sandbox, and CI runs the fast tier only, so nothing automatic will catch a mismatch. Write the reason at the constants and in TuningNotes.
6. **Say the replay cost and stamp the saves** (F2). Tell the owner which saves are now good from their checkpoints only: every Harpy save, and anything else with a transcript made before 37c.
7. **Bring the documents in line** (F15): DesignProposal 622, the TuningNotes rows, `readings.py:2103`, the primer's three shown logs, primer 6's "a breeze of four knots", Harness.md on loading a save with a manned station, and the two sentences that F1 makes untrue if F1 is not mended.
8. **After the merge the bridge and the server are one code again**, so `opt_out`'s `final` shows in the bridge without `PYTHONPATH`. Check that the owner's Claude Desktop config no longer sets it.

**What I would not carry.**

- The three `.webp` files.
- `CHANGES-m5c-b.md` and `m5c-b.diff` as files. Fold what CHANGES says into the package's notes, without the "Running it" section and with "the saves are as in m5c" and "the simulation itself is unchanged" corrected.
- m5c-b's `saves/`. The root saves are identical to m5c's. The four from session 2's continuation were made under 37b without 37c (F2).
- The comment at `tests/test_officer.py:1023` as it reads.

## 9. Checked and found sound

- The diff file is the whole difference between the trees (regenerated and compared).
- The seating count: `seatings` goes up once at each reseat and nowhere else (`harness.py:1919`); the return value, the log line and the journal entry read it after the increment; `ordinal_words` is right from 1 to 10 and for 11 to 13, 21, 22, 23, 101, 111. No off-by-one. A take-over counts none, as its test says.
- `left_by` is set on every road out: the captain's `stand down` and `I have the deck`, `hand_over`, a door's release and the ten minutes (all through `stand_down`, `harness.py:2177`); the token and the tool (`leave`, `:2209`). It is cleared at a reseat (`:1923`). No other code releases a station.
- A replay rebuilds both fields: in turn from the reply's own arguments, out of turn from the door act's `final` (`harness.py:1627-1628`, `:1678-1680`). `no_return` is set before the save (`:2210-2211`), so the checkpoint written at the exit holds it. An m5c save has no `final` anywhere and reads as not final.
- The save's JSON does not hold `left_by` or `no_return`, by design; nothing reads them from it. The format is unchanged.
- m5c checkpoints unpickle under the new code: the new fields on `AgentState`, `HullState` and `World` are plain class defaults and the instances fall back to them. The reverse should load too, the extra attributes being plain ones that m5c ignores (read, not run).
- The checkpoint loader's digest check compares the pickled log with its own header, so the changed lines do not affect it in either direction; `matches` reads the seed, the end tick and two lengths.
- The fix changes nothing in a loaded game that no door takes: `Transcript([])` and `Playback(world, [])` both answer `None`, and `Playback` is still a `Transcript` for `tests/test_checkpoint.py:76-78`. The model is not pickled, so a later save is unaffected.
- A different model is refused at a reseat and at a take-over wherever the save names one. The consent gate runs for the model taking over.
- The changed Leaving section is caught by the existing re-ask rule; no new code was needed and none was written.
- A reseated officer has not the deck until the captain gives it.
- `truthy` errs to "not final" for everything but an explicit true.
- 37c touches only its own book-keeping (`seconds_aback`, `aback_noted`, the two new hull fields, `_wind_shift_held_s`, `_last_logged_wind_direction`); no randomness is drawn; nothing else reads any of it. No standing-order event, no stand-by event and nothing in the browser client is keyed on `ship.aback` or `wind.shift`. The new state is in the checkpoint and is recomputed by a replay, so the two roads agree under one code.
- Hove to, and in stays under any whole-ship evolution, she logs no aback line, as before; the truths that ask for none during getting under way are untouched.
- `test_a_backing_script_is_logged_as_a_backing` was not changed and still holds by the same sum as the veering test.
- The method behind the re-recorded truths is sound for what it covers: six runs under the book with no agent, compared line for line with two kinds taken out. The other pinned ticks of those runs were not moved by the diff, which fits.

## 10. Limits

Nothing was run. F1, F2, F3, F8, F9, F10 and F11 are traced through the code line by line and I am confident of them; F2 also rests on the save's transcript and the session log. F4a and F4b are behaviours of the state machine that I have not seen happen. The step table in F13 is my arithmetic on a unit-speed vector mean. The 57-to-11 figure for the naval cruise and the six digests are the author's.
