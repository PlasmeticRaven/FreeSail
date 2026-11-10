# Design note: prizes, the strike and what follows, and the far fight (package 74)

Written before anything of package 74 is built, as the brief asks (`docs/dev/M7-WorkPackages.md`,
"Package 74", its refresh after 84, 85 and 82, and the paragraph "From package 97"): the prize
as a hull of the one world, the captive's channel as the visitor's voice, the far fight on the
sleeping hulls with 75's finding mended first, the court martial and a new command, the prize
court and the money on 86's ordnance and service, the consent revision drafted and not applied,
who leads on when the boarders' officer falls, every edge case decided, what was rejected, and
the order of the steps, each a mergeable state. The ground is spec M7 §11a, §18 to §20 and §29,
the owner's note on the court martial and the continuation (`docs/design/Scenario-StrikingColours.md`,
"The director as the world's voice"), the striking-colours study whole, `Design-OneWorld.md`
(84) and `Design-BoatAndPersonAboard.md` (82) with their postscripts, `Design-PlaceKnowledge.md`
(65, closed: the captive's places are its rule applied), `combat/far.py` (70, measured and not
wired), `combat/boarding.py` (73, and 97's pin of the default draw), `world/ordnance.py` and
`world/service.py` (86's fold of the owner's work), 71's captured private table, 53b's things and
transactions, 66's line and 67's seat at a person, 72's set and its prize hook. Decision 64 binds
every nation-specific table here (Spain in each). Nothing in this note is built yet; its
postscripts, step by step, will say what was built, what was taken another way and what was found.

Every figure below is judgement unless a source is named beside it, and the sources on file
(`docs/references/README.md`) are read where they speak: the Regulations of 1806 (1808 printing)
Sect. XII ch. III (prizes and prisoners: the papers sent to the Court of Admiralty, a privateer
without a commission a pirate, prisoners victualled at two thirds, their lists to the Agent for
Prisoners, the parole), ch. IV (head money: the sentence of condemnation under the court's seal,
the certificate of the men aboard at the beginning of the engagement, the agent's letter of
attorney, paid though she be sunk or burnt), Sect. XIII ch. I art. VI (lieutenants of marines
share in prizes with the warrant officers), and the Flag Officers' art. XXXI (the Commander in
Chief's; a prize purchased for the service: three fourths of the appraised value paid to the
captors' agents, a fourth reserved);
Falconer 1780, ENGAGEMENT ("the defeated ship having acknowledged the victory by striking her
colours is immediately taken possession of by the conqueror, who secures her officers and crew as
prisoners in his own ship, and invests his principal officer with the command of the prize until a
captain is appointed by the commander in chief") and CARTEL ("a ship commissioned in time of war
to exchange the prisoners of any two hostile powers ... no cargo, ammunition or implements of
war, except a single gun for the purpose of firing signals"); James, for the head-money
certificates and the actions' aftermaths. What no page on file gives (the shares of the eighths,
the head money's five pounds, a hull's price a ton, the court's weeks) is FROM MEMORY and marked
so, kept in data for the owner to move.

## 1. The ground, in one paragraph

A ship struck lies to for her captor (`combat/action.strike`: `ship.extra["struck"]`, her colours
the state "struck" the lookout reads, her battery held, her captain's machine in `struck`, her
far record's `Vessel.struck`); at far detail a merchantman that yields is cut out at hailing
distance and joins her captor's company (`squadrons.far_captures`, `Squadron.join(as_prize=True)`,
72's hook); the boarders' deck won strikes her by their hand and puts the boarders' officer on her
deck by `movement.put_aboard` with his station following (82), and finds nobody to lead on when
he falls (97's pin). Every ship is a `Vessel` of the sea with a nation, a role, a fit, a plan and
a far record of her damage (`Vessel.damage`, summed from her parts when she sleeps, 84's step
5), and some are hulls of the one World (`hulls.Hull`): awake under the cap with her physics, her
muster (`ship.extra["crew"]`, a `Crew` of `Sailor`s), her people (the named few in the world's one
registry with a home and a whereabouts), her stations, her papers, her purse and her dealings;
asleep with her state whole, moved by her far body's plan, her coarse acts the port's jobs. A
person changes hulls by one function (`put_aboard`: his whereabouts, his place, his harness or
the player's seat following as a visitor's voice or stood down by the handover's rule); the
player at the prompt reads by his person's place (65) and his prompt follows his body (decision
62); a visitor speaks by `say to`, reads `where am I` and `the ship`, and gives none of the host's
deck's orders. The far fight is measured and not wired (`combat/far.py`: the same tables at
three-minute rounds, two cutters at two cables, truth 7-139), and the far brain never takes the
engaging transition (`brains.FarCaptain._enemy_within` returns None). The ports are the world's,
each with its market, its yard, its crew pool, its places ashore and, since 86, an `ordnance:`
block (who issues or sells powder and shot) and `service.service_of` saying whose service a ship
is in. The director acts through the world-order channel's forms (`director.WORLD_ORDER_FORMS`),
each doubted or refused in words, performed on the world, never shown as sent; a seat at a model
is read from the consent record (`seats.hold`), and the consent brief names no adversarial role.

## 2. The prize is a hull of the one world (item 1)

### 2.1 Possession, one function

`prizes.possess(world, captor, prize, *, by)` is the one road by which a struck ship becomes a
prize, whatever brought her colours down (the strike by morale, the player's own word, the
boarders' hand, the far rounds, 72's cut-out) and whatever shape the two are in:

- **Near** (the captor awake, the prize a hull awake, within a boat's pull, `movement.BOAT_BETWEEN_NM`):
  the captor's order **`take possession of her`** (or `of the <ship>`; the player's and the rules
  captain's alike, through the vocabulary), refused in words beyond a boat's pull ("she lies two
  miles off: close her first"), for a ship that has not struck, for a boat away or lost, and for a
  captor whose own colours are struck. The boat carries the prize crew over and brings the
  prisoners back by 82's road (`Dealings.send_boat_to`, two jobs at the boat's pace), so that
  possession takes the quarter of an hour the boat takes and the log says each stage; the
  boarders' deck won is the one case with no boat (the party is on her deck already: the boarders
  are the prize crew's first draught, the leader of the party the prize master, §2.3, and the
  possession is at once).
- **Far** (either body far, or the two beyond a boat's pull with the prize struck by the far
  rounds or cut out): the possession on the far records alone, at once at hailing distance as
  72's cut-out has it (the far chase never comes nearer than hail; the boat's quarter of an hour is
  not modelled at far detail, said once here), the prize crew a count on the record and the
  prisoners a count; when either ship is made a hull later, §2.6 fills the counts with men.

What possession writes, on both shapes:

- **Her nation the captor's**, her colours the captor's hoisted over her own (`signals.set_colours`
  on her locker, state "shown", the captor's nation; the words of the lookout's reading "British
  colours over French" for a day after the taking: judgement, the period's sign of a prize, kept as
  the `Colours.over` word on the locker, read by `colours_words`), her far record's `nation`,
  `nation_adjective`, `flag` and `colours` the captor's nation's, so that every brain, set and port
  reads her as the captor's from here (`nations.at_war`, the ports' stance, the far captures'
  cover).
- **Her record**: `Vessel.prize`, a small mapping the truth and the court read: `captor` (her id),
  `taken_at` (the tick), `how` ("struck by morale", "carried by boarding", "cut out", "struck at
  far detail", "struck by the captain's word"), `nation_was` (her nation before), `crew` (the
  prize crew's count), `prisoners` (the count), `master` (the prize master's name), `goal` (the
  port she is for, or "in company"), `manned` true (false for a prize burnt or scuttled, §2.7),
  and the sums the court wants (`men_at_start`, her complement less nothing at the engagement's
  beginning, for the head money; `powder_lb`, `shot_lb` for the prize goods). Saved with the
  vessel (its dict), carried by a checkpoint, empty in one from before.
- **Her role and her captain**: `Vessel.role = "prize-master"`, a new role of `captains.ROLES`
  with its file (§2.4), her brain's intent set to **`carry the prize to <port>`** (a new form of the
  intent grammar, read as a passage to that port: `Intent.kind == "passage"`, the planner's legs by
  the port's tracks as every passage) or **`keep company with the <captor>`** (72's set: the prize
  joins her captor's company, `Squadron.join(as_prize=True)`, the `station` leg; the captor's
  doctrine says which, §2.4), the brain's `set_intent` re-reading the role from the vessel's
  (`role_of_vessel` reads `Vessel.role` first, 75's rule) and her near captain's role and doctrine
  made the same by `fold_in` at her next wake or at once when she is awake (`Captain.set_intent`
  with `scenario_role` set to the prize master's).
- **Her set**: out of the set she was in (`Squadron.leave`, "taken by the X") and into her
  captor's company where the doctrine keeps her, as 72's cut-out has it.
- **Her muster and her people** (§2.2), **her prize master** (§2.3), **her papers** (§2.5), **the
  far counts** (§2.6).
- **The lines**: the captor's log, urgent, `prize.taken` ("Possession is taken of the Deux-Frères:
  Mr Pearce and eight hands put aboard her as her prize crew, her people, fifteen, confined below;
  her master, M. Kerguelen, a prisoner in her cabin on his parole. The colours hoisted over hers.
  She is for Falmouth in company."), with the data the truth and the readings read; the prize's
  own log the same event from her side (`prize.possessed`: "Taken possession of by the Renard's
  people: ..."), so that a station in her (her captain's model, a captive's voice) is told; a far
  possession the one line in the captor's story and the prize's (`_story`) as the cut-out writes
  them, and in the player's log when within sight by the lookout's rule (her colours seen to
  change is the lookout's colours line, 71's; nothing is told the player that his people cannot
  see).

### 2.2 The prize crew out of the muster; her people prisoners

**The muster is whoever works her; the prisoners are whoever is confined.** The prize's working
company (`prize_hull.ship.extra["crew"]`) becomes a new `Crew` of the prize crew's `Sailor`s, moved
out of the captor's `Crew.sailors` (the same objects, their ids kept: a crew's ids are unique
within her, and the prisoners are no longer in this muster), the watch bill laid anew over them
(two watches by id order; `Crew.reindex`), the quarter bill reckoned for them when she beats to
quarters (73's `quarters_of` rebuilt from the muster, since its divisions are the sailors'). Her
former company becomes **`prize_hull.ship.extra["prisoners"]`**, a `Prisoners` record: her `Crew`
as it stood (the sailors with their hurt, the dead on her books), where they are confined
(`below`: the hold, the period's practice for the people; `divided`: so many taken into the captor
by the boat and put in his hold, which the captor's order `take <n> of the prisoners aboard`
does and the doctrine's `divide_prisoners` does by rule when the prisoners outnumber the prize
crew by its figure), the tick they were confined, whether they are **in irons** (after a rising
put down, §2.8), and the named few (§2.2's persons). The reason for the swap and not a flag on
one muster: every reader of the muster (`s.fit`, `by_station`, the bill, the runner's hands, the
routine's watches, the needs' meals, the health keeper, the quarter bill, the boarders and the
defenders) would otherwise have to learn a state that is neither hurt nor sick and never work a
prisoner; a muster of the men who work her is what every one of them already reads, and a merchant
brig of fifteen sailed by eight is short-handed at every evolution by the bill's own arithmetic,
which is the realism wanted ("thin and tired").

**The keepers re-pointed.** The routine, the quarters, the health keeper, the needs' keeper, the
evolutions' runner and the water keeper each hold or read `ship.extra["crew"]`; the build's first
job in this step is the audit of which cache the object and which read it at each call
(`grep extra\["crew"\]` and the keepers' constructors), each cache re-pointed by one function
`prizes.remuster(hull, crew)` that the possession and the retaking both call. What it finds is the
postscript's.

**Her named few** (`People`, the persons of the registry with the prize as home) stay her persons:
her master (or captain), her mate, her boatswain and the rest, each **confined** by the period's
custom through 65's hook (`Person.confined_to`, a place he may not leave; `movement.go` refuses in
words: "You are a prisoner, confined to the hold; the deck is not yours"): her master and her
officers to **the cabin** on their parole (§3.2's rule applied to a prisoner of the player's own
prize by parity: an officer's parole given, the cabin and the quarterdeck by day are his; refused,
the gunroom), her people to **the hold**. A person confined is `occupied` with "a prisoner" for
the readings, his needs the ship's (fed with the prisoners, §2.9), his station bindings on her
unbound (her `captain` bound to the prize master, her `officer of the watch` to the prize crew's
mate or to nobody: "the deck the book's"), and a model holding a station of hers stood down by
the handover's rule with the reason "taken in the prize" (82's `seat="stands down"`; the game
saved, the journal kept), **unless** his seat is an adversarial one that §6's refusal would have
refused at the seating, which cannot be (the refusal stands before). The persons of the captor's
company who go over with the prize crew are put aboard her by `put_aboard` (their home the captor,
their whereabouts the prize, as 84 has the prize crew: "persons whose home is the captor and whose
whereabouts is the prize"); the prize master's station in her is her **`captain`'s** (§2.3), the
rest visitors with no station (a hand has none).

**The division of the people** (the captor's doctrine, `divide_prisoners`): a prize crew of eight
over fifteen prisoners sails for Bayonne with them below (the truth's scene); a King's ship with
room takes the officers and half the people into her own hold by the boat (`take the prisoners
aboard`, `take <n> of the prisoners aboard`), where they are prisoners of hers (`ship.extra
["prisoners"]` on the captor too, the same record's shape), fed at two thirds, landed at her port.
A captor's prisoners outnumbering her own fit company by the doctrine's `prisoners_most` share is
the doubt the director is shown when it orders more aboard ("a frigate of 250 holds 300 prisoners
uneasily"), and the rules captain's reason to burn (§2.7) or to land them at the first friendly
port.

### 2.3 The prize master, and who leads on when the boarders' officer falls (97's paragraph)

**The ladder of standing** is one list, read by both roads: the first lieutenant, a lieutenant, the
master's mate (the merchant's mate), the senior midshipman, then the senior petty officer of the
muster by rating and skill (a boatswain's mate or a quartermaster, drawn as a person from his
`Sailor` by `People.draw_sailor` with his rating's role, so that the log names him). Falconer's
"his principal officer" is the first of the list present and whole; the period's practice gave a
frigate's prize to a lieutenant and a privateer's to her mate or a prize master carried for the
purpose, and the boarding party to the first lieutenant, led on by the next when he fell (James's
narratives of the cutting-out actions: the senior survivor took the command as a matter of course).

- **The prize master** (`prizes.prize_master(captor_hull)`): the first of the ladder present, whole
  and **not the captain** (the captain stays with his ship), **not the first lieutenant unless the
  doctrine says so** (`prize_master_from: ["lieutenant", "mate", "midshipman", "petty officer"]` in
  the role's file: a King's ship keeps her first lieutenant and sends her second; a privateer sends
  her mate; a merchantman that takes a prize, rare, her mate), else the first lieutenant, else
  nobody and the prize is not manned (she is burnt or left, §2.7, the refusal saying "nobody to
  command her").
- **The party's leader when the boarders' officer falls** (`boarding.party_leader(aw)`, replacing
  `boarders_officer`'s None): the same ladder among the boarders on her deck (the persons of the
  attacker's company whose `Sailor` is among `boarders_of` and fit, in the ladder's order; the
  senior petty officer drawn as a person when no officer stands), so that the deck won has a man
  on it who leads on and who is the prize master's first draught. **97's pin moves**: under the
  default seed the first lieutenant Mr Pearce is killed at tick 530 and the deck carried; on this
  branch the party is led on by the next of the ladder present (the test names him from the muster
  as it falls), the pin re-measured old beside new with this paragraph as the cause (`tests/
  test_between_hulls.py::test_the_boarders_officer_killed_in_the_round_leaves_the_deck_carried_and_
  none_leads_on` renamed for what it now pins, truth 7-325 reading both).
- **His station in the prize** is her `captain`'s: `put_aboard(world, master, prize_hull,
  "quarterdeck", station="captain", by="the prize crew")`, one new keyword of 82's function (the
  station a person holds in a hull not his own: the visitor's voice by default, as now; `"captain"`
  for the boat's commander and the prize master, the rule 82's §2 gives the boat's commander and
  the design extends to a prize), his harness following into her `agents["captain"]` where a model
  holds him (the brief's "a model's seat by 67's door with his harness following him"), his own
  station on the captor standing bound to him meanwhile (82's rule: the captor's `officer of the
  watch` is nobody's or the book's), and her **rules captain** his stand-in when no model holds
  him (the prize master's doctrine, §2.4), as any hull's. His brief's head says what he commands
  ("You are Mr Pearce, prize master of the Deux-Frères, a merchant brig taken by the Amazon: eight
  of her people are your prize crew, fifteen of hers your prisoners confined below; she is for
  Falmouth in company with the Amazon") through `shape_words` and the ship words, 85's in-world
  rule binding every sentence.

### 2.4 The doctrine of it: the captor's role files, and the prize master's own

**The captor's** (`data/captains/kings-ship.yaml`, `cruiser.yaml`, `commodore.yaml`,
`privateer.yaml`; the merchant and the packet take no prizes and say so by `mans_prizes: false`;
the fisherman none), new thresholds each with its source or its judgement:

| threshold | the King's ship | the privateer | what it is |
|---|---|---|---|
| `mans_prizes` | true | true | whether a prize is manned at all |
| `prize_crew_share` | 0.08 of his fit men, at least 6 | 0.15, at least 6 | the prize crew's size, bounded by `prize_crew_most` (half of her complement) and by what sails her (the bill's least hands for her plain sail, read from her file: judgement, the 1805 practice of thin prize crews, James passim) |
| `prize_master_from` | lieutenant, mate, midshipman, petty officer | mate, midshipman, petty officer | §2.3 |
| `divide_prisoners` | over 1.5 × the prize crew | never (a privateer has no room) | when half the prisoners come into the captor |
| `prisoners_most` | 1.2 × his fit men | 0.5 | the share above which he burns or lands them |
| `burns_when` | "not worth manning" | "never" | §2.7's rule: a prize whose valuation (§5.1) is under `worth_least` (£400, judgement) with the captor's fit men under `fit_least` (0.8 of his complement), or no prize master to be had |
| `prize_goal` | "the nearest friendly port" | "home" | the prize's goal: the nearest port open to his nation by the stance (a King's ship's prize for Falmouth from the Lizard; a privateer's for her home port, the intent's origin, Bayonne or St Malo) |
| `prize_company` | "in company while bound the same way" | "parts" | whether the prize keeps company (the set) or parts at once |
| `parole_accepted` | true | true | §3.2 |
| `prisoners_landed` | "the first friendly port" | "home" | §3.3 |
| `takes_possession_within_nm` | 1.0 | 1.0 | he closes a struck enemy within this to take possession (the state `taking possession`, below) |

**The captor's machine**: a new state **`taking possession`** of `captains.STATES` with its book
(`heave to` within a boat's pull of the prize, `take possession of her` once hove to; the near
captain's `_work` gives the order and the state ends at the possession's line, `prize.taken`, or
after a glass with nothing taken: "she is gone"), entered from `engaging` on `enemy struck` where
`mans_prizes` (the row `{from: engaging, on: enemy struck, to: taking possession}` replaces the
`to: on passage` row in the files that man prizes; the far brain's `_enemy_struck` already reads
the stimulus), and from `chasing` on `enemy struck` (the cut-out's road for a ship that fights,
§4.5). The transition out: `{from: taking possession, on: prize taken, to: on passage}` (the
stimulus true when `Vessel.prize` names him as captor) and `on: overmatched, to: evading` (a
cruiser coming up before he has her: he leaves her). The far brain resolves the state on the far
body as a `to_ship` leg to hailing distance and the possession at once there (§2.1).

**The prize master's** (`data/captains/prize-master.yaml`, the merchant's seamanship: the form of
`merchant.yaml`): `engage_nm: 0` (a prize fights nobody), `stranger_hostile_nm: 6` (she hauls off
from every stranger that is not her captor and not of her captor's nation, a prize being worth
nothing lost), `yields_when_caught: true` (72's far capture rule retakes her by a cruiser of her
old nation coming alongside with no cover: **the retaking by a cruiser coming up is 72's rule
read from the prize's side**, the cruiser her captor now, the prize record rewritten with
`retaken_by`, her nation her old one again, the prize crew her prisoners and the prisoners her
company, §2.8's swap), `gale_kn` the merchant's, the books the merchant's passage books with the
`station` leg of `in company`, and the hail's standard answers of a prize ("the Deux-Frères, prize
to the Amazon, for Falmouth": `hail.yaml`'s table gains the role's row).

### 2.5 Her papers, and the captured signal book

A prize's hull keeps her papers as any hull's (84's step 1: `papers` per hull). Possession makes
**a thing** by 53b's road (`things.make`: "the Deux-Frères's signal book, in the captain's keeping"
on the captor, with her nation's root as the thing's description) when her locker holds a book or a
private table (`signals.held_books`, `table_of` of her hull; a merchantman has none and the log
says "no signal book or private table found in her: a merchantman"), and adds her nation's root to
the captor's **`held_books`** (the scenario's `papers.signal_books` list on the captor's hull's
scenario copy, which `signals.books_for` reads: a captured French book lets the captor's lookout
read French hoists, 71's design: "a captured book is a thing of M7's prizes"); her private table of
the month is carried as a paper of the captor's (`Papers.write("the captured private table", ...)`)
and read by `signals.table_of` as the captor's answer to a French challenge for the month only
(the tables change by the month; the captor who answers a French private signal right under false
colours is 71's ruse carried further, said in the truth). The prize's own log, her manifest and her
purse are hers still (her purse is prize goods, §5.1, and her manifest the court's evidence: the
Regulations' art. II, "all passports, custom-house papers, clearances, log-books and all other
ship's papers which shall be found on board" sent to the court).

### 2.6 The far body, and a far prize made a hull

A prize at far detail is her `Vessel` with the fields of §2.1 and no hull; her `damage` the far
rounds' sum (§4). When the cap makes her a hull (`make_hull`, 84's step 6: her ship from her file
at her truth, her company mustered **whole from her file**), `prizes.fill_far_prize(hull)` runs
after the adoption: her muster cut to the prize crew's count (the first `crew` fit men of the
file's muster by the bill's order, the trimmers and the helm first, so that she sails; their names
the muster's draw, since the captor's names are not hers), the rest her prisoners (`Prisoners` from
the men cut, confined below), her named persons her former company's (prisoners by the custom) and
a prize master drawn as a person of the captor's company when the captor has a hull (`People.
draw_sailor` of a man of the ladder's rating from the captor's muster, moved into her by `put_
aboard(station="captain")`) or made from words ("the prize master, Mr Trevithick, of the Renard")
when the captor has none, his home the captor's id (a person of the world keeps a home, 84's
rule). Said in her log once. The far damage into her parts is §4.4's road. **The far crew counts
are not names**: a prize taken and sailed home wholly at far detail carries a prize crew of eight
on her record and never names them, as the far business's ships carry crews of nobody; the truth
says "eight of the Renard's people" and no more.

### 2.7 Burning and scuttling; a prize not worth manning

`burn the prize` / `set fire to her` and `scuttle her` / `sink her` (the captor's orders, refused
for a ship not his prize, for a prize beyond a boat's pull, with people still in her: "take her
people out first", which `take the prisoners aboard` does): her people into the captor by the boat
as prisoners (§2.2's division, all of them), her stores and her powder and shot taken off where the
captor has room and the time (`take her powder and shot` through 86's magazine as a transaction:
captured powder is prize goods of the captor's, the owner's ruling; `Magazine.receive` as the hoy's
stowed stage receives), then the vessel `done` with the word (`burnt`, `scuttled`) in her record
and the captor's (`Vessel.prize["manned"] = False`, `fate`), a line urgent in the captor's log and
the lookout's "a ship on fire, bearing SE" to every lookout within sight for an hour (judgement;
the glow by night at the lantern's rule's reach: `ships._lights_of` gains the fire). Nothing is
paid for her at any court but **head money** where she was a ship of war or a privateer (the
Regulations ch. IV art. V: the vouchers without the condemnation), and the captor's doctrine burns
by `burns_when` (§2.4). A prize left (neither manned nor burnt) is a struck ship lying to that her
own people retake in a glass (her machine back to `on passage` when no captor is within a mile for
thirty minutes: judgement, the period's prizes that got away when the captor was drawn off).

### 2.8 Retaken: the prisoners rising, and the cruiser coming up

**The rising** is a rule of the prize's own minute (`prizes.minute(hull)`, run in both ticks of
her hull, awake and asleep, and on a far prize's record at far detail with the counts alone):
while her prisoners outnumber her prize crew's fit men by `RISING_ODDS` (2.0: judgement; the
prize crews that lost their prizes were a third of the prisoners or less, James passim), and the
prize crew is **tired** (the mean fatigue of the prize crew over `RISING_FATIGUE` 0.6, or the hours
since possession over `RISING_HOURS` 18 with no watch below, which the bill of a crew of eight
cannot keep: the muster's own arithmetic), and the captor is **not near** (no ship of her captor's
nation within `COVER_NM`, 72's two miles, awake or far: the gale that separated prize from captor
is the study's case, and needs no rule of its own), and the prisoners are not in irons, then **once
an hour a draw** from the prize's own stream `prize` with chance `RISING_CHANCE` (0.25 a qualifying
hour: judgement, so that a thin and tired prize crew loses her in a night more often than not and a
sufficient one never) rises. The fight is **73's tables on one deck**: the prize crew the
defenders (their arms served 1.0, the marines' kit where marines are among them, their temper the
captor's morale figure carried in the record), the prisoners the attackers (unarmed 0.5, their
temper the prize's old doctrine's `morale_start`, their cover 0.8 in the first round as boarders
crossing), a round a minute by `boarding._strength` and the Poisson losses on `ROUND_LOSS`, the
men struck by `strike_a_man` on each side's list (the prisoners' losses from the `Prisoners`
record's sailors), the end by `CARRIED_RATIO` on either side or `CONTEST_ROUNDS`: **retaken** (the
swap: the prisoners' `Crew` her muster again with its hurt, the prize crew her prisoners confined
below, her nation and colours her old nation's, her brain's role and intent her old ones (kept on
the record at the taking: `intent_was`), `Vessel.prize["retaken"] = ("the prisoners rising", tick)`,
the prize master a captive in her cabin on his parole by §3.2's rule, his station stood down by the
handover's rule as a captive's is, the lines urgent on her log and the captor's story) or **put
down** (the prisoners' losses, the rest **in irons**: no rising for `IRONS_HOURS` 24, the line
"the prisoners rose and were put down: n of them killed, the rest in irons"). Judgement
throughout, named in the tuning notes; the figures are the owner's to move. A far prize's rising
is the same rule on the counts with 73's strengths over the counts alone (no men named; the losses
drawn as counts into `damage`), so that a prize sailed home at far detail may be lost at far
detail.

**The cruiser coming up** is 72's `far_captures` for a prize that yields (§2.4), and §4's rounds
for a prize whose prize master fights (none does: `engage_nm: 0`), with the near action's road
(70's strike, then `take possession`) when the two are awake. The retaking by boats at anchor (§20's
first truth as the spec wrote it) is **left to 63 and 77 with the truth's words amended** (§8): the
boat as a vessel is 82's and the cutting out by boats 77's, and a frigate's boats retaking a prize
at anchor is that drill; the truth's cruiser comes up at sea instead, which the period's record has
as often (the recaptures of the Channel, the prize courts' salvage cases: from memory, UNVERIFIED).
**Salvage** on a recapture (an eighth of the value to the recaptor, from memory of the Prize Acts,
UNVERIFIED) is the court's rule of §5.3 when the recaptor brings her in.

### 2.9 What the prize's hull does with her prisoners every day

Fed at **two thirds** of the company's allowance (the Regulations Sect. XII ch. III art. IX, read
on file): the needs' meals draw the stores for the prisoners' count at two thirds beside the
muster's at the full (`needs.py`'s daily draw gains the prisoners' term; nothing of the needs'
states for the prisoners as persons beyond the named few, who are fed as the persons of the hull
are). Their sick are the surgeon's where she has one (the health keeper's queue takes the
`Prisoners` record's hurt men after her own: the Regulations' art. VIII's care for the sick
prisoners). Their count is on the truth, the readings and the butcher's bill of the prize. The
dead among them buried with hers (`bury the dead` takes both lists).

## 3. The captive's channel is the visitor's voice (item 3)

### 3.1 The player struck

The player's `strike the colours` is never refused (70) and now has its consequence: his ship lies
to, and **when her captor takes possession** (§2.1: the rules captain by `taking possession`, a
model at the captor's captain's station by its own `take possession of her`, or the far body at
hail) the player's person (`knowledge.players_person`) **is put aboard the captor** by `put_aboard
(world, person, captor_hull, place, seat="stands down", why="taken in the prize", by="the captor")`
with his place by §3.2's parole rule; his officers with him or confined in the prize by the
captor's `divide_prisoners`; his people the prize's prisoners (§2.2). The captor is made a hull if
she has none (a far body that takes the player's ship: `make_hull` under the cap's order, the
possession a dealing of the first rank, §4.3), so that the captive is aboard a real hull with
places, a company and a log.

**His own station stands down** by the handover's rule (the brief's "or stood down ... as the
design decides for a captive"; the game saved, the journal kept, the station released with the
reason "taken in the prize"): a captive does not command his ship, and a station standing bound to
him would say he does; her `captain` is the prize master's (§2.3). The player's seat (`PlayerSeat`,
82's step 3) at a lesser station of hers is stood down the same; a model at a station of hers
(his officer, his master) is stood down "taken in the prize" (§2.2). What is **not** stood down is
the player himself: **his prompt follows his body** (decision 62, `movement._drivers_follow`: the
drivers' `followed` moves to the captor's hull with his person, a routine line `hull.followed` of
her log, a consequence of the possession and never a driver's input, so that a replay moves it the
same), and at her prompt he is **a visitor of 82's kind** (65's step 4: the player at the prompt
reads by his place, `knowledge.players_visitor`; his `say` is in his own name from his spot): his
reach a passenger's: `where am I` ("aboard the Renard, in the cabin, a prisoner on parole, of the
Amazon"), `the ship` (hers), the readings his place allows (65's table: the cabin's glass and
tell-tale, the deck when he has the liberty of it), `say to the captain: ...` (85's; `say to the
prize master`, `say to the sentry`), `ask`, `tell`, his journal (`journal_of` by his person,
45c's), a free line, `stand by until <an event or a bell>`; every order of her deck refused in words
naming his state ("You are a prisoner aboard the Renard; her deck is not yours. You may speak:
'say to the captain: ...'"), and every order of the Amazon's refused ("The Amazon is a prize under a
prize master; nothing of her deck is yours from here"). A model seated as the player's captain
through a door is in the same case through its harness (the visitor's voice, 82's `move_to`): the
same channel, the brief head saying he is a captive (the visitor's brief with the captive's
sentence: `CAPTIVE_BRIEF`, in-world under 85's rule), its stand-by and its journal going on, so that
**the game does not end at the strike for a model either**.

### 3.2 The parole, the places, and what he can say

**The parole** (`prizes.parole(hull, person, given: bool, by)`) is a state of the captive on the
hull's `Prisoners` record (`parole: given | refused | not asked`) and of his person (`confined_to`):

- **asked** by the captor's captain: a rules captain by doctrine (`parole_accepted`) says the
  period's words in the captive's hearing at his place as a line of the hull's log the captive's
  spot hears (66's hearing, `say as`-shaped but the rules', `prize.parole_asked`: "Captain Bowen,
  your sword, sir; I return it you. Will you give me your parole not to attempt the ship nor to
  leave her without my leave?"), the words from `data/captains/hail.yaml`'s new `parole:` table by
  the captor's nation (the French captain's in French and English as the hail's lies are: "Votre
  parole, monsieur"; Spain's row too, decision 64); a model at the captor's captain's station asks
  in its own words (`say to Captain Bowen: ...`) or not at all; the director `say as` the captain
  where nobody holds him.
- **answered** by the captive in his own words: `say to the captain: I give you my parole` /
  `say to the captain: I will not give it` (the player's `say to`, a model's `say`): the game reads
  the answer for the parole by a small table of the period's forms (`PAROLE_GIVEN_WORDS`: "give
  my parole", "my parole", "you have my word", "I give it"; `PAROLE_REFUSED_WORDS`: "refuse",
  "will not give", "no parole", "I decline") **only when a parole has been asked of him and not yet
  answered**, so that no other sentence is read for it; an answer the table cannot read leaves the
  question open and the captor's rules captain asks once more after a glass, then takes it as
  refused (said); the director's `aboard the <captor>: the parole of Captain Bowen given | refused`
  sets it for a captive nobody asks (doubted where nobody has asked). The exchange is **two lines
  of both logs** (the captor's, where both stand; the prize's by the news when her master is
  told: no), heard by the stations whose spot hears them, **and in no sample's operator voice**
  (the harness sends only the brief in that voice; everything after is the log's data: the
  consent brief's rule, which §8's truth 7-356 pins by the fake door).
- **by rule** when nobody speaks for a watch: an officer's parole given, a seaman's not asked (the
  period's custom: a commissioned officer's word was taken; the people were confined), said.
- **what it gives**: `given` → the cabin and the gunroom his, the quarterdeck by day ("the liberty
  of the quarterdeck", `confined_to` a set of places: `{"cabin", "gunroom", "quarterdeck"}` by day,
  the cabin and the gunroom by night), his sword returned (a thing of 53b's, "Captain Bowen's
  sword, in Captain Bowen's keeping", made at the taking in the captor's keeping and given back by
  the parole: the period's gesture, which the log says); `refused` → the gunroom alone, a sentry
  at the door (said; nothing modelled of the sentry but the refusal's words); a seaman → the hold.
  A captive on parole who is put in the boat or ashore by the director's forms is a parole broken
  only if he leaves without leave: the director's `person: "Captain Bowen" goes aboard the X by
  the boat` performs (the captor's captain gave leave, by the form's own words), the player's own
  `go to the boat` from a captor's deck is refused ("a prisoner on parole does not take the
  boat").

**His people's parole** is not asked; the named few of his company (his officers) are asked as he
is, each by rule unless a model or the director speaks.

### 3.3 The captor's captain by doctrine, and what the director shapes

The captor's rules captain, after the possession: the parole asked (§3.2), his course for his port
(`prisoners_landed`: the first friendly port by the stance for a King's ship, home for a privateer),
the prize in company or parted (§2.4), and at the port **the prisoners landed**: on his hull's
arrival in port (`Dealings.in_port()`) a job of the port's kind at the boat's pace lands the
prisoners (the `Prisoners` record's men into the port's **Agent for Prisoners** (the Regulations'
art. V: the list of their names and the day they were first victualled, which the paper "the
prisoners' list" carries), a new place of every port of a nation at war (`places.PORT_PLACES`
gains `the agent for prisoners` with its `done` and `found`, data in `data/ports/` by nation's
word: the Agent for Prisoners at a British port, "le commissaire des prisonniers" at a French,
"el comisario de prisioneros" at a Spanish, decision 64), the captive's person ashore at that place
(`Dealings.land_person`, his station words "a prisoner of war ashore at Brest"), from where **the
continuation** is the director's: a cartel (§3.4), an exchange, the court (§7) when he is home. A
model at the captor's captain's station does all of this by its own orders (the forms are the
grammar's) or not at all, as its character has it; the director shapes what follows through
plausible causes as always (a gale that night: `weather:`; a cartel in the offing: §3.4; a friendly
cruiser at dawn: `ship: a frigate "Medusa" of Britain at ..., intent: ...`, which 72's and §4's
rules then play out).

### 3.4 The cartel

`cartel: a cartel from <port> for <persons>` (or `for the prisoners of the <ship>`): a vessel put on
the sea as the `ship:` form puts one, of the **cartel** description (a merchant brig under a flag
of truce: `DESCRIPTIONS` gains `cartel` with the merchant brig's file, her colours the white flag
"a flag of truce" which no captain fires on (`Captain._is_enemy` false for a cartel; the far
captures and the rounds pass her by; a shot at her is 71's pirate's act told), one gun for signals
(her fit "cartel", the merchant brig's file gains the fit through the generator with its source:
Falconer, CARTEL), bound for the hull that holds the persons named (a `to_ship` leg to hailing
distance, then the port named), and alongside her she takes them by the boat (82's two jobs) and
sails for her port, where they are landed free (the exchange is the cartel's business ashore, not
modelled: said). The form is doubted beyond a day's sail of the port and refused for a person
nobody holds prisoner. The cartel's and the captive's **places and words filled out are 80's**
(the brief's "Not built here"): here the cartel is a hull of the sea with the one errand, and the
captive aboard her a visitor as anywhere.

### 3.5 A prisoner of the player's own prize, by parity

The same channel serves a prisoner of the player's prize: her master is a person of her company
confined by his parole in her cabin (§2.2), his voice a seat the director may hold for a model
(`seat: <model> as M. Kerguelen for 20 samples`, 67's voice: **not** an adversarial seat, since a
prisoner fires into nobody and takes nobody; §6), or the director's `say as`; the player speaks to
him by `say to the master of the Deux-Frères` from his own deck when the two are within hail, or
aboard her as a visitor by the boat (82's road, the prize in company lying within a boat's pull).

## 4. The far fight on the sleeping hulls (item 5)

### 4.1 75's finding first: the far ship's length

`combat/far.py:111` reads `spec.hull.length_m`, a key `HullSpec` has not (`length_waterline_m` is
its), so every far ship's length is 0.0 and `shot.hit_chance` floors her size term at 0.5
whatever she is. **The mend is one read** (`length_waterline_m`), made first and alone in its own
commit, and **the far fight's pins re-measured old beside new with this line as the cause**. Measured
on the trunk at f67640b in the scratchpad before this note (the design's own throwaway measure, as
83 did; the build repeats it on the step's tree):

| the fight at seed 7 | as it is (length 0.0, size 0.5) | mended (her waterline, size by her length) |
|---|---|---|
| truth 7-139: the two cutters at two cables (400 m), the King's carronades at the hull, the privateer's long guns at the rigging | the long-gun cutter struck after seven rounds (21 min), four hurt, three holes; the King's cutter nobody hurt, 63 shot fired to 58 | struck after **seven rounds (21 min)**, **five hurt**, three holes; the King's cutter **one hurt**, 57 to 61 |
| the same cutters at a cable (185 m) | struck after three rounds (9 min) | struck after **two rounds (6 min)** |
| two frigates at two cables (370 m), one at the hull, one at the rigging | struck after six rounds (18 min), 81 hurt to 14 | struck after **three rounds (9 min)**, 75 hurt to 22 |

So the pin **7-139's outcome stands** (she strikes in the same seven rounds; the truth's bands hold:
under an hour, hurt and holes at least one, the record repeating), its docstring's figures move
(four hurt to five, the King's cutter one hurt), and the tuning notes' row moves with them; the
cutters at a cable and the frigates move by a round and by half, which no pin reads (the near fights
of 7-140 and 7-133 are the near body's and unmoved: `action.target_of` reads `hull.length` from the
part graph, which is right). Every figure the far rounds give from here is the mended one; the
agreement of §4.6 is measured on the mended read. `test_profile.py`'s and `test_indefatigable.py`'s
readers of `far_ship` read the broadside's weight alone and do not move.

### 4.2 The far engaging transition

`FarCaptain._enemy_within(p, within_nm)` returns the nearest enemy of the perception's strangers
within the distance (the same shape as `Captain`'s: by the colours shown and the wars, the private
signal and the hail, the shot that told, `_known_enemy`; not spoken; not struck), so that the
doctrine's rows **`{from: ..., on: enemy in range, to: engaging, unless: overmatched}`** fire for
the far body as they fire for the near (the same files, the same thresholds: `engage_nm` under
the nation's habit's `range_factor`, 71's). **The state `engaging` on the far body** (`resolve_
state`): a `chase` leg to the mark at the doctrine's range (`engage_range_cables` × the habit's
factor, in metres; the chase leg's `arrive_m`, which the body keeps once reached: `Vessel.tick`'s
"within hail: she keeps her distance"), **the gage** not modelled at far detail (said: the far body
has no close-hauled angle but her polar's beat; the near body's helm law is 71's), the transitions
out as the near body's: `enemy struck` (to `taking possession` where the doctrine mans prizes,
§2.4, else `on passage`), `enemy out of range` for `break_off_minutes`, `overmatched` to `evading`,
`chase stale` (88's row). A ship with no guns (her fit "unarmed", a merchantman) in `engaging` is a
ship that **runs** (`merchant.yaml` keeps `engage_nm: 0`: no row fires; she is chased and struck
by the rounds or yields by 72's rule as now).

### 4.3 The rounds, on the far records

`combat/far_action.py` (new; `far.py` keeps the tables and gains `round_once`, the one round
`fight` loops over, so that 7-139's measure is the same function the world runs): once a minute in
the sea's minute (`Vessels.tick`, after the brains have judged and before the bodies move, beside
the sets' and the regimes' minutes), **every pair of far bodies of which at least one is in
`engaging` with the other as her mark** (`brain._stranger`), within the reach of her guns (the
longest `random_m` of her fit's guns; beyond it the round fires nothing and the state's chase leg
closes her), **resolves one round every `FAR_ROUND_S` (180 s, 70's step)** from the first minute
the two are in range: each side a `FarShip` built from her `Vessel` (`far.far_ship` from her file,
her fit and her nation, the aim and the morale figures from **her brain's doctrine under the
nation's habit** (`doctrine.threshold("aim")` with `habits.aim` where the file leaves it empty,
`morale_start`, `strike_below`), her complement less her record's killed and wounded, her record's
dismounted, holes, holes below, sail cut, spars gone and morale carried in, so that a ship that
fought yesterday fights hurt today), the range the bodies' truth, the draws from the World's
stream **`far`** (opened at the first far round and not before, so that no sailing passage's list
of streams moves: 70's rule for the gunnery's stream; the truth 7-139's measure keeps its own
`Rng(seed).stream("far")`), and the sums written back into `Vessel.damage` (the keys 84's step 5
writes, plus `sail_cut`, `morale`, `rounds`, `last_round_tick`) with a line in each side's story
(`_story`) and, where either has a hull asleep, in her log (`action.far_round`, routine: "A round
of the action with the Renard at two cables: three shot struck us, one man wounded; our fire told
twice"), so that a station on a sleeping hull is told her action at the rounds' pace. A pair with
**one side awake** (a hull under the cap, the other far) is not fought here: the awake hull's
battery fires at a far mark by 70's road already (`hits._far_hit` sums into the far record) and
the far mark's reply is the round's half (**the far ship fires her broadside at the awake hull by
the tables**, the hits resolved into the awake hull's parts by `hits.resolve_shot` with a
synthetic `Gun` of her fit's kind: judgement, the least that makes the fight two-sided; measured
and said), until the cap wakes her (§4.5).

**The strike by morale** in the rounds is `far._judge` on the carried sums: the colours come down
by the doctrine's line as 70 measured; then `prey.struck`, her colours "struck", her state and her
brain's `struck`, her plan `lie_to` (as `far_captures` writes them), the captor's `taking
possession` (§2.4) and §2.1's far possession at hailing distance. **A ship with no fit to fire**
(unarmed) under a round's fire strikes by the same morale law (her `morale_start` the merchant's
0.5, the odds term with no guns of her own: `far._judge`'s `enemy.broadside_lb` over `max(own, 1)`
gives the most odds), which is 7-137's merchant brig at far detail, and 72's `far_captures` yields
her without a shot where she yields when caught: the two rules together carry 72's cut-out from
hailing distance to its end **by the same rounds** for a ship that fights (the packet, `yields_
when_caught: false`, fires her six-pounders and strikes by morale; §8's truth 7-369).

### 4.4 The far state into the near body, and back

**Into the parts** (`prizes.far_damage_into_parts(hull, damage)`, called by `make_hull` after the
adoption and by `_to_full` at a wake, for the counts the record carries beyond what her parts
already show): the men killed and wounded applied to her muster (`hits.hit_man` on so many fit
sailors drawn by her `muster` stream, the killed share as the record has it, the wounded with a
wound "a round shot" in words: 73's health keeper takes them), the guns dismounted (`gun.
dismounted = True` for so many of her engaged side's guns from the end, as the far round dismounts
from the end), the shot holes into her damage keeper (`hits.Damage.holes`: so many above, so many
below the water with `below` true, their places drawn along her length, so that 73's water keeper
makes water from them: rule 1, damage is state), the sail cut as the condition of her set sails
(the share spread over them: `Sail.condition` reduced by the share; a sail under a floor blown
out), the spars gone as her topgallant masts and yards wrecked first (`Spar.wrecked` on the least
spars in the generator's order: judgement, a spar at far detail "is not a lower mast", `far._judge`'s
own words). **The record keeps what was carried in** (`damage["carried_in"]`: the counts applied),
so that the carrying is done once. **Back** is 84's `write_damage` at the sleep (the counts
recomputed from the parts: the killed and the wounded by the muster's hurt, the guns, the holes,
the spars, the sails blown out) and the far round's `hits` and `weight_lb` kept; a sleeping hull
fought by the rounds has her record moved by them and her parts moved at her next wake. **The two
roads agree by construction** (the record is the parts' sum, and the parts are the record's
application) and the truth 7-360 pins it: a hull woken with far damage, slept again, carries the
same record; a hull that fought awake and slept carries the parts' sum.

### 4.5 The engagement first among the cap's reasons

`crews.switch`'s `rank` gives a vessel in `engaging` (or `taking possession`, or `struck` within
the hour) **rank 0 with the dealings and the held hulls**, so that two far ships that meet in anger
**within the promotion's range** are woken together (the mark of an engaging ship ranked with her,
even when the mark's own brain is a merchant's running) and the near action takes over (70's), the
far state carried into their bodies by §4.4; **beyond the range they fight asleep by the rounds**
(the owner's decision 8 as 83 recommended it: "no" to waking two sleeping hulls far from the
player; a scenario may raise the cap), the player's lookout seeing the flashes and hearing the guns
by the lookout's rule (`lookout.py`: gunfire heard at the distance the period's logs give, a new
sound of `ships._sound_of`: "the sound of guns to the south-west", by night the flashes seen at
the horizon's range: judgement, a line of the player's log once a round while any far round fires
within the sound's reach, so that the owner's "actions off the horizon" are heard). The cap's
count is unchanged (three), the allowance 82b's; an engagement is a reason, not an exemption.

### 4.6 The agreement, and the pace

**Truth 7-359**: the near fight of 7-140's form (two cutters, the King's carronades and the
privateer's long guns, at a cable with the fire as they bear, 70's near road, the two awake) against
the far rounds of the same two at the same range (the mended `far_ship`s, `far.fight`): the two end
**within a round of each other** (the far at a cable in two rounds, six minutes; the near at a
cable in three minutes after the first shot: the distance between them is three minutes, one
round; the measure on the step's tree is the truth's, and if it does not agree within a round the
truth pins the figure found and says so, with no table's figure moved for the agreement's sake:
realism, not pacing). The far fight is coarser than the near by design (rule 5); where the two
disagree by more than a round the tuning notes say by how much and why (the far round's steady
platform and the near body's roll, the near chase's closing).

**The pace**: the far rounds cost a `far_ship` build (her file read, cached by `load_spec`'s own
cache) and a few hundred draws every three minutes a pair, nothing a tick; measured in truth 51's
form with a scenario of two far ships in anger beyond the range beside the frigate (7-361,
informative, `pace`; the floors not lowered), and the pace tests of before run as they stand: the
far fight wired **can move passages with two far ships in anger** (the brief's caution): the
business's cruisers of two nations on neighbouring stations, 72's convoy and its privateer (7-152,
7-153, 7-159, 7-160: the privateer hovers at a league and evades the escort; her `engage_nm` 1.5
against a merchantman within it is the case to measure), the blockade's inshore squadron and a
sortie (7-154). Each is **run before and after the wiring on the same tree with the rounds toggled**
(`far_action.ENABLED`, the toggle for the bisection), the moved pins listed old beside new with the
pair that fought and the round that moved them, in the tuning notes and the postscript; a pinned
passage with no two enemies within gun's reach of each other cannot move (the round fires nothing),
and that is the proof for the rest.

## 5. The prize court and the money (item 2)

### 5.1 The valuation, the cargo and the prize goods

**The hull's valuation** (`prizes.valuation(spec, age_years, fit)`), the least 60 can take up for
buying and selling: her burthen (`spec.hull.tons`, the file's tons burthen) × a price a ton by her
kind and age (`data/business.yaml` `prize_values:`: a merchant hull £8 a ton and a man of war's
£12, FROM MEMORY of the Navy Board's purchases of prizes and the Lloyd's sales of the war years,
UNVERIFIED; worn by age at two per cent a year from her build year where the file gives one, else
taken as ten years old), her guns at £4 the hundredweight (the Ordnance's price of iron, FROM
MEMORY, UNVERIFIED), her stores at the yard's prices of the port (the port file's `dockyard.items`
where the item is there, else nothing). The shape: a function over the ship file's figures and the
port's tables, every figure in data, its source or "FROM MEMORY" beside it, which 60 takes up for
a ship bought at a port by the same function.

**The cargo at the market** (53b's transactions): each good in her hold sold to the port's market
at its price of the day (`Market.price`, `sold_to_port` moving the supply by the tons: 84's
step 4's rule), the sum into the prize account.

**The prize goods** (the owner's ruling, 86's fold): her powder and shot (`Magazine`'s pounds by
kind) valued at the port's `ordnance:` block's prices where it has one (`powder_per_barrel_pounds`,
`shot_per_ton_pounds`: 86's keys) else at the merchants' defaults (`ordnance.DEFAULTS`), and her
purse's money as it stands; a captor may instead **take her powder and shot into his own magazine**
before the court (`take her powder and shot`, §2.7's transaction through 86's `Magazine.receive`),
in which case they are his and not the court's, said in the account.

### 5.2 The court, at the port

**The court sits where she is brought in**: when a prize hull enters a port (`Dealings.in_port()`)
whose stance to her captor's nation is open (the captor's own nation's port, or an ally's: the
nations at war with her old nation and not with the captor's; a neutral port gives no court and the
prize lies there, said), a **job of the port** (`Job(kind="prize_court")`, 84's road for a coarse
act, due in `court_days` from `data/business.yaml` `prize_courts:` by the port's nation: Britain
7 days (the Vice-Admiralty courts' summary condemnations of the war; the High Court's months are
not modelled: judgement, named), France 7, Spain 10 (judgement, decision 64's row), with the
court's name in the words ("the Vice-Admiralty court at Gibraltar", "the High Court of Admiralty"
for a home port, "le Conseil des prises" at a French port, "el Tribunal de presas" at a Spanish:
the names from the period's usage, FROM MEMORY) sits and **sentences**:

- **condemned** as lawful prize where her old nation was at war with the captor's at the taking
  (`nations.at_war` at the taking's date, read from the record), or where she was a pirate (an
  armed ship without a commission, 71's `outlaw` on her record: the Regulations' art. III), or a
  neutral carrying an enemy's cargo to an enemy's port (her hold's goods' `origin` an enemy's and
  her goal an enemy's port: 43b's market rule read the other way; judgement);
- **restored** with costs where she was a neutral wrongly taken (her nation at peace with the
  captor's and her cargo and her goal no enemy's): she is given back (her nation, colours, role,
  intent, muster and people restored by §2.8's swap; her people were prisoners for the passage,
  which the log says), the captor pays **costs and damages** (`costs_share` 0.1 of her valuation,
  judgement, FROM MEMORY of the Admiralty court's awards of costs, UNVERIFIED) from his purse or
  owes them (`Purse.owe`), the line saying why ("restored to her owners, a Danish neutral wrongly
  taken; the court awards costs against the captors: £120");
- **salvage** on a recapture (a ship of the captor's nation retaken from the enemy): an eighth of
  her value to the recaptors (FROM MEMORY, UNVERIFIED), she restored to her owners.

The player's and the director's roads: the court's sentence is a job and a rule, read by the
director's truth; the director overrides by `port <id>: the court condemns | restores the <prize>`
(a form of the `port` channel, doubted where the rule gives otherwise and performed with a reason:
the court's whim is a plausible cause), and the captain reads `the prize` and `the prize money`.

### 5.3 The money, by the eighths; the purse's line

**What is paid**: the valuation and the cargo and the prize goods less the **agent's commission**
(`agent_share` 0.05: the prize agents' five per cent, FROM MEMORY, UNVERIFIED) less the court's fees
(`court_fees` £20 a sentence, judgement), plus the **head money** for a ship of war or a privateer
(`head_money_pounds` 5 a head of the men aboard her at the beginning of the engagement, the record's
`men_at_start`: the Regulations ch. IV's certificate, on file; the five pounds the Prize Acts'
figure FROM MEMORY, UNVERIFIED; paid though she was burnt, art. V), **three fourths now and a fourth
reserved** where the prize is purchased for the service (the Flag Officers' art. XXXI, the
Commander in Chief's, on file: a King's ship's prize of war that the yard takes; the fourth comes
with a later sentence of the court,
`court_days` more, as a second job: the owner may turn it off by `purchase_for_the_service:
false`), the whole into the **captor's purse** by `Purse.receive(sum, by="the court", words=...)`
with the account's lines (the valuation, the cargo good by good, the prize goods, the head money,
the agent's and the court's deductions, the shares) as `paper.written` lines of **the prize account**
(a paper of the ship's, 53b's road) and one urgent line of the log, **the purse's line saying so**
("Prize money paid at Falmouth for the Deux-Frères, condemned by the Vice-Admiralty court: the hull
and her stores £620, forty tons of brandy at the market £8,000, her powder and shot £31, the
head money nothing (a merchantman); the agent's commission £433 and the court's fees £20 deducted;
£8,198 paid by the eighths: the captain £3,074, the lieutenants, the master and the captain of
marines £1,025, the warrant officers £1,025, the petty officers £1,025, the people £2,049. The
purse: ...").

**The eighths by date** (`data/business.yaml` `prize_shares:`, a list of schemes each with `from`
and `until` dates and its classes, the one in force at the court's date read; every row FROM
MEMORY and UNVERIFIED, so marked, for the owner to check against a printed Act):

- **until 1808** (the Act of 1708, 6 Anne c. 13, in force in June 1805): the captain **3/8** (one
  of them to the flag officer under whose orders he sails: not modelled, no flag; said), the
  lieutenants, the master and the captain of marines **1/8**, the warrant officers (the surgeon,
  the purser, the boatswain, the gunner, the carpenter, the chaplain, the master's mates, the
  lieutenants of marines: the Regulations Sect. XIII ch. I art. VI, on file, for the marines'
  lieutenants) **1/8**, the midshipmen and the petty officers (the sergeants of marines with them)
  **1/8**, the seamen, the marines and the boys **2/8**;
- **from 1808** (the Order in Council of 1808): the captain **2/8** (a third of them to the flag
  officer), the second class **1/8**, the third **1/8**, the remaining **4/8** by shares among the
  classes below (the midshipmen and the principal petty officers four shares and a half each, the
  able and ordinary seamen, the marines' privates and the rest by the scheme's shares);

the purse is the captain's or the owner's (M5's one purse), so the whole sum is received and the
line says the shares, which is the brief's "the purse's line saying so"; the people's shares as
money in their hands is M8's (the career: half-pay, a reputation; the records keep the sum). **A
privateer's** prize money is the owners' and the crew's by her articles (`privateer: {owners: 0.5,
crew: 0.5}`, FROM MEMORY of the Channel privateers' articles, UNVERIFIED), the whole into her purse
with the line saying so; **France's and Spain's** rows are the British eighths with the row saying
"the French and the Spanish distributions not read; the British scheme kept until a source is",
decision 64's rows present and honest.

**A prize lost on the way home** (retaken, foundered, burnt by her own people) pays nothing (no
sentence, no money), and the log says so when the captor hears it (the lookout's sight of her
colours changed in company; her story's line read by the director's truth; nothing told the captor
that his people cannot know, so a prize parted and lost is known at the port when she does not
come in: judgement, the `prize.lost` line at the court's date when no prize of that name lies in the
port).

## 6. The consent revision for adversarial seats, drafted and not applied (item 6)

**Drafted**: `docs/design/ConsentRevision-AdversarialSeats.md`, the text the brief would say,
in the consent brief's voice and sections (*What an instance would see and do*, *Leaving*, *Being
stopped*, *What is not done*, *The record*), for the three roles: **an enemy captain** (a captain
of a ship at war with a human's ship, who fires into her and may take her), **a prize master over
prisoners** (a captain of a prize whose prisoners include a human's person), **a captor's captain
to a human captive** (who asks his parole, confines him, lands him); what an instance would see
(the human's ship as a sail, his log as hers, his words as a prisoner's lines under his name) and
do (the fight by the same grammar, the possession, the parole asked in its own words); the leaving
words unchanged and restated (the token, `opt_out`, stand down); the sentence of *The record* that
this is "more authority than is described here" and so the question put again; a paragraph for the
owner on what it does not ask (a model to be cruel: the game's rules of war are the period's and the
refusals' words say what the custom allowed). **Nothing under `docs/agents/consent/` or in
`docs/agents/ConsentBrief.md` is touched**; package 55 carries the revision and the re-brief.

**The refusal in words, behind a flag** (`seats.ADVERSARIAL_SEATS_CONSENTED = False`, one flag the
revision's package turns, and nothing else): a seat for a model (`seat:`, the desk's `--station
captain --ship`, the harbour's door) **at the captain's station of a hull adversarial to a human**
is refused with the reason before any station is made or any consent record read: "The consent
brief names no role in which a model fires into a human's ship or takes him prisoner; until it is
revised and the question put again, the game seats no model as the captain of the Renard, an enemy
of the Amazon's. Her rules-based captain and the director's voice serve meanwhile (rule 4)."
**Adversarial** is read from the world at the seating (`prizes.adversarial_seat_why(world, hull,
station)`): the hull's nation at war with the nation of a hull **a human holds** (the player's own
hull, `World.players`, or a hull the player's seat or person is on, `knowledge.players_person`'s
hull), or the hull holding a human's person as a prisoner, or the station a prize master's over a
prize whose prisoners include a human's person; the captain's station only (a passenger's voice
aboard an enemy, a prisoner's voice, a lookout's are not adversarial: they fire into nobody); the
rules captain and the director's `say as` serve every such role. A seat held before the hulls
became adversaries (a French captain seated in peace, then war declared by the news) is **not stood
down** (the brief's promise is about seating; the sample says so in its station notice: "the
Amazon is now an enemy of yours; the consent brief does not yet describe this, and the owner is
told") and the owner is told through the director's log; 55 decides the rest. The suite's seats at
enemy captains, if any, are audited at the step and listed in the postscript (the far hail's two
hulls, the convoy's case study: none is at war with the player's hull by my reading of the tests;
the build checks).

## 7. The court martial, and a new command (item 4; the owner's note)

### 7.1 The court as the director's proceeding

**The court sits** by the director's form `court: sits on <person> for the loss of the <ship> at
<port>` (or `court: sits on the captain of the <ship>`), doubted where he is not ashore at a port of
his own nation (a captive is tried when he comes home: by cartel, by exchange, by the port's agent
landing him at a friendly port; the doubt's words say where he is), refused for a person nobody
lost a ship (no `struck` on his hull's record with him in command): a **place of the port**, "the
court" (`PortPlace` made for the sitting: "the great cabin of the flagship in the harbour, where
the court martial sits; the president and the members, the judge advocate, the witnesses waiting"),
the accused's person moved there (`movement.go` to the place ashore, his harness or the prompt
following: the player at the prompt reads the court's place, 65's shore senses), the court's
**questions in-world through the channel**: the director's `say as the president of the court: "..."`
heard at the place (66's hearing by spot), the accused's `say to the court: ...` (his own words, the
player's or a model's), the witnesses' answers by `say as <his first lieutenant>` or by the rules
(the log's record of the action read by the judge advocate: `court: read the log of the action` a
form that writes the action's lines of his old hull's log as the court's reading, `court.reading`
lines heard at the place, so that the proceeding has the facts without the director inventing
them). **The verdict** is a form `court: the verdict on <person>: acquitted with honour |
acquitted | reprimanded | dismissed the ship | dismissed the service` (the period's sentences for
the loss of a ship, the Articles of War's; a sentence the form does not know is answered honestly),
a **world order journaled** as every form is (`World.world_order`: the inputs, the `world_orders`
record, the director's log; the play log carries the court's **report**, "The sentence of the
court martial is read: Captain Bowen is honourably acquitted of the loss of the Amazon, which was
defended with every exertion against a superior force", a notable line heard at the place and
entered in his person's record and the hull's papers, **nothing shown as sent**, the rule of every
form), the person's **`record`** (a list of dated entries on `Person`: the loss, the verdict, a
prize taken, a wound) the thing the career of M8 remembers, kept in the save and the hull's paper
"the captain's record"; the director decides the sentence as it decides every cause (the brief:
"the director sits as the court"), the limits of the brief read (a `limits:` row for the verdict
where the owner wants the court kind or stern: judgement, the brief's shape).

### 7.2 A new command, as a scenario's start

**`command: a new command for <person>: the <description> "<name>" at <port>`** (the director's
form, or the owner's `world:`, after a verdict that leaves him in the service: refused for a man
dismissed the service, doubted for one dismissed the ship within a year), **writes a scenario
file** by 96's writer (`scenarios.write_scenario`) carrying what the records keep: his name as the
ship's captain (`people:` with his role and his record), **his people who followed him** (the
persons of his old company ashore at the same port, prisoners landed with him or exchanged, whose
`record` has the same loss: the period's followers, a captain's coxswain and his lieutenants going
with him; `people:` entries with their roles), the ship (`ship: {file, ...}` from the description's
file at the port's anchorage, the date the court's day after), the verdict and the loss in `papers:
{record: [...]}` (a paper of the new ship's, "the captain's record", read by `the record` and
carried into the next save), the nation and the war as the news has them (85's), and **nothing of
the old game but the record**; the file written **under the saves' folder** (the game's own
`saves/` as the checkpoints are, never `data/scenarios/`, which is the repository's) and named in
the form's answer ("A new command: the sloop Alert at Plymouth; her scenario is saves/
new-command-alert-1805-07-02.yaml, to be given to either driver with --scenario"), so that **a new
command is a scenario's start** as the brief has it, and the career that remembers (half-pay, the
reputation, the next ship chosen by the record) is **M8's**, the hooks named: `Person.record`, the
paper "the captain's record", the scenario's `papers.record` and `people[].record`, the court's
verdict words as a closed list in `prizes.VERDICTS`.

## 8. The stations, the director, the readings and the truths (items 7 and 8)

**Readings** (the registry's rows, each with its `where` by 65 and its `none_words`): `the prize`
/ `the prizes` (each prize of this ship's: her name, her kind, how taken, the prize master, the
prize crew's count, the prisoners' count and where, her goal, in company or parted and where she
is by the lookout; "no prize"), `the prisoners` (the count aboard this hull, where confined, the
named with their parole, fed at two thirds, in irons; "no prisoners"), `the prize crew` (on a prize:
the men, their fatigue, the hours since possession, the prize master), `the parole` (a captive's
own: asked, given, refused, the liberty it gives; a captor's: each prisoner's), `the prize money`
(the account: paid, pending the court, nothing), `the record` (the person's record: the losses, the
verdicts, the prizes). **The events** (`EVENTS`, for `at` and a stand-by): `she is taken` (`prize.
taken`), `possession taken` (`prize.possessed`, on the prize), `the prisoners rising` (`prize.
rising`), `the prize retaken` (`prize.retaken`), `a prize burnt` (`prize.burnt`), `the parole
asked` (`prize.parole_asked`), `the parole given` (`prize.parole`), `a cartel` (`cartel.sighted`,
the lookout's sight of a flag of truce), `the prisoners landed` (`prize.landed`), `the court
sits` (`court.sits`), `the verdict` (`court.verdict`), `prize money paid` (`prize.paid`), `a far
action heard` (`action.far_heard`). The primer's chapter 11's events table and the `EVENTS` row
stay equal (85's test).

**The forms** after `WORLD_ORDER_FORMS`, each with its doubt and its dry run: `ship "<name>": order
take possession of her` (the hand, as every order of her grammar), `aboard the <captor>: the parole
of <person> given | refused` (§3.2), `cartel: a cartel from <port> for <persons>` (§3.4), `port
<id>: the court condemns | restores the <prize>` (§5.2), `court: sits on <person> for the loss of
the <ship> at <port>`, `court: read the log of the action`, `court: the verdict on <person>:
<verdict>` (§7.1), `command: a new command for <person>: the <description> "<name>" at <port>`
(§7.2), `person: "<name>" is exchanged at <port>` (a captive landed as a prisoner freed at the
port, by cartel or exchange, the plausible cause the director gives: doubted within a day of his
landing). The **truth** (`director.truth`) shows every prize with her captor, her crew and her
prisoners, every hull's prisoners and paroles, every far action in its rounds, the courts pending
and sat. **The harness**: the captive's channel is a visitor's sample (65's filter at his place, the
captive's brief sentence), the prize master's station a captain's on a prize (`shape_words` says
"a prize: ..."; the ship words say whose she was), `all_agents` names a captive's station "Captain
Bowen, a prisoner aboard the Renard, of the Amazon" (82b's visitor naming with the captive's word).

**The truths**, 7-350 to 7-369 (the brief's), each a test beside its code and in `tests/
test_known_truths.py`, 85's rule binding their words; the brief's §20 scenes as this design takes
them:

- **7-350** the far ship's length is her waterline's, and the size term hers: 7-139's record
  re-measured old beside new (the figures of §4.1), the pin's bands holding, the frigates' and the
  cutters' at a cable moved by the round the table says.
- **7-351** a ship struck near is possessed by `take possession of her`: the boat's quarter of an
  hour, the prize crew out of the captor's muster (the captor's bill short by them), the prize
  master the ladder's man at her captain's station, her people prisoners below and her master in
  the cabin on his parole, her colours the captor's over hers, her nation and role and intent new,
  her hull asleep whole when she parts and awake again under the cap; refused in its five ways.
- **7-352** (§20's first truth, the boats' retaking amended with the reason: §2.8) a merchant brig
  taken by a privateer schooner at far detail sails for Bayonne under a prize crew of eight with her
  master a prisoner in the cabin, in company and then parted by the privateer's doctrine, and is
  retaken by a cruiser coming up at sea when the prize crew is thin and tired (72's rule from the
  prize's side; her nation, colours and company hers again; the prize master her prisoner).
- **7-353** the prisoners rising: the same prize with a prize crew of eight over fifteen, tired, no
  captor within two miles, rises in the night at seed 7 and retakes her (or is put down and in
  irons at another seed, both pinned), the captor in company seeing her colours change by his
  lookout; a prize crew of twenty over fifteen never rises.
- **7-354** a prize not worth manning is burnt by the doctrine: her people taken aboard as prisoners
  fed at two thirds, her powder and shot into the captor's magazine as prize goods (86's road), the
  glow seen by night by another lookout, nothing paid but the head money for a privateer.
- **7-355** the player struck is a person aboard the captor: possession taken by her rules captain,
  his own station stood down "taken in the prize", the drivers following his person, `where am I`,
  `the ship` and the station line hers, his readings the cabin's by 65's table, `say to the
  captain` heard, his journal going on, every order of her deck and of his old ship's refused in
  words naming his state.
- **7-356** (§20's third truth) the player struck to a ship whose captain a model holds (the test's
  fake door, seated before the war's declaration by the news: §6's rule) is asked for his parole in
  the model's words and answers in his own, the exchange in both logs, the parole read from his
  words and his liberty given, and nowhere in any sample's operator voice (the fake door's
  transcript read).
- **7-357** the captor's rules captain by doctrine: the sword returned, the parole asked and taken
  by rule after a watch, the course for his port, the prisoners landed to the agent for prisoners at
  the port's place, the captive ashore there with the shore's senses; a cartel sent by the director's
  form fetches him and lands him at his own port.
- **7-358** two far ships that meet in anger beyond the range (the first action's two cutters set
  off the horizon with no player's ship near) resolve their action by the rounds asleep at seed 7:
  the engaging transition on the far body, the rounds in both stories and the sleeping hull's log,
  the damage summed into the far state, the colours struck by morale, possession taken at hail and
  the prize carried for Falmouth; the same seed the same record.
- **7-359** the near fight and the far fight of 7-140's two cutters at a cable end within a round of
  each other (the figure found pinned, whatever it is, with its reason).
- **7-360** the far state into the near body and back: a hull made for a vessel with a far record
  carries the record's dead, wounded, dismounted guns, shot holes (the well makes water from the
  ones below), cut sails and spars gone as state; slept again, her record is the same sum.
- **7-361** (pace, informative; the floors not lowered) truth 51's form with two far ships in anger
  beyond the range beside the frigate, and the engagement first among the cap's reasons: two far
  ships that meet in anger within the range are woken together under the cap's order and the near
  action takes over.
- **7-362** (§20's second truth) the prize money paid at Falmouth by the eighths: the merchant brig
  condemned by the court's job after its days, the hull's valuation, the cargo at the market (the
  supply moved), the prize goods, the agent's commission and the court's fees, the purse's line
  saying the shares under the scheme in force at the date (1805's), and the prize account paper;
  a privateer's by her articles; a frigate's by 1808's when the date is after.
- **7-363** a neutral taken wrongly is restored with costs against the captor, said why; a prize
  lost on the way home pays nothing and the court's day says so; head money alone for a privateer
  burnt.
- **7-364** (§20's court) the court martial as the director's proceeding: the captive landed and
  exchanged, the court sat at the port's place by the form, its questions through `say as the
  president` heard at the place and answered by `say to the court`, the log of the action read by
  the judge advocate, the verdict a world order journaled in the inputs and the director's log, the
  play log carrying the sentence read and never the order, his record keeping it.
- **7-365** a new command started from the verdict: the scenario file written under the saves with
  his name, his followers and the record, loaded by the loader and begun; the record paper read
  aboard the new ship.
- **7-366** the adversarial seat refused in words behind the flag (a `seat:` and a door's station at
  the captain of a hull at war with the player's, and at a prize master's over the player's person);
  the rules captain and the director's voice serve; the flag turned, the seat admitted (the test
  turns it and turns it back); a prisoner's voice and a passenger's aboard an enemy admitted.
- **7-367** the readings, the events and the forms: every new form performs in the dry run and in
  play with its doubt; the truth shows every prize, her crew and her prisoners.
- **7-368** a passage with a prize taken near, the captive aboard the captor and the parole
  exchanged replays by both roads to the same digests of every hull's log (84's acceptance form);
  a far fight's passage the same.
- **7-369** the cut-out carried from hailing distance to its end by the rounds: the packet that
  fights is fired on by the privateer's rounds and strikes by morale, where the merchantman yields
  by 72's rule as before (7-153's convoy words unchanged).

**The scenarios** (`data/scenarios/`): `prize-home.yaml` (the prize's passage home: the player's
frigate with a French brig in company as her prize under a prize master, bound for Falmouth, the
business on) and `captive.yaml` (the captive aboard the captor: the player's person a prisoner on
parole aboard a French frigate bound for Brest, his own ship a prize astern, the director's starter
brief `captive.yaml` with its causes: a gale, a cartel, a cruiser at dawn), each loaded and begun
in the fast tier and recorded in the tuning notes.

**The records**: spec M7 §11a, §18 to §20 and §29 "as built" paragraphs; `docs/agents/Harness.md`
§21i (the captive's channel, the prize master's station, the forms); the primer's **chapter 27, "A
prize taken, and striking"** (in-world under 85's rule, through `tests/test_in_world.py`: the
possession and the prize crew, the prisoners and the parole, the prize's passage and her court, the
money, striking and what follows for the captain who strikes, the court martial and a new command),
with the forms tables of chapter 20's (the director's) brought up; the director's library (the
world page's forms); `docs/dev/TuningNotes.md` "## Package 74" (this design's pointer, each item,
the figures and their sources, the far fight's agreement, what moved and its proof, the pins old
beside new, found on the way, decisions, the suites as run); `docs/dev/PrimerRedactions.md` for
what the chapter leaves out.

## 9. The edge cases, each decided

- **The player's ship taken while a model holds a lesser station of hers** (his officer, his
  master): stood down "taken in the prize" by the handover's rule (§2.2); a model at a prisoner's
  voice afterwards is the director's seat (§3.5).
- **The captor far when the player strikes**: the far body closes to hail by `taking possession`
  and possesses there; her hull is made for the captive (§3.1, the cap's first rank); a far body
  with no brain (a convoy's merchantman under orders) takes no possession.
- **The player strikes to nobody** (no enemy within a mile, his word alone): the colours down, the
  battery held, nothing follows until an enemy takes possession; `hoist the colours` after a glass
  with no captor is the player's own again, said (a ship that struck and was not taken rehoisted;
  the period did it with the prize gone: judgement).
- **Two prizes**: each a hull or a far record of her own, the set's `prizes` naming both, the
  captor's prize crews drawn twice from a thinner muster (the doctrine's `prize_crew_share` of what
  is left; a captor under `fit_least` mans no more and burns or leaves the second).
- **The captor sunk or retaken with a prize in company**: her set dissolves (72's rule for a
  commander lost), the prize keeps her intent (`carry the prize to <port>`), her prize master
  commanding; a prize whose captor is taken by the enemy the prize crew's old nation is retaken by
  the same cruiser only by coming alongside her (72's rule).
- **A prize's prisoners' needs**: fed at two thirds (§2.9); the named few's needs as persons; a
  prize whose stores fail starves prisoners and prize crew alike by the needs' rule (said in the
  reading).
- **A model-held prize master**: the adversarial refusal where the prisoners include a human's
  person (§6); otherwise his seat is a captain's on a prize, admitted, the brief head saying so.
- **The prize's papers and the private table of the month**: §2.5; a table of a past month captured
  is nothing (the month's changes), said.
- **A far prize made a hull**: §2.6, the muster cut, the prize master drawn or made from words.
- **The save and the replay**: every move is a consequence of an input (the strike, `take
  possession`, the parole's `say to`), a job (the boat's, the court's), a rule (the rising's draw
  from the hull's stream `prize`, the far round's from the World's `far`) or a form; the record
  fields (`Vessel.prize`, `Prisoners`, `Person.confined_to`, `Person.record`, the far `damage`'s
  new keys) are carried by the checkpoint (`Vessel.to_dict` and the hulls' blocks) and read as
  empty from a checkpoint of before; a save mid-possession (the boat on her way with the prize crew)
  replays by both roads (the jobs are the dealings', 82's road).
- **The pace**: §4.6; the rising's and the court's rules are a minute's reads; the far rounds a
  pair's every three minutes.
- **The hull's façade** (97): everything here reads a hull's own fields through her handle and the
  World's shared things through `hulls.world_of`; the prize record is the vessel's (shared), the
  prisoners the hull's.
- **The captive and the far shape**: a captor's hull put to sleep with the player's person aboard
  cannot be (the followed hull is held awake: 84's rule; the player's person's hull is followed by
  decision 62); a captive's model-held voice on a hull that sleeps samples the far shape as 82b's
  far hull does.
- **Striking in a squadron**: a member struck leaves the set (`Squadron.leave`, "struck"); the
  commodore's book signals nothing new (the signal "enemy struck" is the book's where it has it).
- **The outlaw** (71's pirate): a pirate taken is condemned whatever her nation (§5.2) and her
  people are "carefully confined" (the Regulations' art. III), no parole asked; the player who fired
  under false colours and is taken is tried as a pirate by the court of §7 (the director's verdict
  words gain `hanged`? No: the form answers honestly that the court of a pirate is not the game's,
  and the record says "taken as a pirate"; judgement, 80's or M8's).

## 10. What was rejected, and why

- **A flag on one muster for the prisoners** (§2.2): every reader of the muster would learn a state
  that is neither hurt nor sick; the swap gives the bill's own arithmetic for a thin prize crew.
- **The prize crew as persons only** (no sailors moved): the prize must sail by the bill, and the
  bill is the muster's.
- **Waking two sleeping hulls far from the player for their fight**: the owner's decision 8 as 83
  recommended it; the rounds are rule 5's answer and cost nothing a tick.
- **A separate far-fight clock or queue**: the rounds run in the sea's minute at the far step's
  cadence (every third minute), which is 70's measure in the world.
- **The prize money by a flat figure or a dice**: the valuation, the cargo and the head money are
  each a function of state the game has, which 60 takes up for buying and selling.
- **The court as a dialogue tree**: the director's channel and `say as`/`say to` are the proceeding,
  and the verdict a form; the game owns the facts (the log read) and the director the questions.
- **The cartel's words and places** (the exchange ashore, the agent's business): 80's.
- **A new consent file or an edit to the brief**: forbidden; the draft under `docs/design/` and the
  flag's refusal are the whole of item 6.
- **Standing the player's own station bound to him as a captive** (82's other reading): a bound
  station says he commands; he does not; his prompt follows his body instead.
- **The retaking by boats at anchor** (§20's words): 63's boat and 77's cutting out; the cruiser at
  sea takes the truth's place with the reason.
- **Modelling the sentry, the irons as men, the hold's ventilation**: words in the refusals and the
  reading, nothing in the state beyond `in irons`.
- **A prize awake at all times**: the cap's rule (84's) stands; a prize is a hull like any other.

## 11. The order of the steps, each a mergeable state

Each step one commit or a few on the package's branch with the trunk brought in at the boundary before
the step's final runs in a worktree pinned at the commit measured (the fast tier whole, the slow
tier of the touched files and the known truths, the pace tests alone and last; ruff clean), its
postscript below and its section in the tuning notes, reported to the lead at its boundary.

0. **This note**, pushed and reported before the engine is touched; the lead's rulings on §12.
1. **75's finding** (§4.1): the one read in `combat/far.py`, `round_once` factored out of `fight`
   (the same loop, the same record), truth 7-139's docstring and the tuning notes' row re-measured
   old beside new, truth 7-350; nothing else touched.
2. **The prize possessed near, the prize master and 97's leader-on, the prisoners, the rising, the
   retaking and the burning** (§2): `world/prizes.py` new, `movement.put_aboard`'s `station=`,
   `boarding.party_leader` and 97's pin moved, `Vessel.prize`, `Prisoners`, `remuster`, the role
   `prize-master` and its file, the captors' thresholds and the state `taking possession`, the
   orders (`take possession of her`, `take the prisoners aboard`, `burn the prize`, `scuttle her`,
   `take her powder and shot`), the captured book, the readings `the prize`, `the prisoners`, `the
   prize crew`; truths 7-351 to 7-354, 7-325 and 97's test re-pinned.
3. **The captive's channel** (§3): the player struck and possessed, the stand-down, the drivers
   following, the parole and its words table by nation, the confinement by 65's hook, the captor's
   doctrine after the taking, the prisoners landed to the agent's place, the cartel's description and
   form, the captive's brief sentence, the readings `the parole`; truths 7-355 to 7-357.
4. **The far fight wired** (§4): `combat/far_action.py`, the far engaging, the rounds, the state
   into the parts and back, the cap's reason, the guns heard, the toggled measure of the pinned
   passages with two far ships in anger (old beside new, the pair and the round named), the
   agreement; truths 7-358 to 7-361 and 7-369.
5. **The prize court and the money** (§5): the valuation, the court's job by nation, the sentences,
   the eighths by date, the head money, the prize goods on 86's ordnance, the purse's line and the
   prize account, the director's `port` form; truths 7-362 and 7-363.
6. **The court martial, the new command, and the consent revision drafted with its refusal** (§6,
   §7): `Person.record`, the court's place and forms, the verdict journaled, the scenario written
   under the saves, `ConsentRevision-AdversarialSeats.md`, the flag and the refusal, the suite's
   seats audited; truths 7-364 to 7-366.
7. **The records and the last truths** (§8): the scenarios `prize-home.yaml` and `captive.yaml`
   with a starter brief, the forms' dry run, the replay truths, spec §11a, §18 to §20 and §29 as
   built, Harness §21i, the primer's chapter 27 through `test_in_world.py`, the library's forms
   tables, the tuning notes whole, these postscripts; truths 7-367 and 7-368.

Spain (decision 64) in every table of this note: the parole's words, the agent for prisoners'
place, the court's name and days, the shares' rows.

## 12. Open for the lead

1. **The muster swap** (§2.2) over a flag on one muster: the design's reasons, and the keepers'
   audit as the step's first job; the lead's word if the trunk's keepers make the flag cheaper.
2. **The captive's own station stood down** (§3.1), not standing bound: the design's reading of the
   brief's "or".
3. **The 1805 scheme of the eighths** (6 Anne c. 13) for a game in June 1805, with 1808's beside it
   by date, every row FROM MEMORY and marked: the lead's or the owner's check against a printed Act
   before the figures are trusted; the game's purse takes the whole and the line says the shares.
4. **The far ship's reply to an awake hull** by a synthetic gun of her fit (§4.3): the least that
   makes a far-against-awake fight two-sided; the alternative is to wake her always (the cap's
   first rank does within the range; beyond it the awake hull fires at a mark that cannot answer, as
   70 left it). The design takes the synthetic reply within her guns' reach; the lead may prefer 70's
   silence until the wake.
5. **The guns heard off the horizon** (§4.5): a line of the player's log once a round within the
   sound's reach; a judgement the lead may strike as noise.
6. **The new command's scenario written under `saves/`** (§7.2), never under `data/`: the lead's
   word on the folder and the name.
7. **The retaking by boats at anchor** amended to a cruiser at sea (§2.8): the truth's words as the
   brief allows, with the reason; 77 takes the boats.
8. **The adversarial rule's reach** (§6): the captain's station of a hull at war with a hull a human
   holds, or holding a human's person; a seat held before the war is not stood down. The lead's
   word on whether a model seated at an enemy's *officer of the watch* (who may give the deck's
   orders under a rules captain who fires) is adversarial too; the design says no (the captain
   fires), and lists the suite's seats at the step.
9. **The one touch outside my files**: `combat/boarding.py` (73's and 97's, named in the brief as
   the ground for the leader-on) and `world/crews.py`'s `rank` and `make_hull` (84's, no package's
   by the brief; 82b touched the same function); nothing of 75's files (`data/ships/*.yaml` only
   for the cartel's fit through `tools/gen_ships.py` with its source, which is 75's road: **the lead
   rules** whether the merchant brig's file may gain the fit now or the cartel sails with the
   merchant's fit and the one gun is words until 75 closes; the design takes the words).

## As built (the postscripts, step by step)

### Step 0: the lead's rulings on §12 (2026-11-07)

The note read whole and approved as the design, with these rulings, each taken into the steps:
(1) the muster swap as designed, the keepers' audit the step's first job, a report before building
further if the caches are more than a handful or one cannot be re-pointed; (2) the captive's own
station stood down, as designed; (3) the 1805 scheme of the eighths with 1808's beside it, the head
money, the hull's price a ton, the agent's share, the court's days and the salvage eighth all FROM
MEMORY and marked, built so and not waited on; the lead puts the figures to the owner's references
and cited figures come back by the same road, the data rows then moved old beside new; (4) the far
ship's reply to an awake hull by a gun of her fit is the **fallback only** when the cap has no room
to wake her (three held hulls), never the ordinary case within the range, said in the round's data
and measured for how often it fires in the pinned passages (expected rarely or never); beyond her
guns' reach nothing fires; (5) the guns heard off the horizon kept as a sound of the lookout's
rule under the same toggle as the rounds, the reach and the night flashes' range judgement named
in the notes; (6) the new command's scenario under the game's `saves/`, never `data/`, with **one
correction**: package 96 is held by the owner to the end of the milestone, so no writer of its
exists; a small writer of this package's in `scenarios.py` emits exactly the keys the loader reads
(the ship, the people with their roles and records, the papers' record, the date, the nation and
the war), tested by loading it back, 96 taking it up later (the hook named in step 6's postscript);
(7) the boats' retaking amended to a cruiser at sea, as designed; (8) the adversarial rule's reach
**wider than the captain alone**: any station of an adversarial hull that may give an order of her
deck or her guns (her captain, her officer of the watch, the warrant stations when 87 makes them)
refused behind the same flag with the same reason while she is adversarial; the voices that give
no order (a passenger's, a prisoner's) and the lookout's admitted; a seat held before the war not
stood down and the owner told; the suite's seats listed at the step; (9) the touches to
`combat/boarding.py` and `world/crews.py`'s `rank` and `make_hull` granted; the cartel's one gun
stays words and the merchant's fit until package 75 closes, nothing of `data/ships/` meanwhile.
Noted and accepted without change: §2.1's colours over hers for a day, §2.3's one ladder, §2.8's
figures as judgement, §4.1's table, §4.6's agreement pinned at the figure found, §5.2's court by
nation with Spain's row, §6's draft under `docs/design/`, §9's outlaw left honest, decision 64 in
every table.

### Step 1: the far ship's length (§4.1; 2026-11-07)

**Built as designed**: the one read (`length_waterline_m`) in `far_ship`; `fight`'s loop body
factored into `round_once`, the function step 4's far action runs, the loop and its record
unchanged; truth 7-139's docstring brought to the new read with the old figures beside it; truth
7-350 pinning the read, the move old beside new (the old read set by hand as the toggle) and that
`round_once`'s record is the measure's own. The figures are §4.1's table, confirmed on the step's
tree (`docs/dev/TuningNotes.md`, "Package 74", step 1). **Taken another way**: nothing. **Found on
the way**: nothing.

### Step 2: the prize as a hull of the one world (§2; 2026-11-07)

**Built as designed**: §2.1 to §2.9 whole (`world/prizes.py`, `orders/prize.py`,
`api/prize_readings.py`, the role files' thresholds, `data/captains/prize-master.yaml`, the hail
table's rows, the four verbs, the three readings and the seven events, the primer's chapter 27 in
its first form); truths 7-351 to 7-354; 7-181, 7-325, 97's test and 72's cut-out re-pinned with
the reasons (the table in `docs/dev/TuningNotes.md`, "Package 74", step 2). The keepers' audit
(ruling 1): two keepers cache the muster (the routine and the quarter bill), both re-pointed by
`remuster`; none could not be. **Taken another way**: possession at once when the order is given
within a boat's pull, the boat's quarter of an hour left to the errand when step 3 moves persons by
the same boat; the privateer parts from her prize by his doctrine, so 72's cut-out no longer joins
his company (the Channel privateers' habit, from memory); the player's own ship struck is not
possessed until step 3 (the rules captain lies by her); the doctrine's own burning waits for the
court's valuation (step 5); the replay by both roads with a prize is step 4's passage (the strike
by the test's hand is no recorded act), the checkpoint round trip pinned here. **Found on the
way**: the prize rules ran on defaults for a player's captain with no role (`_doctrine` now answers
the hull's service's file); a rehomed person of a post the new company has already (`Registry.
rehome` gives him his old home's id after a colon); the world order's "merchant brig" is
`brig.yaml`'s muster of 121 (75's file, noted for the lead); the parser's `take <n> of the
prisoners aboard`; the orders' road doubling a function's line (`said`).

### Step 3: the captive's channel (§3; 2026-11-07)

**Built as designed**: §3.1 to §3.5 (`world/captive.py` and its hooks; the design's roads for
the player struck near, by a model's hand and by the far body made a hull; the parole asked by
doctrine in the hail table's words by nation with Spain's row, answered in the captive's own
words, by rule after a watch; the places and the sword; the prisoners landed to the port's agent
with its name by nation; the cartel under a flag of truce; the director's two forms and their
doubts); truths 7-355 to 7-357; the primer's chapter 27 extended. **Taken another way**: the
captive's officers stay confined in the prize (the `divide_prisoners` rule is the counts'); the
cartel keeps her persons on her record and sets them ashore at her port's quay (80's words fill
her out); the prisoners' victualling is not modelled; a model seated as the captive is served by
82's voice station until step 6's seats pass, the captive's brief sentence with it. **Found on
the way**: the far brain forgot a struck mark's nation (she shows no colours) and never saw
`enemy struck`; the privateer's `chasing` rows had him evade a frigate that had struck to him as
a superior force and a man of war (both judgements now pass a struck ship by); a rules captain
bound for Brest from the Iroise lays no course through the goulet and beats without way (the
chart's and the planner's, noted for the lead); the far brain dropped its mark on entering
`taking possession`; the captive's person was read as every hull's captain (he is the followed
prompt's alone); a far vessel whose plan runs out is gone from the sea at the minute's end, so the
cartel's minute keeps her until her persons are landed. The figures and the pins are in
`docs/dev/TuningNotes.md`, "Package 74", step 3.

**The step's mends from the owner's play (2026-11-09, landed with step 4).** Five defects found
by the lead's replay of the owner's strike save, each reproduced in the step's scene, mended and
tested: (1) a captive's words were taken for the player's hand on his captor's captain, who
stood aside and left her with nobody commanding (the hand is one of her own free company's
alone: `movement.hand_on_her`); (2) a captor she had fired on before she struck engaged his own
prize a minute after the possession (his own prize, and any of his nation's, is no enemy:
`Judgement._prize_of_ours`; the taking clears her from what he knew her an enemy by); (3) a bare
yes or no to the open question was not read (read now as whole words, §3.2's list beside); (4) a
prisoner's hail was made from his captor's deck (§3.1 said "his orders of any deck refused"; the
orders read before the vocabulary's were not: a captive's prompt performs a word said, asked or
told, a reading, his moves within his parole, his needs and a free line, and nothing else), and
a prize's answer to a hail named whoever stood at the hailing prompt (her captor's ship and her
prize master now, from her record); (5) his going ashore met the free man's refusal (his own
words now). The measures old beside new are in the notes, "Step 3's mends from the owner's play".

### Step 4: the far fight on the sleeping hulls (§4; 2026-11-07)

**Built as designed**: §4.2 to §4.6 (`combat/far_action.py`: the far engaging by the role
files' rows, one round of `far.round_once` every three minutes for a pair in anger within gun's
reach, each side's record carried in and written back, the draws from the World's `far` stream
opened at the first round; the strike by morale as the cut-out writes it and the far possession
after; the guns heard at the player's ship within twelve miles, the flashes to fifteen by night;
the far ship's reply to an awake hull as the fallback where the cap has no room; the engagement
first among the cap's reasons; the toggle `ENABLED`; the far record into the parts at `make_hull`
and `_to_full`); truths 7-358 to 7-361 and 7-369; the primer's chapter 27 "An action off the
horizon". **Taken another way**: the flashes' fifteen miles by night are a judgement (§4.4 gave
the guns' twelve alone); the agreement (§4.6) is pinned as found and not tuned: the near fight of
7-140's two cutters at a cable ends thirty-five seconds after the first shot where the design
measured three minutes from a docstring's band, and the far rounds of the same pair end in two
rounds (six minutes), within two rounds and not one, the far fight unable to end before its first
round at 180 s and the coarser by design (rule 5). **Found on the way**: the far brain forgot its
mark on entering `engaging` as it had on `taking possession`; the schooner's and the lugger's files
give no armament (75's), so the packet's cut-out is a cutter's against a brig-sloop privateer; the
"merchant brig" of the brig's one file carried the brig-sloop's eighteen guns (75's; mended by its
SW-4, merged at step 2's boundary: her own file, sixteen men and four long 6s). The figures, the pins moved by the wiring measured with the toggle (the passages 7-152,
7-153, 7-154, 7-159, 7-160) and `FALLBACK_COUNT` are in `docs/dev/TuningNotes.md`, "Package 74",
step 4.

**The pace mended at the resumption (2026-11-09).** The far fight read each side's ship file
from disk at every minute of a far brain (`has_guns`) and again at every round (`far_ship_of`),
which took truth 7-159 under its floor (175 ticks a second against 500) and would have taken
7-361 under its own had it ever run: it stood on a world with no place on the chart. The file's
figures are read once a file and fit (`far.file_figures`); 7-361 stands on the frigate of the
brains' sea. No figure of the fight moved; the toggle's measures are in the notes, step 4.

### Step 5: the prize court and the money (§5; 2026-11-07)

**Built as designed**: §5.1 to §5.3 (`world/prize_court.py` and `data/business.yaml`'s four
blocks; the valuation by the rows over the files' figures, the cargo at the port's market, the
prize goods on 86's ordnance, the court by the port's nation sitting in its days as a port job on
the prize hull's dealings or on a far prize's record in her goal's road, the three sentences by the
rules with the wars' dates, the head money, the agent's five per cent and the court's fees, the
reserved fourth of a King's ship's prize of war, the money by the eighths of the scheme in force
at the court's date into the purse with the purse's line and the prize account's lines, the
director's `port <id>: the court condemns | restores the <prize>` doubted against the rule, the
reading `the prize money`, three events); truths 7-362 and 7-363; the primer's chapter 27 "The
court and the money". **The lead's ruling of 2026-11-07 on §5.3** (Lavery, Nelson's Navy, p. 116,
from the owner's shelf): the two British schemes are CONFIRMED and cited in the rows (the book's
words not in the tree), the flag officer's share named as not modelled; the head money, the agent's
commission, the hull's price a ton, the court's days, the costs and the salvage eighth stay FROM
MEMORY, marked. **Added by the ruling** (the design lacked it): the prize money is **shared among
every ship in sight at the moment the enemy struck**, a ship that took no part included, written
on the record at the strike (`in_sight`, the ships at war with her in sight from her masthead, with
their complements, by the near action's, the far rounds' and the cut-out's strike hooks) and
divided before the eighths by their complements (the division a judgement, FROM MEMORY: Lavery
gives the sharing), each ship's part into her purse by her own road, the purse's line saying
"shared with the Sprightly, in sight at the strike: the Amazon's part £..."; truth 7-362 has a
King's cutter in sight. **Taken another way**: her stores price nothing (her file lists none);
`take her powder and shot` is not built (the goods are the court's); the `prize.lost` line at the
court's date for a prize that does not come in is not written (nothing told the captor that his
people cannot know); the reserved fourth is paid by the record's day from the prize's minute, not a
second port job; the salvage is paid to the recaptors alone by their nation's court and scheme, the
enemy's consorts in sight at the first strike sharing nothing of it. The figures and the finds are
in `docs/dev/TuningNotes.md`, "Package 74", step 5.

### Step 6: the court martial, a new command, and the consent revision drafted (§6, §7; 2026-11-07)

**Built as designed**: §7.1 and §7.2 (`world/court.py`: the court sat by the form at a place of
the port made for the sitting, the accused before it, the president and the judge advocate found
there; the questions through `say as` heard at the place; the accused's own `say to the court:
...`; the log of the action read by the judge advocate; the verdict one of `VERDICTS`, a world
order journaled as every form is, the play log carrying the sentence read and never the order;
`Person.record` kept in the save, read as `the record`; the copy of it he carries into a new
command **a thing with words** in his keeping (package 100's letter, made by the scenario's
`things:`; the lead's word of 2026-11-10: a paper given to an officer is a thing with words by
that road and no kind of its own), where the design had a paper of the ship's, "the captain's
record", so that no ship's papers move;
`command: a new command for <person>: the <description> "<name>" at <port>` writing a scenario
under the saves by 96's writer with his name, his followers and the record, the hooks named for
M8), §6 (`docs/design/ConsentRevision-AdversarialSeats.md`, the text in the brief's voice and
sections for the three roles, with a paragraph for the owner; the flag `seats.ADVERSARIAL_SEATS_
CONSENTED` and the refusal in words at the director's seat and the desk's door, adversarial read
from the world at the seating, the captain's station alone; nothing under `docs/agents/consent/`
or in `docs/agents/ConsentBrief.md` touched; the suite's seats audited: none adversarial); truths
7-364 to 7-366; the primer's chapter 27 "The court martial, and a new command"; the forms in the
director's table and chapter 20. **Taken another way**: the accused speaks through a verb of the
prize orders (the court is no station); the court's officers are persons of the sitting, gone at
the verdict; the brief's `limits:` row for the verdict is not built; the exchange is a `person:`
form of its own (`is exchanged at <port>`), doubted within a day of his landing; a scenario may
name the player's ship (`ship.name`, honoured by the loader, nothing recorded moved). **Found on
the way**: the player's own ship's captain is her prize master after the taking, so the freed
player's prompt wanted a memory of who he is (`captive.PLAYERS_PERSON_KEY`); his nation for the
court is his lost ship's, not his prize's colours; the dry run of a form that writes a file wrote
it (the copy is marked, the form says what it would write). The figures and the finds are in
`docs/dev/TuningNotes.md`, "Package 74", step 6.
