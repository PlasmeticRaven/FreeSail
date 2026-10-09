"""The book of standing orders (spec M4 §3): list, show, belay, resume, belay all, and
strike (package 28c, the captain's `cancel standing order` of playtest 3).

**Belay and strike.** Belaying an order keeps it in the book, standing idle, to be
resumed; striking it takes it out of the book altogether, and its name is free again.

The book holds the rules in the order they were given, which is the order the runtime
evaluates them in and the order they are listed. A rule is entered by the dialect
(`grammar.handle`) or by the Python API (package 26) through `enter`, and its state
(standing or belayed, fired how often, last when) is saved with the game as `save()`
gives it. A replay re-enters every rule from the journal, so the saved book is what a
reader and a test check the replayed one against.

`read_orders_file` reads a file of standing orders for the drivers' `read the standing
orders from <file>`: one sentence a line, blank lines and `#` comments passed over. The
drivers submit each line as an order, so each is journaled and replays.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from freesail.orders import errors
from freesail.orders.errors import OrderError
from freesail.standing.rules import Rule

if TYPE_CHECKING:
    from freesail.standing.grammar import BookCommand
    from freesail.standing.runtime import Runtime

__all__ = ["Book", "read_orders_file"]

Result = tuple[str, str, dict[str, Any]]


# The readings that take a charted place, by their registry ids, and the words that mean
# the shore in sight and are no place on any chart (package 37f).
_CHART_READINGS = ("distance_to", "bearing_by_chart")
_SHORE_WORDS = frozenset(
    {"land", "shore", "coast", "nearest land", "nearest shore", "nearest coast", "land in sight"}
)


def check_places(rule: Rule, world: Any) -> None:
    """A standing order's condition is checked when it is entered (package 37f; the
    review of gate 5c's playtests, 5.8 and 8.2: the owner needed four tries at
    'Triangulate', since "the distance to the land" was taken into the book and then held
    at every firing as "not on the chart"). A condition on the distance to a place, or on
    its bearing by the chart, must name a place the chart has, or a position pricked on
    it; else the order is refused here, in words that give the nearest forms the dialect
    does take: for the shore in sight, "the nearest land"; for a name the chart nearly
    has, that name. A world with no chart checks nothing, as it reads nothing."""
    chart = getattr(world, "chart", None)
    if chart is None or getattr(world, "navigation", None) is None:
        return
    from freesail.api import readings as R

    for cond in (rule.trigger.condition, rule.condition):
        for clause in cond.clauses if cond is not None else ():
            if clause.reading not in _CHART_READINGS:
                continue
            for place in clause.params:
                if chart.find_feature(place) is None and R._pricked(place) is None:
                    raise OrderError(_no_such_place(chart, place, clause.reading))


def _no_such_place(chart: Any, place: str, reading: str) -> str:
    said = "the bearing by the chart of" if reading == "bearing_by_chart" else "the distance to"
    words = " ".join(place.lower().split())
    bare = words[4:] if words.startswith("the ") else words
    takes = (
        f"'{said}' takes a place by its name on the chart ('{said} the Lizard') or a "
        f"position pricked on it ('{said} 48 20 N 4 36 W')"
    )
    if bare in _SHORE_WORDS:
        return (
            f"'{place}' is not a place on the chart: {takes}. For the shore in sight say "
            f"'the nearest land' (as in 'when the nearest land is under half a mile'), and "
            f"for whether any land is in sight, 'the land is in sight'."
        )
    names = [f.name for f in chart.features.values() if f.name]
    near = errors.nearest(bare, [n.lower() for n in names])
    by_lower = {n.lower(): n for n in names}
    if near:
        hint = (
            " Did you mean "
            + errors.join_names([f"'{by_lower.get(n, n)}'" for n in near], "or")
            + "?"
        )
    else:
        hint = " For the shore in sight say 'the nearest land'."
    return f"'{place}' is not a place on the chart: {takes}.{hint}"


class Book:
    def __init__(self, runtime: Runtime | None = None):
        self.runtime = runtime
        self.rules: list[Rule] = []

    # -- lookup ----------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self):
        return iter(self.rules)

    @property
    def names(self) -> list[str]:
        return [r.name for r in self.rules]

    def get(self, name: str) -> Rule | None:
        key = " ".join(name.lower().split())
        for r in self.rules:
            if r.key == key:
                return r
        return None

    def loose(self, name: str) -> list[Rule]:
        """The rules a name said loosely may mean (package 33c; playtest 13's brig,
        `resume standing order "trim by the wind"` for "Trim Sails by the Wind"): those
        whose name has every word said, in the order said, case and quotes aside ('the
        well' for "sound the well")."""
        said = _name_words(name)
        if not said:
            return []
        out = []
        for r in self.rules:
            words = iter(_name_words(r.name))
            if all(any(w == x for x in words) for w in said):
                out.append(r)
        return out

    def find(self, name: str) -> Rule:
        rule = self.get(name)
        if rule is None:
            loose = self.loose(name)
            if len(loose) == 1:
                return loose[0]
            if len(loose) > 1:
                names = errors.join_names([f"'{r.name}'" for r in loose])
                raise OrderError(f"'{name}' could be standing order {names}; say which.")
            if not self.rules:
                raise OrderError(f"There is no standing order '{name}'; the book is empty.")
            near = errors.nearest(name, self.names)
            hint = (
                "; did you mean " + errors.join_names(f"'{h}'" for h in near) + "?" if near else "."
            )
            raise OrderError(f"There is no standing order '{name}' in the book{hint}")
        return rule

    # -- entering ----------------------------------------------------------------------

    def add(self, rule: Rule) -> Rule:
        """Enter a rule. A second rule of the same name is refused: belay the first or
        name the new one otherwise."""
        if self.get(rule.name) is not None:
            raise OrderError(
                f"There is a standing order '{rule.name}' in the book already; belay it, "
                f"or give the new one another name."
            )
        if self.runtime is not None:
            check_places(rule, self.runtime.world)
            rule.given_tick = self.runtime.world.clock.tick
            self.runtime.arm(rule)
        self.rules.append(rule)
        return rule

    def enter(self, rule: Rule) -> Result:
        """`add`, with the log line: what was entered and who gave it."""
        self.add(rule)
        by = f" by {rule.officer}" if rule.given_by != "captain" else ""
        text = f"Standing order '{rule.name}' entered in the book{by}: {rule.body_words()}."
        data: dict[str, Any] = {"name": rule.name, "given_by": rule.given_by}
        if rule.held is not None:
            # an order on a reading the ship has not got yet (package 33c): in the book,
            # held, and never fired until the world has it
            text += f" Held until the ship can carry it out: {rule.held}"
            data["held"] = rule.held
        return "standing.given", text, data

    # -- the book's orders ----------------------------------------------------------------

    def carry_out(self, command: BookCommand) -> Result:
        verb = command.verb
        if verb == "standing orders":
            return "query.standing_orders", "\n".join(self.lines()), {"names": self.names}
        if verb == "belay all standing orders":
            return self.belay_all()
        assert command.name is not None
        rule = self.find(command.name)
        if verb == "show standing order":
            return "query.standing_orders", "\n".join(self.show_lines(rule)), {"name": rule.name}
        if verb == "belay standing order":
            return self.belay(rule)
        if verb == "resume standing order":
            return self.resume(rule)
        if verb == "strike standing order":
            return self.strike(rule)
        raise OrderError(f"'{verb}' is not one of the book's orders.")

    def belay(self, rule: Rule) -> Result:
        if rule.belayed:
            raise OrderError(f"Standing order '{rule.name}' is belayed already.")
        rule.belayed = True
        return "standing.belayed", f"Standing order '{rule.name}' belayed.", {"name": rule.name}

    def resume(self, rule: Rule) -> Result:
        if not rule.belayed:
            raise OrderError(f"Standing order '{rule.name}' is standing; it was not belayed.")
        if rule.trigger.kind == "absent":
            # a Python rule loaded without its file (package 26, `python_api.restore_absent`)
            raise OrderError(f"Standing order '{rule.name}' {rule.trigger.text}.")
        rule.belayed = False
        if self.runtime is not None:
            self.runtime.arm(rule)
        return "standing.resumed", f"Standing order '{rule.name}' resumed.", {"name": rule.name}

    def strike(self, rule: Rule) -> Result:
        """Take the order out of the book: it is no longer listed, evaluated or saved,
        and its name may be given again. Journaled as an order like the rest of the book's
        orders, so a replay strikes it at the same tick. A belayed order is struck as it
        stands; belaying is the way to keep one idle."""
        self.rules.remove(rule)
        return (
            "standing.struck",
            f"Standing order '{rule.name}' struck from the book.",
            {"name": rule.name, "was_belayed": rule.belayed},
        )

    def belay_all(self) -> Result:
        standing = [r for r in self.rules if not r.belayed]
        if not self.rules:
            raise OrderError("There are no standing orders in the book to belay.")
        if not standing:
            raise OrderError("Every standing order in the book is belayed already.")
        for r in standing:
            r.belayed = True
        n = len(standing)
        text = "The one standing order belayed." if n == 1 else f"All {n} standing orders belayed."
        return "standing.belayed_all", text, {"names": [r.name for r in standing]}

    # -- lines for the log ---------------------------------------------------------------

    def _clock(self) -> Any:
        return self.runtime.world.clock if self.runtime is not None else None

    def lines(self) -> list[str]:
        """The listing: each order, who gave it, its text and its state."""
        if not self.rules:
            return ["There are no standing orders in the book."]
        n = len(self.rules)
        out = [f"Standing orders ({n}):"] if n > 1 else ["Standing orders (1):"]
        clock = self._clock()
        for r in self.rules:
            book = f", the book '{r.book}'" if getattr(r, "book", "") else ""
            out.append(
                f'  "{r.name}" ({r.officer}{book}): {r.body_words()}. '
                f"{r.state_words(clock)[0].upper()}{r.state_words(clock)[1:]}."
            )
        return out

    def show_lines(self, rule: Rule) -> list[str]:
        clock = self._clock()
        out = [
            f'Standing order "{rule.name}", given by {rule.officer}'
            + (f" ({rule.source})" if rule.source != "dialect" else "")
            + f": {rule.body_words()}.",
            f"{rule.state_words(clock)[0].upper()}{rule.state_words(clock)[1:]}.",
        ]
        if self.runtime is not None and not rule.belayed:
            out.extend(self.runtime.status_lines(rule))
        return out

    # -- saving ------------------------------------------------------------------------

    def save(self) -> list[dict[str, Any]]:
        return [r.save() for r in self.rules]

    def restore_state(self, saved: list[dict[str, Any]]) -> list[str]:
        """Apply saved state (belayed, fired, last fired) to the rules of the same names.
        Returns the names in the save that the book has no rule for, so a caller can say
        so (a Python rule whose file is absent, package 26)."""
        missing: list[str] = []
        for entry in saved:
            rule = self.get(str(entry.get("name", "")))
            if rule is None:
                missing.append(str(entry.get("name", "")))
                continue
            rule.belayed = bool(entry.get("belayed", False))
            rule.fired = int(entry.get("fired", 0))
            rule.last_fired_tick = entry.get("last_fired_tick")
        return missing


def _name_words(name: str) -> list[str]:
    """A standing order's name as its words are matched: lower case, no punctuation."""
    return "".join(c if c.isalnum() or c.isspace() else " " for c in name.lower()).split()


def read_orders_file(path: str | Path) -> list[str]:
    """The standing orders in a file: one a line; blank lines and `#` comments passed over.
    A sentence may continue on the next lines when those are indented."""
    text = Path(path).read_text(encoding="utf-8")
    out: list[str] = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue
        if raw[:1].isspace() and out:
            out[-1] = out[-1] + " " + line.strip()
        else:
            out.append(line.strip())
    return out
