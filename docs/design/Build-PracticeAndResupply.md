# Build design: practice at the great guns, and powder and shot taken in (stages A and B)

The single build document for `Proposal-PracticeFiring.md` and `Proposal-MagazineResupply.md`,
both approved by the owner on 2026-10-25. It starts from the compatibility design (the judges'
best), grafts what the two judges named from the fidelity and determinism designs, and
corrects every error they found, each checked against the code at the owner's local baseline
on `main` (the line's `2774be3` with the provisional pivot gun and privateer schooner; his
local commits are on no branch of the project, and this work is on the line at `5b01fdf`,
package 86's fold-in on top of package 73). Paths are relative to the repository root. Line
numbers are those of the local baseline; a builder re-checks a line before editing it.

The owner's rulings bind: stages A and B both now; the Ordnance's issue to a King's ship is
free and vouched, merchants and privateers pay; practice improves no skill (drill counts
per gun are kept, nothing reads them for pace or aim); the galley fire out while powder
comes aboard is a state the crew's needs read; ship-to-ship transfer waits for package 74.

The working name of this work in code comments and the tuning notes is **"practice and
resupply (between packages 72 and 73)"**. The lead may rename it.

---

## Decisions taken

Every judgement call a reviewer might question, so the owner can see them in one place.

| # | Decision | Why, in short |
|---|---|---|
| 1 | Charges: a long gun a third of its shot's weight, a carronade a twelfth, a swivel a half, rounded to the ounce. **UNVERIFIED.** Written into the ship files as `charges:` | Table No. 29 has lost its figures in the OCR. Package 75 enters the table's figures through the generator alone |
| 2 | A barrel holds 100 lb | Falconer's French glossary (l.22563-22564). The English barrel's weight is UNVERIFIED |
| 3 | Each fit starts with **today's cartridge counts, filled**, split by kind, and a reserve below of **half the filled powder** in whole barrels | Nothing an action does today moves. The period kept most powder in barrels; the share is judgement |
| 4 | The gunner fills **whenever a kind is below its level** (the fit's filled count). At quarters he fills always, with men of the powder division who are not lent out. Out of quarters he fills while the idlers are up. He never fills by night out of quarters, never while the hoy is alongside, and never after the colours are struck | Art. XVIII: "take all opportunities of filling powder" in action. Art. VII: the magazine is opened only with the officer in the light room. The judges preferred this to filling only below a third |
| 5 | The filling party is the bill's new `filling` count, one man to every four great guns (frigate 10, brig 4, the rest 1). The men are **read, never moved**, and no quarter gunner is mustered as a post | Falconer, QUARTER-GUNNER (l.14283-14289). A new post would shift every muster draw and every digest |
| 6 | A gun with no filled cartridge of its kind **waits at the cartridge phase** while there is powder below. With no powder either, **today's path is kept unchanged** | Only the new state takes the new path |
| 7 | "The magazine is out" and the shot-fallback line clear themselves when stores come back. "The gunner is filling" is said once per outage, which ends when the kind is back at its level. A game resumed from an older checkpoint may say an old line once more | This fixes the never-cleared sets without letting the filling line spam |
| 8 | The Ordnance issues **free and vouched** to the King's ships of the port's own nation. Merchants sell to everyone else. **A sale is paid when the hoy comes alongside**, not at the order | Owner's ruling. Paying on delivery needs no refund when the hoy finds her gone (the judges' graft) |
| 9 | A King's ship buys from merchants **only "of necessity"**, from the purse, and the log keeps the captain's word | Regulations l.6220-6247, "absolute necessity" |
| 10 | Ordnance ports: **Plymouth and Gibraltar**. Merchant ports: **Falmouth, St Peter Port, Brest, Lorient, Rochefort, St Malo, Cadiz, Ferrol, Lisbon**. The other **27** port files have no block. Plymouth's town sells nothing (UNVERIFIED; the owner may flip it) | The proposal's list, plus a privateer port for each side. The French and Spanish arsenals are merchants, as the proposal says |
| 11 | Lisbon (neutral) sells to both sides. The knob `sells_in_war_to` is documented in its file and left unset | This is the owner's call. The truth sets the knob itself |
| 12 | Prices: £5 a barrel and £12 a ton of shot at home, £6 and £14 abroad. **UNVERIFIED** | The project's texts give no price |
| 13 | The roads rule applies at Plymouth only (Cawsand Bay or the Sound, never the Hamoaze). At Gibraltar powder is taken in anywhere | Art. VI lists the home roads only |
| 14 | The hoy is a port job, not a vessel (the lighter's precedent). Its timing goes by quantity: a fixed errand, then barrels and tons an hour, at least an hour | It draws nothing and adds no `vessels.serial` |
| 15 | While the galley fire is out it is **state**. The person's meal is cold, the crew's meals are counted cold, and the `stores` reading says so. No hardship and no physics follow. Clear for action's "The galley fire is out." stays a note | Owner's ruling: the needs read it. A cold dinner for one afternoon harms nobody |
| 16 | The empty barrels' shilling (Art. IX) is **said** in the stowed line as the gunner's own; nothing enters the purse | It is the gunner's perquisite, not the ship's |
| 17 | The cask is a lookout sighting with its own stream, `"practice"`. It is **never hailed**; it is said once when lost to sight and once when found again | The judges' graft. No existing draw moves |
| 18 | The cask's size term for the hit chance is √(1/40) ≈ 0.16, against the 0.5 floor that every hull under 10 m gets today | Today a 1 m cask would be hit as often as a 10 m hull |
| 19 | The notional mark is a cutter's 20 m, beam-on at any bearing. It may be laid from **one cable to the ship's longest random shot**, and the refusal names the gun | `Battery._fire` never fires beyond `random_m` (guns.py:499-506) |
| 20 | Dumb show: an empty gun runs its whole cycle and takes nothing. A **loaded gun is exercised from the run out to the point** and keeps its charge. `fire` at the word is refused while exercising; a gun fired by name still fires | Shotted guns are the usual state at sea, and they still get drill |
| 21 | `exercise the guns` is allowed at quarters before the guns are cast loose, so that the cycle starts empty | Douglas's words of command begin with "cast loose your guns" (from memory, UNVERIFIED) |
| 22 | "The mark" and "the target" mean the cask **only while one is in the water**. Empty words keep today's meaning | A rules captain's "her" can never pick a cask |
| 23 | The Regulations' allowance for exercise is a fourth of the upper-deck guns a month, the **first six months' figure**. It is written into the ship file as `exercise_charges` for King's fits only: frigate 6, brig 4, the cutter's carronades fit 1 | Art. XXI (l.13122-13144). The game keeps no commissioning date. The Captain's chapter (l.8842-8879) gives a third, and the note records it |
| 24 | A shotted gun fired with no mark logs **"the shot into the sea"**. "Across her bows" is kept for the order that says it. The fog-gun line of truth 7-147 changes its text and gains a `sea` key; no assertion moves | The proposal's §6 |
| 25 | The shot-fallback line is worded by calibre ("the 12-pounders") when two kinds of the fit share it. Its once-key stays `(pounder, charge)` | Shot is shared by calibre. The Renard's line stays byte-identical |
| 26 | Truth 7-161 pins **state and kinds, not a digest**. Its docstring records 311 lines and `a158a30ce39b345d` as this machine's measure | TuningNotes l.9859-9863: digests differ on this Windows machine |
| 27 | `heave a cask overboard` is refused at night and in a world with no chart | The cask could not be seen. A notional mark serves instead |
| 28 | The order verb is a **gunnery** verb, not an object-`none` evolution verb, so the side can be said | An object-`none` verb takes no words |
| 29 | Every vocabulary entry is written by the lead in stage 0. No builder edits `data/vocabulary.yaml` except to add a synonym inside its own section | That leaves no shared file to merge in practice |
| 30 | `api/action_readings.py` is entirely Builder 3's after stage 0 | Every Python file then has one owner |

---

## 1. Data shapes

### 1.1 The magazine (`freesail/ship/parts.py`, Builder 1)

The existing `Magazine` dataclass (parts.py:553-608) keeps its three `default_factory`
fields, and their names. Their **keys change shape** in layout 2. Every new field has a
plain, immutable default, so a magazine unpickled from packages 70-72 reads it as a class
attribute.

```python
BARREL_LB = 100.0      # Falconer 1780, French glossary, 'Baril de poudre' (l.22563-22564);
                       # the English barrel's weight UNVERIFIED
CHARGE_SHARE = {"long": 1 / 3, "carronade": 1 / 12, "swivel": 1 / 2}   # §2, UNVERIFIED
RESERVE_SHARE = 0.5    # the powder below at completion, of the filled powder (judgement)
FILL_S_BASE = 120.0    # man-seconds a cartridge, and 15 a pound of its charge (judgement)
FILL_S_PER_LB = 15.0
MAGAZINE_LAYOUT = 2

def charge_lb(kind: str, pounder: float) -> float          # to the ounce: round(x * 16) / 16
def fill_seconds(charge: float) -> float                     # FILL_S_BASE + FILL_S_PER_LB * charge
def split_by_kind(by_calibre: Mapping[float, int], guns: Iterable[Any]) -> dict[tuple[str, float], int]
def fit_levels(fit: FitSpec | None) -> dict[tuple[str, float], int]   # either key shape

@dataclass(frozen=True)
class Wanting:                       # never pickled
    powder_lb: float
    barrels: int                     # to the nearest whole barrel
    shot: dict[float, dict[str, int]]
    @property
    def empty(self) -> bool          # no barrel and no shot wanted

@dataclass
class Magazine:
    cartridges: dict = field(default_factory=dict)  # FILLED: {(kind, pounder): n}; layout 1 {pounder: n}
    shot: dict[float, dict[str, int]] = field(default_factory=dict)   # unchanged
    fired: dict = field(default_factory=dict)        # {(kind, pounder): n}; layout 1 {pounder: n}
    # practice and resupply: plain class defaults, so that a magazine pickled before them loads
    layout: int = 1
    level: dict | None = None        # {(kind, pounder): n}, the fit's filled allowance
    charges: dict | None = None      # {(kind, pounder): lb}
    shot_level: dict | None = None   # the fit's shot, {pounder: {kind: n}}
    reserve_lb: float = 0.0          # the barrels' establishment
    powder_lb: float = 0.0           # loose powder below, in the barrels
    short: bool = False              # cached: some kind below its level (the O(1) early-out)
    fill_s: float = 0.0              # man-seconds in hand toward the next cartridge
    filled_by_gunner: int = 0
    barrels_emptied: int = 0         # for the Ordnance's shilling (Art. IX)
    filling_held: bool = False       # `cease filling`
    report_filled: bool = False      # say `guns.filled` when back at the level (a receipt or the order)
    said_powder_out: bool = False
    account: tuple = ()              # ((when, words), ...): reassigned, never mutated
```

**Methods** (exact signatures):

| Method | What it does |
|---|---|
| `has(self, kind: str, pounder: float, charge: Charge) -> bool` | A filled cartridge of that kind and calibre, and the shot: two round for `DOUBLE`, none for `BLANK`, as today |
| `take(self, kind: str, pounder: float, charge: Charge) -> None` | As today, by `(kind, pounder)`. Counts `fired[(kind, pounder)]`, recomputes `short`, and raises `ValueError` as today |
| `filled_of(self, kind: str, pounder: float) -> int` | The filled count |
| `charge_of(self, kind: str, pounder: float) -> float` | The cartridge's powder: `charges`, else `charge_lb` |
| `can_fill(self, kind: str, pounder: float) -> bool` | `powder_lb` is at least the charge, and the filling is not held |
| `fill(self, man_seconds: float) -> list[tuple[str, float]]` | Banks the man-seconds and fills the neediest key: the lowest `filled/level`, ties in `GUN_KINDS` order and then the larger calibre. Each cartridge costs `fill_seconds(charge)` and takes its charge from `powder_lb`. A barrel emptied (`ceil` of the powder over 100 falls) adds to `barrels_emptied`. Returns the keys filled; logs and draws nothing. With nothing to fill, `fill_s` goes back to nought |
| `receive(self, powder_lb: float = 0.0, shot: Mapping[float, Mapping[str, int]] \| None = None, *, when: str = "", words: str = "") -> None` | The receipt as a transaction. It adds the powder and shot and enters `(when, words)` in the account when words are given. It sets `report_filled` and clears `said_powder_out`. Shot keys are floats |
| `wanting(self) -> Wanting` | The establishment is Σ level × charge plus `reserve_lb`, less what is held (Σ filled × charge plus `powder_lb`). Barrels are `int((deficit + 50) // 100)`. Shot is `shot_level` less what is held, never below nought |
| `spoil(self, share: float) -> int` | Unchanged in behaviour. It iterates the filled cartridges by key and leaves the barrels alone. `world/orders._fx_cartridges_damp` (orders.py:2972-2981) needs no edit |
| `describe(self) -> list[str]` | The reading's lines, below |
| `enter(self, when: str, words: str) -> None` | One line of the gunner's account |
| `account_lines(self, last: int = 12) -> list[str]` | The account's page |
| `return_barrels(self) -> int` | The barrels emptied, reset to nought |

`describe()` gives, for the long Tom:

- "Filled cartridges: 30 of 55 for the long 12-pounder, 220 of 220 for the 12-pounder carronades, 176 of 176 for the half-pounder swivels; the gunner filling for the long 12-pounder."
- "Powder below: 2 barrels and 40 pounds, of 3 barrels established."
- "Shot: 12-pounder 175 round, 30 grape, 20 chain; half-pounder 160 round."
- "149 rounds fired."

A ship with no guns keeps today's "The magazine is empty: she carries no powder." No test
pins these words (no test file mentions "magazine"; checked with grep).

**`magazine(ship)`** (parts.py:611-628) keeps its signature. A new store is built from
`fit_levels(fit)`, `fit.charges`, `fit.shot` and `fit.powder_barrels * BARREL_LB` (as both
`powder_lb` and `reserve_lb`), with `layout=2`. A stored `Magazine` with `layout <
MAGAZINE_LAYOUT` is converted once by `_convert_70(store, fit)`, which logs and draws
nothing:

1. It splits each calibre's `cartridges[p]` and `fired[p]` over the fit's gun kinds of that calibre, in proportion to their number of guns, by largest remainder with ties in `GUN_KINDS` order. The long Tom's 275 becomes 55 and 220; 100 becomes 20 and 80; 101 becomes 20 and 81.
2. It sets `level`, `charges` and `shot_level` from the fit. An old pickled `FitSpec` has float-keyed `cartridges`; `fit_levels` splits them the same way, and `charges` falls back to `charge_lb`.
3. It sets `powder_lb = 0.0` and `reserve_lb = fit.powder_barrels * BARREL_LB`. An old `FitSpec` reads the class default 0, so an old game has no reserve until she takes powder in. This goes in the tuning notes.
4. It sets `layout = 2` and recomputes `short`.

A ship with no fit gets `Magazine(layout=2)`. The docstring becomes "a function of the ship
file, the fit, the rounds fired, the gunner's filling and the ports' issues".

### 1.2 Schema, generator and ship files (Builder 1)

**`freesail/ship/schema.py`:**

- `FIT_KEYS = ("source", "guns", "cartridges", "charges", "powder_barrels", "exercise_charges", "shot")` (l.210).
- `FitSpec.cartridges: dict[tuple[str, float], int]` keeps its `default_factory`. New fields with plain defaults: `charges: dict[tuple[str, float], float] | None = None`, `powder_barrels: int = 0`, `exercise_charges: int = 0`.
- `_parse_fit` (l.753-793) reads `cartridges:` and `charges:` keyed by kind and then by calibre. It still accepts the old calibre-keyed `cartridges:` when exactly one kind of the fit has that calibre. Otherwise it refuses: "{source}: {where}'s cartridges of 12 are for guns of two kinds (long, carronade); say them by kind: cartridges: {long: {12: n}, carronade: {12: n}}." The calibre check at l.780-786 becomes a check by `(kind, calibre)`: "... holds cartridges for 12-pounder carronades, and no gun of that kind and calibre."
- `QUARTER_BILL_KEYS` (l.215) gains `"filling"`. `QuarterBillSpec.filling: int | None = None` is a plain default; None means it is reckoned as `max(1, great guns // 4)`. `_parse_quarter_bill` reads it with `_count`.

**`tools/gen_ships.py`:**

- `fit_magazine(guns, rounds_by_kind, exercise_charges=0)` (l.3465) returns a dict in the file's order: `cartridges` (by kind and calibre, the per-gun count unchanged at `int(round(total * 1.1))`), `charges`, `powder_barrels = ceil(RESERVE_SHARE * Σ n * charge / BARREL_LB)`, `exercise_charges` (written only when above nought) and `shot`.
- It imports `charge_lb`, `BARREL_LB` and `RESERVE_SHARE` from `freesail.ship.parts` lazily, as `cloth()` already does (l.348-352). There is no mirrored table.
- `Builder.armament` (l.760) takes fits as `(name, source, guns, magazine, note)`. Its callers at l.3666, 3778-3779, 3907, 3942, 4033 and 4101 follow.
- `Builder.quarter_bill(..., filling=None)` (l.785) writes `filling:` after `powder:` when given, with the note "the quarter gunners and the gunner's crew in the filling room, one to every four cannon (Falconer 1780, QUARTER-GUNNER); the swivels are not cannon".
- The annotation pass (l.925-952) gains a branch for notes on `cartridges:`, `charges:`, `powder_barrels:` and `exercise_charges:` at six spaces. The fit-name regex `^    ([^ :][^:]*):$` (l.946) cannot match them.

**What the files will hold:**

| Fit | Filled (kind calibre: n) | Filled powder | `powder_barrels` | `exercise_charges` | Bill `filling` |
|---|---|---|---|---|---|
| frigate-36 | long 18: 2054; carronade 32: 790; long 9: 316 | 15,395 lb | 77 | 6 | 10 |
| brig | carronade 32: 1264; long 6: 158 | 3,713 lb | 19 | 4 | 4 |
| cutter, carronades | carronade 12: 330 | 330 lb | 2 | 1 | 1 |
| cutter, long guns | long 3: 330; swivel 0.5: 352 | 418 lb | 3 | — | (1) |
| privateer, long tom | long 12: 55; carronade 12: 220; swivel 0.5: 176 | 484 lb | 3 | — | 1 |
| privateer, letter of marque | long 6: 330; swivel 0.5: 176 | 704 lb | 4 | — | (1) |
| merchant-brig | long 6: 104 | 208 lb | 2 | — | 1 |

The frigate's 40 great guns (26 long 18s, 10 carronades and 4 long 9s; 2054/79, 790/79
and 316/79) give 10 men. The compatibility design's 9 was an error. The exercise charges
take the frigate as a ship of one deck: 26 main-deck guns, a fourth, so 6 (judgement). The
cutter's long-guns fit (the revenue's and hired cutters') takes none.

The **regenerated** files are `frigate-36`, `cutter`, `brig`, `merchant-brig` and
`privateer-schooner`: their armament blocks, and one `filling:` line in each bill.
`topsail-schooner`, `lugger` and `smack` must come out byte-identical.

### 1.3 The port file's `ordnance:` block (Builder 2)

```yaml
ordnance:
  kind: ordnance                 # ordnance: the storekeeper, free and vouched to the King's ships
                                 # of the port's nation; merchants: at a price
  sells: false                   # an ordnance port: whether the town's merchants also sell
  roads: [outer_road, anchorage] # spot keys where powder is taken in; omitted: anywhere in port
  roads_words: Plymouth Sound or Cawsand Bay
  hoy_hours: 4                   # the demand and the hoy's errand (judgement)
  barrels_an_hour: 20            # the taking in (judgement)
  shot_tons_an_hour: 2
  powder_per_barrel_pounds: 5.0  # a sale's price (judgement, UNVERIFIED)
  shot_per_ton_pounds: 12.0
  # sells_in_war_to: [britain]   # a neutral's knob: a belligerent not listed is not served
  source: "Regulations 1806 (1808 printing), Gunner, Art. I l.12722-12737, Art. V l.12800-12809, Art. VI l.12833-12839"
```

- `Port.ordnance: dict[str, Any] | None = None` is a plain class default. `load_port` (ports.py:610-737) sets it from `ordnance.parse_block(doc.get("ordnance"), where)`, which refuses unknown keys in words.
- `ordnance.block_of(port)` reads `port.ordnance`. When `"ordnance" not in vars(port)` (a `Port` pickled before this build), it reads the block once from `port.path` and sets it. It returns None if the file is gone.

| Port | Block |
|---|---|
| plymouth | `kind: ordnance`, `sells: false`, roads `[outer_road, anchorage]` (Cawsand Bay, the Sound; the Hamoaze is the mooring), hoy 4 h |
| gibraltar | `kind: ordnance`, `sells: true` at £6 and £14, no roads key, hoy 3 h |
| falmouth, st-peter-port | `kind: merchants`, £5 and £12, hoy 3 h |
| brest, lorient, rochefort, st-malo | `kind: merchants`, £5 and £12, hoy 3 h |
| cadiz, ferrol, lisbon | `kind: merchants`, £6 and £14, hoy 3 h; Lisbon's file carries the commented knob |
| the other 27 | no block: "none to be had" |

### 1.4 The galley, the job and the paper (Builder 2)

- `Stores.galley_fire_out: str = ""` and `Stores.cold_meals: int = 0` (`world/places.py`, the `Stores` dataclass at l.510) are plain defaults. The value `"powder"` means the fire is out for the powder.
- The hoy is `Job(due, "ordnance", port.id, payload)`, keeping `Job`'s shape (ports.py:804-813). The payload is `{stage: "alongside" | "stowed", how: "issue" | "sale", necessity: bool, powder_lb: float, barrels: int, shot: {"12": {"round": n}}, cost: float, words: str}`. Calibre keys are strings so the event data stays plain JSON.
- `data/papers/papers.yaml` gains, **last**: `{handle: "the gunner's account", keeper: gunner, place: gunroom, source: magazine, words: "the powder below, the filled cartridges and the shot, with the receipts and the practice beyond the allowance"}`. `gunroom` is a `PLACES` id.

### 1.5 The marks (`freesail/combat/marks.py`, new; Builder 3)

```python
PRACTICE_PREFIX = "practice:"   # never 'mark:' (the director's), nor truth 7-135's bare 'mark',
                                # nor seen_as 'mark' (the lookout counts that as land)
CASK_LENGTH_M = 1.0
CASK_SIZE = math.sqrt(CASK_LENGTH_M / 40.0)   # 0.16: the size term without the hull's floor
CASK_HEIGHT_M = 2.0             # the flag on its staff
CASK_SEEN_DAY_NM = 1.0          # judgement; at twilight times chart.TWILIGHT_FACTOR; none by night
CASK_LEEWAY_SHARE = 0.02        # of the wind's base speed, to leeward (judgement)
CASK_LOST_NM = 3.0
NOTIONAL_LENGTH_M = 20.0        # a cutter's (judgement)

def is_mark(target_id: str | None) -> bool
def practice_of(ship: Any) -> Practice | None            # ship.extra.get("practice")
def drop_cask(world: Any, side: str) -> Cask
def lay_notional(world: Any, relative_deg: float, range_m: float, words: str) -> None
def target_of_mark(world: Any, target_id: str) -> Target | None
def sightings(world: Any, pos: Position, visibility_nm: float | None, daylight: str) -> list[Sighting]
def struck(battery: Any, gun: Any, target: Target, tick: int) -> list[str]
def count_live(world: Any, rounds: int) -> None
def tick(world: Any, battery: Any, tick: int, minute: bool) -> None

@dataclass
class Cask:                      # every field a plain default; a later field takes one too
    id: str
    position: Position
    dropped_tick: int
    gone: str = ""               # "", "struck", "lost", "abandoned"
    gone_tick: int | None = None
    gone_said: bool = False
    struck_by: str = ""
    struck_at_m: float = 0.0

@dataclass
class Practice:                  # ship.extra["practice"]; immutable defaults only
    cask: Cask | None = None
    notional: tuple[float, float, str] | None = None   # (relative deg, range m, words)
    serial: int = 0
    sight: str = ""              # "", "seen", "lost": the lookout's last say of the cask
    month: str = ""              # "1805-06"
    month_rounds: int = 0
    said_beyond: str = ""        # the month the allowance line was said
```

**`combat/action.target_of`** (action.py:102) gets one branch at its head, before
`world.position` is read: `if is_mark(target_id): return marks.target_of_mark(world,
target_id)`.

| | The cask (`practice:cask-N`) | The notional mark (`practice:notional`) |
|---|---|---|
| Bearing, range | The truth, `bearing_and_distance(world.position, cask.position)`. The gun captain lays by the truth, as for a ship | `ship.heading + relative`, the stated range; no position needed |
| Heading | Bearing + π/2: round, beam-on, so the aspect term is 1.0 | Bearing + π/2: beam-on at the bow and quarter too (the compatibility design's "the ship's heading" was beam-on only abeam) |
| Length, size | `CASK_LENGTH_M`, `CASK_SIZE` | `NOTIONAL_LENGTH_M`, None (today's term) |
| Body, world, nation | the `Cask`, None, None | None, None, None |
| Words, `mark` | "the cask", `"cask"` | "the mark four cables on the starboard beam", `"notional"` |
| None when | gone, or not among `world.lookout.sightings` | never |

`Target` (guns.py:185-200) gains `mark: str = ""` and `size: float | None = None` at its
end. It is rebuilt every tick and never pickled.

### 1.6 The battery: exercise and drill (`freesail/combat/guns.py`, Builder 1)

`Battery` is a plain class, so each new attribute is a class default that is reassigned on
the instance and never mutated at class level:

```python
class Battery:
    exercise: str | None = None          # "starboard" | "larboard" | "both": dumb show
    drill: dict | None = None            # gun id -> Drill, made at the first record
    last_practice_tick: int | None = None
    _dumb: list | None = None            # this minute's (gun id, seconds or None)
    _said_filling: set | None = None     # (kind, pounder) told "the gunner is filling"
    _said_out: set | None = None         # (kind, pounder) told "the magazine is out"
    # _said_no_powder (float keys) stays, unread: an old pickle's is inert

@dataclass
class Drill:            # new objects only; a field added later takes a plain default
    dumb: int = 0
    live: int = 0
    cycles: int = 0                  # full cycles timed, sponge (or a swivel's cartridge) to point
    total_s: float = 0.0
    best_s: float | None = None
    falls: dict[str, int] = field(default_factory=dict)   # "2 struck", "4 short": at marks
```

`Service` gains `began_tick: int | None = None`, and `Volley` gains `mark: str = ""` (both
plain defaults).

Methods, with exact signatures:

- `begin_exercise(self, side: str) -> list[str]`: sets `exercise`; returns the names of the loaded guns, which keep their charges.
- `end_exercise(self) -> None`: resets `run_out` and `primed` on the empty exercised guns and their services to `Service()`, then sets `exercise = None`.
- `exercise_line(self, tick: int) -> tuple[str, dict[str, Any]] | None`: this minute's dumb-show line; None when nothing completed.
- `drill_of(self, gun_id: str) -> Drill`.

### 1.7 The readings' rows

| Row | Owner | Rule |
|---|---|---|
| `magazine` (existing) | B3 (row), B1 (words) | Words from the new `describe()`. The row also rides while she is in port (`world.ports.in_port()`) and `not magazine(ship).wanting().empty` |
| `practice` (new; "the practice", "the exercise", "the gun drill"; kind `state`) | B3, `api/practice_readings.py` | Per gun: dumb, live, mean and best sponge to point. Falls at the mark by cables. The mark: kind, words, bearing, range in cables, in sight, gone. The month, for a King's ship with an allowance: rounds, allowance, beyond. The words are "none" when nothing has happened. **Idle in samples** unless she is exercising, a mark is engaged or a cask is in the water |
| `guns` (existing) | B3 | Words gain "exercising the starboard battery in dumb show"; the data gains `exercise` only while it is set |
| `stores` (existing) | B2 (`Stores.words`, `Stores.lines`) | Gains "the galley fire out while the powder comes aboard" only while set, and "N meals served cold" in the lines once any were |
| `port` (existing) | B2 (`Ports.port_words`, ports.py:2812) | Gains "the Ordnance's hoy coming off with her powder, alongside about 15:00" or "the hoy alongside, the powder coming aboard" only while an ordnance job is pending; the data gains `hoy` then only |

`idle_rows` (action_readings.py:58-86) becomes `_idle_action_rows(world) |
idle_practice_rows(world)`. The old body is renamed unchanged, so every early `return set()`
keeps its meaning for the action's and the squadron's rows, while `practice` is idled on
every path. There are no `hoy` or `galley` rows, because a new registry row rides in every
sample (`harness._sample_readings`, harness.py:1712-1722).

---

## 2. The charges

Table No. 29 ("A Table shewing the quantities of Gunpowder ...", regulations OCR
l.27498-27502) has lost its figures. Art. XVI (l.13025-13033) binds the gunner never to
exceed it. Until the table is read from the page image:

| Kind | Share of the shot's weight | Source |
|---|---|---|
| long | ⅓ | Falconer 1780, **CANNON** (from l.4037), quoting Robins at l.4826-4831: the "present allowance" is half the ball in the smaller pieces and seven-sixteenths in the 32-pounders, and one-third "or even less" would be an advantage. That the 1805 service charge was a third is from memory, **UNVERIFIED**. The CHARGE entry at l.5476 says only "See the article Cannon", so the two other designs' citation of CHARGE was wrong |
| carronade | 1/12 | From memory, **UNVERIFIED**. Falconer 1780 predates the carronade |
| swivel | ½ | Falconer's "smaller pieces" (l.4827), applied to a half-pounder: judgement |

| Gun | Charge | Fill, man-seconds |
|---|---|---|
| long 18 | 6 lb | 210 |
| long 12 | 4 lb | 180 |
| long 9 | 3 lb | 165 |
| long 6 | 2 lb | 150 |
| long 3 | 1 lb | 135 |
| carronade 32 | 2 lb 11 oz (2.6875) | 160 |
| carronade 12 | 1 lb | 135 |
| swivel ½ | 4 oz | 124 |

The cartridge counts are today's (§1.2). The code marks all three shares UNVERIFIED, and the
generator's note says package 75 replaces them from Table No. 29.

---

## 3. The orders, their words, and replay

### 3.1 Vocabulary (`data/vocabulary.yaml`, written in stage 0)

The port section, after `enter` (about l.921-924), under the comment "# powder and shot
taken in (docs/design/Build-PracticeAndResupply.md §5)":

```yaml
  take in powder and shot:
    synonyms: [complete the powder and shot, complete her powder and shot, complete powder and shot,
               demand powder and shot, indent for powder and shot, take in powder, take in shot,
               take in ammunition, complete the magazine, fill the magazine, complete the powder,
               complete the shot, demand powder, demand shot, indent for powder, indent for shot,
               buy powder and shot, buy powder, buy shot, purchase powder, purchase shot]
    object: port
    level: 1
```

The gunnery section, after `sail before guns` (about l.1440-1443), under "# practice at
the great guns, and the gunner's filling (Build-PracticeAndResupply.md §4, §6)":

```yaml
  heave a cask overboard:
    synonyms: [heave a cask overboard for a mark, heave over a mark, heave a mark overboard,
               put a cask over the side, put a mark over the side, drop a cask for a mark,
               drop a cask, drop a mark]
    object: gunnery
    level: 1
  exercise the guns:
    synonyms: [exercise the great guns, exercise great guns, exercise at the guns, exercise the battery,
               exercise both batteries, exercise the starboard battery, exercise the larboard battery,
               exercise the starboard guns, exercise the larboard guns, exercise in dumb show,
               exercise the guns in dumb show]
    object: gunnery
    level: 1
  cease exercising:
    synonyms: [cease the exercise, stop exercising, belay the exercise, end the exercise]
    object: gunnery
    level: 1
  fill cartridges:
    synonyms: [fill the cartridges, fill powder into cartridges, the gunner to fill cartridges]
    object: gunnery
    level: 1
  cease filling:
    synonyms: [stop filling, stop filling cartridges, cease filling cartridges, belay the filling]
    object: gunnery
    level: 1
```

`_match_verb` takes the longest phrase first (grammar.py:458-465), so these beat `take
in`, `demand`'s "indent for", `buy`, `heave` and `fill away`'s bare `fill`. No "throw"
synonym is given, because `throw` is a free-line verb. `standing/runtime.GUNNERY_PARTS`
(runtime.py:118) gains: `"heave a cask overboard": "the cask"`, `"exercise the guns"` and
`"cease exercising": "the exercise"`, `"fill cartridges"` and `"cease filling": "the
filling"`.

### 3.2 The supply's orders (Builder 2: `orders/ordnance.py` new, `world/ordnance.py` new)

**Routes in:**

- The verb `take in powder and shot`: `orders/port.execute` sends it to `ordnance_orders.execute(ship, order)`.
- `buy ...` and `demand ...` whose words `names_powder()` (whole words: powder, shot, ball, cartridge(s), ammunition): intercepted in `orders/port.execute` before the yard's and the market's branches. No market trades powder, so GATE_5C_MERCHANT's tin is untouched.
- "take in forty barrels of powder": `orders/__init__._stores_order` (l.274-290) gains a third branch after water and provisions, giving `Order(verb="take in powder and shot", verb_phrase="take in", object=rest)`.
- `port.check` (l.246-262) reads the same words for a standing order's action, through `ordnance_orders.check(ship, order)`.

**What is asked.** The verb phrase and the words together say powder, shot, or both; with
neither said, both. The words are read in this order:

1. "of necessity" and "of absolute necessity" are struck out as a flag.
2. Calibre and kind words are stripped before `numbers.number_in` (numbers.py:209), which takes the first number: "for the 12-pounders", "for the long 12", "for the carronades", "for the pivot gun", "for the long Tom", "for the swivels", "of 12 pounds".
3. Then the quantities: "N barrels of powder"; "N cartridges for <guns>" (as powder, N × charge, in whole barrels rounded up); "N round (grape, chain) shot for <guns>"; "N tons of shot for <guns>". With no number, the order completes to `Magazine.wanting()`.
4. Any quantity is cut to what `wanting()` leaves room for, with words ("the magazine has room for 12 barrels").

**Refusals, in this order** (the answer's kind is `ordnance.demanded`):

| # | Case | Words |
|---|---|---|
| 1 | No guns | "She carries no guns; there is no magazine to fill." |
| 2 | Not in port | "She is not in port: powder and shot are taken in at a port, of the Ordnance or a merchant." |
| 3 | Stance hostile or closed | "{Port} is {stance} to her; no powder will be issued or sold her." |
| 4 | No block | "There is no powder or shot to be had at {Port}: no storekeeper of the Ordnance, and no merchant who deals in it." |
| 5 | A hoy pending | "The hoy is coming off with her powder already; it will be alongside in {hours}." |
| 6 | Not a King's ship at an Ordnance port that does not sell | "The Ordnance's storekeeper at {Port} issues to the King's ships alone, and no merchant here sells powder." |
| 7 | A King's ship at merchants without the word | "There is no storekeeper of the Ordnance at {Port}, and a captain is charged not to purchase stores without an absolute necessity (the Regulations): say 'buy powder of necessity' to buy it of the merchants at £{price} a barrel." |
| 8 | Not at the roads (issue) | "Powder is taken in at {roads_words}, not in the harbour (the Regulations, the Gunner, Art. VI): weigh and bring her to the road first." |
| 9 | The knob | "{Port}'s merchants sell no powder to a {adjective} ship while the war lasts." |
| 10 | Complete | "Her magazine is complete: {the first line of describe()}." |
| 11 | Purse | "{words} costs {£} and the purse holds {purse}." (the yard's form, ports.py:3247-3250) |
| 12 | Cartridges for a gun she has not got | "She carries no 9-pounders; her calibres are 18, 32 and 9 ..." / "Shot for which guns? She carries ...: say 'take in 100 round shot for the 18-pounders'." |

An issue's answer reads: "Demanded 2 barrels of powder and 149 round shot of 12 pounds of
the Ordnance's storekeeper at Plymouth, issued and vouched; the hoy will be alongside in
four hours." A sale reads "... of the merchants at Falmouth for £14 10s, paid when it comes
alongside; ...". The words "powder hoy" and "gun wharf" are in none of the project's texts,
so they are not used.

### 3.3 The practice orders (Builder 3: `orders/gunnery.py`)

`execute` (gunnery.py:161-199) handles `heave a cask overboard`, `fill cartridges` and
`cease filling` **before** the quarters test, beside `strike the colours` and `cease
firing`. Everything else keeps the quarters refusal.

- **`heave a cask overboard`** ("from the starboard quarter"; the lee quarter by default, from the heel's sign) starts `runner.start(ship, "heave_mark", "her", {"side": side})`, as `heave_log` does (reckoning.py:2888-2904). A cask already in the water is abandoned (`practice.mark_lost`, ROUTINE). Refusals:
  - With no lookout: "The ship sails alone, with no chart: a cask over the side could not be seen. Say 'engage a mark four cables on the starboard beam'."
  - By night: "It is dark: a cask over the side would not be seen from the masthead; a notional mark serves by night ('engage a mark four cables on the starboard beam')."
- **`engage the cask` / `the mark` / `the target` to <side>.** The words are read before `_mark`'s "no sail in sight" refusals (gunnery.py:270-279). "The cask" is always the cask. "The mark" and "the target" mean the cask while one is in the water, and otherwise keep today's `_HER` meaning (l.127-136). Refusals:
  - "There is no cask in the water: say 'heave a cask overboard' first, or 'engage a mark four cables on the starboard beam'."
  - "The mark is not in sight from the masthead."
  - "The mark is knocked to pieces: heave another cask overboard for a mark."
  - The answer: "Engage the cask to starboard: the starboard battery, the guns to fire as they bear."
- **`engage a mark N cables on (off) the <side> <bow|beam|quarter>`.** It is parsed by `^(?:a|the)\s+(?:notional\s+)?mark\s+(.+?)\s+cables?\s+(?:on|off|broad on)\s+the\s+(starboard|larboard|port)\s+(bow|beam|quarter)$` **before `_side_of`** in both `_engage` and `check`, because `_side_of` raises on a bare "starboard" (l.229-234). Bow is 45°, beam 90°, quarter 135° (judgement); larboard is negative. The range runs from one cable to the ship's longest `random_m`. Beyond it: "No gun of hers carries ten cables: her long 18-pounders' random shot is 9.9 cables." Guns that do not reach are named in the answer ("her 12-pounder carronades do not carry four cables").
- **`exercise the guns`.** The side comes from the verb phrase and the words; with none said it is the engaged side, else both. It may be given before `cast loose the guns`.
  - Refusal while a ship (not a mark) is engaged: "She is engaged with {words}; the guns are not exercised in dumb show while an enemy is engaged."
  - The answer: "Exercise the starboard battery in dumb show: the guns served without powder, and no shot leaves the ship." With guns loaded it adds "; the 8 guns loaded keep their charges and are run out and pointed only". Before cast loose it adds " The guns are not yet cast loose: say 'cast loose the guns'."
- **`cease exercising`** calls `end_exercise()`. With none on: "The guns are not being exercised." Any `engage`, `secure the guns` (`SecureGunsScript.end_phase`, action_scripts.py:204-219, which also clears a mark target) and `strike()` (action.py:450) end the exercise too.
- **`fire`** (the broadside at the word, or a side) while exercising: "The battery is exercising in dumb show: no gun is fired at the word; say 'cease exercising' first." A gun fired by name, and the gun to leeward, fire as today.
- **`aim at`** with mark words (`fire at the mark` is an `aim at` synonym, vocabulary l.1405) keeps its refusal and adds: "to fire at the mark, say 'engage the mark to starboard' and 'fire'."
- **`fill cartridges`** clears `filling_held` and sets `report_filled`. The answer: "The gunner fills cartridges from the powder below: 181 of 330 for the 12-pounder carronades, 2 barrels below; by day, and at quarters with a man of the powder to spare." When already complete: "The cartridges are filled to the allowance already: ...". With no powder: "There is no powder below to fill: the filled cartridges are all she has."
- **`cease filling`** sets `filling_held`. The answer: "The gunner fills no more cartridges until he is ordered; the magazine shut." With none in hand: "The gunner is not filling."

Answer kinds: `evolution.started` (the heave), `guns.engage`, `guns.exercise`,
`guns.fill_order`. None collides with an event kind of §8's table.

### 3.4 Replay

Every new order is journaled and re-submitted at its tick by `core/replay`. Everything that
follows comes from pickled state and draws nothing:

- the jobs (`Ports.jobs`);
- the cask (`ship.extra["practice"]`, from the position at the heave);
- the filling (the magazine);
- the dumb show (the battery).

The cask's estimate draws from `"practice"`, opened lazily on the first cask sighting. No
scenario field is added, and `papers: {service: ...}` passes through the loader unvalidated
(scenarios.py:399). The rules fingerprint moves with the code, so replay across builds is
refused as for any package.

---

## 4. The gunner's filling (Builder 1: `freesail/combat/filling.py`, new)

`fill_tick(world: Any, battery: Battery, quarters: Any) -> None` is called once a minute
from `tick_action`'s minute block. Stage 0 adds the call with a no-op body; Builder 1 fills
the body in.

**When.** It returns at once (O(1)) in each of these cases:

- `not mag.short`, which covers every sailing passage and every full magazine;
- `mag.filling_held`;
- `ship.extra.get("struck")`;
- `getattr(world.stores, "galley_fire_out", "")`, while the magazine is open to the hoy;
- no man to fill.

Otherwise it calls `mag.fill(60.0 * men)`.

**Who.**

| Where | The party | Source |
|---|---|---|
| At quarters | The first `filling` men of `quarters.divisions[POWDER]`, in id order, that are fit with `at is None`. They are read, never reassigned | Art. XVIII (l.13065-13071) |
| Out of quarters, while `crew.bill.idlers_up(world.clock)` (06:00 to the dog watches' end) | `filling` men, notionally the gunner and his crew in the filling room. Nobody's `at` moves | Falconer, QUARTER-GUNNER |
| Out of quarters, otherwise | Nobody | Art. VII (l.12843-12850), judgement |

`filling` is the bill's figure. Where it is None (an old pickle or a hand-written file), it
is `max(1, great guns // 4)`, swivels excepted. The fillers' fatigue is left out (§10).

**In the battery** (`_charge_for` at guns.py:351-374, and `_work`'s cartridge phase at
l.400-420):

- `_charge_for` asks `mag.has(gun.kind, gun.pounder, want)`. On success it discards `(gun.pounder, want.value)` from `_fell_back`. The fallback line keeps its key, its kind `guns.magazine_empty`, and its data `{"pounder", "charge", "instead"}`. Its words name "the 12-pounders" when two kinds of the fit share the calibre, and `gun.kind_words` otherwise, as today.
- **The new path.** With no filled cartridge of the gun's kind and `mag.powder_lb >= mag.charge_of(kind, pounder)`, the gun **waits at the cartridge phase** with its phase and `left_s` kept and `stalled = "no cartridge"`. It says once per `(kind, pounder)` per outage, NOTABLE `guns.filling`: "No more filled cartridges for the 12-pounder carronades: the gunner is filling, and the guns wait on him." With the filling held, the words end "... the filling stopped by order; say 'fill cartridges'."
- **Today's path, unchanged.** With no powder either, `phase = -1`, the gun is sponged again, and "The gunner reports no more cartridges for the {kind_words}s: the magazine is out." is said with today's data `{"pounder", "charge"}`. Only its once-set becomes `_said_out`, keyed `(kind, pounder)`; a successful take discards the key.
- `fill_tick` discards a key from `_said_filling` once that kind is back at its level.

**Lines of its own**, each once per change of state:

- `guns.filled`, ROUTINE, only when `report_filled` is set (by a receipt or by `fill cartridges`) and the last kind comes back to its level out of quarters: "The gunner has the cartridges filled to the allowance: 330 for the 12-pounder carronades; 1 barrel and 31 pounds below." This clears `report_filled`.
- `guns.powder_out`, NOTABLE, when the powder below falls under the least charge while short: "The gunner reports all the powder filled: no loose powder below, and 40 cartridges short of the allowance."

**Why truths 7-133 to 7-160 do not move.**

1. The filled counts at the start are today's for every truth ship. No truth ship shares a calibre between kinds, so `has` and `take` decide the same on every tick.
2. The filling only ever adds cartridges, so `has` can differ only where today's would be False. Builder 1 first checks this on the local baseline: the action truths 7-133 to 7-160, run alone, give **no** "the magazine is out" line (the map measured 181 of 330 left for the King's cutter at the strike, and 205 of 330 for the Renard).
3. The filling draws nothing, moves no man, and says nothing at quarters. `guns.filled` needs `report_filled`, which no existing path sets. The beat's line, `Quarters.describe()`, the casualty order (hits.py:337) and the runner's borrowing are untouched.
4. `PHASES`, `NUMBERS_POWER`, the share floor and `hit_chance`'s default figures are unchanged, so 7-135 and 7-139 hold.
5. It costs O(1) a minute when full, and O(kinds) when short.

---

## 5. The supply (Builder 2)

**Service** (`freesail/world/service.py`, new, written complete in stage 0).
`service_of(world) -> str` returns `"kings"`, `"privateer"` or `"merchant"` from the first
of these that answers:

1. `scenario.papers["service"]`, read as `private_signals` is (signals.py:1313-1343);
2. the captain's role: kings-ship, cruiser or commodore give kings; privateer gives privateer; merchant, packet or fisherman give merchant;
3. `captains._is_kings_ship(world)` (captains.py:896-913);
4. otherwise merchant.

The first action's cutter comes out kings, by her role.

**Who gets what.**

| Ship | Ordnance port of her nation | Merchants (or an Ordnance port with `sells: true`) |
|---|---|---|
| King's | Issued, free and vouched; the roads rule applies; the purse is untouched | Refused unless "of necessity"; then bought, the line keeping "of absolute necessity, on the captain's word, for the Admiralty's account" |
| Privateer, merchant | Refused unless the port `sells` | Bought, subject to `sells_in_war_to`: a ship whose nation has an enemy (`nations.enemies_of`) and is not listed is refused |

The stance rule (`Ports.stance`, ports.py:927-930) is applied first, as the yard applies it.
**The roads rule**: `port.nearest_spot(world.position)[0]` (ports.py:555-562) must be one
of `getattr(port, k)` for `k` in `roads`.

**The two stages of the job.** `Ports._apply_job` (ports.py:3339-3435) gains one branch,
`elif job.kind == "ordnance": ordnance.apply_job(self, job, port)`. The yard's branch stays
byte-identical, which GATE_5C_CRUISE pins.

1. **Alongside**, at `hoy_hours`.
   - The job re-checks that `in_port()` is this port and, for an issue, the roads rule. If either fails, it logs NOTABLE `ordnance.missed`: "The hoy came off and found her gone from the road; it went back with the powder." Nothing is paid.
   - For a sale it calls `purse.pay(cost, "powder and shot of the merchants at {Port}", tick)` (places.py:493). If the purse is now short: "The merchants' hoy came alongside, but the purse holds £x against £y; it went back with the powder."
   - Then `stores.galley_fire_out = "powder"`, and NOTABLE `ordnance.alongside`: "The Ordnance's hoy is alongside with the powder: the galley fire is put out, no light allowed but in the light room, and no man to smoke (the Regulations, the Gunner, Art. V)." (l.12800-12809.)
   - The `stowed` job is queued at `max(1, barrels / barrels_an_hour + tons / shot_tons_an_hour)` hours.
2. **Stowed.**
   - If she has weighed, nothing is received and the fire is lit again.
   - Otherwise the job calls `magazine(ship).receive(powder_lb, shot, when=..., words=...)` and sets `galley_fire_out = ""`.
   - NOTABLE `ordnance.stowed`: "Two barrels of powder and 149 round shot of 12 pounds struck down and stowed, issued by the Ordnance's storekeeper and vouched; the magazine secured and the keys to the captain; the galley fire lit again." (l.12815-12827.) At an Ordnance port, after `return_barrels()`, it adds "the gunner returns three empty barrels to the storekeeper, a shilling apiece his own" (Art. IX, l.12887-12898).
   - Then ROUTINE `paper.written`: `papers.write("the gunner's account", done)`.

**The galley state, read.**

- In `NeedsKeeper.eat` (needs.py:547-574), when she is aboard and the fire is out, the hot branch becomes: "A cold meal, biscuit and cheese, the galley fire being out while the powder comes aboard; you eat {place}". `n.ate` and the easing are unchanged, and the answer is unlogged.
- In `victuals.serve` (victuals.py:221-262), each meal served while the fire is out adds one to `stores.cold_meals`. There is no line, and `_set_hardship` and the physics are unchanged.
- `Stores.words` and `Stores.lines` add the state only while it is set, so 7b-103 and 7b-104 hold.

**The paper** (`world/places.py`, `Papers` at l.629-809):

- `_lines` gains `source == "magazine"`: `describe() + account_lines()`, or "She carries no guns; the gunner keeps no account."
- `_keeper("gunner")` falls to the boatswain, the mate and then the master. The cutter has no gunner (data/people/cutter.yaml).
- `_entry`, on a miss, reloads `PAPERS_PATH` once and appends the handles the pickled catalogue lacks, then looks again. This mends a checkpoint with ten papers.

---

## 6. Practice (Builder 3, with Builder 1's battery)

**The cask.**

- `data/evolutions/heave_mark.yaml` carries every key an evolution file has (see `secure_guns.yaml`):
  - `id: heave_mark`, `verb: heave_mark`, `applies_to: {class: ship}`, `script: heave_mark`, `preconditions: []`, `timing: {heave_s: 60}`;
  - `on_start: {log: "Hands to the quarter: an empty cask over the side for a mark."}`;
  - `on_complete: {log: "The mark is over the side from the {side} quarter, an empty cask with a flag on a staff.", kind: practice.mark_over, severity: notable}`;
  - `on_fail`;
  - `crew: {hands: 2, rating: ordinary, stations: [afterguard, quarterdeck]}`;
  - `source`.
- `HeaveMarkScript(PhasedScript)` goes in `evolutions/action_scripts.py` and is registered in `ACTION_SCRIPTS` (l.294-299), which `scripts.py:8010-8012` merges, so `scripts.py` is untouched. It has `DEFAULTS = {"heave": 60.0}`, `holds() -> set()` and `holds_subject = False` (the boat's precedent, runner.py:709-717), so two hands at the quarter never hold her against a tack. Its `end_phase` calls `marks.drop_cask(world, side)` at `geo.destination(position, heading ± 135°, 0.6 × length)`. The cooper's casks are not counted.
- **Drift**, once a minute in `marks.tick`: the stream as `Vessel._stream` reads it (ships.py:843-850: `tide.stream_at(pos, greenwich_time(world))`), plus `CASK_LEEWAY_SHARE × world.wind.base_speed` to leeward of `wind.direction_from`, by `Position.advanced`. Nothing is drawn.
- **Its life.**
  - **Struck:** `hits.resolve_shot` (hits.py:111) gets a first branch, `if is_mark(target.id): return marks.struck(battery, gun, target, tick)`, before `body is None` and before `hasattr(body, "parts")`, which would reach `_far_hit`. `struck` sets `gone = "struck"` once and returns `[]`; a second hit in the tick returns `[]`. The notional mark returns `[]` and draws nothing. Then `marks.tick` logs NOTABLE `practice.mark_struck` once ("The mark struck by No. 3 starboard gun at two cables and knocked to staves; the guns hold their fire for want of a mark.") and clears `battery.target` and `target_words`.
  - **Lost:** beyond `CASK_LOST_NM` from the ship, ROUTINE `practice.mark_lost` ("The mark is lost astern, three miles off."), and the target is cleared.
  - **Abandoned:** at a new heave.
- **The lookout** (`world/lookout.py`):
  - `look()` (l.395-514) extends `found` with `marks.sightings(...)` after the vessels and sorts **only if any were added**. The feature is `Feature(cask.id, "cask", "the mark", lat, lon, modern=cask.id, height_m=CASK_HEIGHT_M)` and the sighting's `seen_as` is `"cask"`.
  - The range is the lesser of `CASK_SEEN_DAY_NM` and the visibility by day, that times `chart.TWILIGHT_FACTOR` at twilight, and nothing by night.
  - The hail loop at l.476-488 skips `seen_as == "cask"`, so the cask is never a `lookout.sighting` line.
  - `_judge` (l.516) takes the cask's estimate from `Lookout._practice_stream: random.Random | None = None` (a plain default), opened in `look()` as `rng.stream("practice")` when the first cask sighting is added.
  - `_closing`, `_sails`, `_land_ahead`, `land()` and `strangers()` skip it by kind. `reading()` lists it, and `find("the mark")` answers it.
  - `marks.tick` says ROUTINE `practice.mark_sight` once each way ("The mark is lost to sight in the haze." / "The mark is made out again, bearing ..., about three cables."), with `{"seen": bool}`. `Practice.sight` guards it, so the first sighting says nothing.

**Firing at a mark** (Builder 1, `_discharge` at guns.py:537-604):

- It keeps today's laying and today's two `rng.random()` draws.
- `S.hit_chance(..., size=getattr(target, "size", None))`. The new keyword in `combat/shot.py` (l.132) replaces the size term when given; the default None keeps every figure, so `far.py` and the ships are unchanged.
- For a mark it sets `last_practice_tick` and not `last_fired_tick`. So `_judge_morale`'s `engaged` (action.py:397) stays false, and morale skips marks with no edit there.
- It records no `opened_fire_at`. It writes `Volley(..., mark=target.mark)`, `drill_of(gun.id).live += 1` (in action too), and for a mark `falls[f"{cables} {outcome}"] += 1`.
- `tick_action` (Builder 3) calls `_fired_on` only for a target that `not is_mark(target.id)`; for a mark it calls `marks.count_live(world, rounds)` instead. So there is no `_recognition`, no `action.unrecognised`, no outlaw and no witnesses.
- `marks.tick(world, battery, tick, minute)` is called after the battery's tick, and returns at once with no `Practice`.

**The minute's words** (Builder 1, `minute_line` at guns.py:606-654):

- A struck volley at the cask reads "struck the mark"; at the notional mark, "on the mark".
- `data` gains `mark` only when the minute's volleys were at a mark.
- With no mark, a shotted gun's outcome is `"into the sea"`. `_discharge`'s rule: blank gives "blank"; `across_bows` gives "across her bows"; no target gives "into the sea".
- `minute_line` counts `sea`. When `n == sea` the line is "Fired one gun, the shot into the sea." When mixed, the fall list gains "N into the sea". `data` gains `sea` only when above nought.
- Any minute with no into-the-sea volley keeps today's code path exactly. (The determinism design's "One shot: ." came from an uncounted outcome; this counts it.)

**Dumb show** (Builder 1, `serving`, `wants_work`, `_work` and `_fire`):

- `serving()` reads the side from `exercise` when it is set; `wants_work()` is True for every exercised gun.
- An empty exercised gun starts at phase 0 with `began_tick = tick`. Its cartridge phase takes nothing (it branches before `_charge_for`). Shot, ram, run out, prime and point run by time.
- A loaded exercised gun starts at the run out (a swivel at the point) and keeps its charge.
- At the phases' end the cycle is recorded (`drill.dumb += 1`; a cycle begun at phase 0 is timed into `cycles`, `total_s` and `best_s`). Then `run_out = False`, `primed = False` if the gun is empty, and `phase = -1`.
- A live gun records its timed cycle at the same place.
- `_fire` fires the single guns as today, then returns while exercising, so no volley leaves the ship.
- `exercise_line` gives ROUTINE `practice.exercise`, never `action.fired`: "Exercising the starboard battery in dumb show: nine rounds in the minute, No. 3 starboard gun the quickest, a minute and twenty seconds from sponge to point." `tick_action` records it in the stage-0 line.

**Captains, the fighting book and morale skip marks by construction.**

- A mark is not in `world.vessels`, and its `seen_as` is not "sail". `Captain._mark` (captains.py:3657-3668) falls back to `_enemy_within`; `_enemy_struck` (l.3819-3825) finds no vessel; the far brains use the strangers.
- In `fighting.orders`, "open fire" and "long shot" apply to a cask through the `range` reading: the drill follows the book. "Return her fire", "she strikes" and "the colours" never fire, because a mark writes none of their kinds.
- Nothing in `captains.py`, `brains.py`, `morale.py` or the books is edited. If Builder 3's test finds a rules captain standing the guns down while a mark is engaged, it records the finding for the lead and does not fix it here.

**The allowance** (Art. XXI, l.13122-13144). For a King's ship (`service_of`) with
`fit_spec.exercise_charges > 0`, `count_live` adds to `month_rounds`, which resets when the
month changes. At the first round beyond the allowance in a month it logs NOTABLE
`practice.beyond_allowance` once: "Beyond the allowance for exercise this month (six
charges by the Regulations, the Gunner, Art. XXI): the powder past it is spent on the
captain's word, and the gunner's account keeps it." It then calls `mag.enter` and
`papers.write("the gunner's account", ...)`, the latter guarded with `except KeyError`
until Builder 2's paper is merged.

**The scenario.** `data/scenarios/exercising-the-great-guns.yaml`:

- the header in first-action's form, saying that under the rules captains with no model seated nothing happens;
- `seed: 7`, `start: 1805-06-14T09:00`, the position 49 52 N 5 12 W, `region: channel-west`, `nation: britain`;
- frigate-36, heading 180, 5 knots, `intent: cruise off the Lizard within 10 miles`;
- the wind from 280° at 10 knots, `gustiness: 0.0`, `variability: 0.0`;
- `ports: [falmouth, plymouth]`, both books, no `ships`, `orders: [set plain sail]`.

It must round-trip byte for byte (test_scenarios.py:133-143), carry no `weather_bound`
(7-158), and use LF line endings.

**The primer**, chapter 22 (Builder 3): a section "Practice at the great guns", with log
lines in plain blocks and no `orders` blocks, so `test_primer.CHAPTERS` stays as it is.
Builder 3 fixes the stale facts, verifying each by running the first action at seed 7:

- "12:06" → "11:12" at both l.104 and l.111;
- "eight shot holes" → "seven" at l.111;
- at l.62, the lee port's shutting (`shot.lee_port_shut` is never called) and "250 yards for a long gun", which is the 3-pounder's figure (the 18-pounder's is 380).

Chapter 14 (Builder 2) gains a section "Powder and shot", in prose and a table only, because
chapter 14 is in `CHAPTERS` and its `orders` blocks are run.

---

## 7. File ownership: three builders in three worktrees

### 7.1 Stage 0, by the lead on `main`, before the worktrees fork

One commit that changes no behaviour. It passes the fast tier and ruff, and the first
action still measures 311 lines and `a158a30ce39b345d` on this machine. It holds:

1. `combat/guns.py`: `Target.mark` and `Target.size`, `Volley.mark`, `Service.began_tick`, the `Drill` dataclass, the `Battery` class defaults of §1.6, and the stubs `begin_exercise` (sets `exercise`, returns `[]`), `end_exercise` (sets None), `exercise_line` (None) and `drill_of`.
2. `ship/parts.py`: the constants, `charge_lb`, `fill_seconds`, `split_by_kind`, `fit_levels`, `Wanting`, the new `Magazine` fields, and safe stubs: `filled_of`, `charge_of`, `can_fill` (False), `fill` (`[]`), `receive` (adds the powder and the shot), `wanting` (`Wanting(0.0, 0, {})`), `enter`, `account_lines` (`[]`), `return_barrels` (0). `has` and `take` keep today's signatures until Builder 1 changes them together with their callers.
3. `combat/filling.py`: `fill_tick`, a no-op. `combat/marks.py`: `PRACTICE_PREFIX`, `is_mark`, the dataclasses, and no-op stubs of every §1.5 function.
4. `combat/action.py`: at the end of `tick_action`'s minute block, after `_watch_struck`, two lines: record `battery.exercise_line(tick)` as ROUTINE `practice.exercise`, and call `filling.fill_tick(world, battery, quarters)`.
5. `world/service.py` complete, with `tests/test_service.py` (the four sources, the first action's cutter kings, the privateer privateer).
6. `api/practice_readings.py`: `register()` with the `practice` row (a stub function giving "none") and **every new event spec** of §8, and `idle_practice_rows` returning `{"practice"}`. Its import and register lines go at the end of `api/readings.py` (after the squadron block at l.4013-4015). `idle_rows` is split as §1.7 says, and the `magazine` row's description becomes "the magazine as the gunner counts it: filled cartridges by gun, the powder below and the shot".
7. `standing/runtime.py`: the `GUNNERY_PARTS` entries.
8. `data/vocabulary.yaml`: every entry of §3.1, the port block and the gunnery block about 500 unchanged lines apart.

### 7.2 Who owns what after the fork

| Builder | Owns (edits only these) |
|---|---|
| **1: the magazine and the gun deck** | `freesail/ship/parts.py`, `ship/schema.py`, `combat/guns.py`, `combat/shot.py`, `combat/filling.py`; `tools/gen_ships.py`; `data/ships/*.yaml` (regenerated only, never by hand); `tests/test_magazine.py`, `tests/test_filling.py`, `tests/test_dumb_show.py` (new); `tests/test_ship_particulars.py` (add `merchant-brig.yaml` to the comparison at l.560, after checking that it reproduces on the local baseline) |
| **2: the supply** | `freesail/world/ordnance.py`, `orders/ordnance.py` (new); `world/ports.py`, `orders/port.py`, `orders/__init__.py` (`_stores_order` only), `world/places.py`, `world/needs.py`, `crew/victuals.py`; `data/ports/*.yaml` (the 11 files of §1.3), `data/papers/papers.yaml`; `docs/primer/14-the-port.md`; `tests/test_ordnance.py`, `tests/test_powder_orders.py` (new); `tests/test_places.py` (l.149-161, 209, 230) and `tests/test_server.py` (l.532-543): ten papers become eleven |
| **3: practice** | `freesail/combat/marks.py`, `combat/action.py`, `combat/hits.py`, `world/lookout.py`, `orders/gunnery.py`, `evolutions/action_scripts.py`, `api/action_readings.py`, `api/practice_readings.py`; `data/evolutions/heave_mark.yaml`, `data/scenarios/exercising-the-great-guns.yaml`; `docs/primer/22-an-action.md`; `tests/test_practice.py`, `tests/test_practice_lookout.py`, `tests/test_practice_orders.py` (new) |
| **The lead, after the merge** | `tests/test_agents.py` l.1868 (87 evolutions → 88, from `heave_mark.yaml`; `data/evolutions` holds 87 files) and l.1870 (10 papers → 11). The two lines are too close for two branches to edit. Also `tests/conftest.py` `SLOW_TESTS` (one `# practice and resupply:` comment), `tests/test_known_truths.py`, `docs/dev/TuningNotes.md`, `docs/TechnicalSpec-M7.md` ("As built", Part 7-ii), `docs/agents/Harness.md` (the readings and the events), `docs/dev/M7-WorkPackages.md`, and the stale "truths 7-161 and 7-162" at `docs/design/Design-Squadrons.md:278` (built as 7-159 and 7-160) |

Nobody touches `crew/quarters.py`, `core/world.py`, `core/replay.py`, `world/orders.py`,
`world/captains.py`, `world/brains.py`, the books, the consent files or `BUILD_NAME`.

**The shared-file rule.** `data/vocabulary.yaml` is the only shared file. After stage 0, a
builder may only add a synonym inside its own block (Builder 2 the port block, Builder 3 the
gunnery block; Builder 1 none). The blocks are far apart, so git merges them as they stand.
Until the lead's step, Builder 2's worktree fails `test_agents.py:1870` and Builder 3's
fails `:1868`. That is expected and noted in each branch's message.

### 7.3 Interface contracts

| Provider | Contract the others may assume |
|---|---|
| Builder 1 | The §1.1 `Magazine` API and fields (`powder_lb`, `filling_held`, `report_filled`, `filled_by_gunner`). `fill_tick(world, battery, quarters)`. The §1.6 battery API, and that `Volley.mark` and `Drill.falls` are kept. `"struck"` is still the outcome that calls `resolve` for a mark `Target`. `hit_chance(..., size=None)`. `FitSpec.exercise_charges`. The kinds `guns.filling`, `guns.filled`, `guns.powder_out`, `practice.exercise`. Builder 1 reads `getattr(world.stores, "galley_fire_out", "")` and nothing else of the others |
| Builder 2 | `world.ordnance.block_of(port)` and `apply_job`; `Stores.galley_fire_out` and `cold_meals`; the paper "the gunner's account"; the kinds `ordnance.demanded`, `ordnance.alongside`, `ordnance.stowed`, `ordnance.missed`. It calls `receive`, `wanting`, `describe`, `account_lines`, `return_barrels` and `charge_of`, and tests against a `Magazine` subclass fake set in `ship.extra["magazine"]` with `layout=2` until Builder 1 is merged |
| Builder 3 | `marks.*` of §1.5; the `Target` it builds (`mark`, `size`, heading beam-on); the kinds `practice.mark_over`, `practice.mark_struck`, `practice.mark_lost`, `practice.mark_sight`, `practice.beyond_allowance`. It calls `begin_exercise`, `end_exercise`, `drill_of`, `magazine(ship).filling_held`, `report_filled`, `enter`, `wanting` and `service_of` |

**Merge order.** Builder 1, then Builder 2, then Builder 3. Each rebases onto the merged
`main`, runs the fast tier and its own files under `--slow`, and then merges.

---

## 8. Tests, events and the truths after the merge

**The events** (stage 0, `practice_readings.register`):

| Words | Kind |
|---|---|
| the gunner filling | `guns.filling` |
| the cartridges filled | `guns.filled` |
| the powder all filled | `guns.powder_out` |
| the hoy alongside | `ordnance.alongside` |
| the powder stowed | `ordnance.stowed` |
| the hoy turned back | `ordnance.missed` |
| the mark over the side | `practice.mark_over` |
| the mark struck | `practice.mark_struck` |
| the mark lost | `practice.mark_lost` |
| the mark lost to sight / the mark in sight again | `practice.mark_sight` (by `seen`) |
| the exercise | `practice.exercise` |
| beyond the allowance | `practice.beyond_allowance` |

### 8.1 Each builder's tests

- **Builder 1.**
  - `test_magazine.py`:
    - the charge table;
    - `has` and `take` by kind: the long Tom's carronades emptied leave the pivot's 55, and `DOUBLE` and `BLANK` behave as today;
    - `fill`'s order and pace, and the empty barrels;
    - `receive`, `wanting` (nearest barrel, capped) and `spoil`, by kind;
    - the conversion, with a `Magazine.__new__` holding a three-field float-keyed `__dict__` as in test_ground.py:386-409: 275 to 55 and 220, 100 to 20 and 80, 101 to 20 and 81; nothing logged, and `stream_names()` unchanged;
    - an old `FitSpec` and `QuarterBillSpec`;
    - the schema's two forms and its refusals;
    - the §1.2 table from the committed files;
    - the bill's `filling` equal to `max(1, cannon // 4)`.
  - `test_filling.py`:
    - the party at quarters, out of quarters by day, and none at night;
    - men read and never moved (every `at` equal before and after);
    - no filling while the hoy is alongside or when struck;
    - the wait at the cartridge phase, with its line once per outage;
    - today's "magazine is out" words and data on an empty magazine, and the line said again after a `receive`;
    - `guns.filled` only with `report_filled`;
    - a spy proving that `fill` is never called for a full magazine;
    - old `Battery` and `Service` objects built with `__new__`.
  - `test_dumb_show.py`:
    - nothing taken from the magazine and nothing discharged; `rounds_fired` unchanged; no `"gunnery"` stream opened;
    - a loaded gun exercised from the run out with its charge kept;
    - the timing and the drill;
    - the minute words at hand-built mark targets; "into the sea", and today's exact text with no sea volley;
    - `hit_chance(size=None)` equal to today's over a table of inputs;
    - `last_fired_tick` untouched by a shot at a mark.
- **Builder 2.**
  - `test_ordnance.py`:
    - the 11 blocks load, and an unknown key is refused;
    - the lazy block of an old `Port`;
    - every refusal of §3.2, word for word;
    - the roads at Plymouth by spot (Cawsand and the Sound pass, the Hamoaze fails);
    - the knob;
    - both job stages: missed, paid at alongside, short purse, stowed, the shilling, the paper;
    - an issue that moves nothing in the purse;
    - the merged catalogue of an old `Papers`;
    - the gunner's-account keeper falling to the boatswain in the cutter.
  - `test_powder_orders.py`:
    - the number and calibre forms;
    - the intercepts;
    - `take in twenty tons of water`, `take in provisions for thirty days` and `buy twenty tons of tin` giving the same kinds and texts as before;
    - `eat` cold with the fire out and today's exact words with it lit, `n.ate` equal either way;
    - `cold_meals` counted with no line;
    - `Stores.words` unchanged when lit.
- **Builder 3.**
  - `test_practice.py`:
    - `target_of` for both marks, and the beam-on aspect at 45° and 135°;
    - the `resolve_shot` branch, once and then `[]`;
    - no `_fired_on`, outlaw or `extra["morale"]` for a mark;
    - drift, loss and abandonment;
    - the reading, and `idle_rows` idling `practice` on every path;
    - the in-port `magazine` row;
    - the allowance line once a month.
  - `test_practice_lookout.py`:
    - the cask by day, at twilight, at night and in haze;
    - never hailed; the sight lines once each way;
    - `"practice"` opened only with a cask;
    - absent from `strangers()` and `land()`;
    - `find("the mark")`.
  - `test_practice_orders.py`:
    - every form in `execute` and `check`, and every refusal;
    - "the mark" meaning the cask only while one is out;
    - `secure the guns` ending the exercise and clearing a mark;
    - the heave not holding a tack;
    - `heave_mark.yaml` loading in the catalogue;
    - the scenario's round-trip and load;
    - a rules captain in the scenario with a cask engaged for 30 minutes.

### 8.2 The known truths to add (the last today is 7-160, at test_known_truths.py:9140)

The lead agrees these numbers with package 73, whose brief takes "the number after 72's".

| No. | The claim (the test's name) | What it pins |
|---|---|---|
| 7-161 | the first action is untouched by the magazine by kind, the filling and practice | 7-133's band (2700 to 10800 s from the first shot to the strike). No `guns.filling`, `guns.filled`, `guns.powder_out`, `practice.*` or `ordnance.*` kind in either log. `"practice"` not in `stream_names()`. The Renard's chain-fallback line with today's words and data keys (verify on the local baseline). The King's cutter's filled carronade cartridges equal 330 − fired + `filled_by_gunner`, and her powder equals 200 − `filled_by_gunner` lb. The docstring records 311 lines and `a158a30ce39b345d`, measured on the local baseline and on the merged tree, **not pinned** |
| 7-162 | the frigate knocks a cask to staves at two cables and nobody is made an outlaw | The cask placed by the test two cables abeam (as 7-134 places the cutter). `practice.mark_struck` once within a band of rounds that the builder measures and the lead narrows. The target cleared, and no `action.fired` two minutes after. No `action.unrecognised`, `action.false_colours`, `extra["outlaw"]`, `extra["morale"]` or `action.enemy_struck`. The 18-pounders' filled count equals 2054 − fired + `filled_by_gunner` |
| 7-163 | the shot at a mark tells more often at two cables than at four | A notional mark on the starboard beam, 20 minutes at each range. The share "on the mark" is higher at two. The practice reading's falls hold rows "2" and "4". This replaces the cask comparison the judges found ill-defined, since a struck cask ends a run |
| 7-164 | dumb show serves the guns at the action's pace and spends nothing | `exercise` given before `cast loose`. The 18-pounders' mean sponge-to-point within 7-135's band (90 to 125 s). The magazine identical to the start, `rounds_fired` 0, `"gunnery"` never opened, no `action.fired`, and `practice.exercise` each minute after the first cycle |
| 7-165 | a notional mark serves by night and in fog | At 02:00 and again in fog: "on the mark" in the minute line, `the range` exactly 4.0 cables, no sighting of a mark, and the heave refused by night in §3.3's words |
| 7-166 | a cask lost in the haze holds the guns' fire, is told once each way, and is given up at three miles | One `practice.mark_sight` each way, no round while unseen, firing resumed, then `practice.mark_lost` and the target cleared |
| 7-167 | in Plymouth Sound the King's cutter completes her magazine from the Ordnance free | Purse unchanged. Alongside at 4 h with the galley fire out, `eat` cold and `cold_meals` above nought. Stowed at 4 h plus the taking in (at least 1 h). The gunner's account written. `wanting()` empty once the gunner has filled by day. "The magazine is out" said again on a second emptying |
| 7-168 | powder is taken in at the road and not in the harbour, and bought only of necessity | The Hamoaze refused in Art. VI's words. Falmouth refusing the King's cutter, then "buy powder of necessity" charging the purse once at alongside. The merchant brig buying at Falmouth. The privateer refused at Plymouth. A French ship refused at Lisbon with the knob set on the loaded block |
| 7-169 | the long Tom fires on when the carronades' filled cartridges are spent | The schooner at a notional mark three cables on the starboard beam, the carronades' filled count set to four. The pivot never stalls; `guns.filling` once; the carronades fire again after the filling; the powder below falls by exactly the charges filled |
| 7-170 | a checkpoint taken with the hoy alongside resumes to the same digest, and the replay matches | Resumed equals uninterrupted; replay equals both |
| 7-171 | a practice forenoon is checkpointed and replayed | The scenario with the orders submitted by the test, a cask in the water at the checkpoint; resumed and replayed digests equal |

7-161, 7-167, 7-170 and 7-171 are likely to go into `SLOW_TESTS`. The lead measures them.

---

## 9. Pins expected to move, and the checkpoint and replay risks

**Known truths: none move.** That covers every sailing passage (gates 4c, 5a, 5b ×3, 5c
×2, 6a ×2), the five captain's trials, the consent digests and truths 7-133 to 7-160, for
§4's reasons. The three trials that already fail on this Windows machine (TuningNotes
l.9859-9863) stay the baseline. If any figure moves, bisect by turning items off one at a
time: the filling, the wait at the cartridge phase, the self-clearing sets, "into the
sea", the hit chance's keyword, and the lookout's extension.

**Unit pins that move, each with a comment naming this work:**

- `tests/test_places.py:149-161, 209, 230` and `tests/test_server.py:532-543`: eleven papers (Builder 2).
- `tests/test_agents.py:1868` (88 evolutions) and `:1870` (11 papers): the lead.
- `tests/test_ship_particulars.py:560`: one more file compared (Builder 1).

**Log text that changes with no assertion.** Truth 7-147's fog gun (`fire a gun to leeward`,
a shotted single gun with no target; orders/signals.py:750-757, guns.py:560-565) now logs
"Fired one gun, the shot into the sea." with a `sea` key, in place of "... across her bows,
a blank charge." Nothing pins it.

**Watch in the slow tier.** `errors.unknown_verb`'s hints (errors.py:104-130) could change
for a misspelling near a new verb; the first eight verbs are unchanged. `test_catalogue` and
`test_parity` must pass the new verbs and the evolution. `test_aboard_found.py:48` stays at
26.

| Risk | Mitigation |
|---|---|
| An old armed magazine (packages 70-72) | `layout` 1 is converted once in `magazine()`. The kept saves in `tests/fixtures/saves/` have no guns, so the `__new__` tests cover it |
| An old `FitSpec`, `QuarterBillSpec`, `Battery`, `Service`, `Volley`, `Lookout` or `Stores` | Plain class defaults only. `FitSpec.cartridges` float keys are split by `fit_levels` |
| An old `Port` or `Papers` | The block is read lazily from `port.path`; the catalogue is merged on a miss |
| A `default_factory` field on an existing class | None is added. `Drill.falls` is on a new class |
| Mutable class defaults | None. `Practice` and `Cask` hold immutable defaults; containers are made per instance and reassigned |
| An eager stream | `"practice"` is lazy. The filling, dumb show, drift and jobs draw nothing |
| A new key in an existing event's data | Only `sea` and `mark`, added only when used |
| Sample size | `practice` is idled on every path; no `hoy` or `galley` row is added. `magazine` rides in port only when short |
| An old game says a once-said magazine line once more | Documented in the tuning notes |
| An old game has no powder reserve | Documented; its establishment is the filled allowance alone |
| Pace | O(1) a minute when full. 7-138, 7-151, 7-159 and 7-160 are run on the merged tree, alone and last |
| Two suites at once on this machine (TuningNotes l.9864-9870) | One suite at a time, at two workers |

The lead's baseline before stage 0: the fast tier, and on the local baseline the first action's line
count and digest, plus the count of "the magazine is out" lines in 7-133 to 7-160.

---

## 10. What is left out, and why

- **Ship-to-ship transfer, and powder from prizes:** packages 74 and 82, by the owner's ruling.
- **Skill from practice:** the owner's ruling. The drill counts are kept for a later decision.
- **Table No. 29's figures, reduced and increased charges, and range by charge:** they need the page image, and `shot.py` is shared with `far.py`.
- **Quarter gunners and the gunner as posts:** a post shifts the muster's draws and every digest; package 75.
- **The fillers' fatigue, and filling by night out of quarters:** moving men would move evolutions.
- **A national arsenal's issue to French or Spanish warships:** no such ship does port business yet. The proposal makes those ports merchants.
- **Plymouth's town merchants:** UNVERIFIED; `sells: false` stands for the owner to flip.
- **Clear for action's galley fire as state:** nothing relights it (`extra["cleared"]` is never reset, action_scripts.py:116); a separate small decision.
- **The rest of the Regulations' powder rules:** the dry magazine (Art. IV), the sentinel, the keys and turning the barrels every three months (Art. X) are words in the lines only.
- **Gunfire heard and remarked:** new hearing code; for now the director voices it.
- **The broadside at the word in dumb show; drawing a loaded gun's charge; recovering the cask; points before or abaft the beam for the notional mark:** none is needed for a first build.
- **Arcs and reach for a gun fired by name; `lee_port_shut`; a captain whose magazine is out staying `engaging`:** carried in `Proposal-PivotGun.md` §5 for the lead; practice will meet the first.
- **The second six months' allowance:** it needs a commissioning date.
- **An `aboard:` row for the cooper's cask:** a free `aboard:` line already answers honestly, and the table stays at 26.
- **Powder's weight in the trim:** not in this build.
- **The hoy as a vessel, and any powder flag:** the hoy as a vessel is package 82's, and no period text here has a red flag.
