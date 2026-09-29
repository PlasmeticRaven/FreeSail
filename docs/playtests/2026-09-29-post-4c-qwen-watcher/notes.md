# Playtest 10: Qwen3.8 27B as watcher through the local runner, the main branch after package 29c

The topsail schooner from rest in a 20-knot northerly, seed 1805, the owner as captain in
the browser, 04:00 to 05:29 of ship's time; the same weights as playtests 6 and 8, on the
main branch with packages 29b and 29c merged (the door note carries 29c's one-sentence
rule for the turn's end). `save.json` is the game as the harness saved it when the model
left by `opt_out` at the captain's word. No new consent.

## The session

Sail made one at a time, then all hands; a tack with the model narrating it as it went;
the reef shaken out and the topgallant set; the studding sails run out and set in a
19-knot northerly at 47 degrees apparent, the larboard boom whipping and then carried
away at 05:12 with the sail hanging to leeward; the clock eased to 1x on the urgent line
as built; the captain's five orders to deal with the wreck all refused; the session ended
at the captain's word with the wreck still hanging. Eleven turns, stand-bys on the change
of the watch, "a sail shaking", named bells and an urgent event; three journal notes, the
last a review.

## Findings

1. **No order clears a wreck** (the owner's finding, and the model's). `send down the
   larboard fore topmast studdingsail boom`, `unbend the larboard fore topmast studding
   sail`, `cut away ...`, `shift ...` and `rig in the weather stuns'l` were all refused; the
   grammar has no verb for a carried-away spar or a wrecked sail, and every existing verb
   refuses a wrecked part in words. The model: "a wrecked spar with no way to clear it
   hangs over the whole deck; in a real test that is where the session breaks, or where
   the vocabulary should grow." Design: `cut away` / `clear away the wreck` as an
   evolution with hands and time (the wrecked sail unbent and sent down, the spar's
   remains sent down or cut adrift, the log saying what went over the side), and `shift
   the <spar>` for a spare where the ship carries one, as sails are shifted from the sail
   room today.
2. **The storm mizzen is not drawn** (the owner's finding, from another session): the
   frigate's storm mizzen is a jib-headed sail on a vertical stay under the mizzen
   trestle-trees (`storm_mizzen.stay`, `of: mizzen.mast`, no run to another spar), and the
   viewer places a stayed sail by its stay's foot, which that stay has not got; the two
   storm staysails on stays with a run are drawn. A viewer fault for the viewer package
   (`docs/design/Presentation.md`).
3. **"Heard, though nothing was asked" read as a refusal.** The captain sent "shall we
   tack or wear?" with `tell`, a word; the model answered with the `answer` tool; the
   harness put the words in the log as said (`agent.said`, notable) and returned "Heard,
   though nothing was asked", which the model read as its answer refused and lost, and
   said so in its review. The words reached the captain. The result should say so:
   "Heard; your words are in the log, though no question was put." One line.
4. **A stand-by's earlier calls' results are not returned**, so the model believed its
   journal note before a `stand_by` in the same reply "did not run". It ran (the note is
   in the journal at 04:38); the harness ends the turn at the stand-by and returns no
   results for the calls before it (28c). The sample that ends the stand-by could say what
   ran. Small.
5. **What it liked**: the refusals that teach the language ("the main gaff topsail has no
   reef bands; it is set whole or not at all", "which studdingsail: starboard, larboard,
   or both?"); the standing order firing exactly when its condition held; the clock easing
   to 1x so the carry-away could be read; the roll-up keeping the log honest. Its warning
   as the studding sails were run out ("a 19-knot northerly is stiff for studding sails")
   was the right call, and the boom went.

## What it shows

The 29c build holds: the door note's rule was read right, the stand-bys on events and
bells were used as designed, and the urgent wake worked. The findings are the game's
vocabulary (the wreck), the viewer (the storm mizzen) and two result strings.
