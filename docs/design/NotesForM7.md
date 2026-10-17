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
