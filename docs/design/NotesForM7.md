# Notes for milestone 7: details the owner wants kept

Design details noted during milestone 6 for the milestones that follow, each with its
date and its ground, so that the specification of M7 (powder) and M7b (the director) can
pick them up. Not open items of M6: nothing here waits on a package of this milestone.

## Sail handling at fine control (M7, a "fine-control" sub-module)

The owner, 2026-10-10, on the aquatint of the Nimble cutter in chase
(`docs/references/images/cutter-nimble-in-chace-aquatint.webp`) and in conversation with
the lead:

1. **Settling the halyards.** The nearer cutter's topgallant yard is run down with the
   sail left set and billowing: the squall's first order in Luce 1866 ch. XXVI, "settle
   down the top-gallant sails and royals, or clew them up". The game has the yard's hoist
   as a transient of `set`, `take in`, `reef` and `shake out` (the `hoist`, `settle
   halyards` and `clew down` steps; the yard on the cap during a reef; drawn at its hoist
   since 37n) and no held state: an order `settle the topgallant halyards` (a mast's by
   name; `settle the topgallants` for all; the cutter's one), the yard on the cap with the
   sail set and sheeted, a `settled` sail state with its drive and its load cut to a
   fraction (judgement, Luce as the source, the strain truth the check), `hoist the
   topgallant yards` or `sway up` to restore; the books' storm lines using it as the step
   before clewing up. Left out of 37p by the owner's word; a detail for M7.
2. **Fine control of the sails for speed and spill.** The vangs eased or set up to control
   how a gaff sail spills; a sail kept shivering by command ("keep the mizzen topsail
   shivering", as Luce's tacking has it for the main and mizzen topsails); the sheets
   checked or flattened by so much; the weather braces checked a little in a puff. The
   `keep <x> <state>` prefix struck from 37o (decision 39's playtest notes) may return
   here, confined to a fine-control sub-module where a held intention for a sail or a
   yard is the thing wanted, with the helm's `full and by` as its model (an intention the
   crew keeps, logged when it changes something and not every tick).

The measure for both, when they come: the strain truths (a sail settled or shivering
carries less than one drawing), the speed truths (a sail spilled slows her by what it
should), and the gale trials of package 40c under 37p's trim.

## Taking on water (M7)

The owner, 2026-10-11, on gate m6a's gale runs (his note 3b): water taken by damage, by
heeling with heavy seas and rain, foundering, battening down the hatches, the pumps and
the hands at them; a sea-keeping thread of its own beside the powder's milestone.

## From gate m6a-2's runs (the owner, 2026-10-13 to 15; the lead's routing in `docs/dev/M6-WorkPackages.md`)

- **The gybe as an evolution, and sails that do not flip** (note 7): a fore-and-aft sail
  sheeted out and filled from aft is not gybed by a wind that backs a point; the gybe takes
  its time and carries its risk, as the tack does; the lugger's dipping lug is the same
  thread; the viewer shows it. With the halyards and the vangs above, M7's fine control.
- **Provisions, water, hunger, thirst and fatigue** (notes 8 and 13): the crew eat and drink
  on the schedule as they rest; named people and the player have the three needs in three
  to five steps with notable then urgent lines to the person stationed, eased by eating,
  drinking and sleeping below (at a place with food, or the shore); tied to health and the
  surgeon; death by hunger or thirst, collapse by fatigue; the master's "stand by, asleep
  below until called"; once a day to eat and drink, a sleep every day or two; automatic
  where nobody is seated, by hand at a filled station to begin with. Not busywork.
- **People moving between places; books drafted; the papers kept in a place; locational
  knowledge; the journal with the person** (notes 9, 21, 22): the director's milestone's
  immersion thread.
- **Signals, and a hail syntax between captains** (note 19): with combat.
- **The viewer's layering and lighting** (note 6): later.

## The vessels and the chart of milestone 7 (the owner, 2026-10-17)

- **Vessels:** the *Indefatigable* (the razee frigate), and a privateer schooner, either the
  *Grecian* or the *Prince de Neufchatel* (alike in rig and dimensions; the one with the
  better sources), to fill the ship list with combat-ready vessels for powder.
- **The lugger's balance** (43b): the masts scaled on her breadth by Forfait's column, the
  hull's lateral centre moved a metre aft to balance her; the owner may go to a mix of mast
  rake and the mizzen's place after sailing her, or keep the rake and the mizzen where a
  source has them and move the lateral centre instead.
- **The lay line** for the captain's beating (the lugger on the regatta's crossing tacked
  sixty-one times and never passed a sea-route mark); **Roscoff's and St Mary's tracks**
  re-pricked for far detail so the business may use them: the next milestone's captain's
  and chart packages, unless testing shows them seriously wanting.
- **The chart's next goal:** the owner's question of 2026-10-17 (the Mediterranean, or the
  Great Lakes and North America for 1812, or the Caribbean for the West Indies station); the
  lead's opinion in the conversation of that day.

## The world's business beyond one region, and fishing for the player (the owner and the lead, 2026-10-17)

- **The business follows the player's ship.** Package 43b draws the business within the
  region the scenario starts in. The owner's requirement: the draw tracks the player's ship
  (or the followed ship) so that a passage into a new region finds new business about her;
  and, to consider, a low-level simulation in every region so that a region entered is
  already peopled; and any kind of ship passing between regions or routed to distant ports
  and places in other regions. M7's design point: combat wants long-distance chases,
  convoys, war and actions, and long-distance trading and intents. At the least, the
  business's region tracks where the player's ship is.
- **Fishing is a far-detail behaviour only** in m6c: a smack or a lugger of the business is
  given the `fish` intent (a ground from the coast's features at the right depth, so many
  hours on it, home again), by the fisherman's doctrine, never crewed; no catch is modelled
  (she carries nothing home, the ports' pilchards are the market's own) and the player at
  the smack's helm has no order to fish, no gear and no hold filling. For the player to fish
  as the business does: an evolution (the nets or the lines shot and hauled, hours on the
  ground, the hands at it), a catch into the hold by the ground, the season and the hours,
  sold at a port that buys fish, and the far-detail fisherman given the same catch so the
  two bodies agree. The owner, 2026-10-17: an M7b package (56, `docs/TechnicalSpec-M7b.md` §21a), with the glass on a near ship (§21b).

## Signalling, and how ships speak at any range (the owner's question of 2026-10-17; the lead's impression)

The owner: for any ship the basic lights and the bell for night and fog; the private signals
of at least Britain and France where period sources give them; hailing at close range built
with basic function for no model while free when a model holds either or both roles; the
different cases considered before building, and how many covered without a model on the
actor's or the director's side. The lead's impression, for the specification of M7:

- **Channels by medium and range, each a thing the ship models:** the **hail** by the
  speaking trumpet within hail (the existing four cables), words; the **colours** (shown,
  struck, false: M7's); the **private signal**, the recognition challenge and its reply, by
  flags by day as far as flags are made out and by lights or false fires by night, a table
  per nation changed by the month and carried as a paper; the **signal book**, a numerary
  vocabulary of orders and news to a consort or a convoy by day (Popham's telegraphic
  signals of 1803 and the Admiralty's signal book of 1799; the French *Signaux de jour et de
  nuit* and du Pavillon's tables; the convoy instructions for merchantmen), a small set by
  night (lights, false fires, rockets, guns) and in fog (guns, the bell, the drum or horn at
  intervals); **the lights** carried by order (a stern lantern, top lights for a squadron
  keeping station, the fishing boat's lantern on her nets, merchantmen often none) and the
  **bell** at anchor in fog, as the custom and the Regulations have them (Falconer, Lever,
  the Regulations and Instructions; the sources verified or marked).
- **Three bodies for each channel, as the orders have:** the rules answer by tables (a
  rules-based captain answers a hail with the standard exchange: what ship, whence, whither,
  cargo, news, by her nation and her stance, a privateer under false colours lying; answers
  the private signal rightly if her papers hold it and wrongly or not at all if not, which
  is the tell; makes and answers the convoy's and the squadron's signals; fires the gun to
  leeward and hoists the ensign union down in distress; keeps the fog signals and the
  lights by the standing orders); a model speaks free words in a hail and chooses a signal
  from the book's vocabulary by a tool; the player types the hail, `make the signal <number
  or its meaning>`, `show the private signal`, `answer the private signal`, `hoist the
  lights`, `ring the bell`. The director may put words in any unheld mouth (`say as`).
- **Perception is the lookout's:** a signal is seen under the same visibility, range and
  daylight as a sail, misread at the edge of range, "she makes a signal we cannot read"
  without the book; the signal book and the month's private signals are papers in the
  ship's library (a captured book is a thing of M7's prizes).
- **Without a model**, the rules cover: the standard hail's half-dozen questions and their
  answers; the challenge and reply; some thirty signals of the convoy and the squadron
  (make sail, shorten sail, tack, wear, close round the commodore, enemy in sight bearing so,
  chase, recall, anchor); distress; the fog signals and the lights by the book. A model is
  wanted only for talk beyond the standard exchange, and the director only to shape it.
- **The cases to consider before building:** rules to rules (two far-detail or crewed
  captains meeting: the exchange written to the log once, the stances read); rules to the
  player; player to a model; model to model; a convoy under a commodore with the player in
  it or over it; a chase with false colours and the private signal unanswered; night and
  fog with no flags; a signal made to a ship beyond hail and the time it takes to read and
  answer; what the far body can do (make and answer by table) against the crewed one.

### The period's signals, named rightly (the lead, 2026-10-17, on the owner's intent)

The owner's intent: a squadron's commander hoisting a message to his consorts ("England
expects that every man will do his duty") and the basic commands by which the naval work of
the period was conducted, so that intent passes by signal between most ships. The period's
systems, which the design should model by their own names:

- **The numerary signal book** (Howe's of 1790, the Admiralty's *Signal Book for the Ships
  of War* of 1799): ten numeral flags with a substitute and a preparative; a hoist is a
  number, and the number is an order or a piece of news in the book, some four hundred of
  them: form the line, tack in succession, make more sail, chase, engage the enemy more
  closely (No. 16), anchor, the compass and the number flags as qualifiers. **This is the
  working language of a squadron and the one the rules can act on**: each entry maps to an
  intent or an order the rules-based captain understands when the sender commands him.
- **The telegraphic signals** (Popham's *Telegraphic Signals, or Marine Vocabulary*, 1800,
  the 1803 edition at Trafalgar): with the telegraph flag up, the numbers refer to a
  dictionary of words and phrases, so any sentence is spelt word by word and, for a word the
  book lacks, letter by letter ("expects" was in the book and "confides" was not; "duty" was
  spelt). Twelve hoists for Nelson's sentence, a minute or more a hoist to make, as long to
  read and repeat, the repeating frigates relaying down the line. **This is the free
  sentence by flags**, slow and for daylight, and the one a model or the player writes.
- **The private signals** are the recognition signals only: a challenge and its reply,
  issued under seal and changed by the month, by flags by day and by lights or false fires
  by night; the answer wrong or wanting is the tell that she is an enemy. A small table per
  nation per month, kept as a paper.
- **Night and fog**: lanterns in their numbers and places, false fires, rockets and guns by
  the night signal book; guns, muskets, the bell and the drum at intervals in fog; a few
  dozen meanings, not a vocabulary.
- **Merchantmen under convoy**: the Admiralty's *Signals and Instructions for Ships under
  Convoy*, a short book of its own (make sail, shorten sail, tack, wear, close round the
  commodore, enemy in sight, anchor); Marryat's code is 1817 and too late.
- **The French**: du Pavillon's *Tableau des signaux* and the numerary system that followed
  it, on Gallica; a research spree to find the editions before M7 is specified.

**How the design would take them:** a signal as a thing hoisted (the book, the numbers, by
whom, where, when, answered or not); the books as data with their sources
(`data/signals/`), each numerary entry mapped to the intent or order it means; orders by
meaning rather than number (`make the signal to chase`, `make the telegraphic signal:
England expects ...`, `answer the signal`, `repeat it`, `haul it down`), the hoisting an
evolution with the hands at the halyards and a minute a hoist; reading at the other end by
the lookout's sight of the flags (range by their size, the light and the glass), the book
aboard, and a minute to look it up, the answering pennant shown; the receiving rules
captain acting by doctrine when the sender commands him (a `squadron:` or `convoy:`
relation beside the nations' stances) and logging it otherwise; a model given the meaning
in words and answering by meaning or by a free sentence; the private signals a separate
table; night and fog their own small books. Nothing of this needs a model for the squadron's
and the convoy's ordinary work.

## Ship collision (the owner, 2026-10-17)

Noted while passing close by other ships in the gate 6c runs: two ships touching has no
consequence today. For M7's consideration: a collision between the player's ship and
another (or two crewed ships) has consequences, probably disastrous (spars carried away, a
bowsprit through the other's rigging, the hull stove, both ships locked until cleared, a
boat lost), judged by the closing speed and the angle; worth building even if the tuning
nearly removes it from play. The lookout's and the officer's words before a close pass,
the rules captain's avoidance and the far ships' are the parts that make it rare; the
consequence is what makes keeping clear matter.

## The captain as orchestrator (the owner, 2026-10-17, after the Éclair's first cruise)

The owner's observation from play: a good model captain with a lesser model as officer
acts as an orchestrator by nature, giving the deck and the ordinary work to the officer and
keeping the decisions; "a ship is basically a natural agentic harness". The cruise's
usage: the lead's model at the officer's station for a day and a night of ship's time
cost a few per cent of the plan's allowance, so the heavy models are for the captain's and
the director's stations and a lesser model does the officer's busywork well. For the
allocation of models to stations in the harbour's settings (59) and the gate's scenarios
(55): the captain and the director heavy, the officer, lookout and master light.

## Two harness notes from the Éclair's first cruise (the owner and the lead, 2026-10-17)

- **A turn left open under lockstep.** The lead's door sent a stand-by the game refused
  (a wait for the pilot aboard with no sail in sight), did not read the refusal, and polled
  for a turn that could not come while it held the floor; under `--lockstep` the clock
  froze until the owner intervened. The door's fault first (the bridge returns a refused
  stand-by as the call's result, which a model reads); but the harness could say it louder:
  a refused stand-by is a notice at the head of the answer, and the turn's state ("the
  floor is still yours") is in every answer's words. Lockstep itself was not needed: the
  pace rule's default (1x while a sample is open) would have served and cannot freeze.
  The owner wants a run without lockstep to see.
- **Narration for action.** The owner's standing observation: a model says "I'll do x and
  y right away" and ends its turn with no call. The harness counts three empty replies
  before a question or an urgent line; a smaller nudge catches it sooner: a reply with words
  of intent and no call gets, in the next sample, "you said you would set the lugs; nothing
  was ordered". For 58 or the harness's own notes.

## Time, and being cut off (the owner and the lead, 2026-10-17)

The owner: playing without lockstep is "the closest you'll get to experiencing time", since
the ship sails on while the model thinks and the next sample brings what it missed; a true
time sim would stream every tick's lines to the model mid-thought, but that is probably
wasteful and overwhelming. The lead: nothing reaches an API model mid-reply, but the thing
wanted is the interruption, not the stream, and the local runner could have it cheaply: a
reply generated as a stream is stopped when an urgent line arrives, the half-reply dropped
and the model asked again with the line at the top, as a shout from the deck cuts an
officer off. A few lines in the runner, nothing in the game; the API doors keep the wake at
the boundary as now. Every tick's lines would be the opposite of time: the log already does
the editing a mind does. A thought for the local runner, not a package.

## Combat and the naval system: the lead's brainstorm (the owner's ask, 2026-10-17)

The owner's frame: the combat system in general; the naval system's regimes (in port, on
station, convoys, escorts, blockades, in and out of ordinary); how far beyond single-ship
actions is feasible; a six-on-six action as the ideal, tuned and not rushed; single-ship
actions first, the framework allowing more ships, with the command system and signalling
to make it realistic and sane. The lead's input, for the M7 design:

**Single-ship action is mostly things the game has.** The sailing model is the hard part of
a sea fight and exists; combat adds a decision layer and four systems. (1) Gunnery as an
evolution: the guns served by the bill like any work, numbers, skill and fatigue giving the
rate of fire as they give the time to reef; aim a doctrine choice, hull or rigging, which is
the national difference in one knob; range bands for the hit chances; powder and shot as
stores the purser counts. (2) Damage into what exists: the part graph carries a sprung spar
and a parted line, so shot into the rigging is damage the game knows; shot into the hull is
taking on water (above); shot into men is the muster, so health and the surgeon come with
combat, not after. (3) Boarding as an evolution with odds from numbers and temper; striking
as a morale rule, morale the one new quantity (the captain's doctrine, his losses, his odds,
the nation's habits). (4) The prize: a crewed ship given a prize crew out of the muster and
a goal that is a port; the prize court the business's purse; most of it 60's ship-bought
mechanics from the other side; a captured signal book a paper of the prize.

**The naval system is squadrons and regimes at far detail.** One new object, the squadron:
a group of vessels with one commander and one goal, moved as one brain at far detail with
the members at formation offsets, so that a convoy, a blockading squadron and a line of
battle are one cheap thing until the player is near, when members promote one by one under
the cap. One new idea, the regimes: a ship of a nation is in port, in ordinary, on station,
on passage, in convoy or escorting, on blockade, each a doctrine of a few rules (a blockade
keeps an inshore squadron and an offshore one and is blown off by a westerly gale; a convoy
sails at the slowest ship's pace and its escort answers a stranger by doctrine; a ship in
ordinary is a hull in port commissioned with a delay by the business or the director). The
nations differ in their knobs: the British keep the sea and engage; the French keep port and
fire high; privateers of any flag chase what pays. The signal book is the command system
(the signalling note above): a squadron's standing orders are a book like the captain's; a
signal is a world event with a reading delay, a visibility and an acknowledgement;
subordinate captains are rules captains obeying the squadron's book and their doctrine; a
model captain at the flagship is the orchestrator the owner saw in play; station keeping is
a standing-order kind ("keep station two cables astern of the flagship"); the formations
(line ahead, line abreast, the order of sailing) are the book's.

**Six on six is a tuning problem, and the lead's first reading was too dark.** The owner's
figure (2026-10-17): the frigate with twelve crewed ships runs at 95 ticks a second on his
machine, a tick a second of ship's time, so twelve crewed Worlds run at 95x there with
nothing to spare and at 30x with plenty, and a battle wants 1x to 5x. So no third shape is
needed for the target. Two cautions: combat adds cost per ship (the guns served, the damage
worked, each rules captain thinking harder and oftener, every crewed lookout watching
eleven others, which grows with the square of the number), so a fighting ship at five times
a sailing one turns 95 into 19, still above the five a battle wants; and the cap is a budget
knob (`--crewed-cap`, `tools/pace.py --ships N`), raised for a battle's scenario and kept at
three on the open sea. A *fighting shape* (the motion model, the guns, the damage and the
sail state at coarse steps, without the reckoning, the log and the people) stays as a
fallback if the measured cost of combat breaks the figure, not a plan. Measured as combat
lands, the owner's 95 the baseline.

**The order to build it:** M7a single-ship action (gunnery, damage, boarding, striking, the
prize, health and the surgeon), gated on a frigate action (the Indefatigable); M7b
signalling and the squadron primitives (the group, station keeping, the signal book, the
acknowledgement), gated on a convoy and its escort meeting a privateer; M7c the regimes and
the nations' doctrines (stations, blockade, convoy, ordinary); M7d the fighting shape and
the six on six, tuned on the owner's machine, never rushed.

