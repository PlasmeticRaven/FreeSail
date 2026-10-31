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

**Practice and resupply** (between packages 72 and 73; docs/design/Build-PracticeAndResupply.md
§1.6, §4, §6). A gun loads a **filled** cartridge of its own kind and calibre
(`Magazine.has`); with none filled and powder below it waits at the cartridge phase while
the gunner fills (`combat/filling.py`), told once an outage, and with no powder either the
magazine is out as before. The guns may be **exercised in dumb show** (`begin_exercise`): the
crews serve them through the phases at the action's pace with nothing taken from the
magazine, a loaded gun from the run out to the point with its charge kept, and no gun fires
but by name; each gun's drill is counted (`Drill`; kept, and read for nothing: the owner's
ruling, practice improves no skill). A shot at a **mark** (`Target.mark`, a cask or a
notional mark) is laid and drawn as a shot at a ship, with the mark's own size term, and is
counted as practice (`last_practice_tick`), never as firing on a sail; a shotted gun fired
with no mark sends its shot into the sea.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from freesail import units
from freesail.combat import ports
from freesail.combat import shot as S
from freesail.crew import hands as H
from freesail.crew.model import number_words
from freesail.ship.parts import Charge, Gun, gun_words, magazine

__all__ = [
    "ARC_BROADSIDE_DEG",
    "ARC_CHASER_DEG",
    "ARC_PIVOT_FROM_DEG",
    "ARC_PIVOT_TO_DEG",
    "pivot_arc",
    "PIVOT_TRAIN_DEG_S",
    "Aim",
    "Battery",
    "Drill",
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
# PROVISIONAL (the owner's ask of 2026-10-25, ahead of package 75): a pivot gun on its
# racers amidships fires over either side between the fore rigging and the main, through
# the arc its ship file gives it (`arc_deg`, per gun since package 86's fold-in: the
# privateer schooner's is sixty degrees off the bow to a hundred and forty, the owner's
# ruling of the day reasoned from her rig, the fore topmast backstays at about 55 to 60
# degrees from the pivot, the main shrouds at about 140 to 150;
# docs/design/Proposal-PivotGun.md §3, which proposes each pivot's arcs from its own ship).
# Since package 75 a pivot whose file names no arc is refused at the load (`schema._parse_gun`),
# so the two figures below are kept only for a gun pickled before package 86, which has no
# arc of its own (the lead's ruling, 2026-10-28: an old checkpoint's pivot still bears where
# it did). It is trained round by its crew with the handspikes and the training tackles:
# half a circle in a minute with its full crew, slower short-handed (judgement); within five
# degrees of the mark the slide's play and the handspikes point it, and it bears.
ARC_PIVOT_FROM_DEG = 60.0
ARC_PIVOT_TO_DEG = 140.0
PIVOT_TRAIN_DEG_S = 3.0
PIVOT_ON_DEG = 5.0


def pivot_arc(gun: Any) -> tuple[float, float]:
    """The arc a pivot gun fires through over either side, degrees off the bow: its own
    (`Gun.arc_deg`, from its ship file), else the default (`ARC_PIVOT_FROM_DEG`,
    `ARC_PIVOT_TO_DEG`), which since package 75 only a gun pickled before package 86 takes."""
    arc = getattr(gun, "arc_deg", None)
    if arc is None:
        return (ARC_PIVOT_FROM_DEG, ARC_PIVOT_TO_DEG)
    return (float(arc[0]), float(arc[1]))


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
    # practice and resupply (between packages 72 and 73): the tick the cycle began at the
    # sponge, for the drill's timing; a plain default, so that a service pickled before loads
    began_tick: int | None = None

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
    # practice and resupply (between packages 72 and 73): a mark's kind ("cask",
    # "notional"; "" for a ship), and the hit chance's size term in place of the hull's
    # (None: the hull's, as today). Rebuilt every tick and never pickled.
    mark: str = ""
    size: float | None = None


@dataclass
class Volley:
    """What one gun's shot did, for the minute's tally."""

    gun_id: str
    charge: Charge
    outcome: str  # "struck", "short", "over", "wide", "blank"
    seen: list[str] = field(default_factory=list)  # what the firer could see of the hit
    mark: str = ""  # practice and resupply: the mark's kind when the shot was at a mark


@dataclass
class Drill:
    """A gun's drill (practice and resupply, between packages 72 and 73;
    docs/design/Build-PracticeAndResupply.md §1.6): the rounds served in dumb show and
    fired live, the full cycles timed from the sponge (a swivel's from its cartridge) to
    the point with their total and best seconds, and the falls of shot at the marks by
    cables ("2 struck", "4 short"; at the notional mark "4 struck notional"). Kept and
    never read for pace or aim (the owner's ruling: practice improves no skill). New
    objects only; a field added later takes a plain default."""

    dumb: int = 0
    live: int = 0
    cycles: int = 0
    total_s: float = 0.0
    best_s: float | None = None
    falls: dict[str, int] = field(default_factory=dict)


class Battery:
    """A ship's guns as one runtime (the module's head)."""

    # practice and resupply (between packages 72 and 73; the build design's §1.6): plain
    # class defaults, reassigned on the instance and never mutated here, so that a battery
    # pickled before them loads
    exercise: str | None = None  # "starboard", "larboard", "both": the guns in dumb show
    drill: dict[str, Drill] | None = None  # gun id -> Drill, made at the first record
    last_practice_tick: int | None = None
    _dumb: list[tuple[str, float | None]] | None = None  # this minute's (gun id, seconds)
    _said_filling: set[tuple[str, float]] | None = None  # (kind, pounder) told the gunner fills
    _said_out: set[tuple[str, float]] | None = None  # (kind, pounder) told the magazine is out
    # `_said_no_powder` (float keys) stays, unread: an old pickle's is inert
    # the lee ports (package 75; docs/design/Build-Ships.md §7): the ids of the guns whose
    # ports are shut, the sea at their sills, set by `ports.update` at the head of the tick
    # and left out of the work and the fire; a class default, empty until the rule is built
    _shut: frozenset[str] = frozenset()

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
        on the engaged side (or any side while none is engaged, to have both loaded); while
        the guns are exercised in dumb show, the exercised guns and no others."""
        if not gun.serves or not gun.cast_loose:
            return False
        if self.exercise is not None:
            return self.exercised(gun)
        if gun.place in ("bow", "stern", "rail", "pivot"):
            return True
        if self.engaged in (None, "both"):
            return True
        return gun.side == self.engaged

    def ready(self, gun: Gun) -> bool:
        return bool(gun.loaded) and gun.primed and (gun.run_out or gun.kind == "swivel")

    def wants_work(self, gun: Gun) -> bool:
        """Whether the gun has a phase to work: not yet loaded, run out (when wanted) and
        primed; an exercised gun always (its cycle begins again as it ends). A gun whose
        port is shut (`_shut`, package 75) has none."""
        if gun.id in self._shut:
            return False
        if self.exercise is not None and self.exercised(gun):
            return True
        if not gun.loaded:
            return True
        if self.run_out_wanted and not gun.run_out and gun.kind != "swivel":
            return True
        return not gun.primed

    # -- practice: dumb show and the drill (practice and resupply, between packages 72 and
    # 73; the build design's §1.6 and §6) --------------------------------------------------

    def exercised(self, gun: Gun) -> bool:
        """Whether the gun is of the battery exercised in dumb show: its side, or either
        side for a gun with none (the pivot)."""
        return _of_exercise(self.exercise, gun)

    def begin_exercise(self, side: str) -> list[str]:
        """The guns of `side` ("starboard", "larboard", "both") exercised in dumb show from
        now (Douglas 1820, the exercise; from memory, UNVERIFIED): each crew serves its gun
        through the phases at the action's pace and nothing is taken from the magazine; an
        empty gun runs the whole cycle from the sponge, a loaded gun is run out and pointed
        and keeps its charge; no gun fires but by name. Each exercised gun's cycle begins
        afresh. The guns of a side no longer exercised (`exercise both batteries`, then
        `exercise the starboard battery`) are left as `end_exercise` leaves them (the
        review's finding: an empty larboard gun was left run out and primed, its half-done
        round worked on with no charge after `cease exercising`). The names of the loaded
        guns exercised, which keep their charges."""
        old = self.exercise
        if old is not None and old != side:
            for g in self.ship.guns.values():
                if _of_exercise(old, g) and not _of_exercise(side, g):
                    self._leave_dumb_show(g)
        self.exercise = side
        self._dumb = None
        loaded = []
        for g in self.ship.guns.values():
            if not self.exercised(g):
                continue
            self.services[g.id] = Service()
            if g.loaded:
                loaded.append(g.name)
        return loaded

    def end_exercise(self) -> None:
        """The exercise over: the empty guns exercised run in, unprimed and their cycles
        cleared; a loaded gun kept as it stands, its work going on as the intentions say."""
        if self.exercise is not None:
            for g in self.ship.guns.values():
                if self.exercised(g):
                    self._leave_dumb_show(g)
        self.exercise = None
        self._dumb = None

    def _leave_dumb_show(self, gun: Gun) -> None:
        """An exercised gun out of the dumb show: an empty one run in, unprimed and its cycle
        cleared, so that its live cycle begins at the sponge and takes a cartridge; a loaded
        gun kept as it stands."""
        if not gun.loaded:
            gun.run_out = False
            gun.primed = False
            self.services[gun.id] = Service()

    def serve_by_name(self, gun_id: str) -> None:
        """A gun about to be ordered to fire by name, or as the gun to leeward, while its
        battery is exercised in dumb show: an empty one leaves the dumb show
        (`_leave_dumb_show`) and is served live while it is in `single`, taking a cartridge,
        so that it fires as it would (decision 20; the review's finding: an empty gun named
        in dumb show never loaded, and fired only after `cease exercising`). A loaded gun
        fires as it stands; a gun named already, or not exercised, is left alone. The
        caller puts the gun in `single`."""
        g = self.ship.guns.get(gun_id)
        if g is None or gun_id in self.single or not self.exercised(g):
            return
        self._leave_dumb_show(g)

    def exercise_line(self, tick: int) -> tuple[str, dict[str, Any]] | None:
        """This minute's line for the dumb show ('Exercising the starboard battery in dumb
        show: nine rounds in the minute, No. 3 starboard gun the quickest, a minute and
        twenty seconds from sponge to point.'), or None when no gun completed a round in it.
        `tick_action` records it as `practice.exercise`, never `action.fired`."""
        done, self._dumb = self._dumb, None
        if not done or self.exercise is None:
            return None
        side = self.exercise
        what = "both batteries" if side == "both" else f"the {side} battery"
        n = len(done)
        text = (
            f"Exercising {what} in dumb show: {number_words(n)} round{'s' if n != 1 else ''} "
            "in the minute"
        )
        data: dict[str, Any] = {"exercise": side, "rounds": n, "guns": [gid for gid, _ in done]}
        timed = [(sec, gid) for gid, sec in done if sec is not None]
        if timed:
            sec, gid = min(timed)
            g = self.ship.guns.get(gid)
            name = g.name if g is not None else gid
            start = "cartridge" if g is not None and g.kind == "swivel" else "sponge"
            text += f", {name} the quickest, {seconds_words(sec)} from {start} to point"
            data.update({"quickest": gid, "seconds": sec})
        return text + ".", data

    def drill_of(self, gun_id: str) -> Drill:
        """The gun's drill, made at its first record."""
        if self.drill is None:
            self.drill = {}
        d = self.drill.get(gun_id)
        if d is None:
            d = self.drill[gun_id] = Drill()
        return d

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
        """One tick: the ports shut or opened against the sea at their sills (`ports.update`,
        package 75), each crew's work on its guns, then the guns that fire. `resolve` is
        `hits.resolve_shot`, given each shot that goes."""
        # the lee ports first, so that a gun whose port shuts this tick neither works nor
        # fires in it (Build-Ships.md §7.2); the changes it gives are the log's, once the
        # rule is built, and stage 0's hook shuts nothing
        ports.update(self, firer)
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
        self._train_pivots(dt, quarters, firer, target)
        self._fire(quarters, firer, target, rng, tick, resolve, mag)

    def _train_pivots(self, dt: float, quarters: Any, firer: Firer, target: Target | None) -> None:
        """A pivot gun cast loose is trained round toward the mark the shorter way, at its
        crew's pace (`PIVOT_TRAIN_DEG_S` with the full crew, in proportion short-handed,
        not at all with nobody at it); with no mark it stays where it points
        (PROVISIONAL, 2026-10-25)."""
        if target is None:
            return
        want = math.degrees(units.wrap_pi(target.bearing_rad - firer.heading_rad))
        for g in self.ship.guns.values():
            if g.place != "pivot" or not g.serves or not g.cast_loose:
                continue
            if quarters is not None:
                hands = quarters.hands_at(g)
                wanted = max(1, quarters.wanted_at(g))
                share = min(1.0, len(hands) / wanted)
            else:
                share = 1.0
            if share <= 0.0:
                continue
            off = _wrap_deg(want - g.train_deg)
            step = PIVOT_TRAIN_DEG_S * share * dt
            g.train_deg = _wrap_deg(g.train_deg + max(-step, min(step, off)))

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
        if mag.has(gun.kind, gun.pounder, want):
            # the shot is there again (a receipt): its want may be told again when it is out
            self._fell_back.discard((gun.pounder, want.value))
            return want
        if want is not Charge.ROUND and mag.has(gun.kind, gun.pounder, Charge.ROUND):
            key = (gun.pounder, want.value)
            if key not in self._fell_back:
                self._fell_back.add(key)
                self.ship.note(
                    "notable",
                    "guns.magazine_empty",
                    f"The gunner reports no more {_charge_words(want)} for the "
                    f"{self._calibre_words(gun)}: they load with round shot.",
                    gun.id,
                    {"pounder": gun.pounder, "charge": want.value, "instead": "round"},
                )
            return Charge.ROUND
        return None

    def _calibre_words(self, gun: Gun) -> str:
        """The guns whose shot is out, as the gunner says it: by calibre ('the 12-pounders')
        where two kinds of the fit share the calibre, for the shot is shared by calibre;
        else by kind ('long 3-pounders'), as before."""
        if any(g.pounder == gun.pounder and g.kind != gun.kind for g in self.ship.guns.values()):
            calibre = "half" if gun.pounder == 0.5 else f"{gun.pounder:g}"
            return f"{calibre}-pounders"
        return f"{gun.kind_words}s"

    def _same_guns(self, gun: Gun) -> int:
        return sum(
            1 for g in self.ship.guns.values() if g.kind == gun.kind and g.pounder == gun.pounder
        )

    def _phases(self, gun: Gun) -> tuple[tuple[str, float], ...]:
        phases = PHASES.get(gun.kind, PHASES["long"])
        if gun.kind == "long" and gun.weight_cwt > 0.0:
            share = max(LIGHT_GUN_SHARE_FLOOR, min(1.0, gun.weight_cwt / REFERENCE_CWT))
            return tuple((name, s * share) for name, s in phases)
        return phases

    def _work(self, gun: Gun, dt_eff: float, mag: Any, tick: int) -> None:
        svc = self.services[gun.id]
        phases = self._phases(gun)
        # a gun named to fire is served live while it is exercised (`serve_by_name`)
        dumb = self.exercise is not None and self.exercised(gun) and gun.id not in self.single
        svc.stalled = ""
        if svc.idle:
            if dumb and gun.loaded:
                # dumb show with the gun loaded: run out and pointed, the charge kept (a
                # swivel pointed only)
                start = "point" if gun.kind == "swivel" else "run out"
                svc.phase = next(i for i, (name, _) in enumerate(phases) if name == start)
                svc.began_tick = None
            elif gun.loaded:
                # begin where the gun stands: loaded wants running out and priming only
                svc.phase = next(
                    i
                    for i, (name, _) in enumerate(phases)
                    if name == ("run out" if not gun.run_out and gun.kind != "swivel" else "prime")
                )
                svc.began_tick = None
            else:
                svc.phase = 0
                svc.began_tick = tick  # the whole cycle, timed for the drill
            svc.left_s = phases[svc.phase][1]
        left = dt_eff
        while left > 0.0 and not svc.idle:
            name = phases[svc.phase][0]
            if (
                name == "cartridge"
                and not dumb
                and not gun.loaded
                and svc.left_s >= phases[svc.phase][1]
            ):
                # the powder comes up: a filled cartridge and the shot taken from the
                # magazine as the loading begins (in dumb show nothing is taken)
                charge = self._charge_for(gun, mag)
                if charge is None:
                    svc.stalled = "no cartridge"
                    if (
                        mag.filled_of(gun.kind, gun.pounder) <= 0
                        and (mag.level or {}).get((gun.kind, float(gun.pounder)), 0) > 0
                        and mag.powder_lb >= mag.charge_of(gun.kind, gun.pounder)
                    ):
                        # none filled, and powder below for a kind the gunner fills (one
                        # with a level): the gun waits at the cartridge, its phase and
                        # seconds kept, while the gunner fills
                        self._say_filling(gun, mag)
                        return
                    # none filled, and no powder for it or no level the gunner fills to:
                    # the magazine is out (as before)
                    key = (gun.kind, gun.pounder)
                    if self._said_out is None:
                        self._said_out = set()
                    if key not in self._said_out:
                        self._said_out.add(key)
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
                mag.take(gun.kind, gun.pounder, charge)
                if self._said_out:
                    # a cartridge again: the magazine's running out may be told again
                    self._said_out.discard((gun.kind, gun.pounder))
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
                self._cycle_done(gun, svc, tick, dumb)
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
                self._cycle_done(gun, svc, tick, dumb)
                break
            svc.left_s = phases[svc.phase][1]
            if phases[svc.phase][0] == "point" and svc.began_tick is not None:
                # the gun pointed: a live gun is ready now and fires as it bears (its point is
                # not worked: `ready`), so the cycle from the sponge is timed here; in dumb
                # show the round ends here, at the action's pace
                seconds = self._timed(gun, svc, tick)
                if dumb:
                    self._dumb_round(gun, svc, seconds)
                    break

    def _say_filling(self, gun: Gun, mag: Any) -> None:
        """The guns waiting on the gunner, told once an outage of their kind (the outage
        ends when the kind is back at its level: `combat.filling.fill_tick`)."""
        key = (gun.kind, gun.pounder)
        if self._said_filling is None:
            self._said_filling = set()
        if key in self._said_filling:
            return
        self._said_filling.add(key)
        n = self._same_guns(gun)
        words = gun_words(gun.kind, gun.pounder, n)
        wait = "the gun waits" if n == 1 else "the guns wait"
        if mag.filling_held:
            text = (
                f"No more filled cartridges for the {words}, and {wait}: the filling stopped "
                "by order; say 'fill cartridges'."
            )
        else:
            text = (
                f"No more filled cartridges for the {words}: the gunner is filling, and {wait} "
                "on him."
            )
        self.ship.note(
            "notable",
            "guns.filling",
            text,
            gun.id,
            {
                "kind": gun.kind,
                "pounder": gun.pounder,
                "powder_lb": round(float(mag.powder_lb), 4),
                "held": bool(mag.filling_held),
            },
        )

    def _cycle_done(self, gun: Gun, svc: Service, tick: int, dumb: bool) -> None:
        """A gun's phases done (the point worked through: a loaded gun in dumb show, run out
        and pointed with its charge kept): in dumb show the round counted."""
        if svc.began_tick is not None:
            self._timed(gun, svc, tick)
        svc.phase = -1
        if dumb:
            self._dumb_round(gun, svc, None)

    def _timed(self, gun: Gun, svc: Service, tick: int) -> float:
        """A full cycle timed for the drill, from the sponge (a swivel's from its
        cartridge) to the point, in seconds: the ticks it took, this one counted."""
        seconds = float(tick - svc.began_tick + 1)
        svc.began_tick = None
        d = self.drill_of(gun.id)
        d.cycles += 1
        d.total_s += seconds
        d.best_s = seconds if d.best_s is None else min(d.best_s, seconds)
        return seconds

    def _dumb_round(self, gun: Gun, svc: Service, seconds: float | None) -> None:
        """A round in dumb show: counted for the drill and the minute's line, and the gun
        run in again (unprimed when empty), its cycle to begin afresh."""
        self.drill_of(gun.id).dumb += 1
        gun.run_out = False
        if not gun.loaded:
            gun.primed = False
        svc.phase = -1
        svc.began_tick = None
        if self._dumb is None:
            self._dumb = []
        self._dumb.append((gun.id, seconds))

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
        if gun.place == "pivot":
            # within its arc over either side, and trained round on her
            off_bow = abs(_wrap_deg(deg))
            lo, hi = pivot_arc(gun)
            in_arc = lo <= off_bow <= hi
            return in_arc and abs(_wrap_deg(gun.train_deg - deg)) <= PIVOT_ON_DEG
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
        # the single guns and the gun to leeward: by name, once each, at whatever bears; a
        # gun whose port is shut does not fire (package 75)
        for gid in list(self.single):
            g = ship.guns.get(gid)
            if g is None or gid in self._shut or not self.ready(g):
                continue
            self.single.remove(gid)
            self._discharge(g, quarters, firer, target, relative, rng, tick, resolve)
        if self.exercise is not None:
            # dumb show: no gun fires but by name, and no broadside at the word
            self.word = None
            return
        if target is None or relative is None:
            self.word = None
            return
        # a gun captain fires at what his gun can throw to: a mark beyond its random range
        # is not fired at (Douglas 1820 on the waste of powder at long shot; judgement); a
        # gun whose port is shut, not at all (package 75)
        ready = [
            g
            for g in ship.guns.values()
            if g.id not in self._shut
            and self.ready(g)
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
        # a shot at a mark is practice: counted apart, so that nothing of the action's (the
        # morale's engagement, the fire opened) takes it for firing on a sail
        at_mark = target is not None and bool(getattr(target, "mark", ""))
        if at_mark:
            self.last_practice_tick = tick
        else:
            self.last_fired_tick = tick
        self.services[gun.id].phase = -1
        self.drill_of(gun.id).live += 1
        hands = quarters.hands_at(gun) if quarters is not None else []
        if target is None or relative is None or charge is Charge.BLANK or self.across_bows:
            # a blank charge, a shot across her bows, or no mark (the shot into the sea):
            # nothing struck
            if charge is Charge.BLANK:
                outcome = "blank"
            elif self.across_bows:
                outcome = "across her bows"
            else:
                outcome = "into the sea"
            self.across_bows = False
            self.volleys.append(Volley(gun.id, charge, outcome))
            return
        if not at_mark and target.id not in self.opened_fire_at:
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
            size=getattr(target, "size", None),
        )
        high = reach > target.range_m * 1.5  # laid to carry well over her: high
        if reach < target.range_m * 0.95:
            outcome = "short"
        elif rng.random() < p:
            outcome = "struck"
        else:
            outcome = "over" if (high or rng.random() < 0.5) else "wide"
        volley = Volley(gun.id, charge, outcome, mark=target.mark if at_mark else "")
        if outcome == "struck":
            volley.seen = resolve(self, gun, charge, target, high=high, rng=rng, tick=tick)
        if at_mark:
            # the fall of shot at the mark by whole cables, a cable at the least as the deck
            # estimates a range (`geo.estimate_words`; the review's finding: a cask struck at
            # 23 m was "at a cable" in the struck line and "0 cables" in the reading), the
            # notional mark's marked so (the reading says its hits "on the mark")
            falls = self.drill_of(gun.id).falls
            cables = max(1, int(round(target.range_m / units.CABLE)))
            fall = f"{cables} {outcome}" + (" notional" if target.mark == "notional" else "")
            falls[fall] = falls.get(fall, 0) + 1
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
        sea = sum(1 for v in volleys if v.outcome == "into the sea")
        seen = [w for v in volleys for w in v.seen]
        at = f" at {self.target_words}" if self.target_words else ""
        if sea and n == sea:
            text = f"Fired {number_words(n)} gun{'s' if n != 1 else ''}, the shot into the sea."
        elif n == blank:
            across = any(v.outcome == "across her bows" for v in volleys)
            text = (
                f"Fired {number_words(n)} gun{'s' if n != 1 else ''}"
                + (" across her bows" if across else "")
                + ", a blank charge."
            )
        else:
            fell = []
            # at a mark (practice): the cask struck, the notional mark's shot on it
            on_cask = sum(1 for v in volleys if v.outcome == "struck" and v.mark == "cask")
            on_mark = sum(
                1 for v in volleys if v.outcome == "struck" and v.mark and v.mark != "cask"
            )
            struck_her = struck - on_cask - on_mark
            if struck_her:
                fell.append(f"{number_words(struck_her)} struck her")
            if on_cask:
                fell.append(f"{number_words(on_cask)} struck the mark")
            if on_mark:
                fell.append(f"{number_words(on_mark)} on the mark")
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
            if sea:
                fell.append(f"{number_words(sea)} into the sea")
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
        if sea:
            data["sea"] = sea
        marks = [v.mark for v in volleys if v.mark]
        if marks:
            data["mark"] = marks[0]
        return text, data


def _of_exercise(side: str | None, gun: Gun) -> bool:
    """Whether the gun is of the battery `side` exercises in dumb show: that side, or
    either side for a gun with none (the pivot); none while `side` is None."""
    if side is None:
        return False
    return side == "both" or gun.side is None or gun.side == side


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
    starboard). A pivot gun is on the side it is trained to."""
    side = gun.side
    if gun.place == "pivot":
        side = "starboard" if gun.train_deg > 0.0 else "larboard"
    if side is None:
        return False
    return (heel_deg > 0.0) == (side == "starboard")


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


_TEENS = ("thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen")
_TENS = ("", "", "twenty", "thirty", "forty", "fifty", "sixty")


def count_words(n: int) -> str:
    """A count to sixty in words: 'sixteen', 'twenty', 'forty-five' (`number_words` says
    those to twelve and the figures past them, so the teens and the tens are said here:
    truth 7-164 found 'a minute and 16 seconds' beside 'a minute and twenty seconds' in
    the practice's reading); the figures beyond."""
    if 13 <= n < 20:
        return _TEENS[n - 13]
    if n < 20:
        return number_words(n)
    tens, ones = divmod(n, 10)
    if tens >= len(_TENS):
        return str(n)
    return _TENS[tens] + (f"-{number_words(ones)}" if ones else "")


def seconds_words(seconds: float) -> str:
    """'forty seconds', 'a minute', 'a minute and twenty seconds', 'two minutes and five
    seconds' (to the second; the deck's words, the practice's reading's and the drill's
    minute line's alike)."""
    s = int(round(seconds))
    minutes, rest = divmod(s, 60)
    tail = f"{count_words(rest)} second{'s' if rest != 1 else ''}"
    if minutes == 0:
        return tail
    head = "a minute" if minutes == 1 else f"{count_words(minutes)} minutes"
    return head + (f" and {tail}" if rest else "")


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
