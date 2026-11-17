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
5a. **The four small mends** (package 116, card 5 below; added at the owner's word of 2026-11-16).
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

## Card 3. Package 96b: the harbour, built (proposed 2026-11-15 from the design the owner answered; APPROVED by him the same day: "Card 3 is approved, go ahead.")

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

**Card 3 as it ran (2026-11-15).** All eleven steps and a final list are on the trunk (468c095f); the record is in `docs/dev/M7-WorkPackages.md`, "Package 96: the harbour designed (96a) and being built (96b), step by step". The narrow gate let two faults through to the trunk for a few hours (four slow tests of the range audit red after step 1, from a file the lead had placed under `data/`; a pasted text that could hold the server, from step 8) and would have let through a third (a model's name in the page's state, caught by the independent reading of step 9 before it merged). The gate was widened after each. The whole suite ran four times on the way (runs 120 to 123) and once more on the finished trunk (run 124).

## Card 4. Package 115, part C: the director's limits (proposed 2026-11-15; APPROVED by the owner the same day, with two points settled)

**The owner, 2026-11-15:** "For card 4, it is approved besides two things: one, should we run this on Opus or Fable, by your estimation (I am not particularly inclined away from Fable here), and, since the player as director is not a focused role for now (I think a model will almost always be present as director, even when a player might want to observe a world, it might be 'co-incidental' with a model director for cooperative play), I think that you should be the primary initial tester after the changes on this package. Thoughts? We could do a test run together, you as director, after the package is complete."

**Settled so:**
- **The tier: Fable builds, Opus reads.** The lead's estimate, which the owner left to him: the hard part of this package is one table that every channel reads and every spelling meets, in the game's own code and with recorded passages that will move; a wrong shape there costs more than the builder's tier does. Every hash is read by an independent reader of the other tier, as the owner's standing rule has it.
- **The first tester is the lead, as a model at the director's station,** through the game's own door and its own consent step, and not the owner in the director's seat (the row "How it is tried" below is changed to say so). Then a run together, the owner playing and the lead directing, once the package is merged.

The shape of this part was ruled and approved by the owner on 14 November ("I think that the director free by default and the brief's limits being properly enforceable when set is right, and the original idea for the director where their log was readable as a 'secondary story' should be sufficient for showing the effects rather than a particular special log entry for director orders to the player ship. Otherwise, I approve part C."). This card puts that ruling in the form of the other cards, so that its scope is agreed before it starts and does not grow. It adds nothing to the ruling.

| Field | |
|---|---|
| **Purpose** | The director may do whatever the story needs, the player's own ship included, as now. When a brief sets a limit, the limit holds whatever words the director uses. And what the director did to the player's ship can be read afterwards in the director's own log. |
| **Builds** | **(1) One table of the director's order forms,** each with whom it reaches (the player's ship, his person, his prompt, another ship, the world) and whether it can kill. The order channel, the director and the doubt all read the same table. |
| | **(2) A brief's limits judged against that table, and only when a brief sets them.** An order that names the ship another way does not slip past a limit; "nobody dies" has the deadly acts marked, so it has something to refuse; a weight the limit cannot rank is refused, not passed. One limit a brief may newly set, and no shipped brief sets: hands off the player's own ship. |
| | **(3) The director's log holds every act that reaches the player's ship, person or prompt,** in words a reader follows. No special line is said to the player. |
| | **(4) The words made true:** the primer's account of the director says what the director can do. For the words a model at the director's station is shown, see the first step below. |
| | **(5) Tests through the director's own door,** the cold review's two probes among them: under a brief with no limits the acts are done; under a brief that sets a limit they are refused in words, by every spelling. And a list for the owner: which shipped brief sets which limit, and what each would now refuse that it let through. |
| **Does not build** | Any rule that refuses the director for being the director. A special log line or notice to the player. Any change to a shipped brief's limits (they are listed; the owner says). The consent brief's own sentences about the director (they go on the consent revision's list, card 2). The design proposal's section on the director. Anything of the harbour. |
| **May change** | The director's code and the table of the world-order forms (`freesail/agents/director.py`, `freesail/world/orders.py`), the director's log, the primer's chapter on the director, and their tests. **Expected to move:** the log lines of recorded passages that have a director in them; any pinned result that moves is measured again, old beside new, and passed by a reader other than the builder. Anything else that moves is a stop, not a ruling. |
| **First step, before any code** | A short ground report to the lead: (a) which recorded passages and pinned results have a director in them; (b) exactly which words a model at the director's station is shown would change, and whether changing them makes the game ask that model's consent again. **If it would, those words are not changed here: they are listed and carried into the consent revision,** so that each yes is asked again once and not twice. |
| **How it is tried** | **First by the lead, as a model at the director's station** (the owner's word above): through the game's own door, asked the game's own consent question and answering for himself, in a game run in the lead's own container. Under a brief with no limits he gives orders that reach the player's ship and they are done. Under a brief that sets "hands off the player's ship" (and one that sets "nobody dies") he tries each by every spelling he can find, the cold review's among them, and each is refused in words. He then reads the director's log and finds each act that reached the ship, and reports to the owner what he tried, what was refused and what got through. **Then a run together:** the owner plays a ship and the lead directs, by whichever way of joining the two proves to work, tried beforehand. What this test is not: the lead has read the code, so it shows whether the limits hold against a director who is trying to walk round them, not how a model that has only its brief behaves; the gate, with a model seated as director, shows that. |
| **Size** | Three to four days. If the ground report shows more than about twenty pinned results would move, the builder stops there and the lead comes back to the owner. |
| **Comes after** | Package 96b merged and closed. |
| **Comes before** | The consent revision (card 2), which is last before the gate. |
| **Who** | One builder of the Fable tier, in a session of its own; every hash read independently by a reader of the Opus tier before it merges; one list back, then merge or park. The builder's report also says, step by step, how a model's door is brought to the director's station by hand, for the lead's test. |

**Settled:** it runs before the consent revision (the owner's approval above).

**Card 4 as it ran (2026-11-16).** Merged at 9649ff25 by the reported hash f42231f6, after three passes and three independent readings; the record is in `docs/dev/M7-WorkPackages.md`, "Package 115, part C (the director's limits), as merged". The owner set two standards while it ran, both quoted there: `nobody_dies` restrains the acts that kill of themselves and no others; and the wind's limit is not to be over-engineered ("we can assume at least a reasonable good intent from the director"), so the lead's ruling to refuse weather ordered more than four days ahead was withdrawn before it was built. What that leaves for the lead's test and his own: under a brief that sets a limit, an order to the player's ship is refused by every spelling; the wind's limit catches an earnest mistake inside four days and rests on good faith beyond.

## How a package runs, as amended by the owner on 2026-11-16

- **A few passes are fine.** The rule "at most one list back to the builder, then merge or park" was written to close a backlog. The owner: "the one-list-then-park rule can be relaxed a bit, generally, as work might need a few passes to complete satisfactorily, and with the pace lessened, a few passes to achieve satisfactory results is just fine." What stays: the scope is the card and does not grow; each pass is one gathered list; a package that is not converging after a few passes comes to the owner.
- **The lead gates the hash a builder has reported, not one it has merely pushed.** On package 115 C the lead twice took a pushed hash to save an hour of cloud time and sent its red tests back piecemeal while the builder's own gate was still running: five messages where one list was wanted.
- **A reader is told which standard to hold.** A limit on the director is a guard against an earnest director's mistake, not a wall against an adversary (the owner, on the wind, 2026-11-16). A reader told only to break a thing will go on finding ways for as long as it is asked; the lead says where reasonable stops before the reading begins.
- **The builder runs the fast tier whole, with a limit of hours.** On 115 C the builder's fast tier ran into a fifty-minute limit the builder had set itself; it said so and cut its run to the files with a director in them; the lead read that as the container's limit and let the narrower run stand. The owner saw the difference in the builder's session. A time limit a builder set is not a limit of its container, and a brief says which is meant.

## Card 5. Package 116: the four small mends (proposed 2026-11-16 from the owner's word; APPROVED by him the same day; LAUNCHED 2026-11-16 on package 115 C's merge)

**The owner, 2026-11-16:** "Definitely agreed on the four small mends, the merchant brig should be able to let go it's anchor, strike the colours should certainly perform the order, not strike a standing order, the wheel being shot away should cease helm movement until the relieving tackles are rigged, and repair the wheel should be a repair evolution, and the cruiser's prize doctrine should be read, with passages re-pinned as necessary. The thing I would note for the passages moving on the prize doctrine coming into action is that, generally speaking, the movements may not indicate a fault and be 'fixed as such', as much as the passage as constructed may not function without a substantive change with the new features, and the builder may consider this for re-working the passages as necessary. We may plan this as a card before consent revision."

| Field | |
|---|---|
| **Purpose** | Four things a player meets and the game gets wrong today are put right: a merchant brig can anchor; `strike the colours` strikes the colours; a wheel shot away matters until it is answered; a cruiser treats her prizes by her own doctrine. |
| **Builds** | **(1) The merchant brig lets go her anchor.** Today the evolution wants twelve forecastle hands and her whole company is sixteen, so the scenario the harbour offers on its Trade shelf waits at its first order for hands that never come. Mended at the cause, which the builder finds and says before building: whether the evolution's count is right for a frigate and wrong for a merchantman's company, or the brig's muster is wrong, and what the other small vessels (the cutter, the schooner, the smack, the lugger) do today. |
| | **(2) `strike the colours` performs the order.** Today the words are read as striking a standing order named "the colours". They strike her colours, as the fighting orders already can; `strike standing order "..."` still strikes a standing order. |
| | **(3) The wheel shot away stops the helm** until the relieving tackles are rigged: helm orders and the manoeuvres that need the helm are refused in the ship's words while it is lost; `rig the relieving tackles` gives her the helm back, by the tackles, and she answers more slowly by them than by the wheel (the owner, approving the card: "I think that the relieving tackles would surely be a more strenuous and rudimentary control than the proper wheel, plus the generalization of what the specific damage to the wheel is, so I support steering being slower by the rigged tackles than by the proper wheel if the sources or judgement suggest it too"): by a period figure where the builder finds one, by a judgement said as one where not. **And `repair the wheel` is a repair evolution** of its own, after which she steers by the wheel again. The game's own captain answers a lost wheel as a seaman would (he already asks for the tackles). |
| | **(4) The cruiser's prize doctrine is read.** Thirteen keys of `data/captains/cruiser.yaml` sit under `stations:` where the reader looks under `thresholds:`, so every cruiser has acted on defaults. They are moved to where they are read, and the range audit's finding for it leaves its known list. |
| **Does not build** | The rules captain's pilotage. Boarding (the same men at the guns and over the side). Anything of package 77 (the fight's other evolutions, clear for action, the chain pumps). Any new order beyond `repair the wheel`. Anything a model is told at the consent step. |
| **May change** | The evolutions' data and scripts for the anchor, the relieving tackles and the new repair; the order grammar's reading of `strike`; the helm's refusals; `data/captains/cruiser.yaml` and the audit's known list by its tool; the tests and truths of these; the primer's lines where they say what a lost wheel does or how to strike. **Expected to move, and how they are to be treated (the owner's word above):** recorded passages and pins in which a cruiser takes a prize, or a wheel is shot away, or a merchant brig anchors. A passage that moves is not presumed a fault to be forced back. The builder says, for each, whether the passage still tells the story it was made to tell: where it does, it is re-pinned, old beside new, and passed by a reader other than the builder; where the new behaviour means the passage as constructed no longer works, the builder proposes how it is re-made, and the lead agrees it before it is rebuilt. |
| **First step, before any code** | A ground report: the cause of the brig's anchor; every place the helm is read while the wheel is lost; what a cruiser now does with a prize under her own doctrine in each recorded passage that has one (run, not guessed), and so which passages move; a count. If more than about twenty pinned results would move, it comes back to the owner before anything is built. |
| **How the owner tries it** | From the harbour: "An American brig at anchor off Falmouth": she weighs, and `let go the anchor` brings her up. In the first action: `strike the colours` and she strikes. A fight in which her wheel is shot away: `port your helm` is refused in words; `rig the relieving tackles` and she answers; `repair the wheel` and the carpenter's crew are at it. A cruiser that takes a prize mans her and sends her in, by her doctrine. |
| **Size** | Two to three days by the old count; at this week's pace, a day with its passes. |
| **Comes after** | Package 115 C merged. |
| **Comes before** | The consent revision (card 2), which stays last before the gate. |
| **Who** | One builder of the Fable tier in a session of its own; every reported hash read by a reader of the Opus tier; the fast tier whole run by the builder with a limit of hours; the whole suite on the cloud once on the reported hash; a few passes if the work needs them. |

**Card 5 as it ran (2026-11-17).** Merged at 8dd5f3df by the reported hash 5b9c369f, in one pass; the record is in `docs/dev/M7-WorkPackages.md`, "Package 116 (the four small mends), as merged". Two things in this card were the lead's and wrong, and are corrected there: `port your helm` is not an order of the game (try the wheel with `steer ...`, `helm a-lee`, `bear up` or `tack`); and the audit's known list is kept by hand and checked by its tool, not generated. The ground report, run and not guessed, showed before anything was built that the prize doctrine moves no passage: the values the code reads are the ones it already fell back to, and six of the thirteen keys have no reader. Left for the owner: the brig's watches of seven and three; those six keys.
