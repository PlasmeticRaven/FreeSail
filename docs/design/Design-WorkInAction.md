# Design note: the quarter bill, and work in action (package 70, item 1)

Written before anything of package 70 was built (the brief's rule: "the design of item 1
comes first and is written down before it is built, because every other item hangs from
it"). Spec M7 §8a and rule 7 ("nothing pre-defines a battle's timing"), rule 2 ("a gun is
served by the bill") and rule 6 ("realism, not pacing") bind. The lead's reading was that
the helm's `full and by` is the shape, the quarter bill the scheduler and the evolutions
its leaves; this note takes most of that reading and departs from it in one place, said
below with the reason.

## What the engine has, and what an action asks of it

The ship's company today is a watch bill (`freesail/crew/bill.py`): who is on deck is a
pure function of the clock and a few flags (all hands called, a hand turned up, a hand at
work). Work is an evolution (`freesail/evolutions/runner.py`): one instance with a step
list or a script, which asks the hands its file names from the hands on deck, fit and idle,
holds them until it ends, runs its steps at a pace stretched by the weather factor and the
crew factor (numbers, rating, fatigue, the roll), and is serialised against other work by
the parts it holds. Two things in that shape do not fit an action:

1. **An evolution ends.** A gun's service does not: loaded, run out, primed, pointed and
   fired, it begins again, and goes on while there are hands at it, powder in the magazine
   and an enemy to bear on. Queuing a `load` behind a `fire` behind a `run out` for each of
   twenty-six guns, every minute and a half, through a runner whose unit is an order given
   once, would make the log a queue and the player wonder how his orders stack, which is
   what rule 7 forbids.
2. **A hand has one station at a time.** The watch bill's pool is "on deck and idle"; a tack
   takes the whole deck. At quarters every man is already somewhere (a gun, the braces, the
   magazine hatch, the cockpit), and a tack must take its hands *from* those places by a
   rule, say where it took them, and give them back when it is done.

## The design in one paragraph

At quarters the company is ruled by a **quarter bill** beside the watch bill: data in the
ship file (through the generator, each figure with its source) that says, for her fit of
guns, how the divisions are made up (the gun crews by gun pair, the sail trimmers, the
powder, the helm, the marines, the carpenter's crew, the surgeon's), and a runtime
(`freesail/crew/quarters.py`) that assigns each man his quarters station once at the
beat to quarters, deterministically from the muster, and keeps him there. **A gun's
service is a cycle, not an evolution**: a small state machine per gun
(`freesail/combat/guns.py`) stepped every tick by the runner's step beside the helm's
`full and by`, whose steps (sponge, load, ram, run out, prime, point, fire) have nominal
times by the gun's kind and calibre and run at the pace the crew factor gives the hands at
that gun, so the rate of fire falls out of the muster (rule 2) and nothing of a battle's
timing is written anywhere but in the hands, the powder and the sea (rule 7). What the
player gives are **standing intentions** the divisions keep (`engage her to starboard`,
`load with round shot`, `aim at her rigging`, `fire as they bear`) and the few **one-shot
orders** that ride over them (`fire the starboard broadside`, `fire No. 3 gun`, `fire a shot
across her bows`, `cease firing`); the intentions are logged when they change something, as
the helm's are, and the cycle's own doings are one line a minute per battery, never a
line a gun. **Sail work in action is the evolutions as they are**: an order for the braces
or a tack asks the runner for hands exactly as now; the pool it draws on at quarters is the
sail trimmers' division (idle by design), and when that is short the **fighting book's
priority** decides whether the guns are robbed (`sail before guns`: hands are taken from
the gun crews, the disengaged battery first and the engaged by number from the one that
bears least, the gun's cycle slowing or stopping, the log saying from where) or the sail
work waits short-handed (`guns before sail`); and hands whose sail work ends go back to
their quarters station by themselves at the next tick. Clearing for action and beating to
quarters are ordinary evolutions (all hands, a duration from the sources) that end by
putting her under the quarter bill; `secure the guns` and `pipe down` put her back under
the watch bill.

## The pieces

### The quarter bill (data)

In the ship file, under `armament:` (because the gun crews depend on the fit) and
`crew.quarter_bill:` (the rest), written by `tools/gen_ships.py` with a source beside each
figure:

- **the gun crews**: one crew per *pair* of broadside guns (the starboard and the larboard
  gun of a number share a crew, the period's practice: Lavery, *Arming and Fitting*, the
  quarter bill; the Regulations' "the men quartered at the guns"), so many men by the
  gun's weight (Douglas, *Treatise*, 1820, the exercise of the great guns: a man to every
  five hundredweight or thereabouts of the gun, with a powder boy to each gun or pair);
  a chaser and a swivel their own small crews;
- **the sail trimmers**: the topmen of each top who leave the guns for a brace, a sail or
  the lead; the afterguard at the main sheet and the braces aft; the forecastlemen at the
  head sails: counts per station, Luce 1884 ch. XX ('Watch, Quarter and Station Bills')
  for the shape, judgement for the numbers against the file's stations;
- **the helm**: two quartermasters at the wheel (a cutter one at the tiller);
- **the powder**: the boys and the landsmen who pass cartridges from the magazine;
- **the marines**: all, at the poop and the gangways (their fire is 73's; here they are a
  division that may be robbed for the braces last of all);
- **the carpenter's crew**: at the wings and the pumps (idlers of that trade);
- **the surgeon's**: the surgeon's mates in the cockpit (idlers of that trade);
- **the idlers otherwise** (the cook, the stewards, the servants): to the powder and
  the braces;
- **the officers**: the quarterdeck, never hands.

The generator reckons the gun crews from the fit and the rest from the stations, and the
loader checks that the bill does not want more men than the muster has (a short company
mans fewer guns of each battery, the after guns first: the bill says which stand idle).

### The quarter bill (runtime): `freesail/crew/quarters.py`

`Quarters` on `ship.extra["quarters"]`: `at_quarters` (bool), each sailor's quarters
station (`Sailor.quarters`: `"gun:3"` for the crew of the No. 3 pair, `"trimmers"`,
`"helm"`, `"powder"`, `"marines"`, `"carpenter"`, `"surgeon"`), assigned at the beat to
quarters from the muster in id order within each station's preference (the forecastlemen
to the forward guns, the waisters to the midship guns, the afterguard to the after guns and
the quarterdeck carronades, the topmen to the trimmers first; Luce 1884 ch. XX), so that
the same muster gives the same bill.

**The watch bill at quarters.** `bill.on_deck` returns every fit hand (as all hands
called), and the routine's watch changes send nobody below while she is at quarters.
`hands.request` is unchanged: it takes from the hands on deck whose `at` is None. At
quarters a gun crew's hands carry `at = "gun:3"` while they serve the gun, so a sail
evolution finds the trimmers idle and the guns busy, as the period had it.

**Robbing.** `Runner._take_hands`, on a request at quarters that comes out short or too
few, asks `Quarters.lend(want, aloft)` for more: by the fighting book's priority
(`sail before guns`, the default of a ship whose sailing is her weapon; `guns before sail`
by the player's or the doctrine's word) it releases hands from the gun crews, the
disengaged battery first, then the engaged battery's guns from the one that bears least
(the after guns when she engages on the bow, the forward when on the quarter), never the
helm, the powder last, the marines after the guns; the guns robbed go short-handed or
silent, and the line that begins the work says from where ("All hands about ship: the
trimmers, 28, and 24 hands from the larboard guns, Nos. 1 to 6."). A robbed gun is
`short` in `the guns`, and the battery's minute line says so. Hands come back of
themselves: each tick, a hand at quarters whose `at` is None is put back at his quarters
station (`Quarters.tick`), so the guns refill as the tack ends, the earlier guns first.

**The gun's crew is numbers, not names.** The gun keeps the sailors' ids who are at it
(for the casualties and the crew factor); the muster is not changed. A casualty is a man
whose `fit` goes false and whose `hurt` says why; the gun's crew is short by him until
the bill fills the gap from the powder or the trimmers' surplus at the next beat (not of
itself: a gun captain does not rob the braces).

### The gun's cycle: `freesail/combat/guns.py`

`Gun` is a part of the graph (`freesail/ship/parts.py`), with its position (broadside by
number and side, a bow or stern chaser, a swivel on the rail), its kind and calibre, its
carriage, tackles and breeching as condition figures, and its **load state**: `empty`,
`loaded` (round, chain, grape, double), `run_out`, `primed`; its elevation and train; and
`dismounted` (a part out of the bill, as a sprung spar is out of the sail plan). The
`Battery` is the runtime over the guns of one ship: the standing intentions (the engaged
side, the load, the aim, the mode of fire: `as they bear`, `by divisions`, `at the word`,
`hold`), the target (the stranger's id as the lookout has her), and per gun a `Service`:

- the phase and the time left in it; the phases and their nominal times by kind:
  a long gun of the frigate's calibre `sponge 15 s, cartridge 10, wad and shot 15, ram 10,
  run out 20, prime 10, point 15` (a round in 95 s with a full and fresh crew; the figures
  are judgements that give Douglas's and the logs' broadside every minute and a half to
  two minutes at the start of an action, named in the tuning notes); a carronade shorter
  (no sponge-and-ram of a long bore, light to run out); a 3-pounder and a swivel shorter
  still;
- the pace: the nominal time times the crew factor of the hands at the gun
  (`hands.crew_factor`: numbers wanted over numbers at it, the rating, the fatigue, the
  roll on deck) times the weather factor (as every evolution's), so a tired or thinned
  crew fires slower and a full fresh one at the file's pace; a gun with fewer than half
  its crew does not serve (as sail work with fewer than half its hands does not begin);
- `fire` when the gun is primed and pointed and the intention lets it (`as they bear`:
  the target bears within the gun's arc; `at the word`: the word given; `by divisions`:
  its division's turn); the shot's flight and fall are `shot.py`'s and `hits.py`'s; then
  the cycle begins again, if powder and shot remain.

Fatigue: the hands at a gun tire at the deck's work rate (`routine.FATIGUE_AT_WORK_ON_DECK`),
the runner's rule for anyone whose `at` is set; so an action of hours slows of itself.

### Powder and shot

The magazine and the shot lockers are stores on the ship (`ship.extra["magazine"]`):
cartridges by calibre, shot by kind and calibre, from the ship file's armament section
(the Establishments' allowance per gun, Lavery: so many rounds a gun; written by the
generator with the source). Each firing takes one cartridge and one shot (two for double);
a gun whose calibre has no cartridge left falls silent and the battery says so once;
`the magazine` is a reading the gunner answers.

### The orders (the dialect)

Standing intentions (each a line when it changes something, nothing when it does not):
`clear for action`, `beat to quarters` (evolutions); `cast loose the guns`, `load with
round shot` (`chain`, `grape`, `double shot the guns`), `run out` (`run in the guns`),
`engage her to starboard` (`to larboard`, `on both sides`, `engage the brig`), `aim at
her hull` (`rigging`, `between wind and water`), `fire as they bear`, `fire by divisions`,
`hold your fire`, `cease firing`, `secure the guns`, `pipe down` (from quarters). One-shot:
`fire` / `fire the starboard broadside`, `fire No. 3 gun`, `fire the bow chaser`, `fire a
shot across her bows`, `fire a gun to leeward` (a signal: nobody is fired at; 71's hook),
`strike the colours` (never refused, its consequence told). Readings: `the guns`, `the
damage`, `the bill` (`the butcher's bill`), `the magazine`, `the enemy`, `the colours`,
`the quarter bill`. Every verb is data in `data/vocabulary.yaml` with an `object` of
`gunnery`, routed to `freesail/orders/gunnery.py`.

### What was rejected, and why

- **Every step of the cycle an evolution instance** (the lead's reading taken literally):
  rejected for rule 7, above: the runner's serialisation by holds and its one-line-per-start
  log make a queue of what must be continuous, and a broadside of twenty-six guns would be
  twenty-six instances a round. The evolutions keep the transitions (clear for action, beat
  to quarters, cast loose, secure) where their shape fits: an order given once, with all
  hands, a duration and a line at each end.
- **A second crew object for quarters.** Rejected: the muster is the one truth of the
  company (rule 1 for men: a man hurt is a line of the muster); the quarter bill is a
  second *assignment* of the same men, kept as a field on each sailor and a runtime over
  them, so that every reader of the muster (the needs, the routine, the people, the
  readings) sees the same men.
- **A battle clock or a round structure.** Rejected by rule 7: no tick of the action is
  special; each gun is where its hands have got it.
- **Morale per division.** Decided in item 6's design (the ship's one figure), with the
  reason there: the colours are one decision of the captain's for the whole company, and a
  division's temper has nothing to act on until 73's fight on deck.

### What hangs from this (the later items)

Item 2 reads the gun as a part and the fit the scenario chooses; item 3 writes the
evolutions of the transitions and the cycle's figures; item 4 is what `fire` produces;
item 5 is where a shot lands in the part graph and the muster; item 6 gives the rules
captain his engaging book over these intentions and the morale that strikes; item 8 gives
the stations the readings in one line when they change; item 9 measures two crewed ships
served by this bill against the baseline.

### As built (the end of the package)

The shape held, with two of its transitions taken another way once they were run. `beat to quarters` is a crew order beside `call all hands` (`orders/crew.py`), not an evolution: an all-hands evolution queues behind the tack or the heave-to in hand (the first smoke had a crewed cutter wait ten minutes for her drum while her heave-to failed), and the drum must not; the hands are turned up by the routine and the bill assigned at once, a hand at work going to his gun as it is done. `cast loose the guns` and `secure the guns` are evolutions for their time but take it from the crews at their guns, asking the runner for one hand (a frigate's company is minutes coming up the hatchways, and the first measure had her guns never come loose waiting on the pool). `clear for action` stays the all-hands evolution it was. The guns' cycle, the standing intentions, the robbing by priority and the one figure of morale are as written above; every figure is in `docs/dev/TuningNotes.md` (package 70).
