"""The evolution runner: starts evolutions, walks their steps tick by tick, logs.

How it fits together
--------------------

``Runner(ship)`` makes one runner for a ship and registers it as
``ship.extra["evolutions"]`` so the Orders layer can find it. The World's
stepper calls ``runner.step(ship, dt, wind)`` once per tick, *before* the
physics, so that any sail set or yard braced this tick is felt by the
physics in the same tick.

``start(ship, evolution_id, subject_id, params)`` looks the evolution up in
the registry, finds the subject (a sail, a yard, or the ship itself for a
manoeuvre), checks that the evolution applies to that kind of part and
that its preconditions hold, and then either begins it at once or, if
another evolution is already at work on the same parts, queues it to
follow. A failed precondition raises ``OrderError`` with the reason in
words, exactly as the file gives it, so the order is rejected in the log
with a sentence a sailor would say.

Each tick, every running evolution advances through its current step.
A step's nominal ``duration_s`` is stretched by the *weather factor*:
1.0 in light airs on an even keel, rising to 2.0 in thirty knots of wind
with the ship heeled twenty-five degrees (spec §8.4). While a step runs,
its ``ramp`` targets move smoothly from where they were to where the step
sends them (a yard being braced round). When it ends, its ``sets`` are
applied (a sail's state becomes ``loosed``), its ``log`` line is noted if
it has one, and the next step begins after the ``requires`` conditions are
checked again. The last step's end completes the evolution and writes the
file's ``on_complete`` line to the log under its own kind (``sail.set``,
``yard.braced``...). A ``requires`` condition that stops holding mid-way,
or a ``via`` line found parted, fails the evolution with ``on_fail``.

Two evolutions are *serialised* when they would touch the same part: the
runner records which parts each running evolution holds (its subject, and
every object whose attribute a step sets or ramps) and a newcomer that
overlaps waits until those are released. Preconditions of a queued
evolution are checked when it actually begins, because the earlier one
may have changed the state it needs (set the topsail, then reef it).

Scripted manoeuvres (tack, wear, heave to, fill away) have no step list;
their file names a script in ``scripts.py`` that drives the helm targets
and the yards on a timeline and watches the ship's heading and speed to
decide how it ended. The runner treats a script like a single long step.

Hands (milestone 3, spec M3 §3). When the ship carries a crew
(``ship.extra["crew"]``, mustered by ``make_world``), an evolution asks for
the hands its file's ``crew:`` line names when it begins, and holds them
until it ends (``crew/hands.py``). With enough hands it runs at the file's
pace; short but workable, it begins and goes slower in proportion, with a
routine line in the log; with fewer than half, it waits for hands, says so
once, and is tried again every tick. Every step's time, and every script's
pace, is multiplied by the *crew factor* of the hands actually at work
(numbers, rating and fatigue). An evolution whose file says ``hands: all``
is a call for all hands, a pool action: it turns the watch below up through
the routine, takes the idle hands and everyone who comes up, and the hands
of earlier work join it as that work finishes (the per-tick top-up), so it
begins short and speeds up; it pipes down when it ends unless the captain
called all hands himself. Only a manoeuvre (its file says ``belays: true``:
tack, wear, box-haul, lie a-try) also belays the step-list work in hand,
which holds its progress and resumes, hands permitting, when the all-hands
work is done: the owner's ruling of 2026-09-29 at gate 4c (spec M3 §3.4).
Sending down the topgallant masts belays the work on those masts' sails
alone, which it clears away (`Script.clears`).
Who is on deck is the
watch bill's question (``crew/bill.py``), asked at ``Runner.clock``; the
composer sets that to the World's clock, and without it the bill is read at
``DEFAULT_WATCH_TIME``. A ship without a crew takes the milestone 2
behaviour exactly: every request is met and the crew factor is 1.0.

Nothing here is random. Given the same ship, wind and orders the same
ticks produce the same log.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.crew import bill, hands
from freesail.crew.model import Crew, number_words
from freesail.evolutions import expr, registry
from freesail.evolutions.scripts import SCRIPTS, Script
from freesail.ship.graph import Ship
from freesail.ship.parts import Line, LineState, Part, Sail, SailState, Spar
from freesail.ship.schema import YARD_LIKE_CLASSES
from freesail.ship.stub import OrderError

if TYPE_CHECKING:
    from freesail.physics.wind import Wind

# ---------------------------------------------------------------------------
# The weather factor (spec §8.4)
# ---------------------------------------------------------------------------

PROGRESS_EPSILON = 1e-9  # so that ninety ticks of 1/90 count as a whole step
LIGHT_AIRS_KN = 4.0  # up to here the crew works at the nominal pace
HARD_WIND_KN = 30.0  # here the wind alone adds half again to every duration
HARD_HEEL_DEG = 25.0  # and this much heel adds the other half


def weather_factor(wind_speed_ms: float, heel_rad: float) -> float:
    """How much longer everything takes because of wind and heel.

    1.0 in light airs on an even keel; 1.5 in thirty knots upright, or in a
    calm heeled twenty-five degrees; 2.0 with both. Never less than 1.0.
    """
    kn = units.ms_to_knots(wind_speed_ms)
    wind_part = _clamp((kn - LIGHT_AIRS_KN) / (HARD_WIND_KN - LIGHT_AIRS_KN), 0.0, 1.0)
    heel_part = _clamp(abs(units.rad_to_deg(heel_rad)) / HARD_HEEL_DEG, 0.0, 1.0)
    return 1.0 + 0.5 * wind_part + 0.5 * heel_part


def _clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


# ---------------------------------------------------------------------------
# Hands (spec M3 §3)
# ---------------------------------------------------------------------------

# When no clock has been given the runner (a ship stepped without a World, as in many
# tests), the watch bill is read at this time: the default scenario's start, four in the
# morning, the starboard watch on deck and the idlers below.
DEFAULT_WATCH_TIME = datetime(1805, 6, 1, 4, 0, 0)

# What a waiting instance waits for, besides its turn at a part another evolution holds.
WAITING_FOR_HANDS = "hands"

# How many pieces of other work a log line names before it says "at other work".
MAX_WORK_NAMED = 3

# A party the captain names for the work (`hands_from`), in the log's words (package 29c).
_WATCHES = ("starboard", "larboard")
_PARTY_WORDS = {
    "starboard": "starboard watch",
    "larboard": "larboard watch",
    "forecastle": "forecastlemen",
    "fore_top": "fore topmen",
    "main_top": "main topmen",
    "mizzen_top": "mizzen topmen",
}


class PartyTooSmall(OrderError):
    """A named party with fewer than half the hands the work wants (package 29c): the
    sentence names the party, the work and both numbers, and stands alone in the order's
    line."""


# How a sail is left when its work is belayed, by its state (package 29c); a sail set
# is left as `describe_state` says ("set", "set, 1 reef").
_SAIL_LEFT = {
    SailState.FURLED: "furled",
    SailState.IN_THE_GEAR: "hanging in its gear",
    SailState.LOOSED: "loosed and hanging from the yard",
    SailState.SHEETED: "sheeted home and not hoisted",
    SailState.GOOSE_WINGED: "goose-winged",
    SailState.UNBENT: "unbent",
    SailState.BLOWN_OUT: "blown out",
}


# ---------------------------------------------------------------------------
# Names for the log
# ---------------------------------------------------------------------------

_SIDES = ("starboard", "larboard")


def part_name(ship: Ship, part_id: str) -> str:
    """A sailor's name for a part id: 'fore.topsail' -> 'fore topsail',
    'fore.topmast.studdingsail.starboard' -> 'starboard fore topmast studdingsail'.
    The ship file's first plain alias for the part wins ('spanker', 'foresail')."""
    for alias, target in ship.aliases.items():
        if target == part_id and not alias.startswith("the "):
            return alias
    words = part_id.replace("_", " ").split(".")
    if len(words) > 1 and words[-1] in _SIDES:
        words = [words[-1], *words[:-1]]
    return " ".join(words)


class _SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


# ---------------------------------------------------------------------------
# A running (or waiting) evolution
# ---------------------------------------------------------------------------


@dataclass
class Instance:
    evo: registry.Evolution
    subject: Part | Ship
    subject_id: str
    params: dict[str, Any]
    holds: set[str] = field(default_factory=set)
    waiting: bool = True
    step_index: int = -1
    progress: float = 0.0  # 0..1 through the current step
    ramp_start: dict[str, float] = field(default_factory=dict)
    ramp_target: dict[str, float] = field(default_factory=dict)
    script: Script | None = None
    order: int = 0
    waiting_for: str | None = None  # "hands" while it waits for hands; else None
    paused: bool = False  # belayed while all hands are about ship (spec M3 §3.4)
    want: hands.CrewRequest | None = None  # the file's crew line, read when there is a crew
    assignment: hands.Assignment | None = None  # the hands it holds
    all_hands: bool = False  # began as a call for all hands
    short_logged: bool = False
    wait_line: str = ""  # the line it said when it first had to wait for hands
    given: int | None = None  # the order that started it (`Runner.giving`), for `belay that`

    @property
    def inst_id(self) -> str:
        """The name the sailors it holds carry in ``Sailor.at``."""
        return f"{self.evo.id}#{self.order}"

    @property
    def step(self) -> registry.Step | None:
        if 0 <= self.step_index < len(self.evo.steps):
            return self.evo.steps[self.step_index]
        return None

    @property
    def step_name(self) -> str:
        if self.waiting:
            return "waiting"
        if self.paused:
            return "paused"
        if self.script is not None:
            return self.script.phase
        step = self.step
        return step.do if step else "done"


# ---------------------------------------------------------------------------
# The runner
# ---------------------------------------------------------------------------


class Runner:
    """Runs evolutions for one ship. See the module docstring."""

    SHIP_SUBJECTS = ("ship", "her", "the ship")

    def __init__(self, ship: Ship):
        self.ship = ship
        self.instances: list[Instance] = []
        self._counter = 0
        self._last_factor = 1.0
        # Groups of evolutions from one order ("setting plain sail") that have said once
        # that they must wait for hands (package 20): the rest of the group waits quietly.
        self._groups_waiting: set[str] = set()
        # The ship's clock, for the watch bill: the composer sets it to the World's clock.
        # None reads the bill at DEFAULT_WATCH_TIME.
        self.clock: Any | None = None
        # The braces of one trim, logged as one line when the last is done (package 29b,
        # playtest 7's finding 6: a trim logged twelve lines twice): the key an order's
        # evolutions carry in `params["log_group"]`, and the yards done so far with their
        # angles from square.
        self._log_groups: dict[str, list[tuple[str, float]]] = {}
        self._log_group_count = 0
        # The order being carried out (`giving`), so that every evolution it starts carries
        # its number and `belay that` finds the last order's work (package 29c).
        self._giving: int | None = None
        self._given_count = 0
        ship.extra["evolutions"] = self

    # -- the contract --------------------------------------------------------

    def start(
        self,
        ship: Ship,
        evolution_id: str,
        subject_id: str,
        params: dict[str, Any] | None = None,
    ) -> str:
        """Begin an evolution, or queue it behind one already at work on the same
        parts. Returns the log sentence. Raises OrderError with the reason if
        the evolution does not apply or a precondition fails."""
        evo = registry.get(evolution_id)
        if evo is None:
            raise OrderError(f"There is no such evolution as '{evolution_id}'.")
        subject, sid = self._resolve_subject(ship, subject_id)
        self._check_applies(evo, subject, sid, ship)
        merged = dict(evo.params)
        merged.update(params or {})
        inst = Instance(evo=evo, subject=subject, subject_id=sid, params=merged)
        self._counter += 1
        inst.order = self._counter
        inst.given = self._giving
        if evo.script is not None:
            script_cls = SCRIPTS.get(evo.script)
            if script_cls is None:
                raise OrderError(f"'{evolution_id}' names an unknown script '{evo.script}'.")
            inst.script = script_cls(ship, merged, evo.timing)
        inst.holds = self._holds(ship, inst)
        if self._crew(ship) is not None:
            try:
                inst.want = hands.CrewRequest.from_mapping(evo.crew)
            except hands.CrewRequestError as e:
                raise OrderError(f"{evolution_id}: {e}") from None
            self._check_party(ship, inst)
        blockers = [
            other for other in self.instances if other.holds & inst.holds and other is not inst
        ]
        if blockers:
            # The subject is busy: the newcomer waits its turn. Its preconditions
            # are checked when it begins, since the earlier work may satisfy them.
            self.instances.append(inst)
            first = blockers[0]
            return (
                f"'{self._describe(inst).capitalize()}' will follow "
                f"'{self._describe(first)}', which the hands are still at."
            )
        # Free to begin now: a failing precondition rejects the order outright.
        reason = self._failing_condition(ship, inst, evo.preconditions + evo.requires)
        if reason is not None:
            raise OrderError(reason)
        self.instances.append(inst)
        if not self._begin(ship, inst):
            return inst.wait_line
        return self._format(inst, evo.on_start.log)

    def step(self, ship: Ship, dt: float, wind: Wind) -> None:
        """Advance every running evolution by one tick, then start any that were
        waiting and are now free. Call once per tick, before the physics."""
        self._last_factor = weather_factor(wind.effective_speed, ship.dyn.heel)
        crew = self._crew(ship)
        if crew is not None:
            calls = ship.extra.get("watch_calls")  # a watch turned up by an order (package 20)
            if calls:
                calls[:] = [c for c in calls if c.tick(self.clock or DEFAULT_WATCH_TIME)]
            self._top_up_all_hands(crew)
        for inst in list(self.instances):
            if inst.waiting or inst.paused:
                continue
            if inst.script is not None:
                self._tick_script(ship, inst, dt, wind)
            else:
                self._tick_steps(ship, inst, dt)
        self._start_waiting(ship)

    def new_log_group(self) -> str:
        """A key for the evolutions of one order that log as one line (a trim's braces)."""
        self._log_group_count += 1
        return f"group#{self._log_group_count}"

    def in_progress(self) -> list[dict[str, Any]]:
        """What is going on, for the state snapshot."""
        out = []
        for inst in self.instances:
            out.append(
                {
                    "id": inst.evo.id,
                    "subject": inst.subject_id,
                    "step": inst.step_name,
                    "remaining_s": self._remaining_s(inst),
                    "waiting": inst.waiting,
                    "waiting_for": inst.waiting_for,
                    "paused": inst.paused,
                    "hands": inst.assignment.got if inst.assignment is not None else 0,
                }
            )
        return out

    # -- belaying work (package 29c) -------------------------------------------

    @contextmanager
    def giving(self, text: str = "") -> Iterator[int]:
        """While an order is carried out (`orders.handle`), every evolution it starts is
        marked with the order's number, so that `belay that` finds the last order's work
        whether it started one evolution or a dozen."""
        self._given_count += 1
        outer, self._giving = self._giving, self._given_count
        try:
            yield self._given_count
        finally:
            self._giving = outer

    def work(self) -> list[Instance]:
        """The work in hand or waiting, in the order it was given: every evolution the
        runner holds, running, waiting its turn or for hands, or belayed by a manoeuvre."""
        return sorted(self.instances, key=lambda i: i.order)

    def last_order_work(self) -> list[Instance]:
        """The work of the last order given whose work is still in hand or waiting (`belay
        that`): the newest evolution the runner holds, and every other that the same order
        started. An evolution started without an order (a test's direct `start`) is an
        order of its own."""
        work = self.work()
        if not work:
            return []
        last = work[-1]
        if last.given is None:
            return [last]
        return [i for i in work if i.given == last.given]

    def doing(self, inst: Instance) -> str:
        """The work in words as the log names it: 'reefing the mainsail', 'tacking ship'."""
        return self._doing(inst)

    def belay(self, ship: Ship, insts: list[Instance]) -> list[dict[str, Any]]:
        """Belay work in hand or waiting at the captain's word (`belay <the work>`, `belay
        that`, `belay all work`; package 29c). Each is gone, not paused: its hands are
        released and nothing of it resumes. What a finished step did stays done and a step
        half done is left where it stands (a yard half braced round stays at its angle; a
        sail half set is in the state its last finished step left it), since a step's
        `sets` are applied only when it ends. An all-hands evolution belayed ends the call
        as its end would (the hands piped down unless the captain called them). Returns,
        for each, what was belayed and how it was left, for the order's one line. This is
        not the manoeuvres' belay (decision 25; `_call_all_hands`), which holds the work's
        progress to resume it and keeps its own line."""
        out: list[dict[str, Any]] = []
        for inst in sorted(insts, key=lambda i: i.order):
            if inst not in self.instances:
                continue
            was = "waiting" if inst.waiting else "belayed" if inst.paused else "in hand"
            entry: dict[str, Any] = {
                "evolution": inst.evo.id,
                "subject": inst.subject_id,
                "doing": self._doing(inst),
                "was": was,
                "step": None if inst.waiting else inst.step_name,
                "left": self._left_words(ship, inst),
            }
            if isinstance(inst.subject, Sail):
                entry["state"] = inst.subject.state.value
                entry["reefs"] = inst.subject.reefs
            self._remove(ship, inst)
            key = inst.params.get("log_group")
            if key:
                self._group_done(ship, inst, key)  # the braces of a trim already done
            self._after_all_hands(ship, inst)
            out.append(entry)
        return out

    def _left_words(self, ship: Ship, inst: Instance) -> str:
        """How a piece of work is left when it is belayed, in words for the log."""
        if inst.waiting:
            why = "for hands" if inst.waiting_for == WAITING_FOR_HANDS else "its turn"
            return f"not begun, it was waiting {why}"
        subject = inst.subject
        if isinstance(subject, Ship):
            phase = inst.script.phase.replace("_", " ") if inst.script is not None else ""
            at = f" at {phase}" if phase and phase not in ("ready", "done") else ""
            return f"the helm and the yards left as they stand{at}"
        name = part_name(ship, inst.subject_id)
        if isinstance(subject, Sail):
            return f"the {name} left {_SAIL_LEFT.get(subject.state, subject.describe_state())}"
        if isinstance(subject, Spar) and subject.cls in YARD_LIKE_CLASSES:
            deg = abs(units.rad_to_deg(subject.brace_angle))
            return f"the {name} left {deg:.0f}° from square"
        if isinstance(subject, Line):
            return f"the {name} left {subject.state.value}"
        return f"the {name} left as it stands"

    def _check_party(self, ship: Ship, inst: Instance) -> None:
        """An order that names its hands (`with the idlers`, `send the starboard watch
        aloft to ...`) whose party has fewer than half the hands the work wants is refused
        at once, in words with the numbers, since waiting would not bring them (playtest 8:
        the schooner's few idlers held the mainsail's reef, and every later order on the
        mainsail behind it, for the rest of the session). The general case, the watch on
        deck short of hands, still waits (spec M3 §3.2): hands come free and come up."""
        pick = inst.params.get("hands_from")
        crew = self._crew(ship)
        want = inst.want
        if not pick or crew is None or want is None or want.all_hands or not want.hands:
            return
        aloft = self._aloft(inst)
        wanted = min(int(want.hands), hands.company_can_give(crew, aloft))
        party = [
            s
            for s in crew.sailors
            if pick in (s.watch.value, s.station.value) and hands.can_work(s, aloft=False)
        ]
        able = [s for s in party if hands.can_work(s, aloft)]
        if wanted <= 0 or len(able) >= wanted * hands.SHORT_HANDED_SHARE:
            return
        who = _PARTY_WORDS.get(pick, pick.replace("_", " "))
        count = f"The {who} are {number_words(len(party))}"
        if aloft and len(able) < len(party):
            goes = "none of them goes" if not able else f"{number_words(len(able))} of them go"
            count += f", and {goes} aloft"
        remedy = "Call all hands." if pick in _WATCHES else "Call all hands, or name the watch."
        raise PartyTooSmall(f"{count}; {self._doing(inst)} wants {number_words(wanted)}. {remedy}")

    # -- subjects ------------------------------------------------------------

    def _resolve_subject(self, ship: Ship, subject_id: str | None) -> tuple[Part | Ship, str]:
        if subject_id is None or subject_id in self.SHIP_SUBJECTS or subject_id == ship.name:
            return ship, ship.name
        part = ship.parts.get(subject_id)
        if part is None:
            target = ship.aliases.get(subject_id)
            part = ship.parts.get(target) if target else None
        if part is None:
            raise OrderError(f"There is no part called '{subject_id}' in {ship.name}.")
        return part, part.id

    @staticmethod
    def _check_applies(evo: registry.Evolution, subject: Part | Ship, sid: str, ship: Ship) -> None:
        wanted = str(evo.applies_to.get("class"))
        if wanted == "ship":
            if isinstance(subject, Ship):
                return
            raise OrderError(
                f"'{evo.verb}' is an order for the ship, not for the {part_name(ship, sid)}."
            )
        if isinstance(subject, Ship):
            raise OrderError(f"'{evo.verb}' needs a part to work on; say which.")
        kind = (
            "sail" if isinstance(subject, Sail) else "line" if isinstance(subject, Line) else "spar"
        )
        if wanted == "sail" and isinstance(subject, Sail):
            return  # any sail: bending, unbending and shifting (package 19)
        if wanted == "spar" and isinstance(subject, Spar):
            return  # any spar: shifting one for a spare (package 30b)
        if wanted == "part" and isinstance(subject, Sail | Spar):
            return  # a spar or a sail: clearing a wreck (package 30b)
        if wanted == "yard":
            if isinstance(subject, Spar) and subject.cls in YARD_LIKE_CLASSES:
                return
            what = subject.cls.replace("_", " ") + ("" if kind == "spar" else f" {kind}")
            raise OrderError(
                f"The {part_name(ship, sid)} is a {what}, not a yard; it cannot be {evo.verb}d."
            )
        if subject.cls == wanted:
            return
        raise OrderError(
            f"The {part_name(ship, sid)} is a {subject.cls} {kind}; "
            f"'{evo.id}' is for a {wanted} sail."
        )

    # -- the expression environment -------------------------------------------

    def _env(self, ship: Ship, inst: Instance) -> expr.Env:
        subject = inst.subject
        names: dict[str, Any] = {
            "ship": ship,
            "dyn": ship.dyn,
            "subject": subject,
            "params": inst.params,
        }
        if isinstance(subject, Sail):
            names["sail"] = subject
        elif isinstance(subject, Spar):
            names["spar"] = subject
            if subject.cls in YARD_LIKE_CLASSES:
                names["yard"] = subject
        elif isinstance(subject, Line):
            names["line"] = subject

        def wrecked(x: Any) -> bool:
            if x is None:
                return False
            if isinstance(x, Sail):
                return x.wrecked or wrecked(ship.spar_chain(x))
            if isinstance(x, Spar):
                return x.wrecked or x.sent_down
            if isinstance(x, Line):
                return x.state is LineState.PARTED
            return any(wrecked(item) for item in x)

        def tack_sign(side: Any) -> float:
            if side in (None, "", "none"):
                side = ship.dyn.tack
            if side == "starboard":
                return 1.0
            if side in ("larboard", "port"):
                return -1.0
            raise expr.ExpressionError(f"'{side}' is not a side; say starboard or larboard.")

        def close_hauled() -> bool:
            awa = abs(ship.dyn.apparent_wind_angle)
            target = close_hauled_apparent_angle(ship)
            return abs(awa - target) <= units.deg_to_rad(10.0)

        def any_set(sails: Any) -> bool:
            return any(getattr(s, "is_set", False) for s in (sails or []))

        functions = {
            "yard_of": ship.yard_of,
            "sail_of": ship.sail_of,
            "halyard_of": ship.halyard_of,
            "spar_chain": ship.spar_chain,
            "spar_of_role": ship.spar_of_role,
            "mast_of": ship.mast_of,
            "parent_of": ship.parent_of,
            "sails_on": ship.sails_on,
            "sails_using": ship.sails_using,
            "braces_of": ship.braces_of,
            "sheets_of": ship.sheets_of,
            "lines_of": ship.lines_of,
            "line_of": ship.line_of,
            "wrecked": wrecked,
            "deg": units.deg_to_rad,
            "knots": units.knots_to_ms,
            "abs": abs,
            "min": min,
            "max": max,
            "clamp": _clamp,
            "tack_sign": tack_sign,
            "close_hauled": close_hauled,
            "any_set": any_set,
        }
        return expr.Env(names, functions)

    def _failing_condition(
        self, ship: Ship, inst: Instance, conditions: list[registry.Condition]
    ) -> str | None:
        """The reason (in words) of the first condition that does not hold, else None."""
        env = self._env(ship, inst)
        for cond in conditions:
            try:
                ok = expr.evaluate(cond.tree, env)
            except expr.ExpressionError as e:
                return f"{inst.evo.id}: the check '{cond.text}' could not be read ({e})"
            if not ok:
                return self._format(inst, cond.reason)
        if inst.script is not None:
            return inst.script.check(self._format_context(inst))
        return None

    # -- holds: which parts an evolution occupies ------------------------------

    def _holds(self, ship: Ship, inst: Instance) -> set[str]:
        held = {inst.subject_id}
        if inst.script is not None:
            held |= inst.script.holds()
            return held
        env = self._env(ship, inst)
        for step in inst.evo.steps:
            for obj_tree, _attr, _value in list(step.sets.values()) + list(step.ramp.values()):
                try:
                    obj = expr.evaluate(obj_tree, env)
                except expr.ExpressionError:
                    continue
                pid = getattr(obj, "id", None)
                if isinstance(pid, str):
                    held.add(pid)
                elif obj is ship:
                    held.add(ship.name)
        return held

    # -- beginning ---------------------------------------------------------------

    def _begin(self, ship: Ship, inst: Instance) -> bool:
        """Begin an instance whose parts are free. With a crew, it must get its hands
        first; without enough it waits for them and this returns False."""
        crew = self._crew(ship)
        if crew is not None and not self._take_hands(ship, inst, crew):
            return False
        inst.waiting = False
        inst.waiting_for = None
        inst.step_index = -1
        if inst.script is not None:
            inst.script.begin(self._format_context(inst))
            self._note(ship, inst, inst.evo.on_start)
            return True
        if not inst.params.get("log_group"):  # the order's own line said it for the group
            self._note(ship, inst, inst.evo.on_start)
        self._enter_next_step(ship, inst)
        return True

    def _start_waiting(self, ship: Ship) -> None:
        # Start waiting evolutions in the order they were given, when free.
        crew = self._crew(ship)
        for inst in sorted(self.instances, key=lambda i: i.order):
            if inst.paused and crew is not None:
                self._try_resume(ship, inst, crew)
                continue
            if not inst.waiting:
                continue
            busy = any(
                other is not inst and other.order < inst.order and other.holds & inst.holds
                for other in self.instances
            )
            if busy:
                continue
            reason = self._failing_condition(ship, inst, inst.evo.preconditions + inst.evo.requires)
            if reason is not None:
                self._fail(ship, inst, reason)
                continue
            self._begin(ship, inst)

    # -- stepping through a step list -----------------------------------------------

    def _enter_next_step(self, ship: Ship, inst: Instance) -> None:
        """Move to the next runnable step, or complete if there is none."""
        env = self._env(ship, inst)
        while True:
            inst.step_index += 1
            inst.progress = 0.0
            inst.ramp_start.clear()
            inst.ramp_target.clear()
            step = inst.step
            if step is None:
                self._complete(ship, inst)
                return
            reason = self._failing_condition(ship, inst, inst.evo.requires)
            if reason is not None:
                self._fail(ship, inst, reason)
                return
            try:
                if step.condition is not None and not expr.evaluate(step.condition, env):
                    continue
                if step.via is not None:
                    line = expr.evaluate(step.via, env)
                    if line is None:
                        continue  # this ship has no such line (a course has no halyard)
                    if getattr(line, "state", None) is LineState.PARTED:
                        self._fail(ship, inst, f"the {part_name(ship, line.id)} is parted")
                        return
                for key, (obj_tree, attr, value_tree) in step.ramp.items():
                    obj = expr.evaluate(obj_tree, env)
                    inst.ramp_start[key] = float(getattr(obj, attr))
                    inst.ramp_target[key] = float(expr.evaluate(value_tree, env))
            except (expr.ExpressionError, TypeError, ValueError) as e:
                self._fail(ship, inst, f"the step '{step.do}' could not be read ({e})")
                return
            if step.duration_s <= 0:
                self._finish_step(ship, inst)
                if inst not in self.instances:
                    return
                continue
            return

    def _tick_steps(self, ship: Ship, inst: Instance, dt: float) -> None:
        step = inst.step
        if step is None:
            return
        pace = step.duration_s * self._last_factor * self._crew_factor(inst, step.aloft)
        inst.progress = min(1.0, inst.progress + dt / pace)
        if inst.progress >= 1.0 - PROGRESS_EPSILON:
            inst.progress = 1.0
        self._apply_ramp(ship, inst, inst.progress)
        if inst.progress >= 1.0:
            self._finish_step(ship, inst)
            if inst in self.instances:
                self._enter_next_step(ship, inst)

    def _apply_ramp(self, ship: Ship, inst: Instance, fraction: float) -> None:
        step = inst.step
        if step is None or not step.ramp:
            return
        env = self._env(ship, inst)
        for key, (obj_tree, attr, _value) in step.ramp.items():
            obj = expr.evaluate(obj_tree, env)
            start, target = inst.ramp_start[key], inst.ramp_target[key]
            setattr(obj, attr, start + (target - start) * fraction)

    def _finish_step(self, ship: Ship, inst: Instance) -> None:
        step = inst.step
        if step is None:
            return
        env = self._env(ship, inst)
        try:
            self._apply_ramp(ship, inst, 1.0)
            for _key, (obj_tree, attr, value_tree) in step.sets.items():
                obj = expr.evaluate(obj_tree, env)
                _assign(obj, attr, expr.evaluate(value_tree, env))
        except (expr.ExpressionError, TypeError, ValueError) as e:
            self._fail(ship, inst, f"the step '{step.do}' could not be applied ({e})")
            return
        if step.log:
            ship.note("routine", "evolution.step", self._format(inst, step.log), inst.subject_id)

    # -- scripts ------------------------------------------------------------------

    def _tick_script(self, ship: Ship, inst: Instance, dt: float, wind: Wind) -> None:
        assert inst.script is not None
        inst.script.tick(
            dt,
            wind,
            self._last_factor * self._crew_factor(inst, getattr(inst.script, "aloft", False)),
        )
        if inst.script.status == "done":
            self._complete(ship, inst)
        elif inst.script.status == "failed":
            self._fail(ship, inst, inst.script.reason or "she would not answer")

    # -- ending -----------------------------------------------------------------------

    def _complete(self, ship: Ship, inst: Instance) -> None:
        self._remove(ship, inst)
        key = inst.params.get("log_group")
        if key and isinstance(inst.subject, Spar):
            deg = abs(units.rad_to_deg(inst.subject.brace_angle))
            self._log_groups.setdefault(key, []).append((inst.subject_id, deg))
            self._group_done(ship, inst, key)
        else:
            self._note(ship, inst, inst.evo.on_complete)
        self._after_all_hands(ship, inst)

    def _fail(self, ship: Ship, inst: Instance, reason: str) -> None:
        self._remove(ship, inst)
        self._note(ship, inst, inst.evo.on_fail, reason=reason)
        key = inst.params.get("log_group")
        if key:
            self._group_done(ship, inst, key)
        self._after_all_hands(ship, inst)

    def _group_done(self, ship: Ship, inst: Instance, key: str) -> None:
        """The last of a trim's braces is done: one line for all of them, "Braced twelve
        yards to the wind; 26° to 31° from square.", in the evolution's own kind and
        severity, its data naming every yard and its angle (package 29b)."""
        if any(i.params.get("log_group") == key for i in self.instances):
            return
        done = self._log_groups.pop(key, [])
        if not done:
            return
        degs = [round(d) for _, d in done]
        lo, hi = min(degs), max(degs)
        angle = f"{lo}° from square" if lo == hi else f"{lo}° to {hi}° from square"
        if len(done) == 1:
            text = f"Braced the {part_name(ship, done[0][0])}; {angle}."
        else:
            text = f"Braced {number_words(len(done))} yards to the wind; {angle}."
        outcome = inst.evo.on_complete
        data = {
            "evolution": inst.evo.id,
            "subjects": [sid for sid, _ in done],
            "brace_deg": {sid: round(d, 1) for sid, d in done},
        }
        ship.note(outcome.severity, outcome.kind, text, None, data)

    def _remove(self, ship: Ship, inst: Instance) -> None:
        if inst in self.instances:
            self.instances.remove(inst)
        group = inst.params.get("group")
        if group and not any(i.params.get("group") == group for i in self.instances):
            self._groups_waiting.discard(group)
        crew = self._crew(ship)
        if crew is not None and inst.assignment is not None:
            hands.release(crew, inst.inst_id)
            inst.assignment = None

    # -- hands (spec M3 §3) ----------------------------------------------------------

    @staticmethod
    def _crew(ship: Ship) -> Crew | None:
        crew = ship.extra.get("crew")
        return crew if isinstance(crew, Crew) else None

    def _on_deck(self, crew: Crew) -> list:
        when = self.clock if self.clock is not None else DEFAULT_WATCH_TIME
        return bill.on_deck(crew, when)

    def _pool(self, crew: Crew, inst: Instance) -> list:
        """The hands on deck an instance may draw on: the watch or station its order named
        (``params["hands_from"]``, package 20), else all of them."""
        pick = inst.params.get("hands_from")
        deck = self._on_deck(crew)
        return [s for s in deck if pick in (s.watch.value, s.station.value)] if pick else deck

    def _aloft(self, inst: Instance) -> bool:
        """Whether any of the work is aloft: then only hands who go aloft are taken. A
        script names its aloft phases in ``params.aloft`` (package 19). A step whose `if`
        does not hold now is not counted (package 29b: a sail set from the gear wants no
        hands aloft, its loosing skipped)."""
        if inst.script is not None:
            return bool(inst.params.get("aloft"))
        env: expr.Env | None = None
        for step in inst.evo.steps:
            if not step.aloft:
                continue
            if step.condition is None:
                return True
            env = env or self._env(self.ship, inst)
            try:
                if expr.evaluate(step.condition, env):
                    return True
            except expr.ExpressionError:
                return True
        return False

    def _want(self, inst: Instance) -> hands.CrewRequest:
        if inst.want is None:
            inst.want = hands.CrewRequest.from_mapping(inst.evo.crew)
        return inst.want

    def _subject_mast(self, ship: Ship, inst: Instance) -> str | None:
        """The mast the subject stands on ('fore', 'main', 'mizzen'), for the topmen."""
        if isinstance(inst.subject, Ship):
            return None
        try:
            mast = ship.mast_of(inst.subject)
        except (KeyError, AttributeError, TypeError):
            return None
        return mast.id.split(".")[0] if mast is not None else None

    def _crew_factor(self, inst: Instance, aloft: bool) -> float:
        if inst.assignment is None or inst.want is None:
            return 1.0
        return hands.crew_factor(inst.assignment, inst.want, aloft)

    def _all_hands_at_work(self, but: Instance | None = None) -> list[Instance]:
        return [
            i
            for i in self.instances
            if i.all_hands and not i.waiting and not i.paused and i is not but
        ]

    def _take_hands(self, ship: Ship, inst: Instance, crew: Crew) -> bool:
        """Ask for the instance's hands (spec M3 §3.1, §3.2). True if it may begin."""
        want = self._want(inst)
        # hands come free (earlier work done, the watch below coming up) join the all-hands
        # work already going before anything new may have them: a second all-hands evolution
        # waits for the first, as two always have (spec M3 §3.4)
        self._top_up_all_hands(crew)
        if want.all_hands:
            self._call_all_hands(ship, inst, crew)
        got = hands.request(
            crew,
            self._pool(crew, inst),
            inst.inst_id,
            want,
            self._subject_mast(ship, inst),
            aloft=self._aloft(inst),
        )
        if got.outcome == hands.TOO_FEW:
            inst.waiting = True
            inst.waiting_for = WAITING_FOR_HANDS
            if not inst.wait_line:
                # Of a group from one order, the first to wait says so for all, notable;
                # the rest say it routine (package 20). An order given singly is notable.
                group = inst.params.get("group")
                severity = "notable"
                if group and group in self._groups_waiting:
                    severity = "routine"
                    inst.wait_line = self._waiting_line(ship, inst, got)
                elif group:
                    self._groups_waiting.add(group)
                    inst.wait_line = self._group_waiting_line(ship, inst, group)
                else:
                    inst.wait_line = self._waiting_line(ship, inst, got)
                data = self._hands_data(inst, got)
                ship.note(severity, "evolution.waiting", inst.wait_line, inst.subject_id, data)
            return False
        inst.assignment = got
        inst.all_hands = want.all_hands
        if got.outcome == hands.SHORT:
            self._note_short(ship, inst, got)
        return True

    def _note_short(self, ship: Ship, inst: Instance, got: hands.Assignment) -> None:
        if inst.short_logged:
            return
        inst.short_logged = True
        others = self._other_work(inst)
        rest = f"the rest are {others}" if others else "there are no more on deck"
        n = got.got
        men = "hand" if n == 1 else "hands"
        text = f"Only {number_words(n)} {men} to {self._target(inst)}; {rest}."
        data = self._hands_data(inst, got)
        ship.note("routine", "evolution.short_handed", text, inst.subject_id, data)

    def _waiting_line(self, ship: Ship, inst: Instance, got: hands.Assignment) -> str:
        others = self._other_work(inst)
        crew = self._crew(ship)
        if others:
            called = crew is not None and crew.all_hands_called
            rest = f"{'the hands are' if called else 'the watch is'} {others}"
        else:
            spare = got.available
            rest = (
                "there are none to spare"
                if spare == 0
                else f"there are but {number_words(spare)} to spare"
            )
        return f"Not hands enough on deck to {self._describe(inst)}; {rest}."

    def _group_waiting_line(self, ship: Ship, inst: Instance, group: str) -> str:
        """'Setting plain sail: not hands enough for all at once; the watch takes the sails
        in turn.'"""
        crew = self._crew(ship)
        who = "the hands take" if crew is not None and crew.all_hands_called else "the watch takes"
        what = "the sails" if isinstance(inst.subject, Sail) else "them"
        head = group[:1].upper() + group[1:]
        return f"{head}: not hands enough for all at once; {who} {what} in turn."

    @staticmethod
    def _hands_data(inst: Instance, got: hands.Assignment) -> dict[str, Any]:
        return {
            "evolution": inst.evo.id,
            "subject": inst.subject_id,
            "hands_wanted": got.wanted,
            "hands_got": got.got if got.outcome != hands.TOO_FEW else got.available,
        }

    def _top_up_all_hands(self, crew: Crew) -> None:
        """Hands who have come on deck since an all-hands evolution began join it."""
        running = self._all_hands_at_work()
        if not running:
            return
        deck = self._on_deck(crew)
        for inst in sorted(running, key=lambda i: i.order):
            if inst.assignment is not None:
                hands.top_up(inst.assignment, deck, aloft=self._aloft(inst))

    def _call_all_hands(self, ship: Ship, inst: Instance, crew: Crew) -> None:
        """An all-hands evolution turns the hands up (spec M3 §3.4). A manoeuvre (its file
        says ``belays: true``) also belays the step-list work in hand, and sending down the
        topgallant masts the work on their sails (`_belays`); all-hands sail work leaves the
        rest to finish, and its hands join through the top-up (the owner's ruling of
        2026-09-29 at gate 4c)."""
        routine = ship.extra.get("routine")
        call = getattr(routine, "call_all_hands", None)
        if call is not None and not crew.all_hands_called:
            _record(ship, call(f"to {self._describe(inst)}"))  # the routine returns its line
        reason = self._format(inst, inst.evo.on_start.log).strip().rstrip(".!")
        reason = reason[:1].lower() + reason[1:]
        for other in sorted(self.instances, key=lambda i: i.order):
            if other is inst or other.waiting or other.paused or other.script is not None:
                continue
            if other.all_hands:
                continue  # two all-hands evolutions serialise by their holds, as before
            if not self._belays(inst, other):
                continue
            other.paused = True
            hands.release(crew, other.inst_id)
            other.assignment = None
            ship.note(
                "notable",
                "evolution.belayed",
                f"Belayed {self._doing(other)}: {reason}.",
                other.subject_id,
                {"evolution": other.evo.id, "subject": other.subject_id, "for": inst.evo.id},
            )

    @staticmethod
    def _belays(inst: Instance, other: Instance) -> bool:
        """Whether an all-hands evolution belays this step-list work in hand (spec M3
        §3.4, the owner's ruling of 2026-09-29 at gate 4c): a manoeuvre (``belays: true``)
        all of it; sending down the topgallant masts the work on those masts' sails, which
        it clears away (`Script.clears`); any other, nothing."""
        if inst.evo.belays:
            return True
        clears = inst.script.clears() if inst.script is not None else set()
        return bool(clears & other.holds)

    def _try_resume(self, ship: Ship, inst: Instance, crew: Crew) -> None:
        """A belayed instance takes up its work again when all hands are done, if it can
        have its hands; until then it stays belayed, its progress held."""
        if self._all_hands_at_work():
            return
        got = hands.request(
            crew,
            self._pool(crew, inst),
            inst.inst_id,
            self._want(inst),
            self._subject_mast(ship, inst),
            aloft=self._aloft(inst),
        )
        if got.outcome == hands.TOO_FEW:
            return
        # The world moved while the work lay belayed: a hoist half done must not finish
        # on a yard that has since been sent down (package 19's finding).
        reason = self._failing_condition(ship, inst, inst.evo.requires)
        if reason is not None:
            hands.release(crew, inst.inst_id)
            self._fail(ship, inst, reason)
            return
        inst.paused = False
        inst.assignment = got
        if got.outcome == hands.SHORT:
            self._note_short(ship, inst, got)

    def _after_all_hands(self, ship: Ship, inst: Instance) -> None:
        """When the last all-hands evolution ends, pipe down, unless the captain called
        all hands himself (spec M3 §3.2, §4.2). One still waiting its turn (the next
        topsail of "reef the topsails") counts: the hands are not piped down to be turned
        up again on the same tick, which cost the watch below its broken sleep once for
        every topsail (playtest 7, finding 1; docs/dev/TuningNotes.md, package 29b)."""
        crew = self._crew(ship)
        if crew is None or not inst.all_hands or self._all_hands_at_work(but=inst):
            return
        if any(i.waiting and i is not inst and self._want(i).all_hands for i in self.instances):
            return
        if crew.all_hands_called_by_order:
            return
        routine = ship.extra.get("routine")
        pipe_down = getattr(routine, "pipe_down", None)
        if pipe_down is not None:
            _record(ship, pipe_down())

    # -- log text ----------------------------------------------------------------------

    def _note(
        self, ship: Ship, inst: Instance, outcome: registry.Outcome, reason: str = ""
    ) -> None:
        reason = reason.rstrip(".")  # the templates end "{reason}." themselves
        template = outcome.log
        state = getattr(getattr(inst.subject, "state", None), "value", None)
        if state in outcome.from_state:  # a sail set from the gear (package 29b)
            template = outcome.from_state[state]
        text = self._format(inst, template, reason=reason)
        data: dict[str, Any] = {"evolution": inst.evo.id, "subject": inst.subject_id}
        if reason:
            data["reason"] = reason
        if inst.script is not None:
            data.update(inst.script.data())
        ship.note(outcome.severity, outcome.kind, text, inst.subject_id, data)

    def _format_context(self, inst: Instance) -> dict[str, Any]:
        ship = self.ship
        subject = inst.subject
        name = ship.name if isinstance(subject, Ship) else part_name(ship, inst.subject_id)
        ctx: dict[str, Any] = {
            "id": inst.evo.id,
            "verb": inst.evo.verb,
            "subject": name,
            "ship": ship.name,
            "sail": name,
            "yard": name,
            "spar": name,
            "line": name,
            "tack": ship.dyn.tack,
            "heading": units.format_heading(ship.dyn.heading),
            "speed": units.format_speed(ship.dyn.speed),
        }
        if isinstance(subject, Sail):
            ctx["state"] = subject.describe_state()
            ctx["reefs"] = subject.reefs
            ctx["reef_bands"] = subject.reef_bands
        if isinstance(subject, Spar):
            ctx["brace_deg"] = f"{abs(units.rad_to_deg(subject.brace_angle)):.0f}"
        for key, value in inst.params.items():
            ctx.setdefault(key, value)
        if inst.script is not None:
            ctx.update(inst.script.words())
        return ctx

    def _format(self, inst: Instance, template: str, reason: str = "") -> str:
        ctx = _SafeDict(self._format_context(inst))
        ctx["reason"] = reason
        return template.format_map(ctx)

    def _target(self, inst: Instance) -> str:
        """What the hands are sent to: 'the fore topsail', or 'tack ship'."""
        if isinstance(inst.subject, Ship):
            return self._describe(inst)
        return f"the {part_name(self.ship, inst.subject_id)}"

    def _doing(self, inst: Instance) -> str:
        """The work in hand: 'setting the fore topsail', 'tacking ship'."""
        first, _, rest = self._describe(inst).partition(" ")
        return f"{gerund(first)} {rest}".strip()

    def _other_work(self, inst: Instance) -> str:
        """The other work that has hands, for the log: 'setting the main topsail and the
        jib, and bracing the fore topsail yard'."""
        groups: dict[str, list[str]] = {}
        named = 0
        more = False
        for other in sorted(self.instances, key=lambda i: i.order):
            if other is inst or other.assignment is None or not other.assignment.hands:
                continue
            if named >= MAX_WORK_NAMED:
                more = True
                break
            doing = self._doing(other)
            verb, sep, what = doing.partition(" the ")
            key, item = (verb, "the " + what) if sep else (doing, "")
            groups.setdefault(key, [])
            if item:
                groups[key].append(item)
            named += 1
        phrases = [f"{verb} {_and(items)}".strip() for verb, items in groups.items()]
        if more:
            phrases.append("at other work")
        return _and(phrases, comma=True)

    def _describe(self, inst: Instance) -> str:
        subject = inst.subject
        name = (
            inst.subject_id if isinstance(subject, Ship) else part_name(self.ship, inst.subject_id)
        )
        verb = inst.evo.verb.replace("_", " ")
        if isinstance(subject, Ship):
            return f"{verb} ship" if verb in ("tack", "wear") else verb
        return f"{verb} the {name}"

    def _remaining_s(self, inst: Instance) -> float:
        if inst.script is not None:
            return round(inst.script.remaining_s(), 1)
        if inst.waiting:
            return round(inst.evo.nominal_duration_s * self._last_factor, 1)
        step = inst.step
        if step is None:
            return 0.0
        this = (1.0 - inst.progress) * step.duration_s
        rest = inst.evo.steps[inst.step_index + 1 :]
        # of two alternatives (`Step.instead_of`), the one the sail's state now takes
        env = self._env(self.ship, inst)
        taken: set[str] = set()
        for s in rest:
            if s.instead_of is not None and s.condition is not None:
                try:
                    if expr.evaluate(s.condition, env):
                        taken.add(s.instead_of)
                        continue
                except expr.ExpressionError:
                    pass
                taken.add(s.do)
        later = sum(s.duration_s for s in rest if s.do not in taken)
        crew = self._crew_factor(inst, step.aloft)
        return round((this + later) * self._last_factor * crew, 1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def gerund(verb: str) -> str:
    """'set' -> 'setting', 'take' -> 'taking', 'furl' -> 'furling', 'heave' -> 'heaving'."""
    v = verb.lower()
    vowels = "aeiou"
    if not v or v.endswith("ing"):
        return v
    if v.endswith("ie"):
        return v[:-2] + "ying"
    if v.endswith("e") and not v.endswith(("ee", "ye", "oe")):
        return v[:-1] + "ing"
    if (
        len(v) >= 3
        and v[-1] not in vowels + "wxy"
        and v[-2] in vowels
        and v[-3] not in vowels
        and sum(1 for c in v if c in vowels) == 1
    ):
        return v + v[-1] + "ing"
    return v + "ing"


def _record(ship: Ship, note: Any) -> None:
    """Log a note the watch routine returned to its caller ("All hands! (to tack ship)",
    "Piped down; ..."): the routine leaves the recording to whoever called it."""
    if isinstance(note, tuple) and len(note) == 5:
        ship.note(*note)


def _and(items: list[str], comma: bool = False) -> str:
    """'a', 'a and b', 'a, b and c' ('a, b, and c' with comma=True, for long phrases)."""
    if len(items) <= 1:
        return "".join(items)
    last = ", and " if comma and len(items) > 2 else " and "
    return ", ".join(items[:-1]) + last + items[-1]


def close_hauled_apparent_angle(ship: Ship) -> float:
    """The apparent wind angle at which this ship sails close-hauled: the luff
    angle package 4 exposes as ship.extra['luff_angle'] (default 45 degrees)
    plus the five-degree margin the helm keeps (package 5's FULL_AND_BY rule)."""
    luff = float(ship.extra.get("luff_angle", units.deg_to_rad(45.0)))
    return luff + units.deg_to_rad(5.0)


def _assign(obj: Any, attr: str, value: Any) -> None:
    """Set an attribute, converting the value to the type already there:
    text becomes the matching enum member, numbers stay numbers."""
    if attr.startswith("_") or not hasattr(obj, attr):
        raise expr.ExpressionError(f"{type(obj).__name__} has no attribute '{attr}' to set.")
    current = getattr(obj, attr)
    if isinstance(current, Enum) and not isinstance(value, Enum):
        try:
            value = type(current)(value)
        except ValueError:
            options = ", ".join(m.value for m in type(current))
            raise expr.ExpressionError(f"'{value}' is not one of: {options}.") from None
    elif isinstance(current, bool):
        value = bool(value)
    elif isinstance(current, int) and not isinstance(current, bool) and isinstance(value, float):
        value = int(round(value))
    setattr(obj, attr, value)
