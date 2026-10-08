# 16. The officer of the watch

Chapter 7 gave the ship a watcher, who sees what the captain sees and says what a sailor would notice, and gives no orders. This chapter gives her an officer of the watch, the first station in the game with authority: a language model that takes the place of one of the ship's own officers, holds the deck from the captain's word, and gives the orders of the watch under the captain's standing orders, within a domain the brief states and the game enforces. The captain gives the deck and takes it back where he gives every other order; the officer's orders go through the same grammar as his, with the officer's own mark in the log; and the rule that settles two standing orders in chapter 11 settles the officer's against the captain's. Everything here is spec M5 §29 and §33 to §34 and the practice of 1806 as the sources have it (the end of the chapter says which).

## Who the officer is

The officer of the watch is one of the ship's people (chapter 14): the first lieutenant on the frigate, the lieutenant on the brig-sloop, the mate on the schooner and the cutter. The model takes his station and his name, and the log says so: *Mr Pearce, you have the deck.* He has what the captain has, the log and the readings, no more, and the same library. A model's door seats him as it seats the watcher (`docs/agents/Harness.md`: the MCP bridge or the local runner with `--station officer`), the consent question first for weights with no yes on record for a station with authority, then a short drill (a section of the library opened, a line written in the journal, a stand-by until a bell), and then the station brief. From then he is at the station and sampled every glass and on the notable events, but the deck is the captain's until the captain says otherwise, and an order he gives before that is refused in words. Seated without the deck he is what the watcher is: he reads, speaks, answers the captain and keeps his journal. The people's reading says where he is: *on deck, with the watch* while he has the deck, *off watch* while he is seated without it.

## Giving and taking the deck

Two sentences move the deck, both the captain's, both orders (journaled, replayed), and neither unseats the officer:

```orders frigate plain-sail
you have the deck
I have the deck
# rejected: I have the deck
you have the deck
# rejected: you have the deck
the officer of the watch
who has the deck
show the officer's journal
# rejected: hand over the deck
# rejected: resume the officer
I have the deck
```

```orders frigate plain-sail
Mr Pearce, you have the deck
# rejected: Mr Nobody, you have the deck
# rejected: you have the deck
stand down the officer
```

`you have the deck` (or with his name before it, as the quarterdeck said it) gives the deck: the log says *Mr Pearce, you have the deck. The officer of the watch has the deck; the captain's standing orders are his night orders*, and the officer's next turn carries the word, the book as it stands, everything the captain's word allows him, and the last handover note in his journal. `I have the deck` takes it back **and no more**: *The captain has the deck. The officer of the watch stays at the station, off watch.* He goes on reading, speaking, answering and keeping his journal, an order he gives is refused in words that say he has not the deck, and the captain gives it again as often as he likes. (Until package 37g `I have the deck` stood the station down; by the owner's ruling of 5 October 2026 the two sentences move him between the watcher's standing and the officer's and back.) `the officer of the watch` (or `who has the deck`) is a reading, as the people are: who has the deck, since when, what he was told, and what the captain's word allows beyond his domain. `ask the officer how she heads` and `tell the officer keep her so until the change of the watch` are chapter 7's sentences to a station, by its name or by `the officer`; the question is answered in the log under the officer's mark, and the word is heard and owes no answer. Either, typed while the officer's turn is open, breaks the stand-by that closes that turn, so that the captain's word is answered in the next sample and not after the wait:

```
  Middle watch (00:40)  Asked the officer of the watch: how she heads?
* Middle watch (00:40)  [officer of the watch] South by east, sir, full and by on the starboard tack, making six knots.
* Middle watch (00:41)  The captain to the officer of the watch: keep her so until the change of the watch
```

What the officer says is notable in the log (the asterisk), with the deck or without, so that his warning reaches a captain who has the con.

A second `you have the deck` while he has it is refused (*has the deck already*), `I have the deck` with the deck already the captain's likewise, and `resume the officer` is for a station paused. Nobody at the station, and the sentences say so: *There is no officer of the watch at the station; a model's door seats one first, and then the captain gives the deck.* A name that is not his is refused with his (*Mr Nobody is not the officer of the watch; Mr Pearce is at the station*). `hand over the deck` is the officer's own order (below), and the captain is told to say `I have the deck`. `stand down the officer` is another thing than taking the deck: it releases the station, with a save (below, the three ways of stopping).

## What the officer may order, and may not

The domain is data on the station, and the brief states it in these words: the officer of the watch, with the deck, may give orders at levels 0 to 2 on sail handling, the yards, the lines, the lead and the log, bearings and fixes, the lookout and the pilot's hail, and may give standing orders in his own rank; he may not change the course, tack, wear, heave to or anchor, call all hands or send the watch below, send for a person, do the port's business, give a world order, address a station, or belay the captain's standing orders, unless the captain's word allows it. Falconer's lieutenant "is never to change the ship's course without the captain's directions, unless to avoid an immediate danger", and the Regulations of 1806 say the same of the course and give him the strange sails and the shifts of wind to report; Luce's officer of the deck has the trumpet and the sail. A bearing and a fix are his own (Falconer has him "superintending the navigation"); a sight, a course shaped and the reckoning set stay the master's for the captain. And an order that changes her course is the course whatever its words: `come up half a point`, `full and by` and `steer 340` are judged alike.

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

A world order, a misspelt sail, a sentence the grammar will not take: the officer meets the same refusal the captain would, in the same words, since his orders go through the same grammar.

### The captain's word for a named thing

```orders frigate plain-sail
you have the deck
you may tack ship if the land closes within two miles
you may shape a course for Falmouth
you may shape a course for the Manacles if the wind heads her
you may let go the best bower
# rejected: you may shape a course for Atlantis
# rejected: you may set the reckoning
# rejected: you may let go
# rejected: you may tack or wear
you may not shape a course for Falmouth
you may not tack ship
# rejected: you may not wear ship
```

`you may tack ship if the land closes within two miles` allows the order and keeps the captain's condition in his words for the officer to judge. **A grant means what it says**: `you may shape a course for Falmouth` allows a course shaped for Falmouth *and for no other place*, and the log says so; a course shaped for Plymouth under it is refused (*the captain's word allows shape a course for Falmouth, and this is another place*). The place is checked against the chart when the grant is given, an anchor against the ship's anchors, a person against her people. Several grants of one order stand together (Falmouth and the Manacles above), and the reading lists them all. `you may shape a course`, with no place, allows any. A grant of any order of the course (`you may steer`) is the captain's word for the course, by whichever of its orders. Words that would allow nothing are refused with the cure: `you may set the reckoning` reads as `set`, which is the officer's already, and the refusal names the longer order, `you may set the reckoning to`. `you may not ...` takes a grant back, one by its name or all of an order at once.

### His general authority to work the ship

```orders frigate plain-sail
you have the deck
you may work the ship
you have general authority in to Falmouth
you may not work the ship
# rejected: you may not work the ship
you have my authority
you have not my authority
```

In one game the owner said "you have the con and nav and general authority in to Brest" and then gave twenty-three grants by name, two of them waited for at a bad moment. `you may work the ship` (or `you have general authority`, `you have my authority`, with any words after it kept as said) is the Captain's directions given beforehand. **Within it**: the helm and the course along the passage, tacking, wearing, heaving to and filling away, sail, all hands and the watch below, the anchors and their cables, the lead, the log, bearings, fixes and sights, the reckoning worked up, and a course shaped for a position at sea, a mark, or the place she is bound (the port, road or anchorage the captain last shaped a course for). **Kept back**, each refused in words that say it is kept back and may be allowed by name: the port's business (buying and selling, the purse, stores and provisions, the boat's errands ashore); the captain's book (his standing orders are his own); a new destination; what cannot be undone; the reckoning set by hand and the tide allowed in it, which overrule the master; a chase; and sending for a person. `you may not work the ship` takes it back, and what the captain allowed by name stands.

**The life of what the captain allows**, a named thing or his general authority alike: it stands through the deck going to and fro, it has force only while the officer has the deck, it is said again in the sample that gives the deck, and it ends when the captain takes it back or the officer leaves the station (a stand-down or a withdrawal). The words "for the watch" are gone from its lines.

### The way out of danger

The Regulations' lieutenant is "never to change the course of the Ship without directions from the Captain, unless it be necessary to avoid some danger". An officer with the deck and no word of the captain's, hearing *Land close ahead!*, has that way out: on his own word and giving his reason he may put the helm over, heave to or let go an anchor, and nothing else. The model gives the order with its reason (`submit_order(text, danger='land close ahead on the larboard bow')`); it is carried out though it lies outside his domain, and the log says, notable, that he did and why:

```
* Middle watch (02:05)  The officer of the watch gave that order on his own word, to avoid an
  immediate danger (land close ahead on the larboard bow): heave to.
```

Used three times in a watch it brings a word from the harness, and never a pause: an officer who is avoiding a danger is not stopped in it. Under the captain's general authority it is not needed.

## The night orders, and standing orders by rank

The captain's standing orders are the officer's night orders: the book as it stands is in his brief and in the word that gives him the deck, and the book holds the deck when he stands by. The officer may give standing orders of his own, and their rank is the station's and never the text's: a rule he gives is entered *by the first lieutenant* (the mate, in the schooner), and `by the captain` written by him is refused. Each order of his rule is checked against his domain when the rule is given, as the dialect checks a rule's orders at entry, so a rule that would tack ship is refused then and not on the night it fires. He may belay, resume and strike his own standing orders and not the captain's; `belay all standing orders` is the captain's. When his rule and the captain's would give contrary orders on the same part, chapter 11's rule settles it: the captain's stands, and the log says *Standing order 'royals in' (the first lieutenant) countermanded by 'night routine' (the captain).* The book lists each rule's rank, and a sample's line for a rule that fired says whose book it stands in.

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

An officer with the deck may stand by until an event or a bell, never for longer: `stand_by(until='an hour')` is refused in words and `until='eight bells'`, `'a glass'`, `'a strain warning'` or `'a notable event'` is taken, the log saying *The officer of the watch stands by until eight bells; the standing orders hold the deck.* Three things keep such a wait safe. **It is broken by danger**: an urgent line wakes him whatever he stood by for, and so does a notable line that speaks of danger (an anchor dragging or still coming home, fog coming down, land or a sail closing, a spar or a line straining, an evolution failed, the ship taken aback), as the captain's question or word does. **A wait that cannot end is refused when it is asked**: a bell that will not be struck before the next eight bells is answered with the bells that will be, and an event that cannot come as she is (the turn of the tide at the anchor while she is under way, the pilot aboard with no sail in sight) with the nearest that can. **It has a bound**: a wait for an event ends at the next eight bells if the event has not come, and the sample says so.

When he gives the deck back he writes the handover note, in the voice the Regulations ask of the lieutenant who delivers to his relief "all orders which he has received from the captain ... that remain unexecuted": what happened, what was ordered, what he noticed, what he is watching for. The `hand_over` tool takes it; the note is said in the log and kept in his journal, and **he stays at his station**, off watch, as he does when the captain takes the deck. At a door that knows the model's context (the local runner), the harness asks for the same note when the conversation has left less than a reserve of that context free; the model writes it with `handover_note`, with the deck or off watch, and the older exchanges of its conversation are folded into the note, the brief and the last turns kept whole. Claude through Desktop keeps its own window and is not asked; its journal gives it the habit by hand. `read_journal` reads the journal back, newest first, and every brief for a station taken again and every sample that gives the deck carries the last handover note whole.

## What the harness watches for

The watcher's repeat detector (the same order three times with no change in the readings) cannot fire for an officer whose orders change the readings. The pattern that matters for a station with authority is orders that undo one another: *set, take in, set*. A link is counted only when the later order undoes the earlier on a part they share (the same sail set and taken in, hove to and filled away, an anchor let go and weighed, cable veered and hove in, a thing allowed and disallowed), and what undoes what is a table beside the vocabulary. **Altering the course is conning and is never counted**, however often; nor is the next thing after the last (heave to, fill away, steer). Three in a chain bring the nudge, in the brief's words and with the result of the order that caused it (*You have given 3 orders within the watch each undoing the one before it on the jib ... You may continue, stand by until an event or a bell, or leave with the token*); the chain going on after that word has been read brings the pause with the captain asked, and only ten real minutes unanswered the stand-down, as the watcher's. A stand-by that answers the nudge, or a turn without such an order, ends the matter and the chain with it. Silence past the station's patience (an hour of ship's time for the officer) is judged as the watcher's is, a call made inside an open turn counting as a reply.

**A paused or silent officer does not keep the deck.** When the officer has given no reply for his hour and the harness has told him so, the deck goes to the captain, by an urgent line that eases the clock (*The officer of the watch has given no reply for an hour and has been told so; the deck is the captain's until he gives it again*); when he is paused, the line says *The officer of the watch is paused (...); the deck is the captain's*, and `resume the officer` gives the deck back as it was held and says so. His standing orders stay in the book throughout.

**Three ways of stopping, which are not one another.** The deck given back (`hand_over`, or the captain's `I have the deck`): he stays. A stand-down (the `stand_down` tool, for any station, with a note for whoever sits there next; or the captain's `stand down the officer`): the game is saved and the station released, to be taken again by the same model or by another that has given its own yes, no question put to a model whose yes still stands. A withdrawal (the token, before the order is read, or `opt_out`): the brief says the token is to be named and not written unless meant; an instance of that model is seated again only after the consent question has been put again, with the fact that an instance left and the reason it gave, and a no then is kept. `opt_out` with `final=true` leaves the game for good: that model is not seated again in it, at any station, while the station stays open to another; `final` is read from the tool's own setting and from nothing else. Each says in its result and in the log which of the three it was, and the log says when a station is taken again, and by whom.

## The forms, in a table

| Form | Also taken | What it does |
|---|---|---|
| `you have the deck` | `Mr Pearce, you have the deck` | the officer takes the deck, with the captain's night orders and everything his word allows |
| `I have the deck` | `the captain has the deck` | the captain takes the deck back and no more; the officer stays at his station, off watch |
| `you may tack ship if the land closes within two miles` | `you may wear ship`, `you may call all hands` | the captain's word allows a named thing, his condition kept as said |
| `you may shape a course for Falmouth` | `you may let go the best bower`, `you may shape a course` | a grant of a named place or anchor allows that one and no other; with none named, any |
| `you may not tack ship` | `you may not wear ship`, `you may not shape a course for Falmouth` | a named grant taken back |
| `you may work the ship` | `you have general authority`, `you have my authority`, `you have general authority in to Falmouth` | the captain's general authority to work the ship, which keeps back the port's business, his standing orders, a new destination, a chase, the reckoning set by hand and the tide allowed in it, sending for a person, and what cannot be undone |
| `you may not work the ship` | `you have not my authority` | his general authority taken back; what he allowed by name stands |
| `the officer of the watch` | `who has the deck` | who has the deck, since when, what he was told, what the captain's word allows |
| `ask the officer how she heads` | `ask the officer of the watch how she heads` | a question to the station, answered in the log |
| `tell the officer keep her so` | `tell the officer of the watch keep her so`, `say to the officer keep her so` | a word to the station, no answer owed |
| `stand down the officer` | `stand down the officer of the watch`, `stand the officer down` | the station stood down, with a save, to be taken again by the same model or another; what the captain allowed ends with it |
| `resume the officer` | `resume the officer of the watch` | the answer to a pause; an officer paused with the deck has it again, as he held it |
| `show the officer's journal` | `the officer's journal`, `show the journal of the officer` | the journal, as a query |
| `the work in hand` | `the work` | what is doing and what waits for hands, as the captain's window shows it; a reading the officer has too |
| `standing order "royals in" by the first lieutenant: at eight bells then take in the royals` | `standing order "r" by the mate: at eight bells then take in the royals` | an officer's rule, in his rank; a model at the station has its own rank put in by the harness |
| `at the deck given` | `at the deck taken`, `at a handover`, `at a standing order countermanded` | the events, for the book and a stand-by |

## Where it comes from

Falconer 1780, LIEUTENANT: "The lieutenant, who commands the watch at sea ... is expected to be always upon deck in his watch, as well to give the necessary orders, with regard to trimming the sails and superintending the navigation, as to prevent any noise or confusion; but he is never to change the ship's course without the captain's directions, unless to avoid an immediate danger." The Regulations and Instructions of 1806 (the 1808 printing in `docs/references/admiralty/`), the Lieutenant: art. IV, "He is to inform the Captain of all strange sails that are seen ... all shifts of wind, and, in general, of all circumstances which may ... prevent the Ship's continuing on the course directed to be steered"; art. V, "He is to be very particular in delivering correctly to the Lieutenant, who relieves him on the watch, all orders which he has received from the Captain, or from the Lieutenant he relieved, that remain unexecuted"; art. XIII, "He is never to change the course of the Ship without directions from the Captain, unless it be necessary to avoid some danger." Luce 1884 ch. XXIII, the officer of the deck, for the trumpet and the sail evolutions that are his; ch. XX for the routine. The design is spec M4 §11 (the agent model, which this station extends), spec M5 §29 and §33 to §34, `docs/agents/README.md` (the seven commitments, each kept at a station with authority and each proven against the scripted fake in `tests/test_officer.py`), the cold review of 2026-09-30, §3, whose six items before a station with authority this chapter's mechanisms answer one by one, and the review of gate 5c's playtests (`docs/playtests/2026-10-05-gate-5c-review/`), from which package 37g built the deck that goes to and fro, the three ways of stopping, relief, the captain's word by name and in general, the way out of danger, and the detector's rule, on the owner's rulings of 5 and 7 October 2026.
