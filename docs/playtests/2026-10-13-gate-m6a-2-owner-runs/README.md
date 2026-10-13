# Gate m6a-2: the owner's runs (notes of 2026-10-13, in progress)

The owner's notes on his runs of the build merged from package 45 on 2026-10-11 (the branch
at commit 3609fd7; the saves stamp themselves `m6a`, the build name not yet moved), as
written (`m6a-2_notes.txt`), with the saves of each run under `saves/`. The checkpoints that
came with them (`.checkpoint`, gzip) are not kept: a save replays by itself. The lead's cold
read is in the conversation of 2026-10-13 and the items go to the packages named there; the
verdict and the rulings in `docs/gates/gate-m6a-2.md` and `docs/DesignProposal.md`. The saves
are the owner's data files as he sent them, kept for the record and for replay (`--load`),
not read by any test.

## The saves

| Save | Scenario | Ship | End tick | Size |
|---|---|---|---|---|
| `m6a-2-cutter-voyage-anchor-in-Cariño.json` | A merchant cutter, free | cutter | 1018824 (11 d 19:00 from the start) | 1104 KB |
| `m6a-2-cutter-voyage-beat-away-from-Lisbon.json` | A merchant cutter, free | cutter | 1472866 (17 d 01:07 from the start) | 2819 KB |
| `m6a-2-cutter-voyage.json` | A merchant cutter, free | cutter | 642087 (7 d 10:21 from the start) | 732 KB |
| `m6a-real-voyage-bound-for-corunna.json` | A merchant brig, free | brig | 294821 (3 d 09:53 from the start) | 3167 KB |
| `m6a-real-voyage-guernsey.json` | A merchant brig, free | brig | 212854 (2 d 11:07 from the start) | 3257 KB |
| `m6a-real-voyage-tacking-out-of-biscay.json` | A merchant brig, free | brig | 787014 (9 d 02:36 from the start) | 3182 KB |
| `m6a-real-voyage-wind-in-biscay.json` | A merchant brig, free | brig | 693042 (8 d 00:30 from the start) | 3181 KB |
| `m6a-real-voyage.json` | A merchant brig, free | brig | 125683 (1 d 10:54 from the start) | 1907 KB |

Two voyages: the merchant brig from Falmouth to Torbay and Guernsey, then bound for
Corunna across Biscay, beating out of it; and the merchant cutter's voyage, beating away
from Lisbon and anchoring in Cariño. The wardroom stations seated through the doors are in
the saves' `stations` and `station_acts`.

## The notes, verbatim

```text
1. Full chart is working, sailed from Falmouth to Torbay then Guernsey, though the Sonnet 5.5 officer reported some uncertainty about the reported tides versus what we were experiencing, could be circumstantial.
2. The auto-shelf feature for the images is very confusing for Sonnet 5.5 and possibly Opus 5.5, as when their context is automatically rebuilt without the image, they take it to mean they never saw the image, and somewhat refuse to believe that the image was ever there, despite the log line. We need to no longer automatically shelve image requests, but only when the model voluntarily calls a shelve on them. Otherwise, they're more confusing than useful so far.
3. Queued up a send the boat ashore order waiting for hands while coming to anchor, once all the work cleared, the boat was stuck yet again in the "ghosted" hauling-out state, no fix besides a reload of an earlier save could be found in game, and I looked over the code to see if I could find a layman's fix, but I couldn't. The ability to load a saved game to an earlier tick would be useful, if possible.
4. Some more consideration for the images and shelving in general: Opus 5.5 in the master station expressed taking their own journal entry as unreliable information once the image had been shelved, suggested that manual shelving might not be a full solution, rather suggested that the log line should contain the information that their journal was written with the image open at x time, so that they would trust their journal when the context no longer contained the image/content in question. Also, I had a thought that perhaps including a self-written note in the shelf command for the log entry might be a good option, along with other changes (manual shelving and/or prompted auto-shelf note for posterity).

5. Rules based captain will be most important at the far-distance detail, for now, until combat is in. Close promotion to the full ship sim still matters, though, for port and other behavior where ships will be close in to the player's ship, or the particular ship in focus. We'll want to allow for a mode where no player is present in the world, they simply observe what is happening (basically, player in the director's station, if not functionally identical, the same idea of seeing the world as it is and being able to use world orders to interact and play around in the sandbox).
6. Viewer details: sail/mast layering, time of day lighting/some lighting effects in general

7. Wind shifting close to the stern needs to not flip all the sails across automatically and instantly. We need proper gybing and shifting over of sails both on a tack and a wear, and the wind moving about the stern should not flip a gaff sail that has its sheet let out all the way and is catching wind from aft. A gybe should be done when the intent is to actually wear through the wind, and if the wind backs a fore and aft sail, then it should have a realistic effect, possibly gybing it unintentionally, and this should be a general factor (as well as shown in the viewer, no instant gaff gybe, a good time to do this would be when making the lug sail dipping for the lugger).
8. Do crew currently use provisions/water? They should if not, see below for more notes.
9. Improved "people": free self movement between locations (the captain can go to his cabin, anyone can go to various locations on the ship or to the shore, the player can be "on the shore" versus "on the ship" and perform actions in both locations. Drafting "books", so writing up a standing orders sheet, a note for the library/ship's papers, or a manifest to buy and sell multiple items in one go. Draft the "book" for the immersion and the record, but the use is functional and matched to the current papers. If it possibly stands up from the basic consent outline, storing the papers and books on the ship itself in a certain location, so that reading it requires going to that spot (can't just read the whole library on deck, for example). This might be a step too far, but I like driving towards more immersion for both players and LLMs.
10. Multiple times in this versions' playtesting models have tried to speak to members of the crew or characters in the world that weren't stationed/couldn't be spoken to. We'll want director mode to include the ability for a director to "respond" as characters that have not been seated or aren't currently seatable. This will want a generic "world say" or "person say" that the director can use to fill in small characters or world bits that don't need a full seat. We'll also want to consider the director being able to create "people" that can persist in the world and be used durably, along with allowing the ability to fill in the edge cases where needed.
11. Shape a course via trigger needs some adjustment, regularly triggers too far from marks causing turns too early and possibly navigation hazards unnecessarily when using marks near to the coast.
12. Models (local and free ones, usually) tend to try to shape a course directly to points without considering the land in between, and also not noticing/ignoring the message that says that the line crosses land. Not necessarily something to change right away functionally, just an observation. Probably a result of not reading the library before acting, as "shape a course for x miles south of y" is already present in game.
13. Along with general crew consuming provisions and water, named people including the player should have hunger, thirst, and fatigue that increase with time and cause notable then urgent messages (even better if they're only sent/shown to the relevant person who is stationed), for example, "you're feeling a bit drowsy", "you're quite thirsty, a drink would be great right about now", "you're absolutely starving, you really must eat something", perhaps three to five levels for each stat, hunger resolved by eating action (takes from stores, must go to a place with food to eat i.e. cabin, below, the shore, etc.), drinking resolved by drinking (same as eating), fatigue resolved by resting (going below to sleep). Tie in with health mechanics for M7, hunger and thirst eventually cause death, fatigue eventually forces sleep by collapse, surgeon looks after unhealthy crew if one is onboard, general crew eat and drink on the schedule in the same way they rest now, people eat, drink, and rest automatically the same way they currently rest when no one is seated or stationed, and by self-orders otherwise.
14. Image tools on the local harness.
15. A word said between people in a location that is heard by another might want to count as "a word on deck" for the sake of waking stand-bys.
16. Let's consider a review pass on the overall current structure of the orders system (vocabulary, grammar, duplication, extensibility concerns, recommendations for improvement/consolidation/extension).
```
