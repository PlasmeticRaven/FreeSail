# Design note: the sail by her name (package 95)

Written before anything of package 95 is built, as its brief asks (`docs/dev/M7-WorkPackages.md`,
"Package 95: the sail by her name", and the section it draws on, "The owner's testing week: loose
ends mended by the lead", item 5 and the week's turn's note 5; the case study
`docs/playtests/2026-11-05-small-convoy-all-models/case-study.md`, lessons 1 and 3, and the brig
off Falmouth's case study, lesson 2). Short, as asked: the resolver's grammar, the order of its
narrowing, the name, the identification kept and lost, which orders and readings take it, and what
moves and what does not. Nothing here is built yet; the postscripts will say what was built and
what was taken another way.

## 1. What the trunk does now (read and probed, 2026-11-06)

A probe on the trunk at `1ab17aa`: the frigate off the Lizard, two French and British brig-sloops
of war (the *Raven* bearing NE and the *Swift* SSW, each eight cables) and a merchant brig a mile
off SE by E, all lying to, made out to their colours.

- **Four resolvers, not one.** `Lookout.find` (the glass, `make her out`, `give chase`, `take a
  bearing of`, the reading `the bearing of`) knows the generic words (`_SAIL_WORDS`), eight rig
  words (`_RIG_WORDS`, a substring of the made-out words, the nearest of them) and a feature's
  name or id taken whole; `hail._addressee` knows the pronouns and the chase, a vessel's own name
  (on the whole sea, in sight or not), her kind exact and then a substring of her kind or `what`
  among the sails in sight; `orders/boat._pull_for` knows the other hulls' names and
  `Vessels.find` (an id or a name, anywhere); `send the boat to the <ship>` goes through
  `world.orders.hull_named` by name.
- **Every clause the lookout himself speaks is refused.** `make out the brig on the larboard
  quarter` is refused ("Nothing in sight answers to 'on the larboard quarter'"): the verb's
  synonym `make out the brig` eats the kind and the rest is taken as a name; `make out the sail on
  the starboard bow bearing NE distant a mile` likewise. `the glass on the merchant brig` is
  refused though a merchant brig is in sight (her rig made out, not yet her purpose, and
  `merchant brig` is no rig word). `hail the brig on the larboard quarter` hails the nearest brig.
- **A name works by accident.** `the glass on the Raven` finds her by her feature's `modern`,
  which is her id, which the scenarios happen to write as her name; a sail whose id is not her
  name is not found by it, and nothing says whether the deck may know it.
- **Two of a kind read alike.** `the strangers` gives the *Raven* and the *Swift* as "a
  brig-sloop of war ..." twice, the colours the only difference; a sail hailed and answered ("the
  French national sloop Raven") is still "a brig-sloop of war" in every row.

## 2. The resolver (`world/lookout.py`, one function, `Lookout.sail_named`)

One function takes the words an order or a reading names a sail by and returns the sighting, or
refuses in words that list the strangers. The grammar is the lookout's own line read backwards
(`Sail ho! A brig on the larboard quarter, bearing NE by N, distant a mile`; `the strangers`'
`words`), commas or none (the grammar hands words on without them), each part optional and in any
order:

```
[the|a] [<name> | <kind words> | sail | stranger | chase | ship | vessel]
        [on the <side> bow | on the <side> quarter | abeam [to <side>] | right ahead | right astern
         | on the bow | on the quarter | ahead | astern]
        [bearing <point>]            (a point by `units.parse_compass_point`: NE by N, ENE, N 3/4 E)
        [distant <distance>]         ('a mile', 'four cables', 'two leagues'; also '<d> off')
```

The narrowing, in order, each step over the pool the last left:

1. **The pool**: the sails in sight (`seen_as == "sail"`), for the hail the sails in sight and the
   one that has hailed this deck and lies within hail (82b's `_has_hailed_us`, kept).
2. **A name over all.** If the words hold a name the deck knows for a sail in sight (her name by
   identification, §3; or her own name, as the player and the captains name their consorts and
   the scenario's ships, which the trunk already answers by id), she is the one, and the rest of
   the words are not checked against her (the sail moved since the lookout's words; the name is
   the surer). A name of a vessel not in sight keeps each order's road beyond sight as it is (the
   hail's whole sea, `pull for`'s `Vessels.find`, `send the boat`'s hull), so nothing that works
   today is refused.
3. **The kind.** The words left when the article, the name and the clauses are taken off: none
   or a generic word (`sail`, `stranger`, `chase`, `vessel`) narrows nothing; else every word of
   them must be among the words made out of her so far (her feature's name, `_sail_known`, her
   kind), with the period's spellings mapped (`merchantman` to `merchant`, `brig sloop` to
   `brig-sloop`, `ship of war`, `man of war` to `of war`, `sixty-four`, `razee`, `lugger`,
   `privateer`). 'The cutter' with no cutter made out keeps 71's reading (the nearest sail), and a
   rig word with nothing of that rig made out is refused as now.
4. **The quarter** (the relative bearing words): a sail answers when her relative bearing now is
   within the said sector widened by a point each side (`relative_words`' sectors: ahead under one
   point, the bow to six, abeam to ten, the quarter to fifteen, astern beyond), so that a sail on
   the edge of the bow when the lookout spoke and abeam by the order still answers.
5. **The bearing**: within a point and a half of the said point (the lookout's bearing is to the
   nearest point; a point of swing either way in the minute between his words and the order).
6. **The distance**: within a half and twice the said estimate, judged against the lookout's own
   estimate (`judged_m`), not the truth (he answers by what he judged).
7. **The closer** where more than one remains: the least true distance, as every resolver does
   today (the pins hold to it).

A clause that leaves no sail refuses in words: "No sail in sight answers to 'the brig on the
larboard quarter': the strangers are a brig-sloop of war on the starboard bow, bearing NE, distant
eight cables; ..." (the strangers' words, as the trunk's refusal promises and does not give). A
clause the resolver cannot read (`to windward`, `the second sail`) is no part of the grammar and
refuses as a name does today; the windward and leeward sides are a road for later and said so in
the tuning notes.

## 3. The identification, kept while in sight and lost when lost

The lookout keeps, beside `_sail_said` and `_sail_known`, `_sail_ident: {fid: {"name", "how"}}`,
a plain default so that a checkpoint from before loads with it. A sail is identified when the
deck learns her name:

- **her name by hail**: a hail answered (by the table, `deliver`, or by her captain's model, the
  answer's words) whose words carry a name: her own, or a lie's from the hail table's `lies`
  (a privateer under false colours is identified by the name she gives; the lie is the deck's
  knowledge, not the truth's);
- **the private signal answered right** (`signalling` judged `right` on the player's deck, or the
  lookout's `signal.answered` line for the private book): a friend of the deck's nation is known
  by her pendant and the list, her own name;
- **her colours made out on a consort**: a sail of the deck's own squadron or the scenario's
  company (`under_orders_of` either way, the set's members) whose colours are made out is known
  by her own name, as a commodore knows his ships by their pendants.

Her colours alone, on a stranger, give her nation and not her name: she stays "a brig-sloop of
war ... French colours". The identification is cleared where `_sail_said` is cleared now, when
the look no longer has her (`_sails`' lost-sight branch: "a sail lost in the night is a stranger at
dawn"), and the next identification needs her closed and made out again.

## 4. Which orders and readings take it

- **Orders**: `make her out` (the verb's own kind word joined to the rest, so `make out the brig on
  the larboard quarter` is the brig and the quarter), `the glass on`, `hail the` / `say to the`
  (`hail._addressee`: the pronouns and the chase first as now, then the resolver over its pool,
  then the name on the sea, then the mark-in-sight refusal), `the bearing of` and `take a bearing
  of` (through `Lookout.find`, which hands sail words to the resolver and keeps its land, light,
  cask and chart-name roads as they are), `give chase` (by the same `find`), and `pull for`
  (other hulls by name first, then the resolver on the boat's own lookout where she keeps one, then
  `Vessels.find` as now; the refusal names the forms).
- **Readings**: `the strangers` gives each item `name` (None until identified) and leads her words
  with it ("the Raven, a brig-sloop of war on the starboard bow, bearing NE, distant eight cables:
  ..."); `what is in sight` and `a sail in sight` name her the same way in their sail lines. The
  item's `id` is left as it is (the API's handle, read by the viewer's chart and gunnery).
- **Not taken here, for the lead's ruling**: `send the boat to the <ship>` (lesson 1's "send the
  boat to the razee"; `orders/port.py` `_boat_to_ship` and `world.orders.hull_named`, neither on
  this package's list) would take the resolver in a touch of a few lines, the words resolved to
  the sail's name before `hull_named`; and lesson 3's refusal at sea ("She is not in port; there is
  no shore within a boat's pull", `world/dealings.py`) would name the form `send the boat to the
  <ship> with <persons>` when a sail is in sight within a boat's pull. The brig off Falmouth's
  lesson 2 (the lookout's `hail` read before `hail the pilot`) is the grammar's
  (`data/vocabulary.yaml`, `orders/grammar.py`), not this resolver's; I take it if the lead
  rules it mine.

## 5. What moves and what does not

- **The lines a pinned passage writes are not changed.** The event texts (`lookout.made_out`, the
  hail's "Hailed the brig by the trumpet", `lookout.sail_lost`) keep the lookout's words as now:
  the name enters the readings' rows only, and only for an identified sail. `sail_name` and
  `_words_for` (the hail's words for a sail) are left alone.
- **Every naming that resolves today resolves the same.** The resolver's narrowing is a superset:
  the words of the pinned passages and scenario books (`the brig`, `the cutter`, `the sail`, `her`,
  a name, an id) reach steps 2 and 3 alone and their closer-sail rule is the trunk's. A new key in
  a reading's rows (`name`) is added only if the pinned digests that read the rows are unmoved; if
  one moves, the key is added only to an identified sail's item and the tuning notes say why.
- **No draw moves.** The resolver reads; it draws nothing and changes nothing but the
  identification's record, which no tick reads.
- **The truths**: 7-395, the narrowing's four cases (the kind; the kind and the quarter; the
  quarter and the bearing; the bearing and the distance), each picking a sail the nearest-of-kind
  rule would not, across `make her out`, `the glass on`, `hail the`, `the bearing of` and `pull
  for`; 7-396, two sails answering the words alike, the closer taken, and a clause that leaves
  none refused with the strangers listed; 7-397, a name over all (the farther sail named by her
  name against a nearer of the same kind and quarter); 7-398, a sail hailed and answered named in
  `the strangers`, `what is in sight` and `a sail in sight`, two brig-sloops told apart, and the
  name forgotten when she is lost sight of and back to "a brig-sloop of war" when she is closed and
  made out again; 7-399, the recorded passages unmoved: the pinned truths and trials that name
  sails (the glass's 7b-105 to 7b-107, the chase, the hail's 71 truths, the captain trials, gate
  5B and the convoy's) run as before on the resolver, states and counts asserted, never a digest.

## 6. The steps

1. The resolver in `world/lookout.py` and its use by the glass, `make her out`, the hail, the
   bearing and `pull for`; truths 7-395 to 7-397 and 7-399; the primer's chapter 15 (other sail)
   and 23 (colours and signals) on naming a sail.
2. The identification recorded, the readings' rows naming her, and its loss with the sail; truth
   7-398; the primer's chapters and `docs/agents/Harness.md` where the strangers' row is told.
