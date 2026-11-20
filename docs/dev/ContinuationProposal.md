# A proposal for the continuation (for the owner; nothing here is decided)

Written by the lead on 2026-11-14 and 15, at the owner's word ("You may consolidate a continuation proposal for once everything currently in flight is parked/merged based on the cold review and the current state"). It proposes; it decides nothing and starts nothing. Every part of it is the owner's to change, reorder or strike.

It draws on three things: the cold review of 14 November (`docs/reviews/ColdReview-M7.md`, its "For the owner: two pages" and head 6), the state of the trunk once the work in flight was closed (section 1), and what the owner has said this week about how he wants the work to run (section 2).

## 1. Where the game stands

**Since this was written (15 November, morning): all six are merged.** Part D merged after its cloud run; parts A and B were un-parked by the owner, joined by their builder and merged. The owner agreed what runs before the gate: `docs/dev/ScopeCards-BeforeTheGate.md`. The owner's saves, replayed on the trunk with five of the six in: ten of twelve end at the same tick, place and state as on the version he played, with the same orders refused; the logs differ in wording.

### The six things that were in flight on 14 November

| Piece | Outcome | What a player has from it |
|---|---|---|
| The range's audit (package 103a) | **Merged** | Nothing a player meets: a tool that holds the data to the years 1792 to 1825. |
| The ships (package 75) | **Merged and closed** | One judgement of who is an enemy, a prize or a mark, asked again when a ship changes hands; every work on deck named as an order names it; small companies handled true; the 74 finished. |
| A ship bought and changed in play (package 60) | **Merged, closed as its steps 1 and 2** | He can take command of another ship of his, and move people between two of his ships by boat. Steps 3 to 5 are on the held list. |
| The chart's depth-and-tracks step | **Merged** | Seven ports' ways in re-laid off drying ground; marks in port files read strictly. |
| The newcomer's trips (package 115, part D) | **In its last cloud run as this is written** (see the note under the table) | The gun deck answers truly and says what to order; a purchase pays when the goods are had; the starter book fitted to the rig; reports sent below without repeats. |
| The server's guard and the saved game (package 115, parts A and B) | **Parked on its branch** | Not on the trunk. Nothing in it was found unsafe or wrong; joining it to what merged before it wants one more bounded turn of its builder, which is the owner's to grant (three items, in the record). |

Each merge is the exact tree the whole suite passed on the cloud, read independently before it merged, and recorded in `docs/dev/M7-WorkPackages.md` above package 70 with what it leaves undone.

**Part D** is joined to the trunk on a scratch branch and running whole on the cloud. If that run is green and its builder reports the same hash, it merges; if not, it is parked like parts A and B. One thing in it is worth the owner's knowing either way, because it changes play: **after his own `hold your fire`, `engage` no longer opens fire by itself.** The game says so and names the order that does (`fire as they bear`). That is a ruling of the lead's inside the package, and it is his to overturn.

### The trunk against the version the owner last played

The owner last played the trunk of 11 November (his saves of the 12th carry its stamp exactly). Between that version and the six, the trunk gained more sea (Sardinia and North Africa, Sicily and Malta, the ocean to the Canaries and Cape Verde, Morocco), the mends from his play of the 12th, the signals drawn and seen, ports that change with the date, and chart corrections; the sailing, the crew, the guns and the orders were the same code.

The six are where the core changed: the ships package most of all, then package 60 and part D.

**His own saves, replayed as a diagnostic** (never a gate, by his word): on the trunk as it stood before the six, six of his twelve saves were replayed to the end and compared with the version he played, line for line. Five gave the identical log. The sixth cannot be replayed by either version, in the same way (an older limit of the replay itself). The other six, and all twelve on the trunk with the six in, were still to run when this was written; the session that runs them was restarted twice in the night.

### What has not been done, and should be before he relies on it

- **Nobody has yet played the trunk as it now stands from the player's door.** The suite is green and the pieces were read, and the cold review's own finding is that play finds what tests do not. That is step A below, and it comes before anything is built.
- **The safety work is half in.** Part D's mends to the player's road are in or about to be; the server's guard and the saved game's list are parked. Until they merge, the two things the cold review called unsafe to hand to a friend stand as they did.

### What is held, and where it is written

Nothing else is running. Held, each for a conversation with the owner before it starts: package 115's parts C (the director's limits, approved, not begun) and F (the consent work); the wheel shot away (decided, not built); package 60's steps 3 to 5 and the design of a ship's two bodies; step 3 of package 112 and the game's depth readers; packages 77 and 90 (ships); packages 96, 103b and 92 (the three reviews and designs); and the lists each merged package left.

## 2. What the owner has said, which governs the rest

In his words, this week:

- "I would just like to be able to get out from under the work that is currently in flight ... so that I can actually understand and follow what is happening as it happens, rather than being behind it all as I am now."
- "We'll just need to move back to more constrained and pre-registered scope to get back to the pace that works for me, and allows us to more carefully and fully design features and packages rather than reacting to them."
- "My primary desire now is to ensure we still have a functional game to the standard it was on the last version I played."
- "I am not attached to my playtest saves for the purpose of development. If a change invalidates an old save, or an old scenario, that is not necessarily a fault ... the essence of the game is not in any of the currently existing scenarios necessarily."
- Earlier, and still standing: new work is held while what is unsafe or untrue is mended; fewer things in flight; a true proposal; reports useful but too frequent; the milestones to be re-formed; the game built to his own standard.

What I take from these, as rules for everything below:

1. **Scope is written down and agreed before a package starts,** and it does not grow while the package runs.
2. **Few things run at once.** One building package at a time, with at most one data or chart package beside it.
3. **A feature is designed with the owner first,** in a short conversation and a short note, and built only after.
4. **The owner hears from the lead at three moments:** when a package's scope is proposed, when it merges or is parked, and when a decision is his. Not between.
5. **The measure of the game is the game played,** not old saves and not the count of tests.

## 3. How a package would run from here

### The scope card

Before any package starts, the lead writes one card of about a page and the owner agrees it or changes it. Nothing is built before that. The card says:

| Field | What it holds |
|---|---|
| Purpose | One or two sentences, in a player's words: what he will be able to do or see that he cannot now. |
| Builds | The list of what is built. Each item small enough to be tried by hand. |
| Does not build | What a reader might expect it to include and it does not. This is the line that held least this month. |
| May change | Which parts of the game it may touch, and which recorded passages or pinned results it is expected to move. Anything else that moves is a stop, not a ruling. |
| How the owner tries it | The scenario and the orders to give, to see it working. |
| Size | A number of days. If it is exceeded by half, the builder stops and the lead comes back to the owner with what is done and what is left. |
| Comes after, comes before | What must be on the trunk first, and what waits on it. |

### The run of one package

1. The card agreed.
2. For anything with new play in it, a short design note first, read by the owner.
3. Built by one builder, on one branch.
4. Read once by an independent reader, against the card. The reader is told to judge by the card: what is on it and wrong goes back; what is off it goes on a list for the owner.
5. **At most one list back to the builder.** After that it merges, or it is parked on its branch with its list and the owner is told. This is the rule that closed the six, kept as the standing rule.
6. The whole suite on the cloud, then the merge, then a record of a few lines: what a player now has, what was left out, and how to try it.

### What the lead stops doing

These are my own habits, and each of them fed the month's backlog:

- **Rulings that add scope to a package under way.** A finding outside the card goes on the owner's list. It is not ruled into the package.
- **Round after round of lists.** One list, then merge or park.
- **Starting the next thing while the last is still open,** because a builder or an allowance is free.
- **Reports between the moments in rule 4.**
- **Passing my own measurements.** A pin I move is passed by another reader, as a builder's is passed by me.

## 4. The order I propose

Seven steps. The first four follow the cold review's order almost exactly, because I think it is right. Each step is a small number of packages, each with its card. I give a rough size so the whole can be weighed; the sizes are guesses until the cards are written.

### Step A. Stand still and look (no code; a few days, mostly the owner's)

- **The owner plays the trunk as it now stands.** This is the gate the project has not held since October, in the form the cold review asks for: from the opening page, through a passage, a fight and a port. I give him a short page of what is new since he last played and how to see each thing (the signals in particular, which he has not seen in action).
- **Before he plays, I play it myself from the player's door** (each scenario begun; a passage sailed; an anchorage made; an action fought; a boat sent; a game saved and loaded) and mend nothing: I list what fails.
- **The milestones re-formed.** My proposal: milestone 7 is closed where it stands, at that gate, with what it still owes written as a short list and carried forward. No milestone is "frozen open" again. The next milestone is steps B to D below and nothing else.
- **One page of "the game as built"** in place of the records as the way to know the state of the project. The records stay as they are, as history.

### Step B. Finish making it safe and true (about a week)

What is left of the cold review's first step:

- **The server's guard and the saved game, joined and merged** (package 115, parts A and B, parked): one bounded turn of its builder, at the owner's word. And part D, if it was parked.

- **The director's limits** (package 115 part C: approved by the owner, not begun). The director free by default; a brief's limits that refuse when they are set; the director's log as the record.
- **The consent brief against the code** (part F and the revision). The owner's own process: either the code is changed to match what models were told, or the brief is revised and each yes asked again once. His call which, item by item; I will set the items out.
- **The saved game's last gap:** a doctored checkpoint can no longer run code, but it can still make the game read a file of its choosing. Small; mended at the loader.
- **The README and the design proposal's status line made true** where they are not.

### Step C. The first hour (one to two weeks)

The cold review's third step, and in my judgement the most valuable thing on this page for the game as a game:

- A first game named on the opening page, in place of a form and a list of forty-eight scenarios in alphabetical order.
- The lessons listed as lessons; the test and gate scenarios taken out of the player's list.
- The guided first passage with the sailing master, which the design proposal always meant the game to have.

This wants a design conversation with the owner before its card: what the first game is, and what a newcomer is told and not told.

### Step D. The test suite made cheaper and truer (about a week)

A whole run costs over an hour and was the chief cause of this month's queue. In the cold review's order:

- **Restore the meaning of a green run:** the tests found to pass with the game broken are mended or removed.
- **Pins that explain themselves,** each with the reason it holds, and none passed by whoever moved it.
- **Timing tests out of the ordinary tiers.** Three of them failed under load this week and each cost a run.
- Then the cheaper-suite items: the truths that only run another file's tests a second time; the tiers kept by the tool and not by hand.

No change to the game. It buys back hours on every package after it.

### Step E. The small decided things (one package, its scope chosen by the owner from a list)

Things found this month that are small, already decided or plainly wrong, and were kept out of the six to close them. The owner picks which go on the card; the rest stay listed. Among them:

- **The wheel shot away stops the helm until it is repaired** (the owner's decision of 14 November).
- The merchant brig cannot let go her anchor (her company is smaller than the evolution asks).
- The cruiser's prize doctrine is never read (thirteen keys in the wrong place in her file).
- `strike the colours` is read as striking a standing order.
- The rules captain's pilotage out of Carrick Road (he strikes the Black Rock after being warned of it).
- A boarding party made of the same men who serve the guns.
- `fire` at the word fires the first gun that is ready and not the whole side together (older than this month; found when part D's ruling on the hold showed it).
- The lists left by packages 60, 75 and 115 (each in its merge record).

### Step F. The designs that are waiting (each a conversation first, then a card; none sized here)

In the order I would take them, and why:

1. **A ship left and taken up again, and the two bodies of a ship** (package 60's steps 3 to 5, with the design statement of the near and far ship that I owe the owner). It finishes a package the owner did not like to leave unfinished, and it mends the part of the world the player meets most.
2. **The boundary between the simulation and what drives or shows it** (the cold review's step 5): first a test that counts today's crossings and fails at one more; then the worst of them. Unseen by a player, and the thing that makes every later change cheaper.
3. **The harbour and the ship's configuration** (package 96), amended as the cold review advises: the harbour's first duty is the newcomer's first game.
4. **The range of years' lever** (package 103b), after a schema that refuses a key it does not know, so that thirty-three years of rows are not written into files where a mistake is silent.
5. **The career** (package 92), last: it lays a new layer on the ports, the far world and the director.

### Step G. What stays stopped until the owner says otherwise

More sea (the Mediterranean's remaining chart layers; package 112's step 3; the depth readers), more ships (packages 77 and 90), more ports, more nations' tables. The cold review's first instruction was to stop adding, and the owner asked for the same on 13 November. Nothing in steps A to E adds content.

## 5. The decisions that are the owner's

Each with what I would choose, so that a yes is enough where he agrees.

| # | The decision | What I would choose |
|---|---|---|
| 1 | Is the scope card of section 3 the form he wants, and is "one list, then merge or park" the standing rule? | Yes to both. |
| 2 | Is milestone 7 closed where it stands, at a gate he plays, with its remainder carried forward as a list? | Yes. |
| 3 | The order of steps B, C and D. | As written. If he would rather play a better first hour before anything else, C before B, except the saved game's gap, which is small and goes first. |
| 4 | The consent brief: change the code to match what was said, or revise the brief and ask again. | Change the code where it is cheap (the situation sent as data; the whole call scanned for the token), and revise for the rest in one revision. |
| 5 | Which of step E's items go on its card. | The wheel, the merchant brig's anchor, the cruiser's keys, `strike the colours`. The others listed. |
| 6 | Whether package 60's steps 3 to 5 come before the boundary or after. | Before: it is the nearer to a player. |
| 7 | How often he wants to hear from me outside the three moments. | A page a week, on a fixed day, and nothing else unasked. |
| 8 | Whether the parallel cloud runs he allowed on 14 November stay allowed. | Yes, for merges only. They do not make a run shorter (the account runs a fixed number of jobs at once), but they let several finished things be tried together. |

## 6. What this proposal does not do

It does not rewrite the design proposal (the cold review's step 7: "say what the proposal now is"). That is worth doing, and I would do it after step A, once the owner has played and the milestone is closed, so that it describes a thing he has just seen. It does not size steps F and G. And it does not start anything.
