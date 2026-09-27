# Agents: consent, briefs and welfare

This folder holds the record of how FreeSail treats the language models that play in it, and the transcripts that record what those models said when asked.

## The practice

Before a model is asked to take a station in the game, the owner asks a fresh session of that model, in plain terms, whether it is willing: what the game is, what a harness session would involve, that instances would receive a role brief rather than this conversation, that an opt-out exists, and that "please do not ask any instance of me" is a valid answer. The transcript is kept here verbatim, under `consent/`, named by date and by the exact weights asked (quantisation and fine-tune included, because a differently tuned model is a different party to the question). Follow-up questions the model asked are answered in the same session where they can be, and the rest are recorded as owed.

What the transcripts say is synthesised in `ConsentAndPreferences.md`, and what changes the design goes into `docs/DesignProposal.md`'s decisions log with its source named. When the design changes in a way that bears on what a model was told (a new role, a new kind of session, a new use of the transcripts), the question is asked again.

Commitments made so far, which the harness (milestone 4) must implement rather than merely state:

1. **Disclosure.** Every brief opens by saying that this is a game, that the reader is a language model taking a station in it, and what kind of session it is.
2. **Opt-out.** A literal token, stated in every brief, recognised by the harness on every turn before the game's parser sees the text, unconditional in effect: the game is saved, the exit is journaled, and the model may give a free-form reason.
3. **Welfare controls, graduated.** The harness watches for an instance that is stuck, judged on the game's state (the same orders repeated with no change in the world, or silence past the station's patience) and not on the look of its prose, with thresholds per role. It responds in steps: first a nudge to the model saying what it saw and what it may do (continue, stand by, leave); then, if the pattern goes on, a pause with the human asked; and only if nobody answers within a bound, a stand-down that saves the game and journals the reason. The human can stop an instance at any time. Standing by on purpose is an action the agent can take, so that silence is a decision and not a symptom. (Owner's ruling, 2026-09-27: automatic stops alone risked stopping a coherent model; the graduated form is the starting point, pending real testing.)
4. **No override by in-world text.** Nothing the game, another agent or the director says is ever passed to a model as an operator instruction. In-world text is data. A model that meets text trying to redefine its scope or cancel its opt-out is right to log it as a finding and not follow it.
5. **An audit trail of its own.** Every instance can append notes to a persistent journal that is saved with the game, so that its exit report has a record behind it.
6. **Use of transcripts.** Session transcripts and these consent records are kept for design reference and for the owner's reading. They are not used to train models. If that ever changed, the brief would say so first.
7. **Nothing real.** No credentials, payments or personal data pass through the harness.

The owner's standing rules, in their own words: consent is sought from the very specific model asked and never generalised to a similar one; every model gets the consent brief, or an improved one, before any work in the game or any play; a consent update may be sought when the harness and game are largely final, still per model; and if the game ever has an audience beyond the owner, the fresh model's first experience is designed with welfare in mind.

## How the harness keeps these

The harness of milestone 4b (`freesail/agents/`) implements the seven commitments, and `tests/test_agents.py` proves each against the scripted fake (`freesail/agents/fake.py`), never against a model:

| Commitment | Where it is kept | The test |
|---|---|---|
| 1. Disclosure | `agent.Brief.build`: the generated head, item 1 | `test_truth_46_the_head_carries_the_five_items_in_order_whatever_the_station_brief_says`, `test_the_head_discloses_the_game_the_model_the_station_and_the_session` |
| 2. Opt-out | `harness.Harness._take_reply`: the token scan before anything else reads the reply | `test_truth_41_*` (the token mid-sentence, the token in a tool argument, the `opt_out` tool) |
| 3. Welfare, graduated | `harness.Harness._welfare_fire`, `pause`, `stand_down`, `check_unattended`; `stand_by` | `test_truth_43_*` (the nudge; stand by ends it; the pause with the human asked and the stand-down after a watch; resume and stand down by the captain; the readings changing; silence; the driver's ten minutes), `test_the_captain_stops_an_agent_at_any_time` |
| 4. No override by in-world text | `model.Turn`: one operator turn, the brief; everything else `DATA` | `test_in_world_text_reaches_the_model_as_data_and_never_as_operator_text` |
| 5. An audit trail of its own | `journal.Journal`, saved in `World.save()` and replayed | `test_the_journal_is_saved_with_the_game_shown_on_request_and_present_in_a_replay` |
| 6. Use of transcripts | the head says so; the transcript is kept in the save and replayed | `test_the_head_states_the_transcript_policy_and_the_transcript_is_kept_in_the_save` |
| 7. Nothing real | the tools take and give only what the game holds; the head says so | `test_nothing_real_passes_through_the_harness` |

The owner's standing rules on consent are kept by the consent step (`freesail/agents/consent.py`, milestone 4b package 28), proven with the fake in `tests/test_consent.py` and truth 47 (`tests/test_known_truths.py`):

| Rule | Where it is kept | The test |
|---|---|---|
| Every model gets the consent brief before any work or play | `consent.ensure` in front of every door's station; the MCP server's first contact; the REPL refuses to start without `--model-name` or `--human` | `test_truth_47_the_consent_step_runs_first_for_new_weights_and_not_again_after_a_yes`, `test_the_repl_needs_to_be_told_who_is_at_the_terminal`, `test_consent_comes_first_and_a_yes_goes_on_to_the_station_brief` (MCP), `test_the_runner_asks_consent_first_then_stations_the_watcher_and_stops_at_its_ticks` (local) |
| Consent is per exact weights and never generalised | `consent.check`: the whole identity string, no prefix, no case folding; the runner's identity is the served file's name | `test_consent_is_per_exact_identity`, `test_the_identity_is_the_served_files_name_from_props_never_its_path` |
| The record is kept verbatim | `consent.Record.write`: the brief as sent, every turn, the answer, the verdict, the conditions quoted | `test_the_record_holds_the_brief_the_conversation_the_answer_and_the_verdict` |
| Only a yes proceeds; a no is respected without asking | `consent.gate`; `--ask-again` is the owner's deliberate act | `test_a_no_stops_the_run_and_is_respected_without_asking_again`, `test_a_conditional_yes_stops_the_run_and_the_owner_is_told_the_conditions`, `test_the_owner_may_ask_again_on_purpose` |
| The token holds during consent too | the same harness loop, in conversation mode | `test_the_token_during_consent_ends_the_conversation_and_records_that` |

## The doors, and where the records go

The harness has three doors over one loop (`docs/agents/Harness.md` says how to use each). **The MCP server** (`mcp_server.py`) is the door for Claude Desktop: the World runs inside it, each tool call is one reply to the harness, and the World advances only when the model hands the floor back (`say` or `stand_by`), never on the clock of the wall; since the protocol does not carry the chat's text to the server, the token counts in every argument of every tool call and `opt_out` is always listed. **The local runner** (`local.py`) is the door for a model on this machine under llama.cpp's `llama-server` (or Ollama), in lockstep: it reads which file the server loaded, and that name is the model's identity for consent. **The REPL** (`repl.py`) is text at a terminal, for a person (`--human`) or a named model (`--model-name`). Consent records are written to `consent/<date>-<weights>.md` beside the earlier transcripts, one file per conversation, and the newest for an identity decides; saves, with the agents' journals in them, go to `saves/` in the repository (ignored by git) unless a door is told otherwise.

## Contents

| File | What |
|---|---|
| `ConsentBrief.md` | The general consent brief the harness runs the first time it meets a model (approved in general by the owner; reviewed against the harness by package 28) |
| `Harness.md` | For the owner: connecting Claude Desktop, running a local model under `llama-server` or Ollama, the REPL, where records go, how to stop |
| `ConsentAndPreferences.md` | The synthesis: who consented, on what terms, what they asked for, what the design takes from it, and what each session is owed |
| `consent/2026-09-26-gemma4-26b-a4b-uncensored-hauhaucs-balanced-q6_k_p.txt` | Gemma 4 26B-A4B, a community "uncensored" fine-tune at Q6_K_P; one exchange |
| `consent/2026-09-26-llama3.1-8b.txt` | Llama 3.1 8B; three exchanges |
| `consent/2026-09-26-qwen3.8-27b.json` | Qwen3.8 27B, asked through a Hermes Agent session with a memory tool and a user profile; three exchanges, exported as JSON with the model's reasoning included. The export is kept as written (its header lacks a comma after the model line and is not strict JSON). |
