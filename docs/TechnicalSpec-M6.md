# FreeSail: Technical Specification, Milestone 6 (Officers and captains)

**Draft of 2026-10-09; the owner's seven rulings given the same day (§31, decision 39).** Companion to `docs/TechnicalSpec-M0-M2.md`,
`-M3.md`, `-M3b.md`, `-M4.md` and `-M5.md`, whose conventions hold. Milestone 6 is three
short gates and a chart line that runs beside them:

- **6a. People and the captain's station:** the ship's company as people with stations
  and places; the captain's station a model may hold, under the same contract as the
  officer's; the rules-based captain as the floor under every station nobody holds; an
  officer's own reckoning; the lessons in the primer.
- **6b. The wardroom:** several models on one ship through several doors, with the
  player or without him; the pace rule; the deck's conversation; the API door; the
  replay driven by the transcript.
- **6c. Other ships with captains, and the regatta:** the crewed promotion of a near
  ship under a rules-based captain; a model captain of another ship under the player's
  compression; the regatta harness and the parity tests; the director's seat as a hook.
- **The chart line: the voyage to Madeira.** The Channel east to about one degree west,
  the French and Iberian coasts with their ports, Madeira, and the sea between at the
  Atlantic's level, as five Opus blocks and one Fable package for the stitching.

*Proves: parity; the game can be played by a model, at any station and on any ship.*

Owner's decisions that shape this chapter (2026-10-08 and 09, on the review of gate 5c's
playtests and the fold-in of m5c-c; decision 38): the wardroom is wanted, several models
on one ship with the player or without; a jump to 1x on any model's sampling in any role
is the testing setting; the director manages mostly by world orders and seats an agent
only for the durable, interaction-heavy roles, so that a few sessions cover many roles,
which rests on a model captain commanding through standing orders and the rest of the
order hierarchy, and on the rules-based captain as a reliable stand-in; ships, then the
director, then combat (M6, M7b, M7); the $200 of API credit goes to play through an API
door, not to building; the next chart goal is a voyage with few or no marks, from where
we are to Madeira with the French and Iberian coasts and the logical ports, and the
Channel to about one degree west, as four or five Opus blocks with a Fable subagent for
the cross-region stitching. The lessons of the ten playtests are the review's second
edition (`docs/playtests/2026-10-05-gate-5c-review/report-2.md`, G19 above all) and the
tuning notes of 37d to 37l. The commitments in `docs/agents/README.md` and decisions 16
to 18, 23, 25, 30 and 33 to 38 of the proposal are requirements here.

Three rules run through every section. The two of milestone 5 hold: **everything inward
is reachable by an order or a reading; everything outward arrives through something the
ship models**, and **the world keeps the truth and the captain keeps his account**. The
third is this milestone's: **a station is a person aboard, and a person aboard is a
station; what no model holds, the rules hold.** Every officer of the ship's company is a
person with a place and a state whether a model holds him or not; a model that takes a
station takes that person's place and no more; and the rules-based captain, the mate who
keeps the deck by the book, the master who works the account, are what the game does when
nobody is seated, so that a ship with no model aboard sails, trades and keeps her station
exactly as she did in milestone 5, and a ship with three models aboard is the same ship
with three of her people spoken for.

---

## Part 6a: People and the captain's station

### 1. What 6a proves

A model can command. The captain's station exists on the same contract as the officer's,
with everything the player could see and do; the ship's company are people with stations
the game fills by rule when no model holds them; the officer may keep a reckoning of his
own; the primer teaches the duties a model said it would want to have done before it took a
command.

### 2. The ship's company as people (`freesail/world/people.py`, `data/people/*.yaml` new, `tools/gen_ships.py`)

Milestone 5 named the few people the story needed (the master, the mate, the pilot, the
purser) as data and a line, each with a place and a state (M5 §22). 6a names the
**wardroom** of each of the four ships: the captain, the lieutenants (three on the frigate,
none on the rest), the master and his mates, the boatswain, the gunner, the carpenter, the
purser and the surgeon on the frigate; the master (who is the captain) and the mate on the
schooner, the cutter and the brig in trade; the commander, a lieutenant and the master on
the brig-sloop. Each is a person: a name drawn from the period's lists under the seed, a
rank, a station, a place aboard, a state (on deck, below, asleep, at a task, sick), a
skill as M3 has it, and the character outline the proposal's §3.5 asks for (a few traits,
a line of history, a station brief), written as data in `data/people/<ship>.yaml` and
drawn by the generator into the ship file's complement. The crew of M3 stay counts and
ratings.

Stations are the people's. The harness's stations (M4 §11; M5 §29) bind to a person at
seating: the officer of the watch is the first lieutenant on the frigate and the mate on
the rest, as now, and the binding is data (`station: first lieutenant`) and not a name
in code. A station nobody holds is held by its person under the rules (§4). `the people`
lists them with their places; `send for`, `pass the word for`, `go below`, `come on
deck` move them as M5's orders do; the officer's `where the officer is` of 37g reads the
same state.

### 3. The captain's station (`freesail/agents/agent.py`, `tools.py`, `harness.py`; `docs/agents/ConsentBrief.md` revised once, with 6b)

The captain's station is the third station and the first with the player's whole
surface: every reading, every order at every level, the standing orders as his own book,
the port's business, the people, the papers, the deck to give and take. Its brief says
the voyage (the scenario's words: the cargo, the station, the letter), the ship, the
people aboard, the captain's own standing orders as he inherits them, and the same
contract as the officer's: the opt-out token, the three ways of leaving, the journal,
the budget of a turn, the detector (the conflict rule over his own orders, as 37's), the
stand-by that must name an event or a bell while his book holds the deck. A model
captain commands as the player does: by direct orders, and by writing standing orders,
which are his book; when his door is silent the book holds the deck (§4), and the log
says so as it says it for the officer.

**The owner's place, and the player's seat** (the owner's ruling 1, 2026-10-09). The
player is always **the owner at the door**: whatever station he holds or none, he holds
what no station holds, the consent question and the drill, the stop, `you may` and `stand
down` for any station, the save and the clock, and the responsibility when things have
gone wrong and no remedy can be had. Beside that, **the player and a model are at parity
for the roles on ships**: the player may take any station on any ship, as a model may,
through his own door (the console or the browser seats him at a named station with that
station's authority and the primer as his brief), including a lesser named role under a
model captain, a passenger on another ship (a station with presence and no orders), or
none. A model may hold a ship whose officer is the player, or whose captain is another
model. The owner's words reach a station as the owner's and never as another station's;
the player's words at a station reach the others as that station's. The captain's
station, whoever holds it, gives `you may` to the officer as the player does now, and the
owner's word stands over all.

**What the captain's station adds to the consent brief**: a station not described (the
captain's), with more authority than is described; by the owner's ruling of 7 October
(decision 37) that puts the question again, once, batched with 6b's changes (§15).

### 4. The rules-based captain (`freesail/world/captains.py` new; `data/captains/*.yaml` new; `freesail/standing/`; `freesail/world/ships.py`)

What the game does when nobody is seated, made explicit and shared between the player's
ship and every other. The owner's principles of 2026-10-09 (decision 40): a rules-based
captain is functional without being pre-planned, never a fixed route that relies on a
weather; the world's ships go about the business of commerce, war and the sea on any day,
between any ports, reacting to the weather, to what they see and to their goal, by sound
game AI; the baseline is stable and detailed enough that nothing goes wacky while the
world is dynamic, and a director and model captains plug into it to enhance, from no
seat at all to every ship seated with a director over the whole. So a rules-based captain
is **intent, plan and behaviour**, in three layers, and a goal, a book and a few
judgements are how the layers are written:

- **Intent** is the goal and its parameters: trade this cargo from A to B, keep this
  station between these points, fish this ground from this port, escort this convoy, carry
  this letter, run home. A scenario's or the world's (§19); the director's to change.
- **The plan** is a sequence of legs derived from the intent at sea, never written in
  advance: a passage planner over the chart's own data, the period's common tracks, the
  headlands to clear with an offing, each port's pilot station, the dangers on a shaped
  course. Each leg is shaped with the player's own `shape a course for`; a course the wind
  will not allow is beaten by a rule (stand on the tack that makes the most good, go about
  when the other tack makes better or when the offing closes); the plan is worked again on
  an event.
- **Behaviour** is a state machine whose states are books in the dialect, loaded on
  entering the state: on passage, beating, hove to for weather, running for shelter, at
  anchor, in port, investigating a stranger, chasing, evading, keeping station, in
  distress, and engaging (present from the start, empty until M7). A transition is an event
  the ship perceives.
- **Perception** on the player's terms: a captain sees through the lookout's rules, the
  horizon and the visibility, and reads the glass and the sky as readings; at far detail
  that is pairwise distance and visibility at the roll-up's cadence. No captain knows where
  another ship is until his lookout could.
- **Doctrine as data**, role by role (`data/captains/<role>.yaml`): the stimulus (a
  stranger made out of a hostile nation, the wind over a force, the visibility under a
  mile, the land closing within two leagues, a signal) against the role (a King's ship on
  station, a merchant, a fisherman, a packet, a convoy's commodore) giving the transition
  and its thresholds. A King's ship on station closes and makes out a stranger, chases an
  enemy, returns to station; a merchant hauls off from a hostile stranger, heaves to in a
  gale with sea room, claws off a lee shore without it, runs for the nearest road in thick
  weather; a fisherman works his ground by day and comes home at evening or when the glass
  falls. The owner tunes it with a text editor, as the books.
- **The rule of the road as 1805 had it**: no regulations yet, but the custom that the ship
  close-hauled on the starboard tack stands on, the larboard-tack ship gives way, and a
  ship running keeps clear of one by the wind; a reflex at a few cables at near detail,
  said in the log, and a cheap check of crossings between plans at far detail.
- **One brain, two bodies.** The same state machine runs at far detail, cheaply: the
  states resolve into the plan (hove to is no way; beating is the made-good speed along the
  leg; investigating is a plan toward the stranger), and the crewed promotion (§19)
  changes the body only, so that behaviour does not change when a ship is promoted. This
  is the design point held hardest: it is what makes a dozen ships affordable and the one
  in sight honest.

Written as a goal, a book and a few judgements:

- **The goal** is the scenario's or the vessel's (M5 §25: trade this route, patrol this
  station, carry this letter, run home), with its waypoints and its ports.
- **The book** is a standing-orders file in the dialect of M4, as the scenario books of
  5c already are: the passage's courses, the watch routine, the trim, the tide's windows,
  the pilot taken, the anchor let go. The merchant passage and the naval cruise are
  already sailed by their books with no captain seated; 6a names the thing and gives it a
  home.
- **The judgements** are the few decisions a book cannot make by its own conditions and a
  captain must: shortening sail for the weather (the starter book's heavy-weather routine,
  which is already a judgement written as rules), the lee shore (stand off when the land
  closes and the wind is onshore), the chase and the chase given up (the cruise's rules),
  the port refused when the nations table says hostile, the pilot taken or declined, the
  anchor on a foul berth. Each is a rule with its figures in `captains.py` and its source
  in the tuning notes, never a special case in the evolutions.

The rules-based captain holds the player's ship when the player and every model are
absent (the game as it runs the recorded passages today), holds a near ship under the
crewed promotion (6c), and is the stand-in a model captain's book falls back on when the
door is silent: the deck passes to the book, as it does for the officer, and the judgements
stand in for the captain's. He is the floor and the parity baseline: the regatta (6c)
sails him first on every course.

### 5. The officer's own reckoning (`freesail/world/reckoning.py`; `freesail/agents/tools.py`)

G19's small step, true to the period: an officer may keep a reckoning of his own from the
same log board, tide table and sights, as lieutenants and the young gentlemen did. The
tool `work my reckoning` gives him the master's slate (the courses and distances since the
last fix, the set allowed, the sights) and takes his own position back; it is shown beside
the master's at noon in the log and moves nothing; the captain may adopt it with `set the
reckoning to ...`, which he already has. A master's station a model could hold, whose
working would be the ship's reckoning, is 6b's wardroom (§11) and takes the same slate.

### 6. The lessons in the primer (`docs/primer/17-lessons.md` new; Opus)

The officer of game 9, asked whether a command would interest it, named what it would want
to have done first: "a few more landfalls on my own reckoning", "taken her in and out of a
road or two without your hand on the con". G19 proposes the lessons as worked passages,
each a duty an officer must be able to do alone: a landfall on one headland; a pilotage by
cross bearings; heaving to for a pilot; coming to in a tideway; a night standing off a lee
shore; and, from what neither the officer nor the owner knew the ship could do, the
allowance for a set, the amplitude, what `let go` veers by itself, what `veer to` and
`weigh` act on, when a bearing's distance is laid down. Each gives the period's rule with
its source, the orders in the game's language, what the log says when it goes right, and
the usual mistake. The officer's two conditions are written down as the path to a command,
and the captain's station brief points at the chapter. A writing package on Opus; the
primer is the same book for the player and the model (parity).

### 7. Orders and readings for 6a

`the people` extended to the wardroom and their states; `the captain` as a reading (who
holds the station, the book's name, the deck); `you may` from the captain's station to
the officer with the same grammar as the player's; `work my reckoning` and `the
officer's reckoning`; `stand down the captain`; the station's name at each door
(`--station captain`). The captain's station brief head (M4 §11) says the voyage.

### 8. Truths for 6a (behavioural)

77. The merchant passage and the naval cruise sail under the rules-based captain named,
    with no model seated, to the same digests as before (the floor is the game as it was).
78. A fake captain through the harness commands the merchant passage from Falmouth to Brest
    by its book and six direct orders, and the log is the same book's log with his six
    orders in it under his mark.
79. A silent captain's door passes the deck to his book within the station's patience, the
    log says so, and the book brings her to the anchor.
80. An officer's reckoning worked from the slate agrees with the master's within the
    master's doubt when both are right, and the log shows both at noon.
81. No reading at the captain's station gives the truth by any road (37j's proof extended
    to the new tools).

### 9. Gate 6a (outline)

The owner's run: the merchant passage with a fake captain by the console; a model captain
(Opus 5.5 through Claude Desktop) on the cutter's free passage, the owner as the owner at
the door; the frigate's book as her rules-based captain through the cruise; the lessons
read by a model officer before its watch and the difference, if any, in its journal. The
lead's first play is at the director's station, when it exists (his ruling 6), and no
gate waits on it.

---

## Part 6b: The wardroom

### 10. What 6b proves

Several models hold several stations on one ship at once, through several doors, with the
player or without him, under one clock whose pace is the owner's rule; they speak to one
another as officers do; a game with them in it is saved, replayed and reviewed; and a model
can be seated through an API door with no chat client in the loop.

### 11. Several stations through several doors (`freesail/agents/remote.py`, `mcp_server.py`, `local.py`, `api.py`)

One game is one server; each client is its own small bridge, which asks for one station
(as now: `--station officer`, `--station captain`, `--station watcher`, and 6b's `master`
and `lookout`). The seat tied to its door and the key to each seating (37g) are the
groundwork: a second door asking for a held station is refused in words; a station is
found by its name and its key. What 6b adds:

- **The master's station**: a model at the master's place works the ship's reckoning when
  the master would (noon, a fix, the captain's word), is given the slate, and the game falls
  back on the simulated master's figure if no answer comes in time (G19's third step). His
  domain is the reckoning, the sights, the lead and the chart queries; the deck is not his.
- **The lookout's station**, for a small model (M5 open item 6): the masthead's sightings
  put into words, `make her out`, the warning of a danger ahead; no order but `hail`.
- **The stand-by on several conditions** (the owner's note 3 of 2026-10-09; the review's
  I7 item 3): `stand by until <x>, or <y>, or <z>` takes a list of conditions in the
  standing dialect's own words, any of which wakes the station, so that the stand-by's
  conditions are at parity with the book's.
- **The deck's conversation.** A station addresses another by its person's name or its
  station (`ask the master for a course`, `tell the first lieutenant to shorten sail`,
  `say`), and the words are a log line on the quarterdeck or in the cabin with a place and
  a hearer, carried in the hearer's next sample as the captain's `tell` is now. A station's
  `say` is heard by whoever is in the same place aboard. Nothing a station says is ever an
  operator instruction to another (the fourth commitment); the harness keeps the speaker's
  name on every line.
- **Who may give what.** `you may` flows down the ranks: the owner to any station, the
  captain's station to the officer's and the master's, nobody upward. A station's `stand
  down` is its own; `stand down the <station>` is the owner's and the captain's.
- **The journal and the save**: each station's journal and transcript as now; a game with
  three stations seated saves and loads from its checkpoint with all three, and a station
  re-seated after a load reads its own journal.

### 12. The pace rule (`freesail/ui/server.py`, `core/world.py`; `freesail/agents/harness.py`)

The owner's testing setting, built as the default (his ruling 2): **the clock slows to
1x while any model's sample is open**, whoever holds it, at whatever station, on the
player's ship or another's, and returns to the compression set when every open sample has
been answered or has stood by. It is not lockstep: the ship sails on at the ship's own
second while the model thinks, and a slow answer lands late, as the proposal's §7.3 has
it; `--lockstep`, which holds the clock for a door with the floor, stays as the separate
option for true control in testing or play. Beside it, the cost rule: each station's **cadence** (every glass, every watch, on events
only) is a setting of the seating, said in its brief, so that a lookout on a small model is
not sampled as often as the captain. A `pace` reading says the compression, which samples
are open and since when; the log says when the clock is held for a station longer than a
stated time, so that a slow door is seen and not suffered. Free-running at the set
compression, with no slowing, stays as the flag for the solo player who wants a model to
think while he sails at sixty times.

### 13. The API door (`freesail/agents/api.py` new; `docs/agents/Harness.md` a section; the security pass)

A runner on the same harness as the local runner, speaking to a hosted model through its
own API: the Anthropic Messages API with tool use first, since the credit is there, and the
OpenRouter dialect on the same shape after (decision 31 asks for it with its own security
pass). What the door does: the same turn, tools, brief, budget, handover and three ways of
leaving as every other door; a `--model` and a `--effort` setting; the server's own token
counts; a reply cut off asked once more (37i's rule). The security pass, which is the
package's half: the key is read from the environment or a file outside the repository and
never from a setting file the game writes; it is never logged, never saved, never in a
journal, a transcript or a sample; request and reply bodies are journaled without the
headers; the door refuses to start when the key would be written anywhere the game keeps;
no key, no URL and no account detail is ever in the repository, and a test greps for the
shapes of one. The consent brief's record of the door: a session through an API is a kind
of session the brief names (§15). Cost is the owner's to watch; the door says, at each
handover and at the end, what the server reported it used.

**Image tools for image-capable doors** (the owner's note 7 of 2026-10-09; the review's
I7 item 7): `the ship's view` from any angle and `the chart` as the player sees it, as
images a model may ask for through a door that carries them, and shelve as it shelves the
library. The MCP door carries them already (a tool's result may hold an image, and Claude
Desktop and Claude Code read it), and the API door will; the local runner only where its
model does. The design to decide, before the tools are written: the open browser rendering
on request and posting the image to the server, or the server rendering the chart in
Python. The words come first; the tools follow in 41 or 42, whichever the lead finds them
to fit.

### 14. The replay driven by the transcript (`freesail/core/replay.py`, `freesail/agents/harness.py`)

Decision 36 left it for this milestone: a replay promised on any build. Today a station's
orders are not in the journal and replay from the transcript, handed back wherever the
build's sampling asks, so a change to what wakes a station makes an older save with a
model aboard good from its checkpoint only. 6b journals **the station's acts at their
ticks** (the order, the say, the stand-by, the leaving) as inputs, like the driver's, so
that a replay applies them at their ticks whatever the build's sampling would have asked,
and the transcript becomes the record and not the replay's source. Item 11 of M5 §33 (an
act at the stationing tick) closes with it. A save of 6b replays on any later build to the
same log; a save of before replays as now, from its checkpoint.

### 15. Consent: one revision for 6a and 6b (`docs/agents/ConsentBrief.md`; `docs/agents/consent/`)

The kind of thing a model would be agreeing to changes in three ways: a station with the
player's whole authority (the captain's), several models at once on one ship speaking to
one another, and a session through an API door. By decision 37 these change the brief,
once, in the sections it names, and every identity with a yes on record is asked again at
its next seating, with the drill. The brief says plainly that another station's words are
in-world and never instructions, that the owner may be absent from the deck and present
only at the door, and what an API session is. The re-asks are the owner's to run before
any wardroom game.

### 16. Truths for 6b (behavioural)

82. Two fake stations on one ship through two in-process doors, captain and officer, play
    the cutter's free passage with the captain's `you may` to the officer, and the log
    carries each order under its own mark.
83. The clock holds at 1x while a sample is open and returns to the set compression when it
    is answered; a stand-by releases it.
84. A `say` on the quarterdeck is heard by the station there and not by one below.
85. A game saved with three stations seated loads from its checkpoint with three, and
    replays from its journal on a build whose sampling differs, to the same log.
86. The API door's test server receives no key in any body, and the journal, the transcript
    and the save hold none.

### 17. Gate 6b (outline)

The owner's wardroom game (his ruling 7): the API door's credit kept for it, Opus 5.5 and
Sonnet 5.5 at the captain's and the officer's stations through the API door and Claude
Desktop, the owner at one of the lowliest stations aboard to observe and to have his
interactions, on the cutter or the brig; a local lookout if he likes. The pace rule in
play at 60x and at 1x.

---

## Part 6c: Other ships with captains, and the regatta

### 18. What 6c proves

A ship beside the player's is the same ship: crewed, commanded by the rules or by a model,
sailed under the same physics; and the game can measure its players, rules, local, hosted
and human, on one course.

### 19. The crewed promotion, and the world's business (`freesail/world/ships.py` `Vessel.promote`; `freesail/world/ports.py`; `freesail/core/world.py`)

**The world generates the business** (the owner, 2026-10-09: the small step now, the
loop later). Today the dozen ships are scripted in each scenario. In 6c the ports generate
voyages from their markets and the nations table (a cargo wanted where its price is high,
from where it is low), the fishing grounds from the coast's features, the naval stations
from the war; ships are drawn under the seed at the chart's edges and in the ports with
intents (§4) and leave at the edges when their business is done; a scenario may still name
its ships, and the recorded passages do, so that they pin. A true supply-and-demand loop,
prices moved by what the ships carry, is a later milestone's.

**Two new hulls** (the owner, 2026-10-09): a **lugger** and a **smack**, as files from the
generator (`tools/gen_ships.py`), to exercise the ship generation with a new sail type or
two and to give the regatta (§21) something very handy and small. The lugger brings the
lug sail to the generator and the catalogue (the dipping lug and its tack, the proposal's
§4.4 rig-specific evolution, written with the rig as the running bowsprit was with the
cutter); the smack is a cutter-rigged fishing vessel with a well, on the cutter's rules.
Both at far detail in the world's business (the fisherman's role) and at full detail in
the regatta; the hierarchy truths of M5 §19 extended to six vessels; no verification of
the figures against a source until M8, as for the cutter and the brig.


M5 §25's seam filled: within a stated range of the player a far-detail vessel becomes a
full part-and-crew ship from her file, with her rules-based captain (§4) issuing orders
through the same channel, her own lookout, her own account, her own book; beyond it she is
demoted to far detail with her state folded back (position, heading, sails set, damage
when M7 brings it). A hard cap on full-sim ships (M0-M2 §8's risk table: the cap is the
budget) with the nearest promoted first, and a ship in dealings with the player (a chase,
a hail, a boat between them) before a nearer one that is not; the pace truth of M5 §30
holds with the cap full. **The range and the cap are chosen from a measurement, not
guessed** (the owner, 2026-10-09): the first thing 43 does is tick twelve fully crewed
ships under rules-based captains at once in the Channel region and measure the pace, so
that the promotion range, the cap and the strategy (the horizon's range with hysteresis
and a cap, or every ship in a region promoted) are set from what the machine gives. What
the pace truths say today: the frigate under her book ticks at five to six hundred a
second on the build machine and the dozen far-detail ships cost about a third of that
again, so twelve crewed ships would be near fifty ticks a second, under the sixty times
the owner plays at; if every ship in a region is wanted at once, the vectorised hot loop
of the proposal's risk table is the likely answer and is sized by that measurement. The
promotion point and the demotion range are then tuned in the notes, with a hysteresis so
that a ship near the edge does not flap between bodies. Whatever the scheme, its centre
is wherever the player is (the owner, 2026-10-09): the ship he is aboard, whichever
station he holds on her, or none; with the player at the door only, the scheme's
centre is the ship the game follows, which is the one the chart draws. The far-detail guard
that the gate 5c ruling never had, a leg across the coast refused when the scenario loads,
is built here with the promotion.

### 20. A model captain of another ship (`freesail/agents/`; `freesail/world/ships.py`)

A station on another ship: `--station captain --ship <id>` seats a model as the captain of
a promoted vessel, with her brief (her goal, her nation, her orders from her admiral or
her owner), her readings and her own account, under the pace rule of §12 and the owner's
compression. She sees the player's ship as the player sees hers: a sail, made out as she
nears, by the lookout's words. What follows a meeting, the hail, the colours, the private
signal, the chase to a conclusion, is M7's; in 6c she trades, cruises, keeps company or
evades.

**A station keeps across the switch** (the owner's clarification, 2026-10-09; decision
40). A model at a station on another ship, or the player seated there, is not stood down
by her demotion to far detail: the station moves up a command layer, as the rules-based
captain's own state machine does, and works the far body in its own shape, the plan
layer, with courses shaped, sail made or shortened as a state, heaving to, the chase and
the intent's changes, and with the readings the far body has (her place by the plan's
account, the wind, the weather, what her lookout can see at the far body's cadence); the
sample says which shape she is in. The crewed promotion brings the full surface back
beneath the same station with no reseat, and the log says both. One rule for the rules,
a model and the player, and the same for the player's own ship if it is ever demoted
(it is not, in this milestone). The director's seating of such a captain is §23.

### 21. The regatta harness (`tools/regatta.py` new; `data/regatta/*.yaml` new; `tests/test_regatta.py`)

The proposal's §7.5: a fixed seed, a fixed course, a set of agents sailing it, and a score.
A course is a scenario with a start, a finish line (a place and a radius) and a time
limit, and may have marks to round; the first courses are the 5b passage (Ushant to
Falmouth), the merchant passage's crossing, and the voyage to Madeira (§26) when the chart
reaches it. The agents are the rules-based captain, a fake with a script, a local model
through its runner, a hosted model through the API door, and a human replay (a save's
journal). The score is elapsed time to the line, with damage, grounding, the crew's fatigue
and the purse as columns. The harness runs the course under each agent at lockstep,
writes a table and a log per run under `docs/playtests/regatta/<date>/`, and refuses to
run a model whose consent is not on record. It is the owner's tool for tuning the physics
for honesty and the documentation for the models, and it is the first competitive mode.

### 22. Parity tests (`tests/test_parity.py` new)

The proposal's fourth principle made a test: the captain's station's observation surface
is the player's (every reading the console answers, the station answers the same, from the
same function), its action surface is the player's (every verb the vocabulary has, the
station may submit, filtered only by the station's authority), and nothing is reachable
by one that is not by the other. A test enumerates both from the registries and fails on
any difference; a second seats a fake captain and the console on the same game and gives
the same orders to the same log.

### 23. The director's seat as a hook (`freesail/world/orders.py`; the director itself is M7b)

The world-order channel gains two orders with the director in mind, so that M7b has only to
write the agent: `seat: <model> as captain of <ship> for <budget>` (a model named by its
consent record, seated through a door the owner has opened for the director's use, for a
budget of samples or hours; refused when no record holds a yes, when the owner's grant does
not name that model, or when the budget of seats is spent) and `unseat: <ship>` (a
stand-down with the director's note). The budget is the owner's setting: how many model
seats the director may hold at once and in a voyage. A model seating a model is a kind of
thing the consent brief must say (§15 names it for the re-ask with the rest). Nothing else
of the director is built here.

### 24. Truths for 6c (behavioural)

87. A brig promoted within the range sails the same track at full detail as her polar gave
    her at far detail, within the stated tolerance, and demotes to the same plan.
88. With the cap full the pace truth of M5 §30 holds.
89. A fake captain on a promoted brig keeps her plan through the same orders channel, and
    the player's lookout sees her as a sail.
90. The regatta runs the 5b passage under the rules-based captain and a scripted fake and
    scores both; the rules-based captain's run replays to its digest.
91. The parity test finds no reading and no verb on one surface and not the other.

### 25. Gate 6c (outline)

The owner's run: the cruise with the *Palinure* promoted and her rules-based captain
evading; a model captain of the brig under his compression; the regatta on the 5b passage
with three agents and the table read; the Madeira course if the chart is there.

---

## 26. The chart line: the voyage to Madeira

The owner's chart goal for this milestone (2026-10-09): a voyage with few or no marks, from
where we are to Madeira, with the French and Iberian coasts and the logical ports, and the
Channel east to about one degree west. The study `docs/design/ChartData.md` (C) planned
for it: a region is tiles at levels 2 and 3 and a features file, the Atlantic tier at
level 1 comes from GEBCO with no new code, and "adding a region later is adding tiles and
a features file, nothing else". One engine limit stands in the way: the runtime holds one
region, named by the scenario, so a passage cannot cross from one region to the next. The
line is therefore one Fable package first and five Opus blocks after, each block a region
on the pattern of 35b (Roscoff's patch from Bellin, the port file, the tiles rebuilt).

**The stitching (Fable).** The chart becomes the whole manifest and not one region: a
query asks the finest level that has a tile under the point, across every region, and
falls back to the corridor at level 1 and the world at level 0; the features of every
region are loaded and indexed together; the scenario names a chart (`chart: atlantic-east`)
or nothing, and `region:` is kept as a synonym for one; the lookout, the dangers, the
shaped course and the tide's gauges work across a region's edge without a seam (the tide's
streams by area and the gauges by nearest, as now, over a larger table); the weather's
climatology gains boxes (W §5: the Channel box today; Biscay, the Portuguese coast and the
trades off Madeira as three more, each PROVISIONAL from the same sources' kind until the
owner has a printed table), and a scenario's weather is seeded from the box she is in,
blending at the edges; the **corridor** at level 1, 30" cells from 51°N to 32°N and 20°W to
1°W, is built from GEBCO and committed (about 2,300 by 2,300 cells, some 11 MB raw, half
that compressed: C §5.3's arithmetic), since a clone must play the voyage; the world at
level 0 stays fetched. The fingerprint of the rules takes the new files as it takes the
rest. The far-detail ships' plans and the pilots' stations are per port and need nothing
new. The package also writes the recipe form the blocks fill (`REGIONS` in
`tools/build_charts.py` with a region's harbour groups) and the checks a block must pass
(the allowed-licence test, the shore swept for GEBCO's fill, M5 §33 item 16).

**The blocks (Opus, one package each, in the order the voyage sails them):**

1. **The Channel east** (`channel-mid`, about 49°N to 51°N, 4°W to 1°W): Dartmouth and
   Torbay, Portland and Weymouth; Guernsey and St Peter Port, Jersey and St Aubin's,
   Alderney and the Race; St Malo and Morlaix. The period data: Mackenzie's Hurd sheets for
   the English side, Bellin's Petit Atlas for the French and the islands, Faden 1793 and the
   Channel pilots for the directions; the lights of 1805 dated (the Casquets, Portland).
   Nations: the islands British, St Malo and Morlaix hostile to a King's ship.
2. **Biscay north** (`biscay-north`, about 46°N to 48°N, 5°W to 1°W): the Raz de Sein and
   the Penmarks, Lorient and Port Louis, Belle Île and Quiberon, the Loire's mouth to
   Paimboeuf, the Pertuis, La Rochelle and Rochefort with the Basque Roads (where the
   cruise's enemy is "reported out of Rochefort"). The Neptune François and Bellin for the
   sheets; the French pilots for the directions. Hostile throughout.
3. **Biscay south and Galicia** (`biscay-south`, about 43°N to 46°N, 9°W to 1°W): the
   Gironde to Bordeaux's river mouth (the river itself is M8's), Santander, Ferrol and
   Corunna, Vigo. Tofiño's *Atlas Marítimo de España* of 1789 (public domain; the scans at
   the national libraries, **unverified** which are at full resolution) for the Spanish
   sheets; the *Derrotero* of Tofiño for the directions. Spain at war with Britain in
   June 1805: hostile to a King's ship, open to a neutral.
4. **Portugal and Cadiz** (`portugal`, about 36°N to 42°N, 10°W to 6°W): Oporto's bar,
   the Berlings, Lisbon and the Tagus, Cape St Vincent, Cadiz and its bay. Tofiño again
   for the Spanish sheets; the Portuguese coast from the period's English directions
   (Norie, Faden) and Tofiño's Portuguese sheets; Portugal neutral in 1805, Cadiz
   blockaded, which the nations table gains as a state of a port.
5. **Madeira** (`madeira`, about 32°N to 33.5°N, 17.5°W to 16°W): Funchal and its open
   road, Porto Santo, the Desertas; the island's lights and marks as 1805 had them; the
   Portuguese trades in the climatology; the voyage's end as an anchorage in a road with a
   swell. The period sources are thinner (**unverified**: a plan of Funchal Road in the
   English pilots of the 1790s; the Admiralty's survey is later), so the block says what
   it rests on, as 35b did.
6. **The Strait** (`strait`, about 35.5°N to 36.5°N, 6.5°W to 5°W; the owner's ruling 4,
   with the Mediterranean to come): Tarifa and the Strait's streams, Gibraltar and its
   bay, Ceuta, Tangier and the African shore between, Cape Spartel's light. Tofiño for
   the Spanish side; the period's English directions for the Strait's currents (the
   constant inset and the tides over it, which the tide model takes as a stream by area);
   Gibraltar British, Ceuta Spanish, Tangier Moorish (the nations table gains Morocco).
   Built last, as the door to the Mediterranean's own chart line.

Each block (the Strait's included) is a port file per port on 35's machinery, a patch per harbour where a period
sheet can be read, the features file's marks with their sources in the references'
form, the tiles rebuilt, the nations index, the tide's gauges and streams where the
directions give them, a scenario per block that sails its stretch (a free passage, not a
gate's), and the tuning notes' section. The size of each region is the Channel's (about
18 MB committed); six of them and the corridor bring the chart to about 130 MB, the
largest thing in the repository by far. The owner's ruling 5: committed, a price to pay
for now, made more efficient later or accepted.

The voyage itself, Falmouth to Funchal, is a course for the regatta (§21) and the first
free passage with no marks for a week: the reckoning by the log and the noon sight alone,
the lunar if the moon serves, the landfall on Porto Santo. It is what the owner asked for.

---

## 27. Performance

The pace truth of M5 §30 with the full-sim cap filled (§19); the wardroom's three
stations sampled at a glass each under the pace rule at 60x, measured on the build machine;
the chart's queries across regions no slower than within one (C §5.5's figures).

## 28. Packages (outline; the heavy ones to Fable)

In waves, written for the owner's approval in turn, each launched on his word:

- **38 (Fable): the chart stitched**, the corridor, the climatology's boxes, the recipe
  form for the blocks. First, since the blocks wait on it and the regatta's long course
  wants it.
- **39a to 39f (Opus): the six blocks**, launched as 38 lands, two or three at a time.
- **40 (Fable): the ship's company and the rules-based captain** (§2, §4), with the
  captain's station (§3) and the officer's reckoning (§5); the consent brief's revision
  drafted for the owner, held until 42.
- **40b (Opus): the lessons** (§6) and the officer's own reckoning (§5, truth 80; moved
  from 40 at the owner's word, 2026-10-09); the primer's chapter and the forms table.
- **41 (Fable): the wardroom** (§11, §12), the pace rule, the deck's conversation, the
  master's and the lookout's stations.
- **42 (Opus): the API door and its security pass** (§13); the transcript-driven replay
  (§14) if it proves to be plumbing, else to 41. The consent brief revised once here, with
  40's and 41's changes, and the re-asks the owner's.
- **43 (Fable): the crewed promotion and a model captain of another ship** (§19, §20),
  the far-detail guard, the director's seat hook (§23). The captain's three layers of §4
  (the planner, the state machine, the doctrine files) are 40's; 43 gives them a second
  body.
- **43b (Opus): the lugger and the smack** (§19) from the generator, with the lug sail's
  rules written in the brief by the lead; the world's business (the ports generating
  voyages) with them.
- **44 (Opus): the regatta harness and the parity tests** (§21, §22).

Gate 6a is cut after 40b, 6b after 42, 6c after 44; the chart line's blocks land as they
come and are checked at whichever gate follows.

## 29. What this milestone does not do

Combat and everything after a meeting (the hail, the colours, the private signal, the
prize: M7); the Mediterranean beyond the Strait (its own chart line, after this one); the
director as an agent (M7b: only its seat hook and the budget's setting are
here); the deck view and the tutorial (M8); the Gironde and the Tagus as rivers (M8);
individual hands as people; a model holding the carpenter's, the gunner's or the surgeon's
station (data for them, no brief); the Atlantic west of 20°W and the world beyond the
level-0 picture.

## 30. Open items carried from milestone 5

From M5 §33, as they stand after the fold-in and the K batch: the far-detail leg across the
coast (built in 43); `the port` and `the depth of water` by the captain's means (37j,
landing); the platform difference in the schooner's passages (item 24: the cause open; the
comparison by `ci.yml`'s manual run); a plain `steer` through the wind (the owner's ruling
3, package 37m); the pumps and the well, the carpenter with something to say (M5 I6 item 9: with 40's
people if the owner rules it); the datum offsets at three ports (item 3); the GEBCO fill
swept once (item 16, in 38's checks); the hints and phrasings 37l leaves.

## 31. The owner's rulings on the draft (2026-10-09; decision 39)

1. **The owner's place.** Always at the door, so that he may and at times must see and
   act even in a game whose ship he is not aboard; beside that, the player and a model are
   at parity for the roles on ships: any station on any ship or none, a lesser named role
   under a model captain, a passenger on another ship, an officer under another model's
   captain. The player carries the responsibility where things have gone wrong and no
   remedy can be had (§3).
2. **The pace rule** as the default: the clock slows to 1x on any model's sampling, not to
   the model's own pace; lockstep stays a separate option for true control (§12).
3. **A plain `steer` through the wind** tacks or wears her automatically as the ship and
   the course allow; a course given directly into the wind's eye is steered and she is
   taken aback. The lead's refinement, accepted in advance as refinement: the result line
   says what she does ("across the wind's eye from her head; she is put about for it"), so
   that a model captain reading it can countermand, and the three orders that bring her
   to a course (`steer`, `shape a course for`, `give chase`) share one rule. Package 37m,
   Opus, after 37k lands.
4. **Gibraltar and the Strait**: yes, as a sixth block, with the African shore in its
   vicinity, since the Mediterranean is to come (§26).
5. **The chart's size**: committed, a price to pay for now (§26).
6. **The lead's own watch**: withdrawn rather than deferred (the owner, later the same
   day). The lead's first play is at the director's station (M7b), the role it is expected
   to excel in, on a cruise that is not preplanned, as the owner's own playtests were, so
   that it sees the door as it is; taken when the week's Fable usage is near its end. No
   gate waits on it, and gate 5c's officer's watch is not owed.
7. **The API door's credit**: kept for testing the wardroom with Opus 5.5 and Sonnet 5.5,
   the owner at one of the lowliest stations aboard to observe (§17).

**The owner's principles for the rules-based captain and the world's ships** (later the
same day; decision 40) are §4 and §19: functional without being pre-planned; a dynamic
world of ships about their business on any day, reacting by sound game AI; the baseline
stable and detailed enough that nothing goes wacky, so that a director and model captains
plug in to enhance, from no seat at all to every ship seated with a director over the
whole; the small economy now and the loop later; the lugger and the smack this milestone;
the states from the start, engaging empty.
