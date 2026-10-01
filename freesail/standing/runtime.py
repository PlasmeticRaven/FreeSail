"""The standing orders' runtime (spec M4 §3 and §4): every rule evaluated once a tick.

`World.tick` calls `Runtime.tick` last, after the physics, the crew and the bells, so
that a rule reads the tick's settled numbers and `at eight bells` fires on the bell's
own tick. One `ReadingsView` serves the whole pass: every rule of a tick reads the same
readings.

The three guards against thrashing (spec §3):

- **Durations debounce.** `for 2 minutes` is an accumulator of ship's time: the `when`
  condition must have held for that long, counted from the last tick it was false.
- **A `when` order is edge-triggered with a dwell.** Having fired, it is disarmed until
  its condition has been false for `STANDING_DWELL_S` seconds together and every
  evolution its firing started has ended (asked of the runner), and then it must hold
  for its duration again. A wind's shift it waits for ('veers a point') is spent when it
  fires and measured afresh from the wind it fired on (package 29b). An `at` order
  fires once per event; an `every` order fires on its interval whether or not the last
  firing's work is done, but never queues a second behind one still waiting for its
  parts.
- **The conflict rule by rank.** When a rule would give an order on a part that another
  rule's firing within the dwell gave a contrary order on, the senior's stands and the
  log says so: "Standing order 'x' (the master) countermanded by 'y' (the captain)."
  The junior's order is not given; a senior firing after a junior's is given, and the
  junior's is logged as countermanded. Two of one rank give the later precedence with
  a plain note. The grain (spec M5 open item 15, package 33c): a sail, a yard or a line
  is its own part, the helm one, a manoeuvre the helm's and every yard's, the lead the
  leadsman's, the log the log's, a bearing and the account the master's (`the
  reckoning`), a course shaped the helm's, and the ship's only what is left (the masts
  sent down, all work belayed); and a firing whose evolutions have all ended is done
  with, so an order after it is the next step and not a contrary one (`at wore then
  heave to`).

A failing `, if` is said in the log the first time and then once a watch while it goes
on failing (spec M5 open item 15; package 33c); an order held for a reading the ship has
not got (`sound the well`) waits, silent, in the book.

A firing is an ordinary order with an unusual actor: `World.submit(text, actor="standing
order 'x'")`, which the World logs as "By standing order 'x': taking in the royals." and
does not journal, since firings are a deterministic function of the seed and the journal
(spec §4). Everything here iterates in the order the book keeps, so two runs give one log.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from freesail.api import readings as R
from freesail.core.clock import TICK_SECONDS
from freesail.core.events import Severity
from freesail.evolutions.runner import gerund
from freesail.orders import errors, resolve
from freesail.orders import grammar as imperative
from freesail.orders.errors import OrderError
from freesail.orders.vocabulary import load_vocabulary, normalise
from freesail.standing.book import Book
from freesail.standing.rules import STANDING_DWELL_S, Rule

if TYPE_CHECKING:
    from freesail.core.world import World

__all__ = ["ACTOR_PREFIX", "Runtime", "action_parts", "said_as_done"]

# The actor a firing carries; the World knows a firing by it (spec §4).
ACTOR_PREFIX = "standing order "

# Parts an order touches that are not parts of the ship's graph.
HELM = "the helm"
SHIP = "the ship"
CREW = "the watch"


@dataclass(frozen=True)
class ActionParts:
    """What one order lays hands on, for the conflict rule: its canonical verb, the parts
    it names (part ids, or the helm, the ship, the watch) and how it qualifies them."""

    text: str
    verb: str
    parts: frozenset[str]
    manner: frozenset[tuple[str, str]]

    def conflicts_with(self, other: ActionParts) -> frozenset[str]:
        """The parts on which the two give contrary orders: the same part with a different
        verb, or the same verb said otherwise (steer 90 against steer 180, one reef against
        two). The same order twice is a repetition, not a conflict."""
        shared = self.parts & other.parts
        if not shared:
            return frozenset()
        if self.verb == other.verb and self.manner == other.manner:
            return frozenset()
        return shared


@dataclass
class Firing:
    rule: Rule
    tick: int
    actions: list[ActionParts] = field(default_factory=list)
    # the evolutions the firing began (package 33c): once every one has ended its orders
    # are done with, and an order after them is the next step, not a contrary one
    started: list[Any] = field(default_factory=list)


def action_parts(ship: Any, text: str) -> ActionParts:
    """Read an order for the parts it touches. An order that cannot be read (a side the
    ship has not got now) touches nothing, and the conflict rule lets it by."""
    vocab = load_vocabulary()
    try:
        order = imperative.parse(ship, text, vocab)
    except OrderError:
        return ActionParts(text, "", frozenset(), frozenset())
    spec = vocab.verbs[order.verb]
    manner = frozenset((k, str(v)) for k, v in sorted(order.modifiers.items()) if k != "hands_from")
    if order.verb in vocab.group_evolutions:
        parts: set[str] = set()
        for line in vocab.group_evolutions[order.verb]:
            parts |= action_parts(ship, line).parts
        return ActionParts(text, order.verb, frozenset(parts), manner)
    if spec.object in ("heading", "points") or order.verb in imperative_helm_verbs():
        return ActionParts(text, order.verb, frozenset({HELM}), manner)
    if spec.object == "navigation":
        # the master's work (package 33c, spec M5 open item 15): the lead is the
        # leadsman's, the log the log's, a bearing and the account the master's, and a
        # course shaped the helm's; none of them is the ship's, so `heave the lead` and
        # `heave to` are not contrary orders
        return ActionParts(text, order.verb, frozenset({_navigation_part(order.verb)}), manner)
    if order.verb in MANOEUVRES:
        # a manoeuvre is the helm's and the yards' (package 33c)
        yards = frozenset(s.id for s in ship.spars.values() if s.is_yard)
        return ActionParts(text, order.verb, frozenset({HELM}) | yards, manner)
    if spec.object in ("sail", "yards", "line"):
        if order.object is None:
            yards = frozenset(s.id for s in ship.spars.values() if s.is_yard)
            return ActionParts(text, order.verb, yards, manner)
        try:
            res = resolve.resolve(ship, order.object, order.side_word, order.verb)
        except OrderError:
            return ActionParts(text, order.verb, frozenset(), manner)
        return ActionParts(text, order.verb, frozenset(res.ids), manner)
    if order.verb in ("call all hands", "pipe down", "relieve the watch"):
        return ActionParts(text, order.verb, frozenset({CREW}), manner)
    return ActionParts(text, order.verb, frozenset({SHIP}), manner)


# The ship's manoeuvres by their verbs (`data/vocabulary.yaml`): the helm's and the yards'.
MANOEUVRES: frozenset[str] = frozenset(
    {
        "tack ship",
        "wear ship",
        "heave to",
        "fill away",
        "box haul",
        "wear short round",
        "lie a try",
        "scud",
        "back and fill",
    }
)
# The navigation orders' parts, for the conflict rule (package 33c).
LEAD = "the lead"
LOG_LINE = "the log"
RECKONING = "the reckoning"


def _navigation_part(verb: str) -> str:
    if verb in ("heave the lead", "heave the deep sea lead"):
        return LEAD
    if verb == "heave the log":
        return LOG_LINE
    if verb == "shape a course for":
        return HELM
    return RECKONING


def imperative_helm_verbs() -> tuple[str, ...]:
    from freesail.orders.verbs import HELM_VERBS

    return tuple(HELM_VERBS) + ("keep her full",)


def said_as_done(ship: Any, text: str) -> str:
    """'take in the studdingsails' -> 'taking in the studdingsails', for the firing line."""
    words = normalise(text).replace(" , ", ", ").split()
    if not words:
        return text
    try:
        order = imperative.parse(ship, text)
        head = order.verb.split()[0]
        phrase_len = len(order.verb_phrase.split())
    except OrderError:
        head, phrase_len = words[0], 1
    for i in range(min(phrase_len, len(words))):
        if words[i] == head:
            words[i] = gerund(head)
            return " ".join(words)
    words[0] = gerund(words[0])
    return " ".join(words)


class Runtime:
    """The book and its evaluation for one World."""

    def __init__(self, world: World):
        self.world = world
        self.book = Book(self)
        self._seen_log = len(world.log)
        self._firings: list[Firing] = []
        # the rule whose orders are being given now, for a station sentence among them
        # (`tell`/`ask the watcher`, package 31c): the log names the order as the speaker
        self.firing: Rule | None = None

    # -- arming --------------------------------------------------------------------------

    def arm(self, rule: Rule) -> None:
        """Set a rule's runtime state as when it is given or resumed: armed, the
        accumulators empty, an `every` order due one interval from now."""
        rule.armed = True
        rule.reset_edge()
        rule.started = []
        if rule.trigger.kind == "every":
            rule.next_due_tick = self.world.clock.tick + rule.trigger.interval_s

    # -- the tick ------------------------------------------------------------------------

    def tick(self) -> None:
        world = self.world
        # the events logged since the last pass, without copying the log (a day's log is
        # long; package 29 counts ticks a second)
        events = [world.log[i] for i in range(self._seen_log, len(world.log))]
        self._seen_log = len(world.log)
        if not self.book.rules:
            return
        view = world.readings
        tick = world.clock.tick
        self._firings = [f for f in self._firings if tick - f.tick < STANDING_DWELL_S]
        for rule in list(self.book.rules):
            if rule.belayed or rule.held is not None:
                continue  # a held order waits, silent, for the reading it is on (33c)
            kind = rule.trigger.kind
            if kind == "when":
                self._tick_when(rule, view)
            elif kind == "at":
                spec = R.EVENTS[rule.trigger.event or ""]
                for e in events:
                    if (
                        R.event_matches(spec, e.kind, e.data)
                        and e.actor != f"{ACTOR_PREFIX}'{rule.name}'"
                    ):
                        self._fire(rule, view)
            elif kind == "every":
                if rule.next_due_tick is None:
                    rule.next_due_tick = rule.given_tick + rule.trigger.interval_s
                if tick >= rule.next_due_tick:
                    rule.next_due_tick += rule.trigger.interval_s
                    if self._still_queued(rule):
                        world.record(
                            Severity.ROUTINE,
                            "standing.held",
                            f"Standing order '{rule.name}' {rule.trigger.text}: held; the last "
                            f"firing's work is still waiting its turn.",
                            actor=f"{ACTOR_PREFIX}'{rule.name}'",
                            data={"name": rule.name},
                        )
                    else:
                        self._fire(rule, view)

    def _tick_when(self, rule: Rule, view: R.ReadingsView) -> None:
        cond = rule.trigger.condition
        assert cond is not None
        holds = cond.holds(view, rule.memory)
        if rule.armed:
            if holds:
                rule.held_s += TICK_SECONDS
                if rule.held_s >= rule.trigger.duration_s:
                    self._fire(rule, view)
                    rule.armed = False
                    rule.held_s = 0.0
                    rule.clear_s = 0.0
                    # a shift fired on is spent: 'veers a point' is measured afresh from the
                    # wind it fired on, so the rule stands again once the wind has held for
                    # the dwell, and fires at the next point (package 29b; before, a wind
                    # that veered and stayed kept the condition true and the rule never
                    # stood again)
                    rule.spend_shifts(view)
            else:
                rule.held_s = 0.0
            return
        # disarmed: the dwell
        if holds:
            rule.clear_s = 0.0
        else:
            rule.clear_s += TICK_SECONDS
        if rule.clear_s >= STANDING_DWELL_S and not self._still_working(rule):
            rule.armed = True
            # the duration and the dwell start again; a wind's shift is still measured
            # from the direction it fired on (`Rule.spend_shifts`)
            rule.held_s = 0.0
            rule.clear_s = 0.0

    # -- the runner's word on a firing's work ---------------------------------------------

    def _runner(self) -> Any:
        return (getattr(self.world.ship, "extra", None) or {}).get("evolutions")

    def _still_working(self, rule: Rule) -> bool:
        runner = self._runner()
        if runner is None or not rule.started:
            return False
        live = runner.instances
        return any(inst in live for inst in rule.started)

    def _still_queued(self, rule: Rule) -> bool:
        runner = self._runner()
        if runner is None or not rule.started:
            return False
        live = runner.instances
        return any(inst in live and inst.waiting for inst in rule.started)

    # -- firing --------------------------------------------------------------------------

    def _fire(self, rule: Rule, view: R.ReadingsView) -> None:
        world = self.world
        ship = world.ship
        actor = f"{ACTOR_PREFIX}'{rule.name}'"
        tick = world.clock.tick
        if rule.condition is not None and not rule.condition.holds(view, rule.memory):
            # the line the first time, then once a watch while the condition goes on
            # failing (spec M5 open item 15; package 33c: the gate's passage had a hundred
            # and fifty-seven of them, its two leads' `every ..., if` saying every ten
            # minutes that the run since noon was short)
            watch = (world.clock.ship_time.date().isoformat(), world.clock.watch())
            if rule.held_line_watch == watch:
                return
            rule.held_line_watch = watch
            world.record(
                Severity.ROUTINE,
                "standing.held",
                f"Standing order '{rule.name}' {rule.trigger.text}: not carried out; "
                f"{rule.condition.explain(view, rule.memory)}.",
                actor=actor,
                data={"name": rule.name, "reason": rule.condition.explain(view, rule.memory)},
            )
            return
        rule.held_line_watch = None  # it fires: the next failing `if` is said again
        firing = Firing(rule, tick)
        given: list[ActionParts] = []
        for text in rule.actions:
            parts = (
                action_parts(ship, text)
                if hasattr(ship, "parts")
                else ActionParts(text, "", frozenset({HELM}), frozenset())
            )
            if self._countermanded(rule, parts):
                continue
            given.append(parts)
        runner = self._runner()
        before = len(runner.instances) if runner is not None else 0
        self.firing = rule
        try:
            for parts in given:
                world.submit(
                    parts.text,
                    actor=actor,
                    said=f"By standing order '{rule.name}': {said_as_done(ship, parts.text)}",
                    # a cadence's firing is the watch's routine work: a routine line
                    routine=rule.trigger.kind == "every",
                )
        finally:
            self.firing = None
        firing.actions = given
        if runner is not None:
            rule.started = list(runner.instances[before:])
            firing.started = list(rule.started)
        if given:
            rule.fired += 1
            rule.last_fired_tick = tick
        self._firings.append(firing)

    def _countermanded(self, rule: Rule, parts: ActionParts) -> bool:
        """The conflict rule. True when this order must not be given."""
        world = self.world
        runner = self._runner()
        live = runner.instances if runner is not None else []
        for firing in self._firings:
            other = firing.rule
            if other is rule:
                continue
            if firing.started and not any(inst in live for inst in firing.started):
                # its work is done (package 33c): `at wore then heave to` follows the
                # wear, and `at filled away then shape a course` the filling away
                continue
            for theirs in firing.actions:
                shared = parts.conflicts_with(theirs)
                if not shared:
                    continue
                where = _where(world.ship, shared)
                if other.rank < rule.rank:
                    rule.conflicts += 1
                    world.record(
                        Severity.NOTABLE,
                        "standing.countermanded",
                        f"Standing order '{rule.name}' ({rule.officer}) countermanded by "
                        f"'{other.name}' ({other.officer}).",
                        actor=f"{ACTOR_PREFIX}'{rule.name}'",
                        data={
                            "name": rule.name,
                            "by": other.name,
                            "parts": sorted(shared),
                            "order": parts.text,
                        },
                    )
                    return True
                if other.rank > rule.rank:
                    other.conflicts += 1
                    world.record(
                        Severity.NOTABLE,
                        "standing.countermanded",
                        f"Standing order '{other.name}' ({other.officer}) countermanded by "
                        f"'{rule.name}' ({rule.officer}).",
                        actor=f"{ACTOR_PREFIX}'{rule.name}'",
                        data={
                            "name": other.name,
                            "by": rule.name,
                            "parts": sorted(shared),
                            "order": parts.text,
                        },
                    )
                    return False
                world.record(
                    Severity.ROUTINE,
                    "standing.conflict",
                    f"Standing orders '{other.name}' and '{rule.name}' (both {rule.officer}'s) "
                    f"give contrary orders on {where}; the later stands.",
                    actor=f"{ACTOR_PREFIX}'{rule.name}'",
                    data={"names": [other.name, rule.name], "parts": sorted(shared)},
                )
                return False
        return False

    # -- for `show standing order` ----------------------------------------------------------

    def status_lines(self, rule: Rule) -> list[str]:
        t = rule.trigger
        if t.kind == "when":
            if rule.armed:
                if t.duration_s and rule.held_s > 0:
                    return [
                        f"The condition has held {rule.held_s:.0f} s of the "
                        f"{t.duration_s} s it must."
                    ]
                return ["Armed; waiting for its condition."]
            if self._still_working(rule):
                return ["Fired; its work is still in hand."]
            return [
                f"Fired; it stands again when its condition has been false for "
                f"{STANDING_DWELL_S} s ({rule.clear_s:.0f} s so far)."
            ]
        if t.kind == "every" and rule.next_due_tick is not None:
            due = rule.next_due_tick - self.world.clock.tick
            return [f"Next due in {due} s."]
        return []


def _where(ship: Any, parts: frozenset[str]) -> str:
    """The parts two orders are contrary on, in words: every yard of the ship together as
    'the yards' (a manoeuvre's, package 33c), the rest by name."""
    yards = {s.id for s in getattr(ship, "spars", {}).values() if s.is_yard}
    words = []
    if yards and yards <= parts:
        words.append("the yards")
        parts = frozenset(p for p in parts if p not in yards)
    words += sorted(_part_words(ship, p) for p in parts)
    return errors.join_names(words, "and")


def _part_words(ship: Any, part: str) -> str:
    if part in (HELM, SHIP, CREW):
        return part
    if hasattr(ship, "parts") and part in ship.parts:
        return "the " + resolve.display_name(ship, part)
    return part
