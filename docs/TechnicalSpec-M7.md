# FreeSail: Technical Specification, Milestone 7 (Powder)

**Initial draft of 2026-10-23 for the owner's review.** Companion to `docs/TechnicalSpec-M0-M2.md`
through `-M7b.md`, whose conventions hold. Its sources: the proposal's M7 (`docs/
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
it waits on and what it does not yet decide.

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

**A signal is a thing hoisted**: the book, the number, by whom, where and when, answered or
not, with the hands at the halyards and a minute a hoist (an evolution). **It is read by the
lookout**: the flags made out at the range their size and the light allow, "she makes a
signal we cannot read" without the book, a minute to look it up, the answering pennant. The
orders are by meaning (`make the signal to chase`, `make the signal: enemy in sight bearing
NW`, `answer the signal`, `repeat it`, `haul it down`), the number in the log beside the
meaning. The receiving rules captain acts by doctrine when the sender commands him (the
`squadron:` relation of Part 7-vi) and logs it otherwise; a model is given the meaning in
words and answers by meaning or by a free sentence.

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

### 6. Truths for 7-i (outline)

A cutter under false colours spoken by a King's frigate answers the hail by the table and
is made out at the right range; the private signal answered wrong makes her a stranger to
the frigate's captain, who gives chase by doctrine; a convoy of four under a commodore tacks
in succession on one hoist with no model seated; a telegraphic sentence takes the hoists
and the minutes the book says; a lugger behind a headland is not seen by the cruiser
outside it; a signal made in fog is a gun and not a flag.

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

### 8. The gunnery as evolutions (`freesail/evolutions/`; `freesail/crew/bill.py`)

`clear for action` (the bulkheads down, the galley fire out, the boats towed or stowed, the
hands to quarters; a frigate's quarter of an hour, a cutter's five minutes), `beat to
quarters`, `cast loose the guns`, `load with round shot` (or chain, grape, double), `run out`,
`fire` (by broadside, by division, as they bear, a rolling broadside), `cease firing`,
`secure the guns`; the boarders called, the small arms served out. Each with hands, ratings
and time from the bill as sail work has them, so that a tack while the guns are being run
out is the slower for the same hands (the proposal's own example). **Rates of fire fall out
of the muster**: a full and drilled crew's broadside every minute and a half to two minutes
at the start of an action, falling with fatigue and casualties; a merchantman's few guns
served by few and untrained hands at a fraction. The figures are judgements with Douglas
(*A Treatise on Naval Gunnery*, 1820) and the period's captains' logs as the sources, pinned
by the truths and tuned in play.

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
everything. The sequence is deterministic under the seed as everything is.

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

### 11. Boarding, and the fight at far detail (`freesail/evolutions/`; `crews.py`)

Boarding as an evolution: the ships brought together (the helm, the grapnels, the yards
locked), the boarders over by the odds of numbers, arms and temper, resolved in a few steps
with losses on both sides and the deck won or the boarders repulsed; cutting out by the
boats in a harbour the same with the boats (63). **At far detail**, two far ships that meet
in anger resolve their action by the same tables at coarse steps (a round of broadsides a
few minutes long, the damage summed into her far state, the striking by morale), so that
a privateer and a merchantman off the horizon come to the outcome the near fight would;
within the promotion's range the engaged ships are crewed under the cap's order, an
engagement first among the cap's reasons.

### 12. Truths for 7-ii (outline)

Two cutters with six carronades each, one broadside at pistol shot, the hits allotted by the
doctrine and the damage in the part graph (a halyard parted, a hole at the waterline, three
men hurt); the frigate's broadside at the start of an action in a minute and three quarters
with her full company, in three with a quarter of them casualties; a tack with the guns
run out takes longer than the same tack cleared; a merchant brig fired into by a privateer
strikes by morale when her odds fall below the doctrine's figure, the log saying why; the
same action at far detail ends the same way within a round; nothing fires under false
colours without the log saying so and every stance turning.

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
kept only as the director's causes with a doubt.

### 14. Damage control and jury work (`freesail/evolutions/`; `ship/parts.py` the spares)

Plugging a shot hole (the carpenter and his crew, shot plugs and oakum, the time by the
hole's place), fothering a sail over a leak, fishing a sprung spar (in the kit since M3b),
preventer braces and backstays and chain slings before an action, cutting away a mast that
has gone over the side, a jury mast from the spare spars, knotting and splicing the running
rigging under fire; each an evolution competing for hands with the guns and the sails,
which is where the fight's decisions live. The spares as the boatswain's and the
carpenter's stores, counted.

### 15. Truths for 7-iii (outline)

A shot hole below the waterline fills the well at the rate the hole and the heel give and
the pumps hold it with so many hands and not with fewer; the carpenter plugs it in the time
the bill says; a ship that founders does so with the log saying when the pumps lost; the
grounding at Horta replayed with the pumps and the carpenter instead of the stopgap gives
the same tide and a repair that takes hands and hours.

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

### 17. Truths for 7-iv (outline)

A broadside's casualties are men of the muster, named where they were named, and the gun's
crew short by them works the gun slower; the surgeon's work returns the lightly hurt to the
bill in days and not the badly; a hand dead of thirst on a passage with the water foul and
no port is a death the log explains from the needs' lines before it.

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

### 23. Truths for 7-vi (outline)

A convoy of six under a brig-sloop meets a privateer schooner: the escort makes the signal
to close round the commodore, the convoy obeys with no model seated, the privateer cuts
out the straggler by doctrine or is driven off by the odds; a blockading squadron off Brest
is blown off by a gale and the business's frigate slips out on it; the squadron keeps its
line at far detail and promotes member by member as the player closes, each in her station.

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

The *Indefatigable* (the razee frigate, 44, Pellew's) and a privateer schooner (the *Prince
de Neufchatel* or the *Grecian*, the one with the better sources) through the generator with
their armament; the merchant brig of 68 given her few guns; every existing file given its
armament and quarter bill. Each with its sources named as the files have always named them.

### 28. The chart's next goal, and the signals' sources

The owner's question of 2026-10-17 stands open: the Mediterranean, the Great Lakes and North
America for 1812, or the Caribbean for the West Indies station; the lead's opinion in that
conversation (the Mediterranean first for the French and the Spanish and the privateers of
every flag, the Caribbean for the convoys and the fever, the Lakes a milestone of their own
for the water's kind). **Decided with the gate's scenarios, not before 7-i.** The signals'
sources (the 1799 book, Popham 1803, the convoy instructions, du Pavillon) are a research
item before 7-i is briefed, each book marked verified or made.

---

## 29. Consent (one revision before any adversarial seat)

The striking-colours study's gap 6: the consent brief names no role in which an instance
fires into a human's ship or takes him prisoner. **Before a model is seated as an enemy
captain**, the brief is revised to say so and the question put again to every model it
would seat (the brief's own promise); 55's revision carries the M7b items (R-50, R-51) and
this one together, or M7's first package carries this alone if 55 has closed. The lead
edits no consent file; the revision is the package's.

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

## 31. Packages (outline; the allocation, numbered after M7b's)

The heavy design to Fable and the data and the standard work to Opus, as the head rules
have it; the numbers from 70 and provisional until each is briefed.

| # | Who | Package | Part |
|---|---|---|---|
| 70 | Fable | The combat core design: guns as parts, the hit model, damage as state, morale and the strike; the figures' sources; the fighting shape measured | 7-ii |
| 71 | Opus | The ships' armament through the generator; the *Indefatigable* and the privateer schooner | 7-viii |
| 72 | Opus | Colours, the private signal, the hail between ships, the lights and the bell | 7-i |
| 73 | Opus | The signal books as data with their sources; the hoist as an evolution; reading by the lookout; the convoy's and the squadron's signals acted by doctrine | 7-i |
| 74 | Opus | Sight across land | 7-i |
| 75 | Opus | The gunnery evolutions and the bill; the fighting book; the captain's engaging by doctrine | 7-ii |
| 76 | Opus | Taking on water: leaks, the pumps, foundering; damage control and jury work; the hotfix's stopgaps retired | 7-iii |
| 77 | Opus | Health and the surgeon; the needs' ends | 7-iv |
| 78 | Opus | Boarding; the fight at far detail | 7-ii |
| 79 | Opus | The prize, the prisoners, the prize court; a captured book | 7-v |
| 80 | Fable | The captive's channel and the continuation; the court martial as the director's proceeding; with 67's seat at a person | 7-v |
| 81 | Fable | The squadron brain and the formations; station keeping as a standing-order kind | 7-vi |
| 82 | Opus | The regimes and the nations' knobs; the business following the player's ship | 7-vi |
| 83 | Opus | Fine control of the sails; the gybe as an evolution; collision | 7-vii |
| 84 | Opus | The consent revision for adversarial seats (or with 55) | 29 |
| 85 | Fable | Six on six: the measure, the tuning, the fighting shape if wanted; the gate document | 30 |

Order: 70 and 72 first (the design and the voice between ships, which M7b's play wants
now), 71 and 73 beside them, then 75, 76, 77 as the fight's three systems, 78 and 79, 80,
then 81 and 82, 83 where the sailing wants it, 84 before any model is seated as an enemy,
85 last. The weather's stacking and seasonal bound (R-39) and the land-avoiding planner
(M7b's 61) are carried in and placed when 81 shows where the squadrons want them.

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
the climatology's drift (placed with 81); the land-avoiding planner (61, placed with 81 or
82); the boat as a vessel and towing (63, before 78's cutting out); the place's knowledge
(65, with the hail: who perceives what); the harbour's second pass (64, the owner's Fable
run, when he likes); the cold (26); the thermometer's first layer (58 or M7b's last); the
lay line (43b, with 82's convoys beating); the Windows pins (69, before the gate).

## 34. What this draft does not yet decide

The hit model's exact bands and the rates' figures (70's, with their sources); whether
morale is a ship's figure or each division's; whether the far fight is a table or the near
model at coarse steps (70 measures both); the signal books' extent in the first version;
how a model at the flagship gives a signal (a tool, or `make the signal` as an order:
the order, by the equal-reach rule, unless play says otherwise); how prisoners are counted
(people or numbers: numbers but for the named); the chart's next block; and everything the
current packages teach before 70 is briefed.
