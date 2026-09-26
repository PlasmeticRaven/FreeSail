# FreeSail: Technical Specification, Milestone 3 (Crew)

Companion to `docs/TechnicalSpec-M0-M2.md`, whose conventions (units, tick, determinism, log voice, file formats) hold throughout. Read that document's §3 to §8 first. This chapter specifies what milestone 3 adds and the exact seams where it plugs into the milestone 2 code.

Owner's decisions that shape this chapter (gate M2 review, 2026-09-26):

- The **watch on deck** does the ordinary work. All hands are called only for evolutions that historically called them (tacking, wearing, reefing topsails) or when the captain says so.
- **Fatigue and the other crew parameters start soft**, so that everything can be seen working; they are tuned as we go.
- **Marines are aboard** from the start as a station, doing what Luce says they did at sea (standing watch and working as afterguard), and nothing else until powder.
- The **rig geometry** package (spec M0–M2 §12 items 8 and 11) follows milestone 3; it is not part of it.

## 1. What milestone 3 proves

"Orders take time and skill; the game has decisions." Two mechanisms carry that, and everything else in this chapter exists to serve them:

1. **Hands are a finite pool.** Every evolution asks for so many hands of a given rating from named stations. The pool is the watch on deck. Two evolutions that both want the fore topmen cannot both have them, so one waits, or the captain calls all hands and pays for it later.
2. **Work takes as long as the hands doing it need.** A step's time is its file's `duration_s` times the weather factor (as now) times a **crew factor** from the hands actually assigned: how many against how many were wanted, their ratings against the rating wanted, and how tired they are.

The whole of §3.5 of the proposal is not built here. Officers are names with stations; morale, sickness, punishment, watches below decks, the deck view and every crew *character* feature are later.

**Compatibility rule.** A rested crew at the ship file's complement, with the watch on deck, working one evolution at a time, must give a crew factor of exactly 1.0 and reproduce milestone 2's timings. The seventeen truths and the primer were tuned to those timings; a test enforces the factor. Where several evolutions now compete for hands (setting plain sail is eleven sails at once), timings will lengthen, and that is the milestone's point; the gate report carries fresh numbers.

## 2. The crew model (`freesail/crew/`)

Module layout per proposal §8.2, `crew/`:

| File | Owner (package) | Holds |
|---|---|---|
| `model.py` | 16 | `Sailor`, `Rating`, `Station`, `Watch`, `Crew` |
| `muster.py` | 16 | `muster(spec, seed) -> Crew`: the crew from the ship file's `crew:` section and a seed |
| `bill.py` | 16 | the watch bill: which stations stand in which watch, who is on deck now |
| `hands.py` | 17 | the pool: `request`, `release`, the crew factor |
| `routine.py` | 18 | watch changes, all hands and pipe down, fatigue and rest, the log lines for them |

### 2.1 A sailor

```python
@dataclass
class Sailor:
    id: str            # "s017", stable for the voyage
    name: str          # "Wm. Hoskins"
    rating: Rating     # LANDSMAN, ORDINARY, ABLE, PETTY_OFFICER, MARINE, IDLER, OFFICER
    station: Station   # FORECASTLE, FORE_TOP, MAIN_TOP, MIZZEN_TOP, AFTERGUARD, WAISTERS, MARINES, IDLERS, QUARTERDECK
    watch: Watch       # STARBOARD, LARBOARD, or NONE for idlers and officers
    skill_aloft: float # 0..1: work on the yards and in the tops
    skill_deck: float  # 0..1: hauling, the capstan, the braces
    fatigue: float     # 0..1: 0 fresh, 1 done in
    fit: bool          # False when sick or hurt; not built here beyond the flag
    post: str | None   # a station holder's post: "captain", "master", "boatswain", "first lieutenant"...
    trade: str | None  # an idler's trade: "carpenter's crew", "sailmaker's crew", "cooper", "armourer",
                       # "cook", "steward", "servant", "surgeon's mate", "clerk", "master-at-arms"; None for seamen
    at: str | None     # the evolution instance holding this sailor, else None
```

`trade` is data only in milestone 3: the idlers are mustered by trade so that later milestones find the carpenter's crew and the cooks where the ship's books would have them (§10). Nothing reads it yet except `muster`.

Skills come from rating with a small seeded spread, so that two able seamen are not identical but the crew's means are fixed by the file. Reference skill for the factor is the *ordinary* seaman at 0.6; able 0.8, landsman 0.35, marine 0.4 on deck and 0 aloft, idler 0.3 on deck and 0 aloft, petty officers 0.9. Numbers are provisional and tuned by package 17 against the compatibility rule.

Ordinary hands have no character fields, as decided (proposal §12 item 6). Station holders (`post` set) get an `outline: str` that is empty in milestone 3; the field exists so that M4's briefs have somewhere to live.

### 2.2 Stations and the watch bill

Stations and their period meaning, from Luce 1884 ch. XX (Watch, Quarter and Station Bills, from the paragraph beginning "The marines of a ship are divided between the two watches") and Falconer:

| Station | Work | In the watch bill |
|---|---|---|
| Forecastlemen | the head: headsails, bowsprit gear, anchors; the best older seamen | both watches |
| Fore, main, mizzen topmen | aloft on their own mast: loosing, furling, reefing, sending spars up and down | both watches |
| Afterguard | the quarterdeck: main and mizzen braces, spanker, sheets aft | both watches |
| Waisters | the waist: fore and main sheets and tacks, the pumps, the heavy hauling; landsmen | both watches |
| Marines | "their work on deck is generally the same as that of the afterguard. They stand regular watch at sea" (Luce). Never aloft. With all hands, "at the gear of main and mizzen topsails" | both watches |
| Idlers | cooks, stewards, servants, the carpenter's and sailmaker's crews, the armourer, cooper: "stand no night watches" (Luce); on deck by day and turned up with all hands to man gear | no watch: on deck from the morning watch to the first dog watch, below at night |
| Quarterdeck | the officers and young gentlemen: they give orders, they do not haul | no watch here; the officer of the watch is M4 |

Each watch is half of every watched station. **On deck** at any moment: the watch whose turn it is, plus idlers by day, plus everyone when all hands are called. The watch changes at the bells the clock already strikes (`core/clock.py`, `units.watch_of`), with the dog watches as they are.

### 2.3 The ship file's `crew:` section

Added to the ship file format (spec M0–M2 §6) as a top-level key, written by `tools/gen_ships.py` like everything else, validated by `ship/schema.py` (`CrewSpec`), optional: a ship file without it gets no crew and the runner behaves as in milestone 2 (unlimited hands, factor 1.0). That fallback keeps every existing test valid and lets a bare ship be loaded for physics work.

```yaml
crew:
  complement: 264            # Winfield, Amazon class establishment
  names: english             # which name list in data/crew/names.yaml
  stations:                  # hands per station, both watches together
    forecastle: 28
    fore_top: 24
    main_top: 30
    mizzen_top: 14
    afterguard: 50           # includes the boys
    waisters: 36             # so that stations and the twelve posts make the 264
    marines: 40
    idlers: 30
  ratings:                   # share of the seamen (not marines, idlers, officers) by rating
    able: 0.30
    ordinary: 0.40
    landsman: 0.30
  posts:                     # station holders by post; names are generated unless given
    - {post: captain}
    - {post: first lieutenant}
    - {post: second lieutenant}
    - {post: third lieutenant}
    - {post: master}
    - {post: boatswain}
    - {post: gunner}
    - {post: carpenter}
    - {post: purser}
    - {post: surgeon}
    - {post: sailmaker}
    - {post: master-at-arms}
  idlers_by_trade:           # how the idlers line above is made up; must sum to it
    carpenter's crew: 6
    sailmaker's crew: 3
    cooper: 1
    armourer: 1
    cook: 2
    steward: 3
    servant: 8
    surgeon's mate: 2
    clerk: 1
    master-at-arms's party: 3   # the ship's corporals
  stores:                    # numbers only in milestone 3; the milestones that consume them are in §10
    water_tons: 100          # Winfield gives iron-hooped casks for about four months at full allowance
    provisions_days: 120     # at full allowance for the complement
    spare_sails: 3           # made-up sails in the sail room, consumed by shifting a blown-out sail (§6)
    spare_spars: 4           # spare topmasts and yards in the waist and booms
    cordage_fathoms: 600     # spare rope in the boatswain's store
```

The stations must sum with the posts to the complement; the loader says so if they do not. Topmen are drawn from able and ordinary seamen first (Luce: "the smartest of the young seamen"), waisters from landsmen first, the afterguard from what is left, so the ratings line and the stations line together fix each station's quality.

The schooner (a privateer's complement of about forty, Chapelle; judgement): forecastle 10, fore top 6, afterguard 11, waisters 6, idlers 4 (cook, steward, carpenter's crew 1, sailmaker's crew 1), posts master, mate, boatswain; no marines; `names: american`; stores to match a small vessel on a short cruise (water for six weeks).

Names come from `data/crew/names.yaml`: two lists (`english`, `american`) of period given names and surnames, drawn with the seeded stream. The same seed gives the same muster.

### 2.4 Composition and determinism

`api/session.py` gets one more line in `make_world`: after the World exists, `crew.muster(ship.spec.crew, world.rng.stream("muster"))` and the routine attach to the ship (`ship.extra["crew"]`). The muster stream is named, so the crew is a function of the seed like everything else, and replay rebuilds it identically (`tests/test_replay.py` gains a crewed case). A ship built without a World (`make_ship` alone, as in many tests) has no crew and takes the fallback.

Nothing in `crew/` draws randomness except through the stream it is given, and only at muster. Fatigue, allocation and the routine are deterministic functions of the tick.

## 3. Hands: the pool (`crew/hands.py`, package 17)

### 3.1 Requests

An evolution file's `crew:` line, present in every file since milestone 1, becomes a request:

```yaml
crew: {hands: 12, rating: ordinary, stations: [topmen, afterguard]}
crew: {hands: all, rating: ordinary, stations: [all hands]}
```

`stations` names stations in order of preference; `topmen` means the topmen of the subject's mast (`ship.mast_of`), then the other tops; `all hands` means everyone fit. `rating` is the rating wanted; hands of a higher rating serve, hands of a lower rating serve more slowly (§3.3).

When an instance begins (`Runner._begin`) it calls `hands.request(crew, inst, want)`, which returns the sailors assigned and marks them `at = inst`. On completion or failure the runner calls `hands.release`. Scripts hold their hands for their whole run. The request looks only at sailors **on deck, fit and idle**, in this order: preferred stations by rating wanted, then higher ratings, then other stations, then lower ratings. Allocation order is by sailor id, so it is deterministic.

### 3.2 Short-handed

- **Enough** (got ≥ wanted): the crew factor for numbers is 1.0.
- **Short but workable** (wanted/2 ≤ got < wanted): begin with what there is; the numbers factor is `wanted / got` (twelve hands' work done by eight takes half again as long). Log once, routine: "Only eight hands to the fore topsail; the rest are at the main."
- **Too few** (got < wanted/2): the instance waits with `waiting = True` and a new `waiting_for = "hands"`, exactly as it waits today for a held part, and is retried each tick by `_start_waiting`. Log once, notable: "Not hands enough on deck to set the fore topsail; the watch is at the main topsail and the jib." The captain's remedies are to wait, to call all hands, or to belay something.

The runner never calls all hands by itself. An evolution whose file says `hands: all` **is** a call for all hands: it turns the watch below up (routine §5.2), takes everyone, and when it ends the watch below is piped down again unless the captain has called all hands separately.

### 3.3 The crew factor

For an instance with assigned hands `H`, wanting `n` hands at rating `r`:

```
numbers  = max(1, n / len(H))                          # never faster for extra hands in M3
skill    = mean over H of (reference_skill(r) / skill(h))   # skill for the work: aloft for topmen steps, deck otherwise
fatigue  = 1 + FATIGUE_WEIGHT * mean over H of h.fatigue    # FATIGUE_WEIGHT = 0.5 to start (soft, per the owner)
crew_factor = numbers * skill * fatigue
```

`reference_skill(r)` is the skill of a fresh sailor of rating `r`, so a request for ordinary seamen filled by ordinary seamen gives skill 1.0; filled by able seamen 0.75; by landsmen about 1.7. The skill term reads each hand's **rating** through the table (`crew.model.RATING_SKILL`), not the hand's individual skill with its seeded spread, so that a request filled at its own rating gives exactly 1.0 and the compatibility rule (§1) holds to the tick; individual skill is kept for later refinements. The step's rate is `dt / (duration_s * weather_factor * crew_factor)`, one line changed in `Runner._tick_steps`, and scripts receive `weather_factor * crew_factor` where they receive the weather factor today.

Whether a step is aloft or on deck is a per-step flag `aloft: true` in the evolution file (loosing, furling, reefing, sending spars up and down), default deck. Package 19 sets it while it rewrites the catalogue; package 17 reads it and defaults to deck when absent.

### 3.4 Pre-emption by all hands

When an all-hands evolution begins (tack, wear, reef topsails, shorten sail in a squall), the ship's whole attention goes to it. Running step-list evolutions **pause**: their progress holds, their hands are taken, and they resume, hands permitting, when the all-hands evolution ends. Their log says so once: "Belayed setting the studdingsails: all hands about ship." A paused instance is neither waiting nor running; `Instance.paused: bool` and `in_progress()` report it.

Two all-hands evolutions serialise as today, by holds.

## 4. The watch routine (`crew/routine.py`, package 18)

### 4.1 Watch changes

At every watch change the clock already knows (`Clock.watch()` changes value), the routine swaps the deck: the relieved watch goes below, the relief comes up, and the log says, routine: "Eight bells. The larboard watch relieved the deck." Hands **at work** are not relieved mid-evolution; they stay until it ends and then go below (the relief's idle hands are the pool meanwhile). Idlers come up at the start of the morning watch's second half (about six, "idlers, lay up rigging and sweep clean", Luce's routine) and go below after the second dog watch; between, they are on deck and available.

### 4.2 All hands and piping down

`routine.call_all_hands(reason)`: everyone fit comes on deck after a delay of `ALL_HANDS_DELAY_S = 90` seconds (hammocks, ladders), during which the pool grows tick by tick (a third at once, the rest over the delay, deterministically by id). Log, notable: "All hands! (to shorten sail)". While all hands are up, `all_hands_called = True`; watch changes do not send anyone below.

`routine.pipe_down()`: the watch below goes below; log, routine: "Piped down; the starboard watch has the deck." Called by the order, and by the runner when the last all-hands evolution ends if the captain did not call all hands himself (§3.2).

### 4.3 Fatigue and rest

Per sailor, per hour, added to `fatigue` and clamped to 0..1 (provisional, soft):

| Doing | Per hour |
|---|---|
| asleep below (watch below, night) | −0.12 |
| below by day | −0.08 |
| on deck, idle | +0.01 |
| at work on deck | +0.06 |
| at work aloft | +0.10 |
| turned up with all hands at night (the call itself: broken sleep) | +0.20 once (the spec's first figure, 0.03, was slept off before morning and showed nothing; package 18 measured 0.20 as the value that puts truth 20 in the middle of its range) |

A crew driven with three all-hands calls in the middle watch comes to the morning watch with the watch that should have slept at about 0.3 fatigue, a crew factor of about 1.15: visible in the log's timings, not crippling. That is truth 20 (§7). The owner tunes from there.

### 4.4 Meals and sleep

Not built. The dog watches exist; meals and the routine of the day beyond idlers up and down are M4 standing-orders material.

## 5. Orders and queries (package 20)

### 5.1 New orders (imperative dialect)

| Order | Kind | Effect |
|---|---|---|
| `call all hands` (also `all hands`, `turn the hands up`) | level 1 | routine §4.2, reason "by the captain's order" |
| `pipe down` (also `pipe the watch below`) | level 1 | routine §4.2; refused with the reason if an all-hands evolution is still running |
| `muster the crew` (also `muster`) | query | prints the watch bill: each station with hands on deck, below, at work, and their mean fatigue in words ("fresh", "tired", "worn out"); the posts by name |
| `send the larboard watch aloft to furl the main course`, `send the fore topmen to ...`, `... with the starboard watch` | level 0/1 | any sail order with a hands selector: the request is filled from the named watch or station only, calling that watch up if it is below (as a call for that watch alone, with the same delay), and the order is otherwise the same evolution |
| `relieve the watch` | level 1 | an early watch change (used when the routine is upset by all hands) |

Errors in the parser's voice: "The larboard watch is below; say 'send the larboard watch ...' to turn them up, or wait for eight bells." Grammar additions go in `data/vocabulary.yaml` and `orders/grammar.py` as modifiers, not new sentence shapes; the primer's chapter 6 gains the words.

### 5.2 `state`, snapshot and the client

- `World.summary_lines()` (console `state`) gains two lines: "Watch on deck: larboard, 96 hands, 24 at work (12 at the fore topsail, 12 at the main topsail); idlers up." and "All hands called" when they are.
- `queries.snapshot` gains `crew: {watch_on_deck, on_deck, idle, at_work: [{evolution, subject, hands}], all_hands, fatigue_mean_on_deck, fatigue_mean_below}`; `queries.ship_graph` is unchanged.
- The client's instrument panel shows the watch on deck and hands at work; the log shows the routine's lines under the existing severities. No deck view (M8).

### 5.3 What does not change

Level-0 line orders (`haul the weather main brace`) remain instantaneous and free of hands in milestone 3; they are the officer's fine adjustments, and giving them a cost belongs with the deck view. The helmsman is not a modelled sailor yet. Nothing in `physics/` changes except the sail states package 19 adds.

## 6. The catalogue to forty (package 19)

Twenty files exist. Milestone 3 brings the catalogue to at least forty, every file carrying `crew:` with hands and stations checked against Luce (the "hands" numbers in Luce 1884 ch. XX and the evolutions in ch. XXIII to XXVI) and `aloft:` on the steps that are, and cites its passage. The additions, all pure crew work on parts the ships already have:

| Evolution | Notes |
|---|---|
| `call_all_hands`, `pipe_down` | the routine's two orders as evolutions with a delay and a log line, so that they journal and replay like everything else |
| `send_down_topgallant_masts`, `sway_up_topgallant_masts` | `sent_down` on the spar and its dependents; the strain model already ignores sent-down spars; a real answer to a gale, which the gate M2 gale had no way to give |
| `strike_topmasts`, `fid_topmasts` | the same one level down; only with the yards above already sent down |
| `rig_out_studdingsail_boom`, `rig_in_studdingsail_boom` | split from `set_studding`, which then requires the boom out; the boom's state is a spar attribute |
| `unbend_sail`, `bend_sail`, `shift_sail` | a blown-out or wrecked sail is unbent and a new one bent from `stores.spare_sails` (one fewer); `shift` is the pair; new `SailState.UNBENT`. The one repair pulled forward from M8, because it is the most crew-heavy evolution the ship does and it lets the gale's damage be made good |
| `goose_wing` | a course or topsail with one clew hauled up: `SailState.GOOSE_WINGED`, effective area one half, centre shifted a quarter of the yard to the set side; `physics/sails.py` reads the state (the one physics edit) |
| `boxhaul` | script: a wear made short by bracing the head yards aback (Luce 1866 ch. XXIV "Box-hauling") |
| `lie_a_try`, `scud`, `back_and_fill` | scripts: heavy-weather and tideway setups from Luce ch. XXV and XXVI, each a helm policy plus a sail set, ended by `fill away` or a new order |
| `wear_under_bare_poles` | a parameter of `wear`, not a file, but the primer names it |
| `loose_sails_to_dry`, `furl_all` | routine work that costs hands and shows the muster at work |

The count reaches forty with the pairs counted as two. Every new file passes the registry's validation, has a primer sentence (chapter 3 or 5) and an entry in `tests/test_evolutions.py` that runs it on the ship that has the parts.

## 7. Truths for milestone 3 (`tests/test_known_truths.py`)

Numbers are provisional targets; the test states the range and the tuning notes the measured value.

| # | Truth | Source of the expectation |
|---|---|---|
| 18 | The frigate's watch on deck sets plain sail from furled in 25 to 40 minutes; with all hands called first, in 12 to 20 | Luce ch. XXIII: a smart ship loosed and set sail "in a few minutes" with all hands; a watch working sail by sail is several times longer |
| 19 | `tack ship` ordered while the watch is setting the studdingsails pauses that work; the tack takes what it took in M2 (five to seven minutes) and the studdingsails resume after | §3.4 |
| 20 | Three all-hands calls in the middle watch leave the morning watch's crew factor between 1.10 and 1.25; the same orders with a rested crew give 1.0 | §4.3, provisional |
| 21 | The schooner's watch (about fifteen hands) cannot set the fore topsail, the foresail and the mainsail at once: the third waits for hands and the log says so; with all hands it does not | §3.2 |
| 22 | Same seed, same muster, same log digest through a crewed voyage; a replay reproduces it | §2.4 |
| 23 | Sending down the topgallant masts in the gate M2 gale (35 knots, all sail) before the second ten minutes saves the royals: nothing carries away | §6 with the M2 strain model |

The compatibility test (§1) is separate: with the frigate's complement, one evolution at a time, every M2 evolution's duration matches the M2 value to within one tick.

## 8. Gate M3 (outline for `docs/gates/gate-m3.md`)

For the owner, on both ships, seed 7: muster the crew and read the bill; watch the log through a watch change and the idlers going below; set plain sail with the watch and see two sails wait for hands; call all hands and see them come up over a minute and a half and the work go faster; order a tack while the studdingsails are going up and read the pause and the resume; drive the crew through the middle watch and compare the morning's timings against the evening's; the schooner short-handed; the gale with the topgallant masts sent down in time; shift the blown-out fore royal in the gale that was not. Fresh expected numbers for every item, since the timings have moved.

## 9. Open items from this chapter

1. **Hands beyond the request.** In M3 extra hands never speed a step (`numbers ≥ 1`). Luce is clear that more hands on a halyard hoist faster up to the room on the rope; a per-step `max_hands` is the natural next refinement.
2. **The helmsman and the lookout** as modelled sailors, with skill in the helm law and sighting: M4 with the watcher, or M5 with sightings.
3. **The officer of the watch** as the giver of routine orders (standing orders' executor) and the M4 LLM station: `post` and `outline` exist for it.
4. **Meals, sleep below by day, sickness, punishment**: not modelled; fatigue is the only condition.
5. **Level-0 line orders costing hands**: with the deck view.
6. **Boys** are counted in the afterguard with landsman skill; a `boy` rating is trivial to add when it matters (powder monkeys, M7).

## 10. The crew who do not sail: placement in later milestones

Decided at the milestone 3 planning review (owner, 2026-09-26), so that the muster built now carries the fields the later work needs and nothing more. The sources divide the question: Falconer (1780) gives the *establishment*, which posts exist and what each is charged with; Luce (1884) gives the *routine*, when in the day each thing is done. Neither covers the British establishment of 1793 to 1815 exactly; the Admiralty *Regulations and Instructions* (1806 edition) should join `docs/references/` before the victualling work starts.

The organising idea is that the **standing officers are reporters with a domain**: each owns a set of readings, a set of evolutions and a set of hands (the carpenter: the hull and spars, sounding the well, plugs, fishes and jury spars, the carpenter's crew; the purser: water and provisions, serving out, slops, the steward and cooks; the boatswain: rigging and cordage, chafe, setting up; the sailmaker: canvas; the gunner: powder and shot). This is the authority boundary an LLM station needs (proposal §7.1): a model given the carpenter can report and mend and cannot trim a sail, and the watcher's "the carpenter reports two feet in the well" is a report from a post, not a narrator's invention.

| Milestone | What is built | Source to read first |
|---|---|---|
| **M3** (this chapter) | Idlers mustered by trade; posts include purser, surgeon, sailmaker, master-at-arms; `stores:` numbers in the ship file. Only spare sails are consumed. | Falconer, CARPENTER, ORDINARY (the standing officers), STEWARD; Luce ch. XX |
| **M4** (standing orders and the watcher) | The routine of the day as starter standing orders (hammocks up, meals, serving out water, the idlers' work); daily consumption of water and provisions as bookkeeping with readings (`the water` in days) for standing orders to test and the watcher to report; the standing officers' reports as log lines from posts. | Luce ch. XX "Routine", the serving-out passages; Falconer, PURSER |
| **M5** (the world) | Short allowance and its effect on fatigue and a first morale number; spoilage and casks stove in weather (director material, proposal §7.6); watering and victualling at ports; the purser's dealings with the market. | Luce on stowage of provisions (wet under dry, oldest first); port data |
| **M7** (powder) | The surgeon and surgeon's mates with casualties; the gunner's domain; powder monkeys (a `boy` rating). | Falconer, GUNNER, SURGEON |
| **M8** (mending) | The trades' evolutions against the condition model: caulking, plugging shot holes, fishing a sprung spar, jury masts (carpenter); setting up rigging, chafe, worming and serving (boatswain); repairing and making sails (sailmaker); casks (cooper). | Falconer, CARPENTER; Luce ch. XXX to XXXII |
| Deferred | Discipline and the master-at-arms as mechanics, the chaplain, the schoolmaster, midshipmen as characters: LLM and narrative material when stations exist; morale stays one number until short allowance or boarding needs more. | |

Nothing in this table changes the milestone 3 packages beyond the fields in §2.1 and §2.3.
