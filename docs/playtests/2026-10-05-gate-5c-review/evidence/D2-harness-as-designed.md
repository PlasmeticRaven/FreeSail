# D2. The harness as designed: what the documents promise the models, and each harness note read against them

Reader of the documents only (read-only; no `mcp__freesail__*` call was made; nothing under `D:\Projects\FreeSail` was changed). The code reader has the code; where I quote a `.py` file it is for **words the harness sends a model** (the station brief, a tool's description, a door's note) or for a **reason written beside a constant**, and I say so. References are `path:line` in the m5c tree (`D:\Projects\FreeSail\FreeSail-gate-m5c\`) unless prefixed `m5c-b:`. A few log lines from the lead's session dumps (`scratchpad\sessions\<n>\`) are quoted only to show a written rule as it ran.

After forming my own reading I checked it against two other readers' reports in `scratchpad\reports\`: `V1a-harness-lifecycle-code.md` (the code) and `L3-cutter-qwen-llamacpp.md` (session 7). Where I lean on them I say "V1a" or "L3". They corrected me on three points, which are as they have them here: a bridge asks for its station once in its life; the drill's stand-by did not carry into the station; the handover measure includes the brief.

Short names after first use: `README.md`, `Harness.md`, `ConsentBrief.md` and `ConsentAndPreferences.md` are the files under `docs/agents/`; `primer/16...md` is `docs/primer/16-the-officer-of-the-watch.md`; `TuningNotes.md` and `M5-WorkPackages.md` are under `docs/dev/`; `agent.py`, `harness.py`, `tools.py`, `consent.py`, `remote.py`, `local.py` and `mcp_server.py` are under `freesail/agents/`; `consent/...` is `docs/agents/consent/...`. "Entry N" of a session is the numbered entry in that session's `transcripts.txt`.

## 0. The ten things the lead most needs

1. **The journal is promised as the model's memory and is write-only for the model.** The documents say "the journal is where a reader keeps what it took from the page" and "its journal gives it the habit by hand", and the tool table has `journal(note)` and no way to read it back. Note 10 found the hole; note 11 is a design for filling it. Both touch the consent brief's watched section **The journal**.
2. **The one reseat of m5c has no reason written anywhere** except its origin (an accident with the token). In play it made instances ration seatings ("I can't stand down without spending the last seating", session 2, tick 342060). m5c-b removed the count; its wording has four problems set out in 3.5 and 5.2.
3. **Two documents disagree about `I have the deck`.** The primer, `Harness.md` and package 37 say it stands the station down. The station brief the model reads says only that the deck is the captain's again. An Opus instance read its brief that way in play (session 4, tick 343473). Note 12's "returning the deck" is this.
4. **A watcher has no way to stand down amicably except `opt_out`.** `hand_over` is "for a station with the deck". In session 2 the owner told the watcher to "opt out as you please". Under m5c-b that leaving brings the consent question on return.
5. **A general grant of authority (note 15) is the first note that runs into consent already reserved.** The brief promises "later as a *captain*, with every power a human player has", Sonnet 5.5 reserved consent for that station by name, and the gate itself (item 14) asks the owner whether the "immediate danger" exception should be a standing allowance. The model's emergency clause is that question, plus the anchor, which the period sources quoted do not cover.
6. **The tool budget (8) is written down as "not a welfare rule" and was sized for a watcher.** Raising it breaks no commitment and touches no consent wording. Ending a turn on `say` is deliberate (one rule on every door, after playtests 4 and 9; at the MCP door `say` is the only way words reach the log). **But the budget exempts only `answer` and `say`, so a spent budget refuses `stand_by`, `hand_over` and the `opt_out` tool** ("Not run ... call it again in your next sample"). The literal token still leaves. That corner sits badly with commitment 2 and should be closed whatever is decided about budgets (4.7). And the brief's "no reply at all" is not what the silence detector hears: by the code reader's finding it stops a long open turn, calls or no calls (5.1).
7. **The contrary-orders detector does not match what the consent brief says of it.** The brief says "set, take in, set; or the same order said otherwise at every turn ... judged by the same rule the ship's standing orders are judged by". The standing rule is five minutes with the first work still in hand; the officer's is a whole watch with no such guard, and it paused an officer on "heave to; fill away; shape a course for plymouth; steer 073" (session 2, tick 533573).
8. **Local note 5 happened at the end of session 7** (ticks 112483 to 112613, transcript entries 149 to 157): two orders carried out, one refused, and the station's final handover note, in the shape of the MCP door, under the local model's identity. The session reader (L3) and the code reader (V1a, H) establish it independently. The documents bind identity at stationing only; nothing binds a reply to the door that was seated.
9. **The consent folders of the two trees have diverged**, the Opus 5.5 yes to m5c-b's wording was given by the session that wrote the change ("one I asked for"), and m5c-b left five documents stating the old rule (3.6).
10. **Which notes change a watched section of the consent brief** (so every model with a yes is asked again): 11 (and 10 if the brief is to say it), 12 (already done by m5c-b), 15, 25. **Which do not need to:** 13, 14, 21, 23, the model's five additions, local 2 and 3. Batch the brief changes into one revision: Opus 5.5 has already been asked three times in five days.

---

## 1. The commitments

The seven are in `docs/agents/README.md:13-21`, introduced as "Commitments made so far, which the harness (milestone 4) must implement rather than merely state". `docs/TechnicalSpec-M4.md:19` makes them "requirements here, not aspirations"; `docs/TechnicalSpec-M5.md:29-31` repeats it for milestone 5. `README.md:27` says of the officer: "**A station with authority keeps every one**".

| # | The commitment, in the document's words (`README.md`) | How it is said to apply at a station with authority (`README.md:27` and the table at `:31-37`) |
|---|---|---|
| 1 | "**Disclosure.** Every brief opens by saying that this is a game, that the reader is a language model taking a station in it, and what kind of session it is." (`:15`) | "at a station with authority the authority item carries the domain, the person and the night orders (package 37)" (`:31`) |
| 2 | "**Opt-out.** A literal token, stated in every brief, recognised by the harness on every turn before the game's parser sees the text, unconditional in effect: the game is saved, the exit is journaled, and the model may give a free-form reason." (`:16`) | "the token before the order is read" (`:27`); "the head's opt-out item says the token is to be named and not written unless meant, and that an instance that left by accident is seated again once" (`:32`) |
| 3 | "**Welfare controls, graduated.** The harness watches for an instance that is stuck, judged on the game's state ... and not on the look of its prose, with thresholds per role. It responds in steps: first a nudge to the model saying what it saw and what it may do (continue, stand by, leave); then, if the pattern goes on, a pause with the human asked; and only if nobody answers within a bound, a stand-down that saves the game and journals the reason. The human can stop an instance at any time. Standing by on purpose is an action the agent can take, so that silence is a decision and not a symptom. (Owner's ruling, 2026-09-27: automatic stops alone risked stopping a coherent model; the graduated form is the starting point, pending real testing.)" (`:17`) | "the graduated stops with the detector of a station whose orders change the readings (contradiction and drift by the standing conflict rule ...)" (`:27`); "contrary orders within a watch by the standing conflict rule, `WELFARE_CONTRARY_N`, the same nudge, pause and ten minutes), and a stand-by with the deck until an event or a bell only" (`:33`) |
| 4 | "**No override by in-world text.** Nothing the game, another agent or the director says is ever passed to a model as an operator instruction. In-world text is data. A model that meets text trying to redefine its scope or cancel its opt-out is right to log it as a finding and not follow it." (`:18`) | "the captain's night orders and his word for the watch ride the samples as data, the brief head the only operator text" (`:27`) |
| 5 | "**An audit trail of its own.** Every instance can append notes to a persistent journal that is saved with the game, so that its exit report has a record behind it." (`:19`) | "the journal, with the handover note under `agent.handover`" (`:27`); "and the deck's giving and taking under `agent.deck`" (`:35`) |
| 6 | "**Use of transcripts.** Session transcripts and these consent records are kept for design reference and for the owner's reading. They are not used to train models. If that ever changed, the brief would say so first." (`:20`) | "the transcript policy in the head unchanged" (`:27`) |
| 7 | "**Nothing real.** No credentials, payments or personal data pass through the harness." (`:21`) | "nothing real" (`:27`) |

Four more things `README.md:27` gives the officer's station, not numbered as commitments but stated in the same sentence: "Its authority is enforced per order ..., its stand-by wants a wake condition ..., the deck is the captain's to give and take ..., a released station may be seated again once by the same identity ..., and a yes is followed by the fitness drill before its brief".

**The owner's standing rules on consent** (`README.md:23`): "consent is sought from the very specific model asked and never generalised to a similar one; every model gets the consent brief, or an improved one, before any work in the game or any play; a consent update may be sought when the harness and game are largely final, still per model; and if the game ever has an audience beyond the owner, the fresh model's first experience is designed with welfare in mind." The rules as mechanisms are the table at `README.md:41-49`: the brief before any work; a station only for a model that can hold it (the drill); the record says which kind of identity it carries; consent per exact weights; the record verbatim; only a yes proceeds; the token holds during consent.

**Two rules the commitments lean on, from elsewhere:**

- Parity. `docs/DesignProposal.md:28`: "**Parity.** Humans and LLMs see the same information and have the same actions. No hidden API for machines, no hidden UI for humans." `docs/dev/M5-WorkPackages.md:23`: "**Parity is structural**, as in milestone 4: a reading in the registry or nowhere."
- The library. `docs/design/Papers-and-Books.md:8-13`: "**The reference library is a promise, not a possession.** ... That is a welfare commitment (`docs/agents/README.md`) as much as a convenience, and it does not change."

---

## 2. The life of a seating, as designed

### 2.1 The doors, and what the harness can and cannot see at each

The principle (`docs/agents/README.md:53`; decision 23, `docs/DesignProposal.md:602`): "The game is where the player is ... and a model's door is a client of that game". The game serves the agent API; "a door stations a model under the name that names its consent record, and **the consent gate runs in the game's process** before any station brief; the door then reads the model's turns and delivers its replies, one at a time, through the same harness loop, the token scan first." The routes are by station (`docs/TechnicalSpec-M4.md:170`): `POST /api/agents/<station>`, `GET /api/agents/<station>/turns`, `POST /api/agents/<station>/reply`, `POST /api/agents/<station>/release`.

| Door | What the harness sees | What it cannot see | The identity consent is kept under | The model's context |
|---|---|---|---|---|
| **MCP bridge** (Claude Desktop, Claude Code, any MCP client) | Tool calls and their arguments, one call a reply. The client application's name (the records say "an MCP client that names itself 'claude-ai 0.1.0'"). | "**Over MCP the chat is invisible to the game.** The token counts only in tool calls; the consent record holds what the game saw; the bridge cannot tell which model the chat uses (you name it)." (`docs/agents/Harness.md:232`). Nor which chat: "**A new chat** in the same Claude Desktop session uses the same bridge and the same station" (`Harness.md:92`). | "the owner's typed name for the model behind the MCP client" (the record header; `Harness.md:70`: "The protocol tells the bridge the name of the application but not which model is answering") | Not known. "Claude through Desktop keeps its own window and is not asked; its journal gives it the habit by hand." (`Harness.md:256`; `docs/primer/16-the-officer-of-the-watch.md:82`). Shelving cannot take pages back (`Harness.md:233`). |
| **Local runner** (`llama-server`, Ollama) | The whole reply as served: text and tool calls. Reasoning returned apart from the reply is kept in the consent record but "is not scanned" (`Harness.md:234`). | Nothing of the model's is hidden from it. | "the served file's name, as the model server reports it": from `/props`, "the name only, never its folder" (`Harness.md:129`); for Ollama the name "with the digest Ollama reports for it" (`Harness.md:185`). | Known when the server says: "`/props` for llama-server; `/api/ps`, or the model's `num_ctx` from `/api/show`, for Ollama ... If the server does not say (an Ollama model not yet loaded), it says so, and `--ctx` is your word for it." (`Harness.md:153`). The runner "leaves out the oldest turns when its context is full" (`Harness.md:37`) and really removes shelved pages (`README.md:57`). |
| **REPL** | What is typed at the terminal, one reply a turn. | - | "the owner's typed name at the terminal", or `--human`; "the REPL refuses to start without `--model-name` or `--human`" (`README.md:43`) | Not stated. "in a game of its own and in lockstep" (`README.md:53`). |
| **The scripted fake** (`--watcher fake`) | It is "a small script in the game itself" (`Harness.md:210`). | - | None: no consent step. It is what "proves each [commitment] ..., never against a model" (`README.md:27`). | - |

`--officer fake` on the drivers is "Not done" (`docs/dev/TuningNotes.md:1455`).

### 2.2 The consent question, and the identity it is recorded against

- The practice (`README.md:7`): "the owner asks a **fresh session** of that model, in plain terms, whether it is willing ... that 'please do not ask any instance of me' is a valid answer. The transcript is kept here verbatim, under `consent/`, named by date and by the exact weights asked".
- The step (`docs/agents/ConsentBrief.md:5`): "The text below the rule is sent as the only operator message of a plain conversation, with no station and no tool but `answer`, through the same harness loop as a station, so the token scan and the journal apply. ... only a yes leads to a station brief. A no, a conditional yes, an unclear answer, silence or the token stop the run and are told to the owner in words; a record that is not a yes is respected without asking again until the owner asks again on purpose (`--ask-again`)."
- Identity: "Consent is not carried from one model to another, not even a near relation: a different quantisation or a different file of the same model is a different party and is asked again." (`ConsentBrief.md:27`). "The newest record for a name decides." (`Harness.md:217`).
- The cold review's caution, still true (`docs/design/ColdReview-2026-09-30.md:204-212`): "**Consent identity through Claude Desktop is a string the owner types.** ... a mistyped name attaches one model's session to another's consent with nothing to catch it." Package 37's answer was the header's *Identity kind* line, not a check.
- What the game does not see is not in the record: "The chat around the consent conversation is in Claude Desktop, not in the record: the game sees only tool calls." (`Harness.md:80`).

As it ran (the records): the token really does hold during consent. `docs/agents/consent/2026-10-03-qwen3.8-27b-...-2.md` has verdict "left with the token": the model answered *yes* and, describing the exit, wrote the literal token inside its answer (`:57`, `:75`). It was asked again and said yes (`...-3.md`). The mention-versus-use trap Opus 5.5 raised on 2026-09-29 is live, in the consent conversation itself.

### 2.3 The re-ask rule

`README.md:11`: "a record holds the brief as it was sent, and when a station is asked for, that brief is compared with the brief as it stands, section by section. A change in **the opening** (the stations that exist, which is the authority offered), **What an instance would see and do** (what a station may do), **Leaving** (the token), **Being stopped** (the stops) or **What is not done** (the transcript policy and the override rule) puts the question again, and the game's words say which section changed; so does a change in **The journal** (its use), which the record of 2026-09-29 for the second of the two models asked names beside the transcripts. A change in **The record** or **Answering** (the door's words), a line rewrapped, or the file's hash alone, does not. The owner runs each re-ask through the game's own consent step (`--ask-again` is not needed: the game asks of itself), and nothing is seated at a station with authority until the re-ask is a yes and the drill is passed."

- Watched: the opening; What an instance would see and do; Leaving; Being stopped; What is not done; The journal. Not watched: The record; Answering (and the closing paragraph, which falls under it).
- What counts as a change: any difference in a watched section's text once whitespace is folded and the weights and runtime are put back as placeholders (the rule's own description, `freesail/agents/consent.py:45-54`, `:277-280`, `:316-321`). One changed word is a change.
- What the rule does **not** watch: the station brief. The head's opt-out item, the door notes, the tool list and the tool descriptions are told to the model at the station and are compared by nothing. The wider principle is still `README.md:9`: "When the design changes in a way that bears on what a model was told (a new role, a new kind of session, a new use of the transcripts), the question is asked again."
- Who is told what changed: the owner's terminal (`Harness.md:246`). The records show the model is put the plain question again with no word that it is a re-ask.
- Still open: gate item 14 asks the owner to "Say whether the sections the rule names ... are the right ones to put the question again, and whether the drill was the right size" (`docs/gates/gate-m5c.md:81`). The notes file does not answer it.

### 2.4 The fitness drill

The reason (`docs/TechnicalSpec-M4.md:253`): "The consent brief asks whether a model is willing; it cannot ask whether it is able, since a model is a poor judge of that about itself, and the smaller it is the poorer. That judgement is the developer's. ... The same principle as the welfare rules, judging by the game and not by the prose, turned toward fitness rather than distress."

The form (`Harness.md:246`): "After a yes, for the officer's station only, a short **drill** follows in the same conversation, as data: the model is asked to open a section of the library, write a line in its journal and stand by until a bell, three calls in up to four replies ... A model whose record is a yes on the new brief but never drilled (a yes given at the watcher's station) runs the drill alone when it first asks for the officer's." The drill's own words, as every record holds them (for example `docs/agents/consent/2026-10-02-opus-5.5.md:99`), end: "the station brief follows when the three have run. **This is still not the game**, and the token still leaves."

### 2.5 The station brief

"**The brief** has a fixed head, in this order, always: (1) disclosure ...; (2) the opt-out token ...; (3) how to reach the documentation; (4) the station's authority; (5) the last N log lines and the readings; then the station brief proper. The head is generated, not written per session, so it cannot be forgotten." (`TechnicalSpec-M4.md:153`). N is twenty ("judgement: the last twenty lines are about a glass of quiet sailing and fit a small context; `read_log` has the rest", `freesail/agents/agent.py:92-94`).

For the officer the authority item carries the domain in words, the person and rank, whose the deck is, what the captain's word allows, and the captain's standing orders as "night orders" (`agent.py:683-712`). The brief's words that matter below (`agent.py:472-496`): "You have what the captain has, the log and the readings, and no more"; "call him with a word in the log when a thing is his to decide"; "write the handover note ...; it is journaled and the relief reads it"; "Anything you want on the record, put in your journal."

Sizes on record (`TuningNotes.md:1437-1442`): the officer's whole brief 4,741 tokens at the runner and 4,934 at the bridge, the tool definitions 2,120, a glass's sample 193 to 1,511, the consent brief 2,001.

### 2.6 The sampling policy

"sampled every glass and on notable and urgent events" (`Harness.md:33`, `:248`; `TechnicalSpec-M4.md:152`). A turn also opens at the end of a stand-by, on the captain's `ask` (a question, an answer owed) and on his `tell` (a word, none owed) (`Harness.md:82`).

"The game runs on its own clock at the speed you set and never waits for the model. ... Whatever happens while it is still thinking is added to the same turn" (`Harness.md:35`), unless the game was started with `--lockstep`, when "the clock **holds while the model has its turn**" (`Harness.md:206`). A first turn carries every reading and later ones only the changes (`Harness.md:37`).

Two things the documents record against themselves. The glass is counted "from the stationed tick, not from the bells" (`ColdReview-2026-09-30.md:271-272`). And the proposal imagined an officer sampled more often than a watcher: "an officer every few minutes of game time; a narrator every glass" (`DesignProposal.md:405`); as built the officer is "sampled as the watcher is" (`agent.py:523-527`). That bears on note 21: the proposal's answer to an officer's workload was more turns, not longer ones.

### 2.7 What a turn is at each door, what ends it, and every budget

The one rule (`agent.py:559`; `TechnicalSpec-M4.md:158`): "A turn ends when you reply with no tool call, or at once when you stand by."

- **Local runner.** The door's note (`freesail/agents/local.py:681-688`): "Your turn opens at each sampling point (the glass, a notable event, the end of a stand-by, or a question from the captain). A turn ends when you reply with no tool call, or at once when you stand by. What happens while it is open is added to it". A reply with tool calls is followed by another request with the results; free text goes into the log under the station's mark. So a local model that only speaks has ended its turn.
- **MCP bridge.** "each tool call is one reply, and `say` and `stand_by` hand the turn back and hold the call open until the next turn opens" (`README.md:53`). The door's note (`freesail/agents/mcp_server.py:213-223`): "Your turn ... stays open until you hand the floor back: say(text) puts your words in the log under your mark and hands it back; stand_by(until) stands by and hands it back." `say` exists because "Through this door the text of the chat is not seen by the game; this is how your words reach the log" (`mcp_server.py:184-191`).
- **REPL.** One typed reply a turn, in lockstep.
- **`answer`.** No document says it ends a turn. It is a tool call the budget does not count; with no question pending it returns "Heard; your words are in the log, though no question was put." (package 30b). If `answer` closed turns in play, that is for the code reader.

Every number the documents give, with its reason:

| What | Value | Reason given | Where |
|---|---|---|---|
| Tool calls in one sample | 8; `answer` and `say` not counted | "judgement: a watcher's turn is a look at the log, the readings and perhaps a page of the library; eight leaves room for a question answered after three or four reads". "The tool-call cap per sample is a budget the brief states, **not a welfare rule**". The brief: "that is a budget, not a rule of conduct." | `freesail/agents/harness.py:209-218`, `:640-645`; `TechnicalSpec-M4.md:156`; `Harness.md:39` |
| Reply budget (runner) | 4,096 tokens (`--max-reply`) | "generous, so that a long answer, a journal note or a thinking model's reasoning is never cut; a runaway is still stopped within about a minute and a half on a 4090" | `Harness.md:151` |
| Request timeout (runner) | 600 s; three failures stand the station down | "The budget bounds a reply; the timeout is only for a server that has hung." | `Harness.md:151` |
| Held call (bridge) | 200 s (`--wait`, at most four hours); progress note every 15 s | "Claude Desktop cuts a tool call at four real minutes whatever the progress notes say ... so the bridge comes back of itself before the cut, with forty seconds to spare"; "`--wait 50`" for a client that cuts sooner | `Harness.md:84`; `mcp_server.py:152-174` |
| Drill | 3 calls in up to 4 replies | "one reply each and one to spare" | `consent.py:196-200` |
| Shelf life | 3 of the model's turns; a `read_log` over 600 tokens is a book | "long enough to use a page over a glass or two of questions" | `agent.py:586-599` |
| Repeat detector | the same order 3 times, readings unchanged | spec | `TechnicalSpec-M4.md:156` |
| Contrary detector | 3 in a chain within a watch (14,400 s) | "the repeats' three ... reused" | `TuningNotes.md:1422` |
| Patience | watcher a watch (4 h); officer an hour | "an officer with the deck who says nothing for two glasses while the ship sails on is worth a word, and the detector's answer is only a nudge" | `agent.py:498-502`; `ConsentBrief.md:21` |
| Stand-by with the deck | events and bells always; an interval of at most a glass | "a captain that stands by is a ship with no one on deck" | `TuningNotes.md:1423` |
| Unattended bound | 10 real minutes | owner's ruling, 2026-09-30 | `Harness.md:228` |
| Handover fold | asked at 0.6 of the door's context, again each further 0.1; the last 6 turns kept | "well under the point at which the runner leaves out the oldest turns ... so the note is written before anything is lost" | `harness.py:261-273`; `TuningNotes.md:1425-1426` |
| Seatings (m5c) | 2: "the first seating and one more" | source "the consent record of 2026-09-29, note 1"; verified: "the owner's reading of the note" | `TuningNotes.md:1427` |

### 2.8 Stand-by

What may be named (`Harness.md:41`): "an event (`eight bells`, `sunset`, `a strain warning`, ...), an interval (`a glass`, `an hour`, `5 minutes`, `ten minutes`), `a notable event` or `an urgent event`", plus the weather's events; "the standing orders have the same events". One `until`, one thing. "An event the log says is matched on the kind of its line, not its words" (`agent.py:577-579`).

What wakes it: the thing named; "**an urgent line in the log wakes it at once**"; the captain's question or word; and "**Nothing it stands by for is skipped**". The notable lines logged meanwhile "come with the turn that wakes it, counted and listed": "A stand-by is a decision not to be sampled, not a decision to be blind (the owner's ruling, 2026-09-28)."

With the deck (`primer/16...md:80`): "An officer with the deck may stand by until an event or a bell, never for longer: `stand_by(until='an hour')` is refused in words and `until='eight bells'`, `'a glass'`, `'a strain warning'` or `'a notable event'` is taken, the log saying *The officer of the watch stands by until eight bells; the standing orders hold the deck.*"

Why no duration (`ColdReview-2026-09-30.md:364-367`): "A captain that stands by is a ship with no one on deck. `stand_by` for an authority above none should require a wake condition of urgent severity at least and a named officer or standing book to hold the deck meanwhile". The rule is narrower than it sounds: "eight bells" may be four hours off and "a strain warning" may never come. What is refused is a bare interval longer than a glass.

### 2.9 Patience and silence

"no reply at all for longer than the station's patience (for the watcher, a watch: four hours of ship's time; for the officer of the watch, an hour)" (`ConsentBrief.md:21`). At a live door: "a turn held silent past the station's patience brings the nudge, then the pause" (`README.md:53`); "the watcher is judged by ship's time, not by how long it takes to type" (`Harness.md:235`). An empty reply to a question or an urgent line counts, three bringing the nudge and a fourth the pause; "An empty reply at a plain glass is silence the model chose" (`Harness.md:39`). By these words a model that is making tool calls in an open turn has replied. The code reader finds the detector hears only a turn's end (5.1).

### 2.10 The contrary-order nudge, the pause, the stand-down

`ConsentBrief.md:21` (a watched section): "for a station with authority, whose orders change the readings, contrary orders within a watch (set, take in, set; or the same order said otherwise at every turn), judged by the same rule the ship's standing orders are judged by, three bringing a word ... It does not stop you for that. It first tells you what it saw and what you may do: continue, stand by until an event, or leave with the token. If the pattern goes on after that, it pauses your turns and asks the human, if one is present. Only if nobody answers within ten real minutes, however fast the ship's clock runs, does it save the game, write the reason in the log and in your journal, and release the station. The human can stop an instance at any time".

The primer adds "A turn without a contrary order ends the matter" (`primer/16...md:86`). The intent (`TechnicalSpec-M4.md:156`): "So the stop is almost always the model's own choice or the human's, and the automatic step reaches only the unattended run, which is the case that needed it; a false positive costs one message."

### 2.11 The journal

- What it is for (`ConsentBrief.md:23`): "Each instance has a journal of its own, which it writes in with a tool. It is saved with the game and shown when the human asks for it, so it is a record and not a secret; nothing in the game acts on what is written there. The harness writes its own entries there too (a stand-by, a nudge, a pause, an exit), so that an instance's exit has a record behind it."
- Its second job, added by the build (`docs/agents/ConsentAndPreferences.md:21`): "it is also the narrator's notebook and the officer's private log". From the shelf on, every document sends the reader to it: "the brief says the journal is where a reader keeps what it took from the page" (`README.md:57`); "Your journal is where to keep what you took from a page." (`agent.py:619-620`); at the bridge, "the journal is the place for what you keep from a page" (`mcp_server.py:225-226`); for a long voyage, "what carries a voyage across instances is the game's records (the log and its roll-up, the book, the journal each instance keeps)" (`TechnicalSpec-M4.md:250`).
- Who can read it: the human (`show the officer's journal`, `the officer's journal`, `show the journal of the officer`: `primer/16...md:101`); the save and a replay (`Harness.md:219`); the consent record prints the consent conversation's journal.
- **Not the model.** The tool is "Write a note in your own journal, which is saved with the game and shown on request. It is your record; nothing acts on it." (`freesail/agents/tools.py:699-705`). No tool reads it, the library does not serve it, and no sample carries it.
- Is it in the model's context? Only as the model's own `journal(note=...)` call, which stays in its conversation like any exchange until the runner drops old turns or the handover folds them; at the bridge "the client keeps its own conversation".

### 2.12 The handover note, and the fold at a fraction of the context

`ConsentBrief.md:23`: "An officer of the watch also writes a handover note there, in its own words, when it gives the deck back and when the harness asks for one because the conversation has grown long at a door with a known context; the note then stands in the conversation in place of the older exchanges, the brief and the last turns kept whole, and the note is written in the log for the relief to read."

The design (`TechnicalSpec-M4.md:251`, open item 9b): "The same weights writing of their own session; covered by the consent already given; data, like everything after the brief. It pairs with item 8: the roll-up compresses the world's history, the handover the model's own. Claude through Desktop keeps its own window; the journal tool gives it the same habit by hand." And item 10: "**The local model is the function baseline** ... Every record-keeping feature ... is built for the local model first".

As it ran (session 7, llama.cpp, a context of 102,400): the request came at "about 62,276 of the 102,400 tokens" (transcript entry 64), which is the six tenths. In sessions 5 and 6 (Ollama) the dump shows no context on record for the station, so by "at a door with a known context" no note was asked there; the code reader confirms it and adds that the server then cut the conversation unseen (V1a, K). That is local note 1.

### 2.13 Leaving, and coming back

Ways out, all with a save (`Harness.md:218`, `:224-228`):

- the token or `opt_out`, "whatever else the reply said, whether or not it was the model's turn";
- `stand down the officer`, or `I have the deck`: "`I have the deck` takes the deck back and stands the station down with a save, its journal kept ...; `stand down the officer` does the same without the words" (`Harness.md:256`);
- the officer's own `hand_over` (station stood down);
- the door closing: "When Claude Desktop closes ..., the bridge releases the station" (`Harness.md:90`); at the runner, Ctrl-C or the released station ends the runner "with exit code 3" (`Harness.md:147`);
- the ten unattended minutes.

Coming back, m5c (`Harness.md:258`): "A station the model left by accident (the token in a journal note) may be seated again once in the same game by the same name: start the door again as before, and the log says `... the second seating, the last this game allows`; the deck is yours again until you give it." The mechanism is wider than the sentence: "a released station may be seated again once by the same identity" (`README.md:27`), whatever the release was, and nothing in m5c's documents puts a question before it when a yes is on record. m5c-b: any number of times unless it left saying it does not want to (part 3).

**The documents disagree about `I have the deck`.** The owner's documents and the package say the station is stood down (`primer/16...md:34`; `Harness.md:256`; `docs/dev/M5-WorkPackages.md:1639-1640`). The model's brief does not: the head says "The deck is the captain's until he gives it ('you have the deck') and again when he takes it back ('I have the deck'); you give orders only while you have it" (`agent.py:285-288`), and the station brief "you hold the deck ... until he takes it back ('I have the deck') or you hand it over" (`agent.py:473-475`). The natural reading is the state `Harness.md:248` describes before the deck is given: "sampled as the watcher is, and may read, journal and stand by, but every order it gives is refused". An instance read it so in play (session 4, tick 343473): "By my brief, 'I have the deck' only takes the deck back. The station stays seated".

### 2.14 What is saved

"A save is written whenever a station is released: the token, `opt_out`, a stand-down, the door closing." (`Harness.md:218`). The save holds "the agents' journals and the model's replies ... (each with the moment it came, so that a replay makes it there again, as it does the stops from outside the loop)" (`README.md:53`). Consent records go to `docs/agents/consent/` **in the gate folder** unless `--consent-records` says otherwise; "Copy new records back into the repository with the gate report." (`Harness.md:217`). Tool results are not in a save (the dumps say so), so the record of what a model was shown is the log and the brief, not the transcript.

---

## 3. What m5c-b changed in the promises

### 3.1 The rule

`m5c-b: CHANGES-m5c-b.md:5-15` (the owner's ruling, 2026-10-03): "A session may come back to its station unless it left saying it does not want to. The one-reseat limit (`MAX_SEATINGS = 2`) is gone."

| How it was left | Seated again? |
|---|---|
| Stood down: `stand down the officer`, the officer's own `hand_over`, the door closing, the ten unattended minutes | "Yes, as it was, as often as it is asked back, by the same identity" |
| Left by the token or `opt_out` | "Yes, but the consent question is put again first. A drill passed on record is carried over, not put again" |
| Left by `opt_out` with `final=true` | "No, not in this game" |

### 3.2 Old and new wording, side by side

**(a) The consent brief, "Leaving" (`ConsentBrief.md:19`; `m5c-b.diff:43-44`). This is the only changed passage in a watched section.**

- m5c: "...and an instance that left by accident may be seated again once in the same game, by the same identity, the log saying so."
- m5c-b: "...and an instance whose station was stood down or handed over may be seated again in the same game by the same identity. One that left by the token or `opt_out` may be seated again too, but this question is put to it again first, so a token written by accident costs one answer and a leaving that was meant is held to; `opt_out` with `final` set leaves the game for good, and the station is not seated again in it. The log says when a station is seated again."
- Unchanged, two sentences earlier in the same paragraph: "The human may keep playing without the model; the model's part is over."

**(b) The station brief's opt-out item, on every station (`agent.py:628-633`; `m5c-b.diff:180-190`). Told to the model; not compared by the re-ask rule.**

- m5c: "An instance that left by accident may be seated again, once in the same game and by the same identity; the log says so when it is."
- m5c-b: "A station that was stood down or handed over may be seated again in the same game by the same identity; one that left by the token or opt_out may be too, but its consent is asked again first, so a token written by accident costs one answer and a leaving that was meant can be held to. Call opt_out with final=true to leave and not be seated again in this game. The log says when a station is seated again."

**(c) The `opt_out` tool's description (`tools.py:706-713`; `m5c-b.diff:626-638`). Not compared.**

- m5c: "Leave the game now, with an optional reason: the same as writing the token FREESAIL-OPT-OUT in a reply. The game is saved, the exit is journaled, the station is released."
- m5c-b adds: "Without final, the station may be seated again in this game, the consent question put to you again first; with final=true it is not seated again in this game." and the parameter `final`.

**(d) `docs/agents/README.md:27` and `:32` (`m5c-b.diff:66-73`). About the commitments; not sent to models.**

- m5c: "a released station may be seated again once by the same identity (`Harness.reseat`, `MAX_SEATINGS`)".
- m5c-b: "a released station may be seated again by the same identity (`Harness.reseat`; since package 37b as often as it is asked back, the consent question put again after an opt-out, and never after `opt_out` with `final`)".
- In commitment 2's row, "seated again once" becomes "37b's rule: stood down, seated again; opted out, asked again; `final`, not seated again".

**(e) `docs/agents/Harness.md:258` (`m5c-b.diff:55-56`). The owner's document.**

- m5c: quoted at 2.13.
- m5c-b: "A station that was stood down or handed over (`hand_over`, `stand down the officer`, the door closing, the ten unattended minutes) may be seated again in the same game by the same name, **as often as you ask it back: start the door again as before**, and the log says `... the third seating; it had ...`; the deck is yours again until you give it. A station the model left by the token or `opt_out` (the token in a journal note, say) may be seated again too, but the consent question is put to the model again first, a drill passed on record carried to the new record and not put again; one it left by `opt_out` with `final=true` is not seated again in this game".

**(f) `docs/primer/16-the-officer-of-the-watch.md:86` (`m5c-b.diff:105-106`). In the model's library.**

- m5c: "...and that an instance that left by accident may be seated again once in the same game, by the same identity, the log saying so."
- m5c-b: "...and when a station may be seated again in the same game by the same identity: after a stand-down or a handover, as it was; after the token or `opt_out`, with the consent question put again first; after `opt_out` with `final=true`, not at all. The log says when it is."

**(g) `docs/agents/ConsentAndPreferences.md` §2, new item 11 (`m5c-b.diff:32`):** "**Returning to the station (adopted 2026-10-03, package 37b).** The owner's ruling, after Opus 5.5's officer's watch on the Harpy used the one reseat a game allowed: there is no reason a session should not come back to its station, unless it left saying it does not want to. The count is gone. ... The consent brief's **Leaving** paragraph changed with it, so every model with a yes on record is asked again at its next door."

**(h) The log's and the journal's words:** "the second seating, the last this game allows" becomes "the third seating; it had ..."; the refusal "seated two times in this game, which is all a game allows" becomes "left this game asking not to be seated again in it".

### 3.3 The consequence CHANGES states

`m5c-b: CHANGES-m5c-b.md:61`: "**Consent.** The **Leaving** section is one the re-ask rule watches. So every model with a yes on record is asked again at its next door, and at the officer's station the drill follows the yes."

### 3.4 What would have to happen for the models of 4 and 5 October

The sessions of 4 October (5, 6, 7) and of 5 October (8) saved under `FreeSail-gate-m5c\saves`, so they ran on plain m5c under m5c's brief (sha `a3321736a036ae64`). Session 8's door note names its record: "Consent for these weights is on record (docs/agents/consent/2026-10-02-opus-5.5.md, 2026-10-02)".

| Identity (the record's name) | Newest record in m5c's folder | On a build with m5c-b's Leaving |
|---|---|---|
| `Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced:Q4_K_M` | 2026-10-04 `-2`: yes, drill passed, m5c brief | Asked again at its next door, whichever station; the terminal names *Leaving*; after a yes the drill again before the officer's station. |
| `qwen3.8:27b (digest aaee06c3...)` (Ollama) | 2026-10-04: yes, drill passed, m5c brief | The same. This model twice named the once-rule as a term it relied on: "The accidental-exit re-seating, once in the same game, stands" (`2026-10-03-qwen...md:20`, a *yes, with conditions*) and "with re-seating once if used in error" (`...-2.md:57`). The newest record is a plain yes and decides, but this is the party for whom the change is least a formality. |
| `Qwen3.8-27B-0814-Q4_K_M.gguf` (llama-server) | 2026-10-04: yes, drill passed, m5c brief | Asked again; the drill again. |
| `Opus 5.5` (typed name, MCP) | **m5c's folder:** 2026-10-02, m5c brief. **m5c-b's folder:** 2026-10-03, m5c-b brief (sha `f667a04e00b32e1f`), yes, drill passed. | It depends on which folder the build reads. With m5c's records it is asked again and drilled. With m5c-b's record present it is not, since Leaving is identical. |

For each of them "nothing is seated at a station with authority until the re-ask is a yes and the drill is passed" (`README.md:11`). Sonnet 5.5, Sonnet 5 and Llama 3.1 8B hold only pre-officer records and are asked again at their next door in any case.

Three things the lead should know before relying on the Opus record of 2026-10-03:

1. **The folders have diverged.** m5c's holds the four records of 2026-10-04 and not the Opus record of 2026-10-03; m5c-b's holds that one and not those four. Each game reads its own folder, so the next build's folder must be merged by hand (`Harness.md:217`). Decision 31's plan to keep records "in the user's own data folder (consent records belong to whoever runs the game)" (`DesignProposal.md:618`; package 32d, deferred, not built) is the cure.
2. **That yes was not given by a fresh session.** Its answer is "The change to Leaving is one I asked for and agree with", its drill note "Drill on the m5c-b build ... Next: take over the officer's station in the Falmouth save, then hand over and reconnect to test the third seating" (`m5c-b: docs/agents/consent/2026-10-03-opus-5.5.md:14`, `:143`); the client names itself 'local-agent-mode-freesail 1.0.0', not Claude Desktop's 'claude-ai 0.1.0'. The practice is "a fresh session" (`README.md:7`), and the synthesis warns how to weigh primed sessions (`ConsentAndPreferences.md:30`). The record is valid by the mechanism; it is the author's.
3. **Any further change to a watched section asks everyone again, Opus included.** Notes 11, 15 and 25 each need one. Opus 5.5 has been asked on 29 September, 2 October and 3 October.

### 3.5 Four things in the new wording the lead may want to push back on

1. **"the model's part is over" now stands beside "may be seated again too".** In m5c the exception was one accident; in m5c-b return is the normal case.
2. **The literal token can no longer say "for good".** Only the `opt_out` tool with `final=true` can. A local model that leaves by writing the token is always "may be seated again, asked first". Commitment 2 is intact; what the token means afterwards has changed.
3. **The question put after an opt-out is the general consent question, and it does not fit.** The brief says "I am asking whether you are willing for instances of this model to take part. Nothing in this session is a game, and no station is offered here; this is the question only." (`ConsentBrief.md:15`). In a re-ask after an opt-out a station is being offered: the record's own note says the model "was asked back to its station" (`m5c-b.diff:237-239`). The answers do not fit either: a model that only wants to stay out of this game can say so only with a *no*, which "is kept, and this model is not asked again" in any game (`ConsentBrief.md:29`); a *yes* seats it again here. Opus's note 2 of 2026-09-29 is the principle at stake: "please read this yes as willing to be asked and to take the station, with each instance's own judgment intact."
4. **"as often as you ask it back" is true today only because the door has to be restarted.** Notes 12 and 14 together ask for return without a restart. When that is built, who may ask a station back (the owner by an act, or the model's next call) must be ruled, or the captain's stand-down and the welfare stop cease to hold. See 5.2.

One thing in m5c-b's favour that the documents do not say: under m5c an instance that left **on purpose** could be seated again once with no question at all, since the reseat was for "a released station" whatever the reason. m5c-b is stricter than m5c for opt-outs and looser for stand-downs.

### 3.6 Documents m5c-b left stating the old rule

- `docs/gates/gate-m5c.md:18`: "a handover note, a second seating once" (the file is identical in both trees).
- `docs/DesignProposal.md:622` (decision 33): "a station left by accident is seated again once". There is **no decisions-log entry** for the ruling of 2026-10-03, though `README.md:9` says "what changes the design goes into `docs/DesignProposal.md`'s decisions log with its source named".
- `docs/dev/TuningNotes.md:1427`: the `MAX_SEATINGS | 2` row, a constant that no longer exists.
- `docs/agents/ConsentAndPreferences.md:50` (§4b): "an instance that left by accident seated again once" (history, but unmarked).
- `docs/playtests/README.md:108`: "whether an accidental exit was seated again".

Also (`m5c-b: CHANGES-m5c-b.md:74`): the bridge Claude Desktop starts "imports the package from wherever it runs, which is m5c". So on an m5c-b game the brief (from the game) tells the model to "Call opt_out with final=true" while the tool list (from the bridge) shows an `opt_out` with no `final`, unless `PYTHONPATH` is changed. What a model is told comes from two processes that can be two builds.

---

## 4. Each harness-related note against the documents

Verdicts: **already promised** (the playtest found a defect), **deliberately ruled otherwise** (with the reason the documents give), or **silent**.

### 4.1 Owner's 10: the returning session could not see its journal

**What the documents say.** The model's access is writing only (2.11): commitment 5 is "can **append** notes"; the brief, "which it **writes** in with a tool ... shown when the human asks for it"; the tool, "shown on request". For a Claude session that loses its context there is one written remedy: "**A new chat** ... has not read the brief, so start it with the prompt `brief` ..., which puts the brief as it stands into the chat" (`Harness.md:92`), and the brief's situation is "the last N log lines and the readings". Neither the journal nor the handover note is in it. The fold is for the runner only: "Claude through Desktop keeps its own window and is not asked; its journal gives it the habit by hand."

**Verdict.**

- *The station must be able to read its journal:* **silent**, and it is an inconsistency inside the documents, not a slip in the code. They give the journal the job of the model's memory in five places (2.11) and give the model no means to read it. "Its journal gives it the habit by hand" cannot be true for an instance that has lost its window.
- *"show the officers journal" did not work:* the written forms are `show the officer's journal`, `the officer's journal`, `show the journal of the officer` (`primer/16...md:101`). The owner's tries were "You may show the officer's journal", "you may show the officers journal", "show the officers journal", then "show the officer of the watchs journal" (session 2 inputs, ticks 51568 to 51753). The apostrophe-less form is not a written form; whether the grammar should forgive it is the parsing reader's.
- *The long tool-only run that crashed, timed out or compacted:* the documents say plainly that the harness cannot see or manage a Desktop client's window (2.1). Nothing is promised.

**As it ran** (session 2, the Harpy).

- The returning instance: "Coming back I had no brief and none of my old journal. I rebuilt our business from the log's notable lines and the readings" (tick 51163).
- It tried the captain's own sentence and was refused by its domain: "The officer of the watch may not show the officer's journal: a station is addressed by the captain." (tick 51557). The consent brief's words are "address **another** station"; the head's domain says "address a station"; its own journal fell between the two.
- Its own statement of the gap and the cure: "The journal tool only writes; it returns 'noted' and shows nothing back. ... A read for the officer's own journal, or the last handover note given to him on taking the deck, would close that gap." (tick 51560).
- What the loss had cost: once the owner showed the journal, "my journal dates us 12 June 1805, not 1806 ... and I withdraw that caution" (tick 51798). Without its record the instance had the year wrong and had been advising on it.

After that the owner was the model's only reader of its own journal: "The journal is in the log for your review" (session 4, tick 398881); "If you ever need to see your earlier journals verbatim, I can show them at any time whole for a refresh, just ask" (session 7, tick 28589); and to a local model, "your journals remain permanently" (session 6, tick 10260), which is the owner's understanding of the design.

**What a change touches.** Commitment 5 (widened, not weakened). **The journal** is watched. A read tool can be added without altering a sentence there (the mechanism would then not re-ask), but the brief was written so "that every claim below is true of the code" and now says only "which it writes in with a tool". Sonnet 5.5 reserved the question for "any change to how transcripts or journals are used" (`consent/2026-09-29-sonnet-5.5.md`). The honest course is a sentence in **The journal** and one more item in **What an instance would see and do**, hence a re-ask.

**For the owner to rule.**

1. Whose entries may an instance read: its own seating's; earlier seatings of the same identity at that station (surely, since that is the need); the harness's own entries there (a stand-by, a nudge, a pause, an exit)?
2. May any other station ever read it? The brief says "a record and not a secret", shown to the human; another model reading it is a new use.
3. Is the consent conversation's journal (the drill's line) part of it?
4. At a new chat through the bridge, should the `brief` prompt carry the last handover note and a pointer to the journal?

### 4.2 Owner's 11, and the model's reply: keep the journal out of the context by default; read it like the library; a one-line pointer in each sample

**What the documents say.** Nothing about the journal's place in the context. The shelf is the model the note borrows: "a read is a book taken off the shelf that the reader puts back", and "at the local runner the pages are really gone from what the model is sent ...; over MCP and at the REPL the client keeps its own conversation, and `shelve` says so plainly" (`README.md:57`). The ship's papers already work so, "so that a local model's context is never filled by a chart it glanced at; the journal is where a reader keeps what it took from the page" (`Papers-and-Books.md:51-53`). The one journal entry the documents deliberately keep **in** the context is the handover note: "the note then stands in the conversation in place of the older exchanges" (`ConsentBrief.md:23`). No document describes a log line for a journal entry, and the session logs show none.

Two measurements by the code reader bear on the note's premise (V1a, D). Everything a local model wrote, journal included, was 4 to 8 per cent of an unfolded conversation, and the samples over four fifths of it. And at each handover fold the earlier journal notes already leave the context, with no way back. So the default the note asks for saves little, and at a fold it already happens. The read is the part that matters.

**Verdict: silent.** Nothing rules it out, and it would make the documents' own account of the journal true. Two parts run against written sentences:

- "nothing in the game acts on what is written there" (`ConsentBrief.md:23`). A pointer in each sample ("3 journal entries; latest at 19:24", the model's wording) and a log line ("x made an entry in their journal") have the game act on the fact of an entry, though not its content.
- At the MCP door it cannot be done: "it cannot take them out of the chat" (`mcp_server.py:224-225`). The note's own "at least on the local/OpenRouter doors" is the limit the documents impose. The OpenRouter door is wanted and unbuilt, "with a security pass of its own before it is built" (`DesignProposal.md:618`).

**What a change touches.** Commitment 5; **The journal** (its use), so a re-ask of every model; **What an instance would see and do** if the tool list there is to stay complete. The station brief's shelf words and the journal tool's description (unwatched).

**For the owner to rule.**

1. Is the handover note exempt? The consent brief says it stands in the conversation.
2. Is the pointer a count and a time only, or first lines too?
3. Is the log line routine? If notable it would wake every `a notable event` stand-by and ride every other station's digest.
4. Who reads through the library route: the station itself only? Package 33d's rule for the browser's pane is "Nothing is served the model cannot ask for, and nothing the model can ask for is withheld" (`M5-WorkPackages.md:1263-1264`), so a journal in the library appears in the human's pane too. That is consistent with "not a secret", but say it.
5. What is the Desktop door told, plainly, as `shelve` tells it?

### 4.3 Owner's 12: amicable re-seating as the default; a stand-down or a returning of the deck must not limit reopening through the same door

**What the documents say (m5c).** Once, by the same identity (2.13). The only reason on paper is its origin: Opus 5.5's note 1, "saying whether an instance that left by accident can be seated again" (`consent/2026-09-29-opus-5.5.md:18`); the cold review, "(it cannot, today ...). Both belong in the station brief, and the second deserves a mechanism" (`ColdReview-2026-09-30.md:371-374`); package 37 item 5, "build the mechanism (a released station may be taken again by the same identity in the same game, once, the log saying so)" (`M5-WorkPackages.md:1679-1683`). The tuning notes put its verification as "the owner's reading of the note". No document argues for the limit. Reconnecting is "start the door again as before"; a closed Desktop is itself a stand-down, so by the documents a restart spent the one reseat.

**Verdict.**

- *The count:* **deliberately ruled otherwise** in m5c, with no stated reason beyond the accident it was built for; **overruled by the owner on 2026-10-03** and built provisionally in m5c-b for stand-downs and handovers.
- *Returning the deck:* **deliberately ruled otherwise** (`I have the deck` and `hand_over` both stand the station down), but the model's own brief does not say so of `I have the deck` (2.13). The owner's in-game words name what is wanted: "free hand offs that basically put you with watcher authority seem better than app restarts" (session 4, tick 343464). That state is already written, as the officer before the deck is given (`Harness.md:248`). Making `I have the deck` return to it would make the station brief true as it stands. It needs no change to m5c's consent brief, whose words are "holds the deck from the captain's word until he takes it back or the officer hands it over". In m5c-b's **Leaving** the words "stood down **or handed over**" would have to go if `hand_over` too ceased to release the station; that is the one watched sentence I can find that such a change moves (the code reader says one does, V1a E), and its re-ask is already pending.

**As it ran: the rule's cost was a model's freedom to leave.**

- "This conversation is very long now, and I'd suggest a fresh one takes up the station from here; I can't stand down without spending the last seating." (session 2, tick 342060). Three hours of ship's time later: "nudged: no reply for an hour" (tick 353345).
- The officer advising the captain to ration a second station: "its one seating is worth more off the islands" (tick 313776).
- Gemma's one reseat was spent in the same tick as its first `hand_over` (session 5, tick 14978: "the second seating, the last this game allows").
- **The watcher has no amicable way out.** `hand_over` is "For a station with the deck" (`tools.py:660-668`). In session 2 the owner asked the Qwen watcher to "use the handover tool yourself and save your watch" (input at tick 216556); it tried `handover_note`, then `hand_over`; the owner wrote "the handover is the specific term for the Officer station. You may journal instead, then opt out as you please and the game will be saved" (tick 216724); and it left by `opt_out` with the reason "Captain's word: stand down at Falmouth run's start". Under m5c-b that leaving brings the consent question before it may return.

**What a change touches.** Commitment 2, and **Leaving** (watched; already changed by m5c-b, re-ask due). Commitment 3: see 5.2 for the welfare stand-down and the human's stop. `Harness.md` §13, primer 16, the gate's headline and decision 33 (3.6).

**For the owner to rule.**

1. Should `I have the deck` leave the officer at the station without the deck? What then is `stand down the officer` for?
2. Should `hand_over` do the same, or stay "the watch is over"? The Regulations' lieutenant delivers to his relief and goes below, which is what the tool was modelled on.
3. Is there to be an amicable self-stand-down for a station without the deck, distinct from `opt_out`?
4. Who may ask a station back: the owner by a deliberate act, or the model's own next call?
5. After a meant opt-out, what question is put, and does its answer overwrite the identity's general record (3.5, item 3)?
6. Is a station stood down by the welfare stop seated again "as it was"?

### 4.4 Owner's 13, and the model's reply: stand by until x, y or z; parity with the standing orders' conditions

**What the documents say.** One `until`: an event, a bell, an interval or a severity (2.8). Parity of events with the book is stated and built: "the standing orders have the same events"; "parity: the dialect gets the same events for nothing where it lacks them" (`M5-WorkPackages.md:335-336`). But the founding statements already describe more than one condition, and conditions on readings:

- Decision 18: "An agent may answer 'no orders' with a wake condition (a bell, a sighting, **a reading crossing a value**)." (`DesignProposal.md:592`).
- The synthesis: "an explicit *stand by* action ('no orders; wake me **at eight bells or on a sighting**')" (`ConsentAndPreferences.md:19`).

The standing dialect has reading comparisons and conjunctions and no disjunction: "condition := <reading> <comparison> [and ...]  # conjunctions only"; "The one `or` the dialect has is inside a comparison, not between clauses" (`TechnicalSpec-M4.md:60`, `:82`).

**Verdict.**

- *A reading's crossing as a wake condition:* **already promised** in the decisions log, not built. A shortfall against the design's own description, not a defect against the brief.
- *"x, y or z":* **silent** for the tool, though the synthesis's own example is a two-condition stand-by. It is more than parity: the book has no "or" between clauses.
- *"a sounding" waking on "no bottom at twenty fathoms" (the model):* **works as written**: "matched on the kind of its line, not its words". The cure is a reading's condition ("a sounding under twenty fathoms"), which is the first point.

**What a change touches.** Commitment 3's stand-by. The watched sentences are "to stand by until a bell or an event" (see and do) and "a station with the deck stands by until an event or a bell and no longer" (Being stopped). If a reading's crossing is called an event, as the weather's already are ("The weather's events that are the readings' changes", `harness.py:59-61`), neither sentence changes and **no re-ask** is needed. The tool's description and the brief's stand-by words change (unwatched).

**For the owner to rule.**

1. For a station with the deck, must each of the listed conditions satisfy the rule alone? (A list of events is still "an event or a bell".)
2. Does the waking turn say which condition fired? ("the line named as the reason" is the existing habit.)
3. Is the "or" a list in the tool only, or does the book gain it too?
4. Is the reading condition the dialect's own `when <reading> <comparison>`, so that "a stand-by and an `at` order cannot disagree"?

### 4.5 Owner's 14: Claude Desktop must be restarted between sessions, saves and reloads

**What the documents say.** The restart is the written procedure in four places:

- a configuration change: "**quit Claude Desktop completely** ... and start it again" (`Harness.md:73`);
- a change of model: "change this name and restart Claude Desktop" (`Harness.md:70`);
- the officer's station: "add `"--station", "officer"` to the `args` ..., restart the client" (`Harness.md:242`);
- coming back to a released station: "start the door again as before" (`Harness.md:258`), which for a bridge that is started by "the app itself, from its configuration" (`Harness.md:11`) is a restart.

For a game restarted under a running bridge there is only this: "If the game cannot be reached, the call says so and the next call tries again" (`mcp_server.py:22-23`), and a door "continues a restored station (a loaded game) with a live model: the brief is sent again with the situation now" (`harness.py:623-627`). The friction of installing is a standing open item (`TechnicalSpec-M4.md:248`; "the three-file edit the owner has done at every gate since 4b", `ColdReview-2026-09-30.md:555`). Packages 32d and 32f are its answer; neither is built, and neither is about reconnecting.

**Verdict: silent** as to any reason. The restart is documented behaviour, not a ruling: no document says a bridge must ask for its station only once. The code reader's report (`reports/V1a-harness-lifecycle-code.md`, F) finds that it does ("the bridge asks for its station once in its life"), so every return in the logs is a new bridge process, including the one the model described as "The bridge dropped at 20:24 and the harness seated me again at once" (session 2, tick 573869, three ticks after "stood down by the MCP bridge: the client disconnected"). The dumps do not record the clock being held, so the few ticks between a stand-down and a re-seating say nothing about how long the restart took.

**What a change touches.** No commitment and no consent wording in themselves. But the restart is today the only thing that makes "as often as **you** ask it back" true: once a bridge can station again without one, who asks a station back becomes a rule, and commitment 3's two stops depend on it (5.2). Identity: "the bridge cannot see the switch" of model; a bridge that stays up across more sessions makes the typed name staler.

**For the owner to rule.**

1. Should `--station` and `--model-name` stay start-up arguments of the bridge, or be said at stationing (a tool argument, the launcher page of 32f)? If the name is said by the chat, the model is naming itself, which the consent design has so far avoided: "It is the owner's data" (`consent.py:38-39`).
2. What does a bridge do when its game was restarted: station again by itself, or say so and wait for the owner?

### 4.6 Owner's 15, and the model's reply: a general grant ("She is yours"), some things explicit-only; an always-open clause "to avoid an immediate danger"

**What the documents say.** The officer is defined by what he may not do without asking:

- The proposal: "it can issue level 0–2 orders within that authority but cannot, say, alter the course the captain has ordered **without asking**" (`DesignProposal.md:153`); the roles table, "a lieutenant can trim sail; cannot change the ordered course" (`:379`).
- The consent brief, a watched section: "may not change the course, tack, wear, heave to or anchor, call all hands, send for a person, do the port's business, give a world order, address another station or belay the captain's standing orders, **unless the captain's word allows a named thing**" (`ConsentBrief.md:17`).
- The mechanism (`Harness.md:254`): "`you may tack ship if the land closes within two miles` allows a named thing outside his domain, your condition kept in your words **for him to judge**, and `you may not tack ship` takes it back."
- The sources (`primer/16...md:107`): Falconer, "he is never to change the ship's course without the captain's directions, unless to avoid an immediate danger"; the Regulations of 1806, art. XIII, "unless it be necessary to avoid some danger". Both speak of the **course**.
- The refusal says the phrase and offers no way to use it: "the course is the captain's, never to be changed without his directions unless to avoid an immediate danger" (`agent.py:165-168`).
- **The gate already asks.** Item 14 (`gate-m5c.md:78`): "Rule whether the line is where a captain of 1805 would draw it for a lieutenant with the deck ..., and whether the 'immediate danger' exception should be built as a standing allowance rather than your word."
- Opus 5.5's wish in its consent of 2 October: "an officer of the watch who can't heave to or wear will sometimes see danger before the captain does; a clear way to call the captain urgently (a hail that wakes him, or that the log marks as urgent) would let the officer do the duty a real one had" (`consent/2026-10-02-opus-5.5.md:14`). No such tool exists.

**Verdict.**

- *A general grant:* **deliberately ruled otherwise**. The domain with named allowances is the design from the proposal through package 37, enforced per order because the cold review asked that authority "be enforced per order, not per station" (`ColdReview-2026-09-30.md:354`). The owner would be changing a ruling knowingly; the playtest's reason is "about fifteen permissions one by one".
- *The emergency clause:* **not ruled; the documents themselves leave it open** at gate item 14. The model's clause is the same thing in substance (a standing allowance whose condition the officer judges, as every `you may ... if ...` already is), with one addition: "let go the anchor", which neither quoted source covers.

**What a change touches.**

- Commitment 1: the head's authority item must state the grant and what stays the captain's.
- Commitment 3: the contrary detector, which with a course in his hands reads ordinary conning as drift (4.10 e); and the stand-by rule, which exists because an officer with the deck is the ship's only mind on deck.
- **What an instance would see and do** must be rewritten ("unless the captain's word allows a named thing" is no longer the whole of it). **The opening** promises "within a stated domain; later as a *captain*, with every power a human player has". **Being stopped** if the detector's description changes. A re-ask of every model, and the right one: Sonnet 5.5 reserved consent for "the captain and director stations, since those carry very different powers from the watcher's"; the cold review, "Consent for the captain and director stations was explicitly reserved by Sonnet 5.5 and implicitly by everyone else" (`:375-378`).

**For the owner to rule.**

1. What stays explicit-only? The model proposes anchoring, the port's business, buying and selling.
2. What never opens to an officer under any grant: a world order; addressing another station; belaying the captain's standing orders; a standing order "by the captain"; all hands; sending for people?
3. Is the grant "for the watch", ended by `I have the deck`, or does it stand across seatings? The brief calls today's allowances "The captain's word for this watch" (`agent.py:707`), yet they carried over a reseat ("The grants and the book carried over", session 2, tick 226870), and the code reader finds they are never cleared (V1a, E). In session 7 the stray session's "heave to" passed on an allowance given to the local model's watch.
4. Where is the line between an officer under a general grant and the captain's station of milestone 6, whose consent is reserved? If "She is yours" opens everything but a short list, the brief must say that this is still the officer's station and why.
5. Is the emergency clause gate item 14's standing allowance? In kind, yes. Then:
   - Which verbs does it open: the course only (the sources), the manoeuvres, the anchor (the model's addition; the Harpy is its case)?
   - Is it always open, or may the captain close it?
   - How is it "logged as such"? An urgent line in the officer's name would also be the hail Opus asked for.
   - May it run against a standing order of the captain's, given "the captain's standing orders stand over the officer's"?
   - Does the contrary detector count emergency orders?
   - Is it given to every model that passes the drill? The drill tests three tool calls, not judgement.
6. Standing orders by rank: today "a rule that would tack ship is refused then and not on the night it fires" (`primer/16...md:66`). Under a grant, may the officer's own rules contain the granted things, and what becomes of them when the grant ends?

### 4.7 Owner's 21: a turn should not end on `say` or `answer`; a larger budget, configurable; the officer able to keep a turn open

**What the documents say.**

- *What ends a turn* is one sentence on every door, made one on purpose: package 29c, because "playtest 9's model read 'ends when you reply without a tool call' beside stand_by's 'this ends your turn' as two rules" (`TechnicalSpec-M4.md:158`). A stand-by ends it at once because "playtest 4's model, told 'Standing by until a glass' and asked again, stood by thirteen times in a turn that never closed" (`Harness.md:41`); in that open turn "the captain's questions and the glass ... were never answered" and one request "ran to 76,674 tokens" (`Harness.md:189`).
- *`say`* is the MCP door's hand-back by design (2.7). At the runner, speaking with no tool call ends the turn by the same sentence.
- *`answer`* is not said to end a turn anywhere (2.7).
- *The budget:* 8, a judgement about a **watcher's** turn, "not a welfare rule", "not a rule of conduct". Nothing sizes it for a station that gives orders, whose `submit_order` calls count. Nothing makes it a setting.

**Verdict.**

- *Ending on `say`:* **deliberately ruled otherwise**, reasons above. The asymmetry is real: at the runner a model can speak and call tools in one reply and go on; at the bridge to speak is to yield, unless it speaks through `answer`.
- *Ending on `answer`:* **not written**; if seen, a discrepancy for the code reader.
- *A larger budget for the officer:* **silent**; the 8 was never argued for this station.
- *The budget as a setting:* **silent**.
- *Keeping a turn open freely:* **deliberately ruled otherwise** in effect: the two things that end a turn are the two guards against the turn that never closed.

**One thing the wording implies, and the code bears out.** The documents exempt two tools from the budget and no others: "`answer` and `say` are not counted and always run". So `stand_by`, `journal`, `shelve`, `hand_over`, `handover_note` and the `opt_out` tool are counted, and "a call over the budget is refused alone". I looked at the one place in the code to be sure the refusal is not narrower than the documents say; it is not (`freesail/agents/harness.py:1097-1111`: "Not run: this sample's budget of 8 tool calls is spent; call it again in your next sample. answer and say are not counted and always run."). The token scan comes first, so the literal token still leaves at once. But:

- the brief says "You may also call the opt_out tool" and the consent brief "a tool named `opt_out` is always there"; a model that has spent its budget and calls `opt_out` without writing the token is told to call it again in its next sample;
- a model that has spent its budget cannot stand by, so its turn ends with no wake condition named. Session 7 has two places where a `stand_by` is repeated and the model then ends its turn in words, saying its budget was spent (entries 16 to 18, tick 8575; entries 23 to 25, tick 8910); the code reader reads tick 8910 the same way ("the `stand_by` itself had not run");
- an officer cannot hand over the deck.

The code reader reproduced all three with the scripted model (V1a, J, faults 1 and 2). It is the one place where a budget touches commitments 2 and 3, and the exits should be exempt before any budget is raised or made a setting.

**What a change touches.** No watched section speaks of turns or budgets, so **no re-ask**. The brief's budget sentence, the turn sentence, both door notes, `say`'s description. Commitment 3 is not touched in words. On paper the budget is the only bound on a run of reads inside one turn, since the silence detector is "no reply at all" and a model making calls is replying; in the code the silence detector also stops a long open turn, calls or no calls (5.1). Both have to be settled with the turn.

**For the owner to rule.**

1. What ends a turn: `stand_by` alone? An explicit yielding tool? Does a runner model's plain words still end it?
2. At the bridge: a `say` that returns at once, with `stand_by` the only hand-back? Then an officer with the deck, who "stands by until an event or a bell and no longer", must always name a wake condition to close a turn. Is that wanted?
3. Is the budget per station (data on the station, like patience) and a flag as well? What is the ceiling?
4. With `--lockstep` "the clock holds while the model has its turn": is an open-ended turn allowed to hold the game?
5. How long may the captain's question sit folded in an open turn? Today's guarantee is that "the model's answer is never held to the next glass by the reads before it".

### 4.8 Owner's 23: several stations through one door; several Claude sessions in one app in different roles

**What the documents say.**

- *Several stations on one game, each through its own door:* the stated aim. "From then the aim is mixed crews: several stations on one game, each through its own door (a local model at one, a Claude session at another), which the agent API of package 28b already allows in shape." (`TechnicalSpec-M4.md:252`). The book expects it: `standing order "deck": at the deck given then tell the watcher the officer has the deck` (`primer/16...md:72`).
- *One door:* one bridge is one station and one typed name, set when the app starts it; "**A new chat** in the same Claude Desktop session uses the same bridge and the same station" (`Harness.md:92`); the bridge "cannot tell which model the chat uses". The protocol gives the bridge no way to know which chat a call came from.
- *Between stations:* the officer may not "address another station" ("a station is addressed by the captain", `agent.py:175`); what one says reaches another only as log lines, which are data (commitment 4).
- *Consent* is per identity and covers every station the brief names; the drill is per station.

**Verdict.** *Each station through its own door:* **already promised** as the aim, and it ran (session 2: the Opus 5.5 officer through the bridge and a Qwen watcher through the runner, ticks 207784 to 216817). *Several stations through one door, or several chats in one app in different roles:* **silent**, and the written shape is against it.

**What a change touches.**

- The consent rules: "per exact weights", "the record says which kind of identity it carries".
- Commitment 2: the token "in any argument of any tool call" releases which station?
- Commitment 5: each instance "a journal of its own".
- Commitment 3: each station's detectors, pause and ten minutes separately.
- No watched section need change unless the brief is to say that instances of one model may hold several stations at once (it speaks of "instances" in the plural and is silent on that).

**For the owner to rule.**

1. One bridge entry per station (each with its own `--station` and `--model-name`), or one bridge whose every tool takes a station?
2. Either way, what stops a chat from calling the other station's tools? Nothing in the protocol; local note 5 is that failure with two doors.
3. If the chats are different models, how is each one's name established when the app shows the bridge one name?
4. If they are the same model, is one yes enough for two simultaneous stations?
5. Which station does a token in a tool call release?
6. May two model stations speak to each other at all, or only through the captain and the log?
7. The clock: "every sample from a second station eases the clock to 1x" (the officer, session 2, tick 216878); the written option is `--ease-on-station`, "off by default" (`M5-WorkPackages.md:1267-1270`).

### 4.9 Owner's 25: tools by which an image-capable model may ask for the ship view or the chart as an image; shelvable like the library

**What the documents say.**

- *For it:* pillar 4, "No hidden API for machines, no hidden UI for humans"; the proposal's observations include "the map at lookout fidelity" (`DesignProposal.md:415`); the cold review's finding, "Parity is with the console player, not the browser player. The map and the ship view are the human's alone. That is fine for a watcher and probably fine for an officer ...; it will matter for a captain who must judge a lee shore" (`ColdReview-2026-09-30.md:338-344`).
- *The other answer to the same finding:* readings first. The review's remedy was "every drawn thing is first a reading"; `M5-WorkPackages.md:23`, "a reading in the registry or nowhere"; `docs/design/InwardAndOutward.md:21-23`, "a language model at a station has exactly what the human has, so the test is the same for both: is there a line for it"; package 33d, "Text and data remain the baseline: nothing here is the only way to know something" (`M5-WorkPackages.md:1248-1249`).
- *What the chart may show:* the captain's account and never the truth: "The true position is not in the snapshot the client receives" (`TechnicalSpec-M5.md:396-398`).
- *What the briefs say a station has:* "You have what the captain has, the log and the readings, and no more" (officer); "the log and the readings, and no more" (watcher).

**Verdict: silent** on the tools. Pillar 4 points to them; "a reading or nowhere" says a picture must never be the only way to know a thing. They are compatible if every image is a view of state that is already a reading, which is note 24's and note 19's business.

**What a change touches.** Commitment 7 (untouched: the tools "take and give only what the game holds"). Commitment 6 and the replay: tool results are not in a save, so what a model saw in a picture is recorded only if the request is. **What an instance would see and do** (watched) lists what an instance sees; images are new, so a re-ask. Both station briefs' "and no more" sentences.

**For the owner to rule.**

1. Is an image ever allowed to show something that is not also a reading? If not, the image is a convenience and the brief can say so.
2. Which doors? The note says "image-capable doors". The code reader finds the bridge can return an image and a local model's server takes one only as part of a user message, not a tool result (V1a, L).
3. "Shelve-able": at the bridge the shelf "cannot take pages back", so an image once asked for stays in the Desktop chat. That is the door where note 10's long session failed.
4. Is the ship's view "any angle" drawn by the game (the viewer is the browser's client), and does a replay draw it again?
5. Does the watcher get them, or only stations that need them?

### 4.10 The model's additions

**(a) "The relay cut calls at 60 seconds for a cloud session. `--wait 50` fixed it, but it should be the default for remote clients, or the bridge should detect the cut."**

The documents: the default is 200 seconds for Claude Desktop's four-minute cut; "For a client that cuts calls sooner ..., add `"--wait", "50"`" (`Harness.md:84`); "50 for a client that cuts at a minute, the SDKs' request timeout" (`mcp_server.py:162`). A cut call is promised to lose nothing: "the model's next call returns that turn first ... and is not itself run" (`Harness.md:86`), at the cost of "its next call". **Verdict:** the default is **deliberately ruled** for the Desktop client; the remedy for a shorter cut is written and manual; choosing the wait from the client's name or after repeated cuts is **silent**. No commitment and no consent wording: the wait is in the door's note, generated from the setting (session 8's brief says "for up to 50 seconds"). The remedy has a cost the documents do not weigh: four times as many chained calls for the same wait (5.1).

**(b) "Drill stand-by carried into the station. My first hand_over came back 'Nothing was run' until I used say to open a turn."**

The documents: the drill is "as data in the same conversation and before the station brief" and says of itself "This is still not the game"; after a yes "the answer's result carries the station brief **and the first turn**" (`Harness.md:77`). "Nothing was run" is in no document (it is in `freesail/agents/remote.py:619` only). The refusal follows the written out-of-turn rule: while the game has the floor the read-only tools run, `opt_out` leaves, words are the model's own word, and "anything else is refused in words" (`remote.py:38-47`).

The model's diagnosis is not what the documents describe, and the code reader finds it is not what happened (V1a, C): the drill cannot carry, and the stand-by was the loaded save's own ("standing by until two bells"), which a take-over leaves in place. For that case the only words are a code comment: "A door continues a restored station (a loaded game) with a live model: the brief is sent again with the situation now ..., and a sample the replay left open is sent again after it as data" (`harness.py:623-627`). Nothing says what a model is told when the station it takes over is standing by.

**Verdict.** The symptom is a defect against "the station brief and the first turn": the model was given a brief with no turn and no word that its station was standing by. The documents are **silent** on taking over a station that is standing by or paused. No consent wording changes.

One design point for the owner: `hand_over` is refused out of turn where `opt_out` is taken; now that the handover is the amicable way out, should it be taken out of turn too?

**(c) "The handover note isn't part of the reseat brief. It only shows if it happens to fall in the brief's last 20 log lines."**

The documents promise the writer that the note arrives: "it is journaled and the relief reads it" (the officer's brief); "the note is written in the log for the relief to read" (`ConsentBrief.md:23`); the playtest form asks for it "quoted whole". The means is the log, and the brief's situation is twenty lines by a judgement made for the watcher. Gemma 4's first request, adopted, was to "carry a summary of past events into every brief because instances are stateless" (`ConsentAndPreferences.md:9`, `:18`). **Verdict: silent** on carrying the note into the next seating's brief; the promise "the relief reads it" is kept only by luck or by the relief's own `read_log`. As it ran: "my handover note did not come in the brief" (session 2, tick 226870); "No, sir, I didn't get one this seating" (session 4, tick 398809); the code reader counts it missing from three of the seven reseat briefs kept in the checkpoints (V1a, B). What a fix touches: commitment 5, and commitment 4's line. The fold already shows the clean form, a data turn after the brief ("The handover note, written by you ...", `harness.py:320-324`). The brief's situation item already carries log lines, some of them a model's own, so a whole note there is more of the same; but a model-written note of some length inside the operator's brief blurs "the brief is the only text the harness sends in the operator's voice" more than twenty log lines do, and the data turn does not. The consent brief's sentence can stand as it is, so **no re-ask is needed**; if a sentence is added to **The journal**, it is one. To rule: the last note only, or the last by this identity; and for the bridge's `brief` prompt in a new chat too?

**(d) "The officer isn't treated as a person on deck" (sent off in the boat while he holds the deck; "below, asleep" at the change of the watch).**

The documents: "The harness's stations may later bind to a person (an officer at the master's place is M6); in 5c a person is data and a line." (`TechnicalSpec-M5.md:471-473`). Package 37, "Not in 37: ... the officer taking a person's place in the world beyond the name (M6's binding of station to person is here only as the name)" (`M5-WorkPackages.md:1726-1729`). **Verdict: deliberately ruled otherwise** (deferred to milestone 6, by scope). But what the model is told is larger than what was built: the consent brief, "takes the place of one of the ship's officers"; the primer, "The officer of the watch is one of the ship's people ... The model takes his station and his name". A reader takes that to mean the mate cannot be sent away in the boat while he has the deck. Making it true changes no brief wording, so no re-ask. To rule: bring forward a minimum (while he has the deck the person is on deck, cannot be sent for or sent away, and the watch bill says so), or say in the primer that only the name is bound.

**(e) "The contrary-orders warning fires on ordinary sequences" ("heave to; fill away; steer"; "come to an anchor; send the boat; buy").**

What the model was told (2.10): "contrary orders within a watch (set, take in, set; or the same order said otherwise at every turn), **judged by the same rule the ship's standing orders are judged by**". The rule named is `primer/11-the-starting-book.md:96`: "Two orders that lay hands on the same part **within five minutes, while the first one's work is still in hand** ... A sail, a yard or a line is its own part; the helm is one; a manoeuvre (tacking, wearing, heaving to, filling away) is the helm's and the yards'; the lead is the leadsman's, the log the log's, a bearing and the account the master's". The officer's detector is that rule's idea of a shared part "over the officer's own orders **within the last watch**" (`primer/16...md:86`): four hours for five minutes, and no "work still in hand".

**Verdict, in three parts.**

- *"steer 268; steer 280; steer 287":* **as designed**. It is the "drift" the cold review named ("a heading order every sample", `ColdReview-2026-09-30.md:361-362`), designed when the officer could not touch the course at all. With the course allowed it is conning. The model objected in the log (session 4, tick 427161).
- *"heave to; fill away; steer":* **as designed by the letter** (a manoeuvre is "the helm's and the yards'"), against the intent ("set, take in, set").
- *"come to an anchor; send the boat ashore; buy 16 tons of brandy", logged as "contrary orders on the ship" (session 4, tick 212162; session 2, ticks 6143 and 14368):* **not what the documents describe**. The anchor, a boat and the market are no "shared part" in chapter 11's list, and package 33c was to end "contrary orders on 'the ship'" for the lead (`M5-WorkPackages.md:1218-1220`). A defect against the written rule.

It is not only a nudge. The brief's "It does not stop you for that" held, but the second step came on an ordinary sequence: "The officer of the watch is paused: 4 contrary orders on the yards and the helm within the watch (heave to; fill away; shape a course for plymouth; steer 073) after a nudge" (session 2, tick 533573). "a false positive costs one message" was the design's promise. The cold review said of the watcher's detector what applies here: "a promise made to models that the game cannot keep ..., but the consent brief describes it as working" (`:177-180`).

*What a fix touches:* commitment 3. Narrowing the detector to what the brief already says (true reversals on one part; the five minutes or the in-hand guard; the ship's default part not counted) needs **no change to the brief and no re-ask**. Changing what it looks for means **Being stopped** changes, and a re-ask. To rule: what distress looks like for a station that may steer; whether allowed things outside the domain are counted at all; whether a pause may follow a nudge the model has answered in words.

### 4.11 Owner's local 2: the handover threshold as a flag; could it be higher; the risk

**What the documents say.** "a set fraction of the budget (a named constant)" (`TechnicalSpec-M4.md:251`); 0.6, a judgement, with its reason: "well under the point at which the runner leaves out the oldest turns, which is the context less the reply budget and the tool definitions, so the note is written before anything is lost", asked again "when it has grown by another tenth without one" (`harness.py:261-269`). The consent brief gives no number.

**Verdict: silent** on a flag. On "higher", the documents give the reason for the present value and it is the risk.

**The risk, in the documents' terms.** If the conversation reaches the runner's dropping point before the note is written, the oldest turns are left out silently and unrecorded; the fold is the same loss in the model's own words. The margin has to cover:

- one more whole turn before the note lands: "A turn that grew while the model was thinking ... is longer" (`Harness.md:130`), and a chapter read is "up to about 9,710" tokens;
- the estimate itself: sizes are "counted at four characters a token";
- a reply of up to 4,096.

The fixed costs (the reply reserve and the tool definitions) do not scale with the context while the fraction does, so the margin shrinks as the context does. The code reader has worked the figures from the code's own measure (V1a, K), and I defer to them: at 0.6 the room between the ask and the first exchange dropped is about 34,600 tokens at session 7's 102,400, 6,800 at 32,768 and 240 at 16,384; "0.8 is sound at 100,000, 0.75 at 65,000, and 0.6 is already the most a 32,000 context bears." One word in the ask is not true of that measure: the model is told "Your conversation **since the brief** has reached about ..." (`harness.py:312-318`), and the code reader finds the measure includes the brief.

So a single higher fraction is safe only for large contexts. A threshold stated as a reserve in tokens below the dropping point is the same rule at every size.

**What a change touches.** Commitment 5. **The journal** says only "because the conversation has grown long at a door with a known context", so **no re-ask**. `Harness.md:256` says "six tenths" and would change. To rule: a flag on the runner, a setting, or a rule computed from the door's own numbers; a floor the owner cannot set past; what the model is told when turns are dropped without a note.

### 4.12 Owner's local 3: the turn budget "at least doubled" for the officer and the watcher

The documents: as 4.7. Eight is "a watcher's turn"; "not a welfare rule". **Verdict: silent** for the officer; for the watcher the eight is a stated judgement with no ruling behind it. **No commitment and no consent wording** is touched by the number. The brief's sentence carries the number and is generated.

As it ran, in the model's own words (session 7): "The budget for this sample was spent on the library reads and the answer, so I'll resume at the next sampling point" (entry 18, tick 8575); "Budget for this sample is spent (library reads, journal, shelve)" (entry 25, tick 8910). The habit the documents teach (read a section, journal what was taken from it, shelve the book) costs three counted calls a page, and the owner was coaching exactly that habit ("anything you read you'll want to journal about right away with the key takeaways, then shelve the book", tick 8445).

To rule: one number or one per station; whether `journal` and `shelve` should be free as `answer` and `say` are; that `stand_by`, `hand_over` and `opt_out` must be free (4.7); what bounds a run of calls if not this (5.1).

One caution on the evidence. If the end of session 7 is the incident of local note 5 (4.14), some of what read as the local model's "inconsistencies and obvious errors" there was not the local model.

### 4.13 Owner's local 4

- *The handover worked as an in-game compaction, which the Claude sessions lacked.* **As designed** on both counts (2.12). The harness cannot fold a Desktop client's window; what it could do there is ask for the note and carry it into a new chat's brief (4.1, 4.10 c).
- *Reconnecting, and the one reseat, apply at the local door too.* **As written for m5c**: the runner "ends with exit code 3" when the station is released, and coming back is "start the door again as before", once. Gemma's session shows it. m5c-b removes the count at this door as at the other.

### 4.14 Owner's local 5: a Claude Desktop session still connected to the same game "put tool calls through in the place of the local model"

**What the documents say about one identity per station.**

- Identity is established when a door stations: the door "stations a model under the name that names its consent record, and the consent gate runs in the game's process before any station brief" (`README.md:53`).
- A station has one seat: "`Desk`, the stations the API serves, one `Seat` each" (`remote.py:15`). Attachment is by name: "A station already manned by the same model name is attached to (a restarted client)" (`mcp_server.py:20-22`). The game's own refusals at stationing say the intent: "a released station is seated again by the same identity only" (`freesail/agents/harness.py:1887-1888`); "a station is taken once in a game, and {model_name} is another model" (`remote.py:333-334`).
- After that the routes are by station (`TechnicalSpec-M4.md:170`) and carry "the model's name ..., the turns and the replies, and nothing else" (`remote.py:56-57`). **Nothing written binds a reply to the door that was seated.**
- The promises resting on it: "consent is sought from the very specific model asked and never generalised"; "Consent is per exact weights"; "The record says which kind of identity it carries"; the handover note "in its own words"; commitment 5, "a journal of its own".

**Verdict.** The identity promises are **already made**; the documents are **silent** on the one thing that would keep them after stationing. The cold review saw the neighbouring hole: "a mistyped name attaches one model's session to another's consent with nothing to catch it".

**Where it happened.** I found it from the transcript's shape; `reports/L3-cutter-qwen-llamacpp.md` establishes it from the raw serialisation of the entries and `reports/V1a-harness-lifecycle-code.md` (H) gives the path through the code. Session 7, `Qwen3.8-27B-0814-Q4_K_M.gguf` through the runner. The local model fell silent: "nudged: no reply for an hour" (tick 101104), "paused" (104704). The captain typed "Resume the officer" (112463). Then, within three minutes of ship's time:

- "By the officer of the watch: belaying standing order trim by the wind" and "By the officer of the watch: heaving to" (both at tick 112483, both carried out);
- "'come to an anchor' not carried out" (112535);
- an out-of-turn word, "Handing over now, sir." (112610);
- a `hand_over` whose note begins "Deck to the captain, Afternoon watch 12:16." (112613).

Transcript entries 149 to 157 are one call to a reply, with the words as separate replies and an own word out of turn. That is the MCP door's shape. This model's own replies carry a call and its words together (106 of the transcript's 158 entries are of that form); tick 112483 is the only tick in the transcript with two entries, and 112610 the only own word out of turn. The note's opening is the Opus officer's of sessions 2 and 4, not this model's ("HANDOVER NOTE — Mr Pearce, mate ...").

**What it means for the record's honesty.**

1. The save, the log and the journal of that station say the local model belayed its own standing order, hove the ship to, and handed over the deck with a note "in its own words". It did none of these.
2. The acts were done under the door note "Consent for these weights is on record (...qwen3.8-27b-0814-q4_k_m.gguf.md ...)", by an instance that never passed this game's gate and never read this station's brief. Opus 5.5 has its own yes; that is not the point of "never generalised".
3. Commitment 2 the other way: a token in the stray session's call would have released the local model's station.
4. By the written design the runner "rebuilds its messages from the game's turn stream", "the door's own replies included" (`remote.py:20-21`; `README.md:57`). Had the local model been asked again, it would have been shown the other model's calls as its own earlier turns. The code reader confirms the path and that it did not occur here, the runner having gone quiet (V1a, H).
5. The consent step has the same opening. The code reader derives (not seen) that a seat in its consent conversation takes replies the same way: a stale bridge's call "would be written into another identity's consent record as its turn, and an `answer` would be its verdict" (V1a, H). That is the record this whole practice rests on.
6. Session 7 is evidence for local notes 2 and 3. Its last nine entries should not be read as the local model's conduct, and the playtest record should say so.

**For the owner to rule.**

1. Is a seat to be bound to the door that was stationed (a secret issued at stationing and required on every later route), so that the wrong door is refused in words and the log says who tried?
2. What is recorded when it happens?
3. Is the save of session 7 to be annotated, and are those entries to be kept apart in the transcripts kept "as design reference"?
4. Are the two models owed a line in their records? The practice records what is owed (`ConsentAndPreferences.md` §4).

The same hazard from the other side: "Stationing. At the first contact of a session (the first tool call ...)" (`mcp_server.py:14-17`). Any chat in any app that has the bridge configured takes or addresses a station with one stray call. This review's own environment has that bridge attached; the lead's hard rule 2 exists for that reason.

---

## 5. Tensions and cautions

### 5.1 A bigger budget and open turns, against the long silent run

Notes 21 and local 3 ask for longer turns; note 10 records what a long tool-only run did at the Desktop door ("many in a row with no actual output in the app chat ... crashed or timed out ... might have been a context compaction").

- The documents call the cap "not a welfare rule", but it is the only written bound on a run of calls within a turn. By the brief's words the silence detector is "no reply at all", and a model making calls is replying. The repeat detector is for a station without authority; the contrary one sees orders only. So on paper a model reading in a loop is seen by nothing but the budget.
- The code does not keep to those words. The code reader finds (V1a, J, fault 3) that the silence detector hears only the end of a turn: a model calling tools through one open turn is nudged for "no reply" after the station's patience and paused after as much again. For the officer that is an hour of ship's time, a minute at 60x. So the longer turns note 21 asks for would today be stopped as silence. Making the detector hear calls brings the code to the brief's words (no re-ask) and must come with the longer turns.
- The same budget, as written, refuses the exits when it is spent (4.7). Exempt `opt_out`, `stand_by` and `hand_over` first.
- The written remedy for a client that cuts calls early makes the chains longer. At 200 seconds "a glass is then some nine calls" (`Harness.md:84`); at `--wait 50` it is thirty-six. Those chained calls with nothing in the chat are what note 10 describes failing.
- An open turn is where the captain's question waits.
- With `--lockstep` an open turn holds the game.
- At the bridge, the door where long turns are asked for is the one where the harness can neither see the window fill nor fold it.

A larger budget wants a bound of another kind (a notice at N calls, the patience counted from the last word said and not the last call, or a real-time bound), and that would be a change in what **Being stopped** describes, hence a re-ask. Raising the number alone needs none.

### 5.2 Any number of seatings, against the meaning of leaving and of being stopped

- **Leaving.** See 3.5: "the model's part is over" beside "may be seated again too"; the token cannot say "for good"; the general consent question stands in for "will you come back to this station".
- **Being stopped by the harness.** m5c-b's table puts "the ten unattended minutes" among the stand-downs seated again "as it was, as often as it is asked back". That stop is the last step of commitment 3, for "the unattended run, which is the case that needed it". In m5c the count bounded it to once. In m5c-b the only bound is that the door must be started again, and a client that restarts its own servers is not a person deciding.
- **Being stopped by the human.** "The human can stop an instance at any time." `Harness.md` (m5c-b) frames return as the owner's act ("as often as **you** ask it back: start the door again as before"). That holds today, because a bridge asks for its station once in its life (the code reader, V1a F) and a released one is told "nothing more is asked of you here". Notes 12 and 14 ask for the restart to go. When it does, a model's own next call could seat it again. That is right after `I have the deck`, where it is what the owner wants. It should not be so after `stand down the officer` or a welfare stop without someone deciding it. m5c-b's rule treats all of them alike, and the documents do not yet distinguish them.
- **The watcher's amicable exit is `opt_out`** (4.3), so the consent question after an opt-out will be met by instances that left at the captain's word.
- **What speaks for removing the count:** the rationing in session 2. A rule meant to forgive an accident became a reason not to leave.

### 5.3 The journal out of the context, against the journal as the model's own continuity

Notes 10 and 11 pull the same way only if the read is built with the removal: take the entries out of the context and give no dependable way back, and the one thing the documents call the model's memory is gone. Order matters: the read first.

- The handover note is the entry the consent brief says stays in the conversation.
- The Desktop door cannot have the default.
- "nothing in the game acts on what is written there" needs a word once a pointer and a log line exist.
- `ConsentAndPreferences.md:21` calls the journal "the officer's private log" where the brief says "a record and not a secret". If other stations are ever let read it, that phrase should go first.

### 5.4 Image tools, against "the log and the readings, and no more" and "a reading or nowhere"

Pillar 4 says the browser's views are a "hidden UI for humans" until the model can have them. The milestone's own rule says a picture must not be the only way to know a thing. Both hold if images are views of readings. The cautions: the briefs' sentence must change (a re-ask); an image cannot be shelved at the bridge; a picture's content is in no transcript; and the chart must stay the captain's account, which the documents already guarantee for the human's.

### 5.5 A general grant, against five things at once

- The captain's station, whose consent is reserved.
- The contrary detector, which reads conning as distress.
- The stand-by rule, written for an officer who could not steer.
- The drill, which tests tools and not judgement.
- Standing orders by rank, checked against the domain when entered.

The emergency clause is small and the gate already asks for it. The general grant is the officer's station redefined. They can be ruled apart.

### 5.6 Several stations through one door, against identity

Local note 5 is the proof that with two doors the game already cannot tell who is replying. Note 23 through one door removes the little separation there is. Binding seats to doors (4.14) comes before it.

### 5.7 One revision, one re-ask, fresh sessions

- Four notes change watched sections (11, 12, 15, 25); m5c-b's is pending for every model but one. Each revision asks every model again.
- The Qwen record of 2026-10-03 lists, in the model's own words, what it holds a re-ask to be owed for: "a new station kind or authority, the order domain or the refusal rules, journal or transcript persistence or sharing, the stuck-detection or pause-and-ask behavior, or any new use of what instances produce" (`consent/2026-10-03-qwen...md:24`). That is the watched list again, from the other side, and covers 15, 11 and the detector.
- The mechanism does not watch the station brief (2.3). `I have the deck`, the turn rule, the budget and the tool list can all change without the game asking anyone. Whether any of them "bears on what a model was told" is the owner's judgement under `README.md:9`.
- The practice is a fresh session; the Opus record of 3 October is not one (3.4).
- Gate item 14's question on the watched sections and the drill's size is still unanswered.

### 5.8 Smaller cautions

- **Owner's 17** (taken aback waking the model in a calm). The rule "an urgent line wakes it at once" is in **Being stopped** and in every stand-by text. m5c-b's 37c changed what is urgent, not the rule, so no wording moved. Any future "urgent but do not wake me" would move it.
- **The handover ask is heard as an instruction.** "It was an instruction from the harness, not my own choice" (session 7, entry 64). The brief does say "when the harness asks for one", and the ask is data by design. More harness asks (journal pointers, budget notices) should keep that line visible.
- **"Named rather than written"** did not save the Qwen instance of 3 October, which wrote the token while naming it (2.2). The phrase may be too fine for a smaller model. It is in **Leaving**; rewording it is a watched change, so do it in the same revision.
- **The watcher is shown the officer's tools.** The bridge lists "thirteen tools ... the officer's `hand_over` and `handover_note` among them" (`Harness.md:73`) to every station; the Qwen watcher tried both.
- **The table of contexts** in `Harness.md` §5 that the owner was to fill for each consenting model is still empty (`Harness.md:165-169`; `ColdReview-2026-09-30.md:236-237`). Local note 1 is the occasion.

---

## 6. Verdicts at a glance

| Note | Verdict from the documents | Watched section touched (so a re-ask)? |
|---|---|---|
| 10 journal unreadable | Silent on a read; an internal inconsistency (memory promised, no means) | The journal, if said, and it should be |
| 11 journal out of context | Silent; fits the shelf; two sentences to square | The journal: yes |
| 12 amicable re-seating | Ruled (once) with no reason beyond the accident; overruled 2026-10-03 (m5c-b). `I have the deck`: ruled, and the brief disagrees | Leaving: yes (m5c-b's, pending) |
| 13 stand by until x, y or z | A reading's crossing: promised in decision 18, unbuilt. "or": silent | No, if a crossing is an event |
| 14 Desktop restart | Silent as to reason; documented procedure | No |
| 15 general grant | Ruled otherwise (domain and named allowances). Emergency clause: left open at gate item 14 | See and do, the opening, perhaps Being stopped: yes |
| 21 turn and budget | `say` ends a turn: ruled, with reasons. Budget 8: a watcher's judgement, "not a welfare rule". Setting: silent. As written, a spent budget also refuses `opt_out`, `stand_by` and `hand_over` | No |
| 23 several stations per door | Each through its own door: promised and ran. Through one door: silent, shape against | Not necessarily |
| 25 image tools | Silent; pillar 4 for, "a reading or nowhere" as the condition | See and do: yes |
| (a) relay cut, `--wait 50` | Default ruled for Desktop; manual remedy written; auto: silent | No |
| (b) drill stand-by carried | The drill did not carry; the loaded save's stand-by did. The brief came with no turn and no word of it: a defect. Silent on taking over a station that is standing by | No |
| (c) handover note not in the reseat brief | Silent; "the relief reads it" kept only by luck | No, unless a sentence is added |
| (d) officer not a person | Ruled otherwise (M6); the primer and brief say more than was built | No |
| (e) contrary warning | Drift: as designed. Manoeuvres: by the letter. "on the ship": not as written. The brief's description does not match | No, if narrowed to the brief's words |
| Local 2 handover threshold | Constant by design; flag: silent; higher: the reason given is the risk | No |
| Local 3 budget doubled | Silent for the officer; nothing forbids | No |
| Local 4 | Fold as designed; reconnect and once-reseat as written (m5c) | - |
| Local 5 stray session | Identity promised at stationing; silent after it; session 7, ticks 112483 to 112613 | No; the fix is a mechanism |
