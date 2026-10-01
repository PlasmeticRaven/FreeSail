"""The Python API of standing orders (spec M4 §4): the level-3 sketch of proposal §4.3,
made thin on purpose.

    from freesail.standing import bind, when, at, every, order

    bind(world)

    @when("the true wind exceeds 30 knots", for_minutes=2, name="shorten sail for weather")
    def shorten_sail():
        order("take in the studdingsails")
        order("take in the royals")
        order("reef the topsails, one reef")

    @at("sunset", name="night routine")
    def night_routine():
        order("take in the studdingsails")
        order("take in the royals")

    @at("sunrise", condition="the true wind is under 20 knots", name="morning sail")
    def morning_sail():
        order("set the royals")

There is one engine. A decorator builds the same `Rule` the dialect parses to (the same
`Trigger`, the condition parsed by `standing.parse_condition` from the dialect's own
words, the orders as order texts checked by the imperative grammar against the ship),
enters it in the same book, and the same runtime evaluates it and fires it through the
same `World.submit`, so the log reads "By standing order 'night routine': ..." whoever
wrote the rule. A Python rule is marked `source="python"` and `trusted=True` (it ran
in-process; milestone 6's sandbox is where the body runs, not a second engine).

**Binding.** A rule is entered in one world's book, so registration needs a world:
`bind(world)` names it once (a module-level default, as a script or the console would
set it), and any decorator may name another with `world=`. There is no default before
`bind`: a decorator without a bound world refuses in words rather than guess.

**The body runs once, at registration.** The decorated function is called as the rule is
entered, and every `order(...)` it calls is collected, in order, into the rule's action
list. Why then and not at firing: the rule is then exactly a dialect twin (a fixed list
of orders the conflict rule can read parts from, `show standing order` can print, and
the book can save as text), and a misspelt sail is refused when the rule is given, as
the dialect refuses it, not on a dark night when it fires. The body may call only
`order(...)` and read the readings object it is handed (`ReadingsView`, if it takes an
argument): the numbers at the moment of registration, never the World. Computation on
the readings *at firing* is what milestone 6's sandbox adds, under a time budget.

**Saving and loading.** A Python rule saves as its name, its source text (the decorated
function's source, or its module and name when the source cannot be read) and
`source: python`. A save loaded without the module that defined it (`restore_absent`)
lists the rule in the book, belayed, with the sentence that its file is not loaded, and
`resume` refuses it with the same sentence; the rule runs again when its module is
imported against the loaded world.
"""

from __future__ import annotations

import inspect
import textwrap
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from freesail.api import readings as R
from freesail.core.events import Severity
from freesail.orders.errors import OrderError
from freesail.orders.vocabulary import load_vocabulary
from freesail.standing import grammar
from freesail.standing.rules import Condition, Rule, Trigger

if TYPE_CHECKING:
    from freesail.core.world import World

__all__ = [
    "ABSENT_PYTHON",
    "at",
    "bind",
    "bound",
    "every",
    "order",
    "restore_absent",
    "unbind",
    "when",
]

# The sentence for a Python rule loaded without its file (spec §4).
ABSENT_PYTHON = "was written in Python and its file is not loaded; it is listed and will not run"

_bound: World | None = None
_collecting: list[str] | None = None


# ---------------------------------------------------------------------------
# Binding
# ---------------------------------------------------------------------------


def bind(world: World) -> World:
    """Name the world whose book the decorators enter rules in. Returns it."""
    global _bound
    _bound = world
    return world


def unbind() -> None:
    global _bound
    _bound = None


def bound() -> World:
    if _bound is None:
        raise OrderError(
            "No world is bound for the standing orders written in Python; call "
            "freesail.standing.bind(world) first, or say world=... on the decorator."
        )
    return _bound


# ---------------------------------------------------------------------------
# The body's one call
# ---------------------------------------------------------------------------


def order(text: str) -> None:
    """Give an order from a rule's body. Collected into the rule's action list."""
    if _collecting is None:
        raise OrderError(
            "order(...) may only be called inside a rule's body, under @when, @at or @every."
        )
    text = " ".join(str(text).split())
    if not text:
        raise OrderError("order('') gives no order.")
    _collecting.append(text)


# ---------------------------------------------------------------------------
# The decorators
# ---------------------------------------------------------------------------


def when(
    condition: str,
    *,
    for_minutes: float | None = None,
    for_seconds: float | None = None,
    name: str | None = None,
    by: str = "captain",
    world: World | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """`when <condition> [for <duration>]`: the condition in the dialect's words."""
    seconds = 0
    if for_minutes is not None:
        seconds += int(round(float(for_minutes) * 60))
    if for_seconds is not None:
        seconds += int(round(float(for_seconds)))
    if seconds < 0:
        raise OrderError("A duration is not negative.")

    def decorate(fn: Callable[..., Any]) -> Callable[..., Any]:
        w = world or bound()
        cond = grammar.parse_condition(condition, w.ship)
        text = f"when {cond.text}" + (f" for {grammar._duration_words(seconds)}" if seconds else "")
        trigger = Trigger("when", text, condition=cond, duration_s=seconds)
        return _register(fn, w, trigger, None, name, by)

    return decorate


def at(
    event: str,
    *,
    condition: str | None = None,
    name: str | None = None,
    by: str = "captain",
    world: World | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """`at <event> [, if <condition>]`: an event of `readings.EVENTS` by its words."""

    def decorate(fn: Callable[..., Any]) -> Callable[..., Any]:
        w = world or bound()
        words = " ".join(str(event).lower().split())
        spec = R.EVENTS.get(words) or R.EVENTS.get("the " + words)
        if spec is None:
            known = list(R.EVENTS)
            raise OrderError(
                f"'at {words}' names no event the ship knows. The events are {', '.join(known)}."
            )
        if spec.absent:
            raise OrderError(spec.absent)
        trigger = Trigger("at", f"at {spec.words}", event=spec.words)
        return _register(fn, w, trigger, _condition(condition, w), name, by)

    return decorate


def every(
    interval: str,
    *,
    condition: str | None = None,
    name: str | None = None,
    by: str = "captain",
    world: World | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """`every <interval> [, if <condition>]`: 'a glass', 'an hour', '20 minutes'."""

    def decorate(fn: Callable[..., Any]) -> Callable[..., Any]:
        w = world or bound()
        tokens = " ".join(str(interval).lower().split()).split()
        seconds = grammar.parse_duration(tokens, every=True)
        trigger = Trigger("every", f"every {' '.join(tokens)}", interval_s=seconds)
        return _register(fn, w, trigger, _condition(condition, w), name, by)

    return decorate


def _condition(text: str | None, world: World) -> Condition | None:
    return grammar.parse_condition(text, world.ship) if text else None


def _register(
    fn: Callable[..., Any],
    world: World,
    trigger: Trigger,
    condition: Condition | None,
    name: str | None,
    by: str,
) -> Callable[..., Any]:
    global _collecting
    rule_name = " ".join((name or fn.__name__.replace("_", " ")).split())
    actions = _collect(fn, world)
    if not actions:
        raise OrderError(f"Standing order '{rule_name}' gives no orders; call order(...) in it.")
    # the orders checked as the dialect checks them, at give time, against this ship
    ship = world.ship
    held: str | None = None
    if hasattr(ship, "parts"):
        actions, held = grammar._parse_actions(
            "; ".join(actions), ship, load_vocabulary(), rule_name
        )
    try:
        rule = Rule(
            name=rule_name,
            trigger=trigger,
            actions=actions,
            condition=condition,
            given_by=by,
            text=_source_of(fn),
            source="python",
            trusted=True,
            given_tick=world.clock.tick,
            held=held,  # an order on a reading the ship has not got yet (package 33c)
        )
    except ValueError:
        raise OrderError(
            f"'{by}' is no officer who gives standing orders; say the captain, the first "
            f"lieutenant, a lieutenant, the master, a master's mate or a midshipman."
        ) from None
    kind, text, data = world.standing.book.enter(rule)
    world.record(Severity.ROUTINE, kind, text, actor=rule.given_by, data=data)
    fn.rule = rule  # type: ignore[attr-defined]
    return fn


def _collect(fn: Callable[..., Any], world: World) -> list[str]:
    """Run the body once and gather its order(...) calls. It is handed the readings if
    it asks for them (one positional parameter), and nothing else."""
    global _collecting
    wants = False
    try:
        params = inspect.signature(fn).parameters
        wants = len(params) >= 1
    except (TypeError, ValueError):
        wants = False
    _collecting = []
    try:
        if wants:
            fn(world.readings)
        else:
            fn()
        return list(_collecting)
    finally:
        _collecting = None


def _source_of(fn: Callable[..., Any]) -> str:
    try:
        return textwrap.dedent(inspect.getsource(fn)).strip()
    except (OSError, TypeError):
        return f"python: {fn.__module__}.{fn.__qualname__}"


# ---------------------------------------------------------------------------
# Loading a save whose Python rules have no module present
# ---------------------------------------------------------------------------


def restore_absent(world: World, saved: list[dict[str, Any]]) -> list[Rule]:
    """Enter, belayed, a placeholder for each Python rule in a saved book that the
    world's book has not got (its module was not imported against this world), with
    the sentence; the dialect's rules are re-entered by the replay of the journal and
    are not touched. Returns the placeholders entered."""
    out: list[Rule] = []
    book = world.standing.book
    for entry in saved:
        if entry.get("source") != "python":
            continue
        name = str(entry.get("name", ""))
        if not name or book.get(name) is not None:
            continue
        rule = Rule(
            name=name,
            trigger=Trigger("absent", ABSENT_PYTHON),
            actions=["(not loaded)"],
            given_by=str(entry.get("given_by", "captain")),
            text=str(entry.get("text", "")),
            source="python",
            trusted=False,
            belayed=True,
            fired=int(entry.get("fired", 0)),
            last_fired_tick=entry.get("last_fired_tick"),
            given_tick=int(entry.get("given_tick", 0)),
        )
        book.add(rule)
        rule.belayed = True  # `add` arms it; it stays belayed until its file is back
        world.record(
            Severity.NOTABLE,
            "standing.absent",
            f"Standing order '{name}' {ABSENT_PYTHON}.",
            actor="sim",
            data={"name": name},
        )
        out.append(rule)
    return out
