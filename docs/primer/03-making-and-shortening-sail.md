# 3. Making and shortening sail

## Plain sail

*Plain sail* is the working canvas of the ship: on the frigate the courses, the three topsails, the three topgallants, the fore topmast staysail, the jib and the spanker; on the schooner the foresail, mainsail, fore topsail, fore topgallant, fore staysail and jib. Everything beyond it, the royals, the flying jib, the main topmast staysail, the gaff topsail and the studding sails, is *light sail* or *all sail*. The ship file's `plain sail` and `all sail` groups say exactly which sails these are for each ship.

One order does it:

```orders frigate
set plain sail
```

and the log answers with one line per sail as the hands go to work, and one, marked `*`, as each is set:

```
  Morning watch (04:06)  Order: set plain sail.
  Morning watch (04:06)  Hands aloft to loose the foresail.
  Morning watch (04:06)  Hands aloft to loose the mainsail.
  Morning watch (04:06)  Hands aloft to loose the main topsail.
  ...
  Morning watch (04:06)  Clear away the fore topmast staysail; man the halyards.
  Morning watch (04:06)  Clear away the jib; man the halyards.
  Morning watch (04:06)  Hands to the spanker halyards and outhaul.
  Morning watch (04:07)  Laid aloft and loosed the foresail.
* Morning watch (04:07)  Set the fore topmast staysail.
* Morning watch (04:07)  Set the jib.
* Morning watch (04:09)  Set the spanker.
* Morning watch (04:09)  Set the foresail.
* Morning watch (04:09)  Set the mainsail.
* Morning watch (04:11)  Set the main topsail.
```

`make all sail` (*crowd sail*, *crack on*) sets plain sail and then the royals, flying jib, staysails, gaff topsail and studding sails both sides, passing over anything the ship has not got. `shorten sail` (*take in sail*, *snug her down*) takes in the studding sails, royals, flying jib, topgallants and gaff topsail and puts one reef in the topsails. These three are lists of ordinary orders in `data/vocabulary.yaml`; anything they cannot do is reported in the same log line after "Not done:".

## The order of setting

A ship sets sail from the middle out and takes it in from the outside in. Luce's chapter on the officer of the deck at sea gives the evolutions in the order they are wanted (Luce 1866, ch. XXIII At Sea, 'Making and Taking in Sail': courses, topsails, royals, topgallant sails, head sails, studding sails), and the sequence is:

1. **Topsails**, the sails that do the work and stand the most wind.
2. **Courses** and **head sails**, the drivers and the balance.
3. **Spanker**, to hold her up to the wind.
4. **Topgallants**, then **royals**, as the breeze allows.
5. **Studding sails**, in a fair wind only.

```orders frigate
set the topsails
set the courses
set the fore topmast staysail
set the jib
set the spanker
set the topgallants
set the royals
set the flying jib
set the main topmast staysail
```

Taking in runs the other way: light sails first. *Take in* leaves a square sail *in the gear*, hauled up to its yard by clewlines and buntlines but not yet stowed (Falconer, *Buntlines*); *furl* sends the topmen out on the yard to pass the gaskets and make it fast (Falconer, *Furling*). A sail in the gear can be set again quickly; a furled sail must be loosed first.

```orders frigate all-sail
take in the studdingsails
take in the royals
take in the flying jib
take in the topgallants
furl the royals
furl the topgallants
haul down the main topmast staysail
# rejected: take in the royals
```

The last is refused with "Nothing done: the fore royal is already furled; the main royal is already furled; the mizzen royal is already furled." The synonyms are period: `clew up`, `haul down` (head sails), `douse`, `hand`. What the log says:

```
  Morning watch (05:20)  Order: take in the fore topgallant.
  Morning watch (05:20)  Hands to the fore topgallant clewlines and buntlines.
  Morning watch (05:21)  Clewed up the fore topgallant.
* Morning watch (05:22)  Took in the fore topgallant; hanging in the gear.
  Morning watch (05:22)  Order: furl the fore topgallant.
  Morning watch (05:22)  Lay aloft and furl the fore topgallant.
* Morning watch (05:25)  Furled the fore topgallant.
```

## The words of command

Each evolution is a data file in `data/evolutions/` with the steps a working watch goes through, and the log prints the step names as Luce prints the orders. For a square sail (`set_square.yaml`; Luce 1866, ch. XXIII, 'To set a Topsail'; Lever, 'Setting the Topsails'):

| The log says | What is happening |
|---|---|
| *Hands aloft to loose the fore topsail.* | the topmen lay aloft and cast off the gaskets |
| *Laid aloft and loosed the fore topsail.* | the sail hangs loose from the yard |
| (sheet home) | the sheets haul the clews out to the yardarms below |
| *Set the fore topsail.* | the halyard hoists the yard; the sail is drawing |

A course's yard does not hoist: its tack is hauled aboard and its sheet aft instead. A gaff sail (`set_gaff.yaml`): "Hands to the spanker halyards and outhaul", "Cast off the gaskets and cleared away the brails", "Set the spanker". A jib (`set_jibheaded.yaml`): "Clear away the jib; man the halyards", "Set the jib". A studding sail (`set_studding.yaml`): "Stand by to set the...", "Got the ... out and bent on the halyards and tack", "Set the ...".

Every step has a fixed time in this milestone (about four and a half minutes for a topsail, three for a course or a spanker, under two for a jib, four for a studding sail, five for a reef), scaled up to double in a strong breeze and a heavy heel. **The crew's part in these timings is not yet modelled**: it makes no difference who is aboard or how many hands are on deck, and every sail of a group is worked at once, as if the ship had hands for all of them. Milestone 3 replaces the fixed times with crew-derived ones (`docs/TechnicalSpec-M0-M2.md` §8.4).

## Reefing

"The intention of the reef is to reduce the surface of the sail in proportion to the increase of the wind; for which reason there are several reefs parallel to each other in the superior sails" (Falconer, *Reef*). The topsails have three reef bands; the courses one; the spanker two; the schooner's mainsail three and her foresail and topsail two. Royals, topgallants and head sails have none and cannot be reefed.

To reef a topsail the halyards are settled and the yard clewed down, the reef tackles hauled out, the topmen lay out along the yard, pass the earings at the yardarms and tie the points along the band, and the yard is hoisted again (Luce 1866, ch. XXVII Reefing, 'Reefing and Hoisting'; Lever, 'Reefing Topsails'). The log:

```
  Morning watch (04:31)  Order: reef the topsails, one reef.
  Morning watch (04:31)  All hands reef the fore topsail.
  Morning watch (04:32)  Settled the fore topsail halyards and clewed down; hauled out the reef tackles.
  Morning watch (04:36)  Laid out and passed the earings of the fore topsail.
* Morning watch (04:38)  Reefed the fore topsail; now set, 1 reef.
```

You say how many reefs, or *close* for all of them (a *close-reefed* topsail has every reef in). A reef comes out with `shake out`:

```orders frigate plain-sail
reef the topsails, one reef
reef the fore topsail, two reefs
# rejected: reef the fore topsail
reef the main topsail, close
take a reef in the spanker
reef the courses
shake out a reef in the mizzen topsail
# rejected: shake out the reef in the mizzen topsail
shake out two reefs in the fore topsail
shake out all reefs in the main topsail
# rejected: reef the fore royal
# rejected: close reef the topsails
```

The refusals: the fore topsail with three reefs in is "already close reefed (3 reefs in)"; the mizzen topsail with none in has "no reef in the mizzen topsail to shake out"; the royal "has no reef bands; it is set whole or not at all"; and *close* is a modifier after the sail, not a verb before it. A sail must be set to be reefed; reef a furled sail and the runner refuses it.

The schooner's boom mainsail reefs by settling the throat and peak halyards, hauling out the reef earing along the boom and tying the points (Luce 1866, ch. XXVII, 'Boom Mainsail'):

```orders schooner plain-sail
reef the mainsail, two reefs
reef the foresail
reef the topsail, close
shake out a reef in the mainsail
```

## Studding sails

Studding sails need the sail on their yard set (a fore topmast studding sail extends the fore topsail) and a steady breeze abaft the beam; they are the first thing to come in when it freshens (Luce 1866, ch. XXIII, 'The Topmast Studding-sail'; Lever, 'Studding Sails'). Set them on the weather side, the lee side, or both:

```orders frigate plain-sail
set the fore topmast studdingsails
set the studdingsails, lee
set the fore lower studdingsail, weather
# rejected: set the fore topmast studdingsail
take in the studdingsails
```

A studding sail comes in made up and stowed, so `take in` is enough; there is no `furl` for it.

## The schooner

Her sails are named in chapter 1; the verbs are the same. Her gaff sails are not furled on a yard but brailed up or lowered onto the boom, so `furl` is refused for them ("A gaff sail is not furled on its spar; take it in instead"), and her square topsail behaves exactly as the frigate's do (Luce 1884, ch. XXXIV Handling Fore-and-Afters).

```orders schooner
set the foresail
set the mainsail
set the jib
set the fore staysail
set the topsail
set the topgallant
set the gaff topsail
set the flying jib
take in the gaff topsail
take in the topgallant
furl the topgallant
haul down the flying jib
take in the mainsail
# rejected: furl the mainsail
```
