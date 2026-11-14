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
called all hands himself. An all-hands *sail* evolution names its party
(``party: N`` in its crew line, package 31b): it takes at most that many, so
the three topsails of "reef the topsails" are manned together, each up to
its party in the order's order, the surplus to the next job and then to
whatever else waits for hands; the manoeuvres and the masts, with no party,
take everyone. At quarters every all-hands request is bounded so (package 75,
B7.c): its party is the hands the same work takes at sea in one watch, worked by
the trimmers and the marines' division, the helm, the powder, the carpenter's
crew and the surgeon's mates keeping their stations, and the guns are robbed
only for what it wants beyond them (`Runner._quarters_party`,
`Runner._quarters_pool`, `Runner._rob_the_guns`). Only a manoeuvre (its file
says ``belays: true``: tack, wear, box-haul, lie a-try) also belays the step-list
work in hand, which holds its progress and resumes, hands permitting, when the
all-hands work is done: the owner's ruling of 2026-09-29 at gate 4c (spec M3 §3.4).
Sending down the topgallant masts belays the work on those masts' sails
alone, which it clears away (`Script.clears`). Work so held, and work a post leaves under
half its hands (package 75, the lead's ruling 11), takes one road (`Runner._hold`) and is
taken up again where it stood (`Runner._try_resume`): the file's `requires` read again, a
script's own check, which is the beginning's, never (the lead's (C1) and (C6) of 2026-11-14).
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
from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.crew import bill, hands
from freesail.crew.model import Crew, Station, Watch, number_words
from freesail.evolutions import expr, registry
from freesail.evolutions import trim as yard_trim
from freesail.evolutions.scripts import (
    HELM_MANOEUVRES,
    SCRIPTS,
    Script,
    _world_of,
    keep_full_and_by,
    keep_lying_to,
    lying_to_hands_off,
)
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
# The mark package 109's own road (2026-11-13, gone by the lead's ruling 10 of that day) put
# on the boat's params while all hands came up to man her: a checkpoint taken on the trunk
# then carries it, and it is read on load as this road's mark of the same call
# (`Instance.__setstate__`, `Instance.held_up`).
_TRUNK_HANDS_CALLED_FOR = "hands_called_for"

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
    # the hands are up for it and are piped down by it: made all-hands work for itself, its watch
    # too few, as it asked for its hands or before a pipe-down that would have left the watch too
    # few for it (`Runner._made_all_hands`, the one road for both; package 75, the lead's (C5) of
    # 2026-11-14); or a numbered request whose file says `too_few: all hands until manned`, the
    # hands called to man it, until it is manned (`Runner._take_hands`; the lead's ruling 10)
    held_up: bool = False
    short_logged: bool = False
    # the precondition that failed says what was ordered is done already (package 37f)
    done_already: bool = False
    wait_line: str = ""  # the line it said when it first had to wait for hands
    given: int | None = None  # the order that started it (`Runner.giving`), for `belay that`

    def __setstate__(self, state: dict[str, Any]) -> None:
        """An instance read from a checkpoint. One taken on the trunk while all hands came up
        to man the boat by package 109's own road carries that road's mark in its params
        (`_TRUNK_HANDS_CALLED_FOR`): it is read as this road's mark of the same call, held up on
        its numbered request, so that she is manned and the hands piped down as they would have
        been (package 75, the lead's ruling 10 of 2026-11-13).

        A checkpoint holds the work's crew line as it was read when the order was given (`want`,
        and the file itself in `evo`). One written before the boat's file said `too_few: all
        hands until manned` (on the trunk, where package 109's road called for her by her
        evolution's name, or before it) has her waiting for hands with no such key, and on this
        road she would wait until hands came free. Where the file now says it of work
        whose request does not, the request is read with it, so that she calls for her hands as
        on the trunk (the review of the lead's ruling 10). Any other instance loads as it was."""
        state = dict(state)
        params = state.get("params")
        if isinstance(params, dict) and params.pop(_TRUNK_HANDS_CALLED_FOR, None):
            state["held_up"] = True
        want = state.get("want")
        if (
            isinstance(want, hands.CrewRequest)
            and not want.all_hands
            and not getattr(want, "calls_all_hands", False)
        ):
            now = registry.get(getattr(state.get("evo"), "id", ""))
            if now is not None and "too_few" in (now.crew or {}):
                try:
                    until_manned = hands.CrewRequest.from_mapping(now.crew).until_manned
                except hands.CrewRequestError:
                    until_manned = False
                if until_manned:
                    state["want"] = replace(want, calls_all_hands=True, until_manned=True)
        self.__dict__.update(state)

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


# The evolutions that are the gun crews' own work at quarters (package 70): the bill does
# not rob the guns for them.
QUARTERS_OWN = frozenset({"clear_for_action", "cast_loose_guns", "secure_guns"})

# The quarters whose hands keep their stations through an all-hands request at quarters
# (package 75, B7.c, as mended at its review: Bel-D §6.7, "worked first by the trimmers and,
# for the work on deck, the marines' division ... and takes from the guns ... only what its
# party wants beyond them"): the helm, the powder, the carpenter's crew and the surgeon's
# mates (`crew/quarters.py`'s divisions, by a hand's `quarters`).
KEEP_THEIR_STATIONS = frozenset({"helm", "powder", "carpenter", "surgeon"})


class Runner:
    """Runs evolutions for one ship. See the module docstring."""

    SHIP_SUBJECTS = ("ship", "her", "the ship")

    def __init__(self, ship: Ship):
        self.ship = ship
        self.instances: list[Instance] = []
        self._counter = 0
        self._last_factor = 1.0
        self._roll_deg = 0.0  # the ship's roll this tick (spec M5 §4), for the crew factor
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
            inst.script = script_cls(ship, merged, self._timing(ship, evo))
        inst.holds = self._holds(ship, inst)
        if self._crew(ship) is not None:
            try:
                inst.want = hands.CrewRequest.from_mapping(self._crew_line(ship, evo))
            except hands.CrewRequestError as e:
                raise OrderError(f"{evolution_id}: {e}") from None
            self._check_party(ship, inst)
        blockers = [
            other
            for other in self.instances
            if other.holds & inst.holds
            and other is not inst
            and not self._settees_only(ship, inst, other)
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
        motion = ship.extra.get("motion")
        self._roll_deg = float(motion.roll_deg) if motion is not None else 0.0
        crew = self._crew(ship)
        if crew is not None:
            calls = ship.extra.get("watch_calls")  # a watch turned up by an order (package 20)
            if calls:
                calls[:] = [c for c in calls if c.tick(self.clock or DEFAULT_WATCH_TIME)]
            # a merchantman's master or mate off work that counts them no longer (ruling 11)
            self._posts_off_the_work(ship, crew)
            self._top_up_all_hands(crew)
        for inst in list(self.instances):
            if inst.waiting or inst.paused:
                continue
            if inst.script is not None:
                self._tick_script(ship, inst, dt, wind)
            else:
                self._tick_steps(ship, inst, dt)
        self._start_waiting(ship)
        if "hove_to" in ship.extra or "lying_to.hands" in ship.extra:
            # lying to, the watch tends the helm and the sheets (package 37f)
            keep_lying_to(ship, dt, wind, self)
        # full and by, aback or in irons two minutes: the helm has her boxed off (37p)
        keep_full_and_by(ship, self, dt)
        # the true wind's mean as the deck has it, for `shorten sail`'s storm line; and a
        # storm staysail being bent, set when it is (package 37p, `orders.storm`)
        ship.extra["true_wind_kn"] = units.ms_to_knots(float(getattr(wind, "base_speed", 0.0)))
        if "storm_canvas_pending" in ship.extra:
            from freesail.orders.storm import keep_storm_canvas

            keep_storm_canvas(ship)
        if "course_pending" in ship.extra:
            # a course across the wind held for want of way, given when she has it (37m)
            from freesail.orders.navigation import keep_course_pending

            keep_course_pending(ship, dt)
        # the wind across the stern, a lug left against its mast or the yards by the lee:
        # said once a crossing, nothing ordered (package 58b, item 3)
        from freesail.orders.navigation import watch_the_stern

        watch_the_stern(ship)
        # at quarters a hand whose work is done goes back to his gun (package 70, spec M7
        # §8a; `crew/quarters.py`)
        quarters = ship.extra.get("quarters")
        if quarters is not None and getattr(quarters, "at_quarters", False):
            quarters.tick()

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
            if inst.script is not None and not inst.waiting:
                inst.script.belayed()  # package 37k: the capstan's pawl let go
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
        said = inst.script.left_words() if inst.script is not None else None
        if said:
            return said  # the script's own words: where the anchor is left (package 37k)
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

    @staticmethod
    def _timing(ship: Ship, evo: registry.Evolution) -> dict[str, float]:
        """A script's timing: its evolution file's, with the ship file's own figures for that
        evolution over it where her file gives them (`ShipSpec.timing`; package 75, the lead's
        ruling (1) of 2026-11-10 at 19:30: the 74's and the 64's lee helm lying a-try, `helm_deg`).
        Every other ship and evolution, the file's own."""
        spec = getattr(ship, "spec", None)
        own = (getattr(spec, "timing", None) or {}).get(evo.id)
        return {**evo.timing, **own} if own else evo.timing

    @staticmethod
    def _crew_line(ship: Ship, evo: registry.Evolution) -> dict[str, Any]:
        """The work's crew line: its file's, with the ship file's own number of hands for that
        evolution over the file's where her file gives one (`ShipSpec.hands`; package 75, the
        lead's (C2) of 2026-11-14: the bilander's heave-to and filling away, six of her, so that
        either watch's three begin them by night at her nine as the starboard's three did at her
        eight, where the ninth hand had lifted the company's clamp on the file's twelve from six
        to seven). Every other ship and evolution, the file's own; a spec pickled before it, the
        file's own."""
        spec = getattr(ship, "spec", None)
        own = (getattr(spec, "hands", None) or {}).get(evo.id)
        return {**evo.crew, "hands": own} if own else evo.crew

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
        # a post the lead's ruling 11 counts a hand of the watch named (`_working_posts`)
        posts = {s.id for s in self._working_posts(crew, inst, named=True)}
        party = [
            s
            for s in crew.sailors
            if pick in (self._watch_word(crew, s), s.station.value)
            and (hands.can_work(s, aloft=False) or s.id in posts)
        ]
        able = [s for s in party if hands.can_work(s, aloft) or s.id in posts]
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
        if wanted == "flying" and isinstance(subject, Sail) and subject.flying:
            return  # a sail set flying, of whatever cut (package 57)
        if wanted == "settee" and isinstance(subject, Sail) and subject.settee:
            return  # a settee, the bilander's main (package 75)
        if wanted == "spar" and isinstance(subject, Spar):
            return  # any spar: shifting one for a spare (package 30b)
        if wanted == "part" and isinstance(subject, Sail | Spar):
            return  # a spar or a sail: clearing a wreck (package 30b)
        if wanted == "line" and isinstance(subject, Line):
            return  # any line: reeving a parted one afresh (package 31b)
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

        def lee_side() -> str:
            # the lee side as the deck reads the wind (a dipping lug is hoisted on it,
            # package 43b): starboard with the wind on the larboard side
            return "larboard" if ship.dyn.apparent_wind_angle >= 0.0 else "starboard"

        def against_the_mast(sail: Any) -> bool:
            # a dipping lug lying on the weather side of its mast (package 43b)
            side = getattr(sail, "lug_side", None)
            return bool(getattr(sail, "dipping", False)) and side not in (None, lee_side())

        def wanted_sheet(sail: Any) -> float:
            # the sheet's angle the sail wants at the apparent wind, by its `curve_class`
            # (package 75; docs/design/Design-ShipsEngineExtensions.md §3.6, §5.2-§5.3): a
            # lateen cut at the mast is set to the gaff's 18-85 degrees, a settee to the lug's
            # 8-85
            cls = getattr(sail, "curve_class", None)
            if cls not in yard_trim.TRIM_RANGE:
                raise expr.ExpressionError(
                    f"'{getattr(sail, 'id', sail)}' is not a sail trimmed by its sheet."
                )
            return yard_trim.wanted_sheet_angle(cls, ship.dyn.apparent_wind_angle)

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
            "lee_side": lee_side,
            "against_the_mast": against_the_mast,
            "wanted_sheet": wanted_sheet,
        }
        return expr.Env(names, functions)

    def _failing_condition(
        self,
        ship: Ship,
        inst: Instance,
        conditions: list[registry.Condition],
        begun: bool = False,
    ) -> str | None:
        """The reason (in words) of the first condition that does not hold, else None.

        A script's own check (`Script.check`) is read with them as the work begins, and never
        once it has begun (`begun`: the next step of a step list, work held and taken up again,
        `_try_resume`). The check is the beginning's: it reads the world as the work finds it and
        lays its plan from it (the veer's target from the scope out, the kedge's boat and hawser),
        and the work's own going makes it false (the boat away with the kedge, the scope veered).
        Read again on a resume it refused work that was half done ("Could not lay out the kedge:
        the long-boat is away.") and laid a new plan over the old (a veer of twenty fathoms to
        fifty-eight where fifty-six were ordered): work paused and begun again as if new (the
        lead's (C1) of 2026-11-14). The file's `requires` hold through the work and are read
        whenever it goes on."""
        env = self._env(ship, inst)
        inst.done_already = False
        for cond in conditions:
            try:
                ok = expr.evaluate(cond.tree, env)
            except expr.ExpressionError as e:
                return f"{inst.evo.id}: the check '{cond.text}' could not be read ({e})"
            if not ok:
                inst.done_already = cond.done
                return self._format(inst, cond.reason)
        if inst.script is not None and not begun:
            return inst.script.check(self._format_context(inst))
        return None

    # -- holds: which parts an evolution occupies ------------------------------

    def _holds(self, ship: Ship, inst: Instance) -> set[str]:
        held = {inst.subject_id}
        if inst.script is not None:
            held |= inst.script.holds()
            if not getattr(inst.script, "holds_subject", True):
                # package 35: the boat away holds the boat and not the ship, so that the
                # cable is veered and the yards trimmed while she is ashore
                held.discard(inst.subject_id)
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

    def _settees_only(self, ship: Ship, manoeuvre: Instance, work: Instance) -> bool:
        """Whether a manoeuvre that belays the step-list work in hand (``belays: true``, with a
        crew: decision 25, `_call_all_hands`) shares with this step-list work nothing but the
        settees it holds from the order (`Script.order_settees`). Then the work, given before it,
        does not keep it waiting: the manoeuvre begins and belays the work in hand, and work
        still waiting (for hands, or its turn) waits for the manoeuvre (`_start_waiting`), so that
        no order of the settee's is begun while it may be changed (package 75, the lead's ruling
        (3)(iii) of 2026-11-10). Held otherwise, a wear ordered in the bilander's larboard watch
        by night behind "take in the mainsail", itself waiting for hands, waited with it and was
        never begun; in her starboard watch it waited for the take in, where it had belayed it
        (docs/dev/TuningNotes.md, "The review's mends of the two builds")."""
        script = manoeuvre.script
        if script is None or not script.order_settees or work.script is not None:
            return False
        if not manoeuvre.evo.belays or self._crew(ship) is None:
            return False
        return (manoeuvre.holds & work.holds) <= script.order_settees

    # -- beginning ---------------------------------------------------------------

    def _begin(self, ship: Ship, inst: Instance) -> bool:
        """Begin an instance whose parts are free. With a crew, it must get its hands
        first; without enough it waits for them and this returns False."""
        crew = self._crew(ship)
        if crew is not None and inst.evo.id in HELM_MANOEUVRES:
            # a manoeuvre takes the helm and the sheets from the watch that tended her
            # lying to, and its hands with them (package 37f)
            lying_to_hands_off(ship)
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

    def _to_the_conn(self, ship: Ship, crew: Crew, manoeuvre: Instance) -> int:
        """A manoeuvre begun takes a post who works with the watch from the work they hold to
        the conn (package 75, the lead's ruling 11 of 2026-11-13, as ruling 9's probe had it: never
        taken from the conn while the ship is under a manoeuvre they give): the work goes on short,
        or, under half its hands, is held as belayed work is until hands come (`_try_resume`),
        said as the manoeuvre's belay says it ("Belayed battening down: stations for wearing
        ship."). Called by `_take_hands` once the manoeuvre has its hands and before its line, so
        that the hands the held work lets go are the manoeuvre's in the count its line gives (the
        review of ruling 11). Returns how many hands the held work let go."""
        if not getattr(crew, "post_watches", None):
            return 0
        reason = self._format(manoeuvre, manoeuvre.evo.on_start.log).strip().rstrip(".!")
        reason = reason[:1].lower() + reason[1:]
        let_go = 0
        for s in self._posts_at_work(crew):
            work = next((i for i in self.instances if i.inst_id == s.at), None)
            if work is not None and getattr(work.script, "crew_away", False):
                let_go += self._post_off(ship, crew, s, work, None, manoeuvre.evo.id)
                continue
            gone = f"the {s.post} to the conn for {self._doing(manoeuvre)}"
            let_go += self._post_off(ship, crew, s, work, reason, manoeuvre.evo.id, gone)
        return let_go

    @staticmethod
    def _posts_at_work(crew: Crew) -> list:
        """The posts who work with their watch (`hands.post_watch`) and hold work now."""
        return [
            s
            for s in crew.by_station.get(Station.QUARTERDECK, ())
            if s.at is not None and hands.post_watch(crew, s) is not None
        ]

    def _post_off(
        self,
        ship: Ship,
        crew: Crew,
        post: Any,
        work: Instance | None,
        reason: str | None,
        cause: str,
        gone: str | None = None,
    ) -> int:
        """Take a post who works with the watch off the work they hold (the lead's ruling 11 of
        2026-11-13, and the review's mends of it): the work goes on short, or, under half its
        hands, is held as belayed work is until hands come (`_hold`, the pause's one road, taken
        up again where it stood by `_try_resume`), said by the belayed line with `reason`. With
        `reason` None (the boat or the kedge away from her side, `Script.crew_away`) the post
        stays aboard and the work goes on with the rest whatever their share, never held away from
        the ship. Where the work goes on short the post's leaving is said in the short line's
        words with `gone` ("Only four hands to the foresail; the master gone below.": the
        lead's (C3) of 2026-11-14), `reason` where `gone` is not given, "the master stays aboard"
        for the boat. Returns how many hands the held work let go."""
        post.at = None
        a = work.assignment if work is not None else None
        if work is None or a is None:
            return 0
        a.hands[:] = [h for h in a.hands if h is not post]
        if reason is not None and a.got < a.wanted * hands.SHORT_HANDED_SHARE:
            return self._hold(ship, crew, work, reason, {"for": cause, "post": post.post})
        if a.outcome == hands.ENOUGH and a.got < a.wanted:
            a.outcome = hands.SHORT
        said = gone or reason or f"the {post.post} stays aboard"
        n = a.got
        text = (
            f"Only {number_words(n)} hand{'s' if n != 1 else ''} to {self._target(work)}; {said}."
        )
        data = {**self._hands_data(work, a), "for": cause, "post": post.post}
        ship.note("routine", "evolution.short_handed", text, work.subject_id, data)
        return 0

    def _hold(
        self, ship: Ship, crew: Crew, work: Instance, reason: str, data: dict[str, Any]
    ) -> int:
        """The pause's one road (the lead's (C6) of 2026-11-14): work in hand held, its progress
        kept and its hands let go, said ("Belayed setting the fore topsail: stations for tacking
        ship.", "Belayed setting the foresail: the master gone below."), and taken up again
        where it stood when hands come (`_try_resume`). Taken by a manoeuvre's belay of the
        step-list work in hand (decision 25, the owner's ruling of 2026-09-29 at gate 4c;
        `_call_all_hands`) and by a post's leaving work, step-list or scripted, under half its
        hands (the lead's ruling 11 of 2026-11-13; `_post_off`). Returns how many hands it let
        go."""
        work.paused = True
        let_go = hands.release(crew, work.inst_id)
        work.assignment = None
        ship.note(
            "notable",
            "evolution.belayed",
            f"Belayed {self._doing(work)}: {reason}.",
            work.subject_id,
            {"evolution": work.evo.id, "subject": work.subject_id, **data},
        )
        return len(let_go)

    def _posts_off_the_work(self, ship: Ship, crew: Crew) -> None:
        """Each tick, before the work is ticked: a post's hand never outlasts what counted it
        (the lead's ruling 11 of 2026-11-13; the review's mends of it). A post who works with the
        watch and holds work is taken off it (`_post_off`) where `_working_posts` would count them
        no longer: at quarters, or all hands called or coming (the post to the conn: the ruling
        counts them neither at quarters nor for all-hands work), or their person no longer aboard,
        well, free and on deck (`People.works_on_deck`: gone below, sent for, at a sight or at
        their writing). The work goes on short, or is held, said, until hands come. A post whose
        work has taken its crew out of the ship (the boat or the kedge pulling away,
        `Script.crew_away`) stays aboard, the ruling counting them for work on deck alone, and the
        boat goes on with the rest."""
        posts = self._posts_at_work(crew) if getattr(crew, "post_watches", None) else []
        if not posts:
            return
        routine = ship.extra.get("routine")
        called = crew.all_hands_called or getattr(routine, "calling", False)
        people = getattr(_world_of(ship), "people", None)
        off_deck = getattr(people, "off_the_deck", None)
        for s in posts:
            work = next((i for i in self.instances if i.inst_id == s.at), None)
            who = f"the {s.post}"
            if work is not None and getattr(work.script, "crew_away", False):
                self._post_off(ship, crew, s, work, None, "boat")
            elif _at_quarters(ship):
                self._post_off(ship, crew, s, work, f"{who} to the conn at quarters", "quarters")
            elif called:
                self._post_off(
                    ship, crew, s, work, f"{who} to the conn, all hands called", "all_hands"
                )
            elif off_deck is not None and (why := off_deck(s)) is not None:
                self._post_off(ship, crew, s, work, f"{who} {why}", "post")

    def _start_waiting(self, ship: Ship) -> None:
        # Start waiting evolutions in the order they were given, when free.
        crew = self._crew(ship)
        for inst in sorted(self.instances, key=lambda i: i.order):
            if inst.paused and crew is not None:
                self._try_resume(ship, inst, crew)
                continue
            if not inst.waiting:
                continue
            # given first and holding a part of its, or a manoeuvre at work that it gave way to
            # on its settees alone (`_settees_only`): the work waits for the manoeuvre
            busy = any(
                other is not inst
                and other.holds & inst.holds
                and (
                    (other.order < inst.order and not self._settees_only(ship, inst, other))
                    or (
                        other.order > inst.order
                        and not other.waiting
                        and self._settees_only(ship, other, inst)
                    )
                )
                for other in self.instances
            )
            if busy:
                continue
            reason = self._failing_condition(ship, inst, inst.evo.preconditions + inst.evo.requires)
            if reason is not None:
                if inst.done_already:
                    self._done_already(ship, inst, reason)
                elif inst.evo.on_refused is not None:
                    self._refused(ship, inst, reason)
                else:
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
            reason = self._failing_condition(ship, inst, inst.evo.requires, begun=True)
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
                value = expr.evaluate(value_tree, env)
                if isinstance(obj, Sail) and attr == "sheet_angle":
                    # the sheet holds the trim (package 32e): a file that sets a sail's
                    # angle works its sheet to the length that angle needs
                    yard_trim.set_sheet_angle(ship, obj, float(value))
                    continue
                _assign(obj, attr, value)
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
        elif key and isinstance(inst.subject, Sail):
            # a trim's sheets (package 32e): one line for all of them, as for its braces
            deg = abs(units.rad_to_deg(inst.subject.sheet_angle))
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

    def _refused(self, ship: Ship, inst: Instance, reason: str) -> None:
        """Work that waited its turn and could not begin when it came (a precondition
        fails): said in the evolution's own words for it, `on_refused`, and not in its
        `on_fail`'s, which are for work that began and failed (package 37k; the review's
        G7: a tack that waited behind the leadsman and found her off the wind was logged
        "Squared the yards; she fell off on the starboard tack", a missed stay's words,
        and her officer gave up tacking in the Sound for two missed stays that never
        were)."""
        assert inst.evo.on_refused is not None
        self._remove(ship, inst)
        said = reason.strip()
        if len(said) > 1 and said[0].isupper() and said[1].islower():
            said = said[0].lower() + said[1:]  # it follows a colon
        self._note(ship, inst, inst.evo.on_refused, reason=said)
        key = inst.params.get("log_group")
        if key:
            self._group_done(ship, inst, key)
        self._after_all_hands(ship, inst)

    def _done_already(self, ship: Ship, inst: Instance, reason: str) -> None:
        """Work that waited its turn and found, when it came, that what was ordered is
        done already: a routine line in the precondition's own words ("The jib is set
        already."), and no failed evolution (package 37f; the review of gate 5c's
        playtests, 8.2: "Could not set the jib: The jib is set already" and its like
        were notable twenty-five times in game 9, each a failure in the log's count)."""
        self._remove(ship, inst)
        text = reason.strip()
        if text and text[-1] not in ".!?":
            text += "."
        data = {
            "evolution": inst.evo.id,
            "subject": inst.subject_id,
            "reason": reason.rstrip("."),
            "done_already": True,
        }
        ship.note("routine", "evolution.done_already", text, inst.subject_id, data)
        key = inst.params.get("log_group")
        if key:
            self._group_done(ship, inst, key)
        self._after_all_hands(ship, inst)

    def _group_done(self, ship: Ship, inst: Instance, key: str) -> None:
        """The last of a trim's braces is done: one line for all of them, "Braced twelve
        yards to the wind; 26° to 31° from square.", in the evolution's own kind and
        severity, its data naming every yard and its angle (package 29b).

        A trim's sheets name only the group's sails still set when its last sheet is done, and
        with none still set no line is said (package 75, the lead's ruling (3)(iv) of
        2026-11-10): the group's line is said when its last queued sheet is done, and it named
        every sail of the group, one taken in since among them ("Trimmed the sheets of the
        fore-and-aft foresail and the mainsail ..." after lie a-try had taken the fore gaff
        sail in, the *Neufchatel*'s gale; docs/dev/TuningNotes.md, B2c's "After the review")."""
        if any(i.params.get("log_group") == key for i in self.instances):
            return
        done = self._log_groups.pop(key, [])
        if isinstance(inst.subject, Sail):
            done = [(sid, d) for sid, d in done if sid in ship.sails and ship.sails[sid].is_set]
        if not done:
            return
        degs = [round(d) for _, d in done]
        lo, hi = min(degs), max(degs)
        outcome = inst.evo.on_complete
        if isinstance(inst.subject, Sail):
            # the sheets of a trim (package 32e): "Trimmed the sheets of the spanker, the
            # fore topmast staysail and the jib; 24° to 32° off the centreline."
            names = [f"the {part_name(ship, sid)}" for sid, _ in done]
            angle = f"{lo}°" if lo == hi else f"{lo}° to {hi}°"
            if len(done) == 1:
                text = (
                    f"Trimmed the {part_name(ship, done[0][0])} sheet; {angle} off the centreline."
                )
            else:
                text = f"Trimmed the sheets of {_and(names)}; {angle} off the centreline."
            data = {
                "evolution": inst.evo.id,
                "subjects": [sid for sid, _ in done],
                "sheet_deg": {sid: round(d, 1) for sid, d in done},
            }
            ship.note(outcome.severity, outcome.kind, text, None, data)
            return
        angle = f"{lo}° from square" if lo == hi else f"{lo}° to {hi}° from square"
        if len(done) == 1:
            text = f"Braced the {part_name(ship, done[0][0])}; {angle}."
        else:
            text = f"Braced {number_words(len(done))} yards to the wind; {angle}."
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
        # the lead's ruling 11: the post of the watch an order names, turned up with it, as
        # `_check_party` counts them (the review's mend: a party passed there began here too)
        posts = self._working_posts(crew, inst, named=pick in _WATCHES)
        if posts:
            deck = sorted(deck + posts, key=lambda s: s.id)
        if not pick:
            return deck
        return [s for s in deck if pick in (self._watch_word(crew, s), s.station.value)]

    @staticmethod
    def _watch_word(crew: Crew, sailor: Any) -> str:
        """The watch a sailor is of, as an order names it: their own, or for a post the watch
        they head (`hands.post_watch`; the lead's ruling 11 of 2026-11-13)."""
        heads = hands.post_watch(crew, sailor)
        return heads.value if heads is not None else sailor.watch.value

    def _working_posts(
        self, crew: Crew, inst: Instance, piped_down: bool = False, named: bool = False
    ) -> list:
        """The posts counted hands of their own watch for this request
        (`hands.post_watch`; package 75, the lead's ruling 11 of 2026-11-13, the narrower form of
        ruling 9's probe): a merchantman's master or mate, only where the watch's whole
        number (`_watch_whole`) is under the work's want, which is the request's own `wanted` for
        deck work: the file's number of hands, no more than the whole company could ever put to it
        (`hands.company_can_give`, as `hands.request` clamps it). A watch too small for the job,
        not a watch that is busy: hands at other work count in the whole, so a watch busy
        elsewhere waits as before.

        Everything else as ruling 9's probe had it: a numbered request wanting no hand aloft, not
        at quarters, never for a manoeuvre nor while one is in hand (the officer of the deck gives
        it), nor while all hands are called or coming; each while their watch has the deck (for a
        party an order names, `named`, whichever watch) and their person is aboard, well, free and
        on deck (`People.works_on_deck`). A post so counted holds the work no longer than that
        holds (`_posts_off_the_work`, `_to_the_conn`), and hauls at the boat's falls but does not
        go away in her (`Script.crew_away`)."""
        heads = {
            s.id: w
            for s in crew.by_station.get(Station.QUARTERDECK, ())
            if s.fit and (w := hands.post_watch(crew, s)) is not None
        }
        if not heads:
            return []
        want = self._want(inst)
        if want.all_hands or not want.hands or self._aloft(inst) or _at_quarters(self.ship):
            return []
        if inst.evo.id in HELM_MANOEUVRES or any(
            i.evo.id in HELM_MANOEUVRES and not i.waiting for i in self.instances
        ):
            return []
        routine = self.ship.extra.get("routine")
        if not piped_down and (crew.all_hands_called or getattr(routine, "calling", False)):
            return []
        wanted = min(int(want.hands), hands.company_can_give(crew, aloft=False))
        when = self.clock if self.clock is not None else DEFAULT_WATCH_TIME
        watch = bill.watch_on_deck(crew, when)
        # where the post's person is: the world's people, through the standing runtime the World
        # attaches to her (`scripts._world_of`); none for a ship alone
        free = getattr(getattr(_world_of(self.ship), "people", None), "works_on_deck", None)
        return [
            s
            for s in crew.by_station.get(Station.QUARTERDECK, ())
            if s.id in heads
            and (named or heads[s.id] is watch)
            and self._watch_whole(crew, heads[s.id]) < wanted
            and (free is None or free(s))
        ]

    def _watch_whole(self, crew: Crew, watch: Watch) -> int:
        """A watch's whole number (the lead's ruling 11 of 2026-11-13): every hand of it on board
        and fit, whatever they are doing, idle, at other work or below, counted as `hands.can_work`
        counts a hand for work on deck (fit, not of the quarterdeck: hurt at light duty counts,
        the sick, the wounded and the dead do not). A hand away in the boat (held by work whose
        crew is out of the ship, `Script.crew_away`) is not on board; one hoisting her out or in
        is. The posts are not counted: the whole is the hands', and the post makes it up."""
        away = {i.inst_id for i in self.instances if getattr(i.script, "crew_away", False)}
        return sum(
            1
            for s in crew.sailors
            if s.watch is watch
            and hands.can_work(s, aloft=False)
            and (s.at is None or s.at not in away)
        )

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
            inst.want = hands.CrewRequest.from_mapping(self._crew_line(self.ship, inst.evo))
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
        # the ship's roll (spec M5 §4, `physics.motion`): the work aloft slows with it,
        # with a crew or without; nothing without a sea
        roll = self._roll_deg
        if inst.assignment is None or inst.want is None:
            return hands.seaway_factor(roll, aloft)
        return hands.crew_factor(inst.assignment, inst.want, aloft, roll)

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
        want = self._quarters_party(ship, inst, crew, want)
        got = hands.request(
            crew,
            self._quarters_pool(ship, inst, want, self._pool(crew, inst)),
            inst.inst_id,
            want,
            self._subject_mast(ship, inst),
            aloft=self._aloft(inst),
            posts=True,
        )
        got = self._rob_the_guns(ship, inst, crew, want, got)
        if (
            got.outcome == hands.TOO_FEW
            and not inst.held_up
            and self._watch_too_few(ship, inst, crew, want)
        ):
            # a watch too few for the work calls all hands for it, where its file says so
            # (package 75, the lead's ruling (1) of 2026-11-10: a small company's work at her
            # great sail, the settee's files): it is all-hands work from here, its party its
            # own number, and pipes down when it ends (`_after_all_hands`)
            if want.until_manned:
                # or, where the file says `all hands until manned` (the boat's: the lead's
                # ruling 10 of 2026-11-13, one road with package 109's), it keeps its number and
                # waits, said by the call, held up while the hands come up, and pipes down once
                # it is manned (below)
                inst.held_up = True
                self._call_all_hands(ship, inst, crew)
                inst.waiting = True
                inst.waiting_for = WAITING_FOR_HANDS
                return False
            want = self._made_all_hands(inst)
            self._call_all_hands(ship, inst, crew)
            got = hands.request(
                crew,
                self._pool(crew, inst),
                inst.inst_id,
                want,
                self._subject_mast(ship, inst),
                aloft=self._aloft(inst),
                posts=True,
            )
        if got.outcome == hands.TOO_FEW and self._manning(ship, inst):
            # called to man it: it waits for the hands still coming up, said by the call
            inst.waiting = True
            inst.waiting_for = WAITING_FOR_HANDS
            return False
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
        if inst.evo.id in HELM_MANOEUVRES and self._to_the_conn(ship, crew, inst):
            # the hands of the work held by the post's going to the conn are the manoeuvre's
            # too, before its line counts them (the review of the lead's ruling 11)
            if got.all_hands:
                hands.top_up(
                    got,
                    self._quarters_pool(ship, inst, want, self._pool(crew, inst)),
                    aloft=self._aloft(inst),
                    want=want,
                    subject_mast=self._subject_mast(ship, inst),
                )
            elif not _at_quarters(ship):
                hands.release(crew, inst.inst_id)
                got = hands.request(
                    crew,
                    self._pool(crew, inst),
                    inst.inst_id,
                    want,
                    self._subject_mast(ship, inst),
                    aloft=self._aloft(inst),
                    posts=True,
                )
        inst.assignment = got
        inst.all_hands = want.all_hands
        if got.outcome == hands.SHORT:
            self._note_short(ship, inst, got)
        if inst.held_up and not inst.all_hands:
            # manned: the hands called to man it are piped down, unless the captain's own order
            # called them or other work keeps them up (`_after_all_hands`), and it pipes down
            # nothing more when it ends (`too_few: all hands until manned`; the lead's ruling 10)
            self._after_all_hands(ship, inst)
            inst.held_up = False
        return True

    def _made_all_hands(self, inst: Instance) -> hands.CrewRequest:
        """Work made all-hands work for itself because the watch is too few for it (package 75,
        the lead's ruling (1) of 2026-11-10; `hands.CrewRequest.calls_all_hands`), the one road
        for both places that make it so: as it asks for its hands (`_take_hands`) and as a
        pipe-down would leave it too few (`_after_all_hands`). Its request is all hands (the
        boat's, `until manned`, keeps its number), and the hands are up for it and piped down by
        it (`Instance.held_up`), so that taken away before it began (belayed, refused, done
        already, failed) it ends the call as its end would. Made so as it asked for its hands it
        was not marked, and work made all-hands there that then waited and was belayed or refused
        left the hands up for nothing (the lead's (C5) of 2026-11-14). Returns its request."""
        want = self._want(inst)
        if not want.until_manned:
            want = inst.want = want.as_all_hands()
        inst.held_up = True
        return want

    def _manning(self, ship: Ship, inst: Instance) -> bool:
        """Whether this work waits, said by the call, while the hands called to man it come up:
        held up on its numbered request (`too_few: all hands until manned`, `Instance.held_up`)
        while the routine's call is under way (package 75, the lead's ruling 10 of
        2026-11-13). Once all are up, or piped down by order before it was manned, it waits for
        hands with the waiting line, as before, and does not call them again itself."""
        if not inst.held_up or self._want(inst).all_hands:
            return False
        return bool(getattr(ship.extra.get("routine"), "calling", False))

    def _watch_too_few(
        self, ship: Ship, inst: Instance, crew: Crew, want: hands.CrewRequest
    ) -> bool:
        """Whether this work calls all hands because the watch on deck is too few to begin it
        (package 75, the lead's ruling (1) of 2026-11-10; `hands.CrewRequest.calls_all_hands`):
        all hands are not up already and the deck as it is now is too few for it by
        `_calls_for_itself`, the one judge."""
        if crew.all_hands_called:
            return False
        return self._calls_for_itself(ship, inst, crew, want, self._pool(crew, inst))

    def _too_few_piped_down(self, ship: Ship, inst: Instance, crew: Crew) -> bool:
        """Whether work waiting its turn would call all hands for itself the moment the hands
        were piped down: `_calls_for_itself`, the one judge, read on the deck as the pipe-down
        would leave it (`bill.on_deck_piped_down`, all hands not called and nobody turned up),
        with the post of the watch then on deck where it would be counted (`_working_posts`;
        the lead's ruling 11 of 2026-11-13). Read by `_after_all_hands` before it pipes down
        (package 75, the review of the lead's ruling (1) of 2026-11-10)."""
        when = self.clock if self.clock is not None else DEFAULT_WATCH_TIME
        deck = bill.on_deck_piped_down(crew, when) + self._working_posts(crew, inst, True)
        return self._calls_for_itself(ship, inst, crew, self._want(inst), deck)

    def _calls_for_itself(
        self, ship: Ship, inst: Instance, crew: Crew, want: hands.CrewRequest, deck: list
    ) -> bool:
        """The one judge of whether this work, on `deck`, is too few to begin and calls all hands
        for itself (the lead's (C5) of 2026-11-14): asked as it asks for its hands
        (`_watch_too_few`, the deck as it is) and before a pipe-down (`_too_few_piped_down`, the
        deck as the pipe-down would leave it), so that the hands are never piped down to be
        called again for it on the same tick. Its file says so, the ship is not at quarters and
        the order named no party of its own (`hands_from`, which `_check_party` judges).

        Work manned and piped down at once (`until manned`, the boat's crew) by package 109's own
        trigger, so that the one road keeps the boat's lines (the lead's ruling 10 of
        2026-11-13): its request would come back too few on that deck (the hands idle there under
        half its number) and no work of the runner's has the hands, so that a watch busy at
        other work waits, said, and a hand at the pumps does not make the deck enough. Judged
        before the pipe-down by the deck's count, which holds the hands at the pumps, the boat
        waiting behind all-hands work at anchor with her watch at the pumps saw the hands piped
        down and called all hands again on that tick. Any other such work by the deck's count,
        hands at other work counted (`hands.too_few_on_deck`), so that a watch busy elsewhere
        waits as before."""
        if not want.calls_all_hands or _at_quarters(ship) or inst.params.get("hands_from"):
            return False
        aloft = self._aloft(inst)
        if want.until_manned:
            wanted = min(int(want.hands), hands.company_can_give(crew, aloft))
            idle = sum(1 for s in deck if s.at is None and hands.can_work(s, aloft, posts=True))
            return idle < wanted * hands.SHORT_HANDED_SHARE and not self._other_work(inst)
        return hands.too_few_on_deck(crew, deck, want, aloft, posts=True)

    def _rob_the_guns(
        self, ship: Ship, inst: Instance, crew: Crew, want: hands.CrewRequest, got: hands.Assignment
    ) -> hands.Assignment:
        """At quarters, sail work short of hands takes them from the guns by the fighting
        book's priority (package 70, spec M7 §8a; `crew/quarters.py`, `lend`): the crews
        from the end that bears least, whole crews first, for what the work wants beyond
        the hands idle at their quarters. An all-hands request is bounded there by its
        party (`_quarters_party`) and drawn from its pool (`_quarters_pool`), so a manoeuvre
        is worked by the trimmers and the marines' division and takes from the guns only
        the rest of one watch, made up from the hands freed (`hands.top_up`; package 75,
        B7.c: `docs/design/Design-Ship-Bellerophon.md` §6.7; before it, half of every crew
        whatever stood idle). A numbered request's hands freed are taken by a second
        request. The line says how many and from where. Under `guns before sail` nothing
        is lent and the work waits or goes short, as the design has it."""
        quarters = ship.extra.get("quarters")
        if quarters is None or not getattr(quarters, "at_quarters", False):
            return got
        if inst.evo.id in QUARTERS_OWN:
            return got  # the guns' own work (cast loose, secured): the crews do it
        if got.outcome == hands.ENOUGH:
            return got
        aloft = self._aloft(inst)
        battery = ship.extra.get("battery")
        bearing_fwd = None
        relative = getattr(battery, "target_relative_rad", None) if battery is not None else None
        if relative is not None:
            bearing_fwd = abs(relative) < 1.5707963
        need = max(0, got.wanted - (got.got if got.outcome != hands.TOO_FEW else 0))
        freed, where = quarters.lend(need, aloft, bearing_fwd)
        if not freed:
            return got
        if want.all_hands:
            # an all-hands request keeps the trimmers and the marines it has and is made up
            # to its party from the hands freed, the best fitted first, the rest back to
            # their guns at once (`Quarters.tick`): the guns give only what its party wants
            # beyond them, and the line says that many (B7.c, mended at its review)
            hands.top_up(
                got,
                self._quarters_pool(ship, inst, want, self._pool(crew, inst)),
                aloft=aloft,
                want=want,
                subject_mast=self._subject_mast(ship, inst),
            )
            again = got
            n = sum(1 for s in freed if s.at == inst.inst_id)
        else:
            if got.outcome != hands.TOO_FEW:
                hands.release(crew, inst.inst_id)
            again = hands.request(
                crew,
                self._pool(crew, inst),
                inst.inst_id,
                want,
                self._subject_mast(ship, inst),
                aloft=aloft,
                posts=True,
            )
            n = len(freed)
        if again.outcome != hands.TOO_FEW and where and n:
            ship.note(
                "notable",
                "quarters.robbed",
                f"{self._doing(inst).capitalize()} at quarters: {number_words(n)} "
                f"hand{'s' if n != 1 else ''} taken {where}; the guns go on short-handed.",
                inst.subject_id,
                {"evolution": inst.evo.id, "hands": n, "from": where},
            )
        return again

    def _quarters_party(
        self, ship: Ship, inst: Instance, crew: Crew, want: hands.CrewRequest
    ) -> hands.CrewRequest:
        """An all-hands request at quarters, bounded by a party (package 75, B7.c; Bel-D
        §6.7): the hands the same work takes at sea in one watch (`_one_watch`, the engine's
        own measure of enough), or the file's own party where that is less. So the trimmers
        and the marines' division work it first (`_quarters_pool`) and the guns give only the
        rest (`_rob_the_guns`), under either priority. Any other request, or one not at
        quarters, as it was; the instance's own request is not changed."""
        if not want.all_hands or not _at_quarters(ship) or inst.evo.id in QUARTERS_OWN:
            return want
        party = self._one_watch(crew, self._aloft(inst))
        if want.party is not None:
            party = min(party, want.party)
        return replace(want, party=max(1, party))

    def _quarters_pool(
        self, ship: Ship, inst: Instance, want: hands.CrewRequest, pool: list
    ) -> list:
        """The hands an all-hands request at quarters may draw on (package 75, B7.c, as
        mended at its review; Bel-D §6.7): the trimmers, the marines' division (on deck
        alone: `hands.can_work` keeps a marine off the yards), the hands the guns lend
        (`_rob_the_guns`) and any not quartered; the helm, the powder, the carpenter's crew
        and the surgeon's mates keep their stations (`KEEP_THEIR_STATIONS`). Any other
        request, or one not at quarters, draws on the pool as it is."""
        if not want.all_hands or not _at_quarters(ship) or inst.evo.id in QUARTERS_OWN:
            return pool
        return [s for s in pool if s.quarters not in KEEP_THEIR_STATIONS]

    def _one_watch(self, crew: Crew, aloft: bool) -> int:
        """The hands on deck in one watch, as the watch bill has them with no call
        (`crew/bill.py`): the watch on deck and, by day, the idlers, each fit for the work
        (`hands.can_work`)."""
        when = bill.when_of(self.clock if self.clock is not None else DEFAULT_WATCH_TIME)
        watch = bill.watch_on_deck(crew, when)
        up = bill.idlers_up(when)
        return sum(
            1
            for s in crew.sailors
            if (s.watch is watch or (up and s.station is Station.IDLERS))
            and hands.can_work(s, aloft)
        )

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
        """Hands who have come on deck since an all-hands evolution began join it, the
        earlier work first and each job only up to its party (package 31b), so that the
        surplus goes to the next job of the order and then to whatever else waits."""
        running = self._all_hands_at_work()
        if not running:
            return
        deck = self._on_deck(crew)
        for inst in sorted(running, key=lambda i: i.order):
            if inst.assignment is not None:
                hands.top_up(
                    inst.assignment,
                    self._quarters_pool(self.ship, inst, self._want(inst), deck),
                    aloft=self._aloft(inst),
                    want=self._want(inst),
                    subject_mast=self._subject_mast(self.ship, inst),
                )

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
            self._hold(ship, crew, other, reason, {"for": inst.evo.id})

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
            posts=True,
        )
        if got.outcome == hands.TOO_FEW:
            return
        # The world moved while the work lay belayed: a hoist half done must not finish
        # on a yard that has since been sent down (package 19's finding). What the work's
        # beginning read (a script's own check: the kedge's boat in the ship, the veer's scope
        # and its target from it) is not read again: the work is taken up where it stood, not
        # begun again (the lead's (C1) of 2026-11-14; `_failing_condition`'s `begun`).
        reason = self._failing_condition(ship, inst, inst.evo.requires, begun=True)
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
        every topsail (playtest 7, finding 1; docs/dev/TuningNotes.md, package 29b).

        Work waiting its turn whose file calls all hands where the watch is too few (the
        bilander's settee, `hands.CrewRequest.calls_all_hands`) counts with it where the watch
        would be too few for it the moment the hands were piped down (`_too_few_piped_down`):
        it is made all-hands work here, before the pipe-down, and the hands stay up for it
        (`Instance.held_up`), so that it begins on them and is not piped down and called again
        on the same tick (package 75, the review of the lead's ruling (1) of 2026-11-10: a furl
        ordered behind a take in, a take in behind a wear, in her larboard watch by night). Such
        work taken away before it began (refused, done already, failed or belayed) ends the call
        as all-hands work ending would.

        Work whose file says `too_few: all hands until manned` (the boat's) pipes down here once
        it is manned (`_take_hands`), or taken away before it was; waiting its turn where the
        watch would be too few for it, it keeps its number and the hands stay up for it, held up
        until it is manned (package 75, the lead's ruling 10 of 2026-11-13)."""
        crew = self._crew(ship)
        if crew is None or self._all_hands_at_work(but=inst):
            return
        if not (inst.all_hands or inst.held_up):
            return
        if crew.all_hands_called_by_order:
            return
        for i in self.instances:
            if i.waiting and i is not inst and self._too_few_piped_down(ship, i, crew):
                self._made_all_hands(i)
        if any(
            i.waiting and i is not inst and (i.held_up or self._want(i).all_hands)
            for i in self.instances
        ):
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
        severity = outcome.severity
        if outcome.kind == "yard.braced" and _at_quarters(ship):
            # the flow of the game through the log (the model officer's fourth point): at
            # quarters the trimmers' yard by yard is the routine of the action, and a
            # stand-by on 'a notable event' is not woken by each; a trim's one line for all
            # of them (`_group_done`) and the sails set or taken in stay notable
            severity = "routine"
        ship.note(severity, outcome.kind, text, inst.subject_id, data)

    def _format_context(self, inst: Instance) -> dict[str, Any]:
        ship = self.ship
        subject = inst.subject
        name = ship.name if isinstance(subject, Ship) else part_name(ship, inst.subject_id)
        ctx: dict[str, Any] = {
            "id": inst.evo.id,
            "verb": inst.evo.verb,
            "subject": name,
            "subject_id": inst.subject_id,  # package 73: the repair scripts find their part by it
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
            ctx["parted"] = self._parted_gear(ship, subject)
        if isinstance(subject, Spar):
            ctx["brace_deg"] = f"{abs(units.rad_to_deg(subject.brace_angle)):.0f}"
        if inst.evo.id == "get_under_way":
            # the first line by her rig (package 68): a lugger has a windlass and no
            # sail-loosers aloft
            from freesail.evolutions.scripts import under_way_start_words

            ctx["start_words"] = under_way_start_words(ship)
        for key, value in inst.params.items():
            ctx.setdefault(key, value)
        if inst.script is not None:
            ctx.update(inst.script.words())
        return ctx

    def _format(self, inst: Instance, template: str, reason: str = "") -> str:
        ctx = _SafeDict(self._format_context(inst))
        ctx["reason"] = reason
        return template.format_map(ctx)

    @staticmethod
    def _parted_gear(ship: Ship, sail: Sail) -> str:
        """The sail's gear that is parted, for a set evolution's refusal (package 31b):
        'the larboard fore topsail sheet is parted and must be rove afresh'. The sheets,
        the tacks and the halyard: the lines a set hauls on."""
        gear = [
            ln
            for ln in ship.lines_of(sail)
            if ln.state is LineState.PARTED and ln.cls in ("sheet", "tack", "halyard")
        ]
        halyard = ship.halyard_of(sail)
        if halyard is not None and halyard.state is LineState.PARTED and halyard not in gear:
            gear.append(halyard)
        if not gear:
            return "its gear is parted and must be rove afresh"
        names = [f"the {part_name(ship, ln.id)}" for ln in gear]
        verb = "is" if len(names) == 1 else "are"
        return f"{_and(names)} {verb} parted and must be rove afresh"

    def _target(self, inst: Instance) -> str:
        """What the hands are sent to: 'the fore topsail', or 'tack ship'."""
        if isinstance(inst.subject, Ship):
            return self._describe(inst)
        return f"the {part_name(self.ship, inst.subject_id)}"

    def _doing(self, inst: Instance) -> str:
        """The work in hand: 'setting the fore topsail', 'tacking ship', and for work on the ship
        whose file names it (`registry.Evolution.doing`) that name: 'laying out the kedge', where
        the verb's gerund was the id with an ending, 'laying out kedge' (the lead's (C8) of
        2026-11-14). Every reader of the work in hand's name reads it here: the belayed lines,
        the captain's belay and its listing, the work the rest are at, the readings."""
        doing = getattr(inst.evo, "doing", None)
        if doing and isinstance(inst.subject, Ship):
            return doing
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


def _at_quarters(ship: Ship) -> bool:
    """Whether the ship is at quarters (the drum beaten and the hands at the guns)."""
    quarters = (getattr(ship, "extra", None) or {}).get("quarters")
    return bool(quarters is not None and getattr(quarters, "at_quarters", False))


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
