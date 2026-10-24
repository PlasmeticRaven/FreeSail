# Design note: the signals' data shape, and the voice between ships (package 71)

Written before anything of package 71 was built (the brief's rule: "the data shape of the
signals is this package's first design, written down before it is built, because 76 builds
the books out from it and every nation's book must fit it"). Spec M7 Part 7-i (§1 to §6),
rule 3 (recognition before fire) and rule 4 (rules first, models welcome) bind; the owner's
note of 2026-10-23 (any nation a combatant, the books built out progressively from one
foundation) is the reason the shape is one shape for every nation. The lead's readings in
the brief are taken where the code agreed with them and departed from in the places said
below, each with its reason.

## What the engine has, and what the voice between ships asks of it

Today a far ship is a `Vessel` with a `nation`, a `shows_colours` flag and a `spoken` flag;
the lookout makes her colours out at two miles (`ships.COLOURS_MADE_OUT_NM`) and names her
nation in the `strangers` reading when she shows them, and a sail within four cables is
"spoken" and a stranger no more. The rules captain's `_is_enemy` reads that nation against
the wars table, and 70's `fired_on` makes an enemy of anyone who fires on him. 70's
recognition is the least of it: the first shot at a sail not made out as an enemy is told
and the firer marked `outlaw` for the ports. Nothing is hoisted, nothing is read, nobody
answers a hail, a false flag is not a thing, and the private signal does not exist. Four
things in that shape do not fit the voice between ships:

1. **The colours are a flag, not a state.** `shows_colours` is true or false for ever; a
   ship cannot haul them down, hoist another nation's or strike them in a way the far body
   and the near body both read. The nation the lookout gives is the true one.
2. **Nothing flies.** A signal is a thing on a halyard for a while, seen by whoever is near
   enough with light enough, read by whoever has the book, answered or not; the lookout
   has no such thing to see.
3. **The hail is a line, not an exchange.** `sail.within_hail` says "She hails: 'What ship
   is that?'" and nobody can answer her, nor she the player.
4. **No ship obeys another.** The convoy's instructions and the squadron's signals command
   nobody until something says whose signals a ship obeys. The squadron as a set is 72's;
   this package needs the least relation under it.

## The design in one paragraph

**Colours are a state** of every body (`signals.Colours`: shown, none, false, struck,
distress, with the nation shown), kept on the far `Vessel` and on the crewed or player's
ship, mirrored between the two bodies with the rest of her truth, and the lookout gives the
nation *shown*, never the true one, so a ruse works on the captain reading it exactly as it
worked on his original. **The books are data in one shape for every nation**
(`data/signals/<root>/`: `book.yaml` the nation's declaration and the flags' figures;
`numerary.yaml` the day signals, each entry mapped to what the rules captain does when
commanded; `telegraphic.yaml` the dictionary for the free sentence; `night_fog.yaml` the
lights, false fires, rockets and guns and the fog's guns, bell and drum; `convoy.yaml` the
instructions to merchantmen; `private.yaml` the *form* of the private table, from which the
month's challenge and reply are drawn under the seed), the nation's entry in
`data/nations.yaml` naming its root and whether it is a well-built book or the basic system,
and `data/signals/basic/` the foundation every nation stands on until 76 builds hers.
**A signal is a thing hoisted** (`signals.Hoist`: the book, the numbers, the meaning, by
whom, since when, answered by whom), made by an evolution with hands at the halyards and a
minute a hoist (a telegraphic sentence as many hoists as it takes, in one evolution), kept
flying on the sender's body where every other lookout sees it as it sees her colours (the
flags' range by day, the lights' by night, the gun's by ear in fog), **read** a minute later
by whoever has that book ("she makes a signal we cannot read" without it), **answered** by
the answering pennant, and **acted on** by a rules captain who is `under the orders of` the
sender (a field on the vessel the scenario or the director sets: the least relation; 72
replaces it with the squadron's set) by the entry's `does`, logged otherwise. **The private
signal is a small table** per nation per month, drawn under the seed from the nation's
`private.yaml` form, carried as a paper of the ship's library by the King's ships alone,
challenged by a King's captain to every strange sail within the flags' range and read as
right, wrong or none, which is the tell that makes her a stranger and starts his chase.
**The hail is an exchange in three bodies**: the rules captain answers by a table of the
standard questions (`data/captains/hail.yaml`: what ship, whence, whither, cargo, news, and
the King's ship's demand to heave to), by his nation, his role and his colours (a privateer
under false colours lies by the same table under the flag she shows); a model at the other
captain's station hears the words in his sample and answers with his own `say to`; the
player types the hail and hears the answer on his deck. **The lights and the bell** are a
state by order and by the books, seen and heard by the lookout at the ranges a light and a
bell carry. **Recognition before fire is completed**: a captain fires on what his people
have made out by the colours shown, the private signal, the hail or her own shot, the first
shot under false or no colours is told and makes her a pirate to everyone who saw it and to
the ports, and 70's `action.unrecognised` becomes the exception it was meant to be.

## The pieces

### The data shape: `data/signals/<root>/`

One directory a root, the same six files in each, every file naming its sources at its
head and every entry that is the builder's own invention marked `made: true`. A nation's
entry in `data/nations.yaml` says which root it reads and what kind of book it has:

```yaml
  britain:
    signals: {root: britain, system: well-built}
  spain:
    signals: {root: basic, system: basic}
```

`system` is one of `well-built` (a book built from the nation's own sources, with a
dictionary for the free sentence) and `basic` (the foundation: a numerary of a few dozen
entries in the period's common form, no telegraphic dictionary, the private table drawn
from the common form, the night, fog and convoy signals of the common form). A nation whose
entry names no `signals:` reads `basic`. A root may be shared (the Spanish and the Dutch
both read `basic` until 76 gives each her own); the words of a signal are the book's, so a
basic book reads the same in any mouth, and the private table differs by nation because the
nation is in the draw.

**`book.yaml`: the declaration.**

```yaml
nation: britain                      # or "basic": the root's own name
system: well-built                   # or basic
sources: ["Howe 1790 ...", "..."]    # the books the entries come from, each named
flags:
  numerals: 10                       # the numeral flags 0 to 9
  substitute: true                   # one substitute (the 1799 book's)
  preparative: true                  # the preparative flag
  telegraph: true                    # Popham's telegraph flag (a well-built book)
  answering_pennant: true
hoist_s: 60                          # a hoist bent and run up (Popham: a minute or more)
read_s: 60                           # the minute to look it up at the other end
read_nm: 2.0                         # the flags made out by eye (the colours' range)
glass_factor: 1.5                    # the glass aloft reaches this much further
```

**`numerary.yaml`: the day signals.** A list of entries, each:

```yaml
- number: 16
  meaning: "Engage the enemy more closely"
  does: {order: "engage her more closely"}   # what a captain under the sender's orders does
  qualifiers: []                              # compass | number | ship | place, as the entry takes them
  source: "the Admiralty's Signal Book for the Ships of War, 1799, No. 16 (from memory)"
  made: false
```

`does` is one of `{order: <an order of the dialect>}` (performed through the receiving
captain's `give`, or through `far_order` on a far body, with the qualifiers filled in:
`steer {compass}`, `give chase`, `put her about`, `wear ship`, `make all sail`, `shorten
sail`, `come to an anchor`, `heave to`, `fill away`), `{intent: <words>}` (a new intent for
his machine: "run home to Brest"), `{state: <a state of the machine>}` (the receiver enters
it: `chasing` with the sender's chase as his stranger), `{news: true}` (no act: enemy in
sight, the land seen, a strange sail; logged and raised as an event the books and the
tripwires read), or `{answer: true}` (the entry is an answer to another: the affirmative,
the negative, "cannot comply"). `in_succession: true` on an entry makes the ships under the
sender's orders perform it one after another, each when the ship made the signal to before
her has done it (the leader first); it is how "tack in succession" and "wear in succession"
read with no station keeping (72's).

The words after `make the signal` are matched against the entries' `meaning` and their
`also` (other words for the same: "chase" for "general chase"), longest match first, the
qualifier words after it read as the entry's qualifiers take them ("enemy in sight bearing
NW": the compass; "No. 3 to chase": a ship by her pennants, which the player names by the
ship's words and the log writes as her pennants' number). A number given plainly (`make
the signal No. 16`) is the entry by number.

**`telegraphic.yaml`: the dictionary** (a well-built book only). `words: {number: word}`
for Popham's numbered vocabulary (the first version a few hundred words chosen for what a
squadron, a chase and a convoy say, the edition named; 76 fills the rest) and `alphabet:
{letter: number}` for the words the dictionary lacks, which are spelt letter by letter as
Pasco spelt "duty". `make the telegraphic signal: <sentence>` encodes the sentence as a
list of hoists (the telegraph flag first, then a hoist a word, a word not in the dictionary
a hoist a letter) and the evolution makes them one after another; the log says the hoists'
count and the minutes.

**`night_fog.yaml`: the night and fog books.** Two lists in the numerary's form with the
hoist replaced by the thing shown or fired: `night: [{meaning, show: "two lights, one over
the other, at the mizen peak, and a false fire", does, source, made}]` and `fog: [{meaning,
fire: "two guns", does, source, made}]`. By night a signal is made by the night book, in
fog by the fog book, chosen by the light and the visibility at the order: the player says
`make the signal to tack` and the book is the ship's choice, said in the line ("in the
fog: two guns, the signal to tack").

**`convoy.yaml`: the instructions to merchantmen.** The numerary's form again, a short book
of its own (make sail, shorten sail, tack, wear, close round the commodore, enemy in sight,
anchor, the convoy to disperse), because the merchantmen under convoy were given these and
not the fleet's book; a merchantman under a commodore's orders reads the convoy book and
no other. The commodore's ship reads both.

**`private.yaml`: the private table's form.** The actual tables were secret and are lost;
the game's are made under the seed in the period's form. The file gives the form and the
pools the draw uses:

```yaml
day:
  challenge: "{flag_a} over {flag_b} at the {place}"
  reply: "{flag_c} at the {place_2}, and the ensign {ensign}"
  flags: [...]            # the pool the numbers or colours are drawn from
  places: [main, fore, mizen peak, ...]
night:
  challenge: "{n} lights {arrangement} at the {place}"
  reply: "{m} lights ... and a false fire"
  ...
changes: monthly           # the table turns with the calendar month
source: "the form as the period's letters and orders quote it; the tables themselves made"
made: true
```

`signals.private_table(nation, year, month, seed)` fills the form from a random stream
seeded by the world's seed, the nation, the year and the month, so that two ships of one
nation in one world hold the same table and a replay has it again; a captured table (74's
prize carries the paper) is the same function's answer for the captor, good until the
month turns.

**The basic system (`data/signals/basic/`).** The same six files: a numerary of a few
dozen entries in the common form of the period's private and national books (the
general signals every navy had: the general chase, the recall, form the line, tack and
wear together and in succession, make more sail, shorten sail, anchor, the enemy in sight
with its bearing, the land seen, a strange sail, distress, the affirmative and the
negative), no telegraphic dictionary (a basic book refuses the telegraphic signal in words,
which is historically right: the free sentence was Popham's and Britain's), the night and
fog signals of the common form, the convoy's, and the private form. Every entry marked
`made: true`, with the note that its *meaning* is one every book of the period had and its
*number* is the builder's. The British book is built from Howe 1790 and the Admiralty's
1799 book with Popham's 1800 and 1803 dictionaries; the French from du Pavillon 1776 and
the numerary of the 1790s, smaller and marked where made.

### The colours: `freesail/world/signals.py` (`Colours`)

A dataclass with `state` (`shown`, `none`, `false`, `struck`, `distress`), `nation` (the
nation whose colours she shows: her own under `shown` and `distress`, the other under
`false`, `""` under `none` and `struck`), `since` (the tick) and `fired_under_false` (the
tick of the first shot under false or no colours, for the log and the stances). Kept as
`ship.extra["colours"]` on a near body (70 wrote the string `"struck"` there and nothing
read it; the string goes) and as `Vessel.colours` on the far body, the two mirrored with
the rest of her truth each tick while she is crewed (`crews.mirror`). The far
`shows_colours` flag becomes a reading of the state (true under `shown`, `false` and
`distress`); `Vessel.colours_words()` and `nation_adjective` read the nation *shown*, so
the lookout's lines, the `strangers` reading's `nation`, the glass and the stranger's
`known` words all carry the ruse. The truth (the director's `truth`, the viewer) carries
the true nation beside the shown.

The orders (object `signals`, `freesail/orders/signals.py`): `hoist the colours` (her
own), `hoist French colours` / `hoist false colours` / `show Danish colours` (another
nation's; `false colours` alone is the nation's principal enemy's), `haul down the
colours` (none), `hoist the ensign union down` (distress; `fire a gun to leeward` is 70's
and stays the gunnery's, the two together the signal of distress), and 70's `strike the
colours` kept in the gunnery with its state written here. The vocabulary's `hoist our
colours` refusal goes. A privateer's doctrine says whether she sails under false colours
(`false_colours: true`), whose (the principal enemy's), and at what range she shows her
own (`true_colours_cables`); the rules captain of any role hoists his true colours before
his first shot (the law allowed the ruse until then and no further), the player is not
made to.

**Recognition (rule 3), completed.** `combat.action._recognition` reads the firer's own
colours first: a shot under `false` or `none` colours is told once ("Fired into the brig
under false colours: a pirate's act; every ship that saw it and every port that hears of it
will hold us so"), the firer marked `outlaw` for the ports (70's), and every captain whose
lookout had her in sight at the shot adds her to his `pirates` (a set beside `fired_on`:
the witnesses; the word reaches the ports with the complaint and nobody else, which is as
far as news travelled). Then the mark: an enemy by the colours shown and the wars, by the
private signal answered wrong or not at all (`recognised[id] == "enemy"`), by her own shot
(`fired_on`), or by a hail that named her (`recognised[id]` from the words); a sail not made
out by any of these is 70's `action.unrecognised`, now the exception. `_is_enemy` on both
bodies reads `recognised` and `pirates` before the colours.

### A signal hoisted: `signals.Hoist`, the evolution and the lookout

`Hoist`: `book` (`numerary`, `telegraphic`, `night`, `fog`, `convoy`, `private`,
`answer`), `numbers` (the hoists' numbers, or the thing shown or fired), `meaning`,
`qualifiers` (a dict), `by` (the ship's id), `since` (the tick it broke out), `down` (the
tick it was hauled down, None while it flies), `answered_by` (ids), `to` (a ship's id when
the signal is addressed to one by her pennants, else None). The hoists flying are kept on
the body as `Vessel.flying` (a list) and mirrored from the crewed ship's
`ship.extra["signals"].flying`; the player's shadow carries his. A numerary hoist flies
until it is answered by every ship it commands and hauled down (`haul down the signal`), or
for `SIGNAL_FLIES_S` (a glass) at most; a telegraphic sentence's hoists each fly for the
hoist's minute and are replaced by the next.

**The evolution** (`data/evolutions/make_signal.yaml`, scripted: `MakeSignalScript` in
`evolutions/action_scripts.py`): hands 3 of the afterguard (the yeoman of the signals and
two at the halyards; the signal officer is an officer), `hoist_s` from the book for each
hoist, daylight wanted for the flags (by night and in fog the night and fog books are
used by the same order and the evolution takes the lantern's or the gun's time instead); at
quarters it draws on the trimmers as any sail work does. Each hoist breaks out at its
step's end (`signal.made`, notable: "No. 16 at the main: engage the enemy more closely"; a
telegraphic word a routine line a hoist and one notable line for the sentence). The answer
(`answer the signal`) is the same evolution with the answering pennant; the private signal
and its reply the same with the table's hoist.

**The lookout** reads the flags of every sail in sight once a minute in `look()`, at the
range the book's `read_nm` and the glass give by day (`glass_factor` for the sail the glass
is on), the lights' range (`LIGHT_SEEN_NM`) by night, and by ear in fog (a gun at
`GUN_HEARD_NM`, a bell at `BELL_HEARD_NM`): a hoist newly flying is "she makes a signal"
(`signal.seen`, with the flags' count and place, notable), and `read_s` later, if the
ship's library holds that book (her nation's root is the sender's, or a captured book), the
meaning (`signal.read`: "The brig's signal is No. 16, engage the enemy more closely"); a
hoist of a book she lacks stays "a signal we cannot read". The private signal's challenge is
read by its form ("she makes the private signal"); the reply is judged against the table
by the challenger alone. The receiving rules captain answers every signal he reads
(`answer the signal`), and acts on it when the sender commands him.

### The least relation: `under the orders of`

`Vessel.under_orders_of: str` (a ship's id, or `the ship` for the player's), set by the
scenario's `ships:` entry (`under_the_orders_of: the ship`), by the director (`ship "Nancy":
under the orders of the Sherbourne`) and by nothing else here; the player's own ship obeys
nobody's signals (a model or the player reads them and chooses). A rules captain who reads
a signal from the ship he is under the orders of performs its `does`; one who reads any
other ship's logs it. The convoy's keeping company is the `company` leg the far body has
(the pilot's boat's), given by the goal "in company with the ship"; 72 replaces both with
the squadron's set, the formations and station keeping. Nothing here keeps a formation.

### The private signal

`signals.private_table(nation, year, month, seed)` as above; `papers: private_signals` in
the scenario (or by the role: a King's ship, a cruiser and a commodore carry their nation's
table; a merchant, a packet, a fisherman and a privateer do not) puts "the private
signals" in the ship's library (`data/papers/papers.yaml`: keeper the captain, place the
cabin, the page this month's challenge and reply by day and by night, and the month it
turns). The orders: `show the private signal` (the challenge), `answer the private signal`
(the reply, refused in words with no table: "there is no private signal aboard to answer
with"). The rules captain of a King's ship challenges every strange sail within the flags'
range by day and the lights' by night, once a stranger, and waits `PRIVATE_ANSWER_WAIT_S`
(five minutes) for her reply: right makes her a friend (and a sail spoken, for the
stimuli); wrong, or none, is the tell. A stranger under his own nation's colours who fails
it is an enemy under false colours (`recognised: enemy`, the chase by doctrine); one under a
neutral's colours who fails it is a stranger still, to be closed and hailed; one under an
enemy's colours was an enemy already. A privateer's doctrine may bluff (`bluff_private_signal:
true`: a wrong reply drawn under the seed, which some did); a merchant shows nothing.

### The hail: the three bodies

Within hail (`ships.HAIL_NM`, four cables) the orders `hail her`, `hail the brig`, `hail
the Nancy: what ship is that?` and `say to the brig: heave to, I am sending a boat` speak
another ship from the quarterdeck by the trumpet (`signals.hail`): the words are a line of
the speaker's log (`hail.made`), heard on the other ship's deck (`hail.heard`, urgent, so
a station there wakes), and answered by her body:

- **the rules captain** by `data/captains/hail.yaml`: the standard questions recognised in
  the words (what ship, whence, whither, what cargo, what news, heave to, who is your
  captain, how many days out), each answered from his truth in the period's form ("The
  Nancy of Guernsey, from Guernsey for Falmouth, in ballast"; "His Majesty's cutter
  Sherbourne"; "No news but the Brest fleet is in"), by his role (a King's ship names
  herself and demands the other's name and port; a merchant answers all; a privateer under
  false colours answers from a table of lies under the flag she shows: a name of that
  nation drawn under the seed, a port of that nation, a cargo), and his stance (an enemy's
  King's ship is answered with the colours hoisted and nothing else; a demand to heave to
  from a King's ship of a nation she is not at war with is obeyed by a merchant and refused
  by a privateer, who makes sail); the answer is a line heard on the hailer's deck
  (`hail.answered`);
- **a model** at the other captain's station hears the words in his sample (`hear`, as the
  deck's conversation reaches a station) and answers with his own `say to the <hailer>:
  <words>`, which is the same order from his side; nothing answers for him by table while
  his seat is live;
- **the player** types the hail and hears the answer as a line; a rules captain's hail of
  him (`She hails: 'What ship is that?'`, 43's line) is answered by `say to her: ...` and
  read by the table's nation words ("His Majesty's", "of Falmouth", a French name), which
  recognises him to that captain.

Between two rules captains the standard exchange (name, port, destination, news) is written
to both logs once when they come within hail, in each one's words for the other, and both
read the stances (`spoken`, as the lookout keeps it; the nation by the words, which a liar
gives false). **The hail as the first order of a search**: a King's ship's captain within
hail of a strange merchantman says "heave to, I am sending a boat"; the merchant rules
captain heaves to (his book's `heave to`) or, an enemy's, makes sail; the boat and the
search are the director's scene and 63's boat, not built here. The director's `say as the
captain of the Nancy: ...` speaks for any unheld captain within hail; 67's seat at a
person makes a model that captain's voice.

### The lights and the bell

`ship.extra["lights"]` and `Vessel.lights`: `none`, `stern lantern`, `top lights`, or the
fishing boat's `a lantern at her nets` (56's, kept), set by `hoist the lights` / `hoist a
stern lantern` / `hoist the top lights` / `show no lights` and by the books (a King's ship
in company a stern lantern at night by the Regulations' custom of ships in company; alone,
none; a merchantman none; the convoy's merchantmen a stern lantern each by the convoy
instructions). The lookout at night sees a light at `LIGHT_SEEN_NM` (three miles on a
clear night, within the visibility; judgement after the period's lights) as a sighting of
its own ("a light, two points on the bow"), the hull's loom at the mile as now. In fog the
ship at anchor rings her bell every two minutes (`fog_signals`: a state the books set with
`keep the fog signals`, one line when it begins and one when it ends, never a line a ring),
under way she fires a gun at the interval the book gives (the Regulations' and the custom's
figures from memory and marked so); the lookout hears a bell within `BELL_HEARD_NM` (a mile)
and a gun within `GUN_HEARD_NM` (three miles) in fog as sightings by ear ("a bell, bearing
SW"; "a gun to the south-west"), and a signal made in fog is a gun and not a flag.

### The nations' habits to data

70's `NATION_HABITS` move into each nation's entry of `data/nations.yaml` as `habits:
{range_factor, aim, roll, source}`, read by `Captain._habit` through `world.nations`; the
code's table goes (its `netherlands` key never matched the table's `batavian-republic`,
found on the way). The same entry's `signals:` names the root and the system, so a nation is
built out in one place: her colours, her habits, her book.

### The captain's helm in action (item 8)

70's `_engaging` steered by the mark's bearing alone. The law becomes
`captains.helm_in_action(...)`: the course that keeps the mark on the engaged beam at the
doctrine's range, **never within the ship's close-hauled angle and half a point of the
wind's eye** (the course clamped to the close-hauled course on her present tack, as
`navigation._chase_course` clamps a chase); the **gage** the doctrine names kept (under
`weather` the course chosen so that the mark lies to leeward of her, under `lee` to
windward, where the geometry allows, and the beam law otherwise); when the mark **passes
through the eye** (the beam law would want a course on the other tack) the doctrine's
`through_the_eye` says what he does: `shift` the engaged battery and stay on this tack (the
default: his guns go on), `tack` or `wear` by his book (a handy cutter tacks, a frigate
wears). The chase of a weaker mark (70's `give chase` renewed) already clamps to the wind
in `_chase_course`; it is unchanged and the two laws share the clamp. The offing's tack
among islands (57's station-gale trial) is read against this and taken or left with its
reason in the tuning notes.

### The stations, the director and the readings

Readings: `the colours` (shown and whose, false, none, struck, distress), `the signals` (the
hoists flying and seen this glass with their meanings where the book is ours, and who
answered), `the private signal` (this month's challenge and reply, the last exchange), `the
lights`. Events for `at` and the stand-by: `she hoists her colours`, `she hoists false
colours`, `her colours come down` (70's), `a signal made`, `a signal seen`, `a signal read`,
`the private signal made`, `the private signal answered`, `the private signal wrong`,
`hailed`, `a hail answered`, `a light seen`, `a gun heard`. The director's forms grow by
their examples under the existing `ship "<name>": order ...` (`order hoist false colours`,
`order make the signal to chase`, `order hail the Sherbourne: ...`) and one new form,
`ship "<name>": under the orders of <ship>`; his truth shows every ship's true colours
beside the shown and her flying signals; a brief's `limits: {false_colours: false}` refuses
his ships the ruse. The harness's sample carries a hail heard and a signal read as lines
a model answers with the orders above.

## What was rejected, and why

- **One book file a nation** (`data/signals/<nation>.yaml`, the spec's first words).
  Rejected: the five books were five printed books with five custodies (the private
  signals under seal and sunk weighted on capture, the convoy instructions given to
  masters who never saw the fleet's book), and 76 fills them at different rates; a
  directory of six small files lets a nation's numerary grow without touching her
  private form, and lets a root be shared by the nations that have no book of their own
  yet.
- **Signals by number at the order line** (`make the signal 16`). Kept as a form but not
  the form: the orders are by meaning (the spec's and the lead's), the number written in
  the log beside the meaning, because the player and a model know what they mean and not
  Howe's numbers, and because the number differs by nation while the meaning does not.
- **A hoist as an instantaneous state change.** Rejected by rule 4's spirit and the spec's
  words ("a thing hoisted ... with the hands at the halyards and a minute a hoist"): the
  minute is where a chase's signal arrives too late and a telegraphic sentence costs a
  quarter of an hour, which is the period's texture; the evolution also takes the hands
  from the trimmers at quarters, as everything does.
- **The receiving captain acting on every signal he reads.** Rejected: a King's ship's
  captain does not tack because a passing frigate's commodore signalled his own division
  to; the `under the orders of` relation is the least that says whose signals command,
  and 72's squadron set replaces it.
- **The whole squadron's work** (station keeping, the formations, the order of sailing,
  the repeating frigate). Not built, by the brief: 72's. The convoy of four tacks in
  succession on one hoist by `in_succession` and nothing more.
- **The true nation in the `strangers` reading with a `false` flag beside it.** Rejected:
  it would let a captain's rule read the truth through the ruse; the reading gives the
  colours shown, and the truth is the director's.
- **Every far ship ringing a bell in every fog as a log line.** Rejected for the log and
  the pace: the fog signals are a state begun and ended, heard by the lookout within the
  mile; nothing per tick for every far ship.
- **The private table as a stored table in the save.** Rejected: it is a pure function of
  the seed, the nation and the month, so a replay has it and a save carries nothing new.
- **The telegraphic dictionary whole** (Popham's three thousand words). Left to 76 by the
  brief; the first version holds a few hundred chosen for the squadron, the chase and the
  convoy, and the alphabet spells the rest, as the period did for a word the book lacked.

## What hangs from this (the later items)

Item 1 reads `Colours` and the recognition; item 2 the private form and the paper; item 3
the six files of the three roots; item 4 the `Hoist`, the evolution and the lookout's
reading, with the least relation; item 5 the hail's tables; item 6 the lights and the fog
signals; item 7 the habits' move; item 8 the helm's law; item 9 the readings, the events,
the director's examples and the harness's lines; item 10 the truths from 7-143, the two
scenarios and the records. 76 builds the books out from the six files and never before
them; 72 replaces `under_orders_of` with the squadron's set and keeps the entries' `does`;
74 gives a prize's papers (a captured table, a captured book) to the captor's library by
the paper's handle.

## As built (the end of the package)

The shape held: the six files a root, the three roots, the `Locker` one object for a ship's
two bodies, the hoist an evolution read a minute after it is seen, the private table a pure
function of the seed, the hail's three bodies by table, `under_orders_of` the least
relation. It grew in two places the convoy showed. **A vessel under orders with no brain**
(a merchantman given only her company to keep, with no intent and so no `FarCaptain`) reads
and obeys by the least captain (`signalling._Reader`, ticked once a minute from
`Vessels.tick`), because the brief's convoy wants no model and no intent in four
merchantmen beyond keeping company; and **the goal `in company with the ship`** was added
to the far body's goals (the pilot's boat's `company` leg of 37h), since no intent of the
captain's machine keeps company and the squadron's set is 72's. Two things were taken
another way with their reasons in the tuning notes: a trader's silence to the private
signal is no tell (a merchantman never had the table; only a man of war's rig under his
own colours, or a reply and the wrong one, makes an enemy), and the fog signals are kept
by a rules captain only while another sail has been in sight within the hour, so that no
single ship's recorded passage in thick weather moves. The hoist's breaking-out minute is
the script's to set when the hands have the first hoist up (`NOT_YET` until then; the
phase's end at the hands' pace, not the order's minute nor the book's), which the encounter
taught when a hoist queued behind a wear was read before it was up, and the convoy when a
short watch's two-minute hoist was read at the book's one. The chase learned two things
from the encounter that were not in the design: the captain names his stranger's rig to
the chase order (the order's own choice is the lookout's nearest stranger, who counts a
sail under our colours none), and a chase on the other side of the wind's eye is gone about
for. Every figure is in `docs/dev/TuningNotes.md` (package 71).
