# Playtest 8: Qwen3.8 27B as watcher through Ollama and the local runner, gate 4c build

The topsail schooner from rest in a 25-knot northerly, seed 10, the owner as captain in the
browser, 04:00 to 06:42 of ship's time on 1 June 1805; the same weights as playtest 6
(consent `docs/agents/consent/e7ec3377-2026-09-28-qwen3.8-27b-digest-...md`), on the gate
4c build (before the path fix). `save.json` is the game as the harness saved it when the
model left by `opt_out` at the captain's word (the ship path's slashes made forward);
`runner-log.txt` is the runner's terminal, which shows every turn as the harness saw it.
No new consent. The owner counts this and playtest 9 as the provisional local test that
closes gate 4c (2026-09-29); `--load` was not exercised.

## The session

Sail made with the watch and then all hands; the model asked for its word on shortening
sail, given after six library reads and a journal note; one reef in the main and the fore;
the wind up to 30 with gusts to 37 and four strain warnings; the model's plan for storm
canvas (bend the trysail and the storm jib, take in the flying jib, two reefs if it holds
above 35); the ship taken aback at 05:27 during the sail shifting, reported in one breath;
the storm jib bent and set; the topgallant mast sent down; the session ended at the
captain's word with the mainsail stuck (below). Twenty-seven turns, one runner timeout at
600 s (05:53, the sample left open and asked again, as 28c built it; the second ask
answered), the shelf used twice, `tell` used four times, one urgent wake-up, stand-by on
"a notable event", "an urgent event" and "three bells".

## Findings

1. **No order cancels work in hand or waiting** (the owner's finding, and the model's).
   `reef the mainsail, one reef with the idlers` waited for hands that the schooner's few
   idlers could never supply, and every later order on the mainsail (unbend, take in,
   shake out, the storm trysail's bend) queued behind it by the subject's hold. The captain
   tried `belay that`, `belay`, `belay reef the mainsail ...`, `cancel all orders`, `belay
   all work` and five more; all refused, because `belay` is a line verb and a standing
   order's verb only. The model wrote the same: "'belay', 'belay that' ... all refused ...
   I just hit 'belay' three and four times because that's the word a sailor reaches for."
   Two faults in one: no way to belay an evolution, and a party named by the captain that
   cannot man the job waits forever instead of being refused at once.
2. **An answer refused by the tool budget.** At 04:11 the model read six library sections,
   wrote a journal note, shelved, and then called `answer` as its ninth call; the budget of
   eight had closed the turn, and the answer went out only at the next sample, 04:21 ("the
   reply itself waits for the next sample, as the budget closed my turn"). `answer` and
   `say` should be allowed past the budget, or the budget should count reads only.
3. **Refusals the captain met** (the owner's, corrected 2026-09-29; the model met only
   `trim the foresail`, a trim in hand): `sail room` and `check the sail room`, which the
   console has answered since 3b (spec 3b §6.3, every sail by canvas and condition) and the
   browser never has; `send the idlers down`, tried to clear the stuck order. The owner
   holds the sail room for the interior-space basics: seeing what is in it should take
   visiting it, or reading the sailmaker's account (`docs/design/InwardAndOutward.md`).
   The model's own note on the refusals it met: they "are kind and give a next word, which
   is the right design".
4. **The bend-a-storm-sail chain** is the least transparent thing in the ship, in the model's
   words: the working sail must be unbent first, and the sequence is many orders; it asks
   for `shift the mainsail for the storm trysail` on the schooner as the frigate's spanker
   has it. (The shift evolution exists; whether the schooner's file offers it for the
   mainsail is to check.)
5. **The wind built too fast for its liking**: 28 to 30 to a 34-knot gust in five minutes
   "is a blow arriving all at once" (the M2 gustiness at 0.3 on a 25-knot base; a tuning
   remark, and the weather-systems study's gust-by-air-mass answers it).
6. **What it liked**: the strain-warning lines ("bar-taut and surging on the pin" is a
   sailor's voice, not a system string); being asked for its word and having it acted on;
   describing the ship in one breath when she was taken aback.

## What it shows

The 28c and 28d fixes hold on a thinking model at length: the stand-by ended every turn,
the one 600-second timeout was retried and the turn recovered, the shelf and the journal
were used as designed, and the model's reasoning from the readings and the primer was a
watch-keeper's throughout. The stuck mainsail is the game's fault, not the door's, and the
first finding is the one to build.
