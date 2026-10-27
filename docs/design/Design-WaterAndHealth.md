# Design note: water in the ship, damage control, health and the fight on deck (package 73)

Written before anything of package 73 was built (the brief's rule: "the water in the ship
and the muster's states are designed first and written down before they are built", because
74's strike and its consequences and 77's damage-control catalogue build on them). Spec M7
§11, §11a, Part 7-iii (§13 to §15) and Part 7-iv (§16, §16a, §17) bind, with rule 1 (damage
is just state), rule 2 (served by the bill), rule 6 (realism, not pacing) and rule 7 (nothing
pre-defines a battle's timing); the owner's note 3 (the marines, their kit by nation) and
note 7 (a station holder hurt at parity) are the reasons for two of the shapes. The lead's
readings in the brief are taken where the engine agreed with them and departed from in the
places said below, each with its reason. What 70 left this package is the ground: the shot
hole written as state with its place against the waterline and no water flowing
(`combat/hits.py`), men killed and wounded off the bill with no surgeon (`Sailor.hurt`), the
marines a division of the quarter bill with no fire, `boarders away` and `man the pumps`
refused in words, and the hotfix's two director forms standing in for the carpenter and the
pumps (`aboard: the leak stopped`, `aboard: the well pumped out`).

## What the engine has, and what water, wounds and a boarding ask of it

- **The well is a number and nothing moves it but the ground.** `Hull.water_in_well_m` is
  written by `world/ground.py` while she lies aground, in metres of the well an hour by the
  bottom's kind, capped at two metres where "she is waterlogged and nothing more is
  modelled"; the carpenter sounds it (`sound the well`, the hotfix's reading) and the
  director's two forms empty it or stop the ground's leak. A shot hole below the waterline
  is a dict in `Damage.holes` with its side, its place along the hull, its height against
  the upright waterline and its diameter: everything the water needs and no water.
- **Work is an evolution with hands that ends, or the guns' cycle that does not.** The
  pumps are the second kind: men at the brakes until the well sucks or they are spelled,
  which is why 70's design made the gun's service a cycle and not an evolution (rule 7).
  The carpenter's plug, the fothered sail, the preventer braces and the jury mast are the
  first kind: an order given once, hands, a duration from the sources, a line at each end.
- **The muster knows `fit` and `hurt` and nothing between.** A man is on the bill or off it;
  70 wrote "killed" and "wounded" into `hurt` and took him off. Nothing heals him, nothing
  buries him, nobody is sick, and the needs of M7b stop at the last step's urgent line and a
  man asleep where he stood.
- **The officers are never hit.** `hits._casualties` draws from the quarter bill's divisions
  and the hands on deck, and the quarterdeck is in neither pool; a station holder's person
  (`Person.sailor_id`) can be hurt only by the director's word, and the harness has no line
  for it.
- **The marines are idle by the bill** (`Quarters.lend` says so), carry no kit, and nothing
  fires at men but the guns' grape through the hit model's shares.
- **Two ships cannot be held together.** The physics has one body per World; the ground and
  the anchor hold a ship in place by state hooks the integrator reads (`extra["aground"]`,
  the cable), and that is the shape a grapple can borrow.

## The design in one paragraph

**The water in the ship is one quantity, in tons, kept by a keeper of the World**
(`world/water.py`, `Water`, ticked every tick after the ship's step, for the player's World
and every crewed World alike) **fed by sources that are each a state the game already has**:
a shot hole below the water (70's dict, flowing by the orifice law from its depth under the
heeled waterline and its diameter, until the carpenter plugs it), the ground (the hotfix's
rate, handed to the keeper instead of written to the well, so the Horta figures stand), the
seams working in a seaway (a small rate by the ship's size and her roll, calibrated so that
a sound ship in ordinary weather makes no water worth a line: the morning watch's pumping is
a routine the watch does unasked and the log never says), and the sea shipped over the
hatches in a heavy sea until they are battened down. The well's depth is the volume over the
bilge's floor, so `sound the well` and `the well` read as they did; the free surface takes
from the metacentric height by the naval architect's formula where the hull's stability is
already a figure (`Hull.gm_m`, read by the heel's balance and the roll in place of the file's
figure, identical with a dry well); **the pumps are a standing work like the guns' cycle**
(`Pumps`, the ship file's pumps through the generator with Falconer's figures, manned by
`man the pumps` from the hands' pool so that the braces and the pumps compete for the same
men, spelled every glass by the keeper or by the word, gaining or losing by the rates), and
**she founders when the water reaches the share of her displacement that is her reserve of
buoyancy**, the log saying when the pumps lost, the hands to the boats, the ship held awash
by a state hook of the ground's kind. **Damage control is evolutions of M3's kind** (the
carpenter's plug by the hole's place, the fothered sail, the fished spar, the preventers
and the chain slings before an action, the standing rigging set up again, every parted
running line rove in turn by one order, a mast cut away, a jury mast from the booms), each
competing for hands by the fighting book's priority, each consuming a counted store through
the generator (shot plugs, cordage, a sail, a spare spar). **The muster gains four states
and a surgeon**: hurt (dressed and fit for light duty on deck), wounded (below, the
surgeon's, light or grave), sick (the sick list, by the ship's condition and the needs'
ends) and dead (buried at sunset with a line of the log and struck from the books, counted
still against the company's temper); the surgeon and his mates work the wounded in the
cockpit one at a time by a queue, the lightly hurt back on the bill in days and the badly
not, by a health stream opened at the first casualty and never before, so no sailing passage
moves; the needs of M7b meet their ends for a stationed person (collapse, then death, by
hours from the table) and for the company (the water expended, the water foul). **A station
holder is a man of the quarterdeck, the most exposed place**: the after deck's hits and the
musketry fall on the officers by a share, his hurt comes to his station as an urgent line
with his three roads (keep the deck, go below to the surgeon, carry on until he collapses),
the same for a model and a human, and a holder killed ends his station as a death does.
**The marines carry a kit by nation from `data/marines.yaml`** (the musket and bayonet, the
sergeant's halberd, the officer's sword; the French with soldiers and sharpshooters in the
tops), stand their sentries by day, and at quarters **fire by volley or at will within
musket shot at the men on a near deck**, the quarterdeck first, beside the ship's company's
small-arms men with the stand of arms served out; **the fight on deck is resolved in rounds
of a minute from the boarders' crossing** with numbers, arms, temper, cover and the volleys
and the grape counted in, the losses written to both musters, the deck carried (the colours
struck by the boarders' hand) or the boarders repulsed, on two ships grappled by §11a's
evolution and held together by the ground's own hook. The rules captain's boarding, his
pumps and his damage control's priority are thresholds in his role's file, the books written
again at the transitions.

## The pieces

### The water: `freesail/world/water.py`

`Water` on `world.water`, made with the World (and with every `CrewedWorld`, which is a
World), ticked once a tick from `World.tick` after the ship's step and before the action:

- **the quantity**: `tons` of water in the ship, kept in `ship.extra["water"]` (a small
  dataclass: the tons, the leaks, the pumps' state, the hatches), and written each tick
  to `Hull.water_in_well_m` as the depth the carpenter's rod finds:
  `depth = tons / (WELL_FLOOR_COEFF · L · B)` with `WELL_FLOOR_COEFF = 0.45` (judgement: the
  flooded floor of a hull of block coefficient about a half, narrower at the bilge; the
  frigate's 1 m of water in the well is 220 tons, the cutter's 40), so that the hotfix's
  grounding figures (metres of the well an hour) convert to tons by the same floor and
  the Western Islands' save reads the same depths;
- **the sources**, each a `Leak` with its kind, its cause in words, where it is, and a rate
  function of the ship's state now:
  - *a shot hole* (`Damage.holes`, 70's dict, gaining `plugged: tick | None`): below the
    heeled waterline it flows by the orifice law `Q = C_d · A · sqrt(2 g h)`, `C_d = 0.6`
    (the sharp-edged orifice; any hydraulics text), `A` the hole's area from its diameter,
    `h` the head: the hole's depth under the water outside less the water inside above it,
    the depth under the heeled waterline being `-(z_m) + s · (B/2) · sin(heel)` with `s`
    positive on the side heeled down. An 18-pounder's hole (5.04 in) half a metre under
    takes in some 85 tons an hour, a 12-pounder carronade's (4.4 in) a third of a metre
    under some 50: a shot hole between wind and water is a grave leak until the carpenter
    gets a plug in it, which is the period's record (the logs' "a shot between wind and
    water, the carpenter stopped it"). A hole above the waterline upright that the heel
    brings under flows while it is under: the lee battery's famous danger. A plugged hole
    flows no more (a plug weeps nothing here: judgement, 77 may give it a trickle);
  - *the ground* (`ground.py`'s `extra["leak_m_per_h"]`, the hotfix's figures kept to the
    number): converted by the floor to tons an hour, stopped by the carpenter's caulking
    (`stop the leak`, the hours below) or the director's cause;
  - *the seams working in a seaway*: `SEAMS_T_PER_H_PER_100T · (displacement/100 t) ·
    f(roll)`, `f` nought under 6° of roll, rising with the square of the roll over it to a
    cap at 25°, `SEAMS_T_PER_H_PER_100T = 0.02` (judgement, calibrated below: the frigate in
    a moderate sea of 9° roll makes a fifth of a ton an hour, a quarter of an inch a watch,
    and in a gale's 20° roll some five tons an hour, two inches a watch; the period's "sucked
    the pumps dry at eight bells" is this water); a ship holed by the ground or strained
    (a `strain` above her rating in the last watch) works her seams three times as much;
  - *the sea shipped* over open hatches: nought under `SEA_SHIPS_OVER_M` of the sea's
    combined height (3 m, "a heavy sea" by the sea's words), rising with the height above
    it, `SEA_T_PER_H_PER_M` = 2 tons an hour a metre of excess for a hull of 100 tons scaled
    by her length; stopped by `batten down the hatches`; rain is left out (the weather has
    rain as words and no quantity; said in the tuning notes);
- **the routine's pumping**: once a watch at the bells, when the well shows under
  `ROUTINE_PUMP_UNDER_M` (0.15 m, half a foot) and no leak but the seams runs, the watch
  pumps her dry unasked, silently (no line, no hands: the idlers' ten minutes at the brakes
  are the morning's routine, and the log of every recorded passage stays as it was); the
  reading `the well` says "sucked dry at eight bells";
- **the well's lines**: the carpenter's report at each foot while she gains (`well.rising`,
  the hotfix's line and kind, now from the keeper for every source), "the pumps gaining",
  "the pumps losing" when the sign of the balance changes under manned pumps
  (`pumps.gaining`, `pumps.losing`, notable), "the pumps suck" when the well is under two
  inches under the pumps (`pumps.sucked`);
- **the free surface**: `Hull.gm_m` a property: the file's `gm_m` less the free surface's
  `i / ∇` with `i = l · b³ / 12`, `l = 0.6 L` (the length of the flooded hold), `b` the
  breadth of the water's surface, the beam times `min(1, 0.3 + depth / (0.5 · T))` (the
  bilge's rise: a few inches of water lie in a narrow trough, a foot spreads over the
  floor; judgement), `∇ = displacement / 1025` (Rawson and Tupper, *Basic Ship Theory*, the
  free surface effect, the standard formula), floored at `GM_FLOOR_M = 0.05` (the motion's
  own floor). `physics/hull.py`'s `equilibrium_heel` and `physics/motion.py`'s
  `Particulars.of` read `hull.gm_m` in place of `hull.spec.gm_m`: two lines, the state hook
  rule 1 wants, identical with a dry well (every pinned passage sails as it did);
- **foundering**: when `tons >= FOUNDER_SHARE · displacement_t`, `FOUNDER_SHARE = 0.5`
  (judgement: half her own weight of water in her and her reserve of buoyancy is gone; the
  frigate at 635 tons, 2.9 m in the well; the cutter at 53 tons, 1.3 m), with a line at
  three fifths of it ("she is settling; the water is over the orlop", urgent,
  `ship.settling`) and the end: "She is going down. The hands take to the boats; the log
  says the pumps lost her at hh:mm" (`ship.foundered`, urgent; the tick the balance last
  turned against the pumps is kept for it), `extra["foundered"] = tick`; the integrator
  holds her as the ground does (`st.aground` true when `extra["foundered"]`: no way but the
  stream's; one line in `physics/integrate.py`, the ground's own hook widened), her sails
  are taken as wrecked by the strain's own rule (`_wreck_spar` on the lower masts: she lies
  a hulk awash), the guns fall silent, the far vessel of a crewed ship is `done` and her
  lookout's words say "she has gone down"; the player's ship founders with the scenario
  going on (`world.ship_lost`): the stations are told, the director may continue it (82's
  boat as a vessel is where the hands in the boats go next; here they are words). The
  hotfix's "waterlogged" word is retired for the settling line;
- **the pumps** (`Pumps` in the same module): the ship file's `pumps:` list through the
  generator (below); `man the pumps` takes `sum(p.hands)` hands from the pool by
  `hands.request` with the instance id `pumps` (so the bill, the routine's fatigue at work
  and every reader see them at work; at quarters the carpenter's division first by the
  bill, then `Quarters.lend` under the doctrine's priority), each pump lifting its rated
  tons an hour times the inverse of a crew factor of its own (`hands.crew_factor`'s terms:
  the numbers, the rating against the ordinary seaman's (a pump's brake is deck work), the
  fatigue; the seaway's deck column) while the well shows water; `spell the pumps` releases
  them and takes fresh hands, which the keeper does of itself every `SPELL_S` (1800 s, the
  period's glass at the pumps; Falconer 1780, PUMP: the chain pump's men "relieved at short
  intervals") when fresh idle hands can be had, the tired ones going idle; `the pumps'
  crews stand down` / `secure the pumps` stops them; the pumps suck when the well is under
  `SUCK_M` (0.05 m) and the hands are released with the line. The figures: the chain pump
  of Cole and Bentinck, standard in the King's ships by 1805, "wrought by four men,
  discharged a ton of water in 43 seconds and a half" (Falconer 1780, PUMP, the Seaford's
  trial of 1769), so 80 tons an hour a pump at four men fresh; the common hand pump (the
  brake or elm-tree pump) 15 tons an hour with two men (judgement from its bore: a 7-inch
  bore, a 12-inch stroke, thirty strokes a minute is 13 tons); the frigate two chain pumps
  and two hand pumps (Lavery, *Arming and Fitting*: two chain pumps at the main mast and two
  elm-tree pumps in a frigate), the brig-sloop one chain pump and two hand pumps
  (judgement), the cutter, the schooner, the lugger and the merchant brig two hand pumps,
  the smack one (judgement; Steel 1794 on the pumps of small vessels).

### Damage control: `freesail/evolutions/repair_scripts.py` and `data/evolutions/`

Each an evolution of M3's kind (a file with its crew line, its timing and its source; a
script where a step list cannot decide), serialised by its holds, competing for hands with
the guns and the sails by the fighting book's priority as every evolution does
(`Runner._rob_the_guns`), each consuming its store:

| Order | Evolution | Hands | Time (judgement unless said) | Store |
|---|---|---|---|---|
| `plug the shot holes`, `plug the hole`, `stop the leak` | `plug_shot_hole` (the carpenter's crew, the worst leak first, a phase a hole) | 4 of the carpenter's crew, else idlers and waisters | 10 min a hole above the waterline, 20 at or within half a metre under, 40 deeper (reached from the hold with the water about the men; Falconer 1780, PLUG: "shot-plugs ... to stop holes made by cannon shot"; the Regulations 1806, the Carpenter: plugs, oakum and sheet lead ready in action) | a shot plug a hole (`crew.stores.shot_plugs`) |
| `stop the leak` with the ground's leak | the same script, the seams caulked | 6 | 3 hours (Steel 1794, the carpenter's duty; the Western Islands' day of it) | oakum (not counted) |
| `fother a sail over the leak` | `fother_sail` | 20 | 90 min (Falconer 1780, FOTHERING; Cook's Endeavour on the reef, 1770) | a spare sail from the sail room, worn out |
| `fish the fore topmast` | `fish_spar` | 8, aloft | 45 min (Luce 1884 ch. XXXI, 'Lower Mast Carried Away or Sprung': the fishes, the woolding) | a fish (not counted; the capstan bars and the spare spars' makings) |
| `rig preventer braces`, `rig preventer backstays`, `sling the yards` | `rig_preventers` | 12, aloft | 20 min each (Luce 1884 ch. XX 'Clearing for Action': "preventer braces rove, the yards slung with chains") | cordage by the lines' fathoms (`crew.stores.cordage_fathoms`) |
| `set up the larboard main shrouds`, `set up the rigging` | `set_up_rigging` (every parted standing line in turn) | 10, aloft | 45 min a shroud or backstay, 60 a stay (Lever 1808, 'Setting up the Shrouds'; judgement for the minutes) | cordage by the line's fathoms |
| `reeve new lines`, `knot and splice the rigging` | `reeve_line` for every parted running line in turn, one order (the owner's form) | 6 each, as the file has it | as `reeve_line` | cordage |
| `cut away the mainmast` | `cut_away_mast` (a standing lower mast wrecked by the axes and cleared) | 10 | 15 min (Falconer 1780, VEERING: "the mizen-mast must instantly be cut away") | none |
| `rig a jury mast`, `rig a jury foremast` | `jury_mast` (a spare topmast from the booms stepped in the stump) | 30 | 4 hours (Luce 1884 ch. XXXI, 'Jury Masts'; Falconer, JURY-MAST) | a spare topmast |
| `batten down the hatches`, `open the hatches` | `batten_down` | 8 | 10 min (Luce 1884 ch. XXIX, 'Preparing for a Gale': the hatches battened) | none |

The effects are states the game has: a hole `plugged`; the ground's leak nought; a fothered
ship's underwater leaks at three tenths while the sail holds (it goes when she makes more
than six knots or takes the ground again: judgement); a fished spar's condition raised to
70 at most (it will not bear a press of sail: the strain reads it); a line with a preventer
rove keeps its office when it is shot away or parts (`Line.preventer` consumed, the strain
model's `_part_line` returning after a note "the preventer brace holds": the hook of 70's
kind at the one place a line parts); a chain sling the same for the yards' halyards and
ties; a standing line set up again sound at a new rope's rating; a lower mast cut away is
`_wreck_spar(how="cut away")` and cleared; a jury mast is the lower mast standing again with
`jury: True`, its rating two fifths and its condition 40 (the topmast and what stood on it
stay down), so the course can be set on it and the strain model takes it at a press, which
is the period's jury rig. The cutter with no spare topgallant mast stays so; a ship with no
spare topmast rigs no jury mast and is told why.

**The damage report names everything** (`the damage report` and the carpenter's and the
boatswain's rows): every parted line by name and class ("the starboard topsail sheet and
the larboard main brace shot away; the larboard main shrouds, two of them, parted"), each
sprung spar (condition under 60: "the fore topmast sprung"), each holed sail with its share,
each dismounted gun, each shot hole by side and place against the waterline and whether
plugged, the helm, the hatches, and the well with its gain; `the parted lines` is a reading
of the parted lines alone, for the owner's `reeve new lines`.

### The muster's states, the surgeon and the needs' ends: `freesail/crew/health.py`

`Sailor.hurt` keeps its words and gains the states; new fields `wound` (`""`, `"light"`,
`"grave"`), `hurt_until` (the tick he is judged or healed), `dressed` (the surgeon has seen
him). The states and what they do:

| State | `fit` | Where | Who may take him | How he got there | How he leaves |
|---|---|---|---|---|---|
| fresh | yes | the bill | any work | | |
| hurt (light duty) | yes | the bill | deck work, never aloft (`can_work`), the gun's crew at a hand short in the factor's skill | a light wound dressed | healed in `HEAL_LIGHT_D` days (7 to 14 by the stream; Turnbull 1806, *The Naval Surgeon*, on contusions and splinter wounds; judgement) |
| wounded | no | the cockpit at quarters, the sick berth after | nobody | a shot's casualty not killed: light or grave half and half (judgement on the returns' "dangerously" and "slightly") | light: dressed by the surgeon in `DRESS_LIGHT_S` (10 min of his time) and then hurt; grave: `DRESS_GRAVE_S` (30 min: the amputation and the ligature), then judged at a day: dies with `DIE_GRAVE_TREATED` (0.3; the period's mortality of the badly wounded about a third: James's returns, Turnbull) or `DIE_GRAVE_UNTREATED` (0.6), else invalided for the voyage (`hurt="wounded"` for `HEAL_GRAVE_D` 40 days) |
| sick | no | the sick berth | nobody | the ship's condition at the morning report (below) or a person's needs' end | recovered in 3 to 7 days (the flux; judgement), or dead by the hazard |
| killed | no | the deck, then the deep | nobody | a shot, a ball, a cutlass | buried at sunset or at the next morning watch, whichever first (`bury the dead` any time), one line of the log naming them ("Committed to the deep the bodies of ..."; the Regulations 1806, the Chaplain, the burial service), struck from the books (`Crew.dead`, so `complement` falls and the morale's losses still count them) |

**The surgeon** is a post the file has (the frigate's and the brig's; a cutter, a lugger, a
schooner and a merchant brig bore none, and the reading says so: their wounded are dressed
by their messmates in an hour and fare as the untreated), with his mates the idlers of that
trade; his place the cockpit at quarters (`SURGEON` division) and the sick berth under the
forecastle else (the frigates' sick berth of the 1800s: Lavery). His work is a queue of the
wounded in the order they came, the grave before the light when both wait (the surgeon's
triage was the reverse in the period, first come first served; the owner may want it so:
a knob, `surgeon_order: worst first`), each man taking his minutes of one surgeon's or
mate's hands (a mate dresses a light wound, the surgeon alone operates); so a broadside's
dozen wounded keep him two hours, which the station reads ("the surgeon: in the cockpit at
work on the wounded, four waiting"). A health stream (`world.rng.stream("health")`) is
opened at the first wounded man and never before (the strain's determinism test pins the
sailing's streams; nothing of a sailing passage draws from it).

**The sick list** by the ship's condition, drawn once a day at the morning watch's eight
bells for every fit man: the water foul (`stores.foul`) `SICK_FOUL_WATER` 2 in a hundred a
day (the flux: Trotter, *Medicina Nautica*, the Channel fleet's sick lists; judgement for
the rate), short allowance beyond a week 1 in a hundred, the water expended (nobody drinks)
thirst's own course below; nothing else (a healthy ship at whole allowance draws nothing,
so no passage moves; the base sickness of a company, the fever and the scurvy are M8's,
and the cold and wet wait on §26's temperature, said in the tuning notes). The sick list is
a reading and the morning report's routine line (`health.morning_report`, said only when the
list is not empty, so that no recorded log gains a line).

**The needs' ends** (M7b §20 left them here): for a stationed person, thirst at
`THIRST_COLLAPSE_H` (72 h) puts him down (sick, in his berth; the station stands by as it
does for a man asleep where he stood, the line saying "you have collapsed", the deck
passing by the bill) and at `THIRST_DEATH_H` (96 h) he dies; hunger at 7 days and 21 days
(the body's figures from the medical commonplaces: three to five days without water, weeks
without food; judgement at the long end because the table's own steps are soft); fatigue's
end is the table's sleep where he stands, as built by 54, and nothing more. For the
company: the water expended (`stores.water_tons <= 0` with the beer expended) counts the
days; from the second day a tenth of the fit men a day go on the sick list "with thirst",
from the fourth day one in twenty of the company a day dies of it, the log explaining from
the stores' lines before ("The last of the water started", the purser's page) and the sick
list's; the water foul drunk from the casks is the flux above, and a tenth of the sick of
the flux die after five days without a port's water. The hunger of a company with the
provisions expended takes the same road a fortnight later.

**The lines.** The butcher's bill after an action, once, when ten minutes have passed with
no shot fired or struck and the company is at quarters still or stood down ("The butcher's
bill: two killed, Wm. Hoskins and Jas. Pryor; seven wounded, three of them dangerously",
notable, `action.bill`); a named person's own line as 70 had it; the morning report; a man
returned to duty, routine; a death in the sick berth, notable; the burial, notable.

### A station holder hurt: `combat/hits.py`, `crew/health.py`, `agents/harness.py`

- **Exposure.** The quarterdeck's people (the posts' sailors, the helm's men, the station
  holders' sailors) join the pool of the casualties for a hit on the after deck
  (`x_m < -L/4`) and for a rigging hit's falling block, with the officers at
  `OFFICER_SHARE` (0.2) of each such casualty (judgement: the quarterdeck of a frigate in
  close action lost its captain or a lieutenant in a good third of the recorded actions;
  James's returns); the musketry below aims at them first. Nobody on the quarterdeck is hit
  by a hit forward of the mainmast. A person's hurt goes to his sailor (`Person.sailor_id`)
  and so to the muster: one truth.
- **The station's line.** His hurt comes to the station holding him as an urgent notice in
  his next sample and the sample's `needs` row ("hit: a splinter in the thigh; dressed, you
  can keep the deck" / "wounded: a musket ball in the shoulder; you can keep the deck for a
  while, or go below to the surgeon"), and to the player at the prompt or his seat through
  the needs' listeners, as the needs' lines go (never the log; the log has `person.hurt` as
  70 wrote it).
- **His roads, at parity.** `keep the deck` is nothing to do: his orders go, his words
  carry, every sample says his state; a light wound costs him fatigue at a hardship of a
  half (he tires half as fast again); a grave wound bleeds: after `COLLAPSE_S` (1800 s,
  judgement) he collapses where he stands, which is `fall_asleep`'s road with its own words
  (the station stands by, "collapsed, carried below", the deck passing by the bill; woken
  by nothing but the surgeon's work, after which he may `come on deck` as hurt).
  `go below to the surgeon` (an order of the needs' kind, every station's own; the person
  moves to the cockpit, the deck passes: the officer's station gives it back to the captain
  as a handover does, the captain's station to the rules captain who carries on by the
  bill, `Captain.carry_on`) and he is in the surgeon's queue; `come on deck` when dressed.
  The same three roads for a model and a human: the harness gives the model the notice with
  its tools' words (`submit_order('go below to the surgeon')`), the player the line with
  the order's words.
- **Killed.** His person is dead (`Person.dead`, his state words "killed in action"), the
  harness tells the model in words in its last sample and stands the station down with the
  reason (`stand_down("killed: ...", by="the world")`: journaled, the log's line, the
  station released; no model is moved to another person by the game), the player's seat is
  released the same way with the line, the player at the prompt is told his person is
  dead and the deck passes by the bill: the first lieutenant (the mate) is the captain's
  person from then on (`People.captain` re-pointed), the rules captain commands by the
  doctrine, and the scenario goes on (74's roads and 82's seat at another person take it
  further; the prompt stays the owner's voice to whoever commands, which is 52's rule).

### The marines and the small arms: `data/marines.yaml`, `freesail/combat/small_arms.py`

- **The kit by nation** in a file of its own, named from each nation's entry
  (`marines: {kit: british}` beside 71's `habits` and 72's `naval`): the kit's weapons
  (words, for the readings and the fight), the musket's figures (`volley_s` the seconds a
  drilled detachment takes between volleys: the British 20 (three rounds a minute, the
  drill's figure; Hughes, *Firepower*), the French soldiers aboard 30; `hit_at_50_yd` the
  chance a shot tells on a man on a near deck at fifty yards: 0.05 (judgement from the
  period's musketry trials: a battalion volley at a hundred yards put one ball in five into
  a target the size of a line of men; a man on a deck behind a bulwark a fifth of that),
  falling with the square of the range to nought at `MUSKET_SHOT_M` (100 yards, spec §11),
  `tops_share` the share of the detachment the captain's book sends aloft (British 0.2,
  French 0.4), `tops_factor` the sharpshooter's edge from the tops (French 1.5, British
  1.0), `soldiers` whether the detachment is soldiers of the line (the French ships'
  troops) with their own temper), and the small arms of the ship's company (cutlasses,
  pikes, pistols, tomahawks: the words and a `boarding_factor` with and without them);
  the basic kit for every nation without one.
- **The detachment** is the muster's `marines` station (the frigate's 40, the brig's 20;
  the generator gives the brig and the frigate a sergeant among them (`post: sergeant of
  marines`, a petty officer's skill) and the frigate a lieutenant of marines on the
  quarterdeck (a post in the wardroom file and the ship file through the generator; the
  brig's party under its sergeant, as a brig-sloop's was); the cutter, the schooner, the
  lugger, the smack and the merchant brig bear none (true to the period; the owner's armed
  Indiaman is 75's). The French privateer cutter has no marines and a large crew of
  boarders: her small arms are the quarter bill's `small_arms` men.
- **By day**: the sentries at the cabin door, the spirit room and the gangway (three men by
  turns, a state the muster's marine line says), the guard, the drill in the forenoon
  watch (words of the state, never lines); at quarters the `MARINES` division as 70 beat
  it (the poop and the gangways), `marines to the tops` sends the book's share aloft (they
  are carried up: `can_work` aloft stays false; a state `in_tops` on the division),
  `marines to the gangways` brings them down; `the marines` a reading.
- **The fire.** Each tick of the action within `MUSKET_SHOT_M` of a near deck (a crewed or
  the player's mark; the far mark gets nothing: 74's), under the standing intention
  `marines, fire by volley` (one volley every `volley_s` by the whole detachment, the hits
  drawn at once) or `marines, fire at will` (each man at his own rate, the same hits over
  the same minute, drawn each tick), else `marines, hold your fire`: the muskets of the
  marines on deck and in the tops and of the small-arms men; hits a Poisson draw on the
  gunnery stream about `n · p(range) · factors`, the mark's roll and ours in the scatter;
  each hit falls on the men exposed on the mark: the quarterdeck's officers, helmsmen and
  station holders with `QUARTERDECK_SHARE` 0.4 (history's lesson, spec §11), the deck's
  divisions else (the marines and the gun crews of the engaged side first); killed three in
  ten, light and grave half and half as the shot's. The mark's people fire back by their own
  book. The hits are counted into `Damage.minute` and the minute line says "musketry from
  her tops: two wounded on the quarterdeck". The orders in the dialect (object `fight`):
  `marines, fire by volley`, `marines, fire at will`, `marines, hold your fire`, `marines to
  the tops`, `marines to the gangways`, `serve out the small arms` (five minutes with the
  gunner's party: the state the boarding reads), `small arms men, fire at will`.

### The fight on deck: `freesail/combat/boarding.py`, the grapple in `repair_scripts.py`

- **The ground for it.** `lay her aboard` (the navigation: the engaging helm's close law to
  `BOARD_RANGE_M` 25 m from `CLOSE_RANGE_M`'s 60 m: the captain's chase order with a
  boarding word) and `grapple her` (`grapple`, an evolution: 8 hands, 2 minutes, refused
  beyond 30 m; Falconer 1780, GRAPPLING) write `extra["grappled_to"]` on both ships; the
  integrator holds both as the ground holds a ship (no way but the stream's; the ground's
  own hook widened by the same `foundered`/`grappled` reading), so the two lie locked and
  drift together for the minutes the fight takes; `cast off the grapnels` frees them
  (either side; the boarders repulsed cast off of themselves). Two hulls within 25 m overlap
  on the chart until 78's collision; said.
- **The sides.** The attacker's boarders: the quarter bill's `boarders` (the generator: half
  of each disengaged gun's crew, the marines, the small-arms men; a privateer's doctrine
  takes more, `boarders_share`), under their officer; the defenders: every fit man on the
  upper deck not at the pumps or the powder, the marines first; `repel boarders` brings the
  gun crews up (the guns silent, the defence at its whole strength) and is the defender's
  one order; `boarders away` the attacker's.
- **The rounds.** From the crossing, once a minute, while grappled: each side's strength is
  its men times its arms (served out 1.0, not 0.5; marines with the bayonet 1.3; soldiers
  1.2) times its temper (the ship's morale, 70's figure) times its cover (the defenders
  behind their bulwarks and nettings 1.3 in the first round, 1.0 after; the boarders
  crossing 0.8 in the first); before the first round the defenders' marines' volley and
  the guns bearing on the boarders' deck loaded with grape tell (the musketry's hits and
  one grape volley's casualties by the hit model); each round each side loses a Poisson
  draw about `ROUND_LOSS · (the other's strength / 10)`, `ROUND_LOSS = 1.0` (judgement: a
  boarding of fifty against forty costs each side five or six men a minute, and is decided
  in five to ten; the period's boardings were short), the fallen killed three in ten and
  wounded else, written to the muster with `hurt_tick`; the deck is **carried** when the
  defenders' strength falls under `CARRIED_RATIO` (0.5) of the boarders' or their morale
  under its line (the colours struck by the boarders' hand: `action.strike(by_rule=False,
  words="carried by boarding")`, the state `struck`, 74's prize crew after), the boarders
  **repulsed** when theirs falls under the same share of the defenders' or their morale
  under its line (they cast off; their morale less `REPULSE_COST` 0.1), and a deck
  **contested** past `CONTEST_ROUNDS` (15) is a repulse (the attacker renews at his word).
  The log carries a line a round on both ships ("The boarders are on her deck: the fight at
  the gangways; four of ours down, six of theirs", urgent) and the end.
- **Morale read and written** as 70's figure: the fight reads it for the temper and the
  lines; the losses it writes move it by the losses' weight; the repulse costs it.

### The doctrine, in data (`data/captains/*.yaml`)

Thresholds with their sources, read by the captain's own work once a minute
(`Captain._work`) and the engaging work (`_engaging`), the books written again at the
transitions as 58b has it:

- `board_odds` (he boards when his boarders are so many times her fit company: a privateer
  1.0, a King's ship and a cruiser 1.3, a packet and a merchant nought: never), `board_when`
  (`her guns silent` or `at any time`: a King's ship boards a ship whose fire has slackened,
  a privateer boards at once to spare the prize), `repel_boarders: always`;
- `pumps_at_m` (he mans the pumps when the well shows so much: a foot, 0.3 m; a cutter half
  a foot), `spell_minutes` (30), `give_up_at_share` (0.4 of the foundering water with the
  pumps losing: he strikes to an enemy at hand or runs for the land; the hands to the
  boats at the end is the keeper's), `lighten_at_m` is named and left to 77 (the guns over
  the side);
- `damage_priority: [the leak, the rigging, the guns]` by his state (in action the leak
  first, then the rigging that keeps him sailing, then a dismounted gun which 77 remounts;
  after the action the rigging whole: `reeve new lines`, `set up the rigging`, `fish` the
  sprung spars, the hatches);
- `musketry_cables` (the marines open by volley within a cable: the British; the French
  within a cable and a half from the tops), `marines_tops` (the book's share aloft on
  entering the action: the French yes, the British no);
- the engaging book gains 'standing order "the small arms": when the range is under
  {musketry_cables} cables then marines, fire by volley' and 'standing order "repel": at
  boarders then repel boarders'.

### The stations, the director and the readings

- Readings (`api/action_readings.py` grown, and `api/health_readings.py` new): `the well`
  (the hotfix's, now with the gain an hour, the pumps' state and "sucked dry at eight
  bells"), `the pumps`, `the leaks`, `the damage report` (named), `the parted lines`, `the
  hatches`, `the sick list`, `the wounded`, `the surgeon`, `the butcher's bill` (70's `bill`
  with the states), `the marines`, `the boarders`; `where is the surgeon` by the people's
  words. Their rows ride in a sample only while something is afoot, as 70's do.
- Events for `at` and a stand-by: `the well rising`, `the pumps gaining`, `the pumps
  losing`, `the pumps suck`, `the leak stopped`, `she is settling`, `she founders`, `a man
  taken ill`, `a man dead`, `the burial`, `a volley`, `boarders` (on our deck),
  `the boarders away`, `the boarders repulsed`, `the deck carried`, `grappled`.
- The director's forms after `WORLD_ORDER_FORMS`: `aboard: a leak found` (the table's
  `seam_working`, modelled now: a leak of two tons an hour from a seam, plausible in a sea
  or after a strain), `aboard: a man taken ill` (one of the fit on the sick list with the
  flux, plausible with the water foul or short allowance or days out), `aboard: the fever
  in the ship` (a tenth), `aboard: Mr X is hurt` / `the marines' officer down` (a person
  hurt by a cause: plausible under fire), `aboard: the surgeon taken ill`; the hotfix's two
  kept with their doubt sharpened (`the well pumped out` doubted while the ship has pumps
  and hands to man them: "the hands could pump her out themselves; enter it again with a
  reason"; `the leak stopped` plausible when a leak runs). The director's truth shows every
  ship's water, her pumps and her muster's states.
- The harness: a hurt holder's line and roads as above (`Harness.md` §21f).

### The scenarios and the truths

`data/scenarios/leak.yaml`: the cutter in a rising westerly off the Lizard with a seam
started by the director's cause at the start and the sea getting up, the pumps gaining with
the carpenter at the seam and losing without him; the first action replayed (truth 7-133
again, with the water flowing from the Renard's holes and her captain's pumps and plugs).
Truths 7-161 onward as the brief's item 9 lists them, numbered in `tests/test_known_truths.py`.

## What was rejected, and why

- **The pumps as an evolution with a duration.** Rejected for the reason 70 gave the guns'
  cycle: pumping ends when the well sucks or the men are spelled, not at a file's seconds,
  and a queue of `man the pumps` behind a tack would be the wrong shape; the pumps are a
  standing work with hands from the same pool, so the braces still rob them and they still
  rob the braces.
- **Water as a change of draught in the physics.** Rejected: the physics is read and not
  changed; the free surface's penalty is applied where the stability is already one figure,
  and the draught's change (a few inches for a foot in the well) is below what the sailing
  would feel.
- **A second hull model (compartments, the orlop, the magazine flooded).** Rejected for
  rule 1: one quantity and the well's depth are what the carpenter knew; the cartridges damp
  with water in the well is the director's cause already.
- **Removing the dead from `sailors` at the moment of death.** Rejected: the morale's losses
  and every index count them until the burial, which is a thing done with its own line, as
  the period did it.
- **A base sickness rate for a healthy ship.** Rejected here: it would put a line into every
  passage of days and move its pin for a figure of judgement; the sick list arises from
  causes, and disease of its own is M8's.
- **The surgeon's triage worst first.** The period's was first come first served (Turnbull
  on the "wretched" rule of it); built as the period had it, with a knob the owner may turn.
- **Locking two hulls as one body.** Rejected: the physics has one body a World; the
  grapple holds both as the ground holds one, and they drift together, which is what the
  fight needs. 78's collision is where two hulls touching becomes the physics'.
- **The officers hit as the hands are, everywhere.** Rejected for the after deck's share:
  the quarterdeck is the most exposed place in a frigate action (the owner's note 7) and the
  one place the officers stand; a hit forward touches nobody aft.
- **The cutter given marines and a surgeon for the replay's sake.** Rejected: a King's
  cutter of 85 tons bore neither (Winfield's establishments give the cutters no marines; a
  surgeon was a frigate's and a sloop's), and the file stays true; the replay shows the water
  and the small arms instead, and says so.
- **Disease, the cold and the wet.** Left with the reason: M8's and §26's.

## What hangs from this (the later items)

74 reads `struck` by the boarders' hand and the prisoners' numbers from the musters; 77 fills
the catalogue from these first forms (the plug that weeps, the guns remounted and jettisoned,
the boarders' drill); 82 takes the hands in the boats off a foundered ship; M8 reads the
sick list's shape for its fevers.

## As built (the postscript)

Filled at the end of the package.
