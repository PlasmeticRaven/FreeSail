# Milestone 1 work packages: contracts between them

This is the working agreement for packages 4 to 7 of `docs/TechnicalSpec-M0-M2.md` §11.2, built on package 3 (the ship schema, parts and graph, already in `freesail/ship/`). Each package is written by a different agent in its own copy of the repository, so the boundaries below are the whole of what they may assume about each other. Read the specification's §3 to §8 first; this document only fixes the seams.

## What package 3 provides (read, do not modify)

- `freesail/ship/schema.py`: the file format, classes and validation.
- `freesail/ship/parts.py`: runtime state. `Spar` (`brace_angle`, `brace_limit`, `sent_down`, `wrecked`, `condition`, `load_kn`, `rating_kn`, `x_m`, `height_m`, `length_m`, `side`), `Sail` (`state: SailState`, `reefs`, `sheet_angle`, `side`, `roles`, `area_m2`, `x_m`, `centre_height_m`, `reef_bands`, `cloth_rating_kn`, physics outputs `backed`, `force_kn`, `thrust_kn`, `side_force_kn`, `area_effective_m2`), `Line` (`state: LineState`, `hauled`, `of`, `side`), `Hull` (`spec`, `hull_speed`, `lateral_area`, `wetted_area`), `Dynamics` (`x, y, heading, u, v, r, heel, rudder, helm_mode, target_heading, target_rudder, steady, speed, leeway, weather_helm, apparent_wind_angle, apparent_wind_speed`, `tack`).
- `freesail/ship/graph.py`: `Ship` with `spars`, `sails`, `lines`, `parts`, `groups`, `aliases`, `hull`, `dyn`, `extra` (a dict for systems to keep their state in), `note(severity, kind, text, subject=None, data=None)` to queue a log entry, and the role queries `yard_of`, `sail_of`, `sails_using`, `spar_of_role`, `parent_of`, `spar_chain`, `dependents`, `sails_on`, `mast_of`, `lines_of`, `line_of`, `halyard_of`, `braces_of`, `sheets_of`. Two hooks the World calls: `ship.stepper(ship, dt, wind)` once per tick and `ship.order_handler(ship, text)`.
- `freesail/physics/wind.py`: `Wind` with `direction_from` (radians, where from), `speed_at_height(h)`, `vector_at_height(h)` (x east, y north, m/s), `effective_speed`.
- `freesail/units.py`: conversions, `wrap_pi`, `heading_vector`, `relative_bearing`, compass points, bells. SI internally.
- `data/ships/frigate-36.yaml` and `data/ships/topsail-schooner.yaml`: draft reference ships. Use them in tests. Do not edit them; if one needs a change, say so in your report.
- `tests/test_ship_loader.py::MINIMAL`: a small valid ship dictionary handy for unit tests.

Sign conventions (from `Dynamics` and the spec §4): heading clockwise from north; `v` and `r` positive to starboard; `rudder` positive turns the ship to starboard; `apparent_wind_angle` positive when the wind is on the starboard bow; `heel` positive to starboard; yard `brace_angle` positive when the yard is braced up for the starboard tack (wind from starboard): starboard yardarm forward, larboard yardarm aft, so on the starboard tack hauling the larboard (lee) brace increases it; `sheet_angle` is the unsigned angle of a fore-and-aft sail's chord from the centreline, with the sail always assumed to lie on the lee side.

If a convention here is unworkable, report it; do not silently choose another.

## Package 4: wind and sail physics (`freesail/physics/sails.py`, `data/sail_classes.yaml`)

Provides:

```python
@dataclass
class SailForces:
    thrust_n: float          # along the keel, forward positive
    side_n: float            # to starboard positive (i.e. same sign as the force pushing to leeward on the larboard tack)
    heel_moment_nm: float    # positive heels to starboard
    yaw_moment_nm: float     # about the hull's centre of lateral resistance (hull.spec.clr_x_m), positive turns to starboard
    windage_drag_n: float    # drag of furled sails, spars and wrecks, along the apparent wind (opposes motion; include in thrust/side)

def compute_sail_forces(ship: Ship, wind: Wind) -> SailForces
```

- Reads `ship.dyn` (heading, u, v, heel), the wind, sail states and trims, spar `brace_angle`, `sent_down`, `wrecked`.
- Implements spec §7.1 (apparent wind at each sail's height), §7.2 (effective area, chord angle, angle of attack, class curves, force resolution), §7.3 (blanketing). Sets each `Sail`'s `backed`, `force_kn`, `thrust_kn`, `side_force_kn`, `area_effective_m2`; sets `load_kn` on the sail (its own cloth), its principal spar, the spar chain beneath (summed), and its sheets, halyard and braces per the fractions in §7.5. Does *not* change condition or carry anything away (that is package 9).
- Also computes and stores in `ship.dyn` the apparent wind at deck level: `apparent_wind_angle`, `apparent_wind_speed`.
- `data/sail_classes.yaml`: per class, the `C_L(α)` and `C_D(α)` tables, reef factor per band, windage fraction when furled, and any class notes. Starting values per spec §7.2; keep them plausible, they will be tuned in package 10.
- Tests: symmetric behaviour on either tack; a square sail backed gives negative thrust; a fore-and-aft sail at zero angle of attack gives no lift; running before the wind, a blanketed sail gives less; total force scales with wind speed squared; the frigate's sails at a beam reach in 15 kn give a total thrust in the tens of kilonewtons.

## Package 5: hull physics, helm and integration (`freesail/physics/hull.py`, `freesail/physics/integrate.py`)

Provides:

```python
def step(ship: Ship, dt: float, wind: Wind) -> None   # in integrate.py; dt is the tick (1.0 s)
```

- Runs four substeps of `dt/4`. Each substep: calls `compute_sail_forces(ship, wind)` (package 4; until it lands, develop against a stub that returns fixed forces, and keep the call site exactly as above), then applies §7.4: resistance, sway damping, yaw moment with rudder and yaw damping, quasi-static heel, helmsman controller, semi-implicit Euler. Updates `ship.dyn` position, heading, `u`, `v`, `r`, `heel`, `rudder`, and the readings `speed`, `leeway`, `weather_helm`.
- Helm modes: `HEADING` (steer `target_heading`), `RUDDER` (hold `target_rudder`), `FULL_AND_BY` (steer to the smallest apparent wind angle at which the sails are not luffing; a simple rule: keep the apparent wind angle at the sail-class-appropriate minimum plus five degrees, using the value package 4 exposes as `ship.extra.get("luff_angle")` if present, else 45°).
- Logs through `ship.note`: `helm.steady` when settled on an ordered heading (within 2° for 20 s, once per order), `ship.aback` (urgent) when the net thrust has been negative for 10 s with sails set, and a routine leeway change note when leeway changes by more than a degree since last noted (at most one per minute).
- Constants (`C_f`, `C_lat`, `C_yaw`, `C_r`, helmsman gains, heel time constant) live at the top of `hull.py`, named, with a comment on each. Package 10 will tune them.
- Tests with a stub `compute_sail_forces`: a constant forward force accelerates to a terminal speed below hull speed; a side force produces leeway and heel of the right sign; rudder to starboard turns the ship to starboard; the helmsman reaches an ordered heading without endless oscillation; a heading order across north is handled.

## Package 6: Orders, imperative dialect (`freesail/orders/`, `data/vocabulary.yaml`)

Provides:

```python
def handle(ship: Ship, text: str) -> tuple[str, str, dict]   # matches Ship.order_handler; raises OrderError
```

plus the pieces in spec §8: `grammar.py` (tokenise and parse into an `Order` with verb, objects, modifiers, side), `resolve.py` (nouns from part ids, aliases, groups, generated names per §6.5, sides, `weather`/`lee` from `ship.dyn.tack`), `verbs.py` (the verb table §8.2), `errors.py` (nautical error messages with nearest-name suggestions).

- Level 1 verbs start evolutions through the runner: `runner = ship.extra["evolutions"]`, `runner.start(ship, evolution_id, subject_id, params) -> str` (returns a log sentence, raises `OrderError` with the reason if a precondition fails). Evolution ids are as in spec §8.4; the verb table maps a verb and a sail class to an id (`set` + `square` -> `set_square`). For group objects, start one evolution per member; if any fails, still start the others and report the failures in the returned text.
- Level 0 verbs act directly: `haul`/`ease` on a brace shift the yard's `brace_angle` by 5° (respecting `brace_limit`, signed by which side's brace); on a sheet of a fore-and-aft sail shift `sheet_angle` by 5°; on a halyard shift `hauled` by 0.1; `let go` sets the line `FREE`; `belay` sets `BELAYED`. Say in the log what happened in a sailor's words.
- Helm verbs set `ship.dyn.helm_mode`, `target_heading`, `target_rudder`, `steady = False`.
- `data/vocabulary.yaml`: verbs and synonyms, modifiers, number words, generated-name rules (contractions such as tops'l, t'gallant, stuns'l), and the group evolutions (`set plain sail`, `make all sail`, `shorten sail`) as lists of orders.
- Tests: a table of at least a hundred orders and their expected parse or rejection against both reference ships, including period phrasings, `port` echoed as larboard, ambiguity ("set the topsail" on the frigate is rejected with the three candidates), `weather`/`lee` resolution on each tack, and level-0 effects on parts. The runner may be stubbed with a fake recorded in `ship.extra["evolutions"]`.

## Package 7: evolution runner (`freesail/evolutions/`, `data/evolutions/*.yaml`)

Provides:

```python
class Runner:
    def __init__(self, ship: Ship): ...        # registers itself as ship.extra["evolutions"]
    def start(self, ship: Ship, evolution_id: str, subject_id: str, params: dict | None = None) -> str
    def step(self, ship: Ship, dt: float, wind: Wind) -> None   # called once per tick, before physics
    def in_progress(self) -> list[dict]        # for the state snapshot: id, subject, step, remaining_s
```

- `registry.py` loads every `data/evolutions/*.yaml` at import into a dictionary by id; file shape per spec §8.4, with a `ramp:` step type in addition to `sets:` for numeric fields that change over the step's duration (a brace evolution ramps `brace_angle` toward its target).
- Preconditions and `sets` are small expressions over the subject and the graph. Implement a *tiny* safe evaluator (no `eval`): names `sail`, `yard`, `spar`, `line` for the subject as appropriate, dotted attributes, the graph functions `yard_of`, `halyard_of`, `spar_chain`, `wrecked` (true if any spar in the chain is wrecked or sent down), comparisons, `in [..]`, `and`, `or`, `not`. Report what the evaluator supports in the module docstring.
- Durations scale by the weather factor of spec §8.4 (1.0 in light airs up to 2.0 at 30 kn and 25° heel; read `wind.effective_speed` and `ship.dyn.heel`).
- Two evolutions on the same subject are serialised: the second waits for the first. Starting an evolution whose preconditions fail raises `OrderError` with the failing condition put into words.
- Logs `evolution.started` (routine), `evolution.completed` / the evolution's own `on_complete` kind (notable), `evolution.failed` (notable).
- Evolution files required: `set_square`, `take_in_square`, `furl_square`, `reef_square`, `shake_out_square`, `set_gaff`, `take_in_gaff`, `reef_gaff`, `shake_out_gaff`, `set_jibheaded`, `take_in_jibheaded`, `set_studding`, `take_in_studding`, `brace` (params: target angle, which yards), `tack`, `wear`, `heave_to`, `fill_away`. Durations from Luce and Lever (`docs/references/`), cited in each file's `source:`; the `crew:` block authored per §8.4 but ignored. `tack`, `wear` and `heave_to` are the scripted forms of spec §8.5: they set helm targets and brace the yards on a timeline and watch `ship.dyn` for the head passing through the wind; `tack` ends in `ship.tacked` or `ship.missed_stays`.
- Tests: each evolution runs to completion on the reference ships with a stub physics that does nothing; preconditions reject correctly with a sentence; serialisation on one subject; the weather factor lengthens durations; tack on a stub that turns the ship succeeds, and on one that stalls it misses stays.

## Integration (done by the lead after the four packages land)

`freesail/api/session.py` (or similar) composes: `Runner(ship)`; `ship.stepper = lambda s, dt, w: (runner.step(s, dt, w), integrate.step(s, dt, w))`; `ship.order_handler = orders.handle`; the console gets a `--ship` argument and the M1 acceptance checks run. Nothing in the four packages should import from the others except as stated above (5 imports 4's `compute_sail_forces`; 6 uses the runner via `ship.extra`).

## House rules for every package

- Python 3.11, `ruff check .`, `ruff format .`, `python -m pytest` all clean before you finish. Add your tests under `tests/`.
- No randomness outside `core/rng.py`; the physics and evolutions are deterministic.
- Log text in the ship's-log voice: short, past tense, concrete, nautical.
- Do not change files owned by another package or by package 3. If you need a change, describe it precisely in your final report and work around it locally.
- Finish with a report: what you built, how to run its tests, what you assumed, what you need from others, what you would tune.
