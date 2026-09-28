# Design study: the ship's papers and books

From the owner's notes of 2026-09-28, on the library tool and what a local model can carry.
A design note, not a specification; milestones 5 to 8 should answer it.

## Two layers, kept distinct

**The reference library is a promise, not a possession.** Every model's brief says the
documentation is reachable, and the consent brief names it among the terms. The primer,
the catalogue of evolutions and the grammar of the order language are out-of-world
reference: always there, never something the world can take away, capture, soak or
burn. That is a welfare commitment (`docs/agents/README.md`) as much as a convenience,
and it does not change.

**The ship's papers are things in the world.** Books and documents aboard a vessel are
objects with in-world contents, varying by the ship, her service and her captain's purse
and history; they can be issued, bought, lost, captured, sunk, forged, read by a boarding
officer or handed over with the ship. They are in-world data, like the log, and a model
reads them through the same tool and the same shelf as the reference, with the same
handles and shelving (spec M4 open item 9's shelf), so that a watcher reading a captured
French signal book does it the way it reads the primer.

## What the period gives, ready made

- **Issued to every King's ship:** the Regulations and Instructions (the 1808 printing is
  in `docs/references/admiralty/`); the signal book and the private signals, the most
  guarded papers aboard; the ship's log and the muster book, kept by the ship herself.
- **A navigator's:** an Epitome (Norie 1805, Hamilton Moore), the Nautical Almanac, and
  the charts the Admiralty or his own purse supplied. A good set of charts of a coast was
  worth buying in port or taking from an enemy master.
- **A captain's own:** his commission; his sailing orders, and secret orders under seal to
  be opened at a stated place; Falconer's Universal Dictionary of the Marine (1780) and
  Steel's Rigging and Seamanship (1794) on the shelf of a captain of means; letters,
  dispatches, a letter of marque for a privateer, a passport, a parole given or held.
- **A little sloop's:** the signal book, a battered Almanac, a chart or two, and not much
  else.

Period matters for the in-world layer: Luce (1866, 1884) and Kipping (1847) are the
game's sources but are decades too late to be aboard in 1805; Steel, Falconer, the
Regulations, Norie and Hamilton Moore are not.

## Where it bites

- **The striking-colours study** (`Scenario-StrikingColours.md`): the dispatch channel of
  gap 4 is a document arriving; the first act of a captain about to strike was to sink
  the signal book and the secret orders in a weighted bag; what a prize crew finds, or
  does not, is papers. Papers are what the director hands people.
- **Career material** (milestone 8 and after): a captain's library grows with his
  fortunes; charts of a station are bought or captured; a commission, a court-martial
  finding and a parole are documents that follow a person.
- **The model's context.** A ship's papers are read by handle and shelved like the
  reference, so a local model's context is never filled by a chart it glanced at; the
  journal is where a reader keeps what it took from the page.
