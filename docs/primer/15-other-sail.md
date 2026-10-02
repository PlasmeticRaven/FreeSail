# 15. Other sail

Chapter 14 brought the first other vessel into the game, the pilot cutter coming off. This chapter puts a dozen more on the sea and says what the ship knows of any of them, which is what her lookout can see; what the captain may ask and order about a sail in sight; and what a world order is, which is the one kind of order the captain cannot give. The rules are the two that run through the whole of this milestone. **Everything outward arrives through something the ship models**: a sail reaches her through the lookout and nothing else, and what the lookout cannot make out the captain does not know. **The world keeps the truth and the captain keeps his account**: the world knows where every ship is and what she is about; the captain has a bearing, a distance by estimation and whatever the tops have made out, and the chart draws no more than that.

## What is on the sea

The other sail are hulls from the same four ship files as yours (the frigate, the topsail schooner, the cutter, the brig), each with a nation whose colours she wears or does not show, a captain with a goal and a plan. The brig has two descriptions in her one file, since the type served two trades: the brig-sloop of the Navy, sixteen ports a side, and the merchant brig of the trade, deep laden. A goal is one of a few a captain of the period had: trading a route, bound from one place for another, patrolling off a station, running home, carrying the mail, carrying a letter to the ship. The plan is the legs the goal makes, and she sails them at the speed her own file gives for her course in the wind she has, with the tide's stream in her track as it is in yours; a mark to windward she beats for. She is moved once a game minute, at the roll-up's cadence, and no oftener, which is what keeps a dozen of them cheap. Within two miles of you she becomes a nearer thing, with a heading that swings and a speed by the second, and a captain who keeps his course and does no more; a ship that fights or evades, or that a model commands, is a later milestone's, and the switch in the code says so in one line.

None of this is yours to read. There is no reading that gives another ship's position, her course by the truth, or her captain's intention. What you have is below.

## The lookout's words for a sail

A sail is seen from the masthead at the distance the horizon gives for the lookout's height of eye and her masthead's, within the weather's visibility and by day (at night a sail is seen only close aboard, as the land is). From a frigate's topmast head that is about twenty-five miles for another frigate's royals, twenty-three for a brig's, twenty-two for a cutter's. The first line is the hail, a bearing first and notable, so a standing order can act on it and a watcher wakes:

```
Sail ho! A sail on the larboard bow, bearing SW by S, distant three leagues.
```

Then, as she nears, the tops make out more of her at the period's distances, each a routine line as it changes: her rig and her course within four miles, her colours or their want within two, what she is within a mile and a half.

```
The sail on the larboard bow is a brig, standing to the eastward (E by N), under plain sail.
The brig on the larboard bow shows British colours, the red ensign.
The brig on the larboard bow is a merchant brig, deep laden.
```

A ship that shows no colours is said so, and that is all the lookout can say of her nation: "The brig on the larboard bow is a stranger, her colours not made out." A sail that goes over the horizon is lost: "The sail on the larboard quarter is out of sight." The pilot cutter of chapter 14 is one of these vessels and follows the same rules: "a cutter standing out from the land" at four miles, "the Falmouth pilot's cutter" within a mile and a half.

`the strangers` (also `what sail is in sight`) is every sail in sight, nearest first, each by her bearing, her distance by estimation and what has been made out of her so far; `a sail in sight` is the shorter row of chapter 14, in sight or not with the nearest sail's words. The distance by estimation is the lookout's judgement, a sixth out either way as the land's is, drawn once a sighting and held while she makes no way (chapter 12); the chart in the browser draws each sail at that bearing and that distance from the reckoned position, with a bar of doubt along the bearing that grows with the estimate, and the words beside it. Nothing draws where she truly is.

```orders frigate plain-sail
the strangers
what sail is in sight
a sail in sight
```

## Making her out, and the chase

`make her out` sends a glass aloft for the nearest sail, or for the one you name by what the tops have called her (`make out the brig`, `make out the stranger`), and answers at once with what the distance allows: the glass reaches half as far again as the eye, so a sail at five miles is a brig to the glass and a sail to the eye, and a sail at nine miles is nothing more to either, hull down. The answer is the same line the lookout would give in time, and the event `a stranger's colours made out` fires for the book when it is her colours the glass makes out.

`give chase` (also `chase the stranger`, `chase the brig`) puts the helm for her bearing, which is Luce's rule for a chaser, to keep the chase on the same compass bearing and so attain her in the shortest time (Luce 1884 p. 553). Given again for the same sail, it reads how her bearing has drawn since the last order and leads the course off the bearing by what brings the drift to nothing, worked from the drift, the lookout's estimate of her distance and your own speed and course, as the master would work it on the slate; the line says how far the bearing drew and how far the course is led, and it never puts her head nearer the wind than she lies close-hauled. It is a helm order and no more: the chase runs on at her plan's speed, you make what sail you please, and the book gives the order again every glass and as the tops make out more of her, which is how the naval cruise of this milestone chases its stranger. Within four cables of a vessel the log says she is within hail, with her course and her colours, and there this milestone stops: what follows a chase, the gun and the boat and the prize, is milestone 7's.

```orders frigate plain-sail
# rejected: make her out
# rejected: give chase
# rejected: chase the brig
```

The three are refused here because no sail is in sight; at sea with one in sight they are taken. The book's forms for a sail:

```orders frigate plain-sail
standing order "a sail": at a sail sighted then make her out
standing order "her colours": at a stranger's colours made out then give chase
standing order "lost": at a sail lost then shape a course for Falmouth
standing order "within hail": at a sail within hail then heave to
```

## What a world order is, and why you cannot give one

The scenario files of this milestone put the other sail on the sea, and may change the world as the day goes on: a weather system appended or a waypoint added to one; a ship put on the sea with a goal, or her goal changed; a letter left at a port or sent out by a cutter; a port closed to a nation or a price moved; a person named aboard or ashore. Each is a **world order**, an order to the world and not to the ship, and the scenario gives it at a time (`world_orders:` in `data/scenarios/*.yaml`); the lead's test harness may give one too, and the director of a later milestone will. Every world order is journaled at its tick with its source and written in the log at the driver's mark, so that a voyage replays exactly and can be read afterwards for what was arranged:

```
World order (the scenario): a cutter sent from Plymouth with a letter from the port admiral.
```

A world order can send the cutter; it cannot put the letter on the cabin table. Everything it causes reaches the ship through what she models: the brig it puts on the sea is a sail the lookout hails, the letter it sends comes aboard by the cutter within hail and is carried aft by the midshipman to wherever the captain is, the price it moves is in the next list the boat brings off, and the person it names ashore is one the boat may fetch. Nothing it does is a line in your log from nowhere.

The captain cannot give one. The grammar knows the channel's words and refuses them at the prompt in so many words, which is the game's promise that the captain plays the ship and not the world:

```orders frigate plain-sail
# rejected: ship: a brig "Harpy" of France at the Iroise, running home to Brest
# rejected: weather: low "the low" radius 450 km at 1805-06-13T04:00 -300 500 990
# rejected: port brest: closed to the United States
# rejected: message: at Brest from the Prefect maritime: "The captain is begged to dine."
# rejected: person: agent "Mr Fox" ashore at Brest
# rejected: world order: a gale tonight
```

## The two passages

Two scenarios ship with this milestone and are the gate's: **the merchant passage** (`data/scenarios/merchant-passage.yaml`), the schooner from Falmouth for Brest with forty tons of tin bought at the quay, out on the ebb, a sail sighted off the Lizard and not made out, the Iroise in her chart's words at the deep-sea lead's cast, the Goulet refused on the ebb on the pilot's word and taken on the flood, Brest entered by the pilot and the tin sold; and **the naval cruise** (`naval-cruise.yaml`), the frigate from Plymouth with her chronometer and the yard's provisions to the station off Ushant, kept two days under her book, a stranger sighted and chased, a message by the cutter. Each has its own book beside it (`.orders`), which is what the scenario loads; the starter book of chapter 11 is a choice, loaded at any time with `read the standing orders from data/standing_orders/starter.orders`, and neither passage needs it. Their numbers at seed 7 are pinned in the tests and measured in `docs/dev/TuningNotes.md`.

## The forms, in a table

| Form | Also taken | What it does |
|---|---|---|
| `the strangers` | `what sail is in sight` | every sail in sight: her bearing, her distance by estimation, what has been made out |
| `a stranger in sight` | `a stranger` | the strangers alone: every sail until her colours are made out, and one under none or another nation's after; for the book, `if a stranger in sight is in sight` |
| `a sail in sight` | `the stranger`, `the pilot cutter` | in sight or not, with the nearest sail's words |
| `make her out` | `make out the sail`, `make out the stranger`, `make out the brig`, `send a glass aloft`, `what is she` | a glass aloft: her rig, her course, her colours, as the distance allows |
| `give chase` | `chase`, `chase the stranger`, `chase the brig`, `stand after her` | the helm put for her bearing, led by the bearing's drift when given again |
| `take a bearing of the stranger` | `take a bearing of the sail`, `take a bearing of the brig` | a bearing of a sail, for the master's account |
| `at a sail sighted` | `at sail ho`, `at a sail made out`, `at a stranger's colours made out`, `at a sail lost`, `at a sail within hail`, `at the pilot's hail`, `at the cargo aboard`, `at the turn to the flood`, `at the turn to the ebb`, `at the course shaped`, `at steady on the course`, `at the pilot asks to be put off` | the events, for the book |

## Where it comes from

The look-out is Falconer 1780, LOOK-OUT ("a watchful attention to some important object ... land, rocks, enemies"), and the colours his COLOURS ("the flags or banners which distinguish the ships of different nations"); the chase is Luce 1866 ch. XXXIII, 'Chasing' ("the officers in charge of a vessel, either chasing or chased, should constantly take the bearings, and angle subtended by the masts of the other"), and Luce 1884 p. 553 ("by constantly keeping the chase on the same compass bearing, the chaser will attain the chase in the shortest time possible"); the horizon is the chart study's formula (C §5.5, 2.08 times the root of the heights in metres, Bowditch's 1.17 times the root in feet) with each ship's masthead from her file; the distances at which a rig, the colours and a ship herself are made out are judgement, named with their reasons in `docs/dev/TuningNotes.md`, package 36, as are the pace of a boat under oars and the level of detail's two miles. The polar a far-detail ship sails by is her file's own, the sails model of this game balanced against her hull's resistance at each point of sailing, within half a knot of the polars the truths measure by sailing her. The design is spec M5 §25 to §27, the proposal's §5.2, §6.1 and §7.6, and `docs/design/InwardAndOutward.md`.
