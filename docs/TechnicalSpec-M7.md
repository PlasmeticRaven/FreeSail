# FreeSail: Technical Specification, Milestone 7 (Powder)

**Initial specification of 2026-10-23.** Drafted for the owner's review, revised the same
day on his eleven notes, and **finalised by the lead for package 70's briefing after 58a,
58b and 67 merged (decision 51)**; what those packages and 68 taught is §33a. Companion to
`docs/TechnicalSpec-M0-M2.md` through `-M7b.md`, whose conventions hold. Its sources: the proposal's M7 (`docs/
DesignProposal.md` §5.3 combat, §3.4 water, §9 the obscure kit, §11 the roadmap; decisions
7, 27, 40, 47 and 49), the owner's notes for this milestone (`docs/design/NotesForM7.md`:
fine control, taking on water, signalling and the period's signals, collision, the captain
as orchestrator, time, the combat brainstorm, temperature, sight across land), the
striking-colours study (`docs/design/Scenario-StrikingColours.md`), and what M7b's play
asked for (`docs/playtests/2026-10-18-to-22-owner-playtests-and-review/`: R-17 the voice
between ships, R-54 a chase with no good options, the pumps and the carpenter superseding
the hotfix's repair forms, the capstan's purchases and sail's thrust aground, R-39 the
weather's stacking). By decision 49 **this is an iterative milestone**: the shape is set
here, the figures are tuned in play, and the parts grow as the current packages (68, 58,
67, 55) teach us; the owner's frame is single-ship actions first, the framework open to
more ships, the command system and the signals to make more ships sane, six on six as the
ideal and never rushed. The draft is written with room left on purpose: each part names what
it waits on and what it does not yet decide. **Revised the same day on the owner's eleven
notes of the first read** (his `M7_spec_notes` of 2026-10-23), each taken into its section
and the allocation of §31 redrawn to front-load the design to Fable.

**Decision 51 (the owner, 2026-10-23):** M7b is frozen open and its remaining work wrapped up
alongside this milestone; the consent re-brief waits until testing begins in earnest; after
58a, 58b and 67 this specification is finalised and package 70 briefed.

*Proves: combat is the same system. A fight is evolutions competing for hands, damage is
state in the part graph, and the ships speak to one another by the means the period had.*

**The rules of this milestone**, beside the earlier ones (everything inward reachable by an
order or a reading; the world keeps the truth and the captain his account; a station is a
person aboard; what no model holds the rules hold; the director acts through plausible
causes):

1. **Damage is just state.** A chain shot that parts a topsail halyard has exactly the
   effect parting it by any other means has; a ball through the side is a leak the well
   knows; a man hurt is a line of the muster the surgeon reads. No second model of the
   ship exists for the fight.
2. **A gun is served by the bill.** Clearing for action, loading, running out and firing
   are evolutions with hands, ratings, fatigue and time, competing with sail work for the
   same men. The rate of fire falls out of the muster as the time to reef does.
3. **Recognition before fire.** A ship shows her true colours before she fires, or she is
   a pirate to every nation's law; the private signal, the hail and the colours are the
   means by which a captain knows whom he fights, and the game refuses nothing but tells
   the consequence.
4. **Rules first, models welcome.** Every exchange, signal, fight and surrender has a
   rules body (tables and doctrine) so that a convoy, a chase or a surrender needs no
   model; a model at a station speaks and chooses freely within it; the director shapes it.
5. **The far ships fight as the near do, coarsely.** A ship engaged within the promotion's
   range is crewed under the cap's order; a fight at far detail is resolved at coarse steps
   by the same tables, the fighting shape of the brainstorm kept as a measured fallback
   and not a plan (the owner's 95 ticks a second with twelve crewed ships is the baseline).
6. **Realism, not pacing (the owner, 2026-10-23).** Nothing is made deadlier or quicker for
   the game's sake. An action of hours is a real and legitimate outcome, and so is one of a
   quarter of an hour that ends after a single broadside and the colours struck; the
   physics, the muster and the morale decide which, never a clock of the design's.
7. **Nothing pre-defines a battle's timing.** The work of an action is continuous and
   concurrent by the quarter bill (§8a), not a queue of evolutions with fixed durations; a
   ship with hands to spare fights better because every order in hand gets done, a
   short-handed one suffers by the same, and the player gives his orders without wondering
   how they will queue.

---

## Part 7-i: Colours, signals and the voice between ships

Why first: the striking-colours study found that the encounter turns on recognition and
nothing in the plan named it; M7b's play found no voice between ships (R-17) and a chase
with no good options but to run (R-54: colours, a bluff, a fort). Everything here is
useful before a gun is fired, and the convoy's and the squadron's work needs no powder.

### 1. Colours (`freesail/world/ships.py`, `nations.py`; `data/nations/*.yaml`; the far and near bodies)

A ship's colours are state: **shown** (which ensign), **none**, **false** (another nation's,
a ruse the law allowed until the first shot), **struck** (hauled down in surrender), and the
signals of distress (the ensign union down, a gun to leeward). Orders: `hoist the colours`,
`hoist French colours` (false), `haul down the colours`, `strike` (the surrender, decision
7's rule made the captain's own word too), `fire a gun to leeward`. The lookout makes
colours out at the glass's range by their size and the light ("she shows no colours",
"British colours, the red ensign", "she has hoisted her true colours: French"); a privateer
of the business sails under false colours by her doctrine and shows her own at the range
the doctrine says. **Firing under false colours** is not refused: it is logged, every nation
treats her as a pirate thereafter (the business's stances), and the director's brief may
forbid it to the director's ships. The `hoist our colours` refusal of the vocabulary goes.

**As built (package 71; `docs/design/Design-Signals.md`).** Colours are a state of every
body (`signals.Colours`: `shown`, `none`, `false` with the nation shown, `struck`,
`distress`), one object for a far vessel and her crewed World (`Vessel.signals`, the
`Locker`) and the player's shadow's his own, so that every lookout, far and near, gives
the nation *shown* and never the true one (`Vessel.nation_shown`; the `strangers` reading's
`nation`): a French privateer under British colours is "British colours, the red ensign" to
the King's captain reading her, and the truth is the director's alone. The orders of
`orders/signals.py`: `hoist the colours`, `hoist French colours` / `hoist false colours` (the
principal enemy's), `haul down the colours` (none; under fire it is the strike, by the
custom), `hoist the ensign union down` (distress, with 70's `fire a gun to leeward`), 70's
`strike the colours` kept; the scenario's `colours: British` on a French ship is false
colours, and the director's `ship "X": order hoist false colours` the same. The lookout
says when a sail's colours shift (`colours.changed`: hoisted, hauled down, shifted). A
privateer's doctrine sails her under false colours while she closes a stranger
(`false_colours`, `true_colours_cables`, `bluff_private_signal` in `privateer.yaml`) and
every rules captain hoists his true colours before his first shot (`_engage_now`); the
player is not made to. **Recognition before fire is completed** (`action._recognition`): the
first shot under false or no colours is a pirate's act, told once (`action.false_colours`),
the ports' stance turned (`outlaw`) and every captain whose people had her in sight holding
her a pirate from then on (`pirates`, the witnesses); then the mark is judged by what his
people have made out: the colours shown against the wars, the private signal answered
wrong or not at all, the hail's words, or her own shot (`captain.recognised`, `fired_on`),
and 70's `action.unrecognised` is the exception. The refusal of the vocabulary is gone.

### 2. The private signal (`data/signals/private/*.yaml`; `freesail/world/signals.py` new; the papers)

The recognition challenge and its reply: a small table per nation per month, issued under
seal and carried as a paper of the ship's library (`papers: private_signals: <nation>
<year>`), by flags by day and by lights or false fires by night. `show the private signal`,
`answer the private signal`; the rules captain of a King's ship challenges a stranger within
the glass's range and reads the answer: right, wrong or none, which is the tell; a privateer
or a merchant has no table and cannot answer; a captured table is a paper of a prize (Part
7-v) and good until the month turns. The sources: the Admiralty's private signals as the
period's letters and orders quote them (the form, not the actual tables, which were secret
and are mostly lost); the game's tables are made, under the seed, in the period's form.

**As built (package 71).** The table is a pure function of the world's seed, the nation,
the year and the month (`signals.private_table`), drawn from the root's `private.yaml` form
(a flag at a named place answered by another with the ensign where the table says; by night
lights and a false fire): two ships of one nation in one world hold one table, a replay has
it again, and the Spanish draw is not the Dutch. It is a paper of the ship's library ("the
private signals", the captain's, in the cabin: this month's challenge and reply by day and
by night), carried by the roles the root names (`carried_by`: a King's ship, a cruiser, a
commodore) or given by the scenario's `papers: {private_signals: true}`; a merchantman, a
packet, a fisherman and a privateer have none. `show the private signal` and `answer the
private signal` are hoists of the `private` and `reply` books by the same hands. The rules
captain of a King's ship makes it to every strange sail within the flags' range once her
colours are made out (by day; the lights' range by night; never in fog, never in action,
never to a ship under his own orders), one a minute, and judges the reply against his table
from the moment his flags are up (`signalling._judge_challenges`): right makes her one of
his and a sail spoken; a reply and the wrong one is the tell whatever her colours (she tried
to pass for one of his); no answer under his own colours is the tell for a man of war's rig
and leaves a trader's rig a stranger to be spoken (a merchantman never had the table); no
answer under a neutral's colours a stranger still. A privateer whose doctrine bluffs hoists
a guessed reply. The verdict is `signal.private_judged`, urgent when it makes an enemy, and
the stranger is recognised so (`captain.recognised`), which the doctrine's `enemy made out`
reads: the encounter's frigate challenges at 10:05, her flags up at 10:11, reads the
privateer's guess wrong at 10:16 and gives chase at 10:17 (truth 7-144). A captured table is
74's prize's by the same function for the captor.

### 3. The signal books (`data/signals/*.yaml`; `signals.py`; `freesail/evolutions/` the hoist)

As the notes have them, by their own names:

- **The numerary book** (Howe's 1790; the Admiralty's *Signal Book for the Ships of War*,
  1799): numeral flags, a substitute and a preparative; a hoist is a number and the number
  an order or news in the book. Each entry is **data mapped to an intent or an order the
  rules captain understands** when the sender commands him (form the line, tack in
  succession, make more sail, chase, engage the enemy more closely, anchor, the compass and
  the numbers as qualifiers). Some two hundred entries in the first version, the rest as
  play asks.
- **The telegraphic signals** (Popham 1800, the 1803 edition): the free sentence by flags,
  word by word from the dictionary and letter by letter for a word it lacks, a minute or
  more a hoist, daylight only, repeating frigates relaying. This is what a model or the
  player writes: `make the telegraphic signal: England expects ...`.
- **Night and fog**: lanterns in their numbers and places, false fires, rockets and guns by
  the night book; guns, muskets, the bell and the drum at intervals in fog; a few dozen
  meanings.
- **Merchantmen under convoy**: the Admiralty's *Signals and Instructions for Ships under
  Convoy*: a short book (make sail, shorten sail, tack, wear, close round the commodore,
  enemy in sight, anchor).
- **The French**: du Pavillon's tables and the numerary system that followed; a research
  item before 7-i is briefed, the French book smaller and marked where made.
- **Any nation (the owner, 2026-10-23).** The British and the French are the well-built
  books; beneath them a **basic system every nation has** from the foundation (a numerary
  book of a few dozen entries in the period's common form, a private table made under the
  seed, the night and fog signals, the convoy's), so that any nation of the table may be a
  combatant in a fictional scenario (the Spanish, the Dutch, the Danes, the Americans of
  1812), and a nation's book is built out progressively from that foundation as its sources
  are found, the data shape the same for all (`data/signals/<nation>/`).

**A signal is a thing hoisted**: the book, the number, by whom, where and when, answered or
not, with the hands at the halyards and a minute a hoist (an evolution). **It is read by the
lookout**: the flags made out at the range their size and the light allow, "she makes a
signal we cannot read" without the book, a minute to look it up, the answering pennant. The
orders are by meaning (`make the signal to chase`, `make the signal: enemy in sight bearing
NW`, `answer the signal`, `repeat it`, `haul it down`), the number in the log beside the
meaning. The receiving rules captain acts by doctrine when the sender commands him (the
`squadron:` relation of Part 7-vi) and logs it otherwise; a model is given the meaning in
words and answers by meaning or by a free sentence.

**As built (package 71; `docs/design/Design-Signals.md`, the shape written first).** One
root a directory under `data/signals/`, the same six files in each: `book.yaml` (the
nation, the system, the sources, the flags, a hoist's minute, the reading's minute, the
flags' range and the glass's factor), `numerary.yaml` (the day signals, each `number`,
`meaning` and `also`, `does` what a commanded captain performs, `qualifiers`,
`in_succession`, `source`, `made`), `telegraphic.yaml` (Popham's dictionary and alphabet),
`night_fog.yaml` (the night book's lights, false fires, rockets and guns, the fog book's
guns, muskets, bell and drum, and the fog signals a ship keeps of herself), `convoy.yaml`
(the instructions to merchantmen) and `private.yaml` (the table's form). A nation names
its root and its system in `data/nations.yaml` (`signals: {root, system}`): **Britain**
well-built (150 day signals from Howe 1790 and the 1799 book, the numbers remembered kept
and the rest marked made; Popham's 1803 dictionary in a first version of 330 words numbered
to the twelve hoists of 21 October 1805, J wanting and V before U, the rest spelt; 25 night
and 16 fog signals; 32 convoy instructions), **France** well-built and smaller (70 day
signals with the Code's phrases where remembered, no dictionary, which is history's), and
**basic** the foundation every other nation stands on (46 day signals in the period's common
form, no dictionary; every entry marked made). The `does` kinds are `order` (a dialect order
with `{compass}`, `{place}` or `{number}` filled), `state`, `news`, `answer`, `closer` (the
engaging range halved: No. 16) and `release`. A signal is made by its meaning (`make the
signal to tack in succession`, `make the signal: enemy in sight bearing NW`, `make the
signal No. 16`), the book chosen by the light (the numerary by day, the night book by night,
in fog the gun fired by the battery), the convoy book when merchantmen are under the
sender's orders; `make the telegraphic signal: <the words>` is a well-built book's with a
dictionary and refused in words elsewhere. **The hoist is an evolution**
(`data/evolutions/make_signal.yaml`, three hands at the halyards, a minute a hoist, a
sentence a phase a word; it breaks out when the hands run it up and never of itself, so a
hoist queued behind a wear is not read before it is up) kept flying on the body
(`signals.Hoist`, a glass at most), **read by every lookout** once a minute at the flags'
range by day (two miles, three with the glass), the lights' at night, the gun's in fog
(`signals.read_flying`: "she makes a signal: two flags at the main", the meaning a minute
later when the ship's library holds the sender's book, "a signal we cannot read: not of our
book" when it does not, the answering pendant and the private signal by their form), and
**acted on by a rules captain under the sender's orders** (`signalling`: answered with the
pendant; obeyed by `does` through `Captain.give` on a crewed ship and `signals.far_perform`
on a far body; `in_succession` performed each when the ship before her has, three minutes
apart; `release` lets her go; **as built (package 72):** within a set the succession is by
the wake, each ship putting about where the ship ahead of her did, the interval over
the pace, and the three minutes stand only outside a set). The least relation is
`Vessel.under_orders_of` (**as built (package 72):** written by the set on every member
and cleared when she leaves; the
scenario's `under_the_orders_of`, the director's `ship "X": under the orders of <ship |
the ship | nobody>`) with the goal `in company with the ship` for a merchantman's keeping
company (the `company` leg), and a brainless vessel under orders reads by the least
captain (`signalling.brainless_minute`); the convoy of four tacks in succession on one hoist
with no model seated (truth 7-145). The player's ship obeys nobody's signals. Readings:
`the signals`, `the colours`, `the private signal`, `the lights`; the paper "the signal
book". 72's squadron replaces the relation and keeps the entries' `does`; 76 builds the
books out from the six files.

### 4. The hail, and the voice between ships (`freesail/world/hearing.py`, `orders.py`; `crews.py`; the harness)

Within hail (the four cables the lookout has) a ship is spoken by the speaking trumpet:
`hail her`, `say to the <description or name>: <words>`, and the answer comes as a line
heard on deck. **Three bodies, as the orders have:** the rules captain answers by table (what
ship, whence, whither, cargo, news, by her nation and her stance; a privateer under false
colours lying; a King's ship demanding to know who she is and bidding her heave to; the
answer in the period's words); a model at the other captain's station is given the words
in his sample and answers freely; the player types the hail and hears the answer. Between a
rules captain and a rules captain the standard exchange is written to both logs once, and
the stances read (a stranger spoken is "spoken", as the lookout already keeps). **The hail
is the first order of a search**: "heave to, I am sending a boat" by the King's ship, the
boat as 63 and 53b have it, the search a scene of the director's or the rules' doctrine
(the dispatches test's missing act). The director may voice any unheld captain within hail
(`say as the captain of the Medusa`), which is 52's rule across the water; 67's seat at a
person makes a model that captain's voice without a seat at her helm.

**As built (package 71; `world/hail.py`, `data/captains/hail.yaml`).** Within four cables
`hail her`, `hail the brig: what ship is that?` and `say to the Nancy: heave to, I am
sending a boat` speak another ship by the trumpet (beyond, refused with the cables): a line
of the speaker's log (`hail.made`), a line heard on her deck (`hail.heard`, urgent, so a
station there wakes and hears it under `heard`), and the answer by her body. **The rules
captain** answers by the table: the half-dozen questions read in the words (what ship,
whence, whither, cargo, news, the captain, the days out, heave to), each answered from her
truth by her role and nation in the period's form ("His Majesty's cutter Sherbourne. And what
ship is that?"; "The Nancy of Guernsey, from Guernsey for Falmouth, a cargo of salt"); a
privateer under false colours lies by the merchant's table under the flag she shows, with a
name and a port of that nation drawn under the seed; a demand to heave to is obeyed by a
merchantman, a packet or a fisherman not at war with a King's ship (her captain heaves to),
run from by an enemy's and by a privateer (she makes sail), declined by a King's ship. **A
model** at the hailed ship's captain's station is given the words in his sample and nothing
answers for him; he answers with his own `say to`. **The player** hears the answer on his
deck (`hail.answered`); a rules captain's hail of him (43's line) is kept for his `say to
her: ...`, and the answer's nation is read by the words (`nation_in_words`: "His Majesty's",
"of Guernsey", "the French national") and recognised to the hailer, a liar's words believed
(the private signal and the shot are the tells). Between two rules captains the standard
exchange is written once in the lookout's line (`exchange_words`), both reading the other's
nation. The hail is the first order of a search in that the heave-to is demanded and
answered; the boat and the search are the director's scene and 63's. The hailed ship is
spoken (`spoken`, both brains' `spoken_ids`).

**As fixed (the owner's playtest of 2026-10-27, folded in by package 86).** The table's
heave-to is worked only when the words demand it ("heave to", "bring to", "sending a boat"
and the rest of the table's phrases): before, every hail had the hailed ship obey or run,
and so every first exchange between two far rules captains hove one to or made her sail.
The player's own ship with no rules captain commanding (`Captain.commands`, a property that
had been called as a method, so that the table answered for him) hears the hail and keeps
it for his `say to her`; a crewed ship whose captain stands aside or holds by the
director's hand is still answered by the table, nobody else being there to answer.

### 5. The lights and the bell; sight across land (`lookout.py`; the standing orders)

A stern lantern, top lights for a squadron keeping station, the fishing boat's lantern on
her nets, merchantmen often none, by order and by the standing orders (`hoist the lights`,
`show no lights`); the bell at anchor in fog and the gun or the drum under way, as the
Regulations and the custom have them; the lookout sees a light at night as it sees a sail
by day, at the range a light carries. **Sight across land** (the owner, 2026-10-18): the
profile along the sight line sampled from the tiles' heights where the land was kept at the
cut, a ship hidden where the ground rises above the line between the lookout's eye and her
masthead, symmetric for the far ships' sightings; where the heights are unusable, any land
on the line blocks the sight. It bears on the chase and the privateer's trade, so it is
7-i's and not later.

**As built (package 71).** The lights are a state of the locker (`none`, `stern lantern`,
`top lights`; 56's lantern at the nets kept) by `hoist the lights` / `hoist a stern lantern`
/ `hoist the top lights` / `show no lights`, by the scenario's `lights:` and by the books'
signals (the convoy's "hoist their lights"); the lookout sees a far ship's light at night as
a sighting of its own ("A light two points on the bow, bearing SW") at `LIGHT_SEEN_NM`
(three miles, within the visibility) beyond the hull's loom at the mile. In fog (the
visibility under a mile) a ship keeping the fog signals (`keep the fog signals`, and the
rules captain of himself while another sail has been in sight within the hour, so that no
single ship's recorded passage moves) is heard beyond the visibility as a sighting by ear
("A bell heard in the fog on the larboard bow, bearing W": the bell at anchor within the
mile, a gun under way in company within three, the drum alone within the mile; the figures
the Regulations' and the custom's from memory, in `night_fog.yaml`'s `keeping`), and a
signal made in fog is the fog book's gun, fired by the battery and read by ear (truth
7-147). **Sight across land is not built** (78's, by the brief).

### 6. Truths for 7-i (outline)

A cutter under false colours spoken by a King's frigate answers the hail by the table and
is made out at the right range; the private signal answered wrong makes her a stranger to
the frigate's captain, who gives chase by doctrine; a convoy of four under a commodore tacks
in succession on one hoist with no model seated; a telegraphic sentence takes the hoists
and the minutes the book says; a lugger behind a headland is not seen by the cruiser
outside it; a signal made in fog is a gun and not a flag.

**As built (package 71).** Truths 7-143 to 7-151 in `tests/test_known_truths.py`, measured
at seed 7: a cutter under false colours is made out as British at the colours' range and
answers the King's frigate's hail by the table with a lie (7-143); the private signal
answered wrong makes her a stranger under false colours and the frigate gives chase by
doctrine, the encounter's figures (7-144); a convoy of four under a commodore tacks in
succession on one hoist with no model seated, each three minutes after the one ahead
(7-145; within a set the wake replaces the three minutes, truth 7-156 of package 72); Nelson's sentence takes twelve hoists and twelve minutes (7-146); a signal made in
fog is a gun, heard at three miles and read by the book (7-147); the King's cutter engaging
a privateer never puts her head within the close-hauled angle, and the first action ends an
hour after the first shot (7-148, with 7-133 re-pinned); a shot under false colours is a
pirate's act, told once, the ports turned and every witness holding her so (7-149); a light
is seen at night at the range a lantern carries and a bell heard in fog (7-150); the pace
with a convoy of four under orders and the hoists read each minute holds the floors (7-151).
The lugger behind a headland is 78's.

---

## Part 7-ii: Powder

### 7. Guns as parts (`freesail/ship/` the gun's class; `tools/gen_ships.py`; `data/ships/*.yaml`)

Guns and carronades by position (the broadside, the bow and stern chasers), each a part
with its carriage, tackles and breeching, a **load state** (empty, loaded with round, chain,
grape or double, run in or out, primed), elevation and train; the magazine and the shot
lockers as stores the purser and the gunner count (powder in cartridges by the gun's
calibre, shot by kind); the gunner, the quarter gunners and the gun crews from the muster's
posts and the quarter bill. The ship files gain their armament through the generator (the
frigate's 18-pounders and carronades, the cutter's carronades, the schooner's long guns, the
lugger's swivels, the merchant brig's few), with the sources named (the Establishments; the
*Indefatigable*'s and the privateer schooner's from their own records: Part 7-viii).

**As built (package 70).** `Gun(Part)` by place, number and side with its load state,
elevation and train (`freesail/ship/parts.py`); `GunSpec`, `FitSpec`, `ArmamentSpec` and
`QuarterBillSpec` in the schema, a ship file carrying one or several fits the scenario
chooses between (`fit:`); the magazine and the shot lockers a `Magazine` store from the
fit's figures, counted by the gunner (`the magazine`). Through the generator with the
source beside each figure: the cutter's two fits (the Admiralty's 12-pounder carronades of
1805, the hired cutters' long 3-pounders with eight swivels), the frigate (the *Amazon*
class's 18-pounders, 32-pounder carronades and 9-pounder chasers), the brig-sloop and the
merchant brig; the schooner, the lugger and the smack left to 75 with the builders in
place. The carriage, the tackles and the breeching are the gun's own state (cast loose,
run out), not parts of the graph; the figures from memory are marked UNVERIFIED in the
generator for 75's sources.

**The magazine by kind (the owner's practice and resupply, folded in by package 86).** The
magazine keeps its filled cartridges by gun kind and calibre, not by calibre alone (the
privateer schooner's long 12 had drawn on the carronades' 12-pounder cartridges), each with
its charge, and its loose powder below in barrels of a hundred pounds; the charges, the
barrels and a King's fit's monthly allowance for exercise are the fit's, through the
generator (the charges' shares UNVERIFIED until Table No. 29 is read; 75's). A store pickled
before it is converted once at the load, nothing drawn or logged. A gun's place may be
`pivot` (PROVISIONAL, the owner's ask of 2026-10-25): no side, trained round by its crew,
and bearing over either side through its own `arc_deg` from the ship file (the privateer
schooner's 60 to 140 degrees off the bow); §8's as-built note says the rest.

### 8. The gunnery as evolutions (`freesail/evolutions/`; `freesail/crew/bill.py`)

`clear for action` (the bulkheads down, the galley fire out, the boats towed or stowed, the
hands to quarters; a frigate's quarter of an hour, a cutter's five minutes), `beat to
quarters`, `cast loose the guns`, `load with round shot` (or chain, grape, double), `run out`,
`fire` (by broadside at the word, by division, **as they bear** (the period's independent
fire: the first broadside together at the word and then each gun as it is loaded and bears,
which is what the owner's "fire at will" was in 1805), a rolling broadside), **a single gun by
its number or place** (`fire the bow chaser`, `fire No. 3 gun`, `fire a shot across her
bows`: the ranging shot, the gun to leeward or to windward, the signal gun, the one shot of
a roleplay), `cease firing`, `secure the guns`; the boarders called, the small arms served
out. Each with hands, ratings
and time from the bill as sail work has them, so that a tack while the guns are being run
out is the slower for the same hands (the proposal's own example). **Rates of fire fall out
of the muster**: a full and drilled crew's broadside every minute and a half to two minutes
at the start of an action, falling with fatigue and casualties; a merchantman's few guns
served by few and untrained hands at a fraction. The figures are judgements with Douglas
(*A Treatise on Naval Gunnery*, 1820) and the period's captains' logs as the sources, pinned
by the truths and tuned in play.

**As built (package 70).** The orders of the gun deck are the dialect's (`orders/gunnery.py`,
object `gunnery`): `clear for action` (a frigate's quarter of an hour, a cutter's five
minutes, by her length), `beat to quarters` (a crew order beside `call all hands`, at once,
never queued behind the work in hand), `cast loose the guns` and `secure the guns` (the gun
crews' own work, their time from the crews at their guns), `load with ...`, `run out the
guns`, `run in the guns`, `fire as they bear`, `fire by divisions`, `hold your fire`, `fire
on the up roll`, `fire` and a side's broadside at the word, a gun by number or place, a
shot across her bows, a gun to leeward, `cease firing`; the boarders and the small arms
73's. The cycle is the battery's own and not an evolution (`combat/guns.py`: seven phases
for a long gun, 85 s nominal; a carronade's 60; a swivel's 35; the crew factor the numbers
squared, the rating, the fatigue, the seaway and the weather), so **the rates fall out of
the muster**: a frigate's 18-pounder every 104 s with her full company and every 159 s
with a quarter of each gun's crew down (truth 7-135). A gun captain fires at nothing beyond
his gun's throw. The rules captain gives them by his doctrine (§10).

**As built (practice and resupply, between packages 72 and 73).** Built locally between
packages from `docs/design/Build-PracticeAndResupply.md` and folded in by package 86 on top
of 73 (`5b01fdf`), on the
owner's rulings of 2026-10-25 (stages A and B; the Ordnance's issue to a King's ship free
and vouched, merchants and privateers paying; practice giving no skill, the drill counted
only; the galley fire out a state the needs read; ship-to-ship transfer deferred). The
magazine of §7 keeps its filled cartridges by gun kind and calibre and its loose powder
below in barrels (`ship/parts.py`; the charges, the barrels and the allowance for exercise
in the fits through the generator), and the gunner fills them from it at quarters and by
day (`combat/filling.py`), a gun with none filled of its kind waiting at the cartridge.
Powder and shot are taken in at eleven ports by the hoy, a port job with the galley fire
out while it is alongside: issued free and vouched by the Ordnance at Plymouth (in the
Sound or Cawsand Bay) and Gibraltar to a King's ship of Britain, sold by the merchants to
the rest (`world/ordnance.py`, `orders/ordnance.py`, `world/service.py`). The guns are
exercised at a cask hove over the side, at a notional mark by day, by night or in fog, and
in dumb show at the action's pace with nothing spent (`combat/marks.py`, `combat/guns.py`,
`orders/gunnery.py`, `api/practice_readings.py`). Truths 7-161 to 7-171, the first action
untouched among them (311 lines and its digest on both of the owner's trees), keep their
numbers (73's are 7-172 to 7-184). Said as built at the fold-in: a port pickled before the
port files carried their `ordnance:` block reads this build's block from its file, once and
silently (`world/ordnance.block_of`); a rules captain's fighting book opens fire on a cask
by the range reading as on a sail, by design, and nothing of the mark is an action's
(recognition, morale, the outlaw); the gunner's filling party is read and never moved, so
the fillers take no hands from other work (the build's decision 5), a stopgap that 75's or
77's brief makes real posts; the pivot gun's arc is the gun's own (`arc_deg`), a default
only where a file names none. The figures and their sources, the decisions as built, the
pins, an old game and what is left out are in the tuning notes ("Between packages 72 and
73: practice at the great guns, and powder and shot taken in", and package 86's section);
the stations' side is Harness §21g.

### 8a. The quarter bill, and work in action (the owner's note 4; `freesail/crew/bill.py` a quarter bill beside the watch bill)

At quarters every man has a station and the work is **continuous, not a queue**: the quarter
bill (data per ship file, as the watch bill is) divides the company into the gun divisions,
the sail trimmers (the afterguard and the topmen who leave the guns for a brace or a sail),
the marines, the boarders, the carpenter's crew at the wings and the pumps, the surgeon's
in the cockpit, the powder boys. A gun's service is a cycle that runs by itself while hands
and powder last; `engage her to starboard`, `fire as they bear`, `aim at her rigging` are
**standing intentions the divisions keep**, logged when they change something; the one-shot
orders (a broadside at the word, a single gun, cease firing, boarders away) ride over them.
Sail orders in action draw first on the sail trimmers and then on the guns by the fighting
book's priority (`sail before guns` or the reverse), so that a tack with the guns served is
slower by exactly the hands it takes and the player never queues a thing: he gives the
order and the bill finds the hands, saying from where. **The design of this is 70's first
item**, since the evolution system as M3 built it (an evolution with hands, a duration and
steps) serves the gun's cycle and the carpenter's plug but not the whole of an action; the
reading is that the standing-intention form the helm's `full and by` already has is the
shape, with the bill as the scheduler and the evolutions as its leaves.

**As built (package 70).** `docs/design/Design-WorkInAction.md` and `crew/quarters.py`: the
quarter bill in the ship's file beside the watch bill (through the generator with its
sources), beaten by `beat to quarters` into the gun crews (one to each pair of guns), the
trimmers, the helm, the powder, the marines, the carpenter and the surgeon; every man's
`quarters` a second assignment beside his watch, his `at` the gun's key while he is at it.
The standing intentions are the battery's (`engage her to starboard`, `load`, `aim at`,
the firing's doctrine, the roll, the ports, the priority), kept until changed and logged
when they change something; the one-shot orders ride over them. Sail work at quarters
draws on the trimmers and then on the guns by the fighting book's priority
(`Runner._rob_the_guns`): under `sail before guns` the frigate's tack takes half of every
gun's crew and keeps its pace (436 s against 447 cleared) while the guns go short; under
`guns before sail` the trimmers alone have her (642 s); the line says from where, and the
hands go back to their guns as the work is done (truth 7-136). The lead's reading held
but for the beat and the cast loose, taken another way with the reason in the tuning notes.

### 9. Shot and the hit model (`freesail/combat/` new: `shot.py`, `hits.py`)

A fired gun produces shot with a simple ballistic by calibre, charge and elevation (the
point-blank range a few hundred yards, random shot to a mile, the carronade short and
heavy) and a hit chance by range band, the roll and the aim, resolved against the target's
**part graph by the aim's doctrine**: at the rigging (the French habit: sails, spars, lines
and the men aloft), at the hull (the British: the hull, the guns, the men on the gun deck),
or between. A hit is a change of state the game already has or this milestone adds: a line
parted, a spar sprung or carried away, a sail holed (its area cut), a gun dismounted (the
part out of the bill), a shot hole at or below the waterline (a leak of Part 7-iii), a boat
stove, the wheel or the tiller ropes shot away (the helm lost until repaired), men killed
and wounded (Part 7-iv) by the men at the part struck. Grape and musketry at close range
work on the men; chain on the rigging; the double-shotted broadside at pistol shot on
everything. **Heel and the sea (the owner's note 6):** the lee battery fires lower and
shorter and the weather battery higher and longer by the heel, the gun's elevation able to
answer only so far; a lee port whose sill is within a foot of the water is shut and its gun
silent (the frigate's lower sills and the 74's lower deck in a breeze: the famous reason the
weather gage and the lee gage differ); the roll's timing is the gunner's doctrine (fire on
the up-roll for the rigging, on the down-roll for the hull) and the sea state scatters the
shot by its height. The sequence is deterministic under the seed as everything is.

**As built (package 70).** `combat/shot.py` and `combat/hits.py`: the ballistics by the
log of the calibre (point blank 250 yd for a long gun, 230 for a carronade; random shot
1,200 and 800 for the 3-pounder and the 12-pounder carronade), the hit chance by band (nine
in ten at a quarter of point blank, one in two at point blank, a fifth at twice), the
mark's size and aspect, the crew's aim and the platform's scatter; the heel added to or
taken from the quoin by the side, the lee port shut within a foot of the water, the roll
by the gunner's doctrine, the sea's height; deterministic under the seed. A hit allotted
by the aim's shares to the hull (a shot hole with its place against the waterline, the men
between decks), the deck (the men, a gun dismounted by the shot's weight against the gun's,
the wheel, a boat) or the rigging (a line shot away by the strain model's own parting, a
spar carried away, a sail holed and drawing the less), and the men killed and wounded in
the muster off the bill. The fired-at ship's log says what her people saw once a minute;
the firer's her own fall of shot; the truth both. The figures are in the tuning notes with
their sources; no water flows from the hole until 73.

**As built (package 73), the men struck.** A man the hit model strikes (`hits.hit_man`) is killed three in ten, else wounded light or grave half and half with the wound in words (`crew/health.py`, the tables of splinter and ball); the quarterdeck's people take `QUARTERDECK_SHARE` (0.2) of the hits on the after deck, 0.4 of the musketry's. The wound's draws are the health stream's, so the gunnery's stream runs as 71 left it.

### 10. The fighting instructions, the captain's engaging, and morale (`data/captains/*.yaml`; `freesail/world/captains.py`, `brains.py`; `data/standing_orders/fighting.orders`)

The rules captain's **engaging state** (present since M6, empty until now) is filled by
doctrine as data: whether he engages at all (a merchantman runs or strikes by the odds; a
privateer takes what pays and runs from a King's ship; a King's ship engages an enemy of
her class and shadows a heavier), from which side (the weather gage to engage, the lee to
escape), at what range (the British close, the French at long shot), his aim, when he
boards and when he breaks off; a **fighting book** of standing orders in the dialect
(`engage from to windward`, `aim at her rigging`, `hold your fire until she bears`, `when
she strikes, cease firing`) that the player reads and rewrites, as the starter book is the
sailing's; and **morale, the one new quantity**: the ship's company's readiness to fight on,
from the captain's doctrine, the losses, the odds, the nation's habit and the hands'
temper, which gives **striking by rule** (decision 7: the colours struck when morale fails,
said in the log with its reason) and the boarders' odds. A model captain reads his book as
the night orders and fights as he judges; the player fights his own.

**As built (package 70).** The engaging state filled by doctrine as data in every role's
file (`engage_nm`, `engage_range_cables`, `break_off_nm`, the gage, the charge, the aim,
`morale_start`, `strike_below`, each with its source), an `engaging` book in the dialect
(open fire within the range, hold at long shot, return her fire when she opens it, cease
firing when she strikes and when our own colours come down), the transitions into the
action (an enemy in range unless overmatched) and out of it (the mark struck, or none
within the breaking-off distance for its minutes; a superior force hauled off from); a new
role, the privateer (`cruise for prizes off <place>`), who engages what pays from long shot
at the rigging and runs from a man of war; the nation's habit over the role's figures (the
French at twice the range and at the rigging on the up-roll; 70's `NATION_HABITS` in the
code, moved by package 71 into each nation's `habits:` of `data/nations.yaml` beside her
colours and her signals' root, on the owner's word of 2026-10-24). The engaging helm's law
is package 71's `helm_in_action` (item 8: never within the close-hauled angle, the gage
kept, the mark through the eye answered by the doctrine's `through_the_eye`). The
captain's own on entering (the drum, the guns cast loose, loaded and laid, the mark on the
side she bears) and each minute (an equal kept on the engaged beam at his range; a weaker
mark, a smaller class or a merchantman, chased and closed to pistol shot). The
player's fighting book `data/standing_orders/fighting.orders`. **Morale is the ship's one
figure** (the division's temper has nothing to act on until 73's fight on deck), from the
doctrine's start, the losses, the guns dismounted, the masts gone and the odds under fire;
the colours come down by rule when it passes the line while under fire and a shot has told,
the log saying the reasons in figures, the battery held, the state `struck` (she lies to),
the colours a state the lookout reads; the player's `strike the colours` never refused.
What follows is 74's. The far body never takes the engaging transition (the far fight 74's;
`combat/far.py` the measure).

### 11. The marines, the small arms and the fight on deck (the owner's note 3; `freesail/crew/`; `data/ships/*.yaml` the detachment; `evolutions/`)

The marines are a division of the muster with their own officer and sergeant, **their kit by
nation and period as data** (the musket and bayonet, the sergeant's halberd or pike, the
officer's sword; the French with more soldiers and sharpshooters in the tops as their habit
was; not intensely detailed, the weapon's kind at least), their duties in the day (the
sentries at the cabin door, the spirit room and the gangway; the guard; the drill) and at
quarters (the poop and the gangways, the tops as marksmen by the captain's book, the
boarders' backbone, the guard on the prisoners). Within musket shot (a hundred yards) they
**fire at the men on a near deck** by volley or at will, the hits on the men at the parts
exposed (the quarterdeck's officers and helmsmen first, which is history's lesson), and
are fired at in turn; the ship's company's small arms (cutlasses, pikes, pistols,
tomahawks) are served out to the boarders by the bill. **The fight on deck** (a boarding
won or repulsed, a deck contested) is resolved in a few steps with cover, numbers, arms and
temper on each side and the losses written to the muster, the marines' volleys and the
guns' grape counted into it.

**As built (package 73).** The kit by nation is `data/marines.yaml` (british, french, basic: the musket, the sergeant's and the officer's arms, `volley_s` 20/30/25, `hit_at_50_yd` 0.05/0.05/0.04, `tops_share` 0.2/0.4/0.2, `tops_factor`, `soldiers`, `boarding` 1.3/1.2/1.2; the ship's company's small arms with the served and unserved factors), named from each nation's entry (`marines: {kit: ...}`, `Nations.marines_kit_of`). The detachment is the muster's `marines` station (the frigate's forty, the brig's twenty; the cutter, the schooner, the lugger, the smack and the merchant brig bear none), its lieutenant and sergeant drawn from it in the people files (`data/people/frigate-36.yaml`, `brig.yaml`; the sergeant addressed 'Sergeant X'). By day the sentries and the drill are the reading's words (`the marines`); at quarters 70's beat puts the marines at the quarterdeck carronades, and `marines, fire by volley` or `at will` takes them to their muskets (the carronades short by them) and `marines, hold your fire` sends them back; `marines to the tops` sends the kit's share aloft, `to the gangways` brings it down. The fire (`combat/small_arms.py`, each tick of `combat/action.py`) is within `MUSKET_SHOT_M` (a hundred yards) of the battery's mark when she is a near deck (a crewed vessel's or the player's; a far vessel gets nothing, 74's): a volley every `volley_s` by the detachment, or the same fire spread over the seconds at will, the hits a Poisson draw about the muskets times the chance at the range (the kit's at fifty yards, five times it at point blank, falling with the square of the range to nought at musket shot) times the roll's scatter (`1/(1 + roll/10°)`), the marksmen aloft by `tops_factor`; each hit falls on an exposed man of the mark, the quarterdeck's people two in five, the marines and the gun crews of the side that bears first; killed three in ten, the wound a musket ball in the health keeper's words. The small-arms men are the quarter bill's `small_arms` (the generator: 20/6/8/2) with the stand of arms' muskets, at will once `serve out the small arms` (an evolution of five minutes with the gunner's party) has armed the company; the boarders the bill's `boarders` (60/20/30/6, Luce's first and second boarders) with the marines. The mark's minute line says 'musketry from her deck' (or 'her tops'), the firer's the volleys and the men seen to fall; the readings `the marines`, `the small arms`, `the boarders`. The hail before the order is the drill's comma, read by the grammar (`DIVISION_HAILS`), and the captain's log says the fight's orders as done in their own words. The rules captain opens by volley within `musketry_cables` (one) and sends the marksmen aloft by the kit's habit (`marines_tops: kit`); the standing orders of the design ('at boarders then repel boarders') were taken another way, as his own minute's work.

### 11a. Boarding, and the fight at far detail (`freesail/evolutions/`; `crews.py`)

Boarding as an evolution: the ships brought together (the helm, the grapnels, the yards
locked), the boarders over by §11's fight on deck, the deck won or the boarders repulsed;
cutting out by the boats in a harbour the same with the boats (63). **At far detail**, two far ships that meet
in anger resolve their action by the same tables at coarse steps (a round of broadsides a
few minutes long, the damage summed into her far state, the striking by morale), so that
a privateer and a merchantman off the horizon come to the outcome the near fight would;
within the promotion's range the engaged ships are crewed under the cap's order, an
engagement first among the cap's reasons.

**Not built here (package 70).** §11 and §11a are 73's and 74's. The far fight is
measured once (`combat/far.py`: the same tables at coarse steps, two cutters at two cables
struck in twenty-one minutes; truth 7-139) and not wired to the far brains.

**As built (package 73), the near fight.** `lay her aboard` is the chase's helm laid on the battery's mark with the boarding's word; `grapple her` an evolution (`fight_scripts.py`: eight hands, two minutes, refused beyond `GRAPPLE_RANGE_M` thirty metres) whose grapnels hold from the throw: `extra["grappled_to"]` on both ships, the integrator holding both as the ground holds a ship, so the two lie locked (and overlap on the chart until 78's collision; said). `boarders away` (`combat/boarding.py`) sends the attacker's boarders over: the crossing's fire first (the defenders' marines' volley at point blank and the loaded guns bearing, `CROSSING_GUN_MEAN` one man each), then a round a minute while grappled, each side's strength its men times their arms (served 1.0 or unserved 0.5, the marines by the kit's `boarding`) times its temper (70's morale) times its cover (the defenders 1.3 and the boarders 0.8 in the first round), each side losing a Poisson draw about `ROUND_LOSS` (1.0) times the other's strength over ten, the fallen killed three in ten, written to the muster with the blow in words; the deck **carried** when the defenders' strength falls under `CARRIED_RATIO` (0.5) of the boarders' or their temper under its line (the colours struck by the boarders' hand, `action.strike(words="carried by boarding")`, the prize alongside for 74), the boarders **repulsed** when theirs falls so or their temper under its line (cast off, the morale's `repulses` the worse by `REPULSE_COST` 0.1), a deck **contested** past `CONTEST_ROUNDS` (15) a repulse. The defenders are the marines, the helm, the trimmers, the quarterdeck and the small-arms men, or every fit man but the powder's, the carpenter's and the surgeon's once `repel boarders` has brought the gun crews up (the guns silent); `cast off the grapnels` frees the ships (the attacker's cast-off a repulse at his own word, the defender's refused with boarders on his deck). A line a round on both logs, the readings, and the rules captain's boarding by `board_odds` and `board_when` (the chase, the grapnels within their throw, the boarders away once grappled; her boarders on his deck repelled). Measured: a hundred boarders against a frigate's whole company awake are repulsed in a round (7-180); against her at quarters with the arms served out they carry her in six (7-181). Cutting out by the boats and the fight at far detail stay 74's and the far fight's.

### 12. Truths for 7-ii (outline)

Two cutters with six carronades each, one broadside at pistol shot, the hits allotted by the
doctrine and the damage in the part graph (a halyard parted, a hole at the waterline, three
men hurt); the frigate's broadside at the start of an action in a minute and three quarters
with her full company, in three with a quarter of them casualties; a tack with the guns
run out takes longer than the same tack cleared; a merchant brig fired into by a privateer
strikes by morale when her odds fall below the doctrine's figure, the log saying why; the
same action at far detail ends the same way within a round; nothing fires under false
colours without the log saying so and every stance turning.

**As built (package 70).** Truths 7-133 to 7-142 in `tests/test_known_truths.py`, measured
at seed 7 and pinned with wide bands (rule 7): two cutters at pistol shot, one broadside at
the word and one struck (a shot hole through the side, one killed and one wounded; 7-134);
the frigate's 18-pounder every 104 s with her full company and 159 s with a quarter of each
crew down (7-135); the tack cleared 447 s, at quarters 436 s with 84 hands lent under
`sail before guns` and 642 s under `guns before sail` (7-136); the merchant brig fired into
by a privateer strikes by morale at the first shot that tells, the log saying why (7-137);
the first action at long shot from 10:13 to the colours at 12:06 (7-133) and the same two
cutters at a cable settled in three minutes (7-140); the far fight measured once and
repeatable (7-139); the pace with two crewed cutters in action 538 ticks a second (7-138);
firing on a sail not made out told and not refused (7-141); the player's strike never
refused (7-142). "Nothing fires under false colours without the log saying so" is 71's.

---

## Part 7-iii: Taking on water, and damage control

### 13. Water in the ship (`freesail/world/ground.py` or `hull.py`; `physics/hull.py`; the well)

Leaks from shot holes, from the ground, from working seams in a seaway, from heavy seas
shipped and rain with the hatches open; the water in the well as a quantity the carpenter
sounds (the hotfix's reading, kept) and a stability penalty as the free surface grows; the
**pumps** as an evolution with hands and a rate by the pump and the men (`man the pumps`,
`spell the pumps`, the chain pump and the hand pumps by the ship's file), the pumps gaining
on the leak or losing; **foundering** when the water wins (the hands to the boats, the ship
lost, the scenario's end or the director's continuation). `batten down the hatches` and the
hands kept below in a gale as the owner's note asks. The hotfix's `aboard: the leak
stopped` and `the well pumped out` are superseded by the carpenter's work and the pumps and
kept only as the director's causes with a doubt; 68's refusal line for the pumps ("not
worked in this game yet") is retired here.

**As built (package 73).** One quantity, the tons of water in the ship, kept by the World's water keeper (`freesail/world/water.py`, ticked after the chart's ground and before the navigation), its sources summed each tick: the shot holes by the orifice law (`Q = 0.6 A sqrt(2gh)`, the head from the hole's depth under the heeled waterline less the water inside), the ground's leak (`extra["leak_m_per_h"]` by the bilge's floor, afloat a third of it on soft ground), the seams working in a seaway (`0.02 t/h per 100 t × ((roll − 6°)/4)²`, trebled for a day after a grounding), the sea shipped over three metres unless the hatches are battened, and the director's seams (`leak_tons_per_h`, two tons an hour each). The well's depth is the tons over the bilge's floor (`0.45 L B`); the carpenter's feet, the hotfix's reading, are kept and read from it; the watch pumps a trickle out at the watch change unnoticed. The free surface takes from the metacentric height (`l b³/12 ∇`, applied from a tenth of a metre of depth; `Hull.gm_m` read by the equilibrium heel and the motion's particulars, the physics themselves untouched). The pumps are the ship file's (`pumps:` through the generator: the frigate two chain pumps of eighty tons an hour at four men and two hand pumps of fifteen at two, Falconer 1780; the brig one and two; the small craft hand pumps alone), a standing work of the hands' pool (`man the pumps`, `spell the pumps`, `secure the pumps`), the rate by the pump and the men's number to the power 1.5 and their skill over their fatigue and the seaway, spelled every half hour by the keeper, sucking under two inches and kept by spells while a leak other than the seams runs; the lines `well.rising` by the foot, `pumps.gaining`, `pumps.losing`, `pumps.sucked`. Foundering at half the displacement (`ship.settling` at three fifths of that), the ship held where she lies, her sails furled, `world.ship_lost`; a crewed vessel `done` with the parent's `action.enemy_sunk`; the hands to the boats are 75's. `batten down the hatches` and `open the hatches` are an evolution (ten minutes); the hands kept below is the sea's source stopped. 68's refusal of the pumps is retired; the hotfix's `aboard: the leak stopped` and `the well pumped out` act through the keeper and are doubted while the ship's own carpenter and pumps could do it (`pumps_cannot`). The rules captain mans the pumps at `pumps_at_m` (a foot) and strikes to an enemy at hand with the water past `give_up_at_share` and the pumps losing; the run for the land is the distress book's and not built here.

### 14. Damage control and jury work (`freesail/evolutions/`; `ship/parts.py` the spares)

Plugging a shot hole (the carpenter and his crew, shot plugs and oakum, the time by the
hole's place), fothering a sail over a leak, fishing a sprung spar (in the kit since M3b),
preventer braces and backstays and chain slings before an action, cutting away a mast that
has gone over the side, a jury mast from the spare spars, knotting and splicing the running
rigging under fire; each an evolution competing for hands with the guns and the sails,
which is where the fight's decisions live. The spares as the boatswain's and the
carpenter's stores, counted.

**As built (package 73).** Each a file in `data/evolutions/` with its crew line, its timing and its source, scripted in `evolutions/repair_scripts.py`, competing for hands as every evolution does: `plug_shot_hole` (the carpenter's crew to the holes worst leak first; above the water ten minutes, within half a metre under twenty from between decks, deeper forty from the hold, the ground's leak and a started seam three hours of caulking; a shot plug from the counted store, `stores.shot_plugs` 40/20/8/8/4/4/2), `fother_sail` (a sail from the sail room thrummed and hauled under: the hole's rate less `FOTHER_SHARE` 0.3 while she makes under six knots), `fish_spar` (a spar under sixty fished to seventy at most), `rig_preventers` (the preventer braces of the lower and topsail yards, the preventer backstays, the chain slings, each from the boatswain's cordage at half the line's fathoms; `Line.preventer` holds the line when the strain would part it), `set_up_rigging` (every parted shroud, backstay and stay, or the one named), `cut_away_mast` (the axes: the wreck over the side), `jury_mast` (a spare topmast in the stump, two fifths of the mast's rating, condition forty), and the owner's `reeve new lines` (every parted running line rove in turn). The damage report names everything: the lines parted (running and standing, with the order that mends each), the sprung spars, the jury masts, the holed sails, the shot holes by place and plugged or not, the well. The rules captain's repairs follow `damage_priority` (the leak, the rigging, the guns): in action the holes under water and the standing rigging, after it the running rigging rove, the spars fished.

### 15. Truths for 7-iii (outline)

A shot hole below the waterline fills the well at the rate the hole and the heel give and
the pumps hold it with so many hands and not with fewer; the carpenter plugs it in the time
the bill says; a ship that founders does so with the log saying when the pumps lost; the
grounding at Horta replayed with the pumps and the carpenter instead of the stopgap gives
the same tide and a repair that takes hands and hours.

**As built (package 73):** truths 7-172 (the orifice law and the pumps' hands), 7-173 (the carpenter's twenty minutes), 7-174 (the cutter foundered with the log's order of lines), 7-175 (the Manacles' grounding with the pumps and three hours of caulking) and 7-184 (the leak scenario, `data/scenarios/leak.yaml`).

---

## Part 7-iv: Health and the surgeon

### 16. The wounded, the sick and the dead (`freesail/crew/`; `freesail/world/needs.py`; `data/people/`)

The muster gains a state beyond "fresh" and "tired": hurt (fit for light duty), wounded
(below, the surgeon's), sick (the sick list, by the needs' ends and the ship's condition:
foul water, short allowance, cold and wet), dead (struck from the muster, buried at sea
with a line of the log). The surgeon and his mates as posts with a place (the cockpit in
action, the sick berth), their work an evolution on each man by his hurt; the needs of
M7b meet their ends here (hunger and thirst to sickness and death, fatigue to collapse) as
§20 of M7b left them; the butcher's bill in the log after an action, the sick list in the
morning report. Disease as a thing of its own (the fever of a station, the scurvy of a long
passage) is **M8's**, the hooks left.

**As built (package 73).** The muster's states are the sailor's `hurt` ('', hurt, wounded, sick, killed) with his `wound` (light, grave, invalid), the tick and the words, `dressed` and `treated`; the dead buried are struck to `Crew.dead`. The health keeper (`crew/health.py`, once a minute) works the surgeon's queue (the surgeon and his mates as posts: the grave under the surgeon half an hour each, the light under a mate ten minutes, first come first served as Turnbull 1806 has it; no surgeon borne, the messmates dress the light in an hour and the grave wait their day), the courses (the light 'hurt' and fit for light duty seven to fourteen days, half as long again untreated; the grave judged at a day, dead three in ten treated and six in ten not, else an invalid for forty days; the sick three to seven days), the day at eight (the sick list from the foul water two in a hundred a day, the short allowance past a week one, the water expended from the second day a tenth and the dead from the fourth; the burial when not at quarters, `bury the dead` by order; the morning report), the butcher's bill ten minutes after the last shot, and the needs' ends for a stationed person (thirst collapses him at three days and kills at four, hunger at a week and three; water and food bring the collapsed round). The readings `the sick list`, `the wounded`, `the surgeon`, the bill's states; the places `cockpit` and `sick berth`; the director's forms `a man taken ill`, `the fever in the ship`, `<person> is hurt`, `<person> is badly hurt`, `the surgeon taken ill`. Disease of its own stays M8's.

### 16a. A station holder hurt (the owner's note 7; the harness)

A person at a station is a valid participant: he is hit as the men at his part are (the
quarterdeck is the most exposed place in a frigate action), and his hurt comes to the
station as an urgent line of his own ("You are hit: a splinter in the thigh; you can keep
the deck, the surgeon can see you below"). **What the holder may do is the same for a model
and a human**, at parity: keep the deck (his words still carry, his orders still go, the
line in every sample saying his state), give the deck and go below to the surgeon (the
officer or the next in the bill takes it as the handover has it), or carry on hurt until
he collapses by the needs' rule for fatigue. A holder killed ends his person's station as a
death does: the harness tells the model in words, writes it in the journal and stands the
station down with the reason (no model is moved to another person by the game; a seat at
the next person is the owner's or the director's), the player at the prompt likewise loses
his person and the scenario continues by Part 7-v's roads or ends; the deck passes by the
bill. The fairness is the rules': the same hit model, the same exposure, the same choices,
whoever holds the station.

**As built (package 73).** A named person's sailor hit tells his station in an urgent line of his own with the two roads (`NeedsKeeper._tell`: the model's notice, the player's line), the muster saying 'wounded (a splinter in the hand), on deck'; on deck he is out of the surgeon's queue, a light wound dressed where he stands after an hour, a grave one collapsing him at the half hour (`holder.carried_below`: the harness's stand-by that no event or bell ends until `wound_dressed`); `go below to the surgeon` gives the deck (`_lose_deck`, the rules captain carrying on) and puts him in the cockpit and the queue, told when dressed; killed, or invalided at the surgeon's judgement, the station is stood down by the world with the reason (`agent.stopped`) and the command passes by the wardroom's order (`ship.command_passes`, `People.command_passed_to`); the player at the prompt is told the same words and loses his person, the scenario going on under whoever commands. At parity: one hit model, one exposure, one set of roads.

### 17. Truths for 7-iv (outline)

A broadside's casualties are men of the muster, named where they were named, and the gun's
crew short by them works the gun slower; the surgeon's work returns the lightly hurt to the
bill in days and not the badly; a hand dead of thirst on a passage with the water foul and
no port is a death the log explains from the needs' lines before it.

**As built (package 73):** truths 7-176 (the casualties named, the bill), 7-177 (the surgeon's returns), 7-178 (the death of thirst explained), 7-182 (the holder's roads); §11's 7-179 to 7-181 (the volley, the repulse, the deck carried) and 7-183 (the first action replayed).

---

## Part 7-v: Prizes, striking, and what follows

### 18. The prize (`freesail/world/crews.py`, `business.py`, `ports.py`; 60's mechanics from the other side)

A ship struck is possessed: her colours the captor's, a prize crew out of the captor's
muster put aboard with a prize master (a person bound to her captain's station under the
rules, or a model's seat), her people prisoners confined below or divided between the
ships, a goal that is a friendly port, the two sailing in company or parting; the prize
court the business's purse (the hull's valuation of 60, the cargo at the market, the head
money), paid at the port, shared by the period's eighths; a prize retaken by her prisoners
rising when the prize crew is thin and tired, or by a cruiser coming up; **a captured signal
book or private table a paper of the prize**. Burning or scuttling a prize not worth
manning. The far body carries a prize as a vessel with a new nation and goal.

### 19. The player struck: the captive's channel (the striking-colours study's gap 1)

The player who strikes has not lost the game: he is a person aboard the captor, with the
place and the voice M7b gave every person (53's places, 66's line, 67's seat at a person as
the shape): where he is (the great cabin, the gunroom, the hold), what he can see from
there, what he can say and to whom (`say to the captain: ...`, the parole given or refused),
his journal; the captor's captain a rules captain by doctrine (the sword returned, the
parole accepted by the period's custom, the course for his port) or a model's seat or the
director's voice; the director shaping what follows (a gale that night, a cartel in the
offing, a friendly cruiser at dawn) through plausible causes as always; **the court
martial** as the director's proceeding on the owner's note (its questions in-world through
the channel, the verdict a world order journaled), **a new command** as a scenario's start.
The continuation is what makes losing survivable; **a career** that remembers (half-pay, a
reputation, the next ship) is **M8's campaign layer**, named here so that the records keep
what it will need.

### 20. Truths for 7-v (outline)

A merchant brig taken by a privateer schooner sails for Bayonne under a prize crew of
eight with her master a prisoner in the cabin and is retaken by a frigate's boats at
anchor; the prize money paid at Falmouth by the eighths; the player struck to a model's
ship is asked for his parole in the model's words and answers in his own, the exchange in
both logs and nowhere in the operator's voice.

---

## Part 7-vi: The naval system: squadrons and regimes

### 21. The squadron (`freesail/world/squadrons.py` new; `crews.py`; `brains.py`)

One new object: a group of vessels with one commander and one goal, moved as **one brain
at far detail** with the members at formation offsets (the line ahead, the line abreast,
the order of sailing, the convoy's columns), so that a convoy, a blockading squadron and a
line of battle are one cheap thing until the player is near, when the members promote one
by one under the cap. The squadron's **standing orders are a book** like the captain's
(station keeping as a standing-order kind: "keep station two cables astern of the
flagship"; the night and fog signals; the order of sailing by the wind); a model captain at
the flagship is the orchestrator the owner saw in play, his signals the command; the
subordinate captains rules captains obeying the book and their doctrine; the `squadron:`
and `convoy:` relations beside the nations' stances, which decide whose signals command.
**A genuine set (the owner's note 8):** a squadron is a set of ships and nothing more
fixed; ships join it and leave it freely by the director's order (`squadron "Channel":
detach the Medusa`, `... join the Harpy`), by the scenario file, by the world (a ship
separated in a gale sails alone until she rejoins by signal; a prize joins her captor's
company; a convoy's straggler is lost to it), and by the commander's own signal (a division
detached in chase and recalled); a squadron may split into divisions with their own leaders
and merge again; a ship alone is a squadron of one for the brain's purposes and no object
at all for the player's. The far brain re-forms the offsets whenever the set changes.

**As built (package 72).** `freesail/world/squadrons.py`: `Squadron` (id, name, kind
`squadron | convoy`, nation, commander, members in the order of sailing, goal, formation
`line ahead | line abreast | order of sailing | close order`, interval, columns, divisions,
stragglers, rendezvous, book, regime, prizes) and the registry `Squadrons` on the World
(`world.squadrons`), ticked once a minute after the brains and before the bodies; the set
writes 71's `under_orders_of` on every member and clears it when she leaves; the formation's
slots are laid in the commander's frame (across positive to leeward, so the line turns with
the wind), and a member at far detail keeps her slot by the plan leg `("station", set)` at
the set's pace, which is the slowest member's polar under the convoy's factor and a cap
on the commander's far body (`Vessel.pace_cap_kn`); the guide dead-reckons when the
commander is on a detour. The state `in company` (every role's book; `keep your station`
every two minutes) is what a promoted member's captain is in, and the far brain's
`resolve_state` lays the station leg for it, so that the promotion under the cap keeps the
line (truth 7-155). Stragglers by the book's distance and minutes, lost beyond its
distance, separated in a gale to the rendezvous; divisions detached in chase by the signal
and recalled, their leaders' signals read by their divisions. The scenario's `squadrons:`
and a ship's `squadron:` key, the director's `squadron:` and `squadron "X": ...` forms. The
commander's book (`data/squadrons/convoy.yaml`, `squadron.yaml`, `blockade.yaml`; rules
with `on`, `signal`, `order`, `goal`, `formation`, `rearm`, `on_rearm`, `near_only`,
`repeat_minutes`) is read once a minute by the rules captain at the commodore's station,
near, crewed or far, and says nothing while a model holds the seat: the model commands by
`make the signal`. A merchantman brought to by an armed enemy with no man of war of hers
within the cover distance strikes and joins his company (`far_captures`; 74 puts the far
fight in). What is not built: the line of battle's own book (76's numbers), the squadron
shown to the player as an object of the world (the brief), the night and fog signals as a
set's standing order (the books' `lights` rule stands in).

**As fixed (the owner's playtest of 2026-10-27, folded in by package 86).** `keep station
two cables astern of the Amazon` names the player's ship by her own name as well as by `the
ship`, and `... of the frigate` a sail by her kind: the nearest of the kind among the sails
her lookout has in sight (never one only the truth knows of), read from her description and
what she is made out to be with a hyphened word whole or by its head ('brig' a merchant
brig, not a brig-sloop; 'sloop' or 'brig-sloop' the brig-sloop). The name leans on the
player's shadow and the id 'the ship', which 82 and 84 rework.

**As built (package 84, steps 1 to 6; `docs/design/Design-OneWorld.md`, "As built, steps 1
and 2" and "Step 3" to "Step 6").** The container of a promoted member is still her own World
(`crews.CrewedWorld`) until the refactor's step 6, but what a World keeps of one ship, the
player's or a member's, is a `Hull` behind the World's names (`freesail/world/hulls.py`,
`world.own`); the persons of every ship and of the shore are one registry of the world
(`world.registry`, `people.Registry`) with each person's whereabouts (`Person.hull`,
`Person.home`), a ship's company a view of it; hearing is by spot with the hull in it, so a
word ashore is heard by whoever is at that place of that port, whichever ship brought him;
and the ports are the world's (`world.ports`, `ports.Ports`: the files, the markets, a stance
toward a nation, who is found ashore) while each ship's dealings with them are hers
(`world.dealings`, `dealings.Dealings`: her pilot, her boat, her price lists, her bargains),
a promoted member's World sharing the ports and dealing with them by her own boat. A
station on a member whose hull sleeps (the far shape) works every act that wants no physics
through her own grammar (step 4; the design's §2.5): her boat's errands as jobs of the port
by the boat's time, her captain landed and fetched, the places ashore, a word said and heard
by spot, the free lines, a signal and a hail; `shape a course for <port>` lays the planner's
passage by the ports' tracks and the chart's coasting tracks, ending at her anchor in the
port; a far trader reaching her port transacts and sails again (`data/business.yaml`
`transact:`); the acceptance test of the design is truth 7-200 (`data/scenarios/tender.yaml`). A member
demoted sleeps rather than being dropped (step 5): her World is kept in the far shape with
the physics off, her company, stores, purse, parts and damage hers, the damage summed into
the far body's record, and she wakes without being remade when the cap takes her again. The
container of a member is a `Hull` of the one World since step 6 (`world.hulls`, the
`CrewedWorld` retired to the unpickler): one clock, her own log and streams, her systems
and her stations holding the hull as their world, the World's tick run with her current.
Since step 7 the player's ship is a vessel of the sea like any member (`Vessels.own`, under
`ships.PLAYER_ID`, last in the list and left out of every viewer's own sail; the shadow
retired), a hull at anchor or in port may be awake, and the cap's order is a ship in
dealings, then a hull with a stationed person, then the nearest. Since step 8 the save holds
every hull's stations (`hulls`), each input and act of a station on another ship names her
hull, and a replay gives them to her again by either road. Since step 9 the director's forms
name a hull (`aboard the Raven: ...`, a person made or come aboard her, a cutter's letter
to her), the truth walks every hull and the persons ashore, `read_log(ship=)` reads a hull's
log, and a seat may be at a person aboard any hull. Since step 10 the drivers follow a hull
(`follow "X"`, a driver's line replayed; the World's names, the snapshot, the chart and the
prompt read the followed hull, the player's own until told), the player's own hull is awake
always and the save the game's, `World.offices` stands empty beside the hulls for M8's
offices, and a world order may be given under a purview (`by`).

### 22. The regimes (`data/captains/`, `data/nations/`, `business.py`)

A ship of a nation is **in port, in ordinary, on station, on passage, in convoy or escorting,
on blockade, in chase**, each a doctrine of a few rules: a blockade keeps an inshore squadron
and an offshore one and is blown off by a westerly gale; a convoy sails at the slowest
ship's pace and its escort answers a stranger by doctrine; a ship in ordinary is a hull in
port commissioned with a delay by the business or the director; the nations differ in their
knobs (the British keep the sea and engage; the French keep port and fire high; the
privateers of any flag chase what pays; the Americans of 1812 build big and fight single
actions). The business draws them under the seed as it draws traders and fishermen (M6
§19), **and the business follows the player's ship across regions** (the owner's requirement
of 2026-10-17), the convoys and the long chases crossing the chart's blocks.

**As built (package 72).** `data/regimes.yaml` the eight regimes, each a rule in words with
its knobs and sources; `data/nations.yaml` `naval:` for every nation (keeps the sea, slips out
when blown off, convoys, the escort, the blockades, the ships in ordinary with their sorties,
the privateers' prey); `freesail/world/regimes.py` the two that are the far body's own
minute: a ship in ordinary (`Vessel.regime`, a hull at a port's anchorage with no brain,
commissioned after the regime's delay by the director's `ship "X": commissioned for
<intent>` or at once) and the sortie (her written `sortie` sailed when no enemy man of war
has been in the offing, fifteen miles of the road or the port's blockade station, for an
hour with the wind under a fresh breeze). The intent `blockade <port>` keeps the port's
blockade station (`data/ports/<port>.yaml` `blockade_station`: Brest's off the Black Rocks)
under the blockade's book, which bears the squadron up for its rendezvous in a westerly
gale and restores the station when it moderates. The business (`business.py`) draws by the
knobs: the convoys (`population.convoys`), the blockades (inshore and offshore), the ships
in ordinary; and **follows the player's ship across the regions' edge**, re-peopling a region
once on entry and carrying over a set whole while any member is within the carry-over
distance (`carry_over_nm`). Not built, left to 79: the nations' fighting habits (fire high,
single actions) as regime rules; the commission's delay drawn by the business.

**As built (package 79a).** **Every knob sourced, or said to be judgement:** each figure of
`data/regimes.yaml` and each key of the eight nations' `naval:` blocks (a `sources:` map
beside 72's `source:`) names its source by work, volume and page from the books under
`docs/references/` (James's *Naval History*, Nicolas's *Dispatches and Letters of Nelson*,
Niles' *Register*, the *Regulations and Instructions* of 1806, Falconer), or says judgement
with what was looked for; Mahan, not in the repository, is no knob's only source. **No figure
moved:** where a source gives another, it is written beside the knob ("the source gives N;
kept at M until re-measured") for the lead to rule (the commission's delay, the sortie's
wind, the convoy's size). **The commission drawn by the business:** a ship in ordinary with
no sortie, the business on, is commissioned at the business's first minute with her for an
intent of her nation's (`Business.intents_for`: a cruise on each of her doctrine's stations
within the region, `data/captains/cruiser.yaml` `stations:`, and a passage to each other port
of hers in play within it), after `commission_delay_h` drawn from the business's own stream;
said in her story and the port's news while her company is raised (`regimes.commission`, the
director's form's too), the line gone when she sails; a ship with a `sortie` keeps the sortie
rule; a ship with no intent of her nation's in the waters stays in ordinary, said in her story.
**The doctrines as data for the waters the chart has:** Britain's `blockades:` entries are a
port's id (Brest's, the book's stations, as 72 had it) or a port with its sources' dates
(`since`, `until`), its own offshore station and lee rendezvous: Rochefort (1803 to 12 July
1805, off Chassiron, Quiberon), Ferrol (from Spain's war, off Cape Prior), Cadiz (Orde's
until 9 April 1805; the frigate and brigs from 31 May, Collingwood by August; off Cadiz within
fifteen miles), Lorient (from March 1808, off Groix); France's frigates in ordinary at
Rochefort (her sortie off the Baleines) and Lorient (none: commissioned by the business),
Spain's at Ferrol (off Cape Ortegal) and Cadiz (off Cape Santa Maria). The Texel lies off the
chart and is drawn for nobody. Nothing new is drawn in the Channel's two regions, the business-on
free games' waters. **Iberia's drift** (72's second left item): Tofiño's *Derrotero* of 1789,
the pilot of the Portuguese and Galician coasts, read for the summer northerlies; no climatic
table found, so the climatology's PROVISIONAL rows stand and the item is a note in the tuning
notes (truth 7-158 stands).

**Still judgement, by knob** (79a): `in ordinary.slip_out_clear_nm` (the fifteen miles: no
distance at which the port's look-outs judged the offing clear in the books held),
`slip_out_clear_minutes` (the hour: no interval between the offing's clearing and the
weighing), `slip_out_wind_max_kn` (22 knots, kept against the sources' sorties in a fair gale
off the land), `commission_delay_h` (two to five days, kept against the Agamemnon's eleven to
thirteen weeks), `in convoy.size` (four to eight, kept against the six to 35 James and Niles
number); the blockade book's Torbay rendezvous (James gives Plymouth and Cawsand Bay; the book is
not this package's file) and its westerly gale for every port (off Cadiz an easterly drove the
squadron off); Rochefort's and Lorient's offshore stations and Rochefort's beginning; the ships
in ordinary's sortie stations; every nation's `engages`, `single_actions` and the fighting
habits (package 74's); Portugal's, Denmark's and Morocco's blocks whole; the privateers' prey
but the Americans' (Niles) and the French privateers' prizes of 1793 (Nicolas); the convoy
acts of 1798 and 1803 (named by none of the books held). Truths 7-260 to 7-269.

### 23. Truths for 7-vi (outline)

A convoy of six under a brig-sloop meets a privateer schooner: the escort makes the signal
to close round the commodore, the convoy obeys with no model seated, the privateer cuts
out the straggler by doctrine or is driven off by the odds; a blockading squadron off Brest
is blown off by a gale and the business's frigate slips out on it; the squadron keeps its
line at far detail and promotes member by member as the player closes, each in her station.

**As built (package 72):** truths 7-152 to 7-160 in `tests/test_known_truths.py` at seed 7,
each from a recorded scenario: the convoy of six keeps its order and the book signals the
straggler (7-152: the signal at 2760, up at 2866, answered at 3000, the Friendship back in
station at 5280, every ship within a cable after two hours); the privateer investigates and
evades the escort at two miles, no ship cut out since none is uncovered (7-153; the cut-out
itself is the unit test in `tests/test_squadrons.py` with a merchantman alone); the blockade
blown off Brest at 11400 and the station restored at 37920, the Hortense out at 43200
(7-154); the squadron's line within a cable at far detail and within a cable and a half
through the promotion of all three (7-155); the succession by the wake (7-156); the business
following the ship over 3° W with the convoy carried whole (7-157); the weather's bound off
in every recorded scenario (7-158); the pace at far detail against the build machine's floor
and under the cap against the crewed floor (7-159, 7-160). The owner's privateer cuts out
the straggler only when the escort is beyond the cover distance: with the King's brig in
company the convoy of six is covered, and that is the doctrine's own answer.

---

## Part 7-vii: Sea sense for action, and the fine control

### 24. Fine control of the sails (`freesail/orders/`, `evolutions/`; the `keep` prefix returned, confined)

The owner's notes: `settle the topgallant halyards` and `sway up` (the yard on the cap with
the sail set, a `settled` state at a fraction of drive and load, Luce as the source); the
vangs eased or set up to spill a gaff sail; a sail kept shivering by command; the sheets
checked or flattened by so much; the weather braces checked in a puff; the `keep <x>
<state>` prefix returned here as a held intention the crew keeps, logged when it changes
something and not every tick, the helm's `full and by` its model. The gybe as an evolution
with its time and its risk (m6a-2's note 7) completes 58b's rule that nothing shifts by the
helm. Measured by the strain truths, the speed truths and the gale trials.

### 25. Collision (`freesail/physics/`, `world/ships.py`)

Two hulls meeting have consequences judged by the closing speed and the angle: spars
carried away, a bowsprit through the other's rigging, the hull stove (a leak of 7-iii),
both ships locked until cleared (a boarding's own road), a boat lost; the lookout's and the
officer's words before a close pass, the rules captain's avoidance and the far ships' by
the rule of the road are what make it rare; the consequence is what makes keeping clear
matter. Built even if the tuning nearly removes it from play (the owner, 2026-10-17).

### 26. The cold, and the second layer of temperature

With a northern or a winter scenario: rain to snow below about 35°, spray freezing on the
rigging in a gale below the sea's freezing, the casks frozen, the watch tiring faster in the
cold; the first layer (the thermometer as a reading, fog by advection) belongs to M7b's
last package or 58 as the notes say. **Deferred within M7** until a scenario wants it.

---

## Part 7-viii: Vessels, the chart and the sources

### 27. The ships of the milestone (`data/ships/`; `tools/gen_ships.py`)

The *Indefatigable* (the razee frigate, 44, Pellew's) and the *Prince de Neufchatel* (the
privateer schooner: the owner's choice, the sources enough and the rig the more novel)
through the generator with their armament; the merchant brig of 68 given her few guns;
every existing file given its armament, its quarter bill and its marines. **And a rated
ship of the line (the owner's note 9: "dream a little big").** The lead's reading of what
the game can make and use: the part graph, the bill and the generator do not care how big
she is (the hands are numbers, the guns parts, the sails the same classes more and larger),
and the lookout's and the crewed cost grow with the number of ships, not their size; the
cost is the data and the sources. The candidate with the best sources by far is a **74 of
Slade's design**, the *Bellona* (1760; Lavery's *Anatomy of the Ship* volume gives every
deck, spar and fitting) or her near sister the *Bellerophon* as the name of 1805: the
workhorse of every fleet of the period, six hundred men, two gun decks, which is the first
true test of the lee ports and the heel of §9 and of a company large enough to fight and
sail at once (§8a). A first rate (the *Victory*, whose sources are immense) is content
rather than design once a 74 runs, and M8's unless a scenario wants her sooner. The 74 is
7-viii's third ship, built after the frigate action has proved the systems at the
frigate's scale.

### 28. The chart's next goal, and the signals' sources

The owner's question of 2026-10-17 stands open: the Mediterranean, the Great Lakes and North
America for 1812, or the Caribbean for the West Indies station; **decided by the owner's note 10
of 2026-10-23: the Mediterranean first** (the French and the Spanish and the privateers of
every flag), **then the Caribbean** with the Bermuda sloops and rigs (the famous
three-masted Bermuda-rigged vessel of the Royal Navy's West Indies station among the
ships: the owner's picture of 2026-10-23, a painting of a three-masted Bermuda sloop under
the white ensign standing out of a West Indies anchorage, each mast tall and raked with a
leg-of-mutton sail laced to it on a boom, no gaff and no topsail, a jib on a long bowsprit,
a low rakish hull; a new sail class for the generator and nothing else new, so she may come
sooner than her sea, the Royal Navy having bought the island's sloops and schooners for the
Channel's advice work too; the image to `docs/references/images/` with its source when the
owner places it), **then the full east coast of America and the Great Lakes** with their own few
vessels for 1812. The Mediterranean's block is cut when 7-i's scenarios want it, by the
chart's own tools as the Channel's and the Bay's were. The signals'
sources (the 1799 book, Popham 1803, the convoy instructions, du Pavillon) are a research
item before 7-i is briefed, each book marked verified or made.

**As built: the Channel's east block (package 79b, 2026-10-29).** Milestone 7's first chart
block, split from package 79 by the owner (79a the regimes, 79b this block, 79c and 79d the
Mediterranean west): `channel-east`, the Wight and Spithead to the Downs, Dover and Dunkirk
and the French coast from the Seine to the Flemish banks, built by `docs/dev/ChartBlocks.md`
on milestone 6's machinery; as built in spec M6 §26's list, figures in
`docs/dev/TuningNotes.md`, "Package 79b". (The brief named this section §26; the chart's
section of this spec is §28, and the pointer is here.)

---

## 29. Consent (one revision before any adversarial seat)

The striking-colours study's gap 6: the consent brief names no role in which an instance
fires into a human's ship or takes him prisoner. **Before a model is seated as an enemy
captain**, the brief is revised to say so and the question put again to every model it
would seat (the brief's own promise); 55's revision carries the M7b items (R-50, R-51) and
this one together, or M7's first package carries this alone if 55 has closed. The lead
edits no consent file; the revision is the package's. 67's seat (the API door started by
the game under the seat's budget, the consent read from the record, a person nobody holds
seated as his voice) is the mechanism every adversarial seat uses; the revision changes
what the brief says and whom the game will seat, not the door.

## 30. Gate 7 (outline), in the brainstorm's order

- **7a, single-ship action:** a frigate action with the *Indefatigable* against a French
  frigate or a privateer under a model captain, fought to a strike by rule, the damage in
  the part graph, the pumps and the surgeon at work, the prize sailed in; and the same
  action at far detail ending the same way.
- **7b, signals and the convoy:** a convoy and its escort meeting a privateer, the signals
  made and obeyed with no model seated, the hail and the private signal in the encounter,
  the lugger behind the headland unseen.
- **7c, the regimes:** a blockade kept and blown off, a ship commissioned from ordinary, the
  business following the player across a region's edge.
- **7d, six on six:** two squadrons of six at the owner's compression on the owner's
  machine, the cap raised for the scenario, measured against the 95 baseline; the fighting
  shape built only if the measure says so.
- **The player struck**, to a model's ship, and the continuation played to a cartel or a
  retaking; the director's court martial.
- The sub-gates may pass separately (decision 49: iterative); a sub-gate's report is the
  gate document's chapter.

## 31. Packages (outline; the allocation, numbered after M7b's; redrawn on the owner's note 11)

**The design to Fable first and front-loaded: five Fable packages, each setting a clear
groundwork and the first of its data, and Opus building out behind each from that baseline
and never before it.** The gate's measure and document (the six on six, the fighting shape
if wanted) are the lead's own work and no package. The numbers from 70 and provisional until
each is briefed.

| # | Who | Package | Part |
|---|---|---|---|
| 70 | Fable | **The combat core:** the quarter bill and work in action (§8a), guns as parts, the gunnery's cycle, the hit model with heel, roll and the sea, damage as state, morale and the strike, the fighting book; the first armament through the generator (the cutter and the frigate) and the first truths; the figures' sources | 7-ii |
| 71 | Fable | **Signals and the voice between ships:** colours, the private signal, the hail with its three bodies, the lights and the bell, the signal as a thing hoisted and read; the books' data shape for any nation and the first books of Britain and France (the numerary entries the convoy and the squadron need, the telegraph, night and fog, the convoy's), each mapped to the intent it means | 7-i |
| 72 | Fable | **The naval system:** the squadron as a genuine set with one brain at far detail, the formations and station keeping, the squadron's book and its signals as the command, the regimes and the nations' knobs, the business following the player's ship | 7-vi |
| 73 | Fable | **Water, damage control, health and the fight on deck:** leaks and the pumps, the carpenter's and the surgeon's work, the muster's states, the marines and the small arms, the fight on deck, a station holder hurt at parity | 7-iii, 7-iv, §11 |
| 74 | Fable | **Prizes, the strike and what follows, and the far fight:** the prize crew and the prize court, prisoners and parole, the captive's channel and the continuation, the court martial as the director's, the action at far detail by the same tables; the consent revision for adversarial seats drafted with it (or with 55) | 7-v, §11a, §29 |
| 75 | Opus | The ships: the *Indefatigable*, the *Prince de Neufchatel*, the 74; every file's armament, quarter bill and marines from 70's shape | 7-viii |
| 76 | Opus | The signal books built out from 71's baseline: the full numerary books, the private tables by month, the French book from its sources, the basic books of the other nations | 7-i |
| 77 | Opus | The gunnery's and the fight's evolutions filled out from 70 and 73: clearing for action by ship, the boarders, the small-arms drill, the damage-control catalogue (plugs, fothering, jury masts, cutting away) | 7-ii, 7-iii |
| 78 | Opus | Sight across land; collision; fine control of the sails and the gybe as an evolution | 7-i, 7-vii |
| 79 | Opus | The regimes filled out from 72: the blockade, the convoy and its escort, ordinary and commissioning, the nations' doctrines as data; the chart's Mediterranean block | 7-vi, 7-viii |
| 80 | Opus | Prizes and the continuation filled out from 74: the prize court's eighths, the cartel, retaking, the captive's places and words; the consent revision's package if 55 has closed | 7-v, §29 |

Order: 70 first and 71 after it (**one Fable package at a time**, the owner's rule of
2026-10-23, so that he can meter the week's usage; the combat core and then the voice
between ships, which M7b's play wants now), 72 and 73 behind them, 74 when 70 has shown the strike; 75 as soon
as 70's shape of a gun is settled, 76 behind 71, 77 behind 70 and 73, 78 where the sailing
wants it, 79 behind 72, 80 behind 74. The sub-gates of §30 fall out of that order: 7a after
70, 73, 75 and 77; 7b after 71, 76 and 72's first half; 7c after 79; 7d the lead's measure.
The weather's stacking and seasonal bound (R-39) and the land-avoiding planner (M7b's 61)
are carried in and placed when 72 shows where the squadrons want them.

## 32. What this milestone does not do

The campaign layer (a career, half-pay, reputation: M8); disease as its own system (M8);
fleet actions beyond six on six; the Lakes or any new chart block before the gate's
scenarios choose one; a three-dimensional ship or a damage picture beyond the viewer's
present honesty (M8's ship view draws the state as it is); the boats as fighting vessels
beyond cutting out (63 first); a full terrain chart (sight across land by the tiles' heights
first).

## 33. Open items carried in from M7b

R-17 and R-54 (7-i); the pumps, the carpenter and the capstan's purchases (7-iii); sail's
thrust aground and the kedge's heave-taut (7-iii with 63); R-39 the weather's stacking and
the climatology's drift (placed with 72); the land-avoiding planner (61, placed with 72 or
78); the boat as a vessel and towing (63, before 77's cutting out); the place's knowledge
(65, with the hail: who perceives what); the harbour's second pass (64, the owner's Fable
run, when he likes); the cold (26); the thermometer's first layer (deferred with §26); the
lay line (43b, with 79's convoys beating); the Windows pins (69, before the gate); the
lead's playtest of 58b's gale book and the owner's decisions listed in 58a's, 58b's and
67's as-merged records (`docs/dev/M7b-WorkPackages.md`).

### 33a. What the last packages of M7b taught (2026-10-23)

Read before 70 was briefed, as §34 asked. **58a** (the deltas, the tripwires, the dry run):
a station's sample carries a part only when it changed, so an action's state (the guns,
the damage, the casualties) comes to a station as one line when it changes and not as a
table every sample; `stand_by(until=...)`'s tripwires, judged by the readings and never by
prose, are the form for the action's events (she opens fire, a shot strikes, her colours
come down, a sail within so many cables); the "n minutes since your last reply" line is
what a model fights against, and an action's samples must stay small enough that a
model's thinking does not cost it a broadside; the director's `WORLD_ORDER_FORMS`, every
example performed by a test, is the shape for the director's forms in action. **58b**
(the captain's sea sense): the rules captain's books are written again at each
transition and must leave out what another hand holds (the leg under the pilot's conn),
which is the rule for the engaging book too (the sailing's book yields what the fighting
book takes: the helm to the engaging's side and range, the sails to the bill's priority);
the gale book lies her to without being taken aback, so a ship beaten in a blow and a ship
beaten in action are different states and not one; a physics figure is not changed by a
package that was told to leave it (the lug's two thirds kept), and the hit model reads
the heel, the roll and the sea from the physics as they are. **67** (the seats): a model is
seated through the API door under the seat's budget and folded at two fifths of its
context, so an action's samples are the fold's enemy; a person nobody holds can be seated
as his voice, which is how an enemy captain speaks under a model when §29's revision
allows it; the `director:` channel is where the owner steers an action out of character.
**68** (the review's mending): the director's hand reaches the ship's state only by the
table's plausible causes (`aboard: the fore topmast is found sprung`), and a hit of §9 is
the same state change by another cause; the pumps' refusal line ("not worked in this game
yet") is retired by 73, the director's `aboard: the well pumped out` kept as his cause;
the deck's wait and cut call bound how long a station may think, which an action makes
sharper; riding and the helm's held courses are the ship's own rules and an engaged ship
keeps them.

## 34. What this draft does not yet decide

The hit model's exact bands and the rates' figures (70's, with their sources); whether
morale is a ship's figure or each division's; whether the far fight is a table or the near
model at coarse steps (70 measures both); the signal books' extent in the first version;
how a model at the flagship gives a signal (a tool, or `make the signal` as an order:
the order, by the equal-reach rule, unless play says otherwise); how prisoners are counted
(people or numbers: numbers but for the named); the chart's next block; the marines' kit tables by nation (73 names the shape, 75 the data); and what the later
packages teach (58a's, 58b's, 67's and 68's lessons are §33a's).
