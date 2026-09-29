# FreeSail Technical Specification: Milestone 5, a world

**Status: scoping draft for the owner's review, 2026-09-29.** This chapter names what
milestone 5 proves, what the game already has to build on, the shape of the work in
gates, and the questions the owner has to answer before the sections are written in the
detail of the M3 and M4 specifications. Nothing here is decided until the owner rules on
§4; the sections that follow §4 are written after that.

Reads with: `docs/DesignProposal.md` §5 (the world), §7.6 (the director), decisions 4
and 11; `docs/design/ThreeDimensions.md` (the seaway as reduced motions);
`docs/design/InwardAndOutward.md` (the principle and the bounds on interiors);
`docs/design/Papers-and-Books.md`; `docs/design/Scenario-StrikingColours.md` (the gaps
a scenario needs from the world); spec M4 §24 open items 7 (windage under bare poles) and
11.

## 1. What milestone 5 proves

*Emergent play; a passage is a game.* A ship leaves one port for another across a small
real sea with weather that comes from somewhere, a coast that can be hit, a tide that
sets her, a position she has to reckon, other sail on the horizon, and a market at the
far end that makes the passage worth making. The captain who is a language model has the
same sea: every one of those is a reading, a log line or an order (inward and outward).
The world-order channel exists, journaled, for scenarios now and the director later.

## 2. What the game has to build on

- **A plane, not a sea.** The ship moves in metres on a flat plane (surge, sway, yaw, heel
  quasi-static); the map draws her track. Latitude is one number for the sun. There is no
  coast, depth, tide, current or sea state, and no position except the true one.
- **One wind.** A single true-wind field over the plane with slow wander and gusts, driven
  by hand or by the weather script's waypoints (M4c). No pressure, no sky, no
  visibility, no rain.
- **Readings and the log.** The registry (M4a) is how a captain, a standing order and a
  model read the world; the roll-up and the samples (M4c) carry it at every compression.
  Everything M5 adds to the world is a reading first.
- **Scenarios** as files: a seed, a start, a latitude, a ship, a wind and a weather
  script, saved with the game and replayed.
- **The ships.** The frigate and the topsail schooner, each with a crew.
- **The agent model.** Stations, briefs, doors, consent; the watcher. Officers and
  captains are M6, but M5's readings are what they will read.
- **The pace.** About a thousand ticks a second for one frigate on the build machine
  (truth 51). A dozen ships at full detail is not affordable; a dozen at far detail is.

## 3. The shape: three gates

The M4 pattern, three short gates with a human check at each, each leaving a passage
the owner can sail and a playtest form to fill. The owner's ruling (2026-09-29): this is a
big milestone and the baseline for everything after it, so the heavy packages go to the
strongest model available for the building (Fable), not the usual Opus, with the lead
reviewing as before.

**5a. The sea and the sky.** Weather that comes from somewhere: a small number of
pressure systems moving over the area, each a centre and a gradient, giving the wind's
direction and strength everywhere and the barometer its meaning; the sky (cloud, rain,
visibility) as words from the same state; the weather script kept for scripted days as a
path the systems follow. A sea state from the wind's recent history, and the reduced
motions of `ThreeDimensions.md` (roll, pitch, heave as a few numbers with time
constants), with their consequences: work aloft slower and riskier, speed lost in a head
sea, the strain model fed. New readings: barometer and its tendency, sky, visibility, sea
state, the ship's motion. Gate: the 4c day sailed again under a system instead of a
script, and the watcher's finding 5 (nothing for weather but the wind) answered.

**5b. The chart and the reckoning.** The map as data: a coastline, a depth raster,
hazards, named places, from public sources at a coarse resolution for one sea area. Two
positions kept apart from the first line of code: where she is, and where she is
reckoned to be. The reckoning from the log-line and the compass by the traverse table;
corrected by the lead, by bearings of landmarks in sight, by a noon latitude, and by a
chronometer where the scenario gives one. Tide as a simplified model: heights at the
ports and streams by area, semi-diurnal with springs and neaps, setting the ship. A
grounding is an event with consequences. The viewer's map shows the chart and the
reckoning, never the truth. Gate: a passage with a landfall made by the reckoning, and
one made wrong.

**5c. Ports, nations and other sail.** Two ports as places: an anchorage and a mooring,
the boat, the market with prices that move, the dockyard, the crew pool, a stance to
each nation; the nations table. A dozen NPC ships at far detail, each a hull from the
ship files, a captain with a goal and a plan, moved cheaply; sighted by the lookout
("sail ho", the bearing, what she looks like from the tops); at near detail an object with
a heading and a speed and a simple keep-course captain, the crewed model and the
rules-based captain being M6's. The world-order channel: orders to the world (weather,
ships, news) that only a scenario or the director gives, journaled and visible after the
fact. The inward minimum `InwardAndOutward.md` names: named people with a position and a
state, the cabin and the deck as places, the boat alongside, so that a message can come
through the door. Gate: the passage between the two ports with a cargo, a sighting, and
the log a captain could keep.

## 4. Questions for the owner

**Rulings of 2026-09-29.** 1: a real sea, and older coast and depth data where it can be
had (dredging and shifting banks have changed the approaches), built so that the map can
grow toward the whole Atlantic and, as a long-term dream, the world. 2: both, the
schooner trading and the frigate cruising, from the same ports. 3: as recommended, but
lunars are to be explored before they are ruled out. 4: to be explored before deciding.
5: far detail with sightings for this milestone, to be revisited as it progresses. 6: the
systems, with something more in depth explored first. 7: yes. 8: three gates. The
explorations are the studies `docs/design/ChartData.md`, `Navigation1805.md`,
`Tides1805.md` and `WeatherSystems.md`.


1. **Where.** A real stretch of sea or an invented one? The gate's day already names
   Falmouth. The lead's recommendation is real: the Western Approaches and the western
   Channel, Falmouth to Ushant and Brest, about a hundred miles square, built from
   public-domain coast and depth data at a coarse resolution. Real places bring the
   period's own sailing directions and tide tables as sources, which is the "cool obscure"
   pillar for free; an invented sea brings nothing but freedom.
2. **Who the player is in M5's world.** A King's frigate has no market; a privateer or a
   merchant has. The proposal makes this a scenario's starting condition. Which one does
   M5 build first: the merchant passage with a cargo (the market matters), or the naval
   cruise (the market is stores and repairs only, the ports a dockyard and a victualling
   yard)? The lead recommends the merchant passage in the schooner and the naval cruise
   in the frigate, both from the same ports, since the ports are the same work.
3. **How deep the navigation goes.** Dead reckoning, the lead, bearings and a noon
   latitude are the floor. A chronometer in 1805 is a captain's own possession and gives
   longitude; lunars are a morning's arithmetic. The lead recommends the floor plus a
   chronometer as a scenario item, lunars never.
4. **The tide.** Real harmonic tides for the Channel are a large data job; a simplified
   semi-diurnal model with springs and neaps and streams by area gives the gameplay (the
   set, the window to get in) for a fraction of it. The lead recommends the simplified
   model with the ports' real establishment times from the period tables.
5. **Other ships.** Far detail only in M5, with sighting and an object with a course at
   near detail, the crewed promotion left to M6? The lead recommends yes; a dozen ships
   sailed in full is not affordable and the captain to sail them is M6's work anyway.
6. **Weather.** Pressure systems (the barometer means something, the wind veers as a low
   passes) or a table of weather types with transitions? The lead recommends the systems,
   few and simple, because every reading then has one cause and the watcher's lesson from
   playtest 7 (wait for the trend) becomes seamanship.
7. **The seaway.** In 5a as reduced motions with consequences, or deferred to 5b or 7?
   The lead recommends 5a: the sea state is a weather reading, and the motions are what
   make a gale a gale for the hands aloft.
8. **Three gates or two.** The lead recommends three, as in M4; 5b is the one that turns
   a passage into a game and deserves its own check.

## 5. Sections to be written after §4 is ruled

The weather systems and the sky; the sea state and the reduced motions; the chart data
and its sources; the two positions and the reckoning's instruments; the tide; the ports;
the nations; NPC ships and their levels of detail; the world-order channel; the scenario
file's growth; the readings each adds; the orders each adds (`heave the lead`, `take a
bearing of`, `work up the reckoning`, `come to an anchor`, `send the boat`); the viewer's
chart; performance; truths 52 onward; the gates in detail; the playtest forms.
