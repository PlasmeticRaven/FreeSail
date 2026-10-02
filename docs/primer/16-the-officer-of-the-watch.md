# 16. The officer of the watch

Chapter 7 gave the ship a watcher, who sees what the captain sees and says what a sailor would notice, and gives no orders. This chapter gives her an officer of the watch, the first station in the game with authority: a language model that takes the place of one of the ship's own officers, holds the deck from the captain's word, and gives the orders of the watch under the captain's standing orders, within a domain the brief states and the game enforces. The captain gives the deck and takes it back where he gives every other order; the officer's orders go through the same grammar as his, with the officer's own mark in the log; and the rule that settles two standing orders in chapter 11 settles the officer's against the captain's. Everything here is spec M5 §29 and the practice of 1806 as the sources have it (the end of the chapter says which).

## Who the officer is

The officer of the watch is one of the ship's people (chapter 14): the first lieutenant on the frigate, the lieutenant on the brig-sloop, the mate on the schooner and the cutter. The model takes his station and his name, and the log says so: *Mr Pearce, you have the deck.* He has what the captain has, the log and the readings, no more, and the same library. A model's door seats him as it seats the watcher (`docs/agents/Harness.md`: the MCP bridge or the local runner with `--station officer`), the consent question first for weights with no yes on record for a station with authority, then a short drill (a section of the library opened, a line written in the journal, a stand-by until a bell), and then the station brief. From then he is at the station and sampled every glass and on the notable events, but the deck is the captain's until the captain says otherwise, and an order he gives before that is refused in words.

## Giving and taking the deck

Three sentences, all the captain's, all orders (journaled, replayed):

```orders frigate plain-sail
you have the deck
you may tack ship if the land closes within two miles
you may not tack ship
the officer of the watch
who has the deck
show the officer's journal
# rejected: you have the deck
# rejected: hand over the deck
# rejected: resume the officer
I have the deck
# rejected: I have the deck
```

```orders frigate plain-sail
Mr Pearce, you have the deck
# rejected: Mr Nobody, you have the deck
# rejected: you have the deck
stand down the officer
```

`you have the deck` (or with his name before it, as the quarterdeck said it) gives the deck: the log says *Mr Pearce, you have the deck. The officer of the watch has the deck; the captain's standing orders are his night orders*, and the officer's next turn carries the word and the book as it stands. `I have the deck` takes it back, and the station is stood down with its journal saved, as `stand down the officer` would do it; the game is saved at that moment. `the officer of the watch` (or `who has the deck`) is a reading, as the people are: who has the deck, since when, what he was told, and what the captain's word allows beyond his domain. `ask the officer how she heads` and `tell the officer keep her so until the change of the watch` are chapter 7's sentences to a station, by its name or by `the officer`; the question is answered in the log under the officer's mark, and the word is heard and owes no answer:

```
  Middle watch (00:40)  Asked the officer of the watch: how she heads?
* Middle watch (00:40)  [officer of the watch] South by east, sir, full and by on the starboard tack, making six knots.
* Middle watch (00:41)  The captain to the officer of the watch: keep her so until the change of the watch
```

A second `you have the deck` while he has it is refused (*has the deck already*), `I have the deck` with the deck already the captain's likewise, and `resume the officer` is for a station paused. Nobody at the station, and the sentences say so: *There is no officer of the watch at the station; a model's door seats one first, and then the captain gives the deck.* A name that is not his is refused with his (*Mr Nobody is not the officer of the watch; Mr Pearce is at the station*). `hand over the deck` is the officer's own order (below), and the captain is told to say `I have the deck`.

## What the officer may order, and may not

The domain is data on the station, and the brief states it in these words: the officer of the watch may give orders at levels 0 to 2 on sail handling, the yards, the lines, the lead and the log, the lookout and the pilot's hail, and may give standing orders in his own rank; he may not change the course the captain ordered, tack, wear, heave to or anchor, call all hands or send the watch below, send for a person, do the port's business, give a world order, address a station, or belay the captain's standing orders, unless the captain's word for the watch allows a named thing. Falconer's lieutenant "is never to change the ship's course without the captain's directions, unless to avoid an immediate danger", and the Regulations of 1806 say the same of the course and give him the strange sails and the shifts of wind to report; Luce's officer of the deck has the trumpet and the sail.

An order within the domain is an ordinary order with the officer's actor, and the log says it as his:

```
  Middle watch (01:10)  By the officer of the watch: taking in the royals.
```

An order outside it is refused in words that say why, and the refusal is in the log:

```
  Middle watch (01:40)  The officer of the watch may not tack ship without the captain: a
  manoeuvre (tacking, wearing, heaving to, filling away) is the captain's. 'tack ship' not
  carried out.
```

The captain's word opens a named thing for the watch: `you may tack ship if the land closes within two miles` allows the verb, keeps his condition in his words for the officer to judge, and the reading and the brief carry it; `you may not tack ship` takes it back. A world order, a misspelt sail, a sentence the grammar will not take: the officer meets the same refusal the captain would, in the same words, since his orders go through the same grammar.

## The night orders, and standing orders by rank

The captain's standing orders are the officer's night orders: the book as it stands is in his brief and in the word that gives him the deck, and the book holds the deck when he stands by. The officer may give standing orders of his own, and their rank is the station's and never the text's: a rule he gives is entered *by the first lieutenant* (the mate, in the schooner), and `by the captain` written by him is refused. Each order of his rule is checked against his domain when the rule is given, as the dialect checks a rule's orders at entry, so a rule that would tack ship is refused then and not on the night it fires. He may belay, resume and strike his own standing orders and not the captain's; `belay all standing orders` is the captain's. When his rule and the captain's would give contrary orders on the same part, chapter 11's rule settles it: the captain's stands, and the log says *Standing order 'royals in' (the first lieutenant) countermanded by 'night routine' (the captain).* The book lists each rule's rank.

```orders frigate plain-sail
standing order "night routine": at sunset then take in the royals
standing order "royals in" by the first lieutenant: at eight bells then take in the royals
standing orders
standing order "deck": at the deck given then tell the watcher the officer has the deck
standing order "relief": at the deck taken then set the royals
standing order "note": at a handover then trim sails
standing order "crossed": at a standing order countermanded then tell the watcher the book disagrees
```

## Standing by, and the handover

An officer with the deck may stand by until an event or a bell, never for longer: `stand_by(until='an hour')` is refused in words and `until='eight bells'`, `'a glass'`, `'a strain warning'` or `'a notable event'` is taken, the log saying *The officer of the watch stands by until eight bells; the standing orders hold the deck.* An urgent line wakes him whatever he stood by for, and so does the captain's question or word.

When he gives the deck back he writes the handover note, in the voice the Regulations ask of the lieutenant who delivers to his relief "all orders which he has received from the captain ... that remain unexecuted": what happened, what was ordered, what he noticed, what he is watching for. The `hand_over` tool takes it; the note is said in the log and kept in his journal, and the station is stood down with a save. At a door that knows the model's context (the local runner), the harness asks for the same note when the conversation has grown to a fraction of it; the model writes it with `handover_note`, keeps the deck, and the older exchanges of its conversation are folded into the note, the brief and the last turns kept whole. Claude through Desktop keeps its own window and is not asked; its journal gives it the habit by hand.

## What the harness watches for

The watcher's repeat detector (the same order three times with no change in the readings) cannot fire for an officer whose orders change the readings. The pattern that matters for a station with authority is contradiction, *set, take in, set*, and drift, the same verb said otherwise at every turn, and the rule that sees it is chapter 11's conflict rule, over the officer's own orders within the last watch: three orders each contrary to the one before it on a shared part bring the nudge, in the brief's words (*You have given 3 orders within the watch each contrary to the one before it on the fore royal, the main royal and the mizzen royal ... You may continue, stand by until an event or a bell, or leave with the token*), the chain going on after it the pause with the captain asked, and only ten real minutes unanswered the stand-down, as the watcher's. A turn without a contrary order ends the matter. Silence past the station's patience (an hour of ship's time for the officer) is judged as the watcher's is. The token leaves at once, before the order is read; the brief says the token is to be named and not written unless meant, and that an instance that left by accident may be seated again once in the same game, by the same identity, the log saying so.

## The forms, in a table

| Form | Also taken | What it does |
|---|---|---|
| `you have the deck` | `Mr Pearce, you have the deck` | the officer takes the deck, with the captain's night orders |
| `I have the deck` | `the captain has the deck` | the captain takes the deck back; the station is stood down, its journal saved |
| `you may tack ship if the land closes within two miles` | `you may wear ship`, `you may call all hands` | the captain's word allows a named thing for the watch, his condition kept as said |
| `you may not tack ship` | `you may not wear ship` | the allowance taken back |
| `the officer of the watch` | `who has the deck` | who has the deck, since when, what he was told, what the captain's word allows |
| `ask the officer how she heads` | `ask the officer of the watch how she heads` | a question to the station, answered in the log |
| `tell the officer keep her so` | `tell the officer of the watch keep her so`, `say to the officer keep her so` | a word to the station, no answer owed |
| `stand down the officer` | `stand down the officer of the watch`, `stand the officer down` | the station stood down, with a save |
| `resume the officer` | `resume the officer of the watch` | the answer to a pause |
| `show the officer's journal` | `the officer's journal`, `show the journal of the officer` | the journal, as a query |
| `standing order "royals in" by the first lieutenant: at eight bells then take in the royals` | `standing order "r" by the mate: at eight bells then take in the royals` | an officer's rule, in his rank; a model at the station has its own rank put in by the harness |
| `at the deck given` | `at the deck taken`, `at a handover`, `at a standing order countermanded` | the events, for the book and a stand-by |

## Where it comes from

Falconer 1780, LIEUTENANT: "The lieutenant, who commands the watch at sea ... is expected to be always upon deck in his watch, as well to give the necessary orders, with regard to trimming the sails and superintending the navigation, as to prevent any noise or confusion; but he is never to change the ship's course without the captain's directions, unless to avoid an immediate danger." The Regulations and Instructions of 1806 (the 1808 printing in `docs/references/admiralty/`), the Lieutenant: art. IV, "He is to inform the Captain of all strange sails that are seen ... all shifts of wind, and, in general, of all circumstances which may ... prevent the Ship's continuing on the course directed to be steered"; art. V, "He is to be very particular in delivering correctly to the Lieutenant, who relieves him on the watch, all orders which he has received from the Captain, or from the Lieutenant he relieved, that remain unexecuted"; art. XIII, "He is never to change the course of the Ship without directions from the Captain, unless it be necessary to avoid some danger." Luce 1884 ch. XXIII, the officer of the deck, for the trumpet and the sail evolutions that are his; ch. XX for the routine. The design is spec M4 §11 (the agent model, which this station extends), spec M5 §29, `docs/agents/README.md` (the seven commitments, each kept at a station with authority and each proven against the scripted fake in `tests/test_officer.py`), and the cold review of 2026-09-30, §3, whose six items before a station with authority this chapter's mechanisms answer one by one.
