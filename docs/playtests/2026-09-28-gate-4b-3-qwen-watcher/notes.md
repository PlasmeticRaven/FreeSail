# Playtest 6: Qwen3.8 27B as watcher through Ollama and the local runner, gate 4b-3 build

The first local model to hold the watcher's station well. `save.json` is the game as the
runner saved it at 04:55 ship's time, when it stood the station down after three
requests to the model server timed out in a row (the ship path made relative). The
consent for these weights is `docs/agents/consent/2026-09-28-qwen3.8-27b-digest-...md`,
asked fresh inside the harness as the owner's rule requires (the earlier conversation of
2026-09-26 was in another agent framework); a plain yes.

## What the model did

- **A sailor's voice from the first line.** "A fresh, steady breeze from the north, fifteen
  knots, no more, no less, yet she lies dead in the water with every sheet furled ... the
  quiet of held-breath, not of calm; canvas and breeze both waiting for a word."
- **Sound reasoning from the readings.** SW by S in a northerly read as a run, then a
  broad reach with the wind on the starboard quarter; the yards braced in turn "not
  hands enough for all at once"; the standing order "Trim Sails" seen to fire at the
  bell and its work described correctly.
- **One stand-by per turn, every turn**, until a notable event, then until one bell. The
  turn-ending stand-by of package 28c did exactly what it was built to do.
- **The shelf, used as designed.** Asked to look in the library, it read the contents,
  opened chapter 4's headings, read the section "The trim order" (about 700 tokens
  rather than the 6,400 of the chapter), journaled what it took from it, and shelved the
  book, then shelved two earlier books it had left open; and it told the captain so in
  its own words, "set the matter down in my journal and put the book back on the shelf".
- **The journal reads like a watch-keeper's**: "04:02, 'Set plain sail' given; hands aloft
  fore, main and mizzen at once ... Helm ordered SW by S (215°), a run, sensible for a
  15-knot northerly."

## How it ended

Asked to journal anything laborious about its tools and then take its leave, it opened
the contents again and then primer 2 whole (`section='all'`, about 2,800 tokens), and
the next three requests each timed out at the runner's 180 s, after which the runner
stood the station down with the reason. The farewell note was never written.

**The cause is the per-request timeout, not the context.** The context guard passed at
stationing (the owner's Ollama serves the model with well over 100k tokens). Qwen3.8 is
a thinking model: a reply that reads a chapter, composes a long journal note and a
farewell, with its reasoning counted against the same budget, can run to the 4,096-token
reply budget, and 4,096 tokens on a 27B model at four bits on a 4090 take about three
minutes to generate, before the prompt of some fifteen thousand tokens is even read. So
a legitimate long reply is cut off at 180 s, and retried, and cut off again, three times.
The budget bounds a runaway; the timeout was meant only for a server that has hung, and
it was set shorter than an honest reply can take.

## Follow-up

The runner's request timeout to be sized from the reply budget and the model's observed
speed (or simply long: ten minutes, with `--request-timeout` to change it), so that the
budget, not the clock, is what bounds a reply; a timeout then means a hung server, as
intended. A small note: the journal's stand-by line for an interval reads "Stood by until
1 bell have passed" (the interval's words need the singular).
