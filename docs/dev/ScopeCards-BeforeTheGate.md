# Scope cards: what runs before the gate (for the owner's agreement)

Written by the lead on 2026-11-15, after the owner's word of that morning: "the only thing I would run before a gate would be the package 96, as the harbour has become enough out of date, and wants access to the full current set of features enough that before I can jump in to a gate or proper testing, the harbour should be brought up to date, and further design of it both for an experienced user and for a newcomer considered. As well, a consent revision package (55(?) or a fresh one)."

**Agreed by the owner, 2026-11-15:** "The order, card 1, and card 2 are approved. Adversarial seating should be included in the consent wording, and the director's limits may be included after a card between the harbour's build and revision." So:

- **The order stands as written below,** with one card added: the director's limits (package 115, part C), a small card of its own, written when its turn comes, between the harbour's build and the consent revision.
- **Card 1 stands,** with its choice settled as proposed: the design covers both layers; the build before the gate is the page only; the deeper layer (a ship's configuration as one thing in the game's code) is designed, left unbuilt, and decided after the gate.
- **Card 2 stands,** with the adversarial seats' wording carried in the one revision.

Nothing is begun until the two pieces in hand have merged (step 1 of the order).

The form is the one proposed in `docs/dev/ContinuationProposal.md`, section 3.

## The order I propose

1. The two pieces still in hand finish: package 115's part D and its parts A and B.
2. **Package 96, first card: the harbour's design** (a document, no code).
3. The owner reads the design and answers its questions.
4. **Package 96, second card: the harbour's build**, written from the design he has agreed, in small steps.
5. **The director's limits** (package 115, part C), a small card of its own (added at the owner's agreement).
6. **The consent revision**, last, so that nothing built after it changes what a model was told; the adversarial seats' wording in it.
7. The gate script (one page) and the lead's own play of the trunk; then the owner's gate.

One thing at a time. The four small mends named on 15 November (the wheel shot away, the merchant brig's anchor, `strike the colours`, the cruiser's prize keys) are not run before the gate; they go into the gate script as known.

## Card 1. Package 96a: the harbour, designed

| Field | |
|---|---|
| **Purpose** | Before the gate the owner can start any game the build can play from the harbour's page, without editing a file by hand. The page serves two readers: the experienced player, who can reach everything; and a newcomer, who is offered a first game and is not shown a wall of fields. |
| **Builds** | One document, `docs/design/Design-Harbour.md`, and nothing else. It holds: |
| | **(1) An inventory.** Everything the game can now be told at its start, in three columns: reachable from the page today; reachable only by editing a file; not reachable at all. It takes in what has arrived since the page was last worked on: a second ship of the player's and people moved between ships; squadrons; the papers and the private signal; the people by name; the ship's fit, role and crew; the flags a ship carries; the scenario's year and the ports as they stood on that day; the new seas and the new ships; several models at several stations; the director and what it is granted; where saves are kept. |
| | **(2) The page for the experienced player:** how all of that is offered without becoming a wall of fields (the common case a few choices; the whole opened by a step; every ship of a scenario set up the same way; each setting explained where it is set). |
| | **(3) The page for a newcomer:** a first game named on the page; the lessons listed as lessons; the scenarios that exist for tests and gates taken out of the player's list. Design only: the guided first passage itself is not part of this package. |
| | **(4) The build, in steps,** each small enough to try by hand, each marked as either "the page only" or "needs a change in how the game reads a scenario". |
| | **(5) The questions that are the owner's.** |
| **Does not build** | Any code. The guided first passage with the sailing master. The director's limits. Anything of the consent work. |
| **May change** | Nothing but the new document. |
| **How the owner tries it** | He reads the document and answers its questions. |
| **Size** | Two to three days. If the inventory alone shows the build is more than about two weeks, the document says so and stops there. |
| **Comes after** | Parts D and A/B of package 115 merged, so that the inventory is of the trunk as it will be at the gate. |
| **Who** | One session, design only; read by the lead against this card, then by the owner. |

**The one choice in this card that is the owner's now.** The brief written for package 96 on 6 November has two layers. The upper one is the page: presenting every setting the game has. The lower one is deeper: making "the configuration of a ship" one thing in the game's own code, which the scenario maker, the director's `ship` order and the world's business would all build their ships from. The lower layer is a change to how every ship in the game is made. It is the kind of change that could make a working game worse by degrees.

What I propose: **the design covers both layers, and the build before the gate is the upper one only**, the page and the scenario's keys as the game already reads them. The lower layer is designed, left unbuilt, and decided after the gate, when the owner has played. If the inventory shows something the page cannot offer without the lower layer, the design names it and the owner chooses.

## Card 2. The consent revision

| Field | |
|---|---|
| **Purpose** | What a model is told when it is asked to take a station is what the game does; the way out works wherever a model writes it; and each model with a yes on record is asked again, once. |
| **Builds** | **(1) The code made to keep the brief where that is cheap.** The opt-out token found wherever a reply can carry it, at every door (today a model at the local runner that writes it inside a tool call is not heard). Nothing from the game, another station or the director reaching a model in the operator's voice (today the station's brief goes as the operator's message at two doors and carries the night orders and the last holder's note): a short ground report to the lead first, then the change. |
| | **(2) A list of every sentence of the consent brief the game does not bear out,** each with where the game shows it, and for each whether code or only a revision can make it true. The cold review names two: that nothing in the game acts on what is written in a journal (a seated director reads every station's reply), and that the director "is to come" (it is built and can be seated). |
| | **(3) One revision of the brief** (`docs/agents/ConsentBrief.md`) carrying all of it, under the practice in `docs/agents/README.md`: everything that touches the brief in one revision, so that each yes is asked again once and not twice. |
| | **(4) What the owner needs for the asking again:** the revised brief, the list of the models with a yes on record, and what changed, in a paragraph a model can be shown. |
| **Does not build** | Any new station. The asking itself, and the records of it, which are the owner's own act and the owner's to file. The director's limits. |
| **May change** | The three doors a model plays through and the harness's scan of a reply; the consent brief; their tests. The brief's sections change, so the game will ask for consent again at each station whose section changed: that is the practice working, and is meant. |
| **How the owner tries it** | He puts the revised brief to one model in a fresh session. A model seated at a station that writes the token inside a tool call is stood down. A standing order named as if it were an operator's instruction reaches an officer as data. |
| **Size** | About a week, the owner's own asking included. |
| **Comes after** | Package 96's build, and anything else that would change what a model is told. Last before the gate. |
| **Who** | One builder; every hash read independently before it merges. |

**Two choices in this card that are the owner's.**

1. **The adversarial seats.** Package 74 drafted a further revision (`docs/design/ConsentRevision-AdversarialSeats.md`): the words that would let a model be asked to captain a ship that fights a human's. Until it is approved the game refuses that seat. It can ride in this one revision, so that no model is asked twice, or stay out. If the gate is to have a model commanding an enemy, it has to be in. I would put it in: the asking is the same asking, and leaving it out means a second round later.
2. **The director's limits** (package 115, part C: approved by the owner on 14 November, not begun). The brief speaks of the director, and part C changes what the director may do. If part C is to be built at all before the next revision, it should be built before this one, or the brief is revised twice. I would run part C as a small card of its own between the harbour's build and this revision. If the owner would rather keep the list before the gate to the two he named, the revision goes ahead without it and says of the director only what is true today.

## Card 3. Package 96b: the harbour, built (proposed 2026-11-15 from the design the owner answered)

**The owner's answers to the design's questions, 2026-11-15:** "Yes to each question, as proposed, except for number 10, as I think we can handle running this without cutting any steps." So: the first game is the primer's chapter 7 written as a scenario, "A first passage"; one card for every ship with the lines the game does not yet take shown greyed; the flags a ship carries wait with the deeper layer; two text boxes for the weather's systems and a port's letters; the year's sentence said on the page; the shelves kept in one new file; the sorting as proposed, the seven tests' and gates' scenarios behind a tick box; one list of models for the API door; the page reads a scenario's "a model" for his own ship and offers the door; the three small faults listed for the gate. **All eleven steps are built; none is cut.**

**And on the tests, his word:** "The key to making sure this work doesn't take 10 days is that we use the suites intelligently here. Since this is meta-game code, we can probably carefully constrain or even bypass the suites for most of the steps here." The gate below is built on that.

| Field | |
|---|---|
| **Purpose** | As card 1: the owner can start any game the build can play from the harbour's page, without editing a file; an experienced player reaches everything; a newcomer is offered a first game. |
| **Builds** | The eleven steps of `docs/design/Design-Harbour.md`, section 4, in its order, as answered above. Each step leaves the page working and is merged alone. |
| **Does not build** | Anything that changes how the game reads a scenario (the design's list a to i). The deeper layer. The locker. The guided first passage. The director's limits. Anything of the consent work. A second local runner. |
| **May change** | **Only these:** the page's own files (`client/harbour.html`, `client/harbour.js`, the harbour's part of `client/style.css`, one new file of the page's sentences); the page's own server (`freesail/ui/harbour.py`); one new file of shelves; in step 2 one new scenario, "A first passage", of keys the game reads today; in step 9 the settings form showing the list of models it already keeps; in step 11 the primer's chapter on starting a game and the README's paragraph; the tests of these. **A step that needs any other file stops, and the builder tells the lead before touching it.** |
| **How the owner tries it** | Each step by its own line in the design ("the owner tries it by"). He may try each as it lands, or wait for the three natural stopping points: after step 3 (the newcomer's page), after step 7 (every ship, squadrons, papers and people), after step 11 (the whole). |
| **Size** | The design counts nine to twelve working days of building. With the gate below, the calendar should be set by how fast the owner wants to try the steps, not by the tests: a few days. If a step proves not to be the page only, it stops there and comes back to the owner. |
| **Comes after** | The design document on the trunk. |
| **Who** | The session that wrote the design, which has the inventory in its head. |

### The gate for this package: narrow where the step is the page only

The whole suite takes over an hour on the cloud and tests the ship, the sea and the fight. A step that changes only the page cannot move any of that, **provided it really does change only the page.** So the rule has two halves: a narrow gate, and a mechanical check that the step earned it.

**For every step:**
1. **The paths are checked, not trusted.** Before a step merges, the lead lists every file it changed and compares them with the "may change" list above. One file outside it, and the step gets the whole suite or goes back.
2. **The narrow gate:** lint; the page's own tests and the server's (the harbour's, the settings', and the guard's truths from package 115, so that every new road the page opens is behind the guard); the browser plans, which drive the real page; and the one test that reads every file of the repository. Minutes, not an hour.
3. **The lead reads the step's changes** before it merges.

**The exceptions, which get more:**
- **Step 2 adds a scenario.** Thirty-six test files walk the scenarios, and several count them. It gets the whole suite on the cloud before it merges, like any package.
- **Step 9 starts doors for models.** It gets the doors' and the stations' tests as well, and an independent reading of its own, because it is where the page touches what a model is asked.
- **Step 11 changes the primer.** It gets the primer's tests.

**The whole suite still runs, after and not before:** on the trunk at the three stopping points (after steps 3, 7 and 11). If one of those runs is red, the next step waits until it is mended. And the whole page gets one independent reading at the end, before the gate.

What is given up, said plainly: between stopping points the trunk carries page changes that the whole suite has not yet run over. The path check is what makes that safe. What is not given up: the guard's tests on every step, a reading of every step, and the owner trying each step by hand, which for a page is the test that finds the most.

