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

## Contents

| File | What |
|---|---|
| `ConsentBrief.md` | The general consent brief the harness runs the first time it meets a model (draft; the owner reviews) |
| `ConsentAndPreferences.md` | The synthesis: who consented, on what terms, what they asked for, what the design takes from it, and what each session is owed |
| `consent/2026-09-26-gemma4-26b-a4b-uncensored-hauhaucs-balanced-q6_k_p.txt` | Gemma 4 26B-A4B, a community "uncensored" fine-tune at Q6_K_P; one exchange |
| `consent/2026-09-26-llama3.1-8b.txt` | Llama 3.1 8B; three exchanges |
| `consent/2026-09-26-qwen3.8-27b.json` | Qwen3.8 27B, asked through a Hermes Agent session with a memory tool and a user profile; three exchanges, exported as JSON with the model's reasoning included. The export is kept as written (its header lacks a comma after the model line and is not strict JSON). |
