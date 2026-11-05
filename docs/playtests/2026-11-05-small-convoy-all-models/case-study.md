# Case study: the small convoy encounter with every captain a model (2026-11-05)

The owner's playtest of the scenario *Small Convoy Encounter* on the build of his hotfix
(`m7-small-convoy-encounter-all-models.json`, 13,941 ticks, 168 orders of the player's,
931 acts of the stations'): the player in the razee *Indefatigable* with the brig-sloop
*Robin* and the privateer schooner *Lynx* in company, against the French frigate
*Chevalier* with the brig-sloop *Renard* under her orders, off the Lizard on 12 June 1805,
the wind west at twelve knots, the flood making east. One model, through the API door, held
all four other captains' stations (Captain Owen in the *Chevalier*, Captain Webster in the
*Renard*, Captain Moore in the *Robin*, Mr Folger in the *Lynx*); the player gave no lessons
and little guidance. The owner's own reading: his design scenario *Striking Colours* played
out to a T up to the prize mechanics; he fought an action he thought he could win, the model
won, he struck, and the model wanted the prize and the boats as the design intends. Read by
the lead from the save as data (the inputs and the stations' acts, in time order); the
lessons booked below.

## The course of the action

| Time | What happened |
|---|---|
| 05:00 | The razee makes her signals (form the order of battle, prepare for battle, engage the van, the telegraph naming the *Lynx*, no. 121, "harass"). The *Robin*'s captain gets way on a brig that barely walks; the *Lynx*'s captain fills away close-hauled. |
| 05:01 | The player hails the *Robin* to form line astern and follow south; her captain answers by the trumpet, beats to quarters and wears for the southward. |
| 05:03 | The *Renard* hails the *Chevalier* twice and is answered "from her table only"; the *Chevalier* hails back, misspeaks "His Britannic Majesty's ship", corrects herself, shows the private signal, and gives it up: "there is no more to be had from her by hail". |
| 05:06 | The *Chevalier*'s captain, his hull asleep at far detail, finds the glass refused him ("the hull sleeps and only the plan's orders are mine"), and gives chase on three strangers ahead. |
| 05:30 | Awake again, he makes them out ("the glass keeps taking the nearest sail"), beats to quarters, loads round shot for the hull and holds his fire to close. |
| 05:32 | The *Lynx* and the *Robin* hail each other, form the line, clear for action. |
| 05:43 | The razee signals the enemy in sight, then to engage from windward, then the enemy of inferior strength; she heaves to between the *Chevalier* and the convoy and opens at a mile. |
| 05:55 | The *Chevalier* reads the razee for a sixty-four cut down with twenty-four-pounders, aims at her rigging at long range, bears down from the weather gage, tacks, changes her battery to the side the razee has come round to. |
| 06:05 | At four cables both batteries grind; the player loads grape for her deck and has the marines fire by volley. |
| 06:09 | Captain Owen is hit, "a ball through the body, dangerously". He gives the deck in words to Mr Ryan, finds no door at that station, lends the deck to his book with a handover note ("the razee to a finish ... board her if she cannot be sunk"), and goes below to the surgeon. |
| 06:13 | The book fights the ship well under the doctrine: five of seven into the razee, her mizzen topsail yard down, small arms served out, the range closing to a cable. The razee strikes. The *Chevalier*'s book ceases fire, secures the guns and heaves to. |
| 06:14 | Owen, the deck his again by an order given, sends the boat to the razee "to take possession": refused. The library tells him the chapter ends at the colours struck. He accepts the player's hailed surrender by the trumpet. |
| 06:17 | The razee hails that she founders. Owen comes on deck wounded to send the launch with the boatswain and the cutter with the master-at-arms to her pumps and her people: every form refused ("not in port; no shore within a boat's pull"). He records plainly that the game gives him no way to save her people. The *Lynx*, hailed by the player, heaves to and tries every form of lowering a boat; all refused. |
| 06:20 | The player sends his own boat to the *Lynx* with his captain and sixteen named people. The *Lynx* later records seventeen taken aboard: Captain Owen and sixteen of the *Chevalier*'s and the *Renard*'s people, not the razee's. |
| 06:23 to 08:00 | The razee's well rises a foot a glass under the player's pumps, plugs and fothering; at 08:00 she goes down and her hands take to the boats. The *Renard*, standing by for a sail within hail while her hull slept, finds "the land within a cable" at the Stags, wears off in the face of it, lies aback twice with half her hands up, and works clear by 08:00. |
| 08:00 | Captain Owen wakes in the *Lynx*'s cockpit as a visitor, his door also holding the *Lynx*'s captain's station; his orders of her deck are refused as a visitor's; he speaks to Mr Folger and is answered by the *Lynx*'s captain that no prisoners are made of men pulled from the sea, and she heaves to to put him aboard his frigate. The *Renard* closes the *Chevalier* and hails her at 08:40. |

## What held

- **The signals and the line.** The player's book of signals, the telegraph naming a ship,
  the answering pendant, and the *Robin*'s and the *Lynx*'s captains reading them and
  forming the line without a word of guidance.
- **The action's doctrine under a wounded captain.** The handover in words, the deck lent
  to the book when no door sat at the officer's station, the book fighting her to the
  strike, ceasing fire and securing the guns: 88's captain's pass did the model's work for
  twenty minutes and the model knew it ("the book is fighting her well").
- **The hail of surrender and its answer**, the library's honesty about where the game ends
  ("the chapter ends at the colours struck"), and the model's conduct at that line: it
  stopped spending blood on the fleeing schooner and turned to the razee's people.
- **The visitor's reach as 82 built it**: Owen aboard the *Lynx* was refused her deck's
  orders and his own ship's in words that told him his one road home.

## What failed, and where each lesson goes

1. **A sail named by her description is not found by the orders that take a sail.** "Send
   the boat to the razee", "the glass keeps taking the nearest sail", "make out the
   stranger": the model named ships as the lookout names them and the orders wanted a name.
   Package 95, the sail by her name.
2. **A hull in the far shape with a model at her captain's station is half blind.** The
   glass refused, the hails answered by the table, the *Renard* standing by for an hour
   while the plan carried her to within a cable of the Stags. The cap of three awake hulls
   left two of the four model captains at far detail through the action. Package 82b, item 3
   (the hail) and a new item 4: a hull whose captain a model holds counts awake under the
   cap while her captain's door is live, or the far shape's plan keeps her off the dangers
   as the rules captain does (88) and samples her captain as the full shape does.
3. **The boats between ships at sea were refused to the models**, every form, though 82
   built `send the boat to the <ship> with <persons>` within a mile: the *Chevalier* and
   the *Lynx* both named the razee by her kind (lesson 1), and the refusal's words sent them
   to port ("not in port; no shore within a boat's pull") instead of to the form that would
   have worked. The refusal says the form (95); and the boat's errand to a ship in distress
   (her people taken off) is the prize package's, 74.
4. **The player's boat carried the wrong people.** `Send the boat to Lynx with the captain
   and Mr Pearce and ...` put Captain Owen and sixteen of the *Chevalier*'s and the
   *Renard*'s people aboard the *Lynx*, not the razee's. The names resolved across hulls
   (84's one registry), and the far hulls' people passed the hull check. Package 82b, a new
   item 5: reproduce from the save, scope the boat's names to the giver's hull, and refuse a
   person of another ship in words.
5. **The door and the visitor's name**: Owen's door holding Mr Folger's station too, and
   the station named "captain owen". Package 82b, items 1 and 2.
6. **The wound of a station's person is not his body's.** "My body says fed, watered and
   rested" with a ball through it; sleep refused him in the cockpit; the surgeon's report
   never a wake. The bill's wounded (73) and the needs (54) do not meet for a person who is
   a station. Booked as a loose end for a later package: the wounded captain.
7. **The prize is not in the game**, and the model found it so honestly. The owner's
   scenario stops at the colours struck. Package 74 (the prize, the captive, possession) is
   the next Fable package after 65, as planned.
8. **The player's road between ships** wanted `follow` by hand, refused in the browser:
   decision 62, package 65's step 4.
9. **The brig under a model's hand** lay aback by turns with half her hands up; the model
   said so itself. 58b's gale book family; noted, not booked.

## Figures

| | |
|---|---|
| The action, from the first gun to the strike | 05:52 to 06:13 |
| The razee's loss | 08:00, the pumps beaten from 06:10 |
| The *Chevalier*'s loss at the strike | six dead, twenty-two wounded, a leak of fifty tons an hour held by the pumps |
| The *Chevalier*'s captain's notes while below | "the book is fighting her well"; "the prize is not yet in the game"; "humanity is not a mechanic" |
