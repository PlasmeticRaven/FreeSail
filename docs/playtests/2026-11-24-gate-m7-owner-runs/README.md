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

## His later notes (received 2026-11-27)

After the gate closed he sent the notes of his further play on the build `m7`, a cruise in the hermaphrodite brig from off Dover as a King's ship, with three saves of it (kept with the lead; read as data and replayed through the game's own loader on the gate's tree; nothing in them run). His notes 1 to 5 are those above; the rest, as he gave them:

6. Some kind of slowdown is occurring, does not seem to be from nearby ships being live from initial impressions. Saved the game and reloaded both with and without restarting the whole game, and the same slow pace remained, at about 100000 ticks, the maximum pace on my computer seems to be about 60x, even when set to a higher compression, and not ticking very quickly at that. At the start of the game, the compression ran correctly. At the later -2 save, the performance appears to have increased for a non-obvious reason. After some further play, could it be that another ship was chasing mine and I was unaware, and that ship was kept at high detail thus causing slower performance, even though it was far out of range? Performance might need a closer look, if this is not a bug.
7. Manually appointed devolution of command for situations with multiple officers of various ranks
8. Bow/stern raking modeling. More effective/damaging hits when raked from bow or stern. Increased lethality/chance of hitting multiple crew.
9. Fires and fire control, powder explosion, gun faults/condition/maintenance.
10. In the Neufchatel Cruise, the ship was set in the harbor to be a king's ship, and reads as such, but was not given the private signals automatically.
11. Temperature.

### What the lead found

- **Note 6 is a fault, and his guess was near it.** The lead replayed his third save on the gate's tree with the pace timed every two thousand ticks, and profiled the slow stretch. No ship chased him. One trader of the background trade, at anchor off Le Havre more than a hundred miles from him, lays her whole passage over the chart afresh every minute of the day and never sails (`docs/dev/CarriedForward-M7.md`, section 4, fault 17). On the build machine the cruise runs four hundred to fourteen hundred ticks a second until the middle of its first afternoon, about fifty from then until dark with two traders crewed within four miles of him, three hundred and fifty to five hundred through the night (she does not weigh by night) with the same two crewed, and thirty-five to forty from the next dawn with three crewed. His "about 100000 ticks" is the second day; his quicker second save, at tick 154909, is the second night. Of 11.6 seconds for six hundred ticks of the slow stretch, 7.7 were hers.
- **The ships kept at full detail are the design's.** A ship with a captain within four miles of the player is made a fully crewed ship, three at most at once; off Dover, with the trade bound for the Downs, the cap is often full. They cost what the design measured (about a hundred and fifty ticks a second with two awake here), which is above the sixty he plays at on the build machine and may be near it on his.
- **Note 10 is a fault of the rule, written down as intended** (fault 18 of the same list): the harbour's King's ship is one by her papers, and the private signals are given by the captain's place or a scenario's line the harbour does not write.
- **Notes 7, 8, 9 and 11 are things not built.** The command devolves on the senior officer by rule, with no order of the captain's to change it (the proposal's decision 63). A shot is placed anywhere along the length a ship presents, whatever her aspect, and harms the men nearest it: nothing rakes. No fire takes hold aboard, no magazine is in danger, and a gun has no faults but a shot's damage. The temperature is the spec's section 26, deferred within milestone 7. The lead's proposed placing of each is in the carried list's section 8.
