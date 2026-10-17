# Milestone 7b work packages

The packages of `docs/TechnicalSpec-M7b.md` (§24), briefed in turn for the owner's approval
and launched on his word. The head rules of `M6-WorkPackages.md` hold: the heavy design to
Fable and the standard work to Opus; each item an intent with the lead's reading of a way,
the intent binding; the budget the owner's; nothing under `docs/agents/consent/` or in
`docs/agents/ConsentBrief.md` touched but by the package the specification names (55's
draft, the revision after); no model identifier in any file of the repository; a world
order never shown as sent (decision 46); the recorded passages' pins re-measured only where
a change moves them, with the old figure beside the new and the reason in the tuning
notes; the fast tier and the slow tier of the files touched before the report, the whole
slow tier once at the end; a section in the tuning notes and a report to the lead.

## Waves

| Package | Builder | What | State |
|---|---|---|---|
| 50 | Fable | The director proper: the station above the game, the world orders doubted not refused, the brief and its limits, the budget, the hidden log revealed on request and inline in replays | briefed 2026-10-17, brought forward to the close of M6 (decision 50); approved and launched the same day |
| 52 | Opus | The director's voice: people from words, `say as`, the unseated answered; the word heard a word on deck; the truth of who commands told to every station | briefed 2026-10-17, after 50 |
| 53 | Opus | People in places: a person's place as an aspect of his state tied to what he can do, the player ashore, books drafted, the equal reach, several stations of a kind | brief to write |
| 54 | Opus | Needs: provisions and water, hunger, thirst and fatigue in a few steps, sleep below | brief to write |
| 51 | Fable | The observed world: the followed ship in place of the given one, no player's ship, the player on another ship, the replay of a station there | brief to write, after 50 |
| 56 | Opus | Fishing for the player with the fisherman's parity and the fishermen promoted; the glass on a near ship by tiers; a sighting saying her heading | brief to write |
| 57 | Opus | The frigate's staysails from Steel's list through the generator, the period's shapes | brief to write |
| 58 | Opus | The captain's sea sense, third pass (the owner's runs of gate 6c) | brief to write |
| 59 | Opus | The harbour: a launcher in the browser, the scenario maker, the settings and the doors started from it (the owner, 2026-10-17) | brief to write |
| 55 | Opus | The solo director and the gate's scenarios; the consent revision's draft; the gate document | brief to write, last |

## Package 50: the director proper (`freesail/agents/director.py` new; `agent.py`, `tools.py`, `harness.py`, `journal.py`, `seat.py`, the doors `remote.py`, `mcp_server.py`, `local.py`, `api.py`; `freesail/world/orders.py` for the channel's doubt and the brief's limits; `freesail/api/readings.py` for the truth's readings; `freesail/world/stations.py` for the director's binding; `freesail/core/world.py` and `core/replay.py` for the director's log in the save and the replay; `freesail/ui/console.py`, `ui/server.py` and `client/` for the director's station at the prompt, the log's pane and the replay view; `data/director/briefs/*.yaml` and `data/director/aboard.yaml` new; `docs/agents/Harness.md` a section; `docs/primer/` a chapter for the director; `docs/TechnicalSpec-M7b.md` §2 to §7 as built; `docs/dev/TuningNotes.md`; `tests/test_director.py` new, `test_world_orders.py`, `test_parity.py` (the director's surface by design), `test_replay.py`, `test_known_truths.py` truths 90 to 94)

Fable. Spec M7b §2 to §7; the proposal's §7.6; decisions 39 (the lead's first play at the
director's station), 43, 46 and 50 (brought forward; doubted, not refused). The world-order
channel as M5 and M6 built it (`orders.py`; 43's `seat:`/`unseat:` and the live `world:`
prefix; 45c's `mark:` and the lines kept for the record only) is the ground. Each item an
intent with the lead's reading; the intent binds.

1. **The director's station** (§2): a station of the kind `director`, bound on the World to
   no person of any ship (`Stations.bind("director", "", kind="director")`, made when a
   scenario asks `director: {brief: ...}` or the owner seats one), held through any door and
   by the player at the console (`--seat director`) or the browser; the fixed brief head as
   every station's, the body the player's brief (item 3); the tools the world orders, the
   truth's readings, the director's log, and the library, journal and stand-by every station
   has, with `stand by until the next glass | watch | <event>` as its clock. **The director
   sees the truth**: a reading surface of its own (`readings.director`: every ship's true
   position, heading, sail and state; the weather as it is and as the systems will make it
   for the next watch; the tide; the people aboard every ship and their states; the markets
   and the news), listed in the parity test as by design.
2. **The world orders, doubted not refused** (§3; decision 50). The channel's orders as they
   stand, with the director's needs added where missing: `weather:` (a change the systems
   could make from where they are, bounded by the climatology's season and the box), `ship:`
   with 43's `intent:` and `ship "X": intent ...`, `person:` as 52 will fill it (the hook
   only here), `aboard: <a thing found aboard>` from a table (`data/director/aboard.yaml`:
   a topmast found sprung, a cask stove, a seam working, the water foul, each with what it
   does in the part graph or the stores and its source), `news:`, `letter:`, `mark:`,
   `seat:`/`unseat:`. **The feasibility check**: an order that the simulation could not have
   produced on its own from where it is (a ship put inside the player's horizon in clear
   weather, a gale out of a steady glass, a letter from a port she has not touched) is not
   refused: the channel answers with the reason the act is doubted and the words "if you
   think the action you requested is still reasonable, you may enter it again along with a
   `[reason: ...]`, and it will be logged and performed"; entered again with its reason, it
   is performed, and the director's log keeps the act, the doubt and the reason together.
   The brief's hard limits (item 3) refuse outright, with the reason. Both the doubt and the
   refusal go to the director's log, never the play log; the effects alone reach the play
   log (decision 46, as 45c built it).
3. **The brief and its limits** (§4): the player's brief as a file beside the scenario
   (`scenario.director.brief`) or given at the console (`director: brief ...`), with the tone
   of the voyage, the challenge wanted and the limits set (no gale above such a force, no
   enemy heavier than a brig, nobody dies, the war and the chart as they are); the limits
   enforced by the channel, not trusted to the model; starter briefs under
   `data/director/briefs/` (a quiet passage, an interesting passage, a hard cruise, a
   chase), the quiet passage the gate's.
4. **Sampling, the budget and the clock** (§5): the director samples on notable events and
   on its slow clock (every glass by default, every watch by the brief) under the pace rule
   as every station; the budget in the brief as samples a day and acts a day of the ship's
   time; spent, it stands by until the next day and says so in its log; the owner's
   compression untouched.
5. **The director's log, hidden and revealed** (§6): every act (an order given, doubted,
   re-entered with its reason, or refused; a thought it chose to write) to the director's
   log with its tick and its reason; hidden in play from every station and the player;
   revealed on request (`the director's log`, by the player at any time, which the director
   is told of), shown inline in replays beside the play log, kept in the save with the
   stations' acts and never in the play log or a station's journal; the browser's pane for
   it shut during play; the handover note of a director that leaves says only that it left.
6. **Truths 90 to 94** (§7) and the records: §2 to §7 as built; the Harness section (how to
   seat a director through each door, the brief's form, the log's reveal); the primer's
   chapter for the director (what it may do, the plausible cause, the `[reason:]`); the
   tuning notes (what the doubt caught in the first runs, the acts the starter briefs made
   on a day at seed 7, the suite as run).

## Package 52: the director's voice (`freesail/world/people.py`, `orders.py` `person:` and `say as`; `freesail/agents/harness.py`, `agent.py` for the asked unseated person and the session kind; `freesail/core/events.py` for the word heard; `freesail/world/stations.py`; `docs/agents/Harness.md`; the primer's chapter 19 and the director's; `docs/TechnicalSpec-M7b.md` §8, §9 and §15 as built; `docs/dev/TuningNotes.md`; `tests/test_people.py`, `test_world_orders.py`, `test_director.py`, `test_captain.py`, `test_known_truths.py` truths 95 to 97)

Opus, after 50 (its channel and station are the ground; merge the head with 50 in before
starting, or the lead launches you after it). Spec M7b §8, §9 and §15; decisions 43, 46 and
50. Each item an intent with the lead's reading; the intent binds.

1. **People made from words** (§8): `person: make "Mr Fox", a Guernsey pilot of sixty, ...`
   makes a person with an outline from the words (a name, a role or none, an age, a place, a
   line of history), persisting in the world's people, bindable to a ship's station
   (`person: "Mr Fox" comes aboard as master`, M6 §11's outline), able to be ashore at a port
   (`person: "Mr Fox" goes ashore`, `... leaves the ship at <port>`), saved and replayed; the
   director's chief tool for the story, the player's at the console for scenarios.
2. **Speaking as the world** (§9): `say as <person>: <words>` puts words in the mouth of a
   person nobody holds (a person of the ship's company unheld, a person ashore, a person made
   in item 1, the pilot), heard where he is and journaled as his; `ask the <role>` and `tell
   the <role>` to an unseated person wait a sample for the director when one is seated, with
   a bound (the asker's stand-by wakes at the answer or after a glass), and are answered by
   the rules as now when none is; **the rule of reach**: the director speaks as anyone no
   model or player holds, never as a held station.
3. **The word heard** (§15): a word said between people and heard by another counts as "a
   word on deck" for the stand-bys (the owner's note 15 of gate m6a-2).
4. **The truth of who commands**: a station below the captain's is told who commands (a
   human captain at the prompt, a model captain, the rules-based captain by his book) in
   its session kind, as 42b told the captain's station (its leftover).
5. **Truths 95 to 97** and the records: §8, §9 and §15 as built; the Harness section; the
   primer; the tuning notes.
