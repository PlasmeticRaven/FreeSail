"""The guns' service as a cycle (spec M7 §8, §8a; rule 2, rule 7; package 70; the design
in `docs/design/Design-WorkInAction.md`).

A gun's service is a small state machine per gun, stepped every tick by the action's
tick (`action.py`) and never an evolution queued: the phases of Douglas's exercise
(*A Treatise on Naval Gunnery*, 1820: "Sponge", "Load with cartridge", "Shot your gun",
"Ram home", "Run out", "Prime", "Point", "Fire") with a nominal time each by the gun's
kind, run at the pace the crew factor gives the hands at that gun (numbers, rating,
fatigue, the roll on deck: `crew.hands.crew_factor`'s own terms) and the weather factor,
so that **the rate of fire falls out of the muster** (rule 2): a full and fresh crew of a
long 18-pounder fires in about a minute and a half, a thinned or tired one slower, a crew
under half its number not at all. The figures are judgements against Douglas's and the
logs' broadside every minute and a half to two minutes at the start of an action, pinned
by the truths and tuned in play.

The **battery** is the runtime over a ship's guns: the standing intentions the divisions
keep (`engaged` side, the `charge`, the `aim`, the `mode` of fire, the gun captain's roll
doctrine) and the target as the lookout has her; the one-shot orders (`fire`, a single gun,
`cease firing`) ride over them. A gun pair's one crew serves the engaged side's gun; with no
side engaged it loads both guns in turn; engaged on both sides it serves both at half
strength. A gun fires when it is primed and pointed and the intention lets it: `as they
bear` (the period's independent fire: the target within its arc and reach), `by divisions`
(the forward division and the after by turns), `at the word` (the broadside together on
`fire`), `hold` (loaded and run out, silent). The shot's flight is `shot.py`'s and its fall
`hits.py`'s; the battery writes **one line a minute** for all its guns (what her people can
see: struck, short, over) and never a line a gun.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from freesail import units
from freesail.combat import shot as S
from freesail.crew import hands as H
from freesail.crew.model import number_words
from freesail.ship.parts import Charge, Gun, magazine

__all__ = [
    "ARC_BROADSIDE_DEG",
    "ARC_CHASER_DEG",
    "Aim",
    "Battery",
    "FireMode",
    "PHASES",
    "Service",
    "battery_of",
    "charge_of_words",
]


class FireMode(StrEnum):
    HOLD = "hold"
    AS_THEY_BEAR = "as they bear"
    BY_DIVISIONS = "by divisions"
    AT_THE_WORD = "at the word"


class Aim(StrEnum):
    HULL = "hull"
    RIGGING = "rigging"
    BETWEEN = "between wind and water"


# The phases of the exercise and their nominal seconds with a full and fresh crew (Douglas
# 1820, part II, the words of command; the seconds judgement, set so that a long 18-pounder
# fires every minute and three quarters or so with the frigate's crews and the weather's
# factor on them (truth 7-135: 85 s nominal measured 105 s at seed 7) and a carronade
# every minute, which is what the logs of 1805 report of a drilled ship at the start of
# an action; a 3-pounder and a swivel are light work).
PHASES: dict[str, tuple[tuple[str, float], ...]] = {
    "long": (
        ("sponge", 13.0),
        ("cartridge", 9.0),
        ("shot", 13.0),
        ("ram", 9.0),
        ("run out", 18.0),
        ("prime", 9.0),
        ("point", 14.0),
    ),
    "carronade": (
        ("sponge", 10.0),
        ("cartridge", 8.0),
        ("shot", 10.0),
        ("ram", 6.0),
        ("run out", 8.0),
        ("prime", 8.0),
        ("point", 10.0),
    ),
    "swivel": (("cartridge", 10.0), ("shot", 10.0), ("prime", 5.0), ("point", 10.0)),
}
# A long gun of the small calibres is worked faster than the frigate's 18-pounder: the
# phases' times scale with the gun's weight against 42 cwt, never below this share
# (judgement: a 3-pounder of 7 cwt is handled by three men in two thirds of the time).
LIGHT_GUN_SHARE_FLOOR = 0.65
REFERENCE_CWT = 42.0
# The short crew's power (see `Battery._factor`): judgement, pinned by truth 7-135.
NUMBERS_POWER = 2.0

# The arc a gun bears through: a broadside gun thirty-five degrees either side of abeam,
# trained with handspikes and the quoin (Douglas; the period's ports allowed about that,
# judgement), a chaser twenty-five either side of right ahead or astern, a swivel on its
# yoke all round but across her own deck.
ARC_BROADSIDE_DEG = 35.0
ARC_CHASER_DEG = 25.0
ARC_SWIVEL_DEG = 100.0

# The words for the charges the orders take.
CHARGE_WORDS = {
    "round": Charge.ROUND,
    "round shot": Charge.ROUND,
    "ball": Charge.ROUND,
    "chain": Charge.CHAIN,
    "chain shot": Charge.CHAIN,
    "bar": Charge.CHAIN,
    "bar shot": Charge.CHAIN,
    "double headed": Charge.CHAIN,
    "double headed shot": Charge.CHAIN,
    "grape": Charge.GRAPE,
    "grape shot": Charge.GRAPE,
    "canister": Charge.GRAPE,
    "double": Charge.DOUBLE,
    "double shot": Charge.DOUBLE,
    "blank": Charge.BLANK,
    "powder": Charge.BLANK,
    "a blank cartridge": Charge.BLANK,
}


def charge_of_words(words: str) -> Charge | None:
    key = " ".join(str(words).lower().replace("-", " ").split())
    for lead in ("with ", "the "):
        key = key.removeprefix(lead)
    return CHARGE_WORDS.get(key)


@dataclass
class Service:
    """One gun's place in the cycle: the phase in hand (-1: nothing in hand), the seconds
    left in it at the nominal pace, and whether the gun waits for the word."""

    phase: int = -1
    left_s: float = 0.0
    stalled: str = ""  # why it is not served: "short-handed", "no cartridge", ""
    said_stalled: bool = False

    @property
    def idle(self) -> bool:
        return self.phase < 0


@dataclass
class Firer:
    """What the firing ship is this tick: her heel (positive to starboard), her roll, the
    sea's height, the weather factor, her half-beam, her heading, her position."""

    heel_deg: float
    roll_deg: float
    sea_height_m: float
    weather_factor: float
    half_beam_m: float
    heading_rad: float
    position: Any


@dataclass
class Target:
    """The mark as the firer's people have her: her id as the lookout names her, her words,
    the true bearing and range from the firer, her heading and length, her heel, her
    nation as made out (or None), and the body the shot resolves against (`hits.py`)."""

    id: str
    words: str
    bearing_rad: float
    range_m: float
    heading_rad: float
    length_m: float
    heel_deg: float
    nation: str | None
    body: Any  # a `Ship` (a crewed or the player's), or a far `Vessel`
    world: Any  # the World whose log her hits go to, or None for a far vessel


@dataclass
class Volley:
    """What one gun's shot did, for the minute's tally."""

    gun_id: str
    charge: Charge
    outcome: str  # "struck", "short", "over", "wide", "blank"
    seen: list[str] = field(default_factory=list)  # what the firer could see of the hit


class Battery:
    """A ship's guns as one runtime (the module's head)."""

    def __init__(self, ship: Any) -> None:
        self.ship = ship
        self.services: dict[str, Service] = {gid: Service() for gid in ship.guns}
        self.target: str | None = None
        self.target_words: str = ""
        self.engaged: str | None = None  # "starboard", "larboard", "both", None
        self.charge: Charge = Charge.ROUND
        self.aim: Aim = Aim.HULL
        self.mode: FireMode = FireMode.HOLD
        self.roll_doctrine: str | None = None  # "up", "down", None
        self.run_out_wanted: bool = True
        self.cleared: bool = False  # cleared for action
        self.word: str | None = None  # a broadside ordered: the side, or "both"
        self.single: list[str] = []  # guns ordered to fire by name, once each
        self.across_bows: bool = False  # the next single shot is a shot across her bows
        self.division_turn: str = "forward"
        self.volleys: list[Volley] = []  # this minute's
        self.opened_fire_at: dict[str, int] = {}  # target id -> tick the first shot went
        self.last_fired_tick: int | None = None
        self.rounds_fired: int = 0
        # the mark's relative bearing this tick, for the runner's robbing of the guns
        self.target_relative_rad: float | None = None
        self._said_no_powder: set[float] = set()
        self._fell_back: set[tuple[float, str]] = set()  # (pounder, charge) said once
        self._warned: set[str] = set()

    # -- the intentions --------------------------------------------------------------

    def side_of(self, gun: Gun) -> str | None:
        return gun.side

    def serving(self, gun: Gun) -> bool:
        """Whether the crew serves this gun under the intentions: cast loose, mounted, and
        on the engaged side (or any side while none is engaged, to have both loaded)."""
        if not gun.serves or not gun.cast_loose:
            return False
        if gun.place in ("bow", "stern", "rail"):
            return True
        if self.engaged in (None, "both"):
            return True
        return gun.side == self.engaged

    def ready(self, gun: Gun) -> bool:
        return bool(gun.loaded) and gun.primed and (gun.run_out or gun.kind == "swivel")

    def wants_work(self, gun: Gun) -> bool:
        """Whether the gun has a phase to work: not yet loaded, run out (when wanted) and
        primed."""
        if not gun.loaded:
            return True
        if self.run_out_wanted and not gun.run_out and gun.kind != "swivel":
            return True
        return not gun.primed

    # -- the tick ------------------------------------------------------------------------

    def tick(
        self,
        dt: float,
        quarters: Any,
        firer: Firer,
        target: Target | None,
        rng: Any,
        tick: int,
        resolve: Any,
    ) -> None:
        """One tick: each crew's work on its guns, then the guns that fire. `resolve` is
        `hits.resolve_shot`, given each shot that goes."""
        ship = self.ship
        mag = magazine(ship)
        crews: dict[str, list[Gun]] = {}
        for g in ship.guns.values():
            crews.setdefault(g.pair_key, []).append(g)
        for guns in crews.values():
            active = [g for g in guns if self.serving(g) and self.wants_work(g)]
            if not active:
                continue
            hands = quarters.hands_at(active[0]) if quarters is not None else []
            wanted = quarters.wanted_at(active[0]) if quarters is not None else active[0].crew_n
            got = len(hands) / len(active)
            if quarters is not None and got * 2.0 < wanted:
                for g in active:
                    self.services[g.id].stalled = "short-handed"
                continue
            factor = self._factor(hands, wanted, got, firer, active[0].kind, len(active))
            for g in active:
                self._work(g, dt / factor, mag, tick)
        self._fire(quarters, firer, target, rng, tick, resolve, mag)

    def _factor(
        self, hands: list[Any], wanted: int, got: float, firer: Firer, kind: str, n_active: int
    ) -> float:
        """The crew factor at a gun: the numbers over the men at it, their rating against
        the ordinary seaman's (the gun's exercise is deck work), their fatigue, the roll on
        deck and the weather factor; a light gun worked faster in proportion to its weight
        (`LIGHT_GUN_SHARE_FLOOR`)."""
        if not hands:
            return 1.0e9
        # a short crew slows the gun more than in proportion: the heavy work (running out,
        # the handspikes at the point) wants its full numbers (Douglas 1820, part II, on the
        # exercise with reduced crews; the square judgement: a crew of three quarters serves
        # the gun in a minute and three quarters' place three minutes, truth 7-135)
        numbers = max(1.0, wanted / max(got, 0.5)) ** NUMBERS_POWER
        reference = H.rating_skill(H.DEFAULT_RATING, False)
        ratios = [reference / max(H.rating_skill(s.rating, False), H.SKILL_FLOOR) for s in hands]
        skill = sum(ratios) / len(ratios)
        mean_fatigue = sum(s.fatigue for s in hands) / len(hands)
        fatigue = 1.0 + H.FATIGUE_WEIGHT * max(0.0, mean_fatigue - H.FATIGUE_FRESH)
        seaway = H.seaway_factor(firer.roll_deg, False)
        return numbers * skill * fatigue * seaway * max(1.0, firer.weather_factor)

    def _charge_for(self, gun: Gun, mag: Any) -> Charge | None:
        """The charge this gun loads under the intention: a swivel takes round or grape
        and never chain or double (its bore; Falconer 1780, 'Swivel'); a charge the
        magazine is out of falls back to round shot with the gunner's word once; None
        when there is no round shot either."""
        want = self.charge
        if gun.kind == "swivel" and want in (Charge.CHAIN, Charge.DOUBLE):
            want = Charge.ROUND
        if mag.has(gun.pounder, want):
            return want
        if want is not Charge.ROUND and mag.has(gun.pounder, Charge.ROUND):
            key = (gun.pounder, want.value)
            if key not in self._fell_back:
                self._fell_back.add(key)
                self.ship.note(
                    "notable",
                    "guns.magazine_empty",
                    f"The gunner reports no more {_charge_words(want)} for the "
                    f"{gun.kind_words}s: they load with round shot.",
                    gun.id,
                    {"pounder": gun.pounder, "charge": want.value, "instead": "round"},
                )
            return Charge.ROUND
        return None

    def _phases(self, gun: Gun) -> tuple[tuple[str, float], ...]:
        phases = PHASES.get(gun.kind, PHASES["long"])
        if gun.kind == "long" and gun.weight_cwt > 0.0:
            share = max(LIGHT_GUN_SHARE_FLOOR, min(1.0, gun.weight_cwt / REFERENCE_CWT))
            return tuple((name, s * share) for name, s in phases)
        return phases

    def _work(self, gun: Gun, dt_eff: float, mag: Any, tick: int) -> None:
        svc = self.services[gun.id]
        phases = self._phases(gun)
        svc.stalled = ""
        if svc.idle:
            # begin where the gun stands: loaded wants running out and priming only
            if gun.loaded:
                svc.phase = next(
                    i
                    for i, (name, _) in enumerate(phases)
                    if name == ("run out" if not gun.run_out and gun.kind != "swivel" else "prime")
                )
            else:
                svc.phase = 0
            svc.left_s = phases[svc.phase][1]
        left = dt_eff
        while left > 0.0 and not svc.idle:
            name = phases[svc.phase][0]
            if name == "cartridge" and not gun.loaded and svc.left_s >= phases[svc.phase][1]:
                # the powder comes up: a cartridge and the shot taken from the magazine as
                # the loading begins; none, and the gun stays empty
                charge = self._charge_for(gun, mag)
                if charge is None:
                    svc.stalled = "no cartridge"
                    if gun.pounder not in self._said_no_powder:
                        self._said_no_powder.add(gun.pounder)
                        self.ship.note(
                            "notable",
                            "guns.magazine_empty",
                            f"The gunner reports no more cartridges for the "
                            f"{gun.kind_words}s: the magazine is out.",
                            gun.id,
                            {"pounder": gun.pounder, "charge": self.charge.value},
                        )
                    svc.phase = -1
                    return
                mag.take(gun.pounder, charge)
                gun.loaded = charge
            step = min(left, svc.left_s)
            svc.left_s -= step
            left -= step
            if svc.left_s > 1e-9:
                break
            # the phase done
            if name == "run out":
                gun.run_out = True
            elif name == "prime":
                gun.primed = True
            elif name == "point":
                pass
            svc.phase += 1
            if svc.phase >= len(phases):
                svc.phase = -1
                break
            # a phase the gun's state has no need of is passed over
            while svc.phase < len(phases):
                nxt = phases[svc.phase][0]
                if nxt == "run out" and (gun.run_out or not self.run_out_wanted):
                    svc.phase += 1
                    continue
                if nxt == "prime" and gun.primed:
                    svc.phase += 1
                    continue
                break
            if svc.phase >= len(phases):
                svc.phase = -1
                break
            svc.left_s = phases[svc.phase][1]

    # -- firing ------------------------------------------------------------------------

    def bears(self, gun: Gun, relative_rad: float) -> bool:
        """Whether the mark at this relative bearing (from the bow, starboard positive) is
        within the gun's arc."""
        deg = math.degrees(relative_rad)
        if gun.place == "broadside":
            centre = 90.0 if gun.side == "starboard" else -90.0
            return abs(_wrap_deg(deg - centre)) <= ARC_BROADSIDE_DEG
        if gun.place == "bow":
            return abs(_wrap_deg(deg)) <= ARC_CHASER_DEG
        if gun.place == "stern":
            return abs(_wrap_deg(deg - 180.0)) <= ARC_CHASER_DEG
        centre = 90.0 if gun.side == "starboard" else -90.0
        return abs(_wrap_deg(deg - centre)) <= ARC_SWIVEL_DEG

    def _fire(
        self,
        quarters: Any,
        firer: Firer,
        target: Target | None,
        rng: Any,
        tick: int,
        resolve: Any,
        mag: Any,
    ) -> None:
        ship = self.ship
        relative = (
            units.wrap_pi(target.bearing_rad - firer.heading_rad) if target is not None else None
        )
        # the single guns and the gun to leeward: by name, once each, at whatever bears
        for gid in list(self.single):
            g = ship.guns.get(gid)
            if g is None or not self.ready(g):
                continue
            self.single.remove(gid)
            self._discharge(g, quarters, firer, target, relative, rng, tick, resolve)
        if target is None or relative is None:
            self.word = None
            return
        # a gun captain fires at what his gun can throw to: a mark beyond its random range
        # is not fired at (Douglas 1820 on the waste of powder at long shot; judgement)
        ready = [
            g
            for g in ship.guns.values()
            if self.ready(g)
            and self.bears(g, relative)
            and self._side_fires(g)
            and target.range_m <= S.ballistics_of(g.kind, g.pounder).random_m
        ]
        if not ready:
            return
        if self.word is not None:
            side = self.word
            volley = [
                g for g in ready if side == "both" or g.side == side or g.place != "broadside"
            ]
            self.word = None
            self._broadside(volley, quarters, firer, target, relative, rng, tick, resolve)
            return
        if self.mode is FireMode.AS_THEY_BEAR:
            for g in ready:
                self._discharge(g, quarters, firer, target, relative, rng, tick, resolve)
        elif self.mode is FireMode.BY_DIVISIONS:
            division = [g for g in ready if (g.x_m >= 0.0) == (self.division_turn == "forward")]
            if division:
                self._broadside(division, quarters, firer, target, relative, rng, tick, resolve)
                self.division_turn = "after" if self.division_turn == "forward" else "forward"

    def _side_fires(self, gun: Gun) -> bool:
        if gun.place != "broadside":
            return True
        if self.engaged is None:
            return False
        return self.engaged == "both" or gun.side == self.engaged

    def _broadside(self, guns, quarters, firer, target, relative, rng, tick, resolve) -> None:
        for g in guns:
            self._discharge(g, quarters, firer, target, relative, rng, tick, resolve)

    def _discharge(
        self,
        gun: Gun,
        quarters: Any,
        firer: Firer,
        target: Target | None,
        relative: float | None,
        rng: Any,
        tick: int,
        resolve: Any,
    ) -> None:
        """One gun fired: the shot laid for the mark by its captain, the heel and the quoin
        answering so far, the fall of shot drawn, the hit resolved against her body; the
        gun empty after, its cycle to begin again."""
        charge = gun.loaded or Charge.ROUND
        gun.loaded = None
        gun.run_out = False
        gun.primed = False
        gun.fired += 1
        self.rounds_fired += 1
        self.last_fired_tick = tick
        self.services[gun.id].phase = -1
        hands = quarters.hands_at(gun) if quarters is not None else []
        if target is None or relative is None or charge is Charge.BLANK or self.across_bows:
            # a blank charge, a shot across her bows, or no mark: nothing struck
            outcome = "blank" if charge is Charge.BLANK else "across her bows"
            self.across_bows = False
            self.volleys.append(Volley(gun.id, charge, outcome))
            return
        if target.id not in self.opened_fire_at:
            self.opened_fire_at[target.id] = tick
        b = S.ballistics_of(gun.kind, gun.pounder)
        lee = _is_lee(gun, firer.heel_deg)
        heel = abs(firer.heel_deg)
        # the gun captain lays the gun for the range, the quoin within its limits, the heel
        # against him on the lee side and for him to windward (`shot.effective_elevation`)
        wanted = _elevation_for(b, target.range_m) + (1.0 if self.aim is Aim.RIGGING else 0.0)
        quoin = wanted + heel if lee else wanted - heel
        quoin = max(-b.depression_max_deg, min(b.elevation_max_deg, quoin))
        eff = S.effective_elevation(quoin, heel, lee)
        reach = S.range_at(b, eff)
        on_roll = (self.roll_doctrine == "up" and self.aim is Aim.RIGGING) or (
            self.roll_doctrine == "down" and self.aim is not Aim.RIGGING
        )
        scatter = S.steadiness(firer.roll_deg, firer.sea_height_m, on_roll)
        aspect = S.aspect_of(target.heading_rad, units.wrap_2pi(target.bearing_rad + math.pi))
        p = S.hit_chance(
            target.range_m,
            b,
            reach,
            target_length_m=target.length_m,
            aspect_rad=aspect,
            aim=S.aim_of(hands),
            scatter_deg=scatter,
        )
        high = reach > target.range_m * 1.5  # laid to carry well over her: high
        if reach < target.range_m * 0.95:
            outcome = "short"
        elif rng.random() < p:
            outcome = "struck"
        else:
            outcome = "over" if (high or rng.random() < 0.5) else "wide"
        volley = Volley(gun.id, charge, outcome)
        if outcome == "struck":
            volley.seen = resolve(self, gun, charge, target, high=high, rng=rng, tick=tick)
        self.volleys.append(volley)

    # -- the minute's line --------------------------------------------------------------

    def minute_line(self, tick: int) -> tuple[str, dict[str, Any]] | None:
        """One line for the minute's fire, in the firer's log: what her people can see of
        it. None when nothing was fired."""
        if not self.volleys:
            return None
        volleys, self.volleys = self.volleys, []
        n = len(volleys)
        struck = sum(1 for v in volleys if v.outcome == "struck")
        short = sum(1 for v in volleys if v.outcome == "short")
        over = sum(1 for v in volleys if v.outcome == "over")
        wide = sum(1 for v in volleys if v.outcome == "wide")
        blank = sum(1 for v in volleys if v.outcome in ("blank", "across her bows"))
        seen = [w for v in volleys for w in v.seen]
        at = f" at {self.target_words}" if self.target_words else ""
        if n == blank:
            across = any(v.outcome == "across her bows" for v in volleys)
            text = (
                f"Fired {number_words(n)} gun{'s' if n != 1 else ''}"
                + (" across her bows" if across else "")
                + ", a blank charge."
            )
        else:
            fell = []
            if struck:
                fell.append(f"{number_words(struck)} struck her")
            if short:
                fell.append(f"{number_words(short)} fell short")
            if over:
                fell.append(f"{number_words(over)} over")
            if wide:
                fell.append(f"{number_words(wide)} wide")
            across = sum(1 for v in volleys if v.outcome == "across her bows")
            if across:
                fell.append(f"{number_words(across)} across her bows")
            if blank - across:
                fell.append(f"{number_words(blank - across)} a blank charge")
            text = f"{number_words(n).capitalize()} shot{at}: {_and(fell)}."
            if seen:
                text += " " + " ".join(seen)
        data = {
            "fired": n,
            "struck": struck,
            "short": short,
            "over": over,
            "wide": wide,
            "target": self.target,
            "guns": [v.gun_id for v in volleys],
        }
        return text, data


def battery_of(ship: Any) -> Battery | None:
    """The ship's battery, kept in `ship.extra["battery"]`; None for a ship without guns."""
    extra = getattr(ship, "extra", None)
    if extra is None or not getattr(ship, "guns", None):
        return None
    b = extra.get("battery")
    if isinstance(b, Battery):
        return b
    b = Battery(ship)
    extra["battery"] = b
    return b


# -- helpers --------------------------------------------------------------------------


def _wrap_deg(d: float) -> float:
    return (d + 180.0) % 360.0 - 180.0


def _is_lee(gun: Gun, heel_deg: float) -> bool:
    """Whether the gun is on the lee side: the side she heels toward (heel positive to
    starboard)."""
    if gun.side is None:
        return False
    return (heel_deg > 0.0) == (gun.side == "starboard")


def _elevation_for(b: S.Ballistics, range_m: float) -> float:
    """The effective elevation that carries to the range: the inverse of `range_at`."""
    if range_m <= b.point_blank_m:
        if range_m >= b.point_blank_m * 0.95:
            return 0.0
        # depressed for a mark under point blank
        share = max(0.2, range_m / b.point_blank_m)
        return (share - 1.0) / 0.8 * b.depression_max_deg
    if range_m >= b.random_m:
        return b.elevation_max_deg
    f = (range_m - b.point_blank_m) / (b.random_m - b.point_blank_m)
    return b.elevation_max_deg * f ** (1.0 / 0.9)


def _charge_words(charge: Charge) -> str:
    return {
        Charge.ROUND: "round shot",
        Charge.CHAIN: "chain shot",
        Charge.GRAPE: "grape",
        Charge.DOUBLE: "round shot",
        Charge.BLANK: "cartridges",
    }[charge]


def _and(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]
