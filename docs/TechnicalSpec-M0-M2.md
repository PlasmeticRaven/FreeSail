# FreeSail Technical Specification: Milestones 0 to 2 (v0.1)

This document says how the first three milestones of `docs/DesignProposal.md` are built: precisely enough that a programmer, or a subagent, can start without further conversation, and plainly enough that the owner can check the sailing against it.

**Reading guide.** §1 to §4 are the shape of things and can be read by anyone. §5 to §10 are the detailed contracts (file formats, formulas, grammar) and can be skimmed by a non-programmer, except for the "known truths" tables, which are exactly where seamanship knowledge should be applied. §11 is the build plan.

**Milestones covered.**

- **M0. Skeleton and log.** A ticking, seeded, replayable core with an event log and a console. A point moving on a plane in a wind.
- **M1. One sail, one hull.** A hull and one square sail from data, apparent wind, sail force, resistance, leeway, helm. The imperative Orders dialect with a dozen verbs.
- **M2. Two rigs from data.** A ship-rigged vessel and a topsail schooner, both fully described in data files, with balance, strain, carrying-away, and a browser client with log, map and profile view.

Crew is milestone 3. Until then, orders change the ship through *nominal-duration evolutions* (§8.4): "set the fore topsail" takes a fixed, realistic time and then happens. M3 replaces the fixed time with the crew task system without changing anything else.

---

## 1. Principles that bind the code

1. **The simulation is a library.** `freesail.sim` has no idea whether a console, a browser, a test, or an LLM is driving it. It exposes: load a world, submit an order, advance one tick, read the log, query state.
2. **Determinism.** Same seed, same ship files, same sequence of `(tick, order)` pairs, same log. No wall-clock time, no unseeded randomness, no iteration over unordered containers where order affects results.
3. **Everything is an event.** Every state change that a person could notice produces a log entry. The log is the primary output; views are derived from it and from state queries.
4. **Rig-agnostic.** The code refers to part classes and roles (§6). If a function has the string `"main"` or the number `3` in it in reference to masts, it is wrong.
5. **Data before code.** Ship definitions, sail classes, evolutions and vocabulary are files under `data/`. The engine validates them loudly at load time.
6. **Nautical outward, SI inward.** Physics in metres, seconds, kilograms, newtons, radians. The log, the client and Orders speak knots, fathoms, feet, compass points, degrees and bells. Conversion happens in one module.

---

## 2. Repository layout

```
freesail/                   the Python package
  __init__.py
  units.py                  conversions, compass points, bells
  core/
    clock.py                ticks, ship's time, compression
    rng.py                  seeded named random streams
    events.py               Event, severity, the Log
    world.py                the World object: owns ships, wind, clock, log
    replay.py               save (seed + orders) and replay
  ship/
    schema.py               dataclasses for parts, validation
    loader.py               YAML -> Ship, alias and group tables, role links
    parts.py                Part, Spar, Sail, Line, Hull and their state machines
    graph.py                queries: "the yard of this sail", "sails on this mast"
  physics/
    wind.py                 true wind field, gusts, apparent wind
    sails.py                per-sail force from class curves
    hull.py                 resistance, sway, yaw, heel, rudder
    strain.py               loads, ratings, condition, carrying away
    integrate.py            the per-tick step, substeps
  orders/
    grammar.py              tokeniser and parser for the imperative dialect
    resolve.py              noun resolution against the ship (aliases, groups, sides)
    verbs.py                verb table -> evolution or level-0 action
    errors.py               nautical error messages
  evolutions/
    registry.py             loads data/evolutions/*.yaml
    runner.py               nominal-duration runner (M0-M2), replaced in M3
  api/
    queries.py              read-only state snapshots for views and agents
    session.py              a driving loop: submit, tick, stream
  ui/
    console.py              M0: prints the log, accepts orders on stdin
    server.py               M2: FastAPI app, websocket state stream, static files
client/                     M2 browser client: index.html, app.js, profile.js, map.js
data/
  sail_classes.yaml         force curves per class (§7.2)
  ships/
    frigate-36.yaml
    topsail-schooner.yaml
  evolutions/
    set_square_sail.yaml, take_in_square_sail.yaml, ...
  vocabulary.yaml           verbs, modifiers, compass points, common aliases
tests/
  test_determinism.py, test_replay.py, test_loader.py, test_grammar.py,
  test_known_truths.py, fixtures/
docs/
pyproject.toml              Python 3.12, deps: pyyaml, numpy, fastapi, uvicorn, pytest, ruff
README.md
```

Dependencies are deliberately few. No game engine, no ORM, no heavy validation framework; dataclasses and explicit checks.

**Running it.** `python -m freesail.ui.console data/ships/frigate-36.yaml` for M0/M1; `python -m freesail.ui.server data/ships/topsail-schooner.yaml` then open `http://localhost:8000` for M2.

---

## 3. Time, seeds, replay

### 3.1 The tick

- The simulation advances in **ticks of one game second**. `World.tick()` advances exactly one.
- Physics inside a tick runs **four substeps of 0.25 s** (semi-implicit Euler). Substeps are invisible outside `physics/`.
- **Compression** is a property of the driver, not the sim: the console or server calls `tick()` N times per real second. The sim never sleeps.
- The **ship's clock** starts at a date and time given in the scenario (default 1805-06-01 04:00 ship's time). Bells and watches are derived from it (§4.3).

### 3.2 Randomness

- `World` is created with an integer **seed**. All randomness comes from `core/rng.py`, which hands out **named streams** (`rng.stream("wind")`, `rng.stream("strain")`), each seeded from the master seed and its name. Adding a new consumer of randomness therefore does not perturb the others.
- Never call `random` or `numpy.random` directly.

### 3.3 The order journal and replay

- Every accepted order is journaled as `(tick, actor, text)`.
- A **save** is: engine version, seed, scenario reference, ship file content hashes, and the journal. It is a small JSON file.
- **Replay** rebuilds the world from the save and re-runs the ticks, re-submitting orders at their ticks. The resulting log must be byte-identical to the original. `tests/test_replay.py` asserts this.
- A **full state snapshot** is *not* the save format. Snapshots exist for views and debugging only.

---

## 4. Units, coordinates, conventions

### 4.1 Units

| Quantity | Internal | Displayed |
|---|---|---|
| Length | metres | feet, fathoms (6 ft), cables (~185 m), nautical miles (1852 m) |
| Speed | m/s | knots (0.5144 m/s) |
| Angle | radians | degrees; compass points (11.25°) where idiomatic |
| Mass | kg | tons (long ton, 1016 kg) |
| Force | newtons | not displayed in play; shown as "strain: light / heavy / dangerous" |
| Time | seconds | bells, watches, minutes |

`units.py` is the only place that converts.

### 4.2 Coordinates

- M0 to M2 use a **flat plane** in metres, `x` east, `y` north. Geography arrives in M5.
- **Heading** is the direction the bow points, radians clockwise from north, displayed in degrees true or as a compass point.
- **Wind direction** is *where the wind comes from* (a north wind blows from the north), as sailors say it. Internally, the wind *vector* points where the air moves; conversion is explicit and named to avoid the classic bug.
- **Tack** is the side the wind is on: wind from starboard means starboard tack.
- **Larboard** is the period word for the left side. `port` is accepted in Orders and echoed as larboard in the log.

### 4.3 Compass points and bells

- 32 points, named per Falconer ("south-west by west"). `units.py` carries the table both ways and "points" as an angle unit for helm orders ("come up two points").
- Watches: middle (00–04), morning (04–08), forenoon (08–12), afternoon (12–16), first dog (16–18), last dog (18–20), first (20–24). Bells every half hour, one to eight. The log stamps entries as `Forenoon watch, 3 bells (09:30)`.

---

## 5. Events and the log

### 5.1 The Event

```
Event
  tick        int            simulation tick
  ship_time   datetime       ship's clock
  severity    routine | notable | urgent
  kind        str            dotted, e.g. "order.accepted", "sail.set", "wind.shift", "spar.carried_away"
  text        str            the sentence in the log, written in log voice
  actor       str            "captain", "sim", "helm", "standing_order:<name>" (M4), "agent:<id>" (M4)
  subject     str | None     part id, ship id, or None
  data        dict           machine-readable details (numbers in SI)
```

The `text` is written for the ship's-log register: short, past tense, concrete. "Set the fore topsail." "Wind veered to WSW, freshening." "Main topgallant mast carried away; sail and yard hanging to leeward."

### 5.2 Severity rules

- **routine**: normal handling, minor wind changes, bells.
- **notable**: a completed evolution, a wind shift of more than two points, a squall, a sighting (M5), a part under dangerous strain.
- **urgent**: anything carried away, grounding (M5), missing stays, being taken aback, water rising.

Views may filter; the log itself keeps everything. At compression above 10x the console and client collapse consecutive routine entries into a one-line summary per bell.

### 5.3 Kinds needed by M2

`order.accepted`, `order.rejected`, `evolution.started`, `evolution.completed`, `evolution.failed`, `sail.set`, `sail.taken_in`, `sail.reefed`, `sail.reef_shaken_out`, `sail.backed`, `sail.blown_out`, `yard.braced`, `line.hauled`, `line.eased`, `line.parted`, `spar.carried_away`, `helm.order`, `helm.steady`, `ship.tacked`, `ship.missed_stays`, `ship.wore`, `ship.aback`, `wind.shift`, `wind.gust`, `clock.bell`, `strain.warning`.

---

## 6. The ship file and the part graph

### 6.1 Purpose

A ship file describes every part of a vessel and how the parts connect. The engine builds a graph from it, derives the Orders vocabulary from it, draws the profile from it, and runs physics over it. **The engine contains no ship.** Two files ship with M2: `frigate-36.yaml` (a 36-gun ship-rigged frigate) and `topsail-schooner.yaml`.

### 6.2 Format

YAML, one document. Top-level keys: `ship`, `hull`, `spars`, `sails`, `lines`, `groups`, `aliases`. Ids are dotted lower-case strings; the dots are for humans and have no meaning to the engine.

```yaml
ship:
  name: Speedwell
  rig: topsail-schooner          # a label; the engine does not branch on it
  era_notes: "Baltimore-built, 1804"

hull:
  length_waterline_m: 27.5
  beam_m: 7.3
  draught_m: 3.2
  displacement_kg: 190000
  gm_m: 1.0                       # metacentric height: stiffness
  clr_x_m: -0.4                   # centre of lateral resistance, +forward of midships
  lateral_area_m2: 75             # underwater profile area, for sway/yaw damping
  hull_speed_kn: 10.5             # optional; default 1.34*sqrt(LWL ft)
  rudder:
    area_m2: 2.2
    max_angle_deg: 35
    rate_deg_s: 4.0               # how fast the helm can be put over
  deck_height_m: 1.2              # freeboard at midships, for sail heights

spars:
  - id: fore.mast
    class: mast
    x_m: 7.5
    height_m: 17.0                # above deck
  - id: fore.topmast
    class: topmast
    steps_on: fore.mast
    height_m: 9.0
    rating_kn: 60                 # load rating in kilonewtons (see strain, §7.5)
  - id: fore.topsail.yard
    class: yard
    on: fore.topmast
    length_m: 11.0
    height_m: 19.5                # above deck when hoisted
    brace_limit_deg: 42           # sharpest it can be braced, from square
    rating_kn: 45
  - id: fore.gaff
    class: gaff
    on: fore.mast
    length_m: 7.0
    height_m: 15.0
  - id: fore.boom
    class: boom
    on: fore.mast
    length_m: 9.5
    height_m: 2.0
  # ... main mast, main gaff, main boom, bowsprit, jib-boom, etc.

sails:
  - id: fore.topsail
    class: square                 # one of the sail classes in data/sail_classes.yaml
    yard: fore.topsail.yard       # role link: the yard of this sail
    area_m2: 62
    reef_bands: 2
    x_m: 7.5
    centre_height_m: 16.0         # centre of effort above the waterline
  - id: fore.sail
    class: gaff
    mast: fore.mast
    gaff: fore.gaff
    boom: fore.boom               # omit for a loose-footed sail
    area_m2: 95
    reef_bands: 2
    x_m: 3.5
    centre_height_m: 8.0
  - id: jib
    class: jibheaded
    stay: fore.topmast.stay       # role link: the stay it hanks to
    area_m2: 40
    x_m: 13.0
    centre_height_m: 7.0

lines:
  - id: fore.topsail.halyard
    class: halyard
    of: fore.topsail.yard         # role: hoists this yard
    rating_kn: 35
  - id: fore.topsail.brace.starboard
    class: brace
    of: fore.topsail.yard
    side: starboard
    rating_kn: 25
  - id: fore.topsail.sheet.larboard
    class: sheet
    of: fore.topsail
    side: larboard
    rating_kn: 30
  - id: fore.sheet
    class: sheet
    of: fore.sail
    rating_kn: 30
  - id: fore.peak.halyard
    class: peak_halyard
    of: fore.gaff
  # clewlines, buntlines, tacks, throat halyard, downhauls, outhauls, lifts ...

groups:                           # plural nouns for Orders
  topsails: [fore.topsail]
  headsails: [jib, fore.staysail]
  fore-and-aft sails: [fore.sail, main.sail, jib, fore.staysail]

aliases:                          # anything a sailor might say
  "fore tops'l": fore.topsail
  "foresail": fore.sail
  "the fore": fore.sail
```

### 6.3 Part classes and roles

**Spar classes**: `mast`, `topmast`, `topgallant_mast`, `royal_mast`, `bowsprit`, `jib_boom`, `flying_jib_boom`, `yard`, `gaff`, `boom`, `studdingsail_boom`, `lug_yard`, `lateen_yard`, `sprit`.

**Sail classes** (each with a force curve in `data/sail_classes.yaml`, §7.2): `square`, `gaff`, `jibheaded`, `lug`, `lateen`, `sprit`, `studding`.

**Line classes**: `halyard`, `throat_halyard`, `peak_halyard`, `sheet`, `tack`, `brace`, `lift`, `clewline`, `buntline`, `leechline`, `bowline`, `reef_tackle`, `downhaul`, `outhaul`, `vang`, `guy`, `stay` (standing), `shroud` (standing), `backstay` (standing).

**Role links** are the `on:`, `steps_on:`, `yard:`, `mast:`, `gaff:`, `boom:`, `stay:`, `of:` keys. The loader turns them into a graph and `ship/graph.py` answers role questions:

- `yard_of(sail)`, `sail_of(yard)`, `halyard_of(spar)`, `braces_of(yard)`, `sheets_of(sail)`, `spar_chain(part)` (everything this part stands on, down to the hull), `dependents(part)` (everything that stands on or hangs from this part).

Evolutions and physics are written only in terms of these.

### 6.4 Validation (loader must reject)

- Unknown class; role link to a missing id; a sail whose class requires a role it lacks (a square sail without a yard, a gaff sail without a mast and gaff); a spar chain that does not reach the hull; a cycle in role links.
- Missing `rating_kn` on a spar or line the physics loads: warn and default from class tables, log it.
- Alias or group name that collides with a part id or a verb.

Errors are sentences, with the file and the id: `topsail-schooner.yaml: sail 'fore.topsail' is class 'square' but has no 'yard'.`

### 6.5 Derived vocabulary

At load, `orders/resolve.py` builds the noun table: every part id; every alias; every group; and **generated names**: for a part `fore.topsail`, the phrases "fore topsail", "the fore topsail", "fore tops'l" are generated by rule (dots to spaces, common contractions from `vocabulary.yaml`). Sides (`starboard`, `larboard`, `port`, `weather`, `lee`) attach to any line that has a `side`. "Weather" and "lee" resolve at parse time from the current tack.

---

## 7. Physics for M1 and M2

Everything here is per ship, per substep. Symbols: ρ_air = 1.225 kg/m³, ρ_water = 1025 kg/m³.

### 7.1 Wind

- **True wind** in M0 to M2 is a single field over the plane: a base direction and speed from the scenario, a slow random walk in both (stream `wind`), and **gusts**: multiplicative bursts of 1.1 to 1.5 on speed lasting 5 to 30 s, with a probability per tick set by a "gustiness" parameter. Vertical shear: speed at height *h* above water is `V(h) = V10 * (h/10)^0.11`, applied per sail at its centre height.
- **Apparent wind** at a sail: `V_app = V_true(h) - V_ship` (vectors). Its angle relative to the bow is the **apparent wind angle** (AWA), 0 ahead, positive to starboard.
- Wind shifts of more than two points since the last logged direction produce `wind.shift`.

### 7.2 Per-sail force

For each sail that is set (not furled, not in the gear, not blown out):

1. **Effective area** `A = area * reef_factor * cos(heel) * blanket`, where `reef_factor` is 1 minus a class-specific fraction per reef taken (square: 0.2 per band, gaff: 0.25 per band), and `blanket` is §7.3.
2. **Chord angle** `θ` relative to the centreline: for `square`, the yard's brace angle (0 = square, signed by which way it is braced); for `gaff`, `lug`, `lateen`, `sprit`, the sheet angle (0 = amidships, up to ~85° squared right off); for `jibheaded`, the sheet angle (5° to 30° typically); for `studding`, its parent yard's angle.
3. **Angle of attack** `α = AWA - θ` (wrapped to ±180°), with the sign giving which face the wind is on. A square sail with the wind on its fore face is **backed**: its thrust is negative and `sail.backed` is logged on the transition.
4. **Coefficients** from the class curve: `C_L(α)`, `C_D(α)`. Curves are piecewise-linear tables in `data/sail_classes.yaml`, symmetric in α, roughly: lift rising linearly to a peak of about 1.4 (square) or 1.6 (gaff, jibheaded) at α ≈ 25° to 30°, falling to about 0.6 by 60° and to 0 by 90°; drag from about 0.1 at 0° rising to about 1.2 at 90°. Square sails keep more lift at large α (they are run before the wind), fore-and-aft sails less. These are starting values to be tuned by the known-truths tests, not physics constants.
5. **Force**: `q = 0.5 * ρ_air * |V_app|² * A`; lift `L = q * C_L` perpendicular to the apparent wind; drag `D = q * C_D` along it. Resolve into ship axes: **thrust** (along the keel, forward positive) and **side force** (to leeward positive).
6. Record the sail's `|F|`, thrust, side force, its `x_m` and `centre_height_m` for balance, heel and strain.

### 7.3 Blanketing

A crude but honest rule: a sail that lies **downwind** of another sail on the same side, within a lateral band of that sail's height and within 3 mast-heights along the apparent wind, has its area reduced by 30% (square-to-square, running) or 15% (otherwise). Computed per substep from sail positions and heights projected along the apparent wind. This makes running dead before the wind under courses and topsails slower than with the wind a little on the quarter, which is a known truth.

### 7.4 Hull, motion, heel, helm

State per ship: position `(x, y)`, heading `ψ`, velocity in ship axes `(u, v)` (surge, sway), yaw rate `r`, heel `φ`, rudder angle `δ`.

- **Resistance (surge)**: `R = 0.5 * ρ_water * S_wet * C_f * u² * (1 + (u / u_hull)^4)`, where `S_wet` is estimated from LWL, beam and draught, `C_f` ≈ 0.004 and `u_hull` is the hull speed. The quartic term is a cheap stand-in for wave-making resistance and caps speed near hull speed.
- **Sway damping**: `Y = -0.5 * ρ_water * lateral_area * C_lat * v * |v|`, `C_lat` ≈ 1.0. Leeway is what results: side force from the sails pushes the hull sideways until damping balances it. Leeway angle `λ = atan2(v, u)` is logged when it changes by more than a degree.
- **Yaw**: moment `N = Σ (side_force_i * (x_i - clr_x)) + N_rudder - 0.5 * ρ_water * lateral_area * L² * C_yaw * r * |r|`, with rudder `N_rudder = -0.5 * ρ_water * A_rudder * C_r * (u² + small) * δ * x_rudder`. Yaw inertia from displacement and length.
- **Heel** (quasi-static): heeling moment `M_h = Σ side_force_i * centre_height_i`; righting moment `M_r = Δ * g * GM * sin(φ)`. Solve `φ` each substep by relaxing toward equilibrium with a time constant of about 4 s. Heel above 25° reduces `C_f`'s effective area exposure and above 40° logs `urgent` "on her beam ends" (M2 does not capsize; the log says it would).
- **Helm**: `steer <heading>` sets a target; a helmsman controller turns the rudder toward `δ = k_p * heading_error + k_d * r`, limited by `max_angle` and `rate_deg_s`. The steady rudder angle needed on a straight course is the **weather helm** reading, positive when the ship wants to round up. `helm.steady` logs when the ship settles within 2° of the ordered heading for 20 s.
- **Integration**: semi-implicit Euler at 0.25 s. Clamp `|v| ≤ 0.6 |u| + 0.5` to keep sway sane at low speed.

### 7.5 Strain and carrying away

- Every sail's `|F|` is a **load** on: its yard or gaff (full), the spar chain beneath (summed, each spar carrying everything above it), its sheets and halyard (a class-specific fraction: sheet 0.6, halyard 0.5, brace 0.3 per side), and its stays where applicable.
- Each loaded part has `rating_kn`. Define `ratio = load / rating`.
  - `ratio ≤ 1.0`: no effect. Condition recovers 0 (repair is M8).
  - `1.0 < ratio ≤ 1.5`: condition decays at `2 * (ratio - 1)` points per minute; `strain.warning` (notable) once per part per 10 minutes.
  - `ratio > 1.5`: each substep, the part carries away with probability `p = 0.002 * (ratio - 1.5)²` (stream `strain`); it also carries away deterministically if condition reaches 0.
- **Carrying away**: a **line** parts (`line.parted`): a halyard drops its yard (sail becomes "in the gear", not driving); a sheet frees its sail (sail flogs: area to 20%, load on the yard doubles, `urgent`); a brace lets the yard swing to the wind (θ follows AWA, no thrust). A **spar** carries away (`spar.carried_away`): it and all `dependents()` are marked `wrecked`, their sails give no force, and the wreck adds drag equal to a furled sail's windage times 3 until cleared (M8). The event text names what went and what hangs where.
- **Blown out**: a set sail with `ratio > 1.8` against its own cloth rating blows out (`sail.blown_out`): no force, and it must be shifted (M8). Cloth rating derives from area and a class constant.

### 7.6 Known truths (acceptance tests for physics)

Each is a pytest in `tests/test_known_truths.py`, run against the M2 reference ships with a steady 15-knot wind unless stated. Targets are ranges; a failing test means "retune curves", not "change the test", unless the owner agrees the truth is wrong. Sources are the references in `docs/references/`.

| # | Truth | Test |
|---|---|---|
| 1 | A ship-rigged vessel close-hauled lies about six points off the true wind, five and a half at best | Set all plain sail, brace sharp up, steer up until speed falls below 3 kn: the best sustained course is 62° to 72° off the true wind. (Luce XXIV, "Tacking") |
| 2 | A topsail schooner points higher than the frigate | Same test: best course 50° to 62° |
| 3 | Beam reach is the fastest point for the frigate; broad reach for the schooner | Sweep AWA in 10° steps; the max-speed point lies where stated, ±15° |
| 4 | Frigate under plain sail on a beam reach in 15 kn makes 7 to 9 kn; in 25 kn, 10 to 12 kn | Speed after 10 minutes steady |
| 5 | Dead before the wind is slower than four points off it | Compare speeds at 180° and 135° AWA under courses and topsails |
| 6 | Taking in the headsails gives weather helm; setting them and taking in the spanker gives lee helm | Steady rudder angle sign changes as stated on a beam reach |
| 7 | Leeway is 3° to 6° close-hauled, near zero running | `λ` in those ranges |
| 8 | Heel under plain sail on a beam reach in 15 kn is 5° to 10°; in 30 kn without shortening sail, 20°+ and topgallant masts under dangerous strain | Heel ranges; `strain.warning` on topgallant masts within 5 min |
| 9 | Carrying royals and topgallants in a 35-knot wind on a reach carries something away within 20 minutes | At least one `spar.carried_away` or `sail.blown_out`; and *nothing* carries away in 20 kn under plain sail |
| 10 | Tacking: frigate takes 5 to 10 minutes and gains to windward; loses way and misses stays if put about at under 3 kn | `ship.tacked` within range; `ship.missed_stays` in the slow case (§8.5) |
| 11 | Wearing loses a quarter to half a mile to leeward and takes 6 to 12 minutes for the frigate | Distance downwind between start and steady on the new tack |
| 12 | Backing the main topsail with the fore yards full stops the ship (heave to) | Speed under 1.5 kn within 5 minutes, heading steady within ±15° |
| 13 | A gaff sail with the sheet eased to 45° on a run gives less thrust than at 70° | Compare thrust; encodes that fore-and-aft sails want to be squared off downwind |
| 14 | Studding sails add 15% to 30% to speed on a broad reach in 10 kn and nothing useful close-hauled | Speed with and without |
| 15 | Determinism: two runs of any of the above with the same seed produce identical logs | Hash compare |

The owner should read this table with a seaman's eye and add or correct entries; it is the contract that keeps the physics honest.

---

## 8. Orders: the imperative dialect (M1, M2)

The standing dialect is M4. What follows is the whole of the imperative dialect.

### 8.1 Grammar

```
order       := verb_phrase [ object ] { modifier } [ "," side ]
verb_phrase := one of the verb table entries (multi-word allowed)
object      := [ "the" ] noun [ side_word ]
noun        := part-name | alias | group-name | "yards" | "sail" | "all sail" | "plain sail"
side_word   := "starboard" | "larboard" | "port" | "weather" | "lee" | "both sides"
modifier    := "sharp up" | "square" | "in" | "up"
             | "on the" tack_word "tack"
             | count "reef" | count "reefs" | "close"
             | "a fathom" | count "fathoms" | "a little" | "handsomely" | "roundly"
             | "to" heading | heading
heading     := number ["degrees"] | compass-point | count "point"/"points" ("up" | "off" | "to starboard" | "to larboard")
count       := "one" | "two" | ... | "eight" | digits
tack_word   := "starboard" | "larboard" | "port"
```

Case-insensitive. Punctuation ignored except the comma. Numbers as words or digits. Unknown words are reported with the nearest known ones.

### 8.2 Verb table for M2

| Verb (and synonyms) | Object | Level | Effect |
|---|---|---|---|
| `set`, `make sail on`, `loose and set` | sail or group | 1 | evolution `set_<class>` |
| `take in`, `clew up`, `haul down` | sail or group | 1 | evolution `take_in_<class>` |
| `furl` | sail or group | 1 | evolution `furl` (after take in) |
| `reef` [n reefs, close] | sail or group | 1 | evolution `reef_<class>` |
| `shake out` [n reefs] | sail or group | 1 | evolution `shake_out` |
| `brace` [sharp up, up, in, square] [the X yards] [on the T tack] | yards | 1 | evolution `brace` toward the given angle: sharp up = `brace_limit`, up = 30°, in = 15°, square = 0° |
| `haul`, `ease`, `let go`, `belay`, `check` | a line | 0 | direct: haul/ease shift the line's controlled angle by 5° (brace, sheet) or its hoist by 10% (halyard); let go frees it; belay stops an in-progress haul |
| `steer` heading | | 1 | helm target |
| `come up`, `luff` [n points] | | 1 | helm target shifts toward the wind |
| `bear away`, `keep away`, `bear up` [n points] | | 1 | helm target shifts away |
| `keep her full`, `full and by` | | 1 | helm target = current best close-hauled angle + 5° |
| `tack ship`, `ready about`, `go about` | | 1 | evolution `tack` (§8.5) |
| `wear ship` | | 1 | evolution `wear` |
| `heave to` [on the T tack] | | 1 | evolution `heave_to` (M2 simplified: back the after topsail) |
| `fill away`, `fill` | | 1 | undo heave to |
| `set plain sail`, `make all sail`, `shorten sail` | | 1 | group evolutions from `vocabulary.yaml` |
| `hold`, `pause`; `go`, `resume`; `time` n | | driver | console and client control, not journaled as ship orders |

### 8.3 Resolution rules

- An object that names a **group** expands to its members; the order becomes one evolution per member, started together.
- `weather` and `lee` resolve using the current tack at parse time and are recorded resolved in the journal ("haul the weather main brace" is journaled as the starboard brace on a starboard tack, so replay is unambiguous).
- A `side` on an order about a sail with sided lines (studding sails, braces) selects the side; `both sides` selects both.
- Ambiguity ("set the topsail" on a ship with three topsails) is rejected with the candidates listed. Rejections are `order.rejected` events, `routine`, with the message; nothing else happens.
- An order for a part in a state where the verb is meaningless (set a sail already set; brace a gaff) is rejected with a nautical reason.

### 8.4 Nominal-duration evolutions (M0 to M2)

`data/evolutions/*.yaml` entries in M2 have this shape:

```yaml
id: set_square_sail
verb: set
applies_to: {class: square}
preconditions:
  - sail.state in [furled, in_the_gear]
  - yard_of(sail).state == crossed
  - not wrecked(spar_chain(sail))
steps:
  - {do: loose,       duration_s: 90,  sets: {sail.state: loosed}}
  - {do: sheet_home,  duration_s: 60,  sets: {sail.state: sheeted}}
  - {do: hoist,       duration_s: 120, sets: {sail.state: set}, via: halyard_of(yard_of(sail))}
on_complete: {log: "Set the {sail}.", kind: sail.set, severity: notable}
on_fail:     {log: "Could not set the {sail}: {reason}.", kind: evolution.failed}
crew: {hands: 12, rating: ordinary}     # ignored until M3, but authored now
source: "Luce 1866, ch. XXIII At sea, 'Topsails'"
```

The M2 runner walks steps in order, each taking `duration_s` ticks scaled by a **weather factor** (1.0 in light airs, up to 2.0 in 30 kn and 25° heel), then applying `sets`. Preconditions are checked at start and at each step; a failed check fails the evolution with the reason. Two evolutions that would set the same part's state at once are serialised: the second waits.

The M3 task system replaces `duration_s` with crew-derived durations and adds the hands. Nothing else in the file changes, which is why the crew line is authored now.

Evolutions required for M2: `set_square`, `take_in_square`, `furl_square`, `reef_square`, `shake_out_square`, `set_gaff`, `take_in_gaff`, `reef_gaff`, `shake_out_gaff`, `set_jibheaded`, `take_in_jibheaded`, `set_studding`, `take_in_studding`, `brace`, `tack`, `wear`, `heave_to`, `fill_away`. Group orders (`set plain sail`) are lists of these in `vocabulary.yaml`.

### 8.5 Tack and wear in M2

Without crew these are scripted sequences that manipulate helm and yards on a timeline, which is faithful enough to Luce XXIV to be tested:

**Tack**: precondition speed ≥ 2 kn and close-hauled within 10°. Steps: helm down (target heading = through the wind by 12 points from current); when head is within 1 point of the wind, "mainsail haul": after yards braced to the new tack (instantly for M2, 45 s duration); if the head passes through the wind, "let go and haul": head yards braced (45 s); steady on new course; `ship.tacked`. **Missing stays**: if speed falls below 0.8 kn before the head passes the wind, the ship stops, falls back on the old tack, `ship.missed_stays` (urgent), and the evolution ends with the yards squared for a wear.

**Wear**: bear away until running, brace yards round progressively as the wind comes aft then onto the new quarter, then come up to the new close-hauled course. Total 6 to 12 minutes for the frigate is the truth to hit.

**Heave to** (M2 simplified): brace the aftermost square yard aback with the others full, helm a-lee. The physics does the rest (truth 12).

---

### 8.6 The living grammar

The verb table in §8.2 was the milestone 1 target. After the Sailing Master's Primer (`docs/primer/`) was written against it, the parser was extended (package 15) with the period orders the primer reached for: `square`, `back` and `lay ... aback`, `trim`, `brace round` and `brace ... to the wind`, class-bound take-in words (`haul up`, `brail up`, `clew up`, `haul down`, `lower`), `sheet home` and the `home`/`aft` modifiers, the conning words as helm orders (`steady`, `meet her`, `right the helm`, `hard a-lee`, `helm a-weather`, `nothing off`, `no higher`, `bring her by the wind`), compound objects joined by `and`, `close`/`double`/`single reef`, plural sided lines, `gybe` as a synonym of `wear ship`, and half-point helm orders. From here on the authoritative description of what parses is `data/vocabulary.yaml` together with the primer, whose every order block is run through the parser by `tests/test_primer.py`; this section is not maintained verb by verb.

## 9. The console (M0) and the browser client (M2)

### 9.1 Console

`freesail.ui.console` runs the world at a chosen compression, prints log entries as they occur, and reads orders from stdin. Driver commands: `hold`, `go`, `time 30` (30x), `tick 600` (advance 600 ticks then hold), `state` (a one-screen summary: heading, speed, leeway, heel, wind true and apparent, helm, sails set), `save <file>`, `replay <file>`. That is all M0 needs and it remains useful forever for tests.

### 9.2 Server

`freesail.ui.server` is a FastAPI app:

- `GET /` serves `client/index.html`.
- `GET /api/ship` returns the loaded ship's part graph as JSON (for drawing).
- `GET /api/state` returns the current snapshot (§9.4).
- `POST /api/order` `{text}` submits an order; returns the accepted/rejected event.
- `POST /api/driver` `{action: hold|go|time, value}`.
- `WS /ws` streams: every log event as it happens, and a state snapshot every tick at 1x, every 10 ticks at 10x, every 60 at 60x and above.

### 9.3 Client

Plain HTML, CSS and JavaScript, no framework, no build step: `client/index.html` loads `app.js`, `profile.js`, `map.js`.

- **Log panel**: scrolling, severity-coloured, filter by severity, collapsing routine entries at high compression. A command line beneath it with history.
- **Instruments**: heading, speed, leeway, heel, true and apparent wind, helm angle, ship's time and bell, compression.
- **Profile view** (`profile.js`): an SVG side elevation built from `/api/ship`. Hull as a simple shape from LWL, freeboard and sheer; each spar drawn at its `x_m`, `height_m`, `length_m`; each sail as a polygon between its spars sized by area and class, filled by state (furled: a bundle on the yard; set: full; reefed: shortened; backed: shaded; blown out: torn outline; wrecked spar: dashed and drooping). Studding sails extend outboard of their yards. The figure is schematic, but it is *true* to the part graph and it is rig-agnostic: it draws whatever the file says.
- **Map view** (`map.js`): canvas, north up, the ship as a small hull symbol with heading, its track for the last hour, a wind arrow, a scale bar. Nothing else until M5.

### 9.4 State snapshot

```
{
  tick, ship_time, bell,
  ship: {x, y, heading, speed_through_water, leeway, heel, rudder, weather_helm},
  wind: {true_from, true_speed, apparent_angle, apparent_speed},
  sails: [{id, class, state, reefs, area_effective, thrust, side, strain_ratio}],
  spars: [{id, class, state, condition, strain_ratio}],
  lines: [{id, class, state, strain_ratio}],
  evolutions_in_progress: [{id, subject, step, remaining_s}]
}
```

Numbers in the snapshot are SI; the client converts for display using a small table mirroring `units.py`.

---

## 10. Tests and quality gates

- `pytest` runs in under a minute for M0 to M2. Physics truths run ten-minute game scenarios at full speed, which is a few seconds each.
- `ruff` for lint and format.
- **Determinism** and **replay** tests run on every reference ship.
- **Loader** tests: each reference ship loads; each validation rule has a failing fixture.
- **Grammar** tests: a table of a hundred orders and their expected parse or rejection, including period phrasings and misspellings.
- **Known truths** as in §7.6.
- A milestone is done when its acceptance list (§11) passes, the checks pass on GitHub's machine, and the owner has passed its **gate** (§11.4).

---

## 11. Build plan and work packages

### 11.1 Milestone acceptance

**M0 done when**: `console` runs a world with a seed; a "ship" that is a point with a heading and a speed order moves in a wind; the log prints bells and wind shifts; `save` then `replay` produces an identical log; determinism test passes.

**M1 done when**: `frigate-36.yaml` loads with a hull and *one* square sail (the main topsail; the rest of the file may exist but is not required); apparent wind, sail force, resistance, sway and helm work; the imperative grammar parses the set/take in/brace/steer/haul/ease verbs against that sail; truths 1 (loosely), 4, 7 pass for one sail with adjusted targets; the console shows `state`.

**M2 done when**: both reference ships load with complete sail plans and rigging; all sail classes present on those ships produce force; balance, heel, blanketing, strain and carrying away work; tack, wear and heave to work; all fifteen truths pass; the browser client shows log, instruments, profile and map for either ship and accepts orders; replay works through the server.

### 11.2 Work packages

Each package is self-contained enough to hand to a subagent with this document and the proposal. Dependencies are stated; packages on the same row can run in parallel.

| WP | Name | Builds | Depends on | Milestone |
|---|---|---|---|---|
| 0 | Scaffold | `pyproject.toml`, package skeleton, `ruff`, `pytest`, README run instructions | | M0 |
| 1 | Core | `units.py`, `core/clock.py`, `core/rng.py`, `core/events.py`, `core/world.py`, `core/replay.py` and their tests | 0 | M0 |
| 2 | Console | `ui/console.py` with driver commands, using a stub point-ship | 1 | M0 |
| 3 | Ship schema and loader | `ship/schema.py`, `loader.py`, `parts.py`, `graph.py`, validation, fixtures, tests; `sail_classes.yaml` skeleton | 1 | M1 |
| 4 | Wind and sail physics | `physics/wind.py`, `physics/sails.py`, class curves | 1, 3 | M1 |
| 5 | Hull physics and helm | `physics/hull.py`, `physics/integrate.py`, helmsman | 1, 3 | M1 |
| 6 | Orders grammar and resolution | `orders/*`, `vocabulary.yaml`, grammar tests | 3 | M1 |
| 7 | Evolution runner | `evolutions/registry.py`, `runner.py`, the M2 evolution files including tack, wear, heave to | 3, 6 | M1/M2 |
| 8 | Reference ships (data) | `frigate-36.yaml`, `topsail-schooner.yaml`, complete, with sources cited from `docs/references/` | 3 | M2 |
| 9 | Strain and balance | `physics/strain.py`, blanketing, heel, weather helm reading | 4, 5, 8 | M2 |
| 10 | Known truths | `tests/test_known_truths.py` and the tuning pass on class curves and hull constants | 4, 5, 7, 8, 9 | M2 |
| 11 | Server and client | `ui/server.py`, `client/*` | 1, 3, 7 | M2 |
| 12 | Milestone review | Owner sails both ships in the client; issues filed as truths or bugs | all | M2 |

Package 8 is data work grounded in Luce, Lever and Falconer and can start as soon as the schema (3) is stable; it is the package where the owner's knowledge is most useful as a reviewer. Package 10 is the one most likely to loop: the curves in §7.2 are guesses until the truths pass.

### 11.3 Delegation notes

- Each package gets: this specification, the design proposal, the package's row, and the instruction to add tests and to run `ruff` and `pytest` before finishing.
- Packages that touch the same file coordinate through the file's owner: `sail_classes.yaml` is owned by 4 and amended by 10; ship files are owned by 8.
- Anything that would change a contract in §5 to §9 is raised as a proposed edit to this document, not silently implemented.

---

### 11.4 Milestone gates

Every milestone ends with a human-checked gate; the next one does not start until the owner has passed it. The process is in `docs/gates/README.md`. In short:

1. The milestone's acceptance list passes locally and on GitHub Actions (`.github/workflows/ci.yml`).
2. A **gate report** is written for a non-programmer at `docs/gates/gate-mN.md`: headline claims, setup with expected output at each step, a live checklist with exact input and expected output per item, a guide to any technical idea the checklist relies on, what is deliberately absent, and what to report back.
3. A snapshot branch `gates/mN` is created at the gate commit. The `gate release` workflow (`.github/workflows/release.yml`) re-runs the checks, tags the commit `gate-mN`, and creates a GitHub release with the report as its notes and a zip of the whole project attached. If the workflow cannot run, the snapshot branch's own *Download ZIP* is the same package.
4. The owner runs the checklist from the zip and gives a verdict, recorded at the top of the report.

Gate reports are part of the milestone's work package, not an afterthought: the report for milestone N is written before the tag, by whoever integrates the milestone.

## 12. Open items in this specification

1. **Curve numbers and hull constants** (§7.2, §7.4) are placeholders until the truths pass. That is expected.
2. **Rudder and yaw constants** need a turning-circle truth; Luce 1884 Appendix L has real turning experiments to draw one from. Proposed as truth 16 once someone reads it.
3. **Reef factors** per class are guesses; Lever gives the depth of reef bands for topsails.
4. **Blanketing** is deliberately crude. If it produces silly results in M2, it becomes a per-sail lookup rather than a rule.
6. **Mast rake.** Closed: masts take a signed `rake_deg` (positive aft, negative forward for a polacre's fore mast), the ship view tilts them, and the generator carries each sail's centre aft with its mast. The physics still reads the sail's `x_m`; a later refinement could derive it from the rake at run time instead of at generation.
7. **The schooner's bare fore yard.** Baltimore schooners spread the topsail's foot on a bare fore yard (0.48 to 0.57 of the waterline length, often with a square fore course). The file omits it because a milestone 1 test counts two yards on her; add the yard, and optionally the course, when that test is revisited.
5. **The frigate's exact particulars** (LWL, beam, sail areas, spar lengths). Package 8 should pick a documented class rather than invent one; a 36-gun 18-pounder frigate of the 1790s is the target, and its dimensions are widely published.
