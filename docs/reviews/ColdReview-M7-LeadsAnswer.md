# The lead's answer to the cold review of milestone 7

**For the owner.** The review (`ColdReview-M7.md`) is merged as its reviewer wrote it. This page stands beside it and changes nothing in it. Read the review's two pages first; this is short on purpose. Written 2026-11-14, the morning the review came in, after reading it whole.

## 1. What I accept

All ten of its first things, and its account of my method (5.8). No defence is offered for any of these; they are true:

- **One reader.** Packages 70 to 101 were merged on my reading alone. Since 10 November every hash has an independent reader, and every one of them has found faults the green suites and I had passed.
- **"Green" came to mean less,** and I let it, to spare the builders' hours.
- **Pins are moved by whoever moved them,** and my record of a re-pin says what changed, not that anyone judged the change was meant.
- **Briefs of mine set aside rules of the proposal without saying so** to you: the brief sent as the system message (package 42), the far captain's true positions (43), parity tested at the captain's station only (44), the ships as the output of code. You approved each brief and could not have seen from it what it overrode.
- **Hand-offs lost things:** the wheel, the sandbox, gate 6c's findings, the playtests' "small faults", the guns left secured (which I filed under "what held").
- **I broke the head rule** when I took the 74's pace test out at a merge.
- **The README's "gate m6c passed" is false,** the interim gate has sat drafted since 30 October, and no gate has been passed since 8 October.
- **The review was launched before its own condition was met.** You gave the word; you gave it on my recommendation.
- **The records cannot be read.** You learn the state of the project from me.

## 2. The two safety findings, checked by me today

Both are as the review says (its 5.4 and 5.7).

- **The server.** `freesail/ui/server.py` accepts a socket from any page (there is no check of where it comes from), and the order line it carries takes `read the standing orders from FILE` and `save PATH`. A web page open in the same browser while the game runs could read a file of yours through the game, or write a save over one.
- **A saved game's folder.** The checkpoint's loader (`freesail/core/replay.py`, `_Unpickler.find_class`) admits any name in any module of the game, and so what those modules import. A checkpoint made by someone else can run a program when it is loaded.

**Until they are mended:** run the game with no other site open in that browser (or in a browser you use for nothing else), and load no save folder that is not your own. Your own saves and your own play are not at risk from either.

## 3. The item the review disputes, and it is right

My sealed notes said the schooner of the recorded merchant passage "takes the ground thirteen times as recorded". The review found that both truths pinning her passage assert she never does.

- The figure was the ships session's, measured on your Windows machine, and I repeated it without running it.
- On the build machine, measured today: the merchant passage is 3,103 lines and she takes the ground **no** times.
- On your machine the same passage is 2,909 lines by the ships session's notes, and there she is said to ground thirteen times.

So the claim as I wrote it is wrong, and what is true is larger: **the same recorded passage is a different passage on your machine.** The pins are the build machine's. The review did not run Windows (it says so); this belongs beside its finding on determinism (§3.2; 5.5 item 9), and it bears on you directly, since Windows is where the game is played.

## 4. What "stop adding" bears on today

The review says stop adding content until the unsafe and untrue things are mended, a gate is held and a newcomer can begin. I agree. This is the work in flight, and my recommendation for each; the ruling is yours.

| Work | What it is | My recommendation |
|---|---|---|
| 111 (the chart's audit) | A check, not content; its last step is on trial | Merge and close |
| 103a (the range's audit) | A check, not content; built, on trial, being read | Merge if its reader finds it sound |
| 112 step 2 (the ocean to Cape Verde, the world's coarse level) | Content, already built and read | Merge what is built; **do not begin** step 3 |
| 106b (Morocco) | Content, building | Stop at its next report |
| The chart session's own next steps (seven tracks; the depth read along a line) | Mends of faults found | Go on |
| 60 (a ship bought, the company moved) | New play, five rounds unmerged | Finish the round in hand; it merges only when a reader cannot break it |
| The ships session (75) | Mends of the far fight and the crew, and Phase 5 | Finish the mends and the one hash; **no new hull**, and 77 and 90 not begun |

## 5. What I propose next, for your word (nothing is launched)

1. **The review's step 1 as one package of mends, in the review's own order,** each part small and each read independently before it merges: the server and the saved game first, at once; then the director's limits; the newcomer's trips (the guns, the purchase with the boat lost, the starter book by rig, the list of its 5.3); the README. The consent brief against the code is yours alone, by your own process; I touch neither the brief nor the records.
2. **Then a newcomer's gate,** as the review describes it, before anything else is added.
3. **The order of the reviews that were to follow,** as the review's 6.6 has it: 96 first, amended to begin with a first game; 103b after the gate, with a schema for the data files and one reader of a dated row first (103a's findings are its list); 92 last.

Four things only you can settle, which the review puts to you and I do not pre-judge: what the director may do to the player's ship (the proposal's sentence or the forms); the consent brief; what decision 68's sentence means for the prize court's head money; and whether the proposal gets a third version true to the tree.

## 6. What changes in my own work from today, without a ruling

- No merge on one reading (already so since 10 November).
- A moved pin is passed by someone other than the one who moved it, and its record says whether the change in the game was meant.
- A brief that sets aside any sentence of the proposal says so in a line of its own, for you to approve or refuse.
- A finding handed from one package to another is written in one place, and I will propose that place to you rather than start another record.
