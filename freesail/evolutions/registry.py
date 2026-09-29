"""The evolution catalogue: every ``data/evolutions/*.yaml`` file, read at import.

An *evolution* is a named piece of seamanship (set a topsail, reef the
mainsail, tack ship) written as a data file. This module reads the files,
checks that each one is well formed, parses every expression in it once
(so a typo fails at import, not in the middle of a game), and keeps the
result in ``EVOLUTIONS``, a dictionary by id.

The file shape (spec §8.4, with the additions the runner needs)::

    id: set_square                 # the evolution's id; the file name must match
    verb: set                      # the order verb it answers (for the vocabulary)
    applies_to: {class: square}    # the subject's class: a sail or spar class, "sail" (any
                                   # sail), "yard", "spar" (any spar), "part" (a spar or a
                                   # sail: clearing a wreck, package 30b), or "ship"
    params: {reefs: 1}             # optional; defaults for order parameters
    preconditions:                 # checked when the evolution starts
      - {check: sail.state != set, reason: "The {sail} is already set."}
    requires:                      # checked at the start and again before every step
      - {check: not wrecked(spar_chain(sail)), reason: "The {sail}'s spars are wrecked."}
    steps:
      - do: loose                  # a name for the step, shown in the state snapshot
        duration_s: 90             # nominal duration, scaled by the weather factor
        sets: {sail.state: loosed} # attributes assigned when the step ends
        ramp: {yard.brace_angle: deg(30)}  # attributes moved smoothly over the step
        via: halyard_of(sail)      # optional; the line used. Absent line: step skipped;
                                   # parted line: evolution fails
        if: sail.state == set      # optional; the step runs only when this holds
        log: "Sheeted home the {sail}."   # optional; a routine note when the step ends
        aloft: true                # optional; the work is aloft (default: on deck), which
                                   # decides the skill the crew factor reads (spec M3 §3.3)
    on_start:    {log: "Hands aloft to loose the {sail}."}
    on_complete: {log: "Set the {sail}.", kind: sail.set, severity: notable}
    on_fail:     {log: "Could not set the {sail}: {reason}", kind: evolution.failed}
    crew: {hands: 12, rating: ordinary}   # authored now, used by the M3 task system
    source: "Luce 1866, ch. XXIII At Sea, 'To set a Topsail'"

Each state a subject starts from may be its own case (package 29b, the owner's rule): a
step may say ``instead_of: <do>`` when it stands, from another state, for a step of the
same file (a sail set from the gear lets go its gear on deck instead of being loosed
aloft), and the nominal duration counts the step it replaces; an outcome may give
``from: {<state>: <log>}``, its line when the subject starts in that state.

An all-hands manoeuvre (``crew: {hands: all}``: tack, wear, box-haul, lie a-try) also
says ``belays: true``: "Ready about!" stops the sail work in hand, which holds its
progress and resumes after (spec M3 §3.4). All-hands sail work (a reef, a furl, sending
down the topgallant masts) leaves it out and belays nothing: the owner's ruling of
2026-09-29 at gate 4c.

A scripted manoeuvre (tack, wear, heave to, fill away) has no ``steps``;
instead it names a Python script and gives that script its timings::

    script: tack
    timing: {brace_s: 45, stays_timeout_s: 180}

A precondition may also be written as a bare expression string, in which
case the reason shown is the expression itself; the files always give a
reason in words. The words in ``{braces}`` are filled in by the runner
(``{sail}``, ``{yard}``, ``{subject}``, ``{reason}``, ``{state}``,
``{reefs}``, ``{speed}``, ``{tack}``, ``{heading}`` and any parameter).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from freesail.evolutions import expr

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "evolutions"


class EvolutionFileError(ValueError):
    """An evolution file the runner cannot accept. The message is a sentence."""


@dataclass
class Condition:
    text: str  # the expression as written
    reason: str  # what to say when it does not hold
    tree: expr.Node


@dataclass
class Step:
    do: str
    duration_s: float
    sets: dict[str, tuple[expr.Node, str, expr.Node]] = field(default_factory=dict)
    ramp: dict[str, tuple[expr.Node, str, expr.Node]] = field(default_factory=dict)
    via: expr.Node | None = None
    condition: expr.Node | None = None
    log: str | None = None
    aloft: bool = False  # work on the yards or in the tops (spec M3 §3.3); else on deck
    # the step this one stands in for from another state (a sail set from the gear lets go
    # its gear instead of loosing it aloft; package 29b): the two are alternatives, and the
    # nominal duration counts the one it replaces
    instead_of: str | None = None


@dataclass
class Outcome:
    log: str
    kind: str
    severity: str
    # the log's words when the subject is in a given state at the start (``from:`` in the
    # file, by state: a sail set from the gear is not loosed aloft; package 29b)
    from_state: dict[str, str] = field(default_factory=dict)


@dataclass
class Evolution:
    id: str
    verb: str
    applies_to: dict[str, Any]
    params: dict[str, Any]
    preconditions: list[Condition]
    requires: list[Condition]
    steps: list[Step]
    on_start: Outcome
    on_complete: Outcome
    on_fail: Outcome
    crew: dict[str, Any]
    source: str
    script: str | None = None
    timing: dict[str, float] = field(default_factory=dict)
    path: str = "<memory>"
    belays: bool = False  # an all-hands manoeuvre stops the sail work in hand (spec M3 §3.4)

    @property
    def nominal_duration_s(self) -> float:
        """The steps' durations, an alternative (`Step.instead_of`) not counted."""
        return sum(s.duration_s for s in self.steps if s.instead_of is None)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def _condition(raw: Any, where: str) -> Condition:
    if isinstance(raw, str):
        text, reason = raw, f"the condition '{raw}' does not hold"
    elif isinstance(raw, dict) and "check" in raw:
        text = str(raw["check"])
        reason = str(raw.get("reason") or f"the condition '{text}' does not hold")
    else:
        raise EvolutionFileError(
            f"{where}: a precondition must be an expression or a {{check, reason}} mapping."
        )
    try:
        tree = expr.parse(text)
    except expr.ExpressionError as e:
        raise EvolutionFileError(f"{where}: {e}") from None
    return Condition(text=text, reason=reason, tree=tree)


def _targets(raw: Any, where: str) -> dict[str, tuple[expr.Node, str, expr.Node]]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise EvolutionFileError(f"{where}: 'sets' and 'ramp' must be mappings.")
    out = {}
    for target, value in raw.items():
        try:
            obj_tree, attr = expr.split_target(str(target))
            value_tree = expr.parse(str(value))
        except expr.ExpressionError as e:
            raise EvolutionFileError(f"{where}: {e}") from None
        out[str(target)] = (obj_tree, attr, value_tree)
    return out


def _optional_expr(raw: Any, where: str) -> expr.Node | None:
    if raw is None:
        return None
    try:
        return expr.parse(str(raw))
    except expr.ExpressionError as e:
        raise EvolutionFileError(f"{where}: {e}") from None


def _step(raw: Any, i: int, where: str) -> Step:
    if not isinstance(raw, dict) or "do" not in raw:
        raise EvolutionFileError(f"{where}: step #{i + 1} needs at least a 'do' name.")
    here = f"{where}, step '{raw['do']}'"
    duration = raw.get("duration_s", 0)
    if isinstance(duration, bool) or not isinstance(duration, int | float) or duration < 0:
        raise EvolutionFileError(
            f"{here}: duration_s must be a number of seconds, not {duration!r}."
        )
    aloft = raw.get("aloft", False)
    if not isinstance(aloft, bool):
        raise EvolutionFileError(f"{here}: aloft must be true or false, not {aloft!r}.")
    return Step(
        do=str(raw["do"]),
        duration_s=float(duration),
        sets=_targets(raw.get("sets"), here),
        ramp=_targets(raw.get("ramp"), here),
        via=_optional_expr(raw.get("via"), here),
        condition=_optional_expr(raw.get("if"), here),
        log=str(raw["log"]) if raw.get("log") else None,
        aloft=aloft,
        instead_of=str(raw["instead_of"]) if raw.get("instead_of") else None,
    )


def _outcome(raw: Any, default_log: str, default_kind: str, default_severity: str) -> Outcome:
    raw = raw or {}
    if not isinstance(raw, dict):
        raise EvolutionFileError("on_start, on_complete and on_fail must be mappings.")
    from_state = raw.get("from") or {}
    if not isinstance(from_state, dict):
        raise EvolutionFileError("An outcome's 'from' must map a state to its log line.")
    return Outcome(
        log=str(raw.get("log") or default_log),
        kind=str(raw.get("kind") or default_kind),
        severity=str(raw.get("severity") or default_severity),
        from_state={str(k): str(v) for k, v in from_state.items()},
    )


def parse_evolution(data: Any, path: str = "<memory>") -> Evolution:
    """Turn a loaded YAML mapping into an Evolution, checking its shape."""
    if not isinstance(data, dict):
        raise EvolutionFileError(f"{path}: the file is not a mapping at the top level.")
    eid = str(data.get("id") or "").strip()
    if not eid:
        raise EvolutionFileError(f"{path}: 'id' is missing.")
    where = f"{path} ({eid})"
    source = str(data.get("source") or "").strip()
    if not source:
        raise EvolutionFileError(f"{where}: 'source' is missing; cite the chapter it comes from.")
    applies_to = data.get("applies_to") or {}
    if not isinstance(applies_to, dict) or "class" not in applies_to:
        raise EvolutionFileError(f"{where}: 'applies_to' must give a class.")
    script = data.get("script")
    steps_raw = data.get("steps")
    if script is None and not steps_raw:
        raise EvolutionFileError(f"{where}: give either 'steps' or a 'script'.")
    if script is not None and steps_raw:
        raise EvolutionFileError(f"{where}: give 'steps' or a 'script', not both.")
    steps = [_step(s, i, where) for i, s in enumerate(steps_raw or [])]
    names = {s.do for s in steps}
    for s in steps:
        if s.instead_of is not None and s.instead_of not in names:
            raise EvolutionFileError(
                f"{where}, step '{s.do}': it stands instead of '{s.instead_of}', which is not "
                "a step of this file."
            )
    params = data.get("params") or {}
    if not isinstance(params, dict):
        raise EvolutionFileError(f"{where}: 'params' must be a mapping of defaults.")
    timing = data.get("timing") or {}
    if not isinstance(timing, dict):
        raise EvolutionFileError(f"{where}: 'timing' must be a mapping.")
    crew = dict(data.get("crew") or {})
    belays = data.get("belays", False)
    if not isinstance(belays, bool):
        raise EvolutionFileError(f"{where}: belays must be true or false, not {belays!r}.")
    if belays and str(crew.get("hands", "")).strip().lower() != "all":
        raise EvolutionFileError(
            f"{where}: only an all-hands evolution belays the work in hand; "
            "its crew line must say hands: all."
        )
    return Evolution(
        id=eid,
        verb=str(data.get("verb") or eid),
        applies_to=dict(applies_to),
        params=dict(params),
        preconditions=[_condition(c, where) for c in data.get("preconditions") or []],
        requires=[_condition(c, where) for c in data.get("requires") or []],
        steps=steps,
        on_start=_outcome(
            data.get("on_start"), "Began {id} on the {subject}.", "evolution.started", "routine"
        ),
        on_complete=_outcome(
            data.get("on_complete"),
            "Completed {id} on the {subject}.",
            "evolution.completed",
            "notable",
        ),
        on_fail=_outcome(
            data.get("on_fail"),
            "Could not complete {id} on the {subject}: {reason}",
            "evolution.failed",
            "notable",
        ),
        crew=crew,
        source=source,
        script=str(script) if script is not None else None,
        timing={str(k): float(v) for k, v in timing.items()},
        path=path,
        belays=belays,
    )


def load_file(path: str | Path) -> Evolution:
    path = Path(path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise EvolutionFileError(f"{path}: the file is not valid YAML ({e}).") from None
    evo = parse_evolution(data, str(path))
    if evo.id != path.stem:
        raise EvolutionFileError(f"{path}: id '{evo.id}' does not match the file name.")
    return evo


def load_directory(directory: str | Path = DATA_DIR) -> dict[str, Evolution]:
    """Read every ``*.yaml`` in a directory into a dictionary by id."""
    directory = Path(directory)
    out: dict[str, Evolution] = {}
    for path in sorted(directory.glob("*.yaml")):
        evo = load_file(path)
        if evo.id in out:
            raise EvolutionFileError(f"{path}: id '{evo.id}' is defined twice.")
        out[evo.id] = evo
    return out


EVOLUTIONS: dict[str, Evolution] = load_directory() if DATA_DIR.is_dir() else {}


def get(evolution_id: str) -> Evolution | None:
    return EVOLUTIONS.get(evolution_id)
