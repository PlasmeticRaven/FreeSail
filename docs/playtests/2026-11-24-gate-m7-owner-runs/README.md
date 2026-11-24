# Gate M7: the owner's runs (2026-11-24)

The owner's play of the build `m7` (branch `gates/m7`, tag `gate-m7`, the second cut), and of a build of his own a few days before the cut. The gate's page is `docs/gates/gate-m7.md`; the verdict is his: **closed, with a list**.

## His notes, as he gave them

1. For the first passage, we should adjust it so that it teaches to use the time compression, rather than the manual tick command, after the first tick command which shows that it is possible.
2. If it does not already exist, an option to end the game from the harbor would be good, so that a running game can be ended without restarting the harbor or starting a new game.
3. Trade passage went smoothly, one thing that stuck out was that fog clears instantaneously. It might be better for it to clear over a period of time, depending on the degree of additional weather simulation necessary. Perhaps, at least, "the fog seems to be clearing", or, "a fog is settling in", or the like.
4. First action went reasonably, I took a musket ball this time and devolved the command, the ship fought on, but seemed outmatched, and I came back on deck and struck the colours. I was taken prisoner on the Renard, paroled, and watched as she was repaired and saved. I noticed she did not attempt to replace the topgallant mast or yard.
5. Saved the first action game after being captured, closed the browser, stopped the harbor, restarted it, loaded the save, and it seems to have loaded properly with me on the Renard.

And with them: "I'm working through it and mostly happy so far, possibly enough to clear the gate, as some of the things gated here I have just been testing on the close pre-gate version, which, despite not being exactly the same, is largely the same by what I can tell." "I think, unless there's something you want me to take a look at specifically now, the gate could probably be marked closed with a list."

On step 9, which the lead put to him as the one step played on neither build: "The one reason I am happy to pass step 9 as not played on the gate build, is that I did run that one adversarial action, and was happy with it's outcome, it only ending before the parole feature was implemented."

## The walk, step by step

| Step | Played on | What came of it |
|---|---|---|
| 1. The opening page (*A first passage*) | the gate build | Played; his note 1 |
| 2. A passage and a port (*Trade*) | the gate build | The merchant cutter, free, from L'Orient, sixty-seven hours of her time; "went smoothly"; his note 3 |
| 3. A fight (*the first action*) | the gate build | Fought; wounded, the command devolved; came back on deck and struck; a prisoner aboard the Renard, his parole asked and given; his note 4 |
| 4. A wheel shot away | did not arise | The step was "if the fight gives you one" |
| 5. Save, close the browser, take the game up again | the gate build | The harbour stopped and started as well; loaded with him aboard the Renard; his note 5 |
| 6 to 8. A director, and models at the stations | his build before the cut | A cruise in the frigate under a privateer's papers: a model at the director's station and a model officer of the watch through thirty-nine hours of her time |
| 9. A model commanding the other ship in a fight | not on the gate build | Passed as not played, in his words above: he had fought one such action on an earlier build and was content with it; it ended before parole was built |

## What the lead checked

His three saves were read by the lead as data and loaded through the game's own loader on the gate's tree; nothing in them was run. They are kept with the lead and are not in the repository.

- **The two gate saves** were written by the build `m7` with the second cut's rules, and both load on the gate's tree (the first action by replay in a minute and a half).
- **Note 2:** the harbour starts a game and has no way to end one. Confirmed.
- **Note 3:** the weather goes between fog, with a cable's sight, and clear at one moment, with the lines "Fog came down." and "The fog lifted." and nothing between. Confirmed.
- **Note 4:** in his save the Renard's main topgallant mast is shot away by his own fire, the yard hanging to leeward. In the three hours of her time that follow, her people plug her shot holes and set up her rigging; the spar is never shifted, and every trim says "the topgallant yard is carried away". The game has the work (a spare spar shifted, a jury mast), and its own captain orders a sprung spar fished; he does not order a spar carried away replaced. Confirmed.
- **The third save,** from his build before the cut, shows what steps 6 to 8 ask: a model at the director's station (288 acts) and a model officer of the watch (1,762 acts).

## The list he names

Mended first in the next milestone, by the gate's fourth rule:

1. *A first passage* teaches the time's compression after the first `tick` has shown what a tick is.
2. A game can be ended from the harbour.
3. Fog comes on and clears over a time, and is said as it does.
4. The game's own captain replaces a spar carried away.

What else is carried forward is the lead's list: `docs/dev/CarriedForward-M7.md`.
