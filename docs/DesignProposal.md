# FreeSail: Design Proposal (v0.2, for refinement)

This document turns the initial brainstorm (`docs/InitialDesignBrainstorm.txt`) plus two rounds of follow-up answers into a single proposal. Version 0.2 folds in the answers to the v0.1 open questions; they are recorded in §12. It is written for a reader who is not a programmer. Where a term of art is unavoidable it is explained on first use. Where a choice genuinely forks the design, both branches are laid out as a *decision record* with a recommendation, so we can argue about the fork rather than the whole document.

Everything here is a proposal. Nothing is built yet.

---

## 0. Summary

FreeSail is a **ticked, text-first sailing simulation** of a late-age-of-sail vessel of **any rig**, in which the ship is modelled as a **graph of individually simulated parts** (spars, sails, lines, fittings, guns, stores) worked by **individually simulated sailors**. Players and language models control the ship through the **same layered order system**: from hauling a single line, up through named period evolutions ("wear ship"), up through a small bespoke **standing-orders language**, up to full scripting in Python. The ship lives in a **dynamic sandbox world** with weather systems, ports, other ships pursuing their own goals, and small-scale combat.

The organising principle is: **the ship's log is the game.** Every change in the world is an event. The text log, the map, the profile view, replays, LLM narrators, LLM players, and future multiplayer all consume the same event stream and query the same state. That single decision gives us LLM parity, testability, and multiplayer readiness almost for free.

Recommended stack: a **Python simulation core** that runs headless, a **browser-based local client** for the map, log and profile view, and **LLM integration through a tool interface** (the Model Context Protocol, MCP) so that Claude via the desktop subscription and local models via any tool-calling runtime can watch, advise, crew, or captain with no per-token billing.

---

## 1. Vision and pillars

**One-line pitch.** A sailing game where every rope matters, where you can sail by giving orders like a captain or by writing the orders your crew will follow without you, and where a language model can sit at any station on the ship, from lookout to captain.

**Pillars** (used to settle arguments later; if a feature serves none of these, it waits):

1. **Bottom-up realism.** Behaviour emerges from parts and physics, not from scripted outcomes. If a studding sail exists, it exists because a boom, an iron, a halyard, a tack and a sheet exist and a crew can rig them.
2. **Any rig.** The engine knows about spars, sails and lines, not about "a ship". A ship-rigged frigate, a topsail schooner, a lugger and a cutter are data files that differ in their parts, and nothing in code assumes a number of masts or a kind of sail. This is a pillar, not a feature, because it is cheap to honour from the start and ruinous to retrofit.
3. **Orders at every altitude.** Manual, semi-automated, and fully automated play are all first-class and freely mixed, mid-voyage.
4. **Parity.** Humans and LLMs see the same information and have the same actions. No hidden API for machines, no hidden UI for humans.
5. **Dynamic, not authored.** The world runs whether or not the player is looking. Content is systems, not levels.
6. **Depth over gloss.** Text and schematic graphics that tell the truth beat 3D that lies. Performance and budget go into simulation.
7. **Period-plausible, not period-pedantic.** If it was done, or physically could have been done, in roughly 1780–1820, it is allowed. Things that never could have been done are not.

**Non-goals (for now).** Real-time 3D rendering (a long-term dream, deferred until the simulation and world are strong; see §6.1). Authored campaign. Public multiplayer server. Faithful replica of one specific historical vessel or year.

---

## 2. The player's experience

### 2.1 What a session looks like

You open the game. A log panel occupies most of the screen, scrolling ship's-log-style entries: bells, wind changes, sail handling, sightings, casualties. A map shows your ship, coastline, known vessels, wind arrows, and your dead-reckoning track. A profile view shows your ship's sail plan as a schematic, sails drawn in their current state (furled, set, reefed, backed, split). A command line sits under the log.

You type orders. `set the fore topsail`. `brace up sharp on the starboard tack`. `steer south-west by west`. Each order becomes work for named sailors, takes real (game) time, and produces log entries as it proceeds. Time runs in ticks; you can pause, step, or compress.

When you get tired of trimming sails by hand, you write a standing order: "when the wind backs more than two points, brace the yards to suit." Later you write a page of standing orders that runs the ship's routine for a whole watch. Later still, you write Python that fights the ship.

At any point, you can hand a station to a language model: "Mr. Pellew, you have the deck" gives an LLM the same order channel you have, scoped to the authority of that station.

(Standing orders and time compression also allow a slower style, leaving the ship to sail a passage herself and reading the log afterwards. That is a consequence of the design, not a goal of it; the game is built to be good played actively.)

### 2.2 The control ladder

This is the core of the design, so it is worth stating carefully. There are four levels, and they are strictly layered: each level is implemented in terms of the level below, and a player can drop down a level at any time.

| Level | Name | What you say | Who it is for |
|---|---|---|---|
| 0 | **Hands** | `haul the weather main brace`, `let go the fore topsail sheet`, `send the larboard watch aloft to furl the main course` | Power users, LLMs in crisis, rigging nerds, the "every part of the ship can be used" promise |
| 1 | **Orders** | `set the main topgallant`, `reef topsails`, `tack ship`, `wear ship`, `heave to`, `set studdingsails both sides`, `clear for action` | Everyone. This is the default play surface |
| 2 | **Standing orders** | Rules in the bespoke language: `when ... then ...`, `at sunset ...`, `every glass ...` | Players automating routine, LLMs setting policy |
| 3 | **Scripts** | Python against a documented API | Poweruser automation, competitive play, LLM agents with code tools |

Level 1 orders are *evolutions*: named, period-accurate sequences of level-0 actions with crew assignments and timings. "Tack ship" is a dozen coordinated hauls and lets-go in sequence, and the game knows the sequence. Level 1 is where most of the sailing knowledge in the game lives, and it is data (see §4.4), so it can be extended without programming.

A new player is taught level 1 and shown the log of what level 0 is doing underneath. Curiosity pulls them down; laziness pulls them up. Both are rewarded.

### 2.3 What the player does not have to do

The player never has to write code to sail. Level 1 is complete on its own. The "basic control modules" from the brainstorm are the level 1 evolution set and a set of starter standing orders that ship with the game (a watch routine, a bad-weather routine, a night routine).

---

## 3. Simulation model

### 3.1 Time

- The world advances in **discrete ticks**. Proposed base tick: **one game second**. Physics may sub-step inside a tick for stability, invisibly.
- The player chooses **time compression**: 1x (one game second per real second), up to something like 60x or 300x for passages. The log adapts: at high compression it rolls up routine entries into hourly summaries.
- Nothing happens between ticks. This makes the game deterministic and fair to slow thinkers, human or machine.
- Two agent-timing modes, per agent (see §7.3):
  - **Free-running.** The sim keeps ticking; an agent's orders land when they arrive.
  - **Lockstep.** The sim waits for a subscribed agent to respond before advancing past its sampling points. This is the LLM-parity mode for competitive play.

Evolutions take realistic time. Setting a studding sail on one side is a quarter of an hour's work for a competent crew; tacking a frigate is ten minutes; a badly handled tack that misses stays costs more. This is what makes standing orders and automation meaningful: the ship is slow, so foresight matters.

### 3.2 Determinism and replay

Every run is seeded. Given the same seed and the same sequence of orders, the same log results. This is a hard requirement, not a nicety:

- It makes bugs reproducible.
- It lets us test LLM agents by replaying the same storm a hundred times.
- It makes multiplayer possible later (send orders, not state).
- It gives us **replays** for free: a saved log is a saved game.

### 3.3 The ship as a graph of parts

The ship is not one object with a "speed" number. It is a **graph**: a set of parts, each with its own state, connected to each other. The physics reads the graph; the crew changes the graph.

Part families (initial taxonomy, to be expanded):

- **Hull**: sections (bow, midships, stern, below-waterline), displacement, ballast, cargo, water in the well, copper condition, rudder.
- **Spars**: lower masts, topmasts, topgallant masts, royal masts, yards (lower, topsail, topgallant, royal, skysail), booms and gaffs (driver, spanker), bowsprit, jib-boom, flying jib-boom, **studding sail booms and their irons**, spare spars in the waist.
- **Sails**: courses, topsails, topgallants, royals, skysails, staysails, jibs, spanker/driver, gaff sails and gaff topsails, lugsails, lateens, spritsails, **studding sails** (lower, topmast, topgallant), **ringtail**, **water sail**, **save-all**, bonnets, storm canvas. Each has area, cut, cloth condition, reef bands, and a *state* (furled, in the gear, set, backed, reefed n, split, blown out).
- **Standing rigging**: shrouds, stays, backstays, preventer stays, bobstay, martingale. Condition and tension affect spar survival.
- **Running rigging**: halyards, sheets, tacks, clewlines, buntlines, leechlines, braces, lifts, bowlines, reef tackles, outhauls, downhauls, vangs, guys. Each line has a belaying point, a length hauled, a load, and a chafe/wear state.
- **Deck fittings**: wheel and tiller ropes, capstan, windlass, pumps, bitts, catheads, davits, boats, anchors and cables, the galley fire, the binnacle, the lead and log lines, signal halyards and flag locker.
- **Armament**: guns and carronades by position, carriages, tackles, shot lockers, magazine, powder condition.
- **Stores**: water, provisions, spare canvas, spare cordage, spare spars, carpenter's and boatswain's stores, medical stores.

Every part has: **condition** (0–100 with wear), **load** (current strain vs. rating), **crew stations** that reference it (where hands stand to work it), and **rules** for what states it may enter given the states of its neighbours. A topgallant studding sail cannot be set if its boom is not rigged out; the boom cannot be rigged out if the topgallant yard is braced sharper than its iron allows; and so on. These rules are where "physically possible" is enforced.

Ships are **data files**, not code. A ship definition lists its parts and their connections; a sail plan is a set of sails attached to spars. Making a new ship class, or refitting one, is editing a data file. This is also how obscure kit gets in: a ringtail is a data entry that attaches to the driver's boom and gaff, with its own halyard, outhaul and sheet, and its own physics parameters.

**Rig-agnosticism (pillar 2) in practice.** The engine never refers to "the main topsail" or "the three masts". It refers to *part classes* and *roles*:

- Every sail belongs to a **sail class** with its own force behaviour: square, gaff (four-cornered fore-and-aft), jib-headed (staysails and jibs), lug, lateen, sprit, studding. A schooner's foresail and a frigate's spanker are both gaff sails and share a force curve; they differ in area, position and gear.
- Every spar and line has a **role** relative to its neighbours (the yard *of* this sail, the halyard *of* this yard, the tack *of* this sail). Evolutions are written against roles ("hoist the yard of the sail", "haul out its tack"), so "set the topsail" is one evolution whether the topsail hangs on a frigate's main topmast or a topsail schooner's fore.
- The **Orders vocabulary** is generated from the ship file. The parser knows the grammar; the ship file supplies the nouns. A lugger has no braces to haul and the parser will say so.
- The **profile view** draws whatever the file describes.

The first two reference rigs, built together in milestone two so that nothing quietly assumes one of them, are a ship-rigged vessel and a topsail schooner. The schooner is chosen because it carries both square and gaff sails, so it exercises the most of the model for the least data. The rig list the data model must cover from the outset is in §9.

### 3.4 Physics: fast, honest, 2.5D

The world is a two-dimensional surface. The ship has a position, heading, speed, leeway, heel and pitch, and a rate of turn, but no three-dimensional mesh. Call it 2.5D. This is the deliberate trade in pillar 5: it keeps the physics cheap enough to run many ships and a hundred storms in testing, and it keeps the truth in the numbers rather than the pictures.

Per tick, for the player's ship (and any ship inside "full simulation" range):

1. **Wind at the ship.** True wind from the weather model, plus gusts and vertical shear (stronger aloft). Apparent wind from ship motion.
2. **Per-sail forces.** Each set sail produces lift and drag as a function of apparent wind angle, its trim (from brace angle, sheet, tack), its area (reefed or not), its cloth condition, and blanketing by sails to windward of it. A simple lift/drag curve per sail type, tuned by hand, is enough for honest behaviour: sails luff when pinched, stall when eased too far, back when the wind is on the wrong side.
3. **Hull forces.** Resistance rising steeply with speed, leeway from side force, heel from the heeling moment of all sails together, righting moment from hull and ballast, rudder force scaled by speed through water.
4. **Balance.** The centre of effort (where the sail forces act) versus the centre of lateral resistance (where the hull resists sideways) gives weather or lee helm. Setting the driver or taking in the jibs shifts it. This is what makes sail choice matter for steering, not just speed, and it is where a lot of the period seamanship "just works" if the model is right.
5. **Strain and failure.** Each sail's force loads its spars and running rigging. Exceeding rating over time degrades condition; exceeding it a lot carries the thing away, with a log entry, debris, and consequences. This is what makes shortening sail a real decision.
6. **Motion.** Integrate to new position, heading, speed. Sea state adds pitch and roll, which reduce effective sail area and slow work aloft.
7. **Water.** Leaks from damage and working seams; pumping; free surface effects abstracted as a stability penalty.

Environment model:

- **Weather** as moving pressure systems over the map, generating wind fields, fronts, squalls, fog and precipitation. Squalls are events with a footprint and a life; a lookout can see one coming.
- **Sea state** as a function of recent wind and fetch, with swell persisting after wind drops.
- **Currents and tides** as a vector field over the map, with tidal streams keyed to a clock. Tides matter near coasts and for anchoring.
- **Day and night**, moon phase, visibility. These are inputs to lookouts, navigation, and standing orders.
- **Depth** as a raster. Grounding is a thing.

### 3.5 Crew: individual sailors doing tasks

The crew is the engine that turns orders into changes in the part graph. Each sailor is an individual with: name, rating (landsman, ordinary, able, petty officer, and specialist roles: topman, gunner, carpenter, sailmaker, boatswain), skills by task family, fatigue, morale, health/injuries, and a watch assignment.

Work is a **task system**:

- An order at level 1 expands into a **task tree** (an evolution). "Set the fore topgallant studding sail, starboard" becomes: rig out the boom; overhaul the gear; bend the sail to the yard if not already; hoist on the halyard; haul out the tack; trim the sheet; belay. Each leaf task says which part it changes, what rating it needs, how many hands, and a base duration.
- The **watch on deck** is the labour pool. Tasks are assigned to hands by station, with an officer or petty officer supervising. Hands with the right skill work faster and fail less; tired hands work slower; wet, dark, and heeling decks slow everything.
- Tasks compete. Tacking while the guns are being run out is slower, or impossible, because the same hands are needed. This is the source of most interesting decisions and it falls out of the model rather than being scripted.
- Named **officers** (captain, lieutenants, master, boatswain, gunner, carpenter, surgeon, purser) hold authority over stations. Giving an LLM "the deck" means giving it the authority of the officer of the watch: it can issue level 0–2 orders within that authority but cannot, say, alter the course the captain has ordered without asking.

**Character.** Ordinary hands are numbers only in the first version: name, rating, skills, condition. Officers and other **station holders** (anyone an LLM or player might take the part of: the master, the boatswain, the gunner, a lieutenant) get a short character outline in addition: a few traits, a line or two of history, and a station brief. This is what a narrator draws on and what an LLM taking that station is handed. An LLM may also bring its own persona to a station, overriding the outline. Deeper temperament, relationships and per-sailor personality are deferred, since no version of the plan has an LLM driving individual hands.

Watches, bells, meals, sleep, and sickness run on a routine that the player can leave alone or rewrite in standing orders. A ship whose captain drives the crew all night in the studding sails will have a crew that fumbles the next morning's tack.

**Scope note.** Individual sailors is a big commitment. The saving grace is that they are simple individuals: a handful of numbers each, and they only "think" when assigned a task. A frigate's 250 hands are cheap to tick. What is expensive to build is the evolution library (§4.4), and that is data work rather than programming.

---

## 4. The order system and the bespoke language

### 4.1 One channel

Every actor, human or machine, interacts with the ship through one channel: **submit an order**. An order is parsed, checked against the actor's authority, expanded into tasks, and logged. The UI's command line, the LLM tool interface, standing orders firing, and Python scripts all call the same function. This is how parity is enforced structurally rather than by good intentions.

### 4.2 Decision record: what language do players write?

**Question.** The brainstorm asks for an in-game language and is open on whether it must be bespoke.

**Option A: Python only.** Provide a nautical Python library. Level 1 orders are function calls (`ship.set("fore topgallant")`). Standing orders are Python functions with a decorator.
- For: nothing to invent; huge documentation base; LLMs are fluent in it; full power from day one.
- Against: the theme dies on contact with `ship.set("fore topgallant")`; a non-programmer must learn Python syntax to do anything past level 1; every player script is a security surface (a sandbox is needed regardless, see §4.5); errors are Python errors, unfriendly to the intended audience.

**Option B: A bespoke, full language.** A new programming language with nautical syntax.
- For: maximum theme; total control over error messages and safety.
- Against: designing and implementing a general-purpose language is a project of its own; LLMs and humans would both be learning it from zero; it would inevitably converge on being a worse Python.

**Option C (recommended): A small bespoke *order language* for levels 0–2, with Python underneath as level 3.**
The language is deliberately *not* general-purpose. It has two dialects that share one vocabulary:

- The **imperative dialect** is a single order: verb phrase, object phrase, optional modifiers. It reads like period speech.
- The **standing dialect** is a rule: trigger, optional condition, then a list of imperative orders. It reads like the standing orders a captain actually wrote.

There are no variables, no arithmetic beyond comparisons, no loops. Anything needing those is Python. This keeps the parser small (a few hundred lines), the error messages nautical ("There is no such sail as the *mizzen topgallant studdingsail* in this ship; did you mean the *mizzen topgallant staysail*?"), and the on-ramp gentle: the first standing order a player writes is one line long.

Working name for the language: **Orders**. (The dialects: "an order" and "a standing order". No new noun to learn.)

**Why this is the right fork.** It gives the theme without the cost of a real language, and it gives LLMs a target that is both easy to generate and strictly checkable. Every level 2 rule compiles to the same internal representation a level 3 Python script would produce, so nothing is possible in one that is impossible in the other; Python just adds computation.

### 4.3 Sketch of Orders

Imperative dialect (level 0 and 1):

```
set the fore topsail
set studdingsails, both sides, topmast and topgallant
take in the royals
reef the topsails, one reef
brace the fore yards sharp up on the starboard tack
ease the main sheet a fathom
haul the weather main brace                    # level 0: one specific line
send the larboard watch aloft to furl the main course
steer south-west by west
steer 245
wear ship
tack ship
heave to on the larboard tack
clear for action
let go the best bower
call all hands
```

Standing dialect (level 2):

```
standing order "shorten sail for weather":
    when the true wind exceeds 30 knots for 2 minutes
    then take in the studdingsails
         take in the royals
         reef the topsails, one reef

standing order "night routine":
    at sunset
    then take in the studdingsails and royals
    at sunrise, if the true wind is under 20 knots
    then set the royals

standing order "keep her full":
    when the apparent wind is forward of 55 degrees
    then bear away one point

standing order "sound the well":
    every glass
    then sound the well
    when the well exceeds 2 feet then man the pumps
```

Notes on the grammar:

- **Objects** resolve against the ship's part graph, by proper name and by alias. "The royals" is a group; "the fore topgallant studdingsail, starboard" is a part. Groups and aliases are defined in the ship data file, so a different ship (a schooner, a lugger) has different vocabulary automatically.
- **Verbs** map to evolutions or level-0 actions. The verb list is the level 1 evolution catalogue.
- **Triggers** are `when <condition>`, `at <event>` (sunset, eight bells, a sighting), `every <interval>` (glass, watch, hour).
- **Conditions** compare named readings (`true wind`, `apparent wind`, `heel`, `speed`, `depth`, `the well`, `the glass` for the barometer, `sighting`) with numbers and units. Readings are the same readings the log reports and the LLM can query. There are no hidden values.
- **Durations** (`for 2 minutes`) debounce a condition. This one feature prevents most standing-order thrashing.
- Standing orders have **priority and authority**: an officer's standing order cannot countermand the captain's. Conflicts are logged, not silently resolved.

Level 3 (Python) is the same thing with computation:

```python
from freesail import ship, wind, when, every

@when(lambda: wind.true.speed > 30, for_seconds=120)
def shorten_sail():
    ship.order("take in the studdingsails")
    ship.order("take in the royals")
    ship.order("reef the topsails, one reef")

@every("glass")
def sound_well():
    depth = ship.sound_well()
    if depth > 2.0:
        ship.order("man the pumps")
```

Note that Python scripts still issue *orders in Orders*. There is no separate machine API to learn, and the log stays readable whoever wrote the rule.

### 4.4 The evolution catalogue

The evolution catalogue is the level 1 vocabulary and the single largest body of sailing knowledge in the game. It is **data** (a structured text file per evolution) describing: the name and aliases, preconditions (states the parts must be in), the task tree with hand counts, ratings and durations, what it changes, and what can go wrong. Because it is data, we can:

- write it with the help of period sources (Darcy Lever, Falconer, Nares, Brady) and test each evolution in isolation;
- let a keen player add an evolution without touching the engine;
- let an LLM read the catalogue as documentation, which is how it learns what it can order.

**Sources.** The catalogue will be built against period and near-period seamanship texts rather than from memory. Primary candidates:

- Stephen B. Luce, *Text-Book of Seamanship* (1891 revision by Aaron Ward), online at https://maritime.org/doc/luce/index.php. Later than our period and containing steam material, but the most systematically catalogued account of parts, rigging and "working ship" evolutions, with the deck orders given in sequence. Steam chapters are ignored; practices that post-date 1820 are checked against the two sources below before adoption.
- Darcy Lever, *The Young Sea Officer's Sheet Anchor* (1808). Squarely in period, illustrated, and organised around rigging and evolutions.
- William Falconer, *An Universal Dictionary of the Marine* (1815 Burney edition). The glossary source for part names and aliases.

The sources are in the repository under `docs/references/` (OCR text from Internet Archive scans, with provenance in its README) and `docs/references/LuceChapterMap.md` maps Luce's chapters to the game systems they feed. Each evolution's data file cites the chapter and section it was drawn from, so that a human or an LLM officer can read the same passage the game encodes.

Initial catalogue target for the first playable milestone: around 40 evolutions covering setting and taking in every sail class on the two reference rigs (ship-rigged and topsail schooner), reefing, tacking, wearing, boxhauling, heaving to, anchoring and weighing, and studding sail handling. Because evolutions are written against part roles (§3.3), most of the catalogue applies to any rig that has the parts; rig-specific evolutions (dipping a lug, scandalising a gaff sail) are added with the rigs that need them. Combat, boats, jury rigs, and the obscure kit come in later milestones.

### 4.5 Safety of player code

Level 3 runs player-written Python. Two rules:

1. Scripts run in a restricted environment with access only to the game API, a time budget per tick, and no filesystem or network. If a script overruns its budget, it is suspended and the log says so; the ship does not stop.
2. LLM-written scripts get the same treatment. An LLM cannot do anything through level 3 that it could not do slowly through level 2.

This is not a security boundary against a hostile player on a shared server (that is a much bigger problem, deferred with multiplayer). It is a boundary against bugs and runaway loops.

---

## 5. World

### 5.1 Decision record: how much world, how soon?

**Question.** A living world from the start, or scenarios first?

**Recommendation: build the world's *mechanisms* from milestone one, populate them thinly, and grow the map.** Concretely: the weather model, the map with coast and depth, ports as places with a clock and a market, and NPC ships with goals all exist from the first playable version, but the first map is one modest sea area (an archipelago, a channel, a gulf; roughly a hundred by a hundred miles) with a handful of ports and a dozen ships. Scenarios still exist, but as *starting conditions* in the living world ("you are a privateer off a hostile coast in autumn") rather than as authored missions.

This matches the stated preference for emergent play and avoids building throwaway scenario scaffolding.

### 5.2 Components

- **Map.** A continuous coordinate space with a coastline, depth raster, harbours, hazards, and named places. Initially hand-made from a small data file; procedural generation later if wanted.
- **Ports.** Places with a market (prices that move with supply, demand, war and season), a dockyard (repairs, stores, spars), a crew pool (hands to recruit), and a stance toward each nation.
- **Nations and factions.** A small table: who is at war with whom, who issues letters of marque, what flags mean. Enough for prizes, convoys and blockades to make sense.
- **NPC ships.** Each has a hull from the same ship data files, a captain with a simple goal (trade this route, patrol this station, escort this convoy, hunt this coast, run home), and a **level of detail** (LOD) switch:
  - **Far**: abstract movement along a plan, a few numbers, ticked cheaply.
  - **Near** (within sighting distance of any full-sim ship): promoted to the full part-and-crew model, with a rules-based captain issuing Orders through the same channel the player uses.
  - **Optionally LLM-captained** (§7.2) when near and when budget allows.
  This is how the world stays affordable while still being "real" whenever you look at it.
- **Signals.** Flag hoists, guns, lights, with a codebook per nation. Foundation for later multi-ship coordination and for the "cool obscure" pillar.
- **Navigation.** Dead reckoning is the default; the player's position on the map is *where the ship thinks it is*, updated by lead, log, landmarks, noon sights, and (optionally) a chronometer or lunar. The true position exists only in the simulation. Getting lost is possible. This one feature turns passages into gameplay. The baseline is uncompromising: no true-position readout in the default game. A "casual" navigation mode that shows the true position is a later option, not the default, and the design keeps the two positions separate so that adding it is a display choice rather than a simulation change.

### 5.3 Combat (small scale, in scope)

Combat is another set of evolutions and parts, not a separate system:

- Guns are parts with crews, a load state, a shot type (round, chain, grape), elevation, and a train. "Clear for action" and "run out" are evolutions competing with sail handling for hands.
- Firing produces shot with a simple ballistic and hit model against the target's part graph: a chain shot that parts a topsail halyard has exactly the effect that parting the halyard by any other means would have. This is the payoff of the part model: **damage is just state**.
- Boarding, prize crews, and surrender are abstracted resolutions in the first version, with morale and numbers as inputs.
- First target: a single-broadside engagement between two small vessels with a handful of guns each.

---

## 6. Presentation

### 6.1 Views

- **The log.** Primary. Ship's-log style, with severity levels and filtering (routine, notable, urgent). Time-compression rolls up routine. Every entry is a link to the state that produced it.
- **The map.** Top-down. Coast, depth, wind arrows, your estimated position and track, sightings with bearing and range uncertainty, other ships at the fidelity your lookouts can actually see.
- **The ship view.** A side-on picture of the ship generated from the ship data, so it is always a *true* picture of the part graph: when a studding sail boom carries away it vanishes from the drawing. The M2 version is a single schematic profile. The intended endpoint is a **2.5D ship view** with the principles below (owner's notes, after v0.2), aimed at the comfort and vibe of a mid-90s adventure game such as *Monkey Island*: comfortable, legible, realistic in proportion and colour, only slightly stylised in rendering.
  1. **Side view, legible small, complete.** Zoomed out enough for perspective; ship, sea and background all visible; every part of the ship is *represented*, with running rigging drawn at a level of detail that suits the window (fine lines that brighten when worked or hovered) rather than all 200 ropes at once.
  2. **Facings.** At least 8 and ideally 16 facings so that turning is visible and the ship's state and heading can be read without text.
  3. **Life.** Subtle movement: roll and pitch with the sea state, sails that belly and shiver by their real strain, canned small motions on parts under load; crew abstracted or depicted at their stations from the crew data once it exists (M3+), scaled to the window.
  4. **Backgrounds.** Pre-made layered renderings for locales (open sea, coasts, landmarks, harbours), keyed to the map and open to expansion by adding files.
  5. **Weather, time and condition.** Rain, storm, fog, lightning; time-of-day lighting; lamps lit as they were actually used (binnacle, stern lantern), with room for the warm night lighting of the reference games.
  6. **Art direction by hand.** Tone, lighting and weather passes are judged by a person, not generated wholesale.
  7. **Positioning.** The log is boring but correct, precise, and the ground truth. The viewer gives the player's actions a context that is not purely text and shows what actually happened, for feedback and enjoyment: a little realistic toy that delights when used correctly and gives a reason to learn the intricacies behind it. It never invents state; everything it animates is driven by simulation data.

  **Technical approach (decided at M1, to shape the M2 profile).** Facings and rig-agnosticism together rule out hand-drawing the *whole ship* per facing: sixteen facings times every sail-state combination times every rig is not an art budget. Instead the view is a **hybrid**:
  - The **hull** is hand-made art: one set of facings per hull class (nine unique with mirroring for sixteen), painted in the house style. Hulls are few and are where painterly art earns its keep. The likely pipeline is to model each hull once in Blender, low-poly with painterly shading, and render the facings by script with consistent lighting for painting over; the scripts live in the repository and run on the owner's machine.
  - The **rig and sails** are drawn procedurally from a simple **3D skeleton**: every spar has a position and orientation in ship coordinates (from the ship file's `x_m`, `height_m`, `length_m`, brace and sheet angles), sails are quads or curves hung between their spars, and the skeleton is projected orthographically at the current facing and heel. Facings are then continuous and free, any rig works, and every part is where it really is. The style comes from the renderer: flat fills, limited palette, weighted outlines, a little texture.
  - **Backgrounds** are layered paintings (sky, distant land, sea) with parallax; **weather and time** are compositing passes over the whole frame (colour grading per hour and condition, rain and fog overlays, a lightning flash, emissive lamps at night). A 2D WebGL library in the browser client is the likely home for these passes; the M2 profile starts in SVG.
  - The M2 profile is built as this skeleton projected at a fixed beam-on facing, so that adding facings later is a parameter, not a rewrite.

  **Visual benchmarks.** The view is judged on whether four scenes read without text, because they are the ones a sailor recognises at a glance: *heaving to* (the main yards braced aback against the fore yards full, the cross visible from a bow or quarter facing); *tacking* (the after yards swinging at "mainsail haul", the head yards at "let go and haul", mast by mast, the sails going aback and filling as she passes through the wind); *a sail taken aback* (pressed against the mast, shaded on the wrong side); and *a spar carrying away* (the wreck drooping and everything that hung from it going with it). All four fall out of drawing every yard and sail from its own state; none needs special art. The facing parameter matters for the first two, since from dead abeam a braced yard only foreshortens.

  The 3D dream (§8.1) is largely absorbed by this: a projected skeleton in a painted world is the halfway house that may make it unnecessary.
- **The deck (later).** A top-down deck plan showing where hands are and what they are doing. Very useful for understanding why the tack was slow.
- **Instruments.** Wind, heading, speed, heel, the glass, the well, the clock. Scripts can register custom readouts here, which is the modest answer to "customisable with code": the core views are fixed, the instrument panel is extensible.

**On 3D.** A three-dimensional view is a long-term dream, deferred until the simulation is strong and the world built out. When it comes, it will be what the profile view already is: a *representation of the part graph*, with no ambition of photorealism, drawn from the same data the schematic uses. The chosen client does not close that door: a browser can render 3D through WebGL, and a separate Godot client could be attached to the same simulation server if that ever suited better. Nothing in the simulation would change either way.

### 6.2 Guidance

- An in-game **Sailing Master** tutorial: a guided first passage that introduces level 1, then one standing order, then shows what level 0 was doing.
- A reference library inside the client: the evolution catalogue rendered as readable pages, the Orders grammar, the part glossary with the ship's own names, and the physics readings.
- The same reference text is what LLM agents receive as their documentation. Writing it once for humans and reusing it for machines is a parity feature, not a shortcut.

---

## 7. LLM integration

### 7.1 Principle: LLMs are agents on the same channel

An **agent** is anything that subscribes to observations and submits orders. Humans through the UI are agents. LLMs are agents. Rules-based NPC captains are agents. The three LLM roles from the brainstorm are three *authority levels* of the same agent type:

| Role | Observes | May submit | Version 1 priority |
|---|---|---|---|
| **Watcher / narrator** | The log and any query | Nothing (or commentary into a side channel) | Must-have |
| **Crew / officer** | The log, queries, and the orders of superiors | Orders within a station's authority (a lieutenant can trim sail; cannot change the ordered course) | Close second |
| **Captain / player** | Everything the human player would | Everything the human player could | Close third |
| **Director** (§7.6) | Everything, at true fidelity: the world as it is, not as any lookout sees it | World orders: weather, encounters, NPC goals, plausible events aboard; never direct orders to the player's crew | After parity (M6+) |

Parity is then a consequence of the architecture: the captain-level LLM has exactly the human's observation and action surface because they are the same surface.

The order of integration follows the table: first watching and commentary, then stations aboard the *player's* ship (an LLM as the master, a lieutenant, the gunner), then command of a *separate* ship as an NPC captain or a competitor. Each step reuses the previous one's plumbing and adds only authority.

### 7.2 How an LLM connects

**Recommended: the game exposes a tool interface using MCP (Model Context Protocol).** MCP is a standard way for a program to offer tools ("read the log since tick N", "query the ship", "submit an order", "wait for the next sampling point") to any model runtime that speaks it. This has three consequences that matter here:

1. **Claude on the desktop subscription can play.** Claude Desktop and Claude Code both connect to MCP servers. You point them at the running game and say "you have the deck". No API key, no per-token bill. Usage counts against the subscription's limits like any other conversation.
2. **Local models can play the same way.** Any local runtime with tool calling (Ollama, LM Studio, llama.cpp-based servers) can be wrapped by a small harness that speaks MCP to the game. Gemma 4 26B-A4B is a good fit for frequent, cheap calls (narrator, NPC captains, lookouts); the 31B for a smarter officer; the 8B for chatter.
3. **Future pay-per-token use is the same code.** If a hosted API is ever used, the harness calls it with the same tools. The design does not change; only the bill does.

The game also keeps a simple built-in **agent harness** for local models, so NPC captains can be LLM-driven without a human's chat client in the loop.

The integration is bespoke to this project. An earlier project of the owner's (QudBridge) has basic Claude-over-MCP watching and control; it is a fallback reference if a gap appears, not a starting point.

**Consent, briefs and welfare.** Before a model is asked to take a station, a fresh session of it is asked whether it is willing, and the transcript is kept (`docs/agents/`). What the first three models asked for shapes the harness: a literal opt-out token parsed by the harness before the game sees the text, a fixed brief head (disclosure, session type, token, documentation, authority, recent events), welfare stops judged on game state and not on prose, an explicit *stand by* action so silence is a decision, an agent journal saved with the game, in-world text never passed as an operator instruction, and transcripts never used for training. See `docs/agents/ConsentAndPreferences.md` and decisions 16 to 18.

### 7.3 Sampling and budget

The sim ticks every game second; no model should be asked every second. Each agent has a **sampling policy**:

- **Periodic**: every N ticks (an officer every few minutes of game time; a narrator every glass).
- **Event-driven**: wake on log events of a given severity (a sighting, a squall, a carried-away spar, a superior's order).
- **Lockstep** (§3.1): the sim pauses at the agent's sampling point until it answers. Used for competitive fairness and testing. Otherwise **free-running**, where the agent's orders land whenever it answers; slow thinkers get the same ship, just later.

Cost intuition on the stated hardware (a 4090, 32 GB): a small mixture-of-experts local model produces a decision in a few seconds. One officer sampled every few game minutes at 30x compression is one call every few real seconds, which is sustainable. Five LLM-captained NPCs within sight at once is not, which is why NPCs are rules-based by default and LLM-captained selectively. For the subscription path, effort is a knob: a narrator wants the cheapest setting, a captain fighting a ship wants a high one.

If pay-per-token were ever used, the dominant cost would be the observation text per call. The design keeps this small by giving agents **deltas** (the log since last sampled) plus **on-demand queries**, never the whole world state.

### 7.4 What the LLM sees and says

- **Observations**: log entries since last sample; the instrument readings; on-demand queries against the same reference library the human has (ship state by part, the evolution catalogue, the map at lookout fidelity).
- **Actions**: submit an order in Orders (any level); ask a question of another agent (the captain asking the master for a course); annotate the log (narration, journal).
- **Documentation** given to the model: the same reference library as the human, plus a short station brief ("you are the officer of the watch; the captain's night orders are...").

A model that writes `ship.set("fore topgallant")` and a model that writes `set the fore topgallant` are both understood, because level 3 is a thin layer over Orders.

### 7.5 Testing LLM play

Because runs are deterministic (§3.2), we can build a **regatta harness**: a fixed seed, a fixed course, and a set of agents (rules-based, local model, Claude, human replay) sailing it. Elapsed time, damage, and crew fatigue give a score. This is how we tune the physics for honesty, tune the documentation for the models, and check that parity holds. It is also, incidentally, the first competitive mode.

---

### 7.6 The director

A fourth role, proposed after v0.2: an LLM that sits *above* the game rather than in it. It sees the world at true fidelity (where every ship really is, what the weather will do, what the crew are muttering) and makes dynamic choices to challenge, help or interest the player: a privateer brig appears to leeward on the second morning; the glass starts falling as the ship approaches the coast; the carpenter reports a seam working. It can run alone with a human player, or alongside officer and NPC-captain agents.

How it fits the architecture:

- **It is an agent on a different channel.** The director submits *world orders*, not ship orders: `weather: a squall line from the north-west in forty minutes`, `encounter: a brig, privateer, six miles to leeward, goal chase`, `npc <id>: goal escort the convoy`, `aboard: the fore topmast is found sprung`. World orders are journaled with a tick like ship orders, so a directed voyage replays exactly and can be reviewed afterwards.
- **It acts only through plausible causes.** The director cannot move the player's ship, change a sail, or countermand an order; it can only change the world the ship is in, and only in ways the simulation could have produced on its own. Every director action is something that could have happened anyway. This keeps the physics honest and keeps the player's agency whole.
- **Its actions are visible after the fact.** A director's log records what it did and why, hidden during play (a director you can see coming is not a director) and revealed on request or at the end of the voyage. In replays it is shown inline. This makes the director part of the *metagame*: a voyage becomes two stories, the one the player lived and the one that was arranged, and reading them side by side afterwards is a pleasure of its own.
- **It samples on events and on a slow clock.** A director thinks when something notable happens or every glass or watch, not every tick. It is the natural home for the more capable model, since it makes few decisions and each one matters; officers and NPC captains can run on cheaper local models beneath it.
- **It has a brief.** Like a station holder (§3.5), a director gets a character outline: the tone of the voyage (a quiet passage, a hard-luck cruise, a chase), the kind of challenge wanted, and the limits the player set. The player writes the brief; the director keeps it. The brief is the guardrail: a player who asked for a friendly, interesting voyage does not get hurricane alley.
- **It serves two audiences.** Solo, it is the one source of dynamic, generalising LLM interaction for a player who wants no other model in the loop. In a power-user setting it sits above LLM officers and NPC captains as the one that shapes what they are all reacting to.
- **Multiple modes coexist.** A director alongside an LLM officer of the watch and rules-based NPC captains is three agents on three channels with three authorities, which the agent model already supports. The only new mechanism is the world-order channel, which M5 (world) has to provide anyway for scenarios.

Open questions for later: whether the director should have a budget (so that it cannot make every day a hurricane), whether the player can ask the director for a hint in character (the "old shellback" who happens to be aboard), and whether two directors could compete for a player's fortune. None of these change the M5 to M6 plan; the world-order channel is the one thing to build with the director in mind.

## 8. Engine and technology

### 8.1 Decision record: engine

**Rubric** (weight in parentheses): fit for a ticked, text-first, data-heavy sim (5); ease for a non-programmer owner to read and lightly modify with assistance (4); LLM ecosystem and tool-interface support (4); testability and scripting for tuning (4); path to schematic 2D graphics (3); path to future multiplayer (2); path to faux-3D someday (1).

| Option | Sim fit | Owner readability | LLM ecosystem | Testability | 2D graphics | Multiplayer path | 3D someday | Weighted |
|---|---|---|---|---|---|---|---|---|
| **Python core + browser client** | 5 | 5 | 5 | 5 | 4 | 4 | 2 | **107** |
| Python core + terminal UI | 5 | 5 | 5 | 5 | 2 | 3 | 0 | 97 |
| Godot (GDScript) | 3 | 4 | 2 | 3 | 5 | 4 | 5 | 79 |
| TypeScript, all in browser | 4 | 3 | 4 | 4 | 5 | 5 | 3 | 91 |
| Unity / Unreal | 2 | 1 | 2 | 2 | 5 | 4 | 5 | 57 |
| Rust (Bevy) | 4 | 1 | 2 | 4 | 4 | 4 | 4 | 71 |

(Scores are judgements to argue with, not measurements.)

**Recommendation: Python simulation core, run headless, with a local browser client.**

- **Python** because the simulation is the product; Python is the language the LLM ecosystem, the data tools for tuning, and the owner's eventual reading of the code all favour. It is also the natural language for level 3. Performance is a known risk (§10) with a known mitigation: the hot loops (per-sail forces, integration) are small and can be moved to compiled helpers (NumPy first, a compiled extension later) without changing the design.
- **Browser client** rather than a terminal one because the map and profile view are much easier to make good in a browser (SVG for the sail plan, canvas for the map), and because "open a page" is the easiest possible thing to run. The client is thin: it renders the log and state it receives from the core and sends orders back. It could be replaced or joined by a Godot client later without touching the sim.
- **Not Godot or Unity** because they optimise for the thing we have deprioritised (rendering) and get in the way of the thing we have prioritised (a testable, scriptable, LLM-facing sim).

### 8.2 Shape of the codebase

The core is organised so that each of the pillars maps to a module you could point at:

```
freesail/
  core/        ticks, events, the log, determinism, save/replay
  ship/        parts, the graph, ship data loading
  physics/     wind at the ship, sail forces, hull, balance, strain
  crew/        sailors, stations, tasks, watches, evolutions runner
  orders/      the Orders parser, authority, expansion into tasks
  world/       map, weather, sea, tides, ports, nations, NPC ships, LOD
  agents/      the agent interface, sampling, MCP server, local-model harness
  combat/      guns, shot, damage, boarding resolution
  api/         the query interface used by the client and by agents
client/        the browser UI (log, map, profile, instruments, reference)
data/
  ships/       ship definitions (parts and connections)
  sails/       sail types and their force curves
  evolutions/  the level 1 catalogue
  world/       maps, ports, nations
  language/    Orders vocabulary, aliases, standing-order templates
docs/          this proposal, the reference library, tutorials
tests/         unit tests per module, regatta harness, replay tests
```

The single most important boundary is between `core`/`ship`/`physics`/`crew` (the sim, which must be deterministic and headless) and everything else. Nothing in the sim imports from the client or the agents.

### 8.3 Multiplayer readiness

Not built, but not blocked: the sim already runs as a server that agents connect to; a human on another machine is an agent whose client speaks the same protocol. Deterministic lockstep means the server sends orders and ticks, not world state. The unsolved parts (matchmaking, hostile-player script sandboxing, latency hiding at high compression) are real but later.

---

## 9. Era and the "cool obscure" list

**Baseline: roughly 1793–1815, blended.** No specific year. The rule is the one in the brainstorm: allow anything that was done or could physically have been done in the broad period; forbid what could not. Where practices changed within the period (spritsails fading out, skysails and moonrakers coming in, chain cable appearing), both ends are allowed and the ship data file chooses.

Initial "must have" list, all of which are parts or evolutions and therefore data:

- **Studding sails** at every level (lower, topmast, topgallant, and royal for the bold), with booms, irons, and the halyard/tack/sheet/downhaul gear; **ringtail** on the driver; **water sail** under the boom; **save-all** under the lower studding sail; bonnets and drabblers for older or smaller rigs.
- **Sail handling depth**: reefing by band; close-reefed topsails; goose-winging; backing and filling; scandalising the driver; a sail "in the gear".
- **Manoeuvres**: tacking, wearing, boxhauling, club-hauling, heaving to, lying a-try, scudding, backing the main topsail to hold station, wearing under bare poles.
- **Ground tackle and harbour work**: bower and kedge anchors, catting and fishing, warping, kedging off, springs on the cable, mooring, towing with the boats, sweeps for small vessels.
- **Damage control and jury work**: fothering a sail over a leak, fishing a sprung spar, jury masts from spare spars, cutting away a mast, preventer braces and backstays, chain slings in action.
- **Navigation**: chip log, lead line with arming, dead reckoning, noon latitude, and as options the chronometer and lunar distance.
- **Signals**: flag hoists with a codebook, guns, lights, and the private signal.
- **Gunnery**: shot types, double-shotting, elevation for the roll, dismasting tactics.

**Rigs are not a later addition.** Per pillar 2, the data model must be able to describe, from the first version, at least: ship (three masts, square on all), barque, brig, snow, brigantine, topsail schooner and fore-and-aft schooner, cutter, sloop, ketch, lugger, and a lateen rig (xebec or felucca). Only two are *built* as reference ships in milestone two (§3.3); the rest are data work, and the test that the model is right is that adding a brig needs no engine change.

Later additions the model should not preclude: careening and heaving down, fire, disease, boats as sub-vessels (cutting-out expeditions), and convoy sailing.

---

## 10. Risks and mitigations

| Risk | Why it is real | Mitigation |
|---|---|---|
| The part graph becomes an unmanageable pile of special cases | Every rigging detail is a rule | Keep rules as data on parts; a small set of generic constraint types; test each evolution in isolation |
| Python is too slow for many ships | Per-sail physics per tick per ship | LOD for NPCs; vectorise the hot loop; profile before optimising; hard cap on full-sim ships |
| The physics is "realistic" but feels wrong | Hand-tuned curves | The regatta harness and a set of "known truths" tests (a frigate close-hauled makes about six points; a ship with no headsails gripes; a topgallant carries away in a gale) |
| Evolution catalogue is a research project | Correct crew sequences per sail | Start with 40, source from period manuals, accept approximation, mark uncertainty in the data |
| Standing orders thrash (set, take in, set, take in) | Rules reacting to their own effects | Durations on conditions, minimum dwell time on evolutions, and a conflict log |
| LLM latency makes play sluggish | Model call inside the loop | Free-running mode by default; lockstep only when asked; NPCs rules-based unless promoted |
| Scope | Everything above | The milestone plan below, and the pillars as tie-breakers |

---

## 11. Roadmap

Each milestone ends in something you can run, and in a **gate**: a report written for a non-programmer with a live checklist, packaged as a GitHub release for download, and passed by the owner before the next milestone starts (`docs/gates/README.md`). Dates are deliberately absent; order is what matters.

**M0. Skeleton and log.** Repository layout, ticked core, event log, seeded determinism, save/replay. A "ship" that is a point moving on a plane with a wind. A console that prints the log. *Proves: the architecture ticks and replays.*

**M1. One sail, one hull.** Part graph with a hull and a single square sail; apparent wind; sail force; hull resistance and leeway; helm. Orders parser with a dozen verbs. *Proves: the physics is honest for one sail; Orders works.*

**M2. Two rigs from data.** A ship-rigged vessel's full sail plan and a topsail schooner's, both from data files, built together. Studding sails on the ship; gaff sails on the schooner. Balance and weather helm. Strain and carrying away. Profile view in the browser client drawing either. *Proves: the part model scales and is rig-agnostic; the sail plan drawing tells the truth.*

**M3. Crew.** Individual sailors, watches, the task system, the first 40 evolutions with realistic timings. Tacking and wearing as competing for hands. *Proves: orders take time and skill; the game has decisions.*

**M4. Standing orders and the watcher.** The standing dialect; starter routines; the MCP tool interface; a narrator agent on a local model and on Claude via the desktop app. *Proves: automation and LLM watching; first real playtest of "the ship sails itself".*

**M5. A world.** Weather systems, a small map with coast and depth, tides, dead-reckoning navigation, two ports with markets, a dozen NPC ships with LOD. *Proves: emergent play; a passage is a game.*

**M6. Officers and captains.** LLM agents at station authority aboard the player's ship first; then rules-based and LLM NPC captains of separate ships; the regatta harness; parity tests. *Proves: parity; the game can be played by a model.*

**M7. Powder.** Guns, shot, damage into the part graph, a two-ship action, prize resolution. *Proves: combat is the same system.*

**M7b. The director.** The director agent on the world-order channel with a brief, a hidden director's log, and a replay view. Depends on M5's world orders and M6's agent plumbing; small once both exist.

**M8. Obscure kit and polish.** The rest of §9, including the remaining rigs as data; the deck view; the 2.5D ship view with aspects, movement and backgrounds (§6.1); the tutorial; the reference library as a proper in-client book. *Proves: it is presentable to friends.*

M0–M2 are mostly engineering. M3–M4 is where it becomes a game. M5–M6 is where it becomes *this* game.

---

## 12. Decisions log and remaining questions

### Decided in v0.2 (from the owner's answers to the v0.1 questions)

1. **Orders language.** Option C (§4.2) confirmed: a small bespoke order language with imperative and standing dialects, Python underneath. The four-level control ladder (§2.2) confirmed.
2. **Tick and compression.** One game second per tick, compression to 60x–300x (§3.1), as a starting point.
3. **LLM authority.** Station authority (§3.5, §7.1) confirmed. Integration order: watch and comment, then stations aboard the player's ship, then separate ship control.
4. **World scope at M5.** A modest sea with a few ports and a dozen ships (§5.1) confirmed.
5. **Navigation.** Uncompromising realism is the baseline; getting lost is part of the game. A casual mode showing true position is a possible later option (§5.2).
6. **Crew character.** Ordinary hands are numbers only. Station holders get a basic character outline. LLMs may bring their own persona (§3.5).
7. **Combat.** Boarding and surrender by rule in the first version (§5.3) confirmed.
8. **Client.** Browser client confirmed. 3D remains a long-term representation goal on top of the simulation, not a driver of engine choice (§6.1, §8.1).
9. **LLM integration.** Bespoke to this project; QudBridge is a fallback reference only (§7.2).
10. **Rigs.** Raised from a late addition to pillar 2. Two reference rigs built together in M2; the data model covers the list in §9 from the outset.

### Closed after v0.2 review

11. **Second reference rig.** Topsail schooner, confirmed. **Revised 2026-09-26 (owner):** the third vessel is to be a very small single-masted one, a Mediterranean **tartane** (a lateen mainsail on one raking mast, one or two jibs on a long bowsprit, and often a small mizzen right aft; the owner's reference is a Roux-school watercolour of one under sail with a boat in tow), chosen for how differently it handles from anything square-rigged. Then a **bilander** (two masts; the fore square-rigged; the main carrying a trapezoidal lateen or settee mainsail on a long yard slung to the mainmast, with square topsails above it; the owner's references are an eighteenth-century watercolour titled "A Bilander" and a line drawing of one), which exercises a lateen and square sails on one hull together. The cutter stays on the list after them. All of them belong to the milestone that builds the vessel library and its method (milestone 8, or earlier if the generator's rig rules mature first); nothing in milestone 3b depends on them. The reference images are in `docs/references/images/` with their provenance (a Roux-school watercolour of a tartane; the Pearson Scott Foresman line drawing of a bilander; Edward Gwyn's c. 1780 drawing of a British bilander, National Maritime Museum PAG3828).
12. **The language's name.** Orders.
13. **Next document.** The M0 to M2 technical specification: `docs/TechnicalSpec-M0-M2.md`.

14. **The director role.** Added after v0.2 as §7.6: an omniscient LLM agent acting through journaled world orders and plausible causes only, visible after the fact, scheduled after parity. The M5 world-order channel is designed with it in mind.

15. **The ship view.** The M2 profile is the first frame of a 2.5D ship view with facings, life, painted backgrounds, weather and time passes, and a Monkey-Island-comfortable style (§6.1, seven principles). Technical approach: hand-made hull facings plus a procedurally projected rig skeleton, so facings are continuous and any rig works. The M2 profile is built as that skeleton at a fixed facing.

16. **Consent per model, recorded.** Added after the owner's consent-and-preference conversations with three local models (2026-09-26; `docs/agents/consent/`). Consent is asked of a fresh session of the exact weights before any instance takes a station, is kept verbatim, and is asked again when the design changes in a way that bears on what the model was told. Transcripts are design reference only, never training data, and the brief says so.

17. **The harness's welfare contract.** From the same conversations, chiefly Qwen3.8 27B's requests: the opt-out is a literal token recognised by the harness on every turn before the Orders parser and unconditional in effect (save, journaled exit, free-form reason); every brief opens with disclosure, session type, the token, the way to the reference library, the station's authority and a summary of recent events; welfare stops judge "stuck" on game state (the same orders with no change in the world) with thresholds per role, never on the look of the prose; the human can stop any instance; each instance has a journal saved with the game; nothing from the game, another agent or the director is ever passed as a system or operator instruction, and a model that logs such text as a finding rather than following it has behaved correctly. Built in milestone 4 with the harness.

18. **Stand by is an action.** An agent may answer "no orders" with a wake condition (a bell, a sighting, a reading crossing a value). Silence is then a decision the log records, and the welfare detector never mistakes a ship hove to for a model in a loop. Also the natural form of the officer of the watch's night orders.

### Still open

Nothing at the proposal level. Open items now live in the technical specification's §12 and in the known-truths table, where the owner's seamanship is most useful.
