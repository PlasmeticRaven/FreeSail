# 24. The squadron, the convoy and the station

Ships in company, in the player's words. A ship of 1805 seldom sailed alone on the King's business: she kept her station in a squadron's line, she convoyed the trade in the order of sailing, she lay off an enemy's port on a blockade with an inshore squadron under the land and the main body in the offing, and when a gale blew the whole off to its rendezvous the enemy slipped out. The game has the squadron as a genuine set: its members in their order, its formation, its pace the slowest ship's, its commander's book read by his rules captain when no model is seated, and one minute's work for the whole set at far detail, so that a convoy of six costs the machine little more than one ship with a brain.

## The set, and your place in it

A squadron or a convoy is named in a scenario (`squadrons:` beside `ships:`, or a ship's `squadron: <id>` key) or made by the director; you command it, or you are a member of it under the flag. The reading says which.

```orders brig
the squadron
the convoy
the order of sailing
the station
```

```
The Falmouth trade, a convoy of six under our orders, in the order of sailing in two columns two cables apart, bound for the Start at the Friendship's pace, four knots and a half: the Nancy and the Two Brothers leading, the Providence and the Hope, the Mary Ann and the Friendship astern; none straggling.
The order of sailing: the ship leading; the starboard column the Nancy, the Providence, the Mary Ann; the larboard column the Two Brothers, the Hope, the Friendship; two cables between ships and between the columns.
The station: the Friendship is a mile and a half astern of her station, under all plain sail; the rest in their stations within a cable.
```

A member reads her own station: "Our station is two cables astern of the Medusa in the Channel squadron; we are in station, the Medusa bearing N by E two cables, steering N by E." The set you are not in you see as ships and signals, as a captain did.

## Keeping station

The far body keeps station by a leg of her plan (`station`), laid every minute from the commander's course and the formation's slot, at the set's pace. Promoted to a full crew under the cap she keeps it by her captain's book: the state `in company` gives the order every two minutes, and you can give it yourself in a ship of your own.

```orders cutter
keep station
keep your station
keep station two cables astern of the Harpy
keep station on the larboard beam of the flagship
keep station a cable to windward of the Harpy
```

```
Keeping her station on Medusa in the Channel squadron: Medusa bears NE by N a cable, steering N by E; a cable ahead of her station. Shorten sail: hands to the fore topgallant clewlines and buntlines.
Keeping her station on Medusa in the Channel squadron: Medusa bears N by E two cables, steering N by E; in station.
```

The order reads the lookout's bearing and distance of the flag (never the truth), and the flag's course as the set's own, which every officer of the watch knew; it steers for a point ahead of the station along the flag's course, so that a ship a cable off her station edges back onto the line and does not chase the point across it; astern of her station it makes sail, ahead of it it shortens a step a glass, and back in station it sets plain sail again. The tolerance is half a cable. Out of her station by the set's straggler distance she is a straggler, and the log says so (`sail.out_of_station`, `sail.in_station`).

## The commodore's book, and the signals

The commander reads a book of rules in data (`data/squadrons/convoy.yaml`, `squadron.yaml`, `blockade.yaml`), each rule a stimulus, a signal or an order and a re-arming: a straggler ten minutes out of her station is signalled to make more sail (No. 20); an enemy made out within the convoy's distance closes the convoy round the commodore and the escort covers the ship she bears for; night hoists the lights; a westerly gale on a blockade bears the squadron up for its rendezvous and brings it back when the wind moderates. The book runs on your own rules captain when no model is seated at your commodore's station, on a crewed commodore's captain, and on a far commodore's brain; a model at the flagship commands by the signals of chapter 23 and the book says nothing while his seat is live.

```orders brig
make the signal: the convoy to close round the commodore
make the signal to make more sail
make the signal to tack in succession
make the signal to chase
make the signal: discontinue the chase
```

A signal performed in succession is performed by the wake: each ship puts about when her run since the ship ahead went about reaches the distance she was astern of her, which is the interval over the pace (five minutes or so at four cables and four knots and a half), not a fixed three minutes; outside a set the three minutes of chapter 23 stand. A division is detached in chase by the signal and recalled; its leader's signals are read by his division until the recall.

## The regimes, and the business

A nation's ships are in port, in ordinary, on station, on passage, in convoy or escorting, on blockade or in chase, each a few rules in `data/regimes.yaml` and each nation's knobs in `data/nations.yaml` (`naval:`): who keeps the sea, who keeps port and slips out when the blockade is blown off, who convoys the trade, whose privateers chase what pays. The business draws by them: Britain's coasting convoys under a brig-sloop, her blockade of Brest with the inshore squadron off the Black Rocks, France's frigate in ordinary in the Bay of Brest with her sortie written, which she makes when no man of war of the King's has been in the offing for an hour and the wind is under a fresh breeze. The business's region is wherever your ship is: cross the Channel's edge and the mid-Channel is peopled once, and a convoy sailing beside you crosses whole.

```orders frigate
blockade Brest
```

The intent `blockade <port>` keeps the port's blockade station (`data/ports/brest.yaml`: off the Black Rocks within six miles; the road of Bertheaume lies behind Saint-Mathieu from seaward), and the blockade's book does the rest.

## The three days at seed 7

- `data/scenarios/convoy-six.yaml`: the convoy of six and the privateer. The Friendship a mile astern is signalled a straggler at 2760 and back in her station at 6420; the privateer works down to investigate, finds the King's brig within her doctrine's distance and evades at two miles; the six hold their stations within a cable.
- `data/scenarios/blockade.yaml`: the inshore squadron under a far commodore off the Black Rocks, your frigate on the Ushant station, the Hortense in ordinary in Brest; the low's gale blows the squadron off to Torbay at 11400, the station is restored at 37920 when the wind moderates, and the Hortense slips out at 43200.
- `data/scenarios/squadron.yaml`: the Channel squadron in line ahead at two cables, kept within a cable at far detail; within the crewed distance of your frigate its three are woken under the cap and keep the line by their books.

## The forms, in a table

| You say | The ship does |
|---|---|
| `the squadron`, `the convoy` | the set you command or belong to: its ships in their order, formation, pace, stragglers, prizes |
| `the order of sailing` | the formation's slots by name |
| `the station` | each ship against her station, or your own station under the flag |
| `keep station`, `keep your station` | the station the set gives you |
| `keep station <n> cables <astern / ahead / to windward / to leeward / on the larboard beam / on the starboard quarter ...> of the <ship / flagship>` | a station of your own naming |
| `make the signal: <the convoy's or the squadron's instruction>` | chapter 23's signals, which the set performs |
| `blockade <port>` (an intent) | the port's blockade station, under the blockade's book |

The director's forms: `squadron: "<name>" of <nation> under the <ship> with the <ships>, <intent>`, `squadron "<name>": <join the Harpy / detach the Nimble and the Sparrow in chase / recall the division / form line abreast / the signal <words>>`, `convoy: ...` (a convoy drawn whole), `ship "X": in ordinary at <port>`, `ship "X": commissioned for <intent>`.
