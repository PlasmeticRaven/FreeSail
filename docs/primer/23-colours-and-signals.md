# 23. Colours, the private signal, a hail, a signal made and read

The voice between ships, in the player's words. Before a gun is fired a captain of 1805 knew whom he had to deal with by three means and no more: the colours she showed, the private signal of the month, and the hail within the trumpet's reach; and he worked his consorts and his convoy by the signal book. The game has each as a thing of the ship's state, seen by the lookout at the range the thing carries, and nothing is refused for being unwise: a shot under false colours is a pirate's act, and the log says so.

## The colours

Your colours are a state the other ships' lookouts read: shown (your own ensign), none, false (another nation's, the ruse the law allowed until the first shot), struck, or the ensign union down in distress. The lookout of every ship, far or near, reads the nation *shown*, never the true one, so a French privateer under British colours is "British colours, the red ensign" to the King's captain who makes her out at two miles (three with the glass aloft), and the truth is the director's alone.

```orders cutter
hoist the colours
hoist French colours
hoist false colours
haul down the colours
hoist the ensign union down
the colours
```

```
False colours hoisted: French colours, the tricolour. The ruse is the law's until the first shot; a gun fired under them makes her a pirate to every nation.
Her true colours hoisted: British colours, the red ensign, the false ones down.
The colours: British colours, the red ensign.
```

`hoist false colours` with no nation named shows the principal enemy's. `haul down the colours` shows none; under fire it is the strike by the custom of the sea, and the log says so. `strike the colours` is chapter 22's and never refused. When another sail shifts hers the lookout says it: "The brig hoists her colours: French colours, the tricolour"; "The cutter hauls down her colours." A rules captain shows his true colours before his first shot; a privateer's doctrine closes her stranger under the enemy's colours and shows her own at four cables. If you fire under false or no colours the first shot is told once ("Fired into the brig under false colours: a pirate's act by the law of nations; every ship that saw it and every port that hears of it will hold us so"), the ports' stance turns against you, and every captain whose people had you in sight holds you a pirate from then on, whatever colours you hoist after.

## The private signal

The recognition signal: a small table per nation per month, issued under seal to the King's ships (a merchantman, a packet, a fisherman and a privateer never had it), the challenge a flag at a named place by day and lights by night, the reply another. The actual tables are lost; the game's are drawn under the seed in the period's form, the same for every ship of one nation in one world. It is a paper of the cabin:

```orders cutter
the private signal
# rejected: show the private signal
# rejected: answer the private signal
```

The hired cutter of this book carries no table, and the orders are refused with the reason ("there is no private signal aboard: the month's table is issued to the King's ships under seal"); in a King's ship, a cruiser or a commodore's (and in any ship whose scenario gives `papers: {private_signals: true}`) they read:

```
The private signal: by day, a blue flag at the mizen topmast head; the reply, a chequered flag at the mizen topmast head, with the ensign at the ensign staff.
Bend on the signal: the private signal (a blue flag at the mizen topmast head; the table for June 1805).
```

A King's ship's rules captain makes it to every strange sail within the flags' range once her colours are made out, and reads the answer from the minute his flags are up: right makes her one of his; a reply and the wrong one is the tell whatever her colours ("The cutter answers the private signal wrong: a stranger under false colours, an enemy"), and he gives chase by his doctrine; no answer under his own colours is the tell for a man of war's rig, and leaves a trader's rig "a merchantman, who has none; a stranger to be spoken". A ship with no table cannot answer; a privateer may bluff a guess, which is wrong by every table but her own.

## A signal made and read

The books are the nation's (`the signal book` in the library: Britain's from Howe's of 1790 and the Admiralty's of 1799 with Popham's dictionary of 1803; the French smaller; every other nation the basic system every navy had), and a signal is made by its meaning, never by a number you must know:

```orders cutter
make the signal to tack in succession
make the signal: enemy in sight bearing NW
make the signal No. 16
make the telegraphic signal: England expects that every man will do his duty
# rejected: answer the signal
# rejected: repeat the signal
haul down the signal
the signals
```

```
Bend on the signal: No. 54, tack in succession (No. 54, tack in succession, the British numerary book; a minute to run it up).
The signal is up: No. 54, tack in succession.
Bend on the signal: the telegraphic signal, England expects that every man will do his duty (12 hoists, 12 minutes, the telegraph flag over each: England 253, expects 269, that 863, every 261, man 471, will 958, do 220, his 370, D 4, U 21, T 19, Y 24; spelt letter by letter where the book has no word: DUTY).
```

`answer the signal` and `repeat the signal` want a signal read from another ship first, and are refused until one has been.

The hoist is an evolution: three hands at the halyards and a minute a hoist, a telegraphic sentence a minute a word, and it breaks out when the hands have run it up, not when you ordered it (a hoist queued behind a wear waits its hands). By night the same order makes the night book's lights and false fires; in fog the fog book's gun, fired by the battery, since the flags are not to be seen. The signal flies a glass at most and then comes down of itself.

It is read at the other end by her lookout: "The brig-sloop of war makes a signal: two flags at the main" at the flags' range, and a minute later, if her library holds the book, "The brig-sloop of war's signal is No. 54, tack in succession"; without the book, "a signal we cannot read: not of our book". A rules captain who reads it hoists the answering pendant, and performs it when the sender is the ship he is under the orders of (the scenario's `under_the_orders_of`, or the director's word): a convoy of four merchantmen under your orders reads your `make the signal to tack in succession` from the convoy's book and puts about one after another, the leader first and each when the ship ahead of her has (`data/scenarios/convoy.yaml`). No ship obeys a signal of a ship she is not under the orders of; she logs it. Your own ship obeys nobody's: you read the signal and choose.

## A hail

Within four cables a ship is spoken by the trumpet, and the answer is a line heard on deck (the orders, which want a sail in sight within hail and so are not run through this book's empty sea):

```
hail her
hail the brig: what ship is that?
hail the brig what ship is that?
say to the brig: heave to, I am sending a boat
hail Nancy, whence come you?
```

The sail is named by her rig (`the brig`, `the fore topsail schooner`), by her name when it is known (`Nancy`, `the Nancy`), or as `her` for the sail engaged or the nearest; the colon after her is optional, and what follows is said as written. `hail <words>` with no sail named is the lookout's hail of the deck (chapter 19).

```
Hailed the brig by the trumpet: 'What ship is that?'. The brig answers: 'The Nancy of Guernsey, from Guernsey for Falmouth, a cargo of salt.'
```

Beyond four cables the hail is refused with the distance. A rules captain answers by the table in the period's form, by his role and his nation: a King's ship names herself ("His Majesty's cutter Sherbourne. And what ship is that?") and heaves to for nobody; a merchantman answers what ship, whence, whither, her cargo and the news, and heaves to for a King's ship not at war with her; a privateer under false colours lies under the flag she shows, with a name and a port of that nation; a model at her captain's station hears your words and answers in his own. A rules captain who comes within hail of you hails you first ("She hails: 'What ship is that?'"), and `say to her: His Majesty's cutter Sherbourne` is read for your nation by his table. Two rules captains within hail of one another exchange the standard questions once, written to the log in the lookout's hearing.

## The lights and the bell

By night a ship shows what her order and her book give her: a stern lantern for ships in company, the top lights of a squadron, a fishing boat's lantern at her nets, a merchantman often none; the lookout sees a light at three miles on a clear night beyond the hull's loom at the mile ("A light two points on the bow, bearing SW"). In fog a ship keeping the fog signals rings her bell every two minutes at anchor, fires a gun every half hour under way in company and beats the drum alone, and is heard beyond the visibility ("A bell heard in the fog on the larboard bow, bearing W").

```orders cutter
hoist the lights
hoist the top lights
show no lights
keep the fog signals
cease the fog signals
the lights
```

## The forms, in a table

| Order | What it does |
|---|---|
| `hoist the colours` | her own colours shown |
| `hoist French colours` / `hoist false colours` | another nation's (the principal enemy's when none is named): the ruse, until the first shot |
| `haul down the colours` | none shown; under fire, the strike |
| `hoist the ensign union down` | the signal of distress (with `fire a gun to leeward`) |
| `show the private signal` / `answer the private signal` | the month's challenge and reply, with a table aboard |
| `make the signal <meaning>` / `make the signal No. <n>` | a signal of the book by day, the night book's lights by night, the fog book's gun in fog |
| `make the telegraphic signal: <words>` | Popham's free sentence, a hoist a word (a well-built book with a dictionary) |
| `answer the signal` / `repeat the signal` / `haul down the signal` | the answering pendant; the last signal read made again; the hoists down |
| `hoist the lights` / `hoist the top lights` / `show no lights` | the lights by night |
| `keep the fog signals` / `cease the fog signals` | the bell, the gun or the drum in fog |
| `hail her` / `hail the <sail>: <words>` / `hail the <sail> <words>` / `say to the <sail>: <words>` / `hail <name> <words>` | the trumpet within four cables; the colon optional, the sail by her rig, her name or `her` |
| `the colours`, `the signals`, `the private signal`, `the lights` | the readings |

Every signal of every book is listed in `the signal book` of the library, with its number, its meaning and its source; the hoists made up in the period's form rather than read from a book are marked so in the files, under `data/signals/`.
